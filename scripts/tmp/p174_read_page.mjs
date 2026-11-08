// P174 branje — VLM, stran za stranjo (mrliška 04894, leto 1908; P173 vzorec)
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

const DIR = '/tmp/p174';

const PROMPT = `To je stran mrliške (mrtvaške) knjige župnije Podzemelj/Griblje (šifra 04894), okoli leta 1908, napisana v nemški Kurrent pisavi s slovenskimi vnosi.

Preberi GLAVO strani in VSAK vnos vrstica-po-vrstico.

GLAVA — poročaj:
- številka strani (Pag.)
- zapis leta v glavi (natančno kot je napisano — pisar pogosto napiše npr. '187006', '18906', '18/905' — napake so POMENBNE!)
- velika letnica čez vrsto (če je)
- ali je restart zaporedne številke (meja let!)

TABELA ima stolpce: zaporedna številka, mesec (Januar, Februari, März/Marec, April, Mai, Juni, July, August, September, October, November, December — piše se samo ob prvem vnosu meseca!), dan smrti, dan pokopa, vas (Griblje, Gradac, Primostek, Krasinec, Otok, Kaplišče/Kapučiše, Ceroviše...), hišna številka, ime in priimek (stan), starost, bolezen, previden (sakramenti — '1' ali pika ali '—'), podpis duhovnika, opombe/marginalije.

PRAVILA:
- Negotova branja označi z [~], neberljiva z [?]
- NE izmišljuj vsebine; če stolpec manjka (npr. mesec ne ponovljen), pusti null
- Duhovnikov podpis preberi natanko (npr. 'Jos. Rauq', 'Hugo Lengsfeld', 'J. R. Kuhinek', 'Florjančič cap.', 'Dostál'...)
- Izhod: JSON objekt {
  "skan": "sNNN",
  "struktura": "opis glave + št. strani + letnica + št. vnosov + duhovniki",
  "meja": "ali strani vsebuje MEJO LET (velika letnica + restart)? opiši",
  "vrstice": [ { "vrsta": <n>, "zaporedna": "...", "mesec": "..."|null, "smrt": "...", "pokop": "...", "vas": "...", "hisna": "...", "ime": "...", "stan": "...", "starost": "...", "bolezen": "...", "previden": "..."|null, "duhovnik": "...", "opomba": "..."|null } ],
  "markerji": ["..."],
  "opomba": "splošna berljivost"
}`;

async function readPage(zai, scan) {
  const jpg = `${DIR}/s${scan}.jpg`;
  const b64 = fs.readFileSync(jpg).toString('base64');
  const completion = await zai.chat.completions.createVision({
    messages: [{ role: 'user', content: [
      { type: 'text', text: PROMPT },
      { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${b64}` } }
    ]}],
    thinking: { type: 'disabled' }
  });
  let raw = completion.choices[0]?.message?.content ?? '';
  // izlušči JSON
  const m = raw.match(/\{[\s\S]*\}/);
  if (!m) throw new Error('no JSON in response');
  return JSON.parse(m[0]);
}

async function main() {
  const scans = process.argv.slice(2);
  if (!scans.length) { console.error('usage: bun p174_read_page.mjs <scan>...'); process.exit(1); }
  const zai = await ZAI.create();
  for (const s of scans) {
    const out = `${DIR}/vlm-page/s${s}.json`;
    if (fs.existsSync(out)) { console.log(`s${s}: že obstaja, preskočim`); continue; }
    const t0 = Date.now();
    let data = null;
    for (let attempt = 1; attempt <= 5; attempt++) {
      try { data = await readPage(zai, s); break; }
      catch (e) {
        console.error(`s${s}: poskus ${attempt} napaka: ${e.message.slice(0, 100)}`);
        if (attempt >= 2 && !e.message.includes('429')) break;
        await new Promise(r => setTimeout(r, 25000));
      }
    }
    if (data) {
      fs.writeFileSync(out, JSON.stringify(data, null, 1));
      const n = (data.vrstice || []).length;
      console.log(`s${s}: OK (${((Date.now() - t0) / 1000).toFixed(0)}s, ${n} vrstic, glava: ${(data.struktura || '').slice(0, 80)})`);
    } else {
      console.error(`s${s}: NEUSPEH`);
    }
    await new Promise(r => setTimeout(r, 4000));
  }
}
main();
