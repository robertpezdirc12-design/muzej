import ZAI from 'z-ai-web-dev-sdk';
import { execSync } from 'child_process';
import fs from 'fs';

const SHEETS = { a01: [2826, 2273], a02: [3010, 2158], a03: [2645, 2154], a04: [2645, 2158], a05: [2634, 2165] };

async function readCorner(zai, sh, corner) {
  const [W, H] = SHEETS[sh];
  const box = corner === 'TL' ? [0, 0, Math.round(W*0.28), Math.round(H*0.14)]
    : corner === 'TR' ? [Math.round(W*0.72), 0, W, Math.round(H*0.14)]
    : corner === 'BL' ? [0, Math.round(H*0.86), Math.round(W*0.28), H]
    : [Math.round(W*0.72), Math.round(H*0.86), W, H];
  execSync(`python3 -c "
from PIL import Image
im = Image.open('public/atlas/n83-${sh}.jpg')
t = im.crop((${box.join(',')}))
t = t.resize((int(t.width*2.2), int(t.height*2.2)), Image.LANCZOS)
t.save('/tmp/p10-corner.jpg', quality=95)
"`);
  const b64 = fs.readFileSync('/tmp/p10-corner.jpg').toString('base64');
  const r = await zai.chat.completions.createVision({
    messages: [{ role: 'user', content: [
      { type: 'text', text: `To je KOT katastrskega lista franciscejskega katastra. V kotu so arhivske oznake: številka lista (rimke I–V), oznaka sekcije (npr. "O.IX24cf", "SI AS 176", "S II AS 176") in morda številke.

PREBERI NATANČNO VSE znake/oznake, ki jih vidiš v tem kotu — znak po znak. Posebej izpiši:
1. Zaporedno številko lista (rimska).
2. Sekcijsko oznako (črke in številke, npr. IX24 + dve črki).
3. Vse ostalo (AS 176, letnice...).
Format: JSON {"list": "...", "sek": "...", "ostalo": "..."}` },
      { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${b64}` } }
    ]}],
    thinking: { type: 'disabled' }
  });
  return (r.choices?.[0]?.message?.content ?? '').trim();
}

async function main() {
  const zai = await ZAI.create();
  const out = {};
  for (const sh of ['a01', 'a04']) {
    for (const c of ['TL', 'TR']) {
      try {
        const r = await readCorner(zai, sh, c);
        out[`${sh}-${c}`] = r;
        console.log(`\n=== ${sh.toUpperCase()} ${c} ===\n${r.slice(0, 400)}`);
      } catch (e) {
        console.log(`${sh}-${c} FAIL: ${String(e.message ?? e).slice(0, 60)}`);
        await new Promise(r2 => setTimeout(r2, 12000));
      }
    }
  }
  fs.writeFileSync('/tmp/p10-corners.json', JSON.stringify(out));
}
main();
