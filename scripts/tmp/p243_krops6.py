#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P243 — pass-6: ultra-zoom kritičnih celic + s38 Pag-koti + fini-vsota."""
import os
from PIL import Image

OUT = "/tmp/p243/crops6"
os.makedirs(OUT, exist_ok=True)

im35 = Image.open("/tmp/p243/s35.jpg")
im36 = Image.open("/tmp/p243/s36.jpg")
im37 = Image.open("/tmp/p243/s37.jpg")
im38 = Image.open("/tmp/p243/s38.jpg")

def cs(im, box, name, scale):
    c = im.crop(box)
    c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS)
    c.save(f"{OUT}/{name}.jpg", quality=93)
    print(name, c.size)

# 1) s35 numcol dno-zona (31,32,33,1,2) 4×
cs(im35, (60, 1000, 300, 1750), "s35-numcol-dno-4x", 4)
# 2) s35 dno vrsti 1–2 polni trakovi (hipoteza: 5 vrstic od y~1050)
cs(im35, (0, 1000, 1300, 1800), "s35-dno-L", 2)
cs(im35, (1250, 1000, 2449, 1800), "s35-dno-R", 2)
# 3) s36 r3 celica (y~300-500): vas+hiša+ime (levo) 
cs(im36, (0, 290, 1300, 520), "s36-r3-L", 2.2)
# 4) s36 r4 celica: Mathias Brine Griblje 24?
cs(im36, (0, 500, 1300, 730), "s36-r4-L", 2.2)
# 5) s36 vas-stolpec vseh vrst (x~260-700 y300-1700) — hiše na enkrat
cs(im36, (260, 280, 720, 1700), "s36-vascol-2.5x", 2.5)
# 6) s37 r6 celica (Griblje 63 × Pegdirec): y~1388-1632
cs(im37, (0, 1380, 1300, 1650), "s37-r6-L", 2.4)
cs(im37, (1250, 1380, 2453, 1650), "s37-r6-R", 2.4)
# 7) s38 r6 celica (Griblje 53): y~1388-1632
cs(im38, (0, 1380, 1300, 1650), "s38-r6-L", 2.4)
cs(im38, (1250, 1380, 2458, 1650), "s38-r6-R", 2.4)
# 8) s38 dno fini/vsota sredina
cs(im38, (0, 1580, 2458, 1800), "s38-dno-fini", 2)
# 9) s38 Pag koti (grid 4 kotov)
w, h = im38.size
corners = [(0,0,700,300,"TL"), (w-700,0,w,300,"TR"), (0,h-300,700,h,"BL"), (w-700,h-300,w,h,"BR")]
for (x0,y0,x1,y1,tag) in corners:
    cs(im38, (x0,y0,x1,y1), f"s38-kot-{tag}", 3)
# 10) s39 kot TR za primerjavo (Pag. 38 P242)
im39 = Image.open("/tmp/p243/s39.jpg")
cs(im39, (2453-700, 0, 2453, 300), "s39-kot-TR", 3)
print("DONE")
