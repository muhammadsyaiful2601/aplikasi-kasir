"""Rebrand bundle: FirdausServis -> AplikasiKasir.

Membaca main-original.js (cadangan asli), menulis main-branded.js.
Patch lain (storage/trial/menu) berjalan di atas main-branded.js.
"""
import os

BASE = r"D:\bongkar kode\PROJECT_BASE"
SRC = os.path.join(BASE, "DOKUMENTASI", "main-original.js")
DST = os.path.join(BASE, "DOKUMENTASI", "main-branded.js")

src = open(SRC, encoding="utf-8").read()

REPLACEMENTS = [
    ("Firdaus Servis", "Aplikasi Kasir"),
    ("FIRDAUS SERVIS", "APLIKASI KASIR"),
    ("FirdausServis", "AplikasiKasir"),
    ("Firdaus Web", "Aplikasi Kasir"),
    ("FIRDAUS_WEB", "APLIKASI_KASIR"),
    ("firdausservis", "aplikasikasir"),
    ("firdaus_", "aplikasikasir_"),
    ("Firdaus", "Aplikasi"),
    ("FIRDAUS", "APLIKASI"),
    ("firdaus", "aplikasikasir"),
    ("FS-", "AK-"),
]
for old, new in REPLACEMENTS:
    n = src.count(old)
    if n:
        src = src.replace(old, new)
        print(f"  {old!r:22} -> {new!r:22} ({n}x)")

compat = [
    ('if(s.app!=="AplikasiKasir")throw new Error("File backup tidak cocok: Bukan file backup AplikasiKasir.")',
     'if(s.app!=="AplikasiKasir"&&s.app!=="FirdausServis")throw new Error("File backup tidak cocok: Bukan file backup AplikasiKasir.")'),
    ('if(!s||s.app!=="AplikasiKasir"||!s.tables||typeof s.tables!="object")throw new Error("Data Cloud tidak cocok dengan struktur AplikasiKasir.")',
     'if(!s||(s.app!=="AplikasiKasir"&&s.app!=="FirdausServis")||!s.tables||typeof s.tables!="object")throw new Error("Data Cloud tidak cocok dengan struktur AplikasiKasir.")'),
]
for old, new in compat:
    if old in src:
        src = src.replace(old, new)
        print("  kompatibilitas backup lama ditambahkan")

open(DST, "w", encoding="utf-8").write(src)
print("Ditulis:", DST, "(", len(src), "byte )")
