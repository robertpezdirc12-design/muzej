// P196: extract all 1881 entries from 9 VLM page JSONs → compact table + raw JSON
import fs from 'fs';

const pages = ['s171','s172','s173','s174','s175','s176','s177','s178','s179'];
const out = [];
const issues = [];

for (const skan of pages) {
  const j = JSON.parse(fs.readFileSync(`/tmp/p196/vlm-page/${skan}.json`, 'utf8'));
  const pag = parseInt(skan.slice(1), 10) - 6;
  for (const v of (j.vrstice || [])) {
    if (v.zaporedna == null) {
      // MEJA or note row — keep only if it looks like MEJA
      if ((v.opomba || '').includes('MEJA') || (v.ime || '').includes('18 / 81')) {
        issues.push(`${skan}: MEJA-vrstica: ${(v.ime || v.opomba || '').slice(0, 80)}`);
      }
      continue;
    }
    // exclude tail-of-1880 rows (zaporedna 72 on s171 = tail-1880, December 1880)
    if (skan === 's171' && v.zaporedna === '72') {
      issues.push(`${skan}: TAIL-1880-vrstica z72 (${(v.ime||'').slice(0,50)}) — izključena iz 93`);
      continue;
    }
    out.push({
      skan, pag,
      zaporedna: v.zaporedna,
      mesec: v.mesec ?? null,
      smrt: v.smrt ?? null,
      pokop: v.pokop ?? null,
      vas: v.vas ?? null,
      hisna: v.hisna ?? null,
      ime: v.ime ?? null,
      stan: v.stan ?? null,
      starost: v.starost ?? null,
      bolezen: v.bolezen ?? null,
      previden: v.previden ?? null,
      duhovnik: v.duhovnik ?? null,
      opomba: v.opomba ?? null,
    });
  }
}

// duplicate check
const seen = new Map();
for (const e of out) {
  const k = e.zaporedna;
  if (seen.has(k)) issues.push(`DUPLIKAT-z${k}: ${seen.get(k)} → ${e.skan}-${(e.ime||'').slice(0,40)}`);
  else seen.set(k, `${e.skan}-${(e.ime||'').slice(0,40)}`);
}

// sequence order check (as read: file order)
const order = out.map(e => e.zaporedna);
console.log('Vrstni-red:', order.join(','));
console.log('SKUPAJ:', out.length);
console.log('--- issues ---');
for (const i of issues) console.log(i);
fs.writeFileSync('/tmp/p196/entries_raw.json', JSON.stringify(out, null, 1));

// compact table print
console.log('--- tabela ---');
for (const e of out) {
  const ime = (e.ime || '').slice(0, 38);
  const vas = (e.vas || '').slice(0, 14);
  const stan = (e.stan || '').slice(0, 24);
  const bol = (e.bolezen || '').slice(0, 26);
  const duh = (e.duhovnik || '').slice(0, 18);
  console.log(`z${e.zaporedna}|${e.skan}|${e.mesec||'?'}|s${e.smrt||'?'}/p${e.pokop||'?'}|${vas}|h${e.hisna||'?'}|${ime}|${stan}|${e.starost||'?'}|${bol}|${duh}`);
}
