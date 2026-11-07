#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P224 — INSERT qa-p224 + sanitizacija (1717→1742, 04104=65→90, yearset-04104-{1882..1885}, pt-luknja)."""
from pathlib import Path
import glob, json, re

ROOT = Path("/home/z/my-project")
QA = ROOT / "src/lib/qa-parish.ts"
src = QA.read_text(encoding="utf-8")
ANCHOR = "  // ——— qa-p223: KRSTNA PREDZGODOVINA 04104 — leto 1883 = 3/15"
assert src.count(ANCHOR) == 1 and "qa-p224-parish-baptism-1882-04104" not in src

BLOCK = '''
  // ——— qa-p224: KRSTNA PREDZGODOVINA 04104 — leto 1882 = 4/15
  //      (P223: 1883 = 3/15!). 1882 = 106 vpisov-DISTINCT (vrstna-aritmetika
  //      8+9+8+8+7+9+8+7+7+8+8+8+8+3 = 106 = P223-LEAD-'z88–z106-tail'-1:1-INVARIANTA!) /
  //      25-GRIBLJE / 23-hiš (h13-×2: z89+z99! h68-×2: z105/z106-DVOJČKI-ZWILLINGE!) =
  //      TIE-REKORD-P221! + ★★★ MEJA-1881/82-s147/s148 (TAIL-1881-z83–z89 + 'finis' +
  //      'Anni 1 8 8 1.'-RAZPETA-P214-TIP-4.-instance! + 'Jahr 18|82'-glava + RESTART-z1-
  //      NA-DAN-2.-1.-JÄNNER-Dobravce-h27!) = 63.-POTRDITEV + ★★★ S160-'NOVEMBER'-MISREAD-
  //      KOREKCIJA = DEZEMBER-BLOK-z92–z106 (z96-'DECEMBER'-labela-VIZUALNO! z103-dan-31!
  //      '…ember'-failure-mode-PARALELA-P223-'Feber'!-Dez-31-×4: z103–z106!) + ★★★ Z71-
  //      MESEC-KOREKCIJA (OKTOBER-11/12!-October-labela-z70!) + ★★★ FOLIACIJA-TRI-SERIJE
  //      (sken−6-1882-9-VIZUALNIH! + ★LUKNJA-'158'-skok-s163→s164! + sken−5-1883! +
  //      'Pag.'-'sken+13'-1884!) + ★★★ S149-Z16-DUPLIKAT (16-×2→17!-P222-z84-PARALELA!)
  //      + ★★★ Z55-ZAP-KOREKCIJA (VIZUALNO-'55'!) + HIŠNE-VIZUALNE-REŠITVE-×6 (z85-58!
  //      z90-74! z91-44! z92-43! z23-73! z97-47!-KURRENT-1↔4/7+3↔5!) +
  //      POZNEJŠI-PRIPISI-MMK-×6 (z7-1955! z22-1960-MNR! z43-†1919! z58-†1937! z91-†1966!
  //      z95-†1971!) + mreže PEZDIRC-×4/DRAGOŠ-×2/KRIŽAN-×2/KLOBUČAR-×3/LAZAR/POŽEK-×2/
  //      BRODARIČ-×2/MILEK/SIMEC/ŽELJKO-×3. Dokaz: parish-baptism-1882-04104.json; skripte p224.
  {
  const p224Errors: string[] = [];
  const p224Bapt = HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && h.year === 1882);
  if (p224Bapt.length !== 25)
    p224Errors.push(`bloki 1882 (04104) ≠ 25 (${p224Bapt.length} — 25 Griblje-vpisov / 23 hiš (h13-×2 + h68-×2-DVOJČKI!) / 106-DISTINCT = P223-LEAD-1:1 / TIE-REKORD-P221!)`);
  if (HOUSE_VITALS.length !== 1742)
    p224Errors.push(`HOUSE_VITALS ≠ 1742 (${HOUSE_VITALS.length} — P223: 1717; P224: + 25 blokov 1882-04104 = 1742!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length !== 90)
    p224Errors.push(`bloki 04104 ≠ 90 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length} — P223: 65; P224: + 25 × 1882 = 90!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)
    p224Errors.push("04104-bloki izven {1882, 1883, 1884, 1885} (predzgodovina-4/15: 1882–1885-do-P225!)");
  if (!p224Bapt.some((h) => h.whatSi.includes("63.-POTRDITEV") || h.whatSi.includes("MEJA-KOREKCIJA")))
    p224Errors.push("★★★ MEJA-1881/82-s147/s148 (finis + Anni-'1 8 8 1.'-RAZPETA + RESTART-z1-Jän-2!) ni označena");
  if (!p224Bapt.some((h) => h.houseNo === "58" && h.whatSi.includes("VIZUALNO-3×")))
    p224Errors.push("★★★ z85-hiša-VIZUALNA-REŠITEV (58!-page-'38'-3/5-ZAVRNJEN!) ni označena");
  if (!p224Bapt.some((h) => h.houseNo === "74" && h.whatSi.includes("7→1-ZAVRNJEN")))
    p224Errors.push("★★★ z90-hiša-VIZUALNA-REŠITEV (74!-page-'14'-7→1-ZAVRNJEN!) ni označena");
  if (!p224Bapt.some((h) => h.houseNo === "44" && h.whatSi.includes("4→1-ZAVRNJEN")))
    p224Errors.push("★★★ z91-hiša-VIZUALNA-REŠITEV (44!-page-'11'-4→1-ZAVRNJEN!) ni označena");
  if (!p224Bapt.some((h) => h.houseNo === "43" && h.whatSi.includes("DEZEMBER-labela-z92-VIZUALNO")))
    p224Errors.push("★★★ z92-hiša-43-VIZUALNO + DEZEMBER-labela-z92 (carry-over-1882!) ni označena");
  if (!p224Bapt.some((h) => h.houseNo === "73" && h.whatSi.includes("γ-7")))
    p224Errors.push("★★★ z23-hiša-VIZUALNA-REŠITEV (73!-γ-7!) ni označena");
  if (!p224Bapt.some((h) => h.houseNo === "68") || p224Bapt.filter((h) => h.houseNo === "68").length !== 2)
    p224Errors.push("★★★ h68-×2-DVOJČKI-ZWILLINGE (z105+z106!) ni 2 blokov");
  if (!p224Bapt.some((h) => h.houseNo === "13") || p224Bapt.filter((h) => h.houseNo === "13").length !== 2)
    p224Errors.push("★★★ h13-×2 (z89 + z99!) ni 2 blokov");
  if (!p224Bapt.some((h) => h.whatSi.includes("ZAP-KOREKCIJA (z55-NE-z54!")))
    p224Errors.push("★★★ z55-ZAP-KOREKCIJA (VIZUALNO-'55'!-page-shift!) ni označena");
  if (!p224Bapt.some((h) => h.whatSi.includes("OKTOBER-11/12")))
    p224Errors.push("★★★ z71-MESEC-KOREKCIJA (OKTOBER!-page-'[?Nov]'-'…ember'-failure!) ni označena");
  if (!p224Bapt.some((h) => h.whatSi.includes("DECEMBER-labela-z96-VIZUALNO")))
    p224Errors.push("★★★ s160-DEZEMBER-KOREKCIJA (z96-'DECEMBER'-labela!-dan-31!) ni označena");
  if (!p224Bapt.some((h) => h.whatSi.includes("ZWILLINGE")))
    p224Errors.push("★★★ DVOJČKI-GRIBLJE-h68-ZWILLINGE-bracket (z105/z106!) ni označena");
  if (!p224Bapt.some((h) => h.whatSi.includes("umrl-27.3.1966")))
    p224Errors.push("★★★ z91-pripis-MMK-'umrl-27.3.1966-MMK-k.50-str.81' ni označena");
  if (!p224Bapt.some((h) => h.whatSi.includes("Maria-Križan")))
    p224Errors.push("★★★ z29-KRIŽAN-mati-nit-KOREKCIJA (page-'Kuržan'!) ni označena");
  if (!p224Bapt.some((h) => h.whatSi.includes("umrla-29.11.1960")))
    p224Errors.push("★★★ z22-pripis-MMK-'umrla-29.11.1960'-MNR-št.187 ni označena");
  push(
    "qa-p224-parish-baptism-1882-04104",
    "P224: ŽUPNIJA PODZEMELJ — KRSTNA PREDZGODOVINA 04104, LETO 1882 = 4/15 (issue #18): okvir — s147–s161 (15 skenov; 2×-neodvisna-prenosa-md5-17/17!; s145–s146-proba! s159–s161-lead-ŽE-VLM-P223!) + **gola-svinčna-pag-'sken−6'** (9-VIZUALNIH: s148='142'/s153='147'/s157='151'/s159='153'/s160='154'/s161='155'/s162='156'/s163='157'! — s157-DUEL-REŠEN: page-'154'+krop-'157'-ZAVRNJENA-'151'! — P223-'s161=155[~156?]'-GARBLE-REŠEN!) + **★★★ MEJA-1881/82 = s147/s148 (TAIL-1881-z83–z89-Dez-8–21-×7 + 'finis'-beseda + 'Anni 1 8 8 1.'-RAZPETE-CIFRE-črez-stolpce-P214-TIP-4.-instance (1/8/8/5-P221 + 1/8/8/4-P222 + 1 8 8 3.-P223!) + s148-glava-'Jahr 18|82' + RESTART-z1-NA-DAN-2.-1.-JÄNNER-Dobravce-h27-Maria-Nemanic — PARALELA-P221-z1-1.1.!-P222-z1-1.1.!-P223-z1-4.1.!) = 63.-POTRDITEV-invariante! (62.-P223!)** + **★★★ 106-VPIISOV-DISTINCT — ŠTEVJE-IZ-VRSTIC-4.×-ZA-KRSTNO-LINIJO** (z1–z106; vrstna-aritmetika 8+9+8+8+7+9+8+7+7+8+8+8+8+3 = 106 = P223-LEAD-'z88–z106-tail-1882'-1:1-INVARIANTA!) + **★★★ S160-'NOVEMBER'-MISREAD-KOREKCIJA = DEZEMBER-BLOK-z92–z106: page-VLM-'November-16–30'-ANOMALIJA-po-z95-Dez-16 → KROPI-REŠILI: (1) z96-LABELA-'DECEMBER'-VIZUALNO! (2) z103-DAN-31/31 (November-NIMA-31.!-2×!) (3) z92-'DECEMBER'-labela-VIZUALNO (carry-over!) — '…ember'-failure-mode-PARALELA-P223-'Feber'/'Mai'! — DEZ-31-×4 (z103–z106!) — KRONOLOGIJA-POPOLNA!** + **★★★ Z71-MESEC-KOREKCIJA: page-'[?November]-11.-12.' → October-labela-z70 + carry-over = OKTOBER-11/12! (…ember-2.-instance!)** + **★★★ FOLIACIJA-TRI-SERIJE (DOPOLNJENI-S-TREJEM-DELOM!): (1) GOLA-'sken−6'-1882-okno-9-VIZUALNIH (142/147/151/153/154/155/156/157!) (2) ★FOLIACIJSKA-LUKNJA-'158' (NOVO!-skok-s163='157'→s164='159'!) (3) 'sken−5'-1883-okno (P223!) — menjava-konvencije-NA-s164 (LUKNJA!)** + **★★★ S149-Z16-DUPLIKAT-ANOMALIJA (2.-instance!): zap-stolpec-'15[prečrt-palična-revizija]','16','16[prečrt]/17[dopisano]' — pisar-16-×2! — PARALELA-P222-z84-DUPLIKAT + z16/z17-Dobravce-h26-Feber-18-×2-DVOJČKI?-X-open-garble!** + **★★★ Z55-ZAP-KOREKCIJA (page-VLM-zap-shift!): Griblje-Milech-vrstica = Z55 (NE-z54! — zap-stolpec-50–57-ČISTO + VIZUALNO-'55-14-14-Griblje-65'! — z54='Kornee-8'!)** + **★★★ HIŠNE-VIZUALNE-REŠITVE-×6 (KURRENT-1↔4/7-in-3↔5-page-misredi!): z85-'38'→'58'-3× + z90-'14'→'74'-VIZUALNO (γ-7!) + z91-'11'→'44'-3× + z92-'13'→'43'-3× + z23-'43'-krop→'73'-VIZUALNO + z97-'17'-krop→'47'-2:1** + **★★★ 25-GRIBLJE / 23-hiš (h13-×2: z89+z99! h68-×2: z105/z106-DVOJČKI-ZWILLINGE!) = TIE-REKORD-P221 (1885!) — vs-21-P222 + 19-P223!** + **★★★ POZNEJŠI-PRIPISI-MMK-ERA-×6 (4.-LETO-KRSTNE-LINIJE!): z7-'umrla-7.[~4-DUEL!].8.1955-v-Bohinju[?]' + z22-'umrla-29.11.1960-v-Groblju[~Otočec]-MNR-Griblje-8/1960-št.187' + z43-'†-23/4.[~1-DUEL!]-1919' + z58-'†-30.4.[~9-DUEL!]-1937' + z91-'umrl-27.3.1966-v-Gribljah-MMK-k.50-str.81'-2× + z95-'umrla-26.[~28-DUEL!]-6.1971-v-Ljubljani'** + mreže: PEZDIRC-grafija-×4 (z23-mati-'Pegdire'-X-open! + z89-mati-'roj.-Pezdirc'-2×! + z90-mati-'roj.-Perdiuc'+botra-'Michel-Perdiuc'-DVOJNI-2×! — PARALELA-P223-z96-Peddire-×2! + z99-mati-'Peghire'-X-open + z55-botra + z73-oče-X-open) + DRAGOŠ-×2 (z22-mati-'Dragos'-2×! + z85-mati-'Drugot'-X-open!) + KRIŽAN-×2 (z29-mati-'Maria-Križan'-KOREKCIJA! + z99-botra-'Dorothea-Hrižan'-2×!) + KLOBUČAR-×3 (z10-mati! + z34-oče! + z97-oče! — ×3-leta-nit!) + LAZAR (z31-oče-'Michael'! — P220/P222!) + POŽEK-×2 (z43-oče-'Požeh'! + z105/z106-mati-'Požek'!) + BRODARIČ-×2 (z31 + z74-botre!) + MILEK (z55-oče-'Milech'-h65!) + SIMEC (z22-botra-'Georg'-2×!) + ŽELJKO-×3 (z29-oče+botri-×2! — P139-1909-nit!) + **25 NOVIH BLOKOV parish.ts: vitals 1717 → 1742 · 04104 = 65 → 90 · 04105/04106/04894/04455-NESPREMENJENI**; skripte p224 (fetch-2×-md5-17/17 + read-×17 + krop-51 + krop2-34 + krop3-15 + duel-celice-×11-VIZUALNO + build-entries + build-proof) + qa-p224 (224. kontrola!) + dokaz parish-baptism-1882-04104.json (106-DISTINCT: 25-Griblje + 81-druge! 9-anomalij/10-crossChecks/honesty-22!) + pt-luknja-90/1742; **★★★ KRSTNA-PREDZGODOVINA-LINIJA-4/15-LET!** (P225-LEAD: 1881 — TAIL-ŽE-VLM (s147: z83–z89-Dez-8–21 + finis + Anni-'1 8 8 1.'-razpeta!) → MEJA-1880/81-pred-s147 → probe-s141–s147! — gola-pag-'sken−6'-pričakovana!)",
    "P224: THE PARISH OF PODZEMELJ — THE BAPTISM-REGISTER-PREHISTORY 04104, THE YEAR 1882 = 4/15 (issue #18): the-frame — s147–s161 (15 scans; 2×-INDEPENDENT-md5-17/17!) + the-plain-pencil-pag-'scan−6' (9-VISUAL-reads!) + **★★★ THE-1881/82-BOUNDARY = s147/s148 (the-TAIL-1881-z83–z89-Dec-8–21 + the-'finis'-word + the-'Anni 1 8 8 1.'-SPREAD-DIGITS-P214-TYPE-4th-instance + the-'Jahr 18|82'-header + the-RESTART-z1-ON-DAY-2-1-JÄNNER-Dobravce-h27!) = the-63rd-CONFIRMATION!** + **★★★ 106-ENTRIES-DISTINCT — the-ROW-COUNTING-4th-×-FOR-THE-BAPTISM-LINE (the-ROW-ARITHMETIC = 106 = the-P223-LEAD-1:1-INVARIANT!)** + **★★★ THE-S160-'NOVEMBER'-MISREAD-CORRECTION = THE-DEZEMBER-BLOCK-z92–z106 (the-z96-'DECEMBER'-label-VISUAL! the-z103-day-31! the-'…ember'-failure-mode-PARALLEL-to-P223! — Dec-31-×4!)** + **★★★ THE-Z71-MONTH-CORRECTION (OCTOBER-11/12!-the-October-label-z70-carry-over!)** + **★★★ THE-FOLIATION-THREE-SERIES (the-'scan−6'-1882-window-9-visual! + ★the-FOLIATION-GAP-'158' (the-skip-s163→s164!) + the-'scan−5'-1883! + the-'Pag.'-'scan+13'-1884!)** + **★★★ THE-S149-Z16-DUPLICATE-ANOMALY (the-16-×2→17!-the-P222-z84-PARALLEL!)** + **★★★ THE-Z55-ZAP-CORRECTION (VISUAL-'55'!-the-page-shift!)** + **★★★ THE-HOUSE-VISUAL-RESOLUTIONS-×6 (z85-58! z90-74! z91-44! z92-43! z23-73! z97-47!-the-KURRENT-1↔4/7+3↔5!)** + **★★★ 25-GRIBLJE / 23-houses (h13-×2! h68-×2-TWINS!) = TIE-RECORD-P221!** + **★★★ THE-LATER-ANNOTATIONS-MMK-ERA-×6 (z7-1955 + z22-1960-MNR! + z43-†1919 + z58-†1937 + z91-†1966 + z95-†1971!)** + the-threads: PEZDIRC-×4 + DRAGOŠ-×2 + KRIŽAN-×2 + KLOBUČAR-×3 + LAZAR + POŽEK-×2 + BRODARIČ-×2 + MILEK + SIMEC + ŽELJKO-×3 + **25 NEW BLOCKS: the vitals 1717 → 1742 · the 04104 = 65 → 90**; the scripts p224 + qa-p224 (the 224th check!) + the evidence parish-baptism-1882-04104.json (106-DISTINCT: 25-Griblje + 81-others!) + the pt-gap-90/1742; **★★★ THE-BAPTISM-PREHISTORY-LINE-4/15-YEARS!** (the P225-LEAD: 1881 — the-TAIL-ALREADY-VLM (s147: z83–z89 + finis + the-'1 8 8 1.'-spread!) → the-boundary-1880/81-before-s147 → probe-s141–s147!)",
    p224Errors.length === 0,
    p224Errors.length === 0
      ? `25 vpisov / 106-DISTINCT (vrstna-aritmetika = P223-LEAD-1:1!) / 23 hiš (h13-×2 + h68-×2-DVOJČKI!) · MEJA-1881/82-s147/s148-63.-POTRDITEV ('Anni-1-8-8-1.'-RAZPETA!) · S160-DEZEMBER-KOREKCIJA (z96-labela-VIZUALNO!-Dez-31-×4!) + Z71-OKT-KOREKCIJA · FOLIACIJA-TRI-SERIJE (sken−6 + LUKNJA-'158' + sken−5!) · S149-z16-DUPLIKAT (P222-PARALELA!) · Z55-ZAP-KOREKCIJA · hišne-VIZUALNE-×6 · pripisi-MMK-×6 · mreže-PEZDIRC-×4 + KLOBUČAR-×3! · **LINIJA-4/15!** · vitals 1742 · 04104 90`
      : p224Errors.join("; "),
  );
  }

'''
src = src.replace(ANCHOR, BLOCK + ANCHOR, 1)
src = src.replace("HOUSE_VITALS.length !== 1717", "HOUSE_VITALS.length !== 1742")
# P223-block 04104-total: 65 → 90 (zdaj vključuje 1882!)
src = src.replace('if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length !== 65)',
                  'if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length !== 90)')
src = src.replace('p223Errors.push(`bloki 04104 ≠ 65 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length} — P221: 25 × 1885; P222: + 21 × 1884; P223: + 19 × 1883 = 65!)`)',
                  'p223Errors.push(`bloki 04104 ≠ 90 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length} — P221: 25 × 1885; P222: + 21 × 1884; P223: + 19 × 1883; P224: + 25 × 1882 = 90!)`)')
# yearset-04104: {1883,1884,1885} → {1882,1883,1884,1885} (v P223-bloku!)
src = src.replace('if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)\n    p223Errors.push("04104-bloki izven {1883, 1884, 1885} (predzgodovina-3/15: 1883–1885-do-P224!)");',
                  'if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)\n    p223Errors.push("04104-bloki izven {1882, 1883, 1884, 1885} (predzgodovina-4/15: 1882–1885-do-P225!)");')
QA.write_text(src, encoding="utf-8")
print(f"qa-parish: 1742×{src.count('HOUSE_VITALS.length !== 1742')} · qa-p224×{src.count('qa-p224-parish-baptism-1882-04104')} · yearset-{src.count('(h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885')}")

# --- skripte + verifierji patch (1717→1742) ---
files = sorted(set(glob.glob(str(ROOT / "scripts/**/*.py"), recursive=True) + glob.glob(str(ROOT / "scripts/**/*.mjs"), recursive=True)))
skip = ("p224_",)
patched = 0
for f in files:
    if any(s2 in f for s2 in skip): continue
    t = Path(f).read_text(encoding="utf-8")
    if "1717" not in t: continue
    o = t
    t = t.replace("1717", "1742")
    if t != o:
        Path(f).write_text(t, encoding="utf-8"); patched += 1
print(f"skripte-patched: {patched}")

vpatched = 0
for f in sorted(ROOT.glob("scripts/p19*.py")) + sorted(ROOT.glob("scripts/p2[0-2][0-9]_parish*.py")):
    if "p224" in f.name: continue
    t = f.read_text(encoding="utf-8"); o = t
    for a, b in [("vitals == 1717", "vitals == 1742"), ("vitalsTotal == 1717", "vitalsTotal == 1742"),
                 ('vitalsTotal"] == 1717', 'vitalsTotal"] == 1742'),
                 ('"vitalsTotal": 1717', '"vitalsTotal": 1742'),
                 ('\\"vitalsTotal\\": 1717', '\\"vitalsTotal\\": 1742'),
                 ('!== 1717"', '!== 1742"'),
                 ("1717-številcev", "1742-številcev"),
                 ("vitals-števec-1717", "vitals-števec-1742"), ("vitals-1717", "vitals-1742")]:
        t = t.replace(a, b)
    if t != o:
        f.write_text(t, encoding="utf-8"); vpatched += 1
print(f"verifierji-patched: {vpatched}")

# p191 EXPECTED_CORPUS: 04104 65 → 90
p191 = ROOT / "scripts/p191_pt_luknja_final.py"
t = p191.read_text(encoding="utf-8"); o = t
t = t.replace('"04104": 65}', '"04104": 90}')
t = t.replace("# POSODABLJENO P223: + krstna-04104 = 65 (25×1885-P221 + 21×1884-P222 + 19×1883-P223!)",
              "# POSODABLJENO P224: + krstna-04104 = 90 (25×1885-P221 + 21×1884-P222 + 19×1883-P223 + 25×1882-P224!)")
if t != o: p191.write_text(t, encoding="utf-8"); print("p191-EXPECTED_CORPUS-patched (90)")

ptp = ROOT / "research/issue17/pt-luknja-18-final.json"
pt = json.loads(ptp.read_text(encoding="utf-8"))
pt["corpus"]["vitalsTotal"] = 1742
pt["corpus"]["byBook"]["04104"] = 90
pt["corpus"]["housesNote"] = (pt["corpus"].get("housesNote") or "") + " | P224: +25-blokov-1882-krstna-04104-4/15 (vitals 1717→1742; 04104 65→90; 106-DISTINCT = P223-LEAD-'z88–z106'-1:1 + 25-GRIBLJE/23-hiš = TIE-REKORD-P221 + MEJA-1881/82-s147/s148-63.-POTRDITEV ('Anni-1-8-8-1.'-RAZPETA!) + S160-DEZEMBER-KOREKCIJA (z96-'DECEMBER'-labela-VIZUALNO!-Dez-31-×4!) + Z71-OKT-KOREKCIJA + FOLIACIJA-TRI-SERIJE (sken−6 + LUKNJA-'158'!) + S149-z16-DUPLIKAT + Z55-ZAP-KOREKCIJA + hišne-VIZUALNE-×6 + pripisi-MMK-×6 + mreže-PEZDIRC-×4 + KLOBUČAR-×3)"
ptp.write_text(json.dumps(pt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"pt-luknja: {pt['corpus']['vitalsTotal']}/{pt['corpus']['byBook']['04104']}")
