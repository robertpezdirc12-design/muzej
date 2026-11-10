#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P243 — verifikator POROČNE PREDZGOVINE 04455, leto 1880 = 6/13 (I1–I10 + --live)."""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "04455",\s*year: 1880,', src)
check("I1 bloki 04455/1880 == 3 (h24+h63+h53 — vsi ženi n!)",
      len(bloki) == 3, f"najdeno {len(bloki)}: {','.join(bloki)}")
check("I1b vrstni-red-3 (24,63,53!)", bloki == ["24", "63", "53"], ",".join(bloki))
skupaj = src.count('bookSignature: "04455"')
check("I2 vitals-1990 + 04455==247", "HOUSE_VITALS.length !== 1990" not in src and skupaj == 247, f"04455={skupaj}")

nove = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "04455",\s*year: 1880,\s*scan: (\d+),\s*page: (\d+),', src)
check("I3 skeni+pagi (36/35 · 37/36 · 38/37 — pag=sken−1!)",
      [b[1] for b in nove] == ["36", "37", "38"]
      and [b[2] for b in nove] == ["35", "36", "37"],
      ";".join(f"s{b[1]}/p{b[2]}" for b in nove))

d = json.load(open(f"{ROOT}/research/issue17/parish-marriage-1880-04455.json", encoding="utf-8"))
an = json.dumps(d["anomalie"], ensure_ascii=False)
check("I4 dokaz (20-vpisov + 3-Griblje + restart-s35-DNO-NOVA-7.-VARIANTA + finis-s38 + meja-s38→s39-P242!)",
      d["stats"]["entries"] == 20 and d["stats"]["gribljeMarriages"] == 3
      and "NOVA-7.-MEJNA-VARIANTA" in d["frame"]["restart_varianta"]
      and "s35-DNO" in d["frame"]["restart_varianta"]
      and "finis / s 1880" in d["frame"]["finis"]
      and "s38→s39" in d["frame"]["meja_1880_81"],
      f"entries={d['stats']['entries']} griblje={d['stats']['gribljeMarriages']}")
check("I4b h53-DVIG-1890→1880 + Gaveldzettel + h63-KRIŽAN + BRINE",
      "h53-firstYear-04455-1890→1880-DVIG-ZA-10-LET" in an and "Gaveldzettel" in an
      and "h63-KRIŽAN-continuum" in an and "Mathias-BRINE" in an)
check("I4c PEZDIRC-continuum-×3-reads + GRIBLJAN-izvor-×2 + foliacija-X-OPEN-DUEL",
      "PEZDIRC-CONTINUUM" in an and "GRIBLJAN-IZVOR-pripise-×2" in an
      and "X-OPEN-DUEL" in d["frame"]["foliacija"])

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 1990")
check("I5 qa-p243 + števec-1978 (×152!)", "qa-p243-parish-marriage-early-04455-1880" in qa and st >= 152, f"1990-številcev={st}")
check("I5b sidra-235 + 1878:7-P246 + 1879:9-P244 + 1880:3-P243 (qa-sidra-message)", "poročna sidra ≠ 240 (1877:5-P247! · 1878:7-P246! · 1879:9-P244! · 1880:3-P243!" in qa)
check("I5c dobe-202 + 32-pred-linijskih", "dobe-bloki ≠ 214/7/26" in qa and "44 pred-linijskih 1877-P247×5!" in qa)
check("I5d p80-1880:3-garda + sken-range-35–38", 'p80MarrAnchors.filter((h) => h.year === 1880).length !== 3' in qa and "skeni izven 35–38" in qa)

i0 = src.find("P243: POROČNA PREDZGOVINA 04455, leto 1880")
seg = src[i0:] if i0 >= 0 else ""
check("I6a 20-VPISOV-BREZ-PRESKOKOV + RESTART-s35-DNO-NOVA-7.-VARIANTA", "RESTART-1880 = s35-DNO" in seg and "NOVA-7.-MEJNA-VARIANTA" in seg and "20 VPISOV-BREZ-PRESKOKOV" in seg)
check("I6b meja-1879/80-s35-mid + meja-1880/81-s38→s39-finis", "MEJA-1879/80 = s35-mid" in seg and "MEJA-1880/81 = s38→s39" in seg and "finis/s-1880" in seg)
check("I6c 3-GRIBLJE-bloki + h53-DVIG + Gaveldzettel", "3-GRIBLJE-bloki" in seg and "h53-firstYear-04455-1890→1880-DVIG-ZA-10-LET" in seg and "Gaveldzettel-der-Gemeinde-Griblje" in seg)
check("I6d PEZDIRC-continuum + GRIBLJAN-izvor-×2 + Dovgan-6-let", "PEZDIRC-continuum-×3-reads" in seg and "GRIBLJAN-IZVOR-pripise-×2" in seg and "Dovgan/Dovžan-[~Dorgano]-continuum-6-let" in seg)

m = open(f"{ROOT}/src/data/atlas/parish-marriage-early.ts", encoding="utf-8").read()
check("I7a modul-1880 (MARRIAGE_1880_*-izvozi)", all(x in m for x in [
    "MARRIAGE_1880_BLOCKS", "MARRIAGE_1880_GRIBLJE", "MARRIAGE_1880_HOUSES", "MARRIAGE_1880_TOTAL",
    "MARRIAGE_1880_MEJA", "MARRIAGE_1880_NUMBERING", "H53_1880_DVIG", "KRIZAN_1880_NIT",
    "BRINC_1880_NIT", "GRIBLJAN_1880_IZVOR", "FOLIACIJA_1880_XOPEN", "PRIEST_1880",
    "MARRIAGE_1880_DUELS", "MARRIAGE_1880_KORPUS"]))
check("I7b h53-DVIG-v-modulu + ZA-10-LET + OUTRUNA-ZA-7-LET", "1890→1880" in m and "DVIG-ZA-10-LET" in m and "OUTRUNA-krstno-na-h53-ZA-7-LET" in m)
check("I7c finis-v-modulu", "finis / s 1880" in m)

pt = json.load(open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8"))
check("I8a pt-luknja-1990 + byBook-04455=247", pt.get("vitalsTotal") == 1990 and pt.get("corpus", {}).get("byBook", {}).get("04455") == 247,
      f"vitalsTotal={pt.get('vitalsTotal')} 04455={pt.get('corpus', {}).get('byBook', {}).get('04455')}")
h53 = [x for x in pt["gapHouses"] if x["houseNo"] == "53"][0]
check("I8b h53-posodobljen (22-blokov/04455=4/firstYear=1880/p243Note!)",
      h53["blocksTotal"] == 22 and h53["byBook"]["04455"] == 4 and h53["firstYear"] == 1880 and "p243Note" in h53)
check("I9 UI-MarriageEarly1880-v-ParishTab + importi", "MarriageEarly1880" in open(f"{ROOT}/src/components/museum/museum-atlas.tsx", encoding="utf-8").read()
      and "H53_1880_DVIG" in open(f"{ROOT}/src/components/museum/museum-atlas.tsx", encoding="utf-8").read()
      and "Gaveldzettel" in open(f"{ROOT}/src/components/museum/museum-atlas.tsx", encoding="utf-8").read())
check("I9b worklog-P243-vnos", "## P243" in open(f"{ROOT}/worklog.md", encoding="utf-8").read())
check("I9c stari-verifikatorji-na-živih-številkah",
      "1990" in open(f"{ROOT}/scripts/p238_parish_marriage_1885_04455.py", encoding="utf-8").read()
      and "235" in open(f"{ROOT}/scripts/p242_parish_marriage_1881_04455.py", encoding="utf-8").read())

# ——— I10: QA-živo ———
try:
    r = urllib.request.Request(f"{ROOT.replace('/home/z/my-project', 'http://localhost:3000')}/api/qa")
    with urllib.request.urlopen(r, timeout=30) as resp:
        qa_data = json.load(resp)
    check("I10 QA-živo 245/245 ok:True (+qa-p243-id!)",
          qa_data.get("ok") is True and qa_data.get("passed") == 245 and qa_data.get("failed") == 0,
          f"passed={qa_data.get('passed')} failed={qa_data.get('failed')}")
except Exception as e:
    check("I10 QA-živo", False, str(e)[:80])

# ——— --live: Matricula-04455 ———
if "--live" in sys.argv:
    try:
        req = urllib.request.Request("https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/",
                                     headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            code = r.status
        check("I10b LIVE matricula-04455 HTTP 200 (križ-knjiga!)", code == 200, f"status={code}")
    except Exception as e:
        check("I10b LIVE matricula-04455", False, str(e)[:60])

f = sum(1 for _, c, _ in results if not c)
print(f"\n{'='*56}\nP243 VERIFIKATOR: {len(results)-f}/{len(results)} PASS" + (" — VSI OK ✓" if f == 0 else f" — {f} FAIL!"))
sys.exit(0 if f == 0 else 1)
