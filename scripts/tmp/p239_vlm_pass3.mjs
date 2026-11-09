// P239 — VLM pass-3: ultra-zoom trakov (številčenje+datum / Griblje bloki)
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

const KROPS = '/tmp/p239/krops';

const PROMPTS = {
  's53_nodat': `To je ULTRA-ZOOM levega roba poročne knjige 04455 (Podzemelj), leto 1884 začetek. Vidne so zaporedne številke vpisov in datumi (kurent-pisava, dvoriščna nemščina). Preberi TOČNO: številka (1., 2., ...) in datum (dan + mesec, npr. "6. Februar", "10. Februar", "13. Februar", "17. Februar" itd.). Kurent števila so zapisana kot "1.", "2." z majhno končnico. Mesece piši izpisano kot na listu (Februar/März/April...).
Izhod SAMO JSON: {"rows": [{"no": "...", "date": "...", "note": "..."}], "bigHeadings": ["..."], "pageNote": "..."}`,
  's54_nodat': `To je ULTRA-ZOOM levega roba poročne knjige 04455 (Podzemelj), leto 1884 nadaljevanje. Preberi TOČNO zaporedne številke (okvirno 6.–10. ali 6.–11.) in datume. Kurent "11" ima dve navpični črti z dvojnim spodnjim prelomom; "12" ima navpično črto + c-kotiko — bodi zelo pozoren.
Izhod SAMO JSON: {"rows": [{"no": "...", "date": "...", "note": "..."}], "pageNote": "..."}`,
  's55_nodat': `To je ULTRA-ZOOM levega roba poročne knjige 04455 (Podzemelj), leto 1884. Preberi TOČNO zaporedne številke (KRITIČNO: ali je prva številka "11." ali "12."? Kurent 11 = dve navpični črti; 12 = črta + c-kotika) in datume. Zadnja vrstica naj bi bila "14." ali "15." — bodi natančen.
Izhod SAMO JSON: {"rows": [{"no": "...", "date": "...", "note": "..."}], "pageNote": "..."}`,
  's56_nodat': `To je ULTRA-ZOOM levega roba poročne knjige 04455 (Podzemelj). Zgoraj TAIL-vpisi leta 1884 (številke okvirno 15.–18.), pod njimi velike številke »1885« in restart "1." (25. Jän). Preberi TOČNO vse številke in datume.
Izhod SAMO JSON: {"tailRows": [{"no": "...", "date": "...", "note": "..."}], "restart1885": [{"no": "...", "date": "...", "note": "..."}], "bigHeadings": ["..."], "pageNote": "..."}`,
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
      const rows = parsed.rows?.length ?? (parsed.tailRows?.length ?? 0) + (parsed.restart1885?.length ?? 0);
      console.log(`OK vrstice=${rows}`);
    } catch (e) {
      fs.writeFileSync(out.replace('.json', '.raw.txt'), content, 'utf-8');
      console.log('RAW:', e.message.slice(0, 50));
    }
  }
}
main().catch(e => { console.error('FATAL', e.message); process.exit(1); });
