import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';
const DIR = '/tmp/p253';
const zai = await ZAI.create();
const BASE = `Poročna knjiga Trauungs-Buch 01738 (Podzemelj, 1873, Kurrent). Prepiši znak-za-znakom. Pazi: 'b'≠'2' (Kurrent!), 'Feber'='Februar', 'Jänner'='Januar', 'Mai'≠'März', '873'='1873'. Izhod SAMO JSON.`;
const QS = {
  'm1_dat': `${BASE} Slika = IZREZ marginalne št. + datumskega stolpca vpisa m1 (prvi vpis leta 1873 po restartu!).
Prepiši: (1) marginalno št. (kand. '1'), (2) DATUM poroke (DUEL: '24. Jänner' vs '29. Jänner' 1873 — pazi '2' vs '2'-z-obkljukanko, '4' vs '9'!).
JSON: {"marg":"","datum":"","kaj_je_vidno":""}`,
  'm2_dat': `${BASE} Slika = IZREZ marginalne št. + datuma vpisa m2 (1873). DUEL za datum: '3. Februar' vs '5. Februar' vs '8. Februar'.
JSON: {"marg":"","datum":""}`,
  'm3_dat': `${BASE} Slika = IZREZ marginalne št. + datuma vpisa m3 (1873). DUEL za datum: '4. Febr' vs '8. April' vs '5. Febr'.
JSON: {"marg":"","datum":""}`,
  'm1_stolpca': `${BASE} Slika = IZREZ ženin+nevesta stolpcev vpisa m1 (1873, restart!). Ženin: Anton [Kure/Huve/Fuße?]-kand. (Griblje 63?, 35/38 let, status?). Nevesta: Barbara [Križan?], 19 let, vas+hiša? (Griblje?).
JSON: {"zenin":{"ime":"","status":"","starost":"","vas":"","hisa":""},"nevesta":{"ime":"","status":"","starost":"","vas":"","hisa":""}}`,
  'm2_stolpca': `${BASE} Slika = IZREZ ženin+nevesta stolpcev vpisa m2 (1873). Ženin: Johann [Mavrin?], 26/33?, Griblje 28?. Nevesta: Anna [Jurjevič/Gnjejpič?], 23, hiša?
JSON: {"zenin":{"ime":"","status":"","starost":"","vas":"","hisa":""},"nevesta":{"ime":"","status":"","starost":"","vas":"","hisa":""}}`,
  'm3_stolpca': `${BASE} Slika = IZREZ ženin+nevesta stolpcev vpisa m3 (1873). Ženin: Mathias [Brin/Brine/Brinc?], 28, hiša DUEL: 25 vs 28 vs 8 (Griblje/Gorica?). Nevesta: Maria [Mavrin?], 28, hiša DUEL: 18 vs 25.
JSON: {"zenin":{"ime":"","status":"","starost":"","vas":"","hisa":""},"nevesta":{"ime":"","status":"","starost":"","vas":"","hisa":""}}`,
  'm5_dat': `${BASE} Slika = IZREZ marginalne št. + datuma vpisa m5 (1873). DUEL za marginalo: 5 vs 12 (restart-številčenje 1–17!). DUEL za datum: '8. Februar' vs '10. Februar' vs '12. Februar'.
JSON: {"marg":"","datum":""}`,
  'm7_dat': `${BASE} Slika = IZREZ marginalne št. + datuma vpisa m7 (1873). DUEL za marginalo: 7 vs 19. DUEL za datum: '19. Feber' vs '22. März' vs '28. Jänner'.
JSON: {"marg":"","datum":""}`,
  'm9_dat': `${BASE} Slika = IZREZ marginalne št. + datuma vpisa m9 (1873). DUEL za marginalo: 9 vs 19. Datum: '19. Feber' vs '25. Jänner'?
JSON: {"marg":"","datum":""}`,
  'm10_dat': `${BASE} Slika = IZREZ marginalne št. + datuma vpisa m10 (1873, zadnji na strani!). DUEL za marginalo: 10 vs 14 vs 15 vs 19. DUEL za datum: '19. Febr' vs '15. Jänner'?
JSON: {"marg":"","datum":""}`,
  'm7_stolpca': `${BASE} Slika = IZREZ ženin+nevesta stolpcev vpisa m7 (1873). Ženin: Georg [Hrovat/Hircel/Grabrijan?] (hiša 20?). Nevesta: Anna [Pezdirc!] (21, hiša?).
JSON: {"zenin":{"ime":"","status":"","starost":"","vas":"","hisa":""},"nevesta":{"ime":"","status":"","starost":"","vas":"","hisa":""}}`,
  'm11_full': `${BASE} Slika = CELA LEVA stran vrstice m11 (1873). Ženin DUEL: 'Johann' vs 'Peter' Hlebec (24, Griblje 3?). Nevesta: Maria [Jakofčič/Jahovič?], 18, vas+hiša DUEL: 'Griblje 7' vs 'Podheter 7'?.
JSON: {"zenin":{"ime":"","status":"","starost":"","vas":"","hisa":""},"nevesta":{"ime":"","status":"","starost":"","vas":"","hisa":""}}`,
  'm12_full': `${BASE} Slika = CELA LEVA stran vrstice m12 (1873). Ženin DUEL: 'Miho/Mihovil Kupamič?' vs 'Grible?' (starost 31, hiša 73?). Nevesta: 'Maria [Krambič/Zeljko/Hamler?]' (hiša 73? 13?). Prepiši vse vidno.
JSON: {"zenin":{"ime":"","status":"","starost":"","vas":"","hisa":""},"nevesta":{"ime":"","status":"","starost":"","vas":"","hisa":""}}`,
  'm13_full': `${BASE} Slika = CELA LEVA stran vrstice m13 (1873). Ženin DUEL: 'Ivan/John Leben? Pegdirc?' (28, hiša 46? 28? 'Leben'? = priimek ali 'Ledina'?). Nevesta: 'Anna [Geralj/Thralz/Šimec?]' (21, hiša 10, vas 'Mali Vrh'?).
JSON: {"zenin":{"ime":"","status":"","starost":"","vas":"","hisa":""},"nevesta":{"ime":"","status":"","starost":"","vas":"","hisa":""}}`,
  'm14_full': `${BASE} Slika = CELA LEVA stran vrstice m14 (1873). Ženin DUEL: 'Georg Kralj? Braj?' (27, vas 'Breg'?). Nevesta: 'Anna [Pegedin/Pegdirc/Legdire?]' (23, vas 'Pezdine/Primošek'?).
JSON: {"zenin":{"ime":"","status":"","starost":"","vas":"","hisa":""},"nevesta":{"ime":"","status":"","starost":"","vas":"","hisa":""}}`,
  'm15_dat': `${BASE} Slika = IZREZ marginalne št. + datuma vpisa m15 (1873). DUEL za marginalo: 15 vs 27. DUEL za datum: '25. April' vs '27. April' vs '8. April'.
JSON: {"marg":"","datum":""}`,
  'm16_dat': `${BASE} Slika = IZREZ marginalne št. + datuma vpisa m16 (1873). DUEL za datum: '23. April' vs '24. Febr' vs '27. April'.
JSON: {"marg":"","datum":""}`,
  'm17_full': `${BASE} Slika = CELA LEVA stran vrstice m17 (1873, ZADNJI VPIS v stari knjigi pred prehodom!). Ženin: Anton [Henke?] (33, hiša DUEL: 35 vs 15? vas 'Gra?'='Gradac?'). Nevesta: ime?? (Josefa? Marija?), priimek?, hiša?. Prepiši VSE.
JSON: {"zenin":{"ime":"","status":"","starost":"","vas":"","hisa":""},"nevesta":{"ime":"","status":"","starost":"","vas":"","hisa":""}}`,
};
async function ask(tag) {
  const out = `${DIR}/z2_${tag}.json`;
  if (fs.existsSync(out)) { console.log(`${tag}: skip`); return; }
  const content = [{ type: 'text', text: QS[tag] }];
  content.push({ type: 'image_url', image_url: { url: `data:image/jpeg;base64,${fs.readFileSync(`${DIR}/z2/${tag}.jpg`).toString('base64')}` } });
  for (let a = 1; a <= 5; a++) {
    try {
      const r = await zai.chat.completions.createVision({
        messages: [{ role: 'user', content }],
        temperature: 0.1, max_tokens: 800, thinking: { type: 'disabled' },
      });
      fs.writeFileSync(out, r.choices[0].message.content || '');
      console.log(`${tag}: OK`);
      await new Promise(r2=>setTimeout(r2,8000));
      return;
    } catch (e) { console.log(`${tag}: a${a} ${String(e).slice(0,50)}`); await new Promise(r2=>setTimeout(r2,11000)); }
  }
  console.log(`${tag}: FAIL`);
}
for (const tag of Object.keys(QS)) await ask(tag);
