// P248 — leto 1876 = 10/13: VLM pass-1 na s11–s14 (polni prepisi JSON)
// Restart-1876 = s11-VRSTA-2 (Read-očesi: margina 1, vpis 1 = 9.-Januar-1876, h31×h44!);
// s11-VRSTA-1 = tail-1875 (violet, margina ~18); s14-tail (vpisi 14–15 + finis) že 1:1 v P247.
import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';

const DIR = '/home/z/p248tmp';
const OUT = `${DIR}/pass248`;
fs.mkdirSync(OUT, { recursive: true });

const pagePrompt = (n) => `To je razprti list poročne knjige (Trauungs-Buch) župnije Podzemelj, sken s${n}, foliacija 'Pag.' zgoraj desno. Leto je 1876 (meja-1875/76 je na s11). Odgovori natančno:
1. Prepiši foliacijo zgoraj desno (npr. "Pag. 10").
2. ŠTEVILO VRSTIC (vpisov) na LEVI polovici lista. Za vsako vrsto od zgoraj navzdol prepiši:
   (a) marginalno zaporedno številko v LEVI margini (svetlejše/modro-sivo črnilo; tudi slabo vidne, prečrtane ali popravljene!),
   (b) datumski stolpec (leto/mesec/dan — npr. "1876 Jänner 9." — če letnica NI napisana, samo mesec+dan; NAPIŠI EKSPLICITNO, če letnica MANJKA!),
   (c) ženin: Wohnort z hišno št. (pazi: "Griblje 36" / "Gri. šte. 35" / "Gübl." / kraj + hišna št.), Zaufname/Familien-Name und Stand, starost,
   (d) nevesta: Wohnort z hišno št., Zaufname/Familien-Name und Stand, starost,
   (e) Eltern des Bräutigams (starši ženina: oče+mati z Zaufname) in Eltern der Braut (starši neveste),
   (f) Befunde-stolpec: ključne ugotovitve (Einwilligung-datum, Dispens, Konsens, priče, mladoletnost, finis...), povzemi 2–3 stavka,
   (g) Unterchrift (podpis duhovnika) — prepiši ime.
3. Ali je NAD tabelo posebna VELIKA letnična glava "1876" (kot naslov), ALI letnica nastopi SAMO kot del datuma prvega vpisa? Prepiši točno, kaj stoji na vrhu datumskega stolpca.
4. Ali je na sredini strani med vrstami kakšna VELIKA rokopisna opomba (npr. "finis ...")? Če je, jo prepiši znak za znak.
Negotovo branje označi z [~], neberljivo z [?]. Izhod: SAMO veljaven JSON brez ograj in komentarjev:
{"sken": "s${n}", "foliacija": "...", "velikaGlava": "opis", "rows": [{"m": "...", "date": "...", "groomWohnort": "...", "groom": "...", "groomAge": "...", "brideWohnort": "...", "bride": "...", "brideAge": "...", "elternGroom": "...", "elternBride": "...", "befunde": "...", "priest": "..."}], "opomba": "...", "note": "berljivost"}`;

const s11Prompt = `To je razprti list poročne knjige (Trauungs-Buch) župnije Podzemelj, sken s11, foliacija 'Pag.' zgoraj desno. MEJA-LET na tem listu: PRVA (zgornja, delno odrezana) vrsta je TAIL prejšnjega leta 1875 (vijolično/svetlo črnilo), od DRUGE vrste naprej se začne leto 1876 (marginalna številka 1 = restart!). Odgovori natančno:
1. Prepiši foliacijo zgoraj desno.
2. TAIL-VRSTA (zgornja, margina ~8 ali 18): prepiši marginalno številko TOČNO (ali je "8" ali "18"? ali več števk?), datum (leto!mesec!dan), ženin (Wohnort+št.+ime+starost), nevesta, starši, Befunde (vijolični pripisi!), podpis.
3. ŠTEVILO preostalih vrst (restart-1876) od 2. vrste navzdol. Za vsako: (a) marginalna številka, (b) datum (pri PRVI restart-vrsti: ali je letnica "1876" napisana v datumskem stolpcu? NAPIŠI EKSPLICITNO!), (c) ženin Wohnort+št.+ime+starost, (d) nevesta Wohnort+št.+ime+starost, (e) starši ženina, (f) starši neveste, (g) Befunde 2–3 stavka, (h) podpis.
4. Ali je NAD tabelo VELIKA letnična glava "1876" ALI letnica samo v datumu restart-vpisa? Prepiši vrh datumskega stolpca.
5. Ali je sredinska velika rokopisna opomba (npr. "finis ...")? Prepiši znak za znak.
Negotovo=[~], neberljivo=[?]. Izhod: SAMO veljaven JSON brez ograj:
{"sken": "s11", "foliacija": "...", "tail1875": {"m": "...", "datum": "...", "zenin": "...", "nevesta": "...", "eltern": "...", "befunde": "...", "podpis": "..."}, "velikaGlava": "opis", "rows": [{"m": "...", "date": "...", "groomWohnort": "...", "groom": "...", "groomAge": "...", "brideWohnort": "...", "bride": "...", "brideAge": "...", "elternGroom": "...", "elternBride": "...", "befunde": "...", "priest": "..."}], "opomba": "...", "note": "..."}`;

const tasks = [
  { id: 's11-meja', img: `${DIR}/s11.jpg`, prompt: s11Prompt },
  ...[12, 13, 14].map((n) => ({ id: `s${n}-full`, img: `${DIR}/s${n}.jpg`, prompt: pagePrompt(n) })),
];

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
      const s = raw.indexOf('{');
      const e = raw.lastIndexOf('}');
      if (s === -1 || e === -1) throw new Error('ni JSON v odgovoru');
      const j = JSON.parse(raw.slice(s, e + 1));
      fs.writeFileSync(out, JSON.stringify(j, null, 2));
      console.log(`${t.id}: OK (${raw.length} znakov)`);
      return;
    } catch (err) {
      console.log(`${t.id}: poskus ${attempt} NAPAKA: ${err.message}`);
      await new Promise(r => setTimeout(r, 4000));
    }
  }
  console.log(`${t.id}: VSI POSKUSI NEUSPEŠNI`);
}

for (const t of tasks) await run(t);
console.log('pass-1 KONČAN');
