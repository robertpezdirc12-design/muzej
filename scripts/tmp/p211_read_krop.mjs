// P211 — generični KROP-reader (7 izrezov → JSON). Vzorec: PROMPTS-po-imenu, createVision,
// thinking-disabled, 4-retry, 180s-timeout. Izhod: /tmp/p211/krop-reads/<ime>.json
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';

const DIR = '/tmp/p211/krop-grib';
const OUT = '/tmp/p211/krop-reads';
fs.mkdirSync(OUT, { recursive: true });

const PROMPTS = {
  arb_s51_glava: `To je zgornji del skena mrliške matične knjige župnije Podzemelj (Kurrent pisava, nemški gotski vpliv). Vsebuje GLAVO leta 1866 (restart vpisov) in TAIL leta 1865.
Preberi in odgovori SAMO z JSON:
{"velika_letnica": "kaj piše v veliki letnici-glavi (npr. '1866 Jänner')", "leta_v_poti": "vse letnice vidne v stolpcu des Todes/des Begräbnis",
"tail_vrstice": [{"zaporedna": "65", "mesec": "...", "smrt": "...", "pokop": "...", "vas": "...", "hisna": "...", "ime": "...", "stan": "...", "starost": "..."}],
"precrtana_vrsta": "opis prečrtane/prazne vrste (Schlangenlinien) ali null",
"restart_vrsta1": {"zaporedna": "1", "mesec": "...", "smrt": "...", "pokop": "...", "vas": "...", "hisna": "...", "ime": "...", "stan": "..."},
"opomba": "..."}`,

  z58_s56_mesec: `To je zadnja vrstica skena mrliške matične knjige (Podzemelj, Kurrent pisava). Vidna sta mesec-pokopa in del vrstice.
Preberi in odgovori SAMO z JSON:
{"mesec_pokop": "natančno kaj piše v levem stolpcu (mesec + številka)", "vas": "vas", "hisna": "hišna št.", "ime": "ime in stan", "ali_juli": "true če mesec piše 'Juli'", "opomba": "..."}`,

  z34z35_s55_anomalija: `To sta prvi dve vrstici skena mrliške matične knjige (Podzemelj, Kurrent pisava).
Preberi in odgovori SAMO z JSON:
{"v34": {"mesec": "...", "smrt": "...", "pokop": "...", "vas": "...", "hisna": "...", "ime": "natančno besedilo", "starost": "...", "todesart": "..."}, "v35": {...}, "ali_totgeborenes": "kaj točno piše v imenu (beseda za besedo)", "oc_jezika": "ali je 'Totgeborenes Kind'? Kdo je starš (v. ...)?", "opomba": "..."}`,

  z90_s59_anomalia: `To je vrstica 90 skena mrliške matične knjige (Podzemelj, Kurrent pisava) z ANOMALIJO — v stolpcu imena naj bi bila več besed/oseb.
Preberi in odgovori SAMO z JSON:
{"zaporedna": "90", "mesec": "...", "smrt": "...", "pokop": "...", "vas": "...", "hisna": "natančno hišna št.", "ime": "VSA besedila v stolpcu imena (vrstica za vrstico)", "starost": "...", "todesart": "...", "koliko_oseb": "koliko imen/oseb je zapisanih v eni vrstici?", "opomba": "..."}`,

  z41_s55_h14: `To je vrstica 41 skena mrliške matične knjige (Podzemelj, Kurrent pisava).
Preberi in odgovori SAMO z JSON:
{"zaporedna": "41", "smrt": "...", "pokop": "...", "vas": "...", "hisna": "...", "ime": "...", "stan": "besedilo v 2. vrstici imenskega stolpca", "starost": "natančno število+enota iz stolpca Alter (pozor: ½ = pol, 'jährig' = star)", "todesart": "...", "opomba": "..."}`,

  z22_s53_ime: `To je vrstica 22 skena mrliške matične knjige (Podzemelj, Kurrent pisava). Priimek se začne na K ali H (Kurrent K-brez-descenderja).
Preberi in odgovori SAMO z JSON:
{"zaporedna": "22", "ime": "natančno ime in priimek", "priimek_zacetnica": "K ali H?", "priimek_kandidati": ["Kusić", "Hušić", "Novak", ...], "starost": "...", "stan": "...", "opomba": "..."}`,

  z22_s53_hisa: `To je del vrstice 22 mrliške matične knjige (Podzemelj) s stolpcema Land und Wohnort (vas) in Haus No. (hišna številka).
Preberi in odgovori SAMO z JSON:
{"vas": "natančno vas", "hisna": "natančno hišna številka (pozor Kurrent: 4 ima zanko, 1 je ozka črtica, 7 ima prečko)", "hisna_alternativa": "druga možnost ali null", "opomba": "..."}`
};

function parseContent(content) {
  const t = content.trim().replace(/^```(json)?/i, '').replace(/```$/, '').trim();
  const a = t.indexOf('{'); const b = t.lastIndexOf('}');
  if (a < 0 || b < 0) throw new Error('ni JSON v odgovoru');
  return JSON.parse(t.slice(a, b + 1));
}

async function readKrop(zai, name) {
  const b64 = fs.readFileSync(`${DIR}/${name}.png`).toString('base64');
  const make = () => zai.chat.completions.createVision({
    messages: [{ role: 'user', content: [
      { type: 'text', text: PROMPTS[name] },
      { type: 'image_url', image_url: { url: `data:image/png;base64,${b64}` } }
    ]}],
    thinking: { type: 'disabled' }
  });
  for (let attempt = 1; attempt <= 4; attempt++) {
    try {
      const completion = await Promise.race([
        make(),
        new Promise((_, rej) => setTimeout(() => rej(new Error('timeout')), 180000))
      ]);
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
  for (const name of Object.keys(PROMPTS)) {
    const out = `${OUT}/${name}.json`;
    if (fs.existsSync(out)) { console.log(`${name}: ŽE`); continue; }
    try {
      const res = await readKrop(inst, name);
      fs.writeFileSync(out, JSON.stringify(res, null, 2));
      console.log(`${name}: OK → ${JSON.stringify(res).slice(0, 150)}`);
    } catch (e) {
      console.error(`${name}: FAIL ${e.message}`);
    }
  }
}
main().catch(e => { console.error(e); process.exit(1); });
