import importlib.util, re
p = r"D:\bongkar kode\PROJECT_BASE\DOKUMENTASI\apply_saas_layout.py"
spec = importlib.util.spec_from_file_location("saas", p)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
css = open(r"D:\bongkar kode\PROJECT_BASE\app\assets\main-Bc5OOWNf.css", encoding="utf-8").read()
extra = open(r"D:\bongkar kode\PROJECT_BASE\app\assets\layout-extra.css", encoding="utf-8").read()
allcss = css + extra

classes = set()
for attr in [m.NEW_SIDEBAR, m.NEW_DASH]:
    for mm in re.finditer(r'className:"([^"]*)"', attr):
        for t in mm.group(1).split(): classes.add(t)
    for mm in re.finditer(r'className:`([^`]*)`', attr):
        s = re.sub(r'\$\{[^}]*\}', ' ', mm.group(1))
        for t in s.split(): classes.add(t)

def esc(s):
    return s.replace('\\','\\\\').replace('[','\\[').replace(']','\\]').replace('/','\\/').replace(':','\\:').replace('.','\\.').replace('(','\\(').replace(')','\\)').replace('#','\\#')

missing = [c for c in sorted(classes) if len(c) > 1 and esc(c) not in allcss and c not in allcss]
print("Total:", len(classes), "Missing:", len(missing))
for c in missing: print(" ", c)
