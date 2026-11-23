"""Patch bundle: ganti class dh (IdbStorage) dengan penyimpanan berbasis file.

Ambil dari main-branded.js (cadangan), tulis ke app/assets/main-DbOgN5j6.js.
Aman dijalankan berulang: selalu mulai dari cadangan.
"""
import os

BASE = r"D:\bongkar kode\PROJECT_BASE"
src_path = os.path.join(BASE, "DOKUMENTASI", "main-branded.js")
dst_path = os.path.join(BASE, "app", "assets", "main-DbOgN5j6.js")
cls_path = os.path.join(BASE, "DOKUMENTASI", "storage-class.js")

src = open(src_path, encoding="utf-8").read()
new_class = open(cls_path, encoding="utf-8").read().rstrip()

marker = "class dh{"
i = src.find(marker)
if i < 0:
    raise SystemExit("Marker class dh{ tidak ditemukan di bundle asli")

j = src.find("{", i)
depth = 0
k = j
quote = None
escaped = False
while k < len(src):
    c = src[k]
    if quote:
        if escaped:
            escaped = False
        elif c == "\\":
            escaped = True
        elif c == quote:
            quote = None
        k += 1
        continue
    if c in ('"', "'", "`"):
        quote = c
        k += 1
        continue
    if c == "{":
        depth += 1
    elif c == "}":
        depth -= 1
        if depth == 0:
            end = k + 1
            break
    k += 1
else:
    raise SystemExit("Class dh tidak memiliki tutup '}'")

old_class = src[i:end]
print("Class lama ditemukan, panjang:", len(old_class))

out = src[:i] + new_class + src[end:]
open(dst_path, "w", encoding="utf-8").write(out)
print("Patch diterapkan. Ukuran bundle baru:", len(out), "byte")
