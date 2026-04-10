import os
import requests

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://host.docker.internal:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "gemma3:4b")

def generate(prompt):
    url = f"{OLLAMA_HOST}/api/generate"
    response = requests.post(
        url,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )
    response.raise_for_status()
    data = response.json()
    return data["response"]