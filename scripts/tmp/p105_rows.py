#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P105 forenzični izrezi Griblje vrstic 1910 — levi (kraj/hiša/ime) + desni (roditelja/botra/babica/podpis)."""
import os
from PIL import Image

OUT = "/tmp/p105/read"

# (sken, ime, y0, y1)
ROWS = [
    (211, "r03", 855, 970),
    (211, "r07", 1175, 1350),
    (212, "r10", 370, 485),
    (212, "r18", 1180, 1300),
    (213, "r22", 385, 480),
    (213, "r26", 825, 930),
    (214, "r32", 185, 285),
    (214, "r33", 275, 395),
    (214, "r39", 920, 1025),
    (214, "r42", 1195, 1300),
    (214, "r43", 1290, 1405),
    (215, "r47", 470, 580),
    (215, "r48", 570, 655),
    (215, "r54", 1195, 1300),
    (216, "r64", 1015, 1115),
    (216, "r66", 1195, 1300),
    (216, "r67", 1290, 1405),
    (218, "r72", 570, 655),
    (218, "r78", 1195, 1300),
    (218, "r79", 1290, 1405),
    (219, "r83", 470, 580),
    (219, "r84", 570, 655),
]

for scan, ime, y0, y1 in ROWS:
    im = Image.open(f"/tmp/p105/scan-{scan:02d}.jpg")
    # levi del: kraj + hiša + ime
    l = im.crop((150, y0, 1060, y1))
    l = l.resize((int(l.width * 3), int(l.height * 3)), Image.LANCZOS)
    l.save(f"{OUT}/{ime}-left.png")
    # desni del: roditelja + botra + babica + podpis
    r = im.crop((950, y0, 2038, y1))
    r = r.resize((int(r.width * 3), int(r.height * 3)), Image.LANCZOS)
    r.save(f"{OUT}/{ime}-right.png")
    print(ime, l.size, r.size)
