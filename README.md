# Aplikasi Kasir & Servis — Offline Desktop

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

- **Kasir/POS**: keranjang, diskon, tunai/transfer/QRIS, kembalian, faktur otomatis
- **Servis**: penerimaan, 8 status pengerjaan, jasa & sparepart, DP/pelunasan, garansi + klaim
- **Stok**: katalog produk, opname, riwayat mutasi, peringatan stok menipis
- **Keuangan**: laba kotor/bersih, arus kas, piutang, produk terlaris, ekspor CSV
- **Cetak**: struk thermal ESC/POS (Bluetooth/RawBT/BLE/USB/AirPrint), faktur A4/PDF, WhatsApp
- **Backup**: file JSON + auto-backup harian + pemulihan + sinkronisasi

## Menjalankan

### Cara cepat (production)
Double-click `FirdausServis.exe` atau `Buka-Aplikasi.bat`.

### Mode preview (development, tanpa build)
Double-click `PREVIEW\jalankan-preview.bat`, lalu buka `http://localhost:5180` di Chrome/Edge.
Setiap perubahan di folder `app\` cukup **Ctrl+F5**.

> Gunakan Chrome/Edge lewat `http://localhost` agar fitur pemilihan file database aktif.

## Lokasi database

Klik panel **"Lokasi Database"** di sisi kiri bawah aplikasi untuk memilih/memindah file database.
Data lama dari browser otomatis dipindahkan saat pertama kali memilih file.

## Dokumentasi

- `PANDUAN_PROJECT.md` — panduan lengkap project & patch
- `DOKUMENTASI/LAPORAN_UTAMA.md` — arsitektur & hasil pembongkaran kode
- `DOKUMENTASI/REKOMENDASI.md` — rekomendasi pengembangan lanjutan
- `DOKUMENTASI/apply_all_patches.py` — menerapkan ulang semua patch dari bundle asli

## Catatan

Mode trial/lisensi sudah dihilangkan dari bundle; aplikasi berjalan sebagai versi penuh tanpa watermark atau batas waktu.
