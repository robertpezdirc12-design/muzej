import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';
const FILES = ['/tmp/p207/krop-grib/arb_s81_glava.png', '/tmp/p207/krop-grib/arb_s80_dno.png'];
const inst = await ZAI.create();
for (const f of FILES) {
  const out = f.replace('.png', '.json');
  if (fs.existsSync(out)) { console.log(f, 'ŽE'); continue; }
  const b64 = fs.readFileSync(f).toString('base64');
  const make = () => inst.chat.completions.createVision({
    messages: [{ role: 'user', content: [
      { type: 'text', text: `To je IZREZ iz MRLIŠKE matične knjige Podzemelj (meja-letnika-1869/1870!). Forenzična-naloga:
1) Prepiši VSE letnice-glave (velike-cifre npr. '1870'/'1849'/'1869'!) — KURRENT-zmeda-0/6/9-pogosta!
2) Prepiši ordinalne-številke-vrstic (levo)!
3) Prepiši mesečne-glave ('Jänner.', 'Februar'...) z-datumi!
4) Če-je vidna VALOVITA-ČRTA / prazni-prostor / 'finis' — to-POVEJ (konec-letnika!).
5) Prve-2-vrstice-čišče (vas+hišna+ime+datumi)!
Izhod: SAMO JSON: {"izrez": "...", "letnice": ["..."], "ordinali": ["..."], "meseci": ["..."], "valovita_crta": "opis-ali-null", "vrstice": [{"ordinala": "...", "vas": "...", "hisna": "...", "ime": "...", "mesec": "...", "smrt": "...", "pokop": "..."}], "opomba": "..."}` },
      { type: 'image_url', image_url: { url: `data:image/png;base64,${b64}` } }
    ]}],
    thinking: { type: 'disabled' }
  });
  for (let a = 1; a <= 4; a++) {
    try {
      const c = await Promise.race([make(), new Promise((_, r) => setTimeout(() => r(new Error('t')), 180000))]);
      const t = (c?.choices?.[0]?.message?.content || '').trim().replace(/^```(json)?/i, '').replace(/```$/, '');
      const res = JSON.parse(t.slice(t.indexOf('{'), t.lastIndexOf('}') + 1));
      fs.writeFileSync(out, JSON.stringify(res, null, 2));
      console.log(f.split('/').pop(), 'OK letnice=', JSON.stringify(res.letnice), 'valovita=', res.valovita_crta ? 'DA' : '-');
      break;
    } catch (e) { console.error(`poskus ${a} FAIL`); await new Promise(r => setTimeout(r, 2500 * a)); }
  }
}
