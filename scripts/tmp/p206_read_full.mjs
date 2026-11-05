// P206 — branje širokega arbitražnega izreza s88-r9..r13
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';
const f = '/tmp/p206/krop2/arb_s88_full_table.png';
const b64 = fs.readFileSync(f).toString('base64');
const inst = await ZAI.create();
const make = () => inst.chat.completions.createVision({
  messages: [{ role: 'user', content: [
    { type: 'text', text: `To je IZREZ dna strani MRLIŠKE matične knjige Podzemelj (leto 1871, meseca April–Mai!), slovenska Kurrent pisava. Izrez vsebuje VSE vrstice tabele tabele s STOLPCI: [zaporedna-št. (ročna, levo-ozka)] [mesec+dan smrti / dan pokopa] [vas Land/Wohnort] [Hišna No.] [ime+stan] [starost] [bolezen]...

NALOGA — prepiši VSAKO vrstico od-zgoraj-navzdol s TEMI POLJI in za VSAKO vrstico posebej:
1. zaporedna (ročna-št.-levo — NATAČNO! 28/29/30/31 Kurrent-zmeda!)
2. mesec (April ali Mai — mesečni-prelom-v-izrezu?)
3. smrt + pokop (dva-datuma!)
4. vas
5. hišna
6. ime (z [~] negotovo)
7. starost

POSEBNA VPRAŠANJA:
A) Koliko vrstic SKUPAJ vidiš v izrezu?
B) Katera je ZADNJA (spodnja) zaporedna-številka pred končno-debelo-črto?
C) Ali je MESČENI-PRELOM (April→Mai) v izrezu — pri kateri vrstici?
D) Ali katera vrstica ima vas 'Griblje' — katera-zaporedna + hišna + ime?

Izhod: SAMO en veljaven JSON:
{"izrez": "s88-CELATA-TABELA", "n_vrstic": 5, "vrstice": [{"zaporedna": "...", "mesec": "...", "smrt": "...", "pokop": "...", "vas": "...", "hisna": "...", "ime": "...", "starost": "..."}], "zadnja_zaporedna": "...", "prelom": "...", "griblje": "...", "opomba": "..."}` },
    { type: 'image_url', image_url: { url: `data:image/png;base64,${b64}` } }
  ]}],
  thinking: { type: 'disabled' }
});
for (let a = 1; a <= 4; a++) {
  try {
    const c = await Promise.race([make(), new Promise((_, r) => setTimeout(() => r(new Error('t')), 180000))]);
    const t = (c?.choices?.[0]?.message?.content || '').trim().replace(/^```(json)?/i, '').replace(/```$/, '');
    const res = JSON.parse(t.slice(t.indexOf('{'), t.lastIndexOf('}') + 1));
    fs.writeFileSync('/tmp/p206/krop2/arb_s88_wide.json', JSON.stringify(res, null, 2));
    console.log('OK n_vrstic=', res.n_vrstic, 'zadnja=', res.zadnja_zaporedna, 'prelom=', res.prelom, 'griblje=', res.griblje);
    process.exit(0);
  } catch (e) { console.error(`poskus ${a} FAIL ${e.message}`); await new Promise(r => setTimeout(r, 2500 * a)); }
}
process.exit(1);
