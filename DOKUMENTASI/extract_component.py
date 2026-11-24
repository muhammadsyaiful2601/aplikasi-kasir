import sys

p = r"D:\bongkar kode\PROJECT_BASE\app\assets\main-DbOgN5j6.js"
s = open(p, encoding="utf-8").read()
name = sys.argv[1]
i = s.find(name)
if i < 0:
    raise SystemExit("tidak ditemukan: " + name)

arrow = s.find("=>{", i)
if arrow < 0:
    arrow = s.find("=>", i)
j = s.find("{", arrow)
depth = 0
k = j
quote = None
esc = False
while k < len(s):
    c = s[k]
    if quote:
        if esc: esc = False
        elif c == "\\": esc = True
        elif c == quote: quote = None
        k += 1
        continue
    if c in ('"', "'", "`"):
        quote = c
    elif c == "{": depth += 1
    elif c == "}":
        depth -= 1
        if depth == 0: break
    k += 1
out = s[i:k+1]
print("PANJANG:", len(out))
print(out)
