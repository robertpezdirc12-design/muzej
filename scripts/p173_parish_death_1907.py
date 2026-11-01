#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P173 — verifikator MRLIŠKE knjige 04894, leto 1907 (21. → 22. polno leto).
Celoten neodvisen preracun iz bundled parish.ts + dokaz-JSON + qa + kaskada.
I-checki I1–I13 (vzorec P153–P172); --live = dodatna HTTP verifikacija
matricula-online.eu.
P173-novosti: 67 vpisov (zap1–67, ČISTA-SEKVENCA!) / 20 GRIBLJE = NOV-REKORD
LINIJE (rast 17→16→16→10→20!) / 18 hiš (h49-×2 + h10-×2 = PADEC-vzorec-4.-leto!)
+ 3 PISAR-DATUM-NAPAKE = 1.-TIPO-V-LINIJI (z18-'29.-Feb-1907'-NE-PRESTOPNO!
+ z55/z56-'31.-Sept'-×2-BATCH!) + 5 GLAVE-NAPAKE = REKORD-IZENAČEN-3.×
(s111-'181904'-NAPAČNO-LETO-NOV-VZOREC + s112-'18'-NEKOMPLETNA!) +
P172-'BRINEC-PAR-vez'-KOREKCIJA (z1 = Anton-BRODARIČ!) + h75/h10 = 1.-MRLIŠKI-
VPIS-KADARKOLI-×2 (30./31.-PT-kandidata!) + h65-8.-vpis-IZENAČUJE-h58 +
NOVI-DUHOVNIK-LILEK-'župnik-v.p.' + Nemaniš + Guido-KRUSCH-layman + CERAR-
DOMINANTA + VLM-korekcije-imen-×13 + bolezni-×4-→-KAŠEL + MEJA-1907/08 = s114
(15. POTRDITEV — P172-lead-'[~ s113+?]'-KOREKCIJA!).
Kumulativ: vitals 976 → 996, mrliški bloki 04894 277 → 297, p80 hiše 91 → 92
(+h75!), korpus 93 NESPREMENJEN, PT 29."""
import json, os, re, sys, time, urllib.request, urllib.error

DOKAZ = "research/issue17/parish-death-1907.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
QA_TS = "src/lib/qa-parish.ts"
PARISH_TS = "src/data/atlas/parish.ts"

EXPECTED_ENTRIES = 67   # 20 Griblje + 47 ne-Griblje
EXPECTED_EXCLUDED = 2
EXPECTED_ANOMALIES = 12
EXPECTED_CROSSCHECKS = 5
GRIBLJE_HOUSES = "1,10,10,11,14,19,21,25,28,31,32,49,49,52,60,65,74,75,87,91"
GRIBLJE_ZAPS = [1, 2, 4, 5, 9, 11, 13, 18, 27, 32, 36, 37, 39, 53, 55, 56, 57, 58, 63, 65]
VITALS_TOTAL = 1032             # 1020 + 12! (P176)
BLOKI_04894 = 333               # 321 + 12! (P176)
P80_HOUSES = 92                  # 91 + h75!
KORPUS_HOUSES = 93               # NESPREMENJENO (h75/h10-ŽE-v-korpusu!)
NEW_SCANS = [110, 111, 112, 113, 114]  # s109-reuse (P172-meja-lead!)

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
    check("I1 dokaz obstaja + status", d["status"] == "SAMPLE-TRANSCRIPTION-D1907", d["status"])
    check("I1b 67 vnosov (20-Griblje + 47-ne-Griblje!)", len(ent) == EXPECTED_ENTRIES, str(len(ent)))
    check("I1c 2 excluded / 12 anomalij / 5 križnih",
          len(d["excluded"]) == EXPECTED_EXCLUDED and len(d["anomalies"]) == EXPECTED_ANOMALIES
          and len(d["crossChecks"]) == EXPECTED_CROSSCHECKS,
          f"{len(d['excluded'])}/{len(d['anomalies'])}/{len(d['crossChecks'])}")

    # ---------- I2: okvir ----------
    check("I2 1907 = 67 vpisov / 20 Griblje / 18 hiš = NOV-REKORD (rast-17→16→16→10→20!)",
          fr["vpisi"] == 67 and fr["zap_oštevilčenih"] == 67
          and fr["griblje_vpisi"] == 20 and fr["hise"] == 18,
          f"{fr['vpisi']}/{fr['zap_oštevilčenih']}/{fr['griblje_vpisi']}/{fr['hise']}")
    check("I2b 3-PISAR-DATUM-NAPAKE (1.-TIPO!) + 5-GLAVE-NAPAKE (s111-'181904'!)",
          "29.-Februar" in d["anomalies"][0]["opis"] and len(fr["glave_napake"]) == 5
          and any("181904" in g for g in fr["glave_napake"]), str(len(fr["glave_napake"])))
    check("I2c hiše-zaporedje (h49-×2 + h10-×2!)",
          ",".join([str(e["houseNo"]) for e in sorted(grb, key=lambda x: int(x["houseNo"]))]) == GRIBLJE_HOUSES,
          ",".join([str(e["houseNo"]) for e in sorted(grb, key=lambda x: int(x["houseNo"]))]))

    # ---------- I3: zap-continuity ----------
    zaps = sorted(int(e["zap"]) for e in grb)
    check("I3a Griblje-zap: 1,2,4,5,9,11,13,18,27,32,36,37,39,53,55,56,57,58,63,65",
          zaps == GRIBLJE_ZAPS, str(zaps))
    check("I3b ČISTA-SEKVENCA zap1–67 (BREZ-predorov/DUPLIKATOV — nasprotje-1906!)",
          sorted(int(e["zap"]) for e in ent) == list(range(1, 68)), "")
    check("I3c neštevilčenih = 0", fr["neštevilčenih"] == 0, "")

    # ---------- I4: invarianta ----------
    check("I4 stran == sken − 1 (vseh 67 — 82.–87. potrditev!)",
          all(e["page"] == e["scan"] - 1 for e in ent), "")
    check("I4b skeni: s109-reuse + s110–s114 (6-skupaj!)",
          all(e["scan"] in [109] + NEW_SCANS for e in ent), str(sorted({e["scan"] for e in ent})))

    vit = parse_house_vitals()
    d04894 = [v for v in vit if v["bookSignature"] == "04894"]
    d1907 = [v for v in d04894 if v["year"] == 1907]

    def v_scan_zap(scan, ime_frag):
        return next((v for v in d1907 if v["scan"] == scan and ime_frag in v["whatSi"]), None)

    # ---------- I5: hišne veze (parish.ts-whatSi-long-forme!) ----------
    e49 = next(v for v in d1907 if v["houseNo"] == "49" and "BRODARIČ" in v["whatSi"] and "66 LET" in v["whatSi"])
    check("I5a h49-Anton-BRODARIČ = P172-'BRINEC-PAR-vez'-KOREKCIJA (kompozit-×4!)",
          "KOREKCIJA" in e49["whatSi"] and "BRODARIČ" in e49["whatSi"]
          and "P172-'BRINEC-PAR-vez'-KOREKCIJA" in e49["whatSi"], "")
    e91 = next(v for v in d1907 if v["houseNo"] == "91")
    check("I5b h91-Ana-MUC = P172-lead-'MEC'-KOREKCIJA (h91-MUC-×-KURE-genetska!)",
          "MUC" in e91["whatSi"] and "KOREKCIJA" in e91["whatSi"]
          and "MUC-×-KURE" in e91["whatSi"], "")
    e75 = next(v for v in d1907 if v["houseNo"] == "75")
    check("I5c h75-Matija-ŠIMEC = 1. MRLIŠKI VPIS KADARKOLI (30.-PT-kandidat!)",
          "1. MRLIŠKI VPIS KADARKOLI" in e75["whatSi"] and "30.-PT-vezni-kandidat" in e75["whatSi"], "")
    e10a = next(v for v in d1907 if v["houseNo"] == "10" and "4 DNI" in v["whatSi"])
    check("I5d h10-Anton-BRINEC = 1. MRLIŠKI VPIS KADARKOLI (31.-PT-kandidat!)",
          "1. MRLIŠKI VPIS KADARKOLI" in e10a["whatSi"] and "31.-PT-vezni-kandidat" in e10a["whatSi"], "")
    e10b = next(v for v in d1907 if v["houseNo"] == "10" and "11 DNI" in v["whatSi"])
    check("I5e h10-×2-v-1-letu (z63-Anton-4-dni + z65-Jožef-11-dni = 6-DNI-APART!)",
          "×2-v-1-letu" in e10b["whatSi"] and "BRINEC-×3-v-1907" in e10b["whatSi"], "")
    e65 = next(v for v in d1907 if v["houseNo"] == "65")
    check("I5f h65-Matija-MILEK = 8. mrliški vpis-IZENAČUJE-REKORDISTKO-h58 (VLM-'Mlek'-ZAVRJENA!)",
          "8. mrliški vpis" in e65["whatSi"] and "IZENAČUJE-REKORDISTKO-h58" in e65["whatSi"]
          and "MILEK" in e65["whatSi"] and "Mlek" in e65["whatSi"], "")
    e60 = next(v for v in d1907 if v["houseNo"] == "60")
    check("I5g h60-Anton-ŽELJKO = VLM-'Veliko'-ZAVRJENA + ŽELJKO-genetska (h60!)",
          "ŽELJKO" in e60["whatSi"] and "Veliko" in e60["whatSi"]
          and "ŽELJKO-h60-GENETSKA" in e60["whatSi"], "")
    e52 = next(v for v in d1907 if v["houseNo"] == "52")
    check("I5h h52-Marija-roj.-NOVAK = VLM-'pri-Jovanek/POVH'-ZAVRJENA (PEZDIREC-h52-vez!)",
          "NOVAK" in e52["whatSi"] and "pri-Jovanek" in e52["whatSi"]
          and "PEZDIREC-h52-vez" in e52["whatSi"], "")
    e32 = next(v for v in d1907 if v["houseNo"] == "32")
    check("I5i h32-Matija-URH = PISAR-DATUM-NAPAKA-1/3 (29.-Feb-1907-NE-PRESTOPNO!)",
          "URH" in e32["whatSi"] and "PISAR-DATUM-NAPAKA-1/3" in e32["whatSi"]
          and "29. 2." in e32["whatSi"], "")
    e19 = next(v for v in d1907 if v["houseNo"] == "19")
    check("I5j h19-Ana-KRIŽE = PISAR-DATUM-NAPAKA-2/3 (31.-Sept!) + KRIŽE-kontinuiteta",
          "KRIŽE" in e19["whatSi"] and "PISAR-DATUM-NAPAKA-2/3" in e19["whatSi"]
          and "KRIŽE-h19-KONTINUITETA" in e19["whatSi"], "")
    e14 = next(v for v in d1907 if v["houseNo"] == "14")
    check("I5k h14-Marija-ŠTRMEC = BRINEC-genetska (krstna-1908-h14!)",
          "ŠTRMEC" in e14["whatSi"] and "h14-BRINEC-genetska" in e14["whatSi"], "")
    e11 = next(v for v in d1907 if v["houseNo"] == "11")
    check("I5l h11-Marija-ŽUNIČ = VLM-'Kumič'-ZAVRJENA (KAŠEL-diag-jasno!)",
          "ŽUNIČ" in e11["whatSi"] and "Kumič" in e11["whatSi"] and "KAŠEL-POTRJEN" in e11["whatSi"], "")

    # ---------- I6: kumulativ + parish.ts ----------
    check("I6a vitals 996", len(vit) == VITALS_TOTAL, str(len(vit)))
    check("I6b mrliški bloki 04894 = 297", len(d04894) == BLOKI_04894, str(len(d04894)))
    check("I6c bloki 1907 = 20", len(d1907) == 20, str(len(d1907)))
    check("I6d bloki 1907: skeni 109–114 + stran == sken − 1",
          all(v["scan"] and 109 <= v["scan"] <= 114 and v["page"] == v["scan"] - 1 for v in d1907), "")
    check("I6d2 bloki 1908+ ne obstajajo (P174-lead!; P173 = 1907 sedaj v korpusu!)",
          all(v["year"] < 1911 for v in d04894), "")
    p80 = open("scripts/p80_parish_md_books.py", encoding="utf-8").read()
    check("I6e p80-skripta pini 996 + 92 + gap-18 (vitals-P173-kaskada!)",
          "len(vitals) == 1032" in p80 and "len(houses) == 92" in p80 and "len(gap) == 18" in p80, "")
    houses_all = {v["houseNo"] for v in vit if v["houseNo"].isdigit()}
    check("I6f korpus = 93 hiš (NESPREMENJENO — h75/h10-ŽE-v-korpusu!)",
          len(houses_all) == KORPUS_HOUSES, str(len(houses_all)))

    # ---------- I7: forenzika (anomalije A1–A12!) ----------
    a1 = next(x for x in d["anomalies"] if x["id"] == "A1")
    check("I7a A1: 3-PISAR-DATUM-NAPAKE-1.-TIPO (29.-Feb + 31.-Sept-×2!)",
          "29.-Februar-1907" in a1["opis"] and "31.-September" in a1["opis"], "")
    a2 = next(x for x in d["anomalies"] if x["id"] == "A2")
    check("I7b A2: 5-GLAVE-NAPAKE-REKORD-IZENAČEN-3.× (s111-'181904'-NAPAČNO-LETO!)",
          "REKORD-IZENAČEN-3.×" in a2["opis"] and "181904" in a2["opis"]
          and "NEKOMPLETNA" in a2["opis"], "")
    a4 = next(x for x in d["anomalies"] if x["id"] == "A4")
    check("I7c A4: P172-'BRINEC-PAR-vez'-KOREKCIJA (z1 = Anton-BRODARIČ!)",
          "BRODARIČ" in a4["opis"] and "KOREKCIJA" in a4["opis"], "")
    a6 = next(x for x in d["anomalies"] if x["id"] == "A6")
    check("I7d A6: NOVI-DUHOVNIK-LILEK + Nemaniš + KRUSCH + CERAR-DOMINANTA",
          "LILEK" in a6["opis"] and "NEMANIŠ" in a6["opis"] and "KRUSCH" in a6["opis"]
          and "CERAR" in a6["opis"], "")
    a7 = next(x for x in d["anomalies"] if x["id"] == "A7")
    check("I7e A7: VLM-HALUCINACIJE-imen-×13 (MUC + NOVAK + ŽELJKO + BRINEC!)",
          "MUC" in a7["opis"] and "NOVAK" in a7["opis"] and "ŽELJKO" in a7["opis"]
          and "BRINEC" in a7["opis"] and "URH" in a7["opis"], "")
    a8 = next(x for x in d["anomalies"] if x["id"] == "A8")
    check("I7f A8: VLM-bolezen-korekcije-×4 (→KAŠEL!)",
          "KAŠEL" in a8["opis"] and "Maščef" in a8["opis"] and "Kaicij" in a8["opis"], "")

    # ---------- I8: meje + lead ----------
    c1 = d["crossChecks"][0]["opis"]
    check("I8a zap-kontinuiteta (C1 — 67-oštevilčenih = 67-VPISOV!)",
          "67-oštevilčenih" in c1 and "ČISTA-SEKVENCA" in c1, c1[:60])
    check("I8b meja 1906/07 = s109 + meja 1907/08 = s114 (15.-POTRDITEV — KOREKCIJA!)",
          "s109" in fr["meja_1906_07"] and "s114" in fr["meja_1907_08"]
          and "15. POTRDITEV" in fr["meja_1907_08"]
          and "KOREKCIJA" in fr["meja_1907_08"], "")
    ns = json.dumps(d["nextSteps"], ensure_ascii=False)
    check("I8c P174-lead v dokazu (1908 + PEZDIREC-h42 + 4-GRIBLJE!)",
          "P174-lead" in ns and "1908" in ns and "PEZDIREC" in ns, "")
    check("I8d X1–X2 excluded (s114-zap1–3-1908 + s115/s116-P174-lead!)",
          len(d["excluded"]) == 2 and "s114-zap1–3" in d["excluded"][0]["opis"]
          and "s115" in d["excluded"][1]["opis"], "")

    # ---------- I9: demografija ----------
    duh = [e["duhovnik"] or "" for e in grb]
    n_rauq = sum(1 for x in duh if "Rauq" in x)
    n_cer = sum(1 for x in duh if "Cerar" in x or "CERAR" in x)
    n_lil = sum(1 for x in duh if "LILEK" in x)
    n_flor = sum(1 for x in duh if "Florjančič" in x or "FLORJANČIČ" in x)
    check("I9a duhovniki-Griblje: Rauq-×9 + Cerar-×6 + LILEK-×1 + Florjančič-×4 = 20 (7-podpisovcev!)",
          n_rauq == 9 and n_cer == 6 and n_lil == 1 and n_flor == 4,
          f"R{n_rauq}/C{n_cer}/L{n_lil}/F{n_flor}")
    meseci = {}
    for e in grb:
        k = (e["mesec"] or "")[:3]
        meseci[k] = meseci.get(k, 0) + 1
    check("I9b meseci Griblje: Jan6 + Feb2 + Maj1 + Jun1 + Jul3 + Sep3 + Nov2 + Dec2 = 20",
          meseci.get("Jan") == 6 and meseci.get("Feb") == 2 and meseci.get("Maj") == 1
          and meseci.get("Jun") == 1 and meseci.get("Jul") == 3 and meseci.get("Sep") == 3
          and meseci.get("Nov") == 2 and meseci.get("Dec") == 2, str(meseci))
    check("I9c starostni-razpon 3-tednov → 69-let (z5 → z9!)",
          any("3 TEDNOV" in e["starost"] for e in grb)
          and any("69 LET" in e["starost"] for e in grb), "")
    otroci = [e for e in grb if "DNI" in e["starost"] or "MESECEV" in e["starost"]
              or "MESECE" in e["starost"] or "TEDNOV" in e["starost"]]
    check("I9d otroška-smrt 6/20 (z5-3-tednov + z11/z13-mesece + z57/z63/z65-dni!)",
          len(otroci) == 6, str([(e["houseNo"], e["starost"]) for e in otroci]))
    prev = [e["previden"] for e in grb]
    check("I9e previden-Griblje: '1' ×9 + PRAZNO ×11",
          sum(1 for x in prev if str(x).strip() == "1") == 9, str(prev))

    # ---------- I10: qa-parish + pin-kaskada ----------
    qa = open(QA_TS, encoding="utf-8").read()
    check("I10a qa-p173 = 174. kontrola", "qa-p173-parish-death-1907" in qa, "")
    check("I10b qa-parish pini 996 + 297 (P173-kaskada!)",
          qa.count("!== 1032") == 91 and qa.count("!== 333") == 25,
          f"996×{qa.count('!== 1032')}/297×{qa.count('!== 333')}")
    check("I10c qa-parish guardi ≥1908 (21× — P173-kaskada + p173-lastni!)",
          qa.count(">= 1911") == 24, f"{qa.count('>= 1911')}")
    check("I10d qa-parish p80 = 92 (24× — +h75!)",
          qa.count("p80Houses.size !== 92") == 24, f"{qa.count('p80Houses.size !== 92')}")
    check("I10e 1907-izjeme-v-krstnih-guardih (p86-h28/p87-h75/p88-h91/p90-h87/p91-h14/p92-h10/p94-h49/p96-h19!)",
          all(f'"04894" && v.year === 1907 && hn === "{h}"' in qa for h in ["28", "75", "91", "87", "14", "10", "49"])
          and qa.count("04894\" && h.year === 1907") >= 2, "")

    # ---------- I11: parish.ts-kaskada ----------
    src = open(PARISH_TS, encoding="utf-8").read()
    check("I11a P173-blok-komentar-v-parish.ts",
          "P173: mrliška 1907" in src, "")
    check("I11b P173-20-blokov-whatSi-potrditve (BRODARIČ + MUC + LILEK + KAŠEL!)",
          all(k in src for k in ["P172-'BRINEC-PAR-vez'-KOREKCIJA", "P172-lead-'MEC'-KOREKCIJA",
                                 "NOVI-DUHOVNIK-×1-GRIBLJE", "IZENAČUJE-REKORDISTKO-h58",
                                 "PISAR-DATUM-NAPAKA-1/3", "KAŠEL-POTRJEN"]), "")
    check("I11c P174-LEAD-v-parish.ts (s114-zap1–3 + s115/s116!)",
          "P174-LEAD: 1908" in src and "s115-zap4–15" in src, "")
    check("I11d ni-04894-1911-blokov-še (P177-lead!; P176 = 1910 sedaj v korpusu!; 04455-1911-legalno!)",
          re.search(r'bookSignature: "04894",\s*year: 1911', src) is None, "")

    # ---------- I12: honesty ----------
    check("I12 honesty ≥5 (honesty-1–6!)",
          len(d["honesty"]) >= 5, str(len(d["honesty"])))
    check("I12b honesty-rows-v3-FAIL-lekcija (diag-grid-recept!)",
          any("rows-v3" in x for x in d["honesty"]), "")

    # ---------- I13: --live (HTTP!) ----------
    if live:
        st, body = http_get(BOOK_URL)
        ok = st == 200 and (b"04894" in body or b"podzemelj" in body.lower())
        check("I13a --live matricula-04894-dostopen", st == 200, f"HTTP {st}")
        check("I13b dokaz-Griblje == parish.ts-Griblje (1:1!)",
              sorted([e["houseNo"] for e in grb]) == sorted([v["houseNo"] for v in d1907]),
              f"{sorted([e['houseNo'] for e in grb])}")
        check("I13c dokaz-skeni == parish.ts-skeni (1:1!)",
              sorted([(e["houseNo"], e["scan"], e["page"]) for e in grb])
              == sorted([(v["houseNo"], v["scan"], v["page"]) for v in d1907]), "")

    ok_n = sum(1 for _, ok, _ in results if ok)
    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'}: {name}" + (f" — {detail}" if detail and not ok else ""))
    print(f"\nP173: {ok_n}/{len(results)} " + ("PASS ✓" if ok_n == len(results) else "FAIL ✗"))
    return 0 if ok_n == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
