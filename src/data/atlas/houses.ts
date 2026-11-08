// ATLAS 1825 — register hiš/domačij iz Protokola stavbnih parcel (N083PT, leto 1825)
// VSI vnosi: status REVIEW — prepis nemške kurzive (Kurrent) je pomožen (strojni očrt),
// imena lastnikov so približki. Po P3 paleografski preverbi (2. krog VLM, črka-za-črko,
// 2026-10-08) so popravki z 2-kratno konvergenco APLICIRANI; statusi ostajajo REVIEW,
// ker je tudi 2. krog strojno branje (dokončna potrditev: človeška paleografija).
// Vir: Arhiv RS, SI AS 176/N/N83/s/PT, strani 2–7.

export interface AtlasHouse {
  id: string;
  /** hišna številka 1825 (konskripcijska) */
  no: string;
  owner: string;
  /** domnevna sodobna različica imena (REVIEW, samo približek) */
  ownerModernGuess?: string;
  /** sklici na parcele/rabo, kot zapisano v viru (prepis) */
  parcelRefs?: string;
  /** strani vira */
  sourcePage: number;
  status: "REVIEW";
  /** povezava na muzejski zapis, kjer je utemeljena */
  museumRef?: string;
  /** paleografska preverba P3 (2. krog): dokaz, branja, verdikt */
  paleo?: string;
}

export const ATLAS_HOUSES: AtlasHouse[] = [
  // stran 3 — naslovnica Protocoll der Bau Parcellen der Gemeinde „GRÜBLE“
  { id: "hiša-1", no: "1", owner: "Veith (H.) [~]", ownerModernGuess: "Veith", parcelRefs: "Stand: Lam. Grüble [~] (prej brano: Lauri Gavella)", sourcePage: 3, status: "REVIEW", paleo: "P3 (3. neodvisno branje, črka-za-črko): začetnica V, ne P; končnica -th — prej Peth (H.) popravljeno" },
  { id: "hiša-2", no: "2", owner: "Veith (St.?) [~]", ownerModernGuess: "Veith", sourcePage: 3, status: "REVIEW", paleo: "P3: isti priimek kot hiša 1 (kratica imena H./St. se med branjema razlikuje)" },
  { id: "hiša-3", no: "3", owner: "Šimec Jakob", ownerModernGuess: "Schimek/Šimec", sourcePage: 3, status: "REVIEW" },
  { id: "hiša-4", no: "4", owner: "Šimec Matija", ownerModernGuess: "Schimek/Šimec", sourcePage: 3, status: "REVIEW" },
  { id: "hiša-5", no: "5", owner: "Knavc Janez", ownerModernGuess: "Knolc/Knavc", sourcePage: 3, status: "REVIEW" },
  { id: "hiša-6", no: "6", owner: "Tilel Miho", ownerModernGuess: "Tillel?", sourcePage: 3, status: "REVIEW" },
  { id: "hiša-6b", no: "7", owner: "Lebing/Lebring Mädl. [~]", ownerModernGuess: "Lebing?", parcelRefs: "Nº 14 [~] · Areal 84 kv. kl [~]", sourcePage: 3, status: "REVIEW", paleo: "P3 DODANA VRSTICA: obstaja v rokopisu (branje 1: Lebring Mäfa/Leudig Martin; branje 2: Lebing Mädl. — L-priimek + Mädl. konvergirata); prej je v registru manjkala" },
  { id: "hiša-7", no: "7½", owner: "Bödig mündl. [~]", sourcePage: 3, status: "REVIEW", paleo: "P3: 2× Bödig mündl. (veliko B, -ig) — prej Podlesy Marija popravljeno" },
  { id: "hiša-8", no: "8", owner: "Lebing/Lebring Mädl. [~]", sourcePage: 3, status: "REVIEW", paleo: "P3: isti lastnik kot hiša 7 (Lebing Mädl. 2×) — prej Leskovec Matija popravljeno" },
  { id: "hiša-9", no: "8½", owner: "Bödig mündl. [~]", sourcePage: 3, status: "REVIEW", paleo: "P3: 2× Bödig mündl. — prej Leskovec Matija popravljeno" },
  { id: "hiša-10", no: "9", owner: "Stalhutstetisch Miho", parcelRefs: "neprepisljivo", sourcePage: 3, status: "REVIEW" },
  { id: "hiša-11", no: "10", owner: "Stalhutstetisch Miho", sourcePage: 3, status: "REVIEW" },
  { id: "hiša-12", no: "11", owner: "Stalhutstetisch Marko", parcelRefs: "v zvezku tudi »Nr. 108 Peter«", sourcePage: 3, status: "REVIEW" },
  { id: "hiša-13", no: "12", owner: "Stalhutstetisch Marko", sourcePage: 3, status: "REVIEW" },
  { id: "hiša-14", no: "13", owner: "Stalhutstetisch Ruard", sourcePage: 3, status: "REVIEW" },
  { id: "hiša-15", no: "14", owner: "Stalhutstetisch Jhan (Ivan)", sourcePage: 3, status: "REVIEW" },
  { id: "hiša-16", no: "15", owner: "Stalhutstetisch Jhan (Hrovatic Jhan)", sourcePage: 3, status: "REVIEW" },
  { id: "hiša-17", no: "16", owner: "Stautschel Jhan", sourcePage: 3, status: "REVIEW" },
  { id: "hiša-18", no: "17", owner: "Stalhutsch Marko", sourcePage: 3, status: "REVIEW" },
  { id: "hiša-19", no: "18", owner: "Hrovat Jhan", ownerModernGuess: "Hrovat/Hrvat", sourcePage: 3, status: "REVIEW" },
  { id: "hiša-20", no: "19", owner: "Krudelen Matija", sourcePage: 3, status: "REVIEW" },
  { id: "hiša-21", no: "20", owner: "Krištan/Kraihan Mäfa [~]", ownerModernGuess: "Krištof/Kraihan?", parcelRefs: "Weingarten 3 [~] · 92 [~]", sourcePage: 3, status: "REVIEW", paleo: "P3: 2× začetnica K (ne V) + Mäfa/Mädl (branja: Kruišter Mäfa / Kraihan Mäfa / Chrischan Mädl) — prej Vičak Matija popravljeno; točna oblika priimka še odprta" },
  // stran 4 — z parcelnimi sklici (W. = Wohnort, št. parcele, raba)
  { id: "hiša-22", no: "21", owner: "Šture Majzel", parcelRefs: "W.10 · Schißing 102", sourcePage: 4, status: "REVIEW" },
  { id: "hiša-23", no: "22", owner: "Šture Majzel", parcelRefs: "W.10 · Apnind 19", sourcePage: 4, status: "REVIEW" },
  { id: "hiša-24", no: "23", owner: "Ludvig Gregor", parcelRefs: "W.11 · Schißing 101", sourcePage: 4, status: "REVIEW" },
  { id: "hiša-25", no: "24", owner: "Štunidat Mufa", parcelRefs: "W.1 · Apnind 28", sourcePage: 4, status: "REVIEW", museumRef: "MVG-010" },
  { id: "hiša-26", no: "25", owner: "Štunidat Mufa", parcelRefs: "W.1 · Schißing 89", sourcePage: 4, status: "REVIEW" },
  { id: "hiša-27", no: "26", owner: "Hlebetz Jan", parcelRefs: "W.2 · Schißing 245", sourcePage: 4, status: "REVIEW" },
  { id: "hiša-28", no: "27", owner: "Jožef Miko", parcelRefs: "W.21 · Schißing 88", sourcePage: 4, status: "REVIEW" },
  { id: "hiša-29", no: "28", owner: "Jožef Miko", parcelRefs: "W.31 · Apnind 23", sourcePage: 4, status: "REVIEW" },
  { id: "hiša-30", no: "29", owner: "Krišan Gregor", parcelRefs: "W.66 · Apnind 15", sourcePage: 4, status: "REVIEW" },
  { id: "hiša-31", no: "30", owner: "Krišan Gregor", parcelRefs: "W.66 · Schißing 68", sourcePage: 4, status: "REVIEW" },
  { id: "hiša-32", no: "31", owner: "Bring Marko", ownerModernGuess: "Brinig/Bring (PUA: Bring)", parcelRefs: "W.66 · Walle 15", sourcePage: 4, status: "REVIEW" },
  { id: "hiša-33", no: "32", owner: "Bring Marko", parcelRefs: "W.65 · Schißing 90", sourcePage: 4, status: "REVIEW" },
  { id: "hiša-34", no: "33", owner: "Varbutek Mufa", parcelRefs: "W.64 · Schißing 67", sourcePage: 4, status: "REVIEW" },
  { id: "hiša-35", no: "34", owner: "Milleg Hans [~]", ownerModernGuess: "Milleg", parcelRefs: "W.29 · Schißing 46", sourcePage: 4, status: "REVIEW", paleo: "P3: Milleg Hanne/Hans 2× (prej Milleg Stane — ime negotovo [~])" },
  { id: "hiša-36", no: "34 (prečrtana dvojnica)", owner: "Milleg Hans [~]", parcelRefs: "W.29 · Walle 8", sourcePage: 4, status: "REVIEW", paleo: "P3 STRUKTURNO (4. potrditev): PREČRTAN DVOJNI vpis št. 34 (isti lastnik Milleg) — STARI register ga je štel kot hišo 35, zato so bile naslednje številke zamaknjene za +1. Ni samostojna hiša; vrstica ostaja zaradi načela nič-zgube" },
  { id: "hiša-37", no: "35", owner: "Brinig Magnus [~]", ownerModernGuess: "Brinig/Bring", parcelRefs: "W.24 · Schißing 54/64", sourcePage: 4, status: "REVIEW", paleo: "P3 RENUMERACIJA (36→35) + Brinig Magnus 2× (Migurl/Mufur/Magnus) — prej Bring Majzel" },
  { id: "hiša-38", no: "36", owner: "Milleg Hans [~]", parcelRefs: "W.27 · Schißing 164/416", sourcePage: 4, status: "REVIEW", paleo: "P3 RENUMERACIJA (37→36); Milleg Hans 2× (Jan = Hans, ista oseba)" },
  { id: "hiša-39", no: "37", owner: "Brinig Malfa [~]", ownerModernGuess: "Brinig/Bring", parcelRefs: "W.22/23 · Schißing 58", sourcePage: 4, status: "REVIEW", paleo: "P3 RENUMERACIJA (38→37); Brinig Malfa/Malga/Mufa 2×" },
  { id: "hiša-40", no: "38", owner: "Brinig Malfa [~]", ownerModernGuess: "Brinig/Bring", parcelRefs: "W.20/22 · Apnind 21", sourcePage: 4, status: "REVIEW", paleo: "P3 RENUMERACIJA (39→38); Brinig Malfa 2×" },
  { id: "hiša-41", no: "39", owner: "Brinig Miklo [~]", ownerModernGuess: "Brinig/Bring", parcelRefs: "W.25 · Schißing 39", sourcePage: 4, status: "REVIEW", paleo: "P3 RENUMERACIJA (40→39); Brinig Misko/Milo/Miklo/Niklo 2× — prej Tonig Miko (očrt je zamenjal Brinig)" },
  { id: "hiša-42", no: "40", owner: "Brinig Malfa [~]", ownerModernGuess: "Brinig/Bring", parcelRefs: "W.23 · Walle 6", sourcePage: 4, status: "REVIEW", paleo: "P3 RENUMERACIJA (41→40) — ZADNJA vrstica str. 4 (stran se konča s 40, kar 4 neodvisna branja); hiša 41 NE obstaja; str. 5 se začne s PARCELO 41" },
  // stran 5 — parcelni del (parcele 41–60, lastniki + hišne št. W.)
  { id: "parcela-41", no: "—", owner: "Jörg Georg", parcelRefs: "parc. 41 · Weingart 469/51 · W.64", sourcePage: 5, status: "REVIEW" },
  { id: "parcela-42", no: "—", owner: "Glan Georg", parcelRefs: "parc. 42 · Weingart 64 · W.26", sourcePage: 5, status: "REVIEW" },
  { id: "parcela-43", no: "—", owner: "Glan Matthäus", parcelRefs: "parc. 43 · Weingart 109 · W.27", sourcePage: 5, status: "REVIEW" },
  { id: "parcela-44", no: "—", owner: "Malfs Mathäus", parcelRefs: "parc. 44 · Weingart 108 · W.20", sourcePage: 5, status: "REVIEW" },
  { id: "parcela-45", no: "—", owner: "Mals Georg", parcelRefs: "parc. 45 · Weingart 80 · W.28", sourcePage: 5, status: "REVIEW" },
  { id: "parcela-46", no: "—", owner: "Grög Michael", parcelRefs: "parc. 46 · 214 · W.63", sourcePage: 5, status: "REVIEW" },
  { id: "parcela-47", no: "—", owner: "Greg Michael", parcelRefs: "parc. 47 · 4 · W.63", sourcePage: 5, status: "REVIEW" },
  { id: "parcela-48", no: "—", owner: "Greg Michael", parcelRefs: "parc. 48 · 14 · W.63", sourcePage: 5, status: "REVIEW" },
  { id: "parcela-49", no: "—", owner: "Malt Simon", parcelRefs: "parc. 49 · 16 · W.61", sourcePage: 5, status: "REVIEW" },
  { id: "parcela-50", no: "—", owner: "Joger Schello", parcelRefs: "parc. 50 · 9 · W.60", sourcePage: 5, status: "REVIEW" },
  { id: "parcela-51", no: "—", owner: "Joger Schello", parcelRefs: "parc. 51 · 90 · W.60", sourcePage: 5, status: "REVIEW" },
  { id: "parcela-52", no: "—", owner: "Meßle Michael", parcelRefs: "parc. 52 · 87 · W.62", sourcePage: 5, status: "REVIEW" },
  { id: "parcela-52b", no: "—", owner: "Malt Simon D.", parcelRefs: "parc. 52 (2. vnos) · 46 · W.61", sourcePage: 5, status: "REVIEW" },
  { id: "parcela-53", no: "—", owner: "Marlo Michael", parcelRefs: "parc. 53 · 184 · W.31", sourcePage: 5, status: "REVIEW" },
  { id: "parcela-54", no: "—", owner: "Greg Ulrich", parcelRefs: "parc. 54 · Weingart 60 · W.32", sourcePage: 5, status: "REVIEW" },
  { id: "parcela-55", no: "—", owner: "Joger Schello", parcelRefs: "parc. 55 · Weide 43 · W.60", sourcePage: 5, status: "REVIEW" },
  { id: "parcela-56", no: "—", owner: "Malt Ulrich", parcelRefs: "parc. 56 · 196 · W.68", sourcePage: 5, status: "REVIEW" },
  { id: "parcela-57", no: "—", owner: "Piberig Ulrich", parcelRefs: "parc. 57 · 25 · W.32", sourcePage: 5, status: "REVIEW" },
  { id: "parcela-58", no: "—", owner: "Greg Ulrich", parcelRefs: "parc. 58 · 15 · W.32", sourcePage: 5, status: "REVIEW" },
  { id: "parcela-59", no: "—", owner: "Leder Simon", parcelRefs: "parc. 59 · 10 · W.36", sourcePage: 5, status: "REVIEW" },
  { id: "parcela-60", no: "—", owner: "Glan Simonz", parcelRefs: "parc. 60 · 12 · W.65", sourcePage: 5, status: "REVIEW" },
  // stran 6 — hiše 61–80 z parcelami
  { id: "hiša-63", no: "61", owner: "Peutinger Jhan", parcelRefs: "Leim grüben · parc. 59 · Apein 9", sourcePage: 6, status: "REVIEW" },
  { id: "hiša-64", no: "62", owner: "Lappanig Miho", parcelRefs: "parc. 54 · Apfein 9", sourcePage: 6, status: "REVIEW" },
  { id: "hiša-65", no: "63", owner: "Šimec Ripane", ownerModernGuess: "Schimeg/Schimek", parcelRefs: "parc. 49 · Agneid 19", sourcePage: 6, status: "REVIEW" },
  { id: "hiša-66", no: "64", owner: "Šimec Jhan", parcelRefs: "parc. 55 · Agneind 20", sourcePage: 6, status: "REVIEW" },
  { id: "hiša-67", no: "65", owner: "Peutinger Jhan", parcelRefs: "parc. 53 · Abfogjung 34", sourcePage: 6, status: "REVIEW" },
  { id: "hiša-68", no: "66", owner: "Šimec Jhan", parcelRefs: "parc. 55 · Abfagjung 13", sourcePage: 6, status: "REVIEW" },
  { id: "hiša-69", no: "67", owner: "Lappanig Miho", parcelRefs: "parc. 54 · Abfogjung 84", sourcePage: 6, status: "REVIEW" },
  { id: "hiša-70", no: "68", owner: "Dikobutar Rupre", parcelRefs: "parc. 53 · Abfogjung 192", sourcePage: 6, status: "REVIEW" },
  { id: "hiša-71", no: "69", owner: "Filak Peter", parcelRefs: "parc. 55 · Apfein 15", sourcePage: 6, status: "REVIEW" },
  { id: "hiša-72", no: "70", owner: "Filak Peter", parcelRefs: "parc. 95 · Abfogjung 86", sourcePage: 6, status: "REVIEW" },
  { id: "hiša-73", no: "71", owner: "Filak Mihel", parcelRefs: "parc. 94 · Abfogjung 202", sourcePage: 6, status: "REVIEW" },
  { id: "hiša-73b", no: "71½", owner: "Stettner [~] (prečrtana)", parcelRefs: "prečrtana polovična vrstica [~]", sourcePage: 6, status: "REVIEW", paleo: "P3 DODANA VRSTICA: 2× potrjena PREČRTANA polovična vrstica 71 1/2; priimek se bere Stettner/St-…-ner [~] — neštet priimni vnos, ostaja zaradi nič-zgube" },
  { id: "hiša-74", no: "72", owner: "Dikobutar Mihelo", parcelRefs: "parc. 47 · Abfogjung 187", sourcePage: 6, status: "REVIEW" },
  {
    id: "hiša-75",
    no: "73",
    owner: "Peutinger Mihel",
    ownerModernGuess: "prepis negotov (Kurrent)",
    parcelRefs: "parc. 60 · Abfogjung 210",
    sourcePage: 6,
    status: "REVIEW",
    museumRef: "MVG-010",
  },
  { id: "hiša-76", no: "74", owner: "Drulak Jhan", parcelRefs: "parc. 51 · Abfogjung 318", sourcePage: 6, status: "REVIEW" },
  { id: "hiša-77", no: "75", owner: "Drulak Peter", parcelRefs: "parc. 51 · Agneid 63", sourcePage: 6, status: "REVIEW" },
  { id: "hiša-78", no: "76", owner: "Strauß Georg [~]", ownerModernGuess: "Strauß", parcelRefs: "parc. 45 · Wiese · Areal 20", sourcePage: 6, status: "REVIEW", paleo: "P3: 2× Strauß Georg (S-t-r-a-u-ß, ime Georg ali Gregor) — prej Stenopfs Georg popravljeno" },
  { id: "hiša-78b", no: "76½", owner: "Hufschmied [~] (rdeči vpis, prečrtana)", parcelRefs: "W.47 [~] · 14 [~]", sourcePage: 6, status: "REVIEW", paleo: "P3 DODANA VRSTICA: 2× potrjena prečrtana polovična vrstica z besedo Hufschmied (podkovar — poklic?) v RDEČEM čnilu — verjetno ne lastniški vnos, ostaja zaradi nič-zgube" },
  { id: "hiša-79", no: "77", owner: "Dikobutar Mihlo", parcelRefs: "parc. 47 · Agneid 14", sourcePage: 6, status: "REVIEW" },
  { id: "hiša-80", no: "78", owner: "Dikobutar Marko", parcelRefs: "parc. 47 · Abfogjung 176", sourcePage: 6, status: "REVIEW" },
  { id: "hiša-81", no: "79", owner: "Strauß Georg [~] (vrstica rdeče prečrtana)", parcelRefs: "parc. 45 · Agneid 100", sourcePage: 6, status: "REVIEW", paleo: "P3: 2× Strauß Georg + 2× prečrtanost vrstice (duplikat hiše 76?) — prej Stenopfs Georg" },
  { id: "hiša-82", no: "80", owner: "Dikobutar Marko", parcelRefs: "parc. 47 · Agneid 21", sourcePage: 6, status: "REVIEW" },
  // stran 7 — hiše 81–98 (Schopfhütte/Hof, Abgerissen)
  { id: "hiša-83", no: "81", owner: "Strauß Georg [Groy] [~]", ownerModernGuess: "Strauß/Groy", parcelRefs: "Grüble 45 · Bau · Hof gültfällig [~]", sourcePage: 7, status: "REVIEW", paleo: "P3: 2× Strauß + ime Georg (ne Hanž); »Groy« se v rokopisu pojavi kot DRUGI zapis (dvojni priimek/družinsko ime) — prej Groy Hanž" },
  { id: "hiša-84", no: "82", owner: "Strauß Georg [Groy] [~]", parcelRefs: "45 · Abgerissen (porušeno) [~]", sourcePage: 7, status: "REVIEW", paleo: "P3: Strauß [Georg]/Groy 2×; Abgerissen potrjen" },
  { id: "hiša-85", no: "83", owner: "Strauß Georg [Groy] [~]", parcelRefs: "46 [~] · Schupfhütte/Hof · gültfällig [~]", sourcePage: 7, status: "REVIEW", paleo: "P3: Strauß [Georg]/Groy 2×; opomba Hof Gültfällig (davčno obvezna kljub rušitvi)" },
  { id: "hiša-86", no: "84", owner: "Strauß Georg [Groy] [~]", parcelRefs: "46 [~] · Abgerissen", sourcePage: 7, status: "REVIEW", paleo: "P3: Strauß Groy 2×; Abgerissen potrjen" },
  { id: "hiša-87", no: "85", owner: "Peta Krištof (Krischan)", parcelRefs: "37 · Schopfhütte/Hof", sourcePage: 7, status: "REVIEW" },
  { id: "hiša-88", no: "86", owner: "Matja Krištof", parcelRefs: "36 · Abgerissen", sourcePage: 7, status: "REVIEW" },
  { id: "hiša-89", no: "87", owner: "Heurisch Marko", parcelRefs: "44 · Abgerissen", sourcePage: 7, status: "REVIEW" },
  { id: "hiša-90", no: "88", owner: "Matja Krištof", parcelRefs: "36 · Schopfhütte/Hof", sourcePage: 7, status: "REVIEW" },
  { id: "hiša-91", no: "89", owner: "Heurisch Marko", parcelRefs: "44 · Schopfhütte/Hof", sourcePage: 7, status: "REVIEW" },
  { id: "hiša-92", no: "90", owner: "Kuncelj Miha [?] — branja divergirajo", parcelRefs: "40 [~: 43] · Schopfhütte/Hof · Areal 88/89 [~]", sourcePage: 7, status: "REVIEW", paleo: "P3: TRI medsebojno izključujoča branja (1. krog: Kavalar/Bumiller Marlo; 2. krog: Ihmeyer Georg — čisto nemško berljivo) — ostaja ILLEGIBLE/REVIEW; priimek Kuncelj se v nobenem krogu ne potrdi" },
  { id: "hiša-93", no: "91", owner: "Heurisch Marko", parcelRefs: "44 · Schopfhütte/Hof", sourcePage: 7, status: "REVIEW" },
  { id: "hiša-94", no: "92", owner: "Groy Feidig", parcelRefs: "41 · Schopfhütte/Hof", sourcePage: 7, status: "REVIEW" },
  { id: "hiša-95", no: "93", owner: "Matja Feidig", parcelRefs: "40 · Abgerissen", sourcePage: 7, status: "REVIEW" },
  { id: "hiša-96", no: "94", owner: "Matja Feidig", parcelRefs: "40 · Schopfhütte/Hof", sourcePage: 7, status: "REVIEW" },
  { id: "hiša-97", no: "95", owner: "Schmerz Marko", parcelRefs: "39 · Schopfhütte/Hof", sourcePage: 7, status: "REVIEW" },
  { id: "hiša-98", no: "96", owner: "Ihmeyer Manko [~]", ownerModernGuess: "Ihmeyer?", parcelRefs: "38 [~] · Schopfhütte [~] · Areal 90 [~]", sourcePage: 7, status: "REVIEW", paleo: "P3: 2× Ihmeyer (2. krog: Manko/Mankl; 1. krog: Georg — ime negotovo) — prej Groy Khunz popravljeno" },
  { id: "hiša-99", no: "97", owner: "Schmerz Marko", parcelRefs: "39 · Abgerissen", sourcePage: 7, status: "REVIEW" },
  {
    id: "hiša-100",
    no: "98",
    owner: "k.k. Zollamt (ärarial) [~] — institucija",
    parcelRefs: "40 · Schopfhütte · Hauptmagazin 1826 [~] (prej brano: 1860)",
    sourcePage: 7,
    status: "REVIEW",
    paleo: "P3: 2× institucionalno branje — A. A. Zollamt + ärarial + opomba »Hauptmagazin von 1826« (ne 1860, ne priimek Zollnerd) — carinska postaja/glavno skladišče kot lastnik",
  },
  { id: "hiša-101", no: "99", owner: "[prazna vrstica — zaključek str. 7]", parcelRefs: "oštevilčena vrstica s prazno lastniško celico", sourcePage: 7, status: "REVIEW", paleo: "P3 DODANA VRSTICA: 2× potrjena prazna vrstica 99 (zaključni vnos strani)" },
];
