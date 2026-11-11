#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P235 — verifikator KRSTNE PREDZGODOVINE 04104, leto 1871 = 15/15 — LINIJA KOMPLETNA (I1–I10 + --live)."""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "04104",\s*year: 1871,', src)
check("I1 bloki 04104/1871-numeric == 17", len(bloki) == 17, f"najdeno {len(bloki)}")
pri = ["24", "23", "60", "5", "46", "4", "69", "12", "1", "48", "28", "28", "65", "72", "26", "6", "10"]
check("I2 hiše-1871 (file-order, 17-vpisov / 16-DISTINCT-h28-×2-DUEL!)", bloki == pri and len(set(bloki)) == 16, ",".join(bloki) if bloki else "-")
skupaj = src.count('bookSignature: "04104"')
check("I3 vitals-1940 + 04104==288", "HOUSE_VITALS.length !== 1940" not in src and skupaj == 288, f"04104={skupaj}")

d = json.load(open(f"{ROOT}/research/issue17/parish-baptism-1871-04104.json", encoding="utf-8"))
grib = [e for e in d["entries"] if "grib" in str(e.get("vas", "")).lower()]
an = json.dumps(d["anomalije"], ensure_ascii=False)
check("I4 dokaz (17-griblje + 108-ARITMETIKA + MEJA-1870/71-ZAČETEK-KNJIGE + DUPLIKAT-s3=s4 + nalepek-15-let)",
      len(grib) == 17
      and "108-vpisov-aritmetricni-model" in an
      and "meja-1870-71-zacetek-knjige-nalepek-15-let" in an
      and "meja-1871-72-page-boundary-p234-re-use" in an
      and "duplikat-s3-s4-resitev-p234-uge" in an
      and "dvojcki-z72-z73-zwillinge-x-potrjen" in an
      and d["frame"]["rowsTotal"] == 108 and d["stats"]["griblje_vpisov"] == 17
      and "s3='1'" in d["frame"]["pagKonvencija"] and "s28=s29-fol-25" in d["frame"]["pagKonvencija"],
      f"entries={len(d['entries'])} griblje={len(grib)} anomalije={len(d['anomalije'])}")
check("I4b novosti (pezdirc-x8-peter-x3 + milič-x5 + jakofčič-sakofčič + hrižan-x9 + duhovniki + dvojčki + prečrtani)",
      "pezdirc-x8-peter-x3-z81-ekspliciten" in an and "milič-x5-jakofčič-x11-hrižan-x9-rekordi" in an
      and "duhovniki-1871-ekstrahirani-weisel-continuum" in an and "precrtani-z37-z38-dvojni-harasinič" in an
      and "h28-x2-duel-3-leto-vzorec-continuum" in an)

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 2059")
check("I5 qa-p235 + števec-2059 (P258-kaskada!)", "qa-p235-parish-baptism-1871-04104" in qa and st >= 147, f"2059-številcev={st}")

i0 = src.find("P235: krstna PREDZGODOVINA 04104, leto 1871")
seg = src[i0:] if i0 >= 0 else ""
check("I6a 108-VPISOV + SEKVENČNO-1:1 + 116−8-DUPLIKAT + LEAD-POTRJENO", "108-VPISOV-ARITMETIČNI-MODEL" in seg and "SEKVENČNO-1:1-10/10-strani" in seg and "116-vrstic-−-8-DUPLIKAT = 108-DISTINCT-VPISOV" in seg and "vs-LEAD-'~90–110'-POTRJENO-1:1" in seg)
check("I6b MEJA-1870/71-ZAČETEK-KNJIGE + 13.-restart + MEJA-1871/72 + 12.-restart-P234", "MEJA-1870/71 = ZAČETEK-KNJIGE" in seg and "13.-restart" in seg and "MEJA-1871/72 = s13/s14-PAGE-BOUNDARY" in seg and "12.-restart-P234-SUPER" in seg)
check("I6c FOLIACIJA-KOMPLETNA + DUPLIKAT-s3=s4 + 2-DUPLIKATA-KNJIGE", "FOLIACIJA-'sken−3'-KOMPLETNA-FORMULA-KNJIGE-s3–s14" in seg and "DUPLIKAT-s3 = s4-RESITEV" in seg and "2-DUPLIKATA-KNJIGE" in seg and "108-TOTAL-1871-INTAKTEN" in seg)
check("I7a 17-GRIBLJE / 16-hiš-h28-DUEL-3.-LETO + h69-continuum-×3 + h12-continuum", "17-GRIBLJE / 16-hiš" in seg and "h28-×2-DUEL-z81-Pezdirc" in seg and "h69-×3-CONTINUUM-v-3-letih" in seg and "h12-CONTINUUM" in seg)
check("I7b PEZDIRC-×8-'Peter'-×3 + MILIČ-×5 + JAKOFČIČ-×11-ish + HRIŽAN-×9", "PEZDIRC-×8-'Peter'-×3-linije" in seg and "MILIČ-×5-oseb-REKORD" in seg and "JAKOFČIČ-×11-ish-REKORD" in seg and "HRIŽAN-×9-oseb-REKORD" in seg)
check("I7c KLOBUČAR-×5 + BRODARIČ-×5 + DRAGOŠ-×6-DVOJNI + POŽEK-nit", "KLOBUČAR-×5" in seg and "BRODARIČ-×5" in seg and "DRAGOŠ-×6-oseb (z46-DVOJNI-oče+matec" in seg and "POŽEK-nit" in seg)
check("I7d DUHOVNIKI-EKSTRAHIRANI + z81-X-POTRJEN + z80-X + TAIL-VERIGA-z98", "DUHOVNIKI-1871-EKSTRAHIRANI-1:1" in seg and "'Peter-Pezdirc-in-Griblach'" in seg and "KLOBUČAR-oče-nit-EKSPPLICITEN" in seg and "TAIL-VERIGA-z98" in seg)
check("I7e DVOJČKI + PREČRTANI + z91-PRAZNO + z30-TOTGEBOREN + NEZ-×1 + MODRI-×3-1957 + 2-PRAZNA-MESECA", "z72/z73-DVOJČKI-'Zwillinge'-pripis-X-POTRJEN" in seg and "z37/z38-PREČRTANI-DVOJNI" in seg and "z91-KRSTEN-PRAZNO-BREZ-botra" in seg and "z30-TOTGEBOREN-Dragoše" in seg and "NEZAKONSKI-×1" in seg and "MODRI-×3-arhivski-pripisi" in seg and "1957-NAJNOVEJŠI-LINIJE" in seg and "JÄNNER-×0-+ JUNI-×0-GRIBLJE" in seg)
check("I8a nalepek-PODZEMELJ-R-1871-1885 + KNJIGA = 15-LET-LINIJA", "PODZEMELJ-R-1871-1885" in seg and "KNJIGA = 15-LET-LINIJA" in seg)
check("I8b P234-LEAD-POTRJEN + LINIJA-15/15-KOMPLETNA", "vs-LEAD-'~90–110'-POTRJENO-1:1" in seg and "LINIJA-15/15-KOMPLETNA" in qa)
check("I9a qa-p235 (235. kontrola!)", "qa-p235" in qa and "235. kontrola" in qa)
pt = open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8").read()
check("I9b pt-luknja-288/2059 (P254!) + byBook-04104", '"vitalsTotal": 2059' in pt and '"04104": 288' in pt)
v234 = open(f"{ROOT}/scripts/p234_parish_baptism_1872_04104.py", encoding="utf-8").read()
check("I9c p234-verifier-sanitizacija (1940→2059-P258!)", '"vitalsTotal": 2059' in v234 and "1923" not in v234)

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
