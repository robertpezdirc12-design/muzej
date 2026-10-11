// P44 sonda: ali je VLM dostop (z-ai-web-dev-sdk createVision) trenutno na voljo?
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

async function main() {
  const zai = await ZAI.create();
  const t0 = Date.now();
  try {
    const c = await zai.chat.completions.createVision({
      messages: [{ role: 'user', content: [
        { type: 'text', text: 'Odgovori samo z: OK' },
        { type: 'image_url', image_url: { url: 'data:image/jpeg;base64,' + fs.readFileSync('/tmp/p44-probe.jpg').toString('base64') } }
      ]}],
      thinking: { type: 'disabled' }
    });
    console.log('VLM PROBE OK', Date.now() - t0, 'ms:', (c.choices[0]?.message?.content ?? '').slice(0, 40));
  } catch (e) {
    console.log('VLM PROBE ERR:', String(e.message).slice(0, 300));
  }
}
main();
