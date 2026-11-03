#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P195 — forenzični izrezi MRLIŠKE PREDZGODOVINE 04106, leto 1882 (skeni 180–186).
yc = vizualno-prebrane z Read-očmi (28 kvadrantov prebranih!).
Izhod: /tmp/p195/crops/*.png"""
from PIL import Image
import os

OUT = "/tmp/p195"
os.makedirs(f"{OUT}/crops", exist_ok=True)

# (ime, sken, y0, y1, x0, x1, zoom)  — None = privzeto celotna širina
TRAKT = [
    # --- GRIBLJE-1882 (celotne vrstice čez obe strani!) ---
    ("g180-z2-pezdirc-h20",         "s180", 430, 545, None, None, 2.5),
    ("g181-z14-zelsko-h1",          "s181", 240, 345, None, None, 2.5),
    ("g181-z15-krizan-h3",          "s181", 340, 445, None, None, 2.5),
    ("g181-z17-simec-wittwe-h54",   "s181", 540, 645, None, None, 2.5),
    ("g181-z18-terdic-h69",         "s181", 640, 745, None, None, 2.5),
    ("g182-z24-lupanic-h73",        "s182", 560, 670, None, None, 2.5),
    ("g183-z32-zelsko-h1",          "s183", 480, 590, None, None, 2.5),
    ("g183-z33-jakofcic-h8",        "s183", 585, 690, None, None, 2.5),
    ("g183-z35-husic-h29",          "s183", 790, 900, None, None, 2.5),
    ("g183-z37-mravinec-h10",       "s183", 990, 1100, None, None, 2.5),
    ("g184-z38-simec-h54",          "s184", 230, 340, None, None, 2.5),
    ("g184-z43-milek-h65",          "s184", 490, 600, None, None, 2.5),
    ("g184-z44-simec-h55",          "s184", 595, 705, None, None, 2.5),
    ("g184-z46-mrh-urh-h68",        "s184", 800, 915, None, None, 2.5),
    ("g185-z56-jakofcic-h13",       "s185", 655, 765, None, None, 2.5),
    ("g185-z58-peclir-h50",         "s185", 965, 1075, None, None, 2.5),
    ("g186-z59-dragos-tail",        "s186", 155, 275, None, None, 2.5),
    # --- ANOMALIJE ---
    ("a180-glava-1882",             "s180", 90, 400, None, None, 1.6),
    ("a181-z11-jaklsa-muhlzugler",  "s181", 240, 350, 640, 1400, 3.0),
    ("a182-z25-ulcer-opomba",       "s182", 745, 1035, 590, 1500, 2.2),
    ("a182-z21-gradac64-kovac",     "s182", 240, 355, None, None, 2.5),
    ("a182-z29-maffenfucht",        "s182", 810, 940, 880, 1560, 3.2),
    ("a183-z34-maffenocht",         "s183", 285, 400, 880, 1560, 3.2),
    ("a183-z35-maffenrift",         "s183", 830, 960, 880, 1560, 3.2),
    ("a183-z36-klemencic-opomba",   "s183", 900, 1035, 590, 1560, 2.5),
    ("a184-z40-fabrik-husic",       "s184", 450, 560, None, None, 2.5),
    ("a184-z46-vrstica",            "s184", 800, 915, 700, 2050, 2.8),
    ("a185-z50-todtgeboren",        "s185", 640, 770, None, None, 2.5),
    ("a185-z52-hrast-tome",         "s185", 770, 890, None, None, 2.5),
    ("a185-z53-whare-vrizan",       "s185", 885, 1000, None, None, 2.5),
    ("a185-z57-stanadinic",         "s185", 860, 975, 590, 1560, 2.8),
    ("a185-asthma-par-z48-z49",     "s185", 340, 560, 880, 1560, 2.6),
    ("a185-davica-z51-z53",         "s185", 545, 700, 880, 1560, 2.6),
    ("a186-meja-1882-83",           "s186", 130, 400, None, None, 1.8),
    ("a180-duhovnik-jancar-pfr",    "s180", 430, 560, 1370, 1990, 3.0),
    ("a182-z27-priest-pfarrer",     "s182", 575, 700, 1370, 1990, 3.0),
    ("a185-z58-priest-rcpfarr",     "s185", 965, 1090, 1370, 1990, 3.0),
    ("a185-z48-49-pust-abl",        "s185", 340, 480, 590, 1100, 3.0),
]

for name, scan, y0, y1, x0, x1, zoom in TRAKT:
    im = Image.open(f"{OUT}/{scan}.jpg")
    w, h = im.size
    if x0 is None: x0 = 0
    if x1 is None: x1 = w
    crop = im.crop((x0, max(0, y0), min(w, x1), min(h, y1)))
    crop = crop.resize((int(crop.width * zoom), int(crop.height * zoom)), Image.LANCZOS)
    crop.save(f"{OUT}/crops/{name}.png")
print(f"crops: {len(TRAKT)} OK")
