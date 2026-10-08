#!/usr/bin/env python3
"""P10: A04 PONOVNA georeferenca — river trace ↔ Kolpa pri celici cg (ne ovin Adlešiči!)."""
import json, math
import numpy as np
from scipy.optimize import least_squares

M = 111320.0
COS = math.cos(math.radians(45.55))

MODERN = np.array(json.load(open('research/georef-n83/kolpa-modern-centerline.json')))
# SAMO segment lat 45.542–45.559 (celica cg vzhodni rob)
seg = MODERN[(MODERN[:,0] >= 45.542) & (MODERN[:,0] <= 45.559)]
MODERN_M = np.stack([seg[:,1]*M*COS, seg[:,0]*M], axis=1)
print(f'moderna struga (segment cg): {len(MODERN_M)} točk, lat {seg[:,0].min():.4f}-{seg[:,0].max():.4f}, lng {seg[:,1].min():.4f}-{seg[:,1].max():.4f}')

d = json.load(open('research/georef-n83/p9b-a04-refined.json'))
pts = np.array([[p[0], p[1]] for p in d['seeds']], dtype=float)
print(f'A04 sled reke: {len(pts)} točk ({pts[0][0]:.0f},{pts[0][1]:.0f}) → ({pts[-1][0]:.0f},{pts[-1][1]:.0f})')

def dist_to_river(pts_m):
    dmin = np.full(len(pts_m), 1e9)
    a = MODERN_M[:-1]; b = MODERN_M[1:]
    for i in range(len(a)):
        ab = b[i]-a[i]; L2 = float(ab@ab)
        if L2 < 1e-6: continue
        t = np.clip(((pts_m-a[i])@ab)/L2, 0, 1)
        proj = a[i] + t[:,None]*ab
        dmin = np.minimum(dmin, np.hypot(*(pts_m-proj).T))
    return dmin

best = None
# mreža: rot -180..180 (10°), s 0.5–1.6; translacija = centroid struge na centroid segmenta
c_river_px = pts.mean(axis=0)
c_target = MODERN_M.mean(axis=0)
for th10 in range(-180, 180, 10):
    for s in [x/100 for x in range(50, 161, 5)]:
        co, si = math.cos(math.radians(th10)), math.sin(math.radians(th10))
        X = (co*(pts[:,0]-c_river_px[0]) - si*(pts[:,1]-c_river_px[1]))*s + c_target[0]
        Y = (si*(pts[:,0]-c_river_px[0]) + co*(pts[:,1]-c_river_px[1]))*s + c_target[1]
        d = dist_to_river(np.column_stack([X, Y]))
        med = float(np.median(d))
        if best is None or med < best[0]:
            best = (med, th10, s)
print(f'grobo: mediana {best[0]:.0f} m, rot {best[1]}°, s {best[2]:.2f}')

# natančno (least_squares, 4 parametri: θ, s, tx, ty)
def resid(p):
    th, s, tx, ty = p
    co, si = math.cos(th), math.sin(th)
    X = (co*pts[:,0] - si*pts[:,1])*s + tx
    Y = (si*pts[:,0] + co*pts[:,1])*s + ty
    return dist_to_river(np.column_stack([X, Y]))
th0, s0 = math.radians(best[1]), best[2]
co, si = math.cos(th0), math.sin(th0)
tx0 = c_target[0] - s0*(co*c_river_px[0] - si*c_river_px[1])
ty0 = c_target[1] - s0*(si*c_river_px[0] + co*c_river_px[1])
sol = least_squares(resid, [th0, s0, tx0, ty0], bounds=([-math.pi, 0.3, -1e9, -1e9], [math.pi, 2.5, 1e9, 1e9]))
th, s, tx, ty = sol.x
med = float(np.median(resid(sol.x)))
print(f'FINO: rot {math.degrees(th):.1f}°, s {s:.3f} m/px, mediana {med:.1f} m')

# geo oglišča lista A04
def px2geo(x, y):
    X = (math.cos(th)*x - math.sin(th)*y)*s + tx
    Y = (math.sin(th)*x + math.cos(th)*y)*s + ty
    return (45.0 + Y/M, 0.0 + X/(M*COS))
# preveri: uporabi lokalni izhodiščni sistem: pretvori prek referenčne točke c_target
lat_ref, lng_ref = seg[:,0].mean(), seg[:,1].mean()
def px2geo2(x, y):
    X = (math.cos(th)*x - math.sin(th)*y)*s + tx
    Y = (math.sin(th)*x + math.cos(th)*y)*s + ty
    return (lat_ref + (Y - c_target[1])/M, lng_ref + (X - c_target[0])/(M*COS))
W, H = 2645, 2158
corners = {'NW': px2geo2(0,0), 'NE': px2geo2(W,0), 'SW': px2geo2(0,H), 'SE': px2geo2(W,H)}
for k, v in corners.items(): print(f'  {k}: {v[0]:.5f} {v[1]:.5f}')
# center lista
cc = px2geo2(W/2, H/2)
print(f'  CENTER lista: {cc[0]:.5f} {cc[1]:.5f} (celica cg center: 45.55050 15.28505)')
json.dump({'rotDeg': round(math.degrees(th),2), 'scale': round(s,3), 'medianM': round(med,1),
           'corners': {k: [round(v[0],5), round(v[1],5)] for k,v in corners.items()},
           'center': [round(cc[0],5), round(cc[1],5)]}, open('/tmp/p10-a04-refit.json','w'))
