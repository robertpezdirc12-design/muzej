// P243 — VLM pass-3: vrstični trakovi L+R (18) + številčni stolpci 3× (3).
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

const CROPS = '/tmp/p243/crops3';
const OUT = '/tmp/p243/pass3';
fs.mkdirSync(OUT, { recursive: true });

const ROW_STRUCT = `To je ENA vrstica poročnega vpisa (Trauungs-Buch 04455 Podzemelj, Kurrent, ~1880). Lev del = ženin (datum, ime/priimek, stan, hiša/vas, starost, starši ženina), desni del = nevesta (ime/priimek, stan, hiša/vas, starost, starši neveste) + priče + duhovnik + zaporedna št. levo. Prepiši TOČNO, znak-za-znak; številke s črkami razloži (npr. '8 — dvom 9'). Negotovo=[~], neberljivo=[?]. SAMO JSON: {"zapSt": "...", "datum": "...", "zenin": "...", "starostZenin": "...", "hisaZenin": "...", "starsZenin": "...", "nevesta": "...", "starostNevesta": "...", "hisaNevesta": "...", "starsNevesta": "...", "price": "...", "duhovnik": "...", "opombe": "..."}`;

async function read(zai, file, ask) {
  const b64 = fs.readFileSync(`${CROPS}/${file}.jpg`).toString('base64');
  const call = zai.chat.completions.createVision({
    messages: [{ role: 'user', content: [
      { type: 'text', text: ask },
      { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${b64}` } }
    ]}],
    thinking: { type: 'disabled' }
  });
  const completion = await Promise.race([call, new Promise((_, rej) => setTimeout(() => rej(new Error('TIMEOUT 180s')), 180000))]);
  let t = (completion.choices[0]?.message?.content ?? '').replace(/```json/g, '').replace(/```/g, '').trim();
  const i = t.indexOf('{'); const j = t.lastIndexOf('}');
  if (i >= 0 && j > i) t = t.slice(i, j + 1);
  try { return JSON.parse(t); } catch { return { raw: t.slice(0, 1200), parseError: true }; }
}

async function main() {
  const zai = await ZAI.create();
  const results = {};
  const jobs = [];
  for (const page of ['s36', 's37', 's38'])
    for (let r = 1; r <= 6; r++)
      jobs.push([`${page}-r${r}-L`, `${ROW_STRUCT} (LEVI trak — ženinska polovica vrstice ${r} strani ${page})`],
                [`${page}-r${r}-R`, `${ROW_STRUCT} (DESNI trak — nevestna polovica vrstice ${r} strani ${page})`]);
  for (const page of ['s36', 's37', 's38'])
    jobs.push([`${page}-numcol-3x`, `To je STOLPEC zaporednih številk (3× zoom, stran ${page}). Prepiši VSAKO številko vrh→dno kot jo vidiš znak-za-znak; dvome označi [~]. SAMO JSON: {"numbers": ["..."], "count": N}`]);

  for (const [file, ask] of jobs) {
    console.error(`--- ${file}`);
    try {
      const j = await read(zai, file, ask);
      results[file] = j;
      fs.writeFileSync(`${OUT}/${file}.json`, JSON.stringify(j, null, 2));
      if (file.includes('numcol')) console.log(`${file}: ${JSON.stringify(j.numbers ?? j.raw ?? '')}`);
      else console.log(`${file}: Z=${(j.zenin ?? j.raw ?? '').slice(0, 55)} × N=${(j.nevesta ?? '').slice(0, 45)} | hZ=${j.hisaZenin} hN=${j.hisaNevesta}`);
    } catch (e) { console.error(`${file} FAIL: ${e.message}`); results[file] = { fail: e.message }; }
  }
  fs.writeFileSync('/tmp/p243/pass3/ALL.json', JSON.stringify(results, null, 2));
  console.log('PASS3 DONE');
}

main().catch(e => { console.error(e); process.exit(1); });
