// P243 — VLM pass-5: s35 dno/glava + s36 top zona (6 klicev).
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';
const CROPS = '/tmp/p243/crops5';
const OUT = '/tmp/p243/pass5';
fs.mkdirSync(OUT, { recursive: true });
function extractJson(text) {
  let t = (text ?? '').replace(/```json/g, '').replace(/```/g, '').trim();
  const i = t.indexOf('{'); const j = t.lastIndexOf('}');
  if (i >= 0 && j > i) t = t.slice(i, j + 1);
  try { return JSON.parse(t); } catch { return { raw: t.slice(0, 1200), parseError: true }; }
}
async function main() {
  const zai = await ZAI.create();
  const jobs = [
    ['s35-numcol-full-3x', 'STOLPEC zaporednih številk (3×, polna višina, stran s35 poročne knjige 04455). Prepiši VSAKO številko vrh→dno; štej vrstice. SAMO JSON: {"numbers": [...], "count": N}' ],
    ['s35-dno', 'DNO strani s35 (poročna 04455, ~1879/1880) — prepiši VSE: zadnje vrstice, datume, imena, hiše, ali je tu VELIKA letnica (1880? 1879?) ali restart številčenja (številke 1-2?). SAMO JSON: {"reading": "...", "rows": [...], "bigNumbers": [...], "note": "..."}'],
    ['s35-glava-zona', 'Glava strani s35 — kaj piše (Trauungs-Buch? letnica? velike številke?)? SAMO JSON: {"heading": "...", "bigNumbers": [...]}'],
    ['s35-datumcol-top-3x', 'Datumski stolpec vrh s35 3× — kaj piše? Letnica? Prvi datum? SAMO JSON: {"reading": "..."}'],
    ['s35-datumcol-dno-3x', 'Datumski stolpec dno s35 3× — kaj piše (datumi zadnjih vrstic? letnica 1880?). SAMO JSON: {"reading": "..."}'],
    ['s36-top-zona-3x', 'VRH strani s36 3× (zona letnica+vrste 1-2) — prepiši VSE znak-za-znak: letnica 1880 položaj, datume, zap-št. (1? 2? 3?), imena prvih vrstic. SAMO JSON: {"reading": "...", "numbers": [...], "dates": [...]}'],
  ];
  const results = {};
  for (const [file, ask] of jobs) {
    console.error(`--- ${file}`);
    try {
      const b64 = fs.readFileSync(`${CROPS}/${file}.jpg`).toString('base64');
      const call = zai.chat.completions.createVision({
        messages: [{ role: 'user', content: [
          { type: 'text', text: `${ask} Kurrent pisava ~1880, poročna knjiga 04455 Podzemelj. Negotovo=[~], neberljivo=[?].` },
          { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${b64}` } }
        ]}],
        thinking: { type: 'disabled' }
      });
      const completion = await Promise.race([call, new Promise((_, rej) => setTimeout(() => rej(new Error('TIMEOUT 150s')), 150000))]);
      const j = extractJson(completion.choices[0]?.message?.content);
      results[file] = j;
      fs.writeFileSync(`${OUT}/${file}.json`, JSON.stringify(j, null, 2));
      console.log(`${file}: ${JSON.stringify(j).slice(0, 400)}`);
    } catch (e) { console.error(`${file} FAIL: ${e.message}`); results[file] = { fail: e.message }; }
  }
  fs.writeFileSync('/tmp/p243/pass5/ALL.json', JSON.stringify(results, null, 2));
  console.log('PASS5 DONE');
}
main().catch(e => { console.error(e); process.exit(1); });
