import os
import shutil
import uuid
import torch
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from backend.app.services.transcriber import transcribe_audio
from backend.app.services.translator import translate_to_english
import logging

logger = logging.getLogger("fir_copilot.api.forthright")
router = APIRouter()

TEMP_DIR = "data/temp_audio"
os.makedirs(TEMP_DIR, exist_ok=True)


@router.post("/forthright/transcribe")
async def transcribe(
    file: UploadFile = File(...),
    translate: bool = Form(True)
):
    try:
        # Save uploaded file
        file_ext = os.path.splitext(file.filename)[1] or ".wav"
        temp_file_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}{file_ext}")
        
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        logger.info("Saved temp audio upload to %s", temp_file_path)
        
        # Transcribe audio
        transcript = transcribe_audio(temp_file_path)
        
        # Clean up temp file
        try:
            os.remove(temp_file_path)
        except Exception as e:
            logger.warning("Failed to remove temp audio file: %s", e)
            
        # Translate if requested
        translation = ""
        if translate and transcript:
            translation = translate_to_english(transcript)
            
        return {
            "status": "success",
            "transcript": transcript,
            "translation": translation or transcript
        }
    except Exception as e:
        logger.error("Error in transcribe endpoint: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/forthright/translate")
async def translate_text(data: dict):
    try:
        text = data.get("text", "")
        if not text:
            return {"status": "success", "translation": ""}
            
        translation = translate_to_english(text)
        return {
            "status": "success",
            "translation": translation
        }
    except Exception as e:
        logger.error("Error in translate endpoint: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cuda/status")
def get_cuda_status():
    cuda_available = torch.cuda.is_available()
    device_name = ""
    gpu_memory_allocated = 0
    gpu_memory_reserved = 0
    
    if cuda_available:
        device_name = torch.cuda.get_device_name(0)
        gpu_memory_allocated = torch.cuda.memory_allocated(0)
        gpu_memory_reserved = torch.cuda.memory_reserved(0)
        
    return {
        "status": "success",
        "cuda_available": cuda_available,
        "device_name": device_name,
        "gpu_memory": {
            "allocated_mb": round(gpu_memory_allocated / (1024 * 1024), 2),
            "reserved_mb": round(gpu_memory_reserved / (1024 * 1024), 2)
        },
        "whisper_device": "cuda" if cuda_available else "cpu"
    }
