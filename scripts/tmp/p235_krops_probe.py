#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P235 — PROBE-krops: glave + foliacije + prve-vrstice + dna s9–s13 (lov MEJA-1870/71!)
  + ločena-dvojica-listov s1–s8 (UREJANJE-KONCA-LINIJE!).
LEAD-P234: MEJA-1871/72 = ŽE-DOKAZANA-s13/s14 (restart-z1-NA-s14-r1!-X-SUPER!-12.-restart!).
  → probe-s9–s13-DESCENDING! Pričakovana-foliacija-'sken−3': s13='10'-s12='9'-s11='8'-s10='7'-s9='6'! (s14='11'-P234!).
★★★ POZOR: 1-DUPLIKAT-še-vedno-neznana-lokacija-s1–s13! TROJNI-s60=s61=s62-P231 + s28=s29-P234-dokazana!
  → zaporedje-LAHKO-skoči!
★★★ ISKAMO: RESTART-z1-1871 (MEJA-1870/71!-lahko-že-v-s1–s8!-ali-še-dalj-nazaj-—-knjiga-LAHKO-začne-z-1871!-s1-majhna-150KB!)
  + GLAVE-'Jahr 1871'-s9–s13 + TAIL-1871-Dezember + 'finis-Anni-1871'-kalligrafija-LAHKO
  + ALI-'Initium-anni-Domini-1871' (P232-vzorec!) + GLAVE-'Jahr 1870'/'Jahr 1871'-s1–s8 (UREJANJE!)."""
from PIL import Image, ImageDraw, ImageFont
import os

T = "/tmp/p235"
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


S9 = [9, 10, 11, 12, 13]
S1 = [1, 2, 3, 4, 5, 6, 7, 8]

# — A-dvojica: s9–s13 (probe DESCENDING — pričakovano VSE-'Jahr 1871'!)
# Q1: glave s9–s13 ('Jahr 18__?' — pričakovane 'Jahr 1871' 5/5!)
sheet("A-Q1-glave", [
    (f"G{s} glava-zgornji-pas", s, (0.08, 0.995, 0.0, 0.18)) for s in S9
])

# Q2: foliacije s9–s13 (pričakovano 'sken−3': 6–10!-POZOR-DUPLIKAT-s1–s13!)
sheet("A-Q2-foliacije", [
    (f"F{s} svinčna-cifra", s, (0.0, 0.22, 0.0, 0.10)) for s in S9
])

# Q3: prva-vrstica (mesec+dan+zap!) s9–s13 — iskamo MEJA-1870/71 (RESTART-z1!-lahko-že-v-s1–s8!) + TAIL-1871!
sheet("A-Q3-prve-vrstice", [
    (f"s{s}-r1 (mesec/dan/zap/vas!)", s, (0.08, 0.60, 0.12, 0.26)) for s in S9
])

# Q4: dna s9–s13 (finis-Anni-1871-kalligrafija? / Initium-1871? / VSOTNA?)
sheet("A-Q4-dna", [
    (f"D{s} spodnji-pas (finis/Initium/VSOTNA?)", s, (0.08, 0.995, 0.78, 0.995)) for s in S9
])

# — B-dvojica: s1–s8 (UREJANJE-KONCA-LINIJE!-meja-1870/71-LAHKO-tukaj!-ali-knjiga-začne-z-1871!)
# Q1: glave s1–s8 ('Jahr 1870'/'Jahr 1871'/naslovna-stran?)
sheet("B-Q1-glave", [
    (f"G{s} glava-zgornji-pas", s, (0.08, 0.995, 0.0, 0.18)) for s in S1
])

# Q2: foliacije s1–s8 (pričakovano 'sken−3': s13='10' → s9='6' → s8='5'?-...-DUPLIKAT-LAHKO!)
sheet("B-Q2-foliacije", [
    (f"F{s} svinčna-cifra", s, (0.0, 0.22, 0.0, 0.10)) for s in S1
])

# Q3: prva-vrstica s1–s8 — iskamo RESTART-z1-1871 (MEJA-1870/71!) + 1870-tail!
sheet("B-Q3-prve-vrstice", [
    (f"s{s}-r1 (mesec/dan/zap/vas!)", s, (0.08, 0.60, 0.12, 0.26)) for s in S1
])

# Q4: dna s1–s8 (finis-Anni-1870-kalligrafija? / Initium-1871? / VSOTNA?)
sheet("B-Q4-dna", [
    (f"D{s} spodnji-pas (finis/Initium/VSOTNA?)", s, (0.08, 0.995, 0.78, 0.995)) for s in S1
])

print("P235-PROBE-KROPS-GOTOVI")
