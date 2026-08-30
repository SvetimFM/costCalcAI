#!/usr/bin/env python3
"""Aggregate Claude Code token usage from local transcript JSONL files."""
import json, os, glob, collections, datetime, sys

root = os.path.expanduser("~/.claude/projects")
by_model = collections.defaultdict(collections.Counter)
by_day = collections.defaultdict(collections.Counter)
seen = set()
files = glob.glob(root + "/**/*.jsonl", recursive=True)
sessions = set()

for path in files:
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
                mid = m.get("id")
                rid = d.get("requestId")
                if mid:
                    key = (mid, rid)
                    if key in seen:
                        continue
                    seen.add(key)
                model = m.get("model", "unknown")
                ts = (d.get("timestamp") or "")[:10]
                sid = d.get("sessionId")
                if sid:
                    sessions.add(sid)
                vals = {
                    "input": u.get("input_tokens", 0) or 0,
                    "output": u.get("output_tokens", 0) or 0,
                    "cache_create": u.get("cache_creation_input_tokens", 0) or 0,
                    "cache_read": u.get("cache_read_input_tokens", 0) or 0,
                }
                for k, v in vals.items():
                    by_model[model][k] += v
                    by_day[ts][k] += v
                by_day[ts]["requests"] += 1
    except Exception as e:
        print(f"skip {path}: {e}", file=sys.stderr)

def fmt(c):
    return (f"in={c['input']:,} out={c['output']:,} "
            f"cacheW={c['cache_create']:,} cacheR={c['cache_read']:,}")

days = sorted(k for k in by_day if k)
print(f"files={len(files)} sessions={len(sessions)} active_days={len(days)}")
if days:
    print(f"date_range: {days[0]} .. {days[-1]}")

total = collections.Counter()
for c in by_day.values():
    total.update(c)
print("TOTAL:", fmt(total), f"requests={total['requests']:,}")

today = datetime.date(2026, 8, 28)
cut30 = (today - datetime.timedelta(days=30)).isoformat()
last30 = collections.Counter()
n30 = 0
for d, c in by_day.items():
    if d >= cut30:
        last30.update(c)
        n30 += 1
print(f"LAST_30D ({n30} active days):", fmt(last30), f"requests={last30['requests']:,}")

print("\nBY MODEL (all time):")
for model, c in sorted(by_model.items(), key=lambda x: -(x[1]["input"] + x[1]["output"] + x[1]["cache_create"] + x[1]["cache_read"])):
    print(f"  {model}: {fmt(c)}")

print("\nLAST 30 DAYS, per day:")
for d in days:
    if d >= cut30:
        c = by_day[d]
        tot = c["input"] + c["output"] + c["cache_create"] + c["cache_read"]
        print(f"  {d}: total={tot:,} out={c['output']:,} req={c['requests']:,}")
