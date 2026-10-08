#!/usr/bin/env python3
"""P10: A04 = celica cg BREZ rotacije — validacija s stavbami."""
import json, math
import numpy as np
from PIL import Image
from scipy import ndimage
from scipy.spatial import cKDTree

M = 111320.0; COS = math.cos(math.radians(45.55)); M_LNG = M*COS

# celica cg
LAT0, LAT1 = 45.5436, 45.5574
LNG0, LNG1 = 15.2728, 15.2973
W, H = 2645, 2158
sx = (LNG1-LNG0)*M_LNG/W  # m/px x
sy = (LAT1-LAT0)*M/H

a = np.asarray(Image.open('public/atlas/n83-a04.jpg').convert('L')).astype(float)
med = ndimage.median_filter(a, size=31)
dark = (a - med) < -20
dark = ndimage.binary_closing(dark, structure=np.ones((3,3)))
lab, n = ndimage.label(dark)
objs = ndimage.find_objects(lab)
pts = []
for i, sl in enumerate(objs):
    h = sl[0].stop-sl[0].start; w = sl[1].stop-sl[1].start
    if 7 <= w <= 45 and 7 <= h <= 35 and w*h >= 60:
        m = (lab[sl] == i+1)
        if m.mean() > 0.4:
            pts.append(((sl[1].start+sl[1].stop)/2, (sl[0].start+sl[0].stop)/2))
P = np.array(pts)
print(f'A04 zaznanih simbolov: {len(P)}')

# geo po celici (brez rotacije)
def px2geo(x, y):
    return (LAT1 - y*sy/M, LNG0 + x*sx/M_LNG)
G = np.array([px2geo(x, y) for x, y in P])

# sodobne stavbe v coni (k.o. 1544 + 1552 severni del)
mods = []
for f in ['research/georef-n83/gurs/parcels-ko1544-merged.json', 'research/georef-n83/gurs/parcels-ko1552-merged.json']:
    for o in json.load(open(f)):
        aA = o.get('a', o.get('geom_area', 9999))
        if aA < 800 and 45.535 <= o['lat'] <= 45.560 and 15.260 <= o['lng'] <= 15.305:
            mods.append((o['lat'], o['lng']))
Q = np.array(mods)
print(f'sodobnih točk: {len(Q)}')
tree = cKDTree(Q)
d, _ = tree.query(G, k=1)
sc = float(np.clip(1-(d-20)/60, 0, 1).mean())
print(f'A04-cg BREZ rotacije: score {sc:.3f}, mediana {np.median(d):.0f} m')

# nič-test (naključne rotacije okoli 0 s prosto translacijo v okviru)
import random
random.seed(5)
nulls = []
qc = Q.mean(axis=0)
pc = P.mean(axis=0)
for _ in range(60):
    th = math.radians(random.uniform(-25, 25)); s = random.uniform(0.6, 0.9)
    co, si = math.cos(th), math.sin(th)
    X = (co*(P[:,0]-pc[0]) - si*(P[:,1]-pc[1]))*s
    Y = (si*(P[:,0]-pc[0]) + co*(P[:,1]-pc[1]))*s
    lat = LAT1 - (Y+sy*H/2)/M; lng = LNG0 + (X+sx*W/2)/M_LNG
    # dodaj slučajni zamik ±300 m
    lat = lat + random.uniform(-0.003, 0.003); lng = lng + random.uniform(-0.004, 0.004)
    d2, _ = tree.query(np.column_stack([lat, lng]), k=1)
    nulls.append(float(np.clip(1-(d2-20)/60, 0, 1).mean()))
print(f'nič-test: medijana {np.median(nulls):.3f}, p95 {np.percentile(nulls,95):.3f}')

# kje so A04 stavbe v geo (grozdi)
import collections
cl = collections.Counter((round(la,3), round(lo,3)) for la, lo in G)
print('največji grozdi A04-stavb (lat, lng):', cl.most_common(10))
json.dump({'lat': G[:,0].tolist(), 'lng': G[:,1].tolist()}, open('/tmp/p10-a04-geo-unrot.json','w'))
