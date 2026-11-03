import fs from 'node:fs';
import { runQA } from '../../src/lib/qa.ts';
const rep = runQA({
  fileExists: (p) => fs.existsSync(p),
  readFile: (p) => { try { return fs.readFileSync(p, 'utf8'); } catch { return null; } },
});
const failed = rep.tests.filter(t => !t.pass);
console.log('total:', rep.tests.length, '| report-ok:', rep.ok, '| failed:', failed.length);
for (const f of failed) console.log('FAIL:', f.id, '—', (f.detail || '').slice(0, 120));
const p196 = rep.tests.find(t => t.id === 'qa-p196-parish-death-1881-04106');
console.log('qa-p196:', p196 ? (p196.pass ? 'PASS ✓' : 'FAIL') : 'MANJKA');
