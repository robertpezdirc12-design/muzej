// P239 — VLM pass-2: ciljni kropi (polovice) za razrešitev številčenja in Griblje blokov
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

const KROPS = '/tmp/p239/krops';

const PROMPTS = {
  's55_levo_cel': `To je LEVA polovica razprtega lista razprtega poročne knjige 04455 župnije Podzemelj (leto 1884, pag. ~54). Vidnih je več vpisov. Za VSAKO vrstico prepiši: (1) zaporedno številko TOČNO (mali zapisi na levem robu), (2) datum, (3) ženinovo ime + priimek + stan (ledig/vdovec) + starost, (4) hiša/kraj ženina (npr. "Griblje 25", "Otok 1", "Cernomelj 352" itd.), (5) ženinove starše (oče × mati) če so vidni.
Štajerska oblika: glava bloka bere se desno→levo.
Negotovo = [~], neberljivo = [?]. Ne izmišljuj.
Izhod: SAMO veljaven JSON:
{"rows": [{"no": "...", "date": "...", "groom": "...", "age": "...", "place": "...", "parents": "...", "note": "..."}], "bigHeadings": ["..."], "pageNote": "..."}`,

  's55_desno_cel': `To je DESNA polovica razprtega lista poročne knjige 04455 župnije Podzemelj (leto 1884). Vidne so neveste (nadljevanje vpisov z leve strani). Za VSAKO vrstico prepiši: (1) zaporedno številko če je vidna, (2) datum, (3) nevestino ime + priimek + stan + starost, (4) hiša/kraj neveste, (5) nevestine starše (oče × mati), (6) priče, (7) duhovnik.
Negotovo = [~], neberljivo = [?]. Ne izmišljuj.
Izhod: SAMO veljaven JSON:
{"rows": [{"no": "...", "date": "...", "bride": "...", "age": "...", "place": "...", "parents": "...", "witnesses": "...", "priest": "...", "note": "..."}], "pageNote": "..."}`,

  's56_levo_cel': `To je LEVA polovica razprtega lista poročne knjige 04455 župnije Podzemelj. NA VRHU: TAIL-zadnji vpisi leta 1884 (zaporedne št. okvirno 15–18). POD NJIM: velike številke »1885« in restart vpis št. 1 (25. Jän 1885). Prepiši: (1) zaporedne številke TOČNO, (2) datume, (3) ženina (ime + priimek + stan + starost), (4) hiša/kraj ženina (npr. "Otok 1", "Griblje 25"), (5) starše ženina.
Pozor na dvojnike v hišnih številkah (npr. 58-vs-38!). Negotovo = [~], neberljivo = [?].
Izhod: SAMO veljaven JSON:
{"tailRows": [{"no": "...", "date": "...", "groom": "...", "age": "...", "place": "...", "parents": "...", "note": "..."}], "restart1885": [{"no": "...", "date": "...", "groom": "...", "place": "...", "note": "..."}], "bigHeadings": ["..."], "pageNote": "..."}`,

  's56_desno_cel': `To je DESNA polovica razprtega lista poročne knjige 04455 župnije Podzemelj. TAIL-vpisi leta 1884 (neveste) zgoraj, restart-1885 spodaj. Za VSAKO vrstico: (1) zaporedna št., (2) datum, (3) nevesta (ime + priimek + stan + starost), (4) hiša/kraj neveste (npr. "Griblje 34", "Griblje 36"), (5) nevestine starše, (6) priče, (7) duhovnik.
Negotovo = [~], neberljivo = [?].
Izhod: SAMO veljaven JSON:
{"tailRows": [{"no": "...", "date": "...", "bride": "...", "age": "...", "place": "...", "parents": "...", "witnesses": "...", "priest": "...", "note": "..."}], "restart1885": [{"no": "...", "bride": "...", "place": "...", "witnesses": "...", "note": "..."}], "pageNote": "..."}`,

  's53_levo_cel': `To je LEVA polovica razprtega lista poročne knjige 04455 župnije Podzemelj, začetek leta 1884 (velika glava »1884«). Zaporedne številke restartajo na 1. Prepiši VSAKO vrstico: (1) zap. št., (2) datum (npr. "6. Februar"), (3) ženin (ime + priimek + stan + starost), (4) hiša/kraj ženina (npr. "Oslob 1", "Griblje 25"), (5) starše ženina (oče × mati). Posebno pozorno na priimke PEZDIRC/PEGDIREC, KRIZAN/HRIZAN, MALESIČ.
Negotovo = [~], neberljivo = [?]. Ne izmišljuj.
Izhod: SAMO veljaven JSON:
{"rows": [{"no": "...", "date": "...", "groom": "...", "age": "...", "place": "...", "parents": "...", "note": "..."}], "bigHeadings": ["..."], "pageNote": "..."}`,

  's53_desno_cel': `To je DESNA polovica razprtega lista poročne knjige 04455 župnije Podzemelj, začetek leta 1884. Prepiši za VSAKO vrstico: (1) zap. št., (2) datum, (3) nevesta (ime + priimek + stan + starost), (4) hiša/kraj neveste, (5) nevestine starše, (6) priče, (7) duhovnik.
Negotovo = [~], neberljivo = [?].
Izhod: SAMO veljaven JSON:
{"rows": [{"no": "...", "date": "...", "bride": "...", "age": "...", "place": "...", "parents": "...", "witnesses": "...", "priest": "...", "note": "..."}], "pageNote": "..."}`,

  's54_levo_cel': `To je LEVA polovica razprtega lista poročne knjige 04455 župnije Podzemelj, leto 1884 nadaljevanje (zap. št. okvirno 6–10). Prepiši VSAKO vrstico: (1) zap. št. TOČNO, (2) datum, (3) ženin (ime + priimek + stan + starost), (4) hiša/kraj ženina (npr. "Griblje 54", "Voranci 13", "Gradac 2"), (5) starše ženina. Posebno pozorno na Griblje-vpise (SIMIEC, STRUCH, HRIZAN) in priče PEZDIRC/PEGDIREC.
Negotovo = [~], neberljivo = [?]. Ne izmišljuj.
Izhod: SAMO veljaven JSON:
{"rows": [{"no": "...", "date": "...", "groom": "...", "age": "...", "place": "...", "parents": "...", "note": "..."}], "pageNote": "..."}`,

  's54_desno_cel': `To je DESNA polovica razprtega lista poročne knjige 04455 župnije Podzemelj, leto 1884 nadaljevanje. Prepiši za VSAKO vrstico: (1) zap. št., (2) datum, (3) nevesta (ime + priimek + stan + starost), (4) hiša/kraj neveste (npr. "Griblje 44", "Vrtok 5", "Gradac 66"), (5) nevestine starše, (6) priče, (7) duhovnik.
Negotovo = [~], neberljivo = [?].
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
      const rows = parsed.rows?.length ?? (parsed.tailRows?.length ?? 0) + (parsed.restart1885?.length ?? 0);
      console.log(`OK vrstice=${rows}`);
    } catch (e) {
      fs.writeFileSync(out.replace('.json', '.raw.txt'), content, 'utf-8');
      console.log('RAW:', e.message.slice(0, 50));
    }
  }
}
main().catch(e => { console.error('FATAL', e.message); process.exit(1); });
