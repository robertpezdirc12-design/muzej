#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P192 — forenzični izrezi v2 (kalibrirano z mrežami!)."""
from PIL import Image
import os

OUT = "/tmp/p192"
os.makedirs(f"{OUT}/crops2", exist_ok=True)

# (ime, sken, y0, y1, x0, x1, zoom) — None = celotna širina
TRAKT = [
    # --- 16 GRIBLJE-1885 ---
    ("g199-z4dup-dragot-h1",     "s199", 285, 395, None, None, 2.5),
    ("g199-z12-zuparic-h31",     "s199", 1045, 1145, None, None, 2.5),
    ("g200-z24-hojan-h62",       "s200", 950, 1045, None, None, 2.5),
    ("g201-z26-papic-h31-25j",   "s201", 260, 350, None, None, 2.5),
    ("g201-z29-papic-h31-19j",   "s201", 495, 580, None, None, 2.5),
    ("g202-z39-papric-witwe-h4", "s202", 250, 340, None, None, 2.5),
    ("g202-z43-stubler-h78",     "s202", 590, 680, None, None, 2.5),
    ("g203-z60-drogar-h5",       "s203", 865, 960, None, None, 2.5),
    ("g203-z61-kusic-h13",       "s203", 950, 1045, None, None, 2.5),
    ("g204-z64-simec-h54",       "s204", 515, 615, None, None, 2.5),
    ("g204-z66-prijzan-h63",     "s204", 695, 795, None, None, 2.5),
    ("g204-z68-poceh-h21",       "s204", 875, 975, None, None, 2.5),
    ("g205-z77-jakofcic-h9",     "s205", 695, 795, None, None, 2.5),
    ("g206-z83-poceh-h58",       "s206", 410, 505, None, None, 2.5),
    ("g206-z84-alth-h68",        "s206", 495, 590, None, None, 2.5),
    ("g206-z89-hrovatic-h63",    "s206", 840, 940, None, None, 2.5),
    # --- ANOMALIJE ---
    ("a198-meja-janner-1885",    "s198", 875, 1290, None, None, 1.8),
    ("a203-z53-mai-prazno",      "s203", 325, 425, None, None, 2.5),
    ("a203-z62-precrtan",        "s203", 1035, 1160, None, None, 2.2),
    ("a203-glava-jahr-18",       "s203", 130, 200, 120, 800, 2.8),
    ("a204-dual-numbering",      "s204", 225, 800, 90, 215, 1.6),
    ("a205-glava-jahr-18",       "s205", 120, 200, 120, 800, 2.8),
    ("a205-desni-slovenske-glave","s205", 50, 220, 780, 1500, 2.2),
    ("a206-glava-mrtvaska",      "s206", 45, 185, None, None, 2.0),
    ("a206-z81-precrtan",        "s206", 210, 315, None, None, 2.5),
    ("a199-glava-jahr-1885",     "s199", 150, 300, None, None, 2.2),
    ("a200-glava-1885",          "s200", 170, 260, None, None, 2.5),
    ("a201-glava-1885",          "s201", 125, 230, None, None, 2.5),
    ("a202-z40-compound-vas",    "s202", 330, 430, None, None, 2.5),
    ("a202-z49-z50-meseci",      "s202", 985, 1160, 90, 700, 2.5),
    ("a207-konec-z92-z93",       "s207", 175, 370, None, None, 2.2),
    ("a198-z71-jalencic-h8",     "s198", 395, 490, None, None, 2.5),
    ("a198-z76-huzic-h10",       "s198", 795, 890, None, None, 2.5),
]

for name, scan, y0, y1, x0, x1, zoom in TRAKT:
    im = Image.open(f"{OUT}/{scan}.jpg")
    w, h = im.size
    if x0 is None: x0 = 0
    if x1 is None: x1 = w
    crop = im.crop((x0, max(0, y0), min(w, x1), min(h, y1)))
    nw, nh = int(crop.width * zoom), int(crop.height * zoom)
    crop = crop.resize((nw, nh), Image.LANCZOS)
    crop.save(f"{OUT}/crops2/{name}.png")
    print(f"{name}: {nw}x{nh}")

print(f"\nSKUPAJ: {len(TRAKT)}")
