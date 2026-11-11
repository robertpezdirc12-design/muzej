import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';
const DIR = '/tmp/p253';
const zai = await ZAI.create();

const PROMPT = `Dve sliki sta IZREZA iste VRSTICE poročne knjige Trauungs-Buch 01738 (Podzemelj, 1873, Kurrent): 1. slika = LEVA stran (marginala+številka, datum Copulati, ženin Bräutigam z imenom/statusom/starostjo/Wohnort-vas+hiša, nevesta Braut isto), 2. slika = DESNA stran (starši oče/mati za ženina in nevesto, priče, Urkunden/dokumenti, podpis duhovnika).
PREPIŠI znak-za-znakom vse vidno polje. Pazi Kurrent: 'b'≠'2', 'Jänner'='Januar', 'Mai'≠'März', 'ledig'='samsen', hišne št. 1–80, vasi: Griblje/Podzemelj/Vinica/Gradac/Dolence/Primošek/Zemlje/Mokronog/Dobravice/Cerklje... Duhovnik: župnik 'Franz Dovgan' (zapisan tudi kot Dergan/Dorgan).
Izhod SAMO JSON: {"marg":"","datum":"","zenin":{"ime":"","status":"","starost":"","vas":"","hisa":""},"nevesta":{"ime":"","status":"","starost":"","vas":"","hisa":""},"starsi_zenin":{"oce":"","mati":""},"starsi_nevesta":{"oce":"","mati":""},"price":"","urkunde":"","duhovnik":"","opombe":""}`;

async function run(marg, files) {
  const out = `${DIR}/dual_m${marg}.json`;
  if (fs.existsSync(out)) { console.log(`m${marg}: skip`); return; }
  const content = [{ type: 'text', text: PROMPT }];
  for (const f of files) content.push({ type: 'image_url', image_url: { url: `data:image/jpeg;base64,${fs.readFileSync(f).toString('base64')}` } });
  for (let a = 1; a <= 4; a++) {
    try {
      const r = await zai.chat.completions.createVision({
        messages: [{ role: 'user', content }],
        temperature: 0.1, max_tokens: 1400, thinking: { type: 'disabled' },
      });
      fs.writeFileSync(out, r.choices[0].message.content || '');
      console.log(`m${marg}: OK`);
      return;
    } catch (e) { console.log(`m${marg}: a${a} ${String(e).slice(0,70)}`); await new Promise(r2=>setTimeout(r2,2500)); }
  }
  console.log(`m${marg}: FAIL`);
}
// 1873 entries: m1-m3 (s143), m4-m10 (s144), m11-m17 (s145); 1872-tail: 26-29 (s143)
const jobs = [];
for (const m of [1,2,3]) jobs.push([m, [`${DIR}/krops/s143_L_m${m}.jpg`, `${DIR}/krops/s143_R_m${m}.jpg`]]);
for (const m of [4,5,6,7,8,9,10]) jobs.push([m, [`${DIR}/krops/s144_L_m${m}.jpg`, `${DIR}/krops/s144_R_m${m}.jpg`]]);
for (const m of [11,12,13,14,15,16,17]) jobs.push([m, [`${DIR}/krops/s145_L_m${m}.jpg`, `${DIR}/krops/s145_R_m${m}.jpg`]]);
for (const m of [26,27,28,29]) jobs.push([`t${m}`, [`${DIR}/krops/s143_L_m${m}.jpg`, `${DIR}/krops/s143_R_m${m}.jpg`]]);
for (const [m, files] of jobs) await run(m, files);
