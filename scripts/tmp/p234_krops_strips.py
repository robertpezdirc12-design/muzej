#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P234 — ZAP-STOLPEC-STRIPES (×3): vertikalni-stolpec zaporednih-številk s19, s25, s26, s27, s28
+ s28-r1-HISNA-zoom (misterij-'28'-vs-'11'!) — GROUND-TRUTH za zap-verige!"""
from PIL import Image, ImageDraw, ImageFont
import os

T = "/tmp/p234"
OUT = f"{T}/krops"
os.makedirs(OUT, exist_ok=True)

try:
    FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
except Exception:
    FONT = ImageFont.load_default()

def strip(scan, x0=0.045, x1=0.235, y0=0.11, y1=0.93, scale=3.0):
    im = Image.open(f"{T}/s{scan}.jpg")
    W, H = im.size
    px = (int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H))
    c = im.crop(px)
    c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS)
    return c

def sheet(name, items):
    imgs = []
    for label, scan in items:
        c = strip(scan)
        lab = Image.new("RGB", (c.width, 36), (20, 20, 20))
        d = ImageDraw.Draw(lab)
        d.text((8, 5), label, fill=(255, 220, 120), font=FONT)
        imgs += [lab, c, Image.new("RGB", (c.width, 12), (255, 255, 255))]
    W = max(i.width for i in imgs)
    H = sum(i.height for i in imgs)
    out = Image.new("RGB", (W, H), (240, 240, 240))
    y = 0
    for i in imgs:
        out.paste(i, (0, y)); y += i.height
    out.save(f"{OUT}/{name}.png")
    print(f"{name}: {W}x{H} ({len(items)} stripov)")

# zap-stolpec (levo!) celotne-višine-tabele — vsaka-številka-vidna-v-zaporedju!
sheet("ZAP-STRIPS", [
    ("STRIP-s19 (zap-stolpec-celot!-pričakovano-z1–z9-ALI-z51–z59?!)", 19),
    ("STRIP-s25 (zap!-TAIL-1872!-6-vrstic!)", 25),
    ("STRIP-s26 (zap!-RESTART-z1-1873?-ALI-Dez-1872?!-11-vrstic!)", 26),
    ("STRIP-s27 (zap!-z1–z10-model-vs-z12–z21!-10-vrstic!)", 27),
    ("STRIP-s28 (zap!-z11–z21-P233-MODEL!-11-vrstic!)", 28),
])

# s28-r1 SUPER-zoom (zap + hišna + dan) — '28' vs '11' vs '20' misterij!
im = Image.open(f"{T}/s28.jpg")
W, H = im.size
c = im.crop((int(0.05 * W), int(0.125 * H), int(0.42 * W), int(0.21 * H)))
c = c.resize((int(c.width * 4.0), int(c.height * 4.0)), Image.LANCZOS)
c.save(f"{OUT}/S28R1-SUPER.png")
print(f"S28R1-SUPER: {c.width}x{c.height}")

# s26-r1 SUPER-zoom — restart-z1 kontrola!
im = Image.open(f"{T}/s26.jpg")
c = im.crop((int(0.05 * W), int(0.125 * H), int(0.42 * W), int(0.21 * H)))
c = c.resize((int(c.width * 4.0), int(c.height * 4.0)), Image.LANCZOS)
c.save(f"{OUT}/S26R1-SUPER.png")
print(f"S26R1-SUPER: {c.width}x{c.height}")
print("P234-ZAP-STRIPS-GOTOVI")
