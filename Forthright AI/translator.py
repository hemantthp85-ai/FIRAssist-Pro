import requests

def translate_to_english(text):

    prompt = f"""
You are a translator.

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

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "gemma3:4b",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"].strip()