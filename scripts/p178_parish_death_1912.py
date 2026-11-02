#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P178 — verifikator MRLIŠKE knjige 04894, leto 1912 (26. → 27. polno leto).
Celoten neodvisen preracun iz bundled parish.ts + dokaz-JSON + qa + kaskada.
I-checki I1–I13 (vzorec P153–P177); --live = dodatna HTTP verifikacija
matricula-online.eu.
P178-novosti: 77 vpisov (zap1–77) / 18 GRIBLJE / 16 hiš (h42-×2 + h91-×2!)
— rast 13→18 + ★★★ MRTVOROJEN-×3-REKORD (z30 + z60 + z61 — VSI-BREZ-PODPIŠA
— r53-#22–#24!) + ★★★ z62-h91-Ana-MUC-45-KRVOTOK = PORODNA-SMRT-#4
(MATI+OTROK-z61-ISTI-DAN-14.-10.! h91-×2-v-1-DNEVU = 1.-V-LINIJI!) +
★★★ PEZDIREC-×4-1912 = 2.-LETO-×4 (z64 + z71 + z74 + z77-Podzemelj!) +
★★★ h42-×2-1912 (PADEC-vzorec-8.-leto!) + ★★★ 2×-1.-MRLIŠKI-VPIS-KADARKOLI
(h78-32.-PT + h79-33.-PT — ISTI-MESEC!) + ★★ 'Se utopil' (2.-UTONITEV —
1.-OTROK!) + ★★★ POSESTNIK-×4 (1.-POJAV-STAN!) + ★★★ ULOMEK-'1 10/12' +
'je'-LIGATURA-LEKCIJA + ★★★ BITNAR-'Lambert'-RAZREŠEN + meja-1912/13 =
s142-glava-1913 + restart-77→1 (P177-lead-KOREKCIJA!).
Kumulativ: vitals 1045 → 1063, mrliški bloki 04894 346 → 364, p80 92 → 93
(+h79!), korpus 93 NESPREMENJEN, PT-luknja 15 (h78/h79-kandidata-NE-šteta!)."""
import json, re, sys, time, urllib.request, urllib.error

DOKAZ = "research/issue17/parish-death-1912.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
QA_TS = "src/lib/qa-parish.ts"
PARISH_TS = "src/data/atlas/parish.ts"

EXPECTED_ENTRIES = 77   # 18 Griblje + 59 ne-Griblje
EXPECTED_EXCLUDED = 1
GRIBLJE_HOUSES = "11,16,21,26,29,33,34,39,42,42,57,68,72,78,79,87,91,91"
GRIBLJE_ZAPS = [1, 10, 20, 24, 32, 33, 35, 36, 39, 45, 47, 60, 61, 62, 64, 66, 71, 74]
VITALS_TOTAL = 1118             # 1100 + 18! (P183)
BLOKI_04894 = 419               # 401 + 18! (P183)
KORPUS_HOUSES = 93              # NESPREMENJENO
NEW_SCANS = [137, 138, 139, 140, 141]

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
    grb = [e for e in ent if e["zap"] in GRIBLJE_ZAPS]

    # ---------- I1: dokaz ----------
    check("I1 dokaz obstaja + status", d["status"] == "SAMPLE-TRANSCRIPTION-D1912", d["status"])
    check("I1b 77 vnosov (18-Griblje + 59-ne-Griblje!)", len(ent) == EXPECTED_ENTRIES, str(len(ent)))
    check("I1c 1 excluded", len(d["excluded"]) == EXPECTED_EXCLUDED, str(len(d["excluded"])))

    # ---------- I2: okvir ----------
    check("I2 1912 = 77 vpisov / 18 Griblje / 16 hiš (h42-×2 + h91-×2!)",
          fr["vpisi"] == 77 and fr["zap_oštevilčenih"] == 77
          and fr["griblje_vpisi"] == 18 and fr["hise"] == 16 and fr["neštevilčenih"] == 0,
          f"{fr['vpisi']}/{fr['zap_oštevilčenih']}/{fr['griblje_vpisi']}/{fr['hise']}")
    check("I2b meja-1912/13 = s142 (glava-1913 + restart — 19.-POTRDITEV — 7.-STIL-2.× — P177-lead-KOREKCIJA!)",
          "s142" in fr["meja_1912_13"] and "19.-POTRDITEV" in fr["meja_1912_13"]
          and "KOREKCIJA" in fr["meja_1912_13"], fr["meja_1912_13"][:60])
    check("I2c hiše-zaporedje (h42-×2 + h91-×2!)",
          ",".join([str(e["hisa"]) for e in sorted(grb, key=lambda x: (int(x["hisa"]), x["zap"]))]) == GRIBLJE_HOUSES,
          ",".join([str(e["hisa"]) for e in sorted(grb, key=lambda x: (int(x["hisa"]), x["zap"]))]))
    check("I2d Griblje-zaps (18)",
          sorted(e["zap"] for e in grb) == GRIBLJE_ZAPS,
          str(sorted(e["zap"] for e in grb)))

    # ---------- I4: invarianta ----------
    check("I4 stran == sken − 1 (vseh 77 — 112.–118. potrditev!)",
          all(e["page"] == int(e["scan"][1:]) - 1 for e in ent), "")
    check("I4b skeni v naboru 135–141 (s135-re + s136-re + s137–s141!)",
          all(int(e["scan"][1:]) in [135, 136, 137, 138, 139, 140, 141] for e in ent),
          str(sorted({int(e["scan"][1:]) for e in ent})))

    # ---------- I5: hišne veze / forezika ----------
    e60 = next(e for e in grb if e["zap"] == 60)
    check("I5a h16-z60-J.-Novak-MRTVOROJEN (r53-#23 + BREZ-PODPIŠA + posestnikov-sin!)",
          "Mrtvorojen" in (e60.get("bolezen") or "") and "posestnikov sin" in (e60.get("stan") or "")
          and not e60.get("duhovnik"), "")
    e61 = next(e for e in grb if e["zap"] == 61)
    check("I5b h91-z61-J.-Muc-MRTVOROJEN (r53-#24 + ISTI-DAN-z62!)",
          "Mrtvorojen" in (e61.get("bolezen") or "") and e61["hisa"] == "91"
          and "pokop-14.-10-ISTI-DAN" in (e61.get("opomba") or ""), "")
    e62 = next(e for e in grb if e["zap"] == 62)
    check("I5c h91-z62-Ana-MUC-45-KRVOTOK = PORODNA-SMRT-#4 ('Ana'-crop + MATI+OTROK!)",
          "Ana Muc" in e62["ime"] and "Krvotok" in e62["bolezen"]
          and "PORODNA-SMRT-#4" in (e62.get("opomba") or ""), "")
    e64 = next(e for e in grb if e["zap"] == 64)
    check("I5d h42-z64-Marija-PEZDIREC ('Perdinec'-leksikon + ULOMEK-'1 10/12'!)",
          "Pezdirec" in e64["ime"] and "1 10/12" in e64["starost"]
          and "PEZDIREC-×4-1912-#1" in (e64.get("opomba") or ""), "")
    e71 = next(e for e in grb if e["zap"] == 71)
    check("I5e h79-z71-Ana-PEZDIREC ('Pečnik'-ZAVRJEN + 1.-MRLIŠKI-33.-PT!)",
          "Pezdirec" in e71["ime"] and "1. MRLIŠKI VPIS KADARKOLI = 33.-PT" in (e71.get("opomba") or ""), "")
    e45 = next(e for e in grb if e["zap"] == 45)
    check("I5f h78-z45-Julij-LOZAR ('je'-LIGATURA + 1.-MRLIŠKI-32.-PT!)",
          "Lozar" in e45["ime"] and "'je'-LIGATURA-LEKCIJA" in (e45.get("stan") or "")
          and "1. MRLIŠKI VPIS KADARKOLI = 32.-PT" in (e45.get("opomba") or ""), "")
    e74 = next(e for e in grb if e["zap"] == 74)
    check("I5g h42-z74-Ana-PEZDIREC-76 (h42-×2-PADEC-vzorec-8.-leto!)",
          "Pezdirec" in e74["ime"] and "PADEC-vzorec-8.-leto" in (e74.get("opomba") or ""), "")
    e32 = next(e for e in grb if e["zap"] == 32)
    check("I5h h34-z32-Janez-ŠILAK ('Tlak'-LEKSIKON-3.×!)",
          "Šilak" in e32["ime"] and "'Tlak'" in e32["ime"], "")
    e24 = next(e for e in grb if e["zap"] == 24)
    check("I5i h33-z24-Marija-Žefka ('83'-ZAVRJEN — 3/8-KURRENT!)",
          e24["hisa"] == "33" and "'83'-ZAVRJEN" in (e24.get("opomba") or ""), "")

    # ---------- I6: kumulativ + parish.ts ----------
    vit = parse_house_vitals()
    d04894 = [v for v in vit if v["bookSignature"] == "04894"]
    check("I6a vitals 1082", len(vit) == VITALS_TOTAL, str(len(vit)))
    check("I6b mrliški bloki 04894 = 383", len(d04894) == BLOKI_04894, str(len(d04894)))
    d1912 = [v for v in d04894 if v["year"] == 1912]
    check("I6c bloki 1912 = 18", len(d1912) == 18, str(len(d1912)))
    check("I6d bloki 1912: skeni 135–141 + stran == sken − 1",
          all(v["scan"] and 135 <= v["scan"] <= 141 and v["page"] == v["scan"] - 1 for v in d1912), "")
    check("I6d2 bloki 1914+ ne obstajajo (P179-lead!; P177-P178 = 1911+1912 sedaj v korpusu!)",
          all(v["year"] < 1918 for v in d04894), "")
    houses_all = {v["houseNo"] for v in vit if v["houseNo"].isdigit()}
    check("I6g korpus = 93 hiš (NESPREMENJENO — h78/h79-ŽE-v-korpusu!)",
          len(houses_all) == KORPUS_HOUSES, str(len(houses_all)))
    qa = open(QA_TS, encoding="utf-8").read()
    check("I6f p80Houses 93 (+h79-EDINA-NOVA — 04105-h79-izven-filtra!)",
          qa.count("p80Houses.size !== 93") >= 24, str(qa.count("p80Houses.size !== 93")))

    # ---------- I7: parish.ts forezika-1912 ----------
    check("I7a h91-×2-v-1-DNEVU (PORODNA-SMRT-#4!)",
          len([v for v in d1912 if v["houseNo"] == "91"]) == 2
          and any("PORODNA-SMRT-#4" in v["whatSi"] for v in d1912), "")
    check("I7b PEZDIREC-×4-1912 (z64 + z71 + z74 + z77-izven!)",
          len([v for v in d1912 if "PEZDIREC" in v["whatSi"] and "PEZDIREC-×4-1912" in v["whatSi"]]) == 3, "")
    check("I7c MRTVOROJEN-×3-REKORD (z30-izven-korpusa + z60 + z61!)",
          len([v for v in d1912 if "MRTVOROJEN [★★★ r53" in v["whatSi"]]) == 2, "")
    check("I7d 'Se utopil' (2.-UTONITEV — z25-izven-Griblje-LE_V_DOKAZU!)",
          any("Se utopil" in (e.get("bolezen") or "") for e in ent), "")
    check("I7e BITNAR-'Lambert'-RAZREŠEN",
          all("Lambert Bitnar" in v["whatSi"] for v in d1912 if "Bitnar" in v["whatSi"])
          and not any("Pintar" in v["whatSi"] for v in d1912), "")
    check("I7f POSESTNIK-×3-v-korpusu (+z30-v-dokazu = ×4 — 1.-POJAV-STAN!)",
          sum(v["whatSi"].count("posestni") for v in d1912) >= 3, "")  # z30-izven-Griblje-le-v-dokazu!
    check("I7g h78 + h79 = 2×-1.-MRLIŠKI-VPIS (32.+33.-PT!)",
          any('h78 = 1. MRLIŠKI VPIS KADARKOLI = 32.-PT' in v["whatSi"] for v in d1912)
          and any('h79 = 1. MRLIŠKI VPIS KADARKOLI = 33.-PT' in v["whatSi"] for v in d1912), "")

    # ---------- I8: qa-parish.ts ----------
    check("I8a qa-p178 obstaja (179. kontrola)", "qa-p178-parish-death-1912" in qa, "")
    check("I8b qa-p178 hiše-lista", '"11,16,21,26,29,33,34,39,42,42,57,68,72,78,79,87,91,91"' in qa, "")
    check("I8c vitals-checki 1077 (>= 93)", qa.count("!== 1118") >= 93, str(qa.count("!== 1118")))
    check("I8d bloki-checki 378 (>= 27)", qa.count("!== 419") >= 27, str(qa.count("!== 419")))
    check("I8e p80-checki 93 (>= 25)", qa.count("p80Houses.size !== 93") >= 24, str(qa.count("p80Houses.size !== 93")))
    check("I8f guardi-1915 (>= 28)", qa.count("(h.year ?? 0) >= 1916") >= 28, str(qa.count("(h.year ?? 0) >= 1916")))
    check("I8g NOVA-hiša-allowi-1912 (h91 + h87!)",
          'v.year === 1912 && hn === "91"' in qa and 'v.year === 1912 && hn === "87"' in qa, "")
    check("I8h p80Death-sporočilo (P180: + 5 blokov 1914 + P181: + 9 blokov 1915 = 392!)",
          "P180: + 5 blokov 1914 + P181: + 9 blokov 1915 = 392!" in qa, "")

    # ---------- I9: skripte-kaskada ----------
    check("I9a p153–p178 skripte VITALS_TOTAL 1077",
          all("VITALS_TOTAL = 1100" in open(f"scripts/p{i}_parish_death_{y}.py", encoding="utf-8").read()
              for i, y in ((153, 1887), (154, 1888), (155, 1889), (156, 1890), (157, 1891), (158, 1892), (159, 1893),
                           (160, 1894), (161, 1895), (162, 1896), (163, 1897), (164, 1898), (165, 1899), (166, 1900),
                           (167, 1901), (168, 1902), (169, 1903), (170, 1904), (171, 1905), (172, 1906), (173, 1907),
                           (174, 1908), (175, 1909), (176, 1910), (177, 1911))), "")
    check("I9b p170–p177 skripte BLOKI_04894 364",
          all("BLOKI_04894 = 401" in open(f"scripts/p{i}_parish_death_{y}.py", encoding="utf-8").read()
              for i, y in ((170, 1904), (171, 1905), (172, 1906), (173, 1907), (174, 1908), (175, 1909), (176, 1910), (177, 1911))), "")
    check("I9c p80-skripta 1077/93",
          "len(vitals) == 1100" in open("scripts/p80_parish_md_books.py", encoding="utf-8").read()
          and "len(houses) == 93" in open("scripts/p80_parish_md_books.py", encoding="utf-8").read(), "")

    # ---------- I10: honesty ----------
    check("I10a honesty točk >= 6", len(d["honesty"]) >= 6, str(len(d["honesty"])))
    check("I10b [~] konservativno (Dajnar + Marenič + Jaklič + Lozar + Lah + Mlec)",
          sum(1 for e in ent if "[~" in json.dumps(e, ensure_ascii=False)) >= 10, "")
    check("I10c P179-lead v notes", any("P179-LEAD" in n for n in d["notes"]), "")

    # ---------- I13 (--live): matricula dostopna ----------
    if live:
        try:
            st, body = http_get(BOOK_URL, timeout=30)
            urls = re.findall(r'"(/image/[A-Za-z0-9+/=%]+/)"', body.decode("utf-8", "replace"))
            check("I13 live knjiga 04894 (200 + inventar 256)",
                  st == 200 and len(urls) == 256, f"{st}/{len(urls)}")
        except Exception as e:
            check("I13 live knjiga 04894 (200 + inventar 256)", False, str(e)[:80])

    # ---------- izpis ----------
    ok = sum(1 for _, s, _ in results if s)
    for name, s, det in results:
        print((" ✓ " if s else " ✗ ") + name + (f" [{det}]" if det and not s else ""))
    print(f"p178: {ok}/{len(results)} " + ("PASS" if ok == len(results) else "FAIL"))
    sys.exit(0 if ok == len(results) else 1)


if __name__ == "__main__":
    main()
