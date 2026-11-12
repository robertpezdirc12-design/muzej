// P259 — RAW kvota-proba: EN klic na vision-endpoint prek surovega fetch (da vidimo glave).
// Izpis: STATUS + vse x-ratelimit* glave (posebej daily-remaining). Payload minimalen (1x1 jpg).
import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';

const zai = await ZAI.create();
const { baseUrl, chatId, userId, apiKey, token } = zai.config;

const headers = {
  'Content-Type': 'application/json',
  'Authorization': `Bearer ${apiKey}`,
  'X-Z-AI-From': 'Z',
};
if (chatId) headers['X-Chat-Id'] = chatId;
if (userId) headers['X-User-Id'] = userId;
if (token) headers['X-Token'] = token;

const body = {
  messages: [{
    role: 'user',
    content: [
      { type: 'text', text: 'Reply with the single word: ok' },
      { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${fs.readFileSync('/tmp/p259/tiny.jpg').toString('base64')}` } },
    ],
  }],
  temperature: 0.1,
  max_tokens: 16,
  thinking: { type: 'disabled' },
};

let status = 'UNKNOWN';
try {
  const r = await fetch(`${baseUrl}/chat/completions/vision`, {
    method: 'POST', headers, body: JSON.stringify(body),
  });
  status = `${r.status} ${r.statusText}`;
  const hdrs = {};
  r.headers.forEach((v, k) => { if (k.toLowerCase().includes('ratelimit') || k.toLowerCase().includes('quota')) hdrs[k] = v; });
  for (const [k, v] of Object.entries(hdrs)) console.log(`${k}: ${v}`);
  if (r.ok) {
    const j = await r.json();
    const c = j?.choices?.[0]?.message?.content || '';
    console.log(`reply: ${String(c).slice(0, 40)}`);
  } else {
    const t = await r.text();
    console.log(`err-body: ${t.slice(0, 200)}`);
  }
} catch (e) {
  status = `EXC ${String(e).slice(0, 120)}`;
}
console.log(`STATUS ${status}`);
