import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';
const f = process.argv[2];
const b64 = fs.readFileSync(f).toString('base64');
const inst = await ZAI.create();
const make = () => inst.chat.completions.createVision({
  messages: [{ role: 'user', content: [
    { type: 'text', text: `To je VERTIKALNI IZREZ levega ozkega STOLPCA ročnih ZAPOREDNIH ŠTEVILK iz MRLIŠKE matične knjige (leto 1871). Stolpec vsebuje Približno 12–14 ročno zapisanih številk, ena-na-vrstico, od-zgoraj-navzdol.

NALOGA — prepiši VSILE ŠTEVILKE po vrsti od-zgoraj-navzdol. TOČNO!

KURRENT-ŠTEVKE: 0=velik-oval, 1=ozka-črtica, 2=z-spodnjim-lakom, 3=dve-zanki-desno, 4=zanka-levo-zgoraj, 5=spodnja-zanka-+zgornja-črtica, 6=spodnja-zanka, 7=γ-forma-s-prečko, 8=dve-zanki-nad-seboj, 9=zgornja-zanka-z-dolgo-črto.
Pozor: 0-vs-9 zmeda na koncu številke (30-vs-39?); 0-vs-6 (20-vs-26?); 1-vs-7.
Številke-niso-nujno-lepo-v-ravi — nekatere-malce-desno/levo.

Izhod: SAMO JSON:
{"krop": "ord", "stevilke": ["19", "20", ...], "koliko": 12, "prva": "...", "zadnja": "...", "preskok_ali_dup": "opis-ali-null", "opomba": "..."}` },
    { type: 'image_url', image_url: { url: `data:image/png;base64,${b64}` } }
  ]}],
  thinking: { type: 'disabled' }
});
for (let a = 1; a <= 4; a++) {
  try {
    const c = await Promise.race([make(), new Promise((_, r) => setTimeout(() => r(new Error('t')), 180000))]);
    const t = (c?.choices?.[0]?.message?.content || '').trim().replace(/^```(json)?/i, '').replace(/```$/, '');
    const res = JSON.parse(t.slice(t.indexOf('{'), t.lastIndexOf('}') + 1));
    fs.writeFileSync(process.argv[2].replace('.png','.json'), JSON.stringify(res, null, 2));
    console.log('OK koliko=', res.koliko, 'prva=', res.prva, 'zadnja=', res.zadnja, '|', JSON.stringify(res.stevilke));
    process.exit(0);
  } catch (e) { console.error(`poskus ${a} FAIL ${e.message}`); await new Promise(r => setTimeout(r, 2500 * a)); }
}
process.exit(1);
