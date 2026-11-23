/* Server statis sederhana untuk preview.
   Tidak ada build step: edit file di folder app/ lalu refresh browser. */
const http = require("http");
const fs = require("fs");
const path = require("path");

const PORT = Number(process.env.PORT || 5180);
const ROOT = path.resolve(__dirname, "..", "app");

const MIME = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".mjs": "text/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".png": "image/png",
  ".ico": "image/x-icon",
  ".wasm": "application/wasm",
  ".apk": "application/vnd.android.package-archive",
  ".svg": "image/svg+xml",
  ".txt": "text/plain; charset=utf-8"
};

function send(res, code, data, type) {
  res.writeHead(code, {
    "Content-Type": type || "application/octet-stream",
    "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
    "Pragma": "no-cache",
    "Access-Control-Allow-Origin": "*"
  });
  res.end(data);
}

const server = http.createServer((req, res) => {
  let urlPath;
  try {
    urlPath = decodeURIComponent(new URL(req.url, "http://localhost").pathname);
  } catch {
    return send(res, 400, "Bad request", "text/plain");
  }

  if (urlPath === "/") urlPath = "/index.html";

  let filePath = path.join(ROOT, urlPath);
  if (!filePath.startsWith(ROOT)) return send(res, 403, "Forbidden", "text/plain");

  fs.stat(filePath, (err, st) => {
    if (err || st.isDirectory()) {
      // SPA fallback
      const fallback = path.join(ROOT, "index.html");
      return fs.readFile(fallback, (e, buf) => {
        if (e) return send(res, 404, "Not found", "text/plain");
        send(res, 200, buf, MIME[".html"]);
      });
    }
    fs.readFile(filePath, (e, buf) => {
      if (e) return send(res, 404, "Not found", "text/plain");
      const ext = path.extname(filePath).toLowerCase();
      send(res, 200, buf, MIME[ext] || "application/octet-stream");
    });
  });
});

server.listen(PORT, "127.0.0.1", () => {
  console.log("PREVIEW siap: http://localhost:" + PORT);
  console.log("Folder sumber: " + ROOT);
  console.log("Tekan CTRL+C untuk berhenti.");
});
