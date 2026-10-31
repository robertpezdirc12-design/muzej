#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P168 — forenzični izrezi mrliške 04894, leto 1902 (skeni 85–90).
Trakovi ×2.2 (celotne vrstice; 15 Griblje-1902-kandidatov + meja 1902/03
na s90 + s85-meja-re) + celice ×3.0 (targetirane: vas/hisna + imena +
starosti spornih + Dostal/Rauq podpisi + zapcol rezine).
yc iz /tmp/p168/rows3.json (v3-detekcija + agent-eyes diag-verifikacija
5/5: s86 zap10–21, s87 zap22–33, s88 zap34–45['345'], s89 zap46–57,
s90 zap58–61 + MEJA-1903 + 1903 zap1–7).
Izhod: /tmp/p168/crops/*.png"""
from PIL import Image
import os

OUT = "/tmp/p168/crops"
os.makedirs(OUT, exist_ok=True)

# cell-yc po skenu (rows3.json celice c1–c12 = zap-vrste; s85 iz P167-rows-final)
S85 = {"z4": 1069, "z8": 1610, "z9": 1748, "z10": 1884, "mk": 536}
S86 = {"z10": 401, "z11": 536, "z12": 672, "z13": 808, "z14": 943, "z15": 1079,
       "z16": 1216, "z17": 1355, "z18": 1491, "z19": 1625, "z20": 1760, "z21": 1898}
S87 = {"z22": 403, "z23": 540, "z24": 675, "z25": 810, "z26": 947, "z27": 1083,
       "z28": 1217, "z29": 1352, "z30": 1489, "z31": 1625, "z32": 1763, "z33": 1898}
S88 = {"z34": 399, "z35": 535, "z36": 671, "z37": 805, "z38": 939, "z39": 1077,
       "z40": 1214, "z41": 1352, "z42": 1489, "z43": 1626, "z44": 1765,
       "z45": 1901}
S89 = {"z46": 399, "z47": 537, "z48": 677, "z49": 815, "z50": 951, "z51": 1085,
       "z52": 1222, "z53": 1361, "z54": 1498, "z55": 1636, "z56": 1774, "z57": 1905}
S90 = {"z58": 398, "z59": 533, "z60": 663, "z61": 797, "mk1903": 934,
       "r1": 1072, "r2": 1209, "r3": 1347, "r4": 1484, "r5": 1620,
       "r6": 1757, "r7": 1892}

TRAKT = [
    # --- Griblje-kandidati 1902 (15) ---
    ("griblje-s85-z4-janez-pezdirec", 85, S85["z4"]),
    ("griblje-s85-z8-matija-prinec", 85, S85["z8"]),
    ("griblje-s85-z10-matija-dehlic", 85, S85["z10"]),
    ("griblje-s86-z11-nikolaj-tome", 86, S86["z11"]),
    ("griblje-s86-z13-anton-stravs", 86, S86["z13"]),
    ("griblje-s86-z15-katarina-zupanic", 86, S86["z15"]),
    ("griblje-s86-z16-mihail-bondivec", 86, S86["z16"]),
    ("griblje-s86-z17-marjeta-zogriva", 86, S86["z17"]),
    ("griblje-s86-z21-marko-srobrijan", 86, S86["z21"]),
    ("griblje-s87-z22-veria-macvar", 87, S87["z22"]),
    ("griblje-s88-z45-ana-simec", 88, S88["z45"]),
    ("griblje-s89-z49-alojzij-stravs", 89, S89["z49"]),
    ("griblje-s89-z54-marija-novak", 89, S89["z54"]),
    ("griblje-s89-z55-ana-bendirec", 89, S89["z55"]),
    ("griblje-s89-z56-matija-brunez", 89, S89["z56"]),
    ("griblje-s90-z59-marjeta-mkek", 90, S90["z59"]),
    ("griblje-s90-z61-janez-brinec", 90, S90["z61"]),
    # --- meja 1902/03 (s90): zadnji-1902 + marker + prvi-1903 ---
    ("meja-1902-03-z61-zadnji-1902", 90, S90["z61"]),
    ("meja-1902-03-marker-1903", 90, S90["mk1903"]),
    ("meja-1902-03-z1-prvi-1903", 90, S90["r1"]),
    # --- s85-meja-re (P167-meja 1901/02 re-potrditev) ---
    ("meja-1901-02-marker-1903-re", 85, S85["mk"]),
]

CELLS = [
    # --- vas+hisna ×3.0 (vseh 15 Griblje) ---
    ("s85-z4-vas-hisna", 85, S85["z4"]),
    ("s85-z8-vas-hisna", 85, S85["z8"]),
    ("s85-z10-vas-hisna", 85, S85["z10"]),
    ("s86-z11-vas-hisna", 86, S86["z11"]),
    ("s86-z13-vas-hisna", 86, S86["z13"]),
    ("s86-z15-vas-hisna", 86, S86["z15"]),
    ("s86-z16-vas-hisna", 86, S86["z16"]),
    ("s86-z17-vas-hisna", 86, S86["z17"]),
    ("s86-z21-vas-hisna", 86, S86["z21"]),
    ("s87-z22-vas-hisna", 87, S87["z22"]),
    ("s88-z45-vas-hisna", 88, S88["z45"]),
    ("s89-z49-vas-hisna", 89, S89["z49"]),
    ("s89-z54-vas-hisna", 89, S89["z54"]),
    ("s89-z55-vas-hisna", 89, S89["z55"]),
    ("s89-z56-vas-hisna", 89, S89["z56"]),
    ("s90-z59-vas-hisna", 90, S90["z59"]),
    ("s90-z61-vas-hisna", 90, S90["z61"]),
    # --- imena (konflikti: Prinec/Brunez/Brinec + Mkek/Milek + Bendirec) ---
    ("s85-z8-ime", 85, S85["z8"]),
    ("s85-z10-ime", 85, S85["z10"]),
    ("s89-z55-ime", 89, S89["z55"]),
    ("s89-z56-ime", 89, S89["z56"]),
    ("s90-z59-ime", 90, S90["z59"]),
    ("s90-z61-ime", 90, S90["z61"]),
    # --- starosti spornih (s85-z10 '3', s89-z49 '1-leta?', s89-z55 56?, s90-z61 92?) ---
    ("s85-z4-starost", 85, S85["z4"]),
    ("s85-z8-starost", 85, S85["z8"]),
    ("s85-z10-starost", 85, S85["z10"]),
    ("s89-z49-starost", 89, S89["z49"]),
    ("s89-z55-starost", 89, S89["z55"]),
    ("s89-z56-starost", 89, S89["z56"]),
    ("s90-z59-starost", 90, S90["z59"]),
    ("s90-z61-starost", 90, S90["z61"]),
    # --- podpisi: Dostal-varianta (Hanš./Hemislav/Stanislav/Haniel) + Rauq ---
    ("s86-z12-podpis-dostal", 86, S86["z12"]),
    ("s87-z22-podpis-dostal", 87, S87["z22"]),
    ("s88-z36-podpis-dostal", 88, S88["z36"]),
    ("s89-z49-podpis-dostal", 89, S89["z49"]),
    ("s86-z10-podpis-rauq", 86, S86["z10"]),
    ("s90-z58-podpis-rauq", 90, S90["z58"]),
    # --- zapcol spot-checks (zap-dup-10 + '345' + γ-cifre) ---
    ("s85-z9-zapcol", 85, S85["z9"]),
    ("s85-z10-zapcol", 85, S85["z10"]),
    ("s86-z10-zapcol", 86, S86["z10"]),
    ("s86-z11-zapcol", 86, S86["z11"]),
    ("s88-z45-zapcol", 88, S88["z45"]),
    ("s89-z49-zapcol", 89, S89["z49"]),
    ("s89-z56-zapcol", 89, S89["z56"]),
    ("s90-z59-zapcol", 90, S90["z59"]),
]

T_X = (100, 2450)   # trak x-range
C_X = (520, 900)    # celica vas+hisna
I_X = (860, 1400)   # ime
S_X = (1770, 2200)  # starost
P_X = (2080, 2470)  # podpis
Z_X = (80, 200)     # zapcol (zap št. ~0.035–0.075 × 2640)


def crop(name, scan, x0, x1, yc, half, zoom):
    im = Image.open(f"/tmp/p168/s{scan:02d}.jpg")
    c = im.crop((x0, max(0, yc - half), x1, min(im.size[1], yc + half)))
    c = c.resize((int(c.size[0] * zoom), int(c.size[1] * zoom)), Image.LANCZOS)
    c.save(f"{OUT}/{name}.png")
    return c.size


def main():
    n = 0
    for (name, scan, yc) in TRAKT:
        crop(name, scan, T_X[0], T_X[1], yc, 90, 2.2)
        n += 1
    for (name, scan, yc) in CELLS:
        if "podpis" in name:
            x0, x1 = P_X
        elif "ime" in name:
            x0, x1 = I_X
        elif "starost" in name:
            x0, x1 = S_X
        elif "zapcol" in name:
            x0, x1 = Z_X
        else:
            x0, x1 = C_X
        half = 100 if "zapcol" in name else 85
        zoom = 2.5 if "zapcol" in name else 3.0
        crop(name, scan, x0, x1, yc, half, zoom)
        n += 1
    print(f"crops: {n} shranjenih ({len(TRAKT)} trakov + {len(CELLS)} celic)")


if __name__ == "__main__":
    main()
