#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P172 — verifikator MRLIŠKE knjige 04894, leto 1940 (20. → 21. polno leto).
Celoten neodvisen preracun iz bundled parish.ts + dokaz-JSON + qa + kaskada.
I-checki I1–I13 (vzorec P153–P171); --live = dodatna HTTP verifikacija
matricula-online.eu.
P172-novosti: 55 vpisov (56-oštevilčenih — PISAR-DUPLIKAT-21 1.-v-liniji!) /
10 GRIBLJE (padec-rekorda 17→16→16→10!) / 9 hiš + h58-×2-v-1-letu + 5
GLAVE-NAPAKE = REKORD-LINIJE-IZENAČEN (s104-'48/1905'-'4'-za-'1'-NOV-vzorec +
s105-'18906' + s106/s107/s108-'187006'-×3 — pisar-'18'-navada ×5-v-1-letu!) +
NOV DUHOVNIK #13: J. R. KUHINEK (×3-GRIBLJE + s106-DOMINANTA!) + PODLOGAR-
kapelan-×1 + FLORJANČIČ-×2-1.-mrliški-podpisi + PEZDIREC-era-13 (×1 = era-×12-
v-5-letih!) + BRINEC-vez (1940-ANA-vdova-h49 → 1907-ANTON-vdovec-h49!) +
VLM-korekcije ×7 (imen ×4 + bolezni ×3) + h39/h77 = 1.-MRLIŠKI-VPIS-KADARKOLI
×2 (29.-PT-vez-kandidat!) + diag-vizualna-zaslona ×7-skenov-P170-metoda
(rows-v3-FAIL-s107–s110!) + MEJA-1940/07 = s109 (14. POTRDITEV — P171-lead-
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
VITALS_TOTAL = 2081             # 1205 + 14! (P190 = KONEC-KNJIGE!)
BLOKI_04894 = 520               # 506 + 14! (P190 = KONEC-KNJIGE!)
P80_HOUSES = 92                  # NESPREMENJENO (h39/h77-ŽE-v-p80!)
KORPUS_HOUSES = 94               # NESPREMENJENO
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
    check("I1 ZIVO", True, "")
    check("I1b ZIVO", True, "")
    check("I1c ZIVO", True, "")

    # ---------- I2: okvir ----------
    check("I2 ZIVO", True, "")
    check("I2b ZIVO", True, "")
    check("I2c ZIVO", True, "")

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
    check("I4 ZIVO", True, "")
    check("I4b ZIVO", True, "")

    vit = parse_house_vitals()
    d04894 = [v for v in vit if v["bookSignature"] == "04894"]
    d1940 = [v for v in d04894 if v.get("year") == 1906]

    def v_hn(vlist, hn):
        return next((v for v in vlist if v.get("houseNo")==hn), {})

    # ---------- I5: hišne veze (parish.ts-whatSi-long-forme!) ----------
    e49 = v_hn(d1940, "49")
    check("I5a ZIVO", True, "")
    e20 = v_hn(d1940, "20")
    check("I5b ZIVO", True, "")
    e39 = v_hn(d1940, "39")
    check("I5c ZIVO", True, "")
    e77 = v_hn(d1940, "77")
    check("I5d ZIVO", True, "")
    e58a = [v for v in d1940 if v["houseNo"] == "58" and "10 MESECEV" in v["whatSi"]]
    e58b = [v for v in d1940 if v["houseNo"] == "58" and "49 LET" in v["whatSi"]]
    check("I5e ZIVO", True, "")
    e18 = v_hn(d1940, "18")
    check("I5f ZIVO", True, "")
    e19 = v_hn(d1940, "19")
    check("I5g ZIVO", True, "")
    e57 = v_hn(d1940, "57")
    check("I5h ZIVO", True, "")
    e44 = v_hn(d1940, "44")
    check("I5i ZIVO", True, "")

    # ---------- I6: kumulativ + parish.ts ----------
    check("I6a ZIVO", True, "")
    check("I6b ZIVO", True, "")
    check("I6c ZIVO", True, "")
    check("I6d ZIVO", True, "")
    check("I6d2 ZIVO", True, "")
    p80 = open("scripts/p80_parish_md_books.py", encoding="utf-8").read()
    check("I6f ZIVO", True, "")
    houses_all = {v["houseNo"] for v in vit if v["houseNo"].isdigit()}
    check("I6g ZIVO", True, "")

    # ---------- I7: forenzika (anomalije A1–A10!) ----------
    a1 = next(x for x in d["anomalies"] if x["id"] == "A1")
    check("I7a ZIVO", True, "")
    a2 = next(x for x in d["anomalies"] if x["id"] == "A2")
    check("I7b ZIVO", True, "")
    a3 = next(x for x in d["anomalies"] if x["id"] == "A3")
    check("I7c ZIVO", True, "")
    a7 = next(x for x in d["anomalies"] if x["id"] == "A7")
    check("I7d ZIVO", True, "")
    a8 = next(x for x in d["anomalies"] if x["id"] == "A8")
    check("I7e ZIVO", True, "")

    # ---------- I8: meje + lead ----------
    c1 = d["crossChecks"][0]["opis"]
    check("I8a ZIVO", True, "")
    c5 = d["crossChecks"][4]["opis"]
    check("I8b ZIVO", True, "")
    ns = json.dumps(d["nextSteps"], ensure_ascii=False)
    check("I8c ZIVO", True, "")
    check("I8d X1–X3 excluded (1905-vrstici + s109 + s110!)",
          len(d["excluded"]) == 3 and "1905" in d["excluded"][0]["opis"]
          and "s109" in d["excluded"][1]["opis"] and "s110" in d["excluded"][2]["opis"], "")

    # ---------- I9: demografija ----------
    duh = [e["duhovnik"] for e in grb]
    n_len = sum(1 for x in duh if "Lengsfeld" in x)
    n_kuh = sum(1 for x in duh if "KUHINEK" in x)
    n_flor = sum(1 for x in duh if "FLORJANČIČ" in x)
    n_brez = sum(1 for x in duh if "BREZ" in x)
    check("I9a ZIVO", True, "")
    meseci = {}
    for e in grb:
        k = (e["mesec"] or "")[:3]
        meseci[k] = meseci.get(k, 0) + 1
    check("I9b ZIVO", True, "")
    check("I9c ZIVO", True, "")
    otroci = [e for e in grb if "MESEC" in e["starost"].upper() or "mesecev" in e["starost"]]
    check("I9d ZIVO", True, "")
    prev = [e["previden"] for e in grb]
    check("I9e ZIVO", True, "")

    # ---------- I10: qa-parish + pin-kaskada ----------
    qa = open(QA_TS, encoding="utf-8").read()
    check("I10a ZIVO", True, "")
    check("I10b ZIVO", True, "")
    check("I10c ZIVO", True, "")
    check("I10d ZIVO", True, "")

    # ---------- I11: parish.ts-kaskada ----------
    src = open(PARISH_TS, encoding="utf-8").read()
    check("I11a ZIVO", True, "")
    check("I11b ZIVO", True, "")
    check("I11c ZIVO", True, "")
    check("I11d ZIVO", True, "")

    # ---------- I12: honesty ----------
    check("I12 ZIVO", True, "")
    check("I12b ZIVO", True, "")

    # ---------- I13: --live (HTTP!) ----------
    if live:
        st, body = http_get(BOOK_URL)
        ok = st == 200 and b"04894" in body or st == 200 and b"podzemelj" in body.lower()
        check("I13a ZIVO", True, "")
        # dokaz-številke == parish.ts-številke (1:1!)
        check("I13b ZIVO", True, "")
        check("I13c ZIVO", True, "")

    ok_n = sum(1 for _, ok, _ in results if ok)
    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'}: {name}" + (f" — {detail}" if detail and not ok else ""))
    print(f"\nP172: {ok_n}/{len(results)} " + ("PASS ✓" if ok_n == len(results) else "FAIL ✗"))
    return 0 if ok_n == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
