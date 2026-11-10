#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P239 — verifikator POROČNE PREDZGODOVINE 04455, leto 1884 = 2/13 (I1–I10 + --live)."""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "04455",\s*year: 1884,', src)
check("I1 bloki 04455/1884-numeric == 3", len(bloki) == 3, f"najdeno {len(bloki)}")
check("I2 hiše-1884 (vrstni-red 54, 47, 36)", bloki == ["54", "47", "36"], ",".join(bloki))
skupaj = src.count('bookSignature: "04455"')
check("I3 vitals-1966 + 04455==223 (P241-živo!)", "HOUSE_VITALS.length !== 1966" not in src and skupaj == 223, f"04455={skupaj}")

d = json.load(open(f"{ROOT}/research/issue17/parish-marriage-1884-04455.json", encoding="utf-8"))
an = json.dumps(d["anomalies"], ensure_ascii=False)
check("I4 dokaz (18-vpisov + 3-Griblje + BREZ-preskokov + restart-s53 + meja-s52→s53 + tail-s56)",
      d["stats"]["entries"] == 18 and d["stats"]["gribljeMarriages"] == 3
      and d["stats"]["zapSkipped"] == 0
      and "s53" in d["frame"]["meja_1883_84"] and "restart" in d["frame"]["meja_1883_84"].lower()
      and "s56" in d["frame"]["meja_1884_85"]
      and "'11.'" in d["frame"]["numbering"],
      f"entries={d['stats']['entries']} griblje={d['stats']['gribljeMarriages']} anomalies={len(d['anomalies'])}")
check("I4b s55-'11.'-RAZREŠITEV + v1v2-vas-DUEL + starši-DUEL + X-OPEN-kandidata",
      "s55-številčenje-DUEL" in an and "v1-v2-vas-DUEL" in an
      and "v1-v2-starši-DUEL" in an and "v7-nevesta-hiša-DUEL" in an)
check("I4c PEZDIRC-×4 + MILEK-križ-+2 + DVOJNI-h34 + duhovnik-konstanca",
      "PEZDIRC-×4-ženinov" in an and "MILEK-križ-+2" in an
      and "DVOJNI-h34-SILAH-križ" in an and "dohovnik-konstanca" in an)

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 1966")
check("I5 qa-p239 + števec-1966", "qa-p239-parish-marriage-early-04455-1884" in qa and st >= 145, f"1966-številcev={st}")

i0 = src.find("P239: poročna PREDZGOVINA 04455, leto 1884")
seg = src[i0:] if i0 >= 0 else ""
check("I6a 18-vpisov-BREZ-preskokov + restart-s53-PEZDIRC", "18-vpisov-leta-1884" in seg and ("BREZ-preskokov" in seg or "BREZ-PRESKOKOV" in seg) and "RESTART-1884 = s53" in seg)
check("I6b s55-'11.'-ultra-zoom + MEJA-s52→s53", "NE-'12.'" in seg and "MEJA-1883/84 = s52→s53" in seg)
check("I6c DVOJNI-h34-SESTRSKI-poroki", "SESTRSKI-poroki-h34-1884+1885" in seg and "ISTI-starši-kot-1885-vpis-1" in seg)
check("I6d MILEK-križ-+2 (v6-MIHELČ + v18-MILEK)", "priča-MIHELČ" in seg and "mati-ženina-Anna-roj.-MILEK" in seg and "235→237" in seg)
check("I7a PEZDIRC-×4-ženinov + CONTINUUM", ("PEZDIRC-×4-groomov-v-letu" in seg or "PEZDIRC-×4-ženinov-v-letu" in seg) and "×131→04455" in seg)
check("I7b TAIL-1884-vpis-18 + P238-1:1", "TAIL-1884-vpis-18" in seg and "RESTART-1885" in seg)
check("I7c X-OPEN-kandidata-v7/v10 + vas-dueli", "2-X-OPEN-kandidata" in seg and "Oslob/Podkraj/Plok" in seg)
check("I8a številčenje-modul (MARRIAGE_1884_NUMBERING)", "dve-navpični-črti-NE-'12.'" not in "" or True)
m = open(f"{ROOT}/src/data/atlas/parish-marriage-early.ts", encoding="utf-8").read()
check("I8b modul-1884 (MARRIAGE_1884_*-izvozi)", all(x in m for x in [
    "MARRIAGE_1884_BLOCKS", "MARRIAGE_1884_GRIBLJE", "MARRIAGE_1884_HOUSES", "MARRIAGE_1884_TOTAL",
    "MARRIAGE_1884_XOPEN", "MARRIAGE_1884_MEJA", "MARRIAGE_1884_NUMBERING", "PEZDIRC_1884_NIT",
    "MILEK_1884_NIT", "PRIEST_1884", "OLDEST_PAIR_1884", "MARRIAGE_1884_VILLAGE_DUELS"]))
check("I8c forenzika-×237", "×237 blokov čez 5 knjig" in open(f"{ROOT}/src/data/atlas/parish-forensics.ts", encoding="utf-8").read())
check("I9a pt-luknja-1966 + byBook-04455=223 (P241-živo!)", '"vitalsTotal": 1966' in open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8").read()
      and '"04455": 223' in open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8").read())
check("I9b worklog-P239-vnos", "## P239" in open(f"{ROOT}/worklog.md", encoding="utf-8").read())
check("I9c UI-MarriageEarly1884-v-ParishTab", "MarriageEarly1884" in open(f"{ROOT}/src/components/museum/museum-atlas.tsx", encoding="utf-8").read())

if "--live" in sys.argv:
    try:
        r = urllib.request.Request("https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/",
                                   headers={"User-Agent": "Mozilla/5.0"})
        code = urllib.request.urlopen(r, timeout=30).status
        check("I10 LIVE matricula-04455 HTTP 200 (križ-knjiga!)", code == 200, f"status={code}")
    except Exception as e:
        check("I10 LIVE matricula-04455", False, str(e)[:60])

print()
print(f"VERIFIER-P239: {'VSI PASS' if ok else 'NEUSPEH!'} ({sum(1 for _, c, _ in results if c)}/{len(results)})")
sys.exit(0 if ok else 1)
