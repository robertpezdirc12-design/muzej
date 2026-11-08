#!/usr/bin/env python3
"""
GEOREF 1812 — DRUGI SKEN (P7: koroboracija georeference na neodvisnem skenu)
============================================================================
Drugi sken istega lista (Lapie/Malte-Brun/Chamouin/Giraldon; Internet Archive,
7636 × 5936 px, javna last). Sključno s P6 je bil georeferenciran PRVI sken
(Commons 8297 × 6080). Namen P7: preveriti, da rezultat P6 NI artefakt skeniranja.

Metoda (deterministična, 0 SDK):
 1. REGISTRACIJA LISTA: ORB (~30k značilk na sken) + BFMatcher + RANSAC afina
    sken1→sken2 (regis-orb.json): 4030/4670 inlierjev, RMS 3,9 px — oba skena
    sta ista lista, povezana skoraj-similariteto (merilo 0,8187/0,8148,
    rotacija ~0,3°, strig ~0,03°).
 2. OCR DRUGA SKENA: napovedane lege oznak (iz registracije) → ozki izrezi
    (3–8×, CLAHE/OTSU/erode) → 12 oznak prebranih v drugem skenu
    (scan2-labels.json): 5 celih (Pest, Nissa, WIDDIN, Raguse, Semlin) +
    7 fragmentov (Bel, Prist, Agr, icone, eobern, aye, wor — enaki fragmenti
    kot v prvem skenu pri Bel/Prist). Laibach/Fiume/Trieste/BanyaLuka v
    drugem skenu NEberljivi (verjetno pregibi knjižnega zvezka).
 3. NEODVISEN GEO-MODEL DRUGEGA SKENA: LSQ afina px→WGS84 na 12 točkah
    (vključno Nissa = Niš, ki je ni v modelu prvega skena).
 4. KOROBORACIJA GRIBLJE (ključno merilo):
    - POT A: Griblje geo → model1⁻¹ → px1 (2499,2286) → registracija → px2
    - POT B: Griblje geo → model2⁻¹ → px2 (neposredno iz drugega skena)
    - |POT A − POT B| = sporazumenje o legi Gribelj na listu med skenoma.

Poganjanje:
    python3 research/georef-1812/fit-georef-second.py   # predpogoj: orig-1812-second.jpg, regis-orb.json, scan2-labels.json
"""

import json, math
import numpy as np

# ——— točke drugega skena: izmerjeni centri oznak (px) → realne koordinate ———
L2 = json.load(open('scan2-labels.json'))
GEO = {
    'Pest':      (47.497, 19.041),
    'Leoben':    (47.383, 15.094),
    'Ancona':    (43.622, 13.508),
    'Vidin':     (43.993, 22.868),
    'Semlin':    (44.843, 20.400),
    'Zvornik':   (44.387, 19.093),
    'Pristina':  (42.664, 21.166),
    'Belgrade':  (44.817, 20.457),
    'Sarajevo':  (43.857, 18.413),
    'Ragusa':    (42.651, 18.091),
    'Agram':     (45.815, 15.982),
    'Nissa':     (43.320, 21.903),   # Niš — nova točka, ni je v modelu skena 1
}
FULL = {'Pest', 'Nissa', 'Vidin', 'Ragusa', 'Semlin'}  # cele besede; ostalo fragmenti [~]

PTS = [(n, L2[n]['px'][0], L2[n]['px'][1], GEO[n][0], GEO[n][1]) for n in GEO if n in L2]

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

def invert(f, lat, lng, x0, y0):
    x, y = x0, y0
    for _ in range(60):
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
    med_full = [r for r, n in rq if n in FULL]
    med_full = sorted(med_full)[len(med_full)//2] if med_full else None

    sx = math.hypot(aa[0]*M, ba[0]*M*COS); sy = math.hypot(aa[1]*M, ba[0]*M*COS)
    # proper: sy uses ba[1]
    sy = math.hypot(aa[1]*M, ba[1]*M*COS)

    # ——— Griblje po POTI B: neposredno iz modela 2. skena ———
    gxa, gya = invert(fa, 45.568, 15.290, 2513.0, 2003.0)
    gxq, gyq = invert(fq, 45.568, 15.290, 2513.0, 2003.0)
    spread = math.hypot(gxa-gxq, gya-gyq)

    # ——— POT A: registracija (sken1 → sken2) ———
    d = json.load(open('regis-orb.json'))
    R = np.array(d['M_work']); k1 = d['k1']; k2 = d['k2']
    pA = R @ np.array([2499*k1, 2286*k1, 1.0]); pA = (pA[0]/k2, pA[1]/k2)

    # ——— sporazumenje ———
    agree_px = math.hypot(pA[0]-gxa, pA[1]-gya)
    agree_km = agree_px * (sx/1000.0)

    # kam kaže model 2. skena za ista mesta kot model 1. skena (veriga geo)
    out = {
        'map': 'Provinces Illyriennes Servie et Bosnie 1812 — DRUGI SKEN (Lapie/Malte-Brun/Chamouin/Giraldon; Internet Archive 7636x5936; PD)',
        'method': 'ORB+RANSAC registracija sken1→sken2 (4030 inlierjev, RMS 3,9 px) → OCR 12 oznak 2. skena (3-8× izrezi) → LSQ afina+kvadratna px→WGS84; koroboracija: POT A (model1+registracija) vs POT B (model2)',
        'points': [{'name': p[0], 'px': [p[1], p[2]], 'geo': [p[3], p[4]],
                    'word': L2[p[0]]['text'], 'full': p[0] in FULL,
                    'residualKm': round(dict((n, r) for r, n in rq)[p[0]], 1)} for p in PTS],
        'residualsKm': {'affineMedian': round(med_a, 1), 'quadMedian': round(med_q, 1),
                        'quadMedianFullWords': round(med_full, 1) if med_full else None,
                        'quadMax': round(rq[-1][0], 1)},
        'scaleMPerPx': {'x': round(sx, 1), 'y': round(sy, 1), 'ratio': round(sx/sy, 3)},
        'registration': {'inliers': d['inliers'], 'matches': d['matches'],
                         'rmsFullPx': round(d['rmsWorkPx']/k2, 1),
                         'scaleXY': [round(R[0,0]*k1/k2, 5), round(R[1,1]*k1/k2, 5)],
                         'rotDeg': round(math.degrees(math.atan2(R[1,0], R[0,0])), 2)},
        'griblje': {
            'geo': [45.568, 15.290],
            'pxPathA_registration': [round(pA[0]), round(pA[1])],
            'pxPathB_affine': [round(gxa), round(gya)],
            'pxPathB_quad': [round(gxq), round(gyq)],
            'modelSpreadPx': round(spread),
            'agreementPx': round(agree_px),
            'agreementKm': round(agree_km, 1),
        },
        'status': 'REVIEW [~] — koroboracija na drugem skenu istega lista; 7/12 točk so fragmenti oznak (bias centra ±1–3 km); Laibach/Fiume/Trieste/BanyaLuka v 2. skenu neberljivi (pregibi)',
        'notes': [
            'sken 2 je knjižni sken zloženega priloga — nekateri napisi na pregibih neberljivi',
            'Nissa (Niš) je nova kontrolna točka, ki je NI v modelu 1. skena — model 2. skena je neodvisno 12-točkovni',
            'POT A uporablja izključno model 1. skena + slikovno registracijo; POT B izključno OCR 2. skena — merjeni sporazumenje |A−B| je čista koroboracija',
            'isti fragmenti (Bel, Prist) kot v skenu 1 — primerljive meritve centrov',
        ],
    }
    with open('georef-1812-second.json', 'w') as f:
        json.dump(out, f, indent=1, ensure_ascii=False)

    print(f"točk: {len(PTS)} (celih besed: {len(FULL & set(GEO))}); afina mediana {med_a:.1f} km; kvadratna mediana {med_q:.1f} km (max {rq[-1][0]:.1f})")
    if med_full: print(f"mediana samo CELIH besed: {med_full:.1f} km")
    print(f"merilo 2. skena: {sx:.0f} × {sy:.0f} m/px (razmerje {sx/sy:.3f})")
    print(f"POT A (model1+registracija): Griblje px2 = ({pA[0]:.0f},{pA[1]:.0f})")
    print(f"POT B (model2 afina):        Griblje px2 = ({gxa:.0f},{gya:.0f})  [kvadratna: ({gxq:.0f},{gyq:.0f})]")
    print(f"SPORAZUMENJE: {agree_px:.0f} px = {agree_km:.1f} km")
    print(f"model spread (afina/kvadratna): {spread:.0f} px")
    print("saved georef-1812-second.json")

if __name__ == '__main__':
    main()
