import sys

path = r"D:\bongkar kode\PROJECT_BASE\app\assets\main-DbOgN5j6.js"
src = open(path, encoding="utf-8").read()

def extract(start_marker):
    i = src.find(start_marker)
    if i < 0:
        print("MARKER NOT FOUND:", start_marker)
        return
    # find first '{' of class body
    j = src.find("{", i)
    depth = 0
    k = j
    quote = None
    escaped = False
    while k < len(src):
        c = src[k]
        if quote:
            if escaped:
                escaped = False
            elif c == "\\":
                escaped = True
            elif c == quote:
                quote = None
            k += 1
            continue
        if c in ('"', "'", "`"):
            quote = c
            k += 1
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return src[i:k+1]
        k += 1
    print("UNCLOSED", start_marker)

for marker in sys.argv[1:]:
    out = extract(marker)
    if out:
        print("=====", marker, "len", len(out))
        print(out)
        print()
