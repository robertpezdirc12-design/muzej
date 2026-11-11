import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';
const DIR = '/tmp/p253';
const zai = await ZAI.create();

const DETAIL = `Slika je stran poročne knjige Trauungs-Buch 01738 (Podzemelj, konec knjige = leto 1873, Kurrent-pisava). PREPIŠI VSE vrstice tabele znak-za-znakom (nemško, okrajšave razreši). Za vsak vpis podaj:
- marg: zaporedna številka (marginala levo)
- datum: datum poroke (iz stolpca 'Copulati' / datumskega stolpca)
- zenin: ime + priimek + status (ledig/witwer/...) + Wohnort (vas + hiša št.)
- nevesta: ime + priimek + status + Wohnort (vas + hiša št.)
- starosti (če vidni)
- starši (če vidni — oče/mati za ženina/nevesto)
- price (priče)
- duhovnik (podpis)
- dokumenti/opombe (Urkunden, naknadni vpisi)
Pazi na Kurrent oblike: 'b' vs '2', 'Jänner' vs 'Januar', hišne št. 1–80. Izhod SAMO JSON: {"vrstice":[{...}]}`;

async function run(id) {
  const out = `${DIR}/det_${id}.json`;
  if (fs.existsSync(out)) { console.log(`${id}: skip`); return; }
  const file = `${DIR}/${id}_page.jpg`;
  const content = [{ type: 'text', text: DETAIL }];
  content.push({ type: 'image_url', image_url: { url: `data:image/jpeg;base64,${fs.readFileSync(file).toString('base64')}` } });
  for (let a = 1; a <= 4; a++) {
    try {
      const r = await zai.chat.completions.createVision({
        messages: [{ role: 'user', content }],
        temperature: 0.1, max_tokens: 2200, thinking: { type: 'disabled' },
      });
      fs.writeFileSync(out, r.choices[0].message.content || '');
      console.log(`${id}: OK ${(r.choices[0].message.content||'').length}B`);
      return;
    } catch (e) { console.log(`${id}: a${a} ${String(e).slice(0,70)}`); await new Promise(r2=>setTimeout(r2,2500)); }
  }
  console.log(`${id}: FAIL`);
}
const order = ['s143_L','s143_R','s144_L','s144_R','s145_L','s145_R','s146_L','s146_R'];
for (const id of order) await run(id);
