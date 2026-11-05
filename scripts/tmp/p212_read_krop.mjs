// P212 — generični KROP-reader (15 izrezov → JSON). Vzorec: PROMPTS-po-imenu, createVision,
// thinking-disabled, 4-retry, 180s-timeout. Izhod: /tmp/p212/krop-reads/<ime>.json
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';

const DIR = '/tmp/p212/krop-grib';
const OUT = '/tmp/p212/krop-reads';
fs.mkdirSync(OUT, { recursive: true });

const ROW = (z) => `To je vrstica ${z} skena mrliške matične knjige župnije Podzemelj (leto 1865, Kurrent pisava, nemški gotski vpliv).
Preberi natančno in odgovori SAMO z JSON:
{"zaporedna": "${z}", "mesec": "mesec smrti/pokopa", "smrt": "dan smrti", "pokop": "dan pokopa", "vas": "vas (Land und Wohnort)", "hisna": "hišna številka (Haus No. — pozor Kurrent 3/5/8, 7=γ-z-prečko, 4=z-zanko!)", "ime": "ime in priimek (beseda za besedo)", "stan": "stan/zakonski status +sluga (2. vrstica imenskega stolpca, npr. ½ Gütler, Inwohner, kind=otrok)", "starost": "število + enota (let/leta/mesecev/dni/tednov/uri — pozor ½!)", "todesart": "bolezen/vzrok smrti", "previden": "ali je prejel zakramente", "opomba": "kaj koli drugega opaznega"}`;

const PROMPTS = {
  arb_s46_glava: `To je SREDNJI del skena mrliške matične knjige župnije Podzemelj (Kurrent pisava). Vsebuje MEJO med letom 1864 (tail) in letom 1865 (restart).
Preveri: dvojna ločilna črta, VELIKA letnica čez vrsto, restart zaporedne številke na 1.
Odgovori SAMO z JSON:
{"velika_letnica": "kaj piše v veliki letnici (npr. '1865' ali '1|8|6|5' posamične cifre)", "cifre_posamicne": ["1","8","6","5"], "ali_dvojna_crta": true/false, "restart_potrjen": "ali se zaporedna številka restarta na 1?", "restart_vrsta1": {"mesec": "...", "smrt": "...", "pokop": "...", "vas": "...", "hisna": "...", "ime": "...", "stan": "...", "starost": "..."}, "naslednja_vrsta2": {"vas": "...", "hisna": "...", "ime": "..."}, "opomba": "..."}`,

  arb_s46_tail: `To je ZGORNJI del skena mrliške matične knjige župnije Podzemelj (Kurrent pisava) — TAIL leta 1864 (December).
PREŠEJ vrstice: koliko je popolnih vpisanih vrstic? (možnost: 4 vrstice z zaporednimi 88,89,90,91 ALI 7 vrstic z 85,86,87,88,89,90,91!)
Odgovori SAMO z JSON:
{"stevilo_vrstic": N, "zaporedne": ["..."], "vrstice": [{"zaporedna": "...", "mesec": "...", "smrt": "...", "pokop": "...", "vas": "...", "hisna": "...", "ime": "...", "starost": "..."}], "ali_precrtana": "ali je katera vrsta prečrtana/prazna?", "opomba": "..."}`,

  z74_s45_zap: `To je ZGORNJI del skena mrliške matične knjige župnije Podzemelj (Kurrent pisava). Vidne so PRVE 3 vrstice skena.
KLJUČNO: preberi ZAPOREDNE ŠTEVILKE v najbolj levem stolpcu — ali so 71,72,73 ALI 74,75,76? (Kurrent: 4 ima ZANKO, 1 je ozka črtica!)
Odgovori SAMO z JSON:
{"zaporedne": ["...","...","..."], "prva_vrsta": {"zaporedna": "...", "vas": "...", "hisna": "...", "ime": "..."}, "cifra_analiza": "zakaj 4-nebo-1: opisi oblik cifr", "opomba": "..."}`,

  z1_s46_grib: ROW(1) + ` TA VRSTICA je PRVI vpis leta 1865 (po MEJI) — vas naj bi bila GRIBLJE. Preveri hišno št. in ime posebej natačno!`,
  z8_s47_grib: ROW(8) + ` TA VRSTICA naj bi bila GRIBLJE — preveri vas, hišno št. (68?) in ime (Katarina Urik[~]?) natačno!`,
  z9_s47_grib: ROW(9) + ` TA VRSTICA naj bi bila GRIBLJE — preveri vas, hišno št. (23?) in ime (Anna Brinc?) natačno!`,
  z11_s47_grib: ROW(11) + ` TA VRSTICA naj bi bila GRIBLJE — preveri hišno št. (80?) in stan (Gablar?) natačno!`,
  z13_s47_grib: ROW(13) + ` TA VRSTICA naj bi bila GRIBLJE — ANOMALIJA: dan-smrti-18-vs-dan-pokopa-17 (pokop PRED smrtjo?!) — preveri OBE številki natačno! Prav tako ime (Anna Husič?) in hišno št. (37?)!`,
  z17_s47_grib: ROW(17) + ` TA VRSTICA naj bi bila GRIBLJE — preveri hišno št. (18?) in ime (Marija Muc?) natačno!`,
  z18_s47_grib: ROW(18) + ` TA VRSTICA naj bi bila GRIBLJE — preveri ime (Anna Husič-kind? otrok?) in hišno št. (37? — ISTA kot vrstica 13!) starost (2 mesece?) natačno!`,
  z24_s48_grib: ROW(24) + ` TA VRSTICA naj bi bila GRIBLJE — preveri hišno št. (70?) in ime (Nicolaus Ulrich?) natačno!`,
  z36_s49_grib: ROW(36) + ` TA VRSTICA naj bi bila GRIBLJE — preveri hišno št. (67?) in ime (Mathias Požek/Poček?) natačno!`,
  z50_s50_grib: ROW(50) + ` TA VRSTICA naj bi bila GRIBLJE — preveri hišno št. (32?) in ime (Michael Straus[~]?) starost (6 dni?) natačno!`,
  z63_s50_grib: ROW(63) + ` TA VRSTICA naj bi bila GRIBLJE — preveri vas (Grible?), hišno št. (19?) in ime (Anna Križe?) natačno!`,
  z20_s47_grib: ROW(20) + ` TA VRSTICA naj bi bila GRIBLJE — preveri hišno št. (28?) in ime (Jernej Brinc?) natačno!`,
  z8_s47_grib2: ROW(8) + ` TA VRSTICA naj bi bila GRIBLJE (prva vrstica pod glavo tabele) — preveri vas (Griblje?), hišno št. (68?) in ime (Katarina Urih?) natačno!`,
};

function parseContent(content) {
  const t = content.trim().replace(/^```(json)?/i, '').replace(/```$/, '').trim();
  const a = t.indexOf('{');
  const b = t.lastIndexOf('}');
  if (a < 0 || b < 0) throw new Error('ni JSON v odgovoru');
  return JSON.parse(t.slice(a, b + 1));
}

async function read(zai, name) {
  const b64 = fs.readFileSync(`${DIR}/${name}.png`).toString('base64');
  const make = () => zai.chat.completions.createVision({
    messages: [{ role: 'user', content: [
      { type: 'text', text: PROMPTS[name] },
      { type: 'image_url', image_url: { url: `data:image/png;base64,${b64}` } }
    ]}],
    thinking: { type: 'disabled' }
  });
  let completion;
  for (let attempt = 1; attempt <= 4; attempt++) {
    completion = await Promise.race([
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
  const inst = await ZAI.create();
  const names = process.argv.slice(2);
  const ALL = Object.keys(PROMPTS);
  for (const name of (names.length ? names : ALL)) {
    const out = `${OUT}/${name}.json`;
    if (fs.existsSync(out)) { console.log(`${name}: ŽE`); continue; }
    if (!fs.existsSync(`${DIR}/${name}.png`)) { console.error(`${name}: manjka PNG`); continue; }
    try {
      const res = await read(inst, name);
      fs.writeFileSync(out, JSON.stringify(res, null, 2));
      console.log(`${name}: OK`);
    } catch (e) {
      console.error(`${name}: FAIL ${e.message}`);
    }
  }
}
main().catch(e => { console.error(e); process.exit(1); });
