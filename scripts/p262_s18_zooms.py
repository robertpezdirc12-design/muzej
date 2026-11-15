#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P262 — s18 per-row/cell zooms (AGENT-VIZIJA). 7 vrstic (m6–m12), L+R stran."""
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = f"{ROOT}/research/issue17/p261-work/s18.jpg"
OUT = f"{ROOT}/research/issue17/p262-work"

w, h = 2173, 1500
# 7 vrstic — grobe meje (z overlapom)
rows = {1: (240, 440), 2: (420, 620), 3: (600, 800), 4: (780, 980), 5: (950, 1160), 6: (1130, 1330), 7: (1310, 1500)}

# L-stran celice (x): datum+margin | Wohnort+HausNr+imeni | nevesta-blok
lx = {"date": (80, 340), "groom": (290, 760), "brideL": (740, 1146)}
# R-stran celice (x): starši-zenina | starši-neveste | priče+urkunden+podpis
rx = {"parentsG": (1060, 1420), "parentsB": (1400, 1800), "witness": (1780, 2173)}

cmds = []
for r, (y0, y1) in rows.items():
    for name, (x0, x1) in lx.items():
        cmds.append((f"z{r}_{name}_L", x0, y0, x1, y1))
    for name, (x0, x1) in rx.items():
        cmds.append((f"z{r}_{name}_R", x0, y0, x1, y1))

for tag, x0, y0, x1, y1 in cmds:
    cw, ch = x1 - x0, y1 - y0
    scale = 3 if cw < 400 else 2
    code = (f"from PIL import Image; im=Image.open('{SRC}'); "
            f"im.crop(({x0},{y0},{x1},{y1})).resize((({x1}-{x0})*{scale},({y1}-{y0})*{scale}),Image.LANCZOS)"
            f".save('{OUT}/{tag}.png')")
    subprocess.run(["python3", "-c", code], check=True)

print("zooms:", len(os.listdir(OUT)))
