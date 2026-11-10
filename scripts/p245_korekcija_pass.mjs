// P245 — P244-KOREKCIJA: VLM potrditveni prehodi na s25/s26/s27/s28
// Namen: potrditi/ovrži tezo "RESTART-1879 = s26" (P244 je trdil s27-TOP!)
import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';

const DIR = '/home/z/p245tmp';
const OUT = `${DIR}/pass245`;
fs.mkdirSync(OUT, { recursive: true });

const tasks = [
  {
    id: 's26-margin',
    img: `${DIR}/p245-margin-L.jpg`,
    prompt: `To je SKRAJNO LEVI ROB razprtega lista poročne knjige (Trauings-Buch) župnije Podzemelj, leto 1879. V LEVI MARGINI (levo od natisnjene tabele, ob vsaki vrsti) so rokopisne zaporedne številke vpisov (Lfd. Nummern), pisane svetlejšim (modro-sivim) črnilom.
Prepiši TOČNO, znak za znak, od zgoraj navzdol:
(a) vsako marginalno številko (tudi zelo svetle/nejasne!),
(b) datumski stolpec vsake vrste (leto, mesec, dan — npr. "1879 Jänner 1."),
(c) Wohnort-stolpec vsake vrste,
(d) prvi del imena ženina vsake vrste.
Negotovo branje označi z [~], neberljivo z [?].
Izhod: SAMO veljaven JSON brez ograj in komentarjev:
{"rows": [{"marginNo": "...", "date": "...", "wohnort": "...", "groomFirst": "..."}], "note": "komentar o berljivosti margin"}`
  },
  {
    id: 's26-full',
    img: `${DIR}/s26.jpg`,
    prompt: `To je razprti list poročne knjige (Trauungs-Buch) župnije Podzemelj, foliacija zgoraj desno. Odgovori:
1. Prepiši foliacijo zgoraj desno.
2. Koliko vpisov (vrst) je na LEVI polovici lista? Za vsako vrsto: datum (leto/mesec/dan), ženin (ime, poklic, Wohnort, hišna št.), nevesta (ime, hiša), starosti.
3. Ali je NAD tabelo posebna VELIKA letnična glava "1879" (kot naslov), ALI letnica nastopi SAMO kot del datuma prvega vpisa? Prepiši točno, kaj stoji na vrhu datumskega stolpca.
4. Kaj piše v Befunde-stolpcu (desna polovica) pri 3. (zadnji) vrsti — prepiši ključne datume in imena (npr. Einwilligung-datum, priče, Marta...).
5. Kdo je duhovnik (Unterschrift ali Befunde-podpisi) pri vsaki vrsti?
Negotovo = [~], neberljivo = [?]. Izhod: SAMO veljaven JSON:
{"foliacija": "...", "rows": [{"date": "...", "groom": "...", "bride": "...", "ages": "...", "befunde": "...", "priest": "..."}], "glava": "opis vrha datumskega stolpca", "note": "..."}`
  },
  {
    id: 's27-margin',
    img: `${DIR}/p245-s27-margin-L.jpg`,
    prompt: `To je SKRAJNO LEVI ROB razprtega lista poročne knjige župnije Podzemelj (leto 1879). V levi margini so rokopisne zaporedne številke vpisov (svetlejše črnilo, lahko zelo nejasne!).
Prepiši TOČNO, od zgoraj navzdol: (a) vsako marginalno številko (tudi slabo vidne — poglej ob sredini višine vsake vrste!), (b) datumski stolpec vsake vrste, (c) Wohnort (hišna številka!), (d) ime ženina.
Negotovo = [~], neberljivo = [?]. Izhod: SAMO JSON:
{"rows": [{"marginNo": "...", "date": "...", "wohnort": "...", "groomFirst": "..."}], "note": "..."}`
  },
  {
    id: 's28-margin',
    img: `${DIR}/p245-s28-margin-L.jpg`,
    prompt: `To je SKRAJNO LEVI ROB razprtega lista poročne knjige župnije Podzemelj (leto 1879). V levi margini so rokopisne zaporedne številke vpisov (svetlejše črnilo).
Prepiši TOČNO, od zgoraj navzdol: (a) vsako marginalno številko, (b) datum vsake vrste, (c) Wohnort z hišno številko, (d) ime ženina. Število vrst preštej natančno!
Negotovo = [~], neberljivo = [?]. Izhod: SAMO JSON:
{"rows": [{"marginNo": "...", "date": "...", "wohnort": "...", "groomFirst": "..."}], "note": "..."}`
  },
  {
    id: 's25-margin',
    img: `${DIR}/p245-s25-margin-L.jpg`,
    prompt: `To je SKRAJNO LEVI ROB razprtega lista poročne knjige župnije Podzemelj (konec leta 1878). Prepiši TOČNO:
(a) vsako marginalno številko v levi margini (svetlejše črnilo),
(b) datum vsake vrste (leto/mesec/dan),
(c) Wohnort z hišno številko,
(d) ime ženina,
(e) VELIKO rokopisno opombo, ki stoji MED/POD vrstami na sredini strani (začne se z "finis...") — prepiši jo čim bolj točno, znak za znak!
Negotovo = [~], neberljivo = [?]. Izhod: SAMO JSON:
{"rows": [{"marginNo": "...", "date": "...", "wohnort": "...", "groomFirst": "..."}], "finis": "prepis opombe", "note": "..."}`
  },
  {
    id: 's26-glava',
    img: `${DIR}/p245-glava-L.jpg`,
    prompt: `To je VRH (glava natisnjene tabele) leve strani razprtega lista poročne knjige župnije Podzemelj (Pag. 25). Prepiši TOČNO vsa natisnjena imena stolpcev od leve proti desni (tudi okrajšave, npr. "Jahr, Monat und Tag der Trauung", "Wohnort", "Lfd. Nr." ali podobno, "Trauname...", ...). Ali stolpec "Lfd. Nr." obstaja med Wohnort in Trauname? Izhod: SAMO JSON:
{"columns": ["..."], "lfdNrColumnExists": true, "note": "..."}`
  }
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

for (const t of tasks) await run(t);
console.log('P245-KOREKCIJA potrditveni prehodi: končano.');
