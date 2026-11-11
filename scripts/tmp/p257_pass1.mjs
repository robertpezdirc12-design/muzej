import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';
const DIR = '/tmp/p257';
const zai = await ZAI.create();
const SCANS = [6, 7];

const PROMPT = `Slika je sken strani PREDHODNIKA poročne knjige Trauungs-Buch 01738 (Podzemelj, 1828–1873), Kurrent-pisava, nemško.
Kontekst: P255 je prebral 1828 (s1–s3), P256 pa 1829 (s4–s6 vrstice 1–3). Znani podatki:
- s6 (Pag. 9): vrstice 1–3 = leto 1829 (1. März / 5. Juli / 25. November), nato RESTART letnice 1830 na vrstici 4: '1830 12 Jenner' (12. Jänner). Pričakovanih 8 vpisov 1830: 12. Jän + 17. Febr ×4 + 18. + 21. + 30. Juni (spodnja polovica leta 1830 je PRAZNA — julij–december ni vpisov).
- s7 (Pag. 11): pričakovano leto 1831 (26. Jänner 1831 + 1./9. Febr + dt°-vrstice), ~13 vrstic.
Naloga — prepiši STRUKTURO strani:
1) 'Pag.' foliacijska številka čez vrh strani (pričakovano: s6='Pag. 9', s7='Pag. 11')
2) ŠTEVILO vrstic z vpisi (ne štej praznih) + ali so vse številčene (m1, m2, …) ali tudi neštevilčene
3) Letnica/letnice v glavi ali nad vrsticami (1829? 1830? 1831?) — kje točno se zgodi RESTART letnice
4) Za VSAKO vrstico poskusi prebrati: DATUM (dan. mesec), nato ŽENIN (ime, priimek, vas, hiša) in NEVESTA (ime, priimek, vas, hiša). Hišne številke so majhne — prepiši jih previdno, tudi delno.
5) Podpis duhovnika (desno spodaj) + ali je spodnji del strani (julij–december) res PRAZEN (s6) oz. kje se stran konča (s7)
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
