#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P169 — kompozit-2: re-crops (pravilni x-rangei) + super-zoomi.
Izhod: /tmp/p169/forensic/KOMPOZIT2-*.png"""
from PIL import Image, ImageDraw
import os

C = "/tmp/p169/crops"
F = "/tmp/p169/forensic"
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
    else:
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


# A. STAROST-RE: 17 Griblje (pravilni x 1530–1770!)
stack(["re-s90-r1-starost", "re-s90-r3-starost", "re-s90-r4-starost",
       "re-s91-z8-starost", "re-s91-z10-starost", "re-s91-z12-starost",
       "re-s91-z13-starost", "re-s91-z14-starost", "re-s91-z16-starost",
       "re-s91-z19-starost", "re-s92-z22-starost", "re-s92-z30-starost",
       "re-s93-z38-starost", "re-s93-z41-starost", "re-s93-z42-starost",
       "re-s94-z48-starost", "re-s94-z50-starost"],
      "KOMPOZIT2-starost-re.png", 0.8, cols=2)
# B. BOLEZEN: 17 Griblje
stack(["re-s90-r1-bolezen", "re-s90-r3-bolezen", "re-s90-r4-bolezen",
       "re-s91-z8-bolezen", "re-s91-z10-bolezen", "re-s91-z12-bolezen",
       "re-s91-z13-bolezen", "re-s91-z14-bolezen", "re-s91-z16-bolezen",
       "re-s91-z19-bolezen", "re-s92-z22-bolezen", "re-s92-z30-bolezen",
       "re-s93-z38-bolezen", "re-s93-z41-bolezen", "re-s93-z42-bolezen",
       "re-s94-z48-bolezen", "re-s94-z50-bolezen"],
      "KOMPOZIT2-bolezen.png", 0.8, cols=2)
# C. SUPER-ZOOM-IME ×6 (8 konfliktov)
stack(["sz-s90-r4-ime-x6", "sz-s91-z12-ime-x6", "sz-s93-z38-ime-x6",
       "sz-s93-z41-ime-x6", "sz-s94-z48-ime-x6", "sz-s94-z50-ime-x6",
       "sz-s91-z19-hisna-x6", "sz-s94-z48-hisna-x6"],
      "KOMPOZIT2-super-ime.png", 0.55, cols=2)
# D. SUPER-ZOOM-HISNA ×6 (4 konflikta + 2 kontrola)
stack(["sz-s91-z19-hisna-x6", "sz-s93-z38-hisna-x6",
       "sz-s93-z42-hisna-x6", "sz-s94-z48-hisna-x6"],
      "KOMPOZIT2-super-hisna.png", 0.7)
# E. SUPER-ZOOM-STAROST ×6 (s90-r1/r3 = Štravs otroka!)
stack(["sz-s90-r1-starost-x6", "sz-s90-r3-starost-x6"],
      "KOMPOZIT2-super-starost.png", 0.8)
