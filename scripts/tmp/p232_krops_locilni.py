#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P232 — ločilni-krops (×2.4): kritične Griblje-vrstice + DUELI (meja/hisna/imesa/datumi/meseci!)."""
from PIL import Image, ImageDraw, ImageFont
import os

T = "/tmp/p232"
OUT = f"{T}/krops"
os.makedirs(OUT, exist_ok=True)

try:
    FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
except Exception:
    FONT = ImageFont.load_default()

L = (0.075, 0.56)   # datumi+vas+hisna+ime
R = (0.50, 0.995)   # starši+botra+duhovnik
F = (0.075, 0.995)  # polno
HIS = (0.24, 0.36)  # hisna-stolpec
MES = (0.075, 0.24)  # mesec+dan

def rowy(scan, r, n, pad=0.010):
    y_a = 0.13 + (r - 1) * (0.88 - 0.13) / n - pad
    y_b = 0.13 + r * (0.88 - 0.13) / n + pad
    return max(0.0, y_a), min(1.0, y_b)

N = {37: 8, 38: 8, 39: 9, 40: 11, 42: 9, 43: 9, 44: 9, 45: 8, 46: 8, 47: 8}

ITEMS = {
 "X1": [
  ("s37-r1 POLNO (TAIL-1873!-zap-28/98-DUEL!-Dez-28/29-Kloster-69-Amalia)", 37, F, 1),
  ("s37-r2 POLNO (RESTART-z1!-Gradac-h31-Maria-1./4.!-'Initium-anni-Domini-1874'!)", 37, F, 2),
  ("s37-r2 MESEC-zoom ('Jänner'/'1.'-glava-1874-prelom!)", 37, MES, 2),
  ("s37-r4 LEVO (Jän-14/14-Griblje-h12-Anton)", 37, L, 4),
  ("s37-r4 DESNO (Dragoš/Dragas!-botra-Joseph+Anna-VS-Maria-Jakofčič-DUEL!)", 37, R, 4),
  ("s38-r1 LEVO (Feber-7/8-Griblje-h46-Anna)", 38, L, 1),
  ("s38-r1 DESNO (oče-Hribuar/Gribovc/Hlobučar-DUEL!-½/¾G!-botra-Kruel!)", 38, R, 1),
  ("s38-r1 HISNA-zoom (46!)", 38, HIS, 1),
  ("s38-r3 POLNO (Feber-17/17-h45/25-DUEL!-Anna-Brune/Brime!-Marvin/Horvat!)", 38, F, 3),
  ("s38-r3 HISNA-zoom (45/25!)", 38, HIS, 3),
  ("s39-r3 POLNO (Griblje?-h1?-April-11?-Maria-Juharič-'kajfežl'!-row-read-NI-G!)", 39, F, 3),
  ("s39-r5 DESNO (oče-Strauch/Braučič-DUEL!-Klobučar-matec!)", 39, R, 5),
 ],
 "X2": [
  ("s39-r5 LEVO (mesec-März/April-DUEL!-13/13-h44-Katharina)", 39, L, 5),
  ("s39-r6 LEVO (15/16-h18-Mathias-matec-Janapič/Zunjič-DUEL!)", 39, L, 6),
  ("s39-r6 DESNO (Simec-Hlepec/Klepec!-botra!-opomba-†3.2.1933?)", 39, R, 6),
  ("s39-r8 POLNO (Griblje?-h30-Josefa-Herbavec-row-read-NI-Griblje-DUEL!)", 39, F, 8),
  ("s39-r9 POLNO (April/März-19/19-h48-oče-Klobučar/Kolbl-DUEL!-matec-PEZDIRC/Prahin!-botra-Strauch+Brodarič!)", 39, F, 9),
  ("s40-r3 POLNO (mesec??-h39-oče-Jarrec/Jarmec-VS-Simec-DUEL!-Jakofič-matec!)", 40, F, 3),
  ("s42-r7 LEVO (Aug-15/16-h40/10-DUEL!-Johann)", 42, L, 7),
  ("s42-r7 DESNO (oče-Zupančič/Zgajdire!-matec-Jakofčič/Sathošič!-botra-Brodarič/Milek!)", 42, R, 7),
  ("s43-r4 DESNO (oče-Felk/Zelko!-Hrižan-matec!-botra-Felah/Pilak-Begić/Bizdivec!)", 43, R, 4),
  ("s43-r5 DESNO (Brodarič-oče!-★★★ matec-PEZDIRC/Bizdivec-DUEL!-botra-Deblič!)", 43, R, 5),
  ("s44-r1 DESNO (oče-Jaškovič/Jakofčič-DUEL!-botra-Kelho/'Kef?Ho'!-Anna-Dragos!)", 44, R, 1),
  ("s44-r3 DESNO (★★★ boter-PEZDIRC/Petohne-DUEL!-Jakopič/Jakofčič!-opomba-preseljen-19.3.1882?)", 44, R, 3),
 ],
 "X3": [
  ("s45-r2 LEVO (Nov-1/1-h66-oče-Priban/Pritzau/Grižan/KRIŽAN-DUEL!)", 45, L, 2),
  ("s45-r2 DESNO (Halter? + ★★★ MODRI-†22.10.1930!)", 45, R, 2),
  ("s45-r5 LEVO (Nov-8/9-h32/52/62-TROJNI-DUEL!)", 45, L, 5),
  ("s45-r5 DESNO (Legdire-oče!-matec-Voralt/Vorak/Novak-DUEL!)", 45, R, 5),
  ("s46-r2 DESNO (Hrižan/Križan-oče+matec-×2!-botra-Kump/Pircer!)", 46, R, 2),
  ("s46-r3 LEVO (Nov-28-h40/4-DUEL-P231!-Nicolaus)", 46, L, 3),
  ("s46-r3 DESNO (★★★ oče-PEZDIRC-Pegdire/Perdic!-matec-Pahovič/Jakofčič-DUEL!-†1947-pripis!)", 46, R, 3),
  ("s47-r1 MES+zap-zoom (Dez-26/26-Dobravce-h13-P231-tail-kontrola!)", 47, MES, 1),
  ("s47-r3 HISNA-zoom (22/42-DUEL!)", 47, HIS, 3),
  ("s47-r4 POLNO (ime-Maria/Franziska-DUEL!-★★★ boter-Peter-PEZDIRC/Perchke!-botra-2-Putlar/Turk!)", 47, F, 4),
  ("s47-r7 POLNO (1875-z2-P231-kontrola-1:1!-NEZ-HRIŽAN-DVOJNI!-μh65?)", 47, F, 7),
  ("s46-r4 POLNO (Krasinec-CHICAGO-1949-P231-kontrola!-Mathias-Anton)", 46, F, 4),
 ],
}

def crop(scan, box, scale=2.4):
    im = Image.open(f"{T}/s{scan}.jpg")
    W, H = im.size
    px = (int(box[0] * W), int(box[2] * H), int(box[1] * W), int(box[3] * H))
    c = im.crop(px)
    c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS)
    return c

for sheet, lst in ITEMS.items():
    imgs = []
    for label, scan, (x0, x1), r in lst:
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
    out.save(f"{OUT}/sheet-{sheet}.png")
    print(f"sheet-{sheet}: {W}x{H} ({len(lst)} kropov)")
print("P232-X-KROPS-GOTOVI")
