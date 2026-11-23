# REKOMENDASI PERUBAHAN — APLIKASI KASIR (versi Anda)

Disusun setelah pembongkaran kode + patch tahap awal (database file & penghapusan trial).
Prioritas: **P1 = sebaiknya segera**, **P2 = penting**, **P3 = peningkatan**.

---

## 1. Integritas & Keamanan Data

### P1 — Ganti checksum backup DJB2 dengan SHA-256
- **Sekarang**: `computeSimpleChecksum()` memakai hash DJB2 32-bit (8 digit hex), bukan kriptografi. Siapa pun bisa membuat file backup dengan checksum palsu.
- **Rekomendasi**: pakai `crypto.subtle.digest("SHA-256", ...)` (async). Simpan checksum 64 digit.
- **Catatan**: perhatikan kompatibilitas backup lama — terima dua format saat transisi.

### P1 — Wajib auto-snapshot sebelum restore
- **Sekarang**: `restoreBackup()` langsung `DELETE` 14 tabel. Kalau file backup rusak tapi lolos checksum (atau salah pilih file), data hilang.
- **Rekomendasi**: sebelum eksekusi, panggil `createBackup()` dan simpan sebagai snapshot darurat. Beri tombol "Urungkan" dengan satu klik.

### P1 — Perbaiki penyimpanan file database baru
- File `*.fdb` saat ini berisi **JSON** (bukan biner SQLite mentah). Ini tidak salah secara fungsi, tapi menyesatkan.
- Rekomendasi:
  - Ganti ekstensi ke `.json` atau `.fdb.json`, **atau**
  - Tulis biner SQLite asli (`sqlJsDb.export()`) langsung ke file, dan simpan riwayat backup di file terpisah.
- Tambahkan indikator izin yang jelas: browser bisa mencabut izin file setelah restart. Panel sudah punya status, tapi sebaiknya ada peringatan aktif saat izin perlu diminta ulang.

### P2 — Pisahkan/mperjelas laporan laba
- `grossProfitServices` dihitung dari **kas masuk** (`payments`), sementara `totalServiceReceivables` dari **tagihan** (`remaining_balance`). Keduanya dibandingkan dalam satu layar tanpa keterangan.
- Rekomendasi: beri label eksplisit, mis. "Laba Servis ( kas diterima )" vs "Piutang ( belum ditagih )", atau tambahkan baris "Laba Servis ( akrual )".

### P2 — `servicesByStatus` tidak mengikuti filter periode
- Query `GROUP BY status` tidak memakai `created_at >= start AND <= end`.
- Rekomendasi: tambahkan filter yang sama seperti komponen laporan lain, supaya angka harian/bulanan konsisten.

### P2 — Nomor nota rentan duplikat
- `generateNextOrderNumber()` / `generateNextInvoiceNumber()` memakai `SELECT MAX(...)` lalu `+1`, tanpa *sequence* atau lock.
- Rekomendasi: bungkus pembuatan nomor di dalam transaksi yang sama dengan INSERT, atau buat tabel `counters(harian, last_no)` dengan `UPDATE ... RETURNING`.

---

## 2. Fitur yang Belum Aktif / Perlu Diputuskan

### P2 — PIN aplikasi tidak diimplementasikan
- Field `app_pin_hash` / `app_owner_pin` ada di settings, tapi tidak ada fungsi hash/validasi di bundle.
- Kalau versi Anda butuh PIN: implementasikan dengan salt + PBKDF2 (`crypto.subtle`), bukan plaintext. Kalau tidak butuh, hapus field tersebut agar tidak menyesatkan.

### P3 — Lisensi sudah tidak relevan
- Setelah trial dihapus, kelas lisensi (`Gc`) tidak dipakai. Bisa dibiarkan (dead code) atau dihapus saat rekonstruksi source.

---

## 3. Identitas Brand (yang Anda rencanakan)

Saat Anda kirim detail brand, titik yang perlu diubah:

| Prioritas | File / bagian | Catatan |
|---|---|---|
| P1 | `app/index.html` | `<title>`, `theme-color`, `apple-mobile-web-app-title` |
| P1 | `app/manifest.json` | `name`, `short_name` |
| P1 | `app/logo.png`, `favicon.png`, `app.ico` | siapkan 192×192 & 512×512 (sekarang deklarasi 512 tidak sesuai file) |
| P1 | Bundle: nama toko default | `"Aplikasi Kasir"` di seeding settings |
| P2 | Bundle: footer & pesan error | `"AplikasiKasir (Full Version Terdaftar) — Dikembangkan oleh Aplikasi Kasir"`, `"Memuat AplikasiKasir..."`, `"Gagal Membuka Database"` |
| P2 | `Buka-Aplikasi.bat` | `title` jendela |
| P2 | `CARA_PENGGUNAAN_PC.txt` | seluruh teks brand lama |
| P3 | Prefiks nota | `FS-` / `TRX-` → inisial brand (opsional; bukan sekadar teks, karena dipakai query `LIKE`) |

⚠️ **Jangan search-replace "firdaus" secara global.** Itu juga dipakai sebagai nama DB, kunci IndexedDB/localStorage, dan field `app` pada backup. Rencanakan migrasi terpisah.

---

## 4. Arsitektur & Packaging

### ✅ SUDAH — Integrasi menu lokasi database
- Kartu **"Lokasi Database"** sudah ditambahkan ke halaman **Menu Lainnya** (patch `apply_menu_patch.py`).
- Panel melayang sudah dihapus; kartu membuka modal dari `app\storage-ui.js`.
- Rekomendasi lanjutan: bisa juga ditaruh di halaman **Profil & Pengaturan Toko** bila diinginkan.

### P2 — Launcher desktop
- Mengganti nama file `.exe` + referensi di `.bat` itu mudah.
- Teks system tray ada di dalam biner .NET yang sudah dikompilasi. Kalau ingin ikut berganti, perlu launcher pengganti (bisa dibuat kecil dengan .NET/C# atau WebView2).

### P3 — Service worker tidak ada
- Manifest PWA valid, tapi tanpa SW tidak ada caching offline di browser.
- Untuk desktop ini tidak masalah (file lokal + HttpListener). Kalau nanti mau deploy web, tambahkan SW sederhana.

### P3 — Bersihkan aset duplikat
- `sql-wasm.wasm` ≡ `sql-wasm-browser.wasm` (sengaja fallback).
- `favicon.png` ≡ `logo.png`.
- `aplikasi-kasir.apk` tidak dipakai untuk desktop — bisa dihapus dari project.

---

## 5. Maintainability

### P2 — Simpan rantai patch, jangan edit bundle sembarangan
- Sudah saya siapkan: `main-original.js` + `apply_storage_patch.py` + `apply_trial_patch.py` + `apply_all_patches.py`.
- **Aturan**: selalu patch dari `main-original.js` lewat `apply_all_patches.py`. Jangan mengedit `main-*.js` langsung tanpa mencatat, karena akan hilang saat patch diulang.

### P3 — Rekonstruksi source (opsional, jangka panjang)
- Kalau project ini akan dikembangkan lama, pertimbangkan membuat source TypeScript per-modul dari hasil dekompilasi, lalu build dengan Vite.
- Risiko: perilaku bisa berubah. Lakukan hanya setelah semua perilaku saat ini terdokumentasi & diuji.

---

## 6. Checklist Uji Manual Setiap Patch

1. Buka `PREVIEW\jalankan-preview.bat` → `http://localhost:5180` di Chrome/Edge.
2. Pastikan **tidak ada** banner kuning "Mode Trial" dan tidak ada hitungan menit.
3. Buat 1 servis + 1 transaksi kasir.
4. Cetak nota thermal & A4 → pastikan **tidak ada** watermark trial.
5. Refresh browser (Ctrl+F5) → data masih ada (artinya file database dipakai).
6. Klik panel "Database" → status harus `file`, bukan `browser`.
7. Tutup browser, buka lagi → jika izin file diminta, berikan; data tetap ada.

---

## Ringkasan 5 Prioritas Teratas

1. **SHA-256 untuk checksum backup** + auto-snapshot sebelum restore.
2. **Perbaiki format file database** (JSON vs `.fdb`) + indikator izin.
3. **Konsistensi laporan**: filter periode pada `servicesByStatus` & label laba kas/akrual.
4. **Nomor nota aman** terhadap duplikat.
5. **Identitas brand** menyeluruh (dengan migrasi kunci penyimpanan yang hati-hati).
