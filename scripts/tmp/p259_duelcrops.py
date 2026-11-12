#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P259 — duel-kompoziti: celice vrstic s11/s12/s13 (imena/hiše/datumi) lepljene v
označene navpične kompozite ×3–4 zoom. Geometrija (po p259_rows.py, isti skeni!):
  vrstice: s11 = 13 (y0 285, y1 1400) · s12 = 12 (y0 280, y1 1260) · s13 = 11 (y0 280, y1 1040)
  stolpci: date 70–220 | ženin-vas+hiša 210–480 | ženin-ime 450–730 |
           nevesta-vas+hiša 680–950 | nevesta-ime 920–1095 | desna 1030–2050
Duel-seznam (iz hints a/b alternativ + facts.json datumDueli):
  s11_r2 (Gosling|Pesdirz? h53|33 + Bring|Brinc h24) · s12_r1/r2 (19.|12.-Febr + Hofferer|Hohenauer)
  s12_r5 (Schmig|Amiz h60 + 19.|10.|26.-Oct) · s12_r7 (RESTART-1834 22.|27.-Jän)
  s13_r1 (5.|8.-Febr) · s13_r2 (5.|9.) · s13_r6 (Vrh h58|68 + h51) · s13_r11 (10.|17.-Febr + Marentič 24|29)"""
import os
from PIL import Image, ImageDraw

OUT = "/tmp/p259/duels"
os.makedirs(OUT, exist_ok=True)

ROWS = {'s11': (13, 285, 1400), 's12': (12, 280, 1260), 's13': (11, 280, 1040)}
# Kalibracija po p258-s8/s9 (ISTI fizični zvezek!) + p259_rows.py G/B-bloki (G 40–640 / B 600–1080):
GEOM = {
    'date':     (70, 220),
    'groom_vh': (220, 475),
    'groom_nm': (445, 700),
    'bride_vh': (695, 915),
    'bride_nm': (890, 1095),
    'right':    (1030, 2050),
}


def yc(scan, r):
    n, y0, y1 = ROWS[scan]
    pitch = (y1 - y0) / n
    return int(y0 + (r - 0.5) * pitch)


def half(scan):
    n, y0, y1 = ROWS[scan]
    return int((y1 - y0) / n * 0.55) + 6


def cell(im, x0, x1, cy, hf, zoom):
    c = im.crop((x0, max(0, cy - hf), x1, min(im.size[1], cy + hf)))
    return c.resize((int(c.width * zoom), int(c.height * zoom)), Image.LANCZOS)


def composite(name, scan, items, zoom=4):
    """items = [(row, colkey, label)] — lepi navpično z oznakami."""
    im = Image.open(f'/tmp/p259/{scan}.jpg')
    parts = []
    for row, col, label in items:
        cy = yc(scan, row)
        x0, x1 = GEOM[col]
        c = cell(im, x0, x1, cy, half(scan), zoom)
        band = Image.new('RGB', (c.width, 34), 'white')
        d = ImageDraw.Draw(band)
        d.text((10, 8), label, fill='black')
        parts.append(band); parts.append(c)
        sep = Image.new('RGB', (c.width, 6), 'gray')
        parts.append(sep)
    W = max(p.width for p in parts)
    H = sum(p.height for p in parts)
    out = Image.new('RGB', (W, H), 'white')
    y = 0
    for p in parts:
        out.paste(p, (0, y)); y += p.height
    out.save(f'{OUT}/{name}.jpg', quality=93)
    print(f"{name}: {out.size}")


# D1–D3: datumski kompoziti (vse vrstice, ×3) — kaskada 6./13. Febr 1833 + restarti 1834
composite('s11_dates', 's11', [(i, 'date', f'VRSTICA {i} — DATUM (6. Febr-kaskada → 13. d°):') for i in range(1, 14)], zoom=3)
composite('s12_dates', 's12', [(i, 'date', f'VRSTICA {i} — DATUM (1833-konec → 1834-RESTART):') for i in range(1, 13)], zoom=3)
composite('s13_dates', 's13', [(i, 'date', f'VRSTICA {i} — DATUM (rob-št. {i+7} — 5./9./10. Febr 1834):') for i in range(1, 12)], zoom=3)

# D4: s11_r2 GOSLING/PESDIRZ — glavni imenski duel!
composite('s11_r2_gosling', 's11', [
    (2, 'groom_nm', 'R2 ŽENIN-IME (Joh. GOSLING? PESDIRZ? GUTTING?) — ČRKO ZA ČRKO!'),
    (2, 'groom_vh', 'R2 ŽENIN-VAS+HIŠA (Griblje 53 ali 33?) — ŠTEVILKO ZA ŠTEVILKO!'),
    (2, 'bride_nm', 'R2 NEVESTA-IME (Maria BRING? BRINC? BRUNG?) — črko za črko!'),
    (2, 'bride_vh', 'R2 NEVESTA-VAS+HIŠA (Griblje 24?)'),
], zoom=4)

# D5: s12_r1+r2 — datumski 19.|12.-Febr + imena Hofferer/Hohenauer
composite('s12_r1_r2', 's12', [
    (1, 'groom_nm', 'R1 ŽENIN-IME (Georg HOFFERER? HOHENAUER?) — črko za črko!'),
    (1, 'groom_vh', 'R1 ŽENIN-VAS+HIŠA (Nötsch? Kreuzdorf? 13?)'),
    (1, 'bride_nm', 'R1 NEVESTA-IME (Anna Tschesch? Stunigk?)'),
    (1, 'bride_vh', 'R1 NEVESTA-VAS+HIŠA (Goritschach? Prüstein? 10?)'),
    (2, 'date', 'R2 DATUM (19. d°? 12. April?) — pazi mesec!'),
    (2, 'groom_nm', 'R2 ŽENIN-IME + priimek'),
], zoom=4)

# D6: s12_r5 — SCHMIG/ŠIMIČ h60 + datumski 19.|10.|26.-Oct
composite('s12_r5_schmig', 's12', [
    (5, 'date', 'R5 DATUM (19.? 10.? 26. October?) — DAN + MESEC!'),
    (5, 'groom_nm', 'R5 ŽENIN-IME (Georg SCHMIG? AMIZ? ~ŠIMIČ?) — črko za črko!'),
    (5, 'groom_vh', 'R5 ŽENIN-VAS+HIŠA (Griblje/Gribl 60?)'),
    (5, 'bride_nm', 'R5 NEVESTA-IME (Katharina Harschpich? Jureisjofrig?)'),
    (5, 'bride_vh', 'R5 NEVESTA-VAS+HIŠA (Kresling? Kosting? 21?)'),
], zoom=4)

# D7: s12_r7 — RESTART-1834! 22.|27.-Jän + imena
composite('s12_r7_restart', 's12', [
    (7, 'date', 'R7 DATUM (22. ali 27. Jänner 1834?) — DAN! + letnica 1834?'),
    (7, 'groom_nm', 'R7 ŽENIN-IME (Johann Kalmigh? Stephan Pasfrig?) — črko za črko!'),
    (7, 'groom_vh', 'R7 ŽENIN-VAS+HIŠA (Vano? Vivano? 5?)'),
    (7, 'bride_nm', 'R7 NEVESTA-IME (Maria Dobrak? Kosak?)'),
    (7, 'bride_vh', 'R7 NEVESTA-VAS+HIŠA (Gordej? Gradiz? 3?)'),
], zoom=4)

# D8: s13_r1 — restart-glava 5.|8.-Febr + imena
composite('s13_r1_restart', 's13', [
    (1, 'date', 'R1 DATUM (5. ali 8. Febr 1834?) — DAN! (pepelni-1834 = 5. 2.?)'),
    (1, 'groom_nm', 'R1 ŽENIN-IME (Georg Kapucžik? Koschizhigl?) — črko za črko!'),
    (1, 'groom_vh', 'R1 ŽENIN-VAS+HIŠA (Gerhüpe/Gorjupa? 2?)'),
    (1, 'bride_nm', 'R1 NEVESTA-IME (Anna Vipotnik? Viqnay?)'),
    (1, 'bride_vh', 'R1 NEVESTA-VAS+HIŠA (Jeschnica? Gerhuipa? 8?)'),
], zoom=4)

# D9: s13_r6 — VRH h58|h68 + h51 (GRIBLJE-PAR!)
composite('s13_r6_vrh', 's13', [
    (6, 'groom_nm', 'R6 ŽENIN-IME (Marcus VRH? VRBAN? — ČRKO ZA ČRKO!)'),
    (6, 'groom_vh', 'R6 ŽENIN-VAS+HIŠA (Griblje 58 ali 68?) — ŠTEVILKO ZA ŠTEVILKO!'),
    (6, 'bride_nm', 'R6 NEVESTA-IME (Maria Haraghtinich? Karafhainj?) — črko za črko!'),
    (6, 'bride_vh', 'R6 NEVESTA-VAS+HIŠA (Griblje 51?)'),
], zoom=4)

# D10: s13_r11 — zadnja vrstica: 10.|17.-Febr + MARENTIČ 24|29
composite('s13_r11_marentic', 's13', [
    (11, 'date', 'R11 DATUM (10. ali 17. Febr 1834?) — DAN!'),
    (11, 'groom_nm', 'R11 ŽENIN-IME (Georg Hozhoved? Koschheuel?) — črko za črko!'),
    (11, 'groom_vh', 'R11 ŽENIN-VAS+HIŠA (Konyev/Kostanjevica? 13?)'),
    (11, 'bride_nm', 'R11 NEVESTA-IME (Margareth MARENTICH? Marcuteich? ~MARENTIČ!)'),
    (11, 'bride_vh', 'R11 NEVESTA-VAS+HIŠA (Dobravlje 24 ali 29?) — ŠTEVILKO!'),
], zoom=4)

print("DONE — kompoziti:", len([f for f in os.listdir(OUT) if f.endswith('.jpg')]))
