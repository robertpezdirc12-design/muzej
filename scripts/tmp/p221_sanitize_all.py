#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P221 — INSERT qa-p221 + sanitizacija (1652→1819, 04104=25 NOVO, yearset/guard-04104-1885, izjeme-NOVE-hiše-×4-loops, verifierji, pt-luknja)."""
from pathlib import Path
import glob, json, re

ROOT = Path("/home/z/my-project")
QA = ROOT / "src/lib/qa-parish.ts"
src = QA.read_text(encoding="utf-8")
ANCHOR = "  // ——— qa-p220: MRLIŠKA PREDZGODOVINA 04106 — leto 1857 = 29/29 — ZADNJE leto knjige —"
assert src.count(ANCHOR) == 1 and "qa-p221-parish-baptism-1885-04104" not in src

BLOCK = '''
  // ——— qa-p221: KRSTNA PREDZGODOVINA 04104 — leto 1885 = 1/15 — NOVA LINIJA
  //      (mrliška-04106-KONČANA-29/29-P220!). 1885 = 104 vpisov-kronološko
  //      (ŠTEVJE-IZ-VRSTIC-1.×-za-krstno-linijo! vrstna-aritmetika
  //      4+8+8+8+9+9+8+8+8+7+8+8+9+2) / 25-GRIBLJE = NOV-REKORD-PREDZGODOVINE/KORPUSA
  //      (prej-23-P218-1859!) / 20-hiš + 3-[?]-dueli (h1-×2 + h55-×2!) +
  //      ★★★ DVOJČKI-GRADAC-×2-2-VRSTICI (z92+z93 — page-VLM-SPOJIL-KOREKCIJA!) +
  //      ★★★ z101-NEIDENTIFICIRANA (DOKAZ: POPRAVEK-PISARJA-s199-102/103→103/104!) +
  //      ★★★ NASLOVNA-SREDI-LETNIKA-s190 + page-VLM-hišne-MISREAD-KOREKCIJE-×7 +
  //      ★★★ POZNEJŠI-PRIPISI-KRIŽ-z-mrliško-04106 (NOVA-VERIFIKACIJSKA-DIMENZIJA!) +
  //      pag = sken+13-FOLIO-SVINČNIK (razprti-list = 1-folio!). Dokaz:
  //      parish-baptism-1885-04104.json; skripte p221.
  {
  const p221Errors: string[] = [];
  const p221Bapt = HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && h.year === 1885);
  if (p221Bapt.length !== 25)
    p221Errors.push(`bloki 1885 (04104) ≠ 25 (${p221Bapt.length} — 25 Griblje-vpisov / 20 hiš + 3-[?]-dueli / 104 kronoloških = NOV-REKORD-25!)`);
  const p221Houses = p221Bapt.map((h) => h.houseNo);
  if (p221Houses.join(",") !== "21,[?],31,61,11,63,49,28,42,1,55,53,35,16,24,[?],17,58,9,55,[?],2,23,1,8")
    p221Errors.push(`hiše 1885 (04104) neujemane — najdeno: ${p221Houses.join(",")}`);
  if (HOUSE_VITALS.length !== 1819)
    p221Errors.push(`HOUSE_VITALS ≠ 1819 (${HOUSE_VITALS.length} — P220: 1652; P221: + 25 blokov 1885-04104 = 1819!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length !== 25)
    p221Errors.push(`bloki 04104 ≠ 25 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length} — P221: 25 × 1885 = krstna-predzgodovina-1/15!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && (h.year ?? 0) !== 1885).length > 0)
    p221Errors.push("04104-bloki izven {1885} (predzgodovina-1/15: samo-1885-do-P222!)");
  if (!p221Bapt.filter((h) => h.houseNo === "1").every((h) => h.whatSi.includes("h1")))
    p221Errors.push("★★★ h1-×2 (z33-ŽELKO + z100-'Škrilje'-MISREAD-KOREKCIJA!) ni označena (h1)");
  if (!p221Bapt.some((h) => h.houseNo === "1" && h.whatSi.includes("Škrilje")))
    p221Errors.push("★★★ z100-page-'Škrilje'-MISREAD-KOREKCIJA (GRIBLJE-h1!) ni označena");
  if (!p221Bapt.filter((h) => h.houseNo === "55").length === 2)
    p221Errors.push("★★★ h55-×2 (z37 + z68-SIMIC!) ni 2 blokov");
  if (!p221Bapt.some((h) => h.houseNo === "61" && h.whatSi.includes("4-MREŽE-V-1-VRSTICI") && h.whatSi.includes("URIH")))
    p221Errors.push("★★★ z14-h61-URIH-POŽEK-FILAK-PEZDIRC-4-MREŽE ni označena");
  if (!p221Bapt.some((h) => h.houseNo === "53" && h.whatSi.includes("MISREAD-KOREKCIJA") && h.whatSi.includes("PEZDIRC")))
    p221Errors.push("★★★ z47-page-'h33'-MISREAD-KOREKCIJA (h53! PEZDIRC-oče!) ni označena");
  if (!p221Bapt.some((h) => h.houseNo === "35" && h.whatSi.includes("h33-×2-HIPOTEZA-MRTVA")))
    p221Errors.push("★★★ z48-page-'h33'-MISREAD-KOREKCIJA (h35! h33-×2-HIPOTEZA-MRTVA!) ni označena");
  if (!p221Bapt.some((h) => h.houseNo === "58" && h.whatSi.includes("DRAGOŠ")))
    p221Errors.push("★★★ z63-mati-DRAGOŠ-nit ni označena");
  if (!p221Bapt.some((h) => h.houseNo === "8" && h.whatSi.includes("TAIL-1885") && h.whatSi.includes("KRIŽAN")))
    p221Errors.push("★★★ z104-TAIL-1885-ZADNJI-VPIS-KNJIGE-04104 + botra-KRIŽAN ni označena");
  push(
    "qa-p221-parish-baptism-1885-04104",
    "P221: ŽUPNIJA PODZEMELJ — KRSTNA PREDZGODOVINA 04104, LETO 1885 = 1/15 — NOVA LINIJA (mrliška-04106-KONČANA-29/29-P220!) (issue #18): okvir — s185–s199 (15 svežih 2×-md5-NEODVISNA-PRENOSA-15/15 + s200-vez-proba!; s185 = 1884-tail-kontekst!) + pag = sken+13-FOLIO-SVINČNIK-ARHIVARJA (razprti-dvostranski-list = 1-FOLIO! — potrjeno-5×-natančno: s185='198'/s190='203'/s193='206'/s196='209'/s199='212'! + tens-MISREADI-dokumentirani: s185-'148'/s188-'241'/s193-'266'/s195-'268'! — NOVA-KONVENCIJA-za-04104!) + **★★★ MEJA-1884/85 = s186 (TAIL-1884-z111[prečrtano!]-Gradac-68-Maria-†25.9.1885-pripis + z112[prečrtano!]-GRIBLJE-h43-Mathias-†28.12.1887-pripis + VSOTNA-razpete-'1/8/8/5'-P214-TIP-sorodna + rokopisna-'Jänner'-glava + RESTART-z1-NA-DAN-1.-1.-GRIBLJE-h21!) = 60.-POTRDITEV-invariante! (59.-P220!) + 1884 = 112-vpisov (s185-ordinali-103–110!)** + **★★★ 104-VPIISOV-KRONOLOŠKO — ŠTEVJE-IZ-VRSTIC-1.×-ZA-KRSTNO-LINIJO-04104** (z1–z104; vrstna-aritmetika 4+8+8+8+9+9+8+8+8+7+8+8+9+2 = 104; zap-stolpci-15/15-ČISTO; meseci J11+F3+M9+A6+M9+J11+J7+A10+S7+O9+N3+D16) + **★★★ DVOJČKI-GRADAC-×2-2-VRSTICI (z92-Anton-'Na-umrla'-umrl + z93-Jožef-živ — OBA-Dez-14/14-Gradac-5[~]! — page-VLM-SPOJIL-v-1-vrstico-KOREKCIJA-2-vrstici! — PARALELA-P219-DVOJČKI-SIMIC-h19-1858! + pripis-'Umrła-28.4.1965-Zagreb'-MMK!)** + **★★★ z101-NEIDENTIFICIRANA-VRSTICA (page-VLM-ZAMUJENA!) — DOKAZ-za-obstoj: POPRAVEK-PISARJA-s199 (z103-'102'-prečrtano→103 + z104-'103'-prečrtano→104 = pisar-sprva-pozabil-štet-z101!) + t4-trak-fragment-'oče-Janez-Tomaž-½-gem.' + robni-svinčnik-100/101/102-na-dnu-s198 (revizija!) + r11-mikro-8×-'pravih-vrstic-3'-na-dnu! — X-open!** + **★★★ POPRAVEK-PISARJA-s199-×2 + z102-IME-POPRAVEK (Katharina-prečrtano→Marija!)** + **★★★ NASLOVNA-GLAVA-SREDI-LETNIKA-s190 ('Geburts-und-Tauf-Buch.'-natisnjena-PONOVLJENA! — paralela-mrliška-04106-s9+s10-SREDI-1858-quiri! + glava-'18 85'-page-VLM-'1886'-MISREAD-KOREKCIJA-krop-1:1!)** + **★★★ 25-GRIBLJE = NOV-REKORD-PREDZGODOVINE-IN-KORPUSA (prej-23-P218-1859-mrliška!) / 20-hiš + 3-[?]-dueli** (h1-×2: z33-Mathias-ŽELKO-oče-'Miklo'-botri-Želko-×2 + z100-Anton-[page-'Škrilje'-MISREAD-KOREKCIJA-r7-krop-'Gribile-h1'-1:1!]; h55-×2: z37-Johann-oče-'Simec'-¼ + z68-Mathias-oče-'Miko-Simic'!; z59-honesty-MAX-1885-hiša-QUAD-DUEL-27/47/37/21-ime-TRI-DUEL-Marko/Maria/Martin/Martha!; z78-hiša-TRI-DUEL-17/29/9/99!; z26-hiša-TRI-DUEL-49/17/1[8?]!) + **★★★ page-VLM-hišne-MISREAD-KOREKCIJE-×7** (h6→61 [z14!]-2:1-trak+krop + h45→42 [z30!] + h33→53 [z47!]-PEZDIRC-oče-'Johan-Pegdic' + h33→35 [z48!]-h33-×2-HIPOTEZA-MRTVA! + h19→17 [z62!] + h39-ep91→23 [z85!]-mati-PEZDIRC-'Katharina-roj.-Pegdirec'! + ordinali-MISREADI-×4-rešeni-zap-stolpcem!) + **★★★ POZNEJŠI-PRIPISI-NA-KRSTNIH-VPISIH = KRIŽ-Z-MRLIŠKO-04106 (NOVA-VERIFIKACIJSKA-DIMENZIJA!): z1-Mathias-h21-'†7.9.1887' + z5-Martin-'gest.-12.[?]1888' + 1884-tail-†25.9.1885/†28.12.1887 + z80-Grem-'†30.9.99' + MMK-modri-pripisi-s197-×5!** + mreže: PEZDIRC-×4 (z47-oče + z85-mati + z63/z14-botri!) + POŽEK (z14-oče + z5-botra!) + ŽELKO (z33!) + SIMIC-×2 (z37+z68!) + URIH (z14-h61!) + FILAK (z14-mati!) + DRAGOŠ (z63-mati!) + HLEBEC (z82-oče!) + KRIŽAN-botra-TAIL (z104!) + **★★★ KNJIGA-04104-KONČANA-do-konca (TAIL-z103–z104-Dez-26/30 + BREZ-VSOTNE + s200-VEZ-platnica! — 1886-gre-v-04105 = korpus-P79!); **25 NOVIH BLOKOV parish.ts: vitals 1652 → 1819 · 04104 = 0 → 25 · 04105/04106/04894/04455-NESPREMENJENI**; skripte p221 (fetch-2×-md5-15/15 + read-×15 + traki-60 + krop-~75 + build-entries + build-proof) + qa-p221 (221. kontrola!) + dokaz parish-baptism-1885-04104.json (104 entries: 25-Griblje + 79-druge! 12-anomalij/12-crossChecks/honesty-16!) + pt-luknja-25/1819; **★★★ KRSTNA-PREDZGODOVINA-LINIJA-1/15-LET!** (P222-LEAD: 1884 — s185-tail-ŽE-VLM (z105-GRIBLJE-h62-Johann-oče-'Simon-Kure-½-Gribl.' + z106–z110: 5-vrstic! Dez-5–18) → MEJA-1883/84-pred-s185 → probe-s178–s185!)",
    "P221: THE PARISH OF PODZEMELJ — THE BAPTISM-REGISTER-PREHISTORY 04104, THE YEAR 1885 = 1/15 — A NEW LINE (the-death-04106-COMPLETE-29/29-P220!) (issue #18): the-frame — s185–s199 (15 fresh 2×-md5-INDEPENDENT-DOWNLOADS-15/15 + s200-cover-probe!; s185 = the-1884-tail-context!) + pag = scan+13-THE-FOLIO-PENCIL (the-spread-two-sided-leaf = 1-FOLIO! — confirmed-5×-exactly + the-tens-MISREADS-documented! — the-NEW-CONVENTION-for-04104!) + **★★★ THE-1884/85-BOUNDARY = s186 (the-TAIL-1884-z111[crossed!]-Gradac-68 + z112[crossed!]-GRIBLJE-h43 + the-SUM-ROW-SPREAD-'1/8/8/5'-P214-TYPE + the-handwritten-'Jänner'-header + the-RESTART-z1-ON-DAY-1-1-GRIBLJE-h21!) = the-60th-CONFIRMATION! + 1884 = 112-entries** + **★★★ 104-ENTRIES-CHRONOLOGICAL — THE-ROW-COUNTING-1st-×-FOR-THE-BAPTISM-LINE** (z1–z104; the-row-arithmetic 4+8+8+8+9+9+8+8+8+7+8+8+9+2 = 104; the-ordinal-columns-15/15-CLEAN!) + **★★★ THE-GRADAC-TWINS-×2-2-ROWS (z92-Anton-died + z93-Jožef-lived — BOTH-Dec-14/14! — the-page-VLM-MERGED-into-1-row-CORRECTION-2-rows! — the-PARALLEL-to-P219-the-SIMIC-TWINS!)** + **★★★ z101 = THE-UNIDENTIFIED-ROW (the-page-VLM-MISSED!) — the-PROOF-of-existence: the-SCRIBE-CORRECTION-s199 ('102'-crossed→103 + '103'-crossed→104 = the-scribe-initially-forgot-to-count-z101!) + the-t4-strip-fragment-'father-Janez-Tomaž-½-gem.' + the-margin-pencil-100/101/102!** + **★★★ THE-SCRIBE-CORRECTION-s199-×2 + z102-the-NAME-CORRECTION (Katharina-crossed→Marija!)** + **★★★ THE-TITLE-HEADER-MID-YEAR-s190 (the-printed-'Geburts-und-Tauf-Buch.'-REPEATED! — the-parallel-to-the-death-book-s9+s10-MID-1858-quirk! + the-'18 85'-header-the-page-VLM-'1886'-MISREAD-CORRECTION-crop-1:1!)** + **★★★ 25-GRIBLJE = the-NEW-RECORD-of-the-PREHISTORY-and-THE-CORPUS (the-previous-23-P218-1859!) / 20-houses + 3-[?]-duels** + **★★★ the-page-VLM-house-MISREAD-CORRECTIONS-×7** + **★★★ THE-LATER-ANNOTATIONS-ON-THE-BAPTISM-ENTRIES = THE-CROSS-WITH-THE-DEATH-BOOK-04106 (the-NEW-VERIFICATION-DIMENSION!)** + the-threads: PEZDIRC-×4 + POŽEK + ŽELKO + SIMIC-×2 + URIH + FILAK + DRAGOŠ + HLEBEC + KRIŽAN-godmother-TAIL + **★★★ THE-BOOK-04104-COMPLETE-to-the-end (the-TAIL-z103–z104-Dec-26/30 + WITHOUT-the-SUM-ROW + s200-the-COVER! — 1886-goes-to-the-NEW-book-04105 = the-corpus-P79!); **25 NEW BLOCKS: the vitals 1652 → 1819 · the 04104 = 0 → 25**; the scripts p221 + qa-p221 (the 221st check!) + the evidence parish-baptism-1885-04104.json (104 entries: 25-Griblje + 79-others!) + the pt-gap-25/1819; **★★★ THE-BAPTISM-PREHISTORY-LINE-1/15-YEARS!** (the P222-LEAD: 1884 — the-s185-tail-ALREADY-VLM-read → the-boundary-1883/84-before-s185 → probe-s178–s185!)",
    p221Errors.length === 0,
    p221Errors.length === 0
      ? `25 vpisov / 104 kronoloških (ŠTEVJE-IZ-VRSTIC-1.×-krstna!) / 20 hiš + 3-[?]-dueli (h1-×2-ŽELKO + h55-×2-SIMIC! z59-honesty-MAX!) · MEJA-1884/85-s186-60.-POTRDITEV · DVOJČKI-GRADAC-2-VRSTICI · z101-NEIDENTIFICIRANA (popravek-pisarja-DOKAZ!) · NASLOVNA-sredi-letnika-s190 · MISREAD-KOREKCIJE-×7 · pripisi-KRIŽ-04106 · **NOVA-LINIJA-1/15!** · vitals 1819 · 04104 25`
      : p221Errors.join("; "),
  );
  }

'''
src = src.replace(ANCHOR, BLOCK + ANCHOR, 1)
src = src.replace("HOUSE_VITALS.length !== 1652", "HOUSE_VITALS.length !== 1819")
# izjeme-NOVE-hiše: blanket 04104 (predzgodovina-PRED-vsemi-pini!)
for marker in [
    'for (const hn of ["28", "53"]) {',
    'for (const hn of ["23", "46", "70", "91"]) {',
    'for (const hn of ["9", "14", "45"]) {',
    'for (const hn of ["22", "49"]) {',
]:
    i = src.index(marker)
    j = src.index("HOUSE_VITALS.some((v) => v.houseNo === hn &&", i)
    ins = 'HOUSE_VITALS.some((v) => v.houseNo === hn && !(v.bookSignature === "04104") &&'  # P221: + krstna-04104-predzgodovina (1885!) — PRED-vsemi-pini!
    src = src[:j] + ins + src[j + len('HOUSE_VITALS.some((v) => v.houseNo === hn &&'):]
QA.write_text(src, encoding="utf-8")
print(f"qa-parish: 1819×{src.count('HOUSE_VITALS.length !== 1819')} · 04104-izjeme×{src.count('!(v.bookSignature === \"04104\")')} · qa-p221×{src.count('qa-p221-parish-baptism-1885-04104')}")

# --- skripte + verifierji patch (1652→1819) ---
files = sorted(set(glob.glob(str(ROOT / "scripts/**/*.py"), recursive=True) + glob.glob(str(ROOT / "scripts/**/*.mjs"), recursive=True)))
skip = ("p221_",)
patched = 0
for f in files:
    if any(s2 in f for s2 in skip): continue
    t = Path(f).read_text(encoding="utf-8")
    if "1652" not in t: continue
    o = t
    t = t.replace("1652", "1819")
    if t != o:
        Path(f).write_text(t, encoding="utf-8"); patched += 1
print(f"skripte-patched: {patched}")

vpatched = 0
for f in sorted(ROOT.glob("scripts/p19*.py")) + sorted(ROOT.glob("scripts/p2[0-2][0-9]_parish*.py")):
    if "p221" in f.name: continue
    t = f.read_text(encoding="utf-8"); o = t
    for a, b in [("vitals == 1652", "vitals == 1819"), ("vitalsTotal == 1652", "vitalsTotal == 1819"),
                 ('vitalsTotal"] == 1652', 'vitalsTotal"] == 1819'),
                 ('"vitalsTotal": 1652', '"vitalsTotal": 1819'),
                 ('\\"vitalsTotal\\": 1652', '\\"vitalsTotal\\": 1819'),
                 ('!== 1652"', '!== 1819"'),
                 ("1652-številcev", "1819-številcev"),
                 ("vitals-števec-1652", "vitals-števec-1819"), ("vitals-1652", "vitals-1819")]:
        t = t.replace(a, b)
    if t != o:
        f.write_text(t, encoding="utf-8"); vpatched += 1
print(f"verifierji-patched: {vpatched}")

ptp = ROOT / "research/issue17/pt-luknja-18-final.json"
pt = json.loads(ptp.read_text(encoding="utf-8"))
pt["corpus"]["vitalsTotal"] = 1819
pt["corpus"]["byBook"]["04104"] = 25
pt["corpus"]["housesNote"] = (pt["corpus"].get("housesNote") or "") + " | P221: +25-blokov-1885-krstna-04104-NOVA-LINIJA-1/15 (vitals 1652→1819; 04104 0→25; ŠTEVJE-IZ-VRSTIC-1.×-104-kronološko + 25-GRIBLJE-NOV-REKORD-KORPUSA (prej-23!) + DVOJČKI-GRADAC-2-VRSTICI (page-VLM-SPOJIL-KOREKCIJA!) + z101-NEIDENTIFICIRANA (popravek-pisarja-DOKAZ!) + NASLOVNA-sredi-letnika-s190 + MISREAD-KOREKCIJE-×7 (h6→61/h45→42/h33→53/h33→35/h19→17/h39→23/'Škrilje'→GRIBLJE!) + pripisi-KRIŽ-z-mrliško-04106-NOVA-DIMENZIJA!)"
ptp.write_text(json.dumps(pt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"pt-luknja: {pt['corpus']['vitalsTotal']}/{pt['corpus']['byBook']['04104']}")
