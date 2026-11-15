#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P262 — s18 datum-celice mega-zoom (x=90–460, na vrstico) + margin-celica."""
import subprocess
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = f"{ROOT}/research/issue17/p261-work/s18.jpg"
OUT = f"{ROOT}/research/issue17/p262-work"

rows = {1: (255, 425), 2: (415, 575), 3: (565, 725), 4: (715, 880), 5: (870, 1035), 6: (1025, 1185), 7: (1175, 1340)}

for r, (y0, y1) in rows.items():
    subprocess.run(["python3", "-c",
        f"from PIL import Image; im=Image.open('{SRC}'); "
        f"c=im.crop((90,{y0},470,{y1})); c.resize((int(c.width*3.2),int(c.height*3.2)),Image.LANCZOS).save('{OUT}/date{r}_big.png')"], check=True)

print("date zooms OK")
