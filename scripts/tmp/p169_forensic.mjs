// P169 — forenzično branje kompozitov (max-zoom verifikacija).
// Izhod: /tmp/p169/forensic/vlm-KOMPOZIT-*.json
// Uporaba: node scripts/tmp/p169_forensic.mjs [filter]
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';
import path from 'path';

const F = '/tmp/p169/forensic';
const OUT = F;

const KOMPOZITI = [
  'KOMPOZIT-griblje-A.png', 'KOMPOZIT-griblje-B.png', 'KOMPOZIT-griblje-C.png',
  'KOMPOZIT-meja-1903-04.png', 'KOMPOZIT-glave-napake.png',
  'KOMPOZIT-vas-hisna-A.png', 'KOMPOZIT-vas-hisna-B.png',
  'KOMPOZIT-ime.png', 'KOMPOZIT-starost.png', 'KOMPOZIT-podpisi.png',
  'KOMPOZIT-zapcol.png',
  'KOMPOZIT2-starost-re.png', 'KOMPOZIT2-bolezen.png',
  'KOMPOZIT2-super-ime.png', 'KOMPOZIT2-super-hisna.png',
  'KOMPOZIT2-super-starost.png',
];

function promptFor(name) {
  if (name.includes('KOMPOZIT2-starost-re')) {
    return `Te so PANCIRANE celice ×3.0 (stolpec 'Starost', x-range 1530–1770 = PRAVILEN!) iz mrliške knjige Podzemelj 1903 — 17 Griblje-vpisov.

NALOGA: Za vsak panel preberi ŠTEVILKO + ENOTO (let/leto/leta, mesecev, tednov, dni, uri; Kurrent cifre: γ-zanka s prečko = 7!, 4 = zanka, 9 = zaprta zanka, 5 = ravna-zgoraj, 8 = dvojna-zanka, 1 = črtica, 6 = spodnja-zanka, 2 = z-lanka). Primeri: '5 mesecev' = cifra-5 + mesecov; '2 leta'; '33 let'; '10 mesecev'; '4 leta'; '1½ leta' = 1/2. Pozor: PRAZNO polje = ni vpisa! Negotovo z [~].
Izhod: SAMO JSON: {"paneli":[{"panel":1,"id":"...","starost":"...","enota":"...","opomba":"..."}]}`;
  }
  if (name.includes('KOMPOZIT2-bolezen')) {
    return `Te so PANCIRANE celice ×3.0 (stolpec 'Bolezen ali vzrok smrti', x-range 1755–2100 = PRAVILEN!) iz mrliške knjige Podzemelj 1903 — 17 Griblje-vpisov.

NALOGA: Za vsak panel preberi BOLEZEN/VZROK (npr. Jetika, Božjast, Slabost, Harost, Nadluha, Nadruha, Pljučnica, Sušica, Mrzlica, Griža, Gliste, Krastelj, Marbmil, Habost, Davica, Mertvod, Vodenica, Kap, Kašelj, Prehlajenje, Krivica ...). Kurrent: Š = karočki, Ž = kliko-zgoraj, J = dolga-podaljšana. Negotovo z [~].
Izhod: SAMO JSON: {"paneli":[{"panel":1,"id":"...","bolezen":"...","opomba":"..."}]}`;
  }
  if (name.includes('KOMPOZIT2-super')) {
    return `To so SUPER-ZOOM izrezi ×6.0 iz mrliške knjige Podzemelj 1903 (Kurrent pisava, maksimalno povečano). PANEL-ov: ime-priimek-stan (x 850–1450) ali HIŠNA ŠT. (x 430–700, ozek stolpec) ali STAROST (x 1530–1770).

NALOGA: Za vsak PANEL prepiši vse VIDNO cifro-po-cifro in črko-po-črko:
- HIŠNA ŠT.: Kurrent cifre: 3/5/8 zmeda (5 = zgornja ravna črta, 8 = dvojna zanka), 7 = γ s prečko, 4 = zanka, 9 = zaprta zanka, 1 = črtica, 2 = z-lanka, 6 = spodnja zanka! (npr. je to 42 ali 72? 83 ali 85 ali 33? 58 ali 38? 4 ali 7?)
- IME+PRIIMEK: ali 'Žegriva' / 'Zegina' / 'Zagriva'? ali 'Kukan' / 'Križan'? ali 'Špan' / 'Špavc' / 'Štravs'? ali 'Šimec' / 'Simenc'? ali 'Radovič' / 'Radlovič'? ali 'Dragar' / 'Dragaš'?
- STAROST: cifre + enota (pazi γ=7, 5 vs 6, 8 vs 9!)
Negotovo z [~], neberljivo z [?].
Izhod: SAMO JSON: {"paneli":[{"panel":1,"id":"...","vsebina":"...","cifre":"...","opomba":"..."}]}`;
  }
  if (name.includes('griblje')) {
    return `Te so PANCIRANI izrezi (trakovi ×2.2) vrstic MRLIŠKE matične knjige župnije Podzemelj, leto 1903, Kurrent pisava. Vsak PANEL = 1 celotna vrstica (zaporedna št. | mesec+dni | vas+hišna št. | ime+priimek+stan | starost | bolezen | podpis duhovnika).

NALOGA: Za VSAK PANEL prepiši vsa polja z maksimalno natančnostjo. Še posebej:
- VAS (3. stolpec: 'mesto, trg ali vas') — ali je 'Griblje' ali druga vas (Krasinec, Gradac, Otok, Giriče, Cerkviše, Klošter, Primostek, Dobravice, Podzemelj, Hrnelj, Grm, Grem, Boršt, Vranoviče, Begunja vas, Boginja vas, Krivoglave, Prilozje, Zemelj, Malše ...)? Ne ugibaj 'Griblje' — preveri črke (G-r-i-b-l-j-e)!
- HIŠNA ŠTEVILKA (ozek stolpec ob vasi) — Kurrent cifre: 3/5/8 zmeda (5 = zgornja ravna črta, 8 = dvojna zanka), 7 = γ-forma s prečko, 4 = zanka, 9 = zaprta zgornja zanka, 1 = ozka črtica!
- STAROST (številka + enota)
- BOLEZEN (npr. Jetika, Božjast, Slabost, Harost, Nadluha, Nadruha, Pljučnica, Sušica, Mrzlica, Griža, Gliste, Krastelj, Marbmil, Habost, Davica, Mertvod, Vodenica, Kap, Kašelj, Prehlajenje)
- DUHOVNIK (Jos. Rauq / Stanislav Dostal ...)
- Negotovo z [~], neberljivo z [?].
Izhod: SAMO JSON: {"paneli":[{"panel":1,"id":"iz oznake PANEL-N: ...","zap":"...","mesec":"...","smrt":"...","pokop":"...","vas":"...","hisna":"...","ime":"...","stan":"...","starost":"...","bolezen":"...","previden":"...","duhovnik":"...","opomba":"..."}]}`;
  }
  if (name.includes('meja')) {
    return `Te so PANCIRANI izrezi (×2.2) iz MRLIŠKE matične knjige župnije Podzemelj, konec leta 1903 in meja 1903/04. PANEL-1 = zadnja vrstica 1903 (zap 51, December, pokop 1 jan 04?), PANEL-2 = MEJA: prazna vrsta z VELIKO letnico '1904' (+ podčrtaj?), PANEL-3 = prva vrstica 1904 (zap 1, Januarj), PANEL-4 = re-potrditev meje 1902/03 iz s90 ('1903' z podčrtajem).

NALOGA: Za VSAK PANEL prepiši vse vidno: letnico (VELIKA cifre!), ali je podčrtana (enojno/dvojno/večkratno!), mesec ('Januarj'?), zap številko, vas, hišno št., ime, starost, bolezen, duhovnika. Negotovo z [~].
Izhod: SAMO JSON: {"paneli":[{"panel":1,"id":"...","letnica":"...","podcrtaj":"brez/enojen/dvojen/vecikrat","zap":"...","mesec":"...","smrt":"...","pokop":"...","vas":"...","hisna":"...","ime":"...","starost":"...","bolezen":"...","duhovnik":"..."}]}`;
  }
  if (name.includes('glave')) {
    return `Te so PANCIRANI izrezi GLAV ('Leto NNNN') mrliške knjige Podzemelj: PANEL-1 = s92 (napis naj bi bil 1903 — a videti '18903'?), PANEL-2 = s94 (napis naj bi bil 1903 — a videti '18903'?), PANEL-3 = s95 (napis naj bi bil 1904 — a videti '18 1904' z dvema letnicama?).

NALOGA: Za vsak PANEL prepiši GLAVO DOBESNO cifro-po-cifro. So tri cifre '1-8-9' pred '03'/'04'? Ali samo '1-9' + '03'? Posebej: PANEL-3 — sta tam DVE letnici ('18' + '1904') ali ena? To so pisarjeve napake-kandidati — potrebna pikselska potrditev! Negotovo z [~].
Izhod: SAMO JSON: {"paneli":[{"panel":1,"id":"...","glava-dobesedno":"...","cifre-ločeno":"...","napaka":"opis ali null"}]}`;
  }
  if (name.includes('vas-hisna')) {
    return `Te so PANCIRANE celice ×3.0 (stolpec 'Bivališče mrličevo': vas + hišna št.) iz mrliške knjige Podzemelj 1903. Vsak PANEL = 1 vrstica.

NALOGA: Za vsak PANEL preberi VAS (ali 'Griblje'? — preveri črke G-r-i-b-l-j-e; alternativе: Krasinec, Gradac, Otok, Giriče, Cerkviše, Primostek, Dobravice, Podzemelj, Hrnelj, Grm, Grem, Klošter, Vranoviče, Malše, Boršt, Zemelj, Krivoglave, Boginja vas ...) in HIŠNO ŠT. (Kurrent: 3/5/8 zmeda — 5 zgornja ravna črta, 8 dvojna zanka; 7 = γ s prečko; 4 = zanka; 9 zaprta zanka; 1 črtica; 2 = z-lanka odprta; 6 = spodnja zanka). Negotovo z [~].
Izhod: SAMO JSON: {"paneli":[{"panel":1,"id":"...","vas":"...","hisna":"...","opomba":"..."}]}`;
  }
  if (name.includes('ime')) {
    return `Te so PANCIRANE celice ×3.0 iz mrliške knjige Podzemelj 1903: stolpec 'Ime, priimek in stan mrličev'.

NALOGA: Za vsak panel prepiši ime, priimek, stan (npr. 'vdovec', 'oženjen ožilkar', '1/2 zemljakov sin', 'mrliška [~]'). Posebej pozoren na priimke podobne: ŽEGRIVA / ZAGRIVA / LEGIRCA / KUKAN / KRIZAN / PEČNIREC / PEZDIREC / ŠPAN / ŠTRAVS / DRAGAR / DRAGOŠ / PUČEK / POŽEK! Kurrent: Š ima karočke, Ž ima kliko-zgoraj. Negotovo z [~].
Izhod: SAMO JSON: {"paneli":[{"panel":1,"id":"...","ime":"...","priimek":"...","stan":"...","opomba":"..."}]}`;
  }
  if (name.includes('starost')) {
    return `Te so PANCIRANE celice ×3.0 (stolpec 'Starost') iz mrliške knjige Podzemelj 1903.

NALOGA: Za vsak panel preberi ŠTEVILKO + ENOTO (let/leto/leta, mesecev, tednov, dni, uri; Kurrent cifre: γ-zanka s prečko = 7!, 4 = zanka, 9 = zaprta zanka, 5 = ravna-zgoraj, 8 = dvojna-zanka, 1 = črtica, 6 = spodnja-zanka, 2 = z-lanka). Pozor: '5 mesecev' vs '15 let'? '2 leta' vs '72 let'? '54' vs '34'? '64' vs '84'? Negotovo z [~].
Izhod: SAMO JSON: {"paneli":[{"panel":1,"id":"...","starost":"...","enota":"...","opomba":"..."}]}`;
  }
  if (name.includes('podpisi')) {
    return `Te so PANCIRANE celice ×3.0 (Podpis duhovna pokopovalca) iz mrliške knjige Podzemelj 1903. PANEL-1, 5 = domnevni 'Dostal' podpisi, PANEL-2, 4 = 'Jos. Rauq' reference, PANEL-3 = s94-zap44 PRAZNO/ČRTICA?, PANEL-6, 7 = s95-kontekst (Griblje/Giriče zmeda).

NALOGA: Za vsak panel prepiši PODPIS čim bolj natančno (ime + priimek). PANEL-1, 5: ali 'Stanislav Dostal'? PANEL-2, 4: ali 'Jos. Rauq'? PANEL-3: je podpis res PRAZEN (samo črtica —)? PANEL-6, 7: preberi VAS + ime (Griblje ali Giriče/Grisže?). PRIMERJAJ forme med paneli — isti rokopis ali različna? Negotovo z [~].
Izhod: SAMO JSON: {"paneli":[{"panel":1,"id":"...","podpis":"...","primerjava":"..."}]}`;
  }
  return `Te so PANCIRANE rezine (×2.5) zaporedna-številka stolpca mrliške knjige Podzemelj 1903 (s90-dno: restart 1903 zap1–7; s91–s94 spot-checks; s94-r1 = restart 1904!).

NALOGA: Za vsak PANEL preberi CIFRO/VSE cifre v stolpcu. Kurrent: γ-zanka = 7, 4 = zanka, 9 = zaprta zgornja zanka, 5 = zgornja ravna črta, 8 = dvojna zanka, 1 = črtica, 6 = spodnja zanka. PANEL-7 (s94-r1) je RESTART-1904 = mora biti '1'! PANEL-1–2 = 1903-restart-kontrola ('1' in '7'). Negotovo z [~].
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
