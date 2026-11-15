#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P260 — mikro-kropsi s14: Wohnort + Haus-Nr (ženini) po vrsticah + neveste."""
import os
from PIL import Image

OUT = "/tmp/p260"
img = Image.open(f"{OUT}/s14.jpg")
W, H = img.size

os.makedirs(f"{OUT}/crops", exist_ok=True)

def crop(name, box, scale=4):
    c = img.crop(box)
    c = c.resize((c.width * scale, c.height * scale), Image.LANCZOS)
    c.save(f"{OUT}/crops/{name}.png")
    print(name, box, "->", c.size)

# y-središča vrstic (12 vrstic med ~190 in ~1420): iz dates-kropa je razporeditev ~101px
rows = [190, 295, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1310]
# Wohnort + Haus-Nr stolpca: x ~170–345 (Wohnort) — glej s14_dates (60–260) in grooms_L (260+)
for i, y in enumerate(rows):
    y0 = max(150, y - 45)
    y1 = min(H - 40, y + 70)
    crop(f"s14_w{i+1}", (150, y0, 420, y1), 4)

# neveste: ime+hišna (Braut del) — x ~610–800 za ime, hišna ~640?
crop("s14_bride_names", (610, 150, 830, H - 60), 2)
# Braut Haus-Nr stolpec — iskat med 600–700
crop("s14_bride_house", (580, 150, 700, H - 60), 3)
print("DONE")
