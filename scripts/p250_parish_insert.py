#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P250 — vstavi P249-razdelek-komentar + 11 blokov (1874) v parish.ts pred P249-sekcijo."""

ROOT = "/home/z/my-project"
P = f"{ROOT}/src/data/atlas/parish.ts"

COMMENT = """  // ——— P250: POROČNA PREDZGOVINA 04455, leto 1874 = 12/13 — (s1–s7 + P249-tail-RE-VERIFIKACIJA; md5-7/7-s1–s7!-s7-križna-md5-2.-neodvisen-prenos-1:1-identičen-P249-disku!-s1-=-VEZALO!-Read-očesa-NAJPREJ-×7-P244-LEKCIJA!-+ VLM-pass-1-×5 + krops-×83 + mikro-forenzika-8×-×3!); ★★★ RESTART-1874 = s2-DNO (ZADNJA-vrsta-strani!-vpis-1 = '1874 Jänner 19.'-[~18-DUEL!]-Jakob-Pašič-×-Anna-Kunič-oba-34-l-WITWA-Z-OTROKI!-NI-blok!) = 12.-MEJNA-VARIANTA (dno-vzorec-2.-instance-cf.-P243-s35!-P249-napoved-'s5-ali-s6'-FALSIFICIRANA-2×!) + ★★★ NOV-STRUKTURNI-DOKAZ: KNIJIŽNO-ODPIRANJE-04455-=-Pag.-1-=-s2-top-=-m18-'1873-Juni-11' (vpisi-m1–m17-leta-1873-NISO-v-tej-knjigi!-predhodnik-Trauungs-Buch!-1873-=-samo-m18–m21-kontekst!-m20-=-Griblje-[22~26]-×-[50~51]-MILEK-×-PEGDIRC!-m19-podpis-FERCHER!) + ★★★ MEJA-1873/74 = s2-MID/DNO = 13.-VARIANTA (tail-m21-'26.-Novembris-1873'-→-m1-NA-ISTI-STRANI!) · **m1–m32 = 32-VPISOV-BREZ-PRESKOKOV-9.-LETO** (P249-'1–27'-FALSIFICIRANO!-NODAT-×0-5.-leto!-m3-celica-'28'-BREZ-meseca-vzorec!) · ★★★ **11-BLOKOV-V-1-LETU-NOV-REKORD** (prej-6-P248!-10-hiš-h27-×2!-2-POLNI-DVOJNI-m6-h7×h4-+-m16-h29×h30!) + ★★★★★ **10-DVIGOV-REKORD** (h4-7-+ h7-15-+ h10-3-+ h27-7-+ h29-23-IZENAČUJE-h44!-+ h30-2-+ h33-14-+ h42-5-+ h43-**34-NOV-ABSOLUTNI-REKORD**!-+ h65-12!) · ★★★ 3-MNOŽIČNI-DANI-'8.-Februar'-×5-+-'11.-February'-×5-+-'14.-Juni'-×2 (10-porok-v-2-dneh!-vzorec-3.-leto!) + ★★★ P249-KOREKCIJA-m28-'28.-Februar'-MISREAD→'28.-Avgust'-1:1-KROP (kronologija!-+ NADEL-POPPRAVEK-rjavo-'23.'→vijolično-'28.-Aug'-cf.-P242-v9!) + m12-'Jänner-11'-DUEL→'11.-Februar'-KROP-1:1 + m26-prečrtan-prvotni-datum! · ★★★★★ FOLIACIJA-'Pag-=-sken−1'-5/5-1874 (s2-'Pag. 1'-…-s6-'Pag. 5'!) = 28/28-V-ZAPOREDNIH-LETIH-7.-LETO! · ★★★ HRIŽAN-×4 (m5-mati-+ m6-nevesta-h4!-+ m10-nevesta-×-h27!-+ m22-ženin-63-l-[Pribež!]-P-forenzika-NI-Griblje!) + ★★★ MILEK-×3 (m5-h65-+ m16-h29-+ priča-Marcus!-+ 1873-kontekst-m20!) + ★ H43-BRULA-PARALELA (Marina-1874-==-Katharina-1878-P246!-'43'-forenzika-8×!) + ★★★★★ h42-PROMOCIJA-NAPAVED-IZPOLNJENA (Maria-Pegdirc-tail→blok-cf.-P248-h30!) + ★★★ SEGINA-×2 (m12-+ m14-h27!) + HLEBEC-×2 + 63-l-ženin-×2 + **52-l-nevesta-REKORD-m17** (prej-46-P249!) + MLADOLETNICA-×2 (m5-19-l-Konsens!-+ m18-17-l!) + DOVGAN-CONTINUUM-**12-LET (1874–1885!)**-IZJEMI-×2 (m27-'Hegrič'-[~X-OPEN]-na-rednem!-1873-m19-Fercher!) ———
"""

BLOCKS = """  {
    houseNo: "65",
    bookSignature: "04455",
    year: 1874,
    scan: 3,
    page: 2,
    whatSi: "poroka 4. Februar 1874 (vpis 5, s3, margina-'5') — ženin Mathias MILEK, 32 let, GRIBLJE 65 (ultra-8×-1:1-'65'!-Kurrent-'5' = enojna-zanka+kavelj-NE-dvojna-zanka-'3'-cf.-m25-'43'-m10-'63'!-+ SKLAD-P246-h65-Anna-MILEK-1878-'65'-NE-63/68-ODLOČILNO!) × nevesta Katharina [Hlavasič~Starasič~Hlavasem-3-branja!], 19 let (8×-'19'-'9'-z-repkom-1:1!-MLADOLETNICA!), Krasinec 23; starši ženina: Miko MILEK × Margareta BRODA; starši neveste: Johann [Škaradi~Harasič] × Maria **HRIŽAN**; duhovnik Franz Dovgan; Befunde: zettel-Griblje-4.-Febr-1874-+ Consens-k.k.-31.-Jänner-st.-Minderjährig-der-Braut!; + ★★★★★ h65-04455-firstYear-1886→1874-DVIG-ZA-12-LET (MILEK-HIŠA-1:1!-P246-1878-h65-Anna-MILEK-=-bride-KONTEKST-ne-blok!) + ★★★ MILEK-×2-BLOKA-V-1-LETU (m5-h65-+ m16-h29!-+ priča-Marcus-Milek!) + HRIŽAN-v-starših!",
    whatEn: "marriage Feb 4, 1874 (entry 5, s3, margin-'5') — groom Mathias MILEK, 32 y., GRIBLJE 65 (ultra-8×-1:1-'65'!-the-Kurrent-'5'-single-loop+hook-NOT-the-double-loop-'3'!-+ SKLAD-P246-ODL-of-1878!) × bride Katharina [3-reads!], 19 y. (8×-'19'-the-'9'-with-tail-1:1!-MINOR!), Krasinec 23; groom's parents: Miko MILEK × Margareta BRODA; bride's parents: Johann [~] × Maria **HRIŽAN**; priest Franz Dovgan; Befunde: zettel-Griblje-Feb-4-1874-+ Consens-k.k.-Jan-31-st.-Minderjährig-der-Braut!; + ★★★★★ h65-firstYear-1886→1874-DVIG-BY-12-YEARS (the-MILEK-HOUSE-1:1!) + ★★★ MILEK-×2-blocks-in-1-year + HRIŽAN-among-parents!",
    status: "DOCUMENTED" as const,
  },
  {
    houseNo: "7",
    bookSignature: "04455",
    year: 1874,
    scan: 3,
    page: 2,
    whatSi: "poroka 4. Februar 1874 (vpis 6, s3, margina-'6') — ženin Johann [Totlhar~Tošhar~Botlhar-X-OPEN-3-branja!], 36 let, GRIBLJE 7 (mikro-1:1-'Griblje 7'!) × nevesta Katharina HRIŽAN, 26 let (NE-16!-'2'-zanka-forenzika-očesi-misread!), GRIBLJE 4 [~]; duhovnik Franz Dovgan; Befunde: zettel-Griblje-3.-Febr-1874; + ★★★ POLNI-DVOJNI-BLOK-h7×h4! + ★★★★★ h7-04455-firstYear-1889→1874-DVIG-ZA-15-LET (h7-že-v-korpusu-4-bloki-min-1889!) + ★★★★★ h4-04455-firstYear-1881→1874-DVIG-ZA-7-LET (cf.-P242-h4-nevesta-1881!) + HRIŽAN-×2-v-1-vpisu-kontekst (m5-mati!)",
    whatEn: "marriage Feb 4, 1874 (entry 6, s3, margin-'6') — groom Johann [3-reads-X-OPEN!], 36 y., GRIBLJE 7 (mikro-1:1!) × bride Katharina HRIŽAN, 26 y. (NOT-16!-the-'2'-loop-forensics!-the-eyes-misread-rejected!), GRIBLJE 4 [~]; priest Franz Dovgan; Befunde: zettel-Griblje-Feb-3-1874; + ★★★ THE-FULL-DOUBLE-BLOCK-h7×h4! + ★★★★★ h7-firstYear-1889→1874-DVIG-BY-15-YEARS + ★★★★★ h4-firstYear-1881→1874-DVIG-BY-7-YEARS + HRIŽAN-×2-in-1-entry!",
    status: "DOCUMENTED" as const,
  },
  {
    houseNo: "4",
    bookSignature: "04455",
    year: 1874,
    scan: 3,
    page: 2,
    whatSi: "poroka 4. Februar 1874 (vpis 6, s3, margina-'6' — NEVESTA-polovica-polnega-dvojnega!-cf.-h7-blok!) — nevesta-Katharina-HRIŽAN-26-l-GRIBLJE-4-[~]-ženin-Johann-[Totlhar~]-36-l-GRIBLJE-7! + ★★★★★ h4-04455-firstYear-1881→1874-DVIG-ZA-7-LET (h4-krstna-1871-z35-TOMC-kontekst-P242!-h4-že-v-korpusu-1-blok-1881!)",
    whatEn: "marriage Feb 4, 1874 (entry 6, s3, margin-'6' — the-BRIDE-half-of-the-full-double!-cf.-h7-block!) — bride-Katharina-HRIŽAN-26-y.-GRIBLJE-4-[~]-groom-Johann-[~]-36-y.-GRIBLJE-7! + ★★★★★ h4-firstYear-1881→1874-DVIG-BY-7-YEARS!",
    status: "DOCUMENTED" as const,
  },
  {
    houseNo: "27",
    bookSignature: "04455",
    year: 1874,
    scan: 4,
    page: 3,
    whatSi: "poroka 8. Februar 1874 [množični-dan-×5!] (vpis 10, s4, margina-'10') — ženin Jacob [Skulhan~Brikhan~Kruhar-X-OPEN-3-branja!], **63 let**-NAJSTAREJŠI-ŽENIN-KANDIDAT-PREDZGOVINE (cf.-P243-v11-'69'-[~X-OPEN]-+ m22-tudi-63!), GRIBLJE 27 (polna-vrsta-1:1-'Griblje 27'-G-ornament!-pass1-'Črneč-14'-pasme-artefakt-ZAVRŽEN!) × nevesta Anna HRIŽAN, 31 let, [Vitob~Witob] 26 [~]; starši neveste: Peter HRIŽAN × Anna HLEPEC (cf.-m22-Anna-Hlebec!); duhovnik Franz Dovgan; Befunde: zettel-'vom-Gemeindeamte-GRIBLJE-dd-8.-Febr-874'-+ podpis-scrawl-'M.Oppranm?'-[~X-OPEN]; + ★★★ h27-04455-firstYear-1881→1874-DVIG-ZA-7-LET (cf.-P242-h27-×2-1881!)",
    whatEn: "marriage Feb 8, 1874 [the-MASS-DAY-×5!] (entry 10, s4, margin-'10') — groom Jacob [3-reads-X-OPEN!], **63 y.-the-OLDEST-GROOM-CANDIDATE** (cf.-P243-'69'-[~X-OPEN]-+ m22-also-63!), GRIBLJE 27 (full-row-1:1!-the-pass1-'Črneč-14'-band-artifact-REJECTED!) × bride Anna HRIŽAN, 31 y., [Vitob~] 26 [~]; bride's parents: Peter HRIŽAN × Anna HLEPEC; priest Franz Dovgan; Befunde: zettel-'vom-Gemeindeamte-GRIBLJE-dd-8.-Febr-874'-+ the-signature-scrawl-[~X-OPEN]; + ★★★ h27-firstYear-1881→1874-DVIG-BY-7-YEARS!",
    status: "DOCUMENTED" as const,
  },
  {
    houseNo: "27",
    bookSignature: "04455",
    year: 1874,
    scan: 5,
    page: 4,
    whatSi: "poroka 11. Februar 1874 [množični-dan-×5!] (vpis 14, s5, margina-'14') — ženin Michael SEGINA [~Sagina!], [23~33-X-OPEN], ½-Hüfler, GRIBLJE 27 (mikro-1:1-'Gribje 27'-G-ornament!-pass1-'Milozze'-ZAVRŽEN!) × nevesta [Olganul~]-JAKŠA, 21 let, [Uranoviče~Crnaviče~Hrastovice]-[14~19-X-OPEN]; duhovnik Franz Dovgan; + ★★★ h27-2.-BLOK-V-1-LETU-3.-×-LINIJE (cf.-P242-h27-×2-1881!-P244-h16!) + ★★★ SEGINA-NIT (m12-Georg-Segina-kontekst-+ P249-SEGINA!)",
    whatEn: "marriage Feb 11, 1874 [the-MASS-DAY-×5!] (entry 14, s5, margin-'14') — groom Michael SEGINA [~!], [23~33-X-OPEN], ½-Hüfler, GRIBLJE 27 (mikro-1:1!-the-pass1-'Milozze'-REJECTED!) × bride [Olganul~]-JAKŠA, 21 y., [3-reads]-[14~19-X-OPEN]; priest Franz Dovgan; + ★★★ h27-the-2nd-BLOCK-in-1-year-the-3rd-×-of-the-line + ★★★ the-SEGINA-thread!",
    status: "DOCUMENTED" as const,
  },
  {
    houseNo: "33",
    bookSignature: "04455",
    year: 1874,
    scan: 5,
    page: 4,
    whatSi: "poroka 11. Februar 1874 [množični-dan-×5!] (vpis 15, s5, margina-'15') — ženin [Leopold~Solomon?]-CERNIE [~X-OPEN-ime-3-branja!], 40 let, GRIBLJE 33 (3×-1:1-krops!-+ 2./3.-vrstica-celice-'und-Vredenj'~'Theresia-№13'-[~X-OPEN]) × nevesta Maria HUŠIČ, 40 let (ime-2:1-očesi+mikro!-pass1-'Elisabeth'-ZAVRŽENO!), Ceroviče 30; duhovnik Franz Dovgan; + ★★★ h33-04455-firstYear-1888→1874-DVIG-ZA-14-LET (h33-že-v-korpusu-4-bloki-min-1888!) + CERNIE/ČERNE-nit-cf.-m23-ČERNIČ!",
    whatEn: "marriage Feb 11, 1874 [the-MASS-DAY-×5!] (entry 15, s5, margin-'15') — groom [Leopold~Solomon?]-CERNIE [~X-OPEN-name!], 40 y., GRIBLJE 33 (3×-1:1!-+ the-2nd/3rd-cell-lines-'und-Vredenj'~'Theresia-№13'-[~X-OPEN]) × bride Maria HUŠIČ, 40 y. (the-name-2:1!-the-pass1-'Elisabeth'-REJECTED!), Ceroviče 30; priest Franz Dovgan; + ★★★ h33-firstYear-1888→1874-DVIG-BY-14-YEARS + the-CERNIE/ČERNE-thread!",
    status: "DOCUMENTED" as const,
  },
  {
    houseNo: "29",
    bookSignature: "04455",
    year: 1874,
    scan: 5,
    page: 4,
    whatSi: "poroka 11. Februar 1874 [množični-dan-×5!] (vpis 16, s5, margina-'16') — ženin Johann MILEK, 44 let, ½-Instmann, GRIBLJE 29 (mikro-2×-1:1!-pass1-'Verček'-garble-ZAVRŽEN!) × nevesta Maria [geb.-Grabrijan~Stubler-Witwa-X-OPEN!], 50 let, GRIBLJE 30 (mikro-1:1!); starši ženina: †Nikolaus [Milek~Urban] × †Anna [Urban~Urbas]; starši neveste: †Nikolaus GRABRIJAN × †Anna BUKOVEC; priče: Marcus **MILEK** × Grabrijan [~]; duhovnik Franz Dovgan; + ★★★ POLNI-DVOJNI-BLOK-h29×h30! + ★★★★★ h29-04455-firstYear-1897→1874-DVIG-ZA-23-LET-**IZENAČUJE-ABSOLUTNI-REKORD-h44-P248** (1899→1876-=-23!) + ★★★★ h30-04455-firstYear-1876→1874-ZA-2-LETA (cf.-P248-h30-v14-née-PEGDIRE!) + MILEK-×2-v-1-letu-2.-blok!",
    whatEn: "marriage Feb 11, 1874 [the-MASS-DAY-×5!] (entry 16, s5, margin-'16') — groom Johann MILEK, 44 y., ½-Instmann, GRIBLJE 29 (mikro-2×-1:1!-the-pass1-'Verček'-garble-REJECTED!) × bride Maria [geb.-Grabrijan~Stubler-Witwa-X-OPEN!], 50 y., GRIBLJE 30 (mikro-1:1!); groom's parents: †Nikolaus [Milek~Urban] × †Anna [Urban~Urbas]; bride's parents: †Nikolaus GRABRIJAN × †Anna BUKOVEC; witnesses: Marcus **MILEK** × Grabrijan [~]; priest Franz Dovgan; + ★★★ THE-FULL-DOUBLE-BLOCK-h29×h30! + ★★★★★ h29-firstYear-1897→1874-DVIG-BY-23-YEARS-**TIES-THE-ABSOLUTE-RECORD-h44-P248** + ★★★★ h30-firstYear-1876→1874-BY-2-YEARS + MILEK-×2-in-the-year!",
    status: "DOCUMENTED" as const,
  },
  {
    houseNo: "30",
    bookSignature: "04455",
    year: 1874,
    scan: 5,
    page: 4,
    whatSi: "poroka 11. Februar 1874 [množični-dan-×5!] (vpis 16, s5, margina-'16' — NEVESTA-polovica-polnega-dvojnega!-cf.-h29-blok!) — nevesta-Maria-[Grabrijan-Stubler-Witwa?]-50-l-GRIBLJE-30! + ★★★★ h30-04455-firstYear-1876→1874-ZA-2-LETA (P248-h30-v14-Anna-PEGDIRE-'Leinmannstochter'-1876!-h30-PEZDIRC-mati-kontekst!)",
    whatEn: "marriage Feb 11, 1874 [the-MASS-DAY-×5!] (entry 16, s5, margin-'16' — the-BRIDE-half-of-the-full-double!-cf.-h29-block!) — bride-Maria-[Grabrijan-Stubler-Witwa?]-50-y.-GRIBLJE-30! + ★★★★ h30-firstYear-1876→1874-BY-2-YEARS (the-P248-h30-v14-Anna-PEGDIRE-1876!)",
    status: "DOCUMENTED" as const,
  },
  {
    houseNo: "10",
    bookSignature: "04455",
    year: 1874,
    scan: 5,
    page: 4,
    whatSi: "poroka 16. Februar 1874 (vpis 17, s5, margina-'17') — ženin Mathias KRAUE [~Kraac!], 56 let, [gemeinde-Genosse~?], GRIBLJE №10 (mikro-1:1-'Griblje №10'!-celica-2.-vrstica-'[Gern~Gradec?]-28'-[~X-OPEN]-pass1-'Gornje-Gradec-28'-delno!) × nevesta Anna VIPAVEC [~Vpavec-Vpravec!], **52 let-NAJSTAREJŠA-NEVESTA-PREDZGOVINE-REKORD** (prej-P249-v13-Katharina-Stubler-46-l!-+ m16-50-l!), Krasinec 33 (mikro-1:1-'Krasine 33'!-očesi-'Drasine'-VLM-'Vipavc'-ZAVRŽENA!); duhovnik Franz Dovgan; + ★★★★★ h10-04455-firstYear-1877→1874-ZA-3-LETA (cf.-P247-h10-nevesta-1887→1877!)",
    whatEn: "marriage Feb 16, 1874 (entry 17, s5, margin-'17') — groom Mathias KRAUE [~!], 56 y., [gemeinde-Genosse~?], GRIBLJE №10 (mikro-1:1!-the-2nd-cell-line-'[Gern~Gradec?]-28'-[~X-OPEN]) × bride Anna VIPAVEC [~!], **52 y.-THE-OLDEST-BRIDE-OF-THE-PREHISTORY-RECORD** (previously-the-P249-v13-46-y!-+ m16-50-y!), Krasinec 33 (mikro-1:1!); priest Franz Dovgan; + ★★★★★ h10-firstYear-1877→1874-BY-3-YEARS!",
    status: "DOCUMENTED" as const,
  },
  {
    houseNo: "43",
    bookSignature: "04455",
    year: 1874,
    scan: 6,
    page: 5,
    whatSi: "poroka 14. Juni 1874 [×2-dan!] (vpis 25, s6, margina-'25') — nevesta Marina [~Martin-DUEL-P245-vzorec!] **BRULA**, 27 let, GRIBLJE 43 (ultra-8×-1:1-'Gribje 43'!-Kurrent-'4'-odprti-vrh-forenzika-NE-'93'/'33'!) × ženin [ime-X-OPEN-'Gmeind-Vorsteher'-v-stolpcu-ime~Jožef-Vlašič~Anton-Rotte-3-branja!], 32 let, [Dolenice~Smasine]-43-p.-Adlešiči; duhovnik Franz Dovgan; + ★★★★★ **H43-BRULA-PARALELA-1:1**: Marina-Brula-1874-==-Katharina-BRULA-1878-P246-v5-bride-KONTEKST-ISTA-HIŠA-ISTA-PRIIMEK (P249-h42-vzorec-2.-instance!) → **h43-04455-firstYear-1908→1874-DVIG-ZA-34-LET-NOV-ABSOLUTNI-REKORD-DVIGA** (prej-h44-P248-23-let!)",
    whatEn: "marriage Jun 14, 1874 [the-×2-day!] (entry 25, s6, margin-'25') — bride Marina [~Martin-DUEL!] **BRULA**, 27 y., GRIBLJE 43 (ultra-8×-1:1-'Gribje 43'!-the-Kurrent-'4'-open-top-forensics-NOT-'93'/'33'!) × groom [name-X-OPEN-'Gmeind-Vorsteher'-in-the-name-column~3-reads!], 32 y., [Dolenice~Smasine]-43-p.-Adlešiči; priest Franz Dovgan; + ★★★★★ **THE-H43-BRULA-PARALLEL-1:1**: Marina-Brula-1874-==-Katharina-BRULA-1878-the-SAME-HOUSE-the-SAME-SURNAME → **h43-firstYear-1908→1874-DVIG-BY-34-YEARS-NEW-ABSOLUTE-RECORD**!",
    status: "DOCUMENTED" as const,
  },
  {
    houseNo: "42",
    bookSignature: "04455",
    year: 1874,
    scan: 7,
    page: 6,
    whatSi: "poroka 18. November 1874 (vpis 32, s7-tail, margina-'32' — P249-mikro-6×-1:1-RE-VERIFIKACIJA!) — nevesta Maria **PEGDIRC**, GRIBLJE 42 × ženin Nicolaus Marasinič [~], Krasinice 12, 48 let, ½-g.-+ Dispens-3-leonisticnih-gradov-P249! — ★★★★★ **NAPAVED-P250-IZPOLNJENA**: h42-tail-kontekst-P249-→-PROMOCIJA-V-BLOK (cf.-P248-h30-vzorec!) + **h42-04455-firstYear-1879→1874-ZA-5-LET** (Georg-Pegdirc-1879-P244-v21!-h42-PARALELA-PEZDIRC-ISTA-HIŠA-ISTA-PRIIMEK-2-dokaza-5-let-narazen!-PEZDIRC-CONTINUUM-04455-v-7.-letu-predzgodovine!)",
    whatEn: "marriage Nov 18, 1874 (entry 32, s7-tail, margin-'32' — the-P249-mikro-6×-1:1-RE-VERIFICATION!) — bride Maria **PEGDIRC**, GRIBLJE 42 × groom Nicolaus Marasinič [~], Krasinice 12, 48 y., ½-g.-+ the-Dispens-P249! — ★★★★★ **THE-P250-FORECAST-FULFILLED**: the-h42-tail-context-P249-→-PROMOTION-TO-A-BLOCK (cf.-P248-h30!) + **h42-firstYear-1879→1874-BY-5-YEARS** (the-h42-PARALLEL-PEZDIRC-2-evidences-5-years-apart!)",
    status: "DOCUMENTED" as const,
  },
"""

src = open(P, encoding="utf-8").read()
anchor = "  // ——— P249: POROČNA PREDZGOVINA 04455, leto 1875 = 11/13"
assert anchor in src, "P249-anchor ni najden!"
assert "year: 1874,\n    scan: 3," not in src, "P250-bloki že vstavljeni!"
src = src.replace(anchor, COMMENT + BLOCKS + anchor, 1)
open(P, "w", encoding="utf-8").write(src)
print("P250: 11 blokov + komentar vstavljenih v parish.ts")
