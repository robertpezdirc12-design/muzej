#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P222 — verifikator KRSTNE PREDZGODOVINE 04104, leto 1884 = 2/15 (I1–I10 + --live)."""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "04104",\s*year: 1884,', src)
check("I1 bloki 04104/1884-numeric == 21", len(bloki) == 21, f"najdeno {len(bloki)}")
pri = ["[?]", "13", "5", "[?]", "2", "56", "36", "68", "69", "13", "22", "[?]", "20", "51", "[?]", "18", "49", "23", "62", "8", "43"]
check("I2 hiše-1884 (file-order, h13-×2! + 3-×-[?]-DUELI!)", bloki == pri, ",".join(bloki[:8]) + "…")
skupaj = src.count('bookSignature: "04104"')
check("I3 vitals-1819 + 04104==151", "HOUSE_VITALS.length !== 1819" not in src and skupaj == 167, f"04104={skupaj}")

d = json.load(open(f"{ROOT}/research/issue17/parish-baptism-1884-04104.json", encoding="utf-8"))
grib = [e for e in d["entries"] if "gribl" in str(e.get("vas", "")).lower() and "grem" not in str(e.get("vas", "")).lower()]
an = json.dumps(d["anomalije"], ensure_ascii=False)
check("I4 dokaz (21-griblje + MEJA-s173 + z84-DUPLIKAT + s175 + s177 + 112-DISTINCT + pag-sken+13)",
      len(grib) == 21
      and "s173 (61.-POTRDITEV" in json.dumps(d["okvir"], ensure_ascii=False)
      and "z84-DUPLIKAT" in an
      and "s175" in an and "s177" in an
      and d["frame"]["rowsTotal"] == 112 and d["stats"]["vpisov_distinct"] == 112
      and "sken+13" in d["okvir"]["pag"],
      f"entries={len(d['entries'])} griblje={len(grib)} anomalije={len(d['anomalije'])}")
check("I4b pisar-anomalije (s175-prepiše + s177-REORIZENTACIJA + z84-DUPLIKAT + s184-prazna)",
      "pisar-ostevilcenje-s175" in an and "pisar-reorientacija-s177" in an
      and "z84-duplikat-s183" in an and "s184-prazna-vrstica-revizije" in an)
check("I4c vas-dueli-reseni + krstni-pripisi + mreze-1884",
      "vas-dueli-reseni" in an and "krstni-pripisi-kriz-mrlisko-1884" in an and "mreze-1884" in an)

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 1819")
check("I5 qa-p222 + števec-1819", "qa-p222-parish-baptism-1884-04104" in qa and st >= 135, f"1819-številcev={st}")

i0 = src.find("P222: krstna PREDZGODOVINA 04104, leto 1884")
seg = src[i0:] if i0 >= 0 else ""
check("I6a 112-DISTINCT-ŠTEVJE-IZ-VRSTIC-2.× + MEJA-s173-61.-POTRDITEV", "112-vpisov-DISTINCT" in seg and "ŠTEVJE-IZ-VRSTIC-2.×" in seg and "61.-POTRDITEV-invariante" in seg)
check("I6b PISARJEVE-ANOMALIJE (s175-prepiše-8–14 + s177-REORIZENTACIJA-61–68→31–38!)", "s175-prepiše-8–14" in seg and "s177-REORIZENTACIJA" in seg and "61–68-prečrtano-×8→31–38" in seg)
check("I6c z84-DUPLIKAT (NOVA-TIP!) + s184-prazna-vrstica", "z84-DUPLIKAT" in seg and "1-PRAZNA-NEŠTEVILČENA-VRSTICA" in seg)
check("I7a 21-GRIBLJE / 20-hiš (h13-×2!)", "21-GRIBLJE / 20-hiš (h13-×2" in seg)
check("I7b vas-DUELI-REŠENI-krop-hi (z99-GRIBLJE! z52/z60-IZLOČENI!)", "z99-GRIBLJE-JASNO" in seg and "z52-PRILOZJE-IZLOČEN" in seg and "z60-BORŠT-IZLOČEN" in seg)
check("I7c POZNEJŠI-PRIPISI-KRIŽ-04106 (†29/10-1887 + †28/12-1887 + MMK-1974!)", "†29/10-1887" in seg and "†28/12-1887" in seg and "1974" in seg)
check("I8a mreže-1884 (PEZDIRC-×4 + KRIŽAN-×3 + BRODARIČ-×5 + MILEK + LAZAR!)", "PEZDIRC-×4" in seg and "KRIŽAN-×3" in seg and "BRODARIČ-×5" in seg and "MILEK" in seg and "LAZAR" in seg)
check("I8b pag-sken+13-RE-POTRJENO-×3 + 61.-POTRDITEV", "sken+13-FOLIO-SVINČNIK" in seg and "re-potrjeno-×3" in seg)
check("I9a qa-p222 (222. kontrola!)", "qa-p222" in qa and "222. kontrola" in qa)
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
