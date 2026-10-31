#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P169 diag — vizualna kontrola rows3.json (celice + cifre + linije).
Izhod: /tmp/p169/diag-sNN.png (agent-oči: Read tool)."""
from PIL import Image, ImageDraw
import json

OUT = "/tmp/p169"
rep = json.load(open(f"{OUT}/rows3.json"))

for key, d in rep.items():
    scan = int(key[1:])
    im = Image.open(f"{OUT}/s{scan:02d}.jpg").convert("RGB")
    dr = ImageDraw.Draw(im)
    w, h = im.size
    for i, c in enumerate(d["cells"]):
        dr.line([(0, c["y0"]), (w, c["y0"])], fill=(0, 160, 255), width=1)
        dr.line([(0, c["y1"]), (w, c["y1"])], fill=(0, 160, 255), width=1)
        dr.text((w - 60, c["yc"] - 6), f"c{i}", fill=(255, 120, 0))
    for r in d["rows"]:
        col = (255, 0, 0) if r.get("orphan") else (220, 0, 180)
        dr.line([(0, r["cifra_yc"]), (w, r["cifra_yc"])], fill=col, width=2)
    for y in d["lines"]:
        dr.line([(0, y), (w, y)], fill=(0, 190, 0), width=1)
    im.save(f"{OUT}/diag-{key}.png")
    print(f"diag-{key}.png: celic={len(d['cells'])} linij={len(d['lines'])}")
