// P167 — forenzično branje kompozitov (max-zoom potrditve/popravki).
// 6 kompozitov × 1 VLM klic. Izhod: /tmp/p167/forensic/<ime>.json
// Uporaba: node scripts/tmp/p167_forensic.mjs [filter]
// NASVET (P158-lekcija): FOREGROUND v serijah po ≤2!
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';
import path from 'path';

const F = '/tmp/p167/forensic';
fs.mkdirSync(F, { recursive: true });

const TASKS = [
  {
    name: 'kompozit-meja-1901-02',
    q: `Forenzični kompozit mejnih izrezov mrliške matične knjige Podzemelj (Kurrent pisava). 3 PANELI (rdeča obroba + oznaka pod izrezom):
PANEL-1 = zadnja vrstica leta 1901 (zaporedna 55)
PANEL-2 = PRAZNA vrstica z VELIKO PODČRTANO letnico '1902.' (meja 1901/02)
PANEL-3 = prva vrstica leta 1902 (zaporedna 1)
Za vsak panel prepiši: zaporedno št., mesec/dan smrti, dan pokopa, vas, hišno št., ime+priimek+stan, starost, bolezen/vzrok, previden, podpis duhovnika, opombe. Posebej natačno: letnica v PANEL-2 (ali je '1902.' + podčrtaj?), mesec-vrstica pod markerjem, Kurrent cifre (γ-zanka=7, ±=4, zaprta-zanka=9, 5/6 zmeda!). Izhod SAMO JSON:
{"panel1": {"zap": "...", "vsebina": "..."}, "panel2": {"letnica": "...", "podcrtaj": "da/ne", "opis": "..."}, "panel3": {"zap": "...", "vsebina": "..."}, "sklep": "..."}`
  },
  {
    name: 'kompozit-griblje-A',
    q: `Forenzični kompozit 5 izrezov (trakovi ×2.2, celotne vrstice) MRLIŠKE matične knjige Podzemelj, leto 1901 (Kurrent pisava). PANELI (oznake pod izrezi):
PANEL-1 = griblje-zap1-ana-krizan-80dno (hišna ~36)
PANEL-2 = griblje-zap4-matija-hlobucar-80dno (hišna ~48 — HLOBUČAR-×2-v-2-MESECIH!)
PANEL-3 = griblje-zap7-anton-stolfa-81 (hišna ~60)
PANEL-4 = griblje-zap11-marija-brinec-81 (hišna ~28)
PANEL-5 = griblje-zap13-marija-cindric-81 (hišna ~81)
Za vsak panel prepiši NATAČNO: zaporedna št. (Kurrent: 7=γ-forma!, 4=±-zanka, 9=zaprta-zanka!), mesec+dan smrti, dan pokopa, VAS (Griblje?), HIŠNA ŠT. (3/5/8-zmeda; 7=γ!), IME+PRIIMEK+STAN, STAROST (številka+enota), BOLEZEN, previden, duhovnik. Izhod SAMO JSON:
{"panel1": {"zap": "...", "vas": "...", "hisna": "...", "ime": "...", "stan": "...", "starost": "...", "bolezen": "...", "opomba": ""}, "panel2": {...}, "panel3": {...}, "panel4": {...}, "panel5": {...}, "sklep": "..."}`
  },
  {
    name: 'kompozit-griblje-B',
    q: `Forenzični kompozit 5 izrezov (trakovi ×2.2) MRLIŠKE matične knjige Podzemelj, leto 1901 (Kurrent pisava). PANELI:
PANEL-1 = griblje-zap15-ana-milek-81 (hišna ~29)
PANEL-2 = griblje-zap19-martin-papic-82 (hišna ~33)
PANEL-3 = griblje-zap50-janez-kesran-84 (hišna ~35 — ime: Kešran ali Križan?)
PANEL-4 = griblje-zap51-janez-jakobcic-84 (hišna ~64)
PANEL-5 = griblje-zap55-nikolaj-rampic-85 (hišna ~34 — ime: Rampič? zadnja vrstica 1901)
Za vsak panel prepiši NATAČNO: zaporedna št., mesec+dan smrti, dan pokopa, VAS, HIŠNA ŠT., IME+PRIIMEK+STAN, STAROST, BOLEZEN, previden, duhovnik, opomba. Izhod SAMO JSON:
{"panel1": {"zap": "...", "vas": "...", "hisna": "...", "ime": "...", "stan": "...", "starost": "...", "bolezen": "...", "opomba": ""}, "panel2": {...}, "panel3": {...}, "panel4": {...}, "panel5": {...}, "sklep": "..."}`
  },
  {
    name: 'kompozit-vas-hisna',
    q: `Forenzični kompozit 10 izrezov (vas + hišna št. celice ×3.0) mrliške Podzemelj 1901 (Kurrent). PANELI (2 stolpca):
PANEL-1 = s80-r1 (Griblje? ~36) | PANEL-2 = s80-r4 (Griblje? ~48)
PANEL-3 = s81-zap7 (Griblje? ~60) | PANEL-4 = s81-zap11 (Griblje? ~28)
PANEL-5 = s81-zap13 (Griblje? ~81) | PANEL-6 = s81-zap15 (Griblje? ~29)
PANEL-7 = s82-zap19 (Griblje? ~33) | PANEL-8 = s84-zap50 (Griblje? ~35)
PANEL-9 = s84-zap51 (Griblje? ~64) | PANEL-10 = s85-zap55 (Griblje? ~34)
Za vsak panel: VAS (Griblje/Drugo — prepiši točno!) + HIŠNA ŠT. (Kurrent: 3/5/8-zmeda — 5 = raven-vrh, 8 = dve zanki, 3 = odprta-zgoraj; 7 = γ-s-prečko; 2 = odprta-zgornja-zanka, 6 = zaprta-zgornja-zanka; 1 = črtica; 9/4!). Izhod SAMO JSON:
{"panel1": {"vas": "...", "hisna": "...", "gotovost": "..."}, ..., "panel10": {...}, "sklep": "..."}`
  },
  {
    name: 'kompozit-ime-starost',
    q: `Forenzični kompozit 11 izrezov (ime-celice + starost-celice ×3.0) mrliške Podzemelj 1901 (Kurrent). PANELI (2 stolpca):
PANEL-1 = s81-zap7-ime (Anton Štolfa?) | PANEL-2 = s81-zap13-ime (Marija Cindrič?)
PANEL-3 = s82-zap19-ime (Martin Papič?) | PANEL-4 = s84-zap50-ime (Janez Kešran/Križan?)
PANEL-5 = s84-zap51-ime (Janez Jakobčič?) | PANEL-6 = s85-zap55-ime (Nikolaj Rampič?)
PANEL-7 = s80-r1-starost (Ana Križan ~76 let?) | PANEL-8 = s80-r4-starost (Matija Hlobučar ~65 let?)
PANEL-9 = s84-zap50-starost (~63 let?) | PANEL-10 = s84-zap51-starost (~42 let?)
PANEL-11 = s85-zap55-starost (~19 let?)
Za ime-panele: IME+PRIIMEK+STAN (Kurrent-leksikon: Križan, Hlobučar, Štolfa, Cindrič, Milek, Papič, Kešran/Križan, Jakobčič, Rampič/Grampič...). Za starost-panele: ŠTEVILKA + ENOTA (Kurrent cifre: 7=γ!, 4=±, 9=zaprta-zanka, 5/6-zmeda; enote: let/leto/leta/mesecev/dni/tednov/uri). Izhod SAMO JSON:
{"panel1": {"ime": "...", "stan": "..."}, "panel7": {"starost": "...", "oblika": "..."}, ..., "sklep": "..."}`
  },
  {
    name: 'kompozit-podpisi',
    q: `Forenzični kompozit 6 izrezov (podpis duhovnika ×3.0) mrliške Podzemelj 1901 (Kurrent). PANELI:
PANEL-1 = s81-zap7-podpis | PANEL-2 = s81-zap11-podpis
PANEL-3 = s84-zap50-podpis | PANEL-4 = s85-zap55-podpis
PANEL-5 = s82-zap20-podpis-rauq (Jos. Rauq-referencna!) | PANEL-6 = s83-zap32-podpis
Prepoznaj PODPIS: kandidati = J.R. Kut'nek [~ Kutinek/Kub'nek — NOVI 1900+!], Jos. Rauq [~ Ramej/Romey], Fr. Škurmelj, Jos. Perz coop., Franc Češarek coop., Ivan Šašelj, Jan Jelen, Jož. Lamp. Izhod SAMO JSON:
{"panel1": {"podpis": "...", "identifikacija": "..."}, ..., "sklep": "..."}`
  },
];

function parseContent(content) {
  const t = content.trim().replace(/^```(json)?/i, '').replace(/```$/, '').trim();
  const a = t.indexOf('{');
  const b = t.lastIndexOf('}');
  if (a < 0 || b < 0) throw new Error('ni JSON v odgovoru');
  return JSON.parse(t.slice(a, b + 1));
}

async function readOne(zai, task) {
  const img = path.join(F, `${task.name}.png`);
  const b64 = fs.readFileSync(img).toString('base64');
  const make = () => zai.chat.completions.createVision({
    messages: [{ role: 'user', content: [
      { type: 'text', text: task.q },
      { type: 'image_url', image_url: { url: `data:image/png;base64,${b64}` } }
    ]}],
    thinking: { type: 'disabled' }
  });
  let completion;
  for (let attempt = 1; attempt <= 4; attempt++) {
    completion = await Promise.race([
      make(),
      new Promise((_, rej) => setTimeout(() => rej(new Error('TIMEOUT 200s')), 200000))
    ]).catch(e => {
      if (attempt < 4) {
        console.log(`  ${task.name}: poskus ${attempt}/4 (${e.message}) — čakam ${attempt * 12}s`);
        return new Promise(res => setTimeout(() => res(null), attempt * 12000));
      }
      throw e;
    });
    if (completion) break;
  }
  if (!completion) throw new Error('vsi poskusi izčrpani');
  return parseContent(completion.choices[0].message.content);
}

async function main() {
  const filter = process.argv[2] || '';
  const zai = await ZAI.create();
  let ok = 0, fail = 0;
  for (const t of TASKS.filter(t => t.name.includes(filter))) {
    const out = path.join(F, `${t.name}.json`);
    if (fs.existsSync(out)) { console.log(`${t.name}: že obstaja`); ok++; continue; }
    try {
      const r = await readOne(zai, t);
      fs.writeFileSync(out, JSON.stringify(r, null, 1));
      console.log(`${t.name}: OK`);
      ok++;
    } catch (e) {
      console.log(`${t.name}: FAIL ${e.message}`);
      fail++;
    }
  }
  console.log(`SKUPAJ: ${ok} OK / ${fail} FAIL`);
}

main().catch(e => { console.error(e); process.exit(1); });
