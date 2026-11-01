#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P174 — verifikator MRLIŠKE knjige 04894, leto 1908 (22. → 23. polno leto).
Celoten neodvisen preracun iz bundled parish.ts + dokaz-JSON + qa + kaskada.
I-checki I1–I13 (vzorec P153–P173); --live = dodatna HTTP verifikacija
matricula-online.eu.
P174-novosti: 76 vpisov (zap1–76, ČISTA-SEKVENCA!) / 13 GRIBLJE / 12 hiš
(h24 ×2 = PADEC-vzorec-5.-leto!) + ★★★ z47-'SE-JE-OBESIL' = 2.-SUICID-LINIJE
(1892-h9-1.! — 16-letni-lok!) + BREZ-PODPISA + ★★★ z57-'Z-VRCA-PADEL-JE-SE-UBIL'
= 2.-TRAUMA-SMRT + 'sv.-olje' = 3.-IZPISANI-SAKRAMENT! + ★★★ z25-'VSLED-TEŽKEGA-
PORODA' = PORODNA-SMRT-#3 (1888-×2 → 1908-OTROK!) + ŠKRLATINKA-EPIDEMIJA-×10
(Jun–Sep + SMUK-SIBLI-1-DAN!) + 'DOBRČI-[~]'-NERAZREŠEN-×4 + VLM-korekcije-
imen-×10 + številke-×4 (z10-'81'→51 = P173-LEAD-KOREKCIJA!) + NOVI-DUHOVNIK-
'G. g. Matija-CERAR-DEKAN' + z31-MRTVOROJEN-vas-'Zorit-[?]' + z72-smrt-IZBRISANA
+ MEJA-1908/09 = s121 (16. POTRDITEV — P173-lead-'[~ s119+?]' KOREKCIJA!).
Kumulativ: vitals 996 → 1009, mrliški bloki 04894 297 → 310, p80 92 NESPREMENJENE
(vseh-12-hiš-ŽE-v-p80!), korpus 93 NESPREMENJEN, PT 29."""
import json, os, re, sys, time, urllib.request, urllib.error

DOKAZ = "research/issue17/parish-death-1908.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
QA_TS = "src/lib/qa-parish.ts"
PARISH_TS = "src/data/atlas/parish.ts"

EXPECTED_ENTRIES = 76   # 13 Griblje + 63 ne-Griblje
EXPECTED_EXCLUDED = 2
EXPECTED_ANOMALIES = 14
EXPECTED_CROSSCHECKS = 5
GRIBLJE_HOUSES = "2,3,5,20,24,24,30,33,39,42,44,83,85"
GRIBLJE_ZAPS = [10, 16, 20, 25, 42, 47, 54, 59, 64, 70, 71, 72, 75]
VITALS_TOTAL = 1020             # 996 + 13!
BLOKI_04894 = 321               # 297 + 13!
P80_HOUSES = 92                 # NESPREMENJENO (vseh-12-hiš-ŽE-v-p80!)
KORPUS_HOUSES = 93              # NESPREMENJENO
NEW_SCANS = [115, 116, 117, 118, 119, 120, 121]  # s114-reuse (P173-meja-lead!) + s122 = 1909-lead

results = []


def check(name, ok, detail=""):
    results.append((name, ok, detail))


def http_get(url, timeout=30, tries=3):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            if e.code in (403, 429, 502, 503):
                time.sleep(3 * (i + 1))
                last = e
                continue
            return e.code, b""
        except Exception as e:
            last = e
            time.sleep(3 * (i + 1))
    raise last


def parse_house_vitals():
    """Preprost parsnik HOUSE_VITALS iz parish.ts (vzorec p80)."""
    src = open(PARISH_TS, encoding="utf-8").read()
    m = re.search(r"export const HOUSE_VITALS[^=]*=\s*\[(.*?)\n\];", src, re.S)
    body = m.group(1)
    vitals = []
    for obj in re.finditer(r"\{(.*?)\}", body, re.S):
        o = obj.group(1)

        def pick(key):
            mm = re.search(key + r':\s*"((?:[^"\\]|\\.)*)"', o)
            return mm.group(1) if mm else None

        def pickn(key):
            mm = re.search(key + r':\s*(\d+)', o)
            return int(mm.group(1)) if mm else None

        h = pick("houseNo")
        b = pick("bookSignature")
        y = pickn("year")
        if h and b and y:
            vitals.append({"houseNo": h, "bookSignature": b, "year": y,
                           "scan": pickn("scan"), "page": pickn("page"),
                           "whatSi": pick("whatSi") or ""})
    return vitals


def main():
    live = "--live" in sys.argv
    d = json.load(open(DOKAZ, encoding="utf-8"))
    ent = d["entries"]
    fr = d["frame"]
    grb = [e for e in ent if str(e["vas"]).lower().startswith("griblje")]

    # ---------- I1: dokaz ----------
    check("I1 dokaz obstaja + status", d["status"] == "SAMPLE-TRANSCRIPTION-D1908", d["status"])
    check("I1b 76 vnosov (13-Griblje + 63-ne-Griblje!)", len(ent) == EXPECTED_ENTRIES, str(len(ent)))
    check("I1c 2 excluded / 14 anomalij / 5 križnih",
          len(d["excluded"]) == EXPECTED_EXCLUDED and len(d["anomalies"]) == EXPECTED_ANOMALIES
          and len(d["crossChecks"]) == EXPECTED_CROSSCHECKS,
          f"{len(d['excluded'])}/{len(d['anomalies'])}/{len(d['crossChecks'])}")

    # ---------- I2: okvir ----------
    check("I2 1908 = 76 vpisov / 13 Griblje / 12 hiš (h24-×2-PADEC-5.-leto!)",
          fr["vpisi"] == 76 and fr["zap_oštevilčenih"] == 76
          and fr["griblje_vpisi"] == 13 and fr["hise"] == 12 and fr["ponovitve"] == "24",
          f"{fr['vpisi']}/{fr['zap_oštevilčenih']}/{fr['griblje_vpisi']}/{fr['hise']}")
    check("I2b 14-anomalij (SUICID + TRAUMA + POROD-#3 + ŠKRLATINKA-×10!) + glave-'18'-×7",
          "SE JE OBESIL" in d["anomalies"][2]["opis"] and len(fr["glave_napake"]) == 3
          and any("181908" in g or "18[ročno-1908]" in g for g in fr["glave_napake"]),
          str(len(fr["glave_napake"])))
    check("I2c hiše-zaporedje (h24-×2!)",
          ",".join([str(e["houseNo"]) for e in sorted(grb, key=lambda x: int(x["houseNo"]))]) == GRIBLJE_HOUSES,
          ",".join([str(e["houseNo"]) for e in sorted(grb, key=lambda x: int(x["houseNo"]))]))

    # ---------- I3: zap-continuity ----------
    zaps = sorted(int(e["zap"]) for e in grb)
    check("I3a Griblje-zap: 10,16,20,25,42,47,54,59,64,70,71,72,75",
          zaps == GRIBLJE_ZAPS, str(zaps))
    check("I3b ČISTA-SEKVENCA zap1–76 (BREZ-predorov/DUPLIKATOV — 4.-čisto-leto!)",
          sorted(int(e["zap"]) for e in ent) == list(range(1, 77)), "")
    check("I3c neštevilčenih = 0", fr["neštevilčenih"] == 0, "")

    # ---------- I4: invarianta ----------
    check("I4 stran == sken − 1 (vseh 76 — 88.–95. potrditev!)",
          all(e["page"] == e["scan"] - 1 for e in ent), "")
    check("I4b skeni: s114-reuse + s115–s121 (8-skupaj; s122 = 1909-lead!)",
          all(e["scan"] in [114] + NEW_SCANS for e in ent), str(sorted({e["scan"] for e in ent})))

    vit = parse_house_vitals()
    d04894 = [v for v in vit if v["bookSignature"] == "04894"]
    d1908 = [v for v in d04894 if v["year"] == 1908]

    # ---------- I5: hišne veze (parish.ts-whatSi-long-forme!) ----------
    e44 = next(v for v in d1908 if v["houseNo"] == "44")
    check("I5a h44-Peter-HROVAT = SE-JE-OBESIL = SAMOMOR-2.-V-LINIJI (1892-16-letni-lok!)",
          "HROVAT" in e44["whatSi"] and "SE JE OBESIL" in e44["whatSi"]
          and "SAMOMOR-2.-V-LINIJI" in e44["whatSi"] and "BREZ PODPISA" in e44["whatSi"], "")
    e85 = next(v for v in d1908 if v["houseNo"] == "85")
    check("I5b h85-Jožef-PERDINEC = VSLED-TEŽKEGA-PORODA = PORODNA-SMRT-#3 (1888-×2!)",
          "PERDINEC" in e85["whatSi"] and "VSLED TEŽKEGA PORODA" in e85["whatSi"]
          and "PORODNA-SMRT-#3" in e85["whatSi"], "")
    e42 = next(v for v in d1908 if v["houseNo"] == "42")
    check("I5c h42-Doroteja-PEZDIREC = P173-LEAD-'81'-KOREKCIJA-→-51 (max-zoom!)",
          "PEZDIREC" in e42["whatSi"] and "P173-LEAD-'81'-KOREKCIJA" in e42["whatSi"]
          and "51 LET" in e42["whatSi"], "")
    e83 = next(v for v in d1908 if v["houseNo"] == "83")
    check("I5d h83-Anton-BRINEC = VLM-'Alojz-Ožinger'-ZAVRJENA (P173-patroN!)",
          "BRINEC" in e83["whatSi"] and "Alojz-Ožinger" in e83["whatSi"], "")
    e20 = next(v for v in d1908 if v["houseNo"] == "20")
    check("I5e h20-Katarina-PEZDIREC = P175-KOREKCIJA-×2 (prejšnja-'PERDINEC'-'Pečnik'-ZAVRJENA — z-DESCENDER!)",
          "PEZDIREC" in e20["whatSi"] and "P175-KOREKCIJA" in e20["whatSi"]
          and "PERDINEC' ZAVRJENA" in e20["whatSi"], "")
    e24a = next(v for v in d1908 if v["houseNo"] == "24" and "BRINEC" in v["whatSi"])
    check("I5f h24-Marjeta-BRINEC = VLM-'Majeta-Binec'-KOREKCIJA (P173-patroN!)",
          "Marjeta BRINEC" in e24a["whatSi"] and "Majeta-Binec" in e24a["whatSi"], "")
    e24b = next(v for v in d1908 if v["houseNo"] == "24" and "subfamilija" in v["whatSi"])
    check("I5g h24-×2-v-1908-PADEC-vzorec-5.-leto (z16 + z64 — različni-priimki!)",
          "h24-×2-v-1908" in e24b["whatSi"] and "PADEC-vzorec-5.-LETO" in e24b["whatSi"]
          and "KURRENT-2/3" in e24b["whatSi"], "")
    e2 = next(v for v in d1908 if v["houseNo"] == "2")
    check("I5h h2-Mihael-TAPRIČ = TAPRIČ-vez-h2×h33 (mati+sin-hipoteza!)",
          "TAPRIČ" in e2["whatSi"] and "TAPRIČ-vez-h2×h33" in e2["whatSi"], "")
    e5 = next(v for v in d1908 if v["houseNo"] == "5")
    check("I5i h5-Marija-ŠTRUCELJ = VLM-'Špancej'-ZAVRJENA + smrt-IZBRISANA (edina-1908!)",
          "ŠTRUCELJ" in e5["whatSi"] and "Špancej" in e5["whatSi"]
          and "EDINA-1908-vrsta-BREZ-datuma-smrti" in e5["whatSi"], "")
    e39 = next(v for v in d1908 if v["houseNo"] == "39")
    check("I5j h39-Barbara-MILEK = VLM-'Mlek'-KOREKCIJA + 'dnadelovka' [~]",
          "MILEK" in e39["whatSi"] and "dnadelovka" in e39["whatSi"], "")

    # ---------- I6: kumulativ + parish.ts ----------
    check("I6a vitals 1009", len(vit) == VITALS_TOTAL, str(len(vit)))
    check("I6b mrliški bloki 04894 = 310", len(d04894) == BLOKI_04894, str(len(d04894)))
    check("I6c bloki 1908 = 13", len(d1908) == 13, str(len(d1908)))
    check("I6d bloki 1908: skeni 115–120 + stran == sken − 1",
          all(v["scan"] and 115 <= v["scan"] <= 120 and v["page"] == v["scan"] - 1 for v in d1908), "")
    check("I6d2 bloki 1910+ ne obstajajo (P176-lead!; P175 = 1909 sedaj v korpusu!)",
          all(v["year"] < 1910 for v in d04894), "")
    p80 = open("scripts/p80_parish_md_books.py", encoding="utf-8").read()
    check("I6e p80-skripta pini 1009 + 92 + gap-18 (vitals-P174-kaskada!)",
          "len(vitals) == 1020" in p80 and "len(houses) == 93" in p80 and "len(gap) == 18" in p80, "")
    houses_all = {v["houseNo"] for v in vit if v["houseNo"].isdigit()}
    check("I6f korpus = 93 hiš (NESPREMENJENO — vseh-12-1908-hiš-ŽE-v-korpusu!)",
          len(houses_all) == KORPUS_HOUSES, str(len(houses_all)))

    # ---------- I7: forenzika (anomalije A1–A14!) ----------
    a1 = next(x for x in d["anomalies"] if x["id"] == "A1")
    check("I7a A1: VLM-HALUCINACIJE-imen-×10 (BRINEC + HROVAT + PERDINEC-×3 + ŠTRUCELJ!)",
          "BRINEC" in a1["opis"] and "HROVAT" in a1["opis"] and "ŠTRUCELJ" in a1["opis"]
          and "ŽUGELJ" in a1["opis"], "")
    a3 = next(x for x in d["anomalies"] if x["id"] == "A3")
    check("I7b A3: SAMOMOR-2.-V-LINIJI (1892-h9-16-letni-lok!) + BREZ-PODPISA",
          "SAMOMOR" in a3["opis"] and "2.-V-LINIJI" in a3["opis"] and "1892" in a3["opis"]
          and "BREZ-podpisa-pri-samomoru" in a3["opis"], "")
    a4 = next(x for x in d["anomalies"] if x["id"] == "A4")
    check("I7c A4: 'Z-VRCA-PADEL-JE-SE-UBIL' + sv.-olje = 3.-SAKRAMENT",
          "PADEL" in a4["opis"] and "sv. olje" in a4["opis"] and "3.-IZPISANI-SAKRAMENT" in a4["opis"], "")
    a6 = next(x for x in d["anomalies"] if x["id"] == "A6")
    check("I7d A6: ŠKRLATINKA-EPIDEMIJA-×10 + SMUK-SIBLI-1-DAN",
          "ŠKRLATINKA" in a6["opis"] and "×10" in a6["opis"] and "SMUK" in a6["opis"], "")
    a7 = next(x for x in d["anomalies"] if x["id"] == "A7")
    check("I7e A7: DOBRČI-NERAZREŠEN-×4 (X8-epidemija!)",
          "DOBRČI" in a7["opis"] and "×4" in a7["opis"], "")
    a9 = next(x for x in d["anomalies"] if x["id"] == "A9")
    check("I7f A9: NOVI-DUHOVNIK-Matija-CERAR-DEKAN + OPOMBA-marginalija",
          "Matija-CERAR-DEKAN" in a9["opis"] and "OPOMBA-marginalija" in a9["opis"], "")

    # ---------- I8: meje + lead ----------
    c1 = d["crossChecks"][0]["opis"]
    check("I8a zap-kontinuiteta (C1 — 76-oštevilčenih = 76-VPISOV!)",
          "76-oštevilčenih" in c1 and "ČISTA-SEKVENCA" in c1, c1[:60])
    check("I8b meja 1907/08 = s114 + meja 1908/09 = s121 (16.-POTRDITEV — KOREKCIJA!)",
          "s114" in fr["meja_1907_08"] and "s121" in fr["meja_1908_09"]
          and "16. POTRDITEV" in fr["meja_1908_09"]
          and "BREZ-podčrtanja" in fr["meja_1908_09"]
          and "KOREKCIJA" in fr["meja_1908_09"], "")
    ns = json.dumps(d["nextSteps"], ensure_ascii=False)
    check("I8c P175-lead v dokazu (1909 + Stublar-92 + ŠILAK-dvojčki!) [P175-zgodovinska]",
          "P175-lead" in ns and "1909" in ns and "Stublar" in ns and "ŠILAK" in ns, "")
    check("I8d X1–X2 excluded (s121-zap1–10-1909 + s122!)",
          len(d["excluded"]) == 2 and "s121-zap1–10" in d["excluded"][0]["opis"]
          and "s122" in d["excluded"][1]["opis"], "")

    # ---------- I9: demografija ----------
    duh = [e["duhovnik"] or "" for e in grb]
    n_rauq = sum(1 for x in duh if "Rauq" in x)
    n_cer = sum(1 for x in duh if "Cerar" in x or "CERAR" in x)
    n_brez = sum(1 for x in duh if "BREZ" in x)
    check("I9a duhovniki-Griblje: Cerar-×9 + Rauq-×3 + BREZ-×1 = 13",
          n_rauq == 3 and n_cer == 9 and n_brez == 1,
          f"R{n_rauq}/C{n_cer}/B{n_brez}")
    meseci = {}
    for e in grb:
        k = (e["mesec"] or "")[:3]
        meseci[k] = meseci.get(k, 0) + 1
    check("I9b meseci Griblje: Mar1 + Apr1 + Maj2 + Jul1 + Avg1 + Sep1 + Okt2 + Nov1 + Dec3 = 13",
          meseci.get("Mar") == 1 and meseci.get("Apr") == 1 and meseci.get("Maj") == 2
          and meseci.get("Jul") == 1 and meseci.get("Avg") == 1 and meseci.get("Sep") == 1
          and meseci.get("Okt") == 2 and meseci.get("Nov") == 1 and meseci.get("Dec") == 3, str(meseci))
    check("I9c starostni-razpon: '—' (porod!) → 85-let (Griblje-×1 + Krasinec-×1 = 2!)",
          any(e["starost"] == "—" for e in grb)
          and sum(1 for e in grb if "85" in e["starost"]) == 1
          and sum(1 for e in ent if "85 LET" in str(e.get("starost") or "")) == 2, "")
    otroci = [e for e in grb if "DNI" in e["starost"] or "MESECEV" in e["starost"]
              or "MESECE" in e["starost"] or "TEDNOV" in e["starost"] or e["starost"] == "—"]
    check("I9d otroška-smrt 2/13 (z25-'—'-porod + z64-5-mes!; 11-let-z16-otrok-v-širšem-smislu)",
          len(otroci) == 2, str([(e["houseNo"], e["starost"]) for e in otroci]))
    prev = [e["previden"] for e in grb]
    check("I9e previden-Griblje: '1' ×7 + '.'/prazno ×6",
          sum(1 for x in prev if str(x).strip() == "1") == 7, str(prev))

    # ---------- I10: qa-parish + pin-kaskada ----------
    qa = open(QA_TS, encoding="utf-8").read()
    check("I10a qa-p174 = 175. kontrola", "qa-p174-parish-death-1908" in qa, "")
    check("I10b qa-parish pini 1009 + 310 (P174-kaskada!)",
          qa.count("!== 1020") == 90 and qa.count("!== 321") == 24,
          f"1009×{qa.count('!== 1020')}/310×{qa.count('!== 321')}")
    check("I10c qa-parish guardi ≥1909 (22× — P174-kaskada-21 + qa-p174-lastni!)",
          qa.count(">= 1910") == 23, f"{qa.count('>= 1910')}")
    check("I10d qa-parish p80 = 92 (24× — NESPREMENJENO!)",
          qa.count("p80Houses.size !== 93") == 24, f"{qa.count('p80Houses.size !== 93')}")
    check("I10e 1908-izjeme-v-guardih (p85-h30 + p90-h20!)",
          all(f'"04894" && v.year === 1908 && hn === "{h}"' in qa for h in ["30", "20"])
          and qa.count('"04894" && v.year === 1908 && hn ===') == 2, "")

    # ---------- I11: parish.ts-kaskada ----------
    src = open(PARISH_TS, encoding="utf-8").read()
    check("I11a P174-blok-komentar-v-parish.ts",
          "P174: mrliška 1908" in src, "")
    check("I11b P174-13-blokov-whatSi-potrditve (SAMOMOR + POROD + KOREKCIJE!)",
          all(k in src for k in ["SE JE OBESIL", "SAMOMOR-2.-V-LINIJI", "VSLED TEŽKEGA PORODA",
                                 "P173-LEAD-'81'-KOREKCIJA", "VLM-'Alojz-Ožinger'-ZAVRJENA",
                                 "P175-KOREKCIJA", "h24-×2-v-1908", "TAPRIČ-vez-h2×h33",
                                 "ŠTRUCELJ", "EDINA-1908-vrsta-BREZ-datuma-smrti"]), "")
    check("I11c P175-LEAD-v-parish.ts (s121-zap1–10 + s122!)",
          "P175-LEAD: 1909" in src and "s122-zap11–22" in src, "")
    check("I11d ni-04894-1910-blokov-še (P176-lead!; 04455/04105-1910-legalno!)",
          re.search(r'bookSignature: "04894",\s*year: 1910', src) is None, "")

    # ---------- I12: honesty ----------
    check("I12 honesty ≥6 (honesty-1–6!)",
          len(d["honesty"]) >= 6, str(len(d["honesty"])))
    check("I12b honesty-rows-v3-FAIL-lekcija (diag-grid-recept — 3.-leto!)",
          any("rows-v3" in x for x in d["honesty"]), "")

    # ---------- I13: --live (HTTP!) ----------
    if live:
        st, body = http_get(BOOK_URL)
        ok = st == 200 and (b"04894" in body or b"podzemelj" in body.lower())
        check("I13a --live matricula-04894-dostopen", st == 200, f"HTTP {st}")
        check("I13b dokaz-Griblje == parish.ts-Griblje (1:1!)",
              sorted([e["houseNo"] for e in grb]) == sorted([v["houseNo"] for v in d1908]),
              f"{sorted([e['houseNo'] for e in grb])}")
        check("I13c dokaz-skeni == parish.ts-skeni (1:1!)",
              sorted([(e["houseNo"], e["scan"], e["page"]) for e in grb])
              == sorted([(v["houseNo"], v["scan"], v["page"]) for v in d1908]), "")

    ok_n = sum(1 for _, ok, _ in results if ok)
    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'}: {name}" + (f" — {detail}" if detail and not ok else ""))
    print(f"\nP174: {ok_n}/{len(results)} " + ("PASS ✓" if ok_n == len(results) else "FAIL ✗"))
    return 0 if ok_n == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
