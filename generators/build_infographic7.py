#!/usr/bin/env python3
"""Infographic v8 — the payback edition. Time is the master axis: a five-year
cumulative-spend race (breakeven crossings drawn as literal future dates), and
below it a true alignment nomograph: wage scale -> rig pivot -> months-to-payback
scale. Works because 1/T is affine in the wage: T = H/(200 - power - 13.7r).
Color semantics unchanged: ink = local, blue = plan, red = violation/penalty.
A3 sheet, 990x1400 (1:sqrt2)."""

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
def Trot(x, y, txt, ang, size=10.5, fill=INK, w="400", anchor="middle", it=True, hl=True):
    ex = (halo() + " " if hl else "") + f'transform="rotate({ang:.2f} {x:.1f} {y:.1f})"'
    T(x, y, txt, size, fill, w, anchor, extra=ex, it=it)
def L(x1, y1, x2, y2, stroke=RULE, sw=1, dash="", op=None):
    d = f'stroke-dasharray="{dash}" ' if dash else ""
    o = f'opacity="{op}" ' if op else ""
    s.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}" {d}{o}/>')
def R(x, y, w_, h_, fill, rx=0, extra=""):
    s.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w_:.1f}" height="{h_:.1f}" fill="{fill}" rx="{rx}" {extra}/>')
def dot(cx, cy, r_, fill, open_=False, stroke=None, sw=1.3):
    if open_:
        st = stroke or INK
        s.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r_}" fill="none" stroke="{st}" stroke-width="{sw}"/>')
    else:
        s.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r_}" fill="{fill}"/>')
def hollow(cx, cy, r_):
    s.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r_}" fill="{PAPER}" stroke="{INK}" stroke-width="1.3"/>')
def halo(wd=3):
    return f'paint-order="stroke" stroke="{PAPER}" stroke-width="{wd}"'
def claim(x, y, txt, size=17):
    T(x, y, txt, size, INK, "600")

R(0, 0, W, H, PAPER)

# ---- data: (name, quality, hardware $, power $/mo, feasible) ----
RIGS = [("2×3090",     48,  2900, 34, True),
        ("Strix Halo", 52,  3650, 15, False),
        ("DGX Spark",  52,  4699, 22, False),
        ("RTX 5090",   48,  8500, 22, True),
        ("Mac 256GB",  53, 10799, 28, True),
        ("Mac 512GB",  56, 17200, 33, False)]
PLAN, HOURS = 200.0, 13.7

# ================= masthead =================
T(ML, 40, "A COST INVESTIGATION · SIX DESK RIGS · THREE WAYS TO BUY TOKENS · FIVE YEARS FORWARD", 10, MUT, "600", extra='letter-spacing="2.6"')
T(MR, 40, "SET AS ONE A3 SHEET · 1 : √2", 10, MUT, "600", "end", extra='letter-spacing="2"')
T(ML, 88, "The Payback Horizon", 42, INK, "600")
T(ML, 112, "A rig is a bet: pay for the box today, and hope enough cheap months follow to beat a $200 plan that starts at zero.", 13, INK, it=True)
T(ML, 128, "Five years out, the bet clears only if your hour is worth less than $13 — for quality the plan beat on day one.", 13, INK, it=True)
L(ML, 142, MR, 142, RULE, 1)

# ================= I. the five-year race (hero) =================
claim(ML, 174, "I · Five years, all-in — a plan is a slope; a rig is a down payment racing to catch it")
T(MR, 198, "ink — the six rigs bought outright: the box on day one, then power only, your hours at $0", 10, MUT, anchor="end")
T(MR, 212, "blue — the plans: $20 · $100 · $200 a month, nothing down · red ring — cannot serve the month", 10, MUT, anchor="end")
T(MR, 226, "red — what breaks the picture: metered API, or your hours priced at $75", 10, RED, anchor="end", it=True)

PX0, PX1 = 130, 900
PY1, PY0 = 254, 770
MONTHS, YMAX = 60.0, 13500.0
def mx(m): return PX0 + m * (PX1 - PX0) / MONTHS
def my(v): return PY0 - v * (PY0 - PY1) / YMAX

# y axis
L(114, PY1, 114, PY0, FAINT, 1.2)
for v_ in (0, 3000, 6000, 9000, 12000):
    L(110, my(v_), 118, my(v_), MUT, 1.2)
    T(104, my(v_) + 4, f"${v_:,}" if v_ else "$0", 10, MUT, anchor="end")
T(104, 240, "cumulative dollars — everything in, from day one", 10, MUT, it=True)
# x axis
L(PX0, PY0, PX1, PY0, FAINT, 1.2)
for m_ in (0, 12, 24, 36, 48, 60):
    L(mx(m_), PY0, mx(m_), PY0 + 5, MUT, 1.2)
    T(mx(m_), 786, str(m_), 10, MUT, anchor="middle")
T(PX1 + 8, 786, "months", 10, MUT)

# plan lines
L(mx(0), my(0), mx(60), my(20 * 60), BLUE, 1, op=0.5)
T(893, 757, "the $20 plan", 9.5, BLUE, anchor="end", it=True, extra=halo())
L(mx(0), my(0), mx(60), my(100 * 60), BLUE, 1.1, op=0.6)
ang100 = math.degrees(math.atan2(my(6000) - my(0), mx(60) - mx(0)))
Trot(600, 621, "the $100 mid tiers", ang100, 9.5, BLUE, "400")
L(mx(0), my(0), mx(60), my(PLAN * 60), BLUE, 2)
ang200 = math.degrees(math.atan2(my(12000) - my(0), mx(60) - mx(0)))
Trot(497, 541, "the $200 plan — nothing down, $200 a month", ang200, 11, BLUE, "600")
dot(mx(0), my(0), 3.4, BLUE)
T(904, my(12000) + 3, "$12,000", 9.5, BLUE, "600")
T(904, my(12479) + 1, "$12,479", 8.5, MUT)

# metered ray
mex = mx(YMAX / 14914.0)
L(mx(0), my(0), mex, PY1, RED, 2)
s.append(f'<path d="M{mex-3.2:.1f},265.5 L{mex:.1f},254.5 L{mex+3.2:.1f},265.5 Z" fill="{RED}"/>')
Trot(156, 512, "the meter — $14,914 a month, gone in 27 days", -88.7, 10.5, RED, "600")

# rig lines (ink), $0/h
ends = {}
for name, q, hw, pw, ok in RIGS:
    if hw > YMAX:
        continue
    y0, y1 = my(hw), my(hw + pw * 60)
    ends[name] = y1
    L(mx(0), y0, mx(60), y1, INK, 1.4)
    dot(mx(0), y0, 3.4, INK)
    if not ok:
        dot(mx(0), y0, 5.8, None, open_=True, stroke=RED, sw=1.3)
T(904, ends["2×3090"] + 3, "$4,940", 8.5, MUT)
T(904, ends["Strix Halo"] + 6, "$4,550", 8.5, MUT)
T(904, ends["RTX 5090"] + 3, "$9,820", 8.5, MUT)

# the $75/h loaded line (cheapest rig)
lx1 = mx((YMAX - 2900) / 1059.0)
L(mx(0), my(2900), lx1, PY1, RED, 1.6)
s.append(f'<path d="M{lx1-3.2:.1f},265.5 L{lx1:.1f},254.5 L{lx1+3.2:.1f},265.5 Z" fill="{RED}"/>')
Trot(206, 462, "hours at $75 — gone by month 9", -72.4, 10, RED, "600")

# rig labels along lines
T(200, 672, "2×3090 · Q48 — $2,900 in", 10.5, INK, it=True, extra=halo())
T(181, 616, "Strix Halo · Q52 — $3,650 in", 10.5, INK, it=True, extra=halo())
T(266, 596, "DGX Spark · Q52 — $4,699 in", 10.5, INK, it=True, extra=halo())
T(361, 422, "RTX 5090 · Q48 — $8,500 in", 10.5, INK, it=True, extra=halo())
T(386, 327, "Mac 256GB · Q53 — $10,799 in", 10.5, INK, it=True, extra=halo())
T(893, my(12479) - 14, "crosses in month 63 →", 9, SUB, anchor="end", it=True, extra=halo())

# Mac 512 annotation (off-chart)
T(310, 268, "Mac 512GB · Q56 enters at $17,200 — a page above this chart;", 10.5, INK, it=True, extra=halo())
T(310, 283, "its crossing waits until month 103, and it cannot serve the month anyway", 9.5, RED, it=True, extra=halo())

# breakeven crossings vs the $200 plan
crossings = []
for name, q, hw, pw, ok in RIGS:
    tm = hw / (PLAN - pw)
    if tm <= 60:
        crossings.append((name, tm, ok))
    print(f"{name:<11} T0={tm:6.1f} mo   end5y=${hw + pw * 60:>6,.0f}")
for name, tm, ok in crossings:
    cxx, cyy = mx(tm), my(PLAN * tm)
    L(cxx, cyy + 5, cxx, PY0 - 2, FAINT, 0.9, "3 3")
    hollow(cxx, cyy, 4)
    lab = f"mo {math.ceil(tm)}" + ("" if ok else "*")
    T(cxx, 764, lab, 9.5, INK if ok else RED, "600", "middle", extra=halo())

# the Spark = $100-plan dead heat at year five
hollow(900, my(6019), 5)
T(893, 522, "year five, a dead heat —", 9.5, SUB, anchor="end", it=True, extra=halo())
T(893, 536, "the Spark has cost exactly a $100 plan", 9.5, SUB, anchor="end", it=True, extra=halo())

# under-axis
T(130, 806, "Five years of free tending on the cheapest workable rig banks $7,060 against the $200 plan — at quality 48 against the plan’s 63.", 10, SUB, it=True)
T(130, 820, "* a crossing this rig never reaches — it cannot serve the month’s 14.69B tokens no matter how many hours you feed it.", 9.5, RED, it=True)
T(130, 834, "Every crossing assumes your hours are free. The nomograph below re-prices the crossing at any wage — most wages erase it.", 10, SUB, it=True)

# ================= II. the payback nomograph =================
L(ML, 848, MR, 848, RULE, 1)
claim(ML, 880, "II · The payback nomograph — a straightedge from your wage, through your machine, reads the breakeven month")
T(ML, 900, "cash out against the $200 plan — purchase, power, and 13.7 h/mo of tending at your wage · no resale credit · derived from the same measured month", 10, MUT)

XL, XR = 230.0, 850.0
YB, YT = 1160.0, 930.0          # wage scale: $0 bottom .. $15 top
RMAX = 15.0
mpx = (YB - YT) / RMAX          # px per $/h  = 15.333
UZERO, UMAX = 1122.0, 0.0667    # 1/T = 0 at y=1122; T=15 at y=930.1
kpx = (UZERO - 930.1) / UMAX    # px per unit u  = 2879
def yl(r): return YB - r * mpx
def yr(u): return UZERO - u * kpx

# how to read
T(ML, 950, "Find what your hour honestly costs.", 10.5, SUB, it=True)
T(ML, 966, "Lay a line through your machine’s pivot.", 10.5, SUB, it=True)
T(ML, 982, "Where it lands on the right is the month", 10.5, SUB, it=True)
T(ML, 998, "the box has finally cost less than the plan.", 10.5, SUB, it=True)
T(ML, 1024, "a market-rate hour — $75 — sits 28 cm above", 9.5, MUT, it=True)
T(ML, 1038, "the top of the wage scale", 9.5, MUT, it=True)

# left scale
T(XL, 916, "what your hour is worth", 10.5, INK, "600", "middle")
L(XL, YT, XL, YB, FAINT, 1.2)
for r_ in range(0, 16):
    major = (r_ % 5 == 0)
    L(XL - (8 if major else 4), yl(r_), XL, yl(r_), MUT if major else FAINT, 1.1 if major else 0.8)
    if major:
        T(XL - 12, yl(r_) + 3.5, "$15/h" if r_ == 15 else f"${r_}", 9.5, MUT, anchor="end")
L(XL - 12, yl(7.25), XL + 12, yl(7.25), INK, 1, "3 2")
T(XL - 16, yl(7.25) + 3.5, "$7.25 — federal minimum", 9, MUT, anchor="end", it=True)

# right scale
T(XR, 916, "the month you break even", 10.5, INK, "600", "middle")
L(XR, YT, XR, YB, FAINT, 1.2)
rticks = [(15, "15 mo", MUT, "400", 8.5), (18, "18", MUT, "400", 8.5),
          (24, "24 — year two", INK, "600", 9.5), (30, "30", MUT, "400", 8.5),
          (36, "36 — year three", INK, "600", 9.5), (48, "48", MUT, "400", 8.5),
          (60, "60 — year five", INK, "600", 9.5), (120, "120 — year ten", MUT, "400", 8.5)]
for tmo, lab, col, wt, sz in rticks:
    yy = yr(1.0 / tmo)
    L(XR, yy, XR + 6, yy, MUT, 1.1)
    T(XR + 10, yy + 3, lab, sz, col, wt)
L(XR, UZERO, XR + 6, UZERO, RED, 1.3)
T(XR + 10, UZERO + 3.5, "never", 10.5, RED, "600")
L(XR, UZERO, XR, YB, RED, 2.5, op=0.6)
T(XR - 8, 1155, "the straightedge lands below zero — the plan is cheaper forever", 9.5, RED, anchor="end", it=True, extra=halo())

# pivots: for each rig, u = a - b*r with a=(200-power)/H, b=13.7/H
pivots = []
for name, q, hw, pw, ok in RIGS:
    a = (PLAN - pw) / hw
    b = HOURS / hw
    t = mpx / (mpx + b * kpx)
    xp = XL + t * (XR - XL)
    yp = (1 - t) * YB + t * (UZERO - a * kpx)
    pivots.append((name, xp, yp, ok))
    print(f"{name:<11} pivot=({xp:6.1f},{yp:6.1f})  parity wage=${(PLAN-pw)/HOURS:5.2f}/h")
pl = " ".join(f"{'M' if i == 0 else 'L'}{x:.1f},{y:.1f}" for i, (_, x, y, _o) in enumerate(pivots))
s.append(f'<path d="{pl}" fill="none" stroke="{FAINT}" stroke-width="0.8"/>')

# isopleths, all through the 2x3090 pivot
def iso(r, color, sw, dash):
    a, b = (PLAN - 34) / 2900.0, HOURS / 2900.0
    u = a - b * r
    y1_, y2_ = yl(r), yr(u)
    L(XL, y1_, XR, y2_, color, sw, dash)
    dot(XL, y1_, 2.6, PAPER, open_=True, stroke=color)
    dot(XR, y2_, 2.6, PAPER, open_=True, stroke=color)
    return y1_, y2_
iso(0, MUT, 1.1, "5 4")
Trot(450, 1076, "hours at $0 — breakeven month 18", -18.1, 9.5, SUB)
iso(7.25, SUB, 1.2, "")
T(240, 1040, "at minimum wage — month 44", 9.5, SUB, "600", it=True, extra=halo())
iso(13, RED, 1.2, "5 4")
Trot(330, 976, "at $13 an hour — never", 15.6, 9.5, RED, "600")

# pivot dots + labels
for name, xp, yp, ok in pivots:
    dot(xp, yp, 3.6, INK)
    if not ok:
        dot(xp, yp, 6, None, open_=True, stroke=RED, sw=1.3)
plabels = {"2×3090":     (550, 1038, "end",   "2×3090"),
           "Strix Halo": (602, 1041, "start", "Strix Halo"),
           "DGX Spark":  (622, 1084, "end",   "DGX Spark"),
           "RTX 5090":   (706, 1071, "middle","RTX 5090"),
           "Mac 256GB":  (723, 1109, "end",   "Mac 256"),
           "Mac 512GB":  (779, 1096, "start", "Mac 512")}
for name, xp, yp, ok in pivots:
    lx, ly, an, lab = plabels[name]
    T(lx, ly, lab, 10, INK, "400", an, it=True, extra=halo())

# takeaway
T(ML, 1192, "Only if your hour is worth less than about $13 does the straightedge land on a month at all.", 12.5, INK, "600")
T(ML, 1210, "Priced at a real market rate for skilled hours — $75 — every machine lands on never.", 11, RED, it=True)
T(ML, 1226, "isopleths drawn through the 2×3090 pivot — past about $7/h the low-power Strix reads sooner; lay your own straightedge · red ring — cannot serve the month", 8.5, MUT)

# ================= footer =================
L(ML, 1244, MR, 1244, RULE, 1)
T(ML, 1270, "The crossing arrives in year two at the earliest — at $0/h, at two-thirds the quality. At an honest wage it never comes.", 15, INK, "600")
T(ML, 1290, "The meter, for scale: the month cost $200 on plan and $14,914 metered — 74.6×. What a rig still buys is privacy, control, and ownership.", 12, INK, it=True)
T(ML, 1314, "Reading the money — payback: months until plan spend exceeds rig spend (purchase + power + tending at your wage) · plan: flat subscription · metered: same tokens at per-MTok list · quality: AA Intelligence Index", 8.5, MUT)
T(ML, 1334, "Sources — plan prices: Anthropic / OpenAI / Google published tiers · hardware: US street &amp; apple.com prices · power: EIA US average · all verified Aug 28 2026 · resale-credit (sell-anytime) accounting is the frontier sheet", 8.5, MUT)
T(ML, 1346, "demand: our own Claude Code transcripts, Jul 29 – Aug 28 2026 — 14.69B tokens, 71,350 requests, 96% cache-served, deduplicated · feasibility: measured throughput vs the month’s token demand, companion report", 8.5, MUT)
T(W / 2, 1376, "costCalcAI · full method, sensitivity &amp; validation in the companion report · August 2026", 9, MUT, anchor="middle")

# ================= pages =================
def b64(fn):
    return base64.b64encode(open(fn, "rb").read()).decode()
svg = f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;display:block">' + "".join(s) + "</svg>"

fontcss = f"""@font-face{{font-family:'EB Garamond';src:url(data:font/woff2;base64,{b64("ebg-normal-400.woff2")}) format('woff2');font-weight:400 600;font-style:normal;font-display:block}}
@font-face{{font-family:'EB Garamond';src:url(data:font/woff2;base64,{b64("ebg-italic-400.woff2")}) format('woff2');font-weight:400 600;font-style:italic;font-display:block}}"""

page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Payback Horizon — A3 edition</title>
<style>
{fontcss}
body{{margin:0;background:#eceae5;display:flex;justify-content:center;padding:26px 10px}}
.poster{{max-width:990px;width:100%;background:{PAPER};box-shadow:0 8px 34px rgba(0,0,0,.13)}}
@media print{{body{{background:none;padding:0}}.poster{{box-shadow:none}}@page{{size:A3 portrait;margin:0}}}}
</style></head>
<body><div class="poster">{svg}</div></body></html>"""
open("infographic7.html", "w").write(page)
print(f"infographic7.html written: {len(page):,} bytes")

shot = f"""<!doctype html><html><head><meta charset="utf-8"><style>
{fontcss}
html,body{{margin:0;padding:0}}svg{{display:block}}
</style></head><body>{svg}</body></html>"""
open("infographic7_shot.html", "w").write(shot)
print(f"infographic7_shot.html written: {len(shot):,} bytes")

canvas_page = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Payback Horizon — A3 edition</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,600;1,400&display=swap');
body{margin:0;background:#eceae5;display:flex;justify-content:center;padding:26px 10px}
.poster{max-width:990px;width:100%;background:#fffdf8;box-shadow:0 8px 34px rgba(0,0,0,.13)}
</style></head>
<body><div class="poster">""" + svg + "</div></body></html>"
open("infographic7_canvas.html", "w").write(canvas_page)
print(f"infographic7_canvas.html written: {len(canvas_page):,} bytes")
