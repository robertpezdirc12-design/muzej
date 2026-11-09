#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P232 — verifikator KRSTNE PREDZGODOVINE 04104, leto 1874 = 12/15 (I1–I10 + --live)."""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "04104",\s*year: 1874,', src)
check("I1 bloki 04104/1874-numeric == 19", len(bloki) == 19, f"najdeno {len(bloki)}")
pri = ["12", "46", "45", "44", "18", "30", "48", "39", "40", "60", "49", "9", "13", "66", "32", "3", "40", "22", "65"]
check("I2 hiše-1874 (file-order, 19-vpisov / 18-DISTINCT-h40-×2-DUEL!)", bloki == pri and len(set(bloki)) == 18, ",".join(bloki) if bloki else "-")
skupaj = src.count('bookSignature: "04104"')
check("I3 vitals-1940 + 04104==288", "HOUSE_VITALS.length !== 1889" not in src and skupaj == 288, f"04104={skupaj}")

d = json.load(open(f"{ROOT}/research/issue17/parish-baptism-1874-04104.json", encoding="utf-8"))
grib = [e for e in d["entries"] if "grib" in str(e.get("vas", "")).lower()]
an = json.dumps(d["anomalije"], ensure_ascii=False)
check("I4 dokaz (19-griblje + MEJA-s37-INITIUM-71.-POTRDITEV + 92-VPISOV-LEAD-1:1 + TAIL-1873-zap-28 + sken−3-33–44)",
      len(grib) == 19
      and "s37-SREDI-PAGI" in json.dumps(d["okvir"], ensure_ascii=False) and "71.-POTRDITEV" in an
      and "meja-1873-74-s37-sredi-pagi-initium-kalligrafija-nova-varianta" in an
      and "vpisov-92-lead-1-1-potrjeno" in an
      and "foliacija-sken-3-sekvenčno-33-44-brez-duplikatov" in an
      and d["frame"]["rowsTotal"] == 92 and d["stats"]["griblje_vpisov"] == 19
      and "sken−3" in d["frame"]["pagKonvencija"] and "33–44" in d["frame"]["pagKonvencija"],
      f"entries={len(d['entries'])} griblje={len(grib)} anomalije={len(d['anomalije'])}")
check("I4b novosti (trioduhovnikov + pezdirc-x7-porast + brez-praznih-meseci + modri-1882-1947 + s43-glava-misread + skrile-izkljucitev)",
      "trioduhovnikov-1874-novi-x2" in an and "pezdirc-x7-porast-milek-x7-rekord" in an
      and "brez-praznih-meseci-1-liniji" in an and "modri-x4-griblje-razpon-1882-1947" in an
      and "s43-glava-1871-vlm-misread" in an and "s39-r3-skrile-vas-izkljucitev" in an)

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 1940")
check("I5 qa-p232 + števec-1940", "qa-p232-parish-baptism-1874-04104" in qa and st >= 144, f"1940-številcev={st}")

i0 = src.find("P232: krstna PREDZGODOVINA 04104, leto 1874")
seg = src[i0:] if i0 >= 0 else ""
check("I6a 92-VPISOV + aritmetika + 1874-sklenjen-z92 + LEAD-1:1", "92-VPISOV" in seg and "7+8+9+11+9+9+9+9+8+8+5 = 92" in seg and "1874-sklenjen-z92" in seg and "LEAD-'~92'-1:1-POTRJENO" in seg)
check("I6b MEJA-s37-INITIUM + TAIL-1873-zap-28 + RESTART-z1-1./1. + krst-4. + 71.-POTRDITEV + 12.-restart", "MEJA-1873/74 = s37-SREDI-PAGI" in seg and "Initium-anni-Domini-1874" in seg and "TAIL-1873" in seg and "zap-28" in seg and "RESTART-z1-NA-DAN-1./1.-JÄNNER" in seg and "krst-4." in seg and "71.-POTRDITEV-invariante" in seg and "12.-restart" in seg)
check("I6c 'sken−3'-33–44-SEKVENČNO + formula-CONTINUES + 2-DUPLIKATA-pred-s36", "'sken−3'-SEKVENČNO-s36–s47 (33–44!" in seg and "formula-CONTINUES-iz-P231" in seg and "2-DUPLIKATA-še-vedno-pred-s36" in seg)
check("I7a 19-GRIBLJE / 18-hiš-h40-DUEL", "19-GRIBLJE / 18-hiš" in seg and "h40-×2-DUEL" in seg and "h9-NOVA" in seg and "h66" in seg and "h3" in seg)
check("I7b PEZDIRC-×7-PORAST + MILEK-×7-REKORD + HRIŽAN-×5", "PEZDIRC-×7-Griblje-PORAST" in seg and "MILEK-×7-REKORD-PORAST" in seg and "HRIŽAN-×5" in seg)
check("I7c zap-ARITMETIKA-4/4 + NEZAKONSKI-×0 + MODRI-×4 + BREZ-PRAZNIH-MESECEV", "POZICIJSKA-ARITMETIKA-4/4-POTRJENA" in seg and "NEZAKONSKI-×0-GRIBLJE" in seg and "MODRI-×4-Griblje" in seg and "BREZ-PRAZNIH-MESECEV-1.-LINIJI" in seg)
check("I7d TRI-duhovnika + 'Albin-Schwinger' + 'Fabijan-Kragelj' + TAIL-1874-GRIBLJE-KRIŽ", "TRI-duhovnika-1874" in seg and "'Albin-Schwinger-Coop'-NOVI" in seg and "'Fabijan-Kragelj[?]-Cap'-NOVI-X-open" in seg and "TAIL-1874-GRIBLJE" in seg and "P231-1:1-KRIŽ" in seg)
check("I7e X-ločitve (Hlobučar-3-way + Koblar-3-way + Jarrec-NE-Simec + Zgajdire + h40-REŠEN-×2 + h45/h32/h22/h66)", "HLOBUČAR-oče-X-★★★" in seg and "KOBLAR-oče-X-★★★" in seg and "JARREC-oče-X-★★★" in seg and "ZGAJDIRE-oče-X-★★★" in seg and "hisna-40-×2-DELO-DUEL" in seg and "hisna-45/25-DUEL-X-★★★-REŠEN-'45'" in seg and "hisna-32/52/62-TROJNI-DUEL-X-★★★-REŠEN-'32'" in seg and "22/42-DUEL-X-★★★-REŠEN-'22'" in seg and "hisna-66/64-X-rešen-'66'" in seg)
check("I8a meseci-BREZ-PRAZNIH + 1873-LEAD", "BREZ-PRAZNIH-MESECEV-1.-LINIJI" in seg and "P233-LEAD" in qa and "1873" in qa)
check("I8b s47-SREDI-PAGI-MEJA-1874/75-P231 + GLAVE-'Jahr 1873'-×2", "s47-SREDI-PAGI-MEJA-1874/75-P231" in seg and "GLAVE-'Jahr 1873'-×2 (s36–s37!" in seg)
check("I9a qa-p232 (232. kontrola!)", "qa-p232" in qa and "232. kontrola" in qa)
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
