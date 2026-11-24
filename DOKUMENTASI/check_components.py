import importlib.util, os
spec = importlib.util.spec_from_file_location("lp", r"D:\bongkar kode\PROJECT_BASE\DOKUMENTASI\apply_layout_patch.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
for name in ["NEW_NAV", "NEW_DASH"]:
    code = "const X=" + getattr(m, name) + ";\n"
    p = os.path.join(r"D:\bongkar kode\PROJECT_BASE\DOKUMENTASI", "_check_" + name + ".js")
    open(p, "w", encoding="utf-8").write(code)
    print(name, "->", p, "len", len(code))
