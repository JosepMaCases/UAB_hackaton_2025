import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("PUBLICAI_API_KEY")
BASE_URL = "https://api.publicai.co/v1/chat/completions"
MODEL = "BSC-LT/salamandra-7b-instruct-tools-16k"

if not API_KEY:
    raise RuntimeError("Falta PUBLICAI_API_KEY al .env")

def ask_salamandra(messages, max_tokens=512, temperature=0.4):
    """
    messages = [
        {"role": "system", "content": "..."},
        {"role": "user", "content": "Hola"}
    ]
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    resp = requests.post(BASE_URL, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"]
