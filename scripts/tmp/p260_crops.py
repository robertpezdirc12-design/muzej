#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P260 — kropsi s14 (Pag. 25/26) za mikro-forenziko: datumi, marginale, hišne številke."""
import os
from PIL import Image

OUT = "/tmp/p260"
img = Image.open(f"{OUT}/s14.jpg")
W, H = img.size
print("s14 size:", W, H)

os.makedirs(f"{OUT}/crops", exist_ok=True)

def crop(name, box, scale=3):
    c = img.crop(box)
    c = c.resize((c.width * scale, c.height * scale), Image.LANCZOS)
    c.save(f"{OUT}/crops/{name}.png")
    print(name, box, "->", c.size)

# levi rob + datumski stolpec (celotna višina tabele)
crop("s14_dates", (60, 150, 260, H - 60), 2)
# Bräutigam: Wohnort + Ime (levo stran)
crop("s14_grooms_L", (260, 150, 560, H - 60), 2)
crop("s14_grooms_house", (340, 150, 470, H - 60), 3)
# Braut: Wohnort + Ime
crop("s14_brides", (610, 150, 800, H - 60), 2)
# vrstice 1–2 (margine 19/20) polna višina
crop("s14_r1_r2", (60, 150, W // 2 + 10, 420), 2)
# vrstica 3 (margin 1) + vrstica 4 (margin 2) — datumi + imena
crop("s14_r3_r4", (60, 400, W // 2 + 10, 660), 2)
# desna stran vrstice 4–5 (1835 potrditev + urkunden)
crop("s14_r4_r5_R", (W // 2 - 20, 400, W - 30, 700), 2)
# foliacija svinčnik zgoraj
crop("s14_folio", (40, 30, 200, 110), 3)
crop("s14_folio_R", (W - 200, 30, W - 40, 110), 3)
# podpis duhovnika (r1–r3)
crop("s14_priest_1_3", (W - 240, 150, W - 20, 500), 2)
print("DONE")
