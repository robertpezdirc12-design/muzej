import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';
const zai = await ZAI.create();

const PROMPT = `Slika je DATUMSKI STOLPEC (povečan ×4) strani poročne knjige 01738 (Kurrent-pisava) z NARIŠANO RDEČO MREŽO: vodoravne rdeče črte z oznakami 'y150', 'y200', … vsake 100 px (v koordinatah ORIGINALNEGA skena).
Naloga: za VSAKO vrstico z zapisanim datumom podaj:
1) datum (dan. mesec; 'd°'=isto kot prejšnja vrstica),
2) y-pozicijo: med katerima dvema rdečima črtama (oznakama) se nahaja SREDINA vrstice (npr. 'y300-y400'),
3) številko v levem ROBU (marginalna številka vpisa, če je — npr. '8', '9'…) ali prazno.
Vrstice preberi OD ZGORAJ DOL. Ne izpusti nobene vrstice z vsebino (tudi delno zapisane). Če je med črtama prazno, ne navajaj je.
Izhod SAMO JSON: {"rows":[{"r":1,"datum":"","y":"","rob":""}],"razlaga":""}`;

async function run(s) {
  const out = `/tmp/p259/ygrid_s${s}.json`;
  if (fs.existsSync(out) && fs.statSync(out).size > 30) { console.log(`s${s}: skip`); return; }
  const content = [{ type: 'text', text: PROMPT }];
  content.push({ type: 'image_url', image_url: { url: `data:image/jpeg;base64,${fs.readFileSync(`/tmp/p259/dates_grid_s${s}.jpg`).toString('base64')}` } });
  for (let a = 1; a <= 4; a++) {
    try {
      const r = await zai.chat.completions.createVision({
        messages: [{ role: 'user', content }],
        temperature: 0.1, max_tokens: 1600, thinking: { type: 'disabled' },
      });
      fs.writeFileSync(out, r.choices[0].message.content || '');
      console.log(`s${s}: OK`);
      return;
    } catch (e) { console.log(`s${s}: a${a} ${String(e).slice(0,60)}`); await new Promise(r2=>setTimeout(r2,2500)); }
  }
  console.log(`s${s}: FAIL`);
}
for (const s of [11, 12, 13]) { await run(s); await new Promise(r => setTimeout(r, 1200)); }
