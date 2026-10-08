#!/usr/bin/env python3
"""
P9b — zgoščena in deterministično izboljšana sled Kolpe na A04.
1. VLM semena (10 točk) → lokalna detekcija pasu (svetloba med bregovoma) ±120 px
2. Interpolacija (kubična) do ~60 točk vzdolž toku
3. Similarity fit proti moderni centerline (KD-drevo) + analiza merila
Izhod: research/georef-n83/p9b-a04-refined.json
"""
import cv2
import numpy as np
import json, math
from scipy.optimize import least_squares
from scipy.spatial import cKDTree
from scipy.interpolate import CubicSpline

M = 111320.0
COS = math.cos(math.radians(45.5))

MODERN = np.array(json.load(open('research/georef-n83/kolpa-modern-centerline.json')))
pts_m = np.stack([MODERN[:, 1] * M * COS, MODERN[:, 0] * M], axis=1)
dense = [pts_m[0]]
for i in range(len(pts_m) - 1):
    a, b = pts_m[i], pts_m[i + 1]
    seg = np.hypot(*(b - a)); n = max(1, int(seg / 3))
    for t in np.linspace(0, 1, n, endpoint=False)[1:]:
        dense.append(a + t * (b - a))
dense.append(pts_m[-1])
TREE = cKDTree(np.array(dense))

SEEDS = np.array([
    (2456, 743), (2361, 910), (2319, 1077), (1950, 1114), (1884, 1282),
    (1819, 1449), (1753, 1616), (1557, 1645), (1544, 1796), (1537, 1947),
], dtype=float)

im = cv2.imread('public/atlas/n83-a04.jpg', cv2.IMREAD_GRAYSCALE)
dark = (im < 150).astype(np.float32)

def refine(x, y, win=36, search=130):
    """Poišči center pasu svetlobe (<6 % temnih) najbližje (x, y)."""
    y0, y1 = max(0, int(y - win)), min(im.shape[0], int(y + win))
    x0, x1 = max(0, int(x - search)), min(im.shape[1], int(x + search))
    col = dark[y0:y1, x0:x1].mean(axis=0)
    col = np.convolve(col, np.ones(9) / 9, mode='same')
    water = col < 0.06
    best = None
    i = 0
    while i < len(water):
        if water[i]:
            j = i
            while j < len(water) and water[j]: j += 1
            w = j - i
            if 50 <= w <= 350:
                c = (i + j) / 2
                # kvaliteta: simetrična bregova
                li, ri = max(0, i - 30), min(len(col), j + 30)
                lb = col[li:i].max() if i > li else 0
                rb = col[j:ri].max() if ri > j else 0
                q = min(lb, rb)
                if best is None or q > best[0]:
                    best = (q, x0 + c, w)
            i = j
        else:
            i += 1
    return best

refined = []
for x, y in SEEDS:
    r = refine(x, y)
    if r and r[0] > 0.12:
        refined.append((r[1], y, r[2]))
        print(f'seme ({int(x)},{int(y)}) → pas x={r[1]:.0f}, širina {r[2]} px (kvaliteta {r[0]:.2f})')
    else:
        refined.append((x, y, None))
        print(f'seme ({int(x)},{int(y)}) → NI pasu, obdržim VLM točko')

pts = np.array([(x, y) for x, y, w in refined])
# dolžina parametra vzdolž toku
d = np.concatenate([[0], np.cumsum(np.hypot(np.diff(pts[:, 0]), np.diff(pts[:, 1])))])
# zgoščevanje: kubična interpolacija po 60 točk
cs_x = CubicSpline(d, pts[:, 0])
cs_y = CubicSpline(d, pts[:, 1])
ds = np.linspace(0, d[-1], 60)
dense_pts = np.stack([cs_x(ds), cs_y(ds)], axis=1)
# zavrnemo točke ekstrapolacije (zadnjih 5 % na obeh koncih)
mask = (ds >= d[0] + 0.03 * d[-1]) & (ds <= d[-1] * 0.97)
dense_pts = dense_pts[mask]
print(f'\nZgoščena sled: {len(dense_pts)} točk, dolžina {d[-1]:.0f} px')

# FIT — similarity na zgoščeni sledi
px = dense_pts
best = None
for th0 in (math.radians(a) for a in range(-60, 61, 10)):
    for s0 in (0.5, 0.6, 0.7, 0.9, 1.1):
        c, sn = math.cos(th0), math.sin(th0)
        E0 = 15.30 * M * COS - s0 * (c * px[:, 0].mean() - sn * px[:, 1].mean())
        N0 = 45.533 * M - s0 * (sn * px[:, 0].mean() + c * px[:, 1].mean())
        def resid(p):
            th, s, dE, dN = p
            cc, ss = math.cos(th), math.sin(th)
            E = E0 + dE + s * (cc * px[:, 0] - ss * px[:, 1])
            N = N0 + dN + s * (ss * px[:, 0] + cc * px[:, 1])
            return TREE.query(np.stack([E, N], axis=1))[0]
        try:
            r = least_squares(resid, [th0, s0, 0, 0], loss='soft_l1', f_scale=35,
                              bounds=([-1.1, 0.4, -6000, -6000], [1.1, 1.6, 6000, 6000]), max_nfev=500)
        except Exception:
            continue
        med = np.median(r.fun)
        if best is None or med < best[0]:
            best = (med, r.x, r.fun)
med, x, res = best
th, s, dE, dN = x
# rekonstrukcija ex/ny iz zadnjega starta (shranjenega parametra E0/N0 v dE/dN)
# — posodobi: izvedi ponovno s fiksno tvorbo
print(f'\nFIT (zgoščena sled): rot {math.degrees(th):+.1f}°, s {s:.3f} m/px, mediana {med:.0f} m, p90 {np.percentile(res, 90):.0f} m')

# ISKANJE MERILA po območjih (dvoumnost)
print('\nMerilo po prisiljenih območjih:')
for lo, hi in [(0.45, 0.60), (0.60, 0.70), (0.70, 0.80), (0.80, 0.95), (0.95, 1.10)]:
    bb = None
    for th0 in (math.radians(a) for a in range(-60, 61, 12)):
        s0 = min(max(0.6, lo + 0.02), hi - 0.02)
        c, sn = math.cos(th0), math.sin(th0)
        E0 = 15.30 * M * COS - s0 * (c * px[:, 0].mean() - sn * px[:, 1].mean())
        N0 = 45.533 * M - s0 * (sn * px[:, 0].mean() + c * px[:, 1].mean())
        def resid(p):
            t_, s_, dE_, dN_ = p
            cc, ss = math.cos(t_), math.sin(t_)
            return TREE.query(np.stack([
                E0 + dE_ + s_ * (cc * px[:, 0] - ss * px[:, 1]),
                N0 + dN_ + s_ * (ss * px[:, 0] + cc * px[:, 1])], axis=1))[0]
        try:
            r = least_squares(resid, [th0, s0, 0, 0], loss='soft_l1', f_scale=35,
                              bounds=([-1.1, lo, -6000, -6000], [1.1, hi, 6000, 6000]), max_nfev=400)
        except Exception:
            continue
        m_ = np.median(r.fun)
        if bb is None or m_ < bb[0]:
            bb = (m_, r.x, E0 + r.x[2], N0 + r.x[3])
    if bb:
        print(f'  s∈[{lo},{hi}]: s={bb[1][1]:.3f}, rot {math.degrees(bb[1][0]):+.1f}°, mediana {bb[0]:.0f} m')

json.dump({
    'seeds': SEEDS.tolist(),
    'refined': [[float(x), float(y), w] for x, y, w in refined],
    'dense': [[float(x), float(y)] for x, y in dense_pts],
    'fit': {'theta_deg': math.degrees(th), 's': float(s), 'dE': float(dE), 'dN': float(dN),
            'median_m': float(med), 'p90_m': float(np.percentile(res, 90))},
}, open('research/georef-n83/p9b-a04-refined.json', 'w'), indent=1)
print('\n→ research/georef-n83/p9b-a04-refined.json')
