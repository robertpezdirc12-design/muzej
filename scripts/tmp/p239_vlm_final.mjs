// P239 — VLM final: s53 vrstici 1–2 (PEZDIRC starši) + s54 vrstica 6 (Griblje blok)
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

const KROPS = '/tmp/p239/krops';

const PROMPTS = {
  's53_v1v2_full': `To je ULTRA-ZOOM zgornjega dela leve strani poročne knjige 04455 (Podzemelj), 6. Februar 1884, VRSTICI 1 in 2 (zaporedni številki "1." in "2."). OBE vrstici: ženina Martin Pezdirc (30 let?) in Mathias Pezdirc (27 let) — oba na isti hišni številki 1.

PREPIŠI TOČNO, črka-za-črko, ZA OBĚ VRSTICI:
(a) zaporedna številka
(b) datum
(c) ime + PRIIMEK ženina (Pezdirc/Pegdirc/Pezdirč — kakšno črko vidíš za "Pe"?)
(d) starost
(e) stan/lastništvo (¼-Gübler? "Güblanschfr."? ledinec?)
(f) KRAJ + hišna številka ženina — KRITIČNO: prva beseda (P-d-v-k-r-a-j? Oslob? Otok? Ploh?) — opíši vsako črko, dvom = [~]
(g) STARŠI ŽENINA: oče (ime + priimek) × mati (ime + roj. priimek) — KRITIČNO: ali je oče "Mathias/Matthias Pezdirc" ALI "Primož"?
(h) nevesta (ime + priimek + starost + kraj) če je vidna na tem izseku

Izhod SAMO veljaven JSON:
{"rows": [{"no": "...", "date": "...", "groom": "...", "age": "...", "status": "...", "village": "...", "houseNo": "...", "parents": "...", "bride": "...", "note": "..."}], "pageNote": "splošna opomba"}`,

  's54_v6_full': `To je ULTRA-ZOOM vrstice 6 poročne knjige 04455 (Podzemelj), Februar 1884 — GRIBLJE-BLOK: ženin Johann Simec (Griblje 54?) × nevesta Anna (Struč? Strucli? Struch?) (Griblje 44?).

PREPIŠI TOČNO:
(a) zaporedna številka (6.)
(b) datum (13. Februar?)
(c) ženin: ime + priimek + starost + stan ("Griblenski"? "Griblmarjev sin"?)
(d) ženinov kraj + hišna številka — KRITIČNO: "Griblje 54"? (54 ali 5½?)
(e) nevesta: ime + priimek + starost + stan
(f) nevestin kraj + hišna številka — KRITIČNO: "Griblje 44"? ali "34"? ali "½-Griblje"?
(g) starši ženina (oče × mati)
(h) starši neveste (oče × mati)
(i) priče (Mathias Klobučar? Jovan Mihelč?)
(j) duhovnik (Franz Dovgan/Dorgen?)

Izhod SAMO veljaven JSON:
{"rows": [{"no": "...", "date": "...", "groom": "...", "groomAge": "...", "groomStatus": "...", "groomPlace": "...", "bride": "...", "brideAge": "...", "bridePlace": "...", "parentsGroom": "...", "parentsBride": "...", "witnesses": "...", "priest": "...", "note": "..."}], "pageNote": "splošna opomba"}`,
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
  const zai = await ZAI.create();
  for (const name of process.argv.slice(2)) {
    const out = `${KROPS}/${name}.final.json`;
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
      console.log(`OK vrstice=${parsed.rows?.length}`);
    } catch (e) {
      fs.writeFileSync(out.replace('.json', '.raw.txt'), content, 'utf-8');
      console.log('RAW:', e.message.slice(0, 50));
    }
  }
}
main().catch(e => { console.error('FATAL', e.message); process.exit(1); });
