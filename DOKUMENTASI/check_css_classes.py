import importlib.util, re, os

spec = importlib.util.spec_from_file_location("lp", r"D:\bongkar kode\PROJECT_BASE\DOKUMENTASI\apply_layout_patch.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

css = open(r"D:\bongkar kode\PROJECT_BASE\app\assets\main-Bc5OOWNf.css", encoding="utf-8").read()

classes = set()
for attr in [m.NEW_NAV, m.NEW_DASH]:
    for mm in re.finditer(r'className:"([^"]*)"', attr):
        for tok in mm.group(1).split():
            classes.add(tok)
    # template literals with ${...}
    for mm in re.finditer(r'className:`([^`]*)`', attr):
        s = mm.group(1)
        s = re.sub(r'\$\{[^}]*\}', ' ', s)
        for tok in s.split():
            classes.add(tok)

def escape(s):
    return s.replace('\\', '\\\\').replace('[', '\\[').replace(']', '\\]').replace('/', '\\/').replace(':', '\\:').replace('.', '\\.').replace('(', '\\(').replace(')', '\\)').replace('#', '\\#').replace('%', '\\%')

missing = []
for c in sorted(classes):
    if len(c) < 2: continue
    if escape(c) not in css and c not in css:
        missing.append(c)

print("Total class:", len(classes))
print("Missing:", len(missing))
for c in missing:
    print(" ", c)
