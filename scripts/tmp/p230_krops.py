#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P230 — MAX-krop montażni sheet-i (VIZUALNO-arhivar-metodologija P229!).
Sheet-i = vertikalno-složeni-krop-i (×1.8-lanczos) z labelami. Izhod: /tmp/p230/krops/sheet-*.png"""
from PIL import Image, ImageDraw, ImageFont

T = "/tmp/p230"
OUT = f"{T}/krops"
import os
os.makedirs(OUT, exist_ok=True)

# vrstic-na-stran (iz VIZUALNO-branja!)
ROWS = {64: 4, 65: 7, 66: 7, 67: 7, 68: 8, 69: 9, 70: 8, 71: 8, 72: 7, 73: 8, 74: 8, 75: 7, 76: 7, 77: 8, 78: 5}
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
DAT = (0.11, 0.44)  # samo mesec+dan

# A: GRIBLJE s65–s68 (5 hiš)
sheet("A", [
 ("A1 s68-r1 z?-GRIBLJE-h40-Maria LEVO (PEZDIRE-oce-garble 'Braðire'!)", 68, rowbox(68, 1, L)),
 ("A1b s68-r1 DESNO (botra DEBLI-C+KLOBU-CAR + Hoggia)", 68, rowbox(68, 1, R)),
 ("A2 s68-r5 GRIBLJE-h39-Georg LEVO (SIMEC-oce!)", 68, rowbox(68, 5, L)),
 ("A2b s68-r5 DESNO (BRODARI-C+KLOBU-CAR-botra!)", 68, rowbox(68, 5, R)),
 ("A3 s68-r7 Mai-1/2 GRIBLJE-h20-Mathias LEVO (PEZDIRE-oce!)", 68, rowbox(68, 7, L)),
 ("A3b s68-r7 DESNO (MILEK+BRODARI-C-botra)", 68, rowbox(68, 7, R)),
 ("A4 s69-r3 GRIBLJE-h16-Joannes LEVO (ELAH-oce!)", 69, rowbox(69, 3, L)),
 ("A4b s69-r3 DESNO (ELKO+HRI-AN-botra)", 69, rowbox(69, 3, R)),
 ("A5 s70-r5 Juli-3/3 GRIBLJE-h7-Anna LEVO (JETTER-oce-garble + HRI-AN-matec!)", 70, rowbox(70, 5, L)),
 ("A5b s70-r5 DESNO (HURE-botra + als-Amtsvormund!)", 70, rowbox(70, 5, R)),
])

# B: GRIBLJE s70–s73 (4 hiše)
sheet("B", [
 ("B1 s70-r8 GRIBLJE-h15-Nicolaus LEVO (MUC-oce!)", 70, rowbox(70, 8, L)),
 ("B1b s70-r8 DESNO (BRAJ-C+RI-E-botra)", 70, rowbox(70, 8, R)),
 ("B2 s71-r7 Griblje-h22-Katharina LEVO (mesec-DUEL! + †7.10.1931!)", 71, rowbox(71, 7, L)),
 ("B2b s71-r7 DESNO (MILEK-oce + BRODARI-C+HUSI-C-botra!)", 71, rowbox(71, 7, R)),
 ("B3 s73-r6 GRIBLJE-h53-Maria LEVO (PEZDIRE-oce+boter-DVOJNI!)", 73, rowbox(73, 6, L)),
 ("B3b s73-r6 DESNO (Anna-ERDI-C-matec + DRAGO-boter!)", 73, rowbox(73, 6, R)),
 ("B4 s73-r7 GRIBLJE-h62-Nicolaus LEVO (KURE-oce + KRI-AN-matec + MODRI!)", 73, rowbox(73, 7, L)),
 ("B4b s73-r7 DESNO (MILEK+BRODARI-C-botra!)", 73, rowbox(73, 7, R)),
])

# C: GRIBLJE s74–s77 (5 hiš)
sheet("C", [
 ("C1 s74-r1 Sep-18/19 GRIBLJE-h25-Mathias LEVO (BRINC-oce! + †9.12.1935!)", 74, rowbox(74, 1, L)),
 ("C1b s74-r1 DESNO (POTIH + PLUTAI-botra)", 74, rowbox(74, 1, R)),
 ("C2 s75-r3 Okt-19/19 GRIBLJE-h8-Catharina LEVO (JAKOF-C-oce + BRODARI-C-matec!)", 75, rowbox(75, 3, L)),
 ("C2b s75-r3 DESNO (KLOBU-CAR + DRAGO-botra!)", 75, rowbox(75, 3, R)),
 ("C3 s76-r4 Nov-21/21 GRIBLJE-h55-Maria LEVO (SIMEC-oce + PEZDIRE-matec!)", 76, rowbox(76, 4, L)),
 ("C3b s76-r4 DESNO (KRANC + PEZDIRE-botra-DVOJNI!)", 76, rowbox(76, 4, R)),
 ("C4 s76-r6 Nov-23/23 GRIBLJE-h44-Barbara LEVO (HRUZEL-oce + KLOBU-CAR-matec!)", 76, rowbox(76, 6, L)),
 ("C4b s76-r6 DESNO (KRANC + KLOBU-CAR-botra!)", 76, rowbox(76, 6, R)),
 ("C5 s77-r3 Dez-1/1 GRIBLJE-h31-Nicolaus LEVO (ZUPANI-C-oce + PEZDIRE-matec! + zap-94-MODRA!)", 77, rowbox(77, 3, L)),
 ("C5b s77-r3 DESNO (ZUPANI-C+HARASINI-C-botra + MODRI-†18.9.1961!)", 77, rowbox(77, 3, R)),
])

# D: DUELI — Griče/Griblje + hišne + meseci
sheet("D", [
 ("D1 s66-r4 'Gritže'-h6 DUEL (Griče-vs-Griblje! + PEZDIRE-matec!)", 66, rowbox(66, 4, L)),
 ("D1b s66-r4 DESNO", 66, rowbox(66, 4, R)),
 ("D2 s72-r6 'Grilže'-h55 Wolfgr-Daisl RETRO-DUEL (25/25-po-28/29! + brez-botra!)", 72, rowbox(72, 6, L)),
 ("D2b s72-r6 DESNO", 72, rowbox(72, 6, R)),
 ("D3 s71-r6 'Gri-moršč'-h15 Nicolaus+Martin DVOJNI-IME (vas-DUEL!)", 71, rowbox(71, 6, L)),
 ("D4 s73-r8 Certoviše-h20/'pmix-16' DUEL + Lunenič", 73, rowbox(73, 8, L)),
 ("D5 s76-r7 Vranoviče-mit-Boršt-№18 LEVO (†19.1.1933!)", 76, rowbox(76, 7, L)),
 ("D6 s77-r1 Nov-29/29 Otok-h5 LEVO (PEZDIRE-boter!)", 77, rowbox(77, 1, L)),
 ("D7 s77-r3 zap-'94'-MODRA LEVO-ROB", 77, (0.09, 0.22, rowbox(77, 3)[2], rowbox(77, 3)[3])),
])

# E: NEZAKONSKI + Wolfgr-anomalije + meje
sheet("E", [
 ("E1 s66-r6 NEZAKONSKI-Krasine-h34 (oče-PRAZNA + Maria-Kralj-dolga-nota!)", 66, rowbox(66, 6, L)),
 ("E1b s66-r6 DESNO (botra-Cernič+BRODARI-C+Jurejčič!)", 66, rowbox(66, 6, R)),
 ("E2 s72-r3 NEZAKONSKI-Zemelj-h22 (oče-dash! + Jaklič-matec!)", 72, rowbox(72, 3, L)),
 ("E3 s72-r7 NEZAKONSKI-Certoviše-h13 (oče-dash + Jurejčič-garble!)", 72, rowbox(72, 7, L)),
 ("E4 s77-r7 NEZAKONSKI-Grem-h33 (oče-dash +elah-matec!)", 77, rowbox(77, 7, L)),
 ("E5 s74-r2 NEZAKONSKI-Boginja-vas-h42 (oče-dash + dolga-matec-nota!)", 74, rowbox(74, 2, L)),
 ("E6 s69-r1 Wolfgr-anomalia (botra+duhovnik-PRAZNA! + hebamme-only!)", 69, rowbox(69, 1, FULL)),
 ("E7 s70-r1 Wolfgr-anomalia (botra+duhovnik-PRAZNA! + hebamme-only!)", 70, rowbox(70, 1, FULL)),
 ("E8 s65-r1 z1-RESTART Jänner-5/5 (prvi-vpis-1876! + zap-1!)", 65, rowbox(65, 1, FULL)),
])

# F: MEJA-1875/76 + TAIL-1875 + finis-KALLIGRAFIJA
n64 = ROWS[64]
sheet("F", [
 ("F1 s64 GLAVA-'Jahr 1875' + TAIL-r1 Dez-1/1 Krasine-h15", 64, rowbox(64, 1, FULL)),
 ("F2 s64-r2 Dez-3/3 Zemelj-h17 (MUC-oce!)", 64, rowbox(64, 2, FULL)),
 ("F3 s64-r3 Dez-26/26 GRIBLJE-h11-Anna (TAIL-1875-GRIBLJE!-Hoggia)", 64, rowbox(64, 3, FULL)),
 ("F4 s64-r4 Dez-18/19-RETRO-DUEL Gradac-h55 + Prosenik-×3", 64, rowbox(64, 4, FULL)),
 ("F5 s64 FINIS-ANNI-1875-KALLIGRAFIJA (sredina-spodaj!)", 64, (0.10, 0.995, 0.135 + (Y1 - Y0) / n64 * 4 - 0.02, 0.92)),
 ("F6 s65 GLAVA-'Jahr 1876' (brez-Incipit!)", 65, (0.10, 0.995, 0.09, 0.155)),
 ("F7 s78-r1 TAIL-1876-Dobravce-h16-Martin (P229-ŽE-VLM!)", 78, rowbox(78, 1, FULL)),
])

# G: DVOJČKI-brackets + anomalije
sheet("G", [
 ("G1 s71-r4+5 DVOJČKI-Peter+Michael Krasine-h25 (brace!)", 71, rowsbox(71, 4, 5, L)),
 ("G1b s71-r4+5 DESNO (isti-starši!)", 71, rowsbox(71, 4, 5, R)),
 ("G2 s73-r3+4 DVOJČKI-Petrus+Maria Certoviše-h26 (brace!)", 73, rowsbox(73, 3, 4, L)),
 ("G2b s73-r3+4 DESNO (isti-starši!)", 73, rowsbox(73, 3, 4, R)),
 ("G3 s69-r9 DVOJNI?-Anna+Katharina Goriče-h25 (Juni-4/5!-†5.1945!)", 69, rowbox(69, 9, FULL)),
 ("G4 s71-r6 Nicolaus+Martin 'Gri-moršč'-h15 DVOJNI-IME", 71, rowbox(71, 6, L)),
 ("G5 s72-r1 August-9/12-DUEL (rojen-9-krsten-12?!) Dobravce-h13", 72, rowbox(72, 1, DAT)),
 ("G6 s71-r2 4-tička-margin (rdeča!) + Gradove-3-Marin", 71, rowbox(71, 2, DAT)),
])

# H: MODRI + MMK + foliacija + duhovniki
sheet("H", [
 ("H1 s67-r6 MODRI-MMK-Dobravce-h17-Anna (dolg!)", 67, rowbox(67, 6, L)),
 ("H2 s68-r3 MODRI-MMK-Certoviše-h18-Anna (dolg!)", 68, rowbox(68, 3, L)),
 ("H3 s69-r5 MODRI-Krasine-h12-Anton (umrl-18.8.1946!)", 69, rowbox(69, 5, L)),
 ("H4 s72-r5 MODRI-Dobravce-h8-Anton (umrl-5.1.1950!)", 72, rowbox(72, 5, L)),
 ("H5 s75-r5 MODRI-Prilozje-h35-Anna (umrla-9.10.1956!)", 75, rowbox(75, 5, L)),
 ("H6 s75-r6 MODRI-Vranoviče-h17-Margaretha (umrla-20.3.1957!)", 75, rowbox(75, 6, DAT)),
 ("H7 s65-r3 MODRA-Certovise-h9-Anna (Chicago-1970!)", 65, rowbox(65, 3, L)),
 ("H8 s71-foliacija-'66' (svinčnik-LEVO-ZGORAJ)", 71, (0.07, 0.20, 0.03, 0.09)),
 ("H9 s65-foliacija-'60' (svinčnik!)", 65, (0.07, 0.20, 0.03, 0.09)),
 ("H10 s64-foliacija-'59' (svinčnik!)", 64, (0.07, 0.20, 0.03, 0.09)),
])
print("KROPS-GOTOVI")
