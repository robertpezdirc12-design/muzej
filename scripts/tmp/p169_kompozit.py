#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P169 — kompozit-skladalnik forenzičnih izrezov.
Združi izreze v kompozite z rdečo obrobo + rumeno oznako (ime izreza),
da VLM vidi vse v 1 klicu (P162-primerjava-vzor, P168-9-kompozitov).
Izhod: /tmp/p169/forensic/KOMPOZIT-*.png"""
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


# 1. GRIBLJE-A: s90-dno (z1, z3, z4) + s91 (z8, z10, z12)
stack(["griblje-s90-z1-alojzij-stravs", "griblje-s90-z3-nikolaj-stravs",
       "griblje-s90-z4-jozef-zegriva", "griblje-s91-z8-barbara-pezdirec",
       "griblje-s91-z10-marija-pezdirec", "griblje-s91-z12-franciska-kukan"],
      "KOMPOZIT-griblje-A.png", 0.52)
# 2. GRIBLJE-B: s91 (z13, z14, z16, z19) + s92 (z22, z30)
stack(["griblje-s91-z13-ana-brodaric", "griblje-s91-z14-marija-zefko",
       "griblje-s91-z16-janez-simec", "griblje-s91-z19-alojzij-pozek",
       "griblje-s92-z22-janez-pecnirec", "griblje-s92-z30-katarina-zefko"],
      "KOMPOZIT-griblje-B.png", 0.52)
# 3. GRIBLJE-C: s93 (z38, z41, z42) + s94 (z48, z50)
stack(["griblje-s93-z38-marija-span", "griblje-s93-z41-jurij-simec",
       "griblje-s93-z42-andrej-sotler", "griblje-s94-z48-katarina-radovic",
       "griblje-s94-z50-marija-dragar"], "KOMPOZIT-griblje-C.png", 0.52)
# 4. MEJA 1903/04 (s94): z51 + marker-1904 + r1 + s90-marker-re
stack(["meja-1903-04-z51-zadnji-1903", "meja-1903-04-marker-1904",
       "meja-1903-04-z1-prvi-1904", "meja-1902-03-marker-1903-re"],
      "KOMPOZIT-meja-1903-04.png", 0.62)
# 5. GLAVE-NAPAKE (3 pisarjeve napake-kandidati)
stack(["glava-s92-18903", "glava-s94-18903", "glava-s95-181904"],
      "KOMPOZIT-glave-napake.png", 0.85)
# 6. VAS-HISNA-A: 9 celic (2 cols)
stack(["s90-z1-vas-hisna", "s90-z3-vas-hisna", "s90-z4-vas-hisna",
       "s91-z8-vas-hisna", "s91-z10-vas-hisna", "s91-z12-vas-hisna",
       "s91-z13-vas-hisna", "s91-z14-vas-hisna", "s91-z16-vas-hisna"],
      "KOMPOZIT-vas-hisna-A.png", 0.75, cols=2)
# 7. VAS-HISNA-B: 8 celic (2 cols)
stack(["s91-z19-vas-hisna", "s92-z22-vas-hisna", "s92-z30-vas-hisna",
       "s93-z38-vas-hisna", "s93-z41-vas-hisna", "s93-z42-vas-hisna",
       "s94-z48-vas-hisna", "s94-z50-vas-hisna"],
      "KOMPOZIT-vas-hisna-B.png", 0.75, cols=2)
# 8. IME (8 konfliktov, 2 cols)
stack(["s90-z4-ime", "s91-z12-ime", "s92-z22-ime", "s93-z38-ime",
       "s93-z41-ime", "s94-z48-ime", "s94-z50-ime", "s94-r3-ime"],
      "KOMPOZIT-ime.png", 0.75, cols=2)
# 9. STAROST (10 spornih, 2 cols)
stack(["s90-r1-starost", "s90-r3-starost", "s90-r4-starost",
       "s91-z10-starost", "s92-z22-starost", "s92-z30-starost",
       "s93-z38-starost", "s93-z41-starost", "s94-z48-starost",
       "s94-z50-starost"], "KOMPOZIT-starost.png", 0.75, cols=2)
# 10. PODPISI + s95-kontekst (7)
stack(["s91-z8-podpis-dostal", "s93-z37-podpis-rauq",
       "s94-z44-podpis-prazno", "s94-r1-podpis-rauq",
       "s95-z4-podpis-dostal", "s95-z8-anton-sajnic-kontekst",
       "s95-z10-ana-krvan-kontekst"], "KOMPOZIT-podpisi.png", 0.62)
# 11. ZAPCOL (8 rezin, 2 cols)
stack(["s90-r1-zapcol", "s90-r7-zapcol", "s91-z8-zapcol",
       "s92-z20-zapcol", "s93-z32-zapcol", "s94-z44-zapcol",
       "s94-r1-zapcol", "s95-z4-zapcol"], "KOMPOZIT-zapcol.png",
      0.9, cols=2)
