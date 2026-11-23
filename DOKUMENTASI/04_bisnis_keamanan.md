# Layanan Bisnis, Utilitas & Keamanan — Firdaus Servis

Sumber: `main.pretty.js`. File tidak diubah.

## 1. Reports / Analytics — class `xg` (baris 8533–8579)

`getSummary({start,end,label})` — filter `created_at >= start AND <= end` (kecuali servicesByStatus):

| Komponen | Rumus / sumber |
|---|---|
| totalSalesRevenue | SUM(grand_total) sales **PAID** |
| totalSalesCost | SUM(total_cost_snapshot) sales PAID |
| grossProfitSales | `revenue - cost` |
| totalServicePayments | SUM(amount) payments reference_type=SERVICE (kas masuk) |
| totalServicePartsCost | per order dibayar: SUM(cost_price_snapshot×qty) item PART, else fallback `so.total_parts_cost` |
| grossProfitServices | `payments - partsCost` (basis **kas**, bukan tagihan) |
| totalServiceBilled | SUM(grand_total) servis status bukan DIBATALKAN/TIDAK_DAPAT_DIPERBAIKI |
| totalServiceReceivables | SUM(remaining_balance) order aktif (piutang) |
| totalExpenses | SUM(amount) expenses |
| totalCashIn | `salesRevenue + servicePayments` |
| totalGoodsCost | `salesCost + servicePartsCost` |
| totalGrossProfit | `grossProfitSales + grossProfitServices` |
| netCashFlow | `cashIn - goodsCost - expenses` |
| totalNetProfit | `grossProfit - expenses` |
| servicesByStatus | GROUP BY status — ⚠️ tanpa filter tanggal |
| topSellingProducts | TOP 5 sale_items (qty desc) dari sales PAID |

- `exportSalesCsv(start,end)` → header `No Faktur,Tanggal,Pelanggan,Subtotal,Diskon,Grand Total,Status`; file `laporan_penjualan_kasir_${t}.csv`.
- `exportServicesCsv(start,end)` → filter `(so.created_at between) OR (p.created_at between)`; header `No Nota,Tanggal,Pelanggan,Telepon,Merek HP,Model HP,Keluhan,Status,Total Tagihan,Sudah Dibayar,Sisa Tagihan,Status Bayar`; keluhan di-escape `"`. File `laporan_servis_hp_${t}.csv`.

⚠️ Laba servis basis kas vs piutang basis tagihan → bisa menyesatkan.

## 2. Backup, Restore, Cloud Sync — class `bg` (8588)

- Checksum: DJB2 32-bit 8 digit hex dari `JSON.stringify(tables)` (non-kripto).
- `createBackup()`: 16 tabel → envelope `{app:"FirdausServis",version:1,createdAt,checksum,tables}`, pretty JSON.
- `restoreBackup()`: validasi JSON → app → tables → checksum; transaksi DELETE 14 tabel (child→parent) + INSERT OR REPLACE per baris; return recordsRestored. ⚠️ `audit_logs` & `schema_migrations` ikut backup tapi tidak dihapus saat restore.
- `mergeCloudSync()`: validasi + PIN; FK OFF; key = `key` (settings) / `id`; update jika `updated_at` lebih baru; insert jika belum ada; duplikat `order_number` → suffix `-C`; return `{recordsAdded,recordsUpdated,hasLocalAdditions}`.
- AutoBackup `wg` (8588): IndexedDB `firdausservis_offline_backups_idb`/`backups`, migrasi dari localStorage, maks 5 snapshot harian, nama `FirdausServis_Backup_YYYY-MM-DD_HHmm.json`; share via native → Web Share API → download Blob.

## 3. Lisensi & Trial

### Deteksi trial `es()` (8372)
true jika: host `netlify.app` OR `VITE_TRIAL_MODE==="true"` OR query `?trial=true|demo=true` OR path `/trial|/demo` OR `window.__IS_TRIAL_MODE__===true`.

### Durasi & sesi
- `Mu = 15*60*1000` (15 menit).
- `ag()`: sessionStorage `firdaus_trial_session_start` → timer per tab/sesi.
- `ig()`: hapus sessionStorage + kunci DB + `firdaus_trial_has_run` → reload.
- `initWeb()` saat trial: DB binary dihapus, persistensi di-skip → **data hilang saat refresh**.
- UI: banner "Mode Trial — Data sementara", countdown MM:SS, modal "Waktu Demo 15 Menit Berakhir", tombol mulai ulang (11561–11695).
- Watermark cetak: *"NOTA INI DITERBITKAN DALAM MODE TRIAL / DEMO — TIDAK SAH…"* (10461, 10820–10830).
- WA penjualan `Uu = https://wa.me/6287810851738?text=...` (8372) → tombol "Beli Resmi".

### Lisensi `Gc` (8588)
- Secret `FIRDAUS_WEB_OFFLINE_LICENSE_PUB_2026` (plaintext di bundle).
- deviceId `FS-XXXX-YYYY` dari hash userAgent+screen; activation key `FS-ACT-XXXX-YYYY` (DJB2 deviceId+secret).
- `checkStatus()` **selalu** `{isLicensed:true,status:"ACTIVE",licenseKey:"FULL-COMMERCIAL-LIFETIME"}`; `activate()` selalu true; tidak ada pemanggilan validasi di UI → **tidak ada blokir lisensi**.

## 4. PIN aplikasi
Field `app_pin_hash` / `app_owner_pin` ada di settings & mergeCloudSync (sentinel "1234"), tapi **tidak ada fungsi hash/validasi PIN di bundle**. PIN "0000/1234" di UI adalah PIN pairing Bluetooth printer, bukan PIN aplikasi. Fitur PIN tidak aktif di build ini.

## 5. Utilitas
| Fungsi | Baris | Keterangan |
|---|---|---|
| `xe(prefix)` | 8423 | ID unik prefix+base36 time+random |
| `uh()` | 8423 | YYYYMMDD |
| `mh(n,4)` | 8423 | padStart |
| generateNextOrderNumber | 8433 | `FS-YYYYMMDD-0001` (MAX query, rentan duplikat konkuren, >9999 tak ditangani) |
| generateNextInvoiceNumber | 8493 | `TRX-YYYYMMDD-0001` |
| `$` | 9640 | Rupiah `Rp 1.234` |
| `eo` / `ht` | 9648/9662 | Intl.DateTimeFormat id-ID |
| `vn` | 9855 | label status servis |
| `Zo` | 9855 | sanitasi ESC/POS (buang non-ASCII) |
| `sb` | 9858 | padding dua kolom (32/48 char) |
| `Ch` | 9934 | Uint8Array → base64 |

## 6. Cetak / Struk / Faktur
Kanal: **Bluetooth SPP native** (`window.AndroidBluetoothPrinter`: getPairedPrinters, printRawEscPos(base64,MAC)), **RawBT** native, **Web Bluetooth BLE** (`navigator.bluetooth.requestDevice`), **window.print()** dengan `@page` dinamis (58mm auto / A4 portrait margin 8mm, class `print-format-thermal`/`print-format-a4`), **WhatsApp** (teks struk markdown → wa.me).

Builder ESC/POS class `Th` (9866): ESC @, GS ., ESC t 0, align/bold/doubleSize/text/line/twoCols/divider/feed/cut → Uint8Array.
- `nb(order,settings)` (9912): struk nota servis, lebar 32 (58mm)/48 (80mm); kop, No. Nota, pelanggan, perangkat, IMEI, kelengkapan, status, teknisi, keluhan, rincian, total tagihan/dibayar/sisa, garansi, footer, cut.
- `rb(sale,settings)` (9923): struk penjualan; faktur, item, subtotal, diskon, TOTAL, metode bayar, tunai & kembalian.
- Faktur A4 (10829–11056): judul dinamis (FAKTUR SERVIS KOMPUTER / FAKTUR TANDA TERIMA SERVIS / FAKTUR PENJUALAN RESMI), tabel rincian, tanda tangan teknisi, catatan pengambilan.
- Modal "Cetak Nota & Struk" (10285–10344): tab Struk Kasir (Thermal) / Faktur Resmi A4 / Panduan; tombol Cetak Bluetooth, Cetak Roll USB/AirPrint, Cetak A4/PDF, Kirim WhatsApp. Panduan (11326–11545) pairing PIN, RawBT, BLE, AirPrint, USB POS-58/80.

## Temuan kritis
1. Laba servis kas vs piutang tagihan — beda basis.
2. `servicesByStatus` abaikan filter periode.
3. Checksum non-kripto; restore hapus 14 tabel tanpa auto-backup selain snapshot harian.
4. Lisensi web selalu aktif; activation key dapat direkayasa.
5. Trial hanya UI + non-persisten, bisa di-reset.
6. PIN aplikasi tidak diimplementasikan.
