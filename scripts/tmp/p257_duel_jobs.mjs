// P257 — seznam dvobojev (duel jobs). s7-pitch: center_i = 300 + 84.9*(i-0.5); pas ±50.
// s6-pitch: center_i = 290 + 96.8*(i-0.5). Vsi izrezi so iz /tmp/p257/s{scan}.jpg.
export const ROWS = [
  // ===== VAL 1 — NIT PEZDIRC + KLJUČNE CELICE =====
  {
    id: 'duel_r2_pesdirc', scan: 7, y0: 375, y1: 480, x0: 360, x1: 740, zoom: 4,
    q: "1. Febr 1831, Georg [Pesdirz/Podierz?] (Grübln 50). VPRAŠANJE: PRIIMEK ŽENINA v stolpcu Taufname+Familien-Name — je 'Pesdirz' (P-e-s-d-i-r-z = Pesdirc) ali 'Podierz' (P-o-d-i-e-r-z) ali kaj tretjega? Preberi črko za črko: začetna P/B, nato središčna zanka (sd ali di?), končnica.",
  },
  {
    id: 'duel_r2_pesdirc_oce', scan: 7, y0: 375, y1: 480, x0: 1030, x1: 1560, zoom: 3,
    q: "1. Febr 1831 — starši ŽENINA (Eltern des Bräutigams, desna stran razprtega lista). Pričakovano: oče 'Marco Pesdirz' + mati 'Dorothea Chernigl'. VPRAŠANJE: priimek OČETA — 'Pesdirz' ali 'Podierz'? In priimek MATI — 'Chernigl' ali kaj drugega?",
  },
  {
    id: 'duel_r7_mario', scan: 7, y0: 795, y1: 910, x0: 360, x1: 740, zoom: 4,
    q: "9. Febr 1831 — vrstica z ANOMALIJO: v stolpcu ženina je žensko ime 'Maria Pödiz' (Grübln 26). VPRAŠANJE 1: je ime 'Maria' (Ž) ali 'Mario' (M)? Zadnja črka pred priimkom — a ali o? VPRAŠANJE 2: priimek — 'Pödiz/Podierz/Pesdirz'? VPRAŠANJE 3: hišna številka ženina — 26 ali 20?",
  },
  {
    id: 'duel_r7_hisa', scan: 7, y0: 795, y1: 910, x0: 180, x1: 460, zoom: 5,
    q: "9. Febr 1831 — Wohnort + Haus-Nr ŽENINA (Grübln/Griblje). VPRAŠANJE: hišna številka — 26 ali 20? Preberi obliko zadnje številke (6 = zanka z glavo, 0 = krog).",
  },
  {
    id: 'duel_r6_bedicz', scan: 7, y0: 715, y1: 820, x0: 360, x1: 740, zoom: 4,
    q: "9. Febr 1831 — Peter [Bedicz/Podierz/Pesdirz?] (Kapln 4). VPRAŠANJE: PRIIMEK ŽENINA — 'Bedicz', 'Podierz', 'Pesdirz' ali kaj četrtega? Preberi črkovno: začetnica B ali P? sredina: di/de/edi?",
  },
  {
    id: 'duel_r13_podierz', scan: 7, y0: 1310, y1: 1420, x0: 620, x1: 1080, zoom: 4,
    q: "9. Febr 1831 — NEVESTA zadnje vrstice: Catharina [Podierz?] (Grübln 11). VPRAŠANJE 1: priimek neveste — 'Podierz', 'Pesdirz', 'Salophig' ali kaj drugega? VPRAŠANJE 2: hišna številka neveste — 11? Preberi natančno.",
  },
  {
    id: 'duel_r13_oceN', scan: 7, y0: 1310, y1: 1420, x0: 1030, x1: 1560, zoom: 3,
    q: "9. Febr 1831 — starši NEVESTE (Eltern der Braut, desna stran). Prejšnje branje: oče 'Math. Salophig'?? + mati 'Dorothea Schiner'. VPRAŠANJE: priimek OČETA neveste — 'Salophig' ali 'Podierz/Pesdirz' ali kaj drugega? Je to sploh priimek ali beri znova.",
  },
  // ===== VAL 1 — HIŠE GRIBLJE (korpus!) =====
  {
    id: 'duel_r1_hisi', scan: 7, y0: 290, y1: 400, x0: 180, x1: 1080, zoom: 4,
    q: "26. Jänner 1831 — Peter Križan (Griblje/Grüble, hiša 3) × Anna [Pehligh/Doblič?] (Griblje, hiša 33?). VPRAŠANJE 1: hišna številka ŽENINA — 3? VPRAŠANJA 2: hišna številka NEVESTE — 33 ali 38 ali 3x? Preberi OBE številki natančno (Wohnort+Haus-Nr stolpca ženina IN neveste).",
  },
  {
    id: 'duel_r1_priimekN', scan: 7, y0: 290, y1: 400, x0: 620, x1: 1080, zoom: 4,
    q: "26. Jänner 1831 — NEVESTA Anna [priimek?]. Branja doslej: 'Pehligh', 'Doblič', oče 'Mario Doblioz [Doblič]'. VPRAŠANJE: priimek neveste — 'Pehligh', 'Doblič/Doblioz' ali kaj tretjega? Preberi črkovno.",
  },
  {
    id: 'duel_r3_schimiz', scan: 7, y0: 465, y1: 560, x0: 360, x1: 740, zoom: 4,
    q: "9. Febr 1831 — Math. [Schimiz/Kiniz?] (Griblje, hiša 56). VPRAŠANJE 1: priimek ženina — Schimiz ali Kiniz ali kaj tretjega? VPRAŠANJE 2: hišna številka ženina — 56? Preberi natančno.",
  },
  {
    id: 'duel_r3_pedierz', scan: 7, y0: 465, y1: 560, x0: 620, x1: 1080, zoom: 4,
    q: "9. Febr 1831 — NEVESTA Maria [Pedierz?] (Podsemel 3). VPRAŠANJE: priimek neveste — 'Pedierz', 'Pesdirz' ali kaj drugega? In hiša — 3?",
  },
  {
    id: 'duel_r10_milek', scan: 7, y0: 1055, y1: 1160, x0: 360, x1: 740, zoom: 4,
    q: "9. Febr 1831 — Nicol [Milek/Milic?] (Grübln, hiša 65). VPRAŠANJE 1: priimek ženina — Milek ali Milic ali kaj tretjega? VPRAŠANJE 2: hišna številka — 65? (6+5 previdno).",
  },
  {
    id: 'duel_r12_hambicz', scan: 7, y0: 1225, y1: 1330, x0: 360, x1: 740, zoom: 4,
    q: "9. Febr 1831 — Nicol [Hambicz/Kambicz?] (Podlog?, hiša 13/15?). VPRAŠANJE 1: priimek ženina — Hambicz ali Kambicz? VPRAŠANJE 2: hišna številka — 13 ali 15? VPRAŠANJE 3: vas — Podlog ali Priloje?",
  },
  // ===== VAL 1 — s6/1830 =====
  {
    id: 'duel_s6_tschall', scan: 6, y0: 750, y1: 930, x0: 40, x1: 2040, zoom: 1.5,
    q: "Segment s6 med vrstico 12. Jänner 1830 (Marcus Vipavc) in vrstico 17. Febr (Mathias Kozina). Tu bi morala biti VRSTICA '17. Febr 1830': Martin [Tschall/Taschall?] iz [Gurila/Mronš?] hiša 8 × Catharina [Stephanitsch?] iz [Dobrnič?] hiša 8. PREBERI CELO VRSTICO (datum, ženin vas+hiša+ime+starost, nevesta vas+hiša+ime+starost, starši, priči). Če vrstice ni, povej kaj vidiš.",
  },
  {
    id: 'duel_s6_marcusN', scan: 6, y0: 630, y1: 800, x0: 620, x1: 1080, zoom: 4,
    q: "12. Jänner 1830 — NEVESTA Marcusa Vipavca: Catharina [Aurnigl?]. Branja: vas 'Kapljske/Kaplja vas' hiša 7 ALI vas '[~ophrs]' hiša 1. VPRAŠANJE: preberi Wohnort + Haus-Nr NEVESTE natančno — kakšna je vas in hišna številka?",
  },
  {
    id: 'duel_s6_kozina', scan: 6, y0: 770, y1: 930, x0: 180, x1: 740, zoom: 4,
    q: "17. Febr 1830 — ženin te vrstice: [Kozina/Koging/Koynig?], vas [Dobrnik/Dobraiz/Dobrnič?], hiša [17/14?]. VPRAŠANJE: preberi priimek, vas in hišno številko ŽENINA natančno.",
  },
  {
    id: 'duel_s6_mogorinN', scan: 6, y0: 830, y1: 1000, x0: 620, x1: 1080, zoom: 4,
    q: "17. Februar 1830 — NEVESTA: Anna [Milek], Griblje, hiša 22 (branje: oče Joh. Milek). VPRAŠANJE 1: priimek neveste — Milek ali Miller? VPRAŠANJA 2: hiša — 22? Preberi natančno (to je hiša 'Millerjevih nevest' 1828/1829 — a je tu spet ista družina?).",
  },
  {
    id: 'duel_s6_mogorinZ', scan: 6, y0: 830, y1: 1000, x0: 180, x1: 560, zoom: 4,
    q: "17. Februar 1830 — ženin: Georg [Mogorin/Moosin/Megorin?], vas [Zarkwische/Zerkinjef/Zarkwishe?], hiša 15. VPRAŠANJE: preberi priimek, vas in hišo ŽENINA natančno.",
  },
  {
    id: 'duel_s6_kosolt', scan: 6, y0: 985, y1: 1100, x0: 180, x1: 560, zoom: 4,
    q: "18. März 1830 — ženin: Mart. [Kosolt/Kosalth?], vas Möttling, hiša [110/140/10?]. VPRAŠANJE: hišna številka — 110, 140 ali 10? Preberi obliko: 1 na začetku, nato 0/4/1, nato 0.",
  },
  {
    id: 'duel_s6_schunigh', scan: 6, y0: 1120, y1: 1250, x0: 40, x1: 1080, zoom: 2,
    q: "21.? Juni 1830 — vrstica: Mart. [Schunigh?], vas [Vrhnika?/Gorjuše?/Vastaniz?], hiša [0/10?], 19 let × Maria [May?], vas [Breg?], hiša 20, 16 let. VPRAŠANJA: 1) datum — 21.? 2) vas+hiša ženina? 3) vas+hiša neveste? Preberi vse tri natančno.",
  },
  {
    id: 'duel_s6_khaphingN', scan: 6, y0: 930, y1: 1060, x0: 620, x1: 1080, zoom: 4,
    q: "17.2.1830 — NEVESTA: Anna [Tong?], vas [~amath/Pamaets?], hiša [14/11?]. VPRAŠANJE: preberi vas in hišno številko neveste natančno.",
  },
];
