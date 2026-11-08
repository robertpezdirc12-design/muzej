#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P192 — izrezi v3: 2-vrstični pasovi (varnostni zamik ±70)."""
from PIL import Image
import os, sys

OUT = "/tmp/p192"
os.makedirs(f"{OUT}/crops3", exist_ok=True)

# (ime, sken, y0, y1, zoom)
BANDS = [
    ("g199-z4dup-dragot-h1",     "s199", 280, 400),
    ("g199-z12-zuparic-h31",     "s199", 1040, 1160),
    ("g200-z24-hojan-h62",       "s200", 1050, 1240),
    ("g201-z26-papic-h31-25j",   "s201", 255, 395),
    ("g201-z29-papic-h31-19j",   "s201", 500, 650),
    ("g202-z39-papric-witwe-h4", "s202", 240, 380),
    ("g202-z43-stubler-h78",     "s202", 540, 690),
    ("g203-z60-drogar-h5",       "s203", 850, 970),
    ("g203-z61-kusic-h13",       "s203", 945, 1060),
    ("g204-z64-simec-h54",       "s204", 505, 630),
    ("g204-z66-prijzan-h63",     "s204", 685, 805),
    ("g204-z68-poceh-h21",       "s204", 865, 985),
    ("g205-z77-jakofcic-h9",     "s205", 685, 805),
    ("g206-z83-poceh-h58",       "s206", 400, 520),
    ("g206-z84-alth-h68",        "s206", 490, 610),
    ("g206-z89-hrovatic-h63",    "s206", 830, 950),
]

for name, scan, y0, y1 in BANDS:
    im = Image.open(f"{OUT}/{scan}.jpg")
    w, h = im.size
    crop = im.crop((0, max(0, y0), w, min(h, y1)))
    zoom = 2.2
    nw, nh = int(crop.width * zoom), int(crop.height * zoom)
    crop = crop.resize((nw, nh), Image.LANCZOS)
    crop.save(f"{OUT}/crops3/{name}.png")
    print(f"{name}: {nw}x{nh}")
