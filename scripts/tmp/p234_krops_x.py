#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P234 — ločilni-X-krops (×2.6): VSEH-17-GRIBLJE-vrstic 1872 (L+R) + TAIL-kontrole.
Izhod: /tmp/p234/krops/X-P234-1.png + X-P234-2.png"""
from PIL import Image, ImageDraw, ImageFont
import os

T = "/tmp/p234"
OUT = f"{T}/krops"
os.makedirs(OUT, exist_ok=True)

try:
    FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
except Exception:
    FONT = ImageFont.load_default()

L = (0.07, 0.56)   # zap+datumi+vas+hisna+ime
R = (0.50, 0.995)  # starši+botra+duhovnik+opombe
HIS = (0.22, 0.40)

def rowy(scan, r, n, pad=0.010):
    y_a = 0.125 + (r - 1) * (0.90 - 0.125) / n - pad
    y_b = 0.125 + r * (0.90 - 0.125) / n + pad
    return max(0.0, y_a), min(1.0, y_b)

N = {14: 11, 15: 10, 16: 9, 17: 10, 18: 10, 19: 9, 20: 9, 21: 11, 22: 10, 23: 10, 24: 11, 25: 6}

def crop(scan, box, scale=2.6):
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
        c = crop(scan, (x0, x1, y_a, y_b))
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

# X-P234-1: s14–s18 (7-GRIBLJE-vrstic × 2 = 14-kropov + 2-kontrole!)
sheet("X-P234-1", [
    ("A1 s14-r1 LEVO (★★★ 1.-VPIS-1872-GRIBLJE-h11!-Mathias-Zumič?!-restart-z1!-Jänner-5!-DRAGOŠ-matec!)", 14, L, 1),
    ("A1 s14-r1 DESNO (matec-Catharina-DRAGOŠ!-botra-Zumič+Ljustan!)", 14, R, 1),
    ("A1b s14-r1 ZAP-super (z1-KONTROLA-restart!)", 14, (0.05, 0.30), 1),
    ("B1 s15-r3 LEVO (GRIBLJE-h30!-Mathias-Petek?)-Februar-16!)", 15, L, 3),
    ("B1 s15-r3 DESNO (matec-Lakocič!-botra-Stibler+Grovasič!)", 15, R, 3),
    ("C1 s16-r6 LEVO (GRIBLJE-h3!-Maria-HRIŽAN-oče!-mesec-garbage!)", 16, L, 6),
    ("C1 s16-r6 DESNO (botra-ŠIMEC+Hrižan!)", 16, R, 6),
    ("D1 s17-r4 LEVO (GRIBLJE-h44?)-Margareth-KRAUP!-März-27!)", 17, L, 4),
    ("D1 s17-r4 DESNO (matec-HLOBUČAR!-botra-Kraup+Hlobučar!)", 17, R, 4),
    ("D2 s17-r6 LEVO (GRIBLJE-h9!-Georg-Luket!-April-17!)", 17, L, 6),
    ("D2 s17-r6 DESNO (botra-Johann-DRAGOŠ!-+Leško!)", 17, R, 6),
    ("D3 s17-r8 LEVO (GRIBLJE-h38!-Anna-ŠIMEC-oče!-Mai-2!-MODRI-1919?!)", 17, L, 8),
    ("D3 s17-r8 DESNO (matec-Vržan!-botra-Todi+Anna-DRAGOŠ!-MODRI-poroka-†!)", 17, R, 8),
    ("E1 s18-r7 LEVO (GRIBLJE-h24!-Barbara-Princ!-Mai-29!)", 18, L, 7),
    ("E1 s18-r7 DESNO (matec-Ivanc!-botra-Ložek+Horvat!)", 18, R, 7),
    ("E1b s18-r10 ZAP-kontrola (z50-KONTROLA-verige-s18-konec!)", 18, (0.05, 0.30), 10),
])

# X-P234-2: s19–s25 (10-GRIBLJE-vrstic × 2 = 20-kropov + TAIL!)
sheet("X-P234-2", [
    ("F1 s19-r9 LEVO (GRIBLJE-h12!-Johann-PEGDIC-PEZDIRC-GARBLE-★★★!-mesec?!-Juni/July!)", 19, L, 9),
    ("F1 s19-r9 DESNO (matec-Novak!-botra-KLOBUČAR+KRIŽAN!)", 19, R, 9),
    ("G1 s20-r2 LEVO (GRIBLJE-h33!-Mathias-DOBLIČ-DEBLIČ-garble-★★★!-Juli-14!)", 20, L, 2),
    ("G1 s20-r2 DESNO (matec-Husič!-botra-BRODARIČ+Publar!)", 20, R, 2),
    ("G2 s20-r4 LEVO (GRIBLJE-h6!-Maria-Verbič!-Juli-23!)", 20, L, 4),
    ("G2 s20-r4 DESNO (★★★ matec-Anna-PEZDIRC!-boter-Michael-PEZDIRC!-DVOJNI!)", 20, R, 4),
    ("H1 s21-r6 LEVO (★★★ GRIBLJE-h40-continuum-P232/P233!-Katharina-LEZDIRC-PEZDIRC-garble!-Aug-3/4!)", 21, L, 6),
    ("H1 s21-r6 DESNO (matec-Anna-JAKOFČIČ!-botra-SIMEC+KLOBUČAR!)", 21, R, 6),
    ("I1 s23-r3 LEVO (GRIBLJE-h68!-Georg-Potok!-Oct-14!-zap-92?!)...", 23, L, 3),
    ("I1 s23-r3 DESNO (matec-Ložek!-botra-Milhoeluc+Šukovš!)", 23, R, 3),
    ("I2 s23-r8 LEVO (GRIBLJE-h69!-Barbara-Borin!-Nov-9/10!)", 23, L, 8),
    ("I2 s23-r8 DESNO (matec-Podlesnik!-botra-Pogorelec+Hamleri!)", 23, R, 8),
    ("I3 s23-r10 LEVO (GRIBLJE-h7!-Katharina-Foster!-Nov-13!-botra-Anna-PEGHIRC-PEZDIRC-★★★!)", 23, L, 10),
    ("I3 s23-r10 DESNO (matec-Brina!-botra-Šubler+PEGHIRC!)", 23, R, 10),
    ("J1 s24-r4 LEVO (GRIBLJE-h30!-Katharina-Simic!-Nov-22!-matec-JAKOFČIČ!)", 24, L, 4),
    ("J1 s24-r4 DESNO (botra-Hlobuar+Brodnik!)", 24, R, 4),
    ("J2 s24-r7 PREČRTANA-KONTROLA (celotna-vrstica-z-X!-kopija-r4?!)", 24, L, 7),
    ("K1 s25-r2 LEVO (GRIBLJE-h66?)-Maria-Kribžan!-Nov-26/27!-'Morija'-črtano?!)", 25, L, 2),
    ("K1 s25-r2 DESNO (matec-Mihelič!-botra-Drinc+Legbar!)", 25, R, 2),
    ("K2 s25-r5 LEVO (★★★ TAIL-1872-GRIBLJE-h29!-Maria-Mihelič!-Dez-29!-zap-115/116?!)", 25, L, 5),
    ("K2 s25-r5 DESNO (matec-Anna-Kribžan!-botra-Bavča+T!)", 25, R, 5),
    ("K2b s25-r6 ZAP-TAIL-KONTROLA (zadnja-vrstica-1872!-z115?/z116?/prazna?)", 25, (0.05, 0.30), 6),
])
print("P234-X-KROPS-GOTOVI")
