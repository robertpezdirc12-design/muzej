// P240 — VLM pass-3: nodat trakov (številčenje+datumi) + pass-3b ultra-zoom bloki
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

const KROPS = '/tmp/p240/krops';

const PROMPTS = {
  // — pass-3: nodat trakov —
  's50_nodat': `To je ULTRA-ZOOM levega roba poročne knjige 04455 (Podzemelj). ZGORAJ: tail-vpisi leta 1882 (številke okvirno 24.–26. + datumi novembra 1882). NA DNU: statistična vrsta + VELIKE številke »1883« + restart "1." (21. Januar?). Preberi TOČNO vse številke in datume (Kurent: "11" = dve navpični črti; "12" = črta + c-kotika).
Izhod SAMO JSON: {"tailRows": [{"no": "...", "date": "...", "note": "..."}], "bigHeadings": ["..."], "restart1883": [{"no": "...", "date": "...", "note": "..."}], "pageNote": "..."}`,
  's51_nodat': `To je ULTRA-ZOOM levega roba poročne knjige 04455 (Podzemelj), leto 1883 nadaljevanje. KRITIČNO: preberi zaporedne številke TOČNO (ali je prva "2." ali "1."? Kurent 2 = en navpični lok; 1 = ena črta) in datume (Jänner/februar/April).
Izhod SAMO JSON: {"rows": [{"no": "...", "date": "...", "note": "..."}], "pageNote": "..."}`,
  's52_nodat': `To je ULTRA-ZOOM levega roba poročne knjige 04455 (Podzemelj), TAIL leta 1883. Preberi TOČNO zaporedne številke (okvirno 8.–12.) in datume (Mai/August/September/October). Kurent "8" = dva loka nad seboj; "9" = lok + rep.
Izhod SAMO JSON: {"rows": [{"no": "...", "date": "...", "note": "..."}], "pageNote": "..."}`,

  // — pass-3b: ultra-zoom bloki —
  's50_restart_bot': `To je DNO razprtega lista poročne knjige 04455 (Podzemelj): zadnji tail-vpis 1882 + statistična vrsta + VELIKE številke »1883« + PRVI vpis leta 1883 (restart zap. št. = 1). Prepiši restart-vrstico POPOLNOSTI: zap. št., datum (21. Januar?), ženin (ime + priimek + stan + hiša/kraj + starost), starši ženina, nevesta, nevestina starša, priče, duhovnik. Statistično vrsto prepiši TOČNO (kaj pomeni: letnica 1883 ali številke stanov?).
Izhod SAMO JSON: {"tailLast": {"no": "...", "date": "...", "groom": "...", "bride": "..."}, "statsRow": "...", "bigHeadings": ["..."], "restart1883": {"no": "...", "date": "...", "groom": "...", "groomPlace": "...", "groomParents": "...", "bride": "...", "bridePlace": "...", "brideParents": "...", "witnesses": "...", "priest": "..."}, "pageNote": "..."}`,

  's51_v4_pezdirc': `To je ULTRA-ZOOM ene vrstice poročne knjige 04455 (Podzemelj, leto 1883) — ženin naj bi bil Miha PEZDIRC, Podzemelj 3, ~30 let (Jänner 28.). Prepiši vrstico POPOLNOSTI: zap. št., datum, ženin (ime + priimek + stan + hiša + starost), starši ženina, nevesta (ime + priimek + stan + hiša + starost), nevestina starša, priče, duhovnik. KRITIČNO: priimek ženina črka-za-črko (PEZDIRC/Pegdirc/Pezdic?).
Izhod SAMO JSON: {"no": "...", "date": "...", "groom": "...", "groomPlace": "...", "groomParents": "...", "bride": "...", "bridePlace": "...", "brideParents": "...", "witnesses": "...", "priest": "...", "pageNote": "..."}`,

  's51_v5_v6_blok': `To sta ULTRA-ZOOM dve vrstici poročne knjige 04455 (Podzemelj, leto 1883): (a) Jurij/Juri Radovič [~] — hiša/kraj DUEL: "Griblje 13" vs "z. Segeselo №2 Pf. Vinica"; (b) Peter Petlebec/Hlebec — GRIBLJE 2, ~35 let (februar 4.). Prepiši obe vrstici POPOLNOSTI (zap. št., datum, ženin + stan + hiša + starost, starši ženina, nevesta + hiša, nevestina starša, priče, duhovnik). KRITIČNO: hišni kraji črka-za-črko — je (a) res "Griblje 13" ali "Pf. Vinica"? Je (b) res "Griblje 2"?
Izhod SAMO JSON: {"rows": [{"no": "...", "date": "...", "groom": "...", "groomPlace": "...", "groomParents": "...", "bride": "...", "bridePlace": "...", "brideParents": "...", "witnesses": "...", "priest": "...", "note": "..."}], "pageNote": "..."}`,

  's51_v2_v3_blok': `To sta ULTRA-ZOOM prvi dve vrstici poročne knjige 04455 (Podzemelj, leto 1883, po restartu-1 na prejšnjem listu): zap. št. verjetno 2. in 3. (oba Jänner 28.). Prepiši obe vrstici POPOLNOSTI: zap. št., datum, ženin (ime + priimek + stan + hiša + starost), starši ženina, nevesta + hiša + starost, nevestina starša, priče, duhovnik. KRITIČNO: zap. številki TOČNO (2. in 3.?).
Izhod SAMO JSON: {"rows": [{"no": "...", "date": "...", "groom": "...", "groomPlace": "...", "groomParents": "...", "bride": "...", "bridePlace": "...", "brideParents": "...", "witnesses": "...", "priest": "...", "note": "..."}], "pageNote": "..."}`,

  's51_v7_blok': `To je ULTRA-ZOOM zadnja vrstica poročne knjige 04455 (Podzemelj, leto 1883, April 22.) — zap. št. verjetno 7. Martin Jurejevič × Maria Zmidar/Zidar. Prepiši vrstico POPOLNOSTI. KRITIČNO: nevestina mati (roj. Pezdič/PEZDIRC?).
Izhod SAMO JSON: {"no": "...", "date": "...", "groom": "...", "groomPlace": "...", "groomParents": "...", "bride": "...", "bridePlace": "...", "brideParents": "...", "witnesses": "...", "priest": "...", "pageNote": "..."}`,

  's52_v10_milek': `To je ULTRA-ZOOM vrstica poročne knjige 04455 (Podzemelj, TAIL 1883, 26. August) — zap. št. verjetno 10. Nevesta naj bi bila Margaretha MILEK/Milleh. Prepiši vrstico POPOLNOSTI: zap. št., datum, ženin (ime + priimek + stan + hiša + starost), starši ženina, nevesta (ime + priimek + stan + hiša + starost), nevestina starša, priče, duhovnik. KRITIČNO: nevestin priimek črka-za-črko (MILEK/Milleh/Milech/MILIČ?) + njena hiša/kraj (Konec? Graditz? Vend?).
Izhod SAMO JSON: {"no": "...", "date": "...", "groom": "...", "groomPlace": "...", "groomParents": "...", "bride": "...", "bridePlace": "...", "brideParents": "...", "witnesses": "...", "priest": "...", "pageNote": "..."}`,

  's52_v8_v9_blok': `To sta ULTRA-ZOOM prvi dve vrstici poročne knjige 04455 (Podzemelj, TAIL 1883): zap. št. 8. in 9. (oba 13. Mai). Prepiši obe vrstici POPOLNOSTI: zap. št., datum, ženin (ime + priimek + stan + hiša + starost), starši ženina, nevesta + hiša + starost, nevestina starša, priče, duhovnik. KRITIČNO: priimek ženina vrstice 8 (Hvalc/Hrovalj/Straus?) + njegova hiša (Kaplitz 8?) + nevesta vrstice 9 (Hrovalj — ISTA-hiša-kot-ženin-8?).
Izhod SAMO JSON: {"rows": [{"no": "...", "date": "...", "groom": "...", "groomPlace": "...", "groomParents": "...", "bride": "...", "bridePlace": "...", "brideParents": "...", "witnesses": "...", "priest": "...", "note": "..."}], "pageNote": "..."}`,

  's52_v11_blok': `To je ULTRA-ZOOM vrstica poročne knjige 04455 (Podzemelj, TAIL 1883, 9. September) — zap. št. verjetno 11. Prepiši vrstico POPOLNOSTI: zap. št., datum, ženin (ime + priimek + stan + hiša + starost), starši ženina, nevesta + hiša + starost (Hrižan?), nevestina starša, priče, duhovnik.
Izhod SAMO JSON: {"no": "...", "date": "...", "groom": "...", "groomPlace": "...", "groomParents": "...", "bride": "...", "bridePlace": "...", "brideParents": "...", "witnesses": "...", "priest": "...", "pageNote": "..."}`,

  's52_v12_straus': `To je ULTRA-ZOOM zadnja vrstica poročne knjige 04455 (Podzemelj, TAIL 1883, 28. October) — zap. št. verjetno 12. Ženin naj bi bil Peter Straus, Gertsitš/Gerenč 5, nevesta Maria Pegitč/Pepec, Graditz 2. Prepiši vrstico POPOLNOSTI. KRITIČNO: priimki + hišne številke črka-za-črko (Straus? Gertsitš 5? Pegitč/Pepec? Graditz 2?).
Izhod SAMO JSON: {"no": "...", "date": "...", "groom": "...", "groomPlace": "...", "groomParents": "...", "bride": "...", "bridePlace": "...", "brideParents": "...", "witnesses": "...", "priest": "...", "pageNote": "..."}`,
};

async function readCrop(zai, name) {
  const b64 = fs.readFileSync(`${KROPS}/${name}.jpg`).toString('base64');
  const call = zai.chat.completions.createVision({
    messages: [{ role: 'user', content: [
      { type: 'text', text: PROMPTS[name] },
      { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${b64}` } }
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
    const out = `${KROPS}/${name}.pass3.json`;
    if (fs.existsSync(out)) { console.log(' obstoji:', out); continue; }
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
      console.log('OK');
    } catch (e) {
      fs.writeFileSync(out.replace('.json', '.raw.txt'), content, 'utf-8');
      console.log('RAW:', e.message.slice(0, 50));
    }
  }
}
main().catch(e => { console.error('FATAL', e.message); process.exit(1); });
