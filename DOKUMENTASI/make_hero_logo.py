from PIL import Image
import os

BASE = r"D:\bongkar kode\PROJECT_BASE"
src = os.path.join(BASE, "app", "assets", "logo.jpg")
im = Image.open(src).convert("RGBA")
px = im.load()
w, h = im.size
# Buang background putih (termasuk anti-aliasing) -> transparan
for y in range(h):
    for x in range(w):
        r, g, b, a = px[x, y]
        if r > 242 and g > 242 and b > 242:
            px[x, y] = (r, g, b, 0)
        elif r > 225 and g > 225 and b > 225:
            px[x, y] = (r, g, b, int(a * 0.25))
# Crop ke area logo (ikon + teks), buang margin putih berlebih
bbox = im.getbbox()
if bbox:
    im = im.crop(bbox)
out = os.path.join(BASE, "app", "assets", "logo-hero.png")
im.save(out)
print("Ditulis:", out, im.size, "bbox", bbox)
