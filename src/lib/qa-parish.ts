// qa-parish.ts — župnija Podzemelj: matrične kontrole (qa-p79 + qa-p80) izvlečene
// iz qa.ts runQA (P80: telo glavne funkcije je preseglo prag TS control flow
// analysis; vzorec ločevanja modulov). Deterministično iz runtime podatka
// parish.ts + pini PT klasifikacije/okvirjev; paleografske faze so ročne in
// dokumentirane v dokazih research/issue17/parish-*.json; live verifikatorja:
// scripts/p79_parish_sample.py --check (I1–I8) in scripts/p80_parish_md_books.py
// --check (I1–I10). Produkcija ne bere research/ (P53/P57/P58) — pini živijo tu.

import { HOUSE_VITALS, PARISH_BOOKS } from "@/data/atlas/parish";

type Push = (id: string, nameSi: string, nameEn: string, pass: boolean, detail: string) => void;

export function parishChecks(push: Push): void {
// ——— qa-p79: župnija Podzemelj — vzorčni prepis matrik (issue #18; HOUSE_VITALS;
//      deterministično iz runtime podatka parish.ts + pini PT klasifikacije;
//      paleografska faza dokumentirana v research/issue17/parish-sample-transcription.json,
//      live verifikator scripts/p79_parish_sample.py --check I1–I8) ———
// P80: kontrola je omejena na KRSTNE vpise (04105) — poročni/mrliški iz P80
// imajo svojo kontrolno qa-p80-parish-md-books
const p79Hv = HOUSE_VITALS.filter((h) => h.bookSignature === "04105");
const p79Errors: string[] = [];
// PT klasifikacija (pin iz research/issue13/chain-full-pt-ps.json; PT 1825:
// 84 hiš 1–40 + 61–99 z polovičkami; LUKNJA 41–60) — produkcija ne bere
// research/, zato klasifikacija živi kot pin (vzorec p76 pini)
const P79_PT_IN_SET = ["8", "16", "11", "36", "94", "39", "13", "71", "75", "61"];
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
  "P79: ŽUPNIJA PODZEMELJ — VZORČNI PREPIS MATRIČNIH VPISOV Z GRIBELJSKIMI HIŠNIMI ŠT. (issue #18; vir Matricula Online, Krstna knjiga 04105 1886–1919; paleografska faza + deterministična verifikacija; deterministično, brez AI ob delovanju): VZOREC = polno leto 1886 (skeni 2–15 == tiskane strani 1–14: VSI vpisi z Griblji v tem letu) + sidro 1887 (verifikacija obstoječega zapisa hiše 61) — 15 vpisov / 13 različnih hiš (8 [~], 11, 13, 16, 36×2 — dve družini pod eno št. [~], 39, 54, 56, 57, 61, 71, 75, 94) — NAD merili issue #18 (vzorec 5 hiš); vsak vpis: signatura + leto + stran/skan + hišna št. + otrok + starši (Kurrent z [~]); okvir 1886: 12 vpisov, skeni 2–15, stran == sken − 1 (kontrola sken 11 → stran 10, sken 20 → 19); PT usklajenost (pin iz chain-full-pt-ps.json: 84 hiš 1–40 + 61–99 z polovičkami, LUKNJA 41–60): 10/13 hiš v naboru (8, 11, 13, 16, 36, 39, 61, 71, 75, 94), 3/13 (54, 56, 57) v luknji 41–60 — DOKAZ ŠTEVILČNE EVOLUCIJE med 1825 in 1886 (številčna usklajenost ≠ identiteta stavbe); hiša 36: 2 vpisa v 1886 (row 39 brez očeta — mati Barbara Šimec; row 95 oče Matija Križan) — dokumentirano kot zapisano; poznejši modri pripisi 20. st. (umrl dne …, npr. hiša 39: umrl 18.9.1961 v Gribljah št. 39 — potrjuje hišno št.) dokumentirani ločeno; sidro: hiša 61 (sken 20, stran 19, vrstica 28 — Katarina) ponovno prebrana in POTRJENA (sken/leto/hiša/ime == parish.ts; oče: obe branji dokumentirani — »Miha P.—« obstoječe / »Miko Jože H.?« ponovno); live verifikacija: knjiga HTTP 200, inventar 326 slik (base64 dekodiranje), citirani skeni 10/10 JPEG 200; skripta scripts/p79_parish_sample.py (I1–I8, --check PASS); status SAMPLE-TRANSCRIPTION",
  "P79: PARISH OF PODZEMELJ — SAMPLE TRANSCRIPTION OF REGISTER ENTRIES WITH GRIBLJE HOUSE NUMBERS (issue #18; source Matricula Online, Baptism register 04105 1886–1919; paleographic phase + deterministic verification; deterministic, no AI at runtime): SAMPLE = the full year 1886 (scans 2–15 == printed pages 1–14: ALL Griblje entries in that year) + the 1887 anchor (verification of the existing house-61 record) — 15 entries / 13 distinct houses (8 [~], 11, 13, 16, 36×2 — two families under one number [~], 39, 54, 56, 57, 61, 71, 75, 94) — ABOVE the issue #18 criteria (a 5-house sample); every entry: signature + year + page/scan + house number + child + parents (Kurrent with [~]); the 1886 frame: 12 entries, scans 2–15, page == scan − 1 (controls scan 11 → page 10, scan 20 → 19); the PT consistency (pin from chain-full-pt-ps.json: 84 houses 1–40 + 61–99 with halves, the GAP 41–60): 10/13 houses in the set (8, 11, 13, 16, 36, 39, 61, 71, 75, 94), 3/13 (54, 56, 57) in the 41–60 gap — EVIDENCE OF NUMERIC EVOLUTION between 1825 and 1886 (numeric consistency ≠ building identity); house 36: 2 entries in 1886 (row 39 without a father — mother Barbara Šimec; row 95 father Matija Križan) — documented as written; later blue 20th-century annotations (died …, e.g. house 39: died 18 Sep 1961 in Griblje no. 39 — confirms the house number) documented separately; the anchor: house 61 (scan 20, page 19, row 28 — Katarina) re-read and CONFIRMED (scan/year/house/child == parish.ts; the father: both readings documented — »Miha P.—« existing / »Miko Jože H.?« re-read); live verification: the book HTTP 200, an inventory of 326 images (base64 decoding), the cited scans 10/10 JPEG 200; the script scripts/p79_parish_sample.py (I1–I8, --check PASS); status SAMPLE-TRANSCRIPTION",
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
const p80All = HOUSE_VITALS;
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

}
