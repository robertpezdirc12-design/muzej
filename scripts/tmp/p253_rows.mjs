import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';
const DIR = '/tmp/p253';
const zai = await ZAI.create();

const ROWPROMPT = (side) => `Slika je ${side} stran razprtega lista poročne knjige Trauungs-Buch 01738 (Podzemelj, konec knjige = leto 1873, Kurrent-pisava). Tabela: VRSTICE = vpisi (poroke) z marginalno številko na skrajnem levem robu.
Naloga: določi Y-MEJE vrstic v PIKSLIH (višina slike = 1500 px). Za vsako tablično vrstico (BREZ glave tabele, BREZ letne glave '1873') podaj približno y1 (zgornja meja) in y2 (spodnja meja) ter številko vpisa (marginala) in datum poroke, če je viden.
Izhod SAMO JSON: {"vrstice":[{"y1":0,"y2":0,"marg":"","datum":""}],"leto_glave":"","opomba":""}`;

async function run(id) {
  const out = `${DIR}/rows_${id}.json`;
  if (fs.existsSync(out)) { console.log(`${id}: skip`); return; }
  const file = `${DIR}/${id.replace('rows_','')}_page.jpg`;
  const content = [{ type: 'text', text: ROWPROMPT(id.includes('_R') ? 'DESNA' : 'LEVA') }];
  content.push({ type: 'image_url', image_url: { url: `data:image/jpeg;base64,${fs.readFileSync(file).toString('base64')}` } });
  for (let a = 1; a <= 4; a++) {
    try {
      const r = await zai.chat.completions.createVision({
        messages: [{ role: 'user', content }],
        temperature: 0.1, max_tokens: 1100, thinking: { type: 'disabled' },
      });
      fs.writeFileSync(out, r.choices[0].message.content || '');
      console.log(`${id}: OK`);
      return;
    } catch (e) { console.log(`${id}: a${a} ${String(e).slice(0,70)}`); await new Promise(r2=>setTimeout(r2,2500)); }
  }
  console.log(`${id}: FAIL`);
}
for (const id of ['s143_L','s143_R','s144_L','s144_R','s145_L','s145_R','s146_L','s146_R']) await run(id);
