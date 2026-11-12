// P259 — ONE-SHOT pass1 (s11|s12|s13): strukturni pass.
import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';
const s = process.argv[2];
if (![11, 12, 13].includes(Number(s))) { console.error('UPORABA: bun p259_pass1_one.mjs 11|12|13'); process.exit(2); }
const out = `/tmp/p259/pass1_s${s}.json`;
if (fs.existsSync(out) && fs.statSync(out).size > 50) { console.error(`s${s}: ze-obstaja`); process.exit(0); }
const PROMPT = `Slika je sken strani PREDHODNIKA poročne knjige Trauungs-Buch 01738 (Podzemelj, 1828–1873), Kurrent-pisava, nemško.
Kontekst: notranjost je brana po fazah: P255 = 1828 (s1–s3), P256 = 1829 (s4–s6 r1–r3), P257 = 1830/1831-odpiranje (s6 r4–r11 + s7), P258 = 1831-konec (s8) + 1832 (s9–s10-zgornji) + 1833-ODPIRANJE (s10-spodaj = Pag. 17: m1 = [3.|5.] Febr 1833 RESTART + m2–m6 = 6. Febr ×5 d°, zadnja vrstica strani = Johann PESDIRZ Griblje 50).
Foliacija: Pag. = 2·sken − 3 (s10=17 → s11 = Pag. 19, s12 = 21, s13 = 23).
Naloga — prepiši STRUKTURO strani:
1) 'Pag.' foliacijska številka čez vrh strani
2) ŠTEVILO vrstic z vpisi (ne štej praznih) + ali so vse številčene ali tudi neštevilčene
3) Letnica/letnice v glavi ali nad vrsticami (1833? 1834?) — kje točno se zgodi RESTART letnice
4) Za VSAKO vrstico poskusi prebrati: DATUM (dan. mesec), ŽENIN (ime, priimek, vas, hiša) in NEVESTA (ime, priimek, vas, hiša). Hišne številke so majhne — prepiši jih previdno, tudi delno.
5) Podpis duhovnika (desno spodaj) + ali je spodnji del strani PRAZEN. Ali je kje 'finis' ali drug zaključni zapis? Robne (marginalne) številke v levem robu — ali so in katere?
Izhod SAMO JSON: {"pag":"...","vrstic":N,"stevilcene":true,"leta_glava":"...","restart_kje":"...","rows":[{"r":1,"datum":"...","zenin":"ime [priimek?] vas hiša","nevesta":"ime [priimek?] vas hiša"}],"duhovnik":"...","spodaj_prazen":"...","razlaga":"..."}`;
const zai = await ZAI.create();
const content = [{ type: 'text', text: PROMPT }];
content.push({ type: 'image_url', image_url: { url: `data:image/jpeg;base64,${fs.readFileSync(`/tmp/p259/s${s}.jpg`).toString('base64')}` } });
const r = await zai.chat.completions.createVision({
  messages: [{ role: 'user', content }],
  temperature: 0.1, max_tokens: 1600, thinking: { type: 'disabled' },
});
const c = r.choices[0].message.content || '';
if (c.length < 30) { console.error(`s${s}: prekratko`); process.exit(1); }
fs.writeFileSync(out, c);
console.error(`s${s}: OK (${c.length})`);
process.exit(0);
