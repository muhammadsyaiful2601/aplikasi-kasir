"""Jalankan semua patch dari bundle asli menghasilkan bundle final.

Urutan:
  1. apply_storage_patch  (penyimpanan database berbasis file)
  2. apply_trial_patch    (hilangkan trial & lisensi)

Cara: python apply_all_patches.py
"""
import os
import sys

BASE = r"D:\bongkar kode\PROJECT_BASE"
sys.path.insert(0, os.path.join(BASE, "DOKUMENTASI"))

import apply_storage_patch  # noqa: F401  (modul ini langsung menulis saat di-import)
import apply_trial_patch

bundle = os.path.join(BASE, "app", "assets", "main-DbOgN5j6.js")
src = open(bundle, encoding="utf-8").read()
out, changes = apply_trial_patch.patch(src)
open(bundle, "w", encoding="utf-8").write(out)

print("=== Patch trial ===")
for c in changes:
    print(" -", c)
print("Ukuran final:", len(out), "byte")
