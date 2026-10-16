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
// h90: P87 kontinuiteta dovoli tudi blok 1892 (učitelj ISTA družina)
for (const hn of ["7", "30", "38", "41", "77", "90"]) {
  const allow = hn === "30" ? [1890, 1891, 1893] : hn === "90" ? [1890, 1892] : hn === "41" ? [1890, 1893] : [1890];
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
// NOVE hiše 1891 (28, 53) — ne obstajajo v nobenem prejšnjem letu/knjigi
for (const hn of ["28", "53"]) {
  if (HOUSE_VITALS.some((v) => v.houseNo === hn && !(v.bookSignature === "04105" && v.year === 1891)))
    p86Errors.push(`NOVA hiša ${hn} (P86) že obstaja v prejšnjem letu — pini neskladni`);
}
// vitals skupaj 150 (P87: 133 + 17)
if (HOUSE_VITALS.length !== 150)
  p86Errors.push(`HOUSE_VITALS ≠ 150 (${HOUSE_VITALS.length})`);
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
// NOVE hiše 1892 (12, 73, 75) — ne obstajajo v nobenem prejšnjem letu/knjigi
for (const hn of ["12", "73", "75"]) {
  if (HOUSE_VITALS.some((v) => v.houseNo === hn && !(v.bookSignature === "04105" && v.year === 1892)))
    p87Errors.push(`NOVA hiša ${hn} (P87) že obstaja v prejšnjem letu — pini neskladni`);
}
// vitals skupaj 150 (P87: 133 + 17)
if (HOUSE_VITALS.length !== 150)
  p87Errors.push(`HOUSE_VITALS ≠ 150 (${HOUSE_VITALS.length})`);
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
// NOVE hiše 1893 (23, 46, 60, 70, 91) — ne obstajajo v nobenem prejšnjem letu/knjigi
for (const hn of ["23", "46", "70", "91"]) {
  if (HOUSE_VITALS.some((v) => v.houseNo === hn && !(v.bookSignature === "04105" && v.year === 1893)))
    p88Errors.push(`NOVA hiša ${hn} (P88) že obstaja v prejšnjem letu — pini neskladni`);
}
// h60: NOVA krstna — ponovitev čez knjige (poroka 04455 1886 GRIBLJE 60)
const p88H60b = HOUSE_VITALS.find((v) => v.houseNo === "60" && v.bookSignature === "04455" && v.year === 1886);
if (!p88H60b || !p88H60b.whatSi.includes("GRIBLJE 60"))
  p88Errors.push("kontinuiteta hiša 60 (1886, 04455, pin GRIBLJE 60) manjka");
// vitals skupaj 150 (P87: 133 + 17)
if (HOUSE_VITALS.length !== 150)
  p88Errors.push(`HOUSE_VITALS ≠ 150 (${HOUSE_VITALS.length})`);
push(
  "qa-p88-parish-baptism-1893",
  "P88: ŽUPNIJA PODZEMELJ — KRSTNA KNJIGA 04105, POLNO LETO 1893 (issue #18; SAMPLE-TRANSCRIPTION-1893; MERI, NE odloča; v7 join nespremenjen): širitev vzorca P79 (1886) → P82 (1887) → P83 (1888) → P84 (1889) → P85 (1890) → P86 (1891) → P87 (1892) na leto 1893 — okvir: skeni 63–70 == tiskane strani 62–69 (stran == sken − 1; glava »1893~« na str. 62 po 1892 row 82; vpisi na skenih 63–68; velike cifre »1894« na str. 69 po row 83 — oznake se ponastavijo na 1, novela P83 potrjena 6. leto; 1893 ima 83 zveznih vrstic) — VSI vpisi z Griblji: 17 vpisov / 16 hiš (h27 DVOJČICI!): 60, 65, 41, 70, 23, 91, 27 ×2, 15, 46, 72, 30, 24, 74, 21, 25, 32 — NOVE hiše 4 (23, 46, 70, 91) + ponovitve 12 (h60 nova krstna — poroka 04455 1886) — skupaj s P79–P87 vzorec 156 vpisov / 66 hiš čez tri knjige in OSEM LET; NOVELA (novela P85 potrjena 4. leto): vsi statusi ulomki — ½ zemljak 13 + ¼ zemljak 4 (brez bajtarjev/obrtnikov); PT klasifikacija 13/3 (46 v luknji 41–60 — NOVA, 15. dokazana številka; 41 že dokazana P85, 60 P80; luknja zdaj 15 dokazanih); 0 nezakonskih; r50 brez babice (edini); r34 vsi starševski stolpci »isto« (ditto); SIDRA: h72 (oče Matija Strauš [~] — SIDRO 3. VPIS: ISTI oče 3× čez 6 let 1888+1891+1893; mati 1891+1893 ISTA Jakobič; botra Straucelj ISTA 2×; tri-virska P80 + PUA @71 0.8571 — najmočnejša veriga vzorca), h65 (oče Matija Milek [~] — ISTI 3×: 1887+1889+1893; Milek = P81 near-miss), h27 (DVOJČICI Antonija †13/9.93 + Ivana — vertikalni pripis »dvojčice«, 2. dvojčki v vzorcu po P85 h30; oče Janez Stukar/Stubhar [~] = 1887 Kukar + 1890 Stubhar ISTI; ISTA mati Katarina Klobučar — 3.+4. vpis; forenzika 5x: jasno 27, prvi prebir 24 [~]), h21 (oče Janez Požek [~] ISTI 1887+1893; MATI MENJANA: 1887 Brinec → 1893 Ana Šimec — 3. dokazana menjava matere po h61/h72; ŠIMEC NAZAJ NA GRIBLJIH — mati + botra Janez Šimec prvič od 1890; Požek 6. leto), h24 (Matija Brinec [~] × Barbara Jakobčič [~] — ISTA ZVEZA kot 1887; 5. VPIS; gospodinjstvi Brinec ↔ Jurajevič se izmenjujeta 1887→1892→1893), h30 (Peter Jakljevič [~] × Marija Kralj [~] — MENJAVA GOSPODINJSTVA Milek → Jakljevič; babica PRAZNA; podpis obiskni G. Ambrož? m.p.), h41 (Matija Hušič? [~] × Neža Jakobič [~] — ISTA ZVEZA kot 1890 Hrušič × Jakobčič; 3. vpis na luknji), h15 (Janez Jaklič [~] × Marija Brinec [~] — ISTA ZVEZA kot 1887 Jakšič × Brinec), h60 (NOVA — oče Nikolaj Željko [~] = h1 oče 1888+1892 — ŽELJKO 2. HIŠA: h1 → h60), h91 (NOVA — botra Nikolaj Željko + Katarina Kure = h1 starši priimki — Željko signal 3. hiša), h74 (mrliška 04894 1886 Hambeč [~] → Kambič? [~] — čez knjige varianta), h25 (poroka 04455 1886 Klepec GRIBLJE 25 → 1893 Matija Hrižan × Ana Požek — menjava gospodinjstva; 2. Hrižan oče), h32 (oče Matija Meh/Mrh? [~] — MERI: ISTA mati Pegdirec + ISTA botra Hrižan/Strauš kot 1892 Urh — isti oče z novo brano priimko ali drug mož); ŽELJKO VERIGA 3 hiše (h1 + h60 + h91 botra); ŠIMEC nazaj (2 signala); babice: Trotter 9× (dominanta) + Ana Hrižan 3× + Barbara Adlešič 2× + Ana Križan 1× + Ana Klepec 1× + prazna 1; DUHOVNIKI: Jos. Rauq [~] 14 (Jan–Avg) + NOV Janez Jelovšek? [~] 2 (od septembra) + G. Ambrož? m.p. 1 (obiskni); live verifikacija: knjiga HTTP 200 (inventar 326), citirani skeni 6/6 JPEG 200; skripta scripts/p88_parish_baptism_1893.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1893",
  "P88: PARISH OF PODZEMELJ — BAPTISM REGISTER 04105, THE FULL YEAR 1893 (issue #18; SAMPLE-TRANSCRIPTION-1893; MEASURES, does not decide; the v7 join unchanged): extending the P79 (1886) → P82 (1887) → P83 (1888) → P84 (1889) → P85 (1890) → P86 (1891) → P87 (1892) sample to 1893 — the frame: scans 63–70 == printed pages 62–69 (page == scan − 1; the »1893~« heading on p. 62 after the 1892 row 82; entries on scans 63–68; the large figures »1894« on p. 69 after row 83 — the labels restart at 1, the P83 novel confirmed for the 6th year; 1893 has 83 continuous rows); ALL Griblje entries: 17 entries / 16 houses (h27 TWINS!): 60, 65, 41, 70, 23, 91, 27 ×2, 15, 46, 72, 30, 24, 74, 21, 25, 32 — 4 NEW houses (23, 46, 70, 91) + 12 repeats (h60 a new baptism — the 1886 marriage 04455) — with P79–P87 the sample totals 156 entries / 66 houses across three books and EIGHT years; NOVEL (the P85 novel confirmed for the 4th year): all statuses fractions — ½ smallholder 13 + ¼ smallholder 4 (no cottagers/craftsmen); the PT classification 13/3 (46 in the 41–60 gap — NEW, the 15th proven number; 41 already proven P85, 60 P80; the gap now has 15 proven); 0 illegitimates; r50 without a midwife (the only one); r34 all parent columns »isto« (ditto); ANCHORS: h72 (father Matija Strauš [~] — the ANCHOR'S 3rd ENTRY: THE SAME father 3× across 6 years 1888+1891+1893; the mother 1891+1893 THE SAME Jakobič; godmother Straucelj THE SAME 2×; the three-source P80 + PUA @71 0.8571 — the strongest chain of the sample), h65 (father Matija Milek [~] — THE SAME 3×: 1887+1889+1893; Milek = the P81 near-miss), h27 (TWINS Antonija † + Ivana — the vertical note »dvojčice«, the 2nd twins in the sample after the P85 h30; father Janez Stukar/Stubhar [~] = 1887 Kukar + 1890 Stubhar THE SAME; THE SAME mother Katarina Klobučar — the 3rd+4th entries; 5x forensics: clearly 27, first read 24 [~]), h21 (father Janez Požek [~] THE SAME 1887+1893; MOTHER CHANGE: 1887 Brinec → 1893 Ana Šimec — the 3rd proven mother change after h61/h72; ŠIMEC BACK IN GRIBLJE — mother + godfather Janez Šimec for the first time since 1890; Požek the 6th year), h24 (Matija Brinec [~] × Barbara Jakobčič [~] — THE SAME COUPLE as 1887; the 5th ENTRY; the Brinec ↔ Jurajevič households alternate 1887→1892→1893), h30 (Peter Jakljevič [~] × Marija Kralj [~] — HOUSEHOLD CHANGE Milek → Jakljevič; midwife EMPTY; visiting signature G. Ambrož? m.p.), h41 (Matija Hušič? [~] × Neža Jakobič [~] — THE SAME COUPLE as 1890 Hrušič × Jakobčič; the 3rd entry on the gap), h15 (Janez Jaklič [~] × Marija Brinec [~] — THE SAME COUPLE as 1887 Jakšič × Brinec), h60 (NEW — father Nikolaj Željko [~] = the h1 father 1888+1892 — ŽELJKO'S 2nd HOUSE: h1 → h60), h91 (NEW — godparents Nikolaj Željko + Katarina Kure = the h1 parents' surnames — the Željko signal, a 3rd house), h74 (mrliška 04894 1886 Hambeč [~] → Kambič? [~] — the cross-book variant), h25 (the 1886 marriage 04455 Klepec GRIBLJE 25 → 1893 Matija Hrižan × Ana Požek — a household change; the 2nd Hrižan father), h32 (father Matija Meh/Mrh? [~] — MEASURES: THE SAME mother Pegdirec + THE SAME godparents Hrižan/Strauš as the 1892 Urh — either the same father with a newly read surname or another husband); THE ŽELJKO CHAIN of 3 houses (h1 + h60 + h91 godparents); ŠIMEC back (2 signals); midwives: Trotter 9× (the dominant) + Ana Hrižan 3× + Barbara Adlešič 2× + Ana Križan 1× + Ana Klepec 1× + empty 1; PRIESTS: Jos. Rauq [~] 14 (Jan–Aug) + NEW Janez Jelovšek? [~] 2 (from September) + G. Ambrož? m.p. 1 (visiting); live verification: the book HTTP 200 (inventory 326), cited scans 6/6 JPEG 200; the script scripts/p88_parish_baptism_1893.py (I1–I10, --check PASS); status SAMPLE-TRANSCRIPTION-1893",
  p88Errors.length === 0,
  p88Errors.length === 0
    ? `17 vpisov / 16 hiš — h27 DVOJČICI (0 neberljivih; 17 zasidranih v vitals) · okvir 1893 skeni 63–70 (vpisi 63–68; prelom 1894 str. 69; 83 zveznih vrstic) · NOVELA: ulomki, novela P85 potrjena 4. leto (½ 13 + ¼ 4) · PT 13/3 (46 NOVA — 15. dokazana luknja; 41/60 že znani) · nove hiše 4 (23, 46, 70, 91) + ponovitve 12 (h60 nova krstna) · sidra h72 Strauš SIDRO 3. VPIS (oče ISTI 3×) / h65 Milek oče ISTI 3× / h27 dvojčici (oče ISTI, ISTA mati) / h21 Šimec nazaj + mati menjana / h24 ISTA zveza 1887+1893 / h30 menjava Milek → Jakljevič / h41 ISTA zveza / h15 ISTA zveza / h60 Željko 2. hiša / h91 NOVA botra Željko · Željko veriga 3 hiše · Šimec nazaj · Rauq 14× + NOV Jelovšek? od sept.`
    : p88Errors.join("; "),
);
}
