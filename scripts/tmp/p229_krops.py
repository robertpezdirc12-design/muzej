#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P229 — MAX-krop montażni sheet-i (VIZUALNO-arhivar-metodologija P228!).
Sheet-i = vertikalno-složeni-krop-i (×1.8-lanczos) z labelami. Izhod: /tmp/p229/krops/sheet-*.png"""
from PIL import Image, ImageDraw, ImageFont

T = "/tmp/p229"
OUT = f"{T}/krops"
import os
os.makedirs(OUT, exist_ok=True)

# vrstic-na-stran (iz VIZUALNO-branja!)
ROWS = {78: 6, 79: 7, 80: 8, 81: 9, 82: 7, 83: 8, 84: 9, 85: 7, 86: 8, 87: 8, 88: 7, 89: 6, 90: 7, 91: 6, 92: 6}
Y0, Y1 = 0.135, 0.875  # tabelarna-območja (pod-glavo, nad-dnom)


def rowbox(scan, r, xr=(0.10, 0.56), pad=0.012):
    """vrni (x0,x1,y0,y1) frakcije za vrstico r (1-based) na skenu."""
    n = ROWS[scan]
    y_a, y_b = Y0 + (r - 1) * (Y1 - Y0) / n - pad, Y0 + r * (Y1 - Y0) / n + pad
    return xr[0], xr[1], max(0, y_a), min(1.0, y_b)


def rowsbox(scan, r1, r2, xr=(0.10, 0.56)):
    n = ROWS[scan]
    y_a = Y0 + (r1 - 1) * (Y1 - Y0) / n - 0.012
    y_b = Y0 + r2 * (Y1 - Y0) / n + 0.012
    return xr[0], xr[1], y_a, y_b


try:
    FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
except Exception:
    FONT = ImageFont.load_default()


def crop(scan, box, scale=1.8):
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


L = (0.10, 0.56)   # datumi+vas+hišna+ime
R = (0.50, 0.995)  # starši+botra+duhovnik
FULL = (0.10, 0.995)

# A: Griblje s79–s82
sheet("A", [
 ("A1 s79-r3 z8 Griblje-h37 LEVO (PEZDIRE-oce+JAKOF-C-matec)", 79, rowbox(79, 3, L)),
 ("A1b s79-r3 z8 DESNO (botra MILEK+PEZDIRE + MODRI-MATCH-37 + Roggja)", 79, rowbox(79, 3, R)),
 ("A2 s80-r1 z13 Griblje-h6 LEVO (JAKOF-C-oce + MODRI-dolg)", 80, rowbox(80, 1, L)),
 ("A2b s80-r1 z13 DESNO", 80, rowbox(80, 1, R)),
 ("A3 s80-r3 z15 Griblje-h13 LEVO (JAKOF-C-oce + Feb28>Mar1)", 80, rowbox(80, 3, L)),
 ("A3b s80-r3 z15 DESNO (PEZDIRE-boter)", 80, rowbox(80, 3, R)),
 ("A4 s81-r2 z22 Griblje-h36 PRE-CRTANA-X LEVO", 81, rowbox(81, 2, L)),
 ("A4b s81-r2 z22 DESNO (SIMEC-matec + BRODARI-C)", 81, rowbox(81, 2, R)),
 ("A5 s81-r5 z25 Griblje-h65 LEVO (MILEK-oce)", 81, rowbox(81, 5, L)),
 ("A5b s81-r5 z25 DESNO (PEZDIRE-boter)", 81, rowbox(81, 5, R)),
])

# B: Griblje s82–s86
sheet("B", [
 ("B1 s82-r5 z34 Griblje-h74 LEVO (HAMBI-C-oce)", 82, rowbox(82, 5, L)),
 ("B1b s82-r5 z34 DESNO (BRODARI-C+MILEK + Roggja)", 82, rowbox(82, 5, R)),
 ("B2 s85-r3 z56 Griblje-h6 LEVO (KLOBU-CAR-oce + MILEK-matec + krnilo!)", 85, rowbox(85, 3, L)),
 ("B2b s85-r3 z56 DESNO (JAKOF-C-boter)", 85, rowbox(85, 3, R)),
 ("B3 s86-r1 z61 Griblje-h7 LEVO", 86, rowbox(86, 1, L)),
 ("B3b s86-r1 z61 DESNO (SIMEC-boter)", 86, rowbox(86, 1, R)),
 ("B4 s86-r7+8 z67/68 Griblje-h14 DVOJ-CKI LEVO (bracket!)", 86, rowsbox(86, 7, 8, L)),
 ("B4b s86-r7+8 z67/68 DESNO (PEZDURE + JAKOF-C+HAMBI-C)", 86, rowsbox(86, 7, 8, R)),
])

# C: Griblje s88–s89
sheet("C", [
 ("C1 s88-r1 z77 Griblje-h2 LEVO (JAKOF-C-matec)", 88, rowbox(88, 1, L)),
 ("C1b s88-r1 z77 DESNO (KLOBU-CAR)", 88, rowbox(88, 1, R)),
 ("C2 s88-r3 z79 Griblje-h35 LEVO (HRI-AN-oce)", 88, rowbox(88, 3, L)),
 ("C2b s88-r3 z79 DESNO", 88, rowbox(88, 3, R)),
 ("C3 s89-r1 z84 Griblje-h20 LEVO (PEZDIRE-oce)", 89, rowbox(89, 1, L)),
 ("C3b s89-r1 z84 DESNO (BRODARI-C+MILEK)", 89, rowbox(89, 1, R)),
 ("C4 s89-r2 z85 Griblje-h9 LEVO (JAKOF-C x2!)", 89, rowbox(89, 2, L)),
 ("C4b s89-r2 z85 DESNO (DRAGO-S)", 89, rowbox(89, 2, R)),
 ("C5 s89-r6 z89 Griblje-h40 LEVO (PEZDI-C-oce + Nov31/1-DUEL!)", 89, rowbox(89, 6, L)),
 ("C5b s89-r6 z89 DESNO (JAKOF-C-matec + HLOBU-CAR)", 89, rowbox(89, 6, R)),
])

# D: Griblje s90–s92
sheet("D", [
 ("D1 s90-r5 z94 Griblje-h49-DUEL LEVO (BRODARI-C-oce + krnilo-6.3.1945!)", 90, rowbox(90, 5, L)),
 ("D1b s90-r5 z94 DESNO", 90, rowbox(90, 5, R)),
 ("D2 s90-r6 z95 Griblje-h78 LEVO", 90, rowbox(90, 6, L)),
 ("D2b s90-r6 z95 DESNO (BRODARI-C)", 90, rowbox(90, 6, R)),
 ("D3 s91-r3 z99 Griblje-h3 LEVO (HRI-AN x2)", 91, rowbox(91, 3, L)),
 ("D3b s91-r3 z99 DESNO (SIMEC-boter)", 91, rowbox(91, 3, R)),
 ("D4 s91-r5 z101 Griblje-h34-DUEL LEVO (SKALA-S + DEBLI-C)", 91, rowbox(91, 5, L)),
 ("D4b s91-r5 z101 DESNO", 91, rowbox(91, 5, R)),
 ("D5 s92-r4 z106 Griblje-h33 LEVO (DEBLI-C + HUSI-C)", 92, rowbox(92, 4, L)),
 ("D5b s92-r4 z106 DESNO (BRODARI-C+PEZDIRE!-P228-tail)", 92, rowbox(92, 4, R)),
])

# E: MEJA + restart-z1 + Nov31-DUEL
n78 = ROWS[78]
sheet("E", [
 ("E1 s78 TAIL-1876-r1 (Dobravce Dez-24/26 + glava-1876)", 78, rowbox(78, 1, FULL)),
 ("E2 s78 INCIPIT-ANNUS-DOMINI-1877 MEJA (sredina!)", 78, (0.10, 0.995, 0.13 + (Y1 - Y0) / n78 * 0.9, 0.13 + (Y1 - Y0) / n78 * 1.75)),
 ("E3 s78 z1 RESTART Jänner-9/10 Zemelj-h20 (JAKOF-C-matec!)", 78, rowbox(78, 3, FULL)),
 ("E4 s89-r6 DATUM-DUEL '31/1' (Nov-31-ne-obstaja!)", 89, rowbox(89, 6, (0.11, 0.42))),
 ("E5 s90-r1 DATUM-DUEL '31/1' + mesec-NNovember", 90, rowbox(90, 1, (0.11, 0.42))),
])

# F: todtgeboren-garbles + nezakonski
sheet("F", [
 ("F1 s83-r5 z41 Krasine-h1 IME-GARBLE 'Nurlygabuni-t' (P228-z28-PARALELA!)", 83, rowbox(83, 5, L)),
 ("F2 s83-r6 z42 Podzemelj IME-GARBLE + oce-Misnik", 83, rowbox(83, 6, L)),
 ("F3 s83-r2 z38 Krasine-h46 NEZAKONSKI (oce-PRAZEN-dash!)", 83, rowbox(83, 2, L)),
 ("F4 s83-r7 z43 Certovi-e-h14 NEZAKONSKI (oce-PRAZEN!)", 83, rowbox(83, 7, L)),
 ("F5 s83-r8 z44 Vranovi-e-h20 X-open-mati-only", 83, rowbox(83, 8, L)),
 ("F6 s86-r5 z65 Kloster-h13 IME-GARBLE + botra/duhovnik-PRAZNA", 86, rowbox(86, 5, L)),
])

# G: DVOJČKI-brackets + hišni-DUELI + rojen-krsten
sheet("G", [
 ("G1 s87-r4+5 z75/76 DVOJ-CKI Michael+Martin Krasine-h18 (bracket!)", 87, rowsbox(87, 4, 5, L)),
 ("G1b s87-r4+5 DESNO (isti-star-i + isti-botra)", 87, rowsbox(87, 4, 5, R)),
 ("G2 s84-r1+2 z46/47 DVOJ-CKI Joannes+Anna Grem-h26 (bracket!)", 84, rowsbox(84, 1, 2, L)),
 ("G3 s81-r8+9 z28/29 DVOJ-CKI Georg+Marcus Prilozje-h30 (bracket!)", 81, rowsbox(81, 8, 9, L)),
 ("G4 s80-r3 z15 DATUM Feb-28>Mar-1 (rojen-krsten!)", 80, rowbox(80, 3, (0.11, 0.44))),
 ("G5 s91-r5 z101 HI-NA-DUEL '34/84/94' KROP-MAX", 91, rowbox(91, 5, (0.30, 0.47))),
 ("G6 s91-r1+2 z97/98 RETRO-VPISI Nov-29/30 (na-strani-po-Dec-28!)", 91, rowsbox(91, 1, 2, L)),
])
print("KROPS-GOTOVI")
