# PREVIEW / DEVELOPMENT SERVER

Server ini hanya untuk **testing**. Tidak ada proses build sama sekali.

## Menjalankan
Double-click `jalankan-preview.bat`. Browser Chrome/Edge akan terbuka di:
```
http://localhost:5180
```

## Alur kerja
1. Edit file apa pun di folder `app\` (mis. `storage-ui.js`, `index.html`, atau `assets\main-*.js`).
2. Kembali ke browser, tekan **Ctrl+F5** (hard refresh).
3. Perubahan langsung terlihat. **Tidak perlu build / kompilasi.**

Server menggunakan header `no-cache`, jadi browser selalu mengambil file terbaru.

## Kenapa harus http://localhost?
Fitur *File System Access API* (`showSaveFilePicker`) hanya aktif di **secure context**.
`http://localhost` dianggap aman oleh Chrome/Edge. Kalau aplikasi dibuka lewat
`file://`, fitur pilih lokasi database tidak akan muncul dan aplikasi falling back
ke IndexedDB browser.

## Panel "Lokasi Database"
Di sisi kiri bawah ada panel kecil:
- Klik untuk membuka menu.
- **Pilih / Ganti Lokasi…** → dialog file; data lama dari browser otomatis dipindahkan ke file baru.
- **Kembali ke Browser** → memakai IndexedDB lagi (data di file tidak dihapus).
- **Perbarui Status** → melihat mode & jumlah entri.

Setelah memilih file, **muat ulang halaman** supaya adapter memakai file tersebut
sejak awal inisialisasi.

## File yang tersedia
| File | Fungsi |
|---|---|
| `server.js` | server statis Node (tanpa dependency) |
| `jalankan-preview.bat` | menjalankan server + membuka browser |
| `README.md` | berkas ini |

## Catatan
- Node.js harus terpasang (sudah tersedia di komputer ini: v26).
- Perubahan pada `assets\main-*.js` adalah patch langsung pada bundle.
  Cadangan asli ada di `DOKUMENTASI\main-original.js`, dan patch bisa diulang
  lewat `DOKUMENTASI\apply_storage_patch.py`.
