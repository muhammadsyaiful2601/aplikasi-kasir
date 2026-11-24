p = r"D:\bongkar kode\PROJECT_BASE\DOKUMENTASI\apply_saas_layout.py"
s = open(p, encoding="utf-8").read()

# Tambahkan menu Pengaturan (ke halaman Tb / Lainnya) di sidebar
old = '{id:"backup",label:"Backup Data",icon:gh}];const o='
new = '{id:"backup",label:"Backup Data",icon:gh},{id:"lainnya",label:"Pengaturan",icon:Vg}];const o='
if old in s:
    s = s.replace(old, new, 1)
    print("Menu Pengaturan ditambahkan ke sidebar")
else:
    print("PERINGATAN: marker sidebar tidak ditemukan")

# Mobile nav: tampilkan 5 menu utama termasuk Pengaturan
old2 = 'children:i.slice(0,5).map(a=>{const l=a.icon'
new2 = 'children:i.filter(x=>["beranda","servis","kasir","stok","lainnya"].includes(x.id)).map(a=>{const l=a.icon'
if old2 in s:
    s = s.replace(old2, new2, 1)
    print("Mobile nav disesuaikan")
else:
    print("PERINGATAN: marker mobile nav tidak ditemukan")

open(p, "w", encoding="utf-8").write(s)
