#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P171 — kompozit-skladalnik forenzičnih izrezov.
Združi izreze v kompozite z rdečo obrobo + rumeno oznako (ime izreza),
da VLM vidi vse v 1 klicu (P168-vzor).
Izhod: /tmp/p171/forensic/KOMPOZIT-*.png"""
from PIL import Image, ImageDraw
import os

C = "/tmp/p171/crops"
F = "/tmp/p171/forensic"
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


# 1. z1-PEZDIREC-forenzika: s99-z1 (4 celice) + kalibracija
#    (s101-z27 Martin-Bedirec/Pezdirec + s100-z15 Jožef-Pesdirec ime-celici!)
stack(["s99-z1-ime", "s99-z1-vas-hisna", "s99-z1-starost", "s99-z1-bolezen",
       "s101-z27-ime", "s100-z15-ime"],
      "KOMPOZIT-z1-pezdirec.png", 0.55)

# 2. VAS-HISNA-A: 8 celic (2 cols; brez trakov — preširoki!)
stack(["s99-z10-vas-hisna", "s103-z49-vas-hisna", "s103-z59-vas-hisna",
       "s104-z61-vas-hisna", "s102-z45-vas-hisna", "s99-z5-vas-hisna",
       "s101-z27-vas-hisna", "s104-r6-ime"],
      "KOMPOZIT-vas-hisna-A.png", 0.75, cols=2)

# 3. IMENA-A: Griblje-imena (3 cols)
stack(["s100-z16-ime", "s100-z19-ime", "s100-z20-ime",
       "s101-z26-ime", "s101-z29-ime", "s102-z44-ime",
       "s103-z49-ime", "s103-z50-ime", "s103-z59-ime"],
      "KOMPOZIT-imena-A.png", 0.62, cols=3)

# 4. IMENA-B: kontekst-imena (3 cols)
stack(["s99-z6-ime", "s99-z8-ime", "s99-z11-ime", "s99-z12-ime",
       "s104-z61-ime", "s104-r6-ime",
       "s102-z48-ime", "s103-z54-ime", "s101-z27-ime"],
      "KOMPOZIT-imena-B.png", 0.62, cols=3)

# 5. STAROSTI-A (3 cols)
stack(["s99-z1-starost", "s99-z4-starost", "s99-z7-starost",
       "s99-z9-starost", "s99-z10-starost", "s100-z15-starost",
       "s100-z19-starost", "s100-z24-starost", "s101-z30-starost"],
      "KOMPOZIT-starosti-A.png", 0.62, cols=3)

# 6. STAROSTI-B (3 cols)
stack(["s101-z31-starost", "s101-z32-starost", "s102-z37-starost",
       "s102-z39-starost", "s102-z41-starost", "s102-z44-starost",
       "s102-z48-starost", "s103-z53-starost", "s103-z59-starost"],
      "KOMPOZIT-starosti-B.png", 0.62, cols=3)

# 7. MEJA + GLAVE (10. glava-napaka!)
stack(["meja-1923-pas", "glava-s99-18905", "glava-s101-18",
       "glava-s102-18905", "glava-s103-18905"],
      "KOMPOZIT-meja-glave.png", 0.62)

# 8. BOLEZNI (3 cols)
stack(["s99-z1-bolezen", "s100-z20-bolezen", "s102-z38-bolezen",
       "s103-z57-bolezen", "s104-z61-bolezen", "s99-z10-starost"],
      "KOMPOZIT-bolezni.png", 0.68, cols=3)
