// P259 — QUOTA CHECK za OSNOVNI chat endpoint (/chat/completions — NE vision!)
// Preveri ločeno kvoto + ali sprejme slike (multimodalni test).
import fs from 'fs';
const cfg = JSON.parse(fs.readFileSync('/etc/.z-ai-config', 'utf-8'));
const url = `${cfg.baseUrl}/chat/completions`;
const headers = {
  'Content-Type': 'application/json',
  'Authorization': `Bearer ${cfg.apiKey}`,
  'X-Z-AI-From': 'Z',
};
if (cfg.chatId) headers['X-Chat-Id'] = cfg.chatId;
if (cfg.userId) headers['X-User-Id'] = cfg.userId;
if (cfg.token) headers['X-Token'] = cfg.token;

const mode = process.argv[2] || 'text';
const body = {
  model: 'glm-4.6',
  messages: [{ role: 'user', content: 'Reci natanko: OK' }],
  max_tokens: 8,
  thinking: { type: 'disabled' },
};
if (mode === 'img') {
  const b64 = fs.readFileSync('/tmp/p259/dates/s11_d2.jpg').toString('base64');
  body.messages = [{
    role: 'user',
    content: [
      { type: 'text', text: 'To je izrez starega nemškega rokopisa (Kurrent). Prepiši natanko tisto, kar vidiš — datum/vrstico. Samo prepis, brez razlage.' },
      { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${b64}` } },
    ],
  }];
  body.max_tokens = 300;
}

try {
  const r = await fetch(url, { method: 'POST', headers, body: JSON.stringify(body) });
  const h = {};
  r.headers.forEach((v, k) => { if (/rate|limit|remaining|reset|model/i.test(k)) h[k] = v; });
  console.log('STATUS', r.status);
  console.log('HEADERS', JSON.stringify(h));
  const t = await r.text();
  if (r.status !== 200) console.log('BODY', t.slice(0, 300));
  else { const j = JSON.parse(t); console.log('VSEBINA:', (j.choices?.[0]?.message?.content || '').slice(0, 400)); }
} catch (e) {
  console.log('FETCH-ERR', String(e).slice(0, 200));
}
