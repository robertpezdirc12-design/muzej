#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P216 — INSERT qa-p217 + sanitizacija (1590→1600, 371→381, yearset +1861) + verifier-patch + pt-luknja."""
from pathlib import Path
import glob, json, re

ROOT = Path("/home/z/my-project")
QA = ROOT / "src/lib/qa-parish.ts"
src = QA.read_text(encoding="utf-8")
ANCHOR = "  // ——— qa-p215: MRLIŠKA PREDZGODOVINA 04106 — leto 1862 = 24. leto PREDZGODOVINSKE"
assert src.count(ANCHOR) == 1 and "qa-p217-parish-death-1860-04106" not in src
BLOCK = '''
  // ——— qa-p217: MRLIŠKA PREDZGODOVINA 04106 — leto 1860 = 26. leto PREDZGODOVINSKE
  //      LINIJE (issue #18). 1861 = 54 vpisov (ordinali-1–54 ČISTO — 10.-leto-
  //      zapored!) / 10 Griblje / 8 hiš (h42-×3!) + ★★★ MEJA-1860/61-s25
  //      (tail-1860-WRITTEN-53–59 + VSOTNA-'60'-margin-REGISTERJSKA-
  //      ŠTEVILČENJSKA-NAPAKA-NOV-TIP! + VSOTNA-'1|8|...|1'-'1861'-MARKER-
  //      4.-INSTANCE + ROKOPISNA-'1861'-GLAVA = 54.-POTRDITEV! + restart-z1–z5!)
  //      + ★★★ s27=s26-DOUBLE-SCAN-3.-v-knjigi + ★★★ VLM-margin-misreadi-
  //      KOREKCIJE (s23-+1-pomik! + z53-1860-avgust! + z20-vas-'Zemelj'! +
  //      z18-mesec-'Mai'!) + ★★★ h42-×3-APR-KLASTER (družina-HIPEZOZA!) +
  //      ★★★ PEZDIRC-MREŽA-×5-1860–1865 + ŽELKO-h1-nit-4.-LETO + ŠIMEC-h18-nit
  //      + POŽEK-h67-nit-ZADNJI-VNOS + URIH-h68/MALEŠIČ-h26/KLOBUČAR-h48-NOVE
  //      + VALENTIN-×2-h57-1860-tail + otroška-umrljivost-50%-5/10 (NAJVIŠJA!).
  //      Dokaz: parish-death-1861-04106.json; skripte p216.
  {
  const p217Errors: string[] = [];
  const p217Death = HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && h.year === 1860);
  if (p217Death.length !== 9)
    p217Errors.push(`bloki 1860 (04106) ≠ 9 (${p217Death.length} — 9 Griblje-vpisov / 73 vpisov kronološko-štetje!)`);
  const p217Houses = p217Death.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
  if (p217Houses.join(",") !== "6,13,24,30,50,55,57,57,58")
    p217Errors.push(`hiše 1860 neujemane — najdeno: ${p217Houses.join(",")}`);
  if (HOUSE_VITALS.length !== 1600)
    p217Errors.push(`HOUSE_VITALS ≠ 1600 (${HOUSE_VITALS.length} — P215: 1590; P216: + 9 blokov 1860-04106 = 1600!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length !== 381)
    p217Errors.push(`bloki 04106 ≠ 381 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length} — P217: 9 × 1860 + P216: 10 × 1861 + P215: 9 × 1862 + P214: 7 × 1863 + P213: 17 × 1864 + P212: 13 × 1865 + P211: 13 × 1866 + P210: 20 × 1867 + P209: 13 × 1868 + P208: 14 × 1869 + P207: 12 × 1870 + P206: 11 × 1871 + P205: 17 × 1872 + P204: 38 × 1873 + P203: 21 × 1874 + P202: 10 × 1875 + P201: 20 × 1876 + P200: 8 × 1877 + P199: 23 × 1878 + P198: 9 × 1879 + P197: 13 × 1880 + P192: 16 × 1885 + P193: 21 × 1884 + P194: 11 × 1883 + P195: 16 × 1882 + P196: 19 × 1881 = 381!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && (h.year ?? 0) !== 1860 && (h.year ?? 0) !== 1861 && (h.year ?? 0) !== 1862 && (h.year ?? 0) !== 1863 && (h.year ?? 0) !== 1864 && (h.year ?? 0) !== 1865 && (h.year ?? 0) !== 1866 && (h.year ?? 0) !== 1867 && (h.year ?? 0) !== 1868 && (h.year ?? 0) !== 1869 && (h.year ?? 0) !== 1870 && (h.year ?? 0) !== 1871 && (h.year ?? 0) !== 1872 && (h.year ?? 0) !== 1873 && (h.year ?? 0) !== 1874 && (h.year ?? 0) !== 1875 && (h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)
    p217Errors.push("04106-bloki izven {1861, ..., 1885} (predzgodovina: 1857–1860 še nebrani!)");
  if (!p217Death.some((h) => h.houseNo === "42" && h.whatSi.includes("h42-×3-APR-KLASTER")))
    p217Errors.push("★★★ h42-×3-APR-KLASTER (družina-HIPEZOZA — z14+z15+z17!) ni označena");
  push(
    "qa-p217-parish-death-1860-04106",
    "P216: ŽUPNIJA PODZEMELJ — MRLIŠKA PREDZGODOVINA 04106, LETO 1861 = 25. LETO PREDZGODOVINSKE LINIJE (issue #18): okvir — s023–s030 == Pag. 18–25 (pag = sken−5; 2×-neodvisna-prenosa-md5-8/8 + s029/s030-carry-P215!) + **★★★ MEJA-1860/61 = s25 (tail-1860-WRITTEN-53–59 + VSOTNA-'60'-margin-REGISTERJSKA-ŠTEVILČENJSKA-NAPAKA-NOV-TIP! + VSOTNA-'1|8|...|1'-'1861'-MARKER-4.-INSTANCE + ROKOPISNA-'1861'-GLAVA = 54.-POTRDITEV! + restart-z1–z5!)** + **★★★ MEJA-1861/62 = s30 (vsotna-'1|8|6|2'-'1862'-MARKER-3.-instance + RESTART-BREZ-rokopisne-glave — P215!)** + **★★★ NOV-TIP-ANOMALIJE: REGISTERJSKA-ŠTEVILČENJSKA-NAPAKA-1860** (s25-tail-WRITTEN-53–59-'60' — prejšnja-s24-že-53–66! kronološko-#67–#73! KROP-s25_zap_tight-1:1!) + **★★★ s27=s26-DOUBLE-SCAN-3.-v-knjigi** (2×-NEODVISNA-VLM-z6–z18!) + **★★★ VLM-margin-misreadi-KOREKCIJE** (s23-'41–53'→'40–52'-+1-pomik-KROP! + z53-1860-mesec-'September'→'avgust-nadaljevanje'-KROP! + z20-vas-'Griblje'→'Zemelj'-KROP! + z18-mesec-'April'→'Mai'-KROP! — kronološka-veriga-ČISTA!) + **★★★ h42-×3-APR-KLASTER** (z14+z15+z17: 6-dnih! PERDIU/PEZDIRC[?]-družina-HIPEZOZA — ime-GARBLE-X-open!) + **★★★ PEZDIRC-MREŽA-×5-1860–1865** (h30[?]-tail-z65 + h42-×3[?] + z1-'von-Griblje[?]'-1862 + h14/h11-1864 + h14-1865!) + **★★★ ŽELKO-h1-NIT-4.-LETO** (z7-47J → 1862-Maria-½J → 1864-×2!) + **★★★ ŠIMEC-h18-NIT-GLOBLJE** (z35-Anna-Goric-1½J → 1863-Georg → 1864-Peter!) + **★★★ POŽEK-h67-NIT-ZADNJI-1861-VNOS** (z54-Mathias-2J → 1865-z36-36J-ISTO-HIŠA!) + **URIH-h68-NOVA** (z11-ime-4-BRANJA-DUEL-SPOL-X-open!) + **MALEŠIČ-h26-NOVA** (z30-Mathias-59J-Abzehrung-3×!) + **KLOBUČAR-h48-NOVA** (z32-Katharina-15J-TRAJNI-DUEL-15/65/1!) + **VALENTIN-×2-h57-1860-tail** (Dez-10/12 + 10/13 — oče-sin-hipoteza?) + **★★★ 54-VPIISOV-ŠTEVJE-IZ-VRSTIC-18.×** (ordinali-1–54-ČISTO — 10.-LETO-ZAPORED! vrstna-aritmetika 5+13+14+16+6!) + otroška-umrljivost-11%-1/9 (NAJNIŽJA-v-predzgodovini!); **1860 = 73 vpisov (z1–z73 kronološko) / 9 Griblje-vpisov / 8 hiš (h57 ×2!)**; **10 NOVIH BLOKOV parish.ts: vitals 1590 → 1600 · 04106 = 371 → 381 · 04894 = 520-NESPREMENJENO · p80 94-NESPREMENJENO · korpus-98→99-hiš-X-open**; skripte p217 (fetch-2×-md5-7/7 + read-×6 + krop-×15 + build-entries + build-proof) + qa-p217 (216. kontrola!) + dokaz parish-death-1860-04106.json (73 entries: 9-Griblje + 64-druge!) + pt-luknja-381/1600; **★★★ PREDZGODOVINA-LINIJA-26/29-LET!** (P218-LEAD: 1859 — s17/s18/s19-ŽE-VLM (z68–z112: 45-vrstic-tail!) → probe-s011–s017!)",
    "P216: THE PARISH OF PODZEMELJ — THE DEATH-REGISTER-PREHISTORY 04106, THE YEAR 1860 = THE 26th YEAR (issue #18): the-frame + **★★★ THE-1860/61-BOUNDARY = s25 (the-1860-tail-WRITTEN-53–59 + the-SUM-ROW-'60'-margin-REGISTER-NUMBERING-ERROR-NEW-TYPE! + the-SUM-ROW-'1861'-MARKER-4th-INSTANCE + the-'1861'-handwritten-header = the-54th-CONFIRMATION! + the-restart-z1–z5!)** + **★★★ THE-1861/62-BOUNDARY = s30 (P215!)** + **★★★ NEW-ANOMALY-TYPE: THE-REGISTER-NUMBERING-ERROR-1860** (the-priest-wrote-53–59-when-67–73-chronologically!) + **★★★ s27=s26-DOUBLE-SCAN-3rd-IN-THE-BOOK** + **★★★ VLM-MARGIN-MISREAD-CORRECTIONS** (s23-+1-shift + z53-month-August-continuation + z20-village-'Zemelj' + z18-month-'Mai' — the-chronological-chain-CLEAN!) + **★★★ THE-h42-×3-APRIL-CLUSTER** (the-FAMILY-HYPOTHESIS-6-days!) + **★★★ THE-PEZDIRC-NETWORK-×5-1860–1865** + **★★★ THE-ŽELKO-h1-THREAD-4th-YEAR** + **★★★ THE-ŠIMEC-h18-THREAD-DEEPER** + **★★★ THE-POŽEK-h67-THREAD-THE-LAST-1861-ENTRY** + **URIH-h68-NEW** (the-name-4-READINGS-DUEL-GENDER-X-open!) + **MALEŠIČ-h26-NEW** + **KLOBUČAR-h48-NEW** (the-TRAJNI-DUEL-15/65/1!) + **VALENTIN-×2-h57-1860-tail** + child-mortality-11%-1/9 (THE-LOWEST-again!); **1860 = 73 entries / 9 Griblje / 8 houses (h57 ×2!)**; **10 NEW BLOCKS: the vitals 1590 → 1600 · the 04106 = 371 → 381**; the scripts p217 + the qa-p217 (the 216th check!) + the evidence parish-death-1860-04106.json (73 entries!) + the pt-gap-381/1600; **★★★ THE-PREHISTORY-LINE-25/29-YEARS!** (the P217-LEAD: 1860 — the-s23/s24/s25-tail-ALREADY-READ → the-probe-s017–s023!)",
    p217Errors.length === 0,
    p217Errors.length === 0
      ? `9 vpisov / 73 vrstic (števje-iz-vrstic-19.×! kronološko-z1–z73 — WRITTEN-duplikat-REGISTERJSKA-NAPAKA!) / 8 hiš (h57 ×2!) · MEJA-s25-tail-1860-WRITTEN-53–59 + vsotna-'60'-REGISTERJSKA-NAPAKA-NOV-TIP + vsotna-'1861'-marker-4.-INSTANCE + '1861'-rokopisna-glava-54.-POTRDITEV · s27=s26-DOUBLE-SCAN-3.-v-knjigi · VLM-misreadi-KOREKCIJE (s23-+1 + z53-avgust + z20-Zemelj + z18-Mai!) · h42-×3-APR-KLASTER-družina · PEZDIRC-MREŽA-×5 · ŽELKO-h1-4.-leto · ŠIMEC-h18-GLOBLJE · POŽEK-h67-ZADNJI-VNOS · URIH-h68-4-BRANJA · MALEŠIČ-h26 · KLOBUČAR-h48-TRAJNI-DUEL · VALENTIN-×2-h57-tail · otroška-50% (NAJVIŠJA!) · **PREDZGODOVINA-25/29!** · vitals 1600 · 04106 381 · 04894 520`
      : p217Errors.join("; "),
  );
  }

'''
src = src.replace(ANCHOR, BLOCK + ANCHOR, 1)
src = src.replace("HOUSE_VITALS.length !== 1590", "HOUSE_VITALS.length !== 1600")
src = src.replace('04106").length !== 371', '04106").length !== 381')
OLD_SET = "(h.year ?? 0) !== 1862 && (h.year ?? 0) !== 1863 && (h.year ?? 0) !== 1864 && (h.year ?? 0) !== 1865 && (h.year ?? 0) !== 1866 && (h.year ?? 0) !== 1867 && (h.year ?? 0) !== 1868 && (h.year ?? 0) !== 1869 && (h.year ?? 0) !== 1870 && (h.year ?? 0) !== 1871 && (h.year ?? 0) !== 1872 && (h.year ?? 0) !== 1873 && (h.year ?? 0) !== 1874 && (h.year ?? 0) !== 1875 && (h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885"
src = src.replace(OLD_SET, "(h.year ?? 0) !== 1860 && (h.year ?? 0) !== 1861 && " + OLD_SET)
src = src.replace("04106-bloki izven {1862, 1863, 1864, 1865, 1866, 1867, 1868, 1869, 1870, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1862 še nebrani!)",
                  "04106-bloki izven {1860, 1861, 1862, 1863, 1864, 1865, 1866, 1867, 1868, 1869, 1870, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1860 še nebrani!)")
src = src.replace("vitals 1590 · 04106 371 · 04894 520", "vitals 1600 · 04106 381 · 04894 520")
QA.write_text(src, encoding="utf-8")
print(f"qa-parish: {src.count('HOUSE_VITALS.length !== 1600')}")

files = sorted(set(glob.glob(str(ROOT / "scripts/**/*.py"), recursive=True) + glob.glob(str(ROOT / "scripts/**/*.mjs"), recursive=True)))
skip = ("p59_ps_blatt_headers", "p199_", "p200_", "p201_", "p202_", "p203_", "p204_", "p205_", "p206_", "p207_", "p208_", "p210_", "p211_", "p212_", "p213_", "p214_", "p215_", "p216_", "p217_")
patched = 0
for f in files:
    if any(s2 in f for s2 in skip): continue
    t = Path(f).read_text(encoding="utf-8")
    if "1590" not in t and "== 371" not in t: continue
    o = t
    t = t.replace("1590", "1600").replace('.get("04106") == 371', '.get("04106") == 381').replace("04106 == 371", "04106 == 381").replace("04106==371", "04106==381").replace("skupaj == 371", "skupaj == 381").replace('"04106") == 371', '"04106") == 381').replace("(04106, 371)", "(04106, 381)").replace("== 371,", "== 381,")
    if t != o:
        Path(f).write_text(t, encoding="utf-8"); patched += 1
print(f"skripte-patched: {patched}")

vpatched = 0
for f in sorted(ROOT.glob("scripts/p19*.py")) + sorted(ROOT.glob("scripts/p2[0-9][0-9]_parish*.py")):
    if "p217" in f.name: continue
    t = f.read_text(encoding="utf-8"); o = t
    for a, b in [("04106 == 371", "04106 == 381"), ("04106==371", "04106==381"),
                 ('04106": 371', '04106": 381'), ("skupaj == 371", "skupaj == 381"),
                 ('"04106") == 371', '"04106") == 381'), ("(04106, 371)", "(04106, 381)"),
                 ('byBook"]["04106"] == 371', 'byBook"]["04106"] == 381'),
                 ('["04106"] == 371', '["04106"] == 381'),
                 ("vitals == 1590", "vitals == 1600"), ("vitalsTotal == 1590", "vitalsTotal == 1600"),
                 ('vitalsTotal"] == 1590', 'vitalsTotal"] == 1600'),
                 ('"vitalsTotal": 1590', '"vitalsTotal": 1600'),
                 ('\\"vitalsTotal\\": 1590', '\\"vitalsTotal\\": 1600'),
                 ('!== 1590"', '!== 1600"'),
                 ("1590-številcev", "1600-številcev"),
                 ("vitals-števec-1590", "vitals-števec-1600"), ("vitals-1590", "vitals-1600")]:
        t = t.replace(a, b)
    t = re.sub(r'set\(izven\) == \{"1862"', 'set(izven) == {"1860", "1861", "1862"', t)
    t = t.replace('",".join(leta) == "1862,1863', '",".join(leta) == "1860,1861,1862,1863')
    t = t.replace('join(leta) == "1862,1863,1864,1865,1866,1867,1868,1869,1870,1871,1872,1873,1874,1875,1876,1877,1878,1879,1880,1881,1882,1883,1884,1885"',
                  'join(leta) == "1860,1861,1862,1863,1864,1865,1866,1867,1868,1869,1870,1871,1872,1873,1874,1875,1876,1877,1878,1879,1880,1881,1882,1883,1884,1885"')
    if t != o:
        f.write_text(t, encoding="utf-8"); vpatched += 1
print(f"verifierji-patched: {vpatched}")

ptp = ROOT / "research/issue17/pt-luknja-18-final.json"
pt = json.loads(ptp.read_text(encoding="utf-8"))
pt["corpus"]["vitalsTotal"] = 1600
pt["corpus"]["byBook"]["04106"] = 381
pt["corpus"]["housesNote"] = (pt["corpus"].get("housesNote") or "") + " | P216: +10-blokov-1861 (04106 371→381, vitals 1590→1600, ordinali-1–54-ČISTO-10.leto + MEJA-'1861'-54.-POTRDITEV (vsotna-'1|8'-marker + rokopisna-glava-OBOJE!) + NOV-TIP-REGISTERJSKA-ŠTEVILČENJSKA-NAPAKA (s25-tail-written-53–59-'60'!) + s27=s26-DOUBLE-SCAN-3.× + h42-×3-APR-KLASTER-družina + PEZDIRC-MREŽA-×5 + ŽELKO-h1-4.-leto + ŠIMEC-h18-GLOBLJE + POŽEK-h67-ZADNJI-VNOS + VLM-margin-misreadi-KOREKCIJE!)"
ptp.write_text(json.dumps(pt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"pt-luknja: {pt['corpus']['vitalsTotal']}/{pt['corpus']['byBook']['04106']}")
