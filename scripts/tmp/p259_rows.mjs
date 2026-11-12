import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';
const zai = await ZAI.create();
const DIR = '/tmp/p259/full';

const COLS = `Stolpci LEVE strani razprtega lista: [Jahr/Monat/Tag der Trauung] [Wohnort ŽENINA] [Haus-Nr] [Taufname+Familien-Name+Stand ŽENINA] [Alter] | DESNE strani: [Eltern des Bräutigams] [Eltern der Braut] [Zeugen] [Urkunden] [Unterschrift des trauenden Priesters]`;

const H = {
  s11_r2: "1833 Pag. 19 (6. Febr d°): POZOR — prejšnja stran Pag. 17 se je končala z 'Johann PESDIRZ Griblje 50 × Maria [Himiz] Griblje 49'! Ta vrstica: (a) 'Joh. Gosling? Griblje 53 × Maria Bring/Brinc Griblje 24' (b) 'Johann Pesdirz? Griblje 33 × Maria Brung Griblje 24' (c) oče: 'Johann Gutting?/Maria Poshel', nevestin oče 'Michael Being? Lindart'. VPRAŠANJE: priimek ženina (Pesdirz? Gosling? Gutting?) ČRKO ZA ČRKO + hiša (33? 53? 50?) + priimek neveste (Bring/Brunc/Brinc?) + hiša (24?).",
  s11_r3: "1833 Pag. 19 (6. Febr d°): (a) 'Mathias Hvauf? Otok 31 × Amal Berkozy? Seel? 14' (b) 'Matthias Mosaic? Otok 31 × Anna Berhozez? Igel? 14' (c) oče 'Joseph Kersch? Lindart/Margareth Palgich', nevestini 'Georg Bartolg? Lindart/Maria Kambisch'. VPRAŠANJE: priimek ženina + priimek/ime neveste + vasi (Otok 31? Seel/Igel 14?).",
  s11_r4: "1833 Pag. 19 (6. Febr d°): (a) 'Nikolaus Bogil? Grinstal? 2 × Maria Schallg? Otok 22' (b) 'Nicolaus Brzin? Grove? 2 × Maria Lebulich? Otok 22' (c) oče 'Martin Bajak?/Catharina Teng', nevestini 'Joh. Felsch? Lindart/Maria Maleschig'. VPRAŠANJE: priimek ženina (Bogil? Brzin? Bajak~Butala?) + vas (Grinstal? Grove?) + hiša 2? + priimek neveste + Otok 22?",
  s11_r5: "1833 Pag. 19 (6. Febr d°): (a) 'Georg Hunczl? Kostava? 10 × Anna Britala? Treblgla? 35' (b) 'Georg Anizek? Sastava? 10 × Anna Batale Tschechel 33' (c) oče 'Martin Trunkig? Lindart/Catharina Bras?', nevestini 'Joh. Kemperl? Lindart/Maria Maleschig'. VPRAŠANJE: priimka + vasi (Kostava/Sastava? Treblgla/Tschechel?) + starost neveste (33? 35?).",
  s11_r6: "1833 Pag. 19 (6. Febr d°): (a) 'Johann Gutthorrgy? Vas? 3 × Maria Bukory? Zeindorf? 4' (b) 'Johann Jotschitsch? 3 (Pfarr-Witwer? = vdovec župnije?) × Maria Bubur? Zorkovica? 4' (c) oče 'Nicel. Gertschnig? Lindart/Anna Palgich?', nevestini 'Nicel. Hohanig? Lindart/Anna Hiponig?'. VPRAŠANJE: priimka + vasi + STAND ženina (vdovec? Pfarr-Witwer?) + hiši (3? 4?).",
  s11_r7: "1833 Pag. 19 (6. Febr, eksplicitno zapisan): (a) 'Mathias Tardigl? Döfja? 13 × Catharina Hunczl? Panigha? 10' (b) 'Matthias Tschirsch? Luse? 13 × Catharina Anizel? Pavinge? 10' (c) oče 'Matthias Lendig? Lindart/Barbara Maschorg?', nevestini 'Martin Hanig? Lindart/Catharina Bras?'. VPRAŠANJA: priimka + vasi (Döfja/Luse? Panigha/Pavinge?) + hiši.",
  s11_r8: "1833 Pag. 19 (6. Febr d°): (a) 'Mathias Mulhorrgy? Döfja? 5 × Catharina Durigh? Panigha? 9' (b) 'Matthias Milsovic? Luse? 8 × Catharina Anizel? Pavinge? 9' (c) oče 'Michael Miltwig? Lindart/Maria Tertig?', nevestini 'Georg Trunkig? Lindart/Maria Agnig?'. VPRAŠANJA: priimka + hiši ženina (5? 8?) + vasi.",
  s11_r9: "1833 Pag. 19 (13. Febr d° — prvi po 6.-Febr-kaskadi): (a) 'Georg Haushfinigl? Krajng? 32 × Catharina Kurra Germ? 29' (b) 'Georg Arahrinigel? Kosting? 22 × Catharina Kurre Gern? 29' (c) oče 'Peter Harschping? Lindart/Maria Horsang?', nevestini 'Matthias Horre? Lindart/Anna Urbas?'. VPRAŠANJA: priimek ženina + vas (Krajng=Kranjec? Kosting=Kostanjevica?) + hiša (32? 22?) + vas neveste + 29?",
  s11_r10: "1833 Pag. 19 (13. Febr d°): (a) 'Nikolaus Kuergfyhigl? Ohlach? 18 × Catharina Tongl? Germ? 20' (b) 'Nicolaus Kirchginzlich? Otok 18 × Catharina Jangcinovci? Gern? 30' (c) oče 'Martin Zerzaffig? Lindart/Catharina Hapes?', nevestini 'Nicolaus Teng? Lindart/Catharina Kramozg?'. VPRAŠANJA: priimka + vasi + hiši (18? 20? 30?).",
  s11_r11: "1833 Pag. 19 (13. Febr d°): (a) 'Georg Haushfinigl? Krajng? 20 × Maria Melill? Seel? 16' (b) 'Georg Starshinigel? Kosting? 20 × Maria Milich? Igel? 16' (c) oče 'Matthias Harschping? Lindart/Maria Hombig?', nevestini 'Peter Mille? Lindart/Maria Sellig?'. VPRAŠANJA: priimka + vasi + hiši.",
  s11_r12: "1833 Pag. 19 (13. Febr d°): (a) 'Mathias Melill? Seel? 16 × Catharina Kurran? Ohlach? 16' (b) 'Matthias Milich? Igel? 26 × Catharina Krischan? Otok 16' (c) oče 'Peter Mille? Lindart/Maria Selbig?', nevestini 'Michael Hirschan? Lindart/Dorothea Hohozig?'. VPRAŠANJA: priimka + vasi + hiša ženina (16? 26?) + ALI je priimek neveste KRIŽAN (Krischan)?!",
  s11_r13: "1833 Pag. 19 (13. Febr d° — ZADNJA vrstica strani): (a) 'Anton Malfghigl? Lindart 21 × Maria Haushfinigl? Krajng? 20' (b) 'Anton Malahtinigel? Gradi? 21 × Maria Anashinigel? Kosting? 20' (c) oče 'Anton Maleschig?=MALEŠIČ?/Maria Angel', nevestini 'Michael Hanarshinig? Lindart/Anna Vipauz?'. VPRAŠANJA: priimka (Maleschig~MALEŠIČ-kand.?) + vasi + priimek neveste.",
  s12_r1: "1833 Pag. 21 (DATUM-DUEL: 12. ali 19. Febr 1833? Prejšnja stran se je končala 13. Febr — chronologija zahteva ≥13.!): (a) 'Georg Hofferer? Nötsch? 13, 23 l × Anna Tschesch? Goritschach? 10, 23 l' (b) 'Georg Hohenauer? Kreuzdorf? 13 × Anna Stunigk? Prüstein? 10' (c) oče 'Georg Hafner?/Ana Perfigh?', nevestini 'Peter Trunk?/Margaretha Zwitting?'. VPRAŠANJA: DATUM (12./19.?) + priimka + vasi + hiši.",
  s12_r2: "1833 Pag. 21 (DATUM-DUEL: 19. d°? 12. April? 13. dito?): (a) 'Matthias Messing? Ottak? 18, 22 l × Catharina Hurrey? geb. Podurg? (VDova!) Pröble? 10, 31 l' (b) 'Mathias Mesing? Ott? 18 × Catharina Kerre? geb. Petrug? Püble? 10' (c) oče 'Nicolaus Masving?/Barbara Agran', nevestini 'Peter Pestig?/Barbara Porell'. VPRAŠANJA: DATUM + priimka + vasi + ALI je nevesta VDOVA (geb.=rodjena poročena)?",
  s12_r3: "1833 Pag. 21 (21. April): (a) 'Martin Havran? GROSUPL? 1, 31 l × Josepha Lebstán? GROSUPL? 1, 30 l' (b) 'Martin Hoervan? Grosupl 1 × Josepha Leopfan? Grosupl 1' (c) oče 'Matthaus Marvan?/Susana Horothin', nevestini 'Lorenz Lebotan?/Theresia Nichola'. VPRAŠANJA: priimka (Havran? Marvan?) + vas (RES Grosuplje pri Ljubljani? ali kaj drugega?) + hiši (1×1?).",
  s12_r4: "1833 Pag. 21 (5. Mai): (a) 'Martin Musser? Dobravič? 34, 48 l × Barbara Klebutschar?=KLOBUČAR! Otok 18, 27 l' (b) 'Martin Muscan? Dobroviz? 34 × Barbara Koschehar? Ott? 18' (c) oče 'Martin Musan?/Catharina Torkel', nevestini 'Peter Habrighar?/Anna Lonorg'. VPRAŠANJA: priimka + vasi + hiši + KLOBUČAR?",
  s12_r5: "1833 Pag. 21 (DATUM-DUEL: 19. ali 10. ali 26. October?): (a) 'Georg Schmig?~ŠIMIČ? Griblje 60?, 39 l × Katharina Harschpich? Kresling? 21, 38 l' (b) 'Georg Amiz? Gribl 60 × Katharina Jureisjofrig? Kosting? 21' (c) oče 'Matthias Parity?/Maria Hanig', nevestini 'Matthias Petig?/Maria Kamlig'. VPRAŠANJA: DATUM + priimek ženina (Šimič? Amiz?) + hiša (60?) + priimek/vas neveste.",
  s12_r6: "1833 Pag. 21 (27. Nov, ROBNA-ŠT. 1 — prva robna številka v knjigi!): (a) 'Georg Bring? GRIBLJE 28, 31 l × Anna Tschekl? Kresling? 22, 30 l' (b) 'Georg Brung? Gribl 28 × Anna Tisch? Kosting? 22' (c) oče 'Nicolaus Woriz?/Catharina Krischan?=KRIŽAN!', nevestini 'Johann Fillal?/Maria Krischan?=KRIŽAN!'. VPRAŠANJA: priimek ženina (Bring/Brung/Brinc?) + GRIBLJE 28? + priimek neveste + KRIŽAN-starši?",
  s12_r7: "★RESTART-1834! Pag. 21 (DATUM-DUEL: 22. ali 27. Jänner 1834? ROBNA-ŠT. 2): (a) 'Johann Kalmigh? Vano? 5, 31 l × Maria Dobrak? Gordej? 3, 26 l' (b) 'Stephan Pasfrig? Vivano? 5 × Maria Kosak? Gradiz? 3' (c) oče 'Johann Gapfich?/Agna Sauel', nevestini 'Anton Novak/Katharina Kopaich'. VPRAŠANJA: DATUM (22./27.?) + ime ženina (Johann? Stephan?) + priimka + vasi + hiši.",
  s12_r8: "1834 Pag. 21 (d° = isti dan kot prejšnja vrstica, ROBNA-ŠT. 3): (a) 'Jakob Suchel? Nötsch? 11?, 26 l × Katharina Roschmann? Kreite? 2, 20 l' (b) 'Jakob Heikel? Dobroviz? 14 × Katharina Rosmann? Skrile? 2' (c) oče 'Georg Ljugal?/Margaretha Bleith', nevestini 'Peter Prichman?/Maria Krischan?'. VPRAŠANJA: priimek ženina + vas (Nötsch? Dobroviz?) + hiša (11? 14?) + vas neveste (ŠKRILJE?).",
  s12_r9: "1834 Pag. 21 (29. Jänner, ROBNA-ŠT. 4): (a) 'Mathias Kotler? Semic? 28, 16 l × Catharina Katuchig? Podloge? 30, 18 l' (b) 'Marius Kolniz? Sinel? 23 × Catharina Fabianz? Palonje? 30' (c) oče 'Marcus Holzel?/Anna Kleper', nevestini 'Matthias Trunkrig?/Catharina Arazpino?'. VPRAŠANJA: ime (Mathias? Marius?) + priimka + vasi (Semelj? Sinel?) + hiši (28? 23? 30?).",
  s12_r10: "1834 Pag. 21 (29. Jän d°, ROBNA-ŠT. 5): (a) 'Mathias Kurjotschig? Ottak? 11, 24 l × Anna MUZ? Perni? 27, 19 l' (b) 'Matthias Kerzejofrig? Ott 11 × Anna Mirz?=MUZ? Verm? 27' (c) oče 'Georg Suragoffigh?/Anna Torkel', nevestini 'Martin Marz?/Anna Tomz'. VPRAŠANJA: priimek ženina + priimek neveste (MUZ?! — družina 1828/1831/1833!) + vasi + hiši.",
  s12_r11: "1834 Pag. 21 (29. Jän d°, ROBNA-ŠT. 6): (a) 'Mathias Novak Ottak 18?, 27 l × Margareth Pogiz? Goritschach? 6, 19 l' (b) 'Matthias Novak Ott 15? × Margaretha Grpliz? Gasprig? 6' (c) oče 'Matthias Novar?/Catharina Kapp', nevestini 'Martin Paspich?/Maria Krischan?'. VPRAŠANJA: hiša ženina (18? 15?) + priimek neveste + vasi.",
  s12_r12: "1834 Pag. 21 (29. Jän d°, ROBNA-ŠT. 7 — zadnja vrstica sredine): (a) 'Mathias Smagel? Semic? 23, 21 l × Anna Kurjotschig? Može? 11, 25 l' (b) 'Matthias Snavze? Sinel? 23 × Anna Kerzejofrig? MLAKE? 11' (c) oče 'Matthias Amozil?/Maria Ang?=ANGEL?', nevestini 'Georg Suragoffigh?/Anna Arazpino?'. VPRAŠANJA: priimka + vasi (Semelj? Mlake?) + hiši.",
  s13_r1: "★RESTART-1834-v-glavi! Pag. 23 (5. Febr 1834, ROBNA-ŠT. 8): (a) 'Georg Kapucžik? Gerhüpe? 2, 29 l × Anna Vipotnik? Jeschnica? 8, 22 l' (b) 'Georg Koschizhigl? Gerhuipa? 2 × Anna Viqnay?/Vischnay? Gerhuipa? 8'. VPRAŠANJA: priimka + vasi (Gerhüpe/Gerhuipa = Gorjupa? Gorenje?) + hiši (2? 8?).",
  s13_r2: "1834 Pag. 23 (DATUM-DUEL: 9. ali 5. Febr, ROBNA-ŠT. 9): (a) 'Matthias Schweiger? GRADEC? 32, 35 l × Maria Kovachich? Ptolaz? 23, 21 l' (b) 'Mathias Schweizer? Gradac? 32 × Maria Rabath? Gradac? 23'. VPRAŠANJA: DATUM + priimka + vasi + hiši.",
  s13_r3: "1834 Pag. 23 (10. Febr, ROBNA-ŠT. 10): (a) 'Mathias Kokhanich? Brodpt?=BROD/BORŠT? 17, 31 l × Maria Kral? Brodpt? 22, 26 l' (b) 'Mathias Kokhanich? Boršt? 17 × Maria Kokal? Dorfšt? 22'. VPRAŠANJA: priimka (Kokhanič?) + vasi (Brod? Boršt? Dorfšt?) + hiši.",
  s13_r4: "1834 Pag. 23 (10. Febr d°, ROBNA-ŠT. 11): (a) 'Michael Kokhanich? Brodpt? 18, 21 l × Maria Koschmann? Brodpt? 19, 16 l' (b) 'Michael Kokhanich? Dorfšt? 18 × Maria Kokhmann? Dorfšt? 19'. VPRAŠANJA: priimka + vasi + hiši (18? 19?) + ALI sta ženina r3/r4 BRATJE (ista priimka, sosednji hiši 17/18)?",
  s13_r5: "1834 Pag. 23 (10. Febr d°, ROBNA-ŠT. 12): (a) 'Martin Hruzl? Dolenei ob Crmo?~Dolenje ob Črmošnjice? 8, 29 l × Maria Kocevar? Gorn? 32, 20 l' (b) 'Martin Anzel? Paunoviči? 8 × Maria Korešig? Gemna? 32'. VPRAŠANJA: priimka + vasi + hiši.",
  s13_r6: "★★1834 Pag. 23 (10. Febr d°, ROBNA-ŠT. 13 — GRIBLJE-PAR!): (a) 'Marcus Vrb?/Vrh? GRIBLJE 58?, 19 l × Maria Haraghtinich? GRIBLJE 51, 19 l' (b) 'Marcus Vrh? GRIBLJE 68? × Maria Karafhainj? GRIBLJE 51'. VPRAŠANJA: priimek ženina (Vrh? Vrban?) ČRKO ZA ČRKO + hiša (58? 68?) + priimek neveste + hiša 51?",
  s13_r7: "1834 Pag. 23 (10. Febr d°, ROBNA-ŠT. 14): (a) 'Nicolaus Kravtuch? Crnavo?~Črnomelj? 6, 22 l × Catharina ANGEL Dobravicz? 11, 23 l' (b) 'Nicolaus Kraisfhuig? Paun Natlange? 8? × Catharina Anzel? Dobravič 11'. VPRAŠANJA: priimka + vasi + hiši (6? 8?) + ANGEL/Dobravlje?",
  s13_r8: "1834 Pag. 23 (DATUM-DUEL: 9. ali 10. Febr, ROBNA-ŠT. 15): (a) 'Peter Goymerac? Bratrina? 6, 19 l × Anna Kambich?=KAMBIČ! Kapin? 13, 20 l' (b) 'Peter Cormaray? Paunoviči? 8 × Anna Kambich? Kraönz? 13'. VPRAŠANJA: DATUM + priimka + vasi + hiši + KAMBIČ (družina Podlog 1831!)?",
  s13_r9: "1834 Pag. 23 (10. Febr d°, ROBNA-ŠT. 16): (a) 'Marius?/Mathias Katuchich? Gerhüpe? 26, 23 l × Katharina Millauer? geb. Porehen? (VDova!) Gerhüpe? 10, 32 l' (b) 'Mathias Falsfzhigl? Kerhuipa? 26 × Katharina Karafzhigl? geb. Mihliov?/Lorkel? Kerhuipa? 10'. VPRAŠANJA: priimka + vasi + hiši + ALI je nevesta vdova (geb.)?",
  s13_r10: "★★1834 Pag. 23 (10. Febr d°, ROBNA-ŠT. 17): (a) 'Mathias Rigs?/Reyer? DOBRAVLJE 13, 27 l × Barbara Novak? geb. KLOBUČAR! DOBRAVLJE 24?, 28 l' (b) 'Mathias Reyer? Dobravič 13 × Barbara Movrin? geb. Klobučar? Dobravič 34?'. VPRAŠANJA: priimka + hiša neveste (24? 34?) + geb. KLOBUČAR (vdova!)?",
  s13_r11: "1834 Pag. 23 (DATUM-DUEL: 10. ali 17. Febr, ROBNA-ŠT. 18 — zadnja vrstica): (a) 'Georg Hozhoved?/Koschheuel? Konyev?~Kostanjevica? 13, 23 l × Margareth Marentich?~MARENTIČ? DOBRAVLJE 24?, 22 l' (b) 'Georg Koschheuel? Paunoviči? Mottling? 13 × Margareth Marcuteich? Dobravič 29?'. VPRAŠANJA: DATUM + priimka + vasi + hiši.",
};

const PROMPT = (id) => `Slika je POVEČAN IZREZ (vodoravni trak, širina celega razprtega lista) poročne knjige Trauungs-Buch 01738 (Podzemelj, Kurrent-pisava, nemško). Trak obsega ENO vrstico vpisa (lahko tudi del sosednje — loči po vsebinski celovitosti!).
KONTEKST: ${H[id]}
${COLS}
Naloga: prepiši DOBESEDNO po stolpcih. Hišne številke so MAJHNE — previdno! Nejasna mesta označi z [~]. Če je trak prazen ali vsebuje dve vrstici, povej.
Izhod SAMO JSON: {"id":"${id}","vrstica":"polna/opis","datum":"","leto":0,"vasZenin":"","hisZenin":0,"zenin":"","standZenin":"","starZenin":0,"letoZenin":0,"vasNevesta":"","hisNevesta":0,"nevesta":"","standNevesta":"","starNevesta":0,"letoNevesta":0,"oceZenin":"","mataZenin":"","oceNevesta":"","mataNevesta":"","price":"","urkunde":"","duhovnik":"","xOpen":[],"razlaga":""}`;

async function run(id) {
  const out = `${DIR}/${id}.json`;
  if (fs.existsSync(out) && fs.statSync(out).size > 40) { console.error(`${id}: skip`); return; }
  const content = [{ type: 'text', text: PROMPT(id) }];
  content.push({ type: 'image_url', image_url: { url: `data:image/jpeg;base64,${fs.readFileSync(`${DIR}/${id}.jpg`).toString('base64')}` } });
  for (let a = 1; a <= 6; a++) {
    try {
      const r = await zai.chat.completions.createVision({
        messages: [{ role: 'user', content }],
        temperature: 0.1, max_tokens: 1500, thinking: { type: 'disabled' },
      });
      fs.writeFileSync(out, r.choices[0].message.content || '');
      console.error(`${id}: OK`);
      return;
    } catch (e) {
      console.error(`${id}: a${a} ${String(e).slice(0,60)}`);
      await new Promise(r2 => setTimeout(r2, 5000 * a));
    }
  }
  console.error(`${id}: FAIL`);
}
// s11 r1 je že prebrana (pilot)
const ROWS = [
  ...Array.from({ length: 13 }, (_, i) => `s11_r${i + 1}`),
  ...Array.from({ length: 12 }, (_, i) => `s12_r${i + 1}`),
  ...Array.from({ length: 11 }, (_, i) => `s13_r${i + 1}`),
];
for (const id of ROWS) {
  try { await run(id); } catch (e) { console.error(`outer ${id}: ${String(e).slice(0,80)}`); }
  await new Promise(r => setTimeout(r, 3000));
}
console.error('ROWS DONE');
