#!/usr/bin/env python3
"""P45 (issue #14) — DOKONČNA ANALIZA: za vsak list A03/A04/A05
  (a) naivna CELIČNA preslikava (okvir lista ≈ celica eZKN),
  (b) PROSTI fit podobnosti (rot/merilo/translacija),
  (c) OMEJENI fit (merilo = celično ±5 % — listi so risani 1:2880;
      rotacija = prior A02 ±3° — ista serija, ista projekcija; A02 resnica:
      0,805 m/px, +0,02°, ostanek 2,4 m),
  (d) oznake → naselja (point-in-polygon, pyproj TM→WGS84),
  (e) A05: alternativni translacijski optimumi (diskriminativnost).
Izhod: research/georef-n83/p45-sheet-fits.json (dokazni artefakt #14)."""
import json, math
import numpy as np
from PIL import Image
from scipy import ndimage
from scipy.spatial import cKDTree
from pyproj import Transformer

ROOT = '/home/z/my-project/muzej'
M_LAT = 111320.0
M_LNG = 78014.0
TM2WGS = Transformer.from_crs(3794, 4326, always_xy=True)


def point_in_poly(x, y, poly):
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]; xj, yj = poly[j]
        if (yi > y) != (yj > y):
            xint = (xj - xi) * (y - yi) / (yj - yi) + xi
            if x < xint:
                inside = not inside
        j = i
    return inside


def detect(path, mask=None):
    """Rdeči detektor stavbnih simbolov (kalibriran na A02: F1 0,56, rec@50 0,94)."""
    rgb = np.asarray(Image.open(path).convert('RGB')).astype(float)
    H, W = rgb.shape[:2]
    R, G, B = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    red = (R - G > 28) & (R - B > 28)
    red = ndimage.binary_closing(red, structure=np.ones((2, 2)))
    lab, n = ndimage.label(red)
    objs = ndimage.find_objects(lab)
    pts = []
    for i, sl in enumerate(objs):
        cy = (sl[0].start + sl[0].stop) / 2
        cx = (sl[1].start + sl[1].stop) / 2
        h = sl[0].stop - sl[0].start
        w = sl[1].stop - sl[1].start
        if not (7 <= w <= 32 and 7 <= h <= 28):
            continue
        if not (60 <= cx <= W - 60 and 60 <= cy <= H - 60):
            continue
        if mask is not None and not mask(cx, cy):
            continue
        pts.append((cx, cy))
    return np.array(pts) if pts else np.zeros((0, 2)), (W, H)


def sim_geo(Ppx, deg, s, tx, ty, lat0, lng0, center_px=None):
    Pup = np.column_stack([Ppx[:, 0], -Ppx[:, 1]])
    if center_px is None:
        center_px = Pup
    else:
        center_px = np.column_stack([center_px[:, 0], -center_px[:, 1]])
    pc = np.array([center_px[:, 0].mean(), center_px[:, 1].mean()])
    Pc = Pup - pc
    co, si = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    X = (co * Pc[:, 0] - si * Pc[:, 1]) * s + tx
    Y = (si * Pc[:, 0] + co * Pc[:, 1]) * s + ty
    return np.column_stack([lat0 + Y / M_LAT, lng0 + X / M_LNG])


def stats_at(G, Q, lat0=None, lng0=None):
    if len(G) == 0 or len(Q) == 0:
        return None
    if lat0 is None:
        lat0, lng0 = G[:, 0].mean(), G[:, 1].mean()
    Gm = np.column_stack([(G[:, 1] - lng0) * M_LNG, (G[:, 0] - lat0) * M_LAT])
    Qm = np.column_stack([(Q[:, 1] - lng0) * M_LNG, (Q[:, 0] - lat0) * M_LAT])
    d, _ = cKDTree(Qm).query(Gm, k=1)
    return {'medianM': round(float(np.median(d)), 1),
            'in30': round(float((d <= 30).mean()), 3),
            'in50': round(float((d <= 50).mean()), 3),
            'score': round(float(np.clip(1 - (d - 15) / 85, 0, 1).mean()), 4)}


def grid_fit(Pup, Qm, rots, scales, txs, tys):
    """Mrežni fit s podanimi doslej vrednostmi; vrne najboljši (score, med, deg, s, tx, ty)."""
    tree = cKDTree(Qm)
    Pc = Pup - Pup.mean(axis=0)
    best = (-1.0, 1e9, rots[0], scales[0], txs[0], tys[0])
    for deg in rots:
        co, si = math.cos(math.radians(deg)), math.sin(math.radians(deg))
        X0 = co * Pc[:, 0] - si * Pc[:, 1]
        Y0 = si * Pc[:, 0] + co * Pc[:, 1]
        for s in scales:
            X = X0 * s; Y = Y0 * s
            for tx in txs:
                for ty in tys:
                    d, _ = tree.query(np.column_stack([X + tx, Y + ty]), k=1)
                    v = float(np.clip(1 - (d - 15) / 85, 0, 1).mean())
                    if v > best[0]:
                        best = (v, float(np.median(d)), float(deg), float(s), float(tx), float(ty))
    return best


def load_modern():
    mods = []
    for fn, ka in [('parcels-ko1544-merged.json', 'geom_area'),
                   ('parcels-ko1552-merged.json', 'a')]:
        for o in json.load(open(f'{ROOT}/research/georef-n83/gurs/{fn}')):
            if o.get(ka, 9999) < 800:
                mods.append((o['lat'], o['lng']))
    return np.array(mods)


def load_naselja():
    n = json.load(open(f'{ROOT}/research/georef-n83/gurs/naselja.json'))
    return {f['properties']['NAZIV']: [TM2WGS.transform(x, y)
                                       for x, y in f['geometry']['coordinates'][0]]
            for f in n['features']}


def load_cells():
    cells = {}
    for f in json.load(open(f'{ROOT}/research/georef-n83/ezkn-ix24.json'))['features']:
        a = f['attributes']
        ring = np.array(f['geometry']['rings'][0])
        c = ring.mean(axis=0)
        if 15.2 < c[0] < 15.35 and 45.5 < c[1] < 45.6:
            cells[a['SPL_OZN']] = ring
    return cells


SHEETS = {
    'a03': dict(img='public/atlas/n83-a03.jpg', cell='VKIX24dg', wh=(2645, 2154),
                mask=lambda x, y, W, H: x >= 0.78 * W,
                labels={'TRIBUTSCH': (0.68, 0.35), 'WEIDENDORF': (0.71, 0.86)}),
    'a04': dict(img='public/atlas/n83-a04.jpg', cell='VKIX24cg', wh=(2645, 2158),
                mask=None,
                labels={'WEIDENDORF': (0.23, 0.91), 'ADLESCHITZ': (0.80, 0.65)}),
    'a05': dict(img='public/atlas/n83-a05.jpg', cell='VKIX24ch', wh=(2634, 2165),
                mask=lambda x, y, W, H: (x >= 0.30 * W) and (y <= 0.80 * H),
                labels={'Pri Jankovichti': (0.65, 0.21), 'ADLESC': (0.88, 0.10)}),
}

PRIOR_DEG = 0.02  # A02 resnica


def analyze(key, cfg, mods, nas, cells, fits):
    W0, H0 = cfg['wh']
    det, (W, H) = detect(f'{ROOT}/{cfg["img"]}',
                         mask=(lambda x, y: cfg['mask'](x, y, W0, H0)) if cfg['mask'] else None)
    print(f'\n{"=" * 70}\n{key.upper()} — {len(det)} rdečih simbolov '
          f'(maska: {"da" if cfg["mask"] else "ne"})')
    # porazdelitev detekcij (%)
    if len(det):
        print('  detekcije %: x', np.percentile(det[:, 0] / W, [10, 50, 90]).round(2),
              'y', np.percentile(det[:, 1] / H, [10, 50, 90]).round(2))

    ring = cells[cfg['cell']]
    lo, hi = ring.min(axis=0), ring.max(axis=0)
    lat0 = float((lo[1] + hi[1]) / 2)
    lng0 = float((lo[0] + hi[0]) / 2)
    m = ((mods[:, 0] >= lo[1] - 0.004) & (mods[:, 0] <= hi[1] + 0.004) &
         (mods[:, 1] >= lo[0] - 0.004) & (mods[:, 1] <= hi[0] + 0.004))
    Q = mods[m]
    Qm = np.column_stack([(Q[:, 1] - lng0) * M_LNG, (Q[:, 0] - lat0) * M_LAT])
    cellW_m = (hi[0] - lo[0]) * M_LNG
    cellH_m = (hi[1] - lo[1]) * M_LAT
    s_cell = (cellW_m / W + cellH_m / H) / 2
    print(f'  cona {cfg["cell"]}: {len(Q)} sodobnih stavb | celično merilo {s_cell:.3f} m/px')

    # (a) CELIČNA preslikava
    fx = det[:, 0] / W
    fy = 1 - det[:, 1] / H
    Gcell = np.column_stack([lo[1] + fy * (hi[1] - lo[1]),
                             lo[0] + fx * (hi[0] - lo[0])])
    st_cell = stats_at(Gcell, Q, lat0, lng0)
    cc = Gcell.mean(axis=0)
    print(f'  (a) CELIČNA: mediana {st_cell["medianM"]} m | in@30 {st_cell["in30"]} '
          f'| težišče ({cc[0]:.5f}, {cc[1]:.5f})')

    Pup = np.column_stack([det[:, 0], -det[:, 1]])

    # (c) OMEJENI fit: s = s_cell ±5 %, rot = prior ±3°, translacija ±500 m
    b_con = grid_fit(Pup, Qm,
                     rots=np.arange(PRIOR_DEG - 3, PRIOR_DEG + 3.01, 0.5),
                     scales=np.arange(s_cell * 0.95, s_cell * 1.051, 0.01),
                     txs=np.arange(-500, 501, 25.0),
                     tys=np.arange(-500, 501, 25.0))
    # fina translacija
    b_con = grid_fit(Pup, Qm,
                     rots=[b_con[2]],
                     scales=[b_con[3]],
                     txs=np.arange(b_con[4] - 25, b_con[4] + 25.1, 5.0),
                     tys=np.arange(b_con[5] - 25, b_con[5] + 25.1, 5.0))
    b_con = grid_fit(Pup, Qm, rots=[b_con[2]], scales=[b_con[3]],
                     txs=np.arange(b_con[4] - 5, b_con[4] + 5.1, 1.0),
                     tys=np.arange(b_con[5] - 5, b_con[5] + 5.1, 1.0))
    print(f'  (c) OMEJENI fit: score {b_con[0]:.3f} | mediana {b_con[1]:.0f} m | '
          f'rot {b_con[2]:+.2f}° | s {b_con[3]:.3f} | t ({b_con[4]:+.0f}, {b_con[5]:+.0f}) m')

    # (b) PROSTI fit (referenca)
    b_free = grid_fit(Pup, Qm,
                      rots=np.arange(PRIOR_DEG - 15, PRIOR_DEG + 15.01, 1.0),
                      scales=np.arange(s_cell * 0.8, s_cell * 1.251, 0.02),
                      txs=np.arange(-600, 601, 50.0),
                      tys=np.arange(-600, 601, 50.0))
    b_free = grid_fit(Pup, Qm,
                      rots=np.arange(b_free[2] - 2, b_free[2] + 2.01, 0.5),
                      scales=np.arange(b_free[3] - 0.04, b_free[3] + 0.041, 0.01),
                      txs=np.arange(b_free[4] - 50, b_free[4] + 50.1, 10.0),
                      tys=np.arange(b_free[5] - 50, b_free[5] + 50.1, 10.0))
    print(f'  (b) PROSTI fit: score {b_free[0]:.3f} | mediana {b_free[1]:.0f} m | '
          f'rot {b_free[2]:+.2f}° | s {b_free[3]:.3f} | t ({b_free[4]:+.0f}, {b_free[5]:+.0f}) m')

    # statistika pri OMEJENEM fitu + nič-testi
    Gcon = sim_geo(det, b_con[2], b_con[3], b_con[4], b_con[5], lat0, lng0)
    st_con = stats_at(Gcon, Q, lat0, lng0)
    gc = Gcon.mean(axis=0)
    tree = cKDTree(Qm)
    Pc = Pup - Pup.mean(axis=0)
    co, si = math.cos(math.radians(b_con[2])), math.sin(math.radians(b_con[2]))
    X0 = co * Pc[:, 0] - si * Pc[:, 1]; Y0 = si * Pc[:, 0] + co * Pc[:, 1]
    rng = np.random.default_rng(45)
    nulls = []
    for _ in range(30):
        d, _ = tree.query(np.column_stack([X0 * b_con[3] + b_con[4] + rng.uniform(-350, 350),
                                           Y0 * b_con[3] + b_con[5] + rng.uniform(-350, 350)]), k=1)
        nulls.append(float(np.clip(1 - (d - 15) / 85, 0, 1).mean()))
    print(f'  OMEJENI: težišče ({gc[0]:.5f}, {gc[1]:.5f}) | Δ od celične '
          f'{math.hypot((gc[0]-cc[0])*M_LAT, (gc[1]-cc[1])*M_LNG):.0f} m | '
          f'nič zamiki povp. {np.mean(nulls):.3f} max {max(nulls):.3f} '
          f'(diskr. {b_con[0]-np.mean(nulls):+.3f})')

    # oznake pod OMEJENIM fitom → naselja
    lab_out = {}
    for name, (px_f, py_f) in cfg['labels'].items():
        g = sim_geo(np.array([[px_f * W, py_f * H]]), b_con[2], b_con[3],
                    b_con[4], b_con[5], lat0, lng0, center_px=det)[0]
        hits = [n for n, poly in nas.items() if point_in_poly(g[1], g[0], poly)]
        lab_out[name] = {'geo': [round(float(g[0]), 5), round(float(g[1]), 5)],
                         'naselja': hits}
        print(f'  {name}: ({g[0]:.5f}, {g[1]:.5f}) → {hits if hits else "-"}')

    # vogali lista pod OMEJENIM fitom
    corners = {}
    for cn, (cx, cy) in {'NW': (0, 0), 'NE': (W, 0), 'SW': (0, H), 'SE': (W, H)}.items():
        g = sim_geo(np.array([[cx, cy]]), b_con[2], b_con[3], b_con[4], b_con[5],
                    lat0, lng0, center_px=det)[0]
        corners[cn] = [round(float(g[0]), 5), round(float(g[1]), 5)]

    fits[key] = {
        'sheet': key.upper(), 'cell': cfg['cell'],
        'nDetected': int(len(det)), 'nModern': int(len(Q)),
        'cellScale': round(s_cell, 4),
        'cell': {'stats': st_cell, 'centroid': [round(float(cc[0]), 5), round(float(cc[1]), 5)]},
        'constrained': {'score': round(b_con[0], 4), 'medianM': round(b_con[1], 1),
                        'rotDeg': round(b_con[2], 2), 'scale': round(b_con[3], 4),
                        'tx': round(b_con[4], 1), 'ty': round(b_con[5], 1),
                        'stats': st_con,
                        'centroid': [round(float(gc[0]), 5), round(float(gc[1]), 5)],
                        'nullTrMean': round(float(np.mean(nulls)), 4),
                        'nullTrMax': round(float(max(nulls)), 4),
                        'discrimination': round(b_con[0] - float(np.mean(nulls)), 4)},
        'free': {'score': round(b_free[0], 4), 'medianM': round(b_free[1], 1),
                 'rotDeg': round(b_free[2], 2), 'scale': round(b_free[3], 4)},
        'labels': lab_out, 'corners': corners,
        'lat0': lat0, 'lng0': lng0, 'detPct': det.tolist(),
    }
    return fits


def main():
    fits = {'a02Truth': {'scaleMPerPx': 0.8046, 'rotDeg': 0.02,
                         'medianResidualM': 2.4,
                         'note': 'lstsq na 156 stavb buildings.json (GEOTRUTH); '
                                 'y-zrcaljeno; celično merilo cf 0,80 — razlika <1 %'}}
    mods = load_modern()
    nas = load_naselja()
    cells = load_cells()
    print('naselja:', {k: (round(np.mean([p[1] for p in v]), 4),
                           round(np.mean([p[0] for p in v]), 4)) for k, v in nas.items()})

    for key, cfg in SHEETS.items():
        analyze(key, cfg, mods, nas, cells, fits)

    # A05 alternativni optimumi (omejeni rot/s)
    f5 = fits['a05']
    ring = cells['VKIX24ch']
    lo, hi = ring.min(axis=0), ring.max(axis=0)
    lat0, lng0 = f5['lat0'], f5['lng0']
    det, (W, H) = detect(f'{ROOT}/public/atlas/n83-a05.jpg',
                         mask=lambda x, y: (x >= 0.30 * 2634) and (y <= 0.80 * 2165))
    m = ((mods[:, 0] >= lo[1] - 0.004) & (mods[:, 0] <= hi[1] + 0.004) &
         (mods[:, 1] >= lo[0] - 0.004) & (mods[:, 1] <= hi[0] + 0.004))
    Q = mods[m]
    Qm = np.column_stack([(Q[:, 1] - lng0) * M_LNG, (Q[:, 0] - lat0) * M_LAT])
    b = f5['constrained']
    Pup = np.column_stack([det[:, 0], -det[:, 1]])
    Pc = Pup - Pup.mean(axis=0)
    co, si = math.cos(math.radians(b['rotDeg'])), math.sin(math.radians(b['rotDeg']))
    X0 = co * Pc[:, 0] - si * Pc[:, 1]; Y0 = si * Pc[:, 0] + co * Pc[:, 1]
    tree = cKDTree(Qm)
    cands = []
    for tx in np.arange(-900, 1201, 25.0):
        for ty in np.arange(-800, 701, 25.0):
            d, _ = tree.query(np.column_stack([X0 * b['scale'] + tx, Y0 * b['scale'] + ty]), k=1)
            cands.append((float(np.clip(1 - (d - 15) / 85, 0, 1).mean()),
                          float(np.median(d)), float(tx), float(ty)))
    cands.sort(reverse=True)
    sep = []
    for c in cands:
        if all(math.hypot(c[2] - s[2], c[3] - s[3]) > 250 for s in sep):
            sep.append(c)
        if len(sep) >= 6:
            break
    print('\nA05 ločeni translacijski optimumi (omejeni rot/s):')
    alts = []
    for c in sep:
        lat = lat0 + c[3] / M_LAT; lng = lng0 + c[2] / M_LNG
        hits = [n for n, poly in nas.items() if point_in_poly(lng, lat, poly)]
        alts.append({'score': round(c[0], 4), 'medianM': round(c[1], 1),
                     'geo': [round(lat, 5), round(lng, 5)], 'naselja': hits})
        print(f'  score {c[0]:.3f} med {c[1]:5.1f} m → ({lat:.5f}, {lng:.5f}) {hits}')
    f5['alternatives'] = alts

    json.dump(fits, open(f'{ROOT}/research/georef-n83/p45-sheet-fits.json', 'w'),
              ensure_ascii=False, indent=1)
    print('\nSHRANJENO: research/georef-n83/p45-sheet-fits.json')


if __name__ == '__main__':
    main()
