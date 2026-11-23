/* Panel kecil untuk mengatur lokasi penyimpanan database.
   Dimuat sebelum bundle utama. Tidak mengubah logika aplikasi. */
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

  waitForStorage(function (S) {
    var wrap = el("div", "position:fixed;left:10px;bottom:78px;z-index:9999;font-family:system-ui,sans-serif;");
    var info = el("div",
      "background:#0f172a;color:#e2e8f0;border-radius:10px;padding:8px 11px;font-size:11px;" +
      "box-shadow:0 4px 18px rgba(0,0,0,.28);max-width:250px;line-height:1.5;cursor:pointer;");
    info.textContent = "Database: memeriksa…";
    wrap.appendChild(info);

    var panel = el("div",
      "display:none;background:#fff;border:1px solid #cbd5e1;border-radius:10px;padding:10px;" +
      "margin-bottom:6px;width:250px;box-shadow:0 6px 24px rgba(0,0,0,.25);");
    var title = el("div", "font-weight:700;font-size:12px;color:#0f172a;margin-bottom:6px;", "LOKASI DATABASE");
    panel.appendChild(title);

    var detail = el("div", "font-size:11px;color:#475569;margin-bottom:8px;line-height:1.5;", "");
    panel.appendChild(detail);

    var status = el("div", "font-size:11px;color:#b91c1c;margin-bottom:8px;min-height:14px;", "");
    panel.appendChild(status);

    function btn(label, bg) {
      var b = el("button",
        "display:block;width:100%;border:0;border-radius:7px;padding:7px 9px;margin-top:5px;" +
        "background:" + bg + ";color:#fff;font-size:11px;font-weight:600;cursor:pointer;");
      b.textContent = label;
      return b;
    }

    var bPilih = btn("Pilih / Ganti Lokasi…", "#2563eb");
    var bBrowser = btn("Kembali ke Browser", "#64748b");
    var bRefresh = btn("Perbarui Status", "#0f766e");
    panel.appendChild(bPilih);
    panel.appendChild(bBrowser);
    panel.appendChild(bRefresh);

    wrap.appendChild(panel);
    document.body.appendChild(wrap);

    function render(i) {
      if (i.mode === "file") {
        info.textContent = "📁 Database: " + (i.name || "file terhubung") + " (" + i.keys + " data)";
        detail.innerHTML =
          "<b>Mode:</b> File di lokasi pilihan<br>" +
          "<b>Nama file:</b> " + (i.name || "-") + "<br>" +
          "<b>Data tersimpan:</b> " + i.keys + " entri";
      } else {
        info.textContent = "🌐 Database: Browser (klik untuk atur file)";
        detail.innerHTML =
          "<b>Mode:</b> Browser / IndexedDB<br>" +
          "<b>Catatan:</b> data masih tersimpan di profil browser. " +
          "Klik tombol pertama untuk memilih file database." +
          (i.canUseFile ? "" : "<br><b style='color:#b91c1c'>Browser tidak mendukung file picker. Gunakan Chrome/Edge desktop.</b>");
      }
    }

    function refresh() {
      S.getInfo().then(render).catch(function (e) {
        status.textContent = "Gagal membaca status: " + e.message;
      });
    }

    info.addEventListener("click", function () {
      panel.style.display = panel.style.display === "block" ? "none" : "block";
      if (panel.style.display === "block") refresh();
    });

    bRefresh.addEventListener("click", refresh);

    bPilih.addEventListener("click", function () {
      status.textContent = "Membuka dialog pemilih file…";
      S.pickLocation().then(function (r) {
        status.style.color = "#15803d";
        status.textContent = "Berhasil: " + r.name + " (" + r.keys + " entri dipindahkan). Muat ulang halaman.";
        refresh();
      }).catch(function (e) {
        status.style.color = "#b91c1c";
        status.textContent = e.name === "AbortError" ? "Dibatalkan." : "Gagal: " + e.message;
      });
    });

    bBrowser.addEventListener("click", function () {
      S.resetToBrowser().then(function () {
        status.style.color = "#15803d";
        status.textContent = "Kembali ke mode browser. Muat ulang halaman.";
        refresh();
      }).catch(function (e) {
        status.style.color = "#b91c1c";
        status.textContent = "Gagal: " + e.message;
      });
    });

    refresh();
  });
})();
