#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P177 kompozit-paneli — vertikalni sklad crops z oznakami (P173 metoda)."""
import os
from PIL import Image, ImageDraw

CROPS = "/tmp/p177/crops"
OUT = "/tmp/p177/forensic"
os.makedirs(OUT, exist_ok=True)
W = 1900


def panel(name, files, scale=1.0):
    ims = []
    for f in files:
        p = os.path.join(CROPS, f)
        im = Image.open(p)
        if scale != 1.0:
            im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
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


panel("K-A-s131s132-griblje.png", [
    "trak-z13-ana-brinec-h14.png",
    "trak-z14-katarina-hrusic-h34.png",
    "trak-z24-ana-pezdirec-h10.png",
    "trak-z26-janez-pezdirec-h42.png",
    "trak-z27-vidou-pezdirec-h48.png",
    "trak-z4-mrtvorojenec-s130.png",
])

panel("K-B-s133s134-griblje.png", [
    "trak-z30-marija-taparic-h33.png",
    "trak-z31-marija-mavric-h57.png",
    "trak-z36-marija-taparic-h33.png",
    "trak-z42-marija-vrsic-h14.png",
    "trak-z46-neza-hrovat-h41.png",
    "trak-z47-nikolaj-nepomuk-h43.png",
])

panel("K-C-s134s135-griblje.png", [
    "trak-z48-matija-bircec-h14.png",
    "trak-z51-peter-perdih-h20.png",
    "trak-z54-janez-foselj-h31.png",
    "trak-z55-katarina-vlobucar-h46.png",
    "trak-z56-margareta-juracevic-h24.png",
    "trak-1912-z1-jozef-pecnik-h87.png",
])

panel("K-D-forenzika-celice.png", [
    "cel-z30-starost-95let.png",
    "cel-z31-starost-96let.png",
    "cel-z48-ime.png",
    "cel-z48-bolezen.png",
    "cel-z47-ime.png",
    "cel-z55-ime.png",
])

panel("K-E-meja-podpisi.png", [
    "glava-s135.png",
    "meja-s135-k5-full.png",
    "glava-s136.png",
    "pod-z30-rauq.png",
    "pod-z31-pithar.png",
    "pod-z13-bitmar.png",
])

panel("K-F-vecje-celice.png", [
    "cel-z54-ime.png",
    "cel-z36-ime.png",
    "cel-z30-datum.png",
    "cel-z13-starost-bolezen.png",
    "cel-z27-starost.png",
    "glava-s133.png",
])
print("OK")
