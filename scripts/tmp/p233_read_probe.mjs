// P233 — branje probe-krop sheetov (rešitev MEJA-1872/73 uganke).
// LEAD-P232: MEJA-1872/73-PRED-s36 → pričakovana-foliacija-'sken−3' s28='25'...s36='33' (P232-potrjena!).
// POZOR: 2-DUPLIKATA-pred-s36 (neznana-lokacija-s1–s35!) — zaporedje-LAHKO-skoči!
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';

const inst = await ZAI.create();
const DIR = '/tmp/p233/krops';

const TASKS = [
  { sheet: 'sheet-Q1-glave.png', prompt: `To je vertikalna zaporedja 9-izrezov-glav (zgornjih-18%) strani krstne knjige Podzemelj, označenih G28–G36 (= skeni s28–s36). Vsak izrez je ZGORNJI PAS strani s tiskano/napisano glavo.
NAJDI za vsak izrez: (1) kaj piše v glavi — tiskano 'Jahr ____' z ročno dopisano letnico? KATERA letnica je ročno dopisana (črke po cifri: npr. 'Jahr 18_73')? (2) ali je glava PRAZNA/nepopisana? (3) katera od teh strani ima 'Jahr 1873' in katera 'Jahr 1872'? — POZOR: ročno dopisana letnica je KURRENT-cifra; 4 ima zanko, 7 ima prečko, 3 je zrcalna, 8/9 po zgornji zanki, 2 ima osnovo.
ZNANO: s36 (zadnji izrez G36) = 'Jahr 1873' (P232-potrjeno!) — uporabi kot KALIBRACIJO pisave!
Izhod: SAMO JSON: {"izrezi":[{"label":"G28","glava":"tocno kaj pise","letnica":"1872|1873|prazno|neberljivo","opomba":"..."}, ...]}` },
  { sheet: 'sheet-Q2-foliacije.png', prompt: `To je vertikalna zaporedja 9-izrezov (zgornji-levi-kot) strani krstne knjige, označenih F28–F36 (= skeni s28–s36); PRIČAKOVANO ZAPOREDJE (vzorec-'sken−3'): 25,26,27,28,29,30,31,32,33 — PAZI: zaporedje LAHKO SKOČI zaradi DUPLIKATOV skenov (2-duplikata-še-vedno-neznana-lokacija-s1–s35!-na-folio-57-je-bil-tudi-TROJNI-duplikat!). V vsakem kotu je SVINČNA ročno napisana cifra (arhivarjeva foliacija!).
Preberi SVAKO svinčno cifro. Cifre so KURRENT: 4 ima zanko, 7 ima prečko, 5 je lahko podobna 6, 8/9 po zgornji zanki, 2 ima osnovo, 3 je zrcalna-E-forma.
ZNANO: F36 (zadnji izrez) = '33' (P232-potrjeno!) — uporabi kot KALIBRACIJO pisave!
Izhod: SAMO JSON: {"izrezi":[{"label":"F28","cifra":"25|...|neberljiva","zanesljivost":"visoko|srednje|nizko"}, ...]}` },
  { sheet: 'sheet-Q3-prve-vrstice.png', prompt: `To je 9-izrezov (PRVE-vrstice) strani krstne knjige Podzemelj: s28–s36 (r1 vsake strani — ZAPOREDNA-ŠTEVILKA-levo!, mesec, dan rojstva/krsta, vas, hišna št., ime). ISKAMO RESTART-zaporedne-številke-na-1 (MEJA-novi-letni-1873!-pričakovano-Januar-Jänner!) in TAIL-1872-December-vrstice (zaključek-leta-1872!) in November-1873-nadaljevanje.
ZNANO: s36-r1 = zap-88-November-24-Vranoviče (P232-potrjeno!-1873-teče-naprej!).
ZA VSAK izrez TOČNO preberi: (1) zaporedno številko (levo! — če je ni/prazna, reces), (2) MESEC (Jänner/Feber/März/April/Mai/Juni/July/August/September/October/November/Dezember — POZOR: 'Jänner' se začne z J-zanko, 'November' z N, 'Dezember' z D! Ne sklepi — poglej prvo črko!), (3) dan rojstva in dan krsta, (4) vas in hišno številko, (5) ime otroka.
Izhod: SAMO JSON: {"izrezi":[{"label":"s28-r1","zap":"...","mesec":"...","roj":"...","krst":"...","vas":"...","hisna":"...","otrok":"..."}, ...]}` },
  { sheet: 'sheet-Q4-dna.png', prompt: `To je vertikalna zaporedja 9-izrezov (SPODNJIH-pasov, 20%) strani krstne knjige, označenih D28–D36 (= skeni s28–s36). ISKAMO veliko kalligrafsko zaporedje 'finis Anni 1872' (ali podobno — 'finis' veliko levo + letnica razpeto desno; PARALELA: na strani s64 obstaja takšna 'finis Anni 1875'!-velika-kalligrafija-čez-dno!) ALBO 'Initium anni Domini 1873' (PARALELA-P232-'Initium-anni-Domini-1874'-s37-SREDI-PAGI!). TUDI: veliki-cifri-'1'+'8' ali VSOTNA-vrsta-z-razpetimi-ciframi-čez-stolpce.
ZA VSAK izrez: (1) ali vidiš veliko kalligrafijo/kuriento napisano besedo 'finis' ALBO 'Initium' ALBO drugo veliko pisavo čez dno? (2) ali so vidne cifre letnice (1-8-7-2 ALI 1-8-7-3)? (3) ali so vidni veliki-cifri-'1'+'8' (prelom-leta-sredinsko!)? (4) ali je spodnji pas samo prazen (prazne vrstice tabele)?
Izhod: SAMO JSON: {"izrezi":[{"label":"D28","finis":"da|ne|nejasno","initium":"da|ne|nejasno","letnica":"...|null","velikiCifri":"...|null","opomba":"..."}, ...]}` },
];

for (const t of TASKS) {
  const outPath = `/tmp/p233/probe-${t.sheet.replace('sheet-', '').replace('.png', '')}.json`;
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
console.log('P233-PROBE-READ-KONČANO');
