"""Hilangkan mode trial 15 menit & lisensi dari bundle.

Patch yang dilakukan:
1. es() -> selalu false (matikan deteksi trial, timer, seed demo; aktifkan persistensi penuh)
2. Hapus watermark thermal & A4
3. Ganti komponen banner/modal trial (pb) dengan null
4. Hapus tautan WA penjualan (Uu)

Bisa dijalankan berulang: jika patch sudah ada, tidak ada yang diubah.
"""
import sys


def patch(src: str) -> str:
    changes = []

    # 1. es() -> false
    start = src.find("es=()=>{")
    if start >= 0:
        depth = 0
        k = src.find("{", start)
        j = k
        quote = None
        escaped = False
        while j < len(src):
            c = src[j]
            if quote:
                if escaped:
                    escaped = False
                elif c == "\\":
                    escaped = True
                elif c == quote:
                    quote = None
                j += 1
                continue
            if c in ('"', "'", "`"):
                quote = c
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        old = src[start:j + 1]
        src = src[:start] + "es=()=>!1" + src[j + 1:]
        changes.append("es() -> false")
    elif "es=()=>!1" in src:
        changes.append("es() sudah false")
    else:
        raise SystemExit("Definisi es() tidak ditemukan")

    # 2a. Watermark thermal
    thermal = ('es()&&n.jsxs("div",{className:"text-center pt-2 border-t border-dashed '
               'border-amber-300 mt-2 text-[8px] text-amber-800 font-bold uppercase '
               'tracking-wider",children:["*** DITERBITKAN DALAM MODE TRIAL DEMO ***",'
               'n.jsx("br",{}),"Beli Versi Resmi: WhatsApp 0878-1085-1738"]})')
    if thermal in src:
        src = src.replace(thermal, "")
        changes.append("watermark thermal dihapus")
    else:
        changes.append("watermark thermal sudah tidak ada")

    # 2b. Watermark A4 (termasuk koma setelahnya)
    a4 = ('es()&&n.jsx("div",{className:"bg-amber-100 border-2 border-dashed '
          'border-amber-500 text-amber-950 p-2.5 rounded-xl text-center font-black '
          'text-xs uppercase tracking-wider",children:'
          '"⚠️ NOTA INI DITERBITKAN DALAM MODE TRIAL / DEMO — TIDAK SAH SEBAGAI '
          'BUKTI TRANSAKSI RESMI TOKO"}),')
    if a4 in src:
        src = src.replace(a4, "")
        changes.append("watermark A4 dihapus")
    else:
        changes.append("watermark A4 sudah tidak ada")

    # 2c. Watermark thermal versi teks (third block)
    thermal2 = ('es()&&n.jsxs("div",{className:"bg-amber-100 text-amber-900 border '
                'border-dashed border-amber-400 p-1 mb-2 text-center text-[9px] '
                'font-black uppercase tracking-wider",children:'
                '["*** VERSI TRIAL / DEMO EVALUASI ***",n.jsx("br",{}),'
                '"TIDAK SAH UNTUK TRANSAKSI RESMI"]}),')
    if thermal2 in src:
        src = src.replace(thermal2, "")
        changes.append("watermark thermal teks dihapus")
    else:
        changes.append("watermark thermal teks sudah tidak ada")

    # 3. Komponen pb -> null
    s = src.find("pb=()=>{")
    if s >= 0:
        e = src.find(",hb=", s)
        if e < 0:
            raise SystemExit("Marker ,hb= tidak ditemukan setelah pb")
        src = src[:s] + "pb=()=>null" + src[e:]
        changes.append("banner/modal trial (pb) -> null")
    elif "pb=()=>null" in src:
        changes.append("pb sudah null")
    else:
        changes.append("pb tidak ditemukan")

    # 4. Tautan WA penjualan
    s = src.find(',Uu="https://wa.me/')
    if s >= 0:
        e = src.find(";", s)
        if e < 0:
            raise SystemExit("Titik koma setelah Uu tidak ditemukan")
        src = src[:s] + src[e:]
        changes.append("tautan WA penjualan dihapus")
    else:
        changes.append("tautan WA sudah tidak ada")

    # 5. Sisa konstanta & fungsi sesi trial yang sudah tidak dipakai (Mu, ag, ig)
    s = src.find(",Mu=15*60*1e3")
    if s >= 0:
        j = src.find("class dh", s)
        if j < 0:
            raise SystemExit("Marker class dh tidak ditemukan setelah Mu")
        src = src[:s] + ";" + src[j:]
        changes.append("Mu/ag/ig (sisa sesi trial) dihapus")
    else:
        changes.append("Mu/ag/ig sudah tidak ada")

    return src, changes


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("Pemakaian: python apply_trial_patch.py <file bundle>")
    path = sys.argv[1]
    src = open(path, encoding="utf-8").read()
    out, changes = patch(src)
    open(path, "w", encoding="utf-8").write(out)
    for c in changes:
        print(" -", c)
    print("Ukuran akhir:", len(out), "byte")
