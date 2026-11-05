// P213 — generični KROP-reader (23 izrezov → JSON). Vzorec: PROMPTS-po-imenu, createVision,
// thinking-disabled, 4-retry, 180s-timeout. Izhod: /tmp/p213/krop-reads/<ime>.json
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';

const DIR = '/tmp/p213/krop-grib';
const OUT = '/tmp/p213/krop-reads';
fs.mkdirSync(OUT, { recursive: true });

const ZAP_PROMPT = `To je LEVI ROB (stolpec zaporednih številk) skena mrliške matične knjige župnije Podzemelj (Kurrent pisava).
Preberi VSAKO zaporedno številko od zgoraj navzdol. POZOR KURRENT CIFRE: 4 ima ZANKO; 1 je OZKA ČRTICA; 7 ima prečko (γ-forma — NE zamenjaj z 8!); 5 je lahko podobna 6; 3/5/8 zmeda; 0 je široka elipsa.
Odgovori SAMO z JSON: {"stevilke": ["...", ...], "opomba": "katera številka je negotova in zakaj"}`;

const ROW_PROMPT = `To je ena vrstica (ali del vrstice) mrliške matične knjige župnije Podzemelj (Kurrent pisava, nemški gotski vpliv).
Stolpci: mesec+dan smrti / dan pokopa | vas (npr. Griblje, Krasinec, Gradac, Podžemelj, Otok, Klošter/Kloster, Zemelj, Grem...) + hišna št. | ime, priimek, stan | vere/spola | starost (število + enota: J=let, M=mesecev, T=tednov, dni, uri) | bolezen/vzrok smrti | previden | podpis.
POZOR: Kurrent 3/5/8 zmeda; hišne številke: 4 ima zanko, 1 je ozka črtica, 7 = γ-forma s prečko! '½' = pol, '¼' = četrt (Gübler/Gütler = kmet-sosed; 'Kind' = otrok; 'Witwe' = vdova).
Preberi NATAČNO besedo za besedo; negotovo z [~], neberljivo z [?]. Odgovori SAMO z JSON:
{"zaporedna": "...", "mesec": "...", "smrt": "...", "pokop": "...", "vas": "...", "hisna": "...", "ime": "...", "stan": "...", "starost": "...", "bolezen": "...", "previden": "...", "duhovnik": "...", "opomba": "..."}`;

const PROMPTS = {
  s40_zap_top: ZAP_PROMPT,
  s40_zap_bot: ZAP_PROMPT,
  s41_zap_top: ZAP_PROMPT,
  s41_zap_bot: ZAP_PROMPT,
  s42_zap_top: ZAP_PROMPT,
  z89_s46_alter: `To je vrstica 89 mrliške matične knjige Podzemelj (Kurrent) — OTROK iz Gradaca. V stolpcu starosti naj bi bila KOREKCIJA-V-ZAPISU (prepis/prekrivanje).
Preberi natančno: {"zaporedna": "89", "mesec": "...", "smrt": "...", "pokop": "...", "vas": "...", "hisna": "...", "ime": "natančno ime+priimek+stan", "starost": "kaj točno piše v stolpcu Alter (vključno s korekcijo: kaj je bilo prvo, kaj je prepisano čez)", "bolezen": "...", "opomba": "opis morebitne korekcije/prekrivanja"}`,
  arb_s39_glava: `To je GLAVA skena mrliške matične knjige Podzemelj (Kurrent). V natisnjeno glavo je ročno vpisana LETNICA.
Odgovori SAMO z JSON: {"rokopisna_letnica": "natančno kaj je ročno vpisano (4 cifre)", "natisnjena_glava": "kaj piše natisnjeno", "opomba": "..."}`,
  arb_s40_glava: `To je GLAVA skena mrliške matične knjige Podzemelj (Kurrent). V natisnjeno glavo je ročno vpisana LETNICA.
Odgovori SAMO z JSON: {"rokopisna_letnica": "natančno kaj je ročno vpisano (4 cifre)", "natisnjena_glava": "kaj piše natisnjeno", "opomba": "..."}`,
  z18_hisa_s41: `To je STOLPEC hišnih številk (Haus No.) dveh sosednjih vrstic mrliške matične knjige Podzemelj (Kurrent). POZOR: Kurrent 4 ima ZANKO; 1 je OZKA ČRTICA brez zanke; 7 ima prečko!
Odgovori SAMO z JSON: {"zgornja_vrstica": "hišna št. (1-2 cifri)", "spodnja_vrstica": "hišna št. (1-2 cifri)", "druga_cifra_zgornje": "4-z-zanko ali 1-ozka-črtica?", "druga_cifra_spodnje": "4-z-zanko ali 1-ozka-črtica?", "opomba": "..."}`,
};

function parseContent(content) {
  const t = content.trim().replace(/^```(json)?/i, '').replace(/```$/, '').trim();
  const a = t.indexOf('{');
  const b = t.lastIndexOf('}');
  if (a < 0 || b < 0) throw new Error('ni JSON v odgovoru');
  return JSON.parse(t.slice(a, b + 1));
}

async function readKrop(zai, name) {
  const b64 = fs.readFileSync(`${DIR}/${name}.png`).toString('base64');
  const make = () => zai.chat.completions.createVision({
    messages: [{ role: 'user', content: [
      { type: 'text', text: PROMPTS[name] || ROW_PROMPT },
      { type: 'image_url', image_url: { url: `data:image/png;base64,${b64}` } }
    ]}],
    thinking: { type: 'disabled' }
  });
  for (let attempt = 1; attempt <= 4; attempt++) {
    const completion = await Promise.race([
      make(),
      new Promise((_, rej) => setTimeout(() => rej(new Error('timeout')), 180000))
    ]);
    try {
      const c = completion?.choices?.[0]?.message?.content;
      if (!c) throw new Error('prazna vsebina');
      return parseContent(c);
    } catch (e) {
      console.error(`  ${name}: poskus ${attempt} ni OK (${e.message})`);
      if (attempt === 4) throw e;
      await new Promise(r => setTimeout(r, 3000 * attempt));
    }
  }
}

async function main() {
  const FILTER = process.argv.slice(2);
  const names = fs.readdirSync(DIR).filter(f => f.endsWith('.png')).map(f => f.replace('.png', ''))
    .filter(n => FILTER.length === 0 || FILTER.includes(n)).sort();
  const inst = await ZAI.create();
  for (const name of names) {
    const out = `${OUT}/${name}.json`;
    if (fs.existsSync(out)) { console.log(`${name}: ŽE`); continue; }
    try {
      const res = await readKrop(inst, name);
      fs.writeFileSync(out, JSON.stringify(res, null, 2));
      console.log(`${name}: OK ${JSON.stringify(res).slice(0, 110)}`);
    } catch (e) {
      console.error(`${name}: FAIL ${e.message}`);
    }
  }
}
main().catch(e => { console.error(e); process.exit(1); });
