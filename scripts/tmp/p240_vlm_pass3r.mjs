// P240 — VLM pass-3 retry: s50 restart (tansen krop) + stats/glava
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

const KROPS = '/tmp/p240/krops';

const PROMPTS = {
  's50_restart_bot2': `To je DNO razprtega lista poročne knjige 04455 (Podzemelj): NA VRHU zadnji tail-vpis leta 1882, nato (morda) črta, nato PRVI vpis leta 1883 (restart zap. št. = 1, datum ~21. Januar 1883). Vrstice so široke: LEVA polovica = ženin + starši, DESNA polovica = nevesta + starši + priče + duhovnik. Prepiši restart-vrstico POPOLNOSTI črka-za-črko: zap. št. (1.?), datum, ženin (ime + priimek + stan + hiša/kraj + starost), starši ženina, nevesta (ime + priimek + stan + hiša/kraj + starost), nevestina starša, priče, duhovnik. Negotovo = [~], neberljivo = [?].
Izhod SAMO JSON: {"restart1883": {"no": "...", "date": "...", "groom": "...", "groomPlace": "...", "groomParents": "...", "bride": "...", "bridePlace": "...", "brideParents": "...", "witnesses": "...", "priest": "..."}, "tailAbove": {"date": "...", "groom": "..."}, "pageNote": "..."}`,

  's50_stats_glava': `To je pas s SREDINE-DNA razprtega lista poročne knjige 04455 (Podzemelj): tukaj je statistična vrsta (številke zakonskih stanov ob koncu leta 1882) in/ali VELIKE številke »1883« (glava novega leta). Prepiši TOČNO kaj vidiš: ali so številke "1 8 8 3" (kot letnica 1883) ali ločene statistične številke (npr. 1, 8, 8, 3 = števila ženinov po stanih)? Kje stojijo (nad glavo / v glavi)? 
Izhod SAMO JSON: {"statsRow": "...", "bigHeadings": ["..."], "interpretation": "kaj številke pomenijo", "pageNote": "..."}`,
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
