#!/usr/bin/env python3
"""P174 — diag grid (P170/P172/P173 recept): fiksni grid @ 330–1950 / 135px
čez originalno sliko → diag-sNNN.jpg za Read-oči. rows-detekcija P172/173
FAIL-vzorec → samo diag + vizualna branja."""
import os, sys
from PIL import Image, ImageDraw, ImageFont

DIR = "/tmp/p174"

def diag_grid(path, out, step=135, start=330):
    im = Image.open(path).convert("RGB")
    d = ImageDraw.Draw(im)
    w, h = im.size
    lines = list(range(start, 1951, step))
    for i, y in enumerate(lines):
        d.line([(0, y), (w, y)], fill=(255, 0, 0), width=2)
        try:
            f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
        except Exception:
            f = None
        d.text((5, y + 3), f"R{i}", fill=(255, 0, 0), font=f)
    for x, lbl in [(120, "zap"), (330, "mesec"), (480, "smrt"), (640, "pokop"),
                   (830, "vas"), (1050, "hisna"), (1300, "ime"), (1750, "star"),
                   (2000, "bolez"), (2250, "prev"), (2450, "podpis")]:
        d.line([(x, 0), (x, h)], fill=(0, 160, 255), width=1)
        d.text((x + 3, 3), lbl, fill=(0, 160, 255))
    im.save(out, quality=88)

if __name__ == "__main__":
    scans = sys.argv[1:] or ["114", "115", "116", "117", "118", "119", "120", "121", "122"]
    for s in scans:
        p = f"{DIR}/s{s}.jpg"
        out = f"{DIR}/diag-s{s}.jpg"
        diag_grid(p, out)
        im = Image.open(p)
        print(f"s{s}: {im.size[0]}x{im.size[1]} → diag-s{s}.jpg")
