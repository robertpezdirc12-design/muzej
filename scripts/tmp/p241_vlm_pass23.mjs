// P241 — VLM pass-2 (polovice) + pass-3 (nodat številčenje) + pass-3b (ultra-zoom bloki)
// poročna 04455, leto 1882 = 4/13 — reconciliacija s P240 (s50-tail #24–26 1:1!)
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

const KROPS = '/tmp/p241/krops';

const PROMPTS = {
  // ---------- PASS-2: polovice ----------
  s45_levo_cel: `To je LEVA polovica razprtega lista poročne knjige 04455 župnije Podzemelj. NA ZAČETKU: VELIKE številke »1882« + RESTART zaporedne številke = 1 (leto 1882 se začne — vpisi 1–4, Jänner/Februar 1882). Prepiši VSAKO vrstico: (1) zap. št. TOČNO (KRITIČNO: je prva vrstica TOČNO »1.«?), (2) datum (dan + mesec), (3) ženin (ime + priimek + stan + starost), (4) hiša/kraj ženina, (5) starši ženina. Posebno pozorno na vpis 1 (Anton Tasie? Mokrine 1?) in vpis 3/4 (Dragoš/Prodnik Krasinec 7 / Draginja vas 15?).
Negotovo = [~], neberljivo = [?]. Ne izmišljuj.
Izhod: SAMO veljaven JSON:
{"rows": [{"no": "...", "date": "...", "groom": "...", "age": "...", "place": "...", "parents": "...", "note": "..."}], "bigHeadings": ["..."], "restartNote": "ali je zap. št. prve vrstice TOČNO 1?", "pageNote": "..."}`,

  s45_desno_cel: `To je DESNA polovica razprtega lista poročne knjige 04455 župnije Podzemelj, leto 1882 vpisi 1–4. Za VSAKO vrstico: (1) zap. št., (2) datum, (3) nevesta (ime + priimek + stan + starost), (4) hiša/kraj neveste (posebno pozorno na vpis 1: Anna Cvet — je hiša TOČNO »Griblje 35«? ali 33/36/38-duel?), (5) nevestine starše, (6) priče, (7) duhovnik.
Negotovo = [~], neberljivo = [?]. Ne izmišljuj.
Izhod: SAMO veljaven JSON:
{"rows": [{"no": "...", "date": "...", "bride": "...", "age": "...", "place": "...", "parents": "...", "witnesses": "...", "priest": "...", "note": "..."}], "pageNote": "..."}`,

  s46_levo_cel: `To je LEVA polovica razprtega lista poročne knjige 04455 župnije Podzemelj, leto 1882 (zap. št. verjetno 5.–8., Februar 1882). Prepiši VSAKO vrstico: (1) zap. št. TOČNO, (2) datum, (3) ženin (ime + priimek + stan + starost), (4) hiša/kraj ženina, (5) starši ženina. Posebno pozorno na vpis 8: Johan Pazeš/Pazek? — hiša TOČNO »Griblje 38«? (½-Güblner-Knecht?) — in datume 12./15. Februar.
Negotovo = [~], neberljivo = [?]. Ne izmišljuj.
Izhod: SAMO veljaven JSON:
{"rows": [{"no": "...", "date": "...", "groom": "...", "age": "...", "place": "...", "parents": "...", "note": "..."}], "bigHeadings": ["..."], "pageNote": "..."}`,

  s46_desno_cel: `To je DESNA polovica razprtega lista poročne knjige 04455 župnije Podzemelj, leto 1882 vpisi 5–8. Za VSAKO vrstico: (1) zap. št., (2) datum, (3) nevesta (ime + priimek + stan + starost), (4) hiša/kraj neveste (posebno pozorno na vpis 8: Anna Dragos/Drugoš? — je hiša TOČNO »Griblje 12«? starost?), (5) nevestine starše, (6) priče, (7) duhovnik.
Negotovo = [~], neberljivo = [?]. Ne izmišljuj.
Izhod: SAMO veljaven JSON:
{"rows": [{"no": "...", "date": "...", "bride": "...", "age": "...", "place": "...", "parents": "...", "witnesses": "...", "priest": "...", "note": "..."}], "pageNote": "..."}`,

  s47_levo_cel: `To je LEVA polovica razprtega lista poročne knjige 04455 župnije Podzemelj, leto 1882 (zap. št. verjetno 9.–12., Februar 1882). Prepiši VSAKO vrstico: (1) zap. št. TOČNO, (2) datum (vpis 9: je 9. ali 15. Februar?), (3) ženin (ime + priimek + stan + starost), (4) hiša/kraj ženina, (5) starši ženina. KRITIČNO vpis 9: Georg PEZDIRC — Podzemelj 3? — in ali je tudi nevesta PEZDIRC (Margaretha)? + vpis 10: Johann Nagert — »Grič? Pfarre Lipnik?«.
Negotovo = [~], neberljivo = [?]. Ne izmišljuj.
Izhod: SAMO veljaven JSON:
{"rows": [{"no": "...", "date": "...", "groom": "...", "age": "...", "place": "...", "parents": "...", "note": "..."}], "pageNote": "..."}`,

  s47_desno_cel: `To je DESNA polovica razprtega lista poročne knjige 04455 župnije Podzemelj, leto 1882 vpisi 9–12. Za VSAKO vrstico: (1) zap. št., (2) datum, (3) nevesta (ime + priimek + stan + starost), (4) hiša/kraj neveste (KRITIČNO vpis 9: Margaretha PEZDIRC — hiša? »Prost. 23«? ali Podzemelj?), (5) nevestine starše (vpis 9: kdo so starši — PEZDIRC?), (6) priče, (7) duhovnik.
Negotovo = [~], neberljivo = [?]. Ne izmišljuj.
Izhod: SAMO veljaven JSON:
{"rows": [{"no": "...", "date": "...", "bride": "...", "age": "...", "place": "...", "parents": "...", "witnesses": "...", "priest": "...", "note": "..."}], "pageNote": "..."}`,

  s48_levo_cel: `To je LEVA polovica razprtega lista poročne knjige 04455 župnije Podzemelj, leto 1882 (zap. št. verjetno 13.–17., Februar–Mai). Prepiši VSAKO vrstico: (1) zap. št. TOČNO, (2) datum, (3) ženin (ime + priimek + stan + starost), (4) hiša/kraj ženina, (5) starši ženina. Posebno pozorno: vpis 13 (Ivan Hrovič? Dolence 24?), vpis 15 (Matthias Jakopič? — TOČNO »Griblje 13«? starost 25?), vpis 16 (Michael PEZDIRC? — TOČNO »Prusi 3«? ali Prusi nec.? starost 42?).
Negotovo = [~], neberljivo = [?]. Ne izmišljuj.
Izhod: SAMO veljaven JSON:
{"rows": [{"no": "...", "date": "...", "groom": "...", "age": "...", "place": "...", "parents": "...", "note": "..."}], "pageNote": "..."}`,

  s48_desno_cel: `To je DESNA polovica razprtega lista poročne knjige 04455 župnije Podzemelj, leto 1882 vpisi 13–17. Za VSAKO vrstico: (1) zap. št., (2) datum, (3) nevesta (ime + priimek + stan + starost), (4) hiša/kraj neveste (KRITIČNO: vpis 13 Katharina Brinc? — TOČNO »Griblje 56«? starost 48?; vpis 15 Maria PEZDIRC? — TOČNO »Griblje 52«? starost 31?; vpis 16 Anna Jakopič? — TOČNO »Griblje 8«? starost 16?), (5) nevestine starše, (6) priče, (7) duhovnik.
Negotovo = [~], neberljivo = [?]. Ne izmišljuj.
Izhod: SAMO veljaven JSON:
{"rows": [{"no": "...", "date": "...", "bride": "...", "age": "...", "place": "...", "parents": "...", "witnesses": "...", "priest": "...", "note": "..."}], "pageNote": "..."}`,

  s49_levo_cel: `To je LEVA polovica razprtega lista poročne knjige 04455 župnije Podzemelj, leto 1882 (zap. št. verjetno 18.–23., Juli–November). Prepiši VSAKO vrstico: (1) zap. št. TOČNO, (2) datum, (3) ženin (ime + priimek + stan + starost), (4) hiša/kraj ženina, (5) starši ženina. Posebno pozorno: vpis 23 (Nicolaus Lesiro/Lesko? — TOČNO »Griblje 1«? starost 50?) + vpis 21 (Daniel Škrca?).
Negotovo = [~], neberljivo = [?]. Ne izmišljuj.
Izhod: SAMO veljaven JSON:
{"rows": [{"no": "...", "date": "...", "groom": "...", "age": "...", "place": "...", "parents": "...", "note": "..."}], "pageNote": "..."}`,

  s49_desno_cel: `To je DESNA polovica razprtega lista poročne knjige 04455 župnije Podzemelj, leto 1882 vpisi 18–23. Za VSAKO vrstico: (1) zap. št., (2) datum, (3) nevesta (ime + priimek + stan + starost), (4) hiša/kraj neveste (KRITIČNO: vpis 18 Anne PEZDIRC? — TOČNO »Otok 1«?; vpis 21 Anne PEZDIRC? — TOČNO »Krupšiše 4«? ali drugače?; vpis 23 Katharina Škrce? — TOČNO »Griblje 10«?), (5) nevestine starše, (6) priče, (7) duhovnik.
Negotovo = [~], neberljivo = [?]. Ne izmišljuj.
Izhod: SAMO veljaven JSON:
{"rows": [{"no": "...", "date": "...", "bride": "...", "age": "...", "place": "...", "parents": "...", "witnesses": "...", "priest": "...", "note": "..."}], "pageNote": "..."}`,

  // ---------- PASS-3: nodat številčenje ----------
  s45_nodat: `To je LEVI ROB (številčni stolpec) razprtega lista poročne knjige 04455. Preberi TOČNO vse zaporedne številke od zgoraj navzdol (mali zapisi). So to 1, 2, 3, 4 (BREZ preskokov/dvojic)? So kje prečrtane številke ali popravki? Izhod: SAMO veljaven JSON: {"numbers": ["..."], "skips": "ali so preskoki? opisi", "marginalia": "opombe na robu, če so", "note": "..."}`,

  s46_nodat: `To je LEVI ROB (številčni stolpec) razprtega lista poročne knjige 04455, leto 1882. Preberi TOČNO vse zaporedne številke od zgoraj navzdol. Pričakovano: 5, 6, 7, 8 (BREZ preskokov)? Izhod: SAMO veljaven JSON: {"numbers": ["..."], "skips": "opis ali prazno", "marginalia": "opombe", "note": "..."}`,

  s47_nodat: `To je LEVI ROB (številčni stolpec) razprtega lista poročne knjige 04455, leto 1882. Preberi TOČNO vse zaporedne številke od zgoraj navzdol. Pričakovano: 9, 10, 11, 12 (BREZ preskokov)? Izhod: SAMO veljaven JSON: {"numbers": ["..."], "skips": "opis ali prazno", "marginalia": "opombe", "note": "..."}`,

  s48_nodat: `To je LEVI ROB (številčni stolpec) razprtega lista poročne knjige 04455, leto 1882. Preberi TOČNO vse zaporedne številke od zgoraj navzdol. Pričakovano: 13, 14, 15, 16, 17 (BREZ preskokov)? Izhod: SAMO veljaven JSON: {"numbers": ["..."], "skips": "opis ali prazno", "marginalia": "opombe", "note": "..."}`,

  s49_nodat: `To je LEVI ROB (številčni stolpec) razprtega lista poročne knjige 04455, leto 1882. Preberi TOČNO vse zaporedne številke od zgoraj navzdol. Pričakovano: 18, 19, 20, 21, 22, 23 (BREZ preskokov)? Izhod: SAMO veljaven JSON: {"numbers": ["..."], "skips": "opis ali prazno", "marginalia": "opombe", "note": "..."}`,

  // ---------- PASS-3b: ultra-zoom ----------
  p01_s45_r1_grib35: `ULTRA-ZOOM vrstice vpisa 1 leta 1882 (RESTART!) poročne knjige 04455 župnije Podzemelj. Prepiši črka-za-črko: zap. št. (TOČNO »1.«?), datum (Jänner 21.? ali Februar?), ženin (Anton Tasie/Tošič? Mokrine 1? starost 24?), starši ženina, nevesta (Anna Cvet/Cvec?), njena hiša (KRITIČNO: TOČNO »Griblje 35«? ali 33/36/38? — preberi ŠTEVILKO števkо-po-števko!), njena starost (19?), njene starši, priče, duhovnik. Negotovo = [~]. Izhod: SAMO veljaven JSON: {"no": "...", "date": "...", "groom": "...", "groomParents": "...", "bride": "...", "brideHouse": "...", "brideHouseDigits": "števke hišne št.", "brideAge": "...", "brideParents": "...", "witnesses": "...", "priest": "...", "note": "..."}`,

  p02_s45_r2: `ULTRA-ZOOM vrstice vpisa 2 leta 1882 poročne knjige 04455. Prepiši črka-za-črko: zap. št., datum (23. Februar? ali drugače — preberi dvakrat!), ženin (Franz Šikar/Šilar? Mokre 24?), nevesta (Gertrud Rozman? Mokre 6?), starosti, starši, priče, duhovnik. Negotovo = [~]. Izhod: SAMO veljaven JSON: {"no": "...", "date": "...", "groom": "...", "bride": "...", "witnesses": "...", "priest": "...", "note": "..."}`,

  p03_s46_r8_grib: `ULTRA-ZOOM vrstice vpisa 8 leta 1882 poročne knjige 04455 župnije Podzemelj. Prepiši črka-za-črko: zap. št., datum (15. Februar?), ženin (Johan Pazeš/Pazek/Božik? — črka-za-črko!), njegova hiša (KRITIČNO: TOČNO »Griblje 38«? — števkо-po-števko! ½-Güblner-Knecht?), starost 24?, njegovi starši, nevesta (Anna Dragos/Drugoš? — črka-za-črko!), njena hiša (KRITIČNO: TOČNO »Griblje 12«? — števkо-po-števko!), njena starost (23?), njeni starši, priče, duhovnik. Negotovo = [~]. Izhod: SAMO veljaven JSON: {"no": "...", "date": "...", "groom": "...", "groomHouse": "...", "groomHouseDigits": "...", "groomAge": "...", "groomParents": "...", "bride": "...", "brideHouse": "...", "brideHouseDigits": "...", "brideAge": "...", "brideParents": "...", "witnesses": "...", "priest": "...", "note": "..."}`,

  p04_s47_r9_pezdirc: `ULTRA-ZOOM vrstice vpisa 9 leta 1882 poročne knjige 04455 župnije Podzemelj — KRITIČNO: OBA partnerja verjetno PEZDIRC! Prepiši črka-za-črko: zap. št., datum (9. ali 15. Februar — preberi dvakrat!), ženin (Georg PEZDIRC? — črka-za-črko P-e-z-d-i-r-c, NI Pegdirc!), njegova hiša (Podzemelj 3?), starost (32?), njegovi starši, nevesta (Margaretha PEZDIRC? — isti priimek?), njena hiša (Podzemelj 3 tudi? ali Prostojna 23? ali ½-Guttenberg-Gütl?), njena starost (20?), njeni starši, priče, duhovnik. Negotovo = [~]. Izhod: SAMO veljaven JSON: {"no": "...", "date": "...", "groom": "...", "groomHouse": "...", "groomAge": "...", "groomParents": "...", "bride": "...", "brideHouse": "...", "brideAge": "...", "brideParents": "...", "witnesses": "...", "priest": "...", "note": "..."}`,

  p05_s47_r9_datum: `ULTRA-ZOOM DATUM vpisa 9 leta 1882 poročne knjige 04455. Preberi datum dvakrat (dan + mesec): je »9. Febr.« ali »15. Febr.« ali drugače? Prva številka: ena-kroglja (9) ali dve-navpični (15)? Izhod: SAMO veljaven JSON: {"date": "...", "dayReading1": "...", "dayReading2": "...", "verdict": "9|15|drugo", "note": "..."}`,

  p06_s48_r13_grib56: `ULTRA-ZOOM vrstice vpisa 13 leta 1882 poročne knjige 04455 župnije Podzemelj. Prepiši črka-za-črko: zap. št., datum (13. Februar?), ženin (Ivan/Johann Hrovič/Hvalc? Dolence 24? starost 36?), njegovi starši, nevesta (Katharina Brinc/Brinec? — črka-za-črko!), njena hiša (KRITIČNO: TOČNO »Griblje 56«? — števkо-po-števko!), njena starost (KRITIČNO: 48? ali 18/41/44 — preberi dvakrat!), njeni starši, priče, duhovnik. Negotovo = [~]. Izhod: SAMO veljaven JSON: {"no": "...", "date": "...", "groom": "...", "groomParents": "...", "bride": "...", "brideHouse": "...", "brideHouseDigits": "...", "brideAge": "...", "brideAgeReading2": "...", "brideParents": "...", "witnesses": "...", "priest": "...", "note": "..."}`,

  p07_s48_r15_grib: `ULTRA-ZOOM vrstice vpisa 15 leta 1882 poročne knjige 04455 župnije Podzemelj. Prepiši črka-za-črko: zap. št., datum (19. Februar?), ženin (Matthias Jakopič/Jakobitsch? — črka-za-črko!), njegova hiša (KRITIČNO: TOČNO »Griblje 13«? — števkо-po-števko!), starost (25?), njegovi starši, nevesta (Maria PEZDIRC/Pegdirc? — črka-za-črko, preveri 2. črko z/e!), njena hiša (KRITIČNO: TOČNO »Griblje 52«? — števkо-po-števko!), njena starost (31?), njeni starši, priče, duhovnik. Negotovo = [~]. Izhod: SAMO veljaven JSON: {"no": "...", "date": "...", "groom": "...", "groomHouse": "...", "groomHouseDigits": "...", "groomAge": "...", "groomParents": "...", "bride": "...", "brideHouse": "...", "brideHouseDigits": "...", "brideAge": "...", "brideParents": "...", "witnesses": "...", "priest": "...", "note": "..."}`,

  p08_s48_r16_pezdirc: `ULTRA-ZOOM vrstice vpisa 16 leta 1882 poročne knjige 04455 župnije Podzemelj. Prepiši črka-za-črko: zap. št., datum (Mai 14.?), ženin (Michael PEZDIRC/Pegdirc? — črka-za-črko!), njegova hiša (TOČNO: »Prusi 3«? ali Prusi nec.? kaj je pripis?), starost (42?), njegovi starši, nevesta (Anna Jakopič?), njena hiša (KRITIČNO: TOČNO »Griblje 8«? — števkо-po-števko!), njena starost (KRITIČNO: 16? — preberi dvakrat!), njeni starši, priče, duhovnik. Negotovo = [~]. Izhod: SAMO veljaven JSON: {"no": "...", "date": "...", "groom": "...", "groomHouse": "...", "groomAge": "...", "groomParents": "...", "bride": "...", "brideHouse": "...", "brideHouseDigits": "...", "brideAge": "...", "brideAgeReading2": "...", "brideParents": "...", "witnesses": "...", "priest": "...", "note": "..."}`,

  p09_s49_r18_pezdirc: `ULTRA-ZOOM vrstice vpisa 18 leta 1882 poročne knjige 04455 župnije Podzemelj. Prepiši črka-za-črko: zap. št., datum (Juli 2.?), ženin (Nicolaus Jablénik/Jablonšek? hiša Brusinec 13? ali Brošinec?), njegovi starši, nevesta (Anne PEZDIRC? — črka-za-črko!), njena hiša (KRITIČNO: TOČNO »Otok 1«? — števkо-po-števko!), njena starost (22?), njeni starši, priče, duhovnik. Negotovo = [~]. Izhod: SAMO veljaven JSON: {"no": "...", "date": "...", "groom": "...", "groomHouse": "...", "groomAge": "...", "groomParents": "...", "bride": "...", "brideHouse": "...", "brideHouseDigits": "...", "brideAge": "...", "brideParents": "...", "witnesses": "...", "priest": "...", "note": "..."}`,

  p10_s49_r21_pezdirc: `ULTRA-ZOOM vrstice vpisa 21 leta 1882 poročne knjige 04455 župnije Podzemelj. Prepiši črka-za-črko: zap. št., datum (30. Juli?), ženin (Daniel Škrca/Škerca? — črka-za-črko! kje je njegova hiša?), njegovi starši, nevesta (Anne PEZDIRC? — črka-za-črko!), njena hiša (KRITIČNO: kaj piše — »Krupšiše 4«? »Krupšiše«? druga vas? — števkо-po-števko!), njena starost (36?), njeni starši, priče, duhovnik. Negotovo = [~]. Izhod: SAMO veljaven JSON: {"no": "...", "date": "...", "groom": "...", "groomHouse": "...", "groomAge": "...", "groomParents": "...", "bride": "...", "brideHouse": "...", "brideHouseDigits": "...", "brideAge": "...", "brideParents": "...", "witnesses": "...", "priest": "...", "note": "..."}`,

  p11_s49_r23_grib: `ULTRA-ZOOM vrstice vpisa 23 leta 1882 poročne knjige 04455 župnije Podzemelj. Prepiši črka-za-črko: zap. št., datum (November 12.?), ženin (Nicolaus Lesiro/Lesko/Leskovšek? — črka-za-črko!), njegova hiša (KRITIČNO: TOČNO »Griblje 1«? — števkо-po-števko! ½-gütlbua?), starost (50?), njegovi starši, nevesta (Katharina Škrce/Škerce?), njena hiša (KRITIČNO: TOČNO »Griblje 10«? — števkо-po-števko!), njena starost (30?), njeni starši, priče, duhovnik. Negotovo = [~]. Izhod: SAMO veljaven JSON: {"no": "...", "date": "...", "groom": "...", "groomHouse": "...", "groomHouseDigits": "...", "groomAge": "...", "groomParents": "...", "bride": "...", "brideHouse": "...", "brideHouseDigits": "...", "brideAge": "...", "brideParents": "...", "witnesses": "...", "priest": "...", "note": "..."}`,

  p12_s45_meja_top: `To je ZGORNJI PAS razprtega lista (skupna št. 45) poročne knjige 04455 župnije Podzemelj — MEJA-LET! Odgovori: (1) Vidiš ZGORAJ tail-vpise leta 1881 (koliko in kateri datumi)? (2) Vidiš VELIKE številke »1882« — točno kje (glava strani ali pred določeno vrstico)? (3) Katera je prva vrstica z zap. št. »1.« (RESTART-1882)? (4) Foliacija/pag. št. če je vidna. Izhod: SAMO veljaven JSON: {"tail1881": [{"no": "...", "date": "...", "groom": "...", "bride": "...", "note": "..."}], "bigHeadings": ["..."], "headingPosition": "kje točno", "restartRow": "katera vrstica je 1.", "folio": "pag če viden", "note": "..."}`,
};

async function readCrop(zai, name) {
  const b64 = fs.readFileSync(`${KROPS}/${name}.png`).toString('base64');
  const call = zai.chat.completions.createVision({
    messages: [{ role: 'user', content: [
      { type: 'text', text: PROMPTS[name] },
      { type: 'image_url', image_url: { url: `data:image/png;base64,${b64}` } }
    ]}],
    thinking: { type: 'disabled' }
  });
  const completion = await Promise.race([
    call,
    new Promise((_, rej) => setTimeout(() => rej(new Error('TIMEOUT 240s')), 240000))
  ]);
  return completion.choices[0]?.message?.content ?? '';
}

async function main() {
  const names = process.argv.slice(2).length ? process.argv.slice(2) : Object.keys(PROMPTS);
  const zai = await ZAI.create();
  for (const name of names) {
    const out = `${KROPS}/${name}.vlm.json`;
    if (fs.existsSync(out)) { console.log(' obstoji:', name); continue; }
    if (!fs.existsSync(`${KROPS}/${name}.png`)) { console.log(' MANJKA PNG:', name); continue; }
    process.stdout.write(` ${name} ... `);
    let content = '';
    for (let attempt = 1; attempt <= 2; attempt++) {
      try { content = await readCrop(zai, name); break; }
      catch (e) { console.log(`poskus ${attempt} NAPAKA: ${e.message}`); }
    }
    const clean = content.replace(/^```json\n?/, '').replace(/\n?```$/, '').trim();
    try {
      const parsed = JSON.parse(clean);
      fs.writeFileSync(out, JSON.stringify(parsed, null, 1), 'utf-8');
      const rows = parsed.rows?.length ?? parsed.numbers?.length ?? (parsed.tail1881?.length ?? 0);
      console.log(`OK vrstice=${rows}`);
    } catch (e) {
      fs.writeFileSync(out.replace('.vlm.json', '.raw.txt'), content, 'utf-8');
      console.log('RAW:', e.message.slice(0, 50));
    }
  }
}
main().catch(e => { console.error('FATAL', e.message); process.exit(1); });
