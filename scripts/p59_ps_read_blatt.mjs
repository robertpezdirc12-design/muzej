// P59 — branje glav listov registra PS ("Nro. des Blattes") iz izrezov levega
// stolpca. Metoda P57: neodvisni VLM prehodi na izrez, glm-5v-turbo, [~]
// negotovo; številke TOČNO kot napisane. Izrez vsebuje 3 stolpce:
//   1) Nro. des Blattes  — rimske številke, samo kjer dejansko izpisano
//   2) Bezeichnung des Grundstückes/Riede — navadno prazen
//   3) Nro. der Parzelle — številke (samokontroliranje vs pageMap P56)
// Vhod: /tmp/p59/send-<page>.jpg (p59_fetch_strip.py: 3× Lanczos, q92)
// Izhod: research/issue17/ps-raw/blatt-<page>{,-pass2,-pass3}.json
//        {page, pass, model, created, usage?, content} — content = JSON:
//        {"parzellen": [...], "blatt": [{"value","atParzella"}], "opomba": "..."}
// Uporaba: node scripts/p59_ps_read_blatt.mjs "5-14" | "7" | "7:2" | "5-20,61"
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

const OUT_DIR = 'research/issue17/ps-raw';
const IMG_DIR = '/tmp/p59';

function promptFor(page) {
  return `To je LEVI DEL tabele iz strani ${page} katastrskega registra "Der Grund-Parcellen der Gemeinde GRÜBLE" (k.o. Griblje, franciscejski kataster 1825), nemška Kurrent pisava, deloma rdeči tuš. Izrez vsebuje do trije stolpci tabele (od leve proti desni):
1. "Nro. des Blattes" — rimske številke (I, II, III, IV ...) ali arabske; izpisane SAMO v vrstici, kjer se Blatt začne/spremeni; v nadaljnjih vrsticah so ditto znamenja (dve majhni piki/kljukici " = isto kot zgoraj).
2. "Bezeichnung des Grundstückes / der Riede" — navadno prazen ali rokopisna opomba.
3. "Nro. der Parzelle" — arabske številke parcel (npr. 41, 42, ... 60).

PRAVILA:
- Iz stolpca 3 ("Nro. der Parzelle") prepiši VSE številke od zgoraj navzdol, TOČNO kot so napisane (ne popravljaš, ne seštevaš). Vsaki vrstici tabele pripiši zaporedni indeks (1 = prva vrstica pod glavo tabele).
- POZOR NA KURRENT CIFRE: števka 4 ima zanko in je lahko podobna 8 ali 9; števka 1 je ozka črtica (ne izpusti je pri trimestnih številkah — npr. 161 je TRI cifre, ne dve); števka 7 ima prečko; števka 5 je lahko podobna 6. Preštej cifre vsake številke. Številke so navadno NARAŠČajoče od zgoraj navzdol (z rdeče prečrtanimi vrsticami vmes) — če tvoje branje ni naraščajoče, dvomljive cifre označi [~].
- Iz stolpca 1 ("Nro. des Blattes") prepiši SAMO številke, ki so DEJANSKO izpisane (ditto znamenj NE prepišeš kot številke!) — vsako z vrstičnim indeksom (in parcelno številko, če je berljiva). Če je numerala prečrtana ali popravljena, prepiši vidno (končno) vrednost in v opomba dodaj [~].
- Negotovo branje označi z [~] (za vrednostjo), neberljivo z [?]. Ne izmišljuj si. Prazni stolpci ostanejo prazni.
- Če je stolpec 1 na celotni strani BREZ izpisane numerele (samo ditto), vrni prazen seznam "blatt".
- Izhod: SAMO en veljaven JSON objekt (brez ograj, brez komentarjev, brez markdown) v tvorci:
{"vrstice": [{"row": 1, "parzella": "41"}, {"row": 2, "parzella": "42"}], "blatt": [{"value":"I","row":1,"atParzella":"41"}], "opomba": "..." ali null}`;
}

function parseContent(content) {
  const t = content.trim().replace(/^```(json)?/i, '').replace(/```$/, '').trim();
  const a = t.indexOf('{');
  const b = t.lastIndexOf('}');
  if (a < 0 || b < 0) throw new Error('ni JSON v odgovoru');
  return JSON.parse(t.slice(a, b + 1));
}

async function readStrip(zai, page, pass) {
  const img = `${IMG_DIR}/send-${page}.jpg`;
  const b64 = fs.readFileSync(img).toString('base64');
  const call = zai.chat.completions.createVision({
    messages: [{ role: 'user', content: [
      { type: 'text', text: promptFor(page) },
      { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${b64}` } }
    ]}],
    thinking: { type: 'disabled' }
  });
  const completion = await Promise.race([
    call,
    new Promise((_, rej) => setTimeout(() => rej(new Error('TIMEOUT 180s')), 180000))
  ]);
  return completion;
}

async function main() {
  const args = process.argv.slice(2);
  const jobs = [];
  if (args.length) {
    for (const a of args) {
      for (const part of a.split(',')) {
        const [pStr, nStr] = part.split(':');
        if (!pStr.includes('-')) {
          const p = Number(pStr);
          if (!p) continue;
          if (nStr) jobs.push([p, Number(nStr)]);
          else jobs.push([p, 1], [p, 2]);
        } else {
          const [a1, a2] = pStr.split('-').map(Number);
          for (let p = a1; p <= a2; p++) {
            if (nStr) jobs.push([p, Number(nStr)]);
            else jobs.push([p, 1], [p, 2]);
          }
        }
      }
    }
  } else {
    for (let p = 5; p <= 139; p++) jobs.push([p, 1], [p, 2]);
  }
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const zai = await ZAI.create();
  let ok = 0, fail = 0;
  for (const [p, n] of jobs) {
    const suffix = n === 1 ? '' : `-pass${n}`;
    const out = `${OUT_DIR}/blatt-${p}${suffix}.json`;
    if (fs.existsSync(out)) { console.log(`stran ${p} prehod ${n}: že obstaja, preskočim`); ok++; continue; }
    const t0 = Date.now();
    let completion = null;
    for (let attempt = 1; attempt <= 6; attempt++) {
      try {
        console.log(`stran ${p} prehod ${n}: poskus ${attempt} ...`);
        completion = await readStrip(zai, p, n);
        break;
      }
      catch (e) {
        const is429 = e.message.includes('429') || e.message.toLowerCase().includes('too many');
        console.error(`stran ${p} prehod ${n}: poskus ${attempt} napaka: ${e.message.slice(0, 120)}`);
        if (!is429 && attempt >= 4) break;
        await new Promise(r => setTimeout(r, is429 ? 25000 : 8000));
      }
    }
    if (completion) {
      const content = completion.choices[0]?.message?.content ?? '';
      let rec = { page: p, pass: n, model: 'glm-5v-turbo', created: Math.floor(Date.now() / 1000) };
      if (completion.usage) rec.usage = completion.usage;
      try {
        rec.parsed = parseContent(content);
        rec.content = content;
      } catch (e) {
        rec.content = content;
        rec.parseError = e.message;
        console.error(`stran ${p} prehod ${n}: JSON PARSE NAPAKA — ${e.message.slice(0, 80)}`);
      }
      fs.writeFileSync(out, JSON.stringify(rec, null, 1) + '\n');
      const np = rec.parsed ? rec.parsed.parzellen?.length ?? '?' : '?';
      const nb = rec.parsed ? rec.parsed.blatt?.length ?? '?' : '?';
      console.log(`stran ${p} prehod ${n}: OK (${((Date.now() - t0) / 1000).toFixed(0)}s, parcele ${np}, blatt ${nb})`);
      ok++;
    } else {
      console.error(`stran ${p} prehod ${n}: NEUSPEH po vseh poskusih`);
      fail++;
    }
    await new Promise(r => setTimeout(r, 3000));
  }
  console.log(`KONEC: ${ok} OK, ${fail} NEUSPEH`);
  process.exit(fail > 0 ? 1 : 0);
}

main();
