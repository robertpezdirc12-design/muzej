import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';
const DIR = '/tmp/p258';
const zai = await ZAI.create();
const SCANS = [8, 9, 10];

const PROMPT = `Slika je sken strani PREDHODNIKA poročne knjige Trauungs-Buch 01738 (Podzemelj, 1828–1873), Kurrent-pisava, nemško.
Kontekst: P255 je prebral 1828 (s1–s3), P256 leto 1829 (s4–s6 vrstice 1–3), P257 pa 1830 (s6 vrstice 4–11: 12. Jän + 17. Febr ×4 + 18. + 21. + 30. Juni — julij–december 1830 PRAZEN) in 1831 (s7 = Pag. 11: 26. Jän 1831 + 1./9. Febr + d°-vrstice, 13 vpisov v 15 dneh).
Foliacija: Pag. = 2·sken − 3 (s6=9, s7=11, s8 naj bi bil Pag. 13).
Naloga — prepiši STRUKTURO strani:
1) 'Pag.' foliacijska številka čez vrh strani (pričakovano: s8='Pag. 13', s9='Pag. 15', s10='Pag. 17')
2) ŠTEVILO vrstic z vpisi (ne štej praznih) + ali so vse številčene (m1, m2, …) ali tudi neštevilčene
3) Letnica/letnice v glavi ali nad vrsticami (1831? 1832? 1833?) — kje točno se zgodi RESTART letnice
4) Za VSAKO vrstico poskusi prebrati: DATUM (dan. mesec), nato ŽENIN (ime, priimek, vas, hiša) in NEVESTA (ime, priimek, vas, hiša). Hišne številke so majhne — prepiši jih previdno, tudi delno.
5) Podpis duhovnika (desno spodaj) + ali je spodnji del strani PRAZEN oz. kje se stran konča. Ali je kje 'finis' ali kakšen drug zaključni zapis?
Izhod SAMO JSON: {"pag":"...","vrstic":N,"stevilcene":true/false,"leta_glava":"...","restart_kje":"...","rows":[{"r":1,"datum":"...","zenin":"ime [priimek?] vas hiša","nevesta":"ime [priimek?] vas hiša"}],"duhovnik":"...","spodaj_prazen":"...","razlaga":"..."}`;
async function run(s) {
  const out = `${DIR}/pass1_s${s}.json`;
  if (fs.existsSync(out) && fs.statSync(out).size > 50) { console.log(`s${s}: skip`); return; }
  const content = [{ type: 'text', text: PROMPT }];
  content.push({ type: 'image_url', image_url: { url: `data:image/jpeg;base64,${fs.readFileSync(`${DIR}/s${s}.jpg`).toString('base64')}` } });
  for (let a = 1; a <= 4; a++) {
    try {
      const r = await zai.chat.completions.createVision({
        messages: [{ role: 'user', content }],
        temperature: 0.1, max_tokens: 1600, thinking: { type: 'disabled' },
      });
      fs.writeFileSync(out, r.choices[0].message.content || '');
      console.log(`s${s}: OK (${(r.choices[0].message.content||'').length} zn.)`);
      return;
    } catch (e) { console.log(`s${s}: a${a} ${String(e).slice(0,70)}`); await new Promise(r2=>setTimeout(r2,2500)); }
  }
  console.log(`s${s}: FAIL`);
}
for (const s of SCANS) await run(s);
