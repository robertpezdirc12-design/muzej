// P239 — VLM pass-3b: Griblje bloki ultra-zoom
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

const KROPS = '/tmp/p239/krops';

const PROMPTS = {
  's53_v1_v2_pezdirc': `To je ULTRA-ZOOM vrstic 1–2 poročne knjige 04455 (Podzemelj), 6. Februar 1884. DVA ženina: Martin Pezdirč in Mathias Pezdirč (VERJETNO BRATA!). Prepiši za vsakega TOČNO: (1) polno ime + priimek (Pezdirc? Pegdirc? Pezdirč?), (2) stan/lastništvo (¼-Gütl? guiltnerjej? ledinec?), (3) VASEN/BEJAKO + hišna številka (KRITIČNO: ali piše "Podkraj 1", "Oslob 1", "Otok 1" ali kaj drugega? — črka-za-črko!), (4) starost, (5) starši (oče + mati, mati roj.?). Kurrent: "Os" vs "Pod" — poglej natančno.
Izhod SAMO JSON: {"rows": [{"no": "...", "groom": "...", "age": "...", "status": "...", "village": "...", "houseNo": "...", "parents": "...", "note": "..."}], "pageNote": "..."}`,

  's54_v6_v7_blok': `To je ULTRA-ZOOM vrstic 6–7 poročne knjige 04455 (Podzemelj), Februar 1884. VRSTICA 6: ženin Johann Simec GRIBLJE 54 × nevesta Anna (Struč? Strucli?) GRIBLJE 44 — TO je Griblje-poroka! VRSTICA 7: ženin (Nikolaus Jakljevič?) × nevesta Anna (Hrizan? Prizan?). Prepiši za obe vrstici TOČNO: imena, starosti, stan, hišne številke (Griblje 54? Griblje 44? ½-Griblje?), starši (oče + mati roj.), priče, duhovnik. Kurrent "44" vs "34" — poglej natančno.
Izhod SAMO JSON: {"rows": [{"no": "...", "groom": "...", "groomPlace": "...", "bride": "...", "bridePlace": "...", "parentsGroom": "...", "parentsBride": "...", "witnesses": "...", "priest": "...", "note": "..."}], "pageNote": "..."}`,

  's54_v9_v10_blok': `To je ULTRA-ZOOM vrstic 9–10 poročne knjige 04455 (Podzemelj), Februar 1884. VRSTICA 9: ženin Peter (Toič?) Borinja/Boginja vas 12. VRSTICA 10: ženin Peter (Jakobčič?) Ceroviči/Cerovica 17 × nevesta Katharina (Kupanic? Supančič?) — KRITIČNO: kje je nevesta rojena/hodila? (Griblje-dekla?). Prepiši obe vrstici črka-za-črko: imena, starosti, vasi+hišne številke, starši, priče, duhovnik.
Izhod SAMO JSON: {"rows": [{"no": "...", "groom": "...", "groomPlace": "...", "bride": "...", "bridePlace": "...", "parentsGroom": "...", "parentsBride": "...", "witnesses": "...", "priest": "...", "note": "..."}], "pageNote": "..."}`,

  's56_v15_nevesta': `To je ULTRA-ZOOM neveste vpisa 15 (tail-1884) poročne knjige 04455. Nevesta: Anna (Jurejevič? Žurejevič?) roj./vdova (Žugelj?) — KRITIČNO: (1) ali je "Wittwe" (vdova) ali "Tochter" (hči)?, (2) hiša/kraj: "Otok 9"? "Griblje 34"? — črka-za-črko!, (3) starost (34? 59?), (4) starši ali pokojni mož, (5) priče (Anton Pezdirc? Mathias Žurejevič?).
Izhod SAMO JSON: {"rows": [{"bride": "...", "status": "...", "age": "...", "village": "...", "houseNo": "...", "parentsOrSpouse": "...", "witnesses": "...", "priest": "...", "note": "..."}], "pageNote": "..."}`,

  's56_v16_v18_nevesti': `To je ULTRA-ZOOM nevest vpisov 16 in 18 (tail-1884) poročne knjige 04455. VPIS 16: nevesta Maria (Silak? Kilak?) — KRITIČNO hišna številka: "Griblje 34"? "½-Griblje 34"? + starost (34?) + starši (Johann Silak × Anna Dehlič?) + priče (Marko Hlobučar? Mathias Mrk/Muc?). VPIS 18: nevesta Anna (Krizan? Hrizan?) — KRITIČNO hišna številka: "Griblje 36"? "½-G."? + starost + starši (Marko Krizan × Anna Regina?) + priče.
Izhod SAMO JSON: {"rows": [{"no": "...", "bride": "...", "age": "...", "village": "...", "houseNo": "...", "parents": "...", "witnesses": "...", "note": "..."}], "pageNote": "..."}`,
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
      const rows = parsed.rows?.length ?? 0;
      console.log(`OK vrstice=${rows}`);
    } catch (e) {
      fs.writeFileSync(out.replace('.json', '.raw.txt'), content, 'utf-8');
      console.log('RAW:', e.message.slice(0, 50));
    }
  }
}
main().catch(e => { console.error('FATAL', e.message); process.exit(1); });
