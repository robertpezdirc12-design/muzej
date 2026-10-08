#!/usr/bin/env python3
"""P10: validacija A05↔Fučkovci fita (nič-test + prosta translacija)."""
import json, math, random
import numpy as np
from scipy.spatial import cKDTree

M_LAT = 111320.0; M_LNG = 78014.0
boxes = json.load(open('/tmp/p10-buildings-a05.json'))
from scipy.spatial import cKDTree as KT
P_all = np.array([(b[0], b[1]) for b in boxes if 0.05*2165 <= b[1] <= 0.55*2165 and 0.30*2634 <= b[0] <= 0.99*2634], dtype=float)
t = KT(P_all)
cnt = t.query_ball_point(P_all, 60, return_length=True)
P = P_all[cnt >= 4]

mods_all = []
for f in ['research/georef-n83/gurs/parcels-ko1544-merged.json', 'research/georef-n83/gurs/parcels-ko1552-merged.json']:
    for o in json.load(open(f)):
        a = o.get('a', o.get('geom_area', 9999))
        if a < 800: mods_all.append((o['lat'], o['lng']))

la0, la1, lo0, lo1 = 45.5396, 45.5535, 15.2868, 15.3015
Q = np.array([((lng-lo0)*M_LNG, -(lat-la0)*M_LAT) for lat, lng in mods_all if la0 <= lat <= la1 and lo0 <= lng <= lo1])
tree = cKDTree(Q)
qc = Q.mean(axis=0)
pc = P.mean(axis=0)

def sc_at(theta, s, tx, ty):
    co, si = math.cos(theta), math.sin(theta)
    X = (co*(P[:,0]-pc[0]) - si*(P[:,1]-pc[1]))*s + qc[0] + tx
    Y = (si*(P[:,0]-pc[0]) + co*(P[:,1]-pc[1]))*s + qc[1] + ty
    d, _ = tree.query(np.column_stack([X, Y]), k=1)
    return float(np.clip(1-(d-20)/60, 0, 1).mean()), float(np.median(d))

# 1) nič-test: 100 naključnih (rot, s) okoli fučkovskega fita + CENTROID zamik
random.seed(7)
nulls = []
for _ in range(100):
    th = math.radians(random.uniform(-25, 25)); s = random.uniform(0.45, 0.8)
    sc, md = sc_at(th, s, 0, 0)
    nulls.append(sc)
print(f'NIČ-TEST (centroid fiksan, naključni rot/s): medijana {np.median(nulls):.3f}, 95. percentil {np.percentile(nulls,95):.3f}')

# 2) prosta translacija okoli najboljšega
best = (0.914, 10.6, 0.48, 0.0, 0.0)
for it in range(3):
    step = [60, 25, 10][it]
    improved = True
    while improved:
        improved = False
        for dx in [-step, 0, step]:
            for dy in [-step, 0, step]:
                sc, md = sc_at(math.radians(best[1]), best[2], best[3]+dx, best[4]+dy)
                if sc > best[0] + 0.0005:
                    best = (sc, best[1], best[2], best[3]+dx, best[4]+dy); improved = True
print(f'PROSTA TRANSLACIJA: score {best[0]:.3f}, rot {best[1]:.1f}°, s {best[2]:.2f}, t=({best[3]:.0f},{best[4]:.0f}) m od centroida')

# 3)robni zapis geo-pozicij A05 oglišč
deg, s = best[1], best[2]
co, si = math.cos(math.radians(deg)), math.sin(math.radians(deg))
def px2geo(x, y):
    X = (co*(x-pc[0]) - si*(y-pc[1]))*s + qc[0] + best[3]
    Y = (si*(x-pc[0]) + co*(y-pc[1]))*s + qc[1] + best[4]
    return (la0 - Y/M_LAT, lo0 + X/M_LNG)
W, H = 2634, 2165
corners = {'NW': px2geo(0,0), 'NE': px2geo(W,0), 'SW': px2geo(0,H), 'SE': px2geo(W,H)}
for k, v in corners.items(): print(f'  {k}: {v[0]:.5f} {v[1]:.5f}')
json.dump({'score': best[0], 'rot': deg, 'scale': s, 'tx': best[3], 'ty': best[4], 'corners': corners}, open('/tmp/p10-fit-a05-final.json','w'))
