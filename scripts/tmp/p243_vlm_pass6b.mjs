// P243 — pass-6b: Pag koti (5 klicev).
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';
const CROPS = '/tmp/p243/crops6';
const OUT = '/tmp/p243/pass6';
function extractJson(text) {
  let t = (text ?? '').replace(/```json/g, '').replace(/```/g, '').trim();
  const i = t.indexOf('{'); const j = t.lastIndexOf('}');
  if (i >= 0 && j > i) t = t.slice(i, j + 1);
  try { return JSON.parse(t); } catch { return { raw: t.slice(0, 600), parseError: true }; }
}
async function main() {
  const zai = await ZAI.create();
  const jobs = ['s38-kot-TL', 's38-kot-TR', 's38-kot-BL', 's38-kot-BR', 's39-kot-TR'];
  const results = {};
  for (const file of jobs) {
    console.error(`--- ${file}`);
    try {
      const b64 = fs.readFileSync(`${CROPS}/${file}.jpg`).toString('base64');
      const call = zai.chat.completions.createVision({
        messages: [{ role: 'user', content: [
          { type: 'text', text: `Kot strani razprtega lista poročne knjige 04455 Podzemelj (~1880) 3×. Išči paginacijo: 'Pag. NN' ali številka v kotu. Prepiši TOČNO številke znak-za-znak (razlikuj 3/4/7/8/9!). SAMO JSON: {"reading": "", "pageNo": "..."}` },
          { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${b64}` } }
        ]}],
        thinking: { type: 'disabled' }
      });
      const completion = await Promise.race([call, new Promise((_, rej) => setTimeout(() => rej(new Error('TIMEOUT 120s')), 120000))]);
      const j = extractJson(completion.choices[0]?.message?.content);
      results[file] = j;
      fs.writeFileSync(`${OUT}/${file}.json`, JSON.stringify(j, null, 2));
      console.log(`${file}: ${JSON.stringify(j).slice(0, 200)}`);
    } catch (e) { console.error(`${file} FAIL: ${e.message}`); results[file] = { fail: e.message }; }
  }
  fs.writeFileSync('/tmp/p243/pass6/koti.json', JSON.stringify(results, null, 2));
  console.log('KOTI DONE');
}
main().catch(e => { console.error(e); process.exit(1); });
