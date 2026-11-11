#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P258 — vstavitev 16 blokov (1831-konec m14–m24 + 1832 m1–m23 + 1833 m1–m6) v parish.ts
za zadnjim P257-blokom (h11-1831, vrstica 14330). Korpus 2043 → 2059; byBook-01738 31 → 47."""

SRC = "src/data/atlas/parish.ts"

HEADER = '''  // ——— P258: NOTRANJOST-01738 — MEJA-1831/32/33! (s8–s10 = Pag. 13/15/17; foliacija-Pag-=-2·sken−3-potrjena-×9-svinčnik-15/16-+17/18!) — 40-VPISOV (11+15+14 — NAJVEČJA-NOTRANJOST-FAZA!): 1831-KONEC-m14–m24 (s8: 9.-Febr-d°-12.-poroka-istega-dne! + 14.-Febr-×2 + 6.-Juni + 24.-Juli + 24.-Aug-×2-KLOBUČAR-BRATJE! + 1.-Nov-BARON! + 6.-9ber + 20.-9ber + 23.-9ber-d°) + 1832-m1–m23 (s9-RESTART-18.-Jän-×3-+-25./29.-Jän + 15.-Febr-×4-+-22. + 29.-Febr-×5-PRESTOPNI-DAN! + s10: 29.-Febr-×4 + 5.-März + 28.-Mai + 20.-Juni + 28.-Nov) + 1833-m1–m6 (s10-spodaj: [~3.|5.]-Febr-RESTART-1833!-letnica-NAD-datumom! + 6.-Febr-×5-d°) · ★★★★★ 16-BLOKOV-10-DVIGOV (h8-40 = 2.-NAJVEČJI-DVIG-VSEH-ČASOV-za-h22-41-P255! + h46-36-+-h66-36-IZENAČITA-3.-mesto! + h35-35 + h47-31 + h42-29 + h2-27 + h48-26 + h36-25 + h49-25) · ★★★★★★ ŠEST-KNJIŽNI-KLUB-23→31 (+8: h2/h8/h35/h36/h42/h46/h47/h48 — 2.-NAJVEČJI-SKOK-za-+7-P257!) · ★★★★★★ PEZDIRC-h50-NIT-NADGRADNJA: 1831-Georg-PESDIRZ-h50 (oče-MARCO!-P257) + 1833-Johann-PESDIRZ-h50 (oče-MARCO!-★-3×-črko-za-črko-'P-e-s-d-i-r-z'-row+duel+region!-[~Petroviz-zavrnjen]) = ★-DVA-SINA-ISTEGA-OČETA-MARCA-h50-(oba-21-l-!) + 1873-Marcus-PEGDIRE-h50 (P251!) = DRUŽINA-1831–1873-42-LET-×3-VPISI + ★-1831-priča-AND.-PEZDIRC (m14!-5.-vrstica-družine-1831!) · ★★★★★ MILEK-h22-DOMNEVA-POTRJENA: 1830-Anna-Milek-oče-Joh.-+ 1832-Johann-MILEK-h22-oče-Johann (duel-'k'-ne-'ch'!) = ISTA-DRUŽINA-h22-4-bloki-v-5-letih (1828+1829+1830+1832!-1831-edina-luknja!) · ★★★★★ KRIŽAN-KONGLOMERAT-1831/32: 1831-h3-Peter + 1832-h36-Nicol (POLNI-DVOJNI-h36×h35!) + 1832-h66-Johann (★-KRIŽAN×KRIŽAN-PAR!) + 1873-h63-RESTART = KRIŽAN-4-GRIBLJE-HIŠE (3+36+66+63!) · ★★★★★ h35-×2-DVE-DRUŽINI-1832 (m8-Štremuz-15.-Febr + m17-Flach-29.-Febr — 2-pora-v-14-dneh-iz-h35!-cf.-h28-×2-1873!) + FLACH-×2-nit (h35-+h61-1832!) · ★★★★ KLOBUČAR-BRATJE-m19×m20-24.-Aug (h46×h8-+-h48×h2-DVA-POLNA-DVOJNA-ISTEGA-DNEVA!-[~bratje-kand.]) + HLEBEC-h2-1832-ženin ↔ 1873-m11-h3-P253 (41-let!) + h2-×2-ZAPOREDNI-LETI (1831-nevesta-Kleberz-+-1832-ženin-Hlebec!) · ★★★ ANOMALIJE-1832-×2: m2-MARIA-Vipavz-ŽENSKO-IME-V-ŽENINSKEM-STOLPCU (duel-črko-za-črko-'M-a-r-i-a'-končnica-'a'!-cf.-P257-m7!) + m3-[~Marino-MOŠKI|Maria?-DUEL]-Talkarigh + ★★★ BARON-VRSTICA-m21-1831 (Aloys-BARON-k.k.-[~Postmeister?]-v-pokoj-u-Gradac-1-×-Helena-[~Rubi]!-EDINA-plemiško-uradniška-vrstica-notranjosti!) + MUZ-NIT-1833 (Catharina-MUZ-oče-Nicol-Semelj!-continuum-1828+1831!) + ŠIMIČ-[~Simig/Himiz]-kand.-h56-1832-+-h49-1833 + METLIKA-1831-m18 (Ferjančec!-2.-omemba-po-1830-METLIKA-140!) + SALOKA-IN-CROATIA-1832-×2! ———
'''

BLOCKS = '''
  {
    houseNo: "47",
    bookSignature: "01738",
    year: 1831,
    scan: 8,
    page: 13,
    whatSi: "poroka m14 (9. Febr-d°-vrstica = 12. poroka istega dne!, s8, Pag. 13 — 1. vpis nadaljevanja 1831 iz Pag. 11!) — NEVESTA Maria KLOBUČAR [~Klobuchar], 20 l, ehel. Tochter, GRIBLJE 47 (duel-'Grible-47'-jasno-2:1-nad-'17'!) × ženin Andreas [~Mercina|Hribar|Luminanic?—3-variant-TEŽAK-GARBLE-X-OPEN], 19 l, ehel. Sohn, ŠKRILJE 1 (oče Josep [~Mercina]); priči: ★ AND. PEZDIRC! (duel-'Pezdirc'-jasno!-[~Simon-zavrnjen]) + Dorothea [~] (+[~Košir?|Klobučar? 6?]); + ★★★★★ PRIČA-AND.-PEZDIRC-1831 = 5.-VRSTICA-Pesdirc-družine-leta-1831 (m2-ženin-Georg-h50 + m3-nevesta + m7-ANOMALIJA + m13-nevesta + m14-PRIČA!) — PEZDIRC-leta-1831-×5-VRSTIC-VSEH-VRST! + ★★★ h47-firstYear-1862→1831-DVIG-ZA-31-LET + h47-VSTOPA-V-ŠEST-KNJIŽNI-KLUB (23→31!) + h47-span-1831–1919-=-88-let + 24→25-blokov",
    whatEn: "marriage m14 (Feb 9-d° = the 12th wedding of that day!, s8, Pag. 13 — the 1831 continuation from Pag. 11) — BRIDE Maria KLOBUČAR, 20, GRIBLJE 47 (duel-'47'-2:1!) × groom Andreas [~Mercina|Hribar|Luminanic?—3-variant-GARBLE-X-OPEN], 19, ŠKRILJE 1; witnesses: AND. PEZDIRC! + Dorothea [~]; + ★★★★★ THE-WITNESS-AND.-PEZDIRC-1831 = the-5th-ROW-of-the-Pesdirc-family-in-1831 (groom + 2-brides + the-anomaly + now-a-WITNESS!) + the-h47-firstYear-1862→1831-LIFT-BY-31 + h47-ENTERS-THE-SIX-BOOKS-CLUB (23→31!) + h47-span-1831–1919-=-88-years + 24→25 blocks",
    status: "DOCUMENTED" as const,
  },
  {
    houseNo: "46",
    bookSignature: "01738",
    year: 1831,
    scan: 8,
    page: 13,
    whatSi: "poroka m19 (24. Avgust 1831, s8, Pag. 13) — ženin Matthias KLOBUČAR, 27 l, [~ledina], GRIBLJE 46 (hiša-46-×3-branj-1:1!) × nevesta Catharina [~Klofčič|Klopčič?—DUEL], 18 l, GRIBLJE 8 — POLNI DVOJNI (h46×h8!); starši ženina: Mathias Klobučar; starši neveste: Matthias [~Klofčič]; urkunde: 'Publice in [~] vulgo den 8ten [~]'; + ★★★ h46-firstYear-1867→1831-DVIG-ZA-36-LET (IZENAČI-h56-P257-3.-mesto-vseh-časov!-zdaj-h46/h56/h66-trojni!) + h46-VSTOPA-V-ŠEST-KNJIŽNI-KLUB (23→31!) + ★★★★ KLOBUČAR-BRATJE-m19×m20 (24.-Avg-DVA-POROKI-ISTEGA-DNE!-h46-×-h48-[~bratje-kand.-X-OPEN-različna-hiši-sorodstvo?]) + h46-span-1831–1920-=-89-let",
    whatEn: "marriage m19 (Aug 24, 1831, s8, Pag. 13) — groom Matthias KLOBUČAR, 27, GRIBLJE 46 × bride Catharina [~Klofčič], 18, GRIBLJE 8 — THE FULL DOUBLE (h46×h8!); groom's father: Mathias Klobučar; + the-h46-firstYear-1867→1831-LIFT-BY-36 (ties-h56-the-3rd-place!) + h46-ENTERS-THE-SIX-BOOKS-CLUB + the-KLOBUČAR-BROTHERS-m19×m20 (two-weddings-of-the-same-day!) + h46-span-1831–1920-=-89-years",
    status: "DOCUMENTED" as const,
  },
  {
    houseNo: "8",
    bookSignature: "01738",
    year: 1831,
    scan: 8,
    page: 13,
    whatSi: "poroka m19 (24. Avgust 1831, s8, Pag. 13) — NEVESTA Catharina [~Klofčič|Klopčič?—DUEL], 18 l, GRIBLJE 8 (hiša-8-×3-branj-1:1!) × ženin Matthias KLOBUČAR, 27 l, GRIBLJE 46 — POLNI DVOJNI (h46×h8!); starši neveste: Matthias [~Klofčič]; + ★★★★★ h8-firstYear-1871→1831-DVIG-ZA-40-LET = 2.-NAJVEČJI-DVIG-VSEH-ČASOV (za-h22-41-P255!-pred-h46/h66-36-+-h56-36!) + h8-VSTOPA-V-ŠEST-KNJIŽNI-KLUB (23→31!) + h8-span-1831–1919-=-88-let + 25→26-blokov",
    whatEn: "marriage m19 (Aug 24, 1831, s8) — BRIDE Catharina [~Klofčič], 18, GRIBLJE 8 × groom Matthias KLOBUČAR, 27, GRIBLJE 46 — THE FULL DOUBLE (h46×h8!); + ★★★★★ the-h8-firstYear-1871→1831-LIFT-BY-40 = THE-2ND-LARGEST-EVER (after-h22-41-P255!) + h8-ENTERS-THE-SIX-BOOKS-CLUB + h8-span-1831–1919-=-88-years + 25→26 blocks",
    status: "DOCUMENTED" as const,
  },
  {
    houseNo: "48",
    bookSignature: "01738",
    year: 1831,
    scan: 8,
    page: 13,
    whatSi: "poroka m20 (24. Avgust-d° 1831, s8, Pag. 13 — istega dne kot m19!) — ženin Johann KLOBUČAR, 29 l, ledig, GRIBLJE 48 (hiša-48-×3-branj-1:1!) × nevesta Anna [~Kleberz=KLEBEC-kand.!|Scalec?|Krebelz?—3-variant-DUEL-X-OPEN], 24 l, GRIBLJE 2 — POLNI DVOJNI (h48×h2!); starši neveste: [~Vincenz Paron??-BARON-m21-veza-kand.-X-OPEN!]; + ★★★ h48-firstYear-1857→1831-DVIG-ZA-26-LET + h48-VSTOPA-V-ŠEST-KNJIŽNI-KLUB (23→31!) + ★★★★ KLOBUČAR-BRATJE-kand. (m19-±m20-24.-Avg!-h46/h48-družini) + h48-span-1831–1922-=-91-let (IZENAČI-h11/h33!)",
    whatEn: "marriage m20 (Aug 24-d° 1831, s8 — the same day as m19!) — groom Johann KLOBUČAR, 29, GRIBLJE 48 × bride Anna [~Kleberz?—3-variant-DUEL], 24, GRIBLJE 2 — THE FULL DOUBLE (h48×h2!); bride's father: [~Vincenz Baron?-cand.!]; + the-h48-firstYear-1857→1831-LIFT-BY-26 + h48-ENTERS-THE-SIX-BOOKS-CLUB + the-KLOBUČAR-brothers-cand. + h48-span-1831–1922-=-91-years",
    status: "DOCUMENTED" as const,
  },
  {
    houseNo: "2",
    bookSignature: "01738",
    year: 1831,
    scan: 8,
    page: 13,
    whatSi: "poroka m20 (24. Avgust-d° 1831, s8, Pag. 13) — NEVESTA Anna [~Kleberz=KLEBEC-kand.!|Scalec?—DUEL], 24 l, GRIBLJE 2 (hiša-2-×3-branj-1:1!) × ženin Johann KLOBUČAR, 29 l, GRIBLJE 48 — POLNI DVOJNI (h48×h2!); + ★★★★★ h2-firstYear-1858→1831-DVIG-ZA-27-LET + h2-VSTOPA-V-ŠEST-KNJIŽNI-KLUB (23→31!) + ★★★★ h2-×2-01738-ZAPOREDNI-LETI (1831-Kleberz-nevesta + 1832-HLEBEC-ženin-m16!) + ★★★ HLEBEC-NIT-NAJAVLJENA: 1832-h2-ženin-Johann-Hlebec ↔ 1873-m11-Hlebec-h3-P253 (41-let!-h2/h3-sosednji-hiši-Griblje!) + h2-span-1831–1924-=-93-let (IZENAČI-h20/h22/h50-3.-mesto!)",
    whatEn: "marriage m20 (Aug 24-d° 1831, s8) — BRIDE Anna [~Kleberz?], 24, GRIBLJE 2 × groom Johann KLOBUČAR, 29, GRIBLJE 48 — THE FULL DOUBLE (h48×h2!); + ★★★★★ the-h2-firstYear-1858→1831-LIFT-BY-27 + h2-ENTERS-THE-SIX-BOOKS-CLUB + h2-×2-in-01738-CONSECUTIVE-YEARS (1831-bride + 1832-groom!) + the-HLEBEC-THREAD: 1832-h2 ↔ 1873-m11-h3-P253 (41-years!) + h2-span-1831–1924-=-93-years",
    status: "DOCUMENTED" as const,
  },
  {
    houseNo: "22",
    bookSignature: "01738",
    year: 1832,
    scan: 9,
    page: 15,
    whatSi: "poroka m8 (15. Februar 1832, s9, Pag. 15 — množični-dan-15.-Febr-×4!) — ženin Johann MILEK (duel-črko-za-črko-zadnja-črka-KURRENT-'k'-NE-'ch'!-[~Milch/Mikau-alt-zavrnjena]), 26 l, GRIBLJE 22 (oče ★ Johann [Milch/Milek]!-census-R-'Johann-Mihl'!) × nevesta Anna [~Štremuz|Štremiz?—DUEL], 21 l, GRIBLJE 35 — POLNI DVOJNI (h22×h35!); starši neveste: Johann [~Štremiz]; + ★★★★★★ MILEK-h22-DOMNEVA-POTRJENA: 1830-Anna-MILEK-h22 (oče-Joh.!-P257) + 1832-Johann-MILEK-h22 (oče-Johann!) = ISTA-DRUŽINA (brat-sestra!-[~Miller-garble-1828/1829-VERJETNO-ISTA-družina-h22-X-OPEN]) + ★★★★★ h22-4.-BLOK-V-5-LETIH (1828+1829+1830+1832!-1831-EDINA-LUKNJA-v-5-letnem-oknu!-prej-3-zaporedna-leta-P257!) + h22-OSTAJA-šest-knjižna (firstYear-1828-nedotaknjen!-35→36-blokov!)",
    whatEn: "marriage m8 (Feb 15, 1832, s9, Pag. 15 — the mass-day-Feb-15-×4!) — groom Johann MILEK (letter-by-letter-Kurrent-'k'-NOT-'ch'!), 26, GRIBLJE 22 (father Johann!) × bride Anna [~Štremuz?], 21, GRIBLJE 35 — THE FULL DOUBLE (h22×h35!); + ★★★★★★ THE-MILEK-h22-HYPOTHESIS-CONFIRMED: the-1830-Anna-MILEK + the-1832-Johann-MILEK (both-children-of-Johann!) = THE-SAME-FAMILY (brother-and-sister!-[~the-1828/1829-Miller-garble-LIKELY-the-same-family]) + ★★★★★ the-h22-4th-BLOCK-IN-5-YEARS (1828+1829+1830+1832!-1831-the-ONLY-gap!) + h22-stays-six-book (35→36 blocks!)",
    status: "DOCUMENTED" as const,
  },
  {
    houseNo: "35",
    bookSignature: "01738",
    year: 1832,
    scan: 9,
    page: 15,
    whatSi: "poroka m8 (15. Februar 1832, s9, Pag. 15) — NEVESTA Anna [~Štremuz|Štremiz?—DUEL], 21 l, GRIBLJE 35 (hiša-35-×4-branj-1:1!) × ženin Johann MILEK, 26 l, GRIBLJE 22 — POLNI DVOJNI (h22×h35!); + ★★★★★ h35-firstYear-1867→1832-DVIG-ZA-35-LET (5.-največji-vseh-časov!) + h35-VSTOPA-V-ŠEST-KNJIŽNI-KLUB (23→31!) + ★★★★★ h35-×2-DVE-DRUŽINI-V-1832 (m8-Štremuz-15.-Febr + m17-Flach-29.-Febr — DVA-PAROV-AV-14-DNEH-IZ-ISTE-HIŠE!-cf.-h28-×2-1873-P253!) + h35-span-1832–1922-=-90-let + 27→29-blokov (2-v-1832!)",
    whatEn: "marriage m8 (Feb 15, 1832, s9) — BRIDE Anna [~Štremuz?], 21, GRIBLJE 35 × groom Johann MILEK, 26, GRIBLJE 22 — THE FULL DOUBLE (h22×h35!); + ★★★★★ the-h35-firstYear-1867→1832-LIFT-BY-35 (the-5th-largest!) + h35-ENTERS-THE-SIX-BOOKS-CLUB + ★★★★★ h35-TWICE-TWO-FAMILIES-IN-1832 (m8-Feb-15 + m17-Feb-29 — two-couples-in-14-days-from-the-same-house!-cf.-h28-×2-1873!) + h35-span-1832–1922-=-90-years + 27→29 blocks",
    status: "DOCUMENTED" as const,
  },
  {
    houseNo: "2",
    bookSignature: "01738",
    year: 1832,
    scan: 10,
    page: 17,
    whatSi: "poroka m16 (29. Februar 1832 — PRESTOPNI-DAN!, s10, Pag. 17 — množični-dan-29.-Febr-×9-v-cez-2-strani!) — ženin Johann [~Hlebez=HLEBEC!|Klebez?—duel-Kurrent-'H'-visoka-z-zalomom-K-zanka!], 21 l ('sein Sohn'!), GRIBLJE 2 (oče ★ Johann [Hlebez], kmet-Bauer!) × nevesta Anna [~Petriz], 17 l, [~GRIBLJE-2:1|Smrečje?-DUEL-VAS-X-OPEN] 42 (oče Matth. [Petriz], kmet!); + ★★★★ h2-2.-blok-01738-ZAPOREDNI-LETI (1831-Anna-Kleberz-NEVESTA + 1832-Johann-Hlebec-ŽENIN — ISTA-hiša-2-drugi-vlogi!) + ★★★★★ HLEBEC-NIT-1832→1873: Johann-Hlebec-h2-1832 ↔ m11-Hlebec-GRIBLJE-3-1873-P253 (41-let!-sosednji-hiši-h2/h3!)",
    whatEn: "marriage m16 (Feb 29, 1832 — THE-LEAP-DAY!, s10, Pag. 17 — the-mass-day-Feb-29-×9-across-2-pages!) — groom Johann [~Hlebez=HLEBEC!], 21 ('sein Sohn'!), GRIBLJE 2 (father Johann, a-farmer!) × bride Anna [~Petriz], 17, [~GRIBLJE-2:1|Smrečje?-VILLAGE-DUEL] 42; + h2-second-01738-block-CONSECUTIVE-YEARS (1831-a-bride + 1832-a-groom!) + ★★★★★ THE-HLEBEC-THREAD-1832→1873: Johann-Hlebec-h2 ↔ the-m11-Hlebec-h3-1873-P253 (41-years!)",
    status: "DOCUMENTED" as const,
  },
  {
    houseNo: "42",
    bookSignature: "01738",
    year: 1832,
    scan: 10,
    page: 17,
    whatSi: "poroka m16 (29. Februar 1832 — prestopni dan!, s10, Pag. 17) — NEVESTA Anna [~Petriz], 17 l, [~GRIBLJE-2:1|Smrečje?-DUEL-VAS-X-OPEN-2-glasovi-za-Grüble-1-Smrečje!] 42 (oče Matth. [Petriz], kmet) × ženin Johann [~Hlebec], 21 l, GRIBLJE 2 — POLNI DVOJNI-[~] (h2×h42!); + ★★★ h42-firstYear-1861→1832-DVIG-ZA-29-LET-[~village-DUEL-ostaja] + h42-VSTOPA-V-ŠEST-KNJIŽNI-KLUB-[~DUEL-vas] (23→31!) + h42-span-1832–1912-=-80-let + 23→24-blokov",
    whatEn: "marriage m16 (Feb 29, 1832, s10) — BRIDE Anna [~Petriz], 17, [~GRIBLJE-2:1|Smrečje?-VILLAGE-DUEL] 42 × groom Johann [~Hlebec], 21, GRIBLJE 2 — THE-FULL-DOUBLE-[~] (h2×h42!); + the-h42-firstYear-1861→1832-LIFT-BY-29-[~village-duel-remains] + h42-ENTERS-THE-SIX-BOOKS-CLUB-[~] + h42-span-1832–1912-=-80-years + 23→24 blocks",
    status: "DOCUMENTED" as const,
  },
  {
    houseNo: "36",
    bookSignature: "01738",
    year: 1832,
    scan: 10,
    page: 17,
    whatSi: "poroka m17 (29. Februar-d° 1832 — prestopni dan!, s10, Pag. 17) — ženin Nicol KRIŽAN [Kirshan/Kirichen/Kirishan-×4-branj-1:1!], 20 l (oče ★ Matthias Križan!), GRIBLJE 36 (hiša-36-×3-branj-1:1!) × nevesta Catharina [~Flach=FLAHA?], 17 l (oče ★ Peter Flach!), GRIBLJE 35 — POLNI DVOJNI (h36×h35!); + ★★★★★★ KRIŽAN-KONGLOMERAT-GRIBLJE: 1831-h3-Peter-KRIŽAN (P257-m1!) + 1832-h36-Nicol + 1832-h66-Johann (m22!) + 1873-h63-RESTART-m1-KURE (P253!) = KRIŽAN-4-GRIBLJE-HIŠE (3+36+66+63!)+HRIŽAN-h62-ŠIV = ★-5-hiš-istega-korena! + ★★★ h36-firstYear-1857→1832-DVIG-ZA-25-LET + h36-VSTOPA-V-ŠEST-KNJIŽNI-KLUB (23→31!) + h36-span-1832–1917-=-85-let",
    whatEn: "marriage m17 (Feb 29-d° 1832 — the-leap-day!, s10, Pag. 17) — groom Nicol KRIŽAN, 20 (father Matthias Križan!), GRIBLJE 36 × bride Catharina [~Flach], 17 (father Peter Flach!), GRIBLJE 35 — THE FULL DOUBLE (h36×h35!); + ★★★★★★ THE-KRIŽAN-CONGLOMERATE: 1831-h3-Peter + 1832-h36-Nicol + 1832-h66-Johann + 1873-h63-the-RESTART = KRIŽAN-4-GRIBLJE-HOUSES (3+36+66+63!) + the-HRIŽAN-h62-seam = 5-houses-of-one-root! + the-h36-firstYear-1857→1832-LIFT-BY-25 + h36-ENTERS-THE-SIX-BOOKS-CLUB + h36-span-1832–1917-=-85-years",
    status: "DOCUMENTED" as const,
  },
  {
    houseNo: "35",
    bookSignature: "01738",
    year: 1832,
    scan: 10,
    page: 17,
    whatSi: "poroka m17 (29. Februar-d° 1832, s10, Pag. 17) — NEVESTA Catharina [~Flach=FLAHA?—DUEL-'Flach'-2:1-nad-'Tienk'], 17 l, GRIBLJE 35 × ženin Nicol KRIŽAN, 20 l, GRIBLJE 36 — POLNI DVOJNI (h36×h35!) — 2.-PAR-IZ-h35-V-14-DNEH (m8-Štremuz-15.-Febr + m17-Flach-29.-Febr = DVE-DRUŽINI-h35-1832!); oče ★ Peter Flach!; + ★★★ FLACH-×2-NIT-1832 (m17-Catharina-h35 + m23-Anna-[Filach]-h61 — FLACH-družina-×2-hiši!) + 28→29-blokov-h35",
    whatEn: "marriage m17 (Feb 29-d° 1832, s10) — BRIDE Catharina [~Flach], 17, GRIBLJE 35 × groom Nicol KRIŽAN, 20, GRIBLJE 36 — THE FULL DOUBLE (h36×h35!) — the-2nd-couple-from-h35-in-14-days (TWO-FAMILIES-of-h35-in-1832!); father Peter Flach!; + ★★★ the-FLACH-×2-THREAD (m17-Catharina-h35 + m23-Anna-[Filach]-h61 — the-FLACH-family-in-2-houses!)",
    status: "DOCUMENTED" as const,
  },
  {
    houseNo: "66",
    bookSignature: "01738",
    year: 1832,
    scan: 10,
    page: 17,
    whatSi: "poroka m22 (20. Juni 1832, s10, Pag. 17) — ženin Johann KRIŽAN, 21 l (oče ★ Georg Križan!), GRIBLJE 66 (duel-'66'-3:1-nad-'6'-pass1+row+duel-jasno-druga-števka-zanka!) × nevesta Anna KRIŽAN, 26 l (oče ★ Johann Križan!), [~Kreuz=Križ?|Kraplje?—DUEL-VAS-X-OPEN] 35 — ★★★★★ KRIŽAN×KRIŽAN-PAR (2.-par-istega-priimka-v-01738-za-MUZ-1828-P255!-a-Križan-marrying-a-Križan!) — POLNI-DVOJNI-NE (nevesta-NI-iz-Griblje!); + ★★★★★ h66-firstYear-1868→1832-DVIG-ZA-36-LET (IZENAČI-h46/h56-3.-mesto-trojno!) + h66-5-KNJIG-BREZ-04455 (poročna-vrzela-hiše!-cf.-h25-smrtna-vrzela-P254!-04104+04105+04106+04894+01738) + KRIŽAN-konglomerat-4-hiše (3+36+66+63!) + h66-span-1832–1909-=-77-let",
    whatEn: "marriage m22 (Jun 20, 1832, s10, Pag. 17) — groom Johann KRIŽAN, 21 (father Georg Križan!), GRIBLJE 66 (duel-'66'-3:1-over-'6'!) × bride Anna KRIŽAN, 26 (father Johann Križan!), [~Kreuz?|Kraplje?-VILLAGE-DUEL] 35 — ★★★★★ A-KRIŽAN-MARRIES-A-KRIŽAN (the-2nd-same-surname-couple-after-MUZ-1828!); + ★★★★★ the-h66-firstYear-1868→1832-LIFT-BY-36 (ties-the-3rd-place-triple!) + h66-FIVE-BOOKS-WITHOUT-04455 (a-marriage-gap!-cf.-the-h25-death-gap!) + the-KRIŽAN-4-house-conglomerate + h66-span-1832–1909-=-77-years",
    status: "DOCUMENTED" as const,
  },
  {
    houseNo: "56",
    bookSignature: "01738",
    year: 1832,
    scan: 10,
    page: 17,
    whatSi: "poroka m23 (28. November 1832, s10, Pag. 17 — ZADNJI-VPIS-1832!) — ženin Peter [~Simig=ŠIMIČ?|Himiz?|Amiz?—3-variant-DUEL-X-OPEN-vsi-končajo-'-imiz'/'-imig'!], 36 l (oče ★ Nicol [~Šimič!]!), GRIBLJE 56 × nevesta Anna [~Filach=FLACH?|Tielak?—DUEL], 22 l (oče ★ Nicol [~Filach]!), GRIBLJE 61 — POLNI DVOJNI (h56×h61!); + ★★★★ h56-2.-blok-01738 (1831-Kiniz?-[P257] + 1832-[Šimič?] — ISTA-hiša-dve-družini!) + ★★★★ ŠIMIČ-[~Simig/Himiz]-KANDIDAT-NIT: 1832-Peter-[Simig]-h56-oče-Nicol-Šimič ↔ 1833-m6-nevesta-Maria-[Himiz]-h49 (ISTI-GARBLE-'-imiz'!-[~ŠIMIČ-družina-2-hiši-kand.-X-OPEN]) + FLACH-×2-nit (nevesta-Filach-h61!) + h56-span-1831–1908-=-77-let + 14→15-blokov",
    whatEn: "marriage m23 (Nov 28, 1832, s10 — the-LAST-entry-of-1832!) — groom Peter [~Simig=ŠIMIČ?—3-variant-DUEL-all-ending-'-imiz'!], 36 (father Nicol [~Šimič!]!), GRIBLJE 56 × bride Anna [~Filach=FLACH?], 22 (father Nicol [~Filach]!), GRIBLJE 61 — THE FULL DOUBLE (h56×h61!); + h56-second-01738-block (1831+1832!) + ★★★★ the-ŠIMIČ-[~Simig/Himiz]-CANDIDATE-THREAD: the-1832-h56-groom ↔ the-1833-h49-bride-Maria-[Himiz] (the-SAME-'-imiz'-garble!-[~one-family-in-2-houses-cand.]) + the-FLACH-×2-thread + h56-span-1831–1908-=-77-years",
    status: "DOCUMENTED" as const,
  },
  {
    houseNo: "61",
    bookSignature: "01738",
    year: 1832,
    scan: 10,
    page: 17,
    whatSi: "poroka m23 (28. November 1832, s10, Pag. 17) — NEVESTA Anna [~Filach=FLACH?|Tielak?—DUEL], 22 l, GRIBLJE 61 (oče ★ Nicol [~Filach]!) × ženin Peter [~Simig=ŠIMIČ?], 36 l, GRIBLJE 56 — POLNI DVOJNI (h56×h61!); + ★★★★ h61-3.-blok-01738 (1828-Miko-TILLAR-½-Gütl-P255! + 1832-Filach — 104-letni-span-od-Tillarja!) + TILLAR→FILACH-ZAMENJAVA-DRUŽIN-h61 ([~X-OPEN: prodana-kmetija-ali-priselitev?]) + h61-span-1828–1919-=-91-let-OSTAJA + 17→18-blokov + FLACH-×2-nit",
    whatEn: "marriage m23 (Nov 28, 1832, s10) — BRIDE Anna [~Filach=FLACH?], 22, GRIBLJE 61 (father Nicol!) × groom Peter [~Simig=ŠIMIČ?], 36, GRIBLJE 56 — THE FULL DOUBLE (h56×h61!); + ★★★★ h61-third-01738-block (1828-TILLAR + 1832-FILACH — the-family-change-of-h61!-[~X-OPEN]) + h61-span-1828–1919-=-91-years + 17→18 blocks + the-FLACH-×2-thread",
    status: "DOCUMENTED" as const,
  },
  {
    houseNo: "50",
    bookSignature: "01738",
    year: 1833,
    scan: 10,
    page: 17,
    whatSi: "poroka m6-1833 (6. Febr-d° 1833, s10, Pag. 17 — RESTART-leta-1833-[~3.|5.]-Febr-prva-vrstica!-6.-Febr-×5-d°-kaskada!) — ženin Johann PESDIRZ (★-TRIPLE-črko-za-črko-'P-e-s-d-i-r-z'-row+duel+region!-[~Petroviz-alt-ZAVRŽENA-2:1!]), 21 l, GRIBLJE 50 (★-oče MARCO PESDIRZ!-2×-prebrano-region+row!) × nevesta Maria [~Himiz|Simig?=ŠIMIČ?—DUEL-X-OPEN-isti-garble-kot-h56-1832!], 25 l, GRIBLJE 49 — POLNI DVOJNI (h50×h49!); + ★★★★★★ PEZDIRC-h50-NIT-3-VRSTICE-42-LET: 1831-Georg-PESDIRZ-h50 (oče-Marco!-P257) + 1833-Johann-PESDIRZ-h50 (oče-MARCO!) = ★-DVA-SINA-ISTEGA-OČETA-MARCA-(oba-21-let!) + 1873-Marcus-PEGDIRE-h50 (P251-m20-oče-neveste!) = ISTA-DRUŽINA-h50-1831–1873! + 12→13-blokov-h50 + h50-span-1831–1924-=-93-let",
    whatEn: "marriage m6-1833 (Feb 6-d° 1833, s10 — the-1833-RESTART-section!) — groom Johann PESDIRZ (★-TRIPLE-letter-by-letter-'P-e-s-d-i-r-z'!-[~Petroviz-rejected]), 21, GRIBLJE 50 (father MARCO PESDIRZ!) × bride Maria [~Himiz|Šimič?—DUEL], 25, GRIBLJE 49 — THE FULL DOUBLE (h50×h49!); + ★★★★★★ THE-PEZDIRC-h50-THREAD-3-ROWS-42-YEARS: the-1831-Georg + the-1833-Johann = ★-TWO-SONS-OF-THE-SAME-FATHER-MARCO (both-aged-21!) + the-1873-Marcus-PEGDIRE (P251!) = THE-SAME-FAMILY-1831–1873! + 12→13 blocks + h50-span-1831–1924-=-93-years",
    status: "DOCUMENTED" as const,
  },
  {
    houseNo: "49",
    bookSignature: "01738",
    year: 1833,
    scan: 10,
    page: 17,
    whatSi: "poroka m6-1833 (6. Febr-d° 1833, s10, Pag. 17 — ZADNJA-VRSTICA-STRani!) — NEVESTA Maria [~Himiz|Simig?=ŠIMIČ?—DUEL-X-OPEN-region-'H-i-m-i-z'!], 25 l, GRIBLJE 49 × ženin Johann PESDIRZ, 21 l, GRIBLJE 50 — POLNI DVOJNI (h50×h49!); starši neveste: [~Matthias-priimek-nejasen]; + ★★★ h49-firstYear-1858→1833-DVIG-ZA-25-LET + h49-5-KNJIG-BREZ-04455 (poročna-vrzela!-cf.-h66-1832!-04104+04105+04106+04894+01738) + [~Šimič-kand.-h56-1832-nit] + h49-span-1833–1918-=-85-let + 15→16-blokov",
    whatEn: "marriage m6-1833 (Feb 6-d° 1833, s10 — the-LAST-row-of-the-page!) — BRIDE Maria [~Himiz|Šimič?—DUEL-region-'H-i-m-i-z'!], 25, GRIBLJE 49 × groom Johann PESDIRZ, 21, GRIBLJE 50 — THE FULL DOUBLE (h50×h49!); + the-h49-firstYear-1858→1833-LIFT-BY-25 + h49-FIVE-BOOKS-WITHOUT-04455 (a-marriage-gap!-cf.-h66!) + [~the-Šimič-h56-cand.-thread] + h49-span-1833–1918-=-85-years + 15→16 blocks",
    status: "DOCUMENTED" as const,
  },
'''

src = open(SRC, encoding="utf-8").read()
lines = src.split("\n")
# vstavi za vrstico 14330 (1-based) = po '  },' koncu h11-bloka
assert lines[14329].strip() == "},", lines[14329]
assert "P251: POROČNA PREDZGOVINA" in lines[14330], lines[14330][:60]
insert = (HEADER + BLOCKS.strip("\n") + "\n").split("\n")
new_lines = lines[:14330] + insert + lines[14330:]
open(SRC, "w", encoding="utf-8").write("\n".join(new_lines))
print("vstavljeno:", len(insert), "vrstic; nova dolžina:", len(new_lines))
