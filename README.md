# Aplikasi Kasir — Offline Desktop

Aplikasi kasir (POS) dan servis HP/komputer yang berjalan **100% offline** di desktop Windows.

## Teknologi

| Lapisan | Teknologi |
|---|---|
| UI | React 18 + Tailwind CSS + lucide-react |
| Build | Vite (bundle statis, tidak perlu build ulang untuk development) |
| Database | SQLite via SQL.js (WASM), disimpan ke **file pilihan pengguna** |
| Desktop | Launcher .NET WinForms + HTTP server lokal |
| Node preview | Server statis sederhana tanpa dependency |

## Fitur utama

- **Kasir/POS**: keranjang, diskon, tunai/transfer/QRIS, kembalian, faktur otomatis (`AK-...`)
- **Servis**: penerimaan, 8 status pengerjaan, jasa & sparepart, DP/pelunasan, garansi + klaim
- **Stok**: katalog produk, opname, riwayat mutasi, peringatan stok menipis
- **Keuangan**: laba kotor/bersih, arus kas, piutang, produk terlaris, ekspor CSV
- **Cetak**: struk thermal ESC/POS, faktur A4/PDF, WhatsApp
- **Backup**: file JSON + auto-backup harian + pemulihan + sinkronisasi

## Menjalankan

### Production
Double-click `AplikasiKasir.exe` atau `Buka-Aplikasi.bat`.

### Preview (development, tanpa build)
Double-click `PREVIEW\jalankan-preview.bat`, lalu buka `http://localhost:5180` di Chrome/Edge.
Setiap perubahan di folder `app\` cukup **Ctrl+F5**.

> Gunakan Chrome/Edge lewat `http://localhost` agar fitur pemilihan file database aktif.

## Lokasi database

Buka menu **Lainnya → Lokasi Database** untuk memilih atau memindah file database.
Data lama otomatis dipindahkan saat pertama kali memilih file.

## Rebranding

Seluruh identitas lama sudah diganti menjadi **Aplikasi Kasir**: judul, manifest PWA,
nama toko default, footer, splash, prefiks nota (`FS-` → `AK-`), nama file, dan kunci
penyimpanan. Backup lama (`app:"FirdausServis"`) tetap diterima.

Ulang patch: `python DOKUMENTASI\apply_all_patches.py`

## Dokumentasi

- `PANDUAN_PROJECT.md` — panduan project & patch
- `DOKUMENTASI/LAPORAN_UTAMA.md` + laporan 03–06 — hasil pembongkaran kode asli
- `DOKUMENTASI/REKOMENDASI.md` — rekomendasi lanjutan
