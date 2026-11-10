// P243 — VLM pass-4: s36 z 8 trakovi + polni numcol + glava + datumstolpec (19 VLM klicev).
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

const CROPS = '/tmp/p243/crops4';
const OUT = '/tmp/p243/pass4';
fs.mkdirSync(OUT, { recursive: true });

const ROW_STRUCT = `To je ENA vrstica poročnega vpisa (Trauungs-Buch 04455 Podzemelj, Kurrent, 1880). Lev del = zap. št. + datum + ženin (ime/priimek, stan, hiša/vas, starost, starši), desni del = nevesta (ime/priimek, stan, hiša/vas, starost, starši) + priče + duhovnik. Prepiši TOČNO znak-za-znak; številke s črkami razloži. Negotovo=[~], neberljivo=[?]. SAMO JSON: {"zapSt": "...", "datum": "...", "zenin": "...", "stan": "...", "hisaZenin": "...", "starsZenin": "...", "nevesta": "...", "hisaNevesta": "...", "starsNevesta": "...", "price": "...", "duhovnik": "...", "opombe": "..."}`;

function extractJson(text) {
  let t = (text ?? '').replace(/```json/g, '').replace(/```/g, '').trim();
  const i = t.indexOf('{'); const j = t.lastIndexOf('}');
  if (i >= 0 && j > i) t = t.slice(i, j + 1);
  try { return JSON.parse(t); } catch { return { raw: t.slice(0, 1200), parseError: true }; }
}

async function main() {
  const zai = await ZAI.create();
  const results = {};
  const jobs = [];
  for (let r = 1; r <= 8; r++)
    jobs.push([`s36-8r${r}-L`, `${ROW_STRUCT} (LEVI trak — vrstica ${r}/8 strani s36)`],
              [`s36-8r${r}-R`, `${ROW_STRUCT} (DESNI trak — nevestna polovica vrstice ${r}/8 strani s36)`]);
  jobs.push(['s36-numcol-full-3x', `STOLPEC zaporednih številk 3× (polna višina, stran s36). Prepiši VSAKO številko vrh→dno znak-za-znak; če je številka šibka/izgubljena, povej koliko vrstic VIDIŠ in kje. SAMO JSON: {"numbers": [...], "count": N, "note": "..."}`]);
  jobs.push(['s36-glava-zona', `Glava strani s36 — prepiši VSE: Trauungs-Buch naslov, VELIKE številke leta (1880?) in njihov NATAČEN položaj (v glavi strani? nad vrsto 1? v datumskem stolpcu?), morebitni prvi datum. SAMO JSON: {"heading": "...", "position": "opis položaja", "firstDate": "..."}`]);
  jobs.push(['s36-datumcol-top-3x', `Datumski stolpec vrh strani s36 3× — ali je tu letnica '1880' (kot P242-varianta-1881) ali prvi datum? Kaj TOČNO piše nad vrsto 1? SAMO JSON: {"reading": "...", "position": "..."}`]);

  for (const [file, ask] of jobs) {
    console.error(`--- ${file}`);
    try {
      const b64 = fs.readFileSync(`${CROPS}/${file}.jpg`).toString('base64');
      const call = zai.chat.completions.createVision({
        messages: [{ role: 'user', content: [
          { type: 'text', text: ask },
          { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${b64}` } }
        ]}],
        thinking: { type: 'disabled' }
      });
      const completion = await Promise.race([call, new Promise((_, rej) => setTimeout(() => rej(new Error('TIMEOUT 150s')), 150000))]);
      const j = extractJson(completion.choices[0]?.message?.content);
      results[file] = j;
      fs.writeFileSync(`${OUT}/${file}.json`, JSON.stringify(j, null, 2));
      if (file.includes('numcol')) console.log(`${file}: ${JSON.stringify(j.numbers ?? '')} ${j.note ?? ''}`);
      else if (file.includes('glava') || file.includes('datumcol')) console.log(`${file}: ${JSON.stringify(j).slice(0, 300)}`);
      else console.log(`${file}: zap=${j.zapSt} d=${j.datum} | Z=${(j.zenin ?? '').slice(0, 40)} hZ=${j.hisaZenin} | N=${(j.nevesta ?? '').slice(0, 35)} hN=${j.hisaNevesta}`);
    } catch (e) { console.error(`${file} FAIL: ${e.message}`); results[file] = { fail: e.message }; }
  }
  fs.writeFileSync('/tmp/p243/pass4/ALL.json', JSON.stringify(results, null, 2));
  console.log('PASS4 DONE');
}

main().catch(e => { console.error(e); process.exit(1); });
