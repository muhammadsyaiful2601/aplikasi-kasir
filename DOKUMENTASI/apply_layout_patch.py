"""Rombak layout: Top Navigation Bar + dashboard Split Workspace."""

import re

PATH = r"D:\bongkar kode\PROJECT_BASE\app\assets\main-DbOgN5j6.js"


def extract(src: str, name: str) -> str:
    i = src.find(name)
    if i < 0:
        raise SystemExit("Marker tidak ditemukan: " + name)
    arrow = src.find("=>{", i)
    j = src.find("{", arrow)
    depth = 0
    k = j
    quote = None
    esc = False
    while k < len(src):
        c = src[k]
        if quote:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == quote:
                quote = None
            k += 1
            continue
        if c in ('"', "'", "`"):
            quote = c
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return src[i:k + 1]
        k += 1
    raise SystemExit("Tidak ada penutup: " + name)


NEW_NAV = r'''Jg=({currentTab:e,onChangeTab:t,serviceBadgeCount:s=0})=>{const r=[{id:"beranda",label:"Dashboard",icon:Bg},{id:"servis",label:"Servis",icon:_a,badge:s},{id:"kasir",label:"Kasir POS",icon:Yc},{id:"stok",label:"Stok",icon:yn},{id:"laporan",label:"Laporan",icon:Ig},{id:"lainnya",label:"Lainnya",icon:yh}];return n.jsxs("header",{className:"sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-slate-200 shadow-sm",children:[n.jsxs("div",{className:"max-w-[1400px] mx-auto px-4 h-14 flex items-center gap-3",children:[n.jsxs("div",{onClick:()=>t("beranda"),className:"flex items-center gap-2 shrink-0 cursor-pointer",title:"Dashboard",children:[n.jsx("img",{src:"/logo.png",alt:"Logo Kasir Servis",className:"w-8 h-8 object-contain"}),n.jsx("span",{className:"font-extrabold text-sm text-slate-800 hidden md:block tracking-tight",children:"Kasir Servis"})]}),n.jsxs("nav",{className:"flex items-center gap-1 flex-1 overflow-x-auto",children:r.map(a=>{const i=a.icon,o=e===a.id;return n.jsxs("button",{key:a.id,onClick:()=>t(a.id),className:`relative flex items-center gap-1.5 px-3 py-2 rounded-lg text-xs font-semibold whitespace-nowrap transition-colors ${o?"bg-blue-600 text-white shadow-sm":"text-slate-500 hover:bg-slate-100 hover:text-slate-700"}`,children:[n.jsx(i,{className:"w-4 h-4"}),a.label,!!(a.badge&&a.badge>0)&&n.jsx("span",{className:"bg-rose-500 text-white text-[9px] font-bold px-1.5 rounded-full leading-4",children:a.badge})]})})}),n.jsxs("div",{className:"flex items-center gap-2 shrink-0",children:[n.jsxs("span",{className:"hidden lg:inline-flex items-center gap-1 text-[10px] font-bold text-blue-700 bg-blue-50 px-2.5 py-1 rounded-full",children:[n.jsx(Qg,{className:"w-3 h-3"}),"Offline"]}),n.jsx("button",{className:"w-8 h-8 rounded-full bg-slate-50 border border-slate-200 flex items-center justify-center text-slate-600 hover:bg-slate-100 relative",children:[n.jsx(Rg,{className:"w-4 h-4"}),n.jsx("span",{className:"absolute top-1 right-1 w-2 h-2 bg-rose-500 rounded-full"})]}),n.jsx("div",{className:"w-8 h-8 rounded-full bg-emerald-600 text-white flex items-center justify-center text-[11px] font-bold",title:"Profil Pengguna",children:"KS"})]})]})]})}'''


NEW_DASH = r'''hb=({serviceRepo:e,productRepo:t,salesRepo:s,financeRepo:r,onNavigateTab:a,onNewService:i,onSelectService:o,refreshTrigger:d})=>{const[u,m]=v.useState(""),[b,g]=v.useState([]),[k,_]=v.useState([]),[E,M]=v.useState([]),[z,N]=v.useState([]),[f,y]=v.useState(0),F=async()=>{try{const O=await e.getAll(),x=O.filter(W=>!["SELESAI","SUDAH_DIAMBIL","DIBATALKAN","TIDAK_DAPAT_DIPERBAIKI"].includes(W.status)),R=O.filter(W=>W.status==="SELESAI"),K=await t.getLowStock(),Z=new Date;Z.setHours(0,0,0,0);const ee=await r.getSummary({start:Z.toISOString(),end:new Date().toISOString(),label:"Hari Ini"});g(O),_(x),M(R),N(K),y(ee.totalCashIn)}catch(O){console.error("Error loading dashboard data:",O)}};v.useEffect(()=>{F()},[d]),v.useEffect(()=>{if(u.trim())return Ht(()=>(m(""),!0))},[u]);const D=b.filter(O=>{if(!u.trim())return!1;const x=u.toLowerCase().trim();return O.order_number&&O.order_number.toLowerCase().includes(x)||O.id&&O.id.toLowerCase().includes(x)||O.customer_name&&O.customer_name.toLowerCase().includes(x)||O.customer_phone&&O.customer_phone.includes(x)||O.device_imei&&O.device_imei.toLowerCase().includes(x)||O.device_brand&&O.device_brand.toLowerCase().includes(x)||O.device_model&&O.device_model.toLowerCase().includes(x)||O.customer_complaint&&O.customer_complaint.toLowerCase().includes(x)}),L=k.slice(0,4),B=k.filter(O=>!["DITERIMA","SELESAI","SUDAH_DIAMBIL","DIBATALKAN","TIDAK_DAPAT_DIPERBAIKI"].includes(O.status)).length;return n.jsxs("div",{className:"space-y-4 pb-8 max-w-[1400px] mx-auto px-4 pt-4 select-none",children:[n.jsxs("div",{className:"flex flex-col sm:flex-row gap-3 sm:items-center",children:[n.jsxs("div",{className:"relative flex-1",children:[n.jsx("input",{type:"text",value:u,onChange:O=>m(O.target.value),placeholder:"Cari nomor nota, nama pelanggan, tipe HP, atau IMEI...",className:"w-full text-xs pl-9 pr-9 py-2.5 bg-white border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:outline-hidden shadow-xs text-slate-800 placeholder-slate-400"}),n.jsx(cr,{className:"w-4 h-4 text-slate-400 absolute left-3 top-2.5 pointer-events-none"}),u&&n.jsx("button",{onClick:()=>m(""),className:"absolute right-3 top-2.5 p-0.5 rounded-full text-slate-400 hover:bg-slate-100",children:n.jsx(zi,{className:"w-4 h-4"})})]}),n.jsxs("button",{onClick:i,className:"inline-flex items-center justify-center gap-2 px-4 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs rounded-xl shadow-sm transition-colors shrink-0",children:[n.jsx($t,{className:"w-4 h-4 stroke-[2.5]"}),"Tambah Servis Baru"]})]}),u.trim()?n.jsxs("div",{className:"bg-white rounded-xl border border-blue-200 shadow-sm p-4 space-y-3",children:[n.jsxs("div",{className:"flex items-center justify-between border-b border-slate-100 pb-2.5",children:[n.jsxs("div",{className:"text-xs font-bold text-slate-800 flex items-center gap-2",children:[n.jsx("span",{className:"w-2.5 h-2.5 rounded-full bg-blue-600 animate-pulse"}),n.jsxs("span",{children:["Hasil Pencarian (",D.length,")"]})]}),n.jsx("button",{onClick:()=>m(""),className:"text-[11px] font-semibold text-blue-600 hover:text-blue-700 bg-blue-50 px-2.5 py-1 rounded-full",children:"Tutup"})]}),D.length===0?n.jsxs("div",{className:"py-8 text-center text-slate-400 space-y-2",children:[n.jsx(cr,{className:"w-8 h-8 mx-auto text-slate-300 stroke-[1.5]"}),n.jsxs("p",{className:"text-xs font-semibold text-slate-700",children:['Tidak ada servis cocok dengan "',u,'"']})]}):n.jsx("div",{className:"space-y-2 max-h-[420px] overflow-y-auto",children:D.map(O=>{const x=xa(O.status);return n.jsxs("div",{onClick:()=>{o(O),m("")},className:"p-3 rounded-xl border border-slate-100 bg-slate-50/60 hover:bg-blue-50 cursor-pointer flex items-center justify-between",children:[n.jsxs("div",{className:"min-w-0",children:[n.jsxs("div",{className:"flex items-center gap-1.5",children:[n.jsx("span",{className:"font-mono text-[10px] font-bold text-blue-700 bg-blue-50 px-1.5 py-0.5 rounded",children:O.order_number}),n.jsx("span",{className:"font-bold text-xs text-slate-900 truncate",children:O.customer_name||"Pelanggan"})]}),n.jsxs("p",{className:"text-[11px] text-slate-500 truncate",children:[O.device_brand," ",O.device_model]})]}),n.jsx("span",{className:`text-[10px] px-2 py-0.5 rounded-full font-bold border ${x.bg} ${x.text} ${x.border}`,children:vn(O.status)})]},O.id)})})]}):n.jsxs(n.Fragment,{children:[n.jsxs("div",{className:"grid grid-cols-2 lg:grid-cols-4 gap-3",children:[n.jsxs("div",{onClick:()=>a("servis"),className:"bg-white p-3.5 rounded-xl border border-slate-200 shadow-xs cursor-pointer hover:border-blue-300 transition-colors",children:[n.jsxs("div",{className:"flex items-center justify-between text-slate-500 mb-1",children:[n.jsx("span",{className:"text-[11px] font-semibold",children:"Antrean Servis"}),n.jsx(Xc,{className:"w-4 h-4 text-blue-500"})]}),n.jsxs("div",{className:"text-xl font-bold text-slate-800",children:[k.length," Unit"]})]}),n.jsxs("div",{onClick:()=>a("servis"),className:"bg-white p-3.5 rounded-xl border border-slate-200 shadow-xs cursor-pointer hover:border-blue-300 transition-colors",children:[n.jsxs("div",{className:"flex items-center justify-between text-slate-500 mb-1",children:[n.jsx("span",{className:"text-[11px] font-semibold",children:"Diproses"}),n.jsx(_a,{className:"w-4 h-4 text-amber-500"})]}),n.jsxs("div",{className:"text-xl font-bold text-amber-600",children:[B," Unit"]})]}),n.jsxs("div",{onClick:()=>a("servis"),className:"bg-white p-3.5 rounded-xl border border-slate-200 shadow-xs cursor-pointer hover:border-emerald-300 transition-colors",children:[n.jsxs("div",{className:"flex items-center justify-between text-slate-500 mb-1",children:[n.jsx("span",{className:"text-[11px] font-semibold",children:"Siap Diambil"}),n.jsx(or,{className:"w-4 h-4 text-emerald-500"})]}),n.jsxs("div",{className:"text-xl font-bold text-emerald-600",children:[E.length," Unit"]})]}),n.jsxs("div",{onClick:()=>a("laporan"),className:"bg-white p-3.5 rounded-xl border border-slate-200 shadow-xs cursor-pointer hover:border-blue-300 transition-colors",children:[n.jsxs("div",{className:"flex items-center justify-between text-slate-500 mb-1",children:[n.jsx("span",{className:"text-[11px] font-semibold",children:"Kas Hari Ini"}),n.jsx(Ig,{className:"w-4 h-4 text-blue-500"})]}),n.jsx("div",{className:"text-sm font-bold text-slate-800 truncate",children:$(f)})]})]}),n.jsxs("div",{className:"grid grid-cols-1 lg:grid-cols-10 gap-4",children:[n.jsxs("div",{className:"lg:col-span-7 space-y-3",children:[n.jsxs("div",{className:"flex items-center justify-between",children:[n.jsx("h3",{className:"font-bold text-sm text-slate-800",children:"Servis Aktif Terbaru"}),n.jsxs("button",{onClick:()=>a("servis"),className:"text-xs font-semibold text-blue-600 hover:text-blue-700 flex items-center",children:["Lihat Semua ",n.jsx(Jo,{className:"w-3.5 h-3.5 ml-0.5"})]})]}),L.length===0?n.jsxs("div",{className:"bg-white rounded-xl border border-slate-200 shadow-xs p-8 text-center text-slate-400 space-y-2",children:[n.jsx(gs,{className:"w-8 h-8 text-slate-300 mx-auto"}),n.jsx("p",{className:"text-xs",children:"Tidak ada unit servis yang sedang berjalan saat ini."})]}):n.jsx("div",{className:"space-y-2",children:L.map(O=>{const x=xa(O.status);return n.jsxs("div",{onClick:()=>o(O),className:"bg-white rounded-xl border border-slate-200 shadow-xs p-3.5 flex items-center justify-between hover:border-blue-300 cursor-pointer transition-colors",children:[n.jsxs("div",{className:"flex items-center gap-3 min-w-0",children:[n.jsx("div",{className:"w-10 h-10 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center shrink-0",children:n.jsx(gs,{className:"w-5 h-5"})}),n.jsxs("div",{className:"min-w-0",children:[n.jsxs("h4",{className:"font-bold text-xs text-slate-900 truncate",children:[O.device_brand," ",O.device_model," — ",O.customer_name]}),n.jsxs("p",{className:"text-[11px] text-slate-500 truncate",children:["Estimasi: ",$(O.grand_total||O.estimated_cost)]})]})]}),n.jsxs("div",{className:"flex items-center gap-2 shrink-0",children:[n.jsx("span",{className:`text-[10px] px-2 py-0.5 rounded-full font-bold border ${x.bg} ${x.text} ${x.border}`,children:vn(O.status)}),n.jsx("button",{onClick:R=>{R.stopPropagation(),o(O)},className:"text-[11px] font-semibold text-blue-600 hover:bg-blue-50 px-2 py-1 rounded-lg",children:"Lihat Detail"})]})]},O.id)})})]}),n.jsxs("div",{className:"lg:col-span-3 space-y-3",children:[n.jsx("h3",{className:"font-bold text-sm text-slate-800",children:"Fitur & Utilitas"}),n.jsxs("div",{className:"bg-white rounded-xl border border-slate-200 shadow-xs p-2 space-y-1",children:[n.jsxs("button",{onClick:()=>a("servis"),className:"w-full flex items-center gap-3 p-2.5 rounded-lg hover:bg-slate-50 text-left transition-colors",children:[n.jsx("span",{className:"w-8 h-8 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center shrink-0",children:n.jsx(Wi,{className:"w-4 h-4"})}),n.jsxs("span",{children:[n.jsx("span",{className:"block text-xs font-semibold text-slate-800",children:"Cetak Nota"}),n.jsx("span",{className:"block text-[10px] text-slate-400",children:"Struk & faktur A4"})]})]}),n.jsxs("button",{onClick:()=>a("lainnya"),className:"w-full flex items-center gap-3 p-2.5 rounded-lg hover:bg-slate-50 text-left transition-colors",children:[n.jsx("span",{className:"w-8 h-8 rounded-lg bg-purple-50 text-purple-600 flex items-center justify-center shrink-0",children:n.jsx(Ys,{className:"w-4 h-4"})}),n.jsxs("span",{children:[n.jsx("span",{className:"block text-xs font-semibold text-slate-800",children:"Garansi"}),n.jsx("span",{className:"block text-[10px] text-slate-400",children:"Klaim & monitor garansi"})]})]}),n.jsxs("button",{onClick:()=>a("lainnya"),className:"w-full flex items-center gap-3 p-2.5 rounded-lg hover:bg-slate-50 text-left transition-colors",children:[n.jsx("span",{className:"w-8 h-8 rounded-lg bg-teal-50 text-teal-600 flex items-center justify-center shrink-0",children:n.jsx(gh,{className:"w-4 h-4"})}),n.jsxs("span",{children:[n.jsx("span",{className:"block text-xs font-semibold text-slate-800",children:"Backup Data"}),n.jsx("span",{className:"block text-[10px] text-slate-400",children:"Cadangkan & pulihkan"})]})]}),n.jsxs("button",{onClick:()=>a("stok"),className:"w-full flex items-center gap-3 p-2.5 rounded-lg hover:bg-slate-50 text-left transition-colors",children:[n.jsx("span",{className:"w-8 h-8 rounded-lg bg-sky-50 text-sky-600 flex items-center justify-center shrink-0",children:n.jsx(yn,{className:"w-4 h-4"})}),n.jsxs("span",{children:[n.jsx("span",{className:"block text-xs font-semibold text-slate-800",children:"Stok Barang"}),n.jsx("span",{className:"block text-[10px] text-slate-400",children:"Katalog & mutasi stok"})]})]})]})]})]})]})]})}'''


def patch(src: str) -> str:
    # ganti navigasi bawah -> top nav
    old_nav = extract(src, "Jg=({currentTab")
    src = src.replace(old_nav, NEW_NAV, 1)
    print("  Top Navigation Bar dipasang")

    # ganti dashboard
    old_dash = extract(src, "hb=({serviceRepo")
    src = src.replace(old_dash, NEW_DASH, 1)
    print("  Dashboard Split Workspace dipasang")

    # hapus header lama (Yg) karena sudah digabung ke top nav
    old_header = 'n.jsx(Yg,{title:S(),settings:_,onOpenSettings:()=>U("lainnya")}),'
    if old_header in src:
        src = src.replace(old_header, "", 1)
        print("  Header lama dihapus")

    # pindahkan top nav sebelum <main> agar sticky di bagian atas sejak awal
    nav_call = 'n.jsx(Jg,{currentTab:M,onChangeTab:w=>U(w),serviceBadgeCount:F})'
    anchor = 'n.jsx(mb,{}),'
    if nav_call in src and anchor in src:
        src = src.replace(',' + nav_call, '', 1)
        src = src.replace(anchor, anchor + nav_call + ',', 1)
        print("  Top Navigation dipindah ke atas main")

    # tambah tab laporan
    marker = 'M==="stok"&&n.jsx(kb,{productRepo:o}),'
    if marker in src and 'M==="laporan"&&n.jsx(Sb,{financeRepo:m})' not in src:
        src = src.replace(marker, marker + 'M==="laporan"&&n.jsx(Sb,{financeRepo:m}),', 1)
        print("  Tab Laporan ditambahkan")

    return src


if __name__ == "__main__":
    s = open(PATH, encoding="utf-8").read()
    out = patch(s)
    open(PATH, "w", encoding="utf-8").write(out)
    print("Ukuran:", len(out))
