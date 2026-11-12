// P259 — DUELI: VLM-branja duel-kompozitov (10 jobov, po p258_duels.mjs vzoru).
// Uporaba: bun p259_duels.mjs [job-id]  (brez id-ja = vsi jobi zaporedno)
// Poganja se KO JE KVOTA (p259_chunk.sh DUELS-faza ali ročno). Izhod: /tmp/p259/duels/*.json
import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';
const zai = await ZAI.create();

const ONLY = process.argv[2] || null;

const JOBS = [
  { id: 's11_dates', q: 'Kompozit 13 DATUMSKIH celic (VRSTICA 1–13) strani Pag. 19, leto 1833 (kaskada se je začela na Pag. 17: 6. Febr ×5). Preberi VSAK datum dobesedno (d° = isti dan). Pričakovano: r1–r8 = 6. Febr/d° (morda r7 ponovno 6. Febr), r9–r13 = 13. d°. Izhod JSON: {"d1":"...",...,"d13":"...","opomba":"..."}' },
  { id: 's12_dates', q: 'Kompozit 12 DATUMSKIH celic (VRSTICA 1–12) strani Pag. 21: r1–r6 = konec leta 1833, r7–r12 = RESTART 1834! Preberi VSAK datum + letnico če je. KRITIČNO: R1 = 19. ali 12. Febr 1833? (kronologija: prejšnja stran se je končala 13. Febr!); R2 = 19. d° ali 12. April?; R5 = 19.? 10.? 26. October?; R6 = 27. Novembris?; R7 = 22. ali 27. Jänner 1834 (RESTART)?; R8 = d°; R9–R12 = 29. Jän d°×4? Izhod JSON: {"d1":"...",...,"d12":"...","restart_kje":"...","opomba":"..."}' },
  { id: 's13_dates', q: 'Kompozit 11 DATUMSKIH celic (VRSTICA 1–11) strani Pag. 23, leto 1834 v glavi (robno-številčenje 8–18!). Preberi VSAK datum dobesedno (d° = isti dan). KRITIČNO-SISTEMATIK: R1 = 5. ali 8. Febr?; R2 = 5. ali 9. Febr?; ★R3–R7 = 5. ali 10. Febr pri VSAKI (en vir pravi 5.×7-vseh, dva pa 10.×5 — preberi DAN pri vsaki posamično, številko za številko!); R8 = 9. Febr?; R9–R11 = 10. d°? Izhod JSON: {"d1":"...",...,"d11":"...","opomba":"..."}' },
  { id: 's11_r2_gosling', q: '★★★ GLAVNI IMENSKI DUEL — kompozit 4 celic vrstice 2 (6. Febr 1833, Pag. 19). Kontekst: prejšnja stran (Pag. 17) se je končala z Johann PESDIRZ Griblje 50 × Maria [Himiz] Griblje 49! ŽENIN-IME: Joh. GOSLING? Johann PESDIRZ? GUTTING? — ČRKO ZA ČRKO (G-o-s/P-e-s)! ŽENIN-VAS+HIŠA: Griblje 53 ali 33? — ŠTEVILKO ZA ŠTEVILKO! NEVESTA-IME: Maria BRING? BRINC? BRUNG? — črko za črko! NEVESTA-VAS+HIŠA: Griblje 24? Izhod JSON: {"zenin":"","crke_zenin":"","zenin_vh":"","nevesta":"","nevesta_vh":"","opomba":"..."}' },
  { id: 's12_r1_r2', q: 'Kompozit 6 celic strani Pag. 21 (1833). R1 (19.?12. Febr): ženin-ime Georg HOFFERER? HOHENAUER? — črko za črko!; ženin-vas+hiša (Nötsch? Kreuzdorf? 13?); nevesta-ime (Anna Tschesch? Stunigk?); nevesta-vas+hiša (Goritschach? Prüstein? 10?). R2: datum (19. d°? 12. April? — pazi MESEC!) + ženin-ime. Izhod JSON: {"r1_zenin":"","r1_zenin_vh":"","r1_nevesta":"","r1_nevesta_vh":"","r2_datum":"","r2_zenin":"","opomba":"..."}' },
  { id: 's12_r5_schmig', q: 'Kompozit 5 celic vrstice 5 (October 1833, Pag. 21) — ŠIMIČ-kandidat! DATUM: 19.? 10.? 26. October — DAN + MESEC! ŽENIN-IME: Georg SCHMIG? AMIZ? (~ŠIMIČ — kontekst: 1832 Peter [Simig] h56 oče Nicol Šimič + 1833 Maria [Himiz] h49!) — črko za črko! Ženin-vas+hiša (Griblje 60?). NEVESTA-IME (Katharina Harschpich? Jureisjofrig?). NEVESTA-VAS+HIŠA (Kresling? Kosting? 21?). Izhod JSON: {"datum":"","zenin":"","zenin_vh":"","nevesta":"","nevesta_vh":"","opomba":"..."}' },
  { id: 's12_r7_restart', q: '★★★ RESTART-VRSTICA — kompozit 5 celic vrstice 7 Pag. 21 (robna-št. 2, prvi 1834-vpis na tej strani?). DATUM: 22. ali 27. Jänner 1834 — DAN! + ali piše letnica 1834? ŽENIN-IME (Johann Kalmigh? Stephan Pasfrig?) — črko za črko! Ženin-vas+hiša (Vano? Vivano? 5?). NEVESTA-IME (Maria Dobrak? Kosak?). NEVESTA-VAS+HIŠA (Gordej? Gradiz? 3?). Izhod JSON: {"datum":"","leto":"","zenin":"","zenin_vh":"","nevesta":"","nevesta_vh":"","opomba":"..."}' },
  { id: 's13_r1_restart', q: 'Kompozit 5 celic vrstice 1 Pag. 23 (rob-št. 8, leto 1834 v glavi). DATUM: 5. ali 8. Febr — DAN! (post 1834 začne šele 12. 2. — koledar NE odloča, preberi SAMO ČRKE!). ŽENIN-IME (Georg Kapucžik? Koschizhigl?) — črko za črko! Ženin-vas+hiša (Gerhüpe/Gorjupa? 2?). NEVESTA-IME (Anna Vipotnik? Viqnay?). NEVESTA-VAS+HIŠA (Jeschnica? Gerhuipa? 8?). Izhod JSON: {"datum":"","zenin":"","zenin_vh":"","nevesta":"","nevesta_vh":"","opomba":"..."}' },
  { id: 's13_r6_vrh', q: '★★★ GRIBLJE-PAR — kompozit 4 celic vrstice 6 (10. Febr 1834, rob-št. 13, Pag. 23). ŽENIN-IME: Marcus VRH? VRB? VRBAN? — ČRKO ZA ČRKO! ŽENIN-VAS+HIŠA: Griblje 58 ali 68? — ŠTEVILKO ZA ŠTEVILKO! NEVESTA-IME: Maria Haraghtinich? Karafhainj? — črko za črko! NEVESTA-VAS+HIŠA: Griblje 51? Izhod JSON: {"zenin":"","zenin_vh":"","nevesta":"","nevesta_vh":"","opomba":"..."}' },
  { id: 's13_r11_marentic', q: 'Kompozit 5 celic vrstice 11 (zadnja, rob-št. 18, Pag. 23, 1834) — MARENTIČ-nit (1832 Barbara [Marentig] Otok 18)! DATUM: 10. ali 17. Febr — DAN! ŽENIN-IME (Georg Hozhoved? Koschheuel?) — črko za črko! Ženin-vas+hiša (Konyev/Kostanjevica? 13?). NEVESTA-IME (Margareth MARENTICH? Marcuteich?) — črko za črko! NEVESTA-VAS+HIŠA (Dobravlje 24 ali 29?) — ŠTEVILKO! Izhod JSON: {"datum":"","zenin":"","zenin_vh":"","nevesta":"","nevesta_vh":"","opomba":"..."}' },
];

async function run(j) {
  const out = `/tmp/p259/duels/${j.id}.json`;
  if (fs.existsSync(out) && fs.statSync(out).size > 30) { console.log(`${j.id}: skip`); return; }
  const content = [{ type: 'text', text: `Slika je KOMPOZIT POVEČANIH CELIC (označene z belimi trakovi z napisi VRSTICA/številkami) iz poročne knjige Trauungs-Buch 01738 (Podzemelj, 1833–1834, Kurrent-pisava, nemško). Vsaka celica je ločena s sivo črto. Preberi IZKLJUČNO to, kar je vprašano — dobesedno, črkovno. Kurrent: p/b, o/a, e/n, s/f, u/v, i/j so pogosto podobne — RAZLOČUJ previdno. Negotovo podaj kot alternative [~].\n${j.q}` }];
  content.push({ type: 'image_url', image_url: { url: `data:image/jpeg;base64,${fs.readFileSync(`/tmp/p259/duels/${j.id}.jpg`).toString('base64')}` } });
  for (let a = 1; a <= 4; a++) {
    try {
      const r = await zai.chat.completions.createVision({
        messages: [{ role: 'user', content }],
        temperature: 0.1, max_tokens: 900, thinking: { type: 'disabled' },
      });
      fs.writeFileSync(out, r.choices[0].message.content || '');
      console.log(`${j.id}: OK`);
      return;
    } catch (e) { console.log(`${j.id}: a${a} ${String(e).slice(0,70)}`); await new Promise(r2=>setTimeout(r2,2500)); }
  }
  console.log(`${j.id}: FAIL`);
}
for (const j of JOBS) {
  if (ONLY && j.id !== ONLY) continue;
  await run(j);
  await new Promise(r=>setTimeout(r,1200));
}
