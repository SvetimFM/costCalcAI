#!/usr/bin/env python3
"""Infographic v5 — Tufte edition. Main-column (60-640) + margin-notes (672-888)
grid; sections as numbered claims; range-frame axes, dot-dash data ticks, dot
plot instead of bars, direct italic labels, no legends/boxes/bands. One serif
(EB Garamond); ink + muted blue (cloud) + red (emphasis) only."""

import base64

W, H = 940, 2200
PAPER = "#fffdf8"
INK, SUB, MUT = "#1a1713", "#57534b", "#8a867d"
RULE, FAINT, WAF = "#ddd9d0", "#c9c5bc", "#dedad1"
BLUE, RED = "#3d6f9e", "#b23a25"
EBG = "'EB Garamond',Georgia,'Times New Roman',serif"
MX = 672          # margin-notes column x
M0, M1 = 60, 640  # main column

s = []
def T(x, y, txt, size=14, fill=INK, w="400", anchor="start", extra="", it=False):
    ital = 'font-style="italic" ' if it else ""
    s.append(f'<text x="{x}" y="{y}" font-family="{EBG}" font-size="{size}" '
             f'font-weight="{w}" fill="{fill}" text-anchor="{anchor}" {ital}{extra}>{txt}</text>')
def L(x1, y1, x2, y2, stroke=RULE, sw=1, dash=""):
    d = f'stroke-dasharray="{dash}"' if dash else ""
    s.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}" {d}/>')
def R(x, y, w_, h_, fill, rx=0, extra=""):
    s.append(f'<rect x="{x}" y="{y}" width="{w_}" height="{h_}" fill="{fill}" rx="{rx}" {extra}/>')
def dot(cx, cy, r_, fill, open_=False):
    if open_:
        s.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r_}" fill="{PAPER}" stroke="{INK}" stroke-width="1.3"/>')
    else:
        s.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r_}" fill="{fill}"/>')
def halo(wd=3):
    return f'paint-order="stroke" stroke="{PAPER}" stroke-width="{wd}"'
def head(y, txt):
    T(M0, y, txt, 21, INK, "600")
def mnote(y0, lines, lh=15):
    y = y0
    for ln in lines:
        if ln is None:
            y += 8; continue
        txt, it = (ln, False) if isinstance(ln, str) else ln
        T(MX, y, txt, 10.5, MUT, it=it)
        y += lh
    return y

R(0, 0, W, H, PAPER)

# ---------- masthead ----------
T(M0, 58, "A COST INVESTIGATION · AUGUST 2026", 11, MUT, "600", extra='letter-spacing="3"')
T(M0, 104, "The Real Price of Local AI", 50, INK, "600")
T(M0, 140, "Once your time has a price, a $200 subscription buys about ten times more quality per dollar than any rig", 17, INK, it=True)
T(M0, 163, "that fits on a desk. Local wins on privacy and control — not on cost.", 17, INK, it=True)
L(M0, 186, 888, 186, RULE, 1)

# ---------- I. scatter (full width) ----------
head(232, "I. Every plan is cheaper and better than every desk rig")
T(M0, 256, "Monthly cost against quality (Artificial Analysis Intelligence Index; local rigs at effective post-quantization score).", 12, MUT)
T(M0, 272, "Each vertical pair is one rig — hollow dot: your time at $0; filled dot: at $75/h. Cloud plans in blue. The x-axis spans only the data, 48–63.", 12, MUT)

px0, px1 = 120, 860
py1, py0 = 360, 690
def sx(q): return px0 + (q - 47) * (px1 - px0) / 17.0
def sy(d): return py0 - d * (py0 - py1) / 1500.0

rigs = [("2×3090",    48, -10,  86, 1111, 328),
        ("RTX 5090",  48,  10, 128, 1153, 344),
        ("Strix Halo", 52, -10,  91, 1116, 312),
        ("DGX Spark",  52,  10, 120, 1145, 296),
        ("Mac 256GB",  53,   0, 193, 1218, 328),
        ("Mac 512GB",  56,   0, 296, 1321, 344)]
plans = ((0, -6), (20, 3), (100, -2), (200, 5))

# range frames + data-value ticks (dot-dash frame)
ymax = 1321
L(104, sy(ymax), 104, sy(0), FAINT, 1.2)
for d_, lab in ((0, "$0"), (500, "$500"), (1000, "$1,000")):
    L(100, sy(d_), 108, sy(d_), MUT, 1.2)
    T(94, sy(d_) + 4, lab, 10.5, MUT, anchor="end")
L(100, sy(ymax), 108, sy(ymax), MUT, 1.2)
T(94, sy(ymax) + 4, "$1,321", 9.5, MUT, anchor="end", it=True)
for _, q, jx, lo, hi, _r in rigs:
    L(100, sy(lo), 104, sy(lo), FAINT, 0.8)
    L(100, sy(hi), 104, sy(hi), FAINT, 0.8)
ax_y = 702
L(sx(48) - 10, ax_y, sx(63) + 10, ax_y, FAINT, 1.2)
for q_, ink_ in ((48, True), (50, False), (55, False), (60, False), (63, True)):
    L(sx(q_), ax_y, sx(q_), ax_y + 5, MUT, 1.2)
    T(sx(q_), ax_y + 19, str(q_), 10.5, INK if ink_ else MUT, "600" if ink_ else "400", "middle")
for _, q, jx, lo, hi, _r in rigs:
    L(sx(q) + jx, ax_y - 3, sx(q) + jx, ax_y, FAINT, 0.8)
L(sx(63), ax_y - 3, sx(63), ax_y, FAINT, 0.8)
T((sx(48) + sx(63)) / 2, ax_y + 36, "quality · Artificial Analysis Intelligence Index", 11, SUB, anchor="middle", it=True)

# pairs: line, pole, dots, label
for name, q, jx, lo, hi, ry in rigs:
    x = sx(q) + jx
    L(x, sy(lo) - 5, x, sy(hi) + 5, INK, 0.7)
    L(x, ry + 5, x, sy(hi) - 6, FAINT, 0.7)
for name, q, jx, lo, hi, ry in rigs:
    dot(sx(q) + jx, sy(lo), 3.4, PAPER, open_=True)
    dot(sx(q) + jx, sy(hi), 3.4, INK)
for name, q, jx, lo, hi, ry in rigs:
    T(sx(q) + jx, ry, f"{name} · ${lo:,} → ${hi:,}", 11.5, INK, "400", "middle", extra=halo(), it=True)
for d_, jx_ in plans:
    dot(sx(63) + jx_, sy(d_), 3.4, BLUE)

# annotations, set type — no boxes, no leaders
T(790, 592, "the corner you want —", 12.5, INK, "600", "end", extra=halo(), it=True)
T(790, 610, "all quality 63: free · $17–20 Pro / Plus", 11, SUB, anchor="end", extra=halo())
T(790, 626, "$100 mid tiers · $200 Max 20x / GPT Pro / Ultra", 11, SUB, anchor="end", extra=halo())
T(790, 648, "our metered month: $14,914 — ten times off this chart", 11.5, RED, anchor="end", extra=halo(), it=True)
T(640, 480, "the gap no money closes:", 11.5, MUT, anchor="end", extra=halo(), it=True)
T(640, 496, "more spend moves a rig up, not right", 11.5, MUT, anchor="end", extra=halo(), it=True)

T(M0, 748, "Sources — quality: Artificial Analysis Intelligence Index v4.1.1, retrieved Aug 28 2026 · plan prices: Anthropic / OpenAI / Google published tiers, verified Aug 28 2026", 10, MUT)
T(M0, 762, "rig $/mo: the report’s TCO model — 3-yr amortization net of resale, power at $0.18–0.40/kWh, labor $0 or $75/h · full workings in the companion report", 10, MUT)

# ---------- II. rig table (main + margin) ----------
head(816, "II. Hardware is the cheap part")
T(M0, 840, "Five community builds at August 2026 street prices. Both monthly figures re-appear as the pairs above.", 12, MUT)
for cx_, lab_ in ((420, "HARDWARE"), (528, "$/MO · TIME $0"), (640, "$/MO · $75/H")):
    T(cx_, 872, lab_, 10, MUT, "600", "end", extra='letter-spacing="1.5"')
T(M0, 872, "RIG", 10, MUT, "600", extra='letter-spacing="1.5"')
L(M0, 880, M1, 880, RULE, 1)
table = [
    ("2× used RTX 3090", "$2,900", "$86", "$1,111",
     "the r/LocalLLaMA classic — 48GB · runs 27B-class · ~150 tok/s"),
    ("Strix Halo 128GB", "$3,650", "$91", "$1,116",
     "the 2026 mini-PC wave (GMKtec, Framework) — 128GB unified · 120B-class MoE · 35–57 tok/s"),
    ("DGX Spark", "$4,699", "$120", "$1,145",
     "NVIDIA’s desk AI box — 128GB unified · 120B-class MoE · 39–61 tok/s"),
    ("RTX 5090 workstation", "$8,500", "$128", "$1,153",
     "the fast lane (card alone $4.3–4.9k) — 32GB · 27B-class · 180–420 tok/s"),
    ("Mac Studio 256–512GB", "$10.8–17.2k", "$193–296", "$1,218–1,321",
     "the big-memory king (or lease from $210/mo) — up to 512GB unified · GLM-5.3-Flash, DeepSeek-class"),
]
for i, (nm, hw, lo, hi, tag) in enumerate(table):
    y = 906 + i * 54
    T(M0, y, nm, 15, INK, "600")
    T(420, y, hw, 13, SUB, anchor="end")
    T(528, y, lo, 13, SUB, anchor="end")
    T(640, y, hi, 13, INK, "600", "end")
    T(M0, y + 16, tag, 10.5, MUT, it=True)
L(M0, 1148, M1, 1148, RULE, 1)
mnote(816, [
    "Sources: r/LocalLLaMA build threads;",
    "US street &amp; apple.com list / lease",
    "prices, Aug 28 2026. $/mo — the",
    "companion TCO model (3-yr, resale-",
    "and power-adjusted).",
    None,
    "tok/s = tokens per second; 20 is",
    "comfortable reading speed. MoE =",
    "mixture-of-experts — big models",
    "that run lighter.",
    None,
    ("The software layer is free and", True),
    ("excellent — llama.cpp, Ollama, LM", True),
    ("Studio, MLX, vLLM. Open source did", True),
    ("the innovating; the hardware bill", True),
    ("is the part nobody waives.", True),
])

# ---------- III. model dot plot (main + margin) ----------
head(1204, "III. Open models trail by three points — at sizes no desk can hold")
T(M0, 1228, "Artificial Analysis Intelligence Index. Hollow circles: the effective score after the 4-bit quantization needed to fit desk memory.", 12, MUT)
def sx3(v): return 262 + (v - 20) * (620 - 262) / 45.0
models = [
    ("Claude Opus 5", 63, BLUE, None, "cloud only — in every plan", False),
    ("Kimi K3 · open", 60, INK, None, "no desk can hold it (2.8T)", False),
    ("GLM-5.3 · open", 60, INK, None, "server-class only (753B)", False),
    ("GLM-5.3-Flash", 57, INK, 53, "fits a 256GB Mac", True),
    ("Qwen3.8-Flash-Next", 56, INK, 52, "fits 128GB boxes", False),
    ("Qwen3.8-27B", 52, INK, 48, "fits a 32GB GPU", False),
    ("gpt-oss-120b", 24, INK, None, "2025 generation — superseded", False),
]
for i, (nm, v, col, eff, note, new) in enumerate(models):
    y = 1260 + i * 33
    T(250, y, nm, 13, INK, anchor="end")
    end_x = (sx3(eff) if eff else sx3(v)) - 8
    L(262, y - 4, end_x, y - 4, FAINT, 1, "1 4")
    if eff:
        dot(sx3(eff), y - 4, 4, PAPER, open_=True)
        L(sx3(eff) + 5, y - 4, sx3(v) - 5, y - 4, INK, 0.8)
    dot(sx3(v), y - 4, 4, col)
    T(sx3(v) + 10, y, str(v), 12, INK, "600")
    T(MX, y, note, 10.5, MUT)
    if new:
        T(MX + 100, y, "· new — weeks old", 10.5, RED, it=True)
ax3 = 1478
L(sx3(24) - 8, ax3, sx3(63) + 8, ax3, FAINT, 1.2)
for v_ in (20, 30, 40, 50, 60):
    L(sx3(v_), ax3, sx3(v_), ax3 + 5, MUT, 1.2)
    T(sx3(v_), ax3 + 19, str(v_), 10.5, MUT, anchor="middle")
L(sx3(63), ax3, sx3(63), ax3 + 5, INK, 1.2)
T(sx3(63), ax3 + 19, "63", 10.5, INK, "600", "middle")
mnote(1486, [
    "Source: Artificial Analysis Intelligence",
    "Index v4.1.1, retrieved Aug 28 2026.",
    "4-bit effective score ≈ 93% retention",
    "— community quantization evals.",
])

# ---------- IV. builder stats (main + margin) ----------
head(1584, "IV. The builders count the cost in days and interventions")
L(M0, 1600, M1, 1600, RULE, 1)
stats = [
    ("2–7 days", ["to stand up an", "agent-grade rig"]),
    ("7×", ["more interventions than", "Claude — paired study"]),
    ("44×", ["the same error looped;", "the agent never noticed"]),
    ("0", ["working local replacements", "for a €440k/yr Claude", "team, asking publicly"]),
]
for i, (big, lines) in enumerate(stats):
    x = (M0, 205, 350, 495)[i]
    T(x, 1638, big, 24, INK, "600")
    for j, ln in enumerate(lines):
        T(x, 1658 + j * 14, ln, 10.5, SUB)
T(M0, 1722, "“Comparing agentic Qwen to Claude Opus is like a junior… versus a senior that thinks.”", 14.5, INK, it=True)
T(M0, 1742, "— Mac Studio 128GB owner, Hacker News, June 2026", 10.5, MUT)
mnote(1584, [
    "Sources: paired-agent field study,",
    "Jun 2026; llama.cpp GitHub issues",
    "#20198 &amp; #27406 (closed “not",
    "planned”); Hacker News and",
    "r/LocalLLaMA threads, 2025–26.",
])

# ---------- V. case study (main + margin) ----------
head(1812, "V. Our own month would not fit on any of them")
T(M0, 1836, "One month of our Claude Code usage, measured from transcripts: 14.69B tokens, 71,350 requests — 96% served from provider cache.", 12, MUT)
for i in range(75):
    r_, c_ = divmod(i, 15)
    R(M0 + c_ * 15, 1862 + r_ * 15, 12, 12, RED if i == 0 else WAF, rx=1)
T(330, 1892, "$14,914", 30, INK, "600")
T(330, 1912, "API-equivalent consumed", 11, MUT)
T(478, 1892, "$200", 30, RED, "600")
T(478, 1912, "actually paid — 75× leverage", 11, MUT)
T(M0, 1956, "Each square is $200 of API-equivalent usage; the red square is what we actually paid — the other 74 came with the subscription.", 10.5, MUT)
T(M0, 1992, "Compute-hours the month demands from each rig", 12.5, INK, "600")
T(M0, 2008, "Open circles fit inside the month’s 720 hours; red squares don’t.", 10.5, MUT)
ly = 2036
def fx(h): return M0 + min(h, 1400) * (628 - M0) / 1400.0
L(M0, ly, 628, ly, FAINT, 1.5)
L(fx(720), ly - 12, fx(720), ly + 32, INK, 1, "4 3")
for h in (143, 341, 1263):
    T(fx(h), ly - 14, f"{h:,}", 10.5, SUB, "600", "middle")
T(fx(692) - 3, ly - 14, "692", 10.5, SUB, "600", "end")
T(fx(731) + 3, ly - 14, "731", 10.5, SUB, "600", "start")
T(628, ly - 14, "3,817", 10.5, SUB, "600", "end")
for h in (143, 341, 692):
    dot(fx(h), ly, 5, PAPER, open_=True)
for h in (731, 1263):
    R(fx(h) - 5, ly - 5, 10, 10, RED, rx=1)
s.append(f'<path d="M{622},{ly-6} l11,6 l-11,6 z" fill="{RED}"/>')
names1 = (("5090", 143), ("2×3090", 341), ("Spark", 731), ("Strix", 1263))
for nm, h in names1:
    T(fx(h), ly + 18, nm, 9.5, MUT, "600", "middle", extra=halo())
T(fx(692), ly + 30, "Mac 256", 9.5, MUT, "600", "middle", extra=halo())
T(628, ly + 18, "Mac 512", 9.5, MUT, "600", "end")
T(fx(720), ly + 44, "720 h", 10, INK, "600", "middle", extra=halo(), it=True)
T(M0, 2108, "No rig on this page could serve our volume at frontier quality — several can’t serve it at all.", 14.5, INK, "600")
T(M0, 2128, "For a heavy user the plan wins by an order of magnitude; local wins on privacy, API-arbitrage or hobby terms — not on cost-per-quality.", 11.5, SUB)
mnote(1812, [
    "Demand measured from our own",
    "Claude Code transcripts, Jul 29 –",
    "Aug 28 2026, deduplicated per",
    "request; API-equivalent dollars at",
    "published per-MTok rates including",
    "cache-write and cache-read tiers.",
    None,
    "Hours pair each rig with its best",
    "model: 5090 &amp; 2×3090 — Qwen-27B;",
    "Spark &amp; Strix — Qwen-Flash-Next;",
    "Mac 256 — GLM-5.3-Flash; Mac 512 —",
    "DeepSeek-class (3,817 h, off scale).",
    None,
    "Hardware, plan and benchmark data",
    "primary-source verified Aug 28 2026.",
])

T(W / 2, 2172, "Full method, sensitivity and validation in the companion report · costCalcAI, August 2026", 10.5, MUT, anchor="middle")

# ---------- page ----------
def b64(fn):
    return base64.b64encode(open(fn, "rb").read()).decode()
svg = f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;display:block">' + "".join(s) + "</svg>"
page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Real Price of Local AI — Tufte edition</title>
<style>
@font-face{{font-family:'EB Garamond';src:url(data:font/woff2;base64,{b64("ebg-normal-400.woff2")}) format('woff2');font-weight:400 600;font-style:normal;font-display:block}}
@font-face{{font-family:'EB Garamond';src:url(data:font/woff2;base64,{b64("ebg-italic-400.woff2")}) format('woff2');font-weight:400 600;font-style:italic;font-display:block}}
body{{margin:0;background:#eceae5;display:flex;justify-content:center;padding:26px 10px}}
.poster{{max-width:960px;width:100%;background:{PAPER};border-radius:6px;
box-shadow:0 8px 34px rgba(0,0,0,.13)}}</style></head>
<body><div class="poster">{svg}</div></body></html>"""
open("infographic4.html", "w").write(page)
print(f"infographic4.html written: {len(page):,} bytes")

canvas_head = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Real Price of Local AI — Tufte edition</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,600;1,400&display=swap');
body{margin:0;background:#eceae5;display:flex;justify-content:center;padding:26px 10px}
.poster{max-width:960px;width:100%;background:#fffdf8;border-radius:6px;
box-shadow:0 8px 34px rgba(0,0,0,.13)}</style></head>
<body><div class="poster">"""
open("infographic4_canvas.html", "w").write(canvas_head + svg + "</div></body></html>")
print(f"infographic4_canvas.html written: {len(canvas_head + svg) + 22:,} bytes")
