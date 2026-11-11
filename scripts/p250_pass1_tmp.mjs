// P250 — leto 1874 = 12/13: VLM pass-1 na s2–s6 (polni prepisi JSON)
// Očesi-najprej POTRJENO: restart-1874 = s2-DNO (m1 = 19.-Jänner-1874!),
// Pag.1 = s2-top = m18/1873 (knjižno odpiranje SREDI številčenja!), s3 = m2–6, s4 = m7–11,
// s5 = m12–18, s6 = m19–27. s7-tail m28–32 že P249-1:1 (krop-datum m28 posebej).
import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';

const DIR = '/home/z/p250tmp';
const OUT = `${DIR}/pass250`;
fs.mkdirSync(OUT, { recursive: true });

const pagePrompt = (n, range) => `To je razprti list poročne knjige (Trauungs-Buch) župnije Podzemelj, sken s${n}, foliacija 'Pag.' zgoraj desno. Na tem listu so vpisi z marginalnimi številkami ${range} (leto 1874; meja-1873/74 je že prej). Odgovori natančno:
1. Prepiši foliacijo zgoraj desno (npr. "Pag. 4").
2. ŠTEVILO VRSTIC (vpisov) na LEVI polovici lista. Za vsako vrsto od zgoraj navzdol prepiši:
   (a) marginalno zaporedno številko v LEVI margini (svetlejše/modro-sivo črnilo; tudi slabo vidne, prečrtane ali popravljene!),
   (b) datumski stolpec (leto/mesec/dan — npr. "1874 Jänner 19." — če letnica NI napisana, samo mesec+dan; NAPIŠI EKSPLICITNO, če letnica MANJKA!),
   (c) ženin: Wohnort z hišno št. (pazi: "Griblje 63" / "Gri. šte." / "Gübl." / kraj + hišna št.), Zaufname/Familien-Name und Stand (IME + poklic!), starost,
   (d) nevesta: Wohnort z hišno št., Zaufname/Familien-Name und Stand, starost,
   (e) Eltern des Bräutigams (starši ženina: oče+mati z Zaufname) in Eltern der Braut (starši neveste),
   (f) Befunde-stolpec: ključne ugotovitve (Ehevertragstettel-datum + KRAJ!, Einwilligung, Dispens, Konsens, mladoletnost "Minderjährig", priče, Möttling-pripis...), povzemi 2–3 stavka,
   (g) Unterchrift (podpis duhovnika) — prepiši ime (Dovgan ali drugo!).
3. Ali je NAD tabelo posebna VELIKA letnična glava "1874" (kot naslov), ALI letnica nastopi SAMO kot del datuma prvega vpisa? Prepiši točno, kaj stoji na vrhu datumskega stolpca.
4. Ali je na sredini strani med vrstami ali na dnu kakšna VELIKA rokopisna opomba (npr. "finis ...")? Če je, jo prepiši znak za znak.
Negotovo branje označi z [~], neberljivo z [?]. Izhod: SAMO veljaven JSON brez ograj in komentarjev:
{"sken": "s${n}", "foliacija": "...", "velikaGlava": "opis", "rows": [{"m": "...", "date": "...", "groomWohnort": "...", "groom": "...", "groomBeruf": "...", "groomAge": "...", "brideWohnort": "...", "bride": "...", "brideAge": "...", "elternGroom": "...", "elternBride": "...", "befunde": "...", "priest": "..."}], "opomba": "...", "note": "berljivost"}`;

const s2Prompt = `To je razprti list poročne knjige (Trauungs-Buch) župnije Podzemelj, sken s2 = 'Pag. 1' = PRVA tabelarna stran knjige. MEJA-LET na tem listu: zgornje 4 vrste so TAIL leta 1873 (margine 18–21!), ZADNJA (spodnja, 5.) vrsta je RESTART leto 1874 (marginalna številka 1!). Odgovori natančno:
1. Prepiši foliacijo zgoraj desno.
2. ŠTEVILO vseh vrst. Za VSAAKO vrsto od zgoraj navzdol prepiši: (a) marginalno številko, (b) datum (leto!mesec!dan — pri TAIL-vrstah je leto 1873, pri zadnji vrsti 1874! NAPIŠI EKSPLICITNO, če letnica manjka), (c) ženin Wohnort+hišna št.+ime+poklic+starost, (d) nevesta Wohnort+št.+ime+starost, (e) starši ženina, (f) starši neveste, (g) Befunde 2–3 stavka (Ehevertragstettel-datum+KRAJ, Consens, Minderjährig, Möttling-pripisi!), (h) podpis duhovnika (pri tail-vrsti 19 je podpis VERJETNO DRUGAČEN — prepiši znak za znak!).
3. Ali je NAD tabelo posebna VELIKA glava (npr. "1873" ali "Trauungs-Buch" ali knjižni naslov)? Prepiši točno, kaj stoji na vrhu strani.
4. KER je to PRVA tabela knjige: ali prva vrsta začne z marginalno številko 18? Ali je kje opomba, da so prejšnji vpisi (1–17 leta 1873) v drugi knjigi?
Negotovo=[~], neberljivo=[?]. Izhod: SAMO veljaven JSON brez ograj:
{"sken": "s2", "foliacija": "...", "glavaVrh": "opis", "rows": [{"m": "...", "date": "...", "groomWohnort": "...", "groom": "...", "groomBeruf": "...", "groomAge": "...", "brideWohnort": "...", "bride": "...", "brideAge": "...", "elternGroom": "...", "elternBride": "...", "befunde": "...", "priest": "..."}], "opomba": "...", "note": "..."}`;

const tasks = [
  { id: 's2-meja-restart', img: `${DIR}/s2.jpg`, prompt: s2Prompt },
  { id: 's3-full', img: `${DIR}/s3.jpg`, prompt: pagePrompt(3, '2–6') },
  { id: 's4-full', img: `${DIR}/s4.jpg`, prompt: pagePrompt(4, '7–11') },
  { id: 's5-full', img: `${DIR}/s5.jpg`, prompt: pagePrompt(5, '12–18') },
  { id: 's6-full', img: `${DIR}/s6.jpg`, prompt: pagePrompt(6, '19–27') },
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
