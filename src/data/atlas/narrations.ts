/**
 * GOVORNE SKRIPTE časovnih točk (P15) — glas muzeja so skripte.
 *
 * Vsaka časovna točka ima skripto v slovenčini in angleščini, napisano
 * ZA GLAS (branje na glas). Vsebina je izpeljana IZKLJUČNO iz obstoječih
 * muzejskih podatkov (src/data/atlas/timespots.ts: naslov, opis, dokaz)
 * — nobeno zgodovinsko dejstvo ni dodano, spremenjeno ali izmišljeno;
 * spremenjena je le oblika: pisni citat »EŠD 2122 · MVG-002« postane
 * govorna oblika »register nepremične kulturne dediščine …«.
 *
 * Skripte predvaja DETERMINISTIČNI narrator (src/lib/narrator.ts) prek
 * brskalnikove vgrajene speechSynthesis: zastonj, lokalno, BREZ AI
 * modelov, brez omrežnih klicev in brez plačljivih storitev. Skripta je
 * hkrati transkript — enako besedilo se ob predvajanju pokaže na zaslonu.
 */

import type { TimeSpot } from "./timespots";

export interface SpotNarration {
  /** id točke (TimeSpot.id) */
  spotId: string;
  /** govorna skripta, slovenščina */
  scriptSi: string;
  /** govorna skripta, angleščina */
  scriptEn: string;
}

export const SPOT_NARRATIONS: SpotNarration[] = [
  {
    spotId: "cerkev",
    scriptSi: `Griblje. Časovna točka: Cerkev svetega Vida.

Stojiš pred cerkvijo na pokopališkem gričku južno od jedra vasi. Cerkev je prvič omenjena leta 1526. V rekonstrukciji leta 1825 njen tridimenzionalni model stoji na uradni lokaciji iz registra nepremične kulturne dediščine — z zvonikom. Letos obeležujemo petsto let od prve omembe.

Vir: register nepremične kulturne dediščine, številka 2122, uradni vir. Zapisa MVG-002 in MVG-003. Katastrski list A02, Arhiv Slovenije.`,
    scriptEn: `Griblje. Time spot: the church of Saint Vitus.

You stand before the church on its cemetery hill south of the village core. The church is first mentioned in 1526. In the 1825 reconstruction its three-dimensional model stands at the official heritage-register location — with its bell tower. This year marks five hundred years since the first mention.

Source: the Register of Immovable Cultural Heritage, number 2122, official source. Records MVG-002 and MVG-003. Cadastre sheet A02, Archives of Slovenia.`,
  },
  {
    spotId: "jedro",
    scriptSi: `Griblje. Časovna točka: jedro vasi leta 1825, Grüble.

Sredi vasi, kakršna je bila leta 1825: okoli tebe stoji 156 katastrskih stavb, jedro v dveh sklopih ob cerkvi. Približaj se hišam in jih tapni — vsaka ti pove svoj tloris in postavi vprašanje, kdo je v njej živel: register hiš iz leta 1825 ima 80 lastnikov, matične knjige pa obsegajo leta 1669 do 1947. Današnje jedro leži približno štiristo metrov severneje — vas je zrasla proti severu.

Vir: zapis MVG-001. Katastrski list A02, Arhiv Slovenije, georeferenciran. Register hiš 1825. Matične knjige župnije Podzemelj.`,
    scriptEn: `Griblje. Time spot: the village core in 1825, Grüble.

In the middle of the village as it stood in 1825: 156 cadastre buildings surround you, the core in two clusters by the church. Come closer and tap a house — it shows you its footprint and asks who lived there: the 1825 house register holds 80 owners, and the parish books span the years 1669 to 1947. Today's core lies roughly four hundred metres further north — the village grew northward.

Source: record MVG-001. Georeferenced cadastre sheet A02, Archives of Slovenia. The 1825 house register. The parish books of Podzemelj.`,
  },
  {
    spotId: "kolpa",
    scriptSi: `Griblje. Časovna točka: Kolpa, življenje ob reki.

Ob reki, ki je vasi dala življenje. Med letoma 1809 in 1813 je tu delovala Napoleonova carinarnica, v času Ilirskih provinc. Struga Kolpe je v rekonstrukciji georeferencirana.

Vir: zapisa MVG-006 in MVG-092 — carinarnica 1809 do 1813. Georeferencirana struga reke.`,
    scriptEn: `Griblje. Time spot: the Kolpa, life on the river.

By the river that gave the village life. Between 1809 and 1813 Napoleon's customs post operated here, in the days of the Illyrian Provinces. The Kolpa riverbed is georeferenced in the reconstruction.

Source: records MVG-006 and MVG-092 — the customs post of 1809 to 1813. A georeferenced riverbed.`,
  },
  {
    spotId: "ribnik",
    scriptSi: `Griblje. Časovna točka: vaški ribnik.

Kraj, kjer je vas hranila vodo za živino. Riba sam v prizoru ni — vidiš jedro vasi ob koncu devetnajstega stoletja: oceno zgoščevanja po delitvi domačij, s petintridesetimi novimi stavbami.

Vir: zapis MVG-016. Približno leto 1900 je ocena po metodologiji periode.`,
    scriptEn: `Griblje. Time spot: the village pond.

The place where the village kept water for livestock. The pond itself is not in the scene — you see the village core around 1900: an estimate of densification after the farm divisions, with thirty-five new buildings.

Source: record MVG-016. The year around 1900 is an estimate, by the period methodology.`,
  },
  {
    spotId: "gornje",
    scriptSi: `Griblje. Časovna točka: zgornji konec vasi — spomenik in zaselki.

Severni rob vasi leta 1825; vas je pozneje zrasla še severneje. Zaselki Dolnje, Srednje in Gornje Griblje so zapisani že leta 1526. Tu, pred osnovno šolo, stoji spomenik padlim vaščanom iz leta 1961 — na uradni lokaciji iz registra nepremične kulturne dediščine. Preklopi na danes in primerjaj.

Vir: register nepremične kulturne dediščine, številka 19326, uradni vir. Zapisa MVG-029 in MVG-049 — zaselki 1526.`,
    scriptEn: `Griblje. Time spot: the upper end of the village — memorial and hamlets.

The north end of the 1825 village; it later grew further north still. The hamlets of Dolnje, Srednje and Gornje Griblje are recorded as early as 1526. Here, in front of the primary school, stands the memorial to the fallen villagers from 1961 — at its official heritage-register location. Switch to today and compare.

Source: the Register of Immovable Cultural Heritage, number 19326, official source. Records MVG-029 and MVG-049 — the hamlets of 1526.`,
  },
  {
    spotId: "meja",
    scriptSi: `Griblje. Časovna točka: meja ob Kolpi — danes in duhovi.

Stojiš na meji, ki je tu od leta 1991. Vklopi pogled na danes: žični duhovi hiš iz leta 1825 razmejujejo, kje je stala vas — pogovor med preteklostjo in sedanjostjo.

Vir: zapis MVG-015 — meja 1991. Pogled na danes je interpretacija: žični obris leta 1825.`,
    scriptEn: `Griblje. Time spot: the border on the Kolpa — today and ghosts.

You stand on the border, here since 1991. Switch to the today view: the wireframe ghosts of the 1825 houses trace where the village stood — a dialogue between past and present.

Source: record MVG-015 — the border of 1991. The today view is an interpretation: the 1825 wireframe outline.`,
  },
  {
    spotId: "mlini",
    scriptSi: `Griblje. Časovna točka: mlini ob Kolpi.

Ob Kolpi so mlini mleli žito bližnjih vasi stoletja — urbarji jih navajajo v Dolu, Radencih, Pobrežju in Krasincu. Pred tabo stoji proceduralna scena vodnega mlina: hiša, kolo, jez in toča. Pošteno povejmo: to je rekonstrukcija vrste mlina — žimaln, z vodoravnim kolesom znotraj — ne konkretnega mlina; koordinata zapisa je reprezentativna točka mlinarskega območja. Preklopi na danes — mlin postane duh: večina jih je propadla, Pobrežje je med ohranjenimi.

Vir: zapis MVG-009. Radio Odeon, urbarji. Krajinski park Kolpa. Scena je interpretacija vrste — terenska preverba še čaka.`,
    scriptEn: `Griblje. Time spot: the mills on the Kolpa.

Along the Kolpa, mills ground the grain of nearby villages for centuries — the urbars list them at Dol, Radenci, Pobrežje and Krasinec. Before you stands a procedural water-mill scene: the house, the wheel, the weir and the millstream. Honestly said: this is a reconstruction of the mill type — a žimaln, with a horizontal wheel inside — not of a particular mill; the record coordinate is a representative point of the milling stretch. Switch to today — the mill turns into a ghost: most have decayed, Pobrežje is among the preserved.

Source: record MVG-009. Radio Odeon, the urbars. Kolpa Landscape Park. The scene is an interpretation of the type — a field check is still pending.`,
  },
  {
    spotId: "otok",
    scriptSi: `Griblje. Časovna točka: partizansko letališče Otok, 1944 do 1945.

Na travniku ob vasi Otok pri Metliki, približno deset kilometrov severno od Gribelj, so partizani spomladi 1944 uredili letališče za zavezniška letala. Letala so pristajala ob zatemnitvi, travnik so označili z lučmi. Do konca vojne so od tod odpeljali tisoč štiristo triinsedemdeset ranjencev v zavezniške bolnišnice v južni Italiji; rešili so tudi dvainosemdeset britanskih letalcev. Danes dogodek varuje spominski letal Douglas C-47 Dakota. Točka je samo zgodba: travnik je pred tabo, spomenik stoji fizično — v treh dimenzijah tu ničesar ne dodajamo.

Vir: zapis MVG-013. RTV Slovenija. Wikipedija, Otok pri Metliki. Wikimedia Commons, dokumentarna fotografija 1944. Koordinata je groba — terenska preverba še čaka.`,
    scriptEn: `Griblje. Time spot: the Otok partisan airfield, 1944 to 1945.

On a meadow by the village of Otok near Metlika, roughly ten kilometres north of Griblje, the Partisans laid out an airfield for Allied aircraft in the spring of 1944. The planes landed at blackout, the meadow marked with lanterns. By the end of the war one thousand four hundred and seventy-three wounded had been flown from here to Allied hospitals in southern Italy; eighty-seven British airmen were rescued too. Today a memorial Douglas C-47 Dakota stands guard over the memory. This spot is story-only: the meadow lies before you, the monument stands in the physical world — we add nothing in three dimensions.

Source: record MVG-013. RTV Slovenia. Wikipedia, Otok near Metlika. Wikimedia Commons, documentary photograph 1944. The coordinate is coarse — a field check is still pending.`,
  },
  {
    spotId: "cerkvisce",
    scriptSi: `Griblje. Časovna točka: Cerkvišče — tri cerkvice, ki jih ni več.

Ime vasi je arheologija sama: tu so stale tri cerkvice, Turki pa so jih ob vpadih — od leta 1408 naprej — porušili in zažgali. Pred tabo utripajo trije rdeči duhovi. Za dve domnevno vaščani še vedno vesta, kje sta stali; za tretjo ne ve nihče — postavitev je interpretacija. Ob njih stoji bela kapelica iz leta 1994 — edini kamen, ki danes nosi spomin. Zaselk pripada isti krajevni skupnosti kot Griblje.

Vir: zapis MVG-040. Wikipedija, Cerkvišče. Občina Črnomelj — krajevna skupnost Griblje obsega obe naselji. Sidro iz OpenStreetMap. Duhovi so interpretacija; lega tretje ni znana.`,
    scriptEn: `Griblje. Time spot: Cerkvišče — the three churches that are no more.

The hamlet's name is an archaeology in itself: three churches stood here, and the Turks pulled them down and burned them during the incursions, from around 1408 onwards. Before you, three red ghosts pulse. For two, the villagers still believe they know where they stood; of the third, no one knows — the placement is an interpretation. Beside them stands the white chapel of 1994 — the only stone that still carries the memory. The hamlet belongs to the same local community as Griblje.

Source: record MVG-040. Wikipedia, Cerkvišče. Municipality of Črnomelj — the Griblje local community covers both settlements. An OpenStreetMap anchor. The ghosts are an interpretation; the third position is unknown.`,
  },
];

/** Skripta točke (null, če skripta ni napisana). */
export function getSpotNarration(spot: TimeSpot): SpotNarration | null {
  return SPOT_NARRATIONS.find((n) => n.spotId === spot.id) ?? null;
}

/**
 * Besedilo pripovedi točke v izbranem jeziku. Če skripta manjka,
 * se pošteno uporabi naslov + opis točke (isti vir resnice).
 */
export function narrationText(spot: TimeSpot, lang: "si" | "en"): string {
  const n = getSpotNarration(spot);
  if (n) return lang === "si" ? n.scriptSi : n.scriptEn;
  return `${lang === "si" ? spot.titleSi : spot.titleEn}. ${
    lang === "si" ? spot.descSi : spot.descEn
  }`;
}
