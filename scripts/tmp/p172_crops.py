#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P172 — forenzični izrezi mrliške 04894, leto 1940 (skeni 104–108).
Trakovi ×2.2 (10 Griblje-1940) + celice ×3.0 (targetirane forenzike:
z1-Brinec/h49-vs-19 + z6-bolezen + z16-ime + z21-ime/Kuhinek-podpis
+ z48-ime-Joček + z54-ime-Šimec + GLAVE-napake ×4).
yc = P172-diag-vizualno-prebrane (Read-oči ×7: s104–s110, P170-recept!)
Izhod: /tmp/p172/crops/*.png"""
from PIL import Image
import os

OUT = "/tmp/p172"
os.makedirs(f"{OUT}/crops", exist_ok=True)

# yc po skenu (diag-vizualna-verifikacija 7-strani-z-Read-očmi!)
S104 = {"z61": 385, "z62": 518, "MEJA": 632, "z1": 746, "z2": 880, "z3": 1015,
        "z4": 1150, "z5": 1290, "z6": 1425, "z7": 1560, "z8": 1695, "z9": 1830}
S105 = {"z10": 390, "z11": 525, "z12": 660, "z13": 795, "z14": 930, "z15": 1065,
        "z16": 1200, "z17": 1335, "z18": 1470, "z19": 1605, "z20": 1740, "z21": 1875}
S106 = {"z21": 390, "z22": 525, "z23": 660, "z24": 795, "z25": 930, "z26": 1065,
        "z27": 1200, "z28": 1335, "z29": 1470, "z30": 1605, "z31": 1740, "z32": 1875}
S107 = {"z33": 390, "z34": 525, "z35": 660, "z36": 795, "z37": 930, "z38": 1065,
        "z39": 1200, "z40": 1335, "z41": 1470, "z42": 1605, "z43": 1740, "z44": 1875}
S108 = {"z45": 390, "z46": 525, "z47": 660, "z48": 795, "z49": 930, "z50": 1065,
        "z51": 1200, "z52": 1335, "z53": 1470, "z54": 1605, "z55": 1740}
GLAVA = 155  # letnica-glava y (vsi skeni)

TRAKT = [
    # --- 10 Griblje-1940 (celotne vrstice) ---
    ("griblje-s104-z1-ana-brinec", 104, S104["z1"]),
    ("griblje-s104-z6-katarina-pezdirec", 104, S104["z6"]),
    ("griblje-s105-z16-matija-strukelj", 105, S105["z16"]),
    ("griblje-s105-z21-janez-krizc", 105, S105["z21"]),
    ("griblje-s106-z23-katarina-simec", 106, S106["z23"]),
    ("griblje-s106-z29-matija-tozek", 106, S106["z29"]),
    ("griblje-s107-z34-matija-urh", 107, S107["z34"]),
    ("griblje-s107-z35-janez-focek", 107, S107["z35"]),
    ("griblje-s108-z48-jurij-jocek", 108, S108["z48"]),
    ("griblje-s108-z54-alojz-simec", 108, S108["z54"]),
    # --- kontekst: MEJA + 1907-z1 (s109 Brinec Ana/Anton?) ---
    ("s104-meja-1940-pas", 104, S104["MEJA"]),
    ("s109-z1-anton-ali-ana-brinec", 109, 530),
    ("s109-z2-ana-veljko", 109, 660),
    ("s109-z4-ana-mec-h91", 109, 930),
]

CELLS = [
    # --- forenzika: zmede (×3.0) ---
    ("cell-s104-z1-hisna-h49-vs-19", 104, S104["z1"], 1180, 1560),   # hišna št. celica
    ("cell-s104-z6-bolezen-nadruka", 104, S104["z6"], 2050, 2600),   # bolezen
    ("cell-s104-z1-ime-ana-brinec", 104, S104["z1"], 1560, 2200),    # ime+stan
    ("cell-s105-z16-ime-strukelj", 105, S105["z16"], 1560, 2200),
    ("cell-s105-z21-ime-krizc-podpis", 105, S105["z21"], 1560, 3400),
    ("cell-s108-z48-ime-jocek", 108, S108["z48"], 1560, 2200),
    ("cell-s108-z54-ime-simec", 108, S108["z54"], 1560, 2200),
    ("cell-s108-z48-hisna-h77", 108, S108["z48"], 1180, 1560),
    ("cell-s108-z54-hisna-h18", 108, S108["z54"], 1180, 1560),
]

# --- GLAVE-napake (celice) ---
GLAVE = [
    ("cell-s104-glava-48-1905", 104),
    ("cell-s105-glava-18906", 105),
    ("cell-s106-glava-187006", 106),
    ("cell-s107-glava-187006", 107),
    ("cell-s108-glava-187006", 108),
]


def trakt(scan, yc):
    im = Image.open(f"{OUT}/s{scan}.jpg")
    w, h = im.size
    y0, y1 = max(0, yc - int(90 * 2.2)), min(h, yc + int(45 * 2.2))
    c = im.crop((0, y0, w, y1))
    c = c.resize((int(c.width * 2.2), int(c.height * 2.2)), Image.LANCZOS)
    return c


def cell(scan, yc, x0f, x1f):
    im = Image.open(f"{OUT}/s{scan}.jpg")
    w, h = im.size
    y0, y1 = max(0, yc - 62), min(h, yc + 62)
    c = im.crop((int(w * x0f / 4000), y0, int(w * x1f / 4000), y1))
    c = c.resize((int(c.width * 3.0), int(c.height * 3.0)), Image.LANCZOS)
    return c


for nm, scan, yc in TRAKT:
    trakt(scan, yc).save(f"{OUT}/crops/{nm}.png")
    print(f"TRAKT {nm}")
for nm, scan, yc, x0, x1 in CELLS:
    cell(scan, yc, x0, x1).save(f"{OUT}/crops/{nm}.png")
    print(f"CELL  {nm}")
for nm, scan in GLAVE:
    cell(scan, GLAVA, 150, 1050).save(f"{OUT}/crops/{nm}.png")
    print(f"GLAVA {nm}")
print("KONČANO")
