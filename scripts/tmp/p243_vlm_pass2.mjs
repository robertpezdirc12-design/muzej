// P243 — VLM pass-2: ultra-zoom klope (številčenje, glava, Pag-kot, bloki, s39-recon).
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

const CROPS = '/tmp/p243/crops';
const OUT = '/tmp/p243/pass2';
fs.mkdirSync(OUT, { recursive: true });

function readOne(zai, crop, name) {
  const b64 = fs.readFileSync(`${CROPS}/${crop}.jpg`).toString('base64');
  return zai.chat.completions.createVision({
    messages: [{ role: 'user', content: [
      { type: 'text', text: `To je ultra-zoom izrez iz poročne knjige 04455 župnije Podzemelj (Kurrent pisava, ~1880). Izrez: ${name}. Prepiši črka-za-črko TOČNO kaj vidiš; številke znak-za-znak (razlike 3/5/8/9, 4/6, 1/7 povej eksplicitno kaj gašaš videti). Negotovo=[~], neberljivo=[?]. SAMO JSON: {"reading": "...", "numbers": ["..."], "details": "..."}` },
      { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${b64}` } }
    ]}],
    thinking: { type: 'disabled' }
  });
}

function extractJson(text) {
  let t = text.replace(/```json/g, '').replace(/```/g, '').trim();
  const i = t.indexOf('{'); const j = t.lastIndexOf('}');
  if (i >= 0 && j > i) t = t.slice(i, j + 1);
  try { return JSON.parse(t); } catch { return { raw: text.slice(0, 1500), parseError: true }; }
}

async function main() {
  const jobs = [
    ['s36-glava', 's36 velika glava — kakšna je položaj/dimenzija letnice 1880? NAD vrsto zap-št-1 ali v glavi strani? Kaksna oblika (velika ročna, podčrtana, v stolpcu)?'],
    ['s36-stolpec-L', 's36 levi stolpec zaporednih št. — preštej in prepiši VSE številke vrstic od vrha do dna (pričakujemo 1–8 ali 1–6)!'],
    ['s36-desna', 's36 desna polovica vrstice — prepiši zap. št. + imena nevest (pričakujemo vpisi 4–8?)'],
    ['s36-blok-v2v3', 's36 bloka v2+v3 — ženin v2 priimek (Brinc?), hiša 25? nevesta v2 hiša 18? v3 ženin priimek (Kure/Kura?), hiša Griblje 10?, nevesta Klevič?, hiša Griblje 11? Prepiši zvezno.'],
    ['s37-stolpec-L', 's37 levi stolpec zaporednih št. — prepiši VSE številke (pričakujemo 7–14 ali 9–14 — REŠI LUKNJO 7–8!)'],
    ['s37-glava', 's37 vrh strani — ali je tam kaj glave (velike številke, nadaljevalni znak, Pag)?'],
    ['s37-v13v14', 's37 v13+v14 — v14: ženin ime/priimek (Bričan/Brižan?), vasi; nevesta v14: Konstantia Pegdirec/Pezdirc? hiša GRIBLJE? Prepiši zvezno.'],
    ['s38-stolpec-L', 's38 levi stolpec zaporednih št. — prepiši VSE (pričakujemo 15–20) + ali je na dnu vsota?'],
    ['s38-pag-kot', 's38 kot — prepiši Pag. oznako TOČNO (pričakujemo Pag. 37 ali 34!)'],
    ['s38-pag-kot-L', 's38 levi spodnji kot — kaj piše? Pag/številka?'],
    ['s38-v20', 's38 v20 — ženin: Peter Pegdirec/Pezdirc? hiša GRIBLJE 53? nevesta Anna Zupančič? Krasinec 18? Prepiši zvezno.'],
    ['s38-dno-vsote', 's38 dno — rezane vsote/štetje (m21? n1? i8/0?) — prepiši TOČNO.'],
    ['s39-top-recon', 's39 VRH — reconciliacija: letnica 1881 — kje STOJI (v datumskem stolpcu NAD vrsto 1, kot je rekel P242)? + vpiši zap-št-1 datum (16. Jänner?). Prepiši.'],
  ];
  const zai = await ZAI.create();
  const results = {};
  for (const [crop, ask] of jobs) {
    console.error(`--- pass2 ${crop} ...`);
    try {
      const b64 = fs.readFileSync(`${CROPS}/${crop}.jpg`).toString('base64');
      const call = zai.chat.completions.createVision({
        messages: [{ role: 'user', content: [
          { type: 'text', text: `${ask} (Kurrent pisava ~1880, poročna knjiga 04455 Podzemelj. Negotovo=[~], neberljivo=[?]. SAMO JSON: {"reading": "...", "numbers": [...], "details": "..."})` },
          { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${b64}` } }
        ]}],
        thinking: { type: 'disabled' }
      });
      const completion = await Promise.race([call, new Promise((_, rej) => setTimeout(() => rej(new Error('TIMEOUT 180s')), 180000))]);
      const json = extractJson(completion.choices[0]?.message?.content ?? '');
      results[crop] = json;
      fs.writeFileSync(`${OUT}/${crop}.json`, JSON.stringify(json, null, 2));
      console.log(`${crop}: ${(json.reading ?? json.raw ?? '').slice(0, 260)}`);
    } catch (e) {
      console.error(`${crop} FAIL: ${e.message}`);
      results[crop] = { fail: e.message };
    }
  }
  fs.writeFileSync('/tmp/p243/pass2/ALL.json', JSON.stringify(results, null, 2));
  console.log('PASS2 DONE');
}

main().catch(e => { console.error(e); process.exit(1); });
