// P246 — pass-3: polne vrstične klope ×4 za sporne vrstice leta 1878
import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';

const DIR = '/home/z/p246tmp/krops4';
const OUT = '/home/z/p246tmp/pass246';
fs.mkdirSync(OUT, { recursive: true });

const files = fs.readdirSync(DIR).filter(f => f.startsWith('p246-') && f.endsWith('.jpg'));

const zai = await ZAI.create();

async function run(f) {
  const id = f.replace('p246-', '').replace('-row.jpg', '');
  const out = `${OUT}/row-${id}.json`;
  if (fs.existsSync(out)) { console.log(`${id}: že obstaja, preskočim`); return; }
  const b64 = fs.readFileSync(`${DIR}/${f}`).toString('base64');
  const prompt = `To je VELIKI ZOOM (4×) ENE VRSTICE (ali njenega dela) iz poročne knjige (Trauungs-Buch) župnije Podzemelj, leto 1878, Kurrent-rokopis.
Vrstica ima stolpce (levo→desno): [datum poroke] | [Wohnort ženina + Hiš-Nr.] | [Tauname, Familien-Name und Stand ženina] | [starost ženina] | [Wohnort neveste + Hiš-Nr.] | [Tauname, Familien-Name und Stand neveste] | [starost neveste].
Prepiši TOČNO, znak za znak, celotno vsebino VRSTICE stolpec po stolpec (od zgoraj navzdol, če je več vrstic besedila v eni celici). Pri številkah, ki niso jasne, ponudi alternativo: "63/65". Poudarek: natančno beri PRVE ČRKE imen (K vs. H!) in hišne številke.
Izhod: SAMO veljaven JSON brez ograj:
{"datum": "...", "groomWohnort": "...", "groomName": "...", "groomStarost": "...", "brideWohnort": "...", "brideName": "...", "brideStarost": "...", "note": "dvomi"}`;

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
console.log('P246 pass-3 vrstice: končano.');
