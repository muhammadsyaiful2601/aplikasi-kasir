# Packaging, Build, PWA & Aset — Firdaus Servis

Pemeriksaan read-only. Tidak ada executable yang dijalankan.

## Ringkasan tech stack

| Lapisan | Teknologi |
|---|---|
| UI | React + Tailwind CSS (kelas `bg-slate-50` di index.html) |
| Bundler | Vite (chunk `main-<hash>.js`, env `VITE_TRIAL_MODE`) |
| Database | SQL.js / SQLite WASM di web; SQLCipher native di Android |
| Wrapper Desktop | .NET Framework WinForms (C#) kustom — bukan Electron |
| Wrapper Mobile | Capacitor (`@capacitor/core` + plugin SQLite, App, StatusBar) |
| Hosting | Netlify (SPA `_redirects`, deteksi `netlify.app`) |

## 1. PWA (`app/manifest.json`)

- short_name `FirdausServis`; name `FirdausServis — Kasir & Servis HP Offline`
- ikon: dua entri keduanya `/logo.png` dideklarasikan 192×192 & 512×512; file aktual hanya 192×192 (47.100 B) → deklarasi 512 tidak akurat.
- `start_url: "/"`, `display: "standalone"`, `orientation: "portrait"`, `theme_color: #2563eb`, `background_color: #ffffff`.
- Tanpa `shortcuts`, `scope`, `id`, `screenshots`. Shortcut desktop berasal dari fitur Install browser, bukan manifest.
- `_redirects`: `/*  /index.html  200` (rewrite Netlify untuk SPA routing).
- **Tidak ada service worker** di bundle maupun folder → offline bukan via SW, melainkan file lokal + server HTTP wrapper desktop / `capacitor://localhost`.

## 2. Peran file

| File | Ukuran | Peran |
|---|---|---|
| `sql-wasm.wasm`, `sql-wasm-browser.wasm` | 688.197 B各自 | Engine SQL.js; identik (SHA256 sama), dipakai primary + fallback. Magic byte `\0asm` divalidasi saat fetch. |
| `web-CVjPqDCm.js` | 673 B | Implementasi web plugin `@capacitor/app` (visibilitychange → appStateChange/pause/resume). |
| `web-DMqn_XAc.js` | 9.624 B | Implementasi web `@capacitor-community/sqlite` (jeep-sqlite + SQL.js). |
| `favicon.png`, `logo.png` | 47.100 B | Identik (SHA256 sama); favicon + ikon PWA + apple-touch-icon. |
| `app.ico` | 2.686 B | ICO Windows 64×64 (PNG di dalam ICO). |

Bundle memuat urutan fallback WASM: `sql-wasm-browser.wasm` lalu `sql-wasm.wasm`; error: *"Timeout memuat engine SQL.js (sql-wasm.wasm tidak ditemukan… Pastikan file ada di folder public/)"*.

## 3. Peluncuran PC

`Buka-Aplikasi.bat`: `cd /d "%~dp0"` → jika `FirdausServis.exe` ada, jalankan; else fallback `start "" "app\index.html"` (berisiko gagal via `file://` untuk ES module + fetch WASM).

`CARA_PENGGUNAAN_PC.txt`: portable offline Win7/8/10/11, jendela mandiri tanpa address bar, system tray (Buka Aplikasi / Buka di Browser Biasa / Keluar), cetak struk 58/80 mm & faktur A4/PDF, opsi Install PWA.

## 4. FirdausServis.exe

- 14.336 byte, SHA256 `E5CBA40A…CAA371BD9`, PE32/i386, impor `mscoree.dll` → assembly .NET Framework.
- String: `FirdausServisApp`, `FirdausServis-Offline`, `HttpListener`, `serverThread`, `FindBrowser`, `NotifyIcon`, `ContextMenu`, `MenuItem`, `ProcessStartInfo`.
- Kesimpulan: launcher WinForms C# kecil yang menyalakan **HTTP server lokal** (`HttpListener`) untuk menyajikan folder `app/` (agar ES module/fetch/WASM punya origin `http://`), membuka browser via `Process.Start`, dan memasang ikon tray dengan menu sesuai panduan. Membutuhkan .NET Framework 4.x.

## 5. firdausservis.apk

- 7.824.109 byte (~7,46 MiB), 514 entri ZIP, signed v1, package `com.firdausweb.firdausservis`, versionName **1.0.5**, AGP 8.2.1 + Kotlin + baseline profile.
- Capacitor: `assets/capacitor.config.json` (appId `com.firdausweb.firdausservis`, appName `FirdausServis Custom`, `webDir: dist-custom`, `server.androidScheme: https`, CapacitorSQLite `androidIsEncryption: false`, StatusBar LIGHT `#ffffff`). Plugin: `@capacitor-community/sqlite`, `@capacitor/app`, `@capacitor/status-bar`.
- `libsqlcipher.so` arm64-v8a (3,6 MB) & armeabi-v7a (2,2 MB); 3 dex (8,6 MB + ...); MainActivity `com.firdausweb.firdausservis.MainActivity`.
- Izin: INTERNET, BLUETOOTH*, READ/WRITE_EXTERNAL_STORAGE, DUMP. `<queries>`: WhatsApp (wa.me, api.whatsapp.com) & `ru.a402d.rawbtprinter` (cetak struk thermal RawBT).
- Web di APK: `assets/public/` build Vite chunk hash berbeda (`main-BcWH6pxi.js`, `main-BjdQoAJN.css`) dari folder `app/`, tapi struktur sama + kedua WASM (658.410 B — versi library berbeda).

## 6. Catatan tindak lanjut

1. Duplikasi aset: WASM & favicon/logo identik (WASM sengaja fallback).
2. Deklarasi ikon 512×512 tidak sesuai file aktual (192×192).
3. Tanpa service worker → klaim offline bergantung file lokal + wrapper, bukan PWA caching.
4. Versi web `app/` vs APK berbeda hash chunk → pastikan sinkron saat rilis.
