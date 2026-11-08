import ZAI from 'z-ai-web-dev-sdk';
import { execSync } from 'child_process';
import fs from 'fs';

async function look(zai, id, file, crop, prompt) {
  execSync(`python3 -c "
from PIL import Image
im = Image.open('${file}')
tile = im.crop((${crop.join(',')}))
tile = tile.resize((min(1800, int(tile.width*1.5)), int(tile.height*1.5*min(1800, tile.width*1.5)/ (tile.width*1.5))), Image.LANCZOS)
tile.save('/tmp/p10-look-${id}.jpg', quality=93)
"`);
  const b64 = fs.readFileSync(`/tmp/p10-look-${id}.jpg`).toString('base64');
  for (let a = 1; a <= 3; a++) {
    try {
      const r = await zai.chat.completions.createVision({
        messages: [{ role: 'user', content: [
          { type: 'text', text: prompt },
          { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${b64}` } }
        ]}],
        thinking: { type: 'disabled' }
      });
      return r.choices?.[0]?.message?.content ?? '';
    } catch (e) {
      console.error(`  ${id} poskus ${a}: ${String(e.message ?? e).slice(0, 50)}`);
      await new Promise(r2 => setTimeout(r2, 12000));
    }
  }
  return null;
}

async function main() {
  const zai = await ZAI.create();
  // A03: vzhodni pas vsebine (x 2050–2645, y 0–2154) — celoten pas
  let out = await look(zai, 'a03strip', 'public/atlas/n83-a03.jpg', [2050, 0, 2645, 2154],
    `To je VZHODNI PAS katastrskega lista A03 (k.o. Griblje, franciscejski kataster 1825). Lev 15 % izrezka je večinoma prazen, desni del ima parcele.
Odgovori natanko:
1. Ali je na izrezku vidna REKA (širok prazen/svetel vijugast pas med bregovnima črtama)? Kje (levo/desno, zgoraj/spodaj)?
2. Ali vidiš VAS — verigo hiš (temni pravokotni simboli) ob cesti? Kje točno (levo/desno %, zgoraj/spodaj %)? Približno koliko hiš?
3. Ali vidiš CESTO ali POT (črta, ob kateri stojijo hiše)?
4. Preberi 2-3 največja/močnejša besedilna napisa.
5. Kaj je na skrajnem DESNEM robu izrezka (meja lista, reka, gozd)?
Odgovori v 5-6 stavkih, stvarno.`);
  console.log('=== A03 PAS ===\n', out);
  fs.writeFileSync('/tmp/p10-look-a03strip.txt', out ?? '');
}
main();
