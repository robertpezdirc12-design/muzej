import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';
const DIR = '/tmp/p253';
const zai = await ZAI.create();

// KONTEKST: 04455 (nova knjiga) Pag.1 prvi vpis m18 = 11. Juni 1873:
// ženin Mathias GABOVŠIČ (Griblje 13) × nevesta Maria HRIŽAN (Griblje 62), 19 let.
// S146 = ZADNJA stran STARE knjige 01738 — 1 fizična vrstica, PREKRIŽANA (kand. = isti vpis!).
const QS = {
  'seam1': `Tri slike = isti izrez (marginala+datum) zadnje fizične vrstice na zadnji strani poročne knjige 01738 (1873, Kurrent) v treh obdelavah (kontrast/autocontrast/svetlost). Vrstica je domnevno PREKRIŽANA (križ čez njo).
Prepiši: (1) marginalno številko (kand. 18 ali 11 ali 17 — pazi Kurrent '8' vs '1'), (2) DATUM (kand. '11. Juni 1873' ali 'April'), (3) ali je vrstica prekrižana (enojna/dvojna črta).
Izhod SAMO JSON: {"marg":"","datum":"","preckrizana":"","razlaga":""}`,
  'seam2': `Tri slike = isti izrez (ženin: ime+priimek+status+starost) zadnje fizične vrstice na zadnji strani knjige 01738 (1873, Kurrent). KONTEKST: v novi knjigi 04455 je prvi vpis m18 (11.6.1873) = ženin 'Mathias GABOVŠIČ' (Griblje 13), nevesta 'Maria HRIŽAN' (Griblje 62).
Prepiši ženinovo ime, priimek (kand. 'Gabovšič/Jabovšič/Josefič/Jakopec'), status, starost.
Izhod SAMO JSON: {"ime":"","priimek":"","status":"","starost":"","razlaga":""}`,
  'seam3': `Tri slike = isti izrez (ženinov Wohnort + hiša) zadnje fizične vrstice (01738, 1873, Kurrent). Kand. hiša: 13 (kot v 04455-m18!) ali 15 ali 1. Pazi Kurrent: '1' vs '4' vs '5'.
Izhod SAMO JSON: {"vas":"","hisa":"","razlaga":""}`,
  'seam4': `Tri slike = isti izrez (nevesta: ime+priimek+vas+hiša) zadnje fizične vrstice (01738, 1873, Kurrent). KONTEKST: v novi knjigi 04455 m18 nevesta = 'Maria HRIŽAN' (Griblje 62), 19 let — kand. priimek tukaj: 'Hrižan/Križan/Krigzer/Kriblje'; hiša kand. 62.
Izhod SAMO JSON: {"ime":"","priimek":"","hisa":"","starost":"","razlaga":""}`,
};
const FILES = {
  'seam1': ['zoom_marg_a.jpg','zoom_marg_b.jpg','zoom_marg_c.jpg'],
  'seam2': ['zoom_zenin_a.jpg','zoom_zenin_b.jpg','zoom_zenin_c.jpg'],
  'seam3': ['zoom_zenin2_a.jpg','zoom_zenin2_b.jpg','zoom_zenin2_c.jpg'],
  'seam4': ['zoom_nevesta_a.jpg','zoom_nevesta_b.jpg','zoom_nevesta_c.jpg'],
};
async function ask(id) {
  const out = `${DIR}/${id}.json`;
  if (fs.existsSync(out)) { console.log(`${id}: skip`); return; }
  const content = [{ type: 'text', text: QS[id] }];
  for (const f of FILES[id]) content.push({ type: 'image_url', image_url: { url: `data:image/jpeg;base64,${fs.readFileSync(`${DIR}/${f}`).toString('base64')}` } });
  for (let a = 1; a <= 5; a++) {
    try {
      const r = await zai.chat.completions.createVision({
        messages: [{ role: 'user', content }],
        temperature: 0.1, max_tokens: 900, thinking: { type: 'disabled' },
      });
      fs.writeFileSync(out, r.choices[0].message.content || '');
      console.log(`${id}: OK`);
      await new Promise(r2=>setTimeout(r2,9000));
      return;
    } catch (e) { console.log(`${id}: a${a} ${String(e).slice(0,50)}`); await new Promise(r2=>setTimeout(r2,12000)); }
  }
  console.log(`${id}: FAIL`);
}
for (const id of Object.keys(QS)) await ask(id);
