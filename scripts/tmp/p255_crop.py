#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P255 — izrez vrstic vpisov 1828 (m1–m15) iz skenov s2–s3 knjige 01738.
Vsak vpis = vodoravni trak čez razprti list (leva polovica = ženin/nevesta,
desna = starši/priče/urkunde/podpis). Enakomerni trakovi z 25% prekrivanjem,
dedup prek marginalne številke pri VLM branju."""
import os
from PIL import Image

OUT = "/tmp/p255/full"
os.makedirs(OUT, exist_ok=True)


def strips(src, tag, y0, y1, n, half=58):
    im = Image.open(src)
    W, H = im.size
    pitch = (y1 - y0) / n
    for i in range(1, n + 1):
        c = y0 + (i - 0.5) * pitch
        top = max(0, int(c - half))
        bot = min(H, int(c + half))
        im.crop((0, top, W, bot)).save(f"{OUT}/{tag}_m{i}.jpg", quality=92)
        print(f"{tag}_m{i}: y {top}-{bot} ({bot - top}px)")


# s2: glava se konča ~y=235, m1–m8 do ~y=935
strips("/tmp/p255/s2.jpg", "s2", 235, 935, 8)
# s3: glava ~y=225, m9–m15 do ~y=815
strips("/tmp/p255/s3.jpg", "s3", 225, 815, 7)
print("DONE")
