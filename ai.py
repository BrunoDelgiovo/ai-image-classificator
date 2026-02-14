import base64
import os
import requests

ollama_url = os.getenv("ollama_url", "http://localhost:11434/api/generate")
ollama_model = os.getenv("ollama_model", "llava:latest")


def _img_b64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def describe_image(image_path: str) -> str:
    prompt = (
        "descreva a imagem em 1-2 frases e sugira uma categoria curta. "
        "responda exatamente no formato: descricao | categoria"
    )

    payload = {
        "model": ollama_model,
        "prompt": prompt,
        "stream": False,
        "images": [_img_b64(image_path)],
    }

    r = requests.post(ollama_url, json=payload, timeout=180)
    if r.status_code != 200:
        print("status:", r.status_code)
        print("body:", r.text)
        r.raise_for_status()

    data = r.json()
    return (data.get("response") or "").strip()
