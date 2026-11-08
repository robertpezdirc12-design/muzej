#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P219 — verifikator MRLIŠKE PREDZGODOVINE 04106, leto 1858 (predzgodovina-28/29). I1–I10 + --live."""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'\{\s*houseNo:\s*"(\d+)",\s*bookSignature:\s*"04106",\s*year:\s*1858,', src)
check("I1 bloki 04106/1858-numeric == 10", len(bloki) == 10, f"najdeno {len(bloki)}")
pri = ["49", "19", "19", "19", "60", "65", "3", "2", "44", "50"]
check("I2 hiše-1858-numeric (file-order)", bloki == pri, ",".join(bloki))
skupaj = src.count('bookSignature: "04106"')
check("I3 vitals-1759 + 04106==433", "HOUSE_VITALS.length !== 1759" not in src and skupaj == 433, f"04106={skupaj}")

d = json.load(open(f"{ROOT}/research/issue17/parish-death-1858-04106.json", encoding="utf-8"))
grib = [e for e in d["entries"] if "gribl" in str(e.get("vas", "")).lower() and "grem" not in str(e.get("vas", "")).lower()]
an = json.dumps(d["anomalije"], ensure_ascii=False)
check("I4 dokaz (58/10-griblje + meja-s7-1857/58 + 57-written + vsotna-'1 8 [5 8]' + NEŠTEVILČENA)",
      len(d["entries"]) == 58 and len(grib) == 10
      and "s7" in d["okvir"]["meja_1857_58"] and "1 8 [5 8]" in d["okvir"]["meja_1857_58"]
      and d["statistika"]["vpisov_1858_kronolosko"] == 58 and d["statistika"]["vpisov_written"] == 57,
      f"entries={len(d['entries'])} griblje={len(grib)} anomalije={len(d['anomalije'])}")
check("I4b nesteviceena-s7 + naslovna-lista-×3 + dvojcki-simic + gaufigalbrann",
      "nesteviceena-s7-zadnja" in an and "naslovna-lista-×3-sredi-leta" in an and "dvojcki-simic-h19" in an and "gaufigalbrann-klaster-×4" in an)
check("I4c pezdirc-mreza-padire + nov-duhovnik-auber-duel + starost-0-dueli",
      "pezdirc-mreza-padire" in an and "nov-duhovnik-auber-duel" in an and "starost-0-dueli" in an)

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 1759")
check("I5 qa-p219 + števec-1642", "qa-p219-parish-death-1858-04106" in qa and st >= 126, f"1759-številcev={st}")

i0 = src.find("P219: mrliška PREDZGODOVINA 04106, leto 1858")
seg = src[i0:] if i0 >= 0 else ""
check("I6a 58-VPIISOV-ŠTEVJE-IZ-VRSTIC-21.× + NEŠTEVILČENA-s7", "58 vpisov" in seg and "ŠTEVJE-IZ-VRSTIC-21.×" in seg and "NEŠTEVILČENA" in seg)
check("I6b ČISTA-ORDINALNA-LINIJA-1–57 + NASLOVNA-LISTA-s9+s10", "ČISTA-ORDINALNA-LINIJA" in seg and "NASLOVNA-LISTA-s9+s10" in seg and "30–33" in seg)
check("I6c DVOJČKI-SIMIC-h19 (ZWILLINGE!)", "DVOJČKI-SIMIC-h19" in seg and "ZWILLINGE" in seg)
check("I7a MEJA-s7 (VSOTNA-'1 8 [5 8]'-P214-TIP-3.-INSTANCE + 57.-POTRDITEV!)", "MEJA-1857/58-s7" in seg and "1 8 [5 8]" in seg and "57.-POTRDITEV" in seg)
check("I7b GAUFIGALBRANN-KLASTER-×4 + FRAISEN-nit", "GAUFIGALBRANN" in seg and "×4" in seg and "FRAISEN-nit" in seg)
check("I7c NOV-DUHOVNIK-DUEL-'Auber' + KOREKCIJA-P218-Knavs-ŽE-Feb-1858", "NOV-DUHOVNIK-DUEL-'J.-Auber[?]/Huber[?]-P.'" in seg and "KOREKCIJA-P218: Knavs-ŽE-Feb-1858" in seg)
check("I8a PEZDIRC-MREŽA-NAJGLABLJE-'Padire'-h50-4-GENERACIJE", "PEZDIRC-MREŽA-NAJGLABLJE-'Padire'-h50" in seg and "4-GENERACIJSKA-GRAFIJA-LINIJA" in seg)
check("I8b h19-×3-TRIPLE (edina-×3-v-predzgodovini!)", "h19-×3-TRIPLE" in seg and "edina-×3-v-predzgodovini" in seg)
check("I8c otroška-umrljivost-50%-5/10 + ekstremi-0[?]-→-68-J[?]", "otroška-umrljivost-50%-5/10" in seg and "0[?]-→-68-J[?]" in seg)
check("I8d foliacija-svinčnik-sken−1-dokumentirana + pag-konvencija", "svinčnik-foliacija-arhivarja = sken−1" in seg and "sken−5-KORPUS-KONVENCIJA" in seg)
check("I9a qa-p219 (219. kontrola!)", "qa-p219" in qa and "219. kontrola" in qa)
pt = open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8").read()
check("I9b pt-luknja-423/1642", '"vitalsTotal": 1759' in pt and '"04106": 433' in pt)

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
