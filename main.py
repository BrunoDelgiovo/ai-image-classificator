import os
import sys
import hashlib
from db import insert_image, find_by_sha256
from ai import describe_image


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main():

    #   pode rodar com python main.py testimage0.jpg
    # ou sem arg e ele pergunta
    image_path = sys.argv[1] if len(sys.argv) > 1 else input("caminho da imagem: ").strip().strip('"')

    if not os.path.exists(image_path):
        print("arquivo nao encontrado:", image_path)
        return

    digest = sha256_file(image_path)

    # se ja tiver, nao faz nada (dedup)
    existing = find_by_sha256(digest)
    if existing:
        print("ja existe no banco:", existing)
        return

    print("analisando imagem com ia...")
    text = describe_image(image_path)

    # espera descricao | categoria
    if "|" in text:
        description, category = [x.strip() for x in text.split("|", 1)]
    else:
        description, category = text.strip(), "outros"

    new_id = insert_image(
        filename=os.path.basename(image_path),
        sha256=digest,
        description=description,
        category=category,
    )

    print("salvo! id =", new_id)
    print("descricao:", description)
    print("categoria:", category)


if __name__ == "__main__":
    main()
