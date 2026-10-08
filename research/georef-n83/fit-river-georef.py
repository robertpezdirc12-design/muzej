#!/usr/bin/env python3
"""
GEOREF N83 — A03/A04/A05: poskus georeference prek reke Kolpe (P8) — NEGATIVNA ugotovitev
======================================================================================
REZULTAT (validacija na A02, znana resnica EŠD 2122): metoda NE DELA —
Kolpa na odseku Griblje je premalo vijugasta (± 400 m na 6 km), da bi razločila
sever–jug lego in merilo:
 - brez mej: s zdrsne na 0,4 m/px, cerkev 1,6 km napačno (reka sama 11 m!)
 - realne meje (s 0,70–1,15): s → 0,70, cerkev 916 m napačno (dN −909 m)
 - fiksirani s ∈ 0,70–1,00: inlier-mean 30,5–37,7 m — s=0,84 »boljši« kot
   pravi s=0,79 (31,5) → merilo NI razločno
 - VZHOD–ZAHOD kontrola je močna (dE −9…−33 m) — premalo.
Podrobnosti + diagnoza: research/georef-n83/README.md.

Kaj je vseeno UPORABNO (validirano):
 - kolpa-modern-centerline.json — modernа Kolpa iz OpenTopoMap ploščic
   (pri lat cerkve 45,5676 → lng 15,29866 = TOČNO sidro issue #14);
 - extract_river() — ekstrakcija ~1825 struge s listov (A02: center x
   2780–2900 pri y 100–1400, skladno z GEOTRUTH).

Poganjanje: python3 research/georef-n83/fit-river-georef.py [a02|a03|a04|a05|all]
"""

import json, math, sys
import numpy as np
import cv2
from scipy.optimize import least_squares

M = 111320.0
COS = math.cos(math.radians(45.5))

MODERN = np.array(json.load(open('research/georef-n83/kolpa-modern-centerline.json')))
MODERN_M = np.stack([MODERN[:, 1] * M * COS, MODERN[:, 0] * M], axis=1)  # [E, N] meters

def dist_to_modern(pts_m):
    """min distance of each point to the modern polyline (segment-wise)."""
    d = np.full(len(pts_m), 1e9)
    a = MODERN_M[:-1]; b = MODERN_M[1:]
    for i in range(0, len(MODERN_M) - 1, 3):
        aa, bb = a[i], b[i]
        ab = bb - aa
        ab2 = (ab * ab).sum()
        if ab2 < 1e-6: continue
        t = ((pts_m - aa) @ ab) / ab2
        t = np.clip(t, 0, 1)
        proj = aa[None, :] + t[:, None] * ab[None, :]
        dd = np.hypot(*(pts_m - proj).T)
        d = np.minimum(d, dd)
    return d

def extract_river(scan_path, x_from, dark_thr=150, gap_min=40, win=40, stride=20, y_margin=0):
    im = cv2.imread(scan_path, cv2.IMREAD_GRAYSCALE)
    h, w = im.shape
    dark = (im < dark_thr).astype(np.float32)
    out = []
    for y in range(y_margin, h - win - y_margin, stride):
        col = dark[y:y + win, x_from:w].mean(axis=0)
        col = np.convolve(col, np.ones(9) / 9, mode='same')
        water = col < 0.06
        i = 0
        while i < len(water):
            if water[i]:
                j = i
                while j < len(water) and water[j]: j += 1
                if j - i >= gap_min:
                    li, ri = max(0, i - 25), min(len(col), j + 25)
                    lb = col[li:i].max() if i > li else 0
                    rb = col[j:ri].max() if ri > j else 0
                    if lb > 0.15 and rb > 0.15:
                        out.append((y + win // 2, (i + j) // 2 + x_from, j - i))
                i = j
            else:
                i += 1
    # keep the most easterly run per y (river = eastern boundary)
    by_y = {}
    for y, cx, wd in out:
        by_y.setdefault(y, []).append((cx, wd))
    pts = []
    for y in sorted(by_y):
        cx, wd = max(by_y[y])  # eastern-most center
        pts.append((y, cx, wd))
    return pts

def sim(params, px_pts):
    """similarity: geo = R(theta) * s * (px - anchor) + geo_anchor (in meters)"""
    theta, s, ex, ny = params
    c, sn = math.cos(theta), math.sin(theta)
    # ex, ny = geo position (meters, east/north) of the px-origin (0, 0)
    X = px_pts[:, 1].astype(float)  # column
    Y = px_pts[:, 0].astype(float)  # row
    E = ex + s * (c * X - sn * Y)
    N = ny + s * (sn * X + c * Y)
    return np.stack([E, N], axis=1)

def fit(river_pts, lat0=45.56, lng0=15.299):
    px = np.array([(y, x) for y, x, w in river_pts], dtype=float)
    mean_px = px.mean(axis=0)
    best = None
    for theta0 in (math.radians(a) for a in (-15, -10, -5, 0, 5, 10, 15)):
        for s0 in (0.8, 1.0, 1.2):
            c, sn = math.cos(theta0), math.sin(theta0)
            E0 = lng0 * M * COS - s0 * (c * mean_px[1] - sn * mean_px[0])
            N0 = lat0 * M - s0 * (sn * mean_px[1] + c * mean_px[0])
            # params: [theta, s, dE, dN] — offsets from E0/N0 (meters)
            def resid(p):
                theta, s, dE, dN = p
                cc, ss = math.cos(theta), math.sin(theta)
                E = E0 + dE + s * (cc * px[:, 1] - ss * px[:, 0])
                N = N0 + dN + s * (ss * px[:, 1] + cc * px[:, 0])
                return dist_to_modern(np.stack([E, N], axis=1))
            try:
                r = least_squares(resid, [theta0, s0, 0.0, 0.0],
                                  loss='soft_l1', f_scale=60.0,
                                  bounds=([-0.5, 0.4, -3000, -3000], [0.5, 2.0, 3000, 3000]),
                                  max_nfev=600)
            except Exception:
                continue
            res = r.fun
            med = np.median(res)
            if best is None or med < best[0]:
                best = (med, (r.x[0], r.x[1], E0 + r.x[2], N0 + r.x[3]), res)
    return best, px

def report(name, best, px, extra=None):
    med, params, res = best
    theta, s, ex, ny = params
    print(f'--- {name}: {len(px)} river pts')
    print(f'    rotacija {math.degrees(theta):+.2f}°, merilo {s:.3f} m/px, '
          f'izvor px(0,0) → E {ex:.0f} m N {ny:.0f} m')
    print(f'    razdalje do moderne Kolpe: mediana {med:.0f} m, '
          f'p90 {np.percentile(res, 90):.0f} m, max {res.max():.0f} m')
    if extra:
        for label, (yy, xx) in extra.items():
            E = ex + s * (math.cos(theta) * xx - math.sin(theta) * yy)
            N = ny + s * (math.sin(theta) * xx + math.cos(theta) * yy)
            print(f'    {label} px({xx},{yy}) → lat {N/M:.6f} lng {E/(M*COS):.6f}')
    return params

if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'all'

    if which in ('a02', 'all'):
        # VALIDACIJA: A02 — reka naj sama rekonstruira lego CERKVE (EŠD 2122)
        rp = extract_river('public/atlas/n83-a02.jpg', x_from=2400, y_margin=60)
        best, px = fit(rp, lat0=45.562, lng0=15.299)
        report('A02 (validacija — cerkev EŠD 2122: 45.567610, 15.290311)',
               best, px, extra={'CERKEV': (577, 1995)})

    if which in ('a03', 'all'):
        rp = extract_river('public/atlas/n83-a03.jpg', x_from=1800, y_margin=60)
        best, px = fit(rp, lat0=45.566, lng0=15.301)
        p = report('A03', best, px)
        json.dump({'theta': p[0], 'mPerPx': p[1], 'originEN': [p[2], p[3]]},
                  open('research/georef-n83/a03-river-fit.json', 'w'))

    if which in ('a04', 'all'):
        rp = extract_river('public/atlas/n83-a04.jpg', x_from=1800, y_margin=60)
        best, px = fit(rp, lat0=45.545, lng0=15.302)
        p = report('A04', best, px)
        json.dump({'theta': p[0], 'mPerPx': p[1], 'originEN': [p[2], p[3]]},
                  open('research/georef-n83/a04-river-fit.json', 'w'))

    if which in ('a05', 'all'):
        rp = extract_river('public/atlas/n83-a05.jpg', x_from=1800, y_margin=60)
        if len(rp) < 10:
            print('--- A05: reka NI zaznana (k.o. južna meja ni ob Kolpi?) — brez georef prek reke')
        else:
            best, px = fit(rp, lat0=45.55, lng0=15.30)
            p = report('A05', best, px)
            json.dump({'theta': p[0], 'mPerPx': p[1], 'originEN': [p[2], p[3]]},
                      open('research/georef-n83/a05-river-fit.json', 'w'))
