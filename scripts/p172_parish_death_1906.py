#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P172 — verifikator MRLIŠKE knjige 04894, leto 1906 (20. → 21. polno leto).
Celoten neodvisen preracun iz bundled parish.ts + dokaz-JSON + qa + kaskada.
I-checki I1–I13 (vzorec P153–P171); --live = dodatna HTTP verifikacija
matricula-online.eu.
P172-novosti: 55 vpisov (56-oštevilčenih — PISAR-DUPLIKAT-21 1.-v-liniji!) /
10 GRIBLJE (padec-rekorda 17→16→16→10!) / 9 hiš + h58-×2-v-1-letu + 5
GLAVE-NAPAKE = REKORD-LINIJE-IZENAČEN (s104-'48/1905'-'4'-za-'1'-NOV-vzorec +
s105-'18906' + s106/s107/s108-'181906'-×3 — pisar-'18'-navada ×5-v-1-letu!) +
NOV DUHOVNIK #13: J. R. KUHINEK (×3-GRIBLJE + s106-DOMINANTA!) + PODLOGAR-
kapelan-×1 + FLORJANČIČ-×2-1.-mrliški-podpisi + PEZDIREC-era-13 (×1 = era-×12-
v-5-letih!) + BRINEC-vez (1906-ANA-vdova-h49 → 1907-ANTON-vdovec-h49!) +
VLM-korekcije ×7 (imen ×4 + bolezni ×3) + h39/h77 = 1.-MRLIŠKI-VPIS-KADARKOLI
×2 (29.-PT-vez-kandidat!) + diag-vizualna-zaslona ×7-skenov-P170-metoda
(rows-v3-FAIL-s107–s110!) + MEJA-1906/07 = s109 (14. POTRDITEV — P171-lead-
[~ s107+?]-KOREKCIJA!).
Kumulativ: vitals 966 → 976, mrliški bloki 04894 267 → 277, p80 hiše 91
NESPREMENJENE (h39/h77-ŽE-v-p80!), korpus 93 NESPREMENJEN, PT 29."""
import json, os, re, sys, time, urllib.request, urllib.error

DOKAZ = "research/issue17/parish-death-1906.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
QA_TS = "src/lib/qa-parish.ts"
PARISH_TS = "src/data/atlas/parish.ts"
NOTES = "research/issue17/parish-death-1906-notes.md"

EXPECTED_ENTRIES = 56   # 10 Griblje + 46 ne-Griblje-s-* (vključno-z-DUP-21!)
EXPECTED_EXCLUDED = 3
EXPECTED_ANOMALIES = 10
EXPECTED_CROSSCHECKS = 5
GRIBLJE_HOUSES = "18,19,20,39,44,49,57,58,77"
GRIBLJE_ZAPS = [1, 6, 16, 21, 23, 29, 34, 35, 48, 54]
VITALS_TOTAL = 1444             # 1205 + 14! (P190 = KONEC-KNJIGE!)
BLOKI_04894 = 520               # 506 + 14! (P190 = KONEC-KNJIGE!)
P80_HOUSES = 92                  # NESPREMENJENO (h39/h77-ŽE-v-p80!)
KORPUS_HOUSES = 93               # NESPREMENJENO
NEW_SCANS = [105, 106, 107, 108]  # s104-reuse (P171-lead-diag!)

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
    grb = [e for e in ent if not str(e["houseNo"]).endswith("*")]

    # ---------- I1: dokaz ----------
    check("I1 dokaz obstaja + status", d["status"] == "SAMPLE-TRANSCRIPTION-D1906", d["status"])
    check("I1b 56 vnosov (10-Griblje + 46-ne-Griblje-s-*!)", len(ent) == EXPECTED_ENTRIES, str(len(ent)))
    check("I1c 3 excluded / 10 anomalij / 5 križnih",
          len(d["excluded"]) == EXPECTED_EXCLUDED and len(d["anomalies"]) == EXPECTED_ANOMALIES
          and len(d["crossChecks"]) == EXPECTED_CROSSCHECKS,
          f"{len(d['excluded'])}/{len(d['anomalies'])}/{len(d['crossChecks'])}")

    # ---------- I2: okvir ----------
    check("I2 1906 = 55 vpisov (56-oštevilčenih!) / 10 Griblje / 9 hiš",
          fr["vpisi"] == 55 and fr["zap_oštevilčenih"] == 56
          and fr["griblje_vpisi"] == 10 and fr["hise"] == 9,
          f"{fr['vpisi']}/{fr['zap_oštevilčenih']}/{fr['griblje_vpisi']}/{fr['hise']}")
    check("I2b PISAR-DUPLIKAT-21 (1.-v-liniji!) + 5-GLAVE-NAPAKE + rast-17→16→16→10",
          "dup_zaporedna" in fr and "21" in fr["dup_zaporedna"]
          and len(fr["glave_napake"]) == 5, str(len(fr["glave_napake"])))
    check("I2c hiše = 9 različnih (h58-×2-v-1-letu!)",
          ",".join(sorted({str(e["houseNo"]) for e in grb}, key=int)) == GRIBLJE_HOUSES,
          ",".join(sorted({e["houseNo"] for e in grb}, key=int)))

    # ---------- I3: zap-continuity ----------
    zaps = sorted(int(e["zap"]) for e in grb)
    check("I3a Griblje-zap: 1,6,16,21,23,29,34,35,48,54",
          zaps == GRIBLJE_ZAPS, str(zaps))
    check("I3b 56-oštevilčenih / 55-vpisov (DUP-21!)",
          fr["zap_oštevilčenih"] == 56 and fr["vpisi"] == 55
          and fr["neštevilčenih"] == 0, "")
    dup21 = [e for e in ent if e["zap"] == 21]
    check("I3c DUP-21 = 2-vrstice (s105-Maj-10-Griblje + s106-Maj-22-Klošter!)",
          len(dup21) == 2 and "Griblje" in dup21[0]["vas"] and "Klošter" in dup21[1]["vas"],
          f"{[(e['scan'], e['vas'], e['mesec']) for e in dup21]}")

    # ---------- I4: invarianta ----------
    check("I4 stran == sken − 1 (vseh 56 — 77.–81. potrditev!)",
          all(e["page"] == e["scan"] - 1 for e in ent), "")
    check("I4b skeni: s104-reuse + s105–s108 (5-skupaj!)",
          all(e["scan"] in [104] + NEW_SCANS for e in ent), str(sorted({e["scan"] for e in ent})))

    vit = parse_house_vitals()
    d04894 = [v for v in vit if v["bookSignature"] == "04894"]
    d1906 = [v for v in d04894 if v["year"] == 1906]

    def v_hn(vlist, hn):
        return next(v for v in vlist if v["houseNo"] == hn)

    # ---------- I5: hišne veze (parish.ts-whatSi-long-forme!) ----------
    e49 = v_hn(d1906, "49")
    check("I5a h49-Ana-BRINEC = P171-lead-POTRJEN-×3 (kompozit-'49'-jasno-NI-'19'!)",
          "P171-lead" in e49["whatSi"] and "POTRJEN" in e49["whatSi"]
          and "BRINEC" in e49["whatSi"] and "h19" in e49["whatSi"], "")
    e20 = v_hn(d1906, "20")
    check("I5b h20-Katarina-PEZDIREC = P171-lead-POTRJEN + era-13-nadaljevanje (×12-v-5-letih!)",
          "P171-lead" in e20["whatSi"] and "PEZDIREC" in e20["whatSi"]
          and "era-13-nadaljevanje" in e20["whatSi"], "")
    e39 = v_hn(d1906, "39")
    check("I5c h39-Katarina-ŠIMEC = 1. MRLIŠKI VPIS KADARKOLI (29.-PT-vez-kandidat!)",
          "1. MRLIŠKI VPIS KADARKOLI" in e39["whatSi"] and "ŠIMEC" in e39["whatSi"]
          and "29.-PT-vez-kandidat" in e39["whatSi"], "")
    e77 = v_hn(d1906, "77")
    check("I5d h77-Jurij-JOČEK = 1. MRLIŠKI VPIS KADARKOLI (VLM-'Potokar'-ZAVRJENA!)",
          "1. MRLIŠKI VPIS KADARKOLI" in e77["whatSi"] and "JOČEK" in e77["whatSi"]
          and "Potokar" in e77["whatSi"], "")
    e58a = [v for v in d1906 if v["houseNo"] == "58" and "10 MESECEV" in v["whatSi"]]
    e58b = [v for v in d1906 if v["houseNo"] == "58" and "49 LET" in v["whatSi"]]
    check("I5e h58-×2-v-1-letu (z29-Matija-TOŽEK-10-mes + z35-Janez-FOČEK-49!)",
          len(e58a) == 1 and len(e58b) == 1 and "TOŽEK" in e58a[0]["whatSi"]
          and "FOČEK" in e58b[0]["whatSi"] and "×2-v-1-letu" in e58b[0]["whatSi"], "")
    e18 = v_hn(d1906, "18")
    check("I5f h18-Alojzij-ŠIMEC = 6. mrliški vpis (VLM-'Timec'-ZAVRJENA!)",
          "6. mrliški vpis" in e18["whatSi"] and "Timec" in e18["whatSi"]
          and "ŠIMEC" in e18["whatSi"], "")
    e19 = v_hn(d1906, "19")
    check("I5g h19-Janez-KRIŽE = NOV-DUHOVNIK-#13-KUHINEK (1.-mrliški-podpis!)",
          "KRIŽE" in e19["whatSi"] and "KUHINEK" in e19["whatSi"]
          and "NOVI DUHOVNIK" in e19["whatSi"], "")
    e57 = v_hn(d1906, "57")
    check("I5h h57-Matija-URH = 4. mrliški vpis + podpis-BREZ (z33–z36!)",
          "4. mrliški vpis" in e57["whatSi"] and "URH" in e57["whatSi"]
          and "podpis-BREZ" in e57["whatSi"], "")
    e44 = v_hn(d1906, "44")
    check("I5i h44-Matija-ŠTRUKELJ = 2. mrliški vpis (19-letna-vrzela-1887!)",
          "2. mrliški vpis" in e44["whatSi"] and "ŠTRUKELJ" in e44["whatSi"]
          and "19-letna-vrzela" in e44["whatSi"], "")

    # ---------- I6: kumulativ + parish.ts ----------
    check("I6a vitals 976", len(vit) == VITALS_TOTAL, str(len(vit)))
    check("I6b mrliški bloki 04894 = 277", len(d04894) == BLOKI_04894, str(len(d04894)))
    check("I6c bloki 1906 = 10", len(d1906) == 10, str(len(d1906)))
    check("I6d bloki 1906: skeni 104–108 + stran == sken − 1",
          all(v["scan"] and 104 <= v["scan"] <= 108 and v["page"] == v["scan"] - 1 for v in d1906), "")
    check("I6d2 bloki 1908+ ne obstajajo (P174-lead!; P172 = 1906 sedaj v korpusu!)",
          all(v["year"] < 1925 for v in d04894), "")
    p80 = open("scripts/p80_parish_md_books.py", encoding="utf-8").read()
    check("I6f p80-skripta pini 976 + 91 + gap-18 (vitals-P172-kaskada!)",
          "len(vitals) == 1100" in p80 and "len(houses) == 94" in p80 and "len(gap) == 18" in p80, "")
    houses_all = {v["houseNo"] for v in vit if v["houseNo"].isdigit()}
    check("I6g korpus = 93 hiš (NESPREMENJENO — h39/h77-ŽE-v-korpusu!)",
          len(houses_all) == KORPUS_HOUSES, str(len(houses_all)))

    # ---------- I7: forenzika (anomalije A1–A10!) ----------
    a1 = next(x for x in d["anomalies"] if x["id"] == "A1")
    check("I7a A1: 5-GLAVE-NAPAKE-REKORD-IZENAČEN (48/1905 + 18906 + 181906-×3!)",
          "5 GLAVE-NAPAKE" in a1["opis"] and "48/1905" in a1["opis"]
          and "18906" in a1["opis"] and "181906" in a1["opis"], "")
    a2 = next(x for x in d["anomalies"] if x["id"] == "A2")
    check("I7b A2: PISAR-DUPLIKAT-zaporedna-21 (1.-v-liniji — 56-oštevilčenih = 55-vpisov!)",
          "DUPLIKAT-zaporedna-21" in a2["opis"], "")
    a3 = next(x for x in d["anomalies"] if x["id"] == "A3")
    check("I7c A3: NOV-DUHOVNIK-#13-KUHINEK (×3-GRIBLJE + s106-DOMINANTA!)",
          "KUHINEK" in a3["opis"] and "#13" in a3["opis"], "")
    a7 = next(x for x in d["anomalies"] if x["id"] == "A7")
    check("I7d A7: VLM-HALUCINACIJE-×4-imen (Potokar→JOČEK + Timec→ŠIMEC!)",
          "JOČEK" in a7["opis"] and "ŠIMEC" in a7["opis"] and "KRIŽE" in a7["opis"], "")
    a8 = next(x for x in d["anomalies"] if x["id"] == "A8")
    check("I7e A8: VLM-korekcije-boleznih-×3 (Šarost→SLABOST + Nadluhek/Nadluka→NADRUKA!)",
          "SLABOST" in a8["opis"] and "NADRUKA" in a8["opis"]
          and "Nadluka" in a8["opis"], "")

    # ---------- I8: meje + lead ----------
    c1 = d["crossChecks"][0]["opis"]
    check("I8a zap-kontinuiteta (C1 — 56-oštevilčenih!)",
          "56-oštevilčenih" in c1 or "56-oštevilčenih" in c1, c1[:60])
    c5 = d["crossChecks"][4]["opis"]
    check("I8b meja 1905/06 = s104 + meja 1906/07 = s109 (14.-POTRDITEV — KOREKCIJA!)",
          "s104" in fr["meja_1905_06"] and "s109" in fr["meja_1906_07"]
          and "14. POTRDITEV" in fr["meja_1906_07"]
          and "KOREKCIJA" in fr["meja_1906_07"], "")
    ns = json.dumps(d["nextSteps"], ensure_ascii=False)
    check("I8c P173-lead v dokazu (1907 + BRINEC-Anton + SPOL-KOREKCIJA!)",
          "P173-lead" in ns and "1907" in ns and "Anton-BRINEC" in ns
          and "SPOL-KOREKCIJA" in ns, "")
    check("I8d X1–X3 excluded (1905-vrstici + s109 + s110!)",
          len(d["excluded"]) == 3 and "1905" in d["excluded"][0]["opis"]
          and "s109" in d["excluded"][1]["opis"] and "s110" in d["excluded"][2]["opis"], "")

    # ---------- I9: demografija ----------
    duh = [e["duhovnik"] for e in grb]
    n_len = sum(1 for x in duh if "Lengsfeld" in x)
    n_kuh = sum(1 for x in duh if "KUHINEK" in x)
    n_flor = sum(1 for x in duh if "FLORJANČIČ" in x)
    n_brez = sum(1 for x in duh if "BREZ" in x)
    check("I9a duhovniki-Griblje: Lengsfeld-×3 + KUHINEK-×3 + brez-×2 + Florjančič-×2 = 10",
          n_len == 3 and n_kuh == 3 and n_brez == 2 and n_flor == 2,
          f"L{n_len}/K{n_kuh}/B{n_brez}/F{n_flor}")
    meseci = {}
    for e in grb:
        k = (e["mesec"] or "")[:3]
        meseci[k] = meseci.get(k, 0) + 1
    check("I9b meseci Griblje: Jan1·Feb1·Mar1·Maj1·Jun1·Avg1·Okt2·Dec2 (8-mesecev!)",
          meseci.get("Jan") == 1 and meseci.get("Feb") == 1 and meseci.get("Mar") == 1
          and meseci.get("Maj") == 1 and meseci.get("Jun") == 1 and meseci.get("Avg") == 1
          and meseci.get("Okt") == 2 and meseci.get("Dec") == 2, str(meseci))
    check("I9c starostni-razpon 1-mes → 78-let (z21/z29 → z34!)",
          any("1 MESEC" in e["starost"] or "1 mesec" in e["starost"] for e in grb)
          and any("78 LET" in e["starost"] or "78 let" in e["starost"] for e in grb), "")
    otroci = [e for e in grb if "MESEC" in e["starost"].upper() or "mesecev" in e["starost"]]
    check("I9d otroška-smrt ≥3/10 (z21-1-mes + z29-10-mes + z54-5-mes!)",
          len(otroci) >= 3, str([(e["houseNo"], e["starost"]) for e in otroci]))
    prev = [e["previden"] for e in grb]
    check("I9e previden-Griblje: '1' ×7 + PRAZNO ×3 (z21 + z29-'.' + z54!)",
          sum(1 for x in prev if x == "1") == 7, str(prev))

    # ---------- I10: qa-parish + pin-kaskada ----------
    qa = open(QA_TS, encoding="utf-8").read()
    check("I10a qa-p172 = 173. kontrola", "qa-p172-parish-death-1906" in qa, "")
    check("I10b qa-parish pini 976 + 277 (P172-kaskada!)",
          qa.count("!== 1444") >= 91 and qa.count("!== 446") >= 25,
          f"976×{qa.count('!== 976')}/277×{qa.count('!== 277')}")
    check("I10c qa-parish guardi ≥1916 (20× — P172-kaskada!)",
          qa.count(">= 1916") >= 28, f"{qa.count('>= 1915')}")
    check("I10d qa-p171-govori-P172-LEAD (1906-BRINEC-PEZDIREC!)",
          "P172-LEAD" in qa and "1906" in qa, "")

    # ---------- I11: parish.ts-kaskada ----------
    src = open(PARISH_TS, encoding="utf-8").read()
    check("I11a P172-blok-komentar-v-parish.ts",
          "P172: mrliška 1906" in src, "")
    check("I11b P172-10-blokov-whatSi-potrditve (BRINEC + PEZDIREC + KUHINEK + JOČEK!)",
          all(k in src for k in ["P171-lead-'zap1-Ana-BRINEC-h49-66-Jan' = POTRJEN-×3",
                                 "P171-lead-'zap6-Katarina-PEZDIREC-h20-61-Feb' = POTRJEN",
                                 "NOV DUHOVNIK #13" if "NOV DUHOVNIK #13" in src else "NOVI DUHOVNIK-#13",
                                 "VLM-'Potokar'-ZAVRJENA"]), "")
    check("I11c P173-LEAD-v-parish.ts (s109-zap1–11-ŽE-vidni!)",
          "P173-LEAD: 1907" in src and "Anton-BRINEC" in src.replace("ANTON", "Anton"), "")
    check("I11d ni-04894-1916-blokov-še (P182-lead!; P181 = 1915 sedaj v korpusu!)",
          re.search(r'bookSignature: "04894",\s*year: 1916', src) is None, "")

    # ---------- I12: honesty ----------
    check("I12 honesty ≥5 (honesty-1–7!)",
          len(d["honesty"]) >= 5, str(len(d["honesty"])))
    check("I12b honesty-rows-v3-FAIL-lekcija (diag-grid-recept-REŠILA!)",
          any("rows-v3" in x for x in d["honesty"]), "")

    # ---------- I13: --live (HTTP!) ----------
    if live:
        st, body = http_get(BOOK_URL)
        ok = st == 200 and b"04894" in body or st == 200 and b"podzemelj" in body.lower()
        check("I13a --live matricula-04894-dostopen", st == 200, f"HTTP {st}")
        # dokaz-številke == parish.ts-številke (1:1!)
        check("I13b dokaz-Griblje == parish.ts-Griblje (1:1!)",
              sorted([e["houseNo"] for e in grb]) == sorted([v["houseNo"] for v in d1906]),
              f"{sorted([e['houseNo'] for e in grb])}")
        check("I13c dokaz-skeni == parish.ts-skeni (1:1!)",
              sorted([(e["houseNo"], e["scan"], e["page"]) for e in grb])
              == sorted([(v["houseNo"], v["scan"], v["page"]) for v in d1906]), "")

    ok_n = sum(1 for _, ok, _ in results if ok)
    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'}: {name}" + (f" — {detail}" if detail and not ok else ""))
    print(f"\nP172: {ok_n}/{len(results)} " + ("PASS ✓" if ok_n == len(results) else "FAIL ✗"))
    return 0 if ok_n == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
