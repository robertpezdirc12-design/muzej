import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';
const DIR = '/tmp/p258/full';
const zai = await ZAI.create();

const HINTS = {
  s8_r1: "1831-konec (Pag. 13, nadaljevanje iz Pag. 11 kjer je bilo 9. Febr + d°×10): ta vrstica = 9. Febr d° (12. poroka tega dne!) — ženin [Andreas Mercina?|Matija Hribar?] (vas [Škil?|Gribel?], hiša 1) × nevesta Marija Klobučar (vas [Griblje?|Grilic?], hiša [47?|17?-DUEL!]). PREVIDNO: priimek ženina in hiša/vas neveste!",
  s8_r2: "1831: 14. Febr — ženin [Georg Staroling?|Franz Krasting?] (vas [Krasinec?|Krasting?], hiša 17) × nevesta Barbara [Kostjan?|Hribernik?] (vas [Osilnica?|Grabel?=Griblje?], hiša 16). PREVIDNO: priimka + vasi!",
  s8_r3: "1831: 14. Febr d° — ženin [Jožef Kerm?|Peter Joseph Pavšelč?] (vas [Grič?|Gradače?], hiša [35?|38?], vdovec?) × nevesta [Johanna Jakl?|(vdova) Graboner?] (hiša [38?|3?]). PREVIDNO: vse!",
  s8_r4: "1831: 6. Juni — ženin [Michel Butala!|Nikolaj Bubilec/Batale? — BUTALA-kand. (mati/oče Butala na desni strani!)] (vas [Sodevci?|Ložane?], hiša 26) × nevesta Maria [Krischan?=Križan?|Krizman?] (vas [Osilnica?|Grabel?=Griblje?], hiša 16). PREVIDNO: priimek ženina (Butala?) + priimek/vas neveste!",
  s8_r5: "1831: [2. Juni?|2. April?|24. Septembra?-DUEL-datuma!] — ženin [Jožef Perman?|Ignacij Ferjančec?] (vas [Prelo?|Mödling?=Metlika?], hiša 9) × nevesta Magdalena [Gstroliž?|Schatzberg?] (vas [Gradišče?], hiša [7?]). PREVIDNO: datum + priimka!",
  s8_r6: "1831: 24. Aug — ženin Matthias Klobučar (Griblje, hiša 46) × nevesta Catharina [Kolarič?|Klofčič?] (Griblje, hiša 8). PREVIDNO: priimek neveste!",
  s8_r7: "1831: 24. Aug d° — ženin Johann Klobučar (Griblje, hiša 48) × nevesta Anna [Krebelz?|Scalec?] (Griblje, hiša 2). PREVIDNO: priimek neveste!",
  s8_r8: "1831: [13. Nov?|1. Nov?-DUEL!] — ženin Aloys [Paron — BARON?! 'unierter Priester' (grško-uniatni duhovnik?) / Krajnski plemič?] (vas [Gradič?|Kostanjevica?], hiša 1) × nevesta Helena [Rubi?|Dubil?] (hiša 1). POSEBNA VRSTICA — plemiška poroka! PREVIDNO: datum + status + priimka!",
  s8_r9: "1831: 6. Nov — ženin Nicolaus Muz (Semelj=Podzemelj, hiša 24) × nevesta Anna [Tomažič? Kovačič?|Novošec?|Dovžec?] (Semelj, hiša 15). MUZ-družina (continuum 1828!). PREVIDNO: priimek neveste!",
  s8_r10: "1831: 20. Nov — ženin Martin [Stephan?|Stržinar?] (vas [Vejrij?/Wörth?|Vrhovlje?], hiša 9) × nevesta Maria [Josefa Dolenc?|Stržinar?] (vas [Dobrava?], hiša 8). PREVIDNO: priimka!",
  s8_r11: "1831: [23. Nov d°?|20. Dec?-DUEL!] — ženin Matthias [Hočevar?|Antonijevič?] (vas [Prest? pri Mokronogu?|Vrhovlje?], hiša 108) × nevesta Maria [Höffner?|Hribar?] (vas [Dobrovnik?|Dobrava?], hiša 36). PREVIDNO: datum + priimka!",
  s9_r1: "1832 (Pag. 15, RESTART letnice!): 18. Jänner 1832 — ženin Georg [Harejž?|Surajofs?] (vas [Gradetz?|Prädaz?], hiša 49) × nevesta Catharina [Bergant?|Petersch?] (vas [Podberg?/Kerslovy?|Dorfpt?], hiša 1). PREVIDNO: priimka + vasi!",
  s9_r2: "1832: 18. Jän d° — ★ ANOMALIJA: v stolpcu ženina ŽENSKO IME [Maria Vipavz!|Matija Vipavc?] (vdova? glej status!) (vas [Krajnç?|Krafing?], hiša [24?|34?-DUEL!]) × nevesta Anna [Klopčez?|Klepez?] (vas [Brvšt?=Boršt?|Dorfpt?], hiša 21). PREVIDNO: spol/status ženina + hiša!",
  s9_r3: "1832: 18. Jän d° — ★ ANOMALIJA: [Maria Tolkarigh?|Mario/Marijo Johannig?] (vdova?) (vas [Partož?|Prilogje?], hiša 30) × nevesta Anna [Tsaltrigh?|Taschig?] (vas [Božina vas?|Regina vas?], hiša 13). PREVIDNO: spol/status + priimka!",
  s9_r4: "1832: 25. Jän d° — ženin Johann [Morauz?|Moravc?] (vas [Krajnç?|Krafing?], hiša 22) × nevesta Cath. [Petriž?|Petriz?] (vas [Krajnç?|Krafing?], hiša [5?|3?-DUEL!]). PREVIDNO: hiša neveste!",
  s9_r5: "1832: 29. Jän d° — ženin Martin [Krefts?|Kropa?] (status vid.=vdovec?) (vas [Gradetz?|Prädaz?], hiša [18?|48?-DUEL!]) × nevesta Gertrud [Pevac?|Peter?] (vas [Gumnišče?|Podboršt?], hiša [16?|46?-DUEL!]). PREVIDNO: hiši!",
  s9_r6: "1832: 15. Febr — ženin Matthias [Noval=Novak?] (vas [Vranoviž?|Vranoviče?], hiša 11) × nevesta Maria [Sipuš?|Hrija?] (vas [Gradetz?|Prädaz?], hiša 6). PREVIDNO: priimek neveste!",
  s9_r7: "1832: 15. Febr d° — ženin Georg [Muz=Muc?!|Matz?] (vas [Gorn?|Görn?], hiša [24?|27?]) × nevesta Maria [Popiž?|Fenigl?] (vas [Gepršağ?|Görprihl?], hiša 35). PREVIDNO: priimek ženina (Muc? — znana družina Griblje-h10!)!",
  s9_r8: "1832: 15. Febr d° — ★★ ženin Johann [Milch?|Miklau?|Milek?!] (GRIBLJE/Grüble, hiša 22 — četrto leto zapored: 1828 Catra [Miller], 1829 Maria [Miller], 1830 Anna MILEK, zdaj 1832!) (oče na desni: Johann Mihl/Milek?!) × nevesta Anna [Štremiz?|Fessig?] (GRIBLJE/Grüble, hiša 35). PREVIDNO: priimek ženina (Milek?!) + priimek neveste!",
  s9_r9: "1832: 15. Febr d° — ženin Martin [Potha?|Pejka?] (vas [Višnja?|Podboršt?], hiša 5) × nevesta Margaretha [Goedpriž?|Sodržig?] (vas [Dolenja vas?|Dobravc?], hiša 19). PREVIDNO: priimka!",
  s9_r10: "1832: 22. Febr d° — ženin Georg [Muz?|Matz?] (vas [Pomre?|Primostek?], hiša 7) × nevesta Barbara [Marertlih?|Marentig?] (Otok, hiša 18). PREVIDNO: priimka ženina!",
  s9_r11: "1832: 29. Febr d° — ženin Georg [German?|Jurman?] (vas [Doiprt?|Dorfpt?], hiša 19) × nevesta Catharina [Tonž?|Tomž?] (vas [Kraplje?|Kapišce?], hiša [5?|9?]). PREVIDNO: priimka + vasi!",
  s9_r12: "1832: 29. Febr d° — ženin Nicul [Tskeliž?|Tehlig?] (vas [Smel?|Somel?=Semelj?], hiša [15?|13?]) × nevesta Anna [Tonž?|Tomž?] (vas [Kraplje?|Kapišce?], hiša 9). PREVIDNO: priimek ženina + vasi!",
  s9_r13: "1832: 29. Febr d° — ženin Peter [Kambriž?|Kambig?=KAMBIČ?!] (vas [Krajnç?|Krafing?], hiša 19) × nevesta Maria [Toleh?|Kulah?] (vas [Gern?|Görn?], hiša 25). PREVIDNO: priimek ženina (Kambič — znana 1831-družina!) + priimek neveste!",
  s9_r14: "1832: 29. Febr d° — ženin Mathias [Toleh?|Felah?] (vas [Gern?|Görn?], hiša [25?|26?]) × nevesta Catharina [Jurijefpriž?|Jurojfižig?=Jurjevič?!] (vas [Primožtol?|Primoštens?], hiša [11?|41?]). PREVIDNO: priimka + hiši!",
  s9_r15: "1832: 29. Febr d° — ženin Michael [Grichaž?|Fricah?] (vas [Očosl?|Ochlau?], hiša [16?|10?]) × nevesta Anna [ToHe?|Salher?] (vas [Petolge?|Prilozje?], hiša 29). PREVIDNO: priimka + hiša ženina!",
  s10_r1: "1832-konec (Pag. 17): 29. Febr 1832 — ženin Johann [Klebez=KLEPEC?!|Hlebez=HLEBEC?!] (GRIBLJE/Gruble, hiša 2) × nevesta Anna [Petiz?|Petriz?] (vas [GRIBLJE?|Smrečje?-DUEL!], hiša [32?|42?-DUEL!]). PREVIDNO: priimek ženina + vas/hiša neveste!",
  s10_r2: "1832: 29. Febr d° — ★ ženin Nicol [Kirishan=KRIŽAN!] (GRIBLJE/Gruble, hiša 36!) × nevesta Catharina [Flach?|Tienk?] (GRIBLJE/Gruble, hiša 35). PREVIDNO: priimek neveste + hiši (36/35)!",
  s10_r3: "1832: 29. Febr d° — ženin [Mario?|Matias?] [Gorshig?|Gerspich?] (vas [Stamma?|Laune?], hiša 23) × nevesta Margareth Angel (vas [Salova?|Dobravlje?], hiša 11). PREVIDNO: ime+priimek ženina!",
  s10_r4: "1832: 29. Febr d° — ženin Joh. [Heroman?|Kernza?] (vas [Saloha in Croatia?|Laune?], hiša [27?|7?]) × nevesta Maria [Horel?|Novak?] (vas [Ortach?|Otok?], hiša 15). PREVIDNO: priimek ženina + vasi!",
  s10_r5: "1832: 5. März — ženin Georg Vipavz/Vipavc (vas [Kreuz?|Kraplje?], hiša [31?|21?]) × nevesta Catharina [Harizojfzhig?|Jurjevčič?] (vas [Kreuz?|Kraplje?], hiša [21?]). PREVIDNO: vasi + hiši + priimek neveste!",
  s10_r6: "1832: 28. Mai — ženin [Mich.?|Nicol?] [Petrin?] (vas [Saloha in Krainz?|Nova vas?], hiša [0?|10?]) × nevesta Anna [Hafllig?|Volkich?] (vas [Samei?|Smrečje?], hiša 21). PREVIDNO: ime ženina + hiša!",
  s10_r7: "1832: 20. Juni — ★★ ženin Johann [Kirishan=KRIŽAN!] (GRIBLJE/Gruble, hiša [66?|6?-DUEL-KLJUČNI!] — prejšnja vrstica je bila 36!) × nevesta Anna [Kirishan=KRIŽAN?] (vas [Kreuz?|Krapping?=Kraplje?], hiša 35). PREVIDNO: hiša ženina (66 ali 6?!) + vas neveste!",
  s10_r8: "1832: 28. Nov — ženin Peter [Himiz?|Amiz?|ŠIMIČ?!] (GRIBLJE/Gruble, hiša 56; oče na desni: Nicol Šimic?!) × nevesta Anna [Flach?|Tielak?] (vas [GRIBLJE?|Smrečje?-DUEL!], hiša 61). PREVIDNO: priimek ženina (Himič ali Šimič?) + vas/hiša neveste!",
  s10_r9: "★★ RESTART-1833! (Pag. 17 spodaj): [3.?|5.?-DUEL-datuma!] Febr 1833 — ženin Anton [Sipaz?|Seipa?] (vas [Krainz?|Grilaz?], hiša 6, iz [Tihove?/Thieffen?]) × nevesta [Burgstainer?|Auffschein?] (vas [Kloster?|Klofter?], hiša 43, status [Büük-Kind?]). PREVIDNO: datum + priimka!",
  s10_r10: "1833: [5.?|6.?] Febr d° — ženin Nicol [Tonz?] (vas [Kaplice?|Laune?], hiša [5?|3?]) × nevesta Barbara [Fritzhofzhig?|Krithovigh?] (vas [Mühle?=Mlin?|Mile?], hiša 2). PREVIDNO: vas ženina + priimek neveste!",
  s10_r11: "1833: 6. Febr d° — ženin Mathias [Jurizojfzhig?|Jurjepsich?=Jurjevič?] (vas [Mühle?=Mlin?|Mlake?], hiša 11) × nevesta Catharina [Jofllig?|Jalling?] (vas [Podsmel?=Podzemelj?|Podgrad?], hiša 12). PREVIDNO: priimka + vasi!",
  s10_r12: "1833: 6. Febr d° — ženin [Marcus?|Martin?] [Papizh?|Parpich?] (vas [Gorschiz?|Gerspich?], hiša 6) × nevesta Catharina Angel (Dobravlje, hiša 22). PREVIDNO: ime + priimek ženina!",
  s10_r13: "1833: 6. Febr d° — ženin Nicol [Petraz?|Petrin?] (vas [Tratzhig?|Draphigh?], hiša [36?|25?]) × nevesta Catharina [Muz=MUZ?!|Pino?-DUEL!] (vas [Grintez?|Pino?], hiša 4). PREVIDNO: priimek neveste (Muz — družina 1828/1831!)!",
  s10_r14: "1833: 6. Febr d° — ★★★ ženin Johann [Petroviz?|Petrič?|PEZDIRZ?!!] (GRIBLJE/Gruble, hiša 50!! — PEZDIRC-hiša: 1831 Georg Pesdirz h50 oče Marco Pesdirz ↔ 1873 Marcus Pegdire h50!) (oče na desni: [Marco Petrič?!|MARCO PESDIRZ?!!]) × nevesta Maria [Himiz?|?] (GRIBLJE/Gruble, hiša 49). NAJVEČJA-PREDNOSTNA-VRSTICA: preberi priimek ženina ČRKO ZA ČRKO (Petr… ali Pesd…?) + ime očeta (Marco?) + priimek neveste!",
};

const PROMPT = (id) => `Slika je POVEČAN IZREZ (vodoravni trak, širina celega razprtega lista) poročne knjige Trauungs-Buch 01738 (Podzemelj, Kurrent-pisava, nemško). Trak obsega ENO vrstico vpisa (lahko tudi del sosednje — loči po vsebinski celovitosti!).
KONTEKST: ${HINTS[id]}
Stolpci LEVE strani razprtega lista: [Jahr/Monat/Tag der Trauung] [Wohnort ŽENINA] [Haus-Nr] [Taufname+Familien-Name+Stand ŽENINA] [Alter] | [Wohnort NEVESTE] [Haus-Nr] [Taufname+Familien-Name+Stand NEVESTE] [Alter]
Stolpci DESNE strani razprtega lista: [Eltern des Bräutigams] [Eltern der Braut] [Zeugen] [Urkunden] [Unterschrift des trauenden Priesters]
Naloga: prepiši DOBESEDNO po stolpcih. Hišne številke so MAJHNE — previdno! Nejasna mesta označi z [~]. Če je trak prazen ali vsebuje dve vrstici, povej.
Izhod SAMO JSON: {"id":"${id}","vrstica":"polna/opis","datum":"","leto":0,"vasZenin":"","hisZenin":0,"zenin":"","standZenin":"","starZenin":0,"letoZenin":0,"vasNevesta":"","hisNevesta":0,"nevesta":"","standNevesta":"","starNevesta":0,"letoNevesta":0,"oceZenin":"","mataZenin":"","oceNevesta":"","mataNevesta":"","price":"","urkunde":"","duhovnik":"","xOpen":[],"razlaga":""}`;

const ROWS = [];
for (let i = 1; i <= 11; i++) ROWS.push(`s8_r${i}`);
for (let i = 1; i <= 15; i++) ROWS.push(`s9_r${i}`);
for (let i = 1; i <= 14; i++) ROWS.push(`s10_r${i}`);

async function run(id) {
  const out = `${DIR}/${id}.json`;
  if (fs.existsSync(out) && fs.statSync(out).size > 40) { console.log(`${id}: skip`); return; }
  const content = [{ type: 'text', text: PROMPT(id) }];
  content.push({ type: 'image_url', image_url: { url: `data:image/jpeg;base64,${fs.readFileSync(`${DIR}/${id}.jpg`).toString('base64')}` } });
  for (let a = 1; a <= 4; a++) {
    try {
      const r = await zai.chat.completions.createVision({
        messages: [{ role: 'user', content }],
        temperature: 0.1, max_tokens: 1500, thinking: { type: 'disabled' },
      });
      fs.writeFileSync(out, r.choices[0].message.content || '');
      console.log(`${id}: OK`);
      return;
    } catch (e) { console.log(`${id}: a${a} ${String(e).slice(0,70)}`); await new Promise(r2=>setTimeout(r2,2500)); }
  }
  console.log(`${id}: FAIL`);
}
// zaporedno s premorom (429-omejitev!)
for (const id of ROWS) {
  await run(id);
  await new Promise(r => setTimeout(r, 1500));
}
