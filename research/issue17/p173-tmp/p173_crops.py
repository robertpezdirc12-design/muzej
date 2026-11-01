#!/usr/bin/env python3
"""P173 crops — celice ×3.0 + glave + podpisi (P172 recept ×2.2/×3.0).
Vrstica k (0-based): y = [330 + k*135, 330 + (k+1)*135]."""
import os
from PIL import Image, ImageDraw, ImageFont

DIR = "/tmp/p173"
OUT = os.path.join(DIR, "crops")
os.makedirs(OUT, exist_ok=True)

# x-stolpci (diag-osi, širina 2659)
X = dict(zap=(90, 170), mesec=(170, 340), smrt=(340, 490), pokop=(490, 630),
         vas=(620, 840), hisna=(830, 970), ime=(950, 1570), star=(1550, 1790),
         bolez=(1770, 2140), prev=(2120, 2270), podpis=(2250, 2560), opomba=(2520, 2660))

def row_y(scan, k):
    return 330 + k * 135 - 10, 330 + (k + 1) * 135 + 10

def crop(scan, k, cols, scale=3.0, name=None, ypad=0):
    p = f"{DIR}/s{scan}.jpg"
    im = Image.open(p)
    y0, y1 = row_y(scan, k)
    y0 -= ypad; y1 += ypad
    for col in cols:
        x0, x1 = X[col]
        c = im.crop((x0, max(0, y0), min(im.width, x1), min(im.height, y1)))
        c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS)
        out = f"{OUT}/{name or (f'cell-s{scan}-{col}-k{k}')}.png"
        c.save(out)
    return True

def crop_glava(scan, x0=170, x1=830, y0=60, y1=210, scale=3.0):
    im = Image.open(f"{DIR}/s{scan}.jpg")
    c = im.crop((x0, y0, x1, y1))
    c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS)
    c.save(f"{OUT}/glava-s{scan}.png")

def crop_full(scan, k, label, x0, x1, scale=3.0, ypad=12):
    im = Image.open(f"{DIR}/s{scan}.jpg")
    y0, y1 = row_y(scan, k)
    y0 -= ypad; y1 += ypad
    c = im.crop((x0, max(0, y0), min(im.width, x1), min(im.height, y1)))
    c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS)
    c.save(f"{OUT}/{label}.png")

# ——— GLAVE (4: s109 potrditev-P172 + s111-cifra? + s112-necel? + s114-meja) ———
crop_glava(109); crop_glava(111); crop_glava(112); crop_glava(113); crop_glava(114)

# ——— GRIBLJE-IME+VAS+HIŠNA trakovi ×2.2 (vseh 20!) ———
grib = [
 (109, 0,  "z1-Anton-Brodaric-Brinec-h49"), (109, 1, "z2-Ana-Zeljko-h1"),
 (109, 3,  "z4-Ana-Hleu-Mec-h91"),          (109, 4, "z5-Barbara-Pezdirec-h87"),
 (109, 8,  "z9-Marija-pri-Jovanek-h52"),    (109, 10, "z11-Alojzij-Brisek-h31"),
 (110, 1,  "z13-Anton-Zeljko-Veljko-h60"),  (110, 6, "z18-Matija-Urh-h32"),
 (111, 3,  "z27-Marija-Simec-Strmec-h14"),  (111, 8, "z32-Marija-Kumic-h11"),
 (112, 0,  "z36-Marija-r-Dragos-h74"),      (112, 1, "z37-Matija-Simec-h75"),
 (112, 3,  "z39-Matija-Mlek-h65"),
 (113, 5,  "z53-Jurij-Tocek-h28"),          (113, 7, "z55-Ana-Kruse-h19"),
 (113, 8,  "z56-Ana-rojena-omozena-h21"),   (113, 9, "z57-Nikolaj-Brodaric-h49-40"),
 (113, 10, "z58-Matija-Ogrince-h25"),       (114, 3, "z63-Anton-Brince-Vrhnar-h10"),
 (114, 5,  "z65-Jozef-Brinec-h10"),
]
for scan, k, label in grib:
    crop_full(scan, k, f"trak-{label}", 620, 1600, scale=2.2)

# ——— ZMEDE-celice ×3.0 ———
cells = [
 (109, 0,  ["ime", "bolez", "prev"],   "s109-z1-ime-bolez"),     # Brodarič/Brinec + Nadruka
 (109, 1,  ["ime", "bolez"],           "s109-z2-ime-bolez"),     # Željko + Kasek
 (109, 3,  ["ime", "star", "bolez"],   "s109-z4-ime-star"),      # Hleu/Mec + 16-let?
 (109, 8,  ["ime", "bolez", "podpis"], "s109-z9-ime-stan"),      # pri-Jovanek + Pezdirec
 (109, 10, ["ime", "bolez"],           "s109-z11-ime-bolez"),    # Brišek/Drišek
 (110, 1,  ["ime", "bolez"],           "s110-z13-ime-bolez"),    # Željko/Veljko
 (110, 6,  ["smrt", "pokop", "ime"],   "s110-z18-datum-ime"),    # smrt-29-Feb!
 (111, 3,  ["ime", "bolez"],           "s111-z27-ime-bolez"),    # Šimec/Štrmec
 (111, 8,  ["ime", "bolez"],           "s111-z32-ime-bolez"),    # Kumič + Kaikel
 (112, 0,  ["ime", "star"],            "s112-z36-ime-stan"),     # r-Dragos + ovozena
 (112, 1,  ["ime", "bolez"],           "s112-z37-ime-bolez"),    # Šimec + Ubel-opreklin
 (112, 3,  ["ime", "bolez"],           "s112-z39-ime-bolez"),    # Mlek + Kasek
 (113, 5,  ["ime", "star"],            "s113-z53-ime-stan"),     # Toček + venčen
 (113, 7,  ["ime", "bolez"],           "s113-z55-ime"),          # Kruše/Kroše
 (113, 8,  ["ime", "star"],            "s113-z56-ime-stan"),     # rojena-? omožena-?
 (113, 9,  ["vas", "hisna", "ime"],    "s113-z57-hisna-ime"),    # h49-vs-h40!
 (113, 10, ["ime", "bolez"],           "s113-z58-ime"),          # Ogrince/Brince
 (113, 11, ["smrt", "pokop", "ime"],   "s113-z59-datum-ime"),    # 2./14. + Pezdirec
 (114, 3,  ["ime", "podpis"],          "s114-z63-ime-podpis"),   # Brince/Vrhnar + Lilek
 (114, 5,  ["ime", "podpis"],          "s114-z65-ime-podpis"),   # Brinec + Cerar
]
for scan, k, cols, label in cells:
    crop(scan, k, cols, scale=3.0, name=label)

# ——— PODPISI ×3.0 (Lilek-župnik? + Šuida-Šuič + Dostál + z35-brez) ———
sigs = [
 (111, 11, "s111-z35-podpis-brez"),
 (112, 6,  "s112-z42-podpis-Suida-Suic"),
 (113, 0,  "s113-z48-podpis-Lilek"),
 (109, 2,  "s109-z3-podpis-Dostal"),
]
for scan, k, label in sigs:
    crop(scan, k, ["podpis"], scale=3.0, name=label)

n = len(os.listdir(OUT))
print(f"crops: {n} datotek v {OUT}")
