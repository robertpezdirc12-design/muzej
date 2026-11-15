#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P260 — s15 datumi m1–m3 (1836-restart) — kronološka veriga."""
import os
from PIL import Image

OUT = "/tmp/p260"
def crop(name, path, box, scale):
    img = Image.open(path)
    c = img.crop(box)
    c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS)
    c.save(f"{OUT}/crops/{name}.png")
    print(name, box, "->", c.size)

s15 = f"{OUT}/s15.jpg"
# s15 spodnji del datumskega stolpca (m1–m3 1836) — y ~1080-1420
crop("s15_d_m1_m3", s15, (55, 1060, 280, 1440), 3)
print("DONE")
