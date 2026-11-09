// P234 — branje X-DECISIVE sheeta (zap-veriga-kalibracija s19–s31!).
// ★★★ ODLOČA: (A) 1872-start NA-s19-r1 (z1!) vs PRED-s19 (z51!); (B) P233-model-s28=11–21 vs restart-z1-s26!
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';

const inst = await ZAI.create();
const DIR = '/tmp/p234/krops';

const CTX = `To je vertikalna zaporedja 17-IZREZOV (povečava ×2.8) iz KRSTNE matične knjige župnije Podzemelj, leta 1872–1873 (STAREJŠA Kurrent-pisava z nemškim gotskim vplivom). Vsak izrez = LEVI-DEL ENE vrstice tabele: zaporedna-številka (najbolj levo, ročno zapisana!) + mesec + dan rojstva/krsta (+ del vasi/hišne-št.).
★★★ KLJUČNA-NALOGA: preberi ZAPOREDNO-ŠTEVILKO (prvo-številko-levo!) na VSAKEM izrezu TOČNO — CIFRE-so-KURRENT: '1' = ozka-črtica (lahko-s-serifom-na-dnu!-BREZ-zanke!), '2' ima-osnovo-in-zgornjo-zanko, '3' = zrcalna-E, '4' ima-zanko, '5' = zgornja-črta+spodnja-zanka, '7' = γ-forma-s-prečko, '8' = dve-zanki, '9' = zanka-spodaj+rep, '0' = oval.
★★★ POZOR-na-DVOJKE: zaporedna-številka-je-PISANA-ROČNO-in-lahko-ima-PREDPONOVO/popravek; hišna-št.-je-DRUGI-stolpec (ne-zamenjuj!); dnevi-so-MALA-cifre-s-piko ('3.').
MESeci: Jänner, Feber, März, April, Mai, Juni, July, August, September, October, November, Dezember (J-zanka-pri-Jänner/Juni/July!-N-pri-November!-D-pri-Dezember!-M-pri-März/Mai!).
ZNANE-KONTROLE (kalibracija!): I2 (zadnji-izrez) = s31-r11 = ZAP-'51' (X-POTRJEN-v-P233!-uporabi-kot-KALIBRACIJO!); F = s28-r1.
Zapiši TOČNO kaj vidiš; negotovo z [~], neberljivo z [?].`;

const ITEMS = ['A s19-r1', 'A2 s19-r9', 'B s20-r1', 'C s25-r4', 'C2 s25-r5', 'D s26-r1', 'D2 s26-r11', 'E s27-r1', 'E2 s27-r10', 'F s28-r1', 'F2 s28-r11', 'G s29-r1', 'G2 s29-r11', 'H s30-r1', 'H2 s30-r8', 'I s31-r1', 'I2 s31-r11'];

const prompt = `${CTX}

Izrezi (zaporedje po labelah): ${ITEMS.join(' | ')}.

Izhod: SAMO veljaven JSON:
{"izrezi":[{"label":"A","zap":"...|null","zapZanesljivost":"visoko|srednje|nizko","mesec":"...|null","roj":"...|null","krst":"...|null","vas":"...|null","hisna":"...|null","otrok":"...|null","opomba":"...|null"}, ...]}`;

let done = false;
for (let attempt = 1; attempt <= 4 && !done; attempt++) {
  try {
    const b64 = fs.readFileSync(`${DIR}/X-DECISIVE.png`).toString('base64');
    const r = await Promise.race([
      inst.chat.completions.createVision({
        messages: [{ role: 'user', content: [
          { type: 'text', text: prompt },
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
    fs.writeFileSync('/tmp/p234/xread-DECISIVE.json', JSON.stringify(j, null, 2));
    console.log('X-DECISIVE: OK', j.izrezi?.length, 'izrezov');
    for (const i of j.izrezi || []) console.log(`  ${i.label}: zap=${i.zap} (${i.zapZanesljivost}) mesec=${i.mesec} vas=${i.vas} otrok=${i.otrok}`);
    done = true;
  } catch (e) {
    console.error(`poskus ${attempt} FAIL ${e.message.slice(0, 100)}`);
    if (/429|Too many/.test(e.message)) await new Promise(r2 => setTimeout(r2, 45000));
    else await new Promise(r2 => setTimeout(r2, 8000));
  }
}
if (!done) console.error('KONČNO-FAIL');
console.log('X-DECISIVE-READ-KONČANO');
