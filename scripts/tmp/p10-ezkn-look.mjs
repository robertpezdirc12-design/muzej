import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

async function main() {
  const zai = await ZAI.create();
  const b64 = fs.readFileSync('/tmp/ezkn-g2-mid.jpg').toString('base64');
  for (let a = 1; a <= 3; a++) {
    try {
      const r = await zai.chat.completions.createVision({
        messages: [{ role: 'user', content: [
          { type: 'text', text: `To je katastrski načrt (DjVu sken, 1:2880) z eZKN portala Geodetske uprave RS, k.o. GRIBLJE, list "GRIBLJE 2", ki pokriva sredino k.o. (vas Griblje).

Odgovori natanko (5-7 stavkov):
1. Katero obdobje prikazuje ta načrt? (starec franciscejski/reambuliran ~19. stoletje, ali moderen ZKN 20. stoletje?) Utemelji (pisava, vsebina).
2. Ali vidiš VAS (veriga/gruča hiš)? Kje?
3. Ali vidiš CERKEV (simbol z križem)?
4. Ali vidiš REKO na vzhodu?
5. Preberi 2-3 napisov (krajevna imena, hišne številke).
6. Ali so vidne hišne številke ob hišah? Kakšne (približno)?` },
          { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${b64}` } }
        ]}],
        thinking: { type: 'disabled' }
      });
      console.log((r.choices?.[0]?.message?.content ?? '').slice(0, 900));
      break;
    } catch (e) {
      console.error(`poskus ${a}: ${String(e.message ?? e).slice(0, 60)}`);
      await new Promise(r2 => setTimeout(r2, 15000));
    }
  }
}
main();
