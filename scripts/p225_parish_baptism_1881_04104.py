#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P225 — verifikator KRSTNE PREDZGODOVINE 04104, leto 1881 = 5/15 (I1–I10 + --live)."""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "04104",\s*year: 1881,', src)
check("I1 bloki 04104/1881-numeric == 17", len(bloki) == 17, f"najdeno {len(bloki)}")
pri = ["55", "37", "3", "38", "49", "20", "17", "8", "62", "51", "63", "14", "57", "24", "6", "22", "42"]
check("I2 hiše-1881 (file-order, 17-VSE-DISTINCT!)", bloki == pri and len(set(bloki)) == 17, ",".join(bloki[:8]) + "…")
skupaj = src.count('bookSignature: "04104"')
check("I3 vitals-1870 + 04104==201", "HOUSE_VITALS.length !== 1870" not in src and skupaj == 218, f"04104={skupaj}")

d = json.load(open(f"{ROOT}/research/issue17/parish-baptism-1881-04104.json", encoding="utf-8"))
grib = [e for e in d["entries"] if "gribl" in str(e.get("vas", "")).lower() and "grem" not in str(e.get("vas", "")).lower()]
an = json.dumps(d["anomalije"], ensure_ascii=False)
check("I4 dokaz (17-griblje + MEJA-s135/s136-64.-POTRDITEV + 89-DISTINCT + pag-sken−6-13/13 + brez-luknje)",
      len(grib) == 17
      and "s135/s136 (64.-POTRDITEV" in json.dumps(d["okvir"], ensure_ascii=False)
      and "meja-1880-81-s135-s136" in an
      and "foliacija-sken-6-sekvenčno" in an
      and d["frame"]["rowsTotal"] == 89 and d["stats"]["vpisov_distinct"] == 89
      and "13/13-SEKVENČNO" in d["frame"]["pagKonvencija"] and "129–141" in d["okvir"]["pag"],
      f"entries={len(d['entries'])} griblje={len(grib)} anomalije={len(d['anomalije'])}")
check("I4b novosti (z48-botra-prazna + z66-nezakonski + porocni-pripisi + z14-april + mreze-1881)",
      "z48-botra-prazna" in an and "z66-nezakonski" in an
      and "porocni-pripisi-×2" in an and "z14-mesec-duel-april" in an and "mreze-1881" in an)

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 1870")
check("I5 qa-p225 + števec-1870", "qa-p225-parish-baptism-1881-04104" in qa and st >= 137, f"1870-številcev={st}")

i0 = src.find("P225: krstna PREDZGODOVINA 04104, leto 1881")
seg = src[i0:] if i0 >= 0 else ""
check("I6a 89-DISTINCT + MEJA-s135/s136-64.-POTRDITEV", "89-vpisov-DISTINCT" in seg and "vrstna-aritmetika" in seg and "7+7+7+7+7+7+8+8+8+8+8+7 = 89" in seg and "64.-POTRDITEV-invariante" in seg)
check("I6b FOLIACIJA-sken−6-13/13-SEKVENČNO + sandwich", "13/13-SEKVENČNO" in seg and "129–141" in seg and "sandwich" in seg and "s143='137'" in seg and "s145='139'" in seg)
check("I6c RESTART-z1-GRIBLJE-h55 + Finis-BREZ-VSOTNE", "RESTART-z1-NA-DAN-1.-1.-JÄNNER-GRIBLJE-h55" in seg and "'Finis'" in seg and "BREZ-VSOTNE" in seg and "4.-GRIBLJE-restart-z1" in seg)
check("I7a 17-GRIBLJE / 17-hiš-VSE-DISTINCT", "17-GRIBLJE / 17-hiš-VSE-DISTINCT" in seg and "brez-duplikatov" in seg)
check("I7b PEZDIRC-×9-REKORD + KRIŽAN-×6 + BRODARIČ-×6", "PEZDIRC-×9-NOV-REKORD" in seg and "×12" in seg and "KRIŽAN-×6" in seg and "BRODARIČ-×6" in seg and "grafija-continuum-5-let" in seg)
check("I7c POROKE-'VNALILA'-×2 + Z48-BOTRA-PRAZNA + Z66-NEZAKONSKI", "Vnalila" in seg and "VNALILA" in seg and "BOTRA-PRAZNA-ANOMALIJA" in seg and "NEZAKONSKI-VPIS" in seg)
check("I7d Z14-APRIL-REŠEN + pripisi-MMK-†-×2", "APRIL-1" in seg and "31-März'-ZAVRNJENO" in seg and "†-16.12.1931" in seg and "Umrła-11.11.1960" in seg)
check("I8a meseci-Griblje (Feber/März/Dez-×0!) + 1880-122-BONUS", "Feber/März/Dez-×0" in seg and "J1+A1+Juni2+Juli1+Aug4+Sep2+Okt3+Nov3" in seg and "1880 = 122" in seg)
check("I8b hišni-DUELI-1:1-×3 (z15-37! + z40-49! + z66-57!)", "hiša-'37'-DUEL-1:1" in seg and "hiša-'49'-DUEL-1:1" in seg and "hiša-'57'-DUEL-1:1" in seg)
check("I9a qa-p225 (225. kontrola!)", "qa-p225" in qa and "225. kontrola" in qa)
pt = open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8").read()
check("I9b pt-luknja-201/1870 + byBook-04104", '"vitalsTotal": 1870' in pt and '"04104": 218' in pt)

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
