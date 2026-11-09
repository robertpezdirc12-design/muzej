// P240 — VLM pass-1 branje poročna 04455 s50–s52 (leto 1883 predzgodovina, 3/13)
// + kontrolno branje s52-tail (vpisi 8–12 že iz P239) za 1:1 preverbo.
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

const IMG_DIR = '/tmp/p240';
const OUT_DIR = '/tmp/p240/pass1';

function promptFor(scan, tailHint) {
  return `To je razprti list (skupna št. ${scan}) poročne knjige 04455 (Trauungs-Buch) župnije Podzemelj, Nadškofijski arhiv Ljubljana, leto okvirno 1882/1883. Pisan: nemška Kurrent pisava, oblika tabele s stolpci.${tailHint}

ZGRADBA STRANI (razprti list = 2 strani knjige s skupnim oštevilčenjem):
- LEVA polovica: glava leta (velike številke) + vrstice vpisov (zaporedna št., datum, ženin, starost, stan, hiša/kraj, starši)
- DESNA polovica: nadaljevanje vrstic (nevesta, starost, stan, hiša/kraj, starši, priče, duhovnik)
- Štajerska oblika: blok glave bere se DESNO→LEVO (4 pasovi krop)

VRSTICE: išči MEJO LET: zadnji vpisi prejšnjega leta (tail), nato VELIKE številke novega leta + restart zaporedne št. = 1. Od tam naprej so vsi vpisi novega leta.

PRAVILA:
- Prepiši VSAKO vrstico črka-za-črko; številke TOČNO kot so napisane (ne popravljaš!).
- Negotovo branje = [~], neberljivo = [?]. Ne izmišljuj.
- Hišne številke: točno kot napisane (npr. "GRIBLJE 47", "Otok 1", "½-Gütl").
- Surnames: Pezdirc/Pegdirec/Milek/Milič/Mileh, Brinc/Brinec/Brunc, Straus/Štraus, Silah/Silak, Hvalc/Hlepec — piši TOČNO kaj vidiš, dvom = [~].
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

async function main() {
  const scans = process.argv.slice(2).map(Number).filter(Boolean).length
    ? process.argv.slice(2).map(Number).filter(Boolean)
    : [50, 51, 52];
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const zai = await ZAI.create();
  for (const scan of scans) {
    const out = `${OUT_DIR}/s${scan}.json`;
    if (fs.existsSync(out)) { console.log(' obstoji:', out); continue; }
    const tailHint = scan === 51
      ? ' NAMIG: išči velike številke »1883« + RESTART zaporedne številke na 1 (leto 1883 se začne; pred tem so tail-vpisi leta 1882).'
      : scan === 52
      ? ' NAMIG: VSE vrstice so TAIL leta 1883 (vpisi 8–12, napisani leta 1883, velika glava »1883«) — na tem listu NI restarta; 1884 se začne na naslednjem listu.'
      : scan === 50
      ? ' NAMIG: verjetno tail-vpisi leta 1882; na dnu (ali naslednji list) velike številke »1883« — povej točno kje.'
      : '';
    process.stdout.write(` s${scan} ... `);
    let content = '';
    for (let attempt = 1; attempt <= 2; attempt++) {
      try { content = await readPage(zai, scan, tailHint); break; }
      catch (e) { console.log(`poskus ${attempt} NAPAKA: ${e.message}`); if (attempt === 2) content = ''; }
    }
    const clean = content.replace(/^```json\n?/, '').replace(/\n?```$/, '').trim();
    try {
      const parsed = JSON.parse(clean);
      fs.writeFileSync(out, JSON.stringify(parsed, null, 1), 'utf-8');
      console.log(`OK vrstice=${parsed.rows?.length} leta=${JSON.stringify(parsed.bigYearHeadings)}`);
    } catch (e) {
      fs.writeFileSync(out.replace('.json', '.raw.txt'), content, 'utf-8');
      console.log('RAW (ni bil JSON):', e.message.slice(0, 60));
    }
  }
}
main().catch(e => { console.error('FATAL', e.message); process.exit(1); });
