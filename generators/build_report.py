#!/usr/bin/env python3
"""Builds report.html — local vs cloud true-cost/efficacy analysis."""
import html as H

# ---------------- palette (dataviz reference instance) ----------------
C = dict(s1="#2a78d6", s2="#eb6834", s3="#1baf7a", s4="#eda100",
         crit="#d03b3b", good="#0ca30c", warn="#fab219",
         ink="#0b0b0b", ink2="#52514e", mut="#898781",
         grid="#e1e0d9", base="#c3c2b7", surf="#fcfcfb", page="#f9f9f7")

FONT = 'system-ui,-apple-system,"Segoe UI",sans-serif'

# ---------------- data ----------------
usage_by_model = [  # (label, $, out-tokens M)
    ("Claude Fable 5", 7475, 18.2), ("Claude Opus 5", 5799, 13.1),
    ("Claude Opus 4.8", 1200, 7.5), ("Claude Sonnet 5", 441, 0.8)]

feas = [  # (label, base_h, opt_h, pess_h, class) class: ok|sat|imp
    ("RTX 5090 wkstn — Qwen3.8-27B", 143, 113, 234, "ok"),
    ("2× used RTX 3090 — Qwen3.8-27B", 341, 243, 636, "sat"),
    ("Mac Studio M5 Ultra 256GB — GLM-5.3-Flash", 692, 496, 1282, "sat"),
    ("DGX Spark 128GB — Qwen3.8-Flash-Next", 731, 553, 1267, "imp"),
    ("Strix Halo 128GB — Qwen3.8-Flash-Next", 1263, 906, 2334, "imp"),
    ("Mac M5 Ultra 512GB — DeepSeek V4 / Kimi K3", 3817, 2784, 6918, "imp")]

tco = [  # (label, amort, capital, elec, labor, feasible-class)
    ("2× used RTX 3090 (~$2.9k)", 40, 12, 34, 1025, "sat"),
    ("Strix Halo 128GB ($3.65k)", 61, 15, 15, 1025, "imp"),
    ("DGX Spark 128GB ($4.7k)", 78, 20, 22, 1025, "imp"),
    ("RTX 5090 workstation ($8.5k)", 71, 35, 22, 1025, "ok"),
    ("Mac M5 Ultra 256GB ($10.8k)", 120, 45, 28, 1025, "sat"),
    ("Mac M5 Ultra 512GB (~$17.2k)", 191, 72, 33, 1025, "imp")]

quality = [  # (label, score, kind cloud|open, local_eff or None, note)
    ("Claude Opus 5 (your main driver)", 63, "closed", None, ""),
    ("Claude Fable 5", 62, "closed", None, ""),
    ("Kimi K3 — open, 2.8T params", 60, "open", None, "≫1TB: not desk-runnable"),
    ("GLM-5.3 — open, 753B", 60, "open", None, "~400GB+: not desk-runnable"),
    ("GLM-5.3-Flash @ 256GB Mac", 57, "open", 53, "4-bit ≈93% retention"),
    ("Qwen3.8-Flash-Next @ 128GB", 56, "open", 52, "4-bit ≈93% retention"),
    ("Qwen3.8-27B @ 32GB GPU", 52, "open", 48, "4-bit; needs xhigh effort"),
    ("gpt-oss-120b (2025 gen)", 24, "open", None, "superseded")]

CLASS_TXT = {"ok": "workable", "sat": "saturated", "imp": "impossible"}
CLASS_COL = {"ok": C["good"], "sat": C["warn"], "imp": C["crit"]}

def fmt(n): return f"{n:,.0f}"

# ---------------- svg helpers ----------------
def hbar_chart(items, vmax, width=780, bar_h=26, gap=14, label_w=300,
               refline=None, unit="", tick_step=None, clip=None):
    """items: (label, value, color, endlabel, tooltip, marker_or_None)"""
    n = len(items); ph = n * (bar_h + gap) + 30
    pw = width - label_w - 70
    out = [f'<svg viewBox="0 0 {width} {ph}" role="img" style="width:100%;height:auto">']
    # grid
    if tick_step:
        v = 0
        while v <= vmax:
            x = label_w + pw * v / vmax
            out.append(f'<line x1="{x:.1f}" y1="0" x2="{x:.1f}" y2="{ph-26}" stroke="{C["grid"]}" stroke-width="1"/>')
            out.append(f'<text x="{x:.1f}" y="{ph-10}" font-size="11" fill="{C["mut"]}" text-anchor="middle">{fmt(v)}{unit}</text>')
            v += tick_step
    for i, (lab, val, col, endlab, tip, marker) in enumerate(items):
        y = i * (bar_h + gap) + 6
        w = pw * min(val, clip or vmax) / vmax
        clipped = clip and val > clip
        out.append(f'<text x="{label_w-10}" y="{y+bar_h/2+4}" font-size="12.5" fill="{C["ink"]}" text-anchor="end">{H.escape(lab)}</text>')
        out.append(f'<g class="bar"><title>{H.escape(tip)}</title>'
                   f'<rect x="{label_w}" y="{y}" width="{max(w,2):.1f}" height="{bar_h}" fill="{col}" rx="4"/>' +
                   (f'<path d="M{label_w+w-1:.1f},{y} l8,{bar_h/2} l-8,{bar_h/2}" fill="{C["surf"]}"/>' if clipped else '') +
                   f'<text x="{label_w+w+8:.1f}" y="{y+bar_h/2+4}" font-size="12" font-weight="600" fill="{C["ink"]}">{endlab}</text></g>')
        if marker is not None:  # (value,label) tick marker
            mx = label_w + pw * marker[0] / vmax
            out.append(f'<g><title>{H.escape(marker[1])}</title>'
                       f'<line x1="{mx:.1f}" y1="{y-3}" x2="{mx:.1f}" y2="{y+bar_h+3}" stroke="{C["ink"]}" stroke-width="2"/></g>')
    if refline:
        rx = label_w + pw * refline[0] / vmax
        out.append(f'<line x1="{rx:.1f}" y1="0" x2="{rx:.1f}" y2="{ph-26}" stroke="{C["ink"]}" stroke-width="1.5" stroke-dasharray="5 4"/>')
        out.append(f'<text x="{rx+6:.1f}" y="14" font-size="11.5" font-weight="600" fill="{C["ink"]}">{H.escape(refline[1])}</text>')
    out.append('</svg>')
    return "".join(out)

def stacked_chart(items, vmax, width=780, bar_h=28, gap=16, label_w=250):
    segcols = [C["s1"], C["s2"], C["s3"], C["s4"]]
    segnames = ["hardware amortisation", "capital charge (5%/yr)", "electricity", "labor (setup+maint+babysit @ $75/h)"]
    n = len(items); ph = n * (bar_h + gap) + 46
    pw = width - label_w - 90
    out = [f'<svg viewBox="0 0 {width} {ph}" role="img" style="width:100%;height:auto">']
    for v in range(0, int(vmax) + 1, 300):
        x = label_w + pw * v / vmax
        out.append(f'<line x1="{x:.1f}" y1="16" x2="{x:.1f}" y2="{ph-26}" stroke="{C["grid"]}" stroke-width="1"/>')
        out.append(f'<text x="{x:.1f}" y="{ph-10}" font-size="11" fill="{C["mut"]}" text-anchor="middle">${fmt(v)}</text>')
    for i, (lab, a, cp, e, l, cls) in enumerate(items):
        y = i * (bar_h + gap) + 22
        total = a + cp + e + l
        out.append(f'<text x="{label_w-10}" y="{y+bar_h/2+4}" font-size="12.5" fill="{C["ink"]}" text-anchor="end">{H.escape(lab)}</text>')
        x = label_w
        for val, col, nm in zip((a, cp, e, l), segcols, segnames):
            w = pw * val / vmax
            out.append(f'<g class="bar"><title>{H.escape(lab)} — {nm}: ${fmt(val)}/mo</title>'
                       f'<rect x="{x:.1f}" y="{y}" width="{max(w-2,1):.1f}" height="{bar_h}" fill="{col}" rx="3"/></g>')
            x += w
        badge = CLASS_TXT[cls]
        out.append(f'<text x="{x+8:.1f}" y="{y+bar_h/2-3}" font-size="12" font-weight="600" fill="{C["ink"]}">${fmt(total)}</text>')
        out.append(f'<text x="{x+8:.1f}" y="{y+bar_h/2+11}" font-size="10.5" fill="{CLASS_COL[cls]}">&#9679; {badge}</text>')
    # $200 reference
    rx = label_w + pw * 200 / vmax
    out.append(f'<line x1="{rx:.1f}" y1="16" x2="{rx:.1f}" y2="{ph-26}" stroke="{C["ink"]}" stroke-width="1.5" stroke-dasharray="5 4"/>')
    out.append(f'<text x="{rx:.1f}" y="12" font-size="11.5" font-weight="600" fill="{C["ink"]}" text-anchor="middle">$200 = Max 20x / ChatGPT Pro / AI Ultra</text>')
    out.append('</svg>')
    # legend
    leg = '<div class="legend">' + "".join(
        f'<span><i style="background:{c}"></i>{n}</span>' for c, n in zip(segcols, segnames)) + '</div>'
    return "".join(out) + leg

# ---------------- charts ----------------
chart_usage = hbar_chart(
    [(l, v, C["s1"], f"${fmt(v)}", f"{l}: ${fmt(v)}/mo API-equivalent, {m}M output tokens", None)
     for l, v, m in usage_by_model],
    vmax=8000, label_w=200, tick_step=2000, unit="")

chart_feas = hbar_chart(
    [(l, b, CLASS_COL[c], (f"{fmt(b)} h" + (" &#8594;" if b > 1400 else "")),
      f"{l}: base {fmt(b)} h/mo (range {fmt(o)}–{fmt(p)} h across 5–25% KV-miss)", None)
     for l, b, o, p, c in feas],
    vmax=1400, label_w=330, tick_step=350, unit="h", clip=1400,
    refline=(720, "720 h = running 24/7"))

chart_tco = stacked_chart(tco, vmax=1500)

chart_quality = hbar_chart(
    [(l, s, (C["s1"] if k == "closed" else C["s2"]),
      f"{s}" + (f" &#183; &#8776;{le} local" if le else ""),
      f"{l}: AA Intelligence Index {s} (cloud-served, full precision)" + (f"; ≈{le} effective after 4-bit local quantization" if le else f". {n}" if n else ""),
      ((le, f"≈{le} after 4-bit quantization") if le else None))
     for l, s, k, le, n in quality],
    vmax=70, label_w=300, tick_step=10)

leg_quality = ('<div class="legend"><span><i style="background:' + C["s1"] + '"></i>closed frontier (cloud only)</span>'
               '<span><i style="background:' + C["s2"] + '"></i>open weights</span>'
               '<span><i style="background:' + C["ink"] + ';height:12px;width:2px"></i>effective score after 4-bit local quantization</span></div>')

# ---------------- html ----------------
def sec(title, body, kicker=""):
    k = f'<div class="kicker">{kicker}</div>' if kicker else ''
    return f'<section>{k}<h2>{title}</h2>{body}</section>'

page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Local vs Cloud — True Cost &amp; Efficacy</title>
<style>
:root {{ color-scheme: light; }}
* {{ box-sizing: border-box; margin: 0; }}
body {{ font-family:{FONT}; background:{C['page']}; color:{C['ink']};
  line-height:1.55; padding:34px 18px 60px; }}
.wrap {{ max-width: 880px; margin: 0 auto; }}
h1 {{ font-size: 27px; letter-spacing:-.02em; margin-bottom:6px; }}
h2 {{ font-size: 19px; margin: 0 0 10px; letter-spacing:-.01em; }}
h3 {{ font-size: 14.5px; margin: 16px 0 6px; }}
.sub {{ color:{C['ink2']}; font-size:13.5px; margin-bottom:24px; }}
.kicker {{ font-size:11px; font-weight:700; letter-spacing:.09em; text-transform:uppercase; color:{C['s1']}; margin-bottom:4px; }}
section {{ background:{C['surf']}; border:1px solid rgba(11,11,11,.10); border-radius:10px;
  padding:22px 24px; margin-bottom:18px; }}
p, li {{ font-size: 13.5px; color:{C['ink']}; }}
p {{ margin: 8px 0; }}
ul {{ margin: 8px 0 8px 20px; }}
li {{ margin: 3px 0; }}
.tiles {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:12px; margin:16px 0 8px; }}
.tile {{ background:{C['surf']}; border:1px solid rgba(11,11,11,.10); border-radius:10px; padding:14px 16px; }}
.tile .v {{ font-size:24px; font-weight:700; letter-spacing:-.02em; }}
.tile .l {{ font-size:11.5px; color:{C['ink2']}; margin-top:2px; }}
table {{ border-collapse:collapse; width:100%; font-size:12.5px; margin:10px 0; }}
th {{ text-align:left; font-size:11px; text-transform:uppercase; letter-spacing:.05em;
  color:{C['mut']}; font-weight:600; padding:6px 10px 6px 0; border-bottom:1px solid {C['base']}; }}
td {{ padding:6px 10px 6px 0; border-bottom:1px solid {C['grid']}; vertical-align:top; }}
td.num, th.num {{ text-align:right; font-variant-numeric:tabular-nums; }}
.legend {{ display:flex; flex-wrap:wrap; gap:14px; font-size:11.5px; color:{C['ink2']}; margin-top:6px; }}
.legend i {{ display:inline-block; width:11px; height:11px; border-radius:3px; margin-right:5px; vertical-align:-1px; }}
.note {{ font-size:12px; color:{C['ink2']}; background:{C['page']}; border-left:3px solid {C['s1']};
  padding:8px 12px; border-radius:0 6px 6px 0; margin:10px 0; }}
.warnbox {{ border-left-color:{C['crit']}; }}
.bar:hover rect {{ opacity:.82; }}
.tag {{ display:inline-block; font-size:10.5px; font-weight:700; padding:1px 8px; border-radius:99px; margin-left:6px; vertical-align:2px; }}
.verdict {{ font-size:14.5px; }}
.small {{ font-size:11.5px; color:{C['mut']}; }}
a {{ color:{C['s1']}; }}
@media (prefers-color-scheme: dark) {{
 :root {{ color-scheme: dark; }}
 body {{ background:#0d0d0d; color:#fff; }}
 section, .tile {{ background:#1a1a19; border-color:rgba(255,255,255,.10); }}
 .sub, .tile .l, .legend, .note, p, li {{ color:#c3c2b7; }}
 p, li, .tile .v, h1, h2, h3 {{ color:#fff; }}
 td {{ border-color:#2c2c2a; }} th {{ border-color:#383835; }}
 .note {{ background:#111110; }}
 svg text {{ fill:#c3c2b7; }}
}}
</style></head><body><div class="wrap">

<h1>Local models vs cloud frontier: a true-cost &amp; efficacy analysis</h1>
<div class="sub">Built on <b>your measured Claude Code usage</b> (last 30 days, 2026-07-29 &#8594; 08-28) and primary-source pricing
verified 2026-08-28. Amortized hardware, electricity, labor, residual value, sensitivity analysis and validation included.
Plan detected: <b>Claude Max 20x, $200/mo</b> (billed via Apple, extra-usage enabled).</div>

<div class="tiles">
 <div class="tile"><div class="v">$14,914</div><div class="l">API-equivalent value consumed /mo (list prices)</div></div>
 <div class="tile"><div class="v">$200</div><div class="l">what you actually pay (Max 20x)</div></div>
 <div class="tile"><div class="v">75&#215;</div><div class="l">subscription leverage</div></div>
 <div class="tile"><div class="v">14.69B</div><div class="l">tokens processed /mo &#183; 96% from prompt cache</div></div>
 <div class="tile"><div class="v">71,350</div><div class="l">requests /mo &#183; 31 active days</div></div>
</div>

{sec("Your workload, measured", f'''
<p>Parsed from local Claude Code transcripts (2,317 JSONL files, deduplicated by message + request ID) — the same data behind <code>/usage</code>:</p>
<table>
<tr><th>Last 30 days</th><th class="num">Input (uncached)</th><th class="num">Cache write</th><th class="num">Cache read</th><th class="num">Output</th><th class="num">API-equiv $</th></tr>
<tr><td>Claude Fable 5</td><td class="num">0.1M</td><td class="num">89.8M</td><td class="num">4,868M</td><td class="num">18.2M</td><td class="num">$7,475</td></tr>
<tr><td>Claude Opus 5</td><td class="num">0.4M</td><td class="num">319.3M</td><td class="num">6,599M</td><td class="num">13.1M</td><td class="num">$5,799</td></tr>
<tr><td>Claude Opus 4.8</td><td class="num">0.3M</td><td class="num">40.5M</td><td class="num">1,346M</td><td class="num">7.5M</td><td class="num">$1,200</td></tr>
<tr><td>Claude Sonnet 5</td><td class="num">0.2M</td><td class="num">62.1M</td><td class="num">1,326M</td><td class="num">0.8M</td><td class="num">$441</td></tr>
<tr><td><b>Total</b></td><td class="num"><b>1.0M</b></td><td class="num"><b>511.6M</b></td><td class="num"><b>14,138M</b></td><td class="num"><b>39.6M</b></td><td class="num"><b>$14,914</b></td></tr>
</table>
{chart_usage}
<p class="small">All-time since 2026-05-06: 96,358 requests, 74 active days, 18.1B cache-read tokens. Peak day Aug 20: 2.70B tokens, 10,064 requests.
Priced at Anthropic list (Fable $10/$50, Opus $5/$25, Sonnet 5 $2/$10 per MTok; cache writes 1.25&#215;/2&#215;, reads 0.1&#215; input).</p>
<div class="note"><b>The structural fact that decides everything downstream:</b> 96% of your token volume is served from the provider-side prompt cache
at a 90% discount. A local rig has no equivalent free lunch at this scale — every cached token evicted from a local KV cache must be physically
recomputed (prefill), and your multi-agent pattern (up to 10k requests/day) churns sessions constantly.</div>
''', "Demand side")}

{sec("What the clouds charge (verified 2026-08-28)", f'''
<h3>Consumer subscriptions</h3>
<table>
<tr><th>Provider</th><th>Free tier</th><th>Top consumer tier</th><th>Coding-agent limits</th></tr>
<tr><td>Anthropic</td><td>$0 — Fable/Opus/Sonnet/Haiku at ~50% of weekly limits</td><td><b>Max 20x — $200/mo</b> (Pro $17–20, Max 5x $100)</td><td>5-h rolling + weekly caps, pooled across surfaces; token amounts unpublished. Limits doubled 2026-05-06.</td></tr>
<tr><td>OpenAI</td><td>$0 — GPT-5.6 Luna, basic Codex</td><td><b>Pro — $100 (5&#215;) or $200 (20&#215;)</b> (Plus $20, Go $8)</td><td>Only provider publishing numbers: Pro-20x = 200–2,000 GPT-5.6-Sol Codex msgs/5h. 1 credit &#8776; $0.04 (inferred).</td></tr>
<tr><td>Google</td><td>$0 — Gemini 3.6 Flash; Jules 15 tasks/day</td><td><b>AI Ultra — $99.99 (5&#215;) or $199.99 (20&#215;)</b> (Pro $19.99)</td><td>Jules: 300 tasks/day, 60 concurrent on Ultra (same at both Ultra price points).</td></tr>
</table>
<h3>API list prices, $/MTok in &#8594; out (frontier + mid)</h3>
<table>
<tr><th>Anthropic</th><th class="num">$</th><th>OpenAI</th><th class="num">$</th><th>Google</th><th class="num">$</th></tr>
<tr><td>Fable 5</td><td class="num">10 / 50</td><td>gpt-5.6-sol</td><td class="num">4 / 20</td><td>Gemini 3.1 Pro Prev &#8804;200k</td><td class="num">2 / 12</td></tr>
<tr><td>Opus 5</td><td class="num">5 / 25</td><td>gpt-5.6-terra</td><td class="num">2 / 12</td><td>&gt;200k ctx</td><td class="num">4 / 18</td></tr>
<tr><td>Sonnet 5</td><td class="num">2 / 10</td><td>gpt-5.6-luna</td><td class="num">0.20 / 1.20</td><td>Gemini 3.7 Flash (promo &#8594; 2&#215; on 2027-01-01)</td><td class="num">0.75 / 3.75</td></tr>
</table>
<p class="small">Corrections to commonly circulated figures: Google AI Ultra is no longer $249.99 (split $99.99/$199.99 at I/O 2026);
ChatGPT Pro is now two price points; Sonnet 5's scheduled Sept-2026 rise to $3/$15 was <b>cancelled</b> — $2/$10 is permanent.
Claude 4.7+ tokenizer produces ~30% more tokens per unit text than Sonnet 4.6-era models (already reflected in your measured counts).</p>
<div class="note">Free tiers vs your workload: Claude Free is ~50% of <i>Pro</i> weekly limits &#8594; roughly <b>2–3%</b> of your Max-20x volume.
Gemini free Jules (15 vs 300 tasks/day) &#8594; ~5%. ChatGPT Free ("basic Codex") — unpublished but similar order. Free tiers are not a
serviceable option for this workload; they exist in this analysis as a $0 floor only.</div>
''', "Cloud supply side")}

{sec("Local hardware in the 2026 DRAM shortage", f'''
<table>
<tr><th>Option</th><th class="num">Price (Aug 2026)</th><th>Best current open model it can serve</th><th class="num">Idle / load W</th><th class="num">3-yr residual (base)</th></tr>
<tr><td>2&#215; used RTX 3090 build (48GB)</td><td class="num">~$2,900</td><td>Qwen3.8-27B 4-bit</td><td class="num">40 / 500</td><td class="num">50%</td></tr>
<tr><td>Strix Halo 128GB (GMKtec EVO-X2)</td><td class="num">$3,650</td><td>Qwen3.8-Flash-Next</td><td class="num">13 / 112</td><td class="num">40%</td></tr>
<tr><td>NVIDIA DGX Spark 128GB</td><td class="num">$4,699 (+$700 Aug hike)</td><td>Qwen3.8-Flash-Next</td><td class="num">35 / 170</td><td class="num">40%</td></tr>
<tr><td>RTX 5090 workstation (32GB)</td><td class="num">~$8,500 (card $4.3–4.9k street, 2.2&#215; MSRP)</td><td>Qwen3.8-27B 4-bit</td><td class="num">30 / 700</td><td class="num">70%</td></tr>
<tr><td>Mac Studio M5 Ultra 256GB</td><td class="num">$10,799</td><td>GLM-5.3-Flash 4-bit (200GB)</td><td class="num">~10 / ~220&#8224;</td><td class="num">60%</td></tr>
<tr><td>Mac Studio M5 Ultra 512GB</td><td class="num">~$17,200 (est&#8224;, ships late Oct)</td><td>DeepSeek V4 / heavy-quant Kimi K3</td><td class="num">~10 / ~250&#8224;</td><td class="num">60%</td></tr>
</table>
<p class="small">&#8224; M5 hardware ships Sept 22 2026: power figures proxied from Apple's official M3 Ultra measurements (9W idle / 270W max);
512GB price extrapolated at Apple's observed $25/GB memory pricing — Apple says only "well above $10,000". Flagged, not quoted.</p>
<h3>Apple's leasing program ("Apple Upgrade", launched 2026-07-28)</h3>
<ul>
<li>Klarna-underwritten, 0% interest, soft credit check. Mac Studio from $48.99/mo. <b>Payments + buyout = exactly list price</b> — it is deferred payment, not depreciation-priced leasing.</li>
<li>36-mo structure: pay ~70% of list over the term, ~30% residual buyout — or return the machine. M5 Ultra 256GB: &#8776;<b>$210/mo</b>, $3,240 buyout.</li>
<li>Return-at-term = a <b>guaranteed 30% residual with zero resale friction</b>. Buying + reselling at today's 60% used-market retention is cheaper ($120/mo effective) — <i>if</i> the shortage-inflated used market holds. Lease = insurance against residual collapse. Ceiling for five-figure BTO configs unconfirmed.</li>
</ul>
<div class="note">Shortage context: AI datacenters are absorbing ~70% of world memory output (IDC). RTX 5090 street is 2.1–2.5&#215; MSRP;
RTX PRO 6000 is +87% since launch; DGX Spark +$700 in August; Apple pulled all &gt;128GB Macs for 5 months and repriced upward.
Used RTX 4090s now sell <b>above</b> their original MSRP — GPU depreciation has inverted. Residuals in this model are therefore
shortage-propped: the base case uses today's observed values, the conservative case assumes partial normalization after 2027 supply relief.</div>
''', "Hardware supply side")}

{sec("The physics: can a local box even serve this workload?", f'''
<p>Your workload requires prefilling <b>~513M genuinely new tokens/mo</b>, plus recomputing whatever share of the 14.1B cached tokens
a local KV cache cannot hold (base case 10%, range 5–25%), plus decoding 39.6M output tokens. Dividing by each machine's
<i>depth-adjusted, primary-source</i> throughput (measured at agentic 30–130k contexts, not headline pp512 numbers) gives the
compute-hours each box needs per month — against 720 hours existing:</p>
{chart_feas}
<div class="legend"><span><i style="background:{C['good']}"></i>workable (&lt;240 h)</span>
<span><i style="background:{C['warn']}"></i>saturated 240–720 h: permanent queueing, minutes-long TTFT</span>
<span><i style="background:{C['crit']}"></i>impossible &gt;720 h even running 24/7</span></div>
<p>Bars show the base case; tooltips carry the optimistic&#8594;pessimistic range. Two findings:</p>
<ul>
<li><b>The only workable class is the small-model GPU class</b> (RTX 5090 running a 27B). Every 128GB+ unified-memory box that could host a <i>better</i> model is saturated or physically impossible — prefill speed, not decode, is the wall.</li>
<li><b>The near-frontier open models are unservable at your volume.</b> The Mac that fits DeepSeek V4-class models would need 3,800+ h/mo — 5&#215; more hours than a month contains. Measured TTFT for a 128k prompt: RTX 5090 ~20s &#183; DGX Spark ~2 min &#183; Strix Halo 4–7 min &#183; Mac Studio ~14 min. The cloud serves the same request from cache in seconds.</li>
</ul>
''', "Feasibility")}

{sec("True monthly cost, amortized", f'''
<p>3-year straight-line amortization net of residual value, 5%/yr opportunity cost of capital, US-average electricity (18.3&#162;/kWh),
and labor at $75/h — 24h one-time setup (measured range: a weekend to a week), 3 h/mo maintenance (chat-template patches, driver
regressions), 10 h/mo extra babysitting (controlled study: local agents needed 7 operator interventions per task vs 1 for Claude):</p>
{chart_tco}
<table>
<tr><th>Scenario ($/mo, base KV-miss)</th><th class="num">2&#215;3090</th><th class="num">Strix</th><th class="num">Spark</th><th class="num">5090</th><th class="num">Mac 256</th><th class="num">Mac 512</th></tr>
<tr><td>Hobbyist — your time worth $0</td><td class="num">$86</td><td class="num">$91</td><td class="num">$120</td><td class="num">$128</td><td class="num">$193</td><td class="num">$296</td></tr>
<tr><td>Base — light babysit, $75/h</td><td class="num">$1,111</td><td class="num">$1,116</td><td class="num">$1,145</td><td class="num">$1,153</td><td class="num">$1,218</td><td class="num">$1,321</td></tr>
<tr><td>PG&amp;E marginal 40&#162;/kWh</td><td class="num">$1,140</td><td class="num">$1,133</td><td class="num">$1,172</td><td class="num">$1,178</td><td class="num">$1,251</td><td class="num">$1,360</td></tr>
<tr><td>Heavy babysit (40 h/mo)</td><td class="num">$3,361</td><td class="num">$3,366</td><td class="num">$3,395</td><td class="num">$3,403</td><td class="num">$3,468</td><td class="num">$3,571</td></tr>
<tr><td>Senior time $150/h</td><td class="num">$2,136</td><td class="num">$2,141</td><td class="num">$2,170</td><td class="num">$2,178</td><td class="num">$2,243</td><td class="num">$2,346</td></tr>
<tr><td>Conservative residuals</td><td class="num">$1,127</td><td class="num">$1,131</td><td class="num">$1,165</td><td class="num">$1,200</td><td class="num">$1,263</td><td class="num">$1,392</td></tr>
</table>
<p><b>Labor dominates everything.</b> Hardware amortization is $40–191/mo; electricity is $15–34/mo; the moment your time has market value,
the babysitting tax is 5–25&#215; the hardware cost. This matches the strongest first-hand study's conclusion: the GPU is
"16–20 months of Claude for the price of the card alone — before the rest of the rig, the electricity, or your time."</p>
<div class="note">Reference points: your $200/mo subscription (dashed line) &#183; API pay-as-you-go for this workload: <b>$14,914/mo — 10&#215; above
the chart's top edge</b>. Local inference IS dramatically cheaper than API list prices. It is dramatically more expensive than your subscription,
which is the option you actually hold.</div>
''', "TCO")}

{sec("Efficacy: what quality do you give up?", f'''
<p>Independent cross-vendor scores (Artificial Analysis Intelligence Index v4.1.1, 9 evals, same harness for open and closed models).
Bars = cloud-served full precision; tick marks = effective level after 4-bit quantization (&#8776;93% retention, Unsloth measurements)
needed to fit local memory:</p>
{chart_quality}
{leg_quality}
<table>
<tr><th>Signal (independent where possible)</th><th>Frontier</th><th>Best local-servable</th><th>Gap</th></tr>
<tr><td>AA Intelligence Index</td><td>Opus 5: 63</td><td>GLM-5.3-Flash @256GB: 57 &#8594; &#8776;53 quantized</td><td>&#8722;10 pts (&#8722;16%)</td></tr>
<tr><td>SWE-bench Verified</td><td>GPT-5.6 Sol 96.2% &#183; Opus 5 96%</td><td>DeepSeek V4-Pro 80.6% (vendor, unservable locally)</td><td>&#8722;16 pts</td></tr>
<tr><td>Terminal-Bench 2.1 (agentic)</td><td>GPT-5.6 Sol 89.5 &#183; Opus 5 89.1</td><td>GLM-5.3-Flash 84.3 (cloud-served)</td><td>&#8722;5 pts</td></tr>
<tr><td>LMArena Elo</td><td>Fable 5 ~1525 (#1)</td><td>best open ~1450</td><td>&#8722;55–75 Elo &#8776; 54–58% win rate</td></tr>
</table>
<p><b>The paper gap is the floor, not the ceiling.</b> Three multipliers hit local deployments specifically:</p>
<ul>
<li><b>Quantization tax</b> — 4-bit &#8776;93% retention, 3-bit 82%; and quantization specifically degrades tool-call formatting, the exact capability agentic coding depends on.</li>
<li><b>Reasoning-effort tax</b> — Qwen3.8-27B hits its 52 only at xhigh effort, burning 160M output tokens vs a 43M median on the same eval: a benchmark win that becomes a wall-clock loss at 40–180 tok/s local decode.</li>
<li><b>Workflow tax</b> — the one controlled head-to-head (Ring, Jun 2026): local agent passed 74 tests vs Claude's 114 (65%), needed 7 operator interventions vs 1, hit 4 context compactions vs 0, and looped on an identical error 44 consecutive times. Documented ecosystem breakage is systemic: llama.cpp broke OpenAI-compatible tool-calls (Mar 2026); a coding-agent + llama.cpp tool-role bug was closed "not planned"; broken GGUF chat templates are endemic.</li>
</ul>
<p>Quality-adjusted (÷0.65 acceptance from the controlled study), the feasible local options cost <b>$1,774–1,874/mo</b> for
Claude-equivalent completed work — 9&#215; your subscription — before counting the intervention time already in the labor line.</p>
<p class="small">A genuinely important nuance: the open-model gap has narrowed sharply in 2026 (Kimi K3 and GLM-5.3 sit at 60 vs 63) —
but only at parameter scales (753B–2.8T) that no desk-side machine can serve at your volume. The gap you can <i>buy</i> at retail is
&#8722;10 to &#8722;15 index points, not &#8722;3.</p>
''', "Efficacy")}

{sec("Verdict", f'''
<p class="verdict"><b>For your workload, nothing local comes within an order of magnitude of your current setup.</b>
You consume ~$14,914/mo of API-equivalent frontier compute for $200. The best local alternative that is even
<i>physically feasible</i> at your volume costs ~$1,153/mo honestly accounted ($128/mo if your time is worth $0), delivers
&#8776;48/63 of frontier quality, ~7&#215; the operator interventions, and minutes-long prompt latencies the cloud serves in seconds.</p>
<table>
<tr><th>Option</th><th class="num">$/mo</th><th>Quality (AA)</th><th>Serves your volume?</th></tr>
<tr><td><b>Claude Max 20x (current)</b></td><td class="num"><b>$200</b></td><td><b>63</b></td><td><b>yes — proven by 3 months of logs</b></td></tr>
<tr><td>ChatGPT Pro 20x / Google AI Ultra 20x</td><td class="num">$200</td><td>&#8776;62–63</td><td>likely yes (limits unpublished/lower)</td></tr>
<tr><td>RTX 5090 workstation, honest labor</td><td class="num">$1,153</td><td>&#8776;48</td><td>yes (143 h/mo)</td></tr>
<tr><td>Mac M5 Ultra 256GB (buy or lease $210/mo)</td><td class="num">$1,218</td><td>&#8776;53</td><td>saturated</td></tr>
<tr><td>API pay-as-you-go</td><td class="num">$14,914</td><td>63</td><td>yes</td></tr>
<tr><td>Free tiers (all providers)</td><td class="num">$0</td><td>62–63</td><td>~2–5% of your volume</td></tr>
</table>
<h3>When local genuinely wins</h3>
<ul>
<li><b>Hard privacy / air-gap / compliance requirements</b> — the only case where every credible source agrees, because the cloud is simply unavailable. Price it as +$950–1,650/mo vs your subscription.</li>
<li><b>Workloads locked out of consumer subscriptions</b> (high-volume programmatic API use): local at ~$1.1–1.3k/mo beats $14.9k API list by 10&#215;+ — this is the real arbitrage local serves, and it is not your situation.</li>
<li><b>Hobby scale with time valued at $0</b> and quality tolerance: $86–128/mo beats a $200 subscription in cash terms (at ~25% lower model quality and no frontier access).</li>
<li><b>A hedge you already own</b>: running a 4-bit 27B on hardware you have anyway costs ~$15–30/mo of electricity — reasonable as an offline fallback, not a replacement.</li>
</ul>
<p>If cost pressure is the motive: the far better lever is <b>model-mix discipline</b> — your Fable 5 usage ($7,475 API-equivalent, 50%
of consumption) burns weekly limits ~2&#215; faster than Opus per token; shifting exploratory work down-tier stretches the same $200 further
than any hardware purchase ever could.</p>
''', "Bottom line")}

{sec("Method, sensitivity &amp; validation", f'''
<h3>Cost-estimation practices applied</h3>
<ul>
<li><b>Measured demand, not assumed</b> — 30-day token/request census from local transcripts, deduplicated; model-mix priced per token category (input / 5m &amp; 1h cache-write / cache-read / output).</li>
<li><b>Primary-source prices with dates</b> — every price re-verified 2026-08-28 against provider-owned pages; stale figures (AI Ultra $249.99, single-tier ChatGPT Pro, $2k RTX 5090) explicitly rejected; SEO/AI content farms excluded by name.</li>
<li><b>Full TCO</b> — amortization net of residual, opportunity cost of capital, marginal (not average) electricity, one-time + recurring + per-task labor, lease-vs-buy for Apple hardware.</li>
<li><b>Depth-adjusted throughput</b> — feasibility uses long-context measurements (headline pp512 figures overstate agentic throughput 2–5&#215;).</li>
<li><b>Sensitivity grid</b> — six scenarios per option (above); conclusions survive every branch: even at $0 labor + optimistic KV-miss + US-cheap power, no option matches subscription quality-per-dollar.</li>
</ul>
<h3>Cross-checks</h3>
<ul>
<li>Two independent scripts computed usage totals — agree to rounding. Priced total re-computed after the Sonnet 5 price correction ($15,117 &#8594; $14,914).</li>
<li>Blended cost $1.02/MTok is consistent with the one published heavy-user datapoint (10B tokens &#8776; $15k API-equiv &#8594; $1.5/MTok, lighter caching).</li>
<li>Feasibility model reproduces independently reported real-world TTFT (~90s for a 16k prompt on Mac Studio &#8776; our 178 t/s effective prefill).</li>
<li>Amortization cross-checks the Ring study's framing ("GPU = 16–20 months of subscription for the card alone").</li>
<li>Your 75&#215; leverage vs third-party "heavy user" estimates ($600–1,500/mo): you are 10&#215; their "heavy" — explained by multi-agent workflows, 1h-TTL cache pricing, and Fable-tier rates; flagged rather than smoothed.</li>
</ul>
<h3>Key uncertainties (direction of bias)</h3>
<ul>
<li>M5 Ultra power &amp; throughput unmeasured until Sept 22 — proxied from M3 Ultra (likely <i>understates</i> M5 prefill — but a feasibility class only flips if throughput is off by ~2&#215;, and the 512GB case misses by 5&#215;).</li>
<li>512GB price extrapolated ($25/GB observed); Apple Upgrade eligibility ceiling unconfirmed.</li>
<li>KV-miss fraction (5–25% band) is an engineering estimate — the single biggest feasibility lever, hence carried as the scenario axis.</li>
<li>Throughput for Qwen3.8-FN / GLM-5.3-Flash proxied from measured same-active-param predecessors (gpt-oss-120b etc.).</li>
<li>GPU residuals are shortage-propped; conservative branch provided. SWE-bench Pro / LCB open-model scores are vendor-reported.</li>
<li>Your possible extra-usage overage spend is billed server-side and invisible to local logs — if material, it strengthens the subscription-value conclusion's denominator but not its direction.</li>
</ul>
<p class="small">Sources: Anthropic/OpenAI/Google pricing &amp; support pages; apple.com newsroom + Apple Upgrade terms; EIA Electric Power Monthly
&amp; STEO Aug-2026; PG&amp;E tariff sheet (eff. 2026-03-01); Artificial Analysis Index v4.1.1; Vals AI Terminal-Bench 2.1; llama.cpp/mlx/vLLM
GitHub benchmark discussions &amp; issues (#15396, #16578, #17917, #19890, #20198, #3209); kyuz0 Strix toolboxes; CloudRift; jetsonhacks;
johnhringiv.com controlled study; Swappa/BuySellRam resale data; videocardz/overclock3d price reporting. Full URL list available on request.</p>
''', "Validation")}

<p class="small" style="text-align:center;margin-top:6px">Generated 2026-08-28 &#183; demand data: your machine's Claude Code transcripts &#183;
model: 3-yr horizon, 36-mo amortization &#183; all flagged estimates marked in place</p>
</div></body></html>"""

open("report.html", "w").write(page)
print(f"report.html written: {len(page):,} bytes")
