import os
from dotenv import load_dotenv
from google import genai


def _guess_mime(path: str) -> str:
    # tenta adivinhar o tipo da imagem pelo final do nome
    # nao é perfeito, mas resolve p/ jpg/png/webp
    p = path.lower()
    if p.endswith(".png"):
        return "image/png"
    if p.endswith(".webp"):
        return "image/webp"
    return "image/jpeg"


def describe_image(image_path: str) -> str:
    # func principal que chama o gemini
    # recebe o caminho da img
    # devolve: "descricao | categoria"

    # carrega variaveis do .env
    load_dotenv()

    api_key = os.getenv("gemini_api_key")
    model = os.getenv("gemini_model", "gemini-2.0-flash")

    # se nao tiver chave, para aqui
    if not api_key:
        raise RuntimeError("faltou gemini_api_key no .env")

    # cria cliente gemini
    client = genai.Client(api_key=api_key)

    # le a imagem como bytes
    with open(image_path, "rb") as f:
        img_bytes = f.read()

    # prompt simples e direto
    # a gente força o formato de resposta
    prompt = (
        "descreva a imagem em 1-2 frases e sugira uma categoria curta. "
        "responda exatamente no formato: descricao | categoria"
    )

    # faz a chamada pro modelo
    # manda texto + imagem inline
    response = client.models.generate_content(
        model=model,
        contents=[
            {
                "role": "user",
                "parts": [
                    # parte 1 = texto
                    {"text": prompt},
                    # parte 2 = imagem em bytes
                    {
                        "inline_data": {
                            "mime_type": _guess_mime(image_path),
                            "data": img_bytes,
                        }
                    },
                ],
            }
        ],
    )

    # devolve só o texto 
    return response.text.strip()
