#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P170 — verifikator MRLIŠKE knjige 04894, leto 1904 (18. → 19. polno leto).
Celoten neodvisen preracun iz bundled parish.ts + dokaz-JSON + qa + kaskada.
I-checki I1–I13 (vzorec P153–P169); --live = dodatna HTTP verifikacija
matricula-online.eu.
P170-rekordi: 47 vpisov / 12 GRIBLJE / 12 hiš (BREZ ×2!) = PADEC-po-2-rekordih
(rast 10→17→17→12!) + 5 GLAVE-NAPAKE = NOVI REKORD LINIJE (P169-3 → P170-5!)
+ PEZDIREC-×3-1904 = era-13 (×9-v-3-letih!) + h63 = 1. mrliški = 28. PT-vez +
h66 = 2. mrliški = 26.-PT-kontinuiteta + NOVI DUHOVNIK #12 Hugo LENGSFELD
(od-oktobra-1904!) + NEKOMPLETEN-TRIPLI-1.-v-liniji (z42!) + DIAG-METODA-NOVO
(vizualni-gridi-z-Read-očmi!) + GLAVA-HALUCINACIJA-LEKCIJA.
Kumulativ: vitals 938 → 950, mrliški bloki 04894 239 → 251, p80 hiše 91
NESPREMENJENE (vseh-12-ŽE-v-p80!), korpus 93 NESPREMENJEN, PT 28 → 29."""
import json, os, re, sys, time, urllib.request, urllib.error

DOKAZ = "research/issue17/parish-death-1904.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
QA_TS = "src/lib/qa-parish.ts"
PARISH_TS = "src/data/atlas/parish.ts"
NOTES = "research/issue17/parish-death-1904-notes.md"

EXPECTED_ENTRIES = 47   # 12 Griblje + 35 ne-Griblje (s-*!)
EXPECTED_EXCLUDED = 7
EXPECTED_ANOMALIES = 10
EXPECTED_CROSSCHECKS = 5
GRIBLJE_HOUSES = "1,2,14,31,34,35,48,58,62,63,66,91"
VITALS_TOTAL = 950               # 938 + 12!
BLOKI_04894 = 251                # 239 + 12!
P80_HOUSES = 91                  # NESPREMENJENO (vseh-12-ŽE-v-p80!)
KORPUS_HOUSES = 93               # NESPREMENJENO
NEW_SCANS = [95, 96, 97, 98]

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


def e_hn(grb, hn):
    return next(e for e in grb if e["houseNo"] == hn)


def main():
    live = "--live" in sys.argv
    d = json.load(open(DOKAZ, encoding="utf-8"))
    ent = d["entries"]
    fr = d["frame"]
    # Griblje-podmnožica (ne-Griblje-vpisi-imajo-'*'-v-houseNo — cf. excluded!)
    grb = [e for e in ent if not e["houseNo"].endswith("*")]

    # ---------- I1: dokaz ----------
    check("I1 dokaz obstaja + status", d["status"] == "SAMPLE-TRANSCRIPTION-D1904", d["status"])
    check("I1b 47 vnosov (12-Griblje + 35-ne-Griblje-s-*!)", len(ent) == EXPECTED_ENTRIES, str(len(ent)))
    check("I1c 7 excluded / 10 anomalij / 5 križnih",
          len(d["excluded"]) == EXPECTED_EXCLUDED and len(d["anomalies"]) == EXPECTED_ANOMALIES
          and len(d["crossChecks"]) == EXPECTED_CROSSCHECKS,
          f"{len(d['excluded'])}/{len(d['anomalies'])}/{len(d['crossChecks'])}")

    # ---------- I2: okvir ----------
    check("I2 1904 = 47 vrstic / 12 Griblje / 12 hiš (PADEC-po-2-rekordih!)",
          fr["vrstic"] == 47 and fr["griblje_vpisi"] == 12 and fr["hise"] == 12,
          f"{fr['vrstic']}/{fr['griblje_vpisi']}/{fr['hise']}")
    check("I2b Griblje 10→17→17→12 (PADEC!) + 5 GLAVE-NAPAKE-REKORD",
          "10→17→17→12" in fr["rast"] and "5-GLAVE-NAPAKE" in fr["rekordi"]
          and "PEZDIREC" in fr["rekordi"], fr["rekordi"][:90])
    check("I2c hiše = 12 različnih (BREZ ×2-Griblje — padec-po-×2-letih!)",
          ",".join(str(e["houseNo"]) for e in sorted(grb, key=lambda x: int(x["houseNo"]))) == GRIBLJE_HOUSES,
          ",".join(e["houseNo"] for e in sorted(grb, key=lambda x: int(x["houseNo"]))))

    # ---------- I3: zap-continuity (ČISTO leto!) ----------
    zaps = sorted(int(e["zap"]) for e in grb)
    check("I3a Griblje-zap: 3,8,10,14,15,16,18,24,26,33,38,45",
          zaps == [3, 8, 10, 14, 15, 16, 18, 24, 26, 33, 38, 45], str(zaps))
    check("I3b zapcol-ČIST (47-oštevilčenih / 47-fizičnih)",
          fr["zap_oštevilčenih"] == 47 and fr["neštevilčenih"] == 0, "")

    # ---------- I4: invarianta ----------
    check("I4 stran == sken − 1 (vseh 12 — 67.–71. potrditev!)",
          all(e["page"] == e["scan"] - 1 for e in ent), "")
    check("I4b skeni v naboru 94–98 (s94-dno-reuse + s95–s98!)",
          all(e["scan"] in [94] + NEW_SCANS for e in ent), str(sorted({e["scan"] for e in ent})))

    vit = parse_house_vitals()
    d04894 = [v for v in vit if v["bookSignature"] == "04894"]
    d1904 = [v for v in d04894 if v["year"] == 1904]

    # ---------- I5: hišne veze (parish.ts-whatSi-long-forme!) ----------
    def v_hn(vlist, hn):
        return next(v for v in vlist if v["houseNo"] == hn)
    e63 = v_hn(d1904, "63")
    check("I5a h63 = 1. MRLIŠKI VPIS KADARKOLI = 28. PT-vez + MARGINALIJA!",
          "1. MRLIŠKI VPIS KADARKOLI" in e63["whatSi"]
          and "28. PT-vezni dokaz" in e63["whatSi"] and "MARGINALIJA" in e63["whatSi"], "")
    e66 = v_hn(d1904, "66")
    check("I5b h66 = 2. MRLIŠKI VPIS = 26.-PT-kontinuiteta (1. = P168-1902!)",
          "2. MRLIŠKI VPIS" in e66["whatSi"] and "26.-PT-vezni-dokaz" in e66["whatSi"], "")
    e48 = v_hn(d1904, "48")
    check("I5c h48-Katarina = PEZDIREC-×3-1904-#1 (super-×5-ime!)",
          "PEZDIREC" in e48["whatSi"] and "PEZDIREC-×3-1904-#1" in e48["whatSi"]
          and "Cudriec" in e48["whatSi"], "")
    e14v = v_hn(d1904, "14")
    check("I5d h14-Ana = PEZDIREC-×3-1904-#3 + ZADNJA-GRIBLJE (meja-12.!) — era-13!",
          "PEZDIREC" in e14v["whatSi"] and "PEZDIREC-×3-1904-#3" in e14v["whatSi"]
          and "ZADNJA-GRIBLJE-1904" in e14v["whatSi"] and "12. POTRDITEV" in e14v["whatSi"], "")
    e31 = v_hn(d1904, "31")
    check("I5e h31-hišna-forenzika-×6 = 31-NE-37 (kalibracija-z13-'31'-ISTA-forma!)",
          "hišna-forenzika-×6-'31'" in e31["whatSi"] and "3-glasa-NAPAČNO" in e31["whatSi"], "")
    e58 = v_hn(d1904, "58")
    check("I5f h58-Ivana = PRVI-GRIBLJE-1904 (P169-lead-'Puček?'-POTRJEN!)",
          "PRVI-GRIBLJE-1904" in e58["whatSi"] and "PUČEK" in e58["whatSi"], "")
    e1 = v_hn(d1904, "1")
    check("I5g h1-ŽELEZNIK-71 = NAJNIŽJA-hiša-mrliška (1889+1890+1904 — 3. vpis!)",
          "NAJNIŽJA-hiša" in e1["whatSi"] and "ŽELEZNIK" in e1["whatSi"], "")
    check("I5h h62 + h34 + h91 + h2 + h35 = kontinuitete (4.–5.–2.–4. vpis!)",
          "KUREC" in v_hn(d1904, "62")["whatSi"] and "ČIŠLAK" in v_hn(d1904, "34")["whatSi"]
          and "MRAVINEC" in v_hn(d1904, "91")["whatSi"] and "ZAPIČ" in v_hn(d1904, "2")["whatSi"]
          and "ŠIMEC" in v_hn(d1904, "35")["whatSi"], "")
    check("I5i Lengsfeld-×2-Griblje (h66 + h14 — od-oktobra-1904!)",
          "LENGSFELD" in e66["whatSi"] and "LENGSFELD" in e14v["whatSi"]
          and "#12" in e66["whatSi"], "")

    # ---------- I6: kumulativ + parish.ts ----------
    vit = parse_house_vitals()
    d04894 = [v for v in vit if v["bookSignature"] == "04894"]
    check("I6a vitals 950", len(vit) == VITALS_TOTAL, str(len(vit)))
    check("I6b mrliški bloki 04894 = 251", len(d04894) == BLOKI_04894, str(len(d04894)))
    d1904 = [v for v in d04894 if v["year"] == 1904]
    check("I6c bloki 1904 = 12", len(d1904) == 12, str(len(d1904)))
    check("I6d bloki 1904: skeni 94–98 + stran == sken − 1",
          all(v["scan"] and 94 <= v["scan"] <= 98 and v["page"] == v["scan"] - 1 for v in d1904), "")
    check("I6d2 bloki 1905+ ne obstajajo (P171-lead!; P170 = 1904 sedaj v korpusu!)",
          all(v["year"] < 1905 for v in d04894), "")
    p80 = open("scripts/p80_parish_md_books.py", encoding="utf-8").read()
    check("I6f p80-skripta pini 950 + 91 + gap-18 (vitals-P170-kaskada!)",
          "len(vitals) == 950" in p80 and "len(houses) == 91" in p80 and "len(gap) == 18" in p80, "")
    houses_all = {v["houseNo"] for v in vit if v["houseNo"].isdigit()}
    check("I6g korpus = 93 hiš (NESPREMENJENO — vseh-12-hiš-ŽE-v-korpusu!)",
          len(houses_all) == KORPUS_HOUSES, str(len(houses_all)))

    # ---------- I7: forenzika (DIAG-METODA + GLAVA-HALUCINACIJA!) ----------
    a1 = next(x for x in d["anomalies"] if x["id"] == "A1")
    check("I7a A1: 5-GLAVE-NAPAKE-REKORD (18/904 + 18/94 + 18904 ×2 + 18905!)",
          "5 GLAVE-NAPAKE" in a1["opis"] and "18904" in a1["opis"] and "18905" in a1["opis"], "")
    a2 = next(x for x in d["anomalies"] if x["id"] == "A2")
    check("I7b A2: PEZDIREC-era-13-×9-v-3-letih (z33+z37+z45 + 1905-lead!)",
          "era-13" in a2["opis"] and "×9-v-3-letih" in a2["opis"], "")
    a3 = next(x for x in d["anomalies"] if x["id"] == "A3")
    check("I7c A3: NEKOMPLETEN-TRIPLI-1.-v-liniji (z42-3×-PRAZNO!)",
          "NEKOMPLETEN-TRIPLI" in a3["opis"] and "3×-PRAZNO" in a3["opis"], "")
    a4 = next(x for x in d["anomalies"] if x["id"] == "A4")
    check("I7d A4: NOVI-DUHOVNIK-#12-LENGSFELD (L-ne-D!; alternacija!)",
          "LENGSFELD" in a4["opis"] and "L-ne-D" in a4["opis"]
          and "alternacija" in a4["opis"], "")
    check("I7e VLM-vas-0-napak-4.-leto (12/12-Griblje-vizualno!)",
          any("VLM-vas-0-napak-4.-leto" in h for h in d["honesty"]), "")
    check("I7f GLAVA-HALUCINACIJA-LEKCIJA-v-honesty (interpretacija-NE-ZANESLJIVA!)",
          any("HALUCINACIJA" in h and "interpretacija" in h for h in d["honesty"]), "")

    # ---------- I8: meje + lead ----------
    check("I8a meja 1903/04 = s94-row9 (P169-potrjena — 11.!)",
          "s94" in d["crossChecks"][1]["opis"] and "11. POTRDITEV" in d["crossChecks"][1]["opis"], "")
    check("I8b meja 1904/05 = s99-glava (12.-POTRDITEV-5.-STILA!)",
          "s99" in d["crossChecks"][1]["opis"] and "12. POTRDITEV" in d["crossChecks"][1]["opis"], "")
    check("I8c P171-lead v dokazu (1905 + PEZDIREC-z1-h59!)",
          "P171-lead" in d["nextSteps"] and "1905" in d["nextSteps"]["P171-lead"]
          and "PEZDIREC" in d["nextSteps"]["P171-lead"], "")
    e7 = next(x for x in d["excluded"] if x["id"] == "E7")
    check("I8d E7-s99-kontekst (zap1–12-1905 + P171!)",
          "zap1–12" in e7["opis"] or "zap1-12" in e7["opis"], "")

    # ---------- I9: demografija ----------
    prev = [e["previden"] for e in grb]
    check("I9a previden: 1 ×6 + '—' ×6 (Griblje-12)",
          prev.count("1") == 6 and prev.count("—") == 6, str(prev))
    duh = [e["duhovnik"] for e in grb]
    check("I9b Dostál ×8 + Rauq ×2 + Lengsfeld ×2 (Griblje-12 — tranzicija!)",
          sum(1 for x in duh if "Dostál" in x) == 8
          and sum(1 for x in duh if "Rauq" in x) == 2
          and sum(1 for x in duh if "LENGSFELD" in x) == 2, str(duh))
    meseci = {}
    for e in grb:
        k = e["mesec"][:3]
        meseci[k] = meseci.get(k, 0) + 1
    check("I9c meseci Griblje: Jan1·Feb1·Mar1·Apr3·Maj1·Jul2·Sep1·Okt1·Dec1 (8-mesecev!)",
          meseci.get("Jan") == 1 and meseci.get("Feb") == 1 and meseci.get("Mar") == 1
          and meseci.get("Apr") == 3 and meseci.get("Maj") == 1 and meseci.get("Jul") == 2
          and meseci.get("Sep") == 1 and meseci.get("Okt") == 1 and meseci.get("Dec") == 1, str(meseci))
    check("I9d starostni-razpon 1-mesec → 79-let (z33/z48-Katarina → z10-Ana!)",
          any("1 mesec" in e["starost"] for e in grb) and any("79 let" in e["starost"] for e in grb), "")
    otroci = [e for e in grb if "mesec" in e["starost"] or "leta" in e["starost"] or "leti" in e["starost"]]
    check("I9e otroška-smrt ≥5/12 (mesec/leti/mesece!)",
          len(otroci) >= 5, str([(e["houseNo"], e["starost"]) for e in otroci]))

    # ---------- I10: qa-parish + pin-kaskada ----------
    qa = open(QA_TS, encoding="utf-8").read()
    check("I10a qa-p170 = 171. kontrola", "qa-p170-parish-death-1904" in qa, "")
    check("I10b qa-pini 950/251/91",
          qa.count("!== 950") >= 80 and qa.count("!== 251") >= 15 and qa.count("p80Houses.size !== 91") >= 18,
          f"{qa.count('!== 950')}/{qa.count('!== 251')}/{qa.count('p80Houses.size !== 91')}")
    check("I10c qa guard 1905 (bloki 1905+ ne!)",
          "1905+-mrliški bloki že v korpusu" in qa and "(h.year ?? 0) >= 1905" in qa, "")
    check("I10d P80_PT_GAP doc-list 15 (NESPREMENJENO!)",
          '"49", "51"' in qa and "p80Gap.length !== 15" in qa, "")
    check("I10e stale-guardi → 1905 (17× qa)",
          qa.count("1905+-mrliški bloki že v korpusu") >= 15,
          f"{qa.count('1905+-mrliški bloki že v korpusu')}")

    # ---------- I11: honesty + notes ----------
    check("I11a honesty 10 točk", len(d["honesty"]) == 10, str(len(d["honesty"])))
    check("I11b DIAG-METODA-v-honesty (vizualni-gridi-Read-oči!)",
          "DIAG-METODA" in d["honesty"][0] and "Read" in d["honesty"][0], "")
    check("I11c GLAVA-HALUCINACIJA-lekcija (interpretacija-NE-ZANESLJIVA!)",
          "HALUCINACIJA" in d["honesty"][1], "")
    notes = open(NOTES, encoding="utf-8").read()
    check("I11d notes: forenzika + P171-lead",
          "forenzika" in notes and "P171-lead" in notes, "")

    # ---------- I12: kaskada ----------
    check("I12a p153–p169 skripte VITALS_TOTAL 950",
          all("VITALS_TOTAL = 950" in open(f"scripts/p{i}_parish_death_{y}.py", encoding="utf-8").read()
              for i, y in ((153, 1887), (154, 1888), (155, 1889), (156, 1890), (157, 1891), (158, 1892), (159, 1893), (160, 1894), (161, 1895), (162, 1896), (163, 1897), (164, 1898), (165, 1899), (166, 1900), (167, 1901), (168, 1902), (169, 1903))), "")
    check("I12b p80-skripta P169-komentar-kaskada (938 → 950-pini!)",
          "len(vitals) == 950" in p80, "")
    check("I12c stale-guardi → 1905 (14 skript-s-qa-stringom!)",
          all("1905+-mrliški bloki že v korpusu" in open(f"scripts/p{i}_parish_death_{y}.py", encoding="utf-8").read()
              for i, y in ((155, 1889), (156, 1890), (157, 1891), (158, 1892), (159, 1893), (160, 1894), (162, 1896), (163, 1897), (164, 1898), (165, 1899), (166, 1900), (167, 1901), (168, 1902), (169, 1903))), "")
    check("I12d qa-parish.ts bloki 04894 = 251 (P170-kaskada!)",
          qa.count('04894").length !== 251') >= 15, str(qa.count('04894").length !== 251')))

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
            for s in [94] + NEW_SCANS:
                try:
                    st2, data = http_get(inv[s - 1], timeout=60)
                    if st2 == 200 and len(data) > 50000:
                        ok_all += 1
                except Exception:
                    pass
                time.sleep(1.2)
            check("I13b live citirani skeni 5/5 JPEG-200", ok_all == 5, f"{ok_all}/5")
        except Exception as e:
            check("I13 live (napaka)", False, str(e)[:120])

    ok = sum(1 for _, o, _ in results if o)
    for name, o, det in results:
        print(f"{'PASS' if o else 'FAIL'}  {name}" + (f"  [{det}]" if det else ""))
    print(f"\np170: {ok}/{len(results)}")
    sys.exit(0 if ok == len(results) else 1)


if __name__ == "__main__":
    main()
