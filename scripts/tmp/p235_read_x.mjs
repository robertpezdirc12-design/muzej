// P235 — branje X-DECISIVE krops (aritmetična-sidra-1:1!).
// Sheet-X1: z1-RESTART (s3r1!) + z1-DUPLIKAT (s4r1!) + z9-POST-DUP (s5r1!)
// Sheet-X2: TAIL-VERIGA (s13: r1=z97! + r2=z98-GRIBLJE! + r12=z108-TAIL!)
// Sheet-X3: DVOJČKI z72/z73 (s10 r8/r9-'Zwillings'!) + PREČRTANI z37/z38 (s7 r7/r8!)
// Sheet-X4: z80-KLOBUČAR + z81-'Peter-Pezdirc'-EKSPPLICITNO (s11 r6/r7!)
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';

const inst = await ZAI.create();
const DIR = '/tmp/p235/krops';

const TASKS = [
  { sheet: 'sheet-X1-restart-dup.png', prompt: `To je 3-izrezov vrstic krstne knjige Podzemelj (1871!). Vsak izrez = PRVA VRSTICA strani s ZAPOREDNO ŠTEVILKO na skrajnem levem robu.
K1 = s3-r1 (pričakovano zap='1' — RESTART leta 1871!-mesec Jänner-dan 3.-vas Krasinec?).
K2 = s4-r1 (pričakovano zap='1' — DUPLIKAT iste strani fol-1!-vsebina NAJ bi bila ista kot K1: Jänner-3!-POZOR: vrstica je delno pokrita z vlepljenim listom!).
K3 = s5-r1 (pričakovano zap='9' — nadaljevanje po duplikatu!-Jänner-24-Otok?).
ZA VSAK izrez TOČNO preberi: (1) zaporedno številko (SKRAJNI LEVI ROB!-ena-cifra ALBO dve!-KURRENT: 1 = ozka črtica, 9 = zanka-spodaj-desno, 7 = γ-s-prečko, 4 = z zanko, 3 = zrcalna-E!), (2) mesec (Jänner/Feber/März...), (3) dan rojstva + dan krsta, (4) vas, (5) hišno številko, (6) ime otroka.
Izhod: SAMO JSON: {"izrezi":[{"label":"K1","zap":"...","mesec":"...","roj":"...","krst":"...","vas":"...","hisna":"...","otrok":"...","opomba":"..."}, ...]}` },
  { sheet: 'sheet-X2-tail-veriga.png', prompt: `To je 3-izrezov vrstic krstne knjige Podzemelj (1871-TAIL-stran fol-10 = s13!). Vsak izrez = ena vrstica s ZAPOREDNO ŠTEVILKO na skrajnem levem robu.
T1 = s13-r1 (pričakovano zap='97' — November-16-Dobravice).
T2 = s13-r2 (pričakovano zap='98' — November-25-GRIBLJE-h6-Maria!-★KLJUČNA-GRIBLJE-vrstica!).
T3 = s13-r12 = ZADNJA-vrstica-strani (pričakovano zap='108' — Dezember-31-Otok-h31-Maria!-TAIL-1871!).
ZA VSAK izrez TOČNO preberi: (1) zaporedno številko (SKRAJNI LEVI ROB!-DVE-CIFRI!-KURRENT: 9 = zanka-spodaj-desno, 7 = γ-s-prečko, 0 = ovalna-zanka, 8 = dve-zanki-nad-soboj, 1 = ozka črtica!), (2) mesec (November/Dezember — November se začne z N, Dezember z D!), (3) dan rojstva + dan krsta, (4) vas, (5) hišno številko, (6) ime otroka.
Izhod: SAMO JSON: {"izrezi":[{"label":"T1","zap":"...","mesec":"...","roj":"...","krst":"...","vas":"...","hisna":"...","otrok":"...","opomba":"..."}, ...]}` },
  { sheet: 'sheet-X3-dvojcki-precrtani.png', prompt: `To je 4-izrezov vrstic krstne knjige Podzemelj (1871!). ISKAMO DVOJČKE in PREČRTANE vrstice:
D1 = s10-r8 (pričakovano zap='72' — Juli-9-Boršt-h20-Georg!-pripis 'Zwillings' = DVOJČEK!).
D2 = s10-r9 (pričakovano zap='73' — ISTI-dan-Boršt!-Catharina!-brano-'ib.'(idem) = DVOJČEK-od-vrstice-72!).
P1 = s7-r7 (pričakovano zap='37' — April-22-Krasinec-h12-Johan!-vrstica-LAHKO-PREČRTANA!).
P2 = s7-r8 (pričakovano zap='38' — April-22-Krasinec-h12-Maria!-vrstica-LAHKO-PREČRTANA!).
ZA VSAK izrez TOČNO preberi: (1) zaporedno številko (SKRAJNI LEVI ROB!-KURRENT: 7 = γ-s-prečko, 2 = s-osnovo, 3 = zrcalna-E, 8 = dve-zanki!), (2) mesec + dan rojstva + dan krsta, (3) vas + hišno št., (4) ime otroka, (5) ★★★ ALI je vrstica PREČRTANA (črta-čez-besedilo!-X-oznaka!-pika!)? — odgovori 'DA-celotna' / 'DA-delno' / 'NE' + kaj piše v opombi čez vrstico.
Izhod: SAMO JSON: {"izrezi":[{"label":"D1","zap":"...","mesec":"...","roj":"...","krst":"...","vas":"...","hisna":"...","otrok":"...","precrtano":"DA-celotna|DA-delno|NE","opomba":"..."}, ...]}` },
  { sheet: 'sheet-X4-pezdirc-klobucar.png', prompt: `To je 2-izrezov vrstic krstne knjige Podzemelj (1871-September!).
Z1 = s11-r6 (pričakovano zap='80' — September-15-GRIBLJE-h48-Mathias!-oče 'Joanes Klobučar'!).
Z2 = s11-r7 (pričakovano zap='81' — September-19-GRIBLJE-h28-Joanes!-★★★ oče NAJ bi bil 'Peter Pezdirc' — EKSPPLICITNO-'Pezdirc'!-KLJUČNA-pezdirc-nit!).
ZA VSAK izrez TOČNO preberi: (1) zaporedno številko (SKRAJNI LEVI ROB!-KURRENT: 8 = dve-zanki, 0 = ovalna, 1 = ozka črtica!), (2) mesec + dan, (3) vas + hišno št., (4) ime otroka, (5) OČET: ime + priimek (PREBERI-NATAČNO-priimek!-'Klobučar'/'Pezdirc'-KURRENT-razločevanje-K-P-začetnica!), (6) MATI, (7) BOTRA.
Izhod: SAMO JSON: {"izrezi":[{"label":"Z1","zap":"...","mesec":"...","roj":"...","krst":"...","vas":"...","hisna":"...","otrok":"...","ocec":"...","matec":"...","botra":"...","opomba":"..."}, ...]}` },
];

for (const t of TASKS) {
  const outPath = `/tmp/p235/x-${t.sheet.replace('sheet-', '').replace('.png', '')}.json`;
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
  await new Promise(r => setTimeout(r, 15000));
}
console.log('P235-X-READ-KONČANO');
