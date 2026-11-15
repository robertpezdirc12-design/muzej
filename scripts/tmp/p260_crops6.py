#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P260 — letterform-referenca: hišna m7 (63/68) VS starost m7 (28) — isti roka!"""
import os
from PIL import Image

OUT = "/tmp/p260"
def crop(name, path, box, scale):
    img = Image.open(path)
    c = img.crop(box)
    c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS)
    c.save(f"{OUT}/crops/{name}.png")
    print(name, box, "->", c.size)

s16 = f"{OUT}/s16.jpg"
# m7 (r4, y~530-670): hišna ženina (x~230-320) | starost ženina (x~440-500)
crop("s16_m7_house", s16, (215, 540, 320, 665), 10)
crop("s16_m7_age", s16, (430, 540, 520, 665), 10)
# m6 (r3, y~425-560): nevesta hišna (x~700-810) + starost neveste
crop("s16_m6_bhouse", s16, (690, 430, 810, 560), 10)
crop("s16_m6_bage", s16, (880, 430, 950, 560), 10)
# s13_r6 (P259 duel 58-vs-68!) — primerjava s s13 iz P259-diska
print("DONE")
