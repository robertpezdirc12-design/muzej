// P243 — VLM pass-1 branje poročna 04455 sNN (leto 1880 predzgodovina, 6/13)
// + iskanje restart-1880 + reconciliacija s s39-top (letnica '1881' P242-1:1).
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

const IMG_DIR = '/tmp/p243';
const OUT_DIR = '/tmp/p243/pass1';
fs.mkdirSync(OUT_DIR, { recursive: true });

function promptFor(scan, tailHint) {
  return `To je razprti list (skupna št. ${scan}) poročne knjige 04455 (Trauungs-Buch) župnije Podzemelj, Nadškofijski arhiv Ljubljana, leto okvirno 1879–1881. Pisan: nemška Kurrent pisava, oblika tabele s stolpci.${tailHint}

ZGRADBA STRANI (razprti list = 2 strani knjige s skupnim oštevilčenjem):
- LEVA polovica: glava leta (velike številke) + vrstice vpisov (zaporedna št., datum, ženin, starost, stan, hiša/kraj, starši)
- DESNA polovica: nadaljevanje vrstic (nevesta, starost, stan, hiša/kraj, starši, priče, duhovnik)
- Štajerska oblika: blok glave bere se DESNO→LEVO (4 pasovi krop)

VRSTICE: išči MEJO LET: zadnji vpisi prejšnjega leta (tail), nato VELIKE številke novega leta + restart zaporedne št. = 1. Od tam naprej so vsi vpisi novega leta. Letnica '1881' je na vrhu skena 39 (P242-1:1) — na tem skenu pričakujemo tail leta 1880 in/ali velike številke '1880'.

PRAVILA:
- Prepiši VSAKO vrstico črka-za-črko; številke TOČNO kot so napisane (ne popravljaš!).
- Negotovo branje = [~], neberljivo = [?]. Ne izmišljuj.
- Hišne številke: točno kot napisane (npr. "GRIBLJE 36", "Otok 1", "½-Gütl").
- Priimki: Pezdirc/Pegdirec/Milek/Milič/Mileh/Mihelč, Brinc/Brinec/Brunc, Straus/Štraus, Silah/Silak, Klobučar/Klobasar, Šilar/Schilar, Tapič/Topic — piši TOČNO kaj vidiš, dvom = [~].
- Izhod: SAMO veljaven JSON brez ograj in komentarjev:
{"bigYearHeadings": ["leta, ki jih vidiš kot velike glave"],
 "rows": [{"no": "zap-št-kot-napisano", "date": "datum-kot-napisan", "groom": "ime + priimek + stan + hiša/kraj + starost", "groomParents": "oče × mati", "bride": "ime + priimek + stan + hiša/kraj + starost", "brideParents": "oče × mati", "witnesses": "priče", "priest": "duhovnik", "half": "L|D", "note": "[~]/[?] opombe"}],
 "mejaNote": "kje je meja med leti in kje restart",
 "pageNote": "berljivost strani"}`;
}

async function readPage(zai, scan, tailHint) {
  const img = `${IMG_DIR}/s${scan}.jpg`;
  const b64 = fs.readFileSync(img).toString('base64');
  const call = zai.chat.completions.createVision({
    messages: [{ role: 'user', content: [
      { type: 'text', text: promptFor(scan, tailHint) },
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
  const scans = process.argv.slice(2).map(Number).filter(Boolean);
  if (!scans.length) { console.error('usage: p243_vlm_pass1.mjs sNN ...'); process.exit(1); }
  const zai = await ZAI.create();
  for (const scan of scans) {
    const tailHint = scan === 39 ? " VEDNO: na vrhu te strani je letnica '1881' nad vrstico zap-št-1 (P242-1:1). Prepiši tudi njen položaj!" : '';
    console.error(`--- pass1 s${scan} ...`);
    try {
      const raw = await readPage(zai, scan, tailHint);
      const json = extractJson(raw);
      const out = `${OUT_DIR}/s${scan}.json`;
      fs.writeFileSync(out, JSON.stringify({ scan, json }, null, 2));
      const heads = json.bigYearHeadings?.join(' | ') ?? '(ni)';
      const rows = json.rows?.length ?? 0;
      console.log(`s${scan}: glave=[${heads}] vrstic=${rows} -> ${out}`);
      console.log(`  meja: ${(json.mejaNote ?? '').slice(0, 220)}`);
    } catch (e) {
      console.error(`s${scan} FAIL: ${e.message}`);
      fs.writeFileSync(`${OUT_DIR}/s${scan}.FAIL.txt`, String(e));
    }
  }
}

main().catch(e => { console.error(e); process.exit(1); });
