#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P225-sanitizacija-2: yearset-P221/P222/P223-blokov ({1882..1885} → {1881..1885}) + p85-izjema-h38-1881 (z30-PIRCER!)."""
from pathlib import Path
ROOT = Path("/home/z/my-project")
QA = ROOT / "src/lib/qa-parish.ts"
src = QA.read_text(encoding="utf-8")

old_y = 'if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)\n    p221Errors.push("04104-bloki izven {1882, 1883, 1884, 1885} (predzgodovina-4/15: 1882–1885-do-P225!)");'
new_y = 'if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)\n    p221Errors.push("04104-bloki izven {1881, 1882, 1883, 1884, 1885} (predzgodovina-5/15: 1881–1885-do-P226!)");'
n1 = src.count(old_y)
src = src.replace(old_y, new_y)
old_y2 = old_y.replace("p221Errors", "p222Errors")
new_y2 = new_y.replace("p221Errors", "p222Errors")
n2 = src.count(old_y2)
src = src.replace(old_y2, new_y2)
old_y3 = old_y.replace("p221Errors", "p223Errors")
new_y3 = new_y.replace("p221Errors", "p223Errors")
n3 = src.count(old_y3)
src = src.replace(old_y3, new_y3)
print(f"yearset-patched: p221={n1} p222={n2} p223={n3}")

# p85-izjema: + h38-1881 (z30-Georg-PIRCER-Griblje!-9-let-pred-prvencem-1890!)
old_ex = '&& !(v.bookSignature === "04104" && v.year === 1882 && hn === "41")'
new_ex = '&& !(v.bookSignature === "04104" && v.year === 1882 && hn === "41") && !(v.bookSignature === "04104" && v.year === 1881 && hn === "38")'
n4 = src.count(old_ex)
src = src.replace(old_ex, new_ex)
old_c = "// P224: + izjema-04104-1882-h41 (z58-Maria-IGREC!-8-let-pred-prvencem-1890!)"
new_c = old_c + "\n// P225: + izjema-04104-1881-h38 (z30-Georg-PIRCER[?]-Griblje!-9-let-pred-prvencem-1890!)"
n5 = src.count(old_c)
src = src.replace(old_c, new_c)
print(f"p85-izjema-patched: condition={n4} comment={n5}")
QA.write_text(src, encoding="utf-8")
