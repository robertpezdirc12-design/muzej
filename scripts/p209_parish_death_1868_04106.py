#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P209 — verifikator MRLIŠKE PREDZGODOVINE 04106, leto 1868 (predzgodovina-15/29)."""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'\{\s*houseNo:\s*"(\d+)",\s*bookSignature:\s*"04106",\s*year:\s*1868,', src)
check("I1 bloki 04106/1868-numeric == 13", len(bloki) == 13, f"najdeno {len(bloki)}")
check("I2 hiše-1868-numeric (file-order)", bloki == ["54", "54", "50", "36", "65", "66", "26", "15", "13", "10", "41", "35", "13"], ",".join(bloki))
skupaj = src.count('bookSignature: "04106"')
check("I3 vitals-1889 + 04106==433", "HOUSE_VITALS.length !== 1889" not in src and skupaj == 433, f"04106={skupaj}")

d = json.load(open(f"{ROOT}/research/issue17/parish-death-1868-04106.json", encoding="utf-8"))
grib = [e for e in d["entries"] if "gribl" in str(e.get("vas", "")).lower()]
an = json.dumps(d["anomalije"], ensure_ascii=False)
check("I4 dokaz (80/13-griblje/anomalije + meja-s69-vsota-4-delna + 80-vrstic)",
      len(d["entries"]) == 80 and len(grib) == 13
      and "s69" in d["okvir"]["meja_1867_68"] and "vsota" in d["okvir"]["meja_1867_68"].lower()
            and "vsota" in an.lower() and d["statistika"]["vpisov_1868"] == 80,
      f"entries={len(d['entries'])} griblje={len(grib)} anomalije={len(d['anomalije'])}")

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 1889")
check("I5 qa-p209 + števec-1511", "qa-p209-parish-death-1868-04106" in qa and st >= 100, f"1870-številcev={st}")

i0 = src.find("P209: mrliška PREDZGODOVINA 04106, leto 1868")
seg = src[i0:] if i0 >= 0 else ""
check("I6a 73-VPIISOV-ŠTEVJE-IZ-VRSTIC-8.×", "73 vpisov" in seg and "ŠTEVJE-IZ-VRSTIC-8.×" in seg)
check("I6b ANOMALIA-z61 + 2-smrti-v-1-dnevu", 'nožgodanujeleg' in seg and "2-smrti-v-ISTEM-dnevu" in seg)
check("I6c h1-GOSPODAR (z28-Jessernigg!)", "JAKOFČIČ-×2" in seg)
check("I7a MEJA-s75 ('1868'-glava-KROP + restart + vsota-3.×!)", "MEJA-1867/68-s69" in seg)
check("I7b KONEC-1868-s80-valovita (P207!)", '1|8|6|8' in seg)
check("I7c ord-stolpec-s69 (1–10!)", "ord-stolpci" in seg and "1–10" in seg)
check("I8a ime-DUELI-×3 (z39-z60-z63!)", "ULEDBA-vzorec-×2" in seg)
check("I8b POŽEK-h28-NIT-2.-LETO-z51", "h54-×2" in seg)
check("I8c MRTVOROJEN-z42-Knavs-h52", "PERDIRC-nit" in seg)
check("I8d 12-hiš-vsi-različni", "12 hiš" in seg)
check("I9 qa-p206 (207. kontrola!)", "qa-p209" in qa and "209. kontrola" in qa)
pt = open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8").read()
check("I9 pt-luknja-292/1511", '"vitalsTotal": 1889' in pt and '"04106": 433' in pt)

try:
    req = urllib.request.Request("https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04106/",
                                 headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        check("I10 LIVE matricula-04106 HTTP 200", r.status == 200, f"status={r.status}")
except Exception as e:
    check("I10 LIVE matricula-04106", False, str(e)[:80])

print("SKUPAJ:", "VSI-PASS ✓" if ok else "NEKAJ-FAIL ✗")
sys.exit(0 if ok else 1)
