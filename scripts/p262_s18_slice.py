#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P262 — s18 slicing (AGENT-VIZIJA metodika P259/P260/P261 — 0 VLM klicev).
s18 = Pag. 33/34 (foliacija Pag = 2·sken − 3 — serija 15/15) — 1837-nadaljevanje (m6+).
Izhod: research/issue17/p262-work/ — margin + 3 horizontalne slise × L/R + celotni L/R + full."""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = f"{ROOT}/research/issue17/p261-work/s18.jpg"
OUT = f"{ROOT}/research/issue17/p262-work"
os.makedirs(OUT, exist_ok=True)

p = subprocess.run([sys.executable, "-c", f"from PIL import Image; im=Image.open('{SRC}'); print(im.size)"],
                   capture_output=True, text=True)
w, h = map(int, p.stdout.strip().strip("()").split(","))
print(f"s18 velikost: {w}x{h}")

def pil(code):
    subprocess.run([sys.executable, "-c", code], check=True)

pil(f"from PIL import Image; Image.open('{SRC}').save('{OUT}/s18_full.png')")
pil(f"from PIL import Image; im=Image.open('{SRC}'); im.crop((0,0,{w//2+60},{h})).save('{OUT}/s18_L.png')")
pil(f"from PIL import Image; im=Image.open('{SRC}'); im.crop(({w//2-60},0,{w},{h})).save('{OUT}/s18_R.png')")
pil(f"from PIL import Image; im=Image.open('{SRC}'); im.crop((0,0,int({w}*0.16),{h})).resize((int({w}*0.16)*2,{h}*2)).save('{OUT}/s18_margins.png')")
# 3 horizontalne slise × L/R
b1, b2 = h // 3, 2 * h // 3
pil(f"from PIL import Image; im=Image.open('{SRC}'); im.crop((0,0,{w//2+60},{b1})).save('{OUT}/s18_sliceA_L.png')")
pil(f"from PIL import Image; im=Image.open('{SRC}'); im.crop(({w//2-60},0,{w},{b1})).save('{OUT}/s18_sliceA_R.png')")
pil(f"from PIL import Image; im=Image.open('{SRC}'); im.crop((0,{b1},{w//2+60},{b2})).save('{OUT}/s18_sliceB_L.png')")
pil(f"from PIL import Image; im=Image.open('{SRC}'); im.crop(({w//2-60},{b1},{w},{b2})).save('{OUT}/s18_sliceB_R.png')")
pil(f"from PIL import Image; im=Image.open('{SRC}'); im.crop((0,{b2},{w//2+60},{h})).save('{OUT}/s18_sliceC_L.png')")
pil(f"from PIL import Image; im=Image.open('{SRC}'); im.crop(({w//2-60},{b2},{w},{h})).save('{OUT}/s18_sliceC_R.png')")

print("slicing OK:", sorted(os.listdir(OUT)))
