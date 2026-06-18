import logging
from backend.app.models.qwen_loader import ask_qwen

logger = logging.getLogger("fir_copilot.services.translator")


def translate_to_english(text: str) -> str:
    if not text or not text.strip():
        return ""

    # Check if text is likely already english (quick check to save LLM calls)
    # But Qwen is very fast with cache, so we can always run it to normalize the text
    prompt = f"""
You are an expert police translator.

Translate the complaint into English.

Preserve:
- Names
- Locations
- Dates
- Facts

Do not explain.
Do not provide options.
Return only the English translation.

Complaint:
{text}

English:
"""
    logger.info("Translating complaint text to English...")
    try:
        translation = ask_qwen(prompt)
        logger.info("Translation completed successfully")
        return translation.strip()
    except Exception as e:
        logger.error("Translation failed: %s, returning original text", e)
        return text
