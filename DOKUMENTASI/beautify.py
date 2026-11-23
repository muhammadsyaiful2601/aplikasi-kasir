import re, sys

src = open(r"D:\bongkar kode\app\assets\main-DbOgN5j6.js", encoding="utf-8").read()

out = []
i = 0
n = len(src)
indent = 0
quote = None      # current string quote char: ' " or `
escaped = False
# regex template expressions are left inline; acceptable for readability

while i < n:
    c = src[i]
    if quote:
        out.append(c)
        if escaped:
            escaped = False
        elif c == '\\':
            escaped = True
        elif c == quote:
            quote = None
        i += 1
        continue

    if c in ('"', "'", '`'):
        quote = c
        out.append(c)
        i += 1
        continue

    # comments
    if c == '/' and i + 1 < n and src[i+1] == '/':
        j = src.find('\n', i)
        if j == -1: j = n
        out.append(src[i:j])
        i = j
        continue
    if c == '/' and i + 1 < n and src[i+1] == '*':
        j = src.find('*/', i+2)
        j = n if j == -1 else j+2
        out.append(src[i:j])
        i = j
        continue

    if c == '{':
        out.append(' {\n' + '  ' * (indent+1))
        indent += 1
        i += 1
        continue
    if c == '}':
        indent = max(0, indent-1)
        out.append('\n' + '  ' * indent + '}\n')
        i += 1
        continue
    if c == ';':
        out.append(';\n' + '  ' * indent)
        i += 1
        continue
    if c == '\n':
        out.append('\n' + '  ' * indent)
        i += 1
        continue

    out.append(c)
    i += 1

open(r"D:\bongkar kode\_analysis\main.pretty.js", "w", encoding="utf-8").write(''.join(out))
print("lines:", ''.join(out).count('\n'))
