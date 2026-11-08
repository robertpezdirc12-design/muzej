#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P220 — verifikator MRLIŠKE PREDZGODOVINE 04106, leto 1857 = 29/29 — ZADNJE leto knjige (I1–I10 + --live)."""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'\{\s*houseNo: "([^"]+)",\s*bookSignature: "04106",\s*year: 1857,', src)
check("I1 bloki 04106/1857-numeric == 10", len(bloki) == 10, f"najdeno {len(bloki)}")
pri = ["60", "64", "52", "13", "36", "31", "48", "65", "[?]", "36"]
check("I2 hiše-1857 (file-order, vključno-[?])", bloki == pri, ",".join(bloki))
skupaj = src.count('bookSignature: "04106"')
check("I3 vitals-1906 + 04106==433", "HOUSE_VITALS.length !== 1906" not in src and skupaj == 433, f"04106={skupaj}")

d = json.load(open(f"{ROOT}/research/issue17/parish-death-1857-04106.json", encoding="utf-8"))
grib = [e for e in d["entries"] if "gribl" in str(e.get("vas", "")).lower() and "grem" not in str(e.get("vas", "")).lower()]
an = json.dumps(d["anomalije"], ensure_ascii=False)
check("I4 dokaz (73/10-griblje + knjiga-start-'18 57' + LUKNJA-32 + 73-written + OKTOBER-×0)",
      len(d["entries"]) == 73 and len(grib) == 10
      and "18 57" in d["okvir"]["knjiga_start"] and "LUKNJA-32" in d["okvir"]["luknja_32"]
      and d["statistika"]["vpisov_1857_kronolosko"] == 73 and d["statistika"]["vpisov_written"] == 73
      and "OKTOBER-1857-×0" in d["okvir"]["oktober_luknja"],
      f"entries={len(d['entries'])} griblje={len(grib)} anomalije={len(d['anomalije'])}")
check("I4b luknja-32 + scarlatina-klaster + h36-krizan-×2 + z71-neberljiva",
      "luknja-32" in an and "scarlatina-klaster" in an and "h36-krizan-×2" in an and "z71-hisa-neberljiva-starost-duel" in an)
check("I4c knjiga-start-1857 + oktober-luknja + z58-honesty-max + popravki-pisarja",
      "knjiga-start-1857" in an and "oktober-luknja" in an and "z58-honesty-max" in an and "popravki-pisarja-×2" in an)

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 1906")
check("I5 qa-p220 + števec-1870", "qa-p220-parish-death-1857-04106" in qa and st >= 132, f"1870-številcev={st}")

i0 = src.find("P220: mrliška PREDZGODOVINA 04106, leto 1857")
seg = src[i0:] if i0 >= 0 else ""
check("I6a 73-VPIISOV-ŠTEVJE-IZ-VRSTIC-22.× + LUKNJA-32", "73 vpisov" in seg and "ŠTEVJE-IZ-VRSTIC-22.×" in seg and "LUKNJA-32" in seg)
check("I6b KNJIGA-START-'18 57'-RAZPETA + MEJA-1856/57-NE-OBSTAJA", "KNJIGA-04106-SE-ZAČNE-1857" in seg and "18 57" in seg and "MEJA-1856/57-NE-OBSTAJA" in seg)
check("I6c OKTOBER-×0 + SCARLATINA?-klaster", "OKTOBER-×0" in seg and "SCARLATINA?-klaster" in seg)
check("I7a h36-KRIŽAN-×2 (z50 + z74-TAIL)", "h36-×2-KRIŽAN" in seg and "z50-otrok-4J" in seg and "z74-Marijan-73J-TAIL" in seg)
check("I7b 8-od-10-hiš-PRVI-vpis-v-korpusu", "8-od-10-hiš-dobi-PRVI-vpis-v-korpusu" in seg)
check("I7c z74-MOŽEN-ZGODNJI-Knavs-podpis (KOREKCIJA-P219-lead!)", "MOŽEN-ZGODNJI-Knavs-podpis" in seg and "KOREKCIJA-P219-lead" in seg)
check("I8a MEJA-1857/58-s7-re-križ-59.-POTRDITEV + VSOTNA-'1 8 5 [8]'", "MEJA-1857/58-s7" in seg and "59.-POTRDITEV" in seg and "1 8 5 [8]" in seg)
check("I8b pag-sken−1-SVINČNIK-FOLIACIJA (konvencijski-prehod!)", "sken−1-SVINČNIK-FOLIACIJA-ARHIVARJA" in seg and "sken−5-NEMOŽEN-za-s1–s5" in seg)
check("I8c otroška-umrljivost-30%-3/10 + ekstremi-3-tedne-→-73-J", "umrljivost-30%-3/10" in seg and "3-tedne-→-73-J" in seg)
check("I9a qa-p220 (220. kontrola!)", "qa-p220" in qa and "220. kontrola" in qa)
pt = open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8").read()
check("I9b pt-luknja-433/1870", '"vitalsTotal": 1906' in pt and '"04106": 433' in pt)

live = "--live" in sys.argv
if live or "--check" not in sys.argv:
    try:
        req = urllib.request.Request("https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04106/",
                                     headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            check("I10 LIVE matricula-04106 HTTP 200", r.status == 200, f"status={r.status}")
    except Exception as e:
        check("I10 LIVE matricula-04106", False, str(e)[:80])

print(f"\n{'VSI PASS' if ok else 'NEUSPEH!'} ({sum(1 for _, c, _ in results if c)}/{len(results)})")
sys.exit(0 if ok else 1)
