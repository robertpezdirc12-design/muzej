#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P222 — INSERT qa-p222 + sanitizacija (1677→1839, 04104=25→46, yearset-04104-{1884,1885}, pt-luknja)."""
from pathlib import Path
import glob, json, re

ROOT = Path("/home/z/my-project")
QA = ROOT / "src/lib/qa-parish.ts"
src = QA.read_text(encoding="utf-8")
ANCHOR = "  // ——— qa-p221: KRSTNA PREDZGODOVINA 04104 — leto 1885 = 1/15 — NOVA LINIJA"
assert src.count(ANCHOR) == 1 and "qa-p222-parish-baptism-1884-04104" not in src

BLOCK = '''
  // ——— qa-p222: KRSTNA PREDZGODOVINA 04104 — leto 1884 = 2/15
  //      (P221: 1885 = 1/15!). 1884 = 112 vpisov-DISTINCT (ŠTEVJE-IZ-VRSTIC-2.×!
  //      vrstna-aritmetika 7+7+9+8+8+10+10+10+8+8+9+10+8+2 = 114-vrstic −
  //      z84-DUP-korekcija = 112-DISTINCT = P221-'1884-=-112'-1:1!) /
  //      21-GRIBLJE / 20-hiš (h13-×2!) + ★★★ PISARJEVE-ANOMALIJE: s175-prepiše-
  //      8–14 (vrstna-aritmetika-REŠI-15–23!) + s177-REORIZENTACIJA (61–68→31–38!)
  //      + s182-81-DUP-korekcije-×3 + ★★★ z84-DUPLIKAT (s182+s183! NOVA-TIP!) +
  //      s184-prazna-vrstica + revizijske-poševnice-×10 + vas-DUELI-REŠENI-krop-hi
  //      (z99-GRIBLJE! z52-IZLOČEN! z60-IZLOČEN!) + ★★★ POZNEJŠI-PRIPISI-KRIŽ-
  //      z-mrliško-04106 (z70-†29/10-1887 + z112-†28/12-1887 + z75-MMK-1974!) +
  //      pag = sken+13-FOLIO-SVINČNIK (re-potrjeno-×3!). Dokaz:
  //      parish-baptism-1884-04104.json; skripte p222.
  {
  const p222Errors: string[] = [];
  const p222Bapt = HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && h.year === 1884);
  if (p222Bapt.length !== 21)
    p222Errors.push(`bloki 1884 (04104) ≠ 21 (${p222Bapt.length} — 21 Griblje-vpisov / 20 hiš (h13-×2!) / 112 DISTINCT = ŠTEVJE-IZ-VRSTIC-2.×!)`);
  if (HOUSE_VITALS.length !== 1839)
    p222Errors.push(`HOUSE_VITALS ≠ 1839 (${HOUSE_VITALS.length} — P221: 1677; P222: + 21 blokov 1884-04104 = 1839!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length !== 46)
    p222Errors.push(`bloki 04104 ≠ 46 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length} — P221: 25 × 1885; P222: + 21 × 1884 = 46!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)
    p222Errors.push("04104-bloki izven {1884, 1885} (predzgodovina-2/15: 1884–1885-do-P223!)");
  if (!p222Bapt.some((h) => h.houseNo === "37" && h.whatSi.includes("RESTART-z1")))
    p222Errors.push("★★★ z1-RESTART-z1-NA-DAN-1.-1.-GRIBLJE-h37 (PARALELA-P221!) ni označena");
  if (!p222Bapt.some((h) => h.houseNo === "36" && h.whatSi.includes("KRIŽAN") && h.whatSi.includes("96'-MISREAD-KOREKCIJA")))
    p222Errors.push("★★★ z59-hiša-page-'96'-MISREAD-KOREKCIJA (h36! KRIŽAN-oče+botri-×2!) ni označena");
  if (!p222Bapt.some((h) => h.houseNo === "13") || p222Bapt.filter((h) => h.houseNo === "13").length !== 2)
    p222Errors.push("★★★ h13-×2 (z19 + z69-PEZDIRC-mati!) ni 2 blokov");
  if (!p222Bapt.some((h) => h.whatSi.includes("z84-DUPLIKAT")))
    p222Errors.push("★★★ z84-DUPLIKAT-ANOMALIJA (s182+s183! NOVA-TIP!) ni označena");
  if (!p222Bapt.some((h) => h.whatSi.includes("vas-DUEL-REŠEN")))
    p222Errors.push("★★★ z99-vas-DUEL-REŠEN (GRIBLJE-vs-'Podplanina'-ZAVRNJENA!) ni označena");
  if (!p222Bapt.some((h) => h.houseNo === "18" && h.whatSi.includes("LAZAR")))
    p222Errors.push("★★★ z93-LAZAR-oče-nit (P220-1857!) ni označena");
  if (!p222Bapt.some((h) => h.houseNo === "62" && h.whatSi.includes("MILEK")))
    p222Errors.push("★★★ z105-botra-MILEK-nit (P218/P220-h65!) ni označena");
  if (!p222Bapt.some((h) => h.houseNo === "43" && h.whatSi.includes("PREČRTANA-TAIL") && h.whatSi.includes("†28/12-1887")))
    p222Errors.push("★★★ z112-PREČRTANA-TAIL + †28/12-1887-KRIŽ ni označena");
  if (!p222Bapt.some((h) => h.houseNo === "22" && h.whatSi.includes("†29/10-1887")))
    p222Errors.push("★★★ z70-pripis-†29/10-1887-KRIŽ ni označena");
  push(
    "qa-p222-parish-baptism-1884-04104",
    "P222: ŽUPNIJA PODZEMELJ — KRSTNA PREDZGODOVINA 04104, LETO 1884 = 2/15 (issue #18): okvir — s173–s186 (14 skenov; 2×-neodvisna-prenosa-md5-17/17!; s170–s172-proba-nazaj!; s185/s186-tail-kontekst!) + pag = sken+13-FOLIO-SVINČNIK-ARHIVARJA (re-potrjeno-×3-sveže: s177='190'/s181='194'/s185='198'! — skupaj-8×!) + **★★★ MEJA-1883/84 = s173 (z99-TAIL-1883 + VSOTNA-razpete-'1/8/8/4'-P214-TIP + rokopisna-'Jänner'-glava + RESTART-z1-NA-DAN-1.-1.-GRIBLJE-h34[~84-DUEL!] — PARALELA-P221-restart-z1-1885!) = 61.-POTRDITEV-invariante! (60.-P221!) + 1883 = 99-vpisov (P223-LEAD!)** + **★★★ 112-VPIISOV-DISTINCT — ŠTEVJE-IZ-VRSTIC-2.×-ZA-KRSTNO-LINIJO** (z1–z112; vrstna-aritmetika 7+7+9+8+8+10+10+10+8+8+9+10+8+2 = 114-vrstic − z84-DUP-korekcija = 112-DISTINCT = P221-'1884-=-112-vpisov'-1:1!) + **★★★ PISARJEVE-OŠTEVILČEVSKA-ANOMALIJE-×6 (REKORD!): s175-prepiše-8–14-za-9-vrstic (2-manjka! '8'-RAZPETA-VSOTNA-TIP! — VRSTNA-ARITMETIKA-REŠI-15–23!) + s177-REORIZENTACIJA (izvirno-61–68-PREČRTANO-×8→dopisano-31–38! — 4-strani-naprej-številke-s180!) + s178-40/41-wobble + s176-'81'→29-korekcija + s179-top-48/49-korekciji + s182-81-DUP-korekcije-×3 (→82/83/84! — 'Pri-vrstici-z-datumom-15-je-bila-številka-81-dvakrat-DUPLIKAT'!)** + **★★★ z84-DUPLIKAT-ANOMALIJA (s182-vrsta8=84 + s183-vrsta1=84-DUPLIKAT — pisar-2×-84! — zap-hi-2×-ČISTO + X-open-vs-85 — NOVA-TIP-ANOMALIJE! PARALELA-s182-81-DUP-isti-pisar!)** + **★★★ s184 = 93–102 + 1-PRAZNA-NEŠTEVILČENA-VRSTICA (med-99-in-100!) + REVIZIJSKE-POŠEVNICE-×10 (page-VLM-MIS-count-9! — P221-z101-PARALELA!)** + **★★★ 21-GRIBLJE / 20-hiš (h13-×2: z19+z69-PEZDIRC-mati!)** + **★★★ VAS-DUELI-REŠENI-krop-hi (z99 = GRIBLJE-JASNO-2:1-vs-trak-'Podplanina'-ZAVRNJENA! + z52 = PRILOZJE-IZLOČEN (page-'Griblje'-MISREAD!) + z60 = BORŠT-IZLOČEN (re-crop-'in-Gribl'-column-bleed-dokumentiran!))** + hišni-DUELI: z1-h34-vs-84 ('37'-3-reads-ZAVRNJENE-hi2-'digit2=4-ne-7'!) + z26-TRI (33/58/38!) + z75 (43/13!) + z93 (18-2:1-vs-page-'48'!) + z84dup (54/57!) + ordinal-KOREKCIJE (z19-'11'→19-krop-MISREAD! z26-'10'→26! z45-'44'→45-3:1! z59-'39'→59! z61-h68-vas-hi-'18'-noise!) + mesec-KOREKCIJE (z69/z75-'November/Feber'→august-chrono! z59-'Juni'→Juli! z51-Juni-rekonstrukcija!) + **★★★ POZNEJŠI-PRIPISI-KRIŽ-z-mrliško-04106 (2.-LETO-KRSTNE-LINIJE!): z70-Mathias-h22-'†29/10-1887' (krop-'1883'-chrono-KOREKCIJA!) + z112-Mathias-h43-'†28/12-1887' (krop-'1882'-KOREKCIJA-2:1! — PREČRTANA-TAIL!) + z19-'gest-3/5-884[?]-X-open' + z75-MMK-'matični-pregled-1974' + z99-'6.2.1911' + z105-'Mrt/Poroč-1.10.1953'-X-open (page-'1883'-chrono-KOREKCIJA-'1953'!)** + mreže: PEZDIRC-×4 (z69-mati + z95-mati+botra + z78-oče-grafija-'Peržirec' + z84dup-oče-'Peter-Pezdirec'!) + KRIŽAN-×3 (z59-oče+botri-×2 + z84-botra + z105-mati!) + BRODARIČ-×5 (z78-botra + z84-mati + z84dup-botra + z95-oče-Simon + z105-botra-Margaretha!) + POŽEK-×2 (z61-mati + z65-botra-X-open!) + URIH (z61-oče-'Urich/Uršič'-X-open!) + SIMEC (z51-mati-3:1!) + URH (z51-oče-krop!) + MILEK (z105-botra-'Mathias-Milek'! — P218/P220-h65!) + LAZAR (z93-oče-'Michael-Logar'! — P220-z4-1857!) + DRAGOŠ (z26-mati-3:1!) + DEBLIČ-×2 (z69-botra + z78-mati!) + JAKLIČ (z99-oče!) + **21 NOVIH BLOKOV parish.ts: vitals 1677 → 1839 · 04104 = 25 → 46 · 04105/04106/04894/04455-NESPREMENJENI**; skripte p222 (fetch-2×-md5-17/17 + read-×17 + traki-56 + krop-43+21+13 = 77 + build-entries + build-proof) + qa-p222 (222. kontrola!) + dokaz parish-baptism-1884-04104.json (112-DISTINCT: 21-Griblje + 91-druge! 10-anomalij/11-crossChecks/honesty-18!) + pt-luknja-46/1839; **★★★ KRSTNA-PREDZGODOVINA-LINIJA-2/15-LET!** (P223-LEAD: 1883 — s171–s172-ŽE-proba (z83–z98: Griblje-×4-tail: z88-h25[?]-Katharina + z94-h11-Nikolaus + z96-h63-Ana + z97-h29-Barbara!) + z99-tail-s173-ŽE-VLM → MEJA-1882/83-pred-s171 → probe-s164–s171!)",
    "P222: THE PARISH OF PODZEMELJ — THE BAPTISM-REGISTER-PREHISTORY 04104, THE YEAR 1884 = 2/15 (issue #18): the-frame — s173–s186 (14 scans; 2×-INDEPENDENT-md5-17/17!; the-s170–s172-backward-probe!) + pag = scan+13-THE-FOLIO-PENCIL (re-confirmed-×3-fresh — 8×-total!) + **★★★ THE-1883/84-BOUNDARY = s173 (the-z99-TAIL-1883 + the-SUM-ROW-SPREAD-'1/8/8/4'-P214-TYPE + the-handwritten-'Jänner'-header + the-RESTART-z1-ON-DAY-1-1-GRIBLJE-h34[~84-DUEL!] — the-PARALLEL-to-P221-the-restart-z1-1885!) = the-61st-CONFIRMATION! + 1883 = 99-entries (the-P223-LEAD!)** + **★★★ 112-ENTRIES-DISTINCT — THE-ROW-COUNTING-2nd-×-FOR-THE-BAPTISM-LINE** (z1–z112; the-row-arithmetic 7+7+9+8+8+10+10+10+8+8+9+10+8+2 = 114-rows − the-z84-DUP-correction = 112-DISTINCT = P221-'1884-=-112-entries'-1:1!) + **★★★ THE-SCRIBE-NUMBERING-ANOMALIES-×6 (RECORD!): s175-rewrites-8–14-FOR-9-ROWS (2-missing! the-'8'-SPREAD-SUM-TYPE! — the-ROW-ARITHMETIC-RESOLVES-15–23!) + s177-the-REORIENTATION (originally-61–68-CROSSED-×8→corrected-31–38! — the-4-pages-ahead-numbers-of-s180!) + s178-40/41-wobble + s176-'81'→29-correction + s179-top-48/49-corrections + s182-81-DUP-corrections-×3 (→82/83/84!)** + **★★★ THE-z84-DUPLICATE-ANOMALY (s182-row8=84 + s183-row1=84-DUPLICATE — the-scribe-2×-84! — zap-hi-2×-CLEAN + X-open-vs-85 — the-NEW-ANOMALY-TYPE! the-PARALLEL-to-s182-81-DUP-the-same-scribe!)** + **★★★ s184 = 93–102 + 1-EMPTY-UNNUMBERED-ROW (between-99-and-100!) + the-REVISION-SLASHES-×10 (the-page-VLM-MIS-count-9! — the-P221-z101-PARALLEL!)** + **★★★ 21-GRIBLJE / 20-houses (h13-×2!)** + **★★★ THE-VILLAGE-DUELS-RESOLVED-BY-CROP-HI (z99 = GRIBLJE-CLEARLY-2:1-vs-the-trak-'Podplanina'-REFUSED! + z52 = PRILOZJE-EXCLUDED (the-page-'Griblje'-MISREAD!) + z60 = BORŠT-EXCLUDED (the-re-crop-'in-Gribl'-column-bleed-documented!))** + the-house-DUELS + the-ordinal-CORRECTIONS + the-month-CORRECTIONS + **★★★ THE-LATER-ANNOTATIONS = THE-CROSS-WITH-THE-DEATH-BOOK-04106 (the-2nd-YEAR-OF-THE-BAPTISM-LINE!): z70-'†29/10-1887' + z112-'†28/12-1887' (the-CROSSED-TAIL!) + z19-'gest-3/5-884[?]' + z75-the-MMK-'1974' + z99-'6.2.1911' + z105-'Mrt/Poroč-1.10.1953'-X-open** + the-threads: PEZDIRC-×4 + KRIŽAN-×3 + BRODARIČ-×5 + POŽEK-×2 + URIH + SIMEC + URH + MILEK + LAZAR + DRAGOŠ + DEBLIČ-×2 + JAKLIČ + **21 NEW BLOCKS: the vitals 1677 → 1839 · the 04104 = 25 → 46**; the scripts p222 + qa-p222 (the 222nd check!) + the evidence parish-baptism-1884-04104.json (112-DISTINCT: 21-Griblje + 91-others!) + the pt-gap-46/1839; **★★★ THE-BAPTISM-PREHISTORY-LINE-2/15-YEARS!** (the P223-LEAD: 1883 — the-s171–s172-ALREADY-probed (the-Griblje-×4-tail!) → the-boundary-1882/83-before-s171 → probe-s164–s171!)",
    p222Errors.length === 0,
    p222Errors.length === 0
      ? `21 vpisov / 112 DISTINCT (ŠTEVJE-IZ-VRSTIC-2.×! − z84-DUP!) / 20 hiš (h13-×2!) · MEJA-1883/84-s173-61.-POTRDITEV · PISARJEVE-ANOMALIJE-×6 (s175 + s177-REORIZENTACIJA + z84-DUPLIKAT-NOVA-TIP!) · s184-prazna-vrstica+revizije-×10 · vas-DUELI-REŠENI (z99-GRIBLJE! z52/z60-IZLOČENI!) · pripisi-KRIŽ-04106 (†1887-×2 + MMK!) · **LINIJA-2/15!** · vitals 1839 · 04104 46`
      : p222Errors.join("; "),
  );
  }

'''
src = src.replace(ANCHOR, BLOCK + ANCHOR, 1)
src = src.replace("HOUSE_VITALS.length !== 1677", "HOUSE_VITALS.length !== 1839")
# P221-block 04104-total: 25 → 46 (zdaj vključuje 1884!)
src = src.replace('if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length !== 25)',
                  'if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length !== 46)')
src = src.replace('p221Errors.push(`bloki 04104 ≠ 25 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length} — P221: 25 × 1885 = krstna-predzgodovina-1/15!)`)',
                  'p221Errors.push(`bloki 04104 ≠ 46 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length} — P221: 25 × 1885; P222: + 21 × 1884 = 46!)`)')
# yearset-04104: {1885} → {1884, 1885}
src = src.replace('if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && (h.year ?? 0) !== 1885).length > 0)\n    p221Errors.push("04104-bloki izven {1885} (predzgodovina-1/15: samo-1885-do-P222!)");',
                  'if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)\n    p221Errors.push("04104-bloki izven {1884, 1885} (predzgodovina-2/15: 1884–1885-do-P223!)");')
QA.write_text(src, encoding="utf-8")
print(f"qa-parish: 1839×{src.count('HOUSE_VITALS.length !== 1839')} · qa-p222×{src.count('qa-p222-parish-baptism-1884-04104')} · yearset-{src.count('(h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885')}")

# --- skripte + verifierji patch (1677→1839) ---
files = sorted(set(glob.glob(str(ROOT / "scripts/**/*.py"), recursive=True) + glob.glob(str(ROOT / "scripts/**/*.mjs"), recursive=True)))
skip = ("p222_",)
patched = 0
for f in files:
    if any(s2 in f for s2 in skip): continue
    t = Path(f).read_text(encoding="utf-8")
    if "1677" not in t: continue
    o = t
    t = t.replace("1677", "1839")
    if t != o:
        Path(f).write_text(t, encoding="utf-8"); patched += 1
print(f"skripte-patched: {patched}")

vpatched = 0
for f in sorted(ROOT.glob("scripts/p19*.py")) + sorted(ROOT.glob("scripts/p2[0-2][0-9]_parish*.py")):
    if "p222" in f.name: continue
    t = f.read_text(encoding="utf-8"); o = t
    for a, b in [("vitals == 1677", "vitals == 1839"), ("vitalsTotal == 1677", "vitalsTotal == 1839"),
                 ('vitalsTotal"] == 1677', 'vitalsTotal"] == 1839'),
                 ('"vitalsTotal": 1677', '"vitalsTotal": 1839'),
                 ('\\"vitalsTotal\\": 1677', '\\"vitalsTotal\\": 1839'),
                 ('!== 1677"', '!== 1839"'),
                 ("1677-številcev", "1839-številcev"),
                 ("vitals-števec-1677", "vitals-števec-1839"), ("vitals-1677", "vitals-1839")]:
        t = t.replace(a, b)
    if t != o:
        f.write_text(t, encoding="utf-8"); vpatched += 1
print(f"verifierji-patched: {vpatched}")

ptp = ROOT / "research/issue17/pt-luknja-18-final.json"
pt = json.loads(ptp.read_text(encoding="utf-8"))
pt["corpus"]["vitalsTotal"] = 1839
pt["corpus"]["byBook"]["04104"] = 46
pt["corpus"]["housesNote"] = (pt["corpus"].get("housesNote") or "") + " | P222: +21-blokov-1884-krstna-04104-2/15 (vitals 1677→1839; 04104 25→46; ŠTEVIE-IZ-VRSTIC-2.×-112-DISTINCT = P221-'1884-=-112'-1:1 + 21-GRIBLJE/20-hiš (h13-×2!) + PISARJEVE-ANOMALIJE-×6 (s175-prepiše-8–14! + s177-REORIZENTACIJA-61–68→31–38! + z84-DUPLIKAT-NOVA-TIP!) + s184-prazna-vrstica+revizije-×10 + vas-DUELI-REŠENI-krop-hi (z99-GRIBLJE! z52/z60-IZLOČENI!) + pripisi-KRIŽ-†1887-×2-MMK!)"
ptp.write_text(json.dumps(pt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"pt-luknja: {pt['corpus']['vitalsTotal']}/{pt['corpus']['byBook']['04104']}")
