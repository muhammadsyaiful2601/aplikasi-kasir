class dh {
  constructor(t, s = "keyvalue") {
    Ae(this, "dbPromise", null);
    this.dbName = t;
    this.storeName = s;
  }
  isSupported() {
    return typeof window < "u" && typeof window.indexedDB < "u";
  }

  /* ---------- IndexedDB (kode asli, dipakai sebagai fallback) ---------- */
  _getDb() {
    return this.isSupported() ? this.dbPromise ? this.dbPromise : (this.dbPromise = new Promise(t => {
      try {
        const s = window.indexedDB.open(this.dbName, 1);
        s.onupgradeneeded = () => {
          const r = s.result;
          r.objectStoreNames.contains(this.storeName) || r.createObjectStore(this.storeName);
        };
        s.onsuccess = () => t(s.result);
        s.onerror = r => {
          console.warn(`[IdbStorage] Failed to open IndexedDB (${this.dbName}):`, s.error || r);
          this.dbPromise = null;
          t(null);
        };
      } catch (s) {
        console.warn(`[IdbStorage] Error initializing IndexedDB (${this.dbName}):`, s);
        this.dbPromise = null;
        t(null);
      }
    })) : Promise.resolve(null);
  }
  _idbGet(t) {
    return this._getDb().then(s => s ? new Promise(r => {
      try {
        const o = s.transaction(this.storeName, "readonly").objectStore(this.storeName).get(t);
        o.onsuccess = () => r(o.result ?? null);
        o.onerror = () => r(null);
      } catch { r(null); }
    }) : null).catch(() => null);
  }
  _idbSet(t, s) {
    return this._getDb().then(r => r ? new Promise(a => {
      try {
        const d = r.transaction(this.storeName, "readwrite").objectStore(this.storeName).put(s, t);
        d.onsuccess = () => a(!0);
        d.onerror = u => { console.warn(`[IdbStorage] Put failed for key "${t}":`, d.error || u); a(!1); };
      } catch { a(!1); }
    }) : !1).catch(() => !1);
  }
  _idbDelete(t) {
    return this._getDb().then(s => s ? new Promise(r => {
      try {
        const o = s.transaction(this.storeName, "readwrite").objectStore(this.storeName).delete(t);
        o.onsuccess = () => r(!0);
        o.onerror = () => r(!1);
      } catch { r(!1); }
    }) : !1).catch(() => !1);
  }
  _idbClear() {
    return this._getDb().then(t => t ? new Promise(s => {
      try {
        const i = t.transaction(this.storeName, "readwrite").objectStore(this.storeName).clear();
        i.onsuccess = () => s(!0);
        i.onerror = () => s(!1);
      } catch { s(!1); }
    }) : !1).catch(() => !1);
  }

  /* ---------- File System Access API ---------- */
  static canUseFile() {
    return typeof window !== "undefined" && typeof window.showSaveFilePicker === "function";
  }
  static _legacyKey(key) {
    return key.replace("aplikasikasir_", "firdausservis_");
  }
  static _metaDb(legacy) {
    return new Promise(resolve => {
      if (typeof window === "undefined" || !window.indexedDB) return resolve(null);
      try {
        const req = window.indexedDB.open(legacy ? "firdaus_filedb_meta" : "aplikasikasir_filedb_meta", 1);
        req.onupgradeneeded = () => {
          const db = req.result;
          if (!db.objectStoreNames.contains("handles")) db.createObjectStore("handles");
        };
        req.onsuccess = () => resolve(req.result);
        req.onerror = () => resolve(null);
      } catch { resolve(null); }
    });
  }
  static async _readHandle(db) {
    if (!db) return null;
    return new Promise(res => {
      try {
        const q = db.transaction("handles", "readonly").objectStore("handles").get("dbfile");
        q.onsuccess = () => res(q.result || null);
        q.onerror = () => res(null);
      } catch { res(null); }
    });
  }
  static async getHandle() {
    let h = await dh._readHandle(await dh._metaDb(false));
    if (!h) h = await dh._readHandle(await dh._metaDb(true));
    return h;
  }
  static async setHandle(h) {
    const db = await dh._metaDb();
    if (!db) return false;
    return new Promise(res => {
      try {
        const q = db.transaction("handles", "readwrite").objectStore("handles").put(h, "dbfile");
        q.onsuccess = () => res(!0);
        q.onerror = () => res(!1);
      } catch { res(!1); }
    });
  }
  static async clearHandle() {
    const db = await dh._metaDb();
    if (!db) return false;
    return new Promise(res => {
      try {
        const q = db.transaction("handles", "readwrite").objectStore("handles").delete("dbfile");
        q.onsuccess = () => res(!0);
        q.onerror = () => res(!1);
      } catch { res(!1); }
    });
  }
  static _toB64(bytes) {
    let out = "";
    const chunk = 0x8000;
    for (let i = 0; i < bytes.length; i += chunk) {
      out += String.fromCharCode.apply(null, bytes.subarray(i, i + chunk));
    }
    return btoa(out);
  }
  static _fromB64(b64) {
    const s = atob(b64);
    const a = new Uint8Array(s.length);
    for (let i = 0; i < s.length; i++) a[i] = s.charCodeAt(i);
    return a;
  }
  static _pack(value) {
    if (value && typeof value === "object" && typeof ArrayBuffer !== "undefined" && ArrayBuffer.isView(value) && !(value instanceof DataView)) {
      return { __fdb_b64: dh._toB64(new Uint8Array(value.buffer, value.byteOffset, value.byteLength)) };
    }
    if (value instanceof ArrayBuffer) return { __fdb_b64: dh._toB64(new Uint8Array(value)) };
    return value;
  }
  static _unpack(value) {
    if (value && typeof value === "object" && value.__fdb_b64 !== void 0) return dh._fromB64(value.__fdb_b64);
    return value;
  }
  static async _ensurePermission(h) {
    try {
      if (h.queryPermission && await h.queryPermission({ mode: "readwrite" }) === "prompt") {
        await h.requestPermission({ mode: "readwrite" });
      }
    } catch { /* diabaikan; operasi akan mencoba langsung */ }
  }
  static async _readFile(h) {
    const f = await h.getFile();
    const txt = await f.text();
    if (!txt.trim()) return {};
    const obj = JSON.parse(txt);
    for (const k of Object.keys(obj)) obj[k] = dh._unpack(obj[k]);
    return obj;
  }
  static async _writeFile(h, obj) {
    const copy = {};
    for (const k of Object.keys(obj)) copy[k] = dh._pack(obj[k]);
    const w = await h.createWritable();
    await w.write(JSON.stringify(copy));
    await w.close();
  }
  static _queue() {
    if (!dh._writeChain) dh._writeChain = Promise.resolve();
    return dh._writeChain;
  }
  static _runExclusive(fn) {
    const run = dh._queue().then(fn, fn);
    dh._writeChain = run.catch(() => {});
    return run;
  }
  _key(t) {
    return `${this.dbName}|${this.storeName}|${t}`;
  }
  async _fileData() {
    const h = await dh.getHandle();
    if (!h || !dh.canUseFile()) return null;
    await dh._ensurePermission(h);
    return { h, data: await dh._readFile(h) };
  }

  /* ---------- API publik: file dulu, fallback ke IndexedDB ---------- */
  async get(t) {
    try {
      const box = await this._fileData();
      if (box) {
        const key = this._key(t);
        if (box.data[key] !== void 0) return box.data[key];
        const legacy = dh._legacyKey(key);
        if (legacy !== key && box.data[legacy] !== void 0) return box.data[legacy];
        return null;
      }
    } catch (e) {
      console.warn("[FileStorage] gagal baca file, pakai IndexedDB:", e);
    }
    return this._idbGet(t);
  }
  async set(t, s) {
    try {
      const box = await this._fileData();
      if (box) {
        await dh._runExclusive(async () => {
          const fresh = await dh._readFile(box.h);
          const key = this._key(t);
          const legacy = dh._legacyKey(key);
          if (legacy !== key) delete fresh[legacy];
          fresh[key] = s;
          await dh._writeFile(box.h, fresh);
        });
        return true;
      }
    } catch (e) {
      console.warn("[FileStorage] gagal tulis file, pakai IndexedDB:", e);
    }
    return this._idbSet(t, s);
  }
  async delete(t) {
    try {
      const box = await this._fileData();
      if (box) {
        await dh._runExclusive(async () => {
          const fresh = await dh._readFile(box.h);
          const key = this._key(t);
          const legacy = dh._legacyKey(key);
          delete fresh[key];
          if (legacy !== key) delete fresh[legacy];
          await dh._writeFile(box.h, fresh);
        });
        return true;
      }
    } catch (e) {
      console.warn("[FileStorage] gagal hapus di file:", e);
    }
    return this._idbDelete(t);
  }
  async clear() {
    try {
      const box = await this._fileData();
      if (box) {
        const prefix = `${this.dbName}|${this.storeName}|`;
        const legacyPrefix = dh._legacyKey(prefix);
        await dh._runExclusive(async () => {
          const fresh = await dh._readFile(box.h);
          for (const k of Object.keys(fresh)) {
            if (k.startsWith(prefix) || k.startsWith(legacyPrefix)) delete fresh[k];
          }
          await dh._writeFile(box.h, fresh);
        });
        return true;
      }
    } catch (e) {
      console.warn("[FileStorage] gagal kosongkan di file:", e);
    }
    return this._idbClear();
  }

  /* ---------- Fungsi untuk modal "Lokasi Database" ---------- */
  static async _collectLegacy() {
    const out = {};
    const specs = [
      ["aplikasikasir_offline_idb", ["sqlite_storage"]],
      ["aplikasikasir_offline_backups_idb", ["backups"]],
      ["firdausservis_offline_idb", ["sqlite_storage"]],
      ["firdausservis_offline_backups_idb", ["backups"]]
    ];
    for (const [dbName, stores] of specs) {
      const db = await new Promise(res => {
        try {
          const r = indexedDB.open(dbName, 1);
          r.onsuccess = () => res(r.result);
          r.onerror = () => res(null);
        } catch { res(null); }
      });
      if (!db) continue;
      for (const storeName of stores) {
        if (!db.objectStoreNames.contains(storeName)) continue;
        const keys = await new Promise(res => {
          try {
            const q = db.transaction(storeName, "readonly").objectStore(storeName).getAllKeys();
            q.onsuccess = () => res(q.result || []);
            q.onerror = () => res([]);
          } catch { res([]); }
        });
        for (const key of keys) {
          const val = await new Promise(res => {
            try {
              const q = db.transaction(storeName, "readonly").objectStore(storeName).get(key);
              q.onsuccess = () => res(q.result);
              q.onerror = () => res(void 0);
            } catch { res(void 0); }
          });
          if (val !== void 0) out[`${dbName}|${storeName}|${key}`] = val;
        }
      }
    }
    return out;
  }
  static async pickLocation() {
    if (!dh.canUseFile()) {
      throw new Error("Browser tidak mendukung File System Access API. Gunakan Chrome atau Edge desktop, lalu buka lewat http://localhost (bukan file://).");
    }
    const h = await window.showSaveFilePicker({
      suggestedName: "databasesaya.fdb",
      types: [{ description: "File database Aplikasi Kasir", accept: { "application/octet-stream": [".fdb", ".json"] } }]
    });
    const data = await dh._collectLegacy();
    await dh._writeFile(h, data);
    await dh.setHandle(h);
    return { name: h.name, keys: Object.keys(data).length };
  }
  static async resetToBrowser() {
    await dh.clearHandle();
    return true;
  }
  static async getInfo() {
    const h = await dh.getHandle();
    let keys = 0;
    let name = "";
    if (h && dh.canUseFile()) {
      try {
        await dh._ensurePermission(h);
        const data = await dh._readFile(h);
        keys = Object.keys(data).length;
        name = h.name;
      } catch (e) { name = `${h.name} (perlu izin)`; }
    }
    return {
      canUseFile: dh.canUseFile(),
      mode: h ? "file" : "browser",
      name,
      keys
    };
  }
}
window.__aplikasikasirStorage = dh;
