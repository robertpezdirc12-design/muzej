#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P243 — pass-4: s36 z 8 vrstičnimi trakovi (hipoteza 1–8) + polni numcol + glava-zona."""
import os
from PIL import Image

OUT = "/tmp/p243/crops4"
os.makedirs(OUT, exist_ok=True)

im = Image.open("/tmp/p243/s36.jpg")
w, h = im.size

# hipoteza: 8 vrstic od ~y300 do ~y1640
n = 8
top, bot = 300, 1640
step = (bot - top) / n
for r in range(n):
    y0 = max(0, int(top + r * step) - 10)
    y1 = min(h, int(top + (r + 1) * step) + 10)
    L = im.crop((0, y0, 1230, y1))
    L = L.resize((L.width * 2, L.height * 2), Image.LANCZOS)
    L.save(f"{OUT}/s36-8r{r+1}-L.jpg", quality=92)
    R = im.crop((1180, y0, w, y1))
    R = R.resize((R.width * 2, R.height * 2), Image.LANCZOS)
    R.save(f"{OUT}/s36-8r{r+1}-R.jpg", quality=92)
    print(f"s36-8r{r+1}: y {y0}-{y1}")

# polni numcol (y0–1700) 3×
c = im.crop((60, 0, 260, 1700))
c = c.resize((c.width * 3, c.height * 3), Image.LANCZOS)
c.save(f"{OUT}/s36-numcol-full-3x.jpg", quality=93)
print("numcol-full:", c.size)

# glava-zona: velika 1880 + prvi datum (nad vrsto 1?)
g = im.crop((0, 0, 1400, 420))
g = g.resize((int(g.width * 2.2), int(g.height * 2.2)), Image.LANCZOS)
g.save(f"{OUT}/s36-glava-zona.jpg", quality=93)
print("glava-zona:", g.size)

# datumski stolpec s36 (nad vrsto 1 — 5. MEJNA-VARIANTA preverba: je letnica v stolpcu ali vrhnja glava?)
d = im.crop((260, 0, 700, 500))
d = d.resize((d.width * 3, d.height * 3), Image.LANCZOS)
d.save(f"{OUT}/s36-datumcol-top-3x.jpg", quality=93)
print("datumcol-top:", d.size)
print("DONE")
