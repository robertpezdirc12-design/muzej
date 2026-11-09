#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P234 — VERIŽNI-X-krops: VSAKIH-vrstic s26 (11) + s27 (10) — zap+mesec+dan zoom ×3.2
UGANKA: s26 = z1–z11-Jänner-Feber (celost+SUPER!) ALI Dez-1872-tail (P233-model!)?!
        s27 = z1–z10 (X-E/E2!-P233-model!) ALI z12–z21 (celost!)?!"""
from PIL import Image, ImageDraw, ImageFont
import os

T = "/tmp/p234"
OUT = f"{T}/krops"
os.makedirs(OUT, exist_ok=True)

try:
    FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
except Exception:
    FONT = ImageFont.load_default()

ZAPL = (0.05, 0.40)   # zap+mesec+dan (+del vasi)

def rowy(scan, r, n, pad=0.006):
    y_a = 0.125 + (r - 1) * (0.90 - 0.125) / n - pad
    y_b = 0.125 + r * (0.90 - 0.125) / n + pad
    return max(0.0, y_a), min(1.0, y_b)

def crop(scan, box, scale=3.2):
    im = Image.open(f"{T}/s{scan}.jpg")
    W, H = im.size
    px = (int(box[0] * W), int(box[2] * H), int(box[1] * W), int(box[3] * H))
    c = im.crop(px)
    c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS)
    return c

def sheet(name, items):
    imgs = []
    for label, scan, r, n in items:
        y_a, y_b = rowy(scan, r, n)
        c = crop(scan, (ZAPL[0], ZAPL[1], y_a, y_b))
        lab = Image.new("RGB", (c.width, 28), (20, 20, 20))
        d = ImageDraw.Draw(lab)
        d.text((8, 3), label, fill=(255, 220, 120), font=FONT)
        imgs += [lab, c, Image.new("RGB", (c.width, 7), (255, 255, 255))]
    W = max(i.width for i in imgs)
    H = sum(i.height for i in imgs)
    out = Image.new("RGB", (W, H), (240, 240, 240))
    y = 0
    for i in imgs:
        out.paste(i, (0, y)); y += i.height
    out.save(f"{OUT}/{name}.png")
    print(f"{name}: {W}x{H} ({len(items)} kropov)")

items = []
for r in range(1, 12):
    items.append((f"s26-r{r} (zap+mesec+dan!)", 26, r, 11))
for r in range(1, 11):
    items.append((f"s27-r{r} (zap+mesec+dan!)", 27, r, 10))
sheet("VERIGA-26-27", items)
print("P234-VERIGA-KROPS-GOTOVI")
