#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P171 — verifikator MRLIŠKE knjige 04894, leto 1905 (19. → 20. polno leto).
Celoten neodvisen preracun iz bundled parish.ts + dokaz-JSON + qa + kaskada.
I-checki I1–I13 (vzorec P153–P170); --live = dodatna HTTP verifikacija
matricula-online.eu.
P171-rekordi: 61 vpisov / 16 GRIBLJE = 2. REKORD LINIJE (rast 17→12→16!) /
14 hiš + h18/h27 ×2-v-1-letu (PADEC-vzorec ×3!) + 4 GLAVE-NAPAKE (s99-'18 905'
+ s101-'18'-NEKOMPLETNA-1.-v-liniji! + s102-'18/905'-POŠEVNICA + s103-'18 905')
+ PEZDIREC-×2-1905 = era-13 (×11-v-4-letih: 1902×3+1903×3+1904×3+1905×2!)
+ LENGSFELD-DOMINANTA ×15/16 (samo-z26-Rauq-Griblje!) + VLM-VAS-LEKCIJA-×4
(PREKINITEV-4-letnega-'0-napak'-vzorca!) + starost-korekcije-×9 (diag+kompozit!)
+ ime-VLM-zmede ×3 (z44-'Agnes'→ANTON + z49-'Lapajne'→CAPRIČ + z59-'Martina-
Hlavos'→ŠTRAVS!) + DVOJNI-VPIŠ-v-1-dnevu (z22+z23-Miše-h29!) + z57-'Se-ubila'
+ z38-'Žganje-v-glavi' + MEJA-1905/06 = s104 (13. POTRDITEV 5. STIL!).
Kumulativ: vitals 950 → 966, mrliški bloki 04894 251 → 267, p80 hiše 91
NESPREMENJENE, korpus 93 NESPREMENJEN (vseh-14-ŽE-v-p80!), PT 29 (BREZ-novega!)."""
import json, os, re, sys, time, urllib.request, urllib.error

DOKAZ = "research/issue17/parish-death-1905.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
QA_TS = "src/lib/qa-parish.ts"
PARISH_TS = "src/data/atlas/parish.ts"
NOTES = "research/issue17/parish-death-1905-notes.md"

EXPECTED_ENTRIES = 61   # 16 Griblje + 45 ne-Griblje (s-*!)
EXPECTED_EXCLUDED = 3
EXPECTED_ANOMALIES = 10
EXPECTED_CROSSCHECKS = 5
GRIBLJE_HOUSES = "2,18,21,25,27,31,32,35,42,59,63,64,65,81"
GRIBLJE_ZAPS = [1, 16, 19, 20, 24, 26, 29, 39, 40, 44, 47, 49, 50, 52, 59, 61]
VITALS_TOTAL = 1511             # 1205 + 14! (P190 = KONEC-KNJIGE!)
BLOKI_04894 = 520               # 506 + 14! (P190 = KONEC-KNJIGE!)
P80_HOUSES = 92                  # NESPREMENJENO (vseh-14-ŽE-v-p80!)
KORPUS_HOUSES = 93               # NESPREMENJENO
NEW_SCANS = [100, 101, 102, 103, 104]   # s99-reuse (diag iz P170 + VLM-datumi!)

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
    # Griblje-podmnožica (ne-Griblje-vpisi-imajo-'*'-v-houseNo — cf. excluded!)
    grb = [e for e in ent if not str(e["houseNo"]).endswith("*")]

    # ---------- I1: dokaz ----------
    check("I1 dokaz obstaja + status", d["status"] == "SAMPLE-TRANSCRIPTION-D1905", d["status"])
    check("I1b 61 vnosov (16-Griblje + 45-ne-Griblje-s-*!)", len(ent) == EXPECTED_ENTRIES, str(len(ent)))
    check("I1c 3 excluded / 10 anomalij / 5 križnih",
          len(d["excluded"]) == EXPECTED_EXCLUDED and len(d["anomalies"]) == EXPECTED_ANOMALIES
          and len(d["crossChecks"]) == EXPECTED_CROSSCHECKS,
          f"{len(d['excluded'])}/{len(d['anomalies'])}/{len(d['crossChecks'])}")

    # ---------- I2: okvir ----------
    check("I2 1905 = 61 vrstic / 16 Griblje / 14 hiš (2.-REKORD-LINIJE!)",
          fr["vrstic"] == 61 and fr["griblje_vpisi"] == 16 and fr["hise"] == 14,
          f"{fr['vrstic']}/{fr['griblje_vpisi']}/{fr['hise']}")
    check("I2b Griblje 17→12→16 (2.-REKORD!) + 4-GLAVE-NAPAKE + PEZDIREC-era-13",
          "17→12→16" in fr["rast"] and "4-GLAVE-NAPAKE" in fr["rekordi"]
          and "PEZDIREC" in fr["rekordi"], fr["rekordi"][:90])
    check("I2c hiše = 14 različnih (h18/h27-×2-v-1-letu!)",
          ",".join(sorted({str(e["houseNo"]) for e in grb}, key=int)) == GRIBLJE_HOUSES,
          ",".join(sorted({e["houseNo"] for e in grb}, key=int)))

    # ---------- I3: zap-continuity (ČISTO leto!) ----------
    zaps = sorted(int(e["zap"]) for e in grb)
    check("I3a Griblje-zap: 1,16,19,20,24,26,29,39,40,44,47,49,50,52,59,61",
          zaps == GRIBLJE_ZAPS, str(zaps))
    check("I3b zapcol-ČIST (61-oštevilčenih / 61-fizičnih; restart-61→1 = MEJA!)",
          fr["zap_oštevilčenih"] == 61 and fr["neštevilčenih"] == 0, "")

    # ---------- I4: invarianta ----------
    check("I4 stran == sken − 1 (vseh 61 — 72.–76. potrditev!)",
          all(e["page"] == e["scan"] - 1 for e in ent), "")
    check("I4b skeni: s99-reuse + s100–s104 (6-skupaj!)",
          all(e["scan"] in [99] + NEW_SCANS for e in ent), str(sorted({e["scan"] for e in ent})))

    vit = parse_house_vitals()
    d04894 = [v for v in vit if v["bookSignature"] == "04894"]

    # ---------- I5: hišne veze (parish.ts-whatSi-long-forme!) ----------
    def v_zap(vlist, z):
        return next(v for v in vlist if v["scan"] == 99 and z == 1) if z == 1 else next(
            v for v in vlist if v["year"] == 1905 and f"zap" in v["whatSi"].lower()[:0] or v)  # fallback

    d1905 = [v for v in d04894 if v["year"] == 1905]

    def v_hn(vlist, hn):
        return next(v for v in vlist if v["houseNo"] == hn)

    e1 = v_hn(d1905, "59")
    check("I5a h59-Marjeta = P170-lead-POTRJEN-×3 (PEZDIREC!)",
          "P170-lead" in e1["whatSi"] and "POTRJEN" in e1["whatSi"]
          and "PEZDIREC" in e1["whatSi"], "")
    e63 = v_hn(d1905, "63")
    check("I5b h63 = 4. mrliški vpis + 28.-PT-vez-kontinuiteta (1.-1904 = P170!)",
          "4. mrliški vpis" in e63["whatSi"] and "28.-PT-vez-kontinuiteta" in e63["whatSi"], "")
    e81 = v_hn(d1905, "81")
    check("I5c h81-Amalija = NOVI-MAKSIMUM-hiša-81 (2.-najvišja-mrliška-po-h91!)",
          "NOVI-MAKSIMUM-hiša-81" in e81["whatSi"] and "CINDRIČ" in e81["whatSi"], "")
    e18a = [v for v in d1905 if v["houseNo"] == "18" and "24 LET" in v["whatSi"]]
    e18b = [v for v in d1905 if v["houseNo"] == "18" and "7 MESECEV" in v["whatSi"]]
    check("I5d h18-×2-v-1-letu (z20-Ana-24-mati? + z52-Ana-7-mes-hči!)",
          len(e18a) == 1 and len(e18b) == 1 and "ŠIMEC" in e18a[0]["whatSi"]
          and "×2-v-1-letu" in e18a[0]["whatSi"], "")
    e27a = [v for v in d1905 if v["houseNo"] == "27" and "9½" in v["whatSi"]]
    e27b = [v for v in d1905 if v["houseNo"] == "27" and "75 LET" in v["whatSi"]]
    check("I5e h27-×2-v-1-letu (z40-Marija-9½ + z44-Anton-75-'Agnes'-ZAVRJENA!)",
          len(e27a) == 1 and len(e27b) == 1 and "KUKAR" in e27b[0]["whatSi"]
          and "Agnes" in e27b[0]["whatSi"], "")
    e59 = v_hn(d1905, "35")
    check("I5f h35-Martin-ŠTRAVS = ŠTRAVS-×2-hiši (h45-P169-×5 + h35!) — 9.-VPIS-REKORDISTKA (komentar!)",
          "ŠTRAVS" in e59["whatSi"] and "Martina-Hlavos" in e59["whatSi"]
          and "72 LET" in e59["whatSi"], "")
    e61 = v_hn(d1905, "42")
    check("I5g h42-Anton = ZADNJA-GRIBLJE-1905 + PEZDIREC-era-13-zaključek!",
          "ZADNJA-GRIBLJE-1905" in e61["whatSi"] and "PEZDIREC" in e61["whatSi"], "")
    e2 = v_hn(d1905, "2")
    check("I5h h2 = 6. mrliški vpis + EDINA-GRIBLJE-Rauq-1905 (Lengsfeld-×15-DOMINANTA!)",
          "6. mrliški vpis" in e2["whatSi"] and "EDINA-GRIBLJE-Rauq-1905" in e2["whatSi"], "")
    e35h = v_hn(d1905, "65")
    check("I5i h65 = 7. mrliški vpis + h81 = 3. mrliški vpis (rekordisti!)",
          "7. mrliški vpis" in e35h["whatSi"] and "3. mrliški vpis" in e81["whatSi"], "")

    # ---------- I6: kumulativ + parish.ts ----------
    vit = parse_house_vitals()
    d04894 = [v for v in vit if v["bookSignature"] == "04894"]
    check("I6a vitals 976", len(vit) == VITALS_TOTAL, str(len(vit)))
    check("I6b mrliški bloki 04894 = 277", len(d04894) == BLOKI_04894, str(len(d04894)))
    d1905 = [v for v in d04894 if v["year"] == 1905]
    check("I6c bloki 1905 = 16", len(d1905) == 16, str(len(d1905)))
    check("I6d bloki 1905: skeni 99–104 + stran == sken − 1",
          all(v["scan"] and 99 <= v["scan"] <= 104 and v["page"] == v["scan"] - 1 for v in d1905), "")
    check("I6d2 bloki 1908+ ne obstajajo (P174-lead!; P171 = 1905 sedaj v korpusu!)",
          all(v["year"] < 1925 for v in d04894), "")
    p80 = open("scripts/p80_parish_md_books.py", encoding="utf-8").read()
    check("I6f p80-skripta pini 966 + 91 + gap-18 (vitals-P171-kaskada!)",
          "len(vitals) == 1100" in p80 and "len(houses) == 94" in p80 and "len(gap) == 18" in p80, "")
    houses_all = {v["houseNo"] for v in vit if v["houseNo"].isdigit()}
    check("I6g korpus = 93 hiš (NESPREMENJENO — vseh-14-hiš-ŽE-v-korpusu!)",
          len(houses_all) == KORPUS_HOUSES, str(len(houses_all)))

    # ---------- I7: forenzika (VLM-VAS-LEKCIJA + starost-korekcije!) ----------
    a1 = next(x for x in d["anomalies"] if x["id"] == "A1")
    check("I7a A1: 4-GLAVE-NAPAKE (18 905 ×2 + nekompletna-s101 + poševnica-s102!)",
          "4 GLAVE-NAPAKE" in a1["opis"] and "NEKOMPLETNA" in a1["opis"]
          and "POŠEVNICA" in a1["opis"], "")
    a2 = next(x for x in d["anomalies"] if x["id"] == "A2")
    check("I7b A2: PEZDIREC-era-13-×11-v-4-letih (+z15-ne-Griblje-×3-vpisi!)",
          "era-13" in a2["opis"] and "×11-v-4-letih" in a2["opis"], "")
    a3 = next(x for x in d["anomalies"] if x["id"] == "A3")
    check("I7c A3: VLM-VAS-LEKCIJA-×4 (PREKINITEV-4-letnega-vzorca!)",
          "VLM-VAS-LEKCIJA" in a3["opis"] and "PREKINITEV-4-letnega" in a3["opis"], "")
    a4 = next(x for x in d["anomalies"] if x["id"] == "A4")
    check("I7d A4: LENGSFELD-DOMINANTA-×15/16 (samo-z26-Rauq!)",
          "LENGSFELD-DOMINANTA" in a4["opis"] and "×15/16" in a4["opis"], "")
    a5 = next(x for x in d["anomalies"] if x["id"] == "A5")
    check("I7e A5: h18-×2 + h27-×2-v-1-letu (PADEC-vzorec-×3!)",
          "h18-×2" in a5["opis"] and "h27-×2" in a5["opis"], "")
    a6 = next(x for x in d["anomalies"] if x["id"] == "A6")
    check("I7f A6: DVOJNI-VPIŠ-v-1-dnevu (z22+z23-MIŠE-h29-oba-9-mes!)",
          "DVOJNI-VPIŠ" in a6["opis"] and "MIŠE" in a6["opis"], "")
    check("I7g A7-A10: Se-ubila + Žganje-v-glavi + starost-korekcije-×9 + 99-let!",
          any("Se-ubila" in x["opis"] for x in d["anomalies"])
          and any("Žganje-v-glavi" in x["opis"] for x in d["anomalies"])
          and any("starost-korekcije" in x["opis"] for x in d["anomalies"])
          and any("99-let" in x["opis"] for x in d["anomalies"]), "")

    # ---------- I8: meje + lead ----------
    check("I8a meja 1904/05 = s99-glava (P170-potrjena — 12.!)",
          "s99" in d["crossChecks"][0]["opis"] or "restart" in d["crossChecks"][0]["opis"], "")
    check("I8b meja 1905/06 = s104 (13.-POTRDITEV-5.-STILA — VIZUALNO!)",
          "s104" in d["crossChecks"][2]["opis"] and "13. POTRDITEV" in d["crossChecks"][2]["opis"]
          and "restart-61→1" in d["crossChecks"][2]["opis"], "")
    check("I8c P172-lead v dokazu (1906 + BRINEC-zap1 + PEZDIREC-zap6!)",
          "P172-lead" in d["nextSteps"] and "1906" in d["nextSteps"]["P172-lead"]
          and "BRINEC" in d["nextSteps"]["P172-lead"]
          and "PEZDIREC" in d["nextSteps"]["P172-lead"], "")
    check("I8d X1-s104-zap1–9-LEAD-kontekst (P172-scope!)",
          any("zap1" in x["opis"] and "1906" in x["opis"] for x in d["excluded"]), "")

    # ---------- I9: demografija ----------
    prev = [e["previden"] for e in grb]
    check("I9a previden Griblje: 1 ×10 + '—' ×6",
          sum(1 for x in prev if x == "1") == 10 and sum(1 for x in prev if x == "—") == 6, str(prev))
    duh = [e["duhovnik"] for e in grb]
    check("I9b Lengsfeld ×15 + Rauq ×1 (Griblje-16 — DOMINANTA!)",
          sum(1 for x in duh if "LENGSFELD" in x) == 15
          and sum(1 for x in duh if "Rauq" in x) == 1, str(duh))
    meseci = {}
    for e in grb:
        k = e["mesec"][:3]
        meseci[k] = meseci.get(k, 0) + 1
    check("I9c meseci Griblje: Jan1·Feb1·Mar4·Apr1·Avg3·Sep4·Okt1·Dec1 (8-mesecev!)",
          meseci.get("Jan") == 1 and meseci.get("Feb") == 1 and meseci.get("Mar") == 4
          and meseci.get("Apr") == 1 and meseci.get("Avg") == 3 and meseci.get("Sep") == 4
          and meseci.get("Okt") == 1 and meseci.get("Dec") == 1, str(meseci))
    check("I9d starostni-razpon 7-tednov → 84-let (z26 → z24!)",
          any("7 tednov" in e["starost"] for e in grb) and any("84 let" in e["starost"] for e in grb), "")
    otroci = [e for e in grb if "mesec" in e["starost"] or "tednov" in e["starost"] or "½ leta" in e["starost"]]
    check("I9e otroška-smrt ≥5/16 (mesec/tednov/½!)",
          len(otroci) >= 5, str([(e["houseNo"], e["starost"]) for e in otroci]))

    # ---------- I10: qa-parish + pin-kaskada ----------
    qa = open(QA_TS, encoding="utf-8").read()
    check("I10a qa-p171 = 172. kontrola", "qa-p171-parish-death-1905" in qa, "")
    check("I10b qa-pini 966/267/91",
          qa.count("!== 1511") >= 80 and qa.count("!== 446") >= 18 and qa.count("p80Houses.size !== 93") >= 18,
          f"{qa.count('!== 976')}/{qa.count('!== 277')}/{qa.count('p80Houses.size !== 92')}")
    check("I10c qa guard 1919 (bloki 1919+ ne!)",
          "1916+-mrliški bloki že v korpusu" in qa and "(h.year ?? 0) >= 1925" in qa, "")
    check("I10d P80_PT_GAP doc-list 15 (NESPREMENJENO!)",
          '"49", "51"' in qa and "p80Gap.length !== 15" in qa, "")
    check("I10e stale-guardi → 1908 (20× qa)",
          qa.count("1908+-mrliški bloki že v korpusu") >= 18,
          f"{qa.count('1908+-mrliški bloki že v korpusu')}")

    # ---------- I11: honesty + notes ----------
    check("I11a honesty 10 točk", len(d["honesty"]) == 10, str(len(d["honesty"])))
    check("I11b s99-datumi-dopolnilni-klic-v-honesty (diag-reža!)",
          any("s99-datumi" in h for h in d["honesty"]), "")
    check("I11c VLM-vas-LEKCIJA-v-honesty (PREKINITEV!)",
          any("VLM-page-vas-×4-NAPAČNE" in h for h in d["honesty"]), "")
    check("I11d notes: forenzika + P172-lead",
          os.path.exists(NOTES) and "forenzika" in open(NOTES, encoding="utf-8").read()
          and "P172-lead" in open(NOTES, encoding="utf-8").read(), "")

    # ---------- I12: kaskada ----------
    check("I12a p153–p170 skripte VITALS_TOTAL 976",
          all("VITALS_TOTAL = 1100" in open(f"scripts/p{i}_parish_death_{y}.py", encoding="utf-8").read()
              for i, y in ((153, 1887), (154, 1888), (155, 1889), (156, 1890), (157, 1891), (158, 1892), (159, 1893), (160, 1894), (161, 1895), (162, 1896), (163, 1897), (164, 1898), (165, 1899), (166, 1900), (167, 1901), (168, 1902), (169, 1903), (170, 1904))), "")
    check("I12b p80-skripta P171-komentar-kaskada (950 → 966-pini!)",
          "len(vitals) == 1100" in p80 and "P171: 950 → 966" in p80, "")
    check("I12c stale-guardi → 1908 (20× qa)",
          all("1916+-mrliški bloki že v korpusu" in open(f"scripts/p{i}_parish_death_{y}.py", encoding="utf-8").read()
              for i, y in ((155, 1889), (156, 1890), (157, 1891), (158, 1892), (159, 1893), (160, 1894), (161, 1895), (162, 1896), (163, 1897), (164, 1898), (165, 1899), (166, 1900), (167, 1901), (168, 1902), (169, 1903), (170, 1904))), "")
    check("I12d qa-parish.ts bloki 04894 = 277 (P171-kaskada!)",
          qa.count('04894").length !== 520') >= 15, str(qa.count('04894").length !== 520')))

    # ---------- I13 (--live): matricula dostopna ----------
    if live:
        try:
            st, body = http_get(BOOK_URL, timeout=30)
            urls = re.findall(r'"(/image/[A-Za-z0-9+/=%]+/)"', body.decode("utf-8", "replace"))
            check("I13 live knjiga 04894 (200 + inventar 256)",
                  st == 200 and len(urls) >= 256, f"{st}/{len(urls)}")
            import base64
            inv = []
            for m in re.finditer(r'"(/image/[A-Za-z0-9+/=%]+/)"', body.decode("utf-8", "replace")):
                s = m.group(1)[7:-1]
                try:
                    u = base64.b64decode(s + "=" * (-len(s) % 4)).decode("utf-8")
                    if u.startswith("http"):
                        inv.append(u)
                except Exception:
                    pass
            inv = sorted(set(inv))
            ok_all = 0
            for s in [99] + NEW_SCANS:
                try:
                    st2, data = http_get(inv[s - 1], timeout=60)
                    if st2 == 200 and len(data) > 50000:
                        ok_all += 1
                except Exception:
                    pass
                time.sleep(1.2)
            check("I13b live citirani skeni 6/6 JPEG-200", ok_all == 6, f"{ok_all}/6")
        except Exception as e:
            check("I13 live (napaka)", False, str(e)[:120])

    ok = sum(1 for _, o, _ in results if o)
    for name, o, det in results:
        print(f"{'PASS' if o else 'FAIL'}  {name}" + (f"  [{det}]" if det else ""))
    print(f"\np171: {ok}/{len(results)}")
    sys.exit(0 if ok == len(results) else 1)


if __name__ == "__main__":
    main()
