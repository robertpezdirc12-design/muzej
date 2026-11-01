#!/usr/bin/env python3
"""P173 kompozit-panele — vertikalni sklad crops z oznakami (P172 metoda)."""
import os
from PIL import Image, ImageDraw

CROPS = "/tmp/p173/crops"
OUT = "/tmp/p173/forensic"
os.makedirs(OUT, exist_ok=True)
W = 1900

def panel(name, files, scale=1.0):
    ims = []
    for f in files:
        p = os.path.join(CROPS, f)
        im = Image.open(p)
        if scale != 1.0:
            im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
        # normiraj širino
        if im.width > W:
            r = W / im.width
            im = im.resize((W, int(im.height * r)), Image.LANCZOS)
        ims.append((f, im))
    H = sum(im.height + 42 for _, im in ims) + 10
    canvas = Image.new("RGB", (W, H), (250, 250, 245))
    d = ImageDraw.Draw(canvas)
    y = 0
    for f, im in ims:
        d.rectangle([0, y, W, y + 38], fill=(40, 40, 40))
        d.text((10, y + 9), f, fill=(255, 220, 80))
        y += 40
        canvas.paste(im, ((W - im.width) // 2, y))
        y += im.height + 2
    out = os.path.join(OUT, name)
    canvas.save(out)
    print(f"{name}: {len(ims)} delov, {W}x{H}")

panel("KOMPOZIT-A-glave.png", ["glava-s109.png", "glava-s111.png", "glava-s112.png", "glava-s113.png", "glava-s114.png"])
panel("KOMPOZIT-B-ime-zmede-1.png",
      ["s109-z1-ime-bolez.png", "s109-z2-ime-bolez.png", "s109-z4-ime-star.png",
       "s109-z9-ime-stan.png", "s109-z11-ime-bolez.png", "s110-z13-ime-bolez.png"])
panel("KOMPOZIT-C-ime-zmede-2.png",
      ["s111-z27-ime-bolez.png", "s111-z32-ime-bolez.png", "s112-z36-ime-stan.png",
       "s112-z37-ime-bolez.png", "s112-z39-ime-bolez.png", "s113-z53-ime-stan.png"])
panel("KOMPOZIT-D-ime-datum.png",
      ["s113-z55-ime.png", "s113-z56-ime-stan.png", "s113-z57-hisna-ime.png",
       "s113-z58-ime.png", "s113-z59-datum-ime.png", "s110-z18-datum-ime.png"])
panel("KOMPOZIT-E-dec-h10-podpisi.png",
      ["s114-z63-ime-podpis.png", "s114-z65-ime-podpis.png", "s113-z48-podpis-Lilek.png",
       "s112-z42-podpis-Suida-Suic.png", "s109-z3-podpis-Dostal.png", "s111-z35-podpis-brez.png"])
