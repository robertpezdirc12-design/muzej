#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P203 — INSERT qa-p203 blok + sanitizacija (1385→1406, 166→187, yearset +1874) +
verifier-patch (p190–p202) + pt-luknja + skripte-kaskada."""
from pathlib import Path
import glob, json, re

ROOT = Path("/home/z/my-project")

# ——— A: qa-p202 INSERT ———
QA = ROOT / "src/lib/qa-parish.ts"
src = QA.read_text(encoding="utf-8")
ANCHOR = "  // ——— qa-p202: MRLIŠKA PREDZGODOVINA 04106 — leto 1875 = 11. leto PREDZGODOVINSKE"
assert src.count(ANCHOR) == 1 and "qa-p203-parish-death-1874-04106" not in src
BLOCK = '''
  // ——— qa-p203: MRLIŠKA PREDZGODOVINA 04106 — leto 1874 = 12. leto PREDZGODOVINSKE
  //      LINIJE (issue #18). 1874 = 94 vpisov (z1–z94, ŠTEVJE-IZ-VRSTIC-5.×!) /
  //      21 Griblje / 18 hiš (h64-×2 + h69-×2 + h72-×2!) + ★★★ MEJA-1873/74-s119
  //      (TAIL-10-DEZ-1873-margine-201–212 + VELIKA-'18 74. Jänner'-glava!) +
  //      ★★★ VLM-FALSIFIKACIJE-×3-KROP-REŠENE (s125-'Jänner'-×13→SEPTEMBER +
  //      s122-'1877'→'1874' + 'Incipit'-halucinacija!) + 45.-46.-POTRDITVI +
  //      ★★★ LEKCIJA-#21-DOUBLE-SCAN (s123==s124 = pag-118-×2!) + KROP-POPRAVKI-
  //      hišnih-št.-×5 (h33/h57/h39/h19/h29!) + KOGEJ-'provisorium'-1874.
  //      Dokaz: parish-death-1874-04106.json; skripte p203.
  {
  const p203Errors: string[] = [];
  const p203Death = HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && h.year === 1874);
  if (p203Death.length !== 21)
    p203Errors.push(`bloki 1874 (04106) ≠ 21 (${p203Death.length} — 21 Griblje-vpisov / 94 vpisov vrstno-štetje!)`);
  const p203Houses = p203Death.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
  if (p203Houses.join(",") !== "11,19,21,24,28,29,33,36,38,39,48,55,57,6,64,64,69,69,72,72,86")
    p203Errors.push(`hiše 1874 neujemane — najdeno: ${p203Houses.join(",")}`);
  if (HOUSE_VITALS.length !== 1406)
    p203Errors.push(`HOUSE_VITALS ≠ 1406 (${HOUSE_VITALS.length} — P202: 1385; P203: + 21 blokov 1874-04106 = 1406!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length !== 187)
    p203Errors.push(`bloki 04106 ≠ 187 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length} — P203: 21 × 1874 + P202: 10 × 1875 + P201: 20 × 1876 + P200: 8 × 1877 + P199: 23 × 1878 + P198: 9 × 1879 + P197: 13 × 1880 + P192: 16 × 1885 + P193: 21 × 1884 + P194: 11 × 1883 + P195: 16 × 1882 + P196: 19 × 1881 = 187!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && (h.year ?? 0) !== 1874 && (h.year ?? 0) !== 1875 && (h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)
    p203Errors.push("04106-bloki izven {1874, ..., 1885} (predzgodovina: 1857–1873 še nebrani!)");
  if (!p203Death.some((h) => h.houseNo === "33" && h.whatSi.includes("h83-VLM-POPRAVEK→h33")))
    p203Errors.push("★★★ KRIŽAN-h33-POPRAVEK (KROP-'33.'-ne-h83 + KOGEJ-'provisorium'-podpis!) ni označena");
  if (!p203Death.some((h) => h.houseNo === "57" && h.whatSi.includes("P200-NIT-RAZŠIRJENA-NAZAJ")))
    p203Errors.push("★★★ LOGAR-h57-POPRAVEK (ne-h8 + P200-h57-NIT-1874→1877 + modra-tinta-'12'!) ni označena");
  if (!p203Death.some((h) => h.houseNo === "39" && h.whatSi.includes("s123==s124-DVOSCAN")))
    p203Errors.push("★★★ TILAK-h39-POPRAVEK (ne-h34 + s123==s124-DOUBLE-SCAN-KROP-×2!) ni označena");
  if (!p203Death.some((h) => h.houseNo === "72" && h.whatSi.includes("MRTVOROJEN")))
    p203Errors.push("★★★ h72-MRTVOROJEN-z39 (oče-[?]Krajnc-vs-Janec-NESOGLASJE!) ni označena");
  if (!p203Death.some((h) => h.houseNo === "24" && h.whatSi.includes("BRIME-1/2-×2-v-5-TEDNIH")))
    p203Errors.push("★★★ BRIME-×2-v-5-tednih (z6-h24-9J + z13-h28-62J!) ni označena");
  if (!p203Death.some((h) => h.houseNo === "11" && h.whatSi.includes("h11-KUNIĆ-hiša-NIT")))
    p203Errors.push("★★★ LUNIČ-h11-KUNIĆ-NIT (z2-16dni → 1875-z71-KUNIĆ!) ni označena");
  push(
    "qa-p203-parish-death-1874-04106",
    "P203: ŽUPNIJA PODZEMELJ — MRLIŠKA PREDZGODOVINA 04106, LETO 1874 = 12. LETO PREDZGODOVINSKE LINIJE (issue #18): okvir — s119-glava–s127-z10 == Pag. 114–121 (md5-križna-veriga-P197→…→P203-7.×: s127+s126-sveža == P202-disk-1:1!) + **★★★ LEKCIJA-#21: NATISNJENE-ŠT.-STRANI-PREVERJENE-×7 (s118=113, s121=116, s122=117 → sken−5; s123/124=118-DUPLIKAT!, s125=119, s126=120, s127=121 → sken−6!) + ★★★ DOUBLE-SCAN-2.×: s123==s124 = pag-118-×2 (natisnjena-'118'-na-obeh + hamming-15/256 + KROP-r1/r2-'Tilak'/'Gradec-75'-1:1!)** + **★★★ MEJA-1873/74 = s119 (TAIL-10-DEZ-1873-margine-201–212! 3-Griblje! + VELIKA-'18 74. Jänner'-GLAVA-split — NO-'Incipit-annus-Domini'-VLM-halucinacija-FALSIFICIRANA!)** + **★★★ VLM-FALSIFIKACIJE-×3-KROP-REŠENE: s125-'Jänner'-×13→SEPTEMBER ('9.'-numerični-mesec! nov-format-1874!) + s122-'1877'→'1874.'-glif-za-glifom ('4'-z-zanko!) + 'Incipit'-halucinacija!** + **★★★ 45.-in-46.-POTRDITEV-invariante (s122-z1-'1874.'-Mai-celica + s125-z1-'1874.'-September-celica!)** + **★★★ 94-VPIISOV-ŠTEVJE-IZ-VRSTIC-5.×** (ordinali-ZMEDANI-[?]! vrstna-aritmetika 3+11+16+15+14+13+12+10 + meseci J4+F5+M4+A10+M19-MAX+J11+J5+A1-MIN+S17+O3+N11+D4 = 94!) + **★★★ KROP-POPRAVKI-hišnih-št.-×5 (KRIŽAN-h33-ne-h83! + LOGAR-h57-ne-h8 + P200-NIT! + TILAK-h39-ne-h34! + KRIČ-h19 + MILER-h29 — P202-tail-None→POPRAVLJENO!)** + **★★★ KOGEJ-'provisorium'-PODPIS-1874 (z69-'p.-undenard-Kogej' — KOGEJ-NIT-4.-LETO-1874→1875→1876→1877!)** + DOVGAN-nit-×6 + BRIME-×2-v-5-TEDNIH (z6-h24-9J + z13-h28-62J — 2-MARIJE-2-HIŠI!) + MRTVOROJEN-z39-h72 (oče-NESOGLASJE-Krajnc-vs-Janec-[?]!) + BRUNE-z51-starost-NESOGLASJE (KROP-69-vs-VLM-56¾-[?]!) + h11-LUNIČ-16-DNI (KUNIĆ-hiša-1-leto-pred-KUNIĆ-1875!) + h6/h57-NITI-RAZŠIRJENE-NAZAJ (→1877!) + h72-×2-v-4-mesecih + h64-×2 + h69-×2 + Sabler-priimek-PREČRTAN-KORIGIRAN + MODRA-TINTA-'12'-annotacija-z81 + ULEDBA-×2 (1873-Brumc-31-Dec→1-Jan + 1874-Plam→P202-z1!) + otroška-umrljivost-33%-7/21-jasna; **1874 = 94 vpisov (z1–z94) / 21 Griblje-vpisov / 18 hiš**; **21 NOVIH BLOKOV parish.ts: vitals 1385 → 1406 · 04106 = 166 → 187 · 04894 = 520-NESPREMENJENO · p80 94-NESPREMENJENO · korpus 93-NESPREMENJEN**; skripte p203 (fetch-md5 + read + crop + build-entries + build-proof) + qa-p203 (203. kontrola!) + dokaz parish-death-1874-04106.json (94 entries: 21-Griblje + 73-druge! 14-anomalij + 10-crossChecks + honesty-16 + tail_1873-×10 + leadP204-1873!) + pt-luknja-REGENERACIJA (187/1406!); **★★★ PREDZGODOVINA-LINIJA-12/29-LET!** (P204-LEAD: 1873 — s119-TAIL-×10-DEZ-1873-ŽE-PREBRAN (3-Griblje: h23-Brinec + h2-Hlebec + h26-Brumc!) + s118-ŽE-FETCHAN+VLM → probe-s110–s119!)",
    "P203: THE PARISH OF PODZEMELJ — THE DEATH-REGISTER-PREHISTORY 04106, THE YEAR 1874 = THE 12th YEAR (issue #18): the-frame + **★★★ LESSON-#21: the-PRINTED-PAGE-NUMBERS-VERIFIED-×7 + ★★★ the-DOUBLE-SCAN-2.×: s123==s124 = page-118-×2!** + **★★★ the-1873/74-BOUNDARY = s119 (the-TAIL-10-DEZ-1873-margins-201–212! + the-BIG-'18 74. Jänner'-SPLIT-HEAD — NO-'Incipit-annus-Domini'-VLM-hallucination-FALSIFIED!)** + **★★★ VLM-FALSIFICATIONS-×3-KROP-RESOLVED (s125-'Jänner'-×13→SEPTEMBER-the-'9.'-numeric-month! + s122-'1877'→'1874.' + the-hallucination!)** + **★★★ the-45th-and-46th-INVARIANT-CONFIRMATIONS** + **★★★ THE-94-ENTRIES-COUNT-FROM-ROWS-5.×** + **★★★ KROP-CORRECTIONS-of-house-numbers-×5** + **★★★ the-KOGEJ-'provisorium'-SIGNATURE-1874 (the-THREAD-4th-YEAR!)** + the-DOVGAN-thread + BRIME-×2-IN-5-WEEKS + the-STILLBORN-z39 + the-BRUNE-age-DISAGREEMENT + the-h11-LUNIČ-thread + the-h6/h57-threads-EXTENDED-BACK + the-blue-ink-annotation + the-ULEDBA-×2 + the-child-mortality-33%; **1874 = 94 entries / 21 Griblje / 18 houses**; **21 NEW BLOCKS: the vitals 1385 → 1406 · the 04106 = 166 → 187**; the scripts p203 + the qa-p203 (the 203rd check!) + the evidence parish-death-1874-04106.json (94 entries!) + the pt-gap-REGENERATION (187/1406!); **★★★ THE-PREHISTORY-LINE-12/29-YEARS!** (the P204-LEAD: 1873 — the-s119-TAIL-×10-ALREADY-READ (3-Griblje!) + the-s118-ALREADY-FETCHED+VLM → the-probe-s110–s119!)",
    p203Errors.length === 0,
    p203Errors.length === 0
      ? `21 vpisov / 94 vrstic (števje-iz-vrstic-5.×!) / 18 hiš (×2-×3!) · LEKCIJA-#21-natisnjene-št.-strani-×7 + s123==s124-DVOSCAN · MEJA-s119-'18 74. Jänner'-VELIKA-glava + TAIL-10-margine-201–212 · VLM-FALSIFIKACIJE-×3-KROP-REŠENE · 45.-46.-POTRDITVI-celici · KROP-POPRAVKI-hišnih-št.-×5 · KOGEJ-'provisorium'-1874 · BRIME-×2 · MRTVOROJEN-h72 · otroška-umrljivost-33% · **PREDZGODOVINA-12/29!** · vitals 1406 · 04106 187 · 04894 520`
      : p203Errors.join("; "),
  );
  }

'''
src = src.replace(ANCHOR, BLOCK + ANCHOR, 1)

# ——— B: SANITIZACIJA 1385→1406 + 166→187 + yearset +1874 ———
src = src.replace("HOUSE_VITALS.length !== 1385", "HOUSE_VITALS.length !== 1406")
src = src.replace('04106").length !== 166', '04106").length !== 187')
src = src.replace("+ P202: 10 × 1875 = 166!)", "+ P202: 10 × 1875 + P203: 21 × 1874 = 187!)")
OLD_SET = "(h.year ?? 0) !== 1875 && (h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885"
src = src.replace(OLD_SET, "(h.year ?? 0) !== 1874 && " + OLD_SET)
src = src.replace("04106-bloki izven {1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1874 še nebrani!)",
                  "04106-bloki izven {1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1873 še nebrani!)")
src = src.replace("vitals 1385 · 04106 166 · 04894 520", "vitals 1406 · 04106 187 · 04894 520")
QA.write_text(src, encoding="utf-8")
print(f"qa-parish: total-{src.count('HOUSE_VITALS.length !== 1406')} | 04106-{src.count('04106\").length !== 187')}")

# ——— C: skripte-kaskada (skip p59/p199–p203) ———
files = sorted(set(glob.glob(str(ROOT / "scripts/**/*.py"), recursive=True) + glob.glob(str(ROOT / "scripts/**/*.mjs"), recursive=True)))
skip = ("p59_ps_blatt_headers", "p199_", "p200_", "p201_", "p202_", "p203_")
patched = 0
for f in files:
    if any(s in f for s in skip):
        continue
    t = Path(f).read_text(encoding="utf-8")
    if "1385" not in t and "== 166" not in t:
        continue
    o = t
    t = t.replace("1385", "1406").replace(".get(\"04106\") == 166", ".get(\"04106\") == 187").replace("04106 == 166", "04106 == 187").replace("04106==166", "04106==187").replace("skupaj == 166", "skupaj == 187").replace("\"04106\") == 166", "\"04106\") == 187").replace("(04106, 166)", "(04106, 187)").replace("== 166,", "== 187,")
    if t != o:
        Path(f).write_text(t, encoding="utf-8")
        patched += 1
print(f"skripte-patched: {patched}")

# ——— D: verifier-patch p190–p202 ———
vpatched = 0
for f in sorted(ROOT.glob("scripts/p19*.py")) + sorted(ROOT.glob("scripts/p20[012]_parish*.py")):
    t = f.read_text(encoding="utf-8")
    o = t
    t = t.replace("04106 == 166", "04106 == 187").replace("04106==166", "04106==187").replace("04106\": 166", "04106\": 187").replace("skupaj == 166", "skupaj == 187").replace('"04106") == 166', '"04106") == 187').replace("(04106, 166)", "(04106, 187)").replace("byBook\"][\"04106\"] == 166", "byBook\"][\"04106\"] == 187")
    t = t.replace("vitals == 1385", "vitals == 1406").replace("vitalsTotal == 1385", "vitalsTotal == 1406").replace('vitalsTotal"] == 1385', 'vitalsTotal"] == 1406').replace("!== 1385\"", "!== 1406\"").replace("1385-številcev", "1406-številcev").replace("vitals-števec-1385", "vitals-števec-1406").replace("vitals-1385", "vitals-1406")
    t = re.sub(r'set\(izven\) == \{"1875"', 'set(izven) == {"1874", "1875"', t)
    t = t.replace('",".join(leta) == "1875,1876', '",".join(leta) == "1874,1875,1876')
    t = t.replace('join(leta) == "1875,1876,1877,1878,1879,1880,1881,1882,1883,1884,1885"',
                  'join(leta) == "1874,1875,1876,1877,1878,1879,1880,1881,1882,1883,1884,1885"')
    if t != o:
        f.write_text(t, encoding="utf-8")
        vpatched += 1
print(f"verifierji-patched: {vpatched}")

# ——— E: pt-luknja ———
ptp = ROOT / "research/issue17/pt-luknja-18-final.json"
pt = json.loads(ptp.read_text(encoding="utf-8"))
pt["corpus"]["vitalsTotal"] = 1406
pt["corpus"]["byBook"]["04106"] = 187
pt["corpus"]["housesNote"] = (pt["corpus"].get("housesNote") or "") + " | P203: +21-blokov-1874 (04106 166→187, vitals 1385→1406, LEKCIJA-#21-dvostavni-sken-s123==s124!)"
ptp.write_text(json.dumps(pt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"pt-luknja: {pt['corpus']['vitalsTotal']}/{pt['corpus']['byBook']['04106']}")
