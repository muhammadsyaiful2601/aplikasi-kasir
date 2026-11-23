/* Modal "Lokasi Database" — dipanggil dari kartu menu di halaman Menu Lainnya.
   Tidak mengubah logika aplikasi. */
(function () {
  function waitForStorage(cb, tries) {
    if (window.__firdausStorage) return cb(window.__firdausStorage);
    if ((tries || 0) > 100) return;
    setTimeout(function () { waitForStorage(cb, (tries || 0) + 1); }, 100);
  }

  function el(tag, style, text) {
    var e = document.createElement(tag);
    if (style) e.setAttribute("style", style);
    if (text !== void 0) e.textContent = text;
    return e;
  }

  var overlay = null;
  var S = null;

  function close() {
    if (overlay && overlay.parentNode) overlay.parentNode.removeChild(overlay);
    overlay = null;
    document.removeEventListener("keydown", onKey);
  }
  function onKey(e) { if (e.key === "Escape") close(); }

  function button(label, bg, onClick) {
    var b = el("button",
      "flex:1;border:0;border-radius:8px;padding:10px 12px;" +
      "background:" + bg + ";color:#fff;font-size:12px;font-weight:700;" +
      "cursor:pointer;transition:opacity .15s;", label);
    b.onmouseenter = function () { b.style.opacity = ".85"; };
    b.onmouseleave = function () { b.style.opacity = "1"; };
    b.onclick = onClick;
    return b;
  }

  function build() {
    overlay = el("div",
      "position:fixed;inset:0;z-index:10000;background:rgba(15,23,42,.55);" +
      "display:flex;align-items:center;justify-content:center;padding:20px;");

    var card = el("div",
      "background:#fff;border-radius:18px;width:100%;max-width:460px;" +
      "box-shadow:0 20px 60px rgba(0,0,0,.3);overflow:hidden;font-family:system-ui,sans-serif;");

    var head = el("div",
      "padding:18px 20px 14px;border-bottom:1px solid #e2e8f0;" +
      "display:flex;align-items:center;justify-content:space-between;");
    head.appendChild(el("div", "font-size:15px;font-weight:800;color:#0f172a;", "Lokasi Database"));
    var x = el("button", "border:0;background:transparent;font-size:20px;color:#64748b;cursor:pointer;line-height:1;", "×");
    x.onclick = close;
    head.appendChild(x);
    card.appendChild(head);

    var body = el("div", "padding:18px 20px;");

    var statusBox = el("div",
      "background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;" +
      "padding:12px 14px;font-size:12px;color:#334155;line-height:1.7;margin-bottom:14px;");
    body.appendChild(statusBox);

    var msg = el("div", "font-size:11px;min-height:16px;margin-bottom:12px;color:#b91c1c;");
    body.appendChild(msg);

    var info = el("div",
      "background:#fffbeb;border:1px solid #fde68a;border-radius:10px;" +
      "padding:10px 12px;font-size:11px;color:#92400e;line-height:1.6;margin-bottom:14px;",
      "Pilih file untuk menyimpan database. Data lama di browser akan otomatis dipindahkan. " +
      "Gunakan Chrome/Edge dan buka lewat http://localhost agar fitur ini tersedia.");
    body.appendChild(info);

    var row = el("div", "display:flex;gap:8px;");
    row.appendChild(button("Pilih / Ganti Lokasi…", "#2563eb", function () {
      msg.style.color = "#64748b";
      msg.textContent = "Membuka dialog pemilih file…";
      S.pickLocation().then(function (r) {
        msg.style.color = "#15803d";
        msg.textContent = "Berhasil: " + r.name + " (" + r.keys + " entri). Muat ulang aplikasi.";
        refresh();
      }).catch(function (e) {
        msg.style.color = "#b91c1c";
        msg.textContent = e.name === "AbortError" ? "Dibatalkan." : "Gagal: " + e.message;
      });
    }));
    row.appendChild(button("Kembali ke Browser", "#64748b", function () {
      S.resetToBrowser().then(function () {
        msg.style.color = "#15803d";
        msg.textContent = "Kembali ke mode browser. Muat ulang aplikasi.";
        refresh();
      }).catch(function (e) {
        msg.style.color = "#b91c1c";
        msg.textContent = "Gagal: " + e.message;
      });
    }));
    body.appendChild(row);

    var footer = el("div", "padding:0 20px 18px;text-align:right;");
    var tutup = el("button",
      "border:1px solid #cbd5e1;background:#fff;color:#475569;" +
      "border-radius:8px;padding:8px 16px;font-size:12px;font-weight:700;cursor:pointer;",
      "Tutup");
    tutup.onclick = close;
    footer.appendChild(tutup);
    card.appendChild(body);
    card.appendChild(footer);

    overlay.appendChild(card);
    overlay.onclick = function (e) { if (e.target === overlay) close(); };
    document.body.appendChild(overlay);
    document.addEventListener("keydown", onKey);

    function refresh() {
      S.getInfo().then(function (i) {
        statusBox.innerHTML =
          "<b>Mode penyimpanan:</b> " + (i.mode === "file" ? "File" : "Browser / IndexedDB") + "<br>" +
          "<b>Nama file:</b> " + (i.name || "-") + "<br>" +
          "<b>Data tersimpan:</b> " + i.keys + " entri" +
          (i.canUseFile ? "" : "<br><b style='color:#b91c1c'>Browser tidak mendukung file picker.</b>");
      }).catch(function (e) {
        statusBox.textContent = "Gagal membaca status: " + e.message;
      });
    }
    refresh();
  }

  window.__openDbSettings = function () {
    if (overlay) close();
    waitForStorage(function (s) {
      if (!s) {
        alert("Modul penyimpanan belum siap. Silakan muat ulang halaman.");
        return;
      }
      S = s;
      build();
    });
  };
})();
