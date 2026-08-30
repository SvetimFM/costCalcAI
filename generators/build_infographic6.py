#!/usr/bin/env python3
"""Infographic v7 — the frontier edition. One master encoding (cost-capability
frontier with an explicit dominance region) at ~55% of the sheet; three demoted
evidence panels: cost decomposition + breakeven wage, required utilization,
the metered ratio. Color semantics: ink = local, blue = plan, red = constraint
violation / metered penalty only. A3 sheet, 990x1400 (1:sqrt2)."""

import base64

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

# ================= masthead =================
T(ML, 40, "A COST INVESTIGATION · SIX DESK RIGS · FOUR CLOUD PLANS · ONE METERED MONTH", 10, MUT, "600", extra='letter-spacing="2.6"')
T(MR, 40, "SET AS ONE A3 SHEET · 1 : √2", 10, MUT, "600", "end", extra='letter-spacing="2"')
T(ML, 88, "The Inference Frontier", 42, INK, "600")
T(ML, 112, "One measured month of agentic coding, priced against six desk rigs and four cloud plans. Once your time has a price, every rig is dominated —", 13, INK, it=True)
T(ML, 128, "less capable and more expensive than the plan that did the work. What local still sells is privacy, control, and ownership.", 13, INK, it=True)
L(ML, 142, MR, 142, RULE, 1)

# ================= I. the frontier (hero) =================
claim(ML, 174, "I · The cost–capability frontier — capable is right, cheap is down; only the plans reach the corner you want")
T(MR, 198, "each vertical pair is one rig — hollow: cash TCO, your hours at $0 · filled: fully loaded, 13.7 h/mo at $75/h", 10, MUT, anchor="end")
T(MR, 212, "blue — the four cloud plans, all at quality 63 · red ring — cannot finish the month (see III)", 10, MUT, anchor="end")
T(MR, 226, "shaded — dominated by the $200 plan: less capable and more expensive", 10, RED, anchor="end", it=True)

PX0, PX1 = 130, 900
PY1, PY0 = 254, 820                       # $1,400 top, $0 bottom
YMAX = 1400.0
def qx(q): return PX0 + (q - 47) * 770.0 / 17.0
def cy(d): return PY0 - d * (PY0 - PY1) / YMAX

# (name, q, jitter, cash lo, loaded hi, hours, feasible)
rigs = [("2×3090",     48, -12,  86, 1111,  341, True),
        ("RTX 5090",   48,  12, 128, 1153,  143, True),
        ("Strix Halo", 52, -12,  91, 1116, 1263, False),
        ("DGX Spark",  52,  12, 120, 1145,  731, False),
        ("Mac 256GB",  53,   0, 193, 1218,  692, True),
        ("Mac 512GB",  56,   0, 296, 1321, 3817, False)]
plans = ((0, -6), (20, 3), (100, -2), (200, 5))
p200x, p200y = qx(63) + 5, cy(200)

# dominance region (under everything else in the plot)
R(114, PY1, p200x - 114, p200y - PY1, RED, extra='opacity="0.032"')
L(114, p200y, p200x, p200y, RED, 1, "5 4", op=0.45)
L(p200x, p200y, p200x, PY1, RED, 1, "5 4", op=0.45)

# axes
L(114, cy(YMAX), 114, cy(0), FAINT, 1.2)
for v_, lab in ((0, "$0"), (400, "$400"), (800, "$800"), (1200, "$1,200")):
    L(110, cy(v_), 118, cy(v_), MUT, 1.2)
    T(104, cy(v_) + 4, lab, 10, MUT, anchor="end")
L(110, cy(200), 118, cy(200), RED, 1, op=0.6)
T(104, cy(200) + 3, "$200", 9, RED, anchor="end", it=True)
T(104, 240, "dollars per month — cheaper ↓", 10, MUT, it=True)
L(114, PY0, PX1, PY0, FAINT, 1.2)
for q_, ink_ in ((48, True), (52, False), (56, False), (60, False), (63, True)):
    L(qx(q_), PY0, qx(q_), PY0 + 5, MUT, 1.2)
    T(qx(q_), PY0 + 18, str(q_), 10, INK if ink_ else MUT, "600" if ink_ else "400", "middle")

# model rug + the gap bracket
T(qx(48), 852, "Qwen3.8-27B", 8.5, MUT, anchor="middle", it=True)
T(380, 852, "Qwen-Flash · GLM-5.3-Flash", 8.5, MUT, anchor="middle", it=True)
T(qx(56), 852, "DeepSeek-class", 8.5, MUT, anchor="middle", it=True)
L(qx(60), 860, qx(63), 860, MUT, 1)
L(qx(60), 860, qx(60), 856, MUT, 1)
L(qx(63), 860, qx(63), 856, MUT, 1)
T((qx(60) + qx(63)) / 2, 874, "the gap no desk closes", 8.5, SUB, anchor="middle", it=True)
T(130, 874, "quality — Artificial Analysis Intelligence Index · more capable →", 8.5, MUT, it=True)

# open-weights ceiling
L(qx(60), PY0, qx(60), 520, FAINT, 1, "3 4")
T(qx(60), 508, "open-weights ceiling — 60, at server-rack sizes", 9, MUT, anchor="middle", it=True, extra=halo())

# region label
T(842, 452, "everything shaded is dominated by the $200 plan —", 12.5, RED, "600", "end", extra=halo(), it=True)
T(842, 470, "less capable, and more expensive", 12.5, RED, "400", "end", extra=halo(), it=True)

# rig pairs: connector + up arrowhead + dots + tags
for name, q, jx, lo, hi, hrs, ok in rigs:
    x = qx(q) + jx
    L(x, cy(lo) - 5, x, cy(hi) + 6, INK, 0.7)
    s.append(f'<path d="M{x-3.2:.1f},477 L{x:.1f},468 L{x+3.2:.1f},477 Z" fill="{INK}"/>')
for name, q, jx, lo, hi, hrs, ok in rigs:
    x = qx(q) + jx
    hollow(x, cy(lo), 3.2)
    dot(x, cy(hi), 3.2, INK)
    if not ok:
        dot(x, cy(hi), 5.8, None, open_=True, stroke=RED, sw=1.2)
    T(x + 7, cy(lo) + 3.5, f"${lo:,}", 8.5, MUT)

# rig labels (verified stagger: above/below/left/right per rig)
T(qx(48) - 12, 388, "2×3090 — $1,111", 11, INK, "400", "middle", extra=halo(), it=True)
T(qx(48) + 12, 338, "RTX 5090 — $1,153", 11, INK, "400", "middle", extra=halo(), it=True)
T(qx(52) - 12 - 11, 371, "Strix Halo — $1,116", 11, INK, "400", "end", extra=halo(), it=True)
T(qx(52) + 12 + 12, 359, "DGX Spark — $1,145", 11, INK, "400", "start", extra=halo(), it=True)
T(qx(53) + 12, 330, "Mac 256GB — $1,218", 11, INK, "400", "start", extra=halo(), it=True)
T(qx(56) + 12, 288, "Mac 512GB — $1,321", 11, INK, "400", "start", extra=halo(), it=True)

# the one lesson of the vertical pairs
T(300, 545, "$75/h of tending moves every rig up — never right", 11, MUT, "400", "middle", extra=halo(), it=True)

# plans
for d_, jx_ in plans:
    dot(qx(63) + jx_, cy(d_), 3.4, BLUE)
dot(p200x, p200y, 8, None, open_=True, stroke=BLUE, sw=1.2)
T(843, p200y - 5, "$200 Max / Pro / Ultra — the tier that served this month", 11, BLUE, "600", "end", extra=halo(), it=True)
T(843, cy(100) + 4, "$100 mid tiers", 10, BLUE, "400", "end", extra=halo())
T(840, cy(20) + 4, "free · $20 Pro / Plus", 10, BLUE, "400", "end", extra=halo())

# metered annotation — off the top of the axis
L(868, 330, 868, 268, RED, 1.6)
s.append(f'<path d="M864.4,269 L868,259 L871.6,269 Z" fill="{RED}"/>')
T(930, 350, "the same month, metered: $14,914", 11.5, RED, "600", "end", extra=halo(), it=True)
T(930, 366, "10.7× past the top of this axis — the plan compressed it 74.6×", 9, RED, "400", "end", extra=halo(), it=True)

# ================= evidence band =================
L(ML, 892, MR, 892, RULE, 1)
L(376, 906, 376, 1156, FAINT, 1)
L(680, 906, 680, 1156, FAINT, 1)

# ---- II. where the money goes ----
claim(ML, 924, "II · Where the money goes", 15)
k = 300.0 / 1111.0
T(ML, 950, "cash $86", 8.5, MUT)
R(ML, 956, 86 * k, 16, MUT)
R(ML + 86 * k + 2, 956, 1025 * k, 16, INK)
T(ML + 86 * k + 2 + 1025 * k / 2, 967.5, "your hours — $1,025", 9.5, PAPER, "600", "middle")
T(ML, 990, "fully loaded: $1,111/mo — 92% is your 13.7 hours", 10.5, INK, "600")
T(ML, 1004, "box $40 · capital $12 · power $34 — then the hours", 8.5, MUT)

T(ML, 1022, "the breakeven wage — the most an hour of yours can be", 9.5, MUT, it=True)
T(ML, 1034, "worth before the rig loses to the $200 plan on cost:", 9.5, MUT, it=True)
def wx(r): return ML + r * 30.0
wy = 1070
L(wx(0), wy, wx(10), wy, FAINT, 1.5)
for r_, lab in ((0, "$0"), (10, "$10/h")):
    L(wx(r_), wy, wx(r_), wy + 5, MUT, 1.2)
    T(wx(r_), wy + 16, lab, 8.5, MUT, anchor="middle")  # y1086 shared with below-row labels
L(wx(7.25), wy - 14, wx(7.25), wy + 10, MUT, 1, "3 3")
T(wx(7.25) - 40, 1102, "US federal minimum — $7.25", 8, MUT, "400", "middle", it=True, extra=halo())
bes = ((8.32, "2×3090"), (7.96, "Strix"), (5.84, "Spark"), (5.26, "RTX 5090"), (0.51, "Mac 256"))
for r_, nm in bes:
    dot(wx(r_), wy, 3, INK)
T(wx(5.26), 1054, "5090 · $5.26", 8.5, SUB, "400", "middle", extra=halo())
T(wx(7.96) + 4, 1054, "Strix · $7.96", 8.5, SUB, "400", "middle", extra=halo())
T(wx(5.84) - 4, 1086, "Spark · $5.84", 8.5, SUB, "400", "middle", extra=halo())
T(wx(8.32) + 8, 1086, "2×3090 · $8.32", 8.5, SUB, "400", "end", extra=halo())
T(wx(0.51) + 6, 1086, "Mac 256 · $0.51", 8.5, SUB, "400", "start", extra=halo())
T(ML, 1120, "Mac 512GB never breaks even — $296/mo at $0/h.", 9.5, RED, it=True)
T(ML, 1140, "Even the best rig pays you $8.32 an hour —", 10.5, INK, "600")
T(ML, 1154, "barely a minimum wage, before anything breaks.", 10.5, INK, "600")

# ---- III. can one machine keep up ----
claim(392, 924, "III · Can one machine keep up?", 15)
T(392, 946, "generation-hours our month demands, as a share of one", 9, MUT, it=True)
T(392, 958, "machine-month — 720 hours of nonstop output:", 9, MUT, it=True)
BX0, BX1 = 462, 660
uk = (BX1 - BX0) / 530.0
u100 = BX0 + 100 * uk
rows = (("RTX 5090", 20, "20%"), ("2×3090", 47, "47%"), ("Mac 256GB", 96, "96%"),
        ("DGX Spark", 102, "102%"), ("Strix Halo", 175, "175%"), ("Mac 512GB", 530, "530%"))
L(u100, 966, u100, 1108, INK, 1, "4 3")
for i, (nm, u, lab) in enumerate(rows):
    yb = 974 + i * 23
    T(392, yb + 8, nm, 9.5, INK)
    if u <= 100:
        R(BX0, yb, u * uk, 10, INK)
        T(BX0 + u * uk + 5, yb + 8, lab, 9, SUB, "600")
    else:
        R(BX0, yb, 100 * uk, 10, INK)
        R(u100 + 1, yb, max((u - 100) * uk - 1, 0.9), 10, RED)
        if u == 530:
            T(BX1 - 5, yb + 8, lab, 9, PAPER, "600", "end")
        else:
            T(BX0 + u * uk + 5, yb + 8, lab, 9, RED, "600")
T(u100, 1122, "one machine-month", 8.5, MUT, "400", "middle", it=True, extra=halo())
T(392, 1140, "Three rigs cannot finish the month at all —", 10, RED, it=True)
T(392, 1154, "the heaviest needs 5.3 machines running nonstop.", 10, RED, it=True)

# ---- IV. what the meter said ----
claim(700, 924, "IV · What the meter said", 15)
T(700, 964, "$200", 30, BLUE, "600")
T(700, 980, "the plan — flat, one month", 8.5, MUT)
T(700, 1026, "$14,914", 30, RED, "600")
T(700, 1042, "the same tokens, metered at API list price", 8.5, MUT)
R(700, 1058, 234.0 / 74.57, 9, BLUE)
T(700 + 234.0 / 74.57 + 6, 1066, "$200", 8, MUT)
R(700, 1071, 234, 9, RED)
T(928, 1078.5, "$14,914", 8, PAPER, "600", "end")
T(700, 1102, "74.6× realized price compression", 11.5, INK, "600")
T(700, 1126, "14.69B tokens · 71,350 requests · 96% cache-served", 9, MUT)
T(700, 1140, "the metered figure is workload-dependent — an annotation, not a plan", 8.5, MUT, it=True)

# ================= verdict + evidence + method =================
L(ML, 1172, MR, 1172, RULE, 1)
T(ML, 1200, "No rig tested reaches the frontier — three cannot even finish the month.", 15, INK, "600")
T(ML, 1220, "What local still buys is privacy, control, and ownership. The work itself belongs on the plan — the meter says the gap is 74.6×.", 12, INK, it=True)

T(ML, 1248, "interventions per task, paired field study:", 9.5, SUB)
for i in range(7):
    dot(252 + i * 11, 1244, 2.8, INK)
T(326, 1248, "local 7", 9.5, INK, "600")
dot(394, 1244, 2.8, BLUE)
T(402, 1248, "Claude 1", 9.5, BLUE, "600")
T(MR, 1248, "“A junior next to a senior that thinks” — a Mac Studio owner, HN, June 2026", 10, INK, anchor="end", it=True)
for i in range(44):
    L(56 + i * 4, 1262, 56 + i * 4, 1271, RED, 1.1)
T(240, 1270, "one error, looped 44 times — the agent never noticed", 9.5, RED, it=True)
T(MR, 1270, "2–7 days to stand one up · 0 local replacements surfaced for a €440k/yr Claude team", 9, SUB, anchor="end")

T(ML, 1298, "Reading the money — cash TCO: hardware amortized over 36 months net of resale + 5%/yr capital charge + power at 18.3¢/kWh · fully loaded: cash TCO + 13.7 h/mo of setup, patches and tending at $75/h", 8.5, MUT)
T(ML, 1310, "plan: flat subscription price · metered: the same tokens at published per-MTok rates, cache tiers included · quality: Artificial Analysis Intelligence Index v4.1.1, effective at each rig’s largest servable model", 8.5, MUT)
T(ML, 1334, "Sources — plan prices: Anthropic / OpenAI / Google published tiers · hardware: US street &amp; apple.com prices · power: EIA US average · all verified Aug 28 2026", 8.5, MUT)
T(ML, 1346, "demand: our own Claude Code transcripts, Jul 29 – Aug 28 2026 — 14.69B tokens, 71,350 requests, 96% cache-served, deduplicated · field evidence: paired study Jun 2026, llama.cpp #20198/#27406, HN &amp; r/LocalLLaMA", 8.5, MUT)
T(W / 2, 1376, "costCalcAI · full method, sensitivity &amp; validation in the companion report · August 2026", 9, MUT, anchor="middle")

# ================= pages =================
def b64(fn):
    return base64.b64encode(open(fn, "rb").read()).decode()
svg = f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;display:block">' + "".join(s) + "</svg>"

fontcss = f"""@font-face{{font-family:'EB Garamond';src:url(data:font/woff2;base64,{b64("ebg-normal-400.woff2")}) format('woff2');font-weight:400 600;font-style:normal;font-display:block}}
@font-face{{font-family:'EB Garamond';src:url(data:font/woff2;base64,{b64("ebg-italic-400.woff2")}) format('woff2');font-weight:400 600;font-style:italic;font-display:block}}"""

page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Inference Frontier — A3 edition</title>
<style>
{fontcss}
body{{margin:0;background:#eceae5;display:flex;justify-content:center;padding:26px 10px}}
.poster{{max-width:990px;width:100%;background:{PAPER};box-shadow:0 8px 34px rgba(0,0,0,.13)}}
@media print{{body{{background:none;padding:0}}.poster{{box-shadow:none}}@page{{size:A3 portrait;margin:0}}}}
</style></head>
<body><div class="poster">{svg}</div></body></html>"""
open("infographic6.html", "w").write(page)
print(f"infographic6.html written: {len(page):,} bytes")

shot = f"""<!doctype html><html><head><meta charset="utf-8"><style>
{fontcss}
html,body{{margin:0;padding:0}}svg{{display:block}}
</style></head><body>{svg}</body></html>"""
open("infographic6_shot.html", "w").write(shot)
print(f"infographic6_shot.html written: {len(shot):,} bytes")

canvas_page = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Inference Frontier — A3 edition</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,600;1,400&display=swap');
body{margin:0;background:#eceae5;display:flex;justify-content:center;padding:26px 10px}
.poster{max-width:990px;width:100%;background:#fffdf8;box-shadow:0 8px 34px rgba(0,0,0,.13)}
</style></head>
<body><div class="poster">""" + svg + "</div></body></html>"
open("infographic6_canvas.html", "w").write(canvas_page)
print(f"infographic6_canvas.html written: {len(canvas_page):,} bytes")
