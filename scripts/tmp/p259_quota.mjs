// P259 — QUOTA CHECK: ena minimalna zahteva na vision endpoint, izpiše rate-limit glave
// (tudi ob 429!). NE porabi veliko — 1 majhen tekstovni poziv.
import fs from 'fs';
const cfg = JSON.parse(fs.readFileSync('/etc/.z-ai-config', 'utf-8'));
const url = `${cfg.baseUrl}/chat/completions/vision`;
const headers = {
  'Content-Type': 'application/json',
  'Authorization': `Bearer ${cfg.apiKey}`,
  'X-Z-AI-From': 'Z',
};
if (cfg.chatId) headers['X-Chat-Id'] = cfg.chatId;
if (cfg.userId) headers['X-User-Id'] = cfg.userId;
if (cfg.token) headers['X-Token'] = cfg.token;

const body = {
  model: 'glm-4.5v',
  messages: [{ role: 'user', content: [{ type: 'text', text: 'Reci OK' }] }],
  max_tokens: 4,
  thinking: { type: 'disabled' },
};

try {
  const r = await fetch(url, { method: 'POST', headers, body: JSON.stringify(body) });
  const h = {};
  r.headers.forEach((v, k) => { if (/rate|limit|remaining|reset/i.test(k)) h[k] = v; });
  console.log('STATUS', r.status);
  console.log('HEADERS', JSON.stringify(h));
  if (r.status !== 200) console.log('BODY', (await r.text()).slice(0, 200));
  else { const j = await r.json(); console.log('OK-dolzina', JSON.stringify(j).length); }
} catch (e) {
  console.log('FETCH-ERR', String(e).slice(0, 200));
}
