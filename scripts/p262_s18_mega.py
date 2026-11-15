#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P262 — s18 odločilni mega-zoomi: r1 Haus-Nr + prečrtan-ort, datumi 6x, r4-ort, starosti, r6-bride-Nr."""
import subprocess

ROOT = "/home/z/my-project"
SRC = f"{ROOT}/research/issue17/p261-work/s18.jpg"
OUT = f"{ROOT}/research/issue17/p262-work"

crops = [
    # r1 Wohnort+Haus-Nr (prečrtan garble + številka) — 5x
    ("mz_r1_ort_nr", 240, 255, 470, 425, 5),
    # r1 datum 6x
    ("mz_r1_date", 90, 255, 250, 425, 6),
    # r2 datum 6x
    ("mz_r2_date", 90, 415, 250, 575, 6),
    # r4 Wohnort (prečrtan) + Haus-Nr 31 — 5x
    ("mz_r4_ort_nr", 240, 715, 470, 880, 5),
    # r4 datum 6x
    ("mz_r4_date", 90, 715, 250, 880, 6),
    # r6 datum 6x
    ("mz_r6_date", 90, 1025, 250, 1185, 6),
    # r7 datum 6x
    ("mz_r7_date", 90, 1175, 250, 1340, 6),
    # r5 starost+ženin-celica 4x (age 33|22?)
    ("mz_r5_age", 480, 870, 780, 1035, 4),
    # r6 starost 4x (29|39?)
    ("mz_r6_age", 480, 1025, 780, 1185, 4),
    # r6 bride Haus-Nr (32|23?) — 5x
    ("mz_r6_bride_nr", 940, 1025, 1146, 1185, 5),
    # r1 starost (25?) + r1 bride Haus-Nr 36 5x
    ("mz_r1_age", 480, 255, 780, 425, 4),
    ("mz_r1_bride_nr", 860, 255, 1146, 425, 5),
    # r3 groom-annotacija "güblest Beje" 5x
    ("mz_r3_annot", 300, 565, 700, 725, 4),
    # r7 bride "Agnes Haljha" + r7 bride annot 4x
    ("mz_r7_bride", 860, 1175, 1146, 1340, 5),
]
for tag, x0, y0, x1, y1, s in crops:
    subprocess.run(["python3", "-c",
        f"from PIL import Image; im=Image.open('{SRC}'); "
        f"c=im.crop(({x0},{y0},{x1},{y1})); c.resize((int(c.width*{s}),int(c.height*{s})),Image.LANCZOS).save('{OUT}/{tag}.png')"], check=True)

print("mega-zooms OK:", len(crops))
