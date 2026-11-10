#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P243 — pass-5: s35 (hipoteza restart-1880 = s35-dno) + s36-top zona."""
import os
from PIL import Image

OUT = "/tmp/p243/crops5"
os.makedirs(OUT, exist_ok=True)

im35 = Image.open("/tmp/p243/s35.jpg")
w, h = im35.size
print("s35:", im35.size)

# s35: numcol cel + dno + glava
c = im35.crop((60, 0, 260, 1700))
c = c.resize((c.width * 3, c.height * 3), Image.LANCZOS)
c.save(f"{OUT}/s35-numcol-full-3x.jpg", quality=93)

d = im35.crop((0, 1300, w, 1800))  # dno strani
d = d.resize((d.width * 2, d.height * 2), Image.LANCZOS)
d.save(f"{OUT}/s35-dno.jpg", quality=92)

g = im35.crop((0, 0, 1400, 400))
g = g.resize((int(g.width * 2.2), int(g.height * 2.2)), Image.LANCZOS)
g.save(f"{OUT}/s35-glava-zona.jpg", quality=92)

# s36: top zona 0–700 v 2 pasova (letnica + vrste 1–2?)
im36 = Image.open("/tmp/p243/s36.jpg")
t = im36.crop((0, 0, 2457, 700))
t = t.resize((int(t.width * 1.6), int(t.height * 1.6)), Image.LANCZOS)
t.save(f"{OUT}/s36-top-1.6x.jpg", quality=92)

n2 = im36.crop((60, 0, 700, 760))
n2 = n2.resize((n2.width * 3, n2.height * 3), Image.LANCZOS)
n2.save(f"{OUT}/s36-top-zona-3x.jpg", quality=93)

# s35 datum stolpec top + dno
d2 = im35.crop((260, 0, 760, 500))
d2 = d2.resize((d2.width * 3, d2.height * 3), Image.LANCZOS)
d2.save(f"{OUT}/s35-datumcol-top-3x.jpg", quality=93)
d3 = im35.crop((260, 1250, 760, 1800))
d3 = d3.resize((d3.width * 3, d3.height * 3), Image.LANCZOS)
d3.save(f"{OUT}/s35-datumcol-dno-3x.jpg", quality=93)
print("DONE")
