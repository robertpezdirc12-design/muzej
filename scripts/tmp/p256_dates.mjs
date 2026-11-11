import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';
const DIR = '/tmp/p256/dates';
const zai = await ZAI.create();

const CELLS = [];
for (const [tag, n] of [['s4', 9], ['s5', 8], ['s6', 11], ['s7', 13]])
  for (let i = 1; i <= n; i++) CELLS.push(`${tag}_d${i}`);

const PROMPT = `Slika je POVEČANA (×3) datumski celica iz poročne knjige Trauungs-Buch 01738 (Podzemelj, 1829–1831, Kurrent-pisava). Celica vsebuje leto/mesec/dan poroke. Nemške okrajšave mesecov: Jän(n) = Jänner, Febr/Fe = Februar, Mär = März, Ap(ril) = April, Mai, Jun(i), Jul(i), Aug, Sept, Okt(=8br!), Nov, Dez. Kurent številke: '3'=flat-top, '2'=zankasta, '1'=črt, '4'=odprt-krož, '8'=dvojna-zanka, '9'=zanka+rep, '0'=krož. DITTO (vmestno pomeni 'isto kot zgoraj') je lahko črta ali prazno. Letnica (npr. 1829/1830/1831) je lahko napisana ENKRAT na vrhu (nato ditto).
Izhod SAMO JSON: {"leto":"","mesec":"","dan":"","dittoOdZgoraj":true/false,"besedilo":"","razlaga":"","zanesljivost":"visoka/srednja/nizka"}`;

async function run(id) {
  const out = `${DIR}/${id}.json`;
  if (fs.existsSync(out)) { console.log(`${id}: skip`); return; }
  const content = [{ type: 'text', text: PROMPT }];
  content.push({ type: 'image_url', image_url: { url: `data:image/jpeg;base64,${fs.readFileSync(`${DIR}/${id}.jpg`).toString('base64')}` } });
  for (let a = 1; a <= 4; a++) {
    try {
      const r = await zai.chat.completions.createVision({
        messages: [{ role: 'user', content }],
        temperature: 0.1, max_tokens: 500, thinking: { type: 'disabled' },
      });
      fs.writeFileSync(out, r.choices[0].message.content || '');
      console.log(`${id}: OK`);
      return;
    } catch (e) { console.log(`${id}: a${a} ${String(e).slice(0,70)}`); await new Promise(r2=>setTimeout(r2,2500)); }
  }
  console.log(`${id}: FAIL`);
}
for (const id of CELLS) await run(id);
