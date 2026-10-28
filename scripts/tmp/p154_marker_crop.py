#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P154 forensika — MARKER-MEJA na s13 (prazna vrsta 72): veliki cifri
P153-prvič-brano »1 8 8 8« vs. P154-celostansko-brano »1 8 8 9«?
Max-zoom izrez markerja (celotna širina, visok ločljivosti) + izrezi
posameznih cifrov. Izhod: /tmp/p154/forensics/."""
from PIL import Image
import numpy as np, os

OUT = "/tmp/p154/forensics"
os.makedirs(OUT, exist_ok=True)

im = Image.open("/tmp/p154/s13.jpg")
w, h = im.size
print(f"s13: {w}×{h}")

# detekcija horizontalnih črt (vzorec p153_rows2)
a = np.asarray(im.convert("L"), dtype=np.float32) / 255.0
x0, x1 = int(w * 0.03), int(w * 0.97)
y0, y1 = int(h * 0.055), int(h * 0.985)
band = a[y0:y1, x0:x1]
dark = (band < 0.45).mean(axis=1)
ys = [y for y in range(band.shape[0]) if dark[y] > 0.45]
groups, cur = [], []
for y in ys:
    if cur and y - cur[-1] <= 3:
        cur.append(y)
    else:
        if cur:
            groups.append(int(np.mean(cur)) + y0)
        cur = [y]
if cur:
    groups.append(int(np.mean(cur)) + y0)
print(f"horizontalne črte: {len(groups)} @ {groups[:20]}")

# marker-vrsta = prostoren predel; po p153_rows.py je r72 (indeks 8/14).
# Poiščemo NAJVIŠJO vrstico (največja višina med sosednjima črtama)
heights = [groups[i+1] - groups[i] for i in range(len(groups)-1)]
big_i = max(range(len(heights)), key=lambda i: heights[i])
print(f"najvišja vrstica: med črtama {big_i} in {big_i+1} ({heights[big_i]} px)")

# izrez s šumnikom: celotna širina
top = max(0, groups[big_i] - 12)
bot = min(h, groups[big_i + 1] + 12)
full = im.crop((0, top, w, bot))
sc = 3.0 if w < 2400 else 2.0
full.resize((int(full.width * sc), int(full.height * sc)), Image.LANCZOS).save(f"{OUT}/s13-marker-full.png")
print(f"marker-full: {full.size} → ×{sc}")

# desna polovica (kjer so cifri) še večja
right = im.crop((int(w*0.35), top, w, bot))
sc2 = 4.5
right.resize((int(right.width * sc2), int(right.height * sc2)), Image.LANCZOS).save(f"{OUT}/s13-marker-right.png")
print(f"marker-right: {right.size} → ×{sc2}")

# posamezne cifre: poiščemo temne bloke v marker-vrsti (navpična projekcija)
mband = a[top+8:bot-8, :]
darkcol = (mband < 0.5).mean(axis=0)
cols = [x for x in range(w) if darkcol[x] > 0.08]
cgroups, cur2 = [], []
for x in cols:
    if cur2 and x - cur2[-1] <= 14:
        cur2.append(x)
    else:
        if cur2:
            cgroups.append((cur2[0], cur2[-1]))
        cur2 = [x]
if cur2:
    cgroups.append((cur2[0], cur2[-1]))
print(f"cifri-bloki: {len(cgroups)} @ {cgroups}")
for i, (cx0, cx1) in enumerate(cgroups):
    c = im.crop((max(0, cx0-14), top, min(w, cx1+14), bot))
    sc3 = 6.0
    c.resize((int(c.width * sc3), int(c.height * sc3)), Image.LANCZOS).save(f"{OUT}/s13-marker-d{i+1}.png")
print("cifre shranjene")
