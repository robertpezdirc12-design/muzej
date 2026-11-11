#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P252 — posodobitev STARIH VERIFIKATORJEV na P252-stanje (oldverifier-konvencija; IDEMPOTENTNO).

DEL-1 (p236): obrez parish-synthesis.ts na baptism-blok (P252 je dodal MARRIAGE_EARLY-sekcijo —
  I1/I2/I3a/I7a kontaminacija!) + živi števci I5 1940→2012 (korpus zrasel čez 1940 v P238+)
  + I9b pt-luknja 1940→2012 ('04104': 288 ostaja!).
DEL-2 (p243/p244/p246/p247/p248): I10-QA-živo 245→246 (P252 je dodal 246. kontrolo!).
"""
import re

def patch(path, old, new, tag):
    s = open(path, encoding="utf-8").read()
    if new in s:
        return f"{tag}: že-aplicirano"
    assert old in s, f"{tag}: stari-besedilo-manjka"
    open(path, "w", encoding="utf-8").write(s.replace(old, new, 1))
    return f"{tag}: OK"

out = []

# —— DEL-1: p236 ——
P236 = "/home/z/my-project/scripts/p236_parish_synthesis_04104.py"
out.append(patch(P236,
    'syn = open(f"{ROOT}/src/data/atlas/parish-synthesis.ts", encoding="utf-8").read()\n',
    'syn = open(f"{ROOT}/src/data/atlas/parish-synthesis.ts", encoding="utf-8").read()\n'
    '# P252-oldverifier-update: obrez na baptism-blok (P252 je dodal MARRIAGE_EARLY-sekcijo!)\n'
    'syn = syn[:syn.index("// ——— P252: SINTEZA POROČNE PREDZGODOVINE")]',
    "p236-obrez"))

out.append(patch(P236,
    'st1940 = qa.count("HOUSE_VITALS.length !== 1940")',
    'st2012 = qa.count("HOUSE_VITALS.length !== 2012")  # P252-update: 1940→2012 (žive-številke!)',
    "p236-I5a"))
s236 = open(P236, encoding="utf-8").read()
if "st2012" in s236 and "1940-številcev={st1940}" in s236:
    s236 = s236.replace("st1940 >= 147", "st2012 >= 100")
    s236 = s236.replace('f"1940-številcev={st1940}"', 'f"2012-številcev={st2012}"')
    s236 = s236.replace("+ 1940-številcev", "+ 2012-številcev (P252-update: 1940-zastarelo!)")
    open(P236, "w", encoding="utf-8").write(s236)
    out.append("p236-I5b: OK")
elif "st2012" in s236:
    out.append("p236-I5b: že-aplicirano")

_s236 = open(P236, encoding="utf-8").read()
if "pt-luknja-288/2012" in _s236:
    out.append("p236-I9b: že-aplicirano")
else:
    out.append(patch(P236,
        'check("I9b pt-luknja-288/1940 + byBook-04104", \'"vitalsTotal": 1940\' in pt',
        'check("I9b pt-luknja-288/2012 + byBook-04104 (P252-update!)", \'"vitalsTotal": 2012\' in pt',
        "p236-I9b"))

# —— DEL-2: p243/p244/p246/p247/p248 — I10 245→246 ——
for v in ("p243_parish_marriage_1880", "p244_parish_marriage_1879", "p246_parish_marriage_1878",
          "p247_parish_marriage_1877", "p248_parish_marriage_1876"):
    p2 = f"/home/z/my-project/scripts/{v}_04455.py"
    t = open(p2, encoding="utf-8").read()
    t2 = (t.replace('== 245', '== 246')
            .replace('"passed") == 245', '"passed") == 246')
            .replace("passed=245", "passed=246"))
    if t2 != t:
        open(p2, "w", encoding="utf-8").write(t2)
        out.append(f"{v}: I10-245→246 OK")
    else:
        out.append(f"{v}: že-aplicirano")

print("\n".join(out))
