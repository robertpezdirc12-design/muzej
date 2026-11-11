#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P258 — duel-kompoziti: celice vrstic s8/s9/s10 (imena/hiše/datumi) lepljene v
označene navpične kompozite ×3–5 zoom. Geometrija:
  s8: date 80–222 | ženin-vas+hiša 222–463 | ženin-ime 463–700 | nevesta-vas+hiša 700–898 | nevesta-ime 898–1010 | priče 1451–1672
  s9: date 90–230 | ženin-vas+hiša 230–470 | ženin-ime 470–700 | nevesta-vas+hiša 700–920 | nevesta-ime 920–1040 | starši 1080–1330
  s10: date 130–205 | ženin-vas+hiša 205–643 | ženin-ime 643–812 | nevesta-vas+hiša 887–1056 | nevesta-ime 1056–1225 | starši 1323–1450"""
import os
from PIL import Image, ImageDraw

OUT = "/tmp/p258/duels"
os.makedirs(OUT, exist_ok=True)

GEOM = {
    's8':  {'date': (80, 222), 'groom_vh': (222, 463), 'groom_nm': (463, 700), 'bride_vh': (700, 898), 'bride_nm': (898, 1010), 'witness': (1451, 1672)},
    's9':  {'date': (90, 230), 'groom_vh': (230, 470), 'groom_nm': (470, 700), 'bride_vh': (700, 920), 'bride_nm': (920, 1040), 'witness': (1330, 1560)},
    's10': {'date': (130, 205), 'groom_vh': (205, 643), 'groom_nm': (643, 812), 'bride_vh': (887, 1056), 'bride_nm': (1056, 1225), 'witness': (1323, 1450)},
}

# prilagojeni y-centri vrstic (iz regijskih branj)
YC = {
    's8':  {1: 337, 2: 440, 3: 544, 4: 615, 5: 680, 6: 765, 7: 865, 8: 990, 9: 1100, 10: 1200, 11: 1310},
    's9':  {i: 318 + (i-1)*75 for i in range(1, 16)},
    's10': {i: 320 + (i-1)*80 for i in range(1, 15)},
}
HALF = {'s8': 48, 's9': 40, 's10': 42}


def cell(im, x0, x1, cy, half, zoom):
    c = im.crop((x0, max(0, cy - half), x1, min(im.size[1], cy + half)))
    return c.resize((int(c.width * zoom), int(c.height * zoom)), Image.LANCZOS)


def composite(name, scan, items, zoom=3):
    """items = [(row, colkey, label)] — lepi navpično z oznakami."""
    im = Image.open(f'/tmp/p258/{scan}.jpg')
    parts = []
    for row, col, label in items:
        cy = YC[scan][row]
        x0, x1 = GEOM[scan][col]
        c = cell(im, x0, x1, cy, HALF[scan], zoom)
        # oznaka zgoraj
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


# D1–D3: datumski kompoziti (vse vrstice, ×3)
for scan, n in [('s8', 11), ('s9', 15), ('s10', 14)]:
    composite(f'{scan}_dates', scan, [(i, 'date', f'VRSTICA {i} — DATUM:') for i in range(1, n + 1)], zoom=3)

# D4: s8 imena A (r1/r2)
composite('s8_namesA', 's8', [
    (1, 'groom_nm', 'R1 ŽENIN-IME (Mercina? Hribar?):'),
    (1, 'bride_vh', 'R1 NEVESTA-VAS+HIŠA (Griblje 47 ali 17?):'),
    (1, 'bride_nm', 'R1 NEVESTA-IME (Klobuchar?):'),
    (2, 'groom_nm', 'R2 ŽENIN-IME (Staroling? Krasting?):'),
    (2, 'groom_vh', 'R2 ŽENIN-VAS+HIŠA (Krasting 17?):'),
    (2, 'bride_nm', 'R2 NEVESTA-IME (Kostjan? Hribernik?):'),
], zoom=4)

# D5: s8 imena B (r3/r4/r5/r7)
composite('s8_namesB', 's8', [
    (3, 'groom_nm', 'R3 ŽENIN-IME (Kermann? Pavšelč?) + status (Wittmer?):'),
    (3, 'groom_vh', 'R3 ŽENIN-VAS+HIŠA (Gradač 35 ali 38?):'),
    (4, 'bride_vh', 'R4 NEVESTA-VAS+HIŠA (Osilnica 16 ali Griblje 16?):'),
    (5, 'groom_nm', 'R5 ŽENIN-IME (Ignatius Ferjancz?):'),
    (5, 'bride_vh', 'R5 NEVESTA-VAS+HIŠA (Gradišče 1 ali 7?):'),
    (5, 'bride_nm', 'R5 NEVESTA-IME (Magdalena + priimek?):'),
    (7, 'bride_nm', 'R7 NEVESTA-IME (Kleberz? Scalec? Krebelz?):'),
], zoom=4)

# D6: s8 imena C (r8/r9/r10/r11)
composite('s8_namesC', 's8', [
    (8, 'groom_nm', 'R8 ŽENIN-IME + STATUS (Aloys Baron? unierter Priester?):'),
    (8, 'groom_vh', 'R8 ŽENIN-VAS+HIŠA (Gradič/Gradatz 1?):'),
    (8, 'bride_nm', 'R8 NEVESTA-IME (Helena Rubi? Dubil?):'),
    (9, 'bride_nm', 'R9 NEVESTA-IME (Anna + priimek?):'),
    (10, 'groom_nm', 'R10 ŽENIN-IME (Martin Stephan?) + priimek'),
    (10, 'groom_vh', 'R10 ŽENIN-VAS+HIŠA (Wörth? Niedoipriß? 9?):'),
    (11, 'bride_nm', 'R11 NEVESTA-IME (Maria Hasle? Höffler? + geborna?):'),
], zoom=4)

# D6b: s8 r1 priče (Simon Pezdirc?!)
composite('s8_r1_witness', 's8', [
    (1, 'witness', 'R1 PRIČE (Simon Pezdirc?! Košir?):'),
], zoom=4)

# D7: s9 r2 anomALIJA
composite('s9_r2_anomaly', 's9', [
    (2, 'groom_nm', 'R2 ŽENIN-IME — MOŠKI ALI ŽENSKI? (MARINO ali MARIA Vipavz?) — črko za črko!'),
    (2, 'groom_vh', 'R2 ŽENIN-VAS+HIŠA (Krajnç 34 ali 24?):'),
    (2, 'bride_nm', 'R2 NEVESTA-IME (Anna Klepez/Klopčez?):'),
], zoom=4)

# D8: s9 r3 anomALIJA
composite('s9_r3_anomaly', 's9', [
    (3, 'groom_nm', 'R3 ŽENIN-IME — MOŠKI ALI ŽENSKI? (MARINO/MARIA Tolkarigh/Thalkarigh?) — črko za črko!'),
    (3, 'groom_vh', 'R3 ŽENIN-VAS+HIŠA (Prilogje 30?):'),
    (3, 'bride_nm', 'R3 NEVESTA-IME (Anna Taschig/Tsch~righ geb. ?):'),
], zoom=4)

# D9: s9 r1+r5
composite('s9_r1_r5', 's9', [
    (1, 'groom_nm', 'R1 ŽENIN-IME (Georg Surajofz? Harejž?) — črko za črko!'),
    (1, 'groom_vh', 'R1 ŽENIN-VAS+HIŠA (Gradetz/Prädaz 49?):'),
    (1, 'bride_nm', 'R1 NEVESTA-IME (Catharina Ber/Bergant?):'),
    (1, 'bride_vh', 'R1 NEVESTA-VAS+HIŠA (Derberg? 1?):'),
    (5, 'groom_nm', 'R5 ŽENIN-IME (Martin Krefta?):'),
    (5, 'bride_nm', 'R5 NEVESTA-IME (Gertrud Pevac?):'),
], zoom=4)

# D10: s9 r8 MILEK!
composite('s9_r8_milek', 's9', [
    (8, 'groom_nm', 'R8 ŽENIN-IME (Johann Milch? Miklau? MILEK?) — ČRKO ZA ČRKO! (družina hiše 22 iz 1830: Milek!)'),
    (8, 'groom_vh', 'R8 ŽENIN-VAS+HIŠA (Grüble 22?):'),
    (8, 'bride_nm', 'R8 NEVESTA-IME (Anna Snioriz? Štremiz? Fessig?):'),
    (8, 'bride_vh', 'R8 NEVESTA-VAS+HIŠA (Grüble 35?):'),
], zoom=4)

# D11: s9 garbli r9/r11/r13/r14/r15
composite('s9_garbles', 's9', [
    (9, 'groom_nm', 'R9 ŽENIN-IME (Martin Potha? Pejka? Pcpka?):'),
    (9, 'bride_nm', 'R9 NEVESTA-IME (Margaretha Sodržig? Goedpriž?):'),
    (11, 'groom_nm', 'R11 ŽENIN-IME (Georg German? Jurman?):'),
    (13, 'bride_nm', 'R13 NEVESTA-IME (Maria Tilah? Kulah? Toleh?):'),
    (14, 'groom_nm', 'R14 ŽENIN-IME (Mathias Felah? Toleh?):'),
    (15, 'groom_nm', 'R15 ŽENIN-IME (Michael Gricar? Grižar?):'),
], zoom=4)

# D12: s10 r1 nevesta
composite('s10_r1', 's10', [
    (1, 'bride_vh', 'R1 NEVESTA-VAS+HIŠA (GRÜBLE/Griblje 42 ali Smrečje 42?) — previdno!'),
    (1, 'bride_nm', 'R1 NEVESTA-IME (Anna Petriz?):'),
    (1, 'groom_nm', 'R1 ŽENIN-IME (Johann Hlebez? Klebez?) — črko za črko!'),
], zoom=4)

# D13: s10 r5 vasi
composite('s10_r5', 's10', [
    (5, 'groom_vh', 'R5 ŽENIN-VAS+HIŠA (Kreuz 31? Kraplje 21?):'),
    (5, 'bride_vh', 'R5 NEVESTA-VAS+HIŠA (Kreuz 21? Kraplje?):'),
    (5, 'bride_nm', 'R5 NEVESTA-IME (Catharina Hurejzphigh? Jurjevčič?):'),
], zoom=4)

# D14: s10 r7 KRIŽAN 66
composite('s10_r7_krizan', 's10', [
    (7, 'groom_vh', 'R7 ŽENIN-VAS+HIŠA (Güble 66 ali 6?) — ŠTEVILKO ZNAMKO ZA ZNAMKO!'),
    (7, 'groom_nm', 'R7 ŽENIN-IME (Johann Krišan/Kirishan?):'),
    (7, 'bride_vh', 'R7 NEVESTA-VAS+HIŠA (Kraplje 26? Kreuz 35?):'),
    (7, 'bride_nm', 'R7 NEVESTA-IME (Anna Krišan?):'),
], zoom=4)

# D15: s10 r9 RESTART-1833
composite('s10_r9_restart', 's10', [
    (9, 'groom_nm', 'R9 ŽENIN-IME (Anton Sipaž? Seipa?):'),
    (9, 'groom_vh', 'R9 ŽENIN-VAS+HIŠA (Krainz 6?):'),
    (9, 'bride_nm', 'R9 NEVESTA-IME (Anna Auffschein?):'),
    (9, 'bride_vh', 'R9 NEVESTA-VAS+HIŠA (Kleffer? Klofter? 43?):'),
], zoom=4)

# D16: s10 r10+r11
composite('s10_r10_r11', 's10', [
    (10, 'groom_vh', 'R10 ŽENIN-VAS+HIŠA (Kaplice 3? Laune 3?):'),
    (10, 'bride_nm', 'R10 NEVESTA-IME (Barbara Frithovigh?):'),
    (10, 'bride_vh', 'R10 NEVESTA-VAS+HIŠA (Mühle 2?):'),
    (11, 'groom_vh', 'R11 ŽENIN-VAS+HIŠA (Mlake 11?):'),
    (11, 'bride_vh', 'R11 NEVESTA-VAS+HIŠA (Podsmell 12? Podgrad?):'),
    (11, 'bride_nm', 'R11 NEVESTA-IME (Catharina Jafllig?):'),
], zoom=4)

# D17: s10 r13 MUZ
composite('s10_r13_muz', 's10', [
    (13, 'groom_vh', 'R13 ŽENIN-VAS+HIŠA (Draphigh 25? Tratzhig 36?):'),
    (13, 'groom_nm', 'R13 ŽENIN-IME (Nicolaus Petras? Petrin?):'),
    (13, 'bride_nm', 'R13 NEVESTA-IME (Catharina MUZ?) — črko za črko!'),
    (13, 'bride_vh', 'R13 NEVESTA-VAS+HIŠA (Pino 4? Grintez?):'),
], zoom=4)

# D18: s10 r14 PESDIRZ — FINALNA POTRDITEV
composite('s10_r14_pesdirz', 's10', [
    (14, 'groom_nm', 'R14 ŽENIN-IME (Johann PESDIRZ?) — ČRKO ZA ČRKO, KONČNA POTRDITEV!'),
    (14, 'groom_vh', 'R14 ŽENIN-VAS+HIŠA (Gruble 50?):'),
    (14, 'bride_nm', 'R14 NEVESTA-IME (Maria Himiz? SIMIG? Šimič?) — črko za črko!'),
    (14, 'bride_vh', 'R14 NEVESTA-VAS+HIŠA (Gruble 49?):'),
], zoom=5)

# D19: s9 starši r2/r3 (ANOMALIJA-starši)
composite('s9_r23_parents', 's9', [
    (2, 'witness', 'R2 DESNA STRAN — ELTERN des Bräutigams (Marino/Maria Vipavz oče?):'),
    (3, 'witness', 'R3 DESNA STRAN — ELTERN des Bräutigams:'),
], zoom=3)

print("DONE — kompoziti:", len(os.listdir(OUT)))
