#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P234 — DECISIVE X-krops (×2.8): zap-veriga-kalibracija s19–s31!
Nasprotja-celostanskih-branj: s19-r1 (z1-probe vs z51-celost!), s26-r1 (restart-z1? Dez-1872?),
s27-r1/r10 (z1/z10-model vs z12/z21-celost!), s28-r1 (z11-P233-model vs z22-celost-chain!),
s29-r11 (z32-pancer!), s30-r8 (z40-full!), s31-r1 (z41!) — X-ANKA-z51-s31-r11-P233-POTRJEN!
★★★ ODLOČA: (A) ali-1872-starta-NA-s19-r1 (z1!-okno-s19–s25=66-vrstic!) ALBO-PRED-s19 (z51!-okno-s13–s25!-116+!);
  (B) ali-P233-model-s28=11–21-STOJI (s27=z1–z10, s26=1872-Dez-tail!) ALBO je-RESTART-z1-NA-s26-r1 (s26=z1–z11, s27=z12–z21!)."""
from PIL import Image, ImageDraw, ImageFont
import os

T = "/tmp/p234"
OUT = f"{T}/krops"
os.makedirs(OUT, exist_ok=True)

try:
    FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
except Exception:
    FONT = ImageFont.load_default()

# vrstic-na-sken (celostanska- branja; P233: s28=11!)
N = {19: 9, 20: 9, 21: 11, 22: 10, 23: 10, 24: 11, 25: 6, 26: 11, 27: 10, 28: 11, 29: 11, 30: 8, 31: 11}

ZAPL = (0.07, 0.34)   # zap+mesec+dan levo-zoom
L = (0.07, 0.56)
R = (0.50, 0.995)

def rowy(scan, r, n, pad=0.010):
    y_a = 0.13 + (r - 1) * (0.88 - 0.13) / n - pad
    y_b = 0.13 + r * (0.88 - 0.13) / n + pad
    return max(0.0, y_a), min(1.0, y_b)

def crop(scan, box, scale=2.8):
    im = Image.open(f"{T}/s{scan}.jpg")
    W, H = im.size
    px = (int(box[0] * W), int(box[2] * H), int(box[1] * W), int(box[3] * H))
    c = im.crop(px)
    c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS)
    return c

def sheet(name, items):
    imgs = []
    for label, scan, (x0, x1), r in items:
        y_a, y_b = rowy(scan, r, N[scan])
        box = (x0, x1, y_a, y_b)
        c = crop(scan, box)
        lab = Image.new("RGB", (c.width, 30), (20, 20, 20))
        d = ImageDraw.Draw(lab)
        d.text((8, 3), label, fill=(255, 220, 120), font=FONT)
        imgs += [lab, c, Image.new("RGB", (c.width, 8), (255, 255, 255))]
    W = max(i.width for i in imgs)
    H = sum(i.height for i in imgs)
    out = Image.new("RGB", (W, H), (240, 240, 240))
    y = 0
    for i in imgs:
        out.paste(i, (0, y)); y += i.height
    out.save(f"{OUT}/{name}.png")
    print(f"{name}: {W}x{H} ({len(items)} kropov)")

# X-DECISIVE sheet — zap-kontrole na 2.8× (LEVI-DEL: zap+mesec+dan!)
sheet("X-DECISIVE", [
    ("A s19-r1 ZAP (z1-restart? vs z51?!-Jänner-Gradac-Maria!)", 19, ZAPL, 1),
    ("A2 s19-r9 ZAP (z9? vs z59!)", 19, ZAPL, 9),
    ("B s20-r1 ZAP (z10? vs z60!-Juli!)", 20, ZAPL, 1),
    ("C s25-r4 ZAP (Dez-31!-z114?)-LEVO", 25, L, 4),
    ("C2 s25-r5 ZAP (Dez-29-Griblje-h29!-TAIL?)-LEVO", 25, L, 5),
    ("D s26-r1 ZAP (restart-z1-1873?? vs Dez-1872-tail??-Jänner-Gradac-Anna!)", 26, ZAPL, 1),
    ("D2 s26-r11 ZAP (z11? vs z11-Dez?!-Feber-Geriče-Maria!)", 26, ZAPL, 11),
    ("E s27-r1 ZAP (z1-P233-model! vs z12!-Podzemelj-Josef-h28!)", 27, ZAPL, 1),
    ("E2 s27-r10 ZAP (z10-P233-model! vs z21!-März-Zemelj!)", 27, ZAPL, 10),
    ("F s28-r1 ZAP (★★★ z11-P233-MODEL! vs z22-celost!-März-3-Podzemelj-Mathildis!)", 28, ZAPL, 1),
    ("F2 s28-r11 ZAP (z21-P233-model!-veriga!)", 28, ZAPL, 11),
    ("G s29-r1 ZAP (z22-P233-model! vs z33!)", 29, ZAPL, 1),
    ("G2 s29-r11 ZAP (★★★ z32-P233-veriga! vs z43!)", 29, ZAPL, 11),
    ("H s30-r1 ZAP (z33-P233! vs z44!)", 30, ZAPL, 1),
    ("H2 s30-r8 ZAP (★★★ z40-full-P233! vs z51!)", 30, ZAPL, 8),
    ("I s31-r1 ZAP (z41-P233! vs z52!)", 31, ZAPL, 1),
    ("I2 s31-r11 ZAP (★★★ z51-X-ANKA-P233-POTRJEN!-kontrola!)", 31, ZAPL, 11),
])
print("P234-X-DECISIVE-GOTOVI")
