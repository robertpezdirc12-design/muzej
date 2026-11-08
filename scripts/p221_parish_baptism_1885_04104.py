#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P221 — verifikator KRSTNE PREDZGODOVINE 04104, leto 1885 = 1/15 — NOVA LINIJA (I1–I10 + --live)."""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "04104",\s*year: 1885,', src)
check("I1 bloki 04104/1885-numeric == 25", len(bloki) == 25, f"najdeno {len(bloki)}")
pri = ["21", "[?]", "31", "61", "11", "63", "49", "28", "42", "1", "55", "53", "35", "16", "24", "[?]", "17", "58", "9", "55", "[?]", "2", "23", "1", "8"]
check("I2 hiše-1885 (file-order, 3×-[?])", bloki == pri, ",".join(bloki[:8]) + "…")
skupaj = src.count('bookSignature: "04104"')
check("I3 vitals-1853 + 04104==201", "HOUSE_VITALS.length !== 1853" not in src and skupaj == 201, f"04104={skupaj}")

d = json.load(open(f"{ROOT}/research/issue17/parish-baptism-1885-04104.json", encoding="utf-8"))
grib = [e for e in d["entries"] if "gribl" in str(e.get("vas", "")).lower() and "grem" not in str(e.get("vas", "")).lower()]
an = json.dumps(d["anomalije"], ensure_ascii=False)
check("I4 dokaz (104/25-griblje + MEJA-s186 + DVOJČKI-2-vrstici + z101 + 104-written + pag-sken+13)",
      len(d["entries"]) == 104 and len(grib) == 25
      and "s186 (TAIL-1884" in d["okvir"]["meja_1884_85"]
      and "DVOJČKI-GRADAC-×2-2-VRSTICI" in d["okvir"]["dvojcki_gradac"]
      and "z101 = NEIDENTIFICIRANA-VRSTICA" in d["okvir"]["z101_neidentificirana"]
      and d["stats"]["vpisov_1885_kronolosko"] == 104 and d["stats"]["vpisov_written"] == 104
      and "sken + 13" in d["okvir"]["pag"],
      f"entries={len(d['entries'])} griblje={len(grib)} anomalije={len(d['anomalije'])}")
check("I4b dvojcki-gradac + z101-neidentificirana + z100-griblje-korekcija + popravek-pisarja",
      "dvojcki-gradac-2-vrstici" in an and "z101-neidentificirana-vrstica" in an
      and "z100-griblje-h1-misread-korekcija" in an and "popravek-pisarja-s199-×2" in an)
check("I4c naslovna-sredi-letnika + foliacija-pag-sken-plus-13 + hisa-dueli + krstni-pripisi",
      "naslovna-sredi-letnika-s190" in an and "foliacija-pag-sken-plus-13" in an
      and "hisa-dueli-tri-quad" in an and "krstni-pripisi-kriz-mrlisko" in an)

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 1853")
check("I5 qa-p221 + števec-1853", "qa-p221-parish-baptism-1885-04104" in qa and st >= 133, f"1853-številcev={st}")

i0 = src.find("P221: krstna PREDZGODOVINA 04104, leto 1885")
seg = src[i0:] if i0 >= 0 else ""
check("I6a 104-VPIISOV-ŠTEVJE-IZ-VRSTIC-1.× + MEJA-s186-60.-POTRDITEV", "104-vpisov-kronološko" in seg and "ŠTEVJE-IZ-VRSTIC-1.×" in seg and "60.-POTRDITEV-invariante" in seg)
check("I6b DVOJČKI-GRADAC-2-VRSTICI + PARALELA-P219", "DVOJČKI-GRADAC-×2-2-VRSTICI" in seg and "PARALELA-P219-DVOJČKI-SIMIC" in seg)
check("I6c z101-NEIDENTIFICIRANA + POPRAVEK-PISARJA-s199-DOKAZ", "z101-NEIDENTIFICIRANA-VRSTICA" in seg and "POPRAVEK-PISARJA-s199" in seg)
check("I7a 25-GRIBLJE-NOV-REKORD-KORPUSA (prej-23-P218!)", "NOV-REKORD-PREDZGODOVINE" in seg and "prej-23-P218-1859" in seg)
check("I7b h1-×2 + h55-×2 + z59-honesty-MAX-QUAD", "h1-×2" in seg and "h55-×2" in seg and "QUAD-DUEL-27/47/37/21" in seg)
check("I7c MISREAD-KOREKCIJE-×7 (h6→61 + h33-×2-MRTVA + Škrilje→GRIBLJE!)", "h6→61" in seg and "h33-×2-HIPOTEZA-MRTVA" in seg and "Škrilje" in seg)
check("I8a POZNEJŠI-PRIPISI-KRIŽ-04106 (NOVA-DIMENZIJA!)", "POZNEJŠI-PRIPISI-KRIŽ-Z-MRLIŠKO-04106" in seg.upper() or "POZNEJŠI-PRIPISI-KRIŽ-z-mrliško-04106" in seg)
check("I8b pag-sken+13-FOLIO-SVINČNIK + NASLOVNA-SREDI-LETNIKA-s190", "sken+13-FOLIO-SVINČNIK" in seg and "NASLOVNA-SREDI-LETNIKA-s190" in seg)
check("I9a qa-p221 (221. kontrola!)", "qa-p221" in qa and "221. kontrola" in qa)
pt = open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8").read()
check("I9b pt-luknja-201/1853 + byBook-04104", '"vitalsTotal": 1853' in pt and '"04104": 201' in pt)

live = "--live" in sys.argv
if live or "--check" not in sys.argv:
    try:
        req = urllib.request.Request("https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04104/",
                                     headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            check("I10 LIVE matricula-04104 HTTP 200", r.status == 200, f"status={r.status}")
    except Exception as e:
        check("I10 LIVE matricula-04104", False, str(e)[:80])

print(f"\n{'VSI PASS' if ok else 'NEUSPEH!'} ({sum(1 for _, c, _ in results if c)}/{len(results)})")
sys.exit(0 if ok else 1)
