from PIL import Image, ImageOps
import os

BASE = r"D:\bongkar kode\PROJECT_BASE"
src = os.path.join(BASE, "app", "assets", "logo.jpg")

im = Image.open(src).convert("RGB")
print("Sumber:", im.size)

# Crop bagian ikon (mesin POS + gear) di sisi kiri, buang teks & whitespace
w, h = im.size
box = (int(w * 0.165), int(h * 0.20), int(w * 0.475), int(h * 0.80))
icon = im.crop(box)
# Tambah padding putih agar proporsi kotak rapi
icon = ImageOps.pad(icon, (1024, 1024), color=(255, 255, 255), method=Image.Resampling.LANCZOS)
print("Crop ikon:", icon.size)

for size in (192, 512, 64):
    out = icon.resize((size, size), Image.Resampling.LANCZOS)
    path = (
        os.path.join(BASE, "app", "logo.png") if size == 192 else
        os.path.join(BASE, "app", "logo-512.png") if size == 512 else
        os.path.join(BASE, "app", "favicon.png") if size == 64 else None
    )
    # favicon sebaiknya 64; logo.png 192; logo-512 512
    if size == 64:
        out.save(os.path.join(BASE, "app", "favicon.png"))
    else:
        out.save(path)
    print("Ditulis:", path or os.path.join(BASE, "app", "favicon.png"), size)

# ICO Windows
ico = icon.resize((64, 64), Image.Resampling.LANCZOS)
ico.save(os.path.join(BASE, "app.ico"), format="ICO", sizes=[(64, 64)])
print("Ditulis: app.ico")
