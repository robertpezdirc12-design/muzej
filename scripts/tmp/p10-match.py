#!/usr/bin/env python3
"""P10: točkovno-parna registracija A02↔A03 (RANSAC podobnostne preslikave).
Če se lista prekrivata, skupne stavbe določijo rotacijo+merilo+translacijo."""
import json, math, random
import numpy as np
from PIL import Image
from scipy import ndimage

def detect(f, x0, x1, y0, y1, W, H):
    im = Image.open(f).convert('L')
    a = np.asarray(im).astype(float)
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

# A02: pas vasi + južni trak (celoten pas x 950–2600, y 900–2158)
P2 = detect('public/atlas/n83-a02.jpg', 950, 2600, 900, 2158, 3010, 2158)
# A03: pas (x 2000–2550, y 0–1300)
P3 = detect('public/atlas/n83-a03.jpg', 2000, 2550, 0, 1300, 2645, 2154)
print(f'A02 točk: {len(P2)}; A03 točk: {len(P3)}')

random.seed(42)
best = None
N_TRIES = 60000
t2 = [tuple(p) for p in P2]
for it in range(N_TRIES):
    # trikotnik iz A03
    i, j, k = random.sample(range(len(P3)), 3)
    a, b, c = P3[i], P3[j], P3[k]
    d_ab3 = math.hypot(a[0]-b[0], a[1]-b[1])
    if not (40 < d_ab3 < 700): continue
    # trikotnik iz A02 z istim razmerjem stranic (znotraj tolerance)
    i2, j2, k2 = random.sample(range(len(P2)), 3)
    p, q, r = P2[i2], P2[j2], P2[k2]
    d_ab2 = math.hypot(p[0]-q[0], p[1]-q[1])
    s = d_ab2 / d_ab3  # merilo A02px/A03px
    if not (0.8 < s < 1.25): continue
    # preveri obe drugi stranici
    d_bc3 = math.hypot(b[0]-c[0], b[1]-c[1]) * s
    d_ca3 = math.hypot(c[0]-a[0], c[1]-a[1]) * s
    d_bc2 = math.hypot(q[0]-r[0], q[1]-r[1])
    d_ca2 = math.hypot(r[0]-p[0], r[1]-p[1])
    big = max(d_bc2, d_ca2, d_ab2)
    tol = max(6.0, big*0.04)
    if abs(d_bc3-d_bc2) > tol or abs(d_ca3-d_ca2) > tol: continue
    # podobnostna preslikava: P3 → A02 px: rot θ, merilo s, translacija
    # reši iz dvojic (a→p, b→q)
    dx, dy = a[0]-b[0], a[1]-b[1]
    ex, ey = p[0]-q[0], p[1]-q[1]
    n3 = dx*dx+dy*dy; n2 = ex*ex+ey*ey
    if n3 < 1 or n2 < 1: continue
    sc = n2/n3
    co = (dx*ex+dy*ey)/math.sqrt(n3*n2)
    si = (dx*ey-dy*ex)/math.sqrt(n3*n2)
    if not (-1 <= co <= 1 and -1 <= si <= 1): continue
    s2 = math.sqrt(sc)
    if not (0.8 < s2 < 1.25): continue
    theta = math.atan2(si, co)
    deg = math.degrees(theta)
    if not (-30 < deg < 30): continue
    tx = p[0] - s2*(co*a[0]-si*a[1])
    ty = p[1] - s2*(si*a[0]+co*a[1])
    # preveri tretjo točko
    cx2 = s2*(co*c[0]-si*c[1]) + tx
    cy2 = s2*(si*c[0]+co*c[1]) + ty
    if math.hypot(cx2-r[0], cy2-r[1]) > 8: continue
    # štej ujemanja: preslikaj VSE točke A03 → A02 in preveri bližino
    X3 = P3[:,0]; Y3 = P3[:,1]
    Xf = s2*(co*X3 - si*Y3) + tx
    Yf = s2*(si*X3 + co*Y3) + ty
    # grid hash točk A02
    matches = 0
    from collections import defaultdict
    grid = defaultdict(list)
    for (qx2, qy2) in t2:
        grid[(int(qx2//15), int(qy2//15))].append((qx2, qy2))
    for xf, yf in zip(Xf, Yf):
        key = (int(xf//15), int(yf//15))
        for qx2, qy2 in grid.get(key, []):
            if math.hypot(xf-qx2, yf-qy2) < 7:
                matches += 1; break
    if matches >= 6:
        if best is None or matches > best['m']:
            best = {'m': matches, 'deg': round(deg,2), 's': round(s2,4), 'tx': round(tx,1), 'ty': round(ty,1)}
            print(f'  kandidat: {matches} ujemanj, rot {deg:.2f}°, s {s2:.3f}, t ({tx:.0f},{ty:.0f})')

if best:
    print('\nNAJBOLJŠI:', best)
    # izpiši ujemanja podrobno
    co = math.cos(math.radians(best['deg'])); si = math.sin(math.radians(best['deg']))
    s = best['s']
    Xf = s*(co*P3[:,0] - si*P3[:,1]) + best['tx']
    Yf = s*(si*P3[:,0] + co*P3[:,1]) + best['ty']
    from collections import defaultdict
    grid = defaultdict(list)
    for (qx2, qy2) in t2: grid[(int(qx2//15), int(qy2//15))].append((qx2, qy2))
    pairs = []
    for idx, (xf, yf) in enumerate(zip(Xf, Yf)):
        key = (int(xf//15), int(yf//15))
        for qx2, qy2 in grid.get(key, []):
            if math.hypot(xf-qx2, yf-qy2) < 7:
                pairs.append((round(xf), round(yf), round(P3[idx][0]), round(P3[idx][1]))); break
    print('pari (A02x,A02y ← A03x,A03y):', pairs[:25])
    json.dump(best, open('/tmp/p10-match-a02-a03.json','w'))
else:
    print('NI ujemanj — lista se ne prekrivata (ali detektor premalo točk).')
