#!/usr/bin/env python3
"""
True-cost model: local LLM inference vs cloud frontier for THIS user's measured workload.
All demand figures measured from ~/.claude transcripts (last 30 days, 2026-07-29..08-28).
All prices/throughputs from primary-source research 2026-08-28 (see report for citations).
"""
import json

# ---------------- MEASURED DEMAND (tokens/month) ----------------
DECODE = 39.6e6          # output tokens
NEW_PREFILL = 513e6      # uncached input + cache writes = genuinely new tokens
CACHE_READ = 14.14e9     # tokens served from provider prompt cache
API_EQUIV_COST = 14914   # $/mo at current Anthropic list prices (computed exactly)

# Fraction of cache-read volume a local server must RE-prefill (KV-cache slot
# eviction across parallel sessions/restarts; API-side cache is effectively
# unlimited, local KV slots are not).
KV_MISS = {"optimistic": 0.05, "base": 0.10, "pessimistic": 0.25}

HOURS_MO = 720.0

# ---------------- HARDWARE OPTIONS ----------------
# pp = depth-adjusted prefill tok/s (agentic 30-130k contexts), tg = decode tok/s
# residual = base-case 3-yr resale fraction (shortage-inflated; cons = conservative)
HW = {
    "Strix Halo 128GB (GMKtec, $3.65k)": dict(
        price=3650, idle_w=13, load_w=112, pp=550, tg=38,
        residual=0.40, res_cons=0.25,
        model="Qwen3.8-Flash-Next (proxy: gpt-oss-120b)", aa=56, aa_local=52,
        quality="mid-open"),
    "DGX Spark 128GB ($4.7k)": dict(
        price=4699, idle_w=35, load_w=170, pp=1100, tg=45,
        residual=0.40, res_cons=0.25,
        model="Qwen3.8-Flash-Next (proxy: gpt-oss-120b)", aa=56, aa_local=52,
        quality="mid-open"),
    "2x used RTX 3090 build (~$2.9k)": dict(
        price=2900, idle_w=40, load_w=500, pp=2000, tg=150,
        residual=0.50, res_cons=0.30,
        model="Qwen3.8-27B 4-bit (proxy: Qwen3-30B-A3B)", aa=52, aa_local=48, quality="small-open"),
    "RTX 5090 workstation ($8.5k street)": dict(
        price=8500, idle_w=30, load_w=700, pp=6500, tg=180,
        residual=0.70, res_cons=0.50,
        model="Qwen3.8-27B 4-bit (proxy: Qwen3.5-35B-A3B)", aa=52, aa_local=48, quality="small-open"),
    "Mac Studio M5 Ultra 256GB ($10.8k)": dict(
        price=10799, idle_w=10, load_w=220, pp=1000, tg=70,
        residual=0.60, res_cons=0.45,
        model="GLM-5.3-Flash 4-bit (200GB) / Qwen3.8-FN", aa=57, aa_local=53, quality="mid-open"),
    "Mac Studio M5 Ultra 512GB (~$17.2k est)": dict(
        price=17199, idle_w=10, load_w=250, pp=190, tg=11,
        residual=0.60, res_cons=0.45,
        model="DeepSeek V4 Pro / Kimi K3 heavy-quant", aa=60, aa_local=56, quality="large-open"),
}

# ---------------- COST PARAMETERS ----------------
ELEC = {"US avg $0.183": 0.1834, "PG&E marginal $0.40": 0.40}
SETUP_HOURS = 24          # one-time (weekend..1 week measured range 16-40)
MAINT_H_MO = 3            # template/driver/regression upkeep (range 1-6)
BABYSIT_H_MO = {"hobby ($0/h)": 0, "light": 10, "heavy": 40}  # extra interventions
LABOR_RATE = 75           # $/h base (0 hobby, 150 senior sensitivity)
CAPITAL = 0.05            # opportunity cost of capital /yr
MONTHS = 36

def feasibility(hw, miss):
    prefill_tok = NEW_PREFILL + miss * CACHE_READ
    h_prefill = prefill_tok / hw["pp"] / 3600
    h_decode = DECODE / hw["tg"] / 3600
    return h_prefill, h_decode, h_prefill + h_decode

def monthly_cost(hw, miss, elec_rate, babysit_h, labor_rate=LABOR_RATE,
                 residual=None, capital=CAPITAL):
    res = hw["residual"] if residual is None else residual
    hp, hd, busy = feasibility(hw, miss)
    feasible = busy <= HOURS_MO
    busy_c = min(busy, HOURS_MO)
    idle_c = HOURS_MO - busy_c
    kwh = (busy_c * hw["load_w"] + idle_c * hw["idle_w"]) / 1000
    amort = hw["price"] * (1 - res) / MONTHS
    cap = hw["price"] * capital / 12
    elec = kwh * elec_rate
    labor = (SETUP_HOURS / MONTHS + MAINT_H_MO + babysit_h) * labor_rate
    return dict(feasible=feasible, busy_h=busy, kwh=kwh, amort=amort,
                capital=cap, elec=elec, labor=labor,
                total=amort + cap + elec + labor)

print("=" * 100)
print("A. FEASIBILITY — hours of compute/month your workload needs (720 h available)")
print("=" * 100)
print(f"{'hardware':<42}{'model class':<28}{'opt(5%)':>9}{'base(10%)':>10}{'pess(25%)':>10}")
for name, hw in HW.items():
    row = [feasibility(hw, m)[2] for m in KV_MISS.values()]
    flags = ["" if h <= HOURS_MO else " XX" for h in row]
    print(f"{name:<42}{hw['model']:<28}"
          f"{row[0]:>7.0f}h{flags[0]:<2}{row[1]:>8.0f}h{flags[1]:<2}{row[2]:>8.0f}h{flags[2]}")
print("XX = physically impossible (>720 h).")
print("CLASSIFICATION: <240 h/mo = workable; 240-720 h = saturated (queueing, minutes-long")
print("TTFT for interactive multi-agent work); >720 h = impossible even running 24/7.")

print()
print("=" * 100)
print("B. MONTHLY TCO (base: 10% KV miss, US-avg electricity, light babysitting 10 h/mo @ $75)")
print("=" * 100)
print(f"{'hardware':<42}{'amort':>7}{'capital':>8}{'elec':>7}{'labor':>7}{'TOTAL':>8}  feasible")
results = {}
for name, hw in HW.items():
    c = monthly_cost(hw, KV_MISS["base"], ELEC["US avg $0.183"], BABYSIT_H_MO["light"])
    results[name] = c
    print(f"{name:<42}{c['amort']:>7.0f}{c['capital']:>8.0f}{c['elec']:>7.0f}"
          f"{c['labor']:>7.0f}{c['total']:>8.0f}  {'yes' if c['feasible'] else 'NO'}")

print()
print("=" * 100)
print("C. SCENARIO GRID — total $/mo (rows: hardware; feasible cases only marked *)")
print("=" * 100)
scen_defs = [
    ("hobby: US elec, $0 labor",       dict(elec=ELEC["US avg $0.183"], bab=0,  rate=0)),
    ("base: US elec, light, $75/h",    dict(elec=ELEC["US avg $0.183"], bab=10, rate=75)),
    ("PG&E, light, $75/h",             dict(elec=ELEC["PG&E marginal $0.40"], bab=10, rate=75)),
    ("heavy babysit, $75/h",           dict(elec=ELEC["US avg $0.183"], bab=40, rate=75)),
    ("senior time $150/h, light",      dict(elec=ELEC["US avg $0.183"], bab=10, rate=150)),
    ("conservative residual",          dict(elec=ELEC["US avg $0.183"], bab=10, rate=75, cons=True)),
]
hdr = f"{'hardware':<42}" + "".join(f"{s[:14]:>16}" for s, _ in scen_defs)
print(hdr)
grid = {}
for name, hw in HW.items():
    row = []
    for sname, s in scen_defs:
        c = monthly_cost(hw, KV_MISS["base"], s["elec"], s["bab"], labor_rate=s["rate"],
                         residual=hw["res_cons"] if s.get("cons") else None)
        row.append((c["total"], c["feasible"]))
    grid[name] = row
    print(f"{name:<42}" + "".join(f"{t:>14.0f}{'*' if f else 'X'} " for t, f in row))
print("* feasible  X infeasible at this workload volume")

print()
print("=" * 100)
print("D. CLOUD REFERENCE POINTS ($/mo)")
print("=" * 100)
cloud = {
    "Claude Max 20x (current setup)": 200,
    "ChatGPT Pro 20x": 200,
    "Google AI Ultra 20x": 199.99,
    "Claude Pro": 20,
    "Any free tier": 0,
    "Anthropic API pay-as-you-go (this workload)": API_EQUIV_COST,
}
for k, v in cloud.items():
    print(f"  {k:<46} ${v:>9,.0f}")
print(f"\n  Subscription leverage: ${API_EQUIV_COST:,}/mo of API-equivalent compute for $200 = {API_EQUIV_COST/200:.0f}x")

print()
print("=" * 100)
print("E. EFFECTIVE COST PER MILLION OUTPUT TOKENS (quality-unadjusted)")
print("=" * 100)
base = KV_MISS["base"]
for name, hw in HW.items():
    c = monthly_cost(hw, base, ELEC["US avg $0.183"], BABYSIT_H_MO["light"])
    if c["feasible"]:
        print(f"  {name:<44} ${c['total']/ (DECODE/1e6):>8.2f}/M out-tok "
              f"(vs $200 sub = ${200/(DECODE/1e6):.2f}/M, API blend = ${API_EQUIV_COST/(DECODE/1e6):.2f}/M)")

print()
print("=" * 100)
print("F. QUALITY ADJUSTMENT — frontier AA Index = 63 (Opus 5); local effective index in")
print("   parens. Workflow lens (Ring 2026 study): local passes 74 vs Claude 114")
print("   tests => ~65% acceptance; 7x operator interventions)")
print("=" * 100)
for name, hw in HW.items():
    c = monthly_cost(hw, base, ELEC["US avg $0.183"], BABYSIT_H_MO["light"])
    if c["feasible"]:
        adj = c["total"] / 0.65
        print(f"  {name:<44} raw ${c['total']:>6.0f} -> quality-adj ${adj:>7.0f}/mo "
              f"for equivalent completed work")

print()
print("=" * 100)
print("G. WHEN DOES LOCAL WIN? (hobby mode: your time valued at $0)")
print("=" * 100)
for name, hw in HW.items():
    hp, hd, busy = feasibility(hw, KV_MISS["base"])
    c = monthly_cost(hw, KV_MISS["base"], ELEC["US avg $0.183"], 0, labor_rate=0)
    verdict = "impossible at your volume" if busy > HOURS_MO else (
        "saturated at your volume" if busy > 240 else "workable")
    print(f"  {name:<44} hobby-cost ${c['total']:>4.0f}/mo vs $200 sub -> "
          f"{'cheaper' if c['total'] < 200 else 'MORE expensive'}; {verdict}")
print("  NOTE: even where hobby-cost < $200, the $200 subscription serves FRONTIER-model")
print("  quality; local serves small/mid open-weights (see quality adjustment above).")
print("  Local wins cleanly only vs API pay-as-you-go rates ($14.9k/mo equivalent) --")
print("  i.e., for workloads that cannot use consumer subscriptions (compliance, air-gap,")
print("  automation outside subscription ToS), or where privacy is priced above quality.")
print()
print("=" * 100)
print("H. APPLE UPGRADE LEASE vs BUY (Mac Studio M5 Ultra 256GB, $10,799 list)")
print("=" * 100)
lease_mo = 10799 * 0.70 / 36
print(f"  Lease 36mo (~70% of list): ~${lease_mo:.0f}/mo, buyout ${10799*0.30:,.0f} or return")
print(f"  Return at term = guaranteed 30% residual, zero resale friction, 0% interest")
print(f"  Buy + resell at 60% market residual: net 3-yr cost ${10799*0.40:,.0f} "
      f"(${10799*0.40/36:.0f}/mo) - cheaper IF shortage-propped resale holds")
print(f"  Buy + resell at 45% conservative: ${10799*0.55:,.0f} (${10799*0.55/36:.0f}/mo) - lease wins as insurance")

# dump JSON for the report
out = {
    "demand": dict(decode=DECODE, new_prefill=NEW_PREFILL, cache_read=CACHE_READ,
                   api_equiv=API_EQUIV_COST),
    "feasibility": {n: {k: feasibility(h, m)[2] for k, m in KV_MISS.items()} for n, h in HW.items()},
    "base_tco": {n: monthly_cost(h, KV_MISS['base'], ELEC['US avg $0.183'], 10) for n, h in HW.items()},
    "grid": {n: [t for t, f in grid[n]] for n in HW},
}
json.dump(out, open("tco_results.json", "w"), indent=1)
print("\n[tco_results.json written]")
