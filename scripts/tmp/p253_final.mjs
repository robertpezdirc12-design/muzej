import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';
const DIR = '/tmp/p253';
const zai = await ZAI.create();
const BASE = `Poročna knjiga 01738 (Podzemelj, 1873, Kurrent). Prepiši znak-za-znakom. 'b'≠'2', 'Feber'='Februar', '873'='1873'. Pri vsaki osebi: VAS+HIŠA pride PRED imenom. Izhod SAMO JSON.`;
const QS = {
  'm4_full': `${BASE} CELA vrstica m4 (poroka ~9.2.1873). Ženin: Nikolaus [Jaklič/Jahlič/Gabrijel?] — njegova VAS+HIŠA? (kand. 'Zemlje/Knežja vas/Griblje' h18/h28/1?). Nevesta: Maria [Tomc/Tomić?] — njena VAS+HIŠA? Starosti?
JSON: {"zenin":{"ime":"","vas":"","hisa":"","starost":""},"nevesta":{"ime":"","vas":"","hisa":"","starost":""}}`,
  'm6_full': `${BASE} CELA vrstica m6 (poroka ~12.2.1873). Ženin: Georg [Kolbezen?] — VAS+HIŠA? (kand. Griblje, ¼-blok?). Nevesta: Maria [Muc/Mutz?] — VAS+HIŠA? (kand. Griblje h10?). Starosti?
JSON: {"zenin":{"ime":"","vas":"","hisa":"","starost":""},"nevesta":{"ime":"","vas":"","hisa":"","starost":""}}`,
  'm8_full': `${BASE} CELA vrstica m8 (poroka ~19.2.1873). Ženin: Matthias [Silak/Lilak?], 32 — VAS+HIŠA? (kand. 'Primož 3'?). Nevesta: Barbara Tome, 19 — VAS+HIŠA? (kand. 'Vinica/Podzemelj 19'?).
JSON: {"zenin":{"ime":"","vas":"","hisa":"","starost":""},"nevesta":{"ime":"","vas":"","hisa":"","starost":""}}`,
  'm9_full': `${BASE} CELA vrstica m9 (poroka ~19.2.1873). Ženin: Miho [Silak/Lilah?], 26 — VAS+HIŠA? Nevesta: Maria Bahorić, 18, diene — VAS+HIŠA?
JSON: {"zenin":{"ime":"","vas":"","hisa":"","starost":""},"nevesta":{"ime":"","vas":"","hisa":"","starost":""}}`,
  'm12_full2': `${BASE} CELA vrstica m12 (poroka ~19.2.1873). Ženin: [Miho Kupamič?], 31 — VAS+HIŠA? (kand. 'Griblje h73'?). Nevesta: Maria [Krambič?] — VAS+HIŠA? (kand. 'Griblje h73/h13'?). Prepiši tudi morebitni prečrtani/popravljeni zapis.
JSON: {"zenin":{"ime":"","vas":"","hisa":"","starost":""},"nevesta":{"ime":"","vas":"","hisa":"","starost":""},"opomba":""}`,
  'm17_zenin2': `${BASE} IZREZ hiše+Wohnort ženina vrstice m17 (zadnji vpis 25.5.1873): Anton [Henke?], 33. VAS (kand. 'Gradac'/'Griblje'?) + HIŠA (kand. 35 ali 15?).
JSON: {"vas":"","hisa":""}`,
  'm17_nevesta': `${BASE} IZREZ neveste vrstice m17 (25.5.1873): ime (Josefa?), priimek?, VAS + HIŠA, starost?
JSON: {"ime":"","priimek":"","vas":"","hisa":"","starost":""}`,
};
async function ask(tag) {
  const out = `${DIR}/z3_${tag}.json`;
  if (fs.existsSync(out)) { console.log(`${tag}: skip`); return; }
  const content = [{ type: 'text', text: QS[tag] }];
  content.push({ type: 'image_url', image_url: { url: `data:image/jpeg;base64,${fs.readFileSync(`${DIR}/z3/${tag}.jpg`).toString('base64')}` } });
  for (let a = 1; a <= 5; a++) {
    try {
      const r = await zai.chat.completions.createVision({
        messages: [{ role: 'user', content }],
        temperature: 0.1, max_tokens: 700, thinking: { type: 'disabled' },
      });
      fs.writeFileSync(out, r.choices[0].message.content || '');
      console.log(`${tag}: OK`);
      await new Promise(r2=>setTimeout(r2,8000));
      return;
    } catch (e) { console.log(`${tag}: a${a} ${String(e).slice(0,50)}`); await new Promise(r2=>setTimeout(r2,11000)); }
  }
  console.log(`${tag}: FAIL`);
}
for (const tag of Object.keys(QS)) await ask(tag);
