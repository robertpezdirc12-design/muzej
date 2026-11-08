// P10: ciljani VLM sken A03 (vzhodni pas) + A05 (sklop stavb) — hišne št., cerkev, reka, meje
import ZAI from 'z-ai-web-dev-sdk';
import { execSync } from 'child_process';
import fs from 'fs';

const SHEETS = {
  a03: { file: 'public/atlas/n83-a03.jpg', w: 2645, h: 2154 },
  a05: { file: 'public/atlas/n83-a05.jpg', w: 2634, h: 2165 },
};

const QUERIES = {
  'a03-e1': { s: 'a03', x0: 0.76, y0: 0.00, x1: 1.00, y1: 0.36 },
  'a03-e2': { s: 'a03', x0: 0.76, y0: 0.32, x1: 1.00, y1: 0.70 },
  'a03-e3': { s: 'a03', x0: 0.76, y0: 0.64, x1: 1.00, y1: 1.00 },
  'a05-c1': { s: 'a05', x0: 0.58, y0: 0.13, x1: 0.78, y1: 0.34 },
  'a05-c2': { s: 'a05', x0: 0.72, y0: 0.13, x1: 0.94, y1: 0.34 },
  'a05-c3': { s: 'a05', x0: 0.58, y0: 0.28, x1: 0.78, y1: 0.50 },
  'a05-c4': { s: 'a05', x0: 0.72, y0: 0.28, x1: 0.94, y1: 0.50 },
};

async function scan(zai, id, q) {
  const sh = SHEETS[q.s];
  const x0 = Math.round(sh.w * q.x0), y0 = Math.round(sh.h * q.y0);
  const x1 = Math.round(sh.w * q.x1), y1 = Math.round(sh.h * q.y1);
  execSync(`python3 -c "
from PIL import Image
im = Image.open('${sh.file}')
tile = im.crop((${x0}, ${y0}, ${x1}, ${y1}))
tile = tile.resize((int(tile.width*1.7), int(tile.height*1.7)), Image.LANCZOS)
tile.save('/tmp/p10-${id}.jpg', quality=94)
"`);
  const b64 = fs.readFileSync(`/tmp/p10-${id}.jpg`).toString('base64');
  const prompt = `To je izrezek katastrskega lista ${q.s.toUpperCase()} (franciscejski kataster 1825, k.o. Griblje / okolica, Bela krajina), nemška Kurrent pisava.

NATANČNO odgovori na vprašanja:
1. REKA: Ali je na izrezku vidna reka (vijugasta svetla/temna črta s pasom)? Kje točno (levo/desno/zgoraj/spodaj, % pozicija)?
2. MEJNA ČRTA: Ali vidiš debelo mejno črto (katastralsko občino)? Poteka kje?
3. CERKEV: Ali vidiš cerkev (simbol z križem, apsido) ali pokopališče (obrobl zapos)? Kje (% pozicija)?
4. STAVBE + HIŠNE ŠTEVILKE: Preštej stavbne simbole (temni pravokotniki). Če so ob stavbah številke (npr. N°12), preberi VSE — pari (približna xPct%, yPct% pozicija v IZREZKU, številka).
5. NAPISI: preberi vse besedilne napise s pozicijo (%).

Izhod: SAMO JSON: {"reka": ..., "meja": ..., "cerkev": ..., "stDB": ..., "hisaSt": [{"xPct":.., "yPct":.., "st":".."}], "napisi": [{"text":"..", "xPct":.., "yPct":..}]}`;
  for (let a = 1; a <= 4; a++) {
    try {
      const r = await zai.chat.completions.createVision({
        messages: [{ role: 'user', content: [
          { type: 'text', text: prompt },
          { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${b64}` } }
        ]}],
        thinking: { type: 'disabled' }
      });
      return r.choices?.[0]?.message?.content ?? '';
    } catch (e) {
      console.error(`  ${id} poskus ${a}: ${String(e.message ?? e).slice(0, 60)}`);
      await new Promise(r2 => setTimeout(r2, 15000));
    }
  }
  return null;
}

function parseJSON(text) {
  if (!text) return null;
  let t = text.trim();
  const i = t.indexOf('{'), j = t.lastIndexOf('}');
  if (i >= 0 && j > i) t = t.slice(i, j + 1);
  try { return JSON.parse(t); } catch { return null; }
}

async function main() {
  const zai = await ZAI.create();
  const out = {};
  for (const [id, q] of Object.entries(QUERIES)) {
    const t0 = Date.now();
    const raw = await scan(zai, id, q);
    out[id] = parseJSON(raw) ?? raw;
    console.log(`${id}: ${Date.now() - t0}ms — ${raw ? String(raw).slice(0, 60).replace(/\n/g, ' ') : 'FAIL'}`);
    fs.writeFileSync('/home/z/my-project/research/georef-n83/tiles-vlm/p10-targeted.json', JSON.stringify(out, null, 1));
  }
  console.log('KONEC.');
}
main();
