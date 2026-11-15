#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P261 — izrezi s17 POPRAVLJENE y-koordinate (kalibracija po margin-stolpcu)."""
from PIL import Image
import os

SRC = "research/issue17/p261-work/s17.jpg"
OUT = "/tmp/p261"
os.makedirs(OUT, exist_ok=True)
im = Image.open(SRC)
W, H = im.size  # 2139 x 1500

# kalibracija: margin-crop (140-910) je pokazal header ~140-280 + 9 vrstic ~75-90px
rows = {
    "r14_m14": (272, 372),
    "r15_m15": (372, 468),
    "r16_m16": (468, 552),
    "r17_m17": (552, 632),
    "r18_m1": (632, 708),
    "r19_m2": (708, 782),
    "r20_m3": (782, 856),
    "r21_m4": (856, 932),
    "r22_m5": (932, 1014),
}
for name, (y0, y1) in rows.items():
    # L del: margina+datum+Wohnort+HausNr+ženin(ime,religija,starost,stan) do x~1080
    im.crop((80, y0, 1090, y1)).resize((2020, (y1 - y0) * 2), Image.LANCZOS).save(f"{OUT}/s17_{name}_L.png")
    # R del: nevesta + starši + priče + duhovnik (x~1030-2100)
    im.crop((1030, y0, 2100, y1)).resize((2140, (y1 - y0) * 2), Image.LANCZOS).save(f"{OUT}/s17_{name}_R.png")
print("OK", len(rows) * 2)
