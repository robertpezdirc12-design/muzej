#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P162 — forenzični izrezi za leto 1896 (mrliška 04894, skeni 55–61).
Iz rows.json (rule/ink detekcija) izreže:
  1. TRAKOVI x2.2 (polna širina, yc±72) za vse Griblje vrstice 1896 + mejne
     vrstice + območji markerjev 1896./1897.
  2. CELICE x3.0 (starost) za sporne: Peter Urh (s56 v9), Ana Ogrizovičeva
     (s55 v11).
Izhod: /tmp/p162/crops/*.png + manifest.json."""
from PIL import Image
import os, json

OUT = "/tmp/p162"
CROPS = f"{OUT}/crops"
os.makedirs(CROPS, exist_ok=True)
rows = json.load(open(f"{OUT}/rows.json"))

# --- MANIFEST -------------------------------------------------------------
# strip: (skan, vrsta_index_1based, namen)
STRIPS = [
    # 18 Griblje vrstic leta 1896
    (55, 11, "griblje-zap1-ana-ogrizoviceva-58"),          # GR-01
    (56, 1, "griblje-zap5-marija-copnik-42"),              # GR-02
    (56, 4, "griblje-zap8-n-binec-14"),                    # GR-03
    (56, 6, "griblje-zap10-barbara-straus-45"),            # GR-04
    (56, 7, "griblje-zap11-marija-mih-51"),                # GR-05
    (56, 9, "griblje-zap13-peter-urh-51"),                 # GR-06
    (57, 4, "griblje-zap20-matija-pezdirec-20"),           # GR-07
    (57, 7, "griblje-zap23-marija-pezdirec-42"),           # GR-08
    (58, 3, "griblje-zap31-ana-cernic-27"),                # GR-09
    (58, 4, "griblje-zap32-nikolaj-brodaric-46"),          # GR-10
    (58, 5, "griblje-zap33-ana-verbicar-61"),              # GR-11
    (58, 12, "griblje-zap40-barbara-hvalesic-26"),         # GR-12
    (59, 3, "griblje-zap43-nikolaj-stabigar-46"),          # GR-13
    (59, 8, "griblje-zap48-ana-krizan-63"),                # GR-14
    (59, 9, "griblje-zap49-matija-jakobcic-64"),           # GR-15
    (59, 10, "griblje-zap50-magdalena-hlevic-41"),         # GR-16
    (59, 12, "griblje-zap52-neza-jakobcic-9"),             # GR-17
    (60, 2, "griblje-zap54-joana-papic-31"),               # GR-18
    # meja 1895/1896 (s55): zadnja 1895 vrstica + marker + prva 1896
    (55, 7, "meja-1895-96-zap52-zadnja-1895"),
    (55, 8, "meja-1895-96-zap1-prva-1896"),
    # meja 1896/1897 (s60): zadnja 1896 + marker + prvi 1897
    (60, 8, "meja-1896-97-zap60-zadnja-1896"),
    (60, 9, "meja-1896-97-zap1-prva-1897"),
    (60, 10, "meja-1896-97-zap2-1897"),
]
# celice x3.0: (skan, vrsta, namen, x0, x1)
CELLS = [
    (56, 9, "celica-urh-starost", 0.555, 0.685),
    (55, 11, "celica-ogrizoviceva-starost", 0.555, 0.685),
    # referencne cifre istega pisarja (s56): v2 = "95 let" (9), v11 = "4 leta" (4)
    (56, 2, "ref-s56-v2-95let", 0.555, 0.685),
    (56, 11, "ref-s56-v11-4leta", 0.555, 0.685),
    # spori iz forenzike: 40/90, 72/92, 11/14, 90/10, hisna 61/64, Binec ?
    (56, 6, "celica-straus-starost", 0.545, 0.695),
    (56, 7, "celica-muh-starost", 0.545, 0.695),
    (57, 7, "celica-pezdirec-m-starost", 0.545, 0.695),
    (58, 3, "celica-cernic-starost", 0.545, 0.695),
    (58, 5, "celica-verbicar-hisna", 0.245, 0.335),
    (56, 4, "celica-binec-starost", 0.545, 0.695),
]
HALF = 72
Z_STRIP, Z_CELL = 2.2, 3.0
X_FULL = (0.015, 0.985)


def crop(scan, vrsta, x0, x1, half, zoom, name):
    key = f"s{scan:02d}"
    r = rows[key]["rows"][vrsta - 1]
    im = Image.open(f"{OUT}/{key}.jpg")
    w, h = im.size
    yc = r["yc"]
    y0, y1 = max(0, yc - half), min(h, yc + half)
    c = im.crop((int(w * x0), y0, int(w * x1), y1))
    c = c.resize((int(c.width * zoom), int(c.height * zoom)), Image.LANCZOS)
    p = f"{CROPS}/{name}.png"
    c.save(p)
    return {"name": name, "scan": scan, "vrsta": vrsta, "yc": yc,
            "y0": y0, "y1": y1, "x": [x0, x1], "zoom": zoom,
            "px": [c.width, c.height], "file": p}


def main():
    man = {"strips": [], "cells": []}
    for (scan, vrsta, name) in STRIPS:
        man["strips"].append(crop(scan, vrsta, *X_FULL, HALF, Z_STRIP, name))
    for (scan, vrsta, name, x0, x1) in CELLS:
        man["cells"].append(crop(scan, vrsta, x0, x1, HALF, Z_CELL, name))
    json.dump(man, open(f"{CROPS}/manifest.json", "w"), indent=1)
    # primerjalna slika: Urh | ref 9 (iz 95) | ref 4 (iz 4 leta)
    comps = []
    for nm in ("celica-urh-starost", "ref-s56-v2-95let", "ref-s56-v11-4leta"):
        im = Image.open(f"{CROPS}/{nm}.png")
        # izrezi sredinski del (starostni zapisi so na sredini celice)
        w, h = im.size
        comps.append(im.crop((int(w * 0.15), int(h * 0.15), int(w * 0.62), h)))
    hh = max(c.height for c in comps)
    tot = Image.new("RGB", (sum(c.width for c in comps) + 40, hh), (255, 255, 255))
    x = 0
    for c in comps:
        tot.paste(c, (x, 0))
        x += c.width + 20
    tot.save(f"{CROPS}/primerjava-cifer.png")
    print(f"primerjava-cifer.png: {tot.size}")
    print(f"trakov={len(man['strips'])} celic={len(man['cells'])}")
    for s in man["strips"]:
        print(f"  {s['name']}: s{s['scan']} v{s['vrsta']} yc={s['yc']} "
              f"{s['px'][0]}x{s['px'][1]}")
    for c in man["cells"]:
        print(f"  {c['name']}: s{c['scan']} v{c['vrsta']} yc={c['yc']} "
              f"{c['px'][0]}x{c['px'][1]}")


if __name__ == "__main__":
    main()
