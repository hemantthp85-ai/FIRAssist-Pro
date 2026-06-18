import os
import torch
import logging
from faster_whisper import WhisperModel

logger = logging.getLogger("fir_copilot.services.transcriber")

# CUDA / GPU Detection
device = "cuda" if torch.cuda.is_available() else "cpu"
compute_type = "float16" if device == "cuda" else "int8"
# Use large-v3 for maximum accuracy on GPU, base model for speed on CPU
model_size = "large-v3" if device == "cuda" else "base"

logger.info(
    "TRANSCRIPTION DEVICE DETECTED: %s, COMPUTE TYPE: %s, MODEL: %s",
    device.upper(),
    compute_type,
    model_size
)

# Load model (lazy loading to prevent blocking backend startup unnecessarily)
model = None


def get_model():
    global model
    if model is None:
        logger.info("Loading Whisper model: %s on %s...", model_size, device)
        model = WhisperModel(
            model_size,
            device=device,
            compute_type=compute_type,
            cpu_threads=4
        )
        logger.info("Whisper model loaded successfully")
    return model


def transcribe_audio(audio_path: str) -> str:
    try:
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found at: {audio_path}")

        whisper_model = get_model()
        segments, info = whisper_model.transcribe(
            audio_path,
            beam_size=1,
            best_of=1,
            temperature=0.0,
            condition_on_previous_text=False,
            vad_filter=True,
            repetition_penalty=1.2
        )

        text = ""
        for segment in segments:
            text += segment.text + " "

        text = text.strip()
        logger.info("Audio transcription complete: %s characters", len(text))
        return text

    except Exception as e:
        logger.error("Error transcribing audio: %s", e)
        raise e
