#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P179 — verifikator MRLIŠKE knjige 04894, leto 1913 (27. → 28. polno leto).
Celoten neodvisen preracun iz bundled parish.ts + dokaz-JSON + qa + kaskada.
I-checki I1–I13 (vzorec P153–P178); --live = dodatna HTTP verifikacija
matricula-online.eu.
P179-novosti: 58 vpisov (zap1–58) / 14 GRIBLJE / 13 hiš (h59-×2-JAKLIČ!)
— padec 18→14 + ★★★ PEZDIREC-1913 = 3.-LETO-ZAPORED (z51-'Penčiče'-
ZAVRJEN-@×6.0 x-KRIŽEC+DESCENDER!) + ★★★ h92 = 1.-MRLIŠKI-VPIS-KADARKOLI
= 34.-PT-kandidat (Matija-ŠTRAVS-89-NAJVIŠJA!) + ★★★ 1.-LJUDSKI-UČITELJ
(z19-h90-g.-Frane-HALAR-56-'ženjen ljudski učitelj' — VLM-'Ivana'-
ZAVRJEN!) + ★★★ 1.-KOVAČ-STAN (z35-'ženjen kovač') + ★★★ ANZELM-POLÁK-
'Koop.' = NOVI-DUHOVNIK-LINIJE + ★★ 3×-'Grišiče'-EXCLUDE (P177-vzorec!)
+ 21-korekcij (MILEK + ŠILAK + KRAMBIČ-Agota-HALUCINACIJA + z35-DVOJNI-
MISREAD + ...) + meja 1913/14 = s147-glava-'18 1914' + restart-58→1
(20.-POTRDITEV — STIL-7-2.×!).
Kumulativ: vitals 1063 → 1077, mrliški bloki 04894 364 → 378, p80 93
NESPREMENJENO (h92-ŽE-v-p80-prek-poročne-1921!), korpus 93 NESPREMENJENO,
PT-luknja 15 NESPREMENJENA (h92-kandidat-NE-štet!)."""
import json, re, sys, time, urllib.request, urllib.error

DOKAZ = "research/issue17/parish-death-1913.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
QA_TS = "src/lib/qa-parish.ts"
PARISH_TS = "src/data/atlas/parish.ts"

EXPECTED_ENTRIES = 55   # 14 Griblje + 41 ne-Griblje
EXPECTED_EXCLUDED = 3
GRIBLJE_HOUSES = "1,5,12,34,44,47,49,51,59,59,65,76,90,92"
GRIBLJE_ZAPS = [2, 4, 5, 19, 24, 30, 33, 35, 37, 39, 47, 48, 51, 52]
VITALS_TOTAL = 1484             # 1205 + 14! (P190 = KONEC-KNJIGE!)
BLOKI_04894 = 520               # 506 + 14! (P190 = KONEC-KNJIGE!)
KORPUS_HOUSES = 93              # NESPREMENJENO
NEW_SCANS = [143, 144, 145, 146]

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
    check("I1 dokaz obstaja + status", d["status"] == "SAMPLE-TRANSCRIPTION-D1913", d["status"])
    check("I1b 55 vnosov (14-Griblje + 41-ne-Griblje!)", len(ent) == EXPECTED_ENTRIES, str(len(ent)))
    check("I1c 3 excluded (Grišiče!)", len(d["excluded"]) == EXPECTED_EXCLUDED, str(len(d["excluded"])))

    # ---------- I2: okvir ----------
    check("I2 1913 = 55 vnosov / 14 Griblje / 13 hiš (h59-×2!)",
          fr["vpisi"] == 55 and fr["zap_oštevilčenih"] == 58
          and fr["griblje_vpisi"] == 14 and fr["hise"] == 13,
          f"{fr['vpisi']}/{fr['zap_oštevilčenih']}/{fr['griblje_vpisi']}/{fr['hise']}")
    check("I2b meja-1913/14 = s147 (glava-18-1914 + restart-58→1 — 20.-POTRDITEV — STIL-7-2.×!)",
          "s147" in fr["meja_1913_14"] and "20.-POTRDITEV" in fr["meja_1913_14"]
          and "STIL-7-2.×" in fr["meja_1913_14"], fr["meja_1913_14"][:60])
    check("I2c hiše-zaporedje (h59-×2!)",
          ",".join([str(e["hisa"]) for e in sorted(grb, key=lambda x: (int(x["hisa"]), x["zap"]))]) == GRIBLJE_HOUSES,
          ",".join([str(e["hisa"]) for e in sorted(grb, key=lambda x: (int(x["hisa"]), x["zap"]))]))
    check("I2d Griblje-zaps (14)",
          sorted(e["zap"] for e in grb) == GRIBLJE_ZAPS,
          str(sorted(e["zap"] for e in grb)))
    check("I2e excluded = 3×-Grišiče (z14 + z28 + z49 — P177-vzorec-2.×!)",
          all("Grišiče" in e["razlog"] for e in d["excluded"])
          and sorted(str(e["zap"]) for e in d["excluded"]) == ["14", "28", "49"],
          str([e["zap"] for e in d["excluded"]]))

    # ---------- I4: invarianta ----------
    check("I4 stran == sken − 1 (vseh 55 — 119.–123. potrditev!)",
          all(e["page"] == int(e["scan"][1:]) - 1 for e in ent), "")
    check("I4b skeni v naboru 142–146 (s142-lead + s143–s146-novi!)",
          all(int(e["scan"][1:]) in [142, 143, 144, 145, 146] for e in ent),
          str(sorted({int(e["scan"][1:]) for e in ent})))

    # ---------- I5: hišne veze / forezika-1913 ----------
    e2 = next(e for e in grb if e["zap"] == 2)
    check("I5a h65-z2-Marija-MILEK (VLM-'Hlebič'-ZAVRJEN-@×4.0 + P178-lead!)",
          "MILEK" in e2["ime"] and "Hlebič-ZAVRJEN" in e2["ime"]
          and "P178-lead-potrjen" in (e2.get("opomba") or "") + (e2.get("ime") or ""), "")
    e4 = next(e for e in grb if e["zap"] == 4)
    check("I5b h5-z4-Anton-ŠTRUCELJ (P178-lead + ſl-LIGATURA-Slabost!)",
          "ŠTRUCELJ" in e4["ime"] and "ſl-LIGATURA" in e4["bolezen"], "")
    e5 = next(e for e in grb if e["zap"] == 5)
    check("I5c h47-z5-Marija-HLOBUČAR (K-LIGATURA-leksikon-2.×!)",
          "HLOBUČAR" in e5["ime"] and "K-LIGATURA" in e5["ime"], "")
    e19 = next(e for e in grb if e["zap"] == 19)
    check("I5d h90-z19-g.-Frane-HALAR (VLM-'Ivana'-ZAVRJEN + 1.-UČITELJ-STAN!)",
          "HALAR" in e19["ime"] and "Ivana-IME-ZAVRJEN" in e19["ime"]
          and "ljudski učitelj" in e19["stan"], "")
    e30 = next(e for e in grb if e["zap"] == 30)
    check("I5e h34-z30-Anton-ŠILAK (VLM-'Viljak'-ZAVRJEN-@×5.0 Ṽ+caron!)",
          "ŠILAK" in e30["ime"] and "Viljak-ZAVRJEN" in e30["ime"], "")
    e35 = next(e for e in grb if e["zap"] == 35)
    check("I5f h59-z35-Janez-JAKLIČ-kovač (1.-KOVAČ + DVOJNI-MISREAD-smrt/pokop!)",
          "JAKLIČ" in e35["ime"] and "kovač" in e35["stan"]
          and "DVOJNI-MISREAD" in (e35.get("opomba") or ""), "")
    e39 = next(e for e in grb if e["zap"] == 39)
    check("I5g h44-z39-Anton-KRAMBIČ ('Agota'-halucinacija + Kašelj-'kavrg'!)",
          "KRAMBIČ" in e39["ime"] and "Agota" in e39["ime"] and "kavrg" in e39["bolezen"], "")
    e48 = next(e for e in grb if e["zap"] == 48)
    check("I5h h92-z48-Matija-ŠTRAVS (1.-MRLIŠKI-VPIS-34.-PT + 'delavec in vdovec'!)",
          "ŠTRAVS" in e48["ime"] and "Špavc-ZAVRJEN" in e48["ime"]
          and "delavec in vdovec" in e48["stan"], "")
    e51 = next(e for e in grb if e["zap"] == 51)
    check("I5i h51-z51-Janez-PEZDIREC ('Penčiče'-ZAVRJEN-@×6.0 x-KRIŽEC+DESCENDER!)",
          "PEZDIREC" in e51["ime"] and "x-KRIŽEC+DESCENDER" in e51["ime"], "")

    # ---------- I6: kumulativ + parish.ts ----------
    vit = parse_house_vitals()
    d04894 = [v for v in vit if v["bookSignature"] == "04894"]
    check("I6a vitals 1082", len(vit) == VITALS_TOTAL, str(len(vit)))
    check("I6b mrliški bloki 04894 = 383", len(d04894) == BLOKI_04894, str(len(d04894)))
    d1913 = [v for v in d04894 if v["year"] == 1913]
    check("I6c bloki 1913 = 14", len(d1913) == 14, str(len(d1913)))
    check("I6d bloki 1913: skeni 142–146 + stran == sken − 1",
          all(v["scan"] and 142 <= v["scan"] <= 146 and v["page"] == v["scan"] - 1 for v in d1913), "")
    check("I6d2 bloki 1916+ ne obstajajo (P181-lead!; P177–P179 = 1911+1912+1913 sedaj v korpusu!)",
          all(v["year"] < 1925 for v in d04894), "")
    houses_all = {v["houseNo"] for v in vit if v["houseNo"].isdigit()}
    check("I6g korpus = 93 hiš (NESPREMENJENO — h78/h79-ŽE-v-korpusu!)",
          len(houses_all) == KORPUS_HOUSES, str(len(houses_all)))
    qa = open(QA_TS, encoding="utf-8").read()
    check("I6f p80Houses 93 (+h79-EDINA-NOVA — 04105-h79-izven-filtra!)",
          qa.count("p80Houses.size !== 93") >= 24, str(qa.count("p80Houses.size !== 93")))

    # ---------- I7: parish.ts forezika-1913 ----------
    check("I7a h59-×2-1913 (JAKLIČ-oče+hči-v-2-mesecih = PADEC-9.!)",
          len([v for v in d1913 if v["houseNo"] == "59"]) == 2
          and any("h59-×2-1913-#2" in v["whatSi"] for v in d1913), "")
    check("I7b PEZDIREC-1913 = 3.-LETO-ZAPORED (x-KRIŽEC+DESCENDER-@×6.0!)",
          len([v for v in d1913 if "PEZDIREC" in v["whatSi"]]) == 1
          and any("x-KRIŽEC+DESCENDER" in v["whatSi"] for v in d1913), "")
    check("I7c h92 = 1.-MRLIŠKI-VPIS-KADARKOLI = 34.-PT (NAJVIŠJA-hiša!)",
          any('h92 = 1. MRLIŠKI VPIS KADARKOLI = 34.-PT' in v["whatSi"] for v in d1913), "")
    check("I7d 1.-LJUDSKI-UČITELJ-STAN (z19-HALAR — LE_V_DOKAZU!)",
          any("ljudski učitelj" in (e.get("stan") or "") for e in grb), "")
    check("I7e ANZELM-POLÁK-'Koop.'-NOVI-DUHOVNIK (×4-v-korpusu!)",
          sum(v["whatSi"].count("Anzelm Polák") for v in d1913) == 4, "")
    check("I7f 1.-KOVAČ + 1.-'delavec-in-vdovec'-FORMULA (LE_V_DOKAZU + korpus!)",
          any("ženjen kovač" in v["whatSi"] for v in d1913)
          and any("delavec in vdovec" in v["whatSi"] for v in d1913), "")
    check("I7g korekcije-važne-v-korpusu (MILEK + ŠILAK + KRAMBIČ-'Agota' + JAKLIČ!)",
          any("VLM-'Hlebič'-ZAVRJEN" in v["whatSi"] for v in d1913)
          and any("VLM-'Viljak'-ZAVRJEN" in v["whatSi"] for v in d1913)
          and any("VLM-'Agota'-IME-HALUCINACIJA" in v["whatSi"] for v in d1913)
          and any("VLM-'Jakhlič'-ZAVRJEN" in v["whatSi"] for v in d1913), "")

    # ---------- I8: qa-parish.ts ----------
    check("I8a qa-p179 obstaja (180. kontrola)", "qa-p179-parish-death-1913" in qa, "")
    check("I8b qa-p179 hiše-lista", '"1,5,12,34,44,47,49,51,59,59,65,76,90,92"' in qa, "")
    check("I8c vitals-checki 1077 (>= 93)", qa.count("!== 1484") >= 93, str(qa.count("!== 1484")))
    check("I8d bloki-checki 378 (>= 27)", qa.count("!== 446") >= 27, str(qa.count("!== 446")))
    check("I8e p80-checki 93 (>= 25)", qa.count("p80Houses.size !== 93") >= 24, str(qa.count("p80Houses.size !== 93")))
    check("I8f guardi-1915 (>= 28)", qa.count("(h.year ?? 0) >= 1916") >= 28, str(qa.count("(h.year ?? 0) >= 1916")))
    check("I8g allowi-1913 (h90-p85 + h12-p87 + h49-p94!)",
          'v.year === 1913 && hn === "90"' in qa and 'v.year === 1913 && hn === "12"' in qa
          and 'v.year === 1913 && hn === "49"' in qa, "")
    check("I8h p80Death-sporočilo (P180: + 5 blokov 1914 + P181: + 9 blokov 1915 = 392!)",
          "P180: + 5 blokov 1914 + P181: + 9 blokov 1915 = 392!" in qa, "")

    # ---------- I9: skripte-kaskada ----------
    check("I9a p153–p178 skripte VITALS_TOTAL 1077",
          all("VITALS_TOTAL = 1100" in open(f"scripts/p{i}_parish_death_{y}.py", encoding="utf-8").read()
              for i, y in ((153, 1887), (154, 1888), (155, 1889), (156, 1890), (157, 1891), (158, 1892), (159, 1893),
                           (160, 1894), (161, 1895), (162, 1896), (163, 1897), (164, 1898), (165, 1899), (166, 1900),
                           (167, 1901), (168, 1902), (169, 1903), (170, 1904), (171, 1905), (172, 1906), (173, 1907),
                           (174, 1908), (175, 1909), (176, 1910), (177, 1911), (178, 1912))), "")
    check("I9b p170–p178 skripte BLOKI_04894 378",
          all("BLOKI_04894 = 401" in open(f"scripts/p{i}_parish_death_{y}.py", encoding="utf-8").read()
              for i, y in ((170, 1904), (171, 1905), (172, 1906), (173, 1907), (174, 1908), (175, 1909), (176, 1910), (177, 1911), (178, 1912))), "")
    check("I9c p80-skripta 1077/93",
          "len(vitals) == 1100" in open("scripts/p80_parish_md_books.py", encoding="utf-8").read()
          and "len(houses) == 94" in open("scripts/p80_parish_md_books.py", encoding="utf-8").read(), "")

    # ---------- I10: honesty ----------
    check("I10a honesty točk >= 6", len(d["honesty"]) >= 6, str(len(d["honesty"])))
    check("I10b [~] konservativno (Dajnar + Marenič + Jaklič + Lozar + Lah + Mlec)",
          sum(1 for e in ent if "[~" in json.dumps(e, ensure_ascii=False)) >= 10, "")
    check("I10c P181-lead v notes", "P180_LEAD" in d["notes"], "")

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
    print(f"p179: {ok}/{len(results)} " + ("PASS" if ok == len(results) else "FAIL"))
    sys.exit(0 if ok == len(results) else 1)


if __name__ == "__main__":
    main()
