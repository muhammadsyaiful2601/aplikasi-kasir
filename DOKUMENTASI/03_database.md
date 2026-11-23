# Lapisan Database & Repository — Firdaus Servis

Sumber: `main.pretty.js` (beautify dari bundle Vite/React ter-minify), fokus baris ~8203–8588.

## 1. Skema Database (17 tabel)

Definisi ada di objek migrasi `ng` (baris 8203):
`ng = { version: 1, description: "Initial schema for FirdausServis (17 core relational tables)", up: [...] }`
`rg = [ng]` — hanya 1 migrasi resmi (versi 1). Semua PK bertipe `TEXT`, uang `INTEGER` (Rupiah), waktu `TEXT` (ISO-8601), `PRAGMA foreign_keys = ON`.

| # | Tabel | Kolom penting |
|---|---|---|
| 1 | `schema_migrations` | `version` PK, `applied_at`, `description` |
| 2 | `settings` | `key` PK, `value`, `updated_at`. Key: store_name, store_address, store_phone, store_header_notes, store_footer_notes, receipt_paper_size, default_warranty_days, currency, business_type, app_pin_hash, app_owner_pin, license_key, device_id, starter_products_seeded, autobackup_* |
| 3 | `customers` | id, name, phone, address, created_at, updated_at. Index: phone, name |
| 4 | `products` | id, name, sku(UNIQUE), barcode, category, cost_price, selling_price, stock, min_stock(2), unit('Pcs'), is_active(1), created_at, updated_at. Index: sku, barcode, category |
| 5 | `stock_movements` | id, product_id→products(CASCADE), type(INITIAL/SALE/SERVICE_USAGE/RETURN), quantity(absolut), previous_stock, new_stock, reference_id, notes, created_at |
| 6 | `service_orders` | id, order_number(UNIQUE `FS-YYYYMMDD-0001`), customer_id→customers, customer_name, customer_phone, device_brand, device_model, device_imei, device_condition, completeness, customer_complaint, technician_diagnosis, technician_notes, technician_name, status('DITERIMA'), estimated_cost, total_services_cost, total_parts_cost, total_discount, grand_total, total_paid, remaining_balance, payment_status(UNPAID/PARTIAL/PAID), warranty_duration_days, warranty_expiry_date, picked_up_at, created_at, updated_at |
| 7 | `service_order_items` | id, service_order_id→service_orders(CASCADE), item_type(LABOR/PART), product_id→products(SET NULL), name, quantity, cost_price_snapshot, selling_price_snapshot, subtotal, created_at |
| 8 | `service_status_history` | id, service_order_id(CASCADE), from_status, to_status, notes, created_at |
| 9 | `sales` | id, invoice_number(UNIQUE `TRX-YYYYMMDD-0001`), customer_id(SET NULL), subtotal, discount, grand_total, total_cost_snapshot, payment_status(PAID/CANCELLED), notes, created_at, updated_at |
| 10 | `sale_items` | id, sale_id(CASCADE), product_id, product_name_snapshot, cost_price_snapshot, selling_price_snapshot, quantity, discount, subtotal |
| 11 | `payments` | id, reference_type(SERVICE/SALE), reference_id, payment_method, amount, amount_tendered, change_returned, notes, created_at (polimorfik, tanpa FK) |
| 12 | `expenses` | id, category, amount, description, created_at |
| 13 | `warranties` | id, service_order_id(CASCADE), customer_id, start_date, end_date, terms, status(ACTIVE/CLAIMED/EXPIRED), created_at |
| 14 | `warranty_claims` | id, warranty_id(CASCADE), claim_date, complaint, technician_finding, action_taken, decision('ACCEPTED'), created_at |
| 15 | `cash_movements` | id, type(IN/OUT), amount, source(SALE_PAYMENT/SERVICE_PAYMENT/EXPENSE), reference_id, notes, created_at |
| 16 | `audit_logs` | id, action(DELETE_PRODUCT/DELETE_SERVICE), entity, entity_id, payload(JSON), created_at |
| 17 | (gabungan) `schema_migrations` + 16 tabel data = 17 sesuai deskripsi & array backup |

## 2. SqliteAdapter (class `cg`, singleton `It = new cg`, baris 8372)

- **Inisialisasi**: deteksi native via `Qs.isNativePlatform()`. Native (Capacitor `@capacitor-community/sqlite`, DB `firdausservis_db`, timeout 4 Detik) → fallback ke sql.js bila gagal. Web: fetch WASM (`sql-wasm-browser.wasm`/`sql-wasm.wasm`, validasi magic `\0asm`, timeout 10 detik), DB in-memory.
- **Persistensi web**: biner DB di IndexedDB (`firdausservis_offline_idb`/`sqlite_storage`/`sqlite_db_binary`) via `IdbStorage`; fallback localStorage base64. Debounce 150 ms + flush saat `beforeunload`/`pagehide`/`visibilitychange`. Migrasi dari localStorage lama (`firdausservis_sqlite_binary`).
- **Mode trial/demo** (`es()`, baris 8372): host netlify.app, `?trial=true|demo=true`, path `/trial|/demo`, `VITE_TRIAL_MODE`, `window.__IS_TRIAL_MODE__` → biner DB sengaja tidak dipersistenkan; `ig()` hapus semua kunci + reload.
- **Transaksi** `runTransaction(cb)`: re-entrant; native begin/commit/rollback; web `BEGIN;`/`COMMIT;`/`ROLLBACK;` + flush. Callback `{execute, query, queryOne}`.
- **`applyMigrationsInternal()`**: jalankan DDL versi 1, catat di `schema_migrations`. Patch non-versi: `ALTER TABLE service_orders ADD COLUMN customer_name/customer_phone` + backfill dari `customers`.

## 3. Repository & method

- **`dh` / IdbStorage** — get/set/delete/clear IndexedDB generik (fail-safe).
- **`ug` / Settings** — `getAll()` dengan default (Firdaus Servis, 58mm, garansi 30, IDR, HP); `set()`, `setMany()`.
- **`mg` / Customers** — getAll, getById, findByPhone (strip `-`/spasi), search(LIMIT 50), create, update, getCustomerSummary (total order/aktif/penjualan PAID/tagihan).
- **`pg` / Products** — getAll, getActive, getById, search(q,category), getCategories, getLowStock, create (+movement INITIAL), update (stock tidak diubah), adjustStock (bisa terima db eksternal), getStockMovements, delete (FK dimatikan sementara + audit_logs).
- **`hg` / ServiceOrders** (paling kompleks) — generateNextOrderNumber; getAll(filter AKTIF/SEMUA/status); getById (+items); create (+history awal); **updateStatus**: SUDAH_DIAMBIL → isi picked_up_at + auto-buat garansi bila hari > 0; BATAL/GAGAL → retur stok PART; updateWarrantyDuration; updateTechnicianName; addItem (validasi stok + movement SERVICE_USAGE + hitung ulang grand_total/remaining/payment_status); removeItem (retur + hitung ulang); updatePartsCost; addPayment (+cash_movements IN, hitung ulang); getStatusHistory; getPayments; delete (retur + hapus semua + audit_logs).
- **`fg` / Sales** — generateNextInvoiceNumber; getAll/getById (+items+payments); createSale (validasi stok semua item, cost snapshot, PAID, potong stok, movement SALE, payment + cash IN); cancelSale (CANCELLED + retur + cash OUT); deleteSale.
- **`xg` / Expenses & Reporting** — addExpense (+cash OUT), getExpenses, deleteExpense, getServicePayments (parts_cost dinamis), updateServicePartsCost, deleteServicePayment (hitung ulang), **getSummary** (laba kotor sales/jasa, laba kotor total, piutang, expenses, arus kas, laba bersih, status servis, top 5 produk), exportSalesCsv, exportServicesCsv.
- **`gg` / Warranty** — getAll (auto-EXPIRED), getById, getClaims, addClaim (ACCEPTED → status CLAIMED; tidak ubah stok/uang).
- **`bg` / Backup & Cloud Sync** — checksum djb2; createBackup (16 tabel JSON); restoreBackup (validasi app+checksum, hapus+insert transaksional); mergeCloudSync (merge by key/id + updated_at, konflik order_number → suffix `-C`, PIN owner, FK dimatikan).
- **`wg` / AutoBackup** — IndexedDB `firdausservis_offline_backups_idb`/`backups`, maks 5 snapshot (harian), share via native/Android Bluetooth printer / Web Share / download Blob.
- **`Gc` / License** — device_id `FS-XXXX-XXXX`, activation key djb2 dengan secret `FIRDAUS_WEB_OFFLINE_LICENSE_PUB_2026`, `checkStatus()` selalu ACTIVE "FULL-COMMERCIAL-LIFETIME", `activate()` selalu true (lisensi deklaratif, tidak memblokir).

## 4. Seeding & patch

- **Settings awal**: hanya bila store_name kosong atau mode trial. Nama toko `DEMO FIRDAUS SERVIS` saat trial.
- **5 starter products** (prod-starter-1..5): Kabel Data Type-C (12k/25k, stok20), Charger 20W (35k/65k, stok12), Tempered Glass (5k/15k, stok35), Baterai BN53 (75k/125k, stok4), LCD Realme C11/C12 (130k/220k, stok3). Flag `starter_products_seeded='1'`.
- **Demo data (trial only)**: 2 customer (Budi Santoso, Siti Rahma), 2 servis (FS-DEMO-001 Samsung A52 SEDANG_DIKERJAKAN; FS-DEMO-002 Redmi Note 10 SELESAI), 1 penjualan INV-DEMO-001 PAID (tendered 50k, kembalian 10k). Garansi demo tidak otomatis dibuat.

## 5. Poin logika bisnis kunci

- Stok konsisten via `stock_movements` (quantity absolut; arah dari type).
- Payment status dihitung ulang (PAID/PARTIAL/UNPAID) pada add/remove item & payment.
- Retur otomatis: batal/gagal servis, hapus item, hapus servis, batal/hapus sale, hapus expense/payment.
- Garansi otomatis saat status → SUDAH_DIAMBIL; auto-EXPIRED saat getAll; klaim ACCEPTED → CLAIMED.
- Nomor harian `FS-`/`TRX-` + YYYYMMDD + 4 digit (MAX query, bukan sequence).
- Sales dibatalkan via status CANCELLED (soft), check-out kasir langsung PAID.
- Mode trial non-persisten + seed demo; lisensi selalu ACTIVE.
