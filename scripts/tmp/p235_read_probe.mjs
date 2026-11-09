// P235 — branje probe-krop sheetov (rešitev MEJA-1870/71 + UREJANJE-KONCA-LINIJE uganke).
// LEAD-P234: MEJA-1871/72 = ŽE-DOKAZANA-s13/s14 (restart-z1-NA-s14-r1!-X-SUPER-POTRJEN!-12.-restart!)
//   → probe-s9–s13-DESCENDING! Pričakovana-foliacija-'sken−3': s13='10'-s12='9'-s11='8'-s10='7'-s9='6'! (s14='11'-P234!)
//   + dvojica-B s1–s8: UREJANJE-KONCA-LINIJE (meja-1870/71-LAHKO-že-tukaj!-ali-knjiga-začne-z-1871!-s1-majhna-150KB!)
// ★★★ POZOR: 1-DUPLIKAT-še-vedno-neznana-lokacija-s1–s13! TROJNI-s60=s61=s62-P231 + s28=s29-P234! Zaporedje-LAHKO-skoči!
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';

const inst = await ZAI.create();
const DIR = '/tmp/p235/krops';

const TASKS = [
  { sheet: 'sheet-A-Q1-glave.png', prompt: `To je vertikalna zaporedja 5-izrezov-glav (zgornjih-18%) strani krstne knjige Podzemelj, označenih G9–G13 (= skeni s9–s13). Vsak izrez je ZGORNJI PAS strani s tiskano/napisano glavo.
NAJDI za vsak izrez: (1) kaj piše v glavi — tiskano 'Jahr ____' z ročno dopisano letnico? KATERA letnica je ročno dopisana (črke po cifri: npr. 'Jahr 18_71')? (2) ali je glava PRAZNA/nepopisana? (3) katera od teh strani ima 'Jahr 1871' in katera drugo leto? — POZOR: ročno dopisana letnica je KURRENT-cifra; 4 ima zanko, 7 ima prečko, 3 je zrcalna, 8/9 po zgornji zanki, 2 ima osnovo, 1 je ozka črtica.
ZNANO: naslednja-stran-s14 = 'Jahr 1872' (P234-potrjeno!) — pričakujemo VSE teh 5 = 'Jahr 1871', a zaporedje LAHKO skoči zaradi DUPLIKATOV skenov!
Izhod: SAMO JSON: {"izrezi":[{"label":"G9","glava":"tocno kaj pise","letnica":"1870|1871|1872|prazno|neberljivo","opomba":"..."}, ...]}` },
  { sheet: 'sheet-A-Q2-foliacije.png', prompt: `To je vertikalna zaporedja 5-izrezov (zgornji-levi-kot) strani krstne knjige, označenih F9–F13 (= skeni s9–s13); PRIČAKOVANO ZAPOREDJE (vzorec-'sken−3'): 6,7,8,9,10 — PAZI: zaporedje LAHKO SKOČI zaradi DUPLIKATA skenov (1-duplikat-še-vedno-neznana-lokacija-s1–s13!-na-folio-25-je-bil-DUPLIKAT-s28=s29-P234!-na-folio-57-TROJNI-s60=s61=s62-P231!). V vsakem kotu je SVINČNA ročno napisana cifra (arhivarjeva foliacija!).
Preberi SVAKO svinčno cifro. Cifre so KURRENT: 4 ima zanko, 7 ima prečko, 5 je lahko podobna 6, 8/9 po zgornji zanki, 2 ima osnovo, 3 je zrcalna-E-forma, 1 je ozka črtica.
ZNANO: F14 (naslednja) = '11' (P234-potrjeno!) — uporabi kot KALIBRACIJO pisave!
Izhod: SAMO JSON: {"izrezi":[{"label":"F9","cifra":"6|...|neberljiva","zanesljivost":"visoko|srednje|nizko"}, ...]}` },
  { sheet: 'sheet-A-Q3-prve-vrstice.png', prompt: `To je 5-izrezov (PRVE-vrstice) strani krstne knjige Podzemelj: s9–s13 (r1 vsake strani — ZAPOREDNA-ŠTEVILKA-levo!, mesec, dan rojstva/krsta, vas, hišna št., ime). ISKAMO: (A) MEJA-1870/71 = RESTART-zaporedne-številke-na-1 (pričakovano-Jänner!-lahko-KJER-KOLI-v-s1–s13!-1871-LETO-KONCA-LINIJE!) in (B) TAIL-1871-Dezember-vrstice (zaključek-leta-1871!-s13-tail-pričakovano-12-vrstic!) in (C) 1871-nadaljevanje-s9–s13.
ZNANO: s14-r1 = zap-1-Jänner-5-GRIBLJE-h11-Mathias (P234-potrjeno!-MEJA-1871/72-PAGE-BOUNDARY!-1872-že-teče!-restart-12.-restart!).
ZA VSAK izrez TOČNO preberi: (1) zaporedno številko (levo! — če je ni/prazna, reces), (2) MESEC (Jänner/Feber/März/April/Mai/Juni/July/August/September/October/November/Dezember — POZOR: 'Jänner' se začne z J-zanko, 'November' z N, 'Dezember' z D! Ne sklepi — poglej prvo črko!), (3) dan rojstva in dan krsta, (4) vas in hišno številko, (5) ime otroka.
Izhod: SAMO JSON: {"izrezi":[{"label":"s9-r1","zap":"...","mesec":"...","roj":"...","krst":"...","vas":"...","hisna":"...","otrok":"..."}, ...]}` },
  { sheet: 'sheet-A-Q4-dna.png', prompt: `To je vertikalna zaporedja 5-izrezov (SPODNJIH-pasov, 20%) strani krstne knjige, označenih D9–D13 (= skeni s9–s13). ISKAMO veliko kalligrafsko zaporedje 'finis Anni 1871' (ali podobno — 'finis' veliko levo + letnica razpeto desno; PARALELA: na strani s64 obstaja takšna 'finis Anni 1875'!) ALBO 'Initium anni Domini 1871' (PARALELA-P232-'Initium-anni-Domini-1874'-s37-SREDI-PAGI!). TUDI: veliki-cifri-'1'+'8' ali VSOTNA-vrsta-z-razpetimi-ciframi-čez-stolpce.
ZA VSAK izrez: (1) ali vidiš veliko kalligrafijo/kuriento napisano besedo 'finis' ALBO 'Initium' ALBO drugo veliko pisavo čez dno? (2) ali so vidne cifre letnice (1-8-7-1 ALI 1-8-7-2)? (3) ali so vidni veliki-cifri-'1'+'8' (prelom-leta-sredinsko!)? (4) ali je spodnji pas samo prazen (prazne vrstice tabele)?
Izhod: SAMO JSON: {"izrezi":[{"label":"D9","finis":"da|ne|nejasno","initium":"da|ne|nejasno","letnica":"...|null","velikiCifri":"...|null","opomba":"..."}, ...]}` },
  { sheet: 'sheet-B-Q1-glave.png', prompt: `To je vertikalna zaporedja 8-izrezov-glav (zgornjih-18%) strani krstne knjige Podzemelj, označenih G1–G8 (= skeni s1–s8). Vsak izrez je ZGORNJI PAS strani s tiskano/napisano glavo (ALI naslovno stran!).
NAJDI za vsak izrez: (1) kaj piše v glavi — tiskano 'Jahr ____' z ročno dopisano letnico? KATERA letnica je ročno dopisana? (2) ali je glava PRAZNA/nepopisana (ali naslovna-stran-knjige!)? (3) katera od teh strani ima 'Jahr 1870' in katera 'Jahr 1871'? — POZOR: ročno dopisana letnica je KURRENT-cifra; 4 ima zanko, 7 ima prečko, 3 je zrcalna, 8/9 po zgornji zanki, 2 ima osnovo, 1 je ozka črtica.
ZNANO: G9 (naslednja-dvojica) = pričakovano 'Jahr 1871' — uporabi kot KONTEKST! POZOR: s1 = majhna-datoteka (verjetno NASLOVNA-STRAN-knjige ALBO prazna-forma!).
Izhod: SAMO JSON: {"izrezi":[{"label":"G1","glava":"tocno kaj pise","letnica":"1870|1871|1872|naslovna|prazno|neberljivo","opomba":"..."}, ...]}` },
  { sheet: 'sheet-B-Q2-foliacije.png', prompt: `To je vertikalna zaporedja 8-izrezov (zgornji-levi-kot) strani krstne knjige, označenih F1–F8 (= skeni s1–s8); PRIČAKOVANO ZAPOREDJE (vzorec-'sken−3'-'kontinuiteta-iz-s9–s13-pričakovanih-6–10'): če-formula-drži → s9='6' → s8='5'-s7='4'-s6='3'-s5='2'-s4='1'-s3='?'-... — PAZI: zaporedje LAHKO SKOČI zaradi DUPLIKATA skenov (1-duplikat-še-vedno-neznana-lokacija-s1–s13!). V vsakem kotu je SVINČNA ročno napisana cifra (arhivarjeva foliacija!) — ALI je kot PRAZEN (brez-cifre!-npr.-naslovna-stran!).
Preberi SVAKO svinčno cifro (ali PRAZNO). Cifre so KURRENT: 4 ima zanko, 7 ima prečko, 5 je lahko podobna 6, 8/9 po zgornji zanki, 2 ima osnovo, 3 je zrcalna-E-forma, 1 je ozka črtica.
Izhod: SAMO JSON: {"izrezi":[{"label":"F1","cifra":"5|...|prazno|neberljiva","zanesljivost":"visoko|srednje|nizko"}, ...]}` },
  { sheet: 'sheet-B-Q3-prve-vrstice.png', prompt: `To je 8-izrezov (PRVE-vrstice) strani krstne knjige Podzemelj: s1–s8 (r1 vsake strani — ZAPOREDNA-ŠTEVILKA-levo!, mesec, dan rojstva/krsta, vas, hišna št., ime). ISKAMO: (A) MEJA-1870/71 = RESTART-zaporedne-številke-na-1 (pričakovano-Jänner!-1871 = 15/15-ZADNJE-LETO-LINIJE!-lahko-KJER-KOLI!) in (B) TAIL-1870-Dezember-vrstice (če-knjiga-začne-z-1870!) in (C) 1871-zacetek (Jänner-1871!-1.-vpis-leta!).
ZNANO: s9–s13-r1 = pričakovano-1871-nadaljevanje (zap-~20–60!) — uporabi kot KONTEKST! POZOR: s1/s2 = majhni-datoteki (verjetno NASLOVNA-STRAN ALBO naslovnica+prva-pag!).
ZA VSAK izrez TOČNO preberi: (1) zaporedno številko (levo! — če je ni/prazna, reces), (2) MESEC (Jänner/Feber/März/April/Mai/Juni/July/August/September/October/November/Dezember — POZOR: 'Jänner' se začne z J-zanko, 'November' z N, 'Dezember' z D! Ne sklepi — poglej prvo črko!), (3) dan rojstva in dan krsta, (4) vas in hišno številko, (5) ime otroka.
Izhod: SAMO JSON: {"izrezi":[{"label":"s1-r1","zap":"...","mesec":"...","roj":"...","krst":"...","vas":"...","hisna":"...","otrok":"..."}, ...]}` },
  { sheet: 'sheet-B-Q4-dna.png', prompt: `To je vertikalna zaporedja 8-izrezov (SPODNJIH-pasov, 20%) strani krstne knjige, označenih D1–D8 (= skeni s1–s8). ISKAMO veliko kalligrafsko zaporedje 'finis Anni 1870' (če-knjiga-začne-z-1870!-PARALELA-'finis-Anni-1875'-s64!) ALBO 'Initium anni Domini 1871' (PARALELA-P232-'Initium-anni-Domini-1874'!). TUDI: veliki-cifri-'1'+'8' ali VSOTNA-vrsta-z-razpetimi-ciframi-čez-stolpce.
ZA VSAK izrez: (1) ali vidiš veliko kalligrafijo/kuriento napisano besedo 'finis' ALBO 'Initium' ALBO drugo veliko pisavo čez dno? (2) ali so vidne cifre letnice (1-8-7-0 ALI 1-8-7-1)? (3) ali so vidni veliki-cifri-'1'+'8' (prelom-leta-sredinsko!)? (4) ali je spodnji pas samo prazen (prazne vrstice tabele)?
Izhod: SAMO JSON: {"izrezi":[{"label":"D1","finis":"da|ne|nejasno","initium":"da|ne|nejasno","letnica":"...|null","velikiCifri":"...|null","opomba":"..."}, ...]}` },
];

for (const t of TASKS) {
  const outPath = `/tmp/p235/probe-${t.sheet.replace('sheet-', '').replace('.png', '')}.json`;
  if (fs.existsSync(outPath)) { console.log(`${t.sheet}: ŽE`); continue; }
  const b64 = fs.readFileSync(`${DIR}/${t.sheet}`).toString('base64');
  let done = false;
  for (let attempt = 1; attempt <= 4 && !done; attempt++) {
    try {
      const r = await Promise.race([
        inst.chat.completions.createVision({
          messages: [{ role: 'user', content: [
            { type: 'text', text: t.prompt },
            { type: 'image_url', image_url: { url: `data:image/png;base64,${b64}` } }
          ]}],
          thinking: { type: 'disabled' }
        }),
        new Promise((_, rej) => setTimeout(() => rej(new Error('timeout')), 240000))
      ]);
      const c = r?.choices?.[0]?.message?.content || '';
      const a = c.indexOf('{'), b = c.lastIndexOf('}');
      if (a < 0 || b < 0) throw new Error('ni JSON');
      const j = JSON.parse(c.slice(a, b + 1));
      fs.writeFileSync(outPath, JSON.stringify(j, null, 2));
      console.log(`${t.sheet}: OK -> ${outPath}`);
      done = true;
    } catch (e) {
      console.error(`${t.sheet}: poskus ${attempt} FAIL ${e.message.slice(0, 80)}`);
      if (/429|Too many/.test(e.message)) await new Promise(r2 => setTimeout(r2, 45000));
      else await new Promise(r2 => setTimeout(r2, 8000));
    }
  }
  if (!done) console.error(`${t.sheet}: KONČNO-FAIL`);
  await new Promise(r => setTimeout(r, 20000));
}
console.log('P235-PROBE-READ-KONČANO');
