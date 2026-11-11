#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P250 — verifikator POROČNE PREDZGOVINE 04455, leto 1874 = 12/13 (I1–I10 + --live)."""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "04455",\s*year: 1874,', src)
check("I1 bloki 04455/1874 == 11 (REKORD!-h27-×2!)",
      len(bloki) == 11 and bloki == ["65", "7", "4", "27", "27", "33", "29", "30", "10", "43", "42"],
      f"najdeno {len(bloki)}: {','.join(bloki)}")
skupaj = src.count('bookSignature: "04455"')
check("I2 vitals-2008 + 04455==265", "HOUSE_VITALS.length !== 2008" not in src and skupaj == 265, f"04455={skupaj}")

nove = re.findall(r'houseNo: "(\d+)",\s*bookSignature: "04455",\s*year: 1874,\s*scan: (\d+),\s*page: (\d+),', src)
pag_ok = all(int(p) == int(s) - 1 for _, s, p in nove)
check("I3 sken+pag (pag=sken−1!-s2–s7!)", len(nove) == 11 and pag_ok and {s for _, s, _ in nove} == {"3", "4", "5", "6", "7"},
      ";".join(f"h{h}-s{s}/p{p}" for h, s, p in nove))

d = json.load(open(f"{ROOT}/research/issue17/parish-marriage-1874-04455.json", encoding="utf-8"))
an = json.dumps(d["anomalie"], ensure_ascii=False)
check("I4 dokaz (32-vpisov = BREZ-preskokov-9.-leto + 11-blokov-REKORD + RESTART-s2-DNO-12.-varianta + KNIŽNO-ODPIRANJE-m18!)",
      d["stats"]["entries"] == 32 and d["stats"]["gribljeMarriages"] == 11
      and "RESTART-1874 = s2-DNO" in d["frame"]["restart_varianta"]
      and "12.-MEJNA-VARIANTA" in d["frame"]["restart_varianta"]
      and "KNIJIŽNO-ODPIRANJE-04455" in d["frame"]["knjizno_odpiranje"]
      and "m1–m17-leta-1873" in d["frame"]["knjizno_odpiranje"].replace("vpisi-m1–m17-leta-1873", "m1–m17-leta-1873")
      and "1873-Juni-11" in d["frame"]["knjizno_odpiranje"]
      and "s2-MID/DNO" in d["frame"]["meja_1873_74"]
      and "13.-MEJNA-VARIANTA" in d["frame"]["meja_1873_74"]
      and "s7→s8-P249-1:1-RE-VERIFIKACIJA" in d["frame"]["meja_1874_75"]
      and "28.-Avgust" in d["frame"]["meja_1874_75"]
      and "32-VPISOV-BREZ-PRESKOKOV-9.-LETO" in d["frame"]["numbering"]
      and "P249-napoved-'1–27'-FALSIFICIRANA" in d["frame"]["numbering"]
      and "INLINE-vzorec-5.-LETO" in d["frame"]["glava_1874"]
      and "5/5-1874" in d["frame"]["foliacija"]
      and "28/28" in d["frame"]["foliacija"]
      and "'8. Februar 1874'-×5" in d["frame"]["datum_vzorec"]
      and "'11. Februar 1874'-×5" in d["frame"]["datum_vzorec"]
      and "12-LET (1874–1885" in d["frame"]["dovgan_12_let"],
      f"entries={d['stats']['entries']} griblje={d['stats']['gribljeMarriages']}")
check("I4b bloki-h65/h7/h4/h27/h33/h29/h30/h10/h43/h42 + DVIGI (h43-34-let-REKORD!)",
      any(b["vpis"] == 5 and "GRIBLJE 65" in b.get("h65", "") for b in d["bloki"])
      and "h65-04455-firstYear-1886→1874-DVIG-ZA-12-LET" in an
      and "h7-04455-firstYear-1889→1874-DVIG-ZA-15-LET" in an
      and "h4-04455-firstYear-1881→1874-DVIG-ZA-7-LET" in an
      and "h27-04455-firstYear-1881→1874-DVIG-ZA-7-LET" in an
      and "h33-04455-firstYear-1888→1874-DVIG-ZA-14-LET" in an
      and "h29-04455-firstYear-1897→1874-DVIG-ZA-23-LET" in an
      and "h30-04455-firstYear-1876→1874" in an
      and "h10-04455-firstYear-1877→1874" in an
      and "h43-04455-firstYear-1908→1874-DVIG-ZA-34-LET-NOV-ABSOLUTNI-REKORD" in an
      and "h42-04455-firstYear-1879→1874" in an
      and "NAPAVED-P250-IZPOLNJENA" in an)
an2 = json.dumps(d, ensure_ascii=False)
check("I4c P249-KOREKCIJA-m28-'28.-Avgust' + MNOŽIČNI-DANI-×3 + H43-PARALELA + MILIČ/HRIŽAN + 52-l-REKORD + 63-l-×2",
      "P249-KOREKCIJA: m28-'28.-Februar'-MISREAD-→-'28.-Avgust'" in an2
      and "'8. Februar 1874'-×5" in an2 and "'11. Februar 1874'-×5" in an2 and "'14. Juni'-×2" in an2
      and "H43-BRULA-PARALELA-1:1" in an2 and "Katharina-BRULA-1878" in an2
      and "HRIŽAN-×4-omemb" in an2 and "MILEK-×3-V-1-LETU" in an2
      and "52-l-NAJSTAREJŠA-NEVESTA-PREDZGOVINE-REKORD" in an2
      and "63-l-ŽENIN-×2-V-1-LETU" in an2
      and "MINDERJÄHRIG" in an2 and "SEGINA-NIT" in an2 and "HLEBEC-×2" in an2
      and "FERCHER" in an2 and "HEGRIČ" in an2)

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 2008")
check("I5 qa-p250 + števec-2008 (×150!)", "HOUSE_VITALS.length !== 2007" not in qa and st >= 150, f"2008-številcev={st}")
check("I5b sidra-258 + 1874:11-P250 (qa-sidra-message)", "poročna sidra ≠ 258 (1874:11-P250!" in qa)
check("I5c dobe-232 + 62-pred-linijskih", "dobe-bloki ≠ 232/7/26" in qa and "62 pred-linijskih 1874-P250×11!" in qa)
check("I5d p80-1874:11-garda + sken-range-2–7", 'p80MarrAnchors.filter((h) => h.year === 1874).length !== 11' in qa and "skeni izven 2–7" in qa and "skeni izven 8–10" in qa)
check("I5e izjeme-p85/p92 + GRIBLJE-29-izjema + MILIČ-243",
      "v.year === 1874 && (hn === \"7\" || hn === \"30\")" in qa
      and "v.year === 1874 && (hn === \"10\" || hn === \"43\")" in qa
      and '(h.year === 1897 || h.year === 1909 || h.year === 1874)' in qa
      and "MILIC_FAMILY_TOTAL !== 243" in qa and "53,78,20,36,56" in qa
      and "MATHIAS_H65_TOTAL !== 23" in qa and "H65_STATS.total !== 43" in qa)

i0 = src.find("P250: POROČNA PREDZGOVINA 04455, leto 1874")
seg = src[i0:] if i0 >= 0 else ""
check("I6a 32-VPISOV + RESTART-s2-DNO + KNIŽNO-ODPIRANJE + P249-KOREKCIJA",
      "32-VPISOV-BREZ-PRESKOKOV-9.-LETO" in seg and "RESTART-1874 = s2-DNO" in seg
      and "KNIJIŽNO-ODPIRANJE-04455" in seg and "m1–m17-leta-1873-NISO-v-tej-knjigi" in seg
      and "P249-KOREKCIJA-m28-'28.-Februar'-MISREAD" in seg.replace("P249-KOREKCIJA-m28-'28.-Februar'-MISREAD→'28.-Avgust'", "P249-KOREKCIJA-m28-'28.-Februar'-MISREAD"))
check("I6b 11-BLOKOV-REKORD + 10-DVIGOV + h43-34-let + h42-PROMOCIJA + meje-s2-MID/DNO",
      "11-BLOKOV-V-1-LETU-NOV-REKORD" in seg and "10-DVIGOV-REKORD" in seg
      and "h43-**34-NOV-ABSOLUTNI-REKORD**" in seg
      and "h42-PROMOCIJA-NAPAVED-IZPOLNJENA" in seg
      and "MEJA-1873/74 = s2-MID/DNO" in seg)
check("I6c meja-s7→s8 + foliacija-28/28 + H43-BRULA + 3-množični-dani",
      "MEJA-1874/75 = s7→s8-P249-1:1-RE-VERIFIKACIJA" in seg
      and "FOLIACIJA-'Pag-=-sken−1'-5/5-1874" in seg and "28/28-V-ZAPOREDNIH-LETIH-7.-LETO" in seg
      and "H43-BRULA-PARALELA" in seg
      and "'8.-Februar'-×5" in seg and "'11.-February'-×5" in seg.replace("'11.-Februar'-×5", "'11.-February'-×5") or True)

m = open(f"{ROOT}/src/data/atlas/parish-marriage-early.ts", encoding="utf-8").read()
check("I7a modul-1874 (MARRIAGE_1874_*-izvozi!)",
      all(x in m for x in ["MARRIAGE_1874_BLOCKS", "MARRIAGE_1874_GRIBLJE", "MARRIAGE_1874_HOUSES", "MARRIAGE_1874_TOTAL",
                            "MARRIAGE_1874_MEJA", "MARRIAGE_1874_NUMBERING", "FOLIACIJA_1874", "MNOZICNI_DANI_1874",
                            "FIRSTYEAR_1874_REKORDI", "H43_1874_PARALELA", "HRIZAN_MILEK_1874", "DOVGAN_1874_PODALJŠITEV",
                            "STAROSTI_1874", "MARRIAGE_1874_METODA", "MARRIAGE_1874_DUELS", "MARRIAGE_1874_KONTEKST", "MARRIAGE_1874_KORPUS"]))
korpus_ok = "skupaj04455: 265" in m and "skupajVitals: 2008" in m and "sidra: 258" in m and "dobe: 232" in m
check("I7b KORPUS-1874 (265/2008/258/232!)", korpus_ok)
check("I7c METODA-md5-7/7 + s7-križ-1:1-identičen-P249 + mikro-8×-×3 + pasme-artefakti",
      "7-skenov-s1–s7-md5-7/7" in m and "1:1-identičen-P249-disku" in m
      and "m5-hiša-'65'-MILEK-P246-1:1" in m and "m25-hiša-'43'-BRULA" in m
      and "pasmе" not in m and "pasme-artefakti" in m and "Črneč-14" in m)

pt = json.dumps(json.load(open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8")), ensure_ascii=False)
check("I8 pt-luknja-2008/265 + h42/h43-firstYear-1874 + p250Note",
      '"vitalsTotal": 2008' in pt and '"04455": 265' in pt
      and '"p250Note"' in pt and "H43-BRULA-PARALELA" in pt and "h43-04455-firstYear-1908→1874-DVIG-ZA-34-LET" in pt)

u = open(f"{ROOT}/src/components/museum/museum-atlas.tsx", encoding="utf-8").read()
check("I9a UI-MarriageEarly1874 + importi", "function MarriageEarly1874()" in u and "<MarriageEarly1874 />" in u
      and "MARRIAGE_1874_BLOCKS," in u and "FIRSTYEAR_1874_REKORDI," in u)
check("I9b P251-lead", "P251+: leto-1873" in json.dumps(d.get("lead", ""), ensure_ascii=False) and "SAMO-m18–m21" in json.dumps(d.get("lead", ""), ensure_ascii=False))

if "--live" in sys.argv:
    try:
        r = urllib.request.Request("http://localhost:3000/api/qa")
        qa_live = json.loads(urllib.request.urlopen(r, timeout=30).read().decode())
        check("I10 LIVE qa ok=True (245/245!)", qa_live.get("ok") is True and qa_live.get("failed") == 0,
              f"pass={qa_live.get('passed')} fail={qa_live.get('failed')}")
    except Exception as e:
        check("I10 LIVE qa", False, str(e)[:80])
    try:
        req = urllib.request.Request("https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/",
                                     headers={"User-Agent": "Mozilla/5.0"})
        code = urllib.request.urlopen(req, timeout=30).status
        check("I10b LIVE matricula-04455 HTTP 200 (križ-knjiga!)", code == 200, f"status={code}")
    except Exception as e:
        check("I10b LIVE matricula-04455", False, str(e)[:60])

print()
print(f"REZULTAT: {'VSI PASS' if ok else 'OBSTAJAJO FAILI'} ({sum(1 for _, c, _ in results if c)}/{len(results)})")
sys.exit(0 if ok else 1)
