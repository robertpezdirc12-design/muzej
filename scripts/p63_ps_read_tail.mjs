// P63 — branje zaključnih strani registra PS (138–139): lastninska tabela
// ("Des Eigenthümers": Parzelle → Dominical/Rustical → Haus Nº → Vor und
// Zuname → Stand → Wohnort) + kultura tabela ("Des Grundstückes": Kulturs
// Gattung → Flächen Inhalt → Classe → Reiner Ertrag → Capital Werth →
// Anmerkung) + bledi ostanki p138. Metoda P59: neodvisni VLM prehodi,
// glm-5v-turbo, [~] negotovo, številke TOČNO kot napisane.
// Vhod: /tmp/p63/p138-left.jpg, p138-right.jpg, p139-full-a.jpg,
//       p139-full-b.jpg, p139-right-a.jpg, p139-right-b.jpg
// Izhod: research/issue17/ps-raw/tail-<target>-<part>.json
//        {target, part, model, created, usage?, content} — content = JSON
// Uporaba: node scripts/p63_ps_read_tail.mjs            (vseh 6 delov)
//          node scripts/p63_ps_read_tail.mjs 139-left:2 (izbrani del)
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

const OUT_DIR = 'research/issue17/ps-raw';
const IMG_DIR = '/tmp/p63';

const PARTS = [
  ['139-left', 'a'], ['139-left', 'b'],
  ['139-right', 'a'], ['139-right', 'b'],
  ['138-left', 'a'], ['138-right', 'a'],
];

const IMG_OF = {
  '139-left:a': 'p139-full-a.jpg',
  '139-left:b': 'p139-full-b.jpg',
  '139-right:a': 'p139-right-a.jpg',
  '139-right:b': 'p139-right-b.jpg',
  '138-left:a': 'p138-left.jpg',
  '138-right:a': 'p138-right.jpg',
};

function promptFor(target, part) {
  if (target === '139-left') {
    return `To je LEVA knjižna stran tabele iz strani 139 zaključka registra "Der Grund-Parcellen der Gemeinde GRÜBLE" (k.o. Griblje, 1825), nemška Kurrent pisava, deloma rdeči tuš.${part === 'b' ? ' Ta izrez je SPODNJA polovica strani (vrstice 11–20).' : ' Ta izrez je ZGORNJA polovica strani (vrstice 1–10) z glavo tabele.'}
Stolpci (od leve): "Nro. des Blattes" | "Benennung des Riedes" | "Nro. der Parzelle" | "Dominical" (pod skupno glavo "Gesetzliche Eigenschaft des Grundstückes") | "Rustical" (3 podkolone) | "Haus Nro." | "Vor und Zuname" | "Stand" | "Wohnort".

PRAVILA:
- Prepiši VSAKO vrstico od zgoraj navzdol, TOČNO kot je napisano (ne popravljaš, ne seštevaš). Vsaki vrstici pripiši zaporedni indeks (1 = prva vrstica pod glavo; v izrezu b nastavi ${part === 'b' ? 'indeks tako, da prva vidna vrstica dobi indeks 11' : 'indeks 1 za prvo vrstico'}).
- POZOR NA KURRENT CIFRE: 4 ima zanko in je podobna 8/9; 1 je ozka (161 je TRI cifre); 7 ima prečko; 5 podobna 6. Preštej cifre.
- "Nro. der Parzelle" je navadno NARAŠČajoče (41–60) — samokontrola: če tvoje branje ni naraščajoče, označi dvomljive cifre [~].
- "Nro. des Blattes": prepiši SAMO dejansko izpisano numerele (ditto znamenja — dve piki — NE prepišeš kot številko!). Numerala je lahko rimska (npr. IIb ali IIᵇ) ali arabska — prepiši vidno obliko (npr. "IIb" če vidíš dve veliki črti + malo b; "11b" če sta izpisani dve arabski enici).
- "Haus Nro." in "Wohnort" nosita pogosto RDEČO tuš; "Vor und Zuname" lahko vsebuje rokopisne ŠTEVILKE ali kratico (prepiši točno vidno, npr. "62." ali "G. l. fin." — ne izmišljuj imen!). "Rustical" podkolone so navadno prazne.
- Prazni stolpci ostanejo prazni (null ali ""). Negotovo označi [~], neberljivo [?].
- Izhod: SAMO en veljaven JSON objekt (brez ograj, brez komentarjev):
{"vrstice": [{"row": 1, "blatt": "IIb", "benennung": null, "parzelle": "41", "dominical": "1", "rustical": null, "haus": "1082", "vorUndZuname": "G. l. fin.", "stand": null, "wohnsort": "63"}], "opomba": "..." ali null}`;
  }
  if (target === '139-right') {
    return `To je DESNA knjižna stran tabele iz strani 139 zaključka registra "Der Grund-Parcellen der Gemeinde GRÜBLE" (k.o. Griblje, 1825), nemška Kurrent pisava, deloma rdeči tuš. Glava nad tabelo: "Des Grundstückes".${part === 'b' ? ' Ta izrez je SPODNJA polovica (vrstice ~91–100 + vsote).' : ' Ta izrez je ZGORNJA polovica (vrstice ~81–90) z glavo.'}
Stolpci: "Kulturs Gattung." | "Flächen Inhalt." (podkoloni "N. Oe. Sache" in "Quadrat Klafter") | "Classe." | "Reiner jährlicher Ertrag, in Metall-Münze" (podkoloni "fl." in "kr.") | "Capital Werth nach p.Ct." (podkoloni "fl." in "kr.") | "Anmerkung."

PRAVILA:
- Prepiši VSAKO vrstico od zgoraj navzdol, TOČNO kot je napisano. Vsaki vrstici pripiši zaporedni indeks (${part === 'b' ? 'prva vidna vrstica v izrezu naj dobi indeks 11' : 'prva vrstica pod glavo dobi indeks 1'}).
- "Kulturs Gattung" je zaporedje številk (81–100); "Classe" je drugače zaporedje (101–120) — prepiši TOČNO, brez poenotenja.
- Rdeči tuš: "Ertrag kr." in "Capital Werth" vrednosti so pogosto rdeče; prepiši vse cifre TOČNO (Kurrent pasti: 4≈8/9; 1 ozka; 7 s prečko; 5≈6).
- Spodnje vsote (pod debelo črto) vpiši v posebno polje "vsote" (samo v delu b): {"row": ..., "stolpec": "vrednost"} — kot jih vidiš (npr. "Fürtrag 189 | 1228", "125 | 183", "162 | 1447").
- Prazni stolpci null. Negotovo [~], neberljivo [?].
- Izhod: SAMO en veljaven JSON objekt:
{"vrstice": [{"row": 1, "kultur": "81", "noe": "4", "klafter": "590", "classe": "101", "ertragFl": null, "ertragKr": "146", "capitalFl": "1860", "capitalKr": null, "anmerkung": null}], "vsote": [{"opis": "Fürtrag", "kol1": "189", "kol2": "1228"}], "opomba": "..." ali null}`;
  }
  // 138-left: bledi ostanki
  if (target === '138-left') {
    return `To je LEVA knjižna stran tabele iz strani 138 zaključka registra "Der Grund-Parcellen der Gemeinde GRÜBLE" (k.o. Griblje, 1825) — tabela je skoraj POVSEM IZBRISANA/NEZAPISANA; ostali so samo BLEDI OSTANKI prejšnjih zapisov (izprana ali izbrisana kreda/tuš). Nemška Kurrent pisava.
Stolpci (od leve): "Nro. des Blattes" | "Benennung der Riedes" | "Nro. der Parzelle" | "Dominical" | "Rustical" (3 podkolone) | "Haus Nro." | "Vor und Zuname" (s rokopisnimi podglavami) | "Stand" | "Wohnort".

PRAVILA:
- Glej ZELO POZORNO (bledi zapisi!). Vpiši VSAK vidni ostanek številke/črke s svojim vrstnim indeksom in stolpcem. Izbrisane/prazne vrstice vrni kot {"row": N, ...prazno}.
- Zapis, ki izgleda kot "T. 191" / "7. 191" / "T.191" pri vrstici ~14 v stolpcu "Nro. des Blattes": prepiši TOČNO, kar vidiš, z [~] (razloči T/7/J, 9/0, 1/II). Enako za "89" / "86" pri vrstici ~27.
- Pri vrsticah ~14–15 v stolpcu "Nro. der Parzelle" so sledi številk (23? 24? 25?) — prepiši najbolj verjetno z [~].
- Ročno podglave pod "Vor und Zuname" (rokopis: npr. "Lotus" / "Lung" / "Al"?) — prepiši v "opomba", najbolje kot vidiš z [~].
- Izhod: SAMO en veljaven JSON objekt:
{"vrstice": [{"row": 1, "blatt": null, "benennung": null, "parzelle": null, "dominical": null, "rustical": null, "haus": null, "vorUndZuname": null, "stand": null, "wohnsort": null}, {"row": 14, "blatt": "T. 191[~]", "parzelle": "23[~]"}], "opomba": "..." ali null}`;
  }
  // 138-right
  return `To je DESNA knjižna stran tabele iz strani 138 zaključka registra "Der Grund-Parcellen der Gemeinde GRÜBLE" (k.o. Griblje, 1825), nemška Kurrent pisava, veliko rdečega tuša z PREČRTANJMI. Glava je lahko enaka sosednji strani ("Des Grundstückes": Kulturs Gattung | Flächen Inhalt (N. Oe. Sache | Quadrat Klafter) | Classe | Reiner Ertrag (fl | kr) | Capital Werth | Anmerkung).

PRAVILA:
- Prepiši VSAKE vidne vrstice s številkami: prvi stolpec ("Kulturs Gattung" ali zaporedje ~18–40), "N. Oe. Sache", "Quadrat Klafter", rdeče vrednosti. Vsaki vrstici zaporedni indeks (1 = prva vidna).
- Rdeče PREČRTANE vrstice označi: dodaj polje "precrtana": true.
- Vsote pod debelo črto (npr. "Suma 120", "Suma 403" ali podobno) vpiši v "vsote".
- Bledi/izbrisani ostanki z [~]; neberljivo [?]; prazno null.
- Izhod: SAMO en veljaven JSON objekt:
{"vrstice": [{"row": 1, "kultur": "18", "noe": null, "klafter": null, "classe": null, "ertragFl": null, "ertragKr": null, "capitalFl": null, "capitalKr": null, "anmerkung": null, "precrtana": false}], "vsote": [{"opis": "Suma", "kol1": "120"}], "opomba": "..." ali null}`;
}

function parseContent(content) {
  const t = content.trim().replace(/^```(json)?/i, '').replace(/```$/, '').trim();
  const a = t.indexOf('{');
  const b = t.lastIndexOf('}');
  if (a < 0 || b < 0) throw new Error('ni JSON v odgovoru');
  return JSON.parse(t.slice(a, b + 1));
}

async function main() {
  const args = process.argv.slice(2);
  const jobs = [];
  for (const a of (args.length ? args : PARTS.map(([t, p]) => `${t}:${p}`))) {
    const [tp] = a.split(':');
    for (const [t, p] of PARTS) if (`${t}:${p}` === a || (args.length && a === tp)) jobs.push([t, p]);
  }
  if (!jobs.length) { console.error('ni veljavnih delov'); process.exit(1); }
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const zai = await ZAI.create();
  let ok = 0, fail = 0;
  for (const [target, part] of jobs) {
    const out = `${OUT_DIR}/tail-${target}-${part}.json`;
    if (fs.existsSync(out)) { console.log(`tail ${target} del ${part}: že obstaja, preskočim`); ok++; continue; }
    const img = `${IMG_DIR}/${IMG_OF[`${target}:${part}`]}`;
    if (!fs.existsSync(img)) { console.error(`tail ${target} del ${part}: manjka izrez ${img}`); fail++; continue; }
    const t0 = Date.now();
    let completion = null;
    for (let attempt = 1; attempt <= 6; attempt++) {
      try {
        console.log(`tail ${target} del ${part}: poskus ${attempt} ...`);
        const b64 = fs.readFileSync(img).toString('base64');
        completion = await Promise.race([
          zai.chat.completions.createVision({
            messages: [{ role: 'user', content: [
              { type: 'text', text: promptFor(target, part) },
              { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${b64}` } }
            ]}],
            thinking: { type: 'disabled' }
          }),
          new Promise((_, rej) => setTimeout(() => rej(new Error('TIMEOUT 180s')), 180000))
        ]);
        break;
      }
      catch (e) {
        const is429 = e.message.includes('429') || e.message.toLowerCase().includes('too many');
        console.error(`tail ${target} del ${part}: poskus ${attempt} napaka: ${e.message.slice(0, 120)}`);
        if (!is429 && attempt >= 4) break;
        await new Promise(r => setTimeout(r, is429 ? 25000 : 8000));
      }
    }
    if (completion) {
      const content = completion.choices[0]?.message?.content ?? '';
      const rec = { target, part, model: 'glm-5v-turbo', created: Math.floor(Date.now() / 1000) };
      if (completion.usage) rec.usage = completion.usage;
      try {
        rec.parsed = parseContent(content);
        rec.content = content;
      } catch (e) {
        rec.content = content;
        rec.parseError = e.message;
        console.error(`tail ${target} del ${part}: JSON PARSE NAPAKA — ${e.message.slice(0, 80)}`);
      }
      fs.writeFileSync(out, JSON.stringify(rec, null, 1) + '\n');
      const nr = rec.parsed ? rec.parsed.vrstice?.length ?? '?' : '?';
      console.log(`tail ${target} del ${part}: OK (${((Date.now() - t0) / 1000).toFixed(0)}s, vrstice ${nr})`);
      ok++;
    } else {
      console.error(`tail ${target} del ${part}: NEUSPEH po vseh poskusih`);
      fail++;
    }
    await new Promise(r => setTimeout(r, 3000));
  }
  console.log(`KONEC: ${ok} OK, ${fail} NEUSPEH`);
  process.exit(fail > 0 ? 1 : 0);
}

main();
