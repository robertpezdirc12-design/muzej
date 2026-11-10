// P247 pass-2: VLM na 15 kropih (ultra-zoom 3×)
import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';

const DIR = '/home/z/p247tmp';
const OUT = `${DIR}/pass247`;

const rowPrompt = (id, hint) => `To je ULTRA-ZOOM krop ene vrstice (vpisa) poročne knjige Podzemelj, ${id}. Kontekst: ${hint}. Prepiši VSAKO polje natančno znak za znak (Kurrent-rokopis, nemško):
- marginalna številka v levi margini (tudi prečrtane/popravljene!),
- datum (leto/mesec/dan — če manjka letnica, reci EXPLICITNO!),
- ženin: Wohnort + hišna št. (pazi: "Griblje N" / "Gri. belj. č. N" / "Gübl." / kraj+št.), priimek+ime, stan (Bauer/½ Gübl./Baumw.-arbeiter/Inwohner/Häusler...), starost,
- nevesta: Wohnort + hišna št., priimek+ime (tudi roj./geb./verw.-opombe!), stan, starost,
- starši ženina (Eltern des Bräutigams): oče (ime+priimek+stan) + mati (ime+roj. priimek),
- starši neveste (Eltern der Braut),
- Befunde: vsa besedila (unanimous-datum, Konsens, Dispens, priče, mladoletnost, pripisi!),
- podpis duhovnika.
Negotovo=[~], neberljivo=[?]. Izhod: SAMO veljaven JSON:
{"id": "${id}", "m": "...", "datum": "...", "zenin": "...", "nevesta": "...", "elternZenin": "...", "elternNevesta": "...", "befunde": "...", "podpis": "...", "note": "..."}`;

const specialPrompts = {
  's18-margins': `To je ULTRA-ZOOM LEVE MARGINE razprtega lista poročne knjige (s18), foliacija Pag. 17. Vidnih je 4 vrstic. Za vsako vrsto od zgoraj navzdol prepiši marginalno številko TOČNO: ali je "14", "15", "16", "17" ali "18" ali kaj drugega? Ali je katera PREČRTANA ali POPRAVLJENA (npr. prečrtan pripisana druga številka)? Ali številka vsebuje več števk (npr. "74")? Prepiši vsako znak za znak z opombami o prečrtanem. Izhod: SAMO veljaven JSON: {"id": "s18-margins", "vrste": [{"pozicija": 1, "stevilka": "...", "opomba": "..."}, ...], "note": "..."}`,
  's18-r1-date': `To je ULTRA-ZOOM DATUMSKEGA STOLPCA prve vrstice lista s18 poročne knjige Podzemelj. Prepiši datum TOČNO znak za znak: ali je "Jänner 14" ALI "November 14" ALI kaj drugega? Ali je letnica ("1877") prisotna? Kurrent črki J/N/M so zavočene — preveri dobro: prva črka meseca ima en zalogeni spodaj (J) ali dva (N) ali nikoli (M)? Izhod: SAMO veljaven JSON: {"id": "s18-r1-date", "datum": "...", "letnica": "...", "mesec": "...", "reasoning": "kratek opis črk", "note": "..."}`,
};

const tasks = [];
const rowHints = {
  's15-m1-row': 'leto-1877 restart-lista s15 (Pag. 14), 1. vpis leta 1877, datum ~Jänner 14.',
  's15-m4-row': 'leto-1877, ~Februar, ženin z Griblje 8 (½ Gübl.), nevesta morda tudi Griblje (8 ali 31).',
  's15-m5-row': 'leto-1877, ~Februar, ženin z Griblje (31 ali 51), nevesta 16 let (mladoletnica!), kraj "Arau. sine" ali "Kra. sine" (Krasinec?).',
  's16-m6-row': 'leto-1877, ~Feber 6., ženin "Horasi nec. 16" ali "Krasinec 16" Johann Čupanič/Trupanič, nevesta Margaretha Harasinič.',
  's16-m7-row': 'leto-1877, ~Februar, ženin Johann Prodavie/Prodančič/Brozdovič Krasinec?, nevesta Katharina March/Ahac, hišna 31, 16 let (mladoletnica!).',
  's16-m8-row': 'leto-1877, ~Februar/Marec, ženin Martin Skala/Skalar "Adligsmann", nevesta Margaretha Ptičjan/Perjan 17 let.',
  's16-m9-row': 'leto-1877, ~Februar/Marec, ženin Peter Jakofčič/Jagerfeir, nevesta Margaretha Jakofčič/Jagerfeir (ISTA PRIIMKA obeh strani?).',
  's17-m13-row': 'leto-1877, ~August 1., ženin Josef Plut/Pleivc "ausser Ehe geb." s pripisom "des Pfarrers v. Črnomelj"?, nevesta Agnes Plut/Guek Kloster 27 ali 3.',
  's17-m14-row': 'leto-1877, ~September 16., ženin Johann Mic/Muec Primostek?, nevesta Maria geb. Križan/Pežjan.',
  's18-r2-row': 'leto-1877-tail, datum morda "28. Desembris" ali "28. Novembris", ženin Nicholaus Terdić/Serttič Gradac?/Griblje 3?, nevesta Theresia Allešić/Ažetič Griblje 69, 40 let, vmožitva/verw.',
  's18-r3-row': 'leto-1877-tail, ~November 21., ženin Josef Blat/Bluh/Pluh z "Gri. belj./Riblov/Ble. št. 36", nevesta Katharina Hugelf/Kugelj Dobrava 11?, 19 let.',
  's18-r4-row': 'leto-1877-tail, ~25. November, ženin Josef Stubler "Cerki 31", nevesta Barbara Stubler gospodarica Primostek 2?, 35 let, pripis morda "wgrin 33".',
  's14-m14-row': 'leto-1876-TAIL (kontekst!, ne 1877), ~November 15., ženin Johann Juregovič "Wilsput nec. 18", nevesta Anna Pegdire/PEZDIRC Griblje 30, 20 let.',
};
for (const [id, hint] of Object.entries(rowHints)) {
  tasks.push({ id, img: `${DIR}/krops2/${id}.jpg`, prompt: rowPrompt(id, hint) });
}
tasks.push({ id: 's18-margins', img: `${DIR}/krops2/s18-margins.jpg`, prompt: specialPrompts['s18-margins'] });
tasks.push({ id: 's18-r1-date', img: `${DIR}/krops2/s18-r1-date.jpg`, prompt: specialPrompts['s18-r1-date'] });

const zai = await ZAI.create();

async function run(t) {
  const out = `${OUT}/p2-${t.id}.json`;
  if (fs.existsSync(out)) { console.log(`${t.id}: že obstaja`); return; }
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
      console.log(`${t.id}: OK (${raw.length} znakov)`);
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
console.log('PASS-2 KONČAN');
