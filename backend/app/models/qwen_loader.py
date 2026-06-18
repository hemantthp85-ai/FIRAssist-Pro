import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import threading

from backend.app.utils.performance import (
    cached_call,
    timed_agent
)

logger = logging.getLogger("fir_copilot.qwen_loader")

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_TAGS_URL = "http://localhost:11434/api/tags"
OLLAMA_PS_URL = "http://localhost:11434/api/ps"
MODEL_NAME = "qwen2.5:3b"

# Global session with connection pooling and retries
_session = None
_lock = threading.Lock()


def get_session():
    global _session
    if _session is None:
        with _lock:
            if _session is None:
                session = requests.Session()
                # Exponential backoff retry strategy
                retries = Retry(
                    total=5,
                    backoff_factor=0.5,
                    status_forcelist=[500, 502, 503, 504],
                    raise_on_status=False
                )
                adapter = HTTPAdapter(
                    pool_connections=20,
                    pool_maxsize=40,
                    max_retries=retries
                )
                session.mount("http://", adapter)
                session.mount("https://", adapter)
                _session = session
    return _session


def get_model_status() -> dict:
    try:
        session = get_session()
        
        # Check if Ollama is running and lists models
        tags_response = session.get(OLLAMA_TAGS_URL, timeout=5)
        if tags_response.status_code != 200:
            return {"status": "error", "message": f"Ollama tags endpoint returned {tags_response.status_code}"}
            
        tags_data = tags_response.json()
        models = [m.get("name") for m in tags_data.get("models", [])]
        
        if MODEL_NAME not in models:
            return {
                "status": "error",
                "message": f"Model '{MODEL_NAME}' is not pulled in Ollama. Available: {models}"
            }
            
        # Check currently loaded models
        ps_response = session.get(OLLAMA_PS_URL, timeout=5)
        is_loaded = False
        if ps_response.status_code == 200:
            ps_data = ps_response.json()
            loaded_models = [m.get("name") for m in ps_data.get("models", [])]
            is_loaded = MODEL_NAME in loaded_models or any(MODEL_NAME in name for name in loaded_models)
            
        return {
            "status": "healthy",
            "model": MODEL_NAME,
            "available_models": models,
            "currently_loaded": is_loaded
        }
    except Exception as e:
        logger.error("Error checking Qwen model health: %s", e)
        return {"status": "unhealthy", "message": str(e)}


def warm_qwen_model():
    logger.info("Warming up Qwen model '%s' (keep_alive = -1)...", MODEL_NAME)
    payload = {
        "model": MODEL_NAME,
        "prompt": "Hello",
        "stream": False,
        "keep_alive": -1  # Keep model in memory indefinitely
    }

    try:
        response = get_session().post(
            OLLAMA_URL,
            json=payload,
            timeout=30
        )
        logger.info("WARMUP STATUS: %s", response.status_code)
        response.raise_for_status()
        
        logger.info("Qwen warmup completed successfully")
        return response.json().get("response", "")
    except Exception as e:
        logger.error("Qwen model warmup failed: %s", e)
        raise e


def _ask_qwen_uncached(prompt: str):
    # Configure fast options for generation
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "keep_alive": -1,  # Keep model in memory
        "options": {
            "temperature": 0.0,  # Speed and consistency
            "num_predict": 2048,  # Prevent infinite generation
        }
    }

    response = get_session().post(
        OLLAMA_URL,
        json=payload
    )

    response.raise_for_status()
    return response.json()["response"]


@timed_agent("qwen_model")
def ask_qwen(prompt: str):
    return cached_call(
        "qwen_prompt",
        {
            "model": MODEL_NAME,
            "prompt": prompt
        },
        _ask_qwen_uncached,
        prompt
    )