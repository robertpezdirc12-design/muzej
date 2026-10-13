// P44 — 2d krog: p67 ODLOČILNI izrez — zgornji pas tabele (Acker I/II, Wiesen I/II)
// samo stolpci Classe + Fläche, visoka ločljivost.
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';
import { execSync } from 'child_process';

const SRC = '/tmp/p44-pz-pages/pz-67.jpg';
const RAW_DIR = 'research/issue11/pz-raw';

async function main() {
  const out = `${RAW_DIR}/pz-67-band1.json`;
  if (fs.existsSync(out)) { console.log('že obstaja'); return; }
  // pas zgornje tretjine strani (naslov + prve 4 vrstice), polna širina, 2x povečava
  execSync(`python3 -c "
from PIL import Image
im = Image.open('${SRC}')
w, h = im.size
band = im.crop((0, 0, w, int(h * 0.38)))
band = band.resize((int(band.width * 1.6), int(band.height * 1.6)), Image.LANCZOS)
band.save('/tmp/p44-pz-67-band1.jpg', quality=95)
print('band:', band.size)"`);
  const b64 = fs.readFileSync('/tmp/p44-pz-67-band1.jpg').toString('base64');
  const PROMPT = `To je ZGORNJI DEL rekapitulacijske tabele (Specifischer Ausweis der Endresultate, občina Grüble, Kurrent 1825), povečan. Vidiš naslov in prve vrstice: Acker I, Acker II, nato Wiesen I (in morebiti Wiesen II).

PREBERI SAMO dva stolpca: Classe (I/II/III) in Fläche (Joch in Klafter) za VSAKO vidno vrstico. Števke preberi znak-za-znakom; če je števka dvoumna, zapiši OBE možnosti (npr. "2 ali 3").

POZOR na tipične zamenjave v Kurrent: 2 ↔ 3, 3 ↔ 5, 1 ↔ 4, 7 ↔ 9. Števka "234" ali "334"? "29" ali "39"?

IZHOD: SAMO veljaven JSON:
{"rows":[{"culture":"Acker|Wiesen|...","class":"I|II|...","joch":"št. ali 'X ali Y'","klafter":"št. ali 'X ali Y'","digitNotes":"opis dvoumnosti","confidence":"clear|~|?"}],"note":"1 stavek"}`;

  const zai = await ZAI.create();
  for (let a = 1; a <= 4; a++) {
    try {
      const c = await zai.chat.completions.createVision({
        messages: [{ role: 'user', content: [
          { type: 'text', text: PROMPT },
          { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${b64}` } }
        ]}],
        thinking: { type: 'disabled' }
      });
      const txt = c.choices[0]?.message?.content ?? '';
      const m = txt.match(/\{[\s\S]*\}/);
      let parsed = null;
      if (m) { try { parsed = JSON.parse(m[0]); } catch { try { parsed = JSON.parse(m[0].replace(/,(\s*[}\]])/g, '$1')); } catch {} } }
      fs.writeFileSync(out, JSON.stringify({
        page: 67, phase: 'p44-pass2d-band1',
        readAt: new Date().toISOString(), parseOk: parsed !== null,
        structured: parsed, raw: parsed ? undefined : txt.slice(0, 6000)
      }, null, 1));
      console.log(parsed ? 'JSON OK' : 'samo raw');
      return;
    } catch (e) {
      const wait = /429|rate/i.test(String(e.message)) ? 60 * a : 15;
      console.log(`poskus ${a} padel, čakam ${wait}s`);
      await new Promise(r => setTimeout(r, wait * 1000));
    }
  }
}
main().catch(e => { console.error('FATAL', e); process.exit(1); });
