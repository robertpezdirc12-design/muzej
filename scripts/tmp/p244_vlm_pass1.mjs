// P244 — VLM pass-1 branje poročna 04455 sNN (leto 1879 predzgodovina, 5/13)
// + iskanje restart-1879 + reconciliacija s s35-top (vpisi 31–33 = tail-1879 P243-1:1).
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

const IMG_DIR = '/tmp/p244';
const OUT_DIR = '/tmp/p244/pass1';
fs.mkdirSync(OUT_DIR, { recursive: true });

function promptFor(scan, tailHint) {
  return `To je razprti list (skupna št. ${scan}) poročne knjige 04455 (Trauungs-Buch) župnije Podzemelj, Nadškofijski arhiv Ljubljana, leto okvirno 1878–1880. Pisan: nemška Kurrent pisava, oblika tabele s stolpci.${tailHint}

ZGRADBA STRANI (razprti list = 2 strani knjige s skupnim oštevilčenjem):
- LEVA polovica: glava leta (velike številke) + vrstice vpisov (zaporedna št., datum, ženin, starost, stan, hiša/kraj, starši)
- DESNA polovica: nadaljevanje vrstic (nevesta, starost, stan, hiša/kraj, starši, priče, duhovnik)
- Štajerska oblika: blok glave bere se DESNO→LEVO (4 pasovi krop)

VRSTICE: išči MEJO LET: zadnji vpisi prejšnjega leta (tail), nato VELIKE številke novega leta + restart zaporedne št. = 1. Od tam naprej so vsi vpisi novega leta. Znane sile (P243-1:1): sken 35-top = vpisi 31-32-33 leta 1879 (tail!) + sken 35-dno = restart leta 1880. NA TEM SKENU pričakujemo vpise leta 1879 (ali tail leta 1878 + velike številke '1879' + restart).

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
  if (!scans.length) { console.error('usage: p244_vlm_pass1.mjs sNN ...'); process.exit(1); }
  const zai = await ZAI.create();
  for (const scan of scans) {
    const tailHint = scan === 35
      ? ' POSEBNOST: ta sken vsebuje na VRHU vpise 31-32-33 leta 1879 (tail) in na DNU restart leta 1880 (P243-1:1) — prepisi VRH brez glave!'
      : '';
    process.stdout.write(`s${scan} ... `);
    try {
      const raw = await readPage(zai, scan, tailHint);
      const data = extractJson(raw);
      fs.writeFileSync(`${OUT_DIR}/s${scan}.json`, JSON.stringify(data, null, 2));
      const rows = Array.isArray(data.rows) ? data.rows.length : 0;
      console.log(`OK rows=${rows} glave=${JSON.stringify(data.bigYearHeadings || [])}`);
    } catch (e) {
      console.log('FAIL', e.message);
    }
  }
}

main().catch(e => { console.error(e); process.exit(1); });
