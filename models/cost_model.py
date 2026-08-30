#!/usr/bin/env python3
"""API-equivalent cost of last-30-day Claude Code usage, per model."""
import json, os, glob, collections, datetime

root = os.path.expanduser("~/.claude/projects")
CUT = (datetime.date(2026, 8, 28) - datetime.timedelta(days=30)).isoformat()

# $/MTok: input, output, cache_write_5m (1.25x), cache_write_1h (2x), cache_read (0.1x)
PRICE = {
    "claude-fable-5":            (10.0, 50.0, 12.50, 20.0, 1.00),
    "claude-opus-5":             (5.0,  25.0,  6.25, 10.0, 0.50),
    "claude-opus-4-8":           (5.0,  25.0,  6.25, 10.0, 0.50),
    "claude-opus-4-7":           (5.0,  25.0,  6.25, 10.0, 0.50),
    "claude-sonnet-5":           (2.0,  10.0,  2.50,  4.0, 0.20),
    "claude-haiku-4-5-20251001": (1.0,   5.0,  1.25,  2.0, 0.10),
}

agg = collections.defaultdict(collections.Counter)
seen = set()
for path in glob.glob(root + "/**/*.jsonl", recursive=True):
    try:
        with open(path, errors="ignore") as f:
            for line in f:
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                m = d.get("message") or {}
                u = m.get("usage")
                if not u or not isinstance(u, dict):
                    continue
                if (d.get("timestamp") or "")[:10] < CUT:
                    continue
                mid = m.get("id"); rid = d.get("requestId")
                if mid:
                    key = (mid, rid)
                    if key in seen:
                        continue
                    seen.add(key)
                model = m.get("model", "unknown")
                c = agg[model]
                c["in"] += u.get("input_tokens", 0) or 0
                c["out"] += u.get("output_tokens", 0) or 0
                cc = u.get("cache_creation")
                if isinstance(cc, dict):
                    c["cw5m"] += cc.get("ephemeral_5m_input_tokens", 0) or 0
                    c["cw1h"] += cc.get("ephemeral_1h_input_tokens", 0) or 0
                else:
                    c["cw5m"] += u.get("cache_creation_input_tokens", 0) or 0
                c["cr"] += u.get("cache_read_input_tokens", 0) or 0
    except Exception:
        pass

total_cost = 0.0
total_out = 0
print(f"{'model':<28}{'in(M)':>8}{'out(M)':>8}{'cw5m(M)':>9}{'cw1h(M)':>9}{'cr(M)':>10}{'cost($)':>11}")
for model, c in sorted(agg.items(), key=lambda x: -sum(x[1].values())):
    p = PRICE.get(model)
    if p is None:
        if sum(c.values()) > 0:
            print(f"{model:<28} (unpriced, skipped) tokens={sum(c.values()):,}")
        continue
    cost = (c["in"]*p[0] + c["out"]*p[1] + c["cw5m"]*p[2] + c["cw1h"]*p[3] + c["cr"]*p[4]) / 1e6
    total_cost += cost
    total_out += c["out"]
    print(f"{model:<28}{c['in']/1e6:>8.1f}{c['out']/1e6:>8.1f}{c['cw5m']/1e6:>9.1f}{c['cw1h']/1e6:>9.1f}{c['cr']/1e6:>10.0f}{cost:>11,.0f}")

print(f"\nLAST-30-DAY API-EQUIVALENT COST: ${total_cost:,.0f}")
print(f"Output tokens (30d): {total_out/1e6:.1f}M")
print(f"Implied $/day: ${total_cost/30:,.0f}")
