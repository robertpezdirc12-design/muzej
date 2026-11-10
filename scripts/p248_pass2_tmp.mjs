// P248 pass-2: VLM na 19 kropih (vrstice) + 24 mikro-kropih
import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';

const DIR = '/home/z/p248tmp';
const OUT = `${DIR}/pass248`;

const rowPrompt = (id, hint) => `To je ULTRA-ZOOM krop ene vrstice (vpisa) poročne knjige Podzemelj, ${id}. Kontekst: ${hint}. Prepiši VSAKO polje natančno znak za znak (Kurrent-rokopis, nemško):
- marginalna številka v levi margini (tudi prečrtane/popravljene!),
- datum (leto/mesec/dan — če manjka letnica ALI mesec, reci EXPLICITNO!),
- ženin: Wohnort + hišna št. (pazi: "Griblje N" / "Gri. šte. N" / "Gübl." / kraj+št.), priimek+ime, stan (Bauer/Leinweber/Inwohner/Häusler/Sohn...), starost,
- nevesta: Wohnort + hišna št., priimek+ime (tudi roj./geb./verw./-tochter opombe!), stan, starost,
- starši ženina: oče (ime+priimek+stan) + mati (ime+roj. priimek),
- starši neveste,
- Befunde: vsa besedila (Gemeindezettel-datum, Konsens, Dispens, priče, mladoletnost, bolezni, sodišča!),
- podpis duhovnika (prepiši ime — pazi: "Dovgan" ima lahko garble D/B/P!).
Negotovo=[~], neberljivo=[?]. Izhod: SAMO veljaven JSON:
{"id": "${id}", "m": "...", "datum": "...", "zenin": "...", "nevesta": "...", "elternZenin": "...", "elternNevesta": "...", "befunde": "...", "podpis": "...", "note": "..."}`;

const hints = {
  's11-r1-row': 'RESTART-1876 vpis-1 (margina 1): ženin Gri.šte 31 Nicolaus Krupanič[~] 34-l, nevesta Gri.šte 44 Katarina Pegdire 20-l, Befunde Gemeindezettel woher Griblje dd. 8.[?] 1876.',
  's11-r2r3-rows': 'vpisi 2–3 (margine 2–3), datumi "16.", vpis-2 ženin Johann Tome 24-l Škri.še 1 × Mlakve 11 Maria Jurejevič 18-l; vpis-3 Mathias Pasič 45-l Desinec 3 × Cerhin.šte 18 Anna Movrin 41-l.',
  's11-r4r5-rows': 'vpisi 4–5 (margine 4–5), datumi "16.", vpis-4 Georg Movrin 29-l Cerhin.šte 15 × Desinec 3 Margareh Pasič 19-l (IZMENA-VLOG kandidat z v3!); vpis-5 Georg Jurejevič 40-l Cerhin.šte 17 × Krasinec 20 Dorothea Škrabanič 26-l.',
  's12-r6r7-rows': 'vpisi 6–7 (margine 6–7), v6: datum "1876. Febr. 16.", ženin [Gradac?] 36 Mathias Mohlorič[~] 28-l × Dobranice 8 Margareta Štefanič 22-l; v7: "16.", Dobranice 8 Jakob Štefanič 25-l × Podzgemeľ 6 Barbara Tome 40-l (DISPENS 3. krvno-sorodstveni kandidat!).',
  's12-r8-row': 'vpis-8 (margina 8): datum "16.", ženin Gri.šte 35 Mathias Križan[~Hrižan]-[Leinann?] 20-ali-22-l × Gri.šte 64 Anna Požeh 19-l; starši neveste morda Mathias Pegdire × Maria Krasovec; Befunde z zettelom Griblje dd. 15.Feb + vojaška omamba kandidat.',
  's12-r9-row': 'vpis-9 (margina 9): datum "23.", ženin Femeli[~Zemelj?] 19 Nikolaus Mihelič[~Milek] 22-l × Boršt 23 Barbara Pegdire 21-l; starši neveste morda Georg Pegdire × Anna Tome; Befunde dispens-kandidat.',
  's13-r10-row': 'vpis-10 (margina 10): datum "1876. Februar 23.", ženin [Vinica?] 1 Johann Županič/Kupanič 23-l × Krasina 63[~43?] Anna Bahovič 17-l MMLADOLETNICA; podpis duhovnika!',
  's13-r11r12-rows': 'vpisi 11–12 (margine 11–12), v11: Velika-Gorica/Lipnik 9 Janko Mihelec 26-l × Adlešiči 16 Barbara Novak 22-l; v12: Graz/Windberg-48 Eduard Lingl 30-l × Graz/Blae 23 Josepa 29-l (vojak-oficir kandidat).',
  's13-r13-row': 'vpis-13 (margina 13): ženin Wsch 22 [55 prečrtano, popravka "z Griblje"!] Nicolaus Simec 22-l × Gri.šte 41 Maria Pegdire Leinmannstochter 20-l; starši neveste Georg Pegdire × Anna Brinc; priče Peter/Johann Mrh; Befunde "pro die minderj. Braut".',
  's14-r14-row': 'vpis-14 (margina 14): datum "1876. Novembris 15.", ženin [Wilsput?/A.Pfslph?] 18 Johann Jurgovič[~Jurgpovič] 20-l × Griblje 30 Anna Pegdire Leinmannstochter 20-l; starši neveste Markus Margon[?] × Mathiewa née Pegdire; Befunde Typhus + k.k. Bez.Gericht Metlika (Milfhing).',
  's14-r15-row': 'vpis-15 (margina 15): datum "20.", ženin Gradac 3 Anton Novak 33-l × Gradac 14 Rosalia Mascle 18-l; Befunde Gemeindezettel 19 Novembris 1876.',
  's11-tail-row': 'TAIL-1875 vrsta (vijolično črnilo, margina 8!): ženin [Gornje-Kamenice?] 3 Johann Blažek 31-l × [Gorica?] 1 Klemenčič[~] 23-l; Befunde VIJOLIČNO: Copulations-Erlaubnis + Einsegn-datumi; podpis kaplan Daniel Perschek[~Fošbek?].',
};

const mikroPrompts = {
  's11-r1-date-mikro': `ULTRA-ZOOM (6×) datumske celice RESTART-VPISA-1 na s11 poročne knjige. Besedilo je 3 vrstice: kratka predpona (npr. "de."), MES+"nar/ruar" beseda, in dan "9". VPRAŠANJE: ali mesec berš "Januar" ALI "Februar"? PRIMERJAJ črkovne oblike: Kurrent "J" = EN velik zankast lok z dolgim spuščanjem; Kurrent "F" = DVOJNI zgornji lok z vodoravno črto zgoraj. Prepiši znak za znak in zeloj razloži obliko prve črke meseca. {"id":"s11-r1-date-mikro","predpona":"...","mesec":"...","dan":"...","prvaCrka":"opis oblike","odgovor":"Januar|Februar|X-OPEN","note":"..."}`,
  's11-r1-befunde-mikro': `ULTRA-ZOOM (4×) Befunde-celice vpisa-1 na s11. Poišči datum ZETTLA: "Communalzettel/Gemeinezettel vn. Gemeinde woher Griblje dd. 8. [MES] 1876" — ali mesec berš "Februar" ALI "Januar" ALI "Jänner"? Prepiši celoten Befunde znak za znak. {"id":"s11-r1-befunde-mikro","befunde":"...","zettelDatum":"...","mesec":"Januar|Februar|Jänner|X-OPEN","note":"..."}`,
  's11-tail-date-mikro': `ULTRA-ZOOM (6×) datumske celice TAIL-VRSTE (vijolični vpis, leto 1875) na s11. Celica vsebuje: "1875" + MES + "3". Ali mesec berš "Dezembris" (D z več loki), "Februar", "Januar" ali kaj drugega? Prepiši znak za znak z opisom prve črke. {"id":"s11-tail-date-mikro","leto":"1875","mesec":"...","dan":"3","prvaCrka":"opis","odgovor":"...","note":"..."}`,
  's11-r1-strip': `ULTRA-ZOOM (3×) leve polovice vpisa-1 na s11 (ženin + nevesta). Prepiši: ženinovo hišno številko po "Gri. šte." (pričakovano 31), priimek+ime ženina (Krupanič/Kupanič/Zupanič-DUEL! + pripis pod imenom), starost (34?), nevestino hišno številko (44?), priimek (Pegdire?), starost (20?). {"id":"s11-r1-strip","zeninHisna":"...","zenin":"...","zeninPripis":"...","zeninStarost":"...","nevestaHisna":"...","nevesta":"...","nevestaStarost":"...","note":"..."}`,
  's11-r1-elternB': `ULTRA-ZOOM (4×) staršev neveste vpisa-1 na s11 (desna stran, 2. blok stolpcev). Pričakovano: oče "Georg Pegdire/Pegelič"-DUEL + mati "Agnes/Ana Škrvanič/Bahovič"-DUEL + morda tretja oseba "Nicolaus Bahovič". Prepiši VSE vrstice znak za znak. {"id":"s11-r1-elternB","ocee":"...","mati":"...","dodatno":"...","note":"..."}`,
  's12-m6-date-mikro': `ULTRA-ZOOM (4×) datumske celice VPISA-6 na s12 (prvi vpis lista). Pričakovano "1876. Febr. 16." — prepiši znak za znak, potrdi letnico in mesec. {"id":"s12-m6-date-mikro","datum":"...","letnica":"...","mesec":"...","dan":"...","note":"..."}`,
  's12-r8-hisne': `ULTRA-ZOOM (8×) ženinove hišne številke vpisa-8 na s12 za "Gri. šte." — pričakovano "35" — preveri: ali je 35 ALI 36/38/45? {"id":"s12-r8-hisna","stevilka":"...","zanesljivost":"...","note":"..."}`,
  's12-r8-hisneB': `ULTRA-ZOOM (8×) nevestine hišne številke vpisa-8 na s12 za "Gri. šte." — pričakovano "64" — preveri: ali je 64 ALI 6/6x/84/61? (Kurrent 6-vs-4 duel!) {"id":"s12-r8-hisnaB","stevilka":"...","prvaStevka":"6|?","drugaStevka":"4|?","zanesljivost":"...","note":"..."}`,
  's12-r8-age': `ULTRA-ZOOM (8×) ženinove starosti vpisa-8 na s12 — pričakovano "20" ali "22" — prepiši točno. {"id":"s12-r8-age","starost":"...","note":"..."}`,
  's12-r8-eltern': `ULTRA-ZOOM (3×) staršev vpisa-8 na s12 (desna stran): starši ŽENINA (pričakovano: Nicolaus Križan[~] × Maria née Gilah?) in starši NEVESTE (pričakovano: Mathias Pegdire × Maria Krasovec?). Prepiši VSE vrstice znak za znak. {"id":"s12-r8-eltern","elternZenin":{"ocee":"...","mati":"..."},"elternNevesta":{"ocee":"...","mati":"..."},"note":"..."}`,
  's12-r8-befunde': `ULTRA-ZOOM (4×) Befunde vpisa-8 na s12: pričakovano Gemeindezettel Griblje dd. 15. Feb 1876 + VOJAŠKA OMAMBA kandidat ("zum k.k. [vojaška_enota]"?) + Cernomełj omemba. Prepiši znak za znak. {"id":"s12-r8-befunde","befunde":"...","vojska":"...","note":"..."}`,
  's12-r9-eltern': `ULTRA-ZOOM (3×) staršev vpisa-9 na s12: starši ŽENINA (Nicolaus Mihelič[~Milek] × Barbara née Krojmič?) in starši NEVESTE (Georg Pegdire × Anna Tome?). Prepiši VSE. {"id":"s12-r9-eltern","elternZenin":{"ocee":"...","mati":"..."},"elternNevesta":{"ocee":"...","mati":"..."},"note":"..."}`,
  's12-r6-priest': `ULTRA-ZOOM (6×) podpisa duhovnika vpisa-6 na s12 — pričakovano "Georg Dovgan Pfrnar" — prepiši (garble D/B/P/G dovoljen). {"id":"s12-r6-priest","podpis":"...","note":"..."}`,
  's13-m10-date-mikro': `ULTRA-ZOOM (4×) datumske celice VPISA-10 na s13 (prvi vpis lista) — pričakovano "1876. Februar 23." — prepiši znak za znak (to je REFERENČNI vzorec meseca "Februar" od istega pisarja!). {"id":"s13-m10-date-mikro","datum":"...","mesecOblika":"opis črk F-e-b-r","note":"..."}`,
  's13-r11-date-mikro': `ULTRA-ZOOM (4×) datuma vpisa-11 na s13 — pričakovano "[Februar] 27." — ali je mesec prisoten? Prepiši. {"id":"s13-r11-date-mikro","datum":"...","mesec":"...","dan":"...","note":"..."}`,
  's13-r12-date-mikro': `ULTRA-ZOOM (4×) datuma vpisa-12 na s13 — pričakovano "September 14" ali "Sept 17" — prepiši. {"id":"s13-r12-date-mikro","datum":"...","mesec":"...","dan":"...","note":"..."}`,
  's13-r13-date-mikro': `ULTRA-ZOOM (4×) datuma vpisa-13 na s13 — pričakovano "October 22" ali "Sept 22" — prepiši. {"id":"s13-r13-date-mikro","datum":"...","mesec":"...","dan":"...","note":"..."}`,
  's13-r13-wohnort': `ULTRA-ZOOM (4×) Wohnortov vpisa-13 na s13: ženin "Wsch 22" + PREČRTANA številka/kraj + popravka "z Griblje" spodaj?; nevesta "Gri. šte. 41" + "Maria Pegdire Leinmannstochter". Prepiši VSE (tudi prečrtano!). {"id":"s13-r13-wohnort","zeninWohnort":"...","precrtno":"...","popravek":"...","nevestaWohnort":"...","nevesta":"...","stan":"...","note":"..."}`,
  's13-r13-befunde': `ULTRA-ZOOM (4×) Befunde vpisa-13 na s13: pričakovano "Gemeinezettel ... Griblje dd. 16. [Okt?] 1876" + "pro die minderj. Braut" (mladoletna nevesta!) + priče Peter/Johann Mrh. Prepiši znak za znak. {"id":"s13-r13-befunde","befunde":"...","zettelDatum":"...","mladoletnost":"...","pricE":"...","note":"..."}`,
  's13-r10-priest': `ULTRA-ZOOM (6×) podpisa duhovnika vpisa-10 na s13 — pričakovano "Georg Dovgan Pfrnar" — prepiši (je morda "Franc Grgas" ali drug?). {"id":"s13-r10-priest","podpis":"...","note":"..."}`,
  's14-r14-wohnort': `ULTRA-ZOOM (4×) ženinovega Wohnorta vpisa-14 na s14 — kandidati: "Wilsput 18" / "A. Pfslph 18" / "Mali Lipoglav 18" — prepiši znak za znak. {"id":"s14-r14-wohnort","wohnort":"...","hisna":"18","odgovor":"...","note":"..."}`,
  's14-r14-hisne': `ULTRA-ZOOM (8×) nevestine hišne številke vpisa-14 na s14 za "Griblje" — pričakovano "30" — preveri 30-vs-36-vs-50! {"id":"s14-r14-hisna","stevilka":"...","zanesljivost":"...","note":"..."}`,
  's14-r14-befunde': `ULTRA-ZOOM (3×) Befunde vpisa-14 na s14: pričakovano Gemeindezettel woher Griblje dd. 11. [9br=Novembris?] 1876 + TYPHUS omemba ("da fraglich dt Typh") + zdravniško sodišče + Consens k.k. Bez.Gericht [Metlika/Milfhing] dd. 18. 9br 1876. Prepiši znak za znak. {"id":"s14-r14-befunde","befunde":"...","typhus":"...","sodisce":"...","consensDatum":"...","note":"..."}`,
  's14-r14-elternB': `ULTRA-ZOOM (4×) staršev neveste vpisa-14 na s14 — pričakovano: oče "Markus [Margon?/Morzan?]" + mati "Mathiewa née Pegdire" — prepiši znak za znak. {"id":"s14-r14-elternB","ocee":"...","mati":"...","note":"..."}`,
};

const tasks = [];
for (const [id, hint] of Object.entries(hints)) {
  tasks.push({ id: `p2-${id}`, img: `${DIR}/krops2/${id}.jpg`, prompt: rowPrompt(id, hint) });
}
for (const [id, prompt] of Object.entries(mikroPrompts)) {
  tasks.push({ id: `p3-${id}`, img: `${DIR}/krops3/${id}.jpg`, prompt });
}

const zai = await ZAI.create();

async function run(t) {
  const out = `${OUT}/${t.id}.json`;
  if (fs.existsSync(out)) { console.log(`${t.id}: že obstaja`); return; }
  const b64 = fs.readFileSync(t.img).toString('base64');
  for (let attempt = 1; attempt <= 4; attempt++) {
    try {
      console.log(`--- ${t.id} (poskus ${attempt}) ...`);
      const completion = await Promise.race([
        zai.chat.completions.createVision({
          messages: [{ role: 'user', content: [
            { type: 'text', text: t.prompt },
            { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${b64}` } }
          ]}],
          thinking: { type: 'disabled' }
        }),
        new Promise((_, rej) => setTimeout(() => rej(new Error('TIMEOUT 240s')), 240000))
      ]);
      const raw = completion.choices[0]?.message?.content ?? '';
      const s = raw.indexOf('{');
      const e = raw.lastIndexOf('}');
      if (s === -1 || e === -1) throw new Error('ni JSON v odgovoru');
      const j = JSON.parse(raw.slice(s, e + 1));
      fs.writeFileSync(out, JSON.stringify(j, null, 2));
      console.log(`${t.id}: OK`);
      return;
    } catch (err) {
      console.log(`${t.id}: poskus ${attempt} NAPAKA: ${err.message}`);
      await new Promise(r => setTimeout(r, 3000));
    }
  }
  console.log(`${t.id}: VSI POSKUSI NEUSPEŠNI`);
}

for (const t of tasks) await run(t);
console.log('pass-2+3 KONČAN');
