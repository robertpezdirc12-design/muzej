#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P227 — verifikator KRSTNE PREDZGODOVINE 04104, leto 1879 = 7/15 (I1–I10 + --live)."""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "04104",\s*year: 1879,', src)
check("I1 bloki 04104/1879-numeric == 22", len(bloki) == 22, f"najdeno {len(bloki)}")
pri = ["31", "68", "16", "18", "6", "22", "24", "17", "23", "49", "44", "7", "46", "22", "62", "17", "37", "63", "11", "31", "28", "40"]
check("I2 hiše-1879 (file-order, 22/19-DISTINCT — h31-×2 + h22-×2 + h17-×2-DUELI-REŠENI!)", bloki == pri and len(set(bloki)) == 19, ",".join(bloki[:8]) + "…")
skupaj = src.count('bookSignature: "04104"')
check("I3 vitals-1853 + 04104==201", "HOUSE_VITALS.length !== 1853" not in src and skupaj == 201, f"04104={skupaj}")

d = json.load(open(f"{ROOT}/research/issue17/parish-baptism-1879-04104.json", encoding="utf-8"))
grib = [e for e in d["entries"] if "grib" in str(e.get("vas", "")).lower()]
an = json.dumps(d["anomalije"], ensure_ascii=False)
check("I4 dokaz (22-griblje + MEJA-s105/s106-66.-POTRDITEV + 96-DISTINCT + pag-sken−6-14/14 + s112-'106')",
      len(grib) == 22
      and "s105/s106" in json.dumps(d["okvir"], ensure_ascii=False) and "66.-POTRDITEV" in an
      and "meja-1878-79-s105-s106" in an
      and "foliacija-sken-6-14-14" in an
      and d["frame"]["rowsTotal"] == 96 and d["stats"]["griblje_vpisov"] == 22
      and "14/14-SEKVENČNO" in d["frame"]["pagKonvencija"] and "100–113" in d["frame"]["pagKonvencija"],
      f"entries={len(d['entries'])} griblje={len(grib)} anomalije={len(d['anomalije'])}")
check("I4b novosti (dvojcki-zwillinge-x3 + todtgeboren-x3 + nezakonski-x2 + modri-x12 + duhovniska-izmenjava + z60-pogojni + z32 + z76)",
      "dvojcki-zwillinge-x3" in an and "todtgeboren-x3" in an and "nezakonski-x2" in an
      and "modri-pripisi-x12" in an and "duhovniska-izmenjava" in an
      and "z60-pogojni-krst" in an and "z32-imenski-popravek" in an and "z76-datumski-pripis" in an)

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 1853")
check("I5 qa-p227 + števec-1853", "qa-p227-parish-baptism-1879-04104" in qa and st >= 139, f"1853-številcev={st}")

i0 = src.find("P227: krstna PREDZGODOVINA 04104, leto 1879")
seg = src[i0:] if i0 >= 0 else ""
check("I6a 96-DISTINCT + MEJA-s105/s106-66.-POTRDITEV", "96-vpisov-DISTINCT" in seg and "vrstna-aritmetika" in seg and "2+8+7+7+6+6+7+8+8+9+8+7+8+5 = 96" in seg and "66.-POTRDITEV-invariante" in seg)
check("I6b FOLIACIJA-sken−6-14/14-SEKVENČNO + s112-'106'-PREDICTION", "14/14-SEKVENČNO" in seg and "100–113" in seg and "s112='106'-LEAD-PREDICTION-POTRJENA" in seg)
check("I6c RESTART-z1-8./9.-JÄNNER-Kloster-h37 + VSOTNA-RAZPETA-'1 8'+'79' + NAJPONEJŠI", "RESTART-z1-NA-DAN-8./9.-JÄNNER-Kloster-h37" in seg and "VSOTNA-RAZPETA-'1 8'+'79'" in seg and "7.-restart-z1-NAJPONEJŠI" in seg and "'Jahr 1878'-s-popravo-cifre" in seg)
check("I7a 22-GRIBLJE / 19-hiš (h31-×2 + h22-×2 + h17-×2-DUELI-REŠENI-MAX-krop)", "22-GRIBLJE / 19-hiš" in seg and "h31-×2" in seg and "h22-×2" in seg and "h17-×2" in seg and "MAX-krop" in seg)
check("I7b PEZDIRC-×12-continuum-7-let + MILEK-×6 + JAKOFČIČ-×5", "PEZDIRC-×12-vrstic" in seg and "grafija-continuum-7-let" in seg and "MILEK-×6" in seg and "JAKOFČIČ-×5" in seg)
check("I7c DVOJČKI-ZWILLINGE-×3-REKORD + TODTGEBOREN-×3 + NEZAKONSKI-z23", "DVOJČKI-ZWILLINGE-×3-REKORD" in seg and "'Zwillinge'-vertikalno-anotacijo" in seg and "TODTGEBOREN-garble-×3" in seg and "z23-NEZAKONSKI-GRIBLJE" in seg)
check("I7d MODRI-×12-REKORD + DUHOVNIŠKA-IZMENJAVA + z60-POGOJNI", "MODRI-MATIČARSKI-PRIPISI-×12-REKORD" in seg and "DUHOVNIŠKA-IZMENJAVA-1879" in seg and "z60-POGOJNI-KRST" in seg and "B.Dog" in seg)
check("I7e Z32-IMENSKI-POPRAVEK + Z76-DATUMSKI + HEBAMME", "z32-IMENSKI-POPRAVEK" in seg and "z76-DATUMSKI-PRIPIS" in seg and "z42-HEBAMME" in seg and "Maria-Rom" in seg)
check("I8a meseci-Griblje (März/Mai-×0!) + 1878-94-BONUS-LEAD", "März/Mai-×0" in seg and "J1+F2+A5+Juni2+Juli2+A2+S3+O1+N2+D2" in seg and "P228-LEAD" in qa and "1878" in qa)
check("I8b TAIL-1879 + †-15.6.1941 + DOVGAN-podpis + h-paralele", "TAIL-1879-ZAČETEK" in seg and "†-15.6.1941" in seg and "podpis-Franz-DOVGAN" in seg and "HURE-oče-nit" in seg and "P226-PARALELA" in seg)
check("I9a qa-p227 (227. kontrola!)", "qa-p227" in qa and "227. kontrola" in qa)
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
