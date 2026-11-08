#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P171 — forenzični izrezi mrliške 04894, leto 1905 (skeni 99–104).
Trakovi ×2.2 (16 Griblje-1905) + celice ×3.0 (targetirane forenzike:
z1-Pezdirec/h59/72let + 10-glava-napak + starost-korekcije + imena
Caprič/Lapajne + ŠTRAVS-h35 + Anton-Kukar + MEJA-1906 pas).
yc iz /tmp/p171/rows3.json (v3-detekcija + diag-vizualna-verifikacija
6-strani-z-Read-očmi: s99 zap1–12, s100 zap13–24, s101 zap25–36,
s102 zap37–48, s103 zap49–60, s104 zap61 + MEJA-1906 + 1906-z1–9!).
Izhod: /tmp/p171/crops/*.png"""
from PIL import Image
import os

OUT = "/tmp/p171/crops"
os.makedirs(OUT, exist_ok=True)

# cell-yc po skenu (rows3.json: c0 = GLAVA-ostanek, c1–c12 = zap-vrste!
# p169-recept 'c0=naslov-ostanek' — diag-vizualno-potrijeno ×6!)
S99 = {"z1": 380, "z2": 510, "z3": 643, "z4": 779, "z5": 916, "z6": 1051,
       "z7": 1187, "z8": 1323, "z9": 1456, "z10": 1588, "z11": 1720, "z12": 1852}
S100 = {"z13": 387, "z14": 521, "z15": 653, "z16": 787, "z17": 922, "z18": 1057,
        "z19": 1190, "z20": 1326, "z21": 1465, "z22": 1602, "z23": 1737,
        "z24": 1868}
S101 = {"z25": 391, "z26": 527, "z27": 664, "z28": 797, "z29": 931, "z30": 1065,
        "z31": 1198, "z32": 1334, "z33": 1511, "z34": 1610, "z35": 1747,
        "z36": 1881}
S102 = {"z37": 389, "z38": 528, "z39": 666, "z40": 802, "z41": 939, "z42": 1075,
        "z43": 1209, "z44": 1344, "z45": 1480, "z46": 1620, "z47": 1839,
        "z48": 1894}
S103 = {"z49": 388, "z50": 525, "z51": 664, "z52": 801, "z53": 938, "z54": 1077,
        "z55": 1217, "z56": 1354, "z57": 1493, "z58": 1631, "z59": 1764,
        "z60": 1895}
S104 = {"z61": 385, "z62": 518, "MEJA": 632, "r1": 746, "r2": 883, "r3": 1022,
        "r4": 1158, "r5": 1294, "r6": 1432, "r7": 1567, "r8": 1703, "r9": 1872}
GLAVA = 155  # letnica-glava y (vsi skeni)

TRAKT = [
    # --- 16 Griblje-1905 (celotne vrstice) ---
    ("griblje-s99-z1-marjeta", 99, S99["z1"]),
    ("griblje-s100-z16-marija-hrizan", 100, S100["z16"]),
    ("griblje-s100-z19-amalija", 100, S100["z19"]),
    ("griblje-s100-z20-ana-simec", 100, S100["z20"]),
    ("griblje-s100-z24-marija-brinec", 100, S100["z24"]),
    ("griblje-s101-z26-janez-tome", 101, S101["z26"]),
    ("griblje-s101-z29-andrej-verbicar", 101, S101["z29"]),
    ("griblje-s102-z39-marija-jakofcic", 102, S102["z39"]),
    ("griblje-s102-z40-marija-kukar", 102, S102["z40"]),
    ("griblje-s102-z44-anton-kukar", 102, S102["z44"]),
    ("griblje-s102-z47-matija-milek", 102, S102["z47"]),
    ("griblje-s103-z49-marjeta-capric", 103, S103["z49"]),
    ("griblje-s103-z50-marija-urh", 103, S103["z50"]),
    ("griblje-s103-z52-ana-simec", 103, S103["z52"]),
    ("griblje-s103-z59-martin-stravs", 103, S103["z59"]),
    ("griblje-s104-z61-anton-pezdirec", 104, S104["z61"]),
    # --- kontekst (non-Griblje forenzika) ---
    ("s100-z15-jozef-pesdirec-kontekst", 100, S100["z15"]),
    ("s101-z27-martin-pezdirec-kontekst", 101, S101["z27"]),
]

CELLS = [
    # --- z1 PEZDIREC forenzika (×4) ---
    ("s99-z1-vas-hisna", 99, S99["z1"]),
    ("s99-z1-ime", 99, S99["z1"]),
    ("s99-z1-starost", 99, S99["z1"]),
    ("s99-z1-bolezen", 99, S99["z1"]),
    # --- s99 kontekst forenzika ---
    ("s99-z5-vas-hisna", 99, S99["z5"]),
    ("s99-z8-ime", 99, S99["z8"]),
    ("s99-z10-vas-hisna", 99, S99["z10"]),
    ("s99-z4-starost", 99, S99["z4"]),
    ("s99-z7-starost", 99, S99["z7"]),
    ("s99-z9-starost", 99, S99["z9"]),
    ("s99-z10-starost", 99, S99["z10"]),
    ("s99-z6-ime", 99, S99["z6"]),
    ("s99-z11-ime", 99, S99["z11"]),
    ("s99-z12-ime", 99, S99["z12"]),
    # --- s100 forenzika ---
    ("s100-z15-starost", 100, S100["z15"]),
    ("s100-z16-ime", 100, S100["z16"]),
    ("s100-z19-ime", 100, S100["z19"]),
    ("s100-z19-starost", 100, S100["z19"]),
    ("s100-z20-ime", 100, S100["z20"]),
    ("s100-z20-bolezen", 100, S100["z20"]),
    ("s100-z24-starost", 100, S100["z24"]),
    # --- s101 forenzika ---
    ("s101-z26-ime", 101, S101["z26"]),
    ("s101-z27-ime", 101, S101["z27"]),
    ("s101-z29-ime", 101, S101["z29"]),
    ("s101-z30-starost", 101, S101["z30"]),
    ("s101-z31-starost", 101, S101["z31"]),
    ("s101-z32-starost", 101, S101["z32"]),
    # --- s102 forenzika ---
    ("s102-z37-starost", 102, S102["z37"]),
    ("s102-z38-bolezen", 102, S102["z38"]),
    ("s102-z39-starost", 102, S102["z39"]),
    ("s102-z41-starost", 102, S102["z41"]),
    ("s102-z44-ime", 102, S102["z44"]),
    ("s102-z44-starost", 102, S102["z44"]),
    ("s102-z45-vas-hisna", 102, S102["z45"]),
    ("s102-z48-ime", 102, S102["z48"]),
    ("s102-z48-starost", 102, S102["z48"]),
    # --- s103 forenzika ---
    ("s103-z49-ime", 103, S103["z49"]),
    ("s103-z49-vas-hisna", 103, S103["z49"]),
    ("s103-z50-ime", 103, S103["z50"]),
    ("s103-z53-starost", 103, S103["z53"]),
    ("s103-z54-ime", 103, S103["z54"]),
    ("s103-z57-bolezen", 103, S103["z57"]),
    ("s103-z59-ime", 103, S103["z59"]),
    ("s103-z59-starost", 103, S103["z59"]),
    ("s103-z59-vas-hisna", 103, S103["z59"]),
    # --- s104 forenzika (meja + zap61 + P172-lead) ---
    ("s104-z61-vas-hisna", 104, S104["z61"]),
    ("s104-z61-ime", 104, S104["z61"]),
    ("s104-z61-starost", 104, S104["z61"]),
    ("s104-z61-bolezen", 104, S104["z61"]),
    ("s104-r6-ime", 104, S104["r6"]),
]

T_X = (100, 2450)   # trak x-range
C_X = (520, 900)    # celica vas+hisna
I_X = (860, 1400)   # ime
S_X = (1770, 2200)  # starost
B_X = (1500, 2080)  # bolezen
P_X = (2080, 2470)  # podpis
Z_X = (80, 200)     # zapcol
G_X = (100, 900)    # glava (Leto NNNN)


def crop(name, scan, x0, x1, yc, half, zoom):
    im = Image.open(f"/tmp/p171/s{scan}.jpg")
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
        if "bolezen" in name:
            x0, x1 = B_X
        elif "starost" in name:
            x0, x1 = S_X
        elif "ime" in name:
            x0, x1 = I_X
        elif "zapcol" in name:
            x0, x1 = Z_X
        else:
            x0, x1 = C_X
        half = 100 if "zapcol" in name else 85
        zoom = 2.5 if "zapcol" in name else 3.0
        crop(name, scan, x0, x1, yc, half, zoom)
        n += 1
    # glave (10. napaka-vzorec: s99 '18905'!)
    for name, scan in [("glava-s99-18905", 99), ("glava-s101-18", 101),
                       ("glava-s102-18905", 102), ("glava-s103-18905", 103)]:
        crop(name, scan, G_X[0], G_X[1], GLAVA, 70, 2.0)
        n += 1
    # MEJA 1906 pas (širok, ~1.6 zoom)
    im = Image.open("/tmp/p171/s104.jpg")
    c = im.crop((300, S104["z62"] + 30, 1900, S104["r1"] - 10))
    c = c.resize((int(c.size[0] * 1.6), int(c.size[1] * 1.6)), Image.LANCZOS)
    c.save(f"{OUT}/meja-1906-pas.png")
    n += 1
    print(f"crops: {n} ({len(TRAKT)} trakov + {len(CELLS)} celic + 4 glave + meja)")


if __name__ == "__main__":
    main()
