#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P233 — ločilni-krops (×2.6): VSAKIH-18-Griblje-vrstic (L+R) + HISNA-zoom za DUELE.
Izhod: /tmp/p233/krops/sheet-X1/X2/X3.png"""
from PIL import Image, ImageDraw, ImageFont
import os

T = "/tmp/p233"
OUT = f"{T}/krops"
os.makedirs(OUT, exist_ok=True)

try:
    FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
except Exception:
    FONT = ImageFont.load_default()

L = (0.075, 0.56)   # zap+datumi+vas+hisna+ime
R = (0.50, 0.995)   # starši+botra+duhovnik
HIS = (0.24, 0.38)  # hisna-stolpec-zoom

def rowy(scan, r, n, pad=0.010):
    y_a = 0.13 + (r - 1) * (0.88 - 0.13) / n - pad
    y_b = 0.13 + r * (0.88 - 0.13) / n + pad
    return max(0.0, y_a), min(1.0, y_b)

N = {28: 11, 29: 11, 30: 8, 31: 11, 32: 10, 33: 8, 34: 10, 35: 9, 36: 10}

# (label, scan, box, row)
ITEMS = {
 "X1": [
  ("s28-r4 LEVO (GRIBLJE-h16?-Anna-Šilar!-zap-24/22-DUEL!)", 28, L, 4),
  ("s28-r4 DESNO (matec?-botra-Žigon/Korošan!)", 28, R, 4),
  ("s28-r8 LEVO (GRIBLJE-h34-Mathias-Šilar!-zap-28/26!)", 28, L, 8),
  ("s28-r8 DESNO (matec-Deblik!-botra-Prijon+Žega!)", 28, R, 8),
  ("s28-r9 LEVO (GRIBLJE-h37/27-DUEL!-Maria-Hrič/Flurič!)", 28, L, 9),
  ("s28-r9 DESNO (botra-Urc/Urch+Debelak!)", 28, R, 9),
  ("s29-r2 LEVO (GRIBLJE-h13-Marcus-Jakhofič!-zap-33?!) + 'von 20 April' pripis!", 29, L, 2),
  ("s29-r2 DESNO (matec-Gilah!-botra-Legdirc+Jakhofič!)", 29, R, 2),
  ("s29-r7 LEVO (GRIBLJE-h31/33-DUEL!-Johann-Bezdur/Legdirc!-Mai?!)", 29, L, 7),
  ("s29-r7 DESNO (oče+botra-Humar/Hrnič!)", 29, R, 7),
  ("s30-r7 LEVO (GRIBLJE-h49-Antonius-Brodarič!-Juli?!-zap-39?)", 30, L, 7),
  ("s30-r7 DESNO (★★★ matec-Perdisek-PEZDIRC-garble!-boter-Peter-Perdisek!)", 30, R, 7),
 ],
 "X2": [
  ("s31-r7 LEVO (GRIBLJE-h1-Johann-Štefko!-Juli-4!)", 31, L, 7),
  ("s31-r7 DESNO (matec-Zumič!-botra-Zabukovič-×2!)", 31, R, 7),
  ("s31-r11 LEVO (GRIBLJE-h40-DUEL-P232-continuum!-Georg-Ležir/PEZDIRC!-zap-51!)", 31, L, 11),
  ("s31-r11 DESNO (matec-Debelak/Debelič!-botra-Milič!-†12.3.1938-MODRI!)", 31, R, 11),
  ("s32-r4 LEVO (GRIBLJE-h69-Georgius-Glušac/Kuss!-Aug-1!-zap-55!)", 32, L, 4),
  ("s32-r4 DESNO (botra-Brinar+Pavšič!-Maria-Pedice-PEZDIRC?-full-duel!)", 32, R, 4),
  ("s32-r5 LEVO (GRIBLJE-h74?-Mathias-Hambič/Kambič!-Aug-4!-zap-56!)", 32, L, 5),
  ("s32-r5 DESNO (matec-BRODARIČ!-botra-Hübler+Margareta!)", 32, R, 5),
  ("s33-r5 LEVO (GRIBLJE-h8-Maria-Jakopic/Glaspić!-Aug-8!-zap-65!)", 33, L, 5),
  ("s33-r5 DESNO (matec-BRODARIČ!-botra-Podbregar+Anna-DRAGOŠ!)", 33, R, 5),
  ("s33-r8 LEVO (GRIBLJE-h22/42-DUEL!-Michael-Novac/MILEK-DUEL!-Aug-20/21!)", 33, L, 8),
  ("s33-r8 DESNO (matec-PRAZNO/prečrtano!-botra-Brodarič+Zupančič!)", 33, R, 8),
 ],
 "X3": [
  ("s34-r5 LEVO (GRIBLJE-h53-Nicolaus-Pegdire-PEZDIRC!-Oct-3!)", 34, L, 5),
  ("s34-r5 HISNA-zoom (53?)", 34, HIS, 5),
  ("s34-r5 DESNO (botra-Georg-Pegdire+Anna-DRAGOŠ!)", 34, R, 5),
  ("s35-r2 LEVO (Griblje?-Carolina/Ludwig-Sušnik?-row-vs-Michael-Logar-full-DUEL!)", 35, L, 2),
  ("s35-r2 DESNO (matec-Kurent!-botra-Tom+yudin?!-row-vs-Klobučar-full!)", 35, R, 2),
  ("s35-r3 LEVO (GRIBLJE-h37/57-DUEL!-Michael-Lozar-Pustkar-Logar!-Oct-27/28!)", 35, L, 3),
  ("s35-r3 HISNA-zoom (37 vs 57!)", 35, HIS, 3),
  ("s35-r3 DESNO (matec-Staračnik/Staracumić!-botra-Brodaršič+Mihovič/Klobučar!)", 35, R, 3),
  ("s36-r5 LEVO (GRIBLJE-h6-Anna-JAKOFČIČ/JAKOŠA-DUEL!-Nov-20/25?!-zap-92!)", 36, L, 5),
  ("s36-r5 DESNO (matec-Fekša!-botra-Grmič+Anna-DRAGOŠ!)", 36, R, 5),
  ("s36-r6 LEVO (GRIBLJE-h62-Barbara-Guveč/HURE-DUEL!-Krijan-HRIŽAN!-zap-93!)", 36, L, 6),
  ("s36-r6 DESNO (★★★ botra-Mihelč-vs-MILEK-P232-DUEL!+Paulič/Pihlir!)", 36, R, 6),
  ("s36-r7 LEVO (GRIBLJE-h41/11-DUEL!-Katharina/Kaspar-DUEL!-Grmič/KUMIĆ!-zap-94!)", 36, L, 7),
  ("s36-r7 DESNO (matec-DRAGOŠ!-botra-Simec+Jakofčič!)", 36, R, 7),
  ("s36-r1 ZAP-kontrola (88-VIDEN!)", 36, L, 1),
 ],
}

def crop(scan, box, scale=2.6):
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
print("P233-X-KROPS-GOTOVI")
