// P259 — TIEBREAK VLM: 2 nevtralna klica (r1/r2/r5 datumi, r5-ultra)
import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';

const DIR = '/home/z/my-project/research/issue17/p259-work/tiebreak';
const OUT = '/home/z/my-project/research/issue17/p259-work/tiebreak';

const JOBS = [
  {
    name: 'tiebreak_dates',
    ask: `Slika je navpični sklad 3 POVEČANIH izrezov (x6) iz poročne knjige Trauungs-Buch 01738 (Kurrent-pisava, nemško, leto 1833). Vsak izrez ima BEL OZNAKOVNI NASELOVNI TRAK nad sabo: TRAK A = VRSTICA 1, TRAK B = VRSTICA 2, TRAK C = VRSTICA 5. V vsakem traku prepiši DATUM POROKE DOBESEDNO (dan, mesec, letnica — če je letnica zapisana). Če je datum dito/d°/att°, to zapiši. Če je v levem robu vidna robovna številka (lahko tudi prečrtana), jo zapiši posebej. NE ugibaj med alternativami — prepiši SAMO glyph-e, ki jih vidiš, in pri vsakem oceni gotovost (jasno/verjetno/nejasno). Izhod SAMO JSON: {"A":{"datum":"","gotovost":""},"B":{"datum":"","gotovost":""},"C":{"datum":"","rob":"","gotovost":""},"razlaga":""}`,
  },
  {
    name: 'r5_ultra',
    ask: `Slika je ULTRA POVEČAN izrez (x7) VRSTICE 5 poročne knjige Trauungs-Buch 01738 (Kurrent, nemško, 1833): levi rob + datumski stolpec. Prepiši DOBESEDNO: (1) vse, kar je v levem robu (robovna številka? prečrtano?), (2) datum poroke (dan + mesec; pazi na Kurrent številke 9/0, 1/2!). NE ugibaj — opiši glyph-e. Izhod SAMO JSON: {"rob":"","datum":"","razlaga":""}`,
  },
];

const zai = await ZAI.create();
for (const j of JOBS) {
  const content = [
    { type: 'text', text: j.ask },
    { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${fs.readFileSync(`${DIR}/s12_${j.name}.jpg`).toString('base64')}` } },
  ];
  const r = await zai.chat.completions.createVision({
    messages: [{ role: 'user', content }],
    temperature: 0.1, max_tokens: 1200, thinking: { type: 'disabled' },
  });
  const c = (r.choices[0].message.content || '').trim();
  fs.writeFileSync(`${OUT}/s12_${j.name}.VAL.json`, c);
  console.log(`${j.name}: OK (${c.length})`);
  await new Promise((res) => setTimeout(res, 3500));
}
console.log('TIEBREAK-VLM DONE');
