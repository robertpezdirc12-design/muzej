import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';
import { execSync } from 'child_process';
const zai = await ZAI.create();
fs.mkdirSync('/tmp/p258/regions', { recursive: true });

// Regijska branjа za uganko s8 r4–r8 (neenakomerna razporeditev vrstic!)
const JOBS = [
  { id: 's8_reg_560_800', y0: 560, y1: 800, q: 'To je izrez LEVE strani (stolpci: datum | vas+hiša ŽENINA | ime ŽENINA | vas+hiša NEVESTE | ime NEVESTE) poročne knjige 01738, leto 1831. V izrezu so verjetno 2–3 vpisi: ~6. Juni (Michel Butala Sodevci 26 × Maria Krischan/Križan 16), nato naslednji vpis (kandidati branj: [Ignacij Ferjančec Mödling 9 × Schatzberg Gradišče 7] ali [Jožef Perman Prelo 9 × Magdalena] ali [Mathias Klobučar Griblje 46 × Catharina Klofčič 8]). PREPIŠI VSE vidne vrstice DOBESEDNO po stolpcih, vključno z datumi (paziti: 7bris=september, 8bris=oktober, 9bris=november, Xbris=december v stari nemški notaciji!). Označi meje med vpisi.' },
  { id: 's8_reg_760_990', y0: 760, y1: 990, q: 'To je izrez LEVE strani poročne knjige 01738, leto 1831. V izrezu so verjetno 2 vpisa Klobučar (Matthias Griblje 46 × Catharina 8; Johann Griblje 48 × Anna/Elisabeth 2) + morda začetek naslednjega. PREPIŠI VSE vidne vrstice DOBESEDNO po stolpcih. Datumi: 24. 8bris (oktober)? ali 24. Aug? Pazljivo na staro notacijo mesecov (7bris/8bris/9bris/Xbris)!' },
  { id: 's8_reg_960_1180', y0: 960, y1: 1180, q: 'To je izrez LEVE strani poročne knjige 01738, leto 1831. V izrezu so verjetno: zadnji Klobučar-vpis (Johann 48) + PLEMIŠKA VRSTICA (Aloys Paron/Baron, unirirter Priester, Gradič 1 × Helena Rubi/Dubil 1) + Nicol Muz Semelj 24 × Anna 15. PREPIŠI VSE vidne vrstice DOBESEDNO po stolpcih. Datumi: pazi na 9bris (november)!' },
  { id: 's8_reg_1150_1420', y0: 1150, y1: 1420, q: 'To je izrez LEVE strani poročne knjige 01738, leto 1831. V izrezu so verjetno 3 vpisi: 6. Nov (Nicol Muz Semelj 24 × Anna 15), 20. Nov (Martin Stephan/Stržinar Wörth 9 × Maria Josepha 8), zadnji (Mathias Hočevar Prest 108 × Maria Höffler 36; datum 23. d°? 2. Xbris?). PREPIŠI VSE vidne vrstice DOBESEDNO po stolpcih (pazi Xbris=december). Ali je pod zadnjim vpisom še kaj?' },
];

async function run(j) {
  const out = `/tmp/p258/regions/${j.id}.json`;
  if (fs.existsSync(out) && fs.statSync(out).size > 40) { console.log(`${j.id}: skip`); return; }
  const tmpf = `/tmp/p258/regions/_${j.id}.jpg`;
  execSync(`python3 -c "
from PIL import Image
im = Image.open('/tmp/p258/s8.jpg')
c = im.crop((40, ${j.y0}, 1050, ${j.y1}))
c = c.resize((int(c.width*1.6), int(c.height*1.6)), Image.LANCZOS)
c.save('${tmpf}', quality=93)
print(c.size)
"`);
  const content = [{ type: 'text', text: `Slika je POVEČAN IZREZ strani poročne knjige Trauungs-Buch 01738 (Podzemelj, 1831, Kurrent-pisava, nemško).\n${j.q}\nIzhod SAMO JSON: {"vrstic":N,"rows":[{"datum":"","vasZenin":"","hisZenin":0,"zenin":"","starZenin":0,"vasNevesta":"","hisNevesta":0,"nevesta":"","starNevesta":0}],"opomba":"..."}` }];
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
