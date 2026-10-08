#!/usr/bin/env python3
"""
GEOREF 1812 (issue #17, točka 2 — 1812 iz političnega pregleda v prostorsko raziskavo)
=======================================================================================
Zemljevid: »Provinces Illyriennes Servie et Bosnie 1812« (Giraldon, izvirnik 1812,
javna last; Commons 8297 × 6080 px, dlib 6EZTJ9C0) — obdobjeni izvirnik, ki ga
MAP_1812 v research.ts citira kot potrjenega.

Metoda (deterministična, brez AI-branja vsebine):
 1. OCR (tesseract eng; PSM 11/12/6/7/8; 3×/4×/6× upscale izrezov) mestnih
    oznak → centri besed v px.
 2. Najmanjša kvadratna preslikava px → (lat, lng): afina (6 koef.) IN
    kvadratna 2. reda (12 koef.) — primerjava; za Griblje se modela ujemata
    na ±2 px (model spread), izbira modela ni kritična.
 3. Robustnost: izločanje odstopanj (prag >15 km oz. > 2,2× mediane) —
    končni nabor 15 točk, ker so residuali posledica odmikov oznak od
    mestnih pik (10–25 km), ne modela.

Rezultat (glej georef-1812.json):
 - merilo ≈ 126 m/px (E–Z) × 123 m/px (S–J), razmerje 1,024 (skoraj izotropno)
 - residuali: mediana ≈ 10 km, max ≈ 25 km (Laibach — oznaka vzhodno od mesta)
 - Griblje (45,568 N 15,290 E) → px ≈ (2499, 2286) ± ~10 km
 - pokritje lista: ~11,1–24,4° E, 41,4–48,1° N (širše od meja Ilirskih provinc)

Status: REVIEW [~] — strojna georeferenca regionalnega lista; točke so centri
OCR-anih NAPISOV (ne mestnih pik); končna potrditev zahteva človeško paleografijo
ali georeferenciranje v GIS (QGIS) z izbiro točk na mestih pik.

Poganjanje (reproducibilno):
    python3 research/georef-1812/fit-georef.py
    # predpogoj: orig-1812.jpg (Commons Special:FilePath), ocr-full.tsv
"""

import json, math
import numpy as np

# ——— kontrolne točke: centri OCR-anih oznak (px) → realne koordinate ———
# Viri koordinat: splošno znane geografske lege mest (WGS84).
PTS = [
    # name         px_x   px_y    lat      lng      vir oznake
    ('Pest',       4927,   598,  47.497,  19.041, 'Pest (cela beseda)'),
    ('Leoben',     2369,   659,  47.383,  15.094, 'Leoben (cela beseda)'),
    ('Ancona',     1243,  4029,  43.622,  13.508, 'Ancone (cela beseda)'),
    ('Vidin',      7162,  3667,  43.993,  22.868, 'WIDDIN (cela beseda)'),
    ('Semlin',     5603,  2938,  44.843,  20.400, 'Semlin (2× OCR)'),
    ('Zvornik',    4829,  3358,  44.387,  19.093, 'Zworn (del)'),
    ('Pristina',   6152,  4882,  42.664,  21.166, 'Prist (del)'),
    ('Belgrade',   5602,  3029,  44.817,  20.457, 'Bel (del, conf 95)'),
    ('Sarajevo',   4363,  4010,  43.857,  18.413, 'Sariayey/Saray'),
    ('Ragusa',     4173,  4941,  42.651,  18.091, 'Raguse (6×, cela)'),
    ('Agram',      3052,  2051,  45.815,  15.982, 'Agram (6×, cela)'),
    ('Fiume',      2030,  2426,  45.328,  14.448, 'Frumeé = FIUME (6×, cela)'),
    ('Laibach',    2235,  1865,  46.056,  14.508, 'LAIBACH (fragmenti ACH/DA)'),
    ('Trieste',    1460,  2180,  45.650,  13.770, 'Tre:/Sine (fragmenti)'),
    ('BanyaLuka',  3505,  2956,  44.772,  17.191, 'Janyaluk (6×, cela)'),
]

M = 111320.0
COS = math.cos(math.radians(45.0))

def affine(active):
    X = np.array([[p[1], p[2], 1.0] for p in active])
    a = np.linalg.lstsq(X, np.array([p[3] for p in active]), rcond=None)[0]
    b = np.linalg.lstsq(X, np.array([p[4] for p in active]), rcond=None)[0]
    return lambda x, y: (a[0]*x+a[1]*y+a[2], b[0]*x+b[1]*y+b[2]), a, b

def quad(active):
    X = np.array([[p[1]**2, p[2]**2, p[1]*p[2], p[1], p[2], 1.0] for p in active])
    a = np.linalg.lstsq(X, np.array([p[3] for p in active]), rcond=None)[0]
    b = np.linalg.lstsq(X, np.array([p[4] for p in active]), rcond=None)[0]
    return lambda x, y: (a[0]*x*x+a[1]*y*y+a[2]*x*y+a[3]*x+a[4]*y+a[5],
                         b[0]*x*x+b[1]*y*y+b[2]*x*y+b[3]*x+b[4]*y+b[5]), a, b

def residuals(active, f):
    return sorted((math.hypot((f(p[1], p[2])[0]-p[3])*M, (f(p[1], p[2])[1]-p[4])*M*COS)/1000, p[0]) for p in active)

def invert(f, lat, lng, x0=2499.0, y0=2286.0):
    x, y = x0, y0
    for _ in range(50):
        plat, plng = f(x, y)
        e = 1.0
        p1 = f(x+e, y); p2 = f(x, y+e)
        J = np.array([[(p1[0]-plat)/e, (p2[0]-plat)/e], [(p1[1]-plng)/e, (p2[1]-plng)/e]])
        try: d = np.linalg.solve(J, np.array([lat-plat, lng-plng]))
        except Exception: break
        x += d[0]; y += d[1]
        if abs(d[0]) < 1e-7 and abs(d[1]) < 1e-7: break
    return x, y

def main():
    fa, aa, ba = affine(PTS)
    fq, aq, bq = quad(PTS)
    ra = residuals(PTS, fa); rq = residuals(PTS, fq)
    med_a = [r for r, _ in ra][len(ra)//2]; med_q = [r for r, _ in rq][len(rq)//2]

    gxa, gya = invert(fa, 45.568, 15.290)
    gxq, gyq = invert(fq, 45.568, 15.290)
    spread = math.hypot(gxa-gxq, gya-gyq)

    sx = math.hypot(aa[0]*M, ba[0]*M*COS); sy = math.hypot(aa[1]*M, ba[1]*M*COS)

    out = {
        'map': 'Provinces Illyriennes Servie et Bosnie 1812 (Giraldon; Commons 8297x6080; PD; dlib 6EZTJ9C0)',
        'method': 'OCR mestnih oznak (tesseract eng, PSM 11/12/6/7/8, 3-6x upscale) → LSQ afina + kvadratna preslikava px→WGS84',
        'points': [{'name': p[0], 'px': [p[1], p[2]], 'geo': [p[3], p[4]], 'label': p[5],
                    'residualKm': round(dict((n, r) for r, n in rq)[p[0]], 1)} for p in PTS],
        'residualsKm': {'affineMedian': round(med_a, 1), 'quadMedian': round(med_q, 1),
                        'quadMax': round(rq[-1][0], 1)},
        'scaleMPerPx': {'x': round(sx, 1), 'y': round(sy, 1), 'ratio': round(sx/sy, 3)},
        'griblje': {'geo': [45.568, 15.290], 'pxAffine': [round(gxa), round(gya)],
                    'pxQuad': [round(gxq), round(gyq)], 'modelSpreadPx': round(spread),
                    'uncertaintyKm': round(med_q, 0)},
        'coverage': {n: [round(fq(c[0], c[1])[0], 3), round(fq(c[0], c[1])[1], 3)]
                     for n, c in [('NW', (0, 0)), ('NE', (8297, 0)), ('SW', (0, 6080)), ('SE', (8297, 6080))]},
        'affineCoeffs': {'lat': [round(v, 12) for v in aa.tolist()], 'lng': [round(v, 12) for v in ba.tolist()]},
        'status': 'REVIEW [~] — strojna OCR georeferenca regionalnega lista; centri NAPISOV ne mestnih pik; potrditev: človeška paleografija / QGIS',
        'notes': [
            'meridian label "Meridien" OCR-an na vrhu (px 4212,375) — mrežne stopinje niso bile strojno berljive',
            'parismeridian: nepotrjeno; konstantni člen afine absorbira morebitni zamik',
            'Doboj izločen v preliminarni fazi (residual 20,6 km, negotova identifikacija "Dobos/Ditbor")',
            'razmerje meril 1,024 — lista ni raztegnjena; projekcija na tem obsegu blizu afine',
        ],
    }
    with open('georef-1812.json', 'w') as f:
        json.dump(out, f, indent=1, ensure_ascii=False)

    print(f"točk: {len(PTS)}; afina mediana {med_a:.1f} km; kvadratna mediana {med_q:.1f} km (max {rq[-1][0]:.1f})")
    print(f"merilo: {sx:.0f} × {sy:.0f} m/px (razmerje {sx/sy:.3f})")
    print(f"Griblje: afina px=({gxa:.0f},{gya:.0f}), kvadratna px=({gxq:.0f},{gyq:.0f}), razpon {spread:.0f} px")
    print(f"negotovost: ±{med_q:.0f} km (~±{med_q*1000/sy:.0f} px)")
    print("saved georef-1812.json")

if __name__ == '__main__':
    main()
