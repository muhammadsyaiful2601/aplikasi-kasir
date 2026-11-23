import sys
src = open(r"D:\bongkar kode\PROJECT_BASE\app\assets\main-DbOgN5j6.js", encoding="utf-8").read()
needle = sys.argv[1]
width = int(sys.argv[2]) if len(sys.argv) > 2 else 600
start = 0
while True:
    i = src.find(needle, start)
    if i < 0: break
    print("---- @", i, "----")
    print(src[max(0,i-width):i+width])
    print()
    start = i + 1
