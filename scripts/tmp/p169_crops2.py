#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P169 — re-crops z PRAVILNIMI x-rangei (x-check-lekcija: starost
@ 1530–1770, bolezen @ 1755–2100, previden @ 1950–2090!) + super-zoomi
za hisna/ime-konflikte. Izhod: /tmp/p169/crops/*.png (dodaten set)."""
from PIL import Image
import os

OUT = "/tmp/p169/crops"
os.makedirs(OUT, exist_ok=True)

S90 = {"r1": 1072, "r3": 1347, "r4": 1484}
S91 = {"z8": 396, "z10": 672, "z12": 941, "z13": 1079, "z14": 1216,
       "z16": 1493, "z19": 1904}
S92 = {"z22": 671, "z30": 1750}
S93 = {"z38": 1208, "z41": 1608, "z42": 1744}
S94 = {"z48": 915, "z50": 1182}

GRIBLJE = [
    ("s90-r1", 90, S90["r1"]), ("s90-r3", 90, S90["r3"]),
    ("s90-r4", 90, S90["r4"]), ("s91-z8", 91, S91["z8"]),
    ("s91-z10", 91, S91["z10"]), ("s91-z12", 91, S91["z12"]),
    ("s91-z13", 91, S91["z13"]), ("s91-z14", 91, S91["z14"]),
    ("s91-z16", 91, S91["z16"]), ("s91-z19", 91, S91["z19"]),
    ("s92-z22", 92, S92["z22"]), ("s92-z30", 92, S92["z30"]),
    ("s93-z38", 93, S93["z38"]), ("s93-z41", 93, S93["z41"]),
    ("s93-z42", 93, S93["z42"]), ("s94-z48", 94, S94["z48"]),
    ("s94-z50", 94, S94["z50"]),
]

ST_X = (1530, 1770)   # starost (PRAVILNO!)
B_X = (1755, 2100)    # bolezen
H_X = (430, 700)      # hišna št. super-zoom (ozek)
IM_X = (850, 1450)    # ime super-zoom


def crop(name, scan, x0, x1, yc, half, zoom):
    im = Image.open(f"/tmp/p169/s{scan:02d}.jpg")
    c = im.crop((x0, max(0, yc - half), x1, min(im.size[1], yc + half)))
    c = c.resize((int(c.size[0] * zoom), int(c.size[1] * zoom)), Image.LANCZOS)
    c.save(f"{OUT}/{name}.png")
    return c.size


def main():
    n = 0
    # starost-re + bolezen za vseh 17 Griblje (×3.0)
    for (nm, s, yc) in GRIBLJE:
        crop(f"re-{nm}-starost", s, *ST_X, yc, 80, 3.0); n += 1
        crop(f"re-{nm}-bolezen", s, *B_X, yc, 80, 3.0); n += 1
    # SUPER-ZOOM ×6: hišne konflikte (zap48 83/85/33!) + ime-konflikti
    crop("sz-s94-z48-hisna-x6", 94, *H_X, S94["z48"], 70, 6.0); n += 1
    crop("sz-s90-r4-ime-x6", 90, *IM_X, S90["r4"], 70, 6.0); n += 1
    crop("sz-s91-z12-ime-x6", 91, *IM_X, S91["z12"], 70, 6.0); n += 1
    crop("sz-s93-z38-ime-x6", 93, *IM_X, S93["z38"], 70, 6.0); n += 1
    crop("sz-s93-z41-ime-x6", 93, *IM_X, S93["z41"], 70, 6.0); n += 1
    crop("sz-s94-z48-ime-x6", 94, *IM_X, S94["z48"], 70, 6.0); n += 1
    crop("sz-s94-z50-ime-x6", 94, *IM_X, S94["z50"], 70, 6.0); n += 1
    crop("sz-s91-z19-hisna-x6", 91, *H_X, S91["z19"], 70, 6.0); n += 1
    crop("sz-s93-z38-hisna-x6", 93, *H_X, S93["z38"], 70, 6.0); n += 1
    crop("sz-s93-z42-hisna-x6", 93, *H_X, S93["z42"], 70, 6.0); n += 1
    crop("sz-s90-r1-starost-x6", 90, *ST_X, S90["r1"], 70, 6.0); n += 1
    crop("sz-s90-r3-starost-x6", 90, *ST_X, S90["r3"], 70, 6.0); n += 1
    print(f"re-crops: {n} shranjenih")


if __name__ == "__main__":
    main()
