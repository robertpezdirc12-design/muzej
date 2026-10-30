import { runQA } from '/home/z/muzej/src/lib/qa.ts';
const r = runQA({});
const tests = r.tests || r.checks || [];
const fails = tests.filter(t => !t.ok);
console.log('ok:', r.ok, '| testov:', tests.length, '| FAILS:', fails.length);
for (const f of fails.slice(0, 10)) console.log(' -', f.name, '::', String(f.detail || f.error || '').slice(0, 160));
const last = tests.filter(t => /p163|p162/.test(t.name));
for (const t of last) console.log(t.ok ? '✓' : '✗', t.name, t.ok ? '' : String(t.detail).slice(0, 120));
