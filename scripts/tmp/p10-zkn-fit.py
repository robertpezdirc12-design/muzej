#!/usr/bin/env python3
"""P10: georeferenca ZKN 'GRIBLJE 4' (1970) prek sodobnih stavbnih parcel GURS."""
import json, math
import numpy as np
from scipy import ndimage
from scipy.spatial import cKDTree

M_LAT = 111320.0; M_LNG = 78014.0

# ZKN G4 detekcija (z velikostmi)
im = np.asarray(Image.open if False else None) if False else None
from PIL import Image
a = np.asarray(Image.open('/tmp/ezkn-g0003.pgm')).astype(float)
H, W = a.shape
th = a.mean() - 40
dark = a < th
lab, n = ndimage.label(dark)
objs = ndimage.find_objects(lab)
pts = []
for i, sl in enumerate(objs):
    h = sl[0].stop - sl[0].start; w = sl[1].stop - sl[1].start
    if 18 <= w <= 130 and 18 <= h <= 130 and w*h >= 400:
        m = (lab[sl] == i+1)
        if m.mean() > 0.4:
            pts.append(((sl[1].start+sl[1].stop)/2, (sl[0].start+sl[0].stop)/2))
print(f'ZKN G4 (velike simbole): {len(pts)}')
P = np.array(pts)

# sodobne stavbe (vse male parcele k.o. 1544 + okoliških k.o. — samo cona)
mods = []
for f in ['research/georef-n83/gurs/parcels-ko1544-merged.json']:
    for o in json.load(open(f)):
        if o.get('geom_area', 9999) < 800:
            mods.append((o['lat'], o['lng']))
Q = np.array([((lng-15.28)*M_LNG, -(lat-45.55)*M_LAT) for lat, lng in mods])
tree = cKDTree(Q)
print(f'sodobnih točk: {len(Q)}')

pc = P.mean(axis=0)
best = None
for deg in [x/2 for x in range(-40, 41)]:
    for s in [x/1000 for x in range(190, 311, 5)]:
        co, si = math.cos(math.radians(deg)), math.sin(math.radians(deg))
        # zaradi velike translacijske negotovosti: poravnaj centroida
        X = (co*(P[:,0]-pc[0]) - si*(P[:,1]-pc[1]))*s
        Y = (si*(P[:,0]-pc[0]) + co*(P[:,1]-pc[1]))*s
        qc = Q.mean(axis=0)
        XY = np.column_stack([X+qc[0], Y+qc[1]])
        d, _ = tree.query(XY, k=1)
        sc = float(np.clip(1-(d-15)/45, 0, 1).mean())
        if best is None or sc > best[0]: best = (sc, deg, s)
print(f'grobo: score {best[0]:.3f}, rot {best[1]:.1f}°, s {best[2]:.3f} m/px (nominal 0.244)')

# nič-test za primerjavo
import random
random.seed(3)
nulls = []
for _ in range(50):
    deg = random.uniform(-20, 20); s = random.uniform(0.2, 0.3)
    co, si = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    X = (co*(P[:,0]-pc[0]) - si*(P[:,1]-pc[1]))*s
    Y = (si*(P[:,0]-pc[0]) + co*(P[:,1]-pc[1]))*s
    qc = Q.mean(axis=0)
    XY = np.column_stack([X+qc[0], Y+qc[1]])
    d, _ = tree.query(XY, k=1)
    nulls.append(float(np.clip(1-(d-15)/45, 0, 1).mean()))
print(f'nič-test: medijana {np.median(nulls):.3f}, p95 {np.percentile(nulls,95):.3f}')
json.dump({'best': best, 'null_med': float(np.median(nulls))}, open('/tmp/p10-zkn-fit.json','w'))
