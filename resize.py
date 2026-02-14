from PIL import Image

src = "testimage1.jpg"
dst = "testimage1_small.jpg"

img = Image.open(src).convert("RGB")
img.thumbnail((640, 640))          # limite 640x640 (bem leve)
img.save(dst, quality=85, optimize=True)

print("ok ->", dst, img.size)
