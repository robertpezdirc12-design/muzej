#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P262 — s18 full-width per-row crops (L stran + R stran), 1.6x/1.8x."""
import subprocess
import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = f"{ROOT}/research/issue17/p261-work/s18.jpg"
OUT = f"{ROOT}/research/issue17/p262-work"

# 7 vrstic — meje iz grid črt (L stran; R stran ima iste višine približno)
rows = {1: (255, 425), 2: (415, 575), 3: (565, 725), 4: (715, 880), 5: (870, 1035), 6: (1025, 1185), 7: (1175, 1340)}

for r, (y0, y1) in rows.items():
    # L-stran celotna vrstica (margin → nevesta-konec)
    subprocess.run([sys.executable, "-c",
        f"from PIL import Image; im=Image.open('{SRC}'); "
        f"c=im.crop((80,{y0},1146,{y1})); c.resize((int(c.width*1.6),int(c.height*1.6)),Image.LANCZOS).save('{OUT}/row{r}_L.png')"], check=True)
    # R-stran celotna vrstica (starši → podpis)
    subprocess.run([sys.executable, "-c",
        f"from PIL import Image; im=Image.open('{SRC}'); "
        f"c=im.crop((1060,{y0},2173,{y1})); c.resize((int(c.width*1.6),int(c.height*1.6)),Image.LANCZOS).save('{OUT}/row{r}_R.png')"], check=True)

print("row crops OK")
