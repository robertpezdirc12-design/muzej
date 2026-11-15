#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P260 — odločilni kropsi: hišne številke m6/m7 (63-vs-68-duel!) + starši/priče m6/m7."""
import os
from PIL import Image

OUT = "/tmp/p260"
os.makedirs(f"{OUT}/crops", exist_ok=True)

def crop(name, path, box, scale):
    img = Image.open(path)
    c = img.crop(box)
    c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS)
    c.save(f"{OUT}/crops/{name}.png")
    print(name, box, "->", c.size)

s16 = f"{OUT}/s16.jpg"

# m6 (r3): ženin hišna (Grihle 9) y~425-560 — hišna stolpec x~230-320
crop("s16_hn6_groom", s16, (200, 425, 330, 560), 8)
# m6: nevesta hišna (Grihle 63/68) x~700-800
crop("s16_hn6_bride", s16, (640, 425, 810, 560), 8)
# m7 (r4): ženin hišna 63/68
crop("s16_hn7_groom", s16, (200, 530, 330, 670), 8)
# m7: nevesta hišna 9
crop("s16_hn7_bride", s16, (640, 530, 810, 670), 8)
# m6/m7 starši (desna stran): x~820-1330, y~425-670
crop("s16_starši_m6_m7", s16, (820, 425, 1340, 670), 3)
# m6/m7 priče: x~1340-1600
crop("s16_priče_m6_m7", s16, (1330, 425, 1620, 670), 4)
# s15 m14/m15 neveste hišne (Grübl 4/6) — y~480-720, x~640-780
s15 = f"{OUT}/s15.jpg"
crop("s15_hn14", s15, (620, 480, 790, 610), 8)
crop("s15_hn15", s15, (620, 600, 790, 730), 8)
print("DONE")
