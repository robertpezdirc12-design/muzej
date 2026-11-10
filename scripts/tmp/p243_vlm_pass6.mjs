// P243 — VLM pass-6: finalne ultra-zoom celice (12 klicev).
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';
const CROPS = '/tmp/p243/crops6';
const OUT = '/tmp/p243/pass6';
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
    ['s35-numcol-dno-4x', 'Številčni stolpec dno strani s35 4× — pričakujemo 31, 32, 33, nato RESTART 1, 2 (leto 1880!). Prepiši vsako številko znak-za-znak. SAMO JSON: {"numbers": [...]}'],
    ['s35-dno-L', 'Dno strani s35 LEVI pol — zadnji 2 vrstici: zap-št, datum (Jänner 1880?), ženin (Jožef Kvas?), hiša/vas, starost, starši. SAMO JSON: {"rows": [{"zapSt": "", "datum": "", "zenin": "", "vas": "", "hisa": "", "starost": ""}]}'],
    ['s35-dno-R', 'Dno strani s35 DESNI pol — nevesti zadnjih 2 vrstic (Marija Dragot/Dragote?), hiše, priče, duhovnik. SAMO JSON: {"rows": [{"nevesta": "", "vas": "", "hisa": "", "priče": "", "duhovnik": ""}]}'],
    ['s36-r3-L', 'Vrstica 3 strani s36 (zap-št 3, datum 4. Febr 1880?) LEVI pol — ženin: ime/priimek (Martin Eree/Brne/Krase?), vas (Gradec/Griblje/Gumann Möttling?), hiša (19?), starost, starši. SAMO JSON: {"zapSt": "3", "datum": "", "zenin": "", "vas": "", "hisa": "", "starost": "", "stars": ""}'],
    ['s36-r4-L', 'Vrstica 4 strani s36 LEVI pol — ženin (Mathias Brine/Braune?), vas GRIBLJE?, hiša (24?), starost, stan (bauernsohn?), starši. SAMO JSON: {"zapSt": "4", "datum": "", "zenin": "", "vas": "", "hisa": "", "starost": "", "stan": "", "stars": ""}'],
    ['s36-vascol-2.5x', 'STOLPEC vas/hiša strani s36 (vseh ~6-8 vrstic) 2.5× — prepiši za vsako vrstico: vas + hišno št. (išči GRIBLJE!). SAMO JSON: {"rows": [{"vas": "", "hisa": ""}]}'],
    ['s37-r6-L', 'Vrstica 14 strani s37 (4. Juli 1880) LEVI pol — ženin: priimek (Križan Miklavčič? Bričan?), vas GRIBLJE?, hiša (63?), starost, stan, starši. SAMO JSON: {"zapSt": "14", "datum": "", "zenin": "", "vas": "", "hisa": "", "starost": "", "stars": ""}'],
    ['s37-r6-R', 'Vrstica 14 strani s37 DESNI pol — nevesta (Konstantia/Magdalena Pegdirec/Pezdirc?), vas/hiša (Podgorica? Griblje?), priče, duhovnik. SAMO JSON: {"nevesta": "", "vas": "", "hisa": "", "price": "", "duhovnik": ""}'],
    ['s38-r6-L', 'Vrstica 20 strani s38 (Nov 1880) LEVI pol — ženin: ime/priimek (Peter Pegdirec/Perdivec?), vas GRIBLJE?, hiša (53? 58?), starost, stan, starši, margine. SAMO JSON: {"zapSt": "20", "datum": "", "zenin": "", "vas": "", "hisa": "", "starost": "", "stars": "", "margine": ""}'],
    ['s38-r6-R', 'Vrstica 20 strani s38 DESNI pol — nevesta: ime (Anna Zupančič? Maria Brine? Zarasinič?), vas (Krasinec 18?), priče, duhovnik, margine (Väterliche Einwilligung?). SAMO JSON: {"nevesta": "", "vas": "", "hisa": "", "price": "", "duhovnik": "", "margine": ""}'],
    ['s38-dno-fini', 'DNO strani s38 (tail 1880) — prepiši vsoto/oznako (npr. s 1880 fini; rezane vsote m21 n1). SAMO JSON: {"reading": "", "sums": [...]}'],
    ['s38-kotovi', '4 kota strani s38 + kot s39 (primerjava) — PAG oznake. SAMO JSON: {"TL": "", "TR": "", "BL": "", "BR": "", "s39TR": ""}'],
  ];
  const results = {};
  for (const [file, ask] of jobs) {
    console.error(`--- ${file}`);
    try {
      const b64 = fs.readFileSync(`${CROPS}/${file}.jpg`).toString('base64');
      const call = zai.chat.completions.createVision({
        messages: [{ role: 'user', content: [
          { type: 'text', text: `${ask} Kurrent pisava ~1879-1880, poročna knjiga 04455 Podzemelj. Negotovo=[~], neberljivo=[?].` },
          { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${b64}` } }
        ]}],
        thinking: { type: 'disabled' }
      });
      const completion = await Promise.race([call, new Promise((_, rej) => setTimeout(() => rej(new Error('TIMEOUT 150s')), 150000))]);
      const j = extractJson(completion.choices[0]?.message?.content);
      results[file] = j;
      fs.writeFileSync(`${OUT}/${file}.json`, JSON.stringify(j, null, 2));
      console.log(`${file}: ${JSON.stringify(j).slice(0, 350)}`);
    } catch (e) { console.error(`${file} FAIL: ${e.message}`); results[file] = { fail: e.message }; }
  }
  fs.writeFileSync('/tmp/p243/pass6/ALL.json', JSON.stringify(results, null, 2));
  console.log('PASS6 DONE');
}
main().catch(e => { console.error(e); process.exit(1); });
