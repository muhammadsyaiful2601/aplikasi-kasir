# PANDUAN PROJECT — BASE CODE (BELUM DIUBAH)

Folder ini adalah **salinan persis** dari aplikasi asli `D:\bongkar kode`.
**Belum ada satu pun baris kode yang diubah.** Gunakan ini sebagai titik awal untuk versi Anda.

---

## 1. Cara menjalankan di Desktop (sekarang, kondisi base)

1. Buka folder `PROJECT_BASE` di Windows Explorer.
2. **Double-click `FirdausServis.exe`** — atau --
   **Double-click `Buka-Aplikasi.bat`** (jika EXE tidak ada, script membuka `app\index.html` sebagai fallback).
3. Aplikasi muncul sebagai **jendela mandiri tanpa address bar**, dengan ikon di system tray.
   - Klik kanan ikon tray: *Buka Aplikasi* / *Buka di Browser Biasa* / *Keluar Aplikasi*.

> Catatan: `FirdausServis.exe` adalah launcher .NET kecil (~14 KB) yang menyalakan HTTP server lokal lalu membuka browser. Jadi yang berjalan sebenarnya tetap **aplikasi web di `app\`**, bukan native binary.

---

## 2. Struktur folder

```
PROJECT_BASE
├── PANDUAN_PROJECT.md          ← berkas ini (baca dulu)
├── FirdausServis.exe           launcher desktop (.NET WinForms)
├── Buka-Aplikasi.bat           script peluncur + fallback
├── CARA_PENGGUNAAN_PC.txt      panduan pengguna lama (brand lama)
├── app.ico                     ikon Windows 64×64
├── app\
│   ├── index.html              shell aplikasi: <title>, theme-color, #root
│   ├── manifest.json           PWA: nama, ikon, standalone, portrait
│   ├── _redirects              aturan Netlify (tidak dipakai di desktop)
│   ├── logo.png / favicon.png  ikon 192×192 (file identik)
│   ├── sql-wasm.wasm           mesin SQLite/WASM (cadangan)
│   ├── sql-wasm-browser.wasm   mesin SQLite/WASM (utama, identik)
│   ├── firdausservis.apk       versi Android — TIDAK dipakai untuk desktop
│   └── assets\
│       ├── main-*.js           SELURUH logika aplikasi (minified, 553 KB)
│       ├── main-*.css          gaya Tailwind (86,5 KB)
│       └── web-*.js            shim plugin Capacitor untuk web
└── DOKUMENTASI\
    ├── LAPORAN_UTAMA.md        ringkasan arsitektur + temuan
    ├── 03_database.md          skema 17 tabel + repository
    ├── 04_bisnis_keamanan.md   laporan, backup, lisensi, trial, cetak
    ├── 05_ui.md                halaman, modal, alur kerja
    ├── 06_packaging.md         PWA, launcher, APK
    ├── main.pretty.js          bundle JS yang sudah dirapikan (17.350 baris)
    └── beautify.py             skrip perapian (jika perlu ulang)
```

---

## 3. Peta perubahan untuk nanti (BELUM saya kerjakan)

Saat Anda sudah siap dengan daftar perubahan, ini titik-titik yang perlu disentuh:

### A. Identitas visual & shell
| File | Yang diubah |
|---|---|
| `app\index.html` | judul tab, `theme-color`, `apple-mobile-web-app-title` |
| `app\manifest.json` | `name`, `short_name` |
| `app\logo.png`, `app\favicon.png`, `app.ico` | gambar ikon |
| `app\assets\main-*.css` | warna tema Tailwind bila perlu |
| `Buka-Aplikasi.bat` | `title` jendela command prompt |
| `CARA_PENGGUNAAN_PC.txt` | seluruh teks brand lama |

### B. Teks yang "hardcode" di dalam bundle
Semua ada di `DOKUMENTASI\main.pretty.js` (nomor baris sesuai laporan):

| Yang dicari | Baris perkiraan | Catatan |
|---|---|---|
| Nama toko default & demo | ~8386 | `"Firdaus Servis"`, `"DEMO FIRDAUS SERVIS"` |
| Judul splash & error DB | ~17235 | `"Memuat FirdausServis..."`, `"Gagal Membuka Database"` |
| Footer pengembang | ~17088 | `"FirdausServis (Full Version Terdaftar) — Dikembangkan oleh Firdaus Web"` |
| Link & pesan WhatsApp penjualan | ~8372 | `wa.me/6287810851738`, teks "Firdaus Web…lisensi" |
| Secret lisensi | ~8588 | `FIRDAUS_WEB_OFFLINE_LICENSE_PUB_2026` |
| Teks trial & watermark nota | ~11562, ~10461, ~10820 | countdown, "Beli Resmi", watermark TIDAK SAH |
| Prefiks nomor nota | ~8433, ~8493 | `FS-` (servis) dan `TRX-` (kasir) — opsional |

### C. ⚠️ Jangan di-search-replace mentah-mentah
Nama "Firdaus/firdausservis" juga dipakai sebagai:
- nama database & kunci IndexedDB (`firdausservis_offline_idb`, `firdausservis_db`)
- kunci localStorage (`firdaus_trial_session_start`, `firdaus_custom_service_templates_*`)
- field `app` pada file backup (`"FirdausServis"`)

Mengganti semuanya sekaligus bisa membuat **data lama tidak terbaca** atau **backup lama gagal dipulihkan**. Setiap perubahan harus dipertimbangkan satu per satu.

---

## 4. Keputusan yang sudah Anda sampaikan (dicatat, belum dikerjakan)

1. **Platform: Desktop saja.** File APK di `app\` boleh diabaikan / dihapus nanti.
2. **Hilangkan mode trial 15 menit dan sistem lisensi** — tidak ada countdown, watermark, tombol "Beli Resmi", dan tanpa validasi lisensi.
3. **Database tersimpan sebagai file SQLite di dalam aplikasi**, bukan di localStorage/IndexedDB browser.
4. **Nanti ditambahkan menu untuk memindahkan lokasi database.**
5. **Identitas brand** (nama, warna, logo, WA, toko default) — Anda akan kirim kemudian.

> Poin 3 & 4 adalah perubahan **arsitektur**, bukan sekadar ganti teks. Lokasi penyimpanan saat ini ada di IndexedDB browser (karena aplikasinya berjalan di browser lewat launcher HTTP). Untuk memindahkannya ke file di folder aplikasi + menu pindah lokasi, nanti perlu penyesuaian pada **launcher desktop dan lapisan adapter database**. Ini akan saya rencanakan terpisah sebelum ada kode.

---

## 5. Alur kerja kita setelah ini

1. Anda **menuliskan perubahan** yang Anda inginkan (boleh bertahap).
2. Saya **menjelaskan dampaknya** dan menyusun daftar file/baris yang akan disentuh — **belum menulis kode** sampai Anda konfirmasi.
3. Setelah Anda bilang "oke, kerjakan", baru saya ubah file di folder `PROJECT_BASE` (file asli di `D:\bongkar kode` tetap saya biarkan apa adanya).
4. Setiap perubahan bisa diuji langsung dengan double-click `FirdausServis.exe`.

---

## 6. Hal yang sudah tersedia untuk membantu Anda

- `DOKUMENTASI\main.pretty.js` — kode yang sudah dirapikan; semua nomor baris di panduan ini merujuk ke file itu.
- `DOKUMENTASI\LAPORAN_UTAMA.md` + 4 laporan detail — penjelasan lengkap tiap modul.
- Saya bisa mencarikan lokasi teks tertentu, menjelaskan fungsi suatu baris, atau menyiapkan daftar perubahan tanpa mengubah file.

**File asli di luar `PROJECT_BASE` tidak saya sentuh sama sekali.**

---

## 7. TAHAP AWAL YANG SUDAH DIKERJAKAN

### 7.1 Penyimpanan database berbasis file ✅
- `class dh` (adapter penyimpanan) di dalam `app\assets\main-DbOgN5j6.js` sudah saya ganti.
- Data SQLite (dan riwayat auto-backup) kini ditulis ke **file pilihan Anda** memakai *File System Access API*.
- **Fallback**: kalau browser tidak mendukung / izin ditolak, aplikasi otomatis memakai IndexedDB seperti semula (tidak ada data hilang).
- Saat pertama kali memilih file, data lama dari IndexedDB **otomatis dipindahkan** ke file baru.
- Logika bisnis (SQL, repositori, React) **tidak diubah** — hanya lapisan penyimpanannya.

### 7.2 Menu "Lokasi Database" ✅ (sudah terintegrasi)
- Kartu baru **"Lokasi Database"** ada di halaman **Menu Lainnya**, di bawah "Backup & Pemulihan Data".
- Kartu membuka **modal** (panel melayang sudah dihapus). Isi modal:
  - Status penyimpanan: mode, nama file, jumlah entri
  - **Pilih / Ganti Lokasi…** → memilih file database
  - **Kembali ke Browser** → pakai IndexedDB lagi
  - **Tutup** (tombol ×, Esc, atau klik di luar modal)
- File terkait: `app\storage-ui.js` (modal) + patch `DOKUMENTASI\apply_menu_patch.py`.
- Setelah memilih file, **muat ulang aplikasi** agar adapter memakai file sejak awal.

### 7.3 Preview server (tanpa build) ✅
- Folder baru: `PREVIEW\` berisi `server.js`, `jalankan-preview.bat`, `README.md`.
- Jalankan: **double-click `PREVIEW\jalankan-preview.bat`** → buka `http://localhost:5180` di **Chrome/Edge**.
- Setiap ada perubahan di folder `app\`, cukup **Ctrl+F5** — tidak perlu build/kompilasi.
- Port 5180 dipilih karena 5173 sudah dipakai server lain di komputer ini.

### 7.4 File pendukung di `DOKUMENTASI\`
| File | Fungsi |
|---|---|
| `main-original.js` | cadangan bundle sebelum dipatch (untuk revert) |
| `storage-class.js` | source kelas `dh` yang baru (dibaca oleh patch script) |
| `apply_storage_patch.py` | menerapkan patch dari cadangan → bundle |
| `test_storage.js` | uji otomatis serialisasi & baca/tulis file (lulus) |
| `extract_class.py`, `context.py` | alat bantu inspecting bundle |

### 7.5 Cara membatalkan patch (jika diperlukan)
```bat
copy /Y "DOKUMENTASI\main-original.js" "app\assets\main-DbOgN5j6.js"
```
Lalu hapus baris `<script src="/storage-ui.js"></script>` dari `app\index.html`.

### 7.6 Mode trial & lisensi SUDAH DIHILANGKAN ✅
- `es()` kini selalu `false` → tidak ada deteksi trial, countdown, atau mode demo.
- Banner, modal "Waktu Demo 15 Menit Berakhir", dan tombol "Beli Resmi" **dihapus** (komponen `pb` → `null`).
- Watermark nota thermal & faktur A4 **dihapus**.
- Tautan WA penjualan & sisa konstanta sesi trial (`Mu`, `ag`, `ig`) **dihapus**.
- Efek samping yang **menguntungkan**: persistensi database kini selalu aktif (dulu di-skip saat trial), jadi file database Anda benar-benar dipakai.
- Data demo (Budi/Siti, 2 servis, 1 penjualan) **tidak lagi di-seed** karena hanya muncul saat trial. Data starter (5 produk) tetap ada.
- Cara ulang patch: `python DOKUMENTASI\apply_all_patches.py` (storage + trial sekaligus, dari bundle asli).

### 7.7 Yang BELUM dikerjakan
- Mengganti identitas brand (nama, warna, logo, nomor WA, toko default).
- Membangun ulang `.exe` launcher bila diperlukan.

---

## 8. REKOMENDASI PERUBAHAN

Lihat bagian 8 pada laporan terpisah yang saya berikan bersama ini (atau pada
`DOKUMENTASI\REKOMENDASI.md`). Ringkasannya: prioritas keamanan data, konsistensi
pelaporan, lalu identitas brand.
