#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P244 — kropi za pass-2/3: Griblje-bloki (v1-s27, v2-s27, v?-s28 Pezdirc-50,
v12-s30 Požeh-21/Princ-24, v20/v21-s32 Tome/Pegdirec-42-Križan-63, v24/v25-s33
Kralj-17/Tomc-16), številčenje (s27 restart + s28 zap.št.), glave (ponavljanje),
tail-s35 reconciliacija (31–33) + pag-koti. Vzorec P242/P243-krop."""
import os, sys
from PIL import Image

OUT = "/tmp/p244/crops"
os.makedirs(OUT, exist_ok=True)

def crop_save(im, box, name, scale=2):
    c = im.crop(box)
    c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS)
    c.save(f"{OUT}/{name}.jpg", quality=93)
    print(f"{name}: box={box} -> {c.size}")

def main():
    jobs = sys.argv[1:] or ["all"]
    ims = {s: Image.open(f"/tmp/p244/s{s}.jpg") for s in [26, 27, 28, 29, 30, 31, 32, 33, 34, 35]}

    # --- s26: tail-1878 meja (P244 potrditev s26→s27!) ---
    if "all" in jobs or "s26" in jobs:
        crop_save(ims[26], (0, 1000, 2457, 1800), "s26-dno-tail1878", 1.5)

    # --- s27: RESTART-1879 glava + v1 (Helepec h16 × Jurejevič h10) + v2 (Stepanič × Rus) ---
    if "all" in jobs or "s27" in jobs:
        crop_save(ims[27], (0, 0, 2457, 500), "s27-glava-1879", 1.7)
        crop_save(ims[27], (0, 300, 2457, 800), "s27-v1", 2.0)
        crop_save(ims[27], (0, 700, 2457, 1250), "s27-v2", 2.0)
        crop_save(ims[27], (0, 0, 700, 1800), "s27-stolpec-L", 1.8)

    # --- s28: vpisi 3–8 (Pezdirc h50 × Škuncelj h44 kandidat) + številčenje ---
    if "all" in jobs or "s28" in jobs:
        crop_save(ims[28], (0, 0, 700, 1800), "s28-stolpec-L", 1.9)
        crop_save(ims[28], (0, 300, 2457, 1000), "s28-vrste-zg", 1.8)
        crop_save(ims[28], (0, 1000, 2457, 1750), "s28-vrste-sp", 1.8)

    # --- s29: vpisi 9–11 (datum razrešnica Febr-12 vs Jän) ---
    if "all" in jobs or "s29" in jobs:
        crop_save(ims[29], (0, 300, 1228, 1750), "s29-L-vse", 1.7)

    # --- s30: vpisi 12–14 (v12 Požeh h21 × Princ h24; datum 29-Jan zmeda) ---
    if "all" in jobs or "s30" in jobs:
        crop_save(ims[30], (0, 300, 1228, 1200), "s30-L-zg-v12v13", 1.9)
        crop_save(ims[30], (0, 1000, 2457, 1750), "s30-v14-dno", 1.7)
        crop_save(ims[30], (0, 0, 2457, 420), "s30-glava", 1.7)

    # --- s31: vpisi 15–18 ---
    if "all" in jobs or "s31" in jobs:
        crop_save(ims[31], (0, 0, 2457, 420), "s31-glava", 1.6)
        crop_save(ims[31], (0, 300, 1228, 1750), "s31-L-vse", 1.6)

    # --- s32: v20 (Tome h16?) + v21 (Pegdirec h42 × Križan h63 ★★★) + glava ---
    if "all" in jobs or "s32" in jobs:
        crop_save(ims[32], (0, 0, 2457, 450), "s32-glava", 1.7)
        crop_save(ims[32], (0, 400, 2457, 1100), "s32-v20", 2.0)
        crop_save(ims[32], (0, 1000, 2457, 1750), "s32-v21", 2.2)

    # --- s33: v24 (Kralj h17) + v25 (Tomc h16?) + glava ---
    if "all" in jobs or "s33" in jobs:
        crop_save(ims[33], (0, 0, 2457, 450), "s33-glava", 1.7)
        crop_save(ims[33], (0, 950, 2457, 1400), "s33-v24", 2.1)
        crop_save(ims[33], (0, 1350, 2457, 1800), "s33-v25", 2.1)

    # --- s34: glava (ponovitev) + datum stolpec ---
    if "all" in jobs or "s34" in jobs:
        crop_save(ims[34], (0, 0, 2457, 450), "s34-glava", 1.6)
        crop_save(ims[34], (0, 300, 700, 1750), "s34-datumi", 2.0)

    # --- s35: tail-31–33 reconciliacija (P243-1:1) + pag-kot ---
    if "all" in jobs or "s35" in jobs:
        crop_save(ims[35], (0, 0, 2457, 700), "s35-top-tail", 1.8)
        crop_save(ims[35], (1800, 0, 2457, 300), "s35-pag-kg", 3.0)

    print("DONE")

if __name__ == "__main__":
    main()
