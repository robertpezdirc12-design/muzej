#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P167 — zapcol rezine: zap-stolpec z detekcijskimi črtami za ročno
sanacijo manjkajočih vrstic (P166-lekcija: yc→zap-preslikavo VEDEJO
verificirati pikselsko!). Izreže x 0.035–0.075 (zap + natisnjen naslov),
3 vertikalne segmente na sken, zoom ×2.5, rdeče črte @ detekcije +
rumene vrstne številke. Izhod: /tmp/p167/zapcol-sNN-SEG.png"""
from PIL import Image, ImageDraw
import json

OUT = "/tmp/p167"
rows = json.load(open(f"{OUT}/rows.json"))
SCANS = (81, 82, 83, 84, 85)
SEG = 3          # vertikalni segmenti
X0, X1 = 0.035, 0.075
ZOOM = 2.5

for s in SCANS:
    key = f"s{s:02d}"
    rep = rows[key]
    im = Image.open(f"{OUT}/{key}.jpg").convert("RGB")
    w, h = im.size
    x0, x1 = int(w * X0), int(w * X1)
    det = [r["yc"] for r in rep["rows"]]
    marks = [m["yc"] for m in rep["markers"]]
    for seg in range(SEG):
        y0 = h * seg // SEG
        y1 = h * (seg + 1) // SEG
        c = im.crop((x0, y0, x1, y1)).resize(
            (int((x1 - x0) * ZOOM), int((y1 - y0) * ZOOM)), Image.LANCZOS)
        dr = ImageDraw.Draw(c)
        for i, yc in enumerate(det):
            if y0 <= yc < y1:
                yy = (yc - y0) * ZOOM
                dr.line([(0, yy), (c.width, yy)], fill=(255, 0, 0), width=2)
                dr.text((c.width - 60, yy - 14), f"R{i+1}", fill=(255, 200, 0))
        for yc in marks:
            if y0 <= yc < y1:
                yy = (yc - y0) * ZOOM
                dr.line([(0, yy), (c.width, yy)], fill=(0, 190, 0), width=2)
        c.save(f"{OUT}/zapcol-{key}-{seg}.png")
        print(f"{key}-seg{seg}: y {y0}–{y1}, det={len([y for y in det if y0 <= y < y1])}")
print("zapcol rezine: shranjene")
