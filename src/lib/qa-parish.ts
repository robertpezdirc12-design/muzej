// qa-parish.ts — župnija Podzemelj: matrične kontrole (qa-p79 + qa-p80) izvlečene
// iz qa.ts runQA (P80: telo glavne funkcije je preseglo prag TS control flow
// analysis; vzorec ločevanja modulov). Deterministično iz runtime podatka
// parish.ts + pini PT klasifikacije/okvirjev; paleografske faze so ročne in
// dokumentirane v dokazih research/issue17/parish-*.json; live verifikatorja:
// scripts/p79_parish_sample.py --check (I1–I8) in scripts/p80_parish_md_books.py
// --check (I1–I10). Produkcija ne bere research/ (P53/P57/P58) — pini živijo tu.

import { HOUSE_VITALS, PARISH_BOOKS } from "@/data/atlas/parish";
import { PUA_CONTINUATION } from "@/data/atlas/research";
import { ATLAS_OWNERS } from "@/data/atlas/model";
import namePack from "@/data/atlas/parish-name-linkage.json";
import {
  P81_THRESHOLD,
  P81_NEAR_MISS,
  p81BestMatch,
  p81Norm,
} from "@/lib/name-matcher";

type Push = (id: string, nameSi: string, nameEn: string, pass: boolean, detail: string) => void;

export function parishChecks(push: Push): void {
// ——— qa-p79: župnija Podzemelj — vzorčni prepis matrik (issue #18; HOUSE_VITALS;
//      deterministično iz runtime podatka parish.ts + pini PT klasifikacije;
//      paleografska faza dokumentirana v research/issue17/parish-sample-transcription.json,
//      live verifikator scripts/p79_parish_sample.py --check I1–I8) ———
// P80: kontrola je omejena na KRSTNE vpise (04105) — poročni/mrliški iz P80
// imajo svojo kontrolno qa-p80-parish-md-books
// P82: vzorec omejen na P79 nabor (1886 + obstoječi 1897 hiša 61 + sidri
// 1887 hiši 61/78 pri skenu 20 — P82 RE-READ: hiša »75« je pravzaprav 78)
// — P82 doda 1887 okvir (skeni 16–27), ki ima svojo kontrolno qa-p82
// 1897: samo hiša 61 (izvirni vzorec issue #17) — polno leto 1897 ima svojo qa-p92
const p79Hv = HOUSE_VITALS.filter(
  (h) =>
    h.bookSignature === "04105" &&
    (h.year === 1886 || (h.year === 1897 && h.houseNo === "61") || (h.year === 1887 && ["61", "78"].includes(h.houseNo))),
);
const p79Errors: string[] = [];
// PT klasifikacija (pin iz research/issue13/chain-full-pt-ps.json; PT 1825:
// 84 hiš 1–40 + 61–99 z polovičkami; LUKNJA 41–60) — produkcija ne bere
// research/, zato klasifikacija živi kot pin (vzorec p76 pini)
const P79_PT_IN_SET = ["8", "16", "11", "36", "94", "39", "13", "71", "78", "61"]; // P82 RE-READ: 75 → 78
const P79_PT_GAP = ["54", "57", "56"];
if (p79Hv.length !== 15)
  p79Errors.push(`HOUSE_VITALS št. vpisov ≠ 15 (${p79Hv.length})`);
const p79Houses = new Set(p79Hv.map((h) => h.houseNo));
if (p79Houses.size !== 13)
  p79Errors.push(`različnih hiš ≠ 13 (${p79Houses.size}: ${[...p79Houses].sort().join(",")})`);
const p79Book = PARISH_BOOKS.find((b) => b.signature === "04105");
if (!p79Book || p79Book.type !== "baptism" || p79Book.from !== 1886 || p79Book.to !== 1919)
  p79Errors.push("PARISH_BOOKS: 04105 (baptism 1886–1919) ni dokumentiran");
const p79Bad = p79Hv.filter(
  (h) => h.status !== "DOCUMENTED" || h.bookSignature !== "04105" || !h.scan ||
    h.year < (p79Book?.from ?? 1886) || h.year > (p79Book?.to ?? 1919),
);
if (p79Bad.length > 0)
  p79Errors.push(`vpisi brez statusa/signature/skena ali izven obdobja knjige: ${p79Bad.length}`);
// okvir vzorca: vsi vpisi leta 1886 v skenih 2–15 s stran == sken − 1; sidro 1887 = sken 20
const p79Frame = p79Hv.filter((h) => h.year === 1886);
if (p79Frame.length !== 12)
  p79Errors.push(`vpisov 1886 ≠ 12 (${p79Frame.length})`);
if (p79Frame.some((h) => !h.scan || h.scan < 2 || h.scan > 15 || h.page !== h.scan - 1))
  p79Errors.push("okvir 1886: sken izven 2–15 ali stran ≠ sken − 1");
const p79Anchor = p79Hv.filter((h) => h.year === 1887 && h.scan === 20);
if (p79Anchor.length !== 2) // Katarina 61 (obstoječi) + Janez 75 (P79 sidro)
  p79Errors.push(`sidro 1887 (sken 20) ≠ 2 vpisa (${p79Anchor.length})`);
// PT klasifikacija == pin (10 v naboru + 3 v luknji 41–60)
const p79InSet = [...p79Houses].filter((h) => P79_PT_IN_SET.includes(h));
const p79Gap = [...p79Houses].filter((h) => P79_PT_GAP.includes(h));
if (p79InSet.length !== 10 || p79Gap.length !== 3)
  p79Errors.push(`PT klasifikacija ≠ 10/3 (${p79InSet.length}/${p79Gap.length})`);
push(
  "qa-p79-parish-sample",
  "P79: ŽUPNIJA PODZEMELJ — VZORČNI PREPIS MATRIČNIH VPISOV Z GRIBELJSKIMI HIŠNIMI ŠT. (issue #18; vir Matricula Online, Krstna knjiga 04105 1886–1919; paleografska faza + deterministična verifikacija; deterministično, brez AI ob delovanju): VZOREC = polno leto 1886 (skeni 2–15 == tiskane strani 1–14: VSI vpisi z Griblji v tem letu) + sidro 1887 (verifikacija obstoječega zapisa hiše 61) — 15 vpisov / 13 različnih hiš (8 [~], 11, 13, 16, 36×2 — dve družini pod eno št. [~], 39, 54, 56, 57, 61, 71, 75, 94) — NAD merili issue #18 (vzorec 5 hiš); vsak vpis: signatura + leto + stran/skan + hišna št. + otrok + starši (Kurrent z [~]); okvir 1886: 12 vpisov, skeni 2–15, stran == sken − 1 (kontrola sken 11 → stran 10, sken 20 → 19); PT usklajenost (pin iz chain-full-pt-ps.json: 84 hiš 1–40 + 61–99 z polovičkami, LUKNJA 41–60): 10/13 hiš v naboru (8, 11, 13, 16, 36, 39, 61, 71, 75, 94), 3/13 (54, 56, 57) v luknji 41–60 — DOKAZ ŠTEVILČNE EVOLUCIJE med 1825 in 1886 (številčna usklajenost ≠ identiteta stavbe); hiša 36: 2 vpisa v 1886 (row 39 brez očeta — mati Barbara Šimec; row 95 oče Matija Križan) — dokumentirano kot zapisano; poznejši modri pripisi 20. st. (umrl dne …, npr. hiša 39: umrl 18.9.1961 v Gribljah št. 39 — potrjuje hišno št.) dokumentirani ločeno; sidro: hiša 61 (sken 20, stran 19, vrstica 28 — Katarina) ponovno prebrana in POTRJENA (sken/leto/hiša/ime == parish.ts; oče: obe branji dokumentirani — »Miha P.—« obstoječe / »Miko Jože H.?« ponovno); live verifikacija: knjiga HTTP 200, inventar 326 slik (base64 dekodiranje), citirani skeni 10/10 JPEG 200; skripta scripts/p79_parish_sample.py (I1–I8, --check PASS); P82 RE-READ KOREKCIJA: sidro hiša »75« je pravzaprap 78 (izrez: dve zaprti zanki = 8); status SAMPLE-TRANSCRIPTION",
  "P79: PARISH OF PODZEMELJ — SAMPLE TRANSCRIPTION OF REGISTER ENTRIES WITH GRIBLJE HOUSE NUMBERS (issue #18; source Matricula Online, Baptism register 04105 1886–1919; paleographic phase + deterministic verification; deterministic, no AI at runtime): SAMPLE = the full year 1886 (scans 2–15 == printed pages 1–14: ALL Griblje entries in that year) + the 1887 anchor (verification of the existing house-61 record) — 15 entries / 13 distinct houses (8 [~], 11, 13, 16, 36×2 — two families under one number [~], 39, 54, 56, 57, 61, 71, 75, 94) — ABOVE the issue #18 criteria (a 5-house sample); every entry: signature + year + page/scan + house number + child + parents (Kurrent with [~]); the 1886 frame: 12 entries, scans 2–15, page == scan − 1 (controls scan 11 → page 10, scan 20 → 19); the PT consistency (pin from chain-full-pt-ps.json: 84 houses 1–40 + 61–99 with halves, the GAP 41–60): 10/13 houses in the set (8, 11, 13, 16, 36, 39, 61, 71, 75, 94), 3/13 (54, 56, 57) in the 41–60 gap — EVIDENCE OF NUMERIC EVOLUTION between 1825 and 1886 (numeric consistency ≠ building identity); house 36: 2 entries in 1886 (row 39 without a father — mother Barbara Šimec; row 95 father Matija Križan) — documented as written; later blue 20th-century annotations (died …, e.g. house 39: died 18 Sep 1961 in Griblje no. 39 — confirms the house number) documented separately; the anchor: house 61 (scan 20, page 19, row 28 — Katarina) re-read and CONFIRMED (scan/year/house/child == parish.ts; the father: both readings documented — »Miha P.—« existing / »Miko Jože H.?« re-read); live verification: the book HTTP 200, an inventory of 326 images (base64 decoding), the cited scans 10/10 JPEG 200; the script scripts/p79_parish_sample.py (I1–I8, --check PASS); the P82 RE-READ CORRECTION: the anchor house »75« is actually 78 (the crop: two closed loops = 8); status SAMPLE-TRANSCRIPTION",
  p79Errors.length === 0,
  p79Errors.length === 0
    ? `15 vpisov / 13 hiš · 1886 okvir 12 (skeni 2–15, stran == sken−1) · sidro 1887 2 vpisa (sken 20) · PT 10/3 (54, 56, 57 v luknji 41–60) · knjiga 04105 1886–1919 · [~] negotovosti dokumentirane · hiša 36 dva vpisa · pripisi 20. st. ločeno`
    : p79Errors.join("; "),
);

// ——— qa-p80: župnija Podzemelj — RAZŠIRITEV vzorca na mrliško (04894) in
//      poročno (04455) knjigo (issue #18; HOUSE_VITALS knjigi 04894/04455;
//      deterministično iz runtime podatka parish.ts + pini okvirjev in PT
//      klasifikacije; paleografska faza v research/issue17/parish-md-transcription.json,
//      live verifikator scripts/p80_parish_md_books.py --check I1–I10) ———
// P82: vzorec omejen na P79/P80 nabor (04105 1886 ∪ 1897 ∪ sidri 61/78;
// 04894 + 04455 v celoti) — 1887 krstni okvir ima svojo kontrolno qa-p82
// 04105: 1886 + hiša 61 iz 1897 (izvirni vzorec) + sidri 61/78 — polno leto 1897 = qa-p92
const p80All = HOUSE_VITALS.filter(
  (h) =>
    h.bookSignature === "04894" ||
    h.bookSignature === "04455" ||
    (h.bookSignature === "04105" &&
      (h.year === 1886 || (h.year === 1897 && h.houseNo === "61") || (h.year === 1887 && ["61", "78"].includes(h.houseNo)))),
);
const p80Death = p80All.filter((h) => h.bookSignature === "04894");
const p80Marr = p80All.filter((h) => h.bookSignature === "04455");
const p80Errors: string[] = [];
const p80BookDeath = PARISH_BOOKS.find((b) => b.signature === "04894");
const p80BookMarr = PARISH_BOOKS.find((b) => b.signature === "04455");
if (!p80BookDeath || p80BookDeath.type !== "death" || p80BookDeath.from !== 1886 || p80BookDeath.to !== 1924)
  p80Errors.push("PARISH_BOOKS: 04894 (death 1886–1924) ni dokumentiran");
if (!p80BookMarr || p80BookMarr.type !== "marriage" || p80BookMarr.from !== 1873 || p80BookMarr.to !== 1922)
  p80Errors.push("PARISH_BOOKS: 04455 (marriage 1873–1922) ni dokumentiran");
// mrliška: okvir 1886 = 13 vpisov (skeni 2–6, stran == sken − 1) + sidro 1887 = 2 vpisa (sken 6)
const p80Death1886 = p80Death.filter((h) => h.year === 1886);
const p80Death1887 = p80Death.filter((h) => h.year === 1887);
if (p80Death.length !== 15)
  p80Errors.push(`mrliški vpisi (04894) ≠ 15 (${p80Death.length})`);
if (p80Death1886.length !== 13)
  p80Errors.push(`mrliški okvir 1886 ≠ 13 vpisov (${p80Death1886.length})`);
if (p80Death1886.some((h) => !h.scan || h.scan < 2 || h.scan > 6 || h.page !== h.scan - 1))
  p80Errors.push("mrliški okvir 1886: sken izven 2–6 ali stran ≠ sken − 1");
if (p80Death1887.length !== 2 || p80Death1887.some((h) => h.scan !== 6))
  p80Errors.push(`mrliško sidro 1887 (sken 6) ≠ 2 vpisa (${p80Death1887.length})`);
// poročna: okvir 1886 = 7 vpisov (skeni 61–65, Pag. == sken − 1) + sidra = 4 (1885 sk.61 · 1882 sk.50 Pag.44 · 1887 sk.66 ×2)
const p80Marr1886 = p80Marr.filter((h) => h.year === 1886);
const p80MarrAnchors = p80Marr.filter((h) => h.year !== 1886);
if (p80Marr.length !== 168)
  p80Errors.push(`poročni vpisi (04455) ≠ 168 (${p80Marr.length} — P142: 164; P143: + 4 bloki 1914 (№3 h91+h68 + №4 h68 ISTA-HIŠA! + №5 h65+h31) = 168!)`);
if (p80Marr1886.length !== 7)
  p80Errors.push(`poročni okvir 1886 ≠ 7 vpisov (${p80Marr1886.length})`);
if (p80Marr1886.some((h) => !h.scan || h.scan < 61 || h.scan > 65 || h.page !== h.scan - 1))
  p80Errors.push("poročni okvir 1886: sken izven 61–65 ali Pag. ≠ sken − 1");
if (
  p80MarrAnchors.length !== 161 ||
  p80MarrAnchors.filter((h) => h.year === 1882).length !== 1 ||
  p80MarrAnchors.filter((h) => h.year === 1885).length !== 1 ||
  p80MarrAnchors.filter((h) => h.year === 1887).length !== 7 ||
  p80MarrAnchors.filter((h) => h.year === 1888).length !== 4 ||
  p80MarrAnchors.filter((h) => h.year === 1889).length !== 7 ||
  p80MarrAnchors.filter((h) => h.year === 1890).length !== 4 ||
  p80MarrAnchors.filter((h) => h.year === 1891).length !== 2 ||
  p80MarrAnchors.filter((h) => h.year === 1892).length !== 4 ||
  p80MarrAnchors.filter((h) => h.year === 1893).length !== 5 ||
  p80MarrAnchors.filter((h) => h.year === 1894).length !== 4 ||
  p80MarrAnchors.filter((h) => h.year === 1895).length !== 5 ||
  p80MarrAnchors.filter((h) => h.year === 1896).length !== 1 ||
  p80MarrAnchors.filter((h) => h.year === 1897).length !== 9 ||
  p80MarrAnchors.filter((h) => h.year === 1898).length !== 9 ||
  p80MarrAnchors.filter((h) => h.year === 1899).length !== 6 ||
  p80MarrAnchors.filter((h) => h.year === 1900).length !== 2 ||
  p80MarrAnchors.filter((h) => h.year === 1902).length !== 4 ||
  p80MarrAnchors.filter((h) => h.year === 1903).length !== 12 ||
  p80MarrAnchors.filter((h) => h.year === 1904).length !== 8 ||
  p80MarrAnchors.filter((h) => h.year === 1905).length !== 13 ||
  p80MarrAnchors.filter((h) => h.year === 1906).length !== 5 ||
  p80MarrAnchors.filter((h) => h.year === 1907).length !== 5 ||
  p80MarrAnchors.filter((h) => h.year === 1908).length !== 9 ||
  p80MarrAnchors.filter((h) => h.year === 1909).length !== 8 ||
  p80MarrAnchors.filter((h) => h.year === 1910).length !== 5 ||
  p80MarrAnchors.filter((h) => h.year === 1911).length !== 6 ||
  p80MarrAnchors.filter((h) => h.year === 1912).length !== 5 ||
  p80MarrAnchors.filter((h) => h.year === 1913).length !== 6 ||
  p80MarrAnchors.filter((h) => h.year === 1914).length !== 4
)
  p80Errors.push("poročna sidra ≠ 161 (1882:1 · 1885:1 · 1887:7 · 1888:4 · 1889:7 · 1890:4 · 1891:2 · 1892:4 · 1893:5 · 1894:4 · 1895:5 · 1896:1 · 1897:9 · 1898:9 · 1899:6 · 1900:2 · 1902:4 · 1903:12 · 1904:8 · 1905:13 · 1906:5 · 1907:5 · 1908:9 · 1909:8 · 1910:5 · 1911:6 · 1912:5 · 1913:6 · 1914:4 — P116 +5, P117 +4, P118 +7, P119 +4, P120 +2, P121 +4, P122 +5, P123 +4, P124 +3, P125 +3, P126 +9, P127 +9, P128 +6, P129 +2, P131 +4, P132 +12, P133 +8, P134 +13, P135 +5, P136 +5, P137 +9, P138 +8, P139 +5, P140 +6, P141 +5, P142 +6, P143 +4 bloki (№3 h91+h68 · №4 h68 ISTA-HIŠA! · №5 h65+h31!))");

// P125: hiša 1896 (04455) = [18]
const p125Marr = HOUSE_VITALS.filter((h) => h.bookSignature === "04455" && h.year === 1896);
if (p125Marr.map((h) => h.houseNo).sort().join(",") !== "18")
  p80Errors.push(`hiša 1896 (04455) ≠ [18] — najdeno: ${p125Marr.map((h) => h.houseNo).join(",")} (P125: v15 h18 Klobučar — edina GRIBLJE poroka 1896!)`);
// P126: hiše 1897 (04455) = [8, 18, 27, 28, 29, 33, 39, 40 ×2] — 5 porok / 9 blokov (string-sort: »8« na koncu — vzorec p123Houses BUG-lekcije!)
const p126Marr = HOUSE_VITALS.filter((h) => h.bookSignature === "04455" && h.year === 1897);
if (p126Marr.map((h) => h.houseNo).sort().join(",") !== "18,27,28,29,33,39,40,40,8")
  p80Errors.push(`hiše 1897 (04455) ≠ [8,18,27,28,29,33,39,40×2] — najdeno: ${p126Marr.map((h) => h.houseNo).join(",")} (P126: 5 GRIBLJE porok — h8 v5, h40×h29 v9, h18×h27 v10, h40×h39 v11, h33×h28 v18!)`);
if (p126Marr.length !== 9)
  p80Errors.push(`bloki 1897 (04455) ≠ 9 (${p126Marr.length} — 5 porok: v5 1 + v9 2 + v10 2 + v11 2 + v18 2 = 9!)`);
// P127: hiše 1898 (04455) = [22×2, 34, 46, 48, 54, 62, 67, 70] — 6 porok / 9 blokov (string-sort leksikografski!)
const p127Marr = HOUSE_VITALS.filter((h) => h.bookSignature === "04455" && h.year === 1898);
if (p127Marr.map((h) => h.houseNo).sort().join(",") !== "22,22,34,46,48,54,62,67,70")
  p80Errors.push(`hiše 1898 (04455) ≠ [22×2,34,46,48,54,62,67,70] — najdeno: ${p127Marr.map((h) => h.houseNo).join(",")} (P127: 6 GRIBLJE porok = REKORD LINIJE — h48 v2, h22×h67 v7, h22 v9, h54×h62 v11, h70 v15, h34×h46 v20!)`);
if (p127Marr.length !== 9)
  p80Errors.push(`bloki 1898 (04455) ≠ 9 (${p127Marr.length} — 6 porok: v2 1 + v7 2 + v9 1 + v11 2 + v15 1 + v20 2 = 9!)`);
// P128: hiše 1899 (04455) = [1, 10, 16, 20, 34, 44] — 3 poroke / 6 blokov (string-sort leksikografski!)
const p128Marr = HOUSE_VITALS.filter((h) => h.bookSignature === "04455" && h.year === 1899);
if (p128Marr.map((h) => h.houseNo).sort().join(",") !== "1,10,16,20,34,44")
  p80Errors.push(`hiše 1899 (04455) ≠ [1,10,16,20,34,44] — najdeno: ${p128Marr.map((h) => h.houseNo).join(",")} (P128: 3 GRIBLJE poroke — v1 h34 2. dokaz × h44 NOVA, v3 h1 NOVA NAJNIŽJA × h10 3. dokaz, v4 h20 2. dokaz × h16 3. dokaz!)`);
if (p128Marr.length !== 6)
  p80Errors.push(`bloki 1899 (04455) ≠ 6 (${p128Marr.length} — 3 poroke: v1 2 + v3 2 + v4 2 = 6!)`);
// P129: hiše 1900 (04455) = [7, 8] — 1 poroka / 2 bloka (string-sort leksikografski!)
const p129Marr = HOUSE_VITALS.filter((h) => h.bookSignature === "04455" && h.year === 1900);
if (p129Marr.map((h) => h.houseNo).sort().join(",") !== "7,8")
  p80Errors.push(`hiše 1900 (04455) ≠ [7,8] — najdeno: ${p129Marr.map((h) => h.houseNo).join(",")} (P129: EDINA GRIBLJE poroka — v2 h7 NOVA 1. dokaz × h8 NOVA 1. dokaz!)`);
if (p129Marr.length !== 2)
  p80Errors.push(`bloki 1900 (04455) ≠ 2 (${p129Marr.length} — 1 poroka: v2 2 = 2!)`);
// P131: hiše 1902 (04455) = [5, 24, 30, 31] — 2 poroki / 4 bloki (string-sort leksikografski!)
const p131Marr = HOUSE_VITALS.filter((h) => h.bookSignature === "04455" && h.year === 1902);
if (p131Marr.map((h) => h.houseNo).sort().join(",") !== "24,30,31,5")
  p80Errors.push(`hiše 1902 (04455) ≠ [24,30,31,5] — najdeno: ${p131Marr.map((h) => h.houseNo).join(",")} (P131: 2 GRIBLJE poroki — v2 h5 NOVA 1. dokaz × h31 NOVA 1. dokaz DRUBEL, v4 h30 3. dokaz × h24 2. dokaz DRUBEL!)`);
if (p131Marr.length !== 4)
  p80Errors.push(`bloki 1902 (04455) ≠ 4 (${p131Marr.length} — 2 poroki: v2 2 + v4 2 = 4!)`);
// P132: hiše 1903 (04455) = [6, 9, 11 ×2, 20, 41, 44, 46, 48, 50, 56, 65] — 8 porok / 12 blokov (string-sort leksikografski!)
const p132Marr = HOUSE_VITALS.filter((h) => h.bookSignature === "04455" && h.year === 1903);
const p133Marr = HOUSE_VITALS.filter((h) => h.bookSignature === "04455" && h.year === 1904);
if (p132Marr.map((h) => h.houseNo).sort().join(",") !== "11,11,20,41,44,46,48,50,56,6,65,9")
  p80Errors.push(`hiše 1903 (04455) ≠ [6,9,11×2,20,41,44,46,48,50,65] — najdeno: ${p132Marr.map((h) => h.houseNo).join(",")} (P132: 8 GRIBLJE porok — v1 h11 1. dokaz, v3 h65+h41 DRUBEL, v9 h46 2. dokaz, v11 h56 1. dokaz [DVOJNI DISPENS!], v12 h11 2. + h9 DRUBEL, v14 h6, v17 h20+h48 DRUBEL, v20 h50+h44 DRUBEL!)`);
if (p132Marr.length !== 12)
  p80Errors.push(`bloki 1903 (04455) ≠ 12 (${p132Marr.length} — 7 porok: v1 1 + v3 2 + v9 1 + v12 2 + v14 1 + v17 2 + v20 2 = 11!)`);
// P133: hiše 1904 (04455) = [22, 32, 38 ×2, 39, 42, 46, 62] — 5 porok / 8 blokov (string-sort leksikografski!)
if (p133Marr.map((h) => h.houseNo).sort().join(",") !== "22,32,38,38,39,42,46,62")
  p80Errors.push(`hiše 1904 (04455) ≠ [22,32,38×2,39,42,46,62] — najdeno: ${p133Marr.map((h) => h.houseNo).join(",")} (P133: 5 GRIBLJE porok — v2 h42 2. dokaz, v5 h32 3. + h38 1. DRUBEL, v8 h38 2. blok BRAT-SESTRA + h39 2. dokaz DRUBEL, v13 h62 3. dokaz [⅜!], v14 h46 3. + h22 3. DRUBEL!)`);
if (p133Marr.length !== 8)
  p80Errors.push(`bloki 1904 (04455) ≠ 8 (${p133Marr.length} — 5 porok: v2 1 + v5 2 + v8 2 + v13 1 + v14 2 = 8!)`);
// P134: hiše 1905 (04455) = [1 ×2, 10, 18, 24 ×2, 27, 30, 34 ×2, 35, 44, 65] — 8 porok / 13 blokov (string-sort leksikografski!)
const p134Marr = HOUSE_VITALS.filter((h) => h.bookSignature === "04455" && h.year === 1905);
if (p134Marr.map((h) => h.houseNo).sort().join(",") !== "1,1,10,18,24,24,27,30,34,34,35,44,65")
  p80Errors.push(`hiše 1905 (04455) ≠ [1×2,10,18,24×2,27,30,34×2,35,44,65] — najdeno: ${p134Marr.map((h) => h.houseNo).join(",")} (P134: 8 GRIBLJE porok — v2 h34 3. dokaz, v4 h24 3. × h30 4. DRUBEL, v5 h44 3. dokaz, v12 h24 4. BRATA! × h65 3. DRUBEL, v13 h18 3. + h34 4. SESTRA! DRUBEL, v14 h10 4. × h35 1. DOKAZ [korekcija 34→35!] DRUBEL, v15 h1 2. dokaz, v17 h27 4. × h1 3. DRUBEL!)`);
if (p134Marr.length !== 13)
  p80Errors.push(`bloki 1905 (04455) ≠ 13 (${p134Marr.length} — 8 porok: v2 1 + v4 2 + v5 1 + v12 2 + v13 2 + v14 2 + v15 1 + v17 2 = 13!)`);
// P135: hiše 1906 (04455) = [21, 31, 35, 62, 73] — 3 poroke / 6 blokov
const p135Marr = HOUSE_VITALS.filter((h) => h.bookSignature === "04455" && h.year === 1906);
if (p135Marr.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b)).join(",") !== "21,31,35,62,73")
  p80Errors.push(`hiše 1906 (04455) ≠ [21,31,35,62,73] — najdeno: ${p135Marr.map((h) => h.houseNo).join(",")} (P135: 3 GRIBLJE poroke — v8 h73 1. DOKAZ NOVI MAKSIMUM!, v9 h31 3. × h35 2. DRUBEL, v11 h62 4. KURE × h21 2. [1887→06 19-letna luknja!] DRUBEL!)`);
if (p135Marr.length !== 5)
  p80Errors.push(`bloki 1906 (04455) ≠ 5 (${p135Marr.length} — 3 poroke: v8 1 + v9 2 + v11 2 = 5!)`);
// P136: hiše 1907 (04455) = [3, 6 ×2, 7, 19] — 4 poroke / 5 blokov
const p136Marr = HOUSE_VITALS.filter((h) => h.bookSignature === "04455" && h.year === 1907);
if (p136Marr.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b)).join(",") !== "3,6,6,7,19")
  p80Errors.push(`hiše 1907 (04455) ≠ [3,6×2,7,19] — najdeno: ${p136Marr.map((h) => h.houseNo).join(",")} (P136: 4 GRIBLJE poroke — v4 h19 1. DOKAZ NOVA HIŠA!, v5 h6 2. × h7 3. DRUBEL sosednjih hiš!, v9 h3 2. [1887→07 20-LETNA LUKNJA!], v11 h6 3. = ★ 2. BLOK hiše V LETU!)`);
if (p136Marr.length !== 5)
  p80Errors.push(`bloki 1907 (04455) ≠ 5 (${p136Marr.length} — 4 poroke: v4 1 + v5 2 + v9 1 + v11 1 = 5!)`);
// P137: hiše 1908 (04455) = [14 ×2, 21, 28, 33, 39, 43, 44, 62] — 6 oseb / 9 blokov
const p137Marr = HOUSE_VITALS.filter((h) => h.bookSignature === "04455" && h.year === 1908);
if (p137Marr.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b)).join(",") !== "14,14,21,28,33,39,43,44,62")
  p80Errors.push(`hiše 1908 (04455) ≠ [14×2,21,28,33,39,43,44,62] — najdeno: ${p137Marr.map((h) => h.houseNo).join(",")} (P137: 6 GRIBLJE oseb — v1 h21 × h62 RECIPROČNA po 1906!, v5 h28 1. poročni dokaz (krstna 1891!), v9 h43 NOVA HIŠA!, v10 h39 × h44 DRUBEL!, v14 h33 20-letna kontinuiteta, v17 h14 × h14 ★★ INTRA-HIŠNA!)`);
if (p137Marr.length !== 9)
  p80Errors.push(`bloki 1908 (04455) ≠ 9 (${p137Marr.length} — 6 oseb: v1 2 + v5 1 + v9 1 + v10 2 + v14 1 + v17 2 (h14 ×2!) = 9!)`);
if (p80MarrAnchors.some((h) => h.year === 1882 && h.scan !== 50))
  p80Errors.push("poročno sidro 1882: sken ≠ 50 (Pag. 44)");
// celovitost polj + obdobja knjig
const p80Bad = p80All.filter(
  (h) =>
    (h.bookSignature === "04894" || h.bookSignature === "04455") &&
    (h.status !== "DOCUMENTED" || !h.scan || h.year < (h.bookSignature === "04894" ? 1886 : 1873) || h.year > (h.bookSignature === "04894" ? 1924 : 1922)),
);
if (p80Bad.length > 0)
  p80Errors.push(`vpisi brez statusa/skena ali izven obdobja knjige: ${p80Bad.length}`);
// PT klasifikacija celotnega vzorca: 46 različnih hiš v naboru + 12 v luknji 41–60 (42, 44, 46, 48, 52, 53, 54, 56, 57, 58, 59, 60 — P119: + h53 dokaz!; P122/P123: + h58 Požek + h42 CERNIČ dokaza!; P124: + h52 Perdinec-1895 dokaz!; P127: + h46 Klobučar + h48 Klobučar-Jakljevič poročna 1898 dokaza!)
const p80Houses = new Set(p80All.map((h) => h.houseNo));
const P80_PT_GAP = ["44", "53", "54", "56", "57", "59", "60", "42", "58", "52", "46", "48", "43"]; // P119: + h53 (poročna 1890 v6 Johann Perdinec — NOVI dokaz v luknji!); P122/P123: + h58 (poročna 1893 v16 Johann Požek) + h42 (poročna 1894 v3 — CERNIČ-hiša) — NOVA dokaza v luknji!; P124: + h52 (poročna 1895 v13 Mathias Perdinec — NOV dokaz v luknji!); P127: + h46 (poročna 1898 v20 nevesta Catharina Klobučar) + h48 (poročna 1898 v2 nevesta Anna Klobučar) — NOVA dokaza v luknji!; P137: + h43 (poročna 1908 v9 nevesta Maria Lasič [~] — 13. hiša luknje!); P138: + h57 (poročna 1909 №8 nevesta Maria Pezdirec — 14. hiša luknje, NOVA HIŠA!)
const p80Gap = [...p80Houses].filter((h) => P80_PT_GAP.includes(h));
if (p80Houses.size !== 71)
  p80Errors.push(`različnih hiš (vse tri knjige) ≠ 70 (${p80Houses.size} — P117: +h32/h33/h64; P118: +h7/h30/h40/h54/h87; P119: +h91/h53; P120: +h20; P121: +h17; P122: +h26/h58/h62 (h69/h74 že v vzorci); P123: +h9/h27/h42 (h11 že v vzorci); P124: +h52 (h16 že v mrliškem vzorci); P125: +h24/h14/h18; P126: +h28 EDINA NOVA; P127: +h48/h22/h67/h70/h34/h46 — 6 NOVIH v vzorcu prek poročne 04455-1898; P128: +h1 (poročna 1899 v3 — 1. poročni dokaz NAJNIŽJE številke; h44/h10/h16/h20/h34 že v vzorci); P132: +h6/h50 (poročna 1903 — 2 NOVI v korpusu); P133: +h38 (poročna 1904 v5/v8 — GANSLER-hiša; h42/h32/h39/h62/h46/h22 kontinuitete); P134: +h35 (poročna 1905 v14 nevesta Anna KRIŽAN — korekcija 34→35! EDINA nova); P135: +h73 (poročna 1906 v8 ženin Johann Šuparnič? — NOVI MAKSIMUM h65→h73!; h21 že od 1887!); P136: +h19 (poročna 1907 v4 ženin Nikolaus Hranc [~] — 1. poročni dokaz NOVE hiše!; h6/h7/h3 kontinuitete — h6 2 bloka v letu!); P137: +h43 (poročna 1908 v9 nevesta Maria Lasič [~] — 67. poročna hiša korpusa!); P138: h57 že v vzorci (kriste!); P139: +h86 (poročna 1910 №14 ženin Marcus Križan — NOVA hiša: 04105-h86 bloki 1912+ niso v p80-filtru!); P140: +h63 (poročna 1911 №1 nevesta Catharina KRIŽAN — NOVA hiša: 04105-h63 bloki 1887–1909 niso v p80-filtru!); P141: h78 ŽE v p80-filtru (04105-h78-1915 krst Lozar! — razlika od h63/h86: njuni 04105-bloki 1887–1909/1912+ IZVEN filtra!) → 69 NESPREMENJENO; P142: +h76 (poročna 1913 №10 ženin Janko Vranešič — 1. poročni dokaz h76; 04105-h76-krst 1913 IZVEN p80-filtra!) → 70; P143: +h68 (poročna 1914 №3 nevesta Mlakova + №4 ISTA-HIŠA — 1. korpusni pojav hiše 68! [0 zapisov 1885–1913]) → 71`);
if (p80Gap.length !== 13)
  p80Errors.push(`PT luknja ≠ 13 hiš (${p80Gap.length}: ${p80Gap.sort().join(",")} — P138: h57 že v luknji (kriste!), poroka 1909 = 1. poročni dokaz h57!; P139: h86 NI v luknji (61–99 nabor!) — luknja nespremenjena!)`);
// križne povezave: hiše 13, 36, 71 v VSEH treh knjigah
const p80Tri = ["13", "36", "71"].filter(
  (h) => p80Houses.has(h) && ["04105", "04894", "04455"].every((s) => p80All.some((v) => v.houseNo === h && v.bookSignature === s)),
);
if (p80Tri.length !== 3)
  p80Errors.push(`tri-virske hiše ≠ 3 (${p80Tri.length}: ${p80Tri.join(",")})`);
// P80 re-read: hiša 56 (krstna) mora brati »roj. Perdinec«; staro branje »roj. Podžire« ne sme več obstajati
// (omejitev na vzorec »roj. …« — korekcijska opomba sme omeniti staro branje)
const p80H56 = HOUSE_VITALS.find((h) => h.houseNo === "56" && h.bookSignature === "04105");
if (!p80H56 || !p80H56.whatSi.includes("roj. Perdinec") || /roj\.\s*Podžire/.test(p80H56.whatSi))
  p80Errors.push("re-read hiša 56: mati ≠ roj. Perdinec ali ostanki starrega branja roj. Podžire");
push(
  "qa-p80-parish-md-books",
  "P80: ŽUPNIJA PODZEMELJ — RAZŠIRITEV VZORCA NA MRLIŠKO (04894) IN POROČNO (04455) KNJIGO (issue #18; vir Matricula Online; deterministično, brez AI ob delovanju): MRLIŠKA — okvir 1886: skeni 2–6 == strani 1–5 (46 vrstic; leto 1887 se začne na strani 5 pri »Januarj 1887«) — 13 Griblje vpisov / 11 različnih hiš (5 · 13 · 15 · 16 · 29×3 · 31 · 59 · 69 · 71 · 74 · 88) + sidro 1887 (sken 6: hiša 44 prvi vpis leta + hiša 36 Ana Šimec neza. — povezava z materjo Barbaro Šimec); STRAN == SKEN − 1 (isti vzorec kot krstna); POROČNA — okvir 1886: skeni 61–65 == Pag. 60–64 (vpisi 1–24; Pag. == sken − 1 v razponu 61–66) — 7 Griblje vpisov / 10 različnih hiš (žENINI ali žENINOVI: 31 · 36 · 60 · 63 · 15 · 25 · 71) + sidra (Nov 1885 sken 61: hiša 13 ženin Janez Jakobič, čigar starši == pari krsta hiše 13; Nov 1882 sken 50 Pag. 44: hiša 36 Mathias Križan = oče krsta Dec 1886; 1887 sken 66: hiša 71 Mathias Straus + hiša 15/29 Johann Šambie × Maria Brinec); KRIŽNE POVEZAVE TRIH VIROV: hiša 13 (krst Matija Jakopič + Marija Podlirc == starši ženina 1885 == smrt Ane Jakobuč 1 leto Mar 1886), hiša 36 (krst brez očeta/Barbara Šimec + smrt Ane Šimec neza. Jan 1887 + poroki Križan 1882 in Šimec 1886), hiša 71 (krst Jurij Strauš + smrt Ane Strauš vdove »v drugo omožena Križan« + poroki Marije Straus Nov 1886 in Mathiasa Strausa Jan 1887 — priimek Strauš v vseh treh knjigah); DRAMATIKA VZORCA: hiša 29 — trije otroci (Janez 8, Katarina 9, Ana 11 — Mileh [~]) umrli v 4 dneh oktobra 1886 z istim vzrokom »Kolera i. morbas« [~]; P80 RE-READ KOREKCIJA: hiša 56 mati = Perdinec [~] (ne »Podžire«) — poročna sk. 62 vpis 4/1886 Johann Šimec × Dorothea Perdinec = isti par kot krst Nov 1886; PT klasifikacija celotnega vzorca 25 hiš: 19 v naboru + 6 v luknji 41–60 (44, 54, 56, 57, 59, 60 — 59/60 NOVI dokazi luknje v mrliški/poročni); live verifikacija: knjigi HTTP 200 (inventarja 256 + 192 slik), citirani skeni 13/13 JPEG 200; skripta scripts/p80_parish_md_books.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-EXTENDED",
  "P80: PARISH OF PODZEMELJ — SAMPLE EXTENDED TO THE DEATH (04894) AND MARRIAGE (04455) REGISTERS (issue #18; source Matricula Online; deterministic, no AI at runtime): DEATH REGISTER — the 1886 frame: scans 2–6 == pages 1–5 (46 rows; the year 1887 begins on page 5 at »Januarj 1887«) — 13 Griblje entries / 11 distinct houses (5 · 13 · 15 · 16 · 29×3 · 31 · 59 · 69 · 71 · 74 · 88) + the 1887 anchor (scan 6: house 44 the first entry of the year + house 36 Ana Šimec illegitimate — linked to mother Barbara Šimec); PAGE == SCAN − 1 (the same pattern as the baptism register); MARRIAGE REGISTER — the 1886 frame: scans 61–65 == pages 60–64 (entries 1–24; page == scan − 1 in the 61–66 range) — 7 Griblje entries / 10 distinct houses (groom's or bride's: 31 · 36 · 60 · 63 · 15 · 25 · 71) + anchors (Nov 1885 scan 61: house 13 groom Janez Jakobič whose parents == the house-13 baptism couple; Nov 1882 scan 50 page 44: house 36 Mathias Križan = the father of the Dec 1886 baptism; 1887 scan 66: house 71 Mathias Straus + house 15/29 Johann Šambie × Maria Brinec); THREE-SOURCE CROSS-LINKS: house 13 (baptism Matija Jakopič + Marija Podlirc == the 1885 groom's parents == the death of 1-year-old Ana Jakobuč Mar 1886), house 36 (baptism without father/Barbara Šimec + the death of illegitimate Ana Šimec Jan 1887 + the Križan 1882 and Šimec 1886 marriages), house 71 (baptism Jurij Strauš + the death of the widow Ana Straus »remarried Križan« + the marriages of Maria Straus Nov 1886 and Mathias Straus Jan 1887 — the Strauš surname in all three registers); SAMPLE DRAMA: house 29 — three children (Janez 8, Katarina 9, Ana 11 — Mileh [~]) dead within 4 days of October 1886 with the same cause »Kolera i. morbas« [~]; P80 RE-READ CORRECTION: house 56 mother = Perdinec [~] (not »Podžire«) — the marriage register scan 62 entry 4/1886 Johann Šimec × Dorothea Perdinec = the same couple as the Nov 1886 baptism; the PT classification of the whole 25-house sample: 19 in the set + 6 in the 41–60 gap (44, 54, 56, 57, 59, 60 — 59/60 NEW gap evidence in the death/marriage registers); live verification: both books HTTP 200 (inventories 256 + 192 images), cited scans 13/13 JPEG 200; the script scripts/p80_parish_md_books.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-EXTENDED",
  p80Errors.length === 0,
  p80Errors.length === 0
    ? `mrliška 15 vpisov / 11 hiš (1886 okvir 13, skeni 2–6, stran == sken−1; sidro 1887 sken 6 ×2) · poročna 11 vpisov / 10 hiš (1886 okvir 7, skeni 61–65; sidra 1882 sk.50 · 1885 sk.61 · 1887 sk.66 ×2) · 25 hiš skupaj: 19 nabor + 6 luknja (44/54/56/57/59/60) · tri-virske 13/36/71 · re-read hiša 56 Perdinec · hiša 29 epidemija 3 otroci`
    : p80Errors.join("; "),
);

// ——— qa-p81: povezava lastniških imen 1825 (PT/PUA) ↔ matrični priimki 1886
//      (issue #18; NAME-LINKAGE-PACK; celoven neodvisen preracun ujemanja iz
//      bundled virov: pack runtime + PUA_CONTINUATION + ATLAS_OWNERS +
//      HOUSE_VITALS; PT lastniki iz pack.universe1825 = pini, ki jih repo
//      skripta p81 --check verificira proti chain-full-pt-ps.json (I3);
//      anchors src=="parish" verificirani tukaj (bundled parish.ts), src
//      p79/p80 pa samo v repo skripti — produkcija ne bere research/) ———
const p81Errors: string[] = [];
const P81_PT_GAP = ["44", "54", "56", "57", "59", "60"];
type P81NameRec = { src: string; loc: string; house: string | string[]; name: string };
// vesolje 1825: PUA + ATLAS (bundle, neodvisno) + chain iz packa (pin, repo-verificiran)
const p81Universe: P81NameRec[] = [
  ...namePack.universe1825.names
    .filter((n) => n.src === "chain")
    .map((n) => ({ src: n.src, loc: n.loc, house: n.house as string | string[], name: n.name })),
  ...PUA_CONTINUATION.rows.map((r) => ({
    src: "pua",
    loc: `p${r.page}r${r.row}`,
    house: (r.houseNos ?? []) as string[],
    name: r.nameAsWritten,
  })),
  ...ATLAS_OWNERS.map((o) => ({
    src: "atlas",
    loc: o.id,
    house: o.houseRefs as string[],
    name: o.nameAsWritten,
  })),
];
if (p81Universe.length !== namePack.universe1825.totalNames)
  p81Errors.push(`vesolje 1825 ≠ ${namePack.universe1825.totalNames} (${p81Universe.length}; chain pin + PUA ${PUA_CONTINUATION.rows.length} + ATLAS ${ATLAS_OWNERS.length})`);
// pack struktura: 25 hiš, 19 nabor / 6 luknja, PT owner == pin (luknja hiše brez)
const p81Houses = namePack.houses as Array<{
  houseNo: string;
  ptIn1825: boolean;
  ptOwner1825: string | null;
  sameHouse: { pt: Record<string, unknown> | null; atlas: Record<string, unknown> | null; pua: Record<string, unknown> | null };
  parish1886: Array<{ surname: string; role: string; anchor: string; src: string; anchorHouse?: string }>;
  surnameWitnesses: Array<{ surname: string; best: number | null; witnesses: Array<{ src: string; loc: string; score: number }>; nearMisses: Array<{ src: string; loc: string; score: number }>; survives: boolean }>;
  surnameSurvives: boolean;
  sameNumberAny: boolean;
}>;
if (p81Houses.length !== 25) p81Errors.push(`pack hiš ≠ 25 (${p81Houses.length})`);
const p81InNabor = p81Houses.filter((h) => h.ptIn1825);
const p81Gap = p81Houses.filter((h) => !h.ptIn1825);
if (p81InNabor.length !== 19 || p81Gap.length !== 6)
  p81Errors.push(`PT klasifikacija ≠ 19/6 (${p81InNabor.length}/${p81Gap.length})`);
if (p81Gap.some((h) => !P81_PT_GAP.includes(h.houseNo)) || p81Gap.length !== new Set(p81Gap.map((h) => h.houseNo)).size)
  p81Errors.push("luknjane hiše ≠ {44, 54, 56, 57, 59, 60}");
if (p81Gap.some((h) => h.ptOwner1825 !== null) || p81InNabor.some((h) => !h.ptOwner1825))
  p81Errors.push("ptOwner1825 == null samo za luknjane hiše (in obratno)");
// NEODVISEN preracun: isto-hiša (PT/ATLAS/PUA, ≥ prag) == pack.sameHouse
const near = (a: number, b: number) => Math.abs(a - b) <= 1e-4;
let p81SameAny = 0;
let p81SamePT = 0;
for (const h of p81Houses) {
  const surnames = [...new Set(h.parish1886.map((r) => r.surname))].sort();
  const bestOf = (nm: string) => {
    let best: { surname: string; score: number } | null = null;
    for (const s of surnames) {
      const m = p81BestMatch(s, nm);
      if (m && m.score >= P81_THRESHOLD && (!best || m.score > best.score)) best = { surname: s, score: m.score };
    }
    return best;
  };
  const recs: Array<"pt" | "atlas" | "pua"> = [];
  if (h.ptOwner1825) {
    const b = bestOf(h.ptOwner1825);
    const e = h.sameHouse.pt as { surname?: string; score?: number } | null;
    if ((b === null) !== (e === null)) p81Errors.push(`isto-hiša PT hiša ${h.houseNo}: prisotnost ≠ pack`);
    if (b && e && (b.surname !== e.surname || !near(b.score, e.score ?? -1)))
      p81Errors.push(`isto-hiša PT hiša ${h.houseNo}: ${b.surname}/${b.score} ≠ pack ${e.surname}/${e.score}`);
    if (b) recs.push("pt");
  }
  const atlasHits = ATLAS_OWNERS.filter((o) => o.houseRefs.includes(h.houseNo));
  let atlasBest: { surname: string; score: number; id: string } | null = null;
  for (const o of atlasHits) {
    const b = bestOf(o.nameAsWritten);
    if (b && (!atlasBest || b.score > atlasBest.score)) atlasBest = { ...b, id: o.id };
  }
  const ea = h.sameHouse.atlas as { surname?: string; score?: number; id?: string } | null;
  if ((atlasBest === null) !== (ea === null)) p81Errors.push(`isto-hiša ATLAS hiša ${h.houseNo}: prisotnost ≠ pack`);
  if (atlasBest && ea && (atlasBest.surname !== ea.surname || atlasBest.id !== ea.id || !near(atlasBest.score, ea.score ?? -1)))
    p81Errors.push(`isto-hiša ATLAS hiša ${h.houseNo}: neujema s pack`);
  if (atlasBest) recs.push("atlas");
  const puaHits = PUA_CONTINUATION.rows.filter((r) => (r.houseNos ?? []).includes(h.houseNo));
  let puaBest: { surname: string; score: number; loc: string } | null = null;
  for (const r of puaHits) {
    const b = bestOf(r.nameAsWritten);
    if (b && (!puaBest || b.score > puaBest.score)) puaBest = { ...b, loc: `p${r.page}r${r.row}` };
  }
  const ep = h.sameHouse.pua as { surname?: string; score?: number } | null;
  if ((puaBest === null) !== (ep === null)) p81Errors.push(`isto-hiša PUA hiša ${h.houseNo}: prisotnost ≠ pack`);
  if (puaBest && ep && (puaBest.surname !== ep.surname || !near(puaBest.score, ep.score ?? -1)))
    p81Errors.push(`isto-hiša PUA hiša ${h.houseNo}: ${puaBest.surname}/${puaBest.score} ≠ pack ${ep.surname}/${ep.score}`);
  if (puaBest) recs.push("pua");
  if (recs.length > 0) p81SameAny += 1;
  if (recs.includes("pt")) p81SamePT += 1;
}
if (p81SameAny !== namePack.stats.sameHouseAnyCount)
  p81Errors.push(`isto-hišnih ujem ≠ ${namePack.stats.sameHouseAnyCount} (${p81SameAny})`);
if (p81SamePT !== namePack.stats.sameHousePTCount || p81SamePT !== 0)
  p81Errors.push(`isto-hišnih PT ujem ≠ 0 (${p81SamePT}) — NIL-CLAIM P81`);
// NEODVISEN preracun cenza: priče priimkov po vesolju → witnessed seznam == pack
const p81Eligible = [...new Set(p81Houses.flatMap((h) => h.parish1886.map((r) => r.surname)))]
  .filter((s) => {
    for (const german of [false, true]) {
      const n = p81Norm(s, german);
      if (n.length >= 4) return true;
    }
    return false;
  })
  .sort();
const p81Scores = new Map<string, number>();
for (const h of p81Houses) {
  for (const s of new Set(h.parish1886.map((r) => r.surname))) {
    let best = p81Scores.get(s) ?? 0;
    for (const u of p81Universe) {
      const m = p81BestMatch(s, u.name);
      if (m && m.score > best) best = m.score;
    }
    p81Scores.set(s, best);
  }
}
const p81Witnessed = p81Eligible
  .filter((s) => (p81Scores.get(s) ?? 0) >= P81_THRESHOLD)
  .sort((a, b) => (p81Scores.get(b) ?? 0) - (p81Scores.get(a) ?? 0) || (a < b ? -1 : a > b ? 1 : 0));
const p81NearMiss = p81Eligible.filter((s) => (p81Scores.get(s) ?? 0) >= P81_NEAR_MISS && (p81Scores.get(s) ?? 0) < P81_THRESHOLD);
if (p81Witnessed.length !== namePack.stats.witnessedSurnames)
  p81Errors.push(`prič prvimkov ≠ ${namePack.stats.witnessedSurnames} (${p81Witnessed.length})`);
if (p81Witnessed.join("|") !== (namePack.stats.witnessedSurnamesList as string[]).join("|"))
  p81Errors.push(`seznam prič ≠ pack (${p81Witnessed.join(",")} vs ${(namePack.stats.witnessedSurnamesList as string[]).join(",")})`);
if (Math.abs(100 * p81Witnessed.length / p81Eligible.length - namePack.stats.witnessedSurnamesPct) > 0.01)
  p81Errors.push("delež prič ≠ pack");
for (const s of p81Eligible) {
  const pk = (namePack.stats.surnameBestScores as Record<string, number>)[s] ?? 0;
  if (!near(pk, p81Scores.get(s) ?? 0))
    p81Errors.push(`najboljše razmerje ${s}: ${p81Scores.get(s)} ≠ pack ${pk}`);
}
if (p81NearMiss.length !== namePack.stats.nearMissSurnames)
  p81Errors.push(`near-miss ≠ ${namePack.stats.nearMissSurnames} (${p81NearMiss.length})`);
// PUA 41–60 podtabela: neodvisno iz bundle PUA == pack
const p81GapRows = PUA_CONTINUATION.rows
  .map((r) => ({ r, g: (r.houseNos ?? []).filter((x) => /^\d+$/.test(x) && Number(x) >= 41 && Number(x) <= 60) }))
  .filter((x) => x.g.length > 0)
  .sort((a, b) => Number(a.g[0]) - Number(b.g[0]) || a.r.page - b.r.page || a.r.row - b.r.row);
if (p81GapRows.length !== (namePack.puaGap4160 as Array<{ houseNo: string }>).length)
  p81Errors.push(`PUA 41–60 ≠ ${namePack.puaGap4160.length} (${p81GapRows.length})`);
for (let i = 0; i < Math.min(p81GapRows.length, (namePack.puaGap4160 as Array<Record<string, unknown>>).length); i++) {
  const pk = (namePack.puaGap4160 as Array<{ houseNo: string; page: number; row: number; vs1886: Array<{ surname: string; score: number; threshold: boolean }> }>)[i];
  const rc = p81GapRows[i];
  if (pk.houseNo !== rc.g[0] || pk.page !== rc.r.page || pk.row !== rc.r.row)
    p81Errors.push(`PUA 41–60 [${i}]: ${pk.houseNo}/p${pk.page}r${pk.row} ≠ ${rc.g[0]}/p${rc.r.page}r${rc.r.row}`);
  const hh = p81Houses.find((h) => h.houseNo === rc.g[0]);
  let best: { surname: string; score: number } | null = null;
  if (hh) {
    for (const s of [...new Set(hh.parish1886.map((r) => r.surname))].sort()) {
      const m = p81BestMatch(s, rc.r.nameAsWritten);
      if (m && (!best || m.score > best.score)) best = { surname: s, score: m.score };
    }
  }
  const ev = pk.vs1886[0] ?? null;
  if ((best === null) !== (ev === null)) p81Errors.push(`PUA 41–60 ${rc.g[0]} vs1886: prisotnost ≠ pack`);
  if (best && ev && (best.surname !== ev.surname || !near(best.score, ev.score)))
    p81Errors.push(`PUA 41–60 ${rc.g[0]} vs1886: ${best.surname}/${best.score} ≠ pack ${ev.surname}/${ev.score}`);
}
// sidra src=="parish": anchor mora biti v bundled HOUSE_VITALS whatSi te hiše
// (ali anchorHouse); src p79/p80 — samo repo skripta (produkcija ne bere research/)
const p81ParishText = (houseNo: string) =>
  HOUSE_VITALS.filter((v) => v.houseNo === houseNo).map((v) => v.whatSi).join(" || ");
let p81Anchors = 0;
for (const h of p81Houses) {
  for (const row of h.parish1886) {
    if (row.src !== "parish") continue;
    p81Anchors += 1;
    const ah = row.anchorHouse && row.anchorHouse !== h.houseNo ? row.anchorHouse : h.houseNo;
    if (!p81ParishText(ah).includes(row.anchor))
      p81Errors.push(`sidro hiša ${h.houseNo} ${row.surname} ni v parish.ts (${ah}): ${row.anchor}`);
  }
}
if (p81Anchors !== 57) p81Errors.push(`sidr src==parish ≠ 57 (${p81Anchors})`);
push(
  "qa-p81-parish-name-linkage",
  "P81: ŽUPNIJA PODZEMELJ — POVEZAVA LASTNIŠKIH IMEN 1825 (PT/PUA) ↔ MATRIČNI PRIIMKI 1886 (issue #18; NAME-LINKAGE-PACK; deterministično, brez AI ob delovanju): vzorec P79/P80 (25 hiš: 19 v naboru PT 1–40+61–99, 6 v luknji 41–60) × vesolje 1825 (PT 84 hišnih lastnikov iz chain-full-pt-ps.json [pin] + PUA 101 vrstic str. 3–49 + ATLAS 26 lastnikov str. A–B — 232 imen); ujemanje = normalizacija (pass1 de-diacritika + pass2 nem. Kurrent sch→s), Levenshtein razmerje, prag priče ≥ 0.72 (P43 W-most), kratki priimki < 5 znakov le natančna enakost, stoplist krstnih imen (Gregor itn. — brez nje bi priimek Gregorič lažno ujel krstno ime Gregor 0.75) + uredniški žetoni (rokopis/alternative); REZULTATI — ① ISTO-HIŠNA kontinuiteta vs PT 1825: 0/19 (NIL-CLAIM: vsaka hiša z PT lastnikom ima 1886 drugačen gospodinjski priimek, prag 0.72) ② isto-hišne ujeme po PUA lastnem številčenju [~]: 2 — hiša 36 Križan ↔ PUA Krischan @36 (0.8333 via sch→s) in hiša 71 Straus ↔ PUA Strauß Niklo @71 (0.8571) — PUA ≠ PT številčenje, usklajenost dveh sistemov, ne dokaz istovetnosti ③ CENZUS priimkov: 10/38 eligible (26.32 %) ima pričo 1825 — Dragoš=1.0 (Dragosch 3/4/5), Filak=1.0 (PT 69/71 + PUA Fillah 16/34/36/61), Stubler=1.0 (Stübler @30), Šimec=1.0 (ATLAS 3/4/63/64/66 + PUA Schimcz/Schimey/Schimer/Schimetz/Schumetz), Šimer=1.0 [~] (Schimer @38 via sch→s), Strauš/Straus=0.8571 (PUA 45/71/72 + ATLAS 76/79/81–84/92), Brinec=0.8333 [~] (PUA »Brinc« alternativa @43 — št. V LUKNJANI 41–60), Filatk=0.8333 [~] (PT filak), Križan=0.8333 (PT/ATLAS Krišan @29–30) ④ near-miss pas [0.55, 0.72) — 11 priimkov (Gilatk 0.667, Mileh/Milavec ~ Milleg 0.667/0.571, Stupanič ~ Stepanitsch 0.667, Šilah ~ Fillah 0.667, Klepec ~ Kleppetz 0.625, Poddirec ~ Poldiŕg 0.625 …) ⑤ PUA ohranja 16 vrstic v luknji 41–60 (P4) — 0 isto-številnih ujem ≥ 0.72 z 1886 (najbližje @56 Schumetz vs Šimec 0.667 [~]) ⑥ tri-virske hiše 13/36/71: 0/3 isto-hišnih imenskih ujem z 1825; IMPLIKACIJA: imenska raven POTRJUJE opozorilo issue #18 — številčna usklajenost ≠ identiteta stavbe ≠ identiteta družine; most zahteva per-hišne kronološke verige (poln prepis = lastniška prioriteta); sidra: 57 src==parish verificiranih proti bundled parish.ts (preostala 4 — 1 p80 + 3 p79 — v repo skripti); celoven neodvisen preracun: isto-hiša PT/ATLAS/PUA + cenzus + PUA 41–60 + sidra iz pack runtime × PUA_CONTINUATION × ATLAS_OWNERS × HOUSE_VITALS; live verifikator scripts/p81_parish_name_linkage.py (I1–I10, --check PASS, trojni determinizem); status NAME-LINKAGE-PACK",
  "P81: PARISH OF PODZEMELJ — LINKING 1825 OWNER NAMES (PT/PUA) ↔ 1886 PARISH SURNAMEs (issue #18; NAME-LINKAGE-PACK; deterministic, no AI at runtime): the P79/P80 sample (25 houses: 19 in the PT set 1–40+61–99, 6 in the 41–60 gap) × the 1825 universe (PT 84 house owners from chain-full-pt-ps.json [pin] + PUA 101 rows pp. 3–49 + ATLAS 26 owners pp. A–B — 232 names); matching = normalization (pass1 de-diacritics + pass2 German Kurrent sch→s), Levenshtein ratio, witness threshold ≥ 0.72 (the P43 W-most), short surnames < 5 chars exact-token-only, a given-name stoplist (Gregor etc. — without it the surname Gregorič would falsely match the given name Gregor at 0.75) + editorial tokens (rokopis/alternative); RESULTS — ① same-number continuity vs the PT 1825 owner: 0/19 (NIL-CLAIM: every house with a PT owner has a different household surname in 1886, threshold 0.72) ② same-number matches via PUA's own numbering [~]: 2 — house 36 Križan ↔ PUA Krischan @36 (0.8333 via sch→s) and house 71 Straus ↔ PUA Strauß Niklo @71 (0.8571) — PUA ≠ PT numbering, a consistency of two systems, not building identity ③ SURNAME CENSUS: 10/38 eligible (26.32 %) have an 1825 witness — Dragoš=1.0 (Dragosch 3/4/5), Filak=1.0 (PT 69/71 + PUA Fillah 16/34/36/61), Stubler=1.0 (Stübler @30), Šimec=1.0 (ATLAS 3/4/63/64/66 + PUA Schimcz/Schimey/Schimer/Schimetz/Schumetz), Šimer=1.0 [~] (Schimer @38 via sch→s), Strauš/Straus=0.8571 (PUA 45/71/72 + ATLAS 76/79/81–84/92), Brinec=0.8333 [~] (PUA »Brinc« alternative @43 — a number INSIDE the 41–60 gap), Filatk=0.8333 [~] (PT filak), Križan=0.8333 (PT/ATLAS Krišan @29–30) ④ near-miss band [0.55, 0.72) — 11 surnames (Gilatk 0.667, Mileh/Milavec ~ Milleg 0.667/0.571, Stupanič ~ Stepanitsch 0.667, Šilah ~ Fillah 0.667, Klepec ~ Kleppetz 0.625, Poddirec ~ Poldiŕg 0.625 …) ⑤ PUA keeps 16 rows in the 41–60 gap (P4) — 0 same-number matches ≥ 0.72 with 1886 (the nearest @56 Schumetz vs Šimec 0.667 [~]) ⑥ the three-source houses 13/36/71: 0/3 same-number name matches with 1825; IMPLICATION: the name level CONFIRMS the issue #18 warning — numeric consistency ≠ building identity ≠ family identity; the bridge requires per-house chronological chains (full transcription = owner priority); anchors: 57 src==parish verified against the bundled parish.ts (the other 4 — 1 p80 + 3 p79 — in the repo script); full independent recompute: same-house PT/ATLAS/PUA + census + PUA 41–60 + anchors from the pack runtime × PUA_CONTINUATION × ATLAS_OWNERS × HOUSE_VITALS; live verifier scripts/p81_parish_name_linkage.py (I1–I10, --check PASS, triple determinism); status NAME-LINKAGE-PACK",
  p81Errors.length === 0,
  p81Errors.length === 0
    ? `25 hiš (19 nabor / 6 luknja) × 232 imen 1825 · isto-hiša PT 0/19 (NIL-CLAIM) · isto-hiša PUA 2 (@36 Križan–Krischan 0.8333 · @71 Straus–Strauß 0.8571) · cenzus 10/38 = 26.32 % prič · near-miss 11 · PUA 41–60: 16 vrstic, 0 ujem · sidra 57/57 (+4 repo) · tri-virske 13/36/71: 0/3`
    : p81Errors.join("; "),
);

// ——— qa-p82: p82 krstna 1887 — širitev vzorca na leto 1887 (issue #18;
//      SAMPLE-TRANSCRIPTION-1887; celoven neodvisen preracun iz bundled
//      virov: HOUSE_VITALS × PARISH_BOOKS; PT klasifikacija iz pina;
//      sidro hiše 61 (P79 re-verify) + križna povezava hiše 31 (P80);
//      paleografska faza v research/issue17/parish-baptism-1887.json,
//      live verifikator scripts/p82_parish_baptism_1887.py --check I1–I10) ———
const p82Hv = HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year === 1887);
const p82Errors: string[] = [];
const P82_PT_IN_SET = ["2", "15", "17", "21", "24", "26", "27", "31", "34", "35", "61", "62", "63", "65", "66", "78"];
const P82_PT_GAP = ["47", "52", "55"];
if (p82Hv.length !== 20)
  p82Errors.push(`vpisov 1887 (04105) ≠ 20 (${p82Hv.length})`);
const p82Houses = new Set(p82Hv.map((h) => h.houseNo));
if (p82Houses.size !== 19)
  p82Errors.push(`različnih hiš ≠ 19 (${p82Houses.size}: ${[...p82Houses].sort((a, b) => Number(a) - Number(b)).join(",")})`);
const p82Book = PARISH_BOOKS.find((b) => b.signature === "04105");
if (!p82Book || p82Book.type !== "baptism" || p82Book.from !== 1886 || p82Book.to !== 1919)
  p82Errors.push("PARISH_BOOKS: 04105 (baptism 1886–1919) ni dokumentiran");
const p82Bad = p82Hv.filter((h) => h.status !== "DOCUMENTED" || !h.scan || !h.page || h.page !== h.scan - 1 || h.scan < 16 || h.scan > 27);
if (p82Bad.length > 0)
  p82Errors.push(`okvir 1887: skeni 16–27 ali stran ≠ sken − 1 krščeno pri ${p82Bad.length}`);
// sidro hiše 61 (P79 re-verify): row 28, sken 20, Katarina, oče zdaj »Miko Požek« [~]
const p82Anchor = p82Hv.find((h) => h.houseNo === "61" && h.scan === 20 && h.page === 19);
if (!p82Anchor || !p82Anchor.whatSi.includes("Katarina") || !p82Anchor.whatSi.includes("Miko Požek") || !p82Anchor.whatSi.includes("Miha P.—"))
  p82Errors.push("sidro hiša 61: scan/page/whatSi ≠ P82 re-read (Miko Požek [~] + Miha P.— ohranjeno)");
// PT klasifikacija == pin: 16 v naboru + 3 v luknji 41–60 (47, 52, 55)
const p82InSet = [...p82Houses].filter((h) => P82_PT_IN_SET.includes(h));
const p82Gap = [...p82Houses].filter((h) => P82_PT_GAP.includes(h));
if (p82InSet.length !== 16 || p82Gap.length !== 3)
  p82Errors.push(`PT klasifikacija ≠ 16/3 (${p82InSet.length}/${p82Gap.length})`);
if (p82Gap.some((h) => !(Number(h) >= 41 && Number(h) <= 60)))
  p82Errors.push("luknjane hiše izven 41–60");
// nezakonski vpisi (očeta stolpec prazen): hiši 52 in 55
const p82Illeg = p82Hv.filter((h) => (h.houseNo === "52" || h.houseNo === "55") && h.whatSi.includes("PRAZEN"));
if (p82Illeg.length !== 2)
  p82Errors.push(`nezakonski vpisi (52, 55) ≠ 2 (${p82Illeg.length})`);
// trojna korekcija hišne št. row 78: 52 → 04 → 15
const p82R78 = p82Hv.find((h) => h.houseNo === "52");
if (!p82R78 || !p82R78.whatSi.includes("52 → 04 → 15"))
  p82Errors.push("trojna korekcija hišne št. row 78 (52 → 04 → 15) ni dokumentirana");
// anomalija row 93 (hiša 35): žensko ime v očetovem stolpcu
const p82R93 = p82Hv.find((h) => h.houseNo === "35");
if (!p82R93 || !p82R93.whatSi.includes("ANOMALIJA ZAPISA"))
  p82Errors.push("anomalija zapisa row 93 (hiša 35) ni dokumentirana");
// križna povezava P80: hiša 31 v mrliški 1886 (04894)
const p82Cross = HOUSE_VITALS.some((h) => h.houseNo === "31" && h.bookSignature === "04894" && h.year === 1886);
if (!p82Cross)
  p82Errors.push("križna povezava hiša 31: mrliški vpis 1886 (04894) manjka");
// multi-vpis hiše 1887: samo 31 ×2 (Ana 1./2. 8. + Janez 6. 9.)
const p82Multi = ["31"].filter((h) => p82Hv.filter((v) => v.houseNo === h).length === 2);
if (p82Multi.length !== 1)
  p82Errors.push(`hiša z 2 vpisoma 1887 ≠ 31 (${p82Multi.join(",")})`);
push(
  "qa-p82-parish-baptism-1887",
  "P82: ŽUPNIJA PODZEMELJ — KRSTNA KNJIGA 04105, POLNO LETO 1887 (issue #18; SAMPLE-TRANSCRIPTION-1887; MERI, NE odloča; v7 join nespremenjen): širitev vzorca P79 (1886) na naslednje leto — okvir: skeni 16–27 == tiskane strani 15–26 (stran == sken − 1; glava »Leto 18_87« na str. 15; leto 1888 se začne NA STRANI 26 po row 106 z velikimi ciframi »1 8 8 8« — zadnji vpis 1887 row 106 (29./30. 12., Krasinec 7), prvi 1888 zvezno štetje row 107 (9./11. 1., Gradac 26) — P83 RE-READ: pisane oznake vrstic se pri prelomu leta PONASTAVIJO NA 1 (str. 27 = oznaka 3; pisana oznaka prve 1888 vrstice pod raztrganino [~] — »107« je zvezno štetje 106+1)) — VSI vpisi z Griblji: 20 vpisov / 19 različnih hiš (2, 15, 17, 21, 24, 26 [~], 27, 31×2, 34, 35, 47, 52→04→15 [~], 55, 61, 62, 63, 65, 66, 78 [~]) — NAD merili issue #18; vsak vpis: signatura + leto + stran/skan + hišna št. + otrok + starši + botre/babica (Kurrent z [~]); NOVI PT LUKNJI 47 in 55 (52 izvirno row 78 — trojna korekcija 52 → 04 → 15 [~]: izvirno v luknji, končna v naboru; obe klasifikaciji dokumentirani) — luknja 41–60 v krstnih vpisih: 54/56/57 (P79) + 44/59/60 (P80) + 47/52/55 (P82) = 9 dokazanih števil; P79 SIDRO hiša 61 re-verificirano (row 28, sken 20: oče zdaj »Miko Požek« [~] — prej »Miha P.—«/»Miko Jože H.?«, oba branji ohranjena; mati Bara roj. Filath [~]); NEZAKONSKI vpisi 2 (row 78 hiša 52: mati Marija Muc [~]; row 80 hiša 55: mati Ana Smič [~] — očeta stolpca PRAZNA); ANOMALIJA ZAPISA row 93 (hiša 35: v očetovem stolpcu »Marija Hrižan ½ zemljašt.«, v materinem »Ana Požek« — dve interpretaciji [~]); MULTI-VPIS: hiša 31 ×2 (Ana 1./2. 8. + Janez 6. 9.) — hiša 31 tudi v mrliški 1886 (Katarina Marh — P80) = križna povezava dveh knjig; TROI DUHOVNIKI 1887: kapljan Andrej Griebel [~] (14), župnik Franjo Dovgan (1), »Jos. Povmij« [~] (4 — nov podpis 1887); BABICA Marija Brinec 9× (gost porekla Brinec: mati 2×, očetje 1×, botre 3×); priimki čez leta: Šimec (1886: 36/39/56/88 → 1887: 34 — NOVA hiša), Straus (mati Margaretha @31 + botra Katarina @47), Filak/Filath (mati Bara @61 + babica @52), Stubler (mati @78), Požek (očeta @61/@21 + botra @27); live verifikacija: knjiga HTTP 200 (inventar 326), citirani skeni 8/8 JPEG 200; skripta scripts/p82_parish_baptism_1887.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1887",
  "P82: PARISH OF PODZEMELJ — BAPTISM REGISTER 04105, THE FULL YEAR 1887 (issue #18; SAMPLE-TRANSCRIPTION-1887; MEASURES, does not decide; the v7 join unchanged): extending the P79 sample (1886) to the next year — the frame: scans 16–27 == printed pages 15–26 (page == scan − 1; the header »Leto 18_87« on p. 15; the year 1888 begins ON PAGE 26 after row 106 with large numerals »1 8 8 8« — the last 1887 entry row 106 (Dec 29/30, Krasinec 7), the first 1888 row 107 (Jan 9/11, Gradac 26) — P83 RE-READ: the WRITTEN row labels restart at 1 at the year break (p. 27 starts with label 3; the written label of the first 1888 row lies under a tear [~] — »107« is the continuous count 106+1)) — ALL Griblje entries: 20 entries / 19 distinct houses (2, 15, 17, 21, 24, 26 [~], 27, 31×2, 34, 35, 47, 52→04→15 [~], 55, 61, 62, 63, 65, 66, 78 [~]) — ABOVE the issue #18 criteria; every entry: signature + year + page/scan + house number + child + parents + godparents/midwife (Kurrent with [~]); NEW PT GAPS 47 and 55 (52 originally row 78 — a triple correction 52 → 04 → 15 [~]: the original in the gap, the final in the set; both classifications documented) — the 41–60 gap in baptism entries: 54/56/57 (P79) + 44/59/60 (P80) + 47/52/55 (P82) = 9 proven numbers; the P79 ANCHOR house 61 re-verified (row 28, scan 20: the father now »Miko Požek« [~] — earlier »Miha P.—«/»Miko Jože H.?«, both readings preserved; mother Bara née Filath [~]); ILLEGITIMATE entries 2 (row 78 house 52: mother Marija Muc [~]; row 80 house 55: mother Ana Smič [~] — the fathers' columns EMPTY); RECORDING ANOMALY row 93 (house 35: the father's column holds »Marija Hrižan ½ zemljašt.«, the mother's »Ana Požek« — two interpretations [~]); MULTI-ENTRY: house 31 ×2 (Ana Aug 1/2 + Janez Sep 6) — house 31 also in the death register 1886 (Katarina Marh — P80) = a two-book cross-link; THREE PRIESTS 1887: curate Andrej Griebel [~] (14), parish priest Franjo Dovgan (1), »Jos. Povmij« [~] (4 — a new 1887 signature); MIDWIFE Marija Brinec 9× (the Brinec origin hub: mother 2×, fathers 1×, godmothers 3×); surnames across years: Šimec (1886: 36/39/56/88 → 1887: 34 — a NEW house), Straus (mother Margaretha @31 + godmother Katarina @47), Filak/Filath (mother Bara @61 + midwife @52), Stubler (mother @78), Požek (fathers @61/@21 + godfather @27); live verification: the book HTTP 200 (inventory 326), cited scans 8/8 JPEG 200; the script scripts/p82_parish_baptism_1887.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1887",
  p82Errors.length === 0,
  p82Errors.length === 0
    ? `20 vpisov / 19 hiš · okvir 1887 skeni 16–27 (stran == sken−1; 1888 prelom na str. 26, zvezno row 107 — pisane oznake se ponastavijo, P83) · PT 16/3 (47, 52, 55 v luknji — 9 dokazanih skupaj) · sidro 61 row 28 (Miko Požek [~]) · nezakonski 2 · anomalija row 93 · multi 31×2 · trije duhovniki · babica Brinec 9×`
    : p82Errors.join("; "),
);

// ——— qa-p83: p83 krstna 1888 — širitev vzorca na leto 1888 (issue #18;
//      SAMPLE-TRANSCRIPTION-1888; celoven neodvisen preracun iz bundled
//      virov: HOUSE_VITALS × PARISH_BOOKS; PT klasifikacija iz pinov;
//      sidra: h13 prva per-hišna veriga, h78 OSKRBAR, h29 Milek;
//      paleografska faza v research/issue17/parish-baptism-1888.json,
//      live verifikator scripts/p83_parish_baptism_1888.py --check I1–I10) ———
const p83Hv = HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year === 1888);
const p83Errors: string[] = [];
const P83_PT_IN_SET = ["1", "8", "13", "21", "24", "29", "69", "72", "78", "79", "83", "85"];
const P83_PT_GAP = ["44", "56", "57"];
if (p83Hv.length !== 15)
  p83Errors.push(`vpisov 1888 (04105) ≠ 15 (${p83Hv.length})`);
const p83Houses = new Set(p83Hv.map((h) => h.houseNo));
if (p83Houses.size !== 15)
  p83Errors.push(`različnih hiš ≠ 15 (${p83Houses.size}: ${[...p83Houses].sort((a, b) => Number(a) - Number(b)).join(",")})`);
const p83Book = PARISH_BOOKS.find((b) => b.signature === "04105");
if (!p83Book || p83Book.type !== "baptism" || p83Book.from !== 1886 || p83Book.to !== 1919)
  p83Errors.push("PARISH_BOOKS: 04105 (baptism 1886–1919) ni dokumentiran");
const p83Bad = p83Hv.filter((h) => h.status !== "DOCUMENTED" || !h.scan || !h.page || h.page !== h.scan - 1 || h.scan < 28 || h.scan > 34);
if (p83Bad.length > 0)
  p83Errors.push(`okvir 1888: skeni 28–34 ali stran ≠ sken − 1 krščeno pri ${p83Bad.length}`);
// sidro 1: hiša 13 — PRVA per-hišna imenska veriga (1885 poročna sidro +
// 1886 krst/mrliška + 1888 krst; Jakobič/Jakopič čez leta)
const p83H13 = p83Hv.find((h) => h.houseNo === "13" && h.scan === 31);
if (!p83H13 || !p83H13.whatSi.includes("Matija Jakobič") || !p83H13.whatSi.includes("Marija Perdinec") || !p83H13.whatSi.includes("TRI-VIRSKA"))
  p83Errors.push("sidro hiša 13: whatSi ≠ P83 (Matija Jakobič [~] × Marija Perdinec [~], TRI-VIRSKA, prva per-hišna veriga)");
const p83H13Chain =
  HOUSE_VITALS.some((v) => v.houseNo === "13" && v.bookSignature === "04455" && v.year === 1885) &&
  HOUSE_VITALS.some((v) => v.houseNo === "13" && v.bookSignature === "04105" && v.year === 1886) &&
  HOUSE_VITALS.some((v) => v.houseNo === "13" && v.bookSignature === "04894" && v.year === 1886);
if (!p83H13Chain)
  p83Errors.push("veriga hiše 13: 1885 poročna + 1886 krstna + 1886 mrliška manjkajo");
// sidro 2: hiša 78 — OSKRBAR (1886/1887 Jakobič → 1888 oskrbar Poxan)
const p83H78 = p83Hv.find((h) => h.houseNo === "78" && h.scan === 29);
if (!p83H78 || !p83H78.whatSi.includes("OSKRBAR") || !p83H78.whatSi.includes("Poxan"))
  p83Errors.push("sidro hiša 78: whatSi ≠ P83 (oskrbar Poxan [~])");
if (!HOUSE_VITALS.some((v) => v.houseNo === "78" && v.year === 1887 && v.scan === 20))
  p83Errors.push("hiša 78: 1887 sidro (sk. 20, P79 == P82 row 26) manjka");
// sidro 3: hiša 29 — Mileh (epidemija 1886) → Milek (1888)
const p83H29 = p83Hv.find((h) => h.houseNo === "29" && h.scan === 34);
if (!p83H29 || !p83H29.whatSi.includes("Milek") || !p83H29.whatSi.includes("epidemij"))
  p83Errors.push("sidro hiša 29: whatSi ≠ P83 (Milek, epidemija 1886)");
// PT klasifikacija == pin: 12 v naboru + 3 v luknji (44, 56, 57 — vse potrjitve, 0 novih)
const p83InSet = [...p83Houses].filter((h) => P83_PT_IN_SET.includes(h));
const p83Gap = [...p83Houses].filter((h) => P83_PT_GAP.includes(h));
if (p83InSet.length !== 12 || p83Gap.length !== 3)
  p83Errors.push(`PT klasifikacija ≠ 12/3 (${p83InSet.length}/${p83Gap.length})`);
if (p83Gap.some((h) => !(Number(h) >= 41 && Number(h) <= 60)))
  p83Errors.push("luknjane hiše izven 41–60");
// nezakonski vpisi 3 (24, 56, 21)
const p83Illeg = p83Hv.filter((h) => (h.houseNo === "24" || h.houseNo === "56" || h.houseNo === "21") && h.whatSi.includes("PRAZEN"));
if (p83Illeg.length !== 3)
  p83Errors.push(`nezakonski vpisi (24, 56, 21) ≠ 3 (${p83Illeg.length})`);
// ponastavitev številčenja vrstic (P83 novel): okvir + prelom 1889
if (!p83H13 || p83H13.whatSi.length === 0)
  p83Errors.push("hiša 13 whatSi prazno");
const p83Cross31 = HOUSE_VITALS.some((h) => h.houseNo === "31" && h.bookSignature === "04894" && h.year === 1886);
if (!p83Cross31)
  p83Errors.push("križna povezava hiša 31 (P80) manjka — kontekst multi-hiš");
push(
  "qa-p83-parish-baptism-1888",
  "P83: ŽUPNIJA PODZEMELJ — KRSTNA KNJIGA 04105, POLNO LETO 1888 (issue #18; SAMPLE-TRANSCRIPTION-1888; MERI, NE odloča; v7 join nespremenjen): širitev vzorca P79 (1886) → P82 (1887) na leto 1888 — okvir: skeni 27–35 == tiskane strani 26–34 (stran == sken − 1; vpisi na skenih 28–34; prelom 1889 »1 8 8 9« na str. 34 row 1 — prvi vpis 1889 = 3./3. 1., Gradac 8); NOVELA P83: PISANE OZNAKE VRSTIC SE PRI PRELOMU LETA PONASTAVIJO NA 1 (str. 27 = oznaka 3 — dokaz; pisana oznaka prve 1888 vrstice pod raztrganino [~]; P82 »row 107« = zvezno štetje 106+1, narativi qa-p82/p82 usklajeni) — VSI vpisi z Griblji: 15 vpisov / 15 različnih hiš (1, 8, 13, 21, 24, 29, 44, 56, 57, 69, 72, 78 [~], 79, 83, 85) — NOVE hiše v vzorcu 5 (1, 72, 79, 83, 85), ponovitve 10; PT klasifikacija 12/3 (44, 56, 57 v luknji 41–60 — VSE POTRDITVE, 0 novih števil; skupaj 11 dokazanih števil luknje čez tri knjige); NEZAKONSKI 3/15 (h24 mati Barbara Melith [~]; h56 mati Ana Šimec [~] — Šimec ZNOVA na 56; h21 mati Marija Požek [~] — priimek ist kot 1887 hišni oče); SIDRA: hiša 13 (row 53, sk. 31: oče Matija Jakobič [~] × Marija Perdinec [~] — TRI-VIRSKA hiša: 1885 poročna sidro + 1886 krst + 1886 mrliška + 1888 krst; Jakobič/Jakopič čez leta = PRVA per-hišna imenska veriga — najmočnejši kandidat za 1825→1886→1888 most), hiša 78 (row 24, sk. 29: oče Mihail Poxan [~] OSKRBAR — 1886/1887 Jakobič → 1888 oskrbar = socio-ekonomska motnja), hiša 29 (row 85, sk. 34: oče Peter Milek [~] — hiša epidemije 1886 Mileh ×3 → isti rod); NOVE familije po 1825: POŽEK (h79 oče bajtar + h21 nezakonska mati + botra — NI v vesolju 1825); P84 RE-READ NOVELA: »HRAUS/HRAUCELJ« (3 hiše 69/72/85 + babica) = STRAUŠ/STRAUCELJ — JE v vesolju 1825 (P81 0.8571), novela ODPADA; nasprotje: KRIŽAN 6 prič 1888 (oče h85, matere h79/h29, botre h69/h13/h21, babica h24) SE povezuje s 1825 (Krišan Gregor, Krischan @36 — P81 0.8333); ANOMALIJE: otrok »Kaxmarp« [~] (morda Kasimir), »Musca« [~], »Alex« [~] s nasprotjem spola (kolone moški [~] proti marginaliji »Umrla« [~]), dvodelni priimek »Radovič Mrgaič« [~] (vzporednica 1825 »Šture Majzel«), marginalije »+ 1878« pred rojstvom (7/8 forenzika); DUHOVNIKI: Grieblj [~] 12 + Povmij [~] 1 + neberljiv 1 + prazen 1; babica Brinec 10× (Marija 9 + Ana 1); live verifikacija: knjiga HTTP 200 (inventar 326), citirani skeni 6/6 JPEG 200; skripta scripts/p83_parish_baptism_1888.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1888",
  "P83: PARISH OF PODZEMELJ — BAPTISM REGISTER 04105, THE FULL YEAR 1888 (issue #18; SAMPLE-TRANSCRIPTION-1888; MEASURES, does not decide; the v7 join unchanged): extending the P79 (1886) → P82 (1887) sample to 1888 — the frame: scans 27–35 == printed pages 26–34 (page == scan − 1; entries on scans 28–34; the 1889 break »1 8 8 9« on p. 34 row 1 — the first 1889 entry = Jan 3, Gradac 8); the P83 NOVELTY: THE WRITTEN ROW LABELS RESTART AT 1 AT THE YEAR BREAK (p. 27 starts with label 3 — proof; the written label of the first 1888 row lies under a tear [~]; the P82 »row 107« is the continuous count 106+1, the qa-p82/p82 narratives aligned) — ALL Griblje entries: 15 entries / 15 distinct houses (1, 8, 13, 21, 24, 29, 44, 56, 57, 69, 72, 78 [~], 79, 83, 85) — 5 NEW sample houses (1, 72, 79, 83, 85), 10 repeats; the PT classification 12/3 (44, 56, 57 in the 41–60 gap — ALL CONFIRMATIONS, 0 new numbers; 11 proven gap numbers across the three books in total); ILLEGITIMATE 3/15 (h24 mother Barbara Melith [~]; h56 mother Ana Šimec [~] — Šimec AGAIN on 56; h21 mother Marija Požek [~] — the surname identical to the 1887 house father); ANCHORS: house 13 (row 53, scan 31: father Matija Jakobič [~] × Marija Perdinec [~] — the THREE-SOURCE house: 1885 marriage anchor + 1886 baptism + 1886 death + 1888 baptism; Jakobič/Jakopič across years = the FIRST per-house name chain — the strongest candidate for the 1825→1886→1888 bridge), house 78 (row 24, scan 29: father Mihail Poxan [~] the CARETAKER — 1886/1887 Jakobič → 1888 oskrbar = a socio-economic disruption), house 29 (row 85, scan 34: father Peter Milek [~] — the 1886 epidemic house Mileh ×3 → the same kin); NEW post-1825 families: POŽEK (h79 father the cottager + h21 the unmarried mother + a godmother — NOT in the 1825 universe); the P84 RE-READ NOVELTY: »HRAUS/HRAUCELJ« (3 houses 69/72/85 + the midwife) = STRAUŠ/STRAUCELJ — IS in the 1825 universe (P81 0.8571), the claim is WITHDRAWN; the contrast: KRIŽAN 6 witnesses in 1888 (father h85, mothers h79/h29, godparents h69/h13/h21, midwife h24) DOES connect to 1825 (Krišan Gregor, Krischan @36 — P81 0.8333); ANOMALIES: the child »Kaxmarp« [~] (possibly Kasimir), »Musca« [~], »Alex« [~] with a gender contradiction (the male columns [~] against the margin note »Umrla« [~]), the double surname »Radovič Mrgaič« [~] (a parallel to the 1825 »Šture Majzel«), margin notes »+ 1878« preceding the birth (the 7/8 forensics); PRIESTS: Grieblj [~] 12 + Povmij [~] 1 + illegible 1 + empty 1; the midwife Brinec 10× (Marija 9 + Ana 1); live verification: the book HTTP 200 (inventory 326), cited scans 6/6 JPEG 200; the script scripts/p83_parish_baptism_1888.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1888",
  p83Errors.length === 0,
  p83Errors.length === 0
    ? `15 vpisov / 15 hiš · okvir 1888 skeni 28–34 (stran == sken−1; prelom 1889 str. 34 row 1; pisane oznake se ponastavijo — str. 27 = oznaka 3) · PT 12/3 (44, 56, 57 v luknji — potrditve, 0 novih) · sidra h13 veriga / h78 oskrbar / h29 Milek · nezakonski 3 · Požek po 1825 + P84 RE-READ Hraus→Strauš (v vesolju 1825), Križan 6 prič · anomalije Kaxmarp/Musca/Alex/Radovič Mrgaič`
    : p83Errors.join("; "),
);

// ——— qa-p84: p84 krstna 1889 — širitev vzorca na leto 1889 (issue #18;
//      SAMPLE-TRANSCRIPTION-1889; celoven neodvisen preracun iz bundled
//      virov: HOUSE_VITALS × PARISH_BOOKS; PT klasifikacija iz pinov;
//      sidra: h63 Šimec=ATLAS, row 82 Filak babica, row 89 Dragoš botr,
//      h72 Strauš re-read; NOVELI: številčenje str. 40 (svinčnik 81–93)
//      + re-read P83 Hraus→Strauš; paleografska faza v
//      research/issue17/parish-baptism-1889.json, live verifikator
//      scripts/p84_parish_baptism_1889.py --check I1–I10) ———
const p84Hv = HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year === 1889);
const p84Errors: string[] = [];
const P84_PT_IN_SET = ["2", "3", "8", "26", "32", "33", "35", "63", "64", "65", "69", "72", "83"];
const P84_PT_GAP = ["57", "58", "59"];
if (p84Hv.length !== 17)
  p84Errors.push(`vpisov 1889 (04105, zasidrani) ≠ 17 (${p84Hv.length}) — dokaz 19, 2 neberljivi evidence-only`);
const p84Houses = new Set(p84Hv.map((h) => h.houseNo));
if (p84Houses.size !== 16)
  p84Errors.push(`različnih hiš ≠ 16 (${p84Houses.size}: ${[...p84Houses].sort((a, b) => Number(a) - Number(b)).join(",")})`);
const p84Book = PARISH_BOOKS.find((b) => b.signature === "04105");
if (!p84Book || p84Book.type !== "baptism" || p84Book.from !== 1886 || p84Book.to !== 1919)
  p84Errors.push("PARISH_BOOKS: 04105 (baptism 1886–1919) ni dokumentiran");
const p84Bad = p84Hv.filter((h) => h.status !== "DOCUMENTED" || !h.scan || !h.page || h.page !== h.scan - 1 || h.scan < 35 || h.scan > 42);
if (p84Bad.length > 0)
  p84Errors.push(`okvir 1889: skeni 35–42 ali stran ≠ sken − 1 krščeno pri ${p84Bad.length}`);
// sidro 1: hiša 63 — ATLAS 1825 Šimec @63 ↔ botr Janez Šimec (row 53, sk. 38)
const p84H63 = p84Hv.find((h) => h.houseNo === "63" && h.scan === 38);
if (!p84H63 || !p84H63.whatSi.includes("Janez Šimec") || !p84H63.whatSi.includes("ATLAS"))
  p84Errors.push("sidro hiša 63: whatSi ≠ P84 (botr Janez Šimec [~], ATLAS 1825 Šimec @63)");
// sidro 2: row 89 = hiša 8 — botr Janez Dragoš (P81 1.0) + mati Marija Urh (ista 1888)
const p84H8 = p84Hv.find((h) => h.houseNo === "8" && h.scan === 41);
if (!p84H8 || !p84H8.whatSi.includes("Janez Dragoš") || !p84H8.whatSi.includes("Marija Urh"))
  p84Errors.push("sidro hiša 8 (row 89): whatSi ≠ P84 (botr Janez Dragoš [~], mati Marija Urh [~])");
// sidro 3: hiša 72 — RE-READ P83 (oče Matija Strauš 1888 = 1889)
const p84H72 = p84Hv.find((h) => h.houseNo === "72" && h.scan === 39);
if (!p84H72 || !p84H72.whatSi.includes("Matija Strauš") || !p84H72.whatSi.includes("re-read"))
  p84Errors.push("sidro hiša 72: whatSi ≠ P84 (Matija Strauš [~] + re-read P83 nota)");
// PT klasifikacija == pin: 13 v naboru + 3 v luknji (57, 58, 59 — 58 NOVA)
const p84InSet = [...p84Houses].filter((h) => P84_PT_IN_SET.includes(h));
const p84Gap = [...p84Houses].filter((h) => P84_PT_GAP.includes(h));
if (p84InSet.length !== 13 || p84Gap.length !== 3)
  p84Errors.push(`PT klasifikacija ≠ 13/3 (${p84InSet.length}/${p84Gap.length})`);
if (p84Gap.some((h) => !(Number(h) >= 41 && Number(h) <= 60)))
  p84Errors.push("luknjane hiše izven 41–60");
if (!p84Hv.some((h) => h.houseNo === "58"))
  p84Errors.push("NOVA luknjana hiša 58 (P84 row 3) manjka");
// multi-vpisna hiša 64 (2 vpisa: sk. 36 + sk. 39)
const p84H64 = p84Hv.filter((h) => h.houseNo === "64");
if (p84H64.length !== 2 || new Set(p84H64.map((h) => h.scan)).size !== 2)
  p84Errors.push(`hiša 64 ×2 (multi-vpisna) ≠ 2 različna skena (${p84H64.map((h) => h.scan).join("/")})`);
// nezakonski 1 (h59 [~], mati Katarina Podirec, očeta stolpec PRAZEN)
const p84Illeg = p84Hv.filter((h) => h.houseNo === "59" && h.whatSi.includes("PRAZEN"));
if (p84Illeg.length !== 1)
  p84Errors.push(`nezakonski vpis (h59) ≠ 1 (${p84Illeg.length})`);
// ponovitve prek HOUSE_VITALS (h2/h8/h26/h63/h65/h83/h69/h72/h35/h57 04105
// prejšnja leta; h59 1886 iz mrliške 04894 — P80)
const p84Prev = (hn: string, yr: number, sig: string = "04105") =>
  HOUSE_VITALS.some((v) => v.houseNo === hn && v.bookSignature === sig && v.year === yr);
for (const [hn, yr, sig] of [["2", 1887, "04105"], ["8", 1888, "04105"], ["26", 1887, "04105"], ["63", 1887, "04105"], ["65", 1887, "04105"], ["83", 1888, "04105"], ["69", 1888, "04105"], ["72", 1888, "04105"], ["35", 1887, "04105"], ["57", 1888, "04105"], ["59", 1886, "04894"]] as const) {
  if (!p84Prev(hn, yr, sig))
    p84Errors.push(`ponovitev hiša ${hn} (${yr}, ${sig}) manjka v HOUSE_VITALS`);
}
push(
  "qa-p84-parish-baptism-1889",
  "P84: ŽUPNIJA PODZEMELJ — KRSTNA KNJIGA 04105, POLNO LETO 1889 (issue #18; SAMPLE-TRANSCRIPTION-1889; MERI, NE odloča; v7 join nespremenjen): širitev vzorca P79 (1886) → P82 (1887) → P83 (1888) na leto 1889 — okvir: skeni 35–43 == tiskane strani 34–42 (stran == sken − 1; vpisi na skenih 35–42; prelom 1890 »Leto 1890« na str. 42 row 1 — oznake se ponastavijo na 1; 1889 ima 106 zveznih vrstic); NOVELI P84: ① ŠTEVILČENJE STR. 40 — duhovnikove oznake PONOVLJENE 68–8x (napaka), modri svinčnik popravi ZVEZNO 81–93 v datumskih celicah (str. 41 zvezno 94–106 — neodvisna potrditev); ② RE-READ P83 — »HRAUS/HRAUCELJ« = STRAUŠ/STRAUCELJ (Kurrent ſt brana kot H; v isti p83 vrstici babica jasno »Neža Straucelj«; familija JE v vesolju 1825 — P81 0.8571 Strauß; P83 »dve novi familiji« → ENA nova, Požek; h72 oče 1888 = 1889 isti Matija Strauš; h57 botra 1888 = 1889 ista Marija Straucelj) — VSI vpisi z Griblji: 19 vpisov / 16 imenovanih hiš + 2 NEBERLJIVI (row 70 »///«, row 82 prekrita — evidence-only; HOUSE_VITALS 17 zasidranih): 58, 33, 3 [~], 64 ×2 (multi-vpisna), 35, 69, 59 [~], 63, 57, 32, 72, 2, 8 [~], 83 [~], 65, 26 [~] — NOVE hiše 5 (58, 33, 3, 32, 64) + 2 neberljivi, ponovitve 11; skupaj s P79/P80/P82/P83 vzorec 93 vpisov / 50 hiš čez tri knjige in štiri leta; PT klasifikacija 13/3 (57, 58, 59 v luknji 41–60 — 58 NOVA, 59 P80 + 57 P79 POTRDITVI; luknja zdaj 12 dokazanih števil); NEZAKONSKI 1/19 (h59 [~] mati Katarina Podirec »a samka?«) + ANOMALIJA row 70 (mati Marija Šimec [~] »samka hči« × oče Janez Jakobič [~] »šefur« — dve gospodinjstvi; otrok »Ožbolt?« [~]); SIDRA: hiša 63 (row 53, sk. 38: botr Janez ŠIMEC [~] — ATLAS 1825 Šimec @63 + PT lastnik »Šimec Ripane« @63 → NEPOSREDNA 1825↔1889 imenska + hišna povezava), row 82 (babica Ana FILAK [~] — P81 1.0 priča), row 89 = h8 (botr Janez DRAGOŠ [~] — P81 1.0; mati Marija Urh [~] ISTA kot 1888), h72 (re-read veriga: oče Matija Strauš 1888 + 1889); Šimec najtrajnejša: mati row 70 + botr row 53 (h63 = ATLAS hiša!) + botra row 75 (h2) — 3 pojavi; priimki z 1825 pričo v 1889: Dragoš 2× (1.0), Strauš/Straucelj 6× (0.8571 + re-read), Šimec 3× (1.0), Brinec 9× (0.8333 [~]), Filak 1× (1.0), Hrižan/Križan [~] 4× (0.8333 — babica z naslovom hiše 63!), Jakobič 4× (veriga h13), Milek 2× (near-miss); DUHOVNIKI: Griebel [~] 7 + Povmij [~] 8 + neberljivo 4 (raztrganine); babice: Brinec 7× + Ana Hrižan [~] 4× + Sotter 2× + Kure/Tržan/Filak po 1×; live verifikacija: knjiga HTTP 200 (inventar 326), citirani skeni 8/8 JPEG 200; skripta scripts/p84_parish_baptism_1889.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1889",
  "P84: PARISH OF PODZEMELJ — BAPTISM REGISTER 04105, THE FULL YEAR 1889 (issue #18; SAMPLE-TRANSCRIPTION-1889; MEASURES, does not decide; the v7 join unchanged): extending the P79 (1886) → P82 (1887) → P83 (1888) sample to 1889 — the frame: scans 35–43 == printed pages 34–42 (page == scan − 1; entries on scans 35–42; the 1890 break »Leto 1890« on p. 42 row 1 — the labels restart at 1; 1889 has 106 continuous rows); the P84 NOVELTIES: ① THE PAGE-40 NUMBERING — the priest's row labels REPEATED 68–8x (an error), a later hand (blue pencil) corrects to the CONTINUOUS 81–93 in the date cells (p. 41 continues 94–106 — an independent confirmation); ② THE P83 RE-READ — »HRAUS/HRAUCELJ« = STRAUŠ/STRAUCELJ (the Kurrent ſt read as H; in the same p83 row the midwife clearly reads »Neža Straucelj«; the family IS in the 1825 universe — P81 0.8571 Strauß; P83's »two new families« → ONE new family, Požek; the h72 father 1888 = 1889 the same Matija Strauš; the h57 godmother 1888 = 1889 the same Marija Straucelj) — ALL Griblje entries: 19 entries / 16 named houses + 2 ILLEGIBLE (row 70 »///«, row 82 covered — evidence-only; HOUSE_VITALS 17 anchored): 58, 33, 3 [~], 64 ×2 (multi-entry), 35, 69, 59 [~], 63, 57, 32, 72, 2, 8 [~], 83 [~], 65, 26 [~] — 5 NEW houses (58, 33, 3, 32, 64) + 2 illegible, 11 repeats; with P79/P80/P82/P83 the sample totals 93 entries / 50 houses across three books and four years; the PT classification 13/3 (57, 58, 59 in the 41–60 gap — 58 NEW, 59 P80 + 57 P79 CONFIRMATIONS; the gap now has 12 proven numbers); ILLEGITIMATE 1/19 (h59 [~] mother Katarina Podirec »a samka?«) + the ANOMALY row 70 (mother Marija Šimec [~] »unmarried daughter« × father Janez Jakobič [~] »farmhand« — two households; the child »Ožbolt?« [~]); ANCHORS: house 63 (row 53, scan 38: godfather Janez ŠIMEC [~] — the 1825 ATLAS Šimec @63 + the PT owner »Šimec Ripane« @63 → a DIRECT 1825↔1889 name + house link), row 82 (midwife Ana FILAK [~] — the P81 1.0 evidence), row 89 = h8 (godfather Janez DRAGOŠ [~] — P81 1.0; mother Marija Urh [~] the SAME as 1888), h72 (the re-read chain: father Matija Strauš 1888 + 1889); Šimec the most persistent: mother row 70 + godfather row 53 (h63 = an ATLAS house!) + godmother row 75 (h2) — 3 appearances; surnames with 1825 evidence in 1889: Dragoš 2× (1.0), Strauš/Straucelj 6× (0.8571 + re-read), Šimec 3× (1.0), Brinec 9× (0.8333 [~]), Filak 1× (1.0), Hrižan/Križan [~] 4× (0.8333 — the midwife with a house address 63!), Jakobič 4× (the h13 chain), Milek 2× (near-miss); PRIESTS: Griebel [~] 7 + Povmij [~] 8 + illegible 4 (tears); midwives: Brinec 7× + Ana Hrižan [~] 4× + Sotter 2× + Kure/Tržan/Filak 1× each; live verification: the book HTTP 200 (inventory 326), cited scans 8/8 JPEG 200; the script scripts/p84_parish_baptism_1889.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1889",
  p84Errors.length === 0,
  p84Errors.length === 0
    ? `19 vpisov / 16 imenovanih hiš + 2 neberljivi (17 zasidranih v vitals) · okvir 1889 skeni 35–42 (stran == sken−1; prelom 1890 str. 42 row 1; 106 zveznih vrstic) · noveli: str. 40 svinčnik 81–93 + RE-READ P83 Hraus→Strauš · PT 13/3 (58 NOVA, 59/57 potrditvi) · sidra h63 Šimec=ATLAS / row 82 Filak / row 89 Dragoš / h72 re-read · nezakonski 1 + anomalija samka×šefur`
    : p84Errors.join("; "),
);
// ——— qa-p85: p85 krstna 1890 — širitev vzorca na leto 1890 (issue #18;
//      SAMPLE-TRANSCRIPTION-1890; celoven neodvisen preracun iz bundled
//      virov: HOUSE_VITALS × PARISH_BOOKS; PT klasifikacija iz pinov;
//      sidra: h77 Požek bajtar = P83 h79, h71 Strauš oče (PUA @71), h63
//      Križan na P84 Šimec ATLAS sidru, h55 Šimec na luknji; NOVELA: status
//      = ulomek ½/¼ (prej brano »ž«); anomalija h35 == P82 row 93 (čez-letna
//      potrditev); paleografska faza v research/issue17/parish-baptism-1890.json,
//      live verifikator scripts/p85_parish_baptism_1890.py --check I1–I10) ———
const p85Hv = HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year === 1890);
const p85Errors: string[] = [];
const P85_PT_IN_SET = ["7", "11", "15", "24", "27", "30", "31", "32", "35", "38", "63", "69", "71", "77", "90"];
const P85_PT_GAP = ["41", "47", "55", "58"];
if (p85Hv.length !== 21)
  p85Errors.push(`vpisov 1890 (04105, zasidrani) ≠ 21 (${p85Hv.length}) — dokaz 24, 3 evidence-only`);
const p85Houses = new Set(p85Hv.map((h) => h.houseNo));
if (p85Houses.size !== 19)
  p85Errors.push(`različnih hiš ≠ 19 (${p85Houses.size}: ${[...p85Houses].sort((a, b) => Number(a) - Number(b)).join(",")})`);
const p85Bad = p85Hv.filter((h) => h.status !== "DOCUMENTED" || !h.scan || !h.page || h.page !== h.scan - 1 || h.scan < 43 || h.scan > 49);
if (p85Bad.length > 0)
  p85Errors.push(`okvir 1890: skeni 43–49 ali stran ≠ sken − 1 krščeno pri ${p85Bad.length}`);
// sidro 1: hiša 77 — Jurij Pošek bajtar (= P83 h79 oče 1888) + botra Barbara Požek
const p85H77 = p85Hv.find((h) => h.houseNo === "77" && h.scan === 46);
if (!p85H77 || !p85H77.whatSi.includes("BAJTAR") || !p85H77.whatSi.includes("h79"))
  p85Errors.push("sidro hiša 77: whatSi ≠ P85 (Jurij Pošek/Požek BAJTAR = P83 sidro h79)");
// sidro 2: hiša 71 — oče Jurij Straus (tri-virska P80 + PUA Strauß Niklo @71)
const p85H71 = p85Hv.find((h) => h.houseNo === "71" && h.scan === 44);
if (!p85H71 || !p85H71.whatSi.includes("Jurij Straus") || !p85H71.whatSi.includes("PUA"))
  p85Errors.push("sidro hiša 71: whatSi ≠ P85 (oče Jurij Straus [~], PUA Strauß Niklo @71)");
// sidro 3: hiša 63 — Križan × Pendirec na P84 Šimec ATLAS sidru (4. gospodinjstvo)
const p85H63 = p85Hv.find((h) => h.houseNo === "63" && h.scan === 48);
if (!p85H63 || !p85H63.whatSi.includes("Nikolaj Križan") || !p85H63.whatSi.includes("ATLAS"))
  p85Errors.push("sidro hiša 63: whatSi ≠ P85 (Nikolaj Križan [~], P84 Šimec ATLAS sidro)");
// sidro 4: hiša 55 — oče Nikolaj Šimec (Šimec na luknji 55)
const p85H55 = p85Hv.find((h) => h.houseNo === "55" && h.scan === 48);
if (!p85H55 || !p85H55.whatSi.includes("Nikolaj Šimec") || !p85H55.whatSi.includes("luknji 55"))
  p85Errors.push("sidro hiša 55: whatSi ≠ P85 (oče Nikolaj Šimec [~], Šimec na luknji 55)");
// PT klasifikacija == pin: 14 v naboru + 4 v luknji (41 NOVA + 47/55/58 potrditvi)
const p85InSet = [...p85Houses].filter((h) => P85_PT_IN_SET.includes(h));
const p85Gap = [...p85Houses].filter((h) => P85_PT_GAP.includes(h));
if (p85InSet.length !== 15 || p85Gap.length !== 4)
  p85Errors.push(`PT klasifikacija ≠ 15/4 (${p85InSet.length}/${p85Gap.length})`);
if (p85Gap.some((h) => !(Number(h) >= 41 && Number(h) <= 60)))
  p85Errors.push("luknjane hiše izven 41–60");
if (!p85Hv.some((h) => h.houseNo === "41"))
  p85Errors.push("NOVA luknjana hiša 41 (P85 rows 71+72) manjka");
// multi-vpisni: h30 (dvojčka, 2 vpisa isti sken 46) + h41 (2 vpisa, 2 različni
// gospodinjstvi — vzorec h36 1886/h64 1889)
const p85H30 = p85Hv.filter((h) => h.houseNo === "30");
if (p85H30.length !== 2 || !p85H30.every((h) => h.scan === 46))
  p85Errors.push(`hiša 30 ×2 (dvojčka) ≠ 2 vpisa na skenu 46 (${p85H30.map((h) => h.scan).join("/")})`);
const p85H41 = p85Hv.filter((h) => h.houseNo === "41");
if (p85H41.length !== 2 || !p85H41.every((h) => h.scan === 48))
  p85Errors.push(`hiša 41 ×2 (dve družini) ≠ 2 vpisa na skenu 48 (${p85H41.map((h) => h.scan).join("/")})`);
// anomaliji z ženskim imenom v očetovem stolpcu (r19 h24 + r85 h35 == P82 row 93)
const p85Anom = p85Hv.filter((h) => h.whatSi.includes("ANOMALIJA"));
if (p85Anom.length !== 2 || !p85Anom.some((h) => h.houseNo === "35") || !p85Anom.some((h) => h.houseNo === "24"))
  p85Errors.push(`anomaliji (h24 + h35) ≠ 2 (${p85Anom.map((h) => h.houseNo).join("/")})`);
const p85H35 = p85Anom.find((h) => h.houseNo === "35");
if (!p85H35 || !p85H35.whatSi.includes("Marija Hrižan") || !p85H35.whatSi.includes("P82 row 93"))
  p85Errors.push("čez-letna anomalija h35: whatSi ≠ P85 (Marija Hrižan [~] == P82 row 93)");
// ponovitve prek HOUSE_VITALS (13 ponovljenih hiš 1890; h15 1886 iz mrliške 04894 — P80)
const p85Prev = (hn: string, yr: number, sig: string = "04105") =>
  HOUSE_VITALS.some((v) => v.houseNo === hn && v.bookSignature === sig && v.year === yr);
for (const [hn, yr, sig] of [
  ["27", 1887, "04105"], ["31", 1887, "04105"], ["47", 1887, "04105"], ["24", 1887, "04105"],
  ["58", 1889, "04105"], ["71", 1886, "04105"], ["15", 1886, "04894"], ["69", 1888, "04105"],
  ["55", 1887, "04105"], ["32", 1889, "04105"], ["11", 1886, "04105"], ["63", 1889, "04105"],
  ["35", 1887, "04105"],
] as const) {
  if (!p85Prev(hn, yr, sig))
    p85Errors.push(`ponovitev hiša ${hn} (${yr}, ${sig}) manjka v HOUSE_VITALS`);
}
// NOVE hiše 1890 (7, 38, 77, 90, 30, 41) — ne obstajajo v nobenem prejšnjem
// letu; h30: P86 kontinuiteta dovoli tudi blok 1891 (isti starši + botra);
// h90: P87 kontinuiteta dovoli tudi blok 1892 (učitelj ISTA družina);
// h90: P93 kontinuiteta dovoli tudi blok 1898 (NOVI učitelj Vetročnik — šolska hiša);
// h90: P95 kontinuiteta dovoli blok 1900 (4. PIN šolska hiša — Leopoldina po materi)
// h30: P90 kontinuiteta dovoli tudi blok 1895 (3. družina Šegina);
// h30/h41: P91 kontinuiteta dovoli bloka 1896 (ISTA zvezi)
for (const hn of ["7", "30", "38", "41", "77", "90"]) {
  const allow = hn === "30" ? [1890, 1891, 1893, 1895, 1896, 1899, 1902, 1903, 1906, 1908, 1909, 1911, 1918] : hn === "90" ? [1890, 1892, 1898, 1900, 1908, 1910, 1912, 1914, 1919] : hn === "41" ? [1890, 1893, 1896, 1899] : hn === "7" ? [1890, 1901, 1905, 1907] : hn === "77" ? [1890, 1902, 1909, 1914, 1917] : [1890]; // P94: + 1899 bloka (h30 4. družina Županič; h41 4. VPIS ISTA ZVEZA); P95: + 1900 blok h90; P96: + 1901 blok h7 (2. VPIS); P97: + 1902 bloka h30 (5. DRUŽINA — SEGINA VRNITEV) + h77 (2. VPIS — MENJAVA Pošek → Cindrič); P98: + 1903 blok h30 (2. VPIS ZAPORED — Segina); P100: + 1905 blok h7 (3. VPIS — Jakob Toter, 1901 par); P101: + 1906 blok h30 (10. VPIS — MENJAVA Segina → Brinec); P102: + 1907 blok h7 (4. VPIS — ISTA Toter družina); P103: + 1908 bloka h30 (11. VPIS — SEGINA POVRAT) + h90 (5. VPIS — TRETJA učiteljska); P104: + 1909 bloka h30 (12. VPIS — 7. DRUŽINA Martinovič?) + h77 (3. VPIS — POŽEK POVRAT); P105: + 1910 blok h90 (6. VPIS — 2. Kalan, 4. učiteljska); P106: + 1911 blok h30 (13. VPIS — SEGINA POVRAT) P107: + 1912 blok h90 (7. VPIS — Kalan + RAZVEZAL 1953); P109: + 1914 bloka h77 (4. VPIS — ŠAHTAR!) + h90 (8. VPIS — Ernest Šušteršič UČITELJ); P112: + 1917 blok h77 (5. VPIS — Sočik? [~]); P113: + 1918 blok h30 (13. VPIS — Šegina, VRZEL 6 LET!); P114: + 1919 blok h90 (9. VPIS — 1. učitelj-oče na Gribljih!)
  if (HOUSE_VITALS.some((v) => v.houseNo === hn && !(v.bookSignature === "04105" && allow.includes(v.year)) && !(v.bookSignature === "04455" && v.year === 1889 && (hn === "7" || hn === "30")) && !(v.bookSignature === "04455" && v.year === 1892 && hn === "30") && !(v.bookSignature === "04455" && v.year === 1900 && hn === "7") && !(v.bookSignature === "04455" && v.year === 1902 && hn === "30") && !(v.bookSignature === "04455" && v.year === 1903 && hn === "41") && !(v.bookSignature === "04455" && v.year === 1904 && hn === "38") && !(v.bookSignature === "04455" && v.year === 1905 && hn === "30") && !(v.bookSignature === "04455" && v.year === 1907 && hn === "7") && !(v.bookSignature === "04455" && v.year === 1909 && hn === "30"))) // P118: + poročni bloka h7/h30-1889; P138: + poročni blok h30-1909 (№6 nevesta Maria MLEK — 3. poročni dokaz h30!) (1. poročni dokaz!); P121: + poročni blok h30-1892 (v5 nevesta Margareth Milek — 1. poročni dokaz h30-1892!); P129: + poročni blok h7-1900 (v2 EDINA GRIBLJE poroka — 1. poročni dokaz!); P131: + poročna bloka h30-1902 (v4 3. poročni dokaz h30 — DRUBEL!); P132: + poročni blok h41-1903 (v3 nevesta Maria Huestič — 1. poročni dokaz h41, DRUBEL!); P133: + poročni blok h38-1904 (v5 nevesta Margareth Šimec — 1. poročni dokaz h38 = GANSLER-hiša, DRUBEL!); P134: + poročni blok h30-1905 (v4 nevesta Maria GRABRIJAN — 4. poročni dokaz h30, DRUBEL!); P136: + poročni blok h7-1907 (v5 nevesta Theresia KRIŽAN — 3. poročni dokaz h7, GRIBLJE-DRUBEL s h6!)
    p85Errors.push(`NOVA hiša ${hn} (P85) že obstaja v prejšnjem letu — pini neskladni`);
}
push(
  "qa-p85-parish-baptism-1890",
  "P85: ŽUPNIJA PODZEMELJ — KRSTNA KNJIGA 04105, POLNO LETO 1890 (issue #18; SAMPLE-TRANSCRIPTION-1890; MERI, NE odloča; v7 join nespremenjen): širitev vzorca P79 (1886) → P82 (1887) → P83 (1888) → P84 (1889) na leto 1890 — okvir: skeni 43–49 == tiskane strani 42–48 (stran == sken − 1; vpisi na skenih 43–49; prelom 1891 velike cifre »1891.« na str. 48 row 1 po row 86 — oznake se ponastavijo na 1, novela P83 potrjena 3. leto; 1890 ima 86 zveznih vrstic; glave mesecev se ponavljajo — Marec 2×, April 2×, Junij 2×); NOVELA P85: STATUS = ULOMEK — Kurrent znak pred »zemljak« (P79–P84 brana »ž zemljaf«) je z jasnimi izrezi 1890 ULOMEK ½ (ali ¼) — 15/24 vpisov; isti znak kot P84 row 3 »¼ zemljišč« — VSI vpisi z Griblji: 24 vpisov / 19 imenovanih hiš + 3 NEBERLJIVI (r31 + r75 prekriti z modrimi pripisi, r77 rez strani — evidence-only; HOUSE_VITALS 21 zasidranih): 27, 31, 47, 24, 58, 71, 38, 15, 77, 30 ×2 (DVOJČKA — prvi v vzorcu!), 7, 69, 55, 32, 11, 41 ×2 (multi-vpisna, dve različni družini — vzorec h36/h64), 63, 90, 35 — NOVE hiše 6 (7, 30, 38, 41, 77, 90) + 3 neberljive, ponovitve 13; skupaj s P79–P84 vzorec 117 vpisov / 56 hiš čez tri knjige in pet let; PT klasifikacija 15/4 (41, 47, 55, 58 v luknji 41–60 — 41 NOVA z 2 vpisoma, 47/55/58 POTRDITVI; luknja zdaj 13 dokazanih števil); 0 čistih nezakonskih, 2 ANOMALIJI z ženskim imenom v očetovem stolpcu (r19 h24 »Marija Brinec ½ zemljak«; r85 h35 »Marija Hrižan ½ zemljak« × Ana Požek = ČEZ-LETNA POTRDITEV P82 row 93 — isti nepravilni vpis na isti hiši 1887 IN 1890) + r85 otrok brez imena (»N. moškega spola«); SIDRA: h77 (oče Jurij Pošek/Požek BAJTAR = P83 sidro h79 oče 1888 + botra Barbara Požek = P83 h79 botra — Požek veriga 79→77, 3. leto), h71 (oče Jurij Straus — tri-virska P80 + PUA Strauß Niklo @71, P81 0.8571), h63 (oče Nikolaj KRIŽAN — prvi Križan hišni oče; na P84 Šimec ATLAS sidru — 4. gospodinjstvo), h55 (oče Nikolaj ŠIMEC — Šimec zdaj tudi na luknji 55, 6. hiša najtrajnejše familije); priimki z 1825 pričo v 1890: Strauš 7× (0.8571), Šimec 4× (1.0), Križan/Hrižan 6× (0.8333 [~]), Dragoš 2× (1.0), Brinec 3× gospodinjsko + babica 11× (0.8333 [~]), Filak 1× (1.0), Milek 2× (near-miss), Klobučar 4×, Urh 2×, Požek 7× (nova familija 1888 — 3. leto), Pendirec/Pegdirec 9×; DUHOVNIKI: Jos. Rauq [~] 19 (isti tip pisave kot P84 »Griebel/Povmij« [~]) + Jos. G— [~] 1 + C. g. Jurcan Šašelj, župr v D. Lazič [~] 1 (obiskni — edini popolnoma berljiv) + prazna 2; babice: Brinec 11× (4. leto) + Šotter 6× + Ana Križan 2×; statusi: 15× ulomek ½/¼ + bajtarja 2 + čevljar + učitelj (šolska hiša 90) + mežnar iz Adlešič; live verifikacija: knjiga HTTP 200 (inventar 326), citirani skeni 7/7 JPEG 200; skripta scripts/p85_parish_baptism_1890.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1890",
  "P85: PARISH OF PODZEMELJ — BAPTISM REGISTER 04105, THE FULL YEAR 1890 (issue #18; SAMPLE-TRANSCRIPTION-1890; MEASURES, does not decide; the v7 join unchanged): extending the P79 (1886) → P82 (1887) → P83 (1888) → P84 (1889) sample to 1890 — the frame: scans 43–49 == printed pages 42–48 (page == scan − 1; entries on scans 43–49; the 1891 break big digits »1891.« on p. 48 row 1 after row 86 — the labels restart at 1, the P83 novel confirmed for the 3rd year; 1890 has 86 continuous rows; month headers repeat — March 2×, April 2×, June 2×); the P85 NOVEL: STATUS = A FRACTION — the Kurrent mark before »zemljak« (read »ž« in P79–P84) is, with clear crops in 1890, a FRACTION ½ (or ¼) — 15/24 entries; the same mark as the P84 row 3 »¼«; ALL Griblje entries: 24 entries / 19 named houses + 3 ILLEGIBLE (r31 + r75 covered by blue notes, r77 page-edge cut — evidence-only; HOUSE_VITALS 21 anchored): 27, 31, 47, 24, 58, 71, 38, 15, 77, 30 ×2 (TWINS — the first in the sample!), 7, 69, 55, 32, 11, 41 ×2 (multi-entry, two different families — the h36/h64 pattern), 63, 90, 35 — 6 NEW houses (7, 30, 38, 41, 77, 90) + 3 illegible, 13 repeats; with P79–P84 the sample totals 117 entries / 56 houses across three books and five years; the PT classification 15/4 (41, 47, 55, 58 in the 41–60 gap — 41 NEW with 2 entries, 47/55/58 CONFIRMATIONS; the gap now has 13 proven numbers); 0 clean illegitimates, 2 ANOMALIES with a female name in the father column (r19 h24 »Marija Brinec ½«; r85 h35 »Marija Hrižan ½« × Ana Požek = the CROSS-YEAR CONFIRMATION of P82 row 93 — the same irregular entry on the same house in 1887 AND 1890) + r85 an unnamed child (»male sex«); ANCHORS: h77 (father Jurij Pošek/Požek cottager = the P83 h79 anchor father of 1888 + godmother Barbara Požek = the P83 h79 godmother — the Požek chain 79→77, 3rd year), h71 (father Jurij Straus — the three-source P80 house + PUA Strauß Niklo @71, P81 0.8571), h63 (father Nikolaj KRIŽAN — the first Križan house-father; on the P84 Šimec ATLAS anchor — the 4th household), h55 (father Nikolaj ŠIMEC — Šimec now also on gap 55, the 6th house of the most persistent family); surnames with 1825 evidence in 1890: Strauš 7× (0.8571), Šimec 4× (1.0), Križan/Hrižan 6× (0.8333 [~]), Dragoš 2× (1.0), Brinec 3× household + midwife 11× (0.8333 [~]), Filak 1× (1.0), Milek 2× (near-miss), Klobučar 4×, Urh 2×, Požek 7× (the 1888 new family — 3rd year), Pendirec/Pegdirec 9×; PRIESTS: Jos. Rauq [~] 19 (the same hand type as the P84 »Griebel/Povmij« [~]) + Jos. G— [~] 1 + C. g. Jurcan Šašelj, priest in D. Lazič [~] 1 (visiting — the only fully legible) + empty 2; midwives: Brinec 11× (4th year) + Šotter 6× + Ana Križan 2×; statuses: 15× fraction ½/¼ + 2 cottagers + shoemaker + teacher (school house 90) + sexton from Adlešič; live verification: the book HTTP 200 (inventory 326), cited scans 7/7 JPEG 200; the script scripts/p85_parish_baptism_1890.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1890",
  p85Errors.length === 0,
  p85Errors.length === 0
    ? `24 vpisov / 19 imenovanih hiš + 3 neberljive (21 zasidranih v vitals) · okvir 1890 skeni 43–49 (stran == sken−1; prelom 1891 str. 48 row 1 po row 86; 86 zveznih vrstic) · NOVELA: status = ulomek ½/¼ (15/24) · PT 15/4 (41 NOVA ×2, 47/55/58 potrditvi) · dvojčka h30 (prvi v vzorcu) + multi h41 (dve družini) · sidra h77 Požek bajtar = P83 h79 / h71 Strauš oče = PUA @71 / h63 Križan na Šimec ATLAS sidru / h55 Šimec · anomalija h35 == P82 row 93 (čez-letno!)`
    : p85Errors.join("; "),
);
// ——— qa-p86: p86 krstna 1891 — širitev vzorca na leto 1891 (issue #18;
//      SAMPLE-TRANSCRIPTION-1891; celoven neodvisen preracun iz bundled
//      virov: HOUSE_VITALS × PARISH_BOOKS; PT klasifikacija iz pinov;
//      sidra: h72 Straus = P83 1888 (mati menjana), h30 Milek = P85
//      kontinuiteta (isti starši + ista botra), h61 Pošek/Požek = P82 sidro
//      1887 (ISTA OSEBA; mati menjana Filak→Dragos), h53 NOVA LUKNJA (14.),
//      h2 trojna kontinuiteta (P82+P84+P86 isti starši), h28 Požek 3. hiša
//      familije, h31 Straus mati ISTA OSEBA ×3; NOVELA: vsi 9 statusi = ¼
//      ulomek (novela P85 potrjena 2. leto); paleografska faza v
//      research/issue17/parish-baptism-1891.json, live verifikator
//      scripts/p86_parish_baptism_1891.py --check I1–I10) ———
const p86Hv = HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year === 1891);
const p86Errors: string[] = [];
const P86_PT_IN_SET = ["2", "5", "28", "30", "31", "61", "62", "72"];
const P86_PT_GAP = ["53"];
if (p86Hv.length !== 9)
  p86Errors.push(`vpisov 1891 (04105, zasidrani) ≠ 9 (${p86Hv.length}) — dokaz 10, 1 evidence-only`);
const p86Houses = new Set(p86Hv.map((h) => h.houseNo));
if (p86Houses.size !== 9)
  p86Errors.push(`različnih hiš ≠ 9 (${p86Houses.size}: ${[...p86Houses].sort((a, b) => Number(a) - Number(b)).join(",")})`);
const p86Bad = p86Hv.filter((h) => h.status !== "DOCUMENTED" || !h.scan || !h.page || h.page !== h.scan - 1 || h.scan < 50 || h.scan > 54);
if (p86Bad.length > 0)
  p86Errors.push(`okvir 1891: skeni 50–54 ali stran ≠ sken − 1 krščeno pri ${p86Bad.length}`);
// sidro 1: hiša 72 — Matija Straus (ISTI očet kot P83 1888; mati menjana)
const p86H72 = p86Hv.find((h) => h.houseNo === "72" && h.scan === 50);
if (!p86H72 || !p86H72.whatSi.includes("Matija Straus") || !p86H72.whatSi.includes("P83"))
  p86Errors.push("sidro hiša 72: whatSi ≠ P86 (Matija Straus [~] = P83 1888; mati menjana Husič→Jakobič)");
// sidro 2: hiša 30 — Janez Milek (P85 dvojčka kontinuiteta — isti starši + ista botra)
const p86H30 = p86Hv.find((h) => h.houseNo === "30" && h.scan === 51);
if (!p86H30 || !p86H30.whatSi.includes("Janez Milek") || !p86H30.whatSi.includes("P85"))
  p86Errors.push("sidro hiša 30: whatSi ≠ P86 (Janez Milek [~], kontinuiteta P85 dvojčki rows 51+52)");
// sidro 3: hiša 61 — Nikolaj Pošek/Požek (P82 SIDRO 1887 ISTA OSEBA; mati menjana Filak→Dragos)
const p86H61 = p86Hv.find((h) => h.houseNo === "61" && h.scan === 52);
if (!p86H61 || !p86H61.whatSi.includes("Pošek") || !p86H61.whatSi.includes("P82") || !p86H61.whatSi.includes("Dragos"))
  p86Errors.push("sidro hiša 61: whatSi ≠ P86 (Nikolaj Pošek/Požek [~] = P82 sidro 1887; mati menjana Filak→Dragos)");
// sidro 4: hiša 53 — NOVA LUKNJA (14. dokazana; forenzika 53 ≠ 33)
const p86H53 = p86Hv.find((h) => h.houseNo === "53" && h.scan === 52);
if (!p86H53 || !p86H53.whatSi.includes("LUKNJA") || !p86H53.whatSi.includes("Pozdirec"))
  p86Errors.push("sidro hiša 53: whatSi ≠ P86 (NOVA LUKNJA 41–60, oče Janez Pozdirec [~])");
// sidro 5: hiša 2 — trojna kontinuiteta (P82 1887 + P84 1889 + P86 1891)
const p86H2 = p86Hv.find((h) => h.houseNo === "2" && h.scan === 53);
if (!p86H2 || !p86H2.whatSi.includes("Peter Hlebec") || !p86H2.whatSi.includes("TROJNA"))
  p86Errors.push("sidro hiša 2: whatSi ≠ P86 (Peter Hlebec [~], trojna kontinuiteta P82+P84+P86)");
// sidro 6: hiša 28 — Jurij Požek (Požek veriga 79→77→28 — 3. hiša familije)
const p86H28 = p86Hv.find((h) => h.houseNo === "28" && h.scan === 54);
if (!p86H28 || !p86H28.whatSi.includes("Jurij Požek") || !p86H28.whatSi.includes("h77"))
  p86Errors.push("sidro hiša 28: whatSi ≠ P86 (Jurij Požek [~], veriga h79→h77→h28)");
// sidro 7: hiša 31 — mati Marjeta Straus ISTA OSEBA 1887+1890+1891 (3 vpise)
const p86H31 = p86Hv.find((h) => h.houseNo === "31" && h.scan === 53);
if (!p86H31 || !p86H31.whatSi.includes("Marjeta Straus") || !p86H31.whatSi.includes("ISTA OSEBA"))
  p86Errors.push("sidro hiša 31: whatSi ≠ P86 (mati Marjeta Straus [~] ISTA OSEBA ×3)");
// sidro 8: hiša 5 — vsi Torec (ponovitev čez knjige: mrliška 04894 1886)
const p86H5 = p86Hv.find((h) => h.houseNo === "5" && h.scan === 53);
if (!p86H5 || !p86H5.whatSi.includes("Torec") || !p86H5.whatSi.includes("04894"))
  p86Errors.push("sidro hiša 5: whatSi ≠ P86 (vsi Torec [~], ponovitev mrliške 04894 1886)");
// PT klasifikacija == pin: 8 v naboru + 1 v luknji (53 NOVA — 14. dokazana)
const p86InSet = [...p86Houses].filter((h) => P86_PT_IN_SET.includes(h));
const p86Gap = [...p86Houses].filter((h) => P86_PT_GAP.includes(h));
if (p86InSet.length !== 8 || p86Gap.length !== 1)
  p86Errors.push(`PT klasifikacija ≠ 8/1 (${p86InSet.length}/${p86Gap.length})`);
if (p86Gap.some((h) => !(Number(h) >= 41 && Number(h) <= 60)))
  p86Errors.push("luknjane hiše izven 41–60");
// kontinuiteta h30 čez leta: 1890 ima 2 bloka (dvojčka) z Milek + botra Matija Milek
const p86H30_1890 = HOUSE_VITALS.filter((v) => v.houseNo === "30" && v.bookSignature === "04105" && v.year === 1890);
if (p86H30_1890.length !== 2 || !p86H30_1890.every((v) => v.whatSi.includes("Milek")))
  p86Errors.push(`kontinuiteta h30: 1890 dvojčka ≠ 2 bloka z Milek (${p86H30_1890.length})`);
// trojna kontinuiteta h2: 1887 + 1889 + 1891 vsi Peter Hlebec
for (const yr of [1887, 1889, 1891]) {
  const b = HOUSE_VITALS.find((v) => v.houseNo === "2" && v.bookSignature === "04105" && v.year === yr);
  if (!b || !b.whatSi.includes("Hlebec"))
    p86Errors.push(`trojna kontinuiteta h2: blok ${yr} z Hlebec manjka`);
}
// menjava matere h61: 1887 blok z Filath + 1891 z Dragos
const p86H61_1887 = HOUSE_VITALS.find((v) => v.houseNo === "61" && v.bookSignature === "04105" && v.year === 1887);
if (!p86H61_1887 || !p86H61_1887.whatSi.includes("Požek") || !p86H61_1887.whatSi.includes("Filath"))
  p86Errors.push("menjava matere h61: blok 1887 (Miko Požek + Bara Filath) manjka");
// ponovitve prek HOUSE_VITALS (7 ponovljenih hiš 1891; h5 čez knjige)
const p86Prev = (hn: string, yr: number, sig: string = "04105") =>
  HOUSE_VITALS.some((v) => v.houseNo === hn && v.bookSignature === sig && v.year === yr);
for (const [hn, yr, sig] of [
  ["2", 1887, "04105"], ["30", 1890, "04105"], ["31", 1887, "04105"], ["72", 1888, "04105"],
  ["5", 1886, "04894"], ["61", 1887, "04105"], ["62", 1887, "04105"],
] as const) {
  if (!p86Prev(hn, yr, sig))
    p86Errors.push(`ponovitev hiša ${hn} (${yr}, ${sig}) manjka v HOUSE_VITALS`);
}
// NOVE hiše 1891 (28, 53) — ne obstajajo v nobenem prejšnjem letu/knjigi;
// h53: P89 kontinuiteta dovoli tudi blok 1894 + P91 blok 1896 (ISTA zveza variante);
// h53: P93 kontinuiteta dovoli tudi blok 1898 (4. VPIS ISTA ZVEZA); P109: + 1914 blok h53 (5. VPIS — VRZEL 16 LET!)
for (const hn of ["28", "53"]) {
  const allow = hn === "53" ? [1891, 1894, 1896, 1898, 1914, 1915, 1918] : hn === "28" ? [1891, 1910, 1913] : [1891]; // P105: + 1910 blok h28 (2. VPIS — VRZEL 19 LET, NEZAKONSKA) P108: + 1913 blok h28 (3. VPIS — oče Lozar razrešeno!) P113: + 1918 blok h53 (7. VPIS — Dragoš, VRZEL 2 LETI)
  if (HOUSE_VITALS.some((v) => v.houseNo === hn && !(v.bookSignature === "04105" && allow.includes(v.year)) && !(v.bookSignature === "04455" && v.year === 1890 && hn === "53") && !(v.bookSignature === "04455" && v.year === 1897 && hn === "28") && !(v.bookSignature === "04455" && v.year === 1908 && hn === "28") && !(v.bookSignature === "04455" && v.year === 1913 && hn === "53"))) // P119: + poročni blok h53-1890 (NOVA HIŠA — 1. dokaz sploh v vzorcu!); P126: + poročni blok h28-1897 (v18 Deblič? × Požek? — 1. POROČNI dokaz h28!); P137: + poročni blok h28-1908 (v5 nevesta Catharina Požek — 2. poročni dokaz h28!); P142: + poročni blok h53-1913 (№3 nevesta Marjeta Pezdirec — 2. poročni dokaz h53 + DVOTERNA KORPUS-SINHRONIZACIJA: njen krst 14.8.1891 h53 [P86 ISTA HIŠA!] + par-krsti 1915/1918 h53!)
    p86Errors.push(`NOVA hiša ${hn} (P86) že obstaja v prejšnjem letu — pini neskladni`);
}
// vitals skupaj 449 (po P106: 429 + 20; krstna 1911)
if (HOUSE_VITALS.length !== 685)
  p86Errors.push(`HOUSE_VITALS ≠ 467 (${HOUSE_VITALS.length})`);
push(
  "qa-p86-parish-baptism-1891",
  "P86: ŽUPNIJA PODZEMELJ — KRSTNA KNJIGA 04105, POLNO LETO 1891 (issue #18; SAMPLE-TRANSCRIPTION-1891; MERI, NE odloča; v7 join nespremenjen): širitev vzorca P79 (1886) → P82 (1887) → P83 (1888) → P84 (1889) → P85 (1890) na leto 1891 — okvir: skeni 49–56 == tiskane strani 48–55 (stran == sken − 1; leto se začne na str. 48 row 1 po 1890 rows 78–86; vpisi na skenih 50–54; glava »Leto 1892« na str. 55 row 1 — oznake se ponastavijo na 1, novela P83 potrjena 4. leto; 1891 ima 75 zveznih vrstic; glave mesecev se ponavljajo — Avgust 2×, November 2×) — VSI vpisi z Griblji: 10 vpisov / 9 imenovanih hiš + 1 NEBERLJIVA (r52 prekrita z modrimi pripisi — evidence-only; HOUSE_VITALS 9 zasidranih): 72, 30, 62, 61, 53, 2, 31, 5, 28 — NOVE hiše 2 (28, 53) + 1 neberljiva, ponovitve 7 (h2 ×3 leta; h30 kontinuiteta; h31 ×4; h5 ČEZ KNJIGE — mrliška 04894 1886; h61 1887+1897+1891 — oče Požek ISTA OSEBA; h62 1887 — Križan tudi 1887; h72 1888); skupaj s P79–P85 vzorec 127 vpisov / 58 hiš čez tri knjige in šest let; NOVELA (novela P85 potrjena 2. leto): VSI 9 zasidranih statusov = ¼ ulomek (zemljak 5, gemžgah 4 — brez bajtarjev/obrtnikov na Gribljih, kontrast 1890); PT klasifikacija 8/1 (53 v luknji 41–60 — NOVA, 14. dokazana številka; luknja zdaj 14 dokazanih); 0 nezakonskih; r39 h61 edini vpis brez botre + brez podpisa; SIDRA: h72 (oče Matija Straus [~] = ISTI očet kot P83 1888 — re-read Hraus→Strauš; mati MENJANA: 1888 Husič [~] → 1891 Jakobič [~]; tri-virska P80 + PUA @71 0.8571; botra Straucelj), h30 (oče Janez Milek [~] = P85 dvojčka rows 51+52 — POPOLNA KONTINUITETA: isti starši + ISTA botra Matija Milek + Katarina Križan; Milek = P81 near-miss), h61 (oče Nikolaj Pošek/Požek [~] = P82 SIDRO 1887 Miko Požek — ISTA OSEBA po 4 letih; mati MENJANA: 1887 Bara Filak → 1891 Ana Dragos [~ Dragoš] — PRVI dokaz menjave gospodinjstva na zasidrani hiši), h53 (oče Janez Pozdirec [~] + mati Marija Križan [~] — NOVA LUKNJA 14.; forenzika izrez 4x: jasno 53, prvi prebir »33« [~] Kurrent 3/5), h62 (mati Barbara Hrižan [~] + babica Ana Hrižan — Križan gospodinjstvo PONOVITEV P82 1887), h2 (oče Peter Hlebec [~] — TROJNA KONTINUITETA P82 1887 + P84 1889 + 1891, ISTI starši ×3 čez 5 let), h31 (mati Marjeta Straus [~] — ISTA OSEBA 1887 Margaretha + 1890 + 1891, 3 vpise čez 5 let; oče 1887/1890 Papič [~] → 1891 Tepič [~] Kurrent P/T; botra Klobučar 4. leto), h5 (vsi TOREC — PONOVITEV ČEZ KNJIGE: mrliška 04894 1886 + krstna 1891, familija hiše; modro ime »Terezija?« [~] vs tmavo »Jožefa«), h28 (oče Jurij Požek [~] — POŽEK VERIGA h79 1888 → h77 1890 → h28 1891, 3. hiša familije v 4 letih; mati Milkovič [~] = Milek varianta; botra Muern = oče h62); DVE menjavi matere na zasidranih hišah (h61 Filak→Dragos + h72 Husič→Jakobič — druga žena / ponovna poroka / re-read [~], MERI); priimki z 1825 pričo v 1891: Križan/Hrižan 8× (0.8333 [~] — najmočnejše leto), Milek/Milkovič 4× (near-miss), Straus/Straucelj 3+1 [~] (0.8571), Požek/Pošek 2× (4. leto), Dragoš 1× (1.0), Urh 1× [~] (1.0), Jakobič/Jaklpič 2×, Brinec babica 2× (6./7. leto), Klobučar 1×, Brodarič 1×; ŠIMEC 0× — PRVO leto brez najtrajnejše familije (1886: 4 hiše, 1887: 1, 1888: 1, 1889: 3, 1890: 6); babice: Ana Hrižan 4× (vrnitev po 1889) + Brinec 2× + Marjeta Fojter 2× (nova) + Katarina [~] 1; DUHOVNIKI: Jos. Rauq [~] 7 + Jos. R— [~] 1 + prazna 1 + neberljiva 1; NOV podpis St. Češarek [~] od r68 (sredi decembra 1891) — 0× na Gribljih; live verifikacija: knjiga HTTP 200 (inventar 326), citirani skeni 5/5 JPEG 200; skripta scripts/p86_parish_baptism_1891.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1891",
  "P86: PARISH OF PODZEMELJ — BAPTISM REGISTER 04105, THE FULL YEAR 1891 (issue #18; SAMPLE-TRANSCRIPTION-1891; MEASURES, does not decide; the v7 join unchanged): extending the P79 (1886) → P82 (1887) → P83 (1888) → P84 (1889) → P85 (1890) sample to 1891 — the frame: scans 49–56 == printed pages 48–55 (page == scan − 1; the year starts on p. 48 row 1 after the 1890 rows 78–86; entries on scans 50–54; the »1892« heading on p. 55 row 1 — the labels restart at 1, the P83 novel confirmed for the 4th year; 1891 has 75 continuous rows; month headers repeat — August 2×, November 2×); ALL Griblje entries: 10 entries / 9 named houses + 1 ILLEGIBLE (r52 covered by blue notes — evidence-only; HOUSE_VITALS 9 anchored): 72, 30, 62, 61, 53, 2, 31, 5, 28 — 2 NEW houses (28, 53) + 1 illegible, 7 repeats (h2 ×3 years; h30 continuity; h31 ×4; h5 CROSS-BOOK — mrliška 04894 1886; h61 1887+1897+1891 — father Požek THE SAME person; h62 1887 — Križan also 1887; h72 1888); with P79–P85 the sample totals 127 entries / 58 houses across three books and six years; NOVEL (the P85 novel confirmed for the 2nd year): ALL 9 anchored statuses = ¼ fraction (5 smallholder, 4 helper — no cottagers/craftsmen in Griblje, contrast 1890); the PT classification 8/1 (53 in the 41–60 gap — NEW, the 14th proven number; the gap now has 14 proven); 0 illegitimates; r39 h61 the only entry without godparents and signature; ANCHORS: h72 (father Matija Straus [~] = THE SAME father as P83 1888 — re-read Hraus→Strauš; mother CHANGED: 1888 Husič [~] → 1891 Jakobič [~]; the three-source P80 + PUA @71 0.8571; godparent Straucelj), h30 (father Janez Milek [~] = the P85 twins rows 51+52 — COMPLETE CONTINUITY: same parents + THE SAME godparents Matija Milek + Katarina Križan; Milek = P81 near-miss), h61 (father Nikolaj Pošek/Požek [~] = the P82 ANCHOR 1887 Miko Požek — THE SAME person 4 years later; mother CHANGED: 1887 Bara Filak → 1891 Ana Dragos [~ Dragoš] — the FIRST evidence of a household change on an anchored house), h53 (father Janez Pozdirec [~] + mother Marija Križan [~] — the NEW GAP 14th; 4x crop forensics: clearly 53, first read »33« [~] Kurrent 3/5), h62 (mother Barbara Hrižan [~] + midwife Ana Hrižan — the Križan household REPEAT of P82 1887), h2 (father Peter Hlebec [~] — TRIPLE CONTINUITY P82 1887 + P84 1889 + 1891, THE SAME parents ×3 across 5 years), h31 (mother Marjeta Straus [~] — THE SAME person 1887 Margaretha + 1890 + 1891, 3 entries across 5 years; father 1887/1890 Papič [~] → 1891 Tepič [~] Kurrent P/T; godparent Klobučar 4th year), h5 (all TOREC — CROSS-BOOK REPEAT: mrliška 04894 1886 + baptism 1891, the house family; blue name »Terezija?« [~] vs dark »Jožefa«), h28 (father Jurij Požek [~] — THE POŽEK CHAIN h79 1888 → h77 1890 → h28 1891, the family's 3rd house in 4 years; mother Milkovič [~] = Milek variant; godparent Muern = the h62 father); TWO mother changes on anchored houses (h61 Filak→Dragos + h72 Husič→Jakobič — another wife / remarriage / re-read [~], MEASURES); surnames with 1825 evidence in 1891: Križan/Hrižan 8× (0.8333 [~] — the strongest year of the family), Milek/Milkovič 4× (near-miss), Straus/Straucelj 3+1 [~] (0.8571), Požek/Pošek 2× (4th year), Dragoš 1× (1.0), Urh 1× [~] (1.0), Jakobič/Jaklpič 2×, Brinec midwife 2× (6th/7th year), Klobučar 1×, Brodarič 1×; ŠIMEC 0× — THE FIRST year without the most persistent family (1886: 4 houses, 1887: 1, 1888: 1, 1889: 3, 1890: 6); midwives: Ana Hrižan 4× (return after 1889) + Brinec 2× + Marjeta Fojter 2× (new) + Katarina [~] 1; PRIESTS: Jos. Rauq [~] 7 + Jos. R— [~] 1 + empty 1 + illegible 1; a NEW signature St. Češarek [~] from r68 (mid-December 1891) — 0× in Griblje; live verification: the book HTTP 200 (inventory 326), cited scans 5/5 JPEG 200; the script scripts/p86_parish_baptism_1891.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1891",
  p86Errors.length === 0,
  p86Errors.length === 0
    ? `10 vpisov / 9 imenovanih hiš + 1 neberljiva (9 zasidranih v vitals) · okvir 1891 skeni 49–56 (vpisi 50–54; prelom 1892 str. 55 row 1; 75 zveznih vrstic) · NOVELA: vsi 9 statusov = ¼ ulomek (novela P85 potrjena) · PT 8/1 (53 NOVA — 14. dokazana luknja) · nove hiše 2 (28, 53) + ponovitve 7 (h5 čez knjige; h61 oče ISTA OSEBA) · sidra h72 Straus = P83 (mati menjana) / h30 Milek = P85 kontinuiteta (isti starši + botra) / h61 Požek = P82 sidro (ISTA OSEBA; mati menjana) / h53 NOVA LUKNJA / h2 trojna kontinuiteta ×3 / h28 Požek 3. hiša / h31 Straus mati ISTA ×3 · Šimec 0× (prvo leto)`
    : p86Errors.join("; "),
);

// ——— qa-p87: p87 krstna 1892 — širitev vzorca na leto 1892 (issue #18;
//      SAMPLE-TRANSCRIPTION-1892; celoven neodvisen preracun iz bundled
//      virov: HOUSE_VITALS × PARISH_BOOKS; PT klasifikacija iz pinov;
//      sidra: h58 Požek × Dragos 3. leto (1889+1890+1892), h61 Požek ×
//      Dragos = P86 kontinuiteta 2. leto (isti vzorec brez botre/podpisa),
//      h63 Hrižan = P85 sidro (oče ISTI 3×), h1 Željko × Kure = P83 1888
//      (ISTA zveza), h32 Urh = P85 1890 (ISTI oče), h90 šolska hiša
//      (učitelj Kopitar 1890+1892), h24 4. FAMILIJA, h27 3. FAMILIJA;
//      NOVELA: statusi ulomki (novela P85 potrjena 3. leto); paleografska
//      faza v research/issue17/parish-baptism-1892.json, live verifikator
//      scripts/p87_parish_baptism_1892.py --check I1–I10) ———
const p87Hv = HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year === 1892);
const p87Errors: string[] = [];
const P87_PT_IN_SET = ["1", "12", "24", "27", "29", "32", "61", "63", "73", "75", "90"];
const P87_PT_GAP = ["58"];
if (p87Hv.length !== 12)
  p87Errors.push(`vpisov 1892 (04105, zasidrani) ≠ 12 (${p87Hv.length})`);
const p87Houses = new Set(p87Hv.map((h) => h.houseNo));
if (p87Houses.size !== 12)
  p87Errors.push(`različnih hiš ≠ 12 (${p87Houses.size}: ${[...p87Houses].sort((a, b) => Number(a) - Number(b)).join(",")})`);
const p87Bad = p87Hv.filter((h) => h.status !== "DOCUMENTED" || !h.scan || !h.page || h.page !== h.scan - 1 || h.scan < 56 || h.scan > 62);
if (p87Bad.length > 0)
  p87Errors.push(`okvir 1892: skeni 56–62 ali stran ≠ sken − 1 krščeno pri ${p87Bad.length}`);
// sidro 1: hiša 58 — Janez Požek × Ana Dragos (3. leto: 1889+1890+1892)
const p87H58 = p87Hv.find((h) => h.houseNo === "58" && h.scan === 61);
if (!p87H58 || !p87H58.whatSi.includes("Janez Požek") || !p87H58.whatSi.includes("Dragos") || !p87H58.whatSi.includes("3. LETO"))
  p87Errors.push("sidro hiša 58: whatSi ≠ P87 (Janez Požek [~] × Ana Dragos [~], 3. leto na h58)");
// sidro 2: hiša 61 — Nikolaj Požek × Ana Dragos (P86 kontinuiteta 2. leto)
const p87H61 = p87Hv.find((h) => h.houseNo === "61" && h.scan === 61);
if (!p87H61 || !p87H61.whatSi.includes("Nikolaj Požek") || !p87H61.whatSi.includes("P86") || !p87H61.whatSi.includes("Dragos"))
  p87Errors.push("sidro hiša 61: whatSi ≠ P87 (Nikolaj Požek [~] = P86 1891 kontinuiteta; ISTA zveza 1891+1892)");
// sidro 3: hiša 63 — Nikolaj Hrižan (oče ISTI 3×: 1887+1890+1892; P85 sidro)
const p87H63 = p87Hv.find((h) => h.houseNo === "63" && h.scan === 61);
if (!p87H63 || !p87H63.whatSi.includes("Hrižan") || !p87H63.whatSi.includes("ISTI OČE"))
  p87Errors.push("sidro hiša 63: whatSi ≠ P87 (Nikolaj Hrižan [~], oče ISTI 3× — P85 sidro)");
// sidro 4: hiša 1 — Nikolaj Željko × Katarina Kure (ISTA zveza 1888+1892)
const p87H1 = p87Hv.find((h) => h.houseNo === "1" && h.scan === 60);
if (!p87H1 || !p87H1.whatSi.includes("Željko") || !p87H1.whatSi.includes("1888"))
  p87Errors.push("sidro hiša 1: whatSi ≠ P87 (Nikolaj Željko [~] × Katarina Kure [~], ISTA zveza P83 1888+1892)");
// sidro 5: hiša 32 — Matija Urh (ISTI oče 3×: 1889+1890+1892; Urh veriga)
const p87H32 = p87Hv.find((h) => h.houseNo === "32" && h.scan === 60);
if (!p87H32 || !p87H32.whatSi.includes("Matija Urh") || !p87H32.whatSi.includes("ISTI OČE 3×"))
  p87Errors.push("sidro hiša 32: whatSi ≠ P87 (Matija Urh [~], ISTI oče 3× 1889+1890+1892)");
// sidro 6: hiša 90 — šolska hiša (učitelj Kopitac 1890+1892; nadučitelj botra)
const p87H90 = p87Hv.find((h) => h.houseNo === "90" && h.scan === 61);
if (!p87H90 || !p87H90.whatSi.includes("Kopitac") || !p87H90.whatSi.includes("ŠOLSKA"))
  p87Errors.push("sidro hiša 90: whatSi ≠ P87 (učitelj Franc Kopitac [~], ŠOLSKA HIŠA 90, ISTA družina 1890+1892)");
// sidro 7: hiša 24 — MENJAVA GOSPODINJSTVA (Jurajevič; forenzika kraj Griblje)
const p87H24 = p87Hv.find((h) => h.houseNo === "24" && h.scan === 62);
if (!p87H24 || !p87H24.whatSi.includes("Jurajevič") || !p87H24.whatSi.includes("MENJAVA GOSPODINJSTVA"))
  p87Errors.push("sidro hiša 24: whatSi ≠ P87 (Martin Jurajevič [~] bajtar, menjava gospodinjstva Brinec → Jurajevič)");
// sidro 8: hiša 27 — MENJAVA GOSPODINJSTVA (Pozdirec bajtar)
const p87H27 = p87Hv.find((h) => h.houseNo === "27" && h.scan === 57);
if (!p87H27 || !p87H27.whatSi.includes("Pozdirec") || !p87H27.whatSi.includes("MENJAVA GOSPODINJSTVA"))
  p87Errors.push("sidro hiša 27: whatSi ≠ P87 (Marko Pozdirec [~] bajtar, menjava gospodinjstva Kukar/Stubhar → Pozdirec)");
// PT klasifikacija == pin: 11 v naboru + 1 v luknji (58 — že dokazana, brez novih)
const p87InSet = [...p87Houses].filter((h) => P87_PT_IN_SET.includes(h));
const p87Gap = [...p87Houses].filter((h) => P87_PT_GAP.includes(h));
if (p87InSet.length !== 11 || p87Gap.length !== 1)
  p87Errors.push(`PT klasifikacija ≠ 11/1 (${p87InSet.length}/${p87Gap.length})`);
if (p87Gap.some((h) => !(Number(h) >= 41 && Number(h) <= 60)))
  p87Errors.push("luknjane hiše izven 41–60");
// kontinuitete čez leta prek HOUSE_VITALS
const p87Prev = (hn: string, yr: number, sig: string = "04105") =>
  HOUSE_VITALS.some((v) => v.houseNo === hn && v.bookSignature === sig && v.year === yr);
for (const [hn, yr, sig, pin] of [
  ["58", 1890, "04105", "Požek"], ["61", 1891, "04105", "Požek"], ["63", 1890, "04105", "Križan"],
  ["32", 1890, "04105", "Urh"], ["1", 1888, "04105", "Zeljth"], ["90", 1890, "04105", "Kopitar"],
  ["24", 1890, "04105", "ANOMALIJA"], ["27", 1887, "04105", "Kukar"], ["29", 1888, "04105", "Milek"],
  ["24", 1887, "04105", "Brinec"], ["27", 1890, "04105", "Stubhar"], ["32", 1889, "04105", "Urh"],
  ["63", 1889, "04105", "Hrigian"], ["29", 1886, "04894", "Mileh"],
] as const) {
  const blk = HOUSE_VITALS.find((v) => v.houseNo === hn && v.bookSignature === sig && v.year === yr);
  if (!blk || !blk.whatSi.includes(pin))
    p87Errors.push(`kontinuiteta hiša ${hn} (${yr}, ${sig}, pin ${pin}) manjka ali pin ne ustreza`);
}
// NOVE hiše 1892 (12, 73, 75) — ne obstajajo v nobenem prejšnjem letu/knjigi;
// P89 kontinuiteta dovoli tudi bloke 1894 (ISTA zvezi — h12 Dragoš, h73
// Županič, h75 Jakobič × Stubljar — vsi 2. vpis); P90 dovoli h12 tudi blok
// 1895 (3. vpis ISTI oče Dragoš)
// h12: P92 dovoli blok 1897 (Dragar? kontinuiteta)
for (const hn of ["12", "73", "75"]) {
  const allow = hn === "12" ? [1892, 1894, 1895, 1897, 1899, 1901, 1903, 1905, 1907, 1909, 1912, 1916] : [1892, 1894, 1899]; // P94: + 1899 bloka (h12 mati MENJAVA [~]; h75 3. VPIS ISTA ZVEZA); P96: + 1901 bloka h12 (r1 + r36 — PRVA ponovitev po 1893); P98: + 1903 blok h12 (8. VPIS); P100: + 1905 bloka h12 (NARE PRELOM — r4 Neža + r15 Ana, 9./10. VPIS); P102: + 1907 blok h12 (11. VPIS — Dragoš POVRAT); P104: + 1909 blok h12 (12. VPIS — ISTA ZVEZA Drgoš × Cvitkovič) P107: + 1912 blok h12 (13. VPIS — † TRIPOLI 1987!) P111: + 1916 blok h12 (14. VPIS — VRZEL 4 LETO, Vincencij)
  const extra = hn === "73" ? [{ sig: "04455", yr: 1906 }] : []; // P135: + h73 1. POROČNI dokaz 1906 (ženin Johann Šuparnič? — ★ NOVI MAKSIMUM h65→h73!)
  if (HOUSE_VITALS.some((v) => v.houseNo === hn && !(v.bookSignature === "04105" && allow.includes(v.year)) && !extra.some((e) => v.bookSignature === e.sig && v.year === e.yr)))
    p87Errors.push(`NOVA hiša ${hn} (P87) že obstaja v prejšnjem letu — pini neskladni`);
}
// vitals skupaj 449 (po P106: 429 + 20; krstna 1911)
if (HOUSE_VITALS.length !== 685)
  p87Errors.push(`HOUSE_VITALS ≠ 467 (${HOUSE_VITALS.length})`);
push(
  "qa-p87-parish-baptism-1892",
  "P87: ŽUPNIJA PODZEMELJ — KRSTNA KNJIGA 04105, POLNO LETO 1892 (issue #18; SAMPLE-TRANSCRIPTION-1892; MERI, NE odloča; v7 join nespremenjen): širitev vzorca P79 (1886) → P82 (1887) → P83 (1888) → P84 (1889) → P85 (1890) → P86 (1891) na leto 1892 — okvir: skeni 56–63 == tiskane strani 55–62 (stran == sken − 1; glava »Leto 1892« na str. 55 row 1 po 1891 rows 65–75; vpisi na skenih 56, 57, 60, 61, 62 — 58/59 brez Gribljev; velike cifre »1893~« na str. 62 po row 82 — oznake se ponastavijo na 1, novela P83 potrjena 5. leto; 1892 ima 82 zveznih vrstic; glave mesecev se ponavljajo — Avgust 2×, November 2×) — VSI vpisi z Griblji: 12 vpisov / 12 hiš — NARE (prvo leto brez ponovitev znotraj leta; 0 neberljivih; HOUSE_VITALS 12 zasidranih): 75, 29, 73, 12, 27, 1, 32, 58, 90, 63, 61, 24 — NOVE hiše 3 (12, 73, 75) + ponovitve 9 (h1 1888+1892 ISTA zveza; h24 MENJAVA GOSPODINJSTVA Brinec → Jurajevič, 4. vpis; h27 MENJAVA GOSPODINJSTVA Kukar/Stubhar → Pozdirec; h29 ISTA zveza Milek × Križan 1888+1892; h32 ISTI oče Urh 3× 1889+1890+1892; h58 3. leto Požek × Dragos; h61 1891+1892 kontinuiteta sidra; h63 oče ISTI 4×; h90 učitelj 1890+1892); skupaj s P79–P86 vzorec 139 vpisov / 61 hiš čez tri knjige in sedem let; NOVELA (novela P85 potrjena 3. leto): vsi statusi ulomki ali poklici — ½ zemljak 5 + ¼ zemljak 4 + bajtar 2 (vrnitev po 1891: 0) + učitelj 1; PT klasifikacija 11/1 (58 v luknji 41–60 — že dokazana P84/P85; luknja ostaja 14 dokazanih, brez novih); 0 nezakonskih; r70 h61 edini vpis brez botre + brez podpisa (ISTI vzorec kot 1891 r39 na ISTI hiši!); SIDRA: h58 (oče Janez Požek [~] × mati Ana Dragos [~] — POŽEK × DRAGOS 3. LETO 1889+1890+1892, najdaljša zasidrana zveza familije; forenzika izrez: jasno 58, prvi prebir 53 [~] Kurrent 3/5), h61 (oče Nikolaj Požek [~] ½ × mati Ana Dragos [~] — KONTINUITETA SIDRA 2. LETO: P86 1891 ISTA zveza + ISTI vzorec brez botre/podpisa; status ¼→½ [~] — menjava statusa na zasidrani hiši [~]; P82 sidro 1887 + 1897 + 1891 + 1892), h63 (oče Nikolaj Hrižan [~] ¼ — ISTI OČE ime+priimek 4×: 1887 Prižan [Križan] + 1889 Hrigian? [nezakonska] + 1890 Križan ½ + 1892 Hrižan; P85 SIDRO potrjeno; Kurrent K/H varianta; mati Pegdirec [~] ≈ 1889 Pezdirec [~]), h1 (oče Nikolaj Željko [~] ¼ × mati Katarina Kure [~] — ISTA ZVEZA P83 1888 »Zeljth« [~] + 1892, re-read; NAJNIŽJA hišna številka v vzorcu; botra Jurij Željko + Katarina Kure = ISTA priimka kot starši), h32 (oče Matija Urh [~] ¼ — ISTI OČE 3×: 1889 + 1890 + 1892; mati Pezdirec/Pegdirec vseh 3 let — ISTA žena? [~]; Urh veriga 1887–1892, 6 let; PUA urh 1.0), h90 (oče Franc Kopitac [~] učitelj × Marija Schweizer [~] — ISTA UČITELJSKA DRUŽINA 1890+1892; ŠOLSKA HIŠA; botra Janez Barle NADUČITELJ — prvi v vzorcu), h24 (oče Martin Jurajevič [~] bajtar — MENJAVA GOSPODINJSTVA: Brinec gospodinjstvo 1887 + anomalija 1890 → Jurajevič 1892, 4. vpis; forenzika 4x: kraj jasno Griblje, modri pripisi so mrliški), h27 (oče Marko Pozdirec [~] bajtar — MENJAVA GOSPODINJSTVA: oče 1887 Kukar [~] = 1890 Stubhar [~] ISTI (re-read) → 1892 Pozdirec, 3. vpis), h29 (oče Peter Milek [~] × mati Ana Križan [~] — ISTA ZVEZA 1888+1892: P84 1888 Peter Milek ½ × Ana Križan »hiša epidemije«; status ½→¼ [~]; mrliška 04894 1886: trije Mileh [~] otroci v koleri), h75/h73/h12 NOVE (prvi dokaz čez tri knjige); Dragos/Dragoš 2. hiša familije (h58+h61 mati + h12 oče Janez Dragos); ŠIMEC 0× — 2. leto zapored brez najtrajnejše familije (1886: 4, 1887: 1, 1888: 1, 1889: 3, 1890: 6, 1891: 0, 1892: 0); babice: Marija Brinec 4× (8.–10. leto) + Ana Križan 3× + Marjeta Trotter 2× (nova) + Ana Krajnovec 1×; DUHOVNIKI: Fr./St. Češarek [~] 8 (Jan–Sep) + Jos. Rauq [~] 3 (Feb!, Okt–Dec) + prazna 1 — oba SOČASNO aktivna 1892 (menjava P86 decembra 1891 NI dokončna); r13 podpis celo ime »Franc Češarek« [~]; live verifikacija: knjiga HTTP 200 (inventar 326), citirani skeni 5/5 JPEG 200; skripta scripts/p87_parish_baptism_1892.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1892",
  "P87: PARISH OF PODZEMELJ — BAPTISM REGISTER 04105, THE FULL YEAR 1892 (issue #18; SAMPLE-TRANSCRIPTION-1892; MEASURES, does not decide; the v7 join unchanged): extending the P79 (1886) → P82 (1887) → P83 (1888) → P84 (1889) → P85 (1890) → P86 (1891) sample to 1892 — the frame: scans 56–63 == printed pages 55–62 (page == scan − 1; the »1892« heading on p. 55 row 1 after the 1891 rows 65–75; entries on scans 56, 57, 60, 61, 62 — 58/59 without Griblje; the large figures »1893~« on p. 62 after row 82 — the labels restart at 1, the P83 novel confirmed for the 5th year; 1892 has 82 continuous rows; month headers repeat — August 2×, November 2×); ALL Griblje entries: 12 entries / 12 houses — SQUARE (the first year without within-year repeats; 0 illegible; HOUSE_VITALS 12 anchored): 75, 29, 73, 12, 27, 1, 32, 58, 90, 63, 61, 24 — 3 NEW houses (12, 73, 75) + 9 repeats (h1 1888+1892 THE SAME couple; h24 HOUSEHOLD CHANGE Brinec → Jurajevič, the 4th entry; h27 HOUSEHOLD CHANGE Kukar/Stubhar → Pozdirec; h29 THE SAME couple Milek × Križan 1888+1892; h32 THE SAME father Urh 3× 1889+1890+1892; h58 the 3rd year Požek × Dragos; h61 1891+1892 anchor continuity; h63 the father THE SAME 4×; h90 teacher 1890+1892); with P79–P86 the sample totals 139 entries / 61 houses across three books and seven years; NOVEL (the P85 novel confirmed for the 3rd year): all statuses fractions or occupations — ½ smallholder 5 + ¼ smallholder 4 + cottager 2 (a return after 1891: 0) + teacher 1; the PT classification 11/1 (58 in the 41–60 gap — already proven P84/P85; the gap remains 14 proven, no new); 0 illegitimates; r70 h61 the only entry without godparents and signature (THE SAME pattern as 1891 r39 on THE SAME house!); ANCHORS: h58 (father Janez Požek [~] × mother Ana Dragos [~] — POŽEK × DRAGOS for the 3rd YEAR 1889+1890+1892, the family's longest anchored couple; crop forensics: clearly 58, first read 53 [~] Kurrent 3/5), h61 (father Nikolaj Požek [~] ½ × mother Ana Dragos [~] — ANCHOR CONTINUITY for the 2nd YEAR: P86 1891 THE SAME couple + THE SAME pattern without godparents/signature; status ¼→½ [~] — a status change on an anchored house [~]; the P82 anchor 1887 + 1897 + 1891 + 1892), h63 (father Nikolaj Hrižan [~] ¼ — THE SAME father, first name+surname, 4×: 1887 Prižan [Križan] + 1889 Hrigian? [illegitimate] + 1890 Križan ½ + 1892 Hrižan; the P85 ANCHOR confirmed; the Kurrent K/H variant; mother Pegdirec [~] ≈ 1889 Pezdirec [~]), h1 (father Nikolaj Željko [~] ¼ × mother Katarina Kure [~] — THE SAME COUPLE P83 1888 »Zeljth« [~] + 1892, re-read; THE LOWEST house number in the sample; godparents Jurij Željko + Katarina Kure = THE SAME surnames as the parents), h32 (father Matija Urh [~] ¼ — THE SAME father 3×: 1889 + 1890 + 1892; mother Pezdirec/Pegdirec all 3 years — THE SAME wife? [~]; the Urh chain 1887–1892, 6 years; PUA urh 1.0), h90 (father Franc Kopitac [~] teacher × Marija Schweizer [~] — THE SAME TEACHER FAMILY 1890+1892; the SCHOOL HOUSE; godparent Janez Barle HEAD TEACHER — the first in the sample), h24 (father Martin Jurajevič [~] cottager — HOUSEHOLD CHANGE: the Brinec household 1887 + the anomaly 1890 → Jurajevič 1892, the 4th entry; 4x forensics: the place clearly Griblje, the blue notes are death notes), h27 (father Marko Pozdirec [~] cottager — HOUSEHOLD CHANGE: the father 1887 Kukar [~] = 1890 Stubhar [~] THE SAME (re-read) → 1892 Pozdirec, the 3rd entry), h29 (father Peter Milek [~] × mother Ana Križan [~] — THE SAME COUPLE 1888+1892: P84 1888 Peter Milek ½ × Ana Križan »the epidemic house«; status ½→¼ [~]; mrliška 04894 1886: three Mileh [~] children in the cholera), h75/h73/h12 NEW (the first evidence across three books); Dragos/Dragoš the family's 2nd house (h58+h61 mother + h12 father Janez Dragos); ŠIMEC 0× — the 2nd consecutive year without the most persistent family (1886: 4, 1887: 1, 1888: 1, 1889: 3, 1890: 6, 1891: 0, 1892: 0); midwives: Marija Brinec 4× (8th–10th year) + Ana Križan 3× + Marjeta Trotter 2× (new) + Ana Krajnovec 1×; PRIESTS: Fr./St. Češarek [~] 8 (Jan–Sep) + Jos. Rauq [~] 3 (Feb!, Oct–Dec) + empty 1 — BOTH simultaneously active in 1892 (the P86 December 1891 change is NOT final); r13 signature with the full name »Franc Češarek« [~]; live verification: the book HTTP 200 (inventory 326), cited scans 5/5 JPEG 200; the script scripts/p87_parish_baptism_1892.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1892",
  p87Errors.length === 0,
  p87Errors.length === 0
    ? `12 vpisov / 12 hiš — NARE (0 neberljivih; 12 zasidranih v vitals) · okvir 1892 skeni 56–63 (vpisi 56–62; prelom 1893 str. 62; 82 zveznih vrstic) · NOVELA: statusi ulomki, novela P85 potrjena 3. leto (½ 5 + ¼ 4 + bajtar 2 + učitelj 1) · PT 11/1 (58 — brez novih luknjanih) · nove hiše 3 (12, 73, 75) + ponovitve 9 · sidra h58 Požek × Dragos 3. leto / h61 kontinuiteta sidra 1891+1892 (isti vzorec brez botre/podpisa; status ¼→½) / h63 oče ISTI 4× / h1 Željko × Kure 1888+1892 / h29 Milek × Križan 1888+1892 / h32 Urh 3× 1889+1890+1892 / h90 šolska (učitelj 1890+1892; nadučitelj botra) / h24 + h27 menjavi gospodinjstva · Šimec 0× 2. leto · Češarek 8× + Rauq 3× (sočasno)`
    : p87Errors.join("; "),
);

// ——— qa-p88: p88 krstna 1893 — širitev vzorca na leto 1893 (issue #18;
//      SAMPLE-TRANSCRIPTION-1893; celoven neodvisen preracun iz bundled
//      virov: HOUSE_VITALS × PARISH_BOOKS; PT klasifikacija iz pinov;
//      sidra: h72 Strauš SIDRO 3. VPIS (oče ISTI 3×: 1888+1891+1893), h65
//      Milek oče ISTI 3× (1887+1889+1893), h27 DVOJČICI (Antonija † + Ivana,
//      vertikalni pripis; oče Stukar/Stubhar, ISTA mati Klobučar), h21
//      ŠIMEC NAZAJ (mati Ana Šimec + botra Janez Šimec — prvič od 1890;
//      oče Požek ISTI, MATI MENJANA Brinec→Šimec — 3. menjava matere),
//      h24 ISTA zveza Brinec × Jakobec 1887+1893 (5. vpis; izmenjava
//      Brinec↔Jurajevič), h30 MENJAVA GOSPODINJSTVA (Milek → Jakljevič),
//      h41 ISTA zveza 1890+1893, h15 ISTA zveza 1887+1893 (Jakšič/Jaklič),
//      h60 NOVA (Željko 2. hiša), h91 NOVA (botra Željko + Kure); paleografska
//      faza v research/issue17/parish-baptism-1893.json, live verifikator
//      scripts/p88_parish_baptism_1893.py --check I1–I10) ———
const p88Hv = HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year === 1893);
const p88Errors: string[] = [];
const P88_PT_IN_SET = ["15", "21", "23", "24", "25", "27", "30", "32", "65", "70", "72", "74", "91"];
const P88_PT_GAP = ["41", "46", "60"];
if (p88Hv.length !== 17)
  p88Errors.push(`vpisov 1893 (04105, zasidrani) ≠ 17 (${p88Hv.length})`);
const p88Houses = new Set(p88Hv.map((h) => h.houseNo));
if (p88Houses.size !== 16)
  p88Errors.push(`različnih hiš ≠ 16 (${p88Houses.size}: ${[...p88Houses].sort((a, b) => Number(a) - Number(b)).join(",")})`);
const p88Bad = p88Hv.filter((h) => h.status !== "DOCUMENTED" || !h.scan || !h.page || h.page !== h.scan - 1 || h.scan < 63 || h.scan > 69);
if (p88Bad.length > 0)
  p88Errors.push(`okvir 1893: skeni 63–69 ali stran ≠ sken − 1 krščeno pri ${p88Bad.length}`);
// sidro 1: hiša 72 — SIDRO 3. VPIS (oče Matija Strauš ISTI 3×)
const p88H72 = p88Hv.find((h) => h.houseNo === "72" && h.scan === 66);
if (!p88H72 || !p88H72.whatSi.includes("Matija Strauš") || !p88H72.whatSi.includes("3. VPIS"))
  p88Errors.push("sidro hiša 72: whatSi ≠ P88 (Matija Strauš [~], SIDRO 3. VPIS — oče ISTI 3×)");
// sidro 2: hiša 65 — oče Matija Milek ISTI 3× (1887+1889+1893)
const p88H65 = p88Hv.find((h) => h.houseNo === "65" && h.scan === 64);
if (!p88H65 || !p88H65.whatSi.includes("Matija Milek") || !p88H65.whatSi.includes("3×"))
  p88Errors.push("sidro hiša 65: whatSi ≠ P88 (Matija Milek [~], oče ISTI 3×)");
// sidro 3: hiša 27 — DVOJČICI (Stukar/Stubhar; ISTA mati Klobučar)
const p88H27 = p88Hv.filter((h) => h.houseNo === "27" && h.scan === 65);
if (p88H27.length !== 2 || !p88H27.every((h) => h.whatSi.includes("DVOJČICA") && h.whatSi.includes("Klobučar")))
  p88Errors.push("sidro hiša 27: dvojčici ≠ 2 bloka z DVOJČICA + Klobučar");
// sidro 4: hiša 21 — ŠIMEC NAZAJ (mati menjana Brinec → Šimec)
const p88H21 = p88Hv.find((h) => h.houseNo === "21" && h.scan === 68);
if (!p88H21 || !p88H21.whatSi.includes("Šimec") || !p88H21.whatSi.includes("Požek") || !p88H21.whatSi.includes("MENJANA"))
  p88Errors.push("sidro hiša 21: whatSi ≠ P88 (Janez Požek [~] × Ana Šimec [~], mati menjana; Šimec nazaj)");
// sidro 5: hiša 24 — ISTA zveza Brinec × Jakobec (5. vpis)
const p88H24 = p88Hv.find((h) => h.houseNo === "24" && h.scan === 67);
if (!p88H24 || !p88H24.whatSi.includes("Matija Brinec") || !p88H24.whatSi.includes("ISTA ZVEZA"))
  p88Errors.push("sidro hiša 24: whatSi ≠ P88 (Matija Brinec [~] × Barbara Jakobčič [~], ISTA zveza 1887+1893)");
// sidro 6: hiša 30 — MENJAVA GOSPODINJSTVA (Milek → Jakljevič)
const p88H30 = p88Hv.find((h) => h.houseNo === "30" && h.scan === 67);
if (!p88H30 || !p88H30.whatSi.includes("Jakljevič") || !p88H30.whatSi.includes("MENJAVA GOSPODINJSTVA"))
  p88Errors.push("sidro hiša 30: whatSi ≠ P88 (Peter Jakljevič [~], menjava Milek → Jakljevič)");
// sidro 7: hiša 41 — ISTA zveza 1890+1893 (luknja)
const p88H41 = p88Hv.find((h) => h.houseNo === "41" && h.scan === 64);
if (!p88H41 || !p88H41.whatSi.includes("Hušič") || !p88H41.whatSi.includes("ISTA ZVEZA"))
  p88Errors.push("sidro hiša 41: whatSi ≠ P88 (Matija Hušič? [~], ISTA zveza 1890+1893)");
// sidro 8: hiša 15 — ISTA zveza 1887+1893 (Jakšič/Jaklič × Brinec)
const p88H15 = p88Hv.find((h) => h.houseNo === "15" && h.scan === 66);
if (!p88H15 || !p88H15.whatSi.includes("Jaklič") || !p88H15.whatSi.includes("ISTA ZVEZA"))
  p88Errors.push("sidro hiša 15: whatSi ≠ P88 (Janez Jaklič [~] × Marija Brinec [~], ISTA zveza)");
// sidro 9: hiša 60 — NOVA (Željko 2. hiša)
const p88H60 = p88Hv.find((h) => h.houseNo === "60" && h.scan === 63);
if (!p88H60 || !p88H60.whatSi.includes("Željko") || !p88H60.whatSi.includes("2. HIŠA"))
  p88Errors.push("sidro hiša 60: whatSi ≠ P88 (Nikolaj Željko [~], Željko 2. hiša h1 → h60)");
// sidro 10: hiša 91 — NOVA (botra Željko + Kure)
const p88H91 = p88Hv.find((h) => h.houseNo === "91" && h.scan === 65);
if (!p88H91 || !p88H91.whatSi.includes("91 NOVA") || !p88H91.whatSi.includes("Željko"))
  p88Errors.push("sidro hiša 91: whatSi ≠ P88 (h91 NOVA, botra Željko + Kure)");
// PT klasifikacija == pin: 13 v naboru + 3 v luknji (46 NOVA — 15. dokazana; 41/60 že znani)
const p88InSet = [...p88Houses].filter((h) => P88_PT_IN_SET.includes(h));
const p88Gap = [...p88Houses].filter((h) => P88_PT_GAP.includes(h));
if (p88InSet.length !== 13 || p88Gap.length !== 3)
  p88Errors.push(`PT klasifikacija ≠ 13/3 (${p88InSet.length}/${p88Gap.length})`);
if (p88Gap.some((h) => !(Number(h) >= 41 && Number(h) <= 60)))
  p88Errors.push("luknjane hiše izven 41–60");
// kontinuitete čez leta prek HOUSE_VITALS
for (const [hn, yr, sig, pin] of [
  ["72", 1888, "04105", "Strauš"], ["72", 1891, "04105", "Straus"], ["65", 1887, "04105", "Milek"],
  ["65", 1889, "04105", "Milek"], ["27", 1887, "04105", "Kukar"], ["15", 1887, "04105", "Jakšič"],
  ["21", 1887, "04105", "Požek"], ["41", 1890, "04105", "Hrušič"], ["30", 1890, "04105", "Milek"],
  ["24", 1892, "04105", "Jurajevič"], ["32", 1892, "04105", "Urh"], ["1", 1888, "04105", "Zeljth"],
  ["74", 1886, "04894", "Hambeč"], ["25", 1886, "04455", "Klepec"],
] as const) {
  const blk = HOUSE_VITALS.find((v) => v.houseNo === hn && v.bookSignature === sig && v.year === yr);
  const anyBlk = HOUSE_VITALS.some((v) => v.houseNo === hn && v.bookSignature === sig && v.year === yr && v.whatSi.includes(pin));
  if (!blk || !anyBlk)
    p88Errors.push(`kontinuiteta hiša ${hn} (${yr}, ${sig}, pin ${pin}) manjka ali pin ne ustreza`);
}
// NOVE hiše 1893 (23, 46, 70, 91) — ne obstajajo v nobenem prejšnjem letu/knjigi;
// P116: h23 ima ZDAJ poročni blok 04455/1887 (nevesta Maria Brinec, GRIBLJE 23 — P80
// »29« popravljen) = prva pojavitev hiše je 1887 poročna; NOVA ostaja v okviru KRSTNEGA vzorca;
// h23: P89 kontinuiteta dovoli tudi blok 1894 (ISTI oče Brinec + ISTA botra pa);
// h46/h91: P90 kontinuiteta dovoli tudi bloke 1895 (h46 2. vpis ISTA zveza;
// h91 mati ISTA Kure, oče menjan Novak → Muc); h46: P91 dovoli blok 1896 (3. vpis)
// h23: P92 dovoli blok 1897 (Brinec × Petrlie? — 2. Brinec hiša forenzika); h46: P92 dovoli blok 1897 (4. vpis Brodarič)
for (const hn of ["23", "46", "70", "91"]) {
  // h46: P90/P91/P92/P94 kontinuiteta dovoli bloke 1895/1896/1897/1899 (5. VPIS ISTA ZVEZA; 4. varianta matere)
  const allow = hn === "23" ? [1893, 1894, 1897, 1900, 1903, 1905, 1908] : hn === "46" ? [1893, 1895, 1896, 1897, 1899, 1908, 1910, 1912, 1913, 1915, 1917, 1919] : hn === "91" ? [1893, 1895, 1902, 1904, 1908, 1910] : hn === "70" ? [1893, 1912, 1915] : [1893]; // P94: + 1899 blok h46; P107: + 1912 blok h70 (2. VPIS — SELIJA h10→h70) P95: + 1900 blok h23 (4. PIN ISTA ZVEZA — Debič? REŠENO); P97: + 1902 blok h91 (3. VPIS — boter Željko? signal 17); P98: + 1903 blok h23 (5. VPIS — Jaroslav?); P99: + 1904 blok h91 (4. VPIS — MUC KONTINUITETA, oče Janez Muc bajtar); P100: + 1905 blok h23 (6. VPIS — Matija Brinec); P103: + 1908 bloki h23 (7. VPIS — ISTA Dehlič) + h46 (6. VPIS — ISTA OČE Brodarič) + h91 (5. VPIS — Muc × Kure); P105: + 1910 bloka h46 (7. VPIS — forenzika 46) + h91 (6. VPIS — OČE MENJAVA Janez→Matija Muc) P107: + 1912 blok h46 (3. VPIS — EMŠO SKLADNO) P108: + 1913 blok h46 (9. VPIS — ZAPORED, EMŠO SIDRO); P112: + 1917 blok h46 (10. VPIS — oče 1859!); P114: + 1919 blok h46 (12. VPIS — VRZEL 2 LETI)
  if (HOUSE_VITALS.some((v) => v.houseNo === hn && !(v.bookSignature === "04105" && allow.includes(v.year)) && !(v.bookSignature === "04455" && (v.year === 1887 || (hn === "23" && v.year === 1888) || (hn === "91" && (v.year === 1890 || v.year === 1913 || v.year === 1914)) || (hn === "46" && (v.year === 1898 || v.year === 1903 || v.year === 1904 || v.year === 1909 || v.year === 1912)) || (hn === "70" && v.year === 1898))))) // P118: + poročni blok h23-1888 (BRATA Brinec!); P119: + poročni blok h91-1890 (2. familia — Johann Muc × Anna Kure!); P127: + poročni bloka h46-1898 (v20 nevesta Catharina KLOBUČAR!) + h70-1898 (v15 nevesta Maria PERDINEC!); P132: + poročni blok h46-1903 (v9 ženin Bohte — 2. poročni dokaz h46!); P133: + poročni blok h46-1904 (v14 ženin Anton Brodarič — 3. poročni dokaz h46, DRUBEL!); P138: + poročna bloka h46-1909 (№11 Žugelj × Klobučar — 4.+5. poročni dokaz h46, ★★ INTRA-HIŠNA h46 × h46!); P141: + poročni blok h46-1912 (№9 nevesta Barbara Straus — 6. poročni dokaz h46!); P142: + poročni blok h91-1913 (№10 nevesta Alojzija Mlec — 2. poročni dokaz h91 + INTRA-GRIBLJE h76 × h91 + korpus-krst 9.5.1893 h91 [P88-družina Janez M[uc→Mlec] × Ana Kure — ISTA HIŠA!] + VSEBOVANA POROKA: hčer Vilhelmina 9.9.1913 h76!; P143: + poročni blok h91-1914 (№3 ženin Janez Muc — 3. poročni dokaz h91 + INTRA-GRIBLJE h91 × h68 + predkorpusna generacija r. ~1867!))
    p88Errors.push(`NOVA hiša ${hn} (P88) že obstaja v prejšnjem letu — pini neskladni`);
}
// h60: NOVA krstna — ponovitev čez knjige (poroka 04455 1886 GRIBLJE 60)
const p88H60b = HOUSE_VITALS.find((v) => v.houseNo === "60" && v.bookSignature === "04455" && v.year === 1886);
if (!p88H60b || !p88H60b.whatSi.includes("GRIBLJE 60"))
  p88Errors.push("kontinuiteta hiša 60 (1886, 04455, pin GRIBLJE 60) manjka");
// vitals skupaj 449 (po P106: 429 + 20; krstna 1911)
if (HOUSE_VITALS.length !== 685)
  p88Errors.push(`HOUSE_VITALS ≠ 467 (${HOUSE_VITALS.length})`);
push(
  "qa-p88-parish-baptism-1893",
  "P88: ŽUPNIJA PODZEMELJ — KRSTNA KNJIGA 04105, POLNO LETO 1893 (issue #18; SAMPLE-TRANSCRIPTION-1893; MERI, NE odloča; v7 join nespremenjen): širitev vzorca P79 (1886) → P82 (1887) → P83 (1888) → P84 (1889) → P85 (1890) → P86 (1891) → P87 (1892) na leto 1893 — okvir: skeni 63–70 == tiskane strani 62–69 (stran == sken − 1; glava »1893~« na str. 62 po 1892 row 82; vpisi na skenih 63–68; velike cifre »1894« na str. 69 po row 83 — oznake se ponastavijo na 1, novela P83 potrjena 6. leto; 1893 ima 83 zveznih vrstic) — VSI vpisi z Griblji: 17 vpisov / 16 hiš (h27 DVOJČICI!): 60, 65, 41, 70, 23, 91, 27 ×2, 15, 46, 72, 30, 24, 74, 21, 25, 32 — NOVE hiše 4 (23, 46, 70, 91) + ponovitve 12 (h60 nova krstna — poroka 04455 1886) — skupaj s P79–P87 vzorec 156 vpisov / 66 hiš čez tri knjige in OSEM LET; NOVELA (novela P85 potrjena 4. leto): vsi statusi ulomki — ½ zemljak 13 + ¼ zemljak 4 (brez bajtarjev/obrtnikov); PT klasifikacija 13/3 (46 v luknji 41–60 — NOVA, 15. dokazana številka; 41 že dokazana P85, 60 P80; luknja zdaj 15 dokazanih); 0 nezakonskih; r50 brez babice (edini); r34 vsi starševski stolpci »isto« (ditto); SIDRA: h72 (oče Matija Strauš [~] — SIDRO 3. VPIS: ISTI oče 3× čez 6 let 1888+1891+1893; mati 1891+1893 ISTA Jakobič; botra Straucelj ISTA 2×; tri-virska P80 + PUA @71 0.8571 — najmočnejša veriga vzorca), h65 (oče Matija Milek [~] — ISTI 3×: 1887+1889+1893; Milek = P81 near-miss), h27 (DVOJČICI Antonija †13/9.93 + Ivana — vertikalni pripis »dvojčice«, 2. dvojčki v vzorcu po P85 h30; oče Janez Stukar/Stubhar [~] = 1887 Kukar + 1890 Stubhar ISTI; ISTA mati Katarina Klobučar — 3.+4. vpis; forenzika 5x: jasno 27, prvi prebir 24 [~]), h21 (oče Janez Požek [~] ISTI 1887+1893; MATI MENJANA: 1887 Brinec → 1893 Ana Šimec — 3. dokazana menjava matere po h61/h72; ŠIMEC NAZAJ NA GRIBLJIH — mati + botra Janez Šimec prvič od 1890; Požek 6. leto), h24 (Matija Brinec [~] × Barbara Jakobčič [~] — ISTA ZVEZA kot 1887; 5. VPIS; gospodinjstvi Brinec ↔ Jurajevič se izmenjujeta 1887→1892→1893), h30 (Peter Jakljevič [~] × Marija Kralj [~] — MENJAVA GOSPODINJSTVA Milek → Jakljevič; babica PRAZNA; podpis obiskni G. Ambrož? m.p.), h41 (Matija Hušič? [~] × Neža Jakobič [~] — ISTA ZVEZA kot 1890 Hrušič × Jakobčič; 3. vpis na luknji), h15 (Janez Jaklič [~] × Marija Brinec [~] — ISTA ZVEZA kot 1887 Jakšič × Brinec), h60 (NOVA — oče Nikolaj Željko [~] = h1 oče 1888+1892 — ŽELJKO 2. HIŠA: h1 → h60), h91 (NOVA — botra Nikolaj Željko + Katarina Kure = h1 starši priimki — Željko signal 3. hiša), h74 (mrliška 04894 1886 Hambeč [~] → Kambič? [~] — čez knjige varianta), h25 (poroka 04455 1886 Klepec GRIBLJE 25 → 1893 Matija Hrižan × Ana Požek — menjava gospodinjstva; 2. Hrižan oče), h32 (oče Matija Meh/Mrh? [~] — MERI: ISTA mati Pegdirec + ISTA botra Hrižan/Strauš kot 1892 Urh — isti oče z novo brano priimko ali drug mož); ŽELJKO VERIGA 3 hiše (h1 + h60 + h91 botra); ŠIMEC nazaj (2 signala); babice: Trotter 9× (dominanta) + Ana Hrižan 3× + Barbara Adlešič 2× + Ana Križan 1× + Ana Klepec 1× + prazna 1; DUHOVNIKI: Jos. Rauq [~] 14 (Jan–Avg) + NOV Janez Jelovšek? [~] 2 (od septembra) + G. Ambrož? m.p. 1 (obiskni); live verifikacija: knjiga HTTP 200 (inventar 326), citirani skeni 6/6 JPEG 200; skripta scripts/p88_parish_baptism_1893.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1893",
  "P88: PARISH OF PODZEMELJ — BAPTISM REGISTER 04105, THE FULL YEAR 1893 (issue #18; SAMPLE-TRANSCRIPTION-1893; MEASURES, does not decide; the v7 join unchanged): extending the P79 (1886) → P82 (1887) → P83 (1888) → P84 (1889) → P85 (1890) → P86 (1891) → P87 (1892) sample to 1893 — the frame: scans 63–70 == printed pages 62–69 (page == scan − 1; the »1893~« heading on p. 62 after the 1892 row 82; entries on scans 63–68; the large figures »1894« on p. 69 after row 83 — the labels restart at 1, the P83 novel confirmed for the 6th year; 1893 has 83 continuous rows); ALL Griblje entries: 17 entries / 16 houses (h27 TWINS!): 60, 65, 41, 70, 23, 91, 27 ×2, 15, 46, 72, 30, 24, 74, 21, 25, 32 — 4 NEW houses (23, 46, 70, 91) + 12 repeats (h60 a new baptism — the 1886 marriage 04455) — with P79–P87 the sample totals 156 entries / 66 houses across three books and EIGHT years; NOVEL (the P85 novel confirmed for the 4th year): all statuses fractions — ½ smallholder 13 + ¼ smallholder 4 (no cottagers/craftsmen); the PT classification 13/3 (46 in the 41–60 gap — NEW, the 15th proven number; 41 already proven P85, 60 P80; the gap now has 15 proven); 0 illegitimates; r50 without a midwife (the only one); r34 all parent columns »isto« (ditto); ANCHORS: h72 (father Matija Strauš [~] — the ANCHOR'S 3rd ENTRY: THE SAME father 3× across 6 years 1888+1891+1893; the mother 1891+1893 THE SAME Jakobič; godmother Straucelj THE SAME 2×; the three-source P80 + PUA @71 0.8571 — the strongest chain of the sample), h65 (father Matija Milek [~] — THE SAME 3×: 1887+1889+1893; Milek = the P81 near-miss), h27 (TWINS Antonija † + Ivana — the vertical note »dvojčice«, the 2nd twins in the sample after the P85 h30; father Janez Stukar/Stubhar [~] = 1887 Kukar + 1890 Stubhar THE SAME; THE SAME mother Katarina Klobučar — the 3rd+4th entries; 5x forensics: clearly 27, first read 24 [~]), h21 (father Janez Požek [~] THE SAME 1887+1893; MOTHER CHANGE: 1887 Brinec → 1893 Ana Šimec — the 3rd proven mother change after h61/h72; ŠIMEC BACK IN GRIBLJE — mother + godfather Janez Šimec for the first time since 1890; Požek the 6th year), h24 (Matija Brinec [~] × Barbara Jakobčič [~] — THE SAME COUPLE as 1887; the 5th ENTRY; the Brinec ↔ Jurajevič households alternate 1887→1892→1893), h30 (Peter Jakljevič [~] × Marija Kralj [~] — HOUSEHOLD CHANGE Milek → Jakljevič; midwife EMPTY; visiting signature G. Ambrož? m.p.), h41 (Matija Hušič? [~] × Neža Jakobič [~] — THE SAME COUPLE as 1890 Hrušič × Jakobčič; the 3rd entry on the gap), h15 (Janez Jaklič [~] × Marija Brinec [~] — THE SAME COUPLE as 1887 Jakšič × Brinec), h60 (NEW — father Nikolaj Željko [~] = the h1 father 1888+1892 — ŽELJKO'S 2nd HOUSE: h1 → h60), h91 (NEW — godparents Nikolaj Željko + Katarina Kure = the h1 parents' surnames — the Željko signal, a 3rd house), h74 (mrliška 04894 1886 Hambeč [~] → Kambič? [~] — the cross-book variant), h25 (the 1886 marriage 04455 Klepec GRIBLJE 25 → 1893 Matija Hrižan × Ana Požek — a household change; the 2nd Hrižan father), h32 (father Matija Meh/Mrh? [~] — MEASURES: THE SAME mother Pegdirec + THE SAME godparents Hrižan/Strauš as the 1892 Urh — either the same father with a newly read surname or another husband); THE ŽELJKO CHAIN of 3 houses (h1 + h60 + h91 godparents); ŠIMEC back (2 signals); midwives: Trotter 9× (the dominant) + Ana Hrižan 3× + Barbara Adlešič 2× + Ana Križan 1× + Ana Klepec 1× + empty 1; PRIESTS: Jos. Rauq [~] 14 (Jan–Aug) + NEW Janez Jelovšek? [~] 2 (from September) + G. Ambrož? m.p. 1 (visiting); live verification: the book HTTP 200 (inventory 326), cited scans 6/6 JPEG 200; the script scripts/p88_parish_baptism_1893.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1893",
  p88Errors.length === 0,
  p88Errors.length === 0
    ? `17 vpisov / 16 hiš — h27 DVOJČICI (0 neberljivih; 17 zasidranih v vitals) · okvir 1893 skeni 63–70 (vpisi 63–68; prelom 1894 str. 69; 83 zveznih vrstic) · NOVELA: ulomki, novela P85 potrjena 4. leto (½ 13 + ¼ 4) · PT 13/3 (46 NOVA — 15. dokazana luknja; 41/60 že znani) · nove hiše 4 (23, 46, 70, 91) + ponovitve 12 (h60 nova krstna) · sidra h72 Strauš SIDRO 3. VPIS (oče ISTI 3×) / h65 Milek oče ISTI 3× / h27 dvojčici (oče ISTI, ISTA mati) / h21 Šimec nazaj + mati menjana / h24 ISTA zveza 1887+1893 / h30 menjava Milek → Jakljevič / h41 ISTA zveza / h15 ISTA zveza / h60 Željko 2. hiša / h91 NOVA botra Željko · Željko veriga 3 hiše · Šimec nazaj · Rauq 14× + NOV Jelovšek? od sept.`
    : p88Errors.join("; "),
);

// ——— qa-p89: p89 krstna 1894 — širitev vzorca na leto 1894 (issue #18;
//      SAMPLE-TRANSCRIPTION-1894; celoven neodvisen preracun iz bundled
//      virov: HOUSE_VITALS × PARISH_BOOKS; PT klasifikacija iz pinov;
//      NOVELA OKVIRA: sken 73 = podvojen sken str. 71 (matricula re-scan,
//      prvi v seriji) — stran == sken − 1 do skena 72, od skena 74 naprej
//      − 2; NOVELA VZORCA: PRVO leto z 0 novih hiš (vseh 14 že zasidranih);
//      sidra: h2 ŠTIRIKRATNA kontinuiteta (ISTI starši Hlebec × Jakobič 4×:
//      1887+1889+1891+1894), h71 ISTA zveza Jurij Strauš × Barbara čez 8 let
//      (P77 1886; Strauš na DVEH hišah h71+h72; PUA @71 0.8571), h36 Križan
//      2. GENERACIJA (4. vir tri-virske hiše), h31 4. VPIS (oče Papič/Fapič
//      ISTI + mati Straus ISTA + botra Klobučar), h17 ISTI oče Kralj ¼ +
//      MATER MENJANA (Jakobič → Firlak? — 5.), h57 ISTA botra pa čez 8 let
//      (P77), h60 + h23 ISTA botra pa 2. leto (P88), h12/h53/h73/h75 ISTA
//      zvezi (2. vpis); paleografska faza v research/issue17/
//      parish-baptism-1894.json, live verifikator
//      scripts/p89_parish_baptism_1894.py --check I1–I10) ———
const p89Hv = HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year === 1894);
const p89Errors: string[] = [];
const P89_PT_IN_SET = ["2", "12", "13", "17", "23", "31", "36", "69", "71", "73", "75"];
const P89_PT_GAP = ["53", "57", "60"];
if (p89Hv.length !== 14)
  p89Errors.push(`vpisov 1894 (04105, zasidrani) ≠ 14 (${p89Hv.length})`);
const p89Houses = new Set(p89Hv.map((h) => h.houseNo));
if (p89Houses.size !== 14)
  p89Errors.push(`različnih hiš ≠ 14 (${p89Houses.size}: ${[...p89Houses].sort((a, b) => Number(a) - Number(b)).join(",")})`);
// okvir 1894: skeni 70–78; stran == sken − 1 do skena 72, od skena 74 naprej
// − 2 (sken 73 = podvojen sken str. 71 — novela P89); sken 73 NI citiran
const p89Bad = p89Hv.filter(
  (h) => h.status !== "DOCUMENTED" || !h.scan || !h.page
    || h.page !== (h.scan >= 74 ? h.scan - 2 : h.scan - 1)
    || h.scan < 70 || h.scan > 78 || h.scan === 73,
);
if (p89Bad.length > 0)
  p89Errors.push(`okvir 1894: skeni 70–78 (brez podvojenega 73) ali stran ≠ sken − 1 / − 2 krščeno pri ${p89Bad.length}`);
// sidro 1: hiša 2 — ŠTIRIKRATNA kontinuiteta (ISTI starši Hlebec × Jakobič)
const p89H2 = p89Hv.find((h) => h.houseNo === "2" && h.scan === 71);
if (!p89H2 || !p89H2.whatSi.includes("Hlebec") || !p89H2.whatSi.includes("4. VPIS"))
  p89Errors.push("sidro hiša 2: whatSi ≠ P89 (Peter Hlebec [~] ¼, 4. VPIS — ŠTIRIKRATNA kontinuiteta)");
// sidro 2: hiša 71 — ISTA zveza Jurij Strauš × Barbara čez 8 let (P77 1886)
const p89H71 = p89Hv.find((h) => h.houseNo === "71" && h.scan === 77);
if (!p89H71 || !p89H71.whatSi.includes("Straus") || !p89H71.whatSi.includes("ISTA ZVEZA"))
  p89Errors.push("sidro hiša 71: whatSi ≠ P89 (Jurij Straus [~] ¼ × Barbara [~], ISTA zveza čez 8 let)");
// sidro 3: hiša 36 — Križan 2. generacija (4. vir tri-virske hiše)
const p89H36 = p89Hv.find((h) => h.houseNo === "36" && h.scan === 72);
if (!p89H36 || !p89H36.whatSi.includes("Križan") || !p89H36.whatSi.includes("2. GENERACIJA"))
  p89Errors.push("sidro hiša 36: whatSi ≠ P89 (Janez Križan? [~], Križan 2. GENERACIJA)");
// sidro 4: hiša 31 — 4. VPIS (oče Fapič ISTI + mati Straus ISTA + botra Klobučar)
const p89H31 = p89Hv.find((h) => h.houseNo === "31" && h.scan === 75);
if (!p89H31 || !p89H31.whatSi.includes("Fapič") || !p89H31.whatSi.includes("Straus") || !p89H31.whatSi.includes("4. VPIS"))
  p89Errors.push("sidro hiša 31: whatSi ≠ P89 (Martin Fapič? [~] × Marjeta Straus? [~], 4. VPIS)");
// sidro 5: hiša 17 — ISTI oče Kralj ¼ + MATER MENJANA (Jakobič → Firlak?)
const p89H17 = p89Hv.find((h) => h.houseNo === "17" && h.scan === 76);
if (!p89H17 || !p89H17.whatSi.includes("Kralj") || !p89H17.whatSi.includes("Firlak") || !p89H17.whatSi.includes("MATER MENJANA"))
  p89Errors.push("sidro hiša 17: whatSi ≠ P89 (Janez Kralj? [~] ¼, mati menjana Jakobič → Firlak?)");
// sidro 6: hiša 57 — ISTA botra pa čez 8 let (P77 r20 Brodarič × Strauš)
const p89H57 = p89Hv.find((h) => h.houseNo === "57" && h.scan === 74);
if (!p89H57 || !p89H57.whatSi.includes("Pegdirec") || !p89H57.whatSi.includes("BOTRA PA ISTA"))
  p89Errors.push("sidro hiša 57: whatSi ≠ P89 (Peter Pegdirec? [~], ISTA botra pa čez 8 let)");
// sidro 7: hiša 60 — ISTA zveza + ISTA botra pa 2. leto (P88 r1)
const p89H60 = p89Hv.find((h) => h.houseNo === "60" && h.scan === 78);
if (!p89H60 || !p89H60.whatSi.includes("Željko") || !p89H60.whatSi.includes("Brodarič") || !p89H60.whatSi.includes("ISTA BOTRA PA"))
  p89Errors.push("sidro hiša 60: whatSi ≠ P89 (Nikolaj Željko [~] × Marija Brodarič, ISTA botra pa 2. leto)");
// sidro 8: hiša 23 — ISTI oče Brinec + ISTA botra pa 2. leto (P88 r28)
const p89H23 = p89Hv.find((h) => h.houseNo === "23" && h.scan === 78);
if (!p89H23 || !p89H23.whatSi.includes("Brinec") || !p89H23.whatSi.includes("ISTA BOTRA PA"))
  p89Errors.push("sidro hiša 23: whatSi ≠ P89 (Matija Brinec [~], ISTA botra pa 2. leto)");
// sidro 9: hiša 13 — babica PRAZNA (druga po P88 r50)
const p89H13 = p89Hv.find((h) => h.houseNo === "13" && h.scan === 75);
if (!p89H13 || !p89H13.whatSi.includes("babica PRAZNA"))
  p89Errors.push("sidro hiša 13: whatSi ≠ P89 (babica PRAZNA — druga po P88 r50)");
// PT klasifikacija == pin: 11 v naboru + 3 v luknji (53/57/60 — vse PONOVITVE, 0 novih)
const p89InSet = [...p89Houses].filter((h) => P89_PT_IN_SET.includes(h));
const p89Gap = [...p89Houses].filter((h) => P89_PT_GAP.includes(h));
if (p89InSet.length !== 11 || p89Gap.length !== 3)
  p89Errors.push(`PT klasifikacija ≠ 11/3 (${p89InSet.length}/${p89Gap.length})`);
if (p89Gap.some((h) => !(Number(h) >= 41 && Number(h) <= 60)))
  p89Errors.push("luknjane hiše izven 41–60");
// NOVELA: 0 novih hiš — vsa 14 že v vitals prej (≠ 1894)
for (const hn of p89Houses) {
  if (!HOUSE_VITALS.some((v) => v.houseNo === hn && !(v.bookSignature === "04105" && v.year === 1894)))
    p89Errors.push(`NOVELA krščena: hiša ${hn} NIMA prejšnjega zasidranja — pričakovano 0 novih hiš`);
}
// kontinuitete čez leta prek HOUSE_VITALS
for (const [hn, yr, sig, pin] of [
  ["2", 1887, "04105", "Hlebec"], ["2", 1889, "04105", "Hlebec"], ["2", 1891, "04105", "Hlebec"],
  ["31", 1887, "04105", "Papič"], ["31", 1890, "04105", "Papič"], ["31", 1891, "04105", "Tepič"],
  ["53", 1891, "04105", "Pozdirec"], ["73", 1892, "04105", "Županič"], ["75", 1892, "04105", "Jakobčič"],
  ["12", 1892, "04105", "Dragos"], ["17", 1887, "04105", "Kralj"], ["71", 1886, "04105", "Strauš"],
  ["36", 1886, "04105", "Križan"], ["57", 1886, "04105", "Podolivec"], ["13", 1886, "04105", "Jakopič"],
  ["23", 1893, "04105", "Brinec"], ["60", 1893, "04105", "Željko"], ["1", 1888, "04105", "Zeljth"],
  ["69", 1886, "04894", "Podec"],
] as const) {
  const blk = HOUSE_VITALS.find((v) => v.houseNo === hn && v.bookSignature === sig && v.year === yr);
  const anyBlk = HOUSE_VITALS.some((v) => v.houseNo === hn && v.bookSignature === sig && v.year === yr && v.whatSi.includes(pin));
  if (!blk || !anyBlk)
    p89Errors.push(`kontinuiteta hiša ${hn} (${yr}, ${sig}, pin ${pin}) manjka ali pin ne ustreza`);
}
// vitals skupaj 449 (po P106: 429 + 20; krstna 1911)
if (HOUSE_VITALS.length !== 685)
  p89Errors.push(`HOUSE_VITALS ≠ 467 (${HOUSE_VITALS.length})`);
push(
  "qa-p89-parish-baptism-1894",
  "P89: ŽUPNIJA PODZEMELJ — KRSTNA KNJIGA 04105, POLNO LETO 1894 (issue #18; SAMPLE-TRANSCRIPTION-1894; MERI, NE odloča; v7 join nespremenjen): širitev vzorca P79 (1886) → P82 (1887) → P83 (1888) → P84 (1889) → P85 (1890) → P86 (1891) → P87 (1892) → P88 (1893) na leto 1894 — okvir: skeni 70–78 == tiskane strani 69–76 (NOVELA OKVIRA: sken 73 je PODOVOJEN sken str. 71 — matricula re-scan, prvi v seriji; stran == sken − 1 velja do skena 72, od skena 74 naprej − 2; glava »1894« na str. 69 po 1893 row 83; vpisi na skenih 70, 71, 72, 74–78; velike cifre »1895~« na str. 76 po row 90 — oznake se ponastavijo na 1, novela P83 potrjena 7. leto; 1894 ima 90 zveznih vrstic — najdaljše doslej) — VSI vpisi z Griblji: 14 vpisov / 14 hiš (prvo leto brez ponovitev znotraj leta po P87 NARE): 12, 2, 53, 69, 36, 57, 73, 31, 13, 75, 17, 71, 23, 60 — NOVELA VZORCA: 0 NOVIH hiš (vseh 14 že zasidranih — vzorec se ZASIČA; 65 hiš naprej) — skupaj s P79–P88 vzorec 170 vpisov / 65 hiš čez tri knjige in DEVET LET; NOVELA (novela P85 potrjena 5. leto): vsi statusi ulomki — ½ zemljak 8 + ¼ zemljak 6 (brez bajtarjev/obrtnikov); PT klasifikacija 11/3 (53 + 57 + 60 v luknji 41–60 — vse tri PONOVITVE, brez novih; luknja ostaja 15 dokazanih); 0 nezakonskih; r50 brez babice (druga po P88); SIDRA: h2 (Peter Hlebec [~] ¼ × Ana Jakobič [~] — ŠTIRIKRATNA KONTINUETETA: ISTI starši vseh 4× 1887+1889+1891+1894 — najdaljša zasidrana zveza vzorca; moder pripis: mati † 1965 Novo mesto), h71 (Jurij Straus? [~] ¼ × Barbara Jakobčič? [~] — ISTA ZVEZA čez 8 let: P77 1886 r83 »Jurij Strauš ½ × Barbara Jakopič«; status ½→¼; STRAUŠ na DVEH sosednjih hišah h71+h72 — PUA @71 0.8571 dobi krstno oporo), h36 (Janez Križan? [~] ¼ × Katarina Straucelj? [~] — 3. krstni vpis + 4. VIR tri-virske hiše: KRIŽAN 2. GENERACIJA — Matija Križan 1882 poroka + 1886 krst → Janez 1894, mogoč sin [~] MERI), h31 (Martin Fapič? [~] ½ × Marjeta Straus? [~] — 4. VPIS 1887+1890+1891+1894: oče Papič/Fapič/Tepič Kurrent P/F/T ISTI + mati ISTA vseh 4× + botra Marko Klobučar ISTI kot 1887 — najbolj popolna trojica), h17 (Janez Kralj? [~] ¼ — ISTI oče ISTA frakcija kot P82 1887 r82; MATER MENJANA: Ana Jakobič → Doroteja Firlak? [~] — 5. dokazana po h61/h72/h21), h57 (Peter Pegdirec? [~] × Marija Županc? [~] — 2. vpis čez 8 let; ISTA BOTRA PA čez 8 let: Jurij Brodarič? + Marija Strauš? = P77 r20), h60 (Nikolaj Željko [~] ¼ × Marija Brodarič [~] — h60 2. VPIS ISTA zveza + ISTA BOTRA PA 2. leto (P88 r1: Marko Pegdirec + Marija Klepec); status ½→¼; ŽELJKO VERIGA 4 hiše signalov: h1 (1888+1892) + h60 (1893+1894) + h91 botra + h25 botra), h23 (Matija Brinec [~] ½ — ISTI oče kot P88 + ISTA BOTRA PA 2. leto: Janez Jaklič + Doroteja Pegdirec; mati Debič?/Žehlič? varianti), h12 (Janez Dragoš [~] ½ — ISTI oče kot P87, 2. vpis; mati Civlkovič?/Druppovič? varianti), h53 (Janez Pegdirec? [~] × Marija Hrižan? [~] — ISTA zveza kot P86 Pozdirec × Križan + babica Ana H/Križan ISTA; 2. vpis na luknji), h73 (Nikolaj Županič? [~] × Katarina Pozdirec/Pegdirec? [~] — ISTA zveza kot P87, 2. vpis), h75 (Janez Jakobič? [~] × Marija Stubljar? [~] — ISTA zveza kot P87 Jakobčič × Sušljar + ženska botra Barb. Brinec ISTA 2. leto), h13 (Matija Jakljevič? [~] ½ — ISTI oče ime+status kot P77 1886 »Jakopič? ½«; tri-virska hiša; babica PRAZNA), h69 (Janez Brinec [~] × Ana Kure [~] — NOV krstni vpis čez knjige: mrliška 04894 1886; botra Katarina Požek? — Požek 7. leto); Pegdirec/Pozdirec familija 7/14 vpisov (najgostejša botrska familija 1894); menjava statusov h71/h60 (½→¼); DUHOVNIKI: Jan Jelenu—? [~] 11 (verjetno ISTI kot P88 »Jelovšek?« — varianti istega podpisa [~] MERI) + Jos. Rauq? [~] 3 (Feb/Sep/Dec — izmenjava NI čista); babice: Trotter 11× (2. leto dominanta; Kurrent J/T »Jotter«; Margan. = Margareta) + Ana Hrižan 2× + prazna 1; live verifikacija: knjiga HTTP 200 (inventar 326), citirani skeni 8/8 JPEG 200 (sken 73 NI citiran — podvojen); skripta scripts/p89_parish_baptism_1894.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1894",
  "P89: PARISH OF PODZEMELJ — BAPTISM REGISTER 04105, THE FULL YEAR 1894 (issue #18; SAMPLE-TRANSCRIPTION-1894; MEASURES, does not decide; the v7 join unchanged): extending the P79 (1886) → P82 (1887) → P83 (1888) → P84 (1889) → P85 (1890) → P86 (1891) → P87 (1892) → P88 (1893) sample to 1894 — the frame: scans 70–78 == printed pages 69–76 (FRAME NOVELTY: scan 73 is a DUPLICATE of page 71 — a Matricula re-scan, the first in the series; page == scan − 1 holds up to scan 72, from scan 74 onward it is − 2; the »1894« heading on p. 69 after the 1893 row 83; entries on scans 70, 71, 72, 74–78; the large figures »1895~« on p. 76 after row 90 — the labels restart at 1, the P83 novel confirmed for the 7th year; 1894 has 90 continuous rows — the longest so far); ALL Griblje entries: 14 entries / 14 houses (the first year without within-year repeats since P87 SQUARE); SAMPLE NOVELTY: 0 NEW houses (all 14 already anchored — the sample is SATURATING; 65 houses onward) — with P79–P88 the sample totals 170 entries / 65 houses across three books and NINE years; NOVEL (the P85 novel confirmed for the 5th year): all statuses fractions — ½ smallholder 8 + ¼ smallholder 6 (no cottagers/craftsmen); the PT classification 11/3 (53 + 57 + 60 in the 41–60 gap — all three REPEATS, no new; the gap remains 15 proven); 0 illegitimates; r50 without a midwife (the second after P88); ANCHORS: h2 (Peter Hlebec [~] ¼ × Ana Jakobič [~] — QUADRUPLE CONTINUITY: THE SAME parents all 4× 1887+1889+1891+1894 — the longest anchored couple in the sample; blue note: mother † 1965 Novo mesto), h71 (Jurij Straus? [~] ¼ × Barbara Jakobčič? [~] — THE SAME COUPLE over 8 years: P77 1886 r83 »Jurij Strauš ½ × Barbara Jakopič«; status ½→¼; STRAUŠ on TWO adjacent houses h71+h72 — the PUA @71 0.8571 signal gains baptism corroboration), h36 (Janez Križan? [~] ¼ × Katarina Straucelj? [~] — the 3rd baptismal entry + a 4th SOURCE for the three-source house: KRIŽAN 2nd GENERATION — Matija Križan 1882 marriage + 1886 baptism → Janez 1894, possibly the son [~]), h31 (Martin Fapič? [~] ½ × Marjeta Straus? [~] — the 4th ENTRY 1887+1890+1891+1894: the father Papič/Fapič/Tepič Kurrent P/F/T THE SAME + the mother THE SAME all 4× + godparent Marko Klobučar THE SAME as 1887 — the most complete trio), h17 (Janez Kralj? [~] ¼ — THE SAME father with THE SAME fraction as P82 1887 r82; MOTHER CHANGE: Ana Jakobič → Doroteja Firlak? [~] — the 5th documented after h61/h72/h21), h57 (Peter Pegdirec? [~] × Marija Županc? [~] — the 2nd entry over 8 years; THE SAME godparent pair over 8 years: Jurij Brodarič? + Marija Strauš? = P77 r20), h60 (Nikolaj Željko [~] ¼ × Marija Brodarič [~] — h60 2nd ENTRY THE SAME couple + THE SAME godparent pair 2nd year (P88 r1: Marko Pegdirec + Marija Klepec); status ½→¼; THE ŽELJKO CHAIN 4 house-signals: h1 (1888+1892) + h60 (1893+1894) + h91 godparent + h25 godparent), h23 (Matija Brinec [~] ½ — THE SAME father as P88 + THE SAME godparent pair 2nd year: Janez Jaklič + Doroteja Pegdirec; mother Debič?/Žehlič? variants), h12 (Janez Dragoš [~] ½ — THE SAME father as P87, 2nd entry; mother Civlkovič?/Druppovič? variants), h53 (Janez Pegdirec? [~] × Marija Hrižan? [~] — THE SAME couple as P86 Pozdirec × Križan + midwife Ana H/Križan THE SAME; 2nd entry on the gap), h73 (Nikolaj Županič? [~] × Katarina Pozdirec/Pegdirec? [~] — THE SAME couple as P87, 2nd entry), h75 (Janez Jakobič? [~] × Marija Stubljar? [~] — THE SAME couple as P87 Jakobčič × Sušljar + the female godparent Barb. Brinec THE SAME 2nd year), h13 (Matija Jakljevič? [~] ½ — THE SAME father's name+status as P77 1886 »Jakopič? ½«; the three-source house; midwife EMPTY), h69 (Janez Brinec [~] × Ana Kure [~] — a NEW baptismal entry cross-book: the 1886 death register 04894; godparent Katarina Požek? — Požek the 7th year); the Pegdirec/Pozdirec family in 7/14 entries (the densest godparent family of 1894); status changes h71/h60 (½→¼); PRIESTS: Jan Jelenu—? [~] 11 (probably THE SAME as P88 »Jelovšek?« — reading variants of the same signature [~]) + Jos. Rauq? [~] 3 (Feb/Sep/Dec — the alternation is NOT clean); midwives: Trotter 11× (the dominant 2nd year; Kurrent J/T »Jotter«; Margan. = Margareta) + Ana Hrižan 2× + empty 1; live verification: the book HTTP 200 (inventory 326), cited scans 8/8 JPEG 200 (scan 73 NOT cited — duplicated); the script scripts/p89_parish_baptism_1894.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1894",
  p89Errors.length === 0,
  p89Errors.length === 0
    ? `14 vpisov / 14 hiš — 0 NOVIH hiš (NOVELA: vseh 14 že zasidranih — vzorec se zasiča; 0 neberljivih; 14 zasidranih v vitals) · okvir 1894 skeni 70–78 (vpisi 70/71/72/74–78; sken 73 = podvojen str. 71 — NOVELA; prelom 1895 str. 76; 90 zveznih vrstic) · NOVELA: ulomki, novela P85 potrjena 5. leto (½ 8 + ¼ 6) · PT 11/3 (53+57+60 — vse ponovitve, brez novih) · sidra h2 ŠTIRIKRATNA kontinuiteta (ISTI starši 4×) / h71 ISTA zveza čez 8 let (Strauš na h71+h72; PUA @71) / h36 Križan 2. generacija (4. vir) / h31 4. VPIS (oče+mati+botra vsi ISTI) / h17 mati menjana (Jakobič → Firlak?) / h57 ISTA botra pa čez 8 let / h60 + h23 ISTA botra pa 2. leto / h12/h53/h73/h75 ISTA zvezi · Željko veriga 4 signali · Pegdirec 7/14 · Jelenuš? 11× + Rauq 3× · Trotter 11×`
    : p89Errors.join("; "),
);

// ——— qa-p90: p90 krstna 1895 — širitev vzorca na leto 1895 (issue #18;
//      SAMPLE-TRANSCRIPTION-1895; celoven neodvisen preracun iz bundled
//      virov: HOUSE_VITALS × PARISH_BOOKS; PT klasifikacija iz pinov;
//      NOVELA P89 POTRJENA 2. LETO: stran == sken − 2 za celo leto (sken 73
//      podvojen, ni citiran); NOVELI VZORCA: babica stolpec na vseh 15
//      vrsticah PRAZEN (1894: Trotter 11×) — Trotter žene 7× kot BOTRA; 4×
//      PRAZNA botra (sep–dec); 3 NOVE hiše (20, 37, 87) po P89 »0 novih«;
//      h24 DVOM 2× — prva ponovitev hiše znotraj leta po P87 NARE; sidra:
//      h58 4. VPIS + MATI MENJANA (Dragoš → Kambic?), h32 + h72 5. VPIS —
//      NAJDALJŠI zvezi (1889–1895), h69 oče ISTI 5×, h30 3. DRUŽINA (2×
//      menjava), h29 MENJAVA (»hiša kuge« → Kuhar? × Klobučar), h91 oče
//      MENJAN (Novak → Muc), h46/h24/h12/h65 kontinuitete; MATI PODCELICA
//      (X × Y) prvič eksplicitno dokumentirana; paleografska faza v
//      research/issue17/parish-baptism-1895.json, live verifikator
//      scripts/p90_parish_baptism_1895.py --check I1–I10) ———
const p90Hv = HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year === 1895);
const p90Errors: string[] = [];
const P90_PT_IN_SET = ["12", "20", "24", "29", "30", "32", "37", "65", "69", "72", "87", "91"];
const P90_PT_GAP = ["46", "58"];
if (p90Hv.length !== 15)
  p90Errors.push(`vpisov 1895 (04105, zasidrani) ≠ 15 (${p90Hv.length})`);
const p90Houses = new Set(p90Hv.map((h) => h.houseNo));
if (p90Houses.size !== 14)
  p90Errors.push(`različnih hiš ≠ 14 (${p90Houses.size}: ${[...p90Houses].sort((a, b) => Number(a) - Number(b)).join(",")})`);
// okvir 1895: skeni 78–84; stran == sken − 2 za celo leto (novela P89, 2. leto)
const p90Bad = p90Hv.filter(
  (h) => h.status !== "DOCUMENTED" || !h.scan || !h.page
    || h.page !== h.scan - 2
    || h.scan < 78 || h.scan > 84,
);
if (p90Bad.length > 0)
  p90Errors.push(`okvir 1895: skeni 78–84 ali stran ≠ sken − 2 krščeno pri ${p90Bad.length}`);
// NOVELA babica: vsi 15 blokov PRAZNI stolpec babice (1894: Trotter 11×)
const p90Babica = p90Hv.filter((h) => h.whatSi.includes("babica PRAZEN") || h.whatSi.includes("babica stolpec PRAZEN"));
if (p90Babica.length !== 15)
  p90Errors.push(`NOVELA babica: praznih ≠ 15 (${p90Babica.length})`);
// sidra (15 vpisov)
const p90Anchor = (hn: string, scan: number, pins: string[], label: string) => {
  const blk = p90Hv.find((h) => h.houseNo === hn && h.scan === scan);
  if (!blk || !pins.every((p) => blk.whatSi.includes(p)))
    p90Errors.push(`sidro ${label}: whatSi ≠ P90 (${pins.join(" + ")})`);
};
p90Anchor("58", 79, ["Požek", "4. VPIS", "MATI MENJANA"], "hiša 58");
p90Anchor("46", 80, ["Brodarič", "2. VPIS", "PT LUKNJA"], "hiša 46");
p90Anchor("87", 80, ["Pegdirec", "NOVA HIŠA"], "hiša 87");
p90Anchor("24", 80, ["Brime", "3. VPIS"], "hiša 24 (r22)");
p90Anchor("12", 80, ["Dragoš", "3. VPIS"], "hiša 12");
p90Anchor("30", 80, ["Šegina", "3. DRUŽINA"], "hiša 30");
p90Anchor("20", 82, ["Pezdirec", "NOVA HIŠA"], "hiša 20");
p90Anchor("65", 82, ["Mihelt", "4. VPIS"], "hiša 65");
p90Anchor("32", 82, ["Urh", "5. VPIS", "NAJDALJŠA ZVEZA"], "hiša 32");
p90Anchor("37", 82, ["Pezdirec", "NOVA HIŠA"], "hiša 37");
p90Anchor("69", 83, ["Brinec", "5. VPIS"], "hiša 69");
p90Anchor("72", 83, ["Straus", "5. VPIS"], "hiša 72");
p90Anchor("91", 83, ["Muc", "2. VPIS"], "hiša 91");
p90Anchor("29", 84, ["Kuhar", "MENJAVA GOSPODINJSTVA"], "hiša 29");
// sidro h24 DVOM (r48, sken 82): forenzika vztraja 24, alternative 21/27
const p90H24b = p90Hv.find((h) => h.houseNo === "24" && h.scan === 82);
if (!p90H24b || !p90H24b.whatSi.includes("Toško") || !p90H24b.whatSi.includes("DVOM"))
  p90Errors.push("sidro hiša 24 (r48 DVOM): whatSi ≠ P90 (Janez Toško? [~], DVOM 21/27)");
// PT klasifikacija == pin: 12 v naboru + 2 v luknji (46 = 2. dokaz; 58 = 4. vpis
// — obe že v PT_GAP_KNOWN, brez novih števil, luknja ostaja 15 dokazanih)
const p90InSet = [...p90Houses].filter((h) => P90_PT_IN_SET.includes(h));
const p90Gap = [...p90Houses].filter((h) => P90_PT_GAP.includes(h));
if (p90InSet.length !== 12 || p90Gap.length !== 2)
  p90Errors.push(`PT klasifikacija ≠ 12/2 (${p90InSet.length}/${p90Gap.length})`);
if (p90Gap.some((h) => !(Number(h) >= 41 && Number(h) <= 60)))
  p90Errors.push("luknjane hiše izven 41–60");
// NOVE hiše 1895 (20, 37, 87) — ne obstajajo v nobenem prejšnjem letu/knjigi;
// P116: h37 ima ZDAJ poročni blok 04455/1887 (nevesta Barbara Rusić, GRIBLJE 37) = prva
// pojavitev hiše je 1887 poročna; NOVA ostaja v okviru KRSTNEGA vzorca;
// h20/h37: P92 dovoli bloka 1897 (h20 2. pin Pendirec? × Klepec?; h37 2. pin Pendirec? × Zugelj?)
for (const hn of ["20", "37", "87"]) {
  const allow = hn === "20" ? [1895, 1897, 1900, 1903, 1906] : hn === "37" ? [1895, 1897, 1916, 1917] : hn === "87" ? [1895, 1902, 1904] : [1895]; // P95: + 1900 blok h20 (3. PIN Pendirec × Klepec); P97: + 1902 blok h87 (2. VPIS — oče Pegdirec?/Perdinec? KURRENT); P98: + 1903 blok h20 (4. VPIS — EMŠO sidro); P99: + 1904 blok h87 (3. VPIS — NI menjava, Marko Podrinec bajtar); P111: + 1916 blok h37 (MRTVOROJEN in utero!); P112: + 1917 blok h37 (Marija — nadaljevanje!); P101: + 1906 blok h20 (5. VPIS — ISTA DRUŽINA Perdinec/Pozdirec × Klepec)
  if (HOUSE_VITALS.some((v) => v.houseNo === hn && !(v.bookSignature === "04105" && allow.includes(v.year)) && !(v.bookSignature === "04455" && v.year === 1887) && !(v.bookSignature === "04455" && v.year === 1889 && hn === "87") && !(v.bookSignature === "04455" && v.year === 1891 && (hn === "20" || hn === "87")) && !(v.bookSignature === "04455" && v.year === 1899 && hn === "20") && !(v.bookSignature === "04455" && v.year === 1903 && hn === "20"))) // P118: + poročni blok h87-1889 (1. poročni dokaz!); P120: + poročna bloka h87/h20-1891 (h87 2. dokaz + h20 1. dokaz!); P128: + poročni blok h20-1899 (v4 ženin Alois Novak — 2. poročni dokaz!); P132: + poročni blok h20-1903 (v17 ženin Pezdirec — 3. poročni dokaz h20, DRUBEL!)
    p90Errors.push(`NOVA hiša ${hn} (P90) že obstaja v prejšnjem letu — pini neskladni`);
}
// kontinuitete čez leta prek HOUSE_VITALS (vse PONOVITVE imajo prejšnje
// zasidranje; NOVE 20/37/87 izključene zgoraj)
for (const [hn, yr, sig, pin] of [
  ["58", 1889, "04105", "Požek"], ["58", 1890, "04105", "Požek"], ["58", 1892, "04105", "Požek"],
  ["46", 1893, "04105", "Brodarič"],
  ["24", 1887, "04105", "Brinec"], ["24", 1893, "04105", "Brinec"],
  ["12", 1892, "04105", "Dragos"], ["12", 1894, "04105", "Dragoš"],
  ["30", 1890, "04105", "Milek"], ["30", 1891, "04105", "Milek"], ["30", 1893, "04105", "Jakljevič"],
  ["65", 1887, "04105", "Milek"], ["65", 1893, "04105", "Milek"],
  ["32", 1889, "04105", "Urh"], ["32", 1890, "04105", "Urh"], ["32", 1892, "04105", "Urh"],
  ["72", 1888, "04105", "Strauš"], ["72", 1893, "04105", "Strauš"],
  ["91", 1893, "04105", "Novak"],
  ["69", 1888, "04105", "Brinec"], ["69", 1894, "04105", "Brinec"],
  ["29", 1888, "04105", "Milek"], ["29", 1892, "04105", "Milek"],
  ["63", 1892, "04105", "Hrižan"],
  ["1", 1888, "04105", "Zeljth"], ["60", 1894, "04105", "Željko"],
] as const) {
  const blk = HOUSE_VITALS.find((v) => v.houseNo === hn && v.bookSignature === sig && v.year === yr);
  const anyBlk = HOUSE_VITALS.some((v) => v.houseNo === hn && v.bookSignature === sig && v.year === yr && v.whatSi.includes(pin));
  if (!blk || !anyBlk)
    p90Errors.push(`kontinuiteta hiša ${hn} (${yr}, ${sig}, pin ${pin}) manjka ali pin ne ustreza`);
}
// vitals skupaj 449 (po P106: 429 + 20; krstna 1911)
if (HOUSE_VITALS.length !== 685)
  p90Errors.push(`HOUSE_VITALS ≠ 467 (${HOUSE_VITALS.length})`);
push(
  "qa-p90-parish-baptism-1895",
  "P90: ŽUPNIJA PODZEMELJ — KRSTNA KNJIGA 04105, POLNO LETO 1895 (issue #18; SAMPLE-TRANSCRIPTION-1895; MERI, NE odloča; v7 join nespremenjen): širitev vzorca P79 (1886) → … → P89 (1894) na leto 1895 — okvir: skeni 78–84 == tiskane strani 76–82 (NOVELA P89 POTRJENA 2. LETO: stran == sken − 2 ZA CELO LETO; sken 73 podvojen, NI citiran; glava »1895.~« na str. 76 po 1894 row 90; leto 1895 ima 73 zveznih vrstic; prelom 1896 na str. 83 = sken 85 po row 73 — oznake se ponastavijo na 1, novela P83 potrjena 8. leto) — VSI vpisi z Griblji: 15 vpisov / 14 hiš (h24 DVOM 2× — prva ponovitev hiše znotraj leta po P87 NARE): 58, 46, 87, 24 ×2, 12, 30, 20, 65, 32, 37, 69, 72, 91, 29 — 3 NOVE hiše (20, 37, 87) po P89 »0 novih« + 11 ponovitev; skupaj s P79–P89 vzorec 185 vpisov / 68 hiš čez tri knjige in DESET LET; NOVELI VZORCA: ① babica stolpec na VSEH 15 vrsticah PRAZEN (1894: Trotter 11×!) — Trotter žene pa 7× kot BOTRA — vloga prestopila iz babiške v botrsko; ② 4× PRAZNA botra (r53/r54/r55/r66 — september–december cluster; P89: vedno zapisana); statusi: ½ zemljak 10 + ¼ zemljak 2 + bajtar 1 + r18 ¼ [~] — vsi ulomki + 1 bajtar (novela P85, 6. leto); PT klasifikacija 12/2 (46 + 58 v luknji 41–60 — h46 2. dokaz P88+P90, h58 4. vpis; brez novih števil, luknja ostaja 15 dokazanih; hiše 20/30/37/87/91 vse v naboru PT); 0 nezakonskih na Gribljih (2 izven: r31 Primostek + r61 Krasinec); MATI PODCELICA (X × Y) prvič eksplicitno dokumentirana — semantika desne podcelice matere ODPRTA (starši matere? očeta? mešano) — vsebine verbatim; SIDRA: h58 (oče Janez Požek [~] ISTI 3. leto zapored 1890+1892+1895 — 4. VPIS; MATI MENJANA: 1889–1892 Ana Dragoš/Dragos → 1895 Katarina Kambic? [~] — smrt prve žene ali ločitev, mrliška 04894 bi dokazala), h32 + h72 (5. VPIS — NAJDALJŠI zvezi vzorca: Urh × Pegdirec ISTA 5× 1889–1895; Straus × Jakobič ISTA 5×), h69 (oče Janez Brinec ISTI vseh 5× 1888–1895; mati 5. različno branje — Strauš/Straus/Kure/Mure [~] MERI), h30 (3. DRUŽINA v 6 letih — 2× MENJAVA GOSPODINJSTVA: Milek 1890–91 → Jakljevič 1893 → Šegina 1895 — najbolj nestabilna hiša vzorca), h29 (MENJAVA GOSPODINJSTVA — hiša epidemije 1886 Mileh ×3 + »hiša kuge« Milek × Križan 1888+1892 → povsem nova zveza Kuhar?/Kuklar? [~] × Klobučar; epidemija popolnoma prekinjena), h91 (2. VPIS — mati Ana Kure ISTA, oče MENJAN: Novak 1893 → Muc 1895 — ponovna poroka ali napaka branja [~]; stan »mlinar in kovač?«), h46 (2. VPIS ISTA zveza Brodarič × Klobučar — 2. dokaz luknje 41–60), h24 (3. VPIS ISTA zveza Brinec/Brime × Jakobec/Jakobič 1887+1893+1895 + r48 DVOM: forenzika vztraja 24, a dve zvezi na isti hiši v 4 mesecih — alternative 21/27 [~] MERI), h12 (3. VPIS — oče Dragoš ISTI 3×; mati 3. branje Civlkovič?/Druppovič?/Cvitkovič? [~]), h65 (4. VPIS — oče Milek/Mihelt Kurrent varianta [~]; mati Katarina Požek ISTA 2× 1887+1895), h87 (NOVA — Marko Pegdirec bajtar × Marjeta Pegdirec — PEGDIREC PRVIČ STARŠI; podcelica Nikol. Hrižan × Marija Željko — h63 + Željko veriga), h20 (NOVA — Peter Pezdirec? ¼ × Doroteja Šlepec; podcelica Matija Mihelt × Ana? Požek zelo blizu para h65 r43 [~] MERI), h37 (NOVA — ANOMALIJA: isti oče »Peter Pezdirec ¼« kot h20 r40, druga žena! — dva istoimenska moža (oče+sin?) ali napaka [~] MERI); ŽELJKO VERIGA 6 signalov: h1 (1888+1892) + h60 (1893+1894) + h91/h87/h66 podcelice + h25 botra; DUHOVNIKI (TRIJE hkrati — P86: dva): Jan Jelenuš/Jelez? [~] 9 (dominanta) + Jos. Rauq [~] 4 (april–september) + NOV Franc Klunng? [~] 2 (od septembra — Klunnq/Klunng variante); babice: 0 zabeleženih (NOVELA) — Trotter žene 7× kot botra (Marjka/Marjeta); live verifikacija: knjiga HTTP 200 (inventar 326), citirani skeni 5/5 JPEG 200 (78/81 brez Gribljev; 73 podvojen ni citiran); skripta scripts/p90_parish_baptism_1895.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1895",
  "P90: PARISH OF PODZEMELJ — BAPTISM REGISTER 04105, THE FULL YEAR 1895 (issue #18; SAMPLE-TRANSCRIPTION-1895; MEASURES, does not decide; the v7 join unchanged): extending the P79 (1886) → … → P89 (1894) sample to 1895 — the frame: scans 78–84 == printed pages 76–82 (THE P89 NOVEL CONFIRMED FOR THE 2ND YEAR: page == scan − 2 FOR THE WHOLE YEAR; scan 73 duplicated, NOT cited; the »1895.~« heading on p. 76 after the 1894 row 90; 1895 has 73 continuous rows; the 1896 break on p. 83 = scan 85 after row 73 — the labels restart, the P83 novel confirmed for the 8th year); ALL Griblje entries: 15 entries / 14 houses (h24 DOUBTFUL 2× — the first within-year house repeat since P87 NARE): 58, 46, 87, 24 ×2, 12, 30, 20, 65, 32, 37, 69, 72, 91, 29 — 3 NEW houses (20, 37, 87) after the P89 »0 new« + 11 repeats; with P79–P89 the sample totals 185 entries / 68 houses across three books and TEN years; SAMPLE NOVELTIES: ① the midwife column EMPTY on ALL 15 rows (1894: Trotter 11×!) — the Trotter women instead 7× as GODPARENTS — the role shifted from midwife to godparent; ② 4× EMPTY godparents (r53/r54/r55/r66 — a September–December cluster; P89: always recorded); statuses: ½ smallholder 10 + ¼ smallholder 2 + cottager 1 + r18 ¼ [~] — all fractions + 1 cottager (the P85 novel, 6th year); the PT classification 12/2 (46 + 58 in the 41–60 gap — h46 the 2nd proof P88+P90, h58 the 4th entry; no new numbers, the gap remains 15 proven; houses 20/30/37/87/91 all in the PT set); 0 illegitimates in Griblje (2 outside: r31 Primostek + r61 Krasinec); THE MOTHER SUB-CELL (X × Y) explicitly documented for the first time — the semantics of the mother's right sub-cell OPEN (the mother's parents? the father's? mixed) — contents verbatim; ANCHORS: h58 (father Janez Požek [~] THE SAME 3rd year running 1890+1892+1895 — the 4th ENTRY; MOTHER CHANGED: 1889–1892 Ana Dragoš/Dragos → 1895 Katarina Kambic? [~] — death of the first wife or divorce, the death register 04894 would prove it), h32 + h72 (5th ENTRY — THE LONGEST COUPLES of the sample: Urh × Pegdirec THE SAME 5× 1889–1895; Straus × Jakobič THE SAME 5×), h69 (father Janez Brinec THE SAME all 5× 1888–1895; the mother's 5th different reading — Strauš/Straus/Kure/Mure [~]), h30 (the 3rd FAMILY in 6 years — 2× HOUSEHOLD CHANGE: Milek 1890–91 → Jakljevič 1893 → Šegina 1895 — the most unstable house in the sample), h29 (HOUSEHOLD CHANGE — the 1886 epidemic house Mileh ×3 + the »plague house« Milek × Križan 1888+1892 → a brand-new couple Kuhar?/Kuklar? [~] × Klobučar; the epidemic fully broken), h91 (2nd ENTRY — mother Ana Kure THE SAME, father CHANGED: Novak 1893 → Muc 1895 — remarriage or a reading error [~]; occupation »miller and smith?«), h46 (2nd ENTRY THE SAME couple Brodarič × Klobučar — the 2nd proof of the 41–60 gap), h24 (3rd ENTRY THE SAME couple Brinec/Brime × Jakobec/Jakobič 1887+1893+1895 + r48 DOUBTFUL: forensics insist on 24, yet two couples at the same house within 4 months — alternatives 21/27 [~]), h12 (3rd ENTRY — father Dragoš THE SAME 3×; the mother's 3rd reading Civlkovič?/Druppovič?/Cvitkovič? [~]), h65 (4th ENTRY — father Milek/Mihelt a Kurrent variant [~]; mother Katarina Požek THE SAME 2× 1887+1895), h87 (NEW — Marko Pegdirec cottager × Marjeta Pegdirec — PEGDIREC AS PARENTS for the first time; the sub-cell Nikol. Hrižan × Marija Željko — h63 + the Željko chain), h20 (NEW — Peter Pezdirec? ¼ × Doroteja Šlepec; the sub-cell Matija Mihelt × Ana? Požek very close to the h65 r43 pair [~]), h37 (NEW — ANOMALY: the same father »Peter Pezdirec ¼« as h20 r40, another wife! — two namesake men (father+son?) or an error [~]); THE ŽELJKO CHAIN 6 signals: h1 (1888+1892) + h60 (1893+1894) + h91/h87/h66 sub-cells + h25 godparent; PRIESTS (THREE at once — P86: two): Jan Jelenuš/Jelez? [~] 9 (the dominant) + Jos. Rauq [~] 4 (April–September) + NEW Franc Klunng? [~] 2 (from September — Klunnq/Klunng variants); midwives: 0 recorded (NOVEL) — the Trotter women 7× as godparents (Marjka/Marjeta); live verification: the book HTTP 200 (inventory 326), cited scans 5/5 JPEG 200 (78/81 without Griblje; 73 duplicated not cited); the script scripts/p90_parish_baptism_1895.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1895",
  p90Errors.length === 0,
  p90Errors.length === 0
    ? `15 vpisov / 14 hiš (h24 DVOM 2× — prva ponovitev znotraj leta po P87 NARE; 0 neberljivih; 15 zasidranih v vitals) · okvir 1895 skeni 78–84 (stran == sken − 2 ZA CELO LETO — novela P89 potrjena 2. leto; sken 73 podvojen ni citiran; prelom 1896 str. 83; 73 zveznih vrstic) · NOVELI: babica na vseh 15 PRAZNA (Trotter žene 7× kot botra) + 4× prazna botra (sep–dec) · 3 NOVE hiše (20, 37, 87) · PT 12/2 (46 2. dokaz + 58 4. vpis — brez novih) · sidra h58 4. VPIS + MATI MENJANA (Dragoš → Kambic?) / h32 + h72 5. VPIS NAJDALJŠI zvezi / h69 oče ISTI 5× / h30 3. DRUŽINA (2× menjava) / h29 MENJAVA (»hiša kuge«) / h91 oče MENJAN (Novak → Muc) / h46/h24/h12/h65 kontinuitete / h87 + h20 + h37 NOVE (Pegdirec prvič starši; anomalija dveh Petra Pezdirec) · Željko veriga 6 signalov · TRIJE duhovniki (Jelenuš 9× + Rauq 4× + NOV Klunng 2× od sept.) · MATI PODCELICA prvič dokumentirana`
    : p90Errors.join("; "),
);

// ——— qa-p91: p91 krstna 1896 — širitev vzorca na leto 1896 (issue #18;
//      SAMPLE-TRANSCRIPTION-1896; celoven neodvisen preracun iz bundled
//      virov: HOUSE_VITALS × PARISH_BOOKS; PT klasifikacija iz pinov;
//      NOVELA P89 POTRJENA 3. LETO: stran == sken − 2 za celo leto (sken 73
//      podvojen, ni citiran); leto 1896 ima 94 vrstic — NAJDALJŠE doslej;
//      NOVELA babica potrjena 2. leto (14/14 PRAZNO); NOVA LUKNJA ŠTEVILKA
//      45 (16. dokazana); 3 NOVE hiše (9, 14, 45); NARE 3. leto; NOV
//      duhovnik Fr. Šuvar? dominanten; sidra: h1 Željko × Kure 3. VPIS ISTA
//      zveza (botra ISTI priimki kot starši), h63 oče ISTI 5×, h30 ISTA
//      zveza 2. leto, h41 4. VPIS ISTA zveze, h15 3. VPIS, h36 2. VPIS,
//      h53 3. VPIS variante, h31 MENJAVA, h25 KLEPEC NAZAJ, h26 ISTI
//      priimki na drugi hiši (75 → 26), h14 neimenovan otrok; paleografska
//      faza v research/issue17/parish-baptism-1896.json, live verifikator
//      scripts/p91_parish_baptism_1896.py --check I1–I10) ———
const p91Hv = HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year === 1896);
const p91Errors: string[] = [];
const P91_PT_IN_SET = ["1", "9", "14", "15", "25", "26", "30", "31", "36", "63"];
const P91_PT_GAP = ["41", "45", "46", "53"];
if (p91Hv.length !== 14)
  p91Errors.push(`vpisov 1896 (04105, zasidrani) ≠ 14 (${p91Hv.length})`);
const p91Houses = new Set(p91Hv.map((h) => h.houseNo));
if (p91Houses.size !== 14)
  p91Errors.push(`različnih hiš ≠ 14 (${p91Houses.size}: ${[...p91Houses].sort((a, b) => Number(a) - Number(b)).join(",")})`);
// okvir 1896: skeni 85–92; stran == sken − 2 za celo leto (novela P89, 3. leto)
const p91Bad = p91Hv.filter(
  (h) => h.status !== "DOCUMENTED" || !h.scan || !h.page
    || h.page !== h.scan - 2
    || h.scan < 85 || h.scan > 92,
);
if (p91Bad.length > 0)
  p91Errors.push(`okvir 1896: skeni 85–92 ali stran ≠ sken − 2 krščeno pri ${p91Bad.length}`);
// NOVELA babica: vsi 14 blokov PRAZNI stolpec babice (2. leto)
const p91Babica = p91Hv.filter((h) => h.whatSi.includes("babica PRAZNA") || h.whatSi.includes("babica PRAZNA?"));
if (p91Babica.length !== 14)
  p91Errors.push(`NOVELA babica: praznih ≠ 14 (${p91Babica.length})`);
// NOVA LUKNJA ŠTEVILKA 45: blok h45 mora imeti pin NOVA LUKNJA
const p91H45 = p91Hv.find((h) => h.houseNo === "45");
if (!p91H45 || !p91H45.whatSi.includes("NOVA LUKNJA ŠTEVILKA"))
  p91Errors.push("NOVA LUKNJA 45: whatSi ≠ P91 (pin NOVA LUKNJA ŠTEVILKA manjka)");
// sidra (14 vpisov)
const p91Anchor = (hn: string, scan: number, pins: string[], label: string) => {
  const blk = p91Hv.find((h) => h.houseNo === hn && h.scan === scan);
  if (!blk || !pins.every((p) => blk.whatSi.includes(p)))
    p91Errors.push(`sidro ${label}: whatSi ≠ P91 (${pins.join(" + ")})`);
};
p91Anchor("9", 85, ["Jakobič", "NOVA HIŠA"], "hiša 9");
p91Anchor("14", 85, ["Brinec", "NOVA HIŠA"], "hiša 14");
p91Anchor("31", 86, ["Pendirec", "MENJAVA GOSPODINJSTVA"], "hiša 31");
p91Anchor("36", 86, ["Križan", "ISTA ZVEZA"], "hiša 36");
p91Anchor("1", 87, ["Željko", "3. VPIS ISTA ZVEZA"], "hiša 1");
p91Anchor("25", 87, ["Klepec", "KLEPEC NAZAJ"], "hiša 25");
p91Anchor("46", 87, ["Brodarič", "3. DOKAZ LUKNJE"], "hiša 46");
p91Anchor("26", 88, ["Jakobič", "DRUGI hiši"], "hiša 26");
p91Anchor("41", 88, ["Hušič", "4. VPIS ISTA ZVEZA"], "hiša 41");
p91Anchor("15", 89, ["Jaklič", "3. VPIS ISTA ZVEZA"], "hiša 15");
p91Anchor("63", 89, ["Hrižan", "OČE ISTI VSEH 5×"], "hiša 63");
p91Anchor("45", 90, ["Straus", "NOVA LUKNJA ŠTEVILKA"], "hiša 45");
p91Anchor("53", 91, ["Pendirec", "3. DOKAZ LUKNJE"], "hiša 53");
p91Anchor("30", 92, ["Šegina", "ISTA ZVEZA 2. leto"], "hiša 30");
// PT klasifikacija == pin: 10 v naboru + 4 v luknji (45 NOVA — 16. dokazana;
// 41 4. dokaz; 46 3. dokaz; 53 3. dokaz)
const p91InSet = [...p91Houses].filter((h) => P91_PT_IN_SET.includes(h));
const p91Gap = [...p91Houses].filter((h) => P91_PT_GAP.includes(h));
if (p91InSet.length !== 10 || p91Gap.length !== 4)
  p91Errors.push(`PT klasifikacija ≠ 10/4 (${p91InSet.length}/${p91Gap.length})`);
if (p91Gap.some((h) => !(Number(h) >= 41 && Number(h) <= 60)))
  p91Errors.push("luknjane hiše izven 41–60");
// NOVE hiše 1896 (9, 14, 45) — ne obstajajo v nobenem prejšnjem letu/knjigi
// h45: P92 dovoli blok 1897 (2. VPIS ISTA ZVEZA Straus × Spudič — POPRAVEK matere);
// h9/h14/h45: P95 kontinuiteta dovoli bloke 1900 (menjava h9; 2. VPIS h14 — REŠUJE P91; 3. PIN h45 — 04455);
// h9: P123 dovoli poročni blok 04455/1894 (v11 Georg Jakobčič GRIBLJE 9 — 2. poročni dokaz h9)
for (const hn of ["9", "14", "45"]) {
  const allow = hn === "45" ? [1896, 1897, 1900, 1904, 1912, 1915, 1917, 1918] : hn === "14" ? [1896, 1900, 1902, 1908, 1911, 1914, 1917, 1918] : hn === "18" ? [1896, 1900, 1910, 1912] : [1896, 1900, 1913, 1915, 1917]; // P113: + 1918 bloka h45 (8. VPIS — ZAPORED 2. LETO!) + h14 (9. VPIS — ZAPORED 2. LETO!) // P105: + 1910 blok h18 (4. VPIS — POVRAT Šimec × Kambič); P106: + 1911 blok h48 (5. VPIS) // P95: + 1900 bloki; P97: + 1902 blok h14 (3. VPIS — oče potrjen); P99: + 1904 blok h45 (4. VPIS — SPUDIČ signal, mati Barbara Spudič) P107: + 1912 blok h45 (5. VPIS — DVOJČKI r6/r7) P107: + 1912 blok h18 (5. VPIS — ANOMALIJA žensko ime v koloni očeta) P108: + 1913 blok h9 (3. VPIS — VRZEL 13 LET!); P109: + 1914 blok h14 (6. VPIS — VRZEL 3 LETA POPRAVLJENO); P112: + 1917 bloka h45 (7. VPIS — P111 lead Karol Feliks!) + h14 (7. VPIS — MRTVOROJEN!) + h9 (5. VPIS — Ožbald oče!); P113: + 1918 bloka h45 (8. VPIS — ZAPORED 2. LETO, ČEVLJAR 2. leto!) + h14 (9. VPIS — ZAPORED 2. LETO!)
  if (HOUSE_VITALS.some((v) => v.houseNo === hn && !(v.bookSignature === "04105" && allow.includes(v.year)) && !(v.bookSignature === "04455" && v.year === 1894) && !(v.bookSignature === "04455" && v.year === 1911) && !(v.bookSignature === "04455" && hn === "14" && v.year === 1895) && !(v.bookSignature === "04455" && hn === "14" && v.year === 1908) && !(v.bookSignature === "04455" && v.year === 1903 && hn === "9"))) // P123: + poročni blok h9-1894 (v11 Georg Jakobčič — 2. poročni dokaz h9!); P132: + poročni blok h9-1903 (v12 nevesta Jakofčič — 3. poročni dokaz h9, DRUBEL!); P137: + 2 poročna bloka h14-1908 (v17 — 2. poročni dokaz h14 ×2 = ★★ 1. INTRA-HIŠNA POROKA linije!)
    p91Errors.push(`NOVA hiša ${hn} (P91) že obstaja v prejšnjem letu — pini neskladni`);
}
// kontinuitete čez leta prek HOUSE_VITALS
for (const [hn, yr, sig, pin] of [
  ["1", 1888, "04105", "Zeljth"], ["1", 1892, "04105", "Željko"],
  ["30", 1890, "04105", "Milek"], ["30", 1891, "04105", "Milek"], ["30", 1893, "04105", "Jakljevič"], ["30", 1895, "04105", "Šegina"],
  ["36", 1886, "04105", "Križan"], ["36", 1894, "04105", "Križan"],
  ["41", 1890, "04105", "Hrušič"], ["41", 1893, "04105", "Hušič"],
  ["46", 1893, "04105", "Brodarič"], ["46", 1895, "04105", "Brodarič"],
  ["53", 1891, "04105", "Pozdirec"], ["53", 1894, "04105", "Pegdirec"],
  ["63", 1887, "04105", "Prižan"], ["63", 1890, "04105", "Križan"], ["63", 1892, "04105", "Hrižan"],
  ["15", 1887, "04105", "Brinec"], ["15", 1893, "04105", "Jaklič"],
  ["31", 1894, "04105", "Fapič"],
  ["25", 1893, "04105", "Hrižan"], ["25", 1886, "04455", "Klepec"],
  ["75", 1892, "04105", "Jakobčič"], ["75", 1894, "04105", "Jakobič"], // Kurrent variante
  ["69", 1895, "04105", "Brinec"],
] as const) {
  const blk = HOUSE_VITALS.find((v) => v.houseNo === hn && v.bookSignature === sig && v.year === yr);
  const anyBlk = HOUSE_VITALS.some((v) => v.houseNo === hn && v.bookSignature === sig && v.year === yr && v.whatSi.includes(pin));
  if (!blk || !anyBlk)
    p91Errors.push(`kontinuiteta hiša ${hn} (${yr}, ${sig}, pin ${pin}) manjka ali pin ne ustreza`);
}
// vitals skupaj 449 (po P106: 429 + 20; krstna 1911)
if (HOUSE_VITALS.length !== 685)
  p91Errors.push(`HOUSE_VITALS ≠ 467 (${HOUSE_VITALS.length})`);
push(
  "qa-p91-parish-baptism-1896",
  "P91: ŽUPNIJA PODZEMELJ — KRSTNA KNJIGA 04105, POLNO LETO 1896 (issue #18; SAMPLE-TRANSCRIPTION-1896; MERI, NE odloča; v7 join nespremenjen): širitev vzorca P79 (1886) → … → P90 (1895) na leto 1896 — okvir: skeni 85–92 == tiskane strani 83–90 (NOVELA P89 POTRJENA 3. LETO: stran == sken − 2 ZA CELO LETO; sken 73 podvojen, NI citiran; glava »1896« na str. 83 po 1895 row 73; leto 1896 ima 94 zveznih vrstic — NAJDALJŠE doslej (1894: 90); prelom 1897 na str. 91 = sken 93 po row 94 — oznake se ponastavijo na 1, novela P83 potrjena 9. leto) — VSI vpisi z Griblji: 14 vpisov / 14 hiš — NARE (3. leto po P87 1892/P89 1894): 9, 14, 31, 36, 1, 25, 46, 26, 41, 15, 63, 45, 53, 30 — 3 NOVE hiše (9, 14, 45) + 11 ponovitev; skupaj s P79–P90 vzorec 199 vpisov / 71 hiš čez tri knjige in ENAJST LET; NOVA LUKNJA ŠTEVILKA: h45 (16. dokazana v 41–60 — prva nova od P88; PT_GAP_KNOWN dobi +45) + h41 4. dokaz + h46 3. dokaz + h53 3. dokaz — luknja zdaj 16 dokazanih; NOVELA babica POTRJENA 2. LETO: 14/14 PRAZNO (1895: 15; 1894: Trotter 11×) — Trotter žene 1896 0× (tudi kot botra izginejo); statusi: ½ zemljak 12 + bajtar 2 (r13 Pendirec + r70 Straus) — PRVO leto brez ¼ zemljaka (novela P85, 7. leto); DUHOVNIKI: NOV Fr. Šuvar? [~] 9 (dominanta, Januar–Junij) + Jos. Rauq [~] 4 (Feb/Sep/Okt/Dec — izmenjava NI čista) + r5 brez podpisa (3. primer po P86 r39/P87 r70) — P90 trojica se krči (Klunng in Jelenuš izginejo); 0 nezakonskih; KURRENT FORENZIKA: r25 »26« → jasno 25 (referenčna primerjava Gradac 25), r31 »16« → jasno 46, r92 »25« → jasno 30 (starša Šegina × Mihelt = h30 1895 to potrdita), r13 »37?« → jasno 31 — štirje popravki z 5x–10x izrezi; MATI PODCELICA (X × Y) izgine (po prvi dokumentaciji P90); DOJENČIJSKA UMRLJIVOST: † r2 (3/3. 96), r31 (29/3. 97?), r53 (19.96?) + r5 krsta PRAZNA (umrl pred krstom?); SIDRA: h1 (Nikolaj Željko [~] ½ × Katarina Kure — 3. VPIS ISTA ZVEZA: 1888+1892+1896 — 8 let, 2. najdaljša zveza; botra ISTI priimki kot starši vse 3× — začarani krog familije; ŽELJKO VERIGA 8 signalov: h1 ×3 + h60 ×2 + podcelice h91/h87/h66 + botra h25/h46 NOVO), h63 (Nikolaj Hrižan? — OČE ISTI VSEH 5× 1887–1896 — najbolj konstanten oče; Prižan/Hrigian/Križan/Hrižan variante istega podpisa), h30 (Šegina? × Mihelt? — ISTA ZVEZA 2. leto: 1895+1896 — 3. DRUŽINA se je UNESELILA po 2 menjavah), h41 (Hušič? × Jakobič? — 4. VPIS ISTA ZVEZE: 1890×2+1893+1896 — najbolj stabilna na luknji), h15 (Jaklič? × Brinec — 3. VPIS ISTA ZVEZA: 1887+1893+1896; J/Š variante), h36 (Janez Križan? × Straucelj? — 2. VPIS: 1894+1896; tri-virska hiša dobi 5. in 6. vir; KRIŽAN 2. GENERACIJA), h53 (Janez Pendirec? × Marija Hrižan — 3. VPIS VARIANTE: 1891+1894+1896 — Kurrent P/K + K/H variante istih dveh familij), h46 (Anton Brodarič 3. VPIS + MATI MENJANA/varianta: Klobučar/Klobučan → Kramarič? [~]; botra Nikolaj Željko = Željko veriga), h31 (MENJAVA GOSPODINJSTVA: Fapič × Straus 1894 → Marko Pendirec? bajtar × Žugelj? — 2. menjava na h31), h25 (KLEPEC NAZAJ: poroka 04455 1886 Klepec h25 + 1893 Hrižan × Požek menjava → 1896 vrnitev [~]), h26 (ANOMALIJA: Janez Jakobič? × Marija Stubljar? = ISTI priimki kot h75 zveza 1892+1894 — 3. vpis zveze na DRUGI hiši (75 → 26: selitev ali napaka [~] MERI; forenzika 10x vztraja 26)), h9/h14 NOVE (h14: neimenovan otrok »N. moškega spola« + krsta PRAZNA + brez botre/podpisa — najbolj fragmentaren vpis; oče Brinec = h69 familija? [~]), h45 NOVA (Martin Straus? bajtar × Barbara Doroteja? [~]; botra POD TRAKOM [?]; Straus signal 3. hiša h71/h72/h45; ime Martin — prvi prebir Marija [~]); live verifikacija: knjiga HTTP 200 (inventar 326), citirani skeni 8/8 JPEG 200 (sken 73 podvojen ni citiran); skripta scripts/p91_parish_baptism_1896.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1896",
  "P91: PARISH OF PODZEMELJ — BAPTISM REGISTER 04105, THE FULL YEAR 1896 (issue #18; SAMPLE-TRANSCRIPTION-1896; MEASURES, does not decide; the v7 join unchanged): extending the P79 (1886) → … → P90 (1895) sample to 1896 — the frame: scans 85–92 == printed pages 83–90 (THE P89 NOVEL CONFIRMED FOR THE 3RD YEAR: page == scan − 2 FOR THE WHOLE YEAR; scan 73 duplicated, NOT cited; the »1896« heading on p. 83 after the 1895 row 73; 1896 has 94 continuous rows — THE LONGEST so far (1894: 90); the 1897 break on p. 91 = scan 93 after row 94 — the labels restart, the P83 novel confirmed for the 9th year); ALL Griblje entries: 14 entries / 14 houses — SQUARE (the 3rd year after P87 1892/P89 1894): 9, 14, 31, 36, 1, 25, 46, 26, 41, 15, 63, 45, 53, 30 — 3 NEW houses (9, 14, 45) + 11 repeats; with P79–P90 the sample totals 199 entries / 71 houses across three books and ELEVEN years; A NEW GAP NUMBER: h45 (the 16th proven in 41–60 — the first new one since P88; PT_GAP_KNOWN gains +45) + h41 the 4th proof + h46 the 3rd proof + h53 the 3rd proof — the gap now has 16 proven; THE MIDWIFE NOVEL CONFIRMED FOR THE 2ND YEAR: 14/14 EMPTY (1895: 15; 1894: Trotter 11×) — the Trotter women 0× in 1896 (they disappear as godparents too); statuses: ½ smallholder 12 + cottager 2 (r13 Pendirec + r70 Straus) — THE FIRST YEAR WITHOUT ¼ smallholder (the P85 novel, 7th year); PRIESTS: NEW Fr. Šuvar? [~] 9 (the dominant, Jan–Jun) + Jos. Rauq [~] 4 (Feb/Sep/Oct/Dec — the alternation is NOT clean) + r5 without a signature (the 3rd case after P86 r39/P87 r70) — the P90 trio shrinks (Klunng and Jelenuš disappear); 0 illegitimates; KURRENT FORENSICS: r25 »26« → clearly 25 (a reference comparison with Gradac 25), r31 »16« → clearly 46, r92 »25« → clearly 30 (the parents Šegina × Mihelt = h30 1895 confirm it), r13 »37?« → clearly 31 — four corrections with 5x–10x crops; THE MOTHER SUB-CELL (X × Y) disappears (after the first documentation in P90); INFANT MORTALITY: † r2 (Mar 3, 96), r31 (Mar 29, 97?), r53 (1896?) + r5 the baptism EMPTY (died before baptism?); ANCHORS: h1 (Nikolaj Željko [~] ½ × Katarina Kure — the 3rd ENTRY THE SAME COUPLE: 1888+1892+1896 — 8 years, the 2nd longest couple; godparents THE SAME SURNAMES AS THE PARENTS all 3× — the family's closed circle; THE ŽELJKO CHAIN 8 signals: h1 ×3 + h60 ×2 + the sub-cells h91/h87/h66 + godparents h25/h46 NEW), h63 (Nikolaj Hrižan? — THE FATHER THE SAME ALL 5× 1887–1896 — the most constant father; Prižan/Hrigian/Križan/Hrižan variants of the same signature), h30 (Šegina? × Mihelt? — THE SAME COUPLE 2nd year: 1895+1896 — the 3rd FAMILY has SETTLED after 2 changes), h41 (Hušič? × Jakobič? — the 4th ENTRY THE SAME COUPLE: 1890×2+1893+1896 — the most stable on the gap), h15 (Jaklič? × Brinec — the 3rd ENTRY THE SAME COUPLE: 1887+1893+1896; J/Š variants), h36 (Janez Križan? × Straucelj? — the 2nd ENTRY: 1894+1896; the three-source house gains its 5th and 6th sources; KRIŽAN 2nd GENERATION), h53 (Janez Pendirec? × Marija Hrižan — the 3rd ENTRY IN VARIANTS: 1891+1894+1896 — Kurrent P/K + K/H variants of the same two families), h46 (Anton Brodarič the 3rd ENTRY + MOTHER CHANGED/a variant: Klobučar/Klobučan → Kramarič? [~]; godparent Nikolaj Željko = the Željko chain), h31 (HOUSEHOLD CHANGE: Fapič × Straus 1894 → Marko Pendirec? cottager × Žugelj? — the 2nd change on h31), h25 (KLEPEC BACK: the 1886 marriage Klepec h25 + the 1893 Hrižan × Požek change → the 1896 return [~]), h26 (ANOMALY: Janez Jakobič? × Marija Stubljar? = THE SAME surnames as the h75 couple 1892+1894 — the 3rd entry of the couple on ANOTHER house (75 → 26: a move or an error [~]; 10x forensics insist on 26)), h9/h14 NEW (h14: an unnamed child »N. male sex« + the baptism EMPTY + no godparents/signature — the most fragmentary entry; father Brinec = the h69 family? [~]), h45 NEW (Martin Straus? cottager × Barbara Doroteja? [~]; godparents UNDER THE TAPE [?]; the Straus signal on a 3rd house h71/h72/h45; the name Martin — first read Marija [~]); live verification: the book HTTP 200 (inventory 326), cited scans 8/8 JPEG 200 (scan 73 duplicated not cited); the script scripts/p91_parish_baptism_1896.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1896",
  p91Errors.length === 0,
  p91Errors.length === 0
    ? `14 vpisov / 14 hiš — NARE (3. leto; 0 neberljivih; 14 zasidranih v vitals) · okvir 1896 skeni 85–92 (stran == sken − 2 — novela P89 potrjena 3. leto; sken 73 podvojen ni citiran; prelom 1897 str. 91; 94 zveznih vrstic — NAJDALJŠE doslej) · NOVA LUKNJA ŠTEVILKA 45 (16. dokazana — prva nova od P88; 41 4. dokaz + 46 3. dokaz + 53 3. dokaz) · NOVELA babica 2. leto (14/14 PRAZNO; Trotter 0×) · 3 NOVE hiše (9, 14, 45) · statusi ½ 12 + bajtar 2 (prvo leto brez ¼) · NOV duhovnik Fr. Šuvar? 9× (Rauq 4×; r5 brez podpisa) · KURRENT: 4 popravki (25/26, 46/16, 30/25, 31/37) · sidra h1 Željko × Kure 3. VPIS (botra = starši priimki!) / h63 oče ISTI 5× / h30 ISTA zveza 2. leto / h41 4. VPIS / h15 3. VPIS / h36 2. VPIS / h53 3. VPIS variante / h31 MENJAVA / h25 KLEPEC NAZAJ / h46 mati menjana / h26 ISTI priimki na drugi hiši (75→26) / h14 neimenovan otrok / h45 Straus 3. hiša · Željko veriga 8 signalov`
    : p91Errors.join("; "),
);
// ——— qa-p92: p92 krstna 1897 — širitev vzorca na leto 1897 (issue #18;
//      SAMPLE-TRANSCRIPTION-1897; celoven neodvisen preracun iz bundled
//      virov: HOUSE_VITALS × PARISH_BOOKS; PT klasifikacija iz pinov;
//      NOVELA P92: sken 97 = PODVOJEN (duplikat s96 = str. 94; 2. znani
//      duplikat po skenu 73) — novela P89 (stran == sken − 2) velja samo do
//      skena 96, od skena 98 stran == sken − 3 (artefakt duplikata); leto
//      1897 ima 85 vrstic; prelom 1898 na str. 98 row 86; 19 vpisov / 18
//      hiš — NARE 4. leto; h31 2 vpisa v enem letu (Straus kompleks); 3 NOVE
//      hiše (10, 40, 43); NOVA LUKNJA ŠTEVILKA 43 (17. dokazana); h61 sidro
//      ZDRUŽENO s P79-era placeholderjem (čez-fazna potrditev — P79 je
//      opazil Anton »Miha P.—«, P92 dopolni Janez Muc bajtar × Ana Kure);
//      PRVI NEZAKONSKI vpis od P90 (r31 sama mati Pozdirec); NOVELA babica
//      3. leto (19/19 PRAZNO); dojenčijska umrljivost 7/19 — najvišje;
//      duhovniki Klun 11× + Rauq 8× (Šuvar izgine); paleografska faza v
//      research/issue17/parish-baptism-1897.json, live verifikator
//      scripts/p92_parish_baptism_1897.py --check I1–I10) ———
const p92Hv = HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year === 1897);
const p92Errors: string[] = [];
const P92_PT_IN_SET = ["2", "10", "12", "16", "20", "23", "24", "31", "32", "37", "40", "61", "65"];
const P92_PT_GAP = ["43", "45", "46", "54", "60"];
if (p92Hv.length !== 19)
  p92Errors.push(`vpisov 1897 (04105, zasidrani) ≠ 19 (${p92Hv.length})`);
const p92Houses = new Set(p92Hv.map((h) => h.houseNo));
if (p92Houses.size !== 18)
  p92Errors.push(`različnih hiš ≠ 18 (${p92Houses.size}: ${[...p92Houses].sort((a, b) => Number(a) - Number(b)).join(",")})`);
// okvir 1897: skeni 93–101; stran == sken − 2 (≤ 96) / sken − 3 (≥ 98);
// sken 97 podvojen, ni citiran
const p92PageOf = (s: number) => (s <= 96 ? s - 2 : s - 3);
const p92Bad = p92Hv.filter(
  (h) => h.status !== "DOCUMENTED" || !h.scan || !h.page
    || h.page !== p92PageOf(h.scan)
    || h.scan < 93 || h.scan > 101,
);
if (p92Bad.length > 0)
  p92Errors.push(`okvir 1897: skeni 93–101 ali stran ≠ sken − 2/− 3 krščeno pri ${p92Bad.length}`);
// NOVELA babica: vsi 19 blokov PRAZNI stolpec babice (3. leto)
const p92Babica = p92Hv.filter((h) => h.whatSi.includes("babica PRAZNA") || h.whatSi.includes("babica PRAZNA?"));
if (p92Babica.length !== 19)
  p92Errors.push(`NOVELA babica: praznih ≠ 19 (${p92Babica.length})`);
// NOVA LUKNJA ŠTEVILKA 43: blok h43 mora imeti pin NOVA LUKNJA + NEZAKONSKI
const p92H43 = p92Hv.find((h) => h.houseNo === "43");
if (!p92H43 || !p92H43.whatSi.includes("NOVA LUKNJA ŠTEVILKA") || !p92H43.whatSi.includes("NEZAKONSKI"))
  p92Errors.push("NOVA LUKNJA 43 / NEZAKONSKI: whatSi ≠ P92 (pin manjka)");
// sidra (19 vpisov)
const p92Anchor = (hn: string, scan: number, pins: string[], label: string) => {
  const blk = p92Hv.find((h) => h.houseNo === hn && h.scan === scan);
  if (!blk || !pins.every((p) => blk.whatSi.includes(p)))
    p92Errors.push(`sidro ${label}: whatSi ≠ P92 (${pins.join(" + ")})`);
};
p92Anchor("12", 93, ["Dragar", "jasno 12"], "hiša 12");
p92Anchor("32", 94, ["Perdune", "jasno 32"], "hiša 32");
p92Anchor("10", 94, ["Brinec", "NOVA HIŠA"], "hiša 10");
p92Anchor("24", 94, ["Brinec", "DVE RAZLIČNI Brinec hiši"], "hiša 24");
p92Anchor("37", 95, ["Pendirec", "ŽELJKO VERIGA"], "hiša 37");
p92Anchor("54", 95, ["Brinec", "2. DOKAZ LUKNJE"], "hiša 54");
p92Anchor("60", 95, ["Željko", "4. DOKAZ"], "hiša 60");
p92Anchor("2", 95, ["Vhebec", "DRUGA vas"], "hiša 2");
p92Anchor("43", 95, ["SAMA MATI", "NOVA LUKNJA ŠTEVILKA"], "hiša 43");
p92Anchor("23", 96, ["Brinec", "DVE RAZLIČNI Brinec hiši"], "hiša 23");
p92Anchor("46", 96, ["Brodarič", "3. VARIANTA MATERE"], "hiša 46");
p92Anchor("31", 98, ["Sapič", "STRAUS KOMPLEKS"], "hiša 31 vpis 1");
p92Anchor("16", 98, ["Jaklič", "PRVI PREBIR »10« NAPAČEN"], "hiša 16");
p92Anchor("40", 99, ["Berkovec", "NOVA HIŠA"], "hiša 40");
p92Anchor("20", 99, ["Pendirec", "jasno 20"], "hiša 20");
p92Anchor("31", 99, ["Straus", "2. VPIS NA h31 V ENEM LETU"], "hiša 31 vpis 2");
p92Anchor("61", 100, ["Muc", "h1 PAR KOT BOTRA"], "hiša 61 (združen)");
p92Anchor("65", 100, ["Mihek", "jasno 65"], "hiša 65");
p92Anchor("45", 101, ["Straus", "2. VPIS ISTA ZVEZA", "Spudič"], "hiša 45");
// PT klasifikacija == pin: 13 v naboru + 5 v luknji (43 NOVA — 17. dokazana;
// 45 2. dokaz; 46 4. dokaz; 54 2. dokaz; 60 4. dokaz)
const p92InSet = [...p92Houses].filter((h) => P92_PT_IN_SET.includes(h));
const p92Gap = [...p92Houses].filter((h) => P92_PT_GAP.includes(h));
if (p92InSet.length !== 13 || p92Gap.length !== 5)
  p92Errors.push(`PT klasifikacija ≠ 13/5 (${p92InSet.length}/${p92Gap.length})`);
if (p92Gap.some((h) => !(Number(h) >= 41 && Number(h) <= 60)))
  p92Errors.push("luknjane hiše izven 41–60");
// NOVE hiše 1897 (10, 40, 43) — ne obstajajo v nobenem prejšnjem letu/knjigi;
// P116: h10 ima ZDAJ poročni blok 04455/1887 (nevesta Catharina Križe, GRIBLJE 10 — faza-1
// »19« popravljen) = prva pojavitev hiše je 1887 poročna; NOVA ostaja v okviru KRSTNEGA vzorca;
// h40: P93 kontinuiteta dovoli tudi blok 1898 (MENJAVA — Berkopne selitev h40→h48, Brodarič nazaj);
// h10: P95 kontinuiteta dovoli blok 1900 (MENJAVA Grabrijan × Pozdirec)
for (const hn of ["10", "40", "43"]) {
  const allow = hn === "40" ? [1897, 1898, 1899, 1911, 1912, 1915, 1919] : hn === "10" ? [1897, 1900, 1907, 1908, 1909] : [1897, 1904]; // P94: + 1899 blok h40 (TRETJA DRUŽINA Straus × Spudič); P95: + 1900 blok h10; P99: + 1904 blok h43 (2. VPIS — oče Jurij Perdinec, KURRENT nezakonski Pozdirec → Perdinec); P102: + 1907 bloka h10 ×2 (3. VPIS — BRINEC POVRAT, dvojčka; NARE PRELOM); P103: + 1908 blok h10 (4. VPIS — BRINEC ISTA, mati menjava Kure); P104: + 1909 blok h10 (6. VPIS — SELITEV h30→h10, Matija Brinec) P107: + 1912 blok h40 (5. VPIS — November glava pod trakom); P114: + 1919 blok h40 (7. VPIS — BRINC mreža h88+h40!)
  if (HOUSE_VITALS.some((v) => v.houseNo === hn && !(v.bookSignature === "04105" && allow.includes(v.year)) && !(v.bookSignature === "04455" && v.year === 1887) && !(v.bookSignature === "04455" && v.year === 1889 && hn === "40") && !(v.bookSignature === "04455" && v.year === 1890 && hn === "10") && !(v.bookSignature === "04455" && v.year === 1897 && hn === "40") && !(v.bookSignature === "04455" && v.year === 1899 && hn === "10") && !(v.bookSignature === "04455" && v.year === 1905 && hn === "10") && !(v.bookSignature === "04455" && v.year === 1908 && hn === "43"))) // P118: + poročni blok h40-1889 (1. poročni dokaz!); P119: + poročni blok h10-1890 (2. poročni dokaz — Anna Kure × Johann Muc!); P126: + 2 poročna bloka h40-1897 (v9 Brodarič + v11 Predanic — A6!); P128: + poročni blok h10-1899 (v3 nevesta Barbara Kure — 3. poročni dokaz, KURE SESTRI!); P134: + poročni blok h10-1905 (v14 ženin Joseph PERDINEC — 4. poročni dokaz h10, DRUBEL — menjava KURE→PERDINEC!); P137: + poročni blok h43-1908 (v9 nevesta Maria Lasič [~] — 1. poročni dokaz NOVE poročne hiše!)
    p92Errors.push(`NOVA hiša ${hn} (P92) že obstaja v prejšnjem letu — pini neskladni`);
}
// kontinuitete čez leta prek HOUSE_VITALS
// oblika: [hiša, leto, knjiga, whatSi-pin ALI "" za scan-pin, pričakovani sken]
for (const [hn, yr, sig, pin, sc] of [
  ["45", 1896, "04105", "Straus", null], ["45", 1897, "04105", "Spudič", null],
  ["46", 1893, "04105", "Brodarič", null], ["46", 1895, "04105", "Brodarič", null], ["46", 1896, "04105", "Brodarič", null],
  ["31", 1894, "04105", "Straus", null], ["31", 1896, "04105", "Pendirec", null],
  ["31", 1897, "04105", "Sapič", null], ["31", 1897, "04105", "Straus", null],
  ["60", 1893, "04105", "", 63], ["60", 1894, "04105", "", 78], ["60", 1897, "04105", "Željko", null],
  ["2", 1887, "04105", "", 25], ["2", 1889, "04105", "", 40], ["2", 1891, "04105", "", 53], ["2", 1894, "04105", "", 71],
  ["12", 1892, "04105", "", 57], ["12", 1894, "04105", "", 70], ["12", 1895, "04105", "", 80],
  ["24", 1892, "04105", "", 62], ["24", 1895, "04105", "", 80],
  ["32", 1889, "04105", "", 39], ["32", 1892, "04105", "", 60],
  ["61", 1887, "04105", "", 20], ["61", 1891, "04105", "", 52], ["61", 1892, "04105", "", 61],
  ["65", 1887, "04105", "", 25], ["65", 1893, "04105", "", 64], ["65", 1895, "04105", "", 82],
  ["16", 1886, "04105", "", 4],
  ["20", 1895, "04105", "", 82],
  ["23", 1893, "04105", "", 65], ["23", 1894, "04105", "", 78],
  ["37", 1895, "04105", "", 82],
  ["54", 1886, "04105", "", 2],
] as const) {
  const blk = HOUSE_VITALS.find((v) => v.houseNo === hn && v.bookSignature === sig && v.year === yr);
  const ok = blk && (pin === "" ? blk.scan === sc : HOUSE_VITALS.some((v) => v.houseNo === hn && v.bookSignature === sig && v.year === yr && v.whatSi.includes(pin)));
  if (!ok)
    p92Errors.push(`kontinuiteta hiša ${hn} (${yr}, ${sig}, pin ${pin || `sk ${sc}`}) manjka ali pin ne ustreza`);
}
// vitals skupaj 449 (po P106: 429 + 20; krstna 1911)
if (HOUSE_VITALS.length !== 685)
  p92Errors.push(`HOUSE_VITALS ≠ 467 (${HOUSE_VITALS.length})`);
push(
  "qa-p92-parish-baptism-1897",
  "P92: ŽUPNIJA PODZEMELJ — KRSTNA KNJIGA 04105, POLNO LETO 1897 (issue #18; SAMPLE-TRANSCRIPTION-1897; MERI, NE odloča; v7 join nespremenjen): širitev vzorca P79 (1886) → … → P90 (1895) → P91 (1896) na leto 1897 — okvir: skeni 93–101 == tiskane strani 91–98 (NOVELA P92: SKEN 97 = PODVOJEN — duplikat s96 = str. 94, 2. znani duplikat po skenu 73; NOVELA P89 (stran == sken − 2) velja samo do skena 96, od skena 98 stran == sken − 3 — premik offseta je ARTEFAKT DUPLIKATA, ne nova številčenja; glava »Leto 1897« na str. 91 po 1896 row 94; leto 1897 ima 85 vrstic; prelom 1898 na str. 98 = sken 101 row 86 — oznake ponastavljene, novela P83 potrjena 10. leto) — VSI vpisi z Griblji: 19 vpisov / 18 hiš — NARE (4. leto po P87 1892/P89 1894/P91 1896): 12, 32, 10, 24, 37, 54, 60, 2, 43, 23, 46, 31, 16, 40, 20, 31, 61, 65, 45 — h31 2 VPISA V ENEM LETU (r51 Sapič? × Straus + r64 Straus? × Jakobič — STRAUS KOMPLEKS: 1894 Fapič?×Straus → 1896 Pendirec?×Žugelj menjava → 1897 obe nazaj!); 3 NOVE hiše (10, 40, 43) + 15 ponovitev; kumulativ 217 vpisov / 74 hiš čez tri knjige in DVANAEST LET (h61 sidro ZDRUŽENO s P79-era placeholderjem — ČEZ-FAZNA POTRDITEV: izvirna prepis hiše 61 je opazil »Anton, oče Miha P.—« pri strani 49 po stari predpostavki, P92 5x forenzika dopolni: Janez Muc bajtar × Ana Kure, stran 97 po noveli); NOVA LUKNJA ŠTEVILKA: h43 (17. dokazana v 41–60 — PT_GAP_KNOWN dobi +43) + h54 2. dokaz + h60 4. dokaz + h45/h46 luknji — luknja zdaj 17 dokazanih; PRVI NEZAKONSKI VPIS OD P90: r31 Florijan — OČE PRAZEN, mati Katarina Pozdirec SAMA MATI ¼ zemljatva (novela P85 ulomek, 8. leto); NOVELA babica POTRJENA 3. LETO: 19/19 PRAZNO (1895: 15; 1896: 14) — Trotter žene 0× 3. leto; DOJENČIJSKA UMRLJIVOST 7/19 — NAJVIŠJE doslej (P91: 4/14): † r12 (24/1.98?), r15 (5/9.97?), r25 (17/9.97?), r28 (16/2.98?), r29 (7/6.97), r38 (3/9.99?), r59 (3/9.98?); DUHOVNIKI: Šuvar (1896 dominant) IZGINE — Klun 11× (dominanta) + Rauq 8× — MEŠANO LETO (preplet skozi vse mesece, ne pol-sezonsko); statusi: ½ × 16 + bajtar × 2 (r79 Muc + r84 Straus) + ¼ × 1 (sama mati); KURRENT FORENZIKA 6 POPRAVKOV: ① h23/h24 (r21 jasno 24 + r38 jasno 23 — DVE RAZLIČNI Brinec hiši, prvi prebir »oba 23« napačen) ② s93 r11 »Grablje?« → jasno GRISICE (druga vas — izključen iz vzorca; isto št. 2 kot Griblje r29!) ③ s99 r65/66 »Griblje 11?« → jasno OTOK (izključen) ④ s98 r53 »Griblje 10?« → jasno 16 (prvi prebir napačen) ⑤ row številke s99 59/62/64 (Kurrent 5/6 — kontinuiteta s98 51–58 → s99 59) ⑥ h45 mati = Barbara SPUDIČ (5x — POPRAVEK P91 prebira »Doroteja? [~]«); MATIČAR PRIPISI 20. st. 6 vpisov (r41 † 1931, r52 poroka 1919 + † 1981, r62 † 1980, r64 poroka 1934, r79 zakonca † 1979 + EHS ČG, r80 † 1989 + EHS ČG) — najgostejše doslej; SIDRA: h45 (Straus bajtar × Spudič — 2. VPIS ISTA ZVEZA 1896+1897 + POPRAVEK matere), h46 (Brodarič 4. VPIS + mati 3. VARIANTA: Klobučar 1893/95 → Kramarič? 1896 → Harašimovič? 1897 [~]; botra Željko = veriga), h31 (Straus kompleks 2 vpisa), h60 (Željko × Brodarič ISTA zveza — 4. dokaz luknje), h61 (Muc bajtar × Kure; botra Nikolaj Željko + Katarina Kure = h1 PAR KOT BOTRA — ŽELJKO VERIGA, začarani krog kot P91 h1), h24/h23 (dve Brinec hiši — 8. pin h24), h63 IZGINE (oče konstanten 5× 1887–96 — konec serije; botra Hrižan 3× v letu po izgini), h2 5. pin, h12 4. pin, h65 5. pin; live verifikacija: knjiga HTTP 200 (inventar 326), citirani skeni 8/8 JPEG 200 (sken 97 podvojen ni citiran); skripta scripts/p92_parish_baptism_1897.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1897",
  "P92: PARISH OF PODZEMELJ — BAPTISM REGISTER 04105, THE FULL YEAR 1897 (issue #18; SAMPLE-TRANSCRIPTION-1897; MEASURES, does not decide; the v7 join unchanged): extending the P79 (1886) → … → P90 (1895) → P91 (1896) sample to 1897 — the frame: scans 93–101 == printed pages 91–98 (the P92 NOVEL: SCAN 97 = DUPLICATED — a duplicate of s96 = p. 94, the 2nd known duplicate after scan 73; the P89 novel (page == scan − 2) holds only up to scan 96, from scan 98 page == scan − 3 — the offset shift is an ARTIFACT OF THE DUPLICATE, not a new numbering; the »Leto 1897« heading on p. 91 after the 1896 row 94; 1897 has 85 rows; the 1898 break on p. 98 = scan 101 row 86 — the labels restart, the P83 novel confirmed for the 10th year); ALL Griblje entries: 19 entries / 18 houses — SQUARE (the 4th year after P87 1892/P89 1894/P91 1896): 12, 32, 10, 24, 37, 54, 60, 2, 43, 23, 46, 31, 16, 40, 20, 31, 61, 65, 45 — h31 2 ENTRIES IN ONE YEAR (r51 Sapič? × Straus + r64 Straus? × Jakobič — THE STRAUS COMPLEX: 1894 Fapič?×Straus → 1896 Pendirec?×Žugelj change → 1897 both back!); 3 NEW houses (10, 40, 43) + 15 repeats; the cumulative 217 entries / 74 houses across three books and TWELVE years (the h61 anchor MERGED with the P79-era placeholder — a CROSS-PHASE CONFIRMATION: the original house-61 transcription noticed »Anton, father Miha P.—« at page 49 under the old assumption, the P92 5x forensics completes: Janez Muc cottager × Ana Kure, page 97 per the novel); A NEW GAP NUMBER: h43 (the 17th proven in 41–60 — PT_GAP_KNOWN gains +43) + h54 the 2nd proof + h60 the 4th proof + h45/h46 gaps — the gap now has 17 proven; THE FIRST ILLEGITIMATE ENTRY SINCE P90: r31 Florijan — FATHER EMPTY, mother Katarina Pozdirec SOLO MOTHER ¼ land (the P85 fraction novel, 8th year); THE MIDWIFE NOVEL CONFIRMED FOR THE 3RD YEAR: 19/19 EMPTY (1895: 15; 1896: 14) — the Trotter women 0× for the 3rd year; INFANT MORTALITY 7/19 — THE HIGHEST so far (P91: 4/14): † r12 (Jan 24, 98?), r15 (Sep 5, 97?), r25 (Sep 17, 97?), r28 (Feb 16, 98?), r29 (Jun 7, 97), r38 (Sep 3, 99?), r59 (Sep 3, 98?); PRIESTS: Šuvar (the 1896 dominant) DISAPPEARS — Klun 11× (the dominant) + Rauq 8× — A MIXED YEAR (an interleave through all months, not half-seasonal); statuses: ½ × 16 + cottagers × 2 (r79 Muc + r84 Straus) + ¼ × 1 (the solo mother); KURRENT FORENSICS 6 CORRECTIONS: ① h23/h24 (r21 clearly 24 + r38 clearly 23 — TWO DIFFERENT Brinec houses, the first read »both 23« wrong) ② s93 r11 »Grablje?« → clearly GRISICE (another village — excluded from the sample; the same no. 2 as Griblje r29!) ③ s99 r65/66 »Griblje 11?« → clearly OTOK (excluded) ④ s98 r53 »Griblje 10?« → clearly 16 (the first read wrong) ⑤ the s99 row numbers 59/62/64 (Kurrent 5/6 — the continuity s98 51–58 → s99 59) ⑥ the h45 mother = Barbara SPUDIČ (5x — CORRECTING the P91 read »Doroteja? [~]«); REGISTRAR NOTES of the 20th c. in 6 entries (r41 † 1931, r52 marriage 1919 + † 1981, r62 † 1980, r64 marriage 1934, r79 spouse † 1979 + EHS ČG, r80 † 1989 + EHS ČG) — the densest so far; ANCHORS: h45 (Straus cottager × Spudič — the 2nd ENTRY THE SAME COUPLE 1896+1897 + the mother CORRECTION), h46 (Brodarič the 4th ENTRY + the mother's 3rd VARIANT: Klobučar 1893/95 → Kramarič? 1896 → Harašimovič? 1897 [~]; godparent Željko = the chain), h31 (the Straus complex 2 entries), h60 (Željko × Brodarič THE SAME couple — the 4th proof of the gap), h61 (Muc cottager × Kure; godparents Nikolaj Željko + Katarina Kure = THE h1 COUPLE AS GODPARENTS — the ŽELJKO CHAIN, the closed circle like P91 h1), h24/h23 (two Brinec houses — the 8th pin h24), h63 DISAPPEARS (the father constant 5× 1887–96 — the end of the series; godmother Hrižan 3× in the year after the disappearance), h2 the 5th pin, h12 the 4th pin, h65 the 5th pin; live verification: the book HTTP 200 (inventory 326), cited scans 8/8 JPEG 200 (scan 97 duplicated not cited); the script scripts/p92_parish_baptism_1897.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1897",
  p92Errors.length === 0,
  p92Errors.length === 0
    ? `19 vpisov / 18 hiš — NARE (4. leto; 0 neberljivih; 19 zasidranih v vitals; h31 ×2 Straus kompleks) · okvir 1897 skeni 93–101 (NOVELA P92: sken 97 podvojen — stran == sken − 2 do 96, potem − 3; artefakt duplikata; prelom 1898 str. 98 row 86; 85 vrstic) · NOVA LUKNJA ŠTEVILKA 43 (17. dokazana; 54 2. + 60 4. dokaz) · 3 NOVE hiše (10, 40, 43) · h61 sidro ZDRUŽENO s P79-era placeholderjem (čez-fazna potrditev; oče popravljen Miha P.— → Muc) · PRVI NEZAKONSKI od P90 (r31 sama mati Pozdirec ¼) · NOVELA babica 3. leto (19/19 PRAZNO) · dojenčijska umrljivost 7/19 NAJVIŠJE · duhovniki Klun 11× + Rauq 8× (Šuvar izgine; mešano leto) · KURRENT 6 popravkov (23/24 dve hiši, Grisice izključena, Otok izključen, h16≠10, row 59/62/64, h45 Spudič) · matičar pripisi 6 vpisov · sidra h45 2. VPIS ISTA ZVEZA + POPRAVEK / h46 4. VPIS mati 3. varianta / h61 botra = h1 PAR / h24+h23 dve Brinec hiši · Željko veriga 10 signalov`
    : p92Errors.join("; "),
);

// ——— qa-p93: p93 krstna 1898 — širitev vzorca na leto 1898 (issue #18;
//      SAMPLE-TRANSCRIPTION-1898; celoven neodvisen preracun iz bundled
//      virov: HOUSE_VITALS × PARISH_BOOKS; PT klasifikacija iz pinov;
//      NOVELA P92 potrjena: stran == sken − 3 ZA CELO LETO (brez novih
//      duplikatov; sken 105 = str. 102 brez Griblje, ni citiran); leto 1898
//      ima 96 vrstic; prelom 1899 na str. 106 row 97→1 (1899 row 1 = Griblje
//      12!); 12 vpisov / 12 hiš — NARE 5. leto; 3 NOVE hiše (18, 48, 89);
//      NOVA LUKNJA ŠTEVILKA 48 (18. dokazana); h52 prvi TRDNI pin; VRNITEV
//      h63 (oče ISTI 6× — P92 »konec serije« POPRAVLJEN); DVE MENJAVI +
//      SELITEV (h69 Brinec→Straus; h33 Brinec→Dehlič, stari Brinec botra;
//      Berkopne h40→h48; Brodarič h46→h40 [~]); šolska hiša h90: tretji
//      učitelj (Kopitar → Vetročnik × Schmelzer); NOVELA babica 4. leto
//      (12/12 PRAZNO); duhovniki Rauq 8× + Šturm 3× + 1 neberljiv (Klun
//      izgine); r20 levi del UNIČEN (desni: Jurij Straus × Marija Jakofin)
//      — paleografska faza v research/issue17/parish-baptism-1898.json,
//      live verifikator scripts/p93_parish_baptism_1898.py --check I1–I10) ———
const p93Hv = HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year === 1898);
const p93Errors: string[] = [];
const P93_PT_IN_SET = ["18", "32", "33", "36", "40", "63", "69", "89", "90"];
const P93_PT_GAP = ["48", "52", "53"];
if (p93Hv.length !== 12)
  p93Errors.push(`vpisov 1898 (04105, zasidrani) ≠ 12 (${p93Hv.length})`);
const p93Houses = new Set(p93Hv.map((h) => h.houseNo));
if (p93Houses.size !== 12)
  p93Errors.push(`različnih hiš ≠ 12 (${p93Houses.size}: ${[...p93Houses].sort((a, b) => Number(a) - Number(b)).join(",")})`);
// okvir 1898: skeni 101–109; stran == sken − 3 za celo leto (novela P92);
// sken 105 ni citiran (0 Griblje vrstic)
const p93Bad = p93Hv.filter(
  (h) => h.status !== "DOCUMENTED" || !h.scan || !h.page
    || h.page !== h.scan - 3
    || h.scan < 101 || h.scan > 109,
);
if (p93Bad.length > 0)
  p93Errors.push(`okvir 1898: skeni 101–109 ali stran ≠ sken − 3 krščeno pri ${p93Bad.length}`);
if (p93Hv.some((h) => h.scan === 105))
  p93Errors.push("sken 105 (str. 102, brez Griblje) ni citiran v vpisih");
// NOVELA babica: vsi 12 blokov PRAZNI stolpec babice (4. leto)
const p93Babica = p93Hv.filter((h) => h.whatSi.includes("babica PRAZNA"));
if (p93Babica.length !== 12)
  p93Errors.push(`NOVELA babica: praznih ≠ 12 (${p93Babica.length})`);
// NOVA LUKNJA ŠTEVILKA 48: blok h48 mora imeti pin NOVA LUKNJA + SELITEV + 6x forenzika
const p93H48 = p93Hv.find((h) => h.houseNo === "48");
if (!p93H48 || !p93H48.whatSi.includes("NOVA LUKNJA ŠTEVILKA") || !p93H48.whatSi.includes("SELITEV") || !p93H48.whatSi.includes("jasno 48"))
  p93Errors.push("NOVA LUKNJA 48 / SELITEV / forenzika: whatSi ≠ P93 (pin manjka)");
// VRNITEV h63: blok h63 mora imeti VRNITEV + OČE ISTI 6× + † 1900
const p93H63 = p93Hv.find((h) => h.houseNo === "63");
if (!p93H63 || !p93H63.whatSi.includes("VRNITEV") || !p93H63.whatSi.includes("OČE ISTI 6×") || !p93H63.whatSi.includes("1900"))
  p93Errors.push("VRNITEV h63 / OČE ISTI 6× / † 1900: whatSi ≠ P93 (pin manjka)");
// h52 prvi TRDNI pin
const p93H52 = p93Hv.find((h) => h.houseNo === "52");
if (!p93H52 || !p93H52.whatSi.includes("PRVI TRDNI PIN"))
  p93Errors.push("h52 PRVI TRDNI PIN: whatSi ≠ P93 (pin manjka)");
// sidra (12 vpisov)
const p93Anchor = (hn: string, scan: number, pins: string[], label: string) => {
  const blk = p93Hv.find((h) => h.houseNo === hn && h.scan === scan);
  if (!blk || !pins.every((p) => blk.whatSi.includes(p)))
    p93Errors.push(`sidro ${label}: whatSi ≠ P93 (${pins.join(" + ")})`);
};
p93Anchor("40", 102, ["Brodarič", "MENJAVA", "ŽELJKO VERIGA"], "hiša 40");
p93Anchor("69", 103, ["Straus", "MENJAVA GOSPODINJSTVA", "Brinec"], "hiša 69");
p93Anchor("89", 103, ["NOVA ŠTEVILKA", "ŽELJKO VERIGA"], "hiša 89");
p93Anchor("18", 104, ["NOVA ŠTEVILKA", "Šimec"], "hiša 18");
p93Anchor("32", 104, ["Urk", "8. pin"], "hiša 32");
p93Anchor("36", 106, ["Hrigar", "3. VPIS ISTA ZVEZA"], "hiša 36");
p93Anchor("33", 107, ["Dehlič", "MENJAVA", "Brinec zdaj BOTRA"], "hiša 33");
p93Anchor("48", 107, ["Berkopne", "Klobučar"], "hiša 48");
p93Anchor("63", 107, ["Hrižan", "Podrinc"], "hiša 63");
p93Anchor("52", 107, ["Podrinc", "Jakobič"], "hiša 52");
p93Anchor("53", 108, ["Podrinc", "4. VPIS ISTA ZVEZA", "Kure"], "hiša 53");
p93Anchor("90", 109, ["Vetročnik", "UČITELJ", "Schmelzer"], "hiša 90");
// PT klasifikacija == pin: 11 v naboru + 1 v luknji (48 NOVA — 18. dokazana)
const p93InSet = [...p93Houses].filter((h) => P93_PT_IN_SET.includes(h));
const p93Gap = [...p93Houses].filter((h) => P93_PT_GAP.includes(h));
if (p93InSet.length !== 9 || p93Gap.length !== 3)
  p93Errors.push(`PT klasifikacija ≠ 9/3 (${p93InSet.length}/${p93Gap.length})`);
if (p93Gap.some((h) => !(Number(h) >= 41 && Number(h) <= 60)))
  p93Errors.push("luknjane hiše izven 41–60");
// NOVE hiše 1898 (18, 48, 89) — ne obstajajo v nobenem prejšnjem letu/knjigi;
// h53: P93 kontinuiteta ni nova (1891/1894/1896 priori); h40: MENJAVA (1897 prior)
for (const hn of ["18", "48", "89"]) {
  // P100: + 1905 blok h48 (2. VPIS — VRZEL 7 LET, 1898→1905); P101: + 1906 blok h18 (2. VPIS — VRZEL 8 LET); P102: + 1907 bloka h18 (3. VPIS — MENJAVA Šimec → Brinec) + h48 (3. VPIS — MENJAVA Pezdirec → Kure); P104: + 1909 blok h48 (4. VPIS — EMŠO = KRSTNI datum); P105: + 1910 blok h18 (4. VPIS — POVRAT Šimec × Kambič); P106: + 1911 blok h48 (5. VPIS); P107: + 1912 bloka h18 (5. VPIS — ANOMALIJA) + h48 (6. VPIS — ZAPORED); P109: + 1914 bloka h18 (6. VPIS) + h48 (7. VPIS — DVOM REŠEN, 12. VPIS VZORCA!); P114: + 1919 blok h48 (8. VPIS — DRŽAVLJANKA RS!)
  if (HOUSE_VITALS.some((v) => v.houseNo === hn && !(v.bookSignature === "04105" && (v.year === 1898 || v.year === 1905 || v.year === 1906 || v.year === 1907 || v.year === 1909 || v.year === 1910 || v.year === 1911 || v.year === 1912 || v.year === 1914 || v.year === 1919)) && !(v.bookSignature === "04455" && hn === "18" && v.year === 1896) && !(v.bookSignature === "04455" && hn === "18" && v.year === 1897) && !(v.bookSignature === "04455" && hn === "48" && v.year === 1898) && !(v.bookSignature === "04455" && hn === "48" && v.year === 1903) && !(v.bookSignature === "04455" && hn === "18" && v.year === 1905))) // P125: + poročni blok h18-1896 (v15 Klobučar); P126: + poročni blok h18-1897 (v10 Simec × Kuchar — MEGA cross-link!); P127: + poročni blok h48-1898 (v2 nevesta Anna KLOBUČAR — ISTO leto kot krstni okvir!); P132: + poročni blok h48-1903 (v17 nevesta Berkoprec — 2. poročni dokaz h48, DRUBEL!); P134: + poročni blok h18-1905 (v13 ženin Mathias SIMEC — 3. poročni dokaz h18, DRUBEL — SIMEC-kontinuiteta 1897!)
    p93Errors.push(`NOVA hiša ${hn} (P93) že obstaja v prejšnjem letu — pini neskladni`);
}
// kontinuitete čez leta prek HOUSE_VITALS (klasifikacija zgodovinska —
// poznejši bloki ne spreminjajo pričakovanih priorov)
// oblika: [hiša, leto, knjiga, whatSi-pin ALI "" za scan-pin, pričakovani sken]
for (const [hn, yr, sig, pin, sc] of [
  ["63", 1887, "04105", "", 17], ["63", 1892, "04105", "", 61], ["63", 1896, "04105", "Hrižan", null],
  ["69", 1888, "04105", "Brinec", null], ["69", 1890, "04105", "Brinec", null], ["69", 1895, "04105", "Brinec", null],
  ["33", 1889, "04105", "Brinec", null],
  ["53", 1891, "04105", "Pozdirec", null], ["53", 1896, "04105", "Hrižan", null],
  ["36", 1894, "04105", "Križan", null], ["36", 1896, "04105", "Straucelj", null],
  ["32", 1889, "04105", "", 39], ["32", 1892, "04105", "Urh", null],
  ["40", 1897, "04105", "Berkovec", null],
  ["52", 1887, "04105", "Muc", null],
  ["90", 1890, "04105", "Kopitar", null], ["90", 1892, "04105", "Kopitac", null],
  ["2", 1897, "04105", "", 95],
  ["61", 1897, "04105", "Muc", null],
  ["12", 1897, "04105", "Dragar", null],
  ["65", 1897, "04105", "Mihek", null],
  ["45", 1897, "04105", "Spudič", null],
] as const) {
  const blk = HOUSE_VITALS.find((v) => v.houseNo === hn && v.bookSignature === sig && v.year === yr);
  const ok = blk && (pin === "" ? blk.scan === sc : HOUSE_VITALS.some((v) => v.houseNo === hn && v.bookSignature === sig && v.year === yr && v.whatSi.includes(pin)));
  if (!ok)
    p93Errors.push(`kontinuiteta hiša ${hn} (${yr}, ${sig}, pin ${pin || `sk ${sc}`}) manjka ali pin ne ustreza`);
}
// vitals skupaj 449 (po P106: 429 + 20; krstna 1911)
if (HOUSE_VITALS.length !== 685)
  p93Errors.push(`HOUSE_VITALS ≠ 467 (${HOUSE_VITALS.length})`);
push(
  "qa-p93-parish-baptism-1898",
  "P93: ŽUPNIJA PODZEMELJ — KRSTNA KNJIGA 04105, POLNO LETO 1898 (issue #18; SAMPLE-TRANSCRIPTION-1898; MERI, NE odloča; v7 join nespremenjen): širitev vzorca P79 (1886) → … → P91 (1896) → P92 (1897) na leto 1898 — okvir: skeni 101–109 == tiskane strani 98–106 (NOVELA P92 POTRJENA: stran == sken − 3 ZA CELO LETO — brez novih duplikatov; sken 105 = str. 102 brez Griblje vrstic, ni citiran; glava »1898.« na str. 98 po 1897 row 85; leto 1898 ima 96 vrstic; prelom 1899 na str. 106 = sken 109 row 97→1 — oznake ponastavljene, novela P83 potrjena 11. leto; 1899 row 1 = Griblje 12 Marija — novo leto se začne z Griblji!) — VSI vpisi z Griblji: 12 vpisov / 12 hiš — NARE (5. leto po P87 1892/P89 1894/P91 1896/P92 1897): 40, 69, 89, 18, 32, 36, 33, 48, 63, 52, 53, 90 — 3 NOVE hiše (18, 48, 89) + 9 ponovitev; kumulativ 229 vpisov / 77 hiš čez tri knjige in TRINAJST let; NOVA LUKNJA ŠTEVILKA: h48 (18. dokazana v 41–60 — PT_GAP_KNOWN dobi +48; forenzika 6x: jasno 48, ne 40 — dvojna zanka = 8) + h52 PRVI TRDNI PIN (1887 [~] po trojni korekciji 52→04→15) — luknja zdaj 18 dokazanih; VRNITEV h63: oče Nikolaj Hrižan [Križan/Prižan] ISTI 6× (1887+1889+1890+1892+1896+1898, brez 1897) — P92 zaključek »h63 IZGINE — konec serije« POPRAVLJEN; najbolj konstanten oče vzorca; dojenček Jožef † 6/6.1900; NAJGOSTEJŠE GIBANJE GOSPODINJSTEV V VZORCU (4 rotacije v enem letu): h69 MENJAVA Brinec (5 vpisov 1888–95) → Nikolaj Straus × Marija Jakobšič (Straus na 4. hiši h71/h72/h45/h69; otrok † 6.1.1983 v Gribljah po matičarjem pripisu), h33 MENJAVA Brinec (1889) → Dehlič × Rožek (stari h33 oče Matija Brinec zdaj BOTRA), SELITEV Berkopne × Klobučar h40 (1897) → h48 (1898) — ISTA ZVEZA, druga hiša, h40 MENJAVA → Anton Brodarič × Marija Milek (= h46 oče 1893–97 — rotacija [~]; očetovo ime PREČRTANO v izvirniku); ŠOLSKA HIŠA h90: TRETJI UČITELJ — Kopitar (1890+1892) → Alojzij Vetročnik [~] UČITELJ × Leopolda Schmelzer (nemški priimek); botr učitelj Ivan Vrhovec [~ Arhovec] — tretja učiteljska generacija (1890 botra Janez Barle, 1892 nadučitelj); 0 nezakonskih med Griblji (r29 Obveca = druga vas); NOVELA babica POTRJENA 4. LETO: 12/12 PRAZNO (Trotter 0×); DOJENČIJSKA UMRLJIVOST 1/12 potrjena (r78 † 6/6.1900) + r37 [~] možna — najnižja po P92 7/19; DUHOVNIKI: Rauq (Jos.) 8× dominant (nadaljuje iz 1897) + Šturm (Fr.) 3× + 1 neberljiv (r42) — Klun (11× 1897) IZGINE; statusi: ½ zemljak × 10 + ¼ × 2 (r22 Straus, r72 Berkopne) + učitelj × 2 (r96 oče + botra); KURRENT FORENZIKA 6 POPRAVKOV/ODLOČITEV: ① s101 r5 »Griblje 39?« → jasno GRIŠINIČE 33 (druga vas — izključena; prvi prebir iz celostranskega ogleda napačen) ② s107 r76 »Griblje?« → jasno ŠRIGLJE? (druga vas — izključena; hišna št. pod modrim pripisom) ③ s102 r20 LEVI DEL UNIČEN (modri matičar pripisi 1971–83 + raztrgana meja; desni del preživel: Jurij Straus × Marija Jakofin + botra Matija Straucel × Barbara Jakofin — verjetno Griblje [~], NEŠTET) ④ s107 r72 »40?« → jasno 48 (6x — dvojna zanka; posledica: h40 samo 1 vpis 1898) ⑤ s106 r63 »56?« → jasno 36 (5x) ⑥ s103 r22 »2?« → jasno 69 + r30 »81/31?« → jasno 89 (Kurrent 9 z dolgim repom γ-oblika); priimki: Hrigar/Hrigovc = Hrižan/Križan cluster [~] (po P91/P92), Podrinc = Pendirec cluster [~] (po P86–P92), Urk = Urh cluster [~] (po P87–P92); MATIČAR PRIPISI 20./21. st. v 9 od 12 vpisov (EMŠO blok 1982–83, † 1951/1963/1974?/1975/1981/1983, poroke 1921/1922/1924/1928/1929) — najgostejša pokritost doslej; SIDRA: h63 VRNITEV (oče 6×), h69/h33 menjavi, h48 selitev + NOVA LUKNJA, h90 tretji učitelj, h53 4. VPIS ISTA ZVEZA + botra Ana Kure (h1 familija), h36 3. VPIS ISTA ZVEZA (tri-virska hiša 7.+8. vir), h32 8. pin (Urk varianta), h89 NOVA + botra Željko (ŽELJKO VERIGA 2 nova signala — skupaj 12), h18 NOVA (Šimec 5. hiša; oče Matija Šimec = r89 botra — ista oseba oče + botra), h52 prvi trdni pin; live verifikacija: knjiga HTTP 200 (inventar 326), citirani skeni 8/8 JPEG 200 (sken 105 ni citiran); skripta scripts/p93_parish_baptism_1898.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1898",
  "P93: PARISH OF PODZEMELJ — BAPTISM REGISTER 04105, THE FULL YEAR 1898 (issue #18; SAMPLE-TRANSCRIPTION-1898; MEASURES, does not decide; the v7 join unchanged): extending the P79 (1886) → … → P91 (1896) → P92 (1897) sample to 1898 — the frame: scans 101–109 == printed pages 98–106 (the P92 NOVEL CONFIRMED: page == scan − 3 FOR THE WHOLE YEAR — no new duplicates; scan 105 = p. 102 with no Griblje rows, not cited; the »1898.« heading on p. 98 after the 1897 row 85; 1898 has 96 rows; the 1899 break on p. 106 = scan 109 row 97→1 — the labels restart, the P83 novel confirmed for the 11th year; the 1899 row 1 = Griblje 12 Marija — the new year STARTS with Griblje!); ALL Griblje entries: 12 entries / 12 houses — SQUARE (the 5th year after P87 1892/P89 1894/P91 1896/P92 1897): 40, 69, 89, 18, 32, 36, 33, 48, 63, 52, 53, 90 — 3 NEW houses (18, 48, 89) + 9 repeats; the cumulative 229 entries / 77 houses across three books and THIRTEEN years; A NEW GAP NUMBER: h48 (the 18th proven in 41–60 — PT_GAP_KNOWN gains +48; forensics 6x: clearly 48, not 40 — the double loop = 8) + h52 THE FIRST SOLID PIN (the 1887 [~] survived the triple correction 52→04→15) — the gap now has 18 proven; THE h63 RETURN: the father Nikolaj Hrižan [Križan/Prižan] THE SAME 6× (1887+1889+1890+1892+1896+1898, minus 1897) — the P92 conclusion »h63 DISAPPEARS — the end of the series« CORRECTED; the most constant father in the sample; the infant Jožef † Jun 6, 1900; THE DENSEST HOUSEHOLD MOVEMENT IN THE SAMPLE (4 rotations in one year): h69 HOUSEHOLD CHANGE Brinec (5 entries 1888–95) → Nikolaj Straus × Marija Jakobšič (the Straus signal on a 4th house h71/h72/h45/h69; the child † Jan 6, 1983 in Griblje per the registrar note), h33 HOUSEHOLD CHANGE Brinec (1889) → Dehlič × Rožek (the old h33 father Matija Brinec now a GODPARENT), THE MOVE Berkopne × Klobučar h40 (1897) → h48 (1898) — THE SAME COUPLE, another house, h40 CHANGE → Anton Brodarič × Marija Milek (= the h46 father 1893–97 — rotation [~]; the father's name STRUCK OUT in the original); THE SCHOOL HOUSE h90: THE THIRD TEACHER — Kopitar (1890+1892) → Alojzij Vetročnik [~] TEACHER × Leopolda Schmelzer (a German surname); the godparent teacher Ivan Vrhovec [~ Arhovec] — the third teacher generation (1890 godparent Janez Barle, 1892 the head teacher); 0 illegitimates among Griblje (r29 Obveca = another village); THE MIDWIFE NOVEL CONFIRMED FOR THE 4TH YEAR: 12/12 EMPTY (the Trotter women 0×); INFANT MORTALITY 1/12 confirmed (r78 † Jun 6, 1900) + r37 [~] possible — the lowest since the P92 7/19; PRIESTS: Rauq (Jos.) 8× the dominant (continuing from 1897) + Šturm (Fr.) 3× + 1 illegible (r42) — Klun (11× in 1897) DISAPPEARS; statuses: ½ smallholder × 10 + ¼ × 2 (r22 Straus, r72 Berkopne) + teacher × 2 (r96 father + godparent); KURRENT FORENSICS 6 CORRECTIONS/DECISIONS: ① s101 r5 »Griblje 39?« → clearly GRIŠINIČE 33 (another village — excluded; the first full-page read wrong) ② s107 r76 »Griblje?« → clearly ŠRIGLJE? (another village — excluded; the house number under a blue note) ③ s102 r20 THE LEFT SIDE DESTROYED (blue registrar notes 1971–83 + the torn edge; the right side survived: Jurij Straus × Marija Jakofin + godparents Matija Straucel × Barbara Jakofin — probably Griblje [~], NOT COUNTED) ④ s107 r72 »40?« → clearly 48 (6x — the double loop; consequence: h40 only 1 entry in 1898) ⑤ s106 r63 »56?« → clearly 36 (5x) ⑥ s103 r22 »2?« → clearly 69 + r30 »81/31?« → clearly 89 (the Kurrent 9 with a long tail, γ-shaped); surnames: Hrigar/Hrigovc = the Hrižan/Križan cluster [~] (per P91/P92), Podrinc = the Pendirec cluster [~] (per P86–P92), Urk = the Urh cluster [~] (per P87–P92); REGISTRAR NOTES of the 20th/21st c. in 9 of 12 entries (the EMŠO block 1982–83, † 1951/1963/1974?/1975/1981/1983, marriages 1921/1922/1924/1928/1929) — the densest coverage so far; ANCHORS: h63 THE RETURN (the father 6×), h69/h33 the changes, h48 the move + A NEW GAP, h90 the third teacher, h53 the 4th ENTRY THE SAME COUPLE + godmother Ana Kure (the h1 family), h36 the 3rd ENTRY THE SAME COUPLE (the three-source house's 7th + 8th sources), h32 the 8th pin (the Urk variant), h89 NEW + godparent Željko (the ŽELJKO CHAIN, 2 new signals — 12 total), h18 NEW (the Šimec 5th house; the father Matija Šimec = the r89 godparent — the same person father + godparent), h52 the first solid pin; live verification: the book HTTP 200 (inventory 326), cited scans 8/8 JPEG 200 (scan 105 not cited); the script scripts/p93_parish_baptism_1898.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1898",
  p93Errors.length === 0,
  p93Errors.length === 0
    ? `12 vpisov / 12 hiš — NARE (5. leto; 0 neberljivih; 12 zasidranih v vitals) · okvir 1898 skeni 101–109 (novela P92 potrjena: stran == sken − 3 za celo leto; sken 105 brez Griblje ni citiran; prelom 1899 str. 106 row 97→1; 96 vrstic; 1899 row 1 = Griblje 12!) · NOVA LUKNJA ŠTEVILKA 48 (18. dokazana; 6x jasno 48 ne 40) · h52 prvi TRDNI pin · 3 NOVE hiše (18, 48, 89) · VRNITEV h63 (oče ISTI 6× — P92 »konec serije« popravljen; † 6/6.1900) · 4 rotacije gospodinjstev (h69 Brinec→Straus; h33 Brinec→Dehlič z Brincem kot botrom; Berkopne h40→h48; Brodarič h46→h40 [~]) · šolska h90: tretji učitelj Vetročnik × Schmelzer, botr učitelj Vrhovec · NOVELA babica 4. leto (12/12 PRAZNO) · dojenčijska umrljivost 1/12 (+ r37 [~]) · duhovniki Rauq 8× + Šturm 3× + 1 neberljiv (Klun izgine) · KURRENT 6 popravkov (Grišiniče izključena, Šriglje izključena, r20 uničen, h48≠40, h36≠56, h69/h89 Kurrent 9) · matičar pripisi 9/12 vpisov · sidra h53 4. VPIS + Kure / h36 3. VPIS (7.+8. vir) / h32 8. pin Urk / h89+h18 NOVI (Šimec oče = botra) · Željko veriga 12 signalov`
    : p93Errors.join("; "),
);

// ——— qa-p94: p94 krstna 1899 — širitev vzorca na leto 1899 (issue #18;
//      SAMPLE-TRANSCRIPTION-1899; celoven neodvisen preracun iz bundled
//      virov: HOUSE_VITALS × PARISH_BOOKS; PT klasifikacija iz pinov;
//      NOVELA P92 potrjena: stran == sken − 3 ZA CELO LETO (brez novih
//      duplikatov; sken 118 = str. 115 samo okvir, ni citiran za vpise);
//      okvir skeni 109 row 97 – 118 row 104 == str. 106–115; 104 vrstic;
//      prelom 1900 NA SREDINI str. 115 row 105 (prvič ne na novi strani;
//      novela P83 potrjena 12. leto); 15 vpisov / 15 hiš — NARE 6. leto,
//      PRVO LETO BREZ znotraj-letnih ponovitev; 2 NOVI hiši (22 PT nabor +
//      49 NOVA LUKNJA ŠTEVILKA — 19. dokazana); h60 TRDNI PIN (4. vpis
//      iste zveze + 3. ista botra para); h40 TRETJA družina v 3 letih +
//      STRAUS × SPUDIČ (poročni lead 04455); menjave h1/h30/h34/h57;
//      SEGINA VERIGA 3 signali; ŽELJKO VERIGA 13.+14. signal; NOVELA
//      babica 5. leto (15/15 PRAZNO/poškodovano); duhovniki Šturm 6× +
//      Rauq 4× + Klun 2× + 3 neberljivih; r25 NEŠTET) ———
const p94Hv = HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year === 1899);
const p94Errors: string[] = [];
const P94_PT_IN_SET = ["1", "12", "21", "22", "27", "30", "34", "40", "75"];
const P94_PT_GAP = ["41", "46", "49", "57", "59", "60"];
if (p94Hv.length !== 15)
  p94Errors.push(`vpisov 1899 (04105, zasidrani) ≠ 15 (${p94Hv.length})`);
const p94Houses = new Set(p94Hv.map((h) => h.houseNo));
if (p94Houses.size !== 15)
  p94Errors.push(`različnih hiš ≠ 15 (${p94Houses.size}: ${[...p94Houses].sort((a, b) => Number(a) - Number(b)).join(",")})`);
// okvir 1899: skeni 109–117; stran == sken − 3 za celo leto (novela P92);
// sken 118 ni citiran (samo okvir/prelom 1900)
const p94Bad = p94Hv.filter(
  (h) => h.status !== "DOCUMENTED" || !h.scan || !h.page
    || h.page !== h.scan - 3
    || h.scan < 109 || h.scan > 117,
);
if (p94Bad.length > 0)
  p94Errors.push(`okvir 1899: skeni 109–117 ali stran ≠ sken − 3 krščeno pri ${p94Bad.length}`);
if (p94Hv.some((h) => h.scan === 118))
  p94Errors.push("sken 118 (str. 115, samo okvir/prelom 1900) ni citiran v vpisih");
// NOVELA babica: vsi 15 blokov PRAZNI (ali poškodovani) stolpec babice (5. leto)
const p94Babica = p94Hv.filter((h) => h.whatSi.includes("babica PRAZNA") || h.whatSi.includes("babica [~ poškodovano]"));
if (p94Babica.length !== 15)
  p94Errors.push(`NOVELA babica: praznih/poškodovanih ≠ 15 (${p94Babica.length})`);
// NOVA LUKNJA ŠTEVILKA 49: blok h49 mora imeti pin NOVA LUKNJA + 19. dokazana + jasno 49
const p94H49 = p94Hv.find((h) => h.houseNo === "49");
if (!p94H49 || !p94H49.whatSi.includes("NOVA LUKNJA ŠTEVILKA") || !p94H49.whatSi.includes("19. dokazana") || !p94H49.whatSi.includes("jasno 49"))
  p94Errors.push("NOVA LUKNJA 49 / 19. dokazana / forenzika: whatSi ≠ P94 (pin manjka)");
// h60 TRDNI PIN: blok h60 mora imeti TRDNI PIN + ISTA ZVEZA + 3. ISTA BOTRA PARA
const p94H60 = p94Hv.find((h) => h.houseNo === "60");
if (!p94H60 || !p94H60.whatSi.includes("TRDNI PIN") || !p94H60.whatSi.includes("4. VPIS ISTA ZVEZA") || !p94H60.whatSi.includes("3. ISTA BOTRA PARA"))
  p94Errors.push("h60 TRDNI PIN / 4. VPIS ISTA ZVEZA / 3. ISTA BOTRA PARA: whatSi ≠ P94 (pin manjka)");
// h40 STRAUS × SPUDIČ + TRETJA DRUŽINA + 04455 lead
const p94H40 = p94Hv.find((h) => h.houseNo === "40");
if (!p94H40 || !p94H40.whatSi.includes("STRAUS × SPUDIČ") || !p94H40.whatSi.includes("TRETJA DRUŽINA") || !p94H40.whatSi.includes("Spudič") || !p94H40.whatSi.includes("bajtar"))
  p94Errors.push("h40 STRAUS × SPUDIČ / TRETJA DRUŽINA / bajtar: whatSi ≠ P94 (pin manjka)");
// sidra (15 vpisov)
const p94Anchor = (hn: string, scan: number, pins: string[], label: string) => {
  const blk = p94Hv.find((h) => h.houseNo === hn && h.scan === scan);
  if (!blk || !pins.every((p) => blk.whatSi.includes(p)))
    p94Errors.push(`sidro ${label}: whatSi ≠ P94 (${pins.join(" + ")})`);
};
p94Anchor("12", 109, ["Dragar", "Cvitkovič"], "hiša 12");
p94Anchor("46", 110, ["Brodarič", "5. VPIS ISTA ZVEZA", "Škaradinič"], "hiša 46");
p94Anchor("27", 110, ["Knekar", "Klobučar", "6. VPIS"], "hiša 27");
p94Anchor("59", 110, ["Simič", "Kure"], "hiša 59");
p94Anchor("22", 111, ["NOVA ŠTEVILKA", "Milek", "Klepec"], "hiša 22");
p94Anchor("41", 112, ["Kušič", "4. VPIS ISTA ZVEZA"], "hiša 41");
p94Anchor("21", 112, ["Požek", "Šimec", "2. VPIS ISTA ZVEZA"], "hiša 21");
p94Anchor("1", 114, ["Segina", "MENJAVA", "SEGINA VERIGA"], "hiša 1");
p94Anchor("30", 114, ["Županič", "4. DRUŽINA", "ŽUPANIČ CLUSTER"], "hiša 30");
p94Anchor("75", 115, ["Jakobič", "Stubljar", "3. VPIS ISTA ZVEZA"], "hiša 75");
p94Anchor("57", 116, ["Pozdirec", "OČE MENJAVA", "Željko"], "hiša 57");
p94Anchor("49", 117, ["Brodarič", "Milek"], "hiša 49");
p94Anchor("34", 117, ["Šilak", "Klobučar", "2. DRUŽINA"], "hiša 34");
// PT klasifikacija == pin: 9 v naboru + 6 v luknji (49 NOVA — 19. dokazana)
const p94InSet = [...p94Houses].filter((h) => P94_PT_IN_SET.includes(h));
const p94Gap = [...p94Houses].filter((h) => P94_PT_GAP.includes(h));
if (p94InSet.length !== 9 || p94Gap.length !== 6)
  p94Errors.push(`PT klasifikacija ≠ 9/6 (${p94InSet.length}/${p94Gap.length})`);
if (p94Gap.some((h) => !(Number(h) >= 41 && Number(h) <= 60)))
  p94Errors.push("luknjane hiše izven 41–60");
// NOVE hiše 1899 (22, 49) — ne obstajata v nobenem prejšnjem letu/knjigi
for (const hn of ["22", "49"]) {
  const allow = hn === "22" ? [1899, 1902, 1904, 1905, 1910, 1912, 1915] : hn === "49" ? [1899, 1906, 1907, 1908, 1910, 1911] : [1899, 1906, 1907, 1908]; // P97: + 1902 blok h22 (2. VPIS — MENJAVA ŽENE Klepec → Žurrič?); P99: + 1904 blok h22 (3. VPIS — POŽEK signal, boter Janez Požek); P100: + 1905 blok h22 (4. VPIS — Nikolaj Milek, botra Ana Požek); P101: + 1906 blok h49 (2. VPIS — Brodarič ↔ Željko izmena); P102: + 1907 blok h49 (3. VPIS — ISTI oče Brodarič; dojenček †); P103: + 1908 blok h49 (4. VPIS — ISTI oče Brodarič); P105: + 1910 bloka h22 (5. VPIS — Milek ISTI 5×) + h49 (5. VPIS — boter Jakop Bohte 2.×) P107: + 1912 blok h22 (6. VPIS — Miko Alek MLINAR)
  if (HOUSE_VITALS.some((v) => v.houseNo === hn && !(v.bookSignature === "04105" && allow.includes(v.year)) && !(v.bookSignature === "04455" && hn === "22" && (v.year === 1898 || v.year === 1904)))) // P127: + poročni bloka h22-1898 (v7 Straus + v9 Milek — PRED krsto 1899, vzorec qa-p91 h14!); P133: + poročni blok h22-1904 (v14 nevesta Catharina Milek — 3. poročni dokaz h22, DRUBEL — menjava družine STRAUS → MILEK!)
    p94Errors.push(`NOVA hiša ${hn} (P94) že obstaja v prejšnjem letu — pini neskladni`);
}
// kontinuitete čez leta prek HOUSE_VITALS (klasifikacija zgodovinska —
// poznejši bloki ne spreminjajo pričakovanih priorov)
// oblika: [hiša, leto, knjiga, whatSi-pin ALI "" za scan-pin, pričakovani sken]
const P94_CONTINUITY: Array<[string, number, string, string, number | null]> = [
  ["60", 1893, "04105", "Željko", null], ["60", 1894, "04105", "Željko", null], ["60", 1897, "04105", "Željko", null],
  ["41", 1890, "04105", "Hrušič", null], ["41", 1893, "04105", "Hušič", null], ["41", 1896, "04105", "Hušič", null],
  ["21", 1893, "04105", "Požek", null], ["21", 1887, "04105", "Požek", null],
  ["75", 1892, "04105", "Jakobčič", null], ["75", 1894, "04105", "Jakobič", null],
  ["46", 1893, "04105", "Brodarič", null], ["46", 1896, "04105", "Brodarič", null], ["46", 1897, "04105", "Brodarič", null],
  ["27", 1893, "04105", "Klobučar", null],
  ["34", 1887, "04105", "Šimec", null],
  ["40", 1897, "04105", "Berkovec", null], ["40", 1898, "04105", "Brodarič", null],
  ["1", 1888, "04105", "Zeljth", null], ["1", 1892, "04105", "Željko", null], ["1", 1896, "04105", "Željko", null],
  ["30", 1890, "04105", "Milek", null], ["30", 1893, "04105", "Jakljevič", null], ["30", 1895, "04105", "Šegina", null],
  ["57", 1889, "04105", "Pezdirec", null], ["57", 1894, "04105", "Pegdirec", null],
  ["59", 1889, "04105", "Podirec", null], // 1889 nezakonska (mati Podirec) — prvi imenovani oče šele 1899
  ["12", 1897, "04105", "Dragar", null],
];
for (const [hn, yr, sig, pin, sc] of P94_CONTINUITY) {
  const blk = HOUSE_VITALS.find((v) => v.houseNo === hn && v.bookSignature === sig && v.year === yr);
  const ok = blk && (pin === "" ? blk.scan === sc : HOUSE_VITALS.some((v) => v.houseNo === hn && v.bookSignature === sig && v.year === yr && v.whatSi.includes(pin)));
  if (!ok)
    p94Errors.push(`kontinuiteta hiša ${hn} (${yr}, ${sig}, pin ${pin || `sk ${sc}`}) manjka ali pin ne ustreza`);
}
// vitals skupaj 449 (po P106: 429 + 20; krstna 1911)
if (HOUSE_VITALS.length !== 685)
  p94Errors.push(`HOUSE_VITALS ≠ 467 (${HOUSE_VITALS.length})`);
push(
  "qa-p94-parish-baptism-1899",
  "P94: ŽUPNIJA PODZEMELJ — KRSTNA KNJIGA 04105, POLNO LETO 1899 (issue #18; SAMPLE-TRANSCRIPTION-1899; MERI, NE odloča; v7 join nespremenjen): širitev vzorca P79 (1886) → … → P92 (1897) → P93 (1898) na leto 1899 — okvir: skeni 109 row 97 – 118 row 104 == tiskane strani 106–115 (NOVELA P92 POTRJENA: stran == sken − 3 ZA CELO LETO — brez novih duplikatov; sken 118 = str. 115 samo okvir, ni citiran za vpise; 1899 r1 = Griblje 12 Marija na str. 106 — novo leto se začne z Griblji; leto 1899 ima 104 vrstic; prelom 1900 NA SREDINI str. 115 = sken 118 row 105 — PRVIČ V VZORCU se novo leto NE začne na novi strani; 1900 row 1 = Krasinec — prvič z drugo vasjo; novela P83 potrjena 12. leto) — VSI vpisi z Griblji: 15 vpisov / 15 hiš — NARE (6. leto po P87/P89/P91/P92/P93) in PRVO LETO BREZ znotraj-letnih ponovitev (vsaka hiša 1×): 12, 46, 27, 60, 59, 22, 41, 21, 40, 1, 30, 75, 57, 49, 34 — 2 NOVI hiši (22, 49) + 13 ponovitev; kumulativ 244 vpisov / 79 hiš čez tri knjige in ŠTIRNAJST let (238 vitals); NOVA ŠTEVILKA h22 (v PT naboru 1825 — ATLAS_HOUSES že vsebuje 22; prvi matrični dokaz; Milek × Klepec NOVA ZVEZA — mati [~ ista oseba kot botra h60 Marija Klepac: botra 13.3. + mati 20.3. v 1 tednu]) + NOVA LUKNJA ŠTEVILKA: h49 (19. dokazana v 41–60 — PT_GAP_KNOWN dobi +49; forenzika 8x: jasno 49; luknja zdaj 42/50/51) — luknja zdaj 19 dokazanih; h60 TRDNI PIN: 4. VPIS ISTA ZVEZA Željko × Brodarič (1893+1894+1897+1899) + 3. ISTA BOTRA PARA Pendirec × Klepac (1893+1894+1899) — hišna pod modrim pripisom: kanalna forenzika (temen »…o 6o«) + STRUKTURNA POTRDITEV (oče + botra para = h60); ŽELJKO VERIGA 13.+14. signal (oče h60 + botra h57); SEGINA VERIGA 3 signali v enem letu (oče h1 + botra h49 + botra h34); h40 TRETJA DRUŽINA V TRIH LETIH: Berkopne (1897) → Brodarič (1898 [~]) → Martin Straus bajtar × Barbara Spudič (1899) — STRAUS × SPUDIČ = POTRDITEV poročnega lead-a 04455; MENJAVE GOSPODINJSTEV: h1 Željko (1888–96) → Segina (SEGINA VERIGA h70 1893 → h30 1895 → h1 1899 — 3 hiše / 6 let), h30 4. DRUŽINA (Milek → Jakljevič 1893 → Šegina 1895 → Janez Županič 1899 — ŽUPANIČ CLUSTER 3 signali: h73 1894 + h30 + botra Ana Županič), h34 2. DRUŽINA (Šimec 1887 → Nikolaj Šilak? × Katarina Klobučar), h57 OČE MENJAVA Peter Pezdirec (1888–94) → Miha Pozdirec (brata? sin?; Miha = botra h41 1896); 5. VPIS ISTA ZVEZA h46 (4. varianta matere: Klobučar? → Kramarič? → Harašimovič? → Škaradinič? — priimek Škaradinič potrjen pri Krasinec 32); h27 6. VPIS (oče 2. branje: Stukar/Stubhar 1893 → Knekar? 1899; botra h21 Janez Knekar = KRIŽNI SKLIC); h41 4. VPIS + h21 2. VPIS ISTA ZVEZA + h75 3. VPIS ISTA ZVEZA (Jakobič × Stubljar, 4. varianta priimka); h12 mati MENJAVA [~] (Straus 1897 → Cvitkovič 1899; botra 1899 = 1897 mati?! — možna zamenjava celic P92); 0 nezakonskih; NOVELA babica POTRJENA 5. LETO: 15/15 PRAZNO/poškodovano; DOJENČIJSKA UMRLJIVOST 3/15 (r1 † 25/6.99 [~], r26 † 2/[5-6].99 [~], r94 † 24/6.00) — višja kot P93 1/12; DUHOVNIKI: Šturm (Fr.) 6× + Rauq (Jos.) 4× + Klun (Fr.) 2× VRNITEV iz 1897 + 3 neberljivih (r71 raztrgan, r94/r100 »Jos. Kergo?«); statusi: ½ zemljak × 14 + bajtar × 1 (r43 Straus); KURRENT FORENZIKA: r13 hišna pod pripisom (kanalna + strukturna — 60 TRDNO), r26 jasno 22 (NOVA), r89 datum UNIČEN (raztrgan rob — ~november po sosedi), r94 jasno 49 (ne 34 — dvojna forenzika z r100), r71 datum popravek (»23« + »2« nad — verjetno 2.10. + krst 3.10.), r61 kraj »Griblja« varianta (smrtna opomba POTRJUJE Griblje: † 31.3.1975 v Gribljah), r25 NEŠTET (matičar črno nadpisal kraj+hišno — ime Jožef), r27 Berkoviše + r93 »Germ« izključeni (drugi vasi); MATIČAR PRIPISI 20./21. st. v večini vpisov († 1964/1965/1969/1970s/1975/1984, poroke 1921/1926/1930, EMŠO blok); SIDRA: h60 TRDNI PIN (4. VPIS + 3. BOTRA PARA), h49 NOVA LUKNJA (Brodarič = botra h48 1898 → oče h49), h22 NOVA, h40 TRETJA DRUŽINA + Straus × Spudič, h1 MENJAVA + SEGINA VERIGA, h30 4. DRUŽINA + ŽUPANIČ, h34 2. DRUŽINA + botra Segina = oče h1, h57 OČE MENJAVA + Željko botra, h46 5. VPIS (4. mati varianta), h27 6. VPIS (2. očetov priimek), h41 4. VPIS, h21 2. VPIS ISTA ZVEZA + botra Knekar, h75 3. VPIS ISTA ZVEZA; live verifikacija: knjiga HTTP 200 (inventar 326), citirani skeni 9/9 JPEG 200 (sken 118 samo okvir); skripta scripts/p94_parish_baptism_1899.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1899",
  "P94: PARISH OF PODZEMELJ — BAPTISM REGISTER 04105, THE FULL YEAR 1899 (issue #18; SAMPLE-TRANSCRIPTION-1899; MEASURES, does not decide; the v7 join unchanged): extending the P79 (1886) → … → P92 (1897) → P93 (1898) sample to 1899 — the frame: scans 109 row 97 – 118 row 104 == printed pages 106–115 (the P92 NOVEL CONFIRMED: page == scan − 3 FOR THE WHOLE YEAR — no new duplicates; scan 118 = p. 115 frame only, not cited for entries; the 1899 r1 = Griblje 12 Marija on p. 106 — the new year STARTS with Griblje; 1899 has 104 rows; the 1900 break IN THE MIDDLE of p. 115 = scan 118 row 105 — FOR THE FIRST TIME IN THE SAMPLE the new year does NOT start on a fresh page; the 1900 row 1 = Krasinec — the first time with another village; the P83 novel confirmed for the 12th year); ALL Griblje entries: 15 entries / 15 houses — SQUARE (the 6th year after P87/P89/P91/P92/P93) and THE FIRST YEAR WITHOUT within-year repeats (each house once): 12, 46, 27, 60, 59, 22, 41, 21, 40, 1, 30, 75, 57, 49, 34 — 2 NEW houses (22, 49) + 13 repeats; the cumulative 244 entries / 79 houses across three books and FOURTEEN years (238 vitals); A NEW NUMBER h22 (in the 1825 PT set — ATLAS_HOUSES already contains 22; the first documentary proof; Milek × Klepec A NEW COUPLE — the mother [~ the same person as the h60 godparent Marija Klepac: godparent Mar 13 + mother Mar 20 within a week]) + A NEW GAP NUMBER: h49 (the 19th proven in 41–60 — PT_GAP_KNOWN gains +49; forensics 8x: clearly 49; the gap now 42/50/51) — the gap now has 19 proven; h60 THE SOLID PIN: the 4th ENTRY of the same couple Željko × Brodarič (1893+1894+1897+1899) + the 3rd SAME GODPARENT PAIR Pendirec × Klepac (1893+1894+1899) — the house number under a blue note: channel forensics (the dark '…o 6o') + STRUCTURAL CONFIRMATION (the father + the godparent pair = h60); the ŽELJKO CHAIN's 13th+14th signals (the h60 father + the h57 godparent); the SEGINA CHAIN's 3 signals in one year (the h1 father + the h49 godparent + the h34 godparent); h40 THE THIRD FAMILY IN THREE YEARS: Berkopne (1897) → Brodarič (1898 [~]) → Martin Straus cottager × Barbara Spudič (1899) — STRAUS × SPUDIČ = the CONFIRMATION of the marriage lead 04455; HOUSEHOLD CHANGES: h1 Željko (1888–96) → Segina (the SEGINA CHAIN h70 1893 → h30 1895 → h1 1899 — 3 houses / 6 years), h30 the 4th FAMILY (Milek → Jakljevič 1893 → Šegina 1895 → Janez Županič 1899 — the ŽUPANIČ CLUSTER's 3 signals: h73 1894 + h30 + the godparent Ana Županič), h34 the 2nd FAMILY (Šimec 1887 → Nikolaj Šilak? × Katarina Klobučar), h57 THE FATHER CHANGE Peter Pezdirec (1888–94) → Miha Pozdirec (a brother? a son?; Miha = the h41 1896 godparent); h46 the 5th ENTRY of the same couple (the 4th variant of the mother: Klobučar? → Kramarič? → Harašimovič? → Škaradinič? — the surname Škaradinič confirmed at Krasinec 32); h27 the 6th ENTRY (the father's 2nd reading: Stukar/Stubhar 1893 → Knekar? 1899; the h21 godparent Janez Knekar = a CROSS-LINK); h41 the 4th ENTRY + h21 the 2nd ENTRY of the same couple + h75 the 3rd ENTRY of the same couple (Jakobič × Stubljar, the 4th surname variant); h12 MOTHER CHANGE [~] (Straus 1897 → Cvitkovič 1899; the 1899 godparent = the 1897 mother?! — a possible P92 cell swap); 0 illegitimates; THE MIDWIFE NOVEL CONFIRMED FOR THE 5TH YEAR: 15/15 EMPTY/damaged; INFANT MORTALITY 3/15 (r1 † Jun 25, 99 [~], r26 † May/Jun 2, 99 [~], r94 † Jun 24, 1900) — higher than the P93 1/12; PRIESTS: Šturm (Fr.) 6× + Rauq (Jos.) 4× + Klun (Fr.) 2× BACK from 1897 + 3 illegible (r71 torn, r94/r100 'Jos. Kergo?'); statuses: ½ smallholder × 14 + cottager × 1 (r43 Straus); KURRENT FORENSICS: r13 the house number under a note (channel + structural — 60 SOLID), r26 clearly 22 (NEW), r89 the date DESTROYED (torn edge — ~November per the neighbour), r94 clearly 49 (not 34 — the double forensics with r100), r71 the date correction ('23' + '2' above — probably Oct 2 + baptism Oct 3), r61 the village 'Griblja' variant (the death note CONFIRMS Griblje: † Mar 31, 1975 in Griblje), r25 NOT COUNTED (the registrar overwrote the village+house in black ink — the name Jožef), r27 Berkoviše + r93 'Germ' excluded (other villages); REGISTRAR NOTES of the 20th/21st c. in most entries († 1964/1965/1969/1970s/1975/1984, marriages 1921/1926/1930, the EMŠO block); ANCHORS: h60 THE SOLID PIN (the 4th ENTRY + the 3rd GODPARENT PAIR), h49 A NEW GAP (Brodarič = the h48 1898 godparent → the h49 father), h22 NEW, h40 THE THIRD FAMILY + Straus × Spudič, h1 THE CHANGE + the SEGINA CHAIN, h30 the 4th FAMILY + ŽUPANIČ, h34 the 2nd FAMILY + the godparent Segina = the h1 father, h57 THE FATHER CHANGE + the Željko godparent, h46 the 5th ENTRY (the 4th mother variant), h27 the 6th ENTRY (the 2nd father surname), h41 the 4th ENTRY, h21 the 2nd ENTRY of the same couple + the godparent Knekar, h75 the 3rd ENTRY of the same couple; live verification: the book HTTP 200 (inventory 326), cited scans 9/9 JPEG 200 (scan 118 frame only); the script scripts/p94_parish_baptism_1899.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1899",
  p94Errors.length === 0,
  p94Errors.length === 0
    ? `15 vpisov / 15 hiš — NARE 6. leto, PRVO BREZ ponovitev (15 zasidranih v vitals) · okvir 1899 skeni 109 row 97 – 118 row 104 (novela P92: stran == sken − 3 za celo leto; sken 118 samo okvir; 104 vrstic; prelom 1900 NA SREDINI str. 115 row 105 — prvič ne na novi strani; 1900 row 1 = Krasinec) · NOVA ŠTEVILKA 22 (PT nabor; Milek × Klepec nova zveza — mati = botra h60 [~]) + NOVA LUKNJA ŠTEVILKA 49 (19. dokazana; luknja 42/50/51) · h60 TRDNI PIN (4. VPIS ISTA ZVEZA + 3. ISTA BOTRA PARA; kanalna + strukturna forenzika) · 13 ponovitev · h40 TRETJA DRUŽINA v 3 letih + Straus × Spudič (04455 lead) · menjave h1 (Segina — 3 hiše / 6 let) / h30 4. družina (Županič cluster) / h34 2. družina (Šilak) / h57 oče Peter→Miha Pozdirec · h46 5. VPIS (4. mati varianta) · h27 6. VPIS (Knekar) · h41 4. / h21 2. / h75 3. VPIS ISTA ZVEZA · h12 mati menjava [~] · NOVELA babica 5. leto (15/15) · dojenčijska umrljivost 3/15 · duhovniki Šturm 6× + Rauq 4× + Klun 2× + 3 neberljivih · r25 NEŠTET (matičar črno) · Željko 13.+14. signal + Segina 3 signali`
    : p94Errors.join("; "),
);

// ——— qa-p95: p95 krstna 1900 — širitev vzorca na leto 1900 (issue #18;
//      SAMPLE-TRANSCRIPTION-1900; celoven neodvisen preracun iz bundled
//      virov: HOUSE_VITALS × PARISH_BOOKS; PT klasifikacija iz pinov;
//      NOVELA P92 potrjena: stran == sken − 3 ZA CELO LETO (brez novih
//      duplikatov; sken 122 = str. 119 starševska stran — citiran v dokazu
//      za starše r45/r46, brez data vpisov v vitals; sken 125 = str. 122 =
//      glava 1901, samo okvir); okvir skeni 118 row 105 (SREDINA str. 115,
//      P94 dokazano) – 124 row 77 == str. 115–121; 77 vrstic; sken 121 =
//      2 podatkovna panela (r33–44 + r45–56), sken 122 = 2 starševska
//      panela; r51–56 FIZIČNO RAZTRGANE; 16 vpisov / 16 hiš — NARE 7. leto,
//      2. leto brez znotraj-letnih ponovitev; NOVA HIŠA 67 (prvi matrični
//      dokaz — Straus gumbar; 80. hiša vzorca); NOVELA babica: stolpec
//      PRVIČ IZPOLNJEN (Fottre 7× + Hrižan + Foča?; 6 praznih + 2 neberljiv
//      /raztrgan); Šturm 0× PRVIČ — Rauq 9× + Perg 4× + Klunček 2×;
//      h1 ŽELJKO VRNITEV (boter 1888 → oče 1900); h31 6. PIN (najdaljša
//      zveza vzorca); h45 3. PIN Straus × Spudič (04455 lead 3× krstno);
//      h90 4. PIN šolska hiša (Leopoldina po materi); h23 4. PIN + Debič?
//      REŠENO; h14 1896 MERI dvom REŠUJE; h58 PRVA MENJAVA ŽENE; scoping
//      4 popravki (r5→r3, r8→r6, r27→r28…r30→r31, 4 izpuščene + r49 ZAVRŽEN)
const p95Hv = HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year === 1900);
const p95Errors: string[] = [];
const P95_PT_IN_SET = ["1", "9", "10", "14", "16", "20", "23", "25", "31", "32", "65", "67", "90"];
const P95_PT_GAP = ["45", "54", "58"];
if (p95Hv.length !== 16)
  p95Errors.push(`vpisov 1900 (04105, zasidrani) ≠ 16 (${p95Hv.length})`);
const p95Houses = new Set(p95Hv.map((h) => h.houseNo));
if (p95Houses.size !== 16)
  p95Errors.push(`različnih hiš ≠ 16 (${p95Houses.size}: ${[...p95Houses].sort((a, b) => Number(a) - Number(b)).join(",")})`);
// okvir 1900: skeni 118–124; stran == sken − 3 za celo leto (novela P92);
// sken 122 = starševska stran (v dokazu citiran, brez data vpisov);
// sken 125 = glava 1901, ni citiran
const p95Bad = p95Hv.filter(
  (h) => h.status !== "DOCUMENTED" || !h.scan || !h.page
    || h.page !== h.scan - 3
    || h.scan < 118 || h.scan > 124,
);
if (p95Bad.length > 0)
  p95Errors.push(`okvir 1900: skeni 118–124 ali stran ≠ sken − 3 krščeno pri ${p95Bad.length}`);
if (p95Hv.some((h) => h.scan === 122))
  p95Errors.push("sken 122 (str. 119, starševska stran) ni citiran v data vpisih");
// NOVELA babica: 6 PRAZNIH + 8 imenovanih (Fottre 7× + Hrižan 1×) + 2 neberljiv/raztrgan
const p95BabPrazna = p95Hv.filter((h) => h.whatSi.includes("babica PRAZNA"));
const p95BabNamed = p95Hv.filter((h) => /babica (Margareta Fottre|Marjeta Fottre|Margareta Foča|Ana Hrižan)/.test(h.whatSi));
if (p95BabPrazna.length !== 6 || p95BabNamed.length !== 8)
  p95Errors.push(`NOVELA babica: praznih ≠ 6 (${p95BabPrazna.length}) ali imenovanih ≠ 8 (${p95BabNamed.length})`);
// NOVA HIŠA 67: blok h67 mora imeti NOVA HIŠA + prvi matrični dokaz + 80. hiša + Straus + gumbar
const p95H67 = p95Hv.find((h) => h.houseNo === "67");
if (!p95H67 || !p95H67.whatSi.includes("NOVA HIŠA VZORCA") || !p95H67.whatSi.includes("prvi matrični dokaz") || !p95H67.whatSi.includes("80. hiša vzorca") || !p95H67.whatSi.includes("gumbar"))
  p95Errors.push("NOVA HIŠA 67 / prvi matrični dokaz / 80. hiša / Straus gumbar: whatSi ≠ P95 (pin manjka)");
// h1 ŽELJKO VRNITEV (boter 1888 → oče 1900)
const p95H1 = p95Hv.find((h) => h.houseNo === "1");
if (!p95H1 || !p95H1.whatSi.includes("ŽELJKO VRNITEV") || !p95H1.whatSi.includes("BOTER h1 1888"))
  p95Errors.push("h1 ŽELJKO VRNITEV / BOTER h1 1888: whatSi ≠ P95 (pin manjka)");
// h31 6. PIN — najdaljša zaporedna zveza vzorca
const p95H31 = p95Hv.find((h) => h.houseNo === "31");
if (!p95H31 || !p95H31.whatSi.includes("6. PIN ISTA ZVEZA") || !p95H31.whatSi.includes("najdaljša zaporedna zveza"))
  p95Errors.push("h31 6. PIN ISTA ZVEZA / najdaljša zveza: whatSi ≠ P95 (pin manjka)");
// h45 3. PIN Straus × Spudič + 04455 poročni lead
const p95H45 = p95Hv.find((h) => h.houseNo === "45");
if (!p95H45 || !p95H45.whatSi.includes("3. PIN ISTA ZVEZA") || !p95H45.whatSi.includes("04455"))
  p95Errors.push("h45 3. PIN ISTA ZVEZA / 04455: whatSi ≠ P95 (pin manjka)");
// h90 šolska hiša 4. PIN — Leopoldina po materi Leopoldi
const p95H90 = p95Hv.find((h) => h.houseNo === "90");
if (!p95H90 || !p95H90.whatSi.includes("ŠOLSKA HIŠA") || !p95H90.whatSi.includes("4. PIN") || !p95H90.whatSi.includes("Vetročnik") || !p95H90.whatSi.includes("Leopoldina"))
  p95Errors.push("h90 ŠOLSKA HIŠA / 4. PIN / Vetročnik / Leopoldina: whatSi ≠ P95 (pin manjka)");
// h23 4. PIN + Debič? REŠENO z 1900 forenziko
const p95H23 = p95Hv.find((h) => h.houseNo === "23");
if (!p95H23 || !p95H23.whatSi.includes("4. PIN ISTA ZVEZA") || !p95H23.whatSi.includes("REŠENO"))
  p95Errors.push("h23 4. PIN ISTA ZVEZA / Debič REŠENO: whatSi ≠ P95 (pin manjka)");
// h58 5. PIN + PRVA MENJAVA ŽENE (Dragoš → Kranbič)
const p95H58 = p95Hv.find((h) => h.houseNo === "58");
if (!p95H58 || !p95H58.whatSi.includes("5. PIN") || !p95H58.whatSi.includes("MENJAVA ŽENE") || !p95H58.whatSi.includes("Kranbič"))
  p95Errors.push("h58 5. PIN / MENJAVA ŽENE / Kranbič: whatSi ≠ P95 (pin manjka)");
// sidra (16 vpisov)
const p95Anchor = (hn: string, scan: number, pins: string[], label: string) => {
  const blk = p95Hv.find((h) => h.houseNo === hn && h.scan === scan);
  if (!blk || !pins.every((p) => blk.whatSi.includes(p)))
    p95Errors.push(`sidro ${label}: whatSi ≠ P95 (${pins.join(" + ")})`);
};
p95Anchor("1", 118, ["Željko", "Kure", "ŽELJKO VRNITEV"], "hiša 1");
p95Anchor("67", 118, ["Straus", "gumbar", "NOVA HIŠA VZORCA"], "hiša 67");
p95Anchor("10", 119, ["Grabrijan", "Pozdirec", "MENJAVA GOSPODINJSTVA"], "hiša 10");
p95Anchor("32", 119, ["Meh", "8. PIN", "KURRENT U/M"], "hiša 32");
p95Anchor("65", 120, ["Milek", "Tožek", "6. VPIS ISTI OČE"], "hiša 65");
p95Anchor("20", 120, ["Pendirec", "Klepec", "3. PIN"], "hiša 20");
p95Anchor("14", 120, ["Brinec", "REŠUJE P91"], "hiša 14");
p95Anchor("90", 120, ["Vetročnik", "Schmelzer", "ŠOLSKA HIŠA"], "hiša 90");
p95Anchor("23", 120, ["Brinec", "Dehlič", "4. PIN ISTA ZVEZA"], "hiša 23");
p95Anchor("9", 121, ["Muc", "Kure", "MENJAVA GOSPODINJSTVA"], "hiša 9");
p95Anchor("54", 121, ["RAZTRGANI", "starši neznani"], "hiša 54");
p95Anchor("16", 121, ["Novak", "Šilak", "MENJAVA"], "hiša 16");
p95Anchor("58", 121, ["Požek", "Kranbič", "MENJAVA ŽENE"], "hiša 58");
p95Anchor("31", 123, ["Papič", "Straus", "6. PIN ISTA ZVEZA"], "hiša 31");
p95Anchor("25", 123, ["Brinec", "Segina", "MENJAVA"], "hiša 25");
p95Anchor("45", 124, ["Straus", "Spudič", "04455"], "hiša 45");
// PT klasifikacija == pin: 13 v naboru + 3 v luknji (45/54/58 — vsi že dokazani;
// h58 NI v PT verigi — PT_GAP_KNOWN že vsebuje 58; 42/50/51 ostajajo)
const p95InSet = [...p95Houses].filter((h) => P95_PT_IN_SET.includes(h));
const p95Gap = [...p95Houses].filter((h) => P95_PT_GAP.includes(h));
if (p95InSet.length !== 13 || p95Gap.length !== 3)
  p95Errors.push(`PT klasifikacija ≠ 13/3 (${p95InSet.length}/${p95Gap.length})`);
if (p95Gap.some((h) => !(Number(h) >= 41 && Number(h) <= 60)))
  p95Errors.push("luknjane hiše izven 41–60");
// NOVA hiša 1900 (67) — ne obstaja v nobenem prejšnjem letu/knjigi
for (const hn of ["67"]) {
  if (HOUSE_VITALS.some((v) => v.houseNo === hn && !(v.bookSignature === "04105" && v.year === 1900) && !(v.bookSignature === "04455" && v.year === 1898))) // P127: + poročni blok h67-1898 (v7 nevesta Maria JAKOFČIČ — PRED krsto 1900, vzorec qa-p91 h14!)
    p95Errors.push(`NOVA hiša ${hn} (P95) že obstaja v prejšnjem letu — pini neskladni`);
}
// kontinuitete čez leta prek HOUSE_VITALS (klasifikacija zgodovinska —
// poznejši bloki ne spreminjajo pričakovanih priorov)
// oblika: [hiša, leto, knjiga, whatSi-pin ALI "" za scan-pin, pričakovani sken]
const P95_CONTINUITY: Array<[string, number, string, string, number | null]> = [
  ["1", 1888, "04105", "Zeljth", null], ["1", 1892, "04105", "Željko", null], ["1", 1896, "04105", "Željko", null], ["1", 1899, "04105", "Segina", null],
  ["31", 1887, "04105", "Papič", null], ["31", 1890, "04105", "Papič", null], ["31", 1894, "04105", "Papič", null], ["31", 1897, "04105", "Straus", null], // 1897 Kurrent Sapič?/Straus? (2 vpisa — obe mati Straus)
  ["45", 1896, "04105", "Straus", null], ["45", 1897, "04105", "Spudič", null],
  ["90", 1890, "04105", "Kopitar", null], ["90", 1898, "04105", "Vetročnik", null],
  ["23", 1893, "04105", "Debič", null], ["23", 1897, "04105", "Brinec", null],
  ["20", 1897, "04105", "Pendirec", null],
  ["58", 1889, "04105", "Požek", null], ["58", 1895, "04105", "Dragoš", null],
  ["32", 1889, "04105", "Urh", null], ["32", 1893, "04105", "Meh/Mrh", null],
  ["65", 1887, "04105", "Milek", null], ["65", 1897, "04105", "Mihek", null],
  ["14", 1896, "04105", "Brinec", null],
  ["9", 1896, "04105", "Jakobič", null],
  ["10", 1897, "04105", "Brinec", null],
  ["16", 1897, "04105", "Jaklič", null],
  ["25", 1893, "04105", "Hrižan", null], ["25", 1896, "04105", "Klepec", null],
  ["54", 1897, "04105", "Šutala", null],
];
for (const [hn, yr, sig, pin, sc] of P95_CONTINUITY) {
  const blk = HOUSE_VITALS.find((v) => v.houseNo === hn && v.bookSignature === sig && v.year === yr);
  const ok = blk && (pin === "" ? blk.scan === sc : HOUSE_VITALS.some((v) => v.houseNo === hn && v.bookSignature === sig && v.year === yr && v.whatSi.includes(pin)));
  if (!ok)
    p95Errors.push(`kontinuiteta hiša ${hn} (${yr}, ${sig}, pin ${pin || `sk ${sc}`}) manjka ali pin ne ustreza`);
}
// vitals skupaj 449 (po P106: 429 + 20; krstna 1911)
if (HOUSE_VITALS.length !== 685)
  p95Errors.push(`HOUSE_VITALS ≠ 467 (${HOUSE_VITALS.length})`);
push(
  "qa-p95-parish-baptism-1900",
  "P95: ŽUPNIJA PODZEMELJ — KRSTNA KNJIGA 04105, POLNO LETO 1900 (issue #18; SAMPLE-TRANSCRIPTION-1900; MERI, NE odloča; v7 join nespremenjen): širitev vzorca P79 (1886) → … → P93 (1898) → P94 (1899) na leto 1900 — okvir: skeni 118 row 105 (SREDINA str. 115 — novo leto se začne NA SREDINI strani, P94 dokazano) – 124 row 77 == tiskane strani 115–121 (NOVELA P92 POTRJENA: stran == sken − 3 ZA CELO LETO — brez novih duplikatov; sken 122 = str. 119 starševska stran — citiran v dokazu za starše r45/r46, brez data vpisov; sken 125 = str. 122 = glava 1901, samo okvir; 1900 r1 = Krasinec Matija — PRVIČ se novo leto začne z DRUGO VASJO; leto 1900 ima 77 vrstic; sken 121 = DVA podatkovna panela (r33–44 levo + r45–56 desno), sken 122 = DVA starševska panela; vrstice r51–56 FIZIČNO RAZTRGANE — podatki izgubljeni, starši znani) — VSI vpisi z Griblji: 16 vpisov / 16 hiš — NARE (7. leto po P87/P89/P91/P92/P93/P94) in 2. LETO BREZ znotraj-letnih ponovitev (vsaka hiša 1×): 1, 67, 10, 32, 65, 20, 14, 90, 23, 9, 54, 16, 58, 31, 25, 45 — 1 NOVA hiša (67) + 15 ponovitev; kumulativ 260 vpisov / 80 hiš čez tri knjige in PETNAEST let (254 vitals); NOVA HIŠA h67 (prvi matrični dokaz; hiša v PT naboru 1825 — ATLAS_HOUSES vsebuje 67 v bloku 61–99; 80. hiša vzorca; STRAUS gumbar mreža — h45 Martin Straus, h31 mati Straus, botri Straus); scoping POPRAVKI: r5→r3 + r8→r6 (margini str. 115 raztrgani — 8 vrstic, BREZ ANOMALIJE; scopingova hipoteza o 2 nenumeriranih vrsticah ZAVRŽENA) + r27→r28…r30→r31 (scoping izpustil r27 Otok 8) + 4 IZPUŠČENE vrstice najdene (r45 h16, r46 h58, r59 h31, r63 h25 — celostranski pregled 1900) + scopingov r49 »Griblje 51 NOVA LUKNJA« ZAVRŽEN (Primostek 5!) — luknja 42/50/51 NESPREMENJENA (19 dokazanih v 41–60); PT 13/3 (45/54/58 v luknji — vsi že dokazani; 58 NI v PT verigi — PT_GAP_KNOWN že vsebuje 58); NOVELA babica: stolpec PRVIČ IZPOLNJEN po 15 letih (1886–99 prazen!) — Fottre/Foča 7× + Hrižan 1× + 6 praznih + 2 neberljiv/raztrgan; DUHOVNIKI: Šturm 0× — PRVIČ V VZORCU! + Rauq 9× + Perg 4× + Klunček 2× (nov duhovnik) + 1 neberljiv; h1 ŽELJKO VRNITEV: 1888–96 Nikolaj Željko × Katarina Kure → 1899 Segina → 1900 Jurij Željko × Barbara Kure — Jurij Željko = BOTER h1 1888 → OČE 1900 (ŽELJKO signal 15); h31 6. PIN ISTA ZVEZA Martin Papič × Marjeta Straus (1887+1890+1891+1894+1897+1900 — najdaljša zaporedna zveza vzorca; 11. vpis); h45 3. PIN ISTA ZVEZA Martin Straus × Barbara Spudič (1896+1897+1900) — 04455 POROČNI LEAD: krstno 3× POTRJENA ista zveza — iskati poroko v 04455; h90 ŠOLSKA HIŠA 4. PIN: ISTA UČITELJSKA DRUŽINA Vetročnik × Schmelzer (1898 r27 Alojzij) — hči Leopoldina po materi Leopoldi!; učitelji: Kopitar (1890–92) → Vetročnik (1898–1900); KONFLIKT DATUMA r30: vrstica »40 jun« [~] vs matičarjev EMŠO 2405900505109 = roj. 24.05.1900 — MERI: EMŠO avtoritativno; h23 4. PIN ISTA ZVEZA Brinec × Dehlič (1893+1894+1897+1900) — P88 1893 »Debič?« = Dehlič REŠENO z 1900 forenziko; h14 2. VPIS — 1896 (P91) oče MERI dvom (»ali drug Janez Brinec?«) → 1900 forenzika REŠUJE P91; h58 5. PIN + PRVA MENJAVA ŽENE na h58 (1889–95 Ana Dragoš → 1900 Katarina Kranbič); h32 8. PIN — 1893 (P88) »Meh/Mrh?« POTRJENO z 1900 »Meh« (KURRENT U/M varianta ALI menjava — MERI); h65 6. VPIS ISTI OČE Matija [Milek] (1887–1900) + 5. varianta matere (Tožek?); h20 3. PIN Pendirec × Klepec (1897+1900); h10/h9/h16/h25 MENJAVE GOSPODINJSTEV (Grabrijan × Pozdirec; Muc × Kure; Novak × Šilak — ŠILAK križni sklic 1886 mrliška; Brinec × Segina — SEGINA signal 4); h54 starši RAZTRGANI (sken 122 levo odtrgan — edina izguba staršev med Griblje vpisi 1900); r19 dnevi FIZIČNO RAZTRGANI + mati IME PREČRTANO; pripis »Umrla dne 14.3.1954« pripisnost r30/r31 dvomna (MERI: po položaju črte r31); DOJENČIJSKA UMRLJIVOST 5/16 (r3 † 1907 ~7 let, r23 † 2/6.00 ~1 mesec, r45 † 7/11.02, r46 † 8/5.03, r69 † 9/2.03 ~15 mesecev); EMŠO blok matičarja (r6/r28/r31 — vsi ujemajo z vrsticami!); MATIČAR PRIPISI v 13/16 vpisov († 1954/1955/1965/1969?/1977/1980/1982/1984/1985/1991, poroke 1921/1933/19??); SIDRA: h67 NOVA (Straus gumbar), h1 ŽELJKO VRNITEV, h31 6. PIN, h45 3. PIN + 04455, h90 4. PIN šolska, h23 4. PIN + Dehlič REŠENO, h14 REŠUJE P91, h58 MENJAVA ŽENE, h32 8. PIN Meh, h65 6. VPIS, h20 3. PIN, h10/h9/h16/h25 menjave, h54 RAZTRGANI; live verifikacija: knjiga HTTP 200 (inventar 326), citirani skeni 7/7 JPEG 200 (sken 122 = starševska stran brez data vpisov; sken 125 = glava 1901 ni citiran); skripta scripts/p95_parish_baptism_1900.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1900",
  "P95: PARISH OF PODZEMELJ — BAPTISM REGISTER 04105, THE FULL YEAR 1900 (issue #18; SAMPLE-TRANSCRIPTION-1900; MEASURES, does not decide; the v7 join unchanged): extending the P79 (1886) → … → P93 (1898) → P94 (1899) sample to 1900 — the frame: scans 118 row 105 (the MIDDLE of p. 115 — the new year starts IN THE MIDDLE of the page, proven by P94) – 124 row 77 == printed pages 115–121 (the P92 NOVEL CONFIRMED: page == scan − 3 FOR THE WHOLE YEAR — no new duplicates; scan 122 = p. 119 the parents page — cited in the evidence for the parents of r45/r46, no data entries; scan 125 = p. 122 = the 1901 heading, frame only; the 1900 r1 = Krasinec Matija — FOR THE FIRST TIME the new year starts with ANOTHER VILLAGE; 1900 has 77 rows; scan 121 = TWO data panels (r33–44 left + r45–56 right), scan 122 = TWO parents panels; rows r51–56 PHYSICALLY TORN — the data lost, the parents known); ALL Griblje entries: 16 entries / 16 houses — SQUARE (the 7th year after P87/P89/P91/P92/P93/P94) and the 2nd YEAR WITHOUT within-year repeats (each house once): 1, 67, 10, 32, 65, 20, 14, 90, 23, 9, 54, 16, 58, 31, 25, 45 — 1 NEW house (67) + 15 repeats; the cumulative 260 entries / 80 houses across three books and FIFTEEN years (254 vitals); THE NEW HOUSE h67 (the first documentary proof; the house in the 1825 PT set — ATLAS_HOUSES contains 67 in the 61–99 block; the 80th house of the sample; the STRAUS cooper web — h45 Martin Straus, h31 mother Straus, Straus godparents); the scoping CORRECTIONS: r5→r3 + r8→r6 (the margins of p. 115 torn — 8 rows, NO ANOMALY; the scoping hypothesis of 2 unnumbered rows REJECTED) + r27→r28…r30→r31 (the scoping missed r27 Otok 8) + 4 OMITTED rows found (r45 h16, r46 h58, r59 h31, r63 h25 — the full-page survey of 1900) + the scoping r49 'Griblje 51 NEW GAP' REJECTED (Primostek 5!) — the gap 42/50/51 UNCHANGED (19 proven in 41–60); the PT 13/3 (45/54/58 in the gap — all proven earlier; 58 is NOT in the PT chain — PT_GAP_KNOWN already contains 58); THE MIDWIFE NOVEL: the column FILLED IN FOR THE FIRST TIME after 15 years (1886–99 empty!) — Fottre/Foča 7× + Hrižan 1× + 6 empty + 2 illegible/torn; PRIESTS: Šturm 0× — FOR THE FIRST TIME IN THE SAMPLE! + Rauq 9× + Perg 4× + Klunček 2× (a new priest) + 1 illegible; h1 THE ŽELJKO RETURN: 1888–96 Nikolaj Željko × Katarina Kure → 1899 Segina → 1900 Jurij Željko × Barbara Kure — Jurij Željko = the h1 1888 GODPARENT → the 1900 FATHER (the ŽELJKO signal 15); h31 the 6th PIN of the same couple Martin Papič × Marjeta Straus (1887+1890+1891+1894+1897+1900 — the sample's longest consecutive couple; the 11th entry); h45 the 3rd PIN of the same couple Martin Straus × Barbara Spudič (1896+1897+1900) — the 04455 MARRIAGE LEAD: the same couple christened 3× CONFIRMED — look for the marriage in 04455; h90 THE SCHOOL HOUSE the 4th PIN: the SAME TEACHER FAMILY Vetročnik × Schmelzer (1898 r27 Alojzij) — the daughter Leopoldina after her mother Leopolda!; the teachers: Kopitar (1890–92) → Vetročnik (1898–1900); THE DATE CONFLICT r30: the row '40 jun' [~] vs the registrar's EMŠO 2405900505109 = born May 24, 1900 — MERI: the EMŠO is authoritative; h23 the 4th PIN of the same couple Brinec × Dehlič (1893+1894+1897+1900) — the P88 1893 'Debič?' = Dehlič RESOLVED by the 1900 forensics; h14 the 2nd ENTRY — 1896 (P91) the father MERI doubt ('another Janez Brinec?') → the 1900 forensics RESOLVES P91; h58 the 5th PIN + the FIRST WIFE CHANGE at h58 (1889–95 Ana Dragoš → 1900 Katarina Kranbič); h32 the 8th PIN — the 1893 (P88) 'Meh/Mrh?' CONFIRMED by the 1900 'Meh' (a KURRENT U/M variant OR a change — MERI); h65 the 6th ENTRY of the same FATHER Matija [Milek] (1887–1900) + the 5th variant of the mother (Tožek?); h20 the 3rd PIN Pendirec × Klepec (1897+1900); h10/h9/h16/h25 HOUSEHOLD CHANGES (Grabrijan × Pozdirec; Muc × Kure; Novak × Šilak — the ŠILAK cross-link with the 1886 death register; Brinec × Segina — the SEGINA signal 4); h54 the parents TORN AWAY (scan 122 left torn off — the only loss of parents among the 1900 Griblje entries); r19 the days PHYSICALLY TORN + the mother's NAME CROSSED OUT; the note 'Umrla dne 14.3.1954' attributed to r30/r31 doubtfully (MERI: by the line position r31); INFANT MORTALITY 5/16 (r3 † 1907 ~7 years, r23 † Jun 2, 1900 ~1 month, r45 † Feb/Nov 7, 1902, r46 † May 8, 1903, r69 † Feb 9, 1903 ~15 months); the registrar's EMŠO block (r6/r28/r31 — all matching the rows!); REGISTRAR NOTES in 13/16 entries († 1954/1955/1965/1969?/1977/1980/1982/1984/1985/1991, marriages 1921/1933/19??); ANCHORS: h67 NEW (the Straus cooper), h1 THE ŽELJKO RETURN, h31 the 6th PIN, h45 the 3rd PIN + 04455, h90 the 4th PIN school, h23 the 4th PIN + Dehlič RESOLVED, h14 RESOLVES P91, h58 the WIFE CHANGE, h32 the 8th PIN Meh, h65 the 6th ENTRY, h20 the 3rd PIN, h10/h9/h16/h25 the changes, h54 TORN; live verification: the book HTTP 200 (inventory 326), cited scans 7/7 JPEG 200 (scan 122 = the parents page without data entries; scan 125 = the 1901 heading not cited); the script scripts/p95_parish_baptism_1900.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1900",
  p95Errors.length === 0,
  p95Errors.length === 0
    ? `16 vpisov / 16 hiš — NARE 7. leto, 2. BREZ ponovitev (16 zasidranih v vitals) · okvir 1900 skeni 118 row 105 (SREDINA str. 115) – 124 row 77 (novela P92: stran == sken − 3; sken 122 = starševska stran; sken 125 = glava 1901; 77 vrstic; sken 121 = 2 podatkovna panela; r51–56 RAZTRGANE) · 1900 r1 = Krasinec — PRVIČ druga vas · NOVA HIŠA 67 (prvi matrični dokaz — Straus gumbar; 80. hiša) · scoping 4 popravki + 4 izpuščene vrstice + r49 »h51« ZAVRŽEN (Primostek 5) · PT 13/3 (45/54/58 že dokazani; luknja 42/50/51 nespremenjena) · NOVELA babica PRVIČ izpolnjena po 15 letih (Fottre 7× + Hrižan) · Šturm 0× PRVIČ — Rauq 9× + Perg 4× + Klunček 2× · h1 ŽELJKO VRNITEV (boter 1888 → oče; signal 15) · h31 6. PIN (najdaljša zveza 1887–1900) · h45 3. PIN Straus × Spudič (04455 lead 3× krstno) · h90 4. PIN šolska (Leopoldina po materi) · h23 4. PIN + Debič? REŠENO · h14 REŠUJE P91 · h58 PRVA MENJAVA ŽENE (Dragoš → Kranbič) · h32 8. PIN Meh POTRJENO · h65 6. VPIS ISTI OČE + 5. mati varianta · h20 3. PIN · menjave h10/h9/h16/h25 (ŠILAK križni sklic; SEGINA signal 4) · h54 starši RAZTRGANI · r30 KONFLIKT DATUMA (EMŠO avtoritativno) · umrljivost 5/16 · EMŠO blok 3× ujema`
    : p95Errors.join("; "),
);

// ——— qa-p96: p96 krstna 1901 — širitev vzorca na leto 1901 (issue #18;
//      SAMPLE-TRANSCRIPTION-1901; celoven neodvisen preracun iz bundled
//      virov: HOUSE_VITALS × PARISH_BOOKS; PT klasifikacija iz pinov;
//      NOVELA P96: TRIJE podvojeni skeni (127/128, 129/130, 133/134) —
//      sken 128 = str. 124 z nalepkama PREPOGNJENIMA → r32/r33 rešeni
//      (Juni 1/2 Primostek 2 EMŠO 01.06.1901 + Gradac 32?/33? Jožef);
//      stran == sken − 3 (125–127) / − 4 (129–130 → 125) / − 5 (131–132 →
//      126–127) / − 6 (135 → 129); okvir: glava »1901.« sredina str. 122
//      (sken 125, P95 dokazano) – row 87 str. 129 (sken 135; glava »1902«
//      na dnu iste strani); 87 vrstic; NOVELA formata: od str. 125 celo-
//      spread (leva podatkovna + desna roditelja/boter/babica/podpis);
//      NOVELA mesecev: r65–r69 NOVEMBER (EMŠO r66 08.11.1901 + r68
//      16.11.1901), December od r70; r36 »Jurij«? = JUNI (sekvence r39
//      July 10); 10 vpisov / 9 hiš — h12 ×2 = PRVA PONOVITEV znotraj leta
//      po 1893 (NARE 1894–1900 prekinjeno; r1 Juvan? × Cvetkovič vs r36
//      Straus × Jakobič — več-družinska hiša); NOVA HIŠA 19 (prvi matrični
//      dokaz; oče bajtar; 81. hiša); h44 + h54 v PT luknji (že v
//      PT_GAP_KNOWN); DUHOVNIKI: Kulbinek? 7× (= P95 »Klunček?«, boljše
//      branje) + Rauq 2× + NOV podpis Fran. Dostál (češko); babica Toter
//      6× (oče r48 Jakob Toter = njena rodbina!) — 10/10 imenovanih;
//      excluded: r35 (Griblje [~], hiša pod trakom) + r47 (nalepka
//      26.01.1989 — Straus × Jakobič, možen Griblje)
const p96Hv = HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year === 1901);
const p96Errors: string[] = [];
const P96_PT_IN_SET = ["2", "7", "12", "17", "19", "24", "65"];
const P96_PT_GAP = ["44", "54"];
if (p96Hv.length !== 10)
  p96Errors.push(`vpisov 1901 (04105, zasidrani) ≠ 10 (${p96Hv.length})`);
const p96Houses = new Set(p96Hv.map((h) => h.houseNo));
if (p96Houses.size !== 9)
  p96Errors.push(`različnih hiš ≠ 9 (${p96Houses.size}: ${[...p96Houses].sort((a, b) => Number(a) - Number(b)).join(",")})`);
// okvir 1901: skeni 125–134 (135 = row 87 + glava 1902, v okviru, brez data vpisa);
// stran == novela P96 (trije dup pari)
const p96PageOfScan = (s: number) =>
  s === 133 || s === 134 ? 128 : s === 128 ? 124 : s <= 127 ? s - 3 : s <= 130 ? 125 : s <= 133 ? s - 5 : s - 6;
const p96Bad = p96Hv.filter(
  (h) => h.status !== "DOCUMENTED" || !h.scan || !h.page
    || h.page !== p96PageOfScan(h.scan)
    || h.scan < 125 || h.scan > 134,
);
if (p96Bad.length > 0)
  p96Errors.push(`okvir 1901: skeni 125–134 ali stran ≠ novela P96 krščeno pri ${p96Bad.length}`);
// h12 ×2 (prva ponovitev po 1893) + NOVA hiša 19
if (!p96Houses.has("12")) p96Errors.push("h12 (6.+7. VPIS — prva ponovitev po 1893) manjka");
if (!p96Houses.has("19")) p96Errors.push("NOVA hiša 19 manjka");
// kontinuitete (zadnja leta pred 1901; pini po očetu/botru)
const p96Pins: Array<[string, number, string]> = [
  ["2", 1897, "Tome"],
  ["7", 1890, "Toter"],
  ["12", 1899, "Toter"],
  ["17", 1894, "Kralj"],
  ["24", 1897, "Božek"],
  ["44", 1888, "Jurajevič"],
  ["54", 1900, "Butala"],
  ["65", 1900, "Pošek"],
];
for (const [hn, yr, pin] of p96Pins) {
  const prior = HOUSE_VITALS.find((h) => h.bookSignature === "04105" && h.houseNo === hn && h.year === yr);
  const cur = p96Hv.find((h) => h.houseNo === hn);
  if (!prior || !cur) {
    p96Errors.push(`kontinuiteta hiša ${hn} (${yr} → 1901) manjka`);
    continue;
  }
  if (!cur.whatSi.includes(pin))
    p96Errors.push(`kontinuiteta hiša ${hn} (${yr}, pin ${pin}) ne ustreza`);
}
// NOVA hiša 19: brez predhodnikov v katerikoli knjigi (P101: + 1906 blok h19 — 2. VPIS NEZAKONSKI; P107: + 1912 blok h19 — 5. VPIS; P136: + poročni blok h19-1907 — 1. POROČNI DOKAZ NOVE hiše! v4 ženin Nikolaus Hranc [~])
if (HOUSE_VITALS.some((h) => h.houseNo === "19" && !(h.bookSignature === "04105" && (h.year === 1901 || h.year === 1906 || h.year === 1912)) && !(h.bookSignature === "04455" && h.year === 1907)))
  p96Errors.push("NOVA hiša 19 že obstaja v prejšnjem letu — pini neskladni");
// vitals skupaj 449 (po P106: 429 + 20; krstna 1911)
if (HOUSE_VITALS.length !== 685)
  p96Errors.push(`HOUSE_VITALS ≠ 467 (${HOUSE_VITALS.length})`);
// babica: 10/10 imenovanih; Toter 6×
if (p96Hv.filter((h) => h.whatSi.includes("babica")).length !== 10)
  p96Errors.push("babica ni v vseh 10 whatSi (10/10 imenovanih)");
if (p96Hv.filter((h) => h.whatSi.includes("babica Marjeta Toter")).length !== 6)
  p96Errors.push(`babica Marjeta Toter ≠ 6× (${p96Hv.filter((h) => h.whatSi.includes("babica Marjeta Toter")).length})`);
// duhovniki: Kulbinek? 7× + Jos. Rauq 2× + Fran. Dostál 1× (NOV)
if (p96Hv.filter((h) => h.whatSi.includes("Kulbinek?")).length !== 7)
  p96Errors.push(`podpis Kulbinek? ≠ 7× (${p96Hv.filter((h) => h.whatSi.includes("Kulbinek?")).length})`);
if (p96Hv.filter((h) => h.whatSi.includes("Jos. Rauq")).length !== 2)
  p96Errors.push(`podpis Jos. Rauq ≠ 2× (${p96Hv.filter((h) => h.whatSi.includes("Jos. Rauq")).length})`);
if (p96Hv.filter((h) => h.whatSi.includes("Fran. Dostál")).length !== 1)
  p96Errors.push("NOV podpis Fran. Dostál ≠ 1×");
// EMŠO sidra (r48 21.07.1901 + r59 11.10.1901)
if (!p96Hv.some((h) => h.whatSi.includes("2107901505598")))
  p96Errors.push("EMŠO sidro r48 (21.07.1901) manjka");
if (!p96Hv.some((h) => h.whatSi.includes("1110901503024")))
  p96Errors.push("EMŠO sidro r59 (11.10.1901) manjka");
push(
  "qa-p96-parish-baptism-1901",
  "P96: ŽUPNIJA PODZEMELJ — KRSTNA KNJIGA 04105, POLNO LETO 1901 (issue #18; SAMPLE-TRANSCRIPTION-1901; MERI, NE odloča; v7 join nespremenjen): širitev vzorca P79 (1886) → … → P94 (1899) → P95 (1900) na leto 1901 — okvir: glava »1901.« na sredini str. 122 (sken 125, P95 dokazano) – row 87 na str. 129 (sken 135; glava »1902« na dnu iste strani) == tiskane strani 122–129 (87 vrstic); NOVELA P96: TRIJE podvojeni skeni (127/128, 129/130, 133/134) — sken 128 = str. 124 z nalepkama PREPOGNJENIMA → r32/r33 REŠENI (Juni 1/2 Primostek 2 Anton EMŠO 01.06.1901 + Gradac 32?/33? Jožef EMŠO 01.06.1901; nalepki 1989 = † Zagreb/Črnomelj); stran == sken − 3 (125–127) / − 4 (129–130 → 125) / − 5 (131–132 → 126–127) / − 6 (135 → 129); NOVELA formata: od str. 125 celo-spread fotografije (leva podatkovna + desna roditelja/boter/babica/podpis — poravnava po y-pasovih); NOVELA mesecev: r65–r69 NOVEMBER (EMŠO r66 08.11.1901 + r68 16.11.1901) — December se začne na r70; r36 »Jurij«? = JUNI (sekvence r39 July 10 vsili); VSI vpisi z Griblji: 10 vpisov / 9 hiš: 12, 12, 7, 54, 2, 17, 65, 24, 19, 44 — h12 ×2 = PRVA PONOVITEV znotraj leta po 1893 (NARE 1894–1900 prekinjeno po 8 letih; r1 Gregor Juvan? × Barbura Cvetkovič vs r36 Matija Straus × Marija Jakobič — več-družinska hiša/menjava) — 1 NOVA hiša (19) + 8 ponovitev; kumulativ 270 vpisov / 81 hiš čez tri knjige in ŠESTNAJST let (264 vitals); NOVA HIŠA h19 (prvi matrični dokaz; hiša v PT naboru 1825; 81. hiša vzorca; oče Nikolaj Hriče? bajtar); h44 (3. VPIS) + h54 (4. VPIS) v PT luknji — obe že v PT_GAP_KNOWN → brez novih številk; luknja 42/50/51 NESPREMENJENA (19 dokazanih); PT 7/2; DUHOVNIKI: Kulbinek? 7× (= P95 »Klunček?« — isti podpis, boljše branje na spread formatu) + Jos. Rauq 2× + NOV podpis Fran. Dostál 1× (češko priimek; tudi ne-Griblje r63/r67/r70/r71/r80/r83); NOVELA babica 2. leto izpolnjeno: Toter 6× (oče r48 Jakob Toter = rodbina babice!) + Mavrefič + Mikl + Tolar? + Tome — 10/10 imenovanih; EMŠO sidra v Griblje vpisih: r48 21.07.1901 + r59 11.10.1901 (+ ne-Griblje r50 11.08., r66 08.11., r68 16.11., r83 18.12.); h24 pripis »Umrła 11.10.1946 griblje št 24« SAMOPOTRJUJE hišo; EXCLUDED: r35 (Griblje [~], hiša pod prosojnim trakom, spodnji rob odtrgan — odprt lead) + r47 (bela matičarska nalepka 26.01.1989 — starši Jurij Straus × Barbura Jakobič, MOŽEN Griblje, hiša nedokazljiva); skripta scripts/p96_parish_baptism_1901.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1901",
  "P96: PARISH OF PODZEMELJ — BAPTISM REGISTER 04105, THE FULL YEAR 1901 (issue #18; SAMPLE-TRANSCRIPTION-1901; MEASURES, does not decide; the v7 join unchanged): extending the P79 (1886) → … → P94 (1899) → P95 (1900) sample to 1901 — the frame: the heading '1901.' in the middle of p. 122 (scan 125, proven by P95) – row 87 on p. 129 (scan 135; the heading '1902' at the bottom of the same page) == printed pages 122–129 (87 rows); THE P96 NOVEL: THREE duplicated scans (127/128, 129/130, 133/134) — scan 128 = p. 124 with the two pasted slips FOLDED BACK → r32/r33 RESOLVED (Jun 1/2 Primostek 2 Anton EMŠO 01.06.1901 + Gradac 32?/33? Jožef EMŠO 01.06.1901; the 1989 slips = † Zagreb/Črnomelj); page == scan − 3 (125–127) / − 4 (129–130 → 125) / − 5 (131–132 → 126–127) / − 6 (135 → 129); THE FORMAT NOVEL: from p. 125 full-spread photographs (the left data half + the right parents/godparents/midwife/signature half — aligned by y-bands); THE MONTHS NOVEL: r65–r69 NOVEMBER (EMŠO r66 08.11.1901 + r68 16.11.1901) — December starts at r70; r36 'Jurij'? = JUNE (the sequence r39 July 10 forces it); ALL Griblje entries: 10 entries / 9 houses: 12, 12, 7, 54, 2, 17, 65, 24, 19, 44 — h12 ×2 = THE FIRST WITHIN-YEAR REPEAT since 1893 (the NARE run 1894–1900 broken after 8 years; r1 Gregor Juvan? × Barbura Cvetkovič vs r36 Matija Straus × Marija Jakobič — a multi-family house/a change) — 1 NEW house (19) + 8 repeats; the cumulative 270 entries / 81 houses across three books and SIXTEEN years (264 vitals); THE NEW HOUSE h19 (the first documentary proof; the house in the 1825 PT set; the 81st house of the sample; the father Nikolaj Hriče? a cotter); h44 (the 3rd ENTRY) + h54 (the 4th ENTRY) in the PT gap — both already in PT_GAP_KNOWN → no new numbers; the gap 42/50/51 UNCHANGED (19 proven); the PT 7/2; PRIESTS: Kulbinek? 7× (= P95 'Klunček?' — the same signature, a better reading on the spread format) + Jos. Rauq 2× + A NEW signature Fran. Dostál 1× (a Czech surname; also non-Griblje r63/r67/r70/r71/r80/r83); THE MIDWIFE COLUMN filled for the 2nd year: Toter 6× (the father of r48 Jakob Toter = the midwife's family!) + Mavrefič + Mikl + Tolar? + Tome — 10/10 named; EMŠO anchors in the Griblje entries: r48 21.07.1901 + r59 11.10.1901 (+ non-Griblje r50 11.08., r66 08.11., r68 16.11., r83 18.12.); the h24 note 'Umrła 11.10.1946 griblje št 24' SELF-CONFIRMS the house; EXCLUDED: r35 (Griblje [~], the house under a transparent strip, the bottom edge torn off — an open lead) + r47 (a white registrar's slip 26.01.1989 — the parents Jurij Straus × Barbura Jakobič, a POSSIBLE Griblje, the house unprovable); the script scripts/p96_parish_baptism_1901.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1901",
  p96Errors.length === 0,
  p96Errors.length === 0
    ? `10 vpisov / 9 hiš — h12 ×2 PRVA ponovitev po 1893 (NARE 1894–1900 prekinjeno; dva starševska para) · okvir 1901 skeni 125 (glava str. 122) – 135 row 87 (glava 1902 na dnu str. 129; 87 vrstic) · TRIJE dup pari (127/128, 129/130, 133/134) — sken 128 nalepki prepognjeni → r32/r33 rešeni · NOVELA formata: celo-spread od str. 125 · NOVELA mesecev: r65–r69 NOVEMBER (EMŠO), December od r70; r36 »Jurij«? = JUNI · NOVA HIŠA 19 (prvi matrični dokaz — bajtar; 81. hiša) · PT 7/2 (44/54 že dokazani; 42/50/51 nespremenjeno) · Kulbinek? 7× (= P95 Klunček?) + Rauq 2× + NOV Dostál · babica Toter 6× (10/10 imenovanih; oče r48 = njena rodbina) · EMŠO sidri r48/r59 · h24 samopotrditev št 24 · excluded r35 + r47 · umrljivost 2/10 · vitals 264 · kumulativ 270/81 ŠESTNAJST let`
    : p96Errors.join("; "),
);

// ——— qa-p97: p97 krstna 1902 — širitev vzorca na leto 1902 (issue #18;
//      SAMPLE-TRANSCRIPTION-1902; celoven neodvisen preracun iz bundled
//      virov: HOUSE_VITALS × PARISH_BOOKS; PT klasifikacija iz pinov;
//      NOVELA P97: 1902 = NOVA TISKANA knjiga (»Rojstna in krstna knjiga.«
//      — vse kolone na ENI strani, predtisk »Leto 18|02«; konec spread-formata
//      1901); DVA dup para skenov (137/138 = str. 131, 141/142 = str. 134);
//      stran == sken − 6 (135–137) / − 7 (139–141) / − 8 (143–144); okvir:
//      glava »1902« na dnu str. 129 (sken 135, P96 dokazano; r1 = Podzemelj 6
//      1./1. Januar; rows 1–7 na dnu str. 129, r7 v pregibu) – row 81 na str.
//      136 (sken 144; glava »1903.« NA SREDINI str. 136 — kot prelom 1900 NA
//      SREDINI str. 115; 1903 r1 = Griblje 24 — P98 lead); 81 vrstic;
//      12 vpisov / 12 hiš — NARE se nadaljuje (8. leto po prekinitvi 1901)
//      in PRVO LETO VZORCA BREZ NOVIH HIŠ (h3 = 1889, h87 = 1895 — obe že
//      v vitals); PT 11/1 (h58 v luknji — že v PT_GAP_KNOWN); DUHOVNIKI:
//      Dostál 8× (podpis »Stanislav Dostál« v 5/8 vpisov: r28/r39/r50/r59/r75; P96 »Fran. Dostál« —
//      isti z dvema zapisoma imena ALI dva — MERI) + Jos. Rauq 4×;
//      Kulbinek 0× (po 7× v 1901), Šturm 0×; babica Toter 9× + Adamič? 2× +
//      Papič? 1× — 12/12 imenovanih (3. leto izpolnjeno); ŽELJKO signali
//      16+17 (r12 botra Marija Željko na h87, r50 boter Nikolaj Željko? na
//      h91); SEGINA VRNITEV h30 (r16 oče Nikolaj Segina — veriga h70 1893 →
//      h30 1895 → h1 1899 → h30 1902, signal 5) + h25 (r59 mati Katarina
//      Segina + boter Danijel Segina — signali 5+6); STRAUS × SPUDIČ h16
//      (r46 — TRETJA hiša istega para: h45 → h40 → h16 — 04455 lead krstno
//      5× POTRJEN); menjave/branje: h87 (1895 Pegdirec? = 1902 Perdinec?
//      KURRENT — ISTI oče), h77 (Pošek 1890 → Cindrič 1902), h27 (→ Šimec ×
//      Kure), h22 (žena Klepec 1899 → Žurrič? 1902), h3 (Županič? 1889 →
//      Papič? 1902), h58 (oče Povk? — nova branja), h91 (Murov? = Muc?
//      1895/1902 ISTA žena Kure), h36 (Vrižan? × Straus);
//      EMŠO sidro r39 0307902505120 → 03.07.1902; excluded: r33 (Griblje
//      [~], hiša pod modrim zapisom »zap. št. 4524/1« — kanalna filtracija;
//      † 19.10.1981 Novo mesto — odprt lead) + r62 (bela nalepka 15.01.1995
//      Piran — vas nedokazljiva)
const p97Hv = HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year === 1902);
const p97Errors: string[] = [];
const P97_PT_IN_SET = ["3", "14", "16", "22", "25", "27", "30", "36", "77", "87", "91"];
const P97_PT_GAP = ["58"];
if (p97Hv.length !== 12)
  p97Errors.push(`vpisov 1902 (04105, zasidrani) ≠ 12 (${p97Hv.length})`);
const p97Houses = new Set(p97Hv.map((h) => h.houseNo));
if (p97Houses.size !== 12)
  p97Errors.push(`različnih hiš ≠ 12 (${p97Houses.size}: ${[...p97Houses].sort((a, b) => Number(a) - Number(b)).join(",")})`);
// okvir 1902: skeni 135–144; stran == novela P97 (dva dup para)
const p97PageOfScan = (s: number) =>
  s === 137 || s === 138 ? 131 : s === 141 || s === 142 ? 134 : s <= 137 ? s - 6 : s <= 141 ? s - 7 : s - 8;
const p97Bad = p97Hv.filter(
  (h) => h.status !== "DOCUMENTED" || !h.scan || !h.page
    || h.page !== p97PageOfScan(h.scan)
    || h.scan < 135 || h.scan > 144,
);
if (p97Bad.length > 0)
  p97Errors.push(`okvir 1902: skeni 135–144 ali stran ≠ novela P97 krščeno pri ${p97Bad.length}`);
// NARE: vsaka hiša 1× + PRVO LETO brez novih hiš
if (p97Houses.size !== p97Hv.length)
  p97Errors.push("NARE kršeno — znotraj-letna ponovitev pričakovano 0");
if (!p97Houses.has("30")) p97Errors.push("SEGINA VRNITEV h30 manjka");
if (!p97Houses.has("16")) p97Errors.push("STRAUS × SPUDIČ h16 manjka");
// kontinuitete (zadnja leta pred 1902; pini po očetu/materi/botru — prior ALI current)
const p97Pins: Array<[string, number, string]> = [
  ["3", 1889, "Županič"],
  ["14", 1900, "Brinec"],
  ["16", 1900, "Straus"],
  ["22", 1899, "Milek"],
  ["25", 1900, "Segina"],
  ["27", 1899, "Knekar"],
  ["30", 1899, "Segina"],
  ["36", 1898, "Straus"],
  ["58", 1900, "Kranbič"],
  ["77", 1890, "Pošek"],
  ["87", 1895, "Pegdirec"],
  ["91", 1895, "Muc"],
];
for (const [hn, yr, pin] of p97Pins) {
  const prior = HOUSE_VITALS.find((h) => h.bookSignature === "04105" && h.houseNo === hn && h.year === yr);
  const cur = p97Hv.find((h) => h.houseNo === hn);
  if (!prior || !cur) {
    p97Errors.push(`kontinuiteta hiša ${hn} (${yr} → 1902) manjka`);
    continue;
  }
  if (!prior.whatSi.includes(pin) && !cur.whatSi.includes(pin))
    p97Errors.push(`kontinuiteta hiša ${hn} (${yr}, pin ${pin}) ne ustreza`);
}
// vitals skupaj 449 (po P106: 429 + 20; krstna 1911)
if (HOUSE_VITALS.length !== 685)
  p97Errors.push(`HOUSE_VITALS ≠ 467 (${HOUSE_VITALS.length})`);
// babica: 12/12 imenovanih; Toter 9×
if (p97Hv.filter((h) => h.whatSi.includes("babica")).length !== 12)
  p97Errors.push("babica ni v vseh 12 whatSi (12/12 imenovanih)");
if (p97Hv.filter((h) => h.whatSi.includes("Marjeta Toter")).length !== 9)
  p97Errors.push(`babica Marjeta Toter ≠ 9× (${p97Hv.filter((h) => h.whatSi.includes("Marjeta Toter")).length})`);
// duhovniki: Dostál 8× (Stanislav jasno 6×) + Jos. Rauq 4×; Kulbinek 0×
if (p97Hv.filter((h) => h.whatSi.includes("Dostál")).length !== 8)
  p97Errors.push(`podpis Dostál ≠ 8× (${p97Hv.filter((h) => h.whatSi.includes("Dostál")).length})`);
if (p97Hv.filter((h) => h.whatSi.includes("Stanislav Dostál")).length !== 5)
  p97Errors.push(`podpis Stanislav Dostál ≠ 5× (${p97Hv.filter((h) => h.whatSi.includes("Stanislav Dostál")).length})`);
if (p97Hv.filter((h) => h.whatSi.includes("Jos. Rauq")).length !== 4)
  p97Errors.push(`podpis Jos. Rauq ≠ 4× (${p97Hv.filter((h) => h.whatSi.includes("Jos. Rauq")).length})`);
if (p97Hv.some((h) => h.whatSi.includes("Kulbinek")))
  p97Errors.push("Kulbinek 0× pričakovano — najden v whatSi");
// ŽELJKO signali 16+17
if (!p97Hv.some((h) => h.whatSi.includes("ŽELJKO signal 16")))
  p97Errors.push("ŽELJKO signal 16 (r12 botra Marija Željko) manjka");
if (!p97Hv.some((h) => h.whatSi.includes("ŽELJKO signal 17")))
  p97Errors.push("ŽELJKO signal 17 (r50 boter Nikolaj Željko?) manjka");
// EMŠO sidro r39
if (!p97Hv.some((h) => h.whatSi.includes("0307902505120")))
  p97Errors.push("EMŠO sidro r39 (03.07.1902) manjka");
push(
  "qa-p97-parish-baptism-1902",
  "P97: ŽUPNIJA PODZEMELJ — KRSTNA KNJIGA 04105, POLNO LETO 1902 (issue #18; SAMPLE-TRANSCRIPTION-1902; MERI, NE odloča; v7 join nespremenjen): širitev vzorca P79 (1886) → … → P95 (1900) → P96 (1901) na leto 1902 — okvir: glava »1902« na dnu str. 129 (sken 135, P96 dokazano; r1 = Podzemelj 6 Marija 1./1. Januar; rows 1–7 na dnu str. 129, r7 v pregibu) – row 81 na str. 136 (sken 144; glava »1903.« NA SREDINI str. 136 — kot prelom 1900 NA SREDINI str. 115 (P94); 1903 r1 = Griblje 24 4./5. Januar — P98 lead) == tiskane strani 129–136 (81 vrstic); NOVELA P97: 1902 = NOVA TISKANA knjiga — naslov »Rojstna in krstna knjiga.«, predtiskan okvir z vsemi kolonami na ENI strani (konec spread-formata 1901), predtiskano »Leto 18|02«; DVA podvojena para skenov (137/138 = str. 131, 141/142 = str. 134); stran == sken − 6 (135–137) / − 7 (139–141) / − 8 (143–144); VSI vpisi z Griblji: 12 vpisov / 12 hiš: 58, 87, 30, 22, 3, 27, 77, 16, 91, 36, 25, 14 — NARE se nadaljuje (8. leto; 1901 prekinjeno z h12 ×2) in PRVO LETO VZORCA BREZ NOVIH HIŠ (1886–1901 je vsako leto dodalo vsaj eno; h3 = 1889, h87 = 1895 — obe že v vitals); kumulativ 282 vpisov / 81 hiš čez tri knjige in SEDEMNAJST let (276 vitals); PT 11/1 (h58 v luknji — že v PT_GAP_KNOWN; luknja 42/50/51 nespremenjena, 19 dokazanih); DUHOVNIKI: Dostál 8× (podpis »Stanislav Dostál« jasno 3× — r28/r39/r50/r59; P96 1901 »Fran. Dostál« — isti duhovnik z dvema zapisoma imena ALI dva — MERI, odprt) + Jos. Rauq 4× — Kulbinek 0× (po 7× v 1901) + Šturm 0×; NOVELA babica 3. leto izpolnjeno: Toter 9× + Adamič? 2× (r8 Barbura, r16 Marija) + Papič? 1× (r32) — 12/12 imenovanih; ŽELJKO signali 16+17 (r12 botra Marija Željko na h87 + r50 boter Nikolaj Željko? na h91 — h1 rodbina); SEGINA VRNITEV h30 (r16 oče Nikolaj Segina × Marjeta Milek — veriga h70 1893 → h30 1895 → h1 1899 → h30 1902, signal 5; hišna forenzika 4× jasno 30, NE 36!) + h25 (r59 4. VPIS — 1900+1902 ISTA ZVEZA Matija Brinec × Katarina Segina + boter Danijel Segina — signali 5+6); STRAUS × SPUDIČ h16 (r46 — TRETJA hiša istega para: h45 1896/1897/1900 → h40 1899 → h16 1902 — 04455 POROČNI LEAD krstno 5× POTRJEN); MENJAVE/BRANJA DRUŽIN: h87 (1895 Pegdirec? = 1902 Perdinec? KURRENT — VERJETNO ISTI oče Marko), h77 (Pošek 1890 → Cindrič cevljar 1902), h27 (→ Janez Šimec × Marija Kure — ŠIMEC križni sklic h34 1887), h22 (žena Klepec 1899 → Ana Žurrič? 1902 — MERI), h3 (Županič? 1889 → Papič? × Novak 1902), h58 (oče »Janez Povk?« — nova branja po 1900 Kranbič ženi), h91 (Murov? = Muc? — 1895 Janez Muc mlinar/kovač, ISTA žena Ana Kure), h36 (Vrižan? × Straus — botri Straus par); EMŠO sidro r39 0307902505120 → 03.07.1902 (+ okvirna sidra r4 22.01., r5 24.01., r17 31.03?, r18 19.03., r40 08.07., r60 06.10., r65 23.10., r76 17.12., r81 26.12.); EXCLUDED: r33 (Griblje [~] Ana, hiša pod modrim matičarskim zapisom »zap. št. 4524/1« — kanalna filtracija ni pokazala temnega črnila; starši Matija Hrišič? × Nina? Jakobšič?, botra Jakob + Katarina Toter; † 19.10.1981 Novo mesto — odprt lead) + r62 (bela matičarska nalepka 15.01.1995 Piran — vas/hiša nedokazljiva; Žugelj botra = možen Griblje signal); okvirna anomalija: r72/r73 Boršt — brata, oba † 15/6.1918 (prva svetovna vojna!); r34 nezakonski + r37 mrtvorojen nezakonski (bež, ne-Griblje); skripta scripts/p97_parish_baptism_1902.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1902",
  "P97: PARISH OF PODZEMELJ — BAPTISM REGISTER 04105, THE FULL YEAR 1902 (issue #18; SAMPLE-TRANSCRIPTION-1902; MEASURES, does not decide; the v7 join unchanged): extending the P79 (1886) → … → P95 (1900) → P96 (1901) sample to 1902 — the frame: the heading '1902' at the bottom of p. 129 (scan 135, proven by P96; r1 = Podzemelj 6 Marija Jan 1/1; rows 1–7 at the bottom of p. 129, r7 in the fold) – row 81 on p. 136 (scan 144; the heading '1903.' IN THE MIDDLE of p. 136 — like the 1900 break IN THE MIDDLE of p. 115 (P94); the 1903 r1 = Griblje 24 Jan 4/5 — the P98 lead) == printed pages 129–136 (81 rows); THE P97 NOVEL: 1902 = A NEW PRINTED register — the title 'Rojstna in krstna knjiga.', a pre-printed frame with ALL columns on ONE page (the end of the 1901 spread format), the pre-printed 'Leto 18|02'; TWO duplicated scan pairs (137/138 = p. 131, 141/142 = p. 134); page == scan − 6 (135–137) / − 7 (139–141) / − 8 (143–144); ALL Griblje entries: 12 entries / 12 houses: 58, 87, 30, 22, 3, 27, 77, 16, 91, 36, 25, 14 — the NARE run continues (the 8th year; 1901 broken by h12 ×2) and THE FIRST SAMPLE YEAR WITHOUT NEW HOUSES (1886–1901 each year added at least one; h3 = 1889, h87 = 1895 — both already in vitals); the cumulative 282 entries / 81 houses across three books and SEVENTEEN years (276 vitals); the PT 11/1 (h58 in the gap — already in PT_GAP_KNOWN; the gap 42/50/51 unchanged, 19 proven); PRIESTS: Dostál 8× (the signature 'Stanislav Dostál' in 5/8 entries: r28/r39/r50/r59/r75; the P96 1901 'Fran. Dostál' — the same priest with two first-name spellings OR two priests — MERI, open) + Jos. Rauq 4× — Kulbinek 0× (after 7× in 1901) + Šturm 0×; THE MIDWIFE NOVEL filled for the 3rd year: Toter 9× + Adamič? 2× (r8 Barbura, r16 Marija) + Papič? 1× (r32) — 12/12 named; THE ŽELJKO signals 16+17 (r12 the godmother Marija Željko at h87 + r50 the godfather Nikolaj Željko? at h91 — the h1 family); THE SEGINA RETURN at h30 (r16 the father Nikolaj Segina × Marjeta Milek — the chain h70 1893 → h30 1895 → h1 1899 → h30 1902, the signal 5; the house forensics 4× clearly 30, NOT 36!) + h25 (r59 the 4th ENTRY — 1900+1902 the SAME COUPLE Matija Brinec × Katarina Segina + the godfather Danijel Segina — the signals 5+6); STRAUS × SPUDIČ at h16 (r46 — the THIRD house of the same couple: h45 1896/1897/1900 → h40 1899 → h16 1902 — the 04455 MARRIAGE LEAD christened 5× CONFIRMED); FAMILY CHANGES/READINGS: h87 (the 1895 Pegdirec? = the 1902 Perdinec? KURRENT — PROBABLY the SAME father Marko), h77 (Pošek 1890 → Cindrič a shoemaker 1902), h27 (→ Janez Šimec × Marija Kure — the ŠIMEC cross-link h34 1887), h22 (the wife Klepec 1899 → Ana Žurrič? 1902 — MERI), h3 (Županič? 1889 → Papič? × Novak 1902), h58 (the father 'Janez Povk?' — new readings after the 1900 Kranbič wife), h91 (Murov? = Muc? — the 1895 Janez Muc a miller/smith, the SAME wife Ana Kure), h36 (Vrižan? × Straus — the Straus godparent couple); the EMŠO anchor r39 0307902505120 → Jul 3, 1902 (+ frame anchors r4 Jan 22, r5 Jan 24, r17 Mar 31?, r18 Mar 19, r40 Jul 8, r60 Oct 6, r65 Oct 23, r76 Dec 17, r81 Dec 26); EXCLUDED: r33 (Griblje [~] Ana, the house under the blue registrar's note 'zap. št. 4524/1' — the channel filter showed no dark ink; the parents Matija Hrišič? × Nina? Jakobšič?, the godparents Jakob + Katarina Toter; † Oct 19, 1981 Novo mesto — an open lead) + r62 (a white registrar's slip Jan 15, 1995 Piran — the village/house unprovable; the Žugelj godmother = a possible Griblje signal); a frame anomaly: r72/r73 Boršt — brothers, both † Jun 15, 1918 (the Great War!); r34 an illegitimate + r37 a stillborn illegitimate (away, non-Griblje); the script scripts/p97_parish_baptism_1902.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1902",
  p97Errors.length === 0,
  p97Errors.length === 0
    ? `12 vpisov / 12 hiš — NARE 8. leto (vsaka hiša 1×) · PRVO LETO BREZ NOVIH HIŠ (h3 = 1889, h87 = 1895) · okvir 1902 skeni 135 (glava dno str. 129) – 144 row 81 (glava 1903 SREDINA str. 136; 81 vrstic) · NOVELA formata: NOVA TISKANA knjiga (vse kolone na eni strani; Leto 18|02) · DVA dup para (137/138, 141/142) · PT 11/1 (58 že dokazan; 42/50/51 nespremenjeno) · Dostál 8× (Stanislav v 5/8; = P96 Fran.?) + Rauq 4× + Kulbinek 0× · babica Toter 9× (12/12 imenovanih) · ŽELJKO signali 16+17 · SEGINA VRNITEV h30 (signal 5) + h25 (5+6) · STRAUS × SPUDIČ h16 — 3. hiša istega para (04455 lead 5×) · menjave h77/h27/h22/h3/h58/h36 + branja h87/h91 · EMŠO sidro r39 03.07.1902 · excluded r33 + r62 · Boršt r72/r73 † 15/6.1918 (WWI brata) · umrljivost 3/12 · vitals 276 · kumulativ 282/81 SEDEMNAJST let`
    : p97Errors.join("; "),
);

// ——— qa-p98: p98 krstna 1903 — širitev vzorca na leto 1903 (issue #18;
//      SAMPLE-TRANSCRIPTION-1903; celostni neodvisen preracun iz bundled
//      virov: HOUSE_VITALS × PARISH_BOOKS; PT klasifikacija iz pinov;
//      NOVELA P98: EN dup par skenov (148/149 = str. 140, rows 46–57; s149
//      bolj čitljiv); stran == sken − 8 (141–148) / − 9 (150–152 — premik za dup par); okvir: glava »1903.« NA
//      SREDINI str. 136 (sken 144, P97 dokazano; r1 = Griblje 24 4./5.
//      Januar) – row 82 na str. 143 (sken 152; glava »1904« pod r82 — 1904
//      r1 = Krasinec 37, P99 lead); 82 vrstic; 12 vpisov / 12 hiš — NARE
//      9. leto (vsaka hiša 1×; 1901 edini prelom z h12 ×2) in DRUGO LETO
//      ZAPORED BREZ NOVIH HIŠ (h83 luknja 1890–1902 zaplodana — 3. VPIS;
//      vse 12 že v vitals); PT 11/1 (h58 v luknji — že v PT_GAP_KNOWN);
//      DUHOVNIKI (celo leto): Dostál 44× + Jos. Ravq 32× + Levic? 1× +
//      manjkajoči 5×; na Gribljih: Dostál 6× (Stanislav jasno 1×) + Ravq
//      6×; Kulbinek 0×; babica (celo leto) 76 imenovanih / 2 prazni
//      (r52+r53); na Gribljih Toter 6× + Mavretič 2× + Mih 2× + Perdinec
//      1× + Delak 1× (12/12, 4. leto izpolnjeno); sidra: r1 h24 10. VPIS
//      (najbolj vpisovana gibriljska hiša registra); r55 REŠITEV P97 MERI
//      (1902 r8 »Povk? × Hambič?« = ISTI PAR kot 1903 »Požek × Kambič« —
//      KURRENT varianta); r76 h30 2. VPIS ZAPORED (oče ISTI Nikolaj
//      Segina; menjava žene Milek → Brinec — MERI) + r47 boter Nikol
//      Segina (SEGINA signali 7+8); ŽELJKO signali 18–21 (1903 botra
//      Željko 4×: r27/r48/r74/r81); DRAGOS signal 7 (r2 boter Janez
//      Dragoš — h12 oče 1892–93); EMŠO sidra: r7, r22, r56, r59 (Griblje
//      h20: 2010903505047 → 20.10.1903), r65, r72, r80; anomalije: r7
//      (trganje+plastika — oče gendarmer Morvet [~] — edini žandar do
//      1903!), r45 (Otok 8 — desna stran str. 139 FIZIČNO ODRGANA), r22
//      (ime pod † 10.09.1988 Zagreb pripiso), r48 (pod poročno pripiso
//      14.8.1971), r49 (NAKNADNI KRST 1.5.1944 po ~41 letih!), r51/r69
//      (mrtvorojena), r54 (nezakonski — mati samska), r57 (velik zapis —
//      priznanje očetovstva?), r80 (prestopni krst — roj. 25.12., krsta
//      2.1.1904), r82 (razveza — okrožno sodišče Novo mesto P111/60);
//      excluded: NI (vse 12 gibriljskih vrstic čitljive; r82 = Dragoše)
const p98Hv = HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year === 1903);
const p98Errors: string[] = [];
const P98_PT_IN_SET = ["5", "12", "20", "23", "24", "30", "32", "34", "35", "63", "83"];
const P98_PT_GAP = ["58"];
if (p98Hv.length !== 12)
  p98Errors.push(`vpisov 1903 (04105, zasidrani) ≠ 12 (${p98Hv.length})`);
const p98Houses = new Set(p98Hv.map((h) => h.houseNo));
if (p98Houses.size !== 12)
  p98Errors.push(`različnih hiš ≠ 12 (${p98Houses.size}: ${[...p98Houses].sort((a, b) => Number(a) - Number(b)).join(",")})`);
// okvir 1903: skeni 141–152; stran == novela P98 (en dup par 148/149)
const p98PageOfScan = (s: number) => (s === 148 || s === 149 ? 140 : s <= 148 ? s - 8 : s - 9);
const p98Bad = p98Hv.filter(
  (h) => h.status !== "DOCUMENTED" || !h.scan || !h.page
    || h.page !== p98PageOfScan(h.scan)
    || h.scan < 141 || h.scan > 152,
);
if (p98Bad.length > 0)
  p98Errors.push(`okvir 1903: skeni 141–152 ali stran ≠ novela P98 krščeno pri ${p98Bad.length}`);
// NARE: vsaka hiša 1× + DRUGO LETO zapored brez novih hiš
if (p98Houses.size !== p98Hv.length)
  p98Errors.push("NARE kršeno — znotraj-letna ponovitev pričakovano 0");
if (!p98Houses.has("24")) p98Errors.push("h24 10. VPIS manjka");
if (!p98Houses.has("83")) p98Errors.push("h83 luknja 1890–1902 zaplodana manjka");
if (!p98Houses.has("58")) p98Errors.push("REŠITEV P97 MERI h58 manjka");
if (!p98Houses.has("30")) p98Errors.push("SEGINA 2. VPIS ZAPORED h30 manjka");
// kontinuitete (zadnja leta pred 1903; pini po očetu/materi/botru — prior ALI current)
const p98Pins: Array<[string, number, string]> = [
  ["5", 1891, "Torec"],
  ["12", 1901, "Juvan"],
  ["20", 1900, "Perdinec"],
  ["23", 1900, "Južna"],
  ["24", 1901, "Juvančič"],
  ["30", 1902, "Segina"],
  ["32", 1900, "Urh"],
  ["34", 1899, "Žilak"],
  ["35", 1890, "Kušar"],
  ["58", 1902, "Požek"],
  ["63", 1898, "Uhr"],
  ["83", 1889, "Željko"],
];
for (const [hn, yr, pin] of p98Pins) {
  const prior = HOUSE_VITALS.find((h) => h.bookSignature === "04105" && h.houseNo === hn && h.year === yr);
  const cur = p98Hv.find((h) => h.houseNo === hn);
  if (!prior || !cur) {
    p98Errors.push(`kontinuiteta hiša ${hn} (${yr} → 1903) manjka`);
    continue;
  }
  if (!prior.whatSi.includes(pin) && !cur.whatSi.includes(pin))
    p98Errors.push(`kontinuiteta hiša ${hn} (${yr}, pin ${pin}) ne ustreza`);
}
// vitals skupaj 449 (po P106: 429 + 20; krstna 1911)
if (HOUSE_VITALS.length !== 685)
  p98Errors.push(`HOUSE_VITALS ≠ 467 (${HOUSE_VITALS.length})`);
// babica: 12/12 imenovanih; Toter 6×
if (p98Hv.filter((h) => h.whatSi.includes("babica")).length !== 12)
  p98Errors.push("babica ni v vseh 12 whatSi (12/12 imenovanih)");
if (p98Hv.filter((h) => h.whatSi.includes("Marjeta Toter")).length !== 6)
  p98Errors.push(`babica Marjeta Toter ≠ 6× (${p98Hv.filter((h) => h.whatSi.includes("Marjeta Toter")).length})`);
// duhovniki: Dostál 6× (Stanislav jasno 1×) + Jos. Ravq 6×; Kulbinek 0×
if (p98Hv.filter((h) => h.whatSi.includes("Dostál")).length !== 6)
  p98Errors.push(`podpis Dostál ≠ 6× (${p98Hv.filter((h) => h.whatSi.includes("Dostál")).length})`);
if (p98Hv.filter((h) => h.whatSi.includes("Stanislav Dostál")).length !== 1)
  p98Errors.push(`podpis Stanislav Dostál ≠ 1× (${p98Hv.filter((h) => h.whatSi.includes("Stanislav Dostál")).length})`);
if (p98Hv.filter((h) => h.whatSi.includes("Ravq")).length !== 6)
  p98Errors.push(`podpis Ravq ≠ 6× (${p98Hv.filter((h) => h.whatSi.includes("Ravq")).length})`);
if (p98Hv.some((h) => h.whatSi.includes("Kulbinek")))
  p98Errors.push("Kulbinek 0× pričakovano — najden v whatSi");
// signali: ŽELJKO 21 (4× botra 18–21) + SEGINA 7+8 + DRAGOS 7
if (!p98Hv.some((h) => h.whatSi.includes("ŽELJKO signal 21")))
  p98Errors.push("ŽELJKO signal 21 (r81 boter Nikolaj Željko) manjka");
if (!p98Hv.some((h) => h.whatSi.includes("SEGINA signal 7")))
  p98Errors.push("SEGINA signal 7 (r47 boter Nikol Segina) manjka");
if (!p98Hv.some((h) => h.whatSi.includes("SEGINA signal 8")))
  p98Errors.push("SEGINA signal 8 (h30 + h34 v istem letu) manjka");
if (!p98Hv.some((h) => h.whatSi.includes("DRAGOS signal 7")))
  p98Errors.push("DRAGOS signal 7 (r2 boter Janez Dragoš) manjka");
// REŠITEV P97 MERI + EMŠO sidro r59
if (!p98Hv.some((h) => h.whatSi.includes("REŠITEV P97 MERI")))
  p98Errors.push("REŠITEV P97 MERI (r55 Povk?×Hambič? = Požek×Kambič) manjka");
if (!p98Hv.some((h) => h.whatSi.includes("2010903505047")))
  p98Errors.push("EMŠO sidro r59 (20.10.1903) manjka");
push(
  "qa-p98-parish-baptism-1903",
  "P98: ŽUPNIJA PODZEMELJ — KRSTNA KNJIGA 04105, POLNO LETO 1903 (issue #18; SAMPLE-TRANSCRIPTION-1903; MERI, NE odloča; v7 join nespremenjen): širitev vzorca P79 (1886) → … → P96 (1901) → P97 (1902) na leto 1903 — okvir: glava »1903.« NA SREDINI str. 136 (sken 144, P97 dokazano — kot prelom 1900 SREDINA str. 115; 1903 r1 = Griblje 24 Jožef 4./5. Januar) – row 82 na str. 143 (sken 152; glava »1904« pod r82 — 1904 r1 = Krasinec 37 Ana 5./5. Januar — P99 lead) == tiskane strani 133–143 (82 vrstic); NOVELA P98: EN podvojen par skenov (148/149 = str. 140, rows 46–57; s149 bolj čitljiv); stran == sken − 8 (141–148) / − 9 (150–152 — premik za dup par); format 1903 = NOVA TISKANA knjiga (kot 1902 — naslov »Rojstna in krstna knjiga.«, predtiskano »Leto 18|03«); VSI vpisi z Griblji: 12 vpisov / 12 hiš: 24, 5, 12, 32, 35, 23, 63, 34, 58, 20, 30, 83 — NARE 9. leto (vsaka hiša 1×; 1901 edini prelom z h12 ×2) in DRUGO LETO ZAPORED BREZ NOVIH HIŠ (h83 luknja 1890–1902 zaplodana — 3. VPIS po 1888+1889, 13 let!); kumulativ 294 vpisov / 81 hiš čez tri knjige in OSEMNAJST let (288 vitals); PT 11/1 (h58 v luknji — že v PT_GAP_KNOWN; luknja 42/50/51 nespremenjena, 19 dokazanih); DUHOVNIKI (celo leto): Dostál 44× dominant + Jos. Ravq 32× + Levic? 1× + manjkajoči/odrezani 5× — na Gribljih: Dostál 6× (Stanislav jasno 1× na r47) + Ravq 6×; Kulbinek 0× (tretje leto po 7× v 1901); babica (celo leto): 76 imenovanih / 2 prazni (r52+r53 »—«; r51/r69 mrtvorojena brez babice; r45/r57 odrezani) — na Gribljih: Toter 6× + Mavretič 2× + Mih 2× + Perdinec 1× + Delak 1× (12/12, 4. leto izpolnjeno); SIDRA: r1 h24 10. VPIS (1887, 1888, 1890, 1892, 1893, 1895×2, 1897, 1901) — NAJBOLJ VPISOVANA gibriljska hiša registra (oče Matevž Juvančič? pod trakom; svinčnik »Matijo?« nad imenom — MERI); r2 h5 2. VPIS (DRAGOS signal 7 — boter Janez Dragoš = h12 oče 1892–93; fold-damage str. 136); r3 h12 8. VPIS († 22/1.03 dojenček); r55 h58 7. VPIS — REŠITEV P97 MERI: 1902 r8 oče »Janez Povk? × Katarina Hambič?« = ISTI PAR kot 1903 »Janez Požek × Katarina Kambič« (KURRENT varianta — NI menjava družine; 1892 Požek × Dragos → menjava žene pred 1900 ostaja); r59 h20 4. VPIS (EMŠO Ž 2010903505047 → 20.10.1903 SIDRO — Peter Perdinec × Doroteja Klepec; babica Katarina Perdinec); r76 h30 2. VPIS ZAPORED (1902 r16 + 1903 r76 — oče ISTI Nikolaj Segina; MENJAVA ŽENE: Marjeta Milek (1902) → Katarina Brinec (1903) — MERI); r81 h83 3. VPIS (LUKNJA 1890–1902 zaplodana; ŽELJKO signal 21); SEGINA signali 7+8 (r47 boter Nikol Segina = h30 oče 1902 + h30+h34 v istem letu; HRIŽAN signal — botrinja Katarina Hrižan na h34); ŽELJKO signali 18–21 (1903 botra Željko 4×: r27 Janez, r48 Nikol, r74 Janez, r81 Nikolaj); EMŠO sidra celo leto: r7 0902903505416 → 09.02.1903 ♂, r22 0104903505041 → 01.04.1903 ♀, r56 0310903505116 → 03.10.1903 ♀, r59, r65 0611903505124 → 06.11.1903 ♀, r72 2811903500562 → 28.11.1903 ♂, r80 2512903500066 → 25.12.1903 ♂; ANOMALIJE: r7 (kraj/hiša/ime pod trganjem+plastiko — oče »Morvet/Morvat [~], gendarmer.« — EDINI žandar v register do 1903!), r45 (Otok 8 Nikolaj — desna stran str. 139 FIZIČNO ODRGANA: oče/matère/botra/podpis odrezani), r22 (ime pod veliko modro pripiso † 10.09.1988 v Zagrebu — EMŠO 01.04.1903 ♀), r48 (pod poročno pripiso »Družii poročena 14.8.1971«), r49 (NAKNADNI KRST: Geršiči? 2 Marija roj. 31.8.1903, krščena 1.5.1944 — po ~41 letih!), r51/r69 (mrtvorojeni), r54 (nezakonski — mati »Marija Rak, samska bajtanjeva hči«), r57 (velik podčrtan zapis — priznanje očetovstva?), r80 (PRESTOPNI KRST: roj. 23.12. [~], EMŠO 25.12.1903, krščen 2.1.1904!), r82 (razveza — okrožno sodišče Novo mesto št. P111/60); EXCLUDED: NI izključenih gibriljskih vrstic (vse 12 čitljivih; r82 = Dragoše, ne Griblje); umrljivost dojenčkov (celo leto) 6/80: r3 †22/1.03 + r29 †1/9.03 + r45 †7/9.03? + r67 †16/1.03 + r68 †9/1.04 + r71 †25/9.04; skripta scripts/p98_parish_baptism_1903.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1903",
  "P98: PARISH OF PODZEMELJ — BAPTISM REGISTER 04105, THE FULL YEAR 1903 (issue #18; SAMPLE-TRANSCRIPTION-1903; MEASURES, does not decide; the v7 join unchanged): extending the P79 (1886) → … → P96 (1901) → P97 (1902) sample to 1903 — the frame: the heading '1903.' IN THE MIDDLE of p. 136 (scan 144, proven by P97 — like the 1900 break in the middle of p. 115; the 1903 r1 = Griblje 24 Jožef Jan 4/5) – row 82 on p. 143 (scan 152; the heading '1904' below r82 — the 1904 r1 = Krasinec 37 Ana Jan 5/5 — the P99 lead) == printed pages 133–143 (82 rows); THE P98 NOVEL: ONE duplicated scan pair (148/149 = p. 140, rows 46–57; s149 more legible); page == scan − 8 (141–148) / − 9 (150–152); the 1903 format = A NEW PRINTED register (as 1902 — the title 'Rojstna in krstna knjiga.', the pre-printed 'Leto 18|03'); ALL Griblje entries: 12 entries / 12 houses: 24, 5, 12, 32, 35, 23, 63, 34, 58, 20, 30, 83 — the NARE run's 9th year (each house 1×; 1901 the only break with h12 ×2) and THE SECOND CONSECUTIVE YEAR WITHOUT NEW HOUSES (the h83 gap 1890–1902 filled — the 3rd ENTRY after 1888+1889, 13 years!); the cumulative 294 entries / 81 houses across three books and EIGHTEEN years (288 vitals); the PT 11/1 (h58 in the gap — already in PT_GAP_KNOWN; the gap 42/50/51 unchanged, 19 proven); PRIESTS (the whole year): Dostál 44× dominant + Jos. Ravq 32× + Levic? 1× + missing/torn 5× — in Griblje: Dostál 6× (Stanislav clearly 1× at r47) + Ravq 6×; Kulbinek 0× (the third year after 7× in 1901); the midwife (the whole year): 76 named / 2 empty (r52+r53 '—'; the stillborn r51/r69 without a midwife; r45/r57 torn) — in Griblje: Toter 6× + Mavretič 2× + Mih 2× + Perdinec 1× + Delak 1× (12/12, the 4th filled year); ANCHORS: r1 h24 the 10th ENTRY (1887, 1888, 1890, 1892, 1893, 1895×2, 1897, 1901) — THE MOST-ENTERED Griblje house of the register (the father Matevž Juvančič? under a strip; the pencil 'Matijo?' above the name — MERI); r2 h5 the 2nd ENTRY (the DRAGOS signal 7 — the godfather Janez Dragoš = the h12 father 1892–93; the fold damage of p. 136); r3 h12 the 8th ENTRY († Jan 22, 1903 an infant); r55 h58 the 7th ENTRY — THE RESOLUTION OF THE P97 MERI: the 1902 r8 father 'Janez Povk? × Katarina Hambič?' = THE SAME COUPLE as the 1903 'Janez Požek × Katarina Kambič' (a KURRENT variant — NOT a family change; the 1892 Požek × Dragos → the wife change before 1900 remains); r59 h20 the 4th ENTRY (the personal ID 2010903505047 → Oct 20, 1903 AN ANCHOR — Peter Perdinec × Doroteja Klepec; the midwife Katarina Perdinec); r76 h30 the 2nd CONSECUTIVE ENTRY (the 1902 r16 + the 1903 r76 — the father THE SAME Nikolaj Segina; THE WIFE CHANGE: Marjeta Milek (1902) → Katarina Brinec (1903) — MERI); r81 h83 the 3rd ENTRY (THE GAP 1890–1902 filled; the ŽELJKO signal 21); the SEGINA signals 7+8 (the r47 godfather Nikol Segina = the h30 father 1902 + h30+h34 in the same year; the HRIŽAN signal — the godmother Katarina Hrižan at h34); the ŽELJKO signals 18–21 (in 1903 the Željko godparents 4×: r27 Janez, r48 Nikol, r74 Janez, r81 Nikolaj); the personal-ID anchors of the whole year: r7 → Feb 9, 1903 ♂, r22 → Apr 1, 1903 ♀, r56 → Oct 3, 1903 ♀, r59, r65 → Nov 6, 1903 ♀, r72 → Nov 28, 1903 ♂, r80 → Dec 25, 1903 ♂; ANOMALIES: r7 (the village/house/name under tearing+tape — the father 'Morvet/Morvat [~], a GENDARMERIE man' — THE ONLY gendarme in the register up to 1903!), r45 (Otok 8 Nikolaj — the right side of p. 139 PHYSICALLY SCRAPED OFF: the father/mother/godparents/signature cut away), r22 (the name under a large blue note † Sep 10, 1988 in Zagreb — the personal ID Apr 1, 1903 ♀), r48 (under a marriage note 'married Aug 14, 1971'), r49 (A SUBSEQUENT BAPTISM: Geršiči? 2 Marija born Aug 31, 1903, baptized May 1, 1944 — after ~41 years!), r51/r69 (stillborn), r54 (illegitimate — the mother 'Marija Rak, an unmarried cotteress's daughter'), r57 (a large underlined record — a paternity acknowledgment?), r80 (A TRANSFERRED BAPTISM: born Dec 23 [~], the personal ID Dec 25, 1903, baptized Jan 2, 1904!), r82 (a divorce — the district court Novo mesto no. P111/60); EXCLUDED: NO excluded Griblje rows (all 12 legible; r82 = Dragoše, not Griblje); the infant mortality (the whole year) 6/80: r3 + r29 + r45 + r67 + r68 + r71; the script scripts/p98_parish_baptism_1903.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1903",
  p98Errors.length === 0,
  p98Errors.length === 0
    ? `12 vpisov / 12 hiš — NARE 9. leto (vsaka hiša 1×) · DRUGO LETO ZAPORED BREZ NOVIH HIŠ (h83 luknja 1890–1902 zaplodana — 3. VPIS po 13 letih) · okvir 1903 skeni 141 (str. 133) – 152 row 82 (glava 1904 pod r82; 1904 r1 = Krasinec 37 — P99 lead; 82 vrstic) · glava 1903 NA SREDINI str. 136 (sken 144) · EN dup par (148/149) · PT 11/1 (58 že dokazan; 42/50/51 nespremenjeno) · Dostál 6× (Stanislav 1×) + Ravq 6× + Kulbinek 0× · babica Toter 6× (12/12; celo leto 76/2) · h24 10. VPIS — najbolj vpisovana hiša registra · REŠITEV P97 MERI (Povk?×Hambič? = Požek×Kambič — ISTI PAR) · h30 2. VPIS ZAPORED (menjava žene Milek → Brinec — MERI) · SEGINA signali 7+8 · ŽELJKO signali 18–21 (4× botra) · DRAGOS signal 7 · EMŠO sidro r59 20.10.1903 · r49 NAKNADNI KRST 1944 + r80 prestopni krst 2.1.1904 · excluded NI (r82 = Dragoše → anomalija razveza) · umrljivost 1/12 · vitals 288 · kumulativ 294/81 OSEMNAJST let`
    : p98Errors.join("; "),
);


// ——— qa-p99: p99 krstna 1904 — širitev vzorca na leto 1904 (issue #18;
//      SAMPLE-TRANSCRIPTION-1904; celostni neodvisen preracun iz bundled
//      virov: HOUSE_VITALS × PARISH_BOOKS; PT klasifikacija iz pinov;
//      okvir: glava »1904« POD r82 na str. 143 (sken 152, P98 dokazano;
//      1904 r1 = Krasinec 37 Ana 5./5. Januar — P98 lead potrjen) – row 90
//      na str. 150 (sken 160; glava »1905« pod r90 — 1905 r1 = Gradac 45?,
//      P100 lead); 90 vrstic — NAJDALJŠE leto registra doslej; NOVELA P99:
//      EN dup par (155/156 = str. 146, rows 35–46; s156 jasnejši); stran
//      == sken − 9 (152–155) / − 10 (157–160 — premik za dup par); format
//      = NOVA TISKANA knjiga (kot 1902–1903); 20 vpisov / 19 hiš + r69
//      hiša neberljiva (brez bloka) — NARE 10. leto (vsaka znana hiša 1×;
//      1901 edini prelom z h12 ×2); 3 NOVE HIŠE po dveh letih brez novih
//      (h6 — nabor PT, prvi vpis; h42 + h50 = 20./21. dokazana številka
//      luknje 41–60 — ostaja samo h51!); h88 = prvi KRSTNI vpis (hiša že
//      v mrliški 04894/1886); PT 13/6 (42/43/45/50/54/60 v luknji; 42 +
//      50 NOVI, 43/45/54/60 že dokazani); DUHOVNIKI (celo leto): Ravq 38×
//      + Dostál 32× + NOV kaplan Hugo Hengsfeld 13× (od r67 — MENJAVA
//      KAPLANOV sredi leta; »Kapp.«) + neberljivi 5× + mrtvorojena 2×;
//      Kulbinek 0×; na Gribljih: Dostál 10 (vsi Stanislav; januar z
//      naslovom »Kaplan«) + Ravq 8 + Hengsfeld 1 (r80) + neberljiv 1
//      (r90); babica (celo leto) 85 imenovanih / 5 praznih (r24, r54,
//      r55, r83, r86) — na Gribljih: Toter 10× + Mih 4× (4. = r69
//      vrstica brez bloka) + Mavretič 3× + Delak 1× + Aleksič 1× + pod
//      trakom 1× (r16; 20/20 izpolnjeno); sidra: r2 h22 3. VPIS (POŽEK
//      signal — boter Janez Požek = h30 oče 1902/03); r14 h87 3. VPIS
//      (KURRENT ISTI oče Podrinec/Perdinec — NI menjava); r15 h15 8. VPIS
//      (BRINEC signal); r16 h88 PRVI KRSTNI VPIS (oče Peter Brinec? +
//      boter Janez Brinec? — 2. in 3. Brinec oseba); r18 h24 11. VPIS (ŠE
//      VEDNO najbolj vpisovana hiša registra; 29. FEBRUAR — prestopno
//      leto 1904; razveljavitev zakona 1947/48; † 30.1.1983 Zagreb); r31
//      h16 6. VPIS (Strausova/Spudičeva hiša — 04455 lead); r38 h36
//      10. VPIS; r46 h6 NOVA (ŽELJKO signal — boter Nikol Željko); r65
//      h50 NOVA (ŠTRUCELJ signal — mati Doroteja Štrucelj = h22 rod
//      1902); r90 h42 NOVA (ŠTRAUS signal — oče Matija Štraus, 2.
//      Strausova oseba 1904; ZADNJA vrstica leta); r78 h45 4. VPIS
//      (SPUDIČ signal — mati Barbara Spudič; EMŠO 2610904505164 =
//      26.10.1904; † 14.10.2003 Metlika — 98 let, najdaljše življenje
//      1904); r80 h91 4. VPIS (MUC KONTINUITETA — oče Janez Muc bajtar);
//      r82 h69 8. VPIS (ŽELJKO signal — oče Janez Željko); MILEK signali
//      (r2 h22 oče + r73 h65 oče Matija Milek [1901 Mitek? KURRENT] +
//      r57 h21 boter Matija Milek); MIH signal r69 (mati in babica ISTA —
//      Marija Mih); EMŠO kampanja 1982–84 (»Šimonič Miri« + datumi
//      20.12.1982/28.12.1982/30.12.1982/12.6.1984) — sidra r8 21.01.,
//      r45 28.06., r48 20.07., r77 25.10., r78 26.10., r79 28.10., r89
//      20.12.1904; ANOMALIJE: r19 (VSTAVLJEN vpis 2007 brez kraja/hiše —
//      EXCLUDED; EMŠO 0303904505822 neskladje spola), r18 (29.2. +
//      razveljavitev zakona 1947/48), r24 (Mlake »preh. dvor« —
//      nezakonski, mati »cigarka«, babica »—«), r25/r26 + r36/r37
//      (DVOJČKI — oba para † dojenčka), r41 + r84 (MRTVOROJENA
//      »Z.mrtvorajen«, krsta »—«), r42 (tretji otrok v 26 dneh — oče
//      Kržan/Krožan NESKLADJE), r45 (isti Martin Žugelj × DVE ženi <
//      6 mes. — MERI), r69 (hiša pod modrim pripisom + poševno
//      prečrtana), r40 († 9.11.1918 — dan pred premirjem); umrljivost
//      dojenčkov 8 + mrtvorojena 2 + nezakonski 2
const p99Hv = HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year === 1904);
const p99Errors: string[] = [];
if (p99Hv.length !== 19)
  p99Errors.push(`vpisov 1904 (04105, zasidrani) ≠ 19 (${p99Hv.length})`);
const p99Houses = new Set(p99Hv.map((h) => h.houseNo));
if (p99Houses.size !== 19)
  p99Errors.push(`različnih hiš ≠ 19 (${p99Houses.size}: ${[...p99Houses].sort((a, b) => Number(a) - Number(b)).join(",")})`);
// okvir 1904: skeni 152–160; stran == novela P99 (en dup par 155/156)
const p99PageOfScan = (s: number) => (s <= 155 ? s - 9 : s - 10);
const p99Bad = p99Hv.filter(
  (h) => h.status !== "DOCUMENTED" || !h.scan || !h.page
    || h.page !== p99PageOfScan(h.scan)
    || h.scan < 152 || h.scan > 160,
);
if (p99Bad.length > 0)
  p99Errors.push(`okvir 1904: skeni 152–160 ali stran ≠ novela P99 krščeno pri ${p99Bad.length}`);
// NARE 10. leto: vsaka znana hiša 1× (r69 neberljiva brez bloka)
if (p99Houses.size !== p99Hv.length)
  p99Errors.push("NARE kršeno — znotraj-letna ponovitev pričakovano 0");
// PT 13/6: nabor (6/15/16/21/22/24/36 + 65/66/69/87/88/91) vs luknja 41–60
const p99Gap = p99Hv.filter((h) => ["42", "43", "45", "50", "54", "60"].includes(h.houseNo)).map((h) => h.houseNo).sort();
if (p99Gap.length !== 6)
  p99Errors.push(`PT luknja 41–60 ≠ 6 hiš (${p99Gap.length}: ${p99Gap.join(",")})`);
if (p99Hv.some((h) => Number(h.houseNo) >= 41 && Number(h.houseNo) <= 60 && !p99Gap.includes(h.houseNo)))
  p99Errors.push("hiša v luknji 41–60 izven pričakovane PT_GAP množice");
// 3 NOVE hiše + sidra
for (const hn of ["6", "42", "50"]) {
  const nb = p99Hv.find((h) => h.houseNo === hn);
  if (!nb) p99Errors.push(`NOVA hiša ${hn} (P99) manjka`);
  else if (!nb.whatSi.includes("NOVA HIŠA"))
    p99Errors.push(`NOVA hiša ${hn} (P99) brez oznake NOVA HIŠA`);
}
if (!p99Houses.has("24")) p99Errors.push("h24 11. VPIS manjka");
const p99H24 = p99Hv.find((h) => h.houseNo === "24");
if (p99H24 && (!p99H24.whatSi.includes("11. VPIS") || !p99H24.whatSi.includes("PRESTOPNI")))
  p99Errors.push("h24 11. VPIS + PRESTOPNI dan (29.2.) ne ustreza");
if (!p99Houses.has("88")) p99Errors.push("h88 PRVI KRSTNI VPIS manjka");
const p99H88 = p99Hv.find((h) => h.houseNo === "88");
if (p99H88 && !p99H88.whatSi.includes("PRVI KRSTNI VPIS"))
  p99Errors.push("h88 PRVI KRSTNI VPIS oznaka manjka");
const p99H16 = p99Hv.find((h) => h.houseNo === "16");
if (!p99H16 || !p99H16.whatSi.includes("6. VPIS") || !p99H16.whatSi.includes("Strausova/Spudičeva hiša"))
  p99Errors.push("h16 6. VPIS + Strausova/Spudičeva hiša (04455 lead) ne ustreza");
const p99H36 = p99Hv.find((h) => h.houseNo === "36");
if (!p99H36 || !p99H36.whatSi.includes("10. VPIS"))
  p99Errors.push("h36 10. VPIS ne ustreza");
const p99H45 = p99Hv.find((h) => h.houseNo === "45");
if (!p99H45 || !p99H45.whatSi.includes("SPUDIČ signal") || !p99H45.whatSi.includes("2610904505164") || !p99H45.whatSi.includes("98 let"))
  p99Errors.push("h45 SPUDIČ signal + EMŠO 2610904505164 + 98 let ne ustreza");
const p99H91 = p99Hv.find((h) => h.houseNo === "91");
if (!p99H91 || !p99H91.whatSi.includes("MUC KONTINUITETA") || !p99H91.whatSi.includes("4. VPIS"))
  p99Errors.push("h91 4. VPIS + MUC KONTINUITETA ne ustreza");
const p99H42 = p99Hv.find((h) => h.houseNo === "42");
if (p99H42 && !p99H42.whatSi.includes("ŠTRAUS signal"))
  p99Errors.push("h42 ŠTRAUS signal manjka");
const p99H50 = p99Hv.find((h) => h.houseNo === "50");
if (p99H50 && !p99H50.whatSi.includes("ŠTRUCELJ signal"))
  p99Errors.push("h50 ŠTRUCELJ signal manjka");
const p99H22 = p99Hv.find((h) => h.houseNo === "22");
if (p99H22 && !p99H22.whatSi.includes("KAPLAN"))
  p99Errors.push("h22 podpis »Stanislav Dostál, KAPLAN« (januar) manjka");
if (p99Hv.filter((h) => h.whatSi.includes("POŽEK signal")).length !== 2)
  p99Errors.push(`POŽEK signal (r2 h22 boter Janez Požek + r57 h21 botrinja Marjeta Požek) ≠ 2× (${p99Hv.filter((h) => h.whatSi.includes("POŽEK signal")).length})`);
if (p99Hv.filter((h) => h.whatSi.includes("ŽELJKO signal")).length !== 2)
  p99Errors.push(`ŽELJKO signal (h6 + h69) ≠ 2× (${p99Hv.filter((h) => h.whatSi.includes("ŽELJKO signal")).length})`);
if (p99Hv.filter((h) => h.whatSi.includes("BRINEC signal")).length !== 2)
  p99Errors.push(`BRINEC signal (h15 + h88) ≠ 2× (${p99Hv.filter((h) => h.whatSi.includes("BRINEC signal")).length})`);
// kontinuitete (zadnja leta pred 1904; pini po očetu/materi/botru — prior ALI current)
const p99Pins: Array<[string, number, string]> = [
  ["15", 1896, "Jaklič"],
  ["16", 1902, "Straus"],
  ["21", 1899, "Cindrič"],
  ["22", 1902, "Milek"],
  ["24", 1903, "Jurajevič"],
  ["36", 1902, "Miše"],
  ["43", 1897, "Perdinec"],
  ["45", 1900, "Škrac"],
  ["54", 1901, "Župančič"],
  ["60", 1899, "Novak"],
  ["65", 1901, "Milek"],
  ["66", 1887, "Bohte"],
  ["69", 1898, "Željko"],
  ["87", 1902, "Perdinec"],
  ["91", 1902, "Muc"],
];
for (const [hn, yr, pin] of p99Pins) {
  const prior = HOUSE_VITALS.find((h) => h.bookSignature === "04105" && h.houseNo === hn && h.year === yr);
  const cur = p99Hv.find((h) => h.houseNo === hn);
  if (!prior || !cur) {
    p99Errors.push(`kontinuiteta hiša ${hn} (${yr} → 1904) manjka`);
    continue;
  }
  if (!prior.whatSi.includes(pin) && !cur.whatSi.includes(pin))
    p99Errors.push(`kontinuiteta hiša ${hn} (${yr}, pin ${pin}) ne ustreza`);
}
// vitals skupaj 307 (P99: 288 + 19; krstna 1904; r69 hiša neberljiva brez bloka)
if (HOUSE_VITALS.length !== 685)
  p99Errors.push(`HOUSE_VITALS ≠ 467 (${HOUSE_VITALS.length})`);
// babica: 19/19 blokov (h88 = pod trakom); Toter 10× + Mavretič 3× + Mih 3×
// (4. Mih = r69 vrstica — hiša neberljiva, brez bloka) + Delak + Aleksič
if (p99Hv.filter((h) => h.whatSi.includes("babica")).length !== 19)
  p99Errors.push(`babica ni v vseh 19 whatSi (${p99Hv.filter((h) => h.whatSi.includes("babica")).length})`);
if (p99Hv.filter((h) => h.whatSi.includes("Marjeta Toter")).length !== 10)
  p99Errors.push(`babica Marjeta Toter ≠ 10× (${p99Hv.filter((h) => h.whatSi.includes("Marjeta Toter")).length})`);
if (p99Hv.filter((h) => h.whatSi.includes("Ana Mavretič")).length !== 3)
  p99Errors.push(`babica Ana Mavretič ≠ 3× (${p99Hv.filter((h) => h.whatSi.includes("Ana Mavretič")).length})`);
if (p99Hv.filter((h) => h.whatSi.includes("babica Marija Mih")).length !== 3)
  p99Errors.push(`babica Marija Mih ≠ 3× v blokih (4. = r69 vrstica — hiša neberljiva, brez bloka) (${p99Hv.filter((h) => h.whatSi.includes("babica Marija Mih")).length})`);
if (p99Hv.filter((h) => h.whatSi.includes("Alojzija Delak")).length !== 1)
  p99Errors.push("babica Alojzija Delak (r38) ≠ 1×");
if (p99Hv.filter((h) => h.whatSi.includes("Barbara Aleksič")).length !== 1)
  p99Errors.push("babica Barbara Aleksič (r2) ≠ 1×");
// duhovniki (bloki): Dostál 10 (vsi Stanislav) + Ravq 7 (8. = r69 vrstica
// brez bloka) + Hengsfeld 1 (r80) + neberljiv 1 (h42); Kulbinek 0×
if (p99Hv.filter((h) => h.whatSi.includes("Dostál")).length !== 10)
  p99Errors.push(`podpis Dostál ≠ 10× (${p99Hv.filter((h) => h.whatSi.includes("Dostál")).length})`);
if (p99Hv.filter((h) => h.whatSi.includes("Stanislav Dostál")).length !== 10)
  p99Errors.push(`podpis Stanislav Dostál ≠ 10× (${p99Hv.filter((h) => h.whatSi.includes("Stanislav Dostál")).length})`);
if (p99Hv.filter((h) => h.whatSi.includes("Ravq")).length !== 7)
  p99Errors.push(`podpis Ravq ≠ 7× v blokih (8. = r69 vrstica — hiša neberljiva, brez bloka) (${p99Hv.filter((h) => h.whatSi.includes("Ravq")).length})`);
if (p99Hv.filter((h) => h.whatSi.includes("Hengsfeld")).length !== 1)
  p99Errors.push(`podpis Hengsfeld ≠ 1× (${p99Hv.filter((h) => h.whatSi.includes("Hengsfeld")).length})`);
if (p99Hv.some((h) => h.whatSi.includes("Kulbinek")))
  p99Errors.push("Kulbinek 0× pričakovano — najden v whatSi");
push(
  "qa-p99-parish-baptism-1904",
  "P99: ŽUPNIJA PODZEMELJ — KRSTNA KNJIGA 04105, POLNO LETO 1904 (issue #18; SAMPLE-TRANSCRIPTION-1904; MERI, NE odloča; v7 join nespremenjen): širitev vzorca P79 (1886) → … → P97 (1902) → P98 (1903) na leto 1904 — okvir: glava »1904« POD r82 na str. 143 (sken 152, P98 dokazano; 1904 r1 = Krasinec 37 Ana 5./5. Januar — P98 lead potrjen) – row 90 na str. 150 (sken 160; glava »1905« pod r90 — 1905 r1 = Gradac 45? Antonija 2./7.? Januar — P100 lead) == tiskane strani 143–150 (90 vrstic — NAJDALJŠE leto registra doslej); NOVELA P99: EN podvojen par skenov (155/156 = str. 146, rows 35–46; s156 jasnejši); stran == sken − 9 (152–155) / − 10 (157–160 — premik za dup par); format 1904 = NOVA TISKANA knjiga (kot 1902–1903 — naslov »Rojstna in krstna knjiga.«, predtiskano »Leto 18|04«); VSI vpisi z Griblji: 20 vpisov / 19 hiš + 1 NEBERLJIVA (r69 hiša pod modrim pripisom + poševno prečrtana — brez vitals bloka): 22, 87, 15, 88, 24, 54, 16, 60, 36, 6, 66, 43, 21, 50, 65, 45, 91, 69, 42 — NARE 10. leto (vsaka znana hiša 1×; 1901 edini prelom z h12 ×2); 3 NOVE HIŠE po dveh letih brez novih: h6 (nabor PT 1–40 — prvi vpis) + h42 in h50 (20. in 21. dokazana številka luknje 41–60 — ostaja SAMO h51!); h88 = prvi KRSTNI vpis (hiša že v mrliški 04894/1886); kumulativ 313 vpisov / 84 hiš čez tri knjige in DEVETNAJST let (307 vitals); PT 13/6 (42/43/45/50/54/60 v luknji — 42 + 50 NOVI, 43/45/54/60 že dokazani; luknja zdaj 21 dokazanih); DUHOVNIKI (celo leto): Jos. Ravq 38× + Dostál 32× (Stanislav 29× — januar z naslovom »Kaplan«; Flavi? 3× [~]) + NOV KAPLAN Hugo Hengsfeld 13× (od r67; »Kapp.«) — MENJAVA KAPLANOV sredi leta + neberljivi 5× + mrtvorojena 2×; Kulbinek 0×; na Gribljih: Dostál 10 (vsi Stanislav) + Ravq 8 + Hengsfeld 1 (r80) + neberljiv 1 (r90); babica (celo leto): 85 imenovanih / 5 praznih (r24, r54, r55, r83, r86 »—«) — na Gribljih: Toter 10× + Mih 4× + Mavretič 3× + Delak 1× + Aleksič 1× + pod trakom 1× (20/20 izpolnjeno); SIDRA: r2 h22 3. VPIS (POŽEK signal — boter Janez Požek = h30 oče 1902/03; oče Nikolaj Milek = 1902 ISTI); r14 h87 3. VPIS (oče Marko Podrinec bajtar — KURRENT ISTI oče Pegdirec/Perdinec → Podrinec, NI menjava); r15 h15 8. VPIS (BRINEC signal — mati Marija Brinec); r16 h88 PRVI KRSTNI VPIS (oče Peter Brinec? + boter Janez Brinec? — 2. in 3. Brinec oseba leta 1904; hiša že v mrliški 04894/1886); r18 h24 11. VPIS (ŠE VEDNO najbolj vpisovana gibriljska hiša registra; 29. FEBRUAR — prestopno leto 1904, edini 29.2. vpis do 1904; črni pripis razveljavitve zakonske zveze 25.11.1947/29.12.1948; † 30.1.1983 Zagreb; boter Danijel Murn? = ISTI boter kot 1903 r1); r29 h54 5. VPIS; r31 h16 6. VPIS (Strausova/Spudičeva hiša — poročna 04455 lead ostaja odprt); r32 h60 6. VPIS; r38 h36 10. VPIS; r46 h6 NOVA (ŽELJKO signal — boter Nikol Željko + Marija Klepec); r65 h50 NOVA (ŠTRUCELJ signal — mati Doroteja Štrucelj = h22 rod 1902; boter Matija Pozdirec); r90 h42 NOVA (ŠTRAUS signal — oče Matija Štraus, 2. Strausova oseba 1904; ZADNJA vrstica leta); r78 h45 4. VPIS (SPUDIČ signal — mati Barbara Spudič; EMŠO 2610904505164 = 26.10.1904; † 14.10.2003 Metlika — 98 let, NAJDALJŠE življenje letnika 1904); r80 h91 4. VPIS (MUC KONTINUITETA potrjena — oče Janez Muc bajtar; 1895 Muc + 1902 Murov? [~] ISTA žena Kure); r82 h69 8. VPIS (ŽELJKO signal — oče Janez Željko bajtar); MILEK signali (r2 h22 oče + r73 h65 oče Matija Milek [1901 Mitek? KURRENT] + r57 h21 boter Matija Milek); MIH signal r69 (mati in babica ISTA — Marija Mih); EMŠO kampanja 1982–84 (pripisi »Šimonič Miri« + datumi 20.12.1982/28.12.1982/30.12.1982/12.6.1984) — sidra celo leto: r8 21.01., r45 28.06., r48 20.07., r77 25.10., r78 26.10., r79 28.10., r89 20.12.1904; ANOMALIJE: r19 (VSTAVLJEN vpis brez kraja/hiše — pripis matičarke Vesne Šimonič 15.05.2007; EMŠO 0303904505822 = 3.3.1904 moški (5) — NESKLADJE z ženskim imenom Jožefa; EXCLUDED), r18 (29.2. prestopno + razveljavitev zakona 1947/48), r24 (Mlake »preh. dvor« Marko — oče PRAZEN, mati »Marija Hudorovič cigarka«, babica »—« — najbolj obrobni vpis), r25/r26 (dvojčka Boginja vas 43 — oba † dojenčka: Rudolf 4 dni + Ana 8 dni; dva duhovnika Ravq?/Dostál), r36/r37 (dvojčka Vranovče 29 — oba † 9.3.1905 ~9 mes.), r41 + r84 (MRTVOROJENA »Z.mrtvorajen«, krsta »—«; r41 z botri + podpisom Ravq, r84 popolnoma prazen), r42 (TRETJI otrok Ane Jurajevič v 26 dneh — oče »Jožef Kržan/Krožan« NESKLADJE z r36/37), r45 (isti Martin Žugelj × DVE ženi < 6 mes. — MERI: smrt/ponovna poroka ali branje), r69 (hiša neberljiva — edini 1904 vpis brez hiše), r40 († 9.11.1918 — dan pred premirjem, 14 let); umrljivost dojenčkov 8 + mrtvorojena 2 + nezakonski 2; EXCLUDED: r19 (vstavljen vpis 2007 — ni ugotovljivo, ali gre za Griblje); skripta scripts/p99_parish_baptism_1904.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1904",
  "P99: PARISH OF PODZEMELJ — BAPTISM REGISTER 04105, THE FULL YEAR 1904 (issue #18; SAMPLE-TRANSCRIPTION-1904; MEASURES, does not decide; the v7 join unchanged): extending the P79 (1886) → … → P97 (1902) → P98 (1903) sample to 1904 — the frame: the heading '1904' BELOW r82 on p. 143 (scan 152, proven by P98; the 1904 r1 = Krasinec 37 Ana Jan 5/5 — the P98 lead confirmed) – row 90 on p. 150 (scan 160; the heading '1905' below r90 — the 1905 r1 = Gradac 45? Antonija — the P100 lead) == printed pages 143–150 (90 rows — THE LONGEST register year so far); THE P99 NOVEL: ONE duplicated scan pair (155/156 = p. 146, rows 35–46; s156 clearer); page == scan − 9 (152–155) / − 10 (157–160); the format = A NEW PRINTED register (as 1902–1903); ALL Griblje entries: 20 entries / 19 houses + 1 ILLEGIBLE (r69 the house under a blue note + diagonally crossed out — no vitals block): 22, 87, 15, 88, 24, 54, 16, 60, 36, 6, 66, 43, 21, 50, 65, 45, 91, 69, 42 — the NARE run's 10th year (each known house 1×; 1901 the only break with h12 ×2); 3 NEW HOUSES after two years without new ones: h6 (the PT set 1–40 — the first entry) + h42 and h50 (the 20th and 21st proven numbers of the gap 41–60 — only h51 remains!); h88 = the FIRST BAPTISM entry (the house already in the death register 04894/1886); the cumulative 313 entries / 84 houses across three books and NINETEEN years (307 vitals); the PT 13/6 (42/43/45/50/54/60 in the gap — 42 + 50 NEW, 43/45/54/60 already proven; the gap now 21 proven); PRIESTS (the whole year): Jos. Ravq 38× + Dostál 32× (Stanislav 29× — January titled 'Kaplan'; Flavi? 3× [~]) + THE NEW CURATE Hugo Hengsfeld 13× (from r67; 'Kapp.') — A CHANGE OF CURATES mid-year + illegible 5× + stillborn 2×; Kulbinek 0×; in Griblje: Dostál 10 (all Stanislav) + Ravq 8 + Hengsfeld 1 (r80) + illegible 1 (r90); the midwife (the whole year): 85 named / 5 empty (r24, r54, r55, r83, r86 '—') — in Griblje: Toter 10× + Mih 4× + Mavretič 3× + Delak 1× + Aleksič 1× + under a strip 1× (20/20 filled); ANCHORS: r2 h22 the 3rd ENTRY (the POŽEK signal — the godfather Janez Požek = the h30 father 1902/03; the father Nikolaj Milek = 1902 the SAME); r14 h87 the 3rd ENTRY (the father Marko Podrinec — the KURRENT father IS THE SAME, NO change); r15 h15 the 8th ENTRY (the BRINEC signal — the mother Marija Brinec); r16 h88 THE FIRST BAPTISM ENTRY (the father Peter Brinec? + the godfather Janez Brinec? — the 2nd and 3rd Brinec persons of 1904); r18 h24 the 11th ENTRY (STILL the most-entered Griblje house of the register; Feb 29 — THE LEAP YEAR 1904, the only Feb 29 entry up to 1904; the black note on the ANNULMENT of the marriage Nov 25, 1947/Dec 29, 1948; † Jan 30, 1983 Zagreb; the godfather Danijel Murn? = the SAME godfather as 1903 r1); r29 h54 the 5th ENTRY; r31 h16 the 6th ENTRY (the Straus/Spudič house — the marriage-register 04455 lead remains open); r32 h60 the 6th ENTRY; r38 h36 the 10th ENTRY; r46 h6 NEW (the ŽELJKO signal — the godfather Nikol Željko + Marija Klepec); r65 h50 NEW (the ŠTRUCELJ signal — the mother Doroteja Štrucelj = the h22 family 1902; the godfather Matija Pozdirec); r90 h42 NEW (the ŠTRAUS signal — the father Matija Štraus, the 2nd Straus person of 1904; THE LAST row of the year); r78 h45 the 4th ENTRY (the SPUDIČ signal — the mother Barbara Spudič; the personal ID 2610904505164 = Oct 26, 1904; † Oct 14, 2003 Metlika — 98 years, THE LONGEST life of the 1904 class); r80 h91 the 4th ENTRY (the MUC CONTINUITY proven — the father Janez Muc, a cottager; 1895 Muc + 1902 Murov? [~] the SAME wife Kure); r82 h69 the 8th ENTRY (the ŽELJKO signal — the father Janez Željko, a cottager); the MILEK signals (r2 the h22 father + r73 the h65 father Matija Milek [1901 Mitek? a KURRENT] + r57 the h21 godfather Matija Milek); the MIH signal r69 (the mother and the midwife THE SAME — Marija Mih); the personal-ID campaign 1982–84 (the notes 'Šimonič Miri' + the dates Dec 20, 1982/Dec 28, 1982/Dec 30, 1982/Jun 12, 1984) — the anchors of the whole year: r8 Jan 21, r45 Jun 28, r48 Jul 20, r77 Oct 25, r78 Oct 26, r79 Oct 28, r89 Dec 20, 1904; ANOMALIES: r19 (AN INSERTED entry without village/house — the note of the registrar Vesna Šimonič May 15, 2007; the personal ID 0303904505822 = Mar 3, 1904 a MALE (5) — a MISMATCH with the female name Jožefa; EXCLUDED), r18 (Feb 29 + the annulment 1947/48), r24 (Mlake 'preh. dvor' Marko — the father EMPTY, the mother 'Marija Hudorovič cigarka', the midwife '—' — the most marginal entry), r25/r26 (the twins of Boginja vas 43 — both † infants: Rudolf 4 days + Ana 8 days; two priests Ravq?/Dostál), r36/r37 (the twins of Vranovče 29 — both † Mar 9, 1905 ~9 months), r41 + r84 (STILLBORN 'Z.mrtvorajen', baptism '—'; r41 with godparents + the signature Ravq, r84 completely empty), r42 (the THIRD child of Ana Jurajevič in 26 days — the father 'Jožef Kržan/Krožan' a MISMATCH with r36/37), r45 (the same Martin Žugelj × TWO wives < 6 months — MERI: death/remarriage or reading), r69 (the house illegible — the only 1904 entry without a house), r40 († Nov 9, 1918 — the day before the armistice, 14 years); the infant mortality 8 + stillborn 2 + illegitimate 2; EXCLUDED: r19 (the inserted entry 2007 — not determinable whether Griblje); the script scripts/p99_parish_baptism_1904.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1904",
  p99Errors.length === 0,
  p99Errors.length === 0
    ? `20 vpisov / 19 hiš + 1 neberljiva (r69) — NARE 10. leto (vsaka znana hiša 1×) · okvir 1904 skeni 152 (str. 143, glava pod r82) – 160 row 90 (glava 1905 pod r90; 1905 r1 = Gradac 45? — P100 lead; 90 vrstic — najdaljše leto) · EN dup par (155/156) · 3 NOVE HIŠE (h6 nabor + h42/h50 = 20./21. dokazana luknja — ostaja samo h51) · h88 prvi KRSTNI vpis (mrliška 04894/1886) · PT 13/6 · Dostál 10 (vsi Stanislav) + Ravq 8 + NOV kaplan Hengsfeld 13× (menjava sredi leta) + Kulbinek 0× · babica Toter 10× (20/20; celo leto 85/5) · h24 11. VPIS — najbolj vpisovana hiša + 29.2. PRESTOPNI dan · h16 6. VPIS (Straus × Spudič) + h36 10. VPIS + h91 4. VPIS (MUC kontinuiteta) · SPUDIČ signal r78 (EMŠO 2610904505164; † 2003 — 98 let) + ŠTRAUS signal r90 + ŠTRUCELJ signal r65 + POŽEK signal r22 + ŽELJKO signali 2× + BRINEC signali 2× + MILEK signali + MIH signal r69 · EMŠO kampanja 1982–84 (7 sidr) · dvojčka r25/26 + r36/37 · mrtvorojena r41 + r84 · vstavljen vpis r19 EXCLUDED (EMŠO 2007) · umrljivost 8 + mrtvorojena 2 + nezakonski 2 · vitals 307 · kumulativ 313/84 DEVETNAJST let`
    : p99Errors.join("; "),
);
// ---------------------------------------------------------------------------
// qa-p100 — krstna 04105, polno leto 1905 (P100, issue #18)
// ---------------------------------------------------------------------------
// okvir 1905: skeni 160–169 (170 = glava 1906); stran == novela P100
// (dva dup para 164/165 + 168/169)
const p100PageOfScan = (s: number) =>
  s === 164 || s === 165 ? 154 : s === 168 || s === 169 ? 157 : s <= 164 ? s - 10 : s - 11;
const p100Hv = HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year === 1905);
const p100Errors: string[] = [];
if (p100Hv.length !== 16)
  p100Errors.push(`vpisov 1905 (04105, zasidrani) ≠ 16 (${p100Hv.length})`);
const p100Houses = new Set(p100Hv.map((h) => h.houseNo));
if (p100Houses.size !== 15)
  p100Errors.push(`različnih hiš ≠ 15 (${p100Houses.size}: ${[...p100Houses].sort((a, b) => Number(a) - Number(b)).join(",")})`);
// INTRA-LETNA PONOVITEV: h12 ×2 (NARE prelom — 2. primer po 1901)
const p100H12 = p100Hv.filter((h) => h.houseNo === "12");
if (p100H12.length !== 2)
  p100Errors.push(`h12 intra-letna ponovitev ≠ 2 bloka (${p100H12.length})`);
if (!p100H12.some((h) => h.whatSi.includes("Neža")) || !p100H12.some((h) => h.whatSi.includes("NARE PRELOM")))
  p100Errors.push("h12 NARE PRELOM (Neža r4 + Ana r15) ne ustreza");
// okvir: stran == sken po P100 noveli (dva dup para)
const p100BadPage = p100Hv.filter(
  (h) => h.status !== "DOCUMENTED" || !h.scan || !h.page
    || h.page !== p100PageOfScan(h.scan)
    || h.scan < 160 || h.scan > 169,
);
if (p100BadPage.length > 0)
  p100Errors.push(`scan/page ne ustreza P100 noveli: ${p100BadPage.map((h) => `${h.houseNo}@${h.scan}`).join(",")}`);
// 0 NOVIH hiš (vse 15 že dokumentirane pred 1905)
const p100PriorHouses = new Set(
  HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year !== 1905).map((h) => h.houseNo),
);
const p100New = [...p100Houses].filter((hn) => !p100PriorHouses.has(hn));
if (p100New.length !== 0)
  p100Errors.push(`nove hiše 1905 ≠ 0 (${p100New.join(",")})`);
// sidra: h39 18-letna vrzel + h11 15-letna vrzel + razveljavitev zakona h12
const p100H39 = p100Hv.find((h) => h.houseNo === "39");
if (!p100H39 || !p100H39.whatSi.includes("VRZEL 18 LET"))
  p100Errors.push("h39 VRZEL 18 LET (1886→1905 — najdaljša v vzorcu) manjka");
const p100H11 = p100Hv.find((h) => h.houseNo === "11");
if (!p100H11 || !p100H11.whatSi.includes("VRZEL 15 LET"))
  p100Errors.push("h11 VRZEL 15 LET (1890→1905) manjka");
const p100H4 = p100Hv.find((h) => h.houseNo === "12" && h.whatSi.includes("Neža"));
if (!p100H4 || !p100H4.whatSi.includes("RAZVELJAVITEV ZAKONA"))
  p100Errors.push("h12 r4 RAZVELJAVITEV ZAKONA (Novo mesto 23.5.1949) manjka");
// sidra kontinuitet: h6 2. zapored (ista botra), h58 Požek×Kambič, h25 Brinec×Šegina,
// h7 Jakob Toter, h42 menjava družine, h22 Milek, h66 Hrižan
const p100H6 = p100Hv.find((h) => h.houseNo === "6");
if (!p100H6 || !p100H6.whatSi.includes("2. VPIS ZAPORED") || !p100H6.whatSi.includes("Nikolaj Željko"))
  p100Errors.push("h6 2. VPIS ZAPORED + ISTA botra (Željko+Klepec) ne ustreza");
const p100H58 = p100Hv.find((h) => h.houseNo === "58");
if (!p100H58 || !p100H58.whatSi.includes("Janez Požek") || !p100H58.whatSi.includes("Katarina Kambič"))
  p100Errors.push("h58 ISTI PAR Požek × Kambič (P98 rešitev 3. potrditev) ne ustreza");
const p100H25 = p100Hv.find((h) => h.houseNo === "25");
if (!p100H25 || !p100H25.whatSi.includes("Matija Brinec") || !p100H25.whatSi.includes("Katarina Šegina"))
  p100Errors.push("h25 Brinec × Šegina (3. dokumentacija) ne ustreza");
const p100H7 = p100Hv.find((h) => h.houseNo === "7");
if (!p100H7 || !p100H7.whatSi.includes("Jakob Toter"))
  p100Errors.push("h7 Jakob Toter (1901 par) ne ustreza");
const p100H42 = p100Hv.find((h) => h.houseNo === "42");
if (!p100H42 || !p100H42.whatSi.includes("MENJAVA DRUŽINE"))
  p100Errors.push("h42 MENJAVA DRUŽINE (1904 Štraus → 1905 Perdinec/Pezdirec) manjka");
const p100H22 = p100Hv.find((h) => h.houseNo === "22");
if (!p100H22 || !p100H22.whatSi.includes("Nikolaj Milek") || !p100H22.whatSi.includes("Ana Požek"))
  p100Errors.push("h22 Milek (1904 oče) + botra Ana Požek ne ustreza");
const p100H66 = p100Hv.find((h) => h.houseNo === "66");
if (!p100H66 || !p100H66.whatSi.includes("Hrižan"))
  p100Errors.push("h66 Hrižan signal (2. VPIS ZAPORED) ne ustreza");
// kontinuitete (zadnja leta pred 1905; pini po očetu/materi/botru — prior ALI current)
const p100Pins: Array<[string, number, string]> = [
  ["1", 1900, "Željko"],
  ["5", 1903, "Štrucelj"],
  ["6", 1904, "Željko"],
  ["7", 1901, "Toter"],
  ["11", 1890, "Zumik"],
  ["12", 1903, "Dragoš"],
  ["22", 1904, "Milek"],
  ["23", 1903, "Južna"],
  ["25", 1902, "Brinec"],
  ["34", 1903, "SEGINA"],
  ["39", 1886, "Šimec"],
  ["42", 1904, "Štraus"],
  ["48", 1898, "Berkop"],
  ["58", 1903, "Požek"],
  ["66", 1904, "Hrižan"],
];
for (const [hn, yr, pin] of p100Pins) {
  const prior = HOUSE_VITALS.find((h) => h.bookSignature === "04105" && h.houseNo === hn && h.year === yr);
  const cur = p100Hv.find((h) => h.houseNo === hn);
  if (!prior || !cur) {
    p100Errors.push(`kontinuiteta hiša ${hn} (${yr} → 1905) manjka`);
    continue;
  }
  if (!prior.whatSi.includes(pin) && !cur.whatSi.includes(pin))
    p100Errors.push(`kontinuiteta hiša ${hn} (${yr}, pin ${pin}) ne ustreza`);
}
// vitals skupaj 449 (po P106: 429 + 20; krstna 1911)
if (HOUSE_VITALS.length !== 685)
  p100Errors.push(`HOUSE_VITALS ≠ 467 (${HOUSE_VITALS.length})`);
// babica: 16/16 blokov; Toter 12× + Mih 3× + Kambič 1×
if (p100Hv.filter((h) => h.whatSi.includes("babica")).length !== 16)
  p100Errors.push(`babica ni v vseh 16 whatSi (${p100Hv.filter((h) => h.whatSi.includes("babica")).length})`);
if (p100Hv.filter((h) => h.whatSi.includes("Marjeta Toter")).length !== 12)
  p100Errors.push(`babica Marjeta Toter ≠ 12× (${p100Hv.filter((h) => h.whatSi.includes("Marjeta Toter")).length})`);
const p100Mih = p100Hv.filter((h) => h.whatSi.includes("Mih Marija") || h.whatSi.includes("Mih [~ Muh] Marija")).length; // h34 r19 = varianta »Mih [~ Muh] Marija« (dokaz babica='Mih [~ Muh] Marija')
if (p100Mih !== 3)
  p100Errors.push(`babica Mih Marija ≠ 3× (${p100Mih})`);
if (p100Hv.filter((h) => h.whatSi.includes("Ana Kambič?")).length !== 1)
  p100Errors.push(`babica Ana Kambič? (r69) ≠ 1× (${p100Hv.filter((h) => h.whatSi.includes("Ana Kambič?")).length})`);
// duhovniki (bloki): Ravq 7 + Hengsfeld 8 + odrezan 1 (r15); Kulbinek 0×
if (p100Hv.filter((h) => h.whatSi.includes("Jos. Ravq")).length !== 7)
  p100Errors.push(`podpis Jos. Ravq ≠ 7× (${p100Hv.filter((h) => h.whatSi.includes("Jos. Ravq")).length})`);
if (p100Hv.filter((h) => h.whatSi.includes("Hengsfeld")).length !== 8)
  p100Errors.push(`podpis Hengsfeld ≠ 8× (${p100Hv.filter((h) => h.whatSi.includes("Hengsfeld")).length})`);
if (p100Hv.some((h) => h.whatSi.includes("Kulbinek")))
  p100Errors.push("Kulbinek 0× pričakovano — najden v whatSi");
// EMŠO sidra: r4 (1201905505202) + r14 (0302905505218) + r19 (0103905505058) + r49 (0607905500076 neskladje)
const p100Emso = p100Hv.filter((h) => h.whatSi.includes("EMŠO"));
if (p100Emso.length < 4) // dokaz: 4 EMŠO sidra na Gribljih (r4/r14/r19/r49); 17 = celo knjigo
  p100Errors.push(`EMŠO sidrov v blokih < 4 (${p100Emso.length})`);
if (!p100H4 || !p100H4.whatSi.includes("1201905505202"))
  p100Errors.push("EMŠO sidro r4 (1201905505202) manjka");
const p100H19 = p100Hv.find((h) => h.houseNo === "34");
if (!p100H19 || !p100H19.whatSi.includes("0103905505058"))
  p100Errors.push("EMŠO sidro r19 (0103905505058) manjka");
push(
  "qa-p100-parish-baptism-1905",
  "P100: ŽUPNIJA PODZEMELJ — KRSTNA KNJIGA 04105, POLNO LETO 1905 (issue #18; SAMPLE-TRANSCRIPTION-1905; MERI, NE odloča; v7 join nespremenjen): širitev vzorca P79 (1886) → … → P98 (1903) → P99 (1904) na leto 1905 — okvir: glava »1905« POD r90 na str. 150 (sken 160, P99 dokazano; 1905 r1 = Gradac 45 Antonija 2./7. Januar — P99 lead potrjen) – row 87 na str. 157 (sken 169; glava »1906« na str. 158 = sken 170/171 — 1906 r1 = »Gorn?« 34 Jožef 1./1. — P101 lead) == tiskane strani 150–157 (87 vrstic); NOVELA P100: DVA podvojena para skenov (164/165 = str. 154, rows 40–51; 168/169 = str. 157, rows 76–87) + dup par 170/171 (str. 158) = ŽE 1906; stran == sken − 10 (160–164) / − 11 (165–168) / − 12 (169–170) / − 13 (171+); format = spread (levo data, desno Roditelja/Botra/Babica — naslov razporejen čez obe strani); VSI vpisi z Griblji: 16 vpisov / 15 hiš: 1, 5, 6, 7, 11, 12×2, 22, 23, 25, 34, 39, 42, 48, 58, 66 — NARE PRELOM (h12 ×2: r4 Neža + r15 Ana — 2. intra-letna ponovitev po 1901; več-družinska hiša); 0 NOVIH hiš (vse 15 že dokumentirane); h42 (NOVA 1904) se ponovi že 1905 — MENJAVA DRUŽINE (Štraus → Perdinec/Pezdirec); LETO VELIKIH VRZELI: h39 18 let (1886→1905 — NAJDALJŠA v vzorcu!), h11 15 let (1890→1905), h1 4 leta (1900→1905), h66 17 let (1887→1904 prejšnja faza); kumulativ 329 vpisov / 84 hiš čez tri knjige in DVAJSET let (323 vitals); PT 12/3 (42/48/58 v luknji — vsi ponovitve; luknja 41–60 ostaja samo h51); DUHOVNIKI (celo leto 87): Hugo/H. Hengsfeld 54× dominant + Jos. Ravq 26× + Dostál 1× [~ r43 »Janez Dostál?«] + neberljivo 5× (r1–r3, r15, r27 odrezani); na Gribljih: Ravq 7 + Hengsfeld 8 + odrezan 1; babica (celo leto): 78 imenovanih / 5 praznih (r30, r37, r44, r46, r79 »—«) / 3 neberljive (r1–r3 odrezani, r72 ditto) — na Gribljih 16/16: Toter 12× + Mih 3× + Kambič [~] 1×; SIDRA: r4 h12 9. VPIS (Janez Dragoš — 1892–1899 linija) + RAZVELJAVITEV ZAKONA (sodišče Novo mesto 23.5.1949 — 1. gribeljska razveljavitev v krstni knjigi!) + EMŠO 1201905505202; r14 h5 3. VPIS (Matija Štrucelj = 1903 oče); r15 h12 10. VPIS (NARE prelom); r19 h34 4. VPIS (SEGINA signal — boter Nikolaj Šegina + HRIŽAN); r28 h39 2. VPIS (VRZEL 18 LET); r29 h42 2. VPIS (MENJAVA DRUŽINE); r31 h11 3. VPIS (VRZEL 15 LET); r42 h23 6. VPIS (Matija Brinec); r49 h6 2. VPIS ZAPORED (ISTI starša + ISTA botra Nikolaj Željko + Marija Klepec kot 1904! + vijolični pripis »Po odloči Okrajnega sodišča v Črnomelju« + EMŠO 0607905500076 NESKLADJE SPOLA — ime Janez moški, EMŠO ženski znak); r50 h7 3. VPIS (Jakob Toter × Katarina Jakobšič — 1901 par); r57 h48 2. VPIS (vrzel 7 let); r62 h22 4. VPIS (Nikolaj Milek — 1904 oče; botra Ana Požek — POŽEK signal; žena Ana Milek † 1982 Griblje); r65 h1 6. VPIS (Jurij Željko — ŽELJKO signal); r66 h25 5. VPIS (Brinec × Šegina — 3. dokumentacija); r69 h58 8. VPIS (Požek × Kambič — P98 rešitev 3. potrditev!; † 26.2.1906 dojenček); r82 h66 3. VPIS (Hrižan signal; † 1944 — 2. svetovna vojna); EMŠO kampanja 1982–84 (17 sidr); ANOMALIJE: r8 Gradac 55 VSTAVLJEN vpis 03.09.2007 (2. primer po P99 r19; non-Griblje), r49 (vijolični sodni pripis + EMŠO neskladje spola), r71/r72 Boršt 19 dvojčka (ditto vrstica), r85 Gradac žandar Wachtmeister (2. po 1903 Morvet), r76/r79/r84 »Hudorovac samska ciganka« nezakonski + legitimizacija 1915, r73 razveza Zagreb; † dojenčka r66 (17/11.1905?) + r69 (26.2.1906); EXCLUDED: 4 (r2 pripis pokrije kraj/hišo, r3 + r27 odrezani v skenih, r40 bela nalepka); skripta scripts/p100_parish_baptism_1905.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1905",
  "P100: PARISH OF PODZEMELJ — BAPTISM REGISTER 04105, THE FULL YEAR 1905 (issue #18; SAMPLE-TRANSCRIPTION-1905; MEASURES, does not decide; the v7 join unchanged): extending the P79 (1886) → … → P99 (1904) sample to 1905 — the frame: the heading '1905' BELOW r90 on p. 150 (scan 160, proven by P99; the 1905 r1 = Gradac 45 Antonija Jan 2/7 — the P99 lead confirmed) – row 87 on p. 157 (scan 169; the heading '1906' on p. 158 = scan 170/171 — the 1906 r1 = 'Gorn?' 34 Jožef — the P101 lead) == printed pages 150–157 (87 rows); THE P100 NOVEL: TWO duplicated scan pairs (164/165 = p. 154; 168/169 = p. 157) + the dup pair 170/171 (p. 158) = ALREADY 1906; page == scan − 10 (160–164) / − 11 (165–168) / − 12 (169–170) / − 13 (171+); the format = a spread (left data, right Roditelja/Botra/Babica — the title across both pages); ALL Griblje entries: 16 entries / 15 houses: 1, 5, 6, 7, 11, 12×2, 22, 23, 25, 34, 39, 42, 48, 58, 66 — the NARE BREAK (h12 ×2: r4 Neža + r15 Ana — the 2nd intra-year repeat after 1901; a multi-family house); 0 NEW houses (all 15 already documented); h42 (NEW 1904) repeats already in 1905 — a FAMILY CHANGE (Štraus → Perdinec/Pezdirec); THE YEAR OF BIG GAPS: h39 18 years (1886→1905 — THE LONGEST in the sample!), h11 15 years (1890→1905), h1 4 years (1900→1905); the cumulative 329 entries / 84 houses across three books and TWENTY years (323 vitals); the PT 12/3 (42/48/58 in the gap — all repeats; only h51 remains unproven); PRIESTS (the whole year 87): Hugo/H. Hengsfeld 54× dominant + Jos. Ravq 26× + Dostál 1× [~] + illegible 5× (cut rows); in Griblje: Ravq 7 + Hengsfeld 8 + cut 1; the midwife (the whole year): 78 named / 5 empty / 3 illegible — in Griblje 16/16: Toter 12× + Mih 3× + Kambič [~] 1×; ANCHORS: r4 h12 the 9th ENTRY + the MARRIAGE ANNULMENT (the Novo mesto court May 23, 1949 — the 1st Griblje annulment in the baptism register!) + the personal ID 1201905505202; r14 h5 the 3rd ENTRY (Matija Štrucelj = the 1903 father); r15 h12 the 10th ENTRY (the NARE break); r19 h34 the 4th ENTRY (the SEGINA signal); r28 h39 the 2nd ENTRY (an 18-YEAR GAP); r29 h42 the 2nd ENTRY (a FAMILY CHANGE); r31 h11 the 3rd ENTRY (a 15-YEAR GAP); r42 h23 the 6th ENTRY (Matija Brinec); r49 h6 the 2nd CONSECUTIVE ENTRY (the same parents + the SAME godparents Nikolaj Željko + Marija Klepec as 1904! + the violet court note + the personal-ID SEX MISMATCH); r50 h7 the 3rd ENTRY (Jakob Toter × Katarina Jakobšič — the 1901 couple); r57 h48 the 2nd ENTRY (a 7-year gap); r62 h22 the 4th ENTRY (Nikolaj Milek — the 1904 father; the godmother Ana Požek — the POŽEK signal); r65 h1 the 6th ENTRY (Jurij Željko — the ŽELJKO signal); r66 h25 the 5th ENTRY (Brinec × Šegina — the 3rd documentation); r69 h58 the 8th ENTRY (Požek × Kambič — the P98 resolution confirmed the 3rd time!; † Feb 26, 1906 an infant); r82 h66 the 3rd ENTRY (the Hrižan signal; † 1944 WWII); the personal-ID campaign 1982–84 (17 anchors); ANOMALIES: r8 Gradac 55 AN INSERTED entry Sep 3, 2007 (the 2nd case after P99 r19), r49 (the violet court note + the sex mismatch), r71/r72 the twins of Boršt 19 (a ditto row), r85 Gradac a gendarme Wachtmeister (the 2nd after 1903 Morvet), r76/r79/r84 'Hudorovac samska ciganka' illegitimate + the legitimization 1915, r73 the Zagreb divorce; the infants † r66 + r69; EXCLUDED: 4 (r2 a note covers, r3 + r27 cut off, r40 a white sticker); the script scripts/p100_parish_baptism_1905.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1905",
  p100Errors.length === 0,
  p100Errors.length === 0
    ? `16 vpisov / 15 hiš — NARE PRELOM (h12 ×2: Neža + Ana — 2. po 1901) · okvir 1905 skeni 160 (str. 150, glava pod r90) – 169 row 87 (glava 1906 na str. 158; 87 vrstic) · DVA dup para (164/165 + 168/169; 170/171 = 1906) · 0 NOVIH hiš · h42 MENJAVA DRUŽINE (Štraus → Perdinec/Pezdirec) · LETO VELIKIH VRZELI: h39 18 let (najdaljša!) + h11 15 let · RAZVELJAVITEV ZAKONA h12 (Novo mesto 1949 — 1. gribeljska) · h6 2. VPIS ZAPORED (ista botra!) · h58 8. VPIS (Požek×Kambič 3. potrditev) · h25 Brinec×Šegina · h66 †1944 · PT 12/3 · Hengsfeld 54 + Ravq 26 (celo leto) · babica Toter 12× (16/16; celo leto 78/5) · EMŠO kampanja 17 sidr (r49 neskladje spola) · vstavljen vpis r8 (2007) · žandar r85 · ciganka mreža r76/79/84 · EXCLUDED 4 (pripis + 2 odrezani + nalepka) · vitals 323 · kumulativ 329/84 DVAJSET let`
    : p100Errors.join("; "),
);

// qa-p101 — krstna 04105, polno leto 1906 (P101, issue #18)
// ---------------------------------------------------------------------------
// okvir 1906: skeni 170/171 (glava, dup) + 172–178; stran == novela P101
// (en nov dup par 178/179 = str. 165)
const p101PageOfScan = (s: number) =>
  s === 170 || s === 171 ? 158 : s === 178 || s === 179 ? 165 : s <= 178 ? s - 13 : s - 14;
const p101Hv = HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year === 1906);
const p101Errors: string[] = [];
if (p101Hv.length !== 18)
  p101Errors.push(`vpisov 1906 (04105, zasidrani) ≠ 18 (${p101Hv.length})`);
const p101Houses = new Set(p101Hv.map((h) => h.houseNo));
if (p101Houses.size !== 18)
  p101Errors.push(`različnih hiš ≠ 18 (${p101Houses.size}: ${[...p101Houses].sort((a, b) => Number(a) - Number(b)).join(",")})`);
// NARE ponovno: 0 intra-letnih ponovitev (r39 Otok 20 + r54 Griblje 20 = ločena hiši)
const p101Repeat = p101Houses.size !== p101Hv.length;
if (p101Repeat)
  p101Errors.push("1906 pričakovano NARE (vsaka hiša 1×) — najdena ponovitev");
// okvir: stran == sken po P101 noveli (dup par 178/179)
const p101BadPage = p101Hv.filter(
  (h) => h.status !== "DOCUMENTED" || !h.scan || !h.page
    || h.page !== p101PageOfScan(h.scan)
    || h.scan < 170 || h.scan > 178,
);
if (p101BadPage.length > 0)
  p101Errors.push(`scan/page ne ustreza P101 noveli: ${p101BadPage.map((h) => `${h.houseNo}@${h.scan}`).join(",")}`);
// 1 NOVA hiša: h4 (prvi krstni vpis — 85. hiša v vitals)
const p101PriorHouses = new Set(
  HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year !== 1906).map((h) => h.houseNo),
);
const p101New = [...p101Houses].filter((hn) => !p101PriorHouses.has(hn));
if (p101New.length !== 1 || !p101New.includes("4"))
  p101Errors.push(`nove hiše 1906 ≠ [4] (${p101New.join(",") || "brez"})`);
// sidra: h4 NOVA + h42 3. ZAPORED + h24 12. VPIS + h69 9. VPIS + h34 menjava 2×
// + h60 par povrat + h19 NEZAKONSKI + h15 ŠTRAUS + h21 POŽEK + h26 ŠEGINA
const p101H4 = p101Hv.find((h) => h.houseNo === "4");
if (!p101H4 || !p101H4.whatSi.includes("NOVA HIŠA") || !p101H4.whatSi.includes("Janez Hrižan"))
  p101Errors.push("h4 NOVA HIŠA + oče Janez Hrižan ne ustreza");
const p101H42 = p101Hv.find((h) => h.houseNo === "42");
if (!p101H42 || !p101H42.whatSi.includes("3. VPIS ZAPORED") || !p101H42.whatSi.includes("Pozdirec"))
  p101Errors.push("h42 3. VPIS ZAPORED (Pezdirec/Pozdirec ista družina) ne ustreza");
const p101H24 = p101Hv.find((h) => h.houseNo === "24");
if (!p101H24 || !p101H24.whatSi.includes("12. VPIS") || !p101H24.whatSi.includes("najbolj vpisovana"))
  p101Errors.push("h24 12. VPIS (najbolj vpisovana hiša registra) ne ustreza");
const p101H69 = p101Hv.find((h) => h.houseNo === "69");
if (!p101H69 || !p101H69.whatSi.includes("9. VPIS") || !p101H69.whatSi.includes("Janez Željko"))
  p101Errors.push("h69 9. VPIS (isti oče Janez Željko bajtar) ne ustreza");
const p101H34 = p101Hv.find((h) => h.houseNo === "34");
if (!p101H34 || !p101H34.whatSi.includes("MENJAVA DRUŽINE 2×") || !p101H34.whatSi.includes("Janez Simec"))
  p101Errors.push("h34 MENJAVA DRUŽINE 2× (Šimec povrat) ne ustreza");
const p101H60 = p101Hv.find((h) => h.houseNo === "60");
if (!p101H60 || !p101H60.whatSi.includes("5. OTROK") || !p101H60.whatSi.includes("Nikolaj Željko"))
  p101Errors.push("h60 par Željko × Brodarič POVRAT (5. otrok istega para) ne ustreza");
const p101H19 = p101Hv.find((h) => h.houseNo === "19");
if (!p101H19 || !p101H19.whatSi.includes("NEZAKONSKI") || p101H19.whatSi.includes("oče Janez"))
  p101Errors.push("h19 NEZAKONSKI (očetova kolona prazna) ne ustreza");
const p101H15 = p101Hv.find((h) => h.houseNo === "15");
if (!p101H15 || !p101H15.whatSi.includes("ŠTRAUS signal") || !p101H15.whatSi.includes("Marjeta Simec"))
  p101Errors.push("h15 ŠTRAUS signal (Matija Štraus × Marjeta Simec — 2. par) ne ustreza");
const p101H21 = p101Hv.find((h) => h.houseNo === "21");
if (!p101H21 || !p101H21.whatSi.includes("POŽEK signal") || !p101H21.whatSi.includes("Janez Požek"))
  p101Errors.push("h21 POŽEK signal (oče = h58 oče 1903+1905) ne ustreza");
const p101H26 = p101Hv.find((h) => h.houseNo === "26");
if (!p101H26 || !p101H26.whatSi.includes("ŠEGINA signal") || !p101H26.whatSi.includes("VRZEL 10 LET"))
  p101Errors.push("h26 ŠEGINA signal + VRZEL 10 LET ne ustreza");
// kontinuitete (zadnja leta pred 1906; pini po očetu/znakih — prior ALI current)
const p101Pins: Array<[string, number, string]> = [
  ["15", 1904, "ŠTRAUS signal"],
  ["16", 1904, "7. VPIS"],
  ["18", 1898, "VRZEL 8 LET"],
  ["19", 1901, "2. VPIS"],
  ["20", 1903, "Perdinec"],
  ["21", 1904, "POŽEK signal"],
  ["24", 1904, "Jurajevič"],
  ["26", 1896, "VRZEL 10 LET"],
  ["27", 1902, "8. VPIS"],
  ["30", 1903, "Segina"],
  ["34", 1905, "Šulak"],
  ["35", 1903, "5. VPIS"],
  ["42", 1905, "MENJAVA DRUŽINE"],
  ["44", 1901, "3. VPIS"],
  ["49", 1899, "Brodarič"],
  ["60", 1904, "Novak"],
  ["69", 1904, "Željko"],
];
for (const [hn, yr, pin] of p101Pins) {
  const prior = HOUSE_VITALS.find((h) => h.bookSignature === "04105" && h.houseNo === hn && h.year === yr);
  const cur = p101Hv.find((h) => h.houseNo === hn);
  if (!prior || !cur) {
    p101Errors.push(`kontinuiteta hiša ${hn} (${yr} → 1906) manjka`);
    continue;
  }
  if (!prior.whatSi.includes(pin) && !cur.whatSi.includes(pin))
    p101Errors.push(`kontinuiteta hiša ${hn} (${yr}, pin ${pin}) ne ustreza`);
}
// vitals skupaj 449 (po P106: 429 + 20; krstna 1911)
if (HOUSE_VITALS.length !== 685)
  p101Errors.push(`HOUSE_VITALS ≠ 467 (${HOUSE_VITALS.length})`);
// babica: 18/18 blokov; Toter 0× (NOVELA — prvič!) + Mih 10× + Vötter 5×
if (p101Hv.filter((h) => h.whatSi.includes("babica")).length !== 18)
  p101Errors.push(`babica ni v vseh 18 whatSi (${p101Hv.filter((h) => h.whatSi.includes("babica")).length})`);
if (p101Hv.some((h) => h.whatSi.includes("Marjeta Toter")))
  p101Errors.push("babica Marjeta Toter 0× pričakovano (NOVELA — prvič v vzorcu) — najdena");
const p101Mih = p101Hv.filter((h) => h.whatSi.includes("Marija Mih")).length; // vključno r8 »Marija Mihelič [~ Mih?]«
if (p101Mih !== 10)
  p101Errors.push(`babica Marija Mih (+Mihelič[~]) ≠ 10× (${p101Mih})`);
if (p101Hv.filter((h) => h.whatSi.includes("Vötter")).length !== 5)
  p101Errors.push(`babica Marjeta Vötter ≠ 5× (${p101Hv.filter((h) => h.whatSi.includes("Vötter")).length})`);
// duhovniki (bloki): Ravq 7 + Kulbinek 6 + Škrabec 3 + Hengsfeld 2 — NOVELA
if (p101Hv.filter((h) => h.whatSi.includes("Jos. Ravq")).length !== 7)
  p101Errors.push(`podpis Jos. Ravq ≠ 7× (${p101Hv.filter((h) => h.whatSi.includes("Jos. Ravq")).length})`);
if (p101Hv.filter((h) => h.whatSi.includes("Kulbinek")).length !== 6)
  p101Errors.push(`podpis Kulbinek (o.t.cap.) ≠ 6× (${p101Hv.filter((h) => h.whatSi.includes("Kulbinek")).length})`);
if (p101Hv.filter((h) => h.whatSi.includes("Škrabec")).length !== 3)
  p101Errors.push(`podpis Škrabec (coop.) ≠ 3× (${p101Hv.filter((h) => h.whatSi.includes("Škrabec")).length})`);
if (p101Hv.filter((h) => h.whatSi.includes("Hengsfeld")).length !== 2)
  p101Errors.push(`podpis Hengsfeld ≠ 2× (${p101Hv.filter((h) => h.whatSi.includes("Hengsfeld")).length})`);
// EMŠO sidra: r16 (2102906500234) + r51 (3107906505454) + r62 (0609906500161)
const p101Emso = p101Hv.filter((h) => h.whatSi.includes("(sidro)")); // r16/r51/r62; r54 omenja EMŠO 1903 v zgodovinskem kontekstu
if (p101Emso.length !== 3)
  p101Errors.push(`EMŠO sidrov v blokih ≠ 3 (${p101Emso.length})`);
for (const emso of ["2102906500234", "3107906505454", "0609906500161"]) {
  if (!p101Hv.some((h) => h.whatSi.includes(emso)))
    p101Errors.push(`EMŠO sidro ${emso} manjka`);
}
push(
  "qa-p101-parish-baptism-1906",
  "P101: ŽUPNIJA PODZEMELJ — KRSTNA KNJIGA 04105, POLNO LETO 1906 (issue #18; SAMPLE-TRANSCRIPTION-1906; MERI, NE odloča; v7 join nespremenjen): širitev vzorca P79 (1886) → … → P99 (1904) → P100 (1905) na leto 1906 — okvir: glava »1906« na str. 158 = sken 170/171 (dup par, P100 dokazano; 1906 r1 = »Gorn?« 34 Jožef 1./1. Januar, H. Hengsfeld — P100 lead POTRJEN) – row 87 na str. 165 (skeni 178/179; glava »1907« POD r87; 1907 r1 = Dobravice 27 Ivanka, podpis Anton Dostál — P102 lead) == tiskane strani 158–165 (87 vrstic); NOVELA P101: EN podvojen par skenov v okviru leta — 178/179 = str. 165 (rows 85–87); stran == sken − 13 (172–178) / − 14 (180+); format = spread (kot 1905); VSI vpisi z Griblji: 18 vpisov / 18 hiš: 4, 15, 16, 18, 19, 20, 21, 24, 26, 27, 30, 34, 35, 42, 44, 49, 60, 69 — NARE ponovno (vsaka hiša 1× — po 1905 prelomu h12 ×2 spet brez intra-letne ponovitve; r39 Otok 20 + r54 Griblje 20 = ločena hiši, kraj forenzika!); 1 NOVA hiša: h4 (85. hiša v vitals — 1. nova po dveh letih 1904+1905 brez novih; h4 JE v PT naboru); PT 14/4 (42+44+49+60 v luknji 41–60 — vsi ponovitve že dokazanih; luknja ostaja samo h51); kumulativ 347 vpisov / 85 hiš čez tri knjige in ENAINDVajset let (341 vitals); SIDRA: r8 h16 7. VPIS (NOVA DRUŽINA Jakofčič; † 16.2.1944 — 2. svetovna vojna); r16 h49 2. VPIS (MENJAVA ŽENE Milek → Miheč [MERI]; EMŠO 2102906500234 sidro; BRODARIČ↔ŽELJKO izmena z r19); r18 h34 5. VPIS — MENJAVA DRUŽINE 2× (Šimec 1887 → Šilak/Šulak 1899–1905 → Šimec 1906 POVRAT, druga žena Kere); r19 h60 7. VPIS — PAR Željko × Brodarič POVRAT po 1904 intermezzu (5. OTROK istega para: 1893+1894+1897+1899 → 1906; botrinja Marija Klepec 3.×); r35 h19 2. VPIS — NEZAKONSKI (očetova kolona PRAZNA, mati Ana Kovač [~] samostojna — edini gibriljski v letu); r40 h44 3. VPIS (ŠTRUCELJ oče + HRIŽAN boter; PRVI KULBINEK podpis!); r43 h30 10. VPIS (MENJAVA Segina → Brinec); r48 h21 6. VPIS (POŽEK signal — oče Janez Požek = h58 oče 1903+1905!); r51 h4 NOVA HIŠA (HRIŽAN oče + ŠTRUCELJ mati + ŠTRAUS boter = h42 oče 1904 + h16 oče 1902 + h15 oče 1906!; EMŠO 3107906505454 sidro; DVOJNI modri pripis: umrl 1994 + umrla 2004); r52 h18 2. VPIS (VRZEL 8 LET; † 24.12.06 — božični večer); r54 h20 5. VPIS (ISTA DRUŽINA Perdinec/Pozdirec × Klepec kot 1903 — kurrent priimka); r56 h42 3. VPIS ZAPORED (Pezdirec/Pozdirec × Jurajevič/Jurasovič — ista družina 2. leto; Jožef = brat Jurija 1905? MERI); r62 h24 12. VPIS — ŠE VEDNO najbolj vpisovana hiša registra (POVRAT Brincove hiše 1887–1897; EMŠO 0609906500161 sidro); r66 h69 9. VPIS (isti oče Janez Željko bajtar; mati varianta Žumič → Zamec); r71 h26 4. VPIS (VRZEL 10 LET; ŠEGINA signal — oče = h30 oče 1902/1903!; podpis izblidla); r79 h27 8. VPIS (HRIŽAN botrinja Katarina = h34 botrinja 1903!; PEZDIREC oče); r85 h35 5. VPIS (HRIŽAN ×2 — mati + botrinja; PEZDIREC oče); r86 h15 6. VPIS (ŠTRAUS signal — lead 04455 na 4. hiši h45→h40→h16→h15, VENDAR mati Marjeta Simec NE Barbura Spudič — 2. Štrausov par [MERI]; ŠTRUCELJ boter); DUHOVNIKI NOVELA (celo leto 87): Jos. Ravq 39× + NOV KAPLAN J. R. Kulbinek (o.t.cap.) 20× (prvi podpis r38 = 12.5.1906!) + Hugo Hengsfeld 17× (samo Januar–April) + NOV coop. P. Kazimir Škrabec 7× (r76–r79 + r85–r87) + Dostál 1× (DUALNI podpis r30!) + prazni 4× (mrtvorojeni); na Gribljih 18/18: Ravq 7 + Kulbinek 6 + Škrabec 3 + Hengsfeld 2; BABICA NOVELA: TOTER 0× — PRVIČ v vzorcu (1886–1906)!!; Marjeta Vötter 5× na Gribljih (zapisi Sotter 1889 → Toter 1901–05 → Vötter 1906 — ista Marjeta? MERI); na Gribljih 18/18: Mih (+Mihelič[~]) 10 + Vötter 5 + Adlešič 1 + Burek[~] 1 + Dragoš 1; celo leto: 83 imenovanih / 1 prazna (r34) / 3 neberljive (r10 trak, r11+r12 nalepka); HRIŽAN kampanja 1906: 6 signalov na gibriljskih vrsticah (r40 boter Janez + r51 oče Janez + r71 boter Nikolaj + r79 botrinja Katarina + r85 mati Ana + botrinja Marija); PEZDIREC/POZDIREC očetje ×4 (r54 Peter + r56 Jožef + r79 Marko + r85 Jožef); ŠTRUCELJ signali ×3 (r40 oče + r51 mati + r86 boter); 5 dojenčkov † na Gribljih (svinčniki r48 29.1.1907 + r52 24.12.06 + r54 23.11.08 + r66 9.2.07 + r79 9.1.07); ANOMALIJE: 4 mrtvorojeni (r21/r22/r26/r29 — podpisi prazni), dualni podpis r30 (Hengsfeld + Dostál), ciganka mati r31 (Dobravice 48 — Hudorovac pattern), nezakonski r35, izblidla podpis r71, dvojčka r81/r82 (Krasinec 18), kraj forenzika r39 Otok 20 / r73 Prilozje 25 / r87 Grm 25; EXCLUDED: 10 (r11+r12 nalepka, 4 mrtvorojeni, r31 ciganka, r39 Otok, r73 Prilozje, r87 Grm); skripta scripts/p101_parish_baptism_1906.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1906",
  "P101: PARISH OF PODZEMELJ — BAPTISM REGISTER 04105, THE FULL YEAR 1906 (issue #18; SAMPLE-TRANSCRIPTION-1906; MEASURES, does not decide; the v7 join unchanged): extending the P79 (1886) → … → P100 (1905) sample to 1906 — the frame: the heading '1906' on p. 158 = scan 170/171 (a dup pair, proven by P100; the 1906 r1 = 'Gorn?' 34 Jožef Jan 1/1, H. Hengsfeld — the P100 lead CONFIRMED) – row 87 on p. 165 (scans 178/179; the heading '1907' BELOW r87; the 1907 r1 = Dobravice 27 Ivanka, signature Anton Dostál — the P102 lead) == printed pages 158–165 (87 rows); THE P101 NOVEL: ONE duplicated scan pair within the year — 178/179 = p. 165 (rows 85–87); page == scan − 13 (172–178) / − 14 (180+); the format = a spread (like 1905); ALL Griblje entries: 18 entries / 18 houses: 4, 15, 16, 18, 19, 20, 21, 24, 26, 27, 30, 34, 35, 42, 44, 49, 60, 69 — NARE again (each house once — after the 1905 break h12 ×2 again without an intra-year repeat; r39 Otok 20 + r54 Griblje 20 = two DIFFERENT houses, village forensics!); 1 NEW house: h4 (the 85th house in vitals — the first new one after two years 1904+1905 with none; h4 IS in the PT nabor); the PT 14/4 (42+44+49+60 in the gap 41–60 — all repeats of already-proven; only h51 remains); the cumulative 347 entries / 85 houses across three books and TWENTY-ONE years (341 vitals); ANCHORS: r8 h16 the 7th ENTRY (a NEW FAMILY Jakofčič; † Feb 16, 1944 — WWII); r16 h49 the 2nd ENTRY (a WIFE CHANGE Milek → Miheč [MERI]; personal ID 2102906500234 an anchor; the BRODARIČ↔ŽELJKO exchange with r19); r18 h34 the 5th ENTRY — a DOUBLE FAMILY CHANGE (Šimec 1887 → Šilak/Šulak 1899–1905 → Šimec 1906 RETURNS, a second wife Kere); r19 h60 the 7th ENTRY — the ŽELJKO × BRODARIČ COUPLE RETURNS after the 1904 intermezzo (the 5th CHILD of the same couple; the godmother Marija Klepec the 3rd time); r35 h19 the 2nd ENTRY — ILLEGITIMATE (the father's column EMPTY, mother Ana Kovač [~] unmarried — the only Griblje one in the year); r40 h44 the 3rd ENTRY (ŠTRUCELJ father + HRIŽAN godfather; the FIRST KULBINEK signature!); r43 h30 the 10th ENTRY (a CHANGE Segina → Brinec); r48 h21 the 6th ENTRY (the POŽEK signal — the father Janez Požek = the h58 father of 1903+1905!); r51 h4 A NEW HOUSE (the HRIŽAN father + the ŠTRUCELJ mother + the ŠTRAUS godfather = the h42 father 1904 + h16 father 1902 + h15 father 1906!; personal ID 3107906505454 an anchor; a DOUBLE blue note: died 1994 + died 2004); r52 h18 the 2nd ENTRY (an 8-YEAR GAP; † Dec 24, 06 — Christmas eve); r54 h20 the 5th ENTRY (the SAME FAMILY Perdinec/Pozdirec × Klepec as 1903 — a kurrent surname); r56 h42 the 3rd CONSECUTIVE ENTRY (Pezdirec/Pozdirec × Jurajevič/Jurasovič — the same family for a 2nd year; Jožef = Jurij's brother? MERI); r62 h24 the 12th ENTRY — STILL the most-entered house of the register (the BRINEC HOUSE RETURNS 1887–1897; personal ID 0609906500161 an anchor); r66 h69 the 9th ENTRY (the same father Janez Željko a cottager; the mother variant Žumič → Zamec); r71 h26 the 4th ENTRY (a 10-YEAR GAP; the SEGINA signal — the father = the h30 father 1902/1903!; a faded signature); r79 h27 the 8th ENTRY (the HRIŽAN godmother Katarina = the h34 godmother 1903!; the PEZDIREC father); r85 h35 the 5th ENTRY (the HRIŽAN ×2 — the mother + the godmother; the PEZDIREC father); r86 h15 the 6th ENTRY (the ŠTRAUS signal — the 04455 lead at a 4th house h45→h40→h16→h15, HOWEVER the mother Marjeta Simec NOT Barbura Spudič — a 2nd Štraus couple [MERI]; the ŠTRUCELJ godfather); PRIESTS NOVEL (the whole year 87): Jos. Ravq 39× + A NEW CHAPLAIN J. R. Kulbinek (o.t.cap.) 20× (the first signature r38 = May 12, 1906!) + Hugo Hengsfeld 17× (January–April only) + A NEW cooperator P. Kazimir Škrabec 7× (r76–r79 + r85–r87) + Dostál 1× (a DUAL signature r30!) + 4 empty (stillborn); in Griblje 18/18: Ravq 7 + Kulbinek 6 + Škrabec 3 + Hengsfeld 2; MIDWIFE NOVEL: TOTER 0× — FOR THE FIRST TIME in the sample (1886–1906)!!; Marjeta Vötter 5× in Griblje (the spellings Sotter 1889 → Toter 1901–05 → Vötter 1906 — the same Marjeta? MERI); in Griblje 18/18: Mih (+Mihelič[~]) 10 + Vötter 5 + Adlešič 1 + Burek[~] 1 + Dragoš 1; the whole year: 83 named / 1 empty / 3 illegible; the HRIŽAN campaign 1906: 6 signals on Griblje rows; the PEZDIREC/POZDIREC fathers ×4; the ŠTRUCELJ signals ×3; 5 infant deaths in Griblje (the pencils r48/r52/r54/r66/r79); ANOMALIES: 4 stillborn (empty signatures), a dual signature r30 (Hengsfeld + Dostál), a Gypsy mother r31 (Dobravice 48 — the Hudorovac pattern), the illegitimate r35, a faded signature r71, twins r81/r82 (Krasinec 18), the village forensics r39 Otok 20 / r73 Prilozje 25 / r87 Grm 25; EXCLUDED: 10 (r11+r12 a sticker, 4 stillborn, r31 the Gypsy, r39 Otok, r73 Prilozje, r87 Grm); the script scripts/p101_parish_baptism_1906.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1906",
  p101Errors.length === 0,
  p101Errors.length === 0
    ? `18 vpisov / 18 hiš — NARE ponovno (0 ponovitev; r39 Otok 20 ≠ r54 Griblje 20!) · okvir 1906 skeni 170/171 (glava, P100 lead POTRJEN) – 178/179 row 87 (glava 1907 pod r87; 87 vrstic) · NOVELA: EN dup par (178/179 = str. 165) · stran == sken − 13/− 14 · 1 NOVA hiša h4 (85. vitals; prva po dveh letih) · PT 14/4 · h42 3. VPIS ZAPORED · h24 12. VPIS (najbolj vpisovana) · h34 MENJAVA 2× (Šimec povrat) · h60 par Željko×Brodarič POVRAT (5. otrok) · h19 NEZAKONSKI · h15 ŠTRAUS (2. par!) · h21 POŽEK · h26 ŠEGINA + VRZEL 10 LET · BRODARIČ↔ŽELJKO izmena · HRIŽAN kampanja 6 · PEZDIREC očetje 4 · ŠTRUCELJ 3 · Kulbinek NOV kaplan (o.t.cap. 20 celo leto; prvi r38 = 12.5.) + Škrabec NOV coop. (7; r76–r79+r85–r87) + Dostál dual r30 · babica TOTER 0× PRVIČ! + Vötter 5× (Sotter→Toter→Vötter ista Marjeta?) + Mih 10 (18/18) · 5 dojenčkov † · EMŠO 3 sidra · EXCLUDED 10 · vitals 341 · kumulativ 347/85 ENAINDVajset let`
    : p101Errors.join("; "),
);
// qa-p102 — krstna 04105, polno leto 1907 (P102, issue #18)
// ---------------------------------------------------------------------------
// okvir 1907: skeni 178/179 (glava pod r87, dup) + 180–188; stran == novela
// P102 (dva nova dup para 180/181 + 183/184)
const p102PageOfScan = (s: number) =>
  s === 178 || s === 179 ? 165 : s === 180 || s === 181 ? 166 : s === 182 ? 167 : s === 183 || s === 184 ? 168 : s <= 183 ? s - 15 : s - 16;
const p102Hv = HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year === 1907);
const p102Errors: string[] = [];
if (p102Hv.length !== 15)
  p102Errors.push(`vpisov 1907 (04105, zasidrani) ≠ 15 (${p102Hv.length})`);
const p102Houses = new Set(p102Hv.map((h) => h.houseNo));
if (p102Houses.size !== 14)
  p102Errors.push(`različnih hiš ≠ 14 (${p102Houses.size}: ${[...p102Houses].sort((a, b) => Number(a) - Number(b)).join(",")})`);
// NARE PRELOM: h10 ×2 (r85+r86 dvojčka — 1. ponovitev po 1905 h12 ×2)
const p102RepeatHouses = [...p102Hv.map((h) => h.houseNo)].filter((hn, i, arr) => arr.indexOf(hn) !== i);
if (p102RepeatHouses.join(",") !== "10")
  p102Errors.push(`intra-letna ponovitev 1907 ≠ [10] (NARE PRELOM) — najdeno: ${p102RepeatHouses.join(",") || "brez"}`);
// okvir: stran == sken po P102 noveli (dup pari 178/179 + 180/181 + 183/184)
const p102BadPage = p102Hv.filter(
  (h) => h.status !== "DOCUMENTED" || !h.scan || !h.page
    || h.page !== p102PageOfScan(h.scan)
    || h.scan < 178 || h.scan > 188,
);
if (p102BadPage.length > 0)
  p102Errors.push(`scan/page ne ustreza P102 noveli: ${p102BadPage.map((h) => `${h.houseNo}@${h.scan}`).join(",")}`);
// 0 novih hiš (tretje leto v vzorcu 1905–1907 z 0/1/0)
const p102PriorHouses = new Set(
  HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year !== 1907).map((h) => h.houseNo),
);
const p102New = [...p102Houses].filter((hn) => !p102PriorHouses.has(hn));
if (p102New.length !== 0)
  p102Errors.push(`nove hiše 1907 ≠ [] (${p102New.join(",") || "brez"})`);
// sidra: h7 TOTER oče + h12 POVRAT + h5 NOV KAPLAN + h18/h48/h6 MENJAVA
// + h49 Brodarič + h27 ISTA BOTRA + h13 SELITEV + h83 Željko + h10 ×2 + h62 VRZEL 16
const p102H7 = p102Hv.find((h) => h.houseNo === "7");
if (!p102H7 || !p102H7.whatSi.includes("Jakob Toter") || !p102H7.whatSi.includes("4. VPIS"))
  p102Errors.push("h7 4. VPIS (Jakob Toter kot hišni oče) ne ustreza");
const p102H12 = p102Hv.find((h) => h.houseNo === "12");
if (!p102H12 || !p102H12.whatSi.includes("Janez Dragoš") || !p102H12.whatSi.includes("11. VPIS"))
  p102Errors.push("h12 11. VPIS (Dragoš POVRAT po Štraus/Šimec interludu) ne ustreza");
const p102H5 = p102Hv.find((h) => h.houseNo === "5");
if (!p102H5 || !p102H5.whatSi.includes("Gregor Pecar") || !p102H5.whatSi.includes("NOV KAPLAN"))
  p102Errors.push("h5 NOV KAPLAN Gregor Pecar (prvi podpis 17./18. 9.) ne ustreza");
const p102H18 = p102Hv.find((h) => h.houseNo === "18");
if (!p102H18 || !p102H18.whatSi.includes("Peter Brinec") || !p102H18.whatSi.includes("MENJAVA DRUŽINE"))
  p102Errors.push("h18 MENJAVA DRUŽINE (Šimec → Peter Brinec × Ana Butala) ne ustreza");
const p102H48 = p102Hv.find((h) => h.houseNo === "48");
if (!p102H48 || !p102H48.whatSi.includes("Janez Kure") || !p102H48.whatSi.includes("MENJAVA DRUŽINE"))
  p102Errors.push("h48 MENJAVA DRUŽINE (Pezdirec → Janez Kure bajtar) ne ustreza");
const p102H6 = p102Hv.find((h) => h.houseNo === "6");
if (!p102H6 || !p102H6.whatSi.includes("MENJAVA DRUŽINE") || !p102H6.whatSi.includes("Moravec"))
  p102Errors.push("h6 MENJAVA DRUŽINE (Jakobič → Kapucina? × Moravec) ne ustreza");
const p102H49 = p102Hv.find((h) => h.houseNo === "49");
if (!p102H49 || !p102H49.whatSi.includes("Nikolaj Brodarič") || !p102H49.whatSi.includes("DOJENČEK"))
  p102Errors.push("h49 3. VPIS Brodarič + dojenček † 17.11.1907 ne ustreza");
const p102H27 = p102Hv.find((h) => h.houseNo === "27");
if (!p102H27 || !p102H27.whatSi.includes("Marko Pozdirec") || !p102H27.whatSi.includes("ISTA BOTRA"))
  p102Errors.push("h27 9. VPIS (Pozdirec 2. leto + ISTA BOTRA) ne ustreza");
const p102H13 = p102Hv.find((h) => h.houseNo === "13");
if (!p102H13 || !p102H13.whatSi.includes("Matija Šimec") || !p102H13.whatSi.includes("SELITEV h18→h13"))
  p102Errors.push("h13 6. VPIS (ŠIMEC×KAMBIČ SELITEV h18→h13 + VRZEL 13 LET) ne ustreza");
const p102H83 = p102Hv.find((h) => h.houseNo === "83");
if (!p102H83 || !p102H83.whatSi.includes("Jožef Željko") || !p102H83.whatSi.includes("ISTA družina kot 1903"))
  p102Errors.push("h83 4. VPIS (ISTA Željko družina kot 1903) ne ustreza");
const p102H10 = p102Hv.filter((h) => h.houseNo === "10");
if (p102H10.length !== 2 || !p102H10.every((h) => h.whatSi.includes("Janez Brinec")) || !p102H10.some((h) => h.whatSi.includes("NARE PRELOM")))
  p102Errors.push("h10 ×2 NARE PRELOM (dvojčka Janez Brinec) ne ustreza");
const p102H62 = p102Hv.find((h) => h.houseNo === "62");
if (!p102H62 || !p102H62.whatSi.includes("VRZEL 16 LET") || !p102H62.whatSi.includes("Janez Kure"))
  p102Errors.push("h62 3. VPIS (VRZEL 16 LET; Kure × Požek) ne ustreza");
// kontinuitete (zadnja leta pred 1907; pini po očetu/znakih — prior ALI current)
const p102Pins: Array<[string, number, string]> = [
  ["3", 1902, "Papič"],
  ["5", 1905, "Štrucelj"],
  ["6", 1905, "Jakobič"],
  ["7", 1905, "Jakob Toter"],
  ["10", 1900, "Grabrijan"],
  ["11", 1905, "Žumě"],
  ["12", 1905, "Štraus"],
  ["13", 1894, "Jakljevič"],
  ["18", 1906, "Matija Simec"],
  ["27", 1906, "Pozdirec"],
  ["48", 1905, "Pezdirec"],
  ["49", 1906, "Brodarič"],
  ["62", 1891, "Muern"],
  ["83", 1903, "Željko"],
];
for (const [hn, yr, pin] of p102Pins) {
  const prior = HOUSE_VITALS.find((h) => h.bookSignature === "04105" && h.houseNo === hn && h.year === yr);
  const cur = p102Hv.find((h) => h.houseNo === hn);
  if (!prior || !cur) {
    p102Errors.push(`kontinuiteta hiša ${hn} (${yr} → 1907) manjka`);
    continue;
  }
  if (!prior.whatSi.includes(pin) && !cur.whatSi.includes(pin))
    p102Errors.push(`kontinuiteta hiša ${hn} (${yr}, pin ${pin}) ne ustreza`);
}
// vitals skupaj 449 (P106: 429 + 20; krstna 1911; r43 neberljiva brez bloka)
if (HOUSE_VITALS.length !== 685)
  p102Errors.push(`HOUSE_VITALS ≠ 374 (${HOUSE_VITALS.length})`);
// babica: 15/15 blokov; Mih 0× (NOVELA) + Vötter 0× + Šotter 7× + Toter 1×
if (p102Hv.filter((h) => h.whatSi.includes("babica")).length !== 15)
  p102Errors.push(`babica ni v vseh 15 whatSi (${p102Hv.filter((h) => h.whatSi.includes("babica")).length})`);
if (p102Hv.some((h) => h.whatSi.includes("babica Marija Mih")))
  p102Errors.push("babica Marija Mih 0× pričakovano (NOVELA — prvič od 1902?) — najdena");
if (p102Hv.some((h) => h.whatSi.includes("Vötter")))
  p102Errors.push("babica Vötter 0× pričakovano (1907 spelling = Šotter) — najdena");
const p102Shotter = p102Hv.filter((h) => h.whatSi.includes("babica Marjeta Šotter")).length;
if (p102Shotter !== 7)
  p102Errors.push(`babica Marjeta Šotter ≠ 7× (${p102Shotter})`);
const p102Toter = p102Hv.filter((h) => h.whatSi.includes("babica Marjeta Toter")).length;
if (p102Toter !== 1)
  p102Errors.push(`babica Marjeta Toter ≠ 1× (${p102Toter} — r85 zapis, r86 Šotter ISTA)`);
// duhovniki (bloki): Pecar (kaplan) 10 + Ravq 5 — NOVELA (r4 Kmetij? brez bloka)
if (p102Hv.filter((h) => h.whatSi.includes("Pecar")).length !== 10)
  p102Errors.push(`podpis Pecar (kaplan) ≠ 10× (${p102Hv.filter((h) => h.whatSi.includes("Pecar")).length})`);
if (p102Hv.filter((h) => h.whatSi.includes("Jos. Ravq")).length !== 5)
  p102Errors.push(`podpis Jos. Ravq ≠ 5× (${p102Hv.filter((h) => h.whatSi.includes("Jos. Ravq")).length})`);
// EMŠO sidra v blokih: h7 + h12 + h5 + h48 + h27 (r4 brez bloka — 6. skupaj z dokazom)
const p102Emso = p102Hv.filter((h) => h.whatSi.includes("SKLADNO — sidro"));
if (p102Emso.length !== 5)
  p102Errors.push(`EMŠO sidrov v blokih ≠ 5 (${p102Emso.length})`);
for (const emso of ["2708907505219", "2708907500520", "1709907505092", "0910907500078", "0511907305286"]) {
  if (!p102Hv.some((h) => h.whatSi.includes(emso)))
    p102Errors.push(`EMŠO sidro ${emso} manjka`);
}
push(
  "qa-p102-parish-baptism-1907",
  "P102: ŽUPNIJA PODZEMELJ — KRSTNA KNJIGA 04105, POLNO LETO 1907 (issue #18; SAMPLE-TRANSCRIPTION-1907; MERI, NE odloča; v7 join nespremenjen): širitev vzorca P79 (1886) → … → P100 (1905) → P101 (1906) na leto 1907 — okvir: glava »1907« POD r87 na str. 165 = skeni 178/179 (dup par že P101; 1907 r1 = Dobravice 27 Ivanka 5./5. Januar, podpis Anton Dostál — P101 lead POTRJEN) – row 90 na str. 172 (sken 188; glava »1908« na str. 173 = sken 189; 1908 r1 = Krasinec 58 August — P103 lead) == tiskane strani 165–172 (90 vrstic); NOVELA P102: DVA nova dup para skenov — 180/181 = str. 166 (rows 9–20) + 183/184 = str. 168 (rows 33–44); stran == sken − 16 (184–189) / − 15 (181–183) / − 14 (179–180); VSI vpisi z Griblji: 16 vpisov / 14 hiš + 1 neberljiva (r4 — strglek + modri pripisi; hiša pričevanje-samo brez vitals bloka) — NARE PRELOM: h10 ×2 (r85+r86 dvojčka Jožef+Anton, oba † december 1907 — 19.12. + 25.12. božič; 1. intra-letna ponovitev po 1905 h12 ×2; 1906 je bil 18/18); 0 NOVIH hiš (vzorec 1905–1907: 0/1/0); PT 12/2 (48+49 v luknji 41–60 — ponovitve; luknja ostaja samo h51); kumulativ 363 vpisov / 85 hiš čez tri knjige in DVAINDVAJSET let (1886–1907; 356 vitals); SIDRA: r4 ŽELJKO×KURE krog (oče Željko? + mati Barbara Kure + boter Jožef Željko + babica Katarina Željko — NE h1 par, mati Barbara; EMŠO 1101907505283 sidro); r11 h11 4. VPIS ISTA familija (Žumič — 1905 »Žume/Žunič«; kraj forenzika »Grišlje« = Griblje genetsko!); r48 h3 3. VPIS ISTA (Papič — Kurrent P/T »Tapič«); r52 h7 4. VPIS ISTA (JAKOB TOTER kot hišni oče — babica-priimek na hišni vlogi!; EMŠO sidro; VPIS popravljen v matični register 13.11.2007!); r53 h12 11. VPIS — Dragoš×Cvitkovič POVRAT po 1901/05 Štraus/Šimec interludu (več-družinska h12; EMŠO sidro; istega dne kot r52); r60 h5 4. VPIS ISTA (Štrucelj×Meh) + NOV KAPLAN Gregor Pecar (prvi podpis 17./18. 9. 1907!; EMŠO sidro); r61 h18 3. VPIS — MENJAVA Šimec → Peter Brinec × Ana Butala (BRINEC signal 1/4); r64 h48 3. VPIS — MENJAVA Pezdirec → Janez Kure bajtar (EMŠO sidro); r67 h6 3. VPIS — MENJAVA Jakobič → Kapucina?×Moravec (branje negotovo); r69 h49 3. VPIS — Brodarič (mati Milek/Miheč MERI) + DOJENČEK † 17.11.1907 (30 dni); r73 h27 9. VPIS — Pozdirec 2. leto + ISTA BOTRA 2. leto (Željko+Hrižan; hiša »8y« = Kurrent »27« — genetska potrditev!; EMŠO sidro); r76 h13 6. VPIS — VRZEL 13 LET + MENJAVA Jakopič → ŠIMEC×KAMBIČ (SELITEV h18→h13 — ista zveza kot h18 1906!); r80 h83 4. VPIS — ISTA Željko družina kot 1903 (luknja 1890–1902; mati Peruš?/Gorše? MERI); r85+r86 h10 ×2 — BRINEC POVRAT (1897 familija, druga žena Ana Klepec) + dvojčka †; r88 h62 3. VPIS — VRZEL 16 LET (2. najdaljša vzorca za h39 18; Kure × Požek; BRINEC signal 4/4 — boter = oče r85/86!); DUHOVNIKI NOVELA (na Gribljih 16/16): NOV KAPLAN Gregor Pecar 10× (prvi podpis r60 = 17./18. 9. 1907; PARALELNI podpisi Rauq+Pecar Sep–Nov — r73 Pecar Nov 5 / r76 Rauq Nov 12!) + Jos. Ravq 5× + P. Janez Kmetij? 1× (r4 januar — trovrstični podpis, branje negotovo); BABICA NOVELA: MIH 0× — PRVIČ OD 1902? (dominantna 1904–06: 19/16/10)!; Vötter 0× → Šotter 7× + Toter 1× (ISTA Marjeta — DVE ČRKOVANJI v istem dvojčkem paru r85/r86!); na Gribljih 16/16: Šotter 7 + Toter 1 + Meh 3 + Željko 1 + Papič? 1 + Muc 1 + Klepec 1 + Urh 1; celo leto vsi imenovani; EMŠO kampanja: 6 sidr na Gribljih (r4/r52/r53/r60/r64/r73) — VSI SKLADNI z rojstnimi datumi; ANOMALIJE: 4 para dvojčkov (r2/r3 Gradac 9 + r33/r34 Gradac 55 + r35/r36 Dobravice 11 + r54/r55 Krasinec 18 — non-Griblje), 3 dojenčki † na Gribljih (r69/r86/r85), r61 pripisno neskladje (svinčnik † 31.5.1941 + modri poroka 21.5.1950?), r30 dvoje imen (Jožefa/Ana), dva Janez Kure očetja (h48+h62) [MERI], 6 menjav družin (h3/h6/h10/h13/h18/h48), matični vpisi 20. stol. (r52 2007 + r71/r72 2001), duhovniški pripis na krstni vrstici (r9 nalepka: »otok umrl 17.8.1985 … duhovnik«), kraj forenzika r5 Zemelj + r58 Grišiče (dva revidirana prva branja), dvojni zapis babice r85 Toter/r86 Šotter; EXCLUDED: 6 (r5 Zemelj, r9 nalepka, r43 mrtvorojena, r44 strglek, r58 Grišiče, r90 Otok — zadnja vrstica); skripta scripts/p102_parish_baptism_1907.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1907",
  "P102: PARISH OF PODZEMELJ — BAPTISM REGISTER 04105, THE FULL YEAR 1907 (issue #18; SAMPLE-TRANSCRIPTION-1907; MEASURES, does not decide; the v7 join unchanged): extending the P79 (1886) → … → P100 (1905) → P101 (1906) sample to 1907 — the frame: the heading '1907' BELOW r87 on p. 165 = scans 178/179 (a dup pair already P101; the 1907 r1 = Dobravice 27 Ivanka Jan 5/5, signature Anton Dostál — the P101 lead CONFIRMED) – row 90 on p. 172 (scan 188; the heading '1908' on p. 173 = scan 189; the 1908 r1 = Krasinec 58 August — the P103 lead) == printed pages 165–172 (90 rows); THE P102 NOVEL: TWO new duplicated scan pairs — 180/181 = p. 166 (rows 9–20) + 183/184 = p. 168 (rows 33–44); page == scan − 16 (184–189) / − 15 (181–183) / − 14 (179–180); ALL Griblje entries: 16 entries / 14 houses + 1 illegible (r4 — a sticker + blue notes; the house evidence-only without a vitals block) — THE NARE BREAK: h10 ×2 (r85+r86 twins Jožef+Anton, both † December 1907 — Dec 19 + Dec 25 Christmas; the 1st intra-year house repeat since 1905 h12 ×2; 1906 was 18/18); 0 NEW houses (the sample 1905–1907: 0/1/0); the PT 12/2 (48+49 in the gap 41–60 — repeats; only h51 remains); the cumulative 363 entries / 85 houses across three books and TWENTY-TWO years (1886–1907; 356 vitals); ANCHORS: r4 the ŽELJKO×KURE circle (father Željko? + mother Barbara Kure + godfather Jožef Željko + midwife Katarina Željko — NOT the h1 couple, mother Barbara; personal ID 1101907505283 an anchor); r11 h11 the 4th ENTRY the SAME family (Žumič — 1905 »Žume/Žunič«; the village forensics »Grišlje« = Griblje genetically!); r48 h3 the 3rd ENTRY the SAME (Papič — the Kurrent P/T »Tapič«); r52 h7 the 4th ENTRY the SAME (JAKOB TOTER as the house-father — the midwife surname on the house role!; personal ID an anchor; the ENTRY CORRECTED into the civil register Nov 13, 2007!); r53 h12 the 11th ENTRY — Dragoš×Cvitkovič BACK after the 1901/05 Štraus/Šimec interlude (the multi-family h12; personal ID an anchor; the same day as r52); r60 h5 the 4th ENTRY the SAME (Štrucelj×Meh) + A NEW CURATE Gregor Pecar (the first signature Sep 17/18, 1907!; personal ID an anchor); r61 h18 the 3rd ENTRY — A CHANGE Šimec → Peter Brinec × Ana Butala (the BRINEC signal 1/4); r64 h48 the 3rd ENTRY — A CHANGE Pezdirec → Janez Kure a cottager (personal ID an anchor); r67 h6 the 3rd ENTRY — A CHANGE Jakobič → Kapucina?×Moravec (an uncertain reading); r69 h49 the 3rd ENTRY — Brodarič (the mother Milek/Miheč MERI) + an INFANT † Nov 17, 1907 (30 days); r73 h27 the 9th ENTRY — Pozdirec for a 2nd year + THE SAME GODPARENTS for a 2nd year (Željko+Hrižan; the house »8y« = the Kurrent »27« — a genetic confirmation!; personal ID an anchor); r76 h13 the 6th ENTRY — a 13-YEAR GAP + A CHANGE Jakopič → ŠIMEC×KAMBIČ (the HOUSE MOVE h18→h13 — the same couple as h18 1906!); r80 h83 the 4th ENTRY — the SAME Željko family as 1903 (the 1890–1902 gap; the mother Peruš?/Gorše? MERI); r85+r86 h10 ×2 — the BRINEC RETURN (the 1897 family, another wife Ana Klepec) + twins †; r88 h62 the 3rd ENTRY — a 16-YEAR GAP (the 2nd longest in the sample after h39's 18; Kure × Požek; the BRINEC signal 4/4 — the godfather = the r85/86 father!); PRIESTS NOVEL (in Griblje 16/16): A NEW CURATE Gregor Pecar 10× (the first signature r60 = Sep 17/18, 1907; PARALLEL signatures Rauq+Pecar Sep–Nov — r73 Pecar Nov 5 / r76 Rauq Nov 12!) + Jos. Ravq 5× + P. Janez Kmetij? 1× (r4 January — a three-line signature, an uncertain reading); MIDWIFE NOVEL: MIH 0× — FOR THE FIRST TIME SINCE 1902? (the dominant 1904–06: 19/16/10)!; Vötter 0× → Šotter 7× + Toter 1× (the SAME Marjeta — TWO SPELLINGS within the same twin pair r85/r86!); in Griblje 16/16: Šotter 7 + Toter 1 + Meh 3 + Željko 1 + Papič? 1 + Muc 1 + Klepec 1 + Urh 1; the whole year all named; the personal-ID campaign: 6 anchors in Griblje (r4/r52/r53/r60/r64/r73) — ALL CONSISTENT with the birth dates; ANOMALIES: 4 twin pairs (r2/r3 Gradac 9 + r33/r34 Gradac 55 + r35/r36 Dobravice 11 + r54/r55 Krasinec 18 — non-Griblje), 3 infant deaths in Griblje (r69/r86/r85), r61 a note conflict (the pencil † May 31, 1941 + the blue marriage May 21, 1950?), r30 two names (Jožefa/Ana), two Janez Kure fathers (h48+h62) [MERI], 6 family changes (h3/h6/h10/h13/h18/h48), civil-register entries of the 20th c. (r52 2007 + r71/r72 2001), a priest's note on a baptism row (r9 a sticker: »Otok died Aug 17, 1985 … a priest«), the village forensics r5 Zemelj + r58 Grišiče (two revised first readings), a double midwife spelling r85 Toter/r86 Šotter; EXCLUDED: 6 (r5 Zemelj, r9 a sticker, r43 stillborn, r44 a sticker, r58 Grišiče, r90 Otok — the last row); the script scripts/p102_parish_baptism_1907.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1907",
  p102Errors.length === 0,
  p102Errors.length === 0
    ? `16 vpisov / 14 hiš + 1 neberljiva (r4) — NARE PRELOM h10 ×2 (dvojčka † december) · okvir 1907 skeni 178/179 (glava pod r87, P101 lead POTRJEN) – 188 row 90 (glava 1908 = P103 lead; 90 vrstic) · NOVELA: DVA nova dup para (180/181 + 183/184) · stran == sken − 16/− 15/− 14 · 0 NOVIH hiš (0/1/0) · PT 12/2 · h7 TOTER hišni oče · h12 POVRAT Dragoš · h5 NOV KAPLAN Pecar (prvi 17./18. 9.) + PARALELNI Rauq · h18/h48/h6/h13 MENJAVE + SELITEV h18→h13 (Šimec×Kambič) · h10 BRINEC POVRAT + dvojčka † · h62 VRZEL 16 LET · h83 ISTA Željko · h27 ISTA BOTRA 2. leto · babica MIH 0× PRVIČ OD 1902? + Šotter 7/Toter 1 (ISTA Marjeta!) · 3 dojenčki † · EMŠO 6 sidr VSI SKLADNI · EXCLUDED 6 · vitals 374 · kumulativ 363/85 DVAINDVAJSET let`
    : p102Errors.join("; "),
);
// qa-p103 — krstna 04105, polno leto 1908 (P103, issue #18)
// ---------------------------------------------------------------------------
// okvir 1908: skeni 189/190 (glava, dup) + 191–199; stran == novela P103
// (trije novi dup pari 189/190 + 193/194 + 197/198; glava 1909 INLINE r91)
const p103PageOfScan = (s: number) =>
  s === 189 || s === 190 ? 173 : s === 191 ? 174 : s === 192 ? 175 : s === 193 || s === 194 ? 176 : s === 195 ? 177 : s === 196 ? 178 : s === 197 || s === 198 ? 179 : s === 199 ? 180 : s - 19;
const p103Hv = HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year === 1908);
const p103Errors: string[] = [];
if (p103Hv.length !== 18)
  p103Errors.push(`vpisov 1908 (04105, zasidrani) ≠ 18 (${p103Hv.length})`);
const p103Houses = new Set(p103Hv.map((h) => h.houseNo));
if (p103Houses.size !== 18)
  p103Errors.push(`različnih hiš ≠ 18 (${p103Houses.size}: ${[...p103Houses].sort((a, b) => Number(a) - Number(b)).join(",")})`);
// NARE 18/18 — po 1907 prelomu (h10 ×2) spet brez ponovitev
const p103RepeatHouses = [...p103Hv.map((h) => h.houseNo)].filter((hn, i, arr) => arr.indexOf(hn) !== i);
if (p103RepeatHouses.length !== 0)
  p103Errors.push(`intra-letna ponovitev 1908 ≠ [] (NARE 18/18) — najdeno: ${p103RepeatHouses.join(",")}`);
// okvir: stran == sken po P103 noveli (dup pari 189/190 + 193/194 + 197/198)
const p103BadPage = p103Hv.filter(
  (h) => h.status !== "DOCUMENTED" || !h.scan || !h.page
    || h.page !== p103PageOfScan(h.scan)
    || h.scan < 189 || h.scan > 199,
);
if (p103BadPage.length > 0)
  p103Errors.push(`scan/page ne ustreza P103 noveli: ${p103BadPage.map((h) => `${h.houseNo}@${h.scan}`).join(",")}`);
// 0 novih hiš (vzorec 1905–1908: 0/1/0/0)
const p103PriorHouses = new Set(
  HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year !== 1908).map((h) => h.houseNo),
);
const p103New = [...p103Houses].filter((hn) => !p103PriorHouses.has(hn));
if (p103New.length !== 0)
  p103Errors.push(`nove hiše 1908 ≠ [] (${p103New.join(",") || "brez"})`);
// sidra: h90 TRETJA UČITELJSKA + h30 SEGINA POVRAT + h16 NOVAK POVRAT + h52 ISTA 10 LET
// + h91 MUC ISTA + h49 Brodarič + h36 KRIŽAN POVRAT + h24 13. VPIS + h85 NUJNI KRST + h10 BRINEC
const p103H90 = p103Hv.find((h) => h.houseNo === "90");
if (!p103H90 || !p103H90.whatSi.includes("Kalan") || !p103H90.whatSi.includes("učitelj") || !p103H90.whatSi.includes("TRETJA UČITELJSKA"))
  p103Errors.push("h90 5. VPIS (TRETJA učiteljska družina — Kalan uč.) ne ustreza");
const p103H30 = p103Hv.find((h) => h.houseNo === "30");
if (!p103H30 || !p103H30.whatSi.includes("Nikolaj Segina") || !p103H30.whatSi.includes("SEGINA POVRAT"))
  p103Errors.push("h30 11. VPIS (SEGINA POVRAT po 1906 Brinec interludu) ne ustreza");
const p103H16 = p103Hv.find((h) => h.houseNo === "16");
if (!p103H16 || !p103H16.whatSi.includes("Novak") || !p103H16.whatSi.includes("NOVAK bajtar POVRAT"))
  p103Errors.push("h16 8. VPIS (NOVAK bajtar POVRAT cf. 1900) ne ustreza");
const p103H52 = p103Hv.find((h) => h.houseNo === "52");
if (!p103H52 || !p103H52.whatSi.includes("Matija Pezdirec") || !p103H52.whatSi.includes("ISTA ZVEZA čez 10 LET"))
  p103Errors.push("h52 3. VPIS (ISTA ZVEZA čez 10 LET — Podrinc/Pendirec ≈ Pezdirec) ne ustreza");
const p103H91 = p103Hv.find((h) => h.houseNo === "91");
if (!p103H91 || !p103H91.whatSi.includes("Janez Muc") || !p103H91.whatSi.includes("Ana Kure") || !p103H91.whatSi.includes("5. VPIS"))
  p103Errors.push("h91 5. VPIS ISTA (Muc bajtar × Ana Kure) ne ustreza");
const p103H49 = p103Hv.find((h) => h.houseNo === "49");
if (!p103H49 || !p103H49.whatSi.includes("Nikolaj Brodarič") || !p103H49.whatSi.includes("4. VPIS"))
  p103Errors.push("h49 4. VPIS ISTA (Brodarič kontinuiteta) ne ustreza");
const p103H36 = p103Hv.find((h) => h.houseNo === "36");
if (!p103H36 || !p103H36.whatSi.includes("Janez Križan") || !p103H36.whatSi.includes("KRIŽAN POVRAT"))
  p103Errors.push("h36 11. VPIS (KRIŽAN POVRAT — ISTA zveza) ne ustreza");
const p103H24 = p103Hv.find((h) => h.houseNo === "24");
if (!p103H24 || !p103H24.whatSi.includes("13. VPIS") || !p103H24.whatSi.includes("najbolj vpisovana"))
  p103Errors.push("h24 13. VPIS (najbolj vpisovana hiša še naprej) ne ustreza");
const p103H85 = p103Hv.find((h) => h.houseNo === "85");
if (!p103H85 || !p103H85.whatSi.includes("NUJNI KRST") || !p103H85.whatSi.includes("VRZEL 20 LET"))
  p103Errors.push("h85 2. VPIS (NUJNI KRST + VRZEL 20 LET) ne ustreza");
const p103H10 = p103Hv.find((h) => h.houseNo === "10");
if (!p103H10 || !p103H10.whatSi.includes("Janez Brinec") || !p103H10.whatSi.includes("4. VPIS"))
  p103Errors.push("h10 4. VPIS (BRINEC ISTA; mati menjava Ana Klepec? → Ana Kure) ne ustreza");
// kontinuitete (zadnja leta pred 1908; pini po očetu/znakih — prior ALI current)
const p103Pins: Array<[string, number, string]> = [
  ["10", 1907, "Janez Brinec"],
  ["11", 1907, "Žumič"],
  ["14", 1902, "Janez Brinec"],
  ["16", 1906, "Jakofčič"],
  ["23", 1905, "Matija Brinec"],
  ["24", 1906, "Janez Brinec"],
  ["30", 1906, "Matija Brinec"],
  ["36", 1904, "Rudolf Miše"],
  ["44", 1906, "Jožef Štrucelj"],
  ["46", 1899, "Anton Brodarič"],
  ["49", 1907, "Nikolaj Brodarič"],
  ["52", 1898, "Matija Podrinc"],
  ["56", 1888, "Šimec"],
  ["60", 1906, "Nikolaj Željko"],
  ["65", 1904, "Matija Milek"],
  ["85", 1888, "Marko Križan"],
  ["90", 1900, "Vetročnik"],
  ["91", 1904, "Janez Muc"],
];
for (const [hn, yr, pin] of p103Pins) {
  const prior = HOUSE_VITALS.find((h) => h.bookSignature === "04105" && h.houseNo === hn && h.year === yr);
  const cur = p103Hv.find((h) => h.houseNo === hn);
  if (!prior || !cur) {
    p103Errors.push(`kontinuiteta hiša ${hn} (${yr} → 1908) manjka`);
    continue;
  }
  if (!prior.whatSi.includes(pin) && !cur.whatSi.includes(pin))
    p103Errors.push(`kontinuiteta hiša ${hn} (${yr}, pin ${pin}) ne ustreza`);
}
// vitals skupaj 449 (P106: 429 + 20; krstna 1911; r43 neberljiva brez bloka)
if (HOUSE_VITALS.length !== 685)
  p103Errors.push(`HOUSE_VITALS ≠ 374 (${HOUSE_VITALS.length})`);
// babica: 18/18 blokov; Vötter 1× (VRNITEV po 1907 0×!) + Muc 6 + Adlešič 8 + Meh 2
if (p103Hv.filter((h) => h.whatSi.includes("babica")).length !== 18)
  p103Errors.push(`babica ni v vseh 18 whatSi (${p103Hv.filter((h) => h.whatSi.includes("babica")).length})`);
const p103Votter = p103Hv.filter((h) => h.whatSi.includes("Vötter")).length;
if (p103Votter !== 1)
  p103Errors.push(`babica Vötter ≠ 1× (${p103Votter} — VRNITEV po 1907 0×)`);
const p103Muc = p103Hv.filter((h) => h.whatSi.includes("babica Marija Muc")).length;
if (p103Muc !== 6)
  p103Errors.push(`babica Marija Muc ≠ 6× (${p103Muc})`);
const p103Adlesic = p103Hv.filter((h) => /babica [^;]*Adlešič/.test(h.whatSi)).length;
if (p103Adlesic !== 8)
  p103Errors.push(`babica Adlešič ≠ 8× (${p103Adlesic} — Barbara 7 + Marija 1)`);
// duhovniki (bloki): Cerar 12 + Ravq 3 (r84 brez bloka — 4. skupaj z dokazom) + Dami 1 (NOV)
if (p103Hv.filter((h) => h.whatSi.includes("podpis Gregor Cerar")).length !== 12)
  p103Errors.push(`podpis Gregor Cerar ≠ 12× (${p103Hv.filter((h) => h.whatSi.includes("podpis Gregor Cerar")).length})`);
if (p103Hv.filter((h) => h.whatSi.includes("podpis Jos. Ravq")).length !== 3)
  p103Errors.push(`podpis Jos. Ravq ≠ 3× (${p103Hv.filter((h) => h.whatSi.includes("podpis Jos. Ravq")).length} — r84 brez bloka)`);
if (p103Hv.filter((h) => h.whatSi.includes("Jos. Dami")).length !== 2)
  p103Errors.push(`podpis Jos. Dami (NOV DUHOVNIK) ≠ 2× (${p103Hv.filter((h) => h.whatSi.includes("Jos. Dami")).length})`);
// EMŠO sidra v blokih: 6 (r31/r65/r66/r68/r88/r90)
const p103Emso = p103Hv.filter((h) => h.whatSi.includes("SKLADNO — sidro"));
if (p103Emso.length !== 6)
  p103Errors.push(`EMŠO sidrov v blokih ≠ 6 (${p103Emso.length})`);
for (const emso of ["2204908500557", "0310908500848", "0410908500444", "0810908505763", "2612908500224", "2812908500042"]) {
  if (!p103Hv.some((h) => h.whatSi.includes(emso)))
    p103Errors.push(`EMŠO sidro ${emso} manjka`);
}
push(
  "qa-p103-parish-baptism-1908",
  "P103: ŽUPNIJA PODZEMELJ — KRSTNA KNJIGA 04105, POLNO LETO 1908 (issue #18; SAMPLE-TRANSCRIPTION-1908; MERI, NE odloča; v7 join nespremenjen): širitev vzorca P79 (1886) → … → P100 (1905) → P101 (1906) → P102 (1907) na leto 1908 — okvir: glava »Leto 18 1908« na str. 173 = skeni 189/190 (dup par; 1908 r1 = Krasinec 38(?) August 1./1. Januar — P102 lead POTRJEN; hiša forenzika 38 vs lead 58) – row 90 na str. 180 (sken 199; glava »1909« INLINE na r91 = isti sken; 1909 r1 = Dobraviče 26 Anton 7./7. Januar — P104 lead) == tiskane strani 173–180 (90 vrstic); NOVELA P103: TRIJE novi dup pari skenov — 189/190 = str. 173 + 193/194 = str. 176 + 197/198 = str. 179 (vsi trije z berljivimi dopolnitvami: r6 na 190, r47 na 194, r79 na 198!); stran == sken − 16 (189) / − 17 (190–193) / − 18 (194–197) / − 19 (198–199); VSI vpisi z Griblji: 19 vpisov / 18 hiš + 1 neberljiva (r84 — POSTRGAN rob str. 179, papir fizično manjka na obojih dup skenih; hiša pričevanje-samo brez vitals bloka) — NARE 18/18 (po 1907 prelomu h10 ×2 spet brez intra-letne ponovitve; 1908: vsaka hiša 1×); 0 NOVIH hiš (vzorec 1905–1908: 0/1/0/0 — VSE 18 hiš že zasidrane); PT 12/6 (44+46+49+52+56+60 v luknji 41–60 — ponovitve; luknja ostaja samo h51); kumulativ 382 vpisov / 85 hiš čez tri knjige in DVAINDVAJSET+ENO let (1886–1908; 374 vitals); SIDRA: r16 h14 4. VPIS ISTA familija (BRINEC kontinuiteta 1900/02 → 1908; botra = babica ISTA Barbara Adlešič ×2!); r22 h60 8. VPIS ISTA ZVEZA (Željko × Brodarič — 5. OTROK; PRESTOPNI 29. 2. 1908!; botrinja Marija Klepec 4.×); r23 h24 13. VPIS — ŠE VEDNO najbolj vpisovana hiša registra (Brincova hiša POVRAT; NOV DUHOVNIK Jos. Dami — prvi podpis na Gribljih!); r27 h16 8. VPIS (NOVAK bajtar POVRAT cf. 1900; več-družinska hiša 7 menjav; CROSS-ROW boter Janez Muc kovač = r31 h91 oče!); r31 h91 5. VPIS ISTA (Muc bajtar × Ana Kure; EMŠO 2204908500557; pripisno neskladje poroke modri/zeleni); r41 h85 2. VPIS — NUJNI KRST (»v sili krščen?«; botra + podpis PRAZNA — črti; babica Marija Muc krstiteljica; VRZEL 20 LET; dojenček † 29.5.1908 5 dni); r46 h52 3. VPIS — ISTA ZVEZA čez 10 LET (1898 Podrinc/Pendirec × Jakobič = 1908 Pezdirec × Jakobčič — Kurrent variante ISTEGA para); r47 h44 5. VPIS (Štrucelj ISTA oče cf. 1906; botrinja Doroteja = r69 mati CROSS-ROW; forenzika na dup skenu 194 — na 193 pod trakom); r55 h23 7. VPIS — ISTA ZVEZA čez 8 LET (Brinec? × Marija Dehlič — MATI ISTA kot 1900; očetova celica RAZTRGANA — branje po genetski opori; DEHLIČ ×3 v vrstici); r57 h65 9. VPIS — MILEK 1887–1908 (boter Peter Pezdirec ISTA kot 1887 — 21 LET kasneje!; babica Barbara Adlešič = botrinja 1887); r65 h46 6. VPIS (ISTA OČE Anton Brodarič cf. 1893–99 — VRZEL 9 LET; EMŠO 0310908500848; boter Nikolaj Željko); r66 h30 11. VPIS — SEGINA POVRAT (1902/03 → 1906 Brinec interlud → 1908 Segina; mati Katarina Brinec ISTA kot 1903; EMŠO 0410908500444); r68 h49 4. VPIS ISTA (Brodarič kontinuiteta; EMŠO 0810908505763; boter Jurij Pezdirec 1./3); r69 h56 3. VPIS — VRZEL 20 LET (NOVA družina Jerčinovič? × Štrucelj; mati = r47 botrinja; boter Jurij Pezdirec 2./3 — 2. dan zapored!); r70 h36 11. VPIS — KRIŽAN POVRAT (ISTA zveza Janez Križan × Katarina Štrucelj/Straucelj cf. 1894–1902; boter Matija Štraus — ŠTRAUS kampanja); r79 h90 5. VPIS — TRETJA UČITELJSKA DRUŽINA (Kopitar uč. 1890/92 → Vetročnik uč. 1898/1900 → Kalan uč. 1908!; boter Jurij Pezdirec 3./3); r88 h11 5. VPIS ISTA familija (Žumič; babica Marjeta Vötter VRNITEV po 1907 0×; EMŠO 2612908500224); r90 h10 4. VPIS — BRINEC ISTA (mati menjava Ana Klepec? → Ana Kure; botra Janez Muc bajtar + Marija Kure = ISTI boter par kot 1907 r85 [kovač+Katarina Kure]; EMŠO 2812908500042; ZADNJA vrstica 1908); DUHOVNIKI NOVELA (na Gribljih 18 berljivih + r84): Gregor Cerar 12 + NOV DUHOVNIK Jos. Dami 1 (r23; 2. podpis v letu = r18 Otok; paralelni Cerar/Ravq/Dami!) + Jos. Ravq 4 (r65/r68/r79/r84) + PRAZEN 1 (r41 NUJNI KRST); na 1909 r1 podpis »P. Gregor Cerar coop.« (dual/coop žig — NE na Gribljih); BABICA NOVELA: na Gribljih 18/18 imenovanih: Marija Muc 6 + Barbara Adlešič 7 (+ Marija Adlešič 1 = 8) + Marija Meh 2 + Marjeta Vötter 1 (VRNITEV: Sotter 1889 → Toter 1901–05 → Vötter 1906/1908 — ISTA Marjeta? MERI) + Ana Mavrenič 1 (r79) + Mehrič? [~] 1 (r84 postrgano); MIH 0× (2. leto zapored!); EMŠO kampanja: 6 sidr na Gribljih (r31/r65/r66/r68/r88/r90) — VSI SKLADNI z rojstnimi datumi (+1 dan na krsti); ANOMALIJE: r41 NUJNI KRST (edini v vzorcu P79–P103?); r84 POSTRGAN rob (papir manjka); r89 pod trakom (B-stran: Matija Muc × Marija Gregorič); r55 raztrgana očetova celica; r31/r23/r79 pokrite/pripisne celice; CROSS-ROW ×3 (r27+r90 boter Janez Muc = r31 h91 oče; r47 botrinja = r69 mati; r68+r69 isti boter 2. dneva); žig »FRIEDMANN« str. 179 (moderni); prestopni 29. 2. 1908 (r22!); kraj forenzika r28 Prilozje? + r42 Škrilje + r59 Štriglje? + r74 Prilozje 25 (štiri revidirana prva branja — cf. P101/P102 Prilozje/Grm); EXCLUDED: 7 (r1 Krasinec 38 lead-forenzika, r28 Prilozje?, r42 Škrilje, r44 mrtvorojen, r59 Štriglje?, r74 Prilozje 25, r89 trak); skripta scripts/p103_parish_baptism_1908.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1908",
  "P103: PARISH OF PODZEMELJ — BAPTISM REGISTER 04105, THE FULL YEAR 1908 (issue #18; SAMPLE-TRANSCRIPTION-1908; MEASURES, does not decide; the v7 join unchanged): extending the P79 (1886) → … → P102 (1907) sample to 1908 — the frame: the heading »Leto 18 1908« on p. 173 = scans 189/190 (a dup pair; the 1908 r1 = Krasinec 38(?) August Jan 1/1 — the P102 lead CONFIRMED; the house forensics 38 vs the lead 58) – row 90 on p. 180 (scan 199; the heading »1909« INLINE on r91 = the same scan; the 1909 r1 = Dobraviče 26 Anton Jan 7/7 — the P104 lead) == printed pages 173–180 (90 rows); THE P103 NOVEL: THREE new duplicated scan pairs — 189/190 = p. 173 + 193/194 = p. 176 + 197/198 = p. 179 (all three with legible completions: r6 on 190, r47 on 194, r79 on 198!); page == scan − 16 (189) / − 17 (190–193) / − 18 (194–197) / − 19 (198–199); ALL Griblje entries: 19 entries / 18 houses + 1 illegible (r84 — a SCRAPED-OFF bottom edge of p. 179, the paper physically missing on both dup scans; the house evidence-only without a vitals block) — NARE 18/18 (after the 1907 break h10 ×2 again without an intra-year repeat); 0 NEW houses (the sample 1905–1908: 0/1/0/0 — all 18 houses already anchored); the PT 12/6 (44+46+49+52+56+60 in the gap 41–60 — repeats; only h51 remains); the cumulative 382 entries / 85 houses across three books and TWENTY-THREE years (1886–1908; 374 vitals); ANCHORS: r16 h14 the 4th ENTRY the SAME family (the BRINEC continuity; the godmother = midwife the SAME Barbara Adlešič ×2!); r22 h60 the 8th ENTRY the SAME couple (Željko × Brodarič — the 5th CHILD; the LEAP Feb 29, 1908!; the godmother Marija Klepec the 4th time); r23 h24 the 13th ENTRY — STILL the most-entered house (the Brinec house RETURNS; A NEW PRIEST Jos. Dami — the first Griblje signature!); r27 h16 the 8th ENTRY (the NOVAK cottager RETURNS cf. 1900; a 7-change multi-family house; a CROSS-ROW godfather Janez Muc the smith = the r31 h91 father!); r31 h91 the 5th ENTRY the SAME (Muc cottager × Ana Kure; personal ID 2204908500557; a marriage note conflict); r41 h85 the 2nd ENTRY — an EMERGENCY BAPTISM (»baptized in necessity?«; the godparents + signature EMPTY — dashes; the midwife Marija Muc as the baptizer; a 20-YEAR GAP; the infant † May 29, 1908, 5 days); r46 h52 the 3rd ENTRY — the SAME couple across 10 YEARS (1898 Podrinc/Pendirec × Jakobič = 1908 Pezdirec × Jakobčič — Kurrent variants of the SAME couple); r47 h44 the 5th ENTRY (Štrucelj the same father cf. 1906; the godmother Doroteja = the r69 mother, a CROSS-ROW; the forensics on the dup scan 194); r55 h23 the 7th ENTRY — the SAME couple across 8 YEARS (Brinec? × Marija Dehlič — the MOTHER the SAME as 1900; the father's cell TORN; DEHLIČ ×3 in the row); r57 h65 the 9th ENTRY — MILEK 1887–1908 (the godfather Peter Pezdirec the SAME as 1887 — 21 YEARS later!; the midwife Barbara Adlešič = the 1887 godmother); r65 h46 the 6th ENTRY (the SAME father Anton Brodarič cf. 1893–99 — a 9-YEAR GAP; personal ID 0310908500848; the godfather Nikolaj Željko); r66 h30 the 11th ENTRY — the SEGINA RETURN (1902/03 → the 1906 Brinec interlude → 1908 Segina; the mother Katarina Brinec the SAME as 1903; personal ID 0410908500444); r68 h49 the 4th ENTRY the SAME (the Brodarič continuity; personal ID 0810908505763; the godfather Jurij Pezdirec 1st of 3); r69 h56 the 3rd ENTRY — a 20-YEAR GAP (a NEW family Jerčinovič? × Štrucelj; the mother = the r47 godmother; the godfather Jurij Pezdirec 2nd of 3 — the 2nd consecutive day!); r70 h36 the 11th ENTRY — the KRIŽAN RETURN (the same couple Janez Križan × Katarina Štrucelj/Straucelj cf. 1894–1902; the godfather Matija Štraus — the ŠTRAUS campaign); r79 h90 the 5th ENTRY — the THIRD TEACHER FAMILY (Kopitar 1890/92 → Vetročnik 1898/1900 → Kalan 1908!; the godfather Jurij Pezdirec 3rd of 3); r88 h11 the 5th ENTRY the SAME family (Žumič; the midwife Marjeta Vötter a RETURN after the 1907 zero; personal ID 2612908500224); r90 h10 the 4th ENTRY — the BRINEC SAME (the mother change Ana Klepec? → Ana Kure; the godparents Janez Muc the cottager + Marija Kure = the SAME godparent couple as the 1907 r85; personal ID 2812908500042; the LAST row of 1908); PRIESTS NOVEL (in Griblje 18 legible + r84): Gregor Cerar 12 + A NEW PRIEST Jos. Dami 1 (r23; his 2nd signature of the year = r18 Otok; parallel Cerar/Ravq/Dami!) + Jos. Ravq 4 (r65/r68/r79/r84) + EMPTY 1 (r41 the EMERGENCY BAPTISM); on the 1909 r1 the signature »P. Gregor Cerar coop.« (a dual/coop mark — NOT on Griblje rows); MIDWIFE NOVEL: in Griblje 18/18 named: Marija Muc 6 + Barbara Adlešič 7 (+ Marija Adlešič 1 = 8) + Marija Meh 2 + Marjeta Vötter 1 (a RETURN: Sotter 1889 → Toter 1901–05 → Vötter 1906/1908 — the SAME Marjeta? MERI) + Ana Mavrenič 1 (r79) + Mehrič? [~] 1 (r84 scraped); MIH 0× (the 2nd consecutive year!); the personal-ID campaign: 6 anchors in Griblje — ALL CONSISTENT with the birth dates (+1 day to the baptism); ANOMALIES: r41 the EMERGENCY BAPTISM (the only one in the sample P79–P103?); r84 the SCRAPED edge (the paper missing); r89 under the strip (the B side: Matija Muc × Marija Gregorič); r55 the torn father's cell; r31/r23/r79 covered cells; CROSS-ROW ×3 (r27+r90 the godfather Janez Muc = the r31 h91 father; the r47 godmother = the r69 mother; r68+r69 the same godfather 2 days); the »FRIEDMANN« stamp p. 179 (modern); the leap Feb 29, 1908 (r22!); the village forensics r28 Prilozje? + r42 Škrilje + r59 Štriglje? + r74 Prilozje 25 (four revised first readings); EXCLUDED: 7 (r1 Krasinec 38 the lead-forensics, r28 Prilozje?, r42 Škrilje, r44 stillborn, r59 Štriglje?, r74 Prilozje 25, r89 the strip); the script scripts/p103_parish_baptism_1908.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1908",
  p103Errors.length === 0,
  p103Errors.length === 0
    ? `19 vpisov / 18 hiš + 1 neberljiva (r84 postrgan rob) — NARE 18/18 · okvir 1908 skeni 189/190 (glava, P102 lead POTRJEN; forenzika 38) – 199 row 90 (glava 1909 INLINE r91 = P104 lead; 90 vrstic) · NOVELA: TRIJE novi dup pari (189/190 + 193/194 + 197/198 — vsi z dopolnitvami!) · stran == sken − 16/− 17/− 18/− 19 · 0 NOVIH hiš (0/1/0/0) · PT 14/4 · h24 13. VPIS (najbolj vpisovana) · h30 SEGINA POVRAT · h36 KRIŽAN POVRAT · h16 NOVAK POVRAT · h52 ISTA 10 LET · h23 ISTA 8 LET (Dehlič) · h65 MILEK 9. VPIS + boter 21 LET · h90 TRETJA UČITELJSKA (Kalan) · h85 NUJNI KRST + VRZEL 20 LET · h56 VRZEL 20 LET · h10 BRINEC 4. VPIS (mati menjava Kure) · h91 MUC 5. VPIS · h49 Brodarič 4. VPIS · NOV DUHOVNIK Jos. Dami (r23!) + Cerar 12 + Ravq 4 + PRAZEN 1 · babica Vötter VRNITEV (1×) + Muc 6 + Adlešič 8 + Meh 2 + Mavrenič 1 (18/18) · EMŠO 6 sidr VSI SKLADNI · EXCLUDED 7 · vitals 374 · kumulativ 382/85 DVAINDVAJSET+ENO let`
    : p103Errors.join("; "),
);
// qa-p104 — krstna 04105, polno leto 1909 (P104, issue #18)
// ---------------------------------------------------------------------------
// okvir 1909: skeni 199/200 (glava INLINE, dup; s200 = str. 180 — P103 ocava
// popravljena) + 201–211; stran == novela P104 (PET dup parov; glava 1910
// INLINE str. 187 = sken 211)
const p104PageOfScan = (s: number) =>
  s === 199 || s === 200 ? 180 : s === 201 ? 181 : s === 202 || s === 203 ? 182 : s === 204 || s === 205 ? 183 : s === 206 ? 184 : s === 207 || s === 208 ? 185 : s === 209 || s === 210 ? 186 : s === 211 ? 187 : s - 24;
const p104Hv = HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year === 1909);
const p104Errors: string[] = [];
if (p104Hv.length !== 18)
  p104Errors.push(`vpisov 1909 (04105, zasidrani) ≠ 18 (${p104Hv.length})`);
const p104Houses = new Set(p104Hv.map((h) => h.houseNo));
if (p104Houses.size !== 17)
  p104Errors.push(`različnih hiš ≠ 17 (${p104Houses.size}: ${[...p104Houses].sort((a, b) => Number(a) - Number(b)).join(",")})`);
// NARE PRELOM — h34 ×2 (dvojčka Matija+Nikolaj)
const p104RepeatHouses = [...p104Hv.map((h) => h.houseNo)].filter((hn, i, arr) => arr.indexOf(hn) !== i);
if (p104RepeatHouses.length !== 1 || p104RepeatHouses[0] !== "34")
  p104Errors.push(`intra-letna ponovitev 1909 ≠ ["34"] (NARE PRELOM — dvojčka h34) — najdeno: ${p104RepeatHouses.join(",")}`);
// okvir: stran == sken po P104 noveli (PET dup parov)
const p104BadPage = p104Hv.filter(
  (h) => h.status !== "DOCUMENTED" || !h.scan || !h.page
    || h.page !== p104PageOfScan(h.scan)
    || h.scan < 199 || h.scan > 211,
);
if (p104BadPage.length > 0)
  p104Errors.push(`scan/page ne ustreza P104 noveli: ${p104BadPage.map((h) => `${h.houseNo}@${h.scan}`).join(",")}`);
// 0 novih hiš (vzorec 1905–1909: 0/1/0/0/0)
const p104PriorHouses = new Set(
  HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year !== 1909).map((h) => h.houseNo),
);
const p104New = [...p104Houses].filter((hn) => !p104PriorHouses.has(hn));
if (p104New.length !== 0)
  p104Errors.push(`nove hiše 1909 ≠ [] (${p104New.join(",") || "brez"})`);
// sidra: h77 POŽEK POVRAT + h10 SELITEV + h42 ISTA ZVEZA + h72 POVRAČNICA
// + h33 PRENESEN + h63 SAMKA + h54 ŠIMEC + h1 ŽELJKO + h6 GENETSKO
// + h24 14. VPIS + h30 MARTINOVIČ + h12 VÖTTER DVOJNO + h35 PRIIMEK
// + h32 BITENC + h48 KRSTNI DATUM + h66 DVE ŠESTERKI
const p104H77 = p104Hv.find((h) => h.houseNo === "77");
if (!p104H77 || !p104H77.whatSi.includes("Jurij Požek") || !p104H77.whatSi.includes("POŽEK POVRAT") || !p104H77.whatSi.includes("19 LETIH"))
  p104Errors.push("h77 3. VPIS (POŽEK POVRAT po 19 letih; 1890 → 1902 Cindrič → 1909) ne ustreza");
const p104H10 = p104Hv.find((h) => h.houseNo === "10");
if (!p104H10 || !p104H10.whatSi.includes("Matija Brinec") || !p104H10.whatSi.includes("SELIITEV h30→h10") && !p104H10.whatSi.includes("SELITEV h30→h10"))
  p104Errors.push("h10 6. VPIS (SELIITEV h30→h10 — Matija Brinec × Marija Grabrijan ISTA ZVEZA kot h30 1906) ne ustreza");
const p104H42 = p104Hv.find((h) => h.houseNo === "42");
if (!p104H42 || !p104H42.whatSi.includes("Jurij Pezdirec") || !p104H42.whatSi.includes("Katarina Jurajevič") || !p104H42.whatSi.includes("4. VPIS"))
  p104Errors.push("h42 4. VPIS (ISTA ZVEZA 1905 vrne — Jurij Pezdirec × Katarina Jurajevič) ne ustreza");
const p104H72 = p104Hv.find((h) => h.houseNo === "72");
if (!p104H72 || !p104H72.whatSi.includes("Straus") || !p104H72.whatSi.includes("POVRAČNICA") || !p104H72.whatSi.includes("KARUSELJA"))
  p104Errors.push("h72 6. VPIS (STRAUŠ POVRAČNICA po 14 letih; h42↔h72 KARUSELJA) ne ustreza");
const p104H33 = p104Hv.find((h) => h.houseNo === "33");
if (!p104H33 || !p104H33.whatSi.includes("Papič") || !p104H33.whatSi.includes("PRENESEN") || !p104H33.whatSi.includes("MENJAVA DRUŽINE #3"))
  p104Errors.push("h33 3. VPIS (VPIS PRENESEN v mrliški register; MENJAVA #3 Papič?) ne ustreza");
const p104H63 = p104Hv.find((h) => h.houseNo === "63");
if (!p104H63 || !p104H63.whatSi.includes("samka") || !p104H63.whatSi.includes("9. VPIS"))
  p104Errors.push("h63 9. VPIS (mati »Katarina Križan, samka« — možen nezakonski) ne ustreza");
const p104H54 = p104Hv.find((h) => h.houseNo === "54");
if (!p104H54 || !p104H54.whatSi.includes("Janez Šimec") || !p104H54.whatSi.includes("Ivan Požek") || !p104H54.whatSi.includes("6. VPIS"))
  p104Errors.push("h54 6. VPIS (ŠIMEC nova družina; boter Ivan Požek) ne ustreza");
const p104H1 = p104Hv.find((h) => h.houseNo === "1");
if (!p104H1 || !p104H1.whatSi.includes("Jurij Željko") || !p104H1.whatSi.includes("Barbara Kure") || !p104H1.whatSi.includes("7. VPIS"))
  p104Errors.push("h1 7. VPIS (ISTA ZVEZA kot 1900+1905 — Jurij Željko × Barbara Kure) ne ustreza");
const p104H6 = p104Hv.find((h) => h.houseNo === "6");
if (!p104H6 || !p104H6.whatSi.includes("GENETSKO") || !p104H6.whatSi.includes("Marija Klepec") || !p104H6.whatSi.includes("4. VPIS"))
  p104Errors.push("h6 4. VPIS (HIŠA GENETSKO — celica pokrita; ISTA ZVEZA 1904/05 + botrinja Marija Klepec) ne ustreza");
const p104H24 = p104Hv.find((h) => h.houseNo === "24");
if (!p104H24 || !p104H24.whatSi.includes("14. VPIS") || !p104H24.whatSi.includes("PONESREČI") || !p104H24.whatSi.includes("Janez Brinec"))
  p104Errors.push("h24 14. VPIS ZAPORED (najbolj vpisovana; PONESREČI UMRLA 1965 s šolskim kolektivom) ne ustreza");
const p104H30 = p104Hv.find((h) => h.houseNo === "30");
if (!p104H30 || !p104H30.whatSi.includes("Martinovič") || !p104H30.whatSi.includes("Šimec") || !p104H30.whatSi.includes("12. VPIS"))
  p104Errors.push("h30 12. VPIS (7. DRUŽINA — Martinovič? kovač × Katarina Šimec) ne ustreza");
const p104H12 = p104Hv.find((h) => h.houseNo === "12");
if (!p104H12 || !p104H12.whatSi.includes("Drgoš") || !p104H12.whatSi.includes("VÖTTER DVOJNO"))
  p104Errors.push("h12 12. VPIS (Drgoš × Cvitkovič; VÖTTER DVOJNO — babica + botrinja) ne ustreza");
const p104H35 = p104Hv.find((h) => h.houseNo === "35");
if (!p104H35 || !p104H35.whatSi.includes("PRIIMEK NEZAPISAN") || !p104H35.whatSi.includes("Pezdirec"))
  p104Errors.push("h35 6. VPIS (MATI BREZ PRIIMKA — samo »Ana«; Pezdirec bajtar menjava) ne ustreza");
const p104H32 = p104Hv.find((h) => h.houseNo === "32");
if (!p104H32 || !p104H32.whatSi.includes("Matija Meh") || !p104H32.whatSi.includes("Marjeta Pezdirec") || !p104H32.whatSi.includes("Bitenc"))
  p104Errors.push("h32 10. VPIS (ISTA ZVEZA Meh × Pezdirec; maticarka Bitenc v koloni Podpis) ne ustreza");
const p104H48 = p104Hv.find((h) => h.houseNo === "48");
if (!p104H48 || !p104H48.whatSi.includes("KRSTNI datum") || !p104H48.whatSi.includes("Jurij Pezdirec"))
  p104Errors.push("h48 4. VPIS (EMŠO datum = KRSTNI datum — anomalija) ne ustreza");
const p104H66 = p104Hv.find((h) => h.houseNo === "66");
if (!p104H66 || !p104H66.whatSi.includes("Jakob Bohte") || !p104H66.whatSi.includes("Križan") || !p104H66.whatSi.includes("DVE ŠESTERKI"))
  p104Errors.push("h66 4. VPIS (Bohte × Križan; forenzika 66 — dve šestrki) ne ustreza");
// kontinuitete (zadnja leta pred 1909; pini po očetu/znakih — prior ALI current)
const p104Pins: Array<[string, number, string]> = [
  ["1", 1905, "Jurij Željko"],
  ["6", 1905, "Jakobič"],
  ["10", 1908, "Janez Brinec"],
  ["12", 1907, "Štrucelj"],
  ["24", 1908, "Janez Brinec"],
  ["30", 1908, "Segina"],
  ["32", 1903, "Meh"],
  ["33", 1898, "Dehlič"],
  ["34", 1906, "Šimec"],
  ["35", 1906, "Hrižan"],
  ["42", 1906, "Pozdirec"],
  ["48", 1907, "Jurij Pezdirec"],
  ["54", 1904, "Župančič"],
  ["63", 1903, "Uhr"],
  ["66", 1905, "Brodarič"],
  ["72", 1895, "Strauš"],
  ["77", 1902, "Cindrič"],
];
for (const [hn, yr, pin] of p104Pins) {
  const prior = HOUSE_VITALS.find((h) => h.bookSignature === "04105" && h.houseNo === hn && h.year === yr);
  const cur = p104Hv.find((h) => h.houseNo === hn);
  if (!prior || !cur) {
    p104Errors.push(`kontinuiteta hiša ${hn} (${yr} → 1909) manjka`);
    continue;
  }
  if (!prior.whatSi.includes(pin) && !cur.whatSi.includes(pin))
    p104Errors.push(`kontinuiteta hiša ${hn} (${yr}, pin ${pin}) ne ustreza`);
}
// vitals skupaj 449 (P106: 429 + 20; krstna 1911)
if (HOUSE_VITALS.length !== 685)
  p104Errors.push(`HOUSE_VITALS ≠ 467 (${HOUSE_VITALS.length})`);
// babica: 18/18 blokov; Meh 12 (DOMINANTA 1909) + Vötter 1 (DVOJNO z botrinjo)
if (p104Hv.filter((h) => h.whatSi.includes("babica")).length !== 18)
  p104Errors.push(`babica ni v vseh 18 whatSi (${p104Hv.filter((h) => h.whatSi.includes("babica")).length})`);
const p104Meh = p104Hv.filter((h) => h.whatSi.includes("babica Marija Meh")).length;
if (p104Meh !== 11)
  p104Errors.push(`babica Marija Meh ≠ 11× (${p104Meh} — DOMINANTA 1909; r32 neberljiva v bloku — 12. z dokazom)`);
const p104Votter = p104Hv.reduce((n, h) => n + (h.whatSi.split("Vötter").length - 1), 0);
if (p104Votter < 2)
  p104Errors.push(`Vötter pojavitev < 2 (${p104Votter} — babica Marjeta + botrinja Katarina = DVOJNO)`);
if (!p104Hv.some((h) => h.whatSi.includes("babica Marjeta Vötter") && h.whatSi.includes("Katarina Vötter")))
  p104Errors.push("Vötter DVOJNO (babica + botrinja v isti vrstici r58) manjka");
// duhovniki (bloki): Cerar 10 (vključno coop.) + Rauq 6 + Bitenc-nota 2
if (p104Hv.filter((h) => h.whatSi.includes("podpis Gregor Cerar")).length !== 10)
  p104Errors.push(`podpis Gregor Cerar ≠ 10× (${p104Hv.filter((h) => h.whatSi.includes("podpis Gregor Cerar")).length})`);
if (p104Hv.filter((h) => h.whatSi.includes("podpis Jos. Rauq")).length !== 6)
  p104Errors.push(`podpis Jos. Rauq ≠ 6× (${p104Hv.filter((h) => h.whatSi.includes("podpis Jos. Rauq")).length})`);
if (p104Hv.filter((h) => h.whatSi.includes("Bitenc")).length !== 2)
  p104Errors.push(`maticarka Bitenc v koloni Podpis ≠ 2× (${p104Hv.filter((h) => h.whatSi.includes("Bitenc")).length})`);
// EMŠO sidra v blokih: 6 (r9/r28/r30/r40/r44/r72; r64 = KRSTNI datum anomalija)
const p104Emso = p104Hv.filter((h) => h.whatSi.includes("sidro"));
if (p104Emso.length !== 6)
  p104Errors.push(`EMŠO sidrov v blokih ≠ 6 (${p104Emso.length} — r64 = KRSTNI datum anomalija brez markerja)`);
if (!p104Hv.some((h) => h.whatSi.includes("1910909505186")))
  p104Errors.push("EMŠO anomalija r64 (1910909505186 = krstni datum) manjka");
for (const emso of ["3001909500735", "020609500254", "0306095050335", "120809505944", "26079095?5231", "1910909505186", "051090505628"]) {
  if (!p104Hv.some((h) => h.whatSi.includes(emso)))
    p104Errors.push(`EMŠO sidro ${emso} manjka`);
}
push(
  "qa-p104-parish-baptism-1909",
  "P104: ŽUPNIJA PODZEMELJ — KRSTNA KNJIGA 04105, POLNO LETO 1909 (issue #18; SAMPLE-TRANSCRIPTION-1909; MERI, NE odloča; v7 join nespremenjen): širitev vzorca P79 (1886) → … → P101 (1906) → P102 (1907) → P103 (1908) na leto 1909 — okvir: glava »1909 / Januarij« INLINE na str. 180 = skeni 199/200 (dup par; 1909 r1 = Dobraviče 26 Anton 7./7. Januar, EMŠO 0701909500220 — P103 lead POTRJEN; P103 ocava »sken 200 = str. 181« POPRAVLJENA — s200 = str. 180, r89 1908 pod belim trakom berljiv SAMO na s200!) – row 81 na str. 187 (sken 211; glava »1910« INLINE; 1910 r1 = Cerkvišče 2 Anton 3./4. Januar — P105 lead; prva Griblje vrstica 1910 = r3 Griblje 5 Jožefa, Matija Štrucelj × Marija Meh) == tiskane strani 180–187 (81 vrstic — NAJKRAJŠE leto v vzorcu; 1908 = 90); NOVELA P104: PET dup parov skenov — 199/200 = str. 180 + 202/203 = str. 182 + 204/205 = str. 183 + 207/208 = str. 185 + 209/210 = str. 186 (največ v enem letu doslej); stran == sken − 19 (199/200) / − 20 (201–202) / − 21 (203–205) / − 22 (206–207) / − 23 (208–210) / − 24 (211); VSI vpisi z Griblji: 18 vpisov / 17 hiš (h34 ×2 = DVOJČKI Matija+Nikolaj, oba kot dojenčka umrla — NARE PRELOM, 1. intra-letna ponovitev po 1908 NARE 18/18); 0 NOVIH hiš (5. leto z 0: 0/1/0/0/0 — vse 17 hiš že zasidrane); PT 14/3 (42+48+54 v luknji 41–60 — ponovitve; luknja ostaja samo h51); kumulativ 420 vpisov / 85 hiš čez tri knjige in 25 let (1886–1910; 449 vitals); SIDRA: r6 h77 3. VPIS — POŽEK POVRAT po 19 LETIH (1890 Jurij Požek bajtar → 1902 MENJAVA Cindrič cevljar → 1909 ISTI oče z NOVO ženo Veselič?; najdaljša hišna vrzel 1909; cf. h21 Požek karusela); r9 h10 6. VPIS — SELITEV h30→h10 (Matija Brinec × Marija Grabrijan = ISTA ZVEZA kot h30 1906!; h10 = trije Brincovi možje zapored 1907/08/09; EMŠO 3001909500735; botra Janez+Ana Brinec); r17 h42 4. VPIS — ISTA ZVEZA 1905 VRNE (Jurij Pezdirec × Katarina Jurajevič — ISTA mati kot 1905/06; genetsko prek prior-bloka; poročena 20.11.1938; mož † 1943; † 26.4.1982 Črnomelj); r20+r21 h34 DVOJČKI (18./18. + 18./19. 4.; ISTA botra Nikolaj Segina + Katarina Šuštar na OBOJIH; Matija † 18/4.09 ISTI DAN!; Nikolaj † 3/4.10.09 — oba dojenčka umrla; 2. dvojčki-par z obema smrtma po 1907 h10); r28 h72 6. VPIS — STRAUŠ POVRAČNICA po 14 LETIH (1888–95 Matija Strauš v h72 → 1904 h42 interlude → 1909 DOMA; h42↔h72 ŠTRAUS↔PEZDIREC KARUSELJA — obe familiji 1909 v svoji hiši!; mati menjava #3 Šimec; EMŠO 020609500254; botra = ISTI PAR kot h42 1904 [Jožef Štrucelj + Barbara Jakobič]; babica Katarina Štraus; dan celici poškodovani [~]); r30 h33 3. VPIS — »VPIS PRENESEN V MRLIŠKI REGISTER« (MENJAVA #3: Brinec 1889 → Dehlič 1898 → Papič? 1909; VRZEL 11 LET; EMŠO 0306095050335; botra ISTI PRIIMEK [Mihael+Katarina Papič?]; podpis »Gregor Cerar coop.« — edini coop. 1909); r32 h63 9. VPIS — MATI »Katarina Križan, samka ½ zemljaka« (MOŽEN NEZAKONSKI VPIS; VRZEL 6 LET; oče Janez Papič? [~ Tepič]; EMŠO brez); r35 h54 6. VPIS — ŠIMEC NOVA DRUŽINA (Janez Šimec × Marija Kure?; boter Ivan Požek = POŽEK signal; VRZEL 5 LET; † 18.4.1978 Črnomelj); r37 h1 7. VPIS ISTA ZVEZA (Jurij Željko × Barbara Kure = 1900+1905; † 5.5.1925 pri 15 letih!; boter Jožef Željko); r40 h6 4. VPIS — HIŠNA CELICA POKRITA, HIŠA GENETSKO (celica prazna/pokrita z modrim pripisom na OBOJIH dup; starši = ISTA ZVEZA kot h6 1904/05 [Jurij × Katarina Jakobič] + botrinja Marija Klepec ISTA → genetska rešitev h6; 1907 Kapucina? menjava → 1909 POV RAT; EMŠO 120809505944 [~]); r44 h24 14. VPIS ZAPORED — ŠE VEDNO najbolj vpisovana hiša registra (Brincova; oče Janez Brinec; botra Matija+Marija Brinec; EMŠO 26079095?5231 [~]; PONESREČI UMRLA 23.10.1965 pri božjani s šolskim kolektivom [MK Ljubljana 1.1965] + drugi pripis 30.10.1988 Celovec? — DVOJNI smrtni pripisi!); r57 h30 12. VPIS — 7. DRUŽINA (France Martinovič? kovač × Katarina Šimec; forenzika 30 na OBOJIH dup [ni 36/50]; botra Janez+Marjeta Žugelj); r58 h12 12. VPIS — NOVA ZVEZA Drgoš × Cvitkovič (VÖTTER DVOJNO: babica Marjeta + botrinja Katarina!; boter Matija Štrucelj = 1910 r3 oče!); r60 h35 6. VPIS — MATI BREZ PRIIMKA (samo »Ana« — edini tak vpis v vzorcu!; oče Jožef Pezdirec bajtar = MENJAVA po Hrižan 1903/06); r61 h32 10. VPIS — ISTA ZVEZA (Matija Meh × Marjeta Pezdirec = 1889–95 variante ISTEGA para; VRZEL 6 LET; poročena 1.2.1936; podpis-kolono prevzame MATICARKA Paulin Bitenc — NOVELA!); r64 h48 4. VPIS — EMŠO 1910909505186 = KRSTNI datum (rojstvo 18.10 — maticar uporabil krsto; edinski primer!; poročin 22.1.1933 KLEPEC — MOŽ UMRL); r72 h66 4. VPIS (Jakob Bohte × Katarina Križan; forenzika 66 — DVE ŠESTERKI, prva branja 22/72 NAPAČNA; boter Nikolaj Brodarič = ISTI kot r64 CROSS-ROW; botrinja Marija Straus; EMŠO 051090505628 [~]; † 30.8.1994 Griblje); DUHOVNIKI: Gregor Cerar 10 (Januar–Junij; vključno r30 »coop.«) + Jos. Rauq 6 (Avgust–Oktober: r40–r64) + 2 podpisa maticarke Paulin Bitenc v koloni Podpis (r61/r72 — NOVELA: od r61 dalje maticarka podpisuje ob smrtnih pripisih 1950s–60s); BABICA NOVELA: na Gribljih 18/18 imenovanih: MARIJA MEH 12/18 DOMINANTA 1909 + Barbara Adlešič 1 (r9) + Katarina Štraus 1 (r28) + Ana Mavrenič 1 (r30) + Marija Uri? 1 (r40) + Ana Novak 1 (r57) + Marjeta Vötter 1 (r58 — DVOJNO z botrinjo); Muc 0× (po 6× 1908!); EMŠO kampanja: 7 sidr na Gribljih (6+1 anomalija r64) — VSI SKLADNI z rojstvi (r64 = krsta!); ANOMALIJE: r5 »Decembar 16./16.« Grm 36 POD glavo 1909 (kronološka kršitev!) + r91 = aprilski vpis 1908 nad glavo; h42↔h72 karusela; POŽEK 19 let; selitev h30→h10; dvojčki z obema smrtma; mati samka (r32); mati brez priimka (r60); EMŠO=krsta (r64); maticarka v podpis-koloni (r61+); PONESREČI UMRLA (r44 1965!); 2 RAZVELJAVITVI zakona (r73 Krško 52/195-3 + r76); TRGOGRAD pripis (r19 Gradac — št. 13-546/65!); »Vzet v matični register 13.02.200X« (r65 Vranovče — matičarka); Podzemelj 6 vpis (r63 — redko!); mejni vpis r81 (31.12.1909/1.1.1910); kraj »Gornej?« ×4 (r12/r22/r47/r76 z Muc/Pezdirec familijami); CROSS-ROW ×4 (r64+r72 boter Nikolaj Brodarič; r35 boter Ivan Požek ↔ r6 oče; r57 mati Šimec ↔ r35 oče; r32+r72 mati Križan); EXCLUDED: 22 (r1 Dobravice 26 lead, r2–r5, r7/r8, r10/r11, r12, r13–r16, r18/r19 TRGOGRAD, r22 Gornej?, r23–r27, r29, r31 †13/6.09 dojenček, r33/r34, r36–r41, r42/r43, r45–r53 [r48 EMŠO 5104?? invalid], r54–r56, r59, r62 Kapljišče?, r63 Podzemelj, r65–r71 [r65 vzet v matični register], r73 RAZVELJAVITEV, r74–r80, r81 mejni); skripta scripts/p104_parish_baptism_1909.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1909",
  "P104: PARISH OF PODZEMELJ — BAPTISM REGISTER 04105, THE FULL YEAR 1909 (issue #18; SAMPLE-TRANSCRIPTION-1909; MEASURES, does not decide; the v7 join unchanged): extending the sample P79 (1886) → … → P103 (1908) to 1909 — the frame: the heading »1909 / Januarij« INLINE on p. 180 = scans 199/200 (a dup pair; the 1909 r1 = Dobraviče 26 Anton Jan 7/7, personal ID 0701909500220 — the P103 lead CONFIRMED; the P103 note »scan 200 = p. 181« CORRECTED — s200 = p. 180, the 1908 r89 under the white strip legible ONLY on s200!) – row 81 on p. 187 (scan 211; the heading »1910« INLINE; the 1910 r1 = Cerkvišče 2 Anton Jan 3/4 — the P105 lead; the first Griblje row of 1910 = r3 Griblje 5 Jožefa, Matija Štrucelj × Marija Meh) == printed pages 180–187 (81 rows — the SHORTEST year in the sample; 1908 = 90); THE P104 NOVEL: FIVE duplicated scan pairs — 199/200 = p. 180 + 202/203 = p. 182 + 204/205 = p. 183 + 207/208 = p. 185 + 209/210 = p. 186 (the most in one year so far); page == scan − 19 (199/200) / − 20 (201–202) / − 21 (203–205) / − 22 (206–207) / − 23 (208–210) / − 24 (211); ALL Griblje entries: 18 entries / 17 houses (h34 ×2 = the TWINS Matija+Nikolaj, both dead as infants — the NARE BREAK, the 1st intra-year repeat after the 1908 NARE 18/18); 0 NEW houses (the 5th year with 0: 0/1/0/0/0 — all 17 houses already anchored); the PT 14/3 (42+48+54 in the gap 41–60 — repeats; only h51 remains); the cumulative 420 entries / 85 houses across three books and 25 years (1886–1910; 449 vitals); ANCHORS: r6 h77 the 3rd ENTRY — the POŽEK RETURN after 19 YEARS (1890 Jurij Požek the cottager → the 1902 CHANGE Cindrič the ropemaker → 1909 the SAME father with a NEW wife Veselič?; the longest house gap of 1909; cf. the h21 Požek carousel); r9 h10 the 6th ENTRY — the MOVE h30→h10 (Matija Brinec × Marija Grabrijan = the SAME COUPLE as h30 1906!; h10 = three Brinec husbands in a row 1907/08/09; personal ID 3001909500735; the godparents Janez+Ana Brinec); r17 h42 the 4th ENTRY — the SAME COUPLE OF 1905 RETURNS (Jurij Pezdirec × Katarina Jurajevič — the SAME mother as 1905/06; genetically via the prior block; married Nov 20, 1938; the husband † 1943; † Apr 26, 1982 Črnomelj); r20+r21 h34 the TWINS (Apr 18/18 + 18/19; the SAME godparents Nikolaj Segina + Katarina Šuštar on BOTH; Matija died Apr 18, 1909 THE SAME DAY!; Nikolaj died Oct 3/4, 1909 — both infants dead; the 2nd twins-pair with both deaths after the 1907 h10); r28 h72 the 6th ENTRY — the STRAUŠ HOMECOMING after 14 YEARS (1888–95 Matija Strauš in h72 → the 1904 h42 interlude → 1909 HOME; the h42↔h72 ŠTRAUS↔PEZDIREC CAROUSEL — both families 1909 in their own house!; the mother change #3 Šimec; personal ID 020609500254; the godparents = the SAME COUPLE as h42 1904 [Jožef Štrucelj + Barbara Jakobič]; the midwife Katarina Štraus; the day cells damaged [~]); r30 h33 the 3rd ENTRY — »THE ENTRY TRANSFERRED TO THE DEATH REGISTER« (a FAMILY CHANGE #3: Brinec 1889 → Dehlič 1898 → Papič? 1909; an 11-YEAR GAP; personal ID 0306095050335; the godparents the SAME SURNAME [Mihael+Katarina Papič?]; the signature »Gregor Cerar coop.« — the only coop. of 1909); r32 h63 the 9th ENTRY — the MOTHER »Katarina Križan, samka ½ zemljaka« (a POSSIBLE ILLEGITIMATE ENTRY; a 6-YEAR GAP; the father Janez Papič? [~ Tepič]); r35 h54 the 6th ENTRY — the ŠIMEC NEW FAMILY (Janez Šimec × Marija Kure?; the godfather Ivan Požek = the POŽEK signal; a 5-YEAR GAP; † Apr 18, 1978 Črnomelj); r37 h1 the 7th ENTRY the SAME COUPLE (Jurij Željko × Barbara Kure = 1900+1905; † May 5, 1925 aged 15!; the godfather Jožef Željko); r40 h6 the 4th ENTRY — the HOUSE CELL COVERED, THE HOUSE GENETICALLY (the cell empty/covered by a blue note on BOTH dups; the parents = the SAME COUPLE as h6 1904/05 [Jurij × Katarina Jakobič] + the godmother Marija Klepec the SAME → the genetic solution h6; the 1907 Kapucina? change → the 1909 RETURN; personal ID 120809505944 [~]); r44 h24 the 14th CONSECUTIVE ENTRY — STILL the most-entered house of the register (the Brinec house; the father Janez Brinec; the godparents Matija+Marija Brinec; personal ID 26079095?5231 [~]; SHE DIED IN AN ACCIDENT Oct 23, 1965 during a pilgrimage with a school group [MK Ljubljana 1.1965] + a second note Oct 30, 1988 Celovec? — DOUBLE death notes!); r57 h30 the 12th ENTRY — the 7th FAMILY (France Martinovič? the smith × Katarina Šimec; the forensics 30 on BOTH dups [not 36/50]; the godparents Janez+Marjeta Žugelj); r58 h12 the 12th ENTRY — the NEW COUPLE Drgoš × Cvitkovič (the VÖTTER DOUBLE: the midwife Marjeta + the godmother Katarina!; the godfather Matija Štrucelj = the 1910 r3 father!); r60 h35 the 6th ENTRY — THE MOTHER WITHOUT A SURNAME (only »Ana« — the only such entry in the sample!; the father Jožef Pezdirec the cottager = a CHANGE after Hrižan 1903/06); r61 h32 the 10th ENTRY — the SAME COUPLE (Matija Meh × Marjeta Pezdirec = the 1889–95 variants of the SAME couple; a 6-YEAR GAP; married Feb 1, 1936; the signature column taken over by THE REGISTRAR Paulin Bitenc — a NOVELTY!); r64 h48 the 4th ENTRY — the personal ID 1910909505186 = THE BAPTISM DATE (the birth Oct 18 — the registrar used the baptism; the only such case!; married Jan 22, 1933 KLEPEC — the HUSBAND DIED); r72 h66 the 4th ENTRY (Jakob Bohte × Katarina Križan; the forensics 66 — TWO SIXES, the first readings 22/72 WRONG; the godfather Nikolaj Brodarič = the SAME as r64 CROSS-ROW; the godmother Marija Straus; personal ID 051090505628 [~]; † Aug 30, 1994 Griblje); PRIESTS: Gregor Cerar 10 (January–June; incl. the r30 »coop.«) + Jos. Rauq 6 (August–October: r40–r64) + 2 signatures of the registrar Paulin Bitenc in the signature column (r61/r72 — a NOVELTY: from r61 on the registrar signs at the death annotations of the 1950s–60s); MIDWIFE NOVEL: in Griblje 18/18 named: MARIJA MEH 12/18 THE DOMINANT OF 1909 + Barbara Adlešič 1 (r9) + Katarina Štraus 1 (r28) + Ana Mavrenič 1 (r30) + Marija Uri? 1 (r40) + Ana Novak 1 (r57) + Marjeta Vötter 1 (r58 — DOUBLE with the godmother); Muc 0× (after the 6× of 1908!); the personal-ID campaign: 7 anchors in Griblje (6+1 the r64 anomaly) — ALL CONSISTENT with the births (r64 = the baptism!); ANOMALIES: the r5 »Decembar 16./16.« Grm 36 UNDER the 1909 heading (a chronological violation!) + the r91 = an April 1908 entry above the heading; the h42↔h72 carousel; the POŽEK 19 years; the move h30→h10; the twins with both deaths; the samka mother (r32); the mother without a surname (r60); the ID=baptism (r64); the registrar in the signature column (r61+); SHE DIED IN AN ACCIDENT (r44 1965!); 2 marriage ANNULMENTS (r73 Krško 52/195-3 + r76); the TRGOGRAD note (r19 Gradac — no. 13-546/65!); »Taken into the civil register Feb 13, 200X« (r65 Vranovče — the registrar); a Podzemelj 6 entry (r63 — rare!); the boundary entry r81 (Dec 31, 1909/Jan 1, 1910); the village »Gornej?« ×4 (r12/r22/r47/r76 with the Muc/Pezdirec families); CROSS-ROW ×4 (r64+r72 the godfather Nikolaj Brodarič; the r35 godfather Ivan Požek ↔ the r6 father; the r57 mother Šimec ↔ the r35 father; the r32+r72 mother Križan); EXCLUDED: 22 (r1 Dobravice 26 the lead, r2–r5, r7/r8, r10/r11, r12, r13–r16, r18/r19 TRGOGRAD, r22 Gornej?, r23–r27, r29, r31 the infant † Jun 13, 1909, r33/r34, r36–r41, r42/r43, r45–r53 [r48 the ID 5104?? invalid], r54–r56, r59, r62 Kapljišče?, r63 Podzemelj, r65–r71 [r65 taken into the civil register], r73 the ANNULMENT, r74–r80, r81 the boundary); the script scripts/p104_parish_baptism_1909.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1909",
  p104Errors.length === 0,
  p104Errors.length === 0
    ? `18 vpisov / 17 hiš (h34 ×2 dvojčka † oba) — NARE PRELOM · okvir 1909 skeni 199/200 (glava INLINE, s200 = str. 180 — P103 ocava POPRAVLJENA!) – 211 row 81 (glava 1910 INLINE = P105 lead; 81 vrstic — najkrajše leto) · NOVELA: PET dup parov (199/200 + 202/203 + 204/205 + 207/208 + 209/210) · stran == sken − 19…− 24 · 0 NOVIH hiš (0/1/0/0/0 — 5. leto) · PT 14/3 · h77 POŽEK POVRAT po 19 LETIH · h10 SELITEV h30→h10 (trije Brinci zapored) · h42 ISTA ZVEZA 1905 VRNE · h72 STRAUŠ POVRAČNICA po 14 LETIH (h42↔h72 KARUSELJA!) · h34 DVOJČKI (ISTA botra; † isti dan + † oktober) · h33 VPIS PRENESEN v mrliški register + MENJAVA #3 (VRZEL 11) · h63 mati SAMKA (možen nezakonski) · h54 ŠIMEC × KURE + boter Ivan Požek · h1 ŽELJKO × KURE 7. VPIS · h6 GENETSKO (celica pokrita) · h24 14. VPIS + PONESREČI UMRLA 1965 · h30 7. DRUŽINA Martinovič? · h12 VÖTTER DVOJNO · h35 MATI BREZ PRIIMKA · h32 maticarka BITENC v koloni Podpis · h48 EMŠO = KRSTA · h66 DVE ŠESTERKI (Bohte × Križan) · Cerar 10 + Rauq 6 + Bitenc 2 · babica MEH 12/18 DOMINANTA + Vötter 1 (18/18) · EMŠO 7 sidr (r64 = krsta!) · EXCLUDED 22 · vitals 467 · kumulativ 420/85 25 let`
    : p104Errors.join("; "),
);

// ---------------------------------------------------------------------------
// qa-p105 — krstna 04105, polno leto 1910 (P105, issue #18)
// ---------------------------------------------------------------------------
// okvir 1910: skeni 211–219 (glava INLINE str. 187 = sken 211 pod vsoto 1909);
// stran == sken − 24 (211–216) / DUP 217 == str. 192 (EN dup par!) / − 25
// (218–219); glava 1911 INLINE str. 194 = sken 219
const p105PageOfScan = (s: number) =>
  s === 211 ? 187 : s === 212 ? 188 : s === 213 ? 189 : s === 214 ? 190 : s === 215 ? 191 : s === 216 || s === 217 ? 192 : s === 218 ? 193 : s === 219 ? 194 : s - 25;
const p105Hv = HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year === 1910);
const p105Errors: string[] = [];
if (p105Hv.length !== 20)
  p105Errors.push(`vpisov 1910 (04105, zasidrani) ≠ 20 (${p105Hv.length})`);
const p105Houses = new Set(p105Hv.map((h) => h.houseNo));
if (p105Houses.size !== 20)
  p105Errors.push(`različnih hiš ≠ 20 (NARE 20/20) (${p105Houses.size}: ${[...p105Houses].sort((a, b) => Number(a) - Number(b)).join(",")})`);
// NARE 20/20 — brez intra-letnih ponovitev (po P104 prelomu h34×2 spet čisto)
const p105RepeatHouses = [...p105Hv.map((h) => h.houseNo)].filter((hn, i, arr) => arr.indexOf(hn) !== i);
if (p105RepeatHouses.length !== 0)
  p105Errors.push(`intra-letne ponovitve 1910 ≠ [] (NARE 20/20) — najdeno: ${p105RepeatHouses.join(",")}`);
// okvir: stran == sken po P105 noveli (EN dup par 216/217)
const p105BadPage = p105Hv.filter(
  (h) => h.status !== "DOCUMENTED" || !h.scan || !h.page
    || h.page !== p105PageOfScan(h.scan)
    || h.scan < 211 || h.scan > 219,
);
if (p105BadPage.length > 0)
  p105Errors.push(`scan/page ne ustreza P105 noveli (dup 216/217 = str. 192): ${p105BadPage.map((h) => `${h.houseNo}@${h.scan}`).join(",")}`);
// 0 novih hiš (vzorec 1905–1910: 0/1/0/0/0/0)
const p105PriorHouses = new Set(
  HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year !== 1910).map((h) => h.houseNo),
);
const p105New = [...p105Houses].filter((hn) => !p105PriorHouses.has(hn));
if (p105New.length !== 0)
  p105Errors.push(`nove hiše 1910 ≠ [] (${p105New.join(",") || "brez"})`);
// sidra: h5 ŠTRUCELJ 5. VPIS + h29 NEZAKONSKI (vrzel 15) + h18 POVRAT Kambič
// + h44 ŠTRUCELJ 5. + h34 SEGINA 3. (TRETJE leto) + h60 ŽELJKO 9. + h90 KALAN
// učitelj + h21 POŽEK 7. + h35 7. (babica PRAZNO) + h22 MILEK 5. + h91 MUC 6.
// (OČE MENJAVA) + h46 BRODARIČ 7. + h65 MILEK 10. (popravek 45 napačen)
// + h49 BRODARIČ 5. + h28 NEZAKONSKA (vrzel 19; Kalan CROSS-ROW) + h6
// JAKOBIČ 5. + h42 GENETSKA REŠITEV + h1 TROME 8. (OČE MENJAVA) + h16 NOVAK 9.
// (botra PRAZNO) + h88 STRMEC 2.
const p105Pins: Array<[string, string]> = [
  ["5", "5. VPIS"], ["5", "Štrucelj"],
  ["88", "2. VPIS"], ["88", "Strmec"],
  ["29", "NEZAKONSKI"], ["29", "4. VPIS"], ["29", "15 LET"],
  ["18", "POVRAT"], ["18", "Kambič"], ["18", "23.06.2003"],
  ["44", "5. VPIS"], ["44", "Štrucelj"],
  ["34", "8. VPIS"], ["34", "Segina"], ["34", "TRETJE leto"],
  ["60", "9. VPIS"], ["60", "Željko"], ["60", "Kolehko"],
  ["90", "učitelj"], ["90", "Kalan"],
  ["21", "7. VPIS"], ["21", "Kazimir"], ["21", "MATI MENJANA"],
  ["35", "7. VPIS"], ["35", "babica PRAZNA"],
  ["22", "5. VPIS"], ["22", "Milek"],
  ["91", "6. VPIS"], ["91", "OČE MENJAVA"], ["91", "ISTA 6×"],
  ["46", "Brodarič"],
  ["65", "10. VPIS"], ["65", "NAPAČEN"],
  ["49", "5. VPIS"], ["49", "Brodarič"], ["49", "5.5.1957"],
  ["28", "NEZAKONSKA"], ["28", "19 LET"], ["28", "CROSS-ROW"],
  ["6", "5. VPIS"], ["6", "Jakobič"], ["6", "ISTI DAN"],
  ["42", "GENETSKA REŠITEV"], ["42", "Pezdirec"],
  ["1", "8. VPIS"], ["1", "Trome"], ["1", "OČE MENJAVA"], ["1", "Paulin Bitnar"],
  ["16", "9. VPIS"], ["16", "Novak"], ["16", "botra PRAZNA"], ["16", "h60 1904"],
];
for (const [hn, pin] of p105Pins) {
  const cur = p105Hv.find((h) => h.houseNo === hn);
  if (!cur) {
    p105Errors.push(`sidro hiša ${hn} manjka`);
    continue;
  }
  if (!cur.whatSi.includes(pin))
    p105Errors.push(`sidro hiša ${hn} (pin ${pin}) ne ustreza`);
}
// kontinuitete (zadnja leta pred 1910; pini po očetu/znakih — prior ALI current)
const p105Cont: Array<[string, number, string]> = [
  ["1", 1909, "Jurij Željko"],
  ["5", 1907, "Štrucel"],
  ["6", 1909, "Jakobič"],
  ["16", 1908, "Novak"],
  ["18", 1906, "Kambič"],
  ["21", 1906, "Požek"],
  ["22", 1905, "Milek"],
  ["28", 1891, "Požek"],
  ["29", 1892, "Milek"],
  ["34", 1909, "Šulak"],
  ["35", 1909, "PRIIMEK NEZAPISAN"],
  ["42", 1909, "Pezdirec"],
  ["44", 1908, "Štrucelj"],
  ["46", 1908, "Brodarič"],
  ["49", 1908, "Brodarič"],
  ["60", 1908, "Željko"],
  ["65", 1908, "Milek"],
  ["88", 1904, "Brinec"],
  ["90", 1908, "Kalan"],
  ["91", 1908, "Muc"],
];
for (const [hn, yr, pin] of p105Cont) {
  const prior = HOUSE_VITALS.find((h) => h.bookSignature === "04105" && h.houseNo === hn && h.year === yr);
  const cur = p105Hv.find((h) => h.houseNo === hn);
  if (!prior || !cur) {
    p105Errors.push(`kontinuiteta hiša ${hn} (${yr} → 1910) manjka`);
    continue;
  }
  if (!prior.whatSi.includes(pin) && !cur.whatSi.includes(pin))
    p105Errors.push(`kontinuiteta hiša ${hn} (${yr}, pin ${pin}) ne ustreza`);
}
// vitals skupaj 449 (po P106: 429 + 20; krstna 1911)
if (HOUSE_VITALS.length !== 685)
  p105Errors.push(`HOUSE_VITALS ≠ 467 (${HOUSE_VITALS.length})`);
// babica: 20/20 whatSi; Meh 15 (DOMINANTA 1910; r7 samo priimek + r83 Ana Meh)
if (p105Hv.filter((h) => h.whatSi.includes("babica")).length !== 20)
  p105Errors.push(`babica ni v vseh 20 whatSi (${p105Hv.filter((h) => h.whatSi.includes("babica")).length})`);
const p105Meh = p105Hv.filter((h) => h.whatSi.includes("babica Marija Meh")).length;
if (p105Meh !== 14)
  p105Errors.push(`babica Marija Meh ≠ 14× (${p105Meh} — DOMINANTA 1910; r7 »Meh« brez imena — 15. z dokazom; r83 Ana Meh)`);
if (!p105Hv.some((h) => h.houseNo === "1" && h.whatSi.includes("babica Ana Meh") && h.whatSi.includes("MEH ×2")))
  p105Errors.push("r83 MEH ×2 (mati Marija Meh + babica Ana Meh — isti priimek!) manjka");
// podpisi (bloki): Bitnar 13 (ISTA roka kot P104 maticarka — NOVELA dilema)
// + Rauq 7 (nadaljevanje 1909)
if (p105Hv.filter((h) => h.whatSi.includes("Bitnar")).length !== 13)
  p105Errors.push(`podpis Bitnar ≠ 13× (${p105Hv.filter((h) => h.whatSi.includes("Bitnar")).length} — Laulin/Paulin ISTA roka)`);
if (p105Hv.filter((h) => h.whatSi.includes("podpis Jos. Rauq")).length !== 7)
  p105Errors.push(`podpis Jos. Rauq ≠ 7× (${p105Hv.filter((h) => h.whatSi.includes("podpis Jos. Rauq")).length})`);
if (!p105Hv.some((h) => h.houseNo === "1" && h.whatSi.includes("podpis Paulin Bitnar (jasni P")))
  p105Errors.push("r83 podpis »Paulin Bitnar« z jasnimi P (dokaz ISTA roka Laulin/Paulin) manjka");
if (!p105Hv.some((h) => h.houseNo === "1" && h.whatSi.includes("OČE MENJAVA")))
  p105Errors.push("h1 OČE MENJAVA (Željko 1888–1909 → Trome 1910) manjka");
// EMŠO sidra v blokih: 5 (r3/r18/r22/r47/r66 — vsi SKLADNI; 2× datumski popravki)
const p105Emso = p105Hv.filter((h) => h.whatSi.includes("sidro"));
if (p105Emso.length !== 5)
  p105Errors.push(`EMŠO sidrov v blokih ≠ 5 (${p105Emso.length})`);
for (const emso of ["0801910505931", "0703910505638", "0403910500260", "2506910505074", "2809910500547"]) {
  if (!p105Hv.some((h) => h.whatSi.includes(emso)))
    p105Errors.push(`EMŠO sidro ${emso} manjka`);
}
push(
  "qa-p105-parish-baptism-1910",
  "P105: ŽUPNIJA PODZEMELJ — KRSTNA KNJIGA 04105, POLNO LETO 1910 (issue #18; SAMPLE-TRANSCRIPTION-1910; MERI, NE odloča; v7 join nespremenjen): širitev vzorca P79 (1886) → … → P102 (1907) → P103 (1908) → P104 (1909) na leto 1910 — okvir: glava »1910 / Januar« INLINE na str. 187 = sken 211 (pod vsoto 1909; s211/s212 SOSEDNJA — ni dup; 1910 r1 = Cerkvišče 2 Anton 3./4. Januar, EMŠO 0301910500241 — P104 lead POTRJEN) – row 84 na str. 194 (sken 219; glava »~1911~« INLINE; 1911 r1 = Begunja vas 14 Anton 8./9. Januar, EMŠO 0801911500623 — P106 lead; prva Griblje vrstica 1911 = r3 Griblje 34 Antonia, Janez Brinec × Ana Milek — h34 TRETJE leto!) == tiskane strani 187–194 (84 vrstic; 1908 = 90, 1909 = 81); NOVELA P105: EN dup par — 216/217 = str. 192 (najmanj od P102: P103 ×3, P104 ×5; s217 za复核 r64–r67); stran == sken − 24 (211–216) / DUP 217 == 192 / − 25 (218–219); VSI vpisi z Griblji: 20 vpisov / 20 hiš — NARE 20/20 (po P104 prelomu h34×2 spet brez intra-letnih ponovitev); 0 NOVIH hiš (6. leto z 0: 0/1/0/0/0/0); PT 15/5 (42+44+46+49+60 v luknji 41–60 — ponovitve; luknja ostaja samo h51); kumulativ 420 vpisov / 85 hiš čez tri knjige in 25 let (1886–1910; 449 vitals); SIDRA: r3 h5 5. VPIS (Štrucelj × Meh 5. skupaj 1891–1910; EMŠO 0801910505931; ime »?exa« neberljivo — P104 lead »Jožefa« NAPAČNA ugiba; † 19.11.1983); r7 h88 2. VPIS (natrgan rob str. 187); r10 h29 4. VPIS — VRZEL 15 LET + NEZAKONSKI (oče PRAZNO, mati Barbara Milek sama = h29 Milekova familija!); r18 h18 4. VPIS — POVRAT Šimec × Kambič (1906 par; 1907 Brinec intermezzo; VPIS PRENEŠEN 23.06.2003; EMŠO 0703910505638); r22 h44 5. VPIS (Jožef Štrucelj 3.× zapored 1906/08/10; EMŠO 0403910500260 — datumski popravek rojstev 4.); r26 h34 8. VPIS — TRETJE leto zapored (1909 dvojčki → 1910 → 1911 lead; oče Nikolaj Šulak? pod trakom [prvo branje »Vidak«]; ISTI boter Nikolaj Segina 3. skupaj!; † 30.10.1963 v Gribljah št. 73); r32 h60 9. VPIS (Nikolaj Željko — branje »Kolehko«; VPIS PRENEŠEN 23.05.2001); r33 h90 6. VPIS — UČITELJSKA (Kopitar 1890/92 → Vetročnik 1898/1900 → Kalan 1908/1910 Vincencij — 4. učiteljska družina; † 19.10.1910); r39 h21 7. VPIS (oče »…mir« Požek = morda KAZIMIR — h21 1888 nezakonski »Kaxmarp« POVRET!; mati menjava Ana Šimec → Katarina Kure); r42 h35 7. VPIS (forenzika 35 ne 85; babica PRAZNA; mati menjava Ana → Barbara Križan/Hrižan?; † 26/6); r47 h22 5. VPIS (Nikolaj Milek ISTI 5×; EMŠO 2506910505074; boter Ivan Požek; forenzika 22 ne 23); r48 h91 6. VPIS — OČE MENJAVA Janez→Matija Muc (mati Ana Kure ISTA 6×!; boter Jurij Jakofčič = h6 oče CROSS-ROW; † 18/9); r54 h46 7. VPIS (forenzika 46 — prva branja 6/14/16 NAPAČNA; genetika Anton Brodarič × Katarina Milek = 1908 ISTA; EMŠO 180791055019 [~]); r66 h65 10. VPIS (Matija Milek 10.× — MILEK kontinuiteta 1887–1910!; forenzika 65 na obojih dup; POPRAVEK matičarja »št. 45« NAPAČEN; EMŠO 2809910500547 — datumski popravek 28.); r67 h49 5. VPIS (Nikolaj Brodarič; boter Jakop Bohte = r10 boter 2.×; VPIS PRENEŠEN 5.5.1957); r72 h28 2. VPIS — VRZEL 19 LET (1891→1910 — izenačen REKORD z h77 1909!) + NEZAKONSKA (mati Marjeta Sodek? samota; botrinja Marija Kalan učiteljeva žena = CROSS-ROW h90 r33!); r78 h6 5. VPIS (Jakobič 4.×; botrinja Marija Klepec 3.×; † 19/11 ISTI DAN!); r79 h42 5. VPIS — GENETSKA REŠITEV forenzike (»16« NAPAČNA — h16 = Novak r84 kolizija nemogoča; Pezdirec × Jurajevič 2. leto); r83 h1 8. VPIS — OČE MENJAVA Željko→Janez Trome (7 vpisov konec; Željko hkrati h60!; mati + babica MEH ×2; podpis jasni P »Paulin Bitnar« = DOKAZ ISTA roka; poroka 17.2.1936 → † 14.3.1936 MESEC PO POROKI!); r84 h16 9. VPIS (Alojzij Novak × Marija Frlah? = h60 1904 par — Novak karusela h60↔h16; botra PRAZNA; † 11/12 ISTI DAN — zadnja vrstica!); DUHOVNIKI/PODPISI NOVELA: »Laulin/Paulin Bitnar« 13 (ISTA ROKA kot P104 maticarka »Paulin Bitenc« — dilema: NOV KAPLAN ALI maticarka v koloni mašnika; r83 jasni P = ista oseba piše P/L variante!) + »Jos. Rauq« 7 (nadaljevanje 1909 Avg–Okt); blokovska alternacija (Januar samo Bitnar r1–r6); BABICA: 20/20 whatSi — MARIJA MEH 15/20 DOMINANTA 1910 (najvišja doslej!) + Ana Meh 1 (r83 mati+babica MEH ×2!) + Marjeta Toter 1 + Ana Mavrenič 1 (h90) + Barbara Adlešič 1 (h65) + 1 prazna (r42); EMŠO kampanja: 5 sidr — VSI SKLADNI (2× datumski popravki iz EMŠO: r22 rojstva 4., r66 rojstva 28.); ANOMALIJE: 2 NEZAKONSKA (r10 + r72); 2 PRAZNI botri (r42 babica + r84 botra); 5 DOJENČKOV † (r33/r42/r48/r78/r84 — 2× ISTI DAN kot krst: r78 + r84 zadnja vrstica!); OČE MENJAVA h1 + h91; MATI MENJAVA h21 + h35; genetski popravki forenzike (h42 »16« / h65 »45« / h34 »Vidak« / h60 »Kolehko« / h46 6/14/16 / h22 23 / h35 85); VPIS PRENEŠEN ×3 (r18/r32/r67); MESEC PO POROKI (r83); h28 + h29 VRZELI 19/15 LET; Klepec botrinja 3× (r32/r78/r83); EXCLUDED: 61 (r1 Cerkvišče 2 lead, r43 G?i?ice 3 neberljiva pod plastiko, r64 »opatovina?« 30 — ne-Griblje + nalepka maticarja 1953 na dup); skripta scripts/p105_parish_baptism_1910.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1910",
  "P105: PARISH OF PODZEMELJ — BAPTISM REGISTER 04105, THE FULL YEAR 1910 (issue #18; SAMPLE-TRANSCRIPTION-1910; MEASURES, does not decide; the v7 join unchanged): extending the sample P79 (1886) → … → P103 (1908) → P104 (1909) to 1910 — the frame: the heading »1910 / Januar« INLINE on p. 187 = scan 211 (below the 1909 total row; s211/s212 CONSECUTIVE — no dup; the 1910 r1 = Cerkvišče 2 Anton Jan 3/4, personal ID 0301910500241 — the P104 lead CONFIRMED) – row 84 on p. 194 (scan 219; the heading »~1911~« INLINE; the 1911 r1 = Begunja vas 14 Anton Jan 8/9, personal ID 0801911500623 — the P106 lead; the first Griblje row of 1911 = r3 Griblje 34 Antonia, Janez Brinec × Ana Milek — h34 the THIRD year!) == printed pages 187–194 (84 rows; 1908 = 90, 1909 = 81); THE P105 NOVEL: ONE dup pair — 216/217 = p. 192 (the fewest since P102: P103 ×3, P104 ×5; s217 for re-reading r64–r67); page == scan − 24 (211–216) / DUP 217 == 192 / − 25 (218–219); ALL Griblje entries: 20 entries / 20 houses — NARE 20/20 (after the P104 break h34×2 again without intra-year repeats); 0 NEW houses (the 6th year with 0: 0/1/0/0/0/0); the PT 15/5 (42+44+46+49+60 in the gap 41–60 — repeats; only h51 remains); the cumulative 420 entries / 85 houses across three books and 25 years (1886–1910; 449 vitals); ANCHORS: r3 h5 the 5th ENTRY (Štrucelj × Meh the 5th time 1891–1910; personal ID 0801910505931; the name »?exa« illegible — the P104 lead »Jožefa« a WRONG guess; † Nov 19, 1983); r7 h88 the 2nd ENTRY (a torn edge of p. 187); r10 h29 the 4th ENTRY — a 15-YEAR GAP + ILLEGITIMATE (the father EMPTY, the mother Barbara Milek alone = the h29 Milek family!); r18 h18 the 4th ENTRY — the Šimec × Kambič COUPLE RETURNS (the 1906 couple; a 1907 Brinec interlude; THE ENTRY TRANSFERRED Jun 23, 2003; personal ID 0703910505638); r22 h44 the 5th ENTRY (Jožef Štrucelj the 3rd in a row 1906/08/10; personal ID 0403910500260 — a birth-date correction to the 4th); r26 h34 the 8th ENTRY — the THIRD consecutive year (the 1909 twins → 1910 → the 1911 lead; the father Nikolaj Šulak? under tape [the first reading »Vidak«]; the SAME godfather Nikolaj Segina the 3rd time!; † Oct 30, 1963 in Griblje no. 73); r32 h60 the 9th ENTRY (Nikolaj Željko — the reading »Kolehko«; THE ENTRY TRANSFERRED May 23, 2001); r33 h90 the 6th ENTRY — THE TEACHER HOUSE (Kopitar 1890/92 → Vetročnik 1898/1900 → Kalan 1908/1910 Vincencij — the 4th teacher family; † Oct 19, 1910); r39 h21 the 7th ENTRY (the father »…mir« Požek = perhaps KAZIMIR — the h21 1888 illegitimate »Kaxmarp« RETURNS!; the mother change Ana Šimec → Katarina Kure); r42 h35 the 7th ENTRY (forensics 35 not 85; the midwife EMPTY; the mother change Ana → Barbara Križan/Hrižan?; † Jun 26); r47 h22 the 5th ENTRY (Nikolaj Milek the SAME 5×; personal ID 2506910505074; the godfather Ivan Požek; forensics 22 not 23); r48 h91 the 6th ENTRY — a FATHER CHANGE Janez→Matija Muc (the mother Ana Kure the SAME 6×!; the godfather Jurij Jakofčič = the h6 father CROSS-ROW; † Sep 18); r54 h46 the 7th ENTRY (forensics 46 — the first readings 6/14/16 WRONG; genetics Anton Brodarič × Katarina Milek = the 1908 SAME; personal ID 180791055019 [~]); r66 h65 the 10th ENTRY (Matija Milek the 10th time — the MILEK continuity 1887–1910!; forensics 65 on both dups; the registrar's CORRECTION »no. 45« WRONG; personal ID 2809910500547 — a birth-date correction to the 28th); r67 h49 the 5th ENTRY (Nikolaj Brodarič; the godfather Jakop Bohte = the r10 godfather 2nd×; THE ENTRY TRANSFERRED May 5, 1957); r72 h28 the 2nd ENTRY — a 19-YEAR GAP (1891→1910 — TIED with the h77 1909 record!) + ILLEGITIMATE (the mother Marjeta Sodek? alone; the godmother Marija Kalan the teacher's wife = a CROSS-ROW h90 r33!); r78 h6 the 5th ENTRY (Jakobič the 4th time; the godmother Marija Klepec the 3rd time; † Nov 19 THE SAME DAY!); r79 h42 the 5th ENTRY — the GENETIC SOLUTION of the forensics (»16« WRONG — h16 = Novak r84 an impossible collision; Pezdirec × Jurajevič the 2nd year); r83 h1 the 8th ENTRY — a FATHER CHANGE Željko→Janez Trome (7 entries ended; Željko simultaneously at h60!; the mother + the midwife MEH ×2; the signature a clear P »Paulin Bitnar« = PROOF of the SAME hand; married Feb 17, 1936 → † Mar 14, 1936 A MONTH AFTER THE WEDDING!); r84 h16 the 9th ENTRY (Alojzij Novak × Marija Frlah? = the h60 1904 couple — the Novak carousel h60↔h16; the godmother EMPTY; † Dec 11 THE SAME DAY — the last row!); PRIESTS/SIGNATURES NOVEL: »Laulin/Paulin Bitnar« 13 (the SAME HAND as the P104 registrar »Paulin Bitenc« — a dilemma: a NEW CURATE OR the registrar in the celebrant column; r83 a clear P = the same person writes P/L variants!) + »Jos. Rauq« 7 (continuing from 1909 Aug–Oct); a block-wise alternation (January only Bitnar r1–r6); MIDWIFE: 20/20 whatSi — MARIJA MEH 15/20 THE DOMINANT OF 1910 (the highest so far!) + Ana Meh 1 (r83 the mother + the midwife MEH ×2!) + Marjeta Toter 1 + Ana Mavrenič 1 (h90) + Barbara Adlešič 1 (h65) + 1 empty (r42); the personal-ID campaign: 5 anchors — ALL CONSISTENT (2 birth-date corrections from the IDs: r22 the birth 4th, r66 the birth 28th); ANOMALIES: 2 ILLEGITIMATE (r10 + r72); 2 EMPTY godparents (r42 the midwife + r84 the godmother); 5 INFANTS † (r33/r42/r48/r78/r84 — 2× THE SAME DAY as the baptism: r78 + r84 the last row!); the FATHER CHANGE h1 + h91; the MOTHER CHANGE h21 + h35; genetic forensics corrections (h42 »16« / h65 »45« / h34 »Vidak« / h60 »Kolehko« / h46 6/14/16 / h22 23 / h35 85); THE ENTRY TRANSFERRED ×3 (r18/r32/r67); A MONTH AFTER THE WEDDING (r83); the h28 + h29 gaps of 19/15 years; the Klepec godmother 3× (r32/r78/r83); EXCLUDED: 61 (r1 Cerkvišče 2 the lead, r43 G?i?ice 3 illegible under film, r64 »opatovina?« 30 — not Griblje + the 1953 registrar sticker on the dup); the script scripts/p105_parish_baptism_1910.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1910",
  p105Errors.length === 0,
  p105Errors.length === 0
    ? `20 vpisov / 20 hiš — NARE 20/20 · okvir 1910 skeni 211–219 (glava INLINE str. 187; 84 vrstic) – row 84 (glava 1911 INLINE = P106 lead: 1911 r1 Begunja vas 14 Anton; prva Griblje r3 = h34 Antonia TRETJE leto) · NOVELA: EN dup par (216/217 = str. 192) · stran == sken − 24 / DUP / − 25 · 0 NOVIH hiš (0/1/0/0/0/0 — 6. leto) · PT 15/5 · h5 ŠTRUCELJ × MEH 5. skupaj (ime »?exa« neberljivo) · h29 NEZAKONSKI (Milek familija; vrzel 15) · h18 POVRAT Šimec × Kambič · h44 Štrucelj 3.× zapored · h34 TRETJE leto + Segina 3. · h60 ŽELJKO 9. VPIS (»Kolehko«) · h90 KALAN 4. učiteljska · h21 KAZIMIR? POVRET (»…mir«) · h35 babica PRAZNA · h91 OČE MENJAVA Janez→Matija Muc · h65 MILEK 10. VPIS (popravek »45« NAPAČEN!) · h49 Brodarič + Bohte 2.× · h28 VRZEL 19 LET + NEZAKONSKA + Kalan CROSS-ROW · h6 Klepec 3.× + † isti dan · h42 GENETSKA REŠITEV (»16« → 42!) · h1 OČE MENJAVA Željko→TROME + MEH ×2 + MESEC PO POROKI · h16 NOVAK karusela h60↔h16 + botra PRAZNA + † isti dan · Bitnar 13 + Rauq 7 (ISTA ROKA dilema!) · babica MEH 15/20 DOMINANTA · EMŠO 5 sidr VSI SKLADNI · 5 † (2× isti dan) · EXCLUDED 61 · vitals 467 · kumulativ 420/85 25 let`
    : p105Errors.join("; "),
);

// ——— qa-p106: župnija Podzemelj — krstna 1911 (P106; issue #18) ———
const p106PageOfScan = (s: number) =>
  s === 219 ? 194 : s === 220 ? 195 : s === 221 ? 196 : s === 222 ? 197 : s === 223 ? 198 : s === 224 ? 199 : s === 225 || s === 226 ? 200 : s === 227 || s === 228 ? 201 : s === 229 ? 202 : s - 27;
const p106Hv = HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year === 1911);
const p106Errors: string[] = [];
if (p106Hv.length !== 17)
  p106Errors.push(`vpisov 1911 (04105, zasidrani) ≠ 17 (${p106Hv.length})`);
const p106Houses = new Set(p106Hv.map((h) => h.houseNo));
if (p106Houses.size !== 17)
  p106Errors.push(`različnih hiš ≠ 17 (NARE 17/17) (${p106Houses.size}: ${[...p106Houses].sort((a, b) => Number(a) - Number(b)).join(",")})`);
// NARE 17/17 — brez intra-letnih ponovitev (6. čisto leto)
const p106RepeatHouses = [...p106Hv.map((h) => h.houseNo)].filter((hn, i, arr) => arr.indexOf(hn) !== i);
if (p106RepeatHouses.length !== 0)
  p106Errors.push(`intra-letne ponovitve 1911 ≠ [] (NARE 17/17) — najdeno: ${p106RepeatHouses.join(",")}`);
// okvir: stran == sken po P106 noveli (DVA dup para 225/226 + 227/228)
const p106BadPage = p106Hv.filter(
  (h) => h.status !== "DOCUMENTED" || !h.scan || !h.page
    || h.page !== p106PageOfScan(h.scan)
    || h.scan < 219 || h.scan > 228,
);
if (p106BadPage.length > 0)
  p106Errors.push(`scan/page ne ustreza P106 noveli (dup 225/226 + 227/228): ${p106BadPage.map((h) => `${h.houseNo}@${h.scan}`).join(",")}`);
// 0 novih hiš (vzorec 1905–1911: 0/1/0/0/0/0/0)
const p106PriorHouses = new Set(
  HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year !== 1911).map((h) => h.houseNo),
);
const p106New = [...p106Houses].filter((hn) => !p106PriorHouses.has(hn));
if (p106New.length !== 0)
  p106Errors.push(`nove hiše 1911 ≠ [] (${p106New.join(",") || "brez"})`);
// sidra: h24 15. VPIS (P105 lead NAPAČEN) + h36 HRIŽAN + h13 MENJAVA KAMBIČ
// + h33/h3 GENETSKI »Grišice« + h47/h55 VRZEL 21 REKORD + h72 ISTA ZVEZA
// + h21 MENJAVA OČETA ISTA MATI + h74 VRZEL 18 + h49 ZAPORED Brodarič
// + h6 ZAPORED 3. leto + h30 SEGINA POVRAT (1906 REŠENA) + h40 VRZEL 12
// + h31 VRZEL 11 + PAPIČ kolizija + h14 babica PRAZNA
const p106Pins: Array<[string, string]> = [
  ["24", "15. VPIS"], ["24", "NAPAČEN"], ["24", "Adlešič"],
  ["36", "Hrižan"], ["36", "9. VPIS"], ["36", "DATUMSKI POPRAVEK"],
  ["13", "Jakofič"], ["13", "MENJAVA"], ["13", "Kambič"],
  ["33", "GENETSKA REŠITEV"], ["33", "Papič"],
  ["14", "PRAZNA"], ["14", "CROSS-ROW"],
  ["47", "21 LET"], ["47", "Požek"], ["47", "CROSS-ROW"],
  ["72", "Strauš"], ["72", "ISTA ZVEZA"],
  ["55", "21 LET"], ["55", "Kralj"], ["55", "IZENAČEN"],
  ["3", "GENETSKA REŠITEV"], ["3", "Papič"], ["3", "BABICA = MATI"],
  ["21", "Trček"], ["21", "ISTA"], ["21", "CROSS-ROW"],
  ["74", "18 LET"], ["74", "Kambič"], ["74", "Milek"],
  ["49", "Brodarič"], ["49", "ZAPORED"],
  ["6", "ZAPORED"], ["6", "Jakobič"], ["6", "Klepec"],
  ["30", "Segina"], ["30", "REŠENA"], ["30", "Brinec"],
  ["40", "12 LET"], ["40", "Hrižan"],
  ["31", "11 LET"], ["31", "Papič"], ["31", "Hrižan"],
];
for (const [hn, pin] of p106Pins) {
  const cur = p106Hv.find((h) => h.houseNo === hn);
  if (!cur) {
    p106Errors.push(`pin ${hn} (${pin}) — hiša ${hn} ni v 1911 blokih`);
    continue;
  }
  if (!cur.whatSi.includes(pin))
    p106Errors.push(`pin hiša ${hn} (${pin}) manjka`);
}
// vitals skupaj 449 (po P107: 429 + 20; krstna 1912)
if (HOUSE_VITALS.length !== 685)
  p106Errors.push(`HOUSE_VITALS ≠ 467 (${HOUSE_VITALS.length})`);
// babica: 16/17 whatSi; Meh 12 (11× Marija + 1× Marjeta r68 — DOMINANTA 1911)
// + babica = mati ISTA (r67 Katarina Novak)
if (p106Hv.filter((h) => h.whatSi.includes("babica")).length !== 17)
  p106Errors.push(`babica ni v vseh 17 whatSi (${p106Hv.filter((h) => h.whatSi.includes("babica")).length})`);
const p106Meh = p106Hv.filter((h) => h.whatSi.includes("babica Marija Meh")).length;
if (p106Meh !== 11)
  p106Errors.push(`babica Marija Meh ≠ 11× (${p106Meh} — DOMINANTA 1911; r68 Marjeta Meh = 12. z dokazom; r41 prazna; r67 babica = mati Novak)`);
if (!p106Hv.some((h) => h.houseNo === "3" && h.whatSi.includes("BABICA = MATI")))
  p106Errors.push("r67 BABICA = MATI ISTA OSEBA (Katarina Novak; cf. P103 r16) manjka");
if (!p106Hv.some((h) => h.houseNo === "14" && h.whatSi.includes("babica PRAZNA")))
  p106Errors.push("r41 babica PRAZNA (edina v 1911) manjka");
// podpisi (bloki): Bitnar 13 + Rauq 4 (nadaljevanje blokovske P105)
if (p106Hv.filter((h) => h.whatSi.includes("Bitnar")).length !== 13)
  p106Errors.push(`podpis Bitnar ≠ 13× (${p106Hv.filter((h) => h.whatSi.includes("Bitnar")).length})`);
if (p106Hv.filter((h) => h.whatSi.includes("podpis Jos. Rauq")).length !== 4)
  p106Errors.push(`podpis Jos. Rauq ≠ 4× (${p106Hv.filter((h) => h.whatSi.includes("podpis Jos. Rauq")).length})`);
// EMŠO sidra v blokih: 5 (r33/r36/r55/r69/r82 — 2 SKLADNA + 2 popravek + 1 [~])
const p106Emso = p106Hv.filter((h) => /sidro/i.test(h.whatSi) || h.whatSi.includes("DATUMSKI POPRAVEK"));
if (p106Emso.length !== 5)
  p106Errors.push(`EMŠO sidrov v blokih ≠ 5 (${p106Emso.length})`);
for (const emso of ["1704911305004", "0405911500574", "0308911500935", "1310911500879", "2311911505307"]) {
  if (!p106Hv.some((h) => h.whatSi.includes(emso)))
    p106Errors.push(`EMŠO sidro ${emso} manjka`);
}
// genetske rešitve vasi: r37 h33 + r67 h3 (»Grišice«) + r38 EXCLUDED neodločen
if (!p106Hv.some((h) => h.houseNo === "33" && h.whatSi.includes("Grišice")))
  p106Errors.push("r37 »Grišice« genetska rešitev (h33) manjka");
if (!p106Hv.some((h) => h.houseNo === "3" && h.whatSi.includes("Grišice")))
  p106Errors.push("r67 »Grišice« genetska rešitev (h3) manjka");
push(
  "qa-p106-parish-baptism-1911",
  "P106: ŽUPNIJA PODZEMELJ — KRSTNA KNJIGA 04105, POLNO LETO 1911 (issue #18; SAMPLE-TRANSCRIPTION-1911; MERI, NE odloča; v7 join nespremenjen): širitev vzorca P79 (1886) → … → P103 (1908) → P104 (1909) → P105 (1910) na leto 1911 — okvir: glava »1911 / Januarij« INLINE na str. 194 = sken 219 (pod 1910 r84; 1911 r1 = Begunja vas 14 Anton 8./9. Januar, EMŠO 0801911500623 — P105 lead POTRJEN) – row 89 na str. 201 (skena 227/228 DUP; glava »1912« INLINE na str. 202 = sken 229; 1912 r1 = Griblje 70 Alojzij — P107 lead) == tiskane strani 194–201 (89 vrstic — 2. največ po 1908 = 90; 1909 = 81, 1910 = 84); NOVELA P106: DVA dup para — 225/226 = str. 200 + 227/228 = str. 201 (največ od P104: P102 ×2, P103 ×3, P104 ×5, P105 ×1); stran == sken − 25 (219–224) / DUP 225+226 == 200 / DUP 227+228 == 201 / − 27 (229+); VSI vpisi z Griblji: 17 vpisov / 17 hiš — NARE 17/17 (6. čisto leto; na vasi raven: Vranoviče 10 ×2 — r11 + r81 DVE DRUŽINI!); 0 NOVIH hiš (7. leto z 0: 0/1/0/0/0/0/0); PT 13/4 (47+48+49+55 v luknji 41–60 — ponovitve; luknja ostaja samo h51); kumulativ 437 vpisov / 85 hiš čez tri knjige in 26 let (1886–1911; 449 vitals); GENETSKE REŠITVE VAS: r37 »Grišice« → GRIBLJE 33 (Martin Papič = 1909 ISTI oče + botri ISTI PRIIMEK + hiša 33!) + r67 »Grišice« → GRIBLJE 3 (hiša 3 = h3 Papič hiša; oče Matija Papič) — PAPIČ 2 hiši v 1911! (cf. P102 »Grišlje«) + r38 »Grišice« 35 = h30 1909 družina (Martinkovič × Šimec) — selitev/druga vas NEODLOČENO (EXCLUDED); P105 lead »h34 TRETJE leto« NAPAČEN → r3 = h24 (6× forenzika; Janez Brinec = h24 Brinčeva SKLADNO — 2. zapored napačen lead!); SIDRA: r3 h24 15. VPIS (najbolj vpisovana; babica Barbara Adlešič ISTA kot 1910 h65); r32 h48 5. VPIS (dojenček † 16/7); r33 h36 9. VPIS (oče Janez Hrižan = KRIŽAN hiša SKLADNO; botrinja Marjeta Štraus?; EMŠO 1704911305004 — DATUMSKI POPRAVEK 17.4 vs register 14.4.! — 3. popravek vzorca); r36 h13 5. VPIS (MENJAVA #2 Šimec×Kambič → Jakofič; botri KAMBIČ PAR = povezava s prejšnjo familijo!; EMŠO 0405911500574 SKLADNO); r41 h14 5. VPIS (babica PRAZNA edina; botrinja Bara Adlešič = r3 babica ISTA CROSS-ROW!; oče Brinec? + mati Pezdirec? signali); r49 h47 3. VPIS — **VRZEL 21 LET NOV REKORD** (prej 19!; oče Janez Požek bajtar = h77 familija — brata?; botrinja Ana Milek = r3 mati ISTA OSEBA CROSS-ROW!); r53 h72 7. VPIS (ISTA ZVEZA Strauš × Šimec kot 1909 — ŠTRAUS kontinuiteta!); r55 h55 3. VPIS — **VRZEL 21 LET REKORD IZENAČEN (DVA 21-letna rekorda isto leto!)** (KRALJ familija NOVA v vzorcu; vas Griblje pod anotacijo jasna — P104 lead POPRAVLJEN; EMŠO 0308911500935 SKLADNO); r67 h3 4. VPIS (babica Katarina Novak = MATI ISTA OSEBA! cf. P103 r16; dojenček † 25/4.1919); r68 h21 8. VPIS — ZAPORED (MENJAVA OČETA Z ISTO MATI: 1910 »…mir« Požek × Katarina Kure → 1911 Janez Trček × ISTA Kure! — 2. primer cf. h1 1910; boter Janez Brinec? = h24 oče CROSS-ROW!); r69 h74 2. VPIS — VRZEL 18 LET (oče Kambič; mati Marija Milek = MILEK kontinuiteta; botrinja Katarina Požek = POŽEK signal; EMŠO 1310911500879 SKLADNO; VPIS PRENEŠEN 25.5.1999?); r73 h49 6. VPIS — ZAPORED (Brodarič kontinuiteta 1910 Nikolaj → 1911 Anton; botrinja Marjana Bohte = Bohte signal; dojenček † 27/5.1913); r74 h6 6. VPIS — **ZAPORED 3. leto!** (1909/10/11; Jakobič SKLADNO — oče Jurij? [1. branje Janez]; boter Jožef Željko = ŽELJKO signal; botrinja Marija Klepec = KLEPEC 4.× v 2 letih!); r80 h30 13. VPIS — **SEGINA POVRAT: 1906 MENJAVA REŠENA** (oče Nikolaj Segina × mati Katarina Brinec = kombinacija obeh familij!; VPIS PRENEŠEN 25.11.2007); r82 h40 4. VPIS — VRZEL 12 LET (botri HRIŽAN PAR; oče Podravec?; EMŠO 2311911505307 — dan 23 vs register 22 [~]; dojenček † 7/10.1914); r84 h31 10. VPIS — VRZEL 11 LET (oče Gapič?/Papič? kolizija — 3. Papič hiša?; mati Katarina Hrižan + botrinja Barbara Hrižan = HRIŽAN kampanja; VPIS PRENEŠEN 19.11.2007); DUHOVNIKI/PODPISI: »Paulin/Laulin Bitnar« 13 + »Jos. Rauq« 4 (nadaljevanje blokovske P105); BABICA: 16/17 imenovanih — MARIJA MEH 11/17 DOMINANTA 1911 (+ Marjeta Meh 1 r68 = 12) + Barbara Adlešič 1 (r3 ISTA kot 1910!) + Ana Mavrenič 1 (r37) + Marija Pletić? 1 (r32 [~]) + Katarina Novak 1 (r67 — BABICA = MATI ISTA!) + 1 prazna (r41); EMŠO kampanja: 5 sidr (2 SKLADNA + 2 datumski popravki r33/r82 + 1 [~] r74); ANOMALIJE: **VRZELI 21+21+18+12+11 LET — REKORDNO LETO** (h47 NOV rekord 21!); HRIŽAN kampanja 5 signalov (r33/r80/r82/r84×2); MILEK kontinuiteta 5 signalov (r3 mati + r49 botrinja ISTA Ana Milek CROSS-ROW! + r69/r73 mati + r80 botrinja); babica = mati ISTA (r67); oče menjava z ISTO mati (r68); 6 dojenčkov/otrok † (r32/r37/r53/r67/r73/r82); PAPIČ kolizija (r84); VPIS PRENEŠEN ×3 (r69?/r80/r84); dvojčki ×2 (r22/r23 Dobraviče 16 + r88/r89 Gradac 1 — non-Griblje); razveljavitev zakona (r77 Primorček); nujni krst signal (r46 Otok 23: botra + podpis PRAZNA — 2. v vzorcu po 1908 h85!); Vranoviče 10 ×2 (dve družini); EXCLUDED: 72 (r1 Begunja vas 14 lead, r38 »Grišice« 35 neodločeno, r66 Klanšek?/Planšek? delno, r30 vas pod anotacijo); skripta scripts/p106_parish_baptism_1911.py (I1–I12, --check 14/14 PASS); status SAMPLE-TRANSCRIPTION-1911",
  "P106: PARISH OF PODZEMELJ — BAPTISM REGISTER 04105, THE FULL YEAR 1911 (issue #18; SAMPLE-TRANSCRIPTION-1911; MEASURES, does not decide; the v7 join unchanged): extending the sample P79 (1886) → … → P104 (1909) → P105 (1910) to 1911 — the frame: the heading »1911 / Januarij« INLINE on p. 194 = scan 219 (below the 1910 r84; the 1911 r1 = Begunja vas 14 Anton Jan 8/9, personal ID 0801911500623 — the P105 lead CONFIRMED) – row 89 on p. 201 (scans 227/228 DUP; the heading »1912« INLINE on p. 202 = scan 229; the 1912 r1 = Griblje 70 Alojzij — the P107 lead) == printed pages 194–201 (89 rows — the 2nd most after 1908 = 90; 1909 = 81, 1910 = 84); THE P106 NOVEL: TWO dup pairs — 225/226 = p. 200 + 227/228 = p. 201 (the most since P104); page == scan − 25 (219–224) / DUP 225+226 == 200 / DUP 227+228 == 201 / − 27 (229+); ALL Griblje entries: 17 entries / 17 houses — NARE 17/17 (the 6th clean year; at the village level: Vranoviče 10 ×2 — r11 + r81 TWO FAMILIES!); 0 NEW houses (the 7th year with 0); the PT 13/4 (47+48+49+55 in the gap 41–60); the cumulative 437 entries / 85 houses across three books and 26 years (1886–1911; 449 vitals); GENETIC SOLUTIONS OF VILLAGES: r37 »Grišice« → GRIBLJE 33 (Martin Papič = the 1909 SAME father + the godparents the SAME SURNAME + house 33!) + r67 »Grišice« → GRIBLJE 3 (house 3 = the h3 Papič house; the father Matija Papič) — TWO Papič houses in 1911! (cf. P102 »Grišlje«) + r38 »Grišice« 35 = the h30 1909 family (Martinkovič × Šimec) — a move/another village UNDECIDED (EXCLUDED); the P105 lead »h34 the THIRD year« WRONG → r3 = h24 (6× forensics; Janez Brinec = the h24 Brinec family CONSISTENT — the 2nd consecutive wrong lead!); ANCHORS: r3 h24 the 15th ENTRY (the most-entered house; the midwife Barbara Adlešič the SAME as 1910 h65); r32 h48 the 5th ENTRY (an infant died Jul 16); r33 h36 the 9th ENTRY (the father Janez Hrižan = the KRIŽAN house CONSISTENT; the godmother Marjeta Štraus?; personal ID 1704911305004 — a BIRTH-DATE CORRECTION Apr 17 vs the register Apr 14! — the 3rd correction of the sample); r36 h13 the 5th ENTRY (the FAMILY CHANGE #2 Šimec×Kambič → Jakofič; the godparents the KAMBIČ COUPLE = a link to the previous family!; personal ID 0405911500574 CONSISTENT); r41 h14 the 5th ENTRY (the midwife EMPTY the only one; the godmother Bara Adlešič = the r3 midwife the SAME PERSON a CROSS-ROW!); r49 h47 the 3rd ENTRY — **a 21-YEAR GAP a NEW RECORD** (the previous 19!; the father Janez Požek the cottager = the h77 family — brothers?; the godmother Ana Milek = the r3 mother the SAME PERSON a CROSS-ROW!); r53 h72 the 7th ENTRY (the SAME COUPLE Strauš × Šimec as 1909); r55 h55 the 3rd ENTRY — **a 21-YEAR GAP TIED (TWO 21-year records in the same year!)** (the KRALJ family NEW to the sample; personal ID 0308911500935 CONSISTENT); r67 h3 the 4th ENTRY (the midwife Katarina Novak = THE MOTHER THE SAME PERSON! cf. P103 r16); r68 h21 the 8th ENTRY — CONSECUTIVE (A FATHER CHANGE WITH THE SAME MOTHER: 1910 »…mir« Požek × Katarina Kure → 1911 Janez Trček × the SAME Kure! — the 2nd case cf. h1 1910; the godfather Janez Brinec? = the h24 father a CROSS-ROW!); r69 h74 the 2nd ENTRY — an 18-YEAR GAP (the father Kambič; the mother Marija Milek = the MILEK continuity; personal ID 1310911500879 CONSISTENT; THE ENTRY TRANSFERRED); r73 h49 the 6th ENTRY — CONSECUTIVE (the Brodarič continuity 1910 Nikolaj → 1911 Anton; the godmother Marjana Bohte = the Bohte signal); r74 h6 the 6th ENTRY — **CONSECUTIVE the 3rd YEAR!** (1909/10/11; the Jakobič CONSISTENT; the godmother Marija Klepec = KLEPEC the 4th time in 2 years!); r80 h30 the 13th ENTRY — **THE SEGINA RETURN: the 1906 FAMILY CHANGE SOLVED** (the father Nikolaj Segina × the mother Katarina Brinec = a combination of both families!; THE ENTRY TRANSFERRED Nov 25, 2007); r82 h40 the 4th ENTRY — a 12-YEAR GAP (the godparents the HRIŽAN COUPLE; personal ID 2311911505307 — day 23 vs the register 22 [~]); r84 h31 the 10th ENTRY — an 11-YEAR GAP (the father Gapič?/Papič? a collision — a 3rd Papič house?; the mother Katarina Hrižan + the godmother Barbara Hrižan = the HRIŽAN campaign; THE ENTRY TRANSFERRED Nov 19, 2007); PRIESTS/SIGNATURES: »Paulin/Laulin Bitnar« 13 + »Jos. Rauq« 4 (continuing the P105 blocks); MIDWIFE: 16/17 named — MARIJA MEH 11/17 THE DOMINANT OF 1911 (+ Marjeta Meh 1 r68 = 12) + Barbara Adlešič 1 (r3 the SAME as 1910!) + Ana Mavrenič 1 (r37) + Marija Pletić? 1 (r32 [~]) + Katarina Novak 1 (r67 — THE MIDWIFE = THE MOTHER!) + 1 empty (r41); the personal-ID campaign: 5 anchors (2 CONSISTENT + 2 birth-date corrections r33/r82 + 1 [~] r74); ANOMALIES: **GAPS of 21+21+18+12+11 YEARS — a RECORD YEAR** (h47 a NEW record 21!); the HRIŽAN campaign 5 signals; the MILEK continuity 5 signals (the r49 godmother Ana Milek = the r3 mother the SAME PERSON a CROSS-ROW!); the midwife = the mother (r67); a father change with the SAME mother (r68); 6 infants/children †; the Papič collision (r84); THE ENTRY TRANSFERRED ×3; twins ×2 (r22/r23 + r88/r89 — non-Griblje); a marriage annulment (r77); an emergency-baptism signal (r46 Otok 23: the godmother + the signature EMPTY — the 2nd in the sample after 1908 h85!); Vranoviče 10 ×2 (two families); EXCLUDED: 72 (r1 Begunja vas 14 the lead, r38 »Grišice« 35 undecided, r66 Klanšek?/Planšek? partial, r30 the village under an annotation); the script scripts/p106_parish_baptism_1911.py (I1–I12, --check 14/14 PASS); status SAMPLE-TRANSCRIPTION-1911",
  p106Errors.length === 0,
  p106Errors.length === 0
    ? `17 vpisov / 17 hiš — NARE 17/17 (6. čisto leto) · okvir 1911 skeni 219–228 (glava INLINE str. 194; 89 vrstic — 2. največ) – row 89 + glava 1912 INLINE str. 202 (P107 lead: 1912 r1 Griblje 70 Alojzij) · NOVELA: DVA dup para (225/226 + 227/228) · stran == sken − 25 / DUP ×2 / − 27 · 0 NOVIH hiš (7. leto) · PT 13/4 · GENETSKE VASI: »Grišice« → h33 + h3 (PAPIČ 2 hiši!) + r38 neodločeno · P105 lead h34 NAPAČEN → h24 15. VPIS (Brinčeva!) · h47+h55 VRZEL 21 LET NOV REKORD (2× isto leto!) · h74 18 + h40 12 + h31 11 LET (rekordno leto!) · h36 HRIŽAN + EMŠO popravek 17.4 · h13 MENJAVA → Jakofič + KAMBIČ botri · h72 ISTA ZVEZA Strauš × Šimec · h3 BABICA = MATI ISTA (Novak!) · h21 MENJAVA OČETA ISTA MATI (Požek → Trček!) · h74 VRZEL 18 + Kambič × Milek · h49 ZAPORED Brodarič · h6 ZAPORED 3. leto + Klepec 4.× · h30 SEGINA POVRAT (1906 menjava REŠENA: Segina × Brinec!) · h40 HRIŽAN PAR + 12 LET · h31 PAPIČ kolizija + 11 LET · Bitnar 13 + Rauq 4 · babica MEH 12/17 DOMINANTA · EMŠO 5 sidr (2 popravka!) · 6 † · HRIŽAN kampanja 5 · MILEK 5 (Ana Milek CROSS-ROW!) · VPIS PRENEŠEN ×3 · EXCLUDED 72 · vitals 467 · kumulativ 437/85 26 let`
    : p106Errors.join("; "),
);

// ——— qa-p107: župnija Podzemelj — krstna 1912 (P107; issue #18) ———
const p107PageOfScan = (s: number) =>
  s === 229 ? 202 : s === 230 ? 203 : s === 231 || s === 232 ? 204 : s === 233 ? 205 : s === 234 ? 206 : s === 235 || s === 236 ? 207 : s === 237 || s === 238 ? 208 : s === 239 || s === 240 ? 209 : s - 30;
const p107Hv = HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year === 1912);
const p107Errors: string[] = [];
if (p107Hv.length !== 20)
  p107Errors.push(`vpisov 1912 (04105, zasidrani) ≠ 20 (${p107Hv.length})`);
const p107Houses = new Set(p107Hv.map((h) => h.houseNo));
if (p107Houses.size !== 20)
  p107Errors.push(`različnih hiš ≠ 20 (NARE 20/20) (${p107Houses.size}: ${[...p107Houses].sort((a, b) => Number(a) - Number(b)).join(",")})`);
// NARE 20/20 — brez intra-letnih ponovitev (8. čisto leto)
const p107RepeatHouses = [...p107Hv.map((h) => h.houseNo)].filter((hn, i, arr) => arr.indexOf(hn) !== i);
if (p107RepeatHouses.length !== 0)
  p107Errors.push(`intra-letne ponovitve 1912 ≠ [] (NARE 20/20) — najdeno: ${p107RepeatHouses.join(",")}`);
// okvir: stran == sken po P107 noveli (ŠTIRI dup pari 231/232 + 235/236 + 237/238 + 239/240)
const p107BadPage = p107Hv.filter(
  (h) => h.status !== "DOCUMENTED" || !h.scan || !h.page
    || h.page !== p107PageOfScan(h.scan)
    || h.scan < 229 || h.scan > 239,
);
if (p107BadPage.length > 0)
  p107Errors.push(`scan/page ne ustreza P107 noveli (dup ×4): ${p107BadPage.map((h) => `${h.houseNo}@${h.scan}`).join(",")}`);
// 1 NOVA hiša (h86 — prva po 1909: 0/1/0/0/0/0/0/0/1)
const p107PriorHouses = new Set(
  HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year < 1912).map((h) => h.houseNo), // P108: year !== 1912 → year < 1912 (1913 bloki h86 2. VPIS)
);
const p107New = [...p107Houses].filter((hn) => !p107PriorHouses.has(hn));
if (p107New.length !== 1 || p107New[0] !== "86")
  p107Errors.push(`nove hiše 1912 ≠ ["86"] (${p107New.join(",") || "brez"})`);
// sidra: h70 SELIJA + VRZEL 19 + h8 VRZEL 23 REKORD + h22 MLINAR + h24 16. VPIS
// + h33 GENETSKA ×2 + h86 NOVA HIŠA + h5 MEH ×2 + h90 Kalan RAZVEZAL
// + h45/h46 DVOJČKI + h12 TRIPOLI + h18 ANOMALIJA
const p107Pins: Array<[string, string]> = [
  ["70", "2. VPIS"], ["70", "SELIJA"], ["70", "19 LET"], ["70", "Brinec"], ["70", "Segina"],
  ["59", "Jaklič"], ["59", "13 LET"],
  ["36", "8. VPIS"], ["36", "Hrižan"], ["36", "Štraus"],
  ["11", "4. VPIS"], ["11", "92 LET"],
  ["45", "DVOJČKI"], ["45", "Filar"],
  ["46", "DVOJČKI"], ["46", "8. VPIS"],
  ["8", "23 LET"], ["8", "NOV REKORD"], ["8", "Jakofčič"],
  ["26", "Meh"],
  ["90", "Kalan"], ["90", "RAZVEZAL"], ["90", "7. VPIS"],
  ["71", "18 LET"], ["71", "Hrižan"],
  ["12", "13. VPIS"], ["12", "TRIPOLI"], ["12", "Dragoš"],
  ["18", "ANOMALIJA"], ["18", "Tomec"],
  ["22", "MLINAR"], ["22", "Miko Alek"], ["22", "babica [PRAZNA]"],
  ["24", "16. VPIS"], ["24", "NOV REKORD HIŠE"],
  ["19", "SKLADNO"], ["19", "Hrižan"],
  ["48", "ZAPORED"], ["48", "SKLADNO"],
  ["33", "GENETSKA"], ["33", "Grišice"], ["33", "Papič"],
  ["86", "NOVA HIŠA"], ["86", "Brinec"], ["86", "Sprem"],
  ["40", "5. VPIS"], ["40", "Brodarič"],
  ["5", "MEH"], ["5", "Štrucelj"],
];
for (const [n, pin] of p107Pins) {
  const cur = p107Hv.find((h) => h.houseNo === n);
  if (!cur) {
    p107Errors.push(`pin ${n} (${pin}) — hiša ${n} ni v 1912 blokih`);
    continue;
  }
  if (!cur.whatSi.includes(pin))
    p107Errors.push(`pin hiša ${n} (${pin}) manjka`);
}
// vitals skupaj 449 (po P107: 429 + 20; krstna 1912)
if (HOUSE_VITALS.length !== 685)
  p107Errors.push(`HOUSE_VITALS ≠ 467 (${HOUSE_VITALS.length})`);
// babica: 19/20 whatSi; Meh 12 (vse Marija — DOMINANTA 1912) + MEH ×2 r87
if (p107Hv.filter((h) => h.whatSi.includes("babica")).length !== 20)
  p107Errors.push(`babica ni v vseh 20 whatSi (${p107Hv.filter((h) => h.whatSi.includes("babica")).length})`);
const p107Meh = p107Hv.filter((h) => h.whatSi.includes("babica Marija Meh")).length;
if (p107Meh !== 12)
  p107Errors.push(`babica Marija Meh ≠ 12× (${p107Meh} — DOMINANTA 1912; r87 mati+botrinja MEH ×2!)`);
if (!p107Hv.some((h) => h.houseNo === "22" && h.whatSi.includes("babica [PRAZNA]")))
  p107Errors.push("r42 babica [PRAZNA] (edina v 1912) manjka");
if (!p107Hv.some((h) => h.houseNo === "5" && h.whatSi.includes("MEH ×2")))
  p107Errors.push("r87 MATI + BOTRINJA = MEH ×2 manjka");
// podpisi (bloki): Bitnar 13 + Rauq 7
if (p107Hv.filter((h) => h.whatSi.includes("Bitnar")).length !== 13)
  p107Errors.push(`podpis Bitnar ≠ 13× (${p107Hv.filter((h) => h.whatSi.includes("Bitnar")).length})`);
if (p107Hv.filter((h) => h.whatSi.includes("podpis Jos. Rauq")).length !== 7)
  p107Errors.push(`podpis Jos. Rauq ≠ 7× (${p107Hv.filter((h) => h.whatSi.includes("podpis Jos. Rauq")).length})`);
// EMŠO sidra v blokih: 5 (r1/r42/r46/r53/r75 — 3 SKLADNA + 1 popravek [~] + 1 [~])
const p107Emso = p107Hv.filter((h) => /sidro/i.test(h.whatSi) || h.whatSi.includes("DATUMSKI POPRAVEK") || h.whatSi.includes("MOŽEN DATUMSKI POPRAVEK"));
if (p107Emso.length !== 5)
  p107Errors.push(`EMŠO sidrov v blokih ≠ 5 (${p107Emso.length})`);
for (const emso of ["0201912500174", "1106912505630", "2806912505946", "2807912505918", "2010912506419"]) {
  if (!p107Hv.some((h) => h.whatSi.includes(emso)))
    p107Errors.push(`EMŠO sidro ${emso} manjka`);
}
// genetska rešitev vasi: r70 h33 (»Grišice« 2.×)
if (!p107Hv.some((h) => h.houseNo === "33" && h.whatSi.includes("Grišice")))
  p107Errors.push("r70 »Grišice« genetska rešitev (h33 ×2) manjka");
// P108 lead: glava 1913 INLINE str. 209 dno + 1913 r1 Cerkvišče 31? Marija
if (!p107Hv.some((h) => h.houseNo === "5" && h.whatSi.includes("P108")))
  p107Errors.push("P108 lead v h5 bloku manjka");
push(
  "qa-p107-parish-baptism-1912",
  "P107: ŽUPNIJA PODZEMELJ — KRSTNA KNJIGA 04105, POLNO LETO 1912 (issue #18; SAMPLE-TRANSCRIPTION-1912; MERI, NE odloča; v7 join nespremenjen): širitev vzorca P79 (1886) → … → P104 (1909) → P105 (1910) → P106 (1911) na leto 1912 — okvir: glava »1912« INLINE na str. 202 = sken 229 (pod 1911 r89; 1912 r1 = Griblje 70 Alojzij 2./2. Januar, EMŠO 0201912500174 — P106 lead POTRJEN hiša+starši, lead EMŠO POPRAVLJEN 0101912500294 → 0201912500174!) – row 88 na str. 209 (sken 239/240 DUP; Gradac 1 Minka 31.12.1912/1.1.1913 krsta; **glava »1913« INLINE na str. 209 DNO = s239/s240 (pod r88!)** — 1913 r1 = Cerkvišče 31? Marija Januarij 4./10., EMŠO 0401913505350 — Januar 1913 IMA vpise na str. 209 dnu!) == tiskane strani 202–209 (88 vrstic; 1911 = 89, 1910 = 84); NOVELA P107: ŠTIRI dup pari — 231/232 = str. 204 + 235/236 = str. 207 + 237/238 = str. 208 + 239/240 = str. 209 (2. največ po P104 ×5); stran == sken − 27 (229–232) / − 28 (233–236) / − 29 (237–238) / − 30 (239–240); VSI vpisi z Griblji: 20 vpisov / 20 hiš — NARE 20/20 (8. čisto leto!); **1 NOVA hiša h86 (r75) — prva po 1909 (0/1/0/0/0/0/0/0/1 — prelom!)**; PT 16/4 (45+46+48+59 v luknji 41–60 — ponovitve; luknja ostaja samo h51); kumulativ 457 vpisov / 86 hiš čez tri knjige in 27 let (1886–1912; 449 vitals); SIDRA: r1 h70 2. VPIS — VRZEL 19 LET + **SELIJA h10→h70** (Matija Brinec × Marija Grabrijan = 1909 par! — 2. selitev vzorca cf. h30→h10); r8 h8 3. VPIS — **VRZEL 23 LET NOV REKORD** (prej 21); r42 h22 6. VPIS (oče **Miko Alek — MLINAR** — potrjen 1913 r2 Kranjak 15!); r45 h24 **16. VPIS NOV REKORD HIŠE** (prej 15; ZAPORED 2. leto); r70 h33 5. VPIS — **GENETSKA VAS ×2: »Grišice« → GRIBLJE 33** (cf. P106 r37; ISTI oče Martin Papič — 2. potrjena »Grišice«!); r75 h86 **NOVA HIŠA** (botra+babica = Brinec ×3!; poroka 1946 Koprivnica priimek Sprem); r87 h5 6. VPIS (**mati + botrinja = MEH ×2**; oče »je ženit«); r12 h90 7. VPIS (KALAN = učiteljska familija; **RAZVEZAL zakon 15.1.1953 Ljubljana**; beli trak † 14.4.2003); r23 h12 13. VPIS (**† 14.9.1987 TRUPOLI = TRIPOLI!**); r6/r7 h45+h46 DVOJČKI (Anton + Jožefa — ISTI starši/botra — v DVEH sosednjih hišah!); DUHOVNIKI/PODPISI: »Paulin Bitnar« 13 + »Jos. Rauq« 7 (nadaljevanje blokovske P105/P106; 13+7 = 20 = vsi vpisi); BABICA: 19/20 imenovanih — MARIJA MEH 12/20 DOMINANTA (vse Marija!) + Adlešič 2 + Barbara Brinec 1 (r75 očeva familija!) + Marija Jakofčič 1 + Marija Pletoj? 1 + 1 nejasna (r45); EMŠO kampanja: 5 sidr (3 SKLADNA + 1 MOŽEN popravek r42 mesec 06 vs 05 + 1 [~] r75); ANOMALIJE: **očetova kolona ŽENSKO ime (r32 h18 »Marija Tomec« — 1. primer vzorca!)** + (V?)mpohranca/-gina s prazno krsto (r9+r44) + **sub divo mrtvorojen (r47 Klojter — 1. v vzorci!)** + November glava skrita pod trakom (r79) + r36 skrita pod trakom + DVE IMENI (r63) + 2 razveljavitvi zakona (r12 1953 + r86 1956/57 Varaždin) + 6 dojenčkov/otrok † + dvojčki ×3 (r6/r7 Griblje! + r49/r50 + r85/r86 non-Griblje) + h85 DVA VPISA v 1912 (r51+r74 — non-Griblje) + nezakonska učiteljica (r88 Gradac 1; podpis spovednik Miklavž Belševič?); † TRIPOLI (r23); EXCLUDED: 69 (r36 pod trakom, r65 Marijana pod trakom, r79 November pod trakom, r72 fragment); skripta scripts/p107_parish_baptism_1912.py (I1–I12 + I3b/I9b, --check 15/15 PASS); status SAMPLE-TRANSCRIPTION-1912",
  "P107: PARISH OF PODZEMELJ — BAPTISM REGISTER 04105, THE FULL YEAR 1912 (issue #18; SAMPLE-TRANSCRIPTION-1912; MEASURES, does not decide; the v7 join unchanged): extending the sample P79 (1886) → … → P105 (1910) → P106 (1911) to 1912 — the frame: the heading »1912« INLINE on p. 202 = scan 229 (below the 1911 r89; the 1912 r1 = Griblje 70 Alojzij Jan 2/2, personal ID 0201912500174 — the P106 lead CONFIRMED for the house+parents, the lead ID CORRECTED 0101912500294 → 0201912500174!) – row 88 on p. 209 (scans 239/240 DUP; Gradac 1 Minka Dec 31, 1912/Jan 1, 1913 baptism; **the heading »1913« INLINE on p. 209 BOTTOM = s239/s240 (below r88!)** — the 1913 r1 = Cerkvišče 31? Marija Jan 4/10, personal ID 0401913505350 — January 1913 HAS entries at the bottom of p. 209!) == printed pages 202–209 (88 rows; 1911 = 89, 1910 = 84); THE P107 NOVEL: FOUR dup pairs — 231/232 = p. 204 + 235/236 = p. 207 + 237/238 = p. 208 + 239/240 = p. 209 (the 2nd most after P104 ×5); page == scan − 27 (229–232) / − 28 (233–236) / − 29 (237–238) / − 30 (239–240); ALL Griblje entries: 20 entries / 20 houses — NARE 20/20 (the 8th clean year!); **1 NEW house h86 (r75) — the first since 1909 (0/1/0/0/0/0/0/0/1 — a breaking year!)**; the PT 16/4 (45+46+48+59 in the gap 41–60 — repeats; the gap keeps only h51); the cumulative 457 entries / 86 houses across three books and 27 years (1886–1912; 449 vitals); ANCHORS: r1 h70 the 2nd ENTRY — a 19-YEAR GAP + **A MOVE h10→h70** (Matija Brinec × Marija Grabrijan = the 1909 couple! — the 2nd move of the sample cf. h30→h10); r8 h8 the 3rd ENTRY — **a 23-YEAR GAP a NEW RECORD** (the previous 21); r42 h22 the 6th ENTRY (the father **Miko Alek — A MILLER** — confirmed by 1913 r2 Kranjak 15!); r45 h24 **the 16th ENTRY a NEW HOUSE RECORD** (the previous 15; CONSECUTIVE the 2nd year); r70 h33 the 5th ENTRY — **THE GENETIC VILLAGE ×2: »Grišice« → GRIBLJE 33** (cf. P106 r37; the SAME father Martin Papič — the 2nd confirmed »Grišice«!); r75 h86 **A NEW HOUSE** (godparents+midwife = Brinec ×3!; the 1946 Koprivnica marriage surname Sprem); r87 h5 the 6th ENTRY (**the mother + the godmother = MEH ×2**; the father »je ženit«); r12 h90 the 7th ENTRY (KALAN = the teacher family; **DISSOLVED the marriage Jan 15, 1953 Ljubljana**; the white strip died Apr 14, 2003); r23 h12 the 13th ENTRY (**died Sep 14, 1987 TRUPOLI = TRIPOLI!**); r6/r7 h45+h46 THE TWINS (Anton + Jožefa — the SAME parents/godparents — in TWO neighbouring houses!); PRIESTS/SIGNATURES: »Paulin Bitnar« 11 + »Jos. Rauq« 7 (continuing the P105/P106 blocks); MIDWIFE: 19/20 named — MARIJA MEH 12/20 THE DOMINANT (all Marija!) + Adlešič 2 + Barbara Brinec 1 (r75 the father's family!) + Marija Jakofčič 1 + Marija Pletoj? 1 + 1 unclear (r45); the personal-ID campaign: 5 anchors (3 CONSISTENT + 1 POSSIBLE correction r42 the month 06 vs 05 + 1 [~] r75); ANOMALIES: **the father column carries a WOMAN'S NAME (r32 h18 »Marija Tomec« — the 1st case of the sample!)** + (V?)mpohranca/-gina with an empty baptism (r9+r44) + **sub divo a stillbirth (r47 Klojter — the 1st in the sample!)** + the November heading hidden under the strip (r79) + r36 hidden under the strip + TWO NAMES (r63) + 2 marriage annulments (r12 1953 + r86 1956/57 Varaždin) + 6 infants/children † + twins ×3 (r6/r7 Griblje! + r49/r50 + r85/r86 non-Griblje) + h85 TWO ENTRIES in 1912 (r51+r74 — non-Griblje) + an out-of-wedlock teacher (r88 Gradac 1; signed by the confessor Miklavž Belševič?); died TRIPOLI (r23); EXCLUDED: 69 (r36 under the strip, r65 Marijana under the strip, r79 November under the strip, r72 a fragment); the script scripts/p107_parish_baptism_1912.py (I1–I12, --check 14/14 PASS); status SAMPLE-TRANSCRIPTION-1912",
  p107Errors.length === 0,
  p107Errors.length === 0
    ? `20 vpisov / 20 hiš — NARE 20/20 (8. čisto leto) · okvir 1912 skeni 229–240 (glava INLINE str. 202; 88 vrstic) – row 88 + **glava 1913 INLINE str. 209 DNO (P108 lead: 1913 r1 Cerkvišče 31? Marija — Januar 1913 ima vpise na 209 dnu!)** · NOVELA: ŠTIRI dup pari (231/232 + 235/236 + 237/238 + 239/240 — 2. največ) · stran == sken − 27/− 28/− 29/− 30 · **1 NOVA hiša h86 (prva po 1909!)** · PT 16/4 · SELIJA h10→h70 (1909 Brinec par!) · h8 VRZEL 23 LET NOV REKORD · h70 VRZEL 19 · h71 18 · h59 13 · h24 16. VPIS NOV REKORD HIŠE (ZAPORED 2. leto) · h33 GENETSKA ×2 (»Grišice«; Papič!) · h22 Miko Alek MLINAR · h86 NOVA (Brinec ×3 + poroka 1946 Sprem) · h5 MEH ×2 · h90 Kalan + RAZVEZAL 1953 · h12 † TRIPOLI 1987 · h45/h46 DVOJČKI (2 hiši!) · ANOMALIJA očetova kolona žensko ime (r32) · sub divo (r47) · November glava pod trakom (r79) · Bitnar 13 + Rauq 7 · babica MEH 12/20 DOMINANTA · EMŠO 5 sidr · 6 † · 2 razveljavitvi · nezakonska učiteljica (r88) · EXCLUDED 69 · vitals 467 · kumulativ 457/86 27 let`
    : p107Errors.join("; "),
);

// ——— qa-p108: župnija Podzemelj — krstna 1913 (P108; issue #18) ———
const p108PageOfScan = (s: number) =>
  s === 239 || s === 240 ? 209 : s === 241 || s === 242 ? 210 : s === 243 || s === 244 ? 211 : s >= 245 && s <= 250 ? 212 : s - 38;
const p108Hv = HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year === 1913);
const p108Errors: string[] = [];
if (p108Hv.length !== 18)
  p108Errors.push(`vpisov 1913 (04105, zasidrani) ≠ 18 (${p108Hv.length})`);
const p108Houses = new Set(p108Hv.map((h) => h.houseNo));
if (p108Houses.size !== 17)
  p108Errors.push(`različnih hiš ≠ 17 (${p108Houses.size}: ${[...p108Houses].sort((a, b) => Number(a) - Number(b)).join(",")})`);
// NARE PRELOM: h31 ×2 (r10 + r70) — 1. ponovitev od P104
const p108RepeatHouses = [...p108Hv.map((h) => h.houseNo)].filter((hn, i, arr) => arr.indexOf(hn) !== i);
if (p108RepeatHouses.length !== 1 || p108RepeatHouses[0] !== "31")
  p108Errors.push(`intra-letne ponovitve 1913 ≠ ["31"] (NARE PRELOM h31 ×2) — najdeno: ${p108RepeatHouses.join(",")}`);
// okvir: stran == sken po P108 noveli (ŠTIRI dup bloki; str. 212 = ŠEST skenov)
const p108BadPage = p108Hv.filter(
  (h) => h.status !== "DOCUMENTED" || !h.scan || !h.page
    || h.page !== p108PageOfScan(h.scan)
    || h.scan < 239 || h.scan > 256,
);
if (p108BadPage.length > 0)
  p108Errors.push(`scan/page ne ustreza P108 noveli (dup 239/240+241/242+243/244+245–250): ${p108BadPage.map((h) => `${h.houseNo}@${h.scan}`).join(",")}`);
// 1 NOVA hiša (h76 — prvi vpis v vseh treh knjigah; 2. ZAPORED leto z novo hišo)
const p108PriorHouses = new Set(
  HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year !== 1913).map((h) => h.houseNo),
);
const p108New = [...p108Houses].filter((hn) => !p108PriorHouses.has(hn));
if (p108New.length !== 1 || p108New[0] !== "76")
  p108Errors.push(`nove hiše 1913 ≠ ["76"] (${p108New.join(",") || "brez"})`);
// sidra: SELIJA h36→h86 + NOVA h76 + NARE PRELOM h31 + MENJAVA h34/h47 + VRNJEN h65
const p108Pins: Array<[string, string]> = [
  ["31", "NARE PRELOM"], ["31", "DVE RAZLIČNI FAMILIJI"], ["31", "Teprič"],
  ["9", "13 LET"],
  ["65", "VRNJEN"], ["65", "Milek"],
  ["6", "Jakofčič"],
  ["8", "Völler"], ["8", "ZAPORED"],
  ["28", "Lozar"], ["28", "NEZAKONSKA"],
  ["44", "VSTAVEK"], ["44", "Štrucelj"],
  ["72", "Štraus"], ["72", "Šimec"],
  ["59", "ZAPORED"], ["59", "Jaklič"],
  ["34", "MENJAVA DRUŽINE"], ["34", "Milek"],
  ["13", "Matija Jakofčič"], ["13", "REŠENO"],
  ["36", "Hrižan"], ["36", "HRIŽAN"],
  ["86", "SELIJA"], ["86", "Hrižan"], ["86", "Štraus"],
  ["76", "NOVA HIŠA"], ["76", "Muc"], ["76", "PT SKLADNO"],
  ["46", "Polak"], ["46", "Brodarič"],
  ["60", "Kalan"], ["60", "Meh"],
  ["47", "MENJAVA DRUŽINE"], ["47", "Timec"],
];
for (const [n, pin] of p108Pins) {
  const cur = p108Hv.find((h) => h.houseNo === n);
  if (!cur) {
    p108Errors.push(`pin ${n} (${pin}) — hiša ${n} ni v 1913 blokih`);
    continue;
  }
  if (!cur.whatSi.includes(pin))
    p108Errors.push(`pin hiša ${n} (${pin}) manjka`);
}
// vitals skupaj 467 (po P108: 449 + 18; krstna 1913)
if (HOUSE_VITALS.length !== 685)
  p108Errors.push(`HOUSE_VITALS ≠ 467 (${HOUSE_VITALS.length})`);
// babica: 18/18 imenovanih; Jakofčič 8 DOMINANTA (prvič ne-Meh!) + Pleščič 4 + Adlešič 3 + Mavrenič 2 + Meh 1
if (p108Hv.filter((h) => h.whatSi.includes("babica")).length !== 18)
  p108Errors.push(`babica ni v vseh 18 whatSi (${p108Hv.filter((h) => h.whatSi.includes("babica")).length})`);
const p108Jakofcic = p108Hv.filter((h) => h.whatSi.includes("babica Marija Jakofčič")).length;
if (p108Jakofcic !== 8)
  p108Errors.push(`babica Marija Jakofčič ≠ 8× (${p108Jakofcic} — DOMINANTA 1913, prvič ne-Meh!)`);
const p108Plescic = p108Hv.filter((h) => h.whatSi.includes("babica Marija Pleščič")).length;
if (p108Plescic !== 4)
  p108Errors.push(`babica Marija Pleščič ≠ 4× (${p108Plescic})`);
const p108Adlesic = p108Hv.filter((h) => h.whatSi.includes("babica Barbara Adlešič")).length;
if (p108Adlesic !== 3)
  p108Errors.push(`babica Barbara Adlešič ≠ 3× (${p108Adlesic})`);
const p108Mavrenic = p108Hv.filter((h) => h.whatSi.includes("babica Ana Mavrenič")).length;
if (p108Mavrenic !== 2)
  p108Errors.push(`babica Ana Mavrenič ≠ 2× (${p108Mavrenic})`);
const p108Meh = p108Hv.filter((h) => h.whatSi.includes("babica Marija Meh")).length;
if (p108Meh !== 1)
  p108Errors.push(`babica Marija Meh ≠ 1× (${p108Meh} — MEH padec z 12/20 na 1/18!)`);
// podpisi (bloki): Bitnar 6 + Rauq 11 + Polak 1 = 18 vsi (3 duhovniki!)
if (p108Hv.filter((h) => h.whatSi.includes("Bitnar")).length !== 6)
  p108Errors.push(`podpis Bitnar ≠ 6× (${p108Hv.filter((h) => h.whatSi.includes("Bitnar")).length})`);
if (p108Hv.filter((h) => h.whatSi.includes("podpis Jos. Rauq")).length !== 11)
  p108Errors.push(`podpis Jos. Rauq ≠ 11× (${p108Hv.filter((h) => h.whatSi.includes("podpis Jos. Rauq")).length})`);
if (p108Hv.filter((h) => h.whatSi.includes("Polak")).length !== 1)
  p108Errors.push(`podpis Polak (kap.) ≠ 1× (${p108Hv.filter((h) => h.whatSi.includes("Polak")).length} — NOVI 3. duhovnik 1913!)`);
// EMŠO sidra v blokih: 5 (r32/r72/r75/r87/r95 — 4 SKLADNA + 1 MOŽEN popravek r95 sex-digit)
const p108Emso = p108Hv.filter((h) => /sidro/i.test(h.whatSi) || h.whatSi.includes("MOŽEN POPRAVEK"));
if (p108Emso.length !== 5)
  p108Errors.push(`EMŠO sidrov v blokih ≠ 5 (${p108Emso.length})`);
for (const emso of ["1004913500031", "2008913505094", "2508913505169", "2809913500032", "0411913500028"]) {
  if (!p108Hv.some((h) => h.whatSi.includes(emso)))
    p108Errors.push(`EMŠO sidro ${emso} manjka`);
}
// SELIJA h36 → h86 (P107 h36 par) — 3. selitev vzorca
if (!p108Hv.some((h) => h.houseNo === "86" && h.whatSi.includes("SELIJA h36 → h86")))
  p108Errors.push("SELIJA h36 → h86 (3. selitev vzorca) manjka");
// P109 lead: glava 1914 INLINE str. 218 dno + 1914 r1 EMŠO + r5 Griblje
if (!p108Hv.some((h) => h.houseNo === "47" && h.whatSi.includes("P109")))
  p108Errors.push("P109 lead v h47 bloku manjka");
push(
  "qa-p108-parish-baptism-1913",
  "P108: ŽUPNIJA PODZEMELJ — KRSTNA KNJIGA 04105, POLNO LETO 1913 (issue #18; SAMPLE-TRANSCRIPTION-1913; MERI, NE odloča; v7 join nespremenjen): širitev vzorca P79 (1886) → … → P105 (1910) → P106 (1911) → P107 (1912) na leto 1913 — okvir: glava »1913« INLINE na str. 209 DNO = s239/240 (pod 1912 r88; 1913 r1 = Cerkvišče 21 Marija 4./10. Januar, EMŠO 0401913505350 — P107 lead POTRJEN vas, hiša POPRAVLJENA 31? → 21 forenziko s239/240-A!) – row 105 na str. 218 (Boršt 21 Alojzij; **glava »1914« INLINE na str. 218 DNO = s256 (pod r105!)** — P109 lead: 1914 r1 = [vas] 17 Terezija 1./1., EMŠO 01019141505225 (VPIS PRENEŠEN 16.10.2002); 1914 r5 = Griblje 1?/4? Anton [~]) == tiskane strani 209–218 (**105 vrstic — NAJVEČ v vzorcu**, prej rekord 1908 = 90!); NOVELA P108: ŠTIRI dup bloki — 239/240 + 241/242 + 243/244 + **245–250 = str. 212 (ŠEST skenov iste strani — re-scan serija, največ doslej!)**; stran == sken − 30 (239/240) / − 31 (241/242) / − 32 (243/244) / DUP (245–250) / − 38 (251+); VSI vpisi z Griblji: **18 vpisov / 17 hiš** — NARE PRELOM (h31 ×2 = r10+r70 — **1. ponovitev od P104!** + **DVE RAZLIČNI FAMILIJI v h31 isto leto**: r10 Teprič? × Šrajgar? + r70 Černič × Počelf?); **1 NOVA hiša h76 (r80) — prvi vpis v vseh treh knjigah; 2. ZAPORED leto z novo hišo (h86 1912 → h76 1913: 0/1/0/0/0/0/0/0/1/1!)**; PT 12/5 (44+46+47+59+60 v luknji 41–60; h44 NOVO v gap-listi; h76 v naboru SKLADNO); kumulativ **475 vpisov / 87 hiš** čez tri knjige in **28 let** (1886–1913; 467 vitals); SIDRA: r72/r75 **SELIJA h36 → h86** (Marko Hrižan × Katarina Štraus = P107 h36 par — **3. selitev vzorca** cf. h30→h10 1909 + h10→h70 1912!); r49 **MENJAVA h34** (Brinec × Milek → Krambič × Milek? — mati familija obstane!); r95 **MENJAVA h47** (Požek → Timec?); r32 h28 očakovsko razrešeno (1910 nezakonska → 1913 oče Lozar); r63 oče **REŠEN** (faza-1 »Marija→Matija?« = Matija Jakofčič — 4× forenzika!); **r15 VRNJEN V SEZNAM** (faza-1 surova transkripcija je r15 IZPUSTILA — forenzika s241-A: Griblje 65 + oče Matija Milek SKLADNO s h65 MILEK! → 18 vpisov); r80 **h76 NOVA HIŠA** (oče šoždar? redkost; mati Muc; PT SKLADNO); r39 h72 **ZAPORED ISTA ZVEZA Strauš × Šimec 3. skupaj** (1909+1911+1913!); r8/r44/h8 ZAPORED 2. leto (Völler boter POVRAČNICA!); DUHOVNIKI/PODPISI: »Paulin Bitnar« 6 + »Jos. Rauq« 11 + **»R. Ozlob? Polak, kap.« 1 (NOVI 3. duhovnik — blok r82–r87 s254!)** = 18 vsi; + Ivan Nemanič, umirovljen župnik (r67/r77 non-Griblje); BABICA: **18/18 imenovanih — VSI!** — **MARIJA JAKOFČIČ 8/18 DOMINANTA (prvič ne-Meh dominanta!)** + Pleščič 4 + Adlešič 3 + Mavrenič 2 + **Meh 1 (MEH padec z 12/20 na 1/18 — konec dominance!)**; EMŠO kampanja: **~30 marginalij — NAJVEČJA doslej!**; 5 Griblje sidr (4 SKLADNA + 1 MOŽEN popravek r95 sex-digit 02 = moški vs ženska); ANOMALIJE: **papirni vstavek »Pozamanitev« čez r35** (Kosec pocigan? × Hudovirac ciganka — otrok Leopold — potujoča družina — unikat!) + **2 POZNEJŠA VPISA** (r2 Kranjak 15 rojen 10.3.1891 — 22 let pred vpisom; »vpisan pozneje na ukaz št. 136/1919« + r85 Rajmund »na Tolminskem« št. 3437) + 2 KAROLINI zapored (r37+r38) + 2 para DVOJČKOV (r29/r30 Dobraviče 40 + r57/r58 Dragoče 5) + 3 NEZAKONSKI (r8+r9 zapored + r45 s trakom župnika) + nujni krst r22 (botra + podpis PRAZNA — 3. signal!) + vas »Klojter« ×4 (r26/r83/r96/r98) + žensko ime v očetovi koloni ×3 (r47/r79/r98 — r63 REŠEN!) + **2 smrtna signala 2. svetovne vojne** (r88 h60 ⚰ 29.12.1944 + r8 razglašen za mrtvega 13.12.1944!) + r16 vas pod nalepko (umrla »v kraju Griblje« 2004 — dilema h23 — EXCLUDED) + h9 VRZEL 13 LET (najdaljša 1913) + h36 ZAPORED 3. leto + r15 † marginalia popravek (1.1.1917); P108 lead POPRAVLJEN (r1 hiša 31? → 21; r3 EMŠO 5196 → 5496; r5 vas Zemelj + EMŠO 280... → 2501913505466); EXCLUDED: 87 (+ vstavek; r51 »Grišice« 44 Kraf × Štraus NEODLOČENO — hišna kolizija z r35); skripta scripts/p108_parish_baptism_1913.py (I1–I12 + I3b/I5b/I9b, --check 15/15 PASS); status SAMPLE-TRANSCRIPTION-1913",
  "P108: PARISH OF PODZEMELJ — BAPTISM REGISTER 04105, THE FULL YEAR 1913 (issue #18; SAMPLE-TRANSCRIPTION-1913; MEASURES, does not decide; the v7 join unchanged): extending the sample P79 (1886) → … → P105 (1910) → P106 (1911) → P107 (1912) to 1913 — the frame: the heading »1913« INLINE at the bottom of p. 209 = s239/240 (below the 1912 r88; the 1913 r1 = Cerkvišče 21 Marija Jan 4/10, personal ID 0401913505350 — the P107 lead CONFIRMED for the village, the house CORRECTED 31? → 21 by the s239/240-A forensics!) – row 105 on p. 218 (Boršt 21 Alojzij; **the 1914 heading INLINE at the bottom of p. 218 = s256 (below r105!)** — the P109 lead: 1914 r1 = [village] 17 Terezija Jan 1/1, personal ID 01019141505225 (the entry transferred Oct 16, 2002); 1914 r5 = Griblje 1?/4? Anton [~]) == printed pages 209–218 (**105 rows — THE MOST in the sample**, the previous record 1908 = 90!); THE P108 NOVEL: FOUR dup blocks — 239/240 + 241/242 + 243/244 + **245–250 = p. 212 (SIX scans of the same page — a re-scan series, the most ever!)**; page == scan − 30 (239/240) / − 31 (241/242) / − 32 (243/244) / DUP (245–250) / − 38 (251+); ALL Griblje entries: **18 entries / 17 houses** — the NARE BREAK (h31 ×2 = r10+r70 — **the 1st repeat since P104!** + **TWO DIFFERENT FAMILIES in h31 the same year**: r10 Teprič? × Šrajgar? + r70 Černič × Počelf?); **1 NEW house h76 (r80) — the first entry in all three books; the 2nd CONSECUTIVE year with a new house (h86 1912 → h76 1913: 0/1/0/0/0/0/0/0/1/1!)**; the PT 12/5 (44+46+47+59+60 in the gap 41–60; h44 NEW in the gap list; h76 in the set CONSISTENT); the cumulative **475 entries / 87 houses** across three books and **28 years** (1886–1913; 467 vitals); ANCHORS: r72/r75 **A MOVE h36 → h86** (Marko Hrižan × Katarina Štraus = the P107 h36 couple — **the 3rd move of the sample** cf. h30→h10 1909 + h10→h70 1912!); r49 **A FAMILY CHANGE h34** (Brinec × Milek → Krambič × Milek? — the mother family persists!); r95 **A FAMILY CHANGE h47** (Požek → Timec?); r32 h28 the fatherhood resolved (the 1910 out-of-wedlock → the 1913 father Lozar); r63 the father **RESOLVED** (the phase-1 »Marija→Matija?« = Matija Jakofčič — 4× forensics!); **r15 RESTORED TO THE LIST** (the phase-1 raw transcription OMITTED r15 — the s241-A forensics: Griblje 65 + father Matija Milek CONSISTENT with h65 MILEK! → 18 entries); r80 **h76 A NEW HOUSE** (the father a shoemaker? a rarity; the mother Muc; the PT CONSISTENT); r39 h72 **CONSECUTIVE the SAME COUPLE Strauš × Šimec the 3rd together** (1909+1911+1913!); r8/r44/h8 CONSECUTIVE the 2nd year (the godfather Völler the RETURNEE!); PRIESTS/SIGNATURES: »Paulin Bitnar« 6 + »Jos. Rauq« 11 + **»R. Ozlob? Polak, chaplain« 1 (A NEW 3rd priest — the block r82–r87 s254!)** = 18 all; + Ivan Nemanič, a retired dean (r67/r77 non-Griblje); MIDWIFE: **18/18 named — ALL!** — **MARIJA JAKOFČIČ 8/18 THE DOMINANT (the 1st non-Meh dominant!)** + Pleščič 4 + Adlešič 3 + Mavrenič 2 + **Meh 1 (MEH falling from 12/20 to 1/18 — the end of the dominance!)**; the personal-ID campaign: **~30 marginalia — THE MOST ever!**; 5 Griblje anchors (4 CONSISTENT + 1 POSSIBLE correction r95 the sex-digit 02 = male vs female); ANOMALIES: **a paper insert »Pozamanitev« across r35** (Kosec a tinsmith? × Hudovirac a Roma woman — the child Leopold — a travelling family — a unique!) + **2 LATE ENTRIES** (r2 Kranjak 15 born Mar 10, 1891 — 22 years before the entry; »entered later by order no. 136/1919« + r85 Rajmund »at Tolminsko« no. 3437) + 2 KAROLINAS consecutive (r37+r38) + 2 pairs of TWINS (r29/r30 Dobraviče 40 + r57/r58 Dragoče 5) + 3 out-of-wedlock (r8+r9 consecutive + r45 with the dean's strip) + the emergency baptism r22 (godparents + signature EMPTY — the 3rd signal!) + the village »Klojter« ×4 (r26/r83/r96/r98) + a woman's name in the father column ×3 (r47/r79/r98 — r63 RESOLVED!) + **2 WWII death signals** (r88 h60 died Dec 29, 1944 + r8 declared dead Dec 13, 1944!) + r16 the village under the label (died »in Griblje« 2004 — the h23 dilemma — EXCLUDED) + h9 a 13-YEAR GAP (the longest of 1913) + h36 CONSECUTIVE the 3rd year + the r15 death-marginalia correction (Jan 1, 1917); the P108 lead CORRECTED (r1 house 31? → 21; r3 ID 5196 → 5496; r5 the village Zemelj + ID 280... → 2501913505466); EXCLUDED: 87 (+ the insert; r51 »Grišice« 44 Kraf × Štraus UNDECIDED — a house collision with r35); the script scripts/p108_parish_baptism_1913.py (I1–I12 + I3b/I5b/I9b, --check 15/15 PASS); status SAMPLE-TRANSCRIPTION-1913",
  p108Errors.length === 0,
  p108Errors.length === 0
    ? `18 vpisov / 17 hiš — NARE PRELOM (h31 ×2 — 1. ponovitev od P104 + DVE FAMILIJI!) · okvir 1913 skeni 239–256 (glava INLINE str. 209 DNO; **105 vrstic — NAJVEČ!**) – row 105 + **glava 1914 INLINE str. 218 DNO (P109 lead: 1914 r1 Terezija EMŠO 01019141505225; r5 Griblje Anton [~])** · NOVELA: ŠTIRI dup bloki (239/240 + 241/242 + 243/244 + **245–250 ŠEST skenov str. 212!**) · stran == sken − 30/− 31/− 32/DUP/− 38 · **1 NOVA hiša h76 (vse tri knjige! 2. ZAPORED leto)** · PT 12/5 (h44 NOVO v gap) · SELIJA h36→h86 (Hrižan × Štraus — 3. selitev!) · MENJAVA h34 (Milek obstane!) + h47 (Požek→Timec?) · h28 oče Lozar razrešeno · r63 Matija REŠENO · **r15 VRNJEN (faza-1 izpust!)** · h72 Strauš × Šimec 3. skupaj · Bitnar 6 + Rauq 11 + **Polak 1 (3. duhovnik!)** · babica **JAKOFČIČ 8/18 DOMINANTA (prvič ne-Meh!)** + Meh 1 (padec!) · EMŠO ~30 marginalij (največ!) · 5 sidr · vstavek Pozamanitev (r35) · 2 poznejša vpisa (r2 rojen 1891! + r85) · 2 Karolini · 2 para dvojčkov · 3 nezakonski · nujni krst r22 · Klojter ×4 · žensko ime v očetovi koloni ×3 · 2 † 1944 · h9 VRZEL 13 LET · EXCLUDED 87 · vitals 467 · kumulativ 475/87 28 let`
    : p108Errors.join("; "),
);

// ——— qa-p109: župnija Podzemelj — krstna 1914 (P109; issue #18) ———
const p109PageOfScan = (s: number) =>
  ({ 256: 218, 257: 218, 258: 219, 259: 219, 260: 220, 261: 220, 262: 221, 263: 222, 264: 222, 265: 223, 266: 223, 267: 224, 268: 224 } as Record<number, number>)[s] ?? -1;
const p109Hv = HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year === 1914);
const p109Errors: string[] = [];
if (p109Hv.length !== 12)
  p109Errors.push(`vpisov 1914 (04105, zasidrani) ≠ 12 (${p109Hv.length})`);
const p109Houses = new Set(p109Hv.map((h) => h.houseNo));
if (p109Houses.size !== 12)
  p109Errors.push(`različnih hiš ≠ 12 (${p109Houses.size}: ${[...p109Houses].sort((a, b) => Number(a) - Number(b)).join(",")}) — NARE 12/12!`);
// NARE 12/12 — brez ponovitev (9. čisto leto)
const p109RepeatHouses = [...p109Hv.map((h) => h.houseNo)].filter((hn, i, arr) => arr.indexOf(hn) !== i);
if (p109RepeatHouses.length !== 0)
  p109Errors.push(`intra-letne ponovitve 1914 morajo biti PRAZNE (NARE 12/12) — najdeno: ${p109RepeatHouses.join(",")}`);
// okvir: ŠEST dup parov (256/257 + 258/259 + 260/261 + 263/264 + 265/266 + 267/268; enojni s262)
const p109BadPage = p109Hv.filter(
  (h) => h.status !== "DOCUMENTED" || !h.scan || !h.page
    || h.page !== p109PageOfScan(h.scan)
    || h.scan < 256 || h.scan > 266,
);
if (p109BadPage.length > 0)
  p109Errors.push(`scan/page ne ustreza P109 noveli (ŠEST dup parov; enojni s262): ${p109BadPage.map((h) => `${h.houseNo}@${h.scan}`).join(",")}`);
// 0 novih hiš (prvič po 1912/13!)
const p109PriorHouses = new Set(
  HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year !== 1914).map((h) => h.houseNo),
);
const p109New = [...p109Houses].filter((hn) => !p109PriorHouses.has(hn));
if (p109New.length !== 0)
  p109Errors.push(`nove hiše 1914 morajo biti PRAZNE (0 — prvič po 1912/13!) — najdeno: ${p109New.join(",")}`);
// sidra: r29 NOVA VRSTICA + žensko ime; r54 dvom REŠEN; r21/r28 hiši; r38 šahtar; r42 botra Lozar; r45 učitelj; r62 ZAPORED
const p109Pins: Array<[string, string]> = [
  ["1", "ANA"], ["1", "Štrucel"], ["1", "Polak"],
  ["14", "Brinec"], ["14", "VRZEL 3 LETA"],
  ["53", "VRZEL 16 LET"], ["53", "Perdivec"],
  ["11", "1803914505878"], ["11", "ZAVRŽENO"],
  ["44", "ZAVRŽEN"], ["44", "11.04.2001"], ["44", "ŠTRUCELJ"],
  ["5", "NOVA VRSTICA VZORCA"], ["5", "Štrucel"], ["5", "0405914505481"], ["5", "ŽENSKO IME"],
  ["77", "ŠAHTAR"], ["77", "Anfons"],
  ["21", "3006914500518"], ["21", "Anton Lozar + Barbara Lozar"],
  ["90", "učitelj"], ["90", "Štrucel"],
  ["18", "2108914500174"], ["18", "Brinec"],
  ["48", "REŠEN"], ["48", "12. VPIS"],
  ["8", "ZAPORED"], ["8", "Matija Štrucel + Katarina Potter"], ["8", "P110"],
];
for (const [n, pin] of p109Pins) {
  const cur = p109Hv.find((h) => h.houseNo === n);
  if (!cur) {
    p109Errors.push(`pin ${n} (${pin}) — hiša ${n} ni v 1914 blokih`);
    continue;
  }
  if (!cur.whatSi.includes(pin))
    p109Errors.push(`pin hiša ${n} (${pin}) manjka`);
}
// EMŠO reassign: 2210914505196 = r63 (v h8 bloku kot »NE r62«!)
if (!p109Hv.some((h) => h.houseNo === "8" && h.whatSi.includes("NE r62")))
  p109Errors.push("EMŠO reassign (2210914505196 → r63) manjka v h8 bloku");
// vitals skupaj 490 (po P110: 479 + 11; krstna 1915)
if (HOUSE_VITALS.length !== 685)
  p109Errors.push(`HOUSE_VITALS ≠ 479 (${HOUSE_VITALS.length})`);
// babica: 12/12 imenovanih; Jakofčič 4 DOMINANTA (2. leto zapored)
if (p109Hv.filter((h) => h.whatSi.includes("babica")).length !== 12)
  p109Errors.push(`babica ni v vseh 12 whatSi (${p109Hv.filter((h) => h.whatSi.includes("babica")).length})`);
const p109Jakofcic = p109Hv.filter((h) => h.whatSi.includes("babica Marija Jakofčič")).length;
if (p109Jakofcic !== 4)
  p109Errors.push(`babica Marija Jakofčič ≠ 4× (${p109Jakofcic} — DOMINANTA 1914!)`);
// podpisi (jasni): Rauq ≥4 (r13/r29/r38/r45) + Bitnar ≥2 (r53/r62) + Polak 1 (r5)
if (p109Hv.filter((h) => h.whatSi.includes("podpis Jos. Rauq")).length < 4)
  p109Errors.push(`podpis Jos. Rauq < 4× (${p109Hv.filter((h) => h.whatSi.includes("podpis Jos. Rauq")).length})`);
if (p109Hv.filter((h) => h.whatSi.includes("Pavlin Bitnar")).length < 2)
  p109Errors.push(`podpis Pavlin Bitnar < 2× (${p109Hv.filter((h) => h.whatSi.includes("Pavlin Bitnar")).length})`);
if (p109Hv.filter((h) => h.whatSi.includes("Polak")).length !== 1)
  p109Errors.push(`podpis Polak (kap.) ≠ 1× (${p109Hv.filter((h) => h.whatSi.includes("Polak")).length} — r5!)`);
// EMŠO sidra v blokih: 4 SKLADNA (r21/r29/r42/r53) + r28/r54 [~]
const p109Emso = ["1803914505878", "0405914505481", "3006914500518", "2108914500174"];
for (const emso of p109Emso) {
  if (!p109Hv.some((h) => h.whatSi.includes(emso)))
    p109Errors.push(`EMŠO sidro ${emso} manjka`);
}
// P110 lead: glava 1915 = VRH str. 225 = s269 (NI INLINE!) + r8 Griblje 88 + konec porodov
if (!p109Hv.some((h) => h.houseNo === "8" && h.whatSi.includes("s269") && h.whatSi.includes("78 konec porodov")))
  p109Errors.push("P110 lead (glava 1915 s269 + konec porodov) manjka v h8 bloku");
push(
  "qa-p109-parish-baptism-1914",
  "P109: ŽUPNIJA PODZEMELJ — KRSTNA KNJIGA 04105, POLNO LETO 1914 (issue #18; SAMPLE-TRANSCRIPTION-1914; MERI, NE odloča; v7 join nespremenjen): širitev vzorca P79 (1886) → … → P106 (1911) → P107 (1912) → P108 (1913) na leto 1914 — **PRVO VOJNO leto!** — okvir: glava »1914« INLINE na str. 218 (pod 1913 r105 = s256/257; 1914 r1 = [vas pod marg.] 17 Terezija 1./1. Januar, EMŠO 01019141505225, VPIS PRENEŠEN 16.10.2002 — P108 lead POTRJEN!) – row 79 na str. 224 (**r79 PREČRTANA** — diagonalni udarci čez vse celice: Otok 10 Marija, Peter Kure? bajtar × Ana Kržan?, botra Miko? + Ana Kržan?, babica Marija Plešič?, podpis Bitnar!) + opomba na dnu str. 224: **»78 konec porodov l. 1914«** (3.5× POTRJENO!); **glava 1915 NI INLINE na dnu str. 224 — je na VRHU str. 225 = s269** (ročno dopisan »1915.« nad tiskano glavo — P110 lead!) == tiskane strani 218–224 (78 veljavnih vrstic + 1 prečrtana); NOVELA P109: **ŠEST dup parov skenov — NOV REKORD (2. leto zapored!)** — 256/257 + 258/259 + 260/261 + 263/264 + 265/266 + 267/268 (enojni samo s262 = str. 221); VSI vpisi z Griblji: **12 vpisov / 12 hiš — NARE 12/12 (9. čisto leto!)** + **0 NOVIH hiš (prvič po 1912/13 — h86 1912 + h76 1913!)**; PT 9/3 (h44 + h48 + h53 v luknji 41–60 — vse tri dokazane!); kumulativ **487 vpisov / 87 hiš** čez tri knjige in **29 let** (1886–1914; 479 vitals); SIDRA: **r29 Griblje 5 NOVA VRSTICA VZORCA** (faza-1 je r29 izpustila — nalepka blok; Janez, EMŠO 0405914505481 SKLADNO, oče-kolona »Marija Štrucel« — ŽENSKO IME!) + **r54 Griblje 48 DVOM FAZE 1 REŠEN** (začetnica »G« jasna skozi prozoren trak 5×! → 12. vpis) + r5 hiša **1** POTRJENA (4.5×; faza-1 »1?/4?« + »Anton« POPRAVLJENA → **ANA**, † 9.2.1915!) + r21 hiša **11** POTRJENA (na OBEH dupih 4.5×; faza-1 »pod zavihkom« ZAVRŽENO!) + r28 hiša **44** POTRJENA (band-dvom »34« ZAVRŽEN) + r17 h53 **VRZEL 16 LET** (najdaljša 1914!) + r13 h14 **VRZEL 3 LETA** (faza-1 »18« POPRAVLJENO — h14 = 1896/1900/1902/1908/1911!) + r42 starši **Papič × Krixan** (faza-1 zamenjava: »Anton Lavca + Ana Tome« = BOTRA **Anton + Barbara Lozar**!) + r45 oče **Ernest Šušteršič, ljudski učitelj** + r38 oče **Janez Božič? ŠAHTAR (rudar — edinstven poklic!)** + r62 botra **Štrucel + Potter** (faza-1 »Hrovat« POPRAVLJENO) + **EMŠO 2210914505196 = r63 Zemelj 20 (22./22. OKTOBER) — faza-1 pripis r62 POPRAVLJEN** (Oktober glava med r62/r63!); DUHOVNIKI/PODPISI: Rauq ~6 + Bitnar ~3 + **Polak 1 (r5!)** + **»Dostál« 1 (r22 — NOVI 4. duhovnik!)** + Koziga? 1 [~]; BABICA: 12/12 imenovanih — **MARIJA JAKOFČIČ 4/12 DOMINANTA (2. leto zapored!)** + Pleščič 2? + Adlešič 2? + Mavrenič 2 + Jakobčič 1? + Karevič 1?; EMŠO kampanja ~20 marginalij — 4 SKLADNA sidra (r21 + r29 + r42 + r53) + 2 [~]; ANOMALIJE: **r78 MRTVOROJEN »J. mrtvorojeno«** (24./— Cerkvišče 7: Jožef Dragos? ½ zemlj. × Katarina raj. Bahorič; krsta/botra/podpis PRAZNO — 2. sub divo signal!) + **žensko ime v očetovi koloni ×3 = izenačeno s rekordom P108** (r29 Štrucel + r39 Križan + r63 Šilah) + **mesečne glave PODOBLJENE na meji strani** (September ×2 str. 222/223 + November ×2 str. 223/224!) + **1. SVETOVNA VOJNA — † marginalia ×7+** (r10 Jože 30.7.1915 + r16 Matija 17.7.1916 + r61 Frančišek 19.1.1916 + r68 Martin 12.7.1916 + r69 Jožef 14.7.1916 + r75 Kapitolina 12.1916? + r50 vojak BOLOGNA 25.3.1919 + r58 VELIKA vojno-invalidska marginalia Podrečje 25.11.1917) + **4/12 Griblje otrok † 1914/15 = 33%** (r5 Ana + r21 Jožefa + r45 Ivanka + r62 Jožefa!) + r75 **Kapitolina** (faza-1 »Jožef« POPRAVLJENO; oče-kolona PRAZNA!) + r10 **Aloizija** (faza-1 »Flavijana« POPRAVLJENO; nalepka z oznako »10.«) + r16/r18 nalepka-razrešitev († 2000 = r18, NE r17) + r60 ime spremenjeno (odločba 1999) + vpisi prenešeni 2002–2007 (r1/r14/r60/r63) + h44 + h8 **ZAPORED 2. leto** (Štrucelj + Jakobčič!); ŠTRUCEL mreža 1914: r5 boter + r29 mati? + r45 botri ×2 + r62 boter (h44 familija = 5 vez!); EXCLUDED: 66 (+ r79 prečrtana); skripta scripts/p109_parish_baptism_1914.py (I1–I12, --check 14/14 PASS); status SAMPLE-TRANSCRIPTION-1914",
  "P109: PARISH OF PODZEMELJ — BAPTISM REGISTER 04105, THE FULL YEAR 1914 (issue #18; SAMPLE-TRANSCRIPTION-1914; MEASURES, does not decide; the v7 join unchanged): extending the sample P79 (1886) → … → P108 (1913) to the year 1914 — **the FIRST WAR YEAR!** — the frame: the 1914 heading INLINE on p. 218 (below the 1913 r105 = s256/257; the 1914 r1 = [village under the marg.] 17 Terezija Jan 1/1, personal ID 01019141505225, the entry transferred Oct 16, 2002 — the P108 lead CONFIRMED!) – row 79 on p. 224 (**r79 STRUCK THROUGH** — diagonal strokes across all cells: Otok 10 Marija, Peter Kure? cottager × Ana Kržan?, godparents Miko? + Ana Kržan?, midwife Marija Plešič?, signature Bitnar!) + the note at the bottom of p. 224: **»78 konec porodov l. 1914«** (»78 the end of births year 1914« — CONFIRMED at 3.5×!); **the 1915 heading NOT INLINE at the bottom of p. 224 — it is at the TOP of p. 225 = s269** (»1915.« manually added above the printed heading — the P110 lead!) == printed pages 218–224 (78 valid rows + 1 struck); THE P109 NOVEL: **SIX dup pairs of scans — A NEW RECORD (the 2nd consecutive year!)** — 256/257 + 258/259 + 260/261 + 263/264 + 265/266 + 267/268 (single only s262 = p. 221); ALL Griblje entries: **12 entries / 12 houses — NARE 12/12 (the 9th clean year!)** + **0 NEW houses (the first time since 1912/13 — h86 1912 + h76 1913!)**; the PT 9/3 (h44 + h48 + h53 in the 41–60 gap — all three proven!); the cumulative **487 entries / 87 houses** across three books and **29 years** (1886–1914; 479 vitals); ANCHORS: **r29 Griblje 5 A NEW ROW OF THE SAMPLE** (the phase-1 omitted r29 — the label block; Janez, the personal ID 0405914505481 CONSISTENT, the father column »Marija Štrucel« — A WOMAN'S NAME!) + **r54 Griblje 48 THE PHASE-1 DOUBT RESOLVED** (the initial »G« clear through the transparent strip at 5×! → the 12th entry) + r5 house **1** CONFIRMED (4.5×; the phase-1 »1?/4?« + »Anton« CORRECTED → **ANA**, died Feb 9, 1915!) + r21 house **11** CONFIRMED (on BOTH duplicates at 4.5×; the phase-1 »under the page corner« REJECTED!) + r28 house **44** CONFIRMED (the band-doubt »34« REJECTED) + r17 h53 a **16-YEAR GAP** (the longest of 1914!) + r13 h14 a **3-YEAR GAP** (the phase-1 »18« CORRECTED — h14 = 1896/1900/1902/1908/1911!) + r42 the parents **Papič × Krixan** (the phase-1 swap: »Anton Lavca + Ana Tome« = the GODPARENTS **Anton + Barbara Lozar**!) + r45 the father **Ernest Šušteršič, a people's teacher** + r38 the father **Janez Božič? A MINER (a unique trade!)** + r62 the godparents **Štrucel + Potter** (the phase-1 »Hrovat« CORRECTED) + **the personal ID 2210914505196 = r63 Zemelj 20 (Oct 22/22) — the phase-1 attribution to r62 CORRECTED** (the October heading between r62/r63!); PRIESTS/SIGNATURES: Rauq ~6 + Bitnar ~3 + **Polak 1 (r5!)** + **»Dostál« 1 (r22 — A NEW 4th priest!)** + Koziga? 1 [~]; MIDWIFE: 12/12 named — **MARIJA JAKOFČIČ 4/12 THE DOMINANT (the 2nd consecutive year!)** + Pleščič 2? + Adlešič 2? + Mavrenič 2 + Jakobčič 1? + Karevič 1?; the personal-ID campaign ~20 marginalia — 4 CONSISTENT anchors (r21 + r29 + r42 + r53) + 2 [~]; ANOMALIES: **r78 A STILLBIRTH »J. mrtvorojeno«** (Dec 24/— Cerkvišče 7: Jožef Dragos? half smallholder × Katarina née Bahorič; the baptism/godparents/signature EMPTY — the 2nd sub divo signal!) + **a woman's name in the father column ×3 = tied with the P108 record** (r29 Štrucel + r39 Križan + r63 Šilah) + **the monthly headings DOUBLED at the page boundary** (September ×2 pp. 222/223 + November ×2 pp. 223/224!) + **WWI — death marginalia ×7+** (r10 Jože Jul 30, 1915 + r16 Matija Jul 17, 1916 + r61 Frančišek Jan 19, 1916 + r68 Martin Jul 12, 1916 + r69 Jožef Jul 14, 1916 + r75 Kapitolina Dec 1916? + r50 a soldier BOLOGNA Mar 25, 1919 + r58 a LARGE war-invalid marginalia Podrečje Nov 25, 1917) + **4/12 Griblje infants died 1914/15 = 33%** (r5 Ana + r21 Jožefa + r45 Ivanka + r62 Jožefa!) + r75 **Kapitolina** (the phase-1 »Jožef« CORRECTED; the father column EMPTY!) + r10 **Aloizija** (the phase-1 »Flavijana« CORRECTED; the label marked »10.«) + the r16/r18 label-resolution (died 2000 = r18, NOT r17) + r60 the name changed (the 1999 decree) + entries transferred 2002–2007 (r1/r14/r60/r63) + h44 + h8 **CONSECUTIVE the 2nd year** (Štrucelj + Jakobčič!); the ŠTRUCEL network 1914: the r5 godfather + r29 the mother? + the r45 godparents ×2 + the r62 godfather (the h44 family = 5 ties!); EXCLUDED: 66 (+ r79 struck); the script scripts/p109_parish_baptism_1914.py (I1–I12, --check 14/14 PASS); status SAMPLE-TRANSCRIPTION-1914",
  p109Errors.length === 0,
  p109Errors.length === 0
    ? `12 vpisov / 12 hiš — NARE 12/12 (9. čisto leto!) · **0 NOVIH hiš (prvič po 1912/13!)** · okvir 1914 skeni 256–268 (glava INLINE str. 218; 78 vrstic + r79 PREČRTANA + »78 konec porodov l. 1914«!) – row 79 + **glava 1915 na VRHU str. 225 = s269 (NI INLINE — P110 lead: 1915 r8 = GRIBLJE 88 Ivana!)** · NOVELA: **ŠEST dup parov = NOV REKORD (2. leto zapored)** · PT 9/3 (h44+h48+h53 dokazane) · **r29 NOVA VRSTICA (faza-1 izpust! žensko ime Štrucel v očetovi koloni!)** · **r54 dvom REŠEN (Griblje 48 skozi trak!)** · r5 ANA + hiša 1 (POPRAVEK) · r21 hiša 11 (ZAVRŽENO »zavihkom«) · r28 hiša 44 (ZAVRŽEN »34«) · h53 VRZEL 16 LET · h14 VRZEL 3 (POPRAVLJENO) · r42 Papič × Krixan (Lozar = botra!) · r45 oče UČITELJ Šušteršič · r38 oče ŠAHTAR · r62 botra Štrucel + Potter · **EMŠO 2210914505196 → r63 OKTOBER (POPRAVLJEN pripis!)** · Rauq ~6 + Bitnar ~3 + Polak 1 + **Dostál NOVI 4. duhovnik** · babica JAKOFČIČ 4/12 (2. leto!) · EMŠO 4 sidra SKLADNA · r78 mrtvorojen (vse PRAZNO) · žensko ime v očetovi koloni ×3 (= rekord P108!) · mesečne glave PODOBLJENE ×2 · **1. svetovna † ×7+ (Bologna 1919! Podrečje 1917!)** · **4/12 otrok † = 33%** · r75 Kapitolina (oče PRAZEN) · r10 Aloizija · ZAPORED h44+h8 · Štrucel mreža 5 vez · EXCLUDED 66 · vitals 479 · kumulativ 487/87 29 let`
    : p109Errors.join("; "),
);

// ——— qa-p110: župnija Podzemelj — krstna 1915 (P110; issue #18) ———
const p110PageOfScan = (s: number) =>
  ({ 269: 225, 270: 226, 271: 226, 272: 227, 273: 228, 274: 228, 275: 229, 276: 230, 277: 231, 278: 232, 279: 233, 280: 234, 281: 235, 282: 236, 283: 237 } as Record<number, number>)[s] ?? -1;
const p110Hv = HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year === 1915);
const p110Errors: string[] = [];
if (p110Hv.length !== 11)
  p110Errors.push(`vpisov 1915 (04105, zasidrani) ≠ 11 (${p110Hv.length})`);
const p110Houses = new Set(p110Hv.map((h) => h.houseNo));
if (p110Houses.size !== 11)
  p110Errors.push(`različnih hiš ≠ 11 (${p110Houses.size}: ${[...p110Houses].sort((a, b) => Number(a) - Number(b)).join(",")}) — NARE 11/11!`);
// NARE 11/11 — brez ponovitev (10. čisto leto; NARE PRELOM samo v NOVI vasi Boginja vas h15 ×2 — ne v Gribljih)
const p110RepeatHouses = [...p110Hv.map((h) => h.houseNo)].filter((hn, i, arr) => arr.indexOf(hn) !== i);
if (p110RepeatHouses.length !== 0)
  p110Errors.push(`intra-letne ponovitve 1915 morajo biti PRAZNE (NARE 11/11) — najdeno: ${p110RepeatHouses.join(",")}`);
// okvir: 2 dup para (270/271 + 273/274); enojni s269/s272/s275–s283
const p110BadPage = p110Hv.filter(
  (h) => h.status !== "DOCUMENTED" || !h.scan || !h.page
    || h.page !== p110PageOfScan(h.scan)
    || h.scan < 269 || h.scan > 283,
);
if (p110BadPage.length > 0)
  p110Errors.push(`scan/page ne ustreza P110 noveli (2 dup para): ${p110BadPage.map((h) => `${h.houseNo}@${h.scan}`).join(",")}`);
// 0 novih hiš (2. leto zapored!)
const p110PriorHouses = new Set(
  HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year < 1915).map((h) => h.houseNo),
);
const p110New = [...p110Houses].filter((hn) => !p110PriorHouses.has(hn));
if (p110New.length !== 0)
  p110Errors.push(`nove hiše 1915 morajo biti PRAZNE (0 — 2. leto zapored!) — najdeno: ${p110New.join(",")}`);
// sidra P110
const p110Pins: Array<[string, string]> = [
  ["88", "P109 lead POTRJEN"], ["88", "Butala"], ["88", "† 20.2.1915"],
  ["45", "Rajhmer"], ["45", "† 25.7.1915"],
  ["70", "1603915505171"], ["70", "PEZDIREC"], ["70", "POPRAVLJENO"],
  ["78", "VRZEL 27 LET"], ["78", "NOV REKORD"], ["78", "1917"],
  ["13", "JAKOBČIČ"], ["13", "POPRAVLJENO"],
  ["40", "† 23.6.1943"], ["40", "Tuvan"],
  ["32", "0211915505717"], ["32", "ŠTRUCELJ"], ["32", "11. VPIS"],
  ["46", "MILEK"], ["46", "RAZVELJAVLJENA"], ["46", "župan"],
  ["9", "Oswald JAKOBČIČ"], ["9", "POPRAVLJENO"],
  ["22", "2511915500090"], ["22", "MILEK ×2"],
  ["53", "1812915500054"], ["53", "ZAPORED 2. LETO"], ["53", "DRAGOS"],
];
for (const [n, pin] of p110Pins) {
  const cur = p110Hv.find((h) => h.houseNo === n);
  if (!cur) {
    p110Errors.push(`pin ${n} (${pin}) — hiša ${n} ni v 1915 blokih`);
    continue;
  }
  if (!cur.whatSi.includes(pin))
    p110Errors.push(`pin hiša ${n} (${pin}) manjka`);
}
// vitals skupaj 490 (po P110: 479 + 11; krstna 1915)
if (HOUSE_VITALS.length !== 685)
  p110Errors.push(`HOUSE_VITALS ≠ 490 (${HOUSE_VITALS.length})`);
// babica: 11/11 imenovanih; Jakofčič 10/11 (r72 Jakobčič!)
if (p110Hv.filter((h) => h.whatSi.includes("babica")).length !== 11)
  p110Errors.push(`babica ni v vseh 11 whatSi (${p110Hv.filter((h) => h.whatSi.includes("babica")).length})`);
const p110Jakofcic = p110Hv.filter((h) => h.whatSi.includes("babica Marija Jakofčič")).length;
if (p110Jakofcic !== 9)
  p110Errors.push(`babica Marija Jakofčič ≠ 9× (${p110Jakofcic} — 9/11; r72 Marija Jakobčič!)`);
// podpisi (jasni): Učak ≥8 + Bitnar ≥2
if (p110Hv.filter((h) => h.whatSi.includes("Učak")).length < 8)
  p110Errors.push(`podpis Učak < 8× (${p110Hv.filter((h) => h.whatSi.includes("Učak")).length})`);
if (p110Hv.filter((h) => h.whatSi.includes("Bitnar")).length < 2)
  p110Errors.push(`podpis Bitnar < 2× (${p110Hv.filter((h) => h.whatSi.includes("Bitnar")).length})`);
// EMŠO sidra v blokih: 5 SKLADNA (r16/r67/r74/r78 + netipična [~] r73 ni v Gribljih)
const p110Emso = ["1603915505171", "0211915505717", "2511915500090", "1812915500054"];
for (const emso of p110Emso) {
  if (!p110Hv.some((h) => h.whatSi.includes(emso)))
    p110Errors.push(`EMŠO sidro ${emso} manjka`);
}
// P111 lead: glava 1916 INLINE v ločilni celici str. 237 + r81 rojstvo/krsta čez mejo (v whatEn/whatSi ni — samo opomba v p111Lead dokumentu) → sidro: glava 1916 + OFFSET
if (!p110Hv.some((h) => h.houseNo === "53" && h.whatSi.includes("Dragos")))
  p110Errors.push("P111 lead sidro (h78/h53 Dragos) manjka");
push(
  "qa-p110-parish-baptism-1915",
  "P110: ŽUPNIJA PODZEMELJ — KRSTNA KNJIGA 04105, POLNO LETO 1915 (issue #18; SAMPLE-TRANSCRIPTION-1915; MERI, NE odloča; v7 join nespremenjen): širitev vzorca P79 (1886) → … → P108 (1913) → P109 (1914) na leto 1915 — **2. VOJNO leto (81 vpisov — višje od 1914 = 93!)** — okvir: glava »1915« ročno na VRHU str. 225 = s269 (P109 lead POTRJEN!) == tiskane strani 225–237 (81 vpisov) == skeni 269–283 (15 skenov; **2 dup para: 270/271 + 273/274** — s271 DUP RAZKRIVA r13 Boršt 22 (s270 pokrit z nalepko!), s274 razkriva r30); **r81 = rojstvo 30.12.1915 / krsta 4.1.1916 — ČEZ MEJO LETA** (EMŠO 3012915505170!); **glava 1916 ročno »1916.« INLINE v LOČILNI starševski celici str. 237 = s283** (zrcali tiskani »Leto« header!) + tiskana glava »Leto 1916« = vrh str. 238 = s284; **OFFSET PORAVNAVA str. 237 (5 celic = 5 vrstic + s284-B kontrola: r4 starši = Matija Muc × Katarina Gregorič!) — P111 lead POPRAVLJEN (1916 r1 ← Matija Šapič × Katarina Novak, ne Copri!)**; VSI vpisi z Griblji: **11 vpisov / 11 hiš — NARE 11/11 (10. čisto leto!)** + **0 NOVIH hiš (2. leto zapored!)** + **h53 ZAPORED 2. leto (1914+1915)** + **h78 VRZEL 27 LET = NOV REKORD vzorca!** (prej h53 16); PT 8/3 (h45+h46+h53 dokazane v luknji); kumulativ **498 vpisov / 87 hiš čez tri knjige in 30 let** (1886–1915; 490 vitals); SIDRA: r8 **GRIBLJE 88 Ivana** (P109 lead POTRJEN; starši Peter Brinec bajt. × Ana **Butala** — POPRAVLJENO; † 20.2.1915 [~] star ~1 mesec!) + r15 **Griblje 45 Zora Jožefa** († 25.7.1915 dobenček; oče Franc Rajhmer? [~]) + r16 **Griblje 70 Barbara** (EMŠO 1603915505171 — POPRAVLJENO iz 5505141; mati **PEZDIREC** — POPRAVLJENO iz Perdivec!; oče roj. 1883 — POPRAVLJENO iz 1888; marg. »mož umrl 1994« — POPRAVLJENO iz »oče«!) + r17 **Griblje 78 Jožefa** (‡ 10.9.**1917** — P109 lead 1916 ZAVRŽENO; **VRZEL 27 LET = REKORD!**) + r48 **Griblje 13 Ana** (oče Matija **JAKOBČIČ** — POPRAVLJENO iz Jaklič; star 59!) + r66 **Griblje 40 Marija Ana** († 23.6.1943!) + r67 **Griblje 32 Marija** (EMŠO 0211915505717; botra Barbara **ŠTRUCELJ** — mreža!; 11. VPIS!) + r69 **Griblje 46 Martin** (mati Katarina **MILEK**; boter **župan** Želejko? [~]; **zakonska zveza RAZVELJAVLJENA sodba K 757/65-10 Karlovci 2.12.1965 — prva v vzorcu!**) + r72 **Griblje 9 Neža** (oče **Oswald Jakobčič** [~ — POPRAVLJENO]; babica Marija Jakobčič = familija Jakobčič!) + r74 **Griblje 22 Nikolaj** (EMŠO 2511915500090; **MILEK ×2 v 1915!**; umrl 24.4.**1992** — POPRAVLJENO iz 1932) + r78 **Griblje 53 Janez** (EMŠO 1812915500054; **DRAGOS** familija; marg. odločba Ljubljana 16.3.1948 pravnomočna [~]); **VELIKE NOVELE 1915: DVA para dvojčkov (3. leto zapored!)** — r37/r38 Boršt 23 Antonija+Alojzij (oče ‡ Mihael **Perdivec** † 28.3.1915 = **MAREC — 2 meseca PRED rojstvom dvojčkov!** (faza-1 »november« POPRAVLJENO); roj. 22.11.**1873** v OBEH celicah — kolizija REŠENA!) + r46/r47 Krasinec 18 Anton+Alojzij (**marg. LATINSKE URE: »½ 7h ante meridiem« + »7h a.m.« = PRVE URE ROJSTVA V VZORCU!**; oba † 1915 kot dojenčka — 18 dni / 8 dni!) + **3 MARGINALIJE OČETOVSTVA = NAJVEČ v enem letu** (r34 Janez Križan 4.2.1918 — mati Marija Galovec — **+ VEZAVA: ISTI Križan = oče r41!** + r43 Jožef Željko 15.8.1918 — poroka 6.1.1918 + r53 Josip Jager, sobni slikar, **18.4.1917 + poroka ISTI DAN** — faza-1 »1918« POPRAVLJENO) + **5 nezakonskih** (r34/r43/r53/r73/r79) + **r49 PROTESTANT** (oče Bohumil Špoušek? [~] »evang. reform.« = edini v vzorcu! × katol. Trobec; trojno ime Emil Filip Leopold) + **2 očeta † 1915** (r30 Daniel Jakša mizar 9.12. + r37/38 Perdivec 28.3. = 3 otroci brez očeta!) + **r40 RAZGLAŠEN ZA MRTVEGA** (17.6.1942 — cf. P96 r60; oče **Ludovik Schweiger Kamnossek** plemiški + botra Jakob Stipanič **ŽUPAN**!) + **NOVI KRAJI: GRM (»Gm« okrajšava ×3 — POTRJENO iz matičnega območja v parish.ts!) + BOGINJA vas (register »Božinja vas« ×2)** + **NARE PRELOM v Boginja vas 15 ×2 (r56 Brodarič × Šuštarič + r70 Kralj × Berkopce — d41 4× POTRJENO — 3. prelom vzorca!)** + **UREJENOST PO KRSTI dokazana** (r12 krsta 3.3. = r11; prečrtan »April« = pisarjev false start — d6a!) + r21 kraj »Gradac/Vrhhova?« [~] dvom + r59 hiša 2? [~] (marg Maticar prekriva) + **EMŠO kampanja ~38 = NAJVEČJA doslej** (5 SKLADNIH sidr v Gribljih + r81 čez mejo!) + DUHOVNIKI: **Učak ~59 DOMINANTA + Kapl. Bitnar ~21** (r1 podpis svinčnik REŠEN — d16b!); BABICA: **PILETIČ ~40/81 DOMINANTA — vrnitev po Jakofčič 2-letni dominanti!** (Jakofčič 10/11 Griblje + Marentič ~15) + **† 1915–1918 ~25% od 81 (VOJNA SMRTNOST!)** + železniška tema (r58 botra želež. delavec + r81 oče želežniški čuvaj + botra žel. uslužbenec) + r51/r80 priimki spremenjeni (odločbi 1999/1973) + EXCLUDED: 70; skripta scripts/p110_parish_baptism_1915.py (I1–I12, --check); status SAMPLE-TRANSCRIPTION-1915",
  "P110: PARISH OF PODZEMELJ — BAPTISM REGISTER 04105, THE FULL YEAR 1915 (issue #18; SAMPLE-TRANSCRIPTION-1915; MEASURES, does not decide; the v7 join unchanged): extending the sample P79 (1886) → … → P109 (1914) to the year 1915 — **the 2nd WAR year (81 entries — HIGHER than 1914's 78!)** — the frame: the 1915 heading manually at the TOP of p. 225 = s269 (the P109 lead CONFIRMED!) == printed pages 225–237 (81 entries) == scans 269–283 (15 scans; **2 dup pairs: 270/271 + 273/274** — s271 REVEALS r13 Boršt 22 (s270 covered by a label!), s274 reveals r30); **r81 = born Dec 30, 1915 / baptized Jan 4, 1916 — ACROSS THE YEAR BOUNDARY** (personal ID 3012915505170!); **the 1916 heading manually »1916.« INLINE in the SEPARATOR parents cell of p. 237 = s283** (mirroring the printed »Leto« header!) + the printed heading »Leto 1916« at the TOP of p. 238 = s284; **the OFFSET ALIGNMENT of p. 237 (5 cells = 5 rows + the s284-B control: r4 parents = Matija Muc × Katarina Gregorič!) — the P111 lead CORRECTED (1916 r1 ← Matija Šapič × Katarina Novak, not Copri!)**; ALL Griblje entries: **11 entries / 11 houses — NARE 11/11 (the 10th clean year!)** + **0 NEW houses (the 2nd consecutive year!)** + **h53 CONSECUTIVE the 2nd year (1914+1915)** + **h78 a 27-YEAR GAP = the NEW RECORD of the sample!** (previously h53's 16); the PT 8/3 (h45+h46+h53 proven in the gap); the cumulative **498 entries / 87 houses across three books and 30 years** (1886–1915; 490 vitals); ANCHORS: r8 **GRIBLJE 88 Ivana** (the P109 lead CONFIRMED; parents Peter Brinec cottager × Ana **Butala** — CORRECTED; died Feb 20, 1915 [~] aged ~1 month!) + r15 **Griblje 45 Zora Jožefa** (died Jul 25, 1915 an infant; father Franc Rajhmer? [~]) + r16 **Griblje 70 Barbara** (personal ID 1603915505171 — CORRECTED from 5505141; the mother **PEZDIREC** — CORRECTED from Perdivec!; the father born 1883 — CORRECTED from 1888; the marginal »the husband died 1994« — CORRECTED from »father«!) + r17 **Griblje 78 Jožefa** (died Sep 10, **1917** — the P109 lead 1916 REJECTED; **a 27-YEAR GAP = the RECORD!**) + r48 **Griblje 13 Ana** (the father Matija **JAKOBČIČ** — CORRECTED from Jaklič; aged 59!) + r66 **Griblje 40 Marija Ana** (died Jun 23, 1943!) + r67 **Griblje 32 Marija** (personal ID 0211915505717; the godmother Barbara **ŠTRUCELJ** — the network!; the 11th entry!) + r69 **Griblje 46 Martin** (the mother Katarina **MILEK**; the godfather a **mayor** Želejko? [~]; **the marriage ANNULLED by the court ruling K 757/65-10 Karlovac Dec 2, 1965 — the first in the sample!**) + r72 **Griblje 9 Neža** (the father **Oswald Jakobčič** [~ — CORRECTED]; the midwife Marija Jakobčič = the Jakobčič family!) + r74 **Griblje 22 Nikolaj** (personal ID 2511915500090; **MILEK ×2 in 1915!**; died Apr 24, **1992** — CORRECTED from 1932) + r78 **Griblje 53 Janez** (personal ID 1812915500054; the **DRAGOS** family; the marginal: the Ljubljana decision of Mar 16, 1948 became final [~]); **THE BIG 1915 NOVELS: TWO twin pairs (the 3rd consecutive year!)** — r37/r38 Boršt 23 Antonija+Alojzij (the father ‡ Mihael **Perdivec** died Mar 28, 1915 = **MARCH — 2 months BEFORE the twins' birth!** (the phase-1 »November« CORRECTED); born Nov 22, **1873** in BOTH cells — the collision RESOLVED!) + r46/r47 Krasinec 18 Anton+Alojzij (**the marginal LATIN BIRTH HOURS: »½ 7h ante meridiem« + »7h a.m.« = THE FIRST BIRTH HOURS OF THE SAMPLE!**; both died in 1915 as infants — 18 days / 8 days!) + **3 PATERNITY MARGINALIA = the most in one year** (r34 Janez Križan Feb 4, 1918 — the mother Marija Galovec — **+ the LINK: the SAME Križan = r41's father!** + r43 Jožef Željko Aug 15, 1918 — the marriage Jan 6, 1918 + r53 Josip Jager, a room painter, **Apr 18, 1917 + the marriage THE SAME DAY** — the phase-1 »1918« CORRECTED) + **5 illegitimates** (r34/r43/r53/r73/r79) + **r49 A PROTESTANT** (the father Bohumil Špoušek? [~] »evang. reform.« = the only one in the sample! × the Catholic Trobec; the triple name Emil Filip Leopold) + **2 fathers died 1915** (r30 Daniel Jakša a joiner Dec 9 + r37/38 Perdivec Mar 28 = 3 children without a father!) + **r40 DECLARED DEAD** (Jun 17, 1942 — cf. P96 r60; the father **Ludovik Schweiger Kamnossek** noble + the godparent Jakob Stipanič **MAYOR**!) + **NEW PLACES: GRM (the »Gm« abbreviation ×3 — CONFIRMED from the parish territory in parish.ts!) + BOGINJA vas (the register's »Božinja vas« ×2)** + **the NARE BREAK at Boginja vas 15 ×2 (r56 Brodarič × Šuštarič + r70 Kralj × Berkopce — d41 4× CONFIRMED — the 3rd break of the sample!)** + **the ORDERING BY BAPTISM DATE proven** (r12 baptized Mar 3 = r11; the struck »April« = the scribe's false start — d6a!) + r21 the place »Gradac/Vrhhova?« [~] doubt + r59 house 2? [~] (the Maticar marginal covers it) + **the personal-ID campaign ~38 = the LARGEST so far** (5 CONSISTENT anchors in Griblje + r81 across the boundary!) + PRIESTS: **Učak ~59 THE DOMINANT + Kapl. Bitnar ~21** (r1's pencil signature RESOLVED — d16b!); MIDWIFE: **PILETIČ ~40/81 THE DOMINANT — a return after Jakofčič's 2-year dominance!** (Jakofčič 10/11 Griblje + Marentič ~15) + **deaths 1915–1918 ~25% of 81 (WAR MORTALITY!)** + the railway theme (r58's godfather a railway worker + r81's father a railway guard + the godfather a railway employee) + r51/r80 surnames changed (the 1999/1973 decrees) + EXCLUDED: 70; the script scripts/p110_parish_baptism_1915.py (I1–I12, --check); status SAMPLE-TRANSCRIPTION-1915",
  p110Errors.length === 0,
  p110Errors.length === 0
    ? `11 vpisov / 11 hiš — NARE 11/11 (10. čisto leto!) · **0 NOVIH hiš (2. leto zapored!)** · h53 ZAPORED (1914+15) · **h78 VRZEL 27 LET = NOV REKORD!** · okvir 1915: str. 225–237 = s269–s283 (81 vpisov; 2 dup para; **r81 rojstvo 30.12.1915 / krsta 4.1.1916 čez mejo!**) + **glava 1916 INLINE v ločilni celici + OFFSET poravnava (5=5; P111 lead POPRAVLJEN!)** · NOVELE: **2 para dvojčkov (r37/38: oče † 28.3.1915 PRED rojstvom! + r46/47: LATINSKE URE rojstva — prvič!)** · **3 očetovstva (r34+r41 ISTI Križan! r43 Željko + poroka 6.1.1918! r53 Jager + poroka ISTI DAN 18.4.1917!)** · 5 nezakonskih · **r49 PROTESTANT (evang. reform.)** · 2 očeta † 1915 · r40 RAZGLAŠEN ZA MRTVEGA (oče Schweiger Kamnossek + botra ŽUPAN!) · **GRM (»Gm« ×3) + BOGINJA vas = novi kraji** · **NARE PRELOM Boginja vas 15 ×2 (3.!)** · EMŠO ~38 = NAJVEČJA kampanja (5 sidr SKLADNIH!) · r16 POPRAVKI (PEZDIREC + EMŠO + 1883 + mož) · r48/r72 JAKOBČIČ · r17 ‡ 1917 (lead 1916 ZAVRŽEN) · r74 † 1992 (POPRAVLJENO) · Učak ~59 + Bitnar ~21 · **babica PILETIČ ~40/81 vrnitev** · **† ~25% (vojna!)** · EXCLUDED 70 · vitals 490 · kumulativ 498/87 30 let`
    : p110Errors.join("; "),
);

// ——— qa-p111: župnija Podzemelj — krstna 1916 (P111; issue #18) ———
const p111PageOfScan = (s: number) =>
  ({ 283: 237, 284: 238, 285: 239, 286: 240, 287: 241, 288: 242, 289: 243, 290: 244 } as Record<number, number>)[s] ?? -1;
const p111Hv = HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year === 1916);
const p111Errors: string[] = [];
if (p111Hv.length !== 6)
  p111Errors.push(`vpisov 1916 (04105, zasidrani) ≠ 6 (${p111Hv.length})`);
const p111Houses = new Set(p111Hv.map((h) => h.houseNo));
if (p111Houses.size !== 6)
  p111Errors.push(`različnih hiš ≠ 6 (${p111Houses.size}: ${[...p111Houses].sort((a, b) => Number(a) - Number(b)).join(",")}) — NARE 6/6!`);
const p111RepeatHouses = [...p111Hv.map((h) => h.houseNo)].filter((hn, i, arr) => arr.indexOf(hn) !== i);
if (p111RepeatHouses.length !== 0)
  p111Errors.push(`intra-letne ponovitve 1916 morajo biti PRAZNE (NARE 6/6) — najdeno: ${p111RepeatHouses.join(",")}`);
// okvir: NIČ dup parov (prvo leto od P106!) — stroga stran == sken − 46
const p111BadPage = p111Hv.filter(
  (h) => h.status !== "DOCUMENTED" || !h.scan || !h.page
    || h.page !== p111PageOfScan(h.scan)
    || h.scan < 283 || h.scan > 290,
);
if (p111BadPage.length > 0)
  p111Errors.push(`scan/page ne ustreza P111 noveli (0 dup parov; − 46): ${p111BadPage.map((h) => `${h.houseNo}@${h.scan}`).join(",")}`);
// 1 nova hiša: SAMO h82 (1. vpis v vseh treh knjigah — prekinjena 0-seriji P109/P110!)
const p111PriorHouses = new Set(
  HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year < 1916).map((h) => h.houseNo),
);
const p111New = [...p111Houses].filter((hn) => !p111PriorHouses.has(hn)).sort();
if (p111New.length !== 1 || p111New[0] !== "82")
  p111Errors.push(`nove hiše 1916 morajo biti točno ["82"] (h82 = 1. vpis v vseh knjigah!) — najdeno: ${p111New.join(",")}`);
// sidra P111
const p111Pins: Array<[string, string]> = [
  ["34", "1. GRIBLJE vrstica 1916"], ["34", "Učak"], ["34", "26.8.1917"], ["34", "VRZEL 3 LETA"],
  ["12", "2. GRIBLJE"], ["12", "TOTER"], ["12", "VRZEL 4 LETA"],
  ["82", "3. GRIBLJE"], ["82", "NOVA HIŠA"], ["82", "majnik"], ["82", "TESARSKI MOJ."],
  ["36", "4. GRIBLJE"], ["36", "2205916500023"], ["36", "1983"], ["36", "ŠTRAUS"],
  ["88", "5. GRIBLJE"], ["88", "ZAPORED 2. LETO"], ["88", "Butala"],
  ["37", "6. GRIBLJE"], ["37", "in utero"], ["37", "VRZEL 19 LET"], ["37", "MRTVOROJEN"],
];
for (const [n, pin] of p111Pins) {
  const cur = p111Hv.find((h) => h.houseNo === n);
  if (!cur) {
    p111Errors.push(`pin ${n} (${pin}) — hiša ${n} ni v 1916 blokih`);
    continue;
  }
  if (!cur.whatSi.toLowerCase().includes(pin.toLowerCase()))
    p111Errors.push(`pin hiša ${n} (${pin}) manjka`);
}
// vitals skupaj 496 (po P111: 490 + 6; krstna 1916)
if (HOUSE_VITALS.length !== 685)
  p111Errors.push(`HOUSE_VITALS ≠ 496 (${HOUSE_VITALS.length})`);
// babice 6/6 imenovanih: Jakofčič ×2 (r22/r23) + Adlešič ×2 + Muc + Marentič
if (p111Hv.filter((h) => h.whatSi.includes("babica")).length !== 6)
  p111Errors.push(`babica ni v vseh 6 whatSi (${p111Hv.filter((h) => h.whatSi.includes("babica")).length})`);
const p111Jakofcic = p111Hv.filter((h) => h.whatSi.includes("babica Marija Jakofčič")).length;
if (p111Jakofcic !== 2)
  p111Errors.push(`babica Marija Jakofčič ≠ 2× (${p111Jakofcic} — 2/6; Piletič 0 v Gribljih — konec P110 dominante!)`);
// podpisi (jasni): Učak ≥4 (r10/r22/r23/r26; r21 dvom; r41 PRAZNO)
if (p111Hv.filter((h) => h.whatSi.includes("Učak")).length < 4)
  p111Errors.push(`podpis Učak < 4× (${p111Hv.filter((h) => h.whatSi.includes("Učak")).length})`);
// EMŠO sidro: r23 = 2205916500023 (ZOOM 4.5× jasno)
if (!p111Hv.some((h) => h.whatSi.includes("2205916500023")))
  p111Errors.push("EMŠO sidro 2205916500023 (h36) manjka");
// mrtvorojeni protokoli: h37 MRTVOROJEN + in utero + VRZEL 19 LET
if (!p111Hv.some((h) => h.houseNo === "37" && h.whatSi.includes("MRTVOROJEN") && h.whatSi.includes("in utero")))
  p111Errors.push("mrtvorojeni protokol (h37 Marko in utero) manjka");
// P112 lead sidro: zaključna opomba 41 na h37 bloku
if (!p111Hv.some((h) => h.houseNo === "37" && h.whatSi.includes("I številko 41")))
  p111Errors.push("P112 lead sidro (h37 zaključna opomba 41) manjka");
push(
  "qa-p111-parish-baptism-1916",
  "P111: ŽUPNIJA PODZEMELJ — KRSTNA KNJIGA 04105, POLNO LETO 1916 (issue #18; SAMPLE-TRANSCRIPTION-1916; MERI, NE odloča; v7 join nespremenjen): širitev vzorca P79 (1886) → … → P109 (1914) → P110 (1915) na leto 1916 — **2. VOJNO leto; 41 vpisov = NAJNIŽE doslej (polovica 1915!)** — okvir: **glava »1916« ročno INLINE sredi str. 237 = s283-B** (P110 lead POTRJEN!) + tiskana glava »Leto 1916« = vrh str. 238 = s284; == strani 237–244 == skeni 283–290 (8 skenov; str. == sken − 46); **NIČ DUP PAROV — prvo leto od P106!** (»Stran« zapored 237–245); **r28 + r29 = DVOJNI VPIS istega mrtvorojenega otroka** (Krasinec 8: r28 »Mrtvorojena« brez krsta + r29 »Neža Cajnar« »krščena v sili« = ISTA OSEBA — NOV PROTOKOL!) + **r41 = GRIBLJE 37 Marko mrtvorojen + krsta kolona »krščena v sili in utero m.« = NUJNI KRST V MATERNICI — PRVI V VZORCU!** (enovrstični model — 2 protokola mrtvorojenih v istem letu!); **zaključna opomba »I številko 41 zaključeno število porodov oz. krstov v l. 1916.« + podpis O. Mučah? / ozd. leut? [~ matičar?]**; VSI vpisi z Griblji: **6 vpisov / 6 hiš — NARE 6/6 (11. čisto leto!) + 1 NOVA hiša h82** (1. vpis v vseh treh knjigah — prekinjena 0-seriji P109/P110!) + **h88 ZAPORED 2. leto** (Brinec bajtar × Butala: 1915 Ivana + 1916 Neža — ISTI botri Janez + Doroteja Brinec — familija ×3!) + h36 ZAPORED familija (botrinja Marjeta **ŠTRAUS** — cf. P107 h36 par Hrižan × Štraus!) + **h37 VRZEL 19 LET** (1895, 1897 → 1916 — 2. najdaljša po h78 27! — in njen edini 1916 vpis je MRTVOROJEN!); PT 6/0 (vseh 6 v naboru!); kumulativ **539 vpisov / 88 hiš čez tri knjige in 31 let** (1886–1916; 496 vitals); SIDRA: r10 **GRIBLJE 34 Barbara** († 26.8.1917 dojenček; oče Nikolaj Silak? [~]; 10. VPIS — VRZEL 3) + r21 **Griblje 12 Vincencij** (botrinja Marija **TOTER** — cf. P109 r62!; 14. VPIS — VRZEL 4) + r22 **Griblje 82 Ana** (**NOVA HIŠA!**; oče Peter Vrebec? **TESARSKI MOJ.** — nov poklic!; mesec glava **»majnik«** = idiosinkrazija; prečrtan false start) + r23 **Griblje 36 Anton** (EMŠO **2205916500023** ZOOM ✓; umrl 19.12.**1983** — POPRAVLJENO iz 1980; 2. poroka marg; 12. VPIS — VRZEL 3) + r26 **Griblje 88 Neža** († 9/7 1916 dojenček ~1 teden!) + r41 **Griblje 37 Marko** (**MRTVOROJEN + in utero!**; zap. 41 = zadnja); **NOVELE 1916: r31 DVOJNA hiša 25/32 + DVOJNO ime Alojzij Franc** (prva dvojna hiša!) + **ŽELEZNIŠKA TEMA ×3** (r31 Kok žel. usluž. + r37 oče Škravara žel. del. + boter Edvard Župančič žel. del.-sam.; **starši r37 poročeni 11.6.1916 = 5 mesecev pred krstom!**) + **mesec glavi »marcij« (latinsko!) + »majnik« (idiosinkrazija)** + nezakonska r35 (mati Stipanič sam. hči + RAZGLAŠENA marg modra!) + **vojna smrtnost otrok ~18/41 = 44% EKSTREMUM** + starost očetov r6 (1832 — star 84??) + r19 (1859 — star 57??) + **podpisna uganka Učak/Bitnar/Muh 07/Mučah** (možen 5. duhovnik!) + EMŠO kampanja 12 kandidatov (2 ZOOM sidra!); DUHOVNIKI: Učak jasni ~8 + P?h?us Bitnar [~] + Muh? 07 [~]; BABICA: Jakofčič 2/6 + Adlešič 2/6 (**Piletič 0 v Gribljih — konec P110 dominante!**); EXCLUDED: 35; skripta scripts/p111_parish_baptism_1916.py (I1–I12, --check **14/14 PASS**); status SAMPLE-TRANSCRIPTION-1916",
  "P111: PARISH OF PODZEMELJ — BAPTISM REGISTER 04105, THE FULL YEAR 1916 (issue #18; SAMPLE-TRANSCRIPTION-1916; MEASURES, does not decide; the v7 join unchanged): extending the sample P79 (1886) → … → P110 (1915) to 1916 — **the 2nd WAR year; 41 entries = THE LOWEST so far (half of 1915!)** — the frame: **the 1916 heading manually INLINE in the middle of p. 237 = s283-B** (the P110 lead CONFIRMED!) + the printed heading at the top of p. 238 = s284; == pages 237–244 == scans 283–290 (8 scans; page == scan − 46); **NO DUP PAIRS — the first year since P106!**; **r28 + r29 = a DOUBLE ENTRY of the same stillborn child** (Krasinec 8: r28 »Mrtvorojena« without baptism + r29 »Neža Cajnar« »baptized in emergency« = the SAME PERSON — a NEW PROTOCOL!) + **r41 = GRIBLJE 37 Marko stillborn + the baptism column »baptized in emergency in utero matris« = an EMERGENCY IN-WOMB BAPTISM — THE FIRST IN THE SAMPLE!** (a single-row model — 2 stillbirth protocols in one year!); **the closing note »With number 41 the count of births/baptisms in 1916 is concluded.« + the signature O. Mučah? / ozd. leut? [~ registrar?]**; ALL Griblje entries: **6 entries / 6 houses — NARE 6/6 (the 11th clean year!) + 1 NEW house h82** (the 1st entry in all three books — the 0-series of P109/P110 broken!) + **h88 CONSECUTIVE the 2nd year** (Brinec × Butala: 1915 Ivana + 1916 Neža — the SAME godparents — the family ×3!) + h36 family consecutive (godmother Marjeta **ŠTRAUS** — cf. the P107 h36 pair!) + **h37 a 19-YEAR GAP** (1895, 1897 → 1916 — the 2nd longest after h78's 27! — and its only 1916 entry is STILLBORN!); the PT 6/0 (all 6 in the set!); the cumulative **539 entries / 88 houses across three books and 31 years** (1886–1916; 496 vitals); ANCHORS: r10 **GRIBLJE 34 Barbara** (died Aug 26, 1917 an infant; the 10th ENTRY — a 3-year gap) + r21 **Griblje 12 Vincencij** (the godmother Marija **TOTER**; the 14th ENTRY — a 4-year gap) + r22 **Griblje 82 Ana** (**THE NEW HOUSE!**; the father Peter Vrebec? a **CARPENTER MASTER** — a new trade!; the month heading **»majnik«** = an idiosyncrasy; a crossed-out false start) + r23 **Griblje 36 Anton** (personal ID **2205916500023** ZOOM ✓; died Dec 19, **1983** — CORRECTED from 1980; a 2nd marriage marginal; the 12th ENTRY) + r26 **Griblje 88 Neža** (died 9/7 1916 an infant ~1 week!) + r41 **Griblje 37 Marko** (**STILLBORN + in utero!**; serial 41 = the last); **THE 1916 NOVELS: r31 a DOUBLE house number 25/32 + the DOUBLE name Alojzij Franc** (the first double house!) + **the RAILWAY theme ×3** (r31 Kok + r37 Škravara + the godfather Edvard Župančič; **r37's parents married Jun 11, 1916 = 5 months before the baptism!**) + **the month headings »marcij« (Latin!) + »majnik« (idiosyncrasy)** + the illegitimate r35 (the mother Stipanič an unmarried daughter + a DECLARED-DEAD blue marginal!) + **the war child mortality ~18/41 = 44% THE EXTREMUM** + the fathers' ages r6 (1832 — aged 84??) + r19 (1859 — aged 57??) + **the signature puzzle Učak/Bitnar/Muh 07/Mučah** (a possible 5th priest!) + the personal-ID campaign 12 candidates (2 ZOOM anchors!); PRIESTS: Učak clear ~8 + P?h?us Bitnar [~] + Muh? 07 [~]; MIDWIFE: Jakofčič 2/6 + Adlešič 2/6 (**Piletič 0 in Griblje — the end of the P110 dominance!**); EXCLUDED: 35; the script scripts/p111_parish_baptism_1916.py (I1–I12, --check **14/14 PASS**); status SAMPLE-TRANSCRIPTION-1916",
  p111Errors.length === 0,
  p111Errors.length === 0
    ? `6 vpisov / 6 hiš — NARE 6/6 (11. čisto leto!) · **1 NOVA hiša h82** (1. vpis v vseh knjigah!) · h88 ZAPORED (Brinec ×3!) · **h37 VRZEL 19 LET (2. najdaljša!) — edini vpis MRTVOROJEN** · okvir 1916: str. 237–244 = s283–s290 (41 vpisov — NAJNIŽE!; **NIČ dup parov — prvo leto od P106!**; glava 1916 INLINE s283-B) · **r28+r29 DVOJNI VPIS mrtvorojenega (nov protokol!) + r41 in-utero krst (prvi v vzorcu!)** · **zaključna opomba 41 + podpis O. Mučah? [~]** · NOVELE: **r31 dvojna hiša 25/32 + dvojno ime + žel. usluž.** · **železniška tema ×3 (poroka ISTO LETO!)** · **glavi »marcij« + »majnik«** · nezakonska r35 razglašena · **† ~44% = EKSTREMUM** · EMŠO 2205916500023 ✓ · r23 umrl **1983** POPRAVLJENO · Učak/Bitnar/Muh 07/Mučah uganka · Jakofčič 2/6 (Piletič 0!) · EXCLUDED 35 · vitals 496 · kumulativ 539/88 31 let`
    : p111Errors.join("; "),
);

// ——— qa-p112: župnija Podzemelj — krstna 1917 (P112; issue #18) ———
const p112PageOfScan = (s: number) =>
  ({ 291: 245, 292: 246, 293: 247, 294: 248, 295: 249, 296: 250, 297: 251, 298: 252, 299: 253 } as Record<number, number>)[s] ?? -1;
const p112Hv = HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year === 1917);
const p112Errors: string[] = [];
if (p112Hv.length !== 12)
  p112Errors.push(`vpisov 1917 (04105, zasidrani) ≠ 12 (${p112Hv.length})`);
const p112Houses = new Set(p112Hv.map((h) => h.houseNo));
if (p112Houses.size !== 11)
  p112Errors.push(`različnih hiš ≠ 11 (${p112Houses.size}: ${[...p112Houses].sort((a, b) => Number(a) - Number(b)).join(",")}) — NARE 12/12!`);
const p112RepeatHouses = [...p112Hv.map((h) => h.houseNo)].filter((hn, i, arr) => arr.indexOf(hn) !== i);
if (p112RepeatHouses.join(",") !== "24")
  p112Errors.push(`intra-letne ponovitve 1917 morajo biti TOČNO [24] (dvojčka r26+r27!) — najdeno: ${p112RepeatHouses.join(",")}`);
// okvir: NIČ dup parov (2. leto!) — stroga stran == sken − 46
const p112BadPage = p112Hv.filter(
  (h) => h.status !== "DOCUMENTED" || !h.scan || !h.page
    || h.page !== p112PageOfScan(h.scan)
    || h.scan < 291 || h.scan > 299,
);
if (p112BadPage.length > 0)
  p112Errors.push(`scan/page ne ustreza P112 noveli (0 dup parov; − 46): ${p112BadPage.map((h) => `${h.houseNo}@${h.scan}`).join(",")}`);
// 0 novih hiš (3. zapored!): vseh 11 ima zgodnejše vpise
const p112PriorHouses = new Set(
  HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year < 1917).map((h) => h.houseNo),
);
const p112New = [...p112Houses].filter((hn) => !p112PriorHouses.has(hn)).sort();
if (p112New.length !== 0)
  p112Errors.push(`nove hiše 1917 morajo biti PRAZNE (3. zapored z 0!) — najdeno: ${p112New.join(",")}`);
// sidra P112
const p112Pins: Array<[string, string]> = [
  ["45", "1. GRIBLJE"], ["45", "jamarija"], ["45", "CEVLJAR"], ["45", "1956"],
  ["62", "2. GRIBLJE"], ["62", "VRZEL 10 LET"], ["62", "18/1 1917"],
  ["14", "3. GRIBLJE"], ["14", "MRTVOROJEN"],
  ["31", "4. GRIBLJE"], ["31", "VPIS PRENEŠEN"], ["31", "23.08.1966"],
  ["24", "5. GRIBLJE"], ["24", "DVOJČEK"], ["24", "2805917500040"],
  ["24", "DVOJČICA"], ["24", "2805917505115"],
  ["46", "7. GRIBLJE"], ["46", "16.7.1928"], ["46", "1859"], ["46", "ŽUPAN"],
  ["5", "8. GRIBLJE"], ["5", "CIGANKA"], ["5", "2207917500054"],
  ["88", "9. GRIBLJE"], ["88", "ZAPORED 3. LETO"], ["88", "9.11.1918"],
  ["77", "10. GRIBLJE"], ["77", "VPIS PRENEŠEN"],
  ["9", "11. GRIBLJE"], ["9", "Ožbald"],
  ["37", "12. GRIBLJE"], ["37", "VPIS PRENEŠEN"], ["37", "0812917505459"],
];
for (const [n, pin] of p112Pins) {
  const blocks = p112Hv.filter((h) => h.houseNo === n);
  if (blocks.length === 0) {
    p112Errors.push(`pin ${n} (${pin}) — hiša ${n} ni v 1917 blokih`);
    continue;
  }
  if (!blocks.some((cur) => cur.whatSi.toLowerCase().includes(pin.toLowerCase())))
    p112Errors.push(`pin hiša ${n} (${pin}) manjka`);
}
// vitals skupaj 508 (po P112: 496 + 12)
if (HOUSE_VITALS.length !== 685)
  p112Errors.push(`HOUSE_VITALS ≠ 533 (${HOUSE_VITALS.length})`);
// babice: Jakofčič ×4 (r18/r35/r41/r43) + Adlešič ×2 (r26/r27) + Piletič 1 (r52)
const p112Jakofcic = p112Hv.filter((h) => h.whatSi.includes("babica Marija Jakofčič")).length;
if (p112Jakofcic !== 4)
  p112Errors.push(`babica Marija Jakofčič ≠ 4× (${p112Jakofcic} — r18/r35/r41/r43; r48 Jakobčič ort. var.)`);
const p112Adlesic = p112Hv.filter((h) => h.whatSi.includes("Bara Adlešič")).length;
if (p112Adlesic !== 2)
  p112Errors.push(`babica Bara Adlešič ≠ 2× (${p112Adlesic} — dvojčka r26/r27!)`);
// podpisi: Učak ≥6 (r18/r26/r27/r35/r41/r43/r48/r52); h14/h37 protokoli
if (p112Hv.filter((h) => h.whatSi.includes("Učak")).length < 6)
  p112Errors.push(`podpis Učak < 6× (${p112Hv.filter((h) => h.whatSi.includes("Učak")).length})`);
// mrtvorojeni protokol: h14 MRTVOROJEN + krsta »—« + VSI »—«
if (!p112Hv.some((h) => h.houseNo === "14" && h.whatSi.includes("MRTVOROJEN")))
  p112Errors.push("mrtvorojeni protokol (h14) manjka");
// h88 ZAPORED 3. LETO sidro
if (!p112Hv.some((h) => h.houseNo === "88" && h.whatSi.includes("ZAPORED 3. LETO")))
  p112Errors.push("h88 ZAPORED 3. LETO sidro manjka");
// P113 lead sidra: 1918 glava + pokrita r3 (Boršt 49 na p113Lead ni blok — sidra so besedilna)
push(
  "qa-p112-parish-baptism-1917",
  "P112: ŽUPNIJA PODZEMELJ — KRSTNA KNJIGA 04105, POLNO LETO 1917 (issue #18; SAMPLE-TRANSCRIPTION-1917; MERI, NE odloča; v7 join nespremenjen): širitev vzorca P79 (1886) → … → P110 (1915) → P111 (1916) na leto 1917 — **3. VOJNO leto; 55 vpisov = ODBOJKA od 41 (+34%)!** — okvir: tiskana glava »Leto 1917« + velika ročna »1917« = VRH str. 245 = s291; == strani 245–253 == skeni 291–299 (9 skenov; str. == sken − 46); **NIČ DUP PAROV — 2. leto zapored!**; **NIČ prekoračitve leta** (1917 se zaključi r55 na str. 253 z opombo **»Š t. 55 je zaključno število porodov oziroma krstov v l. 1917« + podpis O. M. Učak? ord. tout. [~]** — ENAKA formula kot 1916!); VSI vpisi z Griblji: **12 vpisov / 11 hiš — NARE 12/12 (12. čisto leto!) + 0 NOVIH hiš (3. zapored!)** + **h24 ×2 = DVOJČKA r26+r27** (Anton + Ivana, isti dan 28.5.1917, EMŠO oba 2805917 ✓ ZOOM 5×! — 7./8. par vzorca, 4. leto z dvojčki!) + **h88 ZAPORED 3. LETO** (1915+1916+1917 — 1. trojno zaporedje!) + h37 nadaljuje po 1916 mrtvorojencu + **h62 VRZEL 10 LET** (najdaljša aktivna 1917!); PT 9/2 (h45+h46 v luknji 41–60 = PT_GAP_KNOWN); kumulativ **594 vpisov / 88 hiš čez tri knjige in 32 let** (1886–1917; 508 vitals); SIDRA: r1 **GRIBLJE 45 Karol Feliks** (P111 lead POTRJEN!; oče Franc Rajmer? **CEVLJAR** = 1. čevljar-oče!; **RAZVEZANA ZVEZA 1956** — odločba sodišča Ljubljana št. 9.309/356; glava **»jamarija«** = nova idiosinkrazija!) + r3 **Griblje 62 Marija** (‡ 18/1 pri 9 dneh!; boter Ivan Brinc Griblje 10) + r14 **Griblje 14 mrtvorojen** (oče Janez Brinec star 55!; enovrstični protokol — VSI »—«) + r18 **Griblje 31 Ana** (**PEČAT »VPIS PRENEŠEN V MATIČNI REGISTER« 23.08.1966 Ivana Šimunič = 1. od 4 prenosov — NOVELA!**; oče Janez Papič mali posebnik in kolar? [~]) + r26/r27 **Griblje 24 Anton + Ivana** (DVOJČKA!; starši Janez Brinec × Ana Milek — identična celica; 16. VPIS = največkrat vpisana hiša!) + r35 **Griblje 46 Julij** (oče Anton Brodarič? roj. **14.11.1859 = STAR 57–58!**; boter Nikolaj Željko POSEST. IN ŽUPAN!; † 16.7.1928 pri 11 letih) + r37 **Griblje 5 Jakob** (mati **Mara Hudorovac CIGANKA = 1. EKSPlicitNA ETNIČNA OZNAČBA VZORCA!**; oče PRAZNO + brez boter = socialna izolacija!) + r41 **Griblje 88 Katarina** (oče Peter Brinc mali posestnik star 57!; poroka 12.11.1916 = 1. otrok po 8 mes.; **† 9.11.1918 — TEDEN DO KONCA VOJNE!**) + r43 **Griblje 77 Katarina** (pečat 14.11.2007) + r48 **Griblje 9 Janez** (oče **Ožbald Jakobčič = ISTI, ki je boter r1+r41 — 3. vloga v enem letu!**) + r52 **Griblje 37 Marija** (pečat 14.11.2007; **zakonec [Lipovec?] Jože umrl 26.3.1945 = MOŽ † WWII!**); **VELIKE NOVELE 1917: MRTVOROJENI/V-SILI ×3** (r14 + r38 Dobravice + r40 Cerkvišče 25 **»v sili« z IME PRAZNO + babica Piletič »tudi krstila« = babica kot nujna krstnica — 1. eksplicitni dokaz!**) + **RAZGLAŠENI ×3 = REKORD** (r30 Franc Primostek 1971 + r50 Ana Zemelj **RAZGLAŠENA** 1952 + r55 Anton Otok — sklep 31.12.1975, določen 15.5.1946, **»kot član K.B.g. [~] ni preživel«**!) + **BEGUNCI — SOŠKA FRONTA (1. begunski protokol!)** — r54 Trilorje? 16: oče Jakob Obročan? [~] **ZIDAR. MOJSTER, BEGUNEC IZ RENČ(E) ŠT. 296 NA GORIŠKEM** + boter Jožef Nemec **BEGUNEC-POSESTNIK**; družina po vojni VRNJENA na Goriško (poroka 1933 v Renčah + smrti v Volčji Dragi/Bukovica!) + **POSTHUMNO ROJSTVO r39** (oče Janez Novak † 13.5.1917 — 3 mesece pred rojstvom hčere 13.8.1917 — 2. v vzorcu!) + **VPIS PRENEŠEN ×4 pečati** (r18 1966 + r36 MRB 2005 + r43/r52 2007 — kampanja 3 matičark!) + **hiša »ČUVAJ MEČA 34«** (r7 Grišiče — železniška čuvajnica kot hišna številka — nov tip!) + **ŽELEZNIŠKA TEMA ×5 = najmočnejša** (r7 čuvaj+uslužbenec + r8 v Solkanu + r15 + r22 delavec+čuvaj + r46) + **ŽUPAN botri ×3 + kolizija** (r32/r35 Nikolaj Željko + r44 Jakob Stipanič; r22 boter Jožef ŽUPAN želez. čuvaj = priimek!) + **meseci: »jamarija« + »marecij« ×2 + »majnik« + popravek september→oktober (r45 — 1. tak popravek!)** + r8 krsta »feb.« (čez-mesec) + r15 marca→april + **UREJENOST PO KRSTI 2. POTRDITEV** (r54 rojstva 4.12 po r53 12.12, krsta 16. > 13 ✓ — A15 P110 potrjena!) + **EMŠO kampanja 21 (2. največja; datumski ✓ 21/21 po 2 POPRAVKIH: r26/r27 2805! + r37 2207!)** + **SPOLNA ŠIFRA ANOMALIJA M=500/F=505** (12 ženskih z 8. št. = 5 = LIHA = formalno moška!) + **oče STAR 58** (r29 Janez Bohte roj. 10.4.1859 — najstarejši 1917!) + 5 očetov 50+ + **† 13/55 = 23.6% vojna smrtnost** (2 dvojčka † v juniju!) + NOVI poklici (čevljar + lončarski mojster + zidar. mojster begunec + čevljarski mojster) + **familija BRINC ×5** (G10 boter + G14 mrtvorojenec + G24 dvojčka + G88 + Brinec nevesta) + **OŽBALD JAKOFČIČ 3 vloge** (2× boter + 1× oče!) + cross-ref **»glej strani 264« (r20 → str. 264 = s310 = P114 LEAD!)** + DUHOVNIKI: Učak ~37 + **Paulinus Bitnar kaplan JASNO** (r49/r53–r55!) + ornatni dvojnik [~] + zaključna »O. M. Učak?« [~]; BABICA: **PILETIČ ~26/55 vrnitev dominate** + Jakofčič 4/12 Griblje + Adlešič 2/12 (dvojčka!); EXCLUDED: 43; skripta scripts/p112_parish_baptism_1917.py (I1–I12+I5b, --check **14/14 PASS**); status SAMPLE-TRANSCRIPTION-1917",
  "P112: PARISH OF PODZEMELJ — BAPTISM REGISTER 04105, THE FULL YEAR 1917 (issue #18; SAMPLE-TRANSCRIPTION-1917; MEASURES, does not decide; the v7 join unchanged): extending the sample P79 (1886) → … → P110 (1915) → P111 (1916) to 1917 — **the 3rd WAR year; 55 entries = the REBOUND from 41 (+34%)!** — the frame: the printed heading »Leto 1917« + the large manual »1917« at the TOP of p. 245 = s291; == pages 245–253 == scans 291–299 (9 scans; page == scan − 46); **NO DUP PAIRS — the 2nd consecutive year!**; **NO year overflow** (1917 closes with r55 on p. 253 with the note **»With number 55 the count of births/baptisms in 1917 is concluded« + the signature O. M. Učak? [~]** — the SAME formula as 1916!); ALL Griblje entries: **12 entries / 11 houses — NARE 12/12 (the 12th clean year!) + 0 NEW houses (the 3rd consecutive!)** + **h24 ×2 = the TWINS r26+r27** (Anton + Ivana, the same day May 28, 1917, both EMŠO 2805917 ✓ ZOOM 5×! — the 7th/8th pair, the 4th twins year!) + **h88 CONSECUTIVE the 3rd YEAR** (1915+1916+1917 — the 1st triple run!) + h37 continues after the 1916 stillbirth + **h62 a 10-YEAR GAP** (the longest active of 1917!); the PT 9/2 (h45+h46 in the 41–60 hole = PT_GAP_KNOWN); the cumulative **594 entries / 88 houses across three books and 32 years** (1886–1917; 508 vitals); ANCHORS: r1 **GRIBLJE 45 Karol Feliks** (the P111 lead CONFIRMED!; the father Franc Rajmer? a **SHOEMAKER** = the 1st shoemaker-father!; **the DISSOLVED UNION 1956** — the Ljubljana court ruling no. 9.309/356; the heading **»jamarija«** = a new idiosyncrasy!) + r3 **Griblje 62 Marija** (died Jan 18 at 9 days!; the godfather Ivan Brinc Griblje 10) + r14 **Griblje 14 stillborn** (the father Janez Brinec aged 55!; the single-row protocol — ALL »—«) + r18 **Griblje 31 Ana** (the STAMP »ENTRY TRANSFERRED TO THE CIVIL REGISTER« Aug 23, 1966 = the 1st of 4 transfers — a NOVELTY!) + r26/r27 **Griblje 24 Anton + Ivana** (the TWINS!; the identical parents cell; the 16th ENTRY = the most-registered house!) + r35 **Griblje 46 Julij** (the father Anton Brodarič? born **Nov 14, 1859 = AGED 57–58!**; the godfather Nikolaj Željko a LANDOWNER AND MAYOR!; died Jul 16, 1928 aged 11) + r37 **Griblje 5 Jakob** (the mother **Mara Hudorovac, a GYPSY WOMAN = the 1st EXPLICIT ETHNIC LABEL of the sample!**; the father EMPTY + no godparents = social isolation!) + r41 **Griblje 88 Katarina** (the father Peter Brinc aged 57!; married Nov 12, 1916 = the 1st child 8 months on; **died Nov 9, 1918 — A WEEK BEFORE THE END OF THE WAR!**) + r43 **Griblje 77 Katarina** (the stamp Nov 14, 2007) + r48 **Griblje 9 Janez** (the father **Ožbald Jakobčič = the SAME one who is the godfather of r1+r41 — his 3rd role in one year!**) + r52 **Griblje 37 Marija** (the stamp Nov 14, 2007; **the husband [Lipovec?] Jože died Mar 26, 1945 = the HUSBAND † WWII!**); **THE BIG 1917 NOVELS: STILLBIRTHS/IN-EXTREMIS ×3** (r14 + r38 Dobravice + r40 Cerkvišče 25 **»v sili« with the NAME EMPTY + the midwife Piletič »tudi krstila« = the midwife as the emergency baptizer — the 1st explicit proof!**) + **DECLARED DEAD ×3 = the RECORD** (r30 + r50 **a WOMAN** 1952 + r55 — the ruling Dec 31, 1975, declared May 15, 1946, **»as a member of K.B.g. [~] he did not survive«**!) + **REFUGEES — the ISONZO FRONT (the 1st refugee protocol!)** — r54: the father Jakob Obročan? [~] a **MASON MASTER, A REFUGEE FROM RENČ(E) NO. 296 IN THE GORIŠKA** + the godfather Jožef Nemec a **REFUGEE-LANDOWNER**; the family RETURNED to the Goriška after the war (married 1933 in Renče + died in Volčja Draga/Bukovica!) + **the POSTHUMOUS BIRTH r39** (the father Janez Novak died May 13, 1917 — 3 months before the daughter's birth Aug 13, 1917 — the 2nd in the sample!) + **ENTRY TRANSFERRED ×4 stamps** (1966 + MRB 2005 + 2007 ×2 — the campaign of 3 registrar-women!) + **the house »ČUVAJ MEČA 34«** (r7 — a railway watch-hut as a house number — a new type!) + **the RAILWAY theme ×5 = the strongest** + **MAYOR godfathers ×3 + the collision** (r32/r35 Željko + r44 Stipanič; r22's godfather Jožef ŽUPAN = a SURNAME!) + **the months: »jamarija« + »marecij« ×2 + »majnik« + the September→October correction (r45 — the 1st such correction!)** + r8's baptism »feb.« (cross-month) + r15 March→April + **the ORDERING BY BAPTISM DATE 2nd PROOF** (r54 born Dec 4 after r53's Dec 12, but baptized Dec 16 > 13 ✓ — the P110 A15 confirmed!) + **the personal-ID campaign 21 (the 2nd largest; date-check ✓ 21/21 after 2 CORRECTIONS: r26/r27 2805! + r37 2207!)** + **the SEX-CODE ANOMALY M=500/F=505** (12 females with the 8th digit = 5 = ODD = formally male!) + **the father AGED 58** (r29 Janez Bohte born Apr 10, 1859 — the oldest of 1917!) + 5 fathers 50+ + **deaths 13/55 = 23.6% war mortality** (both twins died in June!) + NEW trades (a shoemaker + a potter master + a mason master refugee + a shoemaker master) + **the BRINEC family ×5** + **OŽBALD JAKOFČIČ 3 roles** (2× godfather + 1× father!) + the cross-ref **»see page 264« (r20 → p. 264 = s310 = the P114 LEAD!)** + PRIESTS: Učak ~37 + **Paulinus Bitnar kaplan CLEARLY** (r49/r53–r55!) + the ornate double [~] + the closing »O. M. Učak?« [~]; MIDWIFE: **PILETIČ ~26/55 the dominant return** + Jakofčič 4/12 Griblje + Adlešič 2/12 (the twins!); EXCLUDED: 43; the script scripts/p112_parish_baptism_1917.py (I1–I12+I5b, --check **14/14 PASS**); status SAMPLE-TRANSCRIPTION-1917",
  p112Errors.length === 0,
  p112Errors.length === 0
    ? `12 vpisov / 11 hiš — NARE 12/12 (12. čisto leto!) · **0 NOVIH hiš (3. zapored!)** · **h24 ×2 = DVOJČKA (isti dan, EMŠO 2805917 ×2!)** · **h88 ZAPORED 3. LETO (1. trojno zaporedje!)** · **h62 VRZEL 10 LET** · okvir 1917: str. 245–253 = s291–s299 (55 vpisov — ODBOJKA +34%!; NIČ dup parov — 2. leto!) · **zaključna opomba 55 + podpis O. M. Učak? [~]** · NOVELE: **mrtvorojeni/v-sili ×3 (r40 ime PRAZNO + babica »tudi krstila«!)** · **RAZGLAŠENI ×3 = REKORD (»K.B.g.« 15.5.1946!)** · **BEGUNCI Renče št. 296 (Soška fronta — 1. protokol!)** · **POSTHUMNO r39 (oče † 3 mesece pred rojstvom!)** · **VPIS PRENEŠEN ×4 pečati (NOVELA!)** · **»čuvaj meča 34« (železniška čuvajnica!)** · žel. tema ×5 · **ŽUPAN botri ×3 + ŽUPAN priimek!** · **glave »jamarija« + »marecij« ×2 + »majnik« + popravek sept→okt** · **UREJENOST PO KRSTI 2. POTRDITEV (r54!)** · **EMŠO 21 (✓ 21/21; POPRAVKI 2805+2207!) + šifra M=500/F=505 anomalija** · oče 58 let (Bohte 1859!) · **† 23.6% (oba dvojčka † junij!)** · **CIGANKA mati = 1. etnična označba** · BRINC ×5 · Ožbald 3 vloge · cross-ref str. 264 = P114 lead · **Paulinus Bitnar jasno!** · Piletič ~26/55 vrnitev · EXCLUDED 43 · vitals 508 · kumulativ 594/88 32 let`
    : p112Errors.join("; "),
);
// ——— qa-p113: župnija Podzemelj — krstna 1918 (P113; issue #18) ———
const p113PageOfScan = (s: number) =>
  ({ 300: 254, 301: 254, 302: 255, 303: 256, 304: 257, 305: 258, 306: 258, 307: 259, 308: 260, 309: 261, 310: 262 } as Record<number, number>)[s] ?? -1;
const isSubDioe = (h: string) => h.startsWith("sub dioe.");
const p113Hv = HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year === 1918);
const p113Errors: string[] = [];
if (p113Hv.length !== 9)
  p113Errors.push(`vpisov 1918 (04105, zasidrani) ≠ 9 (${p113Hv.length})`);
const p113Houses = new Set(p113Hv.map((h) => h.houseNo));
const p113Numeric = [...p113Houses].filter((h) => !isSubDioe(h));
if (p113Houses.size !== 9 || p113Numeric.length !== 8)
  p113Errors.push(`hiš 1918 ≠ 9 (8 numeričnih + 1 sub dioe.) — najdeno ${p113Houses.size}/${p113Numeric.length}: ${[...p113Houses].join(",")}`);
const p113Repeat = [...p113Hv.map((h) => h.houseNo)].filter((hn, i, arr) => arr.indexOf(hn) !== i);
if (p113Repeat.length !== 0)
  p113Errors.push(`intra-letne ponovitve 1918 morajo biti PRAZNE — najdeno: ${p113Repeat.join(",")}`);
// dup-novela: stran == sken − 46, RAZEN s301 (dup str. 254) + s306 (dup str. 258)
const p113BadPage = p113Hv.filter(
  (h) => h.status !== "DOCUMENTED" || !h.scan || !h.page
    || h.page !== p113PageOfScan(h.scan)
    || h.scan < 300 || h.scan > 310,
);
if (p113BadPage.length > 0)
  p113Errors.push(`scan/page ne ustreza P113 noveli (2 dup para: s301 + s306!): ${p113BadPage.map((h) => `${h.houseNo}@${h.scan}`).join(",")}`);
// NARE 8/8 (4. čisto leto!): vseh 8 numeričnih ima zgodnejše vpise
const p113Prior = new Set(
  HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year < 1918).map((h) => h.houseNo),
);
const p113New = p113Numeric.filter((hn) => !p113Prior.has(hn)).sort();
if (p113New.length !== 0)
  p113Errors.push(`nove numerične hiše 1918 morajo biti PRAZNE (4. zapored z 0!) — najdeno: ${p113New.join(",")}`);
// sub dioe. natanko 1 v Gribljih (r45 Vilhelma — oče Jožef Brajdič cig.)
if (p113Hv.filter((h) => isSubDioe(h.houseNo)).length !== 1)
  p113Errors.push(`sub dioe. v Gribljih ≠ 1 (r45 — cf. r10/r12/r30 izven Gribljih)`);
// sidra P113
const p113Pins: Array<[string, string]> = [
  ["86", "1. GRIBLJE"], ["86", "VRZELI 4 LET"], ["86", "16.9.1974"],
  ["34", "11. VPIS"], ["34", "Bitnar"],
  ["21", "NEZAKONSKA"], ["21", "VRZEL 3 LETI"], ["21", "0707918500142"], ["21", "Kolbezen"],
  ["53", "VRZEL 2 LETI"], ["53", "18/3. 1919"], ["53", "Dragoš"],
  ["45", "ZAPORED 2. LETO"], ["45", "ČEVLJAR"], ["45", "0310918500439"], ["45", "Lopar"], ["45", "ZAGREB"],
  ["30", "VRZEL 6 LET"], ["30", "1010918500188"], ["30", "Šegina"],
  ["14", "ZAPORED 2. LETO"], ["14", "19/6. 1920"], ["14", "Brinec"],
  ["sub dioe.", "Brajdič"], ["sub dioe.", "CIG"], ["sub dioe.", "sub dioe."],
  ["44", "VRZEL 3 LETI"], ["44", "101191850503"], ["44", "Lopar"], ["44", "Štucelj"],
];
for (const [n, pin] of p113Pins) {
  const blocks = p113Hv.filter((h) => h.houseNo === n);
  if (blocks.length === 0) {
    p113Errors.push(`pin ${n} (${pin}) — hiša ${n} ni v 1918 blokih`);
    continue;
  }
  if (!blocks.some((cur) => cur.whatSi.toLowerCase().includes(pin.toLowerCase())))
    p113Errors.push(`pin hiša ${n} (${pin}) manjka`);
}
// vitals skupaj 517 (po P113: 508 + 9)
if (HOUSE_VITALS.length !== 685)
  p113Errors.push(`HOUSE_VITALS ≠ 533 (${HOUSE_VITALS.length})`);
// duhovniki 1918 (4 = REKORD!): Učak ≥3, Lopar ≥3, Bitnar ≥1, Kolbezen ≥1
if (p113Hv.filter((h) => h.whatSi.includes("Učak")).length < 3)
  p113Errors.push(`podpis Učak < 3× (${p113Hv.filter((h) => h.whatSi.includes("Učak")).length})`);
if (p113Hv.filter((h) => h.whatSi.includes("Lopar")).length < 2)
  p113Errors.push(`podpis Lopar (kaplan) < 2× v Gribljih (${p113Hv.filter((h) => h.whatSi.includes("Lopar")).length} — +4 izven: r43/r47/r48/r49)`);
if (p113Hv.filter((h) => h.whatSi.includes("Bitnar")).length < 1)
  p113Errors.push("podpis Bitnar (kaplan) < 1×");
if (p113Hv.filter((h) => h.whatSi.includes("Kolbezen")).length < 1)
  p113Errors.push("podpis Kolbezen (žup. upravitelj) < 1×");
// nezakonska r24 (Poček) + EMŠO dvom dokumentiran
if (!p113Hv.some((h) => h.houseNo === "21" && h.whatSi.includes("NEZAKONSKA")))
  p113Errors.push("r24 h21 NEZAKONSKA (Poček) manjka");
if (!p113Hv.some((h) => h.houseNo === "21" && h.whatSi.includes("DATUMSKI DVOM")))
  p113Errors.push("r24 EMŠO datumski dvom manjka");
// regresije: (a) h88 trojno zaporedje 1915–17 = KONEC v 1918
if (p113Hv.some((h) => h.houseNo === "88"))
  p113Errors.push("regresija: h88 NE sme biti v 1918 (trojno zaporedje 1915–1917 zaključeno)");
// (b) h24 (največkrat vpisana) pavza v 1918
if (p113Hv.some((h) => h.houseNo === "24"))
  p113Errors.push("regresija: h24 NE sme biti v 1918 (pavza po dvojčkih 1917)");
// (c) h45 čevljar-oče 2. leto (P112 r1 Franc Rajmer + P113 r37 Franc Rajmr?)
if (!p113Hv.some((h) => h.houseNo === "45" && h.whatSi.includes("ČEVLJAR")))
  p113Errors.push("regresija: h45 čevljar 2. leto manjka");
// (d) h14 zaporedje (2. leto)
if (!p113Hv.some((h) => h.houseNo === "14" && h.whatSi.includes("ZAPORED 2. LETO")))
  p113Errors.push("regresija: h14 ZAPORED 2. LETO manjka");
push(
  "qa-p113-parish-baptism-1918",
  "P113: ŽUPNIJA PODZEMELJ — KRSTNA KNJIGA 04105, POLNO LETO 1918 (issue #18; SAMPLE-TRANSCRIPTION-1918; MERI, NE odloča; v7 join nespremenjen): širitev vzorca P79 (1886) → … → P110 (1915) → P111 (1916) → P112 (1917) na leto 1918 — **4. VOJNO leto; 52 vpisov (r1–r52)** — okvir: velika ročna glava »1918« VRH str. 254 = s300; == strani 254–262 == skeni 300–310; **DUP PAROV ×2 — prvi od P110!** (s301 = dup str. 254 — r3 razkrita prek bele listine + s306 = dup str. 258 — r25 razkrita; bela listina na vrhu str. 258 = †16/17.4.1973 Ljubljana + †1.10.2004 Kranj, maticarka Vesna Simonič!); **BREZ zaključne opombe** (formula 1916/1917 »Š t. …« v 1918 MANJKA — vojno leto!); VSI vpisi z Griblji: **9 vpisov / 9 hiš — NARE 8/8 (4. ČISTO leto: 11/11 + 12/12 + 12/12 + 8/8!) + 0 NOVIH numeričnih hiš (4. zapored!) + 1 »sub dioe.«** (r45 — hišna celica brez številke); SIDRA: r2 **Griblje 86 Marija** (VRZEL 4 LET; † 16.9.1974) + r16 **Griblje 34 Ivana** (11. VPIS; podpis **Paulinus Bitnar kaplan**!) + r24 **Griblje 21 Alojzij** (**NEZAKONSKA** — mati Katarina Poček sam. hči; EMŠO 0707918500142 **DATUMSKI DVOM** 07.07 vs 02.07; **podpis Leopold Kolbezen, ŽUP. UPRAVITELJ — 1. v vzorcu!**) + r28 **Griblje 53 Nikolaj** (Dragoš; † 18/3.1919 dojenček) + r37 **Griblje 45 Anton** (**ZAPORED 2. LETO**; oče Franc Rajmr? **ČEVLJAR** 2. leto!; EMŠO 0310918500439 ✓ SIDRO; poročila 21.6.1947 **ZAGREB**; podpis **Jožef(o) Lopar, KAPLAN**) + r38 **Griblje 30 Franc** (Šegina; **VRZEL 6 LET** = najdaljša 1918!; EMŠO 1010918500188 ✓) + r39 **Griblje 14 Barbara** (**ZAPORED 2. LETO**; Brinec mreža; † 19/6.1920) + r45 **Griblje »sub dioe.« Vilhelma** (oče **Jožef Brajdič CIG.** = 2. Brajdič 1918!) + r46 **Griblje 44 Terezija** (Štucelj?; **EMŠO KOREKCIJSKI PAR ×2**: 0611918505155 ✗ + 101191850503 ✓ = 1. v vzorcu!); **VELIKE NOVELE 1918: CIGANI/ROMI ×5** (Hudorovac ×3 matere + Brajdič oče + Ludmila ∞ Hudorovac Anton 1966 = **najmočnejša etnična tema**!) + **NEMŠKA MARG — 1. v vzorcu!** (r10: k.k. Landesregierung Laibach 18.8.1918 Zl. 24828 + Bezirksgericht Möttling [= Metlika] 21.5.1918 P 41/18-1 — priimek **BRAJDIČ** po 2 SODBAMA; oče = vojak **garnizona Podzemelj**; protokol »žup. grad Podzemelj, 31.8.1918«) + **»sub dioe.« ×4** v hišni celici (r10/r12/r30/r45 — VSI = ciganske/begunske družine!) + **MRTVOROJENI ×2 — prvič IZPIPANO »mrtvorojen«** (r18 Vranoviči 1 + r42 Otok 24? [~]; P112 = prazno ime!) + **4 DUHOVNIKI = REKORD** (Učak + Bitnar kaplan + Kolbezen žup. upr. + Lopar kaplan — vojna rotacija!) + **2. RAZVELJAVITEV ZAKONA** (r31: Okrožno sodišče Novo mesto **P 592/64-5, 13.9.1964** — cf. P110 A12 Karlovci 1965!) + **2 URADNI PREIMENOVANJI** (r44: občinski sekretariat **08-203-1-112/79, 11.12.1979** → Teržič? MILKA + r51: »vpisujem Zora« 9.8.1982!) + **PRIIMEK »BALORDA-RECURT«** (r15: poroka 13.6.1981 Ljubljana — **zakonec † po 3 MESECIH!**) + **ŠVEDSKA** (r11 † 2.10.1988 **Vällingby**; prišel? 12.4.1942!) + **RUSIJA** (r50 † julija 1964 **kot delavec v Rusiji? [~]**) + **ZAGREB ×2 poroke + CELJE †** + **VPIS PRENEŠEN ×9 PEČATOV = REKORD** (P112 ×4 → ×9; VSI izven Gribljih!) + **NEZAKONSKI ×5 = REKORD** (r10/r12/r19/r24/r30; 3 ciganske matere!) + EMŠO kampanja **30 zapisov / 28 vrstic = največja** (18 ✓ + 8 DVOMOV + **anomala r44 občina »128« ≠ 500/505**!) + železniška tema ×6 + hiša popravek **Grm 1→25** + 7 dojenčkov † 1918–1920 + 2 mrtvorojena = **17.3% vojna smrtnost**; **KARLOVCI marg r1** (2. povezava cf. P110 A12!); kumulativ **603 vpisov / 88 hiš / 33 let** (1886–1918; **517 vitals**); **P114 LEAD: glava 1919 (»Avstrija 1919«? [~]) VRH str. 263 = s311 — ZADNJE leto knjige 04105 (1886–1919)!** (r1 = Krasinec 3 Anton); DUHOVNIKI detajl: Učak ~34 + Lopar 6 (r37/r43/r46/r47/r48/r49?) + Bitnar 3 (r16/r17/r27) + Kolbezen 1–2 (r24 + r52?); EXCLUDED: 43 (vsi izven Gribljih; 2 mrtvorojena + 9 pečatov + nemška sodba + 2 preimenovanja); skripta scripts/p113_parish_baptism_1918.py (I1–I13, --check **16/16 PASS**); status SAMPLE-TRANSCRIPTION-1918",
  "P113: PARISH OF PODZEMELJ — BAPTISM REGISTER 04105, THE FULL YEAR 1918 (issue #18; SAMPLE-TRANSCRIPTION-1918; MEASURES, does not decide; the v7 join unchanged): extending the sample P79 (1886) → … → P112 (1917) to 1918 — **the 4th WAR year; 52 entries (r1–r52)** — the frame: the large manual heading »1918« at the TOP of p. 254 = s300; == pages 254–262 == scans 300–310; **DUP PAIRS ×2 — the first since P110!** (s301 = dup p. 254 — r3 revealed via the white slip + s306 = dup p. 258 — r25 revealed; the white slip at the top of p. 258 = deaths Apr 16/17, 1973 Ljubljana + Oct 1, 2004 Kranj, registrar Vesna Simonič!); **NO closing note** (the 1916/1917 formula »No. …« MISSING in 1918 — a war year!); ALL Griblje entries: **9 entries / 9 houses — NARE 8/8 (the 4th CLEAN year: 11/11 + 12/12 + 12/12 + 8/8!) + 0 NEW numeric houses (the 4th consecutive!) + 1 »sub dioe.«** (r45 — the house cell without a number); ANCHORS: r2 **Griblje 86 Marija** (a 4-YEAR GAP; died Sep 16, 1974) + r16 **Griblje 34 Ivana** (the 11th ENTRY; signature **Paulinus Bitnar chaplain**!) + r24 **Griblje 21 Alojzij** (**ILLEGITIMATE** — mother Katarina Poček; personal ID 0707918500142 a **DATE DOUBT** Jul 7 vs 2; **signature Leopold Kolbezen, the PARISH ADMINISTRATOR — the 1st in the sample!**) + r28 **Griblje 53 Nikolaj** (Dragoš; died Mar 18, 1919 an infant) + r37 **Griblje 45 Anton** (**CONSECUTIVE the 2nd YEAR**; the father Franc Rajmr? a **SHOEMAKER** for the 2nd year!; personal ID 0310918500439 ✓ ANCHOR; married Jun 21, 1947 **ZAGREB**; signature **Jožef(o) Lopar, CHAPLAIN**) + r38 **Griblje 30 Franc** (Šegina; a **6-YEAR GAP** = the longest of 1918!; personal ID 1010918500188 ✓) + r39 **Griblje 14 Barbara** (**CONSECUTIVE the 2nd YEAR**; the Brinec network; died Jun 19, 1920) + r45 **Griblje »sub dioe.« Vilhelma** (the father **Jožef Brajdič GYPSY** = the 2nd Brajdič of 1918!) + r46 **Griblje 44 Terezija** (Štucelj?; the **personal-ID CORRECTION PAIR ×2**: 0611918505155 ✗ + 101191850503 ✓ = the 1st in the sample!); **THE BIG 1918 NOVELS: GYPSIES/ROMA ×5** (Hudorovac ×3 mothers + the Brajdič father + Ludmila ∞ Hudorovac Anton 1966 = **the strongest ethnic theme**!) + **the GERMAN MARG — the 1st in the sample!** (r10: the k.k. Landesregierung Laibach Aug 18, 1918 No. 24828 + the Bezirksgericht Möttling [= Metlika] May 21, 1918 P 41/18-1 — the surname **BRAJDIČ** by 2 COURT RULINGS; the father = a soldier of the **Podzemelj GARRISON**; the protocol »žup. grad Podzemelj, Aug 31, 1918«) + **»sub dioe.« ×4** in the house cell (r10/r12/r30/r45 — ALL = Roma/refugee families!) + **STILLBIRTHS ×2 — for the first time WRITTEN OUT »mrtvorojen«** (r18 + r42; P112 = an empty name!) + **4 PRIESTS = the RECORD** (Učak + Bitnar chaplain + Kolbezen parish administrator + Lopar chaplain — the war rotation!) + **the 2nd MARRIAGE ANNULMENT** (r31: the Novo mesto District Court **P 592/64-5, Sep 13, 1964** — cf. P110 A12 Karlovci 1965!) + **2 OFFICIAL RENAMINGS** (r44: the municipal secretariat **Nov 12, 1979** → Teržič? MILKA + r51: »I enter Zora« Aug 9, 1982!) + **the SURNAME »BALORDA-RECURT«** (r15: married Jun 13, 1981 Ljubljana — **the husband died after 3 MONTHS!**) + **SWEDEN** (r11 died Oct 2, 1988 **Vällingby**; arrived? Apr 12, 1942!) + **RUSSIA** (r50 died July 1964 **as a worker in Russia? [~]**) + **ZAGREB ×2 weddings + CELJE death** + **ENTRY TRANSFERRED ×9 STAMPS = the RECORD** (P112 ×4 → ×9; ALL outside Griblje!) + **ILLEGITIMATE ×5 = the RECORD** + the personal-ID campaign **30 records / 28 rows = the largest** (18 ✓ + 8 DOUBTS + **the anomaly r44 district »128« ≠ 500/505**!) + the railway theme ×6 + the house-number correction **Grm 1→25** + 7 infants died 1918–1920 + 2 stillbirths = **17.3% war mortality**; **the KARLOVCI marg r1** (the 2nd link cf. P110 A12!); the cumulative **603 entries / 88 houses / 33 years** (1886–1918; **517 vitals**); **the P114 LEAD: the 1919 heading (»Avstrija 1919«? [~]) at the TOP of p. 263 = s311 — the LAST year of book 04105 (1886–1919)!** (r1 = Krasinec 3 Anton); PRIEST detail: Učak ~34 + Lopar 6 + Bitnar 3 + Kolbezen 1–2; EXCLUDED: 43; the script scripts/p113_parish_baptism_1918.py (I1–I13, --check **16/16 PASS**); status SAMPLE-TRANSCRIPTION-1918",
  p113Errors.length === 0,
  p113Errors.length === 0
    ? `9 vpisov / 9 hiš — NARE 8/8 (4. čisto leto!) + **1 »sub dioe.« (r45 Brajdič cig.)** · **0 novih numeričnih hiš (4. zapored!)** · okvir 1918: str. 254–262 = s300–s310 (52 vpisov; **DUP ×2 = prvi od P110!**; **BREZ zaključne opombe!**) · sidra: h86 VRZEL 4 LET · h34 Bitnar · **h21 NEZAKONSKA + Kolbezen žup. upr.!** · h53 Dragoš · **h45 ZAPORED 2. LETO + ČEVLJAR + Lopar + Zagreb!** · h30 VRZEL 6 LET + Šegina · h14 ZAPORED 2. LETO + Brinec · h44 EMŠO korekcijski PAR · NOVELE: **CIGANI ×5** · **NEMŠKA sodba BRAJDIČ (garnizona!)** · **sub dioe. ×4** · **mrtvorojena izpipana ×2** · **4 duhovniki!** · **2. razveljavitev (Novo mesto 1964)** · **2 preimenovanji (1979 + 1982)** · **Balorda-Recurt († po 3 mes.)** · **Švedska + Rusija + Zagreb ×2 + Celje** · **VPIS PRENEŠEN ×9 = REKORD** · nezakonskih ×5 · **EMŠO 30/28 (18✓ + 8 dvomov + anomala »128«)** · žel. tema ×6 · hiša 1→25 · † 17.3% · P114 lead (ZADNJE leto!) · EXCLUDED 43 · vitals 517 · kumulativ 603/88 33 let`
    : p113Errors.join("; "),
);

// ——— qa-p114: župnija Podzemelj — krstna 1919 (P114; issue #18; ZADNJE leto knjige 04105!) ———
const p114PageOfScan = (s: number) =>
  ({ 311: 263, 312: 264, 313: 265, 314: 266, 315: 267, 316: 268, 317: 269, 318: 270, 319: 271, 320: 272, 321: 272, 322: 273, 323: 274, 324: 275 } as Record<number, number>)[s] ?? -1;
const p114Hv = HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year === 1919);
const p114Errors: string[] = [];
if (p114Hv.length !== 11)
  p114Errors.push(`vpisov 1919 (04105, zasidrani) ≠ 11 (${p114Hv.length})`);
const p114Houses = new Set(p114Hv.map((h) => h.houseNo));
if (p114Houses.size !== 11)
  p114Errors.push(`hiš 1919 ≠ 11 — najdeno ${p114Houses.size}: ${[...p114Houses].join(",")}`);
const p114Repeat = [...p114Hv.map((h) => h.houseNo)].filter((hn, i, arr) => arr.indexOf(hn) !== i);
if (p114Repeat.length !== 0)
  p114Errors.push(`intra-letne ponovitve 1919 morajo biti PRAZNE — najdeno: ${p114Repeat.join(",")}`);
// dup-novela: stran == sken − 48, RAZEN s321 (dup-foto s320, bela listina prepognjena!)
const p114BadPage = p114Hv.filter(
  (h) => h.status !== "DOCUMENTED" || !h.scan || !h.page
    || h.page !== p114PageOfScan(h.scan)
    || h.scan < 311 || h.scan > 324,
);
if (p114BadPage.length > 0)
  p114Errors.push(`scan/page ne ustreza P114 noveli (dup s321!): ${p114BadPage.map((h) => `${h.houseNo}@${h.scan}`).join(",")}`);
// NARE 10/11: natanko 1 nova hiša = "81" (čisto leto se konča pri 4!)
const p114Prior = new Set(
  HOUSE_VITALS.filter((h) => h.bookSignature === "04105" && h.year < 1919).map((h) => h.houseNo),
);
const p114New = p114Houses_1919Numeric();
function p114Houses_1919Numeric(): string[] {
  return [...p114Houses].filter((hn) => /^\d+$/.test(hn) && !p114Prior.has(hn)).sort();
}
if (p114New.join(",") !== "81")
  p114Errors.push(`nove numerične hiše 1919 morajo biti natanko ["81"] (NARE 10/11!) — najdeno: ${p114New.join(",") || "∅"}`);
// brez »sub dioe.« v 1919
if (p114Hv.filter((h) => h.houseNo.startsWith("sub dioe.")).length !== 0)
  p114Errors.push("sub dioe. v 1919 mora biti PRAZNO (0)");
// sidra P114
const p114Pins: Array<[string, string]> = [
  ["8", "1. GRIBLJE"], ["8", "2603919505488"], ["8", "VRZEL 5 LET"],
  ["47", "2. GRIBLJE"], ["47", "VRZEL 6 LET"], ["47", "DVOJNI PODPIS"],
  ["88", "3. GRIBLJE"], ["88", "1605919505381"], ["88", "pravilen Brinc"],
  ["46", "4. GRIBLJE"], ["46", "VRZEL 2 LETI"], ["46", "številčenjska napaka"],
  ["90", "5. GRIBLJE"], ["90", "UČITELJ"],
  ["82", "6. GRIBLJE"], ["82", "TESAR"],
  ["48", "7. GRIBLJE"], ["48", "3108919505332"], ["48", "DRŽAVLJANKA"],
  ["40", "8. GRIBLJE"], ["40", "Briner (= Brinc"],
  ["81", "NOVA HIŠA"], ["81", "0909919505271"], ["81", "9. GRIBLJE"],
  ["6", "10. GRIBLJE"], ["6", "28/4 1921"],
  ["5", "11. GRIBLJE"], ["5", "ZADNJA GRIBLJSKA"], ["5", "12-MESTNI"],
];
for (const [n, pin] of p114Pins) {
  const blocks = p114Hv.filter((h) => h.houseNo === n);
  if (blocks.length === 0) {
    p114Errors.push(`pin ${n} (${pin}) — hiša ${n} ni v 1919 blokih`);
    continue;
  }
  if (!blocks.some((cur) => cur.whatSi.toLowerCase().includes(pin.toLowerCase())))
    p114Errors.push(`pin hiša ${n} (${pin}) manjka`);
}
// vitals skupaj 528 (po P114: 517 + 11)
if (HOUSE_VITALS.length !== 685)
  p114Errors.push(`HOUSE_VITALS ≠ 533 (${HOUSE_VITALS.length})`);
// duhovniki 1919 (5 = REKORD!): Cerar župnik ≥8 (Griblje), Lopar ≥2 (l40+l75; +l15 Logar = DVOJNI PODPIS);
// Rogar (l62–67, l70) + Učak (l2) + Katanov (l27) = SAMO IZVEN Gribljih → v vitals blokah morajo biti PRAZNI
if (p114Hv.filter((h) => h.whatSi.includes("Cerar")).length < 8)
  p114Errors.push(`podpis Cerar (župnik) < 8× (${p114Hv.filter((h) => h.whatSi.includes("Cerar")).length})`);
if (p114Hv.filter((h) => h.whatSi.includes("Lopar")).length < 2)
  p114Errors.push(`podpis Lopar (kaplan) < 2× (${p114Hv.filter((h) => h.whatSi.includes("Lopar")).length} — l40 h82 + l75 h5)`);
if (p114Hv.filter((h) => h.whatSi.includes("Rogar")).length !== 0)
  p114Errors.push("Rogar (kaplan) NE sme biti v Gribljih 1919 (l62–67/l70 = izven — evidence A7)");
if (p114Hv.filter((h) => h.whatSi.includes("Učak")).length !== 0)
  p114Errors.push("Učak NE sme biti v Gribljih 1919 (l2 = izven — evidence A7)");
// EMŠO sidra + anomala l57 prazen + l75 12-mestni
if (!p114Hv.some((h) => h.houseNo === "81" && h.whatSi.includes("0909919505271")))
  p114Errors.push("h81 EMŠO sidro manjka");
// regresije: (a) h86 (P113 r2) NE sme biti v 1919 (pavza)
if (p114Hv.some((h) => h.houseNo === "86"))
  p114Errors.push("regresija: h86 NE sme biti v 1919 (pavza po P113)");
// (b) h24 pavza v 1919
if (p114Hv.some((h) => h.houseNo === "24"))
  p114Errors.push("regresija: h24 NE sme biti v 1919 (pavza)");
// (c) h53 (P113 7. vpis) pavza v 1919
if (p114Hv.some((h) => h.houseNo === "53"))
  p114Errors.push("regresija: h53 NE sme biti v 1919 (7. vpis 1918)");
// (d) h88 ZAPORED? ne — h88 = 6. vpis z vrzeljo; h34 pavza
if (p114Hv.some((h) => h.houseNo === "34"))
  p114Errors.push("regresija: h34 NE sme biti v 1919 (pavza po 11. vpisu 1918)");
push(
  "qa-p114-parish-baptism-1919",
  "P114: ŽUPNIJA PODZEMELJ — KRSTNA KNJIGA 04105, POLNO LETO 1919 = **ZADNJE LETO KNJIGE (1886–1919)!** (issue #18; SAMPLE-TRANSCRIPTION-1919; MERI, NE odloča; v7 join nespremenjen): **ZAKLJUČEK krstne linije** P79 (1886) → … → P113 (1918) → P114 (1919) — **79 vpisov (l1–l78 + DUPLA labela »31« = edina številčenjska napaka vzorca!)** — okvir: velika ročna glava »Anno 1919« + tiskana »Leto 1919« VRH str. 263 = s311; == strani 263–275 == skeni 311–324; **BREZ zaključne opombe** (vojno leto); s321 = **DUP-FOTO s320** (bela listina prepognjena — razkriti starši l56–l59!); s325 = prazna stran + **PRILEPEN DOPIS ŠKOFIJSKEGA ORDINARIATA (25.6.1919, č. 2908): »… pravi podatki o rojstvu in krstu Jakoba Košca … rojstni dan otroka 14. aprila 1917, ne 1. maja 1917 … napačen vpis v rojstni in krstni knjigi v Metliki«** = l27 naknadni vpis (»Leto 1917«, krčen v Metliki 18.5.1919, marg »vpis naredil … 23. maja 1919 št. 49673«; mati Katarina Hudorovac = ISTA kot l14 Košec!); s326 = zadnja platnica »Podzemelj R 1886–1919«; VSI vpisi z Griblji: **11 vpisov / 11 hiš — NARE 10/11 (h90/h82/h48/h40/h81!) + 1 NOVA hiša h81 (čisto leto P110–P113 se konča pri 4!)**; SIDRA: l10 **Griblje 8 Ana** (EMŠO 2603919505488 ✓ SIDRO; VRZEL 5 LET) + l15 **Griblje 47 Marija** (VRZEL 6 LET; **DVOJNI PODPIS Logar + Cerar!**) + l26 **Griblje 88 Amalija** (**PRIIMEK BRINC marg: »Priimek Brinec mi Brinc, ampak je pravilen Brinc«!**; EMŠO 1605919505381 ✓; oče roj. 1860 = 59 let!) + l31 **Griblje 46 Peter** (12. VPIS) + l32 **Griblje 90 Stanislava** (oče UČITELJ — 1. na Gribljih!) + l41 **Griblje 82 Peter** (TESAR; † 11.11.1934) + l45 **Griblje 48 Vida** (EMŠO 3108919505332 ✓; **DRŽAVLJANKA RS marg 1996!**; razveza Beograd 1954/56!) + l47 **Griblje 40 Julij** (**BRINC mreža h88+h40!**) + l48 **Griblje 81 Karolina** (**NOVA HIŠA!**; EMŠO 0909919505271 ✓) + l74 **Griblje 6 Barbara** († 28/4 1921) + l76 **Griblje 5 Jožef** (**ZADNJA GRIBLJSKA vrstica knjige!**; EMŠO 12-MESTNI 191219500852!); **VELIKE NOVELE 1919: BELA LISTINA = LEGITIMIZACIJSKO PISMO** (Bohumil Šponiček, Bahnhof Ljube/Labbe bei **FIUME**, 1.8.1915 — otrok Emil krščen 16.7.1915; starša poročena 10.9.1907 v **Zagrebu**; 2. nemški dokument vzorca + železniška tema + povezava na 1915!) + **EMŠO KAMPANJA ~34 žigov = REKORD** (27 ✓ datumsko + 6 dvomov + **l57 »EMŠO je:« PRAZEN** + l75 12-mestni; spolni pregled neuporaben — naključne končnice!) + **4 RAZVELJAVITVE ZAKONA = REKORD** (l22 Zagreb 6.9.1948 + l24 Novo mesto 9.10.1982 + l40 + l72 Ljubljana 28.2.1958 s prevzemom priimka **TRILAR**!) + **5 DUHOVNIKOV = REKORD** (Grgor Cerar župnik ~50 podpisov = glavni + Učak ord. tret. + Lopar kaplan + Rogar kaplan + **Peter Katanov? barban iz Metlike — zunanji pri l27!**) + **VPIS PRENEŠEN ×19 = REKORD** (P113 ×9 → ×19; 2003–2007) + **NEZAKONSKI ×3** (l24 mati Hudorovac samska + l32 Vranešič + l51 Jakofčič — očetove celice PRAZNE!) + **MRTVOROJEN ×1** (l69 Boginja vas 39 — brez imena, krsta »—«, brez botre/babice/podpisa!) + **† 12 (15.2%)**: 10 dojenčkov 1920 + l33 (+ 6/7 1919 = **ISTI DAN kot rojstvo!**) + l73 (1921) + odrasle: **l78 † 30.1.1945 UBITA OD BOMBARDIRANJA = ZADNJI VPIS KNJIGE!** + l61 arestiran 14.8.1943 + l25 padel 19.3.1943 + **TUJE DRŽAVE ×8** (Rijeka/Fiume + Zagreb ×3 + Beograd ×2 + **AMERIKA poroka l68** + **Ohio l28 Clayton County!** + Pag + Graz ×2 + Jesenice) + **2 NEZNANI VASI** (l23 Okljuka + l53 Trilovje? — ni v matičnem seznamu!) + **KAPLJIŠČE l74 = 1. pojav** + Dragoše l68 = 2. + **Krivoglavice ×2 potrjene** (l5+l21!) + »dvojčici po hiši« Cerkvišče 23 (l55 Stubljar + l56 Petričan — isti dan, različni starši!) + samopopravki »Pomotoma vpisana poroka« (l63/l65) + 1. fotograf (l27 botra Hedviga Štramar!) + 1. učitelj-oče na Gribljih (l32!) + oče roj. 1849 = 70 let (l48 Humar iz Kranjskih Lokv!) + kumulativ **614 vpisov / 88 hiš / 34 let** (1886–1919; **528 vitals**; bloki 04105 **502**); **P115 LEAD: krstna linija issue #18 KONČANA — naslednja poročne/smrtne 04xxx; bela listina ponuja povezavo nazaj na P110 (1915)!**; EXCLUDED: 70; skripta scripts/p114_parish_baptism_1919.py (I1–I12); status SAMPLE-TRANSCRIPTION-1919",
  "P114: PARISH OF PODZEMELJ — BAPTISM REGISTER 04105, THE FULL YEAR 1919 = **THE LAST YEAR OF THE BOOK (1886–1919)!** (issue #18; SAMPLE-TRANSCRIPTION-1919; MEASURES, does not decide; the v7 join unchanged): **the END of the baptism line** P79 (1886) → … → P113 (1918) → P114 (1919) — **79 entries (l1–l78 + the DUPLICATED label »31« = the only numbering error of the sample!)** — the frame: the large hand header »Anno 1919« + printed »Leto 1919« at the TOP of p. 263 = s311; == pages 263–275 == scans 311–324; **NO closing note** (a war year); s321 = the **DUP PHOTO of s320** (the white slip folded back — the parents of l56–l59 revealed!); s325 = a blank page + **the PASTED LETTER of the Diocesan Ordinariate (Jun 25, 1919, no. 2908): »… the true data on the birth and baptism of Jakob Košec … the child's birthday is Apr 14, 1917, not May 1, 1917 … a wrong entry in the birth and baptism register in Metlika«** = l27 the belated entry (»Year 1917«, baptized in Metlika May 18, 1919); s326 = the back cover »Podzemelj R 1886–1919«; ALL Griblje entries: **11 entries / 11 houses — NARE 10/11 + 1 NEW house h81 (the clean streak P110–P113 ends at 4!)**; ANCHORS: l10 **Griblje 8 Ana** (ID 2603919505488 ✓ ANCHOR) + l15 **Griblje 47 Marija** (the DOUBLE SIGNATURE Logar + Cerar!) + l26 **Griblje 88 Amalija** (**the SURNAME BRINC marg: »the surname Brinec mi Brinc, but the correct is Brinc«!**) + l31 **Griblje 46 Peter** (the 12th ENTRY) + l32 **Griblje 90 Stanislava** (a TEACHER father — the 1st on Griblje!) + l41 **Griblje 82 Peter** (a CARPENTER; † Nov 11, 1934) + l45 **Griblje 48 Vida** (**A CITIZEN OF SLOVENIA marg 1996!**; divorced in Belgrade 1954/56) + l47 **Griblje 40 Julij** (**the BRINC network h88+h40!**) + l48 **Griblje 81 Karolina** (**A NEW HOUSE!**) + l74 **Griblje 6 Barbara** († Apr 28, 1921) + l76 **Griblje 5 Jožef** (**THE LAST GRIBLJE row of the book!**; the 12-DIGIT personal ID!); **THE BIG 1919 NOVELS: the WHITE SLIP = a LEGITIMIZATION LETTER** (Bohumil Šponiček, Bahnhof Ljube/Labbe near **FIUME**, Aug 1, 1915 — the child Emil baptized Jul 16, 1915; the parents married Sep 10, 1907 in **Zagreb**; the 2nd German document of the sample + the railway theme + the link back to 1915!) + **the PERSONAL-ID CAMPAIGN ~34 stamps = the RECORD** (27 ✓ + 6 doubts + **l57 »EMŠO je:« EMPTY** + l75 12-digit!) + **4 MARRIAGE ANNULMENTS = the RECORD** (Zagreb 1948 + Novo mesto 1982 + l40 + Ljubljana 1958 with the resumption of the maiden name **TRILAR**!) + **5 PRIESTS = the RECORD** (Grgor Cerar the parish priest ~50 signatures + Učak + Lopar chaplain + Rogar chaplain + **Peter Katanov? the chaplain from Metlika — external, at l27!**) + **ENTRY TRANSFERRED ×19 = the RECORD** (2003–2007) + **ILLEGITIMATE ×3** + **STILLBORN ×1** (l69 — no name, baptism »—«!) + **† 12 (15.2%)**: incl. l33 (the SAME DAY as the birth!) + **l78 † Jan 30, 1945 KILLED BY BOMBING = THE LAST ENTRY OF THE BOOK!** + **8 FOREIGN COUNTRIES** (Rijeka/Fiume + Zagreb ×3 + Belgrade ×2 + **AMERICA the wedding l68** + **Ohio l28 Clayton County!** + Pag + Graz ×2 + Jesenice) + **2 UNKNOWN VILLAGES** (Okljuka + Trilovje?) + **KAPLJIŠČE the 1st appearance** + the »twins by house« Cerkvišče 23 (l55 + l56 — the same day, different parents!) + the 1st photographer (l27 the godmother!) + the 1st teacher-father on Griblje (l32!) + a father born 1849 = aged 70 (l48!); the cumulative **614 entries / 88 houses / 34 years** (1886–1919; **528 vitals**; 04105 blocks **502**); **the P115 LEAD: the baptism line of issue #18 FINISHED — next the marriage/death books 04xxx**; EXCLUDED: 70; the script scripts/p114_parish_baptism_1919.py (I1–I12); status SAMPLE-TRANSCRIPTION-1919",
  p114Errors.length === 0,
  p114Errors.length === 0
    ? `11 vpisov / 11 hiš — **NARE 10/11 + 1 NOVA hiša h81 (čisto leto se konča pri 4!)** · okvir 1919: str. 263–275 = s311–s324 (79 vpisov; **dup labela »31«!**; **BREZ zaključne opombe**) · **s321 = dup-foto s320 (bela listina odprta!)** · **s325 = dopis ordinariata (Jakob Košec 14.4.1917!)** · sidra: h8 SIDRO 2603919505488 · **h88 PRIIMEK BRINC marg** · h48 DRŽAVLJANKA RS · **h81 NOVA HIŠA!** · **h5 ZADNJA GRIBLJSKA (EMŠO 12-mestni!)** · NOVELE: **bela listina = legitimizacijsko pismo Šponiček (Fiume 1915)** · **EMŠO ~34 = REKORD (l57 PRAZEN!)** · **4 razveljavitve = REKORD** · **5 duhovnikov = REKORD** · **VPIS PRENEŠEN ×19 = REKORD** · nezakonski ×3 + mrtvorojen ×1 · **† 15.2% (l78 bombardiranje 1945 = zadnji vpis!)** · **tuje države ×8 (Amerika, Ohio!)** · 2 neznani vasi · Kapljišče 1. pojav · Krivoglavice ×2 · dvojčici po hiši · 1. fotograf · 1. učitelj-oče · EXCLUDED 70 · vitals 528 · kumulativ 614/88 34 let · **KNJIGA 04105 ZAKLJUČENA!**`
    : p114Errors.join("; "),
);

// ——— qa-p115: župnija Podzemelj — poročna knjiga 04455, polno leto 1886 (P115; NOVA linija po zaključku krstne 04105!) ———
const p115Marr = HOUSE_VITALS.filter((h) => h.bookSignature === "04455");
const p115Errors: string[] = [];
if (p115Marr.length !== 168)
  p115Errors.push(`poročni bloki (04455) ≠ 142 (${p115Marr.length} — P121: + 4 bloki 1892; P122: + 5 bloki 1893; P123: + 4 bloki 1894; P124: + 3 bloki 1895; P125: + 3 bloki (h24+h14-1895ext + h18-1896); P126: + 9 blokov 1897; P127: + 9 blokov 1898; P128: + 6 blokov 1899; P132: + 12 blokov 1903; P133: + 8 blokov 1904; P134: + 13 blokov 1905 = 115!)`);
const p115M1886 = p115Marr.filter((h) => h.year === 1886);
const p115Houses1886 = p115M1886.map((h) => h.houseNo).sort();
if (p115Houses1886.join(",") !== "16,25,31,56,60,65,71")
  p115Errors.push(`hiše 1886 (04455) ≠ [16,25,31,56,60,65,71] — najdeno: ${p115Houses1886.join(",")} (P115 popravki: 36→56, 63→65, 15→16!)`);
// P115 re-read sidra (nove brane v whatSi)
const p115Pins: Array<[string, string]> = [
  ["31", "STRAUS"], ["31", "Papič"], ["31", "franz Dovgan"],
  ["56", "PEGDIREC"], ["56", "SESTRIN+BRAT"], ["56", "BREZ PODPISA"],
  ["60", "KLEPEC"], ["60", "BREZ PODPISA"],
  ["65", "POŽEK"], ["65", "GRIBLJE 64"], ["65", "BREZ PODPISA"],
  ["16", "GRIBLJE 16"], ["16", "h15 še vedno sidro 1887"], ["16", "BREZ PODPISA"],
  ["25", "PRILOŽJE 25"], ["25", "Klepec"], ["25", "TOMEC"],
  ["71", "Martin KRIŽAN"], ["71", "MÜNDEL"], ["71", "Landwirth"],
];
for (const [hn, pin] of p115Pins) {
  const blk = p115M1886.filter((h) => h.houseNo === hn);
  if (blk.length === 0) {
    p115Errors.push(`pin ${hn} (${pin}) — hiša ${hn} ni med 1886 bloki`);
    continue;
  }
  if (!blk.some((cur) => cur.whatSi.toLowerCase().includes(pin.toLowerCase())))
    p115Errors.push(`pin hiša ${hn} (${pin}) manjka`);
}
// stara P80 branja IZTEKLA (natančni stari fragmenti — popravna opomba sme citirati kratek »staro«)
const p115OldReadings = [
  "Dorothea Perdinec", "Perdinec [~], 30, Krasinec 38", "Mathias Kukec",
  "Katharina Peršić", "Marko Perzan [~]", "Martin Pavie", "Gasthausmeister [~]",
  "Vinica 9;", "Vinica 10 rad.", "Maria née Podlirec", "née Stabek",
  "bivališče neveste nečitljivo", "GRIBLJE 63", "GRIBLJE 36 (starši",
  // P116 re-read (h15 sidro): ženin Fablić (ne Šambie) + nevesta 23 (ne 29) + mati neveste Kambič (ne Šambiè)
  "Johann Šambie", "GRIBLJE 29", "née Šambiè",
];
for (const old of p115OldReadings) {
  // P126: »GRIBLJE 29« LEGITIMNO v poročnih blokih 1897 (v9 Maria Milek, GRIBLJE 29 — 1. poročni dokaz h29; h40-blok omenja nevestino hišo!) — ban velja le za stare bloke (h15 sidro re-read P116; h23 citira le »29«); P138: + 1909 (№13 nevesta Maria KURE, GRIBLJE 29 — 2. poročni dokaz h29!)
  if (p115Marr.some((h) => h.whatSi.includes(old) && !(old === "GRIBLJE 29" && (h.year === 1897 || h.year === 1909)) && !(old === "GRIBLJE 63" && (h.year === 1911 || h.year === 1912))))  // P140: h63 = PONOVNO VELJAVNA poročna hiša 1911 (№1 nevesta Catharina Križan — 04105-h63 krsti 1887–1909!)
    p115Errors.push(`staro P80 branje še v bloku 04455: »${old}«`);
}
// duhovnik: Dovgan podpisal 3/7 blokov 1886 (h31, h25, h71) — 4 BREZ PODPISA (h56, h60, h65, h16)
const p115Dovgan = p115M1886.filter((h) => h.whatSi.includes("Dovgan")).length;
if (p115Dovgan !== 3)
  p115Errors.push(`Dovgan podpisi 1886 ≠ 3 (${p115Dovgan} — h31/h25/h71)`);
const p115Unsigned = p115M1886.filter((h) => h.whatSi.includes("BREZ PODPISA")).length;
if (p115Unsigned !== 4)
  p115Errors.push(`BREZ PODPISA 1886 ≠ 4 (${p115Unsigned} — h56/h60/h65/h16; vpisi 4–19 neodpisani!)`);
// sidro 1885: Pegdirec (P115 popravek »Podlirec«)
const p115Anchor = p115Marr.find((h) => h.houseNo === "13" && h.year === 1885);
if (!p115Anchor || !p115Anchor.whatSi.includes("PEGDIREC") || p115Anchor.whatSi.includes("née Podlirec"))
  p115Errors.push("sidro 1885 (h13): mati ženina ≠ PEGDIREC ali staro »Podlirec« še prisotno");
// kumulativ (ob P115): vitals 528 nespremenjen (poročni bloki že od P80); P116: + 5 → 533
if (HOUSE_VITALS.length !== 685)
  p115Errors.push(`HOUSE_VITALS ≠ 533 (${HOUSE_VITALS.length} — P116: 528 + 5 novih poročnih blokov (h23/h37/h69/h3/h10) = 533!)`);
push(
  "qa-p115-parish-marriage-1886",
  "P115: ŽUPNIJA PODZEMELJ — POROČNA KNJIGA 04455 (1873–1922), POLNO LETO 1886 (issue #18; SAMPLE-TRANSCRIPTION-M1886; NOVA linija po zaključku krstne 04105!): okvir P80 POTRJEN 1:1 (skeni 61–65 == Pag. 60–64; Pag. == sken − 1 v 61–66; **24 vpisov** = 3+5+7+5+4; meja na Pag. 60: vpis 22/1885 (Griblje 13 × 25 = P80 sidro h13) pod ločilnico »1 8 8 6«; glava 1887 Pag. 65) — **FAZA 2: 24/24 vpisov transkribiranih OBOJESTRANSKO (starši/priče/Urkunden/duhovnik!)**; **P80 RE-READ POPRAVKI ×11** (max zoom + 1:1 primerjava števk): **h36→h56** (vpis 4 — Johann Šimec × Dorothea PEGDIREC, Krasinec 28) + **h63→h65** (vpis 12 — Mathias Milek ½ Gütler × Katharina POŽEK, **GRIBLJE 64 = NOVA hiša okvira**!) + **h15→h16** (vpis 17 — Ana Filak Lavřin; h15 OSTAJA sidro 1887!) + **h25→PRILOŽJE 25** (vpis 20 — Jurij Klepec; IZBRISAN zapis pod vasjo; hiša 25 Griblje brez poročnega dokaza!) + priimki: Klepec (11, ne »Kukec«) + Tomec (20, ne »Gomec«) + Požek (12, ne »Peršić«) + Pegdirec (4/5/12/1885, ne »Perdinec«/»Podlirec«) + **Martin KRIŽAN, Landwirth, Krasinec 9** (23, ne »Marko Perzan, Vinica 9«) + Straus (2, ne »Špelcer«); **VELIKE NOVELE 1886: 6 POROK NA ISTI DAN 15.2. (vpisi 3–8 = pustna masa!)** + **DVA SESTRSKA DVOJNA POROKA** (vpis 4+5 = Pegdirec sestra+brat ISTEGA DNE z ISTIMI starši; vpis 9+21 = Musié sestri Anna 19 + Dorothea 31, 9 mesecev narazen!) + **VDOVE 4 (+1 dvom)** (vpis 7 = 23-letna »Witwe Schweiger«!) + **vpis 19 = OBADVA LEDIGA pri 43/42** (faza 1 »2 vdova« NAPAKA; 1. POLICIST vzorca — Polizeidiener straža № 56 »St. Greina«?; »Podze-meč« = sicerptova pisava Podzemelj!) + **MÜNDEL-TIMELINE (vpis 23)**: Maria Straus (34, h71) poročena kot varovanka — mati Ana Strauš † 7.9.1886 (mrliška!) → kronologija 1:1; skrbnik = verjetno ženin vpis 22 (**Vormund**, 23!) + **PREČRTANO (vpis 24)**: ~~Josef~~ pod Antonom (oče Josef Bufala!; rod = Butala cf. vpis 18) + **DUHOVNIK franz Dovgan = 9 podpisov** (vpisi 1–3 + 20–24 + 1885; **VPISI 4–19 (16!) PRAZEN STOLPEC** — masovna poroka + poletje!) + **DISPENSACIJE ×6** (2./3./3./4. kan. stopnja; Hochfürstl. Konsensi; k.k. Kreisgericht Metlika/Črnomelj) + **EHEVERLAGS-CONTRACT vpis 22** (poročna pogodba pred notarjem 21.11.1886; faza 1 »Villach« = misread »verlags«!) + **»Krasi-nec« = PRELOM besede Krasinec** (faza 1 »Vinica 9/10« popravljeno!) + PEGDIREC-mreža ×7 = najgostejša družina + priča vpis 10 = ženinov oče kot VAISENVORMUND (skrbnik otrok neveste-vdove!) + statusi-novosti (Müllner, Gürtler, Zimmermann, Gasthaus-Wirth, Vormund, Mündel, Polizeidiener, Bürger von Tschernembl, ¼ Gütler) + zunanji (vpis 1 neznana vas [~], vpis 18 Vidošice? 8 pf. Metlika, priča 9 Črnomelj mestan); vitals **528 nespremenjen** (poročni bloki že od P80); bloki 04455 = **11** (7 okvir 1886 + sidra 1882/1885/1887×2); **P116 LEAD: poročna 1887** (glava Pag. 65 = s66, vpisi 1–4/1887; sidra h71 Mathias Straus + h15 Jaklič × Brinec že pinned); EXCLUDED: 5 (sidro 1885 + 4× glava 1887); skripta scripts/p115_parish_marriage_1886.py (I1–I10); status SAMPLE-TRANSCRIPTION-M1886",
  "P115: PARISH OF PODZEMELJ — MARRIAGE REGISTER 04455 (1873–1922), THE FULL YEAR 1886 (issue #18; SAMPLE-TRANSCRIPTION-M1886; a NEW line after the baptism 04105 was finished!): the P80 frame CONFIRMED 1:1 (scans 61–65 == pages 60–64; page == scan − 1 in 61–66; **24 entries** = 3+5+7+5+4; the boundary on p. 60: entry 22/1885 (Griblje 13 × 25 = the P80 h13 anchor) under the separator »1 8 8 6«; the 1887 header on p. 65) — **FAZA 2: 24/24 entries transcribed BOTH-SIDES (parents/witnesses/Urkunden/priest!)**; **THE P80 RE-READ CORRECTIONS ×11** (max zoom + 1:1 digit comparison): **h36→h56** (entry 4 — Johann Šimec × Dorothea PEGDIREC, Krasinec 28) + **h63→h65** (entry 12 — Mathias Milek ½ Gütler × Katharina POŽEK, **GRIBLJE 64 = A NEW house of the frame**!) + **h15→h16** (entry 17 — Ana Filak Lavřin; h15 REMAINS the 1887 anchor!) + **h25→PRILOŽJE 25** (entry 20 — Jurij Klepec; an ERASED entry under the village; house 25 Griblje without a marriage proof!) + surnames: Klepec (11, not »Kukec«) + Tomec (20, not »Gomec«) + Požek (12, not »Peršić«) + Pegdirec (4/5/12/1885, not »Perdinec«/»Podlirec«) + **Martin KRIŽAN, a full farmer, Krasinec 9** (23, not »Marko Perzan, Vinica 9«) + Straus (2, not »Špelcer«); **THE BIG 1886 NOVELS: 6 WEDDINGS ON THE SAME DAY FEB 15 (entries 3–8 = the carnival mass!)** + **TWO SIBLING DOUBLE WEDDINGS** (entries 4+5 = the Pegdirec sister+brother THE SAME DAY with THE SAME parents; entries 9+21 = the Musié sisters Anna 19 + Dorothea 31, 9 months apart!) + **WIDOWS 4 (+1 doubt)** (entry 7 = the 23-year-old »Witwe Schweiger«!) + **entry 19 = BOTH SINGLE at 43/42** (the faza-1 »2 widows« WRONG; the 1st POLICEMAN of the sample — Polizeidiener, post № 56 »St. Greina«?; »Podze-meč« = the scribe's odd writing of Podzemelj!) + **THE WARD TIMELINE (entry 23)**: Maria Straus (34, h71) married as a ward — the mother Ana Strauš † Sep 7, 1886 (death register!) → a 1:1 chronology; the guardian = probably the groom of entry 22 (a **Vormund**, 23!) + **THE STRUCK-OUT NAME (entry 24)**: ~~Josef~~ under Anton (the father Josef Bufala!; the kin = Butala cf. entry 18) + **THE PRIEST franz Dovgan = 9 signatures** (entries 1–3 + 20–24 + 1885; **ENTRIES 4–19 (16!) EMPTY COLUMN** — the mass wedding + the summer!) + **DISPENSATIONS ×6** (the 2nd/3rd/3rd/4th canonical degrees; the princely consents; the k.k. Kreisgericht Metlika/Črnomelj) + **THE EHEVERLAGS-CONTRACT entry 22** (a marriage property contract before a notary Nov 21, 1886; the faza-1 »Villach« = a misread of »verlags«!) + **»Krasi-nec« = the LINE-BREAK of Krasinec** (the faza-1 »Vinica 9/10« corrected!) + the PEGDIREC network ×7 = the densest family + the witness of entry 10 = the groom's father as the ORPHANS' GUARDIAN (probably of the widow-bride's children!) + status novelties (Müllner, Gürtler, Zimmermann, innkeeper, Vormund, Mündel, Polizeidiener, a burgher of Tschernembl, ¼ Gütler) + the externals (entry 1 an unknown village [~], entry 18 Vidošice? 8 parish Metlika, witness 9 a burgher of Črnomelj); vitals **528 unchanged** (the marriage blocks counted since P80); the 04455 blocks = **11** (7 of the 1886 frame + the anchors 1882/1885/1887×2); **the P116 LEAD: the marriages of 1887** (the header p. 65 = s66, entries 1–4/1887; the anchors h71 Mathias Straus + h15 Jaklič × Brinec already pinned); EXCLUDED: 5; the script scripts/p115_parish_marriage_1886.py (I1–I10); status SAMPLE-TRANSCRIPTION-M1886",
  p115Errors.length === 0,
  p115Errors.length === 0
    ? `24 vpisov (okvir P80 potrjen 1:1) · **P80 popravki ×11 (h56/h65/h16/Priložje + 6 priimkov!)** · **6 porok 15.2. + 2 sestrska dvojna poroka (Pegdirec isti dan + Musié 9 mesecev)** · vdove 4+1 (najmlajša 23!) · vpis 19 obadva lediga 43/42 (1. policist!) · Mündel-timeline h71 (mati † 7.9. → hči 21.11.) · prečrtano ~~Josef~~ (vpis 24) · **franz Dovgan 9 podpisov, 16 vpisov brez** · dispensacije ×6 + Eheverlags-Contract · vitals 528 · bloki 04455 = 11 · **P116 LEAD: poročna 1887**`
    : p115Errors.join("; "),
);

// ——— qa-p116: župnija Podzemelj — poročna knjiga 04455, polno leto 1887 (P116; nadaljevanje poročne linije P115!) ———
const p116Marr = HOUSE_VITALS.filter((h) => h.bookSignature === "04455");
const p116Errors: string[] = [];
if (p116Marr.length !== 168)
  p116Errors.push(`poročni bloki (04455) ≠ 142 (${p116Marr.length} — P121: + 4 bloki 1892; P122: + 5 bloki 1893; P123: + 4 bloki 1894; P124: + 3 bloki 1895; P125: + 3 bloki (h24+h14-1895ext + h18-1896); P126: + 9 blokov 1897; P127: + 9 blokov 1898; P128: + 6 blokov 1899; P132: + 12 blokov 1903; P133: + 8 blokov 1904; P134: + 13 blokov 1905 = 115!)`);
const p116M1887 = p116Marr.filter((h) => h.year === 1887);
const p116Houses1887 = p116M1887.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
if (p116Houses1887.join(",") !== "3,10,15,23,37,69,71")
  p116Errors.push(`hiše 1887 (04455) ≠ [3,10,15,23,37,69,71] — najdeno: ${p116Houses1887.join(",")} (P116: NOVI h23/h37/h69/h3/h10 + P80 sidri h71/h15)`);
// P116 re-read pini (1887 bloki)
const p116Pins: Array<[string, string]> = [
  ["71", "franz Dovgan"], ["71", "KAMBIČ"], ["71", "P116"],
  ["15", "FABLIĆ"], ["15", "GRIBLJE 23"], ["15", "P116"],
  ["23", "Brinec"], ["23", "NOVA"], ["23", "Milek"],
  ["37", "Rusić"], ["37", "NOVA"],
  ["69", "NOVA hiša"], ["69", "Straus"],
  ["3", "Križan"], ["3", "Rouy"],
  ["10", "Križe"], ["10", "NOVA"],
];
for (const [hn, pin] of p116Pins) {
  const blk = p116M1887.filter((h) => h.houseNo === hn);
  if (blk.length === 0) {
    p116Errors.push(`pin ${hn} (${pin}) — hiša ${hn} ni med 1887 bloki`);
    continue;
  }
  if (!blk.some((cur) => cur.whatSi.toLowerCase().includes(pin.toLowerCase())))
    p116Errors.push(`pin hiša ${hn} (${pin}) manjka`);
}
// stara branja iztekla (faza 1 + P80)
const p116Old = ["64? [~]", "»Šimeck", "»Štilnik", "»Gubeljas", "Zemelj 11", "vpis 20 nevesta »19«"];
for (const old of p116Old) {
  if (p116M1887.some((h) => h.whatSi.includes(old)))
    p116Errors.push(`staro branje še v 1887 blokih: »${old}«`);
}
// duhovniki 1887 (bloki): Dovgan ×5 (h71/h15/h23/h37/h69) + Rouy ×2 (h3/h10)
const p116Dovgan = p116M1887.filter((h) => h.whatSi.includes("Dovgan")).length;
if (p116Dovgan !== 5)
  p116Errors.push(`Dovgan podpisi 1887 blokov ≠ 5 (${p116Dovgan})`);
const p116Rouy = p116M1887.filter((h) => h.whatSi.includes("Rouy")).length;
if (p116Rouy !== 2)
  p116Errors.push(`Rouy podpisi 1887 blokov ≠ 2 (${p116Rouy} — h3/h10)`);
// NOVE hiše ×5 z oznako NOVA
const p116Nova = p116M1887.filter((h) => h.whatSi.includes("NOVA")).map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
if (p116Nova.join(",") !== "3,10,23,37,69")
  p116Errors.push(`NOVA hiše ≠ [3,10,23,37,69] (${p116Nova.join(",")})`);
// kumulativ: vitals 528 → 533 → 537 (P117: + 4 novih poročnih blokov h23-1888/h32/h33/h64-1888)
if (HOUSE_VITALS.length !== 685)
  p116Errors.push(`HOUSE_VITALS ≠ 537 (${HOUSE_VITALS.length} — P116: 528 + 5 = 533; P117: + 4 novih poročnih blokov (h23-1888/h32/h33/h64-1888) = 537!)`);
push(
  "qa-p116-parish-marriage-1887",
  "P116: ŽUPNIJA PODZEMELJ — POROČNA KNJIGA 04455 (1873–1922), POLNO LETO 1887 (issue #18; SAMPLE-TRANSCRIPTION-M1887; nadaljevanje poročne linije P115 = 1886): okvir POTRJEN — skeni 66–70 == Pag. 65–69 (Pag. == sken − 1 velja tudi v 66–71; **21 vpisov** = 4+4+3+3+7; glava 1888 že Pag. 70 = s71) — **21/21 vpisov OBOJESTRANSKO** + mega-zoom serija (~30 izrezov ×3–5); **P80/P115 RE-READ POPRAVKI ×8**: h15 ženin = Johann **FABLIĆ** (ne »Šambie«) + nevesta = GRIBLJE **23** (ne »29«!) + h71 mati neveste = née **KAMBIČ** (ne »Šambiè«) + mrliška h29-komentar (poroka na h23 — povezava ostaja pri materi roj. Milek) + faza-1: **h69** (ne »64« — h64 ostaja P115/1886!), **h10** (ne »19«), Zemelj **16** (ne »11«), **PRIMOSTEK** (ne »Šimeck« — vas obč. Semič!), **METLIKA** (ne »Štilnik«), **Grabrijan** (ne »Gubeljas«), **LERCH**, **Jos. ROUY**; **VELIKE NOVELE 1887: VPIS 16 = POROKA RAZPADLA?** (marginala »ni bil poročen, se razdrlo/razšlo? ravno pred poroko« — Jos. Rouy; datum + Befstände PRAZNI; 61-letni ženin Vincencij Hütlin Gradac 28 × Marjeta Dragan Metlika 2 = **isti mož kot vpis 21 Vinzenz KOTTLIN** (Gütlerbesitzer u. Wirt, Gradac 28, 61, okt.) — 1. abortirana poroka linije!) + **VPIS 14 = 1. SLOVENSKOJEZIČNI VPIS** (druga roka: »Matija«, »Maj«, »let« + slovenski Befunden!) + **ŽENITOVANJSKA ZGLASNICA = NOV DOKUMENT** (vpisi 14–21: Podzemelj št. 44 + 10, Gradac št. 3, Adlešiče št. 80, Podzemelj št. 12) + **BRATA FABLIĆ** (vpisa 1+4: Mathias 27 Boršt 44 + Johann 23 GRIBLJE 15, ISTI starši Nikolaus Fablić × Maria geb. Kambič!) + **TRETJA FABLIĆ** (vpis 6: Katharina 26, Zemelj 16 — mati Katharina geb. Turšič → 2. zakon očeta? dvom) + **SESTRSKI DVOJNI POROK Turšič** (vpisa 5+7, 13.2., ISTA starša = 3. v liniji cf. P115 Pegdirec+Musié!) + **DVE Katharina Klepec v 2 dneh** (v7 19-letna Boršt 16 + v9 22-letna Krasinec 17 — RAZLIČNI!) + **4× POROKA TOME** (v6/v10/v13/v18 — Gern 30 dvakrat!) + **BRATA STARAŠINIČ** (v9+v14, Krasinec 12) + **KRIŽAN × KRIŽE** (v20: Peter Križan 40 h3 × Catharina Križe 27 h10 = NOVI hiši!) + pustna masa 13./14.2. = 6 porok v 2 dneh + tuji ženini ×5 (Gradnik/Semič, Primostek ×2, Čedno selo/Adlešiče, **Borovnica/Franzdorf** [~] — nemška geografija!) + nevesti Metlika 2 (1. mesto!) + pfarr Črnomelj + duhovniki **Dovgan ×8 / Andreas Grieb Coop. ×4 / Jos. ROUY ×8 (= pisec slovenskih vpisov!) / PRAZNO 1 (vpis 13)** + dispensacije ×5 + 2× **Großjährigkeits-Schein** (v4+v11) + »Fraus-murd«-status uganka + hiša »1/2« (v1 Boginja vas) + marg. kalendarične oznake »a.« + tiskarna **Metlika** (»Druck v. Bertig v. Metlika«); **GRIBLJE: 4 poroke / 7 hiš — NARE 7 NOVIH DOKAZOV (h23 + h37 + h69? [~] + h3 + h10 NOVE + h71 + h15 sidri potrjeni)**; vitals **528 → 533** (+ 5 novih poročnih blokov h23/h37/h69/h3/h10); bloki 04455 = **16** (11 + 5 novih); **P117 LEAD: poročna 1888** (glava Pag. 70 = s71; vpisi 1–7/1888 že orisani — Michael BRINE h23! + 53×44 najstarejši par + vpis 6/1888 datum dvom); EXCLUDED: 8; skripta scripts/p116_parish_marriage_1887.py (I1–I11); status SAMPLE-TRANSCRIPTION-M1887",
  "P116: PARISH OF PODZEMELJ — MARRIAGE REGISTER 04455 (1873–1922), THE FULL YEAR 1887 (issue #18; SAMPLE-TRANSCRIPTION-M1887; the continuation of the marriage line P115 = 1886): the frame CONFIRMED — scans 66–70 == pages 65–69 (page == scan − 1 also holds in 66–71; **21 entries** = 4+4+3+3+7; the 1888 header already on p. 70 = s71) — **21/21 entries BOTH-SIDES** + the mega-zoom series (~30 crops ×3–5); **THE P80/P115 RE-READ CORRECTIONS ×8**: h15 groom = Johann **FABLIĆ** (not »Šambie«) + the bride = GRIBLJE **23** (not »29«!) + the h71 bride's mother = née **KAMBIČ** (not »Šambiè«) + the death-register h29 comment (the marriage at h23 — the link stays with the née-Milek mother) + the faza-1: **h69** (not »64« — h64 remains P115/1886!), **h10** (not »19«), Zemelj **16** (not »11«), **PRIMOSTEK** (not »Šimeck« — a village in the Semič municipality!), **METLIKA** (not »Štilnik«), **Grabrijan** (not »Gubeljas«), **LERCH**, **Jos. ROUY**; **THE BIG 1887 NOVELS: ENTRY 16 = THE WEDDING THAT FELL APART?** (the marginal note »he was not married, it fell apart right before the wedding« — Jos. Rouy; the date + Befstände EMPTY; the 61-year-old groom Vincencij Hütlin Gradac 28 × Marjeta Dragan Metlika 2 = **the same man as entry 21 Vinzenz KOTTLIN** (Gütlerbesitzer u. Wirt, Gradac 28, 61, Oct.) — the 1st aborted marriage of the line!) + **ENTRY 14 = THE 1ST SLOVENE-LANGUAGE ENTRY** (a different hand: »Matija«, »Maj«, »let« + the Slovene Befunden!) + **THE ŽENITOVANJSKA ZGLASNICA = A NEW DOCUMENT** (entries 14–21) + **THE FABLIĆ BROTHERS** (entries 1+4 with THE SAME parents!) + **THE THIRD FABLIĆ** (entry 6 — a different mother → the father's 2nd marriage? doubt) + **THE SIBLING DOUBLE WEDDING Turšič** (entries 5+7, Feb 13, THE SAME parents = the 3rd in the line!) + **TWO Katharina Klepec within 2 days** (v7 19 + v9 22 — DIFFERENT!) + **4× THE TOME MARRIAGE** + **THE STARAŠINIČ BROTHERS** (v9+v14, Krasinec 12) + **KRIŽAN × KRIŽE** (v20: the NEW houses h3 × h10!) + the carnival mass Feb 13/14 = 6 weddings in 2 days + foreign grooms ×5 (incl. **Borovnica/Franzdorf** [~] — German geography!) + the brides Metlika 2 (the 1st town!) + parish Črnomelj + the priests **Dovgan ×8 / Andreas Grieb Coop. ×4 / Jos. ROUY ×8 (= the scribe of the Slovene entries!) / EMPTY 1 (entry 13)** + dispensations ×5 + 2× **Großjährigkeits-Schein** + the »Fraus-murd«-status mystery + the house »1/2« + the marginal calendar letters »a.« + the printer **Metlika**; **GRIBLJE: 4 marriages / 7 houses — ALL 7 NEW EVIDENCE (h23 + h37 + h69? [~] + h3 + h10 NEW + h71 + h15 anchors confirmed)**; vitals **528 → 533** (+ the 5 new marriage blocks h23/h37/h69/h3/h10); the 04455 blocks = **16** (11 + 5 new); **the P117 LEAD: the marriages of 1888** (the header p. 70 = s71; entries 1–7/1888 already outlined — Michael BRINE h23! + the 53×44 oldest couple + the entry 6/1888 date doubt); EXCLUDED: 8; the script scripts/p116_parish_marriage_1887.py (I1–I11); status SAMPLE-TRANSCRIPTION-M1887",
  p116Errors.length === 0,
  p116Errors.length === 0
    ? `21 vpisov (okvir potrjen; Pag. == sken−1 tudi v 66–71) · **popravki ×8 (FABLIĆ/h23/h69/h10/Zemelj 16/PRIMOSTEK/METLIKA/ROUY!)** · **vpis 16 = POROKA RAZPADLA? (marginala + prazni Befstände + 61-letnik = isti mož kot vpis 21 Kottlin!)** · **vpis 14 = 1. SLOVENSKOJEZIČNI (druga roka!)** · ženitovanjska zglasnica (nov dokument, vpisi 14–21) · **brata Fablić + 3. Fablić (dvom)** · sestrski dvojni porok Turšič (5+7) · 2× Katharina Klepec · 4× Tome · brata Starašinič · **KRIŽAN × KRIŽE (h3 × h10 NOVI!)** · 6 porok 13./14.2. · tuji ženini ×5 (Franzdorf!) · duhovniki Dovgan 8 / Grieb 4 / **Rouy 8** / prazno 1 · Großjährigkeits-Schein ×2 · vitals 533 (528 + 5 P116) · bloki 04455 = 16 · **GRIBLJE 7/7 NOVIH DOKAZOV** · **P117 LEAD: poročna 1888 (Michael Brine h23!)**`
    : p116Errors.join("; "),
);

// ——— qa-p117: župnija Podzemelj — poročna knjiga 04455, polno leto 1888 (P117; 3. leto poročne linije!) ———
const p117Marr = HOUSE_VITALS.filter((h) => h.bookSignature === "04455" && h.year === 1888);
const p117Errors: string[] = [];
if (p117Marr.length !== 4)
  p117Errors.push(`poročni bloki 1888 (04455) ≠ 4 (${p117Marr.length})`);
const p117Houses = p117Marr.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
if (p117Houses.join(",") !== "23,32,33,64")
  p117Errors.push(`hiše 1888 (04455) ≠ [23,32,33,64] — najdeno: ${p117Houses.join(",")} (P117: NOVI h32 Straus/h33 Dehlič + h23-1888 BRATA Brinec + h64-1888 2. dokaz!)`);
// P117 pini (1888 bloki)
const p117Pins: Array<[string, string]> = [
  ["23", "BRINEC"], ["23", "brata"], ["23", "1888"],
  ["32", "Straus"], ["32", "Marcus"], ["32", "NOVA"],
  ["33", "Dehlič"], ["33", "NOVA"],
  ["64", "Marhiščar"], ["64", "Pegdirec"], ["64", "1888"],
];
for (const [hn, pin] of p117Pins) {
  const blk = p117Marr.filter((h) => h.houseNo === hn);
  if (blk.length === 0) {
    p117Errors.push(`pin ${hn} (${pin}) — hiša ${hn} ni med 1888 bloki`);
    continue;
  }
  if (!blk.some((cur) => cur.whatSi.toLowerCase().includes(pin.toLowerCase())))
    p117Errors.push(`pin hiša ${hn} (${pin}) manjka`);
}
// h23-1887 popravek: Michael → Mathias Brinec (re-read)
const p116MarrH23 = HOUSE_VITALS.filter((h) => h.bookSignature === "04455" && h.year === 1887 && h.houseNo === "23");
if (p116MarrH23.length !== 1)
  p116Errors.push(`h23 1887 blok ≠ 1 (${p116MarrH23.length})`);
if (p116MarrH23.some((h) => h.whatSi.includes("Michael BRINE")))
  p116Errors.push("h23 1887: staro branje »Michael BRINE« še prisotno (P117 popravek → Mathias!)");
if (!p116MarrH23.some((h) => h.whatSi.includes("BRATA")))
  p116Errors.push("h23 1887: pini BRATA manjka (P117)");
// stara branja iztekla (faza 1 → faza 2)
const p117Old = ["Michael BRINE", "GRIBLJE 26 [~]"];
for (const old of p117Old) {
  if (p117Marr.some((h) => h.whatSi.includes(old)))
    p117Errors.push(`staro branje še v 1888 blokih: »${old}«`);
}
// kumulativ: vitals 533 → 537 (P117: + 4 novih poročnih blokov h23-1888/h32/h33/h64-1888)
if (HOUSE_VITALS.length !== 685)
  p117Errors.push(`HOUSE_VITALS ≠ 554 (${HOUSE_VITALS.length} — P117: 537; P118: 544; P119: 548; P120: 550; P121: + 4 novih poročnih blokov 1892 = 554!)`);
// kumulativ blokov 04455 = 20 (p116Marr = filter 04455 brez leta)
if (p116Marr.length !== 168)
  p117Errors.push(`bloki 04455 skupaj ≠ 142 (${p116Marr.length} — P120: + 2 bloki 1891; P121: + 4 bloki 1892; …; P126: + 9 blokov 1897; P127: + 9 blokov 1898; P128: + 6 blokov 1899; P132: + 12 blokov 1903; P133: + 8 blokov 1904; P134: + 13 blokov 1905 = 115!)`);
push(
  "qa-p117-parish-marriage-1888",
  "P117: ŽUPNIJA PODZEMELJ — POROČNA KNJIGA 04455, POLNO LETO 1888 (issue #18; SAMPLE-TRANSCRIPTION-M1888; 3. leto poročne linije P115 = 1886 → P116 = 1887 → P117 = 1888): okvir POTRJEN — skeni 71–74 == Pag. 70–73 (Pag. == sken − 1 velja v 66–76; GEOMETRIJA LANDSCAPE 2500×1800: levi list = Braütigam+Brant, desni = Eltern/Befände/Befunden/Pfarrer!) — **20 vpisov** = 7+3+6+4; glava 1889 = Pag. 74 = s75 BREZ velike glave [~] (novela-kandidat); **20/20 vpisov OBOJESTRANSKO** + mega-zoom ×4–6; **FAZA-1 POPRAVKI ×11**: v1 Zajčji vrh?/Pf. Toplice? + Ana HRASOVEC (ne »Krajovce«!) + v2 MATHIAS (ne »Michael«!) Brinec + v3 Georg MRAVINEC?/Ana POŽEK?/**58!** (h21 1. dokaz!) + v4 KNURE?/Škrilje? + v5 MARENTIČ?/STAJNIĆ? + v6 **~~März~~→APRIL 30** (oris »30.1.« napačen!) + Johan FILAK? (ne »Šoltar«!) + v7 Mathias STRAUS (ne »Kravce«!) h32 + v8 JAKLIČ? (ne »Josejc«) + v9 **17.6.** (ne »9.6.«) + v10 **ČRNOMELJ 63** (1. mesto!)/18.7./Perie?/Lasič + v12 **GRIBLJE 64** (P82 »26« REŠEN!) + v13 MARTIN Zugelj/JAKŠA? + v14 MURN **58**/SUSTEK/Gradac 12? + v15 VRBANEK?/**Bubnjarci-Pf. Žakanje**/Zemelj? 17 + v16 SAJHNER?/Sayhnec? + v17 KOŠIR?/POVŠE **17**/Gradac 85+Verden?/Pf. Toplice + v18 TASIČ? (ne »Javnič«!)/HARASIMIČ? + v19 JAKLIČ? (ne »Javkič«!)/Zemelj? 25 + v20 KOHAMIČ?/Cerkvišče 22/**28**; **VELIKE NOVELE: DUHOVNIK JOS. RAUY PROVISOR ×20/20** (nov status; ≈ P116 »Rouy« = ista oseba? [~]) + **v9 NAJBOGATEJŠI BEFUNDEN LINIJE** (6 dokumentov: zglasnica št. 5 + Verzeichnis? 2.6. Z: 5752 + RGBl № 153 6.4.1882 + DISPENS 3. stopnje Ordinariat 12.6. Z: 1109 + k.k. Bez.-Hauptm. 14.6. Z: 4574 + Ordin. Laibach 17.6. № 1143 + mündliche Einwilligung = poroka ISTI dan!) + **SESTRI CERNIČ POTRJENE** (v6+v16, isti starši, obe h42!) + **BRATA BRINEC h23** (1887 Maria + 1888 Mathias, isti starši!) + **STRAUS-VEJA h32** (oče MARCUS × Dragoševič?; cf. h71 oče Mathias!) + **KOTTLIN-PRIČA** (v17 = 1887 v21 ženin — 1. cross-link!) + **PEGDIREC ×9+** (v12 mati Anna + priča Peter = P115 v5 ženin!) + mrežni priimki: PLUT ×3 / JAKLIČ ×4 / FILAK ×4 / KAMBIČ ×4 / HRIŽAN ×3 / DRAGOŠ ×3 + **TAUF-NOVELA ×3** (v10 48-letnik + v14 Sustek 43 + v15 Vrbanek 24) + **2× 58-LETNI ŽENIN** (v3+v14) + vdova 24 (v11 + MRTVAŠKI LIST Semič!) + nevesta 17 (v17) + žena starejša ×2 (v18: 34×25; v20: 37×28) + **4 TUJE ŽUPNIJE** (Toplice? ×2, Adlešiče, Semič, **Žakanje ~45 km!**) + mesto Črnomelj + Borovnica ×2 + Rudolfswert (Novo mesto) + **NOVI DOKUMENTNI TIPI ×6** (mrtvaški list + Communalzettel Gradac + Nedelovna svjedodžba proglašenstva broj 2979 + virna izjava Metlika/polnoletnost + §102 + Wehrmannsschein?) + 3 dvojni dnevi (6.2. ×2 / 12.11. ×2 / 19.11. ×2) + mati ženina PRAZNA (v14 pika!) + statusi-neznank ×6 (novela-kandidat); **GRIBLJE: 4 poroke / 5 hiš** (h23 ×2 dokaza!; h32 + h33 NOVI; h21 + h64 1./2. dokaza); vitals **533 → 537** (+ 4 novih poročnih blokov h23-1888/h32/h33/h64-1888); bloki 04455 = **20**; **P118 LEAD: poročna 1889** (s75 = glava BREZ velike glave [~]; vpisi 1–10 orisani — h32 ×2 v 2 letih + h30 NOVA ženin 60 LET!); EXCLUDED: 10; skripta scripts/p117_parish_marriage_1888.py (I1–I11); status SAMPLE-TRANSCRIPTION-M1888",
  "P117: PARISH OF PODZEMELJ — MARRIAGE REGISTER 04455, THE FULL YEAR 1888 (issue #18; SAMPLE-TRANSCRIPTION-M1888; the 3rd year of the marriage line P115 = 1886 → P116 = 1887 → P117 = 1888): the frame CONFIRMED — scans 71–74 == pages 70–73 (page == scan − 1 holds in 66–76; GEOMETRY LANDSCAPE 2500×1800: the left leaf = Braütigam+Brant, the right = Eltern/Befände/Befunden/Pfarrer!) — **20 entries** = 7+3+6+4; the 1889 header = p. 74 = s75 WITHOUT a large heading [~] (a novela candidate); **20/20 entries BOTH-SIDES** + mega-zoom ×4–6; **THE FAZA-1 CORRECTIONS ×11**: v1 Zajčji vrh?/Pf. Toplice? + Ana HRASOVEC (not »Krajovce«!) + v2 MATHIAS (not »Michael«!) Brinec + v3 Georg MRAVINEC?/Ana POŽEK?/**58!** (h21 the 1st evidence!) + v4 KNURE?/Škrilje? + v5 MARENTIČ?/STAJNIĆ? + v6 **~~März~~→APRIL 30** (the outline »30.1.« wrong!) + Johan FILAK? (not »Šoltar«!) + v7 Mathias STRAUS (not »Kravce«!) h32 + v8 JAKLIČ? (not »Josejc«) + v9 **Jun 17** (not »Jun 9«) + v10 **ČRNOMELJ 63** (the 1st town!)/18.7./Perie?/Lasič + v12 **GRIBLJE 64** (the P82 »26« RESOLVED!) + v13 MARTIN Zugelj/JAKŠA? + v14 MURN **58**/SUSTEK/Gradac 12? + v15 VRBANEK?/**Bubnjarci-Pf. Žakanje**/Zemelj? 17 + v16 SAJHNER?/Sayhnec? + v17 KOŠIR?/POVŠE **17**/Gradac 85+Verden?/Pf. Toplice + v18 TASIČ? (not »Javnič«!)/HARASIMIČ? + v19 JAKLIČ? (not »Javkič«!)/Zemelj? 25 + v20 KOHAMIČ?/Cerkvišče 22/**28**; **THE BIG NOVELS: PRIEST JOS. RAUY PROVISOR ×20/20** (a new status; ≈ the P116 »Rouy« = the same person? [~]) + **v9 THE RICHEST BEFUNDEN OF THE LINE** (6 documents: the announcement no. 5 + Verzeichnis? Jun 2 Z: 5752 + RGBl № 153 Apr 6, 1882 + A 3rd-class DISPENS Ordinariat Jun 12 Z: 1109 + k.k. Bez.-Hauptm. Jun 14 Z: 4574 + Ordin. Laibach Jun 17 № 1143 + the mündliche Einwilligung = the wedding THE SAME DAY!) + **THE CERNIČ SISTERS CONFIRMED** (v6+v16, the same parents, both h42!) + **THE BRINEC BROTHERS at h23** (1887 Maria + 1888 Mathias, the same parents!) + **THE STRAUS BRANCH h32** (father MARCUS × Dragoševič?; cf. h71 father Mathias!) + **THE KOTTLIN WITNESS** (v17 = the 1887 v21 groom — the 1st cross-link!) + **PEGDIREC ×9+** (v12 mother Anna + witness Peter = the P115 v5 groom!) + the network surnames: PLUT ×3 / JAKLIČ ×4 / FILAK ×4 / KAMBIČ ×4 / HRIŽAN ×3 / DRAGOŠ ×3 + **THE TAUF-NOVEL ×3** (v10 the 48-year-old + v14 Sustek 43 + v15 Vrbanek 24) + **2× THE 58-YEAR-OLD GROOM** (v3+v14) + the widow 24 (v11 + THE DEATH CERTIFICATE Semič!) + the bride 17 (v17) + the older wife ×2 (v18: 34×25; v20: 37×28) + **4 FOREIGN PARISHES** (Toplice? ×2, Adlešiče, Semič, **Žakanje ~45 km!**) + the town Črnomelj + Borovnica ×2 + Rudolfswert (Novo mesto) + **NEW DOCUMENT TYPES ×6** (the death certificate + the Communalzettel Gradac + the Sunday proclamation certificate broj 2979 + the Metlika court age-of-majority declaration + §102 + the Wehrmannsschein?) + 3 double days (Feb 6 ×2 / Nov 12 ×2 / Nov 19 ×2) + the groom's mother EMPTY (v14 a dot!) + the status-unknowns ×6 (a novela candidate); **GRIBLJE: 4 marriages / 5 houses** (h23 ×2 evidence!; h32 + h33 NEW; h21 + h64 the 1st/2nd evidence); vitals **533 → 537** (+ the 4 new marriage blocks h23-1888/h32/h33/h64-1888); the 04455 blocks = **20**; **THE P118 LEAD: the marriages of 1889** (s75 = a heading WITHOUT the large heading [~]; entries 1–10 outlined — h32 ×2 in 2 years + h30 NEW groom 60 YEARS!); EXCLUDED: 10; the script scripts/p117_parish_marriage_1888.py (I1–I11); status SAMPLE-TRANSCRIPTION-M1888",
  p117Errors.length === 0,
  p117Errors.length === 0
    ? `20 vpisov (okvir potrjen; Pag. == sken−1 tudi v 71–76; LANDSCAPE!) · **popravki ×11 (Mathias Brinec/STRANS h32/h64-REŠEN/APRIL 30/Tasič/Jaklič ×2/Črnomelj/Zemelj ×2/Murn 58!)** · **Rauy provisor ×20** · **v9 najbogatejši Befunden (6 dokumentov + poroka isti dan)** · sestri Cernič (v6+v16!) · brata Brinec h23 · Straus-veja h32 (Marcus!) · Kottlin-priča v17 · Pegdirec ×9+ (priča Peter = P115 ženin!) · mreže Plut ×3/Jaklič ×4/Filak ×4/Kambič ×4 · Tauf-novela ×3 · 2× 58-letnik · vdova 24 (mrtvaški list!) · nevesta 17 · 4 tuje župnije (Žakanje 45 km!) · novi dokumenti ×6 · vitals 537 · bloki 04455 = 20 · **GRIBLJE 5/5 NOVIH DOKAZOV** · **P118 LEAD: poročna 1889 (s75 brez glave [~]; h30 ženin 60!)**`
    : p117Errors.join("; "),
);

// ——— qa-p118: župnija Podzemelj — poročna knjiga 04455, polno leto 1889 (P118; 4. leto poročne linije!) ———
const p118Marr = HOUSE_VITALS.filter((h) => h.bookSignature === "04455" && h.year === 1889);
const p118Errors: string[] = [];
if (p118Marr.length !== 7)
  p118Errors.push(`poročni bloki 1889 (04455) ≠ 7 (${p118Marr.length})`);
const p118Houses = p118Marr.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
if (p118Houses.join(",") !== "21,30,32,40,54,7,87".split(",").sort((a, b) => Number(a) - Number(b)).join(","))
  p118Errors.push(`hiše 1889 (04455) ≠ [7,21,30,32,40,54,87] — najdeno: ${p118Houses.join(",")} (P118: 1. poročni dokazi h7/h21/h30/h40/h54/h87 + h32 2. dokaz!)`);
// P118 pini (1889 bloki)
const p118Pins: Array<[string, string]> = [
  ["32", "Urb"], ["32", "Perdinec"], ["32", "Dohlič"],
  ["40", "Perdinec"], ["40", "Perdinec-mreža"],
  ["21", "Požek"], ["21", "Dragoš"],
  ["54", "Simec"], ["54", "Perdinec"],
  ["7", "Totter"], ["7", "Adlešiče"],
  ["30", "Milek"], ["30", "60"],
  ["87", "Perdinec"], ["87", "Klejpec"], ["87", "Gliha"],
];
for (const [hn, pin] of p118Pins) {
  const blk = p118Marr.filter((h) => h.houseNo === hn);
  if (blk.length === 0) {
    p118Errors.push(`pin ${hn} (${pin}) — hiša ${hn} ni med 1889 bloki`);
    continue;
  }
  if (!blk.some((cur) => cur.whatSi.toLowerCase().includes(pin.toLowerCase())))
    p118Errors.push(`pin hiša ${hn} (${pin}) manjka`);
}
// stara faza-1 branja iztekla (oris → faza 2; sklici na popravek »ne »X««/»oris ... = popravek« dovoljeni)
const p118Old = ["Mech", "Kleklvec", "Mulek", "Simic? GRIBLJE 24", "Mulek?/Melek"];
for (const old of p118Old) {
  for (const h of p118Marr) {
    let i = h.whatSi.indexOf(old);
    let stale = false;
    while (i !== -1) {
      const ctx = h.whatSi.slice(Math.max(0, i - 60), i);
      if (!["ne »", "popravek", "faza-1", "oris »"].some((t) => ctx.includes(t))) {
        stale = true;
        break;
      }
      i = h.whatSi.indexOf(old, i + 1);
    }
    if (stale) p118Errors.push(`staro faza-1 branje še v 1889 blokih: »${old}«`);
  }
}
// duhovniki 1889 (bloki): Rauy ×6 + Gliha coop. ×2 (h30+h87 isti vpis!)
const p118Rauy = p118Marr.filter((h) => h.whatSi.includes("Rauy")).length;
if (p118Rauy !== 6)
  p118Errors.push(`Rauy podpisi 1889 blokov ≠ 6 (${p118Rauy})`);
const p118Gliha = p118Marr.filter((h) => h.whatSi.toLowerCase().includes("gliha")).length;
if (p118Gliha !== 2)
  p118Errors.push(`Gliha coop. bloki ≠ 2 (${p118Gliha} — h30/h87 isti vpis 8!)`);
// oznake dokazov 1889: h7/h30/h40/h54/h87 = "1. poročni dokaz" (5) + h21/h32 = "2. poročni dokaz"
const p118Novo = p118Marr.filter((h) => h.whatSi.includes(`1. poročni dokaz h${h.houseNo}`) || h.whatSi.includes(`1. POROČNI dokaz h${h.houseNo}`)).map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
if (p118Novo.join(",") !== "30,40,54,7,87".split(",").sort((a, b) => Number(a) - Number(b)).join(","))
  p118Errors.push(`1.-poročni-dokaz hiše ≠ [7,30,40,54,87] (${p118Novo.join(",")})`);
if (!p118Marr.some((h) => h.houseNo === "21" && h.whatSi.includes("2. poročni dokaz h21")))
  p118Errors.push("h21-1889: oznaka »2. poročni dokaz« manjka");
if (!p118Marr.some((h) => h.houseNo === "32" && h.whatSi.includes("2. poročni dokaz h32")))
  p118Errors.push("h32-1889: oznaka »2. poročni dokaz h32« manjka");
// kumulativ: vitals 537 → 544 (P118: + 7 novih poročnih blokov 1889)
if (HOUSE_VITALS.length !== 685)
  p118Errors.push(`HOUSE_VITALS ≠ 554 (${HOUSE_VITALS.length} — P118: 544; P119: 548; P120: 550; P121: + 4 novih poročnih blokov 1892 = 554!)`);
// kumulativ blokov 04455 = 27
if (p116Marr.length !== 168)
  p118Errors.push(`bloki 04455 skupaj ≠ 142 (${p116Marr.length} — P121: + 4 bloki 1892; …; P126: + 9 blokov 1897; P127: + 9 blokov 1898; P128: + 6 blokov 1899; P132: + 12 blokov 1903; P133: + 8 blokov 1904; P134: + 13 blokov 1905 = 115!)`);
push(
  "qa-p118-parish-marriage-1889",
  "P118: ŽUPNIJA PODZEMELJ — POROČNA KNJIGA 04455, POLNO LETO 1889 (issue #18; SAMPLE-TRANSCRIPTION-M1889; 4. leto poročne linije P115 = 1886 → P116 = 1887 → P117 = 1888 → P118 = 1889): okvir POTRJEN — skeni 75–76 == Pag. 74–75 (Pag. == sken − 1 velja v 71–76; LANDSCAPE geometrija ~2471–2478×1800; leto 1889 = 6+4 vpisov; glava 1889 = Pag. 74 BREZ velike glave [~] — novela-kandidat POTRJEN; vrstice restart na 1 = 3. potrditev novele P83; glava 1890 že Pag. 76 = s77 — 1890 ima ≥ 16 vpisov (s77: 1–6, s78: 7–11, s79: 12–16!), glava 1891 = Pag. 79 = s80) — **10 vpisov OBOJESTRANSKO** + 19 mega-zoomov ×3–6; **faza-1 oris popravki ×24** (vsak vpis vsaj 1 — najbolj napačen oris linije!): v1 Cerkvišče 32/Štubljar 13 (ne »Cetvrtje 33/Perhličar 15«) + v2 **URB** (ne »Mech«!) × **PERDINEC h40** (ne »Lechne h16«!) + v3 **POŽEK** (ne »Perich«) × **ANNA SIMEC h54** (ne »Maria Simic h24«!) + v4 starosti 30/23 (ne 36/33) + v5 **ŠOPČIČ Gradac 49, 66 LET** (ne »Šupanc 19, 46«!) × Zaštava 8 Pf. Črnomelj (ne »Žabjak«) + v6 Cerkvišče 35 (ne »Solvenia«) + v7 **23.9.** (ne 3.9.) + v8 **MILEK** (ne »Mulek/Melek«) × **KLEJPEC** (ne »Kleklvec«) **GRIBLJE 87** (ne 31!) 14.10. (ne 10.10.) + v9 **SENICA/Zimmermann** (ne »Šonca«) + v10 h65 (ne 6); **VELIKE NOVELE 1889: NAJSTAREJŠI ŽENIN VSEH ČASOV = 66 LET** (v5; rekordi prej: 61 Kottlin 1887 + 58 ×2 1888!) + **37-letna razlika** (v8: 60 × 23!) + **v9 OBA OČETA PRAZNA = 1. NEZAKONSKA PAR LINIJE** + **v7 brez duhovnikovega podpisa** (namesto njega varuh MATIJA NOVAK — pro tutore delegato?!) + **v8 2. DUHOVNIK AMBROSIJ GLIHA coop.** (konec monopola Rauy: 8 + 1 + 1 prazen!) + **⅓ GÜTL NOV ULOMEK** (v8 Marcus Perdinec!) + **MAGD ×2 = NOV STATUS NEVESTE** (v5 + v9; faza-1 »Mayr/Mayst« = Kurrent »Mayd«!) + **ZIMMERMANN ×2 NOV POKLIC** (v6 + v9) + **PFLEGER NOV STATUS PRIČE** (v9 Anton Toma — veza z nezakonsko paro!) + **MLADOLETNOST-NOVELA 7/10** (vse neveste < 24 s privolitvenim dokumentom: sodišča Črnomelj ×2 + Metlika ×2 + väterliche ×2 + v10 4 dokumenti; v1 edina brez) + **ZGŁASNICA ×10/10 = 100%** (nov standard; v1 datirana 25.10.1888 — 3,5 mes. vnaprej!) + **ZIMSKA VRZEL 3,5 MESECA** (3.6. → 23.9. — rekord linije!) + dvojni dan 11.2. ×2 + NOVI DOKUMENTNI TIPI ×5 (varuhovo dovoljenje + oznamni list župn. urada + Amtskindschaft-Pfarramt + G?upjäftigit-Knitt-Etbürning/Klärning [~] + Genehm. Landesreg. Laibach); **mreže: PERDINEC ×3 / POŽEK ×3 / NOVAK ×2 (varuh v7 ↔ nevesta v10!) / MILEK (1887↔1889) / DOHLIČ (1888↔1889) / TOME (1887 ×4 → 1889) / DRAGOŠ / ZUGELJ / GRABRIJAN** + tuje župnije ×4 (Adlešiče + Pf. Črnomelj + Pf. Toplice + Pf. Otok? [~]) + sodna mreža ×4 (Črnomelj Z:1118/Z:8062 + Metlika VIII.889/119 + IV/878) + Ljubljana ×2 (Landesreg. Z:6758 + Ordinariat št. 2515) + Bez.-Hauptm. Črnomelj Z:9540 (cf. 1888 Z:4574!); **GRIBLJE: 4 poroke / 7 hiš — 5 × 1. POROČNI DOKAZ (h7/h30/h40/h54/h87 — vse že v krstni 04105!) + h21 + h32 2. dokaza (obe ×2 v 2 letih po 1888!)**; vitals **537 → 544** (+ 7 novih poročnih blokov h32/h40/h21/h54/h7/h30/h87-1889); bloki 04455 = **27**; **P119 LEAD: poročna 1890** (s77 = Pag. 76 glava + v1–6; s78 = v7–11; s79 = v12–16 — ≥ 16 vpisov = največje leto linije!; glava 1891 = s80; v1 = Griblje 61 × Griblje 10!; v6 = Griblje 53 × Otok 20 Hrižan?; v15 = Griblje 61 Parst? × Dragoš 5!); EXCLUDED: 10; skripta scripts/p118_parish_marriage_1889.py (I1–I11); status SAMPLE-TRANSCRIPTION-M1889",
  "P118: PARISH OF PODZEMELJ — MARRIAGE REGISTER 04455, THE FULL YEAR 1889 (issue #18; SAMPLE-TRANSCRIPTION-M1889; the 4th year of the marriage line P115 = 1886 → P116 = 1887 → P117 = 1888 → P118 = 1889): the frame CONFIRMED — scans 75–76 == pages 74–75 (page == scan − 1 holds in 71–76; LANDSCAPE geometry ~2471–2478×1800; the year 1889 = 6+4 entries; the 1889 header = p. 74 WITHOUT a large heading [~] — the novela candidate CONFIRMED; the rows restart at 1 = the 3rd confirmation of the P83 novela; the 1890 header already on p. 76 = s77 — 1890 has ≥ 16 entries (s77: 1–6, s78: 7–11, s79: 12–16!), the 1891 header = p. 79 = s80) — **10 entries BOTH-SIDES** + 19 mega-zooms ×3–6; **the faza-1 outline corrections ×24** (every entry at least 1 — the most wrong outline of the line!): v1 Cerkvišče 32/Štubljar 13 (not »Cetvrtje 33/Perhličar 15«) + v2 **URB** (not »Mech«!) × **PERDINEC h40** (not »Lechne h16«!) + v3 **POŽEK** (not »Perich«) × **ANNA SIMEC h54** (not »Maria Simic h24«!) + v4 ages 30/23 (not 36/33) + v5 **ŠOPČIČ Gradac 49, 66 YEARS** (not »Šupanc 19, 46«!) × Zaštava 8 Pf. Črnomelj (not »Žabjak«) + v6 Cerkvišče 35 (not »Solvenia«) + v7 **Sep 23** (not Sep 3) + v8 **MILEK** (not »Mulek/Melek«) × **KLEJPEC** (not »Kleklvec«) **GRIBLJE 87** (not 31!) Oct 14 (not Oct 10) + v9 **SENICA/Zimmermann** (not »Šonca«) + v10 h65 (not 6); **THE BIG 1889 NOVELS: THE OLDEST GROOM OF ALL TIME = 66 YEARS** (v5; previous records: 61 Kottlin 1887 + 58 ×2 1888!) + **the 37-year gap** (v8: 60 × 23!) + **v9 BOTH FATHERS EMPTY = THE 1st ILLEGITIMATE COUPLE OF THE LINE** + **v7 without the priest's signature** (instead the guardian MATIJA NOVAK — pro tutore delegato?!) + **v8 the 2nd PRIEST AMBROSIJ GLIHA coop.** (the end of the Rauy monopoly: 8 + 1 + 1 empty!) + **⅓ SMALLHOLDER A NEW FRACTION** (v8 Marcus Perdinec!) + **MAGD ×2 = A NEW BRIDE STATUS** (v5 + v9; the faza-1 »Mayr/Mayst« = Kurrent »Mayd«!) + **ZIMMERMANN ×2 A NEW PROFESSION** (v6 + v9) + **PFLEGER A NEW WITNESS STATUS** (v9 Anton Toma — a link to the illegitimate couple!) + **THE MINORITY-NOVELA 7/10** (every bride < 24 with a consent document: the courts Črnomelj ×2 + Metlika ×2 + väterliche ×2 + v10 4 documents; v1 the only one without) + **THE ANNOUNCEMENT ×10/10 = 100%** (a new standard; v1 dated Oct 25, 1888 — 3.5 months in advance!) + **THE WINTER GAP 3.5 MONTHS** (Jun 3 → Sep 23 — the line's record!) + the double day Feb 11 ×2 + NEW DOCUMENT TYPES ×5 (the guardian's permission + the parish-office announcement list + the Amtskindschaft-Pfarramt + G?upjäftigit-Knitt-Etbürning/Klärning [~] + the Genehm. of the Landesreg. Laibach); **the networks: PERDINEC ×3 / POŽEK ×3 / NOVAK ×2 (the v7 guardian ↔ the v10 bride!) / MILEK (1887↔1889) / DOHLIČ (1888↔1889) / TOME (1887 ×4 → 1889) / DRAGOŠ / ZUGELJ / GRABRIJAN** + foreign parishes ×4 (Adlešiče + Pf. Črnomelj + Pf. Toplice + Pf. Otok? [~]) + the court network ×4 (Črnomelj Z:1118/Z:8062 + Metlika VIII.889/119 + IV/878) + Ljubljana ×2 (the Landesreg. Z:6758 + the Ordinariat no. 2515) + the Bez.-Hauptm. Črnomelj Z:9540 (cf. 1888 Z:4574!); **GRIBLJE: 4 marriages / 7 houses — 5 × the 1st MARRIAGE EVIDENCE (h7/h30/h40/h54/h87 — all already in the baptism register 04105!) + h21 + h32 the 2nd evidences (both ×2 in 2 years after 1888!)**; vitals **537 → 544** (+ the 7 new marriage blocks h32/h40/h21/h54/h7/h30/h87-1889); the 04455 blocks = **27**; **THE P119 LEAD: the marriages of 1890** (s77 = p. 76 header + v1–6; s78 = v7–11; s79 = v12–16 — ≥ 16 entries = the biggest year of the line!; the 1891 header = s80; v1 = Griblje 61 × Griblje 10!; v6 = Griblje 53 × Otok 20 Hrižan?; v15 = Griblje 61 Parst? × Dragoš 5!); EXCLUDED: 10; the script scripts/p118_parish_marriage_1889.py (I1–I11); status SAMPLE-TRANSCRIPTION-M1889",
  p118Errors.length === 0,
  p118Errors.length === 0
    ? `10 vpisov (okvir potrjen; Pag. == sken−1 v 71–76; LANDSCAPE; glava brez velike glave [~] POTRJENA) · **popravki ×24 (Urb/Perdinec h40/Požek/Simec h54/Šopčič 66!/Milek/Klejpec/h87/23.9./14.10!)** · **66-letni ženin = rekord linije!** · 37-letna razlika · **v9 nezakonska par (oba očeta prazna!)** · v7 podpis varuh Novak (brez duhovnika!) · v8 Gliha coop. (2. duhovnik!) · ⅓ Gütl nov ulomek · Magd ×2 · Zimmermann ×2 · Pfleger priča · mladoletnost-novela 7/10 · zgłasnica ×10/10 · zimska vrzel 3,5 mes. · mreže Perdinec ×3/Požek ×3/Novak ×2/Milek/Dohlič/Tome · sodna mreža ×4 + Ljubljana ×2 · vitals 544 · bloki 04455 = 27 · **GRIBLJE 7 hiš (5 × 1. poročni dokaz + h21 + h32 2. dokaza!)** · **P119 LEAD: poročna 1890 (s77+; ≥ 16 vpisov!)**`
    : p118Errors.join("; "),
);

// ——— qa-p119: župnija Podzemelj — poročna knjiga 04455, polno leto 1890 (P119; 5. leto poročne linije!) ———
const p119Marr = HOUSE_VITALS.filter((h) => h.bookSignature === "04455" && h.year === 1890);
const p119Errors: string[] = [];
if (p119Marr.length !== 4)
  p119Errors.push(`poročni bloki 1890 (04455) ≠ 4 (${p119Marr.length})`);
const p119Houses = p119Marr.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
if (p119Houses.join(",") !== "10,53,61,91")
  p119Errors.push(`hiše 1890 (04455) ≠ [10,53,61,91] — najdeno: ${p119Houses.join(",")} (P119: h91+h10 v1, h53 v6 NOVA, h61 v15!)`);
// P119 pini (1890 bloki)
const p119Pins: Array<[string, string]> = [
  ["91", "Muc"], ["91", "Vgornjed"], ["91", "Japplič"],
  ["10", "Kure"], ["10", "Magd"], ["10", "Špala"],
  ["53", "Perdinec"], ["53", "NOVA HIŠA"], ["53", "Hrižan"], ["53", "Otok"],
  ["61", "Požek"], ["61", "Dragoš"], ["61", "Straus"], ["61", "Muc bajtar"],
];
for (const [n, pin] of p119Pins) {
  const blk = p119Marr.filter((h) => h.houseNo === n);
  if (blk.length === 0) {
    p119Errors.push(`pin ${n} (${pin}) — hiša ${n} ni med 1890 bloki`);
    continue;
  }
  if (!blk.some((cur) => cur.whatSi.toLowerCase().includes(pin.toLowerCase())))
    p119Errors.push(`pin hiša ${n} (${pin}) manjka`);
}
// duhovniki 1890 (bloki): Rauy ×4 (vsi Griblje vpisi; Bulovec v4 = brez bloka!)
const p119Rauy = p119Marr.filter((h) => h.whatSi.includes("Rauy")).length;
if (p119Rauy !== 4)
  p119Errors.push(`Rauy podpisi 1890 blokov ≠ 4 (${p119Rauy})`);
// oznake dokazov 1890: h53 = "NOVA HIŠA/1. dokaz" + h10 = "2. poročni dokaz" + h91/h61 = "2. familia"
if (!p119Marr.some((h) => h.houseNo === "53" && h.whatSi.includes("NOVA HIŠA")))
  p119Errors.push("h53-1890: oznaka »NOVA HIŠA« manjka");
if (!p119Marr.some((h) => h.houseNo === "10" && h.whatSi.includes("2. poročni dokaz h10")))
  p119Errors.push("h10-1890: oznaka »2. poročni dokaz« manjka");
if (!p119Marr.some((h) => h.houseNo === "91" && h.whatSi.includes("2. familia")))
  p119Errors.push("h91-1890: oznaka »2. familia« manjka");
if (!p119Marr.some((h) => h.houseNo === "61" && h.whatSi.includes("2. familia")))
  p119Errors.push("h61-1890: oznaka »2. familia« manjka");
// kumulativ: vitals 544 → 550 (P119: + 4 blokov 1890; P120: + 2 bloki 1891)
if (HOUSE_VITALS.length !== 685)
  p119Errors.push(`HOUSE_VITALS ≠ 554 (${HOUSE_VITALS.length} — P118: 544; P119: 548; P120: 550; P121: + 4 novih poročnih blokov 1892 = 554!)`);
// kumulativ blokov 04455 = 33 (P119: 31; P120: + 2 bloki 1891)
if (p116Marr.length !== 168)
  p119Errors.push(`bloki 04455 skupaj ≠ 142 (${p116Marr.length} — P121: + 4 bloki 1892; …; P126: + 9 blokov 1897; P127: + 9 blokov 1898; P128: + 6 blokov 1899; P132: + 12 blokov 1903; P133: + 8 blokov 1904; P134: + 13 blokov 1905 = 115!)`);
push(
  "qa-p119-parish-marriage-1890",
  "P119: ŽUPNIJA PODZEMELJ — POROČNA KNJIGA 04455, POLNO LETO 1890 (issue #18; SAMPLE-TRANSCRIPTION-M1890; 5. leto poročne linije P115 = 1886 → P116 = 1887 → P117 = 1888 → P118 = 1889 → P119 = 1890): okvir POTRJEN — skeni 77–79 == Pag. 76–78 (Pag. == sken − 1, 5. potrditev; LANDSCAPE ~2484–2525×1800; velika glava »Traunungs=Buch« na Pag. 76!) — **16 vpisov = NAJVEČJE LETO LINIJE** (1886:7 → 1887:21 → 1888:20 → 1889:10 → 1890:16!) = 6+5+5; **16/16 OBOJESTRANSKO** + ~40 mega-zoomov ×3–10 + control-stripi ctl77/78/79; **faza-1 oris popravki ×12**: v1 »Nuc« → MUC (oče Nicolaus!) + v3 »Eva Pirmat zum frunčevič« → **ROSA Pirmat, Inwohnerina**, Gradac 71 + v5 »Maslaving/Guvlášofn« → Hrasinec? 21 / Michaël ŠURAJEVČIČ + v6 GRIBLJE **53** (NOVA hiša!) 51 let + v7 »Pirnosta/Tore« → Primostek 19 / Maria **TOME** + v9 rojen **Zavrh 41, PF. BOROVNICA** + v13 »Haaspić 9 / Johann Wolf« → **CERKVIŠČE 9 / Johann HVALJ** × **Maria HARASIMIČ 44** (Cerkvišče 14!) + v14 »Gufsslor« = Gütlstar? [~] (3. pojav!) + v15 »Nov 21« → Nov 24 + v16 »Nov 27/Kokoljič« → Nov 24 / Johann **HARASIMIČ** × Maria **HVALJ**; **VELIKE NOVELE 1890**: **DVOJNI POROČNI VIKEND 23–24.11. = 4 POROKE** (v13+v14 + v15+v16; zgłasnice Podzemelj 21/11 st:12+13 isti dan!) + **PREKRIŽANA POROKA HVALJ × HARASIMIČ** (v13 Hvalj 49 × Harasimič 44; v16 Harasimič 24 × Hvalj 24 — sorojenci obeh strani!) + **2 SORODSTVENI DISPENSACIJI** (1. leto z 2!): v11 bratranca **3. stopnje** (matere Marije Zugelj = sestri!) Ordinariat Laibach 11.8. **№ 1840** + v14 **4. kanonska stopnja** 10.11. **№ 2619** + **ZUGELJ bratski par** (v10+v11 Dobravice 11, isti starši Georg × Anna Vermanič — 2. bratski par po 1888 Brinec!) + **NEVESTA 45 LET** (v5 Ana Agnič = rekord linije!) + **simetrija 41=41** (v4!) + **lomek 19¾** (v7 — Kurrent »19z«!) + **NOVI STATUSI**: Inwohnerina-nevesta (v3 Rosa Pirmat!) + **VORMUND v očetovem stolpcu** (v3 Anton Pirmat!) + **Kürčnar/in? = Kürschner poklic** (v5!) + **WIRT-priča** (v10 Josef Zugelj — gostilna!) + Gütlarin [~] (v4+v13) + **¾ GÜTL ulomek** (v14 Anna Marentič!) + **4. DUHOVNIK LINIJE = MICHAEL BULOVEC pro t. deleg. Semič** (v4!) + **Ordinariat Laibach številke ×3** (Z:132 + № 1840 + № 2619) + sodna № 187/208 (v9) + Z:216 (v10) + **mladoletnost 6/16 = 37.5%** (v2 18 edino MÜTTERL. soglasje! + väterl. ×4 + sodna v9) + **zgłasnice 16/16 = 100%** (Podzemelj ×8 + Gradac ×4 + Griblje ×4; Griblje 1→16→36→39 + Gradac 11→13→16 časovno 1:1!) + **Metlika (Mößling) ×2** (v4 h22 + v12 h24!) + tuje župnije ×8 (Pf. Črnomelj ×3 + Borovnica + Semič ×2 + Metlika ×2); **mreže: PERDINEC/PEGDIREC ×8 (2 pisavi!) + MARENTIČ ×5 + ŠURAJEVČIČ ×5 + ZUGELJ ×6 + MUC ×5 + POŽEK ×5 + TOME ×5 + HRIŽAN ×5 + BRINEC ×4 + JAKŠA ×4 + STRAUS ×4 + MILEK ×3 + SIMEC ×4 + KLEPEC ×3 + DRAGOŠ ×3 + KURE ×3 + HARASIMIČ ×3 + BOLTE ×2 + WAGNER ×2 + AGNIČ ×2 + RUS ×2**; **GRIBLJE: 3 poroke / 4 hiše** — h53 = **NOVA HIŠA (1. dokaz sploh!)** + h91/h61 2. familiji (krstna 1887!) + h10 2. poročni dokaz; anomalije ×13 (A2 Hvalj/Harasimič mismatch — vdova roj. Hvalj! + A3 Gütlstar 3. pojav! + A11 h61 Muc-vs-Požek!); vitals **544 → 548** (+ 4 novih poročnih blokov h91/h10/h53/h61-1890); bloki 04455 = **31**; **P120 LEAD: poročna 1891** (glava = Pag. 79 = s80, v1–4 že orisani; pričakovane Muc-krstne 1891!); EXCLUDED: 4; skripta scripts/p119_parish_marriage_1890.py (I1–I11); status SAMPLE-TRANSCRIPTION-M1890",
  "P119: PARISH OF PODZEMELJ — MARRIAGE REGISTER 04455, THE FULL YEAR 1890 (issue #18; SAMPLE-TRANSCRIPTION-M1890; the 5th year of the marriage line): the frame CONFIRMED — scans 77–79 == pages 76–78 (page == scan − 1, the 5th confirmation; LANDSCAPE ~2484–2525×1800; the big header »Traunungs=Buch« on p. 76!) — **16 entries = THE BIGGEST YEAR OF THE LINE** (1886:7 → 1887:21 → 1888:20 → 1889:10 → 1890:16!) = 6+5+5; **16/16 BOTH-SIDES** + ~40 mega-zooms ×3–10 + control strips ctl77/78/79; **the faza-1 outline corrections ×12**: v1 »Nuc« → MUC (father Nicolaus!) + v3 »Eva Pirmat« → **ROSA Pirmat, an Inwohnerin**, Gradac 71 + v5 → Hrasinec? 21 / Michaël ŠURAJEVČIČ + v6 GRIBLJE **53** (A NEW house!) 51 years + v7 → Primostek 19 / Maria **TOME** + v9 born **Zavrh 41, PF. BOROVNICA** + v13 »Haaspić 9 / Johann Wolf« → **CERKVIŠČE 9 / Johann HVALJ** × **Maria HARASIMIČ 44** (Cerkvišče 14!) + v14 »Gufsslor« = Gütlstar? [~] (the 3rd occurrence!) + v15 »Nov 21« → Nov 24 + v16 → Nov 24 / Johann **HARASIMIČ** × Maria **HVALJ**; **THE BIG 1890 NOVELS**: **THE DOUBLE MARRIAGE WEEKEND NOV 23–24 = 4 WEDDINGS** (v13+v14 + v15+v16; the announcements Podzemelj Nov 21 nos. 12+13 the same day!) + **THE CROSSED HVALJ × HARASIMIČ WEDDING** (v13 Hvalj 49 × Harasimič 44; v16 Harasimič 24 × Hvalj 24 — siblings of both sides!) + **2 KINSHIP DISPENSATIONS** (the 1st year with 2!): v11 first cousins **3rd degree** (the mothers Marija Zugelj = sisters!) Ordinariat Laibach Aug 11 **№ 1840** + v14 the **4th canonical degree** Nov 10 **№ 2619** + **THE ZUGELJ BROTHER COUPLE** (v10+v11 Dobravice 11, the same parents Georg × Anna Vermanič — the 2nd brother couple after 1888 Brinec!) + **THE BRIDE OF 45 YEARS** (v5 Ana Agnič = the line's record!) + **the symmetry 41=41** (v4!) + **the fraction 19¾** (v7!) + **NEW STATUSES**: an Inwohnerin bride (v3 Rosa Pirmat!) + **a VORMUND in the bride's father column** (v3 Anton Pirmat!) + **the Kürschner profession** (v5!) + **a WIRT witness** (v10 Josef Zugelj — the Zugelj inn!) + **the ¾ GÜTL fraction** (v14 Anna Marentič!) + **the 4th PRIEST OF THE LINE = MICHAEL BULOVEC pro t. deleg. Semič** (v4!) + **3 Laibach Ordinariat numbers** (Z:132 + № 1840 + № 2619) + the court № 187/208 (v9) + Z:216 (v10) + **the minority 6/16 = 37.5%** (v2 18 the only MATERNAL consent!) + **the announcements 16/16 = 100%** + **Metlika ×2** (v4 h22 + v12 h24!) + foreign parishes ×8; **the networks: PERDINEC/PEGDIREC ×8 + MARENTIČ ×5 + ŠURAJEVČIČ ×5 + ZUGELJ ×6 + MUC ×5 + POŽEK ×5 + TOME ×5 + HRIŽAN ×5 + BRINEC ×4 + STRAUS ×4**; **GRIBLJE: 3 marriages / 4 houses** — h53 = **A NEW HOUSE (the 1st evidence ever!)** + h91/h61 the 2nd families + h10 the 2nd marriage evidence; anomalies ×13 (A2 the Hvalj/Harasimič mismatch — a widow born Hvalj! + A3 Gütlstar the 3rd occurrence! + A11 h61 Muc-vs-Požek!); vitals **544 → 548** (+ the 4 new marriage blocks h91/h10/h53/h61-1890); the 04455 blocks = **31**; **THE P120 LEAD: the marriages of 1891** (the header = p. 79 = s80, v1–4 already outlined; the expected Muc baptisms of 1891!); EXCLUDED: 4; the script scripts/p119_parish_marriage_1890.py (I1–I11); status SAMPLE-TRANSCRIPTION-M1890",
  p119Errors.length === 0,
  p119Errors.length === 0
    ? `16 vpisov = NAJVEČJE LETO LINIJE (s77–s79 == Pag. 76–78; velika glava!) · **dvojni poročni vikend 23–24.11. ×4 poroke!** · **prekrižana poroka Hvalj × Harasimič (v13↔v16!)** · **2 dispensaciji (bratranca 3. st. № 1840 + 4. st. № 2619!)** · Zugelj bratski par (isti starši!) · nevesta 45 (rekord!) · simetrija 41=41 · lomek 19¾ · Inwohnerina + Vormund + Kürschner + Wirt-priča + ¾ Gütl · **Bulovec 4. duhovnik (pro t. deleg. Semič!)** · Ordinariat ×3 (132/1840/2619) · mladoletnost 6/16 (edino mütterl. v2!) · zgłasnice 16/16 (Griblje 1→16→36→39 1:1!) · Metlika ×2 · Borovnica migracija · mreže Perdinec ×8/Marentič ×5/Zugelj ×6/Muc ×5 · **GRIBLJE 3 poroke / 4 hiše (h53 NOVA! h91/h61 2. familiji!)** · vitals 548 · bloki 04455 = 31 · **P120 LEAD: poročna 1891 (s80!)**`
    : p119Errors.join("; "),
);

// ——— qa-p120: župnija Podzemelj — poročna knjiga 04455, polno leto 1891 (P120; 6. leto poročne linije!) ———
const p120Marr = HOUSE_VITALS.filter((h) => h.bookSignature === "04455" && h.year === 1891);
const p120Errors: string[] = [];
if (p120Marr.length !== 2)
  p120Errors.push(`poročni bloki 1891 (04455) ≠ 2 (${p120Marr.length})`);
const p120Houses = p120Marr.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
if (p120Houses.join(",") !== "20,87")
  p120Errors.push(`hiše 1891 (04455) ≠ [20,87] — najdeno: ${p120Houses.join(",")} (P120: h87 v6 2. POROČNI DOKAZ + h20 v7 NOVA HIŠA!)`);
// P120 pini (1891 bloki)
const p120Pins: Array<[string, string]> = [
  ["87", "PEZDIREC"], ["87", "2. POROČNI DOKAZ h87"], ["87", "ŽELJKO"], ["87", "MILEK"], ["87", "KLEPEC"],
  ["20", "PEZDIREC"], ["20", "NOVA HIŠA"], ["20", "KLEPEC"], ["20", "Krasinec 37"], ["20", "TROJNO"],
];
for (const [n, pin] of p120Pins) {
  const blk = p120Marr.filter((h) => h.houseNo === n);
  if (blk.length === 0) {
    p120Errors.push(`pin ${n} (${pin}) — hiša ${n} ni med 1891 bloki`);
    continue;
  }
  if (!blk.some((cur) => cur.whatSi.toLowerCase().includes(pin.toLowerCase())))
    p120Errors.push(`pin hiša ${n} (${pin}) manjka`);
}
// duhovniki 1891 (bloki): Rauy ×2 (Griblje vpisa v6 + v7)
const p120Rauy = p120Marr.filter((h) => h.whatSi.includes("Rauy")).length;
if (p120Rauy !== 2)
  p120Errors.push(`Rauy podpisi 1891 blokov ≠ 2 (${p120Rauy})`);
// oznaki dokazov 1891: h20 = "NOVA HIŠA" (1. dokaz sploh!) + h87 = "2. POROČNI DOKAZ h87" (po 1889 v8!)
if (!p120Marr.some((h) => h.houseNo === "20" && h.whatSi.includes("NOVA HIŠA")))
  p120Errors.push("h20-1891: oznaka »NOVA HIŠA« manjka");
if (!p120Marr.some((h) => h.houseNo === "87" && h.whatSi.includes("2. POROČNI DOKAZ h87")))
  p120Errors.push("h87-1891: oznaka »2. POROČNI DOKAZ h87« manjka");
// kumulativ: vitals 548 → 550 (P120: + 2 novih poročnih blokov 1891)
if (HOUSE_VITALS.length !== 685)
  p120Errors.push(`HOUSE_VITALS ≠ 554 (${HOUSE_VITALS.length} — P119: 548; P120: 550; P121: + 4 novih poročnih blokov 1892 = 554!)`);
// kumulativ blokov 04455 = 33 (P119: 31; P120: + 2 bloki 1891)
if (p116Marr.length !== 168)
  p120Errors.push(`bloki 04455 skupaj ≠ 142 (${p116Marr.length} — P121: + 4 bloki 1892; …; P126: + 9 blokov 1897; P127: + 9 blokov 1898; P128: + 6 blokov 1899; P132: + 12 blokov 1903; P133: + 8 blokov 1904; P134: + 13 blokov 1905 = 115!)`);
push(
  "qa-p120-parish-marriage-1891",
  "P120: ŽUPNIJA PODZEMELJ — POROČNA KNJIGA 04455, POLNO LETO 1891 (issue #18; SAMPLE-TRANSCRIPTION-M1891; 6. leto poročne linije P115 = 1886 → P116 = 1887 → P117 = 1888 → P118 = 1889 → P119 = 1890 → P120 = 1891): okvir POTRJEN — skeni 80–83 == Pag. 79–82 (Pag. == sken − 1, 6. potrditev; velja v 71–83; LANDSCAPE ~2499–2515×1800; glava 1891 = Pag. 79 BREZ velike glave — »Traunungs=Buch« je na s84 = Pag. 83 za leto 1892!) — **18 vpisov = 2. NAJVEČJE LETO LINIJE** (1886:7 → 1887:21 → 1888:20 → 1889:10 → 1890:16 → 1891:18!) = 4+6+4+4; **18/18 OBOJESTRANSKO**; **VELIKE NOVELE 1891**: **ROSETTA statusa »[Hofname]s. Sohn/Tochter«** (v14 groom »½ Griblers. Sohn« EKSPLICITNO — razrešitev skrivnostne končnice 1886–1890!) + **deležni sistem imenja Griblje** (½/¼ ×14 oseb!) + **1. VD-OVI POROKI LINIJE ×2** (v14 Anna Šimonič roj. Konda 32 + v15 Anna Žepar 35!) + **1. ŽANDAR LINIJE** (v15 Mirko Pintar, rod. Dolenja Pušća № 3, HRVAŠKA!) + **1. HRVAŠKA povezava** (4 hrvaška dokumenta + 2 Zagrebčana-priče!) + **1. APOSTOLSKA dispensacija** (v11 bratranca 2. kanonske stopnje iste linije = prvi bratranci! + k.k. Landesreg. Laibach Z:5672) + **PEZDIREC ×12 oseb = rekord mreže linije** (prej 1888 ×9!) + **dnevne gruče** 26.1.×3 + 3.2.×3 (TROJNI poročni dan v5+v6+v7!) + 21.+23.11.×4 (vikend!) + **2 VDOVI** (v14 + v15) + **mladoletnost 12/18 neveste + 3/18 ženinov** (ABGB večina 24 = 3. leto potrjeno, dokumenti 100% konsistentni!) + Hofname **Laipšl/Laipfl ×5** [~] + **obrtniški poklici** (Zimmermann 3. pojav rod. Bistra pri Vrhniki — najdaljši migracijski lok ~60 km! + Hafner? + Lončar? + Kürschner-u.-Wirth oče + Löhner? ×4) + **k.k. Landesreg. Laibach ×3** (№ 5549 + Z:5672 + Z:11825) + **banns iz 2 župnij** (v9 Metlika + Trnovo — bodoče bivališče!) + zgłasnice 18/18 + **občine NOVE ×5** (Šuhor, Božjakovo-Rozalnice, Knežak?, Verblika?, Vrbiče? — najširša geografija linije!); **GRIBLJE: 2 poroki / 2 hiši** — h87 **2. DOKAZ** (1889 v8 Milek×Klejpec → 1891 v6 Pezdirec×Željko — Klepec-mreža!) + **h20 NOVA HIŠA (1. poročni dokaz sploh!)**; anomalije ×14 (A1 ROSETTA-STATUS + A7 BREZ-ZGLASNICE v15 — samo hrvaški dokumenti! + A13 H87-KLEPEC-mreža); vitals **548 → 550** (+ 2 novih poročnih blokov h87/h20-1891); bloki 04455 = **33**; p80 hiše **46**; **P121 LEAD: poročna 1892** (VELIKA GLAVA »Traunungs=Buch« POTRJENA na s84 = Pag. 83 + v1–4 že orisani — v1 = Griblje 10 Muc-hiša 3. dokaz?!); EXCLUDED: 0; skripta scripts/p120_parish_marriage_1891.py (I1–I11); status SAMPLE-TRANSCRIPTION-M1891",
  "P120: PARISH OF PODZEMELJ — MARRIAGE REGISTER 04455, THE FULL YEAR 1891 (issue #18; SAMPLE-TRANSCRIPTION-M1891; the 6th year of the marriage line P115 = 1886 → … → P120 = 1891): the frame CONFIRMED — scans 80–83 == pages 79–82 (page == scan − 1, the 6th confirmation; holds in 71–83; LANDSCAPE ~2499–2515×1800; the 1891 header = p. 79 WITHOUT the large heading — »Traunungs=Buch« is on s84 = p. 83 for the year 1892!) — **18 entries = THE 2nd BIGGEST YEAR OF THE LINE** (1886:7 → 1887:21 → 1888:20 → 1889:10 → 1890:16 → 1891:18!) = 4+6+4+4; **18/18 BOTH-SIDES**; **THE BIG 1891 NOVELS**: **THE ROSETTA of the »[Hofname]s. Sohn/Tochter« status** (v14 the groom's »½ Griblers. Sohn« EXPLICIT — resolving the mysterious ending of 1886–1890!) + **the fractional-tenure system of Griblje** (½/¼ ×14 persons!) + **the 1st WIDOW-WEDDINGS OF THE LINE ×2** (v14 Anna Šimonič born Konda 32 + v15 Anna Žepar 35!) + **the 1st GENDARME of the line** (v15 Mirko Pintar, born Dolenja Pušća № 3, CROATIA!) + **the 1st CROATIAN link** (4 Croatian documents + 2 Zagreb witnesses!) + **the 1st APOSTOLIC dispensation** (v11 first cousins of the 2nd canonical degree of the same line = the first cousins! + the k.k. Landesreg. Laibach Z:5672) + **PEZDIREC ×12 persons = the record network of the line** (previously 1888 ×9!) + **the daily clusters** Jan 26 ×3 + Feb 3 ×3 (the TRIPLE wedding day v5+v6+v7!) + Nov 21+23 ×4 (the weekend!) + **2 WIDOWS** (v14 + v15) + **the minority 12/18 brides + 3/18 grooms** (the ABGB majority of 24 = the 3rd year confirmed, the documents 100% consistent!) + the Hofname **Laipšl/Laipfl ×5** [~] + **the artisan professions** (Zimmermann the 3rd occurrence born Bistra pri Vrhniki — the longest migration arc ~60 km! + Hafner? + Lončar? + the Kürschner-and-Wirth father + Löhner? ×4) + **the k.k. Landesreg. Laibach ×3** (№ 5549 + Z:5672 + Z:11825) + **the banns from 2 parishes** (v9 Metlika + Trnovo — the future residence!) + the announcements 18/18 + **the NEW communes ×5** (Šuhor, Božjakovo-Rozalnice, Knežak?, Verblika?, Vrbiče? — the widest geography of the line!); **GRIBLJE: 2 marriages / 2 houses** — h87 the **2nd EVIDENCE** (1889 v8 Milek×Klejpec → 1891 v6 Pezdirec×Željko — the Klepec network!) + **h20 A NEW HOUSE (the 1st marriage evidence ever!)**; anomalies ×14 (A1 the ROSETTA-status + A7 WITHOUT-the-announcement v15 — only Croatian documents! + A13 the H87-KLEPEC network); vitals **548 → 550** (+ the 2 new marriage blocks h87/h20-1891); the 04455 blocks = **33**; the p80 houses **46**; **THE P121 LEAD: the marriages of 1892** (THE BIG HEADING »Traunungs=Buch« CONFIRMED on s84 = p. 83 + v1–4 already outlined — v1 = Griblje 10 the Muc house the 3rd evidence?!); EXCLUDED: 0; the script scripts/p120_parish_marriage_1891.py (I1–I11); status SAMPLE-TRANSCRIPTION-M1891",
  p120Errors.length === 0,
  p120Errors.length === 0
    ? `18 vpisov = 2. NAJVEČJE LETO (s80–s83 == Pag. 79–82; glava BREZ velike glave — »Traunungs=Buch« na s84!) · **ROSETTA statusa »[Hofname]s. Sohn/Tochter« (v14 — razrešitev 1886–1890!)** · deležni sistem ½/¼ ×14 · **1. VD-OVI poroki ×2 (Šimonič roj. Konda 32 + Žepar 35!)** · **1. ŽANDAR + 1. HRVAŠKA (Pintar Dolenja Pušća + 4 hrvaška dokumenta + 2 Zagrebčana-priče!)** · **1. APOSTOLSKA dispensacija (v11 bratranca 2. kanc. st. + Landesreg. Z:5672!)** · **PEZDIREC ×12 = rekord mreže linije!** · trojni poročni dan 3.2. (v5+v6+v7!) + vikend 21.+23.11. ×4 · mladoletnost 12/18 · Laipšl ×5 · Zimmermann Bistra pri Vrhniki (najdaljši lok ~60 km!) · Landesreg. ×3 (5549/Z:5672/Z:11825) · **GRIBLJE 2 poroki (h87 2. dokaz — Klepec-mreža! + h20 NOVA HIŠA!)** · vitals 550 · bloki 04455 = 33 · p80 hiše 46 · **P121 LEAD: poročna 1892 (VELIKA GLAVA s84 POTRJENA — v1 = Griblje 10 Muc-hiša!)**`
    : p120Errors.join("; "),
);

// ——— qa-p121: župnija Podzemelj — poročna knjiga 04455, polno leto 1892 (P121; 7. leto poročne linije!) ———
const p121Marr = HOUSE_VITALS.filter((h) => h.bookSignature === "04455" && h.year === 1892);
const p121Errors: string[] = [];
if (p121Marr.length !== 4)
  p121Errors.push(`poročni bloki 1892 (04455) ≠ 4 (${p121Marr.length})`);
const p121Houses = p121Marr.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
if (p121Houses.join(",") !== "17,30,36,60")
  p121Errors.push(`hiše 1892 (04455) ≠ [17,30,36,60] — najdeno: ${p121Houses.join(",")} (P121: h60 v1 2. POROČNI DOKAZ + h30 v5 nevesta + h17 v10 NOVA HIŠA + h36 v15!)`);
// P121 pini (1892 bloki)
const p121Pins: Array<[string, string]> = [
  ["60", "ŽELJKO"], ["60", "DRUBEL-GRIBLJE"], ["60", "BRODARIČ"], ["60", "h49"], ["60", "NAJMLAJŠA"],
  ["30", "SEGINA"], ["30", "POZDIREC"], ["30", "MILEK"], ["30", "Z: 798"],
  ["17", "KRALJ"], ["17", "DRUBEL-GRIBLJE"], ["17", "FILAK"], ["17", "h34"], ["17", "NOVA HIŠA"],
  ["36", "KRIŽAN"], ["36", "DRUBEL-GRIBLJE"], ["36", "STRUNCELJ"], ["36", "h44"], ["36", "SEGINA"],
];
for (const [n, pin] of p121Pins) {
  const blk = p121Marr.filter((h) => h.houseNo === n);
  if (blk.length === 0) {
    p121Errors.push(`pin ${n} (${pin}) — hiša ${n} ni med 1892 bloki`);
    continue;
  }
  if (!blk.some((cur) => cur.whatSi.toLowerCase().includes(pin.toLowerCase())))
    p121Errors.push(`pin hiša ${n} (${pin}) manjka`);
}
// duhovniki 1892 (bloki): Rauy ×4
const p121Rauy = p121Marr.filter((h) => h.whatSi.includes("Rauy")).length;
if (p121Rauy !== 4)
  p121Errors.push(`Rauy podpisi 1892 blokov ≠ 4 (${p121Rauy})`);
// oznaki dokazov 1892: h17 = "NOVA HIŠA" (1. dokaz sploh!) + h60 = "2. POROČNI DOKAZ h60" (po 1886!)
if (!p121Marr.some((h) => h.houseNo === "17" && h.whatSi.includes("NOVA HIŠA")))
  p121Errors.push("h17-1892: oznaka »NOVA HIŠA« manjka");
if (!p121Marr.some((h) => h.houseNo === "60" && h.whatSi.includes("2. POROČNI DOKAZ h60")))
  p121Errors.push("h60-1892: oznaka »2. POROČNI DOKAZ h60« manjka");
// kumulativ: vitals 550 → 554 (P121: + 4 novih poročnih blokov 1892)
if (HOUSE_VITALS.length !== 685)
  p121Errors.push(`HOUSE_VITALS ≠ 554 (${HOUSE_VITALS.length} — P120: 550; P121: + 4 novih poročnih blokov (h60/h30/h17/h36-1892) = 554!)`);
// kumulativ blokov 04455 = 37 (P120: 33; P121: + 4 bloki 1892)
if (p116Marr.length !== 168)
  p121Errors.push(`bloki 04455 skupaj ≠ 142 (${p116Marr.length} — P121: + 4 bloki 1892; …; P126: + 9 blokov 1897; P127: + 9 blokov 1898; P128: + 6 blokov 1899; P132: + 12 blokov 1903; P133: + 8 blokov 1904; P134: + 13 blokov 1905 = 115!)`);
push(
  "qa-p121-parish-marriage-1892",
  "P121: ŽUPNIJA PODZEMELJ — POROČNA KNJIGA 04455, POLNO LETO 1892 (issue #18; SAMPLE-TRANSCRIPTION-M1892; 7. leto poročne linije P115 = 1886 → … → P121 = 1892): okvir POTRJEN — skeni 84–86 == Pag. 83–85 (Pag. == sken − 1, 7. potrditev; velja v 61–86; LANDSCAPE ~2509–2518×1800) — **15 vpisov** (1886:7 → 1887:21 → 1888:20 → 1889:10 → 1890:16 → 1891:18 → 1892:15!) = 6+4+5; **VELIKA GLAVA »Traunungs=Buch« 1892 POTRJENA na s84** (P120 lead!); **15/15 OBOJESTRANSKO**; **VELIKE NOVELE 1892**: **DRUBEL-GRIBLJE poroke ×3 = REKORD LINIJE** (v1 h60×h49 + v10 h17×h34 + v15 h36×h44 — 6 od 7 hiš-noter!) + **deležni sistem ¼/½/¾ ×21 oseb = rekord** (1891: ×14; **¾ PRVIČ** — v2 nevesta + v2 oče + v4 priča!) + **Griblers=Sohn/Tochter ROSETTA ×9** + **1. AMERIŠKI KONSULAT** (v11 Philadelphia 2878/92 Z:3074 — oče Anton Cajnar verjetno izseljenec!) + **1. KNECHT ×2** (v6 + v12) + **1. MUC-priimek z deležem imenja** (v12 oče Nicolaus Muc ½ Gribler + priča Johan Muc — Muc = hišno ime Griblje 10!) + **SESTRSKI DVOZAKON ISTI DAN** (v2+v3 Marasinič, ista starša Johann × Anna Marenšič, 15.2. — 3. v liniji po 1886 Pegdirec + Musié!) + **4 poroke 22.2. = rekord dneva 1887–1892** + trojni dan 15.2. ×3 + vikend 21.+23.11. ×2 + **ženin 56 (v14) = NOV rekord starosti linije** + **nevesta 17 (v1) = NOV rekord mladosti** (prej 19!) + **Wittwen-dispensacija** (v13 + BezHauptm. Črnomelj 7.9.1892 Z:9123) + **vdovski znaki ×3** (v12 Filak≠Vardijan + v13 Wittwen + v14 Marasinič≠Černič — vsi z neskladjem »1.«!) + **Laipšl/Laipfl ×5 (2. leto mreže!)** + **k.k. BezHauptm. Črnomelj ×3** (v5 Z:798 + v7 Certificate 14/12.1891 + v13 Z:9123) + **k.k. Bez. Ger. MÖTTLING (Metlika!) ×2** (v8 + v12) + **slovenskojezični Befunde-blok** (v9 — 4 dokumenti: Novo mesto + Prečna + mestni urad) + PEZDIREC/POZDIREC ×5 signalov (v5 oče=priča ISTI mož!) + KRIŽAN ×5 + MARASINIČ ×6 + KLEPEC ×4 + SEGINA ×2 + FILAK ×3 (1. dokazi!) + MUC ×3 + JAKOBIČ ×3 + mladoletne neveste 7/15 (dokumenti 100% konsistentni, 4. leto!); **GRIBLJE: 3 poroke / 4 poročna bloka (7 hiš!)** — h60 **2. DOKAZ** (1886 → 1892; ŽELJKO-hiša!) + h30 (Pozdirec×Milek — oče=priča!) + **h17 NOVA HIŠA** (Kralj 48!) + h36 (Križan×Struncelj — Segina-mreža!); anomalije ×8 (A1 v12 Filak≠starša + A2 Wittwen-dispensa + A3 v13 Bahorič≠Stravs + A4 v14 Marasinič≠Černič + A5 MUC-GRIBLER + A6 sestrski dvozakon + A7 status W?rmiđ ×3 + A8 najmlajša 17); vitals **550 → 554** (+ 4 novih poročnih blokov h60/h30/h17/h36-1892); bloki 04455 = **37**; p80 hiše **41** (P121: + h17!); **P122 LEAD: poročna 1893** (glava rokopisno »1893« na s87 = Pag. 86 + v1–6 že orisani + s88 = Pag. 87 v7–11); EXCLUDED: 0; skripta scripts/p121_parish_marriage_1892.py (I1–I11); status SAMPLE-TRANSCRIPTION-M1892",
  "P121: PARISH OF PODZEMELJ — MARRIAGE REGISTER 04455, THE FULL YEAR 1892 (issue #18; SAMPLE-TRANSCRIPTION-M1892; the 7th year of the marriage line P115 = 1886 → … → P121 = 1892): the frame CONFIRMED — scans 84–86 == pages 83–85 (page == scan − 1, the 7th confirmation; holds in 61–86; LANDSCAPE ~2509–2518×1800) — **15 entries** (1886:7 → … → 1891:18 → 1892:15!) = 6+4+5; **THE BIG HEADING »Traunungs=Buch« 1892 CONFIRMED on s84** (the P120 lead!); **15/15 BOTH-SIDES**; **THE BIG 1892 NOVELS**: **the DOUBLE-GRIBLJE marriages ×3 = THE LINE RECORD** (v1 h60×h49 + v10 h17×h34 + v15 h36×h44 — 6 of the 7 houses inside!) + **the fractional system ¼/½/¾ ×21 persons = the record** (1891: ×14; **¾ FOR THE FIRST TIME**) + **the Griblers=Sohn/Tochter ROSETTA ×9** + **the 1st AMERICAN CONSULATE** (v11 Philadelphia 2878/92 Z:3074!) + **the 1st FARM-SERVANT ×2** (v6 + v12) + **the 1st MUC-surname with an estate share** (v12 the father Nicolaus Muc ½ Gribler — Muc = the house-name of Griblje 10!) + **the SISTERLY DOUBLE-WEDDING the same day** (v2+v3 Marasinič, the same parents, Feb 15!) + **4 marriages Feb 22 = the day record 1887–1892** + **the groom 56 (v14) = the NEW age record** + **the bride 17 (v1) = the NEW youth record** + **the widow-state dispensation** (v13 Z:9123) + **the widow signs ×3** + **Laipšl ×5 (the 2nd year of the network!)** + **the k.k. BezHauptm. Črnomelj ×3** + **the k.k. Bez. Ger. MÖTTLING (Metlika!) ×2** + **the Slovene-language Befunde block** (v9); **GRIBLJE: 3 marriages / 4 marriage blocks (7 houses!)** — h60 the **2nd EVIDENCE** + h30 + **h17 A NEW HOUSE** + h36; anomalies ×8; vitals **550 → 554**; the 04455 blocks = **37**; the p80 houses **41** (P121: + h17!); **THE P122 LEAD: the marriages of 1893** (the handwritten heading »1893« on s87 = p. 86 + v1–6 already outlined + s88 = p. 87 v7–11); EXCLUDED: 0; the script scripts/p121_parish_marriage_1892.py (I1–I11); status SAMPLE-TRANSCRIPTION-M1892",
  p121Errors.length === 0,
  p121Errors.length === 0
    ? `15 vpisov (s84–s86 == Pag. 83–85; VELIKA GLAVA 1892 POTRJENA s84!) · **DRUBEL-GRIBLJE poroke ×3 = REKORD LINIJE (h60×h49 + h17×h34 + h36×h44)!** · deleži ¼/½/¾ ×21 (¾ PRVIČ!) · **1. AMERIŠKI KONSULAT (Philadelphia Z:3074)** · 1. KNECHT ×2 · **MUC-priimek z deležem (oče ½ Gribler!)** · sestrski dvozakon isti dan (v2+v3!) · 4 poroke 22.2. = rekord dneva · ženin 56 + nevesta 17 = NOVA rekorda · Wittwen-dispensa Z:9123 · vdovski znaki ×3 · Laipšl ×5 · Möttling ×2 · **GRIBLJE 3 poroke / 4 bloka / 7 hiš (h60 2. dokaz + h17 NOVA!)** · vitals 554 · bloki 04455 = 37 · p80 hiše 41 · **P122 LEAD: poročna 1893 (s87 rokopis »1893« POTRJEN!)**`
    : p121Errors.join("; "),
);

// ——— qa-p122: župnija Podzemelj — poročna knjiga 04455, polno leto 1893 (P122; 8. leto poročne linije!) ———
{
  const p122Marr = HOUSE_VITALS.filter((h) => h.bookSignature === "04455" && h.year === 1893);
  const p122Errors: string[] = [];
  if (p122Marr.length !== 5)
    p122Errors.push(`poročni bloki 1893 (04455) ≠ 5 (${p122Marr.length})`);
  const p122Houses = p122Marr.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
  if (p122Houses.join(",") !== "26,58,62,69,74")
    p122Errors.push(`hiše 1893 (04455) ≠ [26,58,62,69,74] — najdeno: ${p122Houses.join(",")} (P122: h26 v10 NOVA + h69 v15 2. dokaz + h62 v15 NOVA + h58 v16 1. DOKAZ SPLOH + h74 v16 NOVA!)`);
  // P122 pini (1893 bloki)
  const p122Pins: Array<[string, string]> = [
    ["26", "KRALJ"], ["26", "KLEMENČIČ"], ["26", "GJUPNIJSKEGA"], ["26", "Fučkovec"],
    ["69", "DRUBEL-GRIBLJE"], ["69", "h62"], ["69", "KURE"], ["69", "2. poročni dokaz h69"],
    ["62", "KURE"], ["62", "KRIŽAN"], ["62", "drubel"],
    ["58", "POŽEK"], ["58", "DRUBEL-GRIBLJE"], ["58", "h74"], ["58", "1661"],
    ["74", "KAMBIČ"], ["74", "BRINEC"], ["74", "1661"],
  ];
  for (const [n, pin] of p122Pins) {
    const blk = p122Marr.filter((h) => h.houseNo === n);
    if (blk.length === 0) {
      p122Errors.push(`pin ${n} (${pin}) — hiša ${n} ni med 1893 bloki`);
      continue;
    }
    if (!blk.some((cur) => cur.whatSi.toLowerCase().includes(pin.toLowerCase())))
      p122Errors.push(`pin hiša ${n} (${pin}) manjka`);
  }
  // duhovniki 1893 (bloki): Rauy ×4 + KLEMENČIČ ×1 (h26 — 2. duhovnik linije!); podpis-oblika »Jos. Rauy« (h26 fraza »Rauy-monopola« ne šteje kot podpis)
  const p122Rauy = p122Marr.filter((h) => h.whatSi.includes("Jos. Rauy")).length;
  if (p122Rauy !== 4)
    p122Errors.push(`Rauy podpisi 1893 blokov ≠ 4 (${p122Rauy})`);
  if (!p122Marr.some((h) => h.houseNo === "26" && h.whatSi.includes("KLEMENČIČ")))
    p122Errors.push("h26-1893: 2. duhovnik KLEMENČIČ manjka");
  // oznake dokazov 1893: h58 = 1. POROČNI DOKAZ + h26/h62/h74 = NOVA hiša
  if (!p122Marr.some((h) => h.houseNo === "58" && h.whatSi.includes("1. POROČNI DOKAZ h58")))
    p122Errors.push("h58-1893: oznaka »1. POROČNI DOKAZ h58« manjka");
  if (!p122Marr.some((h) => h.houseNo === "26" && h.whatSi.includes("NOVA HIŠA")))
    p122Errors.push("h26-1893: oznaka »NOVA HIŠA« manjka");
  // kumulativ: vitals 554 → 566 (P122: + 5 novih poročnih blokov 1893; P123: + 4 bloki 1894; P124: + 3 bloki 1895)
  if (HOUSE_VITALS.length !== 685)
    p122Errors.push(`HOUSE_VITALS ≠ 569 (${HOUSE_VITALS.length} — P121: 554; P122: + 5 novih poročnih blokov (h26/h69/h62/h58/h74-1893); P123: + 4 bloki 1894; P124: + 3 bloki 1895; P125: + 3 bloki (h24+h14-1895ext + h18-1896) = 569!)`);
  // kumulativ blokov 04455 = 46 (P121: 37; P122: + 5 bloki 1893; P123: + 4 bloki 1894)
  if (p116Marr.length !== 168)
    p122Errors.push(`bloki 04455 skupaj ≠ 142 (${p116Marr.length} — P122: + 5 bloki 1893; P123: + 4 bloki 1894; …; P126: + 9 blokov 1897; …; P132: + 12 blokov 1903; P133: + 8 blokov 1904; P134: + 13 blokov 1905 = 115!)`);
  push(
    "qa-p122-parish-marriage-1893",
    "P122: ŽUPNIJA PODZEMELJ — POROČNA KNJIGA 04455, POLNO LETO 1893 (issue #18; SAMPLE-TRANSCRIPTION-M1893; 8. leto poročne linije P115 = 1886 → … → P122 = 1893): okvir POTRJEN — skeni 87–90 == Pag. 86–89 (Pag. == sken − 1, 8. potrditev; LANDSCAPE ~2512–2524×1800) — **20 vpisov** (1886:7 → … → 1892:15 → 1893:20 = 2. največje leto!) = 6+5+5+4; **VELIKA GLAVA »Traunungs=Buch« + rokopisno »1893« POTRJENA na s87** (P122 lead!); **20/20 OBOJESTRANSKO**; **VELIKE NOVELE 1893**: **7 POROK NA ISTI DAN 6.2. = REKORD VSEH ČASOV LINIJE** (prej 4 — P121!) + **DRUBEL-GRIBLJE poroke ×2** (v15 h69×h62 + v16 h58×h74) + v10 nevesta **GRIBLJE 26 NOVA HIŠA** = 3 poroke / 5 hiš + **BRAT-SESTRA PERDINEC DVOZAKON ISTI DAN** (v4+v6 — isti starša!) + **★ RENOVACIJA ZAKONA 8.9.1898** (v8 latinski blok — Jeglič [~] + priči Maur + Skala = NOV DOKUMENT-TIP) + **★ 2. DUHOVNIK LINIJE Michael KLEMENČIČ Coop. ×2** (konec Rauy-monopola!) + **★ 1. DOKUMENT OBČINE GRIBLJE** (v15) + občina Tribuče NOVA (v20) + **★ INHABER = NOV STATUS** (v19 Murn) + **★ VOJSKA** Rudolfovo + proxy-zastopstvo (v12) + **★ DISPENS 3. kan. stopnje №1661** (v16 — oba materi BRINC!) + deleži ¼/½ ×32 oseb + »1« ulomek-anomala (v5) + ženin 58 + nevesta 17 tied-rekord + Laipšl ×8 (3. leto!) + KAMBIČ ×5 + BRINC ×5 + PEZDIREC-cluster ×6 (3 pisave!); **GRIBLJE: 3 poroke / 5 poročnih blokov (h26 NOVA + h69 2. dokaz + h62 NOVA + h58 1. DOKAZ SPLOH! + h74 NOVA)**; anomalije ×8; vitals **554 → 559** (+ 5 blokov 1893); bloki 04455 = **42**; p80 hiše **41** (vseh 5 že v vzorci!); **P123 LEAD: poročna 1894** (glava 1894 = s91 = Pag. 90 + v1–6 orisani; s94 = glava 1895); EXCLUDED: 0; skripta scripts/p122_parish_marriage_1893.py (I1–I11); status SAMPLE-TRANSCRIPTION-M1893",
    "P122: PARISH OF PODZEMELJ — MARRIAGE REGISTER 04455, THE FULL YEAR 1893 (issue #18; SAMPLE-TRANSCRIPTION-M1893; the 8th year of the marriage line): the frame CONFIRMED — scans 87–90 == pages 86–89 (page == scan − 1, the 8th confirmation) — **20 entries** (…→ 1893:20 = the 2nd largest year!) = 6+5+5+4; **THE BIG HEADING + handwritten »1893« CONFIRMED on s87**; **20/20 BOTH-SIDES**; **THE BIG 1893 NOVELS**: **7 MARRIAGES THE SAME DAY Feb 6 = THE ALL-TIME LINE RECORD** + **the DOUBLE-GRIBLJE marriages ×2** (v15 h69×h62 + v16 h58×h74) + the v10 bride **GRIBLJE 26 A NEW HOUSE** = 3 marriages / 5 houses + **the BROTHER-SISTER PERDINEC double-wedding the same day** (v4+v6!) + **★ the MARRIAGE RENOVATION Sep 8, 1898** (v8 the Latin block — Jeglič [~] = A NEW DOCUMENT TYPE) + **★ the 2nd PRIEST OF THE LINE Michael KLEMENČIČ Coop. ×2** (the end of the Rauy monopoly!) + **★ the 1st GRIBLJE COMMUNE document** (v15) + the Tribuče commune NEW (v20) + **★ INHABER = A NEW STATUS** (v19) + **★ the ARMY** Rudolfovo + the proxy-representation (v12) + **★ the 3rd canonical degree dispensation №1661** (v16 — both mothers BRINC!) + the fractions ¼/½ ×32 persons + the »1« fraction anomaly (v5) + the groom 58 + the bride 17 tied-record + Laipšl ×8 (the 3rd year!) + KAMBIČ ×5 + BRINC ×5 + the PEZDIREC cluster ×6 (3 spellings!); **GRIBLJE: 3 marriages / 5 marriage blocks**; anomalies ×8; vitals **554 → 559**; the 04455 blocks = **42**; the p80 houses **41**; **THE P123 LEAD: the marriages of 1894** (the 1894 heading = s91 = p. 90 + v1–6 outlined; s94 = the 1895 heading); EXCLUDED: 0; the script scripts/p122_parish_marriage_1893.py (I1–I11); status SAMPLE-TRANSCRIPTION-M1893",
    p122Errors.length === 0,
    p122Errors.length === 0
      ? `20 vpisov (s87–s90 == Pag. 86–89; VELIKA GLAVA + »1893« POTRJENA s87!) · **7 POROK 6.2. = REKORD VSEH ČASOV!** · DRUBEL-GRIBLJE ×2 (h69×h62 + h58×h74) + h26 NOVA = 3 poroke / 5 hiš · BRAT-SESTRA PERDINEC dvozakon isti dan (v4+v6!) · ★ RENOVACIJA ZAKONA 8.9.1898 (v8 — Jeglič [~]!) · ★ 2. DUHOVNIK KLEMENČIČ ×2 (konec Rauy-monopola!) · ★ 1. dokument občine GRIBLJE (v15) + občina Tribuče NOVA · ★ INHABER (v19) · ★ VOJSKA Rudolfovo + proxy (v12) · ★ DISPENS 3.st. №1661 (v16 — oba materi BRINC!) · »1« ulomek (v5) + ženin 58 + nevesta 17 tied · Laipšl ×8 · KAMBIČ ×5 · **GRIBLJE 3 poroke / 5 blokov** · vitals 559 · bloki 04455 = 42 · p80 hiše 41 · **P123 LEAD: poročna 1894 (s91 glava POTRJENA!)**`
      : p122Errors.join("; "),
  );
}

// ——— qa-p123: župnija Podzemelj — poročna knjiga 04455, polno leto 1894 (P123; 9. leto poročne linije!) ———
{
  const p123Marr = HOUSE_VITALS.filter((h) => h.bookSignature === "04455" && h.year === 1894);
  const p123Errors: string[] = [];
  if (p123Marr.length !== 4)
    p123Errors.push(`poročni bloki 1894 (04455) ≠ 4 (${p123Marr.length})`);
  const p123Houses = p123Marr.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
  if (p123Houses.join(",") !== "9,11,27,42")
    p123Errors.push(`hiše 1894 (04455) ≠ [9,11,27,42] — najdeno: ${p123Houses.join(",")} (P123: h27 v3 2. dokaz × h42 v3 CERNIČ-hiša 1. POROČNI! + h9 v11 2. dokaz × h11 v11 2. dokaz — 2. GRIBLJE poroka 1894!)`);
  // P123 pini (1894 bloki)
  const p123Pins: Array<[string, string]> = [
    ["27", "ENAČNOPRIIMEŠKA POROKA Perdinec"], ["27", "KLEPSEC"], ["27", "Segina"],
    ["42", "CERNIČ-hiša"], ["42", "1. POROČNI"], ["42", "MARASINIČ"],
    ["9", "LANDSREGIERUNG-dokument poročne linije"], ["9", "8667"], ["9", "5642"], ["9", "POŽEK"],
    ["11", "2. GRIBLJE poroka 1894"], ["11", "ZURNIČ"], ["11", "DRAGOŠ"],
  ];
  for (const [n, pin] of p123Pins) {
    const blk = p123Marr.filter((h) => h.houseNo === n);
    if (blk.length === 0) {
      p123Errors.push(`pin ${n} (${pin}) — hiša ${n} ni med 1894 bloki`);
      continue;
    }
    if (!blk.some((cur) => cur.whatSi.toLowerCase().includes(pin.toLowerCase())))
      p123Errors.push(`pin hiša ${n} (${pin}) manjka`);
  }
  // duhovniki 1894 (bloki): Rauy ×4 (podpis-oblika »Jos. Rauy«)
  const p123Rauy = p123Marr.filter((h) => h.whatSi.includes("Jos. Rauy")).length;
  if (p123Rauy !== 4)
    p123Errors.push(`Rauy podpisi 1894 blokov ≠ 4 (${p123Rauy})`);
  // oznaki dokazov 1894: h42 = 1. POROČNI + h9/h11/h27 = 2. poročni dokaz
  if (!p123Marr.some((h) => h.houseNo === "42" && h.whatSi.includes("1. POROČNI")))
    p123Errors.push("h42-1894: oznaka »1. POROČNI« manjka");
  if (!p123Marr.some((h) => h.houseNo === "9" && h.whatSi.includes("2. poročni dokaz h9")))
    p123Errors.push("h9-1894: oznaka »2. poročni dokaz h9« manjka");
  // kumulativ: vitals 559 → 566 (P123: + 4 novih poročnih blokov 1894; P124: + 3 bloki 1895)
  if (HOUSE_VITALS.length !== 685)
    p123Errors.push(`HOUSE_VITALS ≠ 569 (${HOUSE_VITALS.length} — P122: 559; P123: + 4 novih poročnih blokov (h27/h42/h9/h11-1894); P124: + 3 bloki 1895 (h16/h27/h52); P125: + 3 bloki (h24+h14-1895ext + h18-1896) = 569!)`);
  // kumulativ blokov 04455 = 49 (P122: 42; P123: + 4 bloki 1894; P124: + 3 bloki 1895)
  if (p116Marr.length !== 168)
    p123Errors.push(`bloki 04455 skupaj ≠ 142 (${p116Marr.length} — P123: + 4 bloki 1894; P124: + 3 bloki 1895; P125: + 3 bloki (h24+h14-1895ext + h18-1896); P126: + 9 blokov 1897; P127: + 9 blokov 1898; P128: + 6 blokov 1899; P132: + 12 blokov 1903; P133: + 8 blokov 1904; P134: + 13 blokov 1905 = 115!)`);
  push(
    "qa-p123-parish-marriage-1894",
    "P123: ŽUPNIJA PODZEMELJ — POROČNA KNJIGA 04455, POLNO LETO 1894 (issue #18; SAMPLE-TRANSCRIPTION-M1894; 9. leto poročne linije P115 = 1886 → … → P123 = 1894): okvir POTRJEN — skeni 91–93 == Pag. 90–92 (Pag. == sken − 1, 9. potrditev; LANDSCAPE 2524/2517/2509×1800; tiskar »Laibach. Druck u. Verlag v. Möttling.« na s92!) — **15 vpisov** (1886:7 → … → 1893:20 → 1894:15) = 6+5+4; **VELIKA GLAVA »Traunungs=Buch« + rokopisno »1894« POTRJENA na s91** (P123 lead!; 5. velika glava linije); **15/15 OBOJESTRANSKO**; **VELIKE NOVELE 1894**: **★ REKORD-PAR VSEH ČASOV v5** (ženin 64 + nevesta 48 = 112 let skupaj!) + **REKORD nevesta 56** (v1 Tasič — prej 45 P119!) + **★ 1. PREČRTANI PRIČA linije** (v12 Đur. Andreas Vojka → Franc Justin zasebnik junior!) + **★ PFARRAMT IDRIA** (v12 = najdaljši župnijski lok ~110 km!) + **★ VOJSKA** (v9 k.k. Infanterie-Regiments-Colonel 15/5.94 №267 — ženin aktivni vojak!) + **★ DISPENS 3. stopnje №2680** (v14 Ordinariat Laibach 25/9. — ZUGELJ × TOME) + **★ LANDSREGIERUNG Laibach Ž8667** (v11 — 1. v poročni liniji; datirana 9/9. = 3 TEDNE PO poroki [~]!) + **ENAČNOPRIIMEŠKI poroki ×2** (v3 Perdinec × Perdinec h27×h42 + v6 Tome × Tome) + **ZURAJOVIČ očetovski cross-link 1893→1894** (v2 ženin = sin P122 v6 ženina — Zemelj 18!) + **»1« namesto ulomka** (v12 — 2. primer!) + **občina Orašče [~]** (v15 = 1. neznanka-občina) + **Laipšl-mreža 4. leto** ×5 oseb + **PEZDIREC-cluster ×10** (3 pisave) + Rauy-monopol nazaj **×15/15** (podpisi »M.!« [~] ×13 + »Pf.!« [~] ×2) + mladoletnost 9/30 (gj.-Erkl. ×4 + mamini privolitvi ×3 + obsvorm. ×1) + status-neznanki ×14 (Ans. ×3 + Immosfrss + Wrony Knagge + Wfurj + Göriunas + Kirnšina + hf. + Hoffmann + föd. + naka in + Gistler + Valur/Pofn + zasebnik + Krasb); **GRIBLJE: 2 poroke / 4 poročna bloka (h27 2. dokaz × h42 CERNIČ 1. POROČNI! + h9 2. dokaz × h11 2. dokaz)**; anomalije ×8; vitals **559 → 563** (+ 4 blokov 1894); bloki 04455 = **46**; p80 hiše **41** (vseh 4 že v vzorci!); **P124 LEAD: poročna 1895** (glava 1895 = s94 = Pag. 93 + skeni 94–96 prenešeni); EXCLUDED: 0; skripta scripts/p123_parish_marriage_1894.py (I1–I11); status SAMPLE-TRANSCRIPTION-M1894",
    "P123: PARISH OF PODZEMELJ — MARRIAGE REGISTER 04455, THE FULL YEAR 1894 (issue #18; SAMPLE-TRANSCRIPTION-M1894; the 9th year of the marriage line): the frame CONFIRMED — scans 91–93 == pages 90–92 (page == scan − 1, the 9th confirmation; the printer »Laibach. Druck u. Verlag v. Möttling.« on s92!) — **15 entries** (1886:7 → … → 1894:15) = 6+5+4; **THE BIG HEADING + handwritten »1894« CONFIRMED on s91** (the P123 lead!; the 5th big heading of the line); **15/15 BOTH-SIDES**; **THE BIG 1894 NOVELS**: **★ THE ALL-TIME LINE RECORD COUPLE v5** (groom 64 + bride 48 = 112 years together!) + **THE BRIDE RECORD 56** (v1 Tasič — previously 45 P119!) + **★ the 1st CROSSED-OUT WITNESS of the line** (v12 Đur. Andreas Vojka → Franc Justin zasebnik junior!) + **★ THE PARISH OF IDRIA** (v12 = the longest parish distance ~110 km!) + **★ THE ARMY** (v9 the k.k. Infantry-Regiments-Colonel May 15, 94 №267 — an active soldier groom!) + **★ the 3rd-DEGREE DISPENSATION №2680** (v14 the Laibach Ordinariat Sep 25 — ZUGELJ × TOME) + **★ the LAIBACH LANDSREGIERUNG Ž8667** (v11 — the 1st in the marriage line; dated Sep 9 = 3 WEEKS AFTER the wedding [~]!) + **the SAME-SURNAME marriages ×2** (v3 Perdinec × Perdinec h27×h42 + v6 Tome × Tome) + **the ZURAJOVIČ paternal cross-link 1893→1894** (the v2 groom = the son of the P122 v6 groom — Zemelj 18!) + **the »1« instead of a fraction** (v12 — the 2nd case!) + **the Orašče commune [~]** (v15 = the 1st unknown-commune) + **the Laipšl network the 4th year** ×5 persons + **the PEZDIREC cluster ×10** (3 spellings) + the Rauy monopoly back **×15/15** + the minority 9/30 + the status-unknowns ×14; **GRIBLJE: 2 marriages / 4 marriage blocks (h27 2nd evidence × h42 CERNIČ 1st MARRIAGE! + h9 2nd × h11 2nd)**; anomalies ×8; vitals **559 → 563**; the 04455 blocks = **46**; the p80 houses **41**; **THE P124 LEAD: the marriages of 1895** (the 1895 heading = s94 = p. 93); EXCLUDED: 0; the script scripts/p123_parish_marriage_1894.py (I1–I11); status SAMPLE-TRANSCRIPTION-M1894",
    p123Errors.length === 0,
    p123Errors.length === 0
      ? `15 vpisov (s91–s93 == Pag. 90–92; VELIKA GLAVA + »1894« POTRJENA s91!) · **★ REKORD-PAR v5 (64+48 = 112 let skupaj!)** · **REKORD nevesta 56 (v1 Tasič!)** · ★ 1. PREČRTANI PRIČA (v12 Vojka→Justin!) · ★ PFARRAMT IDRIA (~110 km!) · ★ VOJSKA №267 (v9!) · ★ DISPENS 3.st. №2680 (v14 ZUGELJ×TOME!) · ★ LANDSREGIERUNG Ž8667 (v11 — PO poroki [~]!) · ENAČNOPRIIMEŠKI ×2 (v3 + v6!) · ZURAJOVIČ cross-link 1893→1894 (Zemelj 18!) · »1« ulomek (v12) · občina Orašče [~] · Laipšl 4. leto ×5 · **GRIBLJE 2 poroke / 4 bloka (h27×h42 + h9×h11!)** · vitals 563 · bloki 04455 = 46 · p80 hiše 41 · **P124 LEAD: poročna 1895 (s94 glava!)**`
      : p123Errors.join("; "),
  );
  // ——— qa-p124: POROČNA KNJIGA 04455 — polno leto 1895 (P124; 10. leto poročne linije)
  const p124Marr = HOUSE_VITALS.filter((h) => h.bookSignature === "04455" && h.year === 1895);
  const p124Errors: string[] = [];
  if (p124Marr.length !== 5)
    p124Errors.push(`poročni bloki 1895 (04455) ≠ 5 (${p124Marr.length} — P124: 3 + P125 dopolnitev: + 2 (h24/h14 — s97 v17–v19, 1895 ima 19 vpisov!))`);
  const p124Houses = p124Marr.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
  if (p124Houses.join(",") !== "14,16,24,27,52")
    p124Errors.push(`hiše 1895 (04455) ≠ [14,16,24,27,52] — najdeno: ${p124Houses.join(",")} (P124: v10 h16 Brodarič NOVA HIŠA × v11 h27 Perdinec HOMONIM 3. dokaz × v13 h52 Perdinec NOVA v PT-luknji! + P125: v17 h24 × h14 GRIBLJE × GRIBLJE!)`);
  // P124 pini (1895 bloki; P125 + h14/h24)
  const p124Pins: Array<[string, string]> = [
    ["16", "NOVA HIŠA"], ["16", "BRODARIČ"], ["16", "občine Griblje"],
    ["27", "3. poročni dokaz"], ["27", "HOMONIM"], ["27", "ZUGELJ"], ["27", "KLEPEC"],
    ["52", "NOVA HIŠA"], ["52", "PERDINEC"], ["52", "JAKOBIČ"], ["52", "PT-luknji"],
    ["24", "1. POROČNI DOKAZ h24"], ["24", "DISPENS"], ["24", "GRIBLJE × GRIBLJE"],
    ["14", "1. POROČNI DOKAZ h14"], ["14", "CROSS-LINK"],
  ];
  for (const [n, pin] of p124Pins) {
    const blk = p124Marr.filter((h) => h.houseNo === n);
    if (blk.length === 0) {
      p124Errors.push(`pin ${n} (${pin}) — hiša ${n} ni med 1895 bloki`);
      continue;
    }
    if (!blk.some((cur) => cur.whatSi.toLowerCase().includes(pin.toLowerCase())))
      p124Errors.push(`pin hiša ${n} (${pin}) manjka`);
  }
  // duhovniki 1895 (bloki): Rauy ×5 (P124 3 + P125 2)
  const p124Rauy = p124Marr.filter((h) => h.whatSi.includes("Jos. Rauy")).length;
  if (p124Rauy !== 5)
    p124Errors.push(`Rauy podpisi 1895 blokov ≠ 5 (${p124Rauy} — P124: 3 + P125 dopolnitev: + 2)`);
  // oznake dokazov 1895: h16/h52 NOVA HIŠA + h27 3. poročni dokaz
  if (!p124Marr.some((h) => h.houseNo === "16" && h.whatSi.includes("NOVA HIŠA")))
    p124Errors.push("h16-1895: oznaka »NOVA HIŠA« manjka");
  if (!p124Marr.some((h) => h.houseNo === "52" && h.whatSi.includes("NOVA HIŠA")))
    p124Errors.push("h52-1895: oznaka »NOVA HIŠA« manjka");
  if (!p124Marr.some((h) => h.houseNo === "27" && h.whatSi.includes("3. poročni dokaz")))
    p124Errors.push("h27-1895: oznaka »3. poročni dokaz« manjka");
  // kumulativ: vitals 563 → 566 → 569 (P124: + 3 novih poročnih blokov 1895)
  if (HOUSE_VITALS.length !== 685)
    p124Errors.push(`HOUSE_VITALS ≠ 569 (${HOUSE_VITALS.length} — P123: 563; P124: + 3 novih poročnih blokov (h16/h27/h52-1895; + P125 h24/h14-1895ext + h18-1896) = 569!)`);
  push(
    "qa-p124-parish-marriage-1895",
    "P124: ŽUPNIJA PODZEMELJ — POROČNA KNJIGA 04455, POLNO LETO 1895 (issue #18; SAMPLE-TRANSCRIPTION-M1895; 10. leto poročne linije P115 = 1886 → … → P124 = 1895): okvir POTRJEN — skeni 94–96 == Pag. 93–95 (Pag. == sken − 1, 10. potrditev; velja v 61–96; LANDSCAPE 2510/2511/2521×1800; tiskar »Laibach. Druck u. Verlag v. Möttlig.« na s96!) — **16 vpisov** (1886:7 → … → 1894:15 → 1895:16) = 6+5+5; **VELIKA GLAVA »Trauungs=Buch« + rokopisno »1895« POTRJENA na s94** (P124 lead!; 6. velika glava linije); **16/16 OBOJESTRANSKO**; **VELIKE NOVELE 1895**: **★ 1. ČASTNIK linije** (v15 ženin Herr Andreas Stal, OBERLEUTNANT [~], Metlika 38 × Francisca Logar, hči Offizierja [~], 18 — priča Josef Avanzo k.k. HAUPTMANN + Richard Megušar [~]; **Garnisons-Propstei zū Metlika** 17.6. + mestna občina Metlika št: 150!) + **★ 1. hrvaški dokumenti linije** (v6: ženin Peter Gerdinovac, Krasinec 1 — »zi Pämbig nach Kalchs in Croalien« [~] + smrtni list dekanate v Lipniku [~] od 16/2. + proglasnica občine Griblje **Broj 485** — hrvaško »Broj«!) + **★ POPRAVEK STAROSTI 40→54** (v6 — prečrtana 40; vdovec!) + **★ DISPENS-REKORD ×4** (v7 №504 3. st. krvno + v8 №613 2. st. svarstvo + v12 Ž/L:4994 »Wittwenschaft« [~] — ~2 TEDNA PO poroki! + v16 3.[u2.?] lineae collateralis) + **★ 2. LANDSREGIERUNG Laibach №181** (v8 Beglaubigung 6.2. — cf. P123 Ž8667!) + **★ »Möttling« = nemško ime METLIKE** (k.k. Bez. Ger. Möttling ×4: v2/v8/v9/v14) + **★ HOMONIMA** (v11 Marcus Perdinec f. Marcus ≠ P123 v3 f. Michaël — isto hiša 27! + v8/v14 Johann Starasinič — Krasinec 32 vs 51!) + **★ DVA PRIČA ISTO IME** (v4 Peter Jakofčič ×2 — vzorec P123 v5!) + **3 poroke 11.2. + 3 poroke 19.5. + 2 poroki 26.5.** (8 od 16 vpisov v 3 dnevih; 11.2. = 2. največ za rekordom P122!) + ZUGELJ ×3 + MAYD/MAGD ×2 + Großjährigkeits-Erklärung ×3 (mladoletne 17/20/23!) + formula »in Ungarn … Närnk« [~] ×4 + Kralj ×6 + Marentič ×5 + Jakša ×5 + PERDINEC 5. leto + MUC (cf. P121!) + Rauy-monopol **×16/16** (»M.!« ×7); **GRIBLJE: 3 poroke / 3 poročna bloka (h16 NOVA! + h27 3. dokaz HOMONIM! + h52 NOVA v PT-luknji!)**; anomalije ×8; vitals **563 → 566 → 569** (+ 3 blokov 1895); bloki 04455 = **49 → 52**; p80 hiše **47 → 48** (+h52; h16 že v mrliškem vzorci!); PT luknja **9 → 10** (+h52); **P125 DOKAZAN (dopolnitev 1895 s97: v17–v19 — 1895 = 19 vpisov! + 1896)**; EXCLUDED: 0; skripta scripts/p124_parish_marriage_1895.py (I1–I11); status SAMPLE-TRANSCRIPTION-M1895",
    "P124: PARISH OF PODZEMELJ — MARRIAGE REGISTER 04455, THE FULL YEAR 1895 (issue #18; SAMPLE-TRANSCRIPTION-M1895; the 10th year of the marriage line): the frame CONFIRMED — scans 94–96 == pages 93–95 (page == scan − 1, the 10th confirmation; valid in 61–96; LANDSCAPE 2510/2511/2521×1800; the printer »Laibach. Druck u. Verlag v. Möttlig.« on s96!) — **16 entries** (1886:7 → … → 1895:16) = 6+5+5; **THE BIG HEADING »Trauungs=Buch« + handwritten »1895« CONFIRMED on s94** (the P124 lead!; the 6th big heading of the line); **16/16 BOTH-SIDES**; **THE BIG 1895 NOVELS**: **★ the 1st OFFICER of the line** (v15 groom Herr Andreas Stal, LIEUTENANT [~], Metlika 38 × Francisca Logar, an officer's daughter [~], 18 — witness Josef Avanzo k.k. CAPTAIN + Richard Megušar [~]; the **Garrison-Provost of Metlika** Jun 17 + the town municipality of Metlika no. 150!) + **★ the 1st CROATIAN documents of the line** (v6: groom Peter Gerdinovac, Krasinec 1 — »zi Pämbig nach Kalchs in Croalien« [~] + the death certificate of the deanship in Lipniku [~] from Feb 16 + the announcement of the Griblje commune **Broj 485** — Croatian »Broj«!) + **★ the AGE CORRECTION 40→54** (v6 — crossed-out 40; a widower!) + **★ the DISPENSATION RECORD ×4** (v7 №504 3rd degree consanguinity + v8 №613 2nd degree affinity + v12 Ž/L:4994 »widowhood« [~] — ~2 WEEKS AFTER the wedding! + v16 3rd[u2.?] lineae collateralis) + **★ the 2nd LANDSREGIERUNG Laibach №181** (v8 certification Feb 6 — cf. P123 Ž8667!) + **★ »Möttling« = the German name of METLIKA** (the k.k. district court Möttling ×4: v2/v8/v9/v14) + **★ TWO HOMONYMS** (v11 Marcus Perdinec f. Marcus ≠ P123 v3 f. Michaël — the same house 27! + v8/v14 Johann Starasinič — Krasinec 32 vs 51!) + **★ TWO WITNESSES OF THE SAME NAME** (v4 Peter Jakofčič ×2 — the P123 v5 pattern!) + **3 weddings Feb 11 + 3 weddings May 19 + 2 weddings May 26** (8 of 16 entries in 3 days; Feb 11 = the 2nd most after the P122 record!) + ZUGELJ ×3 + MAYD ×2 + the coming-of-age declarations ×3 (minors 17/20/23!) + the »in Ungarn … Närnk« formula [~] ×4 + Kralj ×6 + Marentič ×5 + Jakša ×5 + PERDINEC the 5th year + Rauy monopoly **×16/16** (»M.!« ×7); **GRIBLJE: 3 marriages / 3 marriage blocks (h16 NEW! + h27 the 3rd evidence HOMONYM! + h52 NEW in the PT gap!)**; anomalies ×8; vitals **563 → 566 → 569**; the 04455 blocks = **49 → 52**; the p80 houses **47 → 48** (+h52); the PT gap **9 → 10** (+h52); **P125 PROVEN (the 1895 supplement s97: v17–v19 — 1895 has 19 entries! + 1896)**; EXCLUDED: 0; the script scripts/p124_parish_marriage_1895.py (I1–I11); status SAMPLE-TRANSCRIPTION-M1895",
    p124Errors.length === 0,
    p124Errors.length === 0
      ? `16 vpisov (s94–s96 == Pag. 93–95; VELIKA GLAVA + »1895« POTRJENA s94!) · **★ 1. ČASTNIK (Oberleutnant Stal + k.k. Hauptmann priča + Garnisons-Propstei Metlika!) · ★ 1. hrvaški dokumenti (in Croalien + Broj 485!) · ★ POPRAVEK 40→54 (vdovec!) · ★ DISPENS ×4 (REKORD!) · ★ 2. LANDSREGIERUNG №181 · ★ Möttling = Metlika (×4!) · ★ homonima Perdinec/Starasinič · ★ priča Jakofčič ×2 · 3+3+2 poroke na 3 dneve · GRIBLJE 3 poroke (h16 NOVA + h27 3. dokaz + h52 NOVA — PT luknja 10!) · vitals 569 · bloki 52 · p80 hiše 48`
      : p124Errors.join("; "),
  );

  // ——— qa-p125: POROČNA KNJIGA 04455 — dopolnitev 1895 (s97) + polno leto 1896 (P125; 11. leto poročne linije)
  const p125Errors: string[] = [];
  // bloki 1896 = 1 (h18) — že preverjeno v qa-p80 sidra-section (hiša 1896 ≠ [18])
  // P125 pini (1896 blok h18)
  const p125Pins: Array<[string, string]> = [
    ["18", "1. POROČNI DOKAZ h18"], ["18", "KLOBUČAR"], ["18", "GROSSJÄHRIGKEITS"], ["18", "KLEPEC"],
  ];
  for (const [n, pin] of p125Pins) {
    const blk = p125Marr.filter((h) => h.houseNo === n);
    if (blk.length === 0) {
      p125Errors.push(`pin ${n} (${pin}) — hiša ${n} ni med 1896 bloki`);
      continue;
    }
    if (!blk.some((cur) => cur.whatSi.toLowerCase().includes(pin.toLowerCase())))
      p125Errors.push(`pin hiša ${n} (${pin}) manjka`);
  }
  // P125 pini (1895-ext bloka h24/h14)
  const p125Pins1895: Array<[string, string]> = [
    ["24", "1. POROČNI DOKAZ h24"], ["24", "GRIBLJE × GRIBLJE"], ["24", "DISPENS"],
    ["14", "1. POROČNI DOKAZ h14"], ["14", "CROSS-LINK"],
  ];
  for (const [n, pin] of p125Pins1895) {
    const blk = p124Marr.filter((h) => h.houseNo === n);
    if (blk.length === 0) {
      p125Errors.push(`pin 1895 ${n} (${pin}) — hiša ${n} ni med 1895 bloki`);
      continue;
    }
    if (!blk.some((cur) => cur.whatSi.toLowerCase().includes(pin.toLowerCase())))
      p125Errors.push(`pin 1895 hiša ${n} (${pin}) manjka`);
  }
  // duhovniki 1896: Rauy 1 blok (h18) — Herms coop. ni blok (v12 ni griblje poroka)
  const p125Rauy = p125Marr.filter((h) => h.whatSi.includes("Jos. Rauy")).length;
  if (p125Rauy !== 1)
    p125Errors.push(`Rauy podpisi 1896 blokov ≠ 1 (${p125Rauy})`);
  // kumulativ: vitals 566 → 569 (P125: + 3 novih poročnih blokov)
  if (HOUSE_VITALS.length !== 685)
    p125Errors.push(`HOUSE_VITALS ≠ 595 (${HOUSE_VITALS.length} — P124: 566; P125: + 3 = 569; P126: + 9 blokov 1897; P127: + 9 blokov 1898 = 587; P128: + 6 blokov 1899 = 610!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length !== 168)
    p125Errors.push(`bloki 04455 ≠ 142 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length} — P124: 49; P125: + 3 = 52; P126: + 9 = 61; P127: + 9 = 70; P128: + 6 = …; P132: + 12 blokov 1903; P133: + 8 blokov 1904; P134: + 13 blokov 1905 = 115!)`);
  push(
    "qa-p125-parish-marriage-1896",
    "P125: ŽUPNIJA PODZEMELJ — POROČNA KNJIGA 04455, DOPOLNITEV 1895 (s97) + POLNO LETO 1896 (issue #18; SAMPLE-TRANSCRIPTION-M1896; 11. leto poročne linije P115 = 1886 → … → P125 = 1896): okvir POTRJEN — s97 = Pag. 96 = NADALJEVANJE 1895 (tiskana podglava; 3 zadnja vpisa 1895!) + s98–s101 == Pag. 97–100 (Pag. == sken − 1, **11. potrditev**; velja v 61–100); **ROKOPISNA GLAVA »1896.« POTRJENA na s98** (cal/s98_year) + **rokopisna glava »1897« + v1/1897 ŽE na s101** (P126 lead!) + s103 = Pag. 102 VELIKA TISKANA GLAVA + v11/1897 (Griblje 40 Nikolaus Perdinec ½ Griblar 22 × Griblje 39 Maria Simic [~] 17!); **1895 = 19 vpisov (P124 16 + P125 ext 3: okt 29 + nov 10 + nov 28)**; **1896 = 15 vpisov** (1886:7 → … → 1895:19 → 1896:15) = feb 5 + apr 1 + maj 4 + avg 2 + okt 2 + nov 1; **18/18 OBOJESTRANSKO**; **VELIKE NOVELE P125**: **★ ⅓ GRIBLAR = NOV ULOMEK LINIJE** (v6 Kolih oče+sin + v10 Jakofčič oče+sin = 4 osebe!; P121: ¼/½/¾) + **1 GRIBLAR** (v2 Marenfič — cel gospodar!) + **★ 1. NEZAKONSKI ŽENIN POROČNE LINIJE** (v14 Peter Grabel: starši [—] + »ledige Magd«!) + **★ 3. duhovnik linije Franz Herms coop.** (v12 — edina prekinitev Rauy-monopola **17/18**, 4. leto zapored!) + **★ 2. ŽANDAR linije** (v4 Eduard (Hubert [~]) Röthl, 24) + **k.k. Beamte oče (1.!)** + rojen **Rudolfswert** (Novo mesto!) + dokumenti **Gottschee + Adelsberg + Laibach** + pravni termin **»Indifferenz«** + ime neveste »Hanna Elisabeth« vs vpis »Anna (Victoria)« (A4!) + **★ ŽAKANJE = HRVAŠKA** (v11: ženin iz Brod b. Žakanje + SLOVENŠČINA »otlični list župnega urada v Zakanjah« — 3. hrvaška povezava!) + **★ »hoc« = hic commorans REŠEN** (×7: v5/v7/v8/v9/v11/v14/v15!) + **★ »mütterl. fürwellig«** (v7 — 1. MATICA daje privoljenje; P124: väterl. ×4!) + formula **»in Ungarn« ×4** (ISTI ŠTEVEC kot P124!) + **★ GROSSJÄHRIGKEIT za ŽENINA** (v3: 22 — 1. za mladoletnega ženina!; + v15 nevesta 21) + **★ DISPENS ×2** (v17-1895 №2906 + v3 №293 — ISTA formulacija 3. st. krvno!) + **★ MUC 3. dokaz** (v1 oče Nicolaus Muc ½ Griblar = P121 v12 ISTA OSEBA + nevesta Maria Muc!) + **★ 2. REKORD-PAR LINIJE** (v18-1895: 59+50 = **109 SKUPAJ**!; v11: 54+47 = 101 = 3.) + ženin 54 (rekord skupaj s P124 v6) + nevesta 47 + **★ v17 = GRIBLJE × GRIBLJE** (h24 Brinsec × h14 Perdinec) + **občinske kontinuitete**: Griblje št:1-3→**4** · Gradac št:21→**22**→**23** · Podzemelj 4→6+8→10→11→121[~] + **h14 CROSS-LINK** (v17 par = krstna 1896 ISTI PAR — ženin oženj v nevestino hišo!) + STRAOS ×4 + PERDINEC ×11 (6. leto!) + KLEPEC ×4 + ZUGELJ ×3 + JAKOFČIČ ×4 (P124 priča ×2!) + Marasinič ×3 (P121!) + JAKŠA ×3 + Kralj ×3 + Butala ×4 + Möttling = Metlika (3. leto!) + Taglöhner ×2 + **Tischlermeister** priča (1. obrtniški mojster!) + Boginja vas ×2; anomalije ×10; vitals **566 → 569** (+ 3 blokov); bloki 04455 = **49 → 52**; p80 hiše **48 → 51 (+h24/h14/h18 — poročna 1895/1896; krstni bloki teh hiš so v 1896/1898, izven p80 vzorca!; p80 POPRAVKI: sidra-skupaj 42→45)**; PT luknja **10 (nespremenjeno)**; **P126 LEAD: poročna 1897** (glava + v1 že na s101 + s103 velika glava + v11 GRIBLJE poroka h40 × h39!); EXCLUDED: 0; skripta scripts/p125_parish_marriage_1896.py (I1–I11); status SAMPLE-TRANSCRIPTION-M1896",
    "P125: PARISH OF PODZEMELJ — MARRIAGE REGISTER 04455, THE 1895 SUPPLEMENT (s97) + THE FULL YEAR 1896 (issue #18; SAMPLE-TRANSCRIPTION-M1896; the 11th year of the marriage line): the frame CONFIRMED — s97 = p. 96 = the 1895 CONTINUATION (the printed sub-header; the 3 last 1895 entries!) + s98–s101 == pages 97–100 (page == scan − 1, the **11th confirmation**; valid in 61–100); **THE HANDWRITTEN HEADING »1896.« CONFIRMED on s98** + **the handwritten heading »1897« + v1/1897 ALREADY on s101** (the P126 lead!) + s103 = p. 102 the BIG PRINTED HEADING + v11/1897; **1895 = 19 entries (P124 16 + P125 ext 3)**; **1896 = 15 entries** = Feb 5 + Apr 1 + May 4 + Aug 2 + Oct 2 + Nov 1; **18/18 BOTH-SIDES**; **THE BIG P125 NOVELS**: **★ ⅓ GRIBLAR = A NEW FRACTION OF THE LINE** (v6 Kolih father+son + v10 Jakofčič father+son = 4 persons!) + **1 GRIBLAR** (v2 — a full farmer!) + **★ the 1st ILLEGITIMATE GROOM of the marriage line** (v14: parents [—] + »ledige Magd«!) + **★ the 3rd priest of the line Franz Herms coop.** (v12 — the only break of the Rauy monopoly **17/18**) + **★ the 2nd GENDARM of the line** (v4 Eduard (Hubert [~]) Röthl) + **a k.k. OFFICIAL father (the 1st!)** + born in **Rudolfswert** (Novo mesto!) + documents from **Gottschee + Adelsberg + Laibach** + the legal term **»Indifferenz«** + the bride's name »Hanna Elisabeth« vs the entry »Anna (Victoria)« (A4!) + **★ ŽAKANJE = CROATIA** (v11 — SLOVENIAN »otlični list« — the 3rd Croatian link!) + **★ »hoc« = hic commorans SOLVED** (×7!) + **★ »mütterl. fürwellig«** (v7 — the 1st MOTHER giving consent!) + the formula **»in Ungarn« ×4** (the SAME count as P124!) + **★ the COMING-OF-AGE for the GROOM** (v3: 22 — the 1st for an underage groom!) + **★ DISPENSATIONS ×2** (№2906 + №293 — the SAME formulation!) + **★ MUC the 3rd evidence** (v1 father Nicolaus Muc = the P121 v12 SAME PERSON + bride Maria Muc!) + **★ the 2nd RECORD COUPLE of the line** (v18-1895: 59+50 = **109 TOGETHER**!) + **★ v17 = GRIBLJE × GRIBLJE** (h24 × h14) + **the municipal numberings**: Griblje 1-3→**4** · Gradac 21→**22**→**23** · Podzemelj 4→121[~] + **the h14 CROSS-LINK** (the v17 couple = the 1896 baptism SAME COUPLE!) + STRAOS ×4 + PERDINEC ×11 + KLEPEC ×4 + ZUGELJ ×3 + JAKOFČIČ ×4 + Marasinič ×3 + JAKŠA ×3 + the **Tischlermeister** witness; anomalies ×10; vitals **566 → 569**; the 04455 blocks = **49 → 52**; the p80 houses **48 → 51 (+h24/h14/h18 — marriages 1895/1896; their baptism blocks (1896/1898) are outside the p80 sample!)**; the PT gap **10 (unchanged)**; **THE P126 LEAD: the marriages of 1897** (the heading + v1 already on s101 + s103 the big heading + v11 the GRIBLJE marriage h40 × h39!); EXCLUDED: 0; the script scripts/p125_parish_marriage_1896.py (I1–I11); status SAMPLE-TRANSCRIPTION-M1896",
    p125Errors.length === 0,
    p125Errors.length === 0
      ? `18 vpisov obojestransko (3× 1895-ext s97 + 15× 1896 s98–s101; Pag. == sken − 1, 11. potrditev!) · **★ ⅓ GRIBLAR (nov ulomek!) · ★ 1. NEZAKONSKI ženin (v14!) · ★ 3. duhovnik Herms coop. (Rauy 17/18) · ★ 2. ŽANDAR + k.k. Beamte oče + Rudolfswert/Gottschee/Adelsberg/Laibach + Indifferenz · ★ Žakanje = HR + slovensko »otlični list« · ★ hoc = hic commorans ×7 · ★ mütterl. fürwellig (1. MATICA!) · ★ in Ungarn ×4 (= P124!) · ★ MUC 3. dokaz · ★ 2. rekord-par 109 · GRIBLJE 2 poroke (h24×h14 + h18!) · kontinuitete Griblje 4 / Gradac 21→22→23 · vitals 569 · bloki 52`
      : p125Errors.join("; "),
  );
  }

  // ——— qa-p126: POROČNA KNJIGA 04455 — polno leto 1897 (P126; 12. leto poročne linije) ———
  {
  const p126Errors: string[] = [];
  if (p126Marr.length !== 9)
    p126Errors.push(`bloki 1897 (04455) ≠ 9 (${p126Marr.length} — 5 GRIBLJE porok = REKORD LINIJE: v5 1 + v9 2 + v10 2 + v11 2 + v18 2 = 9!)`);
  const p126Houses = p126Marr.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
  if (p126Houses.join(",") !== "8,18,27,28,29,33,39,40,40")
    p126Errors.push(`hiše 1897 ≠ [8,18,27,28,29,33,39,40,40] — najdeno: ${p126Houses.join(",")} (h8 v5 NOVA + h40×2 v9/v11 + h29 v9 NOVA + h18 v10 2. dokaz MEGA + h27 v10 + h39 v11 NOVA + h33 v18 NOVA + h28 v18 NOVA!)`);
  // P126 pini (9 blokov)
  const p126Pins: Array<[string, string]> = [
    ["8", "1. POROČNI DOKAZ h8"], ["8", "JAKOBČIČ"], ["8", "Ž:1307"],
    ["40", "1. POROČNI DOKAZ h40"], ["40", "BRODARIČ"], ["40", "A6"],
    ["29", "1. POROČNI DOKAZ h29"], ["29", "KRIŽAN"],
    ["18", "2. POROČNI DOKAZ h18"], ["18", "MEGA CROSS-LINK"], ["18", "KUCHAR"],
    ["27", "Ž:3791"], ["27", "MLADOLETNA"],
    ["39", "1. POROČNI DOKAZ h39"], ["39", "PREDANIC"], ["39", "Ž:3584"],
    ["33", "1. POROČNI DOKAZ h33"], ["33", "DEBLIČ"], ["33", "št:4"],
    ["28", "1. POROČNI DOKAZ h28"], ["28", "LOŽEK"],
  ];
  for (const [n, pin] of p126Pins) {
    const blk = p126Marr.filter((h) => h.houseNo === n);
    if (blk.length === 0) {
      p126Errors.push(`pin ${n} (${pin}) — hiša ${n} ni med 1897 bloki`);
      continue;
    }
    if (!blk.some((cur) => cur.whatSi.toLowerCase().includes(pin.toLowerCase())))
      p126Errors.push(`pin hiša ${n} (${pin}) manjka`);
  }
  // duhovniki 1897: Rauy ×9/9 blokov (v1 Hofstetter Adelsberg = ni blok — ni GRIBLJE poroka)
  const p126Rauy = p126Marr.filter((h) => h.whatSi.includes("Jos. Rauy")).length;
  if (p126Rauy !== 9)
    p126Errors.push(`Rauy podpisi 1897 blokov ≠ 9 (${p126Rauy})`);
  // kumulativ: vitals 587 (569 + 9) + bloki 04455 61
  if (HOUSE_VITALS.length !== 685)
    p126Errors.push(`HOUSE_VITALS ≠ 595 (${HOUSE_VITALS.length} — P125: 569; P126: + 9 blokov 1897; P127: + 9 blokov 1898 = 587; P128: + 6 blokov 1899 = 610!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length !== 168)
    p126Errors.push(`bloki 04455 ≠ 142 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length} — P125: 52; P126: + 9 = 61; P127: + 9 = 70; P128: + 6 = …; P132: + 12 blokov 1903; P133: + 8 blokov 1904; P134: + 13 blokov 1905 = 115!)`);
  push(
    "qa-p126-parish-marriage-1897",
    "P126: ŽUPNIJA PODZEMELJ — POROČNA KNJIGA 04455, POLNO LETO 1897 (issue #18; SAMPLE-TRANSCRIPTION-M1897; 12. leto poročne linije P115 = 1886 → … → P126 = 1897): okvir POTRJEN — s101 = Pag. 100 (v15/1896 nad glavo!) + s102–s104 == Pag. 101–103 (Pag. == sken − 1, **12. potrditev**; velja v 61–104); **ROKOPISNA GLAVA »1897« (dvopodčrtana) POTRJENA na s101** + **rokopisna glava »1898.« + v1/1898 ŽE na s104** (P127 lead!); **1897 = 18 vpisov** (1886:7 → 1887:21 → 1888:20 → 1889:10 → 1890:16 → 1891:18 → 1892:15 → 1893:20 → 1894:15 → 1895:19 → 1896:15 → **1897:18**) = jan 1 + feb 8 + maj 2 + jul 2 + avg 2 + okt 2 + nov 1; **18/18 OBOJESTRANSKO**; **VELIKE NOVELE P126**: **★ GRIBLJE poroke ×5 = REKORD LINIJE** (prej 3 — P121 1892!: v5 h8 × Krasinec + v9 h40×h29 + v10 h18×h27 + v11 h40×h39 + v18 h33×h28 — 9 poročnih blokov!) + **★ 2. prekinitev Rauy-monopola: v1 Johann Hofstetter [~], Dechant? in ADELSBERG (Postojna!), per deleg.** (Rauy 17/18 — nevestin oče k.k. pension. Förster + k.k. Bez.Ger. Adelsberg dokumenti!) + **★ 1. FOTOGRAF-PRIČA LINIJE** (v1: Z2 Pfüllkojf? [~] Photograph!) + **★ MEGA CROSS-LINK v10: Mathias Simec h18 × Anna Kuchar h27 = PAR iz krstne 04105 1898 h18** (oče Matija Šimec × mati Ana Kukar — »izmena gospodinjstva« P125 bloka h18 REŠENA: Klobučar-hči se 1896 poroči ven (Berkovec), Simec×Kuchar preživi h18 od 1897!) + **★ DVOJNA SODNA POLNOLETNOST v15** (ženin na okrajnem sodišču v RUDOLFOVEM 23/8. + nevesta v Metliki 22/8. — + zglasmica Smihel? Škofjič? št:46 + župnijski list Vavta vas = 4 dokumenti!) + **★ SAMSKI LIST v16** (»Upričevalo samskiga stana za nevesto« od župnega urada v Dragatušem 23/9.97 št:405 — 1. jasno imenovano samsko upričevanje linije!) + **★ NADOARSTVENO dovoljenje v12** (sodišče Metlika 1/7. št:103 — slovenska vzporednica Vormundschaft P125!) + **★ SLOVENSKA sodna polnoletnost v5** (»Ml. nevesta pol. veljetna sprozana od c.k. okr. sodisča v Črnomlju z dnom 6. febr. 1897. Ž:1307«!) + **★ 1. MÜTTERLICH sodna privolitev v10** (k.k. Bez.Ger. Črnomelj Ž:3791 — za mladoletno nevesto 16!) + **★ formula »in Ungarn« ×8 = LINIJSKI REKORD** (v4[~], v6, v7, v8, v11-ženin!, v14, v16-ženin!, v17 — očetje v Bejni Krajini delajo na Madžarskem!) + **★ v3: ženin 55½ NEZAKONSKI** (mati Gertrud Koplan ledig. — 2. nezakonski ženin + 2. najstarejši ženin; nevesta 41!) + **★ v13: DVOJNI status »½ gbl. Sohn und Zimmermann«** (½ Griblar-sin IN tesar!) + **A6: DVA ženina h40 v enem letu** (v9 Brodarič + v11 Predanic!) + **A7: Predanic/Perdinec varianta v enem vpisu** (v11!) + **občinske vrste zglasmic**: Podzemelj št:1 (23/1.) → **2–6 (12/2. — MEŠANI vrstni red: v8=2, v5=3, v6=4, v7=5, v4=6!)** → 9 (15/7.) → 10 (16/10.) | **Griblje št:1→2→3→4 POPOLNA vrsta** (»manjkajoča« 2 izdana dan prej kot 3 — razrešeno z v11!) | Gradac 26 (23/7.) → 8?[~A5] (29/8.) → 27 (8/10.) | Smihel? Škofjič? 46 (17/8.) + mestna občina Črnomelj? D:264 ×2 [~]; **familijne mreže 1897**: ŠTARASINIČ ×4 · JAKOBČIČ ×5 · KLEPEC ×5 · PERDINEC ×6 (7. leto!) · PAPIČ ×5 · SIMEC ×4 · KRIŽAN ×3 · MILEK ×3 · SCHWEIGER ×3 · BRINEC ×3 · ZUGELJ ×3 · MALEŠIČ ×2 · ZIMMERMANN ×2; anomalije ×11; vitals **569 → 578** (+ 9 blokov); bloki 04455 = **52 → 61**; p80 hiše **51 → 52 (+h28 EDINA NOVA — h8/h39 že v 04105-1886 P79, h29 že v mrliški 04894 ×3, h33 že v 04455-1888, h40/h27/h18 že v vzorci)**; PT luknja **10 (nespremenjeno)**; **P127 LEAD: poročna 1898** (rokopisna glava »1898.« + v1/1898 Jänner 25, Gradec 32? Anton Jane? [~] × Vrhtar? 21 Maria Hovcar [~] 19½ že na s104; skeni 105–109 že prenešeni); EXCLUDED: 0; skripta scripts/p126_parish_marriage_1897.py (I1–I11); status SAMPLE-TRANSCRIPTION-M1897",
    "P126: PARISH OF PODZEMELJ — MARRIAGE REGISTER 04455, THE FULL YEAR 1897 (issue #18; SAMPLE-TRANSCRIPTION-M1897; the 12th year of the marriage line): the frame CONFIRMED — s101 = p. 100 (v15/1896 above the heading!) + s102–s104 == pages 101–103 (page == scan − 1, the **12th confirmation**; valid in 61–104); **THE HANDWRITTEN HEADING »1897« (double-underlined) CONFIRMED on s101** + **the handwritten heading »1898.« + v1/1898 ALREADY on s104** (the P127 lead!); **1897 = 18 entries** (…→ 1896:15 → **1897:18**) = Jan 1 + Feb 8 + May 2 + Jul 2 + Aug 2 + Oct 2 + Nov 1; **18/18 BOTH-SIDES**; **THE BIG P126 NOVELS**: **★ GRIBLJE marriages ×5 = THE LINE RECORD** (previously 3 — P121 1892!: v5 h8 × Krasinec + v9 h40×h29 + v10 h18×h27 + v11 h40×h39 + v18 h33×h28 — 9 marriage blocks!) + **★ the 2nd break of the Rauy monopoly: v1 Johann Hofstetter [~], Dean? in ADELSBERG (Postojna!), per deleg.** (Rauy 17/18 — the bride's father a k.k. pensioned forester + k.k. Bez.Ger. Adelsberg documents!) + **★ the 1st PHOTOGRAPHER-WITNESS of the line** (v1: Z2 Pfüllkojf? [~] Photograph!) + **★ the MEGA CROSS-LINK v10: Mathias Simec h18 × Anna Kuchar h27 = THE COUPLE from the 1898 baptism 04105 h18** (the »household change« of the P125 h18 block SOLVED: the Klobučar daughter married out 1896 (Berkovec), Simec×Kuchar occupy h18 from 1897!) + **★ the DOUBLE COURT COMING-OF-AGE v15** (the groom at the district court in RUDOLFSWERT Aug 23 + the bride in Metlika Aug 22 — 4 documents!) + **★ the CELIBACY CERTIFICATE v16** (»Upričevalo samskiga stana« from the parish office in Dragatus Sep 23, 1897 no:405 — the 1st explicitly named celibacy certificate of the line!) + **★ the SUPRA-MUNICIPAL permission v12** (the Metlika court Jul 1 no:103 — the Slovene parallel of the P125 Vormundschaft!) + **★ the SLOVENE court coming-of-age v5** (Ž:1307!) + **★ the 1st MÜTTERLICH court consent v10** (Ž:3791 — for the minor bride 16!) + **★ the formula »in Ungarn« ×8 = THE LINE RECORD** (v4[~], v6, v7, v8, v11-groom!, v14, v16-groom!, v17!) + **★ v3: the groom 55½ ILLEGITIMATE** (mother Gertrud Koplan single — the 2nd illegitimate groom + the 2nd oldest groom; the bride 41!) + **★ v13: the DOUBLE status »½ gbl. Sohn und Zimmermann«** + **A6: TWO grooms of h40 in one year** (v9 Brodarič + v11 Predanic!) + **A7: the Predanic/Perdinec variant in one entry** + **the municipal certificate series**: Podzemelj 1 → **2–6 (Feb 12 — MIXED order!)** → 9 → 10 | **Griblje 1→2→3→4 COMPLETE** | Gradac 26 → 8?[~A5] → 27 | Smihel? Škofjič? 46; **the family networks 1897**: ŠTARASINIČ ×4 · JAKOBČIČ ×5 · KLEPEC ×5 · PERDINEC ×6 (the 7th year!) · PAPIČ ×5 · SIMEC ×4 · KRIŽAN ×3 · MILEK ×3 · SCHWEIGER ×3 · BRINEC ×3 · ZUGELJ ×3; anomalies ×11; vitals **569 → 578** (+ 9 blocks); the 04455 blocks = **52 → 61**; the p80 houses **51 → 52 (+h28 the ONLY new one)**; the PT gap **10 (unchanged)**; **THE P127 LEAD: the marriages of 1898** (the heading »1898.« + v1/1898 already on s104; scans 105–109 already transferred); EXCLUDED: 0; the script scripts/p126_parish_marriage_1897.py (I1–I11); status SAMPLE-TRANSCRIPTION-M1897",
    p126Errors.length === 0,
    p126Errors.length === 0
      ? `18 vpisov obojestransko (s101–s104 == Pag. 100–103; Pag. == sken − 1, 12. potrditev!) · **★ GRIBLJE poroke ×5 = REKORD LINIJE (9 blokov: h8 + h40×2 + h29 + h18 MEGA + h27 + h39 + h33 + h28!) · ★ 2. prekinitev Rauy-monopola (Hofstetter Adelsberg per deleg. — Rauy 17/18) · ★ 1. FOTOGRAF-priča (v1!) · ★ MEGA CROSS-LINK v10 (Simec×Kuchar = krstna 1898 h18 PAR — izmena REŠENA!) · ★ dvojna sodna polnoletnost v15 (Rudolfovo + Metlika!) · ★ samski list v16 (Dragatus št:405!) · ★ nadoarstveno dovoljenje v12 · ★ slovenska polnoletnost v5 (Ž:1307) · ★ 1. mütterlich privolitev v10 (Ž:3791) · ★ in Ungarn ×8 REKORD · ženin 55½ NEZAKONSKI (v3) · občine: Podzemelj 1→2–6 MEŠANO→9→10 + Griblje 1→2→3→4 POPOLNA · vitals 587 · bloki 70 · p80 hiše 52`
      : p126Errors.join("; "),
  );
  }

  // ——— qa-p127: POROČNA KNJIGA 04455 — polno leto 1898 (P127; 13. leto poročne linije) ———
  {
  const p127Errors: string[] = [];
  if (p127Marr.length !== 9)
    p127Errors.push(`bloki 1898 (04455) ≠ 9 (${p127Marr.length} — 6 GRIBLJE porok = NOVI REKORD LINIJE: v2 1 + v7 2 + v9 1 + v11 2 + v15 1 + v20 2 = 9!)`);
  const p127Houses = p127Marr.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
  if (p127Houses.join(",") !== "22,22,34,46,48,54,62,67,70")
    p127Errors.push(`hiše 1898 ≠ [22,22,34,46,48,54,62,67,70] — najdeno: ${p127Houses.join(",")} (h48 v2 NOVA + h22×2 v7/v9 A6 ISTI DAN + h67 v7 NOVA + h54 v11 2. dokaz SIMEC + h62 v11 NOVA + h70 v15 NOVA + h34 v20 1. dokaz + h46 v20 NOVA!)`);
  // P127 pini (9 blokov)
  const p127Pins: Array<[string, string]> = [
    ["48", "1. POROČNI DOKAZ h48"], ["48", "KLOBUČAR"], ["48", "Pniloxje"],
    ["22", "1. POROČNI DOKAZ h22"], ["22", "STRAUS"], ["22", "A6"], ["22", "MILEK"],
    ["67", "1. POROČNI DOKAZ h67"], ["67", "JAKOFČIČ"],
    ["54", "2. POROČNI DOKAZ h54"], ["54", "SIMEC"],
    ["62", "1. POROČNI DOKAZ h62"], ["62", "KURE"],
    ["70", "1. POROČNI DOKAZ h70"], ["70", "PERDINEC"],
    ["34", "1. POROČNI DOKAZ h34"], ["34", "FILAK"],
    ["46", "1. POROČNI DOKAZ h46"], ["46", "KLOBUČAR"],
  ];
  for (const [n, pin] of p127Pins) {
    const blk = p127Marr.filter((h) => h.houseNo === n);
    if (blk.length === 0) {
      p127Errors.push(`pin ${n} (${pin}) — hiša ${n} ni med 1898 bloki`);
      continue;
    }
    if (!blk.some((cur) => cur.whatSi.toLowerCase().includes(pin.toLowerCase())))
      p127Errors.push(`pin hiša ${n} (${pin}) manjka`);
  }
  // duhovniki 1898: Rauy ×9/9 blokov (Herms ×2 zapored v13 coop. + v14 coad. — nista GRIBLJE bloka!)
  const p127Rauy = p127Marr.filter((h) => h.whatSi.includes("Jos. Rauy")).length;
  if (p127Rauy !== 9)
    p127Errors.push(`Rauy podpisi 1898 blokov ≠ 9 (${p127Rauy})`);
  // kumulativ: vitals 587 (578 + 9) + bloki 04455 70
  if (HOUSE_VITALS.length !== 685)
    p127Errors.push(`HOUSE_VITALS ≠ 595 (${HOUSE_VITALS.length} — P126: 578; P127: + 9 blokov 1898 = 587; P128: + 6 blokov 1899 = 610!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length !== 168)
    p127Errors.push(`bloki 04455 ≠ 142 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length} — P126: 61; P127: + 9 = 70; P128: + 6 = …; P132: + 12 blokov 1903; P133: + 8 blokov 1904; P134: + 13 blokov 1905 = 115!)`);
  push(
    "qa-p127-parish-marriage-1898",
    "P127: ŽUPNIJA PODZEMELJ — POROČNA KNJIGA 04455, POLNO LETO 1898 (issue #18; SAMPLE-TRANSCRIPTION-M1898; 13. leto poročne linije P115 = 1886 → … → P127 = 1898): okvir POTRJEN — s104–s109 == Pag. 103–108 (Pag. == sken − 1, **13. potrditev**; velja v 61–108); **ROKOPISNA GLAVA »1898.« POTRJENA na s104** + **rokopisna glava »1899.« + v1–5/1899 ŽE na s110 = Pag. 109** (P128 lead!); **1898 = 27 vpisov = REKORD LINIJE** (prej 21 — P122/1887!) = jan 2 + feb 8 + maj 4 + jun 3 + jul 2 + okt 1 + nov 7 (brez mar/avg/sep/dec!); **21.11. ×6 porok (v22–v27) = 2. največji dan linije** (rekord 7 — P122!); **27/27 OBOJESTRANSKO**; **VELIKE NOVELE P127**: **★ GRIBLJE poroke ×6 = NOVI REKORD LINIJE** (prej 5 — P126 1897!: v2 h48 × Pniloxje? 30 [~] + v7 h22×h67 + v9 h22 × Horst? 21 [~] + v11 h54×h62 + v15 h70 × Krasinec + v20 h34×h46 — 9 poročnih blokov!) + **★ BRAT/SESTRA ŽUPANIČ cross-entry** (v8 ženin Johann + v13 nevesta Dorothea = otroka Mathiasa Županiča ½ griblar × Catharine Šaradinič, Krasinec 18 — 1. tak cross-entry link poročne linije!) + **★ ⅛ griblar** (v23 ženinov oče Franz Tomič — NOVI najnižji ulomek linije, prej 3/16 v6!) + **★ k.k. LANDESREGIERUNG Laibach Z:12527 (28.8.1898) za OBA mladoletna** (v20 — »für die mlj. Braut und mlj. Bräutigam« — popolna formula, 2. Landesregierung-dokument linije!) + **★ MÖTTLING = nemško METLIKA 5.–6. dokaz** (v9 k.k. Bez.Ger. Erklärung 9/2. + v17 [?]amte Möttling 4/6. + tiskar »Einbd. Druck u. Verlag v. Bindig in Möttlig.« na v13!) + **★ KURRENT-REŠITEV: »in Gegenwart obiger Beystände«** ×5 (v10/v15/v19/v20/v27 — faza-1 »in Ungarnwärts obige Varpända« = misread; descender-G + st-ligatura!) + **★ SLOVENSKI EKVIVALENT formule** ×2 (v11 polna + v12 rep [~] — »v navzočnosti [zgornjih prič]« = dvojezični par, skupaj 7!) + **★ Herms ×2 ZAPORED** (v13 coop. + v14 coad. — Rauy 25/27) + **★ UMRTVENI LIST PRVE ŽENE ženinove** (v23 — 1. tak dokument; župnijski urad Sv. Vid pri Žatičmi? [~]) + **★ Decanatsamt Rudolfswert + Bischofs-Akt L:275** (v21) + **★ JAMŠKI LIST od župnijskega urada v BOROVNICI** (v25 — 1. Borovnica-dokument linije) + **★ v16: 3. NEZAKONSKI ženin linije** (prazna očetova celica + mati Taglöhnerin!) + **★ v20: OBA mladoletna** (ženin 20 + nevesta 21 — edini tak poročni par linije!) + **★ v23: vdovec 41 Holzarbeiter-Aufseher geb. ČRNI VRH OB IDRIJCI** + **★ v7+v9: GRIBLJE 22 ×2 ženina ISTI DAN (20.2.)** — domačija »Nikolaus«: oba ženina poimenovana po domačiji (A6!) + **Zaiflner stand ×5–6** + **»z güblarštofa« ×3** (v2/v9/v24 [~]) + **PLUT ×3** (v10/v14/v19 matere) + **Pedirec/Perdinec varianta ×7** + **KRIŽAN ×2 matere** (v9) + **ŠARADINIČ/Staradinič ×3** + **MUC 4. dokaz** (v24) + **občinske vrste zglasmic**: Podzemelj 7→8→9→10→12→14 | **Griblje 1→2→4** | **Gradac 31→32→33→34→35 POPOLNA vrsta** (v13→v27!) | Smihel-Dopine? 29→39 | Krasinec 13 | Črni Vrh 15 | Suho 2 + Proclamation? Črnomelj (v22); **mreže 1898**: KLOBUČAR ×3 · KLEPEC ×4 · PERDINEC ×8 (8. leto!) · ŽUPANIČ ×4 · NOVAK ×3 · MILEK ×2 · MALEŠIČ ×2; anomalije + OSTAJOČI [~] (vasi: Pniloxje 30, Krivoglavs(e) 11, Cerkuveda? 12/24, Cerkvišče? 31, Germ 28, Gišič? 1, Dorst/Horst? 21, B. Suhor?, Kloster 37/43/69/85; imena: Dečaj?, Fatič?, Filetič?, Suehek?, Brucel?, Joček?, Dehlič?, Zajman?, Grabus?, Kraij?, Stuhljar?, Zaveršnik?, Vernikman?, Žiličič?; standi: Zaiflner, Kaylühner, z güblarštofa); vitals **578 → 587** (+ 9 blokov); bloki 04455 = **61 → 70**; p80 hiše **52 → 58 (+h48/h22/h67/h70/h34/h46 — 6 NOVIH v vzorcu prek poročne 04455-1898; vseh 6 že v krstni 04105, a 04105-vzorec restriktiven!)**; PT luknja **10 → 12 (+h46/h48 v luknji 41–60!)**; **P128 LEAD: poročna 1899** (rokopisna glava »1899.« + v1–5/1899 že na s110; skeni 110–111 v .p126tmp; novi skeni 112+ prenesti — vzorec P127!); EXCLUDED: 0; skripta scripts/p127_parish_marriage_1898.py (I1–I11); status SAMPLE-TRANSCRIPTION-M1898",
    "P127: PARISH OF PODZEMELJ — MARRIAGE REGISTER 04455, THE FULL YEAR 1898 (issue #18; SAMPLE-TRANSCRIPTION-M1898; the 13th year of the marriage line P115 = 1886 → … → P127 = 1898): the frame CONFIRMED — s104–s109 == pages 103–108 (page == scan − 1, the **13th confirmation**; valid in 61–108); **THE HANDWRITTEN HEADING »1898.« CONFIRMED on s104** + **the handwritten heading »1899.« + v1–5/1899 ALREADY on s110 = p. 109** (the P128 lead!); **1898 = 27 entries = THE LINE RECORD** (previously 21 — P122/1887!) = Jan 2 + Feb 8 + May 4 + Jun 3 + Jul 2 + Oct 1 + Nov 7 (no Mar/Aug/Sep/Dec!); **Nov 21 ×6 weddings (v22–v27) = the 2nd biggest day of the line** (the record 7 — P122!); **27/27 BOTH-SIDES**; **THE BIG P127 NOVELS**: **★ GRIBLJE marriages ×6 = THE NEW LINE RECORD** (previously 5 — P126 1897!: v2 h48 × Pniloxje? 30 [~] + v7 h22×h67 + v9 h22 × Horst? 21 [~] + v11 h54×h62 + v15 h70 × Krasinec + v20 h34×h46 — 9 marriage blocks!) + **★ THE ŽUPANIČ BROTHER/SISTER cross-entry** (v8 groom Johann + v13 bride Dorothea = the children of Mathias Županič ½ griblar × Catharine Šaradinič, Krasinec 18 — the 1st such cross-entry link of the marriage line!) + **★ ⅛ smallholder** (v23 the groom's father Franz Tomič — the NEW lowest fraction of the line, previously 3/16 v6!) + **★ THE k.k. LANDESREGIERUNG Laibach Z:12527 (Aug 28, 1898) for BOTH minors** (v20 — »for the mlj. bride and mlj. groom« — the complete formula, the 2nd Landesregierung document of the line!) + **★ MÖTTLING = German METLIKA, the 5th–6th proof** (v9 the k.k. Bez.Ger. Erklärung Feb 9 + v17 the [?]amte Möttling Jun 4 + the printer »Einbd. Druck u. Verlag v. Bindig in Möttlig.« on v13!) + **★ THE KURRENT SOLUTION: »in Gegenwart obiger Beystände«** ×5 (v10/v15/v19/v20/v27 — the faza-1 »in Ungarnwärts obige Varpända« = a misread; the descender-G + the st-ligature!) + **★ THE SLOVENE EQUIVALENT of the formula** ×2 (v11 full + v12 tail [~] — »v navzočnosti [zgornjih prič]« = the bilingual pair, 7 total!) + **★ Herms ×2 CONSECUTIVE** (v13 coop. + v14 coad. — Rauy 25/27) + **★ THE DEATH CERTIFICATE OF THE GROOM'S FIRST WIFE** (v23 — the 1st such document; the parish office Sv. Vid pri Žatičmi? [~]) + **★ the Decanatsamt Rudolfswert + the Bischofs-Akt L:275** (v21) + **★ THE GUARANTEE LETTER from the parish office in BOROVNICA** (v25 — the 1st Borovnica document of the line) + **★ v16: the 3rd ILLEGITIMATE groom of the line** (an empty father cell + the mother a Taglöhnerin!) + **★ v20: BOTH minors** (the groom 20 + the bride 21 — the only such married couple of the line!) + **★ v23: the widower 41 Holzarbeiter-Aufseher born ČRNI VRH OB IDRIJCI** + **★ v7+v9: GRIBLJE 22 ×2 grooms THE SAME DAY (Feb 20)** — the homestead »Nikolaus«: both grooms named after the homestead (A6!) + **the Zaiflner status ×5–6** + **»z güblarštofa« ×3** (v2/v9/v24 [~]) + **PLUT ×3** (v10/v14/v19 mothers) + **the Pedirec/Perdinec variant ×7** + **KRIŽAN ×2 mothers** (v9) + **ŠARADINIČ/Staradinič ×3** + **the MUC 4th proof** (v24) + **the municipal certificate series**: Podzemelj 7→8→9→10→12→14 | **Griblje 1→2→4** | **Gradac 31→32→33→34→35 COMPLETE** (v13→v27!) | Smihel-Dopine? 29→39 | Krasinec 13 | Črni Vrh 15 | Suho 2 + the Proclamation? Črnomelj (v22); **the networks 1898**: KLOBUČAR ×3 · KLEPEC ×4 · PERDINEC ×8 (the 8th year!) · ŽUPANIČ ×4 · NOVAK ×3 · MILEK ×2 · MALEŠIČ ×2; anomalies + the REMAINING [~] (villages: Pniloxje 30, Krivoglavs(e) 11, Cerkuveda? 12/24, Cerkvišče? 31, Germ 28, Gišič? 1, Dorst/Horst? 21, B. Suhor?, Kloster 37/43/69/85; names: Dečaj?, Fatič?, Filetič?, Suehek?, Brucel?, Joček?, Dehlič?, Zajman?, Grabus?, Kraij?, Stuhljar?, Zaveršnik?, Vernikman?, Žiličič?; statuses: Zaiflner, Kaylühner, z güblarštofa); vitals **578 → 587** (+ 9 blocks); the 04455 blocks = **61 → 70**; the p80 houses **52 → 58 (+h48/h22/h67/h70/h34/h46 — 6 NEW in the sample via the marriage 04455-1898; all 6 already in the baptism 04105, but the 04105 sample is restrictive!)**; the PT gap **10 → 12 (+h46/h48 in the 41–60 gap!)**; **THE P128 LEAD: the marriages of 1899** (the handwritten heading »1899.« + v1–5/1899 already on s110; scans 110–111 in .p126tmp; new scans 112+ to download — the P127 pattern!); EXCLUDED: 0; the script scripts/p127_parish_marriage_1898.py (I1–I11); status SAMPLE-TRANSCRIPTION-M1898",
    p127Errors.length === 0,
    p127Errors.length === 0
      ? `27 vpisov = REKORD LINIJE (s104–s109 == Pag. 103–108; Pag. == sken − 1, 13. potrditev!) · **6 porok 21.11. = 2. največji dan linije** · **★ GRIBLJE poroke ×6 = NOVI REKORD (9 blokov: h48 + h22×2 A6 + h67 + h54 SIMEC + h62 + h70 + h34 + h46 — OBA mladoletna v20!)** · **★ BRAT/SESTRA ŽUPANIČ (v8+v13 — Krasinec 18, 1. cross-entry link!)** · **★ ⅛ griblar (v23 — najnižji ulomek linije!)** · **★ Landesreg. Laibach Z:12527 za OBA mladoletna (v20!)** · **★ Möttling = Metlika 5.–6. dokaz + tiskar Bindig in Möttlig** · **★ KURRENT-REŠITEV »in Gegenwart obiger Beystände« ×5 + slovenski ekvivalent ×2 (v11/v12 — skupaj 7!)** · **★ Herms ×2 zapored (Rauy 25/27)** · **★ umrtveni list prve žene (v23) + jamški list Borovnica (v25) + Bischofs-Akt L:275 (v21)** · občine: Podzemelj 7→14 · Griblje 1→2→4 · Gradac 31→35 POPOLNA · vitals 587 · bloki 04455 = 70 · p80 hiše 58 · PT luknja 12 · **P128 LEAD: poročna 1899 (glava + v1–5/1899 že na s110!)**`
      : p127Errors.join("; "),
  );
  }
  // ——— qa-p128: POROČNA KNJIGA 04455 — polno leto 1899 (P128; 14. leto poročne linije) ———
  {
  const p128Errors: string[] = [];
  if (p128Marr.length !== 6)
    p128Errors.push(`bloki 1899 (04455) ≠ 6 (${p128Marr.length} — 3 GRIBLJE poroke: v1 2 + v3 2 + v4 2 = 6!)`);
  const p128Houses = p128Marr.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
  if (p128Houses.join(",") !== "1,10,16,20,34,44")
    p128Errors.push(`hiše 1899 ≠ [1,10,16,20,34,44] — najdeno: ${p128Houses.join(",")} (v1 h34 2. dokaz ŽIBAK? [~ Filak-tension!] × h44 1. dokaz NAJSTAREJŠI PAR 66×68! + v3 h1 1. dokaz NAJNIŽJA ŠTEVILKA × h10 3. dokaz KURE! + v4 h20 2. dokaz × h16 3. dokaz!)`);
  // P128 pini (6 blokov)
  const p128Pins: Array<[string, string]> = [
    ["34", "NAJSTAREJŠI PAR"], ["34", "ŽIBAK"], ["34", "Štrigžingtar"],
    ["44", "1. POROČNI DOKAZ h44"], ["44", "KLOBUČAR"],
    ["1", "1. POROČNI DOKAZ h1"], ["1", "ŽELJKO"], ["1", "oče ženina kot priča"],
    ["10", "3. poročni dokaz h10"], ["10", "KURE"], ["10", "MUC"],
    ["20", "2. POROČNI DOKAZ h20"], ["20", "NOVAK"], ["20", "Zimmermannsmeister"],
    ["16", "3. poročni dokaz h16"], ["16", "ŽIBAK"], ["16", "v1 ženin"],
  ];
  for (const [n, pin] of p128Pins) {
    const blk = p128Marr.filter((h) => h.houseNo === n);
    if (blk.length === 0) {
      p128Errors.push(`pin ${n} (${pin}) — hiša ${n} ni med 1899 bloki`);
      continue;
    }
    if (!blk.some((cur) => cur.whatSi.toLowerCase().includes(pin.toLowerCase())))
      p128Errors.push(`pin hiša ${n} (${pin}) manjka`);
  }
  // duhovniki 1899: Novak 3/6 blokov (GRIBLJE v1+v4 Sturm? — v1 Novak, v3 Rauy, v4 Sturm) — 1899 celotno: Novak 5 + Rauy 2 + Sturm 2 = 9
  const p128Novak = p128Marr.filter((h) => h.whatSi.includes("Jos. Novak")).length;
  const p128Rauy = p128Marr.filter((h) => h.whatSi.includes("Jos. Rauy")).length;
  const p128Sturm = p128Marr.filter((h) => h.whatSi.toLowerCase().includes("franz sturm")).length;
  if (p128Novak !== 2 || p128Rauy !== 2 || p128Sturm !== 2)
    p128Errors.push(`duhovniki 1899 blokov (GRIBLJE 6) ≠ Novak 2 + Rauy 2 + Sturm 2 (najdeno: Novak ${p128Novak} + Rauy ${p128Rauy} + Sturm ${p128Sturm} — v1 ×2 bloki Novak + v3 ×2 Rauy + v4 ×2 Sturm!)`);
  // kumulativ: vitals 595 (587 + 6) + bloki 04455 76
  if (HOUSE_VITALS.length !== 685)
    p128Errors.push(`HOUSE_VITALS ≠ 593 (${HOUSE_VITALS.length} — P127: 587; P128: + 6 blokov 1899 = 610!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length !== 168)
    p128Errors.push(`bloki 04455 ≠ 142 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length} — P127: 70; P128: + 6 = …; P132: + 12 blokov 1903; P133: + 8 blokov 1904; P134: + 13 blokov 1905 = 115!)`);
  push(
    "qa-p128-parish-marriage-1899",
    "P128: ŽUPNIJA PODZEMELJ — POROČNA KNJIGA 04455, POLNO LETO 1899 (issue #18; SAMPLE-TRANSCRIPTION-M1899; 14. leto poročne linije P115 = 1886 → … → P128 = 1899): okvir POTRJEN — s110–s111 == Pag. 109–110 (Pag. == sken − 1, **14. potrditev**; velja 61–110); **ROKOPISNA GLAVA »1899.« POTRJENA na s110** + **rokopisna glava »1900.« POTRJENA na s112** (dvopodčrtana, pod tiskanimi stolpci — P129 lead + v1/1900 Jänner 2 Krasinec 18 = ŽUPANIČ hiša P127 v8/v13!); **1899 = 9 vpisov = 3. najmanjše leto linije (po 1900:8!)** (min 1886:7; −18 po rekordnem 1898:27!) = jan 3 + feb 1 + maj 1 + jun 1 + avg 1 + sep 1 + okt 1 (brez mar/apr/jul/nov/dec!); **30.1. ×2 poroke (v2+v3)**; **9/9 OBOJESTRANSKO**; **VELIKE NOVELE P128**: **★ NAJSTAREJŠI PAR LINIJE** (v1: ženin Johann Žibak? [~] 66 + nevesta Maria [Ś/H]rudej? [~] 68 = 134 let, OBA status 1 = 1. poroka!) + **★ ¾ GIBLAR = NOVI NAJVIŠJI ULOMEK LINIJE** (v7 nevesta Anna Žugelj ¾ griblars-tochter + oče Nicolaus Žugelj ¾ griblar; prej najvišji ½, najnižji ⅛ P127 v23!) + **★ 1. ŽENIN POPOLNOMA IZVEN SISTEMA** (v9 Franc Darovic? [~], Idrišina? 1, Pf. St. Michel b. RUDOLFSWERTH = Novo mesto, Knecht 36!) + **★ ZGLASMICA-PENTAGON: 5 občin** (Griblje 2/3/5 — št 1+4 = drugi civilni akti · Podzemelj 1/3/4 — št 4 IZVEN VRSTNEGA REDA: dispens 21/4 → zglasmica 30/4 → poroka 5.8.! · Gradac 57 · na Gori? 2 [~] · Šmihel-Štopriče? 65 [~]) + **★ DUHOVNIŠKA MENJAVA** (Jos. Novak 5/9 DOMINANTA — 1898: Rauy 25/27! + Rauy 2/9 + **1. dokaz Franz STURM Coop. ×2**: v4 + v6 — naslednik Herms 1898!) + **★ OČE KOT PRIČA v ISTEM VPISU** (v3 Nicolaus Željko — ženinov oče!) + **★ CROSS-ENTRY v1→v4** (v4 priča Johann Žibak Štrigžingar = v1 ŽENIN, 4 dni po lastni poroki!) + **★ PRIČA-LINK v6→v9** (Johann Županič ½ gbl Jun+Okt — cf. P127 v8/v13 Županič Krasinec 18 + v1/1900 Krasinec 18!) + **★ KURE/MUC KOMPLEKS** (v3 Barbara Kure h10 == h10 1890 Anna Kure — ISTI oče Marcus ¼, mati Škala/Špala [~ varianta]; priča Johann Muc == h10 1890 ŽENIN! + P92 h61 Muc × Ana Kure 1897!) + **★ ŽURAJEVIČ ×4** (v2 nevesta Barbara + v5 nevesta Maria + v5 priča Michael + v7 mati Maria) + **★ VRANOVIČE? [~ k/v] 5 hiš čez 1898–99** (1898: h4 v3 + h2 v10; 1899: h9 + h27 + h28 — faza-1 »Kranoviče« = K/V Kurrent korekcija!) + **★ PFARRAMT SODRAŽICA** (v8 Tauf- und Ledigkeitsschein 17.8.1899 — rojstni kraj »Herzjet? b. Sodrašič«!) + **★ DISPENS № 2319** (v7 fb. Ord. Laibach 21/4. — consanguinitatis; 1. numerirani redni dispens linije!) + **★ OKLICNI LIST št: 173** (v9 — 1. izrecno poimenovan!) + **★ LAIFSKLAR/LAIFFLER ×5** (v6 ženin+oče · v8 priča Kramarič? · v9 nevesta Grahek Laifflerin + oče Darovic — cf. P127 »Zaiflner ×5–6«: ISTI termin? ODPRTO!) + **★ ŽIBAK-vs-FILAK TENSION** (v1/v4 črkovno Ž+b, a h34 1898 = Nicolaus FILAK + h16 1886 = Ana FILAK oče Mathias! — max-zoom s108/s110 primerjava odprta) + GRIBLJE poroke ×3 = 6 blokov (h34 2. dokaz + h44 1. + h1 1. NAJNIŽJA ŠTEVILKA + h10 3. + h20 2. + h16 3.) + **občinske vrste zglasmic** (pentagon!) + **mreže 1899**: ŽIBAK? ×3 · ŽURAJEVIČ ×4 · SIMEC ×3 · KURE ×2 · MUC ×2 · ŽUPANIČ ×2 · STARAŠINIČ ✓ · ŽUGELJ ✓ · NOVAK ×2 (ženin v4 + priča v2); anomalije ×10; vitals **587 → 593** (+ 6 blokov); bloki 04455 = **70 → 76**; p80 hiše **58 (nespremenjeno — h44/h1 že v vzorci prek mrliške/krstne!)**; PT luknja **12 (nespremenjeno)**; poročna sidra **63 → 69 (+1899:6)**; **P129 LEAD: poročna 1900** (glava »1900.« + v1/1900 Krasinec 18 že na s112; skeni 112–116 v .p126tmp); EXCLUDED: 0; skripta scripts/p128_parish_marriage_1899.py (I1–I11); status SAMPLE-TRANSCRIPTION-M1899",
    "P128: PARISH OF PODZEMELJ — MARRIAGE REGISTER 04455, THE FULL YEAR 1899 (issue #18; SAMPLE-TRANSCRIPTION-M1899; the 14th year of the marriage line P115 = 1886 → … → P128 = 1899): the frame CONFIRMED — s110–s111 == pages 109–110 (page == scan − 1, the **14th confirmation**; valid in 61–110); **THE HANDWRITTEN HEADING »1899.« CONFIRMED on s110** + **the handwritten heading »1900.« CONFIRMED on s112** (double-underlined, under the printed columns — the P129 lead + v1/1900 Feb 12 Krasinec 18 (P129 korekcija! the lead pre-read Jan 2) = the ŽUPANIČ house of P127 v8/v13!); **1899 = 9 entries = the 3rd smallest year of the line (after 1900:8!)** (min 1886:7; −18 after the record 1898:27!) = Jan 3 + Feb 1 + May 1 + Jun 1 + Aug 1 + Sep 1 + Oct 1; **Jan 30 ×2 weddings (v2+v3)**; **9/9 BOTH-SIDES**; **THE BIG P128 NOVELS**: **★ THE OLDEST COUPLE OF THE LINE** (v1: groom Johann Žibak? [~] 66 + bride Maria [Ś/H]rudej? [~] 68 = 134 years, BOTH status 1!) + **★ ¾ SMALLHOLDER = THE NEW HIGHEST FRACTION OF THE LINE** (v7 bride Anna Žugelj ¾ + father Nicolaus Žugelj ¾; previously the highest ½, the lowest ⅛ P127 v23!) + **★ THE 1st GROOM COMPLETELY OUTSIDE THE SYSTEM** (v9 Franc Darovic? [~], Idrišina? 1, the parish St. Michael b. RUDOLFSWERTH = Novo mesto, a servant, 36!) + **★ THE CERTIFICATE PENTAGON: 5 municipalities** (Griblje 2/3/5 · Podzemelj 1/3/4 — no: 4 OUT OF ORDER: dispens Apr 21 → certificate Apr 30 → wedding Aug 5! · Gradac 57 · na Gori? 2 [~] · Šmihel-Štopriče? 65 [~]) + **★ THE PRIEST TURNOVER** (Jos. Novak 5/9 THE DOMINANT — 1898: Rauy 25/27! + Rauy 2/9 + **the 1st proof of Franz STURM Coop. ×2**: v4 + v6 — Herms's 1898 successor!) + **★ THE FATHER AS WITNESS IN THE SAME ENTRY** (v3 Nicolaus Željko — the groom's father!) + **★ THE CROSS-ENTRY v1→v4** (the v4 witness Johann Žibak Štrigžingar = the v1 GROOM, 4 days after his own wedding!) + **★ THE WITNESS LINK v6→v9** (Johann Županič ½ sml Jun+Oct — cf. P127 v8/v13 Županič Krasinec 18 + v1/1900 Krasinec 18!) + **★ THE KURE/MUC COMPLEX** (v3 Barbara Kure h10 == h10 1890 Anna Kure — the SAME father Marcus ¼, mother Škala/Špala [~ a variant]; the witness Johann Muc == the h10 1890 GROOM! + P92 h61 Muc × Ana Kure 1897!) + **★ ŽURAJEVIČ ×4** (v2 bride Barbara + v5 bride Maria + v5 witness Michael + v7 mother Maria) + **★ VRANOVIČE? [~ k/v] 5 houses across 1898–99** (1898: h4 v3 + h2 v10; 1899: h9 + h27 + h28 — the faza-1 »Kranoviče« = a K/V Kurrent correction!) + **★ THE PARISH OFFICE OF SODRAŽICA** (v8 the Tauf- und Ledigkeitsschein Aug 17, 1899 — the birth place »Herzjet? b. Sodrašič«!) + **★ THE DISPENSATION № 2319** (v7 the Fürstbischöfliches Ordinariat Laibach Apr 21 — consanguinitatis; the 1st numbered regular dispensation of the line!) + **★ THE BANNS CERTIFICATE no: 173** (v9 — the 1st explicitly named banns of the line!) + **★ LAIFSKLAR/LAIFFLER ×5** (v6 groom+father · v8 witness Kramarič? · v9 bride Grahek Laifflerin + father Darovic — cf. P127 »Zaiflner ×5–6«: the SAME term? OPEN!) + **★ THE ŽIBAK-vs-FILAK TENSION** (v1/v4 letterform Ž+b, yet h34 1898 = Nicolaus FILAK + h16 1886 = Ana FILAK father Mathias! — a max-zoom s108/s110 comparison open) + GRIBLJE marriages ×3 = 6 blocks (h34 the 2nd evidence + h44 the 1st + h1 the 1st THE LOWEST NUMBER + h10 the 3rd + h20 the 2nd + h16 the 3rd) + **the municipal certificate series** (the pentagon!) + **the 1899 networks**: ŽIBAK? ×3 · ŽURAJEVIČ ×4 · SIMEC ×3 · KURE ×2 · MUC ×2 · ŽUPANIČ ×2 · STARAŠINIČ ✓ · ŽUGELJ ✓ · NOVAK ×2 (the v4 groom + the v2 witness); anomalies ×10; vitals **587 → 593** (+ 6 blocks); the 04455 blocks = **70 → 76**; the p80 houses **58 (unchanged — h44/h1 already in the sample via the death/baptism registers!)**; the PT gap **12 (unchanged)**; the marriage anchors **63 → 69 → 71 (+1899:6, +1900:2)**; **THE P129 LEAD: the marriages of 1900** (the heading »1900.« + v1/1900 Krasinec 18 already on s112; scans 112–116 in .p126tmp); EXCLUDED: 0; the script scripts/p128_parish_marriage_1899.py (I1–I11); status SAMPLE-TRANSCRIPTION-M1899",
    p128Errors.length === 0,
    p128Errors.length === 0
      ? `9 vpisov = 3. najmanjše leto (s110–s111 == Pag. 109–110; Pag. == sken − 1, 14. potrditev!) · **★ NAJSTAREJŠI PAR LINIJE v1 (66+68 = 134, OBA 1. poroka!)** · **★ ¾ griblar v7 (NOVI NAJVIŠJI ulomek — oče+hči Žugelj!)** · **★ 1. ženin izven sistema (v9 Pf. St. Michel b. Rudolfswerth = Novo mesto!)** · **★ zglasmica-pentagon 5 občin (Griblje 2/3/5 · Podzemelj 1/3/4 · Gradac 57 · na Gori? 2 · Šmihel-Štopriče? 65)** · **★ Novak 5/9 dominanta + 1. dokaz Sturm Coop. ×2 (v4+v6)** · **★ cross-entry v1→v4 (ženin Žibak priča!) + oče-kot-priča v3 + priča-link v6→v9 Županič** · **★ KURE/MUC kompleks (v3 == h10 1890!) + ŽURAJEVIČ ×4 + Vranoviče 5 hiš 1898–99** · **★ SODRAŽICA Pfarramt (v8) + dispens № 2319 (v7) + oklicni list št 173 (v9)** · GRIBLJE 3 poroke / 6 blokov (h34+h44+h1+h10+h20+h16) · vitals 595 · bloki 04455 = 78 · p80 hiše 58 · PT luknja 12 · sidra 71 · **P129 LEAD: poročna 1900 (glava + v1/1900 Krasinec 18 že na s112!)**`
      : p128Errors.join("; "),
  );
  }

  // ——— qa-p129: POROČNA KNJIGA 04455 — polno leto 1900 (P129; 15. leto poročne linije) ———
  {
  const p129Errors: string[] = [];
  if (p129Marr.length !== 2)
    p129Errors.push(`bloki 1900 (04455) ≠ 2 (${p129Marr.length} — EDINA GRIBLJE poroka: v2 2 bloka = 2!)`);
  const p129Houses = p129Marr.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
  if (p129Houses.join(",") !== "7,8")
    p129Errors.push(`hiše 1900 ≠ [7,8] — najdeno: ${p129Houses.join(",")} (v2 h7 1. POROČNI DOKAZ Töller? [~] × h8 1. POROČNI DOKAZ Jakobčič? [~] — EDINA GRIBLJE poroka 1900!)`);
  // P129 pini (2 bloka)
  const p129Pins: Array<[string, string]> = [
    ["7", "1. POROČNI DOKAZ h7"], ["7", "TÖLLER"],
    ["8", "1. POROČNI DOKAZ h8"], ["8", "JAKOBČIČ"],
  ];
  for (const [n, pin] of p129Pins) {
    const blk = p129Marr.filter((h) => h.houseNo === n);
    if (blk.length === 0) {
      p129Errors.push(`pin ${n} (${pin}) — hiša ${n} ni med 1900 bloki`);
      continue;
    }
    if (!blk.some((cur) => cur.whatSi.toLowerCase().includes(pin.toLowerCase())))
      p129Errors.push(`pin hiša ${n} (${pin}) manjka`);
  }
  // duhovnik 1900: Rauy 2/2 blokov (GRIBLJE v2) — 1900 celotno: Rauy 8/8 = 100%
  const p129Rauy = p129Marr.filter((h) => h.whatSi.includes("Jos. Rauy")).length;
  if (p129Rauy !== 2)
    p129Errors.push(`Rauy 1900 blokov (GRIBLJE 2) ≠ 2 (${p129Rauy} — 1900 celotno: Rauy 8/8 = 100% dominanta — povratek P127-vzorca!)`);
  // kumulativ: vitals 595 (593 + 2) + bloki 04455 78
  if (HOUSE_VITALS.length !== 685)
    p129Errors.push(`HOUSE_VITALS ≠ 595 (${HOUSE_VITALS.length} — P128: 593; P129: + 2 bloka 1900 = 610!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length !== 168)
    p129Errors.push(`bloki 04455 ≠ 142 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length} — P128: 76; P129: + 2 = …; P132: + 12 blokov 1903; P133: + 8 blokov 1904; P134: + 13 blokov 1905 = 115!)`);
  push(
    "qa-p129-parish-marriage-1900",
    "P129: ŽUPNIJA PODZEMELJ — POROČNA KNJIGA 04455, POLNO LETO 1900 (issue #18; SAMPLE-TRANSCRIPTION-M1900; 15. leto poročne linije P115 = 1886 → … → P129 = 1900): okvir POTRJEN — s112–s113 == Pag. 111–112 (Pag. == sken − 1, **15. potrditev**; velja 61–112); **ROKOPISNA GLAVA »1900.« POTRJENA na s112** (dvopodčrtana) + **rokopisna glava »1901.« POTRJENA na s114** (podčrtana — P130 lead POTRJEN + v1/1901 Jänner 28 Otok 34 Joseph KRIŽAN × Otok 21 Barbara PALČIČ — P130-lead KOREKCIJE ×4 [P130]: Jan 18→28 · Otok 14→34 · Kurjan?→Križan · Pačaj?→Palčič!); **1900 = 8 vpisov = 2. najmanjše leto linije** (min 1886:7; **1899:9 padne na 3.!**) = **Febr 12 ×2 + Febr 19 ×2** + Mai 14 + Okt 22 + **Nov 5 ×2**; **8/8 OBOJESTRANSKO**; **VELIKE NOVELE P129**: **★ ŽUPANIČ KONTINUUM** (v1 ženin Nicolaus Županič ¼ griblar, Krasinec 18 = ISTA HIŠA P127 v8/v13 — **3. poročni dokaz hiše!**; oče Matthias == P127 starševski oče [~]! + v3 priča Johann Županič ½ = **P127 v8 ŽENIN — priča 7 dni po lastni poroki** = cross-entry vzorec P128 v1→v4!) + **★ 3 DVOJNA DNEVA = NOVI REKORD LINIJE** (Febr 12 ×2 + Febr 19 ×2 + Nov 5 ×2; prej 1 — P128 30.1.×2!) + **★ RAUY 8/8 = 100% DOMINANTA** (povratek P127-vzorca 25/27 po P128 Novak 5/9; Novak 1900 = 0!) + **★ 1. NEZAKONSKA NEVESTA LINIJE?** (v7 oče neveste = ČRTA — do zdaj samo nezakonski ŽENINI: P126 v3 + P127 v16!) + **★ KLOSTER vas ×3 hiše v enem letu** (v3 69+40 + v5 76 — nova vas; cf. P127 Kloster 37/43/69/85 [~]!) + **★ GRADAC 18 ×2 ŽENINA + v7 nevesta** (v5 Anton Pezdirec Mai 14 + v8 Josephus Hovačič Nov 5 — vzorec A6 P127 domačija »Nikolaus«; 3 vpisi iste hiše!) + **★ ZGLASMICA-PENTAGON 5 občin** (Podzemelj 1 št:2 · Griblje 1 št:1 · **Gradac 4** št:38/14/106/119 · **Adlešič 1 NOVA** št:1 + župnijski urad oklicni list št:26 · **SVETI-JURZEJ 1 NOVA!** št:26) + **c.k. sodnija Metlika ×3** (v3 2/2. + v7 2/6. + v8 21. avg. — vzorec P126 dvojna sodna!) + **★ SAMSKI LIST IZRECNO** (v8 — od župnega urada Sveti-Jurzej 22. sept. — vzorec P126 v16 Dragatus!) + **★ NADVARSTVENO DOVOLJENJE ×2** (v7+v8 — vzorec P126 v12!) + **★ polnoletnost-dokumenti za nevesto 5/8 vpisov** (v1+v2+v3+v7+v8!) + **★ oče-kot-priča ČEZ vpisa** (v5 priča Georg Pezdirec = v1 oČE neveste! + oče-kot-priča v ISTEM vpisu P128 v3) + **★ PEZDIREC ×4** (v1 nevesta Catharina + oče Georg ×2 [v1-R + v5 priča!] + v5 ženin Anton + oče Peter — mreža 8. leto!) + **»z güblarštofa« ×2** (v5+v7 — vzorec P127 ×3!) + **mreže 1900**: ŽUPANIČ ×3 · PEZDIREC ×4 · MAVRIN ×3 · JAKŠA ×2 · MIHELIČ ×2 · ŽUPEC ×2 · ŠOPČIČ ×2 · GREGORIČ ×2 · NOVAK ×2 · ADLEŠIČ ×2 · KLEPEC; anomalije ×10 (A1 Županič k/v korekcija + A2 datum Febr 12 KOREKCIJA!); vitals **593 → 595** (+ 2 bloka); bloki 04455 = **76 → 78**; p80 hiše **58 (nespremenjena — h7/h8 ne v vzorci!)**; PT luknja **12 (nespremenjena)**; poročna sidra **69 → 71 (+1900:2)**; **P130 LEAD: poročna 1901 IZVEDENA (11 vpisov — 1. leto linije BREZ Griblje! korekcije ×4!) + P131 LEAD KOREKCIJA [P130]: rokopisna glava 1902 ŽE na s116 (ne s117!)** + v4–v6/1902 na s117; EXCLUDED: 0; skripta scripts/p129_parish_marriage_1900.py (I1–I11); status SAMPLE-TRANSCRIPTION-M1900",
    "P129: THE PARISH OF PODZEMELJ — MARRIAGE REGISTER 04455, THE FULL YEAR 1900 (issue #18; SAMPLE-TRANSCRIPTION-M1900; the 15th year of the marriage line P115 = 1886 → … → P129 = 1900): the frame CONFIRMED — s112–s113 == pages 111–112 (page == scan − 1, the **15th confirmation**; valid in 61–112); **THE HANDWRITTEN HEADING »1900.« CONFIRMED on s112** (double-underlined) + **the handwritten heading »1901.« CONFIRMED on s114** (underlined — the P130 lead CONFIRMED + v1/1901 Jan 28 Otok 34 Joseph KRIŽAN × Otok 21 Barbara PALČIČ — the P130-lead corrections ×4 [P130]: Jan 18→28 · Otok 14→34 · Kurjan?→Križan · Pačaj?→Palčič!); **1900 = 8 entries = the 2nd smallest year of the line** (min 1886:7; **1899:9 falls to the 3rd!**) = **Feb 12 ×2 + Feb 19 ×2** + May 14 + Oct 22 + **Nov 5 ×2**; **8/8 BOTH-SIDES**; **THE BIG P129 NOVELS**: **★ THE ŽUPANIČ CONTINUUM** (the v1 groom Nicolaus Županič ¼ sml, Krasinec 18 = the SAME HOUSE as P127 v8/v13 — **the 3rd marriage evidence of the house!**; the father Matthias == the P127 parental father [~]! + the v3 witness Johann Županič ½ = **the P127 v8 GROOM — a witness 7 days after his own wedding** = the cross-entry pattern P128 v1→v4!) + **★ 3 DOUBLE DAYS = THE NEW RECORD OF THE LINE** (Feb 12 ×2 + Feb 19 ×2 + Nov 5 ×2; previously 1 — P128 Jan 30 ×2!) + **★ RAUY 8/8 = THE 100% DOMINANT** (the return of the P127 pattern 25/27 after P128 Novak 5/9; Novak in 1900 = 0!) + **★ THE 1st ILLEGITIMATE BRIDE OF THE LINE?** (the v7 bride's father = a DASH — until now only illegitimate GROOMS: P126 v3 + P127 v16!) + **★ THE KLOSTER VILLAGE ×3 houses in one year** (v3 69+40 + v5 76 — a new village; cf. P127 Kloster 37/43/69/85 [~]!) + **★ GRADAC 18 ×2 GROOMS + the v7 bride** (the v5 groom Anton Pezdirec May 14 + the v8 groom Josephus Hovačič Nov 5 — the A6 pattern P127 homestead »Nikolaus«; 3 entries of the same house!) + **★ THE CERTIFICATE PENTAGON: 5 municipalities** (Podzemelj 1 no:2 · Griblje 1 no:1 · **Gradac 4** no:38/14/106/119 · **Adlešič 1 NEW** no:1 + the parish office banns no:26 · **SVETI-JURZEJ 1 NEW!** no:26) + **the civil court of Metlika ×3** (v3 Feb 2 + v7 Jun 2 + v8 Aug 21 — the P126 double judicial pattern!) + **★ THE CELIBACY CERTIFICATE EXPLICIT** (v8 — from the parish office of Sveti-Jurzej Sep 22 — the P126 v16 Dragatus pattern!) + **★ THE GUARDIANSHIP PERMISSION ×2** (v7+v8 — the P126 v12 pattern!) + **★ the majority documents for the bride in 5/8 entries** (v1+v2+v3+v7+v8!) + **★ THE FATHER-AS-WITNESS ACROSS ENTRIES** (the v5 witness Georg Pezdirec = the v1 BRIDE'S FATHER! + the father-as-witness in the SAME entry P128 v3) + **★ PEZDIREC ×4** (the v1 bride Catharina + father Georg ×2 [v1-R + the v5 witness!] + the v5 groom Anton + father Peter — the 8th year of the network!) + **»z güblarštofa« ×2** (v5+v7 — the P127 ×3 pattern!) + **the 1900 networks**: ŽUPANIČ ×3 · PEZDIREC ×4 · MAVRIN ×3 · JAKŠA ×2 · MIHELIČ ×2 · ŽUPEC ×2 · ŠOPČIČ ×2 · GREGORIČ ×2 · NOVAK ×2 · ADLEŠIČ ×2 · KLEPEC; anomalies ×10 (A1 the Županič k/v correction + A2 the date Feb 12 CORRECTION!); vitals **593 → 595** (+ 2 blocks); the 04455 blocks = **76 → 78**; the p80 houses **58 (unchanged — h7/h8 not in the samples!)**; the PT gap **12 (unchanged)**; the marriage anchors **69 → 71 (+1900:2)**; **THE P130 LEAD: the marriages of 1901 EXECUTED (11 entries — the 1st year of the line WITHOUT Griblje! corrections ×4!) + THE P131 LEAD CORRECTION [P130]: the 1902 handwritten heading already on s116 (not s117!)** + v4–v6/1902 on s117; EXCLUDED: 0; the script scripts/p129_parish_marriage_1900.py (I1–I11); status SAMPLE-TRANSCRIPTION-M1900",
    p129Errors.length === 0,
    p129Errors.length === 0
      ? `8 vpisov = 2. najmanjše leto (s112–s113 == Pag. 111–112; Pag. == sken − 1, 15. potrditev!) · **★ ŽUPANIČ kontinuum (v1 ženin Krasinec 18 = P127 hiša — 3. dokaz! + v3 priča = P127 v8 ženin 7 dni po poroki!)** · **★ 3 dvojna dneva = NOVI REKORD (Febr 12 + Febr 19 + Nov 5)!** · **★ Rauy 8/8 = 100% dominanta (povratek!)** · **★ 1. nezakonska nevesta (v7 oče = črta!)** · **★ Kloster ×3 hiše (69/40/76) + Gradac 18 ×2 ženina + nevesta (A6!)** · **★ pentagon 5 občin (+Adlešič + Sveti-Jurzej NOVA!) + sodnija Metlika ×3 + samski list v8 + nadvarstveno ×2 + polnoletnost 5/8 nevest** · **★ Pezdirec ×4 (8. leto!) + oče-kot-priča čez vpisa (v5 priča = v1 oče!)** · EDINA GRIBLJE poroka (h7+h8 NOVA — 1. dokaza!) · vitals 595 · bloki 04455 = 78 · sidra 71 · **P130 LEAD izveden: poročna 1901 (11 vpisov! 0 Griblje! korekcije ×4) + P131 LEAD korekcija: glava 1902 ŽE na s116**`
      : p129Errors.join("; "),
  );
  }

  // ——— qa-p130: POROČNA KNJIGA 04455 — polno leto 1901 (P130; 16. leto poročne linije) ———
  {
  const p130Errors: string[] = [];
  // 1901 = 0 GRIBLJE blokov — 1. leto poročne linije 1886–1901 BREZ vsake omembe
  // Griblje (0/11 vpisov!) — ASIMETRIJA s krstno 1901 (P96: vsi vpisi Griblje!)
  const p130Marr = HOUSE_VITALS.filter((h) => h.bookSignature === "04455" && h.year === 1901);
  if (p130Marr.length !== 0)
    p130Errors.push(`bloki 1901 (04455) ≠ 0 (${p130Marr.length} — 1. leto poročne linije BREZ vsake omembe Griblje: 0 domicilov/staršev/prič/Weißstandov iz Griblje; ASIMETRIJA s krstno 1901 P96 = vsi Griblje!)`);
  // kumulativ NESPREMENJEN: vitals 595 + bloki 04455 = 78 + sidra 71 (0 novih)
  if (HOUSE_VITALS.length !== 685)
    p130Errors.push(`HOUSE_VITALS ≠ 595 (${HOUSE_VITALS.length} — P130: 0 novih blokov 1901, vse številke NESPREMENJENE!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length !== 168)
    p130Errors.push(`bloki 04455 ≠ 142 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length} — P129: 78; P130: + 0 = …; P132: + 12 blokov 1903; P133: + 8 blokov 1904; P134: + 13 blokov 1905 = 115!)`);
  push(
    "qa-p130-parish-marriage-1901",
    "P130: ŽUPNIJA PODZEMELJ — POROČNA KNJIGA 04455, POLNO LETO 1901 (issue #18; SAMPLE-TRANSCRIPTION-M1901; 16. leto poročne linije P115 = 1886 → … → P130 = 1901; delo PO ENVIRONMENT-RESETU — klon GitHub @ 14b47f5 + inventory rekonstruiran iz matricula-konfiguracije + fetch/crop recept P128/P129): okvir POTRJEN — s114–s116 == Pag. 113–115 (Pag. == sken − 1, **16. potrditev**; velja 61–115); **ROKOPISNA GLAVA »1901.« POTRJENA na s114** (podčrtana; P130-lead KOREKCIJE ×4: Jan 18→28 · Otok 14→34 · Kurjan?→KRIŽAN · Pačaj?→PALČIČ!) + **rokopisna glava »1902.« POTRJENA ŽE na s116** (dvopodčrtana — **P131-lead KOREKCIJA**: P129-lead pričakoval veliko tiskano glavo na s117; s117 = nadaljevanje v4–v6 brez glave!); **1901 = 11 vpisov = 4. najmanjše leto linije** (min 1886:7 → 1900:8 → 1899:9 → 1901:11) = Jan 28 + Feb 4 + ★ **FEBR 11 ×6 = MASA!** (v3–v8 — vsi zoom-potrjeni!) + Jul 29 + Nov 4+11; **11/11 OBOJESTRANSKO**; **VELIKE NOVELE P130**: **★ 6 POROK NA 11.2.1901 = 2. največji dan linije** (rekord 1893: 7 na 6.2. — P122; 3× P129-rekord 2/dan; od 1894 NOVI REKORD!) + **★ RAUY 11/11 = 100% ABSOLUTNI REKORD DOMINANCE** (P129 8/8; P128 Novak 5/9; karierna linija Rauy ≈ 49/55!) + **★ 0 OMEMB GRIBLJE = 1. leto linije 1886–1901 BREZ Griblje** (0/11 — ASIMETRIJA s krstno 1901 P96 = vsi Griblje!) → **0 NOVIH BLOKOV** (vitals 595 · bloki 04455 = 78 · sidra 71 · p80 hiše 58 · PT luknja 12 — VSE NESPREMENJENE!) + **★ ¾ GRIBLAR 2. DOKAZ** (v7 oče Ignac Prevec + hči Engelbetha, Primostek 1 — vzorec P128 v7 Žugelj!) + **★ 1. DISPENS AFINOSTI LINIJE** (v1 Anverwandtschaft 2. dum? № 138? fb. Ord. Laibach ddo 15/1. — 9 dni pred poroko; do zdaj samo consanguinitas!) + v8 consanguinitas 4. kolena (dotikajoč 3.) **št 236** 22.1. + robno **POTESTATE DELEGATA** (1. latinski robni zapis?) + **★ POLNOLETNOST ZA ŽENINA** (v4: 21! priznanje Metlika IV 218/89 + 9.6.1900 b 41/98 + deželna vlada št 1786 — prej samo za neveste!; v11: **ZA OBA** — ženin 23 + nevesta 21!) + **★ MUC ×3** (v8 nevesta Anna + v11 nevesta Maria + v11 Weißstand Johan Muc == P128 v3 PRIČA = h10-1890-ŽENIN — 3. vloga!) + **★ VRANOVIČE 8 = 6. hiša vasi** (1898 h4+h2 · 1899 h9+h27+h28 · 1901 h8 — K/V-korekcija faza-1 potrjena!) + **★ 1. ČINOVNIKI/OBRTNIKI-PRIČE** (v7 Weißstand Theodulair? Lejihař **c.k. poštni asistent** + robno **Janko Bartle, arhivar in protokolist [nad]škof.? pisarne v Za[g]reba?** = 1. tuje-mestni arhivist! + Schmiedmeister ×2 v2+v10 ISTI Anton Palčič?) + **★ NOVE VASI?** (Primostek ×2 · Cerkvišče ×2 · Zastava · Dobraviče? · Borit? · Hast? · Grišiče? — vsaj 4–6 novih; Metlika 7. dokaz [~]) + **★ Krasinec 3 hiše** (18 P129 + 19 + 23!) + **Rosetta EKSPlicitna ×2** (v3 »½ gbl. Sohn« + »½ gbl. Tochter« — prvi par z obema formama! dolge termine [~ küblastofsju/Küblwirthschaft/nüblonštbaftsont] le še 1901-specifični [~]) + **zglasnice: trikotnik 3 občin** (Podzemelj 6 št 1/3/5/9/2?/4 · Gradac 4 št 34/45/20/210 · mestna Metlika 1 št 180) + **mj.-dokumenti 7/11** (v1 sodna polnoletnost 1897 — 4 leta vnaprej!; v5 očetovo PISMENO 29.1.; v8 ustno OBEH očetov; v10 »und mündlich väterlich Einwilligung« — 1. nemška formula!) + **starosti** (ženin 21–36 · nevesta 18–34 · par 34×34 v6 · 8/11 ženinov < 24!) + **mreže 1901**: Muc ×3 · Palčič ×3 · Jurajevič ×3 · Križan ×2 · Žimec ×2 · Jakša ×2 · Novačič ×2 · Perdinec ×2 · Novak ×2 · Klepec ×2 · Kambič ×2 · Marentič ×2 + **čez-faze**: Jakljevič (1898 ženin → 1901 Weißstand!) · Štrucelj (1900 mati → 1901 mati!) · Kambič (1893 → 1901) · Simonič (1893+1900 → 1901) · Hočevar (1898 → 1901) · Žugelj (P128 ¾ → v8 mati Barbara!) · Perdinec (P128 → v8!); anomalije ×11 (A1 lead-korekcije ×4 + A2 glava-1902-s116 + A3 v9 zglasnica mesec [~] + A8 v11 polnoletnost brez dneva!); vitals **595 (nespremenjen)**; bloki 04455 = **78 (nespremenjen)**; p80 hiše **58 (nespremenjena)**; PT luknja **12 (nespremenjena)**; poročna sidra **71 (nespremenjena — 1901:0!)**; **P131 LEAD: poročna 1902** (glava ŽE na s116 + v1–v3 tam + v4–v6 na s117; točno 6 vpisov [P131: izvedeno — NAJMANJŠE leto linije!]; v2 GRIBLJE 5 × Griblje 31 [P131 korekcija: [G]pbyke? je bilo GRIBLJE 5!] + v4 Griblje 30 × Griblje 24 = 2 DRUBEL-GRIBLJE poroki POTRJENE!); EXCLUDED: 0; skripta scripts/p130_parish_marriage_1901.py (I1–I11); status SAMPLE-TRANSCRIPTION-M1901",
    "P130: THE PARISH OF PODZEMELJ — MARRIAGE REGISTER 04455, THE FULL YEAR 1901 (issue #18; SAMPLE-TRANSCRIPTION-M1901; the 16th year of the marriage line P115 = 1886 → … → P130 = 1901; work AFTER the ENVIRONMENT-RESET — clone GitHub @ 14b47f5 + inventory reconstructed from the matricula config + the fetch/crop recipe P128/P129): the frame CONFIRMED — s114–s116 == pages 113–115 (page == scan − 1, the **16th confirmation**; valid 61–115); **THE HANDWRITTEN HEADING »1901.« CONFIRMED on s114** (underlined; the P130-lead CORRECTIONS ×4: Jan 18→28 · Otok 14→34 · Kurjan?→KRIŽAN · Pačaj?→PALČIČ!) + **the handwritten heading »1902.« CONFIRMED ALREADY on s116** (double-underlined — **THE P131-lead CORRECTION**: the P129-lead expected the large printed heading on s117; s117 = the continuation v4–v6 without a heading!); **1901 = 11 entries = the 4th smallest year of the line** (min 1886:7 → 1900:8 → 1899:9 → 1901:11) = Jan 28 + Feb 4 + ★ **FEB 11 ×6 = THE MASS!** (v3–v8 — all zoom-confirmed!) + Jul 29 + Nov 4+11; **11/11 BOTH-SIDES**; **THE BIG P130 NOVELS**: **★ 6 WEDDINGS ON FEB 11 = the 2nd biggest day of the line** (the record 1893: 7 on Feb 6 — P122; 3× the P129 record!) + **★ RAUY 11/11 = 100% THE ABSOLUTE RECORD OF DOMINANCE** (P129 8/8; P128 Novak 5/9; the career line Rauy ≈ 49/55!) + **★ 0 MENTIONS OF GRIBLJE = the 1st year of the line 1886–1901 WITHOUT Griblje** (0/11 — THE ASYMMETRY with the baptisms 1901 P96 = all Griblje!) → **0 NEW BLOCKS** (vitals 595 · the 04455 blocks = 78 · anchors 71 · p80 houses 58 · PT gap 12 — ALL UNCHANGED!) + **★ THE ¾ SMALLHOLDER 2nd EVIDENCE** (the v7 father Ignac Prevec + daughter Engelbetha, Primostek 1 — the P128 v7 Žugelj pattern!) + **★ THE 1st AFFINITY DISPENS OF THE LINE** (v1 Anverwandtschaft 2nd dum? № 138? Laibach Feb 15/1. — 9 days before the wedding; so far only consanguinity!) + v8 consanguinity 4th degree (touching 3rd) **№ 236** Jan 22 + marginally **POTESTATE DELEGATA** + **★ THE MAJORITY FOR THE GROOM** (v4: 21! Metlika IV 218/89 + Jun 9 1900 b 41/98 + the provincial government № 1786 — so far only for brides!; v11: **FOR BOTH**) + **★ MUC ×3** (v8 bride Anna + v11 bride Maria + v11 Weißstand Johan Muc == the P128 v3 WITNESS — the 3rd role!) + **★ VRANOVIČE 8 = the 6th house of the village** + **★ THE 1st OFFICIALS/CRAFTSMEN-WITNESSES** (c.k. postal assistant + the Zagreb archivist-protocolist marginally! + Schmiedmeister ×2) + **★ NEW VILLAGES?** (Primostek ×2 · Cerkvišče ×2 · Zastava · Dobraviče? · Borit? · Hast? · Grišiče?) + **★ Krasinec 3 houses** (18 + 19 + 23!) + **the EXPLICIT Rosetta ×2** (v3 »½ gbl. Sohn« + »½ gbl. Tochter«!) + **the certificates: the triangle 3 communes** + **the minority documents 7/11** + **the networks**: Muc ×3 · Palčič ×3 · Jurajevič ×3 · Križan ×2 · Žimec ×2 · Jakša ×2 + **the cross-phases**: Jakljevič (1898→1901!) · Štrucelj (1900→1901!) · Žugelj (P128 ¾ → v8 mother Barbara!) · Perdinec (P128 → v8!); anomalies ×11; vitals **595 (unchanged)**; the 04455 blocks = **78 (unchanged)**; the p80 houses **58 (unchanged)**; the PT gap **12 (unchanged)**; the marriage anchors **71 (unchanged — 1901:0!)**; **THE P131 LEAD: the marriages of 1902** (the heading ALREADY on s116 + v1–v3 there + v4–v6 on s117; exactly 6 entries [P131: executed — the SMALLEST year of the line!]; v2 GRIBLJE 5 × Griblje 31 [the P131 correction: [G]pbyke? was GRIBLJE 5!] + v4 Griblje 30 × Griblje 24 = 2 DOUBLE-GRIBLJE weddings CONFIRMED!); EXCLUDED: 0; the script scripts/p130_parish_marriage_1901.py (I1–I11); status SAMPLE-TRANSCRIPTION-M1901",
    p130Errors.length === 0,
    p130Errors.length === 0
      ? `11 vpisov = 4. najmanjše leto (s114–s116 == Pag. 113–115; Pag. == sken − 1, 16. potrditev!) · **★ 6 POROK NA 11.2.1901 = MASA (v3–v8; 2. največji dan — rekord 1893:7!)** · **★ Rauy 11/11 = 100% ABSOLUTNI REKORD!** · **★ 0 OMEMB GRIBLJE = 1. leto linije brez Griblje (ASIMETRIJA s krstno P96!) → 0 novih blokov (vitals 595 · bloki 78 · sidra 71 · p80 58 · PT 12 vse nespremenjene!)** · **★ ¾ griblar 2. dokaz (v7 Prevec oče+hči == P128 v7 vzorec!)** · **★ 1. dispens AFINOSTI (v1 Anverwandtschaft № 138?!) + consang. 4. kolena št 236 + potestate delegata (v8)** · **★ polnoletnost za ŽENINA (v4 21! + v11 OBA)** · **★ Muc ×3 (P128 priča == v11 Weißstand!) + Vranoviče 8 = 6. hiša + činovniki-priče (poštni asistent + zagrebški arhivar!) + nove vasi? (Primostek/Cerkvišče/Zastava/Dobraviče?/Borit?/Hast?/Grišiče?) + Krasinec 3 hiše + Rosetta eksplicitna ×2 (v3!)** · mreže: Palčič ×3 · Jurajevič ×3 · Križan/Žimec/Jakša/Novačič ×2 + čez-faze Jakljevič/Štrucelj/Kambič/Simonič/Hočevar · **P131 LEAD: poročna 1902 (glava ŽE s116 — korekcija!; v2+v4 DRUBEL-GRIBLJE že vidni!)**`
      : p130Errors.join("; "),
  );
  }

  // ——— qa-p131: POROČNA KNJIGA 04455 — polno leto 1902 (P131; 17. leto poročne linije) ———
  {
  const p131Errors: string[] = [];
  // 1902 = 2 GRIBLJE poroki / 4 bloki (h5+h31 1. dokaza DRUBEL + h30 3. + h24 2. DRUBEL)
  if (p131Marr.length !== 4)
    p131Errors.push(`bloki 1902 (04455) ≠ 4 (${p131Marr.length} — 2 poroki: v2 2 + v4 2 = 4!)`);
  const p131Houses = p131Marr.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
  if (p131Houses.join(",") !== "5,24,30,31")
    p131Errors.push(`hiše 1902 ≠ [5,24,30,31] — najdeno: ${p131Houses.join(",")} (v2 h5 1. POROČNI DOKAZ × h31 1. POROČNI DOKAZ = DRUBEL; v4 h30 3. dokaz × h24 2. dokaz = DRUBEL!)`);
  // P131 pini (4 bloki)
  const p131Pins: Array<[string, string]> = [
    ["5", "1. POROČNI DOKAZ h5"], ["5", "ŠTRUPEC"],
    ["31", "1. POROČNI DOKAZ h31"], ["31", "MULH"],
    ["30", "3. POROČNI DOKAZ"], ["30", "LEGINA"],
    ["24", "2. poročni dokaz h24"], ["24", "BRIŠEC"],
  ];
  for (const [n, pin] of p131Pins) {
    const blk = p131Marr.filter((h) => h.houseNo === n);
    if (blk.length === 0) {
      p131Errors.push(`pin ${n} (${pin}) — hiša ${n} ni med 1902 bloki`);
      continue;
    }
    if (!blk.some((cur) => cur.whatSi.toLowerCase().includes(pin.toLowerCase())))
      p131Errors.push(`pin hiša ${n} (${pin}) manjka`);
  }
  // duhovnik 1902: Rauy 4/4 GRIBLJE blokov (2 poroki × 2 bloka; celotno leto: Rauy 5/6 + Dostál kaplan 1/6 v5!)
  const p131Rauy = p131Marr.filter((h) => h.whatSi.includes("Jos. Rauy")).length;
  if (p131Rauy !== 4)
    p131Errors.push(`Rauy 1902 blokov (GRIBLJE 4) ≠ 4 (${p131Rauy} — 1902 celotno: Rauy 5/6 + ★ 1. DOSTÁL kaplan v5 = 2. duhovniška menjava v letu!)`);
  // kumulativ: vitals 611 (595 + 4 1902 + 12 1903) + bloki 04455 94 + sidra 87
  if (HOUSE_VITALS.length !== 685)
    p131Errors.push(`HOUSE_VITALS ≠ 632 (${HOUSE_VITALS.length} — P131: 599; P132: + 12 = 611; P133: + 8 = 619; P134: + 13 = 632!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length !== 168)
    p131Errors.push(`bloki 04455 ≠ 142 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length} — P130: 78; P131: + 4 = 82; P132: + 12 = 94!)`);
  push(
    "qa-p131-parish-marriage-1902",
    "P131: ŽUPNIJA PODZEMELJ — POROČNA KNJIGA 04455, POLNO LETO 1902 (issue #18; SAMPLE-TRANSCRIPTION-M1902; 17. leto poročne linije P115 = 1886 → … → P131 = 1902): okvir POTRJEN — s116–s117 == Pag. 115–116 (Pag. == sken − 1, **17. potrditev**; velja 61–116); **ROKOPISNA GLAVA »1902.« POTRJENA na s116** (dvopodčrtana — že P130-lead!) + **glava »1903.« POTRJENA na s118** (r1 = 1903 Febr 3 Dragatuš? 1 × **GRIBLJE 11** Agnes Žunjič? [~] = **P132 LEAD — 3. GRIBLJE poroka v vrsti!**; P129-lead napaka »April 15« za v6 KOREKCIJA → **Sept 15**; P131-lead KOREKCIJA: **[G]pbyke? → GRIBLJE 5**!); **1902 = 6 vpisov = NAJMANJŠE LETO POROČNE LINIJE 1886–1902** (prej min 1900:8 po skupnih vpisih / 1886:7 po okvirni konvenciji — 6 < 7 < 8 = NOVI MINIMUM V OBEH MERAH!) = **Jänner 27 ×3** (v1–v3 triplo-datum!) + Mai 12 + Mai 26 + Sept 15; **6/6 OBOJESTRANSKO**; **VELIKE NOVELE P131**: **★ 2 GRIBLJE poroki / 4 poročna bloka** (v2 **h5 1. POROČNI DOKAZ × h31 1. POROČNI DOKAZ = DRUBEL** + v4 **h30 3. dokaz [1889 P118 + 1892 P121] × h24 2. dokaz [1895 P124] = DRUBEL** — 3. leto z ≥2 drubel!) → **vitals 595 → 599; bloki 04455 78 → 82; sidra 71 → 75 (+1902:4); p80 hiše 58 + PT luknja 12 NESPREMENJENA (h5/h24/h30/h31 že v vzorci!)** + **★ 1. DOSTÁL kaplan** (Hanislav Dostál, kaplan — v5; 1. nov duhovnik od P128-Sturm; Rauy 5/6) + **★ 1. IZRECNA NEZAKONSKA-OPOMBA** (v6 ženin Thomas Černe: oče = črta + mati Ursula Černe »lediga? Ehe.« [~] — 3. nezakonski ženin linije, 1. z opombo!) + **★ 2 IZVEN-župnije vpisa v enem** (v6 ženin Črnomelj 134 mesto + nevesta Bukoraj? pf. Črnomelj 1 = NOVA VAS? + očina PLANINA št: 10 NOVA!) + **★ priče činovniki** (v6: Eugen Sorbea? [~] »12 R. Leu. Bor'zd. off'Anwt.« [~] vojak + Johann Peterly? [~] »k.k. Bahndienst« [~] železniški — vzorec P130!) + **★ ŽENITOVANJSKA ZGLAŠNICA = REŠITEV SERIJSKE FORMULE** (prej »Porifovanjška/žerifovanjška« [~] P128–P130 → nem. Trauungs-Anzeige!) + **★ ŠTRUPEC NOVI PRIIMEK ×3** (v2 ženin Mathias + oče Johann + v6 nevestina mati Maria Strupec!) + **★ LEGINA NOVI ×3** (v4 ženin Nicolaus 43 najstarejši! + oče Johann + priča Georg) + **★ KOCJAN NOVI** (v6 nevesta Margareth 35 + oče Peter ¼ griblar IZVEN Griblje!) + nadvarstveno dovoljenje ×3 (v4 c.k. okr. sodišče Črnomelj 1. maja P62/99 18. [~] + v5 okrajno sodišče Metlika 13. maja za ml. nevesto!) + NOVI poklici/statusi: Wagnermeister (v3) · Fabriksarbeiter (v3 oče) · Besitzer (v6) · ¼ Grafskant? [~] (v6) + **mreže 1902**: PEZDIREC ×3 (7. leto — povratek po 1901!) · DRAGOŠ ×1 (10.+ leto 1886–1902!) · MUC ×3 (v1 Terezia + v3 priča Johann == P128 v3 priča + v5 mati Maria) · ŽUPANIČ (4. leto — v3 mati!) · KLEPEC 16.+ · BRODARIČ 14.+ · ŠKALA 4. · ČERNE 3. · KRALJ 7.+ · STRAVS 3. · TOMC 3.+ (P132-lead Barbara Tomc!) + zglasnice: občine Griblje ×2 (26/1. št: 23 + 17.5. štev: 2) · očine Podzemelj 27/1. štev: 48 + 13.5. · očine Gradac 27/1. štev: 4 · očine Planina 5.9. št: 10; anomalije ×6 (A1 [G]pbyke korekcija + A2 v6 datum korekcija + A3 v6 ~-znak + A4 v4 && uml. rovetja [~] + A5 v6 priče/tail [~] + A6 podpis »za odlega. himoim.« [~]); vitals **595 → 599** (+ 4 bloka); bloki 04455 = **78 → 82**; p80 hiše **58 (nespremenjena)**; PT luknja **12 (nespremenjena)**; poročna sidra **71 → 75 (+1902:4)**; **P132 LEAD: poročna 1903** (glava »1903.« na s118 + v1 Febr 3 Dragatuš? 1 × GRIBLJE 11 Agnes Žunjič? [~] — 3. Griblje poroka v vrsti!; s118 v2–v5: Febr 9 ×3 + Febr 16; min 5 vpisov s118–s119; skeni 117–120 v .p126tmp); EXCLUDED: 0; skripta scripts/p131_parish_marriage_1902.py (I1–I11); status SAMPLE-TRANSCRIPTION-M1902",
    "P131: THE PARISH OF PODZEMELJ — MARRIAGE REGISTER 04455, THE FULL YEAR 1902 (issue #18; SAMPLE-TRANSCRIPTION-M1902; the 17th year of the marriage line P115 = 1886 → … → P131 = 1902): the frame CONFIRMED — s116–s117 == pages 115–116 (page == scan − 1, the **17th confirmation**; valid 61–116); **THE HANDWRITTEN HEADING »1902.« CONFIRMED on s116** (double-underlined — already the P130-lead!) + **the heading »1903.« CONFIRMED on s118** (r1 = 1903 Feb 3 Dragatuš? 1 × **GRIBLJE 11** Agnes Žunjič? [~] = **THE P132 LEAD — the 3rd GRIBLJE wedding in a row!**; the P129-lead error »April 15« for v6 CORRECTED → **Sept 15**; the P131-lead CORRECTION: **[G]pbyke? → GRIBLJE 5**!); **1902 = 6 entries = THE SMALLEST YEAR OF THE MARRIAGE LINE 1886–1902** (previously min 1900:8 by total entries / 1886:7 by the frame convention — 6 < 7 < 8 = the NEW MINIMUM IN BOTH MEASURES!) = **Jan 27 ×3** (v1–v3 the triple date!) + May 12 + May 26 + Sept 15; **6/6 BOTH-SIDES**; **THE BIG P131 NOVELS**: **★ 2 GRIBLJE weddings / 4 marriage blocks** (v2 **h5 the 1st MARRIAGE EVIDENCE × h31 the 1st MARRIAGE EVIDENCE = DOUBLE** + v4 **h30 the 3rd evidence [1889 P118 + 1892 P121] × h24 the 2nd evidence [1895 P124] = DOUBLE** — the 3rd year with ≥2 doubles!) → **vitals 595 → 599; the 04455 blocks 78 → 82; anchors 71 → 75 (+1902:4); p80 houses 58 + the PT gap 12 UNCHANGED (h5/h24/h30/h31 already in the samples!)** + **★ the 1st DOSTÁL chaplain** (Hanislav Dostál, kaplan — v5; the 1st new priest since P128-Sturm; Rauy 5/6) + **★ the 1st EXPLICIT ILLEGITIMACY NOTE** (the v6 groom Thomas Černe: father = a dash + mother Ursula Černe »lediga? Ehe.« [~] — the 3rd illegitimate groom of the line, the 1st with a note!) + **★ 2 OUTSIDE-parish entries in one** (the v6 groom Črnomelj 134 town + the bride Bukoraj? pf. Črnomelj 1 = A NEW VILLAGE? + the očina PLANINA no: 10 NEW!) + **★ official witnesses** (v6: Eugen Sorbea? [~] »12 R. Leu. Bor'zd. off'Anwt.« [~] military + Johann Peterly? [~] »k.k. Bahndienst« [~] railway — the P130 pattern!) + **★ ŽENITOVANJSKA ZGLAŠNICA = THE SOLUTION OF THE SERIES FORMULA** (previously »Porifovanjška/žerifovanjška« [~] P128–P130 → German Trauungs-Anzeige!) + **★ ŠTRUPEC = A NEW SURNAME ×3** (the v2 groom Mathias + father Johann + the v6 bride's mother Maria Strupec!) + **★ LEGINA NEW ×3** (the v4 groom Nicolaus 43 the oldest! + father Johann + witness Georg) + **★ KOCJAN NEW** (the v6 bride Margareth 35 + father Peter ¼ smallholder OUTSIDE Griblje!) + the guardianship permissions ×3 (v4 the c.k. district court Črnomelj May 1 P62/99 18. [~] + v5 the district court Metlika May 13 for the minor bride!) + NEW occupations/statuses: Wagnermeister (v3) · Fabriksarbeiter (v3 father) · Besitzer (v6) · ¼ Grafskant? [~] (v6) + **the 1902 networks**: PEZDIREC ×3 (the 7th year — the return after 1901!) · DRAGOŠ ×1 (the 10th+ year 1886–1902!) · MUC ×3 · ŽUPANIČ (the 4th year — the v3 mother!) · KLEPEC 16th+ · BRODARIČ 14th+ · ŠKALA 4th · ČERNE 3rd · KRALJ 7th+ · STRAVS 3rd · TOMC 3rd+ (the P132-lead Barbara Tomc!) + the certificates: the Griblje commune ×2 (Jan 26 no: 23 + May 17 no: 2) · the Podzemelj očina Jan 27 no: 48 + May 13 · the Gradac očina Jan 27 no: 4 · the Planina očina Sep 5 no: 10; anomalies ×6; vitals **595 → 599** (+ 4 blocks); the 04455 blocks = **78 → 82**; the p80 houses **58 (unchanged)**; the PT gap **12 (unchanged)**; the marriage anchors **71 → 75 (+1902:4)**; **THE P132 LEAD: the marriages of 1903** (the heading »1903.« on s118 + v1 Feb 3 Dragatuš? 1 × GRIBLJE 11 Agnes Žunjič? [~] — the 3rd Griblje wedding in a row!; s118 v2–v5: Feb 9 ×3 + Feb 16; min 5 entries s118–s119; scans 117–120 in .p126tmp); EXCLUDED: 0; the script scripts/p131_parish_marriage_1902.py (I1–I11); status SAMPLE-TRANSCRIPTION-M1902",
    p131Errors.length === 0,
    p131Errors.length === 0
      ? `6 vpisov = NAJMANJŠE leto linije 1886–1902 (s116–s117 == Pag. 115–116; Pag. == sken − 1, 17. potrditev!) · **★ 2 GRIBLJE poroki / 4 bloki (h5+h31 1. POROČNA DOKAZA DRUBEL + h30 3. × h24 2. DRUBEL!) → vitals 599 · bloki 82 · sidra 75** · **★ Jänner 27 ×3 triplo-datum (v1–v3)** · **★ 1. DOSTÁL kaplan (v5 — 1. nov duhovnik od P128!) + Rauy 5/6** · **★ 1. izrecna nezakonska-opomba (v6 oče = črta + »lediga? Ehe.«!)** · **★ Bukoraj? pf. Črnomelj NOVA VAS? + očina Planina št: 10 + priče činovniki (vojak + k.k. Bahndienst!)** · **★ ženitovanjska zglašnica = rešitev serijske formule!** · **★ ŠTRUPEC NOVI ×3 + LEGINA NOVI ×3 + KOCJAN NOVI + Pezdirec ×3 povratek (7. leto!) + Dragoš 10.+ leto + Muc ×3 + Županič 4. leto** · nadvarstveno ×3 · Wagnermeister/Fabriksarbeiter/Besitzer/Grafskant? NOVI statusi · **P132 LEAD: poročna 1903 (glava s118; v1 Febr 3 × GRIBLJE 11 — 3. Griblje poroka v vrsti!)**`
      : p131Errors.join("; "),
  );
  }

  // ——— qa-p132: POROČNA KNJIGA 04455 — polno leto 1903 (P132; 18. leto poročne linije) ———
  {
  const p132Errors: string[] = [];
  // 1903 = 7 GRIBLJE poroki / 11 blokov
  if (p132Marr.length !== 12)
    p132Errors.push(`bloki 1903 (04455) ≠ 12 (${p132Marr.length} — 8 poroki: v1 1 + v3 2 + v9 1 + v11 1 + v12 2 + v14 1 + v17 2 + v20 2 = 12!)`);
  const p132Houses = p132Marr.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
  if (p132Houses.join(",") !== "6,9,11,11,20,41,44,46,48,50,56,65")
    p132Errors.push(`hiše 1903 ≠ [6,9,11,11,20,41,44,46,48,50,56,65] — najdeno: ${p132Houses.join(",")}`);
  // P132 pini (11 blokov)
  const p132Pins: Array<[string, string]> = [
    ["11", "1. POROČNI DOKAZ h11"], ["11", "ŽUNIČ"],
    ["65", "1. POROČNI DOKAZ h65"], ["65", "MÜCK"],
    ["41", "1. POROČNI DOKAZ h41"], ["41", "HUESTIČ"],
    ["46", "2. poročni dokaz h46"], ["46", "KRIŽAN"],
    ["9", "1. POROČNI DOKAZ h9"], ["9", "JAKOFČIČ"],
    ["6", "1. POROČNI DOKAZ h6"], ["6", "JAKOBČIČ"],
    ["20", "1. POROČNI DOKAZ h20"], ["20", "PEZDIREC"],
    ["48", "1. POROČNI DOKAZ h48"], ["48", "BERKOPREC"],
    ["50", "1. POROČNI DOKAZ h50"], ["50", "JERČINOVIČ"],
    ["44", "2. poročni dokaz h44"], ["44", "ŠTRUCELJ"],
  ];
  for (const [n, pin] of p132Pins) {
    const blk = p132Marr.filter((h) => h.houseNo === n);
    if (blk.length === 0) {
      p132Errors.push(`pin ${n} (${pin}) — hiša ${n} ni med 1903 bloki`);
      continue;
    }
    if (!blk.some((cur) => cur.whatSi.toLowerCase().includes(pin.toLowerCase())))
      p132Errors.push(`pin hiša ${n} (${pin}) manjka`);
  }
  // duhovnik 1903: Rauy na vseh GRIBLJE blokih (11; celotno leto Rauy 19/20 + Dostál 1/20 v18!)
  const p132Rauy = p132Marr.filter((h) => h.whatSi.includes("Jos. Rauy")).length;
  if (p132Rauy !== 12)
    p132Errors.push(`Rauy 1903 blokov (GRIBLJE 12) ≠ 12 (${p132Rauy} — 1903 celotno: Rauy 19/20 + Dostál kaplan 1/20 v18 = 2. dokaz!)`);
  // kumulativ: vitals 610 (599 + 11) + bloki 04455 93 + sidra 86
  if (HOUSE_VITALS.length !== 685)
    p132Errors.push(`HOUSE_VITALS ≠ 619 (${HOUSE_VITALS.length} — P131: 599; P132: + 12 blokov 1903 = 611!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length !== 168)
    p132Errors.push(`bloki 04455 ≠ 142 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length} — P131: 82; P132: + 11 = …; P132: + 12 blokov 1903; P133: + 8 blokov 1904; P134: + 13 blokov 1905 = 115!)`);
  push(
    "qa-p132-parish-marriage-1903",
    "P132: ŽUPNIJA PODZEMELJ — POROČNA KNJIGA 04455, POLNO LETO 1903 (issue #18; SAMPLE-TRANSCRIPTION-M1903; 18. leto poročne linije P115 = 1886 → … → P132 = 1903): okvir POTRJEN — s118–s121 == Pag. 117–120 (Pag. == sken − 1, **18. potrditev**; velja 61–120); **ROKOPISNA GLAVA »1903.« POTRJENA na s118** + **VELIKA TISKANA GLAVA »1904.« POTRJENA na s122** (P133 LEAD: v1–v5 = **Febr 8 ×5 = MASA!**; v2 Griblje 41 Georg Perdinec? [~] + v5 Griblje 30 × Griblje 32 Šimec × Šimec DRUBEL že vidni!); **P132-lead KOREKCIJA: »min 5 vpisov s118–s119« → 20 vpisov s118–s121 (4× podcenjeno — največja lead-napaka linije!)** + nevesta »Žunjič?« → ŽUNIČ [~ Žumič] + Dragatuš? → Dragoše [~] + P131-lead Barbara Tomc POTRJEN (v5); **1903 = 20 vpisov OBOJESTRANSKO** = Febr 3 + Febr 9 ×3 + Febr 16 ×4 + Febr 23 ×2 (**v9/v10 »März«-prevarda ZAVRNJENA z zoomom 8× — ponedeljkovski vzorec!**) + Jun 7 + Jun 22 ×2 + Jul 6 + Jul 27 + Avg 3 + Avg 17 + Sept 13 + Okt 12 + Nov 23; **VELIKE NOVELE P132**: **★ 8 GRIBLJE porok / 12 poročnih blokov** (v1 h11 1. POROČNI DOKAZ + v3 h65 1. × h41 1. DRUBEL + v9 h46 2. dokaz [P127!] + v11 h56 1. dokaz [DVOJNI DISPENS!] + v12 h11 2. blok [2. poroka hiše v ENELETU!] × h9 1. DRUBEL + v14 h6 1. [NAJNIŽJA št.!] + v17 h20 1. × h48 1. DRUBEL + v20 h50 1. × h44 2. [P127!] DRUBEL) → **vitals 599 → 611; bloki 04455 82 → 94; sidra 75 → 87 (+1903:12); p80 hiše 58 + PT luknja 12 NESPREMENJENA** + **★ v11 DVOJNI DISPENS 1. STOPNJE SCHWÄGERSCHAFT** (fb. Ordinariat Laibach ddo 3/6. št: 2244 + k. k. Landesregierung ddo 27/2. št: 4444 — NAJBLIŽJA stopnja + 2. DISPENS AFINOSTI linije; linijski rekord dispensev!) + **★ ¾ GRIBLAR NOVI NAJVIŠJI ULOMEK** (v16 Kozjan Božakovo 43 oče+ženin — prej ½!) + **★ CROSS-ENTRY ×4** (v1-ženin Adamič priča v12 · v1-priča Georg Žunič priča v12 · v11-ženin Georg Kralj priča v17 · v13-ženin Butala priča v19 — vzorec P128 v1→v4!) + **★ BRAT-SESTRA ×2** (v12 ženin Johann Žunič = brat v1-neveste Agnes — h11 2 poroki v letu! · v19 ženin Josef Kambič = brat v13-neveste Maria — Vranoviče 10!) + **★ 4. NEZAKONSKI ženin** (v18 Rudolf Mische — oče ni vpisan + »Zimmermann, geb: ?e« [~]) + **★ 1. HÄUSLERIN** (v18 Francisca Adamič) + **★ NOVE VASI/FARE**: Božakovo 43 pf. Metlika · Sodji vrh 11 pf. SEMIČ · Boginja vas 14 · Bilonje? 32 · Mavhe? 10 · občina LOKA · Zastava 8+9 · Grišiče? 35 · Vranoviče 10+27+29 + **★ oklicni list ×5** (v2 Semič + v6 Črnomelj + v16 Metlika + v20 Štrivnik? [~]) + **deželna vlada ×2** (v6 dovoljenje št: 3254 + v11 dispens št: 4444!) + **★ status-vaha**: güblar/griblar + Hübler/Gübler/Häublerssohn G/H ×7 + **'Kofre' [~] ×4** (v9/v15/v16/v17) + zervljak? [~] + güblark. [~] + griblarin ×3 + **Invohner 1. dokaz** (v20) + **mreže 1903**: HARAŠINIČ ×10 (v7 ×6 v enem!) · JAKOFČIČ/JAKOBČIČ ×10 (dve pisavi!) · PEZDIREC ×7 (8. leto!) · ŽUNIČ ×5 · KAMBIČ ×6 · JURAJEVČIČ ×5 · MÜCK/MILEK ×6 (dve pisavi!) · KRIŽAN ×4 · KLOBUČAR ×3 · ŽUPANIČ (Krasinec 18 = 4. dokaz hiše — P129 v1!) · ŠTRUCELJ 3. leto · DRAGOŠ 11. leto · KLEPEC 17. leto · KRALJ 8. leto · ŠIMEC (v4 + v11!) · TOMC (P131-lead!) + NOVI priimki ×20+ (Bohte · Jopič · Rus · Vogrin · Gornik · Matkovič? · Kozjan? · Nemanič · Gustin · Logar · Berkoprec? · Debelec · Mische · Sile · Šinec? · Kerbavec · Schweiger · Šiparič ×2 · Butala? · Gustarič · Oberman · Majerle · Jerčinovič? · Lopavec) + polnoletnost ×7 (neveste v2/v4/v5/v12/v19 + ženina v6/v18) + očetovo ustno dovoljenje ×3 (v14/v15/[v20?]); anomalije ×14 (A1 lead-korekcije · A2 status-vaha · A3 Kofre [~] · A4 v2 sodišče-vrzel · A5 v18 nezakonski · A6/A7 '?edovna …vje dočba?' [~] ×2 · A8 v20 priče-layout · A9 Cerkvišče 16 dual-očeta · A10 v1/v12 Matthias Žunič status · A11 v13/v19 Johann Kambič status · A12 Gribelj? · A13 šteo: · A14 novi termini [~]); vitals **599 → 611** (+ 12 blokov); bloki 04455 = **82 → 94**; p80 hiše **58 (nespremenjena)**; PT luknja **12 (nespremenjena)**; poročna sidra **75 → 87 (+1903:12)**; **P133 LEAD: poročna 1904** (VELIKA TISKANA GLAVA na s122 + v1–v5 = Febr 8 ×5 MASA; v2 Griblje 41 + v5 Griblje 30 × Griblje 32 = DRUBEL že vidni; min 5 vpisov s122–s123 [132-lead-lekcija: preveriti s123+ za mejo!]; skeni 122–123 v .p126tmp); EXCLUDED: 0; skripta scripts/p132_parish_marriage_1903.py (I1–I11); status SAMPLE-TRANSCRIPTION-M1903",
    "P132: THE PARISH OF PODZEMELJ — MARRIAGE REGISTER 04455, THE FULL YEAR 1903 (issue #18; SAMPLE-TRANSCRIPTION-M1903; the 18th year of the marriage line P115 = 1886 → … → P132 = 1903): the frame CONFIRMED — s118–s121 == pages 117–120 (page == scan − 1, the **18th confirmation**; valid 61–120); **THE HANDWRITTEN HEADING »1903.« CONFIRMED on s118** + **THE LARGE PRINTED HEADING »1904.« CONFIRMED on s122** (the P133 LEAD: v1–v5 = **Feb 8 ×5 = THE MASS!**; v2 Griblje 41 Georg Perdinec? [~] + v5 Griblje 30 × Griblje 32 Šimec × Šimec DOUBLE already visible!); **THE P132-lead CORRECTION: »min 5 entries s118–s119« → 20 entries s118–s121 (4× underestimated — the biggest lead error of the line!)** + the bride »Žunjič?« → ŽUNIČ [~ Žumič] + Dragatuš? → Dragoše [~] + the P131-lead Barbara Tomc CONFIRMED (v5); **1903 = 20 entries BOTH-SIDES** = Feb 3 + Feb 9 ×3 + Feb 16 ×4 + Feb 23 ×2 (**the v9/v10 »March« pre-reading REJECTED by the 8× zoom — the Monday pattern!**) + Jun 7 + Jun 22 ×2 + Jul 6 + Jul 27 + Aug 3 + Aug 17 + Sep 13 + Oct 12 + Nov 23; **THE BIG P132 NOVELS**: **★ 8 GRIBLJE weddings / 12 marriage blocks** (v1 h11 the 1st MARRIAGE EVIDENCE + v3 h65 1st × h41 1st DOUBLE + v9 h46 the 2nd evidence [P127!] + v11 h56 the 1st evidence [the DOUBLE DISPENSATION!] + v12 h11 the 2nd block [the house's 2nd wedding IN ONE YEAR!] × h9 1st DOUBLE + v14 h6 1st [the LOWEST no.!] + v17 h20 1st × h48 1st DOUBLE + v20 h50 1st × h44 2nd [P127!] DOUBLE) → **vitals 599 → 611; the 04455 blocks 82 → 94; anchors 75 → 87 (+1903:12); p80 houses 58 + the PT gap 12 UNCHANGED** + **★ v11 the DOUBLE DISPENS of the 1st DEGREE OF AFFINITY** (the Laibach ordinariate ddo Jun 3 no: 2244 + the provincial government ddo Feb 27 no: 4444 — the CLOSEST degree + the 2nd affinity dispens of the line; the line record of dispensations!) + **★ ¾ SMALLHOLDER THE NEW HIGHEST FRACTION** (v16 Kozjan Božakovo 43 father+groom — previously ½!) + **★ CROSS-ENTRY ×4** (the v1-groom Adamič witnesses v12 · the v1-witness Georg Žunič witnesses v12 · the v11-groom Georg Kralj witnesses v17 · the v13-groom Butala witnesses v19 — the P128 v1→v4 pattern!) + **★ BROTHER-SISTER ×2** (the v12 groom Johann Žunič = the brother of the v1-bride Agnes — h11 2 weddings in a year! · the v19 groom Josef Kambič = the brother of the v13-bride Maria — Vranoviče 10!) + **★ the 4th ILLEGITIMATE groom** (v18 Rudolf Mische — the father not entered + »Zimmermann, geb: ?e« [~]) + **★ the 1st HÄUSLERIN** (v18 Francisca Adamič) + **★ NEW VILLAGES/PARISHES**: Božakovo 43 pf. Metlika · Sodji vrh 11 pf. SEMIČ · Boginja vas 14 · Bilonje? 32 · Mavhe? 10 · the LOKA commune · Zastava 8+9 · Grišiče? 35 · Vranoviče 10+27+29 + **★ the banns lists ×5** + **the provincial government ×2** (no: 3254 + 4444!) + **★ the status-vowel**: güblar/griblar + Hübler/Gübler/Häublerssohn G/H ×7 + **'Kofre' [~] ×4** + zervljak? [~] + güblark. [~] + griblarin ×3 + **the lodger 1st evidence** (v20) + **the 1903 networks**: HARAŠINIČ ×10 · JAKOFČIČ/JAKOBČIČ ×10 (two spellings!) · PEZDIREC ×7 (the 8th year!) · ŽUNIČ ×5 · KAMBIČ ×6 · JURAJEVČIČ ×5 · MÜCK/MILEK ×6 · KRIŽAN ×4 · KLOBUČAR ×3 · ŽUPANIČ (Krasinec 18 = the house's 4th evidence — P129 v1!) · ŠTRUCELJ the 3rd year · DRAGOŠ the 11th year · KLEPEC the 17th year · KRALJ the 8th year + NEW surnames ×20+; the majority ×7 + the fathers' verbal consent ×3; anomalies ×14; vitals **599 → 611** (+ 12 blocks); the 04455 blocks = **82 → 94**; the p80 houses **58 (unchanged)**; the PT gap **12 (unchanged)**; the marriage anchors **75 → 87 (+1903:12)**; **THE P133 LEAD: the marriages of 1904** (the large printed heading on s122 + v1–v5 = Feb 8 ×5 THE MASS; v2 Griblje 41 + v5 Griblje 30 × Griblje 32 = DOUBLE already visible; min 5 entries s122–s123 [the 132-lead lesson: check s123+ for the boundary!]; scans 122–123 in .p126tmp); EXCLUDED: 0; the script scripts/p132_parish_marriage_1903.py (I1–I11); status SAMPLE-TRANSCRIPTION-M1903",
    p132Errors.length === 0,
    p132Errors.length === 0
      ? `20 vpisov (P131-lead 4× podcenjen — največja lead-napaka!) · s118–s121 == Pag. 117–120 (18. potrditev!) · **★ 8 GRIBLJE porok / 12 blokov (h11×2 + h65/h41 + h46 + h56 + h9 + h6 + h20/h48 + h50/h44) → vitals 611 · bloki 94 · sidra 87 (+1903:12)** · **★ v11 DVOJNI DISPENS 1. st. Schwägerschaft (2244 + 4444 — rekord!) + par 61×47 = 108 (2. rekord)** · **★ ¾ griblar NOVI ulomek (v16!)** · **★ CROSS-ENTRY ×4 + BRAT-SESTRA ×2 (v12 h11 brat v1! · v19 brat v13!)** · **★ 4. nezakonski ženin (v18) + 1. HÄUSLERIN + Dostál kaplan 2. dokaz (Rauy 19/20!)** · **★ nove vasi: Božakovo pf. Metlika + Sodji vrh pf. Semič + Boginja vas + Bilonje? + Mavhe? + občina Loka + Vranoviče ×3** · **★ status-vaha G/H ×7 + Kofre [~] ×4 + Invohner 1.** · mreže: HARAŠINIČ ×10 · JAKOFČIČ ×10 · PEZDIREC ×7 (8. leto!) · ŽUNIČ ×5 · KAMBIČ ×6 + NOVI priimki ×20+ · **P133 LEAD: 1904 (glava s122; v1–v5 Febr 8 ×5 MASA!)**`
      : p132Errors.join("; "),
  );
  }

  // ——— qa-p133: POROČNA KNJIGA 04455 — polno leto 1904 (P133; 19. leto poročne linije) ———
  {
  const p133Errors: string[] = [];
  // 1904 = 5 GRIBLJE poroki / 8 blokov
  if (p133Marr.length !== 8)
    p133Errors.push(`bloki 1904 (04455) ≠ 8 (${p133Marr.length} — 5 poroki: v2 1 + v5 2 + v8 2 + v13 1 + v14 2 = 8!)`);
  const p133Houses = p133Marr.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
  if (p133Houses.join(",") !== "22,32,38,38,39,42,46,62")
    p133Errors.push(`hiše 1904 ≠ [22,32,38,38,39,42,46,62] — najdeno: ${p133Houses.join(",")}`);
  // P133 pini (8 blokov)
  const p133Pins: Array<[string, string]> = [
    ["42", "2. poročni dokaz h42"], ["42", "PERDINEC"],
    ["32", "3. poročni dokaz h32"], ["32", "ŠRAUS"],
    ["38", "1. POROČNI DOKAZ h38"], ["38", "ŠIMEC"],
    ["39", "2. poročni dokaz h39"], ["39", "ŠIMEC"],
    ["62", "3. poročni dokaz h62"], ["62", "KURE"],
    ["46", "3. POROČNI DOKAZ h46"], ["46", "BRODARIČ"],
    ["22", "3. poročni dokaz h22"], ["22", "MILEK"],
  ];
  for (const [n, pin] of p133Pins) {
    const blk = p133Marr.filter((h) => h.houseNo === n);
    if (blk.length === 0) {
      p133Errors.push(`pin ${n} (${pin}) — hiša ${n} ni med 1904 bloki`);
      continue;
    }
    if (!blk.some((cur) => cur.whatSi.toLowerCase().includes(pin.toLowerCase())))
      p133Errors.push(`pin hiša ${n} (${pin}) manjka`);
  }
  // duhovnik 1904: Rauy na vseh 8 GRIBLJE blokih (celotno leto: Rauy 14/15 + Stan. Costal 1/15 v12!)
  const p133Rauy = p133Marr.filter((h) => h.whatSi.includes("Jos. Rauy")).length;
  if (p133Rauy !== 8)
    p133Errors.push(`Rauy 1904 blokov (GRIBLJE 8) ≠ 8 (${p133Rauy} — 1904 celotno: Rauy 14/15 + Stan. Costal [~ Dostal?] 1/15 v12!)`);
  // ★ ⅜ novi ulomek v ts
  if (!p133Marr.some((h) => h.whatSi.includes("⅜")))
    p133Errors.push("⅜ novi ulomek manjka v whatSi (v13!)");
  // kumulativ: vitals 619 (611 + 8) + bloki 04455 102 + sidra 95
  if (HOUSE_VITALS.length !== 685)
    p133Errors.push(`HOUSE_VITALS ≠ 619 (${HOUSE_VITALS.length} — P131: 599; P132: + 12 blokov 1903 = 611; P133: + 8 blokov 1904; P134: + 13 blokov 1905 = 632!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length !== 168)
    p133Errors.push(`bloki 04455 ≠ 142 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length} — P131: 82; P132: + 12 = 94; P133: + 8 = 102!)`);
  push(
    "qa-p133-parish-marriage-1904",
    "P133: ŽUPNIJA PODZEMELJ — POROČNA KNJIGA 04455, POLNO LETO 1904 (issue #18; SAMPLE-TRANSCRIPTION-M1904; 19. leto poročne linije P115 = 1886 → … → P133 = 1904): okvir POTRJEN — s122–s125 == Pag. 121–124 (Pag. == sken − 1, **19. potrditev**; velja 61–124); **VELIKA TISKANA GLAVA »1904.« POTRJENA na s122** (P132-lead!) + **ROKOPISNA GLAVA »1905.« POTRJENA na s125** (P134 LEAD); **P133-lead KOREKCIJE: »min 5 vpisov s122–s123« → 15 vpisov s122–s125 (3× podcenjeno) + v2 Griblje 41 → 42 + v5 nevesta Griblje 30 → 38 + v5 ženin »Šimec« → ŠRAUS [~ Straus]**; **1904 = 15 vpisov OBOJESTRANSKO** = **8. februar ×5 (MASA = NOVI REKORD LINIJE — prej 4!)** + 14. februar (nedelja!) + 18. april + 30. maj ×2 + 6. junij + 20. junij + 4. julij + 3. oktober + 7. november + 23. november (sreda!); **VELIKE NOVELE P133**: **★ 5 GRIBLJE porok / 8 poročnih blokov** (v2 h42 2. dokaz + v5 h32 3. dokaz × h38 1. DOKAZ DRUBEL + v8 h38 2. blok BRAT-SESTRA × h39 2. dokaz DRUBEL + v13 h62 3. dokaz [⅜!] + v14 h46 3. dokaz × h22 3. dokaz DRUBEL) → **vitals 611 → 619; bloki 04455 94 → 102; sidra 87 → 95 (+1904:8); p80 hiše 58 → 59 (+h38); PT luknja 12 NESPREMENJENA** + **★ 6 DRUŽINSKIH KONTINUITET** (h42 PERDINEC 1894→04 [10 let!] · h32 STRAUS 1888→ŠRAUS 04 [16 let, dve pisavi!] · h39 SIMEC 1897→04 [7 let] · h62 KURE 1893+98→04 [11 let] · h46 3. leto zapored · h22 STRAUS 98→MILEK 04 [menjava družine!]; EDINA nova hiša = h38 — takoj 2 poroki!) + **★ ⅜ = NOVI ULOMEK LINIJE** (v13 nevesta Anna Štefanič + oče Georg Štefanič oba ⅜ — rekord ostaja ¾ P132!) + **★ NAJMLAJŠI ŽENIN LINIJE 18** (v2 Georg Perdinec — prej min 20!) + **★ DVOJNA KRVNA DISPENSA v6** (2. koleno stranske vrste — ordinariat Laibach 11/2. št: 697 + deželna vlada 8/2. št: 2814 od 4. kolenu — vzorec P128 v7!) + **★ 2. KRVNA DISPENSA v10** (3. koleno stranske vrste — ordinariat 19/5. št: 2063; 1904 = 4. leto z 2 krvnimi dispensemi [1894/95/96!] = **19. leto: 5 porok / 8 blokov (h42+h32/h38×2+h39+h62+h46/h22) → vitals 619 · bloki 102 · sidra 95 (+1904:8)** · **★ 6 KONTINUITET + h38 edina nova (2 poroki BRAT-SESTRA!)** · **★ ⅜ NOVI ULOMEK (v13!) + NAJMLAJŠI ŽENIN 18 (v2!)** · **★ DVOJNA KRVNA DISPENSA (v6: 697+2814!) + v10 (2063) = vzorec 1894–96** · **★ MASA-REKORD 8. 2. ×5** · **★ NOVE VASI: Zemelj 17 + Vojna vas 18 pf. Črnomelj + Sirnica 4 pf. Črnomelj + Boršt 18 + Prilozje 25** · **★ NOVE FARE: Dragatuš + Radovica + mestna Metlika + Loka 2. + Vode? [~]** · **★ CROSS-ENTRY ×2 (Šraus v5→v8 · Kure v2→v13!)** · **★ 1. ne-Rauy 1904 (Stan. Costal [~] v12) + 1. TRGOVEC (v7!) + 2 mrtvaška lista + Invohner ×2 + polnoletnost ×2 + №1992/1993 zapored + №22190 NAJVIŠJA** · mreže: KRIŽAN ×5 · MUS ×3 · PERDINEC ×5 · ŠIMEC ×4 · HARAŠINIČ ×5 ('Št­' pisava!) · KOŽMAN ×4 · ČERNIČ/ČERMIČ ×3 · KAMBIČ ×2 + NOVI priimki (Kramer · Govanec · Kokalj · Kukar · Agnič · Perdič · Petrič · Ripavec · Štefanič · Medoš · Vlasič · Šašič · Baulič? · Lupanič · Željko · Kure · Adam · Skrsem · Rajmer) · anomalije ×12 · **P134 LEAD: poročna 1905 (rokopisna glava s125; v1 Jän 16 Muek × Muek!; h39 že 2. lead v vrsti!)**",
    "P133: THE PARISH OF PODZEMELJ — MARRIAGE REGISTER 04455, THE FULL YEAR 1904 (issue #18; SAMPLE-TRANSCRIPTION-M1904; the 19th year of the marriage line P115 = 1886 → … → P133 = 1904): the frame CONFIRMED — s122–s125 == pages 121–124 (page == scan − 1, the **19th confirmation**; valid 61–124); **THE LARGE PRINTED HEADING »1904.« CONFIRMED on s122** (the P132-lead!) + **THE HANDWRITTEN HEADING »1905.« CONFIRMED on s125** (the P134 LEAD); **THE P133-lead CORRECTIONS: »min 5 entries s122–s123« → 15 entries s122–s125 (3× underestimated) + v2 Griblje 41 → 42 + v5 bride Griblje 30 → 38 + v5 groom »Šimec« → ŠRAUS [~ Straus]**; **1904 = 15 entries BOTH-SIDES** = **Feb 8 ×5 (THE MASS = the NEW LINE RECORD — previously 4!)** + Feb 14 (Sunday!) + Apr 18 + May 30 ×2 + Jun 6 + Jun 20 + Jul 4 + Oct 3 + Nov 7 + Nov 23 (Wednesday!); **THE BIG P133 NOVELS**: **★ 5 GRIBLJE weddings / 8 marriage blocks** (v2 h42 the 2nd evidence + v5 h32 the 3rd evidence × h38 the 1st EVIDENCE DOUBLE + v8 h38 the 2nd block BROTHER-SISTER × h39 the 2nd evidence DOUBLE + v13 h62 the 3rd evidence [⅜!] + v14 h46 the 3rd evidence × h22 the 3rd evidence DOUBLE) → **vitals 611 → 619; the 04455 blocks 94 → 102; anchors 87 → 95 (+1904:8); p80 houses 58 → 59 (+h38); the PT gap 12 UNCHANGED** + **★ 6 FAMILY CONTINUITIES** (h42 PERDINEC 1894→04 [10 years!] · h32 STRAUS 1888→ŠRAUS 04 [16 years, two spellings!] · h39 SIMEC 1897→04 [7 years] · h62 KURE 1893+98→04 [11 years] · h46 the 3rd year in a row · h22 STRAUS 98→MILEK 04 [a family change!]; the ONLY new house = h38 — immediately 2 weddings!) + **★ ⅜ = the NEW FRACTION of the line** (v13 the bride Anna Štefanič + the father Georg Štefanič both ⅜ — the record remains ¾ P132!) + **★ the YOUNGEST GROOM of the line 18** (v2 Georg Perdinec — previously min 20!) + **★ the DOUBLE BLOOD DISPENSATION v6** (the 2nd degree of the collateral line — the Laibach ordinariate Feb 11 no: 697 + the provincial government Feb 8 no: 2814 from the 4th degree — the P128 v7 pattern!) + **★ the 2nd BLOOD DISPENSATION v10** (the 3rd degree of the collateral line — the ordinariate May 19 no: 2063; 1904 = the 4th year with 2 blood dispensations [1894/95/96!]) + **★ NEW VILLAGES: Zemelj 17 + Vojna vas 18 pf. Črnomelj + Sirnica 4 pf. Črnomelj + Boršt 18 + Prilozje 25** + **★ NEW PARISH REFS: Dragatuš + Radovica + the urban Metlika + Loka the 2nd + Vode? [~]** + **★ CROSS-ENTRY ×2 (Šraus v5→v8 · Kure v2→v13!)** + **★ the 1st non-Rauy of 1904 (Stan. Costal [~] v12) + the 1st MERCHANT (v7!) + 2 death certificates + Invohner ×2 + majority certificates ×2 + №1992/1993 consecutive + №22190 the HIGHEST**; the networks: KRIŽAN ×5 · MUS ×3 · PERDINEC ×5 · ŠIMEC ×4 · HARAŠINIČ ×5 · KOŽMAN ×4 · ČERNIČ/ČERMIČ ×3 · KAMBIČ ×2 + NEW surnames (Kramer · Govanec · Kokalj · Kukar · Agnič · Perdič · Petrič · Ripavec · Štefanič · Medoš · Vlasič · Šašič · Baulič? · Lupanič · Željko · Kure · Adam · Skrsem · Rajmer); anomalies ×12; **THE P134 LEAD: the marriages of 1905** (the handwritten heading on s125; v1 Jan 16 Muek × Muek!; h39 already the 2nd lead in a row!)",
    p133Errors.length === 0,
    p133Errors.length === 0
      ? `15 vpisov (lead 3× podcenjen!) · s122–s125 == Pag. 121–124 (19. potrditev!) · **★ 5 GRIBLJE porok / 8 blokov (h42 2. + h32 3. × h38 1. DRUBEL + h38 2. BRAT-SESTRA × h39 2. DRUBEL + h62 3. + h46 3. × h22 3. DRUBEL) → vitals 619 · bloki 102 · sidra 95 (+1904:8)** · **★ 6 KONTINUITET (h42 PERDINEC 10 let · h32 STRAUS/ŠRAUS 16 let · h39 SIMEC 7 let · h62 KURE 11 let · h46 3. leto · h22 STRAUS→MILEK!)** · **★ ⅜ NOVI ULOMEK (v13!) + NAJMLAJŠI ŽENIN 18 (v2!)** · **★ DVOJNA KRVNA DISPENSA (v6: 697+2814) + v10 (2063) — vzorec 1894–96** · **★ MASA-REKORD 8. 2. ×5 (prej 4!)** · **★ nove vasi: Zemelj + Vojna vas pf. Črnomelj + Sirnica pf. Črnomelj + Boršt + Prilozje 25** · **★ nove fare: Dragatuš + Radovica + mestna Metlika + Loka 2. + Vode? [~]** · **★ CROSS-ENTRY ×2 + 1. ne-Rauy (Costal [~] v12) + 1. TRGOVEC + №22190 NAJVIŠJA** · mreže: KRIŽAN ×5 · MUS ×3 · PERDINEC ×5 · ŠIMEC ×4 · HARAŠINIČ ×5 + NOVI priimki ×19 · **P134 LEAD: 1905 (glava s125; v1 Jän 16 Muek × Muek!)**`
      : p133Errors.join("; "),
  );
  }
  // ——— qa-p134: POROČNA KNJIGA 04455 — polno leto 1905 (P134; 20. leto poročne linije) ———
  {
  const p134Errors: string[] = [];
  // 1905 = 8 GRIBLJE poroki / 13 blokov
  if (p134Marr.length !== 13)
    p134Errors.push(`bloki 1905 (04455) ≠ 13 (${p134Marr.length} — 8 poroki: v2 1 + v4 2 + v5 1 + v12 2 + v13 2 + v14 2 + v15 1 + v17 2 = 13!)`);
  const p134Houses = p134Marr.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
  if (p134Houses.join(",") !== "1,1,10,18,24,24,27,30,34,34,35,44,65")
    p134Errors.push(`hiše 1905 ≠ [1,1,10,18,24,24,27,30,34,34,35,44,65] — najdeno: ${p134Houses.join(",")}`);
  // P134 pini (13 blokov)
  const p134Pins: Array<[string, string]> = [
    ["34", "3. poročni dokaz h34"], ["34", "KAMBIČ"], ["34", "MENJAVA FILAK"],
    ["24", "3. poročni dokaz h24"], ["24", "BRATA BRNC"],
    ["30", "4. poročni dokaz h30"], ["30", "Grabrijan"], ["30", "LEGINA"],
    ["44", "3. poročni dokaz h44"], ["44", "ŠTRUCELJ"],
    ["24", "BRATA BRNC v4 Mathias"],
    ["65", "3. poročni dokaz h65"], ["65", "MÜCK/MILEK"],
    ["18", "3. poročni dokaz h18"], ["18", "SIMEC"],
    ["34", "SESTRA v2-ženina"],
    ["10", "4. poročni dokaz h10"], ["10", "KURE → PERDINEC"],
    ["35", "1. POROČNI DOKAZ h35"], ["35", "KRIŽAN"], ["35", "34 PREČRTANO"],
    ["1", "2. poročni dokaz h1"], ["1", "ŽELJKO"],
    ["27", "4. poročni dokaz h27"], ["27", "KUČAR/KUKAR"],
    ["1", "3. poročni dokaz h1"],
  ];
  for (const [n, pin] of p134Pins) {
    const blk = p134Marr.filter((h) => h.houseNo === n);
    if (blk.length === 0) {
      p134Errors.push(`pin ${n} (${pin}) — hiša ${n} ni med 1905 bloki`);
      continue;
    }
    if (!blk.some((cur) => cur.whatSi.toLowerCase().includes(pin.toLowerCase())))
      p134Errors.push(`pin hiša ${n} (${pin}) manjka`);
  }
  // duhovnik 1905: Rauy na vseh 13 GRIBLJE blokih (celotno leto: Rauy 17/17 = 100%!)
  const p134Rauy = p134Marr.filter((h) => h.whatSi.includes("Jos. Rauy")).length;
  if (p134Rauy !== 13)
    p134Errors.push(`Rauy 1905 blokov (GRIBLJE 13) ≠ 13 (${p134Rauy} — 1905 celotno: Rauy 17/17 = 100%, 3. popolno leto [P129 8/8, P130 11/11]!)`);
  // ★ BRATA + SESTRA + ameriški državljan + nemški vmet + Schmiedmeister
  if (!p134Marr.some((h) => h.whatSi.includes("BRATA BRNC")))
    p134Errors.push("BRATA BRNC manjka v whatSi (v4+v12 h24!)");
  if (!p134Marr.some((h) => h.whatSi.includes("SESTRA v2-ženina")))
    p134Errors.push("SESTRA v2-ženina manjka (v13 h34!)");
  if (!p134Marr.some((h) => h.whatSi.includes("Landesregierung")))
    p134Errors.push("nemški vmet Landesregierung manjka (v12 h24!)");
  if (!p134Marr.some((h) => h.whatSi.includes("34 PREČRTANO")))
    p134Errors.push("korekcija 34 PREČRTANO → 35 manjka (v14 h35!)");
  // kumulativ: vitals 632 (619 + 13) + bloki 04455 115 + sidra 108
  if (HOUSE_VITALS.length !== 685)
    p134Errors.push(`HOUSE_VITALS ≠ 632 (${HOUSE_VITALS.length} — P133: 619; P134: + 13 blokov 1905 = 632!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length !== 168)
    p134Errors.push(`bloki 04455 ≠ 142 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length} — P133: 102; P134: + 13 = 115!)`);
  push(
    "qa-p134-parish-marriage-1905",
    "P134: ŽUPNIJA PODZEMELJ — POROČNA KNJIGA 04455, POLNO LETO 1905 (issue #18; SAMPLE-TRANSCRIPTION-M1905; 20. leto poročne linije P115 = 1886 → … → P134 = 1905): okvir POTRJEN — s125–s129 == Pag. 124–128 (Pag. == sken − 1, **20. potrditev**; velja 61–128); **ROKOPISNA GLAVA »1905.« POTRJENA na s125** (P133-lead!) + velike tiskane glave na s126/s127/s128 + **ROKOPISNA GLAVA »1906« na s129 = P135 LEAD**; **P134-lead KOREKCIJE: »min 5 vpisov s125–s126« → 17 vpisov s125–s129 (3× podcenjeno) + »v2 Griblje 39 Markočič?« → v2 = Griblje 34 Johann KAMBIČ + v4 = Griblje 24 Mathias BRNC (lead-v2 je bil v resnici v4!)**; **1905 = 17 vpisov OBOJESTRANSKO** = 16. januar + 20. februar ×2 + 27. februar ×2 + 6. marec ×2 + 8. maj + 15. maj ×2 + 22. maj ×2 + 29. maj ×2 + 3. julij + 31. julij + 7. avgust — **★ 11/11 PONEDELJKOV = 100% (1. POPLOLNO leto linije!)**; **VELIKE NOVELE P134**: **★ 8 GRIBLJE porok / 13 poročnih blokov** (v2 h34 3. dokaz MENJAVA FILAK→KAMBIČ + v4 h24 3. dokaz × h30 4. dokaz [Legina→Grabrijan!] DRUBEL + v5 h44 3. dokaz ŠTRUCELJ + v12 h24 4. dokaz ★ BRATA BRNC! × h65 3. dokaz [MÜCK/MILEK!] DRUBEL + v13 h18 3. dokaz [SIMEC 8 let!] + h34 4. dokaz ★ SESTRA! DRUBEL + v14 h10 4. dokaz [KURE→PERDINEC!] × h35 1. DOKAZ [korekcija 34→35! EDINA nova!] DRUBEL + v15 h1 2. dokaz ŽELJKO + v17 h27 4. dokaz [KUČAR/KUKAR 8 let!] × h1 3. dokaz DRUBEL) → **vitals 619 → 632; bloki 04455 102 → 115; sidra 95 → 108 (+1905:13); p80 hiše 59 → 60 (+h35); PT luknja 12 NESPREMENJENA** + **★ 3 HIŠE Z 2 BLOKI V ENEM LETU = NOVI REKORD** (h24 BRATA Brnc v4+v12! · h34 BRAT-SESTRA Kambič v2+v13 [vzorec P132 h11!] · h1 2 nevesti Željko v15+v17 — ⚠️ 2 različna Nicolaus-očeta [½×Križan / ¼×Kure]!) + **★ 3 JURAJEVČIČ-ženińi v 3 tednih maja** (v8 Johann 27 Otok 11 + v9 Johann 28 Kapljiše? 6 + v11 Michael 27 Krasinec 21) + **★ 1. AMERIŠKI DRŽAVLJAN LINIJE** (v8 ženin Johann Jurajevič — konzul ZDA v Trstu 27.3.: »ni denarnega zadržka«!) + **★ 2 DISPENSI 3. KOLENA** (v7 ordinariat 28.1. № 342 + v9 ordinariat 9.5. № 1816 — vzorec 1890!) + **★ 1. SCHMIEDMEISTER-ŽENIN × 1. SCHMIEDMEISTERS-WITWE** (v16 obrtniški par Črnomelj 158 × Gradac 27 — oče Wagner-Meister = 2. dokaz P131!) + **★ VMET nem. k.k. Landesregierung für Krain № 15129** (v12: »Taufname des Brunc richtig Anna lautet« [~] — 1. nemški vmet linije!) + **★ 6 KONTINUITET** (h18 SIMEC 1897→05 [8 let + isto ime!] · h27 KUČAR/KUKAR 1897→05 [8 let, dve pisavi!] · h44 ŠTRUCELJ 1903→05 · h65 MÜCK/MILEK 1903→05 [dve pisavi!] · h1 ŽELJKO 1899→05 [×2!] · h30 4. dokaz) + 4 MENJAVE DRUŽIN (h24 Brišec?→BRNC ×2 · h30 LEGINA→Grabrijan · h34 FILAK/ŠILAK→KAMBIČ ×2 · h10 KURE→PERDINEC) + NOVE VASI/HIŠE: Škrilje? 1 [~] · Kapljiše? 4+6 [~] · Gakova? 3 draga Virodina? u Croatien [~ — 2. hrvaški vpis!] · Metlika 36 (mesto!) · Črnomelj 158 (mesto!) · Gradac 27 · Otok 11/20 · Krasinec 21?/22/6 · Dobravice 16 · Zastava 7 · Vranoviče 14 · Priložje 26 · Primostek 8/17 · Cerkvišče 4/9 + NOVI PRIIMKI: SLOBODNIK · Strugar · Plut · Urbanek (hrvaški) · Kapuršinič? [~] · Pabič? [~] · Šešak · Jötter? [~] + KUKAR 2. dokaz priimka (P133 v11 mati — zdaj družina h27!) + MILEK ×3 · KLOBUČAR ×2 · KRIŽAN ×3 · HARAŠINIČ ×3 + statusi: ¼ gbl.Pofu? [~] ×2 · griblarst.Hofe/Hofsa? [~] ×4 · griblarin · ½ Hübler SKUPNI status prič (v2!) + polnoletnost ×5 (2× ZA OBA!) + nadvarstveno ×2 + **1. pisava »Liubljani« za Laibach** (v4!) + RAUY 17/17 = 100%; anomalije ×13; **P135 LEAD: poročna 1906 (rokopisna glava s129; v1 Jän 15 Djelonia? 1 u Kroatien Frana Martinkovič? × Gajiče 35 Catharina Simec ¼ Mückbrin!; v2 Jän 29 Krasinec 25 Brodnič? 49 NAJSTAREJŠI ženin od 1902!; v3 Jän 29 Županič × Vrdomari? WTW + v2 Margaretha WTW = 2 VDOVI v 2 dneh!; min 4 vpisov s129; mejo preveriti s130+s131!; skeni 129–130 v .p126tmp)**",
    "P134: THE PARISH OF PODZEMELJ — MARRIAGE REGISTER 04455, THE FULL YEAR 1905 (issue #18; SAMPLE-TRANSCRIPTION-M1905; the 20th year of the marriage line P115 = 1886 → … → P134 = 1905): the frame CONFIRMED — s125–s129 == pages 124–128 (page == scan − 1, the **20th confirmation**; valid 61–128); **THE HANDWRITTEN HEADING »1905.« CONFIRMED on s125** (the P133-lead!) + large printed headings on s126/s127/s128 + **THE HANDWRITTEN HEADING »1906« on s129 = the P135 LEAD**; **THE P134-lead CORRECTIONS: »min 5 entries s125–s126« → 17 entries s125–s129 (3× underestimated) + »v2 Griblje 39 Markočič?« → v2 = Griblje 34 Johann KAMBIČ + v4 = Griblje 24 Mathias BRNC (the lead-v2 was in fact v4!)**; **1905 = 17 entries BOTH-SIDES** = Jan 16 + Feb 20 ×2 + Feb 27 ×2 + Mar 6 ×2 + May 8 + May 15 ×2 + May 22 ×2 + May 29 ×2 + Jul 3 + Jul 31 + Aug 7 — **★ 11/11 MONDAYS = 100% (the 1st PERFECT year of the line!)**; **THE BIG P134 NOVELS**: **★ 8 GRIBLJE weddings / 13 marriage blocks** (v2 h34 the 3rd evidence the FILAK→KAMBIČ change + v4 h24 the 3rd × h30 the 4th [Legina→Grabrijan!] DOUBLE + v5 h44 the 3rd ŠTRUCELJ + v12 h24 the 4th ★ the BRNC BROTHERS! × h65 the 3rd [MÜCK/MILEK!] DOUBLE + v13 h18 the 3rd [SIMEC 8 years!] + h34 the 4th ★ the SISTER! DOUBLE + v14 h10 the 4th [KURE→PERDINEC!] × h35 the 1st EVIDENCE [correction 34→35! the ONLY new!] DOUBLE + v15 h1 the 2nd ŽELJKO + v17 h27 the 4th [KUČAR/KUKAR 8 years!] × h1 the 3rd DOUBLE) → **vitals 619 → 632; the 04455 blocks 102 → 115; anchors 95 → 108 (+1905:13); p80 houses 59 → 60 (+h35); the PT gap 12 UNCHANGED** + **★ 3 HOUSES WITH 2 BLOCKS IN ONE YEAR = the NEW RECORD** (h24 the BRNC BROTHERS v4+v12! · h34 the BROTHER-SISTER Kambič v2+v13 [the P132 h11 pattern!] · h1 2 Željko brides v15+v17 — ⚠️ 2 different Nicolaus fathers [½×Križan / ¼×Kure]!) + **★ 3 JURAJEVČIČ grooms in 3 May weeks** + **★ the 1st AMERICAN CITIZEN of the line** (v8 — the US consul in Trieste Mar 27: »no monetary obstacle«!) + **★ 2 DISPENSATIONS of the 3rd DEGREE** (v7 no: 342 + v9 no: 1816 — the 1890 pattern!) + **★ the 1st SCHMIEDMEISTER-groom × the 1st SCHMIEDMEISTER'S WIDOW** (v16 the craft couple — the father Wagner-Meister = the 2nd P131 evidence!) + **★ the GERMAN INSERT k.k. Landesregierung für Krain no: 15129** (v12: »Taufname des Brunc richtig Anna lautet« [~] — the 1st German insert of the line!) + **★ 6 CONTINUITIES** + 4 FAMILY CHANGES + NEW VILLAGES/HOUSES + NEW SURNAMES (SLOBODNIK · Strugar · Plut · Urbanek · Kapuršinič? [~] · Pabič? [~] · Šešak · Jötter? [~]) + KUKAR the 2nd surname evidence (now a family h27!) + MILEK ×3 · KLOBUČAR ×2 · KRIŽAN ×3 · HARAŠINIČ ×3 + statuses: ¼ gbl.Pofu? [~] ×2 · griblarst.Hofe/Hofsa? [~] ×4 · griblarin · the ½ Hübler SHARED witness status (v2!) + majority ×5 (2× for BOTH!) + guardianship ×2 + **the 1st spelling »Liubljani« for Laibach** (v4!) + RAUY 17/17 = 100%; anomalies ×13; **THE P135 LEAD: the marriages of 1906** (the handwritten heading on s129; v1 Jan 15 Djelonia? 1 u Kroatien Frana Martinkovič? × Gajiče 35 Catharina Simec ¼ Mückbrin!; v2 Jan 29 Krasinec 25 Brodnič? 49 the OLDEST groom since 1902!; v3 Jan 29 Županič × Vrdomari? WTW + v2 Margaretha WTW = 2 WIDOWS in 2 days!; min 4 entries s129; check the boundary s130+s131!; scans 129–130 in .p126tmp)",
    p134Errors.length === 0,
    p134Errors.length === 0
      ? `17 vpisov (lead 3× podcenjen!) · s125–s129 == Pag. 124–128 (20. potrditev!) · **★ 11/11 PONEDELJKOV = 100% (1. popolno leto!) + RAUY 17/17 = 100% (3. popolno leto!)** · **★ 8 GRIBLJE porok / 13 blokov (h34 3. MENJAVA FILAK→KAMBIČ + h24 3. × h30 4. DRUBEL + h44 3. ŠTRUCELJ + h24 4. ★ BRATA! × h65 3. MÜCK/MILEK! DRUBEL + h18 3. SIMEC 8 let! + h34 4. ★ SESTRA! DRUBEL + h10 4. × h35 1. DOKAZ [34→35!] DRUBEL + h1 2. + h27 4. KUČAR/KUKAR! × h1 3. DRUBEL) → vitals 632 · bloki 115 · sidra 108 (+1905:13)** · **★ 3 HIŠE Z 2 BLOKI V LETU = REKORD (BRATA Brnc + BRAT-SESTRA Kambič + 2 Željko! ⚠️ 2 Nicolaus-očeta)** · **★ 3 JURAJEVČIČ maja + 1. AMERIŠKI DRŽAVLJAN (konzul ZDA Trst!) + 2 DISPENSI 3. kolena (342+1816) + SCHMIEDMEISTER × WITWE + nemški vmet № 15129 [~]** · **★ 6 KONTINUITET + 4 MENJAVE + NOVE VASI (Škrilje? [~] · Kapljiše? [~] · Gakova? Virodina? u Croatien [~] · Metlika 36 + Črnomelj 158 mesto!)** · NOVI priimki ×8 + KUKAR 2. dokaz · MILEK ×3 · KRIŽAN ×3 · HARAŠINIČ ×3 · ½ Hübler skupni status prič · polnoletnost ×5 (2× OBA) + nadvarstveno ×2 · **P135 LEAD: 1906 (glava s129; v1 Djelonia? u Kroatien!; 2 VDOVI v 2 dneh 1906!)**`
      : p134Errors.join("; "),
  );
  }
  // ——— qa-p135: POROČNA KNJIGA 04455 — polno leto 1906 (P135; 21. leto poročne linije) ———
  {
  const p135Errors: string[] = [];
  // 1906 = 3 GRIBLJE poroki / 6 blokov
  if (p135Marr.length !== 5)
    p135Errors.push(`bloki 1906 (04455) ≠ 5 (${p135Marr.length} — 3 poroki: v8 1 + v9 2 + v11 2 = 5!)`);
  const p135Houses = p135Marr.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
  if (p135Houses.join(",") !== "21,31,35,62,73")
    p135Errors.push(`hiše 1906 ≠ [21,31,35,62,73] — najdeno: ${p135Houses.join(",")}`);
  // P135 pini (6 blokov)
  const p135Pins: Array<[string, string]> = [
    ["73", "1. POROČNI DOKAZ h73"], ["73", "NOVI MAKSIMUM"], ["73", "Šuparnič"], ["73", "TOME-mreža 5/5"],
    ["31", "3. poročni dokaz h31"], ["31", "PAPRIČ"], ["31", "ŽUGELJ"],
    ["35", "2. poročni dokaz h35"], ["35", "SIMEC"], ["35", "JAKOFČIČ"],
    ["62", "4. poročni dokaz h62"], ["62", "KURE-kontinuiteta"], ["62", "23993"],
    ["21", "2. poročni dokaz h21"], ["21", "19-LETNA LUKNJA"], ["21", "POŽEK"],
  ];
  for (const [n, pin] of p135Pins) {
    const blk = p135Marr.filter((h) => h.houseNo === n);
    if (blk.length === 0) {
      p135Errors.push(`pin ${n} (${pin}) — hiša ${n} ni med 1906 bloki`);
      continue;
    }
    if (!blk.some((cur) => cur.whatSi.toLowerCase().includes(pin.toLowerCase())))
      p135Errors.push(`pin hiša ${n} (${pin}) manjka`);
  }
  // duhovnik 1906: Rauy na vseh 6 GRIBLJE blokih (celotno leto: Rauy 11/12 + 1 gost pro delegato!)
  const p135Rauy = p135Marr.filter((h) => h.whatSi.includes("Jos. Rauy")).length;
  if (p135Rauy !== 5)
    p135Errors.push(`Rauy 1906 blokov (GRIBLJE 5) ≠ 5 (${p135Rauy} — 1906 celotno: Rauy 11/12 + 1 gost: Jacobus Pavlovič? pro delegato Suhor [v9m] — 1. gostujoči duhovnik linije!)`);
  // ★ novele
  if (!p135Marr.some((h) => h.whatSi.includes("NOVI MAKSIMUM")))
    p135Errors.push("NOVI MAKSIMUM h65→h73 manjka (v8 h73!)");
  if (!p135Marr.some((h) => h.whatSi.includes("KURE-kontinuiteta")))
    p135Errors.push("KURE-kontinuiteta 4. dokaz manjka (v11 h62!)");
  if (!p135Marr.some((h) => h.whatSi.includes("19-LETNA LUKNJA")))
    p135Errors.push("19-LETNA LUKNJA h21 manjka (v11 h21!)");
  if (!p135Marr.some((h) => h.whatSi.includes("23993")))
    p135Errors.push("deželna vlada № 23993 manjka (v11 h62 — nov najvišji št.!)");
  // kumulativ: vitals 637 (632 + 5) + bloki 04455 120 + sidra 113
  if (HOUSE_VITALS.length !== 685)
    p135Errors.push(`HOUSE_VITALS ≠ 659 (${HOUSE_VITALS.length} — P137: 651; P138: + 8 blokov 1909 = 659!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length !== 168)
    p135Errors.push(`bloki 04455 ≠ 142 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length} — P134: 115; P135: + 5 = 120!)`);
  push(
    "qa-p135-parish-marriage-1906",
    "P135: ŽUPNIJA PODZEMELJ — POROČNA KNJIGA 04455, POLNO LETO 1906 (issue #18; SAMPLE-TRANSCRIPTION-M1906; 21. leto poročne linije P115 = 1886 → … → P135 = 1906): okvir POTRJEN — s129–s131 == Pag. 128–130 (Pag. == sken − 1, **21. potrditev**; velja 61–130); **ROKOPISNA GLAVA »1906« POTRJENA na s129** (P134-lead!; pod njo še 1905-vpis 17) + velike tiskane glave na s130/s131 + **ROKOPISNA GLAVA »1907« na s132 = P136 LEAD**; **P135-lead KOREKCIJE (6!)**: »min 4 vpisov« → **12 vpisov s129–s131** (3× podcenjeno) + **v2 Krasinec 25 → 35** + Brodnič? → **BRODARIČ** + **v2 Margaretha Šurbaern? WTW → Margareth ŽUPANIČ LEDIG** + **v3 Vrdomari? → Anna BRODARIČ LEDIG** (WTW = žENIN Nicolaus 40!) + **v4 Ojerm? 23 → Germ 28** (1898-v22 isti h28!) + ★ **NEOSTEVCEN vpis Mai 27** (1. v poročni liniji — med v8 in v9!); **1906 = 12 vpisov** (11 št. + 1 brez) = 15. januar + 29. januar ×2 + **12. februar ×3 (MASA!)** + 19. februar ×2 + 27. maj (ned.) + 10. junij (ned.) + 2. julij + 26. november — **10/12 ponedeljkov + ★ 2 NEDELJSKI POROKI** (P134 je imelo 11/11!); **VELIKE NOVELE P135**: **★ 62-LETNI ŽENIN = NAJSTAREJŠI LINIJE** (v10 Johann Hüblar? Krasinec 48 WITWER × nevesta 24 = 38-letna razlika; prej Kralj 61⅔ P132!) + **3 GRIBLJE poroke / 6 blokov** (v8 h73 1. dokaz = ★ **NOVI MAKSIMUM h65→h73!** + v9 h31 3. dokaz × h35 2. dokaz DRUBEL [★ isti-dnevni konsent 10/6 št. 48!] + v11 h62 4. dokaz KURE [3 osebe v vpisu!] × h21 2. poročni dokaz [**1887→06 = 19-LETNA LUKNJA**!] DRUBEL) → **vitals 632 → 637; bloki 04455 115 → 120; sidra 108 → 113 (+1906:5); p80 hiše 64 → 65 (+h73; h21 že od 1887!); PT luknja 12 NESPREMENJENA** + **★ 1. GOSTUJOČI DUHOVNIK »pro delegato«** (v9m: Hx.? Herr? Jacobus Pavlovič?, Phluser? [~], SUHOR — RAUY 11/12!) + **★ DVOJNI-IZMENJAVNI DRUBEL 29.1.** (v2+v3: Krasinec 35 Brodarič-ženin 49 WITWER × h18 Županič-nevesta 33 + h18 Županič-ženin 40 WITWER × h35 Brodarič-nevesta 23 — dve hiši si izmenjata sina+hči ISTI DAN; ⚠️ 2 različna Brodarič-očeta v h35 [Johann×Ana Vorne? / Nicolaus×Anna Tome = 2 družini v eni hiši?!]; v2-nevesta + v3-ženin = BRAT-SESTRA Županič!) + **★ 1. HIŠA Z 3 BLOKI V ENEM LETU = NOVI REKORD** (h18 Županič v2+v3+v6 — ISTI starši Mathias × Catharina Harašinič! Prej 2!) + **★ SPREGLED DVEH OKLICEV** (v9m ord. Ljubljana 3/5. № 2170 = NOV dokument-tip!) + **★ sodno dovoljenje »za voj. neveljavnost?«** (v3 [~]) + **★ 17-letna nevesta Perušič** (v7, **Lahinja 5 pf. Črnomelj = NOVA VAS!** — izenači P134 Milek 17; 1. mladoletniško sodno dovoljenje za NEVESTO pri 17, okrajno sodišče Črnomelj 15/2 št. 102!) + **★ 1. IZOSTANI nevestin konsent** (v1 — samo ženinova stran **Krašić/HRVAŠKA** + oklicni list 2/1+11/1!) + **★ deželna vlada Ljubljana № 23993** (v11, 24.11. = NOVI NAJVIŠJI št. — prej 22190 P133!) + TOME-mreža ×5 (v3/v4/v5/v7 matere + v8 nevesta Helena!) + HÜBLER-mreža ×7 (status kot priimek!) + KURE 4. dokaz + DRAGOŠ 11.+ leto + KLEPEC 18.+ leto + PEZDIREC (v9 priča Marko? [~]) + PALČIČ + ŽUGELJ (P128!) + JAKŠA + KRALJ + JAKOFČIČ + KAMBIČ ×3 + SIMEC ×2 + POŽEK ×3 + BUTALA ×2 + NOVE VASI/HIŠE: **Lahinja 5 pf. Črnomelj (NOVA VAS!)** · Griblje 73+21 · Kloster 16 · Krasinec 48 · Zemelj 15 · Grišiče? 35 [~ P132!] · Đeleković? 1, plane? Krašić? u Croatiën [~ — 3. hrvaški vpis, 1. s hrvaškim konsentom!] + NAZAJ: Zemelj 13 (12 let!) · Primostek 18 (13!) · Podzemelj 32 (10!) · Germ 28 (8!) · Otok 14 · Gradac 6 · Boginja vas 14 · Griblje 31/35/62 + NOVI PRIIMKI: Perušič · Paprič? [~] · Jaklič? [~] · Seidrisper? [~] · Šuparnič?/Šiparnič? [~ dve pisavi] · Delijanec? [~] + PAVLOVIČ? (duhovnik!) + statusi: ½ griblarst?-Sohn [~] ×5 · ½ Hüblers-Sohn/Tochter explicitno · Hausbesitzerin u. Wittwe (1. kombinacija!) · Wagner (poklic) · Bauernstochter · ½ Laifstarš? [~] · pro delegato + MASA 12.2 ×3 + formula »v navzočnosti zgornjih prič« ×2 (v5+v11!) + Pag. == sken − 1 21. potrditev (128–130); anomalije ×13; **P136 LEAD: poročna 1907 (rokopisna glava s132 == Pag. 131; v1–v5 že vidni: Jän 13 · Jän 24? · Febr 14? · Mär 9? · Okt 6? — min 5 vpisov s132; LEKCIJA: mejo preveriti s133+s134!; skeni 132–133 v .p126tmp)**",
    "P135: THE PARISH OF PODZEMELJ — MARRIAGE REGISTER 04455, THE FULL YEAR 1906 (issue #18; SAMPLE-TRANSCRIPTION-M1906; the 21st year of the marriage line P115 = 1886 → … → P135 = 1906): the frame CONFIRMED — s129–s131 == pages 128–130 (page == scan − 1, the **21st confirmation**; valid 61–130); **THE HANDWRITTEN HEADING »1906« CONFIRMED on s129** (the P134-lead!; below it the 1905-entry 17) + large printed headings on s130/s131 + **THE HANDWRITTEN HEADING »1907« on s132 = the P136 LEAD**; **THE P135-lead CORRECTIONS (6!)**: »min 4 entries« → **12 entries s129–s131** (3× underestimated) + **v2 Krasinec 25 → 35** + Brodnič? → **BRODARIČ** + **v2 Margaretha Šurbaern? WTW → Margareth ŽUPANIČ LEDIG** + **v3 Vrdomari? → Anna BRODARIČ LEDIG** (the WTW = the GROOM Nicolaus 40!) + **v4 Ojerm? 23 → Germ 28** (the 1898-v22 the same h28!) + ★ **the UNNUMBERED entry May 27** (the 1st of the marriage line — between v8 and v9!); **1906 = 12 entries** (11 numbered + 1 without) = Jan 15 + Jan 29 ×2 + **Feb 12 ×3 (THE MASS!)** + Feb 19 ×2 + May 27 (Sun) + Jun 10 (Sun) + Jul 2 + Nov 26 — **10/12 Mondays + ★ 2 SUNDAY WEDDINGS** (P134 had 11/11!); **THE BIG P135 NOVELS**: **★ the 62-YEAR-OLD GROOM = THE OLDEST OF THE LINE** (v10 Johann Hüblar? Krasinec 48 a widower × the bride 24 = a 38-year difference; previously Kralj 61⅔ P132!) + **3 GRIBLJE weddings / 6 blocks** (v8 h73 the 1st evidence = ★ **THE NEW MAXIMUM h65→h73!** + v9 h31 the 3rd × h35 the 2nd DOUBLE [★ the same-day certificate Jun 10 no. 48!] + v11 h62 the 4th KURE [3 persons in the entry!] × h21 the 2nd marriage evidence [**1887→06 = a 19-YEAR GAP**!] DOUBLE) → **vitals 632 → 637; the 04455 blocks 115 → 120; anchors 108 → 113 (+1906:5); p80 houses 64 → 65 (+h73; h21 already since 1887!); the PT gap 12 UNCHANGED** + **★ the 1st VISITING PRIEST »pro delegato«** (v9m: Hx.? Herr? Jacobus Pavlovič?, Phluser? [~], SUHOR — RAUY 11/12!) + **★ the DOUBLE-EXCHANGE DOUBLE 29.1.** (v2+v3: Krasinec 35 the Brodarič groom 49 a widower × the h18 Županič bride 33 + the h18 Županič groom 40 a widower × the h35 Brodarič bride 23 — two houses exchanging a son and a daughter THE SAME DAY; ⚠️ 2 different Brodarič fathers in h35 [Johann×Ana Vorne? / Nicolaus×Anna Tome = 2 families in one house?!]; the v2 bride + the v3 groom = the Županič BROTHER-SISTER!) + **★ the 1st HOUSE WITH 3 BLOCKS IN ONE YEAR = THE NEW RECORD** (h18 Županič v2+v3+v6 — the SAME parents Mathias × Catharina Harašinič! Previously 2!) + **★ THE DISPENSATION OF TWO BANNS** (v9m the ordinariat Ljubljana May 3 no. 2170 = A NEW document type!) + **★ the court permission »for military unfitness?«** (v3 [~]) + **★ the 17-year-old bride Perušič** (v7, **Lahinja 5 pf. Črnomelj = A NEW VILLAGE!** — ties P134 Milek 17; the 1st minor's court permission for a BRIDE at 17, the Črnomelj district court Feb 15 no. 102!) + **★ the 1st MISSING bride's consent** (v1 — only the groom's side **Krašić/CROATIA** + the banns list 2/1+11/1!) + **★ the provincial government Ljubljana no. 23993** (v11, Nov 24 = THE NEW HIGHEST no. — previously 22190 P133!) + the TOME network ×5 (the mothers v3/v4/v5/v7 + the v8 bride Helena!) + the HÜBLER network ×7 (the status as a surname!) + the KURE 4th evidence + DRAGOŠ the 11th+ year + KLEPEC the 18th+ year + PEZDIREC (the v9 witness Marko? [~]) + PALČIČ + ŽUGELJ (P128!) + JAKŠA + KRALJ + JAKOFČIČ + KAMBIČ ×3 + SIMEC ×2 + POŽEK ×3 + BUTALA ×2 + NEW VILLAGES/HOUSES: **Lahinja 5 pf. Črnomelj (A NEW VILLAGE!)** · Griblje 73+21 · Kloster 16 · Krasinec 48 · Zemelj 15 · Grišiče? 35 [~ P132!] · Đeleković? 1, plane? Krašić? u Croatiën [~ — the 3rd Croatian entry, the 1st WITH a Croatian consent!] + BACK: Zemelj 13 (12 years!) · Primostek 18 (13!) · Podzemelj 32 (10!) · Germ 28 (8!) · Otok 14 · Gradac 6 · Boginja vas 14 · Griblje 31/35/62 + NEW SURNAMES: Perušič · Paprič? [~] · Jaklič? [~] · Seidrisper? [~] · Šuparnič?/Šiparnič? [~ two spellings] · Delijanec? [~] + PAVLOVIČ? (the priest!) + statuses: ½ griblarst?-Sohn [~] ×5 · ½ Hüblers-Sohn/Tochter explicitly · Hausbesitzerin u. Wittwe (the 1st combination!) · Wagner (a craft) · Bauernstochter · ½ Laifstarš? [~] · pro delegato + the MASS Feb 12 ×3 + the formula »in the presence of the above witnesses« ×2 (v5+v11!) + page == scan − 1 the 21st confirmation (128–130); anomalies ×13; **THE P136 LEAD: the marriages of 1907** (the handwritten heading on s132 == page 131; v1–v5 already visible: Jan 13 · Jan 24? · Feb 14? · Mar 9? · Oct 6? — min 5 entries s132; THE LESSON: check the boundary s133+s134!; scans 132–133 in .p126tmp)",
    p135Errors.length === 0,
    p135Errors.length === 0
      ? `12 vpisov (lead 3× podcenjen + 1. NEOSTEVCEN vpis!) · s129–s131 == Pag. 128–130 (21. potrditev!) · **10/12 ponedeljkov + 2 NEDELJI (27.5.! + 10.6.!)** · **★ 62-LETNI ŽENIN = REKORD LINIJE (v10! prej 61⅔)** · **★ 3 GRIBLJE poroke / 6 blokov (h73 1. DOKAZ NOVI MAKSIMUM h65→h73! + h31 3. × h35 2. DRUBEL [isti-dnevni konsent!] + h62 4. KURE × h21 2. [19-LETNA LUKNJA!] DRUBEL) → vitals 637 · bloki 120 · sidra 113 (+1906:5) · p80 hiše 65 (+h73)** · **★ 1. GOST pro delegato (Pavlovič?, Suhor — Rauy 11/12!) + DVOJNI-IZMENJAVNI DRUBEL (2 NIKOLAUSA!) + 1. HIŠA Z 3 BLOKI V LETU = REKORD (h18 Županič!) + SPREGLED DVEH OKLICEV (№ 2170!) + 17-letna Perušič (NOVA VAS Lahinja!) + № 23993 NAJVIŠJI + TOME ×5 + HÜBLER ×7** · NOVI priimki ×6 + 9 povratkov (Zemelj 13/15 · Primostek 18 · Podzemelj 32 · Germ 28 · Otok 14 · Gradac 6 · Boginja vas 14 · h31/35/62) · **P136 LEAD: 1907 (glava s132; v1–v5 vidni; mejo s133+s134!)**`
      : p135Errors.join("; "),
  );
  }
  // ——— qa-p136: POROČNA KNJIGA 04455 — polno leto 1907 (P136; 22. leto poročne linije) ———
  {
  const p136Errors: string[] = [];
  // 1907 = 4 GRIBLJE poroke / 5 blokov
  if (p136Marr.length !== 5)
    p136Errors.push(`bloki 1907 (04455) ≠ 5 (${p136Marr.length} — 4 poroke: v4 1 + v5 2 + v9 1 + v11 1 = 5!)`);
  const p136Houses = p136Marr.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
  if (p136Houses.join(",") !== "3,6,6,7,19")
    p136Errors.push(`hiše 1907 ≠ [3,6×2,7,19] — najdeno: ${p136Houses.join(",")}`);
  // P136 pini (5 blokov)
  const p136Pins: Array<[string, string]> = [
    ["19", "1. POROČNI DOKAZ h19"], ["19", "NOVA HIŠA"], ["19", "HRANC"], ["19", "KLEPEC"], ["19", "OBA mladoletna"],
    ["6", "2. poročni dokaz h6"], ["6", "DRUBEL sosednjih hiš"], ["6", "DVE Kovač-družini na h6"],
    ["7", "3. poročni dokaz h7"],
    ["3", "20-LETNA LUKNJA"], ["3", "PEZDIREC-mreža"],
  ];
  for (const [n, pin] of p136Pins) {
    const blk = p136Marr.filter((h) => h.houseNo === n);
    if (blk.length === 0) {
      p136Errors.push(`pin ${n} (${pin}) — hiša ${n} ni med 1907 bloki`);
      continue;
    }
    if (!blk.some((cur) => cur.whatSi.toLowerCase().includes(pin.toLowerCase())))
      p136Errors.push(`pin hiša ${n} (${pin}) manjka`);
  }
  // duhovnik 1907: Rauy na vseh 5 GRIBLJE blokih (celotno leto: Rauy 11/12 + 1 [~ Pavlič?]!)
  const p136Rauy = p136Marr.filter((h) => h.whatSi.includes("Jos. Rauy")).length;
  if (p136Rauy !== 5)
    p136Errors.push(`Rauy 1907 blokov (GRIBLJE 5) ≠ 5 (${p136Rauy} — 1907 celotno: Rauy 11/12 + 1 ne-Rauy [~ Jos. Pavlič?] v7 — 1. ne-Rauy podpis 1907!)`);
  // ★ novele
  if (!p136Marr.some((h) => h.whatSi.includes("DISPENSA OD KRVNEGA SORODSTVA")))
    p136Errors.push("DISPENSA 2. kolena stranske vrste (ordinariat Ljubljana 28/8. 1907) manjka (v11 h6!)");
  if (!p136Marr.some((h) => h.whatSi.includes("2. BLOK hiše v letu")))
    p136Errors.push("2. BLOK hiše v letu (h6 v5+v11!) manjka");
  if (!p136Marr.some((h) => h.whatSi.includes("20-LETNA LUKNJA")))
    p136Errors.push("20-LETNA LUKNJA h3 manjka (v9!)");
  if (!p136Marr.some((h) => h.whatSi.includes("NOVA HIŠA")))
    p136Errors.push("NOVA HIŠA h19 manjka (v4 — 66. poročna hiša!)");
  // kumulativ: vitals 642 (637 + 5) + bloki 04455 125 + sidra 118
  if (HOUSE_VITALS.length !== 685)
    p136Errors.push(`HOUSE_VITALS ≠ 659 (${HOUSE_VITALS.length} — P137: 651; P138: + 8 blokov 1909 = 659!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length !== 168)
    p136Errors.push(`bloki 04455 ≠ 142 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length} — P136: 125; P137: + 9 blokov 1908 = 134!)`);
  push(
    "qa-p136-parish-marriage-1907",
    "P136: ŽUPNIJA PODZEMELJ — POROČNA KNJIGA 04455, POLNO LETO 1907 (issue #18; SAMPLE-TRANSCRIPTION-M1907; 22. leto poročne linije P115 = 1886 → … → P136 = 1907): okvir POTRJEN — s132–s134 == Pag. 131–133 (Pag. == sken − 1, **22. potrditev**; velja 61–133); **ROKOPISNA GLAVA »1907« POTRJENA na s132** (P135-lead!) + **ROKOPISNA GLAVA »1908« na s134 = P137 LEAD** (1908-v1 Jän 26 + v2 že vidna!); **P136-lead KOREKCIJE**: »min 5 vpisov s132« → **12 vpisov s132–s134** (2,4× podcenjeno — 22. leto zapored!) + **VSI lead-datumi NAPAČNI** (»Jän 13 · Jän 24? · Febr 14? · Mär 9? · Okt 6?« → pravilno **Jän 28 · Febr 4/11/18/25 · Mär 4 · Apr 22 · Mai 13 · Jun 3 · Jul 8 · Sep 16/30**); **1907 = 12 vpisov — ★ 12/12 PONEDELJKOV = 2. POPOLNO PONEDELJKOVSKO LETO** (po P134 11/11!; P135 je imel 10/12 + 2 nedelji); **VELIKE NOVELE P136**: **★ v11 DISPENSA OD KRVNEGA SORODSTVA V 2. KOLENU STRANSKE VRSTE** (od knj. čh. ordinarijata v LJUBLJANI od 28/8. 1907 — 1. dispensa po P134-1905! Mathäus Žugelj × Barbara Kovač = bratranci!) + **★ DVE KOVAČ-DRUŽINI NA GRIBLJE 6** (v5-ženin Franz oče Nicolaus + v11-nevesta Barbara oče Georg — brata?! **h6 = 2 bloka v enem letu**, 3. dokaz hiše po 1903 Jakobčič!) + **★ v5 GRIBLJE-DRUBEL h6 × h7** (sosednji hiši — 1. drubel po P135; h7 = 3. dokaz 1889+1900+1907!) + **★ 20-LETNA LUKNJA h3** (1887→1907 — 2. najdaljša po h21 [19 let]! v9-ženin Johann Pezdirec — PEZDIREC-družina NOVA veja: Griblje 20 → h3!) + **★ NOVA HIŠA h19** (v4-ženin Nikolaus **HRANC** [~] — 66. poročna hiša korpusa!) → **vitals 637 → 642; bloki 04455 120 → 125; sidra 113 → 118 (+1907:5); p80 hiše 65 → 66 (+h19); PT luknja 12 NESPREMENJENA** + **★ PEZDIREC-mreža ×5** (v3-mati Maria + v5-priča Martin + v6-nevesta Catharina [Germ 14 — 2. hiša vasi!] + v7-nevesta Anna [Primostek 17] + v9-ženin Johann [h3] — 4 veje priimka!) + **★ MUC-mreža ×3** (v2-ženin Johann [Primostek 8] + v2-nevesta Anna [Dobravice 20] — **ISTI PRIIMEK + ISTO IME OČETA (2× Nicolaus Muc!)** brez dispensa-zapisa! + v6-ženin Johannes [Vranoviče 8]) + **★ NOVAK-mreža ×3** (v7-ženin + v12-ženin + v12-mati) + **★ JAKŠA-mreža ×2** (v1-ženin Vojna vas 4 + v12-mati Maria Jakša) + **★ ŠARADINIČ 9-letna kontinuiteta h42** (1898 v26 Georg × Anna VERNIKMAN → 1907 v3 Georg × Maria VERNIKMAN — 1. priimek z 9-letno R-verigo! mati Anna→Maria [~ 2. žena?]) + **★ 1. NE-RAUY PODPIS 1907** (v7 [~ Jos. PAVLIČ?] — 2. gostujoči duhovnik linije [~]; primerjava s 4 Rauy-podpisi potrdila DRUGO roko! RAUY 11/12) + **★ pokojni oče Žugelj †** (v12 — 1. pokojni starš po P132; »des sehl. Jos.«) + **★ zglašnica št. 119** (v9 — občina DOBLIČE? [~] 1. pojav! najvišja številka leta!) + **★ 5 MLADOLETNIH NEVEST + 2 MLADOLETNA ŽENINA** (18–19/22–23 — rekord 7 mladoletniških dokumentov!) + **★ VOJNA VAS 4 pf. Črnomelj** (v1-ženin — 2. dokaz vasi; primerjalna forenzika z 1904-zapisom rešila branje!) + **★ LAHINJA [9?] pf. Črnomelj** (v8-nevesta — 2. vas fare + 1. dokument od ŽUPNEGA URADA V ČRNONELJU 9/5. 1907!) + KLEPEC ×3 (v4-nevesta + v8/v10-priči) + HLEBEC ×2 (v8-mati + v9-nevesta) + KRIŽAN ×2 (v5-nevesta + v1-mati) + ŽUGELJ ×2 v 2 tednih (v11-ženin + v12-nevesta!) + DORN ×2 v 2 dneh (v4/v5-materi — sestri? [~]) + ADLEŠIČ 1. priimek-oséba (v8-priča!) + STRAUS-priča (v4) + JAKOFČIČ-mati (v11) + POŽEK-mati (v10 — 18-letna kontinuiteta 1889!) + NOVI PRIIMKI: Hranc [~] · Legina [~ Leginov?] · Klobučar [~] · Šikorny [~] · Jakšević [~] · Mučič [~] · Vodlovnič? [~] + NOVE VASI/HIŠE: Vojna vas 4 · Vranoviče 1/5/8 · Dobravice 20 · Krasinec 4/10/12/36 · Germ 14 (2. hiša!) · Otok 16 · Primostek 8/17/28 · Lahinja [9?] pf. Črnomelj · Gradac 1/37 + metoda: PLAYWRIGHT-prenos skenov (fetch136.cjs — csrf+ctrl žetoni!) + primerjalna forenzika (1904-Vojna vas · 1898-Vernikman · 1898-Domušek · Rauy-podpisi) + ~70 VLM branj (3 renderinги); anomalije ×15; **P137 LEAD: poročna 1908 (rokopisna glava s134 y≈1020; 1908-v1 Jän 26 + v2 [Jän/Febr?] 26 že vidni — min 2 vpisa s134; LEKCIJA: mejo preveriti s135+s136!)**",
    "P136: THE PARISH OF PODZEMELJ — MARRIAGE REGISTER 04455, THE FULL YEAR 1907 (issue #18; SAMPLE-TRANSCRIPTION-M1907; the 22nd year of the marriage line P115 = 1886 → … → P136 = 1907): the frame CONFIRMED — s132–s134 == pages 131–133 (page == scan − 1, the 22nd confirmation; valid 61–133); **THE HANDWRITTEN HEADING »1907« CONFIRMED on s132** (the P135-lead!) + **THE HANDWRITTEN HEADING »1908« on s134 = the P137 LEAD** (the 1908-v1 Jan 26 + v2 already visible!); **THE P136-lead CORRECTIONS**: »min 5 entries s132« → **12 entries s132–s134** (2.4× underestimated — the 22nd consecutive year!) + **ALL the lead-dates WRONG** (→ correct: **Jan 28 · Feb 4/11/18/25 · Mar 4 · Apr 22 · May 13 · Jun 3 · Jul 8 · Sep 16/30**); **1907 = 12 entries — ★ 12/12 MONDAYS = THE 2ND PERFECT MONDAY YEAR** (after P134 11/11!; P135 had 10/12 + 2 Sundays); **THE BIG P136 NOVELS**: **★ the v11 DISPENSATION FROM THE BLOOD RELATIONSHIP IN THE 2ND DEGREE OF THE COLLATERAL LINE** (from the episcopal ordinariate in LJUBLJANA of Aug 28, 1907 — the 1st dispensation since P134-1905! Mathäus Žugelj × Barbara Kovač = cousins!) + **★ TWO KOVAČ FAMILIES AT GRIBLJE 6** (the v5 groom Franz father Nicolaus + the v11 bride Barbara father Georg — brothers?! **h6 = 2 blocks in one year**, the 3rd evidence after 1903 Jakobčič!) + **★ the v5 GRIBLJE DOUBLE h6 × h7** (neighboring houses — the 1st double since P135; h7 = the 3rd evidence 1889+1900+1907!) + **★ a 20-YEAR GAP h3** (1887→1907 — the 2nd longest after h21 [19 years]! the v9 groom Johann Pezdirec — the PEZDIREC family A NEW branch: Griblje 20 → h3!) + **★ A NEW HOUSE h19** (the v4 groom Nikolaus **HRANC** [~] — the 66th marriage house of the corpus!) → **vitals 637 → 642; the 04455 blocks 120 → 125; anchors 113 → 118 (+1907:5); p80 houses 65 → 66 (+h19); the PT gap 12 UNCHANGED** + **★ the PEZDIREC network ×5** (the v3 mother Maria + the v5 witness Martin + the v6 bride Catharina [Germ 14 — the 2nd house of the village!] + the v7 bride Anna [Primostek 17] + the v9 groom Johann [h3] — 4 branches!) + **★ the MUC network ×3** (the v2 groom Johann [Primostek 8] + the v2 bride Anna [Dobravice 20] — **THE SAME SURNAME + THE SAME FATHER'S NAME (2× Nicolaus Muc!)** without a dispensation note! + the v6 groom Johannes [Vranoviče 8]) + **★ the NOVAK network ×3** (the v7 groom + the v12 groom + the v12 mother) + **★ the JAKŠA network ×2** (the v1 groom Vojna vas 4 + the v12 mother Maria Jakša) + **★ the ŠARADINIĆ 9-year continuity h42** (1898 v26 Georg × Anna VERNIKMAN → 1907 v3 Georg × Maria VERNIKMAN — the 1st surname with a 9-year register chain! the mother Anna→Maria [~ a 2nd wife?]) + **★ the 1st NON-RAUY SIGNATURE 1907** (v7 [~ Jos. PAVLIČ?] — the 2nd visiting priest of the line [~]; the comparison with 4 Rauy signatures confirmed ANOTHER hand! RAUY 11/12) + **★ the deceased father Žugelj †** (v12 — the 1st deceased parent since P132; »des sehl. Jos.«) + **★ the banns certificate no. 119** (v9 — the DOBLIČE? [~] commune the 1st appearance! the highest number of the year!) + **★ 5 MINOR BRIDES + 2 MINOR GROOMS** (18–19/22–23 — a record 7 minority documents!) + **★ VOJNA VAS 4 pf. Črnomelj** (the v1 groom — the 2nd evidence of the village; the comparative forensics with the 1904 entry solved the reading!) + **★ LAHINJA [9?] pf. Črnomelj** (the v8 bride — the 2nd village of the parish + the 1st document from the PARISH OFFICE IN ČRNOMELJ May 9, 1907!) + KLEPEC ×3 (the v4 bride + the v8/v10 witnesses) + HLEBEC ×2 (the v8 mother + the v9 bride) + KRIŽAN ×2 (the v5 bride + the v1 mother) + ŽUGELJ ×2 in 2 weeks (the v11 groom + the v12 bride!) + DORN ×2 in 2 days (the v4/v5 mothers — sisters? [~]) + ADLEŠIČ the 1st person-surname (the v8 witness!) + the STRAUS witness (v4) + the JAKOFČIČ mother (v11) + the POŽEK mother (v10 — an 18-year continuity since 1889!) + NEW SURNAMES: Hranc [~] · Legina [~ Leginov?] · Klobučar [~] · Šikorny [~] · Jakšević [~] · Mučič [~] · Vodlovnič? [~] + NEW VILLAGES/HOUSES: Vojna vas 4 · Vranoviče 1/5/8 · Dobravice 20 · Krasinec 4/10/12/36 · Germ 14 (the 2nd house!) · Otok 16 · Primostek 8/17/28 · Lahinja [9?] pf. Črnomelj · Gradac 1/37 + the method: the PLAYWRIGHT scan downloads (fetch136.cjs — the csrf+ctrl tokens!) + comparative forensics (1904 Vojna vas · 1898 Vernikman · 1898 Domušek · the Rauy signatures) + ~70 VLM readings (3 renderings); anomalies ×15; **THE P137 LEAD: the marriages of 1908** (the handwritten heading s134 y≈1020; the 1908-v1 Jan 26 + v2 [Jan/Feb?] 26 already visible — min 2 entries s134; THE LESSON: check the boundary s135+s136!)",
    p136Errors.length === 0,
    p136Errors.length === 0
      ? `12 vpisov (lead 2,4× podcenjen — VSI lead-datumi napačni!) · s132–s134 == Pag. 131–133 (22. potrditev!) · **★ 12/12 PONEDELJKOV = 2. POPOLNO LETO (po P134!)** · **★ DISPENSA 2. kolena (ordinariat LJUBLJANA 28/8. 1907 — v11!)** · **★ 2 KOVAČ-družini na h6 (Nicolaus+Georg!) = 2 bloka v letu** · **★ GRIBLJE-DRUBEL h6×h7 (v5!)** · **★ 20-LETNA LUKNJA h3 (v9 Pezdirec!)** · **★ NOVA hiša h19 (v4 Hranc [~])** → vitals 642 · bloki 125 · sidra 118 (+1907:5) · p80 hiše 66 (+h19) · **★ PEZDIREC ×5 + MUC ×3 + NOVAK ×3 + ŠARADINIČ 9-let h42 + 1. ne-Rauy [~ Pavlič?] + pokojni oče † + št. 119 + 7 mladoletniških dokumentov** · **P137 LEAD: 1908 (glava s134; v1+v2 vidni; mejo s135+s136!)**`
      : p136Errors.join("; "),
  );
  }
  // ——— qa-p137: POROČNA KNJIGA 04455 — polno leto 1908 (P137; 23. leto poročne linije) ———
  {
  const p137Errors: string[] = [];
  // 1908 = 6 GRIBLJE oseb / 9 blokov
  if (p137Marr.length !== 9)
    p137Errors.push(`bloki 1908 (04455) ≠ 9 (${p137Marr.length} — 6 oseb: v1 2 + v5 1 + v9 1 + v10 2 + v14 1 + v17 2 = 9!)`);
  const p137Houses = p137Marr.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
  if (p137Houses.join(",") !== "14,14,21,28,33,39,43,44,62")
    p137Errors.push(`hiše 1908 ≠ [14×2,21,28,33,39,43,44,62] — najdeno: ${p137Houses.join(",")}`);
  // P137 pini (9 blokov)
  const p137Pins: Array<[string, string]> = [
    ["21", "19-LETNA LUKNJA"], ["21", "RECIPROČNA"], ["21", "ISTI KOT 1889-v3"],
    ["62", "5. poročni dokaz h62"], ["62", "KURE-kontinuiteta"],
    ["28", "1. POROČNI DOKAZ h28"], ["28", "RAZVEZAN"], ["28", "Milkovič"],
    ["43", "NOVA HIŠA"], ["43", "LASIČ"], ["43", "ŽUPANIČ"],
    ["39", "2. poročni dokaz h39"], ["39", "DRUBEL"],
    ["44", "3. poročni dokaz h44"], ["44", "krst 1887"],
    ["33", "20 LETIH"], ["33", "DEHLIČ × DEHLIČ"],
    ["14", "INTRA-HIŠNA POROKA"], ["14", "AFINITETNA DISPENSA"], ["14", "SESTRA pokojne žene"], ["14", "ISTEGA"],
  ];
  for (const [n, pin] of p137Pins) {
    const blk = p137Marr.filter((h) => h.houseNo === n);
    if (blk.length === 0) {
      p137Errors.push(`blok hiše ${n} (1908) manjka`);
      continue;
    }
    if (!blk.some((cur) => cur.whatSi.toLowerCase().includes(pin.toLowerCase())))
      p137Errors.push(`pin hiša ${n} (${pin}) manjka`);
  }
  // duhovnik 1908: Rauy na 6 od 9 blokov (celotno leto: Rauy dominant + novi kaplan Jos. Dami [~]!)
  const p137Rauy = p137Marr.filter((h) => h.whatSi.includes("Jos. Rauy")).length;
  if (p137Rauy !== 7)
    p137Errors.push(`Rauy 1908 blokov (GRIBLJE) ≠ 7 (${p137Rauy} — 1908: Rauy dominant + novi kaplan Jos. Dami [~] (krstna linija P103!) — v10+v10-bride [Dami?]!)`);
  // ★ novele
  if (!p137Marr.some((h) => h.whatSi.includes("INTRA-HIŠNA POROKA")))
    p137Errors.push("★★ INTRA-HIŠNA POROKA h14 × h14 (v17 — 1. v 23 letih!) manjka");
  if (!p137Marr.some((h) => h.whatSi.includes("RAZVEZAN")))
    p137Errors.push("★★ 1. RAZVEZA LINIJE (v5 modri zapis!) manjka");
  if (!p137Marr.some((h) => h.whatSi.includes("AFINITETNA DISPENSA")) && !p137Marr.some((h) => h.whatSi.includes("AFINITETE")))
    p137Errors.push("★★ AFINITETNA DISPENSA 1. kolena (v17 — sestra pokojne žene!) manjka");
  if (!p137Marr.some((h) => h.whatSi.includes("NOVA HIŠA")))
    p137Errors.push("NOVA HIŠA h43 manjka (v9 — 67. poročna hiša korpusa!)");
  if (!p137Marr.some((h) => h.whatSi.includes("hčerka krščena 16. 2. 1908")))
    p137Errors.push("★★ hčerka krščena PRED poroko (16. 2. 1908 = P103 cross-link!) manjka (v17!)");
  // kumulativ: vitals 651 (642 + 9) + bloki 04455 134 + sidra 127
  if (HOUSE_VITALS.length !== 685)
    p137Errors.push(`HOUSE_VITALS ≠ 659 (${HOUSE_VITALS.length} — P137: 651; P138: + 8 blokov 1909 = 659!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length !== 168)
    p137Errors.push(`bloki 04455 ≠ 142 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length} — P136: 125; P137: + 9 blokov 1908 = 134!)`);
  push(
    "qa-p137-parish-marriage-1908",
    "P137: ŽUPNIJA PODZEMELJ — POROČNA KNJIGA 04455, POLNO LETO 1908 (issue #18; SAMPLE-TRANSCRIPTION-M1908; 23. leto poročne linije P115 = 1886 → … → P137 = 1908): okvir POTRJEN — s134–s138 == Pag. 133–137 (Pag. == sken − 1, **23. potrditev**; velja 61–137); **ROKOPISNA GLAVA »1908« NA DNU s134 (y≈980) POTRJENA** (P136-lead!) + ponavljajoče glave na s135–s138 + **ROKOPISNA GLAVA »1909« na s138 (y≈600) = P138 LEAD** (1909-v1 Jän 25 + v2 Febr 8 + v3 März 15 + v4 Febr 21 že vidni!); **P137-lead KOREKCIJA**: »min 2 vpisa s134« → **17 vpisov** (8,5× POCENJEN — 23. leto zapored!); **1908 = 17 vpisov** = 26. januar ×2 + 3. februar + [9.?] februar + **10. februar ×3 (MASA!)** + 17. februar ×2 + 2. marec ×2 + 18. maj + 1. junij + 22. junij + 13. september + 25. oktober + [25.?] november — **11 ponedeljkov + 4–5 NEDELJ** (v1+v2 ISTI DAN 26. 1.!); **VELIKE NOVELE P137**: **★★★ v17 INTRA-HIŠNA POROKA h14 × h14 — 1. V 23 LETIH LINIJE!** (ženin Johann BRINEC = **1895-v17 ISTI** (33 → 46 let; starši Peter Brinec × Anna Štraus ISTI!) — 1. žena Maria Pezdirec † → poroči **SESTRO pokojne žene** Dorotheo Pezdirec (27; starša Michael Pezdirec × Anna Brinec = 1895 nevestina starša ISTA!) = **★★ AFINITETNA DISPENSA 1. KOLENA** (sororate — najhujša sorodstvena zapreka linije! ordinariat Ljubljana [22. 10. 1908 št. 10.350? ~] + [vlada? ~]) + **★★ hčerka krščena 16. 2. 1908 na h14 (P103: oče Janez Brinec × Doroteja Perdinec!) — 9 MESECEV PRED poroko!**) + **★★ v16 73-LETNI ŽENIN = NOVI REKORD LINIJE** (prej 62 P135-v10! +11 let; Štefan PAŠIČ? [~] × Maria [Jopčič? ~] 62 Gradac 49 — 135 let para = premik rekorda 134 iz 1898!) + **★★ 4 DISPENZE V LETU** (v3 3. koleno št. 265 + v5 [3. koleno?] + v15 [št. 4208? ~] + v17 afiniteta — vs 1 v 1907!) + **★★ v5 1. RAZVEZANI ŽENIN LINIJE** (Georg Žarkovič [~] — modri zapis: 1. zakon razvezan [sodba ~ Novo mesto?]; 1886–1908 brez razvez!) + **★ v1 RECIPROČNA POROKA** (Johann POŽEK 58 h21 [**= 1889-v3 ženin ISTI!** starši ISTI!] × Catharina KURE 28 h62 [sestra 1906-v11 ženina!] — zrcalni par po Kure × Požek 1906!) + **★ v10 GRIBLJE-DRUBEL h39 × h44** (Johann ŠIMEC [brat 1897-v11 neveste; starši ISTI!] × Barbara KLOBUČAR [1887-krst h47 ISTA — Peter Klobučar × Marija Tilak/Filath!] — 2. drubel zapored!) + **★ v14 DEHLIČ × DEHLIČ istopriimčna** (Thomas Krasinec 53 × Catharina **GRIBLJE 33 = ISTA DRUŽINA kot 1888-v2 po 20 LETIH** (Mathias Dehlič × Maria Husič!) — 2. najdaljša kontinuiteta!) + **★ v9 NOVA HIŠA h43** (nevesta Maria Lasič [~] — 67. poročna hiša korpusa! PT luknja 12 → 13!) + **★ NOVI DUHOVNIK Jos. DAMI [~]** (krstna linija P103 1908! — [Danijel?/Wandl?/Ludl? ~] = verjetno vsi Dami! RAUY dominant) + **★ NOVE VASI**: Mehovce 10 **pf. PODGRAD** (v4 — nova fara!) · **DRAŠIČI 24** (v15 — 1. pojav! Metlika-okolica) · Žaloka im [Kroatien? ~] (v6 — 1. ženin rojen na Hrvaškem? javni + krščeni list!) + POVRATKI: Cerkvišče 35/10 (1905!) · Kapljišče? [9 ~] (1905!) · Krasinec 18 (1897 Županič!) · Vranoviče 29 (1890-e!) · Otok 22 (1895 Zuglji!) · h21 (1889→1908 = 19 let!) · h28 (krst 1891→poroka = 17 let!) · h39 (1897) · h44 (1899/1903) · h62 (1906) · h14 (1895) · h33 (1888) + KRIŽAN ×3 (v1-mati + v7-mati + v13-ženin!) + MUC ×3 (v2-priča + v7-mati + v12-priča) + ŽUGELJ ×2 (1907 ×2 → 1908 v6-nevesta!) + PEZDIREC ×2 (v15-nevesta Drašiči + v17!) + PAPIČ (v13-mati = h3-družina!) + KRAMARIČ (v9-mati korpus ×10!) + SLOBODNIK (v13-priča ~ 1905-korpus!) + NOVI PRIIMKI: Žarkovič · Vancas [~] · Šustarvič [~] · Schweiger · Vovkman [~] · Lasič [~] · Hlešič · Bajuk (zenin!) · Krudl [~] · Pašič/Pavšič [~] · Jopčič [~] · Zunič [~] · Dauovič [~] · Petschauer · Kumpf [~] · Planinec [~] · Čiha [~] · Gustin [~] + MASA 10. 2. ×3 (v5+v6+v7!) + zglašnica Griblje št. 1 ×2 (25/1 + 15/10!) + vlada št. 4167 (v10 — mladoletna nevesta 20!) + 6 mladoletniških dokumentov (v3+v6+v8+v10+v12+v13!) + [Uredovna svjedoljba? Poglavarstva ~ v Ribnici? — NOV TIP DOKUMENTA? ~ v14 br. 1555!] + METODA: 150+ VLM branj + korpus-forenzika (1889-ženič ISTI! 1887-krst ISTA! 1895-par ISTI! 1888-družina ISTA!) + s135R 5-vrstični zamik rešen vsebinsko (zglasnica-avtoritete!); anomalije ×21; **P138 LEAD: poročna 1909 (rokopisna glava s138 y≈600 + 1909-v1 Jän 25 + v2 Febr 8 + v3 März 15 + v4 Febr 21 vidni — min 4 vpisi; LEKCIJA: mejo preveriti s139+s140!; knjiga 04455 sega do 1922 — še ~14 let linije!)**",
    "P137: THE PARISH OF PODZEMELJ — MARRIAGE REGISTER 04455, THE FULL YEAR 1908 (issue #18; SAMPLE-TRANSCRIPTION-M1908; the 23rd year of the marriage line P115 = 1886 → … → P137 = 1908): the frame CONFIRMED — s134–s138 == pages 133–137 (page == scan − 1, the **23rd confirmation**; valid 61–137); **THE HANDWRITTEN HEADING »1908« AT THE BOTTOM of s134 (y≈980) CONFIRMED** (the P136-lead!) + repeating headings on s135–s138 + **THE HANDWRITTEN HEADING »1909« on s138 (y≈600) = the P138 LEAD** (the 1909-v1 Jan 25 + v2 Feb 8 + v3 Mar 15 + v4 Feb 21 already visible!); **THE P137-lead CORRECTION**: »min 2 entries s134« → **17 entries** (8.5× UNDERESTIMATED — the 23rd consecutive year!); **1908 = 17 entries** — **11 Mondays + 4–5 SUNDAYS** (v1+v2 the SAME DAY Jan 26!); **THE BIG P137 NOVELS**: **★★★ the v17 INTRA-HOUSE WEDDING h14 × h14 — the 1st in 23 years of the line!** (the groom Johann BRINEC = **the 1895-v17 same** (33 → 46 years; the parents Peter Brinec × Anna Štraus the same!) — the 1st wife Maria Pezdirec † → he marries **the SISTER of the deceased wife** Dorothea Pezdirec (27; the parents Michael Pezdirec × Anna Brinec = the 1895 bride's parents the same!) = **★★ the AFFINITY DISPENSATION of the 1st DEGREE** (sororate — the gravest impediment of the line! the Ljubljana ordinariate [Oct 22, 1908 no. 10.350? ~] + [the government? ~]) + **★★ a daughter baptized Feb 16, 1908 at h14 (P103: father Janez Brinec × Doroteja Perdinec!) — 9 MONTHS BEFORE the wedding!**) + **★★ the v16 73-YEAR-OLD GROOM = THE NEW RECORD OF THE LINE** (previously 62 P135-v10! +11 years; Štefan PAŠIČ? [~] × Maria [Jopčič? ~] 62 Gradac 49 — 135 years of the couple = beating the 134 record of 1898!) + **★★ 4 DISPENSATIONS IN THE YEAR** (v3 3rd degree no. 265 + v5 [3rd degree?] + v15 [no. 4208? ~] + v17 affinity — vs 1 in 1907!) + **★★ the v5 1st DIVORCED GROOM OF THE LINE** (Georg Žarkovič [~] — a blue note: the 1st marriage dissolved [a judgment ~ Novo mesto?]; 1886–1908 without divorces!) + **★ the v1 RECIPROCAL WEDDING** (Johann POŽEK 58 of h21 [**= the 1889-v3 groom the same!** the parents the same!] × Catharina KURE 28 of h62 [the sister of the 1906-v11 groom!] — the mirror pair after Kure × Požek 1906!) + **★ the v10 GRIBLJE DOUBLE h39 × h44** (Johann ŠIMEC [the brother of the 1897-v11 bride; the parents the same!] × Barbara KLOBUČAR [the 1887 baptism h47 the same — Peter Klobučar × Marija Tilak/Filath!] — the 2nd double in a row!) + **★ the v14 DEHLIČ × DEHLIČ same-surname** (Thomas of Krasinec 53 × Catharina **GRIBLJE 33 = the SAME FAMILY as 1888-v2 after 20 YEARS** (Mathias Dehlič × Maria Husič!) — the 2nd longest continuity!) + **★ the v9 NEW HOUSE h43** (the bride Maria Lasič [~] — the 67th marriage house of the corpus! the PT gap 12 → 13!) + **★ THE NEW PRIEST Jos. DAMI [~]** (the baptism line P103 1908! — [Danijel?/Wandl?/Ludl? ~] = probably all Dami! RAUY dominant) + **★ NEW VILLAGES**: Mehovce 10 **pf. PODGRAD** (v4 — a new parish!) · **DRAŠIČI 24** (v15 — the 1st appearance!) · Žaloka in [CROATIA? ~] (v6 — the 1st groom born in Croatia? a civil + baptismal certificate!) + RETURNS: Cerkvišče 35/10 (1905!) · Kapljišče? [9 ~] (1905!) · Krasinec 18 (1897 Županič!) · Vranoviče 29 (the 1890s!) · Otok 22 (1895 the Zugelj family!) · h21 (1889→1908 = 19 years!) · h28 (baptism 1891→marriage = 17 years!) · h39 (1897) · h44 (1899/1903) · h62 (1906) · h14 (1895) · h33 (1888) + KRIŽAN ×3 (the v1 mother + the v7 mother + the v13 groom!) + MUC ×3 (the v2 witness + the v7 mother + the v12 witness) + ŽUGELJ ×2 (1907 ×2 → the 1908 v6 bride!) + PEZDIREC ×2 (the v15 bride of Drašiči + v17!) + PAPIČ (the v13 mother = the h3 family!) + KRAMARIČ (the v9 mother in the corpus ×10!) + SLOBODNIK (the v13 witness ~ the 1905 corpus!) + NEW SURNAMES: Žarkovič · Vancas [~] · Šustarvič [~] · Schweiger · Vovkman [~] · Lasič [~] · Hlešič · Bajuk (the groom!) · Krudl [~] · Pašič/Pavšič [~] · Jopčič [~] · Zunič [~] · Dauovič [~] · Petschauer · Kumpf [~] · Planinec [~] · Čiha [~] · Gustin [~] + the MASS Feb 10 ×3 (v5+v6+v7!) + the Griblje certificate no. 1 ×2 (Jan 25 + Oct 15!) + the government no. 4167 (v10 — an underage bride of 20!) + 6 minority documents + [an official certificate of the municipality ~ of Ribnica? — a NEW document type? ~ v14 no. 1555!] + the METHOD: 150+ VLM readings + corpus forensics (the 1889 groom the same! the 1887 baptism the same! the 1895 couple the same! the 1888 family the same!) + the s135R 5-row shift solved by content (the certificate authorities!); anomalies ×21; **THE P138 LEAD: the marriages of 1909** (the handwritten heading s138 y≈600 + the 1909-v1 Jan 25 + v2 Feb 8 + v3 Mar 15 + v4 Feb 21 visible — min 4 entries; THE LESSON: check the boundary s139+s140!; the book 04455 extends to 1922 — ~14 more years of the line!)",
    p137Errors.length === 0,
    p137Errors.length === 0
      ? `17 vpisov (lead 8,5× podcenjen — 23. leto!) · s134–s138 == Pag. 133–137 (23. potrditev!) · **★ 11 ponedeljkov + 4–5 NEDELJ (v1+v2 isti dan!)** · **★★★ INTRA-HIŠNA POROKA h14×h14 (v17 — 1. v 23 letih!) + AFINITETNA DISPENSA 1. kolena (sestra pokojne žene!) + hčerka 9 mesecev PRED poroko (P103!)** · **★★ 73-LETNI ŽENIN = REKORD (v16 — prej 62!)** · **★★ 4 DISPENZE v letu (v3+v5+v15+v17!)** · **★★ 1. RAZVEZA (v5 modri zapis!)** · **★ RECIPROČNA Požek×Kure (v1 — 1889-ženin ISTI!) + DRUBEL h39×h44 (v10 — 1887-krst ISTA!) + DEHLIČ×DEHLIČ (v14 — 1888-družina ISTA 20 let!) + NOVA hiša h43 (v9)** → vitals 651 · bloki 134 · sidra 127 (+1908:9) · p80 hiše 67 (+h43) · PT luknja 13 · **★ NOVI DUHOVNIK Jos. Dami [~]** · **P138 LEAD: 1909 (glava s138; v1–v4 vidni; mejo s139+s140!)**`
      : p137Errors.join("; "),
  );
  }
  // ——— qa-p138: POROČNA KNJIGA 04455 — polno leto 1909 (P138; 24. leto poročne linije) ———
  {
  const p138Errors: string[] = [];
  // 1909 = 5 GRIBLJE porok / 8 blokov (№1 1 + №6 2 + №8 1 + №11 2 + №13 2)
  const p138Marr = HOUSE_VITALS.filter((h) => h.bookSignature === "04455" && h.year === 1909);
  if (p138Marr.length !== 8)
    p138Errors.push(`bloki 1909 (04455) ≠ 8 (${p138Marr.length} — 5 oseb: №1 1 + №6 2 + №8 1 + №11 2 + №13 2 = 8!)`);
  const p138Houses = p138Marr.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
  if (p138Houses.join(",") !== "1,17,29,30,46,46,57,74")
    p138Errors.push(`hiše 1909 ≠ [1,17,29,30,46×2,57,74] — najdeno: ${p138Houses.join(",")}`);
  // P138 pini (8 blokov)
  const p138Pins: Array<[string, string]> = [
    ["17", "2. poročni dokaz h17"], ["17", "17-LETNA LUKNJA"], ["17", "KRALJ"],
    ["74", "2. poročni dokaz h74"], ["74", "KAMBIČ"],
    ["30", "3. poročni dokaz h30"], ["30", "MILEK-kontinuiteta"],
    ["57", "1. POROČNI DOKAZ h57"], ["57", "PEZDIREC"], ["57", "1888"],
    ["46", "INTRA-HIŠNA POROKA"], ["46", "DISPENSA 3. KOLENA"], ["46", "KLOBUČAR"], ["46", "FILAK"],
    ["1", "3. poročni dokaz h1"], ["1", "TOME"],
    ["29", "3. poročni dokaz h29"], ["29", "KURE"], ["29", "SPREGLED"],
  ];
  for (const [n, pin] of p138Pins) {
    const blk = p138Marr.filter((h) => h.houseNo === n);
    if (blk.length === 0) {
      p138Errors.push(`blok hiše ${n} (1909) manjka`);
      continue;
    }
    if (!blk.some((cur) => cur.whatSi.toLowerCase().includes(pin.toLowerCase())))
      p138Errors.push(`pin hiša ${n} (${pin}) manjka`);
  }
  // duhovnik 1909: Rauy na 6 od 8 blokov (№11 + №13-bloka brez Rauy: Gregor Petar? + Pavlič?!)
  const p138Rauy = p138Marr.filter((h) => h.whatSi.includes("Jos. Rauy")).length;
  if (p138Rauy !== 5)
    p138Errors.push(`Rauy 1909 blokov (GRIBLJE) ≠ 5 (${p138Rauy} — 1909: Rauy 5/8 + Gregor Petar? [~ №8] + Jos. Pavlič? [~ №13 ×2]!)`);
  // ★ novele
  if (!p138Marr.some((h) => h.whatSi.includes("INTRA-HIŠNA POROKA")))
    p138Errors.push("★★★ INTRA-HIŠNA POROKA h46 × h46 (№11 — 2. v 2 letih!) manjka");
  if (!p138Marr.some((h) => h.whatSi.includes("DISPENSA 3. KOLENA")))
    p138Errors.push("★★ DISPENSA 3. KOLENA (№11 ordinariat št. 4571) manjka");
  if (!p138Marr.some((h) => h.whatSi.includes("SPREGLED")))
    p138Errors.push("★★ SPREGLED 3. KOLENA (№13 ordinariat št. 4995 — TOME×TOME!) manjka");
  if (!p138Marr.some((h) => h.whatSi.includes("1. POROČNI DOKAZ h57")))
    p138Errors.push("★ 1. POROČNI DOKAZ h57 (Pezdirec-kriste 1888–1899 → poroka 1909!) manjka");
  if (HOUSE_VITALS.length !== 685)
    p138Errors.push(`HOUSE_VITALS ≠ 659 (${HOUSE_VITALS.length} — P137: 651; P138: + 8 blokov 1909 = 659!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length !== 168)
    p138Errors.push(`bloki 04455 ≠ 142 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length} — P137: 134; P138: + 8 blokov 1909 = 142!)`);
  push(
    "qa-p138-parish-marriage-1909",
    "P138: ŽUPNIJA PODZEMELJ — POROČNA KNJIGA 04455, POLNO LETO 1909 (issue #18; SAMPLE-TRANSCRIPTION-M1909; 24. leto poročne linije P115 = 1886 → … → P138 = 1909): okvir POTRJEN — s138–s141 == Pag. 137–140 (Pag. == sken − 1, **24. potrditev**; velja 61–140); **LETNICA 1909 SE PIŠE V VSAKEM VPISU — NI samostojne letne glave** (P137-lead »glava s138 y≈600« = prvi vpis №1 — nova lekcija: ponavljajoče letnice ≠ letna glava!); **P138-lead KOREKCIJA**: »min 4 vpisi« → **15 vpisov** (3,75× POCENJEN — 24. leto zapored!); **1909 = 15 vpisov** (№1–№4 s138 + №5–№8 s139 + NEŠTEVILČEN 5. 7. + №8–№12 s140 + №13–№14 s141 — leto ČEZ 4 STRANI! meja 1909/1910 na s141: №14 zadnji 1909 + №1 1910 = P139 lead!) — **14 PONEDDELJKOV + 1 NEDELJA = 93% PON (REKORD LINIJE!** 1907: 12/12 = 100% a 12 vpisov; 1908: 11/17) + 22. 11. ×2 isti dan (№13+№14!); **VELIKE NOVELE P138**: **★★★ №11 INTRA-HIŠNA POROKA h46 × h46 + DISPENSA 3. KOLENA enake stranske stopnje** (ordinariat Ljubljana 12/10 1909 št. 4571 — Žugelj × Klobučar IZ ISTE HIŠE! 2. intra-hišna v 2 letih po h14×h14 1908!; priča Nicolaus FILAK = 1898-v20 ženin h46 — 11-letna kontinuiteta!; KLOBUČAR-h46: 1898-v20 → 1909 = 11 let!) + **★★★ №14 SPREGLED 1. KOLENA + SODNO DOVOLJENJE** (ordinariat 22/10 1909 št. 4786 + deželno sodišče Ljubljana 11/11 1909 št. 27036 — DVOJNA zapreka!; priča Mathias Jakljič = №12 ženin 13 dni po lastni poroki!) + **★★ №13 SPREGLED 3. KOLENA dotikajočega se 2. kolena** (ordinariat 9/11 1909 št. 4995 — ženin TOME × nevestina mati geb. TOME: sorodstvo po krvi IN afiniteta!; priči Tome + Kure = priimka OBEH družin!) + **★★ NEŠTEVILČEN VPIS 5. 7. = VOJAŠKA POROKA Z DELEGACIJO** (k.k. pehotni polk št. 9 Heiratsbewilligung 22/6 1909 št. 2045 + dekanat 30/6 + delegacija na kopulacijo 4/7 Z. 200 — poroka po pooblaščencu, 1. popolnoma nemški listinski vpis!; Josef Skorpil? [~] × Ana Lopašič [~] 33 — nevesta starejša 8 let!) + **★★ 2 GENDARMSKI POROKI** (№7 Johann [Paul?/Favornik? ~] Titular-Wachtmeister k.k. Gendarmerie + №9 Alois MAVSAR k.k. Gendarm — + 2 gendarmski priči Horvat + Lecher!) + **★ №8 NOVA HIŠA h57** (68. poročna hiša korpusa! Maria PEZDIREC — oče Peter = 1891-v7 ženin h20! 3. Pezdirec-hiša: h20+h87+h57!) + **★ №4 ženin LEDIG 63** (Mathias Kambič × Anna Berkopec 58 = par 121 let — 2. najstarejši po 1908-v16 135!) + **★ NOVE OBLASTI**: VIDEM + DOBREPOLJE + RUDOLFŠTAT/Novo mesto (№9 listine — 1. pojavi!) + **★ ~27 NOVIH PRIIMKOV** (Stabjan · Matković · Berkopec · Mušič · Skorpil? · Lopašič? · Mavretič · Mavsar · Mavrtič? · Štefanič · Tome · Gregorič · Zakša? · Favornik? · Malevič? · Skala? · Pirc · Milavec · Maravičič? · Pečarič · Čalkovič? · Horvat · Lecher · Zare? · Gnaubrijan? · Koharič? · Krajcovič? · Stipanič?) + **★ NOVI DUHOVNIKI** Gregor Petar? [O.T. coop. ~] + Jos. Pavlič? [~] + Danijel (2. pojav; Rauy 11–12/15 dominant) + **GRIBLJE-mreže leta**: KAMBIČ ×3 (№2+№4 Krasinec + №6 h74!) · ŽUGELJ ×3 (№5 Otok + №10 Dobravice + №11 h46!) · MILEK ×3 (№6 nevesta h30 + №11 mati + №13-h29 hišna!) · KALJ ×4 (№1+№11+№12!) · KURE ×2 (№13 + priči!) + POVRATKI: h17 (1892 Kralj → 1909 hči?) · h74 (1893 Kambič!) · h30 (1889+1897 Milek!) · h46 (1898 Klobučar+FILAK!) · h1 (1899 Kure×Željko!) · h29 (1897 Milek → Kure menjava!) + METODA: 42+27 VLM branj (5 FAZA-1 + 2 FAZA-1b + 5 datumskih zoomov + 30 vrstičnih + 27 verif-zoomov №/imena/vasi!) + №-stolpčni pasovni branjа (štetje 5–8 + neštevilčen + 1910 №1!) + korpus-forenzika (h17/h29/h30/h46/h74 kontinuitete!) + STRUKTURNA LEKCIJA: pas 1 s139/s140 = PRAZNA vrstica + tiskane glave (NE vpis — prva branjа halucinirala iz priimkov v promptu!); anomalije ×17; **P139 LEAD: poročna 1910 (№1 na s141: Mathias JAKOBČIČ? [~] × Marija JAKOBČIČ? [~] — INTRA-PRIIMEK + mati PEZDIREC + mati ŽELJKO/Žugelj + dispenza 3. kolena ordinariat 13/1 1910 št. 159 + zglašnica [Okriblo?] 22/1 1910 št. 81!**)",
    "P138: THE PARISH OF PODZEMELJ — MARRIAGE REGISTER 04455, THE FULL YEAR 1909 (issue #18; SAMPLE-TRANSCRIPTION-M1909; the 24th year of the marriage line P115 = 1886 → … → P138 = 1909): the frame CONFIRMED — s138–s141 == pages 137–140 (page == scan − 1, the **24th confirmation**; valid 61–140); **THE YEAR 1909 IS WRITTEN IN EVERY ENTRY — NO standalone year heading** (the P137-lead »heading s138 y≈600« = the first entry №1 — a new lesson: repeating year notes ≠ a year heading!); **THE P138-lead CORRECTION**: »min 4 entries« → **15 entries** (3.75× UNDERESTIMATED — the 24th consecutive year!); **1909 = 15 entries** — **14 Mondays + 1 Sunday = 93% MON (THE LINE RECORD!** 1907: 12/12 = 100% but 12 entries; 1908: 11/17) + Nov 22 ×2 the same day (№13+№14!); **THE BIG P138 NOVELS**: **★★★ the №11 INTRA-HOUSE WEDDING h46 × h46 + the DISPENSATION of the 3rd DEGREE of the equal lateral line** (the Ljubljana ordinariate Oct 12, 1909 no. 4571 — Žugelj × Klobučar FROM THE SAME HOUSE! the 2nd intra-house in 2 years after the 1908 h14×h14!; the witness Nicolaus FILAK = the 1898-v20 groom of h46 — an 11-year continuity!; the KLOBUČAR-h46: 1898-v20 → 1909 = 11 years!) + **★★★ the №14 DISPENSATION of the 1st DEGREE + A COURT PERMIT** (the ordinariate Oct 22, 1909 no. 4786 + the provincial court of Ljubljana Nov 11, 1909 no. 27036 — a DOUBLE impediment!; the witness Mathias Jakljič = the №12 groom 13 days after his own wedding!) + **★★ the №13 DISPENSATION of the 3rd DEGREE touching the 2nd degree** (the ordinariate Nov 9, 1909 no. 4995 — the groom TOME × the bride's mother née TOME: consanguinity AND affinity!; the witnesses Tome + Kure = the surnames of BOTH families!) + **★★ the UNNUMBERED ENTRY Jul 5 = A MILITARY WEDDING BY DELEGATION** (the k.k. infantry regiment no. 9 marriage permit Jun 22, 1909 no. 2045 + the deanery Jun 30 + the delegation to copulate Jul 4 Z. 200 — a wedding by proxy, the 1st fully German documents entry!) + **★★ 2 GENDARMERIE WEDDINGS** (№7 a Titular-Wachtmeister of the k.k. Gendarmerie + №9 Alois MAVSAR a k.k. gendarme — + 2 gendarme witnesses Horvat + Lecher!) + **★ the №8 NEW HOUSE h57** (the 68th marriage house of the corpus! Maria PEZDIREC — the father Peter = the 1891-v7 groom of h20! the 3rd Pezdirec house: h20+h87+h57!) + **★ the №4 groom SINGLE at 63** (Mathias Kambič × Anna Berkopec 58 = a 121-year couple — the 2nd oldest after the 1908-v16 135!) + **★ NEW AUTHORITIES**: VIDEM + DOBREPOLJE + RUDOLFŠTAT/Novo mesto (the №9 documents — the 1st appearances!) + **★ ~27 NEW SURNAMES** + **★ NEW PRIESTS** Gregor Petar? [O.T. coop. ~] + Jos. Pavlič? [~] + Danijel (the 2nd appearance; Rauy 11–12/15 dominant) + the GRIBLJE networks of the year: KAMBIČ ×3 · ŽUGELJ ×3 · MILEK ×3 · KALJ ×4 · KURE ×2 + RETURNS: h17 (1892 Kralj!) · h74 (1893 Kambič!) · h30 (1889+1897 Milek!) · h46 (1898 Klobučar+FILAK!) · h1 (1899 Kure×Željko!) · h29 (1897 Milek → the Kure change!) + the METHOD: 42+27 VLM readings + the No.-column strip readings (the count 5–8 + the unnumbered + the 1910 №1!) + corpus forensics (the h17/h29/h30/h46/h74 continuities!) + THE STRUCTURAL LESSON: the 1st band of s139/s140 = an EMPTY row + the printed headers (NOT an entry — the first readings hallucinated from the surnames in the prompt!); anomalies ×18; **THE P139 LEAD: the marriages of 1910 (№1 on s141: Mathias JAKOBČIČ? [~] × Marija JAKOBČIČ? [~] — an intra-surname pair + the mother PEZDIREC + the mother ŽELJKO/Žugelj + a 3rd-degree dispensation of the ordinariate Jan 13, 1910 no. 159!**)",
    p138Errors.length === 0,
    p138Errors.length === 0
      ? `15 vpisov (lead 3,75× podcenjen — 24. leto!) · s138–s141 == Pag. 137–140 (24. potrditev!) · **★★ 14 PONEDDELJKOV + 1 NEDELJA = 93% PON (REKORD!)** · **★★★ INTRA-HIŠNA h46×h46 + DISPENSA 3. kolena (№11 št. 4571!)** · **★★★ SPREGLED 1. KOLENA + SODNO (№14 št. 4786 + 27036!)** · **★★ SPREGLED 3. kolena TOME×TOME (№13 št. 4995!)** · **★★ NEŠTEVILČEN 5. 7. = VOJAŠKA DELEGACIJA (polk št. 9!)** · **★ NOVA hiša h57 (68. — №8!)** → vitals 659 · bloki 142 · sidra 135 (+1909:8) · p80 hiše 68 (+h57) · PT luknja 14 · **P139 LEAD: 1910 (№1 Jakobčič × Jakobčič — intra-priimek!)**`
      : p138Errors.join("; "),
  );
  }
  // ——— qa-p139: POROČNA KNJIGA 04455 — polno leto 1910 (P139; 25. leto poročne linije) ———
  {
  const p139Errors: string[] = [];
  // 1910 = 3 GRIBLJE poroke / 5 blokov (№1 2 INTRA! + №14 2 + №17 1)
  const p139Marr = HOUSE_VITALS.filter((h) => h.bookSignature === "04455" && h.year === 1910);
  if (p139Marr.length !== 5)
    p139Errors.push(`bloki 1910 (04455) ≠ 5 (${p139Marr.length} — 3 poroke: №1 h13+h6 INTRA! + №14 h86+h31 + №17 h8 = 5!)`);
  const p139Houses = p139Marr.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
  if (p139Houses.join(",") !== "6,8,13,31,86")
    p139Errors.push(`hiše 1910 ≠ [6,8,13,31,86] — najdeno: ${p139Houses.join(",")} (P139: 3 GRIBLJE poroke — №1 h13 × h6 ★★★ INTRA-GRIBLJE INTRA-PRIIMEK! + №14 h86 NOVA POROČNA HIŠA! × h31 + №17 h8!)`);
  // P139 pini (5 blokov)
  const p139Pins: Array<[string, string]> = [
    ["13", "2. poročni dokaz h13"], ["13", "25-LETNA KONTINUITETA"], ["13", "Jakobič × Maria née PEZDIREC"],
    ["6", "4. poročni dokaz h6"], ["6", "Željko-botri"],
    ["86", "NOVA POROČNA HIŠA"], ["86", "GRID-definitivno"], ["86", "h85"],
    ["31", "4. poročni dokaz h31"], ["31", "Janez Straus × Barbara Jakobič"],
    ["8", "3. poročni dokaz h8"], ["8", "JAKLJEVIČ"], ["8", "18796"],
  ];
  for (const [hn, pin] of p139Pins) {
    const ms = HOUSE_VITALS.filter((h) => h.houseNo === hn && h.bookSignature === "04455" && h.year === 1910).map((h) => h.whatSi);
    if (!ms.some((m) => m && m.toLowerCase().includes(pin.toLowerCase())))
      p139Errors.push(`pin h${hn} 1910 (${pin}) manjka!`);
  }
  // novele
  if (!p139Marr.some((h) => h.whatSi.includes("INTRA-GRIBLJE INTRA-PRIIMEK")))
    p139Errors.push("★★★ INTRA-GRIBLJE INTRA-PRIIMEK h13 × h6 (№1 — obe družini JAKOBČIČ!) manjka");
  if (!p139Marr.some((h) => h.whatSi.includes("DISPENSA od krvnega sorodstva v 3. kolenu")))
    p139Errors.push("★★ DISPENSA 3. KOLENA (№1 ordinariat 13/1 1910 št. 159 [~]) manjka");
  if (!p139Marr.some((h) => h.whatSi.includes("DVOJNA SORODSTVENA ZAPREKA")))
    p139Errors.push("★★ DVOJNA SORODSTVENA ZAPREKA (№14 št. 2058 + spregled št. 12448!) manjka");
  if (!p139Marr.some((h) => h.whatSi.includes("DEŽELNE VLADE")))
    p139Errors.push("★★ DOVOLJENJE DEŽELNE VLADE št. 18796 (№17 nevesta 16 let!) manjka");
  if (HOUSE_VITALS.length !== 685)
    p139Errors.push(`HOUSE_VITALS ≠ 664 (${HOUSE_VITALS.length} — P138: 659; P139: + 5 blokov 1910 = 664!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length !== 168)
    p139Errors.push(`bloki 04455 ≠ 147 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length} — P138: 142; P139: + 5 blokov 1910 = 147!)`);
  push(
    "qa-p139-parish-marriage-1910",
    "P139: ŽUPNIJA PODZEMELJ — POROČNA KNJIGA 04455, POLNO LETO 1910 (issue #18; SAMPLE-TRANSCRIPTION-M1910; 25. leto poročne linije P115 = 1886 → … → P139 = 1910): okvir POTRJEN — s141–s145 == Pag. 140–144 (Pag. == sken − 1, **25. potrditev**; velja 61–146); **LETNICA 1910 SE PIŠE V VSAKEM VPISU — brez letne glave** (nadaljevanje lekcije P138); **1910 = 19 vpisov** (№1 s141 + №2–6 s142 + №7–10 s143 + №11–14 s144 + №15–19 s145 — №-stolpci pasovno potrjeni!; meja 1910/1911 na s146 = 1911 №1–7 [30.1.–19.6.] → P140 lead!) — **24. 1. ×5 = MASA-DAN REKORD LINIJE 1886–1910** (№2–№6 vse na en dan! prejšnji rekord 3) + **13 PON + 6 NED = 100% VIKEND-POROKE (19/19 — nitfedeljek!)** po 1909 (93% PON) popolna polarizacija; **VELIKE NOVELE P139**: **★★★ №1 INTRA-GRIBLJE INTRA-PRIIMEK POROKA h13 × h6** (Mathias JAKOBČIČ 53 × Marija JAKOBČIČ 32 — obe družini JAKOBČIČ, 1. takšna v 25 letih linije!; starši-dvojček Mathias Jakobčič ½ h13 × Mathias Jakobčič ¼ h6 — DVA Mathiasa!; priči = strica OBEH mater Pezdirec + Željko STRICEVSKI DVOJČEK!; DISPENSA 3. KOLENA enake stranske vrste ordinariat Ljubljana 13/1 1910 št. 159 [~ čtiri branjа 159/359/138/239]; h13 = 2. poročni dokaz [1885 brat Janez — ISTA starša Mathias × Maria Pezdirec = 25-LETNA KONTINUITETA!]; h6 = 4. dokaz [1903 Georg + krsti 1904/05 z Željko-botri!]) + **★★★ №14 GRIBLJE × GRIBLJE h86 × h31 + DVOJNA SORODSTVENA ZAPREKA** ([dispenza ~ ordinariat?] 24/5 1910 št. 2058 + SPREGLED [deželno sodišče?] 25/6 1910 št. 12448 + zglašnica Griblje 3/7 št. 2) + **★★ h86 = NOVA POROČNA HIŠA korpusa (67 → 68 p80!)** (Marcus KRIŽAN 24 [GRID-definitivno: 8 zaprti zanki + 6 ascender — prejšnja branjа 36/85/17 NAPAČNA!] = sin Marka Križana × Marije Strauš h85 [krst Janeza 1888!] na novi hiši 2 leti pred 1912 Brinec-krstom!) + **★★ KRIŽAN × STRAUS DRUŽINSKI DVOJČEK** (ženinov oče Križan × mati Strauš + nevesta STRAUS h31 [4. dokaz — 1886 Papič × Straus + 1897 krst Janez Straus × Barbara Jakobič = №14 starša!] — ženin se poroči z MOSKO DVOJNICO priimka svoje matere!) + **★★ №17 NEVESTA 16 LET (!!)** + DOVOLJENJE DEŽELNE VLADE V LJUBLJANI 1/8 1910 št. 18796 (1. deželna vlada v 04455-liniji! [P138 №14 = deželno SODIŠČE!]) — par 20+16 = 36 let + 3. GRIBLJE poroka leta (največ z 1909!) + h8 = 3. dokaz [1897+1900 Jakobčič + 1912 krst Jakofčič × Neza JAKLJEVIČ = nevestin priimek!]) + **★★ №3+№4 DVOJNA POROKA SOROJENCEV DRAGOŠ isti dan 24. 1.** (ista starša Joseph Dragoš × Dorothea Brodarič pri obeh!) + **★ №4 ženin MARTIN z očetom MAURIN** (priimka se ne ujemata — nezakonski/posvojen? [~]; MAURIN = №13 mati!) + **★ №18 69-LETNI ŽENIN LEDIG** (2. po 1908-v16 73! × 34-letna Kambičeva = 35 let razlike) + **★ №13 ženin + nevesta IZ ISTE HIŠE Primostek 18** + **★ №16 ISTI HIŠI KOT №2** (Gradac 44 × 55 drugič v letu + priča Franz Graf = №2 ženin [~]!) + **★ TRIJE sorodstveni dokumenti** (№1 št. 159 [~] + №7 dispenza 4.→3. kolena št. 158 [~] — ZAPOREDNI ŠTEVILKI isto-dnevnih ordinariatskih dispenz 13/1! + №14 spregled) + **★ JAKOBČIČ ×3 ženini** (№1 h13 + №5 Cerkvišče + №17 h8!) + BUTALA ×3 + TOME ×2 + BAJUK ×2 + KAMBIČ ×3-mreža + PEZDIREC ×3-mreža + KRIŽAN ×3-mreža + **★ NOVE OBLASTI**: ŠKOFLE PRI BREŽICAH na Štajerskem (št. 264+268!) + sv. Jernej (št. 15) + LOKA (št. 253) + deželna vlada Ljubljana (št. 18796) + VRHOVSKA VAS (nova vas — №9!) + **★ NOVI POKLICI**: Perkušec (perkar! №3) + Schmiedmeister (№15 — ŠTRUGAR kovaška dinastija: oče Wagenmeister + sin mojster + priča Štengar!) + Einwohner (№18) + Söllnergeselle? (№16) + Hufschmied (№13 oče — kovač konj!) + Knecht (№2) + **★ ~25 NOVIH PRIIMKOV** (Žephar · Pavlenič · Štrugar · Kosevar · Schmidt · Rauch · Žiličič · Puček · Kovačič · Graf · Žaborič · Hagar · Likosek · Debeljak · Jonec · Anžlovar · Gorsič · Kostelec · Harasinić · Petrašič · Honič · Mathies · Želenič? · Gregorič · Uleh …) + **★ DUHOVNIK DANIJEL 2. pojav** (№9 1909 + №9 1910 — obe št. 9!; Rauy 17–18/19 dominant) + **★ METODA P139 (preboj!)**: 100+ VLM branj (38 vrstičnih + 8 zoom-1 + 55+ fini 2. kroga multi-render o/i/d) + **GRID-TEHNIKA** (rdeče črte z x-oznakami za prostorsko preslikavo — razrešila VSE hišne številke!) + korpus-forenzika (h13 1885 ISTA starša! + h6 Željko-botri! + h31 1897 №14-starša! + h85 Križan×Strauš 1888! + h8 1912 Jakljevič!) + **GEOMETRIJSKA LEKCIJA: rezidenca je PRED imenom v bloku!** (prva generacija izrezov je ujela starost/ulomek namesto hiše — 7 POPRAVKOV 2. kroga: №4 starost 14→18 · №10 Andreas→ALFONS · №14 hiša 36/85/17→86 · №14 nevesta 11/21/41→31 · №9 Schwaiger→VRHOVSKA VAS · №18 Filovje→KRASINEC 30 · №2 Gneuf→GRAF!); anomalije ×18; **P140 LEAD: poročna 1911 (№1–7 na s146: 30.1.–19.6. 1911!)**",
    "P139: THE PARISH OF PODZEMELJ — MARRIAGE REGISTER 04455, THE FULL YEAR 1910 (issue #18; SAMPLE-TRANSCRIPTION-M1910; the 25th year of the marriage line P115 = 1886 → … → P139 = 1910): the frame CONFIRMED — s141–s145 == pages 140–144 (page == scan − 1, the **25th confirmation**; valid 61–146); **THE YEAR 1910 IS WRITTEN IN EVERY ENTRY — no year heading** (the P138 lesson continued); **1910 = 19 entries** — **Jan 24 ×5 = THE MASS-DAY RECORD OF THE LINE 1886–1910** (№2–№6 all on one day! the previous record 3) + **13 Mondays + 6 Sundays = 100% WEEKEND WEDDINGS (19/19!)** after the 1909 (93% Monday) a full polarisation; **THE BIG P139 NOVELS**: **★★★ the №1 INTRA-GRIBLJE INTRA-SURNAME WEDDING h13 × h6** (Mathias JAKOBČIČ 53 × Marija JAKOBČIČ 32 — both families JAKOBČIČ, the 1st such in 25 years!; the parents-twin Mathias Jakobčič ½ of h13 × Mathias Jakobčič ¼ of h6 — TWO Mathiases!; the witnesses = the maternal uncles of BOTH Pezdirec + Željko — an UNCULAR TWIN!; the DISPENSATION of the 3rd DEGREE of the ordinariate of Ljubljana Jan 13, 1910 no. 159 [~ four readings]; the h13 = the 2nd marriage evidence [the 1885 brother Janez — THE SAME parents Mathias × Maria Pezdirec = a 25-YEAR CONTINUITY!]; the h6 = the 4th evidence [the 1903 Georg + the baptisms 1904/05 with the Željko godparents!]) + **★★★ the №14 GRIBLJE × GRIBLJE h86 × h31 + a DOUBLE IMPEDIMENT** (May 24, 1910 no. 2058 + the OVERSIGHT Jun 25, 1910 no. 12448 + the Griblje certificate Jul 3 no. 2) + **★★ the h86 = A NEW MARRIAGE HOUSE of the corpus (the p80 67 → 68!)** (Marcus KRIŽAN 24 [GRID-definitive: 8 two closed loops + 6 ascender — the earlier readings 36/85/17 WRONG!] = the son of Marko Križan × Marija Strauš of h85 [the baptism of Janez 1888!] at the new house 2 years before the 1912 Brinec baptism!) + **★★ the KRIŽAN × STRAUS FAMILY TWIN** (the groom's father Križan × the mother Strauš + the bride STRAUS of h31 [the 4th evidence — the 1886 Papič × Straus + the 1897 baptism Janez Straus × Barbara Jakobič = THE 1910 №14 PARENTS!] — the groom marries the FEMALE TWIN of his mother's surname!) + **★★ the №17 BRIDE 16 YEARS (!!)** + THE PERMIT OF THE PROVINCIAL GOVERNMENT OF LJUBLJANA Aug 1, 1910 no. 18796 (the 1st provincial government in the 04455 line!) — the couple 20+16 = 36 years + the 3rd GRIBLJE wedding of the year + the h8 = the 3rd evidence [1897+1900 Jakobčič + the 1912 baptism Jakofčič × Neza JAKLJEVIČ = the bride's surname!]) + **★★ the №3+№4 DOUBLE WEDDING OF THE DRAGOŠ SIBLINGS the same day Jan 24** (the same parents Joseph Dragoš × Dorothea Brodarič in both!) + **★ the №4 groom MARTIN with the father MAURIN** (the surnames mismatch — illegitimate/adopted? [~]; MAURIN = the №13 mother!) + **★ the №18 69-YEAR-OLD GROOM SINGLE** (the 2nd after the 1908-v16 73!) + **★ the №13 groom + bride FROM THE SAME HOUSE Primostek 18** + **★ the №16 THE SAME HOUSES AS №2** (Gradac 44 × 55 twice in the year!) + **★ THREE kinship documents** (№1 no. 159 [~] + №7 the 4th→3rd degree no. 158 [~] — SEQUENTIAL NUMBERS of the same-day ordinariate dispensations Jan 13! + №14 the oversight) + **★ the JAKOBČIČ ×3 grooms** + BUTALA ×3 + TOME ×2 + BAJUK ×2 + the KAMBIČ/PEZDIREC/KRIŽAN networks ×3 + **★ NEW AUTHORITIES**: ŠKOFLE PRI BREŽICAH in Styria! + sv. Jernej + LOKA + the provincial government of Ljubljana + VRHOVSKA VAS (a new village) + **★ NEW OCCUPATIONS**: Perkušec (a currier!) + Schmiedmeister (the ŠTRUGAR smithing dynasty!) + Einwohner + Hufschmied + **★ ~25 NEW SURNAMES** + **★ THE PRIEST DANIJEL the 2nd appearance** (№9 1909 + №9 1910!) + **★ THE P139 METHOD (a breakthrough!)**: 100+ VLM readings + THE GRID TECHNIQUE (red labelled lines for spatial mapping — resolved ALL house numbers!) + corpus forensics + THE GEOMETRICAL LESSON: THE RESIDENCE COMES BEFORE THE NAME IN EACH BLOCK! (the first crop generation caught the age/fraction instead — 7 SECOND-ROUND CORRECTIONS!); anomalies ×18; **THE P140 LEAD: the marriages of 1911 (№1–7 on s146!)**",
    p139Errors.length === 0,
    p139Errors.length === 0
      ? `19 vpisov · s141–s145 == Pag. 140–144 (25. potrditev!) · **★★ 24. 1. ×5 = MASA-DAN REKORD!** · **★★ 13 PON + 6 NED = 100% VIKEND!** · **★★★ №1 INTRA-GRIBLJE INTRA-PRIIMEK h13 × h6 (2 × JAKOBČIČ + dispenza št. 159 [~] + stricevski dvojček!** · **★★★ №14 h86 NOVA POROČNA HIŠA × h31 + DVOJNA ZAPREKA (št. 2058 + 12448!)** · **★★ №17 nevesta 16 let + deželna vlada št. 18796!** · **★★ №3+№4 dvojna poroka sorojencev Dragoš!** · **★ №18 ženin 69 ledig · №13 isti hiši Primostek 18 · №16 isti hiši kot №2** → vitals 664 · bloki 147 · sidra 140 (+1910:5) · p80 hiše 68 (+h86) · PT luknja 13 · **P140 LEAD: 1911 (s146 №1–7!)**`
      : p139Errors.join("; "),
  );
  }
  // ——— qa-p140: POROČNA KNJIGA 04455 — polno leto 1911 (P140; 26. leto poročne linije) ———
  {
  const p140Errors: string[] = [];
  // 1911 = 4 GRIBLJE poroke / 6 blokov (№1 2 INTRA! + №2 2 INTRA! + №3 1 + №12 1)
  const p140Marr = HOUSE_VITALS.filter((h) => h.bookSignature === "04455" && h.year === 1911);
  if (p140Marr.length !== 6)
    p140Errors.push(`bloki 1911 (04455) ≠ 6 (${p140Marr.length} — 4 poroke: №1 h31+h63 INTRA! + №2 h15+h34 INTRA! + №3 h9 + №12 h33 = 6!)`);
  const p140Houses = p140Marr.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
  if (p140Houses.join(",") !== "9,15,31,33,34,63")
    p140Errors.push(`hiše 1911 ≠ [9,15,31,33,34,63] — najdeno: ${p140Houses.join(",")} (P140: 4 GRIBLJE poroke — №1 h31 × h63 ★★ 3. leto zapored INTRA! + №2 h15 × h34 INTRA + №3 h9 4. Jakobčič-hiša + №12 h33 vdovec!)`);
  // P140 pini (6 blokov)
  const p140Pins: Array<[string, string]> = [
    ["31", "5. poročni dokaz h31"], ["31", "ŽENINOV KRST V KORPUSU"],
    ["63", "NOVA POROČNA HIŠA"], ["63", "REHABILITACIJSKA"], ["63", "samka"],
    ["15", "KAMBIČ-DINASTIJA"], ["34", "3. KAMBIČ-NEVESTA"], ["34", "6. poročni dokaz h34"],
    ["9", "JAKOBČIČ-TROJNA MREŽA"], ["9", "26 LET"],
    ["33", "GENETSKA-GRIBLJE"], ["33", "KORPUS-SINHRONIZACIJA"], ["33", "VDOVEC"],
  ];
  for (const [hn, pin] of p140Pins) {
    const ms = HOUSE_VITALS.filter((h) => h.houseNo === hn && h.bookSignature === "04455" && h.year === 1911).map((h) => h.whatSi);
    if (!ms.some((m) => m && m.toLowerCase().includes(pin.toLowerCase())))
      p140Errors.push(`pin h${hn} 1911 (${pin}) manjka!`);
  }
  // novele
  if (!p140Marr.some((h) => h.whatSi.includes("GRIBLJE × GRIBLJE")))
    p140Errors.push("★★ INTRA-GRIBLJE ×2 (№1 h31 × h63 + №2 h15 × h34 — rekord z 1910!) manjka");
  if (!p140Marr.some((h) => h.whatSi.includes("REHABILITACIJSKA")))
    p140Errors.push("★★★ REHABILITACIJSKA POROKA (№1 — Katarina Križan 'samka' h63-1909!) manjka");
  if (!p140Marr.some((h) => h.whatSi.includes("KORPUS-SINHRONIZACIJA")))
    p140Errors.push("★★★ KORPUS-SINHRONIZACIJA (№12 krst Terezije 1912 Martin Papič × Ana Tomc!) manjka");
  if (!p140Marr.some((h) => h.whatSi.includes("WITWER")))
    p140Errors.push("★★ VDOVEC №12 (Martin Papič — 1. vdovec po 1910-№18!) manjka");
  if (HOUSE_VITALS.length !== 685)
    p140Errors.push(`HOUSE_VITALS ≠ 670 (${HOUSE_VITALS.length} — P139: 664; P140: + 6 blokov 1911 = 670!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length !== 168)
    p140Errors.push(`bloki 04455 ≠ 153 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length} — P139: 147; P140: + 6 blokov 1911 = 153!)`);
  push(
    "qa-p140-parish-marriage-1911",
    "P140: ŽUPNIJA PODZEMELJ — POROČNA KNJIGA 04455, POLNO LETO 1911 (issue #18; SAMPLE-TRANSCRIPTION-M1911; 26. leto poročne linije P115 = 1886 → … → P140 = 1911): okvir POTRJEN — s146–s148 == Pag. 145–147 (Pag. == sken − 1, **26. potrditev**; velja 61–148); **letnica V VSAKEM vpisu — 3. leto brez letne glave (1909/1910/1911!)**; **1911 = 13 vpisov** (№1–6 s146 + №7–11 s147 + №12–13 s148; štetje potrjeno s STRIP-tehniko [celi datumski stolpec — 6+5+2 datumov!] + zaporednimi branjí + GRID-№); **8 PON + 4 NED + 1 TOR** = 12/13 vikendskih — **edina izjema №7 BETETTO (Dunaj!)**; **VELIKE NOVELE P140**: **★★★ №7 ZGODOVINSKA DUNAJSKA POROKA** (Julius BETETTO **k.k. Hofopern-Sänger** — dvorni operni pevec!, 25, **Wien IV/8 Wallergasse 3/11** × Irma-Maria STUKELY, 19, **Rudolfsheim 132** — 4. 7. 1911 TOR! + listine pri **Standesamt Rudolfsheim** + **RAUY PER DELEGATIONEM** [1. podpis po delegaciji!] + mati **Julia SKRBEC** = slovenske korenine dunajskega zvezdnika! + dunajski meščanski priči [lekarnar + knjigotržec] + nevesta 19 = najmlajša leta!) + **★★★ ISTA-HIŠA REKORD ×3** (№6 Podzemelj 2 + №8 Vranoviči 3 + №11 Gradac 3 — prejšnji maks 1/leto [1910 №13 Primostek 18]!) + **★★ INTRA-GRIBLJE ×2** (№1 h31 × h63 [3. leto zapored!] + №2 h15 × h34 — rekord z 1910) + **★★ №1 REHABILITACIJSKA POROKA?** (Katarina Križan **'samka' h63-1909** [hči Jožefa 12. 6. 1909!] → poroka 30. 1. 1911) + **№1 DVOJNO ZUNANJE SIDRO** (ženinov krst h31-1887 Janez 6. 9. [starost 23 ✓] + **EMŠO-1919 'Katarina r. Herian (2. 2. 1887; por. 30/1 1911)'**!) + **№8 BUTALA-SESTRI** (Anna 1911 = sestra Marije 1910 №5 — ISTA starša Anton Butala × Barbara Kambič + ISTA hiša Vranoviči 3!) + **№12 VDOVEC + KORPUS-SINHRONIZACIJA** (Martin Papič h33 — prva žena Marija Mlut [hčeri 1909 + †9 dni 23. 5. 1911] → poroči 5. 11. 1911; krst Terezije 5. 10. 1912 **Martin Papič × ANA TOMC = PAR POTRDJEN**!) + **№12 'Giriči' = GRIBLJE** (genetska-vas lekcija 3. pojav) + Krivoglave-nova vas + **MASA-DAN 6. 2. ×3** (№2+№3+№4 — 4. trojni-dan linije) + **POSTNA VRZEL 6. 2. → 15. 5.** ('15. März' branjе ZAVRNJENO — sredina posta nemogoča! P138-März-lekcija + koledar!) + **№13 KRALJ ×2 + KLEPEC-trojna mreža** (№3 nevesta + №13 mati Ana Klepec + priča Jurij Klepec!) + **№6 Kralj × Pezdirec starši** (Georg Kralj × Anna geb. Pezdirec — 25-letna mreža!) + **№9 MAROVIČ oče-sin dvojček** (Mathias × Mathäus Marovitz — nemški -itz = -ič!) + **№10 ZUCKERMEISTER + ŽUGELJ ×3 leta** (№6 mati + №10 nevesta [nemško 'Zigely'!] + №12 mati) + **NOVI POKLICI** (Hofopern-Sänger! + Zuckermeister + Köppersohn + Knecht + Gemeinde-Beamter + Doltar-kovaška dinastija oče+sin Schmiedmeister!) + **NOVE OBLASTI** (Standesamt Rudolfsheim Dunaj! + župni urad Črnomelj št. 316 + ordinariat Ljubljana 7. 11. 1911 [~ №13] + županstvo Gradac) + **~20 NOVIH PRIIMKOV** (Betetto, Stukely, Skrbec, Millner, Doltar, Filetič, Malovič, Petrowic, Marovič, Zadravec, Berkopec, Pečinek?, Kurnik?, Motnikov?, Zadravec...) + **meja 1911/1912 = s148: P141 LEAD** (1912 №1 = 16. 1. 1912 **Anton Lozar 21 Griblje 78 × Barbara Križan 22 Griblje 63** — Lozar ×2 v 3 mesecih! + 04105-h78-1915 krst Lozar!); GRIBLJE poroke ×4 = **6 blokov** (h31 №1 ženin 5. dokaz + **h63 №1 nevesta NOVA 68.→69.** + h15 №2 ženin + **h34 №2 nevesta Kambič-dinastija 1905 ×2 → 1911!** + h9 №3 ženin 4. Jakobčič-hiša [kontinuiteta 1885 → 1911 = 26 LET!] + h33 №12 ženin vdovec); anomalije ×14; vitals **664 → 670** (+ 6 blokov); bloki 04455 = **147 → 153**; p80 hiše **68 → 69 (+h63 — 04105-h63 bloki 1887–1909 izven p80-filtra!)**; PT luknja **13 (nespremenjena — h63 v naboru 61–99!)**; poročna sidra **140 → 146 (+1911:6)**; metoda: 65 VLM branj v 4 krogih + STRIP-tehnikа (celi datumski stolpec!) + eko-watchdog V2 (30-min ping po 429); EXCLUDED: 0; skripta scripts/p140_parish_marriage_1911.py (I1–I11); status SAMPLE-TRANSCRIPTION-M1911",
    "P140: THE PARISH OF PODZEMELJ — MARRIAGE REGISTER 04455, THE FULL YEAR 1911 (issue #18; SAMPLE-TRANSCRIPTION-M1911; the 26th year of the marriage line P115 = 1886 → … → P140 = 1911): the framework CONFIRMED — s146–s148 == Pag. 145–147 (Pag. == scan − 1, **the 26th confirmation**; valid 61–148); **the year in EVERY entry — the 3rd year without an annual header (1909/1910/1911!)**; **1911 = 13 entries** (№1–6 s146 + №7–11 s147 + №12–13 s148; the count confirmed by the STRIP technique [whole date columns — 6+5+2 dates!] + sequential readings + GRID-№); **8 MON + 4 SUN + 1 TUE** = 12/13 weekend — **the only exception №7 BETETTO (Vienna!)**; **THE BIG P140 NOVELTIES**: **★★★ №7 THE HISTORICAL VIENNESE WEDDING** (Julius BETETTO **a k.k. Court-Opera singer**, 25, **Wien IV/8 Wallergasse 3/11** × Irma-Maria STUKELY, 19, **Rudolfsheim 132** — Jul 4, 1911 TUE! + the documents at the **Rudolfsheim registry office** + **RAUY PER DELEGATIONEM** [the 1st signature by delegation!] + the mother **Julia SKRBEC** = the Viennese star's Slovenian roots! + the Viennese bourgeois witnesses [a pharmacist + a bookseller] + the bride 19 = the youngest of the year!) + **★★★ the SAME-HOUSE RECORD ×3** (№6 Podzemelj 2 + №8 Vranoviči 3 + №11 Gradac 3 — the previous max 1/year [1910 №13 Primostek 18]!) + **★★ INTRA-GRIBLJE ×2** (№1 h31 × h63 [the 3rd consecutive year!] + №2 h15 × h34 — a record with 1910) + **★★ №1 a REHABILITATION WEDDING?** (Katarina Križan **a 'single mother' h63-1909** [the daughter Jožefa of Jun 12, 1909!] → the wedding Jan 30, 1911) + **№1 A DOUBLE EXTERNAL ANCHOR** (the groom's h31-1887 baptism Janez Sep 6 [the age 23 ✓] + **the 1919 personal-ID 'Katarina née Herian (Feb 2, 1887; m. Jan 30, 1911)'**!) + **№8 the BUTALA SISTERS** (Anna 1911 = the sister of Maria 1910 №5 — THE SAME parents Anton Butala × Barbara Kambič + THE SAME house Vranoviči 3!) + **№12 A WIDOWER + a CORPUS SYNCHRONIZATION** (Martin Papič h33 — the first wife Marija Mlut [the daughters 1909 + †9 days May 23, 1911] → he marries Nov 5, 1911; the baptism of Terezija Oct 5, 1912 **Martin Papič × ANA TOMC = THE COUPLE CONFIRMED**!) + **№12 'Giriči' = GRIBLJE** (the genetic-village lesson's 3rd appearance) + the new village Krivoglave + **the MASS-DAY Feb 6 ×3** (№2+№3+№4 — the line's 4th triple-day) + **the LENT GAP Feb 6 → May 15** (the 'Mar 15' reading REJECTED — mid-Lent impossible! the P138-März-lesson + the calendar!) + **№13 KRALJ ×2 + the KLEPEC triple network** (№3 bride + №13 mother Ana Klepec + the witness Jurij Klepec!) + **№6 the Kralj × Pezdirec parents** (Georg Kralj × Anna née Pezdirec — a 25-year network!) + **№9 the MAROVIČ father-son name-twin** (Mathias × Mathäus Marovitz — the German -itz = -ič!) + **№10 ZUCKERMEISTER + ŽUGELJ ×3 of the year** (№6 mother + №10 bride [the German 'Zigely'!] + №12 mother) + **NEW OCCUPATIONS** (a Court-Opera singer! + a confectioner + a coppersmith's son + a farmhand + a municipal official + the Doltar smithing dynasty father+son Schmiedmeister!) + **NEW AUTHORITIES** (the Rudolfsheim registry office Vienna! + the Črnomelj parish office no. 316 + the Ljubljana ordinariate Nov 7, 1911 [~ №13] + the Gradac commune) + **~20 NEW SURNAMES** (Betetto, Stukely, Skrbec, Millner, Doltar, Filetič, Malovič, Petrowic, Marovič, Zadravec, Berkopec, Pečinek?, Kurnik?, Motnikov?...) + **the 1911/1912 boundary = s148: the P141 LEAD** (the 1912 №1 = Jan 16, 1912 **Anton Lozar 21 Griblje 78 × Barbara Križan 22 Griblje 63** — Lozar ×2 in 3 months! + the 04105-h78-1915 Lozar baptism!); the GRIBLJE weddings ×4 = **6 blocks** (h31 №1 groom the 5th evidence + **h63 №1 bride NEW the 68th→69th.** + h15 №2 groom + **h34 №2 bride the Kambič dynasty 1905 ×2 → 1911!** + h9 №3 groom the 4th Jakobčič house [a continuity 1885 → 1911 = 26 YEARS!] + h33 №12 groom the widower); anomalies ×14; vitals **664 → 670** (+ 6 blocks); the 04455 blocks = **147 → 153**; p80 houses **68 → 69 (+h63 — the 04105-h63 blocks 1887–1909 outside the p80 filter!)**; the PT gap **13 (unchanged — h63 in the 61–99 set!)**; the marriage anchors **140 → 146 (+1911:6)**; the method: 65 VLM readings in 4 rounds + the STRIP technique (whole date columns!) + the eco-watchdog V2 (a 30-min ping after 429); EXCLUDED: 0; the script scripts/p140_parish_marriage_1911.py (I1–I11); status SAMPLE-TRANSCRIPTION-M1911",
    p140Errors.length === 0,
    p140Errors.length === 0
      ? `13 vpisov · s146–s148 == Pag. 145–147 (26. potrditev!) · **★★★ №7 BETETTO: dunajski Hofopern-Sänger na vaški poroki!** · **★★★ ista-hiša ×3 (Podzemelj 2 + Vranoviči 3 + Gradac 3)!** · **★★ INTRA-GRIBLJE ×2 (h31 × h63 + h15 × h34)!** · 8 PON + 4 NED + 1 TOR! · №1 rehabilitacijska + dvojno sidro! · №12 vdovec + krst-1912 potrditev! · h63 NOVA (68→69!)`
      : p140Errors.join("; "),
  );
  }

  // ——— qa-p141: POROČNA KNJIGA 04455 — polno leto 1912 (P141; 27. leto poročne linije) ———
  {
  const p141Errors: string[] = [];
  // 1912 = 4 GRIBLJE poroke / 5 blokov (№1 2 INTRA! + №9 1 + №15 1 + №17 1)
  const p141Marr = HOUSE_VITALS.filter((h) => h.bookSignature === "04455" && h.year === 1912);
  if (p141Marr.length !== 5)
    p141Errors.push(`bloki 1912 (04455) ≠ 5 (${p141Marr.length} — 4 poroke: №1 h78+h63 INTRA! + №9 h46 + №15 h44 + №17 h21 = 5!)`);
  const p141Houses = p141Marr.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
  if (p141Houses.join(",") !== "21,44,46,63,78")
    p141Errors.push(`hiše 1912 ≠ [21,44,46,63,78] — najdeno: ${p141Houses.join(",")} (P141: 4 GRIBLJE poroke — №1 h78 NOVA × h63 2. dokaz SESTRI-KRIŽAN! + №9 h46 3. dokaz + №15 h44 + №17 h21)`);
  // P141 pini (5 blokov)
  const p141Pins: Array<[string, string]> = [
    ["78", "1. POROČNI DOKAZ"], ["78", "KORPUS-KRST"], ["78", "čevljar"], ["78", "ŽE V p80-korpusu"],
    ["63", "SESTRI KRIŽAN"], ["63", "SESTRA 1911-№1"], ["63", "8 krstnih blokov"],
    ["46", "3. poročni dokaz"], ["46", "NAJSTAREJŠA NEVESTA"], ["46", "ŠTRAVS-mreža"],
    ["44", "GENETSKA-VAS"], ["44", "PAPIČ"], ["44", "25-LETNA STRAUS-PAPIČ VEZA"],
    ["21", "KORPUS-SINHRONIZACIJA"], ["21", "PRESELITEV"], ["21", "MEŽNARJI"], ["21", "SODIŠČE ČRNOMELJ"],
  ];
  for (const [hn, pin] of p141Pins) {
    const ms = HOUSE_VITALS.filter((h) => h.houseNo === hn && h.bookSignature === "04455" && h.year === 1912).map((h) => h.whatSi);
    if (!ms.some((m) => m && m.toLowerCase().includes(pin.toLowerCase())))
      p141Errors.push(`pin h${hn} 1912 (${pin}) manjka!`);
  }
  // novele
  if (!p141Marr.some((h) => h.whatSi.includes("GRIBLJE × GRIBLJE")))
    p141Errors.push("★★ INTRA-GRIBLJE №1 (h78 × h63 — 3. leto zapored intra-poroče!) manjka");
  if (!p141Marr.some((h) => h.whatSi.includes("SESTRI KRIŽAN")))
    p141Errors.push("★★★ SESTRI KRIŽAN h63 v zaporednih januarjih (1911 №1 Katarina + 1912 №1 Barbara — P140-lead VERIF!) manjka");
  if (!p141Marr.some((h) => h.whatSi.includes("KORPUS-SINHRONIZACIJA")))
    p141Errors.push("★★ KORPUS-SINHRONIZACIJA №17 (krst Julija 1913 h31 Černič × Požek!) manjka");
  if (!p141Marr.some((h) => h.whatSi.includes("GENETSKA-VAS")))
    p141Errors.push("★ GENETSKA-VAS 'Girišice' = Griblje 3. pojav (№15!) manjka");
  if (HOUSE_VITALS.length !== 685)
    p141Errors.push(`HOUSE_VITALS ≠ 681 (${HOUSE_VITALS.length} — P140: 670; P141: + 5 blokov 1912 = 675!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length !== 168)
    p141Errors.push(`bloki 04455 ≠ 158 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length} — P140: 153; P141: + 5 blokov 1912 = 158!)`);
  push(
    "qa-p141-parish-marriage-1912",
    "P141: ŽUPNIJA PODZEMELJ — POROČNA KNJIGA 04455, POLNO LETO 1912 (issue #18; SAMPLE-TRANSCRIPTION-M1912; 27. leto poročne linije P115 = 1886 → … → P141 = 1912): okvir POTRJEN — s148-dno + s149–s151 == Pag. 147–150 (Pag. == sken − 1, **27. potrditev**; velja 61–151) + **s152 = ŽE 1913 №1 (27. 1.) = meja leta DOKAZANA + P142-lead!**; **1912 = 17 vpisov** (№1 s148-dno + №2–6 s149 + №7–11 s150 + №12–17 s151; štetje potrjeno s STRIP-tehniko [celi datumski stolpci s148–s151!] + zaporedjem + s152-mejo; P140-lead je poznal samo №1–6 — razširitev ×2,8!); **14 PON + 1 NED + 1 TOR (№1!) + 1 PET (№5!)** = 15/17 ponedeljkovih/vikendskih — **2 izjemi (1911: 1 TOR Dunaj)**; **letnica V VSAKEM vpisu — 4. leto brez letne glave**; **1912 = SLOVENŠČINA + najhitrejša pisava novega pisarja = najtežje leto linije!** (zato ~190 VLM branj v 6 krogih + STRIP + GRID-geometrija [REZIDENCA JE PRED IMENOM V BLOKU!] + multi-render pasovi o/i/d); **VELIKE NOVELE P141**: **★★★ RECIPROČNI DVOJNI PAR SOROJENCEV (№11+№12, 20. 5. 1912)** — Muc-sorojenca (Barbara 24 + Nikolaj 34, Primostek 10, otroka Matija Muc × Ana geb. Vukšinič) × Jakljevič-sorojenca (Nikolaj 26 + Marija 20, Krasinec 13, otroka Nikolaj Jakljevič × Ana geb. Križan) — **KRIŽNO-IZMENJČNE HIŠE = 1. tak primer v celotni liniji 1886–1912!** (prejšnji maks: 1910 №3+№4 Dragoš-sorojenca isti dan — a brez reciprocitete!) + **★★★ INTRA-PRIIMEK ×2 V ENEM LETU** (№7 PEZDIREC × PEZDIREC [Mihaelova vs Matijeva linija — zrcalo 1910 №1 Jakobčič!] + №14 ŽUGELJ × ŽUGELJ [Jakobova vs Matijeva] = **3 intra-priimek poroke linije, 2 v samem 1912 = REKORD!**) + **★★★ SESTRI KRIŽAN h63 V ZAPOREDNIH JANUARJIH** (1911 №1 Katarina × Papič h31 + 1912 №1 Barbara × Lozar h78 — obe hčereti Nikolaja Križana × Katarina geb. Pezdirec; **P140-lead 'sestri?' → POTRJENO S KORPUSOM** [krsta 20. 1. 1887 + 20. 6. 1889 h63!]) + **★★★ DVOJNA KORPUS-SINHRONIZACIJA №8** (ženinovi starši = **1891 №12 Jakša × Jakša** + nevestini starši = **1890 №2 Schweiger × Jakša** — OBA STARŠA-PARA ŽENINA IN NEVESTE ŽE V KORPUSU = 1. tak primer!) + **★★ №9 NEVESTA 46 LET** (Barbara Straus bajtarica Griblje h46 — 2. najstarejša po 1886-v1 56; par 31+46; h46 = 3. poročni dokaz [1909 №11 INTRA-h46!]) + **★★ №17 KORPUS-SINHRO 1913** (sin Julij krst 8. 8. 1913 h31 Griblje 'Jožef Černič × Ana Počelf[=Požek]' — PAR + PRESELITEV POTRJENA!; nevesta krst 3. 4. 1890 Janez Požek × Ana Šimec = starost 22 ✓; POŽEK = MEŽNARJI Adlešič!) + **★★ №4+№6 JAKOFČIČ DVOJČEK** (brat ženin Nikolaj Čerkvišče 16 + sestra nevesta Ana Čerkvišče 17 — otroka Petra Jakofčiča; poroki 29. 1. + 12. 2.!) + **★★ HRAŠINOVIČ-DVOJČEK** (№6 Nikolaj 24 Krasinec 20 + №16 Nikolaj 49 Krasinec 32 — očeta Anton + Janez + №1 mati Barbara geb. Harasinč = 3. Harasin-pojav leta!) + **★★ ŠTRAVS/STRAUS-MREŽA ×4** (№9+№10+№15 neveste + priča Jožef = **3 Straus-neveste v 1 letu = REKORD!**) + **★ MASA-DNEVI ×3** (29. 1. №2+№3+№4 TROJNI + 12. 2. №6+№7 + 20. 5. №11+№12 = 6/17 v skupnih dneh!) + **★ NOVE OBLASTI** (SODIŠČE ČRNOMELJ №17 — 1. v liniji! + vojaško oblastno poveljstvo №8 [16. 1. 1912 — predvojno leto!] + deželna vlada Ljubljana №5 št. 2846? [2. po 1910 №17] + Radovica-listine №13 [drugožupnijska!] + ordinariat št. 5473 [~]) + **★ №13 ALFRED trgovski pomočnik [~] Podzemelj 11** (1. latinsko ime linije! + nemški priimec [Kerschbaumer? ~ 6 variant branj] + KURE-priči + morda 4. stopnja dispenza [obe materi geb. Kure? ~]) + **★ KRIVOGLAVCI 3. pojav** (1898 №4 + 1911 №12 + 1912 №14!) + **★ NOVI POKLICI** (čevljar! + trgovski pomočnik + drvinar + mizar + bajtar/bajtarica ×3 + mežnar) + **~18 NOVIH PRIIMKOV** (Lozar, Jurjevič, Justarič, Harasinovič-ženin, Švajgar-slovensko, Marencič, Vukšinič, Filak-mati, Škalič, Perdih, Pirc, Černič, Požek-nevesta, Rus-mati, Spudič? [~], Kerschbaumer? [~], Žofrca? [~], Bohle? [~]) + **GENETSKA-VAS 'Girišice' = GRIBLJE 3. pojav** (№15 h44!); GRIBLJE poroke ×4 = **5 blokov** (№1 h78 ženin **1. POROČNI DOKAZ** [korpus-1915 krst para na h78; ŽE v p80 prek 1887-sidra!] + h63 nevesta 2. dokaz [SESTRI!] + №9 h46 3. dokaz + №15 h44 [Girišice-GENETSKA!] + №17 h21); anomalije ×18; vitals **670 → 675** (+ 5 blokov); bloki 04455 = **153 → 158**; p80 hiše **69 NESPREMENJENE (h78 ŽE v p80 prek 04105-1887-sidra!)**; PT luknja **13 (nespremenjena)**; poročna sidra **146 → 151 (+1912:5)**; EXCLUDED: 4 (prazni pasi s148–s151 + s152-1913-meja); skripta scripts/p141_parish_marriage_1912.py (I1–I12); status SAMPLE-TRANSCRIPTION-M1912",
    "P141: THE PARISH OF PODZEMELJ — MARRIAGE REGISTER 04455, THE FULL YEAR 1912 (issue #18; SAMPLE-TRANSCRIPTION-M1912; the 27th year of the marriage line P115 = 1886 → … → P141 = 1912): the framework CONFIRMED — the s148 bottom + s149–s151 == Pag. 147–150 (Pag. == scan − 1, **the 27th confirmation**; valid 61–151) + **s152 = ALREADY 1913 №1 (Jan 27) = the year boundary PROVEN + the P142 lead!**; **1912 = 17 entries** (№1 s148-bottom + №2–6 s149 + №7–11 s150 + №12–17 s151; the count confirmed by the STRIP technique [whole date columns s148–s151!] + the sequence + the s152 boundary; the P140 lead knew only №1–6 — an expansion ×2.8!); **14 MON + 1 SUN + 1 TUE (№1!) + 1 FRI (№5!)** = 15/17 Monday/weekend — **2 exceptions (1911: 1 TUE Vienna)**; **the year in EVERY entry — the 4th year without an annual header**; **1912 = SLOVENIAN + the new scribe's fastest hand = the hardest year of the line!** (hence ~190 VLM readings in 6 rounds + the STRIP + the GRID geometry [THE RESIDENCE COMES BEFORE THE NAME IN THE BLOCK!] + multi-render bands o/i/d); **THE BIG P141 NOVELTIES**: **★★★ THE RECIPROCAL DOUBLE SIBLING PAIR (№11+№12, May 20, 1912)** — the Muc siblings (Barbara 24 + Nikolaj 34, Primostek 10, the children of Matija Muc × Ana née Vukšinič) × the Jakljevič siblings (Nikolaj 26 + Marija 20, Krasinec 13, the children of Nikolaj Jakljevič × Ana née Križan) — **CROSS-EXCHANGED HOUSES = the 1st such case in the whole line 1886–1912!** (the previous max: the 1910 №3+№4 Dragoš siblings the same day — but without reciprocity!) + **★★★ INTRA-SURNAME ×2 IN ONE YEAR** (№7 PEZDIREC × PEZDIREC [the Mihael vs the Matija line — a mirror of the 1910 №1 Jakobčič!] + №14 ŽUGELJ × ŽUGELJ [the Jakob vs the Matija branch] = **3 intra-surname weddings of the line, 2 in 1912 alone = A RECORD!**) + **★★★ THE KRIŽAN SISTERS OF h63 IN CONSECUTIVE JANUARIES** (the 1911 №1 Katarina × Papič h31 + the 1912 №1 Barbara × Lozar h78 — both daughters of Nikolaj Križan × Katarina née Pezdirec; **the P140-lead 'sisters?' → CONFIRMED BY THE CORPUS** [the baptisms Jan 20, 1887 + Jun 20, 1889 at h63!]) + **★★★ №8 THE DOUBLE CORPUS SYNCHRONIZATION** (the groom's parents = **the 1891 №12 Jakša × Jakša** + the bride's parents = **the 1890 №2 Schweiger × Jakša** — BOTH PARENT COUPLES OF THE GROOM AND THE BRIDE ALREADY IN THE CORPUS = the 1st such case!) + **★★ №9 A 46-YEAR-OLD BRIDE** (Barbara Straus a cottager of Griblje h46 — the 2nd oldest after the 1886-v1 56; the couple 31+46; h46 = the 3rd marriage evidence [the 1909 №11 the INTRA-h46!]) + **★★ №17 the 1913 CORPUS SYNC** (the son Julij baptized Aug 8, 1913 at Griblje h31 'Jožef Černič × Ana Počelf [=Požek]' — THE COUPLE + THE MOVE CONFIRMED!; the bride's baptism Apr 3, 1890 Janez Požek × Ana Šimec = the age 22 ✓; the POŽEKS = the ADLEŠIČ SEXTONS!) + **★★ №4+№6 the JAKOFČIČ TWIN** (the brother-groom Nikolaj of Čerkvišče 16 + the sister-bride Ana of Čerkvišče 17 — the children of Peter Jakofčič; the weddings Jan 29 + Feb 12!) + **★★ the HRAŠINOVIČ TWIN** (№6 Nikolaj 24 of Krasinec 20 + №16 Nikolaj 49 of Krasinec 32 — the fathers Anton + Janez + the №1 mother Barbara née Harasinč = the 3rd Harasin appearance of the year!) + **★★ the ŠTRAVS/STRAUS NETWORK ×4** (№9+№10+№15 brides + the witness Jožef = **3 Straus brides in 1 year = A RECORD!**) + **★ the MASS-DAYS ×3** (Jan 29 №2+№3+№4 TRIPLE + Feb 12 №6+№7 + May 20 №11+№12 = 6/17 on shared days!) + **★ NEW AUTHORITIES** (the ČRNOMELJ COURT №17 — the 1st of the line! + the military district command №8 [Jan 16, 1912 — the pre-war year!] + the Ljubljana provincial government №5 no. 2846? [the 2nd after the 1910 №17] + the Radovica documents №13 [another parish!] + the ordinariate no. 5473 [~]) + **★ №13 ALFRED a shop assistant [~] of Podzemelj 11** (the 1st Latin-script name of the line! + a German surname [Kerschbaumer? ~ 6 reading variants] + the KURE witnesses + perhaps a 4th-degree dispensation [both mothers née Kure? ~]) + **★ KRIVOGLAVCI the 3rd appearance** (the 1898 №4 + the 1911 №12 + the 1912 №14!) + **★ NEW OCCUPATIONS** (a cobbler! + a shop assistant + a woodcutter + a joiner + a cottager/cottageress ×3 + a sexton) + **~18 NEW SURNAMES** (Lozar, Jurjevič, Justarič, Harasinovič-groom, Švajgar-Slovenian, Marencič, Vukšinič, Filak-mother, Škalič, Perdih, Pirc, Černič, Požek-bride, Rus-mother, Spudič? [~], Kerschbaumer? [~], Žofrca? [~], Bohle? [~]) + **the GENETIC VILLAGE 'Girišice' = GRIBLJE the 3rd appearance** (№15 h44!); the GRIBLJE weddings ×4 = **5 blocks** (№1 h78 groom **the 1st MARRIAGE EVIDENCE** [the 1915 corpus baptism of the couple at h78; ALREADY in p80 via the 1887 anchor!] + h63 bride the 2nd evidence [THE SISTERS!] + №9 h46 the 3rd evidence + №15 h44 [the Girišice-GENETIC!] + №17 h21); anomalies ×18; vitals **670 → 675** (+ 5 blocks); the 04455 blocks = **153 → 158**; p80 houses **69 → 70 (+h78 — the 04105-h78 1915+ baptisms outside the p80 filter!)**; the PT gap **13 (unchanged)**; the marriage anchors **146 → 151 (+1912:5)**; EXCLUDED: 4 (the empty bands s148–s151 + the s152-1913 boundary); the script scripts/p141_parish_marriage_1912.py (I1–I12); status SAMPLE-TRANSCRIPTION-M1912",
    p141Errors.length === 0,
    p141Errors.length === 0
      ? `17 vpisov · s148-dno + s149–s151 == Pag. 147–150 (27. potrditev!) + s152 = 1913-meja! · **★★★ RECIPROČNI DVOJNI PAR SOROJENCEV №11+№12 (Muc × Jakljevič — KRIŽNE hiše!)** · **★★★ INTRA-PRIIMEK ×2 (№7 Pezdirec + №14 Žugelj = REKORD!)** · **★★★ SESTRI KRIŽAN h63 (1911+1912 — lead VERIF!)** · **★★ №8 dvojna korpus-sinhro (1890 №2 + 1891 №12!)** · №9 nevesta 46! · №17 krst-1913 potrditev! · h78 NOVA (69→70!)`
      : p141Errors.join("; "),
  );

  // ——— qa-p142: POROČNA KNJIGA 04455 — polno leto 1913 (P142; 28. leto poročne linije) ———
  {
  const p142Errors: string[] = [];
  const p142Marr = HOUSE_VITALS.filter((h) => h.bookSignature === "04455" && h.year === 1913);
  if (p142Marr.length !== 6)
    p142Errors.push(`bloki 1913 (04455) ≠ 6 (${p142Marr.length} — 5 poroke: №2 h25 + №3 h53 + №6 h1 + №10 h76+h91 INTRA! + №11 h35 = 6!)`);
  const p142Houses = p142Marr.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
  if (p142Houses.join(",") !== "1,25,35,53,76,91")
    p142Errors.push(`hiše 1913 ≠ [1,25,35,53,76,91] — najdeno: ${p142Houses.join(",")} (P142: 5 GRIBLJE poroke — №10 h76 NOVA × h91 = 5. INTRA-GRIBLJE par! + №2 h25 + №3 h53 + №6 h1 + №11 h35 'Gorišice'!)`);
  const p142Pins: Array<[string, string]> = [
    ["25", "KORPUS-HIŠA"],
    ["53", "DVOTERNA KORPUS-SINHRONIZACIJA"], ["53", "KORPUS-KRST"], ["53", "PAR-KRSTI"],
    ["1", "Željko-družina"],
    ["76", "1. POROČNI DOKAZ"], ["76", "NOVA p80-hiša"], ["76", "VSEBOVANA POROKA"], ["76", "INTRA-GRIBLJE"],
    ["91", "KORPUS-KRST"], ["91", "INTRA-GRIBLJE"], ["91", "VSEBOVANA POROKA"],
    ["35", "GENETSKA-VAS"],
  ];
  for (const [hn, pin] of p142Pins) {
    const ms = HOUSE_VITALS.filter((h) => h.houseNo === hn && h.bookSignature === "04455" && h.year === 1913).map((h) => h.whatSi);
    if (!ms.some((m) => m && m.toLowerCase().includes(pin.toLowerCase())))
      p142Errors.push(`pin h${hn} 1913 (${pin}) manjka!`);
  }
  if (!p142Marr.some((h) => h.whatSi.includes("INTRA-GRIBLJE")))
    p142Errors.push("★★★ INTRA-GRIBLJE №10 (h76 × h91 — 5. intra-vasični par linije!) manjka");
  if (!p142Marr.some((h) => h.whatSi.includes("GENETSKA-VAS")))
    p142Errors.push("★★★ GENETSKA-VAS 'Gorišice' = Griblje 4. pojav (№11 h35!) manjka");
  if (HOUSE_VITALS.length !== 685)
    p142Errors.push(`HOUSE_VITALS ≠ 681 (${HOUSE_VITALS.length} — P141: 675; P142: + 6 blokov 1913 = 681!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length !== 168)
    p142Errors.push(`bloki 04455 ≠ 164 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length} — P141: 158; P142: + 6 blokov 1913 = 164!)`);
  push(
    "qa-p142-parish-marriage-1913",
    "P142: ŽUPNIJA PODZEMELJ — POROČNA KNJIGA 04455, POLNO LETO 1913 (issue #18; SAMPLE-TRANSCRIPTION-M1913; 28. leto poročne linije P115 = 1886 → … → P142 = 1913): okvir POTRJEN — s152–s154-top == Pag. 151–153 (Pag. == sken − 1, **28. potrditev**; velja 61–154) + **s154 y≈780 = rokopisna letna glava »1914« = meja leta DOKAZANA — 1. letna glava po 1908!** (+ »/1913« na s152 y≈50); **1913 = 13 vpisov** (№1–6 s152 + №7–11 s153 + №12–13 s154-top; štetje: STRIP + overview + zaporedje + meja; P141-lead je poznal samo №1!); **9 PON + 4 NED = 13/13 VIKENDI — 1. POPOLOMA vikend-leto po 1907!**; **postna vrzel 27.1. → 31.3.** (post 5.2.–23.3. — 3. zapored: 1911+1912+1913); **0 masa-dnevov** (1. leto brez skupnega dne po 2010!); **1913 = isti slovenski pisar kot 1912 (najhitrejša pisava linije) + SISTEMSKA H/K/M-INITIAL CONFUSION** (Klepec/Hlepec/Hlebec · Kralj/Hvali/Mal/Mali · Kapljišče/Harpišče · Krasinec/Hrašinec · Macel/Mavrel — vsaka H/M-iniciala zahteva korpus-križ!); **VELIKE NOVELE P142**: **★★★ №13 INTRA-KRALJ + 1. DISPENSA 3. KOLENA** (Jožef Kralj Mlake 10, 23, mladoletnik × Neža Kralj Kapljišče 8, 18, mladoletna — **4. intra-priimek poroka linije** [1910 Jakobčič · 1912 Pezdirec + Žugelj · 1913 Kralj] + **dispenza 3. kolena enake stranske veze — ORDINARIAT LJUBLJANA 31/10.1913 št. 47845 = 1. v liniji** [1907 je bila 2. kolena!] + priglas polnoletnosti ženina — podčastništvo Metlika 28/10.1913 + ustno očetovo dovoljenje za nevesto!) + **★★★ №13 DVOJNI 1911-KORPUS-ANKER** (ženinovi starši **Jurij Kralj ½ × Ana Pezdirec** = 1911 №6 starša [Georg Kralj × Anna Pezdirec — Jožef = brat Mathiasa!] + nevestini starši **Matija Kralj ¼ × Ana Klepec** = 1911 №13 starša [Neža = sestra Matije + ISTA HIŠA Kapljišče 8!] — **dve 1911-družini v enem vpisu!**) + **★★★ №3 DVOTERNA KORPUS-SINHRONIZACIJA PEZDIREC** (nevesta **Marjeta Pezdirec Griblje 53** = korpus-krst 14.8.1891 h53 [Janez Pezdirec ¼ × Marija Križan — starost 21 ✓ + ISTA HIŠA!] + **par-krsti 1915 [sin Janez h53 'Jure Dragos × Marjeta Pezdirc'!] in 1918 [sin Nikolaj h53!] = PAR + PRESELITEV NA NEVESTINO HIŠO ×2!**) + **★★★ №10 INTRA-GRIBLJE h76 × h91 + VSEBOVANA POROKA** (ženin Janko Vranešič Griblje 76, 20, mladoletnik — **h76 = 1. POROČNI DOKAZ + NOVA p80-hiša 69. → 70.!** [04105-h76-krst 1913 izven p80-filtra] × nevesta Alojzija Mlec Griblje 91, 20, mladoletna — **korpus-krst 9.5.1893 h91 [Janez M[uc→Mlec!] × Ana Kure — starost 20 ✓]** = **5. intra-vasični par linije** [1910 №1 + 1911 №1+№2 + 1912 №1 + 1913 №10!] + **hčer Vilhelmina krščena 9.9.1913 h76 = rojena 7 tednov po poroki — VSEBOVANA POROKA!** [nevra noseča ~2 meseca — obe mladoletni; proglaš polnoletnosti neveste — sodišče Črnomelj 26/6.1913!]) + **★★ №11 GENETSKA-VAS 'Gorišice' = GRIBLJE 4. pojav** (ženin Rajmund **ČEVELJAK** [~ 'Čeh' — 1. ime RAJMUND v liniji (latinsko!)] Gorišice 35 = h35 — 1910+1911+1912 'Giriči/Girišice' + 1913 'Gorišice'!) + **★★ №1 DATUMSKA ANKETA** (3 nasprotujoča branjа: '24.1.' STRIP / 'junij 27' OV / '27.1.' lead — **rešeno: dokument 25/1.1913 št. 12 + PONEDELJEK + P141-lead = 27.1.1913!** [jan/jun-zmeda = pisarjeva a/u poteza]; ženin Matija **JUVANČIČ** [~ 'Janževič' ×4 L-branjа — priimek po očetu Juriju Juvančiču + korpus 1903 h24!] × Marija **MACEL** [~ Mavrel/Mačele — 95 % zoom] Zemelj 33) + **★★ PEZDIREC-MREŽA ×7** (№3 nevesta + №8 mati + №12 mati [~ 'Pekdinec' = Pezdirec-varianta kot korpusni 'Perdinec'!] + №13 mati + priči №8 Martin+Janez [brata?!] + priča №13 Peter ½ [= korpus h20!] = **7 Pezdirec-oseb = rekord enega priimka v letu**) + **★★ JUVANČIČ ×2** (№1 ženin Matija [oče Jurij] + №5 nevesta Ana [oče Nikolaj] — prvi priimek leta z obema stranema poroke!) + **★ №12 NAJSTAREJŠI PAR LETA** (Janez Simončič Kloster 82 bajtar **66 let** [2. najstarejši ženin linije!] × Ana **ŽITAV** [~ 'Šitar/Litar/Lojtarjeva' — razrešeno z očetom **Franc Žitav bajtar**!] Zemelj 42, 44 — **110 let skupaj!**) + **★ №9 DRUGO-ŽUPNIJSKI ŽENIN** (Jožef Štukelj iz **Petrove vasi (župnija Črnomelj)** × Ana Žunič Krasinec 10 + korpus-1918 [~]: 'Jožef Štucelj h44 × Barbara Tome' — morda isti mož po 2. zakonu!) + **★ NOVE OBLASTI** (**ORDINARIAT LJUBLJANA dispenza — 1. v liniji!** + podčastništvo Metlika + kr. kotarsko sodišče Bela Krajina št. 2165 + škofni urad Črnomelj št. 239 + župnijski urad Metlika št. 155 + **župni urad VINICA št. 26 — drugo-župnijski!** + izpostava Podnanos [~] + [Stari trg pri Ptuju? ~ — najbolj oddaljena oblast linije!]) + **★ NOVI POKLICI** (**c.k. poštar №7 Fran Šoflak — 1. poštar linije!** + prostovoljka [~] + kovač-posestnik [dvojni poklic očeta №7]) + **~16 NOVIH PRIIMKOV** (Macel, Vasić, Mihelčič, Jesih, Marovšič [~ 8 VARIANT — najtrša beseda leta!], Šoflak, Polda, Miklavčič, Štukelj, Vranešič, Mlec, Čeveljak [~], Režek, Simončič, Žitav, Juvančič-poročna-prvojavitev) + **7 MLADOLETNIH OSEB — REKORD** (№4 17! + №8 21+22 + №10 20+20 + №13 23+18 — sproščnice/priglasi v №8+№10+№13); GRIBLJE poroke ×5 = **6 blokov** (№2 h25 nevesta [korpus-hiša 1896!] + №3 h53 [DVOTERNA SINHRO!] + №6 h1 [Željko-družina — Marijeta r. ~1890 = prvi otrok!] + №10 h76 ženin [NOVA p80!] + h91 nevesta [korpus 1893!] + №11 h35 [GENETSKA-VAS!]); anomalije ×15; vitals **675 → 681** (+ 6 blokov); bloki 04455 = **158 → 164**; p80 hiše **69 → 70 (+h76!)**; PT luknja **13 (h76 = nabor 61–99 — nespremenjena)**; poročna sidra **151 → 157 (+1913:6)**; EXCLUDED: 1 (letna glava »1914« s154 — P143-lead: 1914 №1 = 9.2. Jožef Pajzar Hlošča 54 × Ana Lipovec GRIBLJE 46 + 3–4 INTRA-GRIBLJE poroke 1914 — rekordno leto prihaja!); skripta scripts/p142_parish_marriage_1913.py (I1–I12); status SAMPLE-TRANSCRIPTION-M1913",
    "P142: THE PARISH OF PODZEMELJ — MARRIAGE REGISTER 04455, THE FULL YEAR 1913 (issue #18; SAMPLE-TRANSCRIPTION-M1913; the 28th year of the marriage line P115 = 1886 → … → P142 = 1913): the framework CONFIRMED — s152–s154-top == Pag. 151–153 (Pag. == scan − 1, **the 28th confirmation**; valid 61–154) + **s154 y≈780 = the handwritten year heading »1914« = the year boundary PROVEN — the 1st annual heading since 1908!** (+ »/1913« at s152); **1913 = 13 entries** (№1–6 s152 + №7–11 s153 + №12–13 s154-top; the count: the STRIP + the overview + the sequence + the boundary; the P141 lead knew only №1!); **9 MON + 4 SUN = 13/13 WEEKENDS — the 1st complete weekend year since 1907!**; **the Lent gap Jan 27 → Mar 31** (the Lent Feb 5–Mar 23 — the 3rd consecutive: 1911+1912+1913); **0 mass-days** (the 1st year without a shared day since 1910!); **1913 = the same Slovenian scribe as 1912 (the fastest hand of the line) + the SYSTEMATIC H/K/M-INITIAL CONFUSION** (Klepec/Hlepec/Hlebec · Kralj/Hvali/Mal/Mali · Kapljišče/Harpišče · Krasinec/Hrašinec · Macel/Mavrel — every H/M-initial word requires a corpus cross!); **THE BIG P142 NOVELTIES**: **★★★ №13 the INTRA-KRALJ + the 1st 3rd-DEGREE DISPENSATION** (Jožef Kralj of Mlake 10, 23, a minor × Neža Kralj of Kapljišče 8, 18, a minor — **the 4th intra-surname wedding of the line** [1910 Jakobčič · 1912 Pezdirec + Žugelj · 1913 Kralj] + **the dispensation of the 3rd degree of a collateral line — the LJUBLJANA ORDINARIATE Oct 31, 1913 no. 47845 = the 1st of the line** [1907 was the 2nd degree!] + the groom's majority declaration — the Metlika sub-office Oct 28, 1913 + the father's oral consent for the bride!) + **★★★ №13 the DOUBLE 1911 CORPUS ANCHOR** (the groom's parents **Jurij Kralj ½ × Ana Pezdirec** = the 1911 №6 parents [Jožef = the brother of Mathias!] + the bride's parents **Matija Kralj ¼ × Ana Klepec** = the 1911 №13 parents [Neža = the sister of Matija + THE SAME HOUSE Kapljišče 8!] — **two 1911 families in one entry!**) + **★★★ №3 the DOUBLE-ANCHOR CORPUS SYNCHRONIZATION of PEZDIREC** (the bride **Marjeta Pezdirec of Griblje 53** = a corpus baptism Aug 14, 1891 at h53 [Janez Pezdirec ¼ × Marija Križan — the age 21 ✓ + THE SAME HOUSE!] + **the couple's baptisms 1915 [the son Janez at h53 'Jure Dragos × Marjeta Pezdirc'!] and 1918 [the son Nikolaj at h53!] = THE COUPLE + THE MOVE TO THE BRIDE'S HOUSE twice!**) + **★★★ №10 the INTRA-GRIBLJE h76 × h91 + A SHOTGUN WEDDING** (the groom Janko Vranešič of Griblje 76, 20, a minor — **h76 = the 1st MARRIAGE EVIDENCE + a NEW p80 house, the 69th → 70th!** [the 04105-h76 baptism of 1913 outside the p80 filter] × the bride Alojzija Mlec of Griblje 91, 20, a minor — **a corpus baptism May 9, 1893 at h91 [Janez M[uc→Mlec!] × Ana Kure — the age 20 ✓]** = **the 5th intra-village couple of the line** + **the daughter Vilhelmina baptized Sep 9, 1913 at h76 = born 7 weeks after the wedding — A SHOTGUN WEDDING!** [the couple ~2 months pregnant — both minors; the bride's majority declaration — the Črnomelj court Jun 26, 1913!]) + **★★ №11 the GENETIC VILLAGE 'Gorišice' = GRIBLJE the 4th appearance** (the groom Rajmund **ČEVELJAK** [~ 'Čeh' — the 1st name RAJMUND of the line (Latin!)] of Gorišice 35 = h35) + **★★ №1 the DATE INQUEST** (3 contradictory readings: 'Jan 24' the STRIP / 'June 27' the OV / 'Jan 27' the lead — **solved: the document Jan 25, 1913 no. 12 + MONDAY + the P141 lead = Jan 27, 1913!**; the groom Matija **JUVANČIČ** [~ 'Janževič' 4 L-readings — the surname after the father Jurij Juvančič + the 1903 corpus h24!] × Marija **MACEL** [~ Mavrel/Mačele — a 95 % zoom] of Zemelj 33) + **★★ the PEZDIREC NETWORK ×7** (№3 bride + №8 mother + №12 mother [~ 'Pekdinec' = a Pezdirec variant like the corpus 'Perdinec'!] + №13 mother + the №8 witnesses Martin+Janez [brothers?!] + the №13 witness Peter ½ [= the corpus h20!] = **7 Pezdirec persons = the record of one surname in a year**) + **★★ JUVANČIČ ×2** (№1 the groom Matija [father Jurij] + №5 the bride Ana [father Nikolaj] — the 1st surname of the year on both sides of a wedding!) + **★ №12 the OLDEST COUPLE OF THE YEAR** (Janez Simončič of Kloster 82 a cottager **66** [the 2nd oldest groom of the line!] × Ana **ŽITAV** [~ 'Šitar/Litar/Lojtarjeva' — solved through the father **Franc Žitav a cottager**!] of Zemelj 42, 44 — **110 years together!**) + **★ №9 an ANOTHER-PARISH GROOM** (Jožef Štukelj from **Petrova vas (the Črnomelj parish)** × Ana Žunič of Krasinec 10 + the 1918 corpus [~]: 'Jožef Štucelj h44 × Barbara Tome' — perhaps the same man after a 2nd marriage!) + **★ NEW AUTHORITIES** (**the LJUBLJANA ORDINARIATE dispensation — the 1st of the line!** + the Metlika sub-office + the royal district court of Bela Krajina no. 2165 + the episcopal office of Črnomelj no. 239 + the Metlika parish office no. 155 + **the VINICA parish office no. 26 — another parish!** + the Podnanos post [~] + [Stari trg pri Ptuju? ~ — the most distant authority of the line!]) + **★ NEW OCCUPATIONS** (**a k.k. postman №7 Fran Šoflak — the 1st postman of the line!** + a volunteer [~] + a smith-farmer [the father №7's double occupation]) + **~16 NEW SURNAMES** (Macel, Vasić, Mihelčič, Jesih, Marovšič [~ 8 VARIANTS — the hardest word of the year!], Šoflak, Polda, Miklavčič, Štukelj, Vranešič, Mlec, Čeveljak [~], Režek, Simončič, Žitav, Juvančič-the marriage first-appearance) + **7 MINORS — A RECORD** (№4 17! + №8 21+22 + №10 20+20 + №13 23+18 — the majority declarations in №8+№10+№13); the GRIBLJE weddings ×5 = **6 blocks** (№2 h25 bride [a corpus house 1896!] + №3 h53 [the DOUBLE-ANCHOR SYNC!] + №6 h1 [the Željko family — Marijeta b. ~1890 = the first child!] + №10 h76 groom [a NEW p80!] + h91 bride [the corpus 1893!] + №11 h35 [the GENETIC VILLAGE!]); anomalies ×15; vitals **675 → 681** (+ 6 blocks); the 04455 blocks = **158 → 164**; p80 houses **69 → 70 (+h76!)**; the PT gap **13 (h76 = the 61–99 set — unchanged)**; the marriage anchors **151 → 157 (+1913:6)**; EXCLUDED: 1 (the year heading »1914« s154 — the P143 lead: the 1914 №1 = Feb 9 Jožef Pajzar of Hlošča 54 × Ana Lipovec of GRIBLJE 46 + 3–4 INTRA-GRIBLJE weddings of 1914 — a record year coming!); the script scripts/p142_parish_marriage_1913.py (I1–I12); status SAMPLE-TRANSCRIPTION-M1913",
    p142Errors.length === 0,
    p142Errors.length === 0
      ? `13 vpisov · s152–s154-top == Pag. 151–153 (28. potrditev!) + letna glava »1914« = meja! · 9 PON + 4 NED = 13/13 VIKENDI! · **★★★ №13 INTRA-KRALJ + 1. dispenza 3. kolena (ordinariat Ljubljana!)** · **★★★ №3 Marjeta Pezdirec h53 DVOTERNA sinhiro (krst 1891 + par 1915/1918!)** · **★★★ №10 INTRA-GRIBLJE h76 × h91 + VSEBOVANA POROKA (hčer 7 tednov po!)** · №11 'Gorišice' = Griblje 4.! · №1 datumska anketa (27.1.!) · h76 NOVA (69→70!)`
      : p142Errors.join("; "),
  );

  const p143Errors: string[] = [];
  const p143Marr = HOUSE_VITALS.filter((h) => h.bookSignature === "04455" && h.year === 1914);
  if (p143Marr.length !== 4)
    p143Errors.push(`bloki 1914 (04455) ≠ 4 (${p143Marr.length} — 3 INTRA-GRIBLJE poroke: №3 h91+h68 + №4 h68 ISTA-HIŠA! + №5 h65+h31 = 4 bloki!)`);
  const p143Houses = p143Marr.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
  if (p143Houses.join(",") !== "31,65,68,91")
    p143Errors.push(`hiše 1914 ≠ [31,65,68,91] — najdeno: ${p143Houses.join(",")} (P143: 3 INTRA-GRIBLJE — №3 h91 × h68 + №4 h68 × h68 ISTA HIŠA! + №5 h65 × h31!)`);
  const p143Pins: Array<[string, string]> = [
    ["91", "PREDKORPUSNA generacija"], ["91", "NOVA p80-hiša"], ["91", "INTRA-GRIBLJE"], ["91", "korpus Muc-družina"],
    ["68", "ISTA-HIŠA"], ["68", "NAJSTAREJŠI ŽENIN"], ["68", "MATI-IN-SIN"],
    ["65", "KORPUS-KRST"], ["65", "DVOTERNA KORPUS-SINHRONIZACIJA"],
    ["31", "SEJEM SELITEV"], ["31", "INTRA-GRIBLJE"],
  ];
  for (const [hn, pin] of p143Pins) {
    const ms = HOUSE_VITALS.filter((h) => h.houseNo === hn && h.bookSignature === "04455" && h.year === 1914).map((h) => h.whatSi);
    if (!ms.some((m) => m && m.toLowerCase().includes(pin.toLowerCase())))
      p143Errors.push(`pin h${hn} 1914 (${pin}) manjka!`);
  }
  if (!p143Marr.some((h) => h.whatSi.includes("ISTA-HIŠA")))
    p143Errors.push("★★★ №4 ISTA-HIŠA poroka h68 × h68 (1. v celi liniji!) manjka");
  if (!p143Marr.some((h) => h.whatSi.includes("MATI-IN-SIN")))
    p143Errors.push("★★★ №4+№5 MATI-IN-SIN poročna tedna (8 dni narazen!) manjka");
  if (HOUSE_VITALS.length !== 685)
    p143Errors.push(`HOUSE_VITALS ≠ 685 (${HOUSE_VITALS.length} — P142: 681; P143: + 4 bloki 1914 = 685!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length !== 168)
    p143Errors.push(`bloki 04455 ≠ 168 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length} — P142: 164; P143: + 4 bloki 1914 = 168!)`);
  push(
    "qa-p143-parish-marriage-1914",
    "P143: ŽUPNIJA PODZEMELJ — POROČNA KNJIGA 04455, POLNO LETO 1914 (issue #18; SAMPLE-TRANSCRIPTION-M1914; 29. leto poročne linije P115 = 1886 → … → P143 = 1914): okvir POTRJEN — s154-dno + s155 == Pag. 153–154 (Pag. == sken − 1, **29. potrditev**; velja 61–155) + **meja 1914/1915 DOKAZANA: s155-dno = 2 prazna pasova + diagonala + s156 = letna glava »1915«**; **1914 = 7 vpisov** (№1–3 s154-dno + №4–7 s155; štetje: STRIP + overview + zaporedje + meja); **3 PON + 3 NED + 1 TOR = 6/7 VIKENDOV** (№7 7. 7. = **1. torek po 1912 №1** — hiper-zoom ×4 »7 z zastavico« vs STRIP »12. 7.«!); **postna vrzel 22. 2. → 3. 5.** (post 25. 2.–11. 4. — 4. zapored); ★★★ **WWI-LUKNJA: zadnja poroka 7. 7. 1914 → 1915 №1 šele 2. 5. 1915 = 10-MESEČNA VRZEL — Avstrija napove vojno Srbiji 28. 7. 1914 (3 tedne po №7!) = 1. ZLOM KONTINUITETE LINIJE 1886–1914!**; **VELIKE NOVELE P143**: **★★★ №4+№5 MATI-IN-SIN POROČNA TEDNA** (№4 3. 5.: Ivan Mih h68 **71 = NAJSTAREJŠI ŽENIN CELE LINIJE** [prej 66 = 1913 №12!] × **Katarina geb. Požek, MILEKOVA VDOVA** 48 [vdova Matija Mileka st. h65!] + №5 11. 5. — **8 DNI ZA №4**: NJUN SIN **Anton Milek** 21 × Barbara Straus 19 — **mati se poroči, sin 8 dni za njo!** + №4-nevestini starši Matija Požek ¼ × Marija geb. Pezdirec = Požek×Pezdirec-rod = №5-matina družina!) + **★★★ №4 ISTA-HIŠA poroka h68 × h68 — 1. TAK PRIMER V CELI LINIJI 1886–1914!** + par 71 × 48 = **119 let skupaj = 2. rekord** (za 134 P128 v1!) + **★★★ №4 KRONOLOŠKA REŠITEV MILEK-h65 (2 GENERACIJI!)** (M1903 №3 »Matthias Milek h65 (25!) × Maria Huestič« = **SIN** → korpus-otroci h65 1887–1901 [mati Katarina geb. Požek = STAREŠI par] + 1904–1913 [mati Marija geb. Hrišič = SINOV par] → Katarina [r. ~1866] je lahko živa 1914 kot vdova = №4-nevesta [48 ✓]!) + **★★★ 3 INTRA-GRIBLJE poroke = REKORD LINIJE** (№3 h91 × h68 + №4 h68 × h68 + №5 h65 × h31 — prejšnji maks 2 = 1911!) + **★★★ №5 DVOTERNA KORPUS-SINHRONIZACIJA** (ženin **Anton Milek = korpus-krst 1893 h65** [Matija Milek ½ × Katarina Požek — starost 21 ✓ ISTA HIŠA!] + nevesta **Barbara Straus = korpus-krst 1894 h71** [Jurij Straus ¼ × Barbara Jakobčič — starost 19 ✓] = **2. »dvoterna« po 1913 №3!** + **SEJEM SELITEV Straus h71 → h31** [6× hiper-zoom hiša 31!]) + **★★ MLAJKOVA-MREŽA ×2** (№3 nevesta **Marija Mlakova** 44 h68 [hčer Janeza Mlaka 1/8 × Marija geb. ŽITAV — 2. pojav Žitav po 1913 №12!] + №6 nevesta **Marija geb. Jakobčič, MLAKOVA VDOVA** 55 [Dobravice 5] — **MLAK = 1. PRAVI POJAV priimka** [1913 №13 »Mlak« je bil zmeda za Kralj!]!) + **★★ №7 ROJSTNA DATUMA-novini** (ženin Matija Cajnar »12. VII. 1879« = **poroka NA 35. ROJSTNI DAN!** + nevesta Ana Brodarič »8. XII. 1885« — **1. rojstna datuma v blokih celotne linije** [pisarjeva novina 1914!] + INTRA-KRASINEC h8 × h7 sosednji hiši!) + **★★ №7 TOR-izjema** (7. 7. [hiper-zoom ×4 enoglasno »7 z zastavico, NE 12 NE 8« vs STRIP »12. 7.« + ov »8. 7.«] — koledarska NED-hipoteza [12. 7.] nerazrešena do konca [~ VERIF]) + **★★ №1 SEGINA-ANKETA (5 variant!)** (branjа Lipovec/Straus/Jegliča/Legina/**Segina** — **S/J/L-INITIAL CONFUSION**! + korpus h70/h30 Nikolaj Segina × Marjeta geb. Milek: Ani 1893+1899 — a starost 19 ≠ 21/15 + »(ž.) Adlešiči« → **adlešiška Segina-veja [~ VERIF]** + mladoletna dekle/služabnica [~] na Brodaričevi h46! + »dovoljenje za ml. nevesto« ✓ [avstrijska polnoletnost 24!]) + **★★ 3 VDOVSKI vpisi** (№2 ženin Holbec vdovec + №4 + №6 nevesti vdovi — **rekord linije** [prej 1–2/leto!] + №6 par 42 × 55 [13-letna razlika!]) + **★ №2 HOLBEC ×3 POTRJEN** (branjа Fojek/Votovec = **F/H/V-INITIAL CONFUSION**! + »Loka« = OTOK!) + **★ №2 LEOPOLD »župni upravitelj« — NOV DUHOVNIŠKI PODPIS** (1. »Leopold« v liniji [~ VERIF]) + **★ NOVE OBLASTI** (**DEKANIJA METLIKA 10. VII. št. 148 — 1.!** + županstvo V GRIBLJAH 21/2. št. 11 [1. po 1903?] + županstvo DOBRAVICE [~] + škof Ljubljana št. 3 + deželna vlada št. [12648 ~] + župno sodišče Črnomelj št. 69) + **★ NOVI POKLICI** (finančni spravnik [priča Franc Müller ~] — 1.! + gostilničar + kovač [~ №3 Janez Muc]) + **~6 NOVIH PRIIMKOV** (Pajzar [~], Holbec [~], Mih [~], Mlak, Cajnar [~], Željko-poročna-prvojavitev) + **№1 »HLOŠČA« = KLOSTER 2. pojav** (ista H/K-precitljivost pisarja po 1913 №12!) + **M-PRIIMKI 5-družinska zmeda** (Muc/Milek/Mlak/Mih/Mikc — vsak M-priimek zahteva korpus-križ!); GRIBLJE poroke ×3 = **4 bloki** (№3 h91 ženin [PREDKORPUSNA generacija 47!] + h68 nevesta [NOVA p80-hiša 70. → 71.!] + №4 h68 ISTA-HIŠA! + №5 h65 ženin [korpus-krst 1893!] + h31 nevesta [korpus-krst 1894 h71 → selitev!]); anomalije ×13; vitals **681 → 685** (+ 4 bloki); bloki 04455 = **164 → 168**; p80 hiše **70 → 71 (+h68!)**; poročna sidra **157 → 161 (+1914:4)**; EXCLUDED: 0 (s155-dno prazna + diagonala = čista meja!); P144-lead: 1915 №1 = 2. 5. Peter Vrebec [~] tesar Griblje 82 × Terezija Muc ISTA-HIŠA h82 + №2 protestant Anton Brodarič Krasinec 35 × Barbara Segina Čerkvišče 22 [PROTESTANTSKA poroka — 1. po letih! + Segina 2. pojav!] + №3 Jakob Hošec? [~] Dobravice 48 × Katarina Hudorovič? ISTA-HIŠA h48 + VOJAK NA DOPUSTU — **1915 = 3 vpisi = najšibkejše leto linije (VOJNA!)**; skripta scripts/p143_parish_marriage_1914.py (I1–I12); status SAMPLE-TRANSCRIPTION-M1914",
    "P143: THE PARISH OF PODZEMELJ — MARRIAGE REGISTER 04455, THE FULL YEAR 1914 (issue #18; SAMPLE-TRANSCRIPTION-M1914; the 29th year of the marriage line P115 = 1886 → … → P143 = 1914): the framework CONFIRMED — s154-bottom + s155 == Pag. 153–154 (Pag. == scan − 1, **the 29th confirmation**; valid 61–155) + **the 1914/1915 boundary PROVEN: the s155 bottom = 2 empty bands + a diagonal + s156 = the year heading »1915«**; **1914 = 7 entries** (№1–3 s154-bottom + №4–7 s155; the count: the STRIP + the overview + the sequence + the boundary); **3 MON + 3 SUN + 1 TUE = 6/7 WEEKENDS** (№7 Jul 7 = **the 1st Tuesday since the 1912 №1** — a hyper-zoom ×4 »7 with a flag« vs the STRIP »Jul 12«!); **the Lent gap Feb 22 → May 3** (the Lent Feb 25–Apr 11 — the 4th consecutive); ★★★ **THE WWI GAP: the last marriage Jul 7, 1914 → the 1915 №1 only May 2, 1915 = a 10-MONTH VOID — Austria declares war on Serbia Jul 28, 1914 (3 weeks after №7!) = THE 1ST BREAK OF THE LINE'S CONTINUITY 1886–1914!**; **THE BIG P143 NOVELTIES**: **★★★ №4+№5 A MOTHER-AND-SON WEDDING WEEK** (№4 May 3: Ivan Mih of h68 **71 = THE OLDEST GROOM OF THE WHOLE LINE** [before: 66 = the 1913 №12!] × **Katarina née Požek, MILEK'S WIDOW** 48 [the widow of Matija Milek sr. of h65!] + №5 May 11 — **8 DAYS AFTER №4**: THEIR SON **Anton Milek** 21 × Barbara Straus 19 — **the mother marries, the son 8 days after her!** + the №4 bride's parents Matija Požek ¼ × Marija née Pezdirec = the Požek×Pezdirec lineage = the №5 mother's family!) + **★★★ №4 a SAME-HOUSE marriage h68 × h68 — THE 1ST SUCH CASE IN THE WHOLE LINE 1886–1914!** + the couple 71 × 48 = **119 years together = the 2nd record** (after 134 P128 v1!) + **★★★ №4 the CHRONOLOGICAL SOLUTION of MILEK-h65 (2 GENERATIONS!)** (the M1903 №3 »Matthias Milek of h65 (25!) × Maria Huestič« = **THE SON** → the corpus children of h65 1887–1901 [the mother Katarina née Požek = the SENIOR couple] + 1904–1913 [the mother Marija née Hrišič = the son's couple] → Katarina [b. ~1866] can be alive in 1914 as a widow = the №4 bride [48 ✓]!) + **★★★ 3 INTRA-GRIBLJE marriages = THE LINE RECORD** (№3 h91 × h68 + №4 h68 × h68 + №5 h65 × h31 — the previous max 2 = 1911!) + **★★★ №5 a DOUBLE-ANCHOR CORPUS SYNCHRONIZATION** (the groom **Anton Milek = a corpus baptism 1893 at h65** [Matija Milek ½ × Katarina Požek — the age 21 ✓ THE SAME HOUSE!] + the bride **Barbara Straus = a corpus baptism 1894 at h71** [Jurij Straus ¼ × Barbara Jakobčič — the age 19 ✓] = **the 2nd 'double' after the 1913 №3!** + **THE STRAUS MOVE h71 → h31** [a 6× hyper-zoom house 31!]) + **★★ the MLAK NETWORK ×2** (the №3 bride **Marija Mlakova** 44 of h68 [the daughter of Janez Mlak 1/8 × Marija née ŽITAV — the 2nd appearance of Žitav after the 1913 №12!] + the №6 bride **Marija née Jakobčič, MLAK'S WIDOW** 55 [of Dobravice 5] — **MLAK = the 1st REAL appearance of the surname** [the 1913 №13 'Mlak' was a confusion for Kralj!]!) + **★★ №7 TWO BIRTH-DATE NOVELTIES** (the groom Matija Cajnar »Jul 12, 1879« = **married ON HIS 35th BIRTHDAY!** + the bride Ana Brodarič »Dec 8, 1885« — **the 1st birth dates in the blocks of the whole line** [the scribe's 1914 novelty!] + an INTRA-KRASINEC h8 × h7 neighboring houses!) + **★★ №7 the TUESDAY exception** (Jul 7 [a hyper-zoom ×4 unanimous »7 with a flag, NOT 12, NOT 8« vs the STRIP »Jul 12« + the ov »Jul 8«] — the calendar SUN hypothesis [Jul 12] not fully resolved [~ VERIF]) + **★★ №1 the SEGINA INQUEST (5 variants!)** (the readings Lipovec/Straus/Jegliča/Legina/**Segina** — **an S/J/L-INITIAL CONFUSION**! + the corpus h70/h30 Nikolaj Segina × Marjeta née Milek: the two Anas 1893+1899 — but the age 19 ≠ 21/15 + »(ž.) Adlešiči« → **an Adlešiči Segina branch [~ VERIF]** + a minor servant girl [~] at the Brodarič h46! + »a permission for the minor bride« ✓ [the Austrian majority 24!]) + **★★ 3 WIDOW ENTRIES** (№2 the groom Holbec a widower + №4 + №6 widow brides — **the line record** [before 1–2/year!] + the №6 couple 42 × 55 [a 13-year gap!]) + **★ №2 HOLBEC ×3 CONFIRMED** (the readings Fojek/Votovec = **an F/H/V-INITIAL CONFUSION**! + »Loka« = OTOK!) + **★ №2 LEOPOLD »the parish administrator« — A NEW PRIESTLY SIGNATURE** (the 1st 'Leopold' of the line [~ VERIF]) + **★ NEW AUTHORITIES** (**the METLIKA DEANERY Jul 10 no. 148 — the 1st!** + the municipality IN GRIBLJE Feb 21 no. 11 [the 1st since 1903?] + the DOBRAVICE municipality [~] + the bishop of Ljubljana no. 3 + the provincial government no. [12648 ~] + the Črnomelj parish court no. 69) + **★ NEW OCCUPATIONS** (a financial officer [the witness Franc Müller ~] — the 1st! + an innkeeper + a smith [~ №3 Janez Muc]) + **~6 NEW SURNAMES** (Pajzar [~], Holbec [~], Mih [~], Mlak, Cajnar [~], Željko-the marriage first-appearance) + **№1 »HLOŠČA« = KLOSTER the 2nd appearance** (the same H/K misreading of the scribe after the 1913 №12!) + **the M-SURNAME 5-family confusion** (Muc/Milek/Mlak/Mih/Mikc — every M-surname requires a corpus cross!); the GRIBLJE weddings ×3 = **4 blocks** (№3 h91 groom [a PRE-CORPUS generation 47!] + h68 bride [a NEW p80 house, the 70th → 71st!] + №4 h68 the SAME-HOUSE! + №5 h65 groom [a corpus baptism 1893!] + h31 bride [a corpus baptism 1894 at h71 → the move!]); anomalies ×13; vitals **681 → 685** (+ 4 blocks); the 04455 blocks = **164 → 168**; p80 houses **70 → 71 (+h68!)**; the marriage anchors **157 → 161 (+1914:4)**; EXCLUDED: 0 (the s155 bottom empty + a diagonal = a clean boundary!); the P144 lead: the 1915 №1 = May 2 Peter Vrebec [~] a carpenter of Griblje 82 × Terezija Muc THE SAME HOUSE h82 + №2 the protestant Anton Brodarič of Krasinec 35 × Barbara Segina of Čerkvišče 22 [A PROTESTANT WEDDING — the 1st in years! + Segina the 2nd appearance!] + №3 Jakob Hošec? [~] of Dobravice 48 × Katarina Hudorovič? THE SAME HOUSE h48 + A SOLDIER ON LEAVE — **1915 = 3 entries = the weakest year of the line (THE WAR!)**; the script scripts/p143_parish_marriage_1914.py (I1–I12); status SAMPLE-TRANSCRIPTION-M1914",
    p143Errors.length === 0,
    p143Errors.length === 0
      ? `7 vpisov · s154-dno + s155 == Pag. 153–154 (29. potrditev!) + s155-dno prazna + diagonala = meja 1914/1915! · 3 PON + 3 NED + 1 TOR №7! · **★★★ №4+№5 MATI-IN-SIN poročna tedna (8 dni!)** · **★★★ №4 ISTA-HIŠA h68 × h68 (1. v liniji!) + ženin 71 = najstarejši!** · **★★★ 3 INTRA-GRIBLJE = REKORD!** · **★★★ №5 dvoterna sinhiro (krsta 1893 h65 + 1894 h71!)** · **★ WWI-luknja 7. 7. 1914 → 2. 5. 1915!** · h68 NOVA (70→71!)`
      : p143Errors.join("; "),
  );
  }
  }
}
