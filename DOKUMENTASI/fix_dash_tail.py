p = r"D:\bongkar kode\PROJECT_BASE\DOKUMENTASI\apply_layout_patch.py"
s = open(p, encoding="utf-8").read()
marker = "NEW_DASH = r'''"
i = s.find(marker)
j = s.find("'''", i + len(marker))
block = s[i:j]
# blok diakhiri ...]})},  tambahkan satu ]}) sebelum }
k = block.rfind("}")
new_block = block[:k] + "]})" + block[k:]
s = s[:i] + new_block + s[j:]
open(p, "w", encoding="utf-8").write(s)
print("Ditambahkan ]}) sebelum akhir NEW_DASH")
