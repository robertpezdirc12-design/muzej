#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P235 — KOM-marker popravki v parish.ts (z13-MEJA-1870/71 + DUPLIKAT-s3 + z103-MEJA-1871/72)."""
from pathlib import Path

TS = Path("/home/z/my-project/src/data/atlas/parish.ts")
src = TS.read_text(encoding="utf-8")

# z13 KOM: dodaj MEJA-1870/71 + DUPLIKAT-s3 markerja
old = "★★★ 1.-GRIBLJE-1871 = z13 (Februar!-Jänner-×0-GRIBLJE!-vs-1872-1.-vpis-leta-GRIBLJE-z1!-VZOREC-PREKINJEN!) + BRINE-matec-nit"
new = "★★★ 1.-GRIBLJE-1871 = z13 (Februar!-Jänner-×0-GRIBLJE!-vs-1872-1.-vpis-leta-GRIBLJE-z1!-VZOREC-PREKINJEN!) + ★★★ MEJA-1870/71 = ZAČETEK-KNJIGE (s1-vezava!-s2-naslovna-'Tauf-Buch.'!-arhivski-nalepek-'PODZEMELJ-R-1871-1885'!-restart-z1-NA-s3-r1-Jänner-3-KRASINEC!-13.-restart!-1.-vpis-leta = KRASINEC-NOT-GRIBLJE!-X-kontrola!) + ★★★ DUPLIKAT-s3 = s4-RESITEV (fol-1-2×!-P234-'1-DUPLIKAT-s1–s13'-UGE-REŠENA!-s3-r1 = s4-r1-'Jänner-3'-1:1!) + BRINE-matec-nit"
assert src.count(old) == 1, f"z13 count={src.count(old)}"
src = src.replace(old, new)

# z103 KOM: dodaj MEJA-1871/72 marker
old2 = "★★★ TAIL-1871 = z108 (z103-pred-tail-GRIBLJE!-Dez-22!) + KUKE-DVOJNI"
new2 = "★★★ TAIL-1871 = z108 (z103-pred-tail-GRIBLJE!-Dez-22!) + ★★★ MEJA-1871/72 = s13/s14-PAGE-BOUNDARY (P234-1:1!-re-use!-restart-z1-NA-s14-r1-Jänner-5-GRIBLJE!-12.-restart-P234-SUPER!-BREZ-'finis-Anni-1871'-kalligrafije-Q4-5/5!-plain-PARALELA-1872!) + KUKE-DVOJNI"
assert src.count(old2) == 1, f"z103 count={src.count(old2)}"
src = src.replace(old2, new2)

TS.write_text(src, encoding="utf-8")
print("parish.ts patched (z13-MEJA-1870/71 + DUPLIKAT-s3 + z103-MEJA-1871/72)")
