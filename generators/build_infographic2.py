#!/usr/bin/env python3
"""Infographic v2 — market-first: rigs people build, models they run, cost-per-quality
vs subscription plans; our own usage as closing case study."""

W, H = 940, 2340
INK, SUB, MUT, GRID = "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
BLUE, BLUE_L, BLUE_D = "#2a78d6", "#9ec5f4", "#104281"
ORANGE, ORANGE_D = "#eb6834", "#b34418"
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
    T(78, y, title, 26, INK, "700", font=SER)
    T(52, y + 24, caption, 13, MUT)
def hand(x, y, txt, size=20, rot=-3, anchor="start"):
    T(x, y, txt, size, RED, "700", anchor, HAND, f'transform="rotate({rot} {x} {y})"')
def scribble(cx, cy, rx, ry):
    s.append(f'<path d="M{cx-rx},{cy} C{cx-rx},{cy-ry*1.25} {cx+rx*0.9},{cy-ry*1.3} {cx+rx},{cy-ry*0.15} '
             f'C{cx+rx*1.08},{cy+ry} {cx-rx*0.8},{cy+ry*1.3} {cx-rx*1.06},{cy+ry*0.25}" '
             f'fill="none" stroke="{RED}" stroke-width="3" stroke-linecap="round"/>')
def arrow(x1, y1, x2, y2, bend=30):
    mx, my = (x1 + x2) / 2 + bend, (y1 + y2) / 2
    s.append(f'<path d="M{x1},{y1} Q{mx},{my} {x2},{y2}" fill="none" stroke="{RED}" '
             f'stroke-width="3" stroke-linecap="round" marker-end="url(#ah)"/>')

s.append(f'<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" '
         f'markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{RED}"/></marker></defs>')
R(0, 0, W, H, "#ffffff")

# ---------- title ----------
R(50, 42, 30, 30, ORANGE)
T(94, 68, "The Real Price of Local AI", 44, INK, "700", font=SER)
T(52, 100, "The rigs people build, the open models they run — incl. the weeks-old GLM-5.3-Flash — and what quality", 14.5, SUB)
T(52, 120, "actually costs per month, next to simply subscribing · primary-source data, Aug 28, 2026", 14.5, SUB)

# ---------- S1: the rigs ----------
header(170, "The rigs people actually build", "Six community answers to “run it at home” · $/mo = 3-yr amortization net of resale + power, your time at $0")
cards = [
    ("the r/LocalLLaMA classic", "2× used RTX 3090", "$2,900", "48GB VRAM", "Qwen3.8-27B 4-bit · ~150 t/s", "$86/mo"),
    ("the 2026 mini-PC wave", "Strix Halo 128GB", "$3,650", "128GB unified · GMKtec, Framework", "120B-class MoE · 35–57 t/s", "$91/mo"),
    ("NVIDIA's desk AI box", "DGX Spark", "$4,699", "128GB · fastest small-box prefill", "120B-class MoE · 39–61 t/s", "$120/mo"),
    ("the fast lane", "RTX 5090 workstation", "$8,500", "32GB VRAM · card alone $4.3–4.9k", "27B models · 180–420 t/s", "$128/mo"),
    ("the big-memory king", "Mac Studio 256–512GB", "$10.8–17.2k", "up to 512GB unified · or lease $210/mo", "GLM-5.3-Flash · DeepSeek-class", "$193–296/mo"),
    ("the software (all free)", "llama.cpp · Ollama", "$0", "LM Studio · MLX · vLLM", "open source — the real innovation", "—"),
]
for i, (tag, name, price, l1, l2, permo) in enumerate(cards):
    r_, c_ = divmod(i, 3)
    cx0, cy0 = 52 + c_ * 296, 210 + r_ * 172
    R(cx0, cy0, 280, 160, "#f6f5f2", rx=12)
    T(cx0 + 18, cy0 + 26, tag, 11, MUT, "600", extra='font-style="italic"')
    T(cx0 + 18, cy0 + 52, name, 19, INK, "700", font=SER)
    T(cx0 + 18, cy0 + 84, price, 26, ORANGE, "700", font=SER)
    T(cx0 + 18, cy0 + 108, l1, 12, SUB)
    T(cx0 + 18, cy0 + 126, l2, 12, SUB)
    if permo != "—":
        T(cx0 + 18, cy0 + 148, permo + " to own & run", 13, INK, "700")

T(52, 574, "Sources: r/LocalLLaMA build threads · US street &amp; apple.com list / lease prices, Aug 28 2026 · $/mo — companion TCO model (3-yr, resale- &amp; power-adjusted)", 10, MUT)

# ---------- S2: the models ----------
m_y = 620
header(m_y, "The open models they run — vs the frontier",
       "Artificial Analysis Intelligence Index · independent, same harness · tick = effective score after the 4-bit quantization needed to fit")
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
        R(lw - 10 - 118 - 46, y + 4, 42, 19, GREEN, rx=9)
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
hand(330, leg_y + 37, "open models are 3 pts behind — but only at sizes no desk can serve!", 17, -1)
T(52, leg_y + 60, "Source: Artificial Analysis Intelligence Index v4.1.1 (artificialanalysis.ai), retrieved Aug 28 2026 · 4-bit effective score ≈ 93% retention — community quantization evals", 10, MUT)

# ---------- S3: price vs quality scatter ----------
sc_y = 1080
header(sc_y, "Price vs quality — the whole market on one chart",
       "Monthly cost vs. the quality you actually get · every local rig appears twice — linked dots, two prices on your time")
lgy = sc_y + 48
for lx, col, lab in ((52, BLUE, "subscription plan (dot size = price)"),
                     (332, ORANGE, "local rig · your time at $0"),
                     (542, ORANGE_D, "local rig · time at $75/h")):
    s.append(f'<circle cx="{lx+8}" cy="{lgy}" r="7" fill="{col}" stroke="#ffffff" stroke-width="2"/>')
    T(lx + 22, lgy + 4, lab, 11.5, SUB, "600")
L(744, lgy - 8, 744, lgy + 8, "#b3b2ab", 1.5, "2 3")
T(756, lgy + 4, "same rig, linked", 11.5, SUB, "600")
px0, px1 = 130, 850
py1, py0 = sc_y + 96, sc_y + 376
def sx(q): return px0 + (q - 45) * (px1 - px0) / 20.0
def sy(d): return py0 - d * (py0 - py1) / 1500.0
for d in (0, 500, 1000, 1500):
    L(px0 - 10, sy(d), px1 + 10, sy(d), GRID, 1, "3 5")
    T(px0 - 16, sy(d) + 4, f"${d:,}", 11, MUT, anchor="end")
for q in (45, 50, 55, 60, 65):
    T(sx(q), py0 + 20, str(q), 11.5, MUT, anchor="middle")
    L(sx(q), py0, sx(q), py0 + 5, "#b9b8b2", 1.2)
L(px0 - 10, py0, px1 + 10, py0, "#b9b8b2", 1.5)
T((px0 + px1) / 2, py0 + 42, "quality · Artificial Analysis Intelligence Index (local = effective score after 4-bit quantization)", 12, SUB, anchor="middle")
def dot(q, d, col, r_=7, jx=0):
    s.append(f'<circle cx="{sx(q)+jx:.0f}" cy="{sy(d):.0f}" r="{r_}" fill="{col}" stroke="#ffffff" stroke-width="2"/>')
# six rigs, each twice: linked pair, one mid-connector label carrying both prices
rigs = [("2×3090", 48, 0, 86, 1111, -176), ("RTX 5090", 48, 14, 128, 1153, -154),
        ("Strix Halo", 52, -8, 91, 1116, -132), ("DGX Spark", 52, 10, 120, 1145, -110),
        ("Mac 256GB", 53, 0, 193, 1218, -176), ("Mac 512GB", 56, 0, 296, 1321, -154)]
for name, q, jx, lo, hi, ly in rigs:
    x = sx(q) + jx
    L(x, sy(lo) - 9, x, sy(hi) + 9, "#deddd6", 1.2, "2 4")
for name, q, jx, lo, hi, ly in rigs:
    dot(q, lo, ORANGE, 7, jx)
    dot(q, hi, ORANGE_D, 7, jx)
for name, q, jx, lo, hi, ly in rigs:
    T(sx(q) + jx, py0 + ly, f"{name} · ${lo:,} → ${hi:,}", 10.8, INK, "600", "middle",
      extra='paint-order="stroke" stroke="#ffffff" stroke-width="4"')
# plan cluster (all quality 63) + zoom-lens card replacing the old leader-line fan
for d_, r_, jx_ in ((0, 4, -22), (20, 6, 0), (100, 9, -14), (200, 12, 6)):
    dot(63, d_, BLUE, r_, jx_)
scribble(sx(63) - 2, sy(95), 52, 42)
cw_x, cw_y, cw_w, cw_h = 620, py1 + 18, 234, 194
L(cw_x + 44, cw_y + cw_h, 752, py0 - 56, "#b9b8b2", 1)
L(cw_x + cw_w - 24, cw_y + cw_h, 806, py0 - 56, "#b9b8b2", 1)
R(cw_x, cw_y, cw_w, cw_h, "#ffffff", rx=10, extra=f'stroke="{GRID}" stroke-width="1.5"')
T(cw_x + 14, cw_y + 26, "inside that corner — all quality 63:", 12.5, INK, "700")
ty = cw_y + 50
for pr_, lab_, r_ in (("$0", "free tiers", 4), ("$17–20", "Pro / Plus", 6),
                      ("$100", "mid tiers", 9), ("$200", "Max 20x · Pro · Ultra", 12)):
    s.append(f'<circle cx="{cw_x+26}" cy="{ty}" r="{r_}" fill="{BLUE}" stroke="#ffffff" stroke-width="2"/>')
    T(cw_x + 46, ty + 4, pr_, 12, INK, "700")
    T(cw_x + 104, ty + 4, lab_, 10.5, SUB)
    ty += 26
L(cw_x + 14, ty - 8, cw_x + cw_w - 14, ty - 8, GRID, 1)
hand(cw_x + 14, ty + 14, "API metered? $14,914/mo —", 13.5, 0)
hand(cw_x + 14, ty + 32, "10× above this chart ↑", 13.5, 0)
hand(712, py0 - 8, "the corner you want!", 18, -2, "end")
T(52, py0 + 68, "Reading: every plan lands in the bottom-right corner — cheapest and best quality. What a desk rig can serve sits 10–15 quality points left;", 12, MUT)
T(52, py0 + 84, "price your own hours and it costs 5.6–6.6× the top plan. Each linked pair is one rig making that jump.", 12, MUT)
T(52, py0 + 108, "Sources — quality: Artificial Analysis Intelligence Index v4.1.1, retrieved Aug 28 2026 · plan prices: Anthropic / OpenAI / Google published tiers, verified Aug 28 2026", 10, MUT)
T(52, py0 + 122, "rig $/mo: this report’s TCO model — 3-yr amortization net of resale, measured power at $0.18–0.40/kWh, labor $0 or $75/h · full workings in the companion report", 10, MUT)

# ---------- S4: what builders report ----------
b_y = 1652
header(b_y, "What the builders themselves report", "First-hand studies, GitHub issues and forum reports · 2025–2026")
tiles = [("\U0001F9F0", "a weekend to a week", "just to set up an agent-grade rig"),
         ("\U0001F501", "7× interventions", "vs 1 for Claude · controlled study"),
         ("\U0001FAA4", "44× same-error loop", "agent never noticed it was stuck"),
         ("\U0001F9E9", "tool-calls break", "quantization breaks agent formatting")]
for i, (ico, big, small) in enumerate(tiles):
    cx0 = 52 + i * 222
    R(cx0, b_y + 32, 210, 100, "#f6f5f2", rx=12)
    T(cx0 + 16, b_y + 68, ico, 24)
    T(cx0 + 16, b_y + 96, big, 15.5, INK, "700")
    T(cx0 + 16, b_y + 114, small, 10.8, SUB)
T(52, b_y + 166, "“Comparing agentic Qwen to Claude Opus is like a junior… versus a senior that thinks.”", 15, INK, "400", font=SER, extra='font-style="italic"')
T(52, b_y + 186, "— Mac Studio 128GB owner, HN, June 2026 · Team scale: a €440k/yr Claude shop publicly asked for one working local replacement — got none.", 11.5, MUT)
T(52, b_y + 206, "Sources: paired-agent field study, Jun 2026 · llama.cpp GitHub issues #20198 &amp; #27406 (closed “not planned”) · Hacker News &amp; r/LocalLLaMA threads, 2025–26", 10, MUT)

# ---------- S5: case study ----------
cs_y = 1880
R(40, cs_y, 860, 372, "#fdf2ec", rx=16, extra=f'stroke="{ORANGE}" stroke-width="1.5"')
T(64, cs_y + 38, "CASE STUDY", 12, ORANGE, "700", extra='letter-spacing="2"')
T(64, cs_y + 72, "Our own month on the $200 plan — measured, not estimated", 24, INK, "700", font=SER)
# mini waffle
mwx, mwy, mc, mg = 64, cs_y + 100, 13.5, 3.2
for i in range(75):
    r_, c_ = divmod(i, 15)
    R(mwx + c_ * (mc + mg), mwy + r_ * (mc + mg), mc, mc, ORANGE if i == 0 else BLUE_L, rx=3)
T(mwx, mwy + 105, "14.69B tokens · 71,350 requests · 96% served from provider cache", 12, SUB)
T(390, cs_y + 128, "$14,914", 34, INK, "700", font=SER)
T(390, cs_y + 148, "API-equivalent consumed", 11.5, MUT)
T(620, cs_y + 128, "$200", 34, ORANGE, "700", font=SER)
T(620, cs_y + 148, "actually paid (Max 20x)", 11.5, MUT)
T(780, cs_y + 128, "75×", 34, INK, "700", font=SER)
T(780, cs_y + 148, "leverage", 11.5, MUT)
# feasibility dot strip
T(64, cs_y + 240, "Compute-hours our month would demand from each rig above (a month has 720):", 12.5, INK, "600")
ly2 = cs_y + 272
fx0, fx1 = 64, 850
def fx(h): return fx0 + min(h, 1400) * (fx1 - fx0) / 1400.0
L(fx0, ly2, fx1, ly2, "#d9c9bd", 3)
L(fx(720), ly2 - 14, fx(720), ly2 + 14, INK, 2, "5 4")
T(fx(720), ly2 + 30, "720 h", 11.5, INK, "700", "middle")
for h, col in ((143, GREEN), (341, YELLOW), (692, YELLOW), (731, RED), (1263, RED)):
    s.append(f'<circle cx="{fx(h):.0f}" cy="{ly2}" r="8" fill="{col}" stroke="#ffffff" stroke-width="2"/>')
for h in (143, 341, 1263):
    T(fx(h), ly2 - 16, str(h), 11, SUB, "600", "middle")
T(fx(711), ly2 - 16, "692 · 731", 11, SUB, "600", "middle")
s.append(f'<path d="M{fx1-6},{ly2-8} l12,8 l-12,8 z" fill="{RED}"/>')
T(850, ly2 + 30, "3,817 → (Mac 512 · DeepSeek-class)", 11, SUB, "600", "end")
T(64, cs_y + 328, "No rig on this page could serve our volume at frontier quality — several can't serve it at all.", 15, INK, "700")
T(64, cs_y + 349, "For a heavy user the plan wins by an order of magnitude; local wins on privacy, API-arbitrage or hobby terms — not on cost-per-quality.", 12.5, SUB)

T(W / 2, 2294, "Demand: our own Claude Code transcripts, Jul 29 – Aug 28 2026, deduplicated per request · API-equivalent $ at published per-MTok rates incl. cache-write &amp; cache-read tiers", 10.5, MUT, anchor="middle")
T(W / 2, 2312, "Hardware, plan &amp; benchmark data primary-source verified Aug 28 2026 · full method, sensitivity &amp; validation in the companion report", 10.5, MUT, anchor="middle")

svg = f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;display:block">' + "".join(s) + "</svg>"
page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Real Price of Local AI — Infographic</title>
<style>body{{margin:0;background:#eceae5;display:flex;justify-content:center;padding:26px 10px}}
.poster{{max-width:960px;width:100%;background:#fff;border-radius:8px;
box-shadow:0 10px 40px rgba(0,0,0,.14)}}</style></head>
<body><div class="poster">{svg}</div></body></html>"""
open("infographic2.html", "w").write(page)
print(f"infographic2.html written: {len(page):,} bytes")
