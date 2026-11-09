#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P235 — X-DECISIVE krops: aritmetična-sidra (restart-z1 + post-dup + DVOJČKI + PREČRTANI + TAIL-VERIGA + PEZDIRC!).
LEAD-P234: MEJA-1870/71-REŠENA-probe (knjiga-se-začne-z-1871!-s3=s4-DUPLIKAT-fol-1!) → X-potrditve-1:1:
  (1) s3-r1 = z1-RESTART-'1'-SUPER (kontrola!-Jänner-3-KRASINEC!) + (2) s4-r1 = z1-DUPLIKAT-'1' (s3=s4!)
  + (3) s5-r1 = z9-'9'-POST-DUPLIKAT-continuacija! + (4) s7-r7/r8 = z37/z38-PREČRTANI-DVOJNI!
  + (5) s10-r8/r9 = z72/z73-DVOJČKI-'Zwillings'! + (6) s11-r7 = z81-'81'-+'Peter-Pezdirc'-EKSPPLICITNO!
  + (7) s13-r1 = z97-'97' + (8) s13-r12 = z108-'108'-TAIL-VERIGA! (+ s13-r2 = z98-GRIBLJE-kontekst!)."""
from PIL import Image, ImageDraw, ImageFont
import os

T = "/tmp/p235"
OUT = f"{T}/krops"
os.makedirs(OUT, exist_ok=True)

try:
    FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
except Exception:
    FONT = ImageFont.load_default()


def crop(scan, box, scale=2.6):
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


# Sheet-X1: RESTART + DUPLIKAT + POST-DUP (z1-s3r1 + z1-s4r1 + z9-s5r1) — zap-stolpec + celotna-vrstica
sheet("X1-restart-dup", [
    ("s3-r1 = z1? (RESTART-'1'!-Jänner-3!)", 3, (0.03, 0.55, 0.115, 0.215)),
    ("s4-r1 = z1? (DUPLIKAT-'1'!-ista-stran!)", 4, (0.03, 0.55, 0.115, 0.215)),
    ("s5-r1 = z9? (POST-DUPLIKAT-'9'!-Jänner-24!)", 5, (0.03, 0.55, 0.115, 0.215)),
])

# Sheet-X2: TAIL-VERIGA (s13: r1=z97? + r2=z98-GRIBLJE! + r12=z108-TAIL!) + mesec-November/Dezember
sheet("X2-tail-veriga", [
    ("s13-r1 = z97? (November-16!)", 13, (0.03, 0.55, 0.115, 0.205)),
    ("s13-r2 = z98? (GRIBLJE-h6!-Maria!)", 13, (0.03, 0.55, 0.195, 0.285)),
    ("s13-r12 = z108? (TAIL-Dez-31-Otok!)", 13, (0.03, 0.55, 0.795, 0.885)),
])

# Sheet-X3: DVOJČKI z72/z73 (s10 r8/r9) + PREČRTANI z37/z38 (s7 r7/r8)
sheet("X3-dvojcki-precrtani", [
    ("s10-r8 = z72? (DVOJČEK-'Zwillings'!-Georg!)", 10, (0.03, 0.60, 0.615, 0.705)),
    ("s10-r9 = z73? (DVOJČEK-'ib.'!-Catharina!)", 10, (0.03, 0.60, 0.695, 0.785)),
    ("s7-r7 = z37? (PREČRTAN?-Johan!)", 7, (0.03, 0.60, 0.595, 0.685)),
    ("s7-r8 = z38? (PREČRTAN?-Maria!)", 7, (0.03, 0.60, 0.675, 0.765)),
])

# Sheet-X4: z81-'81'-'Peter-Pezdirc'-EKSPPLICITNO (s11-r7!-Griblje-h28!) + z80-'80' (s11-r6-Klobučar!)
sheet("X4-pezdirc-klobucar", [
    ("s11-r6 = z80? (Griblje-h48-KLOBUČAR-oče!)", 11, (0.03, 0.60, 0.485, 0.575)),
    ("s11-r7 = z81? (Griblje-h28-'Peter-Pezdirc'-EKSPPLICITNO!)", 11, (0.03, 0.60, 0.565, 0.655)),
])

print("P235-X-KROPS-GOTOVI")
