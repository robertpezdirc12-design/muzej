import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';
const DIR = '/tmp/p255';
const zai = await ZAI.create();
const SCANS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];

const PROMPT = `Slika je sken strani PREDHODNIKA poročne knjige Trauungs-Buch 01738 (Podzemelj, 1828–1873), ZAČETEK knjige. Knjiga 04455 se odpre šele konec leta 1873 (vpis m18, 11. junij 1873) — 01738 mora vsebovati vpise od 1828 naprej. Pričakujemo: naslovnica / glava-registre / prvi vpisi leta 1828.
Prepiši STRUKTURO strani (Kurrent-pisava, nemško):
1) Kaj je stran: naslovnica / glava ('Trauungs-Buch' ali podobno) / navadna stran z vpisi / prazna / vezalo?
2) Letnica v glavi strani (npr. '1828' — če je vidna)
3) 'Pag.' foliacijska številka čez vrh strani (če je vidna)
4) PRVA in ZADNJA vidna zaporedna številka vpisa (marginala levo)
5) Datum prvega in zadnjega vpisa na strani (če so vpisi)
6) IMENA v prvem in zadnjem vpisu (ženin × nevesta) — poskusi prebrati
Izhod SAMO JSON: {"tip":"naslovnica/glava/vpisi/prazna/vezalo","leto":"...","pag":"...","prva_marg":"...","zadnja_marg":"...","prvi_datum":"...","zadnji_datum":"...","prvi_par":"","zadnji_par":"","razlaga":"..."}`;

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
