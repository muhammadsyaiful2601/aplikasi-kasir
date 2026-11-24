import importlib.util
spec = importlib.util.spec_from_file_location("lp", r"D:\bongkar kode\PROJECT_BASE\DOKUMENTASI\apply_layout_patch.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
s = m.NEW_DASH
quote = None
esc = False
counts = {c: 0 for c in "()[]{}"}
for c in s:
    if quote:
        if esc: esc = False
        elif c == "\\": esc = True
        elif c == quote: quote = None
        continue
    if c in ('"', "'", "`"):
        quote = c
    elif c in counts:
        counts[c] += 1
print(counts)
print("[ vs ]:", counts['['], counts[']'], "diff", counts['['] - counts[']'])
print("( vs ):", counts['('], counts[')'], "diff", counts['('] - counts[')'])
print("{ vs }:", counts['{'], counts['}'], "diff", counts['{'] - counts['}'])
print("char@1541:", repr(s[1530:1560]))
