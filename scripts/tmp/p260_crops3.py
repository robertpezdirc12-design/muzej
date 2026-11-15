#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P260 — mikro-kropsi s15 (Griblje 4/6) + s16 (datumski stolpec + m4/m5/m6/m7)."""
import os
from PIL import Image

OUT = "/tmp/p260"
os.makedirs(f"{OUT}/crops", exist_ok=True)

def crop(name, path, box, scale=4):
    img = Image.open(path)
    c = img.crop(box)
    c = c.resize((c.width * scale, c.height * scale), Image.LANCZOS)
    c.save(f"{OUT}/crops/{name}.png")
    print(name, box, "->", c.size)

s15 = f"{OUT}/s15.jpg"
s16 = f"{OUT}/s16.jpg"

# s15: datumski stolpec (vrstice m14/m15 — 1. März + 28. Juli) + nevesta Wohnort (Grübl 4/6)
crop("s15_dates", s15, (60, 150, 280, 1500), 2)
crop("s15_bride_w14_15", s15, (590, 480, 780, 720), 4)
crop("s15_m14_names", s15, (60, 480, 800, 620), 2)
crop("s15_m15_names", s15, (60, 580, 800, 720), 2)

# s16: datumski stolpec celoten
crop("s16_dates", s16, (55, 150, 280, 1500), 2)
# s16 m4 (r1): ženin + nevesta (Grübl dv?)
crop("s16_m4", s16, (55, 190, 810, 330), 2)
# s16 m5 (r2): nevesta Grüling 25?
crop("s16_m5", s16, (55, 300, 810, 440), 2)
# s16 m6 (r3): POLNI DVOJNI h9 × h63
crop("s16_m6", s16, (55, 410, 810, 560), 2)
# s16 m7 (r4): IZMENA-VLOG h63 × h9
crop("s16_m7", s16, (55, 525, 810, 670), 2)
print("DONE")
