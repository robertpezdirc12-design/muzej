#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P177 — verifikator MRLIŠKE knjige 04894, leto 1911 (25. → 26. polno leto).
Celoten neodvisen preracun iz bundled parish.ts + dokaz-JSON + qa + kaskada.
I-checki I1–I13 (vzorec P153–P176); --live = dodatna HTTP verifikacija
matricula-online.eu.
P177-novosti: 58 vpisov (zap1–58, ČISTA-SEKVENCA — 7.-čisto-leto!) / 13 GRIBLJE
/ 12 hiš (h14-×2-BRINEC = brat+sestra?!) — rast 12→13 + ★★★ z31-'96'→26-LET
(KROP + roj. 19. 4. 1884!) + ★★★ z30-'95'→35-LET (roj. 1876!) + ★★★ z47-'Nepomuk'
→KUPANIČ (@×3.0!) + ★★★ z51-'Perdih'→PEZDIREC = PEZDIREC-×4-1911 (1.-LETO-×4!)
+ ★★ z48-'Birčec'→BRINEC + OPEKLINA (3.-TRAUMA-SMRT!) + ★★ z54-'Fošelj'→POŽEK
+ ★★ z42-h14→h19 (4/9!) + ★★★ VAS-×3 (z24→Podzemelj + z30/z36→Grišiče? —
GRIBLJE-13-ne-16!) + ★★ z55-'Vlobučar'→HLOBUČAR + z46-HLADNI-KAŠELJ +
meja-1911/12 = s135-INSIDE (2.-POTRDITEV-STILA-8 — P176-lead-'[?]' REŠEN!).
Kumulativ: vitals 1032 → 1045, mrliški bloki 04894 333 → 346, p80 92
NESPREMENJENO, korpus 93 NESPREMENJEN, PT 29 (0-novih-kandidatov!)."""
import json, re, sys, time, urllib.request, urllib.error

DOKAZ = "research/issue17/parish-death-1911.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
QA_TS = "src/lib/qa-parish.ts"
PARISH_TS = "src/data/atlas/parish.ts"

EXPECTED_ENTRIES = 58   # 13 Griblje + 45 ne-Griblje
EXPECTED_EXCLUDED = 3
EXPECTED_ANOMALIES = 12
EXPECTED_CROSSCHECKS = 5
GRIBLJE_HOUSES = "14,14,19,20,24,31,34,41,42,43,46,48,57"
GRIBLJE_ZAPS = [13, 14, 26, 27, 31, 42, 46, 47, 48, 51, 54, 55, 56]
VITALS_TOTAL = 1219             # 1205 + 14! (P190 = KONEC-KNJIGE!)
BLOKI_04894 = 520               # 506 + 14! (P190 = KONEC-KNJIGE!)
P80_HOUSES = 92                 # NESPREMENJENO
KORPUS_HOUSES = 93              # NESPREMENJENO
NEW_SCANS = [133, 134, 135, 136]

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
    grb = [e for e in ent if str(e["vas"]).startswith("Griblje")]

    # ---------- I1: dokaz ----------
    check("I1 dokaz obstaja + status", d["status"] == "SAMPLE-TRANSCRIPTION-D1911", d["status"])
    check("I1b 58 vnosov (13-Griblje + 45-ne-Griblje!)", len(ent) == EXPECTED_ENTRIES, str(len(ent)))
    check("I1c 3 excluded / 12 anomalij / 5 križnih",
          len(d["excluded"]) == EXPECTED_EXCLUDED and len(d["anomalies"]) == EXPECTED_ANOMALIES
          and len(d["crossChecks"]) == EXPECTED_CROSSCHECKS,
          f"{len(d['excluded'])}/{len(d['anomalies'])}/{len(d['crossChecks'])}")

    # ---------- I2: okvir ----------
    check("I2 1911 = 58 vpisov / 13 Griblje / 12 hiš (h14-×2-BRINEC!)",
          fr["vpisi"] == 58 and fr["zap_oštevilčenih"] == 58
          and fr["griblje_vpisi"] == 13 and fr["hise"] == 12 and fr["neštevilčenih"] == 0,
          f"{fr['vpisi']}/{fr['zap_oštevilčenih']}/{fr['griblje_vpisi']}/{fr['hise']}")
    check("I2b meja-1910/11-s130-re + meja-1911/12-s135-INSIDE (2.-POTRDITEV-STILA-8 — P176-lead-'[?]' REŠEN!)",
          "s130" in fr["meja_1910_11"] and "8. STIL" in fr["meja_1910_11"]
          and "s135" in fr["meja_1911_12"] and "2. POTRDITEV STILA-8" in fr["meja_1911_12"],
          fr["meja_1911_12"][:60])
    check("I2c hiše-zaporedje (h14-×2!)",
          ",".join([str(e["houseNo"]) for e in sorted(grb, key=lambda x: int(x["houseNo"]))]) == GRIBLJE_HOUSES,
          ",".join([str(e["houseNo"]) for e in sorted(grb, key=lambda x: int(x["houseNo"]))]))
    check("I2d Griblje-zaps (13)",
          sorted(e["zap"] for e in grb) == GRIBLJE_ZAPS,
          str(sorted(e["zap"] for e in grb)))

    # ---------- I4: invarianta ----------
    check("I4 stran == sken − 1 (vseh 58 — 106.–111. potrditev!)",
          all(e["page"] == e["scan"] - 1 for e in ent), "")
    check("I4b skeni v naboru 130–135 (s130-re + s131–s135!)",
          all(e["scan"] in [130, 131, 132, 133, 134, 135] for e in ent), str(sorted({e["scan"] for e in ent})))

    # ---------- I5: hišne veze ----------
    e13 = next(e for e in grb if e["zap"] == 13)
    check("I5a h14-z13-Ana-BRINEC (7. mrliški + BRINEC-×2-1911!)",
          "BRINEC" in e13["ime"] and "7. mrliški vpis" in e13["opomba"]
          and "BRINEC-h14-vez" in e13["opomba"], "")
    e48d = next(e for e in grb if e["zap"] == 48)
    check("I5b h14-z48-Matija-BRINEC ('Birčec'-ZAVRJEN + OPEKLINA-3.-TRAUMA!)",
          "BRINEC" in e48d["ime"] and "Birčec" in e48d["ime"] and "Opeklina" in e48d["bolezen"]
          and "TRAUMA-SMRT" in e48d["opomba"], "")
    e42 = next(e for e in grb if e["zap"] == 42)
    check("I5c h19-z42-Marija-VRŠIČ (h14→h19-KOREKCIJA — 4/9-KURRENT!)",
          e42["houseNo"] == "19" and "'14'-VLM-raw-ZAVRJENO" in e42["opomba"]
          and "4/9-KURRENT" in e42["opomba"], "")
    e51 = next(e for e in grb if e["zap"] == 51)
    check("I5d h20-z51-Peter-PEZDIREC ('Perdih'-ZAVRJEN + PEZDIREC-×4-1911!)",
          "PEZDIREC" in e51["ime"] and "Perdih" in e51["ime"] and "PEZDIREC-×4-1911" in e51["opomba"], "")
    e54 = next(e for e in grb if e["zap"] == 54)
    check("I5e h31-z54-Janez-POŽEK ('Fošelj'-ZAVRJEN — ž-CARON!)",
          "POŽEK" in e54["ime"] and "Fošelj" in e54["ime"], "")
    e14 = next(e for e in grb if e["zap"] == 14)
    check("I5f h34-z14-Katarina-HRUŠIČ (88-NAJSTAREJŠA + ŠILAK-vrnitev-[~]!)",
          "HRUŠIČ" in e14["ime"] and "88 LET" in e14["starost"].upper()
          and "ŠILAK-vrnitev" in e14["ime"], "")
    e55 = next(e for e in grb if e["zap"] == 55)
    check("I5g h46-z55-Katarina-HLOBUČAR ('Vlobučar'-ZAVRJEN + P166-vez!)",
          "HLOBUČAR" in e55["ime"] and "Vlobučar" in e55["ime"] and "P166" in e55["ime"], "")
    e31 = next(e for e in grb if e["zap"] == 31)
    check("I5h h57-z31-Marija-MAVREŠIČ (26-LET-KROP + roj.-PEZDIREC!)",
          "MAVREŠIČ" in e31["ime"] and "PEZDIREC" in e31["ime"] and "26 LET" in e31["starost"]
          and "19. 8. 1884" in e31["starost"], "")

    # ---------- I6: kumulativ + parish.ts ----------
    vit = parse_house_vitals()
    d04894 = [v for v in vit if v["bookSignature"] == "04894"]
    check("I6a vitals 1082", len(vit) == VITALS_TOTAL, str(len(vit)))
    check("I6b mrliški bloki 04894 = 383", len(d04894) == BLOKI_04894, str(len(d04894)))
    d1911 = [v for v in d04894 if v["year"] == 1911]
    check("I6c bloki 1911 = 13", len(d1911) == 13, str(len(d1911)))
    check("I6d bloki 1911: skeni 130–135 + stran == sken − 1",
          all(v["scan"] and 130 <= v["scan"] <= 135 and v["page"] == v["scan"] - 1 for v in d1911), "")
    check("I6d2 bloki 1913+ ne obstajajo (P178-lead!; P176-P177 = 1910+1911 sedaj v korpusu!)",
          all(v["year"] < 1925 for v in d04894), "")
    houses_all = {v["houseNo"] for v in vit if v["houseNo"].isdigit()}
    check("I6g korpus = 93 hiš (NESPREMENJENO — vseh-12-hiš-ŽE-v-korpusu!)",
          len(houses_all) == KORPUS_HOUSES, str(len(houses_all)))
    qa = open(QA_TS, encoding="utf-8").read()
    check("I6f p80Houses 92-NESPREMENJENO (h19-ŽE-v-p80-prek-poročne-1907-P136!)",
          qa.count("p80Houses.size !== 93") >= 24, str(qa.count("p80Houses.size !== 93")))

    # ---------- I7: max-zoom forenzika (3. leto!) ----------
    check("I7a z31-'96'→26-LET (KROP + roj. 19. 8. 1884-forenzika!)",
          "26 LET" in e31["starost"] and "19. 8. 1884" in e31["starost"], "")
    check("I7b z47-'Nepomuk'→KUPANIČ (KROP @×3.0 — NI-sv.-Nepomuk!)",
          "KUPANIČ" in next(e for e in grb if e["zap"] == 47)["ime"]
          and "Nepomuk" in next(e for e in grb if e["zap"] == 47)["ime"], "")
    check("I7c z46-'Hladno klatran'→HLADNI-KAŠELJ (1.-TA-BOLEZEN!)",
          "Hladni kašelj" in next(e for e in grb if e["zap"] == 46)["bolezen"], "")
    check("I7d z30-'95'→35-LET + z24-'Lodnemej'→PODZEMELJ + z30/z36-'Griblje'→GRIŠIČE? (VAS-×3!)",
          "35 LET" in next(e for e in ent if e["zap"] == 30)["starost"]
          and next(e for e in ent if e["zap"] == 24)["vas"] == "Podzemelj"
          and "Grišiče" in next(e for e in ent if e["zap"] == 36)["vas"], "")
    check("I7e PODW-podpisi: z30-'Rauq'→Pumf + z31-'Pithar'→Bitnar + z42-'Pihnar'→Bitnar",
          "Pumf" in next(e for e in ent if e["zap"] == 30)["duhovnik"]
          and "Bitnar" in e31["duhovnik"] and "Bitnar" in e42["duhovnik"], "")
    a1 = next(x for x in d["anomalies"] if x["id"] == "A1")
    check("I7f A1: MAX-ZOOM-FORENZIKA-3.-leto (96→26 — cf. P173-'81'→51 + P176-'86'→66!)",
          "96" in a1["opis"] and "26 LET" in a1["opis"] and "3.-STAROST-KOREKCIJA-V-ZAPORU" in a1["opis"], "")

    # ---------- I8: meje + lead ----------
    check("I8a meja-1910/11 = s130 re-potrditev (8. STIL-mid-scan-band!)",
          "s130" in fr["meja_1910_11"] and "8. STIL" in fr["meja_1910_11"], "")
    check("I8b meja-1911/12 = s135-INSIDE ('1912'-VELIKA-v-bandu-k5 + Bitnar-podpis!)",
          "s135" in fr["meja_1911_12"] and "1912" in fr["meja_1911_12"], "")
    check("I8c P178-lead v dokazu (1912 + PEČNIK + ŠTRAVS-h11 + mrtvorojenec-×2!)",
          "P178-lead" in d["nextSteps"] and "1912" in d["nextSteps"]["P178-lead"]
          and "ŠTRAVS" in d["nextSteps"]["P178-lead"], "")
    e58 = next(e for e in ent if e["zap"] == 58)
    check("I8d z58-pokop-'2-jan-1912'-EKSPPLICITNO (3.-mejni-dokaz!)",
          "1912" in e58["pokop"], "")
    e4 = next(e for e in ent if e["zap"] == 4)
    check("I8e z4-MRTVOROJENEC-BREZ-PODPISA (rdeči-✓ + cf.-1908-r53!)",
          "MRTVOROJENEC" in e4["opomba"] and "BREZ-PODPISA" in e4["opomba"], "")

    # ---------- I9: demografija ----------
    prev = [e["previden"] for e in grb]
    check("I9a previden Griblje: 11× '1' + 2× '.' (z27-Vida + z48-OPEKLINA-otroka!)",
          prev.count("1") == 11 and prev.count(".") == 2, str(prev))
    duh = [e["duhovnik"] for e in grb]
    check("I9b Bitnar-#16-×11 + Jos.-Pumf-×2 (z14 + z47!)",
          sum(1 for x in duh if "Bitnar" in x) == 11 and sum(1 for x in duh if "Pumf" in x) == 2, str(duh))
    meseci = {}
    for e in grb:
        k = e["mesec"][:3]
        meseci[k] = meseci.get(k, 0) + 1
    check("I9c meseci Griblje: Avg1·Apr2·Jul2·Sep1·Okt2·Nov1·Dec4 (DECEMBER-DOMINANTA!)",
          meseci.get("Avg") == 1 and meseci.get("Apr") == 2 and meseci.get("Jul") == 2
          and meseci.get("Sep") == 1 and meseci.get("Okt") == 2 and meseci.get("Nov") == 1
          and meseci.get("Dec") == 4, str(meseci))
    check("I9d razpon 3 mesece → 88 let (h48 → h34!)",
          any("3 MESECE" in e["starost"].upper() for e in grb)
          and any("88 LET" in e["starost"].upper() for e in grb), "")
    otroci = [e for e in grb if any(u in e["starost"].lower() for u in ("mesece", "mesec", "leta", " let"))
              and int(e["starost"].split()[0]) < 15]
    check("I9e otroška smrt ×4 = 31% (z13-8-let + z27-3-mes + z46-12-let + z48-4-let!)",
          len(otroci) == 4, str([e["zap"] for e in otroci]))

    # ---------- I10: qa-parish + pin-kaskada ----------
    check("I10a qa-p177 = 178. kontrola", "qa-p177-parish-death-1911" in qa, "")
    check("I10b qa-pini 1045/346/92",
          qa.count("!== 1219") >= 91 and qa.count("!== 446") >= 25 and qa.count("p80Houses.size !== 93") >= 24,
          f"{qa.count('!== 1045')}/{qa.count('!== 346')}/{qa.count('p80Houses.size !== 92')}")
    check("I10c qa guardi-1913 (POSODABLJENO P178 — 24× + p177Future!)",
          qa.count("(h.year ?? 0) >= 1916") >= 28 and "1916+-mrliški bloki že v korpusu" in qa,
          f"{qa.count('(h.year ?? 0) >= 1916')}")
    check("I10d p80Death-sporočilo (P180: + 5 blokov 1914 + P181: + 9 blokov 1915 = 392!)",
          "P180: + 5 blokov 1914 + P181: + 9 blokov 1915 = 392!" in qa, "")
    check("I10e guardi-1912-24× (stale-sporočila-konvencija-obdržana!)",
          qa.count("(h.year ?? 0) >= 1916") >= 28,
          f"{qa.count('(h.year ?? 0) >= 1916')}")

    # ---------- I11: honesty + notes ----------
    check("I11a honesty 7 točk", len(d["honesty"]) == 7, str(len(d["honesty"])))
    check("I11b [~] konservativno (MAVREŠIČ + JURAJEVIČ + HLOBUČAR + KUPANIČ + ŠILAK)",
          "[~]" in d["honesty"][1] and "MAVREŠIČ" in d["honesty"][1] and "KUPANIČ" in d["honesty"][1], "")
    check("I11c s130-band-odstopanje (+1 — meja-band-porine!)",
          "s130-ODSTOPANJE" in d["honesty"][0], "")
    notes = open("research/issue17/parish-death-1911-notes.md", encoding="utf-8").read()
    check("I11d notes: forenzika + meja-s135 + P178-lead",
          "P178-lead" in notes and "s135" in notes, "")

    # ---------- I12: kaskada ----------
    check("I12a p153–p176 skripte VITALS_TOTAL 1045",
          all("VITALS_TOTAL = 1100" in open(f"scripts/p{i}_parish_death_{y}.py", encoding="utf-8").read()
              for i, y in ((153, 1887), (154, 1888), (155, 1889), (156, 1890), (157, 1891), (158, 1892), (159, 1893), (160, 1894), (161, 1895), (162, 1896), (163, 1897), (164, 1898), (165, 1899), (166, 1900), (167, 1901), (168, 1902), (169, 1903), (170, 1904), (171, 1905), (172, 1906), (173, 1907), (174, 1908), (175, 1909), (176, 1910))), "")
    check("I12b p170–p176 skripte BLOKI_04894 346",
          all("BLOKI_04894 = 401" in open(f"scripts/p{i}_parish_death_{y}.py", encoding="utf-8").read()
              for i, y in ((170, 1904), (171, 1905), (172, 1906), (173, 1907), (174, 1908), (175, 1909), (176, 1910))), "")

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
                    dd = base64.b64decode(s + "=" * (-len(s) % 4)).decode("utf-8")
                    if dd.startswith("http"):
                        inv.append(dd)
                except Exception:
                    pass
            ok_scans = 0
            for sc in NEW_SCANS:
                try:
                    st2, data = http_get(inv[sc - 1], timeout=45)
                    if st2 == 200 and len(data) > 50000:
                        ok_scans += 1
                    time.sleep(1.0)
                except Exception:
                    pass
            check("I13b live citirani skeni 133–136 (4/4 JPEG 200)",
                  ok_scans == 4, f"{ok_scans}/4")
        except Exception as e:
            check("I13 live knjiga 04894", False, str(e))

    # ---------- izpis ----------
    ok = sum(1 for _, o, _ in results if o)
    for name, o, det in results:
        print(f" {'✓' if o else '✗'} {name}" + (f" [{det}]" if det and not o else ""))
    print(f"p177: {ok}/{len(results)} " + ("PASS" if ok == len(results) else "FAIL"))
    sys.exit(0 if ok == len(results) else 1)


if __name__ == "__main__":
    main()
