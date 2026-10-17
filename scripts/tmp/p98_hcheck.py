#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P98 - preveri kontinuitete gibriljskih his v parish.ts vitals."""
import re

SRC = "src/data/atlas/parish.ts"
CAND = ("5", "20", "23", "24", "32", "34", "35", "63", "83", "12", "30", "58")

src = open(SRC, encoding="utf-8").read()
pat = re.compile(r'\{[^{}]*?bookSignature:\s*"04105"[^{}]*?\}', re.S)
rows = []
for m in pat.finditer(src):
    b = m.group(0)
    hn = re.search(r'houseNo:\s*"([^"]*)"', b)
    yr = re.search(r'year:\s*(\d+)', b)
    sc = re.search(r'scan:\s*(\d+)', b)
    if hn and yr:
        rows.append((int(yr.group(1)), hn.group(1), int(sc.group(1)) if sc else 0))

want = set(CAND)
grib = sorted(r for r in rows if r[1].split(" ")[0] in want)
for r in grib:
    print(r)
print("---- po hisi (zadnje leto pred 1903) ----")
last = {}
for y, h, sc in grib:
    h0 = h.split(" ")[0]
    last.setdefault(h0, []).append((y, sc))
for h in sorted(last, key=int):
    ys = sorted(last[h])
    print(h, ys)
