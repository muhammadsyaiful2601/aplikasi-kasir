"""Pakai logo baru (KASIR SERVIS) di hero & sesuaikan warna brand."""

OLD = [
    ('className:"relative z-10 w-28 sm:w-36 h-28 sm:h-36 -mr-2 -my-2 flex items-center justify-center pointer-events-none",children:n.jsx("img",{src:"/logo.png",alt:"Teknisi AplikasiKasir",className:"w-full h-full object-contain filter drop-shadow-xl"})',
     'className:"relative z-10 w-40 sm:w-56 h-20 sm:h-24 -mr-2 flex items-center justify-center pointer-events-none",children:n.jsx("img",{src:"/assets/logo-hero.png",alt:"Logo Aplikasi Kasir",className:"w-full h-full object-contain filter drop-shadow-xl"})'),
    ('bg-gradient-to-r from-blue-600 via-sky-500 to-sky-400 text-white p-5 shadow-lg shadow-blue-500/20',
     'bg-gradient-to-r from-blue-700 via-blue-600 to-emerald-500 text-white p-5 shadow-lg shadow-blue-700/20'),
    ('bg-sky-300/20 rounded-full blur-lg', 'bg-emerald-300/20 rounded-full blur-lg'),
    ('px-4 py-2 bg-orange-500 hover:bg-orange-600 active:scale-95 text-white font-bold text-xs rounded-xl shadow-md shadow-orange-500/30 transition-all cursor-pointer',
     'px-4 py-2 bg-emerald-600 hover:bg-emerald-700 active:scale-95 text-white font-bold text-xs rounded-xl shadow-md shadow-emerald-600/30 transition-all cursor-pointer'),
]


def patch(src: str) -> str:
    for old, new in OLD:
        if old in src:
            src = src.replace(old, new, 1)
            print("  diterapkan:", old[:65])
        else:
            print("  PERINGATAN tidak ditemukan:", old[:65])
    return src


if __name__ == "__main__":
    import sys
    path = sys.argv[1]
    s = open(path, encoding="utf-8").read()
    open(path, "w", encoding="utf-8").write(patch(s))
