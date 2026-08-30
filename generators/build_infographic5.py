#!/usr/bin/env python3
"""Infographic v6 — one A3 sheet (990x1400, 1:sqrt2). Three charts carry the
whole argument; the methodology (fixed cost amortized vs no fixed cost) is
itself the opening chart. Text budget: title, verdict, three claim lines,
footer. Everything else is in-chart annotation."""

import base64, math

W, H = 990, 1400
PAPER = "#fffdf8"
INK, SUB, MUT = "#1a1713", "#57534b", "#8a867d"
RULE, FAINT, WAF = "#ddd9d0", "#c9c5bc", "#dedad1"
BLUE, RED = "#3d6f9e", "#b23a25"
EBG = "'EB Garamond',Georgia,'Times New Roman',serif"
ML, MR = 56, 934

s = []
def T(x, y, txt, size=14, fill=INK, w="400", anchor="start", extra="", it=False):
    ital = 'font-style="italic" ' if it else ""
    s.append(f'<text x="{x}" y="{y}" font-family="{EBG}" font-size="{size}" '
             f'font-weight="{w}" fill="{fill}" text-anchor="{anchor}" {ital}{extra}>{txt}</text>')
def Trot(x, y, txt, ang, size=11, fill=INK, w="400", anchor="middle", it=True, hl=True):
    ex = (halo() + " " if hl else "") + f'transform="rotate({ang:.2f} {x:.1f} {y:.1f})"'
    T(x, y, txt, size, fill, w, anchor, extra=ex, it=it)
def L(x1, y1, x2, y2, stroke=RULE, sw=1, dash=""):
    d = f'stroke-dasharray="{dash}"' if dash else ""
    s.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}" {d}/>')
def R(x, y, w_, h_, fill, rx=0, extra=""):
    s.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w_:.1f}" height="{h_:.1f}" fill="{fill}" rx="{rx}" {extra}/>')
def dot(cx, cy, r_, fill, open_=False):
    if open_:
        s.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r_}" fill="{PAPER}" stroke="{INK}" stroke-width="1.3"/>')
    else:
        s.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r_}" fill="{fill}"/>')
def halo(wd=3):
    return f'paint-order="stroke" stroke="{PAPER}" stroke-width="{wd}"'
def claim(y, txt):
    T(ML, y, txt, 17, INK, "600")

R(0, 0, W, H, PAPER)

# ================= masthead =================
T(ML, 40, "A COST INVESTIGATION · SIX DESK RIGS · FOUR CLOUD PLANS · ONE METERED MONTH", 10, MUT, "600", extra='letter-spacing="2.6"')
T(MR, 40, "SET AS ONE A3 SHEET · 1 : √2", 10, MUT, "600", "end", extra='letter-spacing="2"')
T(ML, 86, "The Real Price of Local AI", 42, INK, "600")
T(ML, 112, "Once your time has a price, a $200 plan buys about ten times more quality per dollar than any desk rig. Local wins on privacy and control — not on cost.", 13.5, INK, it=True)
L(ML, 128, MR, 128, RULE, 1)

# ================= I. the arithmetic =================
claim(160, "I · The arithmetic — a rig is a down payment amortized; a plan is a slope from zero")

gx0, gx1 = 120, 640
gy1, gy0 = 200, 505
def mx(m): return gx0 + m * (gx1 - gx0) / 36.0
def gy(v): return gy0 - v * (gy0 - gy1) / 7500.0

T(104, 192, "cumulative dollars, three years of ownership — cheapest rig shown (2× used RTX 3090); every other rig starts higher", 10, MUT, it=True)

# frames + ticks
L(104, gy1, 104, gy0, FAINT, 1.2)
for v_, lab in ((0, "$0"), (2500, "$2,500"), (5000, "$5,000"), (7500, "$7,500")):
    L(100, gy(v_), 108, gy(v_), MUT, 1.2)
    T(94, gy(v_) + 4, lab, 10, MUT, anchor="end")
L(100, gy(2900), 108, gy(2900), FAINT, 1)
T(94, gy(2900) + 3, "$2,900", 9, MUT, anchor="end", it=True)
L(gx0, gy0, gx1, gy0, FAINT, 1.2)
for m_ in (0, 12, 24, 36):
    L(mx(m_), gy0, mx(m_), gy0 + 5, MUT, 1.2)
    T(mx(m_), gy0 + 16, "36 mo" if m_ == 36 else str(m_), 10, MUT, anchor="middle")

# $20 plan
L(mx(0), gy(0), mx(36), gy(720), BLUE, 1, extra_dummy := "")
s[-1] = s[-1].replace('stroke-width="1" ', 'stroke-width="1" opacity="0.55" ')
T(310, 482, "the $20 plan — the rig’s power bill alone outruns it", 10, SUB, it=True, extra=halo())
T(644, gy(720) + 3, "$720", 9, BLUE, extra='opacity="0.7"')

# $200 plan
L(mx(0), gy(0), mx(36), gy(7200), BLUE, 2)
ang_b = math.degrees(math.atan2(gy(7200) - gy(0), mx(36) - mx(0)))
Trot(468.5, 296.0, "the $200 plan — $0 down, $200 a month", ang_b, 11, BLUE, "600")
T(644, gy(7200) + 3, "$7,200", 10, BLUE, "600")

# amortized dashed
L(mx(0), gy(0), mx(36), gy(3096), MUT, 1.2, "5 4")
T(636, 404, "net of resale at month 36: ≈$86/mo — the slope chart II prices", 10, SUB, "400", "end", extra=halo(), it=True)
T(644, gy(3096) + 3, "$3,096", 9, MUT)

# rig, hours free: step + power slope
L(121, gy(0), 121, gy(2900), INK, 2)
T(128, 400, "the box: $2,900, day one", 10.5, INK, it=True, extra=halo())
L(mx(0), gy(2900), mx(36), gy(4124), INK, 1.6)
ang_h = math.degrees(math.atan2(gy(4124) - gy(2900), mx(36) - mx(0)))
Trot(494.7, 342.2, "then power only — $34 a month", ang_h, 10.5, INK)
T(644, gy(4124) + 3, "$4,124", 10, INK)

# breakeven
bx, by = mx(2900 / 166.0), gy(200 * 2900 / 166.0)
dot(bx, by, 3.4, PAPER, open_=True)
L(bx, gy0, bx, gy0 + 5, INK, 1.2)
T(bx, gy0 + 28, "breakeven — month 17, and only at $0/h", 9.5, INK, "600", "middle", it=True)

# rig, hours at $75
rx1 = mx((7500 - 2900) / 1059.0)
L(mx(0), gy(2900), rx1, gy1, RED, 2)
s.append(f'<path d="M184.9,193.4 L185.5,201.0 L179.9,199.0 Z" fill="{RED}"/>')
T(192, 212, "now count your hours at $75/h:", 11.5, RED, "600", it=True, extra=halo())
T(192, 228, "off this chart in month 5 — $41,024 by month 36", 11.5, RED, "600", it=True, extra=halo())

# ---- right panel: one month, decomposed ----
k2 = 0.2475
cb = gy0
L(700, cb, 932, cb, FAINT, 1.2)
segs = [(0, 40, FAINT), (40, 52, MUT), (52, 86, SUB), (86, 1111, RED)]
for lo_, hi_, col in segs:
    R(700, cb - hi_ * k2, 52, (hi_ - lo_) * k2, col)
for b_ in (40, 52, 86):
    L(700, cb - b_ * k2, 752, cb - b_ * k2, PAPER, 1)
R(880, cb - 200 * k2, 52, 200 * k2, BLUE)
T(760, 350, "your hours — $1,025", 11.5, RED, "600")
T(760, 365, "13.7 h/mo at $75/h:", 9.5, MUT)
T(760, 379, "setup, patches, babysitting", 9.5, MUT)
T(726, 519, "owned — $1,111/mo", 10.5, INK, "600", "middle")
T(932, 519, "rented — $200/mo", 10.5, BLUE, "600", "end")
T(700, 533, "box $40 + capital $12 + power $34 + hours $1,025", 8.5, MUT)
T(700, 547, "hours are 92% of the honest bill", 10, RED, it=True)
T(932, 547, "no box · no hours", 8.5, MUT, anchor="end")
T(906, cb - 200 * k2 - 8, "$200", 11, BLUE, "600", "middle")

# ================= II. the market =================
L(ML, 556, MR, 556, RULE, 1)
claim(588, "II · The market — every plan is cheaper and better than every desk rig")

px0, px1 = 130, 900
py1, py0 = 650, 940
def sx(q): return px0 + (q - 47) * (px1 - px0) / 17.0
def sy(d): return py0 - d * (py0 - py1) / 1500.0

T(MR, 610, "each vertical pair is one rig — hollow: your hours at $0 · filled: at $75/h", 10, MUT, anchor="end")
T(MR, 624, "blue — the four cloud plans", 10, MUT, anchor="end")
T(MR, 638, "the y-axis prices the dashed slope from I", 10, MUT, anchor="end", it=True)

# (name, q_eff, jitter, $lo, $hi, label_row_y, label_anchor, label_x)
rigs = [("2×3090",     48, -12,  86, 1111, 634, "end",    159.3),
        ("RTX 5090",   48,  12, 128, 1153, 618, "middle", 187.3),
        ("Strix Halo", 52, -12,  91, 1116, 634, "end",    340.5),
        ("DGX Spark",  52,  12, 120, 1145, 618, "end",    364.5),
        ("Mac 256GB",  53,   0, 193, 1218, 602, "middle", 401.8),
        ("Mac 512GB",  56,   0, 296, 1321, 618, "middle", 537.6)]
plans = ((0, -6), (20, 3), (100, -2), (200, 5))

ymax = 1321
L(114, sy(ymax), 114, sy(0), FAINT, 1.2)
for d_, lab in ((0, "$0"), (500, "$500"), (1000, "$1,000")):
    L(110, sy(d_), 118, sy(d_), MUT, 1.2)
    T(104, sy(d_) + 4, lab, 10, MUT, anchor="end")
L(110, sy(ymax), 118, sy(ymax), MUT, 1.2)
T(104, sy(ymax) + 4, "$1,321", 9, MUT, anchor="end", it=True)
for _, q, jx, lo, hi, _r, _a, _lx in rigs:
    L(110, sy(lo), 114, sy(lo), FAINT, 0.8)
    L(110, sy(hi), 114, sy(hi), FAINT, 0.8)
ax_y = 952
L(sx(48) - 10, ax_y, sx(63) + 10, ax_y, FAINT, 1.2)
for q_, ink_ in ((48, True), (50, False), (55, False), (60, False), (63, True)):
    L(sx(q_), ax_y, sx(q_), ax_y + 5, MUT, 1.2)
    T(sx(q_), ax_y + 18, str(q_), 10, INK if ink_ else MUT, "600" if ink_ else "400", "middle")
for _, q, jx, lo, hi, _r, _a, _lx in rigs:
    L(sx(q) + jx, ax_y - 3, sx(q) + jx, ax_y, FAINT, 0.8)
L(sx(63), ax_y - 3, sx(63), ax_y, FAINT, 0.8)

# model rug under axis — each rig sits at its model's 4-bit effective score
T(sx(48), 979, "Qwen3.8-27B", 8.5, MUT, anchor="middle", it=True)
T(366, 979, "Qwen-Flash-Next", 8.5, MUT, anchor="end", it=True)
T(398, 979, "GLM-5.3-Flash", 8.5, MUT, anchor="start", it=True)
T(sx(56), 979, "DeepSeek-class", 8.5, MUT, anchor="middle", it=True)
L(sx(60), 977, sx(60), 973, MUT, 1)
L(sx(63), 977, sx(63), 973, MUT, 1)
L(sx(60), 977, sx(63), 977, MUT, 1)
T(MR, 991, "open weights stop at 60, at server sizes — the last three points are cloud-only", 8.5, SUB, anchor="end", it=True)
T(px0, 991, "quality — Artificial Analysis Intelligence Index", 8.5, MUT, it=True)

for name, q, jx, lo, hi, ry, an, lx in rigs:
    x = sx(q) + jx
    L(x, sy(lo) - 5, x, sy(hi) + 5, INK, 0.7)
    L(x, ry + 5, x, sy(hi) - 6, FAINT, 0.7)
for name, q, jx, lo, hi, ry, an, lx in rigs:
    dot(sx(q) + jx, sy(lo), 3.2, PAPER, open_=True)
    dot(sx(q) + jx, sy(hi), 3.2, INK)
    T(sx(q) + jx + 7, sy(lo) + 3.5, f"${lo:,}", 8.5, MUT)
for name, q, jx, lo, hi, ry, an, lx in rigs:
    T(lx, ry, f"{name} — ${hi:,}", 11, INK, "400", an, extra=halo(), it=True)
for d_, jx_ in plans:
    dot(sx(63) + jx_, sy(d_), 3.4, BLUE)

T(560, 772, "more spend moves a rig up, not right", 11, MUT, it=True, extra=halo())
T(930, 840, "the corner you want — all quality 63:", 12, INK, "600", "end", extra=halo(), it=True)
T(930, 856, "free · $20 Pro / Plus · $100 mid tiers · $200 Max / Pro / Ultra", 10, SUB, anchor="end", extra=halo())
T(930, 888, "our metered month: $14,914 — ten times off this chart", 11.5, RED, anchor="end", extra=halo(), it=True)

# ================= III. the stress test =================
L(ML, 1006, MR, 1006, RULE, 1)
claim(1038, "III · The stress test — our metered month, on their silicon")

# waffle
for i in range(75):
    r_, c_ = divmod(i, 15)
    R(ML + c_ * 15, 1058 + r_ * 15, 12, 12, RED if i == 0 else WAF, rx=1)
T(ML, 1160, "$14,914", 24, INK, "600")
T(ML, 1176, "metered, API-equivalent", 8.5, MUT)
T(220, 1160, "$200", 24, RED, "600")
T(220, 1176, "paid — the 75× month", 8.5, MUT)
T(ML, 1200, "Each square is $200 of metered usage — 14.69B tokens,", 9.5, MUT)
T(ML, 1212, "71,350 requests, 96% from cache. The red square is the entire bill.", 9.5, MUT)

# hours strip
T(510, 1058, "hours of nonstop generation the month asks of each rig", 11, INK, "600")
T(510, 1072, "a month holds 720", 9.5, MUT, it=True)
ly = 1102
def fx(h): return 510 + min(h, 1400) * (900 - 510) / 1400.0
L(510, ly, 900, ly, FAINT, 1.5)
L(fx(720), ly - 14, fx(720), ly + 30, INK, 1, "4 3")
for h in (143, 341, 1263):
    T(fx(h) - (3 if h == 1263 else 0), ly - 12, f"{h:,}", 10, SUB, "600", "end" if h == 1263 else "middle")
T(fx(692) - 3, ly - 12, "692", 10, SUB, "600", "end")
T(fx(731) + 3, ly - 12, "731", 10, SUB, "600", "start")
T(900, ly - 12, "3,817", 10, SUB, "600", "end")
for h in (143, 341, 692):
    dot(fx(h), ly, 4.5, PAPER, open_=True)
for h in (731, 1263):
    R(fx(h) - 4.5, ly - 4.5, 9, 9, RED, rx=1)
s.append(f'<path d="M{894},{ly-5.5} l10,5.5 l-10,5.5 z" fill="{RED}"/>')
for nm, h in (("5090", 143), ("2×3090", 341), ("Spark", 731), ("Strix", 1263)):
    T(fx(h), ly + 18, nm, 9, MUT, "600", "middle", extra=halo())
T(fx(692), ly + 30, "Mac 256", 9, MUT, "600", "middle", extra=halo())
T(900, ly + 30, "Mac 512", 9, MUT, "600", "end")
T(fx(720), ly + 44, "720 h", 9.5, INK, "600", "middle", extra=halo(), it=True)
T(510, 1170, "three rigs need more hours than the month holds —", 10, RED, it=True)
T(510, 1182, "at the best quality a desk can hold, 56 of 63", 10, RED, it=True)

# field evidence, drawn
T(ML, 1236, "interventions per task, paired field study:", 9.5, SUB)
for i in range(7):
    dot(250 + i * 11, 1232, 2.8, INK)
T(324, 1236, "local 7", 9.5, INK, "600")
dot(392, 1232, 2.8, BLUE)
T(400, 1236, "Claude 1", 9.5, BLUE, "600")
for i in range(44):
    L(510 + i * 4, 1224, 510 + i * 4, 1233, RED, 1.1)
T(694, 1236, "one error, looped 44 times — the agent never noticed", 9.5, RED, it=True)
T(ML, 1260, "2–7 days to stand one up · 0 working local replacements surfaced for a €440k/yr Claude team asking publicly", 9.5, SUB)
T(MR, 1260, "“A junior next to a senior that thinks” — a Mac Studio owner on Qwen vs Opus, HN, June 2026", 10, INK, anchor="end", it=True)

# ================= verdict + sources =================
L(ML, 1276, MR, 1276, RULE, 1)
T(ML, 1304, "No rig on this sheet could have served our month at frontier quality — three could not have served it at all.", 15, INK, "600")
T(ML, 1324, "Buy the machine for privacy, control, or the love of it. Buy the plan for the work — the meter says the difference is 75×.", 12, INK, it=True)
T(ML, 1350, "Sources — quality: Artificial Analysis Intelligence Index v4.1.1 · plan prices: Anthropic / OpenAI / Google published tiers · hardware: US street &amp; apple.com prices · power: EIA US average · all verified Aug 28 2026", 8.5, MUT)
T(ML, 1362, "demand: our own Claude Code transcripts, Jul 29 – Aug 28 2026 — 14.69B tokens, 71,350 requests, 96% cache-served, deduplicated, priced at published per-MTok rates", 8.5, MUT)
T(ML, 1374, "TCO: 36-month amortization net of resale · 5%/yr capital charge · labor $0 or $75/h — 24h setup, 3h/mo upkeep, per-task tending · builder evidence: paired study Jun 2026, llama.cpp #20198/#27406, HN &amp; r/LocalLLaMA", 8.5, MUT)
T(W / 2, 1392, "costCalcAI · full method, sensitivity &amp; validation in the companion report · August 2026", 9, MUT, anchor="middle")

# ================= pages =================
def b64(fn):
    return base64.b64encode(open(fn, "rb").read()).decode()
svg = f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;display:block">' + "".join(s) + "</svg>"

fontcss = f"""@font-face{{font-family:'EB Garamond';src:url(data:font/woff2;base64,{b64("ebg-normal-400.woff2")}) format('woff2');font-weight:400 600;font-style:normal;font-display:block}}
@font-face{{font-family:'EB Garamond';src:url(data:font/woff2;base64,{b64("ebg-italic-400.woff2")}) format('woff2');font-weight:400 600;font-style:italic;font-display:block}}"""

page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Real Price of Local AI — A3 edition</title>
<style>
{fontcss}
body{{margin:0;background:#eceae5;display:flex;justify-content:center;padding:26px 10px}}
.poster{{max-width:990px;width:100%;background:{PAPER};box-shadow:0 8px 34px rgba(0,0,0,.13)}}
@media print{{body{{background:none;padding:0}}.poster{{box-shadow:none}}@page{{size:A3 portrait;margin:0}}}}
</style></head>
<body><div class="poster">{svg}</div></body></html>"""
open("infographic5.html", "w").write(page)
print(f"infographic5.html written: {len(page):,} bytes")

shot = f"""<!doctype html><html><head><meta charset="utf-8"><style>
{fontcss}
html,body{{margin:0;padding:0}}svg{{display:block}}
</style></head><body>{svg}</body></html>"""
open("infographic5_shot.html", "w").write(shot)
print(f"infographic5_shot.html written: {len(shot):,} bytes")

canvas_page = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Real Price of Local AI — A3 edition</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,600;1,400&display=swap');
body{margin:0;background:#eceae5;display:flex;justify-content:center;padding:26px 10px}
.poster{max-width:990px;width:100%;background:#fffdf8;box-shadow:0 8px 34px rgba(0,0,0,.13)}
</style></head>
<body><div class="poster">""" + svg + "</div></body></html>"
open("infographic5_canvas.html", "w").write(canvas_page)
print(f"infographic5_canvas.html written: {len(canvas_page):,} bytes")
