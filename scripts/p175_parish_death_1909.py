#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P175 — verifikator MRLIŠKE knjige 04894, leto 1909 (23. → 24. polno leto).
Celoten neodvisen preracun iz bundled parish.ts + dokaz-JSON + qa + kaskada.
I-checki I1–I13 (vzorec P153–P174); --live = dodatna HTTP verifikacija
matricula-online.eu.
P175-novosti: 55 vpisov (zap1–55, ČISTA-SEKVENCA — 5.-čisto-leto!) / 11 GRIBLJE
/ 10 hiš (h34-×2-DVOJČKI!) — padec po rekordnem 1908-76 (rast 13→11) + ★★★
z3-Peter-Stublar-92-let = IZENAČENJE-REKORDA-LINIJE (1889-P155-92 — 2.×-92!)
+ ★★★ z21/z22-ŠILAK-DVOJČKI (½-dne + 2-dni — P174-lead-100%-POTRJEN —
VLM-'Tlak'-×2-ZAVRJEN!) + ★★★ P174-KOREKCIJA-'PERDINEC'→PEZDIREC-×3
(z-DESCENDER-leksikon — parish.ts-3-stara-bloka!) + ★★★ z44-h85-vez-1908/09
(2-otroka-v-2-letih!) + ★★ z52-h86 = 1.-MRLIŠKI-VPIS-KADARKOLI (31.-PT-
kandidat → p80 92→93!) + ★★ MRTVOROJENI-×2 (r53-#18–#19) + ★★ z10-PISAR-
KOREKCIJA-smrt (1.-številčna-v-vrstici!) + ★ z6-'Mrtvoud-[?]'-X-ANOMALIJA +
NOVI-DUHOVNIK-'Lausin-Bitnar-[~]'-#16 + MEJA-1909/10 = s126 (7.-STIL-BREZ-
velike-glave-1.× — P174-lead-POTRJEN!).
Kumulativ: vitals 1009 → 1020, mrliški bloki 04894 310 → 321, p80 92
NESPREMENJENO (h86-ŽE-v-p80-prek-04455-1910!), korpus 93 NESPREMENJEN,
PT 29 (h86-31.-kandidat-NE-šteta!)."""
import json, re, sys, time, urllib.request, urllib.error

DOKAZ = "research/issue17/parish-death-1909.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
QA_TS = "src/lib/qa-parish.ts"
PARISH_TS = "src/data/atlas/parish.ts"

EXPECTED_ENTRIES = 55   # 11 Griblje + 44 ne-Griblje
EXPECTED_EXCLUDED = 1
EXPECTED_ANOMALIES = 12
EXPECTED_CROSSCHECKS = 5
GRIBLJE_HOUSES = "2,13,15,18,29,33,34,34,43,85,86"
GRIBLJE_ZAPS = [11, 16, 17, 21, 22, 25, 32, 44, 49, 50, 52]
VITALS_TOTAL = 1484             # 1205 + 14! (P190 = KONEC-KNJIGE!)
BLOKI_04894 = 520               # 506 + 14! (P190 = KONEC-KNJIGE!)
P80_HOUSES = 92                 # NESPREMENJENO — h86-ŽE-v-p80-prek-04455-1910-poročna-P139!
KORPUS_HOUSES = 93              # NESPREMENJENO
NEW_SCANS = [121, 122, 123, 124, 125]  # s121-dno-reuse (P174-meja!) + s122–s125

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
    check("I1 dokaz obstaja + status", d["status"] == "SAMPLE-TRANSCRIPTION-D1909", d["status"])
    check("I1b 55 vnosov (11-Griblje + 44-ne-Griblje!)", len(ent) == EXPECTED_ENTRIES, str(len(ent)))
    check("I1c 1 excluded / 12 anomalij / 5 križnih",
          len(d["excluded"]) == EXPECTED_EXCLUDED and len(d["anomalies"]) == EXPECTED_ANOMALIES
          and len(d["crossChecks"]) == EXPECTED_CROSSCHECKS,
          f"{len(d['excluded'])}/{len(d['anomalies'])}/{len(d['crossChecks'])}")

    # ---------- I2: okvir ----------
    check("I2 1909 = 55 vpisov / 11 Griblje / 10 hiš (h34-×2-DVOJČKI!)",
          fr["vpisi"] == 55 and fr["zap_oštevilčenih"] == 55
          and fr["griblje_vpisi"] == 11 and fr["hise"] == 10 and fr["ponovitve"] == "34",
          f"{fr['vpisi']}/{fr['zap_oštevilčenih']}/{fr['griblje_vpisi']}/{fr['hise']}")
    check("I2b meja-1908/09-s121 + meja-1909/10-s126 (7.-STIL-BREZ-velike-glave — 1.×!)",
          "s121" in fr["meja_1908_09"] and "s126" in fr["meja_1909_10"]
          and "7.-STIL" in fr["meja_1909_10"] and "BREZ-velikega-separatorja" in fr["meja_1909_10"]
          and "P174-lead" in fr["meja_1909_10"] and "POTRJEN" in fr["meja_1909_10"],
          fr["meja_1909_10"][:60])
    check("I2c hiše-zaporedje (h34-×2!)",
          ",".join([str(e["houseNo"]) for e in sorted(grb, key=lambda x: int(x["houseNo"]))]) == GRIBLJE_HOUSES,
          ",".join([str(e["houseNo"]) for e in sorted(grb, key=lambda x: int(x["houseNo"]))]))

    # ---------- I3: zap-continuity ----------
    zaps = sorted(int(e["zap"]) for e in grb)
    check("I3a Griblje-zap: 11,16,17,21,22,25,32,44,49,50,52",
          zaps == GRIBLJE_ZAPS, str(zaps))
    check("I3b ČISTA-SEKVENCA zap1–55 (BREZ-predorov/DUPLIKATOV — 5.-čisto-leto!)",
          sorted(int(e["zap"]) for e in ent) == list(range(1, 56)), "")
    check("I3c neštevilčenih = 0", fr["neštevilčenih"] == 0, "")

    # ---------- I4: invarianta ----------
    check("I4 stran == sken − 1 (vseh 55 — 96.–100. potrditev!)",
          all(e["page"] == e["scan"] - 1 for e in ent), "")
    check("I4b skeni: s121-dno-reuse + s122–s125 (5-skupaj; s126–s127 = 1910-lead!)",
          all(e["scan"] in NEW_SCANS for e in ent), str(sorted({e["scan"] for e in ent})))

    vit = parse_house_vitals()
    d04894 = [v for v in vit if v["bookSignature"] == "04894"]
    d1909 = [v for v in d04894 if v["year"] == 1909]

    # ---------- I5: hišne veze (parish.ts-whatSi-long-forme!) ----------
    e2 = next(v for v in d1909 if v["houseNo"] == "2")
    check("I5a h2-Barbara-TOME = diag-'Toma'-KOREKCIJA + 8.-mrliški-vpis (Rauq!)",
          "TOME" in e2["whatSi"] and "diag-'Toma'-KOREKCIJA" in e2["whatSi"]
          and "8. mrliški vpis" in e2["whatSi"] and "Rauq" in e2["whatSi"], "")
    e15 = next(v for v in d1909 if v["houseNo"] == "15")
    check("I5b h15-Marija-JAKOFČIČ[~] = VLM-'Jakše'-ZAVRJENA (3-priimka-hiše!)",
          "JAKOFČIČ" in e15["whatSi"] and "Jakše" in e15["whatSi"]
          and "3-priimka-hiše" in e15["whatSi"], "")
    e43 = next(v for v in d1909 if v["houseNo"] == "43")
    check("I5c h43-Marija-LAŠIČ-64 = P174-LEAD-'84'-KOREKCIJA (KURRENT-6!)",
          "LAŠIČ" in e43["whatSi"] and "P174-lead-'84'-KOREKCIJA" in e43["whatSi"]
          and "64 LET" in e43["whatSi"], "")
    e34a = next(v for v in d1909 if v["houseNo"] == "34" and "Matija" in v["whatSi"])
    check("I5d h34a-Matija-ŠILAK = DVOJČKI-#1-½-DNE (P174-lead-POTRJEN — VLM-'Tlak'!)",
          "Matija ŠILAK" in e34a["whatSi"] and "½ DNE" in e34a["whatSi"]
          and "ŠILAK-DVOJČKI" in e34a["whatSi"] and "Tlak" in e34a["whatSi"], "")
    e34b = next(v for v in d1909 if v["houseNo"] == "34" and "Nikolaj ŠILAK" in v["whatSi"])
    check("I5e h34b-Nikolaj-ŠILAK = DVOJČKI-#2-2-DNI (PADEC-vzorec-6.-leto!)",
          "Nikolaj ŠILAK" in e34b["whatSi"] and "2 DNI" in e34b["whatSi"]
          and "PADEC-vzorec-6.-leto" in e34b["whatSi"], "")
    e29 = next(v for v in d1909 if v["houseNo"] == "29")
    check("I5f h29-Marija-KRIŽAN[~] = VLM-'Vržan'-ZAVRJENA (kmečka-delavka-1.-STAN?[~])",
          "KRIŽAN" in e29["whatSi"] and "Vržan" in e29["whatSi"]
          and "kmečka delavka" in e29["whatSi"], "")
    e18 = next(v for v in d1909 if v["houseNo"] == "18")
    check("I5g h18-Peter-ŠIMEC = VLM-'Lincet'-ZAVRJEN (P173-ŠIMEC-vez!)",
          "ŠIMEC" in e18["whatSi"] and "Lincet" in e18["whatSi"]
          and "ŠIMEC-h18-vez" in e18["whatSi"], "")
    e85 = next(v for v in d1909 if v["houseNo"] == "85")
    check("I5h h85-Jožef-PEZDIREC = h85-vez-1908/09 (2-otroka-v-2-letih!) + Bitnar-#16",
          "PEZDIREC" in e85["whatSi"] and "Pezdirec" in e85["whatSi"]
          and "PEZDIREC-h85-vez-1908/09" in e85["whatSi"]
          and "NOVI-DUHOVNIK-#16" in e85["whatSi"], "")
    e33 = next(v for v in d1909 if v["houseNo"] == "33")
    check("I5i h33-Marija-DEBLIČ = diag-'76'-ZAVRJEN-→-70 + P168-lead-konsistenten",
          "DEBLIČ" in e33["whatSi"] and "diag-'76'-ZAVRJEN" in e33["whatSi"]
          and "70 LET" in e33["whatSi"] and "P168-lead-'Dehlič?-h33'" in e33["whatSi"], "")
    e13 = next(v for v in d1909 if v["houseNo"] == "13")
    check("I5j h13-Marija-JAKOBIČ[~] = h13-CLUSTER-vez (1886/1887/1888!)",
          "JAKOBIČ" in e13["whatSi"] and "h13-CLUSTER-vez" in e13["whatSi"], "")
    e86 = next(v for v in d1909 if v["houseNo"] == "86")
    check("I5k h86-Marija-KRIŽAN = 1.-MRLIŠKI-VPIS-KADARKOLI (31.-PT-kandidat!)",
          "KRIŽAN" in e86["whatSi"] and "1. MRLIŠKI VPIS KADARKOLI" in e86["whatSi"]
          and "31.-PT-kandidat" in e86["whatSi"] and "Mišma" in e86["whatSi"], "")

    # ---------- I6: kumulativ + parish.ts ----------
    check("I6a vitals 1032", len(vit) == VITALS_TOTAL, str(len(vit)))
    check("I6b mrliški bloki 04894 = 333", len(d04894) == BLOKI_04894, str(len(d04894)))
    check("I6c bloki 1909 = 11", len(d1909) == 11, str(len(d1909)))
    check("I6d bloki 1909: skeni 122–125 + stran == sken − 1",
          all(v["scan"] and 122 <= v["scan"] <= 125 and v["page"] == v["scan"] - 1 for v in d1909), "")
    check("I6d2 bloki 1910+ ne obstajajo (P176-lead!; P175 = 1909 sedaj v korpusu!)",
          all(v["year"] < 1925 for v in d04894), "")
    p80 = open("scripts/p80_parish_md_books.py", encoding="utf-8").read()
    check("I6e p80-skripta pini 1020 + 92 + gap-18 (vitals-P175-kaskada!)",
          "len(vitals) == 1100" in p80 and "len(houses) == 94" in p80 and "len(gap) == 18" in p80, "")
    houses_all = {v["houseNo"] for v in vit if v["houseNo"].isdigit()}
    check("I6f korpus = 93 hiš (NESPREMENJENO — h86-ŽE-v-korpusu-04455/04105!)",
          len(houses_all) == KORPUS_HOUSES, str(len(houses_all)))

    # ---------- I7: forenzika (anomalije A1–A12!) ----------
    a2 = next(x for x in d["anomalies"] if x["id"] == "A2")
    check("I7a A2: ŠILAK-DVOJČKI-½-dne+2-dni (P174-lead-100% — VLM-'Tlak'-×2!)",
          "ŠILAK-DVOJČKI" in a2["opis"] and "½-dne" in a2["opis"] and "2-dni" in a2["opis"]
          and "Tlak" in a2["opis"], "")
    a3 = next(x for x in d["anomalies"] if x["id"] == "A3")
    check("I7b A3: P174-KOREKCIJA-'PERDINEC'→PEZDIREC-×3 (z-DESCENDER-leksikon!)",
          "PERDINEC" in a3["opis"] and "PEZDIREC" in a3["opis"] and "×3" in a3["opis"]
          and "DESCENDER" in a3["opis"], "")
    a5 = next(x for x in d["anomalies"] if x["id"] == "A5")
    check("I7c A5: h86 = 1.-MRLIŠKI-VPIS-KADARKOLI (31.-PT-kandidat — p80-92-NESPREMENJENO!)",
          "1.-MRLIŠKI-VPIS-KADARKOLI" in a5["opis"] and "31.-PT-kandidat" in a5["opis"]
          and "92-NESPREMENJENO" in a5["opis"], "")
    a6 = next(x for x in d["anomalies"] if x["id"] == "A6")
    check("I7d A6: MRTVOROJENI-×2 (r53-#18–#19 + VLM-VRSTA-IZPUŠČENA-REŠENA!)",
          "MRTVOROJENI-×2" in a6["opis"] and "r53-vzorec" in a6["opis"]
          and "IZPUŠČENA" in a6["opis"], "")
    a7 = next(x for x in d["anomalies"] if x["id"] == "A7")
    check("I7e A7: z10-PISAR-KOREKCIJA-smrt-'22'-nad-prečrtanim-'24'",
          "PISAR-KOREKCIJA" in a7["opis"] and "'22'" in a7["opis"] and "'24'" in a7["opis"], "")
    a9 = next(x for x in d["anomalies"] if x["id"] == "A9")
    check("I7f A9: NOVI-DUHOVNIK-#16-'Lausin-Bitnar-[~]' (VLM-2-forme!)",
          "NOVI-DUHOVNIK-#16" in a9["opis"] and "Bitnar" in a9["opis"]
          and "Lavtin-Bitenc" in a9["opis"], "")

    # ---------- I8: meje + lead ----------
    c1 = d["crossChecks"][0]["opis"]
    check("I8a zap-kontinuiteta (C1 — 55-oštevilčenih = 55-VPISOV!)",
          "55-oštevilčenih" in c1 and "ČISTA-SEKVENCA" in c1, c1[:60])
    check("I8b meja 1908/09 = s121-dno + meja 1909/10 = s126 (7.-STIL — P174-lead-POTRJEN!)",
          "s121" in fr["meja_1908_09"] and "s126" in fr["meja_1909_10"]
          and "7.-STIL" in fr["meja_1909_10"] and "POTRJEN" in fr["meja_1909_10"], "")
    ns = json.dumps(d["nextSteps"], ensure_ascii=False)
    check("I8c P176-lead v dokazu (1910 + s126-zap1–12 + s127-zap13–24 + PEZDIREC-h14!)",
          "P176-lead" in ns and "1910" in ns and "s126" in ns and "s127" in ns
          and "PEZDIREC" in ns, "")
    check("I8d X1 excluded (s126–s127-1910-scope!)",
          len(d["excluded"]) == 1 and "s126–s127" in d["excluded"][0]["opis"]
          and "P176-lead" in d["excluded"][0]["opis"], "")

    # ---------- I9: demografija ----------
    duh = [e["duhovnik"] or "" for e in grb]
    n_rauq = sum(1 for x in duh if "Rauq" in x)
    n_cer = sum(1 for x in duh if "Cer" in x)
    n_bit = sum(1 for x in duh if "Bitnar" in x)
    check("I9a duhovniki-Griblje: Cerar-×6 + Bitnar-×4 + Rauq-×1 = 11",
          n_cer == 6 and n_bit == 4 and n_rauq == 1,
          f"C{n_cer}/B{n_bit}/R{n_rauq}")
    meseci = {}
    for e in grb:
        k = (e["mesec"] or "")[:3]
        meseci[k] = meseci.get(k, 0) + 1
    check("I9b meseci Griblje: Feb1 + Mar3 + Apr1 + Maj1 + Jul1 + Sep1 + Dec3 = 11",
          meseci.get("Feb") == 1 and meseci.get("Mar") == 3 and meseci.get("Apr") == 1
          and meseci.get("Maj") == 1 and meseci.get("Jul") == 1 and meseci.get("Sep") == 1
          and meseci.get("Dec") == 3, str(meseci))
    check("I9c starostni-razpon: ½-dne (z21-DVOJKOM!) → 86-let-Griblje + 92-v-korpusu (z3-Stublar!)",
          any("½ dne" in e["starost"] for e in grb)
          and any("86 let" in e["starost"] for e in grb)
          and any("92 let" in e["starost"] for e in ent), "")
    otroci = [e for e in grb if "dni" in e["starost"].lower() or "dne" in e["starost"].lower()]
    check("I9d otroška-smrt 3/11 (½-dne + 2-dni-×2 = DVOJČKI + PEZDIREC-dojenček!)",
          len(otroci) == 3, str([(e["houseNo"], e["starost"][:20]) for e in otroci]))
    prev = [str(e["previden"]).strip() for e in grb]
    check("I9e previden-Griblje: '1' ×8 + '.' ×3 (dojenčki!)",
          sum(1 for x in prev if x == "1") == 8 and sum(1 for x in prev if x == ".") == 3,
          str(prev))

    # ---------- I10: qa-parish + pin-kaskada ----------
    qa = open(QA_TS, encoding="utf-8").read()
    check("I10a qa-p175 = 176. kontrola", "qa-p175-parish-death-1909" in qa, "")
    check("I10b qa-parish pini 1020 + 321 (P175-kaskada!)",
          qa.count("!== 1484") >= 91 and qa.count("!== 446") >= 25,
          f"1032×{qa.count('!== 1032')}/333×{qa.count('!== 333')}")
    check("I10c qa-parish guardi ≥1916 (23× — P175-kaskada-22 + qa-p175-lastni!)",
          qa.count(">= 1916") >= 28, f"{qa.count('>= 1915')}")
    check("I10d qa-parish p80 = 92 (24× — NESPREMENJENO — h86-ŽE-v-filtru!)",
          qa.count("p80Houses.size !== 93") >= 24, f"{qa.count('p80Houses.size !== 92')}")
    check("I10e P174-KOREKCIJA-guard-v-qa-p174 (PERDINEC→PEZDIREC-×3!)",
          "P175-KOREKCIJA-'PERDINEC'→PEZDIREC-×3" in qa, "")

    # ---------- I11: parish.ts-kaskada ----------
    src = open(PARISH_TS, encoding="utf-8").read()
    check("I11a P175-blok-komentar-v-parish.ts",
          "P175: MRLIŠKA KNJIGA 04894, LETO 1909" in src, "")
    check("I11b P175-11-blokov-whatSi-potrditve (DVOJČKI + KOREKCIJE + h86!)",
          all(k in src for k in ["ŠILAK-DVOJČKI", "P174-lead-'84'-KOREKCIJA",
                                 "1. MRLIŠKI VPIS KADARKOLI", "NOVI-DUHOVNIK-#16",
                                 "ŠIMEC-h18-vez", "P168-lead-'Dehlič?-h33'", "h13-CLUSTER-vez",
                                 "PEZDIREC-h85-vez-1908/09", "diag-'Toma'-KOREKCIJA",
                                 "3-priimka-hiše", "diag-'76'-ZAVRJEN"]), "")
    check("I11c P174-KOREKCIJA-parish.ts-×3-bloki (PERDINEC→PEZDIREC z25/z70/z71!)",
          src.count("P175-KOREKCIJA") == 3, f"{src.count('P175-KOREKCIJA')}")
    check("I11d P176-LEAD-v-parish.ts (s126-zap1–12 + s127!)",
          "P176 LEAD: mrliška 1910" in src and "s126-zap1–12" in src, "")
    check("I11e ni-04894-1916-blokov-še (P182-lead!; P181 = 1915 sedaj v korpusu!)",
          re.search(r'bookSignature: "04894",\s*year: 1916', src) is None, "")

    # ---------- I12: honesty ----------
    check("I12 honesty ≥6 (honesty-1–7!)",
          len(d["honesty"]) >= 6, str(len(d["honesty"])))
    check("I12b honesty-Bitnar-konservativna-lekcija ([~]-status-OHRANJEN!)",
          any("Bitnar" in x for x in d["honesty"]), "")

    # ---------- I13: --live (HTTP!) ----------
    if live:
        st, body = http_get(BOOK_URL)
        ok = st == 200 and (b"04894" in body or b"podzemelj" in body.lower())
        check("I13a --live matricula-04894-dostopen", st == 200, f"HTTP {st}")
        check("I13b dokaz-Griblje == parish.ts-Griblje (1:1!)",
              sorted([e["houseNo"] for e in grb]) == sorted([v["houseNo"] for v in d1909]),
              f"{sorted([e['houseNo'] for e in grb])}")
        check("I13c dokaz-skeni == parish.ts-skeni (1:1!)",
              sorted([(e["houseNo"], e["scan"], e["page"]) for e in grb])
              == sorted([(v["houseNo"], v["scan"], v["page"]) for v in d1909]), "")

    ok_n = sum(1 for _, ok, _ in results if ok)
    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'}: {name}" + (f" — {detail}" if detail and not ok else ""))
    print(f"\nP175: {ok_n}/{len(results)} " + ("PASS ✓" if ok_n == len(results) else "FAIL ✗"))
    return 0 if ok_n == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
