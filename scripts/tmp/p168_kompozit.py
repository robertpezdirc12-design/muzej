#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P168 — kompozit-skladalnik forenzičnih izrezov.
Združi izreze v kompozite z rdečo obrobo + rumeno oznako (ime izreza),
da VLM vidi vse v 1 klicu (P162-primerjava-vzor, P167-6-kompozitov).
Izhod: /tmp/p168/forensic/KOMPOZIT-*.png"""
from PIL import Image, ImageDraw
import os

C = "/tmp/p168/crops"
F = "/tmp/p168/forensic"
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


# 1. GRIBLJE-A: s85-dno (z4, z8, z10) + s86 (z11, z13, z15)
stack(["griblje-s85-z4-janez-pezdirec", "griblje-s85-z8-matija-prinec",
       "griblje-s85-z10-matija-dehlic", "griblje-s86-z11-nikolaj-tome",
       "griblje-s86-z13-anton-stravs", "griblje-s86-z15-katarina-zupanic"],
      "KOMPOZIT-griblje-A.png", 0.52)
# 2. GRIBLJE-B: s86 (z16, z17, z21) + s87 (z22) + s88 (z45) + s89 (z49)
stack(["griblje-s86-z16-mihail-bondivec", "griblje-s86-z17-marjeta-zogriva",
       "griblje-s86-z21-marko-srobrijan", "griblje-s87-z22-veria-macvar",
       "griblje-s88-z45-ana-simec", "griblje-s89-z49-alojzij-stravs"],
      "KOMPOZIT-griblje-B.png", 0.52)
# 3. GRIBLJE-C: s89 (z54, z55, z56) + s90 (z59, z61)
stack(["griblje-s89-z54-marija-novak", "griblje-s89-z55-ana-bendirec",
       "griblje-s89-z56-matija-brunez", "griblje-s90-z59-marjeta-mkek",
       "griblje-s90-z61-janez-brinec"], "KOMPOZIT-griblje-C.png", 0.52)
# 4. MEJA 1902/03 (s90): z61 + marker-1903 + z1-1903 + s85-meja-re
stack(["meja-1902-03-z61-zadnji-1902", "meja-1902-03-marker-1903",
       "meja-1902-03-z1-prvi-1903", "meja-1901-02-marker-1903-re"],
      "KOMPOZIT-meja-1902-03.png", 0.62)
# 5. VAS-HISNA-A: 8 celic (2 cols)
stack(["s85-z4-vas-hisna", "s85-z8-vas-hisna", "s85-z10-vas-hisna",
       "s86-z11-vas-hisna", "s86-z13-vas-hisna", "s86-z15-vas-hisna",
       "s86-z16-vas-hisna", "s86-z17-vas-hisna"],
      "KOMPOZIT-vas-hisna-A.png", 0.75, cols=2)
# 6. VAS-HISNA-B: 9 celic (2 cols)
stack(["s86-z21-vas-hisna", "s87-z22-vas-hisna", "s88-z45-vas-hisna",
       "s89-z49-vas-hisna", "s89-z54-vas-hisna", "s89-z55-vas-hisna",
       "s89-z56-vas-hisna", "s90-z59-vas-hisna", "s90-z61-vas-hisna"],
      "KOMPOZIT-vas-hisna-B.png", 0.75, cols=2)
# 7. IME + STAROST (2 cols; konflikti Brinec/Prinec/Brunez + Mkek/Milek)
stack(["s85-z8-ime", "s85-z10-ime", "s89-z55-ime", "s89-z56-ime",
       "s90-z59-ime", "s90-z61-ime", "s85-z4-starost", "s85-z8-starost",
       "s85-z10-starost", "s89-z49-starost", "s89-z55-starost",
       "s89-z56-starost", "s90-z59-starost", "s90-z61-starost"],
      "KOMPOZIT-ime-starost.png", 0.62, cols=2)
# 8. PODPISI: Dostal ×4 + Rauq ×2
stack(["s86-z12-podpis-dostal", "s87-z22-podpis-dostal",
       "s88-z36-podpis-dostal", "s89-z49-podpis-dostal",
       "s86-z10-podpis-rauq", "s90-z58-podpis-rauq"],
      "KOMPOZIT-podpisi.png", 0.62, cols=2)
# 9. ZAPCOL: zap-dup-10 + '345' + γ-cifre ×8
stack(["s85-z9-zapcol", "s85-z10-zapcol", "s86-z10-zapcol",
       "s86-z11-zapcol", "s88-z45-zapcol", "s89-z49-zapcol",
       "s89-z56-zapcol", "s90-z59-zapcol"],
      "KOMPOZIT-zapcol.png", 0.75, cols=2)
print("kompoziti: 9")
