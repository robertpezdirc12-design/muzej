import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';
const DIR = '/home/z/p251tmp';
const OUT = `${DIR}/solo`;
fs.mkdirSync(OUT, { recursive: true });
const zai = await ZAI.create();

const P = {
  'priest-compare': `Na treh slikah so PODPISI duhovnika iz poročne knjige (Kurrent-pisava, ~1873): 1. slika = vrsta m18, 2. = m20, 3. = m21. Za VSAKO prepiši ime znak za znak. KRITIČNO: prva črka priimka je lahko Kurrent 'D' ali 'V' (npr. 'Dovgan' vs 'Vogran'/'Vogrinc'); zadnjice '-gan/-grin/-granc'. Primerjaj oblike črk med vsemi tremi: isti duhovnik ali ne? Izhod SAMO JSON: {"m18":"...","m20":"...","m21":"...","isti":"da/ne","razlaga":"..."}`,
  'priest-m19': `Sliki kažeta podpis duhovnika (Kurrent, 1873) iz vrste m19: prva = ozek izrez, druga = širši kontekst z opombami. Prepiši IME duhovnika znak za znak (kandidati: 'Daniel Fercher' / 'Teršaj' / drugo). Nato prepiši vse črno/vijolično naknadne zapise pod/ob podpisu (npr. 'Möttling', datum, opombe). Izhod SAMO JSON: {"priest":"...","naknadno":["..."],"razlaga":"..."}`,
  'm18-bride': `Izrez vrste m18 (1873): nevesta. Prepiši: (1) Wohnort + hišno št. (kandidati 'Griblje 62'/'Griblje 63'/'Griblje 6b'), (2) ime+priimek (kandidati 'Maria Hrižan'/'Maria Križan' — pazi začetni 'H'/'K'), (3) starost. Izhod SAMO JSON: {"wohnort":"...","ime":"...","starost":"...","razlaga":"..."}`,
  'm20-groom': `Izrez vrste m20 (1873): ženin. Prepiši: (1) Wohnort + hišno št. (kandidati 'Griblje 22'/'Griblje 26'/'Griblje 2b' — pazi drugi znak '2' vs 'b'!), (2) ime+priimek+status (kandidati 'Johann Milek, Innmann/Inmann/Landmann'), (3) starost (kandidati '34'/'39'). Izhod SAMO JSON: {"wohnort":"...","ime":"...","starost":"...","razlaga":"..."}`,
  'm21-vase': `Dva izreza vrste m21 (1873): Wohnort ženina in neveste. Gre za VAS z hišnima št. 12 in 10. Prepiši ime vasi znak za znak iz obeh (kandidati: 'Lothvišče/Losoviče/Lasoviče/Loštice/Čerlovica/Vetrhovica/...'). Kaj je najverjetnejše? Izhod SAMO JSON: {"zenin":"...","nevesta":"...","sklep":"...","razlaga":"..."}`,
  'm18-groom-ime': `Izrez vrste m18 (1873): ime+priimek+status ženina (Griblje 13). Prepiši znak za znak (kandidati: 'Mathias Jabovšič/Jahovšič/Gahovšič/Jakopšič', status 'Ledina/Lendava/Innmann/kmet?'). Izhod SAMO JSON: {"ime":"...","status":"...","razlaga":"..."}`,
  'm19-groom-ime': `Izrez vrste m19 (1873): ime+priimek+status ženina (Klagenfurt). Prepiši znak za znak — večvrstični zapis: 'Josef/Narzis/Iberer-Überer/h.h.-Leining/genannt-...' (kandidati: 'Nagis/Narzis/Narcis', 'Höfer/Iberer/Überer', 'k.k. Lakai/k.k. Leining'). Izhod SAMO JSON: {"ime":"...","status":"...","razlaga":"..."}`,
};

async function run(id, files) {
  const out = `${OUT}/${id}.json`;
  if (fs.existsSync(out)) { console.log(`${id}: skip`); return; }
  const content = [{ type: 'text', text: P[id] }];
  for (const f of files) content.push({ type: 'image_url', image_url: { url: `data:image/jpeg;base64,${fs.readFileSync(f).toString('base64')}` } });
  for (let a = 1; a <= 4; a++) {
    try {
      const r = await zai.chat.completions.createVision({
        messages: [{ role: 'user', content }],
        temperature: 0.1, max_tokens: 1200, thinking: { type: 'disabled' },
      });
      fs.writeFileSync(out, r.choices[0].message.content || '');
      console.log(`${id}: OK`);
      return;
    } catch (e) { console.log(`${id}: a${a} ${String(e).slice(0,70)}`); await new Promise(s=>setTimeout(s,2500)); }
  }
  console.log(`${id}: FAIL`);
}
await run('priest-compare', [`${DIR}/krops/m18_priest.jpg`, `${DIR}/krops/m20_priest.jpg`, `${DIR}/krops/m21_priest.jpg`]);
await run('priest-m19', [`${DIR}/krops/m19_priest.jpg`, `${DIR}/krops/m19_priest_wide.jpg`]);
await run('m18-bride', [`${DIR}/krops/m18_bride.jpg`]);
await run('m20-groom', [`${DIR}/krops/m20_groom.jpg`]);
await run('m21-vase', [`${DIR}/krops/m21_gw.jpg`, `${DIR}/krops/m21_bw.jpg`]);
await run('m18-groom-ime', [`${DIR}/krops/m18_groom.jpg`]);
await run('m19-groom-ime', [`${DIR}/krops/m19_groom.jpg`]);
