#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P231 — PROBE-krops: glave + foliacije + prvih-vrstic + dna (finis-kalligrafija?) s57–s63.
Cilj: rešiti-MEJA-1874/75-uganko (s61/s62-konflikt!) — kje je dejanska glava-'Jahr 1875'?"""
from PIL import Image, ImageDraw, ImageFont
import os

T = "/tmp/p231"
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


# P1: glave (zgornjih-18%) s57–s63 — kje je 'Jahr 1875'?
sheet("P1-glave", [
    (f"G{s} glava-zgornji-pas (Jahr-18__?)", s, (0.08, 0.995, 0.0, 0.18)) for s in [57, 58, 59, 60, 61, 62, 63]
])

# P2: foliacije (zgornji-levi-kot) s57–s63 — pričakovano 52–58
sheet("P2-foliacije", [
    (f"F{s} svinčna-cifra-zgornji-levi", s, (0.0, 0.22, 0.0, 0.10)) for s in [57, 58, 59, 60, 61, 62, 63]
])

# P3: prve-2-vrstici (datumi+vas) s61+s62 — November-ali-Januar?
sheet("P3-prvi-vrstici", [
    ("s61-r1+2 (mesec/dan/vas!)", 61, (0.08, 0.70, 0.13, 0.32)),
    ("s62-r1+2 (mesec/dan/vas! + zap!)", 62, (0.08, 0.70, 0.13, 0.32)),
    ("s63-r1 (November-21?-kontrola!)", 63, (0.08, 0.70, 0.13, 0.24)),
])

# P4: dna s57–s62 (finis-Anni-1874-kalligrafija?)
sheet("P4-dna", [
    (f"D{s} spodnji-pas (finis-kalligrafija?)", s, (0.08, 0.995, 0.80, 0.995)) for s in [57, 58, 59, 60, 61, 62]
])

print("PROBE-KROPS-GOTOVI")
