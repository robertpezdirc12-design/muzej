// P168 — forenzično branje kompozitov (max-zoom verifikacija).
// Izhod: /tmp/p168/forensic/vlm-KOMPOZIT-*.json
// Uporaba: node scripts/tmp/p168_forensic.mjs [filter]
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';
import path from 'path';

const F = '/tmp/p168/forensic';
const OUT = F;

const KOMPOZITI = [
  'KOMPOZIT-griblje-A.png', 'KOMPOZIT-griblje-B.png', 'KOMPOZIT-griblje-C.png',
  'KOMPOZIT-meja-1902-03.png', 'KOMPOZIT-vas-hisna-A.png', 'KOMPOZIT-vas-hisna-B.png',
  'KOMPOZIT-ime-starost.png', 'KOMPOZIT-podpisi.png', 'KOMPOZIT-zapcol.png',
];

function promptFor(name) {
  if (name.includes('griblje')) {
    return `Te so PANCIRANI izrezi (trakovi ×2.2) vrstic MRLIŠKE matične knjige župnije Podzemelj, leto 1902, Kurrent pisava. Vsak PANEL = 1 celotna vrstica (zaporedna št. | mesec+dni | vas+hišna št. | ime+priimek+stan | starost | bolezen | podpis duhovnika).

NALOGA: Za VSAK PANEL prepiši vsa polja z maksimalno natančnostjo. Še posebej:
- VAS (3. stolpec: 'mesto, trg ali vas') — ali je 'Griblje' ali druga vas (Krasinec, Gradac, Otok, Giriče, Cerkviše, Klošter, Primostek, Dobravice, Podzemelj, Hrnelj, Grm, Grem, Boršt, Vranoviče, Begunja vas, Boginja vas, Krivoglave, Prilozje, Zemelj, Malše ...)? Ne ugibaj 'Griblje' — preveri črke (G-r-i-b-l-j-e)!
- HIŠNA ŠTEVILKA (ozek stolpec ob vasi) — Kurrent cifre: 3/5/8 zmeda (5 = zgornja ravna črta, 8 = dvojna zanka), 7 = γ-forma s prečko, 4 = zanka, 9 = zaprta zgornja zanka, 1 = ozka črtica!
- STAROST (številka + enota)
- BOLEZEN (npr. Jetika, Božjast, Slabost, Harost, Nadluha, Nadruha, Pljučnica, Sušica, Mrzlica, Griža, Gliste, Krastelj, Marbmil, Habost, Davica, Mertvod, Vodenica)
- DUHOVNIK (Jos. Rauq / Stanislav Dostal / Jos. Perz / J.R. Kut'nek ...)
- Negotovo z [~], neberljivo z [?].
Izhod: SAMO JSON: {"paneli":[{"panel":1,"id":"iz oznake PANEL-N: ...","zap":"...","mesec":"...","smrt":"...","pokop":"...","vas":"...","hisna":"...","ime":"...","stan":"...","starost":"...","bolezen":"...","previden":"...","duhovnik":"...","opomba":"..."}]}`;
  }
  if (name.includes('meja')) {
    return `Te so PANCIRANI izrezi (×2.2) iz MRLIŠKE matične knjige župnije Podzemelj, konec leta 1902 in meja 1902/03. PANEL-1 = zadnja vrstica 1902 (zap 61), PANEL-2 = MEJA: prazna vrsta z VELIKO letnico '1903' (+ podčrtaj?), PANEL-3 = prva vrstica 1903 (zap 1, Januarj), PANEL-4 = re-potrditev meje 1901/02 iz s85 ('1902.' z podčrtajem).

NALOGA: Za VSAK PANEL prepiši vse vidno: letnico (VELIKA cifre!), ali je podčrtana (enojno/dvojno/večkratno!), mesec ('Januarj'?), zap številko, vas, hišno št., ime, starost, bolezen, duhovnika. Negotovo z [~].
Izhod: SAMO JSON: {"paneli":[{"panel":1,"id":"...","letnica":"...","podcrtaj":"brez/enojen/dvojen/vecikrat","zap":"...","mesec":"...","smrt":"...","pokop":"...","vas":"...","hisna":"...","ime":"...","starost":"...","bolezen":"...","duhovnik":"..."}]}`;
  }
  if (name.includes('vas-hisna')) {
    return `Te so PANCIRANE celice ×3.0 (stolpec 'Bivališče mrličevo': vas + hišna št.) iz mrliške knjige Podzemelj 1902. Vsak PANEL = 1 vrstica.

NALOGA: Za vsak PANEL preberi VAS (ali 'Griblje'? — preveri črke G-r-i-b-l-j-e; alternativе: Krasinec, Gradac, Otok, Giriče, Cerkviše, Primostek, Dobravice, Podzemelj, Hrnelj, Grm, Grem, Klošter, Vranoviče, Malše, Boršt, Zemelj, Krivoglave, Boginja vas ...) in HIŠNO ŠT. (Kurrent: 3/5/8 zmeda — 5 zgornja ravna črta, 8 dvojna zanka; 7 = γ s prečko; 4 = zanka; 9 zaprta zanka; 1 črtica; 2 = z-lanka odprta; 6 = spodnja zanka). Negotovo z [~].
Izhod: SAMO JSON: {"paneli":[{"panel":1,"id":"...","vas":"...","hisna":"...","opomba":"..."}]}`;
  }
  if (name.includes('ime-starost')) {
    return `Te so PANCIRANE celice ×3.0 iz mrliške knjige Podzemelj 1902: stolpec 'Ime, priimek in stan mrličev' (PANEL-1..6/7) in 'Starost' (PANEL-7/8..14). 

NALOGA: Za IME-panele: prepiši ime, priimek, stan (npr. 'vdovec', 'sijmen [~] 1/2 zemljakov sin', 'omrjena [~] ...'). Posebej pozoren na priimke podobne: BRINEC / PRINEC / BRUNEZ / PEZDIREC / BENDIREC / BEDIREC / MILEK / MKEK / DEHLIČ! Za STAROST-panele: cifre + enota (let/leto/leta, mesecev, dni, tednov, uri; Kurrent γ = 7!). Negotovo z [~].
Izhod: SAMO JSON: {"paneli":[{"panel":1,"id":"...","tip":"ime|starost","vsebina":"..."}]}`;
  }
  if (name.includes('podpisi')) {
    return `Te so PANCIRANE celice ×3.0 (Podpis duhovna pokopovalca) iz mrliške knjige Podzemelj 1902. PANEL-1..4 = domnevni 'Dostal' podpisi (različice: Hanš./Hemislav/Hemislav/Stanislav/Haniel Dostal), PANEL-5..6 = 'Jos. Rauq' reference.

NALOGA: Za vsak panel prepiši PODPIS čim bolj natančno (ime + priimek). Ali se glasi 'Stanislav Dostal', 'Hanš. Dostal', 'Hemislav Dostal', 'Haniel Dostal' ali kaj drugega? PRIMERJAJ forme med paneli — isti rokopis ali različna? Negotovo z [~].
Izhod: SAMO JSON: {"paneli":[{"panel":1,"id":"...","podpis":"...","primerjava":"..."}]}`;
  }
  return `Te so PANCIRANE rezine (×2.5) zaporedna-številka stolpca mrliške knjige Podzemelj 1902 (s85-dno: 10 vrstic po meji; s86 začetek; s88/s89/s90 spot-checks).

NALOGA: Za vsak PANEL preberi CIFRO/VSE cifre v stolpcu. Kurrent: γ-zanka = 7, 4 = zanka, 9 = zaprta zgornja zanka, 5 = zgornja ravna črta, 8 = dvojna zanka, 1 = črtica, 6 = spodnja zanka. PANEL-5 je znana pisarjeva napaka '345' (preveri — so to tri cifre 3-4-5 zapored?). Negotovo z [~].
Izhod: SAMO JSON: {"paneli":[{"panel":1,"id":"...","cifra":"...","opomba":"..."}]}`;
}

function parseContent(content) {
  const t = content.trim().replace(/^```(json)?/i, '').replace(/```$/, '').trim();
  const a = t.indexOf('{');
  const b = t.lastIndexOf('}');
  if (a < 0 || b < 0) throw new Error('ni JSON v odgovoru');
  const raw = t.slice(a, b + 1);
  // sanitizacija kontrolnih znakov znotraj nizov (VLM-včasih-vstavi newline)
  const safe = raw.replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/g, ' ');
  try {
    return JSON.parse(safe);
  } catch (e) {
    // drugi poskus: zamenjaj dobesedne nove vrstice znotraj nizov
    const fixed = safe.replace(/:\s*\n\s*"/g, ': "').replace(/"(\w+)":\s*"([^"]*)\n([^"]*)"/g, '"$1": "$2 $3"');
    return JSON.parse(fixed);
  }
}

async function readKomp(zai, img, name) {
  const b64 = fs.readFileSync(img).toString('base64');
  const make = () => zai.chat.completions.createVision({
    messages: [{ role: 'user', content: [
      { type: 'text', text: promptFor(name) },
      { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${b64}` } }
    ]}],
    thinking: { type: 'disabled' }
  });
  let completion;
  for (let attempt = 1; attempt <= 5; attempt++) {
    completion = await Promise.race([
      make(),
      new Promise((_, rej) => setTimeout(() => rej(new Error('TIMEOUT 240s')), 240000))
    ]).catch(e => {
      if (attempt < 5) {
        console.log(`  ${name}: poskus ${attempt}/5 (${e.message})`);
        return new Promise(res => setTimeout(() => res(null), attempt * 15000));
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
  const files = KOMPOZITI.filter(f => f.includes(filter));
  const zai = await ZAI.create();
  for (const f of files) {
    const out = path.join(OUT, `vlm-${f.replace('.png', '.json')}`);
    if (fs.existsSync(out)) { console.log(`${f}: že obstaja`); continue; }
    try {
      const r = await readKomp(zai, path.join(F, f), f);
      fs.writeFileSync(out, JSON.stringify(r, null, 1));
      console.log(`${f}: OK (${(r.paneli || []).length} panelov)`);
    } catch (e) {
      console.log(`${f}: FAIL ${e.message}`);
    }
  }
}

main().catch(e => { console.error(e); process.exit(1); });
