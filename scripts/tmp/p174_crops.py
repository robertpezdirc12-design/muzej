#!/usr/bin/env python3
"""P174 crops — traki ×2.2 (vas+hisna+ime za Griblje) + celice ×3.0 (zmede)
+ glave ×9 + meja-s121. Recept p173_crops2.py; k = diag-row (R0=vrsta-0)."""
import os
from PIL import Image

DIR = "/tmp/p174"
OUT = os.path.join(DIR, "crops")
os.makedirs(OUT, exist_ok=True)

X = dict(zap=(140, 230), mesec=(260, 440), smrt=(290, 430), pokop=(430, 580),
         vas=(580, 800), hisna=(770, 950), ime=(880, 1450), star=(1500, 1750),
         bolez=(1720, 2100), prev=(2080, 2200), podpis=(2160, 2480),
         opomba=(2480, 2660), meja=(140, 1500))


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


# GLAVE ×9
for s in range(114, 123):
    crop_glava(s)

# MEJA 1908/09 (s121 R1 — velike cifre)
crop_row(121, 1, ["meja"], "meja-s121-1909", scale=2.2)

# GRIBLJE-traki ×2.2
grib = [
 (115, 6,  "z10-Doroteja-Pezdirec-h42-STAROST"),
 (116, 0,  "z16-Marijeta-Brinec-h24"),
 (116, 4,  "z20-Ana-Pupric-h3"),
 (116, 9,  "z25-Jozef-Perdinec-h85-POROD"),
 (118, 2,  "z42-Anton-Brinec-h83"),
 (118, 7,  "z47-Peter-Hrovat-h44-SAMOMOR"),
 (119, 2,  "z54-Mihael-Tapric-h2"),
 (119, 7,  "z59-Marija-Tapric-h33"),
 (120, 0,  "z64-Avgustin-Jurajcic-h34"),
 (120, 6,  "z70-Katarina-Perdinec-h20"),
 (120, 7,  "z71-Matija-Perdinec-h30"),
 (120, 8,  "z72-Marija-Stancej-h5"),
 (120, 11, "z75-Barbara-Mlech-h39"),
]
for scan, k, label in grib:
    crop_row(scan, k, ["vas", "hisna", "ime"], f"trak-{label}", scale=2.2)

# ZMEDE-celice ×3.0
cells = [
 (115, 0,  ["podpis", "opomba", "ime"], "s115-z4-MatijaCerar-dekan"),
 (115, 4,  ["star"],                    "s115-z8-prazna-starost"),
 (115, 5,  ["ime", "bolez"],            "s115-z9-Stiparic-Kapljevode"),
 (115, 6,  ["star"],                    "s115-z10-51-vs-81"),
 (116, 2,  ["ime", "star"],             "s116-z18-Pricek-43-vs-45"),
 (116, 6,  ["ime"],                     "s116-z22-Brodaric-sin"),
 (116, 10, ["ime"],                     "s116-z26-Jely-Pibernik"),
 (117, 1,  ["ime"],                     "s117-z29-Weber-stan"),
 (117, 3,  ["vas", "ime", "podpis"],    "s117-z31-Vosman-Mrtvorojen"),
 (117, 8,  ["vas", "ime", "bolez"],     "s117-z36-Tome-Bozjast"),
 (118, 5,  ["vas", "ime"],              "s118-z45-Serkopec-Kloster"),
 (118, 6,  ["ime", "star"],             "s118-z46-Jelicic-64-vs-84"),
 (118, 8,  ["bolez"],                   "s118-z48-Telacna-mrzlica"),
 (118, 9,  ["ime", "bolez"],            "s118-z49-Vedaric-Bozjast"),
 (118, 10, ["ime"],                     "s118-z50-Kajetana"),
 (118, 11, ["hisna", "star", "bolez"],  "s118-z51-h109-Prirojena"),
 (119, 1,  ["bolez"],                   "s119-z53-Dobrei"),
 (119, 2,  ["ime"],                     "s119-z54-Tapric-stan"),
 (119, 5,  ["ime", "bolez", "prev"],    "s119-z57-padel-ubil"),
 (119, 7,  ["ime"],                     "s119-z59-Tapric"),
 (119, 8,  ["ime"],                     "s119-z60-Perman-Boznar"),
 (119, 11, ["ime", "bolez"],            "s119-z63-Uhr-Dobrei"),
 (120, 2,  ["ime", "bolez"],            "s120-z66-Zmavc-Mrtvoud"),
 (120, 3,  ["ime"],                     "s120-z67-Perdinec-Otok"),
 (120, 5,  ["ime", "star", "bolez"],    "s120-z69-Kozijan-Sicki-porod"),
 (120, 6,  ["ime"],                     "s120-z70-Perdinec"),
 (120, 7,  ["ime"],                     "s120-z71-Perdinec-Griblje"),
 (120, 8,  ["ime", "star", "smrt"],     "s120-z72-Stancej-44"),
 (120, 10, ["ime"],                     "s120-z74-Straf-Wolf"),
 (120, 11, ["ime", "bolez"],            "s120-z75-Mlech-Nemoglost"),
 (121, 0,  ["star", "ime"],             "s121-z76-Stefanjic-4let"),
]
for scan, k, cols, label in cells:
    crop_row(scan, k, cols, label)

# PODPISI ('rog.' suffiksi)
for scan, k, label in [(119, 0, "s119-z52-Cerar-rog"), (120, 0, "s120-z64-Cerar-rog")]:
    crop_row(scan, k, ["podpis"], label, ypad=8)

print("crops:", len(os.listdir(OUT)), "datotek")
