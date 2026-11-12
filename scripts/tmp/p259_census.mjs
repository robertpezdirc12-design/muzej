import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';
const zai = await ZAI.create();
const DIR = '/tmp/p259';

const L = (s, pag, kontext) => `Slika je CELA LEVA STRAN razprtega lista poročne knjige Trauungs-Buch 01738 (Podzemelj), Kurrent-pisava, nemško. Stran = Pag. ${pag}. ${kontext}
Naloga — ŠTETJE VRSTIC (census): preštej VSE vpise na strani in za VSAKEGA podaj:
1) zaporedno številko (1 = zgoraj),
2) DATUM vpisa (dan. mesec; 'd°'/'tt°' = isti dan kot prejšnji),
3) ime ŽENINA + njegovo VAS in hišno številko,
4) ime NEVESTE + njeno VAS in hišno številko,
5) marginalno številko v levem ROBU strani (če je — npr. '1', '2', ...), sicer prazno.
Pazi: vrstice so lahko dvovrstične — štej VPIS, ne mrežno vrstico! Prazne mrežne vrstice ne štej. Označi letnico v glavi stolpca datuma.
Izhod SAMO JSON: {"stevilo":N,"leta_glava":"...","rows":[{"r":1,"datum":"...","zenin":"ime vas hisa","nevesta":"ime vas hisa","rob":""}],"opomba":"..."}`;

const R = (s, pag, kontext) => `Slika je CELA DESNA STRAN razprtega lista poročne knjige Trauungs-Buch 01738 (Podzemelj), Pag. ${pag} — stolpci: Eltern des Bräutigams | Eltern der Braut | Zeugen | Urkunden | Unterschrift des trauenden Priesters. Leva stran (ista višina vrstic) ima vpise: ${kontext}
Naloga: preštej VSE vpise (vrstice) na strani in za VSAKOGA podaj zaporedno št. + imena STARŠEV ŽENINA (stolpec Eltern des Bräutigams) + imena STARŠEV NEVESTE + priči, če berljivi.
Izhod SAMO JSON: {"stevilo":N,"rows":[{"r":1,"starsiZenina":"...","starsiNeveste":"...","price":"..."}],"opomba":"..."}`;

const JOBS = [
  ['L11', L(11, 19, 'NADALJEVANJE leta 1833: kaskada 6. Febr-d° se nadaljuje iz Pag. 17 (tam m1–m6: [3.|5.] Febr + 6. Febr ×5, zadnja = Johann PESDIRZ Griblje 50). Pričakovano ~13 vrstic (8 × 6. Febr + 5 × 13. Febr).'),
      `${DIR}/s11_LEFT.jpg`],
  ['R11', R(11, 20, '1833: 6. Febr-d° ×8 (m7–m14) + 13. Febr ×5 (m15–m19) — ista višina vrstic.'),
      `${DIR}/s11_RIGHT.jpg`],
  ['L12', L(12, 21, '1833-KONEC + 1834-START: pričakovano ~12 vrstic (19. Febr + [12.?]-April? + 21. April + 5. Mai + [10.|26.] Oct + 27. Nov z robno št. 1 + 22. Jänner 1834 rob 2 + d° rob 3 + 29. Jänner ×4 rob 4–7). Pozorno na RESTART letnice 1834 in na ROBNE ŠTEVILKE!'),
      `${DIR}/s12_LEFT.jpg`],
  ['R12', R(12, 22, '1833-konec (19. Febr–27. Nov) + 1834-start (22. Jän + d° + 29. Jän ×4) — ista višina vrstic.'),
      `${DIR}/s12_RIGHT.jpg`],
  ['L13', L(13, 23, 'RESTART letnice 1834 v glavi! Pričakovano ~11 vrstic z ROBNIMI številkami 8–18: 5. Febr ×7 (rob 8–14) + 9. Febr (rob 15) + 10. Febr ×3 (rob 16–18). Pozorno na robne številke!'),
      `${DIR}/s13_LEFT.jpg`],
  ['R13', R(13, 24, '1834: 5. Febr ×7 + 9. Febr + 10. Febr ×3 — ista višina vrstic.'),
      `${DIR}/s13_RIGHT.jpg`],
];

async function run(id, prompt, file) {
  const out = `${DIR}/census_${id}.json`;
  if (fs.existsSync(out) && fs.statSync(out).size > 40) { console.log(`${id}: skip`); return; }
  const content = [{ type: 'text', text: prompt }];
  content.push({ type: 'image_url', image_url: { url: `data:image/jpeg;base64,${fs.readFileSync(file).toString('base64')}` } });
  for (let a = 1; a <= 4; a++) {
    try {
      const r = await zai.chat.completions.createVision({
        messages: [{ role: 'user', content }],
        temperature: 0.1, max_tokens: 2600, thinking: { type: 'disabled' },
      });
      fs.writeFileSync(out, r.choices[0].message.content || '');
      console.log(`${id}: OK`);
      return;
    } catch (e) { console.log(`${id}: a${a} ${String(e).slice(0,60)}`); await new Promise(r2=>setTimeout(r2,2500)); }
  }
  console.log(`${id}: FAIL`);
}
for (const [id, prompt, file] of JOBS) { await run(id, prompt, file); await new Promise(r => setTimeout(r, 1200)); }
