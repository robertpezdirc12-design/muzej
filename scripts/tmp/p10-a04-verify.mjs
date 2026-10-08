import ZAI from 'z-ai-web-dev-sdk';
import { execSync } from 'child_process';
import fs from 'fs';

async function look(zai, crop, prompt, out) {
  execSync(`python3 -c "
from PIL import Image
im = Image.open('public/atlas/n83-a04.jpg')
t = im.crop((${crop.join(',')}))
t = t.resize((int(t.width*2.5), int(t.height*2.5)), Image.LANCZOS)
t.save('/tmp/p10-v.jpg', quality=95)
"`);
  const b64 = fs.readFileSync('/tmp/p10-v.jpg').toString('base64');
  const r = await zai.chat.completions.createVision({
    messages: [{ role: 'user', content: [
      { type: 'text', text: prompt },
      { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${b64}` } }
    ]}],
    thinking: { type: 'disabled' }
  });
  const c = (r.choices?.[0]?.message?.content ?? '').trim();
  console.log(`\n=== ${out} ===\n${c.slice(0, 500)}`);
  return c;
}

async function main() {
  const zai = await ZAI.create();
  // A04 zgornji desni kot (2.5x povečano) — ponovna preveritev kode
  await look(zai, [2645-800, 0, 2645, 320],
    `Preberi NATANČNO arhivsko oznako v tem kotu katastrskega lista. Oznaka ima obliko "O.IX24" + DVE ČRKI (npr. cg, bh, ch, dg). Kateri DVE ČRKI sta zapisani za "24"? Preberi znak-po-znak tudi vse ostale znake v kotu (rimsko številko, AS 176...). Odgovori v formatu: SEKCIJA=XX, OSTALO=...`,
    'A04-desni-zgornji-kot (2.5x)');
}
main();
