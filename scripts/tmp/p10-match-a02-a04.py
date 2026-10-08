#!/usr/bin/env python3
"""P10: RANSAC registracija A02 (jug) ↔ A04 (sever) — prekrivanje listov prek skupnih stavb."""
import math, random, json
import numpy as np
from PIL import Image
from scipy import ndimage
from collections import defaultdict

def detect(f, x0, x1, y0, y1):
    a = np.asarray(Image.open(f).convert('L')).astype(float)
    med = ndimage.median_filter(a, size=31)
    dark = (a - med) < -20
    dark = ndimage.binary_closing(dark, structure=np.ones((3,3)))
    lab, n = ndimage.label(dark)
    objs = ndimage.find_objects(lab)
    pts = []
    for i, sl in enumerate(objs):
        cy = (sl[0].start+sl[0].stop)/2; cx = (sl[1].start+sl[1].stop)/2
        h = sl[0].stop-sl[0].start; w = sl[1].stop-sl[1].start
        if 7 <= w <= 45 and 7 <= h <= 35 and x0 <= cx <= x1 and y0 <= cy <= y1:
            pts.append((cx, cy))
    return np.array(pts)

P2 = detect('public/atlas/n83-a02.jpg', 950, 2600, 1600, 2158)  # A02 južni rob
P4 = detect('public/atlas/n83-a04.jpg', 0, 2645, 0, 700)        # A04 severni rob
print(f'A02-jug: {len(P2)}; A04-sever: {len(P4)}')
random.seed(11)
best = None
t2grid = defaultdict(list)
for x, y in P2: t2grid[(int(x//15), int(y//15))].append((x, y))

for it in range(150000):
    i, j, k = random.sample(range(len(P4)), 3)
    a, b, c = P4[i], P4[j], P4[k]
    d_ab = math.hypot(a[0]-b[0], a[1]-b[1])
    if not (40 < d_ab < 600): continue
    i2, j2, k2 = random.sample(range(len(P2)), 3)
    p, q, r = P2[i2], P2[j2], P2[k2]
    d_ab2 = math.hypot(p[0]-q[0], p[1]-q[1])
    s = d_ab2/d_ab
    if not (0.6 < s < 1.8): continue
    d_bc = math.hypot(b[0]-c[0], b[1]-c[1])*s
    d_ca = math.hypot(c[0]-a[0], c[1]-a[1])*s
    if abs(d_bc - math.hypot(q[0]-r[0], q[1]-r[1])) > 8: continue
    if abs(d_ca - math.hypot(r[0]-p[0], r[1]-p[1])) > 8: continue
    dx, dy = a[0]-b[0], a[1]-b[1]
    ex, ey = p[0]-q[0], p[1]-q[1]
    n3 = dx*dx+dy*dy; n2 = ex*ex+ey*ey
    if n3 < 1 or n2 < 1: continue
    co = (dx*ex+dy*ey)/math.sqrt(n3*n2)
    si = (dx*ey-dy*ex)/math.sqrt(n3*n2)
    if not (-1 <= co <= 1 and -1 <= si <= 1): continue
    s2 = math.sqrt(n2/n3)
    if not (0.6 < s2 < 1.8): continue
    theta = math.degrees(math.atan2(si, co))
    if not (-180 <= theta <= 180): continue
    tx = p[0] - s2*(co*a[0]-si*a[1])
    ty = p[1] - s2*(si*a[0]+co*a[1])
    cx2 = s2*(co*c[0]-si*c[1]) + tx
    cy2 = s2*(si*c[0]+co*c[1]) + ty
    if math.hypot(cx2-r[0], cy2-r[1]) > 9: continue
    Xf = s2*(co*P4[:,0]-si*P4[:,1]) + tx
    Yf = s2*(si*P4[:,0]+co*P4[:,1]) + ty
    matches = 0
    for xf, yf in zip(Xf, Yf):
        key = (int(xf//15), int(yf//15))
        for qx, qy in t2grid.get(key, []):
            if math.hypot(xf-qx, yf-qy) < 8:
                matches += 1; break
    if matches >= 7:
        if best is None or matches > best[0]:
            best = (matches, round(theta,2), round(s2,4), round(tx,1), round(ty,1))
            print(f'  {matches} ujemanj: rot {theta:.2f}°, s {s2:.3f}, t ({tx:.0f},{ty:.0f})')

if best:
    print('\nNAJBOLJŠI:', best)
    # pari
    co, si = math.cos(math.radians(best[1])), math.sin(math.radians(best[1]))
    s = best[2]
    Xf = s*(co*P4[:,0]-si*P4[:,1]) + best[3]
    Yf = s*(si*P4[:,0]+co*P4[:,1]) + best[4]
    pairs = []
    for idx, (xf, yf) in enumerate(zip(Xf, Yf)):
        key = (int(xf//15), int(yf//15))
        for qx, qy in t2grid.get(key, []):
            if math.hypot(xf-qx, yf-qy) < 8:
                pairs.append((round(qx), round(qy), round(P4[idx][0]), round(P4[idx][1]))); break
    print('pari (A02px ← A04px):', pairs[:20])
    json.dump(best, open('/tmp/p10-match-a02a04.json','w'))
else:
    print('NI ujemanj.')
