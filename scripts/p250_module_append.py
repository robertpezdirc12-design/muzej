#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P250-OBNOVA: MARRIAGE_1874_* izvozi → parish-marriage-early.ts (append)."""
add = '''
// ——— P250: leto 1874 = 12/13 (s1–s7 + P249-tail-re-verifikacija; md5-7/7!-s7-križ-1:1-identičen-P249!-s1-vezalo!-Read-očesa-NAJPREJ-×7!-VLM-pass-1-×5 + krops-×83 + mikro-8×-×3!) — 32-VPISOV-BREZ-PRESKOKOV-9.-leto + 11-BLOKOV-NOV-REKORD + 10-DVIGOV + restart-s2-DNO-12.-varianta + KNIJIŽNO-ODPIRANJE-m18/1873! ———

export const MARRIAGE_1874_BLOCKS = HOUSE_VITALS.filter(
  (h) => h.bookSignature === "04455" && h.year === 1874,
);
export const MARRIAGE_1874_GRIBLJE = MARRIAGE_1874_BLOCKS.length;
export const MARRIAGE_1874_HOUSES = MARRIAGE_1874_BLOCKS.map((h) => h.houseNo);
export const MARRIAGE_1874_TOTAL = 32;

/** Meje 1874: RESTART-s2-DNO-12.-varianta + KNIŽNO-ODPIRANJE-m18/1873-Pag.-1! + MEJA-1873/74 = s2-MID/DNO-13.-varianta + MEJA-1874/75 = s7→s8-P249-re-verifikacija (m28-'28.-Februar'-KOREKCIJA→'28.-Avgust'!). */
export const MARRIAGE_1874_MEJA = {
  restartSi:
    "★★★ RESTART-1874 = s2-DNO (ZADNJA-vrsta-strani!-vpis-1 = '1874 Jänner 19.'-[~18-DUEL-pass1!]-Jakob-PAŠIČ-[~]-34-l-[Kramarše~?]-4-×-Anna-KUNIČ-[~]-34-l-WITWA-Z-OTROKI-(per-Befunde-pass1!)-NI-blok!) = 12.-MEJNA-VARIANTA (dno-vzorec-2.-instance-cf.-P243-'restart-1880 = s35-DNO'-7.!-P249-napoved-'restart-pričakovan-na-s5-top-ali-s6'-FALSIFICIRANA-2×: s5-top-=-m12!-s4-top-=-m7!)",
  restartEn:
    "★★★ THE-1874-RESTART = s2-BOTTOM (the-LAST-row-of-the-page!-entry-1 = Jan-19-1874-[~18-DUEL!]-Jakob-PAŠIČ-34-y-×-Anna-KUNIČ-34-y-a-WIDOW-WITH-CHILDREN!-NOT-a-block!) = the-12th-BOUNDARY-VARIANT (the-bottom-pattern-2nd-instance-cf.-P243!-the-P249-forecast-FALSIFIED-twice!)",
  knjiznoSi:
    "★★★ NOV-STRUKTURNI-DOKAZ — KNIJIŽNO-ODPIRANJE-04455: s1-=-VEZALO-KNJIGE (rjava-usnjena-povezava!-brez-tabele!) → Pag.-1-=-s2-TOP-=-m18-'1873-Juni-11' (očesi+VLM-2:1!-pass1-'Nov-8'-ZAVRŽEN!) — knjiga-se-odpira-**SREDI-ŠTEVILČENJA-1873**: vpisi-m1–m17-1873-NISO-V-TEJ-KNJIGI (nadaljevanje-iz-predhodnika!)-1873-=-SAMO-m18–m21! + 1873-kontekst: m18-=-Griblje-13-[~62!]-×-Maria-HRIŽAN-[62~66]-POLNI-DVOJNI-KANDIDAT-1873!-m19-=-podpis-'Dames-FERCHER' [~X-OPEN]-2.-duhovnik!-m20-=-**Johann-MILEK-GRIBLJE-[22~26]-×-Maria-POZDIRC/[~PEGDIRC]-GRIBLJE-[50~51]-POLNI-DVOJNI!**-PEZDIRC-že-1873!",
  knjiznoEn:
    "★★★ NEW-STRUCTURAL-EVIDENCE — THE-BOOK-OPENING-04455: s1-=-the-BOOK-COVER → Pag.-1-=-s2-TOP-=-m18-'Jun-11-1873' (2:1!-the-pass1-'Nov-8'-REJECTED!) — the-book-opens-MID-NUMBERING-of-1873: entries-m1–m17-are-NOT-IN-THIS-BOOK (continuation-from-a-predecessor!)-1873-=-ONLY-m18–m21! + the-1873-context: m18-=-the-FULL-DOUBLE-CANDIDATE-GRIBLJE-13-×-HRIŽAN!-m19-=-the-'Dames-FERCHER'-signature!-m20-=-**Johann-MILEK-GRIBLJE-×-Maria-PEGDIRC-GRIBLJE-FULL-DOUBLE!**-PEZDIRC-already-1873!",
  tailSi:
    "★★★ MEJA-1873/74 = s2-MID/DNO = 13.-MEJNA-VARIANTA (tail-1873-=-s2-margine-18–21-(11.-Juni–26.-Novembris-1873!)-→-RESTART-m1-NA-ISTI-STRANI-dno!-brez-finis!-brez-velike-glave!) · ★★★ MEJA-1874/75 = s7→s8-P249-1:1-RE-VERIFIKACIJA (finis-'f-i-n-i-s-/-1-8-7-4'-4.-instance-SODA-vzorec!-m32-=-18.-November!) · ★★★ P249-KOREKCIJA: m28-'28.-Februar'-MISREAD-→-**'28.-Avgust-1874'-1:1-KROP** (kronologija-m26/27-'5.-August'→m28-SKLAD!-+ Befunde-'23./8.-Aug'-PRED-poroko!-+ NADEL-POPPRAVEK-rjavo-'23.-Aug'→vijolično-'28.-Aug'-cf.-P242-v9!-m28-=-Josef-BAJUK-Primostek-[12~16]-25-l-×-NI-blok!-★-m29–m31-P249-leta-'8.-März'-'21.-April'-'21.-Mai'-kronološko-nemogoče-po-'28.-Aug'→[~X-OPEN-P251+-re-verifikacija!])",
  tailEn:
    "★★★ THE-1873/74-BOUNDARY = s2-MID/BOTTOM = the-13th-VARIANT (the-tail-on-the-same-page!) · ★★★ THE-1874/75-BOUNDARY = s7→s8-P249-RE-VERIFIED (the-finis-4th-instance!-m32-=-Nov-18!) · ★★★ THE-P249-CORRECTION: m28-'Feb-28'-MISREAD-→-**'Aug-28-1874'-1:1** (chronology-FITS!-+ the-NADEL-CORRECTION-brown-'23.'→violet-'28.-Aug'-cf.-P242-v9!)",
} as const;

/** Številčenje 1874 (s2-dno-1 · s3-2–6 · s4-7–11 · s5-12–18 · s6-19–27 · s7-28–32-P249!) — 32-vpisov-BREZ-preskokov-9.-leto! */
export const MARRIAGE_1874_NUMBERING =
  "s2-=-m1-DNO-restart-·-s3-=-2–6-·-s4-=-7–11-·-s5-=-12–18-·-s6-=-19–27-·-s7-=-28–32-P249!-— **32-VPISOV-BREZ-PRESKOKOV-9.-leto-zapored** (P249-napoved-'1–27'-FALSIFICIRANA!-NODAT-×0-5.-leto!-margine-modro-sivo-6.-leto!-m3-datum-celica-=-samo-'28'-BREZ-meseca-MESEC-SAMO-OB-SPREMEMBI-vzorec!)";

/** ★★★★★ FOLIACIJA-1874-'Pag = sken−1'-5/5 (s2-'Pag. 1' + s3-'Pag. 2' + s4-'Pag. 3' + s5-'Pag. 4' + s6-'Pag. 5'!-VSE-1:1-očesa+VLM!) — 28/28-v-zaporednih-letih-7.-leto! */
export const FOLIACIJA_1874 =
  "s2-'Pag. 1'-1:1-+ s3-'Pag. 2'-1:1-+ s4-'Pag. 3'-1:1-+ s5-'Pag. 4'-1:1-+ s6-'Pag. 5'-1:1-(očesa-+pass-1-DVOKRAT!-+ s1-vezalo-brez-Pag!)= 5/5-1874!-→ skupaj-z-4/4-1875-+ 4/4-1876-+ 4/4-1877-+ 6/6-1878-+ 5/5-1879-+ 4/4-1880 = 28/28-v-zaporednih-letih-7.-leto (+1873-kontekst-s2–s7-6/6!)";

/** ★★★ 3-MNOŽIČNI-POROČNI-DANI-v-1-letu: '8. Februar' ×5 (m7–m11!) + '11. Februar' ×5 (m12–m16!-mikro-6×-×3-m12/m13/m14!) + '14. Juni' ×2 (m24–m25!) = 10-porok-v-2-dneh! */
export const MNOZICNI_DANI_1874 =
  "'8. Februar 1874'-×5-(m7–m11-VSE-'8.'-1:1!)-+-'11. Februar 1874'-×5-(m12–m16-'11.'-mikro-6×-m12/m13/m14-1:1-×3!-Kurrent-'4'-odprti-vrh-vs-'874'-referenca!)-+-'14. Juni'-×2-(m24–m25!)-= 10-POROK-V-2-DNEH (cf.-P249-'4.-Februar'-×10-1-dan!-vzorec-3.-leto!-+ m12-DATE-DUEL-'Jänner-11'-očesi/pass1-→-'11.-Februar'-KROP-1:1-kronologija-VSILJUJE!-+ prečrtan-'Jänner'-ostanek-[~X-OPEN-pisarski-popravek-cf.-P242-v9!])";

/** ★★★★★ 10-DVIGOV-V-1-LETU-REKORD (prej-6-P248!) — h43-34-let-NOV-ABSOLUTNI-REKORD-DVIGA! */
export const FIRSTYEAR_1874_REKORDI =
  "h4-1881→1874-ZA-7-LET-+ h7-1889→1874-ZA-15-LET-+ h10-1877→1874-ZA-3-LET-+ h27-1881→1874-ZA-7-LET-+ h29-1897→1874-ZA-23-LET-IZENAČUJE-h44-P248-+ h30-1876→1874-ZA-2-LET-+ h33-1888→1874-ZA-14-LET-+ h42-1879→1874-ZA-5-LET-PROMOCIJA!-+ h43-1908→1874-ZA-34-LET-**NOV-ABSOLUTNI-REKORD-DVIGA**-+ h65-1886→1874-ZA-12-LET = 10-DVIGOV-V-1-LETU (prej-6-P248!-×1.67!)";

/** ★ H43-BRULA-PARALELA-1:1 (Marina-1874 == Katharina-1878-P246-bride-KONTEKST!-ISTA-HIŠA-ISTA-PRIIMEK!-'43'-forenzika-8×!) + h42-PROMOCIJA-NAPAVED-IZPOLNJENA! */
export const H43_1874_PARALELA =
  "Marina-[~Martin!]-BRULA-27-l-GRIBLJE 43-1874-m25-==-Katharina-BRULA-1878-P246-v5-bride-KONTEKST (ISTA-HIŠA-h43-ISTA-PRIIMEK!-hišna-'43'-ultra-8×-Kurrent-'4'-odprti-vrh-NE-'93'/'33'!-P249-h42-vzorec-2.-instance-cf.-P248-h30!)-+ h42-m32-Maria-PEGDIRC-PROMOCIJA (NAPAVED-P250-IZPOLNJENA!-h42-PARALELA-z-Georg-Pegdirc-1879-P244-v21!)";

/** ★★★ HRIŽAN-×4 + MILEK-×3 v 1 letu! */
export const HRIZAN_MILEK_1874 =
  "HRIŽAN-×4-omemb-v-1-letu (m5-mati-Maria-Hrižan!-+ m6-nevesta-Katharina-Hrižan-GRIBLJE 4-BLOK!-+ m10-nevesta-Anna-Hrižan-×-h27-BLOK!-+ m22-ženin-Joseph-Hrižan-63-l-[Pribež-P-forenzika-NI-Griblje!]-cf.-P246-'×3-BLOKI'-1874-=-×2-BLOKI-+ ×2-kontekst!)-+ MILEK-×3-V-1-LETU (m5-ženin-h65-BLOK-+ m16-ženin-h29-BLOK-+ m16-priča-Marcus-MILEK!-+ 1873-kontekst-m20-Johann-MILEK-×-PEGDIRC!)-MILIČ-križ-cf.-P248!";

/** ★★★ DOVGAN-KONTINUUM-PODALJŠAN-NA-12-LET (1874–1885!) — izjemi ×2! */
export const DOVGAN_1874_PODALJŠITEV =
  "Franz-Dovgan-podpisi-NA-VSIH-glavnih-vrstah-s2–s6-(m1–m27!)-+ s7-tail-P249!-garble-'Dorgor/Dorgan'!-kontinuum-**1874–1885-=-12-LET** (P249-'11-let'-PODALJŠAN-ZA-1-LETO-NAZAJ!)-IZJEMI-×2: (a)-m27-podpis-'[Justinius?]-HEGRIČ'-[~X-OPEN]-na-REDNEM-vpisu (cf.-P248-kaplan-Perschek-na-NAKNADNEM-violet!-NOV-vzorec!)-+ (b)-1873-kontekst-m19-'Dames-FERCHER' [~X-OPEN]-že-v-prvi-tabeli-knjige = 3-duhovniki-kontekst!";

/** m17-nevesta 52 l = NAJSTAREJŠA-nevesta-predzgodovine (prej 46 P249!) + 63-l-ženin ×2 + mladoletnici ×2! */
export const STAROSTI_1874 =
  "**m17-Anna-Vipavec-52-l-NAJSTAREJŠA-NEVESTA-PREDZGOVINE-REKORD** (prej-P249-v13-Katharina-Stubler-46!-+ m16-50-l-+ m22-48-l-+ m15-40-l!)-+ **63-l-ŽENIN-×2-V-1-LETU** (m10-Jacob-[Skulhan~Brikhan]-h27-+ m22-Joseph-Hrižan-[Pribež!]-cf.-P243-v11-'69'-[~X-OPEN]!)-+ MLADOLETNICA-×2-POTRJENA (m5-19-l-Konsens-st.-Minderjährig-der-Braut-k.k.-31.-Jänner!-+ m18-Maria-Jurajevič-17-l!)-+ m23-ženin-22-l-[~]-+ m1-WITWA-Z-OTROKI-[~]-+ m16/m26/m27-WITVE!";

/** P249-KOREKCIJE + krops-metodika (pasma-artefakti!-forenzika!) — P250-metoda. */
export const MARRIAGE_1874_METODA =
  "7-skenov-s1–s7-md5-7/7 (s7-križna-md5-2.-neodvisen-prenos-1:1-identičen-P249-disku-4d5ef99c!-s1-vezalo-1664×1800!) + Read-očesi-NAJPREJ-×7-P244-LEKCIJA (restart-s2-dno-najden-NA-OČESA!) + VLM-pass-1-×5-5/5-1.-poskus + krops-×48-+ pass-2b/2c/2d/2e/2f-korektne-pasme-×35 (očesi-na-krops-razkrila-pasme-zamik-×4!-s4-'Črneč-14'-artefakt-=-m11-'Premez 14'!-s6-komprimirane-vrstice!-s2-m1-pri-0.66!)+ solo-klici-×6-KRITIČNI + serije-×13 + mikro-forenzika-8×-×3 (m5-hiša-'65'-MILEK-P246-1:1!-m5-starost-'19'-'9'-z-repkom!-m25-hiša-'43'-BRULA-'4'-odprti-vrh!) + letterform-forenzika ('3'-dvojna-zanka-vs-'5'-enojna+kavelj!-'P'-vs-'G'-m22!-'1'-vs-'4'-m12!-'9'-z-repkom!-'2'-vs-'3'-m14-[X-OPEN]!) + reconciliacija-z-P249-tail (m28-KOREKCIJA!-m32-PROMOCIJA!) + hišna-sinhronizacija (h65-MILEK-P246-ODLOČILNA!) + pasme-artefakti-DOKUMENTIRANI ('Griblje-27'-vs-'Milozze'-vs-'Črneč-14'!-'Gribje-33'-vs-'Bojmavas 14'!)";

/** MARRIAGE_1874_DUELS — glavni dueli (rešeni + odprti pošteno). */
export const MARRIAGE_1874_DUELS = [
  "m12-datum-'Jänner-11'-očesi+pass1-vs-'11.-Februar'-KROP+kronologija-REŠEN-3:1-(+ prečrtan-'Jänner'-ostanek-[~X-OPEN-pisarski-popravek!]!)",
  "m5-hiša-'63'-očesi1+K-solo-4/5-vs-'65'-ultra-8×-forenzika+P246-MILEK-SKLAD-REŠEN-2:1!",
  "m6-nevesta-starost-'16'-očesi-vs-'26'-mikro+pass1-REŠEN-2:1-NI-mladoletnica!",
  "m22-wn-'Griblje'-očesi1-vs-'Pribež'-'P'-forenzika-K-solo+mikro-REŠEN-2:1-NI-blok-pošteno!",
  "m25-bride-wn-'33'-očesi1-vs-'93'-pass1-vs-'43'-ultra-8×-Kurrent-'4'+P246-BRULA-SKLAD-REŠEN!",
  "m25-bride-ime-'Anna'-očesi-vs-'Marina'-pass1+mikro-2:1-[~Martin-DUEL-ostaja-pošteno!]",
  "m25-ženin-ime-'Vlašič'-pass1-vs-'Rotte'-očesi-vs-'Gmeind-Vorsteher'-mikro-X-OPEN-3-branja!",
  "m14-starost-'23'-pass1+očesi-vs-'33'-X-OPEN-ostaja!-+ m14-bride-wn-'Uranoviče~Crnaviče~Hrastovice'-[14~19]-X-OPEN!",
  "m28-datum-'28.-Februar'-P249-vs-'28.-Avgust'-KROP+Befunde-chronologija-REŠEN-P249-KOREKCIJA!",
  "m1-datum-'19'-očesi-vs-'18'-pass1-X-OPEN!",
  "m16-groom-'Johann-Milek'-mikro-1:1-vs-'Verček'-pass1-vs-'Hafell'-serija-pasme-artefakt-REŠEN!",
  "m10-groom-'Skulhan~Brikhan~Kruhar'-3-branja-X-OPEN!",
  "m7-groom-'Hvalič'-pass1/batch-vs-'Hrovalj'-očesi-vs-'Hralj'-eltern-X-OPEN!-+ m26-'Johann-HRAUJ/HROVALJ'-mikro-1:1-H-jasna!-HROVALJ-nit-×2-kand.!",
  "m26-bride-'Maria-geb./w.-Hambič'-mikro-×2-vs-'Kraml'-pass1-vs-'Smuklič'-očesi-REŠEN-2:1-[Witwa-vs-geb.-X-OPEN]!",
  "m18-wn-'Otok~Stokl'-X-OPEN-(oba-ženi n-nevesta-para!)",
  "m1-wn-'Kramarše~?'-vs-'Vrhovlje'-pass1-X-OPEN!",
  "m3-datum-celica-'28'-BREZ-meseca-VLM-'Februar'-hallucinacija-ZAVRŽENA-kronologija-vsiljuje-'Jänner'-[~]!",
] as const;

/** MARRIAGE_1874_KONTEKST — ni-bloki-pošteno (1874 + 1873-tail!). */
export const MARRIAGE_1874_KONTEKST = [
  "m1-19.[~18.]-Jänner-Jakob-PAŠIČ-34-l-[Kramarše~?]-4-×-Anna-KUNIČ-34-l-WITWA-Z-OTROKI-[~]-zettel-[8~3.]-Jänner-RESTART-NI-blok",
  "m2-28.-Jänner-Johann-ORLIČ-25-l-[Hrastje~Skavin?]-14-×-Maria-[Hügel~Engel]-19-l-Dobrave-9-Möttling-pripis-dd.-26.-Jänner!-+ Consens-17.-Jänner!-NI-blok",
  "m3-28.[Jänner~]-Georg-[Grabowiec~]-27-l-[Cerhovice~]-[5~7]-×-Katharina-KRALJ-18-l-Mlake-10-zettel-Podzemelj-28.-Jänner-NI-blok",
  "m4-2.-Februar-Jakob-[Engel~]-39-l-[Vriho-glavce~]-31-×-Maria-[Rus~]-24-l-[Pudlo-vica~]-NI-blok",
  "m7-8.-Februar-Mathias-[Hvalič~Hrovalj~Hralj]-48-l-Boršt-[17~19]-×-Maria-[Šilah~Miklah~Filah]-19-l-Geriče-1-★ elternBride-Michael-ŠILAH-×-Kath.-Jaklič-(cf.-h34-SILAH-P247!)-NI-blok",
  "m8-8.-Februar-Georg-[Hvalič~Hralj]-Tischler-28-l-[Kapl.-9~]-×-Katharina-PLEH-24-l-Dolenec-42-NI-blok",
  "m9-8.-Februar-Peter-[Mušič~]-40-l-[Grendal~]-×-Maria-OGULIN-25-l-Gradac-1-NI-blok",
  "m11-8.-Februar-Marcus-Bertogneć-38-l-Premez-14-×-Anna-TASIČ-23-l-Begine-12-Möttling-dd.-27.-Jänner!-NI-blok",
  "m12-11.-Februar-Georg-SEGINA-24-l-[Pritlze~Milozze]-28-×-Katharina-KLEPEC-19-l-Boršt-21-NI-blok (SEGINA-×1!)",
  "m13-11.-Februar-Joseph-[Zeličko~]-31-l-[Orlova~Cerovice]-[16~18]-×-Katharina-[Herbanec~]-19-l-**KLOSTER-40**-(cf.-P247-'Klo-šter'-diskusija!)-NI-blok",
  "m18-26.-Februar-Nikolaus-ZUGELJ-30-l-½-Hübl-[Otok~Stokl]-18-×-Maria-JURAJEVIČ-17-l-[Otok~Stokl]-9-starši-n.-†Miha-Jurajevič-×-Anna-**ZUGELJ**-NI-blok",
  "m19-19.-April-Heinrich-[Telesnik~]-42-l-Gradac-1-×-Maria-[Horosec~Horvat]-22-l-Gradac-51-zettel-Vinica-15.-April-[~]-NI-blok",
  "m20-3.-Mai-Joseph-[Perdese~Gerdesić]-34-l-[Črnomelj~Cerhovice]-5-×-Maria-MIHELČIČ-24-l-[Črnomelj-24~Cerhovce-35]-NI-blok",
  "m21-3.-Mai-Franz-Sopčič-32-l-Rtiče-5-×-[Katharina~Barbara]-POŽEG-24-l-[Podljune~Dobrinovo]-14-zettel-[Primostek~Adlešiči]-25.-Apr-NI-blok",
  "m22-17.-Mai-Joseph-HRIŽAN-Weber-**63-l**-[Pribež-P-forenzika!]-×-Anna-HLEBEC-48-l-[Temelj~Kemel]-11-(+2.-vrstica-'[Griboie~Griblje?]-№25'-[~X-OPEN!])-zettel-'Griblje-4.-Mai'-[~]-NI-blok",
  "m23-17.-Mai-Marko-ČERNIČ-22-l-MLADOLETNIK-[~]-[Ceroviše~]-22-×-Maria-[Butkovec~Hrušič]-28-l-[Ceroviše~]-11-zettel-Adlešiči-15.-Mai-NI-blok",
  "m24-14.-Juni-Georg-GRABRIJAN-45-l-Ceroviše-25-×-Apollonia-[Zimrec~]-[44~49]-l-Ceroviše-1-'oba-vdova/vdovec?'-[~]-NI-blok",
  "m26-5.-Aug-Johann-HROVALJ-[~Hrauj!]-28-l-Mlake-10-×-Maria-[Witwa~geb.]-HAMBIČ-[~24~26]-l-[Boginjevas~Boginove]-14-starši-ž.-†Georg-Hrovalj-×-Anna-Jaklič-prečrtan-prvotni-datum!-NI-blok (HROVALJ-×2-kand.-z-m7!)",
  "m27-5.-Aug-Jacob-KRIŽE-37-l-Gradac-1-×-Helena-FERWIGA-33-l-WITWA-Gradac-16-podpis-'[Justinius?]-HEGRIČ' [~X-OPEN]-zettel-Gradac-25.-Juni-NI-blok",
  "m28-28.-Aug-POPPRAVEK-rjavo-'23.'-Josef-BAJUK-25-l-Primostek-[12~16]-×-[Katharina-Angelj-batch-konflacija~Maria-Pavč-Keržan-Toma-P249]-[Dobraviče~Dobravlje]-24-l-NI-blok",
  "TAIL-1873-s2-kontekst-NI-bloki-pošteno (v-04455!): m18-11.-Juni-1873-Mathias-Gahofčič-[~Jahnssepić!]-GRIBLJE-13-42-l-×-Maria-HRIŽAN-GRIBLJE-[62~66]-32-l-POLNI-DVOJNI-KANDIDAT-1873!-+ m19-23.-Sept-Josef-[Gloser~]-Klagenfurt-34-l-×-Maria-[Ema-Augustina-Homolsch~]-19-l-Gradac-1-podpis-'Dames-FERCHER'!-+ m20-5.-Dez-Johann-MILEK-34-l-GRIBLJE-[22~26]-×-Maria-POZDIRC/[~PEGDIRC]-26-l-GRIBLJE-[50~51]-POLNI-DVOJNI-★-PEZDIRC!-+ m21-26.-Dez-Mathias-Gahofčič-32-l-Certovica-12-×-Maria-Gahofčič-22-l-Certovica-10",
] as const;

/** Vse-nove-1874-meritve-v-obliki-za-QA (skupaj-04455: 254→265 · vitals: 1997→2008 · sidra: 247→258-1874:11! · dobe: 221→232-62-pred-linijskih!). */
export const MARRIAGE_1874_KORPUS = {
  skupaj04455: 265,
  skupajVitals: 2008,
  sidra: 258,
  dobe: 232,
} as const;
'''
p = 'src/data/atlas/parish-marriage-early.ts'
src = open(p, encoding='utf-8').read()
assert 'MARRIAGE_1874_BLOCKS' not in src, 'že pripeto!'
open(p, 'a', encoding='utf-8').write(add)
print('MARRIAGE_1874_* pripeto:', len(add))
