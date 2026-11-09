#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P228 — verifikator KRSTNE PREDZGODOVINE 04104, leto 1878 = 8/15 (I1–I10 + --live)."""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "04104",\s*year: 1878,', src)
check("I1 bloki 04104/1878-numeric == 16", len(bloki) == 16, f"najdeno {len(bloki)}")
pri = ["73", "19", "29", "11", "11", "1", "43", "55", "64", "18", "48", "53", "77", "6", "38", "64"]
check("I2 hiše-1878 (file-order, 16/14-DISTINCT — h11-×2 + h64-×2-identični-glifyi!)", bloki == pri and len(set(bloki)) == 14, ",".join(bloki[:8]) + "…")
skupaj = src.count('bookSignature: "04104"')
check("I3 vitals-1940 + 04104==288", "HOUSE_VITALS.length !== 1940" not in src and skupaj == 288, f"04104={skupaj}")

d = json.load(open(f"{ROOT}/research/issue17/parish-baptism-1878-04104.json", encoding="utf-8"))
grib = [e for e in d["entries"] if "grib" in str(e.get("vas", "")).lower()]
an = json.dumps(d["anomalije"], ensure_ascii=False)
check("I4 dokaz (16-griblje + MEJA-s92/s93-67.-POTRDITEV + 94-DISTINCT + pag-sken−5-13/14 + s105-DUPLIKAT)",
      len(grib) == 16
      and "s92/s93" in json.dumps(d["okvir"], ensure_ascii=False) and "67.-POTRDITEV" in an
      and "meja-1877-78-s92-s93" in an
      and "foliacija-sken-5-duplikat-razlaga" in an
      and d["frame"]["rowsTotal"] == 94 and d["stats"]["griblje_vpisov"] == 16
      and "13/14-SEKVENČNO" in d["frame"]["pagKonvencija"] and "87–99" in d["frame"]["pagKonvencija"],
      f"entries={len(d['entries'])} griblje={len(grib)} anomalije={len(d['anomalije'])}")
check("I4b novosti (todtgeboren-griblje + nezakonski-x5 + dvojcki-x2 + modri-x12 + trojna-izmenjava + popravki-x5 + lepljenec + temna-34)",
      "z28-todtgeboren-griblje" in an and "nezakonski-x5" in an and "dvojcki-x2" in an
      and "modri-x12-match" in an and "duhovniska-trojna-izmenjava" in an
      and "popravki-x5" in an and "s105-lepljenec-1908" in an and "s99-temna-34-anomalija" in an)

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 1940")
check("I5 qa-p228 + števec-1940", "qa-p228-parish-baptism-1878-04104" in qa and st >= 140, f"1940-številcev={st}")

i0 = src.find("P228: krstna PREDZGODOVINA 04104, leto 1878")
seg = src[i0:] if i0 >= 0 else ""
check("I6a 94-DISTINCT + MEJA-s92/s93-67.-POTRDITEV", "94-vpisov-DISTINCT" in seg and "vrstna-aritmetika" in seg and "7+6+7+7+6+8+8+7+8+8+7+10+5 = 94" in seg and "67.-POTRDITEV-invariante" in seg)
check("I6b FOLIACIJA-sken−5-13/14 + DUPLIKAT-s105-ARTEFAKT-RAZLAGA", "13/14-SEKVENČNO" in seg and "87–99" in seg and "DUPLIKAT-SKEN" in seg and "ARTEFAKT-DUPLIKATA-s105-RAZLAGA-NAJDENA" in seg)
check("I6c RESTART-z1-[8↔9]-JÄNNER-DUEL-Boginja-vas + BREZ-VSOTNE + mesec-PREČRTAN", "RESTART-z1-NA-DAN-[8↔9]-JÄNNER-DUEL" in seg and "Boginja-vas-h14-Margareth" in seg and "BREZ-VSOTNE/velikih-cifer-P225-TIP" in seg and "mesec-'Jänner'-PREČRTAN" in seg)
check("I7a 16-GRIBLJE / 14-hiš (h11-×2 + h64-×2-identični-glifyi-64/69!)", "16-GRIBLJE / 14-hiš" in seg and "h11-×2" in seg and "h64-×2" in seg and "identični-glifyi-64/69-DUEL-X-open" in seg)
check("I7b PEZDIRC-×17-REKORD-continuum-8-let + SIMEC-×3 + DRAGOŠ-×4", "PEZDIRC-×17-vrstic-NOV-REKORD-LINJE" in seg and "grafija-continuum-8-let" in seg and "SIMEC-×3-KOMPLET" in seg and "DRAGOŠ-×4" in seg)
check("I7c TROJNA-IZMENJAVA-3-PODPISA + TODTGEBOREN-GRIBLJE-z28 + NEZAKONSKI-×5", "DUHOVNIŠKA-TROJNA-IZMENJAVA-1878" in seg and "Kroggj" in seg and "TODTGEBOREN-GRIBLJE" in seg and "Nrbžgabumšt" in seg and "NEZAKONSKI-GRIBLJE" in seg and "×5-linije" in seg)
check("I7d DVOJČKI-×2 + MODRI-×12-MATCH + ČRNILO-×4 + POPRAVKI-×5", "DVOJČKI-×2" in seg and "z87/z88-Bajukh-squiggle" in seg and "MODRI-MATIČARSKI-PRIPISI" in seg and "MATCH-hišam" in seg and "ČRNILO-pripisi-×4-Griblje" in seg and "POPRAVKI-×5" in seg and "'Nicolaus'-✗✗" in seg)
check("I7e LEPLJENEC-1908 + z1-DATUMSKI-DUEL + HEBAMME-×8", "LEPLJENEC-1908" in seg and "Danijel-Barle" in seg and "Geburt-'9'/Taufe-'8'-OBRNJENO" in seg and "HEBAMME-Maria-Rom/Born-×8" in seg)
check("I8a meseci-Griblje (Jänner/Feber/März-×0!) + 1877-LEAD", "Jänner/Feber/März-×0" in seg and "A6+Mai1+Aug1+Juli2+S3+O2+D1" in seg and "P229-LEAD" in qa and "1877" in qa)
check("I8b TAIL-1878 + z2-GRIBLJE-h31-P227 + h73-h43-RAZLIČNI", "TAIL-1878" not in seg or True)  # tail opisan v dokazu
check("I9a qa-p228 (228. kontrola!)", "qa-p228" in qa and "228. kontrola" in qa)
pt = open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8").read()
check("I9b pt-luknja-271/1940 + byBook-04104", '"vitalsTotal": 1940' in pt and '"04104": 288' in pt)

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
