import importlib.util, os
p = r"D:\bongkar kode\PROJECT_BASE\DOKUMENTASI\apply_saas_layout.py"
spec = importlib.util.spec_from_file_location("saas", p)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
base = r"D:\bongkar kode\PROJECT_BASE\DOKUMENTASI"
for name in ["NEW_SIDEBAR", "NEW_DASH"]:
    s = getattr(m, name)
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
    print(name, counts)
    f = os.path.join(base, "_v_" + name + ".js")
    open(f, "w", encoding="utf-8").write("const X=" + s + ";\n")
    print("  ->", f)
