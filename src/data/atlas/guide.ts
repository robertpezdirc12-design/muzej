/**
 * VODNIK MUZEJA — podatkovni sloj (issue #15, točka 9).
 *
 * NI chatbot in ne bo: vodnik muzeja ostaja DETERMINISTIČEN —
 * iskanje po muzejsko preverjenem naboru vprašanj/odgovorov
 * (»zgodb«), brez AI modelov. Vsak odgovor ima vir, status,
 * lokacijo (TimeSpot) in periodo; Atlas, evidence in provenance
 * ostanejo edini vir resnice.
 *
 * Vsebina je povzeta IZKLJUČNO iz obstoječih podatkov muzeja
 * (timespots.ts, village3d.ts, atlas, exhibits MVG) — nič izmišljenega.
 *
 * Statusi so skladni z muzejsko lestvico zanesljivosti:
 *   VERIFIED      — uradni vir (EŠD, kataster, arhiv)
 *   DOCUMENTED    — zapis v zbirki s preverljivim virom
 *   RECONSTRUCTED — rekonstrukcija (izmerjeno, višine interpretacija)
 *   INTERPRETATION — poštena interpretacija (lega ni znana)
 */

export type GuideStatus =
  | "VERIFIED"
  | "DOCUMENTED"
  | "RECONSTRUCTED"
  | "INTERPRETATION";

export interface GuideQA {
  /** identifikator zapisa (stabilen za strojno uporabo) */
  id: string;
  /** TimeSpot, na katerega se zgodba veže (id iz TIME_SPOTS) */
  spotId: string;
  questionSi: string;
  questionEn: string;
  answerSi: string;
  answerEn: string;
  /** vir resnice — muzejska številka + arhiv/uradni vir */
  source: string;
  status: GuideStatus;
  /** lokacija (spot id — strojno berljivo) */
  location: string;
  /** perioda, na katero se odgovor nanaša */
  period: string;
}

/** 18 preverjenih zgodovinskih zgodb — po 2 na vsak od 9 TimeSpotov. */
export const GUIDE_QA: GuideQA[] = [
  /* ── cerkev ── */
  {
    id: "qa-cerkev-1526",
    spotId: "cerkev",
    questionSi: "Kdaj je cerkev sv. Vida prvič omenjena?",
    questionEn: "When is St. Vitus' church first mentioned?",
    answerSi:
      "Leta 1526 — letos 2026 obeležujemo 500 let od prve omembe. Cerkev stoji na pokopališkem gričku južno od vaškega jedra.",
    answerEn:
      "In 1526 — this year, 2026, marks 500 years since the first mention. The church stands on its cemetery hill south of the village core.",
    source: "EŠD 2122 · MVG-002 · MVG-003",
    status: "VERIFIED",
    location: "cerkev",
    period: "1526–2026",
  },
  {
    id: "qa-cerkev-lega",
    spotId: "cerkev",
    questionSi: "Kje stoji cerkev v AR rekonstrukciji?",
    questionEn: "Where does the church stand in the AR reconstruction?",
    answerSi:
      "Na uradni lokaciji registra EŠD 2122. Sprva je bila 595 m napake; razrešili smo jo z dokazno potjo (GeoTruth, issue #14) — model stoji na uradni lokaciji.",
    answerEn:
      "At the official location from the EŠD 2122 register. An initial 595 m error was resolved with an evidence chain (GeoTruth, issue #14) — the model stands on the official location.",
    source: "EŠD 2122 · kataster list A02 (SI AS 176) · GeoTruth",
    status: "VERIFIED",
    location: "cerkev",
    period: "1825",
  },
  /* ── jedro ── */
  {
    id: "qa-jedro-156",
    spotId: "jedro",
    questionSi: "Koliko stavb je imela vas leta 1825?",
    questionEn: "How many buildings did the village have in 1825?",
    answerSi:
      "156 katastrskih stavb — vse vektorizirane z georeferenciranega lista A02 franciscejskega katastra. V AR lahko tapnete vsako in poglejte, kdo je v njej živel.",
    answerEn:
      "156 cadastre buildings — all vectorised from the georeferenced sheet A02 of the Franciscan cadastre. In AR you can tap each one and see who lived in it.",
    source: "kataster list A02 (SI AS 176) · MVG-001",
    status: "RECONSTRUCTED",
    location: "jedro",
    period: "1825",
  },
  {
    id: "qa-jedro-lastniki",
    spotId: "jedro",
    questionSi: "Kdo je živel v hišah Gribelj?",
    questionEn: "Who lived in the houses of Griblje?",
    answerSi:
      "Register hiš 1825 ima 80 lastniških zapisov; matične knjige župnije Podzemelj pokrivajo leta 1669–1947 — rojstva, poroke in smrti vaščanov.",
    answerEn:
      "The 1825 house register holds 80 owner entries; the parish books of Podzemelj cover 1669–1947 — births, marriages and deaths of the villagers.",
    source: "Register hiš 1825 · matrike Podzemelj · MVG (hišne zgodbe)",
    status: "DOCUMENTED",
    location: "jedro",
    period: "1669–1947",
  },
  /* ── kolpa ── */
  {
    id: "qa-kolpa-carina",
    spotId: "kolpa",
    questionSi: "Kaj je delovalo ob Kolpi leta 1809–1813?",
    questionEn: "What operated on the Kolpa in 1809–1813?",
    answerSi:
      "Napoleonova carinarnica — v času Ilirskih provinc je bila Kolpa meja Francoskega cesarstva.",
    answerEn:
      "Napoleon's customs post — during the Illyrian Provinces the Kolpa was the border of the French Empire.",
    source: "MVG-092 · MVG-006",
    status: "DOCUMENTED",
    location: "kolpa",
    period: "1809–1813",
  },
  {
    id: "qa-kolpa-reka",
    spotId: "kolpa",
    questionSi: "Kakšna reka je Kolpa?",
    questionEn: "What kind of river is the Kolpa?",
    answerSi:
      "Mejna reka s Hrvaško in ena najtoplejših slovenskih rek — vasi ob njej je dala življenje: vodo, ribe, mlinske gondole in kopanje.",
    answerEn:
      "A border river with Croatia and one of Slovenia's warmest rivers — it gave the village its life: water, fish, millstreams and swimming.",
    source: "MVG-006 · georeferencirana struga (sidro 15,2994 E)",
    status: "DOCUMENTED",
    location: "kolpa",
    period: "do danes",
  },
  /* ── ribnik ── */
  {
    id: "qa-ribnik-voda",
    spotId: "ribnik",
    questionSi: "Čemu je služil vaški ribnik?",
    questionEn: "What was the village pond for?",
    answerSi:
      "Vas je ob njem hranila vodo za živino — pred vodovodi je bil ribnik del vsakodnevnega vaškega ritma.",
    answerEn:
      "The village kept water for livestock by it — before water mains, the pond was part of the daily village rhythm.",
    source: "MVG-016",
    status: "DOCUMENTED",
    location: "ribnik",
    period: "~1900",
  },
  {
    id: "qa-ribnik-1900",
    spotId: "ribnik",
    questionSi: "Koliko stavb je priraslo do leta ~1900?",
    questionEn: "How many buildings grew by ~1900?",
    answerSi:
      "Ocena: 35 novih stavb — zgoščevanje po delitvi domačij. Prijesor ~1900 je OCENA metodologije periode, ne izmera.",
    answerEn:
      "An estimate: 35 new buildings — densification after farm divisions. The ~1900 scene is an ESTIMATE of the period methodology, not a survey.",
    source: "MVG-016 · ~1900 = OCENA (metodologija periode)",
    status: "INTERPRETATION",
    location: "ribnik",
    period: "~1900",
  },
  /* ── gornje ── */
  {
    id: "qa-gornje-spomenik",
    spotId: "gornje",
    questionSi: "Kaj stoji pred osnovno šolo?",
    questionEn: "What stands in front of the primary school?",
    answerSi:
      "Spomenik padlim vaščanom iz leta 1961 — uradna lokacija EŠD 19326.",
    answerEn:
      "The memorial to the fallen villagers from 1961 — the official EŠD 19326 location.",
    source: "EŠD 19326 · MVG-029",
    status: "VERIFIED",
    location: "gornje",
    period: "1961",
  },
  {
    id: "qa-gornje-zaselki",
    spotId: "gornje",
    questionSi: "Kdaj so zaselki Gribelj prvič zapisani?",
    questionEn: "When were the Griblje hamlets first recorded?",
    answerSi:
      "Dolnje, Srednje in Gornje Griblje so zapisani že leta 1526 — skupaj s prvo omembo cerkve sv. Vida.",
    answerEn:
      "Dolnje, Srednje and Gornje Griblje are recorded as early as 1526 — together with the first mention of St. Vitus' church.",
    source: "MVG-049",
    status: "DOCUMENTED",
    location: "gornje",
    period: "1526",
  },
  /* ── meja ── */
  {
    id: "qa-meja-1991",
    spotId: "meja",
    questionSi: "Od kdaj je tu državna meja?",
    questionEn: "Since when is there a state border here?",
    answerSi:
      "Od leta 1991 — ob samostojnosti Slovenije je Kolpa postala mejna reka. Prej je bila notranja meja republik.",
    answerEn:
      "Since 1991 — with Slovenia's independence the Kolpa became a border river. Before, it was an internal republic boundary.",
    source: "MVG-015",
    status: "DOCUMENTED",
    location: "meja",
    period: "1991–danes",
  },
  {
    id: "qa-meja-duhovi",
    spotId: "meja",
    questionSi: "Kaj kažejo žični duhovi hiš?",
    questionEn: "What do the wireframe house-ghosts show?",
    answerSi:
      "Obris, kje je stala vas 1825 — pogovor med preteklostjo in sedanjostjo. Žični obris je INTERPRETACIJA rekonstrukcije, ne ostanek.",
    answerEn:
      "The outline of where the village stood in 1825 — a dialogue between past and present. The wireframe is an INTERPRETATION of the reconstruction, not a ruin.",
    source: "MVG-015 · »danes« = interpretacija (žični obris 1825)",
    status: "INTERPRETATION",
    location: "meja",
    period: "1825 ⇄ danes",
  },
  /* ── mlini ── */
  {
    id: "qa-mlini-zimaln",
    spotId: "mlini",
    questionSi: "Kaj je žimaln?",
    questionEn: "What is a žimaln?",
    answerSi:
      "Mlin z vodoravnim kolesom ZNOTRAJ hiše — takšni so stali ob Kolpi. Pred vami je proceduralna scena VRSTE mlina, ne konkretnega.",
    answerEn:
      "A mill with a horizontal wheel INSIDE the house — such stood on the Kolpa. Before you is a procedural scene of the mill TYPE, not a particular mill.",
    source: "MVG-009 · Radio Odeon (urbarji) · Krajinski park Kolpa",
    status: "RECONSTRUCTED",
    location: "mlini",
    period: "srednji vek–19. stol.",
  },
  {
    id: "qa-mlini-ohranjeni",
    spotId: "mlini",
    questionSi: "Je kateri mlin ostal?",
    questionEn: "Has any mill survived?",
    answerSi:
      "Večina jih je propadla. Med ohranjenimi je mlin v Pobrežju — urbarji navajajo mline v Dolu, Radencih, Pobrežju in Krasincu.",
    answerEn:
      "Most have decayed. Among the preserved is the mill at Pobrežje — the urbars list mills at Dol, Radenci, Pobrežje and Krasinec.",
    source: "MVG-009 · urbarji (Dol, Radenci, Pobrežje, Krasinec)",
    status: "DOCUMENTED",
    location: "mlini",
    period: "do danes",
  },
  /* ── otok ── */
  {
    id: "qa-otok-1473",
    spotId: "otok",
    questionSi: "Koliko ranjencev je odletelo z Otoka?",
    questionEn: "How many wounded flew out from Otok?",
    answerSi:
      "1473 ranjencev — do konca vojne so jih prepeljali v zavezniške bolnišnice v južni Italiji. Rešili so tudi 87 britanskih letalcev.",
    answerEn:
      "1,473 wounded — by the end of the war they were carried to Allied hospitals in southern Italy. 87 British airmen were rescued too.",
    source: "MVG-013 · RTV Slovenija",
    status: "DOCUMENTED",
    location: "otok",
    period: "1944–1945",
  },
  {
    id: "qa-otok-pristanek",
    spotId: "otok",
    questionSi: "Kdaj je pristalo prvo zavezniško letalo?",
    questionEn: "When did the first Allied plane land?",
    answerSi:
      "17. septembra 1944 — pet letali ob zatemnitvi. Travnik so označili z lučmi, letališče pa so partizani uredili spomladi 1944.",
    answerEn:
      "On 17 September 1944 — five aircraft at blackout. The meadow was marked with lanterns; the Partisans had laid out the airfield in spring 1944.",
    source: "MVG-013 · RTV Slovenija · Wikipedija (Otok, Metlika)",
    status: "DOCUMENTED",
    location: "otok",
    period: "17. 9. 1944",
  },
  /* ── cerkvišče ── */
  {
    id: "qa-cerkvisce-ime",
    spotId: "cerkvisce",
    questionSi: "Zakaj se kraj imenuje Cerkvišče?",
    questionEn: "Why is the place called Cerkvišče?",
    answerSi:
      "Tu so stale tri cerkvice — Turki so jih ob vpadih (od ~1408) porušili in zažgali. Za dve domnevno vaščani še vedno vedo, kje sta stali; tretje ni nihče.",
    answerEn:
      "Three churches stood here — the Turks pulled them down and burned them during the incursions (from ~1408). For two the villagers still believe they know where they stood; of the third, no one does.",
    source: "MVG-040 · Wikipedija (Cerkvišče)",
    status: "INTERPRETATION",
    location: "cerkvisce",
    period: "~1408",
  },
  {
    id: "qa-cerkvisce-kapelica",
    spotId: "cerkvisce",
    questionSi: "Kaj stoji na Cerkvišču danes?",
    questionEn: "What stands at Cerkvišče today?",
    answerSi:
      "Bela kapelica iz leta 1994 — edini kamen, ki danes nosi spomin treh cerkvic.",
    answerEn:
      "The white chapel of 1994 — the only stone that today carries the memory of the three churches.",
    source: "MVG-040 · kapelica 1994 (fizični spomenik)",
    status: "VERIFIED",
    location: "cerkvisce",
    period: "1994–danes",
  },
];

/** Zgodbе za posamezno točko (vrstni red po GUIDE_QA). */
export function getGuideForSpot(spotId: string): GuideQA[] {
  return GUIDE_QA.filter((g) => g.spotId === spotId);
}

/** Skupno število preverjenih zgodb (za zaključno statistiko obiska). */
export const GUIDE_TOTAL = GUIDE_QA.length; // 18
