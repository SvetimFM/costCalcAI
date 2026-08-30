import io
p = 'build_infographic2.py'
src = open(p).read()
n0 = len(src)

def rep(a, b):
    global src
    assert a in src, "MISSING: " + a[:60]
    src = src.replace(a, b)

# 1. cards: narrower + tighter grid
rep('cx0, cy0 = 52 + c_ * 300, 210 + r_ * 172', 'cx0, cy0 = 52 + c_ * 296, 210 + r_ * 172')
rep('R(cx0, cy0, 288, 160, "#f6f5f2", rx=12)', 'R(cx0, cy0, 280, 160, "#f6f5f2", rx=12)')

# 2. S2 note + relocate hand annotation
rep('"cloud only · inside every $20–200 plan"', '"cloud only · in every plan"')
rep('hand(640, m_y + 60, "3 pts behind — but only at server scale!", 18, -2)',
    'hand(470, leg_y + 37, "open models are 3 pts behind — but only at sizes no desk can serve!", 17, -1)')

# 3. scatter plan labels -> left fan with leaders
rep('''dot(63, 0, BLUE, 4, -22); dot(63, 20, BLUE, 6); dot(63, 100, BLUE, 9, -14); dot(63, 200, BLUE, 12, 6)
T(sx(63) + 26, sy(200) + 4, "$200 Max 20x / Pro 20x / Ultra", 11.5, SUB, "600")
T(sx(63) + 20, sy(100) - 8, "$100 mid tiers", 11.5, SUB, "600")
T(sx(63) + 16, sy(20) - 14, "$17–20 Pro / Plus", 11.5, SUB, "600")
T(sx(63) - 30, sy(0) - 12, "free tiers", 11.5, SUB, "600", "end")''',
'''plans = [(0, "free tiers", 4, -22, 0), (20, "$17–20 Pro / Plus", 6, 0, -16),
         (100, "$100 mid tiers", 9, -14, -33), (200, "$200 top tiers · Max 20x etc.", 12, 6, -51)]
for d_, lab_, r_, jx_, dy_ in plans:
    dot(63, d_, BLUE, r_, jx_)
    ly_ = sy(0) + dy_
    T(700, ly_ + 4, lab_, 11.5, SUB, "600", "end")
    L(704, ly_, sx(63) + jx_ - r_ - 2, sy(d_), "#b9b8b2", 1)''')
rep('scribble(sx(63) - 4, sy(90), 58, 84)', 'scribble(sx(63) - 2, sy(95), 52, 42)')
rep('''hand(sx(63) - 74, sy(330), "the corner you want!", 19, -3, "end")
hand(sx(50) + 30, sy(1420), "same rigs with your time priced in", 17, -1)''',
'''hand(600, sy(430), "the corner you want!", 19, -3, "end")
arrow(606, sy(430) - 6, sx(63) - 44, sy(200) - 26, bend=20)
hand(sx(50) + 30, sy(1430), "same rigs with your time priced in", 17, -1)''')

# 4. tiles text
rep('"per task vs 1 for Claude — controlled study"', '"vs 1 for Claude · controlled study"')
rep('"quantization degrades exactly what agents need"', '"quantization breaks agent formatting"')

# 5. quote attribution
rep('"— Mac Studio 128GB owner, Hacker News, June 2026 · At team scale: a firm with €440k/yr Claude spend asked publicly for one working local replacement — none was offered."',
    '"— Mac Studio 128GB owner, HN, June 2026 · Team scale: a €440k/yr Claude shop publicly asked for one working local replacement — got none."')

# 6. case-study strip rebuild
i0 = src.index('# feasibility dot strip')
i1 = src.index('T(64, cs_y + 320,')
new = '''# feasibility dot strip
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
'''
src = src[:i0] + new + src[i1:]

# 7. verdict spacing + band height
rep('T(64, cs_y + 320, "No rig', 'T(64, cs_y + 328, "No rig')
rep('T(64, cs_y + 341, "For a heavy user', 'T(64, cs_y + 349, "For a heavy user')
rep('R(40, cs_y, 860, 360, "#fdf2ec"', 'R(40, cs_y, 860, 372, "#fdf2ec"')

open(p, 'w').write(src)
print("patched", n0, "->", len(src))
