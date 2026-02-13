import os
from dotenv import load_dotenv
from google import genai
from google.genai import types


def _guess_mime(path: str) -> str:
    p = path.lower()
    if p.endswith(".png"):
        return "image/png"
    if p.endswith(".webp"):
        return "image/webp"
    return "image/jpeg"


def describe_image(image_path: str) -> str:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

    if not api_key:
        raise RuntimeError("Defina GEMINI_API_KEY no .env")

    client = genai.Client(api_key=api_key)

    with open(image_path, "rb") as f:
        img_bytes = f.read()

    prompt = (
        "Descreva a imagem em 1-2 frases e sugira uma categoria curta. "
        "Responda exatamente no formato: descrição | categoria"
    )

    resp = client.models.generate_content(
        model=model,
        contents=[
            types.Part.from_text(prompt),
            types.Part.from_bytes(data=img_bytes, mime_type=_guess_mime(image_path)),
        ],
    )

    return (resp.text or "").strip()
