// P247 pass-3: VLM na celičnih kropih 6× (Griblje-kandidati + dueli)
import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';

const DIR = '/home/z/p247tmp';
const OUT = `${DIR}/pass247`;

const tasks = [
  { id: 's15-m1-zenin', hint: 'ženin 1. vpisa 1877: kraj ("Aranu.vice"/"Kranu.nec"?), hišna št. (20 ali 21?), ime (Georg Lovišič/Levstik?), stan, starost (24 ali 29?)' },
  { id: 's15-m1-nevesta', hint: 'nevesta 1. vpisa: kraj ("Gri. belj. vac."?=Griblje?), hišna št. (10 ali 16?), ime (Gertrude/Cäcilie Grubanič/Kukamič?), starost (16 ALI 40? KULTEN DUEL!)' },
  { id: 's15-m1-befunde', hint: 'Befunde 1. vpisa: unanimous-datum (13. Jänner 1877?), podpis duhovnika (Franz Dovgan?)' },
  { id: 's15-m4-zenin', hint: 'ženin 4. vpisa: Wohnort "Gri. belj. č. 8"=Griblje 8?, ime Johann (Juhofčič/Jathovič/Kathunik?), stan (½ Gübl.), starost 34' },
  { id: 's15-m4-nevesta', hint: 'nevesta 4. vpisa: Wohnort Griblje (č. 31? ali 8?), ime Maria (Moh/Merk/Arik?), starost 26' },
  { id: 's15-m4-eltern', hint: 'starši 4. vpisa: oče ženina (Michael Darbar?), mati ženina, oče neveste (Mathias Lingen?), mati neveste' },
  { id: 's15-m4-befunde', hint: 'Befunde 4. vpisa: unanimous-datum (6. Februar 1877?), podpis (Franz Dovgan?)' },
  { id: 's15-m5-zenin', hint: 'ženin 5. vpisa: Wohnort "Gri. belj. č. 51" ALI "č. 31" (DUEL!), ime Mathias (Moh/Mohr/Lumin?), stan, starost (24 ali 29?)' },
  { id: 's15-m5-nevesta', hint: 'nevesta 5. vpisa: kraj ("Arau. sine"/"Kra. sine"=Krasinec?), hišna št. (7? 1?), ime Maria Prodaric (PEZDIRC-garble?), starost 16 (mladoletnica!)' },
  { id: 's15-m5-befunde', hint: 'Befunde 5. vpisa: Consens za mladoletnico (pripis!), unanimous-datum (4. Februar 1877?), podpis (Franz Dovgan?)' },
  { id: 's16-m6-par', hint: '6. vpisa: ženin "Krasi(nec) 16" Johann Čupanič/Trupanič 38 × nevesta "Krasi(nec) 14/24" Margaretha Harasinič 22; starši' },
  { id: 's16-m7-zenin', hint: 'ženin 7. vpisa: Wohnort "Gri. belj. č. 31"=GRIBLJE 31?, ime Johann (Prodavić/Prodančič/Brozdovič?), starost 23' },
  { id: 's16-m7-nevesta', hint: 'nevesta 7. vpisa: Wohnort Griblje? č. 31?, ime Katharina (March/Ahač?), starost 16 (mladoletnica!)' },
  { id: 's16-m7-befunde', hint: 'Befunde 7. vpisa: Copulationsschein/Consens datumi (26 Jan 877? 2 Febr 877?), podpis' },
  { id: 's16-m9-zenin', hint: 'ženin 9. vpisa: kraj ("Cerkvi nec."/"Griblje"?), hišna št. (2?), ime Peter (Jakofčič/Jagerfeir?), starost 23' },
  { id: 's16-m9-nevesta', hint: 'nevesta 9. vpisa: kraj ("Gri. belj."/"Thala"?), hišna št. (9?), ime Margaretha (Jakofčič/Jagerfeir? ISTA PRIIMKA?), starost 19' },
  { id: 's17-m13-par', hint: '13. vpisa: ženin Josef (Plut/Pore) "ausser Ehe geb." s pripisom "des Pfarrers v. Črnomelj"?, kraj+št.; nevesta Agnes (Plut/Guek) "Kloster 27 ali 3"; starši' },
  { id: 's17-m13-befunde', hint: 'Befunde 13. vpisa: pripisi (Graz 1877? Leingang?), datumi' },
  { id: 's17-m14-par', hint: '14. vpisa: ženin Johann (Muec/Mic) "Primostek 7 ali 1" 29; nevesta Maria geb. KRIŽAN (HRIŽAN-kontekst!) 30; starši' },
  { id: 's17-m14-befunde', hint: 'Befunde 14. vpisa: unanimous-datum, attest-pripisi, datumi (27 Juli 1877? 3. Vogel? )' },
  { id: 's18-r2-zenin', hint: 'ženin 16. vpisa (margina popravljena 15→16): kraj ("Gri. belj. č. 51"? ali Vrhnika/Pfarrer Cernomelj?), ime Nicholaus (Terdić/Serttič?), starost (29 ali 51?)' },
  { id: 's18-r2-nevesta', hint: 'nevesta 16. vpisa: kraj "Gri(e). 69"=GRIBLJE 69?, ime Catharina/Theresia (Allešić/Ažetič?), vmožitva/verw.-opomba, starost 40' },
  { id: 's18-r2-befunde', hint: 'Befunde 16. vpisa: pripis "d. 19 Jänner 1878"?, podpis blok (Georg... Griblje?)' },
  { id: 's18-r3-zenin', hint: 'ženin 17. vpisa: Wohnort "Gri. belj. č. 36"=GRIBLJE 36!, ime Josef (Pluh/Bluh/Blat), starost (23 ali 25?)' },
  { id: 's18-r3-nevesta', hint: 'nevesta 17. vpisa: kraj "Dobrava č. 11"?, ime Katharina (Hugel/Kugelj), starost 19' },
  { id: 's18-r3-befunde', hint: 'Befunde 17. vpisa: unanimous-datum (27 Oktober 1877?), pripisi, podpis (Franz Dovgan?)' },
  { id: 's18-r4-zenin', hint: 'ženin 18. vpisa: kraj "Cerki (31?)", ime Josef Stubler, stan (gärtner/Windler?), starost 24' },
  { id: 's18-r4-nevesta', hint: 'nevesta 18. vpisa: kraj "Primostek 2"? "Stubler 1"?, ime Barbara Stubler, gospodarica, starost 35, pripis' },
  { id: 's18-r4-befunde', hint: 'Befunde 18. vpisa: unanimous-datum (22. Nov 1877?), podpis (Franz Dovgan?)' },
];

const zai = await ZAI.create();

async function run(t) {
  const out = `${OUT}/p3-${t.id}.json`;
  if (fs.existsSync(out)) { console.log(`${t.id}: že obstaja`); return; }
  const b64 = fs.readFileSync(`${DIR}/krops3/${t.id}.jpg`).toString('base64');
  const prompt = `To je ULTRA-ZOOM (6×) krop ENEGA ali DVEH polj poročne knjige Podzemelj, leto 1877. Kontekst: ${t.hint}. Prepiši TOČNO tisto, kar vidiš, znak za znak (Kurrent). Če v kropu je več polj (wohnort, hišna št., ime, starost), jih loči z "|". Negotovo=[~], neberljivo=[?]. Izhod: SAMO veljaven JSON: {"id": "${t.id}", "prepis": "...", "note": "..."}`;
  for (let attempt = 1; attempt <= 5; attempt++) {
    try {
      console.log(`--- ${t.id} (poskus ${attempt}) ...`);
      const completion = await Promise.race([
        zai.chat.completions.createVision({
          messages: [{ role: 'user', content: [
            { type: 'text', text: prompt },
            { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${b64}` } }
          ]}],
          thinking: { type: 'disabled' }
        }),
        new Promise((_, rej) => setTimeout(() => rej(new Error('TIMEOUT 200s')), 200000))
      ]);
      const raw = completion.choices[0]?.message?.content ?? '';
      fs.writeFileSync(out, raw);
      console.log(`${t.id}: OK (${raw.length})`);
      return;
    } catch (e) {
      const is429 = e.message.includes('429') || e.message.toLowerCase().includes('too many');
      console.error(`${t.id}: napaka: ${e.message.slice(0, 100)}`);
      if (!is429 && attempt >= 4) { fs.writeFileSync(out, `{"ERROR": "${e.message.slice(0,200)}"}`); return; }
      await new Promise(r => setTimeout(r, is429 ? 25000 : 8000));
    }
  }
}

for (const t of tasks) { await run(t); }
console.log('PASS-3 KONČAN');
