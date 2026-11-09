// P240 — VLM pass-2: ciljni kropi (polovice) za razrešitev številčenja, restarta in blokov
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

const KROPS = '/tmp/p240/krops';

const PROMPTS = {
  's50_levo_cel': `To je LEVA polovica razprtega lista poročne knjige 04455 župnije Podzemelj. ZGORAJ: tail-vpisi leta 1882 (novembra 1882). NA DNU: statistična vrsta (številke zakonskih stanov, npr. 1,8,8,3) + VELIKE številke »1883« + prvi vpis novega leta (restart zap. št. = 1). Prepiši VSAKO vrstico: (1) zaporedna št. TOČNO (mali zapisi na levem robu), (2) datum (dan + mesec), (3) ženin (ime + priimek + stan + starost), (4) hiša/kraj ženina (npr. "Griblje 36", "Griblje 25", "Grabelbe 42"), (5) starše ženina. Posebno pozorno na Griblje-vpise in priimke HRIZAN/PEZDIRC/MILEK.
Negotovo = [~], neberljivo = [?]. Ne izmišljuj.
Izhod: SAMO veljaven JSON:
{"tailRows": [{"no": "...", "date": "...", "groom": "...", "age": "...", "place": "...", "parents": "...", "note": "..."}], "statsRow": "...", "restart1883": [{"no": "...", "date": "...", "groom": "...", "age": "...", "place": "...", "parents": "...", "note": "..."}], "bigHeadings": ["..."], "pageNote": "..."}`,

  's50_desno_cel': `To je DESNA polovica razprtega lista poročne knjige 04455 župnije Podzemelj. ZGORAJ: tail-vpisi 1882 (neveste), NA DNU: prvi vpis leta 1883. Za VSAKO vrstico: (1) zaporedna št., (2) datum, (3) nevesta (ime + priimek + stan + starost), (4) hiša/kraj neveste (npr. "Griblje 25"), (5) nevestine starše, (6) priče, (7) duhovnik.
Negotovo = [~], neberljivo = [?]. Ne izmišljuj.
Izhod: SAMO veljaven JSON:
{"tailRows": [{"no": "...", "date": "...", "bride": "...", "age": "...", "place": "...", "parents": "...", "witnesses": "...", "priest": "...", "note": "..."}], "restart1883": [{"no": "...", "bride": "...", "place": "...", "witnesses": "...", "priest": "...", "note": "..."}], "pageNote": "..."}`,

  's51_levo_cel': `To je LEVA polovica razprtega lista poročne knjige 04455 župnije Podzemelj, leto 1883 (velika glava »1883«; restart-1 je že na prejšnjem listu — TUKAJ so naslednji vpisi, zap. št. verjetno 2.–7.!). Prepiši VSAKO vrstico: (1) zap. št. TOČNO s levega roba (KRITIČNO: preberi vsako številko — je prva vrstica "2." ali "1."?), (2) datum (npr. "Jänner 28.", "februar 4.", "April 22."), (3) ženin (ime + priimek + stan + starost), (4) hiša/kraj ženina (npr. "Laze 11", "Granc 25", "Podzemelj 3", "Griblje 2", "Tribuče"), (5) starše ženina. Posebno pozorno na PEZDIRC-ženina (Miha?) in Griblje-ženina (Petlebec h2?).
Negotovo = [~], neberljivo = [?]. Ne izmišljuj.
Izhod: SAMO veljaven JSON:
{"rows": [{"no": "...", "date": "...", "groom": "...", "age": "...", "place": "...", "parents": "...", "note": "..."}], "bigHeadings": ["..."], "pageNote": "..."}`,

  's51_desno_cel': `To je DESNA polovica razprtega lista poročne knjige 04455 župnije Podzemelj, leto 1883. Za VSAKO vrstico: (1) zaporedna št., (2) datum, (3) nevesta (ime + priimek + stan + starost), (4) hiša/kraj neveste, (5) nevestine starše, (6) priče, (7) duhovnik.
Negotovo = [~], neberljivo = [?]. Ne izmišljuj.
Izhod: SAMO veljaven JSON:
{"rows": [{"no": "...", "date": "...", "bride": "...", "age": "...", "place": "...", "parents": "...", "witnesses": "...", "priest": "...", "note": "..."}], "pageNote": "..."}`,

  's52_levo_cel': `To je LEVA polovica razprtega lista poročne knjige 04455 župnije Podzemelj, TAIL leta 1883 (zap. št. verjetno 8.–12., vse leta 1883; 1884 se začne na naslednjem listu). Prepiši VSAKO vrstico: (1) zap. št. TOČNO, (2) datum, (3) ženin (ime + priimek + stan + starost), (4) hiša/kraj ženina (npr. "Kaplitz 8", "Prilozje 11", "Nemška vas 45", "Gertsitš 5"), (5) starše ženina. Posebno pozorno na priimka STRAUS in nevesto MILEK/Milleh (vpis 10!).
Negotovo = [~], neberljivo = [?]. Ne izmišljuj.
Izhod: SAMO veljaven JSON:
{"rows": [{"no": "...", "date": "...", "groom": "...", "age": "...", "place": "...", "parents": "...", "note": "..."}], "pageNote": "..."}`,

  's52_desno_cel': `To je DESNA polovica razprtega lista poročne knjige 04455 župnije Podzemelj, TAIL 1883. Za VSAKO vrstico: (1) zaporedna št., (2) datum, (3) nevesta (ime + priimek + stan + starost), (4) hiša/kraj neveste (npr. "Boršt 16", "Konec", "Graditz 2"), (5) nevestine starše, (6) priče, (7) duhovnik. Posebno pozorno na nevesto vpisa 10 (Milek/Milleh/Milleh?).
Negotovo = [~], neberljivo = [?]. Ne izmišljuj.
Izhod: SAMO veljaven JSON:
{"rows": [{"no": "...", "date": "...", "bride": "...", "age": "...", "place": "...", "parents": "...", "witnesses": "...", "priest": "...", "note": "..."}], "pageNote": "..."}`,
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
    const out = `${KROPS}/${name}.pass2.json`;
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
      const rows = parsed.rows?.length ?? (parsed.tailRows?.length ?? 0) + (parsed.restart1883?.length ?? 0);
      console.log(`OK vrstice=${rows}`);
    } catch (e) {
      fs.writeFileSync(out.replace('.json', '.raw.txt'), content, 'utf-8');
      console.log('RAW:', e.message.slice(0, 50));
    }
  }
}
main().catch(e => { console.error('FATAL', e.message); process.exit(1); });
