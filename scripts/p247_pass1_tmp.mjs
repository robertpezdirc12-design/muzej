// P247 — leto 1877 = 9/13: VLM pass-1 na s15–s18 (polni prepisi)
// Restart-1877 = s15-TOP (Read-očesa predhodno: marginal 1, letnica INLINE); s18-tail že brano z očesi v P246.
import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';

const DIR = '/home/z/p247tmp';
const OUT = `${DIR}/pass247`;
fs.mkdirSync(OUT, { recursive: true });

const pagePrompt = (n) => `To je razprti list poročne knjige (Trauungs-Buch) župnije Podzemelj, sken s${n}, foliacija 'Pag.' zgoraj desno. Leto je 1877 (na s14 je 1876-tail + 'finis'). Odgovori natančno:
1. Prepiši foliacijo zgoraj desno (npr. "Pag. 14").
2. ŠTEVILO VRSTIC (vpisov) na LEVI polovici lista. Za vsako vrsto od zgoraj navzdol prepiši:
   (a) marginalno zaporedno številko v LEVI margini (svetlejše/modro-sivo črnilo; tudi slabo vidne, prečrtane ali popravljene!),
   (b) datumski stolpec (leto/mesec/dan — npr. "1877 Jänner 14." — če letnica NI napisana, samo mesec+dan!),
   (c) ženin: Wohnort z hišno št. (pazi: "Griblje 36" / "Gübl." / "Gri. šte." / "Križ. šte." / kraj + hišna št.), Zaufname/Familien-Name und Stand, starost,
   (d) nevesta: Wohnort z hišno št., Zaufname/Familien-Name und Stand, starost,
   (e) Eltern des Bräutigams (starši ženina: oče+mati z Zaufname) in Eltern der Braut (starši neveste),
   (f) Befunde-stolpec: ključne ugotovitve (Einwilligung-datum, Dispens, Konsens, priče, mladoletnost, finis...), povzemi 2–3 stavka,
   (g) Unterchrift (podpis duhovnika) — prepiši ime.
3. Ali je NAD tabelo posebna VELIKA letnična glava "1877" (kot naslov), ALI letnica nastopi SAMO kot del datuma prvega vpisa? Prepiši točno, kaj stoji na vrhu datumskega stolpca.
4. Ali je na sredini strani med vrstami kakšna VELIKA rokopisna opomba (npr. "finis ...")? Če je, jo prepiši znak za znak.
Negotovo branje označi z [~], neberljivo z [?]. Izhod: SAMO veljaven JSON brez ograj in komentarjev:
{"sken": "s${n}", "foliacija": "...", "velikaGlava": "opis", "rows": [{"m": "...", "date": "...", "groomWohnort": "...", "groom": "...", "groomAge": "...", "brideWohnort": "...", "bride": "...", "brideAge": "...", "elternGroom": "...", "elternBride": "...", "befunde": "...", "priest": "..."}], "opomba": "...", "note": "berljivost"}`;

const tasks = [15, 16, 17, 18].map((n) => ({
  id: `s${n}-full`,
  img: `${DIR}/s${n}.jpg`,
  prompt: pagePrompt(n),
}));

const zai = await ZAI.create();

async function run(t) {
  const out = `${OUT}/${t.id}.json`;
  if (fs.existsSync(out)) { console.log(`${t.id}: že obstaja, preskočim`); return; }
  const b64 = fs.readFileSync(t.img).toString('base64');
  for (let attempt = 1; attempt <= 5; attempt++) {
    try {
      console.log(`--- ${t.id} (poskus ${attempt}) ...`);
      const completion = await Promise.race([
        zai.chat.completions.createVision({
          messages: [{ role: 'user', content: [
            { type: 'text', text: t.prompt },
            { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${b64}` } }
          ]}],
          thinking: { type: 'disabled' }
        }),
        new Promise((_, rej) => setTimeout(() => rej(new Error('TIMEOUT 240s')), 240000))
      ]);
      const raw = completion.choices[0]?.message?.content ?? '';
      fs.writeFileSync(out, raw);
      console.log(`${t.id}: OK (${raw.length} znakov) -> ${out}`);
      return;
    } catch (e) {
      const is429 = e.message.includes('429') || e.message.toLowerCase().includes('too many');
      console.error(`${t.id}: napaka: ${e.message.slice(0, 120)}`);
      if (!is429 && attempt >= 4) { fs.writeFileSync(out, `{"ERROR": "${e.message.slice(0,200)}"}`); return; }
      await new Promise(r => setTimeout(r, is429 ? 25000 : 8000));
    }
  }
}

for (const t of tasks) { await run(t); }
console.log('PASS-1 KONČAN');
