// P231 — branje probe-krop sheetov (rešitev MEJA-1874/75 uganke).
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';

const inst = await ZAI.create();
const DIR = '/tmp/p231/krops';

const TASKS = [
  { sheet: 'sheet-Q1-glave.png', prompt: `To je vertikalna zaporedja 7-izrezov-glav (zgornjih-18%) strani krstne knjige Podzemelj, označenih G45–G56 (= skeni s45–s56). Vsak izrez je ZGORNJI PAS strani s tiskano/napisano glavo.
NAJDI za vsak izrez: (1) kaj piše v glavi — tiskano 'Jahr ____' z ročno dopisano letnico? KATERA letnica je ročno dopisana (črke po cifri: npr. 'Jahr 18_75')? (2) ali je glava PRAZNA/nepopisana? (3) katera od teh strani ima 'Jahr 1875'? — POZOR: ročno dopisana letnica je KURRENT-cifra; 4 ima zanko, 7 ima prečko, 5 je lahko podobna 6/3, 8/9 po zgornji zanki.
Izhod: SAMO JSON: {"izrezi":[{"label":"G57","glava":"tocno kaj pise","letnica":"1874|1875|prazno|neberljivo","opomba":"..."}, ...]}` },
  { sheet: 'sheet-Q2-foliacije.png', prompt: `To je vertikalna zaporedja 7-izrezov (zgornji-levi-kot) strani krstne knjige, označenih F45–F56 (= skeni s45–s56); PRIČAKOVANO ZAPOREDJE: 42,43,44,45,46,47,48,49,50,51,52,53 (vzorec-'sken−5'-PAZI: lahko-je-LOMLJEN-zaradi-DUPLIKATOV-skenov!-na-s60/61/62-je-bil-TROJNI-duplikat-iste-folio-57!). V vsakem kotu je SVINČNA ročno napisana cifra (arhivarjeva foliacija!).
Preberi SVAKO svinčno cifro. Pričakovano zaporedje je 52,53,54,55,56,57,58 (vzorec 'sken−5')! Cifre so KURRENT: 4 ima zanko, 7 ima prečko, 5 je lahko podobna 6, 8/9 po zgornji zanki, 2 ima osnovo.
Izhod: SAMO JSON: {"izrezi":[{"label":"F57","cifra":"52|...|neberljiva","zanesljivost":"visoko|srednje|nizko"}, ...]}` },
  { sheet: 'sheet-Q3-prve-vrstice.png', prompt: `To je 12-izrezov (PRVE-vrstice) strani krstne knjige Podzemelj: s45–s56 (r1 vsake strani — mesec, dan rojstva/krsta, ZAPOREDNA-ŠTEVILKA-levo!, vas, hišna št., ime). ISKAMO RESTART-zaporedne-številke-na-1 (MEJA-novi-letni!-pričakovano-Januar!).
ZA VSAK izrez TOČNO preberi: (1) zaporedno številko (levo! — če je ni/prazna, reces), (2) MESEC (Jänner/Feber/März/April/Mai/Juni/July/August/September/October/November/Dezember — POZOR: 'Jänner' se začne z J-zanko, 'November' z N! Ne sklepi — poglej prvo črko!), (3) dan rojstva in dan krsta, (4) vas in hišno številko, (5) ime otroka.
Izhod: SAMO JSON: {"izrezi":[{"label":"s61-r1+2","r1":{"zap":"...","mesec":"...","roj":"...","krst":"...","vas":"...","hisna":"...","otrok":"..."},"r2":{...}}, ...]}` },
  { sheet: 'sheet-Q4-dna.png', prompt: `To je vertikalna zaporedja 6-izrezov (SPODNJIH-pasov, 20%) strani krstne knjige, označenih D45–D56 (= skeni s45–s56). ISKAMO veliko kalligrafsko zaporedje 'finis Anni 1874' (ali podobno — 'finis' veliko levo + letnica razpeto desno; PARALELA: na strani s64 obstaja takšna 'finis Anni 1875'!).
ZA VSAK izrez: (1) ali vidiš veliko kalligrafijo/kuriento napisano besedo 'finis' ALBO drugo veliko pisavo čez dno? (2) ali so vidne cifre letnice (1-8-7-4 ALI 1-8-7-5)? (3) ali je spodnji pas samo prazen (prazne vrstice tabele)?
Izhod: SAMO JSON: {"izrezi":[{"label":"D57","finis":"da|ne|nejasno","letnica":"...|null","opomba":"..."}, ...]}` },
];

for (const t of TASKS) {
  const outPath = `/tmp/p231/probe-${t.sheet.replace('sheet-', '').replace('.png', '')}.json`;
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
console.log('PROBE-READ-KONČANO');
