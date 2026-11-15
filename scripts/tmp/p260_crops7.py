#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P260 — končni kropsi s15: m14/m15 polni imeni (ženin+nevesta) + s15 datumi."""
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
# m14 (r4, y~480-610): datum+vas+ime ženina
crop("s15_m14_full_L", s15, (55, 470, 620, 620), 3)
# m14: nevesta ime (x~770-980)
crop("s15_m14_bname", s15, (760, 470, 1000, 620), 4)
# m15 (r5, y~590-730): ženin
crop("s15_m15_full_L", s15, (55, 590, 620, 740), 3)
# m15: nevesta ime
crop("s15_m15_bname", s15, (760, 590, 1000, 740), 4)
# s15 datumi m14/m15
crop("s15_d_m14", s15, (65, 470, 210, 620), 6)
crop("s15_d_m15", s15, (65, 590, 210, 740), 6)
print("DONE")
