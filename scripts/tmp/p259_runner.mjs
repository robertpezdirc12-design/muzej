import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';

// POZOR: SDK-jeve napake (429/socket) se včasih pojavijo kot NEULOVLJENE (background promise) —
// globalni handlerji jih pogoltnijo, da proces ne umre (poskusna logika je v run()).
process.on('uncaughtException', (e) => { try { fs.appendFileSync('/tmp/p259/runner.log', `UNCAUGHT ${String(e).slice(0, 80)}\n`); } catch {} });
process.on('unhandledRejection', (e) => { try { fs.appendFileSync('/tmp/p259/runner.log', `UNHANDLED ${String(e).slice(0, 80)}\n`); } catch {} });

const zai = await ZAI.create();
const DIR = '/tmp/p259/full';
const LOG = '/tmp/p259/runner.log';

const COLS = `Stolpci LEVE strani razprtega lista: [Jahr/Monat/Tag der Trauung] [Wohnort ŽENINA] [Haus-Nr] [Taufname+Familien-Name+Stand ŽENINA] [Alter] | DESNE strani: [Eltern des Bräutigams] [Eltern der Braut] [Zeugen] [Urkunden] [Unterschrift des trauenden Priesters]`;

const H = JSON.parse(fs.readFileSync('/tmp/p259/hints.json', 'utf-8'));

const PROMPT = (id) => `Slika je POVEČAN IZREZ (vodoravni trak, širina celega razprtega lista) poročne knjige Trauungs-Buch 01738 (Podzemelj, Kurrent-pisava, nemško). Trak obsega ENO vrstico vpisa (lahko tudi del sosednje — loči po vsebinski celovitosti!).
KONTEKST: ${H[id]}
${COLS}
Naloga: prepiši DOBESEDNO po stolpcih. Hišne številke so MAJHNE — previdno! Nejasna mesta označi z [~]. Če je trak prazen ali vsebuje dve vrstici, povej.
Izhod SAMO JSON: {"id":"${id}","vrstica":"polna/opis","datum":"","leto":0,"vasZenin":"","hisZenin":0,"zenin":"","standZenin":"","starZenin":0,"letoZenin":0,"vasNevesta":"","hisNevesta":0,"nevesta":"","standNevesta":"","starNevesta":0,"letoNevesta":0,"oceZenin":"","mataZenin":"","oceNevesta":"","mataNevesta":"","price":"","urkunde":"","duhovnik":"","xOpen":[],"razlaga":""}`;

function log(s) { fs.appendFileSync(LOG, `${new Date().toISOString().slice(11, 19)} ${s}\n`); }

const ROWS = [
  ...Array.from({ length: 13 }, (_, i) => `s11_r${i + 1}`),
  ...Array.from({ length: 12 }, (_, i) => `s12_r${i + 1}`),
  ...Array.from({ length: 11 }, (_, i) => `s13_r${i + 1}`),
];

async function run(id) {
  const out = `${DIR}/${id}.json`;
  if (fs.existsSync(out) && fs.statSync(out).size > 40) { log(`${id}: skip`); return true; }
  const content = [{ type: 'text', text: PROMPT(id) }];
  content.push({ type: 'image_url', image_url: { url: `data:image/jpeg;base64,${fs.readFileSync(`${DIR}/${id}.jpg`).toString('base64')}` } });
  for (let a = 1; a <= 25; a++) {
    try {
      const r = await zai.chat.completions.createVision({
        messages: [{ role: 'user', content }],
        temperature: 0.1, max_tokens: 1500, thinking: { type: 'disabled' },
      });
      const c = r.choices[0].message.content || '';
      if (c.length < 30) throw new Error('prekratko');
      fs.writeFileSync(out, c);
      log(`${id}: OK (${c.length})`);
      return true;
    } catch (e) {
      const msg = String(e).slice(0, 50);
      const is429 = msg.includes('429');
      log(`${id}: a${a} ${msg}`);
      await new Promise(r2 => setTimeout(r2, is429 ? Math.min(90000, 20000 + a * 10000) : 5000));
    }
  }
  log(`${id}: FAIL-25`);
  return false;
}

let ok = 0, fail = 0;
for (const id of ROWS) {
  const r = await run(id);
  if (r) { ok++; } else { fail++; }
  await new Promise(r => setTimeout(r, 2500));
}
log(`RUNNER DONE ok=${ok} fail=${fail}`);
