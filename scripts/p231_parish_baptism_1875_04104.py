#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P231 — verifikator KRSTNE PREDZGODOVINE 04104, leto 1875 = 11/15 (I1–I10 + --live)."""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "04104",\s*year: 1875,', src)
check("I1 bloki 04104/1875-numeric == 17", len(bloki) == 17, f"najdeno {len(bloki)}")
pri = ["30", "48", "5", "28", "34", "37", "94", "33", "29", "64", "72", "38", "57", "48", "68", "1", "11"]
check("I2 hiše-1875 (file-order, 17-vpisov / 16-DISTINCT-h48-×2-DUEL!)", bloki == pri and len(set(bloki)) == 16, ",".join(bloki) if bloki else "-")
skupaj = src.count('bookSignature: "04104"')
check("I3 vitals-1940 + 04104==288", "HOUSE_VITALS.length !== 1889" not in src and skupaj == 288, f"04104={skupaj}")

d = json.load(open(f"{ROOT}/research/issue17/parish-baptism-1875-04104.json", encoding="utf-8"))
grib = [e for e in d["entries"] if "grib" in str(e.get("vas", "")).lower()]
an = json.dumps(d["anomalije"], ensure_ascii=False)
check("I4 dokaz (17-griblje + MEJA-s47-SREDI-PAGI-70.-POTRDITEV + 119-VPISOV + TAIL-RESTART + TROJNI-DUPLIKAT + sken−3)",
      len(grib) == 17
      and "s47-SREDI-PAGI" in json.dumps(d["okvir"], ensure_ascii=False) and "70.-POTRDITEV" in an
      and "meja-1874-75-s47-sredi-pagi-nova-varianta" in an
      and "vpisov-119-tail-restart-z1-z4-nova-varianta" in an
      and "trojni-duplikat-skenov-folio-57-novo-odkritje" in an
      and d["frame"]["rowsTotal"] == 119 and d["stats"]["griblje_vpisov"] == 17
      and "sken−3" in d["frame"]["pagKonvencija"] and "42–57" in d["frame"]["pagKonvencija"],
      f"entries={len(d['entries'])} griblje={len(grib)} anomalije={len(d['anomalije'])}")
check("I4b novosti (violet-retro-datirani + feber-1-prelim-brez-datuma + z100-todgeborene + nezakonski-x2 + duhovniki-10-7)",
      "violet-retro-vpis-z6-datirani-novi-tip" in an and "feber-1-prelim-brez-datuma" in an
      and "z100-milestone-todgeborene-garble" in an and "nezakonski-x2-griblje" in an
      and "duhovniki-dovgan-x10-hoggia-x7" in an)

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 2043")
check("I5 qa-p231 + števec-1940", "qa-p231-parish-baptism-1875-04104" in qa and st >= 143, f"1940-številcev={st}")

i0 = src.find("P231: krstna PREDZGODOVINA 04104, leto 1875")
seg = src[i0:] if i0 >= 0 else ""
check("I6a 119-VPISOV + aritmetika + zap-NEZAPISAN + TAIL-z1–z4", "119-VPISOV" in seg and "3+9+8+9+9+9+9+7+7+7+7+8+8+7+8+4 = 119" in seg and "zap-stolpec-NEZAPISAN-s47–s63" in seg and "TAIL-RESTART-z1–z4-LOKALNI" in seg)
check("I6b MEJA-s47-SREDI-PAGI + TAIL-1874-×5 + veliki-cifri-'1'+'8' + RESTART-z1-9./9. + 70.-POTRDITEV + BREZ-finis-1874", "MEJA-1874/75 = s47-SREDI-PAGI-NOVA-VARIANTA" in seg and "TAIL-1874-Dez-26–31-×5-vrstic" in seg and "veliki-cifri-'1'+'8'" in seg and "RESTART-z1-NA-DAN-9./9.-JÄNNER" in seg and "70.-POTRDITEV-invariante" in seg and "BREZ-'finis-Anni-1874'-KALLIGRAFIJE" in seg and "11.-restart" in seg)
check("I6c TROJNI-DUPLIKAT-folio-57 + sken−3-42–57 + sken−5-s63/s64 + 2-DUPLIKATA-pred-s45", "TROJNI-DUPLIKAT-folio-57" in seg and "s45–s60-'sken−3'-SEKVENČNO (42–57!" in seg and "s63='58'/s64='59'-'sken−5'-P230" in seg and "2-DUPLIKATA-PRED-s45" in seg)
check("I7a 17-GRIBLJE / 16-hiš-h48-DUEL", "17-GRIBLJE / 16-hiš" in seg and "h48-×2-DUEL" in seg and "h94" in seg and "h68" in seg and "h1" in seg)
check("I7b PEZDIRC-×5-NAJNIŽJA + continuum-11-let + MILEK-×4 + HRIŽAN-×6 + DRAGOŠ-×3", "PEZDIRC-×5-NAJNIŽJA" in seg and "continuum-11-let" in seg and "MILEK-×4" in seg and "HRIŽAN-×6" in seg and "DRAGOŠ-×3-KOMPLET" in seg)
check("I7c NEZAKONSKI-×2 + MODRI-×4 + ledig.-NOTA + VIOLET-RETRO-z6-DATIRANI + FEBER-1-BREZ-DATUMA", "NEZAKONSKI-×2-GRIBLJE" in seg and "MODRI-×4-Griblje" in seg and "'ledig.'-NOTA" in seg and "VIOLET-RETRO-VPIS-z6-datiran" in seg and "FEBER-1-PRELIM-BREZ-DATUMA" in seg)
check("I7d z100-MILESTONE-TODGEBORENE + HEBAMME-Maria-Born + DUHOVNIKI-10/7 + meseci-2-prazne", "z100-MILESTONE-TODGEBORENE" in seg and "HEBAMME-Maria-Born[~Rom]-×2" in seg and "DOVGAN-×10/HOGGIA-×7" in seg and "August+September-×0!-2-prazne" in seg)
check("I7e TAIL-1874-zap-72–87-VIDEN + 1874-sklenjen + GLAVE-NI-meja", "TAIL-1874-zap-72–87-VIDEN-×2-strani" in seg and "1874-sklenjen-z~92" in seg and "glave-'Jahr 1874'-×3/'Jahr 1875'-×14-glava-NI-meja" in seg)
check("I8a meseci-Griblje (August+September-×0!) + 1874-LEAD", "August+September-×0" in seg and "P232-LEAD" in qa and "1874" in qa)
check("I8b TAIL-1875-s64 + finis-Anni-1875-P230 + z3t-KRIŽ", "TAIL-1875" in seg and "finis-Anni-1875" in seg and "s64-r3-P230" in seg)
check("I9a qa-p231 (231. kontrola!)", "qa-p231" in qa and "231. kontrola" in qa)
pt = open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8").read()
check("I9b pt-luknja-271/2043 + byBook-04104", '"vitalsTotal": 2043' in pt and '"04104": 288' in pt)

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
