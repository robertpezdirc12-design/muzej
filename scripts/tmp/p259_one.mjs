// P259 — ONE-SHOT: prebere ENO vrstico (id kot argv[2]) in izstopa. Upravlja bash-zanka.
import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';

const id = process.argv[2];
if (!id) { console.error('UPORABA: bun p259_one.mjs s11_r2'); process.exit(2); }
const DIR = '/tmp/p259/full';
const out = `${DIR}/${id}.json`;
if (fs.existsSync(out) && fs.statSync(out).size > 40) { console.error(`${id}: ze-obstaja`); process.exit(0); }

const H = JSON.parse(fs.readFileSync('/tmp/p259/hints.json', 'utf-8'));
const COLS = `Stolpci LEVE strani razprtega lista: [Jahr/Monat/Tag der Trauung] [Wohnort ŽENINA] [Haus-Nr] [Taufname+Familien-Name+Stand ŽENINA] [Alter] | DESNE strani: [Eltern des Bräutigams] [Eltern der Braut] [Zeugen] [Urkunden] [Unterschrift des trauenden Priesters]`;
const PROMPT = `Slika je POVEČAN IZREZ (vodoravni trak, širina celega razprtega lista) poročne knjige Trauungs-Buch 01738 (Podzemelj, Kurrent-pisava, nemško). Trak obsega ENO vrstico vpisa (lahko tudi del sosednje — loči po vsebinski celovitosti!).
KONTEKST: ${H[id]}
${COLS}
Naloga: prepiši DOBESEDNO po stolpcih. Hišne številke so MAJHNE — previdno! Nejasna mesta označi z [~]. Če je trak prazen ali vsebuje dve vrstici, povej.
Izhod SAMO JSON: {"id":"${id}","vrstica":"polna/opis","datum":"","leto":0,"vasZenin":"","hisZenin":0,"zenin":"","standZenin":"","starZenin":0,"letoZenin":0,"vasNevesta":"","hisNevesta":0,"nevesta":"","standNevesta":"","starNevesta":0,"letoNevesta":0,"oceZenin":"","mataZenin":"","oceNevesta":"","mataNevesta":"","price":"","urkunde":"","duhovnik":"","xOpen":[],"razlaga":""}`;

const zai = await ZAI.create();
const content = [{ type: 'text', text: PROMPT }];
content.push({ type: 'image_url', image_url: { url: `data:image/jpeg;base64,${fs.readFileSync(`${DIR}/${id}.jpg`).toString('base64')}` } });
const r = await zai.chat.completions.createVision({
  messages: [{ role: 'user', content }],
  temperature: 0.1, max_tokens: 1500, thinking: { type: 'disabled' },
});
const c = r.choices[0].message.content || '';
if (c.length < 30) { console.error(`${id}: prekratko`); process.exit(1); }
fs.writeFileSync(out, c);
console.error(`${id}: OK (${c.length})`);
process.exit(0);
