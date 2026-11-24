p = r"D:\bongkar kode\PROJECT_BASE\DOKUMENTASI\apply_saas_layout.py"
s = open(p, encoding="utf-8").read()
marker = "NEW_DASH = r'''"
i = s.find(marker)
j = s.find("'''", i + len(marker))
block = s[i:j]
k = block.rfind("}")
s = s[:i] + block[:k] + "]})" + block[k:] + s[j:]
open(p, "w", encoding="utf-8").write(s)
print("Ditambahkan ]}) sebelum akhir NEW_DASH")
