#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P233 — PROBE-krops: glave + foliacije + prve-vrstice + dna s28–s36 (lov MEJA-1872/73!).
LEAD-P232: MEJA-1872/73-PRED-s36 → probe-s28–s36-DESCENDING!
Pričakovana-foliacija-'sken−3': s36='33' (P232!) ... s35='32'-s30='27'-s28='25'.
★★★ POZOR: 2-DUPLIKATA-še-vedno-neznana-lokacija-s1–s35 — zaporedje-LAHKO-skoči!
★★★ 'finis-Anni-1872'-kalligrafija-LAHKO (če-1872-ne-konča-sredinsko!) ALBO
'Initium-anni-Domini-1873'-kalligrafija (PARALELA-P232-'Initium-1874'!)."""
from PIL import Image, ImageDraw, ImageFont
import os

T = "/tmp/p233"
OUT = f"{T}/krops"
os.makedirs(OUT, exist_ok=True)

try:
    FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
except Exception:
    FONT = ImageFont.load_default()


def crop(scan, box, scale=2.0):
    im = Image.open(f"{T}/s{scan}.jpg")
    W, H = im.size
    px = (int(box[0] * W), int(box[2] * H), int(box[1] * W), int(box[3] * H))
    c = im.crop(px)
    c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS)
    return c


def sheet(name, items):
    imgs = []
    for label, scan, box in items:
        c = crop(scan, box)
        lab = Image.new("RGB", (c.width, 34), (20, 20, 20))
        d = ImageDraw.Draw(lab)
        d.text((8, 4), label, fill=(255, 220, 120), font=FONT)
        imgs += [lab, c, Image.new("RGB", (c.width, 10), (255, 255, 255))]
    W = max(i.width for i in imgs)
    H = sum(i.height for i in imgs)
    out = Image.new("RGB", (W, H), (240, 240, 240))
    y = 0
    for i in imgs:
        out.paste(i, (0, y)); y += i.height
    p = f"{OUT}/sheet-{name}.png"
    out.save(p)
    print(f"sheet-{name}: {W}x{H} ({len(items)} kropov)")


S = [28, 29, 30, 31, 32, 33, 34, 35, 36]

# Q1: glave s28–s36 ('Jahr 18__?' — glava-NI-meja-vse-strani-nosijo-glavo!)
sheet("Q1-glave", [
    (f"G{s} glava-zgornji-pas", s, (0.08, 0.995, 0.0, 0.18)) for s in S
])

# Q2: foliacije s28–s36 (pričakovano 'sken−3': 25–33!-POZOR-DUPLIKATI!)
sheet("Q2-foliacije", [
    (f"F{s} svinčna-cifra", s, (0.0, 0.22, 0.0, 0.10)) for s in S
])

# Q3: prva-vrstica (mesec+dan+zap!) s28–s36 — iskamo RESTART-z1-na-Januar-1873 ALBO November-tail!
sheet("Q3-prve-vrstice", [
    (f"s{s}-r1 (mesec/dan/zap/vas!)", s, (0.08, 0.60, 0.12, 0.26)) for s in S
])

# Q4: dna s28–s36 (finis-Anni-1872-kalligrafija? / Initium-1873? / VSOTNA?)
sheet("Q4-dna", [
    (f"D{s} spodnji-pas (finis/Initium/VSOTNA?)", s, (0.08, 0.995, 0.78, 0.995)) for s in S
])

print("P233-PROBE-KROPS-GOTOVI")
