#!/usr/bin/env python3
"""P10: podobnostni fit sklopa stavb A05 (1825, px) → sodobne stavbne parcele (GURS)."""
import json, math
import numpy as np
from scipy.spatial import cKDTree

M_LAT = 111320.0; M_LNG = 78014.0

# 1825 točke (detekcija na A05)
boxes = json.load(open('/tmp/p10-buildings-a05.json'))
# sklop + zgornji trak (brez okvirja na y>85%)
P = np.array([(b[0], b[1]) for b in boxes if 0.05*2165 <= b[1] <= 0.52*2165 and 0.28*2634 <= b[0] <= 0.99*2634], dtype=float)
print(f'A05 točk: {len(P)}')

# sodobne točke: vse male parcele iz obeh k.o. v coni
mods = []
for f in ['research/georef-n83/gurs/parcels-ko1544-merged.json', 'research/georef-n83/gurs/parcels-ko1552-merged.json']:
    for o in json.load(open(f)):
        if o.get('a', o.get('geom_area', 9999)) < 800 and 45.515 <= o['lat'] <= 45.565 and 15.27 <= o['lng'] <= 15.315:
            mods.append(((o['lng']-15.29)*M_LNG, -(o['lat']-45.54)*M_LAT))  # lokalni m, izhodišče (15.29, 45.54)
Q = np.array(mods)
print(f'sodobnih točk v coni: {len(Q)}')
tree = cKDTree(Q)

pc = P.mean(axis=0); qc = Q.mean(axis=0)

def score(theta, s):
    co, si = math.cos(theta), math.sin(theta)
    X = (co*(P[:,0]-pc[0]) - si*(P[:,1]-pc[1]))*s
    Y = (si*(P[:,0]-pc[0]) + co*(P[:,1]-pc[1]))*s
    XY = np.column_stack([X+qc[0], Y+qc[1]])
    d, _ = tree.query(XY, k=1)
    # mehka točkovalnica: 50 % do 25 m, 0 pri 80 m
    sc = np.clip(1 - (d-25)/55, 0, 1)
    return float(sc.mean()), float(np.median(d))

best = None
for deg10 in range(-300, 301, 5):
    th = math.radians(deg10/10)
    for s in [x/100 for x in range(40, 121, 2)]:
        sc, md = score(th, s)
        if best is None or sc > best[0]:
            best = (sc, md, deg10/10, s)
print(f'GROBO najboljše: score {best[0]:.3f}, mediana {best[1]:.0f} m, rot {best[2]:.1f}°, s {best[3]:.2f} m/px')

# fine
b0 = best
for dd in [x/10 for x in range(-30, 31, 1)]:
    th = math.radians(b0[2]+dd)
    for ds in [x/1000 for x in range(-25, 26, 5)]:
        s = b0[3]+ds
        if s <= 0.1: continue
        sc, md = score(th, s)
        if sc > b0[0]:
            b0 = (sc, md, b0[2]+dd, s)
print(f'FINO najboljše: score {b0[0]:.3f}, mediana {b0[1]:.0f} m, rot {b0[2]:.1f}°, s {b0[3]:.3f} m/px')

# izpiši geo pozicije oglišč lista A05 pod najboljšo fito
deg, s = b0[2], b0[3]
co, si = math.cos(math.radians(deg)), math.sin(math.radians(deg))
def px2geo(x, y):
    X = (co*(x-pc[0]) - si*(y-pc[1]))*s
    Y = (si*(x-pc[0]) + co*(y-pc[1]))*s
    ex, ey = X+qc[0], Y+qc[1]
    return (45.54 - ey/M_LAT, 15.29 + ex/M_LNG)
W, H = 2634, 2165
corners = {'NW': px2geo(0,0), 'NE': px2geo(W,0), 'SW': px2geo(0,H), 'SE': px2geo(W,H), 'center': px2geo(W/2, H/2)}
for k, v in corners.items(): print(f'  {k}: {v[0]:.5f}, {v[1]:.5f}')
json.dump({'score': b0[0], 'medianD': b0[1], 'rotDeg': deg, 'scaleM': s, 'corners': corners, 'n1825': len(P), 'nModern': len(Q)},
          open('/tmp/p10-fit-a05.json', 'w'))
