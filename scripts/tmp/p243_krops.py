#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P243 — klope za pass-2: številčenje (zap.št. stolpec), Pag-koti, Griblje-bloki,
restart-1880 glava + s39-top reconciliacija. Vzorec P242-krop."""
import os, sys
from PIL import Image

OUT = "/tmp/p243/crops"
os.makedirs(OUT, exist_ok=True)

def crop_save(im, box, name, scale=2):
    c = im.crop(box)
    c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS)
    c.save(f"{OUT}/{name}.jpg", quality=93)
    print(f"{name}: box={box} -> {c.size}")

def main():
    jobs = sys.argv[1:] or ["all"]
    im36 = Image.open("/tmp/p243/s36.jpg")
    im37 = Image.open("/tmp/p243/s37.jpg")
    im38 = Image.open("/tmp/p243/s38.jpg")
    im39 = Image.open("/tmp/p243/s39.jpg")

    # --- s36: glava + številčenje ---
    if "all" in jobs or "s36" in jobs:
        crop_save(im36, (0, 0, 2457, 480), "s36-glava", 1.6)          # velika glava 1880
        crop_save(im36, (0, 0, 700, 1800), "s36-stolpec-L", 1.8)      # levi rob (zap št.)
        crop_save(im36, (1000, 0, 2457, 1800), "s36-desna", 1.4)      # desna polovica
        # bloki: v2 (Griblje 25/18) + v3 (Griblje 10/11)
        crop_save(im36, (700, 500, 2457, 1000), "s36-blok-v2v3", 1.8)

    # --- s37: številčenje + v14 Pegdirec ---
    if "all" in jobs or "s37" in jobs:
        crop_save(im37, (0, 0, 700, 1800), "s37-stolpec-L", 1.8)
        crop_save(im37, (0, 0, 2457, 300), "s37-glava", 1.6)
        crop_save(im37, (1000, 1100, 2457, 1800), "s37-v13v14", 1.9)  # v13+v14 vrstice

    # --- s38: tail + Pag-kot + v20 Pegdirec ---
    if "all" in jobs or "s38" in jobs:
        crop_save(im38, (0, 0, 700, 1800), "s38-stolpec-L", 1.8)
        crop_save(im38, (1800, 1550, 2458, 1800), "s38-pag-kot", 3.0)  # Pag. NN desno-zgoraj? + spodaj
        crop_save(im38, (0, 1550, 700, 1800), "s38-pag-kot-L", 3.0)    # Pag levo-spodaj
        crop_save(im38, (1000, 1500, 2457, 1800), "s38-v20", 2.2)      # v20 Pegdirec
        crop_save(im38, (0, 1500, 2458, 1800), "s38-dno-vsote", 1.6)   # rezane vsote

    # --- s39: top reconciliacija (letnica 1881 nad vrsto 1) ---
    if "all" in jobs or "s39" in jobs:
        crop_save(im39, (0, 0, 2457, 420), "s39-top-recon", 1.8)

    print("CROPS DONE")

if __name__ == "__main__":
    main()
