#!/usr/bin/env python3
"""P173 crops v2 — popravljen bug (vsak stolpec svoje ime) + kalibracija."""
import os
from PIL import Image

DIR = "/tmp/p173"
OUT = os.path.join(DIR, "crops")
os.makedirs(OUT, exist_ok=True)

# kalibracija: celotna vrstica z57 s113 (hišna + ime), scale 1.0
im = Image.open(f"{DIR}/s113.jpg")
y0, y1 = 330 + 9 * 135 - 10, 330 + 10 * 135 + 10
strip = im.crop((0, y0, im.width, y1))
strip.save(f"{OUT}/KALIBRACIJA-s113-z57-fullrow.png")
print("kalibracija shranjena:", strip.size)
