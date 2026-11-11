import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';
const DIR = '/tmp/p256';
const zai = await ZAI.create();
const SCANS = [4, 5, 6, 7];

const PROMPT = `Slika je sken strani PREDHODNIKA poročne knjige Trauungs-Buch 01738 (Podzemelj, 1828–1873). P255 je prebral leto 1828 (s1–s3, m1–m13); P253 konec 1873. Ta stran je notranjost: pričakujemo leto 1829 (s4–s5) in prehod v 1830 (s6: '1830 12 Jenner' restart viden že v pass-1 P255!).
Prepiši STRUKTURO strani (Kurrent-pisava, nemško):
1) Kaj je stran: naslovnica / glava ('Trauungs-Buch') / navadna stran z vpisi / prazna / vezalo?
2) Letnica v glavi strani ALI prvi vpis (npr. '1829' / '1830' — če je vidna)
3) 'Pag.' foliacijska številka čez vrh strani (če je vidna)
4) ŠTEVILO vrstic z vpisi (ne štej praznih)
5) Datum PRVEGA vpisa (natančno: mesec + dan) in datum ZADNJEGA vpisa
6) Če je v datumskem stolpcu RESTART letnice (npr. '1830' sredi strani) — to posebej označi!
7) IMENA v prvem in zadnjem vpisu (ženin × nevesta) — poskusi prebrati
8) Podpis duhovnika (desno spodaj / stolpec Unterschrift)
Izhod SAMO JSON: {"tip":"naslovnica/glava/vpisi/prazna/vezalo","leto":"...","pag":"...","vrstic":N,"prvi_datum":"...","zadnji_datum":"...","restart_letnica":".../null","prvi_par":"","zadnji_par":"","duhovnik":"","razlaga":"..."}`;

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
