#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P230 — agregacija 14-GRIBLJE-vpisov leta 1876 (krstna PREDZGODOVINA 04104, 10/15!).
MEJA-1875/76 = s64/s65-DVO-STRANSKA (NOVA-VARIANTA!): s64 = TAIL-1875 (r1-Dez-1/1-Krasine-h15 + r2-Dez-3/3-Zemelj-h17-MUC!
  + r3-Dez-26/26-GRIBLJE-h11-Anna-Hoggia! + r4-Dez-18/19-RETRO-DUEL-Gradac-h55-Prosenik-×3!) + ★★★ 'finis-Anni-1875'-VELIKA-KALLIGRAFIJA
  ('finis'-LEVO-SREDINA + 'An-ni-1-8-75'-DESNO!-PARALELA-'Incipit-annus-Domini-1877'-P229!) | s65 = glava-'Jahr 1876'-BREZ-INCIPIT!
  + RESTART-z1-NA-DAN-5./5.-JÄNNER-Aloshor[?]-h24-Agnes (oče-Mathias-Hampauhar[?]-½-Ġ.-matec-Anna-Schweiger!-10.-restart-z1!-P221-1.1!-P222-1.1!
  -P223-4.1!-P224-2.1!-P225-1.1!-P226-3.1!-P227-8./9.!-P228-[8↔9]-DUEL!-P229-9./10.!-P230-5./5.!) = 69.-POTRDITEV-invariante (68.-P229!).
★★★ 100-VPISOV-DISTINCT (z1–z100!): vrstna-aritmetika 7+7+7+8+9+8+8+7+8+8+7+7+8+1 = 100 (s65:7!-s66:7!-s67:7!-s68:8!-s69:9!-s70:8!
  -s71:8!-s72:7!-s73:8!-s74:8!-s75:7!-s76:7!-s77:8!-s78-r1:1-TAIL-P229!) + zap-stolpci-VIDNI-×6-strani-1:1 (s65:1–7!-s66:8–14!-s67:15–21!
  -s68:22–29!-s69:30–38!-s70:39–46!-P229-×6-PARALELA!) + s77-zap-'94'-MODRA (Dez-1/1-GRIBLJE-h31!) + s78-r1-zap-'100'-pričakovana-X-open!
★★★ FOLIACIJA-'sken−5'-15/15-SEKVENČNO (59–73!): s64='59'-NARISE!/s65='60'-NARISE!/s66='61'/s67='62'/s68='63'/s69='64'/s70='65'/s71='66'-NARISE!
  /s72='67'/s73='68'/s74='69'/s75='70'/s76='71'/s77='72'/s78='73'-P229! — SKUPNA-SERIJA-59–158-continuum (LUKNJA-'94'-s99-ostaja!).
★★★ 14-GRIBLJE / 14-hiš-BREZ-DUPLIKATOV (h7-h8-h15-h16-h20-h22-h25-h31-h39-h40-h44-h53-h55-h62!-vs-P229-18-hiš-h6/h14-×2!):
  PEZDIRC-×18-vrstic-NOV-REKORD-LINJE-continuum-10-let (×4/×4/×6/×4/×9/×14/×12/×17/×11/×17!-×2-DVOJNI-GRIBLJE-h53-oče+boter!-h55-matec+botra!)
  + ★★★ DVOJČKI-×4-dogodki-REKORD-LINJE (2-BRACE-'Zwillinge'-nota: s71-r4/r5-Peter+Michael-Krasine-h25! + s73-r3/r4-Petrus+Maria-Certoviše-h26!
  + 2-SHARED-ROW-VARIANTI: s71-r6-Nicolaus+Martin-'Gri-moršk'-h15! + s69-r9-Anna+Katharina-Goriče-h25!-vs-×4-P229-ALL-BRACE!)
  + ★★★ NEZAKONSKI-×6-REKORD-LINJE (vs-×5-P228!-×4-P229!): s66-r6-Krasine-h34 + s72-r3-Zemelj-h22 + s72-r7-Certoviše-h13 + s77-r7-Grem-h33
  + s74-r2-Boginja-vas-h42 + s72-r6-'Griže'-h55-WOLFGR!) + ★★★ WOLFGR-ANOMALIJA-DRUŽINA-×3 (s69-r1-Gradac-Wolfgrabiff[?]-garble + s70-r1-Gradac-
  Wolfgr-Annišl[?]-garble + s72-r6-'Griže'-h55-Wolfgr-Daisl[?]-garble-RETRO!-VSI-3:-botra+duhovnik-PRAZNA!-samo-hebamme-Maria-Rom-×2!-P229-TODTGEBOREN-
  GARBLE-DRUŽINA-PARALELA!) + ★★★ MODRI-×11-linij-REKORD (×4-Griblje: h22-†7.10.1931! + h62-umrl-23.12.1953! + h25-†9.12.1935! + h31-umrl-18.9.1961-por-1914!
  + ×7-neG: s65-r3-Chicago-1970! + s67-r6-MMK-Metlika-1962! + s68-r3-MMK-Novo-mesto-1963! + s69-r5-umrl-18.8.1946-poročen-10.9.1911! + s72-r5-umrl-5.1.1950!
  + s75-r5-umrla-9.10.1956! + s75-r6-umrla-20.3.1957!) + HEBAMME-Maria-Rom-×9-continuum (botra-×2: s65-r1!-s66-r1! + hebamme-×7!) + RED-tički-✓-margin
  + rojen≠krsten-Griblje-×4 (h39-12/13! + h20-1/2! + h16-19/20! + h25-18/19!) + zap-94-MODRA + DUHOVNIŠKA-IZMENJAVA-1876 ('Hoggia/Roggja/Hoggin-coop'-
  KURRENT-DUEL-continuum ↔ 'Franz-Dovgan'-ALTERNIRAJÖČE!-Griblje-split-7/7-POPOLNOM-IZENAČEN!-vs-P229-13/7!).
Izhod: /tmp/p230/entries_1876.json"""
import json

TMP = "/tmp/p230"

GRIBLJE = [
 {"z":"z22","sken":68,"pag":"63 [konv.-sken−5]","mesec":"März","rojen":"25","krsten":"25","vas":"Griblje","hisna":"40",
  "otrok":"Maria","spol":"ženski",
  "ocec":"Joannes Brađire[?]-Pezdire[?]-garble-X-open [~PEZDIRC!], ¼ Ġübler",
  "matec":"Anna Jakofčič [~JAKOFČIČ!]",
  "botra":"Mathias Deblič [~DEBLIČ!] + Barbara Hlobučar [~KLOBUČAR!]",
  "_opomba":"★★★ PEZDIRC-oče-garble-X-open (1/7-Griblje!-continuum-10-let-NOV-REKORD-×18!) + DEBLIČ-boter + KLOBUČAR-boter + ★★★ MEJA-1875/76-s64/s65-DVO-STRANSKA-69.-POTRDITEV-invariante! (finis-Anni-1875-KALLIGRAFIJA!-RESTART-z1-5./5.-JÄNNER!-10.-restart!) + podpis-'Hoggia-Coop'-KURRENT-DUEL + zap-22-VIDEN!"},
 {"z":"z26","sken":68,"pag":"63 [konv.-sken−5]","mesec":"April","rojen":"12","krsten":"13","vas":"Griblje","hisna":"39",
  "otrok":"Georg","spol":"moški",
  "ocec":"Nicolaus Šimec [~SIMEC!], ½ Ġübler",
  "matec":"Katarina Jakofčič [~JAKOFČIČ!]",
  "botra":"Anton Brodarič [~BRODARIČ!] + Maria Hlobučar [~KLOBUČAR!]",
  "_opomba":"★★★ SIMEC-oče-nit (1/2!) + JAKOFČIČ-matec-nit + BRODARIČ-boter-nit + KLOBUČAR-boter-nit + rojen≠krsten-12/13 + podpis-'Roggja-Coop'-KURRENT-DUEL-HOGGIN-varianta + zap-26-VIDEN + RED-tička!"},
 {"z":"z28","sken":68,"pag":"63 [konv.-sken−5]","mesec":"Mai","rojen":"1","krsten":"2","vas":"Griblje","hisna":"20",
  "otrok":"Mathias","spol":"moški",
  "ocec":"Peter Pezdire [~PEZDIRC!], ¼ Ġübler",
  "matec":"Katarina Deblič [~DEBLIČ!]",
  "botra":"Mathias Milek [~MILEK!] + Barbara Brodarič [~BRODARIČ!]",
  "_opomba":"★★★ PEZDIRC-oče-nit (2/7!-P229-z84-oče-Peter-Pezdire-h20-1:1-PARALELA!-h20-×2-continuum!) + DEBLIČ-matec-nit + MILEK-boter-nit + BRODARIČ-boter-nit + rojen≠krsten-1/2 + podpis-'Hoggia-Coop' + zap-28-VIDEN + Mai-blok!"},
 {"z":"z32","sken":69,"pag":"64 [konv.-sken−5]","mesec":"April","rojen":"19","krsten":"20","vas":"Griblje","hisna":"16",
  "otrok":"Joannes","spol":"moški",
  "ocec":"Mathias Šelah[?]-garble-X-open, ½ Ġübler",
  "matec":"Anna Nemanic [~NEMANIČ!]",
  "botra":"Georg Žeflko[?]-garble + Dorothea Hrižan [~HRIŽAN!]",
  "_opomba":"★★★ HRIŽAN-boter-nit (1/6!) + oče-garble-Šelah-X-open + NEMANIČ-matec + podpis-'Hoggia-Coop' + zap-32-VIDEN + rojen≠krsten-19/20 + h16-continuum (P227-z28/P228-z29-h17-PARALELA!)"},
 {"z":"z43","sken":70,"pag":"65 [konv.-sken−5]","mesec":"Juli","rojen":"3","krsten":"3","vas":"Griblje","hisna":"7 [+'až'-nota-X-open!]",
  "otrok":"Anna","spol":"ženski",
  "ocec":"Joannes Jetter[?]-Jötter[?]-garble-X-open, Ġavčov[?]-Ġüršlön[?]-garble",
  "matec":"Catharina Hrižan [~HRIŽAN!]",
  "botra":"Anton Hure [~HURE!] + Maria Jetter[?]-als-Amtsvormund-der-Ehegatten-Tochter[?]-nota!",
  "_opomba":"★★★ HRIŽAN-matec-nit (2/6!) + ★★★ HURE-boter-nit (1/1!-P228-×1-PARALELA!) + ★★★ 'als-Amtsvormund'-botra-NOTA (uradni-skrbnik!-nova-anomalia!) + oče-garble-JETTER-X-open + h7-+'až7'-nota-X-open + h7-continuum (P228-izjema-h7-11-let!) + podpis-'Hoggia-Coop' + zap-43-VIDEN + Juli-blok!"},
 {"z":"z46","sken":70,"pag":"65 [konv.-sken−5]","mesec":"Juli","rojen":"8","krsten":"8","vas":"Griblje","hisna":"15",
  "otrok":"Nicolaus","spol":"moški",
  "ocec":"Nicolaus Muc [~MUC!], ½ Ġ.",
  "matec":"Marg. Jarlbič[?]-Jaklič[?]-garble-X-open",
  "botra":"Johann Brayč[?]-Brač[?]-garble + Maria Šruže[?]-garble-X-open",
  "_opomba":"★★★ MUC-oče-nit (1/4!-P229-z1-botra-Nicolaus-Muc-PARALELA!-s64-TAIL-r2-oče-Johann-Muc-continuum!) + matec-garble-Jaklič-X-open + botra-garble-×2 + podpis-Franz-DOVGAN + zap-46-VIDEN + h15-continuum (P223-h15-PARALELA!)"},
 {"z":"z53","sken":71,"pag":"66 [konv.-sken−5]","mesec":"August[?]-DUEL","rojen":"4[?]","krsten":"4[?]","vas":"Griblje","hisna":"22",
  "otrok":"Katharina","spol":"ženski",
  "ocec":"Johann Milek [~MILEK!], ½ Ġ.",
  "matec":"Maria Pezdire [~PEZDIRC!]",
  "botra":"Anton Brodarič [~BRODARIČ!] + Maria Husič [~HUSIČ!]",
  "_opomba":"★★★ MILEK-oče-nit (1/3-Griblje!) + ★★★ PEZDIRC-matec-nit (3/7!) + BRODARIČ-boter-nit + HUSIČ-botra (P229-z106-matec-PARALELA!) + ★★★ MESEC-DUEL-X-open ('August[?]-4/4'-garble-'Wörjarff'-vs-'Juli-27/27'-kronologija-fit-obojje!) + ★★★ MODRI-†7.10.1931-črnilo! + RED-tička + podpis-Franz-DOVGAN + rdeča-margin-†-floret + zap-cut"},
 {"z":"z85","sken":73,"pag":"68 [konv.-sken−5]","mesec":"September","rojen":"15","krsten":"15","vas":"Griblje","hisna":"53",
  "otrok":"Maria","spol":"ženski",
  "ocec":"Joannes Pezdire [~PEZDIRC!], ¼ Ġüblar",
  "matec":"Anna Šerdič[?]-garble-X-open",
  "botra":"Georg Pezdire [~PEZDIRC!] + Anna Dragoš [~DRAGOŠ!]",
  "_opomba":"★★★ PEZDIRC-DVOJNI-vrstica (oče-Joannes+boter-Georg!-4/7!) + ★★★ DRAGOŠ-boter-nit (1/2!-P229-×1-continuum!) + matec-garble-Šerdič-X-open + podpis-'Hoggia-Coop' + zap-cut + September-blok!"},
 {"z":"z86","sken":73,"pag":"68 [konv.-sken−5]","mesec":"September","rojen":"16","krsten":"16","vas":"Griblje","hisna":"62",
  "otrok":"Nicolaus","spol":"moški",
  "ocec":"Anton Kure[?]-Kuer[?]-garble-X-open, ¼ Ġübler",
  "matec":"Barbara Križan [~HRIŽAN/KRIŽAN!]",
  "botra":"Mathias Milek [~MILEK!] + Barbara Brodarič [~BRODARIČ!]",
  "_opomba":"★★★ MODRI-'umrl-dne-23.12.1953-n-občin-št.10'-MODRA! + ★★★ MILEK-boter-nit (2/3!) + BRODARIČ-boter-nit (4/7!) + KRIŽAN-matec-nit (3/6!) + oče-garble-KURE-X-open + podpis-Franz-DOVGAN + zap-cut + h62-nova-hiša!"},
 {"z":"z88","sken":74,"pag":"69 [konv.-sken−5]","mesec":"September","rojen":"18","krsten":"19","vas":"Griblje","hisna":"25",
  "otrok":"Mathias","spol":"moški",
  "ocec":"Mathias Brinc[?]-Brine[?]-garble-X-open, ½ Ġ.",
  "matec":"Maria Mavrin [~MAVRIN!]",
  "botra":"Johann Počih[?]-Požih[?]-garble + Anna Plutai[?]-garble-X-open",
  "_opomba":"★★★ BRINC-oče-nit (P229-z67/z68-matec-Anna-Brinc-PARALELA!-BRINC-continuum!) + ★★★ MODRI-†9.12.1935-črnilo! + rojen≠krsten-18/19 + oče-garble-Brinc-X-open + botra-garble-×2 + podpis-Franz-DOVGAN + zap-cut + h25-nova-hiša!"},
 {"z":"z92","sken":75,"pag":"70 [konv.-sken−5]","mesec":"October","rojen":"19","krsten":"19","vas":"Griblje","hisna":"8",
  "otrok":"Catharina","spol":"ženski",
  "ocec":"Joannes Jakofčič [~JAKOFČIČ!], ½ Ġübla",
  "matec":"Anna Brodarič [~BRODARIČ!]",
  "botra":"Marcus Hlobučar [~KLOBUČAR!] + Anna Dragoš [~DRAGOŠ!]",
  "_opomba":"★★★ JAKOFČIČ-oče-nit (3/8!) + ★★★ BRODARIČ-matec-nit + ★★★ DRAGOŠ-boter-nit (2/2-KOMPLET!) + KLOBUČAR-boter-nit (4/5!) + podpis-'Hoggia-Coop' + zap-cut + October-blok! + h8 (P223-h8-PARALELA!)"},
 {"z":"z96","sken":76,"pag":"71 [konv.-sken−5]","mesec":"November","rojen":"21","krsten":"21","vas":"Griblje","hisna":"55",
  "otrok":"Maria","spol":"ženski",
  "ocec":"Nicolaus Šimec [~SIMEC!], ½ Ġ.",
  "matec":"Maria rođ. Pezdire [~PEZDIRC!]",
  "botra":"Mathias Škranc[?]-garble + Anna Pezdire [~PEZDIRC!]",
  "_opomba":"★★★ SIMEC-oče-nit (2/2-KOMPLET!) + ★★★ PEZDIRC-DVOJNI-vrstica (matec-Maria+botra-Anna!-6/7!) + botra-garble-Škranc-X-open + podpis-Franz-DOVGAN + zap-cut + November-blok! + h55-continuum (s72-r6-'Griže'-h55-PARALELA!)"},
 {"z":"z98","sken":76,"pag":"71 [konv.-sken−5]","mesec":"November","rojen":"23","krsten":"23","vas":"Griblje","hisna":"44",
  "otrok":"Barbara","spol":"ženski",
  "ocec":"Mathias Hruzelj[?]-garble-X-open, ½ Ġübler",
  "matec":"Agnes Hlobučar [~KLOBUČAR!]",
  "botra":"Marcus Škranc[?]-garble + Maria Hlobučar [~KLOBUČAR!]",
  "_opomba":"★★★ KLOBUČAR-DVOJNI-vrstica (matec-Agnes+botra-Maria!-5/5!) + oče-garble-Hruzelj-X-open + botra-garble-Škranc + podpis-'Roggja-Coop'-KURRENT-DUEL + zap-cut + h44-nova-hiša!"},
 {"z":"z94","sken":77,"pag":"72 [konv.-sken−5]","mesec":"Dezember","rojen":"1","krsten":"1","vas":"Griblje","hisna":"31",
  "otrok":"Nicolaus","spol":"moški",
  "ocec":"Nicolaus Županič [~ŽUPANIČ!], ½ Ġübl.",
  "matec":"Katharina rođ. Pezdire [~PEZDIRC!]",
  "botra":"Johann Županič [~ŽUPANIČ!] + Maria Škarasinič [~ŠKARASIČ/HRIŽAN-variant!]",
  "_opomba":"★★★ PEZDIRC-matec-nit (7/7-KOMPLET-GRIBLJE!) + ★★★ ŽUPANIČ-oče+botra-DVOJNI-nit + ★★★ zap-'94'-MODRA-LEVO-ROB (zap-stolpec-NE-viden-na-s77-ampak-arhivar-modra-potrditev!) + ★★★ MODRI-dolg-'umrl-dne-18.9.1961-v-Suhorju[?]-kotnik[?]'+por-1914[?]+†-garble! + podpis-Franz-DOVGAN + h31 (P228-'h33-DUEL'-RAZLIČNA!-z101-h34-RAZLIČNI!) + Dezember-blok!"},
]
assert len(GRIBLJE) == 14
assert len(set(g["hisna"].split()[0] for g in GRIBLJE)) == 14

OKVIR = {
 "window": "s64–s78 (15 skenov; s71–s78-proba-P229-LEAD-DESCENDING! + s60–s70-probe-globlje!-s64/s65-MEJA-DVO-STRANSKA!-s78-tail-r1-P229!)",
 "prenos": "2×-neodvisna-md5-15/15 (s64–s78!-s78-fresh-fetch-md5-1:1!)",
 "foliacija": "gola-svinčna-'sken−5'-15/15-SEKVENČNO (s64='59'-NARISE!/s65='60'-NARISE!/s66='61'/s67='62'/s68='63'/s69='64'/s70='65'/s71='66'-NARISE!/s72='67'/s73='68'/s74='69'/s75='70'/s76='71'/s77='72'/s78='73'-P229!-3×-VIZUALNO-NARISE!) — SKUPNA-SERIJA-59–158-continuum (LUKNJA-'94'-s99-P228-ostaja!)",
 "mejaStart": "s64/s65-DVO-STRANSKA-MEJA (NOVA-VARIANTA!-vs-P229-s78-ENO-STRANSKA!): s64 = TAIL-1875 (r1-Dez-1/1-Krasine-h15-Briglanič[?]/Brodarič-Dovgan! + r2-Dez-3/3-Zemelj-h17-oče-Johann-MUC! + r3-Dez-26/26-GRIBLJE-h11-Anna-Zunič[?]/Dragar[?]-botra-'Juve-Šimec'+Anna-Jakofčič-Hoggia! + r4-Dez-18/19-RETRO-DUEL-Gradac-h55-18/19-PO-26/26!) + glava-'Jahr 1875' + ★★★ 'finis-Anni-1875'-VELIKA-KALLIGRAFIJA ('finis'-LEVO-SREDINA + 'An-ni-1-8-75'-DESNO-KURRENT!-PARALELA-'Incipit-annus-Domini-1877'-P229-ZAKLJUČEK-TIP!) | s65 = glava-'Jahr 1876'-BREZ-INCIPIT (POZOR-P229-LEAD-'Incipit-LAHKO-se-ponovi'-NAPAČNA-PREDPOSTAVKA!) + RESTART-z1-NA-DAN-5./5.-JÄNNER-Aloshor[?]-h24-Agnes-Hampauhar[?]/Schweiger!-10.-restart-z1!)",
 "mejaKonec": "s78-r1-TAIL-1876 (P229!-Dobravce-h16-Martin-Dez-24/26-Hržnič[?]/RUS-×3-vrstica!-Hoggia!-zap-100[?]-X-open!) + 'Incipit-annus-Domini-1877'-KALLIGRAFIJA-s78-P229!",
 "rowsTotal": 100,
 "aritmetika": "7+7+7+8+9+8+8+7+8+8+7+7+8+1 = 100 (s65:7 + s66:7 + s67:7 + s68:8 + s69:9 + s70:8 + s71:8 + s72:7 + s73:8 + s74:8 + s75:7 + s76:7 + s77:8 + s78-r1:1!) — zap-stolpci-VIDNI-×6-strani-1:1 (s65:1–7!-s66:8–14!-s67:15–21!-s68:22–29!-s69:30–38!-s70:39–46!-P229-×6-PARALELA!) + s77-zap-'94'-MODRA + s78-r1-zap-'100'-pričakovana-X-open (aritmetika-99+1!) — s71–s76-zap-cut/faint (P229-s84+-PARALELA!) — TWINS-SHARED-ZAP-VARIANTI (s69-r9-Anna+Katharina-zap-38-ISTI! + s71-r6-Nicolaus+Martin-en-vrsti!)",
 "meseci": "M1+A2+Mai1+Juli2+A[?]1+S3+O1+N2+D1 = 14-Griblje (Jänner/Feber/Juni-×0!-3-prazne!-vs-P229-Juni/Sep-×0!)",
 "duhovniki": "DVOJNA-IZMENJAVA-1876-'Hoggia/Roggja/Hoggin-Coop'-KURRENT-DUEL-continuum (ISTI-duhovnik-4-grafični-varianti!) ↔ 'Franz-Dovgan' — ALTERNIRAJÖČE — Griblje-split-HOGGIN-×7/DOVGAN-×7-POPOLNOM-IZENAČEN (vs-P229-13/7!)",
}

stats = {
 "griblje_vpisov": 14,
 "griblje_his": 14,
 "dup": "BREZ-DUPLIKATOV (14-hiš-DISTINCT!-h7-h8-h15-h16-h20-h22-h25-h31-h39-h40-h44-h53-h55-h62!-vs-P229-18-hiš-h6-×2/h14-×2!)",
 "pezdirc": "★★★ ×17-vrstic-TIE-REKORD-P228-continuum-10-let (×4/×4/×6/×4/×9/×14/×12/×17/×11/×17!): Griblje-×6-vrstic-8-oseb (z40-oče-Joannes-Brađire[?]-X-open! + z28-oče-Peter-Pezdire-h20! + z53-matec-Maria-Pezdire-h22! + z85-oče-Joannes+boter-Georg-Pezdire-h53-DVOJNI! + z96-matec-Maria+botra-Anna-Pezdire-h55-DVOJNI! + z94-matec-Katharina-Pezdire-h31!) + ne-Griblje-×11 (s66-r4-matec-Maria-Perdine[?]-Griče-h6-DUEL! + s67-r1-boter-Peter-Pezdire-Krasine! + s67-r2-oče-Anton+boter-Mathias-Grem-DVOJNI! + s67-r5-oče-Georg-Krasine! + s69-r5-matec-Maria-Krasine! + s70-r2-boter-Anton-Primostek! + s70-r6-boter-Mathias-Podzemelj! + s72-r2-oče-Michael-Boršt! + s74-r8-oče-Peter-X-open-Krasine! + s76-r7-boter-Michael-Vranoviče-mit-Boršt! + s77-r1-boter-Mathias-Otok!) — ×2-DVOJNI-GRIBLJE-vrstici (h53!-h55!)",
 "jakofčič": "×8-linij (Griblje-×3: z40-matec-Anna! + z26-matec-Katarina! + z92-oče-Joannes!; ne-G-×5: s66-r4-oče-Mathias-Griče-DUEL! + s73-r5-matec-Anna-Prilozje! + s73-r8-botra-Georg+Dorothea-×2-Certoviše! + s76-r2-oče+botra-×2-Certoviše!)",
 "milek": "×5 (z53-oče-Johann-Griblje-h22! + z28-botra-Mathias-h20! + z86-botra-Mathias-h62! + ne-G: s66-r3-botra-Mathias-Dragoš! + s72-r3-botra-Martin-Zemelj!)",
 "deblič": "×3 (z40-botra-Mathias! + z28-matec-Katarina! + ne-G: s68-r5-boter-Mathias-Deblič[?]-Certoviše!)",
 "brodarič": "×7 (z26-botra-Anton! + z28-botra-Barbara! + z86-botra-Barbara! + z92-matec-Anna! + s66-r6-botra-Katharina! + s64-TAIL-r1-matec-Agnes-Brodarič! + s67-r5-botra-Anna-Krasine!)",
 "klobučar": "×5 (z40-botra-Barbara! + z26-botra-Maria! + z98-matec-Agnes+botra-Maria-DVOJNI! + z92-botra-Marcus!)",
 "hrižan": "×6 (z32-botra-Dorothea! + z43-matec-Catharina! + z86-matec-Barbara-Križan! + z94-botra-Maria-Škarasinič-variant! + s74-r8-matec-Anna-Hrižan[?]-X-open! + s76-r2-matec-Catharina-Certoviše!)",
 "simec": "×3 (z26-oče-Nicolaus! + z96-oče-Nicolaus!-2×-Nicolaus-isti-imes! + s67-r1-matec-Maria-Krasine!-KOMPLET-Griblje-2/2!)",
 "dragoš": "×2 (z85-botra-Anna! + z92-botra-Anna!-×2-Griblje-KOMPLET-continuum!)",
 "hure": "×1 (z43-botra-Anton-h7!-P228-×1-PARALELA!)",
 "muc": "×4 (z46-oče-Nicolaus-h15! + s64-TAIL-r2-oče-Johann-Zemelj! + s75-r2-botra-Nicolaus+Maria-DVOJNI-Primostek! + s77-r8-botra-Nicolaus+Maria-DVOJNI-Primostek!)",
 "županič": "×2-Griblje-DVOJNI (z94-oče-Nicolaus+botra-Johann-h31!)",
 "dvojcki": "★★★ ×4-dogodki-REKORD-LINJE (vs-×4-P229-ALL-BRACE!-NOVI-VARIANTI!): (1) s71-r4/r5-Peter+Michael-Krasine-h25-Aug-19/20-BRACE-'Zwillinge'-vertikalna-nota-1:1-krop! + (2) s73-r3/r4-Petrus+Maria-Certoviše-h26-Sep-15/15-BRACE-'Zwillinge'-nota! + (3) s71-r6-Nicolaus+Martin-'Gri-moršk[?]'-h15-Juli-25/25-SHARED-ROW-VARIANTA (2-otroka-en-vrsti-en-zap!) + (4) s69-r9-Anna+Katharina-Goriče-h25-Juni-4/5-SHARED-ROW-VARIANTA (zap-38-ISTI-za-oboj!-+MODRI-'†5.9.1945'-Anna!) — 2-BRACE + 2-SHARED-ROW!",
 "nezakonski": "★★★ ×6-REKORD-LINJE (vs-×5-P228!): s66-r6-Krasine-h34 (Febrar-3/3!-oče-PRAZNA!-matec-Maria-Kralj-dolga-nota-'Kamen-Parijat-pri-Bedenu-št.10'-botra-Černič+Brodarič+Jurejčič!) + s72-r3-Zemelj-h22 (August-13/13!-oče-dash!-matec-Maria-Jaklič[?]!-botra-Škala+MILEK!) + s72-r7-Certoviše-h13 (August-29/29!-oče-dash!-matec-Maria-Jurejčič[?]-garble!) + s77-r7-Grem-h33 (Dezember-18/18!-oče-dash!-matec-Katharina-Šelah[?]!-botra-Škala+Theresia!) + s74-r2-Boginja-vas-h42 (September-18/18!-oče-dash!-matec-Barbara-Štubler-dolga-nota!) + s72-r6-'Griže'-h55-WOLFGR (RETRO!-oče-dash!)",
 "wolfgr": "★★★ WOLFGR-ANOMALIJA-DRUŽINA-×3-NOVA (P229-TODTGEBOREN-GARBLE-DRUŽINA-PARALELA!): s69-r1-Gradac-h16[?]-'Wolfgrabiff[?]'-garble-MAX (Mai-3!-botra+duhovnik-VSI-PRAZNI!-samo-hebamme-Maria-Rom!-starši-Anton-Kraby[?]+Maria-Winter!) + s70-r1-Gradac-h10-'Wolfgr-Annišl[?]'-garble-MAX (Juni-17!-botra+duhovnik-VSI-PRAZNI!-samo-hebamme-Maria-Rom!-starši-Mathias-Šopit[?]+Cecilia-Vuka[?]!) + s72-r6-'Griže'-h55-'Wolfgr-Daisl[?]'-garble-MAX-RETRO (25/25-PO-28/29!-oče-dash!-botra+duhovnik-PRAZNI!-starši-dash+Agnes-Martin[?]-garble!) — 3-instance-isti-WOLFGR-PATTERN-čez-3-mesce!",
 "modri": "★★★ ×11-linij-REKORD-LINJE (vs-×9-P229!): Griblje-×4 (z53-h22-'†7.10.1931'-črnilo-s-floretom! + z86-h62-'umrl-dne-23.12.1953-n-občin-št.10'-MODRA! + z88-h25-'†9.12.1935'-črnilo! + z94-h31-'umrl-dne-18.9.1961-v-Suhorju[?]'-MODRA-dolg-+por-1914[?]!) + ne-G-×7 (s65-r3-'Anna-v-omr-1970-v-CHICAGO'-MODRA! + s67-r6-MMK-Metlika-'umrla-3.II.1962'-dolg-'1/1964-št-330'-amtlj-con! + s68-r3-MMK-Novo-mesto-'dne-14.10.1963'-'1964-br-42'-quadner-16.10.1963! + s69-r5-'umrl-18.8.1946'-'poročen-10.9.1911-na-Cernice-25'! + s72-r5-'umrl-5-januar-1950-v-Sogjinu-št-17'! + s75-r5-'umrla-9.10.1956'-dolg! + s75-r6-'umrla-20.3.1957'!) — 1931–1970-razpon!-MMK-×2!",
 "cnilo_pripisi": "★★★ črnilo-†-×2-Griblje (z53-'†7.10.1931'-s-floretom! + z88-'†9.12.1935'!) + MODRI-†-×2-Griblje (z86!-z94!) = ×4-†-GRIBLJE-REKORD! + ne-G-črnilo/MODRI-×7 + s74-r2-matec-dolga-nota-'Štubler-Špitál(?)'-X-open + s77-r2-Šcippel-göttlie-nota!",
 "posebne": "★★★ finis-Anni-1875-KALLIGRAFIJA (paralela-Incipit-1877!) + ★★★ WOLFGR-DRUŽINA-×3 + ★★★ 'als-Amtsvormund'-botra-NOTA (z43!-uradni-skrbnik-NOVI-TIP!) + ★★★ RETRO-VPISI-×2 (s72-r6-25/25-PO-28/29-Griže! + s64-TAIL-r4-18/19-PO-26/26-Gradac!) + ★★★ zap-'94'-MODRA + HEBAMME-Maria-Rom-×9-continuum (botra-×2: z1-s65!-z8-s66! + hebamme-×7: s69-r1!-s70-r1!-s70-r3!-s74-r3!-s74-r4!-s74-r7!-s76-r3!-Gradac-continuum!) + rojen≠krsten-Griblje-×4 (z26-12/13! + z28-1/2! + z32-19/20! + z88-18/19!) + RED-tički-✓-margin-continuum + vas-garble-DUELI (s66-r4-'Gritže'-Griče-DUEL! + s72-r6-'Grilže'! + s71-r6-'Gri-moršk'! + s65-r1-'Aloshor[?]'! + s70-r2-'Gradove[?]'-X-open!) + hišne-DUELI (s66-r4-h6/67! + s72-r6-h55-'sof55/ad55'-nota! + s73-r8-h20/'pmix-16'! + s70-r5-h7-+'až7'-nota!)",
}

out = {"leto": 1876, "griblje_entries": GRIBLJE, "okvir": OKVIR, "stats": stats}
json.dump(out, open(f"{TMP}/entries_1876.json", "w"), ensure_ascii=False, indent=1)
print(f"entries_1876.json: {len(GRIBLJE)}-Griblje-vpisov / 100-DISTINCT / 14-hiš-BREZ-DUPLIKATOV")
