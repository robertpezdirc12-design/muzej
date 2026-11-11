import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';
const DIR = '/tmp/p256/datecol';
const zai = await ZAI.create();

const JOBS = [
  { id: 's4', extra: 'To je PRVA stran leta 1829 (r1 = 18. Jänner 1829). 8 vrstic z vpisi + 1 prazna.' },
  { id: 's5', extra: 'To je NADALJEVANJE 1829 (po s4). Pričakovano: Februar vrste, morda März. 8 vrstic.' },
  { id: 's6', extra: 'To stran vsebuje RESTART "1830 / 12 Jänner" na 4. vrsti (potrjeno)! Nad njo: ost 1829 (März r1!). 11 vrstic.' },
  { id: 's7', extra: 'To je leto 1831 (glava vsebuje "1831."). 13 vrstic. P255-pass-1 je brał datume 26. Jän / 1. Feb / 9. Nov / 9. Dec — preveri!' },
];

const PROMPT = (extra) => `Slika je POVEČAN datumski stolpec (celota, od glave do dna tabele) poročne knjige Trauungs-Buch 01738 (Podzemelj, Kurrent-pisava). Stolpec glava: 'Jahr, Monat und Tag der Trauung'. Zgoraj je pogosto letnica (npr. 1829/1830).
Konvencije knjige (iz leta 1828, P255): mesec je napisan ENKRAT, naslednje vrste uporabljajo DITTO: navpične črke (//), 'dto', 'ejusdem'/'ejusd.' (latinsko 'istega [meseca]'), ali prazno. Datum = dan + mesec. Nemške okrajšave: Jän(er), Febr, Mär, Apr, Mai, Jun(i/y), Jul(i), Aug, Sept, Okt(=8br!), Nov(=9br!), Dez(=Xbr/10br!). '8br'=Oktober, '9br'=November, 'Xbr'=Dezember (rimski številski meseci!).
POZOR: v celici sta lahko DVE vrsti rokopisa (dan + mesec/ditto). Prepiši VSZO vrstico zaporedoma (r1, r2, ...), vsako s svojim datumom. Če je ditto, reši verigo (mesec od zadnje napisane letvice).
${extra}
Izhod SAMO JSON: {"vrstice":[{"r":1,"datum":"...","novoLeto":false,"dittoMesec":false,"besedilo":"...","zanesljivost":"visoka/srednja/nizka"}],"razlaga":""}`;

async function run(job) {
  const out = `${DIR}/${job.id}_col.json`;
  if (fs.existsSync(out)) { console.log(`${job.id}: skip`); return; }
  const content = [{ type: 'text', text: PROMPT(job.extra) }];
  content.push({ type: 'image_url', image_url: { url: `data:image/jpeg;base64,${fs.readFileSync(`${DIR}/${job.id}_col5.jpg`).toString('base64')}` } });
  for (let a = 1; a <= 4; a++) {
    try {
      const r = await zai.chat.completions.createVision({
        messages: [{ role: 'user', content }],
        temperature: 0.1, max_tokens: 1600, thinking: { type: 'disabled' },
      });
      fs.writeFileSync(out, r.choices[0].message.content || '');
      console.log(`${job.id}: OK`);
      return;
    } catch (e) { console.log(`${job.id}: a${a} ${String(e).slice(0,70)}`); await new Promise(r2=>setTimeout(r2,4000)); }
  }
  console.log(`${job.id}: FAIL`);
}
for (const job of JOBS) { await run(job); await new Promise(r=>setTimeout(r,2000)); }
