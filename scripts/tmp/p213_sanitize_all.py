#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P213 — INSERT qa-p213 + sanitizacija (1557→1574, 338→355, yearset +1864) + verifier-patch + pt-luknja."""
from pathlib import Path
import glob, json, re

ROOT = Path("/home/z/my-project")
QA = ROOT / "src/lib/qa-parish.ts"
src = QA.read_text(encoding="utf-8")
ANCHOR = "  // ——— qa-p212: MRLIŠKA PREDZGODOVINA 04106 — leto 1865 = 21. leto PREDZGODOVINSKE"
assert src.count(ANCHOR) == 1 and "qa-p213-parish-death-1864-04106" not in src
BLOCK = '''
  // ——— qa-p213: MRLIŠKA PREDZGODOVINA 04106 — leto 1864 = 22. leto PREDZGODOVINSKE
  //      LINIJE (issue #18). 1864 = 91 vpisov (ordinali-1–91 ČISTO — 7.-leto-
  //      zapored!) / 17 Griblje / 16 hiš (h1-×2-ŽELKO!) + ★★★ MEJA-1863/64-s39
  //      (tail-1863-z55–z64 + vsotna-vrstica-1-8-6-4 + restart + '1864'-VELIKA-
  //      LETVICA-na-s40 = 51.-POTRDITEV!) + ★★★ s41-SHIFT-SANACIJA (VLM-zap-+1-
  //      pomik — 2.×-po-P158!) + ★★★ 8-KROP-VIZUALNIH-ADJUDIKACIJ (z18-h14-
  //      PEZDIRC + z27-h3-DRAGOŠ + z33-FILAK + z34-ŠIMIC + z44-h71-γ-7 + z61-h5-
  //      CALIBRACIJA + z85-PEZDIRC-h11 + z85-datumi!) + ANOMALIJA-ne-kronološki-
  //      vnos-z85 + PEZDIRC-×2-hiši + ŽELKO-h1-×2 + otroška-umrljivost-53%!
  //      Dokaz: parish-death-1864-04106.json; skripte p213.
  {
  const p213Errors: string[] = [];
  const p213Death = HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && h.year === 1864);
  if (p213Death.length !== 17)
    p213Errors.push(`bloki 1864 (04106) ≠ 17 (${p213Death.length} — 17 Griblje-vpisov / 91 vpisov vrstno-štetje!)`);
  const p213Houses = p213Death.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
  if (p213Houses.join(",") !== "1,1,2,3,5,11,14,16,18,19,27,34,45,62,63,67,71")
    p213Errors.push(`hiše 1864 neujemane — najdeno: ${p213Houses.join(",")}`);
  if (HOUSE_VITALS.length !== 1574)
    p213Errors.push(`HOUSE_VITALS ≠ 1574 (${HOUSE_VITALS.length} — P212: 1557; P213: + 17 blokov 1864-04106 = 1574!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length !== 355)
    p213Errors.push(`bloki 04106 ≠ 355 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length} — P213: 17 × 1864 + P212: 13 × 1865 + P211: 13 × 1866 + P210: 20 × 1867 + P209: 13 × 1868 + P208: 14 × 1869 + P207: 12 × 1870 + P206: 11 × 1871 + P205: 17 × 1872 + P204: 38 × 1873 + P203: 21 × 1874 + P202: 10 × 1875 + P201: 20 × 1876 + P200: 8 × 1877 + P199: 23 × 1878 + P198: 9 × 1879 + P197: 13 × 1880 + P192: 16 × 1885 + P193: 21 × 1884 + P194: 11 × 1883 + P195: 16 × 1882 + P196: 19 × 1881 = 355!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && (h.year ?? 0) !== 1864 && (h.year ?? 0) !== 1865 && (h.year ?? 0) !== 1866 && (h.year ?? 0) !== 1867 && (h.year ?? 0) !== 1868 && (h.year ?? 0) !== 1869 && (h.year ?? 0) !== 1870 && (h.year ?? 0) !== 1871 && (h.year ?? 0) !== 1872 && (h.year ?? 0) !== 1873 && (h.year ?? 0) !== 1874 && (h.year ?? 0) !== 1875 && (h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)
    p213Errors.push("04106-bloki izven {1864, ..., 1885} (predzgodovina: 1857–1864 še nebrani!)");
  if (!p213Death.some((h) => h.houseNo === "14" && h.whatSi.includes("PEZDIRC-h14-NIT-1864")))
    p213Errors.push("★★★ PEZDIRC-h14-NIT-1864-z18 (KROP-VIZUALNA-ADJUDIKACIJA-3-FAZNA!) ni označena");
  if (!p213Death.some((h) => h.houseNo === "11" && h.whatSi.includes("PEZDIRC-h11")))
    p213Errors.push("★★★ PEZDIRC-h11-z85 (ANOMALIJA-ne-kronološki-vnos + KROP-VIZUAL-×3!) ni označena");
  if (!p213Death.some((h) => h.houseNo === "34" && h.whatSi.includes("FILAK-h34-NIT-1864")))
    p213Errors.push("★★★ FILAK-h34-NIT-1864-z33 (KROP-VIZUAL-'-ilak'!) ni označena");
  if (!p213Death.some((h) => h.houseNo === "1" && h.whatSi.includes("ŽELKO-h1-×2-KLASTER-#2")))
    p213Errors.push("★★★ ŽELKO-h1-×2-MAJ-klaster (z30+z35!) ni označen");
  push(
    "qa-p213-parish-death-1864-04106",
    "P213: ŽUPNIJA PODZEMELJ — MRLIŠKA PREDZGODOVINA 04106, LETO 1864 = 22. LETO PREDZGODOVINSKE LINIJE (issue #18): okvir — s039–s046 == Pag. 34–41 (pag = sken−5; 2×-neodvisna-prenosa-md5-8/8!) + **★★★ MEJA-1863/64 = s39 (tail-1863-z55–z64 + VSHOTNA-VRSTICA-1-8-6-4 + restart-z1–z2! + rokopisna-'1863'-glava-s39 + '1864'-VELIKA-LETVICA-na-s40-glavi = 51.-POTRDITEV-invariante!)** + **★★★ s41-SHIFT-SANACIJA** (VLM-zap-stolpec-+1-pomik-razkrit: margin-N == fresh-row(N-16); KROP-stripi-17–30-VIZUALNO — 2.×-po-P158-lekcija!) + **★★★ 8-KROP-VIZUALNIH-ADJUDIKACIJ** (z18-h14-'4-IMA-ZANKO'+PEZDIRC-glyph-comparacija-z85 + z27-h3-DRAGOŠ-glyph + z33-FILAK-'-ilak'-rez + z34-ŠIMIC-haček + z44-h71-γ-7-S-PREČKO + z61-h5-CALIBRACIJA-z60-'1'/z62-'8' + z85-PEZDIRC-h11-dve-ozki-1 + z85-datumi-Dec-2./4.!) + **★★★ ANOMALIJA-NE-KRONOLOŠKI-VNOS-z85-2.-×-LETA** (Dec-2./4.-vpisan-po-z84-Dec-11.[~] — cf. P212-z13!) + **★★★ 91-VPIISOV-ŠTEVJE-IZ-VRSTIC-15.×** (ordinali-1–91-ČISTO — 7.-LETO-ZAPORED! vrstna-aritmetika 2+14+14+14+15+14+14+4!) + **★★★ PEZDIRC-×2-hiši-1864** (h14-Michael-6-M + h11-Anna-14-let!) + **★★★ ŽELKO-h1-×2-MAJ-KLASTER** (z30-Anna-22-J + z35-Peter-1-J — 13-dni!) + **★★★ FILAK-h34-3.-LETO** + ŠIMEC-×2-hiši (h18+h19!) + POŽEK-h67-nit (→ 1865-z36-ISTI-z36!) + KRIŽAN-×2-hiši (h62-87-J-NAJSTAREJŠA + h63-Kind-von!) + DRAGOŠ-glyph-h3 + ULEDBA-#11-z91 + otroška-umrljivost-53%-9/17 (VIŠJA-kot-1865-31%!); **1864 = 91 vpisov (z1–z91) / 17 Griblje-vpisov / 16 hiš (h1-×2!)**; **17 NOVIH BLOKOV parish.ts: vitals 1557 → 1574 · 04106 = 338 → 355 · 04894 = 520-NESPREMENJENO · p80 94-NESPREMENJENO · korpus 93-NESPREMENJEN**; skripte p213 (fetch-2×-md5-8/8 + read-×8 + krop-×40 + build-entries + build-proof) + qa-p213 (213. kontrola!) + dokaz parish-death-1864-04106.json (91 entries: 17-Griblje + 74-druge!) + pt-luknja-355/1574; **★★★ PREDZGODOVINA-LINIJA-22/29-LET!** (P214-LEAD: 1863 — s39-tail-ŽE-VLM (z55–z64: 10-vrstic-1863-tail + vsotna-1-8-6-4!) → probe-s033–s039!)",
    "P213: THE PARISH OF PODZEMELJ — THE DEATH-REGISTER-PREHISTORY 04106, THE YEAR 1864 = THE 22nd YEAR (issue #18): the-frame + **★★★ THE-1863/64-BOUNDARY = s39 (the-1863-TAIL-z55–z64 + the-SUM-ROW-1-8-6-4 + the-restart-z1–z2! + the-'1864'-BIG-YEAR-on-s40-header = the-51st-CONFIRMATION!)** + **★★★ THE-s41-SHIFT-SANATION** (the-VLM-ordinal-column-+1-slip: margin-N == fresh-row(N-16); KROP-strips-17–30-VISUAL — the-2nd-after-P158-lesson!) + **★★★ 8-KROP-VISUAL-ADJUDICATIONS** (z18-h14-'4-HAS-A-LOOP'+PEZDIRC-glyph-comparison-z85 + z27-h3-DRAGOŠ-glyph + z33-FILAK + z34-ŠIMIC + z44-h71-γ-7 + z61-h5-CALIBRATION + z85-PEZDIRC-h11 + z85-dates!) + **★★★ THE-NON-CHRONOLOGICAL-ENTRY-z85-2nd-OF-THE-YEAR** + **★★★ THE-91-ENTRIES-COUNT-FROM-ROWS-15.×** (ordinals-1–91-CLEAN — the-7th-CONSECUTIVE-CLEAN-YEAR!) + **★★★ PEZDIRC-×2-HOUSES-1864** + **★★★ ŽELKO-h1-×2-MAY-CLUSTER** + FILAK-h34-3rd-YEAR + ŠIMEC-×2 + POŽEK-h67-thread + KRIŽAN-×2 + DRAGOŠ-glyph + ULEDBA-#11 + child-mortality-53%; **1864 = 91 entries / 17 Griblje / 16 houses (h1-×2!)**; **17 NEW BLOCKS: the vitals 1557 → 1574 · the 04106 = 338 → 355**; the scripts p213 + the qa-p213 (the 213th check!) + the evidence parish-death-1864-04106.json (91 entries!) + the pt-gap-355/1574; **★★★ THE-PREHISTORY-LINE-22/29-YEARS!** (the P214-LEAD: 1863 — the-s39-tail-ALREADY-READ → the-probe-s033–s039!)",
    p213Errors.length === 0,
    p213Errors.length === 0
      ? `17 vpisov / 91 vrstic (števje-iz-vrstic-15.×! ordinali-1–91-ČISTO-7.-leto!) / 16 hiš (h1-×2-ŽELKO!) · MEJA-s39-tail-1863 + vsotna-1-8-6-4 + restart + '1864'-glava-s40-51.-POTRDITEV · s41-SHIFT-SANACIJA · 8-KROP-VIZUALNIH-ADJUDIKACIJ · ANOMALIJA-z85-ne-kronološki · PEZDIRC-×2-hiši · ŽELKO-h1-×2 · FILAK-h34 · ŠIMEC-×2 · POŽEK-h67 · KRIŽAN-×2 · otroška-53% · **PREDZGODOVINA-22/29!** · vitals 1574 · 04106 355 · 04894 520`
      : p213Errors.join("; "),
  );
  }

'''
src = src.replace(ANCHOR, BLOCK + ANCHOR, 1)
src = src.replace("HOUSE_VITALS.length !== 1557", "HOUSE_VITALS.length !== 1574")
src = src.replace('04106").length !== 338', '04106").length !== 355')
OLD_SET = "(h.year ?? 0) !== 1865 && (h.year ?? 0) !== 1866 && (h.year ?? 0) !== 1867 && (h.year ?? 0) !== 1868 && (h.year ?? 0) !== 1869 && (h.year ?? 0) !== 1870 && (h.year ?? 0) !== 1871 && (h.year ?? 0) !== 1872 && (h.year ?? 0) !== 1873 && (h.year ?? 0) !== 1874 && (h.year ?? 0) !== 1875 && (h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885"
src = src.replace(OLD_SET, "(h.year ?? 0) !== 1864 && " + OLD_SET)
src = src.replace("04106-bloki izven {1865, 1866, 1867, 1868, 1869, 1870, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1865 še nebrani!)",
                  "04106-bloki izven {1864, 1865, 1866, 1867, 1868, 1869, 1870, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1864 še nebrani!)")
src = src.replace("vitals 1557 · 04106 338 · 04894 520", "vitals 1574 · 04106 355 · 04894 520")
QA.write_text(src, encoding="utf-8")
print(f"qa-parish: {src.count('HOUSE_VITALS.length !== 1574')}")

files = sorted(set(glob.glob(str(ROOT / "scripts/**/*.py"), recursive=True) + glob.glob(str(ROOT / "scripts/**/*.mjs"), recursive=True)))
skip = ("p59_ps_blatt_headers", "p199_", "p200_", "p201_", "p202_", "p203_", "p204_", "p205_", "p206_", "p207_", "p208_", "p210_", "p211_", "p212_", "p213_")
patched = 0
for f in files:
    if any(s2 in f for s2 in skip): continue
    t = Path(f).read_text(encoding="utf-8")
    if "1557" not in t and "== 338" not in t: continue
    o = t
    t = t.replace("1557", "1574").replace('.get("04106") == 338', '.get("04106") == 355').replace("04106 == 338", "04106 == 355").replace("04106==338", "04106==355").replace("skupaj == 338", "skupaj == 355").replace('"04106") == 338', '"04106") == 355').replace("(04106, 338)", "(04106, 355)").replace("== 338,", "== 355,")
    if t != o:
        Path(f).write_text(t, encoding="utf-8"); patched += 1
print(f"skripte-patched: {patched}")

vpatched = 0
for f in sorted(ROOT.glob("scripts/p19*.py")) + sorted(ROOT.glob("scripts/p2[0-9][0-9]_parish*.py")):
    if "p213" in f.name: continue
    t = f.read_text(encoding="utf-8"); o = t
    for a, b in [("04106 == 338", "04106 == 355"), ("04106==338", "04106==355"),
                 ('04106": 338', '04106": 355'), ("skupaj == 338", "skupaj == 355"),
                 ('"04106") == 338', '"04106") == 355'), ("(04106, 338)", "(04106, 355)"),
                 ('byBook"]["04106"] == 338', 'byBook"]["04106"] == 355'),
                 ('["04106"] == 338', '["04106"] == 355'),
                 ("vitals == 1557", "vitals == 1574"), ("vitalsTotal == 1557", "vitalsTotal == 1574"),
                 ('vitalsTotal"] == 1557', 'vitalsTotal"] == 1574'),
                 ('"vitalsTotal": 1557', '"vitalsTotal": 1574'),
                 ('\\"vitalsTotal\\": 1557', '\\"vitalsTotal\\": 1574'),
                 ('!== 1557"', '!== 1574"'),
                 ("1557-številcev", "1574-številcev"),
                 ("vitals-števec-1557", "vitals-števec-1574"), ("vitals-1557", "vitals-1574")]:
        t = t.replace(a, b)
    t = re.sub(r'set\(izven\) == \{"1865"', 'set(izven) == {"1864", "1865"', t)
    t = t.replace('",".join(leta) == "1865,1866', '",".join(leta) == "1864,1865,1866')
    t = t.replace('join(leta) == "1865,1866,1867,1868,1869,1870,1871,1872,1873,1874,1875,1876,1877,1878,1879,1880,1881,1882,1883,1884,1885"',
                  'join(leta) == "1864,1865,1866,1867,1868,1869,1870,1871,1872,1873,1874,1875,1876,1877,1878,1879,1880,1881,1882,1883,1884,1885"')
    if t != o:
        f.write_text(t, encoding="utf-8"); vpatched += 1
print(f"verifierji-patched: {vpatched}")

ptp = ROOT / "research/issue17/pt-luknja-18-final.json"
pt = json.loads(ptp.read_text(encoding="utf-8"))
pt["corpus"]["vitalsTotal"] = 1574
pt["corpus"]["byBook"]["04106"] = 355
pt["corpus"]["housesNote"] = (pt["corpus"].get("housesNote") or "") + " | P213: +17-blokov-1864 (04106 338→355, vitals 1557→1574, ordinali-1–91-ČISTO-7.leto + MEJA-'1864'-51.-POTRDITEV + s41-SHIFT-SANACIJA + 8-KROP-VIZUALNIH-ADJUDIKACIJ + ANOMALIJA-z85 + PEZDIRC-×2-hiši + ŽELKO-h1-×2!)"
ptp.write_text(json.dumps(pt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"pt-luknja: {pt['corpus']['vitalsTotal']}/{pt['corpus']['byBook']['04106']}")
