#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P192 — forenzični izrezi MRLIŠKE PREDHODNICE 04106, leto 1885 (skeni 198–207).
16 Griblje-1885 trakovi ×2.5 + anomalije (meja, glave, dual-numbering, prečrtani,
slovenski-obrazec, compound-vas) + 2 Griblje-1884 kontekst.
yc = vizualno-prebrane z Read-očmi (8 strani prebranih!).
Izhod: /tmp/p192/crops/*.png"""
from PIL import Image
import os

OUT = "/tmp/p192"
os.makedirs(f"{OUT}/crops", exist_ok=True)

# (ime, sken, y0, y1, x0, x1, zoom)  — None = privzeto celotna širina
TRAKT = [
    # --- 16 GRIBLJE-1885 (celotne vrstice čez obe strani!) ---
    ("g199-z4dup-dragot-h1",        "s199", 240, 350, None, None, 2.5),
    ("g199-z12-zuparic-h31",        "s199", 890, 990, None, None, 2.5),
    ("g200-z24-hojan-h62",          "s200", 950, 1045, None, None, 2.5),
    ("g201-z26-papic-h31-25j",      "s201", 240, 340, None, None, 2.5),
    ("g201-z29-papic-h31-19j",      "s201", 490, 585, None, None, 2.5),
    ("g202-z39-papric-witwe-h4",    "s202", 235, 345, None, None, 2.5),
    ("g202-z43-stubler-h78",        "s202", 555, 650, None, None, 2.5),
    ("g203-z60-drogar-h5",          "s203", 845, 945, None, None, 2.5),
    ("g203-z61-kusic-h13",          "s203", 930, 1025, None, None, 2.5),
    ("g204-z64-simec-h54",          "s204", 455, 550, None, None, 2.5),
    ("g204-z66-prijzan-h63",        "s204", 610, 705, None, None, 2.5),
    ("g204-z68-poceh-h21",          "s204", 765, 860, None, None, 2.5),
    ("g205-z77-jakofcic-h9",        "s205", 605, 700, None, None, 2.5),
    ("g206-z83-poceh-h58",          "s206", 355, 450, None, None, 2.5),
    ("g206-z84-alth-h68",           "s206", 435, 530, None, None, 2.5),
    ("g206-z89-hrovatic-h63",       "s206", 830, 925, None, None, 2.5),
    # --- ANOMALIJE / KONTEKST ---
    ("a198-meja-janner-1885",       "s198", 875, 1290, None, None, 1.8),
    ("a198-z71-jalencic-h8-1884",   "s198", 395, 490, None, None, 2.5),
    ("a198-z76-huzic-h10-1884",     "s198", 795, 890, None, None, 2.5),
    ("a199-glava-jahr-1885",        "s199", 125, 260, None, None, 2.2),
    ("a200-glava-1885-garble",      "s200", 155, 250, None, None, 2.5),
    ("a201-glava-1885",             "s201", 130, 230, None, None, 2.5),
    ("a202-z40-compound-vas-certoviše-od-griblje", "s202", 320, 425, None, None, 2.5),
    ("a202-z49-z50-meseci",         "s202", 960, 1130, 90, 700, 2.5),
    ("a203-glava-jahr-18-nepopolna","s203", 120, 205, None, None, 2.5),
    ("a203-z53-mai-prazno-starost", "s203", 305, 400, None, None, 2.5),
    ("a203-z62-precrtan-podzemelj", "s203", 1005, 1140, None, None, 2.2),
    ("a204-dual-numbering-margin",  "s204", 225, 1115, 90, 215, 1.6),
    ("a205-glava-jahr-18",          "s205", 115, 205, None, None, 2.5),
    ("a205-desni-slovenske-glave",  "s205", 50, 220, 780, 1500, 2.2),
    ("a206-glava-mrtvaska-knjiga",  "s206", 45, 185, None, None, 2.0),
    ("a206-z81-precrtan-gemisce",   "s206", 170, 290, None, None, 2.5),
    ("a207-konec-z92-z93",          "s207", 175, 370, None, None, 2.2),
]

W_DEFAULT = None

for name, scan, y0, y1, x0, x1, zoom in TRAKT:
    im = Image.open(f"{OUT}/{scan}.jpg")
    w, h = im.size
    if x0 is None: x0 = 0
    if x1 is None: x1 = w
    crop = im.crop((x0, max(0, y0), min(w, x1), min(h, y1)))
    nw, nh = int(crop.width * zoom), int(crop.height * zoom)
    crop = crop.resize((nw, nh), Image.LANCZOS)
    crop.save(f"{OUT}/crops/{name}.png")
    print(f"{name}: {nw}x{nh}")

print(f"\nSKUPAJ: {len(TRAKT)} izrezov")
