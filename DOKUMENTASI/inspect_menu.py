p = r"D:\bongkar kode\PROJECT_BASE\app\assets\main-DbOgN5j6.js"
s = open(p, encoding="utf-8").read()
needle = 'id:"backup",title:"Backup & Pemulihan Data"'
i = s.find(needle)
print("index:", i)
print(repr(s[i-1400:i+400]))
