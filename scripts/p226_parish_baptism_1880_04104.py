#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P226 — verifikator KRSTNE PREDZGODOVINE 04104, leto 1880 = 6/15 (I1–I10 + --live)."""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "04104",\s*year: 1880,', src)
check("I1 bloki 04104/1880-numeric == 22", len(bloki) == 22, f"najdeno {len(bloki)}")
pri = ["2", "9", "39", "13", "60", "53", "35", "27", "19", "27", "7", "21", "24", "42", "24", "10", "43", "18", "33", "29", "44", "5"]
check("I2 hiše-1880 (file-order, 22/20-DISTINCT — h27-×2 + h24-×2!)", bloki == pri and len(set(bloki)) == 20, ",".join(bloki[:8]) + "…")
skupaj = src.count('bookSignature: "04104"')
check("I3 vitals-1819 + 04104==151", "HOUSE_VITALS.length !== 1819" not in src and skupaj == 167, f"04104={skupaj}")

d = json.load(open(f"{ROOT}/research/issue17/parish-baptism-1880-04104.json", encoding="utf-8"))
grib = [e for e in d["entries"] if "grib" in str(e.get("vas", "")).lower()]
an = json.dumps(d["anomalije"], ensure_ascii=False)
check("I4 dokaz (22-griblje + MEJA-s119/s120-65.-POTRDITEV + 122-DISTINCT + pag-sken−6-17/17 + brez-luknje)",
      len(grib) == 22
      and "s119/s120 (65.-POTRDITEV" in json.dumps(d["okvir"], ensure_ascii=False)
      and "meja-1879-80-s119-s120" in an
      and "foliacija-sken-6-17-17" in an
      and d["frame"]["rowsTotal"] == 122 and d["stats"]["vpisov_distinct"] == 122
      and "17/17-SEKVENČNO" in d["frame"]["pagKonvencija"] and "113–129" in d["okvir"]["pag"],
      f"entries={len(d['entries'])} griblje={len(grib)} anomalije={len(d['anomalije'])}")
check("I4b novosti (dvojcki-borst + missgeburt + z110-krsten-prazen + nezakonski-×7 + modri-×9 + duhovniki)",
      "dvojcki-borst-h20" in an and "missgeburt-x2" in an and "z110-krsten-prazen" in an
      and "nezakonski-x7" in an and "modri-maticarski-pripisi-x9" in an and "duhovniska-menjava" in an)

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 1819")
check("I5 qa-p226 + števec-1819", "qa-p226-parish-baptism-1880-04104" in qa and st >= 138, f"1819-številcev={st}")

i0 = src.find("P226: krstna PREDZGODOVINA 04104, leto 1880")
seg = src[i0:] if i0 >= 0 else ""
check("I6a 122-DISTINCT + MEJA-s119/s120-65.-POTRDITEV", "122-vpisov-DISTINCT" in seg and "vrstna-aritmetika" in seg and "8+9+9+8+7+9+7+6+7+8+7+8+8+7+7+7 = 122" in seg and "65.-POTRDITEV-invariante" in seg)
check("I6b FOLIACIJA-sken−6-17/17-SEKVENČNO + misreada-REŠENA", "17/17-SEKVENČNO" in seg and "113–129" in seg and "9↔3" in seg and "4↔7" in seg and "s132='126'" in seg)
check("I6c RESTART-z1-Dobravce-h11 + velike-cifre-P214-TIP + Schnörkel-BREZ-VSOTNE", "RESTART-z1-NA-DAN-3.-1.-JÄNNER-Dobravce-h11" in seg and "P214-TIP" in seg and "Schnörkel" in seg and "BREZ-VSOTNE" in seg and "5.-restart-z1" in seg)
check("I7a 22-GRIBLJE / 20-hiš (h27-×2 + h24-×2-DUELI-REŠENI)", "22-GRIBLJE / 20-hiš" in seg and "h27-×2" in seg and "h24-×2" in seg)
check("I7b PEZDIRC-×14-REKORD + KRIŽAN-×9 + JAKOFČIČ-×10", "PEZDIRC-×14-NOV-REKORD-LINJE" in seg and "grafija-continuum-6-let" in seg and "KRIŽAN-×9" in seg and "JAKOFČIČ-×10" in seg)
check("I7c DVOJČKI-Boršt-h20 + Mißgeburt-×2 + z110-KRSTEN-PRAZEN", "DVOJČKI-Boršt-h20" in seg and "P223-GRIBLJE-h68-PARALELA" in seg and "Mößgelauffer" in seg and "Mißgeburt" in seg and "z110-KRSTEN-DAN-PRAZEN" in seg)
check("I7d NEZAKONSKI-×7 + MODRI-×9 + Z49 + Z100", "NEZAKONSKI-×7-REKORD" in seg and "MODRI-MATIČARSKI-PRIPISI-×9-REKORD" in seg and "den-17.-Juli-1880-zuzschreiben" in seg and "Alojs-Alojzija" in seg)
check("I7e DUHOVNIŠKA-MENJAVA + z79-JULI + z15-FEB-20", "DUHOVNIŠKA-MENJAVA" in seg and "Janičar" in seg and "Dovgan" in seg and "z79-JULI" in seg and "z15-FEB-20-SANDWICH" in seg)
check("I8a meseci-Griblje (Jänner/April/August-×0!) + 1879-96-BONUS", "Jänner/April/August-×0" in seg and "F3+M4+Mai3+J2+Juli2+S2+O3+N1+D1" in seg and "1879 = 96" in seg)
check("I8b hišne-paralele + TOTER + LASIE + POŽEK + KLOBUČAR", "TOTER-garble" in seg and "LASIE~LAZAR-grafija-X-open" in seg and "POŽEK-oče-grafija-X-open" in seg and "KLOBUČAR-boter-nit-X-open" in seg and "P221-z1-h21" in seg and "P225-z81" in seg)
check("I9a qa-p226 (226. kontrola!)", "qa-p226" in qa and "226. kontrola" in qa)
pt = open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8").read()
check("I9b pt-luknja-167/1819 + byBook-04104", '"vitalsTotal": 1819' in pt and '"04104": 167' in pt)

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
