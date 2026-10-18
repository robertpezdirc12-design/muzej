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
if (p80Marr.length !== 11)
  p80Errors.push(`poročni vpisi (04455) ≠ 11 (${p80Marr.length})`);
if (p80Marr1886.length !== 7)
  p80Errors.push(`poročni okvir 1886 ≠ 7 vpisov (${p80Marr1886.length})`);
if (p80Marr1886.some((h) => !h.scan || h.scan < 61 || h.scan > 65 || h.page !== h.scan - 1))
  p80Errors.push("poročni okvir 1886: sken izven 61–65 ali Pag. ≠ sken − 1");
if (
  p80MarrAnchors.length !== 4 ||
  p80MarrAnchors.filter((h) => h.year === 1882).length !== 1 ||
  p80MarrAnchors.filter((h) => h.year === 1885).length !== 1 ||
  p80MarrAnchors.filter((h) => h.year === 1887).length !== 2
)
  p80Errors.push("poročna sidra ≠ 4 (1882:1 · 1885:1 · 1887:2)");
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
// PT klasifikacija celotnega vzorca (25 različnih hiš): 19 v naboru + 6 v luknji 41–60 (44, 54, 56, 57, 59, 60)
const p80Houses = new Set(p80All.map((h) => h.houseNo));
const P80_PT_GAP = ["44", "54", "56", "57", "59", "60"];
const p80Gap = [...p80Houses].filter((h) => P80_PT_GAP.includes(h));
if (p80Houses.size !== 25)
  p80Errors.push(`različnih hiš (vse tri knjige) ≠ 25 (${p80Houses.size})`);
if (p80Gap.length !== 6)
  p80Errors.push(`PT luknja ≠ 6 hiš (${p80Gap.length}: ${p80Gap.sort().join(",")})`);
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
  const allow = hn === "30" ? [1890, 1891, 1893, 1895, 1896, 1899, 1902, 1903, 1906, 1908, 1909] : hn === "90" ? [1890, 1892, 1898, 1900, 1908] : hn === "41" ? [1890, 1893, 1896, 1899] : hn === "7" ? [1890, 1901, 1905, 1907] : hn === "77" ? [1890, 1902, 1909] : [1890]; // P94: + 1899 bloka (h30 4. družina Županič; h41 4. VPIS ISTA ZVEZA); P95: + 1900 blok h90; P96: + 1901 blok h7 (2. VPIS); P97: + 1902 bloka h30 (5. DRUŽINA — SEGINA VRNITEV) + h77 (2. VPIS — MENJAVA Pošek → Cindrič); P98: + 1903 blok h30 (2. VPIS ZAPORED — Segina); P100: + 1905 blok h7 (3. VPIS — Jakob Toter, 1901 par); P101: + 1906 blok h30 (10. VPIS — MENJAVA Segina → Brinec); P102: + 1907 blok h7 (4. VPIS — ISTA Toter družina); P103: + 1908 bloka h30 (11. VPIS — SEGINA POVRAT) + h90 (5. VPIS — TRETJA učiteljska); P104: + 1909 bloka h30 (12. VPIS — 7. DRUŽINA Martinovič?) + h77 (3. VPIS — POŽEK POVRAT)
  if (HOUSE_VITALS.some((v) => v.houseNo === hn && !(v.bookSignature === "04105" && allow.includes(v.year))))
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
// h53: P93 kontinuiteta dovoli tudi blok 1898 (4. VPIS ISTA ZVEZA)
for (const hn of ["28", "53"]) {
  const allow = hn === "53" ? [1891, 1894, 1896, 1898] : [1891];
  if (HOUSE_VITALS.some((v) => v.houseNo === hn && !(v.bookSignature === "04105" && allow.includes(v.year))))
    p86Errors.push(`NOVA hiša ${hn} (P86) že obstaja v prejšnjem letu — pini neskladni`);
}
// vitals skupaj 392 (po P104: 374 + 18; krstna 1909)
if (HOUSE_VITALS.length !== 392)
  p86Errors.push(`HOUSE_VITALS ≠ 392 (${HOUSE_VITALS.length})`);
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
  const allow = hn === "12" ? [1892, 1894, 1895, 1897, 1899, 1901, 1903, 1905, 1907, 1909] : [1892, 1894, 1899]; // P94: + 1899 bloka (h12 mati MENJAVA [~]; h75 3. VPIS ISTA ZVEZA); P96: + 1901 bloka h12 (r1 + r36 — PRVA ponovitev po 1893); P98: + 1903 blok h12 (8. VPIS); P100: + 1905 bloka h12 (NARE PRELOM — r4 Neža + r15 Ana, 9./10. VPIS); P102: + 1907 blok h12 (11. VPIS — Dragoš POVRAT); P104: + 1909 blok h12 (12. VPIS — ISTA ZVEZA Drgoš × Cvitkovič)
  if (HOUSE_VITALS.some((v) => v.houseNo === hn && !(v.bookSignature === "04105" && allow.includes(v.year))))
    p87Errors.push(`NOVA hiša ${hn} (P87) že obstaja v prejšnjem letu — pini neskladni`);
}
// vitals skupaj 392 (po P104: 374 + 18; krstna 1909)
if (HOUSE_VITALS.length !== 392)
  p87Errors.push(`HOUSE_VITALS ≠ 392 (${HOUSE_VITALS.length})`);
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
// h23: P89 kontinuiteta dovoli tudi blok 1894 (ISTI oče Brinec + ISTA botra pa);
// h46/h91: P90 kontinuiteta dovoli tudi bloke 1895 (h46 2. vpis ISTA zveza;
// h91 mati ISTA Kure, oče menjan Novak → Muc); h46: P91 dovoli blok 1896 (3. vpis)
// h23: P92 dovoli blok 1897 (Brinec × Petrlie? — 2. Brinec hiša forenzika); h46: P92 dovoli blok 1897 (4. vpis Brodarič)
for (const hn of ["23", "46", "70", "91"]) {
  // h46: P90/P91/P92/P94 kontinuiteta dovoli bloke 1895/1896/1897/1899 (5. VPIS ISTA ZVEZA; 4. varianta matere)
  const allow = hn === "23" ? [1893, 1894, 1897, 1900, 1903, 1905, 1908] : hn === "46" ? [1893, 1895, 1896, 1897, 1899, 1908] : hn === "91" ? [1893, 1895, 1902, 1904, 1908] : [1893]; // P94: + 1899 blok h46; P95: + 1900 blok h23 (4. PIN ISTA ZVEZA — Debič? REŠENO); P97: + 1902 blok h91 (3. VPIS — boter Željko? signal 17); P98: + 1903 blok h23 (5. VPIS — Jaroslav?); P99: + 1904 blok h91 (4. VPIS — MUC KONTINUITETA, oče Janez Muc bajtar); P100: + 1905 blok h23 (6. VPIS — Matija Brinec); P103: + 1908 bloki h23 (7. VPIS — ISTA Dehlič) + h46 (6. VPIS — ISTA OČE Brodarič) + h91 (5. VPIS — Muc × Kure)
  if (HOUSE_VITALS.some((v) => v.houseNo === hn && !(v.bookSignature === "04105" && allow.includes(v.year))))
    p88Errors.push(`NOVA hiša ${hn} (P88) že obstaja v prejšnjem letu — pini neskladni`);
}
// h60: NOVA krstna — ponovitev čez knjige (poroka 04455 1886 GRIBLJE 60)
const p88H60b = HOUSE_VITALS.find((v) => v.houseNo === "60" && v.bookSignature === "04455" && v.year === 1886);
if (!p88H60b || !p88H60b.whatSi.includes("GRIBLJE 60"))
  p88Errors.push("kontinuiteta hiša 60 (1886, 04455, pin GRIBLJE 60) manjka");
// vitals skupaj 392 (po P104: 374 + 18; krstna 1909)
if (HOUSE_VITALS.length !== 392)
  p88Errors.push(`HOUSE_VITALS ≠ 392 (${HOUSE_VITALS.length})`);
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
// vitals skupaj 392 (po P104: 374 + 18; krstna 1909)
if (HOUSE_VITALS.length !== 392)
  p89Errors.push(`HOUSE_VITALS ≠ 392 (${HOUSE_VITALS.length})`);
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
// NOVE hiše 1895 (20, 37, 87) — ne obstajajo v nobenem prejšnjem letu/knjigi
// h20/h37: P92 dovoli bloka 1897 (h20 2. pin Pendirec? × Klepec?; h37 2. pin Pendirec? × Zugelj?)
for (const hn of ["20", "37", "87"]) {
  const allow = hn === "20" ? [1895, 1897, 1900, 1903, 1906] : hn === "37" ? [1895, 1897] : hn === "87" ? [1895, 1902, 1904] : [1895]; // P95: + 1900 blok h20 (3. PIN Pendirec × Klepec); P97: + 1902 blok h87 (2. VPIS — oče Pegdirec?/Perdinec? KURRENT); P98: + 1903 blok h20 (4. VPIS — EMŠO sidro); P99: + 1904 blok h87 (3. VPIS — NI menjava, Marko Podrinec bajtar); P101: + 1906 blok h20 (5. VPIS — ISTA DRUŽINA Perdinec/Pozdirec × Klepec)
  if (HOUSE_VITALS.some((v) => v.houseNo === hn && !(v.bookSignature === "04105" && allow.includes(v.year))))
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
// vitals skupaj 392 (po P104: 374 + 18; krstna 1909)
if (HOUSE_VITALS.length !== 392)
  p90Errors.push(`HOUSE_VITALS ≠ 392 (${HOUSE_VITALS.length})`);
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
// h9/h14/h45: P95 kontinuiteta dovoli bloke 1900 (menjava h9; 2. VPIS h14 — REŠUJE P91; 3. PIN h45 — 04455)
for (const hn of ["9", "14", "45"]) {
  const allow = hn === "45" ? [1896, 1897, 1900, 1904] : hn === "14" ? [1896, 1900, 1902, 1908] : [1896, 1900]; // P95: + 1900 bloki; P97: + 1902 blok h14 (3. VPIS — oče potrjen); P99: + 1904 blok h45 (4. VPIS — SPUDIČ signal, mati Barbara Spudič)
  if (HOUSE_VITALS.some((v) => v.houseNo === hn && !(v.bookSignature === "04105" && allow.includes(v.year))))
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
// vitals skupaj 392 (po P104: 374 + 18; krstna 1909)
if (HOUSE_VITALS.length !== 392)
  p91Errors.push(`HOUSE_VITALS ≠ 392 (${HOUSE_VITALS.length})`);
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
// h40: P93 kontinuiteta dovoli tudi blok 1898 (MENJAVA — Berkopne selitev h40→h48, Brodarič nazaj);
// h10: P95 kontinuiteta dovoli blok 1900 (MENJAVA Grabrijan × Pozdirec)
for (const hn of ["10", "40", "43"]) {
  const allow = hn === "40" ? [1897, 1898, 1899] : hn === "10" ? [1897, 1900, 1907, 1908, 1909] : [1897, 1904]; // P94: + 1899 blok h40 (TRETJA DRUŽINA Straus × Spudič); P95: + 1900 blok h10; P99: + 1904 blok h43 (2. VPIS — oče Jurij Perdinec, KURRENT nezakonski Pozdirec → Perdinec); P102: + 1907 bloka h10 ×2 (3. VPIS — BRINEC POVRAT, dvojčka; NARE PRELOM); P103: + 1908 blok h10 (4. VPIS — BRINEC ISTA, mati menjava Kure); P104: + 1909 blok h10 (6. VPIS — SELITEV h30→h10, Matija Brinec)
  if (HOUSE_VITALS.some((v) => v.houseNo === hn && !(v.bookSignature === "04105" && allow.includes(v.year))))
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
// vitals skupaj 392 (po P104: 374 + 18; krstna 1909)
if (HOUSE_VITALS.length !== 392)
  p92Errors.push(`HOUSE_VITALS ≠ 392 (${HOUSE_VITALS.length})`);
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
  // P100: + 1905 blok h48 (2. VPIS — VRZEL 7 LET, 1898→1905); P101: + 1906 blok h18 (2. VPIS — VRZEL 8 LET); P102: + 1907 bloka h18 (3. VPIS — MENJAVA Šimec → Brinec) + h48 (3. VPIS — MENJAVA Pezdirec → Kure); P104: + 1909 blok h48 (4. VPIS — EMŠO = KRSTNI datum)
  if (HOUSE_VITALS.some((v) => v.houseNo === hn && !(v.bookSignature === "04105" && (v.year === 1898 || v.year === 1905 || v.year === 1906 || v.year === 1907 || v.year === 1909))))
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
// vitals skupaj 392 (po P104: 374 + 18; krstna 1909)
if (HOUSE_VITALS.length !== 392)
  p93Errors.push(`HOUSE_VITALS ≠ 392 (${HOUSE_VITALS.length})`);
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
  const allow = hn === "22" ? [1899, 1902, 1904, 1905] : [1899, 1906, 1907, 1908]; // P97: + 1902 blok h22 (2. VPIS — MENJAVA ŽENE Klepec → Žurrič?); P99: + 1904 blok h22 (3. VPIS — POŽEK signal, boter Janez Požek); P100: + 1905 blok h22 (4. VPIS — Nikolaj Milek, botra Ana Požek); P101: + 1906 blok h49 (2. VPIS — Brodarič ↔ Željko izmena); P102: + 1907 blok h49 (3. VPIS — ISTI oče Brodarič; dojenček †); P103: + 1908 blok h49 (4. VPIS — ISTI oče Brodarič)
  if (HOUSE_VITALS.some((v) => v.houseNo === hn && !(v.bookSignature === "04105" && allow.includes(v.year))))
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
// vitals skupaj 392 (po P104: 374 + 18; krstna 1909)
if (HOUSE_VITALS.length !== 392)
  p94Errors.push(`HOUSE_VITALS ≠ 392 (${HOUSE_VITALS.length})`);
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
  if (HOUSE_VITALS.some((v) => v.houseNo === hn && !(v.bookSignature === "04105" && v.year === 1900)))
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
// vitals skupaj 392 (po P104: 374 + 18; krstna 1909)
if (HOUSE_VITALS.length !== 392)
  p95Errors.push(`HOUSE_VITALS ≠ 392 (${HOUSE_VITALS.length})`);
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
// NOVA hiša 19: brez predhodnikov v katerikoli knjigi (P101: + 1906 blok h19 — 2. VPIS NEZAKONSKI)
if (HOUSE_VITALS.some((h) => h.houseNo === "19" && (h.bookSignature !== "04105" || (h.year !== 1901 && h.year !== 1906))))
  p96Errors.push("NOVA hiša 19 že obstaja v prejšnjem letu — pini neskladni");
// vitals skupaj 392 (po P104: 374 + 18; krstna 1909)
if (HOUSE_VITALS.length !== 392)
  p96Errors.push(`HOUSE_VITALS ≠ 392 (${HOUSE_VITALS.length})`);
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
// vitals skupaj 392 (po P104: 374 + 18; krstna 1909)
if (HOUSE_VITALS.length !== 392)
  p97Errors.push(`HOUSE_VITALS ≠ 392 (${HOUSE_VITALS.length})`);
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
// vitals skupaj 392 (po P104: 374 + 18; krstna 1909)
if (HOUSE_VITALS.length !== 392)
  p98Errors.push(`HOUSE_VITALS ≠ 392 (${HOUSE_VITALS.length})`);
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
if (HOUSE_VITALS.length !== 392)
  p99Errors.push(`HOUSE_VITALS ≠ 392 (${HOUSE_VITALS.length})`);
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
// vitals skupaj 392 (po P104: 374 + 18; krstna 1909)
if (HOUSE_VITALS.length !== 392)
  p100Errors.push(`HOUSE_VITALS ≠ 392 (${HOUSE_VITALS.length})`);
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
// vitals skupaj 392 (po P104: 374 + 18; krstna 1909)
if (HOUSE_VITALS.length !== 392)
  p101Errors.push(`HOUSE_VITALS ≠ 392 (${HOUSE_VITALS.length})`);
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
// vitals skupaj 392 (P102: 341 + 15; P103: + 18; krstna 1908; r84 neberljiva brez bloka)
if (HOUSE_VITALS.length !== 392)
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
// vitals skupaj 392 (P103: 356 + 18; krstna 1908; r84 neberljiva brez bloka)
if (HOUSE_VITALS.length !== 392)
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
// vitals skupaj 392 (P104: 374 + 18; krstna 1909)
if (HOUSE_VITALS.length !== 392)
  p104Errors.push(`HOUSE_VITALS ≠ 392 (${HOUSE_VITALS.length})`);
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
  "P104: ŽUPNIJA PODZEMELJ — KRSTNA KNJIGA 04105, POLNO LETO 1909 (issue #18; SAMPLE-TRANSCRIPTION-1909; MERI, NE odloča; v7 join nespremenjen): širitev vzorca P79 (1886) → … → P101 (1906) → P102 (1907) → P103 (1908) na leto 1909 — okvir: glava »1909 / Januarij« INLINE na str. 180 = skeni 199/200 (dup par; 1909 r1 = Dobraviče 26 Anton 7./7. Januar, EMŠO 0701909500220 — P103 lead POTRJEN; P103 ocava »sken 200 = str. 181« POPRAVLJENA — s200 = str. 180, r89 1908 pod belim trakom berljiv SAMO na s200!) – row 81 na str. 187 (sken 211; glava »1910« INLINE; 1910 r1 = Cerkvišče 2 Anton 3./4. Januar — P105 lead; prva Griblje vrstica 1910 = r3 Griblje 5 Jožefa, Matija Štrucelj × Marija Meh) == tiskane strani 180–187 (81 vrstic — NAJKRAJŠE leto v vzorcu; 1908 = 90); NOVELA P104: PET dup parov skenov — 199/200 = str. 180 + 202/203 = str. 182 + 204/205 = str. 183 + 207/208 = str. 185 + 209/210 = str. 186 (največ v enem letu doslej); stran == sken − 19 (199/200) / − 20 (201–202) / − 21 (203–205) / − 22 (206–207) / − 23 (208–210) / − 24 (211); VSI vpisi z Griblji: 18 vpisov / 17 hiš (h34 ×2 = DVOJČKI Matija+Nikolaj, oba kot dojenčka umrla — NARE PRELOM, 1. intra-letna ponovitev po 1908 NARE 18/18); 0 NOVIH hiš (5. leto z 0: 0/1/0/0/0 — vse 17 hiš že zasidrane); PT 14/3 (42+48+54 v luknji 41–60 — ponovitve; luknja ostaja samo h51); kumulativ 400 vpisov / 85 hiš čez tri knjige in 24 let (1886–1909; 392 vitals); SIDRA: r6 h77 3. VPIS — POŽEK POVRAT po 19 LETIH (1890 Jurij Požek bajtar → 1902 MENJAVA Cindrič cevljar → 1909 ISTI oče z NOVO ženo Veselič?; najdaljša hišna vrzel 1909; cf. h21 Požek karusela); r9 h10 6. VPIS — SELITEV h30→h10 (Matija Brinec × Marija Grabrijan = ISTA ZVEZA kot h30 1906!; h10 = trije Brincovi možje zapored 1907/08/09; EMŠO 3001909500735; botra Janez+Ana Brinec); r17 h42 4. VPIS — ISTA ZVEZA 1905 VRNE (Jurij Pezdirec × Katarina Jurajevič — ISTA mati kot 1905/06; genetsko prek prior-bloka; poročena 20.11.1938; mož † 1943; † 26.4.1982 Črnomelj); r20+r21 h34 DVOJČKI (18./18. + 18./19. 4.; ISTA botra Nikolaj Segina + Katarina Šuštar na OBOJIH; Matija † 18/4.09 ISTI DAN!; Nikolaj † 3/4.10.09 — oba dojenčka umrla; 2. dvojčki-par z obema smrtma po 1907 h10); r28 h72 6. VPIS — STRAUŠ POVRAČNICA po 14 LETIH (1888–95 Matija Strauš v h72 → 1904 h42 interlude → 1909 DOMA; h42↔h72 ŠTRAUS↔PEZDIREC KARUSELJA — obe familiji 1909 v svoji hiši!; mati menjava #3 Šimec; EMŠO 020609500254; botra = ISTI PAR kot h42 1904 [Jožef Štrucelj + Barbara Jakobič]; babica Katarina Štraus; dan celici poškodovani [~]); r30 h33 3. VPIS — »VPIS PRENESEN V MRLIŠKI REGISTER« (MENJAVA #3: Brinec 1889 → Dehlič 1898 → Papič? 1909; VRZEL 11 LET; EMŠO 0306095050335; botra ISTI PRIIMEK [Mihael+Katarina Papič?]; podpis »Gregor Cerar coop.« — edini coop. 1909); r32 h63 9. VPIS — MATI »Katarina Križan, samka ½ zemljaka« (MOŽEN NEZAKONSKI VPIS; VRZEL 6 LET; oče Janez Papič? [~ Tepič]; EMŠO brez); r35 h54 6. VPIS — ŠIMEC NOVA DRUŽINA (Janez Šimec × Marija Kure?; boter Ivan Požek = POŽEK signal; VRZEL 5 LET; † 18.4.1978 Črnomelj); r37 h1 7. VPIS ISTA ZVEZA (Jurij Željko × Barbara Kure = 1900+1905; † 5.5.1925 pri 15 letih!; boter Jožef Željko); r40 h6 4. VPIS — HIŠNA CELICA POKRITA, HIŠA GENETSKO (celica prazna/pokrita z modrim pripisom na OBOJIH dup; starši = ISTA ZVEZA kot h6 1904/05 [Jurij × Katarina Jakobič] + botrinja Marija Klepec ISTA → genetska rešitev h6; 1907 Kapucina? menjava → 1909 POV RAT; EMŠO 120809505944 [~]); r44 h24 14. VPIS ZAPORED — ŠE VEDNO najbolj vpisovana hiša registra (Brincova; oče Janez Brinec; botra Matija+Marija Brinec; EMŠO 26079095?5231 [~]; PONESREČI UMRLA 23.10.1965 pri božjani s šolskim kolektivom [MK Ljubljana 1.1965] + drugi pripis 30.10.1988 Celovec? — DVOJNI smrtni pripisi!); r57 h30 12. VPIS — 7. DRUŽINA (France Martinovič? kovač × Katarina Šimec; forenzika 30 na OBOJIH dup [ni 36/50]; botra Janez+Marjeta Žugelj); r58 h12 12. VPIS — NOVA ZVEZA Drgoš × Cvitkovič (VÖTTER DVOJNO: babica Marjeta + botrinja Katarina!; boter Matija Štrucelj = 1910 r3 oče!); r60 h35 6. VPIS — MATI BREZ PRIIMKA (samo »Ana« — edini tak vpis v vzorcu!; oče Jožef Pezdirec bajtar = MENJAVA po Hrižan 1903/06); r61 h32 10. VPIS — ISTA ZVEZA (Matija Meh × Marjeta Pezdirec = 1889–95 variante ISTEGA para; VRZEL 6 LET; poročena 1.2.1936; podpis-kolono prevzame MATICARKA Paulin Bitenc — NOVELA!); r64 h48 4. VPIS — EMŠO 1910909505186 = KRSTNI datum (rojstvo 18.10 — maticar uporabil krsto; edinski primer!; poročin 22.1.1933 KLEPEC — MOŽ UMRL); r72 h66 4. VPIS (Jakob Bohte × Katarina Križan; forenzika 66 — DVE ŠESTERKI, prva branja 22/72 NAPAČNA; boter Nikolaj Brodarič = ISTI kot r64 CROSS-ROW; botrinja Marija Straus; EMŠO 051090505628 [~]; † 30.8.1994 Griblje); DUHOVNIKI: Gregor Cerar 10 (Januar–Junij; vključno r30 »coop.«) + Jos. Rauq 6 (Avgust–Oktober: r40–r64) + 2 podpisa maticarke Paulin Bitenc v koloni Podpis (r61/r72 — NOVELA: od r61 dalje maticarka podpisuje ob smrtnih pripisih 1950s–60s); BABICA NOVELA: na Gribljih 18/18 imenovanih: MARIJA MEH 12/18 DOMINANTA 1909 + Barbara Adlešič 1 (r9) + Katarina Štraus 1 (r28) + Ana Mavrenič 1 (r30) + Marija Uri? 1 (r40) + Ana Novak 1 (r57) + Marjeta Vötter 1 (r58 — DVOJNO z botrinjo); Muc 0× (po 6× 1908!); EMŠO kampanja: 7 sidr na Gribljih (6+1 anomalija r64) — VSI SKLADNI z rojstvi (r64 = krsta!); ANOMALIJE: r5 »Decembar 16./16.« Grm 36 POD glavo 1909 (kronološka kršitev!) + r91 = aprilski vpis 1908 nad glavo; h42↔h72 karusela; POŽEK 19 let; selitev h30→h10; dvojčki z obema smrtma; mati samka (r32); mati brez priimka (r60); EMŠO=krsta (r64); maticarka v podpis-koloni (r61+); PONESREČI UMRLA (r44 1965!); 2 RAZVELJAVITVI zakona (r73 Krško 52/195-3 + r76); TRGOGRAD pripis (r19 Gradac — št. 13-546/65!); »Vzet v matični register 13.02.200X« (r65 Vranovče — matičarka); Podzemelj 6 vpis (r63 — redko!); mejni vpis r81 (31.12.1909/1.1.1910); kraj »Gornej?« ×4 (r12/r22/r47/r76 z Muc/Pezdirec familijami); CROSS-ROW ×4 (r64+r72 boter Nikolaj Brodarič; r35 boter Ivan Požek ↔ r6 oče; r57 mati Šimec ↔ r35 oče; r32+r72 mati Križan); EXCLUDED: 22 (r1 Dobravice 26 lead, r2–r5, r7/r8, r10/r11, r12, r13–r16, r18/r19 TRGOGRAD, r22 Gornej?, r23–r27, r29, r31 †13/6.09 dojenček, r33/r34, r36–r41, r42/r43, r45–r53 [r48 EMŠO 5104?? invalid], r54–r56, r59, r62 Kapljišče?, r63 Podzemelj, r65–r71 [r65 vzet v matični register], r73 RAZVELJAVITEV, r74–r80, r81 mejni); skripta scripts/p104_parish_baptism_1909.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1909",
  "P104: PARISH OF PODZEMELJ — BAPTISM REGISTER 04105, THE FULL YEAR 1909 (issue #18; SAMPLE-TRANSCRIPTION-1909; MEASURES, does not decide; the v7 join unchanged): extending the sample P79 (1886) → … → P103 (1908) to 1909 — the frame: the heading »1909 / Januarij« INLINE on p. 180 = scans 199/200 (a dup pair; the 1909 r1 = Dobraviče 26 Anton Jan 7/7, personal ID 0701909500220 — the P103 lead CONFIRMED; the P103 note »scan 200 = p. 181« CORRECTED — s200 = p. 180, the 1908 r89 under the white strip legible ONLY on s200!) – row 81 on p. 187 (scan 211; the heading »1910« INLINE; the 1910 r1 = Cerkvišče 2 Anton Jan 3/4 — the P105 lead; the first Griblje row of 1910 = r3 Griblje 5 Jožefa, Matija Štrucelj × Marija Meh) == printed pages 180–187 (81 rows — the SHORTEST year in the sample; 1908 = 90); THE P104 NOVEL: FIVE duplicated scan pairs — 199/200 = p. 180 + 202/203 = p. 182 + 204/205 = p. 183 + 207/208 = p. 185 + 209/210 = p. 186 (the most in one year so far); page == scan − 19 (199/200) / − 20 (201–202) / − 21 (203–205) / − 22 (206–207) / − 23 (208–210) / − 24 (211); ALL Griblje entries: 18 entries / 17 houses (h34 ×2 = the TWINS Matija+Nikolaj, both dead as infants — the NARE BREAK, the 1st intra-year repeat after the 1908 NARE 18/18); 0 NEW houses (the 5th year with 0: 0/1/0/0/0 — all 17 houses already anchored); the PT 14/3 (42+48+54 in the gap 41–60 — repeats; only h51 remains); the cumulative 400 entries / 85 houses across three books and 24 years (1886–1909; 392 vitals); ANCHORS: r6 h77 the 3rd ENTRY — the POŽEK RETURN after 19 YEARS (1890 Jurij Požek the cottager → the 1902 CHANGE Cindrič the ropemaker → 1909 the SAME father with a NEW wife Veselič?; the longest house gap of 1909; cf. the h21 Požek carousel); r9 h10 the 6th ENTRY — the MOVE h30→h10 (Matija Brinec × Marija Grabrijan = the SAME COUPLE as h30 1906!; h10 = three Brinec husbands in a row 1907/08/09; personal ID 3001909500735; the godparents Janez+Ana Brinec); r17 h42 the 4th ENTRY — the SAME COUPLE OF 1905 RETURNS (Jurij Pezdirec × Katarina Jurajevič — the SAME mother as 1905/06; genetically via the prior block; married Nov 20, 1938; the husband † 1943; † Apr 26, 1982 Črnomelj); r20+r21 h34 the TWINS (Apr 18/18 + 18/19; the SAME godparents Nikolaj Segina + Katarina Šuštar on BOTH; Matija died Apr 18, 1909 THE SAME DAY!; Nikolaj died Oct 3/4, 1909 — both infants dead; the 2nd twins-pair with both deaths after the 1907 h10); r28 h72 the 6th ENTRY — the STRAUŠ HOMECOMING after 14 YEARS (1888–95 Matija Strauš in h72 → the 1904 h42 interlude → 1909 HOME; the h42↔h72 ŠTRAUS↔PEZDIREC CAROUSEL — both families 1909 in their own house!; the mother change #3 Šimec; personal ID 020609500254; the godparents = the SAME COUPLE as h42 1904 [Jožef Štrucelj + Barbara Jakobič]; the midwife Katarina Štraus; the day cells damaged [~]); r30 h33 the 3rd ENTRY — »THE ENTRY TRANSFERRED TO THE DEATH REGISTER« (a FAMILY CHANGE #3: Brinec 1889 → Dehlič 1898 → Papič? 1909; an 11-YEAR GAP; personal ID 0306095050335; the godparents the SAME SURNAME [Mihael+Katarina Papič?]; the signature »Gregor Cerar coop.« — the only coop. of 1909); r32 h63 the 9th ENTRY — the MOTHER »Katarina Križan, samka ½ zemljaka« (a POSSIBLE ILLEGITIMATE ENTRY; a 6-YEAR GAP; the father Janez Papič? [~ Tepič]); r35 h54 the 6th ENTRY — the ŠIMEC NEW FAMILY (Janez Šimec × Marija Kure?; the godfather Ivan Požek = the POŽEK signal; a 5-YEAR GAP; † Apr 18, 1978 Črnomelj); r37 h1 the 7th ENTRY the SAME COUPLE (Jurij Željko × Barbara Kure = 1900+1905; † May 5, 1925 aged 15!; the godfather Jožef Željko); r40 h6 the 4th ENTRY — the HOUSE CELL COVERED, THE HOUSE GENETICALLY (the cell empty/covered by a blue note on BOTH dups; the parents = the SAME COUPLE as h6 1904/05 [Jurij × Katarina Jakobič] + the godmother Marija Klepec the SAME → the genetic solution h6; the 1907 Kapucina? change → the 1909 RETURN; personal ID 120809505944 [~]); r44 h24 the 14th CONSECUTIVE ENTRY — STILL the most-entered house of the register (the Brinec house; the father Janez Brinec; the godparents Matija+Marija Brinec; personal ID 26079095?5231 [~]; SHE DIED IN AN ACCIDENT Oct 23, 1965 during a pilgrimage with a school group [MK Ljubljana 1.1965] + a second note Oct 30, 1988 Celovec? — DOUBLE death notes!); r57 h30 the 12th ENTRY — the 7th FAMILY (France Martinovič? the smith × Katarina Šimec; the forensics 30 on BOTH dups [not 36/50]; the godparents Janez+Marjeta Žugelj); r58 h12 the 12th ENTRY — the NEW COUPLE Drgoš × Cvitkovič (the VÖTTER DOUBLE: the midwife Marjeta + the godmother Katarina!; the godfather Matija Štrucelj = the 1910 r3 father!); r60 h35 the 6th ENTRY — THE MOTHER WITHOUT A SURNAME (only »Ana« — the only such entry in the sample!; the father Jožef Pezdirec the cottager = a CHANGE after Hrižan 1903/06); r61 h32 the 10th ENTRY — the SAME COUPLE (Matija Meh × Marjeta Pezdirec = the 1889–95 variants of the SAME couple; a 6-YEAR GAP; married Feb 1, 1936; the signature column taken over by THE REGISTRAR Paulin Bitenc — a NOVELTY!); r64 h48 the 4th ENTRY — the personal ID 1910909505186 = THE BAPTISM DATE (the birth Oct 18 — the registrar used the baptism; the only such case!; married Jan 22, 1933 KLEPEC — the HUSBAND DIED); r72 h66 the 4th ENTRY (Jakob Bohte × Katarina Križan; the forensics 66 — TWO SIXES, the first readings 22/72 WRONG; the godfather Nikolaj Brodarič = the SAME as r64 CROSS-ROW; the godmother Marija Straus; personal ID 051090505628 [~]; † Aug 30, 1994 Griblje); PRIESTS: Gregor Cerar 10 (January–June; incl. the r30 »coop.«) + Jos. Rauq 6 (August–October: r40–r64) + 2 signatures of the registrar Paulin Bitenc in the signature column (r61/r72 — a NOVELTY: from r61 on the registrar signs at the death annotations of the 1950s–60s); MIDWIFE NOVEL: in Griblje 18/18 named: MARIJA MEH 12/18 THE DOMINANT OF 1909 + Barbara Adlešič 1 (r9) + Katarina Štraus 1 (r28) + Ana Mavrenič 1 (r30) + Marija Uri? 1 (r40) + Ana Novak 1 (r57) + Marjeta Vötter 1 (r58 — DOUBLE with the godmother); Muc 0× (after the 6× of 1908!); the personal-ID campaign: 7 anchors in Griblje (6+1 the r64 anomaly) — ALL CONSISTENT with the births (r64 = the baptism!); ANOMALIES: the r5 »Decembar 16./16.« Grm 36 UNDER the 1909 heading (a chronological violation!) + the r91 = an April 1908 entry above the heading; the h42↔h72 carousel; the POŽEK 19 years; the move h30→h10; the twins with both deaths; the samka mother (r32); the mother without a surname (r60); the ID=baptism (r64); the registrar in the signature column (r61+); SHE DIED IN AN ACCIDENT (r44 1965!); 2 marriage ANNULMENTS (r73 Krško 52/195-3 + r76); the TRGOGRAD note (r19 Gradac — no. 13-546/65!); »Taken into the civil register Feb 13, 200X« (r65 Vranovče — the registrar); a Podzemelj 6 entry (r63 — rare!); the boundary entry r81 (Dec 31, 1909/Jan 1, 1910); the village »Gornej?« ×4 (r12/r22/r47/r76 with the Muc/Pezdirec families); CROSS-ROW ×4 (r64+r72 the godfather Nikolaj Brodarič; the r35 godfather Ivan Požek ↔ the r6 father; the r57 mother Šimec ↔ the r35 father; the r32+r72 mother Križan); EXCLUDED: 22 (r1 Dobravice 26 the lead, r2–r5, r7/r8, r10/r11, r12, r13–r16, r18/r19 TRGOGRAD, r22 Gornej?, r23–r27, r29, r31 the infant † Jun 13, 1909, r33/r34, r36–r41, r42/r43, r45–r53 [r48 the ID 5104?? invalid], r54–r56, r59, r62 Kapljišče?, r63 Podzemelj, r65–r71 [r65 taken into the civil register], r73 the ANNULMENT, r74–r80, r81 the boundary); the script scripts/p104_parish_baptism_1909.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1909",
  p104Errors.length === 0,
  p104Errors.length === 0
    ? `18 vpisov / 17 hiš (h34 ×2 dvojčka † oba) — NARE PRELOM · okvir 1909 skeni 199/200 (glava INLINE, s200 = str. 180 — P103 ocava POPRAVLJENA!) – 211 row 81 (glava 1910 INLINE = P105 lead; 81 vrstic — najkrajše leto) · NOVELA: PET dup parov (199/200 + 202/203 + 204/205 + 207/208 + 209/210) · stran == sken − 19…− 24 · 0 NOVIH hiš (0/1/0/0/0 — 5. leto) · PT 14/3 · h77 POŽEK POVRAT po 19 LETIH · h10 SELITEV h30→h10 (trije Brinci zapored) · h42 ISTA ZVEZA 1905 VRNE · h72 STRAUŠ POVRAČNICA po 14 LETIH (h42↔h72 KARUSELJA!) · h34 DVOJČKI (ISTA botra; † isti dan + † oktober) · h33 VPIS PRENESEN v mrliški register + MENJAVA #3 (VRZEL 11) · h63 mati SAMKA (možen nezakonski) · h54 ŠIMEC × KURE + boter Ivan Požek · h1 ŽELJKO × KURE 7. VPIS · h6 GENETSKO (celica pokrita) · h24 14. VPIS + PONESREČI UMRLA 1965 · h30 7. DRUŽINA Martinovič? · h12 VÖTTER DVOJNO · h35 MATI BREZ PRIIMKA · h32 maticarka BITENC v koloni Podpis · h48 EMŠO = KRSTA · h66 DVE ŠESTERKI (Bohte × Križan) · Cerar 10 + Rauq 6 + Bitenc 2 · babica MEH 12/18 DOMINANTA + Vötter 1 (18/18) · EMŠO 7 sidr (r64 = krsta!) · EXCLUDED 22 · vitals 392 · kumulativ 400/85 24 let`
    : p104Errors.join("; "),
);
}
