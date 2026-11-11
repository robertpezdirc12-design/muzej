#!/usr/bin/env python3
"""P254 — posodobitev STARIH verifikatorjev na 248 kontrol (P254 je dodal 248. kontrolo
qa-p254-parish-house-stories!). Zadeva: p243/p244/p246/p247/p248/p252 I10-QA-živo
trditve passed == 247 → 248 (+ sporočila '247/247' → '248/248')."""
import re

FILES = [
    "scripts/p243_parish_marriage_1880_04455.py",
    "scripts/p244_parish_marriage_1879_04455.py",
    "scripts/p246_parish_marriage_1878_04455.py",
    "scripts/p247_parish_marriage_1877_04455.py",
    "scripts/p248_parish_marriage_1876_04455.py",
    "scripts/p252_parish_synthesis_04455.py",
]

total = 0
for f in FILES:
    src = open(f, encoding="utf-8").read()
    orig = src
    # pogoj: passed == 247 → 248
    src = src.replace('qa_data.get("passed") == 247', 'qa_data.get("passed") == 248')
    src = src.replace('qa_live.get("passed") == 247', 'qa_live.get("passed") == 248')
    # sporočila: 247/247 → 248/248 (samo v I10-QA kontekstu — ne s247/skanov!)
    src = re.sub(r'I10 QA-živo 247/247', 'I10 QA-živo 248/248', src)
    src = re.sub(r'I10 LIVE qa ok=True \(247/247', 'I10 LIVE qa ok=True (248/248', src)
    src = re.sub(r'QA-živo 247/247 ok:True', 'QA-živo 248/248 ok:True', src)
    if src != orig:
        n = sum(1 for a, b in zip(orig.split("\n"), src.split("\n")) if a != b)
        open(f, "w", encoding="utf-8").write(src)
        total += n
        print(f"{f}: {n} vrstic posodobljenih")
    else:
        print(f"{f}: BREZ sprememb (preveri ročno!)")

print(f"\nSkupaj: {total} vrstic")
