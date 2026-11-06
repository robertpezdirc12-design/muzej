#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P206 — verifikator MRLIŠKE PREDZGODOVINE 04106, leto 1871 (predzgodovina-15/29)."""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'\{\s*houseNo:\s*"(\d+)",\s*bookSignature:\s*"04106",\s*year:\s*1871,', src)
check("I1 bloki 04106/1871 == 11", len(bloki) == 11, f"najdeno {len(bloki)}")
check("I2 hiše-1871 (file-order)", bloki == ["11", "29", "38", "13", "33", "66", "72", "28", "65", "2", "8"], ",".join(bloki))
skupaj = src.count('bookSignature: "04106"')
check("I3 vitals-1652 + 04106==433", "HOUSE_VITALS.length !== 1652" not in src and skupaj == 433, f"04106={skupaj}")

d = json.load(open(f"{ROOT}/research/issue17/parish-death-1871-04106.json", encoding="utf-8"))
grib = [e for e in d["entries"] if "gribl" in str(e.get("vas", "")).lower()]
an = json.dumps(d["anomalije"], ensure_ascii=False)
check("I4 dokaz (73/11-griblje/anomalije + meja-s86-'vsota' + 73-vrstic)",
      len(d["entries"]) == 73 and len(grib) == 11
      and "s86" in d["okvir"]["meja_1870_71"] and "vsota" in d["okvir"]["meja_1870_71"].lower()
      and "vsota" in an and d["statistika"]["vpisov_1871"] == 73,
      f"entries={len(d['entries'])} griblje={len(grib)} anomalije={len(d['anomalije'])}")

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 1652")
check("I5 qa-p206 + števec-1472", "qa-p206-parish-death-1871-04106" in qa and st >= 100, f"1652-številcev={st}")

i0 = src.find("P206: mrliška PREDZGODOVINA 04106, leto 1871")
seg = src[i0:] if i0 >= 0 else ""
check("I6a 73-VPIISOV-ŠTEVJE-IZ-VRSTIC-8.×", "73 vpisov" in seg and "ŠTEVJE-IZ-VRSTIC-8.×" in seg)
check("I6b LUK-18 + DUP-19", "LUK-18" in seg and "DUP-19" in seg)
check("I6c h11-NIT-5.-LETO (z5-Plut!)", "h11-NIT-5.-LETO" in seg)
check("I7a MEJA-s86 ('Jänner'-glava + restart + vsota!)", "MEJA-1870/71-s86" in seg)
check("I7b MEJA-1871/72-s92 (December-KROP!)", "MEJA-1871/72-s92" in seg)
check("I7c ord-stolpec-cele-s88 (19,19,20–30!)", "ord-stolpec-cele-s88" in seg or "19,19,20" in seg)
check("I8a ime-DUEL-z17 (Jančarič-vs-Grüblner!)", "ime-DUEL-z17" in seg or "Grüblner" in seg)
check("I8b stan-'Ablasser'-z29 (1.×!)", "Ablasser" in seg)
check("I8c KROP-POPOLNO-SOGLASJE-z50 (5¾-J!)", "KROP-POPOLNO-SOGLASJE" in seg and "5¾" in seg)
check("I8d 11-hiš-vsi-različni", "11 hiš" in seg)
check("I9 qa-p206 (206. kontrola!)", "qa-p206" in qa and "206. kontrola" in qa)
pt = open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8").read()
check("I9 pt-luknja-292/1511", '"vitalsTotal": 1652' in pt and '"04106": 433' in pt)

try:
    req = urllib.request.Request("https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04106/",
                                 headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        check("I10 LIVE matricula-04106 HTTP 200", r.status == 200, f"status={r.status}")
except Exception as e:
    check("I10 LIVE matricula-04106", False, str(e)[:80])

print("SKUPAJ:", "VSI-PASS ✓" if ok else "NEKAJ-FAIL ✗")
sys.exit(0 if ok else 1)
