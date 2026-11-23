/* Uji mandiri class dh (tanpa browser) dengan mock IndexedDB + file handle. */
const fs = require("fs");
const vm = require("vm");
const path = require("path");

const code = fs.readFileSync(path.join(__dirname, "storage-class.js"), "utf8");

let fileText = "";
const storeMem = { "handles:dbfile": {
  name: "databasesaya.fdb",
  queryPermission: async () => "granted",
  getFile: async () => ({ text: async () => fileText }),
  createWritable: async () => ({
    write: async t => { fileText = t; },
    close: async () => {}
  })
} };

function makeReq(action, storeName) {
  const q = {};
  setTimeout(() => {
    const ops = {
      get: key => storeMem[`${storeName}:${key}`],
      put: (val, key) => { storeMem[`${storeName}:${key}`] = val; return true; },
      delete: key => { delete storeMem[`${storeName}:${key}`]; return true; },
      getAllKeys: () => Object.keys(storeMem)
        .filter(k => k.startsWith(storeName + ":"))
        .map(k => k.slice(storeName.length + 1)),
      clear: () => { for (const k of Object.keys(storeMem)) if (k.startsWith(storeName + ":")) delete storeMem[k]; return true; }
    };
    try { q.result = ops[action](...q.args); } catch (e) { q.result = void 0; }
    q.onsuccess && q.onsuccess();
  }, 0);
  return q;
}

function wrapOp(storeName, action) {
  return function (...args) {
    const q = makeReq(action, storeName);
    q.args = args;
    return q;
  };
}

const fakeIndexedDB = {
  open() {
    const req = {};
    setTimeout(() => {
      const db = {
        objectStoreNames: { contains: () => true },
        createObjectStore() {},
        transaction(storeName) {
          return {
            objectStore() {
              return {
                get: wrapOp(storeName, "get"),
                put: wrapOp(storeName, "put"),
                delete: wrapOp(storeName, "delete"),
                getAllKeys: wrapOp(storeName, "getAllKeys"),
                clear: wrapOp(storeName, "clear")
              };
            }
          };
        }
      };
      req.result = db;
      req.onupgradeneeded && req.onupgradeneeded();
      req.onsuccess && req.onsuccess();
    }, 0);
    return req;
  }
};

const ctx = {
  window: { indexedDB: fakeIndexedDB, showSaveFilePicker: async () => storeMem["handles:dbfile"] },
  Ae: (o, k, v) => { o[k] = v; },
  btoa: s => Buffer.from(s, "binary").toString("base64"),
  atob: s => Buffer.from(s, "base64").toString("binary"),
  console,
  setTimeout,
  Promise
};
ctx.window.window = ctx.window;
vm.createContext(ctx);
vm.runInContext(code, ctx);

const S = ctx.window.__firdausStorage;

(async () => {
  const store = new S("firdausservis_offline_idb", "sqlite_storage");
  const bytes = new Uint8Array([0, 1, 2, 250, 255, 128]);


  const okSet = await store.set("sqlite_db_binary", bytes);
  const got = await store.get("sqlite_db_binary");
  const same = ArrayBuffer.isView(got) && bytes.length === got.length && bytes.every((b, i) => b === got[i]);

  await store.set("nama", "Toko Saya");
  const nama = await store.get("nama");

  const info = await S.getInfo();

  await store.delete("sqlite_db_binary");
  const afterDelete = await store.get("sqlite_db_binary");

  console.log("set()               :", okSet);
  console.log("get() Uint8Array    :", same ? "OK (identik)" : "GAGAL -> " + JSON.stringify(got));
  console.log("get() string        :", nama === "Toko Saya" ? "OK" : "GAGAL -> " + nama);
  console.log("getInfo()           :", JSON.stringify(info));
  console.log("delete()            :", afterDelete === null ? "OK" : "GAGAL");
  console.log("file JSON           :", fileText.slice(0, 120) + "...");

  if (!okSet || !same || nama !== "Toko Saya" || info.mode !== "file" || afterDelete !== null) {
    process.exit(1);
  }
  console.log("\nSEMUA UJI LULUS");
})().catch(e => { console.error("UJI GAGAL:", e); process.exit(1); });
