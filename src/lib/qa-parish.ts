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
const p79Hv = HOUSE_VITALS.filter(
  (h) =>
    h.bookSignature === "04105" &&
    (h.year === 1886 || h.year === 1897 || (h.year === 1887 && ["61", "78"].includes(h.houseNo))),
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
const p80All = HOUSE_VITALS.filter(
  (h) =>
    h.bookSignature === "04894" ||
    h.bookSignature === "04455" ||
    (h.bookSignature === "04105" &&
      (h.year === 1886 || h.year === 1897 || (h.year === 1887 && ["61", "78"].includes(h.houseNo)))),
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
  "P82: ŽUPNIJA PODZEMELJ — KRSTNA KNJIGA 04105, POLNO LETO 1887 (issue #18; SAMPLE-TRANSCRIPTION-1887; MERI, NE odloča; v7 join nespremenjen): širitev vzorca P79 (1886) na naslednje leto — okvir: skeni 16–27 == tiskane strani 15–26 (stran == sken − 1; glava »Leto 18_87« na str. 15; leto 1888 se začne NA STRANI 26 po row 106 z velikimi ciframi »1 8 8 8« — zadnji vpis 1887 row 106 (29./30. 12., Krasinec 7), prvi 1888 row 107 (9./11. 1., Gradac 26)) — VSI vpisi z Griblji: 20 vpisov / 19 različnih hiš (2, 15, 17, 21, 24, 26 [~], 27, 31×2, 34, 35, 47, 52→04→15 [~], 55, 61, 62, 63, 65, 66, 78 [~]) — NAD merili issue #18; vsak vpis: signatura + leto + stran/skan + hišna št. + otrok + starši + botre/babica (Kurrent z [~]); NOVI PT LUKNJI 47 in 55 (52 izvirno row 78 — trojna korekcija 52 → 04 → 15 [~]: izvirno v luknji, končna v naboru; obe klasifikaciji dokumentirani) — luknja 41–60 v krstnih vpisih: 54/56/57 (P79) + 44/59/60 (P80) + 47/52/55 (P82) = 9 dokazanih števil; P79 SIDRO hiša 61 re-verificirano (row 28, sken 20: oče zdaj »Miko Požek« [~] — prej »Miha P.—«/»Miko Jože H.?«, oba branji ohranjena; mati Bara roj. Filath [~]); NEZAKONSKI vpisi 2 (row 78 hiša 52: mati Marija Muc [~]; row 80 hiša 55: mati Ana Smič [~] — očeta stolpca PRAZNA); ANOMALIJA ZAPISA row 93 (hiša 35: v očetovem stolpcu »Marija Hrižan ½ zemljašt.«, v materinem »Ana Požek« — dve interpretaciji [~]); MULTI-VPIS: hiša 31 ×2 (Ana 1./2. 8. + Janez 6. 9.) — hiša 31 tudi v mrliški 1886 (Katarina Marh — P80) = križna povezava dveh knjig; TROI DUHOVNIKI 1887: kapljan Andrej Griebel [~] (14), župnik Franjo Dovgan (1), »Jos. Povmij« [~] (4 — nov podpis 1887); BABICA Marija Brinec 9× (gost porekla Brinec: mati 2×, očetje 1×, botre 3×); priimki čez leta: Šimec (1886: 36/39/56/88 → 1887: 34 — NOVA hiša), Straus (mati Margaretha @31 + botra Katarina @47), Filak/Filath (mati Bara @61 + babica @52), Stubler (mati @78), Požek (očeta @61/@21 + botra @27); live verifikacija: knjiga HTTP 200 (inventar 326), citirani skeni 8/8 JPEG 200; skripta scripts/p82_parish_baptism_1887.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1887",
  "P82: PARISH OF PODZEMELJ — BAPTISM REGISTER 04105, THE FULL YEAR 1887 (issue #18; SAMPLE-TRANSCRIPTION-1887; MEASURES, does not decide; the v7 join unchanged): extending the P79 sample (1886) to the next year — the frame: scans 16–27 == printed pages 15–26 (page == scan − 1; the header »Leto 18_87« on p. 15; the year 1888 begins ON PAGE 26 after row 106 with large numerals »1 8 8 8« — the last 1887 entry row 106 (Dec 29/30, Krasinec 7), the first 1888 row 107 (Jan 9/11, Gradac 26)) — ALL Griblje entries: 20 entries / 19 distinct houses (2, 15, 17, 21, 24, 26 [~], 27, 31×2, 34, 35, 47, 52→04→15 [~], 55, 61, 62, 63, 65, 66, 78 [~]) — ABOVE the issue #18 criteria; every entry: signature + year + page/scan + house number + child + parents + godparents/midwife (Kurrent with [~]); NEW PT GAPS 47 and 55 (52 originally row 78 — a triple correction 52 → 04 → 15 [~]: the original in the gap, the final in the set; both classifications documented) — the 41–60 gap in baptism entries: 54/56/57 (P79) + 44/59/60 (P80) + 47/52/55 (P82) = 9 proven numbers; the P79 ANCHOR house 61 re-verified (row 28, scan 20: the father now »Miko Požek« [~] — earlier »Miha P.—«/»Miko Jože H.?«, both readings preserved; mother Bara née Filath [~]); ILLEGITIMATE entries 2 (row 78 house 52: mother Marija Muc [~]; row 80 house 55: mother Ana Smič [~] — the fathers' columns EMPTY); RECORDING ANOMALY row 93 (house 35: the father's column holds »Marija Hrižan ½ zemljašt.«, the mother's »Ana Požek« — two interpretations [~]); MULTI-ENTRY: house 31 ×2 (Ana Aug 1/2 + Janez Sep 6) — house 31 also in the death register 1886 (Katarina Marh — P80) = a two-book cross-link; THREE PRIESTS 1887: curate Andrej Griebel [~] (14), parish priest Franjo Dovgan (1), »Jos. Povmij« [~] (4 — a new 1887 signature); MIDWIFE Marija Brinec 9× (the Brinec origin hub: mother 2×, fathers 1×, godmothers 3×); surnames across years: Šimec (1886: 36/39/56/88 → 1887: 34 — a NEW house), Straus (mother Margaretha @31 + godmother Katarina @47), Filak/Filath (mother Bara @61 + midwife @52), Stubler (mother @78), Požek (fathers @61/@21 + godfather @27); live verification: the book HTTP 200 (inventory 326), cited scans 8/8 JPEG 200; the script scripts/p82_parish_baptism_1887.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1887",
  p82Errors.length === 0,
  p82Errors.length === 0
    ? `20 vpisov / 19 hiš · okvir 1887 skeni 16–27 (stran == sken−1; 1888 prelom na str. 26 row 107) · PT 16/3 (47, 52, 55 v luknji — 9 dokazanih skupaj) · sidro 61 row 28 (Miko Požek [~]) · nezakonski 2 · anomalija row 93 · multi 31×2 · trije duhovniki · babica Brinec 9×`
    : p82Errors.join("; "),
);
}
