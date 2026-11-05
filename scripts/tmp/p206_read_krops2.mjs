// P206 — fokusirano VLM branje kropov (11-Griblje + 7-probe, leto 1871!)
// Izhod: /tmp/p206/krop-grib/JSON (paralen file: <ime>.json)
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';

const DIR = '/tmp/p206/krop2';
const FILTER = process.argv.slice(2);

const CROPS = fs.readdirSync(DIR).filter(f => f.endsWith('.png') && !f.endsWith('.json'))
  .filter(f => FILTER.length === 0 || FILTER.some(x => f.includes(x)));

function promptFor(name) {
  if (name.startsWith('probe')) {
    return `To je IZREZ (probe) iz MRLIŠKE matične knjige župnije Podzemelj (leto-kontekst: konec-1870/začetek-1871 ali konec-1871/začetek-1872!), slovenska Kurrent pisava. IZREZ je FORENZIČEN — vsebuje GLAVO/MEJO/vrstice z ordinali.

NALOGA — odporedi:
1) Zaporedne-številke-vrstic (levo-ozki-stolpec!) — prepiši VSE vidne, po-vrsti od-zgoraj!
2) Mesečne-glave / letnične-glave (npr. 'Jänner.', '1871.', 'December 1873', 'vsota') — prepiši DOLOVNO z letnico!
3) Če je vidna vsotna-vrsta ('vsota', 'Summa', dvodelna-številka-kot-'1 | 8') — prepiši!
4) Hišne-številke + imena v vrsticah — kratko!
5) Če vidimo RESTART ordinalov na 1 ali prazno-vrstico ali prečrtano-vrsto — to POSEBEJ povej!

KURRENT-ŠTEVKE: 1=ozka-črtica, 3=dve-zanki, 4=zanka-levo-zgoraj, 5=spodnja-zanka, 7=γ-s-prečko, 8=dve-zanki, 9=zgoraj-zanka. Ordinala-18/19/31/38 zmeda-pogosta!

Izhod: SAMO en veljaven JSON (brez markdown):
{"krop": "${name}", "ordinali": ["..."], "glave": ["..."], "vsota": "opis-ali-null", "vrstice": [{"ordinala": "1", "vas": "...", "hisna": "...", "ime": "...", "mesec": "...", "starost": "..."}], "restart": "opis-ali-null", "opomba": "..."}`;
  }
  return `To je IZREZ iz MRLIŠKE matične knjige župnije Podzemelj (leto 1871!), slovenska Kurrent pisava. Izrez vsebuje CENTRALNO VRSTICO (Griblje-vpis!) + kontekst (sosednji vrstici zgoraj/spodaj).

Cilj: NATAČNO prepiši CENTRALNO VRSTICO (tisto z vaso "Griblje" ali "Grible" v stolpcu "Land und Wohnort"!). Sosednje vrstice PREDSTAVI samo kot kontekst.

Stolpci (levo → desno): zaporedna-št. | dan smrti + dan pokopa (mesec nad njima ali v celici!) | Land und Wohnort (vas!) | Haus No. (hišna številka!) | Name und Stand des Verstorbenen (ime + stan!) | Vere/Spol kljukice | Alter (starost!) | Krankheit (bolezen!) | Versehen | duhovnik-podpis | Anmerkung.

KURRENT-ŠTEVKE: 1=ozka črtica, 3=dve zanki desno, 4=zanka levo-zgoraj, 5=spodnja zanka, 7=γ-forma s prečko!, 8=dve zanki, 9=zgoraj-zanka, 0=velik oval.
POSEBEJ pri HIŠNI ŠTEVILKI: 3/5/8 zmeda pogosta! 7 = γ-s-prečko! 9-vs-7 pogosta zmeda! Primerjaj z drugimi številkami v isti vrstici!

PRAVILA:
- Vas mora biti "Griblje/Grible" — če centralna vrstica NIMA vasi Griblje, to jasno povej (opomba: 'ni-Griblje').
- Hišna številka: prepiši z [~] če negotovo; če 2 cifri, obe! (npr. "65 [~ 66?]")
- Mesec: če je zapisan nad datumi (npr. "Februar" nad "31.") ali v celici (npr. "1871. Jüni 14."), to zapiši v mesec-polje!
- Starost: številka + ENOTA (let/leta/mes/Tednov/dni/uri/st.) — frakcije: ½ ¼ ¾!
- Bolezen: nemški izraz + slovenski [~].
- Duhovnik: prepiši podpis (npr. "Heschl Coop.", "Kogej Pfr.", "Vogrinc", "Bobek C.r.p.").
- Izjeme: prečrtano-besedilo, vijolična-poznejša-tinta, marginalne-številke → opomba!
- Izhod: SAMO en veljaven JSON (brez markdown):
{"krop": "${name}", "centralna_vas": "Griblje", "hisna": "65", "ime": "...", "stan": "...", "mesec": "Jänner", "smrt": "8.", "pokop": "10.", "starost": "54 let", "bolezen": "...", "duhovnik": "...", "opomba": null, "kontekst": "zgornja: ...; spodnja: ..."}`;
}

function parseContent(content) {
  const t = content.trim().replace(/^```(json)?/i, '').replace(/```$/, '').trim();
  const a = t.indexOf('{'); const b = t.lastIndexOf('}');
  if (a < 0 || b < 0) throw new Error('ni JSON');
  return JSON.parse(t.slice(a, b + 1));
}

async function main() {
  const inst = await ZAI.create();
  for (const f of CROPS) {
    const out = `${DIR}/${f.replace('.png', '.json')}`;
    if (fs.existsSync(out)) { console.log(`${f}: ŽE`); continue; }
    const b64 = fs.readFileSync(`${DIR}/${f}`).toString('base64');
    const make = () => inst.chat.completions.createVision({
      messages: [{ role: 'user', content: [
        { type: 'text', text: promptFor(f) },
        { type: 'image_url', image_url: { url: `data:image/png;base64,${b64}` } }
      ]}],
      thinking: { type: 'disabled' }
    });
    let res = null;
    for (let a = 1; a <= 4; a++) {
      try {
        const c = await Promise.race([make(), new Promise((_, r) => setTimeout(() => r(new Error('t')), 180000))]);
        res = parseContent(c?.choices?.[0]?.message?.content || '');
        break;
      } catch (e) { console.error(`${f}: poskus ${a} FAIL ${e.message}`); await new Promise(r => setTimeout(r, 2500 * a)); }
    }
    if (res) { fs.writeFileSync(out, JSON.stringify(res, null, 2)); console.log(`${f}: OK`); }
    else console.error(`${f}: TOTAL-FAIL`);
  }
}
main().catch(e => { console.error(e); process.exit(1); });
