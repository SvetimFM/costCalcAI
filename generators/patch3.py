p = 'build_infographic2.py'
src = open(p).read()
def rep(a, b):
    global src
    assert a in src, "MISSING: " + a[:60]
    src = src.replace(a, b)

# S2 annotation: start further left so it fits
rep('hand(470, leg_y + 37, "open models are 3 pts behind — but only at sizes no desk can serve!", 17, -1)',
    'hand(330, leg_y + 37, "open models are 3 pts behind — but only at sizes no desk can serve!", 17, -1)')

# scatter: lift plan labels into the empty zone above the cluster, longer leaders
rep('''plans = [(0, "free tiers", 4, -22, 0), (20, "$17–20 Pro / Plus", 6, 0, -16),
         (100, "$100 mid tiers", 9, -14, -33), (200, "$200 top tiers · Max 20x etc.", 12, 6, -51)]
for d_, lab_, r_, jx_, dy_ in plans:
    dot(63, d_, BLUE, r_, jx_)
    ly_ = sy(0) + dy_
    T(700, ly_ + 4, lab_, 11.5, SUB, "600", "end")
    L(704, ly_, sx(63) + jx_ - r_ - 2, sy(d_), "#b9b8b2", 1)''',
'''plans = [(200, "$200 top tiers (Max 20x…)", 12, 6, 112), (100, "$100 mid tiers", 9, -14, 132),
         (20, "$17–20 Pro / Plus", 6, 0, 152), (0, "free tiers", 4, -22, 172)]
for d_, lab_, r_, jx_, dy_ in plans:
    dot(63, d_, BLUE, r_, jx_)
    ly_ = py1 + dy_
    T(730, ly_ + 4, lab_, 11.5, SUB, "600", "end")
    L(734, ly_, sx(63) + jx_ - 2, sy(d_) - r_ - 1, "#b9b8b2", 1)''')

# reposition "same rigs..." into the clear zone under the dark cluster
rep('hand(sx(50) + 30, sy(1430), "same rigs with your time priced in", 17, -1)',
    'hand(300, sy(1160), "same rigs with your time priced in", 17, -1)')

open(p, 'w').write(src)
print("patched ok")
