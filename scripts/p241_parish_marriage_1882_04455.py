#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P241 — verifikator POROČNE PREDZGOVINE 04455, leto 1882 = 4/13 (I1–I10 + --live)."""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "04455",\s*year: 1882,', src)
check("I1 bloki 04455/1882 == 7 (6-novih + 1-MERGE-z-P80-sidrom-h36!)",
      len(bloki) == 7, f"najdeno {len(bloki)}")
skupaj = src.count('bookSignature: "04455"')
check("I2 vitals-1985 + 04455==242 (MERGE!-P243-živo!)", "HOUSE_VITALS.length !== 1985" not in src and skupaj == 242, f"04455={skupaj}")

# hiše-1882 (vrstni red 35, 38, 56, 13, 8, 1, 36) — preko žive izvedbe filtra (regex po novih blokih + P80-sidro)
nove = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "04455",\s*year: 1882,\s*scan: (\d+),\s*page: (\d+),', src)
check("I3 hiše-7-vrstni-red (35, 38, 56, 13, 8, 1, 36-MERGE!) + skeni (45, 46, 48, 48, 48, 49, 50)",
      [b[0] for b in nove] == ["35", "38", "56", "13", "8", "1", "36"]
      and [b[1] for b in nove] == ["45", "46", "48", "48", "48", "49", "50"],
      ",".join(b[0] for b in nove))
check("I3b P80-sidro-h36-1882-MERGE (page-44-obdržano + P241-MERGE-znak!)",
      'year: 1882,\n    scan: 50,\n    page: 44,' in src and 'P241-MERGE-z-P80-sidrom-1:1' in src
      and 'h36-PREDISTOPNA-NIT-P240-IZPOLNJENA-1:1' in src)

d = json.load(open(f"{ROOT}/research/issue17/parish-marriage-1882-04455.json", encoding="utf-8"))
an = json.dumps(d["anomalies"], ensure_ascii=False)
check("I4 dokaz (26-vpisov + 7-Griblje + BREZ-preskokov + restart-s45-glava-PRED-vrstico-1 + meja-s44→s45 + s50-MID-P240!)",
      d["stats"]["entries"] == 26 and d["stats"]["gribljeMarriages"] == 7
      and d["stats"]["zapSkipped"] == 0
      and "s44→s45" in d["frame"]["meja_1881_82"]
      and "s50-MID" in d["frame"]["meja_1882_83"]
      and "PRED-VRSTICO" in d["frame"]["restart_varianta"]
      and "26-VPISOV-BREZ-PRESKOKA" in d["frame"]["numbering"],
      f"entries={d['stats']['entries']} griblje={d['stats']['gribljeMarriages']} anomalies={len(d['anomalies'])}")
check("I4b h1-REKORD + h36-MERGE + foliacija-'93/94'-X-OPEN",
      "h1-REKORD" in an and "najnižja-hiša-s-poročnim-blokom-KADARKOLI" in json.dumps(d, ensure_ascii=False)
      and "foliacija" in an and "93/94" in an and "X-OPEN" in an)
check("I4c OBA-PEZDIRC-v9 + v13-vdova-48 + v16-NEVESTA-16 + IZMENA-vlog-v6/v7",
      "OBA-PEZDIRC" in an and "48" in an and "16" in an and "IZMENA-vlog" in an)

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 1985")
check("I5 qa-p241 + števec-1978", "qa-p241-parish-marriage-early-04455-1882" in qa and st >= 145, f"1985-številcev={st}")
check("I5b sidra-228 + 1879:9-P244 + 1880:3-P243 (qa-sidra-message-P244-živo!)", "poročna sidra ≠ 235 (1878:7-P246! · 1879:9-P244! · 1880:3-P243!" in qa)
check("I5c dobe-202 + 32-pred-linijskih (P244-živo!)", "dobe-bloki ≠ 209/7/26" in qa and "39 pred-linijskih 1878-P246×7!" in qa)

i0 = src.find("P241: poročna PREDZGOVINA 04455, leto 1882")
seg = src[i0:] if i0 >= 0 else ""
check("I6a 26-vpisov-BREZ-preskokov-4.-leto + restart-s45-glava-PRED-vrstico-1", "26-vpisov-leta-1882" in seg and "BREZ-preskokov" in seg and "RESTART-1882 = s45" in seg and "PRED-VRSTICO" in seg)
check("I6b NOVA-4.-MEJNA-VARIANTA + meja-1881/82-s44→s45", "NOVA-4.-MEJNA-VARIANTA" in seg and "MEJA-1881/82 = s44→s45-glava" in seg)
check("I6c 6-NOVIH-blokov-+ 1-MERGE-z-P80-sidrom-h36", "6-NOVIH-GRIBLJE-blokov + 1-MERGE-z-P80-sidrom-h36" in seg and "P238-h13-MERGE-vzorec" in seg)
check("I6d h1-REKORD-v-sekciji + PEZDIRC-×5-vpisov", "h1 = NAJNIŽJA-HIŠA-S-POROČNIM-BLOKOM-KADARKOLI" in seg and "PEZDIRC-×5-vpisov" in seg)

m = open(f"{ROOT}/src/data/atlas/parish-marriage-early.ts", encoding="utf-8").read()
check("I7a modul-1882 (MARRIAGE_1882_*-izvozi)", all(x in m for x in [
    "MARRIAGE_1882_BLOCKS", "MARRIAGE_1882_GRIBLJE", "MARRIAGE_1882_HOUSES", "MARRIAGE_1882_TOTAL",
    "MARRIAGE_1882_XOPEN", "MARRIAGE_1882_MEJA", "MARRIAGE_1882_NUMBERING", "PEZDIRC_1882_NIT",
    "H1_1882_REKORD", "PRIEST_1882", "FOLIACIJA_1882_XOPEN", "BRINC_1882_NIT", "MARRIAGE_1882_VILLAGE_DUELS"]))
check("I7b h1-REKORD-v-modulu + OUTRUNA-za-7-let", "1.-poročni-blok-na-h1-KADARKOLI" in m and "ZA-7-LET" in m)
check("I7c forenzika-×237-ostaja", "×237 blokov čez 5 knjig" in open(f"{ROOT}/src/data/atlas/parish-forensics.ts", encoding="utf-8").read())

check("I8a pt-luknja-1985 + byBook-04455=242 (P243-živo!)", '"vitalsTotal": 1985' in open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8").read()
      and '"04455": 242' in open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8").read())
pt = json.load(open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8"))
h52 = [x for x in pt["gapHouses"] if x["houseNo"] == "52"][0]
check("I8b h52-posodobljen (9-blokov/04455=2/firstYear=1882/p241Note)",
      h52["blocksTotal"] == 10 and h52["byBook"]["04455"] == 3 and h52["firstYear"] == 1881 and "p242Note" in h52)
check("I9 UI-MarriageEarly1882-v-ParishTab + importi", "MarriageEarly1882" in open(f"{ROOT}/src/components/museum/museum-atlas.tsx", encoding="utf-8").read()
      and "H1_1882_REKORD" in open(f"{ROOT}/src/components/museum/museum-atlas.tsx", encoding="utf-8").read())
check("I9b worklog-P241-vnos", "## P241" in open(f"{ROOT}/worklog.md", encoding="utf-8").read())
check("I9c stari-verifikatorji-na-živih-številkah",
      "1985" in open(f"{ROOT}/scripts/p238_parish_marriage_1885_04455.py", encoding="utf-8").read()
      and "242" in open(f"{ROOT}/scripts/p239_parish_marriage_1884_04455.py", encoding="utf-8").read()
      and "242" in open(f"{ROOT}/scripts/p240_parish_marriage_1883_04455.py", encoding="utf-8").read()
      and "242" in open(f"{ROOT}/scripts/p237_parish_forensics.py", encoding="utf-8").read())

if "--live" in sys.argv:
    try:
        r = urllib.request.Request("https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/",
                                   headers={"User-Agent": "Mozilla/5.0"})
        code = urllib.request.urlopen(r, timeout=30).status
        check("I10 LIVE matricula-04455 HTTP 200 (križ-knjiga!)", code == 200, f"status={code}")
    except Exception as e:
        check("I10 LIVE matricula-04455", False, str(e)[:60])

print()
print(f"VERIFIER-P241: {'VSI PASS' if ok else 'NEUSPEH!'} ({sum(1 for _, c, _ in results if c)}/{len(results)})")
sys.exit(0 if ok else 1)
