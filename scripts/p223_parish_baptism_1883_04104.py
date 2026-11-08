#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P223 — verifikator KRSTNE PREDZGODOVINE 04104, leto 1883 = 3/15 (I1–I10 + --live)."""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "04104",\s*year: 1883,', src)
check("I1 bloki 04104/1883-numeric == 19", len(bloki) == 19, f"najdeno {len(bloki)}")
pri = ["28", "20", "7", "39", "8", "35", "25", "17", "[?]", "19", "24", "90", "1", "56", "37", "25", "11", "63", "29"]
check("I2 hiše-1883 (file-order, h25-×2! + 2-×-[?]-DUELI!)", bloki == pri, ",".join(bloki[:8]) + "…")
skupaj = src.count('bookSignature: "04104"')
check("I3 vitals-1853 + 04104==201", "HOUSE_VITALS.length !== 1853" not in src and skupaj == 201, f"04104={skupaj}")

d = json.load(open(f"{ROOT}/research/issue17/parish-baptism-1883-04104.json", encoding="utf-8"))
grib = [e for e in d["entries"] if "gribl" in str(e.get("vas", "")).lower() and "grem" not in str(e.get("vas", "")).lower()]
an = json.dumps(d["anomalije"], ensure_ascii=False)
check("I4 dokaz (19-griblje + MEJA-s161 + 99-DISTINCT + pag-dvojni-seriji + z99-IZLOČEN)",
      len(grib) == 19
      and "s161 (62.-POTRDITEV" in json.dumps(d["okvir"], ensure_ascii=False)
      and "dvojni-foliacijski-seriji" in an
      and "z99-tail-izlocen" in an
      and d["frame"]["rowsTotal"] == 99 and d["stats"]["vpisov_distinct"] == 99
      and "sken−5" in d["okvir"]["pag"],
      f"entries={len(d['entries'])} griblje={len(grib)} anomalije={len(d['anomalije'])}")
check("I4b novosti (mesec-carry-over + marz-korekcija + hisni-dueli + pripisi-mmk + mreze)",
      "mesec-carry-over-vzorec" in an and "marz-label-misread-korekcija" in an
      and "hisni-dueli-reseni" in an and "pripisi-kriz-mmk-1883" in an and "mreze-1883" in an)

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 1853")
check("I5 qa-p223 + števec-1853", "qa-p223-parish-baptism-1883-04104" in qa and st >= 135, f"1853-številcev={st}")

i0 = src.find("P223: krstna PREDZGODOVINA 04104, leto 1883")
seg = src[i0:] if i0 >= 0 else ""
check("I6a 99-DISTINCT + MEJA-s161-62.-POTRDITEV", "99-vpisov-DISTINCT" in seg and "vrstna-aritmetika 6+9+8+8+9+9+9+8+8+8+8+8+1 = 99" in seg and "62.-POTRDITEV-invariante" in seg)
check("I6b MESEC-CARRY-OVER-VZOREC + MÄRZ-LABEL-MISREAD-KOREKCIJA", "MESEC-CARRY-OVER-VZOREC" in seg and "MÄRZ-LABEL-MISREAD-KOREKCIJA" in seg and "April-sandwich" in seg)
check("I6c DVOJNI-FOLIACIJSKI-SERIJI + P222-'s173=186'-KOREKCIJA", "DVOJNI-FOLIACIJSKI-SERIJI" in seg and "sken−5" in seg and "sken+13" in seg and "s173=186'-KOREKCIJA" in seg)
check("I7a 19-GRIBLJE / 18-hiš (h25-×2!)", "19-GRIBLJE / 18-hiš (h25-×2" in seg)
check("I7b z99-TAIL-IZLOČEN + hišni-DUELI-REŠENI-×5", "z99-TAIL-IZLOČEN" in seg and "Obrijuh" in seg and "hišni-DUELI-REŠENI-×5" in seg)
check("I7c POZNEJŠI-PRIPISI-MMK-ERA-×8 (1962 + 1940 + 1957 + 1985 + 1910!)", "umrla-18.12.1962" in seg and "umrla-6.1.1940-90-let" in seg and "umrla-1957" in seg and "Mrt.-10.7.1985" in seg and "Cop.-1910" in seg)
check("I8a mreže-1883 (PEZDIRC-grafija-×6 + BRODARIČ-×4 + DRAGOŠ-×2 + SIMEC-×3!)", "PEZDIRC-grafija-×6" in seg and "BRODARIČ-×4" in seg and "DRAGOŠ-×2" in seg and "SIMEC-×3" in seg and "KRIŽAN-×2" in seg)
check("I8b DVOJČKI-GRIBLJE-h68-ZWILLINGE-P224-LEAD", "ZWILLINGE" in seg and "P224-LEAD" in seg)
check("I9a qa-p223 (223. kontrola!)", "qa-p223" in qa and "223. kontrola" in qa)
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
