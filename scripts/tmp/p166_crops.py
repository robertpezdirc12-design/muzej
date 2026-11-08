#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P166 — forenzični izrezi mrliške 04894, leto 1900 (skeni 75–80).
Trakovi ×2.2 (celotne vrstice; 12 Griblje + meje 1900 + meja 1900/01)
+ celice ×3.0 (targetirane: sporna imena/hišne, duhovnik J.R. Kut'nek,
P167-lead Griblje-1901). Izhod: /tmp/p166/crops/*.png
yc iz /tmp/p166/rows.json (p166_rows_final — agent-eyes potrjeno)."""
from PIL import Image
import os

OUT = "/tmp/p166/crops"
os.makedirs(OUT, exist_ok=True)

# (ime, sken, x0, y0, x1, y1, zoom)
YC = {  # zap-yc po skenu (rows.json)
    75: {"z60": 383, "z61": 520, "mk": 660, "z1": 848, "z3": 1112, "z4": 1247, "z8": 1787},
    76: {"z9": 399, "z10": 525, "z14": 927, "z16": 1204},
    77: {"z21": 391},
    78: {"z34": 521, "z38": 1058, "z40": 1320, "z41": 1454},
    79: {"z45": 383, "z49": 1058, "z50": 1196, "z53": 1474},
    80: {"z57": 373, "z59": 641, "z61": 895, "mk": 1035, "r1": 1174, "r4": 1571},
}

CROPS = [
    # --- Griblje ×12: trakovi (polna širina, yc±90) ---
    ("griblje-zap3-marko-stavar-75", 75, 100, YC[75]["z3"] - 90, 2450, YC[75]["z3"] + 90, 2.2),
    ("griblje-zap8-marija-urh-75", 75, 100, YC[75]["z8"] - 90, 2450, YC[75]["z8"] + 90, 2.2),
    ("griblje-zap9-barbara-povsek-76", 76, 100, YC[76]["z9"] - 90, 2450, YC[76]["z9"] + 90, 2.2),
    ("griblje-zap10-marija-brodaric-76", 76, 100, YC[76]["z10"] - 90, 2450, YC[76]["z10"] + 90, 2.2),
    ("griblje-zap14-jurij-pezdirec-76", 76, 100, YC[76]["z14"] - 90, 2450, YC[76]["z14"] + 90, 2.2),
    ("griblje-zap16-marija-skavc-76", 76, 100, YC[76]["z16"] - 90, 2450, YC[76]["z16"] + 90, 2.2),
    ("griblje-zap21-alzbeta-hlec-77", 77, 100, YC[77]["z21"] - 90, 2450, YC[77]["z21"] + 90, 2.2),
    ("griblje-zap34-martin-capuc-78", 78, 100, YC[78]["z34"] - 90, 2450, YC[78]["z34"] + 90, 2.2),
    ("griblje-zap38-joze-hrizan-78", 78, 100, YC[78]["z38"] - 90, 2450, YC[78]["z38"] + 90, 2.2),
    ("griblje-zap40-marija-mihelj-78", 78, 100, YC[78]["z40"] - 90, 2450, YC[78]["z40"] + 90, 2.2),
    ("griblje-zap50-peter-brinec-79", 79, 100, YC[79]["z50"] - 90, 2450, YC[79]["z50"] + 90, 2.2),
    ("griblje-zap59-marija-hlobucar-80", 80, 100, YC[80]["z59"] - 90, 2450, YC[80]["z59"] + 90, 2.2),
    # --- meja 1899/1900 (s75) + meja 1900/01 (s80) ---
    ("meja-1899-1900-zap60-mrtvorojen", 75, 100, YC[75]["z60"] - 90, 2450, YC[75]["z60"] + 90, 2.2),
    ("meja-1899-1900-marker-1900", 75, 100, YC[75]["mk"] - 90, 2450, YC[75]["mk"] + 90, 2.2),
    ("meja-1899-1900-zap1-prvi-1900", 75, 100, YC[75]["z1"] - 90, 2450, YC[75]["z1"] + 90, 2.2),
    ("meja-1900-01-zap61-zadnji-1900", 80, 100, YC[80]["z61"] - 90, 2450, YC[80]["z61"] + 90, 2.2),
    ("meja-1900-01-marker-1901", 80, 100, YC[80]["mk"] - 90, 2450, YC[80]["mk"] + 90, 2.2),
    ("meja-1900-01-zap1-prvi-1901", 80, 100, YC[80]["r1"] - 90, 2450, YC[80]["r1"] + 90, 2.2),
    # --- celice ×3.0: sporna imena / hišne / meseci ---
    ("s75-zap3-vas-hisna", 75, 520, YC[75]["z3"] - 85, 900, YC[75]["z3"] + 85, 3.0),
    ("s75-zap3-ime", 75, 860, YC[75]["z3"] - 85, 1400, YC[75]["z3"] + 85, 3.0),
    ("s75-zap8-vas-hisna", 75, 520, YC[75]["z8"] - 85, 900, YC[75]["z8"] + 85, 3.0),
    ("s75-zap8-ime", 75, 860, YC[75]["z8"] - 85, 1400, YC[75]["z8"] + 85, 3.0),
    ("s75-zap1-bolezen", 75, 1770, YC[75]["z1"] - 85, 2200, YC[75]["z1"] + 85, 3.0),
    ("s76-zap9-vas-hisna", 76, 520, YC[76]["z9"] - 85, 900, YC[76]["z9"] + 85, 3.0),
    ("s76-zap10-vas-hisna", 76, 520, YC[76]["z10"] - 85, 900, YC[76]["z10"] + 85, 3.0),
    ("s76-zap14-vas-hisna", 76, 520, YC[76]["z14"] - 85, 900, YC[76]["z14"] + 85, 3.0),
    ("s76-zap16-vas-hisna", 76, 520, YC[76]["z16"] - 85, 900, YC[76]["z16"] + 85, 3.0),
    ("s77-zap21-vas-hisna", 77, 520, YC[77]["z21"] - 85, 900, YC[77]["z21"] + 85, 3.0),
    ("s78-zap34-vas-hisna", 78, 520, YC[78]["z34"] - 85, 900, YC[78]["z34"] + 85, 3.0),
    ("s78-zap34-ime", 78, 860, YC[78]["z34"] - 85, 1400, YC[78]["z34"] + 85, 3.0),
    ("s78-zap38-vas-hisna", 78, 520, YC[78]["z38"] - 85, 900, YC[78]["z38"] + 85, 3.0),
    ("s78-zap38-ime-bolezen", 78, 860, YC[78]["z38"] - 85, 2100, YC[78]["z38"] + 85, 2.6),
    ("s78-zap40-vas-hisna", 78, 520, YC[78]["z40"] - 85, 900, YC[78]["z40"] + 85, 3.0),
    ("s78-zap40-ime", 78, 860, YC[78]["z40"] - 85, 1400, YC[78]["z40"] + 85, 3.0),
    ("s79-zap50-vas-hisna", 79, 520, YC[79]["z50"] - 85, 900, YC[79]["z50"] + 85, 3.0),
    ("s79-zap50-ime", 79, 860, YC[79]["z50"] - 85, 1400, YC[79]["z50"] + 85, 3.0),
    ("s80-zap59-vas-hisna", 80, 520, YC[80]["z59"] - 85, 900, YC[80]["z59"] + 85, 3.0),
    ("s80-zap59-ime", 80, 860, YC[80]["z59"] - 85, 1400, YC[80]["z59"] + 85, 3.0),
    # --- duhovnik J.R. Kut'nek (NOVI #10-kandidat!) ---
    ("s79-zap49-podpis-kutnek", 79, 2080, YC[79]["z49"] - 85, 2470, YC[79]["z49"] + 85, 3.0),
    ("s79-zap50-podpis-kutnek", 79, 2080, YC[79]["z50"] - 85, 2470, YC[79]["z50"] + 85, 3.0),
    ("s80-zap57-podpis-kutnek", 80, 2080, YC[80]["z57"] - 85, 2470, YC[80]["z57"] + 85, 3.0),
    ("s80-zap59-podpis-kutnek", 80, 2080, YC[80]["z59"] - 85, 2470, YC[80]["z59"] + 85, 3.0),
    ("s78-zap41-podpis-perz", 78, 2080, YC[78]["z41"] - 85, 2470, YC[78]["z41"] + 85, 3.0),
    ("s79-zap45-podpis-rauq-perz", 79, 2080, YC[79]["z45"] - 85, 2470, YC[79]["z45"] + 85, 3.0),
    # --- P167-lead: Griblje-1901 (s80 dno) ---
    ("s80-r1-griblje36-ana-krizan", 80, 520, YC[80]["r1"] - 85, 1400, YC[80]["r1"] + 85, 2.6),
    ("s80-r4-griblje-matija-hlobucar", 80, 520, YC[80]["r4"] - 85, 1400, YC[80]["r4"] + 85, 2.6),
]


def main():
    for (name, scan, x0, y0, x1, y1, zoom) in CROPS:
        im = Image.open(f"/tmp/p166/s{scan:02d}.jpg")
        c = im.crop((x0, max(0, y0), x1, min(im.size[1], y1)))
        c = c.resize((int(c.size[0] * zoom), int(c.size[1] * zoom)), Image.LANCZOS)
        c.save(f"{OUT}/{name}.png")
    print(f"crops: {len(CROPS)} shranjenih")


if __name__ == "__main__":
    main()
