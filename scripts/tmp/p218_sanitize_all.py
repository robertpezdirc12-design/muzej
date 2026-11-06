#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P218 — INSERT qa-p218 + sanitizacija (1609→1632, 390→413, yearset +1859) + verifier-patch + pt-luknja."""
from pathlib import Path
import glob, json, re

ROOT = Path("/home/z/my-project")
QA = ROOT / "src/lib/qa-parish.ts"
src = QA.read_text(encoding="utf-8")
ANCHOR = "  // ——— qa-p215: MRLIŠKA PREDZGODOVINA 04106 — leto 1862 = 24. leto PREDZGODOVINSKE"
assert src.count(ANCHOR) == 1 and "qa-p218-parish-death-1859-04106" not in src
BLOCK = '''
  // ——— qa-p218: MRLIŠKA PREDZGODOVINA 04106 — leto 1859 = 27. leto PREDZGODOVINSKE
  //      LINIJE (issue #18). 1859 = 103 vpisov (ŠTEVJE-IZ-VRSTIC-20.× — written-
  //      1–91-ČISTO + 93–103 = 102 + 1-NEŠTEVILČENA-Jalkič!) / ★★★ 23-GRIBLJE =
  //      NOV-REKORD-PREDZGODOVINE (prej-20-1867!) / 16 hiš (6-×2!) + ★★★ MEJA-
  //      1858/59-s11 (NASLOVNI-LIST-'Sterb-Buch.'-DEEL-2-NOVI-TISKANI-STOLPCI +
  //      '1858'-tail-glava-KROP + VSOTNA-'1 8 [5 9]'-RAZPETE-MARKER-P214-TIP-
  //      2.-INSTANCE + restart-z1–z7!) = 56.-POTRDITEV! + ★★★ LUKNJA-92 (s18-91
  //      →s19-93!) + s19-NASLOVNI-LIST-PONOVLJEN + Dec-nadaljevanje! + ★★★
  //      GENICKSTARRE-EPIDEMIJA-×4 (z24+z25+z31+z32!) + ★★★ NOV-DUHOVNIK-'Joh.
  //      Knavs' (podpisi-×7+!) + P217-TAIL-KOREKCIJE (z94/z97-MARGINALI + ime +
  //      starost + vzrok!) + z5+z6-PARIČ-FRAISEN-klaster + z81-99J[~83!]-DUEL.
  //      Dokaz: parish-death-1859-04106.json; skripte p218.
  {
  const p218Errors: string[] = [];
  const p218Death = HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && h.year === 1859);
  if (p218Death.length !== 23)
    p218Errors.push(`bloki 1859 (04106) ≠ 23 (${p218Death.length} — 23 Griblje-vpisov = NOV-REKORD-PREDZGODOVINE! / 103 vpisov kronološko-štetje!)`);
  const p218Houses = p218Death.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
  if (p218Houses.join(",") !== "5,5,19,19,20,21,21,24,26,29,33,37,39,39,49,52,52,57,58,65,65,69,74")
    p218Errors.push(`hiše 1859 neujemane — najdeno: ${p218Houses.join(",")}`);
  if (HOUSE_VITALS.length !== 1632)
    p218Errors.push(`HOUSE_VITALS ≠ 1632 (${HOUSE_VITALS.length} — P217: 1609; P218: + 23 blokov 1859-04106 = 1632!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length !== 413)
    p218Errors.push(`bloki 04106 ≠ 413 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length} — P218: 23 × 1859 + P217: 9 × 1860 + P216: 10 × 1861 + P215: 9 × 1862 + P214: 7 × 1863 + P213: 17 × 1864 + P212: 13 × 1865 + P211: 13 × 1866 + P210: 20 × 1867 + P209: 13 × 1868 + P208: 14 × 1869 + P207: 12 × 1870 + P206: 11 × 1871 + P205: 17 × 1872 + P204: 38 × 1873 + P203: 21 × 1874 + P202: 10 × 1875 + P201: 20 × 1876 + P200: 8 × 1877 + P199: 23 × 1878 + P198: 9 × 1879 + P197: 13 × 1880 + P192: 16 × 1885 + P193: 21 × 1884 + P194: 11 × 1883 + P195: 16 × 1882 + P196: 19 × 1881 = 413!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && (h.year ?? 0) !== 1859 && (h.year ?? 0) !== 1860 && (h.year ?? 0) !== 1861 && (h.year ?? 0) !== 1862 && (h.year ?? 0) !== 1863 && (h.year ?? 0) !== 1864 && (h.year ?? 0) !== 1865 && (h.year ?? 0) !== 1866 && (h.year ?? 0) !== 1867 && (h.year ?? 0) !== 1868 && (h.year ?? 0) !== 1869 && (h.year ?? 0) !== 1870 && (h.year ?? 0) !== 1871 && (h.year ?? 0) !== 1872 && (h.year ?? 0) !== 1873 && (h.year ?? 0) !== 1874 && (h.year ?? 0) !== 1875 && (h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)
    p218Errors.push("04106-bloki izven {1859, ..., 1885} (predzgodovina: 1857–1858 še nebrani!)");
  if (!p218Death.some((h) => h.houseNo === "65" && h.whatSi.includes("h65-NIT-1/2") && h.whatSi.includes("GENICKSTARRE-EPIDEMIJA-1/4")))
    p218Errors.push("★★★ h65-×2-1859 (z24-Graes-GENICKSTARRE + z97-Brince!) ni označena");
  if (!p218Death.some((h) => h.houseNo === "49" && h.whatSi.includes("TAIL-P217-KOREKCIJA-MAKS") && h.whatSi.includes("14-DNI")))
    p218Errors.push("★★★ z94-TAIL-P217-KOREKCIJA-MAKS (Petek-16J-FALSIFICIRAN → 14-DNI!) ni označena");
  if (!p218Death.some((h) => h.houseNo === "69" && h.whatSi.includes("PARIČ-FRAISEN-klaster") && h.whatSi.includes("Joh.-Knavs")))
    p218Errors.push("★★★ z5+z6-PARIČ-FRAISEN-klaster-×2 + NOV-DUHOVNIK-'Joh.-Knavs' ni označena");
  if (!p218Death.some((h) => h.houseNo === "52" && h.whatSi.includes("TRAJNI-DUEL") && h.whatSi.includes("99-J")))
    p218Errors.push("★★★ z81-TRAJNI-DUEL-99J-vs-83J ni označena");
  if (!p218Death.some((h) => h.houseNo === "19" && h.whatSi.includes("GENICKSTARRE-EPIDEMIJA-4/4")))
    p218Errors.push("★★★ GENICKSTARRE-EPIDEMIJA-4/4 (z32-odrasla-40J!) ni označena");
  push(
    "qa-p218-parish-death-1859-04106",
    "P218: ŽUPNIJA PODZEMELJ — MRLIŠKA PREDZGODOVINA 04106, LETO 1859 = 27. LETO PREDZGODOVINSKE LINIJE (issue #18): okvir — s011–s019 == Pag. 6–13 (pag = sken−5; SANDBOX-RESET-REGENERACIJA: 2×-neodvisna-prenosa-md5-9/9 + vsebinska-križ-tail-vs-P217-4/6-1:1!) + **★★★ 103-VPIISOV-ŠTEVJE-IZ-VRSTIC-20.×** (written-1–91-ČISTO + 93–103 = 102 + 1-NEŠTEVILČENA-s15-r12-Jalkič — vrstna-aritmetika 7+12+14+11+12(+1!)+12+12+12+11!) + **★★★ MEJA-1858/59 = s11 (NASLOVNI-LIST-'Sterb-Buch.'-DEEL-2 — NOVI-TISKANI-STOLPCI (Religion/Ledig/Verheirath/Verwittwet/Geschlecht-ločeno!) + '1858'-tail-glava-KROP (arb_s11_meja-glyph-1-8-5-8-BREZ-'9'!) + tail-54–57-1858 (4-vrstice — 0-GRIBLJE!) + VSOTNA-'1 8 [5 9]'-RAZPETE-CIFRE (P214-TIP-2.-INSTANCE — '1 8'-KROP-JASNO + '5'-rob!) + restart-z1–z7-BREZ-Ločne-glave — MARKER=VSOTNA!) = 56.-POTRDITEV-invariante!** + **★★★ LUKNJA-92 (NOV-TIP!): s18-konča-91 (KROP-2.×!) → s19-začne-93 (KROP-'93-pravilna'!) — duhovnik-PRESKOČIL-92!** + **★★★ s19-NASLOVNI-LIST-'Sterb-Buch.'-PONOVLJEN + Dec-1859-nadaljevanje-93–103-BREZ-restarta (piše-ČEZ-natisnjeni-naslov!)** + **★★★ NEŠTEVILČENA-VRSTICA-s15-r12-Jalkič (duhovnik-skoči-55→56!)** + **★★★ GENICKSTARRE-EPIDEMIJA-×4 (NOV-VZROK-v-korpusu!): z24-Graes-h65-2-tedna-Apr-16 + z25-Keržan-h57-63J-Apr-19 + z31-Trnovec-h5-1-mj-Mai-14 + z32-Križič-h19-40J-Mai-21 — 4-smrti-v-5-tednih!** + **★★★ NOV-DUHOVNIK-'Joh.-Knavs'** (podpisi-×7-JASNIH (z5/z6/z73/z80/z86/z94/z97) + 1-DUEL (z76-'J.-Halo[?]') + Jalkič-duhovnik-polje! — Knavs-DRUŽINA-h52-1880s-X-open-vez!) + **★★★ P217-TAIL-MISREADI-KOREKCIJE (s19-nikoli-KROP'd-v-P217!): z95→z94 + z100→z97-MARGINALI (KROP-stolpec-93–103-ČISTO!) + z94-'Jožef-Petek-16J'-FALSIFICIRAN→'Josmat[?]-Padierž[?]-14-DNI' (PAS+VLM-2:1! ENOTE-DNI!) + z97-'Valentin-Brino'→'⅄onalfur[?Valentin?]-Brince[?]' + z73-KLARA-potrjena (KROP-row-'Klana'-vs-fresh-'Elena'!) + z76-ime-TRI (Marlfannina[?]/Katharina/Paulmann!) + z86-ime-DUEL (Anastasia[P217+KROP-glyph]/Katharina[fresh]!)** + **★★★ z5+z6-PARIČ-FRAISEN-klaster-×2-ISTA-DATA-Jän-27/29 (Marija-Vranoviče-h15-10-tednov + Marko[?]-Griblje-h69-1J — 2-otroka-ČEZ-VASI!)** + **★★★ z81-STAROST-TRAJNI-DUEL-X-open (99-J[VLM+KROP-2×!]-vs-83-J[P217!] — Posdiac[?]-h52-NAJSTAREJŠI-1859!)** + **★★★ PEZDIRC-MREŽA-globlje ('Posdiac/Pesdire/Pardire/Podire'≈Pezdirc-grafije: z73/z81/z94! + h52 + h20!)** + hišne-niti: h65-×2 (z24+z97 — P155-1889-MILEK-hiša — 3-obdobja!) + h52-×2 (Knavs-družina-hiša!) + h19-×2 (KRIŽIČ/HRIČ!) + h21-×2 (Požekh!) + h39-×2 (ŠIMEC-grafia-z52!) + h5-×2 (FILAK-nit!) + h58→1860-POŽEK + h57→1860-VALENTIN + h26→1861-MALEŠIČ + h69→1889-Brinec-P155 + h33→1863-FILAK-Grem + h37→1865-HUSIČ + h24→1860-Brenc + NOVE-hiše: h20/h24/h26/h29/h33/h49/h57/h69/h74 (korpus-100→107!); **★★★ 23-GRIBLJE-REKORD-PREDZGODOVINE (prej-20-1867!) / 16 hiš (6-×2!)** + 1. VOJAK-stan (z61-Ulasič-Lediknant!) + MARKTSFREIBN[?Marbmil]-×2 (z57+z65!) + meseci-GRIBLJE-Juni-×0 (edina-luknja!) + August-×6-MAX-klaster + ekstremi-14-DNI→99J + otroška-umrljivost-35%-8/23; **23 NOVIH BLOKOV parish.ts: vitals 1609 → 1632 · 04106 = 390 → 413 · 04894 = 520-NESPREMENJENO · korpus-100→107-hiš-X-open**; skripte p218 (fetch-2×-md5-9/9 + read-×9 + krop-40 (stolpci-×8 + arb-×3 + vrste-×13 + PAS-×4 + traki!) + build-entries + build-proof) + qa-p218 (218. kontrola!) + dokaz parish-death-1859-04106.json (103 entries: 23-Griblje + 80-druge!) + pt-luknja-413/1632; **★★★ PREDZGODOVINA-LINIJA-27/29-LET!** (P219-LEAD: 1858 — s11-tail-ŽE-VLM (54–57: 4-vrstice-1858 + vsotna + '1858'-glava-KROP! — 0-GRIBLJE-tail!) → probe-s004–s011!)",
    "P218: THE PARISH OF PODZEMELJ — THE DEATH-REGISTER-PREHISTORY 04106, THE YEAR 1859 = THE 27th YEAR (issue #18): the-frame + **★★★ 103-ENTRIES-ROW-COUNTING-20th-×** (written-1–91-CLEAN + 93–103 = 102 + 1-UNNUMBERED-s15-r12-Jalkič!) + **★★★ THE-1858/59-BOUNDARY = s11 (the-TITLE-PAGE-'Sterb-Buch.'-VOLUME-2 — NEW-PRINTED-COLUMNS + the-'1858'-tail-header-KROP + the-SUM-ROW-'1 8 [5 9]'-SPREAD-DIGITS (P214-TYPE-2nd-INSTANCE!) + the-restart-z1–z7!) = the-56th-CONFIRMATION!** + **★★★ THE-GAP-92 (NEW-TYPE!): s18-ends-91 → s19-starts-93 — the-priest-SKIPPED-92!** + **★★★ s19-TITLE-PAGE-REPEATED + the-Dec-1859-continuation-WRITTEN-OVER-the-printed-title!** + **★★★ THE-UNNUMBERED-ROW-s15-r12-Jalkič** + **★★★ THE-GENICKSTARRE-EPIDEMIC-×4 (NEW-CAUSE!): 4-deaths-in-5-weeks!** + **★★★ THE-NEW-PRIEST-'Joh.-Knavs'** (7-clear-signatures + Knavs-FAMILY-h52-X-open!) + **★★★ THE-P217-TAIL-MISREAD-CORRECTIONS (z94/z97-marginals + names + age-16J→14-DAYS-FALSIFIED! + z97-Valentin-duel + z73-KLARA-confirmed!)** + **★★★ THE-z5+z6-PARIČ-FRAISEN-CLUSTER-×2-same-date** + **★★★ z81-AGE-TRAJNI-DUEL (99-vs-83!)** + **★★★ THE-PEZDIRC-NETWORK-deeper** + house-threads (h65-×2-MILEK-3-eras! + h52-×2-Knavs + h19/h21/h39/h5-×2 + h58→1860-POŽEK + h57→VALENTIN + h26→MALEŠIČ + h69→1889-Brinec!) + **★★★ 23-GRIBLJE-THE-PREHISTORY-RECORD (prev-20-1867!) / 16-houses (6-×2!)** + the-1st-SOLDIER-stan (z61-Lediknant!) + extremes-14-DAYS→99-YEARS + child-mortality-35%-8/23; **23 NEW BLOCKS: the vitals 1609 → 1632 · the 04106 = 390 → 413**; the scripts p218 + the qa-p218 (the 218th check!) + the evidence parish-death-1859-04106.json (103 entries!) + the pt-gap-413/1632; **★★★ THE-PREHISTORY-LINE-27/29-YEARS!** (the P219-LEAD: 1858 — the-s11-tail-ALREADY-READ (4-lines + the-'1858'-header-KROP!) → the-probe-s004–s011!)",
    p218Errors.length === 0,
    p218Errors.length === 0
      ? `23 vpisov / 103 vrstic (števje-iz-vrstic-20.×! written-1–91-ČISTO + 93–103 + NEŠTEVILČENA-Jalkič — LUKNJA-92!) / 16 hiš (6-×2!) · MEJA-s11-NASLOVNI-LIST-DEEL-2-'1858'-glava-KROP-VSOTNA-'1 8 [5 9]'-marker-56.-POTRDITEV · LUKNJA-92 · s19-naslovni-list-potavljen · GENICKSTARRE-EPIDEMIJA-×4 · NOV-DUHOVNIK-'Joh.-Knavs' · P217-tail-KOREKCIJE (z94-14-DNI-FALSIFIKACIJA + z97-margin-97!) · PARIČ-klaster-×2 · z81-99J[~83!]-DUEL · PEZDIRC-MREŽA-globlje · h65-×2-MILEK-3-obdobja · 1.-VOJAK-Lediknant · **PREDZGODOVINA-27/29!** · vitals 1632 · 04106 413 · 04894 520`
      : p218Errors.join("; "),
  );
  }

'''
src = src.replace(ANCHOR, BLOCK + ANCHOR, 1)
src = src.replace("HOUSE_VITALS.length !== 1609", "HOUSE_VITALS.length !== 1632")
src = src.replace('04106").length !== 390', '04106").length !== 413')
src = src.replace("(h.year ?? 0) !== 1860 &&", "(h.year ?? 0) !== 1859 && (h.year ?? 0) !== 1860 &&")
src = src.replace("1857–1860 še nebrani!", "1857–1859 še nebrani!")
src = src.replace("1857–1862 še nebrani!", "1857–1859 še nebrani!")
src = src.replace("1857–1867 še nebrani!", "1857–1859 še nebrani!")
src = src.replace("izven {1860,", "izven {1859, 1860,")
src = src.replace("izven {1861, ..., 1885}", "izven {1859, 1861, ..., 1885}")
src = src.replace("vitals 1609 · 04106 390 · 04894 520", "vitals 1632 · 04106 413 · 04894 520")
src = src.replace("pt-luknja-390/1609", "pt-luknja-413/1632")
QA.write_text(src, encoding="utf-8")
print(f"qa-parish: 1632×{src.count('HOUSE_VITALS.length !== 1632')} · 413×{src.count('04106\").length !== 413')} · 1859-guard×{src.count('(h.year ?? 0) !== 1859')}")

files = sorted(set(glob.glob(str(ROOT / "scripts/**/*.py"), recursive=True) + glob.glob(str(ROOT / "scripts/**/*.mjs"), recursive=True)))
skip = ("p59_ps_blatt_headers", "p199_", "p200_", "p201_", "p202_", "p203_", "p204_", "p205_", "p206_", "p207_", "p208_", "p210_", "p211_", "p212_", "p213_", "p214_", "p215_", "p216_", "p217_", "p218_")
patched = 0
for f in files:
    if any(s2 in f for s2 in skip): continue
    t = Path(f).read_text(encoding="utf-8")
    if "1609" not in t and "== 390" not in t: continue
    o = t
    t = t.replace("1609", "1632").replace('.get("04106") == 390', '.get("04106") == 413').replace("04106 == 390", "04106 == 413").replace("04106==390", "04106==413").replace("skupaj == 390", "skupaj == 413").replace('"04106") == 390', '"04106") == 413').replace("(04106, 390)", "(04106, 413)").replace("== 390,", "== 413,")
    if t != o:
        Path(f).write_text(t, encoding="utf-8"); patched += 1
print(f"skripte-patched: {patched}")

vpatched = 0
for f in sorted(ROOT.glob("scripts/p19*.py")) + sorted(ROOT.glob("scripts/p2[0-9][0-9]_parish*.py")):
    if "p218" in f.name: continue
    t = f.read_text(encoding="utf-8"); o = t
    for a, b in [("04106 == 390", "04106 == 413"), ("04106==390", "04106==413"),
                 ('04106": 390', '04106": 413'), ("skupaj == 390", "skupaj == 413"),
                 ('"04106") == 390', '"04106") == 413'), ("(04106, 390)", "(04106, 413)"),
                 ('byBook"]["04106"] == 390', 'byBook"]["04106"] == 413'),
                 ('["04106"] == 390', '["04106"] == 413'),
                 ("vitals == 1609", "vitals == 1632"), ("vitalsTotal == 1609", "vitalsTotal == 1632"),
                 ('vitalsTotal"] == 1609', 'vitalsTotal"] == 1632'),
                 ('"vitalsTotal": 1609', '"vitalsTotal": 1632'),
                 ('\\"vitalsTotal\\": 1609', '\\"vitalsTotal\\": 1632'),
                 ('!== 1609"', '!== 1632"'),
                 ("1609-številcev", "1632-številcev"),
                 ("vitals-števec-1609", "vitals-števec-1632"), ("vitals-1609", "vitals-1632")]:
        t = t.replace(a, b)
    t = re.sub(r'set\(izven\) == \{"1860"', 'set(izven) == {"1859", "1860"', t)
    t = t.replace('",".join(leta) == "1860,1861', '",".join(leta) == "1859,1860,1861')
    t = t.replace('join(leta) == "1860,1861,1862,1863,1864,1865,1866,1867,1868,1869,1870,1871,1872,1873,1874,1875,1876,1877,1878,1879,1880,1881,1882,1883,1884,1885"',
                  'join(leta) == "1859,1860,1861,1862,1863,1864,1865,1866,1867,1868,1869,1870,1871,1872,1873,1874,1875,1876,1877,1878,1879,1880,1881,1882,1883,1884,1885"')
    if t != o:
        f.write_text(t, encoding="utf-8"); vpatched += 1
print(f"verifierji-patched: {vpatched}")

ptp = ROOT / "research/issue17/pt-luknja-18-final.json"
pt = json.loads(ptp.read_text(encoding="utf-8"))
pt["corpus"]["vitalsTotal"] = 1632
pt["corpus"]["byBook"]["04106"] = 413
pt["corpus"]["housesNote"] = (pt["corpus"].get("housesNote") or "") + " | P218: +23-blokov-1859 (04106 390→413, vitals 1609→1632, ŠTEVJE-IZ-VRSTIC-20.×-103 + 23-GRIBLJE-REKORD-PREDZGODOVINE + MEJA-1858/59-s11-NASLOVNI-LIST-DEEL-2-'1858'-glava-KROP-VSOTNA-'1 8 [5 9]'-marker-56.-POTRDITEV (P214-TIP!) + LUKNJA-92-NOV-TIP + NEŠTEVILČENA-Jalkič-NOV-TIP + s19-naslovni-list-potavljen + GENICKSTARRE-EPIDEMIJA-×4-NOV-VZROK + NOV-DUHOVNIK-'Joh.-Knavs' + P217-tail-KOREKCIJE (z94/z97-marginali-ime-starost-vzrok!) + PARIČ-klaster-×2 + z81-99J[~83!]-TRAJNI-DUEL + PEZDIRC-MREŽA-globlje + h65-×2-MILEK-3-obdobja!)"
ptp.write_text(json.dumps(pt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"pt-luknja: {pt['corpus']['vitalsTotal']}/{pt['corpus']['byBook']['04106']}")
