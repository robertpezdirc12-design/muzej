// P224 — celostansko branje skenov KRSTNE PREDZGODOVINE 04104 (4/15, leto 1882!).
// LEAD-P223: MEJA-1882/83 = s161 (TAIL-1882-z104–z106 + DVOJČKI-GRIBLJE-h68-z105/z106!);
//   s159 = z88–z95, s160 = z96–z103 (ŽE-VLM-proba!). Iskamo: MEJA-1881/82
//   (VSOTNA-'1 8 8 2.' + restart-z1) — PRED s159 → okno s147–s161!
// Izhod: /tmp/p224/vlm-page/sNN.json
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';

const IN_DIR = "/tmp/p224";
const OUT_DIR = "/tmp/p224/vlm-page";
fs.mkdirSync(OUT_DIR, { recursive: true });

const FILTER = process.argv.slice(2).map(s => 's' + parseInt(s.slice(1), 10));
const SCANS = fs.readdirSync(IN_DIR).filter(f => /^s\d+\.jpg$/.test(f))
  .map(f => f.replace('.jpg', '')).sort((a, b) => parseInt(a.slice(1)) - parseInt(b.slice(1)))
  .filter(s => FILTER.length === 0 || FILTER.includes(s));

function promptFor(scan) {
  return `To je CELLOTEN sken strani KRSTNE matične knjige župnije Podzemelj (obdobje 1871–1885 — STAREJŠI zvezek, STAREJŠA pisava!), slovenska Kurrent pisava (nemški gotski vpliv). Sken = ${scan}.
KONTEKST: to je STAREJŠI zvezek krstne knjige (mlajši zvezek 04105 se začne 1886). Iskamo leto 1882 = 4/15-predzgodovinska-linija — zato so tukaj lahko ZAKLJUČEK leta 1881 (tail + VSOTNA-'1/8/8/1'), MEJA-1881/82 (VSOTNA-'1/8/8/2' + restart-številčenje!), leto 1882, ali ZAČETEK leta 1883 (tail-1882-z104–z106 + VSOTNA-'1/8/8/3' + restart — MEJA-1882/83 = s161, ŽE-POTRJENA v P223!).
ZNANO-IZ-P223: s159 = zaporedne-88–95 (leta 1882!) + s160 = 96–103 (leta 1882!) + s161-vrste-1–3 = z104–z106-TAIL-1882 (Dez-31-×3 + DVOJČKI-GRIBLJE-h68!) — s161-nato-MEJA + restart-1883.
POZOR-ANOMALIJA: z96–z103 (s160) so bile VLM-prebrane kot NOVEMBER 16–30 — a pridejo PO z95-Dezember-16! To je lahko (a) blok-NAKNADNIH-vpisov (late-registracija — z96-'posthuma'!) ALBO (b) VLM-misread-'Dezember'→'November'. Opiši MESECE TOČNO tako kot so napisani — ne sklepaj!

Struktura tabele (stolpci, levo → desno; LAHKO se razlikuje — starejša forma! opisuj TOČNO kaj vidiš):
1. Zaporedna številka vrstice (ročno; vsako leto se restarta na 1!)
2. Mesec in dan rojstva ter dan krsta (meseci: Jänner, Feber, März, April, Mai, Juni, July, August, September, October, November, Dezember)
3. Bivališče: vas (npr. Griblje, Krasinec, Dobravice/Dobravce, Primostek, Gradac, Podžemelj/Podzemelj, Hrast/Hrnelj, Certoviše, Malše, Boršt, Klošter, Otok, Giriče/Geriče, Vranoviče, Begunja vas, Boginja vas, Ohljuka, Prilozje, Krivoglavce, Zemelj, Grem, Dragoše, Gorice, Maršiči, Paunoviče, Dolga vas, Kaplišče, Lemež) + hišna številka (poseben ozek stolpec — POZOR: Kurrent 3/5/8 zmeda, 7 = γ-forma s prečko!)
4. Ime otroka
5. Spola (moški/ženski kljukice »1«) + zakoniti/nezakoniti (včasih ločeni stolpci!)
6. Ime in priimek očeta (+ stan/gospodarska enota: npr. ¼/½/¾/1 Ganzl, Gütl, zemljiščni kmeti)
7. Ime in priimek (roj. dekliško) matere
8. Botra/botri (ime + priimek + stan — pogosto 2 osebi!)
9. Podpis duhovnika krstilnika (Kurrent-ligatura 'Prieſter' — dolgi ſ + in!)
10. Opomba (npr. poznejši pripisi o poroki/smrti!)

PRAVILA:
- Prepiši VSAKO vrstico tabele (od zgoraj navzdol) s čim več natančnostjo. Negotovo z [~], neberljivo z [?].
- ZAPOREDNA ŠTEVILKA: beri IZ KLJUČNEGA STOLPCA najbolj LEVO! Ne zaznamuj številk iz starostnega ali hišnega stolpca!
- POZOR NA KURRENT CIFRE: 4 ima zanko; 1 je ozka črtica; 7 ima prečko (γ-forma!); 5 je lahko podobna 6; 8/9 se ločita po zgornji zanki; 3/5/8 zmeda.
- Še posebej NATAČNO pri VASI: poišči VSE vrstice, kjer je vas »Griblje« (ali varianta Griblj/Grible/Griable) — to so ključne!
- Posebej zapiši VSE MARKERJE: letnica-glava »Leto 18 ..« (ali PRAZNA glava!), velike črte/veliki cifri čez vrsto (npr. »— 82. —« ali »/ 82«), VSOTNA-vrsta (lahko z RAZPETIMI CIFRAMI čez stolpce), mesečni prelomi, prazne vrste, restart zaporedne številke na 1, PREČRTANE vrstice!
- NASLOVNI LIST ('Tauf-Buch.' natisnjeno): če je stran naslovni list (BREZ vpisov ALI z vpisi čez naslov), to OZNAČI v "struktura"!
- Če stran vsebuje ZAČETEK leta 1882 (restart številčenja ali letnica-glava ali vsotna-marker), to jasno označi z MEJA.
- Če stran vsebuje ZAKLJUČEK leta 1881 (tail-vrstice pred restartom/vsotno leta 1882), to jasno označi z TAIL.
- Izhod: SAMO en veljaven JSON objekt (brez ograj, brez markdown):
{"skan": "${scan}", "struktura": "opis (glave, št. vrstic, posebnosti, naslovni-list?)", "leto": "najbolj verjetna letnica ali null", "meja": "opis ali null", "tail": "opis ali null", "vrstice": [{"vrsta": 1, "zaporedna": "1", "mesec": "Jänner", "rojen": "5.", "krsten": "7.", "vas": "Griblje", "hisna": "12", "otrok": "...", "spol": "moški|ženski", "zakonit": "zakoniti|nezakoniti|null", "ocec": "...", "matec": "...", "botra": "...", "duhovnik": "...", "opomba": null}], "markerji": ["opis ali ..."], "opomba": "..."}`;
}

function parseContent(content) {
  const t = content.trim().replace(/^```(json)?/i, '').replace(/```$/, '').trim();
  const a = t.indexOf('{');
  const b = t.lastIndexOf('}');
  if (a < 0 || b < 0) throw new Error('ni JSON v odgovoru');
  return JSON.parse(t.slice(a, b + 1));
}

async function readPage(zai, img, scan) {
  const b64 = fs.readFileSync(img).toString('base64');
  const make = () => zai.chat.completions.createVision({
    messages: [{ role: 'user', content: [
      { type: 'text', text: promptFor(scan) },
      { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${b64}` } }
    ]}],
    thinking: { type: 'disabled' }
  });
  let completion;
  for (let attempt = 1; attempt <= 5; attempt++) {
    completion = await Promise.race([
      make(),
      new Promise((_, rej) => setTimeout(() => rej(new Error('timeout')), 240000))
    ]);
    try {
      const c = completion?.choices?.[0]?.message?.content;
      if (!c) throw new Error('prazna vsebina');
      return parseContent(c);
    } catch (e) {
      console.error(`  ${scan}: poskus ${attempt} ni OK (${e.message})`);
      if (attempt === 5) throw e;
      await new Promise(r => setTimeout(r, 3000 * attempt));
    }
  }
}

async function main() {
  const inst = await ZAI.create();
  for (const scan of SCANS) {
    const out = `${OUT_DIR}/${scan}.json`;
    if (fs.existsSync(out)) { console.log(`${scan}: ŽE`); continue; }
    try {
      const res = await readPage(inst, `${IN_DIR}/${scan}.jpg`, scan);
      fs.writeFileSync(out, JSON.stringify(res, null, 2));
      const n = res.vrstice?.length ?? 0;
      console.log(`${scan}: OK vrstice=${n} leto=${res.leto} meja=${res.meja ? 'DA' : '-'} tail=${res.tail ? 'DA' : '-'} struktura=${String(res.struktura || '').slice(0, 80)}`);
    } catch (e) {
      console.error(`${scan}: FAIL ${e.message}`);
    }
  }
}
main().catch(e => { console.error(e); process.exit(1); });
