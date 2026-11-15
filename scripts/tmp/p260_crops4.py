#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P260 — maksimalni kropsi: datumi s16 (m4/m5/m6), m9-groom Wohnort, m6/m7 imena + priče."""
import os
from PIL import Image

OUT = "/tmp/p260"
os.makedirs(f"{OUT}/crops", exist_ok=True)

def crop(name, path, box, scale):
    img = Image.open(path)
    c = img.crop(box)
    c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS)
    c.save(f"{OUT}/crops/{name}.png")
    print(name, box, "->", c.size)

s16 = f"{OUT}/s16.jpg"

# datumi m4/m5 (27. Februar + 27. ibz) — max zoom
crop("s16_d_m4", s16, (70, 210, 210, 320), 6)
crop("s16_d_m5", s16, (70, 310, 210, 420), 6)
# datum m6 (10. ibz)
crop("s16_d_m6", s16, (70, 425, 210, 530), 6)
# m9 ženin Wohnort (g. Griblje 25 gebürtig?)
crop("s16_w9", s16, (160, 655, 400, 790), 5)
# m9 ženin ime + hišna
crop("s16_g9", s16, (330, 655, 560, 790), 5)
# m6 imena: ženin Peter Zahofzhig h9 + starši; nevesta Maria Krishan h63
crop("s16_n6", s16, (330, 425, 810, 560), 4)
# m7 imena: ženin Matthias Krishan h63 + starši; nevesta Anna Zahofzhig h9
crop("s16_n7", s16, (330, 530, 810, 670), 4)
print("DONE")
