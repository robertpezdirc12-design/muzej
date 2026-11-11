import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';
import * as Z from './p257_w2_jobs.mjs';
const zai = await ZAI.create();

// Z.ROWS = [{id, scan, y0, y1, x0, x1, zoom, q}]
const PROMPT = (j) => `Slika je MOČNO POVEČAN IZREZ celice/segmenta iz poročne knjige Trauungs-Buch 01738 (Podzemelj, 1830/1831, Kurrent-pisava, nemško). Izrez je iz vrstice: ${j.q}
Preberi IZKLJUČNO to, kar je vprašano — dobesedno, črkovno. Kurrent črke: p/b, o/a, e/n, s/f, u/v, i/j so pogosto podobne — RAZLOČUJ previdno. Če je branje negotovo, podaj ALTERNATIVE z [~].
Izhod SAMO JSON: {"id":"${j.id}","branje":"...","alternative":"...","sigurnost":"visoka/srednja/nizka","razlaga":"..."}`;

async function run(j) {
  const out = `/tmp/p257/w2/${j.id}.json`;
  if (fs.existsSync(out) && fs.statSync(out).size > 30) { console.log(`${j.id}: skip`); return; }
  
  // uporabi PIL-ju podobno: preberi iz originala, povečaj, pošlji
  
  const { execSync } = await import('child_process');
  const tmpf = `/tmp/p257/w2/_${j.id}.jpg`;
  const cmd = `python3 -c "
from PIL import Image
im = Image.open('/tmp/p257/s${j.scan}.jpg')
c = im.crop((${j.x0}, ${j.y0}, ${j.x1}, ${j.y1}))
c = c.resize((int(c.width*${j.zoom}), int(c.height*${j.zoom})), Image.LANCZOS)
c.save('${tmpf}', quality=95)
print(c.size)
"`;
  execSync(cmd);
  const content = [{ type: 'text', text: PROMPT(j) }];
  content.push({ type: 'image_url', image_url: { url: `data:image/jpeg;base64,${fs.readFileSync(tmpf).toString('base64')}` } });
  for (let a = 1; a <= 4; a++) {
    try {
      const r = await zai.chat.completions.createVision({
        messages: [{ role: 'user', content }],
        temperature: 0.1, max_tokens: 700, thinking: { type: 'disabled' },
      });
      fs.writeFileSync(out, r.choices[0].message.content || '');
      console.log(`${j.id}: OK`);
      return;
    } catch (e) { console.log(`${j.id}: a${a} ${String(e).slice(0,70)}`); await new Promise(r2=>setTimeout(r2,2500)); }
  }
  console.log(`${j.id}: FAIL`);
}
fs.mkdirSync('/tmp/p257/duels', { recursive: true });
for (const j of Z.ROWS) { await run(j); await new Promise(r=>setTimeout(r,900)); }
