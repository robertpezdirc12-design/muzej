#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P259-ALT — stack generator: L+R polovici vrstice (2x vertikalna povecava),
ena slika na vrstico za branje z agentovo vizijo (Read tool).
L = leva stran razprtega lista (x 0-1060), R = desna (x 1057-konec).
Izhod: /tmp/p259/stacks/{tag}_r{i}.jpg (~1060 x 4*h)"""
import os, sys
from PIL import Image

SRC = "/tmp/p259/full"
OUT = "/tmp/p259/stacks"; os.makedirs(OUT, exist_ok=True)
MID = 1058  # zareza levo/desno (prekrivanje 3px)

JOBS = [("s11", 13), ("s12", 12), ("s13", 11)]

only = sys.argv[1:] if len(sys.argv) > 1 and sys.argv[1] != "all" else None

for tag, n in JOBS:
    for i in range(1, n + 1):
        rid = f"{tag}_r{i}"
        if only and rid not in only:
            continue
        src = f"{SRC}/{rid}.jpg"
        if not os.path.exists(src):
            print(f"{rid}: MANJKA"); continue
        im = Image.open(src)
        W, H = im.size
        L = im.crop((0, 0, MID, H))
        R = im.crop((MID, 0, W, H))
        L = L.resize((MID, H * 2), Image.LANCZOS)
        R = R.resize((W - MID, H * 2), Image.LANCZOS)
        canvas = Image.new("RGB", (MID, H * 4), (20, 20, 20))
        canvas.paste(L, (0, 0))
        canvas.paste(R, (0, H * 2))
        canvas.save(f"{OUT}/{rid}.jpg", quality=92)
        print(f"{rid}: {canvas.size}")
