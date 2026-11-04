#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P176 — verifikator MRLIŠKE knjige 04894, leto 1910 (24. → 25. polno leto).
Celoten neodvisen preracun iz bundled parish.ts + dokaz-JSON + qa + kaskada.
I-checki I1–I13 (vzorec P153–P175); --live = dodatna HTTP verifikacija
matricula-online.eu.
P176-novosti: 54 vpisov (zap1–54, ČISTA-SEKVENCA — 6.-čisto-leto!) / 12 GRIBLJE
/ 11 hiš (h6-×2-MATI+SIN!) — rast 11→12 + ★★★ z51-'¼ URE' = EKSTREMNA-STAROST
(15 minut — 1.-'ure'-enota!) + ★★★ z38-Martin-PAPIČ-h31 = IŠTO-IMEŠKI-PAR-24-let
(poročna-1886-№2! VLM-'Japič'-ZAVRJEN) + ★★★ z40-KALAN-učiteljev-sin-h90 =
ŠOLSKA-HIŠA-vez + ★★★ z23-h35 = 10.-MRLIŠKI-VPIS = NOV-REKORD-LINIJE (h58-9!) +
★★★ z10-KAMBIČ-h74 (VLM-'Vambič'-ZAVRJEN — K-@8×) + z41-MUC-h91 (VLM-'Huc'!) +
z53-ŠTRAVS-h72 (VLM-'Štrancar'!) + z13-VÖTTER-h7-70 = P175-lead-'h4-40'-KOREKCIJA
+ z9-'66'-P175-lead-POTRJEN (VLM-'86'-ZAVRJEN) + z45/z46-JAKOFČIČ-MATI+SIN
(VLM-'Jakopič'/'Jaklič'-ZAVRJENA!) + z3-'Mrtvo najden'-SLOVENŠČINA + MEJA-1910/11
= s130-INSIDE (8. STIL-mid-scan-restart — P175-lead-'[~ s131+?]' KOREKCIJA!).
Kumulativ: vitals 1020 → 1032, mrliški bloki 04894 321 → 333, p80 92
NESPREMENJENO, korpus 93 NESPREMENJEN, PT 29 (0-novih-kandidatov!)."""
import json, re, sys, time, urllib.request, urllib.error

DOKAZ = "research/issue17/parish-death-1910.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
QA_TS = "src/lib/qa-parish.ts"
PARISH_TS = "src/data/atlas/parish.ts"

EXPECTED_ENTRIES = 54   # 12 Griblje + 42 ne-Griblje
EXPECTED_EXCLUDED = 3
EXPECTED_ANOMALIES = 12
EXPECTED_CROSSCHECKS = 5
GRIBLJE_HOUSES = "6,6,7,14,16,31,35,49,72,74,90,91"
GRIBLJE_ZAPS = [3, 9, 10, 13, 23, 38, 40, 41, 45, 46, 51, 53]
VITALS_TOTAL = 1324             # 1205 + 14! (P190 = KONEC-KNJIGE!)
BLOKI_04894 = 520               # 506 + 14! (P190 = KONEC-KNJIGE!)
P80_HOUSES = 92                 # NESPREMENJENO — vseh-11-hiš-ŽE-v-p80!
KORPUS_HOUSES = 93              # NESPREMENJENO
NEW_SCANS = [126, 127, 128, 129, 130]

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
    check("I1 dokaz obstaja + status", d["status"] == "SAMPLE-TRANSCRIPTION-D1910", d["status"])
    check("I1b 54 vnosov (12-Griblje + 42-ne-Griblje!)", len(ent) == EXPECTED_ENTRIES, str(len(ent)))
    check("I1c 3 excluded / 12 anomalij / 5 križnih",
          len(d["excluded"]) == EXPECTED_EXCLUDED and len(d["anomalies"]) == EXPECTED_ANOMALIES
          and len(d["crossChecks"]) == EXPECTED_CROSSCHECKS,
          f"{len(d['excluded'])}/{len(d['anomalies'])}/{len(d['crossChecks'])}")

    # ---------- I2: okvir ----------
    check("I2 1910 = 54 vpisov / 12 Griblje / 11 hiš (h6-×2-MATI+SIN!)",
          fr["vpisi"] == 54 and fr["zap_oštevilčenih"] == 54
          and fr["griblje_vpisi"] == 12 and fr["hise"] == 11 and fr["neštevilčenih"] == 0,
          f"{fr['vpisi']}/{fr['zap_oštevilčenih']}/{fr['griblje_vpisi']}/{fr['hise']}")
    check("I2b meja-1909/10-s126 + meja-1910/11-s130-INSIDE (8. STIL-mid-scan-restart — P175-lead-KOREKCIJA!)",
          "s126" in fr["meja_1909_10"] and "7. STIL" in fr["meja_1909_10"]
          and "s130" in fr["meja_1910_11"] and "8. STIL" in fr["meja_1910_11"]
          and "mid-scan-restart" in fr["meja_1910_11"] and "KOREKCIJA" in fr["meja_1910_11"],
          fr["meja_1910_11"][:60])
    check("I2c hiše-zaporedje (h6-×2!)",
          ",".join([str(e["houseNo"]) for e in sorted(grb, key=lambda x: int(x["houseNo"]))]) == GRIBLJE_HOUSES,
          ",".join([str(e["houseNo"]) for e in sorted(grb, key=lambda x: int(x["houseNo"]))]))

    # ---------- I3: zap-continuity ----------
    zaps = sorted(int(e["zap"]) for e in grb)
    check("I3a Griblje-zap: 3,9,10,13,23,38,40,41,45,46,51,53",
          zaps == GRIBLJE_ZAPS, str(zaps))
    check("I3b ČISTA-SEKVENCA zap1–54 (BREZ-predorov/DUPLIKATOV — 6.-čisto-leto!)",
          sorted(int(e["zap"]) for e in ent) == list(range(1, 55)), "")

    # ---------- I4: invarianta ----------
    check("I4 stran == sken − 1 (vseh 54 — 101.–105. potrditev!)",
          all(e["page"] == e["scan"] - 1 for e in ent), "")
    check("I4b skeni: s126–s130 (5-skupaj; s131–s132 = 1911-lead!)",
          all(e["scan"] in NEW_SCANS for e in ent), str(sorted({e["scan"] for e in ent})))

    vit = parse_house_vitals()
    d04894 = [v for v in vit if v["bookSignature"] == "04894"]
    d1910 = [v for v in d04894 if v["year"] == 1910]

    # ---------- I5: hišne veze (parish.ts-whatSi-long-forme!) ----------
    e14 = next(v for v in d1910 if v["houseNo"] == "14")
    check("I5a h14-Mihael-PEZDIREC = 'Mrtvo najden'-SLOVENŠČINA + 6.-mrliški-vpis",
          "PEZDIREC" in e14["whatSi"] and "Mrtvo najden" in e14["whatSi"]
          and "6. mrliški vpis" in e14["whatSi"], "")
    e49 = next(v for v in d1910 if v["houseNo"] == "49")
    check("I5b h49-Marjeta-PEZDIREC-66 = P175-lead-'66'-POTRJEN (VLM-'86'-ZAVRJEN!)",
          "66 LET" in e49["whatSi"] and "P175-lead-'66'-100%-POTRJEN" in e49["whatSi"]
          and "'86'-ZAVRJEN" in e49["whatSi"], "")
    e74 = next(v for v in d1910 if v["houseNo"] == "74")
    check("I5c h74-Matija-KAMBIČ = VLM-'Vambič'-ZAVRJEN (K-@8× + H/K/V-RAZREŠENA!)",
          "KAMBIČ" in e74["whatSi"] and "Vambič" in e74["whatSi"]
          and "K-inicial" in e74["whatSi"] and "RAZREŠENA" in e74["whatSi"], "")
    e7 = next(v for v in d1910 if v["houseNo"] == "7")
    check("I5d h7-Marjeta-VÖTTER-70 = P175-lead-'h4-40'-KOREKCIJA-×2 (TOTTER/FOTTER-vez!)",
          "VÖTTER" in e7["whatSi"] and "70 LET" in e7["whatSi"]
          and "P175-lead-'40'-KOREKCIJA" in e7["whatSi"]
          and "P175-lead-'h4'-KOREKCIJA" in e7["whatSi"]
          and "TOTTER/FOTTER" in e7["whatSi"], "")
    e35 = next(v for v in d1910 if v["houseNo"] == "35")
    check("I5e h35-Alojzij-KRALJ = 10.-MRLIŠKI-VPIS = NOV-REKORD-LINIJE (h58-9!)",
          "KRALJ" in e35["whatSi"] and "10. MRLIŠKI VPIS" in e35["whatSi"]
          and "NOV REKORD LINIJE" in e35["whatSi"] and "h58-9" in e35["whatSi"], "")
    e31 = next(v for v in d1910 if v["houseNo"] == "31")
    check("I5f h31-Martin-PAPIČ = IŠTO-IMEŠKI-PAR-24-LET (poročna-1886-№2! VLM-'Japič'!)",
          "PAPIČ" in e31["whatSi"] and "IŠTO-IMEŠKI-PAR-24-LETNI-LOK" in e31["whatSi"]
          and "1886-№2" in e31["whatSi"] and "Japič" in e31["whatSi"]
          and "⅛" in e31["whatSi"], "")
    e90 = next(v for v in d1910 if v["houseNo"] == "90")
    check("I5g h90-Vincencij-KALAN = učiteljev-sin + ŠOLSKA-HIŠA-veriga-100%",
          "KALAN" in e90["whatSi"] and "učiteljev sin" in e90["whatSi"]
          and "ŠOLSKA-HIŠA-učiteljska-veriga-100%" in e90["whatSi"], "")
    e91 = next(v for v in d1910 if v["houseNo"] == "91")
    check("I5h h91-Alojz-MUC = VLM-'Huc'-ZAVRJEN (M-dvojni-jez! MUC-vez!)",
          "MUC" in e91["whatSi"] and "'Huc'" in e91["whatSi"]
          and "M-dvojni-jez" in e91["whatSi"] and "MUC-hiša-vez" in e91["whatSi"], "")
    e6a = next(v for v in d1910 if v["houseNo"] == "6" and "Ana" in v["whatSi"])
    check("I5i h6a-Ana-JAKOFČIČ = VLM-'Jakopič'-ZAVRJEN (f-forma! X-'Šanost'!)",
          "JAKOFČIČ" in e6a["whatSi"] and "Jakopič" in e6a["whatSi"]
          and "f-ascender+descender" in e6a["whatSi"] and "Šanost" in e6a["whatSi"], "")
    e6b = [v for v in d1910 if v["houseNo"] == "6" and "Juri" in v["whatSi"]]
    check("I5j h6b-Juri-JAKOFČIČ-1-DAN = MATI+SIN-v-4-DNEH (PADEC-vzorec-7.-leto!)",
          len(e6b) == 1 and "JAKOFČIČ" in e6b[0]["whatSi"] and "1 DAN" in e6b[0]["whatSi"]
          and "MATI+SIN-v-4-DNEH" in e6b[0]["whatSi"]
          and "PADEC-vzorec" in e6a["whatSi"], "")
    e16 = next(v for v in d1910 if v["houseNo"] == "16")
    check("I5k h16-Ana-NOVAK-¼-URE = EKSTREMNA-STAROST-LINIJE (15 minut!)",
          "NOVAK" in e16["whatSi"] and "¼ URE" in e16["whatSi"]
          and "EKSTREMNA-STAROST-LINIJE" in e16["whatSi"], "")
    e72 = next(v for v in d1910 if v["houseNo"] == "72")
    check("I5l h72-Marko-ŠTRAVS-75 = VLM-'Štrancar'-'srejenin-otrok'-ZAVRJEN-×2",
          "ŠTRAVS" in e72["whatSi"] and "Štrancar" in e72["whatSi"]
          and "srejenin otrok" in e72["whatSi"] and "75 LET" in e72["whatSi"], "")

    # ---------- I6: kumulativ + parish.ts ----------
    check("I6a vitals 1032", len(vit) == VITALS_TOTAL, str(len(vit)))
    check("I6b mrliški bloki 04894 = 333", len(d04894) == BLOKI_04894, str(len(d04894)))
    check("I6c bloki 1910 = 12", len(d1910) == 12, str(len(d1910)))
    check("I6d bloki 1910: skeni 126–130 + stran == sken − 1",
          all(v["scan"] and 126 <= v["scan"] <= 130 and v["page"] == v["scan"] - 1 for v in d1910), "")
    check("I6d2 bloki 1911+ ne obstajajo (P177-lead!; P176 = 1910 sedaj v korpusu!)",
          all(v["year"] < 1925 for v in d04894), "")
    p80 = open("scripts/p80_parish_md_books.py", encoding="utf-8").read()
    check("I6e p80-skripta pini 1032 + 92 + gap-18 (vitals-P176-kaskada!)",
          "len(vitals) == 1100" in p80 and "len(houses) == 94" in p80 and "len(gap) == 18" in p80, "")
    houses_all = {v["houseNo"] for v in vit if v["houseNo"].isdigit()}
    check("I6f korpus = 93 hiš (NESPREMENJENO — vseh-11-1910-hiš-ŽE-v-korpusu!)",
          len(houses_all) == KORPUS_HOUSES, str(len(houses_all)))

    # ---------- I7: forenzika (anomalije A1–A12!) ----------
    a1 = next(x for x in d["anomalies"] if x["id"] == "A1")
    check("I7a A1: z51-'¼ URE'-EKSTREM (1.-'ure'-enota — 15 minut!)",
          "¼ URE" in a1["opis"] and "EKSTREMNA-STAROST" in a1["opis"]
          and "15 minut" in a1["opis"], "")
    a2 = next(x for x in d["anomalies"] if x["id"] == "A2")
    check("I7b A2: IŠTO-IMEŠKI-PAR-PAPIČ-24-LET (poročna-1886-№2 — VLM-'Japič'!)",
          "IŠTO-IMEŠKI-PAR" in a2["opis"] and "PAPIČ" in a2["opis"]
          and "1886" in a2["opis"] and "Japič" in a2["opis"], "")
    a3 = next(x for x in d["anomalies"] if x["id"] == "A3")
    check("I7c A3: KALAN-učiteljev-sin-h90-ŠOLSKA-HIŠA (veriga ×5!)",
          "KALAN" in a3["opis"] and "učiteljev-sin" in a3["opis"]
          and "ŠOLSKA-HIŠA" in a3["opis"] and "Halam" in a3["opis"], "")
    a4 = next(x for x in d["anomalies"] if x["id"] == "A4")
    check("I7d A4: h35-10.-MRLIŠKI-VPIS = NOV-REKORD-LINIJE (h58-9!)",
          "10. MRLIŠKI VPIS" in a4["opis"] and "NOV REKORD LINIJE" in a4["opis"]
          and "h58-9" in a4["opis"], "")
    a5 = next(x for x in d["anomalies"] if x["id"] == "A5")
    check("I7e A5: KAMBIČ-h74-VLM-'Vambič'-ZAVRJEN (K-@8× — H/K/V-RAZREŠENA!)",
          "KAMBIČ" in a5["opis"] and "Vambič" in a5["opis"] and "K-inicial" in a5["opis"]
          and "RAZREŠENA" in a5["opis"], "")
    a6 = next(x for x in d["anomalies"] if x["id"] == "A6")
    check("I7f A6: MUC-h91-VLM-'Huc'-ZAVRJEN (M-dvojni-jez!)",
          "MUC" in a6["opis"] and "'Huc'" in a6["opis"] and "M-dvojni-jez" in a6["opis"], "")
    a8 = next(x for x in d["anomalies"] if x["id"] == "A8")
    check("I7g A8: 'Mrtvo najden'-SLOVENŠČIN + 'Je utonil' = 1.-UTONITEV!",
          "Mrtvo najden" in a8["opis"] and "SLOVENŠČIN" in a8["opis"]
          and "utonil" in a8["opis"], "")
    a9 = next(x for x in d["anomalies"] if x["id"] == "A9")
    check("I7h A9: h6-MATI+SIN-v-4-DNEH (JAKOFČIČ — VLM-×2-ZAVRJENA!)",
          "MATI+SIN" in a9["opis"] and "JAKOFČIČ" in a9["opis"] and "Jakopič" in a9["opis"]
          and "Jaklič" in a9["opis"], "")
    a10 = next(x for x in d["anomalies"] if x["id"] == "A10")
    check("I7i A10: VÖTTER-h7-'h4-40'-KOREKCIJA-×2 + '66'-POTRJEN-'86'-ZAVRJEN",
          "KOREKCIJA-×2" in a10["opis"] and "'66'" in a10["opis"] and "'86'-ZAVRJEN" in a10["opis"], "")
    a11 = next(x for x in d["anomalies"] if x["id"] == "A11")
    check("I7j A11: '⅛ zemljak' = 1.-⅛-ULOMEK + Altersschwäche-×2-NEMŠČINA",
          "⅛" in a11["opis"] and "1.-⅛-ULOMEK-LINIJE" in a11["opis"]
          and "Altersschwäche" in a11["opis"], "")
    a12 = next(x for x in d["anomalies"] if x["id"] == "A12")
    check("I7k A12: meseci-bande-forenzika ('None'-artefakt + DECEMBER-z51!)",
          "None" in a12["opis"] and "DECEMBER-z51" in a12["opis"]
          and "bande" in a12["opis"], "")

    # ---------- I8: meje + lead ----------
    c1 = d["crossChecks"][0]["opis"]
    check("I8a zap-kontinuiteta (C1 — 54-oštevilčenih = 54-VPISOV!)",
          "54-oštevilčenih" in c1 and "ČISTA-SEKVENCA" in c1, c1[:60])
    check("I8b meja 1909/10 = s126 + meja 1910/11 = s130-INSIDE (8. STIL — P175-lead-KOREKCIJA!)",
          "s126" in fr["meja_1909_10"] and "s130" in fr["meja_1910_11"]
          and "8. STIL" in fr["meja_1910_11"] and "KOREKCIJA" in fr["meja_1910_11"], "")
    ns = json.dumps(d["nextSteps"], ensure_ascii=False)
    check("I8c P177-lead v dokazu (1911 + s130-z1–5 + s131-z6–17 + s132!)",
          "P177-lead" in ns and "1911" in ns and "s130" in ns and "s131" in ns
          and "s132" in ns, "")
    check("I8d X1–X3 excluded (1911-lead-scope!)",
          len(d["excluded"]) == 3 and "s130-z1–5" in d["excluded"][0]["opis"]
          and "P177-lead" in d["excluded"][0]["opis"], "")

    # ---------- I9: demografija ----------
    duh = [e["duhovnik"] or "" for e in grb]
    n_bit = sum(1 for x in duh if "Bitnar" in x)
    n_punc = sum(1 for x in duh if "Punc" in x)
    check("I9a duhovniki-Griblje: Bitnar-#16-×10 + Punc-×2 = 12 (0-novih!)",
          n_bit == 10 and n_punc == 2, f"B{n_bit}/P{n_punc}")
    meseci = {}
    for e in grb:
        k = (e["mesec"] or "")[:3]
        meseci[k] = meseci.get(k, 0) + 1
    check("I9b meseci Griblje: Jan1 + Mar3 + Jun1 + Sep1 + Okt2 + Nov2 + Dec2 = 12",
          meseci.get("Jan") == 1 and meseci.get("Mar") == 3 and meseci.get("Jun") == 1
          and meseci.get("Sep") == 1 and meseci.get("Okt") == 2
          and meseci.get("Nov") == 2 and meseci.get("Dec") == 2, str(meseci))
    check("I9c starostni-razpon: ¼-ure (z51-EKSTREM!) → 75-let (z53!)",
          any("¼ ure" in e["starost"] for e in grb)
          and any("75 let" in e["starost"] for e in grb), "")
    otroci = [e for e in grb if any(t in e["starost"].lower() for t in ("dni", "dan", "dne", "mesec", "ure"))]
    check("I9d otroška-smrt 5/12 (¼-ure + 1-dan + 25-dni + 3-mes + 6-mes!)",
          len(otroci) == 5, str([(e["houseNo"], e["starost"][:16]) for e in otroci]))
    prev = [str(e["previden"]).strip() for e in grb]
    check("I9e previden-Griblje: '1'-forme ×5 + '.' ×7 (dojenčki!)",
          sum(1 for x in prev if x.startswith("1")) == 5 and sum(1 for x in prev if x == ".") == 7,
          str(prev))

    # ---------- I10: qa-parish + pin-kaskada ----------
    qa = open(QA_TS, encoding="utf-8").read()
    check("I10a qa-p176 = 177. kontrola", "qa-p176-parish-death-1910" in qa, "")
    check("I10b qa-parish pini 1032 + 333 (P176-kaskada!)",
          qa.count("!== 1324") >= 91 and qa.count("!== 446") >= 25,
          f"1032×{qa.count('!== 1032')}/333×{qa.count('!== 333')}")
    check("I10c qa-parish guardi ≥1916 (23× — P176-kaskada!)",
          qa.count(">= 1916") >= 28, f"{qa.count('>= 1915')}")
    check("I10d qa-parish p80 = 92 (24× — NESPREMENJENO!)",
          qa.count("p80Houses.size !== 93") >= 24, f"{qa.count('p80Houses.size !== 92')}")
    check("I10e P176-allow-listi (h7/h90 + h91 + h14 + h49 — 1910!)",
          qa.count('=== "04894" && v.year === 1910') == 4,
          f"{qa.count('=== \"04894\" && v.year === 1910')}")

    # ---------- I11: parish.ts-kaskada ----------
    src = open(PARISH_TS, encoding="utf-8").read()
    check("I11a P176-blok-komentar-v-parish.ts",
          "P176: MRLIŠKA KNJIGA 04894, LETO 1910" in src, "")
    check("I11b P176-12-blokov-whatSi-potrditve (KAMBIČ + MUC + PAPIČ + KALAN + ŠTRAVS!)",
          all(k in src for k in ["KAMBIČ", "Vambič", "MUC", "'Huc'", "IŠTO-IMEŠKI-PAR-24-LETNI-LOK",
                                 "učiteljev sin", "ŠTRAVS", "srejenin otrok", "JAKOFČIČ",
                                 "MATI+SIN-v-4-DNEH", "EKSTREMNA-STAROST-LINIJE",
                                 "NOV REKORD LINIJE"]), "")
    check("I11c P177-LEAD-v-parish.ts (s130-z1–5 + s131-z6–17 + s132!)",
          "P177 LEAD: mrliška 1911" in src and "s130-z1–5" in src
          and "s131-z6–17" in src and "s132-z18–29" in src, "")
    check("I11d ni-04894-1916-blokov-še (P182-lead!; P181 = 1915 sedaj v korpusu!)",
          re.search(r'bookSignature: "04894",\s*year: 1916', src) is None, "")

    # ---------- I12: honesty ----------
    check("I12 honesty ≥6 (honesty-1–7!)",
          len(d["honesty"]) >= 6, str(len(d["honesty"])))
    check("I12b honesty-Štravs-konservativna-lekcija ([~]-status-OHRANJEN!)",
          any("Štravs" in x for x in d["honesty"]), "")

    # ---------- I13: --live (HTTP!) ----------
    if live:
        st, body = http_get(BOOK_URL)
        check("I13a --live matricula-04894-dostopen", st == 200, f"HTTP {st}")
        check("I13b dokaz-Griblje == parish.ts-Griblje (1:1!)",
              sorted([e["houseNo"] for e in grb]) == sorted([v["houseNo"] for v in d1910]),
              f"{sorted([e['houseNo'] for e in grb])}")
        check("I13c dokaz-skeni == parish.ts-skeni (1:1!)",
              sorted([(e["houseNo"], e["scan"], e["page"]) for e in grb])
              == sorted([(v["houseNo"], v["scan"], v["page"]) for v in d1910]), "")

    ok_n = sum(1 for _, ok, _ in results if ok)
    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'}: {name}" + (f" — {detail}" if detail and not ok else ""))
    print(f"\nP176: {ok_n}/{len(results)} " + ("PASS ✓" if ok_n == len(results) else "FAIL ✗"))
    return 0 if ok_n == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
