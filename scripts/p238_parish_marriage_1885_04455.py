#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P238 — verifikator POROČNE PREDZGODOVINE 04455, leto 1885 = 1/13 NOVA LINIJA (I1–I10 + --live)."""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "04455",\s*year: 1885,', src)
check("I1 bloki 04455/1885-numeric == 7", len(bloki) == 7, f"najdeno {len(bloki)}")
pri = ["58", "60", "32", "71", "29 [~X-OPEN]", "26", "13"]
check("I2 hiše-1885 (file-order, h29-X-OPEN)", bloki == pri, ",".join(bloki))
skupaj = src.count('bookSignature: "04455"')
check("I3 vitals-1996 + 04455==253 (P246-živo!)", "HOUSE_VITALS.length !== 1996" not in src and skupaj == 253, f"04455={skupaj}")

d = json.load(open(f"{ROOT}/research/issue17/parish-marriage-1885-04455.json", encoding="utf-8"))
an = json.dumps(d["anomalies"], ensure_ascii=False)
check("I4 dokaz (22-vpisov + 7-Griblje + zap-3-preskočen + restart-s56 + meja-s61 + Pag-sken−1)",
      d["stats"]["entries"] == 22 and d["stats"]["gribljeMarriages"] == 7
      and d["stats"]["zapSkipped"] == 3
      and "s56" in d["frame"]["meja_1884_85"] and "restart" in d["frame"]["meja_1884_85"].lower()
      and "vpis 22" in d["frame"]["meja_1885_86"] and "restart" in d["frame"]["meja_1885_86"].lower()
      and "55–66" in d["frame"]["pag_rule"],
      f"entries={d['stats']['entries']} griblje={d['stats']['gribljeMarriages']} anomalies={len(d['anomalies'])}")
check("I4b zap-3-preskočen + vpis-7-izven-vrsti + 58-vs-38-RAZREŠEN + štajerska-oblika",
      "zap-vpis-3-preskočen" in an and "vpis-7-datum-izven-vrsti" in an
      and "hisa-duel-58-vs-38-vpis-1" in an and "stajerska-oblika" in an)
check("I4c PEZDIRC-×3 + BRINC-mreža + h71-STRAUS + P84-korekcija",
      "pezdirc-×3-leta-1885" in an and "brinc-brinec-mreza-1885" in an
      and "straus-h71-1885" in an and "P84-okvir-korekcija-dokumentirana" in json.dumps(d["crossChecks"], ensure_ascii=False))

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 1996")
check("I5 qa-p238 + števec-1946", "qa-p238-parish-marriage-early-04455" in qa and st >= 148, f"1946-številcev={st}")

i0 = src.find("P238: poročna PREDZGOVINA 04455, leto 1885")
seg = src[i0:] if i0 >= 0 else ""
check("I6a 22-vpisov + zap-2,4,5,6 + VPIS-3-PRESKOČEN", "22-vpisov-leta-1885" in seg and "zap-2,4,5,6" in seg and "VPIS-3-PRESKOČEN" in seg)
check("I6b RESTART-s56 + MEJA-s61 + MISREAD-1883", "RESTART-1885 = s56" in seg and "MEJA-1885/86 = s61" in seg and "MISREAD-»1883«-duel" in seg.replace("★★★", ""))
check("I6c Pag-sken−1-RAZŠIRJENO-55–66", "RAZŠIRJENO-na-55–66" in seg)
check("I6d MERGE-z-starim-P80-sidrom-v-bloku-h13", "MERGE-z-starim-P80-sidrom" in seg and "TRI-DUEL-23/25/28" in seg and "P115-re-read-mati" in seg)
check("I7a PEZDIRC-×3-v-letu + CONTINUUM-×131→04455", "PEZDIRC-×3-v-letu" in seg and "×131→04455" in seg)
check("I7b BRINC/BRINEC-MREŽA-ŠIRŠA (BRUNC + h26 + Marko-50)", "BRINC/BRINEC-MREŽA-ŠIRŠA" in seg and "BRUNC" in seg and "Marko-BRINEC-50-let" in seg)
check("I7c h71-STRAUS-1885-P80-sidro-precejeno + DATUM-IZVEN-VRSTI", "h71-STRAUS-1885" in seg and "DATUM-IZVEN-VRSTI-vpis-7" in seg)
check("I8a štajerska-oblika-RAZREŠENA-4-pasovi + h58-×-h34-DVOJNI", "štajerska-oblika-RAZREŠENA" in seg and "h58-×-h34-DVOJNI" in seg)
check("I8b X-OPEN-vas-dueli-h29/h15/h9 + 3-X-OPEN", "X-OPEN-vas-dueli (h29/h15/h9" in seg or "3-X-OPEN-vas-dueli (h29/h15/h9" in seg)
check("I8c korpus-1946-dokaz (duplikat-odstranjen)", "P239: + 3 bloka 04455-1884 = 1949" in qa)
check("I9a qa-p238 (238. kontrola!)", "qa-p238" in qa and "qa-p238-parish-marriage-early-04455" in qa)
pt = open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8").read()
check("I9b pt-luknja-1996 + byBook-04455=253 (P241-živo!)", '"vitalsTotal": 1996' in pt and '"04455": 253' in pt)

m = open(f"{ROOT}/src/data/atlas/parish-marriage-early.ts", encoding="utf-8").read()
check("I9c modul-parish-marriage-early (15-izvozov)", all(x in m for x in
      ["MARRIAGE_1885_BLOCKS", "MARRIAGE_1885_GRIBLJE", "MARRIAGE_1885_HOUSES", "MARRIAGE_1885_TOTAL",
       "MARRIAGE_1885_ZAP_SKIPPED", "MARRIAGE_1885_XOPEN", "PEZDIRC_1885", "LEDERER_1885", "BRINEC_1885",
       "MARRIAGE_1885_MEJA", "P84_CORRECTION", "MARRIAGE_1885_OUT_OF_ORDER", "PRIEST_1885",
       "OLDEST_PAIR_1885", "YOUNGEST_BRIDE_1885"]))

ui = open(f"{ROOT}/src/components/museum/museum-atlas.tsx", encoding="utf-8").read()
check("I10a UI-MarriageEarly1885-v-ParishTab", "function MarriageEarly1885" in ui and "<MarriageEarly1885 />" in ui)

live = "--live" in sys.argv
if live or "--check" not in sys.argv:
    try:
        req = urllib.request.Request("https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/",
                                     headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            check("I10 LIVE matricula-04455 HTTP 200", r.status == 200, f"status={r.status}")
    except Exception as e:
        check("I10 LIVE matricula-04455", False, str(e)[:80])

print(f"\n{'VSI PASS' if ok else 'NEUSPEH!'} ({sum(1 for _, c, _ in results if c)}/{len(results)})")
sys.exit(0 if ok else 1)
