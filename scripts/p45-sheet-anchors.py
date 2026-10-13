#!/usr/bin/env python3
"""P45 (issue #14): točkovna sidra za A03/A04/A05 — fit porazdelitve stavbnih
simbolov 1825 → sodobne stavbne parcele GURS, s priorjem iz resnice A02.

Veriga dokazov:
  1. KALIBRACIJA na A02 (156 stavb buildings.json: px + lat/lng iz GEOTRUTH):
     - resnična podobnost A02 (z zrcaljenjem y: slika y-dol → metrično y-gor)
       = PRIOR rotacije za sestrobdne liste (isti snemalec 1825, ista projekcija);
     - izbira detektorja: temne lise vs rdeče steblo — F1 na 156 resnice.
  2. DETEKCIJA na A03/A04/A05 z izbranim detektorjem.
  3. FIT podobnosti (rot, merilo, translacija) vs sodobne stavbne parcele
     v coni celice (KD-drevo, NENASIČENA mehka točkovalnica).
  4. DISKRIMINACIJA: nič-testi (zasuki 90/180/270° + naključni zamiki).
  5. IZHOD: research/georef-n83/p45-sheet-fits.json (dokazni artefakt).
"""
import json, math, sys
import numpy as np
from PIL import Image
from scipy import ndimage
from scipy.spatial import cKDTree

ROOT = '/home/z/my-project/muzej'
M_LAT = 111320.0
M_LNG = 78014.0  # cos(45.5°) * 111320

# ---------------------------------------------------------------- nosilci --

_SHEET_CACHE = {}


def load_sheet(path):
    """Sivi + RGB kanal lista (predizračunano)."""
    if path not in _SHEET_CACHE:
        im = Image.open(path)
        gray = np.asarray(im.convert('L')).astype(float)
        rgb = np.asarray(im.convert('RGB')).astype(float)
        _SHEET_CACHE[path] = (gray, rgb)
    return _SHEET_CACHE[path]


def detect(path, mode='dark', thr=-20, wmin=6, wmax=26, hmin=6, hmax=22,
           margin=60, mask=None):
    """Detektor simbolov. mode: dark | red | darkred."""
    gray, rgb = load_sheet(path)
    H, W = gray.shape
    if mode in ('dark', 'darkred'):
        med = ndimage.median_filter(gray, size=31)
        dark = (gray - med) < thr
        dark = ndimage.binary_closing(dark, structure=np.ones((3, 3)))
        base = dark
    if mode in ('red', 'darkred'):
        R, G, B = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
        red = (R - G > 28) & (R - B > 28)   # rdeče steblo (natisnjene stavbe)
        red = ndimage.binary_closing(red, structure=np.ones((2, 2)))
        if mode == 'red':
            base = red
        else:
            base = dark & red
    lab, n = ndimage.label(base)
    objs = ndimage.find_objects(lab)
    pts = []
    for i, sl in enumerate(objs):
        cy = (sl[0].start + sl[0].stop) / 2
        cx = (sl[1].start + sl[1].stop) / 2
        h = sl[0].stop - sl[0].start
        w = sl[1].stop - sl[1].start
        if not (wmin <= w <= wmax and hmin <= h <= hmax):
            continue
        if not (margin <= cx <= W - margin and margin <= cy <= H - margin):
            continue
        if mask is not None and not mask(cx, cy):
            continue
        pts.append((cx, cy))
    return np.array(pts) if pts else np.zeros((0, 2))


def to_up(P):
    """Slika (x, y-dol) → (x, -y): severna orientacija pred podobnostjo."""
    P = np.asarray(P, dtype=float)
    return np.column_stack([P[:, 0], -P[:, 1]])


def sim_apply(Pc, deg, s, tx, ty):
    """Pc (že zrcaljeno, centrirano) → lokalni metri."""
    co, si = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return np.column_stack([(co * Pc[:, 0] - si * Pc[:, 1]) * s + tx,
                            (si * Pc[:, 0] + co * Pc[:, 1]) * s + ty])


def fit_similarity(P, Q, init, rot_prior=6.0, s_frac=0.15, tr_range=500.0,
                   tr_step=25.0, d0=15.0, d1=100.0):
    """Dvostopenjski fit podobnosti P→Q (P že zrcaljeno). Vrne slovar."""
    tree = cKDTree(Q)
    Pc = P - P.mean(axis=0)

    def sc(deg, s, tx, ty):
        d, _ = tree.query(sim_apply(Pc, deg, s, tx, ty), k=1)
        return float(np.clip(1 - (d - d0) / (d1 - d0), 0, 1).mean()), float(np.median(d))

    # STOPNJA 1: translacijska mreža pri prior rot/s — top 3
    cands = []
    for tx in np.arange(init['tx'] - tr_range, init['tx'] + tr_range + 1, tr_step):
        for ty in np.arange(init['ty'] - tr_range, init['ty'] + tr_range + 1, tr_step):
            v, md = sc(init['deg'], init['s'], tx, ty)
            cands.append((v, md, float(tx), float(ty)))
    cands.sort(reverse=True)
    top = cands[:3]

    # STOPNJA 2: rotacija + merilo + fina translacija okoli top kandidatov
    best = dict(score=top[0][0], median=top[0][1], deg=init['deg'],
                s=init['s'], tx=top[0][2], ty=top[0][3])
    for c in top:
        for deg in np.arange(init['deg'] - rot_prior, init['deg'] + rot_prior + 0.001, 1.0):
            for s in np.arange(init['s'] * (1 - s_frac), init['s'] * (1 + s_frac) + 1e-9, 0.02):
                for tx in np.arange(c[2] - tr_step, c[2] + tr_step + 1, tr_step / 2):
                    for ty in np.arange(c[3] - tr_step, c[3] + tr_step + 1, tr_step / 2):
                        v, md = sc(deg, s, tx, ty)
                        if v > best['score']:
                            best = dict(score=v, median=md, deg=float(deg),
                                        s=float(s), tx=float(tx), ty=float(ty))
    # fina lokalna izboljšava
    for _ in range(2):
        for deg in [best['deg'] + k * 0.25 for k in range(-4, 5)]:
            for s in [best['s'] + k * 0.005 for k in range(-4, 5)]:
                if s <= 0.1:
                    continue
                for tx in np.arange(best['tx'] - 12, best['tx'] + 12.1, 2.5):
                    for ty in np.arange(best['ty'] - 12, best['ty'] + 12.1, 2.5):
                        v, md = sc(deg, s, tx, ty)
                        if v > best['score']:
                            best = dict(score=v, median=md, deg=float(deg), s=float(s),
                                        tx=float(tx), ty=float(ty))
    return best


def geo_to_local(lats, lngs, lat0, lng0):
    """Lokalni metri: X proti vzhodu, Y proti SEVERU (skladno s to_up)."""
    return np.column_stack([(np.asarray(lngs) - lng0) * M_LNG,
                            (np.asarray(lats) - lat0) * M_LAT])


# ------------------------------------------------------- 1. kalibracija A02 --

def calibrate_a02():
    print('=' * 72)
    print('1. KALIBRACIJA NA A02 (156 stavb = resnica)')
    print('=' * 72)
    bld = json.load(open(f'{ROOT}/src/data/atlas/buildings.json'))
    px = np.array([b['px'] for b in bld], dtype=float)
    geo = np.array([(b['lat'], b['lng']) for b in bld], dtype=float)
    lat0, lng0 = geo[:, 0].mean(), geo[:, 1].mean()
    G = geo_to_local(geo[:, 0], geo[:, 1], lat0, lng0)
    Pup = to_up(px)

    # resnična PODOBNOST z zrcaljenjem y (malopovprečne kvadrati, 4 param)
    n = len(Pup)
    Amat = np.zeros((2 * n, 4))
    Amat[0::2, 0] = Pup[:, 0]; Amat[0::2, 1] = -Pup[:, 1]; Amat[0::2, 2] = 1
    Amat[1::2, 0] = Pup[:, 1]; Amat[1::2, 1] = Pup[:, 0];  Amat[1::2, 3] = 1
    yv = np.zeros(2 * n)
    yv[0::2] = G[:, 0]
    yv[1::2] = G[:, 1]
    sol, *_ = np.linalg.lstsq(Amat, yv, rcond=None)
    a1, a2, tx, ty = sol
    s_true = math.hypot(a1, a2)
    deg_true = math.degrees(math.atan2(a2, a1))
    fwd = np.column_stack([a1 * Pup[:, 0] - a2 * Pup[:, 1] + tx,
                           a2 * Pup[:, 0] + a1 * Pup[:, 1] + ty])
    r = np.hypot(*(fwd - G).T)
    print(f'  A02 resnična podobnost (z y-zrcaljenjem): merilo {s_true:.3f} m/px, '
          f'rotacija {deg_true:+.2f}°, mediana ostanka {np.median(r):.1f} m, '
          f'povprečje {r.mean():.1f} m')

    # izbira detektorja: F1 na 156 resnice
    tree_true = cKDTree(px)
    best_cfg, best_f1 = None, -1
    for mode in ('dark', 'red', 'darkred'):
        for (wmin, wmax, hmin, hmax) in [(6, 26, 6, 22), (7, 32, 7, 28), (9, 45, 9, 35)]:
            det = detect(f'{ROOT}/public/atlas/n83-a02.jpg', mode=mode,
                         wmin=wmin, wmax=wmax, hmin=hmin, hmax=hmax)
            if len(det) < 20:
                continue
            d, _ = tree_true.query(det, k=1)
            prec = float((d <= 50).mean())
            d2, _ = cKDTree(det).query(px, k=1)
            rec = float((d2 <= 50).mean())
            f1 = 2 * prec * rec / (prec + rec) if prec + rec > 0 else 0
            tag = f'{mode} w{wmin}-{wmax} h{hmin}-{hmax}'
            print(f'  {tag:34s}: {len(det):4d} lis | prec@50 {prec:.2f} rec@50 {rec:.2f} F1 {f1:.2f}')
            if f1 > best_f1:
                best_f1, best_cfg = f1, (mode, wmin, wmax, hmin, hmax)
    mode, wmin, wmax, hmin, hmax = best_cfg
    print(f'  IZBRAN: {best_cfg} (F1 {best_f1:.2f})')
    return s_true, deg_true, best_cfg


# ------------------------------------------------------------ 2. celice ----

def load_cells():
    cells = {}
    for f in json.load(open(f'{ROOT}/research/georef-n83/ezkn-ix24.json'))['features']:
        a = f['attributes']
        ring = np.array(f['geometry']['rings'][0])  # [lng, lat]
        c = ring.mean(axis=0)
        # sanity: samo celice na območju k.o. Griblje (lng 15.2–15.35, lat 45.5–45.6)
        if not (15.2 < c[0] < 15.35 and 45.5 < c[1] < 45.6):
            continue
        cells[a['SPL_OZN']] = ring
    return cells


def load_modern():
    mods = []
    for fn, ka in [('parcels-ko1544-merged.json', 'geom_area'),
                   ('parcels-ko1552-merged.json', 'a')]:
        for o in json.load(open(f'{ROOT}/research/georef-n83/gurs/{fn}')):
            if o.get(ka, 9999) < 800:
                mods.append((o['lat'], o['lng']))
    return np.array(mods)


def zone_modern(mods, ring, pad_deg=0.004):
    lo, hi = ring.min(axis=0), ring.max(axis=0)
    m = ((mods[:, 0] >= lo[1] - pad_deg) & (mods[:, 0] <= hi[1] + pad_deg) &
         (mods[:, 1] >= lo[0] - pad_deg) & (mods[:, 1] <= hi[0] + pad_deg))
    return mods[m]


# ------------------------------------------------------------- 3. fiti -----

def fit_sheet(name, img, sheet_wh, cell_ring, mods, mask, prior_deg, prior_s,
              det_cfg, label=''):
    W, H = sheet_wh
    mode, wmin, wmax, hmin, hmax = det_cfg
    det = detect(img, mode=mode, wmin=wmin, wmax=wmax, hmin=hmin, hmax=hmax, mask=mask)
    print(f'\n--- {name} {label}: {len(det)} zaznanih simbolov ({mode}) ---')
    if len(det) < 8:
        print('  PREMALO SIMBOLOV za fit')
        return None

    lo, hi = cell_ring.min(axis=0), cell_ring.max(axis=0)
    lat0 = float((lo[1] + hi[1]) / 2)
    lng0 = float((lo[0] + hi[0]) / 2)
    Q = zone_modern(mods, cell_ring)
    Qm = geo_to_local(Q[:, 0], Q[:, 1], lat0, lng0)
    print(f'  sodobnih stavbnih v coni: {len(Qm)} (lat0 {lat0:.4f} lng0 {lng0:.4f})')

    cellW_m = (hi[0] - lo[0]) * M_LNG
    cellH_m = (hi[1] - lo[1]) * M_LAT
    s_cell = (cellW_m / W + cellH_m / H) / 2

    Pup = to_up(det)
    pc = Pup.mean(axis=0)
    # iniciacija: težišče zaznanih pod celično preslikavo (približek)
    fx = ((det[:, 0].mean() / W) - 0.5) * cellW_m
    fy = ((det[:, 1].mean() / H) - 0.5) * cellH_m   # y-dol → N je −y: predznak reši fit
    init = {'deg': prior_deg, 's': prior_s, 'tx': fx, 'ty': fy}

    best = fit_similarity(Pup, Qm, init)
    print(f'  FIT: score {best["score"]:.3f} | mediana {best["median"]:.0f} m | '
          f'rot {best["deg"]:+.2f}° (prior {prior_deg:+.2f}°) | s {best["s"]:.3f} m/px '
          f'(celica {s_cell:.3f}) | t ({best["tx"]:+.0f}, {best["ty"]:+.0f}) m')

    # nič-testi: zasuki + naključni translacijski zamiki (isti prostor)
    tree = cKDTree(Qm)
    Pc = Pup - pc
    nulls_rot = []
    for k in (1, 2, 3):
        XY = sim_apply(Pc, best['deg'] + k * 90, best['s'], best['tx'], best['ty'])
        d, _ = tree.query(XY, k=1)
        nulls_rot.append(float(np.clip(1 - (d - 15) / 85, 0, 1).mean()))
    rng = np.random.default_rng(45)
    nulls_tr = []
    for _ in range(20):
        XY = sim_apply(Pc, best['deg'], best['s'],
                       best['tx'] + rng.uniform(-350, 350),
                       best['ty'] + rng.uniform(-350, 350))
        d, _ = tree.query(XY, k=1)
        nulls_tr.append(float(np.clip(1 - (d - 15) / 85, 0, 1).mean()))
    disc_rot = best['score'] - max(nulls_rot)
    disc_tr = best['score'] - float(np.mean(nulls_tr))
    print(f'  nič zasuki: {nulls_rot[0]:.3f}/{nulls_rot[1]:.3f}/{nulls_rot[2]:.3f} '
          f'(diskr. {disc_rot:+.3f}) | nič zamiki: povp. {np.mean(nulls_tr):.3f} '
          f'max {max(nulls_tr):.3f} (diskr. {disc_tr:+.3f})')

    return {'sheet': name, 'n1825': int(len(det)), 'nModern': int(len(Qm)),
            'score': round(best['score'], 4), 'medianM': round(best['median'], 1),
            'rotDeg': round(best['deg'], 2), 'scale': round(best['s'], 4),
            'tx': round(best['tx'], 1), 'ty': round(best['ty'], 1),
            'nullsRot': [round(x, 4) for x in nulls_rot],
            'nullsTrMean': round(float(np.mean(nulls_tr)), 4),
            'nullsTrMax': round(float(max(nulls_tr)), 4),
            'discRot': round(disc_rot, 4), 'discTr': round(disc_tr, 4),
            'cellImpliedScale': round(s_cell, 4), 'priorDeg': prior_deg,
            'lat0': lat0, 'lng0': lng0}


def main():
    out = {}
    s_true, deg_true, det_cfg = calibrate_a02()
    out['a02Truth'] = {'scaleMPerPx': round(s_true, 4), 'rotDeg': round(deg_true, 3),
                       'detector': str(det_cfg)}
    cells = load_cells()
    print(f'\ncelice na območju: {sorted(cells.keys())}')
    mods = load_modern()
    print(f'sodobnih stavbnih skupaj: {len(mods)}')

    results = {}
    W3, H3 = 2645, 2154
    results['a03'] = fit_sheet('A03', f'{ROOT}/public/atlas/n83-a03.jpg', (W3, H3),
                               cells['VKIX24dg'], mods,
                               mask=lambda x, y: x >= 0.78 * W3,
                               prior_deg=deg_true, prior_s=0.72, det_cfg=det_cfg,
                               label='(celica dg, vzhodni pas)')
    W4, H4 = 2645, 2158
    results['a04'] = fit_sheet('A04', f'{ROOT}/public/atlas/n83-a04.jpg', (W4, H4),
                               cells['VKIX24cg'], mods, mask=None,
                               prior_deg=deg_true, prior_s=0.72, det_cfg=det_cfg,
                               label='(celica cg, cel list)')
    W5, H5 = 2634, 2165
    results['a05'] = fit_sheet('A05', f'{ROOT}/public/atlas/n83-a05.jpg', (W5, H5),
                               cells['VKIX24ch'], mods,
                               mask=lambda x, y: (x >= 0.30 * W5) and (y <= 0.80 * H5),
                               prior_deg=deg_true, prior_s=0.73, det_cfg=det_cfg,
                               label='(celica ch, vsebina)')
    out.update(results)

    json.dump(out, open(f'{ROOT}/research/georef-n83/p45-sheet-fits.json', 'w'),
              ensure_ascii=False, indent=1)
    print('\nSHRANJENO: research/georef-n83/p45-sheet-fits.json')


if __name__ == '__main__':
    main()
