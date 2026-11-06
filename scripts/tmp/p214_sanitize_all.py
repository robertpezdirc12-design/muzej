#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P214 — INSERT qa-p214 + sanitizacija (1574→1581, 355→362, yearset +1863) + verifier-patch + pt-luknja."""
from pathlib import Path
import glob, json, re

ROOT = Path("/home/z/my-project/muzej-backup")
QA = ROOT / "src/lib/qa-parish.ts"
src = QA.read_text(encoding="utf-8")
ANCHOR = "  // ——— qa-p213: MRLIŠKA PREDZGODOVINA 04106 — leto 1864 = 22. leto PREDZGODOVINSKE"
assert src.count(ANCHOR) == 1 and "qa-p214-parish-death-1863-04106" not in src
BLOCK = '''
  // ——— qa-p214: MRLIŠKA PREDZGODOVINA 04106 — leto 1863 = 23. leto PREDZGODOVINSKE
  //      LINIJE (issue #18). 1863 = 64 vpisov (ordinali-1–64 ČISTO — 8.-leto-
  //      zapored!) / 7 Griblje (NAJMANJ-v-predzgodovini!) / 7 hiš + ★★★ MEJA-
  //      1862/63-s35 (tail-1862 + VSOTNA-'1|8|6|3'-'1863'-MARKER + restart +
  //      '1863'-rokopisna-glava = 52.-POTRDITEV!) + ★★★ MEJA-1863/64-s39-tail
  //      (z64-ULEDBA-#11-12.×-EKSPLICITNI-LETNICI-'31.Dec.1863'-'2.Jän.1864'! +
  //      VSOTNA-'1|8|6|4'-'1864'-MARKER!) + ★★★ NOV-INVARIANTA-TIP: VSOTNA-
  //      VRSTA = LETNICA-MARKER-naslednjega-leta! + ★★★ 7-KROP-VIZUALNIH-
  //      ADJUDIKACIJSKIH-SKUPIN (z2-Kune-4-branja-X-open + z12-h65-BRINC-
  //      'unehelich'-opomba! + z18-h32/65J + z26-h18-ŠIMEC-nit-ČEZ-LETA +
  //      z27-h11[~71!]-STRAUS-mreža-γ-7 + z33-h53 + z38-Rosalia-infans-4-branja!)
  //      + z53-'außereheliches-Kind-von'-FORMULA-DOKAZ-P213-z6! + FILAK-Grem-h33-×2
  //      + otroška-umrljivost-29%-2/7 (NAJNIŽJA!)! Dokaz: parish-death-1863-
  //      04106.json; skripte p214.
  {
  const p214Errors: string[] = [];
  const p214Death = HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && h.year === 1863);
  if (p214Death.length !== 7)
    p214Errors.push(`bloki 1863 (04106) ≠ 7 (${p214Death.length} — 7 Griblje-vpisov / 64 vpisov vrstno-štetje!)`);
  const p214Houses = p214Death.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
  if (p214Houses.join(",") !== "10,11,18,21,32,53,65")
    p214Errors.push(`hiše 1863 neujemane — najdeno: ${p214Houses.join(",")}`);
  if (HOUSE_VITALS.length !== 1581)
    p214Errors.push(`HOUSE_VITALS ≠ 1581 (${HOUSE_VITALS.length} — P213: 1574; P214: + 7 blokov 1863-04106 = 1581!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length !== 362)
    p214Errors.push(`bloki 04106 ≠ 362 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length} — P214: 7 × 1863 + P213: 17 × 1864 + P212: 13 × 1865 + P211: 13 × 1866 + P210: 20 × 1867 + P209: 13 × 1868 + P208: 14 × 1869 + P207: 12 × 1870 + P206: 11 × 1871 + P205: 17 × 1872 + P204: 38 × 1873 + P203: 21 × 1874 + P202: 10 × 1875 + P201: 20 × 1876 + P200: 8 × 1877 + P199: 23 × 1878 + P198: 9 × 1879 + P197: 13 × 1880 + P192: 16 × 1885 + P193: 21 × 1884 + P194: 11 × 1883 + P195: 16 × 1882 + P196: 19 × 1881 = 362!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && (h.year ?? 0) !== 1863 && (h.year ?? 0) !== 1864 && (h.year ?? 0) !== 1865 && (h.year ?? 0) !== 1866 && (h.year ?? 0) !== 1867 && (h.year ?? 0) !== 1868 && (h.year ?? 0) !== 1869 && (h.year ?? 0) !== 1870 && (h.year ?? 0) !== 1871 && (h.year ?? 0) !== 1872 && (h.year ?? 0) !== 1873 && (h.year ?? 0) !== 1874 && (h.year ?? 0) !== 1875 && (h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)
    p214Errors.push("04106-bloki izven {1863, ..., 1885} (predzgodovina: 1857–1863 še nebrani!)");
  if (!p214Death.some((h) => h.houseNo === "65" && h.whatSi.includes("BRINC-h65-NOVA-HIŠA") && h.whatSi.includes("unehelich")))
    p214Errors.push("★★★ BRINC-h65-NOVA-HIŠA + 'unehelich'-opomba-z12 (KROP-×3!) ni označena");
  if (!p214Death.some((h) => h.houseNo === "18" && h.whatSi.includes("ŠIMEC-h18-NIT-ČEZ-LETA")))
    p214Errors.push("★★★ ŠIMEC-h18-NIT-ČEZ-LETA-z26 (1863-Georg → 1864-Peter-ISTO-HIŠA!) ni označena");
  if (!p214Death.some((h) => h.houseNo === "11" && h.whatSi.includes("STRAUS-mreža-X-open") && h.whatSi.includes("γ-7")))
    p214Errors.push("★★★ STRAUS-mreža-X-open-z27 (h11-vs-71-γ-7-DUEL + 1864-z44-korelacija!) ni označena");
  if (!p214Death.some((h) => h.houseNo === "10" && h.whatSi.includes("Kune") && h.whatSi.includes("X-open")))
    p214Errors.push("★★★ Kune-X-open-z2 (4-branja-duel + Gehirnentzündung-POTRJENA!) ni označena");
  push(
    "qa-p214-parish-death-1863-04106",
    "P214: ŽUPNIJA PODZEMELJ — MRLIŠKA PREDZGODOVINA 04106, LETO 1863 = 23. LETO PREDZGODOVINSKE LINIJE (issue #18): okvir — s033–s039 == Pag. 28–34 (pag = sken−5; 2×-neodvisna-prenosa-md5-7/7 + s39-carry-P213!) + **★★★ MEJA-1862/63 = s35 (tail-1862-z55–z60 + VSOTNA-'1|8|6|3'-'1863'-MARKER + restart-z1–z8! + '1863'-rokopisna-glava-s35 = 52.-POTRDITEV-invariante — arb_s35_glava-KROP!)** + **★★★ MEJA-1863/64 = s39-tail (z64-ULEDBA-#11-12.-INSTANCE-EKSPLICITNO: smrt-'31.-Dec-1863' + pokop-'2.-Jänner-1864' — OBE-LETNICI-V-VPISU @6×-KROP! + VSOTNA-'1|8|6|4'-'1864'-MARKER!)** + **★★★ NOV-INVARIANTA-TIP: VSOTNA-VRSTA = LETNICA-MARKER-naslednjega-leta** (cifre-razpete-čez-stolpce: s35-'1|8|6|3' + s39-'1|8|6|4' — KROP-s39_vsota_desno-Alter-'6'+Priester-'4'-1:1!) + **★★★ 7-KROP-VIZUALNIH-ADJUDIKACIJSKIH-SKUPIN** (z2-'Kune'-4-branja-X-open + bolezen-'Gehirnentzündung'-POTRJENA + z12-h65-'65'-KROP+VIZUALNO-duel-'68'-FALSIFICIRAN + bolezen-'Lungenentzündung+Magenkrampf' + opomba-'unehelich'-1.-V-KORPUSU! + z18-h32-TRIJSKOTRJENA/65J + z26-h18-2×/53J/'¼-Güblerssohn' + z27-h11-ALTERNATIVA-'71'-γ-7 + ime-'Straus'-TRI-branja + z33-h53-2×/13.|15. + z38-'Rosalia-infans'-4-branja/'Dreinsucht'!) + **★★★ ŠIMEC-h18-NIT-ČEZ-LETA** (1863-z26-Georg-Simic-h18 → 1864-z34-Peter-ŠIMIC-h18-ISTO-HIŠO!) + **★★★ BRINC-h65-NOVA-HIŠA** (3.-BRINC-hiša!) + **★★★ STRAUS-h71-korelacija** (1863-'Joannes-Straus'-h11[~71!] → 1864-'Anna-Strauž'-h71-γ-7 — isti-γ-glyph-2-LETI!) + **★★★ FILAK-Grem-h33-×2-v-3-TEDNIH** (z54-novorojenček + z59-Maria-5-J!) + **z53-'außereheliches-Kind-von'-FORMULA-DOKAZ-P213-z6-garble!** + **★★★ 64-VPIISOV-ŠTEVJE-IZ-VRSTIC-16.×** (ordinali-1–64-ČISTO — 8.-LETO-ZAPORED! vrstna-aritmetika 8+15+15+16+10!) + otroška-umrljivost-29%-2/7 (NAJNIŽJA-v-predzgodovini!); **1863 = 64 vpisov (z1–z64) / 7 Griblje-vpisov (NAJMANJ!) / 7 hiš**; **7 NOVIH BLOKOV parish.ts: vitals 1574 → 1581 · 04106 = 355 → 362 · 04894 = 520-NESPREMENJENO · p80 94-NESPREMENJENO · korpus 93-NESPREMENJEN**; skripte p214 (fetch-2×-md5-7/7 + read-×6 + krop-×38 + build-entries + build-proof) + qa-p214 (214. kontrola!) + dokaz parish-death-1863-04106.json (64 entries: 7-Griblje + 57-druge!) + pt-luknja-362/1581; **★★★ PREDZGODOVINA-LINIJA-23/29-LET!** (P215-LEAD: 1862 — s33/s34-ŽE-VLM (z24–z54: 31-vrstic!) + s35-tail-z55–z60 → probe-s029–s033!)",
    "P214: THE PARISH OF PODZEMELJ — THE DEATH-REGISTER-PREHISTORY 04106, THE YEAR 1863 = THE 23rd YEAR (issue #18): the-frame + **★★★ THE-1862/63-BOUNDARY = s35 (the-1862-TAIL + the-SUM-ROW-'1|8|6|3'-'1863'-MARKER + the-restart + the-'1863'-handwritten-header = the-52nd-CONFIRMATION!)** + **★★★ THE-1863/64-BOUNDARY = s39-tail (z64-ULEDBA-#11-12th-INSTANCE-EXPLICIT: death-'31.-Dec-1863' + burial-'2.-January-1864' — BOTH-YEARS-WRITTEN-IN-THE-ENTRY @6×-KROP! + the-SUM-ROW-'1|8|6|4'-'1864'-MARKER!)** + **★★★ NEW-INVARIANT-TYPE: the-SUM-ROW = the-YEAR-MARKER-of-the-following-year** (digits-spread-across-columns!) + **★★★ 7-KROP-VISUAL-ADJUDICATION-GROUPS** (z2-'Kune'-4-readings-X-open + z12-h65-BRINC-'unehelich'-annotation! + z18-h32/65J + z26-h18-ŠIMEC-thread-ACROSS-YEARS + z27-h11[~71!]-STRAUS-network-γ-7 + z33-h53 + z38-'Rosalia-infans'-4-readings!) + **★★★ ŠIMEC-h18-THREAD-ACROSS-YEARS** + **★★★ BRINC-h65-NEW-HOUSE** + **★★★ STRAUS-h71-γ-7-CORRELATION-2-YEARS** + **★★★ FILAK-Grem-h33-×2-in-3-WEEKS** + the-z53-'außereheliches-Kind-von'-FORMULA-EVIDENCE-for-P213-z6! + child-mortality-29%-2/7 (THE-LOWEST!); **1863 = 64 entries / 7 Griblje (THE-FEWEST!) / 7 houses**; **7 NEW BLOCKS: the vitals 1574 → 1581 · the 04106 = 355 → 362**; the scripts p214 + the qa-p214 (the 214th check!) + the evidence parish-death-1863-04106.json (64 entries!) + the pt-gap-362/1581; **★★★ THE-PREHISTORY-LINE-23/29-YEARS!** (the P215-LEAD: 1862 — the-s33/s34-ALREADY-READ → the-probe-s029–s033!)",
    p214Errors.length === 0,
    p214Errors.length === 0
      ? `7 vpisov / 64 vrstic (števje-iz-vrstic-16.×! ordinali-1–64-ČISTO-8.-leto!) / 7 hiš (NAJMANJ-v-predzgodovini!) · MEJA-s35-tail-1862 + vsotna-'1863'-marker + restart + '1863'-glava-52.-POTRDITEV · MEJA-s39-tail-ULEDBA-#11-12.×-EKSPLICITNO ('31.Dec.1863'-'2.Jän.1864'!) + vsotna-'1864'-marker · NOV-INVARIANTA-TIP-LETNICA-MARKER · 7-KROP-SKUPIN (Kune + BRINC-unehelich-h65 + ULRICH-h32 + ŠIMEC-h18-nit + STRAUS-h11[~71!]-γ-7 + SIMIC-h53 + Rosalia-infans-h21!) · ŠIMEC-h18-ČEZ-LETA · STRAUS-h71-korelacija · FILAK-Grem-h33-×2 · z53-FORMULA-DOKAZ · otroška-29% (NAJNIŽJA!) · **PREDZGODOVINA-23/29!** · vitals 1581 · 04106 362 · 04894 520`
      : p214Errors.join("; "),
  );
  }

'''
src = src.replace(ANCHOR, BLOCK + ANCHOR, 1)
src = src.replace("HOUSE_VITALS.length !== 1574", "HOUSE_VITALS.length !== 1581")
src = src.replace('04106").length !== 355', '04106").length !== 362')
OLD_SET = "(h.year ?? 0) !== 1864 && (h.year ?? 0) !== 1865 && (h.year ?? 0) !== 1866 && (h.year ?? 0) !== 1867 && (h.year ?? 0) !== 1868 && (h.year ?? 0) !== 1869 && (h.year ?? 0) !== 1870 && (h.year ?? 0) !== 1871 && (h.year ?? 0) !== 1872 && (h.year ?? 0) !== 1873 && (h.year ?? 0) !== 1874 && (h.year ?? 0) !== 1875 && (h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885"
src = src.replace(OLD_SET, "(h.year ?? 0) !== 1863 && " + OLD_SET)
src = src.replace("04106-bloki izven {1864, 1865, 1866, 1867, 1868, 1869, 1870, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1864 še nebrani!)",
                  "04106-bloki izven {1863, 1864, 1865, 1866, 1867, 1868, 1869, 1870, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1863 še nebrani!)")
src = src.replace("vitals 1574 · 04106 355 · 04894 520", "vitals 1581 · 04106 362 · 04894 520")
QA.write_text(src, encoding="utf-8")
print(f"qa-parish: {src.count('HOUSE_VITALS.length !== 1581')}")

files = sorted(set(glob.glob(str(ROOT / "scripts/**/*.py"), recursive=True) + glob.glob(str(ROOT / "scripts/**/*.mjs"), recursive=True)))
skip = ("p59_ps_blatt_headers", "p199_", "p200_", "p201_", "p202_", "p203_", "p204_", "p205_", "p206_", "p207_", "p208_", "p210_", "p211_", "p212_", "p213_", "p214_")
patched = 0
for f in files:
    if any(s2 in f for s2 in skip): continue
    t = Path(f).read_text(encoding="utf-8")
    if "1574" not in t and "== 355" not in t: continue
    o = t
    t = t.replace("1574", "1581").replace('.get("04106") == 355', '.get("04106") == 362').replace("04106 == 355", "04106 == 362").replace("04106==355", "04106==362").replace("skupaj == 355", "skupaj == 362").replace('"04106") == 355', '"04106") == 362').replace("(04106, 355)", "(04106, 362)").replace("== 355,", "== 362,")
    if t != o:
        Path(f).write_text(t, encoding="utf-8"); patched += 1
print(f"skripte-patched: {patched}")

vpatched = 0
for f in sorted(ROOT.glob("scripts/p19*.py")) + sorted(ROOT.glob("scripts/p2[0-9][0-9]_parish*.py")):
    if "p214" in f.name: continue
    t = f.read_text(encoding="utf-8"); o = t
    for a, b in [("04106 == 355", "04106 == 362"), ("04106==355", "04106==362"),
                 ('04106": 355', '04106": 362'), ("skupaj == 355", "skupaj == 362"),
                 ('"04106") == 355', '"04106") == 362'), ("(04106, 355)", "(04106, 362)"),
                 ('byBook"]["04106"] == 355', 'byBook"]["04106"] == 362'),
                 ('["04106"] == 355', '["04106"] == 362'),
                 ("vitals == 1574", "vitals == 1581"), ("vitalsTotal == 1574", "vitalsTotal == 1581"),
                 ('vitalsTotal"] == 1574', 'vitalsTotal"] == 1581'),
                 ('"vitalsTotal": 1574', '"vitalsTotal": 1581'),
                 ('\\"vitalsTotal\\": 1574', '\\"vitalsTotal\\": 1581'),
                 ('!== 1574"', '!== 1581"'),
                 ("1574-številcev", "1581-številcev"),
                 ("vitals-števec-1574", "vitals-števec-1581"), ("vitals-1574", "vitals-1581")]:
        t = t.replace(a, b)
    t = re.sub(r'set\(izven\) == \{"1864"', 'set(izven) == {"1863", "1864"', t)
    t = t.replace('",".join(leta) == "1864,1865', '",".join(leta) == "1863,1864,1865')
    t = t.replace('join(leta) == "1864,1865,1866,1867,1868,1869,1870,1871,1872,1873,1874,1875,1876,1877,1878,1879,1880,1881,1882,1883,1884,1885"',
                  'join(leta) == "1863,1864,1865,1866,1867,1868,1869,1870,1871,1872,1873,1874,1875,1876,1877,1878,1879,1880,1881,1882,1883,1884,1885"')
    if t != o:
        f.write_text(t, encoding="utf-8"); vpatched += 1
print(f"verifierji-patched: {vpatched}")

ptp = ROOT / "research/issue17/pt-luknja-18-final.json"
pt = json.loads(ptp.read_text(encoding="utf-8"))
pt["corpus"]["vitalsTotal"] = 1581
pt["corpus"]["byBook"]["04106"] = 362
pt["corpus"]["housesNote"] = (pt["corpus"].get("housesNote") or "") + " | P214: +7-blokov-1863 (04106 355→362, vitals 1574→1581, ordinali-1–64-ČISTO-8.leto + MEJA-'1863'-52.-POTRDITEV + NOV-INVARIANTA-TIP-vsotna=LETNICA-MARKER + ULEDBA-#11-12.×-EKSPLICITNO + 7-KROP-SKUPIN + ŠIMEC-h18-ČEZ-LETA + BRINC-h65-unehelich + STRAUS-h71-γ-7-korelacija!)"
ptp.write_text(json.dumps(pt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"pt-luknja: {pt['corpus']['vitalsTotal']}/{pt['corpus']['byBook']['04106']}")
