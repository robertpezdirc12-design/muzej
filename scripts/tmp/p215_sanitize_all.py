#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P215 — INSERT qa-p215 + sanitizacija (1581→1590, 362→371, yearset +1862) + verifier-patch + pt-luknja."""
from pathlib import Path
import glob, json, re

ROOT = Path("/home/z/my-project/muzej-backup")
QA = ROOT / "src/lib/qa-parish.ts"
src = QA.read_text(encoding="utf-8")
ANCHOR = "  // ——— qa-p214: MRLIŠKA PREDZGODOVINA 04106 — leto 1863 = 23. leto PREDZGODOVINSKE"
assert src.count(ANCHOR) == 1 and "qa-p215-parish-death-1862-04106" not in src
BLOCK = '''
  // ——— qa-p215: MRLIŠKA PREDZGODOVINA 04106 — leto 1862 = 24. leto PREDZGODOVINSKE
  //      LINIJE (issue #18). 1862 = 60 vpisov (ordinali-1–60 ČISTO — 9.-leto-
  //      zapored!) / 9 Griblje / 7 hiš (h5+h61-×2!) + ★★★ MEJA-1861/62-s30
  //      (tail-1861-z49–z54 + VSOTNA-'1|8|6|2'-'1862'-MARKER-3.-INSTANCE +
  //      restart-z1–z7! + NOVA-VARIANTA: BREZ-rokopisne-'1862'-glave — vsotna=
  //      EDINI-marker! + KROP-zap-stolpec: '1861'-glava + '49–54' — VLM-
  //      misread-'29–34'-KOREKCIJA!) + ★★★ MEJA-1862/63-s35 (vsotna-'1863' +
  //      '1863'-rokopisna-glava = 52.-POTRDITEV — P214!) + ★★★ s32=s33-DOUBLE-
  //      SCAN-2.-v-knjigi (2×-NEODVISNA-VLM-z24–z39!) + ★★★ FILAK-MREŽA-×3-1862
  //      (z11-Katharina-h61-F/T/K-DUEL + z14-Nicolaus-h5-'Kind-von-ANNA-
  //      FILAK' + ANNA! → h34-1864/65/66!) + ★★★ KUNE-h10-nit ('Kure'-5.-branja!)
  //      + ★★★ ŽELKO-h1-nit + ★★★ KRIŽAN-h63-nit-2-LETI (Typhus-TRI-branja-1:1!)
  //      + ★★★ POŽEK-h67-nit-4-LETA (tail-1861-z54!) + PEZDIRC-z1-restart +
  //      z48-prazni-stolpci + z30-pokop-brez-smrti + otroška-umrljivost-33%-3/9.
  //      Dokaz: parish-death-1862-04106.json; skripte p215.
  {
  const p215Errors: string[] = [];
  const p215Death = HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && h.year === 1862);
  if (p215Death.length !== 9)
    p215Errors.push(`bloki 1862 (04106) ≠ 9 (${p215Death.length} — 9 Griblje-vpisov / 60 vpisov vrstno-štetje!)`);
  const p215Houses = p215Death.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
  if (p215Houses.join(",") !== "1,10,5,47,5,61,61,63,9")
    p215Errors.push(`hiše 1862 neujemane — najdeno: ${p215Houses.join(",")}`);
  if (HOUSE_VITALS.length !== 1590)
    p215Errors.push(`HOUSE_VITALS ≠ 1590 (${HOUSE_VITALS.length} — P214: 1581; P215: + 9 blokov 1862-04106 = 1590!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length !== 371)
    p215Errors.push(`bloki 04106 ≠ 371 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length} — P215: 9 × 1862 + P214: 7 × 1863 + P213: 17 × 1864 + P212: 13 × 1865 + P211: 13 × 1866 + P210: 20 × 1867 + P209: 13 × 1868 + P208: 14 × 1869 + P207: 12 × 1870 + P206: 11 × 1871 + P205: 17 × 1872 + P204: 38 × 1873 + P203: 21 × 1874 + P202: 10 × 1875 + P201: 20 × 1876 + P200: 8 × 1877 + P199: 23 × 1878 + P198: 9 × 1879 + P197: 13 × 1880 + P192: 16 × 1885 + P193: 21 × 1884 + P194: 11 × 1883 + P195: 16 × 1882 + P196: 19 × 1881 = 371!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && (h.year ?? 0) !== 1862 && (h.year ?? 0) !== 1863 && (h.year ?? 0) !== 1864 && (h.year ?? 0) !== 1865 && (h.year ?? 0) !== 1866 && (h.year ?? 0) !== 1867 && (h.year ?? 0) !== 1868 && (h.year ?? 0) !== 1869 && (h.year ?? 0) !== 1870 && (h.year ?? 0) !== 1871 && (h.year ?? 0) !== 1872 && (h.year ?? 0) !== 1873 && (h.year ?? 0) !== 1874 && (h.year ?? 0) !== 1875 && (h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)
    p215Errors.push("04106-bloki izven {1862, ..., 1885} (predzgodovina: 1857–1862 še nebrani!)");
  if (!p215Death.some((h) => h.houseNo === "5" && h.whatSi.includes("FILAK") && h.whatSi.includes("ANNA-FILAK")))
    p215Errors.push("★★★ FILAK-mreža-×3 (z11-h61-Katharina + z14-h5-'Kind-von-ANNA-FILAK' + ANNA!) ni označena");
  if (!p215Death.some((h) => h.houseNo === "10" && h.whatSi.includes("KUNE-h10-NIT") && h.whatSi.includes("Kure")))
    p215Errors.push("★★★ KUNE-h10-NIT-z10 (1862-'Simon-Kure' → 1863-'Joannes-Kune' — 'Kure'-5.-branja!) ni označena");
  if (!p215Death.some((h) => h.houseNo === "1" && h.whatSi.includes("ŽELKO-h1-NIT")))
    p215Errors.push("★★★ ŽELKO-h1-NIT-z41 (1862-Maria-½J → 1864-×2!) ni označena");
  if (!p215Death.some((h) => h.houseNo === "63" && h.whatSi.includes("KRIŽAN-h63-NIT") && h.whatSi.includes("Typhus")))
    p215Errors.push("★★★ KRIŽAN-h63-NIT-z43 (Typhus-TRI-branja-1:1!) ni označena");
  push(
    "qa-p215-parish-death-1862-04106",
    "P215: ŽUPNIJA PODZEMELJ — MRLIŠKA PREDZGODOVINA 04106, LETO 1862 = 24. LETO PREDZGODOVINSKE LINIJE (issue #18): okvir — s029–s035 == Pag. 24–30 (pag = sken−5; 2×-neodvisna-prenosa-md5-7/7 + s033–s035-carry-P214!) + **★★★ MEJA-1861/62 = s30 (tail-1861-z49–z54 + VSOTNA-'1|8|6|2'-'1862'-MARKER-3.-INSTANCE + restart-z1–z7! + NOVA-VARIANTA: BREZ-rokopisne-'1862'-glave — vsotna=EDINI-letnica-marker! + KROP-zap-stolpec: '1861'-glava-bledo + '49–54'-jasno — VLM-misread-'29–34'-KOREKCIJA-dokumentirana!)** + **★★★ MEJA-1862/63 = s35 (vsotna-'1|8|6|3'-'1863'-MARKER + '1863'-rokopisna-glava = 52.-POTRDITEV — P214!)** + **★★★ s32=s33-DOUBLE-SCAN-2.-v-knjigi** (cf.-s53/s54-P211! — 2×-NEODVISNA-VLM-branja-z24–z39: s32-fresh-ČISTEJŠA + s33-P214-obscured — duel-rešitve-z28/z29/z31/z38/z39!) + **★★★ FILAK-MREŽA-×3-1862** (z11-Katharina-Filak-h61-34J-F/T/K-DUEL-rešen-via-z14 + z14-Nicolaus-Filak-h5-10J-'...Kind-von-ANNA-FILAK'-opomba-garble-X-open + ANNA-FILAK-mati! → FILAK-h34-1864/65/66! + KATARINA-age-match-1862/1866-HIPEZOZA-X-open!) + **★★★ KUNE-h10-NIT** (z10-'Simon-Kure'-2J → 1863-z2-'Joannes-Kune' — 'Kure'-5.-branja-PODPORA-X-open-4-branja-duelu!) + **★★★ ŽELKO-h1-NIT-3.-LETO** (z41-Maria-Zeljko-½J-Zuckfall → 1864-z30/z35!) + **★★★ KRIŽAN-h63-NIT-2-LETI** (z43-Thomas-Potočar-28J-Typhus-TRI-branja-1:1! → 1864-z63!) + **★★★ POŽEK-h67-NIT-4-LETA** (tail-1861-z54-Mathias-2J-h67 → 1865-z36-Mathias-36J-ISTO-HIŠA — oče-sin-hipezoza-X-open!) + **z1-PEZDIRC-RESTART** (Andreas-36J-'¼-Güblerssohn'-Podzemelj-h10-'von-Griblje[?]-KROP' — PEZDIRC-mreža!) + **z48-ANOMALIJA-PRAZNI-STOLPCI** (starost-'—' + bolezen-'—' — Jerlicar[?]-h61-2.-instance!) + **z30-ANOMALIJA-POKOP-BREZ-SMRTI** ('Mrtvogrobnik[?]'-garble-X-open!) + **z17-bolezen-DUEL** ('Lungensucht'-vs-'Masern'-'ošpice!'-epidemija-hipoteza?) + **★★★ 60-VPIISOV-ŠTEVJE-IZ-VRSTIC-17.×** (ordinali-1–60-ČISTO — 9.-LETO-ZAPORED! vrstna-aritmetika 7+16+16+15+6!) + otroška-umrljivost-33%-3/9; **1862 = 60 vpisov (z1–z60) / 9 Griblje-vpisov / 7 hiš (h5+h61-×2!)**; **9 NOVIH BLOKOV parish.ts: vitals 1581 → 1590 · 04106 = 362 → 371 · 04894 = 520-NESPREMENJENO · p80 94-NESPREMENJENO · korpus-93→98-hiš-X-open**; skripte p215 (fetch-2×-md5-7/7 + read-×4 + krop-×27 + build-entries + build-proof) + qa-p215 (215. kontrola!) + dokaz parish-death-1862-04106.json (60 entries: 9-Griblje + 51-druge!) + pt-luknja-371/1590; **★★★ PREDZGODOVINA-LINIJA-24/29-LET!** (P216-LEAD: 1861 — s29-ŽE-VLM (z33–z48: 16-vrstic!) + s30-tail-z49–z54 → probe-s023–s029!)",
    "P215: THE PARISH OF PODZEMELJ — THE DEATH-REGISTER-PREHISTORY 04106, THE YEAR 1862 = THE 24th YEAR (issue #18): the-frame + **★★★ THE-1861/62-BOUNDARY = s30 (the-1861-TAIL + the-SUM-ROW-'1|8|6|2'-'1862'-MARKER-3rd-INSTANCE + the-restart! + NEW-VARIANT: NO-handwritten-'1862'-header — the-sum-row=the-ONLY-year-marker! + the-KROP-zap-column: the-'1861'-header + '49–54'-clear — the-VLM-misread-'29–34'-CORRECTION-documented!)** + **★★★ THE-1862/63-BOUNDARY = s35 (the-SUM-ROW-'1863'-MARKER + the-'1863'-handwritten-header = the-52nd-CONFIRMATION — P214!)** + **★★★ s32=s33-DOUBLE-SCAN-2nd-IN-THE-BOOK** (2×-INDEPENDENT-VLM-readings-z24–z39!) + **★★★ THE-FILAK-NETWORK-×3-1862** (z11-Katharina-h61 + z14-Nicolaus-h5-'Child-of-ANNA-FILAK' + ANNA! → h34-1864/65/66!) + **★★★ THE-KUNE-h10-THREAD** ('Kure'-the-5th-reading-SUPPORT!) + **★★★ THE-ŽELKO-h1-THREAD-3rd-YEAR** + **★★★ THE-KRIŽAN-h63-THREAD-2-YEARS** (Typhus-TRIPLE-reading-1:1!) + **★★★ THE-POŽEK-h67-THREAD-4-YEARS** (the-1861-tail-child → the-1865-adult-SAME-HOUSE!) + the-z1-PEZDIRC-restart + the-z48-EMPTY-COLUMNS-anomaly + the-z30-burial-without-death-anomaly + the-z17-disease-DUEL ('Masern'=measles-epidemic-hypothesis?) + child-mortality-33%-3/9; **1862 = 60 entries / 9 Griblje / 7 houses (h5+h61-×2!)**; **9 NEW BLOCKS: the vitals 1581 → 1590 · the 04106 = 362 → 371**; the scripts p215 + the qa-p215 (the 215th check!) + the evidence parish-death-1862-04106.json (60 entries!) + the pt-gap-371/1590; **★★★ THE-PREHISTORY-LINE-24/29-YEARS!** (the P216-LEAD: 1861 — the-s29-ALREADY-READ → the-probe-s023–s029!)",
    p215Errors.length === 0,
    p215Errors.length === 0
      ? `9 vpisov / 60 vrstic (števje-iz-vrstic-17.×! ordinali-1–60-ČISTO-9.-leto!) / 7 hiš (h5+h61-×2!) · MEJA-s30-tail-1861 + vsotna-'1862'-marker-3.-INSTANCE + restart-BREZ-rokopisne-glave-NOVA-VARIANTA + KROP-zap-DOKAZ-'49–54' · MEJA-s35-vsotna-'1863'-P214 · s32=s33-DOUBLE-SCAN-2.-v-knjigi · FILAK-MREŽA-×3 (Katharina-h61 + Nicolaus-h5-Kind-von-ANNA + ANNA!) · KUNE-h10-nit-'Kure'-5.-branja · ŽELKO-h1-nit · KRIŽAN-h63-nit-Typhus-TRI-branja-1:1 · POŽEK-h67-tail-1861-nit-4-LETA · PEZDIRC-z1-restart · z48-prazni-stolpci · z30-pokop-brez-smrti · otroška-33% · **PREDZGODOVINA-24/29!** · vitals 1590 · 04106 371 · 04894 520`
      : p215Errors.join("; "),
  );
  }

'''
src = src.replace(ANCHOR, BLOCK + ANCHOR, 1)
src = src.replace("HOUSE_VITALS.length !== 1581", "HOUSE_VITALS.length !== 1590")
src = src.replace('04106").length !== 362', '04106").length !== 371')
OLD_SET = "(h.year ?? 0) !== 1863 && (h.year ?? 0) !== 1864 && (h.year ?? 0) !== 1865 && (h.year ?? 0) !== 1866 && (h.year ?? 0) !== 1867 && (h.year ?? 0) !== 1868 && (h.year ?? 0) !== 1869 && (h.year ?? 0) !== 1870 && (h.year ?? 0) !== 1871 && (h.year ?? 0) !== 1872 && (h.year ?? 0) !== 1873 && (h.year ?? 0) !== 1874 && (h.year ?? 0) !== 1875 && (h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885"
src = src.replace(OLD_SET, "(h.year ?? 0) !== 1862 && " + OLD_SET)
src = src.replace("04106-bloki izven {1863, 1864, 1865, 1866, 1867, 1868, 1869, 1870, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1863 še nebrani!)",
                  "04106-bloki izven {1862, 1863, 1864, 1865, 1866, 1867, 1868, 1869, 1870, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1862 še nebrani!)")
src = src.replace("vitals 1581 · 04106 362 · 04894 520", "vitals 1590 · 04106 371 · 04894 520")
QA.write_text(src, encoding="utf-8")
print(f"qa-parish: {src.count('HOUSE_VITALS.length !== 1590')}")

files = sorted(set(glob.glob(str(ROOT / "scripts/**/*.py"), recursive=True) + glob.glob(str(ROOT / "scripts/**/*.mjs"), recursive=True)))
skip = ("p59_ps_blatt_headers", "p199_", "p200_", "p201_", "p202_", "p203_", "p204_", "p205_", "p206_", "p207_", "p208_", "p210_", "p211_", "p212_", "p213_", "p214_", "p215_")
patched = 0
for f in files:
    if any(s2 in f for s2 in skip): continue
    t = Path(f).read_text(encoding="utf-8")
    if "1581" not in t and "== 362" not in t: continue
    o = t
    t = t.replace("1581", "1590").replace('.get("04106") == 362', '.get("04106") == 371').replace("04106 == 362", "04106 == 371").replace("04106==362", "04106==371").replace("skupaj == 362", "skupaj == 371").replace('"04106") == 362', '"04106") == 371').replace("(04106, 362)", "(04106, 371)").replace("== 362,", "== 371,")
    if t != o:
        Path(f).write_text(t, encoding="utf-8"); patched += 1
print(f"skripte-patched: {patched}")

vpatched = 0
for f in sorted(ROOT.glob("scripts/p19*.py")) + sorted(ROOT.glob("scripts/p2[0-9][0-9]_parish*.py")):
    if "p215" in f.name: continue
    t = f.read_text(encoding="utf-8"); o = t
    for a, b in [("04106 == 362", "04106 == 371"), ("04106==362", "04106==371"),
                 ('04106": 362', '04106": 371'), ("skupaj == 362", "skupaj == 371"),
                 ('"04106") == 362', '"04106") == 371'), ("(04106, 362)", "(04106, 371)"),
                 ('byBook"]["04106"] == 362', 'byBook"]["04106"] == 371'),
                 ('["04106"] == 362', '["04106"] == 371'),
                 ("vitals == 1581", "vitals == 1590"), ("vitalsTotal == 1581", "vitalsTotal == 1590"),
                 ('vitalsTotal"] == 1581', 'vitalsTotal"] == 1590'),
                 ('"vitalsTotal": 1581', '"vitalsTotal": 1590'),
                 ('\\"vitalsTotal\\": 1581', '\\"vitalsTotal\\": 1590'),
                 ('!== 1581"', '!== 1590"'),
                 ("1581-številcev", "1590-številcev"),
                 ("vitals-števec-1581", "vitals-števec-1590"), ("vitals-1581", "vitals-1590")]:
        t = t.replace(a, b)
    t = re.sub(r'set\(izven\) == \{"1863"', 'set(izven) == {"1862", "1863"', t)
    t = t.replace('",".join(leta) == "1863,1864', '",".join(leta) == "1862,1863,1864')
    t = t.replace('join(leta) == "1863,1864,1865,1866,1867,1868,1869,1870,1871,1872,1873,1874,1875,1876,1877,1878,1879,1880,1881,1882,1883,1884,1885"',
                  'join(leta) == "1862,1863,1864,1865,1866,1867,1868,1869,1870,1871,1872,1873,1874,1875,1876,1877,1878,1879,1880,1881,1882,1883,1884,1885"')
    if t != o:
        f.write_text(t, encoding="utf-8"); vpatched += 1
print(f"verifierji-patched: {vpatched}")

ptp = ROOT / "research/issue17/pt-luknja-18-final.json"
pt = json.loads(ptp.read_text(encoding="utf-8"))
pt["corpus"]["vitalsTotal"] = 1590
pt["corpus"]["byBook"]["04106"] = 371
pt["corpus"]["housesNote"] = (pt["corpus"].get("housesNote") or "") + " | P215: +9-blokov-1862 (04106 362→371, vitals 1581→1590, ordinali-1–60-ČISTO-9.leto + MEJA-'1862'-3.-INSTANCE-vsotna-letnica-marker + NOVA-VARIANTA-brez-rokopisne-glave + s32=s33-DOUBLE-SCAN-2.× + FILAK-MREŽA-×3 + KUNE-h10-nit-'Kure'-5.-branja + ŽELKO-h1-nit + KRIŽAN-h63-nit-Typhus-TRI-branja + POŽEK-h67-tail-1861-nit + KROP-zap-stolpec-DOKAZ-'49–54'!)"
ptp.write_text(json.dumps(pt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"pt-luknja: {pt['corpus']['vitalsTotal']}/{pt['corpus']['byBook']['04106']}")
