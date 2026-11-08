import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

const IDS = { 227666: 'A01', 227668: 'A02', 227670: 'A03', 227671: 'A04', 227673: 'A05' };

async function main() {
  const zai = await ZAI.create();
  for (const [id, sheet] of Object.entries(IDS)) {
    const b64 = fs.readFileSync(`/tmp/vac-img-${id}.jpg`).toString('base64');
    try {
      const r = await zai.chat.completions.createVision({
        messages: [{ role: 'user', content: [
          { type: 'text', text: `To je predogled arhivskega katastrskega lista ${sheet} (SI AS 176/N/N83, franciscejski kataster k.o. Griblje). Opiši v 3-4 stavkih: (1) glavne vidne vsebine (reka? naselje/veriga stavb? gozd?), kje točno (strani lista), (2) orientacijo (kaj je na severu/zgornjem delu), (3) vse vidne napise. Bodi stvarn.` },
          { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${b64}` } }
        ]}],
        thinking: { type: 'disabled' }
      });
      console.log(`\n===== ${sheet} =====`);
      console.log((r.choices?.[0]?.message?.content ?? '').slice(0, 700));
    } catch (e) {
      console.log(`${sheet} FAIL: ${String(e.message ?? e).slice(0, 80)}`);
    }
  }
}
main();
