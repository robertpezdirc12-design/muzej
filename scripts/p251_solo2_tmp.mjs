import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';
const DIR = '/home/z/p251tmp';
const OUT = `${DIR}/solo2`;
fs.mkdirSync(OUT, { recursive: true });
const zai = await ZAI.create();
const P = {
  'm19-priest-6x': `6×-zoom podpisa duhovnika (vrsta m19, 1873). Prepiši znak za znak: 'Daniel X'. Kandidati: 'Daniel Fercher' (Kurrent F, 'ercher') ALI 'Daniel Teršaj' (Kurrent T, 'eršaj'). Pazi: Kurrent F in T imata podobno vodoravno črto; 'k/š' podobna zanka. Očitna šuma: črnobarvni naknadni zapisi. KONČNO ODLUČI eno ime + zaupanje visoko/srednje/nizko. Izhod SAMO JSON: {"ime":"...","nacin":"...","zaupanje":"...","razlaga":"..."}`,
  'm18-bhouse-6x': `6×-zoom: Wohnort-neveste iz vrste m18 (1873). Prepiši: vas + hišna številka. Kandidati: 'Griblje 62' / 'Griblje 63' / 'Griblje 6b' / 'Griblje 68'. Pazi Kurrent '3' (dvojna zanka desno) vs '2' (ena zanka). Izhod SAMO JSON: {"wohnort":"...","stevilka":"...","zaupanje":"...","razlaga":"..."}`,
  'm20-ghouse-6x': `6×-zoom: Wohnort-ženina iz vrste m20 (1873). Prepiši: vas + hišna številka. Kandidati: 'Griblje 22' / 'Griblje 26' / 'Griblje 2b' — pazi, ali drugi znak ima ODPRTO zgornjo zanko ('2') ali DVIHAJOČO PALČKO ('b')! Izhod SAMO JSON: {"wohnort":"...","stevilka":"...","zaupanje":"...","razlaga":"..."}`,
  'm21-bname-5x': `5×-zoom: ime+priimek neveste iz vrste m21 (1873, hiša 10). Prepiši znak za znak. Kandidati: 'Maria Jabovšič' / 'Maria Gabovšič' / 'Maria Jakofaič' / 'Maria Gahofaič'. Priimek ženina iste vrste je podoben (istoimenski par!). Izhod SAMO JSON: {"ime":"...","priimek":"...","zaupanje":"...","razlaga":"..."}`,
  'm19-bride-4x': `4×-zoom: nevesta vrste m19 (1873, Gradac 1, starost 19). Prepiši ime+priimek (več vrst: kandidati 'Maria Eva Anguška Stomašek' / 'Maria Ana Augustina Homolitsch' / kombinacija 'Maria Eva Anguška-Stomašek'). Kateri je PRVI priimek in kateri DRUGI? Izhod SAMO JSON: {"ime":"...","priimek":"...","drugiPriimek":"...","zaupanje":"...","razlaga":"..."}`,
};
async function run(id, files) {
  const out = `${OUT}/${id}.json`;
  if (fs.existsSync(out)) { console.log(`${id}: skip`); return; }
  const content = [{ type: 'text', text: P[id] }];
  for (const f of files) content.push({ type: 'image_url', image_url: { url: `data:image/jpeg;base64,${fs.readFileSync(f).toString('base64')}` } });
  for (let a = 1; a <= 4; a++) {
    try {
      const r = await zai.chat.completions.createVision({
        messages: [{ role: 'user', content }],
        temperature: 0.1, max_tokens: 900, thinking: { type: 'disabled' },
      });
      fs.writeFileSync(out, r.choices[0].message.content || '');
      console.log(`${id}: OK`); return;
    } catch (e) { console.log(`${id}: a${a} ${String(e).slice(0,60)}`); await new Promise(s=>setTimeout(s,2500)); }
  }
  console.log(`${id}: FAIL`);
}
await run('m19-priest-6x', [`${DIR}/krops/m19_priest_6x.jpg`]);
await run('m18-bhouse-6x', [`${DIR}/krops/m18_bhouse_6x.jpg`]);
await run('m20-ghouse-6x', [`${DIR}/krops/m20_ghouse_6x.jpg`]);
await run('m21-bname-5x', [`${DIR}/krops/m21_bname_5x.jpg`]);
await run('m19-bride-4x', [`${DIR}/krops/m19_bride_4x.jpg`]);
