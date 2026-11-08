#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P207 — verifikator MRLIŠKE PREDZGODOVINE 04106, leto 1870 (predzgodovina-15/29)."""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'\{\s*houseNo:\s*"(\d+)",\s*bookSignature:\s*"04106",\s*year:\s*1870,', src)
check("I1 bloki 04106/1870 == 12", len(bloki) == 12, f"najdeno {len(bloki)}")
check("I2 hiše-1870 (file-order)", bloki == ["4", "1", "22", "48", "40", "52", "68", "28", "20", "32", "51", "46"], ",".join(bloki))
skupaj = src.count('bookSignature: "04106"')
check("I3 vitals-1889 + 04106==433", "HOUSE_VITALS.length !== 1889" not in src and skupaj == 433, f"04106={skupaj}")

d = json.load(open(f"{ROOT}/research/issue17/parish-death-1870-04106.json", encoding="utf-8"))
grib = [e for e in d["entries"] if "gribl" in str(e.get("vas", "")).lower()]
an = json.dumps(d["anomalije"], ensure_ascii=False)
check("I4 dokaz (70/12-griblje/anomalije + meja-s80-valovita + 70-vrstic)",
      len(d["entries"]) == 70 and len(grib) == 12
      and "s80" in d["okvir"]["meja_1869_70"] and "valovita" in d["okvir"]["meja_1869_70"].lower()
      and "s86" in d["okvir"]["meja_1870_71"] and "vsota" in d["okvir"]["meja_1870_71"].lower()
      and "vsota" in an and d["statistika"]["vpisov_1870"] == 70,
      f"entries={len(d['entries'])} griblje={len(grib)} anomalije={len(d['anomalije'])}")

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 1889")
check("I5 qa-p207 + števec-1484", "qa-p207-parish-death-1870-04106" in qa and st >= 100, f"1870-številcev={st}")

i0 = src.find("P207: mrliška PREDZGODOVINA 04106, leto 1870")
seg = src[i0:] if i0 >= 0 else ""
check("I6a 73-VPIISOV-ŠTEVJE-IZ-VRSTIC-8.×", "73 vpisov" in seg and "ŠTEVJE-IZ-VRSTIC-8.×" in seg)
check("I6b LUK-18 + DUP-19", "LUK-18" in seg and "DUP-19" in seg)
check("I6c h1-GOSPODAR (z28-Jessernigg!)", "h11-NIT-5.-LETO" in seg)
check("I7a MEJA-s86 ('Jänner'-glava + restart + vsota!)", "MEJA-1869/70-s80→s81" in seg)
check("I7b MEJA-1870/71-s86-tail (P206-soglasje!)", "MEJA-1870/71-s86" in seg)
check("I7c ord-stolpci-s83-s84 (25,26,27–30!)", "ord-stolpec-cele-s88" in seg or "19,19,20" in seg)
check("I8a ime-DUELI-×3 (z39-z60-z63!)", "ime-DUEL-z17" in seg or "Grüblner" in seg)
check("I8b POŽEK-h28-NIT-2.-LETO-z51", "Ablasser" in seg)
check("I8c MRTVOROJEN-z42-Knavs-h52", "KROP-POPOLNO-SOGLASJE" in seg and "5¾" in seg)
check("I8d 12-hiš-vsi-različni", "12 hiš" in seg)
check("I9 qa-p206 (207. kontrola!)", "qa-p206" in qa and "206. kontrola" in qa)
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
