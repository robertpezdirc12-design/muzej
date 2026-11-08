import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

async function main() {
  const zai = await ZAI.create();
  const b64 = fs.readFileSync('/tmp/ezkn-g4.jpg').toString('base64');
  for (let a = 1; a <= 3; a++) {
    try {
      const r = await zai.chat.completions.createVision({
        messages: [{ role: 'user', content: [
          { type: 'text', text: `To je list "GRIBLJE 4" katastrskega načrta k.o. GRIBLJE (ZKN ~1970, 1:2880, eZKN/GURS). Pokriva JUŽNI del k.o. Griblje (območje jugozahodno od vasi Griblje, proti Dragošam/Jankovičem/Bednju — geografsko lat ~45.544–45.557, lng ~15.273–15.297).

Odgovori natanko (5-7 stavkov):
1. Kaj je GLAVNA vsebina (settlementi hiš — kje gruče/verige, ceste)?
2. Preberi vsa večja besedila/krajevna imena, ki jih vidi (npr. Dragoše, Jankoviči...).
3. Ali vidiš reko ali potok?
4. Kakšna je orientacija lista (sever gor?) — kako veš?
5. Hišne številke ob hišah — preberi nekaj (katera območja)?` },
          { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${b64}` } }
        ]}],
        thinking: { type: 'disabled' }
      });
      console.log((r.choices?.[0]?.message?.content ?? '').slice(0, 1100));
      break;
    } catch (e) {
      console.error(`poskus ${a}: ${String(e.message ?? e).slice(0, 60)}`);
      await new Promise(r2 => setTimeout(r2, 15000));
    }
  }
}
main();
