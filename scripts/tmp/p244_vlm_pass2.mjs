// P244 — pass-2: ultra-zoom branje kropov (bloki, glave, številčenje, tail-s35).
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

const CROP_DIR = '/tmp/p244/crops';
const OUT_DIR = '/tmp/p244/pass2';
fs.mkdirSync(OUT_DIR, { recursive: true });

function promptFor(name) {
  return `To je ULTRA-ZOOM izrez razprtega lista poročne knjige 04455 (Trauungs-Buch) župnije Podzemelj, leto ~1879, nemška Kurrent pisava. Izrez: ${name}.

Naloga: prepiši črka-za-črko vse, kar vidiš (številke TOČNO kot napisane, ne popravljaš!). Negotovo = [~], neberljivo = [?].

Posebno pozornost:
- Hišne številke za kraji (npr. "Griblje 17", "½-Gütl", "Otok 1", "Krasinec 18")
- Priimki: Pezdirc/Pegdirec/Perdirc, Milek/Milič/Mileh/Mihelč, Brinc/Brinec/Brunc/Princ, Križan/Hrizan/Križanec, Klobučar/Klobasar, Šilar/Schilar, Tome/Tomc, Kralj, Požeh/Pože, Helepec, Stepanič/Stepanik, Rus, Jurejevič, Škuncelj, Kugelj, Kralj
- Datumi: meseci nemško (Jänner, Feber/Februar, März, April, Mai, Juni, Juli, August, September, Oktober, November, Dezember) ali slovensko
- Zaporedne številke vpisov (prvi stolpec)
- Velike letnice (glava) — točno števke
- Vzorec: ženin (L polovica) | nevesta (D polovica) | priče + duhovnik (D dno)

Izhod: SAMO veljaven JSON:
{"transcription": "popoln prepis črka-za-črko po vrsticah",
 "keyFacts": {"zapStevilke": ["..."], "datumi": ["..."], "gribljeHise": ["vse hišne številke, ki jih vidiš za 'Griblje'"], "velikaLetnica": "če vidiš velike številke letnice", "imenaiPriimki": ["ključna imena"]},
 "opombe": "[~]/[?] negotovosti"}`;
}

async function readCrop(zai, name) {
  const b64 = fs.readFileSync(`${CROP_DIR}/${name}.jpg`).toString('base64');
  const call = zai.chat.completions.createVision({
    messages: [{ role: 'user', content: [
      { type: 'text', text: promptFor(name) },
      { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${b64}` } }
    ]}],
    thinking: { type: 'disabled' }
  });
  const completion = await Promise.race([
    call,
    new Promise((_, rej) => setTimeout(() => rej(new Error('TIMEOUT 240s')), 240000))
  ]);
  return completion.choices[0]?.message?.content ?? '';
}

function extractJson(text) {
  let t = text.replace(/```json/g, '').replace(/```/g, '').trim();
  const i = t.indexOf('{');
  const j = t.lastIndexOf('}');
  if (i >= 0 && j > i) t = t.slice(i, j + 1);
  try { return JSON.parse(t); } catch { return { raw: text.slice(0, 2000), parseError: true }; }
}

async function main() {
  const names = process.argv.slice(2);
  if (!names.length) { console.error('usage: p244_vlm_pass2.mjs crop ...'); process.exit(1); }
  const zai = await ZAI.create();
  for (const name of names) {
    process.stdout.write(`${name} ... `);
    try {
      const raw = await readCrop(zai, name);
      const data = extractJson(raw);
      fs.writeFileSync(`${OUT_DIR}/${name}.json`, JSON.stringify(data, null, 2));
      const kf = data.keyFacts || {};
      console.log(`OK zap=${JSON.stringify(kf.zapStevilke || [])} griblje=${JSON.stringify(kf.gribljeHise || [])} letnica=${kf.velikaLetnica || '-'}`);
    } catch (e) {
      console.log('FAIL', e.message);
    }
  }
}

main().catch(e => { console.error(e); process.exit(1); });
