#!/usr/bin/env python3
"""Infographic v4 — argument-first restructure.
Masthead + verdict standfirst -> lead scatter -> rig table -> model bars ->
field-report stat row -> case-study band. Embedded Fraunces (display) and
Caveat (hand annotations); palette re-validated (ORANGE_D deepened)."""

import base64

W, H = 940, 2610
INK, SUB, MUT, GRID = "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
BLUE = "#2a78d6"
BLUE_L = "#9ec5f4"
ORANGE, ORANGE_D = "#eb6834", "#a03a10"
GREEN, YELLOW, RED = "#0ca30c", "#eda100", "#d03b3b"
RED_S = "#b3252a"  # status red (infeasible) — distinct from annotation red
SER = "Georgia,'Times New Roman',serif"
SER_D = "'Fraunces',Georgia,'Times New Roman',serif"
SANS = "system-ui,-apple-system,'Segoe UI',sans-serif"
HAND = "'Caveat','Bradley Hand','Segoe Print',cursive"
POLE = "#d8d7cf"

s = []
def T(x, y, txt, size=14, fill=INK, w="400", anchor="start", font=SANS, extra=""):
    s.append(f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" '
             f'font-weight="{w}" fill="{fill}" text-anchor="{anchor}" {extra}>{txt}</text>')
def R(x, y, w_, h_, fill, rx=0, extra=""):
    s.append(f'<rect x="{x}" y="{y}" width="{w_}" height="{h_}" fill="{fill}" rx="{rx}" {extra}/>')
def L(x1, y1, x2, y2, stroke=GRID, sw=1, dash=""):
    d = f'stroke-dasharray="{dash}"' if dash else ""
    s.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}" {d}/>')
def C(cx, cy, r_, fill):
    s.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r_}" fill="{fill}" stroke="#ffffff" stroke-width="2"/>')
def header(y, title, caption):
    R(50, y - 15, 17, 17, ORANGE)
    T(78, y, title, 25, INK, "700", font=SER_D)
    T(52, y + 24, caption, 13, MUT)
def hand(x, y, txt, size=20, rot=-3, anchor="start"):
    T(x, y, txt, size, RED, "700", anchor, HAND, f'transform="rotate({rot} {x} {y})"')
def scribble(cx, cy, rx, ry):
    s.append(f'<path d="M{cx-rx},{cy} C{cx-rx},{cy-ry*1.25} {cx+rx*0.9},{cy-ry*1.3} {cx+rx},{cy-ry*0.15} '
             f'C{cx+rx*1.08},{cy+ry} {cx-rx*0.8},{cy+ry*1.3} {cx-rx*1.06},{cy+ry*0.25}" '
             f'fill="none" stroke="{RED}" stroke-width="3" stroke-linecap="round"/>')
def halo(wd=3.5):
    return f'paint-order="stroke" stroke="#ffffff" stroke-width="{wd}"'

R(0, 0, W, H, "#ffffff")

# ---------- masthead ----------
T(52, 54, "A COST INVESTIGATION · AUGUST 2026", 12, ORANGE, "700", extra='letter-spacing="3"')
R(52, 72, 34, 34, ORANGE)
T(102, 101, "The Real Price of Local AI", 53, INK, "900", font=SER_D)
T(52, 136, '<tspan font-weight="700" fill="#0b0b0b">The verdict:</tspan> once your time has a price, a $200 subscription buys about ten times more quality', 16, SUB)
T(52, 158, "per dollar than any rig that fits on a desk. Local wins on privacy, control and tinkering — not on cost.", 16, SUB)
T(52, 184, "Six community builds · open models incl. the weeks-old GLM-5.3-Flash · our own measured month as case study · primary sources, Aug 28 2026", 12, MUT)
L(52, 208, 888, 208, GRID, 1.5)

# ---------- S1 (lead): price vs quality ----------
sc_y = 250
header(sc_y + 14, "Price vs quality — the whole market on one chart",
       "Six desk-class builds (detailed below), each shown twice: your time at $0, then at $75/h · the cloud plans for comparison")
lgy = sc_y + 64
for lx, col, lab in ((52, BLUE, "subscription plan (dot size = price)"),
                     (332, ORANGE, "local rig · your time at $0"),
                     (542, ORANGE_D, "local rig · time at $75/h")):
    C(lx + 8, lgy, 7, col)
    T(lx + 22, lgy + 4, lab, 11.5, SUB, "600")
L(744, lgy - 8, 744, lgy + 8, "#b3b2ab", 1.5, "2 3")
T(756, lgy + 4, "same rig, linked", 11.5, SUB, "600")

px0, px1 = 120, 870
py1, py0 = 374, 774
def sx(q): return px0 + (q - 45) * (px1 - px0) / 20.0
def sy(d): return py0 - d * (py0 - py1) / 1500.0
for d in (0, 500, 1000, 1500):
    L(px0 - 10, sy(d), px1 + 10, sy(d), GRID, 1, "3 5")
    T(px0 - 16, sy(d) + 4, f"${d:,}", 11, MUT, anchor="end")
for q in (45, 50, 55, 60, 65):
    T(sx(q), py0 + 20, str(q), 11.5, MUT, anchor="middle")
    L(sx(q), py0, sx(q), py0 + 5, "#b9b8b2", 1.2)
L(px0 - 10, py0, px1 + 10, py0, "#b9b8b2", 1.5)
L(px0 + 3, py0 + 4, px0 + 9, py0 - 4, "#b9b8b2", 1.2)
L(px0 + 8, py0 + 4, px0 + 14, py0 - 4, "#b9b8b2", 1.2)
T((px0 + px1) / 2, py0 + 42,
  "quality · Artificial Analysis Intelligence Index — local rigs at effective post-quantization score · axis begins at 45", 12, SUB, anchor="middle")

# rigs: (name, q, jx, $/mo hobby, $/mo honest, label-row y)
rigs = [("2×3090",    48, -14,  86, 1111, 380),
        ("RTX 5090",  48,  14, 128, 1153, 400),
        ("Strix Halo", 52, -14,  91, 1116, 360),
        ("DGX Spark",  52,  14, 120, 1145, 340),
        ("Mac 256GB",  53,   0, 193, 1218, 380),
        ("Mac 512GB",  56,   0, 296, 1321, 400)]
for name, q, jx, lo, hi, ry in rigs:          # connectors + poles first
    x = sx(q) + jx
    L(x, sy(lo) - 9, x, sy(hi) + 9, "#deddd6", 1.2, "2 4")
    L(x, ry + 6, x, sy(hi) - 10, POLE, 1)
# plan cluster + zoom-lens card
for d_, r_, jx_ in ((0, 4, -22), (20, 6, 0), (100, 9, -14), (200, 12, 6)):
    C(sx(63) + jx_, sy(d_), r_, BLUE)
scribble(790, 745, 58, 48)
cw_x, cw_y, cw_w, cw_h = 620, 388, 240, 202
L(cw_x + 48, cw_y + cw_h, 768, 692, "#b9b8b2", 1)
L(cw_x + cw_w - 28, cw_y + cw_h, 812, 692, "#b9b8b2", 1)
R(cw_x, cw_y, cw_w, cw_h, "#ffffff", rx=10, extra=f'stroke="{GRID}" stroke-width="1.5"')
T(cw_x + 14, cw_y + 26, "inside that corner — all quality 63:", 12.5, INK, "700")
ty = cw_y + 50
for pr_, lab_, r_ in (("$0", "free tiers", 4), ("$17–20", "Pro / Plus", 6),
                      ("$100", "mid tiers", 9), ("$200", "Max 20x · Pro · Ultra", 12)):
    C(cw_x + 26, ty, r_, BLUE)
    T(cw_x + 46, ty + 4, pr_, 12, INK, "700")
    T(cw_x + 104, ty + 4, lab_, 10.5, SUB)
    ty += 26
L(cw_x + 14, ty - 8, cw_x + cw_w - 14, ty - 8, GRID, 1)
hand(cw_x + 14, ty + 16, "API metered? $14,914/mo —", 15, 0)
hand(cw_x + 14, ty + 38, "10× above this chart ↑", 15, 0)
for name, q, jx, lo, hi, ry in rigs:          # dots over lines
    C(sx(q) + jx, sy(lo), 7, ORANGE)
    C(sx(q) + jx, sy(hi), 7, ORANGE_D)
for name, q, jx, lo, hi, ry in rigs:          # flag-pole labels cap their own line
    T(sx(q) + jx, ry, f"{name} · ${lo:,} → ${hi:,}", 11, INK, "600", "middle", extra=halo())
T(672, 604, "the gap no money closes:", 11.5, MUT, anchor="end",
  extra='font-style="italic" ' + halo(3))
T(672, 620, "more local spend moves you up, not right", 11.5, MUT, anchor="end",
  extra='font-style="italic" ' + halo(3))
hand(720, 768, "the corner you want!", 22, -2, "end")
T(52, py0 + 68, "Reading: every subscription lands bottom-right — cheapest and best quality. The rigs sit 10–15 quality points to the left, and pricing", 12, MUT)
T(52, py0 + 84, "your own hours moves each one up its line to 5.6–6.6× the cost of the top plan. One linked pair = one rig, two prices on your time.", 12, MUT)
T(52, py0 + 108, "Sources — quality: Artificial Analysis Intelligence Index v4.1.1, retrieved Aug 28 2026 · plan prices: Anthropic / OpenAI / Google published tiers, verified Aug 28 2026", 11, MUT)
T(52, py0 + 123, "rig $/mo: this report’s TCO model — 3-yr amortization net of resale, measured power at $0.18–0.40/kWh, labor $0 or $75/h · full workings in the companion report", 11, MUT)

# ---------- S2: rig table ----------
r2_y = 960
header(r2_y, "The rigs behind those dots",
       "Five community builds · hardware at Aug 2026 street prices · $/mo = 3-yr cost, resale- and power-adjusted, your time at $0")
ch_y = r2_y + 54
for cx_, lab_, anc_ in ((52, "RIG", "start"), (320, "HARDWARE", "start"), (445, "MEMORY", "start"),
                        (590, "WHAT IT RUNS", "start"), (888, "$/MO ALL-IN", "end")):
    T(cx_, ch_y, lab_, 10.5, MUT, "700", anc_, extra='letter-spacing="1"')
L(52, ch_y + 10, 888, ch_y + 10, "#b9b8b2", 1.2)
table = [
    ("2× used RTX 3090", "the r/LocalLLaMA classic", "$2,900", "48GB", "27B-class · ~150 tok/s", "$86/mo"),
    ("Strix Halo 128GB", "the 2026 mini-PC wave · GMKtec, Framework", "$3,650", "128GB unified", "120B-class MoE · 35–57 tok/s", "$91/mo"),
    ("DGX Spark", "NVIDIA’s desk AI box", "$4,699", "128GB unified", "120B-class MoE · 39–61 tok/s", "$120/mo"),
    ("RTX 5090 workstation", "the fast lane · card alone $4.3–4.9k", "$8,500", "32GB", "27B-class · 180–420 tok/s", "$128/mo"),
    ("Mac Studio 256–512GB", "the big-memory king · or lease from $210/mo", "$10.8–17.2k", "up to 512GB unified", "GLM-5.3-Flash · DeepSeek-class", "$193–296/mo"),
]
ry0 = r2_y + 84
for i, (nm, tag, hw, mem, runs, pm) in enumerate(table):
    y = ry0 + i * 46
    T(52, y, nm, 15, INK, "700", font=SER_D)
    T(52, y + 15, tag, 10.5, MUT, extra='font-style="italic"')
    T(320, y, hw, 14, ORANGE, "700", font=SER_D)
    T(445, y + 1, mem, 12, SUB)
    T(590, y + 1, runs, 12, SUB)
    T(888, y, pm, 13, INK, "700", "end")
    if i < 4:
        L(52, y + 26, 888, y + 26, GRID, 1)
L(52, ry0 + 4 * 46 + 26, 888, ry0 + 4 * 46 + 26, "#b9b8b2", 1.2)
T(52, ry0 + 236, "The software layer is free and excellent — llama.cpp, Ollama, LM Studio, MLX, vLLM. Open source did the innovating;", 12, SUB)
T(52, ry0 + 253, "the hardware bill above is the part nobody waives.", 12, SUB)
T(52, ry0 + 275, "tok/s = tokens generated per second — 20 is comfortable reading speed; coding agents want hundreds · MoE = mixture-of-experts, big models that run lighter", 10.5, MUT)
T(52, ry0 + 296, "Sources: r/LocalLLaMA build threads · US street &amp; apple.com list / lease prices, Aug 28 2026 · $/mo — companion TCO model (3-yr, resale- &amp; power-adjusted)", 11, MUT)

# ---------- S3: the models ----------
m_y = 1408
header(m_y, "The open models those rigs run — vs the frontier",
       "Artificial Analysis Intelligence Index · higher = smarter · tick = score after the 4-bit compression (‘quantization’) needed to fit desk memory")
rows = [
    ("Claude Opus 5", 63, BLUE, None, "cloud only · in every plan", False),
    ("Kimi K3 · open, 2.8T", 60, ORANGE, None, "no desk can hold it", False),
    ("GLM-5.3 · open, 753B", 60, ORANGE, None, "server-class only", False),
    ("GLM-5.3-Flash", 57, ORANGE, 53, "fits a 256GB Mac", True),
    ("Qwen3.8-Flash-Next", 56, ORANGE, 52, "fits 128GB boxes", False),
    ("Qwen3.8-27B", 52, ORANGE, 48, "fits a 32GB GPU", False),
    ("gpt-oss-120b · 2025 gen", 24, ORANGE, None, "superseded", False),
]
by0, lw = m_y + 52, 300
ppx = (880 - lw - 130) / 70.0
for i, (lab, v, col, tick, note, new) in enumerate(rows):
    y = by0 + i * 43
    T(lw - 10, y + 19, lab, 13.5, INK, "600", "end")
    if new:
        R(lw - 10 - 118 - 46, y + 4, 42, 19, INK, rx=9)
        T(lw - 10 - 118 - 25, y + 18, "NEW", 11, "#ffffff", "700", "middle")
    w_ = v * ppx
    R(lw, y, w_, 27, col, rx=5)
    T(lw + w_ + 8, y + 19, str(v), 14, INK, "700")
    if tick:
        tx = lw + tick * ppx
        L(tx, y - 3, tx, y + 30, INK, 2)
    T(lw + w_ + 34, y + 19, note, 11.5, MUT)
leg_y = by0 + 7 * 43 + 12
R(300, leg_y, 12, 12, BLUE, rx=3); T(318, leg_y + 11, "closed frontier", 12, SUB)
R(430, leg_y, 12, 12, ORANGE, rx=3); T(448, leg_y + 11, "open weights", 12, SUB)
L(560, leg_y, 560, leg_y + 13, INK, 2); T(570, leg_y + 11, "effective after 4-bit quantization", 12, SUB)
hand(330, leg_y + 41, "open models are 3 pts behind — but only at sizes no desk can serve!", 20, -1)
T(52, leg_y + 66, "Source: Artificial Analysis Intelligence Index v4.1.1 (artificialanalysis.ai), retrieved Aug 28 2026 · 4-bit effective score ≈ 93% retention — community quantization evals", 11, MUT)

# ---------- S4: what builders report ----------
b_y = 1900
header(b_y, "What the builders themselves report", "First-hand studies, GitHub issues and forum threads · 2025–2026")
stats = [
    ("2–7 days", "to stand up an agent-grade rig", "(before any real work)"),
    ("7×", "more human interventions than", "Claude in a paired study"),
    ("44×", "one error repeated in a loop —", "the agent never noticed"),
    ("0", "working local replacements found", "by a €440k/yr Claude team, asking publicly"),
]
for i, (big, l1, l2) in enumerate(stats):
    x = (52, 250, 448, 646)[i]
    R(x, b_y + 40, 26, 4, ORANGE)
    T(x, b_y + 76, big, 27, INK, "700", font=SER_D)
    T(x, b_y + 98, l1, 11.5, SUB)
    T(x, b_y + 113, l2, 11.5, SUB)
T(52, b_y + 152, "“Comparing agentic Qwen to Claude Opus is like a junior… versus a senior that thinks.”", 15.5, INK, "400", font=SER, extra='font-style="italic"')
T(52, b_y + 173, "— Mac Studio 128GB owner, Hacker News, June 2026", 11.5, MUT)
T(52, b_y + 195, "Sources: paired-agent field study, Jun 2026 · llama.cpp GitHub issues #20198 &amp; #27406 (closed “not planned”) · Hacker News &amp; r/LocalLLaMA threads, 2025–26", 11, MUT)

# ---------- S5: case study ----------
cs_y = 2148
R(40, cs_y, 860, 400, "#fdf2ec", rx=16, extra=f'stroke="{ORANGE}" stroke-width="1.5"')
T(64, cs_y + 36, "CASE STUDY — THE DEMAND SIDE", 12, ORANGE, "700", extra='letter-spacing="2"')
T(64, cs_y + 70, "Our own month on the $200 plan — measured, not estimated", 23, INK, "700", font=SER_D)
mwx, mwy, mc, mg = 64, cs_y + 96, 13.5, 3.2
for i in range(75):
    r_, c_ = divmod(i, 15)
    R(mwx + c_ * (mc + mg), mwy + r_ * (mc + mg), mc, mc, ORANGE if i == 0 else BLUE_L, rx=3)
T(390, cs_y + 128, "$14,914", 34, INK, "700", font=SER_D)
T(390, cs_y + 148, "API-equivalent consumed", 11.5, MUT)
T(625, cs_y + 128, "$200", 34, ORANGE, "700", font=SER_D)
T(625, cs_y + 148, "actually paid (Max 20x)", 11.5, MUT)
T(790, cs_y + 128, "75×", 34, INK, "700", font=SER_D)
T(790, cs_y + 148, "leverage", 11.5, MUT)
T(64, cs_y + 192, "1 square = $200 of API-equivalent usage · the orange square is all we actually paid — the other 74 came with the subscription", 11.5, SUB, "600")
T(64, cs_y + 210, "14.69B tokens · 71,350 requests · 96% answered from the provider-side cache — economics a local rig cannot replicate", 12, SUB)
# feasibility strip
st_y = cs_y + 252
T(64, st_y, "Compute-hours our month would demand from each rig above", 12.5, INK, "600")
C(604, st_y - 4, 5, GREEN);  T(613, st_y, "fits", 10.5, SUB)
C(650, st_y - 4, 5, YELLOW); T(659, st_y, "tight", 10.5, SUB)
R(701, st_y - 9, 10, 10, RED_S, extra='stroke="#ffffff" stroke-width="1.5"')
T(717, st_y, "over the 720-h month", 10.5, SUB)
ly2 = cs_y + 286
fx0, fx1 = 64, 850
def fx(h): return fx0 + min(h, 1400) * (fx1 - fx0) / 1400.0
L(fx0, ly2, fx1, ly2, "#d9c9bd", 3)
L(fx(720), ly2 - 14, fx(720), ly2 + 42, INK, 2, "5 4")
for h, col, sq in ((143, GREEN, False), (341, YELLOW, False), (692, YELLOW, False),
                   (731, RED_S, True), (1263, RED_S, True)):
    if sq:
        R(fx(h) - 7, ly2 - 7, 14, 14, col, rx=2, extra='stroke="#ffffff" stroke-width="2"')
    else:
        C(fx(h), ly2, 8, col)
for h in (143, 341, 1263):
    T(fx(h), ly2 - 16, f"{h:,}", 11, SUB, "600", "middle")
T(fx(692) - 3, ly2 - 16, "692", 11, SUB, "600", "end")
T(fx(731) + 3, ly2 - 16, "731", 11, SUB, "600", "start")
s.append(f'<path d="M{fx1-6},{ly2-8} l12,8 l-12,8 z" fill="{RED_S}"/>')
T(848, ly2 - 16, "3,817", 11, SUB, "600", "end")
names = (("5090", 143, 18), ("2×3090", 341, 18), ("Mac 256", 692, 32), ("Strix", 1263, 18))
for nm, h, dy in names:
    T(fx(h), ly2 + dy, nm, 10, MUT, "600", "middle", extra=halo(3))
T(fx(731), ly2 + 18, "Spark", 10, MUT, "600", "middle", extra=halo(3))
T(848, ly2 + 18, "Mac 512", 10, MUT, "600", "end")
T(fx(720), ly2 + 56, "the month: 720 h", 10.5, INK, "700", "middle", extra=halo(3))
T(64, cs_y + 364, "No rig on this page could serve our volume at frontier quality — several can’t serve it at all.", 15, INK, "700")
T(64, cs_y + 385, "For a heavy user the plan wins by an order of magnitude; local wins on privacy, API-arbitrage or hobby terms — not on cost-per-quality.", 12.5, SUB)

# ---------- footer ----------
T(W / 2, 2578, "Demand: our own Claude Code transcripts, Jul 29 – Aug 28 2026, deduplicated per request · API-equivalent $ at published per-MTok rates incl. cache-write &amp; cache-read tiers", 11, MUT, anchor="middle")
T(W / 2, 2596, "Hardware, plan &amp; benchmark data primary-source verified Aug 28 2026 · full method, sensitivity &amp; validation in the companion report", 11, MUT, anchor="middle")

# ---------- page ----------
def b64(fn):
    return base64.b64encode(open(fn, "rb").read()).decode()
fraunces, caveat = b64("fraunces-700.woff2"), b64("caveat-700.woff2")
svg = f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;display:block">' + "".join(s) + "</svg>"
page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Real Price of Local AI — Infographic</title>
<style>
@font-face{{font-family:'Fraunces';src:url(data:font/woff2;base64,{fraunces}) format('woff2');font-weight:700 900;font-style:normal;font-display:block}}
@font-face{{font-family:'Caveat';src:url(data:font/woff2;base64,{caveat}) format('woff2');font-weight:700;font-style:normal;font-display:block}}
body{{margin:0;background:#eceae5;display:flex;justify-content:center;padding:26px 10px}}
.poster{{max-width:960px;width:100%;background:#fff;border-radius:8px;
box-shadow:0 10px 40px rgba(0,0,0,.14)}}</style></head>
<body><div class="poster">{svg}</div></body></html>"""
open("infographic3.html", "w").write(page)
print(f"infographic3.html written: {len(page):,} bytes")

canvas_head = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Real Price of Local AI — Infographic</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Caveat:wght@700&family=Fraunces:opsz,wght@9..144,700;9..144,900&display=swap');
body{margin:0;background:#eceae5;display:flex;justify-content:center;padding:26px 10px}
.poster{max-width:960px;width:100%;background:#fff;border-radius:8px;
box-shadow:0 10px 40px rgba(0,0,0,.14)}</style></head>
<body><div class="poster">"""
open("infographic3_canvas.html", "w").write(canvas_head + svg + "</div></body></html>")
print(f"infographic3_canvas.html written: {len(canvas_head + svg) + 22:,} bytes")
