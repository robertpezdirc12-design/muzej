// P232 — branje probe-krop sheetov (rešitev MEJA-1873/74 uganke).
// LEAD-P231: MEJA-1873/74-PRED-s45 → pričakovana-foliacija-'sken−3' s36='33'...s44='41'.
// POZOR: 2-DUPLIKATA-pred-s45 (neznana-lokacija-s1–s44!) — zaporedje-LAHKO-skoči!
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';

const inst = await ZAI.create();
const DIR = '/tmp/p232/krops';

const TASKS = [
  { sheet: 'sheet-Q1-glave.png', prompt: `To je vertikalna zaporedja 10-izrezov-glav (zgornjih-18%) strani krstne knjige Podzemelj, označenih G36–G45 (= skeni s36–s45). Vsak izrez je ZGORNJI PAS strani s tiskano/napisano glavo.
NAJDI za vsak izrez: (1) kaj piše v glavi — tiskano 'Jahr ____' z ročno dopisano letnico? KATERA letnica je ročno dopisana (črke po cifri: npr. 'Jahr 18_74')? (2) ali je glava PRAZNA/nepopisana? (3) katera od teh strani ima 'Jahr 1874' in katera 'Jahr 1873'? — POZOR: ročno dopisana letnica je KURRENT-cifra; 4 ima zanko, 7 ima prečko, 3 je zrcalna, 8/9 po zgornji zanki.
Izhod: SAMO JSON: {"izrezi":[{"label":"G36","glava":"tocno kaj pise","letnica":"1873|1874|prazno|neberljivo","opomba":"..."}, ...]}` },
  { sheet: 'sheet-Q2-foliacije.png', prompt: `To je vertikalna zaporedja 10-izrezov (zgornji-levi-kot) strani krstne knjige, označenih F36–F45 (= skeni s36–s45); PRIČAKOVANO ZAPOREDJE (vzorec-'sken−3'): 33,34,35,36,37,38,39,40,41,42 — PAZI: zaporedje LAHKO SKOČI zaradi DUPLIKATOV skenov (2-duplikata-že-pred-s45-neznana-lokacija!-na-folio-57-je-bil-tudi-TROJNI-duplikat!). V vsakem kotu je SVINČNA ročno napisana cifra (arhivarjeva foliacija!).
Preberi SVAKO svinčno cifro. Cifre so KURRENT: 4 ima zanko, 7 ima prečko, 5 je lahko podobna 6, 8/9 po zgornji zanki, 2 ima osnovo, 3 je zrcalna-E-forma.
Izhod: SAMO JSON: {"izrezi":[{"label":"F36","cifra":"33|...|neberljiva","zanesljivost":"visoko|srednje|nizko"}, ...]}` },
  { sheet: 'sheet-Q3-prve-vrstice.png', prompt: `To je 10-izrezov (PRVE-vrstice) strani krstne knjige Podzemelj: s36–s45 (r1 vsake strani — ZAPOREDNA-ŠTEVILKA-levo!, mesec, dan rojstva/krsta, vas, hišna št., ime). ISKAMO RESTART-zaporedne-številke-na-1 (MEJA-novi-letni!-pričakovano-Januar!) in TAIL-December-vrstice (zaključek-leta-1873!).
ZA VSAK izrez TOČNO preberi: (1) zaporedno številko (levo! — če je ni/prazna, reces), (2) MESEC (Jänner/Feber/März/April/Mai/Juni/July/August/September/October/November/Dezember — POZOR: 'Jänner' se začne z J-zanko, 'November' z N, 'Dezember' z D! Ne sklepi — poglej prvo črko!), (3) dan rojstva in dan krsta, (4) vas in hišno številko, (5) ime otroka.
Izhod: SAMO JSON: {"izrezi":[{"label":"s36-r1","zap":"...","mesec":"...","roj":"...","krst":"...","vas":"...","hisna":"...","otrok":"..."}, ...]}` },
  { sheet: 'sheet-Q4-dna.png', prompt: `To je vertikalna zaporedja 10-izrezov (SPODNJIH-pasov, 20%) strani krstne knjige, označenih D36–D45 (= skeni s36–s45). ISKAMO veliko kalligrafsko zaporedje 'finis Anni 1873' (ali podobno — 'finis' veliko levo + letnica razpeto desno; PARALELA: na strani s64 obstaja takšna 'finis Anni 1875'!-velika-kalligrafija-čez-dno!). TUDI: veliki-cifri-'1'+'8' ali VSOTNA-vrsta-z-razpetimi-ciframi-čez-stolpce (PARALELA-s47-SREDI-PAGI-MEJA-1874/75!).
ZA VSAK izrez: (1) ali vidiš veliko kalligrafijo/kuriento napisano besedo 'finis' ALBO drugo veliko pisavo čez dno? (2) ali so vidne cifre letnice (1-8-7-3 ALI 1-8-7-4)? (3) ali so vidni veliki-cifri-'1'+'8' (prelom-leta-sredinsko!)? (4) ali je spodnji pas samo prazen (prazne vrstice tabele)?
Izhod: SAMO JSON: {"izrezi":[{"label":"D36","finis":"da|ne|nejasno","letnica":"...|null","velikiCifri":"...|null","opomba":"..."}, ...]}` },
];

for (const t of TASKS) {
  const outPath = `/tmp/p232/probe-${t.sheet.replace('sheet-', '').replace('.png', '')}.json`;
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
console.log('P232-PROBE-READ-KONČANO');
