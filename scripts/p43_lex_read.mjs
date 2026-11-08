// P43 — leksikografska kampanja za 16 neznanih družin + kitice (issue #10).
// 2 neodvisna prehoda na sklop, besedilni LLM (brez slike), [~] verjetno /
// [?] morda (metoda P36/P41). Vhod: /tmp/ps43_lex_evidence/<fam>.json
// Izhod: research/issue17/ps-lexicon-raw/<fam>-pass<n>.json
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

const EVID_DIR = '/tmp/ps43_lex_evidence';
const OUT_DIR = 'research/issue17/ps-lexicon-raw';

const CONTEXT = `Zgodovinski kontekst (uporabi ga, ne izmišljuj novega):
- Vir: N083PS, "Protocoll der Grund-Parcellen der Gemeinde GRÜBLE", franciscejski kataster 1825, katastrska občina Griblje (Griebl), Bela krajina (danes Občina Črnomelj, Slovenija); Arhiv RS SI AS 176. Pisava: nemška Kurrent, piskropi (pisar) piše nemško, lastniška imena so pretežno slovenska (Krischan, Wrischan, Pesdiz, Schimey, Knall, Scheuring …).
- Stolpec "Kultur's Gattung" v registrskih vrsticah vsebuje mešanico:
  (a) uradnih kategorij rabe (Acker, Wiese, Wald, Hutweide/Weide, Alm, Weingarten, Garten, Ödung, Bauplatz …), kot jih 1:1 navaja uradni izkaz "AUSWEIS über die Benützungsart des Bodens" (PV, 10. 1. 1825) — in
  (b) LOKALNIH besed, ki med uradnimi kategorijami NISO — to so bodisi LEDINSKA IMENA (imena polj/travnikov/gozdov, ki jih je pisar zapisal namesto ali poleg rabe), bodisi narečni izrazi za rabo, bodisi okrajšave.
- Belokranjska krajina 1825: velike skupne pašnike z drevjem (dubrava, nem. Hutweide/Waldweide — uradno "Weiden" 636 J 263 K = 52 % občine!), njive 413 J, travniki 76+12 J, vinogradi 7 J.
- Dva neodvisna strojna prehoda OCR (VLM) že obstajata; "nasprotni prehod" = drugo branje iste fotografije. GENERIČNI PADCEK = en prehod prebere generično besedo (Wiese/Acker), drugi specifično (neznano) — to dokazuje, da je specifična beseda v viru dejansko zapisana.
- Pogoste Kurrent zamenjave pri strojnem branju: R↔L, h v sredini besede, u/n, t/p/f, ij/y, š/sg/sch, dolžina samoglasnikov.`;

function evidenceText(d) {
  const lines = [];
  lines.push(`DRUŽINA: ${d.family}`);
  const cp = d.crossPass || {};
  lines.push(`Pari (parcela×raba, pass2wins): ${cp.pairs ?? '?'}`);
  lines.push(`Variante zapisa (št. parov): ${JSON.stringify(cp.variants || {})}`);
  lines.push(`Stabilnih parov (oba prehoda enako, do ločila): ${cp.stablePairs ?? 0}; generični padcek: ${cp.fallbackPairs ?? 0}; brez nasprotnega branja: ${cp.noCounterpart ?? 0}`);
  const b = d.block || {};
  lines.push(`Fotografije (strani skena): ${JSON.stringify(b.pages || [])}; teki sosednjih parcel: ${b.contiguousRuns ?? '?'}; parcele ${b.parcelMin ?? '?'}–${b.parcelMax ?? '?'}`);
  if (d.family === 'SINGLES') {
    lines.push('KITICE (posamezne vrednosti, po pogostosti):');
    for (const [raw, occ] of Object.entries(d.groupedRaw || {})) {
      const o = occ[0];
      lines.push(`  "${raw}" ×${occ.length} (npr. parcela ${o.parcel}, stran ${(o.pages||[]).join(',')}, nasprotno branje: ${o.counterparts.map(c => `"${c.kultur}"`).join('; ') || '—'})`);
    }
  } else {
    lines.push('POJAVITVE (parcela, stran, zapis, površina J/K, lastnik, nasprotno branje):');
    for (const o of (d.occurrences || []).slice(0, 40)) {
      const cps = (o.counterparts || []).map(c => `${c.pass === 1 ? 'P1' : 'P2'}:"${c.kultur}"`).join('; ');
      lines.push(`  parz ${o.parcelAsRead}, str ${(o.pages || []).join(',')}: "${o.raw}" ${o.joch ?? ''}J${o.klafter ?? ''}K ${o.owner ? '[' + o.owner + ']' : ''} — nasprotno: ${cps || '—'}`);
    }
  }
  return lines.join('\n');
}

function promptFor(d) {
  return `${CONTEXT}

DOKAZI (iz committed OCR prehodov in P39 modela):
${evidenceText(d)}

NAVALOŽENOST POJAVITEV: ${d.family === 'SINGLES'
    ? 'to so KITICE — posamezne vrednosti brez jasnih družin; večina je verjetno okrnjenih ali od-mašinet-prebranih oblik ZNANIH terminov (npr. Einfach lahko zadeva Einschlag ali pa je samostojen termin "Fach" = poljni pas).'
    : 'vse pojavitve te družine so dobesedno ena (leksikalno) vrednost v stolpcu rabe.'}

VPRAŠANJE — odgovori izključno kot JSON (brez ograj, brez komentarjev):
{
 "termTypeHypothesis": "LEDINSKO-IME | KULTURA-DIALEKT | KULTURA-KOMPOZIT | OKRAJSAVA | ARTIFAKT | NEZNANO",
 "hypotheses": [
   {
     "candidate": "normalizirana kandidat-beseda (nemška ali slovenska pomanjšana/dialektna oblika, npr. 'Hut' ali 'Log')",
     "glossSi": "kaj pomeni v slovenščini in zakaj bi se pojavila v stolpcu rabe",
     "source": "slovar/delo, kjer je ta pomen dokumentiran (npr. 'Schmeller, Bayerisches Wörterbuch' ali 'SSKJ' ali 'Kärntner Wörterbuch' ali 'Pleteršnik' ali 'Bezlaj' ali 'DWB (Grimm)')",
     "confidence": "~ ali ?"
   }
 ],
 "sources": ["izrecno našteti vsi slovarji/viri, ki jih navajaš"],
 "noteSi": "kratek paleografsko-jezikovni komentar (Kurrent zamenjave, narečni kontekst, kritika lastnih hipotez)"
}

PRAVILA:
- NIČesar NE prirejaj: ne spreminjaj zapisov, ne klasificiraj rabe (razred ostaja NEKLASIFICIRANO).
- Vsaka hipoteza MORA imeti vir (slovar/delo). Če vira ne znaš izrecno, navedi 'neznano — hipoteza brez dokumentiranega vira' in zaupanje [?].
- Največ 5 hipotez; če ni nič pametnega, je termTypeHypothesis NEZNANO in hypotheses prazen seznam.
- Upoštevaj KVANTITATIVNI kontekst: če je družina velika (desetino parov) in vezana na eno fotografijo, je LEDINSKO-IME verjetnejše kot splošni narečni termin.
- Kurrent: L/R, h, u/n, t/p, sch/š so pogoste zamenjave — oceni, ali bi lahko variantam družine skupna KURRENT-forma.`;
}

async function readOne(zai, fam, pass, evidence) {
  const call = zai.chat.completions.create({
    messages: [
      { role: 'system', content: 'Si strogo zgodovinsko-jezikovni analitik; odgovarjaš izključno z veljavnim JSON, brez zamišljanja virov. Neizbežno neznano označiš z [?].' },
      { role: 'user', content: promptFor(evidence) }
    ],
    thinking: { type: 'disabled' }
  });
  const completion = await Promise.race([
    call,
    new Promise((_, rej) => setTimeout(() => rej(new Error('TIMEOUT 180s')), 180000))
  ]);
  return completion.choices[0]?.message?.content ?? '';
}

async function main() {
  const only = process.argv.slice(2);
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const files = fs.readdirSync(EVID_DIR).filter(f => f.endsWith('.json'))
    .map(f => f.replace(/\.json$/, ''));
  const targets = only.length ? only : files;
  const zai = await ZAI.create();
  let ok = 0, fail = 0;
  for (const fam of targets) {
    const evidence = JSON.parse(fs.readFileSync(`${EVID_DIR}/${fam}.json`, 'utf8'));
    for (const n of [1, 2]) {
      const out = `${OUT_DIR}/${fam}-pass${n}.json`;
      if (fs.existsSync(out)) { console.log(`${fam} prehod ${n}: že obstaja, preskočim`); ok++; continue; }
      const t0 = Date.now();
      let raw = null;
      for (let attempt = 1; attempt <= 5; attempt++) {
        try {
          console.log(`${fam} prehod ${n}: poskus ${attempt} ...`);
          raw = await readOne(zai, fam, n, evidence);
          break;
        } catch (e) {
          const is429 = e.message.includes('429') || e.message.toLowerCase().includes('too many');
          console.error(`${fam} prehod ${n}: poskus ${attempt} napaka: ${e.message.slice(0, 120)}`);
          if (!is429 && attempt >= 3) break;
          await new Promise(r => setTimeout(r, is429 ? 25000 : 8000));
        }
      }
      if (raw) {
        fs.writeFileSync(out, JSON.stringify({ family: fam, pass: n, model: 'glm-5v-turbo (besedilni)', created: Math.floor(Date.now() / 1000), raw, ms: Date.now() - t0 }, null, 1));
        console.log(`${fam} prehod ${n}: OK (${((Date.now() - t0) / 1000).toFixed(0)}s, ${raw.length} znakov)`);
        ok++;
      } else {
        console.error(`${fam} prehod ${n}: NEUSPEH po vseh poskusih`);
        fail++;
      }
      await new Promise(r => setTimeout(r, 3500));
    }
  }
  console.log(`končano: OK ${ok}, FAIL ${fail}`);
}

main().catch(e => { console.error(e); process.exit(1); });
