"""Jalankan semua patch dari bundle asli menghasilkan bundle final.

Urutan:
  1. apply_brand_patch   (Firdaus -> Aplikasi Kasir)
  2. apply_storage_patch (database berbasis file)
  3. apply_trial_patch   (hilangkan trial & lisensi)
  4. apply_menu_patch    (kartu Lokasi Database)

Cara: python apply_all_patches.py
"""
import os
import sys

BASE = r"D:\bongkar kode\PROJECT_BASE"
sys.path.insert(0, os.path.join(BASE, "DOKUMENTASI"))

import apply_brand_patch  # noqa: F401  (menulis main-branded.js)
import apply_storage_patch  # noqa: F401  (menulis bundle dari main-branded.js)
import apply_trial_patch
import apply_menu_patch
import apply_icon_patch

bundle = os.path.join(BASE, "app", "assets", "main-DbOgN5j6.js")
src = open(bundle, encoding="utf-8").read()
out, changes = apply_trial_patch.patch(src)
open(bundle, "w", encoding="utf-8").write(out)

print("=== Patch trial ===")
for c in changes:
    print(" -", c)

out = apply_menu_patch.patch(out)
print(" - menu 'Lokasi Database' ditambahkan")

out = apply_icon_patch.patch(out)
print(" - ikon template diganti ke SVG modern")
open(bundle, "w", encoding="utf-8").write(out)
print("Ukuran final:", len(out), "byte")
