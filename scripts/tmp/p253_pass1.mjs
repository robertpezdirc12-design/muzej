import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';
const DIR = '/tmp/p253';
const zai = await ZAI.create();
const SCANS = [140,141,142,143,144,145,146,147];

const PROMPT = `Slika je sken strani PREDHODNIKA poročne knjige Trauungs-Buch 01738 (Podzemelj, 1828–1873), konec knjige = leto 1873. Knjiga 04455 se odpri NAKONEC leta 1873 pri vpisu m18 (11. junij 1873) — predhodnik 01738 naj bi vseboval vpise m1–m17 leta 1873 (1. januar – 11. junij 1873).
Prepiši STRUKTURO strani (Kurrent-pisava, nemško):
1) Leto v glavi strani (npr. '1873' — lahko tudi 1872 ali 'finis' ali naslovnica!)
2) 'Pag.' foliacijska številka čez vrh strani (če je vidna)
3) PRVA in ZADNJA vidna zaporedna številka vpisa (marginala levo)
4) Datum prvega in zadnjega vpisa na strani
5) Ali je strani KONEC knjige (finis-prazna / zadnji-vpisi / vezalo)?
Izhod SAMO JSON: {"leto":"...","pag":"...","prva_marg":"...","zadnja_marg":"...","prvi_datum":"...","zadnji_datum":"...","konec_knjige":"da/ne/vezalo/finis","razlaga":"..."}`;

async function run(s) {
  const out = `${DIR}/pass1_s${s}.json`;
  if (fs.existsSync(out)) { console.log(`s${s}: skip`); return; }
  const content = [{ type: 'text', text: PROMPT }];
  content.push({ type: 'image_url', image_url: { url: `data:image/jpeg;base64,${fs.readFileSync(`${DIR}/s${s}.jpg`).toString('base64')}` } });
  for (let a = 1; a <= 4; a++) {
    try {
      const r = await zai.chat.completions.createVision({
        messages: [{ role: 'user', content }],
        temperature: 0.1, max_tokens: 900, thinking: { type: 'disabled' },
      });
      fs.writeFileSync(out, r.choices[0].message.content || '');
      console.log(`s${s}: OK`);
      return;
    } catch (e) { console.log(`s${s}: a${a} ${String(e).slice(0,70)}`); await new Promise(r2=>setTimeout(r2,2500)); }
  }
  console.log(`s${s}: FAIL`);
}
for (const s of SCANS) await run(s);
