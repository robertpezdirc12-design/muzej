#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P110 — generator evidence JSON (krstna 1915)."""
import json

G = []  # Griblje entries (full detail)

G.append({
    "row": 8, "year": 1915, "month": "Januar", "born": "20.", "baptized": "22.",
    "village": "Griblje", "houseNo": "88", "scan": 269, "page": 225,
    "child": "Ivana",
    "father": "Peter Brinec, bajtar, roj. 28/9 1860 (por. 25.9.1892 | 12.96 [~])",
    "mother": "Ana roj. Butala, 22/12 1874 [faza-1 »Buntala« POPRAVLJENO]",
    "botra": "Janez Brinec in žena njegova Doroteja Brinec (½ zemlj.)",
    "babica": "Marija Jakofčič",
    "priest": "V. Valerijan Učak",
    "notes": [
        "**P109 lead POTRJEN (GRIBLJE 88 Ivana!)**",
        "marg. pod imenom: »+ 20/[II] 1915« = † 20.2.1915 [~ — dojenček, star ~1 mesec; 4× d1]",
        "h88 = 4. VPIS vzorca (1886, 1904, 1910 → 1915); VRZEL 5 LET",
        "starševa poroka dvom: »25.9. 1892« + »12.96« [~ — dva datuma; ZOOM ostaja]",
        "podpis svinčnik/bled"
    ]
})

G.append({
    "row": 15, "year": 1915, "month": "Marec", "born": "6.", "baptized": "7.",
    "village": "Griblje", "houseNo": "45", "scan": 270, "page": 226,
    "child": "Zora Jožefa",
    "father": "Franc Rajhmer [~], čuv.[aj]? [~], roj. 13/12 1882 (por. 18.4.1908)",
    "mother": "Ivana roj. Tadej, 13/8 86 [~]",
    "botra": "Jurij Berdir? [~] (½ zemlj.) + Terezija Jakofčič, ros. žena",
    "babica": "Marija Jakofčič",
    "priest": "Učak [~]",
    "notes": [
        "marg.: »+ 25/7 15« = † 25.7.1915 (dobenček, star ~3,5 meseca!)",
        "h45 = 6. VPIS vzorca (1896–1912); VRZEL 3 LETA",
        "oče ime/status dvom: »Rajhmer« + »čuvaj« [~ — 3.2× + 5×]; roj. 13/12 [~ 3/12]"
    ]
})

G.append({
    "row": 16, "year": 1915, "month": "Marec", "born": "16.", "baptized": "17.",
    "village": "Griblje", "houseNo": "70", "scan": 270, "page": 226,
    "child": "Barbara",
    "father": "Matija Brinec, ½ zemlj., roj. 15/7 1883 [~ — 4×; faza-1 »1888« POPRAVLJENO]",
    "mother": "Marija (1877), roj. PEZDIREC, r. 30/1? [~ — faza-1 »Perdivec« POPRAVLJENO (3.2×); PEZDIREC mreža!]",
    "botra": "Miko Šegina? [~] (½ zemlj.) + Ana Brinec, ros. žena",
    "babica": "Barbara Adlešič",
    "priest": "Kapl. Bitnar",
    "notes": [
        "EMŠO ž. 1603915505171 (5× jasno — faza-1 »5505141« POPRAVLJENO)",
        "h70 = 3. VPIS vzorca (1893, 1912 → 1915); VRZEL 3 LETA",
        "marg.: mož umrl dne 04.01.1994 [~ — faza-1 »oče« ZAVRŽENO: nemogoče za očeta r. 1883] + umrla 23.06.2004 (MKU MO Novo mesto 1.2004, str. 220, zap. št. 312) + poročena 13.2.1939 + 12.03.2001/25.10.1982 matičarki"
    ]
})

G.append({
    "row": 17, "year": 1915, "month": "Marec", "born": "22.", "baptized": "23.",
    "village": "Griblje", "houseNo": "78", "scan": 272, "page": 227,
    "child": "Jožefa",
    "father": "Anton Ložar [~ Ložar/Lozar], ½ zemlj., roj. 5/5 890 (por. 16.1.1912)",
    "mother": "Barbara roj. Križan, r. 20/6 1889",
    "botra": "Janez Kambič (½ zemlj.) + Katar. Šapič, ros. žena [faza-1 »Hatar.« = Katar.!]",
    "babica": "Marija Jakofčič",
    "priest": "Učak d.i. (svinčnik)",
    "notes": [
        "marg.: »‡ 10.9. 1917.« = † 10.9.1917 (3.5× jasno — P109 lead »1916« ZAVRŽENO!)",
        "h78 = 3. VPIS vzorca (1887, 1888 → 1915); **VRZEL 27 LET = NOV REKORD vzorca!** (prej h53 16 let)",
        "oče ime dvom: Ložar [~]"
    ]
})

G.append({
    "row": 48, "year": 1915, "month": "Julij", "born": "18.", "baptized": "19.",
    "village": "Griblje", "houseNo": "13", "scan": 277, "page": 231,
    "child": "Ana",
    "father": "Matija JAKOBČIČ [~ — faza-1 »Jaklič/Jakličič« POPRAVLJENO (4× d29)], ½ zemljak, roj. 17.8. 1856",
    "mother": "Marija roj. Jakofčič, 24.2.1877 (por. 28.1.1910)",
    "botra": "Matija Perdivec (½ zemlj.) + Katarina Jakofčič, ½ zemljaka žena",
    "babica": "Marija Jakofčič",
    "priest": "V. Valerijan Učak",
    "notes": [
        "h13 = 8. VPIS vzorca (1885–1913); VRZEL 2 LETI",
        "oče star 59 let ob krsti (roj. 1856!) — najstarejši oče v vzorcu? [~]",
        "boter Perdivec + mati Jakofčič = mrežni斯基 vezi (cf. r16 mati PEZDIREC)"
    ]
})

G.append({
    "row": 66, "year": 1915, "month": "Oktober", "born": "26.", "baptized": "28.",
    "village": "Griblje", "houseNo": "40", "scan": 280, "page": 234,
    "child": "Marija Ana",
    "father": "Nikolaj Pezdirec, posestnik ½ z., roj. 28.11. 1874 (por. 16.11. 1907)",
    "mother": "Rosa roj. Tuvan, r. 29.1. 1880",
    "botra": "Matija Urh, posest. + Ana Pezdirec, posest žena",
    "babica": "Marija Jakofčič, n.zp.",
    "priest": "V. Valerijan Učak d.i.",
    "notes": [
        "marg.: »+ 23. 6. 1943« = † 23.6.1943 (2. svetovna doba!)",
        "h40 = 6. VPIS vzorca (1897–1912); VRZEL 3 LETA",
        "trak čez vrstico (vendar vse berljivo 3×)"
    ]
})

G.append({
    "row": 67, "year": 1915, "month": "November", "born": "2.", "baptized": "3.",
    "village": "Griblje", "houseNo": "32", "scan": 280, "page": 234,
    "child": "Marija",
    "father": "Matija Štravs, posest ½ z., roj. 1.I. 1862 (por. 8.II. 1904)",
    "mother": "Marjeta roj. Šimec, r. 22.2. 1875",
    "botra": "Mihael Jakofčič, posestnik? + Barbara Štrucelj, pos. žena [ŠTRUCELJ mreža!]",
    "babica": "Marija Jakofčič, nj.",
    "priest": "V. Valerijan Učak d.i.",
    "notes": [
        "EMŠO ž. 0211915505717 (4× jasno)",
        "h32 = 11. VPIS vzorca (1889–1909 — največ med hišami 1915!); VRZEL 6 LET",
        "marg.: umrla 31.1.1989 v Novem mestu (MKU Novo mesto 1.1989, str. 112, zap. št. 66) + poročena 19.2.1939 + 12/3-1984 + 14.6.1983 matičarki"
    ]
})

G.append({
    "row": 69, "year": 1915, "month": "November", "born": "8.", "baptized": "8.",
    "village": "Griblje", "houseNo": "46", "scan": 281, "page": 235,
    "child": "Martin",
    "father": "Anton Brodarič, posest. ½ zem., roj. 14/11-1859 (por. 7/11-1904)",
    "mother": "Katarina roj. Milek, 1./8.-1876 [MILEK — cf. P108 h34/h65!]",
    "botra": "Nikolaj Želejko? [~], posr. župan + Ana Pezdirec, posed žena",
    "babica": "Marija Jakofčič, n.zp.",
    "priest": "Kapl. Bitnar",
    "notes": [
        "VELIKA modra marg.: poročen 19.3.1961 v franc. Karlovci s Pi[ronoš]? Ivanko [~] + poroka 19.1.1952 v Žlogu? [~] + **zakonska zveza RAZVELJAVLJENA s sodbo okrož. sodišča št. K 757/65-10 z dne 2.12.1965 v Karlovci (razveljavljena/razvezana!) + Gradac 19.4.1966 matičar** + umrl 15.5.1992 Karlovci [~]",
        "h46 = 10. VPIS vzorca (1893–1913); VRZEL 2 LETI",
        "boter »župan« = 2. župan-botra v vzorcu (cf. r40 Jakob Stipanič župan!)"
    ]
})

G.append({
    "row": 72, "year": 1915, "month": "November", "born": "15.", "baptized": "16.",
    "village": "Griblje", "houseNo": "9", "scan": 281, "page": 235,
    "child": "Neža",
    "father": "Oswald JAKOBČIČ [~ — faza-1 »Jakobeč« POPRAVLJENO; cf. r48 Matija Jakobčič — ISTA familija v h13+h9?], posest ½ z., roj. 3. aug 1889 (por. 6.2.1911)",
    "mother": "Terezija roj. Klepec, r. 21.6. 1890 [faza-1 »20.6« POPRAVLJENO]",
    "botra": "Jurij Klepec, posest. + Marija Žunič, posest žena",
    "babica": "Marija Jakobčič, neizp. [babica = verj. očetova mati]",
    "priest": "V. Valerijan Učak d.i.",
    "notes": [
        "marg.: »+ 23/12 1916« = † 23.12.1916 (dojenček)",
        "h9 = 4. VPIS vzorca (1896, 1900, 1913 → 1915); VRZEL 2 LETI",
        "ime OSWALD = 2. nemško-modno ime leta (cf. r21 Vilhelm + r49 Emil Filip Leopold)",
        "oče star 26 — mlad"
    ]
})

G.append({
    "row": 74, "year": 1915, "month": "November", "born": "25.", "baptized": "26.",
    "village": "Griblje", "houseNo": "22", "scan": 282, "page": 236,
    "child": "Nikolaj",
    "father": "Nikolaj Milek, posest ½ z., roj. 13.11. 1869 (por. 12.2. 1900) [MILEK ×2 v 1915 — cf. r69 mati Milek!]",
    "mother": "Ana roj. Črnič, 2.8. 1875",
    "botra": "Nikolaj Požek, p. ½ z. + Ana Črnič, posest žena",
    "babica": "Marija Jakofčič, neizž.",
    "priest": "Valerijan Učak d.i.",
    "notes": [
        "EMŠO ž. 2511915500090 (4× jasno)",
        "h22 = 7. VPIS vzorca (1899–1912); VRZEL 3 LETA",
        "marg.: sklenil zakonsko zvezo 15.08.1945 v Črnomlju z Alezijo? Angelo? (RNK Črnomelj 1.1945 zap. št. 84) + umrl 24.04.1992 v Črnomlju (MKU 1.1992 str. 214 zap. št. 48 [~ — faza-1 »1932« POPRAVLJENO: nemogoče po poroki 1945]) + Metlika 19.11.1992"
    ]
})

G.append({
    "row": 78, "year": 1915, "month": "December", "born": "18.", "baptized": "18.",
    "village": "Griblje", "houseNo": "53", "scan": 282, "page": 236,
    "child": "Janez",
    "father": "Jure Dragos, posest ½ z., roj. 23. april 1888 (por. 21/4-1913) [DRAGOS — cf. P107 r47 + P109 r78 mrtvorojen Dragos × Bahorič!]",
    "mother": "Marjeta Pezdirc, 14. aug. 1891",
    "botra": "Matija Štravs, posest. + Katarina Pezdirc, posest žena",
    "babica": "Marija Jakofčič, neizpr.",
    "priest": "Kapl. Bitnar",
    "notes": [
        "EMŠO ž. 1812915500054 (4× jasno)",
        "h53 = 6. VPIS vzorca (1891–1914); **ZAPORED 2. LETO** (1914 r17!)",
        "marg.: poročen 5. marec 1947 s Petjak Marijo? [~] + umrl 02.10.1958 (MKU NO Novo mesto 1.1958, str. 251, zap. št. 2345?) + umrla 05.12.1955 + **odločba (Ljubljana) dne 16.3.1948 postala pravnomočna 16.3.1948 — Gradac 4.6.1948 matičar, nam. [~ — 2× d23; vsebina dvom: posvojitev/rodovna pravica?]**"
    ]
})

EX_META = [
    (1, "Škrilje", "1", "Janez", "Januar 1./2.; oče Janez Tome ½ zemlj. × Marija Kure; botra Jurij Klepec ½ Črmlj + Bara Štrucel; babica Marija Piletič; podpis Kapl. Bitnar (svinčnik — d16b!); marg. † 4.5.1916 [~]"),
    (2, "Cerkvišče", "19", "Anton", "Januar 8./9.; EMŠO ž. 0801915500210 (d17 3.5×!); oče Janez Mravinec ½ zemlj. (5.1.1874; por. 13.5.02) × Marija roj. Trvajevčič (29.5.1871); botra Anton Starašinič + Marija Gabrijan; babica Ana Marentič; podpis Kapl. Bitnar; marg. umrl 20.9.1981 Gorbovica? + zaročena 6.2.1932 Gradac [~]"),
    (3, "Boršt", "17", "Jožefa", "Januar 8./11.; EMŠO ž. 0801915005026; oče Nikolaj Štravs ½ zemljak × Katarina roj. Klepec; botra Marija Marentič + Ana Marentič; babica Barbara Marentič; podpis Valerijan Učak"),
    (4, "Vranoviče", "14", "Marija", "Januar 22./23.; oče Jožef Jakša? [~ Jacka/Jokša] ½ zemlj. (18/1/75) × Marija roj. Švagelj (6/6/79); botra Martin Sakša + Neža Švagger; babica Marija Piletič; podpis Kapl. Bitnar"),
    (5, "Otok", "12", "Marija", "Januar 23./23.; EMŠO ž. 2301914505241; oče Peter Kure bajtar (26/6/73; por. 6/3 1905) × Margareta roj. Križan (3/7/74); botra Miko Križan + Ana Križan; babica Marija Piletič; podpis Kapl. Bitnar; marg. umrla 16.01.1995 Metlika"),
    (6, "Vranoviče", "4", "Jožef", "Januar 27./29.; ‡ 7.1.1917; oče Jožef Plut ½ zemlj. (7/3/87; por. 16/2 1914) × Katarina roj. Simonič (13/7 1894); botra Martin Plut (Črnomelj) + Frančiška Simonič; babica Marija Piletič; podpis Kapl. Bitnar"),
    (7, "Cerkvišče", "32", "Jožef", "Februar 10./11.; oče Peter Jakofčič ½ zemlj. (10/1/72; por. 17/5 1899) × Ana r. Rusič (3/1/74); botra Peter Starasinič s žena Marija Starasinič; babica Ana Husič nezg.; podpis Valerijan Učak; marg. poročen 3.3.1946"),
    (9, "Boršt", "49", "Jožef", "Januar 25./26.; oče Nikolaj Rožman bajt. (17/1 882; por. 29/6 1904) × Marija roj. Taiše? [~]; botra Nikolaj Prus s žena Ana Prus; babica Barbara Marentič; podpis V. Valerijan Učak; marg. poročen 7.10.1945 Beograd? [~]"),
    (10, "Kapljišče", "5", "Terezija", "Marec 1./1.; EMŠO ž. 0103915505038; oče Anton Marentič ½ zemlj. (1/7/72; por. 5.2.1899) × Barbara roj. Krašovec (1/7/72); botra Martin Štefanič + Marija Grdiša slik. žena; babica Marija Piletič; podpis Kapl. Bitnar; marg. umrla 07.05.1993 G. Lokvica? + VPIS PRENEŠEN (dose 25.11.2005? [~])"),
    (11, "Krivoglavice", "50", "Jožefa", "Marec 2./3.; EMŠO ž. 0203915505056; oče Nikolaj Milavec bajt. (29/3 1870; por. 24.10.1897) × Marija roj. Ogulin (3/8/78); botra Nikolaj Kambič + Ana Kambič; babica Marija Krasinec; podpis Kapl. Bitnar; velika marg. (1946/1976 Gordan maticar [~]) + umrla 02.10.1997"),
    (12, "Zemelj", "46", "Jožef", "Marec 1./3. [krsta 3.3. = ista dan kot r11 — register urejen po KRSTI; prečrtan »April« nadpis = pisarjev false start (d6a 2×!)]; oče Matija Jurajevčič bajt. (24.7.880; por. 27.7.1913) × Marija roj. Macele (3/8/85); botra Janez Jurajevčič + Marija Starašinič; babica Marija Piletič; podpis Kapl. Bitnar; marg. žena umrla 12.03.1980 Subotica + poročen 27.10.1941 Beograd"),
    (13, "Boršt", "22", "Jožef", "Marec 5./6.; EMŠO ž. 0503915500090 (s271 DUP RAZKRIVA — s270 pokrit z nalepko!); oče Janez Kralj ½ zemlj. (4/8/75; por. 27.9.903) × Marija roj. Mratova? [~]; botra Peter Kralj + Ana Kralj; babica Barbara Marentič; podpis Učak d.i.; marg. poročen 26.11.1937 Beograd? + žena umrla 08.01.1997 Ljubljana"),
    (14, "Krasinec", "42", "Jožefa", "Marec 6./7.; oče Peter Starašinič ½ zemlj. (17.8 881; por. 4.2.1907) × Marija Starašinič (25/7/875); botra Jurij Klepec + Bara Županič km. hči; babica Marija Piletič; podpis Učak d.i.; marg. umrla 25.7.1999 Notranje gore?"),
    (18, "Krasinec", "23", "Marija", "Marec 25./26.; EMŠO ž. 2503915505294; oče Matija Starašinič ½ zemlj. (7.1.1873; por. 10.11.1903) × Marija roj. Starašinič (11.3.1885); botra Jurij Klepec + Ana Perdivec km. žena; babica [Ana Starašinič? ~]; podpis Kapl. Bitnar; marg. umrla 08.04.1999 Novo mesto"),
    (19, "Dobravice", "11", "Ivana", "Marec 28.?/29. [~]; EMŠO ž. 2803915505174; marg. »24.4.1932«? [~ — poznejši vpis?]; oče Janez Žungelj ½ zemlj. (15/1883; por. 5.2.1906) × Margareta roj. Kambič (17.3.881); botra Janez Žungelj + Katarina Markinović; babica Marija Piletič; podpis Valerijan Učak d.i.; marg. poročen 22.2.1938 + mož? umrl 15.3.1983"),
    (20, "Podzemelj", "45", "Stanislav", "Marec 21.?/1. aprila [EMŠO 2103 → roj. 21.3.! krsta 1.4.]; EMŠO ž. 2103915500040; oče Jožef Šimec, MRLI. MOJSTER × Ana roj. Žungelj; botra Martin Skala ½ zemlj. + Ana Röthel prostovoljka; babica Marija Piletič; podpis Valerijan Učak d.i.; marg. poročen 24.4.1946 v Vrbasu?"),
    (21, "Gradac", "10", "Vilhelm", "April 5./6.; ‡ 9/7 1916; kraj: nadpis »Gradac« + temnejši »Vrhhova?« [~ — d5 3×; dva zapisa!]; oče Anton Sakša, GOSTILNIČAR (15/877; por. 22.10.1900) × Ana roj. Župec (13/85); botra Franc Recher c.k. oruž? + Marija Recher; babica Marija Piletič; podpis Valerijan Učak d.i."),
    (22, "Gradac", "60", "Rudolf Feliks", "April 2./7.; oče Alojzij Mavar, c.k. orožnik v.p. (11/875; por. 9.8.1909) × Rozalija Marentič (2.9.1883); botra Franc Kurent c.kr. sod. sluga + Marija Kurent; babica Ana Marentič; podpis Kapl. Bitnar"),
    (23, "Krasinec", "19", "Ana", "April 7./7.; ‡ 22/7 1916; oče Peter Kambič ½ zemlj. (17/6 1879; por. 11.2.1901) × Marija roj. Jurajevičič (28.8.882); botra Janez Županič + Ana Kambič gostilničarka; babica Ana Brodarič? [~]; podpis Kapl. Bitnar"),
    (24, "Cerkvišče", "2", "Jožef", "April 8./9.; marg. † 11.5.1919? [~]; oče Peter Starašinič ½ zemlj. (21.3.1881; por. 3.4.1904) × Marija roj. Jakofčič (27.4.1881); botra Peter Jakofčič + Ana Jakofčič; babica Margareta Jakofčič; podpis Kapl. Bitnar"),
    (25, "Grm", "28", "Angela", "April 9./10.; EMŠO ž. 0904915505143; kraj »Gm« = GRM (okrajšava — POTRJENO prek matičnega območja v parish.ts!); oče Nikolaj Pezdirc pol zemljak (2/11-1881; por. 12/2-1906) × Marija roj. Klaserić (21/1-1882); botra Janez Pezdirc + Anžela Pezdirc; babica Marija Piletič; podpis Kapl. Bitnar; marg. umrla 18.10.1993 + 2× poročena (10.2.1944 + 6.2.1948)"),
    (26, "Cerkvišče", "11", "Jožef", "April 4./12.; + 4.4.1924; oče Jurij Husič bajt. zemljak (17/12 1879; por. 22/4-1907) × Ana roj. Kralj (11/5-1882); botra Jurij Jakofčič + Bara Jakofčič; babica Marija Mihelič nj.zp.; podpis Kapl. Bitnar"),
    (27, "Klojter", "83", "Ana", "April 15./16.; + 21/4 1916; oče Franc Berkopic ½ zemljak (2/4-1873; por. 4/4-1898) × Ivana roj. Županič (10/10-1874); botra Julij Kočevar + Ana Kočevar; babica Marija Piletič; podpis Kapl. Bitnar"),
    (28, "Krivoglavice", "29", "Alojzija", "April 13./18.; EMŠO ž. 1304915505131? [~]; oče Jurij Kralj ½ zemljak (30.11.1880; por. 18.1.1908) × Katarina roj. Muc (16.3.1886); botra Anton Žnidaršič + Katarina Žnidaršič; babica Marija Piletič; podpis Kapl. Bitnar; marg. mož Augustin Sinzon? † 27.8.1980 + umrla 10.12.1988 + poročena 15.8.1938"),
    (29, "Primostek", "8", "Ana", "April 17./18.; EMŠO ž. 1704915505156; oče Janez Auc ½ zemlj. (23/8-1875; por. 4/2-1907) × Ana Rus (2/5-1888); botra Jožef Holek + Marija Holek; babica Ana Marentič; podpis Kapl. Bitnar; marg. umrla 11.06.1988"),
    (30, "Gradac", "93", "Johana", "April 28./29.; EMŠO ž. 2804915505790; VELIKA RTK NALEPKA (s273; s274 dup brez!): RTK Podzemelj 1915/228-30, sprejeta v državlastvo RS 22.5.1992, vpis prenešen v matični register z pripisom DOLIČ, 10.1.2006 Vesna Šimonič; oče † Daniel Jakša, mizar (roj. 12/8-1881, † 9.12.1915!) × Mikla? Župančič [~] (16/2 1880; por. 15.8-1903); botra Franc Gral? [~] lončar + Marija Gral; babica Ana Marija? Piletič [~]; podpis Kapl. Bitnar"),
    (31, "Kapljišče", "6", "Ana", "April 29./30.; EMŠO ž. 2904915505221; oče Janez Jurajevičič ½ zemlj. (3.12.1876; por. 15.5.1905) × Marija roj. Sodja (31.5.1885); botra Matija Tome ½ zemlj. + Marija Tome; babica Marija Piletič; podpis Valerijan Učak d.i.; marg. umrla 10.04.1991 + poročena 10.9.1939"),
    (32, "Gradac", "32", "Stanislav", "Maj 3./5.; oče Anton Frec ½ zemlj. (9.6.870; por. 25.1.98) × Marija r. Kočevar (8.1.879); botra Julij Kočevar + Ana Strugar kovač. žena; babica Marija Piletič; podpis Valerijan Učak d.i."),
    (33, "Gradac", "64", "Ivan", "Maj 7./7.; marg. »+ 12/5 1915« = † 12.5.1915?? [~ — † na dan krste?! ali 12/5 = drug datum; ZOOM]; oče Franc Hovačič bajt. židár (2/3/883; por. 3.2.1908) × Marija r. Plut (6.3.889); botra Martin Hovačič mizar + Amalija Hovačič; babica Marija Piletič; podpis V. Valerijan Učak d.i."),
    (34, "Krasinec", "14", "Ivan", "Maj 8./9. [~ krsta]; NEZAKONSKI — mati Marija Galovec (9/12-1889) v očetovi koloni; VELIKA MARGINALIA OČETOVSTVA: »Janez Križan se je pred podpisanimi pričami spoznal kot očeta tega otroka, kar je tudi podpisana mati potrdila ter zahteval, da se zapiše v krstno knjigo. V Podzemlju, 4. februarja 1918. Janez Križan, oče. Marija Galovec, mati. Miho Starašinič, priča. Miho Starašinič, priča. V. Valerijan Učak ž.u.« (d21 2×!); botra Anton Jaklič ½ zemlj. + Ana Jaklič; babica Marija Piletič; podpis Kapl. Bitnar; marg. umrl 26.10.1979 Novo mesto + poročena 1929? [~]; FORENZIČNA VEZAVA: Janez Križan (r. 6.3.1872) = oče r41 (Otok 19 Marija, ž. Marija Husič)!"),
    (35, "Dobravice", "19", "Johana", "Maj 8./10.; EMŠO ž. 0805915505021; oče Janez Žungelj? ½ zemlj. (21/10-1864; por. 20/8-1893) × Neža Plut (20/5-1872); botra Janez Plut ½ zemlj. + Katarina Žungelj?; babica Marija Klasovec? n.zp. [~]; podpis Kapl. Bitnar; marg. Zelmanec Štefant Jožef † 8.11.1940 + poročen 2.2.1946 + umrla 27.08.1993 Dvorje"),
    (36, "Krasinec", "8", "Ana", "Maj 25./26.; EMŠO ž. 2505915505028? [~]; marg. dovoljenje opčine rudovac 01.03.1958 = VPIS PRENEŠEN [~]; oče Matija Cajnar ½ zemlj. (12.4.1879; por. 12.4.1914) × Ana roj. Brodarič (8.12.1885); botra Jožef Brodarič + Marija Crnič? [~]; babica Ana Brodarič nj.zp.; podpis Kapl. Bitnar; marg. umrla 04.4.1988 + poročena 10.11.1939"),
    (37, "Boršt", "23", "Antonija", "Maj 26./26. — DVOJČEK 1 (dvojčka z r38, identični starši!); oče ‡ Mihael Perdivec [~ — 6× d26b], ½ zemlj., roj. 22.11.1873 (OBE celice 1873 — faza-1 »1875« kolizija REŠENA!), ‡ 28.III. 1915 = MAREC (2 meseca PRED rojstvom dvojčkov — faza-1 »november« POPRAVLJENO!) (por. 26.5. 1902) × Marija roj. Štravs (7.8.1878); botra Jurij Rožman ½ zemlj. + Katarina Štravs ros. žena; babica Barbara Marentič; podpis V. Valerijan Učak d.i."),
    (38, "Boršt", "23", "Alojzij", "Maj 26./26. — DVOJČEK 2; marg. »+ 25/3 1916« = † 25.3.1916; kraj: pisar začel pisati »Alojzij« v koloni kraja in POPRAVIL (prečrtano ime pod »Boršt«!); starši identični r37 (‡ Mihael Perdivec 22.11.1873 ‡ 28.3.1915 × Marija Štravs); botra Jurij Rožman + Katarina Štravs; babica Barbara Marentič; podpis V. Valerijan Učak d.i."),
    (39, "Otok", "38", "Marija", "Maj 29./30.; EMŠO ž. 2905915505090; oče Matija Križan ½ zemlj. (15/892; por. 7.7.1913) × Barbara Kambič (4.8.891); botra Miko Kambič pos. gostilničar? + Jožefina Novak pos. žena; babica Marija Piletič; podpis V. Valerijan Učak d.i.; marg. umrla 20.04.1995 + poročena 22.2.1938"),
    (40, "Gradac", "79", "Anton", "Junij 8./9.; MARGINALIA: »razglašen za mrtvega dne 17.6.1942 od okrožnega sodišča … dne 31.3.1949 Štukovnica? - matičar« (2. razglašen-za-mrtvega vpis vzorca — cf. P96 r60!); oče Ludovik Schweiger Kamnossek [plemiški!] × Ana Vrbas; botra Jakob Stipanič, ŽUPAN + Ana Pezdinec ros. žena; babica Marija Piletič; podpis V. Valer. Učak d.i."),
    (41, "Otok", "19", "Marija", "Junij 9./11.; oče Janez Križan ½ zemljak (6.3.1872; por. 1.6.1908) × Marija Husič (28/10 886) — ISTI Janez Križan kot r34 očetovstvo!; botra Mihael Moravec posrednik + Marjeta Kure pos. žena; babica Marija Piletič; podpis V. Valer Učak d.i.; marg. umrla 22.6.1974 + poročena 26.6.1938"),
    (42, "Zemelj", "21", "Bara", "Junij 20./21.; ‡ 12.3.1918; oče Janez Auc? [~ Huc/Auc — cf. r29 Janez Auc r. 1875; tukaj 28.11.1873] ½ zemljak (por. 22.1.1900) × Marija roj. Hafnik? [~] (2.11.1882); botra Miko Jaklič ½ zemlj. + Ana Jaklič pos. žena; babica Alela? Auc n.zp. [~]; podpis Kapl. Bitnar"),
    (43, "Cerkvišče", "4", "Jožefa", "Junij 30. / Julij 1.; EMŠO ž. 3006915505701 (d19!); NEZAKONSKI — mati Ivana Gregorič, posrednika? sam. hči (v očetovi koloni); VELIKA MARGINALIA OČETOVSTVA: »Jožef Željko, posrednik, se je pred podpisanimi pričami spoznal kot očeta tega otroka, kar je tudi podpisana mati potrdila, ter je zahteval, da se zapiše v krstno knjigo. V Podzemlju, 15. avgusta 1918. Jožef Željko, oče. Ivana Gregorič, mati« + priče Jože Grabrijan + Janez Grabrijan + dno strani: »sta se Jožef Željko in Ivana Gregorič dne 6. januarja 1918 poročila«; botra Jurij Grabrijan pol zemlj. + Terezija Grabrijan; babica Ana Marentič; podpis Kapl. Bitnar; marg. mati pozneje poročena s Pezdircem Martinom († 10.6.1983 Novo mesto)"),
    (44, "Vranoviče", "2", "Marija", "Julij 1./4.; ‡ 25/2 1916; oče Jožef Jahša? [~ Jakša] pol zemljak (3.1.1884; por. 9.5.1910) × Ana r. Grahek (9.1.1895); botra Jakob Spritzer posrednik + Terezija Holberin? [~]; babica Marija Piletič; podpis V. Valerijan Učak d.i."),
    (45, "Podzemelj", "10", "Andrej", "Julij 1./8.; + 26/8 1916; oče Andrej Ruscher, trgovec (26.11.1885; por. 28.8.1911) × Ana r. Sevček (26.6.1882); botra Friderik Klušček trgovec + Josipina Klušček; babica Marija Piletič; podpis V. Valerijan Učak d.i."),
    (46, "Krasinec", "18", "Anton", "Julij 17./17. — DVOJČEK 1; † 4.8.1915 (star 18 dni!); **marg. ob datumih: »½ 7h ante meridiem« = roj. ob 6:30 ZJUTRAJ (d13 3× — PRVE URE ROJSTVA V VZORCU!)**; oče Mikl? Županič [~] ½ zemljak (9/9-1865; por. 29/4-1906) × Ana r. Brodarič (31/7-1882); botra Jurij Klepec posrednik št. 36 + Bara Katarina Klepe? prič. 36 [~]; babica Bara Marentič; podpis Kapl. Bitnar"),
    (47, "Krasinec", "18", "Alojzij", "Julij 17./17. — DVOJČEK 2; † 25.7.1915 (star 8 dni!); **marg.: »7h a.m.« = roj. ob 7:00 (½ ure za bratom!)**; starši identični r46 (Mikl? Županič × Ana Brodarič); botra Jurij Klepec posred. št. 36 + Katarina Klepe prič. 36 [~]; babica Bara Marentič; podpis Kapl. Bitnar"),
    (49, "Gradac", "95", "Emil, Filip, Leopold", "Julij 12./26. (d7!); oče Bohumil Špoušek? [~], Polk.? us meriler? [~ — **»evang. reform.« = PROTESTANT (edini v vzorcu!)**] × Leopoldina roj. Trobec (katol.) — MEŠANA VERA; botra Joh. Frischmolar? [~], Resident K.K. Štaotih? [~] + Štefej? Amalija [~]; babica Marija Piletič; podpis Kapl. Bitnar"),
    (50, "Grm", "53?", "Antonija", "Julij 28./29.; + 2/9 1916; kraj »Gm« = Grm; hiša 53? [~ — dno strani natrano, d4]; oče Janez Kure ½ zemljak (29/4-1869) × Bara Majič? [~]; botra Miko Kure posrednik + Marija Kure njeg žena; babica Alojzija? Piletič [~]; podpis Kapl. Bitnar"),
    (51, "Gradac", "18", "Neža", "Julij 29./30.; EMŠO ž. 2907915505020; marg. priimek: »Priimek Perdavec spremenjen v nov priimek Pecolín? Odločba NSF št. 02/06-16-5-20103-2543/96 z dne 25.11.1999« [~]; oče Anton Pezdirec ½ zemljak (30.8.1877; por. 14.5.1900) × Neža r. Stipanič (21.1.1878); botra Matija Fital? [~] pos. ½ zemljak + Katarina Murn posest. vdova; babica Marija Piletič; podpis V. Valerijan Učak d.i.; marg. umrla 12.05.2004 Črnomelj + MB/Lju 23.12.1939"),
    (52, "Cerkvišče", "25", "Antonija", "August 1./2.; EMŠO ž. 0108915505450; oče Anton Starašinič ½ zemljak (30.5-1876; por. 14.5-1899) × Ana roj. Lukanič (17.11-1874); botra Janez Mravinec posred. + Anžela Grabrijan posed žena; babica Marija Piletič; podpis Kapl. Bitnar; marg. umrla 4.7.1987 + poročena 3.8.1936"),
    (53, "Primostek", "15", "Marija", "August 3./4.; EMŠO ž. 0308915505045; NEZAKONSKI — mati Marija Tome (26/11-1895); VELIKA MARGINALIA OČETOVSTVA: »Josip Jager, sobni slikar, se je pred podpisanimi pričami spoznal kot očeta tega otroka, kar je tudi podpisana mati potrdila, zahteval, da se zapiše v Krstno knjigo. V Podzemlju 18.4.1917. Josip Jager, oče. Marija Tome, mati. Jože Tome? priča. Miho Jaklič, priča. V. Valerijan Učak ž.u.« (d20! — **18.4.1917, ne 1918!**) + »sta se Jožef Jager in Marija Tome dne 18. aprila 1917 poročila« (poroka ISTI DAN!) + VPIS PRENEŠEN 17.11.2007; botra Jožef Brovar? [~] organist + Ana Brine; babica Katarina Jurjevčič meršpr.? [~]; podpis [Štomhmut? ~] Bitnar [~]; marg. doma očetov značaj za vojsko 19.11.1946 + umrl 19.12.1972 Kostanjevica + poročen 13.9.1937"),
    (54, "Krasinec", "37", "Alojzij", "August 6./6.; EMŠO ž. 0608915500054; oče Jurij Klepec posr. ½ zemlj. (22.4.1867; por. 15.2.1897) × Marija r. Tome (12.1.1872); botra Miko Županič posrednik? + Marija Starašinič poso. žena; babica Ana Brodarič n.zp.; podpis V. Valerijan Učak d.i.; marg. poročena 25.11.1992? [~] + umrla 23.08.1989"),
    (55, "Gradac", "2", "Janez", "August 15./17. (d8! — faza-1 »14« POPRAVLJENO); ‡ 23.3.1933; oče Janez Novak ½ zemlj. (16/6-1890; por. 5/2-1912) × Marija roj. Jakša (7/12-1891); botra Jakop Jerman posrednik + Marija Jerman tega žena; babica Marija Plohič? [~]; podpis Kapl. Bitnar"),
    (56, "Boginja vas", "15", "Mihael", "August 17./18.; + 4.11.1915; NOVA VAS vzorca (register »Božinja vas«; uradno Boginja vas/Bojanja vas — cf. marg. r63 »Bojanj«!); oče Miko Brodarič ½ zemlj. (15/5 1875; por. 10/5-1896) × Ana roj. Šuštarič (9/12-1873); botra Miko Galovec posrednik + Bara Šuštarič posed žena (GALOVEC — cf. r34 mati!); babica Marija Brodarič n.zp.; podpis Kapl. Bitnar"),
    (57, "Gradac", "1", "Maksimilijan Avguštin", "August 27./27.; EMŠO ž. 2708915172652? [~ netipičen]; oče Franc Recher, c.kr. stražmaster × Marija Luheč? [~]; botra Josip Pregl? [~] c.kr. stražmaster v.p. + Marija Pregl nj. žena; babica Marija Piletič; podpis V. Valerijan Učak d.i.; marg. poročen 31.8.1946 + mrtvi 4.11.1948 Tuzla? [~]; cf. r21 botra Franc Recher!"),
    (58, "Vranoviče", "1", "Anton", "August 27./28.; EMŠO ž. 2408915500168; oče Anton Županič ½ posestnik (28.4.1884; por. 25.11.1912) × Marija r. Fink (11.8.1893); botra Eduard Županič, ŽELEZ. DELAVEC + Marija Fink posest. žena; babica Marija Piletič; podpis V. Valerijan Učak d.i.; marg. umrl 08.11.1995 Golnik + porožen 29.4.1950 Metlika"),
    (59, "Krasinec", "2?", "Janez", "September 11./12.; EMŠO ž. 1109915500012; hiša 2? [~ — d10c 7×: ena št. »2.«, marg »Maticar« prekriva; faza-1 »74« ZAVRŽENO]; oče Janez Pezdirc ½ posrednik? [~] (25.6.1879; por. 18.5.1903) × Marija Simonič (21.6.884); botra Peter Pezdirec ½ z. posestnik + Marija Pezdirec; babica Bara Marentič; podpis Valerijan Učak d.i.; marg. zakonska zveza sklenjena 17.3.1960 + umrl 18.08.1997? + poročen 7.1.1945"),
    (60, "Dobravice", "26", "Franc", "September 14./19. (d9!); ‡ 18/8 1917; oče Jožef Rus ½ z.p. (24.1.1876; por. 27.7.1903) × Barbara r. Vogrin (25.9.1883); botra Martin Gornik ½ z. pos. + Rus Marjeta sam. dku. [~]; babica n.zp. Marija Vogrin; podpis V. Valerijan Učak d.i."),
    (61, "Gradac", "15", "Julij", "September 17./19.; EMŠO ž. 1709915500040; oče Matija Marentič (29.1.1870; ½ z. posest.; por. 2.10.1911) × Ana r. Štravs (14.8.1881); botra Anton Pezdirec ½ z. + Katarina Štravs sam. delka [~]; babica Marija Piletič; podpis V. Valerijan Učak d.i.; marg. umrl 17.05.2001 Gradac + poročen 30.8.1944"),
    (62, "Klojter", "35", "Antonija", "September 26./27.; EMŠO ž. 260991550501? [~]; oče Franc Šober (3.11.1875; malt. posest.? [~]; por. 27.1.1902) × Marija r. Škala (15.9.1878); botra Martin Škala ½ z. pos. + Ivana Berkopce? pos. žena [~]; babica Marija Piletič; podpis V. Valerijan Učak d.i.; marg. Gradac 12.12.1955 + poročena 26.10.1938"),
    (63, "Grm", "36", "Alojzija", "Oktober 8./9.; EMŠO ž. 0810915305022? [~ netipičen]; kraj »Gm« = Grm (2. vpis Grma!); VELIKA MARGINALIA: »Graduana? ruka izmuzena? … podiga Bojanj? št. E-ž 16955-57 z dne 10.11.1953« + zaposlan 14.8.1971 + poročena 23.11.1939 Zagreb + zakonska zveza 24.7.1951 Štrenice? (RNK grad Zagreb) + gradac 10.4.1952 Maticar; oče Matija Baiuk ½ zemljak (22/5-1872; por. 25/11-1900) × Johana roj. Badena? [~]; botra Nikolaj Kure posestnik + Marija Kure; babica Ana Marentič; podpis Kapl. Bitnar"),
    (64, "Vranoviče", "10", "Ana", "Oktober 10./12.; marg. »+ 12.4.1937 (v Bosanskom ostrovcu?)«; oče Jožef Kambič ½ zemljak (25-1879; por. 12/10-1903) × Ana roj. Hlavace (18/12-1882); botra Martin Jakša posestnik + Neža Potrčnik posed žena; babica Marija Piletič; podpis Kapl. Bitnar"),
    (65, "Otok", "11", "Marija", "Oktober 20./21.; EMŠO ž. 2010915505131; oče Janez Jurajevčič posrednik ½ z. (23.09.1872; por. 8.5.1905) × Marija r. Pezdirc (25.1.1882); botra Jožef Pezdinec posest? + Marija Pezdinec; babica Marija Piletič; podpis Kapl. Bitnar; marg. umrla 27.03.2004 + poročena 22.2.1943"),
    (68, "Vranoviče", "11", "Martin", "November 5./7.; + 16.3.1916; oče Franc Schweiger, posest. ½ z. (26.1.1872; por. 20.4.1892) × Ana roj. Strah (25.7.1876) — cf. r40 Ludovik Schweiger Kamnossek (Gradac!); botra Janez Kerbavec pos. ½ z. + Ana Kerbavec; babica Marija [~]; podpis V. Valerijan Učak d.i. [~]"),
    (70, "Boginja vas", "15", "Amalija", "November 7./8.; ‡ 10.9.1918; **ISTA hiša 15 kot r56 (d41 4× POTRJENO!) = NARE PRELOM — 2 gospodinjstvi v isti hiši isto leto (3. prelom vzorca: cf. P104 + P108 h31!)**; oče Peter Kralj, posest ½ zemlj. (20/10-1879; por. 12/2-1906) × Ana roj. Berkopce (3/4-1885); botra Martin Šapič posred. + Ana Šapič istega žena; babica Bara Marentič; podpis Kapl. Bitnar"),
    (71, "Otok", "16", "Anton", "November 9./11.; EMŠO ž. 0911915500064; oče Nikolaj Novak posest ½ z. (25.9.1877; por. 22.11.1907) × Ana roj. Pezdirec (12.3.1889); botra Martin Pezdirec posest + Ana Zdajtič kovač. žena; babica Marija Piletič; podpis V. Valerijan Učak d.i.; marg. poročen 15.7.1945 + umrl 21.05.1958? [~]"),
    (73, "Gradac", "25", "Ferdinand", "November 20./21.; EMŠO ž. 2011915330001? [~]; NEZAKONSKI (očetova celica PRAZNA/raztrgana); mati Antonija Petrovčič, sam. dekle; botra Julij Beličič? [~] posest + Margareta Stipanič samsko dekle; babica Marija Piletič; podpis V. Valerijan Učak [~]; marg. umrla 24.9.1957 Trnovo-Zagreb + zakonska zveza razveljavljena sodbo Zagreb št. T2 765/75-8 (10.10.1975) + Gradac 22.04.1955"),
    (75, "Dobravice", "16", "Neža", "November 24./27.; EMŠO ž. 2411915505047; oče Martin Matkovič ½ posest (27/1-1885; por. 22/2-1909) × Ana roj. Tome (9/3-1890); botra Anton Hrobdnik? [~] posrednik + Marija Hrobdnik; babica Ana Žungelj neizp.; podpis Kapl. Bitnar; marg. umrla 17.08.2001 + poročena 12.4.1920 + mož umrl 22.09.1940"),
    (76, "Boršt", "21", "Terezija", "December 6./12.; EMŠO ž. 0612915505126; oče Andrej Derganc posest. ½ z. (3.11. 1869? [~ — tudi »1885« prečrtano]; por. 26.10.1903) × Barbara roj. Klepec (11.3.1885); botra Martin Derganc posest + Katarina Derganc posest žena; babica Barb. Marentič; podpis Valerijan Učak d.i.; marg. mož umrl 15.7.1997 Metlika + poročena 11.3.1959 + umrla 10.10.2004 Metlika"),
    (77, "Primostek", "2", "Janez", "December 13./15.; ‡ 8/10 1916; oče Janez Bajuk posest ½ z. (23.11.1874; por. 9.5.1910) × Terezija r. Pezdirec (29.5.85? [~]); botra Matija Pezdirec posest + Marija Pezdirec; babica Marija Piletič; podpis V. Valerijan Učak d.i."),
    (79, "Boršt", "20", "Amalija", "December 20./21.; EMŠO ž. 2012915505142; NEZAKONSKA (očetova celica PRAZNA); mati Ana Filak (24/1-1891); botra Jure Kralj posest. + Katarina Grabrovie? [~] samska; babica Bara Marentič; podpis Kapl. Bitnar; marg. umrla 17.01.2002 Novo mesto + poročena 20.2.1933"),
    (80, "Krasinec", "21", "Marija", "December 26./27.; EMŠO ž. 2612915505409? [~]; oče Mihael Jurajevčič ½ z. posest. (1.7 1877; por. 22.5.1905) × Marija r. Bahorič (22.10.1886); botra Janez Jurajfčič? [~] posest. + Marija Jakofčič posest. žena; babica Marija Jurajevčič neiz.; podpis Valerijan Učak d.i.; marg. priimek spremenjen v Jurgeveič? (odločba 24.10.1973) + VPIS PRENEŠEN 14.11.2004"),
    (81, "Gradac", "96", "Stefanija", "30. december 1915. / 4. januar 1916. (rojstvo/krsta ČEZ MEJO LETA!); EMŠO ž. 3012915505170; **starši (OFFSET PORAVNAVA — 5 celic = 5 vrstic; d11b!): oče Franc Copri [~], goj. želežniški čuvaj, roj. 14.2.1880 (por. 31.7.1905) × mati Alojzija roj. Vidmar, 14.4.1881; botra Janez Pleš, žel. uslužbenec + Ana Kočevar, posed žena; babica Marija Piletič; podpis V. Valerijan Učak d.i.**; marg. »s pravnomočno sodbo okrožnega sodišča v Mariboru št. P.29/52-5 z dne 6.4.1962 je zakonska zveza razveljavana…« + VPIS PRENEŠEN 14.11.2004 + poročena 5.8.1939"),
]

excluded = [{"row": r, "village": v, "houseNo": h, "child": c, "note": n}
            for (r, v, h, c, n) in EX_META]
excluded.sort(key=lambda x: x["row"])

doc = {
    "phase": "P110",
    "type": "parish-baptism-year-transcription",
    "status": "SAMPLE-TRANSCRIPTION-1915",
    "issuedAt": "2026-10-19",
    "source": "matricula-online 04105 (krstna knjiga župnije Podzemelj)",
    "method": "forenzični zoomi s269–s283 (15 skenov / 13 strani; 2 dup para) — grid ruler kalibracija 100px (popravljen track-scale: A/B polstrani 1:1, y-centri iz grid) + L/S/R celice 3–5× + 42 dvom-izrezov (d1–d42) + dup s271/s274; offset poravnava starševskih celic str. 237 rešena s 5=5 preštevanjem + s284-B kontrola",
    "frame": {
        "yearStart": 1915,
        "yearEnd": 1915,
        "rowsTotal": 81,
        "rowsStruck": 0,
        "rowsNote": "brez prečrtanih; r81 = rojstvo 30.12.1915 / krsta 4.1.1916 (čez mejo!); glava 1915 ročno na VRHU str. 225 = s269; glava 1916 ročno »1916.« INLINE v LOČILNI starševski celici str. 237 = s283 (zrcali tiskani »Leto« header na L-strani!) — tiskana glava »Leto 1916« = vrh str. 238 = s284",
        "pages": [225, 237],
        "scans": [269, 283],
        "dupPari": [[270, 271], [273, 274]],
        "dupPariNote": "samo 2 dup para (po rekordih P108/P109); s271 DUP RAZKRIVA r13 (s270 pokrit z nalepko); s274 DUP razkriva r30 (Gradac 93 Johana)",
        "pageOfScan": {"269": 225, "270": 226, "271": 226, "272": 227, "273": 228, "274": 228, "275": 229, "276": 230, "277": 231, "278": 232, "279": 233, "280": 234, "281": 235, "282": 236, "283": 237},
        "rowsPerPage": {
            "225": "glava 1915 (ročno) + r1–r9",
            "226": "r10–r16",
            "227": "r17–r24 (+ April glava med r20/r21)",
            "228": "r25–r30 (+ RTK nalepka r30)",
            "229": "r31–r37 (+ maj glava med r31/r32)",
            "230": "r38–r43 (+ junij glava med r39/r40)",
            "231": "r44–r50 (+ julij glava na vrhu)",
            "232": "r51–r56 (+ august glava med r51/r52)",
            "233": "r57–r62 (+ september glava med r58/r59)",
            "234": "r63–r68 (+ oktober glava na vrhu + november med r66/r67)",
            "235": "r69–r73",
            "236": "r74–r79 (+ december glava med r75/r76)",
            "237": "r80–r81 + »Leto« ločilo + ročna glava »1916.« + 1916 r1–r3"
        }
    },
    "entries": G,
    "excluded": excluded,
    "excludedCount": len(excluded),
    "anomalies": [
        {"id": "A1", "row": "r37/r38", "type": "dvojčki+oče-umrl-pred-rojstvom", "note": "Boršt 23: dvojčka Antonija + Alojzij (oba 26./26. maj) — oče ‡ Mihael Perdivec † 28.III.1915 (MAREC — 2 meseca PRED rojstvom!; faza-1 »november« POPRAVLJENO); roj. 22.11.1873 v OBEH celicah (faza-1 kolizija 1873/1875 REŠENA)"},
        {"id": "A2", "row": "r46/r47", "type": "dvojčki+ure-rojstva", "note": "Krasinec 18: dvojčka Anton + Alojzij (oba 17./17. julij) — marg. LATINSKE URE: »½ 7h ante meridiem« (6:30) + »7h a.m.« (7:00) = PRVE URE ROJSTVA V VZORCU; oba † 1915 kot dojenčka (18 dni / 8 dni!)"},
        {"id": "A3", "row": "r34+r41", "type": "očetovstvo+vezava", "note": "r34 (Krasinec 14 Ivan, mati Marija Galovec) — očetovstvo Janez Križan priznano 4.2.1918 (priča Miho Starašinič ×2) — ISTI Janez Križan (r. 6.3.1872, ž. Marija Husič) = oče r41 (Otok 19 Marija)!"},
        {"id": "A4", "row": "r43", "type": "očetovstvo+poroka", "note": "Cerkvišče 4 Jožefa (mati Ivana Gregorič) — očetovstvo Jožef Željko, posrednik, priznano 15.8.1918; starši poročeni 6.1.1918 (dno str. 230); mati pozneje poročena s Pezdircem Martinom († 10.6.1983)"},
        {"id": "A5", "row": "r53", "type": "očetovstvo+poroka-isti-dan", "note": "Primostek 15 Marija (mati Marija Tome) — očetovstvo Josip Jager, sobni slikar, 18.4.1917 + poroka ISTI DAN 18.4.1917 (faza-1 »1918« POPRAVLJENO); priča Jože Tome + Miho Jaklič"},
        {"id": "A6", "row": "r73+r79", "type": "nezakonski-oče-prazen", "note": "r73 (Gradac 25 Ferdinand, mati Antonija Petrovčič sam. dekle — celica raztrgana) + r79 (Boršt 20 Amalija, mati Ana Filak — celica PRAZNA)"},
        {"id": "A7", "row": "r56+r70", "type": "nare-prelom", "note": "Boginja vas 15 ×2 v istem letu (r56 Brodarič × Šuštarič + r70 Kralj × Berkopce — d41 4×!) = 2 gospodinjstvi v isti hiši = NARE PRELOM (3. v vzorcu: cf. P104 + P108 h31) — NOVA vas!"},
        {"id": "A8", "row": "r17", "type": "vrzel-rekord", "note": "h78: 1888 → 1915 = VRZEL 27 LET = NOV REKORD vzorca (prej h53 16 let)"},
        {"id": "A9", "row": "r30+r37/38", "type": "očeta-†-1915", "note": "2 očeta umrla v 1915: r30 Daniel Jakša, mizar († 9.12.1915 — Johana roj. 28.4.) + r37/38 Mihael Perdivec († 28.3.1915 — pred rojstvom dvojčkov) = 3 otroci brez očeta"},
        {"id": "A10", "row": "r49", "type": "protestant+mešana-vera", "note": "Gradac 95 Emil Filip Leopold — oče Bohumil Špoušek? [~] »evang. reform.« = EDINI protestantski oče vzorca × katol. Leopoldina Trobec; trojno ime; botra Joh. Frischmolar? Resident"},
        {"id": "A11", "row": "r40", "type": "razglašen-za-mrtvega", "note": "Gradac 79 Anton — »razglašen za mrtvega dne 17.6.1942 od okrožnega sodišča … 31.3.1949« (2. tak vpis — cf. P96 r60); oče Ludovik Schweiger Kamnossek (plemiški) + botra Jakob Stipanič ŽUPAN"},
        {"id": "A12", "row": "r69", "type": "zakon-razveljavljen", "note": "Griblje 46 Martin — poroki 19.1.1952 + 19.3.1961 (Karlovci) + zakonska zveza RAZVELJAVLJENA sodba št. K 757/65-10 (2.12.1965, Karlovci) + umrl 15.5.1992 Karlovci [~] — prvi razveljavljen zakon v vzorcu"},
        {"id": "A13", "row": "r25/r50/r63", "type": "nova-vas-Grm", "note": "kraj »Gm« ×3 = GRM (okrajšava — POTRJENO prek matičnega območja v parish.ts!) — hiša 28 + 53? + 36; NOVA vas vzorca (cf. Boginja vas r56/r70)"},
        {"id": "A14", "row": "r81", "type": "offset-poravnava+meja-leta", "note": "r81 = rojstvo 30.12.1915 / krsta 4.1.1916 (čez mejo); starši rešeni s OFFSET poravnavo (5 celic = 5 vrstic + s284-B kontrola): Franc Copri, goj. želežniški čuvaj × Alojzija Vidmar; glava 1916 ročno v ločilni celici"},
        {"id": "A15", "row": "r12/r13", "type": "urejenost-po-krsti+false-start", "note": "prečrtan »April« nadpis na str. 226 = pisarjev false start (d6a!); register urejen po DATUMU KRSTE (r12 krsta 3.3. = r11; r13 EMŠO 0503 = 5.3.) — prvi dokaz urejenosti po krsti"},
        {"id": "A16", "row": "r51", "type": "priimek-spremenjen", "note": "Gradac 18 Neža — »Priimek Perdavec spremenjen v nov priimek Pecolín? Odločba NSF 25.11.1999« [~] + r80 priimek spremenjen v Jurgeveič? (24.10.1973) = 2 spremembi priimkov"},
        {"id": "A17", "row": "r16", "type": "popravki-faza-1", "note": "mati = Marija PEZDIREC (ne Perdivec!); EMŠO 1603915505171 (ne 5505141); oče roj. 15.7.1883 (ne 1888); marg. »mož umrl 1994« (ne »oče«)"},
        {"id": "A18", "row": "r48/r72", "type": "familija-Jakobčič", "note": "h13 oče Matija JAKOBČIČ (r. 1856, star 59!) + h9 oče Oswald JAKOBČIČ (r. 1889) + h9 babica Marija Jakobčič = familija Jakobčič v Gribljih (faza-1 »Jaklič/Jakobeč« POPRAVLJENO)"}
    ],
    "stats": {
        "entries": 11,
        "distinctHouses": 11,
        "housesWritten": 11,
        "housesIllegible": 0,
        "geneticHouses": 11,
        "newSampleHouses": 0,
        "newHouseNos": [],
        "intraYearRepeats": 0,
        "intraYearRepeatsNote": "NARE 11/11 — 10. čisto leto! (h53 ZAPORED 2. leto čez leta 1914/15); NARE PRELOM samo v NOVI vasi Boginja vas (h15 ×2 — ne šteje v Griblje NARE)",
        "pt": "8/3 (h45 + h46 + h53 v luknji 41–60 — vse tri dokazane v PT_GAP_KNOWN!)",
        "vitals": 490,
        "cumulative": "498 vpisov / 87 hiš / 30 let (1886–1915)",
        "gaps": "h78 27 LET (rekord!) + h32 6 + h88 5 + h22/h40/h45/h70 3 + h9/h13/h46 2 + h53 0 (zapored)",
        "babica": "PILETIČ DOMINANTA (~40/81 — vrnitev po Jakofčič 2-letni dominanti 1913/14!) + Jakofčič ~11 (vse 11 Griblje! razen r72) + Marentič ~15 + Adlešič 1 + Krasinec 1 + Husič 1 + Vogrin 1 + Žungelj 1 + Jurjevčič 1 + Jakobčič 1 (r72) + Mihelič 1",
        "podpis": "Učak (Valerijan) ~59 + Kapl. Bitnar ~21 + [~ r53 Štomhmut? Bitnar] — 2 duhovnika (Bitnar = cf. P109!)",
        "emso": "~38 kandidatov = NAJVEČJA kampanja doslej (P109 ~20); 100% skladnih DDMM preverjenih (r13 0503 → Marec 5!)",
        "dvojcki": "2 para = 3. leto zapored (P107/P108/P109/P110? — cf. P108 2 para); 4 dvojčki, 3 † 1915/16 = 75%",
        "nezakonski": "5 (r34 + r43 + r53 + r73 + r79) + 3 marginalije očetovstva (r34/r43/r53) = NAJVEČ v enem letu",
        "smrtnost": "† 1915–1918 marginalia ~20+ od 81 = ~25% (VOJNA!); 2 očeta † 1915",
        "vojska": "r40 razglašen za mrtvega (1942) + r69 zakon razveljavljen (1965) + r63/r80 priimki spremenjeni + železniška tema (r58 botra želež. delavec + r81 oče želežniški čuvaj + botra žel. uslužbenec)"
    },
    "crossChecks": [
        "r13 EMŠO 0503915500090 → 5.3.1915 = dates 5./6. ✓ (s271 dup razkriva pokrito vrstico)",
        "r16 EMŠO 1603915505171 → 16.3.1915 = dates 16./17. ✓",
        "r18 EMŠO 2503915505294 → 25.3. = 25./26. ✓",
        "r19 EMŠO 2803915505174 → 28.3. = 28.?/29. ✓",
        "r20 EMŠO 2103915500040 → 21.3. = rojstva 21.? ✓ (krsta 1.4. naslednji mesec)",
        "r30 EMŠO 2804915505790 → 28.4. = 28./29. ✓",
        "r35 EMŠO 0805915505021 → 8.5. = 8./10. ✓",
        "r67 EMŠO 0211915505717 → 2.11. = 2./3. ✓",
        "r73 EMŠO 2011915330001 → 20.11. = 20./21. ✓",
        "r74 EMŠO 2511915500090 → 25.11. = 25./26. ✓",
        "r78 EMŠO 1812915500054 → 18.12. = 18./18. ✓",
        "r81 EMŠO 3012915505170 → 30.12. = 30.12.1915 rojstvo ✓ (krsta 4.1.1916)",
        "r2 EMŠO 0801915500210 → 8.1. = 8./9. ✓",
        "r3 EMŠO 0801915005026 → 8.1. = 8./11. ✓",
        "r5 EMŠO 2301914505241 → 23.1. = 23./23. ✓",
        "r10 EMŠO 0103915505038 → 1.3. = 1./1. ✓",
        "r11 EMŠO 0203915505056 → 2.3. = 2./3. ✓",
        "offset poravnava str. 237: 5 starševskih celic (Jurajevčič/—/Copri/Šapič/Kralj/Klepec) = 5 vrstic (r80/r81/r1/r2/r3) + s284-B ima r4 starši (Muc × Gregorič) ✓✓",
        "r34 očetovstvo Janez Križan (4.2.1918) ↔ r41 oče Janez Križan (r. 6.3.1872, ž. Marija Husič) — ista oseba ✓",
        "r53 očetovstvo + poroka oba 18.4.1917 ✓",
        "Gm ×3 (r25 h28 + r50 h53? + r63 h36) = Grm iz matičnega območja ✓",
        "Božinja vas ×2 (r56/r70 h15) = Boginja vas iz matičnega območja ✓"
    ],
    "continuityLast04105": {
        "9": 1913, "13": 1913, "22": 1912, "32": 1909, "40": 1912,
        "45": 1912, "46": 1913, "53": 1914, "70": 1912, "78": 1888, "88": 1910
    },
    "p111Lead": {
        "glava1916": "ročno »1916.« INLINE v ločilni starševski celici str. 237 = s283 + tiskana glava »Leto 1916« na VRHU str. 238 = s284",
        "r1": "Grišiče 3 Julija 9./11. Januar (starši Matija Šapič × Katarina Novak — OFFSET poravnava!)",
        "r2": "Mlake 10 Anton 11./12. (starši Jožef Kralj × Neža Kralj)",
        "r3": "Prilozje 25 Jožef 28./29. (starši Jurij Klepec mer. × Ana Kralj; ‡ 4/2 1916)",
        "r4": "Zemelj 17 Alojzij 1./2. Februar (starši Matija Muc, posed. kovač × Katarina Gregorič — s284-B!)",
        "opomba": "1916 r1–r4 že prebrani okvirno; skeni 269–288 v /tmp/p110 (s284–s288 = 1916 str. 238–242)"
    }
}

with open("research/issue17/parish-baptism-1915.json", "w", encoding="utf-8") as f:
    json.dump(doc, f, ensure_ascii=False, indent=1)
print("entries:", len(G), "excluded:", len(excluded))
print("OK")
