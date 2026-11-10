#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P237 — verifikator FORENZIKE NITI: MILIČ↔MILEK križ · h69 zgodba · duhovniški križ (I1–I10 + --live)."""
import re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

# kurirani MILIČ-družinski regex (1:1 z parish-forensics.ts — brez 'Michael' lažnih!)
MILIC_RE = re.compile(
    r"MILIČ|MILEK|MIHELČ|MIHELIČ|MIHELIK|Mihelik|Milech|Milhoeluc|MILCH|Mihelk|Mihelt|Mihek|Milih|Mihelitsch|Mihelj|Mihelčič|Mihelovic|Milek\[|Mileh\[|Mek/Milek|Milek-variant|MILEK-grafija",
    re.IGNORECASE,
)
PRIEST_RE = re.compile(r"Weisel|Wenzel|Wessely", re.IGNORECASE)

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
BLOK_RE = re.compile(
    r'houseNo:\s*"([^"]*)",\s*bookSignature:\s*"([^"]*)",\s*year:\s*(\d+),\s*(?:scan:\s*\d+,\s*)?(?:page:\s*\d+,\s*)?whatSi:\s*"(.*?)",\s*whatEn:',
    re.S,
)
bloki = []
for m in BLOK_RE.finditer(src):
    house, sig, year, what = m.group(1), m.group(2), int(m.group(3)), m.group(4)
    bloki.append({"house": house, "sig": sig, "year": year, "what": what})

check("I1 korpus razčlenjen == 1978 blokov (križ z HOUSE_VITALS) — P244-živo!",
      len(bloki) == 1978, f"razčlenjenih={len(bloki)}")
po_knjigi = {k: sum(1 for b in bloki if b["sig"] == k) for k in ("04104", "04105", "04106", "04894", "04455")}
check("I1b bloki-po-knjigah == {04104:288, 04105:502, 04106:433, 04894:520, 04455:235} (P244-živo!)",
      po_knjigi == {"04104": 288, "04105": 502, "04106": 433, "04894": 520, "04455": 235},
      ",".join(f"{k}:{v}" for k, v in po_knjigi.items()))

milic_po_knjigi = {k: sum(1 for b in bloki if b["sig"] == k and MILIC_RE.search(b["what"])) for k in po_knjigi}
milic_skupaj = sum(milic_po_knjigi.values())
check("I2 MILIČ↔MILEK-križ == [53,78,20,36,51] · skupaj 238 (Python-križ == TS-modul!)",
      milic_po_knjigi == {"04104": 53, "04105": 78, "04106": 20, "04894": 36, "04455": 51} and milic_skupaj == 238,
      ",".join(f"{k}:{v}" for k, v in milic_po_knjigi.items()) + f" · skupaj={milic_skupaj}")

po_letih = {y: sum(1 for b in bloki if b["sig"] == "04104" and b["year"] == y and MILIC_RE.search(b["what"]))
            for y in range(1871, 1886)}
pričakovano = {1871: 5, 1872: 3, 1873: 3, 1874: 7, 1875: 3, 1876: 3, 1877: 5, 1878: 1, 1879: 7,
               1880: 6, 1881: 2, 1882: 2, 1883: 3, 1884: 3, 1885: 0}
check("I3 MILIČ-po-letih-04104 == 1871:[5,3,3,7,3,3,5,1,7,6,2,2,3,3] · 1885 = 0 (iskreno!)",
      po_letih == pričakovano, ",".join(f"{y}:{po_letih[y]}" for y in sorted(po_letih)))

h65 = [b for b in bloki if b["house"] == "65"]
h65_druzina = [b for b in h65 if MILIC_RE.search(b["what"])]
mathias = [b for b in h65 if re.search(r"Mathias|Matija|Matihe", b["what"], re.I)]
leta_mathias = sorted(b["year"] for b in mathias)
check("I4a h65 == {total:42, family:36, others:6}", len(h65) == 42 and len(h65_druzina) == 36,
      f"total={len(h65)} family={len(h65_druzina)} others={len(h65)-len(h65_druzina)}")
check("I4b Mathias/Matija-h65-veriga == 22 blokov · span 1871–1914 (43 let!)",
      len(mathias) == 22 and leta_mathias[0] == 1871 and leta_mathias[-1] == 1914,
      f"n={len(mathias)} span={leta_mathias[0]}–{leta_mathias[-1]}")

h69 = [b for b in bloki if b["house"] == "69"]
h69_knjige = {k: sum(1 for b in h69 if b["sig"] == k) for k in ("04104", "04105", "04106", "04894", "04455")}
h69_milek = [b for b in h69 if MILIC_RE.search(b["what"])]
check("I5 h69 == 25 blokov (4+8+6+5+2!) · Milek@h69-presek == 1 (botra-Katarina-1898)",
      len(h69) == 25 and h69_knjige == {"04104": 4, "04105": 8, "04106": 6, "04894": 5, "04455": 2}
      and len(h69_milek) == 1,
      ",".join(f"{k}:{v}" for k, v in h69_knjige.items()) + f" · milek={len(h69_milek)}")

duhovniki = {k: sum(1 for b in bloki if b["sig"] == k and PRIEST_RE.search(b["what"])) for k in po_knjigi}
check("I6 duhovniški-križ == {04104:3, ostale:0} (X-open pošteno ostaja!)",
      duhovniki == {"04104": 3, "04105": 0, "04106": 0, "04894": 0, "04455": 0},
      ",".join(f"{k}:{v}" for k, v in duhovniki.items()))

mod = open(f"{ROOT}/src/data/atlas/parish-forensics.ts", encoding="utf-8").read()
check("I7 modul parish-forensics.ts (regex + izpeljanke + 3 sodbe + VODENICA)",
      "MILIC_FAMILY_RE" in mod and "MILIC_FAMILY_TOTAL" in mod and "MATHIAS_H65_TOTAL" in mod
      and "H65_STATS" in mod and "H69_ERAS" in mod and "PRIEST_CROSS" in mod
      and "FORENSIC_VERDICTS" in mod and "vodeniška hiša" in mod
      and mod.count("id: \"") >= 6)

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
check("I8 qa-p237 (živi preverja 238/53-78-20-36-51/22/42-36-6/25/3-0-0-0-0!)",
      "qa-p237-parish-forensics" in qa and "MILIC_FAMILY_TOTAL !== 238" in qa
      and '"53,78,20,36,51"' in qa and "MATHIAS_H65_TOTAL !== 22" in qa
      and "H69_TOTAL !== 25" in qa and "FORENZIKA-NITI-POTRJENA" in qa)

ui = open(f"{ROOT}/src/components/museum/museum-atlas.tsx", encoding="utf-8").read()
check("I9 UI-ParishForensics (komponenta + uvoz + render v ParishTab)",
      "function ParishForensics" in ui and "from \"@/data/atlas/parish-forensics\"" in ui
      and "<ParishForensics />" in ui and "MILIC_PER_BOOK" in ui and "H69_ERAS" in ui
      and "FORENSIC_VERDICTS" in ui and "PRIEST_CROSS" in ui)

wl = open(f"{ROOT}/worklog.md", encoding="utf-8").read()
check("I9b worklog P237 vnos (FORENZIKA-NITI)", "## P237" in wl and "FORENZIKA" in wl.upper())

live = "--live" in sys.argv
if live or "--check" not in sys.argv:
    try:
        req = urllib.request.Request("https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04105/",
                                     headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            check("I10 LIVE matricula-04105 HTTP 200 (križ-knjiga!)", r.status == 200, f"status={r.status}")
    except Exception as e:
        check("I10 LIVE matricula-04105", False, str(e)[:80])

print(f"\n{'VSI PASS' if ok else 'NEUSPEH!'} ({sum(1 for _, c, _ in results if c)}/{len(results)})")
sys.exit(0 if ok else 1)
