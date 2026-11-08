#!/usr/bin/env python3
"""
GEOREF N83 P9 — A04: reka Kolpa na listu A04 vsebuje OVIN pri Adlešičih
(SSE→ESE) + toponimi iz VLM ploščičnega skena (research/georef-n83/tiles-vlm/).
P8 je padel na A02 (ravna struga); tu preverimo, ali ovin + sidra zadostujejo.
Izhod: research/georef-n83/p9-a04-fit.json + poročilo.
"""
import json, math
import numpy as np
import cv2
from scipy.optimize import least_squares

M = 111320.0
COS = math.cos(math.radians(45.5))

MODERN = np.array(json.load(open('research/georef-n83/kolpa-modern-centerline.json')))
MODERN_M = np.stack([MODERN[:, 1] * M * COS, MODERN[:, 0] * M], axis=1)  # [E, N] m

# VLM toponimi (tiles-vlm a04-labels.json + bigpicture) — px centra napisov
A04_LABELS = {
    'WEIDENDORF (Bedenj?)': (608, 1964),
    'ADLESCHITZ obmocje': (2116, 1403),
    'ADL razprseno': (1747, 1765),
    'Bresnik': (1032, 1532),
    'Schlatonig': (264, 517),
    'Katastralgemeinde Griblje': (794, 1131),
    'Brëstie': (1590, 917),
}

# Moderne reference (Wikipedija/OSM — 2026-10-08)
REFS = {
    'Bedenj': (45.53742222, 15.27693889),
    'Tribuce': (45.54515000, 15.24304167),
    'Adlesici': (45.52239722, 15.31104444),
    'Griblje-cerkev': (45.56761, 15.290311),
}

def dist_to_modern(pts_m):
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

def extract_river_full(scan_path, dark_thr=150, gap_min=40, win=40, stride=20):
    """A04: reka teče diagonalno — VSA poteči (ne le najvzhodnejša)."""
    im = cv2.imread(scan_path, cv2.IMREAD_GRAYSCALE)
    h, w = im.shape
    dark = (im < dark_thr).astype(np.float32)
    out = []
    for y in range(0, h - win, stride):
        col = dark[y:y + win, :w].mean(axis=0)
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
                        out.append((y + win // 2, (i + j) // 2, j - i))
                i = j
            else:
                i += 1
    # združi poteči v pas: za vsako y vzemi najdaljši potek (širina)
    by_y = {}
    for y, cx, wd in out:
        by_y.setdefault(y, []).append((cx, wd))
    pts = []
    for y in sorted(by_y):
        # vzemi najširši potek = reka
        cx, wd = max(by_y[y], key=lambda t: t[1])
        pts.append((y, cx, wd))
    return pts

def fit(river_pts, lat0, lng0, theta_degs=(-30,-25,-20,-15,-10,-5,0,5,10,15,20,25,30), scales=(0.7,0.85,1.0,1.15,1.3)):
    px = np.array([(y, x) for y, x, w in river_pts], dtype=float)
    best = None
    for theta0 in (math.radians(a) for a in theta_degs):
        for s0 in scales:
            c, sn = math.cos(theta0), math.sin(theta0)
            E0 = lng0 * M * COS - s0 * (c * px[:, 1].mean() - sn * px[:, 0].mean())
            N0 = lat0 * M - s0 * (sn * px[:, 1].mean() + c * px[:, 0].mean())
            def resid(p):
                theta, s, dE, dN = p
                cc, ss = math.cos(theta), math.sin(theta)
                E = E0 + dE + s * (cc * px[:, 1] - ss * px[:, 0])
                N = N0 + dN + s * (ss * px[:, 1] + cc * px[:, 0])
                return dist_to_modern(np.stack([E, N], axis=1))
            try:
                r = least_squares(resid, [theta0, s0, 0.0, 0.0],
                                  loss='soft_l1', f_scale=40.0,
                                  bounds=([-0.6, 0.4, -4000, -4000], [0.6, 2.0, 4000, 4000]),
                                  max_nfev=800)
            except Exception:
                continue
            med = np.median(r.fun)
            if best is None or med < best[0]:
                best = (med, (r.x[0], r.x[1], E0 + r.x[2], N0 + r.x[3]), r.fun, px)
    return best

def px2geo(params, x, y):
    theta, s, ex, ny = params
    c, sn = math.cos(theta), math.sin(theta)
    E = ex + s * (c * x - sn * y)
    N = ny + s * (sn * x + c * y)
    return E, N

def geo2latlng(E, N):
    return N / M, E / (M * COS)

def main():
    # 1) ekstrakcija
    pts = extract_river_full('public/atlas/n83-a04.jpg')
    print(f'A04 river: {len(pts)} točk; y {pts[0][0]}–{pts[-1][0]}, '
          f'x {min(p[1] for p in pts)}–{max(p[1] for p in pts)}, širina {min(p[2] for p in pts)}–{max(p[2] for p in pts)} px')
    # 2) fit — sidro pri Adlešičih
    best = fit(pts, 45.525, 15.30)
    med, params, res, px = best
    theta, s, ex, ny = params
    print(f'\nFIT A04: rot {math.degrees(theta):+.2f}°, s {s:.3f} m/px, px(0,0) → E {ex:.0f} m N {ny:.0f} m')
    print(f'   reka: mediana {med:.0f} m, p90 {np.percentile(res, 90):.0f} m do moderne Kolpe')
    # 3) validacija napisov
    print('\nVALIDACIJA napisov → geo:')
    for name, (x, y) in A04_LABELS.items():
        E, N = px2geo(params, x, y)
        lat, lng = geo2latlng(E, N)
        dists = {rn: math.hypot(E - rl[1] * M * COS, N - rl[0] * M) for rn, rl in REFS.items()}
        dmin = min(dists, key=dists.get)
        print(f'   {name:28} → {lat:.5f}, {lng:.5f} — najbližje {dmin} {dists[dmin]:.0f} m')
    # 4) vogali lista
    print('\nVOGALI lista A04 (2645×2158):')
    corners = {}
    for name, (x, y) in {'NW': (0, 0), 'NE': (2644, 0), 'SW': (0, 2157), 'SE': (2644, 2157)}.items():
        E, N = px2geo(params, x, y)
        corners[name] = geo2latlng(E, N)
        print(f'   {name}: {corners[name][0]:.5f}, {corners[name][1]:.5f}')
    json.dump({
        'sheet': 'a04', 'riverPts': [[y, x, w] for y, x, w in pts],
        'fit': {'theta_deg': math.degrees(theta), 'scale_m_px': s, 'E0': ex, 'N0': ny,
                'median_m': float(med), 'p90_m': float(np.percentile(res, 90))},
        'labels_geo': {k: px2geo(params, v[0], v[1]) and list(geo2latlng(*px2geo(params, v[0], v[1]))) for k, v in A04_LABELS.items()},
        'corners': {k: list(v) for k, v in corners.items()},
    }, open('research/georef-n83/p9-a04-fit.json', 'w'), indent=1)
    print('\n→ research/georef-n83/p9-a04-fit.json')

if __name__ == '__main__':
    main()
