import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';

const DIR = '/home/z/p251tmp';
const OUT = `${DIR}/pass1`;
fs.mkdirSync(OUT, { recursive: true });

const s1Prompt = `To je prvi sken stare poročne knjige (vezalo/naslovnica). Odgovori natančno:
1. Kaj stoji na tej strani — pisani napis, nalepka, pečat, indeks? Prepiši VSE berljivo znak za znak (nemško/latinsko/slovensko).
2. Ali je naslov knjige (npr. "Trauungs-Buch", "Trauungs-Copul-Buch") z letnicami? Prepiši.
3. Ali so vidne kakšne številke/podpisi/krožni pečati?
Negotovo=[~], neberljivo=[?]. Izhod: SAMO veljaven JSON brez ograj: {"sken":"s1","tip":"vezalo/naslovnica/...","napisi":["..."],"pečati":["..."],"opomba":"..."}`;

const s2Prompt = `To je razprti list poročne knjige (Trauungs-Buch) župnije Podzemelj, sken s2 = 'Pag. 1' = PRVA tabelarna stran knjige. Vrh: tiskani naslov 'Trauungs-Buch'. Na LEVI strani tabela (4 vrste leta 1873 z marginalami 18–21 + 1. vrsta leta 1874 z marginalo 1!), na DESNI starši/priče/Befunde/podpis. Odgovori natančno:
1. Prepiši foliacijo zgoraj desno (npr. "Pag. 1").
2. Za VSAKO od 5 vrst (marginala 18, 19, 20, 21, 1) prepiši po levih+desnih stolpcih: (a) datum (leto/mesec/dan!), (b) ženin: Wohnort+hišna št., ime+priimek, poklic/status, starost, (c) nevesta: Wohnort+št., ime+priimek, starost, (d) oče+mati ženina, (e) oče+mati neveste, (f) priče (ime+status), (g) Befunde (Eheschliessungszettel — KRAJ + datum!, Consens, Möttling-pripisi), (h) podpis duhovnika — PREPIŠI IME ZNAK ZA ZNAK (pazi: Kurrent 'D' lahko zgleda kot 'V' — Dovgan vs Vogran!).
3. Kje NA STRANI je meja 1873/74 (med katerima vrstama)? Ali je velika letnica '1874' nad vrsto 1?
4. Ali je kakšen črnilo-kontrast (vijolični/črni naknadni zapisi, prečrtavanja)? Kje?
Negotovo=[~], neberljivo=[?]. Izhod: SAMO veljaven JSON brez ograj: {"sken":"s2","foliacija":"...","rows":[{"m":"18","date":"...","groomWohnort":"...","groom":"...","groomAge":"...","brideWohnort":"...","bride":"...","brideAge":"...","elternGroom":"...","elternBride":"...","priče":"...","befunde":"...","priest":"..."}],"meja1873_74":"...","naknadni":"..."}`;

const zai = await ZAI.create();
async function run(t) {
  const out = `${OUT}/${t.id}.json`;
  if (fs.existsSync(out)) { console.log(`${t.id}: skip`); return; }
  const b64 = fs.readFileSync(t.img).toString('base64');
  for (let a = 1; a <= 4; a++) {
    try {
      const r = await zai.chat.completions.createVision({
        messages: [{ role: 'user', content: [
          { type: 'text', text: t.prompt },
          { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${b64}` } },
        ]}],
        temperature: 0.1, max_tokens: 3000, thinking: { type: 'disabled' },
      });
      fs.writeFileSync(out, r.choices[0].message.content || '');
      console.log(`${t.id}: OK`);
      return;
    } catch (e) { console.log(`${t.id}: attempt ${a} err ${String(e).slice(0,80)}`); await new Promise(s=>setTimeout(s,3000)); }
  }
  console.log(`${t.id}: FAIL`);
}
for (const t of [
  { id: 's1-vezalo', img: `${DIR}/s1_r1.jpg`, prompt: s1Prompt },
  { id: 's2-full', img: `${DIR}/s2_r1.jpg`, prompt: s2Prompt },
]) await run(t);
