p = 'build_infographic2.py'
src = open(p).read()
def rep(a, b):
    global src
    assert a in src, "MISSING: " + a[:60]
    src = src.replace(a, b)

# ---- rewrite the whole S3 scatter block ----
NEW_S3 = '''# ---------- S3: price vs quality scatter ----------
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
rigs = [("2×3090", 48, 0, 86, 1111, -176), ("RTX 5090", 48, 14, 128, 1153, -152),
        ("Strix Halo", 52, -8, 91, 1116, -176), ("DGX Spark", 52, 10, 120, 1145, -152),
        ("Mac 256GB", 53, 0, 193, 1218, -128), ("Mac 512GB", 56, 0, 296, 1321, -176)]
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
                      ("$100", "mid tiers", 9), ("$200", "Max 20x · GPT Pro · Ultra", 12)):
    s.append(f'<circle cx="{cw_x+26}" cy="{ty}" r="{r_}" fill="{BLUE}" stroke="#ffffff" stroke-width="2"/>')
    T(cw_x + 46, ty + 4, pr_, 12, INK, "700")
    T(cw_x + 104, ty + 4, lab_, 10.5, SUB)
    ty += 26
L(cw_x + 14, ty - 8, cw_x + cw_w - 14, ty - 8, GRID, 1)
hand(cw_x + 14, ty + 14, "API metered? $14,914/mo —", 13.5, 0)
hand(cw_x + 14, ty + 32, "10× above this chart ↑", 13.5, 0)
hand(712, py0 - 8, "the corner you want!", 18, -2, "end")
arrow(718, py0 - 14, 736, py0 - 30, bend=6)
T(52, py0 + 68, "Reading: every plan lands in the bottom-right corner — cheapest and best quality. What a desk rig can serve sits 10–15 quality points left;", 12, MUT)
T(52, py0 + 84, "price your own hours and it costs 5.6–6.6× the top plan. Each linked pair is one rig making that jump.", 12, MUT)
T(52, py0 + 108, "Sources — quality: Artificial Analysis Intelligence Index v4.1.1 (artificialanalysis.ai), retrieved Aug 28 2026 · plan prices: published Anthropic / OpenAI / Google tiers, verified Aug 28 2026 ·", 10, MUT)
T(52, py0 + 122, "rig $/mo: this report’s TCO model — 3-yr amortization net of resale, measured power at $0.18–0.40/kWh, labor $0 or $75/h · full workings in the companion report", 10, MUT)

'''
i0 = src.index("# ---------- S3")
i1 = src.index("# ---------- S4")
src = src[:i0] + NEW_S3 + src[i1:]

# ---- S1 source line ----
rep("# ---------- S2: the models ----------",
    'T(52, 574, "Sources: r/LocalLLaMA build threads · US retailer street prices &amp; apple.com list / Apple Upgrade lease pricing, Aug 28 2026 · $/mo — companion TCO model (3-yr, resale- &amp; power-adjusted)", 10, MUT)\n\n'
    "# ---------- S2: the models ----------")

# ---- S2 source line ----
rep('hand(330, leg_y + 37, "open models are 3 pts behind — but only at sizes no desk can serve!", 17, -1)',
    'hand(330, leg_y + 37, "open models are 3 pts behind — but only at sizes no desk can serve!", 17, -1)\n'
    'T(52, leg_y + 60, "Source: Artificial Analysis Intelligence Index v4.1.1 (artificialanalysis.ai), retrieved Aug 28 2026 · 4-bit effective score ≈ 93% retention — community quantization evals", 10, MUT)')

# ---- S4 source line ----
rep('T(52, b_y + 186, "— Mac Studio 128GB owner, HN, June 2026 · Team scale: a €440k/yr Claude shop publicly asked for one working local replacement — got none.", 11.5, MUT)',
    'T(52, b_y + 186, "— Mac Studio 128GB owner, HN, June 2026 · Team scale: a €440k/yr Claude shop publicly asked for one working local replacement — got none.", 11.5, MUT)\n'
    'T(52, b_y + 206, "Sources: paired-agent field study, Jun 2026 · llama.cpp GitHub issues #20198 &amp; #27406 (closed “not planned”) · Hacker News &amp; r/LocalLLaMA threads, 2025–26", 10, MUT)')

# ---- footer: split into two explicit citation lines ----
rep('T(W / 2, 2300, "Demand measured from our Claude Code transcripts · Jul 29 – Aug 28, 2026 · prices, benchmarks &amp; throughput primary-source verified Aug 28, 2026 · methodology in companion report",\n  10.5, MUT, anchor="middle")',
    'T(W / 2, 2294, "Demand: our own Claude Code transcripts, Jul 29 – Aug 28 2026, deduplicated per request · API-equivalent $ at published per-MTok rates incl. cache-write &amp; cache-read tiers", 10.5, MUT, anchor="middle")\n'
    'T(W / 2, 2312, "Hardware, plan &amp; benchmark data primary-source verified Aug 28 2026 · full method, sensitivity &amp; validation in the companion report", 10.5, MUT, anchor="middle")')

open(p, 'w').write(src)
print("patched ok,", len(src), "bytes")
