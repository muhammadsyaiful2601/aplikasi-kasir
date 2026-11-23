"""Ganti emoji template servis dengan ikon SVG bergaya modern (lucide-like)."""

SVG = "<svg xmlns='http://www.w3.org/2000/svg' width='22' height='22' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'>{body}</svg>"

ICONS = {
    "📱": "<rect x='5' y='2' width='14' height='20' rx='2'/><line x1='12' y1='18' x2='12.01' y2='18'/>",
    "🔋": "<rect x='2' y='7' width='16' height='10' rx='2'/><line x1='22' y1='11' x2='22' y2='13'/>",
    "🔌": "<path d='M12 22v-5'/><path d='M9 8V2'/><path d='M15 8V2'/><path d='M18 8v5a6 6 0 0 1-6 6 6 6 0 0 1-6-6V8z'/>",
    "⚡": "<polygon points='13 2 3 14 12 14 11 22 21 10 12 10 13 2'/>",
    "🔄": "<path d='M21 2v6h-6'/><path d='M3 12a9 9 0 0 1 15-6.7L21 8'/><path d='M3 22v-6h6'/><path d='M21 12a9 9 0 0 1-15 6.7L3 16'/>",
    "🔓": "<rect x='3' y='11' width='18' height='11' rx='2'/><path d='M7 11V7a5 5 0 0 1 9.9-1'/>",
    "🔊": "<polygon points='11 5 6 9 2 9 2 15 6 15 11 19 11 5'/><path d='M15.54 8.46a5 5 0 0 1 0 7.07'/><path d='M19.07 4.93a10 10 0 0 1 0 14.14'/>",
    "📷": "<path d='M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z'/><circle cx='12' cy='13' r='4'/>",
    "💻": "<rect x='2' y='3' width='20' height='14' rx='2'/><line x1='8' y1='21' x2='16' y2='21'/><line x1='12' y1='17' x2='12' y2='21'/>",
    "🧠": "<rect x='4' y='4' width='16' height='16' rx='2'/><rect x='9' y='9' width='6' height='6'/><path d='M9 1v3M15 1v3M9 20v3M15 20v3M20 9h3M20 14h3M1 9h3M1 14h3'/>",
    "❄️": "<path d='M9.59 4.59A2 2 0 1 1 11 8H2m10.59 11.41A2 2 0 1 0 14 16H2m15.73-8.27A2.5 2.5 0 1 1 19.5 12H2'/>",
    "⌨️": "<rect x='2' y='6' width='20' height='12' rx='2'/><path d='M6 10h.01M10 10h.01M14 10h.01M18 10h.01M6 14h.01M10 14h.01M14 14h.01M18 14h.01M8 18h8'/>",
    "🖥️": "<rect x='2' y='3' width='20' height='14' rx='2'/><line x1='8' y1='21' x2='16' y2='21'/><line x1='12' y1='17' x2='12' y2='21'/>",
    "🔧": "<path d='M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z'/>",
    "📄": "<path d='M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z'/><path d='M14 2v6h6'/>",
    "🖨️": "<polyline points='6 9 6 2 18 2 18 9'/><path d='M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2'/><rect x='6' y='14' width='12' height='8'/>",
    "⚠️": "<path d='M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z'/><line x1='12' y1='9' x2='12' y2='13'/><line x1='12' y1='17' x2='12.01' y2='17'/>",
    "🧪": "<path d='M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z'/>",
    "⚙️": "<circle cx='12' cy='12' r='3'/><path d='M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z'/>",
}


def patch(src: str) -> str:
    changed = 0
    for emoji, body in ICONS.items():
        old = 'icon:"' + emoji + '"'
        if old in src:
            src = src.replace(old, 'icon:"' + SVG.format(body=body) + '"')
            changed += src.count(old) if False else 1
    print("  ikon diganti:", changed)

    # Render site 1: modal Atur Tarif
    a = 'n.jsx("span",{className:"text-xl shrink-0",children:R.icon})'
    b = 'n.jsx("span",{className:"flex shrink-0 items-center justify-center text-blue-600",dangerouslySetInnerHTML:{__html:R.icon}})'
    n1 = src.count(a)
    src = src.replace(a, b)
    print("  render site 1:", n1)

    # Render site 2: kartu template
    c = 'n.jsx("span",{className:"text-sm",children:te.icon})'
    d = 'n.jsx("span",{className:"flex shrink-0 items-center justify-center text-blue-600",dangerouslySetInnerHTML:{__html:te.icon}})'
    n2 = src.count(c)
    src = src.replace(c, d)
    print("  render site 2:", n2)

    return src


if __name__ == "__main__":
    import sys
    path = sys.argv[1]
    s = open(path, encoding="utf-8").read()
    out = patch(s)
    open(path, "w", encoding="utf-8").write(out)
    print("Ukuran:", len(out))
