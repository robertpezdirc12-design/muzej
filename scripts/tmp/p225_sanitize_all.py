#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P225 — INSERT qa-p225 + sanitizacija (1742→1853, 04104=90→107, yearset-04104-{1881..1885}, pt-luknja)."""
from pathlib import Path
import glob, json, re

ROOT = Path("/home/z/my-project")
QA = ROOT / "src/lib/qa-parish.ts"
src = QA.read_text(encoding="utf-8")
ANCHOR = "  // ——— qa-p224: KRSTNA PREDZGODOVINA 04104 — leto 1882 = 4/15"
assert src.count(ANCHOR) == 1 and "qa-p225-parish-baptism-1881-04104" not in src

BLOCK = '''
  // ——— qa-p225: KRSTNA PREDZGODOVINA 04104 — leto 1881 = 5/15
  //      (P224: 1882 = 4/15!). 1881 = 89 vpisov-DISTINCT (vrstna-aritmetika
  //      7+7+7+7+7+7+8+8+8+8+8+7 = 89 = P224-LEAD-'z83–z89-tail'-1:1-INVARIANTA! —
  //      zap-stolpci-12/12-ČISTO!) / 17-GRIBLJE / 17-hiš-VSE-DISTINCT + ★★★ MEJA-1880/81-
  //      s135/s136 (TAIL-1880-z116–z122 + 'Finis' + 'Jahr 18 80.'-BREZ-VSOTNE! +
  //      'Jahr 1881.'-glava + RESTART-z1-NA-DAN-1.-1.-JÄNNER-GRIBLJE-h55-Agnes!-4.-GRIBLJE-
  //      restart-z1!) = 64.-POTRDITEV + ★★★ FOLIACIJA-'sken−6'-13/13-SEKVENČNO (129–141-
  //      brez-luknje!-s143/s145-sandwich-argument!) + ★★★ PEZDIRC-×9-NOV-REKORD-LETA (z1-matec!
  //      z40-matec! z42-oče-2×! z52-botra! z55-matec+boter-DVOJNI! z57-oče-2×! z66-oče-X-open!
  //      z78-matec-Perdijc! z81-oče! + ×3-ne-Griblje = ×12!) + KRIŽAN-×6 + BRODARIČ-×6 +
  //      ★★★ 2-POROKE-PRIPISA-'VNALILA' (z52-1959-→-Ožbolt! z57-1958-→-Griblje!) + ★★★ Z48-
  //      BOTRA-PRAZNA-ANOMALIJA (1.-v-krstni-liniji!) + ★★★ Z66-NEZAKONSKI ('ynb.'!) +
  //      Z14-MESEC-DUEL-REŠEN (April-labela-VIZUALNO!-page-'31-März'-ZAVRNJENO!) +
  //      pripisi-MMK-†-×2 (z30-†1931! z43-†1960-Črnomelj!) + meseci-Griblje J1+A1+Juni2+Juli1+
  //      Aug4+Sep2+Okt3+Nov3 (Feber/März/Dez-×0!). Dokaz: parish-baptism-1881-04104.json; skripte p225.
  {
  const p225Errors: string[] = [];
  const p225Bapt = HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && h.year === 1881);
  if (p225Bapt.length !== 17)
    p225Errors.push(`bloki 1881 (04104) ≠ 17 (${p225Bapt.length} — 17 Griblje-vpisov / 17 hiš-VSE-DISTINCT / 89-DISTINCT = P224-LEAD-1:1!)`);
  if (HOUSE_VITALS.length !== 1853)
    p225Errors.push(`HOUSE_VITALS ≠ 1853 (${HOUSE_VITALS.length} — P224: 1742; P225: + 17 blokov 1881-04104 = 1853!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length !== 107)
    p225Errors.push(`bloki 04104 ≠ 107 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length} — P224: 90; P225: + 17 × 1881 = 107!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)
    p225Errors.push("04104-bloki izven {1881, 1882, 1883, 1884, 1885} (predzgodovina-5/15: 1881–1885-do-P226!)");
  if (!p225Bapt.some((h) => h.whatSi.includes("RESTART-z1-NA-DAN-1.-1.-JÄNNER-GRIBLJE-h55") || h.whatSi.includes("64.-POTRDITEV")))
    p225Errors.push("★★★ MEJA-1880/81-s135/s136 ('Finis' + 'Jahr 1881.' + RESTART-z1-GRIBLJE-h55!) ni označena");
  if (!p225Bapt.some((h) => h.houseNo === "55" && h.whatSi.includes("PEZDIRC-matec-nit-X-open")))
    p225Errors.push("★★★ z1-RESTART-GRIBLJE-h55 + PEZDIRC-matec (Podžirec~Pezdirec!) ni označena");
  if (p225Bapt.filter((h) => h.whatSi.includes("PEZDIRC")).length < 9)
    p225Errors.push(`★★★ PEZDIRC-×9-rekord-leta ni dosežen (${p225Bapt.filter((h) => h.whatSi.includes("PEZDIRC")).length}/9!)`);
  if (!p225Bapt.some((h) => h.houseNo === "62" && h.whatSi.includes("BOTRA-PRAZNA-ANOMALIJA")))
    p225Errors.push("★★★ z48-BOTRA-PRAZNA-ANOMALIJA (1.-v-krstni-liniji!) ni označena");
  if (!p225Bapt.some((h) => h.whatSi.includes("NEZAKONSKI-vpis")))
    p225Errors.push("★★★ z66-NEZAKONSKI-vpis (matec-'ynb.'!) ni označena");
  if (!p225Bapt.some((h) => h.whatSi.includes("Vnalila-2.9.1959") || h.whatSi.includes("Vnalila-30.3.1958")))
    p225Errors.push("★★★ 2-POROKE-PRIPISA-'VNALILA' (z52-1959! + z57-1958!) nista označena");
  if (!p225Bapt.some((h) => h.whatSi.includes("PEZDIRC-matec+boter-DVOJNI-nit")))
    p225Errors.push("★★★ z55-PEZDIRC-matec+boter-DVOJNI-nit (×2-v-vrstici!) ni označena");
  if (!p225Bapt.some((h) => h.whatSi.includes("hiša-'37'-DUEL-1:1")))
    p225Errors.push("★★★ z15-hiša-'37'-DUEL-1:1 (page-vs-krop-'34'!-KURRENT-3/4!) ni označena");
  if (!p225Bapt.some((h) => h.whatSi.includes("hiša-'49'-DUEL-1:1")))
    p225Errors.push("★★★ z40-hiša-'49'-DUEL-1:1 (page-vs-krop-'19'!) ni označena");
  if (!p225Bapt.some((h) => h.whatSi.includes("hiša-'57'-DUEL-1:1")))
    p225Errors.push("★★★ z66-hiša-'57'-DUEL-1:1 (page-vs-krop-'37'!) ni označena");
  if (!p225Bapt.some((h) => h.whatSi.includes("Umrła-11.11.1960")))
    p225Errors.push("★★★ z43-pripis-MMK-'Umrła-11.11.1960-v-Črnomelju' ni označena");
  if (!p225Bapt.some((h) => h.whatSi.includes("†-16.12.1931")))
    p225Errors.push("★★★ z30-pripis-MMK-'†-16.12.1931-[~1937-DUEL!]' ni označena");
  if (!p225Bapt.some((h) => h.whatSi.includes("DRAGOŠ-botra-nit")))
    p225Errors.push("★★★ z30-DRAGOŠ-botra-nit (2×!-P193/P220-nit!) ni označena");
  if (!p225Bapt.some((h) => h.whatSi.includes("ŽELJKO-matec+boter-nit")))
    p225Errors.push("★★★ z75-ŽELJKO-matec+boter-nit (×2-v-vrstici!-P139-nit!) ni označena");
  if (new Set(p225Bapt.map((h) => h.houseNo)).size !== p225Bapt.length)
    p225Errors.push("★★★ 17-hiš-NI-VSE-DISTINCT (duplikati!)");
  push(
    "qa-p225-parish-baptism-1881-04104",
    "P225: ŽUPNIJA PODZEMELJ — KRSTNA PREDZGODOVINA 04104, LETO 1881 = 5/15 (issue #18): okvir — s135–s147 (13 skenov; 2×-neodvisna-prenosa-md5-14/14!; s138–s144-proba + s134–s137-probe-nazaj! s145–s147-lead-ŽE-VLM-P224!) + **gola-svinčna-pag-'sken−6'-13/13-SEKVENČNO** (s135='129'/s136='130'/s137='131'/s138='132'-2:1!/s139='133'/s140='134'/s141='135'/s142='136'/s143='137'-SANDWICH!/s144='138'/s145='139'-SANDWICH!/s146='140'/s147='141'! — brez-luknje-v-1881-oknu — LUKNJA-'158'-ostaja-v-1882-oknu-s163/s164!) + **★★★ MEJA-1880/81 = s135/s136 (TAIL-1880-z116–z122-Dez-5–30-×7 + 'Finis'-beseda + 'Jahr 18 80.'-glava-BREZ-VSOTNE (razlika-1881-'Anni-1-8-8-1.'-razpeta-s147!) + s136-glava-'Jahr 1881.' + RESTART-z1-NA-DAN-1.-1.-JÄNNER-GRIBLJE-h55-Agnes — 4.-GRIBLJE-restart-z1 (PARALELA-P221-z1-1.1.-h21!-P222-z1-1.1.-h34!) = 64.-POTRDITEV-invariante! (63.-P224!)** + **★★★ 89-VPIISOV-DISTINCT — ŠTEVJE-IZ-VRSTIC-5.×-ZA-KRSTNO-LINIJO (z1–z89; vrstna-aritmetika 7+7+7+7+7+7+8+8+8+8+8+7 = 89 = P224-LEAD-'z83–z89-tail-1881'-1:1-INVARIANTA! — zap-stolpci-12/12-ČISTO-brez-duplikatov!)** + **★★★ 17-GRIBLJE / 17-hiš-VSE-DISTINCT (brez-duplikatov!-vs-25-TIE-rekord-P221/P224 + 21-P222 + 19-P223!): z1-GRIBLJE-h55-RESTART! + z15-h37-DUEL + z28-h3-KRIŽAN-×3 + z30-h38-DRAGOŠ! + z40-h49-DUEL-PEZDIRC! + z42-h20-PEZDIRC-oče! + z43-h17-†1960! + z45-h8-KLOBUČAR! + z48-h62-BOTRA-PRAZNA! + z52-h51-POROKA-1959! + z55-h63-PEZDIRC-DVOJNI! + z57-h14-POROKA-1958! + z66-h57-DUEL-NEZAKONSKI! + z71-h24-QUAD-garble! + z75-h6-ŽELJKO-×2! + z78-h22-MILEK-PEZDIRC! + z81-h42-PEZDIRC-9/9!** + **★★★ PEZDIRC-×9-NOV-REKORD-LETA (z1-matec-'Podžirec~Pezdirec'-X-open! + z40-matec-'Barbara-zab.-Pezdirc'! + z42-oče-'Peter-Pezdirc'-2×! + z52-botra-'Ana-Pezdirc'! + z55-matec-'Katharina'+boter-'Jure'-DVOJNI! + z57-oče-'Michael'-2×! + z66-oče-'Pegdire/Bedire'-X-open! + z78-matec-'Maria-Perdijc'! + z81-oče-'Georg-Perdijc'! — PLUS-ne-Griblje: z72-'Anton-Pezdirc'-Germ! + z76-'Peter-Perdijc'-Krasinec! + z79-'Michael-Perdijc'-Boršt-'in-Griblje'! = ×12-SKUPAJ!) — grafija-continuum-5-let (P221-×4/P222-×4/P223-×6/P224-×4/P225-×9!)** + KRIŽAN-×6 (z28-oče+matec+botra-×3-v-vrstici! + z52-boter + z55-oče + z75-botra + z81-matec+botra-×2!) + BRODARIČ-×6 (z40-oče! + z42-boter! + z52-matec! + z55-botra! + z66-boter! + z78-botra!) + SIMEC-×2 + DEBLIČ-×3 + ŽELJKO-×2 (z75-matec+boter!) + DRAGOŠ (z30-botra!-P193/P220!) + KLOBUČAR (z45-botra!-P224-nit!) + MILEK (z78-oče!-P224-z55-PARALELA!) + BRINC (z57-matec!-P224-z71-PARALELA!) + JAKOFČIČ-×2 (z75-oče!-P224-z89/z99-PARALELA!) + **★★★ 2-POROKE-PRIPISA-'VNALILA' (z52-'Vnalila-dne-2.9.1959-→-Ožbolt-št.6-MŽ-Griblje-1959-št.53'-+'matičar-Tonica-Mihelic'! + z57-'Vnalila-dne-30.3.1958-→-Griblje-št.[?]'! — MATIČARSKI-pripisi-o-poroki-NOVO-v-krstni-liniji!)** + **★★★ Z48-BOTRA-PRAZNA-ANOMALIJA (natisnjena-podčrtana-prazna-vrsta!-1.-v-krstni-liniji!-+oče-TRI-garble-Hure/Hmelj/Hrnč!-+ime-garble-MAX-Justina/JustynAnna/Podtynbormne!)** + **★★★ Z66-NEZAKONSKI-VPIS (edini-eksplicitni-1881-Griblje!-matec-'Maria-ynb.-Lupanič'!-oče-'Pegdire/Bedire'-PEZDIRC-X-open!-rojen-17/krsten-18!)** + **Z14-MESEC-DUEL-REŠEN (krop-s137-VIZUALNO: April-labela-z14-VIDNA-+-rojen-1/krsten-1 → APRIL-1!-page-'31-(März)'-ZAVRNJENO — P224-vzorec-krop>page!)** + z83-dan-DUEL-X-open (8-vs-9!-'December'-labela-'D-ne-N'-ZANESLJIVO!) + pripisi-MMK-†-×2 (z30-'†-16.12.1931-[~1937-DUEL!]'! + z43-'Umrła-dne-11.11.1960-v-Črnomelju'-'Črnušnjak-24.1.[?]'!) + meseci-Griblje: J1+A1+Juni2+Juli1+Aug4+Sep2+Okt3+Nov3 = 17 (Feber/März/Dez-×0!-Dez-×0 = TAIL-brez-Griblje!) + 1880 = 122-vpisov-BONUS (s135-tail-z116–z122!→P226-LEAD!) + **17 NOVIH BLOKOV parish.ts: vitals 1742 → 1853 · 04104 = 90 → 107 · 04105/04106/04894/04455-NESPREMENJENI**; skripte p225 (fetch-2×-md5-14/14 + read-×11 + krop-47 + krop2-13 + krop3/4/5-12 + build-entries + build-proof) + qa-p225 (225. kontrola!) + dokaz parish-baptism-1881-04104.json (89-DISTINCT: 17-Griblje + 72-druge! 10-anomalij/10-crossChecks/honesty-20!) + pt-luknja-107/1853; **★★★ KRSTNA-PREDZGODOVINA-LINIJA-5/15-LET!** (P226-LEAD: 1880 — TAIL-ŽE-VLM (s135: z116–z122-Dez-5–30 + Finis + 'Jahr 18 80.'!) → 1880 = 122-vpisov → MEJA-1879/80-pred-s135 → probe-s129–s135! — gola-pag-'sken−6'-pričakovana-s129='123'!)",
    "P225: THE PARISH OF PODZEMELJ — THE BAPTISM-REGISTER-PREHISTORY 04104, THE YEAR 1881 = 5/15 (issue #18): the-frame — s135–s147 (13 scans; 2×-INDEPENDENT-md5-14/14!) + the-plain-pencil-pag-'scan−6'-13/13-SEQUENTIAL (129–141-no-gap!-s143/s145-sandwich-argument!) + **★★★ THE-1880/81-BOUNDARY = s135/s136 (the-TAIL-1880-z116–z122-Dec-5–30 + the-'Finis'-word + the-'Jahr 18 80.'-header-WITHOUT-THE-SUM-ROW + the-'Jahr 1881.'-header + the-RESTART-z1-ON-DAY-1-1-JÄNNER-GRIBLJE-h55-Agnes — the-4th-GRIBLJE-restart-z1!) = the-64th-CONFIRMATION!** + **★★★ 89-ENTRIES-DISTINCT — the-ROW-COUNTING-5th-×-FOR-THE-BAPTISM-LINE (the-ROW-ARITHMETIC = 89 = the-P224-LEAD-1:1-INVARIANT!-the-zap-columns-12/12-CLEAN!)** + **★★★ 17-GRIBLJE / 17-houses-ALL-DISTINCT** + **★★★ THE-PEZDIRC-×9-NEW-RECORD-OF-THE-YEAR (×12-with-non-Griblje!-the-graph-continuum-5-years!)** + KRIŽAN-×6 + BRODARIČ-×6 + SIMEC-×2 + DEBLIČ-×3 + ŽELJKO-×2 + DRAGOŠ + KLOBUČAR + MILEK + BRINC + JAKOFČIČ-×2 + **★★★ 2-MARRIAGE-ANNOTATIONS-'VNALILA' (z52-1959! + z57-1958!-the-MATRICULAR-annotations-NEW-in-the-baptism-line!)** + **★★★ THE-Z48-EMPTY-GODPARENT-ANOMALY (the-1st-in-the-baptism-line!)** + **★★★ THE-Z66-ILLEGITIMATE-ENTRY** + the-Z14-month-DUEL-RESOLVED (April-label-VISUAL!-the-page-'31-März'-REJECTED!) + the-MMK-†-annotations-×2 (z30-†1931! + z43-†1960!) + **17 NEW BLOCKS: the vitals 1742 → 1853 · the 04104 = 90 → 107**; the scripts p225 + qa-p225 (the 225th check!) + the evidence parish-baptism-1881-04104.json (89-DISTINCT: 17-Griblje + 72-others!) + the pt-gap-107/1853; **★★★ THE-BAPTISM-PREHISTORY-LINE-5/15-YEARS!** (the P226-LEAD: 1880 — the-TAIL-ALREADY-VLM (s135: z116–z122 + Finis!) → 1880 = 122-entries → the-boundary-1879/80-before-s135 → probe-s129–s135!)",
    p225Errors.length === 0,
    p225Errors.length === 0
      ? `17 vpisov / 89-DISTINCT (vrstna-aritmetika = P224-LEAD-1:1!) / 17-hiš-VSE-DISTINCT · MEJA-1880/81-s135/s136-64.-POTRDITEV (RESTART-z1-GRIBLJE-h55-'Finis'-BREZ-VSOTNE!) · FOLIACIJA-sken−6-13/13-SEKVENČNO (129–141!-sandwich-s143/s145!) · PEZDIRC-×9-REKORD-LETA (×12-skupaj!) · 2-POROKE-'VNALILA' (z52 + z57!) · Z48-BOTRA-PRAZNA + Z66-NEZAKONSKI · Z14-APRIL-REŠEN · meseci-Feber/März/Dez-×0 · KRIŽAN-×6 + BRODARIČ-×6! · **LINIJA-5/15!** · vitals 1853 · 04104 107`
      : p225Errors.join("; "),
  );
  }

'''
src = src.replace(ANCHOR, BLOCK + ANCHOR, 1)
src = src.replace("HOUSE_VITALS.length !== 1742", "HOUSE_VITALS.length !== 1853")
# P224-block 04104-total: 90 → 107 (zdaj vključuje 1881!)
src = src.replace('if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length !== 90)',
                  'if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length !== 107)')
src = src.replace('p224Errors.push(`bloki 04104 ≠ 90 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length} — P221: 25 × 1885; P222: + 21 × 1884; P223: + 19 × 1883; P224: + 25 × 1882 = 90!)`)',
                  'p224Errors.push(`bloki 04104 ≠ 107 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length} — P221: 25 × 1885; P222: + 21 × 1884; P223: + 19 × 1883; P224: + 25 × 1882; P225: + 17 × 1881 = 107!)`)')
# yearset-04104: {1882,1883,1884,1885} → {1881,...,1885} (v P224-bloku!)
src = src.replace('if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)\n    p224Errors.push("04104-bloki izven {1882, 1883, 1884, 1885} (predzgodovina-4/15: 1882–1885-do-P225!)");',
                  'if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)\n    p224Errors.push("04104-bloki izven {1881, 1882, 1883, 1884, 1885} (predzgodovina-5/15: 1881–1885-do-P226!)");')
QA.write_text(src, encoding="utf-8")
print(f"qa-parish: 1853×{src.count('HOUSE_VITALS.length !== 1853')} · qa-p225×{src.count('qa-p225-parish-baptism-1881-04104')} · yearset-{src.count('(h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885')}")

# --- skripte + verifierji patch (1742→1853) ---
files = sorted(set(glob.glob(str(ROOT / "scripts/**/*.py"), recursive=True) + glob.glob(str(ROOT / "scripts/**/*.mjs"), recursive=True)))
skip = ("p225_",)
patched = 0
for f in files:
    if any(s2 in f for s2 in skip): continue
    t = Path(f).read_text(encoding="utf-8")
    if "1742" not in t: continue
    o = t
    t = t.replace("1742", "1853")
    if t != o:
        Path(f).write_text(t, encoding="utf-8"); patched += 1
print(f"skripte-patched: {patched}")

vpatched = 0
for f in sorted(ROOT.glob("scripts/p19*.py")) + sorted(ROOT.glob("scripts/p2[0-2][0-9]_parish*.py")):
    if "p225" in f.name: continue
    t = f.read_text(encoding="utf-8"); o = t
    for a, b in [("vitals == 1742", "vitals == 1853"), ("vitalsTotal == 1742", "vitalsTotal == 1853"),
                 ('vitalsTotal"] == 1742', 'vitalsTotal"] == 1853'),
                 ('"vitalsTotal": 1742', '"vitalsTotal": 1853'),
                 ('\\"vitalsTotal\\": 1742', '\\"vitalsTotal\\": 1853'),
                 ('!== 1742"', '!== 1853"'),
                 ("1742-številcev", "1853-številcev"),
                 ("vitals-števec-1742", "vitals-števec-1853"), ("vitals-1742", "vitals-1853")]:
        t = t.replace(a, b)
    if t != o:
        f.write_text(t, encoding="utf-8"); vpatched += 1
print(f"verifierji-patched: {vpatched}")

# p191 EXPECTED_CORPUS: 04104 90 → 107
p191 = ROOT / "scripts/p191_pt_luknja_final.py"
t = p191.read_text(encoding="utf-8"); o = t
t = t.replace('"04104": 90}', '"04104": 107}')
t = t.replace("# POSODABLJENO P224: + krstna-04104 = 90 (25×1885-P221 + 21×1884-P222 + 19×1883-P223 + 25×1882-P224!)",
              "# POSODABLJENO P225: + krstna-04104 = 107 (25×1885-P221 + 21×1884-P222 + 19×1883-P223 + 25×1882-P224 + 17×1881-P225!)")
if t != o: p191.write_text(t, encoding="utf-8"); print("p191-EXPECTED_CORPUS-patched (107)")

ptp = ROOT / "research/issue17/pt-luknja-18-final.json"
pt = json.loads(ptp.read_text(encoding="utf-8"))
pt["corpus"]["vitalsTotal"] = 1853
pt["corpus"]["byBook"]["04104"] = 107
pt["corpus"]["housesNote"] = (pt["corpus"].get("housesNote") or "") + " | P225: +17-blokov-1881-krstna-04104-5/15 (vitals 1742→1853; 04104 90→107; 89-DISTINCT = P224-LEAD-'z83–z89'-1:1 + 17-GRIBLJE/17-hiš-VSE-DISTINCT + MEJA-1880/81-s135/s136-64.-POTRDITEV (RESTART-z1-GRIBLJE-h55-'Finis'-BREZ-VSOTNE!) + FOLIACIJA-sken−6-13/13-SEKVENČNO (129–141!-sandwich-s143/s145!) + PEZDIRC-×9-REKORD-LETA (×12!) + 2-POROKE-'VNALILA' (z52-1959! + z57-1958!) + Z48-BOTRA-PRAZNA + Z66-NEZAKONSKI + Z14-APRIL-REŠEN + 1880 = 122-BONUS → P226-LEAD)"
ptp.write_text(json.dumps(pt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"pt-luknja: {pt['corpus']['vitalsTotal']}/{pt['corpus']['byBook']['04104']}")
