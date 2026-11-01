#!/usr/bin/env python3
"""P173 crops v2 — popravljen bug: vsak stolpec svoje ime + kalibrirani stolpci."""
import os
from PIL import Image

DIR = "/tmp/p173"
OUT = os.path.join(DIR, "crops")
os.makedirs(OUT, exist_ok=True)

X = dict(zap=(140, 230), mesec=(260, 440), smrt=(290, 430), pokop=(430, 580),
         vas=(580, 800), hisna=(770, 950), ime=(880, 1450), star=(1500, 1750),
         bolez=(1720, 2100), prev=(2080, 2200), podpis=(2160, 2480))

def row_y(k):
    return 330 + k * 135 - 12, 330 + (k + 1) * 135 + 12

def crop_row(scan, k, cols, label, scale=3.0, ypad=0):
    im = Image.open(f"{DIR}/s{scan}.jpg")
    y0, y1 = row_y(k)
    y0 -= ypad; y1 += ypad
    for col in cols:
        x0, x1 = X[col]
        c = im.crop((x0, max(0, y0), min(im.width, x1), min(im.height, y1)))
        c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS)
        c.save(f"{OUT}/{label}-{col}.png")

def crop_glava(scan):
    im = Image.open(f"{DIR}/s{scan}.jpg")
    c = im.crop((170, 60, 830, 210))
    c = c.resize((int(c.width * 3.0), int(c.height * 3.0)), Image.LANCZOS)
    c.save(f"{OUT}/glava-s{scan}.png")

for s in (109, 111, 112, 113, 114):
    crop_glava(s)

# GRIBLJE-trakovi ×2.2 (vas+hisna+ime)
grib = [
 (109, 0,  "z1-Anton-Brodaric-Brinec-h49"), (109, 1, "z2-Ana-Zeljko-h1"),
 (109, 3,  "z4-Ana-Hleu-Mec-h91"),          (109, 4, "z5-Barbara-Pezdirec-h87"),
 (109, 8,  "z9-Marija-pri-Jovanek-h52"),    (109, 10, "z11-Alojzij-Brisek-h31"),
 (110, 1,  "z13-Anton-Zeljko-Veljko-h60"),  (110, 6, "z18-Matija-Urh-h32"),
 (111, 3,  "z27-Marija-Simec-Strmec-h14"),  (111, 8, "z32-Marija-Kumic-h11"),
 (112, 0,  "z36-Marija-r-Dragos-h74"),      (112, 1, "z37-Matija-Simec-h75"),
 (112, 3,  "z39-Matija-Mlek-h65"),
 (113, 5,  "z53-Jurij-Tocek-h28"),          (113, 7, "z55-Ana-Kruse-h19"),
 (113, 8,  "z56-Ana-rojena-omozena-h21"),   (113, 9, "z57-Nikolaj-Brodaric-h49"),
 (113, 10, "z58-Matija-Ogrince-h25"),       (114, 3, "z63-Anton-Brince-Vrhnar-h10"),
 (114, 5,  "z65-Jozef-Brinec-h10"),
]
for scan, k, label in grib:
    crop_row(scan, k, ["vas", "hisna", "ime"], f"trak-{label}", scale=2.2)

# ZMEDE-celice ×3.0
cells = [
 (109, 0,  ["ime", "bolez", "podpis"], "s109-z1"),   # Brodarič/Brinec + Nadruka + Florjančič
 (109, 1,  ["ime", "bolez"],           "s109-z2"),   # Željko + Kasek
 (109, 3,  ["ime", "star", "bolez"],   "s109-z4"),   # Hleu/Mec + 16-let + Pljučnica
 (109, 8,  ["ime", "bolez", "podpis"], "s109-z9"),   # pri-Jovanek + Pezdirec-stan
 (109, 10, ["ime", "bolez"],           "s109-z11"),  # Brišek/Drišek + Kasek
 (110, 1,  ["ime", "bolez"],           "s110-z13"),  # Željko/Veljko + Kasek
 (110, 6,  ["smrt", "pokop", "ime"],   "s110-z18"),  # smrt-29-Feb! + Urh
 (111, 3,  ["ime", "bolez"],           "s111-z27"),  # Šimec/Štrmec + Štuimec
 (111, 8,  ["ime", "bolez"],           "s111-z32"),  # Kumič + Kaikel
 (112, 0,  ["ime", "star"],            "s112-z36"),  # r-Dragos + ovozena-Škambič
 (112, 1,  ["ime", "bolez", "vas"],    "s112-z37"),  # Šimec + Ubel-opreklin
 (112, 3,  ["ime", "bolez"],           "s112-z39"),  # Mlek + Kasek
 (113, 5,  ["ime", "star"],            "s113-z53"),  # Toček + venčen
 (113, 7,  ["ime", "bolez"],           "s113-z55"),  # Kruše/Kroše
 (113, 8,  ["ime", "star"],            "s113-z56"),  # rojena-? omožena-?
 (113, 9,  ["hisna", "ime"],           "s113-z57"),  # h49-vs-h40 + Brodarič
 (113, 10, ["ime", "bolez"],           "s113-z58"),  # Ogrince/Brince
 (113, 11, ["smrt", "pokop", "ime"],   "s113-z59"),  # 2./14. + Pezdirec
 (114, 3,  ["ime", "podpis"],          "s114-z63"),  # Brince/Vrhnar + Lilek
 (114, 5,  ["ime", "podpis"],          "s114-z65"),  # Brinec + Cerar
]
for scan, k, cols, label in cells:
    crop_row(scan, k, cols, label)

# PODPISI
for scan, k, label in [(111, 11, "s111-z35"), (112, 6, "s112-z42"),
                       (113, 0, "s113-z48"), (109, 2, "s109-z3"), (114, 2, "s114-z62")]:
    crop_row(scan, k, ["podpis"], label, ypad=8)

print("crops-v2:", len(os.listdir(OUT)), "datotek")
