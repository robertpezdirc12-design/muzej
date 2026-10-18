#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P104 — berljivi polovični izrezi A (zgornja polovica) / B (spodnja polovica)
za skene 199–212, 2× Lanczos (po vzoru p102/p103 read priprave)."""
import os
from PIL import Image

OUT = "/tmp/p104/read"
os.makedirs(OUT, exist_ok=True)
for s in range(199, 213):
    im = Image.open(f"/tmp/p104/scan-{s:02d}.jpg")
    w, h = im.size
    a = im.crop((0, 0, w, int(h * 0.56)))
    b = im.crop((0, int(h * 0.47), w, h))
    a = a.resize((a.width * 2, a.height * 2), Image.LANCZOS)
    b = b.resize((b.width * 2, b.height * 2), Image.LANCZOS)
    a.save(f"{OUT}/s{s}-A.png")
    b.save(f"{OUT}/s{s}-B.png")
    print(f"s{s}: A {a.size} + B {b.size}")
