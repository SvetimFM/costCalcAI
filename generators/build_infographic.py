#!/usr/bin/env python3
"""Builds infographic.html — poster-style multimodal summary of the analysis."""

W, H = 940, 2340
INK, SUB, MUT, GRID = "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
BLUE, BLUE_L, BLUE_D = "#2a78d6", "#9ec5f4", "#104281"
ORANGE, ORANGE_D = "#eb6834", "#c14a17"
GREEN, YELLOW, RED, GRAY = "#0ca30c", "#eda100", "#d03b3b", "#c3c2b7"
SER = "Georgia,'Times New Roman',serif"
SANS = "system-ui,-apple-system,'Segoe UI',sans-serif"
HAND = "'Bradley Hand','Segoe Print','Comic Sans MS',cursive"

s = []
def T(x, y, txt, size=14, fill=INK, w="400", anchor="start", font=SANS, extra=""):
    s.append(f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" '
             f'font-weight="{w}" fill="{fill}" text-anchor="{anchor}" {extra}>{txt}</text>')
def R(x, y, w_, h_, fill, rx=0, extra=""):
    s.append(f'<rect x="{x}" y="{y}" width="{w_}" height="{h_}" fill="{fill}" rx="{rx}" {extra}/>')
def L(x1, y1, x2, y2, stroke=GRID, sw=1, dash=""):
    d = f'stroke-dasharray="{dash}"' if dash else ""
    s.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}" {d}/>')
def header(y, title, caption):
    R(50, y - 15, 17, 17, ORANGE)
    T(78, y, title, 27, INK, "700", font=SER)
    T(52, y + 25, caption, 13.5, MUT)
def hand(x, y, txt, size=21, rot=-3, anchor="start"):
    T(x, y, txt, size, RED, "700", anchor, HAND, f'transform="rotate({rot} {x} {y})"')
def scribble(cx, cy, rx, ry):  # rough hand-drawn ellipse
    s.append(f'<path d="M{cx-rx},{cy} C{cx-rx},{cy-ry*1.25} {cx+rx*0.9},{cy-ry*1.3} {cx+rx},{cy-ry*0.15} '
             f'C{cx+rx*1.08},{cy+ry} {cx-rx*0.8},{cy+ry*1.3} {cx-rx*1.06},{cy+ry*0.25}" '
             f'fill="none" stroke="{RED}" stroke-width="3.2" stroke-linecap="round"/>')
def arrow(x1, y1, x2, y2, bend=30):
    mx, my = (x1 + x2) / 2 + bend, (y1 + y2) / 2
    s.append(f'<path d="M{x1},{y1} Q{mx},{my} {x2},{y2}" fill="none" stroke="{RED}" '
             f'stroke-width="3" stroke-linecap="round" marker-end="url(#ah)"/>')

# defs + bg
s.append(f'<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" '
         f'markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{RED}"/></marker></defs>')
R(0, 0, W, H, "#ffffff")

# ---------- title ----------
R(50, 46, 30, 30, ORANGE)
T(94, 72, "The $200 Frontier Habit", 46, INK, "700", font=SER)
T(52, 106, "One month of measured Claude Code usage — and every other way to buy it · Aug 28, 2026", 15, SUB)

# ---------- B1: waffle ----------
header(172, "What your $200 actually buys", "Each square ≈ $200 of API-equivalent frontier compute · measured total: $14,914 / month")
wx, wy, cell, gap = 52, 222, 34, 7
for i in range(75):
    r, c = divmod(i, 15)
    R(wx + c * (cell + gap), wy + r * (cell + gap), cell, cell,
      ORANGE if i == 0 else BLUE_L, rx=6)
T(700, 278, "$14,914", 42, INK, "700", font=SER)
T(700, 300, "API-equivalent consumed / mo", 12.5, MUT)
T(700, 352, "$200", 34, ORANGE, "700", font=SER)
T(700, 373, "what you actually pay", 12.5, MUT)
T(700, 424, "75×", 38, INK, "700", font=SER)
T(700, 445, "subscription leverage", 12.5, MUT)
scribble(69, 239, 27, 26)
hand(120, 476, "you pay for this one!", 22, -2)
arrow(116, 466, 76, 274, bend=-46)

# ---------- B2: token flow ----------
header(548, "Where 14.69 billion tokens went", "Monthly token flow — the provider-side prompt cache does 96% of the physical work")
sx, sy, sw, sh = 52, 590, 836, 62
w_read = sw * 0.9624; w_write = sw * 0.0348; w_out = 5; w_in = 3
w_read = sw - w_write - w_out - w_in
R(sx, sy, w_read, sh, BLUE, rx=0); R(sx, sy, 8, sh, BLUE)
R(sx + w_read + 1, sy, w_write - 1, sh, ORANGE)
R(sx + w_read + w_write + 1, sy, w_out - 1, sh, GREEN)
R(sx + w_read + w_write + w_out + 1, sy, w_in - 1, sh, INK)
T(sx + 18, sy + 38, "cache reads · 14.14B · 96%", 17, "#ffffff", "700")
xw = sx + w_read + w_write / 2
L(xw, sy + sh, xw - 30, sy + sh + 18, MUT, 1.2)
T(xw - 34, sy + sh + 33, "cache writes · 512M new tokens", 12, SUB, "600", "end")
xo = sx + w_read + w_write + w_out + w_in - 3
L(xo, sy + sh, xo + 12, sy + sh + 38, MUT, 1.2)
T(xo + 16, sy + sh + 53, "output 39.6M · input 1.0M", 12, SUB, "600", "end")
hand(96, 720, "re-served at 90% off — a local box must re-compute these", 18.5, -1)
arrow(80, 708, 116, 660, bend=-14)

# ---------- B3: feasibility ----------
header(772, "Could a desk-side machine even keep up?",
       "Compute-hours one month of your workload needs · measured long-context throughput")
fy0 = 820
rows = [("RTX 5090 · 27B model", 143, GREEN), ("2× RTX 3090 · 27B model", 341, YELLOW),
        ("Mac M5 Ultra 256GB · GLM-Flash", 692, YELLOW), ("DGX Spark 128GB · 120B-class", 731, RED),
        ("Strix Halo 128GB · 120B-class", 1263, RED), ("Mac 512GB · DeepSeek-class", 3817, RED)]
bx, bw = 385, 505; pph = bw / 1400.0
for i, (lab, v, col) in enumerate(rows):
    y = fy0 + i * 47
    T(bx - 10, y + 21, lab, 13.5, INK, "600", "end")
    w_ = min(v, 1400) * pph
    R(bx, y, w_, 30, col, rx=5)
    if v > 1400:
        s.append(f'<path d="M{bx+w_-2},{y} l9,15 l-9,15" fill="#ffffff"/>')
        T(bx + w_ - 18, y + 21, f"{v:,} h →", 15, "#ffffff", "700", "end")
    else:
        T(bx + w_ + 10, y + 21, f"{v:,} h", 15, INK, "700")
x720 = bx + 720 * pph
L(x720, fy0 - 26, x720, fy0 + 6 * 47 - 10, INK, 2, "6 5")
hand(x720 + 22, fy0 - 40, "a month only HAS 720 h!", 20, -2)
ly = fy0 + 6 * 47 + 16
for dx, col, lab in ((0, GREEN, "workable"), (130, YELLOW, "saturated · constant queueing"), (390, RED, "physically impossible")):
    R(bx + dx, ly, 13, 13, col, rx=3); T(bx + dx + 20, ly + 11, lab, 12.5, SUB)

# ---------- B4: monthly bill ----------
header(1188, "The monthly bill, honestly accounted",
       "Amortized hardware + power + labor at $75/h · hardware itself is only $40–191/mo — labor dominates")
base, top = 1610, 1250; scale = (base - top) / 2000.0
bars = [("Any free tier", 0, GRAY, ""), ("RTX 5090 · time = $0", 128, BLUE_L, ""),
        ("Claude Max 20x (you)", 200, ORANGE, ""), ("RTX 5090 · honest labor", 1153, BLUE, ""),
        ("≡ Claude-quality work", 1824, BLUE_D, ""), ("API pay-as-you-go", 14914, ORANGE_D, "")]
for g in (500, 1000, 1500, 2000):
    gy = base - g * scale
    L(90, gy, 870, gy, GRID, 1, "3 5"); T(84, gy + 4, f"${g:,}", 11, MUT, anchor="end")
L(90, base, 870, base, "#b9b8b2", 1.5)
for i, (lab, v, col, note) in enumerate(bars):
    x = 104 + i * 130
    h_ = max(v * scale, 3) if v < 14914 else base - top
    R(x, base - h_, 92, h_, col, rx=6)
    if v == 14914:  # break marks
        s.append(f'<path d="M{x-4},{top+40} l25,-12 l25,12 l25,-12 l25,12 l-100,14 z" fill="#ffffff"/>')
        T(x + 46, base - h_ - 10, "$14,914", 18, INK, "700", "middle")
        hand(x + 46, top - 34, "7× off the chart!", 19, -4, "middle")
    else:
        T(x + 46, base - h_ - 10, f"${v:,}", 17, INK, "700", "middle")
    T(0, 0, lab, 13.5, INK, "600", "end", SANS,
      f'transform="translate({x+52},{base+22}) rotate(-32)"')
scribble(104 + 2 * 130 + 46, base - 200 * scale / 2 - 6, 62, 44)
hand(104 + 2 * 130 + 46, base - 112, "your plan!", 21, -4, "middle")

# ---------- B5: quality trade ----------
q_y = 1868
header(q_y, "The quality you'd trade away", "Artificial Analysis Intelligence Index · independent, same harness for open &amp; closed models")
axy = q_y + 92
def qx(v): return 100 + (v - 40) * (760 / 25.0)
L(100, axy, 860, axy, "#b9b8b2", 1.5)
for t in range(40, 66, 5):
    L(qx(t), axy - 4, qx(t), axy + 4, "#b9b8b2", 1.5); T(qx(t), axy + 20, str(t), 11.5, MUT, anchor="middle")
pts = [(63, BLUE, 11, "Opus 5 — your daily driver", -14), (62, BLUE, 8, "Fable 5", 30),
       (53, ORANGE, 9, "256GB Mac · quantized", -14), (52, ORANGE, 9, "128GB box", 30),
       (48, ORANGE, 9, "32GB GPU · only workable class", -30)]
for v, col, r_, lab, dy in pts:
    s.append(f'<circle cx="{qx(v):.0f}" cy="{axy}" r="{r_}" fill="{col}" stroke="#ffffff" stroke-width="2"/>')
    anch = "middle"
    T(qx(v), axy + dy + (4 if dy > 0 else 0), lab, 12, SUB, "600", anch)
by = axy + 52
s.append(f'<path d="M{qx(53):.0f},{by} L{qx(53):.0f},{by+8} L{qx(63):.0f},{by+8} L{qx(63):.0f},{by}" '
         f'fill="none" stroke="{RED}" stroke-width="2.6" stroke-linecap="round"/>')
hand((qx(53) + qx(63)) / 2, by + 34, "the gap you can actually buy: −10 to −15 pts", 19, -1, "middle")

# ---------- B6: when local wins ----------
w_y = 2088
header(w_y, "When local genuinely wins", "The three honest cases — none of them is a cost win over your subscription")
cards = [("\U0001F512", "Air-gap / compliance", "cloud not an option · +$950–1,650/mo"),
         ("\U0001F50C", "Locked out of subscriptions", "vs $14.9k/mo API rates, local wins 10×+"),
         ("\U0001F6E0️", "Hobby scale, time = $0", "$86–128/mo · ~25% quality cut")]
for i, (ico, t1, t2) in enumerate(cards):
    cx0 = 52 + i * 288
    R(cx0, w_y + 34, 272, 104, "#f6f5f2", rx=12)
    T(cx0 + 20, w_y + 78, ico, 30)
    T(cx0 + 20, w_y + 108, t1, 14.5, INK, "700")
    T(cx0 + 20, w_y + 127, t2, 11.5, SUB)

T(W / 2, 2290, "Measured from this machine's Claude Code transcripts · Jul 29 – Aug 28, 2026 · prices &amp; benchmarks verified Aug 28, 2026 · methodology in companion report", 11, MUT, anchor="middle")

svg = f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;display:block">' + "".join(s) + "</svg>"
page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The $200 Frontier Habit — Infographic</title>
<style>body{{margin:0;background:#eceae5;display:flex;justify-content:center;padding:26px 10px}}
.poster{{max-width:960px;width:100%;background:#fff;border-radius:8px;
box-shadow:0 10px 40px rgba(0,0,0,.14)}}</style></head>
<body><div class="poster">{svg}</div></body></html>"""
open("infographic.html", "w").write(page)
print(f"infographic.html written: {len(page):,} bytes")
