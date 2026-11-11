// P257 — val 2: mikro-dueli na višjih povečavah (8×/6×) za odločitvene celice.
// s7-pasovi (doline+dueli+census): r1 300-417, r2 417-499, r3 499-619, r4 619-693,
// r5 693-783, r6 783-860, r7 860-927, r8 927-1004, r9 1004-1078, r10 1078-1171,
// r11 1171-1239, r12 1239-1323, r13 1323-1421.
export const ROWS = [
  {
    id: 'w2_r2_priimek', scan: 7, y0: 412, y1: 505, x0: 250, x1: 820, zoom: 6,
    q: "1. Febr 1831, vrstica Georg-a [?] iz Grübln 50. Njegov priimek ima te kandidate: 'Pesdirz' (P-e-s-d-i-r-z), 'Podierz' (P-o-d-i-e-r-z), 'Peterž/Petrež', 'Peterlin'. PREBERI ČRKO ZA ČRKO: prva črka (P?), nato sredina (es-di? o-di? te?), nato konec (rz? rž? lin?). Podaj končno oceno.",
  },
  {
    id: 'w2_r7_hisa', scan: 7, y0: 855, y1: 932, x0: 150, x1: 420, zoom: 8,
    q: "Hišna številka ženina v vrstici (Grübl/Griblje), kandidata: 26 in 20. Poglej ZADNJO številko: 6 ima zanko z glavo/repom zgoraj, 0 je zaprt krog brez glave. Katera je? Podaj tudi prvo številko (2).",
  },
  {
    id: 'w2_r7_ime', scan: 7, y0: 855, y1: 932, x0: 250, x1: 820, zoom: 6,
    q: "Ime ženina v tej vrstici: 'Maria' ali 'Mario'? Poglej ZADNJO črko pred priimkom: a (dve piki/ogenjšček zankice) ali o (visoka zanka brez pik)? Podaj tudi priimek (Pödiz? Podierz? Peterž?).",
  },
  {
    id: 'w2_r10_priimek', scan: 7, y0: 1075, y1: 1175, x0: 250, x1: 820, zoom: 6,
    q: "Priimek ženina Nicol-a iz Grübln 65. Kandidati: 'Milek', 'Michl', 'Milic'. Konec besede: -ek, -hl ali -ic? Preberi zadnje 3 črke natančno.",
  },
  {
    id: 'w2_r1_hisaN', scan: 7, y0: 295, y1: 420, x0: 620, y1x: 0, x1: 1080, zoom: 8,
    q: "Hišna številka NEVESTE (Anna [?]) v tej vrstici: kandidati 33 in 39. Poglej drugo številko: 3 ali 9? (3 = dve zgornji zanki desno, 9 = zanka z repom gor). Podaj tudi priimek neveste (Dölker? Pehligh? Dehligl? Doblič?).",
  },
  {
    id: 'w2_r3_hisa', scan: 7, y0: 495, y1: 625, x0: 150, y1x: 0, x1: 460, zoom: 8,
    q: "Hišna številka ženina (Math. [?]) iz Griblje: kandidati 56 in 50. Druga številka: 6 (zanka z glavo) ali 0 (krog)? Podaj tudi njegov priimek (Schimiz? Kiniz? Steinig?).",
  },
  {
    id: 'w2_r12_priimek', scan: 7, y0: 1235, y1: 1330, x0: 250, x1: 820, zoom: 6,
    q: "Vrstica Nicol-a [?]. Priimek ženina: kandidati 'Hambicz', 'Kambicz', 'Klemič'. Prva črka H ali K? Sredina: -bic- ali -mič? Njegova hiša: 13, 15 ali 18? Vas: Podlog ali Priloge? Preberi vse skupaj.",
  },
  {
    id: 'w2_r5_stare', scan: 7, y0: 690, y1: 790, x0: 250, x1: 820, zoom: 6,
    q: "Vrstica Peter-a [?]. Priimek ženina: kandidati 'Stare' (dolga s-zanka na začetku, -are) ali 'Hare'. Njegova nevesta: Maria [Karl? Nikol?]. Preberi priimek ženina in priimek neveste.",
  },
  {
    id: 'w2_r6_priimek', scan: 7, y0: 780, y1: 865, x0: 250, x1: 820, zoom: 6,
    q: "Vrstica Peter-a [?] iz Kaplja vas (Kapln). Priimek ženina: kandidati 'Bedicz', 'Podierz', 'Pesdirz', 'Peterž'. Preberi črkovno: B ali P? -dic- ali -dierz- ali -erž-? Podaj tudi njegovo hišo (4?).",
  },
  {
    id: 'w2_s6_kosolt', scan: 6, y0: 980, y1: 1110, x0: 130, y1x: 0, x1: 420, zoom: 8,
    q: "Hišna številka ženina Mart.-a [Kosolt?] iz Möttling: kandidati 140, 110, 40. Preberi vse tri števke: prva (1 ali 4?), sredinska (4 ali 1?), zadnja (0?). Podaj celoten rezultat.",
  },
  {
    id: 'w2_s6_schunigh', scan: 6, y0: 1115, y1: 1260, x0: 130, y1x: 0, x1: 1080, zoom: 6,
    q: "Vrstica [21.?|26.? Juni] 1830. Ženin Mart. [Schunigh?]: njegova VAS (Vashtaniz? Kofland?) in HIŠA (10 ali 40?). Nevesta Maria [May?]: njena vas (Boršt/Bersht?) in hiša (20?). DATUM: 21. ali 26. Juni? Preberi vse.",
  },
  {
    id: 'w2_s6_khaphingN', scan: 6, y0: 925, y1: 1065, x0: 620, y1x: 0, x1: 1080, zoom: 8,
    q: "Hišna številka NEVESTE (Anna [Tong?]): kandidati 11 in 14. Zadnja številka: 1 (navpična poteza) ali 4 (trikotnik z zanko)?",
  },
  {
    id: 'w2_s6_kozina', scan: 6, y0: 745, y1: 915, x0: 250, x1: 820, zoom: 6,
    q: "Vrstica 17. Febr 1830. Priimek ženina Math.-a [?]: kandidati 'Krajnc', 'Kojnig', 'Kozina'. Njegova nevesta: Maria Angel. Preberi priimek ženina črkovno (Krajnc: K-r-a-j-n-c; Kojnig: K-o-j-n-i-g; Kozina: K-o-z-i-n-a) in njegovo hišo (17?).",
  },
  {
    id: 'w2_s6_marcusN', scan: 6, y0: 620, y1: 800, x0: 620, y1x: 0, x1: 1080, zoom: 6,
    q: "NEVESTA Catharina [Aurnigl?/Sawnich?/Schurig?]. Njena VAS in HIŠA: kandidati 'Kaplja vas 7', 'Strophe 7', '[~ophrs] 1'. Preberi ime vasi (K-a-p-l-j-a? S-t-r-o-p-h-e?) in hišno številko (7?).",
  },
];
