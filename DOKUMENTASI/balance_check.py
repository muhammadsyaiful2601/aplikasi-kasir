import importlib.util

spec = importlib.util.spec_from_file_location("lp", r"D:\bongkar kode\PROJECT_BASE\DOKUMENTASI\apply_layout_patch.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
s = m.NEW_DASH

stack = []
quote = None
esc = False
pairs = {')': '(', ']': '[', '}': '{'}
for i, c in enumerate(s):
    if quote:
        if esc:
            esc = False
        elif c == "\\":
            esc = True
        elif c == quote:
            quote = None
        continue
    if c in ('"', "'", "`"):
        quote = c
        continue
    if c in '([{':
        stack.append((c, i))
    elif c in ')]}':
        if not stack:
            print("EXTRA closing", c, "at", i, repr(s[i-90:i+40]))
            break
        open_c, oi = stack.pop()
        if open_c != pairs[c]:
            print("MISMATCH", open_c, "at", oi, "vs", c, "at", i)
            print(repr(s[oi-100:i+60]))
            break
else:
    if stack:
        print("UNCLOSED:", [(c, i) for c, i in stack[-8:]])
        for c, i in stack[-3:]:
            print(repr(s[i-100:i+80]))
    else:
        print("BALANCED")
