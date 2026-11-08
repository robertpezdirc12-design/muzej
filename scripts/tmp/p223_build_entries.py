#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P223 — agregacija 99-vpisov leta 1883 (krstna PREDZGODOVINA 04104, 3/15!).
MEJA-1882/83 = s161 (TAIL-1882-z104–z106-Dez-31×3 + z105/z106 = DVOJČKI-GRIBLJE-h68-ZWILLINGE!
  + 'Initium[~Inicip]-annos-Domini' + VSOTNA-razpeta-'1 8 8 3.' + RESTART-z1-NA-DAN-4.-1.-Gradac!)
  = 62.-POTRDITEV-invariante (61.-P222!). MEJA-1883/84 = s173 (P222!).
Ordinalna linija: z1–z99 (99-DISTINCT! vrstna-aritmetika 6+9+8+8+9+9+9+8+8+8+8+8+1 = 99
  = P222-LEAD-'1883-=-99-vpisov'-1:1-INVARIANTA!). ČISTA — brez-pisarjevih-anomalij!
★★★ MESECI: carry-over-vzorec (labela-samo-na-prvi-vrstici-bloka!) + MÄRZ-LABEL-MISREAD-KOREKCIJA
  (z24-page-'Mai'-→-hi-'März'! — sicer-April-sandwich-anomalija!) → J2+F1+M3+A1+M1+J2+J2+S1+O2+N1+D3!
★★★ 19-GRIBLJE / 18-hiš (h25-×2: z32+z88!) + z99-TAIL-IZLOČEN (vas-hi-'Obrijuh'-hisna-17!)
★★★ DVOJNI-FOLIACIJSKI-SERIJI (NOVO-ODKRITJE!): gola-svinčna-'pag-=-sken−5' (1883-okno: s165='160'/
  s169='164'/s173='168'-vizualno! + s161='155[~156?]'-5/6-garble!) VS-'Pag.'-natisnjena-serija-'sken+13'
  (1884-okno: s177='Pag.190'/s181='Pag.194'/s185='Pag.198'-vizualno-re-potrjeno!) — menjava-tiskane-forme
  (stara-forma-brez-'Post-Nr.'-do-s173! nova-forma-s-'Post-Nr.'-od-s174/175!) + P222-'s173=186'-KOREKCIJA
  (gola-'168'-6/8-transpozicija-misread-X-open!).
Izhod: /tmp/p223/entries_1883.json"""
import json

TMP = "/tmp/p223"

GRIBLJE = [
 {"z":"z5","sken":161,"pag":"156 [~155-DUEL-5/6-garble!]","mesec":"Jänner","rojen":"22","krsten":"23","vas":"Griblje","hisna":"28",
  "otrok":"Katharina","spol":"ženski",
  "ocec":"Georg Požeh [~Požek-garble!], z-Güblari[?]",
  "matec":"Margaret[~Margaretha!] roj. Mihelovic[~Hublvar-garble-DUEL!]",
  "botra":"Anton Riere[?] + Margareb Hublvar[~]",
  "_opomba":"★★★ MESEC-KOREKCIJA (page-'Feber'-SKLEPANJE → mesecni-stolpec-PRAZEN-carry-over-'Jänner'-iz-z1! — hi-visual-'22./23.') + ★★★ pripis-MMK-'umrla-dne-18.12.1962-v-G[?]' + garble-'gübtjch-Faune-Tersicur[?]'-X-open + ★ mesecni-stolpec-RAZKRIT: z1–z6-VSI-JÄNNER (labela-samo-z1!)"},
 {"z":"z7","sken":162,"pag":"157","mesec":"Jänner","rojen":"26","krsten":"26","vas":"Griblje","hisna":"20",
  "otrok":"Barbara","spol":"ženski",
  "ocec":"Peter Perdiče [~Perdicé-PEZDIRC-grafija!], Bauer",
  "matec":"Katharina Doblš[~Dolšič?]",
  "botra":"Mathias Mihl/Mikl[?] + Bara BRODARIČ[~]",
  "_opomba":"★★★ PEZDIRC-grafija-oče (Perdiče!) + BRODARIČ-botra-nit + Jänner-26/26-potrditev (chrono-z6-Jän-26→z7-Jän-26! — page-'Feber'-carry-over-sklepanje-ZAVRNJENO!)"},
 {"z":"z17","sken":163,"pag":"158","mesec":"Februar","rojen":"26","krsten":"26","vas":"Griblje","hisna":"7",
  "otrok":"Josef","spol":"moški",
  "ocec":"Andreas Totter, Bauer",
  "matec":"Margaretha STRUCELJ [~]",
  "botra":"Georg SIMEC + Maria Strucelj-Laufer[?]",
  "_opomba":"★★★ STRUCELJ-×2-nit (mati + botra!) + SIMEC-botra-nit (P221-mreža!) + pripis-svinčnik-'≈[4/9]/10-[1853/1858]-X-open-garble' + hi-pripis-'Trink/Jancar[?]-svinčnik'"},
 {"z":"z22","sken":163,"pag":"158","mesec":"März","rojen":"2","krsten":"2","vas":"Griblje","hisna":"39",
  "otrok":"Anna","spol":"ženski",
  "ocec":"Nikolaus SIMEC [~'Nikoland-Simec-Lunn'-garble!]",
  "matec":"Katharina roj. Jakopič [~]",
  "botra":"Peter Vlobnčar/PLEBNIČAR[?] + Barbara BRODARIČ[~]",
  "_opomba":"★★★ SIMEC-oče-nit (P221-SIMIC-×2!) + BRODARIČ-botra-nit (2/2-leta!) + ★★★ pripis-MMK-'umrla-6.1.1940-[v-Hrhljan?]-90-let'-X-open + duhovnik-'Franz-Dorgan[?]'-podpis"},
 {"z":"z25","sken":164,"pag":"159","mesec":"März","rojen":"17","krsten":"17","vas":"Griblje","hisna":"8",
  "otrok":"Margaretha [~Margaritha!]","spol":"ženski",
  "ocec":"Johann Galkovič [~Galtovic-Palkovič-G/P-garble-DUEL!], Lunn[?]",
  "matec":"Maria MERK [~]",
  "botra":"Marko KLOBUČAR + Ana DRAGOŠ [~Dragos!]",
  "_opomba":"★★★ MESEC-KOREKCIJA (z24-labela-'März'-hi-VIZUALNO! — page-'Mai'-MISREAD → April-sandwich-anomalija-RAZREŠENA!) + ★★★ DRAGOŠ-botra-nit (P193/P220 + z94-mati-1883!) + KLOBUČAR-botra-nit"},
 {"z":"z28","sken":164,"pag":"159","mesec":"März","rojen":"21","krsten":"21","vas":"Griblje","hisna":"35 [~]",
  "otrok":"Peter","spol":"moški",
  "ocec":"Peter Ostirc[?] [~Stepec-garble!], Gärtner[~]",
  "matec":"Marija Zupanič [~]",
  "botra":"Mare[~Maria!] BRODARIČ + Alois Haucly[?]",
  "_opomba":"★★★ MESEC-KOREKCIJA (März-21! — page-'Mai') + BRODARIČ-botra-nit (3/3!) + hisna-'35'-X-open (odsekani-3/5-zmeda!) + ocec-garble (Ostirc/Stepec!)"},
 {"z":"z32","sken":165,"pag":"160","mesec":"April","rojen":"11","krsten":"11","vas":"Griblje","hisna":"25",
  "otrok":"Maria","spol":"ženski",
  "ocec":"Miha ZUPANIČ, Bauer",
  "matec":"Catharina Perdče [~PEZDIRC-grafija!]",
  "botra":"Janez Zupanič + Cath. Cajner[?]",
  "_opomba":"★★★ PEZDIRC-grafija-mati-nit (Perdče!) + ZUPANIČ-oče+botra + ★★★ pripis-MMK-'umrla-dne-18.[?].1957'-hi-KOREKCIJA (page-'poročena-1957'-MISREAD!)"},
 {"z":"z43","sken":166,"pag":"161","mesec":"Mai","rojen":"6","krsten":"7","vas":"Griblje","hisna":"17 [hi2-VIZUALNO-'17.'-ČISTO!]",
  "otrok":"Georg","spol":"moški",
  "ocec":"Georgius Pazek [~Pazek?], Grentner[~Gärtner-garble!]",
  "matec":"Katharina roj. Hoizan[~]",
  "botra":"Georgius SIMEC[~] + Barbara Kure[~]",
  "_opomba":"★★★ hiša-DUEL-REŠEN (17! — page+'hi2-vizualno' 2:1 vs-'42'-PRELIV-iz-pripisa-'1942'-ZAVRNJEN!) + SIMEC-botra-nit (2/2-leta!) + ★★★ pripisi-MMK-'poročen-3/2.1919' + 'H-30.8.1942' ('42'-preliv-vzrok-'42'-hiša-misread!)"},
 {"z":"z52","sken":167,"pag":"162","mesec":"Juni","rojen":"13","krsten":"13","vas":"Griblje","hisna":"55 [~65-DUEL-5/6-zmeda!]",
  "otrok":"Anton","spol":"moški",
  "ocec":"Michael Peršinc/Persinc [~PEZDIRC-grafija!], Gärtner",
  "matec":"Maria Perdine/Verdine [~PEZDIRC-grafija!]",
  "botra":"Martin Kraus[~] + Katarina Krilan[~], Gärtner",
  "_opomba":"★★★ PEZDIRC-grafija-oče+mati-DVOJNI-nit! (Peršinc + Perdine!) + hisna-'55-vs-65'-DUEL (5/6-zmeda-X-open!) + pripis-'umrl-2.9.1965-[v-Krasinem?]-X-open' (z52-z53-pripis-dodelitev-X-open!)"},
 {"z":"z58","sken":167,"pag":"162","mesec":"Juli","rojen":"7","krsten":"7","vas":"Griblje","hisna":"19",
  "otrok":"Barbara","spol":"ženski",
  "ocec":"Johann Hriže [~Hruže-Krže-Triže-garble!], Lunn[?]",
  "matec":"Maria Sodec [~]",
  "botra":"Anton Kunc[~] + Ana HLEBEC [~Klebec!]",
  "_opomba":"★★★ HLEBEC/KLEPEC-botra-nit (P219-h2!) + ★★★ pripis-MMK-'umrla-dne-8.10.[1959/1960]-[Kapici/Tampči]-vas-19-32/3'-garble-X-open + JUNI/JULI-blok-boundary (z55/z56-Juni-23/26-carry-over → z57/z58-Juli-5/7!)"},
 {"z":"z59","sken":168,"pag":"163","mesec":"Juli","rojen":"15","krsten":"16","vas":"Griblje","hisna":"24",
  "otrok":"Mathias","spol":"moški",
  "ocec":"Mathias Brinc[~Bovha-DUEL-garble!], ¼ Griblan.",
  "matec":"Barbara roj. Jakopič [~Jablovič-garble!]",
  "botra":"Mathias MIHELČ-MILEK [~] + Maria Mihelč[~]",
  "_opomba":"★★★ MILEK/MIHELČ-botri-nit (P218/P220-h65!) + ★★★ pripis-MMK-'Mrt.-dne-10.7.1985-v-Gribljah-št.-57'-hi-KOREKCIJA (page-'rojen-10.7.1965'-MISREAD!) + 'matični-izpis' + oče-DUEL (Brinc-vs-Bovha-garble!)"},
 {"z":"z61","sken":168,"pag":"163","mesec":"Juli","rojen":"21","krsten":"21","vas":"Griblje","hisna":"90 [2:1-vizualno-'90'-9-zanka+rep-brez-7-prečke!-vs-'70']",
  "otrok":"Maria","spol":"ženski",
  "ocec":"Martin Čapič [~Capio-garble!], Häusler[~Krec-garble!]",
  "matec":"Maria Volar [~Totar-garble!]",
  "botra":"Jakob Totar[~Volar?] + Cath. Požeš[~Cožeš-garble!]",
  "_opomba":"★ hiša-DUEL-REŠEN (90-2:1: page+hi-vizualno vs-'70'-γ/9-zmeda-dokumentirana!) + garble-gostota (Čapič/Volar/Totar/Požeš — honesty!)"},
 {"z":"z73","sken":169,"pag":"164","mesec":"September","rojen":"5","krsten":"5","vas":"Griblje","hisna":"1 [hi-VIZUALNO-'1'-ČISTO!]",
  "otrok":"Barbara","spol":"ženski",
  "ocec":"Miha/Michl LESKO [~], Bauer",
  "matec":"Catharina Kure [~]",
  "botra":"Jure LESKO + Cath. Lesko [botri-LESKO-×2!]",
  "_opomba":"★★★ hiša-'1'-VIZUALNO-POTRJENA (prva-GL-številka-1-1883!) + LESKO-×3-nit (oče+botri-×2!) + mati-Kure-nit (z43-botra-Kure!)"},
 {"z":"z76","sken":170,"pag":"165","mesec":"October","rojen":"7","krsten":"7","vas":"Griblje","hisna":"56 [hi3-VIZUALNO-'56'-ČISTO!-vs-page-'51'-1/6-zmeda!]",
  "otrok":"Rikhardsina [?garble-Richmna/Rihardina/Rikhavzina!]","spol":"ženski",
  "ocec":"Dorher/Baraga[?] — neberljivo-garble-DUEL!",
  "matec":"Barba Šinac[?] / 'Incze'[?]",
  "botra":"Johann Grintsch[?] + Maria Pozdire [~PEZDIRC-grafija-botra!]",
  "_opomba":"★★★ hiša-KOREKCIJA (56! — hi3-vizualno-'56' vs-page-'51[?]' 1/6-zmeda!) + ★★★ ime-otroka-TRI-garble-honesty (Rikhardsina/Richmna/Rihardina!) + oče-garble-DUEL + PEZDIRC-grafija-botra (Pozdire!)"},
 {"z":"z78","sken":170,"pag":"165","mesec":"October","rojen":"13","krsten":"13","vas":"Griblje","hisna":"37 [page+'krop-vizualno'-'37'-γ-forma!-vs-hi2-'sy'-garble!]",
  "otrok":"Matthäus (Matevž)","spol":"moški",
  "ocec":"Johann Maske [?] (Janez)",
  "matec":"Katharina Prupar/Prunar[?]",
  "botra":"Fran Žgel[?] + Maria Rudline[?]",
  "_opomba":"★ hiša-'37'-2:1 (page+krop-vizualno-γ-7! vs-hi2-'sy'-garble-ZAVRNJEN!) + KURRENT-γ-7-DOKUMENTIRANO ('sy'-'37'-paralela-P222-z1-'37'-ZAVRNJENA!)"},
 {"z":"z88","sken":171,"pag":"166","mesec":"November","rojen":"15","krsten":"16","vas":"Griblje","hisna":"25 [hi-VIZUALNO-'25.'-ČISTO!]",
  "otrok":"Katharina","spol":"ženski",
  "ocec":"Matthias Borša[?] [~Borre-P222-lead!], ½ Gütl[?]",
  "matec":"Maria roj. Kovin[?]",
  "botra":"Johann Mihelč + Maria Mihelč [~]",
  "_opomba":"★★★ hiša-'25'-VIZUALNO (hi!) + h25-×2 (2/2 — z32!) + P222-LEAD-POTRJEN (z88-h25-Katharina-Borre!) + MIHELČ-botri-nit (z59!)"},
 {"z":"z94","sken":172,"pag":"167","mesec":"December","rojen":"17","krsten":"17","vas":"Griblje","hisna":"11",
  "otrok":"Nicolaus","spol":"moški",
  "ocec":"Mathias Hugel/Šumec[?] [~Hunic-garble!], ¼ Griblan.",
  "matec":"Katharina roj. DRAGOŠ [~Dragol!]",
  "botra":"Peter Hrobe/Hlebec[?] + Anna Jahofir[?]",
  "_opomba":"★★★ DRAGOŠ-mati-nit (2/2-leta — z25-botra!) + ★★★ pripis-MMK-'Cop.-19/4.1910-vs-Pilteburg[?]' (P222-LEAD-'D.17/9-1910-Pillkburk'-paralela!) + P222-LEAD-POTRJEN (z94-h11-Nikolaus!)"},
 {"z":"z96","sken":172,"pag":"167","mesec":"December","rojen":"25","krsten":"25","vas":"Griblje","hisna":"63 [hi2-VIZUALNO-'63.'-ČISTO!-vs-page-'18'-6/8+3/8-zmeda!]",
  "otrok":"Anna","spol":"ženski",
  "ocec":"Nicolaus Pirzov[?] [~Pirzov-garble!], ¾ Gribl.",
  "matec":"Katharina roj. Peddire [~PEZDIRC!]",
  "botra":"Martha Peddire [~PEZDIRC!] + Barbara Partlnič[?], Stan: Simič[?]",
  "_opomba":"★★★ hiša-DUEL-REŠEN (63! — P222-LEAD-h63 + hi2-vizualno-'63.' 2:1 vs-page-'18[~]' 1/8-zmeda-ZAVRNJENA!) + ★★★ PEZDIRC-mati+botra-DVOJNI-nit (Peddire-×2!) + P222-LEAD-POTRJEN (z96-PEZDIRC-mati!)"},
 {"z":"z97","sken":172,"pag":"167","mesec":"December","rojen":"26","krsten":"27","vas":"Griblje","hisna":"29 [hi2-VIZUALNO-'29'-ČISTO!]",
  "otrok":"Barbara","spol":"ženski",
  "ocec":"Petrus Hulik[?] [~Hulik-garble!], ½ Gribljar",
  "matec":"Anna KRIŽAN [~]",
  "botra":"Jvan/Johann Adamic[?] + Maria KRIŽAN [~], ž.-Gribljar",
  "_opomba":"★★★ KRIŽAN-×2-nit (mati + botra!) + hiša-'29'-VIZUALNO + P222-LEAD-POTRJEN (z97-h29-Barbara!) + latinski-pripis-garble"},
]

ANOMALIJE = [
 {"id":"meja-1882-83-s161",
  "opis":"★★★ MEJA-1882/83 = s161 (62.-POTRDITEV-invariante!): TAIL-1882-z104–z106 (Dezember-31-×3! + z105+z106 = DVOJČKI-GRIBLJE-h68-Mathias+Barbara-'Zwillinge'-bracket! — Ivan-Urek-Lanin-Gärtler + Maria-Požek! — P224-LEAD!) + 'Initium[~Inicip]-annos-Domini'-naslov + VSOTNA-razpeta-'1 8 8 3.'-črez-stolpce + RESTART-z1-NA-DAN-4.-1.-JÄNNER-Gradac (page-'Jänner-4.' + hi!) — 1883 = 99-vpisov (P222-LEAD!)",
  "dokazi":["s161-page-VLM (meja-DA!)","s161_zap_stolpec (104/105/106/PRAZNA/1–6!)","arb_s161_meja-krop (z1-Antonia-Gradac-Jän-4 + pripis-MMK-'umrla-23.10.1947-Ljubljana'!)","s161-mesec-hi (z1-'Jänner-4.'-VIZUALNO!)"]},
 {"id":"mesec-carry-over-vzorec",
  "opis":"★★★ MESEC-CARRY-OVER-VZOREC (NOVO-ODKRITJE-1883!): pisar-piše-MESEČNO-LABELO-SAMO-NA-PRVI-VRSICI-BLOKA — z1-'Jänner' + z2–z6-PRAZNI (page-VLM-'Feber'-SKLEPANJE-NAPAČNO!) — dnevi: 4, 8/9, 8/9, 13/15, 22/23, 26/26 — VSI-JÄNNER! + z49-'Juni' + z55/z56-carry-over + bloki: Jän-z1–z9 (4–31!) + Feb-z10–z19 (1–28!-neprestupno!) + Mär-z20–z30 + Apr-z31–z40 + Mai-z41–z48 + Jun-z49–z56 + Jul-z57–z63 + Aug-z64–z70 + Sep-z71–z74 + Okt-z75–z87 + Nov-z88–z91 + Dez-z92–z99 — POPOLNA-KRONOLOGIJA!",
  "dokazi":["s161-mesec-hi (z1–z6-VIZUALNO: labela-samo-z1!)","s162/s163-page-dnevi (26/26,28,31→Feb-1,7,11,12,13,19,25,26,26,28!)","chrono-aritmetika-12-blokov"]},
 {"id":"marz-label-misread-korekcija",
  "opis":"★★★ MÄRZ-LABEL-MISREAD-KOREKCIJA: z24-labela-page-VLM-'Mai' → hi-VIZUALNO-'März' (M-ä-r-z-z-descender!) — brez-korekcije-bi-bila-NESMOSEL-'April-sandwich' (Mai-17–30→April-8–25→Mai-2–31!) — z-korekcijo: Mär-17–30→April-8–25→Mai-2–31-POPOLNA-KRONOLOGIJA! — z25/z28-GRIBLJE-MÄRZ (ne-Mai!)",
  "dokazi":["z24_s164_label_hi (VIZUALNO-'März'!)","s164-mesec-col (17/17,17/17,19/19,21/21,21/21,24/24,29/30!)","s166_mesec_col ('Mai'-2–31 + 'Juni'-3-VIZUALNO!)","chrono-aritmetika"]},
 {"id":"dvojni-foliacijski-seriji",
  "opis":"★★★ DVOJNI-FOLIACIJSKI-SERIJI (NOVO-ODKRITJE!): (1) GOLA-SVINČNA-SERIJA 'pag-=-sken−5' (1883-okno: s165='160'/s169='164'/s173='168'-VIZUALNO! + s161='155[~156?]'-5/6-garble!) — stara-tiskana-forma-BREZ-'Post-Nr.'-stolpca! (2) 'Pag.'-NATISNJENA-SERIJA 'sken+13' (1884-okno: s177='Pag.-190'/s181='Pag.-194'/s185='Pag.-198'-VIZUALNO-re-potrjeno!) — nova-tiskana-forma-S-'Post-Nr.'-stolpcem! — MENJAVA-FORME-okoli-s174/175 (MEJA-1883/84!) + ★ P222-'s173=186'-KOREKCIJA (gola-'168'-6/8-transpozicija-misread! — P222-Window-claims-s177/s181/s185-OSTAJO-PRAVILNI!)",
  "dokazi":["arb_s165_pag (160!)","arb_s169_pag (164!)","arb_s173_pag + s173_pag_hi (168-golo-svinčno-2×-VIZUALNO!)","arb_s161_pag (155[~156?])","recheck_s177_pag ('Pag.-190'-VIZUALNO!)","recheck_s181_pag ('Pag.-194'-VIZUALNO!)","recheck_s185_pag ('Pag.-198'-VIZUALNO!)"]},
 {"id":"z99-tail-izlocen",
  "opis":"★★★ z99-TAIL-1883-IZLOČEN-iz-GRIBLJE: vas-hi-'Obrijuh.'-hisna-'17.' (P222-'OBržuh/Obrije[?]'-potrjeno-razširjeno!) — NI-Griblje! (lokalna/dialektna-forma-X-open — Obrh/Obrije[?]) — TAIL-1883 = zadnja-vrstica-leta-PRED-VSOTNO/restart-1884 (P222-dokumentirano!)",
  "dokazi":["z99_s173_vas_hi ('Obrijuh.-17.'-VIZUALNO!)","P222-arb_s173_meja-paralela"]},
 {"id":"hisni-dueli-reseni",
  "opis":"HIŠNI-DUELI-REŠENI (5!): z43-'42'-ZAVRNJEN (preliv-iz-pripisa-'1942'! — 17-2:1!) + z59-page-'rojen-1965'-KOREKCIJA ('Mrt.-1985-MMK!') + z61-'70'-ZAVRNJENO (90-2:1-γ/9!) + z76-'51'-KOREKCIJA (56!-1/6-zmeda!) + z78-'sy'-ZAVRNJEN (37-γ-forma!) + z96-'18'-ZAVRNJENA (63!-P222-lead+hi2!) + z32/z88-h25-×2 (18-hiš!)",
  "dokazi":["z43_s166_hisna_hi2","z59_s168_grib (pripis!)","z61_s168_hisna_hi2","z76_s170_hisna_hi3","z78_s170_grib","z96_s172_hisna_hi2"]},
 {"id":"pripisi-kriz-mmk-1883",
  "opis":"★★★ POZNEJŠI-PRIPISI-MMK-ERA (8-GRIBLJE!): z5-'umrla-18.12.1962' + z22-'umrla-6.1.1940-90-let' + z32-'umrla-18.[?].1957'-KOREKCIJA (page-'poročena'-MISREAD!) + z43-'poročen-3/2.1919'+'H-30.8.1942' + z52-'umrl-2.9.1965-[X-open]' + z58-'umrla-8.10.[1959/1960]-[Kapici/Tampči]' + z59-'Mrt.-10.7.1985-v-Gribljah-št.-57'-KOREKCIJA + z94-'Cop.-19/4.1910-vs-Pilteburg[?]'-X-open + (z17-svinčnik-'≈[4/9]/10-[1853/1858]-X-open') — KRIŽ-z-maticnimi-podatki-20.-stoljeta!",
  "dokazi":["z05_s161_grib2","z22_s163_band","z32_s165_grib","z43_s166_hisna_hi2","z52_s167_grib","z58_s167_grib","z59_s168_grib","z94_s172_grip"]},
 {"id":"mreze-1883",
  "opis":"MREŽE-1883: PEZDIRC-grafija-×6 (z7-oče-Perdiče! + z32-mati-Perdče! + z52-oče-Peršinc+mati-Perdine! + z76-botra-Pozdire! + z96-mati-Peddire+botra-Martha-Peddire!) + BRODARIČ-×4 (z7-botra-Bara! + z22-botra-Barbara! + z28-botra-Mare! + z58?) + DRAGOŠ-×2 (z25-botra-Ana! + z94-mati-Katharina!) + SIMEC-×3 (z22-oče-Nikolaus! + z17-botra-Georg! + z43-botra-Georgius!) + KRIŽAN-×2 (z97-mati+botra!) + STRUCELJ-×2 (z17-mati+botra!) + LESKO-×3 (z73-oče+botri-×2!) + MIHELČ-MILEK-×2 (z59-botri! + z88-botri!) + HLEBEC (z58-botra!) + KLOBUČAR (z25-botra!) + ZUPANIČ-×2 (z32-oče+botra! + z28-mati!) + Kure-×2 (z73-mati! + z43-botra!)",
  "dokazi":["vsi-row-krops + hi-zoomi + page-VLM"]},
]

CROSS = [
 {"tip":"meja-1882/83 + meja-1883/84","opis":"s161-RESTART-z1 (62.-POTRDITEV!) + s173-RESTART-1884 (P222-re-križ!) — knjiga-04104-leta-1882–1884-verižno-zaklenjena!","status":"POTRJENO"},
 {"tip":"99-vpisov-invarianta","opis":"vrstna-aritmetika-6(s161)+9(s162)+8(s163)+8(s164)+9(s165)+9(s166)+9(s167)+8(s168)+8(s169)+8(s170)+8(s171)+8(s172)+1(s173-tail) = 99-DISTINCT (z1–z99!) = P222-LEAD-'1883-=-99-vpisov'-1:1!","status":"POTRJENO"},
 {"tip":"dvojcki-griblje-h68-1882","opis":"z105+z106-TAIL-1882-'Zwillinge'-bracket (GRIBLJE-h68-Mathias+Barbara-Dez-31! — Ivan-Urek-Lanin + Maria-Požek!) → P224-LEAD (1882 = 4/15!) — PARALELA-P219-DVOJČKI-SIMIC + P221-DVOJČKI-GRADAC + z2/z3-DVOJČKI-DOBRAVCE-1883!","status":"P224-LEAD"},
 {"tip":"PEZDIRC-grafija-mreza-1883","opis":"×6 (z7-oče + z32-mati + z52-oče+mati + z76-botra + z96-mati+botra!) → P221-×4-1885 + P222-×4-1884-PARALELA — grafija-continuum!","status":"DOKUMENTIRANO"},
 {"tip":"DRAGOŠ-mreza-1883","opis":"z25-botra-'Ana-Dragos' + z94-mati-'Katharina-Dragol' → P193-h3 + P220-z45 + z26-mati-1884!","status":"DOKUMENTIRANO"},
 {"tip":"SIMEC-mreza-1883","opis":"z22-oče-'Nikolaus-Simec' + z17-botra-'Georg-Simec' + z43-botra-'Georgius-Simec' → P221-SIMIC-×2 + z51-mati-SIMEC-1884!","status":"DOKUMENTIRANO"},
 {"tip":"BRODARIČ-mreza-1883","opis":"z7-botra-'Bara' + z22-botra-'Barbara' + z28-botra-'Mare' → P222-×5-1884-mreza!","status":"DOKUMENTIRANO"},
 {"tip":"MILEK-MIHELČ-nit","opis":"z59-botri-'Mathias-Mihelč-Milek' + z88-botri-'Johann+Maria-Mihelč' → P218/P220-h65-MILEK + z105-botra-1884!","status":"DOKUMENTIRANO"},
 {"tip":"KRIŽAN-nit-1883","opis":"z97-mati-'Anna-Križan' + botra-'Maria-Križan' → P222-z59/z84/z105-1884-mreza!","status":"DOKUMENTIRANO"},
 {"tip":"pag-odkritje","opis":"dvojni-seriji → P224-LEAD (1882-okno = gola-serija 'sken−5'-pričakovano!) + P222-GLAVA-korekcijska-opomba (s173='168'-ne-'186')","status":"NOVO-DOKUMENTIRANO"},
]

HONESTY = [
 "z76-ime-otroka-TRI-garble (Rikhardsina/Richmna/Rihardina!) + oče-garble-DUEL (Dorher/Baraga!)",
 "z61-garble-gostota (Čapič/Volar/Totar/Požeš-×4-garbles!)",
 "z28-hisna-'35'-X-open (odsekan-krop!) + oče-garble (Ostirc/Stepec!)",
 "z52-hisna-'55-vs-65'-DUEL-X-open (5/6!) + pripis-dodelitev-z52-z53-X-open",
 "z5-matec-garble-DUEL (Mihelovic/Hublvar!)",
 "z59-oče-DUEL (Brinc-vs-Bovha!)",
 "z17-pripis-garble (≈[4/9]/10-[1853/1858]-X-open!)",
 "z58-pripis-garble ([1959/1960]+[Kapici/Tampči]-X-open!)",
 "z94-oče-garble (Hugel/Šumec/Hunic!)",
 "s161-pag-'155-vs-156'-X-open (5/6-garble!)",
 "z99-'Obrijuh'-vas-X-open (IZLOČEN!)",
 "mesec-carry-over-page-VLM-sklepanja-'Feber'-'Mai'-KOREKCIJE (z5/z7/z25/z28!)",
 "pag-hi-geo-zamiki-pass1 (s161/s163/s169/s171-latest-rows-dokumentirano!)",
 "matec/botra-večkrat-[~]-garble — brez-fabriciranja",
 "z43-'42'-preliv-artefakt-dokumentiran (revizijska-poenostavitev!)",
]

entries = []
for e in GRIBLJE:
    e2 = dict(e)
    entries.append(e2)

stats = {
    "leto": 1883,
    "vpisov_distinct": 99,
    "vrstna_aritmetika": "6(s161)+9(s162)+8(s163)+8(s164)+9(s165)+9(s166)+9(s167)+8(s168)+8(s169)+8(s170)+8(s171)+8(s172)+1(s173-tail) = 99-DISTINCT (z1–z99!)",
    "griblje_vpisov": 19,
    "griblje_his": 18,
    "meseci_griblje": "J2+F1+M3+A1+M1+J2+J2+S1+O2+N1+D3 (z25/z28-März-KOREKCIJA!)",
    "meja_1882_83": "s161 (TAIL-1882-z104–z106 + Initium-annos-Domini + VSOTNA-'1 8 8 3.' + restart-z1-Jän-4-Gradac!)",
    "meja_1883_84": "s173 (P222!)",
    "pag_konvencija": "gola-svinčna-'sken−5' (s165='160'/s169='164'/s173='168'-vizualno! s161='155[~156?]') — VS-'Pag.'-'sken+13'-1884-okno!",
    "bloki_mesecev": "Jän-z1–z9 · Feb-z10–z19 · Mär-z20–z30 · Apr-z31–z40 · Mai-z41–z48 · Jun-z49–z56 · Jul-z57–z63 · Aug-z64–z70 · Sep-z71–z74 · Okt-z75–z87 · Nov-z88–z91 · Dez-z92–z99",
    "prisluh": "P223-LEAD-P222: probe-s164–s171 → MEJA-ni-v-oknu → nazaj-do-s159 → MEJA-najdena-s161!",
}

out = {
    "okvir": {"scanFrom": 161, "scanTo": 173, "year": 1883,
              "prenos": "2×-neodvisna-md5-15/15 (s159–s173!)",
              "meja_1882_83": "s161 (62.-POTRDITEV-invariante!)",
              "meja_1883_84": "s173 (P222!)",
              "pag": "dvojni-seriji: gola-'sken−5' (1883!) VS-'Pag.'-'sken+13' (1884!)",
              "dvojcki": "z2/z3-DOBRAVCE-×2-Jän-8/9 (page! — ne-GRIBLJE) + TAIL-1882-z105/z106-GRIBLJE-h68-ZWILLINGE (P224-LEAD!)",
              "z99": "TAIL-1883-IZLOČEN (vas-'Obrijuh'-X-open!)",
              "stats": stats},
    "griblje_entries": entries,
    "statistika": stats,
    "anomalije_keys": [a["id"] for a in ANOMALIJE],
}
json.dump(out, open(f"{TMP}/entries_1883.json", "w"), ensure_ascii=False, indent=1)
print(f"entries_1883.json: {len(entries)} GRIBLJE (pričakovano 19!)")
print(f"anomalije: {len(ANOMALIJE)} | cross: {len(CROSS)} | honesty: {len(HONESTY)}")
