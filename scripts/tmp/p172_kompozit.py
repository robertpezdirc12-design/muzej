#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P172 — kompozit-skladalnik forenzičnih izrezov (P168/P171-vzor).
Izhod: /tmp/p172/forensic/KOMPOZIT-*.png"""
from PIL import Image, ImageDraw
import os

C = "/tmp/p172/crops"
F = "/tmp/p172/forensic"
os.makedirs(F, exist_ok=True)


def stack(names, out, scale=0.55, label_h=40):
    ims = []
    for nm in names:
        im = Image.open(f"{C}/{nm}.png")
        im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
        ims.append((nm, im))
    w = max(im.width for _, im in ims) + 24
    h = sum(im.height + label_h + 10 for _, im in ims) + 10
    canvas = Image.new("RGB", (w, h), (245, 245, 240))
    dr = ImageDraw.Draw(canvas)
    y = 10
    for i, (nm, im) in enumerate(ims):
        dr.rectangle([8, y - 2, 8 + im.width + 8, y + im.height + 8], outline=(220, 0, 0), width=3)
        dr.text((16, y + im.height + 12), f"PANEL-{i+1}: {nm}", fill=(180, 100, 0))
        canvas.paste(im, (12, y))
        y += im.height + label_h + 10
    canvas.save(f"{F}/{out}.png")
    print(f"{out}.png {canvas.size}")


stack([
    "griblje-s104-z1-ana-brinec",
    "griblje-s104-z6-katarina-pezdirec",
    "griblje-s105-z16-matija-strukelj",
    "griblje-s105-z21-janez-krizc",
    "griblje-s106-z23-katarina-simec",
], "KOMPOZIT-A1-griblje-z1-z23", scale=0.5)

stack([
    "griblje-s106-z29-matija-tozek",
    "griblje-s107-z34-matija-urh",
    "griblje-s107-z35-janez-focek",
    "griblje-s108-z48-jurij-jocek",
    "griblje-s108-z54-alojz-simec",
], "KOMPOZIT-A2-griblje-z29-z54", scale=0.5)

stack([
    "cell-s104-z1-hisna-h49-vs-19",
    "cell-s104-z1-ime-ana-brinec",
    "cell-s104-z6-bolezen-nadruka",
    "cell-s105-z16-ime-strukelj",
    "cell-s105-z21-ime-krizc-podpis",
], "KOMPOZIT-B1-celice-zmede", scale=0.62)

stack([
    "cell-s108-z48-ime-jocek",
    "cell-s108-z48-hisna-h77",
    "cell-s108-z54-ime-simec",
    "cell-s108-z54-hisna-h18",
], "KOMPOZIT-B2-celice-s108", scale=0.62)

stack([
    "cell-s104-glava-48-1905",
    "cell-s105-glava-18906",
    "cell-s106-glava-185306",
    "cell-s107-glava-185306",
    "cell-s108-glava-185306",
    "s104-meja-1906-pas",
    "s109-z1-anton-ali-ana-brinec",
], "KOMPOZIT-C-glave-meja", scale=0.45)

print("KONČANO")
