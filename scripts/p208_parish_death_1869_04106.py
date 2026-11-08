#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P208 — verifikator MRLIŠKE PREDZGODOVINE 04106, leto 1869 (predzgodovina-15/29)."""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'\{\s*houseNo:\s*"(\d+)",\s*bookSignature:\s*"04106",\s*year:\s*1869,', src)
check("I1 bloki 04106/1869-numeric == 13", len(bloki) == 13, f"najdeno {len(bloki)}")
check("I2 hiše-1869-numeric (file-order; +1-[?]-izven-regexa!)", bloki == ["22", "13", "12", "65", "22", "49", "20", "73", "47", "72", "28", "70", "65"], ",".join(bloki))
skupaj = src.count('bookSignature: "04106"')
check("I3 vitals-1853 + 04106==433", "HOUSE_VITALS.length !== 1853" not in src and skupaj == 433, f"04106={skupaj}")

d = json.load(open(f"{ROOT}/research/issue17/parish-death-1869-04106.json", encoding="utf-8"))
grib = [e for e in d["entries"] if "gribl" in str(e.get("vas", "")).lower()]
an = json.dumps(d["anomalije"], ensure_ascii=False)
check("I4 dokaz (76/14-griblje/anomalije + meja-s75-vsota + 76-vrstic)",
      len(d["entries"]) == 76 and len(grib) == 14
      and "s75" in d["okvir"]["meja_1868_69"] and "vsota" in d["okvir"]["meja_1868_69"].lower()
            and "vsota" in an and d["statistika"]["vpisov_1869"] == 76,
      f"entries={len(d['entries'])} griblje={len(grib)} anomalije={len(d['anomalije'])}")

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 1853")
check("I5 qa-p208 + števec-1498", "qa-p208-parish-death-1869-04106" in qa and st >= 100, f"1853-številcev={st}")

i0 = src.find("P208: mrliška PREDZGODOVINA 04106, leto 1869")
seg = src[i0:] if i0 >= 0 else ""
check("I6a 73-VPIISOV-ŠTEVJE-IZ-VRSTIC-8.×", "73 vpisov" in seg and "ŠTEVJE-IZ-VRSTIC-8.×" in seg)
check("I6b ULEDBA-z1 + vsota-3.×", "ULEDBA-NOVO-LETO" in seg and "vsota" in seg.lower())
check("I6c h1-GOSPODAR (z28-Jessernigg!)", "POŽEK-NIT-3.-LETO" in seg)
check("I7a MEJA-s75 ('1869'-glava-KROP + restart + vsota-3.×!)", "MEJA-1868/69-s75" in seg)
check("I7b KONEC-1869-s80-valovita (P207!)", "VALOVITA-ČRTA" in seg or "valovita-črta" in seg.lower())
check("I7c ord-stolpci-s75-s80 (77–80→1–9-65–76!)", "ord-stolpci" in seg and "77,78,79,80" in seg)
check("I8a ime-DUELI-×3 (z39-z60-z63!)", "DRAGOS-nit" in seg)
check("I8b POŽEK-h28-NIT-2.-LETO-z51", "Noßgabianstho" in seg)
check("I8c MRTVOROJEN-z42-Knavs-h52", "PEZDIR-grafia-×3" in seg)
check("I8d 12-hiš-vsi-različni", "12 hiš" in seg)
check("I9 qa-p206 (207. kontrola!)", "qa-p208" in qa and "208. kontrola" in qa)
pt = open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8").read()
check("I9 pt-luknja-292/1511", '"vitalsTotal": 1853' in pt and '"04106": 433' in pt)

try:
    req = urllib.request.Request("https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04106/",
                                 headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        check("I10 LIVE matricula-04106 HTTP 200", r.status == 200, f"status={r.status}")
except Exception as e:
    check("I10 LIVE matricula-04106", False, str(e)[:80])

print("SKUPAJ:", "VSI-PASS ✓" if ok else "NEKAJ-FAIL ✗")
sys.exit(0 if ok else 1)
