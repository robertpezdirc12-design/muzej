// P249 — leto 1875 = 11/13: VLM pass-1 na s7–s10 (polni prepisi JSON)
// s7 = TAIL-1874 (margine 28–32 + finis-ornament + Pegdirc-Griblje-kandidat!)
// s8 = RESTART-1875 (velika '1875', 7 vrst, margina-1 '21'~'1' DUEL!)
// s9 = vrste 8–12 (margina-8 FIZIČNO → NAPAVED-preskok-8 kontrola! + nevesta 'Griblje 8' v10!)
// s10 = vrste 13–17 (tail-17 'Juli 20' re-verifikacija + priča 'Georg Pegdire'!)
import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';

const DIR = '/tmp/p249';
const OUT = `${DIR}/pass249`;
fs.mkdirSync(OUT, { recursive: true });

const s7Prompt = `To je razprti list poročne knjige (Trauungs-Buch) župnije Podzemelj, sken s7, foliacija 'Pag.' zgoraj desno. Ta list je TAIL prejšnjega leta 1874: marginalne številke so 28–32, datumi so leta 1874 (28. Februar – 18. November). NA DNU LISTA je velik okrasni zaključni zapis (tip 'finis'). Odgovori natančno:
1. Prepiši foliacijo zgoraj desno.
2. ŠTEVILO VRSTIC (vpisov). Za vsako vrsto: (a) marginalna številka TOČNO, (b) datum (leto+mesec+dan), (c) ženin Wohnort z hišno št. + ime + starost, (d) nevesta Wohnort z hišno št. + ime + starost, (e) starši obeh, (f) Befunde 2–3 stavka (priče!, podpisi!), (g) podpis duhovnika.
3. POMEMBNO — VRSTA Z MARGINALNO ŠT. 32 (zadnja, 18. November 1874): prepiši NEVESTIN Wohnort STOČNO — ali je "Griblje 1a" / "Griblje 13" / "Griblje 18" / kaj točno? Hišna številka s [~] če negotovo. In nevestino ime (ali je "Maria Pegdirc"?).
4. VELIKI OKRASNI ZAPIS na dnu lista (med zadnjo vrsto in robom): prepiši VSAKE VELIKE ČRKE znak za znak (npr. "f i n i s" + morebitne številke/letnice). Ali je v njem letnica 1874?
Negotovo=[~], neberljivo=[?]. Izhod: SAMO veljaven JSON brez ograj:
{"sken":"s7","foliacija":"...","rows":[{"m":"...","date":"...","groomWohnort":"...","groom":"...","groomAge":"...","brideWohnort":"...","bride":"...","brideAge":"...","elternGroom":"...","elternBride":"...","befunde":"...","priest":"..."}],"finisOkras":"znak-za-znak","finisLetnica":"...","note":"..."}`;

const s8Prompt = `To je razprti list poročne knjige (Trauungs-Buch) župnije Podzemelj, sken s8, foliacija 'Pag.' zgoraj desno. RESTART LETA 1875 je na tem listu: v datumskem stolpcu 1. vrste je VELIKA letnica "1875", nato mesec+dan. Odgovori natančno:
1. Prepiši foliacijo zgoraj desno.
2. ŠTEVILO VRSTIC. Za vsako vrsto: (a) marginalna številka TOČNO (pri 1. vrsti: ali je "1" samo, ALI več znakov — npr. "21"? označi [~] če negotovo!), (b) datum 1. vrste TOČNO (ali je "1875 Jänner 16." / "1875 Jänner 21." / kaj?), nadaljnje vrste: mesec+dan (ali ima katera LETNICO?), (c) ženin Wohnort+št.+ime+starost, (d) nevesta Wohnort+št.+ime+starost, (e) starši obeh, (f) Befunde 2–3 stavka (priče, zettel, Consens, Dispens!), (g) podpis duhovnika.
3. Ali je NAD tabelo posebna velika glava "1875" (kot naslov nad stolpcem) ALI stoji letnica SAMO v datumskem stolpcu 1. vrste? Prepiši točno vrh datumskega stolpca.
4. Ali je sredinska velika rokopisna opomba (npr. "finis")? Če je, prepiši znak za znak.
Negotovo=[~], neberljivo=[?]. Izhod: SAMO veljaven JSON brez ograj:
{"sken":"s8","foliacija":"...","velikaGlava":"...","rows":[{"m":"...","date":"...","groomWohnort":"...","groom":"...","groomAge":"...","brideWohnort":"...","bride":"...","brideAge":"...","elternGroom":"...","elternBride":"...","befunde":"...","priest":"..."}],"opomba":"...","note":"..."}`;

const pagePrompt = (n) => `To je razprti list poročne knjige (Trauungs-Buch) župnije Podzemelj, sken s${n}, foliacija 'Pag.' zgoraj desno. Leto je 1875 (meja-1874/75 na s8). Odgovori natančno:
1. Prepiši foliacijo zgoraj desno.
2. ŠTEVILO VRSTIC (vpisov). Za vsako vrsto od zgoraj navzdol: (a) marginalna številka TOČNO (modro-sivo; tudi slabo vidne!${n === 9 ? ' PRI 1. VRSTI: ali je margina "8"? TOČNO ena številka ali več?' : ''}),
   (b) datumski stolpec (pri 1. vrsti liste: ali je letnica "1875" napisana v datumu? nadaljnje vrste samo mesec+dan — NAPIŠI EKSPLICITNO, če letnica MANJKA ali JE prisotna),
   (c) ženin: Wohnort z hišno št. + ime + starost, (d) nevesta: Wohnort z hišno št. + ime + starost${n === 9 ? ' — PRI VRSTI Z MARGINO 10: nevestin Wohnort TOČNO (ali je "Griblje 8"?) in njeno ime (Katharina ALI Maria?)!' : ''},
   (e) starši obeh, (f) Befunde 2–3 stavka (priče!, Consens, mladoletnost, Dispens${n === 10 ? ', opombe tip "Vini 1875"' : ''}), (g) podpis duhovnika.
3. Ali je NAD tabelo velika glava "1875" ALI letnica samo v datumu 1. vpisa? Prepiši vrh datumskega stolpca.
4. Ali je sredinska velika rokopisna opomba (npr. "finis")? Če je, prepiši znak za znak.
Negotovo=[~], neberljivo=[?]. Izhod: SAMO veljaven JSON brez ograj:
{"sken":"s${n}","foliacija":"...","velikaGlava":"...","rows":[{"m":"...","date":"...","groomWohnort":"...","groom":"...","groomAge":"...","brideWohnort":"...","bride":"...","brideAge":"...","elternGroom":"...","elternBride":"...","befunde":"...","priest":"..."}],"opomba":"...","note":"..."}`;

const tasks = [
  { id: 's7-tail1874', img: `${DIR}/s7.jpg`, prompt: s7Prompt },
  { id: 's8-restart', img: `${DIR}/s8.jpg`, prompt: s8Prompt },
  { id: 's9-full', img: `${DIR}/s9.jpg`, prompt: pagePrompt(9) },
  { id: 's10-full', img: `${DIR}/s10.jpg`, prompt: pagePrompt(10) },
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
