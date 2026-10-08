#!/usr/bin/env python3
"""P10: fit sklopa A05 posebej proti vsaki sodobni vasi."""
import json, math
import numpy as np
from scipy.spatial import cKDTree

M_LAT = 111320.0; M_LNG = 78014.0

boxes = json.load(open('/tmp/p10-buildings-a05.json'))
# JEDRO sklopa (po bigpicture x~75%, y~28% + zaznave): vzemimo ozko cono okoli centroida najgostejšega dela
P_all = np.array([(b[0], b[1]) for b in boxes if 0.05*2165 <= b[1] <= 0.55*2165 and 0.30*2634 <= b[0] <= 0.99*2634], dtype=float)
# DBSCAN-gosto jedro: točke z vsaj 3 sosedi v 60 px
from scipy.spatial import cKDTree as KT
t = KT(P_all)
dense = [i for i, p in enumerate(P_all) if t.query_ball_point(p, 60, return_length=True) if True]
cnt = t.query_ball_point(P_all, 60, return_length=True)
P = P_all[cnt >= 4]
print(f'A05 jedro: {len(P)} točk (od {len(P_all)})')

mods_all = []
for f in ['research/georef-n83/gurs/parcels-ko1544-merged.json', 'research/georef-n83/gurs/parcels-ko1552-merged.json']:
    for o in json.load(open(f)):
        a = o.get('a', o.get('geom_area', 9999))
        if a < 800:
            mods_all.append((o['lat'], o['lng']))

# kandidatne vasi (okvirji lat/lng)
CANDS = {
  'Fučkovci':      (45.5396, 45.5535, 15.2868, 15.3015),
  'Adlešiči-vas':  (45.522, 45.540, 15.290, 15.310),
  'Jankoviči':     (45.523, 45.545, 15.273, 15.293),
  'Dragoši':       (45.543, 45.563, 15.267, 15.300),
  'rečni-k.o.1544':(45.548, 45.558, 15.294, 15.302),
  'Bedenj-vzhod':  (45.530, 45.546, 15.270, 15.290),
}
pc = P.mean(axis=0)
results = {}
for name, (la0, la1, lo0, lo1) in CANDS.items():
    Q = np.array([((lng-lo0)*M_LNG, -(lat-la0)*M_LAT) for lat, lng in mods_all if la0 <= lat <= la1 and lo0 <= lng <= lo1])
    if len(Q) < 8: print(f'{name}: premalo ({len(Q)})'); continue
    tree = cKDTree(Q)
    qc = Q.mean(axis=0)
    best = None
    for d10 in range(-250, 251, 10):
        th = math.radians(d10/10)
        for s in [x/100 for x in range(45, 116, 3)]:
            co, si = math.cos(th), math.sin(th)
            X = (co*(P[:,0]-pc[0]) - si*(P[:,1]-pc[1]))*s
            Y = (si*(P[:,0]-pc[0]) + co*(P[:,1]-pc[1]))*s
            XY = np.column_stack([X+qc[0], Y+qc[1]])
            d, _ = tree.query(XY, k=1)
            sc = float(np.clip(1-(d-20)/60, 0, 1).mean())
            if best is None or sc > best[0]: best = (sc, d10/10, s)
    # fine
    for dd in [x/10 for x in range(-10, 11, 1)]:
        for ds in [x/100 for x in range(-3, 4, 1)]:
            th = math.radians(best[1]+dd); s = best[2]+ds/100
            co, si = math.cos(th), math.sin(th)
            X = (co*(P[:,0]-pc[0]) - si*(P[:,1]-pc[1]))*s
            Y = (si*(P[:,0]-pc[0]) + co*(P[:,1]-pc[1]))*s
            XY = np.column_stack([X+qc[0], Y+qc[1]])
            d, _ = tree.query(XY, k=1)
            sc = float(np.clip(1-(d-20)/60, 0, 1).mean())
            if sc > best[0]: best = (sc, best[1]+dd, s)
    results[name] = best
    print(f'{name}: score {best[0]:.3f}  rot {best[1]:+.1f}°  s {best[2]:.2f} m/px  (n={len(Q)})')
json.dump({k: [round(v[0],3), round(v[1],1), round(v[2],2)] for k, v in results.items()}, open('/tmp/p10-a05-cands.json','w'))
