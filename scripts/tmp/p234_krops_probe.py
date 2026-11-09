#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P234 — PROBE-krops: glave + foliacije + prve-vrstice + dna s19–s28 (lov MEJA-1871/72 + RESTART-z1-1873!).
LEAD-P233: MEJA-1872/73 = PRED-s28 (ARITMETIČNO!-restart-z1-Jänner-NA-s26/s27!-X-open!) → probe-s19–s28-DESCENDING!
Pričakovana-foliacija-'sken−3': s28='25' (P233!) ... s27='24'-s26='23'-s25='22'-s24='21'-s23='20'-s22='19'-s21='18'-s20='17'-s19='16'.
★★★ POZOR: 2-DUPLIKATA-še-vedno-neznana-lokacija-s1–s27 — zaporedje-LAHKO-skoči! TROJNI-DUPLIKAT-P231-dokazan!
★★★ ISKAMO: RESTART-z1 (Jänner-1873-NA-s26/s27!-ARITMETIČNO!) + GLAVE-'Jahr 1872'-s19–s27 + TAIL-1872-Dezember
  + 'finis-Anni-1872'-kalligrafija (če-1872-ne-konča-sredinsko!) ALI 'Initium-anni-Domini-1873' (PARALELA-P232!)."""
from PIL import Image, ImageDraw, ImageFont
import os

T = "/tmp/p234"
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


S = [19, 20, 21, 22, 23, 24, 25, 26, 27, 28]

# Q1: glave s19–s28 ('Jahr 18__?' — pričakovane 'Jahr 1872' s19–s27 + 'Jahr 1873'-s28-P233!)
sheet("Q1-glave", [
    (f"G{s} glava-zgornji-pas", s, (0.08, 0.995, 0.0, 0.18)) for s in S
])

# Q2: foliacije s19–s28 (pričakovano 'sken−3': 16–25!-POZOR-DUPLIKATI!)
sheet("Q2-foliacije", [
    (f"F{s} svinčna-cifra", s, (0.0, 0.22, 0.0, 0.10)) for s in S
])

# Q3: prva-vrstica (mesec+dan+zap!) s19–s28 — iskamo RESTART-z1-na-Januar (1873-ARITMETIČNO-s26/s27!) + TAIL-1872!
sheet("Q3-prve-vrstice", [
    (f"s{s}-r1 (mesec/dan/zap/vas!)", s, (0.08, 0.60, 0.12, 0.26)) for s in S
])

# Q4: dna s19–s28 (finis-Anni-1872-kalligrafija? / Initium-1873? / VSOTNA?)
sheet("Q4-dna", [
    (f"D{s} spodnji-pas (finis/Initium/VSOTNA?)", s, (0.08, 0.995, 0.78, 0.995)) for s in S
])

print("P234-PROBE-KROPS-GOTOVI")
