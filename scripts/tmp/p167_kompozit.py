#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P167 — kompozit-skladalnik forenzičnih izrezov.
Združi izreze v vertikalne/grafove kompozite z rdečo obrobo + rumeno
oznako (ime izreza), da VLM vidi vse v 1 klicu (P162-primerjava-vzor).
Izhod: /tmp/p167/forensic/KOMPOZIT-*.png"""
from PIL import Image, ImageDraw
import os

C = "/tmp/p167/crops"
F = "/tmp/p167/forensic"
os.makedirs(F, exist_ok=True)


def stack(names, out, scale=0.8, cols=1, label_h=46):
    ims = []
    for nm in names:
        im = Image.open(f"{C}/{nm}.png")
        im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
        ims.append((nm, im))
    if cols == 1:
        w = max(im.width for _, im in ims) + 24
        h = sum(im.height + label_h + 12 for _, im in ims) + 12
        canvas = Image.new("RGB", (w, h), (245, 245, 240))
        dr = ImageDraw.Draw(canvas)
        y = 12
        for i, (nm, im) in enumerate(ims):
            dr.rectangle([8, y - 2, 8 + im.width + 8, y + im.height + 8],
                         outline=(220, 0, 0), width=3)
            dr.text((16, y + im.height + 14), f"PANEL-{i+1}: {nm}",
                    fill=(180, 100, 0))
            canvas.paste(im, (12, y))
            y += im.height + label_h + 12
    else:  # grid
        cw = max(im.width for _, im in ims) + 24
        ch = max(im.height for _, im in ims) + label_h + 12
        rows = (len(ims) + cols - 1) // cols
        canvas = Image.new("RGB", (cols * cw + 12, rows * ch + 12), (245, 245, 240))
        dr = ImageDraw.Draw(canvas)
        for i, (nm, im) in enumerate(ims):
            r, c = i // cols, i % cols
            x, y = 12 + c * cw, 12 + r * ch
            dr.rectangle([x - 2, y - 2, x + im.width + 8, y + im.height + 8],
                         outline=(220, 0, 0), width=3)
            dr.text((x + 4, y + im.height + 14), f"PANEL-{i+1}: {nm}",
                    fill=(180, 100, 0))
            canvas.paste(im, (x + 2, y))
    canvas.save(f"{F}/{out}")
    print(f"{out}: {canvas.size}, {os.path.getsize(f'{F}/{out}')//1024} KB")


# 1. MEJA 1901/02 (s85): zap55 + marker + zap1-1902
stack(["meja-1901-02-zap55-zadnji-1901", "meja-1901-02-marker-1902",
       "meja-1901-02-zap1-prvi-1902"], "KOMPOZIT-meja-1901-02.png", 0.62)
# 2. GRIBLJE-A: zap1, zap4, zap7, zap11, zap13
stack(["griblje-zap1-ana-krizan-80dno", "griblje-zap4-matija-hlobucar-80dno",
       "griblje-zap7-anton-stolfa-81", "griblje-zap11-marija-brinec-81",
       "griblje-zap13-marija-cindric-81"], "KOMPOZIT-griblje-A.png", 0.52)
# 3. GRIBLJE-B: zap15, zap19, zap50, zap51, zap55
stack(["griblje-zap15-ana-milek-81", "griblje-zap19-martin-papic-82",
       "griblje-zap50-janez-kesran-84", "griblje-zap51-janez-jakobcic-84",
       "griblje-zap55-nikolaj-rampic-85"], "KOMPOZIT-griblje-B.png", 0.52)
# 4. VAS-HISNA ×10 (2 cols × 5)
stack(["s80-r1-vas-hisna", "s80-r4-vas-hisna", "s81-zap7-vas-hisna",
       "s81-zap11-vas-hisna", "s81-zap13-vas-hisna", "s81-zap15-vas-hisna",
       "s82-zap19-vas-hisna", "s84-zap50-vas-hisna", "s84-zap51-vas-hisna",
       "s85-zap55-vas-hisna"], "KOMPOZIT-vas-hisna.png", 0.75, cols=2)
# 5. IME ×6 + STAROST ×5 (2 cols)
stack(["s81-zap7-ime", "s81-zap13-ime", "s82-zap19-ime", "s84-zap50-ime",
       "s84-zap51-ime", "s85-zap55-ime", "s80-r1-starost", "s80-r4-starost",
       "s84-zap50-starost", "s84-zap51-starost", "s85-zap55-starost"],
      "KOMPOZIT-ime-starost.png", 0.62, cols=2)
# 6. PODPISI ×6
stack(["s81-zap7-podpis", "s81-zap11-podpis", "s84-zap50-podpis",
       "s85-zap55-podpis", "s82-zap20-podpis-rauq", "s83-zap32-podpis"],
      "KOMPOZIT-podpisi.png", 0.62, cols=2)
print("kompoziti: 6")
