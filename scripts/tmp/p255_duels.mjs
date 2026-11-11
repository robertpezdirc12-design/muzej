import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';
const DIR = '/tmp/p255';
const zai = await ZAI.create();

const PROMPT = `Slika je POVEČAN IZREZ poročne knjige Trauungs-Buch 01738 (Podzemelj, leto 1828, Kurrent-pisava). Prepiši SAMO vidne rokopisne besede/številke znak-za-znakom (izjeme: 'Jänner', 'Hornung'=Februar). Kurent: '3'=flat-top-zanka, '2'=zankasta-glava-dolgo-rep, '1'=enostaven-črt, '8'=dvojna-zanka, '6'=zaprt-zgornji-krož, 'h'≈dolg- straight.
Izhod SAMO JSON: {"prepis":"","razlaga":"","zanesljivost":"visoka/srednja/nizka"}`;

async function run(id) {
  const out = `${DIR}/duel_${id}.json`;
  if (fs.existsSync(out)) { console.log(`${id}: skip`); return; }
  const content = [{ type: 'text', text: PROMPT }];
  content.push({ type: 'image_url', image_url: { url: `data:image/jpeg;base64,${fs.readFileSync(`${DIR}/${id}.jpg`).toString('base64')}` } });
  for (let a = 1; a <= 4; a++) {
    try {
      const r = await zai.chat.completions.createVision({
        messages: [{ role: 'user', content }],
        temperature: 0.1, max_tokens: 700, thinking: { type: 'disabled' },
      });
      fs.writeFileSync(out, r.choices[0].message.content || '');
      console.log(`${id}: OK`);
      return;
    } catch (e) { console.log(`${id}: a${a} ${String(e).slice(0,70)}`); await new Promise(r2=>setTimeout(r2,2500)); }
  }
  console.log(`${id}: FAIL`);
}
const ids = ['z_m1_datum','z_m1_vas','z_m2_datum','z_m3_vas','z_m4_vas','z_m5_vas','z_m6_imena','z_m6_hisa','z_m7_vas','z_m8_vas','z_m9_vas','z_m10_vas','z_m11_datum','z_m11_vas','z_m12_datum','z_m12_vas','z_m13_datum','z_m13_imena','z_m13_hise','z_m14_vas','z_m15_vas','z_must_row','z_sept_nov_marg'];
for (const id of ids) await run(id);
