#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P169 — forenzični izrezi mrliške 04894, leto 1903 (skeni 90–95).
Trakovi ×2.2 (celotne vrstice; 17 Griblje-1903-kandidatov + meja
1903/04 na s94 + glave-napake s92/'18903' + s94/'18903' + s95/'18 1904')
+ celice ×3.0 (targetirane: vas/hisna + imena-konflikti + starosti +
Dostal/Rauq podpisi + zapcol rezine).
yc iz /tmp/p169/rows3.json (v3-detekcija + agent-eyes diag-verifikacija:
s90 [c0=naslov!] z58–z61 + MEJA-1903 + r1–r7 [P168-podpisano-dno!],
s91 zap8–19, s92 zap20–31 [3-orphan-celice OK], s93 zap32–43 [z43-orphan],
s94 z44–z51 + MEJA-1904 + 1904-r1–r3, s95 zap4–15 [interpolirano]).
Izhod: /tmp/p169/crops/*.png"""
from PIL import Image
import os

OUT = "/tmp/p169/crops"
os.makedirs(OUT, exist_ok=True)

# cell-yc po skenu (rows3.json c1–c12 = zap-vrste; c0 = naslov-ostanek!)
S90 = {"z58": 398, "z59": 533, "z60": 663, "z61": 797, "mk1903": 934,
       "r1": 1072, "r2": 1209, "r3": 1347, "r4": 1484, "r5": 1620,
       "r6": 1757, "r7": 1892}
S91 = {"z8": 396, "z9": 534, "z10": 672, "z11": 806, "z12": 941,
       "z13": 1079, "z14": 1216, "z15": 1354, "z16": 1493, "z17": 1631,
       "z18": 1769, "z19": 1904}
S92 = {"z20": 393, "z21": 531, "z22": 671, "z23": 802, "z24": 945,
       "z25": 1084, "z26": 1218, "z27": 1351, "z28": 1486, "z29": 1620,
       "z30": 1750, "z31": 1881}
S93 = {"z32": 390, "z33": 523, "z34": 659, "z35": 796, "z36": 935,
       "z37": 1074, "z38": 1208, "z39": 1342, "z40": 1475, "z41": 1608,
       "z42": 1744, "z43": 1884}
S94 = {"z44": 383, "z45": 521, "z46": 655, "z47": 785, "z48": 915,
       "z49": 1047, "z50": 1182, "z51": 1319, "mk1904": 1455,
       "r1": 1592, "r2": 1729, "r3": 1864}
S95 = {"z4": 245, "z5": 383, "z6": 521, "z7": 659, "z8": 797, "z9": 923,
       "z10": 1060, "z11": 1196, "z12": 1332, "z13": 1470, "z14": 1608,
       "z15": 1746}
GLAVA = 155  # letnica-glava y (vsi skeni)

TRAKT = [
    # --- Griblje-kandidati 1903 (17) ---
    ("griblje-s90-z1-alojzij-stravs", 90, S90["r1"]),
    ("griblje-s90-z3-nikolaj-stravs", 90, S90["r3"]),
    ("griblje-s90-z4-jozef-zegriva", 90, S90["r4"]),
    ("griblje-s91-z8-barbara-pezdirec", 91, S91["z8"]),
    ("griblje-s91-z10-marija-pezdirec", 91, S91["z10"]),
    ("griblje-s91-z12-franciska-kukan", 91, S91["z12"]),
    ("griblje-s91-z13-ana-brodaric", 91, S91["z13"]),
    ("griblje-s91-z14-marija-zefko", 91, S91["z14"]),
    ("griblje-s91-z16-janez-simec", 91, S91["z16"]),
    ("griblje-s91-z19-alojzij-pozek", 91, S91["z19"]),
    ("griblje-s92-z22-janez-pecnirec", 92, S92["z22"]),
    ("griblje-s92-z30-katarina-zefko", 92, S92["z30"]),
    ("griblje-s93-z38-marija-span", 93, S93["z38"]),
    ("griblje-s93-z41-jurij-simec", 93, S93["z41"]),
    ("griblje-s93-z42-andrej-sotler", 93, S93["z42"]),
    ("griblje-s94-z48-katarina-radovic", 94, S94["z48"]),
    ("griblje-s94-z50-marija-dragar", 94, S94["z50"]),
    # --- meja 1903/04 (s94): zadnji-1903 + marker + prvi-1904 ---
    ("meja-1903-04-z51-zadnji-1903", 94, S94["z51"]),
    ("meja-1903-04-marker-1904", 94, S94["mk1904"]),
    ("meja-1903-04-z1-prvi-1904", 94, S94["r1"]),
    # --- meja 1902/03 re (s90) — 11. stil-potrditev ---
    ("meja-1902-03-marker-1903-re", 90, S90["mk1903"]),
    # --- glave-napake (3 pisarjeve napake-kandidati!) ---
    ("glava-s92-18903", 92, GLAVA),
    ("glava-s94-18903", 94, GLAVA),
    ("glava-s95-181904", 95, GLAVA),
    # --- s95 Griblje/Giriče zmeda (1904 — samo kontekst!) ---
    ("s95-z8-anton-sajnic-kontekst", 95, S95["z8"]),
    ("s95-z10-ana-krvan-kontekst", 95, S95["z10"]),
]

CELLS = [
    # --- vas+hisna ×3.0 (vseh 17 Griblje) ---
    ("s90-z1-vas-hisna", 90, S90["r1"]),
    ("s90-z3-vas-hisna", 90, S90["r3"]),
    ("s90-z4-vas-hisna", 90, S90["r4"]),
    ("s91-z8-vas-hisna", 91, S91["z8"]),
    ("s91-z10-vas-hisna", 91, S91["z10"]),
    ("s91-z12-vas-hisna", 91, S91["z12"]),
    ("s91-z13-vas-hisna", 91, S91["z13"]),
    ("s91-z14-vas-hisna", 91, S91["z14"]),
    ("s91-z16-vas-hisna", 91, S91["z16"]),
    ("s91-z19-vas-hisna", 91, S91["z19"]),
    ("s92-z22-vas-hisna", 92, S92["z22"]),
    ("s92-z30-vas-hisna", 92, S92["z30"]),
    ("s93-z38-vas-hisna", 93, S93["z38"]),
    ("s93-z41-vas-hisna", 93, S93["z41"]),
    ("s93-z42-vas-hisna", 93, S93["z42"]),
    ("s94-z48-vas-hisna", 94, S94["z48"]),
    ("s94-z50-vas-hisna", 94, S94["z50"]),
    # --- imena (konflikti: Žegriva/Legirca + Kukan/Krizan + Pečnirec +
    #     Špan/Štravs + Dragar/Dragoš + Puček/Požek) ---
    ("s90-z4-ime", 90, S90["r4"]),
    ("s91-z12-ime", 91, S91["z12"]),
    ("s92-z22-ime", 92, S92["z22"]),
    ("s93-z38-ime", 93, S93["z38"]),
    ("s93-z41-ime", 93, S93["z41"]),
    ("s94-z48-ime", 94, S94["z48"]),
    ("s94-z50-ime", 94, S94["z50"]),
    ("s94-r3-ime", 94, S94["r3"]),
    # --- starosti spornih (s90-r1 '5-mes', s92-z22 '64?', s93-z41 '72?',
    #     s94-z48 '54?', s94-z50 '10-mes', s90-z61 '92' = P168-re!) ---
    ("s90-r1-starost", 90, S90["r1"]),
    ("s90-r3-starost", 90, S90["r3"]),
    ("s90-r4-starost", 90, S90["r4"]),
    ("s91-z10-starost", 91, S91["z10"]),
    ("s92-z22-starost", 92, S92["z22"]),
    ("s92-z30-starost", 92, S92["z30"]),
    ("s93-z38-starost", 93, S93["z38"]),
    ("s93-z41-starost", 93, S93["z41"]),
    ("s94-z48-starost", 94, S94["z48"]),
    ("s94-z50-starost", 94, S94["z50"]),
    # --- podpisi: Dostál vs Rauq (zamenjava!) + s94-z44-prazno ---
    ("s91-z8-podpis-dostal", 91, S91["z8"]),
    ("s93-z37-podpis-rauq", 93, S93["z37"]),
    ("s94-z44-podpis-prazno", 94, S94["z44"]),
    ("s94-r1-podpis-rauq", 94, S94["r1"]),
    ("s95-z4-podpis-dostal", 95, S95["z4"]),
    # --- zapcol spot-checks (kontinuiteta + restart + napake) ---
    ("s90-r1-zapcol", 90, S90["r1"]),
    ("s90-r7-zapcol", 90, S90["r7"]),
    ("s91-z8-zapcol", 91, S91["z8"]),
    ("s92-z20-zapcol", 92, S92["z20"]),
    ("s93-z32-zapcol", 93, S93["z32"]),
    ("s94-z44-zapcol", 94, S94["z44"]),
    ("s94-r1-zapcol", 94, S94["r1"]),
    ("s95-z4-zapcol", 95, S95["z4"]),
]

T_X = (100, 2450)   # trak x-range
C_X = (520, 900)    # celica vas+hisna
I_X = (860, 1400)   # ime
S_X = (1770, 2200)  # starost
P_X = (2080, 2470)  # podpis
Z_X = (80, 200)     # zapcol (zap št. ~0.035–0.075 × 2640)
G_X = (100, 900)    # glava (Leto NNNN)


def crop(name, scan, x0, x1, yc, half, zoom):
    im = Image.open(f"/tmp/p169/s{scan:02d}.jpg")
    c = im.crop((x0, max(0, yc - half), x1, min(im.size[1], yc + half)))
    c = c.resize((int(c.size[0] * zoom), int(c.size[1] * zoom)), Image.LANCZOS)
    c.save(f"{OUT}/{name}.png")
    return c.size


def main():
    n = 0
    for (name, scan, yc) in TRAKT:
        crop(name, scan, T_X[0], T_X[1], yc, 90, 2.2)
        n += 1
    for (name, scan, yc) in CELLS:
        if "podpis" in name:
            x0, x1 = P_X
        elif "ime" in name:
            x0, x1 = I_X
        elif "starost" in name:
            x0, x1 = S_X
        elif "zapcol" in name:
            x0, x1 = Z_X
        else:
            x0, x1 = C_X
        half = 100 if "zapcol" in name else 85
        zoom = 2.5 if "zapcol" in name else 3.0
        crop(name, scan, x0, x1, yc, half, zoom)
        n += 1
    # glave-trakovi (širši, manjši zoom)
    for name, scan, yc in [("glava-s92-18903", 92, GLAVA),
                           ("glava-s94-18903", 94, GLAVA),
                           ("glava-s95-181904", 95, GLAVA)]:
        crop(name, scan, G_X[0], G_X[1], yc, 70, 2.0)
        n += 1
    print(f"crops: {n} shranjenih ({len(TRAKT)} trakov + {len(CELLS)} celic + 3 glave)")


if __name__ == "__main__":
    main()
