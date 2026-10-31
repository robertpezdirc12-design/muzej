#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P167 — forenzični izrezi mrliške 04894, leto 1901 (skeni 80–85).
Trakovi ×2.2 (celotne vrstice; 10 Griblje-1901 + meja 1901/02 na s85)
+ celice ×3.0 (targetirane: vas/hisna + imena + starosti spornih +
duhovnik Kut'nek-dominanta + P166-lead-re-potrditev s80-dno).
Izhod: /tmp/p167/crops/*.png
yc iz /tmp/p167/rows.json (p167_rows_final — agent-eyes potrjeno)."""
from PIL import Image
import os

OUT = "/tmp/p167/crops"
os.makedirs(OUT, exist_ok=True)

# zap-yc po skenu (rows.json / p167_rows_final)
S80 = {"z57": 373, "z59": 641, "z61": 895, "mk": 1035, "r1": 1174, "r4": 1571}
S81 = {"z7": 375, "z8": 513, "z9": 650, "z10": 787, "z11": 924, "z12": 1061,
       "z13": 1192, "z14": 1324, "z15": 1461, "z16": 1595, "z17": 1731, "z18": 1867}
S82 = {"z19": 395, "z20": 533, "z21": 672, "z22": 810, "z23": 947, "z24": 1086,
       "z25": 1223, "z26": 1360, "z27": 1499, "z28": 1637, "z29": 1774, "z30": 1907}
S83 = {"z31": 391, "z32": 529, "z33": 665, "z34": 799, "z35": 934, "z36": 1070,
       "z37": 1207, "z38": 1343, "z39": 1480, "z40": 1618, "z41": 1756, "z42": 1897}
S84 = {"z43": 395, "z44": 531, "z45": 667, "z46": 803, "z47": 939, "z48": 1073,
       "z49": 1209, "z50": 1344, "z51": 1476, "z52": 1606, "z53": 1737, "z54": 1869}
S85 = {"z55": 395, "mk": 536, "r1": 676, "r2": 807, "r3": 937, "r4": 1069,
       "r5": 1203, "r6": 1339, "r7": 1474, "r8": 1610, "r9": 1748, "r10": 1884}

CROPS = [
    # --- Griblje ×10 (1901): trakovi (polna širina, yc±90) ---
    ("griblje-zap1-ana-krizan-80dno", 80, S80["r1"]),
    ("griblje-zap4-matija-hlobucar-80dno", 80, S80["r4"]),
    ("griblje-zap7-anton-stolfa-81", 81, S81["z7"]),
    ("griblje-zap11-marija-brinec-81", 81, S81["z11"]),
    ("griblje-zap13-marija-cindric-81", 81, S81["z13"]),
    ("griblje-zap15-ana-milek-81", 81, S81["z15"]),
    ("griblje-zap19-martin-papic-82", 82, S82["z19"]),
    ("griblje-zap50-janez-kesran-84", 84, S84["z50"]),
    ("griblje-zap51-janez-jakobcic-84", 84, S84["z51"]),
    ("griblje-zap55-nikolaj-rampic-85", 85, S85["z55"]),
    # --- meja 1901/02 (s85): zadnja-1901 + marker-1902 + prvi-1902 ---
    ("meja-1901-02-zap55-zadnji-1901", 85, S85["z55"]),
    ("meja-1901-02-marker-1902", 85, S85["mk"]),
    ("meja-1901-02-zap1-prvi-1902", 85, S85["r1"]),
    # --- re-potrditev meja: 1900/01 (s80, P166-reuse) ---
    ("meja-1900-01-marker-1901-re", 80, S80["mk"]),
    ("meja-1900-01-zap1-prvi-1901-re", 80, S80["r1"]),
]

CELLS = [
    # --- Griblje vas-hisna ×3.0 (vsi 10) ---
    ("s80-r1-vas-hisna", 80, S80["r1"]),
    ("s80-r4-vas-hisna", 80, S80["r4"]),
    ("s81-zap7-vas-hisna", 81, S81["z7"]),
    ("s81-zap11-vas-hisna", 81, S81["z11"]),
    ("s81-zap13-vas-hisna", 81, S81["z13"]),
    ("s81-zap15-vas-hisna", 81, S81["z15"]),
    ("s82-zap19-vas-hisna", 82, S82["z19"]),
    ("s84-zap50-vas-hisna", 84, S84["z50"]),
    ("s84-zap51-vas-hisna", 84, S84["z51"]),
    ("s85-zap55-vas-hisna", 85, S85["z55"]),
    # --- imena (sporna: Štolfa/Štolfa?, Kešran/Križan?, Rampič?, Papič?) ---
    ("s81-zap7-ime", 81, S81["z7"]),
    ("s81-zap13-ime", 81, S81["z13"]),
    ("s82-zap19-ime", 82, S82["z19"]),
    ("s84-zap50-ime", 84, S84["z50"]),
    ("s84-zap51-ime", 84, S84["z51"]),
    ("s85-zap55-ime", 85, S85["z55"]),
    # --- starosti spornih ---
    ("s80-r1-starost", 80, S80["r1"]),
    ("s80-r4-starost", 80, S80["r4"]),
    ("s84-zap50-starost", 84, S84["z50"]),
    ("s84-zap51-starost", 84, S84["z51"]),
    ("s85-zap55-starost", 85, S85["z55"]),
    # --- duhovnik: Kut'nek-dominanta + kontrast ---
    ("s81-zap7-podpis", 81, S81["z7"]),
    ("s81-zap11-podpis", 81, S81["z11"]),
    ("s84-zap50-podpis", 84, S84["z50"]),
    ("s85-zap55-podpis", 85, S85["z55"]),
    ("s82-zap20-podpis-rauq", 82, S82["z20"]),
    ("s83-zap32-podpis", 83, S83["z32"]),
]

T_X = (100, 2450)   # trak x-range
C_X = (520, 900)    # celica vas+hisna
I_X = (860, 1400)   # ime
S_X = (1770, 2200)  # starost
P_X = (2080, 2470)  # podpis


def crop(name, scan, x0, x1, yc, half, zoom):
    im = Image.open(f"/tmp/p167/s{scan:02d}.jpg")
    c = im.crop((x0, max(0, yc - half), x1, min(im.size[1], yc + half)))
    c = c.resize((int(c.size[0] * zoom), int(c.size[1] * zoom)), Image.LANCZOS)
    c.save(f"{OUT}/{name}.png")
    return c.size


def main():
    n = 0
    for (name, scan, yc) in CROPS:
        crop(name, scan, T_X[0], T_X[1], yc, 90, 2.2)
        n += 1
    for (name, scan, yc) in CELLS:
        if "podpis" in name:
            x0, x1 = P_X
        elif "ime" in name:
            x0, x1 = I_X
        elif "starost" in name:
            x0, x1 = S_X
        else:
            x0, x1 = C_X
        crop(name, scan, x0, x1, yc, 85, 3.0)
        n += 1
    print(f"crops: {n} shranjenih ({len(CROPS)} trakov + {len(CELLS)} celic)")


if __name__ == "__main__":
    main()
