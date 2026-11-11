#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P249 — verifikator POROČNE PREDZGOVINE 04455, leto 1875 = 11/13 (I1–I10 + I11-meje/foliacija/dueli + --live)."""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "04455",\s*year: 1875,', src)
check("I1 bloki 04455/1875 == 1 (h8-nevesta!)",
      len(bloki) == 1 and bloki == ["8"], f"najdeno {len(bloki)}: {','.join(bloki)}")
skupaj = src.count('bookSignature: "04455"')
check("I2 vitals-2026 + 04455==269", "HOUSE_VITALS.length !== 2011" not in src and skupaj == 269, f"04455={skupaj}")

nove = re.findall(r'houseNo: "8",\s*bookSignature: "04455",\s*year: 1875,\s*scan: (\d+),\s*page: (\d+),', src)
check("I3 sken+pag h8 (9/8 — pag=sken−1!)",
      nove and nove[0] == ("9", "8"), ";".join(f"s{b[0]}/p{b[1]}" for b in nove))

d = json.load(open(f"{ROOT}/research/issue17/parish-marriage-1875-04455.json", encoding="utf-8"))
an = json.dumps(d["anomalie"], ensure_ascii=False)
check("I4 dokaz (18-vpisov = 17+1-violet + 1-Griblje + RESTART-s8-TOP + '21'-ANOMALIJA + finis-1874-4.-instance + DUP-8!)",
      d["stats"]["entries"] == 18 and d["stats"]["gribljeMarriages"] == 1
      and "RESTART-1875 = s8-TOP" in d["frame"]["restart_varianta"]
      and "'21'-FIZIČNO-ANOMALIJA" in d["frame"]["restart_varianta"]
      and "s7→s8" in d["frame"]["meja_1874_75"]
      and "f-i-n-i-s / 1-8-7-4" in d["frame"]["meja_1874_75"]
      and "s10→s11" in d["frame"]["meja_1875_76"]
      and "17-VPISOV-BREZ-PRESKOKOV" in d["frame"]["numbering"]
      and "DUP-8-ŠTEVILČENJA-KOLIZIJA" in d["frame"]["numbering"]
      and "NI-PONOVLJENA-KOT-POSEBNA-NASLOVNA-GLAVA" in d["frame"]["glava_1875"]
      and "4/4-1875" in d["frame"]["foliacija"]
      and "23/23" in d["frame"]["foliacija"]
      and "MNOŽIČNI-POROČNI-DAN-'4. Februar 1875'-×10" in d["frame"]["datum_vzorec"]
      and "11-LET" in d["frame"]["dovgan_11_let"],
      f"entries={d['stats']['entries']} griblje={d['stats']['gribljeMarriages']}")
check("I4b blok-h8 + h42-PARALELA + PEZDIRC-×3 + MLADOLETNICA + najstarejša-46",
      any(b["vpis"] == 10 and "GRIBLJE 8" in b.get("h8", "") for b in d["bloki"])
      and "Maria-Pegdirc-GRIBLJE-42" in an and "h42-PARALELA-1:1" in an
      and "P250" in an
      and "Anna-Pegedire" in an and "Anton-Pegdire" in an and "Georg-Pegdire" in an
      and "MLADOLETNICA-×1" in an and "Mötthling-dd.-9.-Juni-1875" in an
      and "46-l" in an)
an2 = json.dumps(d, ensure_ascii=False)
check("I4c P248-NAPAVED-FALSIFICIRANA + '4.'-×10 + mesec-samo-ob-spremembi + MILEK-v8 + migranti",
      "P248-NAPAVED-preskok-8-FALSIFICIRANA" in an2 and "DUP-8-ŠTEVILČENJA-KOLIZIJA" in an2
      and "'4. Februar 1875'-×10" in an2 and "MESEC-SAMO-OB-SPREMEMBI" in an2
      and "Anna-Milek" in an2 and "MIGRANT" in an2 and "Jatnopir" in an2)

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 2032")
check("I5 qa-p249 + števec-2012 (×150!)", "HOUSE_VITALS.length !== 1996" not in qa and st >= 150, f"2012-številcev={st}")
check("I5b sidra-262 + 1875:1-P249 (qa-sidra-message)", "poročna sidra ≠ 262 (1873:4-P251! · 1874:11-P250! · 1875:1-P249!" in qa)
check("I5c dobe-221 + 51-pred-linijskih", "dobe-bloki ≠ 236/7/26" in qa and "66 pred-linijskih 1873-P251×4!+1874-P250×11!+1875-P249×1!" in qa)
check("I5d p80-1875:1-garda + sken-range-8–10", 'p80MarrAnchors.filter((h) => h.year === 1875).length !== 1' in qa and "skeni izven 8–10" in qa and "skeni izven 7–10" not in qa)

i0 = src.find("P249: POROČNA PREDZGOVINA 04455, leto 1875")
seg = src[i0:] if i0 >= 0 else ""
check("I6a 18-VPISOV + RESTART-s8-TOP + '21'-ANOMALIJA + FALSIFICIRANA + DUP-8",
      "18-VPISOV-BREZ-PRESKOKOV-8.-LETO" in seg and "RESTART-1875 = s8-TOP" in seg
      and "'21'-FIZIČNO-ANOMALIJA" in seg and "P248-NAPAVED-preskok-8-FALSIFICIRANA" in seg
      and "DUP-8-ŠTEVILČENJA-KOLIZIJA" in seg)
check("I6b MNOŽIČNI-DAN-×10 + FINIS-1874-4.-INSTANCE + h42-PARALELA + DOVGAN-11-LET",
      "MNOŽIČNI-POROČNI-DAN-'4. Februar 1875'-×10" in seg
      and "f-i-n-i-s-/-1-8-7-4" in seg and "4.-INSTANCE-ZAKLJUČNE-OZNAKE-LETA" in seg
      and "h42-PARALELA-1:1" in seg and "NAPAVED-P250-PROMOCIJA" in seg
      and "DOVGAN-KONTINUUM-PODALJŠAN-NA-11-LET" in seg)
check("I6c meja-s7→s8 + s10→s11 + foliacija-23/23 + h8-blok-Jatnopir",
      "MEJA-1874/75 = s7→s8" in seg and "MEJA-1875/76 = s10→s11-P248-1:1-RE-VERIFIKACIJA" in seg
      and "FOLIACIJA-'Pag-=-sken−1'-4/4-1875" in seg and "23/23-V-ZAPOREDNIH-LETIH-6.-LETO" in seg
      and "Maria-Jatnopir" in seg and "Anton-Pegdire" in seg)

m = open(f"{ROOT}/src/data/atlas/parish-marriage-early.ts", encoding="utf-8").read()
check("I7a modul-1875 (MARRIAGE_1875_*-izvozi!)", all(x in m for x in [
    "MARRIAGE_1875_BLOCKS", "MARRIAGE_1875_GRIBLJE", "MARRIAGE_1875_HOUSES", "MARRIAGE_1875_TOTAL",
    "MARRIAGE_1875_MEJA", "MARRIAGE_1875_NUMBERING", "FOLIACIJA_1875", "MNOZICNI_DAN_1875",
    "DOVGAN_1875_PODALJŠITEV", "H42_1874_PARALELA", "PEZDIRC_1875_KONTEKST", "MLADOLETNICA_1875",
    "MARRIAGE_1875_DUELS", "MARRIAGE_1875_KONTEKST", "MARRIAGE_1875_KORPUS"]))
check("I7b korpus-1875-v-modulu (254/1997/247/221!)",
      "skupaj04455: 254" in m and "skupajVitals: 1997" in m and "sidra: 247" in m and "dobe: 221" in m)
check("I7c FOLIACIJA-23/23 + DUP-8 + '21'-anomalija + finis-1874-v-modulu",
      "23/23-v-zaporednih-letih" in m and "DUP-8-ŠTEVILČENJA-KOLIZIJA" in m
      and "'21'-FIZIČNO-ANOMALIJA" in m and "f-i-n-i-s-/-1-8-7-4" in m
      and "TOTAL = 18" in m)

pt = json.load(open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8"))
h42 = [x for x in pt["gapHouses"] if x["houseNo"] == "42"][0]
check("I8a pt-luknja-2008 + byBook-04455=265",
      pt.get("vitalsTotal") == 2032 and pt.get("corpus", {}).get("byBook", {}).get("04455") == 269,
      f"vitalsTotal={pt.get('vitalsTotal')} 04455={pt.get('corpus', {}).get('byBook', {}).get('04455')}")
check("I8b h42-p249Note (tail-kandidat-PROMOCIJA-P250!-bloki-16!)",
      h42["blocksTotal"] == 16 and "p249Note" in h42 and "Maria Pegdirc" in h42["p249Note"]
      and "P250" in h42["p249Note"])

ui = open(f"{ROOT}/src/components/museum/museum-atlas.tsx", encoding="utf-8").read()
check("I9 UI-MarriageEarly1875-v-ParishTab + importi + h42-kartica!",
      "MarriageEarly1875" in ui and "H42_1874_PARALELA" in ui
      and "PEZDIRC_1875_KONTEKST" in ui and "FOLIACIJA_1875" in ui and "MNOZICNI_DAN_1875" in ui
      and "MARRIAGE_1875_KONTEKST" in ui and "MARRIAGE_1875_NUMBERING" in ui
      and "DOVGAN_1875_PODALJŠITEV" in ui and "MLADOLETNICA_1875" in ui
      and "Poročna predzgodovina 04455 (P249): leto 1875 = 11/13" in ui)
check("I9b worklog-P249-vnos", "## P249" in open(f"{ROOT}/worklog.md", encoding="utf-8").read())
check("I9c stari-verifikatorji-na-živih-številkah",
      "2008" in open(f"{ROOT}/scripts/p238_parish_marriage_1885_04455.py", encoding="utf-8").read()
      and "265" in open(f"{ROOT}/scripts/p242_parish_marriage_1881_04455.py", encoding="utf-8").read())

# ——— I10: QA-živo ———
try:
    r = urllib.request.Request("http://localhost:3000/api/qa")
    with urllib.request.urlopen(r, timeout=30) as resp:
        qa_data = json.load(resp)
    check("I10 QA-živo ok:True", qa_data.get("ok") is True and qa_data.get("failed") == 0,
          f"passed={qa_data.get('passed')} failed={qa_data.get('failed')}")
except Exception as e:
    check("I10 QA-živo", False, str(e)[:80])

# ——— --live: Matricula-04455 ———
if "--live" in sys.argv:
    try:
        req = urllib.request.Request("https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/",
                                     headers={"User-Agent": "Mozilla/5.0 (p249-verifikator)"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            code = resp.status
        check("I10b LIVE matricula-04455 HTTP 200 (križ-knjiga!)", code == 200, f"status={code}")
    except Exception as e:
        check("I10b LIVE matricula-04455", False, str(e)[:60])

n = sum(1 for _, c, _ in results if c)
print(f"\nP249 verifikator: {n}/{len(results)} {'PASS ✓' if ok else 'FAIL ✗'}")
sys.exit(0 if ok else 1)
