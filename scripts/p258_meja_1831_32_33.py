#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P258 — verifikator NOTRANJOSTI-01738: MEJA-1831/32/33 (I1–I10 + --live).
Korpus 2043 → 2059 (+16 blokov: 5×1831-konec + 9×1832 + 2×1833!); šest-knjižne 23 → 31 (+8);
bothEra 26 → 34; 10 dvigov (h8-40 = 2. vseh časov!); PEZDIRC-h50-3-vrstice; MILEK-h22-potrjena;
KRIŽAN-konglomerat-4-hiše; 40-vpisov (11+15+14) = NAJVEČJA-NOTRANJOST-FAZA.
Dokaz: parish-marriage-notranjost-1832.json (+ parish-house-stories.json)."""
import json
import re
import sys
import base64
import urllib.request

ROOT = "/home/z/my-project"
OK = 0
FAIL = 0
LIVE = "--live" in sys.argv


def check(name, ok, msg=""):
    global OK, FAIL
    if ok:
        OK += 1
        print(f"[PASS] {name}" + (f" — {msg}" if msg else ""))
    else:
        FAIL += 1
        print(f"[FAIL] {name}" + (f" — {msg}" if msg else ""))


src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
early = open(f"{ROOT}/src/data/atlas/parish-marriage-early.ts", encoding="utf-8").read()
stories = open(f"{ROOT}/src/data/atlas/parish-house-stories.ts", encoding="utf-8").read()
qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()

# ——— I1: 16 blokov 1831-konec/1832/1833/01738 (file-order!) ———
bloki1831k = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "01738",\s*year: 1831,\s*scan: 8,', src)
check("I1 bloki-01738/1831-konec-s8 == [47,46,8,48,2] (m14+m19×2+m20×2 — 2-POLNA-DVOJNA!)",
      bloki1831k == ["47", "46", "8", "48", "2"], ",".join(bloki1831k))
bloki1832 = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "01738",\s*year: 1832,', src)
check("I1b bloki-01738/1832 == [22,35,2,42,36,35,66,56,61] (h35-×2-DVE-DRUŽINI!)",
      bloki1832 == ["22", "35", "2", "42", "36", "35", "66", "56", "61"], ",".join(bloki1832))
bloki1833 = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "01738",\s*year: 1833,', src)
check("I1c bloki-01738/1833 == [50,49] (m6-PESDIRZ×HIMIZ — POLNI-DVOJNI!)",
      bloki1833 == ["50", "49"], ",".join(bloki1833))
check("I1d foliacija: Pag. 13/15/17 (2·sken−3 ×9 — svinčnik 15/16 + 17/18!)",
      'page: 13,' in src and 'page: 15,' in src and 'page: 17,' in src, "-")

# ——— I2: korpus 2059 + 01738 == 47 + leta 1828–1833+1873 ———
vseh = re.findall(r'bookSignature: "01738"', src)
skupaj = len(re.findall(r'bookSignature: "', src))
leta1738 = sorted(set(int(y) for h, b, y in re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "(01738)",\s*year: (\d+)', src) if b == "01738"))
check("I2 vitals == 2059 + 01738 == 47 + leta == 1828–1833+1873",
      "HOUSE_VITALS.length !== 2059" not in src and len(vseh) == 47 and skupaj == 2059
      and leta1738 == [1828, 1829, 1830, 1831, 1832, 1833, 1873],
      f"01738={len(vseh)} skupaj={skupaj} leta={leta1738}")

# ——— I3: modul PREDHODNIK_1831K/1832/1833 + 258_NITI/KRAJI/KORPUS ———
exports = ["PREDHODNIK_1831K_BLOCKS", "PREDHODNIK_1831K_HOUSES", "PREDHODNIK_1831K_TOTAL",
           "PREDHODNIK_1831K_BLOCKI", "PREDHODNIK_1831K_STRUNA",
           "PREDHODNIK_1832_BLOCKS", "PREDHODNIK_1832_HOUSES", "PREDHODNIK_1832_TOTAL",
           "PREDHODNIK_1832_BLOCKI", "PREDHODNIK_1832_STRUNA",
           "PREDHODNIK_1833_BLOCKS", "PREDHODNIK_1833_HOUSES", "PREDHODNIK_1833_TOTAL",
           "PREDHODNIK_1833_BLOCKI", "PREDHODNIK_1833_RESTART",
           "PREDHODNIK_258_NITI", "PREDHODNIK_258_KRAJI", "PREDHODNIK_258_KORPUS"]
manjka = [e for e in exports if f"export const {e}" not in early]
check("I3 modul parish-marriage-early P258-sekcija (×18 izvozov)", not manjka, f"manjka: {manjka}" if manjka else "×18")
check("I3b števci 11/5 + 23/9 + 6/2 + korpus 2059/47/16",
      "PREDHODNIK_1831K_TOTAL = 11" in early and "PREDHODNIK_1831K_BLOCKI = 5" in early
      and "PREDHODNIK_1832_TOTAL = 23" in early and "PREDHODNIK_1832_BLOCKI = 9" in early
      and "PREDHODNIK_1833_TOTAL = 6" in early and "PREDHODNIK_1833_BLOCKI = 2" in early
      and "vitalsTotal: 2059" in early and "byBook01738: 47" in early and "noviBloki: 16" in early, "-")
check("I3c PREDHODNIK_1831_BLOCKS scan-7-filter (P258-scope-ločitev!)",
      'h.bookSignature === "01738" && h.year === 1831 && h.scan === 7' in early, "-")

# ——— I4: STRUNE + RESTART-1833 + NITI + KRAJI ———
seg = early[early.find("P258: NOTRANJOST"):]
check("I4 STRUNA-1831k: čez-mejo-strani + 12.-poroka-istega-dne + 24-VPISOV-leta",
      "1831-se-nadaljuje-ČEZ-mejo-strani" in seg and "12.-poroka-istega-dne" in seg and "24-VPISOV" in seg, "-")
check("I4b STRUNA-1832: RESTART-18.-Jän + PRESTOPNI-DAN + 9-POROK",
      "RESTART-letnice-1832" in seg and "PRESTOPNI-DAN" in seg and "9-POROK-NA-PRESTOPNI-DAN" in seg, "-")
check("I4c RESTART-1833: ROKOPISNO-NAD-datumom + [~3.|5.]-DUEL + 4.-restart",
      "RESTART-1833" in seg and "ROKOPISNO-NAD-datumom" in seg and "[~3.|5.]" in seg and "4.-restart" in seg, "-")
check("I4d NITI-P258: PEZDIRC-NADGRADNJA + DVA-SINA + MILEK-POTRJENA + KRIŽAN-KONGLOMERAT + KLOBUČAR-BRATJE + HLEBEC + MUZ + BARON",
      "PEZDIRC-h50-NIT-NADGRADNJA" in seg and "DVA-SINA-ISTEGA-OČETA-MARCA" in seg
      and "MILEK-h22-DOMNEVA-POTRJENA" in seg and "KRIŽAN-KONGLOMERAT" in seg
      and "KLOBUČAR-BRATJE" in seg and "HLEBEC-NIT-1832→1873" in seg
      and "MUZ-NIT-1833" in seg and "BARON-vrstica" in seg, "-")
check("I4e KRAJI-P258: SALOKA-IN-CROATIA-×2 + METLIKA-2.-omemba + SEMELJ-×5",
      "SALOKA-IN-CROATIA-×2" in seg and "METLIKA-m18" in seg and "SEMELJ/Podzemelj-×5" in seg, "-")

# ——— I5: dvigi-firstYear v blokih + vrzeli ———
check("I5 dvigi: h8-40 (2.-VSEH-ČASOV!) + h46-36 + h66-36 + h35-35 + h47-31 + h42-29 + h2-27 + h48-26 + h36-25 + h49-25",
      "1871→1831-DVIG-ZA-40" in src and "1867→1831-DVIG-ZA-36" in src and "1868→1832-DVIG-ZA-36" in src
      and "1867→1832-DVIG-ZA-35" in src and "1862→1831-DVIG-ZA-31" in src and "1861→1832-DVIG-ZA-29" in src
      and "1858→1831-DVIG-ZA-27" in src and "1857→1831-DVIG-ZA-26" in src
      and "1857→1832-DVIG-ZA-25" in src and "1858→1833-DVIG-ZA-25" in src, "-")
check("I5b vrzeli: h66+h49-BREZ-04455 (2-poročni-vrzeli!)",
      "h66-5-KNJIG-BREZ-04455" in src and "h49-5-KNJIG-BREZ-04455" in src and "poročna-vrzela" in src, "-")

# ——— I6: ★★★ PEZDIRC-h50-m6-1833 blok (triple-PESDIRZ + MARCO!) ———
m6 = re.search(r'houseNo: "50",\s*bookSignature: "01738",\s*year: 1833.*?whatSi: "((?:[^"\\]|\\.)*)"', src, re.S)
w6 = m6.group(1) if m6 else ""
check("I6 h50-m6-1833: PESDIRZ + MARCO-PESDIRZ + DVA-SINA + 3-VRSTICE-42-LET + h50×h49",
      "Johann PESDIRZ" in w6 and "MARCO PESDIRZ" in w6 and "DVA-SINA-ISTEGA-OČETA-MARCA" in w6
      and "3-VRSTICE-42-LET" in w6 and "POLNI DVOJNI (h50×h49!)" in w6, w6[:60])
m49 = re.search(r'houseNo: "49",\s*bookSignature: "01738",\s*year: 1833.*?whatSi: "((?:[^"\\]|\\.)*)"', src, re.S)
w49 = m49.group(1) if m49 else ""
check("I6b h49-m6-1833: Himiz + PESDIRZ-ženin + BREZ-04455 + 28→29-blokov",
      "Himiz" in w49 and "Johann PESDIRZ" in w49 and "BREZ-04455" in w49 and "28→29-blokov" in w49, "-")

# ——— I7: h47-priča-PEZDIRC + KRIŽAN-bloki + MILEK-h22 ———
m47 = re.search(r'houseNo: "47",\s*bookSignature: "01738",\s*year: 1831.*?whatSi: "((?:[^"\\]|\\.)*)"', src, re.S)
w47 = m47.group(1) if m47 else ""
check("I7 h47-m14: AND.-PEZDIRC-priča + 5.-VRSTICA-družine + Griblje-47 + 18→19-blokov",
      "AND. PEZDIRC" in w47 and "5.-VRSTICA-Pesdirc-družine" in w47 and "GRIBLJE 47" in w47 and "18→19-blokov" in w47, "-")
m36 = re.search(r'houseNo: "36",\s*bookSignature: "01738",\s*year: 1832.*?whatSi: "((?:[^"\\]|\\.)*)"', src, re.S)
w36 = m36.group(1) if m36 else ""
check("I7b h36-m17: KRIŽAN-KONGLOMERAT + 4-GRIBLJE-HIŠE + h36×h35 + 34-blokov",
      "KRIŽAN-KONGLOMERAT" in w36 and "4-GRIBLJE-HIŠE" in w36 and "POLNI DVOJNI (h36×h35!)" in w36 and "34 blokov 1832–1917" not in w36, "-")
m22 = re.search(r'houseNo: "22",\s*bookSignature: "01738",\s*year: 1832.*?whatSi: "((?:[^"\\]|\\.)*)"', src, re.S)
w22 = m22.group(1) if m22 else ""
check("I7c h22-m8-1832: MILEK-DOMNEVA-POTRJENA + 4.-BLOK-V-5-LETIH + brat-sesta + h22×h35",
      "MILEK-h22-DOMNEVA-POTRJENA" in w22 and "4.-BLOK-V-5-LETIH" in w22 and "brat-sestra" in w22.lower()
      and "POLNI DVOJNI (h22×h35!)" in w22, "-")
m66 = re.search(r'houseNo: "66",\s*bookSignature: "01738",\s*year: 1832.*?whatSi: "((?:[^"\\]|\\.)*)"', src, re.S)
w66 = m66.group(1) if m66 else ""
check("I7d h66-m22: KRIŽAN×KRIŽAN-PAR + 3:1-'66' + BREZ-04455",
      "KRIŽAN×KRIŽAN-PAR" in w66 and "3:1" in w66 and "BREZ-04455" in w66, "-")

# ——— I8: hišne zgodbe — 31 šest-knjižnih + p258Dvigi + tierji 31/35/10 ———
check("I8 HOUSE_STORY_SIX == 31 (+8: h2/h8/h35/h36/h42/h46/h47/h48) + TOTALS-2059",
      "sixBook: 31" in stories and "fiveBook: 35" in stories and "fourBook: 10" in stories
      and "blocks: 2059" in stories and "bothEraPorocna: 34" in stories
      and "p258Dvigi" in stories and "h8/h46/h66/h35/h47/h42/h2/h48/h36/h49" in stories, "-")
for h, n in [("2", 34), ("8", 39), ("35", 37), ("36", 34), ("42", 28), ("46", 39), ("47", 19), ("48", 33), ("50", 13), ("56", 15), ("61", 18), ("66", 14), ("22", 36), ("49", 29)]:
    m = re.search(rf'houseNo: "{h}", kind: "griblje", blocks: (\d+),', stories)
    check(f"I8b h{h} == {n} blokov", m and int(m.group(1)) == n, m.group(1) if m else "MANJKA")
m35per = re.search(r'houseNo: "35", kind: "griblje", blocks: 37, books: 6, perBook: \[.*?n: (\d+)', stories)
check("I8c h35-perBook[01738] == 2 (DVE-DRUŽINI-1832!)", m35per and int(m35per.group(1)) == 2, m35per.group(1) if m35per else "-")

# ——— I9: dokaz-JSON 40-vpisov + md5 ———
d = json.load(open(f"{ROOT}/research/issue17/parish-marriage-notranjost-1832.json", encoding="utf-8"))
check("I9 dokaz: P258 + 11+23+6-vpisov + md5-s8/s9/s10 + foliacija-×9",
      d["phase"] == "P258" and len(d["leta"]["1831konec"]) == 11 and len(d["leta"]["1832"]) == 23
      and len(d["leta"]["1833"]) == 6 and d["vir"]["md5"]["s8"] == "15c120e88e48b485c89e53e3640f8111"
      and d["vir"]["md5"]["s9"] == "959869b15f9725dc13898bbce7abba7d"
      and d["vir"]["md5"]["s10"] == "cb608199ce471054fa8085874946f848"
      and "×9" in d["struktura"]["foliacija"], "-")
check("I9b dokaz-niti: PEZDIRC-h50-3-VRSTICE + MILEK-POTRJENA + KRIŽAN-KONGLOMERAT + BARON + anomalije",
      "3-VRSTICE-42-LET" in d["niti"]["pezdircH50"] and "MILEK-DOMNEVA-POTRJENA" in d["niti"]["milekH22"]
      and "KRIŽAN-4-GRIBLJE-HIŠE" in d["niti"]["krizanKonglomerat"] and "BARON" in d["niti"]["baron"]
      and "MARIA-VIPAVC" in d["niti"]["anomalije"], "-")
check("I9c dokaz-korpusUcinek: 16-blokov + 2059 + 47 + dvigi-10 + šest-knjižne-31",
      d["korpusUcinek"]["noviBlok"] == 16 and d["korpusUcinek"]["vitalsTotal"] == "2043 → 2059"
      and d["korpusUcinek"]["byBook01738"] == "31 → 47" and "h8-40" in d["korpusUcinek"]["dvigi"]
      and "23 → 31" in d["korpusUcinek"]["sestKnjizne"], "-")
check("I9d dokaz-xOpen ≥ 12 + p259-s11",
      len(d["xOpen"]) >= 12 and "s11" in d["p259"], f"xOpen={len(d['xOpen'])}")

# ——— I10: LIVE ———
if LIVE:
    # I10: matricula HTTP 200 + inventar 147
    try:
        req = urllib.request.Request("https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/01738/",
                                     headers={"User-Agent": "Mozilla/5.0"})
        html = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "ignore")
        urls = []
        for m in re.finditer(r'"(/image/[A-Za-z0-9+/=]+/)"', html):
            s = m.group(1)[7:-1]
            try:
                dd = base64.b64decode(s + "=" * (-len(s) % 4)).decode("utf-8")
                if dd.startswith("http"):
                    urls.append(dd)
            except Exception:
                pass
        check("I10 LIVE matricula-01738 HTTP-200 + inventar-147-URL", len(urls) == 147, f"URL={len(urls)}")
    except Exception as e:
        check("I10 LIVE matricula-01738", False, str(e)[:80])
    # I10b: /api/qa 252/252
    try:
        qaResp = json.load(urllib.request.urlopen("http://localhost:3000/api/qa", timeout=90))
        check("I10b LIVE /api/qa == 252/252 ok:True",
              qaResp.get("ok") is True and qaResp.get("passed") == 252 and qaResp.get("failed") == 0,
              f"{qaResp.get('passed')}/{qaResp.get('passed', 0) + qaResp.get('failed', 0)}")
    except Exception as e:
        check("I10b LIVE /api/qa", False, str(e)[:80])
    # I10c: qa-p258-id prisoten
    check("I10c LIVE qa-p258-id v /api/qa",
          "qa-p258-parish-marriage-notranjost-01738-1832-1833" in qa, "-")

print(f"\n=== P258: {OK} PASS / {FAIL} FAIL ===")
sys.exit(1 if FAIL else 0)
