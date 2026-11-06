#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P218 — verifikator MRLIŠKE PREDZGODOVINE 04106, leto 1859 (predzgodovina-27/29). I1–I10 + --live."""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'\{\s*houseNo:\s*"(\d+)",\s*bookSignature:\s*"04106",\s*year:\s*1859,', src)
check("I1 bloki 04106/1859-numeric == 23", len(bloki) == 23, f"najdeno {len(bloki)}")
pri = ["69", "21", "37", "39", "65", "57", "5", "19", "26", "58", "52", "39", "5", "19", "33", "74", "29", "20", "24", "52", "21", "49", "65"]
check("I2 hiše-1859-numeric (file-order)", bloki == pri, ",".join(bloki))
skupaj = src.count('bookSignature: "04106"')
check("I3 vitals-1642 + 04106==423", "HOUSE_VITALS.length !== 1642" not in src and skupaj == 423, f"04106={skupaj}")

d = json.load(open(f"{ROOT}/research/issue17/parish-death-1859-04106.json", encoding="utf-8"))
grib = [e for e in d["entries"] if "gribl" in str(e.get("vas", "")).lower() and "grem" not in str(e.get("vas", "")).lower()]
an = json.dumps(d["anomalije"], ensure_ascii=False)
cc = json.dumps(d["crossChecks"], ensure_ascii=False)
check("I4 dokaz (103/23-griblje + meja-s11-1858/59 + 103-vrstic + vsotna-'1 8 [5 9]' + naslovni-list)",
      len(d["entries"]) == 103 and len(grib) == 23
      and "s11" in d["okvir"]["meja_1858_59"] and "1 8 [5 9]" in d["okvir"]["meja_1858_59"]
      and "luknja-92" in an and d["statistika"]["vpisov_1859"] == 103,
      f"entries={len(d['entries'])} griblje={len(grib)} anomalije={len(d['anomalije'])}")
check("I4b nestevilcena-jalkic + naslovni-list-×2 + p217-tail-korekcije + genickstarre-epidemija",
      "nestevilcena-jalkic" in an and "naslovni-list-×2" in an and "p217-tail-korekcije" in an and "genickstarre-epidemija" in an)
check("I4c nov-duhovnik-knavs + paric-fraisen-klaster + z81-trajni-duel",
      "nov-duhovnik-knavs" in an and "paric-fraisen-klaster" in an and "z81-trajni-duel-99-83" in an)

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 1642")
check("I5 qa-p218 + števec-1632", "qa-p218-parish-death-1859-04106" in qa and st >= 125, f"1642-številcev={st}")

i0 = src.find("P218: mrliška PREDZGODOVINA 04106, leto 1859")
seg = src[i0:] if i0 >= 0 else ""
check("I6a 103-VPIISOV-ŠTEVJE-IZ-VRSTIC-20.× + NEŠTEVILČENA", "103 vpisov" in seg and "ŠTEVJE-IZ-VRSTIC-20.×" in seg and "NEŠTEVILČENA" in seg)
check("I6b LUKNJA-92 + s19-NASLOVNI-LIST-PONOVLJEN", "LUKNJA-92" in seg and "NASLOVNI-LIST-PONOVLJEN" in seg)
check("I6c P217-TAIL-MISREADI-KOREKCIJE (z94-'14-DNI'-FALSIFIKACIJA!)", "P217-TAIL-MISREADI-KOREKCIJE" in seg and "14-DNI" in seg and "FALSIFICIRAN" in seg)
check("I7a MEJA-s11 (naslovni-list-DEEL-2 + vsotna-'1 8 [5 9]'-marker + 56.-POTRDITEV!)", "MEJA-1858/59-s11" in seg and "NASLOVNI-LIST-'Sterb-Buch.'-DEEL-2" in seg and "56.-POTRDITEV" in seg)
check("I7b GENICKSTARRE-EPIDEMIJA-×4", "GENICKSTARRE-EPIDEMIJA" in seg and "×4" in seg)
check("I7c NOV-DUHOVNIK-'Joh.-Knavs' + PARIČ-klaster + TRAJNI-DUEL", "NOV-DUHOVNIK-'Joh.-Knavs'" in seg and "PARIČ-FRAISEN-klaster" in seg and "99J[~83!]-TRAJNI-DUEL" in seg)
check("I8a 23-GRIBLJE-REKORD-PREDZGODOVINE (prej-20-1867!)", "23-GRIBLJE-blokov = NOV-REKORD-PREDZGODOVINE" in seg and "prej-20-1867" in seg)
check("I8b PEZDIRC-MREŽA-globlje (Posdiac/Pesdire!)", "PEZDIRC-MREŽA" in seg)
check("I8c otroška-umrljivost-35%-8/23 + ekstremi-14-DNI→99J", "otroška-umrljivost-35%-8/23" in seg and "14-DNI→99J" in seg)
check("I8d h65-×2-MILEK-3-obdobja + VOJAK-Lediknant", "h65 = P155-1889-MILEK-hiša" in seg and "VOJAK" in seg)
check("I9a qa-p218 (218. kontrola!)", "qa-p218" in qa and "218. kontrola" in qa)
pt = open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8").read()
check("I9b pt-luknja-413/1632", '"vitalsTotal": 1642' in pt and '"04106": 423' in pt)

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
