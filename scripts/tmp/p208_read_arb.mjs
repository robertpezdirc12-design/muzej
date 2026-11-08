import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';
const inst = await ZAI.create();
for (const f of ['/tmp/p208/krop-grib/arb_s75_meja.png', '/tmp/p208/krop-grib/arb_z13_s76r6.png']) {
  const out = f.replace('.png', '.json');
  if (fs.existsSync(out)) { console.log(f, 'ŽE'); continue; }
  const b64 = fs.readFileSync(f).toString('base64');
  const make = () => inst.chat.completions.createVision({
    messages: [{ role: 'user', content: [
      { type: 'text', text: f.includes('s75_meja') ?
`To je IZREZ MEJE IZ MRLIŠKE matične knjige Podzemelj (konec-1868/začetek-1869!). Forenzika:
1) VELIKA-LETVICA-glava ('1869'/'1868'? — KURRENT-zmeda!) — prepiši-TOČNO!
2) Mesečna-glava ('Jänner.'?)
3) VSOTNA-VRSTA ('vsota'/'Summa' — dve-številki-'1|8'-forma?) — prepiši-številki!
4) Tail-vrstice (77–80?) — ordinala+vas+hišna+ime+datumi-za-VSAKO!
5) Prve-vrstice-restarta (1–2?) — ordinala+vas+hišna+ime+datumi!
Izhod: SAMO JSON: {"letnice": ["..."], "meseci": ["..."], "vsota": "...", "tail": [{"ordinala": "...", "vas": "...", "hisna": "...", "ime": "...", "starost": "..."}], "restart": [{"ordinala": "...", "vas": "...", "hisna": "...", "ime": "...", "mesec": "...", "smrt": "...", "pokop": "..."}], "opomba": "..."}` :
`To je IZREZ IZ MRLIŠKE matične knjige Podzemelj (leto 1869, Februar-zona!). Centralna-vrsta-ima vas 'Griblje'-ali-podobno — prepiši-ČISTO:
1) ordinala (levo!)
2) mesec+smrt/pokop
3) VAS — TOČNO ('Griblje'/'Grible'?)
4) HIŠNA-ŠTEVILKA — TOČNO (KURRENT-3/5/8-zmeda!-2-cifre-mogoče!)
5) ime+starost+bolezen
Izhod: SAMO JSON: {"ordinala": "...", "vas": "...", "hisna": "... [~ ...?]", "ime": "...", "starost": "...", "mesec": "...", "smrt": "...", "pokop": "...", "bolezen": "...", "opomba": "..."}` },
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
      console.log(f.split('/').pop(), 'OK');
      break;
    } catch (e) { console.error(`poskus ${a} FAIL`); await new Promise(r => setTimeout(r, 2500 * a)); }
  }
}
