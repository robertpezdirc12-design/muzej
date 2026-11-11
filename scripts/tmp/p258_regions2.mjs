import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';
import { execSync } from 'child_process';
const zai = await ZAI.create();

const JOBS = [
  { id: 's10_reg_860_1180', y0: 860, y1: 1180, q: 'Izrez LEVE strani (stolpci: DATUM | vas+hiša ŽENINA | ime ŽENINA | vas+hiša NEVESTE | ime NEVESTE) poročne knjige 01738, Pag. 17. Zgornje 2 vrstici sta še leto 1832 (28. Nov: Peter Simig/Šimič Grüble 56 × Anna Filach Grüble 61). Nato RESTART letnice 1833! V izrezu so 3 vrstice 1833: (1) Anton Sipaž/Seipa [Krainz?] 6 × Anna Auffschein [Kleffer/Klofter?] 43 — DATUM: 3. ali 5. Febr 1833? KJE piše letnica 1833?; (2) Nicol Tonz [Kaplice?/Laune?] 3 × Barbara Frithovigh [Mühle?] 2 — datum 5./6. d°?; (3) Mathias Jurjepfzhig [Mlake?] 11 × Catharina Jafllig [Podsmell?] 12 — 6. Febr. PREPIŠI VSE vrstice DOBESEDNO po stolpcih, posebno pozorno na datume + letnico 1833!' },
  { id: 's10_reg_1140_1420', y0: 1140, y1: 1420, q: 'Izrez LEVE strani poročne knjige 01738, Pag. 17, leto 1833 (6. Febr). V izrezu so zadnje 3 vrstice strani: (1) Marcus/Martin Papizh/Parpich [Gorschiz?] 6 × Catharina Angel Dobravlje 22; (2) ★★★ Nicolaus Petras/Petrin [Draphigh/Tratzhig?] [25?|36?] × Catharina [MUZ?? — družina iz Semelja!] [Pino/Grintez?] 4; (3) ★★★ Johann [PESDIRZ?? PETROVIZ??] Grüble 50 × Maria [Himiz?/Thaviz?/Simig?] Grüble 49 — ZADNJA VRSTICA STRANI! PREPIŠI VSE vrstice DOBESEDNO po stolpcih. PRI ZADNJI VRSTICI preberi priimek ženina ČRKO ZA ČRKO (Pesdirz ima očeta Marco Pesdirz 1831, hiša 50 = ista!) in priimek neveste črko za črko!' },
];

async function run(j) {
  const out = `/tmp/p258/regions/${j.id}.json`;
  if (fs.existsSync(out) && fs.statSync(out).size > 40) { console.log(`${j.id}: skip`); return; }
  const tmpf = `/tmp/p258/regions/_${j.id}.jpg`;
  execSync(`python3 -c "
from PIL import Image
im = Image.open('/tmp/p258/s10.jpg')
c = im.crop((40, ${j.y0}, 1230, ${j.y1}))
c = c.resize((int(c.width*1.7), int(c.height*1.7)), Image.LANCZOS)
c.save('${tmpf}', quality=93)
print(c.size)
"`);
  const content = [{ type: 'text', text: `Slika je POVEČAN IZREZ strani poročne knjige Trauungs-Buch 01738 (Podzemelj, 1832/1833, Kurrent-pisava, nemško).\n${j.q}\nIzhod SAMO JSON: {"vrstic":N,"rows":[{"datum":"","leto":0,"vasZenin":"","hisZenin":0,"zenin":"","starZenin":0,"vasNevesta":"","hisNevesta":0,"nevesta":"","starNevesta":0,"opombaVR":""}],"opomba":"..."}` }];
  content.push({ type: 'image_url', image_url: { url: `data:image/jpeg;base64,${fs.readFileSync(tmpf).toString('base64')}` } });
  for (let a = 1; a <= 4; a++) {
    try {
      const r = await zai.chat.completions.createVision({
        messages: [{ role: 'user', content }],
        temperature: 0.1, max_tokens: 1500, thinking: { type: 'disabled' },
      });
      fs.writeFileSync(out, r.choices[0].message.content || '');
      console.log(`${j.id}: OK`);
      return;
    } catch (e) { console.log(`${j.id}: a${a} ${String(e).slice(0,70)}`); await new Promise(r2=>setTimeout(r2,2500)); }
  }
  console.log(`${j.id}: FAIL`);
}
for (const j of JOBS) { await run(j); await new Promise(r=>setTimeout(r,1200)); }
