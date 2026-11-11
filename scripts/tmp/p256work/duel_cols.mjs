import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';
const zai = await ZAI.create();

const JOBS = [
  { id: 's4_datecol', f: 's4_datecol.jpg' },
  { id: 's4_colW', f: 's4_colW.jpg', skip: true }, // ne obstaja
  { id: 's5_datecol', f: 's5_datecol.jpg' },
  { id: 's5_colW', f: 's5_colW.jpg' },
  { id: 's6_datecol', f: 's6_datecol.jpg' },
  { id: 's6_colW', f: 's6_colW.jpg' },
  { id: 's7_datecol', f: 's7_datecol.jpg' },
  { id: 's7_colW', f: 's7_colW.jpg' },
];

const PROMPT = `Slika je VISOKO POVEČAN datumski stolpec (stolpec 'Jahr, Monat und Tag der Trauung') poročne knjige 01738 (Podzemelj), Kurent/Kurrent-pisava, 19. stoletje.
Naloga: PREPIŠI VSE, kar vidiš, ZGORAJ DOL, brez predpostavk. Vsako datumno vrednost (dan, mesec, letnica) v zaporedju, kot je zapisana. Mesec je lahko napisan enkrat, nato ponovljen z ditto-znaki (navpične črtice, '=', 'dto', 'ejusd.'). Okrajšave: 7br=September, 8br=Oktober, 9br=November, Xbr/10br=Dezember.
POMEMBNO: ne ugibaj zaporedja datumov — prepisi SAMO tisto, kar je dejansko razločno vidno. Nejasna mesta označi [~]. Prazne vrstice med vnosi označi kot (prazna).
Izhod SAMO JSON: {"vnosi":[{"vidno":"...","dan":null,"mesec":null,"leto":null,"zanesljivost":"visoka/srednja/nizka"}],"st_vpisov":0,"razlaga":""}`;

async function run(job) {
  if (job.skip) return;
  const p = `/tmp/p256/datecol/${job.f}`;
  if (!fs.existsSync(p)) { console.log(`${job.id}: MANJKA`); return; }
  const out = `/tmp/p256/datecol/${job.id}_NEUTRAL.json`;
  if (fs.existsSync(out)) { console.log(`${job.id}: skip`); return; }
  const content = [{ type: 'text', text: PROMPT }];
  content.push({ type: 'image_url', image_url: { url: `data:image/jpeg;base64,${fs.readFileSync(p).toString('base64')}` } });
  for (let a = 1; a <= 4; a++) {
    try {
      const r = await zai.chat.completions.createVision({
        messages: [{ role: 'user', content }],
        temperature: 0.1, max_tokens: 2000, thinking: { type: 'disabled' },
      });
      fs.writeFileSync(out, r.choices[0].message.content || '');
      console.log(`${job.id}: OK`);
      return;
    } catch (e) { console.log(`${job.id}: a${a} ${String(e).slice(0,60)}`); await new Promise(r2=>setTimeout(r2,4000)); }
  }
  console.log(`${job.id}: FAIL`);
}
for (const j of JOBS) { await run(j); await new Promise(r=>setTimeout(r,1500)); }
