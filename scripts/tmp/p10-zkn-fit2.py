#!/usr/bin/env python3
"""P10: ZKN G4 fit s PROSTO translacijo (mrežno iskanje)."""
import json, math
import numpy as np
from scipy import ndimage
from scipy.spatial import cKDTree
from PIL import Image

M_LAT = 111320.0; M_LNG = 78014.0

a = np.asarray(Image.open('/tmp/ezkn-g0003.pgm')).astype(float)
H, W = a.shape
th = a.mean() - 40
dark = a < th
lab, n = ndimage.label(dark)
objs = ndimage.find_objects(lab)
pts = []
for i, sl in enumerate(objs):
    h = sl[0].stop - sl[0].start; w = sl[1].stop - sl[1].start
    if 12 <= w <= 130 and 12 <= h <= 130 and w*h >= 150:
        m = (lab[sl] == i+1)
        if m.mean() > 0.35:
            pts.append(((sl[1].start+sl[1].stop)/2, (sl[0].start+sl[0].stop)/2))
P = np.array(pts)
print(f'ZKN G4: {len(P)} simbolov')

mods = []
for o in json.load(open('research/georef-n83/gurs/parcels-ko1544-merged.json')):
    if o.get('geom_area', 9999) < 800 and o['lat'] < 45.560:
        mods.append((o['lat'], o['lng']))
Q = np.array([((lng-15.28)*M_LNG, -(lat-45.55)*M_LAT) for lat, lng in mods])
tree = cKDTree(Q)
print(f'sodobne (jug): {len(Q)}')

pc = P.mean(axis=0)
Pc = P - pc
best = (-1.0, 0.0, 0.24, 0, 0)
# rot ∈ {-6..+6}, s ∈ {0.20..0.29}, translacija mreža ±1200 m po x, ±800 po y (korak 40)
for deg in [x/2 for x in range(-12, 13)]:
    co, si = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    R0 = (co*Pc[:,0] - si*Pc[:,1]); R1 = (si*Pc[:,0] + co*Pc[:,1])
    for s in [x/1000 for x in range(200, 291, 5)]:
        X0 = R0*s; Y0 = R1*s
        for tx in range(-1200, 1201, 40):
            for ty in range(-800, 801, 40):
                XY = np.column_stack([X0+tx, Y0+ty])
                # hitri preskus samo na podmnožici
                d, _ = tree.query(XY[::4], k=1)
                sc = float(np.clip(1-(d-15)/45, 0, 1).mean())
                if sc > best[0]:
                    d2, _ = tree.query(XY, k=1)
                    sc2 = float(np.clip(1-(d2-15)/45, 0, 1).mean())
                    if sc2 > best[0]: best = (sc2, deg, s, tx, ty)
print(f'NAJBOLJŠE: score {best[0]:.3f}, rot {best[1]:.1f}°, s {best[2]:.3f} m/px, t=({best[3]},{best[4]}) m')
# geo oglišča
deg, s, tx, ty = best[1], best[2], best[3], best[4]
co, si = math.cos(math.radians(deg)), math.sin(math.radians(deg))
def px2geo(x, y):
    X = (co*(x-pc[0]) - si*(y-pc[1]))*s + tx
    Y = (si*(x-pc[0]) + co*(y-pc[1]))*s + ty
    return (45.55 - Y/M_LAT, 15.28 + X/M_LNG)
corners = {'NW': px2geo(0,0), 'NE': px2geo(W,0), 'SW': px2geo(0,H), 'SE': px2geo(W,H)}
for k, v in corners.items(): print(f'  {k}: {v[0]:.5f} {v[1]:.5f}')
json.dump({'score': best[0], 'rot': deg, 'scale': s, 'tx': tx, 'ty': ty, 'corners': corners, 'n': len(P)}, open('/tmp/p10-zkn-fit2.json','w'))
