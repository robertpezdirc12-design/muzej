#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P177 crops — celice ×3.0 + traki ×2.2 + glave (P173/P176 recept).
Band-k = 330 + 135*k (0-based vrstica na skenu; P172-recept, 100% veljaven
za 1910 na s126–s130 = isti tiskarski nabor!). P177 vrsticna mapa:
  s130: k6=z1(1911) … k9=z4-MRTVOROJENEC, k10=z5
  s131: k0=z6 … k7=z13-BRINEC, k8=z14-HRUŠIČ … k11=z17
  s132: k0=z18 … k6=z24-PEZDIREC, k8=z26-PEZDIREC, k9=z27-PEZDIREC
  s133: k0=z30-TAPARIČ, k1=z31-MAVRIČ-96?, k6=z36-TAPARIČ … k11=z41
  s134: k0=z42-VRŠIČ, k4=z46-HROVAT, k5=z47-NEPOMUK?, k6=z48-BIRČEC?, k9=z51-PERDIH
  s135: k0=z54-FOŠELJ, k1=z55-VLOBUČAR?, k2=z56-JURAČEVIČ, k5=MEJA-1911/12, k6=1912-z1
"""
import os
from PIL import Image, ImageDraw

DIR = "/tmp/p177"
OUT = os.path.join(DIR, "crops")
os.makedirs(OUT, exist_ok=True)

# x-stolpci (diag-osi, širina 2659 — P173 recept)
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
    outs = []
    for col in cols:
        x0, x1 = X[col]
        c = im.crop((x0, max(0, y0), min(im.width, x1), min(im.height, y1)))
        c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS)
        out = f"{OUT}/{name or (f'cell-s{scan}-{col}-k{k}')}.png"
        c.save(out)
        outs.append(os.path.basename(out))
    return outs


def crop_trak(scan, k, label, x0=620, x1=1570, scale=2.2, ypad=8):
    """vas+hisa+ime trak (P172 ×2.2)."""
    im = Image.open(f"{DIR}/s{scan}.jpg")
    y0, y1 = row_y(scan, k)
    y0 -= ypad; y1 += ypad
    c = im.crop((x0, max(0, y0), min(im.width, x1), min(im.height, y1)))
    c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS)
    c.save(f"{OUT}/{label}.png")


def crop_full(scan, k, label, x0, x1, scale=2.2, ypad=12):
    im = Image.open(f"{DIR}/s{scan}.jpg")
    y0, y1 = row_y(scan, k)
    y0 -= ypad; y1 += ypad
    c = im.crop((x0, max(0, y0), min(im.width, x1), min(im.height, y1)))
    c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS)
    c.save(f"{OUT}/{label}.png")


def crop_glava(scan, x0=170, x1=830, y0=60, y1=210, scale=3.0):
    im = Image.open(f"{DIR}/s{scan}.jpg")
    c = im.crop((x0, y0, x1, y1))
    c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS)
    c.save(f"{OUT}/glava-s{scan}.png")


# ——— 1. GRIBLJE-traki ×2.2 (vseh 16!) ———
crop_trak(131, 7, "trak-z13-ana-brinec-h14")
crop_trak(131, 8, "trak-z14-katarina-hrusic-h34")
crop_trak(132, 6, "trak-z24-ana-pezdirec-h10")
crop_trak(132, 8, "trak-z26-janez-pezdirec-h42")
crop_trak(132, 9, "trak-z27-vidou-pezdirec-h48")
crop_trak(133, 0, "trak-z30-marija-taparic-h33")
crop_trak(133, 1, "trak-z31-marija-mavric-h57")
crop_trak(133, 6, "trak-z36-marija-taparic-h33")
crop_trak(134, 0, "trak-z42-marija-vrsic-h14")
crop_trak(134, 4, "trak-z46-neza-hrovat-h41")
crop_trak(134, 5, "trak-z47-nikolaj-nepomuk-h43")
crop_trak(134, 6, "trak-z48-matija-bircec-h14")
crop_trak(134, 9, "trak-z51-peter-perdih-h20")
crop_trak(135, 0, "trak-z54-janez-foselj-h31")
crop_trak(135, 1, "trak-z55-katarina-vlobucar-h46")
crop_trak(135, 2, "trak-z56-margareta-juracevic-h24")
# + s130-z4-mrtvorojenec (1911) full trak
crop_trak(130, 9, "trak-z4-mrtvorojenec-s130")
# + P178-lead: 1912 z1 Pečnik (s135 k6)
crop_trak(135, 6, "trak-1912-z1-jozef-pecnik-h87")

# ——— 2. FORENZIKA-celice ×3.0 ———
crop(133, 0, ["star"], name="cel-z30-starost-95let")
crop(133, 1, ["star"], name="cel-z31-starost-96let")
crop(134, 6, ["ime"], name="cel-z48-ime")             # Birčec?
crop(134, 6, ["bolez"], name="cel-z48-bolezen")      # Opeklina?
crop(134, 5, ["ime"], name="cel-z47-ime")            # Nepomuk?
crop(135, 1, ["ime"], name="cel-z55-ime")            # Vlobučar?
crop(135, 0, ["ime"], name="cel-z54-ime")            # Fošelj?
crop(133, 6, ["ime"], name="cel-z36-ime")            # Taparič-otrok?
crop(133, 0, ["mesec", "smrt", "pokop"], name="cel-z30-datum")
crop(131, 7, ["star", "bolez"], name="cel-z13-starost-bolezen")
crop(132, 9, ["star"], name="cel-z27-starost")

# ——— 3. GLAVE + MEJA ———
crop_glava(133)
crop_glava(134)
crop_glava(135)
crop_glava(136)
# meja s135 k5 (celotna vrsta + okoli nje)
crop_full(135, 5, "meja-s135-k5-full", 90, 2660, scale=2.2)

# ——— 4. PODPISI (duhovnik-forenzika) ———
crop(133, 0, ["podpis"], name="pod-z30-rauq")
crop(133, 1, ["podpis"], name="pod-z31-pithar")
crop(134, 0, ["podpis"], name="pod-z42-pihnar")
crop(131, 7, ["podpis"], name="pod-z13-bitmar")

print("crops:", len(os.listdir(OUT)))
for f in sorted(os.listdir(OUT)):
    print(" ", f)
