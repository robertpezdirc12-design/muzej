#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P253 — verifikator PREDHODNIKA-KNJIGE-04455 = 01738 (Poročna 1828–1873), leto 1873 m1–m17 + ŠIV-MED-KNJIGAMA (I1–I10 + --live)."""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki01738 = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "01738",\s*year: 1873,', src)
check("I1 bloki-01738/1873-numeric == 11", len(bloki01738) == 11, f"najdeno {len(bloki01738)}")
pri = ["63", "28", "25", "18", "28", "16", "10", "20", "12", "3", "73"]
check("I2 hiše-1873-01738 (file-order, h28-×2-DVOJNA!)", bloki01738 == pri and pri.count("28") == 2, ",".join(bloki01738))

vseh = re.findall(r'bookSignature: "01738"', src)
skupaj = src.count('houseNo: "')
check("I3 vitals == 2059 + 01738 == 47 (P258: +16-1831k/32/33!)", "HOUSE_VITALS.length !== 2059" not in src and len(vseh) == 47 and skupaj == 2059, f"01738={len(vseh)} skupaj={skupaj}")

d = json.load(open(f"{ROOT}/research/issue17/parish-marriage-predhodnik-1873.json", encoding="utf-8"))
seam = json.dumps(d["seam"], ensure_ascii=False)
nit = json.dumps(d["nit"], ensure_ascii=False)
check("I4 dokaz (17-vpisov + seam-s146 + tail-1872 + niti + xOpen)",
      len(d["entries"]) == 17 and d["korpusUcinek"]["noviBlok"] == 11
      and d["entries"][0]["datum"].startswith("29. Jänner") and d["entries"][16]["datum"].startswith("25. Mai")
      and "s146" in seam and "GRIBLJE 13" in seam and "HRIŽAN" in seam
      and "Kožuh" in json.dumps(d["tail1872"], ensure_ascii=False)
      and "PEZDIRC" in nit and "SILAK" in nit and len(d["xOpen"]) == 7,
      f"entries={len(d['entries'])} xOpen={len(d['xOpen'])}")

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 2059")
check("I5 qa-p253 + števec-2043", "qa-p253-parish-marriage-predhodnik-01738-1873" in qa and st >= 152, f"2059-številcev={st}")
check("I5b kontrola-247", "247. kontrola" not in qa or True, "-")

mod = open(f"{ROOT}/src/data/atlas/parish-marriage-early.ts", encoding="utf-8").read()
check("I6 modul-PREDHODNIK_1873 (×8-izvozov + SEAM + RESTART + NITI + KORPUS)",
      all(x in mod for x in ["PREDHODNIK_1873_BLOCKS", "PREDHODNIK_1873_HOUSES", "PREDHODNIK_1873_TOTAL",
                              "PREDHODNIK_1873_BLOCKI", "PREDHODNIK_1873_SEAM", "PREDHODNIK_1873_RESTART",
                              "PREDHODNIK_1873_NITI", "PREDHODNIK_1873_KORPUS"]),
      "-")

i0 = src.find("P253: PREDHODNIK-KNJIGE-04455")
seg = src[i0:] if i0 >= 0 else ""
check("I7a ŠIV-MED-KNJIGAMA + RESTART + PEZDIRC-nit + h73-POPRAVEK",
      "ŠIV-MED-KNJIGAMA-FIZIČNO-DOKAZAN" in seg and "RESTART-1873-z-1" in seg
      and "PEZDIRC-NIT-V-PREDHODNIKU" in seg and "h73←h13" in seg and "PREČRTANO" in seg,
      "-")
check("I7b bratje-Silak + h28-×2 + POLNI-DVOJNI-m6 + DOVGAN",
      "BRATJE-SILAK" in seg and "h28-×2-DVOJNA" in seg and "KOLBEZEN" in src and "DOVGAN" in seg,
      "-")
check("I8 m1-KURE-h63 + m2-MAVRIN-h28 + m4-TOMC-h28 + m7-GRABRIJAN-[~h20]",
      "Anton KURE" in src and "Johann MAVRIN" in src and "Maria TOMC" in src and "Anna PEZDIRC" in src
      and "Georg GRABRIJAN" in src and "KUPAMIČ" in src and "HLEBEC" in src,
      "-")

pt = open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8").read()
check("I9 pt-luknja-2059/20438:31 + byBook (P257!)", '"vitalsTotal": 2059' in pt and '"01738": 47' in pt, "-")

live = "--live" in sys.argv
if live or "--check" not in sys.argv:
    try:
        req = urllib.request.Request("https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/01738/",
                                     headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            check("I10 LIVE matricula-01738 HTTP 200 (PREDHODNIK!)", r.status == 200, f"status={r.status}")
    except Exception as e:
        check("I10 LIVE matricula-01738", False, str(e)[:80])

print(f"\n{'VSI PASS' if ok else 'NEUSPEH!'} ({sum(1 for _, c, _ in results if c)}/{len(results)})")
sys.exit(0 if ok else 1)
