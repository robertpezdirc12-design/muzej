// P203 — KROP-branje izrezov (crop-reader; recept P200/P201/P202).
// Uporaba: bun p203_read_crop.mjs <ime-cropa> <vprašanje>
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';

const ime = process.argv[2];
const q = process.argv[3] || 'Natančno preberi vsebino tega izreza stare Kurrent-pisave (mrtvaški register). Negotovo z [?].';
const b64 = fs.readFileSync(`/tmp/p203/crops/${ime}.png`).toString('base64');
const inst = await ZAI.create();
const r = await inst.chat.completions.createVision({
  messages: [{ role: 'user', content: [
    { type: 'text', text: `${q}\nOdgovori SLOVENSKO, natanko in poleg tega zapiši glif za glifom, če je ključno.` },
    { type: 'image_url', image_url: { url: `data:image/png;base64,${b64}` } }
  ]}],
  thinking: { type: 'disabled' }
});
console.log(r?.choices?.[0]?.message?.content);
