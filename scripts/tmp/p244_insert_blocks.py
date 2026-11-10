#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P244 — vstavi 9 GRIBLJE-blokov leta 1879 (poročna PREDZGOVINA 04455) v
src/data/atlas/parish.ts — za P243-h53-1880-blokom, pred 1887-P116-material."""
import io, sys

PATH = "src/data/atlas/parish.ts"
src = io.open(PATH, encoding="utf-8").read()

BLOKI = r'''  // ——— P244: POROČNA PREDZGOVINA 04455, leto 1879 = 5/13 — (s27–s35; md5-9/9-+ VLM-pass-1-×8 + pass-2-×18-kropov + pass-4-ultra-zoom-4×!); ★★★ RESTART-1879 = s27-top (VELIKA-glava-'1879'-na-ZAČETKU-leve-polovice-PRED-vrstico-zap.-št.-1!-vpis-1 = 29. Jänner[~März-DUEL-2-branja!]-Georg-Klepec-[~Klejec/Klobučar/Pegdirc-TRIPLE-DUEL!]-½-Güblar-h16-[~DUEL-Otok-1!] ×-Marie-Jurejevič-h10-[~!] — cf.-P241-VELIKA-GLAVA-4.-VARIANTA!) + ★★★★★ GLAVA-PONOVLJENA-NA-VSAKEM-RAZPRTEM-LISTU (s27–s34-VSE-velika-glava-'1879'!-mrliški-vzorec-mej-60.–74.-POTRDILO-čez-knjige!-NOVA-8.-MEJNA-VARIANTA!) · MEJA-1878/79 = s26→s27 (tail-1878-Georg-Krugel-[~Krigel!]-½-Grubl-s26-dno!-[X-OPEN-opomba-'dd.-12-Jänner-879'-priča!]) · MEJA-1879/80 = s35-mid (P243-1:1!-vpisi-31–33-tail!) → 33-VPISOV-BREZ-PRESKOKOV (s27-1–2 · s28-3–8 · s29-9–11 · s30-12–14 · s31-15–18 · s32-19–21 · s33-22–25 · s34-26–30 · s35-top-31–33!) — 9-GRIBLJE-blokov (h16-×2-BLOKA-V-1-LETU-2.×-linije-cf.-P242-h27!-+ h63-KRIŽAN-2.-leto!-+ PEZDIRC-×2-ženinov-+ -priča!-+ h50-PT-luknja-hiša-1.-poročni-dokaz!) + ★★★★★ FOLIACIJA-'Pag-=-sken−1'-4/4-1879! (s27-'Pag. 26'-1:1 + s30-'Pag. 29'-1:1 + s34-'Pag. 33'-1:1 + s35-'Pag. 34'-1:1!) → **P243-s38-'Pag. 34.'-X-OPEN-DUEL-REŠEN: pravilo-Pag==sken−1-OSTAJA (s38-branje-'34'-= MISREAD-'37'-0-vs-7-Kurrent-cf.-P162b!)** + ★★★ DOVGAN-continuum-SE-PODALJŠUJE-NA-7-LET (s35-tail-D-podpis-'Copulatus-sum...Dopgan'-1879!-+ v16-'Dovgan[~]' — 1879–1885!) + ★★★ MILEK-križ-kandidat-izven-korpusa (s35-tail-D-starš-'½-Gübl.-Mileh'-[~MILEK!]-cf.-P240-Milleh-+ P239-v18-MILEK!-×237→×238-[~]-iskreno-odprto!) + GRIBLJAN-IZVOR-cf. (s35-tail-v34-restart-1880-'ž.-Griblan'-P243!) + v5-vdova-Schilar-[~ŠILAR!] + v16-priča-'Pezdire'-[~PEZDIRC!] + Gaveldzettel-cf.-v21-D-'Gesuchs-1879-...der-Gemein[de]'-[~X-OPEN] ———
  {
    houseNo: "16",
    bookSignature: "04455",
    year: 1879,
    scan: 27,
    page: 26,
    whatSi: "poroka 29. Jänner 1879 [~März-DUEL-2-branja-'29.-Jänner'-vs-'29.-März'!-pass-1+2+3-za-Jänner!] (vpis 1 = RESTART, s27 — velika-glava-'1879'-pred-vrstico!) — ženin Georg Klepec [~Klejec/Klobučar/Pegdirc-TRIPLE-DUEL-4-branja!-pass-2-'Klepec'-+ pass-4-'Klejec[~Klobučar/Klepec]'-+ pass-1-'Helepec[~Helepec/Pezdirc]'-+ pass-3-'Pegdirc[~Pezdirc]'!], 21 let, ledig, ½-Güblar [~½-Gütl-Griblje!], GRIBLJE 16 [~DUEL-Otok-1-1-branje!] × nevesta Marie Jurejevič, 20 let, ledig, ½-Güblar [~], GRIBLJE 10 [~3-branja-konvergentno-'10. 20. 1.'!-pass-3-Krasinec[~]-1-branje!]; starši + priče: Georg-Stepper[~]/Klepec-oče? × Maria-geb.-Jurejevič-Jablnik[~] + Anne-geb.-Justin[~]-Mihor[?] + Anton-Schweiger[~] + Jurejevič-Jaka[~]-½-Gübl.-Gst.-Bes.-priča!; duhovnik: [~cf.-opomba-'Anton-Franz-von-Dovgan-Dechant-gest.-23.-März-1878'-Z-7307-+-'Gemäß-dießfalls-Anordnung-des-HH-Dechant-von-Admont-vom-9.-Jänner-1879-der-Civil-Beizag-präsent'-MODRI-pripis-1.×-v-predzgovorini!-X-OPEN-kaj-točno!]; + ★ 1.-VPIS-1879-RESTART + h16-1.-poročni-dokaz-v-predzgodovini (2.-blok-h16-v-1879-cf.-v25!) + Klepec-priimek-cf.-P94-h22-Nikolaj-MILEK-×-Marija-KLEPEC-1899! + CIVIL-BEIZAG-margine-NOV-element",
    whatEn: "marriage Jan 29, 1879 [~März-THE-DUEL-2-readings!] (entry 1 = RESTART, s27) — groom Georg Klepec [~Klejec/Klobučar/Pegdirc-TRIPLE-DUEL-4-readings!], 21 y., ledig, ½-Güblar [~½-Gütl-Griblje!], GRIBLJE 16 [~DUEL-Otok-1!] × bride Marie Jurejevič, 20 y., GRIBLJE 10 [~3-readings!]; parents + witnesses incl. Jurejevič-Jaka-[~]-½-Gübl.-priča!; priest: [~cf.-margin-note-'Civil-Beizag-präsent'-9.-Jan-1879-Dechant-opomba-NEW-element!]; + the-1st-1879-RESTART-entry + h16-1st-marriage-proof-in-the-prehistory (2nd-h16-block-in-1879-cf.-v25!) + Klepec-cf.-P94-h22-MILEK-×-KLEPEC-1899!",
    status: "DOCUMENTED" as const,
  },
  {
    houseNo: "50",
    bookSignature: "04455",
    year: 1879,
    scan: 28,
    page: 27,
    whatSi: "poroka 5. Februar 1879 (vpis 5, s28) — ženin Mathias Pezdirc [pass-3-'Griblje-50-Mathias-Pezdirc-½-Gütl-mann-1.-26.-1.'-1:1-CLEARED!], 26 let, ledig, ½-Gütl-mann, GRIBLJE 50 × nevesta Maria Škuncelj [~pass-1-'Škuncelj'-2×-1:1!], 18 let, GRIBLJE 44 [~1-1/2-branja!]; starši: Danilo[?] Pezdirc, ½-Gübl-Schweiger[~] × Anna-geb.-[~] + Mathias-Škuncelj × Agnes-Klobučar[~Klobasar-DUEL!]; + ★★★ h50 = 1.-POROČNI-DOKAZ-v-predzgodovini (PT-luknja-hiša-P191-dokazana-mrliško!-poročna-predzgodovina-zdaj-tudi-h50!) + ★ PEZDIRC-ŽENIN = continuum-×131→04455-v-7.-letu-predzgodovine (1879!) + Klobučar-matere-nit-cf.-P242-v4-Katharina-Klobučar! + v3-Wingler-Cerknobl-vojak-v-vrstici-3-razrešen (NE-Griblje!)",
    whatEn: "marriage Feb 5, 1879 (entry 5, s28) — groom Mathias Pezdirc [pass-3-1:1-CLEARED!], 26 y., ½-Gütl-mann, GRIBLJE 50 × bride Maria Škuncelj [~1:1!], 18 y., GRIBLJE 44 [~]; parents: Danilo[?]-Pezdirc × Anna-geb.-[~] + Mathias-Škuncelj × Agnes-Klobučar[~DUEL!]; + ★★★ h50 = the-1st-MARRIAGE-PROOF-in-the-prehistory (the-PT-hole-house-P191!) + ★ PEZDIRC-GROOM = continuum-×131→04455-in-the-7th-prehistory-year!",
    status: "DOCUMENTED" as const,
  },
  {
    houseNo: "61",
    bookSignature: "04455",
    year: 1879,
    scan: 29,
    page: 28,
    whatSi: "poroka 12. Februar 1879 [pass-4-'1879.-Febr.-12.'-1:1!] (vpis 9, s29) — ženin Georg Tomc [~Tomic-DUEL-1-branje!], ½-Griblm [~½-Gütl-Griblje!], GRIBLJE 61 [~pass-2+4-'1,61'-konvergentno!] × nevesta Barbara geb. Tomc, verw. Schilar [~ŠILAR-DUEL-vdova!-cf.-P238-h34-SILAH-+ P242-v23-Šilar!], GRIBLJE 25 [~]; + ★★★ h61-1.-poročni-dokaz-v-predzgodovini + ŠILAR-nit (vdova-verw.-Schilar!-cf.-mrliška-TUBERCULOSE-Köhler-Güblanns?) + TOMC-×2-v-1879 (v9-Georg + v20-Martin + v25-Matthius = TRIPLET-DRUŽINA-omenja!-cf.-P94-P195-Tominc!)",
    whatEn: "marriage Feb 12, 1879 [pass-4-1:1!] (entry 9, s29) — groom Georg Tomc [~], ½-Griblm[~], GRIBLJE 61 [~] × bride Barbara geb. Tomc, verw. Schilar [~ŠILAR-the-widow!], GRIBLJE 25 [~]; + h61-1st-marriage-proof-in-the-prehistory + the-ŠILAR-thread + TOMC-×3-in-1879 (TRIPLET!)",
    status: "DOCUMENTED" as const,
  },
  {
    houseNo: "21",
    bookSignature: "04455",
    year: 1879,
    scan: 30,
    page: 29,
    whatSi: "poroka 12. Feber 1879 [pass-3-'1879.-Feber-12.'-1:1!] (vpis 12, s30) — ženin Johann Pozèh [~Požeh-1:1!], 24 let, ledig, ½-Gültner [~Hüsn-garble], GRIBLJE 21 (ultra-zoom-1:1!) × nevesta Maria Brinc [~Brüne/Princ-DUEL-cf.-P243-v4-Mathias-BRINE-h24!], GRIBLJE 24; starši: Johann-Požeh-ADB-¼-Hf.[~] × Maria-Dragos[~DRAGOŠ!] + Mathias-Princ[~]-Bruncar[~] ¼-Hf. × Maria-Verbič[~]; + ★★★ h24-2.-leto-predzgovorine-ZAPORED (1879-mati-nevesta-→-1880-ženin-Mathias-BRINE-P243-v4!) + BRINC/BRINEC-MREŽA-5.-leto + DRAGOŠ-nit (mati-Maria-Dragos!) + h21-cf.-P151-1922-h21-Požek!",
    whatEn: "marriage Feb 12, 1879 [pass-3-1:1!] (entry 12, s30) — groom Johann Pozèh [~Požeh!], 24 y., ½-Gültner[~], GRIBLJE 21 (ultra-zoom-1:1!) × bride Maria Brinc [~Brüne/Princ-DUEL!], GRIBLJE 24; parents incl. Maria-Dragos[~DRAGOŠ!]; + ★★★ h24-2nd-consecutive-prehistory-year (1879-bride-→-1880-groom-BRINE!) + BRINC-5th-year + DRAGOŠ-thread!",
    status: "DOCUMENTED" as const,
  },
  {
    houseNo: "32 [~]",
    bookSignature: "04455",
    year: 1879,
    scan: 31,
    page: 30,
    whatSi: "poroka 19. Februar 1879 [~datum-DUEL-3-poroke-19.[?]-X-OPEN-isti-dan-kandidat-cf.-P240-v5+v6!] (vpis 16, s31) — ženin Matthias Vijanec [~Vipovec-DUEL!-Ammanhof[?]-kraj-izven-korpusa!], 28 let [~], ledig × nevesta Anne Sušarič [~Gustaria-garble-1-branje!], 21 let, GRIBLJE 32 [~'Grilogz/Griloz-Je.-32'-2-branja-konvergentno!-X-OPEN]; priče: Johann-Vijanec-+ Michael- + Ann.-Broda[~BRODARIČ!]-+ Ann.-Mre.[~] + Nicolaus-[~Galovec?]; duhovnik: Franc-[~Pasthic/Dovgan-DUEL!]; + ★ nevesta-GRIBLJE-32-[~2-branja!]-h32-2.-poročni-dokaz (cf.-P238-v5-Barbara-Straus-h32-1885!) + ★ priča-'Pezdire[~PEZDIRC!]'-v-pričah + 'Ann.-Broda'-cf.-BRODARIČ-botra-nit!",
    whatEn: "marriage Feb 19, 1879 [~date-DUEL-3-marriages-19.[?]-X-OPEN-same-day-candidate!] (entry 16, s31) — groom Matthias Vijanec [~Vipovec-DUEL!-Ammanhof-out-of-corpus!], 28 y.[~] × bride Anne Sušarič [~Gustaria-garble!], 21 y., GRIBLJE 32 [~2-readings-X-OPEN]; witnesses incl. Ann.-Broda[~BRODARIČ!]; priest Franc-[~Pasthic/Dovgan-DUEL!]; + ★ the-bride-GRIBLJE-32-[~]-h32-2nd-proof (cf.-P238-1885!) + ★ the-witness-'Pezdire[~PEZDIRC!]'",
    status: "DOCUMENTED" as const,
  },
  {
    houseNo: "13 [~]",
    bookSignature: "04455",
    year: 1879,
    scan: 32,
    page: 31,
    whatSi: "poroka 19.[~Feber?] 1879 [~datum-2-branja-'bruar-1879'-X-OPEN!] (vpis 20, s32) — ženin Martin Tomc [~Tome-1-branje!], 24 let, ledig, ½-Griblno [~½-Gütl-Griblje!], GRIBLJE 13 [~DUEL-16-pass-2-'Grlivo-13'-vs-pass-1-'Grimo[~]-sklep[~]'!-X-OPEN] × nevesta Maria Hugelji [~Kugelj-TRIPLE-DUEL-IME: Maria-pass-1+4-vs-Engel-pass-2-vs-Anna-glava-pass-4!], 16 let, 'Privo-glavre-30' [~Brivo-glavice-30-NE-Griblje-bivališče!-cf.-GRIBLJAN-IZVOR-konvencija!]; + ★ h13-2.-poročni-dokaz-v-predzgodovini (cf.-P240-v5-RADOVIČ-h13-1883-+ P242-v22-h13!) + TOMC-×3-1879-TRIPLET + nevesta-16-let-mladoletnica-cf.-Väterliche-Einwilligung-P243-v20!",
    whatEn: "marriage 19.[~Feb?] 1879 (entry 20, s32) — groom Martin Tomc [~], 24 y., ½-Griblno[~], GRIBLJE 13 [~DUEL-16-X-OPEN] × bride Maria Hugelji [~Kugelj-TRIPLE-DUEL-NAME: Maria-vs-Engel-vs-Anna!], 16 y., 'Privo-glavre-30' [~NOT-Griblje-residence!]; + h13-2nd-proof (cf.-P240-+P242!) + TOMC-×3-TRIPLET + the-bride-16-y-underage!",
    status: "DOCUMENTED" as const,
  },
  {
    houseNo: "42",
    bookSignature: "04455",
    year: 1879,
    scan: 32,
    page: 31,
    whatSi: "poroka 19.[~Feber?] 1879 (vpis 21, s32 — ultra-zoom-pass-2-1:1-CLEARED!) — ženin Georg Pegdirec [~Pezdirc-DUEL-grafija!], 34 let, ledig, ½-Güblen [~], GRIBLJE 42 (1:1!) × nevesta Dorothea Hrizan [~Križan-grafija-2-branja!], 22 let, ledig [~bestellen-garble!], GRIBLJE 63 (1:1!); starši: Georg-Pegdirec-½-Gübl. × Kathar.-[~]-Pegdirec-geb.-Kurosi[~] + Johan[~]-Križan-½-Gübl. × Maria-Križan-geb.-Starasi[~Simec-DUEL!]; priče: Anton-Lince[~]-Thure[~]; margine: 'Gesuchs-1879-...der-Gemein[de]'-[~GAVELDZETTEL-cf.-X-OPEN!]; + ★★★ h63-KRIŽAN-continuum-2.-LETO-ZAPORED (1879-nevesta-→-1880-ženin-Križan-Miklavčič-P243-v14!-NIT-5-LET-z-mrliško-1884-P239!) + ★★★ PEZDIRC-ženin = continuum-v-7.-letu (×2-v-1879-z-v5!) + h42-cf.-P242-v14-ženi-n-h42-1881!",
    whatEn: "marriage 19.[~Feb?] 1879 (entry 21, s32 — ultra-zoom-1:1-CLEARED!) — groom Georg Pegdirec [~Pezdirc-DUEL!], 34 y., ½-Güblen[~], GRIBLJE 42 (1:1!) × bride Dorothea Hrizan [~Križan!], 22 y., GRIBLJE 63 (1:1!); parents + witnesses Anton-Lince[~]; margine-'Gesuchs-1879-[~GAVELDZETTEL-cf.-X-OPEN!]'; + ★★★ h63-KRIŽAN-continuum-2nd-CONSECUTIVE-year (1879-bride-→-1880-groom!-NIT-5-YEARS!) + ★★★ PEZDIRC-groom-×2-in-1879!",
    status: "DOCUMENTED" as const,
  },
  {
    houseNo: "17 [~]",
    bookSignature: "04455",
    year: 1879,
    scan: 33,
    page: 32,
    whatSi: "poroka 24. Februar 1879 [~datum-2-branja-'23.'-vs-'24.'-X-OPEN!] (vpis 24, s33) — ženin Johann Kralj, 34 let, ledig, ½-Gütl-besitzer, GRIBLJE 17 [~DUEL-24-pass-1-'Griblje-17'-vs-pass-2-b-'Griblje-dd.-24'-X-OPEN!] × nevesta Anna Janoprič [~Janovič-garble?], 24 let, Crhlivec[?]-nec. [~izven-korpusa!]; starši: Johann-Marg.-Kralj[~] × Johanna-geb.-Juraschek[~] + Georg-Kathoner[~] × Maria-geb.-Copiř-geb.-Carevič[~]; + ★ h17-2.-poročni-dokaz-v-predzgovorini-cf.-P151-1922-Jurij-KRALJ-h17 (3.-dokaz!-ISTO-IME-DRUŽINA-cf.-korpus-aritmetika!) + Kralj-h17-nit (1892-№10-Johann!)",
    whatEn: "marriage Feb 24, 1879 [~date-2-readings-X-OPEN!] (entry 24, s33) — groom Johann Kralj, 34 y., ½-Gütl-besitzer, GRIBLJE 17 [~DUEL-24-X-OPEN!] × bride Anna Janoprič [~], 24 y., Crhlivec[?]; + h17-2nd-proof-in-the-prehistory-cf.-P151-1922-Jurij-KRALJ-h17 (3rd!-THE-SAME-FAMILY!)",
    status: "DOCUMENTED" as const,
  },
  {
    houseNo: "16",
    bookSignature: "04455",
    year: 1879,
    scan: 33,
    page: 32,
    whatSi: "poroka 4. Mai 1879 (vpis 25, s33) — ženin Matthius Tomc [~], 24 let, ledig, ½-Gütl-bes., GRIBLJE 16 [~'Grimo/Griblnag-16'-2-branja-konvergentno-'16'!-X-OPEN-STEM-garble!] × nevesta Maria Mihelec [~Mihelič-DUEL!], 19 let, ledig, ½-Gütl-ing. [~], Semič 3 [izven-korpusa!]; starši: Georg-Tomc-¼-Gübl. × Cathar.-[~]-Jure[~] + Martin-Mihelec × Maria-geb.-[~Stambič?]; priče: Josef-Lužinam[~]-Semic-dd.-30[~]; + ★★★ h16-×2-BLOKA-V-1879 (v1-ženin-Klepec + v25-ženin-Tomc!-2.×-linije-cf.-P242-h27-×2-bloka-v-1881!) + TOMC-×3-TRIPLET-v-1-LETU (v9 + v20 + v25 — 3-brata?-nit!) + Mihelec/Mihelič-DUEL-cf.-MIHELČ-MILIČ-križ!",
    whatEn: "marriage May 4, 1879 (entry 25, s33) — groom Matthius Tomc [~], 24 y., ½-Gütl-bes., GRIBLJE 16 [~2-readings-X-OPEN!] × bride Maria Mihelec [~Mihelič-DUEL!], 19 y., Semič-3 [out-of-corpus!]; witnesses Josef-Lužinam[~]; + ★★★ h16-×2-BLOCKS-in-1879 (2nd-of-the-line-cf.-P242-h27!) + TOMC-×3-TRIPLET-in-1-YEAR!",
    status: "DOCUMENTED" as const,
  },
'''

ANCHOR = '''  {
    houseNo: "71",
    bookSignature: "04455",
    year: 1887,'''

assert ANCHOR in src, "anchor (h71-1887) not found"
src = src.replace(ANCHOR, BLOKI + ANCHOR, 1)
io.open(PATH, "w", encoding="utf-8").write(src)
print("P244: 9 blokov 1879 vstavljenih ✓")
