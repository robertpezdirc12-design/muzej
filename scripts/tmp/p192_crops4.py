#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P192 — izrezi v4: 3-vrstični pasovi (300px) + name-celice ×3.5."""
from PIL import Image
import os

OUT = "/tmp/p192"
os.makedirs(f"{OUT}/crops4", exist_ok=True)

BANDS = [
    ("b201-z28z29z30",   "s201", 480, 780),
    ("b202-z42z43z44",   "s202", 640, 940),
    ("b203-z59z60z61",   "s203", 940, 1240),
    ("b204-z63z64z65",   "s204", 480, 780),
    ("b204-z65z66z67",   "s204", 640, 940),
    ("b204-z67z68z69",   "s204", 800, 1100),
    ("b205-z76z77z78",   "s205", 620, 920),
    ("b206-z82z83z84",   "s206", 340, 640),
    ("b206-z88z89z90",   "s206", 770, 1070),
]
for name, scan, y0, y1 in BANDS:
    im = Image.open(f"{OUT}/{scan}.jpg")
    w, h = im.size
    crop = im.crop((0, y0, w, min(h, y1)))
    zoom = 2.2
    crop = crop.resize((int(crop.width * zoom), int(crop.height * zoom)), Image.LANCZOS)
    crop.save(f"{OUT}/crops4/{name}.png")
    print(f"{name}: {crop.width}x{crop.height}")

CELLS = [
    ("n-z24-hojan",   "s200", 540, 840, 1115, 1245),
    ("n-z26-papic",   "s201", 540, 840, 285, 400),
    ("n-z29-papic",   "s201", 540, 840, 545, 675),
    ("n-z39-papric",  "s202", 540, 840, 265, 400),
    ("n-z61-kusic",   "s203", 540, 840, 985, 1115),
    ("n-z64-simec",   "s204", 540, 840, 545, 675),
    ("n-z66-prijzan", "s204", 540, 840, 715, 845),
    ("n-z68-poceh",   "s204", 540, 840, 900, 1030),
    ("n-z77-h9",      "s205", 540, 840, 725, 855),
    ("n-z83-h58",     "s206", 540, 840, 445, 575),
    ("n-z84-h68",     "s206", 540, 840, 535, 665),
    ("n-z89-h63",     "s206", 540, 840, 875, 1005),
]
for name, scan, x0, x1, y0, y1 in CELLS:
    im = Image.open(f"{OUT}/{scan}.jpg")
    crop = im.crop((x0, y0, x1, y1))
    zoom = 3.5
    crop = crop.resize((int(crop.width * zoom), int(crop.height * zoom)), Image.LANCZOS)
    crop.save(f"{OUT}/crops4/{name}.png")
    print(f"{name}: {crop.width}x{crop.height}")
