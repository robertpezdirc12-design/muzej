import ZAI from 'z-ai-web-dev-sdk';

async function main() {
  try {
    const zai = await ZAI.create();
    const t0 = Date.now();
    const r = await zai.chat.completions.create({
      messages: [{ role: 'user', content: 'Odgovori samo z besedo: OK' }]
    });
    console.log('LLM probe OK:', (r.choices?.[0]?.message?.content ?? '').slice(0, 50), `(${Date.now() - t0}ms)`);
  } catch (e) {
    console.log('PROBE FAIL status=', e.status ?? 'n/a', String(e.message ?? e).slice(0, 150));
  }
}
main();
