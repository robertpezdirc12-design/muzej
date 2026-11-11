#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P251 — verifikator POROČNE PREDZGOVINE 04455, leto 1873 = 13/13 KONČNO (ZAKLJUČEK predzgovine!) (I1–I10 + --live)."""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "04455",\s*year: 1873,', src)
check("I1 bloki 04455/1873 == 4 hiše / 2 POLNA-DVOJNA (h13×h62 + h22×h50!)",
      len(bloki) == 4 and bloki == ["13", "62", "22", "50"],
      f"najdeno {len(bloki)}: {','.join(bloki)}")
skupaj = src.count('bookSignature: "04455"')
check("I2 vitals-2026 + 04455==269", "HOUSE_VITALS.length !== 2032" not in src and skupaj == 269, f"04455={skupaj}")

nove = re.findall(r'houseNo: "(\d+)",\s*bookSignature: "04455",\s*year: 1873,\s*scan: (\d+),\s*page: (\d+),', src)
pag_ok = all(int(p) == int(s) - 1 for _, s, p in nove)
check("I3 sken+pag (pag=sken−1!-NA-ODPIRANJU!-s2/Pag.1!)", len(nove) == 4 and pag_ok and {s for _, s, _ in nove} == {"2"},
      ";".join(f"h{h}-s{s}/p{p}" for h, s, p in nove))

d = json.load(open(f"{ROOT}/research/issue17/parish-marriage-1873-04455.json", encoding="utf-8"))
an = json.dumps(d["anomalie"], ensure_ascii=False)
check("I4 dokaz (4-vpisi-BREZ-preskokov + 2-POLNA-DVOJNA-50%-REKORD + KNIŽNO-ODPIRANJE-marginala-18! + MEJA-13.-VARIANTA!)",
      d["stats"]["entries"] == 4 and d["stats"]["gribljeBlocks"] == 2 and d["stats"]["polniDvojni"] == 2
      and d["stats"]["nodat"] == 0
      and "KNIŽNO-ODPIRANJE-04455" in d["frame"]["knjizno_odpiranje"]
      and "P250-napoved-IZPOLNJENA" in d["frame"]["knjizno_odpiranje"]
      and "s1 = VEZALO KNJIGE" in d["frame"]["knjizno_odpiranje"]
      and "m1–m17" in d["frame"]["knjizno_odpiranje"]
      and "s2-MID/DNO" in d["frame"]["meja_1873_74"]
      and "13.-MEJNA-VARIANTA" in d["frame"]["meja_1873_74"]
      and "NA-ISTI-STRANI!" in d["frame"]["meja_1873_74"]
      and "1/1-1873" in d["frame"]["foliacija"]
      and "29/29" in d["frame"]["foliacija"]
      and "8.-LETO" in d["frame"]["foliacija"]
      and "18–21" in d["frame"]["numbering"]
      and "NODAT-×0-6.-leto" in d["frame"]["numbering"]
      and "13-LET (1873–1885" in d["frame"]["dovgan_13_let"]
      and "13/13-LET-VSEH" in d["frame"]["pezdirc_13_let"]
      and "4-datumov-BREZ-duelov" in d["frame"]["datum_vzorec"]
      and "Augst. 23." in d["frame"]["datum_vzorec"],
      f"entries={d['stats']['entries']} bloki={d['stats']['gribljeBlocks']} dvojni={d['stats']['polniDvojni']}")
check("I4b bloki-m18-h13×h62 + m20-h22×h50 + 4-DVIGI (h22-25-LET!-h62-20-LET!-h13-9!-h50-6!)",
      any(b["vpis"] == "m18" and "POLNI-DVOJNI" in b.get("h13", "") and "GRIBLJE-13" in b.get("h13", "") and "GRIBLJE-62" in b.get("h13", "") for b in d["bloki"])
      and any(b["vpis"] == "m20" and "POLNI-DVOJNI" in b.get("h22", "") and "GRIBLJE-22" in b.get("h22", "") and "GRIBLJE-50" in b.get("h22", "") for b in d["bloki"])
      and "h22-04455-firstYear-1898→1873-DVIG-ZA-25-LET" in an
      and "h62-04455-firstYear-1893→1873-DVIG-ZA-20-LET" in an
      and "h13-04455-firstYear-1882→1873-DVIG-ZA-9-LET" in an
      and "h50-04455-firstYear-1879→1873-DVIG-ZA-6-LET" in an)
an2 = json.dumps(d, ensure_ascii=False)
check("I4c kontekst-m19-KLAGENFURT-IBERER + m21-VETRHVIŠČE + FERCHER-TERŽEK + niti (MILEK-×2!-HRIŽAN-×3!-ŠIMEC-×3!-KUNIČ!)",
      "IBERER" in an2 and "KLAGENFURT" in an2 and "HOMOLSCH" in an2
      and "VETRHVIŠČE" in an2 and "FERCHER" in an2 and "TERŽEK" in an2
      and "MILEK-×2" in an and "HRIŽAN-×3" in an and "ŠIMEC-×3" in an and "KUNIČ" in an
      and "50%-količnik" in an and "GABOFAIČ" in an2)

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 2043")
check("I5 qa-p251 + števec-2043 (×150!)", "HOUSE_VITALS.length !== 2011" not in qa and st >= 150, f"2043-številcev={st}")
check("I5b sidra-262 + 1873:4-P251 (qa-sidra-message)", "poročna sidra ≠ 262 (1873:4-P251!" in qa)
check("I5c dobe-236 + 66-pred-linijskih", "dobe-bloki ≠ 236/7/26" in qa and "66 pred-linijskih 1873-P251×4!" in qa)
check("I5d p80-1873:4-garda + sken-garda-s2", 'p80MarrAnchors.filter((h) => h.year === 1873).length !== 4' in qa and "poročna sidra 1873: sken ≠ 2 (P251: samo-s2-Pag.-1!-s1-vezalo!" in qa)
check("I5e izjeme-p85-×2-h13/h22/h50/h62 + p94-h22 + MILIČ-250-P257",
      qa.count('!(v.bookSignature === "04455" && v.year === 1873 && (hn === "13" || hn === "22" || hn === "50" || hn === "62"))') >= 2
      and '(v.year === 1873 || v.year === 1898 || v.year === 1904 || v.year === 1919)' in qa
      and "MILIC_FAMILY_TOTAL !== 250" in qa and "53,78,20,36,60" in qa
      and "04455 ×60-P251-+4!" in qa)

i0 = src.find("P251: POROČNA PREDZGOVINA 04455, leto 1873")
seg = src[i0:] if i0 >= 0 else ""
check("I6a 4-vpisi + KNIŽNO-ODPIRANJE + marginala-18 + predhodnik",
      "1873" in seg and len(seg) > 100
      and "m18–m21" in seg and "m1–m17-leta-1873-NISO-v-tej-knjigi" in seg
      and "PRVA-tabelarna-stran" in seg and "**18**" in seg)
check("I6b 4-DVIGI + 2-POLNA-DVOJNA + MEJA-s2-MID/DNO + FOLIACIJA-29/29",
      "4-DVIGI-V-1-LETU-ZAKLJUČEK" in seg
      and "h22-04455-firstYear-1898→1873-DVIG-ZA-25-LET" in seg
      and "h62-1893→1873-ZA-20-LET" in seg
      and "h13-1882→1873-ZA-9-LET" in seg
      and "h50-1879→1873-ZA-6-LET" in seg
      and "2-POLNA-DVOJNA-V-4-VPISIH-=-50%-količnik-REKORD" in seg
      and "MEJA-1873/74 = s2-MID/DNO" in seg
      and "29/29-V-ZAPOREDNIH-LETIH-8.-LETO" in seg)

m = open(f"{ROOT}/src/data/atlas/parish-marriage-early.ts", encoding="utf-8").read()
check("I7a modul-1873 (MARRIAGE_1873_*-izvozi!)",
      all(x in m for x in ["MARRIAGE_1873_BLOCKS", "MARRIAGE_1873_GRIBLJE", "MARRIAGE_1873_HOUSES", "MARRIAGE_1873_TOTAL",
                            "KNIŽNO_ODPIRANJE_1873", "MARRIAGE_1873_MEJA", "FIRSTYEAR_1873_DVIGI", "DOVGAN_1873_ZAČETEK",
                            "PEZDIRC_1873_ODPIRANJE", "MARRIAGE_1873_NITI", "DATUMI_1873", "MARRIAGE_1873_METODA", "MARRIAGE_1873_KORPUS"]))
korpus_ok = "skupaj04455: 269" in m and "skupajVitals: 2012" in m and "sidra: 262" in m and "dobe: 236" in m
check("I7b KORPUS-1873 (269/2012/262/236!)", korpus_ok)
check("I7c METODA-md5-2×-neodvisen + očesi-NAJPREJ + solo-×12 + letterform-referenca-m20-'22'",
      "2-skena-s1–s2" in m and "md5-2×-neodvisen-prenos-1:1" in m and "očesi-NAJPREJ" in m
      and "referenca-m20-'22'" in m and "kronološka-verifikacija" in m and "reconciliacija-z-P250-tail" in m)

pt = json.load(open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8"))
check("I8 pt-luknja-2026/2043 vsota-1:1",
      pt.get("vitalsTotal") == 2043 and pt.get("corpus", {}).get("byBook", {}).get("04455") == 269,
      f"vitals={pt.get('vitalsTotal')} 04455={pt.get('corpus', {}).get('byBook', {}).get('04455')}")

u = open(f"{ROOT}/src/components/museum/museum-atlas.tsx", encoding="utf-8").read()
check("I9a UI-MarriageEarly1873 + importi", "function MarriageEarly1873()" in u and "<MarriageEarly1873 />" in u
      and "MARRIAGE_1873_BLOCKS," in u and "FIRSTYEAR_1873_DVIGI," in u and "KNIŽNO_ODPIRANJE_1873," in u
      and "PEZDIRC_1873_ODPIRANJE," in u and "DOVGAN_1873_ZAČETEK," in u and "MARRIAGE_1873_NITI," in u
      and "MARRIAGE_1873_MEJA," in u and "DATUMI_1873," in u and "MARRIAGE_1873_METODA," in u)
check("I9b P252-lead (13/13-ZAKLJUČENA + SINTEZA-možnost!)",
      "P252+" in json.dumps(d.get("lead", ""), ensure_ascii=False)
      and "13/13-ZAKLJUČENA" in json.dumps(d.get("lead", ""), ensure_ascii=False)
      and "SINTEZA-PREDZGOVINE" in json.dumps(d.get("lead", ""), ensure_ascii=False))

if "--live" in sys.argv:
    try:
        r = urllib.request.Request("http://localhost:3000/api/qa")
        qa_live = json.loads(urllib.request.urlopen(r, timeout=30).read().decode())
        check("I10 LIVE qa ok=True", qa_live.get("ok") is True and qa_live.get("failed") == 0,
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
