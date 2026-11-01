#!/usr/bin/env python3
"""P173 re-crops — kalibrirani pasovi za s109 (start 420/step 150) + posebni primeri."""
import os
from PIL import Image

DIR = "/tmp/p173"
OUT = os.path.join(DIR, "crops")

X = dict(mesec=(260, 440), smrt=(290, 430), pokop=(430, 580), datumi=(260, 580),
         vas=(580, 800), hisna=(770, 950), ime=(880, 1450), star=(1500, 1750),
         bolez=(1700, 2120), podpis=(2160, 2500))

def crop_band(scan, y0, y1, cols, label, scale=3.0):
    im = Image.open(f"{DIR}/s{scan}.jpg")
    for col in cols:
        x0, x1 = X[col]
        c = im.crop((x0, max(0, y0), min(im.width, x1), min(im.height, y1)))
        c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS)
        c.save(f"{OUT}/{label}-{col}.png")

# s109: merjene vrstice (z1@~420, step ~150)
S109 = {1: 420, 2: 570, 3: 720, 4: 865, 5: 1010, 6: 1155, 7: 1300, 8: 1450,
        9: 1600, 10: 1745, 11: 1890}
for z, y in S109.items():
    if z in (1, 2, 4, 5, 9, 11):
        cols = ["ime"]
        if z in (1, 4, 9, 11): cols.append("bolez" if z != 9 else "bolez")
        if z == 4: cols.append("star")
        if z == 1: cols.append("podpis")
        if z == 9: cols.append("podpis")
        if z == 11: cols.append("bolez")
        crop_band(109, y - 15, y + 160, cols, f"R109-z{z}")

# s110-z18: širši datumi (29-Feb vprašanje)
crop_band(110, 330 + 6 * 135 - 25, 330 + 7 * 135 + 25, ["datumi", "ime"], "R110-z18", scale=3.0)

# s113-z59: širši datumi (2.→14.?)
crop_band(113, 330 + 11 * 135 - 15, 330 + 12 * 135 + 15, ["datumi"], "R113-z59")

# s112-z37: širša bolezen (?led opeklin)
crop_band(112, 330 + 1 * 135 - 12, 330 + 2 * 135 + 12, ["bolez"], "R112-z37")

# 1906-primerjava: s104-z1 (Ana BRINEC/BRODARIČ?!) — višji pas ker velika-1906
im = Image.open("/tmp/p172/s104.jpg")
c = im.crop((880, 280, 1500, 560))
c = c.resize((int(c.width * 2.5), int(c.height * 2.5)), Image.LANCZOS)
c.save(f"{OUT}/CMP-1906-s104-z1-ime.png")

# s112-z46 podpis (Lilek-formula)
crop_band(112, 330 + 10 * 135 - 15, 330 + 11 * 135 + 15, ["podpis"], "R112-z46")

# s114 velika-1908 meja-crop
im = Image.open(f"{DIR}/s114.jpg")
c = im.crop((150, 1580, 900, 1780))
c = c.resize((int(c.width * 2.5), int(c.height * 2.5)), Image.LANCZOS)
c.save(f"{OUT}/CMP-s114-velika-1908.png")

print("re-crops OK")
