#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P224 — verifikator KRSTNE PREDZGODOVINE 04104, leto 1882 = 4/15 (I1–I10 + --live)."""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "04104",\s*year: 1882,', src)
check("I1 bloki 04104/1882-numeric == 25", len(bloki) == 25, f"najdeno {len(bloki)}")
pri = ["45", "15", "27", "14", "73", "1", "28", "46", "21", "65", "41", "5", "40", "62", "58", "16", "13", "74", "44", "43", "35", "47", "13", "68", "68"]
check("I2 hiše-1882 (file-order, h13-×2! + h68-×2-DVOJČKI!)", bloki == pri, ",".join(bloki[:8]) + "…")
skupaj = src.count('bookSignature: "04104"')
check("I3 vitals-1781 + 04104==129", "HOUSE_VITALS.length !== 1781" not in src and skupaj == 129, f"04104={skupaj}")

d = json.load(open(f"{ROOT}/research/issue17/parish-baptism-1882-04104.json", encoding="utf-8"))
grib = [e for e in d["entries"] if "gribl" in str(e.get("vas", "")).lower() and "grem" not in str(e.get("vas", "")).lower()]
an = json.dumps(d["anomalije"], ensure_ascii=False)
check("I4 dokaz (25-griblje + MEJA-s147/s148-63.-POTRDITEV + 106-DISTINCT + pag-sken−6 + LUKNJA-158)",
      len(grib) == 25
      and "s147/s148 (63.-POTRDITEV" in json.dumps(d["okvir"], ensure_ascii=False)
      and "s160-dezember-korekcija" in an
      and "s149-z16-duplikat" in an
      and d["frame"]["rowsTotal"] == 106 and d["stats"]["vpisov_distinct"] == 106
      and "sken−6" in d["okvir"]["pag"] and "LUKNJA-'158'" in d["okvir"]["pag"],
      f"entries={len(d['entries'])} griblje={len(grib)} anomalije={len(d['anomalije'])}")
check("I4b novosti (dezember-korekcija + z71-okt + z55-zap + hisne-vizualne + pripisi-mmk + mreze)",
      "z71-mesec-korekcija" in an and "z55-zap-korekcija" in an
      and "hisne-vizualne-resitve" in an and "pripisi-kriz-mmk-1882" in an and "mreze-1882" in an)

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 1781")
check("I5 qa-p224 + števec-1781", "qa-p224-parish-baptism-1882-04104" in qa and st >= 136, f"1781-številcev={st}")

i0 = src.find("P224: krstna PREDZGODOVINA 04104, leto 1882")
seg = src[i0:] if i0 >= 0 else ""
check("I6a 106-DISTINCT + MEJA-s147/s148-63.-POTRDITEV", "106-vpisov-DISTINCT" in seg and "vrstna-aritmetika" in seg and "8+9+8+8+7+9+8+7+7+8+8+8+8+3 = 106" in seg and "63.-POTRDITEV-invariante" in seg)
check("I6b S160-DEZEMBER-KOREKCIJA + Z71-OKT-KOREKCIJA", "S160-'NOVEMBER'-MISREAD-KOREKCIJA" in seg and "DEZEMBER-BLOK-z92–z106" in seg and "OKTOBER-11/12" in seg and "…ember" in seg)
check("I6c FOLIACIJA-TRI-SERIJE + LUKNJA-'158'", "sken−6" in seg and "LUKNJA-'158'" in seg and "skok-s163→s164" in seg and "sken−5" in seg and "sken+13" in seg)
check("I7a 25-GRIBLJE / 23-hiš (TIE-REKORD-P221!)", "25-GRIBLJE / 23-hiš" in seg and "TIE-REKORD-P221" in seg)
check("I7b S149-Z16-DUPLIKAT + Z55-ZAP-KOREKCIJA + HIŠNE-VIZUALNE-×6", "S149-Z16-DUPLIKAT" in seg and "16-×2→17" in seg and "Z55-ZAP-KOREKCIJA" in seg and "HIŠNE-VIZUALNE-REŠITVE-×6" in seg)
check("I7c POZNEJŠI-PRIPISI-MMK-ERA-×6 (1955 + 1960 + 1919 + 1937 + 1966 + 1971!)", "umrla-7.[~4!].8.1955" in seg and "umrla-29.11.1960" in seg and "1919" in seg and "1937" in seg and "umrl-27.3.1966" in seg and "6.1971" in seg)
check("I8a mreže-1882 (PEZDIRC-×4 + KLOBUČAR-×3 + DRAGOŠ-×2 + KRIŽAN-×2!)", "PEZDIRC-×4" in seg and "KLOBUČAR-×3" in seg and "DRAGOŠ-×2" in seg and "KRIŽAN-×2" in seg and "ŽELJKO-×3" in seg)
check("I8b DVOJČKI-GRIBLJE-h68-ZWILLINGE + 'Anni-1-8-8-1.'", "ZWILLINGE" in seg and "1 8 8 1" in seg and "P214-TIP-4.-instance" in seg)
check("I9a qa-p224 (224. kontrola!)", "qa-p224" in qa and "224. kontrola" in qa)
pt = open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8").read()
check("I9b pt-luknja-129/1781 + byBook-04104", '"vitalsTotal": 1781' in pt and '"04104": 129' in pt)

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
