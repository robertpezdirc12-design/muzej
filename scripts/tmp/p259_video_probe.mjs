// P259 — VIDEO PROBE: ali video-understand pot ima LOČENO kvoto od vision-slik?
// Surovi fetch na /chat/completions/vision z video_url (data URL). Beri glave + vsebino.
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

const b64 = fs.readFileSync('/tmp/p259/probe.mp4').toString('base64');
const body = {
  model: 'glm-4.5v',
  messages: [{
    role: 'user',
    content: [
      { type: 'text', text: 'Video je diaprojekcija 4 izrezov stare poročne knjige (Kurrent-pisava, nemščina), vsak 2 s. ZA VSAK IZREZ (1–4) prepiši DOBESEDNO besedilo/datum, ki vidiš. Izhod: 4 vrstice "1: ...", "2: ..." itd. Samo prepis.' },
      { type: 'video_url', video_url: { url: `data:video/mp4;base64,${b64}` } },
    ],
  }],
  max_tokens: 600,
  thinking: { type: 'disabled' },
};

try {
  const r = await fetch(url, { method: 'POST', headers, body: JSON.stringify(body) });
  const h = {};
  r.headers.forEach((v, k) => { if (/rate|limit|remaining|reset/i.test(k)) h[k] = v; });
  console.log('STATUS', r.status);
  console.log('HEADERS', JSON.stringify(h));
  const t = await r.text();
  if (r.status !== 200) console.log('BODY', t.slice(0, 300));
  else { const j = JSON.parse(t); console.log('VSEBINA:\n' + (j.choices?.[0]?.message?.content || '').slice(0, 800)); }
} catch (e) {
  console.log('FETCH-ERR', String(e).slice(0, 200));
}
