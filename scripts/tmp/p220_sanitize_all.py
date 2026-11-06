#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P220 — INSERT qa-p220 + sanitizacija (1642→1677, 423→433, yearset +1857, guard-1857-KOMPLET) + verifier-patch + pt-luknja."""
from pathlib import Path
import glob, json, re

ROOT = Path("/home/z/my-project")
QA = ROOT / "src/lib/qa-parish.ts"
src = QA.read_text(encoding="utf-8")
ANCHOR = "  // ——— qa-p219: MRLIŠKA PREDZGODOVINA 04106 — leto 1858 = 28. leto PREDZGODOVINSKE"
assert src.count(ANCHOR) == 1 and "qa-p220-parish-death-1857-04106" not in src
BLOCK = '''
  // ——— qa-p220: MRLIŠKA PREDZGODOVINA 04106 — leto 1857 = 29/29 — ZADNJE leto knjige —
  //      PREDZGODOVINSKA LINIJA KONČANA! (issue #18). 1857 = 73 vpisov-kronološko
  //      (ŠTEVJE-IZ-VRSTIC-22.× — WRITTEN-1–31 + 33–74 = 73-ČISTO + ★★★ LUKNJA-32
  //      pisarski-preskok-3.-instance-po-LUKNJA-92!) / 10-GRIBLJE / 9 hiš (h36-×2-KRIŽAN!
  //      z71-hiša-NEBERLJIVA-3×!) + ★★★ KNJIGA-START: s1-NASLOVNI-LIST-'Tom. III' +
  //      s2-'18 57'-RAZPETA-letnica-glava (rokopisna-nadčrtana!) + restart-z1 —
  //      MEJA-1856/57-NE-OBSTAJA! + ★★★ OKTOBER-×0 (z65-Sep-24/26 → z66-Nov-9/11!) +
  //      ★★★ SCARLATINA?-klaster-×13–14 ('Rušfieber'-×6–7 + 'Amigdilitis[?]'-×7!) +
  //      ★★★ 8-od-10-hiš-PRVI-vpis-v-korpusu! + ★★★ z74-duhovnik-'J.-Knauš/Kranz[?]' —
  //      MOŽEN-ZGODNJI-Knavs-podpis (KOREKCIJA-P219-lead!) + MEJA-1857/58-s7-re-križ =
  //      59.-POTRDITEV! + 2-POPRAVKI-PISARJA ('1867'→1857 + '1858'→1857!) + pag =
  //      sken−1-SVINČNIK-FOLIACIJA (konvencijski-prehod!). Dokaz:
  //      parish-death-1857-04106.json; skripte p220.
  {
  const p220Errors: string[] = [];
  const p220Death = HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && h.year === 1857);
  if (p220Death.length !== 10)
    p220Errors.push(`bloki 1857 (04106) ≠ 10 (${p220Death.length} — 10 Griblje-vpisov / 9 hiš / 73 kronoloških = 73-written + LUKNJA-32!)`);
  const p220Houses = p220Death.map((h) => h.houseNo);
  if (p220Houses.join(",") !== "60,64,52,13,36,31,48,65,[?],36")
    p220Errors.push(`hiše 1857 neujemane — najdeno: ${p220Houses.join(",")}`);
  if (HOUSE_VITALS.length !== 1677)
    p220Errors.push(`HOUSE_VITALS ≠ 1677 (${HOUSE_VITALS.length} — P219: 1642; P220: + 10 blokov 1857-04106 = 1677!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length !== 433)
    p220Errors.push(`bloki 04106 ≠ 433 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length} — P220: 10 × 1857 + P219: 10 × 1858 + P218: 23 × 1859 + P217: 9 × 1860 + P216: 10 × 1861 + P215: 9 × 1862 + P214: 7 × 1863 + P213: 17 × 1864 + P212: 13 × 1865 + P211: 13 × 1866 + P210: 20 × 1867 + P209: 13 × 1868 + P208: 14 × 1869 + P207: 12 × 1870 + P206: 11 × 1871 + P205: 17 × 1872 + P204: 38 × 1873 + P203: 21 × 1874 + P202: 10 × 1875 + P201: 20 × 1876 + P200: 8 × 1877 + P199: 23 × 1878 + P198: 9 × 1879 + P197: 13 × 1880 + P192: 16 × 1885 + P193: 21 × 1884 + P194: 11 × 1883 + P195: 16 × 1882 + P196: 19 × 1881 = 433!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && (h.year ?? 0) !== 1857 && (h.year ?? 0) !== 1858 && (h.year ?? 0) !== 1859 && (h.year ?? 0) !== 1860 && (h.year ?? 0) !== 1861 && (h.year ?? 0) !== 1862 && (h.year ?? 0) !== 1863 && (h.year ?? 0) !== 1864 && (h.year ?? 0) !== 1865 && (h.year ?? 0) !== 1866 && (h.year ?? 0) !== 1867 && (h.year ?? 0) !== 1868 && (h.year ?? 0) !== 1869 && (h.year ?? 0) !== 1870 && (h.year ?? 0) !== 1871 && (h.year ?? 0) !== 1872 && (h.year ?? 0) !== 1873 && (h.year ?? 0) !== 1874 && (h.year ?? 0) !== 1875 && (h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)
    p220Errors.push("04106-bloki izven {1857, ..., 1885} (predzgodovina-KONČANA: 1857–1885-KOMPLET-29-let!)");
  if (!p220Death.some((h) => h.houseNo === "36" && h.whatSi.includes("KRIŽAN") && h.whatSi.includes("h36-KRIŽAN-×2")))
    p220Errors.push("★★★ h36-KRIŽAN-×2 (z50-otrok + z74-TAIL!) ni označena");
  if (!p220Death.some((h) => h.houseNo === "65" && h.whatSi.includes("PRVI-vpis-h65-MILEK-hiša")))
    p220Errors.push("★★★ z61-PRVI-vpis-h65-MILEK-hiša ni označena");
  if (!p220Death.some((h) => h.houseNo === "[?]" && h.whatSi.includes("NEBERLJIVA-3×") && h.whatSi.includes("STAROST-DUEL")))
    p220Errors.push("★★★ z71-hiša-NEBERLJIVA-3× + STAROST-DUEL ni označena");
  if (!p220Death.some((h) => h.houseNo === "36" && h.whatSi.includes("MOŽEN-ZGODNJI-Knavs-podpis")))
    p220Errors.push("★★★ z74-MOŽEN-ZGODNJI-Knavs-podpis (KOREKCIJA-P219-lead!) ni označena");
  if (!p220Death.some((h) => h.houseNo === "13" && h.whatSi.includes("SCARLATINA?-klaster")))
    p220Errors.push("★★★ z45-h13-SCARLATINA?-klaster ni označena");
  push(
    "qa-p220-parish-death-1857-04106",
    "P220: ŽUPNIJA PODZEMELJ — MRLIŠKA PREDZGODOVINA 04106, LETO 1857 = 29/29 — ZADNJE LETO KNJIGE — PREDZGODOVINSKA LINIJA KONČANA! (issue #18): okvir — s001–s007 (7 svežih 2×-md5-NEODVISNA-PRENOSA-7/7 — SANDI-REZET-RESTART!; s1 = NASLOVNI-LIST-'Tom. III'-'Sterb-Buch'-'Podzemelj'-0-vrstic!) + pag = sken−1-SVINČNIK-FOLIACIJA-ARHIVARJA (dokumentirano-3×: s4='3'/s5='4'/s7='6'! — KONVENCIJSKI-PREHOD: sken−5-NEMOŽEN-za-s1–s5!) + **★★★ KNJIGA-04106-SE-ZAČNE-1857: s1-NASLOVNI-LIST + s2-RAZPRTA-NASLOVNA-LISTA ('Sterb-'/'Buch.'-fraktura!) + '18 57'-RAZPETA-letnica-glava (rokopisna-nadčrtana — P214-TIP-sorodna-razpeta-cifra!) + restart-z1 — MEJA-1856/57-NE-OBSTAJA ('18 57'-glava = KNJIGA-START-marker!)** + **★★★ 73-VPIISOV-KRONOLOŠKO-ŠTEVJE-IZ-VRSTIC-22.×** (WRITTEN-1–31 + 33–74 = 73-ČISTO + **★★★ LUKNJA-32 — pisarski-preskok-3.-instance-v-knjigi-po-LUKNJA-92-1859!** — s3-ordinalni-stolpec-KONČA-z-31 (15-ordinalov!) + s3-dno-RAZPRAZNO (y0.925–1.0-brez-vsebine — 3-kropi!) + s4-ZAČNE-z-33 (Juni-21./23.!); kronološki-seam-z31-Juni-21/22 → z33-Juni-21/23-GLADAK! — X-open: morda-32-obrezan-na-dnu-s3!; vrstna-aritmetika 16+15+13+13+14+2 = 73!) + **★★★ OKTOBER-1857-×0-v-celotni-župniji (z65-Sep-24/26 → z66-Nov-9/11 — 15-dnevna-luknja — edini-mesec-×0!)** + **★★★ SCARLATINA?-EPIDEMIJA-klaster-×13–14 ('Rušfieber/Rušenfleck'-×6–7 (July-24→Aug-12) + 'Amigdilitis[?]'-garble-×7 (s5: z48–z57) — isti-garble-družina?-2.-val?-X-open — šrlaha-hipoteza! — 1-GRIBLJE-v-klasterju (z45-Rušfieber!))** + **★★★ 10-GRIBLJE / 9 hiš (h36-×2-KRIŽAN: z50-Georg/Jurij-Križan[?]-4J (Križan-2×-križ-vs-Krajncan-page-DUEL!) + z74-Marijan-Križan[?]-73J-TAIL (4×-garble!) — KRIŽAN-hiša-2-GENERACIJI!; z71-hiša-NEBERLJIVA-3× (page+pas-krop+hi-krop — edini-primer-1857!))** + **★★★ 8-od-10-hiš-dobi-PRVI-vpis-v-celotnem-korpusu (h13! h31! h36! h48! h52! h60?/66-DUEL! h64! h65-MILEK-hiša! — ker-je-1857-1.-leto-knjige!)** + **★★★ z71-STAROST-DUEL (14-let[page]-vs-1-mesec-1-dan[hi-krop]! — dojenček-hipoteza: Wasserkopf + 'ganz-außerehelich'-NEZAKONSKI! — X-open!) + ime-duel (Martin-vs-Max!) + TRI-stan-garble** + **★★★ z74-TAIL-duhovnik-'J.-Knauš/Kranz[?]' — MOŽEN-ZGODNJI-Knavs-podpis (KOREKCIJA-P219-lead: Knavs-morda-ŽE-DEC-1857! — X-open!)** + **★★★ MEJA-1857/58 = s7 (P219-potrjeno + re-križ-P220-arb_s7_meja-1:1: TAIL-z73–z74 + VSOTNA-'1 8 5 [8]'-RAZPETE-P214-TIP-3.-INSTANCE ('1-8' + '5'-vidno-tudi-v-P220-kropu!) + rokopisna-'Jänner-1858'-glava + restart-z1–z11 + NEŠTEVILČENA!) = 59.-POTRDITEV-invariante!** + 2-POPRAVKI-PISARJA (s3-'1867'-prečrtano→1857-ob-vrsti-30/31 + s4-z33-'1858'-prečrtano→1857!) + z73-Gradac-KOREKCIJA-P219 (Martin-Kuncel/Kunstel/Kunovlt-TRI-DUEL-26J[2×-fresh!]-vs-86J[P219]-vs-'Amalia-Rundel'[P219]-zavrnjena!) + z58-honesty-MAX (hiša-TRI-DUEL-48/43/145 + ime-TRI-DUEL-Stamcar/Straus/Maria + starost-DUEL-66/Kind!) + hišne-niti (h13-DRAGOŠ-PRVI! + h31-PRVI! + h36-KRIŽAN-×2! + h48-PRVI! + h52-PRVI-Peskar! + h60-TOMINC-X-open! + h64-PRVI-Verbičar! + h65-MILEK-PRVI!); **★★★ 10-GRIBLJE / 9 hiš** + starost-'0'-ni (ekstremi-3-tedne-z56-→-73-J-z74!) + meseci-GRIBLJE-luknje-×6 (Mär/Apr/Mai/Juni/July/Nov-×0! — rekord!) + otroška-umrljivost-30%-3/10 (+z71-duel-→-40%!) + duhovniki-1857 ('Ladergal'-garble-klaster-DOMINANTA-8-variant! + 'Joann-Skubic-Pav.' + 'Johann-Verbič-cooperator' + 'Fr.-Xaveryal[?]' + 'Thom.-Ladargal-Cop.[?]' + 'J.-Knauš/Kranz[?]'!); **10 NOVIH BLOKOV parish.ts: vitals 1642 → 1677 · 04106 = 423 → 433 · 04894 = 520-NESPREMENJENO**; skripte p220 (fetch-2×-md5-7/7 + read-×7 + traki-24 + krop-29 + build-entries + build-proof) + qa-p220 (220. kontrola!) + dokaz parish-death-1857-04106.json (73 entries: 10-Griblje + 63-druge!) + pt-luknja-433/1677; **★★★ PREDZGODOVINA-LINIJA-04106-KONČANA-29/29-LET — knjiga-POPOLNOTA-prepisana (1857–1885 = 433-Griblje-vpisov!)** (P221-LEAD: krstna-04104-PREDZGODOVINA (1871–1885, 15-let — ×200-skenov-čaka!) — pričakovani-start-1885 (1/15) po-descending-vzorca!)",
    "P220: THE PARISH OF PODZEMELJ — THE DEATH-REGISTER-PREHISTORY 04106, THE YEAR 1857 = 29/29 — THE LAST YEAR OF THE BOOK — THE PREHISTORY LINE COMPLETE! (issue #18): the-frame (s001–s007 — 7 fresh 2×-md5-INDEPENDENT-DOWNLOADS-7/7 — SANDBOX-RESET-RESTART!; s1 = the-TITLE-PAGE-'Tom. III'-'Sterb-Buch'-'Podzemelj'-0-rows!) + pag = scan−1-THE-ARCHIVIST'S-PENCIL-FOLIATION (documented-3×: s4='3'/s5='4'/s7='6'! — the-CONVENTION-SWITCH: scan−5-IMPOSSIBLE-for-s1–s5!) + **★★★ THE-BOOK-04106-BEGINS-1857: s1-TITLE-PAGE + s2-THE-SPREAD-TITLE-PAGE ('Sterb-'/'Buch.'-fraktur!) + the-'18 57'-SPREAD-YEAR-HEADER (handwritten-underlined — P214-TYPE-related-spread-digits!) + restart-z1 — THE-1856/57-BOUNDARY-DOES-NOT-EXIST (the-'18 57'-header = the-BOOK-START-marker!)** + **★★★ 73-ENTRIES-CHRONOLOGICAL-ROW-COUNTING-22nd-×** (WRITTEN-1–31 + 33–74 = 73-CLEAN + **★★★ THE-GAP-32 — the-scribe's-skip-3rd-instance-after-the-GAP-92-1859!** — s3-ordinal-column-ENDS-at-31 (15-ordinals!) + s3-bottom-EMPTY (y0.925–1.0-no-content — 3-crops!) + s4-STARTS-at-33 (Juni-21./23.!); the-chronological-seam-z31-Juni-21/22 → z33-Juni-21/23-SMOOTH! — X-open: maybe-32-cut-at-the-s3-bottom!; the-row-arithmetic 16+15+13+13+14+2 = 73!) + **★★★ OCTOBER-1857-×0-in-the-whole-parish (z65-Sep-24/26 → z66-Nov-9/11 — the-15-day-gap — the-only-×0-month!)** + **★★★ THE-SCARLATINA?-EPIDEMIC-CLUSTER-×13–14 ('Rušfieber/Rušenfleck'-×6–7 (July-24→Aug-12) + 'Amigdilitis[?]'-garble-×7 (s5: z48–z57) — the-same-garble-family?-2nd-wave?-X-open — the-scarlet-fever-hypothesis! — 1-GRIBLJE-in-the-cluster (z45-Rušfieber!))** + **★★★ 10-GRIBLJE / 9 houses (h36-×2-KRIŽAN: z50-Georg/Jurij-Križan[?]-4J (Križan-2×-cross-vs-Krajncan-page-DUEL!) + z74-Marijan-Križan[?]-73J-TAIL (4×-garble!) — the-KRIŽAN-house-2-GENERATIONS!; z71-house-UNREADABLE-3× (page+strip-crop+hi-crop — the-only-case-1857!))** + **★★★ 8-of-10-houses-get-their-FIRST-corpus-entry (h13! h31! h36! h48! h52! h60?/66-DUEL! h64! h65-MILEK-house! — because-1857-is-the-book's-1st-year!)** + **★★★ z71-THE-AGE-DUEL (14-years[page]-vs-1-month-1-day[hi-crop]! — the-infant-hypothesis: Wasserkopf + 'ganz-außerehelich'-ILLEGITIMATE! — X-open!) + the-name-duel (Martin-vs-Max!) + the-TRI-stan-garble** + **★★★ z74-TAIL-priest-'J.-Knauš/Kranz[?]' — the-POSSIBLE-EARLY-Knavs-signature (the-P219-lead-CORRECTION: Knavs-maybe-ALREADY-DEC-1857! — X-open!)** + **★★★ THE-1857/58-BOUNDARY = s7 (P219-confirmed + re-cross-P220-arb_s7_meja-1:1: the-TAIL-z73–z74 + the-SUM-ROW-'1 8 5 [8]'-SPREAD-DIGITS-P214-TYPE-3rd-INSTANCE ('1-8' + '5'-visible-also-in-the-P220-crop!) + the-handwritten-'Jänner-1858'-header + restart-z1–z11 + the-UNNUMBERED!) = the-59th-CONFIRMATION!** + 2-SCRIBE-CORRECTIONS (s3-'1867'-crossed→1857-near-row-30/31 + s4-z33-'1858'-crossed→1857!) + z73-Gradac-P219-CORRECTION (Martin-Kuncel/Kunstel/Kunovlt-TRI-DUEL-26J[2×-fresh!]-vs-86J[P219]-vs-'Amalia-Rundel'[P219]-rejected!) + z58-honesty-MAX (house-TRI-DUEL-48/43/145 + name-TRI-DUEL-Stamcar/Straus/Maria + age-DUEL-66/Kind!) + house-threads (h13-DRAGOŠ-FIRST! + h31-FIRST! + h36-KRIŽAN-×2! + h48-FIRST! + h52-FIRST-Peskar! + h60-TOMINC-X-open! + h64-FIRST-Verbičar! + h65-MILEK-FIRST!); **★★★ 10-GRIBLJE / 9 houses** + no-'0'-age (extremes-3-weeks-z56-→-73-J-z74!) + the-Griblje-month-gaps-×6 (Mär/Apr/Mai/Juni/July/Nov-×0! — the-record!) + child-mortality-30%-3/10 (+z71-duel-→-40%!) + the-1857-priests (the-'Ladergal'-garble-cluster-DOMINANCE-8-variants! + 'Joann-Skubic-Pav.' + 'Johann-Verbič-cooperator' + 'Fr.-Xaveryal[?]' + 'Thom.-Ladargal-Cop.[?]' + 'J.-Knauš/Kranz[?]'!); **10 NEW BLOCKS: the vitals 1642 → 1677 · the 04106 = 423 → 433 · the 04894 = 520-UNCHANGED**; the scripts p220 (fetch-2×-md5-7/7 + read-×7 + traki-24 + krop-29 + build-entries + build-proof) + qa-p220 (the 220th check!) + the evidence parish-death-1857-04106.json (73 entries: 10-Griblje + 63-others!) + the pt-gap-433/1677; **★★★ THE-PREHISTORY-LINE-04106-COMPLETE-29/29-YEARS — the-book-FULLY-transcribed (1857–1885 = 433-Griblje-entries!)** (the P221-LEAD: the-baptism-04104-PREHISTORY (1871–1885, 15-years — ×200-scans-waiting!) — the-expected-start-1885 (1/15) by-the-descending-pattern!)",
    p220Errors.length === 0,
    p220Errors.length === 0
      ? `10 vpisov / 73 kronoloških (73-written-ČISTO + LUKNJA-32!) / 9 hiš (h36-×2-KRIŽAN! z71-hiša-NEBERLJIVA-3×!) · KNJIGA-START-'18 57'-RAZPETA-GLAVA · OKTOBER-×0 · SCARLATINA?-klaster-×13–14 · 8-od-10-hiš-PRVI-vpis-v-korpusu · z74-'Knauš/Kranz[?]'-MOŽEN-ZGODNJI-Knavs · MEJA-s7-re-križ-59.-POTRDITEV · **PREDZGODOVINA-KONČANA-29/29!** · vitals 1677 · 04106 433 · 04894 520`
      : p220Errors.join("; "),
  );
  }

'''
src = src.replace(ANCHOR, BLOCK + ANCHOR, 1)
src = src.replace("HOUSE_VITALS.length !== 1642", "HOUSE_VITALS.length !== 1677")
src = src.replace('04106").length !== 423', '04106").length !== 433')
# year-guards: dodaj 1857 v izjeme (vse "(h.year ?? 0) !== 1858 &&" za 04106-filtre)
src = src.replace('(h.bookSignature === "04106" && (h.year ?? 0) !== 1858 &&', '(h.bookSignature === "04106" && (h.year ?? 0) !== 1857 && (h.year ?? 0) !== 1858 &&')
src = src.replace("1857 še nebran — P220-LEAD!", "predzgodovina-KONČANA: 1857–1885-KOMPLET-29-let! (P220!)")
src = src.replace("1857 še nebran!", "predzgodovina-KONČANA-1857–1885! (P220!)")
src = src.replace("izven {1858, 1859, 1860,", "izven {1857, 1858, 1859, 1860,")
src = src.replace("izven {1858, 1859, 1861, ..., 1885}", "izven {1857, 1858, 1859, 1861, ..., 1885}")
src = src.replace("vitals 1642 · 04106 423 · 04894 520", "vitals 1677 · 04106 433 · 04894 520")
src = src.replace("pt-luknja-423/1642", "pt-luknja-433/1677")
QA.write_text(src, encoding="utf-8")
print(f"qa-parish: 1677×{src.count('HOUSE_VITALS.length !== 1677')} · 433×{src.count('04106\").length !== 433')} · 1857-guard×{src.count('(h.year ?? 0) !== 1857')}")

files = sorted(set(glob.glob(str(ROOT / "scripts/**/*.py"), recursive=True) + glob.glob(str(ROOT / "scripts/**/*.mjs"), recursive=True)))
skip = ("p59_ps_blatt_headers", "p200_", "p201_", "p202_", "p203_", "p204_", "p205_", "p206_", "p207_", "p208_", "p210_", "p211_", "p212_", "p213_", "p214_", "p215_", "p216_", "p217_", "p218_", "p219_", "p220_")
patched = 0
for f in files:
    if any(s2 in f for s2 in skip): continue
    t = Path(f).read_text(encoding="utf-8")
    if "1642" not in t and "== 423" not in t: continue
    o = t
    t = t.replace("1642", "1677").replace('.get("04106") == 423', '.get("04106") == 433').replace("04106 == 423", "04106 == 433").replace("04106==423", "04106==433").replace("skupaj == 423", "skupaj == 433").replace('"04106") == 423', '"04106") == 433').replace("(04106, 423)", "(04106, 433)").replace("== 423,", "== 433,")
    if t != o:
        Path(f).write_text(t, encoding="utf-8"); patched += 1
print(f"skripte-patched: {patched}")

vpatched = 0
for f in sorted(ROOT.glob("scripts/p19*.py")) + sorted(ROOT.glob("scripts/p2[0-2][0-9]_parish*.py")):
    if "p220" in f.name: continue
    t = f.read_text(encoding="utf-8"); o = t
    for a, b in [("04106 == 423", "04106 == 433"), ("04106==423", "04106==433"),
                 ('04106": 423', '04106": 433'), ("skupaj == 423", "skupaj == 433"),
                 ('"04106") == 423', '"04106") == 433'), ("(04106, 423)", "(04106, 433)"),
                 ('byBook"]["04106"] == 423', 'byBook"]["04106"] == 433'),
                 ('["04106"] == 423', '["04106"] == 433'),
                 ("vitals == 1642", "vitals == 1677"), ("vitalsTotal == 1642", "vitalsTotal == 1677"),
                 ('vitalsTotal"] == 1642', 'vitalsTotal"] == 1677'),
                 ('"vitalsTotal": 1642', '"vitalsTotal": 1677'),
                 ('\\"vitalsTotal\\": 1642', '\\"vitalsTotal\\": 1677'),
                 ('!== 1642"', '!== 1677"'),
                 ("1642-številcev", "1677-številcev"),
                 ("vitals-števec-1642", "vitals-števec-1677"), ("vitals-1642", "vitals-1677")]:
        t = t.replace(a, b)
    t = t.replace('set(izven) == {"1858", "1859"', 'set(izven) == {"1857", "1858", "1859"')
    t = t.replace('set(izven) == {"1859"', 'set(izven) == {"1857", "1858", "1859"')
    t = t.replace('",".join(leta) == "1858,1859,1860', '",".join(leta) == "1857,1858,1859,1860')
    t = t.replace('join(leta) == "1858,1859,1860,1861,1862,1863,1864,1865,1866,1867,1868,1869,1870,1871,1872,1873,1874,1875,1876,1877,1878,1879,1880,1881,1882,1883,1884,1885"',
                  'join(leta) == "1857,1858,1859,1860,1861,1862,1863,1864,1865,1866,1867,1868,1869,1870,1871,1872,1873,1874,1875,1876,1877,1878,1879,1880,1881,1882,1883,1884,1885"')
    t = t.replace("1857 še nebran!", "predzgodovina-KONČANA! (P220)")
    if t != o:
        f.write_text(t, encoding="utf-8"); vpatched += 1
print(f"verifierji-patched: {vpatched}")

ptp = ROOT / "research/issue17/pt-luknja-18-final.json"
pt = json.loads(ptp.read_text(encoding="utf-8"))
pt["corpus"]["vitalsTotal"] = 1677
pt["corpus"]["byBook"]["04106"] = 433
pt["corpus"]["housesNote"] = (pt["corpus"].get("housesNote") or "") + " | P220: +10-blokov-1857 (04106 423→433, vitals 1642→1677, ŠTEVJE-IZ-VRSTIC-22.×-73-kronološko (73-written + LUKNJA-32!) + 10-GRIBLJE/9-hiš (h36-×2-KRIŽAN + z71-hiša-NEBERLJIVA-3×!) + KNJIGA-START-'18 57'-RAZPETA-GLAVA + OKTOBER-×0 + SCARLATINA?-klaster-×13–14 + 8-od-10-hiš-PRVI-vpis-v-korpusu + z74-'Knauš/Kranz[?]'-MOŽEN-ZGODNJI-Knavs-podpis! — ★ PREDZGODOVINA-LINIJA-04106-KONČANA-29/29!)"
ptp.write_text(json.dumps(pt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"pt-luknja: {pt['corpus']['vitalsTotal']}/{pt['corpus']['byBook']['04106']}")
