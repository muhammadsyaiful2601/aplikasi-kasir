# LAPORAN PEMBONGKARAN KODE — FIRDAUS SERVIS

**Tanggal:** 23 November 2026
**Lokasi:** `D:\bongkar kode`
**Metode:** Membaca & merapikan (beautify) bundle JavaScript hasil build Vite, memeriksa metadata biner (read-only), tanpa menjalankan executable.

---

## 1. Ringkasan Eksekutif

**Firdaus Servis** adalah aplikasi **kasir (POS) + servis HP/komputer** yang berjalan **100% offline**, dibangun sebagai satu basis kode web lalu dibungkus untuk tiga platform:

| Platform | Wrapper | Teknologi kunci |
|---|---|---|
| Browser / Web | PWA (manifest saja, **tanpa service worker**) | React 18 + Vite + Tailwind + SQL.js (SQLite/WASM) |
| Desktop Windows | Launcher WinForms C# ~14 KB | `HttpListener` (server HTTP lokal) + browser + system tray |
| Android | Capacitor (AGP 8.2.1) | SQLCipher native, Bluetooth printer, WhatsApp, RawBT |

**Karakteristik arsitektur:**
- **Frontend**: React 18 (`createRoot`, StrictMode), Tailwind CSS, ikon lucide-react v0.469.0, **tanpa router library** (navigasi berbasis state), **tanpa Context API** (props drilling).
- **Database**: SQLite. Di web memakai **sql.js** dengan biner WASM, dipersistenkan ke **IndexedDB** (fallback localStorage base64). Di Android memakai plugin `@capacitor-community/sqlite` (SQLCipher).
- **Skema**: 17 tabel relasional dengan 1 migrasi resmi (versi 1) + patch `ALTER TABLE` non-versi. Semua uang `INTEGER` (Rupiah), ID `TEXT`, waktu ISO-8601.
- **Bisnis**: Stok selalu dicatat lewat `stock_movements`; status pembayaran dihitung ulang; retur stok otomatis; garansi dibuat otomatis saat servis diambil.
- **Fitur unggul**: Kasir dengan keranjang & kembalian, alur servis lengkap (terima→cek→jasa/sparepart→DP→ambil→garansi+klaim), laporan laba/rugi & arus kas + ekspor CSV, cetak struk thermal ESC/POS (Bluetooth/RawBT/BLE/USB/AirPrint) & faktur A4/PDF, kirim nota via WhatsApp, backup/restore + auto-backup harian (5 snapshot) + cloud merge.
- **Monetisasi**: Mode trial/demo 15 menit per sesi (non-persisten + watermark nota) dan sistem lisensi yang **selalu aktif** (tidak memblokir).

**Ukuran kode:** bundle utama 566.093 byte / 841 baris minified → **17.350 baris** setelah dirapikan.

---

## 2. Daftar File Hasil Analisis

| File | Isi |
|---|---|
| `main.pretty.js` | Seluruh bundle JS yang sudah dirapikan (17.350 baris) — sumber rujukan semua nomor baris |
| `beautify.py` | Skrip Python yang dipakai untuk merapikan bundle |
| `03_database.md` | Skema 17 tabel, SqliteAdapter, 9 repository, seeding & logika bisnis data |
| `04_bisnis_keamanan.md` | Laporan/analitik, backup-restore-cloud sync, lisensi & trial, PIN, utilitas, sistem cetak |
| `05_ui.md` | Struktur komponen React, daftar layar & modal, fitur per layar, state management, alur kerja, bootstrap |
| `06_packaging.md` | PWA/manifest, peran file WASM & web-*.js, launcher Windows, APK Capacitor, tech stack |
| `LAPORAN_UTAMA.md` | Ringkasan menyeluruh (file ini) |

---

## 3. Peta Struktur Proyek

```
D:\bongkar kode
├── FirdausServis.exe          launcher WinForms C# 14 KB (HttpListener + tray)
├── Buka-Aplikasi.bat          script peluncur (exe → fallback index.html)
├── CARA_PENGGUNAAN_PC.txt     panduan pengguna Windows
├── app.ico                    ikon Windows 64×64
└── app\
    ├── index.html             shell React (mount #root, meta PWA)
    ├── manifest.json          PWA: standalone, portrait, theme #2563eb
    ├── _redirects             Netlify SPA rewrite: /* → /index.html 200
    ├── logo.png / favicon.png ikon 192×192 (file identik)
    ├── sql-wasm.wasm          engine SQLite WASM 688 KB (fallback)
    ├── sql-wasm-browser.wasm  identik (primary)
    ├── firdausservis.apk      Android APK 7,46 MB (Capacitor, v1.0.5)
    └── assets\
        ├── main-*.js          bundle utama (566 KB) → main.pretty.js
        ├── main-*.css         Tailwind 86,5 KB
        ├── web-*.js           web-shim plugin Capacitor App (673 B) & SQLite (9,6 KB)
    └── _analysis\             hasil pembongkaran ini
```

---

## 4. Arsitektur Teknis (Ringkas)

```
┌────────────────────────────────────────────────────────────────┐
│ UI  React 18 + Tailwind + lucide-react   (state di App root)   │
│  Halaman: Beranda · Servis · Kasir · Stok · Lainnya            │
│  Modal: Nota/Cetak · Servis Baru · Detail Servis · Checkout ·  │
│         Produk · Opname · Backup · Pelanggan · Laporan · Garansi│
├────────────────────────────────────────────────────────────────┤
│ LAYANAN  backup/restore + auto-backup + cloud merge ·          │
│          analytics getSummary + CSV · lisensi · trial 15 mnt   │
│          ESC/POS builder · printer BT/RawBT/BLE/USB/WA         │
├────────────────────────────────────────────────────────────────┤
│ REPOSITORY  Settings · Customers · Products · ServiceOrders ·  │
│             Sales · Expenses/Reports · Warranty                │
├────────────────────────────────────────────────────────────────┤
│ DB ADAPTER  Native: @capacitor-community/sqlite (SQLCipher)    │
│             Web: sql.js + IndexedDB (fallback localStorage)    │
│             17 tabel · transaksi BEGIN/COMMIT/ROLLBACK         │
├────────────────────────────────────────────────────────────────┤
│ RUNTIME  Web: Netlify PWA  |  PC: HttpListener + browser       │
│          Android: Capacitor WebView + native plugins           │
└────────────────────────────────────────────────────────────────┘
```

---

## 5. Inventaris Fitur (Ringkas)

**Modul Servis**
- Terima servis dengan nomor otomatis `FS-YYYYMMDD-0001`, template tarif cepat HP & PC/Printer (dapat diatur).
- 8 status pengerjaan dengan riwayat; ubah teknisi & garansi; keluhan, kondisi, kelengkapan, IMEI/SN.
- Rincian jasa (LABOR) & sparepart dari stok (PART) dengan potong stok + audit movement.
- DP/pelunasan (Tunai/Transfer/QRIS), sisa tagihan, piutang.
- Saat status → **Sudah Diambil**: garansi otomatis ACTIVE; klaim garansi dengan keputusan.

**Modul Kasir**
- Keranjang, qty dibatasi stok, diskon, checkout Tunai/Transfer/QRIS Manual, uang diterima + kembalian.
- Faktur `TRX-YYYYMMDD-0001`, status langsung PAID; pembatalan → retur stok + catatan kas OUT.

**Modul Stok**
- Produk (SKU/barcode/kategori/modal/jual/min stock), opname, mutasi stok (`INITIAL/SALE/SERVICE_USAGE/RETURN`), peringatan stok menipis.

**Modul Keuangan**
- Dashboard & laporan periode: laba kotor kasir, laba servis, piutang, pengeluaran, arus kas, laba bersih, produk terlaris.
- Ekspor CSV Penjualan & Servis; catat pengeluaran & modal part.

**Modul Lain**
- Data pelanggan + ringkasan; pengaturan toko (HP vs KOMPUTER, kertas 58/80mm, header/footer nota, garansi default).
- Backup JSON (checksum DJB2) + auto-backup harian 5 snapshot + kirim WA/Drive + pulihkan file + cloud merge dengan resolusi konflik.
- Cetak: struk thermal ESC/POS (Bluetooth SPP/RawBT/BLE/USB/AirPrint), faktur A4/PDF, kirim WhatsApp, salin teks.

---

## 6. Temuan Kritis & Catatan

| # | Temuan | Dampak |
|---|---|---|
| 1 | **Lisensi selalu ACTIVE** (`Gc.checkStatus()` mengembalikan true; secret activation key plaintext di bundle) | Tidak ada proteksi pembajakan riil pada build web |
| 2 | **Trial hanya pembatasan UI + non-persisten**; bisa di-reset lewat tombol/tab/query baru | Mudah dilewati |
| 3 | **PIN aplikasi tidak diimplementasikan** (hanya field `app_pin_hash`/`app_owner_pin`); "PIN 0000/1234" adalah PIN pairing printer | Jangan mengandalkan fitur PIN |
| 4 | **Checksum backup non-kriptografis** (DJB2); restore menghapus 14 tabel | Risiko jika file backup dimodifikasi sengaja |
| 5 | **`servicesByStatus` tidak mengikuti filter periode** laporan | Angka status bisa menyesatkan |
| 6 | **Laba servis basis kas, piutang basis tagihan** | Perlu interpretasi hati-hati saat membaca laporan |
| 7 | **Nomor nota memakai query MAX**, bukan sequence; >9999 & konkurensi tidak ditangani | Risiko duplikat nomor |
| 8 | **Tidak ada service worker** | Offline di browser bergantung file lokal + wrapper, bukan PWA caching |
| 9 | **Deklarasi ikon 512×512 tidak sesuai file aktual (192×192)** | Ikon bisa blur di launcher |
| 10 | **Versi web `app/` vs APK berbeda hash chunk** | Pastikan sinkron saat rilis |
| 11 | Duplikat aset: `favicon.png` ≡ `logo.png`, kedua WASM identik | Boros tempat (WASM sengaja untuk fallback) |

---

## 7. Cara Membaca Kode yang Dirapikan

- Buka `D:\bongkar kode\_analysis\main.pretty.js` dengan editor teks (VS Code disarankan).
- Nomor baris di semua laporan detail merujuk ke file ini.
- Kode masih memakai nama variabel minified (`a`, `i`, `o`, `d`, `u`, `m`, `b`, `g`, `k`), tetapi **nama class repository bermakna** (`ug`, `mg`, `pg`, `hg`, `fg`, `xg`, `gg`, `bg`, `wg`, `Gc`) dan **semua string SQL/UI masih utuh**, sehingga alur bisnis mudah diikuti.
- Untuk mencari fitur, gunakan `grep` pada string Bahasa Indonesia (mis. `"Cetak"`, `"Stok tidak mencukupi"`, `"SUDAH_DIAMBIL"`).

---

## 8. Kesimpulan

Aplikasi ini adalah sistem kasir & servis yang **cukup lengkap dan matang secara fungsional**, dengan arsitektur **offline-first** yang pragmatis: React + SQLite/WASM di web, SQLCipher di Android, dan launcher ringan di Windows. Seluruh logika bisnis (stok, pembayaran, garansi, laporan, backup) terkonsentrasi di lapisan repository kelas `hg`/`fg`/`xg`/`bg`, sementara UI adalah satu komponen root besar dengan props drilling dan pola `refreshTrigger`.

Aspek yang **perlu diperhatikan** jika akan dikembangkan/diaudit: mekanisme lisensi & trial yang bersifat deklaratif, tidak adanya PIN aktif, checksum backup yang lemah, serta beberapa inkonsistensi pelaporan (status tanpa filter periode, basis kas vs tagihan), serta tidak adanya service worker.

Semua file hasil pembongkaran tersimpan di folder `D:\bongkar kode\_analysis\` dan tidak ada file aplikasi asli yang diubah.
