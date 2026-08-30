p = 'build_infographic2.py'
src = open(p).read()
def rep(a, b):
    global src
    assert a in src, "MISSING: " + a[:60]
    src = src.replace(a, b)

# 1. four label rows, two labels max each — kills the row-2 collision
rep('''rigs = [("2×3090", 48, 0, 86, 1111, -176), ("RTX 5090", 48, 14, 128, 1153, -152),
        ("Strix Halo", 52, -8, 91, 1116, -176), ("DGX Spark", 52, 10, 120, 1145, -152),
        ("Mac 256GB", 53, 0, 193, 1218, -128), ("Mac 512GB", 56, 0, 296, 1321, -176)]''',
'''rigs = [("2×3090", 48, 0, 86, 1111, -176), ("RTX 5090", 48, 14, 128, 1153, -154),
        ("Strix Halo", 52, -8, 91, 1116, -132), ("DGX Spark", 52, 10, 120, 1145, -110),
        ("Mac 256GB", 53, 0, 193, 1218, -176), ("Mac 512GB", 56, 0, 296, 1321, -154)]''')

# 2. card: last tier label breathing room
rep('("$100", "mid tiers", 9), ("$200", "Max 20x · GPT Pro · Ultra", 12)',
    '("$100", "mid tiers", 9), ("$200", "Max 20x · Pro · Ultra", 12)')

# 3. drop the stubby arrow — text sits right against the ellipse
rep('arrow(718, py0 - 14, 736, py0 - 30, bend=6)\n', '')

# 4. shorten right-edge-clipped source lines
rep('"Sources — quality: Artificial Analysis Intelligence Index v4.1.1 (artificialanalysis.ai), retrieved Aug 28 2026 · plan prices: published Anthropic / OpenAI / Google tiers, verified Aug 28 2026 ·"',
    '"Sources — quality: Artificial Analysis Intelligence Index v4.1.1, retrieved Aug 28 2026 · plan prices: Anthropic / OpenAI / Google published tiers, verified Aug 28 2026"')
rep('"Sources: r/LocalLLaMA build threads · US retailer street prices &amp; apple.com list / Apple Upgrade lease pricing, Aug 28 2026 · $/mo — companion TCO model (3-yr, resale- &amp; power-adjusted)"',
    '"Sources: r/LocalLLaMA build threads · US street &amp; apple.com list / lease prices, Aug 28 2026 · $/mo — companion TCO model (3-yr, resale- &amp; power-adjusted)"')

open(p, 'w').write(src)
print("patched ok")
