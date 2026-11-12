// P259 — ONE-SHOT pagcheck (11|12|13): foliacijske številke na zgornjem robu.
import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';
const s = process.argv[2];
if (![11, 12, 13].includes(Number(s))) { console.error('UPORABA: bun p259_pag_one.mjs 11|12|13'); process.exit(2); }
const out = `/tmp/p259/pag_s${s}.json`;
if (fs.existsSync(out) && fs.statSync(out).size > 30) { console.error(`s${s}: ze-obstaja`); process.exit(0); }
const PAG = `Slika je ZGORNJI ROB (pas 130 px, povečan ×2) skena razprtega lista (dve strani) poročne knjige Trauungs-Buch 01738.
Na sredini je tiskana glava; ZGORAJ LEVO nad levo stranjo in ZGORAJ (ob sredini/desno) nad desno stranjo so lahko SVINČNIKOVE foliacijske številke (ročno zapisane, npr. '19', '20', '21'...).
Previdno preberi VSE številke/pisma, ki jih vidiš na zgornjem robu, in njihov približen položaj (levo/sredina/desno). Ne ugibaj — če ni številke, reci 'ni'.
Izhod SAMO JSON: {"levo":"","sredina":"","desno":"","opis":""}`;
const zai = await ZAI.create();
const content = [{ type: 'text', text: PAG }];
content.push({ type: 'image_url', image_url: { url: `data:image/jpeg;base64,${fs.readFileSync(`/tmp/p259/hdr_s${s}.jpg`).toString('base64')}` } });
const r = await zai.chat.completions.createVision({
  messages: [{ role: 'user', content }],
  temperature: 0.1, max_tokens: 400, thinking: { type: 'disabled' },
});
const c = r.choices[0].message.content || '';
if (c.length < 20) { console.error(`s${s}: prekratko`); process.exit(1); }
fs.writeFileSync(out, c);
console.error(`s${s}: OK`);
process.exit(0);
