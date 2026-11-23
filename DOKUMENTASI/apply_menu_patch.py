"""Tambahkan kartu 'Lokasi Database' ke halaman Menu Lainnya (komponen Tb)."""

OLD = ('{id:"backup",title:"Backup & Pemulihan Data",'
       'desc:"Cadangkan data ke file atau pulihkan database saat ganti HP",'
       'icon:gh,color:"text-teal-700 bg-teal-50",action:()=>_(!0)}];return n.jsxs("div"')

NEW = ('{id:"backup",title:"Backup & Pemulihan Data",'
       'desc:"Cadangkan data ke file atau pulihkan database saat ganti HP",'
       'icon:gh,color:"text-teal-700 bg-teal-50",action:()=>_(!0)},'
       '{id:"lokasi_database",title:"Lokasi Database",'
       'desc:"Pilih atau pindahkan file penyimpanan database",'
       'icon:gh,color:"text-blue-700 bg-blue-50",'
       'action:()=>{window.__openDbSettings&&window.__openDbSettings()}}];return n.jsxs("div"')


def patch(src: str) -> str:
    if 'id:"lokasi_database"' in src:
        return src
    if OLD not in src:
        raise SystemExit("Marker menu backup tidak ditemukan")
    return src.replace(OLD, NEW, 1)


if __name__ == "__main__":
    import sys
    path = sys.argv[1]
    src = open(path, encoding="utf-8").read()
    out = patch(src)
    open(path, "w", encoding="utf-8").write(out)
    print("Menu 'Lokasi Database' ditambahkan" if out != src else "Menu sudah ada")
