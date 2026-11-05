import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';
const b64 = fs.readFileSync('/tmp/p210/krop-grib/arb_s61_glava.png').toString('base64');
const inst = await ZAI.create();
const make = () => inst.chat.completions.createVision({
  messages: [{ role: 'user', content: [
    { type: 'text', text: `To je IZREZ GLAVE-strani iz MRLIŠKE matične knjige Podzemelj (meja-letnika 1866/1867!). Forenzika:
1) VELIKA-LETVICA-glava ('1867'?/'1866'?/'1864'? — KURRENT-zmeda-6/4/7/9!) — prepiši-TOČNO!
2) Mesečna-glava ('Jänner.'?)
3) Ordinalne-številke-vrstic (levo — restart-na-1?)
4) Prvi-2-vrstici (ordinala+vas+hišna+ime+datumi)!
Izhod: SAMO JSON: {"letnice": ["..."], "meseci": ["..."], "ordinali": ["..."], "vrstice": [{"ordinala": "...", "vas": "...", "hisna": "...", "ime": "...", "mesec": "...", "smrt": "...", "pokop": "..."}], "opomba": "..."}` },
    { type: 'image_url', image_url: { url: `data:image/png;base64,${b64}` } }
  ]}],
  thinking: { type: 'disabled' }
});
for (let a = 1; a <= 4; a++) {
  try {
    const c = await Promise.race([make(), new Promise((_, r) => setTimeout(() => r(new Error('t')), 180000))]);
    const t = (c?.choices?.[0]?.message?.content || '').trim().replace(/^```(json)?/i, '').replace(/```$/, '');
    const res = JSON.parse(t.slice(t.indexOf('{'), t.lastIndexOf('}') + 1));
    fs.writeFileSync('/tmp/p210/krop-grib/arb_s61_glava.json', JSON.stringify(res, null, 2));
    console.log('OK letnice:', JSON.stringify(res.letnice));
    process.exit(0);
  } catch (e) { console.error(`poskus ${a} FAIL`); await new Promise(r => setTimeout(r, 2500 * a)); }
}
process.exit(1);
