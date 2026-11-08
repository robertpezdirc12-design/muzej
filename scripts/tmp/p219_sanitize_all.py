#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P219 — INSERT qa-p219 + sanitizacija (1632→1642, 413→423, yearset +1858) + verifier-patch + pt-luknja."""
from pathlib import Path
import glob, json, re

ROOT = Path("/home/z/my-project")
QA = ROOT / "src/lib/qa-parish.ts"
src = QA.read_text(encoding="utf-8")
ANCHOR = "  // ——— qa-p218: MRLIŠKA PREDZGODOVINA 04106 — leto 1859 = 27. leto PREDZGODOVINSKE"
assert src.count(ANCHOR) == 1 and "qa-p219-parish-death-1858-04106" not in src
BLOCK = '''
  // ——— qa-p219: MRLIŠKA PREDZGODOVINA 04106 — leto 1858 = 28. leto PREDZGODOVINSKE
  //      LINIJE (issue #18). 1858 = 58 vpisov-kronološko (ŠTEVJE-IZ-VRSTIC-21.× —
  //      WRITTEN-1–57-ČISTO-BREZ-luknij — ČISTA-ORDINALNA-LINIJA-2.-leto-zapored!
  //      + 1-NEŠTEVILČENA-s7-zadnja — 2.-instance-po-P218-s15-Jalkič!) / 10-GRIBLJE
  //      / 8 hiš (h19-×3-TRIPLE — edina-×3-v-predzgodovini!) + ★★★ MEJA-1857/58-s7
  //      (NASLOVNI-LIST-RAZPRTA + TAIL-1857-z73–z74 (GRIBLJE-h36!) + VSOTNA-'1 8
  //      [5 8]'-MARKER-P214-TIP-3.-INSTANCE + rokopisna-'Jänner-1858'-glava +
  //      restart-z1–z11!) = 57.-POTRDITEV! + ★★★ MEJA-1858/59-s11 re-križ = 58.! +
  //      ★★★ NASLOVNA-LISTA-s9+s10-SREDI-1858 (quiri-prelom! page-VLM-s10-LE-4/14-
  //      '30–33'-MISREAD → KROP-40–53-ČISTO!) + ★★★ DVOJČKI-SIMIC-h19 (ZWILLINGE!)
  //      + ★★★ GAUFIGALBRANN[?]-KLASTER-×4 + ★★★ PEZDIRC-MREŽA-'Padire'-h50-
  //      4-GENERACIJE! + ★★★ NOV-DUHOVNIK-DUEL-'Auber[?]' + KOREKCIJA-P218: Knavs-
  //      ŽE-Feb-1858! + otroška-umrljivost-50%-5/10. Dokaz:
  //      parish-death-1858-04106.json; skripte p219.
  {
  const p219Errors: string[] = [];
  const p219Death = HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && h.year === 1858);
  if (p219Death.length !== 10)
    p219Errors.push(`bloki 1858 (04106) ≠ 10 (${p219Death.length} — 10 Griblje-vpisov / 8 hiš / 58 kronoloških = 57-written + 1-NEŠTEVILČENA!)`);
  const p219Houses = p219Death.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
  if (p219Houses.join(",") !== "2,3,19,19,19,44,49,50,60,65")
    p219Errors.push(`hiše 1858 neujemane — najdeno: ${p219Houses.join(",")}`);
  if (HOUSE_VITALS.length !== 1642)
    p219Errors.push(`HOUSE_VITALS ≠ 1642 (${HOUSE_VITALS.length} — P218: 1632; P219: + 10 blokov 1858-04106 = 1642!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length !== 423)
    p219Errors.push(`bloki 04106 ≠ 423 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length} — P219: 10 × 1858 + P218: 23 × 1859 + P217: 9 × 1860 + P216: 10 × 1861 + P215: 9 × 1862 + P214: 7 × 1863 + P213: 17 × 1864 + P212: 13 × 1865 + P211: 13 × 1866 + P210: 20 × 1867 + P209: 13 × 1868 + P208: 14 × 1869 + P207: 12 × 1870 + P206: 11 × 1871 + P205: 17 × 1872 + P204: 38 × 1873 + P203: 21 × 1874 + P202: 10 × 1875 + P201: 20 × 1876 + P200: 8 × 1877 + P199: 23 × 1878 + P198: 9 × 1879 + P197: 13 × 1880 + P192: 16 × 1885 + P193: 21 × 1884 + P194: 11 × 1883 + P195: 16 × 1882 + P196: 19 × 1881 = 423!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && (h.year ?? 0) !== 1858 && (h.year ?? 0) !== 1859 && (h.year ?? 0) !== 1860 && (h.year ?? 0) !== 1861 && (h.year ?? 0) !== 1862 && (h.year ?? 0) !== 1863 && (h.year ?? 0) !== 1864 && (h.year ?? 0) !== 1865 && (h.year ?? 0) !== 1866 && (h.year ?? 0) !== 1867 && (h.year ?? 0) !== 1868 && (h.year ?? 0) !== 1869 && (h.year ?? 0) !== 1870 && (h.year ?? 0) !== 1871 && (h.year ?? 0) !== 1872 && (h.year ?? 0) !== 1873 && (h.year ?? 0) !== 1874 && (h.year ?? 0) !== 1875 && (h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)
    p219Errors.push("04106-bloki izven {1858, ..., 1885} (predzgodovina: 1857 še nebran — P220-LEAD!)");
  if (!p219Death.some((h) => h.houseNo === "19" && h.whatSi.includes("DVOJČEK-1/2") && h.whatSi.includes("ZWILLINGE")))
    p219Errors.push("★★★ DVOJČKI-SIMIC-h19 (z16+z17-ZWILLINGE!) ni označena");
  if (!p219Death.some((h) => h.houseNo === "50" && h.whatSi.includes("PEZDIRC-MREŽA-NAJGLABLJE") && h.whatSi.includes("4-GENERACIJSKA-GRAFIJA-LINIJA")))
    p219Errors.push("★★★ z52-'Padire'-h50-PEZDIRC-MREŽA-4-GENERACIJE ni označena");
  if (!p219Death.some((h) => h.houseNo === "65" && h.whatSi.includes("NOV-DUHOVNIK-DUEL") && h.whatSi.includes("Auber")))
    p219Errors.push("★★★ z39-NOV-DUHOVNIK-DUEL-'Auber[?]' ni označena");
  if (!p219Death.some((h) => h.houseNo === "19" && h.whatSi.includes("h19-DRAMA-3/3") && h.whatSi.includes("FRAISEN-nit")))
    p219Errors.push("★★★ z27-h19-DRAMA-3/3 + FRAISEN-nit ni označena");
  if (!p219Death.some((h) => h.houseNo === "49" && h.whatSi.includes("GAUFIGALBRANN") && h.whatSi.includes("hisna-DUEL-3×")))
    p219Errors.push("★★★ z15-h49-GAUFIGALBRANN-nit-1/4 + hisna-DUEL-3× ni označena");
  push(
    "qa-p219-parish-death-1858-04106",
    "P219: ŽUPNIJA PODZEMELJ — MRLIŠKA PREDZGODOVINA 04106, LETO 1858 = 28. LETO PREDZGODOVINSKE LINIJE (issue #18): okvir — s007–s011 (pag = sken−5-KORPUS-KONVENCIJA — svinčnik-foliacija-arhivarja = sken−1 (s7='6'...s11='10')-dokumentirana!; SANDBOX-RESET: 2×-neodvisna-prenosa-md5-8/8!) + **★★★ 58-VPIISOV-KRONOLOŠKO-ŠTEVJE-IZ-VRSTIC-21.×** (WRITTEN-1–57-ČISTO-BREZ-luknij — ČISTA-ORDINALNA-LINIJA-2.-leto-zapored (nasprotje-1859-LUKNJA-92!) + 1-NEŠTEVILČENA-s7-zadnja (Jan-29/31 — levi-stolpec-PRAZEN-KROP-2.×-POTRJENO — 2.-instance-po-P218-s15-Jalkič!); vrstna-aritmetika 11+1(NEŠTEVILČENA!)+14+14+14+4!) + **★★★ MEJA-1857/58 = s7 (NASLOVNI-LIST-'Sterb-Buch.'-RAZPRTA + TAIL-1857-z73–z74 (2-vrstici: Gradac-'Amalia-Rundel[?]'-86J[duel!] + ★ GRIBLJE-h36-'Križan/Krisan/Kristjan[?]-TRI'-73J — 1857-zadnji-Griblje!) + DVOJNA-ČRTA + VSOTNA-'1 8 [5 8]'-RAZPETE-MARKER (P214-TIP-3.-INSTANCE — '1-8'-KROP-JASNO + '5'-v-Alter-stolpcu!) + rokopisna-'Jänner-1858'-glava-KROP + restart-z1–z11 (11!) + ★★★ NEŠTEVILČENA-ZADNJA!) = 57.-POTRDITEV-invariante!** + **★★★ MEJA-1858/59 = s11 (P218-potrjeno + re-križ-P219-arb_s11_meja-1:1 — Zemelj + Krasinec-×2 + Gradac, 0-GRIBLJE!) = 58.-POTRDITEV!** + **★★★ NASLOVNA-LISTA-'Sterb-Buch.'-s9+s10-SREDI-1858 (quiri-prelom-mid-year — paralela-1859-s19!; page-VLM-na-s10-ujel-LE-4/14-vrstic ('30–33'-MISREAD-3/4-ZMEDA!) → KROP-zap-stolpec-glif-viz-1:1-POTRDIL-40–53-ČISTO! + arb_s9_glava-glyph-8-BREZ-repa-NE-9!)** + **★★★ DVOJČKI-SIMIC-h19 (z16-Ana-2-dni + z17-Mannier[?]-'zwilling-Genickfand-kind'-½-dni[?] — ZWILLINGE-dokumentirana-2-vrstica!) — PRE-EHO-1859-GENICKSTARRE-EPIDEMIJE-×4!** + **★★★ GAUFIGALBRANN[?]-KLASTER-×4 (z15-Anna-Radine-h49-19J + z16 + z17 + z27-Kurič-7-mj-Fraisin — Feb-20→Apr-9 — Gichterbrand?-hipoteza-X-open! — ČEZ-MEJO-'FRAISEN'-nit → 1859-Jän-PARIČ-klaster-×2!)** + **★★★ PEZDIRC-MREŽA-NAJGLABLJE-'Padire'-h50 (z52-Maria[?]/Martin[?]-68-J[?]-1858 → 1868-Johann-Perdirc → 1872-Barbara-Kerdise-PEZDIR → 1924-Matija-PERDIRC-POSESTNIK — 4-GENERACIJSKA-GRAFIJA-LINIJA-×4-V-ISTI-HIŠI!)** + **★★★ NOV-DUHOVNIK-DUEL-'J.-Auber[?]/Huber[?]-P.' (z39-h65-Jun-21 — 4×-zoom!; vs-Joh.-Knavs-DOMINANTA-jasni-×6-1:1 (z15/z16/z17/z27/z37/z42) + grafija-variacije-'Khubiz/Knavo/Knaff/Kribiz[?]' + page-VLM-'Šinkovec[?]'-garble!) — ★★★ KOREKCIJA-P218: Knavs-AKTIVEN-ŽE-OD-FEB-1858 (ne-samo-1859!)** + hišne-niti: h19-×3-TRIPLE (dvojčka + Kurič — 3-otroške-smrti-v-1-hiši-1858! → 1859-×2!) + h2-KLEPEC/HLEBEC (z47-otrok → 1864/67/71!) + h3-KRIŽAN (z42-Kind → 1865 → 1882 + 04894-×4!) + h44-ŠTRUCELJ (z51 → 1867 → 1873 + mreža!) + h49-BRODARIČ (z15-'Radine[?]' → 1859-z94-Padierž!) + h60-TOMINC (z37-Jakob-60J → 1881-Katharina!) + h65-MILEK (z39-'Keržan[?]' → 1859-×2 → MILEK-mreža!); **★★★ 10-GRIBLJE / 8 hiš (h19-×3-TRIPLE — edina-×3-v-predzgodovini!)** + starost-'0'-dueli-×2 (z39 + z42!) + meseci-GRIBLJE-luknje-×5 (Jan/Mär/Mai/Nov/Dez-×0!) + otroška-umrljivost-50%-5/10 (NAJVIŠJA-skoraj — cf-1866-77%!) + ekstremi-0[?]-→-68-J[?]-dueli; **10 NOVIH BLOKOV parish.ts: vitals 1632 → 1642 · 04106 = 413 → 423 · 04894 = 520-NESPREMENJENO**; skripte p219 (fetch-2×-md5-8/8 + read-×8-s10-manual + krop-33 (stolpci-×5 + arb-×5 + vrste-×14 + pas-×5 + duh-×3 + foliacija-×5!) + build-entries + build-proof) + qa-p219 (219. kontrola!) + dokaz parish-death-1858-04106.json (58 entries: 10-Griblje + 48-druge!) + pt-luknja-423/1642; **★★★ PREDZGODOVINA-LINIJA-28/29-LET!** (P220-LEAD: 1857 — ZADNJE-leto-04106: s004–s006-ŽE-prenesni+VLM (z33–z72!) + tail-ŽE-KROP'd (s7-z73–z74-GRIBLJE-h36!) → s003-nazaj-proba — knjiga-se-začne-1857!)",
    "P219: THE PARISH OF PODZEMELJ — THE DEATH-REGISTER-PREHISTORY 04106, THE YEAR 1858 = THE 28th YEAR (issue #18): the-frame + **★★★ 58-ENTRIES-CHRONOLOGICAL-ROW-COUNTING-21st-×** (WRITTEN-1–57-CLEAN-NO-GAPS — the-CLEAN-ORDINAL-LINE-2nd-year-in-a-row (vs-1859-GAP-92!) + 1-UNNUMBERED-s7-last-row (Jan-29/31 — the-left-column-EMPTY-KROP-2×-CONFIRMED — the-2nd-instance-after-P218-s15-Jalkič!)) + **★★★ THE-1857/58-BOUNDARY = s7 (the-SPREAD-TITLE-PAGE + the-1857-TAIL-z73–z74 (Gradac + ★ GRIBLJE-h36-'Križan/Krisan[?]'-73J!) + the-SUM-ROW-'1 8 [5 8]'-SPREAD-DIGITS (P214-TYPE-3rd-INSTANCE!) + the-handwritten-'Jänner-1858'-header + the-restart-z1–z11!) = the-57th-CONFIRMATION!** + **★★★ THE-1858/59-BOUNDARY = s11 re-cross = the-58th!** + **★★★ THE-TITLE-PAGES-s9+s10-MID-1858 (the-quire-break!; the-page-VLM-caught-ONLY-4/14-rows ('30–33'-MISREAD!) → the-KROP-zap-column-glif-viz-1:1-CONFIRMED-40–53-CLEAN!)** + **★★★ THE-SIMIC-TWINS-h19 (z16-Ana-2-days + z17-'zwilling-Genickfand-child'-½-day[?] — the-ZWILLINGE-note!) — the-PRE-ECHO-of-the-1859-GENICKSTARRE-EPIDEMIC!** + **★★★ THE-GAUFIGALBRANN[?]-CLUSTER-×4 (Feb-20→Apr-9 — Gichterbrand?-hypothesis — CROSSING-INTO-the-'FRAISEN'-thread → 1859-PARIČ-cluster!)** + **★★★ THE-PEZDIRC-NETWORK-DEEPEST-'Padire'-h50 (1858 → 1868 → 1872 → 1924 — 4-GENERATIONAL-GRAPHIA-LINE-IN-THE-SAME-HOUSE!)** + **★★★ THE-NEW-PRIEST-DUEL-'J.-Auber[?]/Huber[?]-P.' (z39! vs-the-Knavs-DOMINANCE — ★★★ THE-P218-CORRECTION: Knavs-ACTIVE-ALREADY-FROM-FEB-1858!)** + house-threads (h19-×3-TRIPLE! + h2/h3/h44/h49/h50/h60/h65) + the-'0'-age-duels-×2 + the-Griblje-month-gaps-×5 + child-mortality-50%-5/10 + extremes-0[?]-→-68-J[?]; **10 NEW BLOCKS: the vitals 1632 → 1642 · the 04106 = 413 → 423**; the scripts p219 + the qa-p219 (the 219th check!) + the evidence parish-death-1858-04106.json (58 entries!) + the pt-gap-423/1642; **★★★ THE-PREHISTORY-LINE-28/29-YEARS!** (the P220-LEAD: 1857 — the-LAST-year-of-04106: s004–s006-already-downloaded+VLM-read + the-tail-already-KROP'd → the-s003-backward-probe — the-book-BEGINS-1857!)",
    p219Errors.length === 0,
    p219Errors.length === 0
      ? `10 vpisov / 58 kronoloških (57-written-ČISTO + 1-NEŠTEVILČENA-s7!) / 8 hiš (h19-×3-TRIPLE!) · MEJA-s7-VSOTNA-'1 8 [5 8]'-P214-TIP-3.-INSTANCE-57.-POTRDITEV + s11-re-križ-58. · NASLOVNA-LISTA-s9+s10-sredi-1858 (page-VLM-s10-4/14-MISREAD-KOREKCIJA!) · DVOJČKI-SIMIC-h19-ZWILLINGE · GAUFIGALBRANN-×4 · PEZDIRC-'Padire'-h50-4-GENERACIJE · NOV-DUHOVNIK-'Auber[?]'-DUEL + Knavs-ŽE-Feb-1858-KOREKCIJA-P218 · otroška-50%-5/10 · **PREDZGODOVINA-28/29!** · vitals 1642 · 04106 423 · 04894 520`
      : p219Errors.join("; "),
  );
  }

'''
src = src.replace(ANCHOR, BLOCK + ANCHOR, 1)
src = src.replace("HOUSE_VITALS.length !== 1632", "HOUSE_VITALS.length !== 1642")
src = src.replace('04106").length !== 413', '04106").length !== 423')
src = src.replace("(h.year ?? 0) !== 1859 &&", "(h.year ?? 0) !== 1858 && (h.year ?? 0) !== 1859 &&")
src = src.replace("1857–1859 še nebrani!", "1857 še nebran!")
src = src.replace("1857–1860 še nebrani!", "1857 še nebran!")
src = src.replace("1857–1862 še nebrani!", "1857 še nebran!")
src = src.replace("1857–1867 še nebrani!", "1857 še nebran!")
src = src.replace("izven {1859, 1860,", "izven {1858, 1859, 1860,")
src = src.replace("izven {1859, 1861, ..., 1885}", "izven {1858, 1859, 1861, ..., 1885}")
src = src.replace("vitals 1632 · 04106 413 · 04894 520", "vitals 1642 · 04106 423 · 04894 520")
src = src.replace("pt-luknja-413/1632", "pt-luknja-423/1642")
QA.write_text(src, encoding="utf-8")
print(f"qa-parish: 1642×{src.count('HOUSE_VITALS.length !== 1642')} · 423×{src.count('04106\").length !== 423')} · 1858-guard×{src.count('(h.year ?? 0) !== 1858')}")

files = sorted(set(glob.glob(str(ROOT / "scripts/**/*.py"), recursive=True) + glob.glob(str(ROOT / "scripts/**/*.mjs"), recursive=True)))
skip = ("p59_ps_blatt_headers", "p199_", "p200_", "p201_", "p202_", "p203_", "p204_", "p205_", "p206_", "p207_", "p208_", "p210_", "p211_", "p212_", "p213_", "p214_", "p215_", "p216_", "p217_", "p218_", "p219_")
patched = 0
for f in files:
    if any(s2 in f for s2 in skip): continue
    t = Path(f).read_text(encoding="utf-8")
    if "1632" not in t and "== 413" not in t: continue
    o = t
    t = t.replace("1632", "1642").replace('.get("04106") == 413', '.get("04106") == 423').replace("04106 == 413", "04106 == 423").replace("04106==413", "04106==423").replace("skupaj == 413", "skupaj == 423").replace('"04106") == 413', '"04106") == 423').replace("(04106, 413)", "(04106, 423)").replace("== 413,", "== 423,")
    if t != o:
        Path(f).write_text(t, encoding="utf-8"); patched += 1
print(f"skripte-patched: {patched}")

vpatched = 0
for f in sorted(ROOT.glob("scripts/p19*.py")) + sorted(ROOT.glob("scripts/p2[0-9][0-9]_parish*.py")):
    if "p219" in f.name: continue
    t = f.read_text(encoding="utf-8"); o = t
    for a, b in [("04106 == 413", "04106 == 423"), ("04106==413", "04106==423"),
                 ('04106": 413', '04106": 423'), ("skupaj == 413", "skupaj == 423"),
                 ('"04106") == 413', '"04106") == 423'), ("(04106, 413)", "(04106, 423)"),
                 ('byBook"]["04106"] == 413', 'byBook"]["04106"] == 423'),
                 ('["04106"] == 413', '["04106"] == 423'),
                 ("vitals == 1632", "vitals == 1642"), ("vitalsTotal == 1632", "vitalsTotal == 1642"),
                 ('vitalsTotal"] == 1632', 'vitalsTotal"] == 1642'),
                 ('"vitalsTotal": 1632', '"vitalsTotal": 1642'),
                 ('\\"vitalsTotal\\": 1632', '\\"vitalsTotal\\": 1642'),
                 ('!== 1632"', '!== 1642"'),
                 ("1632-številcev", "1642-številcev"),
                 ("vitals-števec-1632", "vitals-števec-1642"), ("vitals-1632", "vitals-1642")]:
        t = t.replace(a, b)
    t = re.sub(r'set\(izven\) == \{"1859"', 'set(izven) == {"1858", "1859"', t)
    t = t.replace('",".join(leta) == "1859,1860', '",".join(leta) == "1858,1859,1860')
    t = t.replace('join(leta) == "1859,1860,1861,1862,1863,1864,1865,1866,1867,1868,1869,1870,1871,1872,1873,1874,1875,1876,1877,1878,1879,1880,1881,1882,1883,1884,1885"',
                  'join(leta) == "1858,1859,1860,1861,1862,1863,1864,1865,1866,1867,1868,1869,1870,1871,1872,1873,1874,1875,1876,1877,1878,1879,1880,1881,1882,1883,1884,1885"')
    if t != o:
        f.write_text(t, encoding="utf-8"); vpatched += 1
print(f"verifierji-patched: {vpatched}")

ptp = ROOT / "research/issue17/pt-luknja-18-final.json"
pt = json.loads(ptp.read_text(encoding="utf-8"))
pt["corpus"]["vitalsTotal"] = 1642
pt["corpus"]["byBook"]["04106"] = 423
pt["corpus"]["housesNote"] = (pt["corpus"].get("housesNote") or "") + " | P219: +10-blokov-1858 (04106 413→423, vitals 1632→1642, ŠTEVJE-IZ-VRSTIC-21.×-58-kronološko (57-written-ČISTO + 1-NEŠTEVILČENA-s7) + 10-GRIBLJE/8-hiš (h19-×3-TRIPLE!) + MEJA-1857/58-s7-VSOTNA-'1 8 [5 8]'-P214-TIP-3.-INSTANCE-57.-POTRDITEV + NEŠTEVILČENA-s7-2.-instance + NASLOVNA-LISTA-s9+s10-sredi-1858 (page-VLM-s10-4/14-MISREAD-KOREKCIJA!) + DVOJČKI-SIMIC-h19 + GAUFIGALBRANN-×4 + PEZDIRC-'Padire'-h50-4-GENERACIJE + NOV-DUHOVNIK-'Auber[?]'-DUEL + Knavs-ŽE-Feb-1858-KOREKCIJA-P218!)"
ptp.write_text(json.dumps(pt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"pt-luknja: {pt['corpus']['vitalsTotal']}/{pt['corpus']['byBook']['04106']}")
