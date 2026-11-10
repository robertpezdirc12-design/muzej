// P246 — pass-2: ultra-zoom klope (6×) za sporne celice leta 1878
import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';

const DIR = '/home/z/p246tmp/krops3';
const OUT = '/home/z/p246tmp/pass246';
fs.mkdirSync(OUT, { recursive: true });

const files = fs.readdirSync(DIR).filter(f => f.startsWith('p246-') && f.endsWith('.jpg'));

const zai = await ZAI.create();

async function run(f) {
  const id = f.replace('p246-', '').replace('.jpg', '');
  const out = `${OUT}/ultra-${id}.json`;
  if (fs.existsSync(out)) { console.log(`${id}: že obstaja, preskočim`); return; }
  const b64 = fs.readFileSync(`${DIR}/${f}`).toString('base64');
  const prompt = `To je SKRAJNO VELIKI ZOOM (6×) dela poročne knjige (Trauungs-Buch) župnije Podzemelj, leto 1878, Kurrent-rokopis.
Prepiši TOČNO, znak za znak, vsako besedilo na sliki (od zgoraj navzdol), vključno z:
- imeni in priimki (obdrži vsa črke, šume, šumnike, škrbine),
- hišnimi številkami (dvomljive cifre označi z [~cifra]),
- poklici/stand (npr. Gübler, Inwohner, Lešanan, Ledigen-Tochter, Müller, Gärtner...),
- opombami (npr. "oba von", "sub", "geb.", "Wwe.").
Če beseda ni berljiva, napiši več variant ločenih s poševnico, npr. "Križan/Hrižan/[~]".
Izhod: SAMO veljaven JSON brez ograj:
{"cells": ["prepis vrstice 1", "prepis vrstice 2", ...], "note": "opombe o berljivosti in dvomih"}`;

  for (let attempt = 1; attempt <= 5; attempt++) {
    try {
      const completion = await Promise.race([
        zai.chat.completions.createVision({
          messages: [{ role: 'user', content: [
            { type: 'text', text: prompt },
            { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${b64}` } }
          ]}],
          thinking: { type: 'disabled' }
        }),
        new Promise((_, rej) => setTimeout(() => rej(new Error('TIMEOUT 180s')), 180000))
      ]);
      const raw = completion.choices[0]?.message?.content ?? '';
      fs.writeFileSync(out, raw);
      console.log(`${id}: OK (${raw.length})`);
      return;
    } catch (e) {
      const is429 = e.message.includes('429') || e.message.toLowerCase().includes('too many');
      console.error(`${id}: ${e.message.slice(0, 90)}`);
      if (!is429 && attempt >= 4) { fs.writeFileSync(out, `{"ERROR": "${e.message.slice(0,150)}"}`); return; }
      await new Promise(r => setTimeout(r, is429 ? 25000 : 8000));
    }
  }
}

for (const f of files) await run(f);
console.log('P246 pass-2 ultra: končano.');
