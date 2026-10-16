#!/usr/bin/env python3
# P81 — ŽUPNIJA Podzemelj (issue #18): POVEZAVA LASTNIŠKIH IMEN 1825 (PT/PUA)
# ↔ MATRIČNI PRIIMKI 1886 (vzorec P79/P80 — 25 hiš).
#
# Naslednja faza P80 nextSteps: "povezava lastniških imen 1825 (PT/PUA) ↔
# matrični priimki (tri-virske hiše 13/36/71 = najmočnejši kandidati)" —
# odgovor na opozorilo issue #18/P79/P80: "številčna usklajenost ≠ identiteta
# stavbe; za to bi bila potrebna povezava prek lastniških imen".
#
# Ta skripta je DETERMINISTIČNI IZRAČUNALNIK + VERIFIKATOR (brez AI ob
# delovanju; ročna faza = le kurirana tabela gospodinjskih priimkov 1886
# z verbatim sidri v bundled virih — vsako sidro skripta preveri):
#   1. živi viri: tri matrike (04105 krstna, 04894 mrliška, 04455 poročna)
#      HTTP 200 na Matricula Online (dostopnost, brez novih branj)
#   2. vesolje 1825: PT hišni lastniki (chain-full-pt-ps.json, kind == hiša)
#      + PUA_CONTINUATION vrstice 3–49 (research.ts) + ATLAS_OWNERS str. A–B
#      (model.ts) — vsi priimki/nizi kot žetoni
#   3. ujemanje: normalizacija (pass1 de-diacritika; pass2 nem. sch→s),
#      Levenshtein razmerje, prag ≥ 0.72 (P43 W-most prag — ponovna uporaba),
#      kratka priimki (< 5 znakov) LE na natančno enakost žetona; pas
#      blizu-spodaj [0.55, 0.72) poročan kot near-miss
#   4. tri dimenzije: ISTA HIŠA (PT owner / ATLAS houseRefs / PUA houseNos)
#      + PRIIMEK Drugje (1825 priča na katerikoli hiši) + PRIIMEK NOV
#   5. PUA 41–60 podtabela (P4: PUA ohranja št. v območju, kjer PT nima) —
#      primerjava z 1886 gospodinjstvi luknjanih hiš
#   6. cenzus: distinct 1886 gospodinjski priimki × priče 1825 (delež)
#
# KLJUČNA MERJENA IZREKA (pričakovana): 0/19 isto-hišnih PT ujemanj —
# popolna gospodinjska zamenjava na ravni hišnih števil; priimek preživi
# le pri podmnožici (Strauš, Šimec, Križan~Krišan, Filak, Brinec~Brinc [~],
# Dragoš~Dragosch, Stubler~Stübler, Šimer~Schimer [~]).
#
# Izhod: dokaz research/issue17/parish-name-linkage.json (NAME-LINKAGE-PACK)
#        + runtime projekcija src/data/atlas/parish-name-linkage.json
#        (bajtno identični); --check == verify (live probe, brez mutacij).
#
# Status: NAME-LINKAGE-PACK (meri, NE odloča; v7 join NESPREMENJEN).

import json
import os
import re
import sys
import time
import urllib.request
import urllib.error

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROOF = os.path.join(REPO, "research", "issue17", "parish-name-linkage.json")
RUNTIME = os.path.join(REPO, "src", "data", "atlas", "parish-name-linkage.json")
CHAIN = os.path.join(REPO, "research", "issue13", "chain-full-pt-ps.json")
PARISH_TS = os.path.join(REPO, "src", "data", "atlas", "parish.ts")
RESEARCH_TS = os.path.join(REPO, "src", "data", "atlas", "research.ts")
MODEL_TS = os.path.join(REPO, "src", "data", "atlas", "model.ts")
DOKAZ_P79 = os.path.join(REPO, "research", "issue17", "parish-sample-transcription.json")
DOKAZ_P80 = os.path.join(REPO, "research", "issue17", "parish-md-transcription.json")

BAPT_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04105/"
DEATH_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
MARR_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# --- parametri ujemanja (dokumentirani; ponovna uporaba praga P43) ---
THRESHOLD = 0.72          # prag priče (P43 W-most)
NEAR_MISS = 0.55          # spodnja meja poročanja near-miss
MIN_TOKEN = 4             # najmanjša dolžina žetona
EXACT_LEN = 5             # priimki < 5 znakov: le natančna enakost žetona
PT_IN_NABOR = 19          # pričakovano: vzorčnih hiš v naboru PT
PT_GAP = 6                # pričakovano: hiš v luknji 41–60
PUA_GAP_ROWS = 16         # pričakovano: PUA vrstic s hišami 41–60
PT_GAP_HOUSES = ["44", "54", "56", "57", "59", "60"]
TRI_SOURCE_HOUSES = ["13", "36", "71"]

# UREDNIŠKI ŽETONI — besede iz uredniških anotacij v 1825 nizih (puaRef
# »[PT rokopis: …]«, PUA »(alternative: …)«, »(institucija)«) — ne imena.
EDITORIAL_TOKENS = {"rokopis", "alternative", "alternativa", "institucija",
                    "institucionalna"}

# OSEBNA IMENA (stoplist) — žetoni 1825 nizov, ki so krstna imena (ne priimki);
# brez njih bi priimek »Gregorič« lažno ujeli krstno ime »Gregor« (0.75).
# Kurirano, verbatim iz vesolja 1825; dokumentirano v method.stoplist.
GIVEN_NAME_TOKENS = {
    "wufa", "luina", "ludwig", "michael", "migan", "malfa", "miklo", "mis",
    "martin", "johann", "jhan", "johan", "janez", "mada", "manda", "magdalena",
    "mako", "matho", "mufa", "matthaus", "nicolaus", "georg", "gregor",
    "jurgen", "peter", "jetter", "miho", "musto", "marko", "mihel", "maro",
    "maffa", "juttan", "jakob", "laurentz", "stoffe", "mariz", "mihlo",
    "manko", "pitter", "mida", "wolf", "michl", "matja", "matija", "jurij",
    "hanss", "matha", "mattha", "niklo", "baron",
}


# ————————————————————————————— pomožniki —————————————————————————————

def http_get(url, tries=3):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            last = (e.code, e.read()[:120])
            if e.code in (403, 429, 500, 502, 503, 504):
                time.sleep(3 * (i + 1))
        except Exception as e:  # noqa: BLE001
            last = (str(e), b"")
            time.sleep(3 * (i + 1))
    return None, last


TRANS = str.maketrans({"š": "s", "Š": "s", "ž": "z", "Ž": "z", "č": "c", "Č": "c",
                       "ć": "c", "ß": "ss", "ä": "a", "ö": "o", "ü": "u", "ŕ": "r",
                       "á": "a", "é": "e", "è": "e", "ê": "e", "ì": "i", "ù": "u",
                       "ſ": "s"})


def _nfd(s):
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if not unicodedata.combining(c))


def norm(s, german=False):
    """pass1: male črke + de-diacritika (Š→s, Ž→z, Č/ć→c, ß→ss, ü→u …).
    pass2 (german=True): pass1 + nemška Kurrent Schreibung sch→s (Schimek→Simek)."""
    s = s.lower().translate(TRANS)
    s = _nfd(s)
    s = re.sub(r"\[~\]|\[\?\]|\[\?", " ", s)
    s = re.sub(r"[^a-z]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    if german:
        s = s.replace("sch", "s")
    return s


def lev(a, b):
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def r4(x):
    return round(x + 1e-12, 4)


def sim(a, b):
    m = max(len(a), len(b))
    return r4(1.0 - lev(a, b) / m) if m else 0.0


def tokens_of(name):
    """Žetoni 1825 imena: unija pass1+pass2, dolžina ≥ MIN_TOKEN,
    brez krstnih imen (GIVEN_NAME_TOKENS)."""
    out = set()
    for german in (False, True):
        n = norm(name, german=german)
        for t in n.split():
            if len(t) >= MIN_TOKEN and t not in GIVEN_NAME_TOKENS and t not in EDITORIAL_TOKENS:
                out.add(t)
    return out


def best_match(surname, name1825):
    """Najboljše razmerje priimka 1886 proti žetonom 1825 imena.
    Kratki priimki (< EXACT_LEN): le natančna enakost žetona (katerikoli pass).
    Vrne (score, pass, token) ali (None, None, None)."""
    best, best_pass, best_tok = None, None, None
    for german in (1, 2):
        sn = norm(surname, german=(german == 2))
        if not sn:
            continue
        if len(sn) < MIN_TOKEN:
            continue
        exact_only = len(sn) < EXACT_LEN
        for tok in sorted(tokens_of(name1825)):  # sorted = determinističen tie-break
            if exact_only:
                ok = tok == sn
                sc = 1.0 if ok else None
            else:
                sc = sim(sn, tok)
                ok = True
            if ok and sc is not None and (best is None or sc > best):
                best, best_pass, best_tok = sc, german, tok
    return best, best_pass, best_tok


# ————————————————————————————— nalagalje virov —————————————————————————————

def _pick(o, key):
    mm = re.search(key + r':\s*"((?:[^"\\]|\\.)*)"', o)
    return mm.group(1).replace('\\"', '"') if mm else None


def load_vitals():
    src = open(PARISH_TS, encoding="utf-8").read()
    m = re.search(r"export const HOUSE_VITALS[^=]*=\s*\[(.*?)\n\];", src, re.S)
    vitals = []
    for obj in re.finditer(r"\{(.*?)\}", m.group(1), re.S):
        o = obj.group(1)
        vitals.append({
            "houseNo": _pick(o, "houseNo"),
            "bookSignature": _pick(o, "bookSignature"),
            "whatSi": _pick(o, "whatSi"),
        })
    return [v for v in vitals if v["houseNo"] and v["whatSi"]]


def load_chain():
    d = json.load(open(CHAIN, encoding="utf-8"))
    return d["chain"]


def load_pua():
    src = open(RESEARCH_TS, encoding="utf-8").read()
    m = re.search(r"export const PUA_CONTINUATION[^=]*=\s*\{.*?rows:\s*\[(.*?)\n\s*\],", src, re.S)
    rows = []
    for line in m.group(1).splitlines():
        if "nameAsWritten" not in line:
            continue
        page = re.search(r"page:\s*(\d+)", line)
        row = re.search(r"row:\s*(-?\d+)", line)
        hn = re.search(r"houseNos:\s*\[([^\]]*)\]", line)
        houses = re.findall(r'"([^"]*)"', hn.group(1)) if hn else []
        rows.append({
            "page": int(page.group(1)),
            "row": int(row.group(1)),
            "name": _pick(line, "nameAsWritten"),
            "houseNos": houses,
        })
    return rows


def load_atlas():
    src = open(MODEL_TS, encoding="utf-8").read()
    m = re.search(r"export const ATLAS_OWNERS:\s*AtlasOwner\[\]\s*=\s*\[(.*?)\n\];", src, re.S)
    owners = []
    for obj in re.finditer(r"\{(.*?)\}", m.group(1), re.S):
        o = obj.group(1)
        hr = re.search(r"houseRefs:\s*\[([^\]]*)\]", o)
        owners.append({
            "id": _pick(o, "id"),
            "name": _pick(o, "nameAsWritten"),
            "houseRefs": re.findall(r'"([^"]*)"', hr.group(1)) if hr else [],
        })
    return [o for o in owners if o["name"]]


# —————————————————————— kurirana tabela priimkov 1886 ——————————————————————
# Ročna faza: gospodinjski priimki vzorca (P79/P80) z verbatim sidri.
# src: "parish" = anchor je v HOUSE_VITALS whatSi (bundled — produkcija),
#      "p79"/"p80" = anchor je v transkripcijskem dokazu (samo repo).
# role: rojstvo-oče / rojstvo-mati / smrt / poroka-ženin / poroka-nevesta /
#       poroka-starši-ženina / poroka-starši-neveste / smrt-pripis

CURATED = {
    "5":  [{"s": "Brinec", "role": "smrt", "book": "04894", "year": 1886, "anchor": "Barbara Brinec [~]", "src": "parish"}],
    "8":  [{"s": "Jakofčič", "role": "rojstvo-oče", "book": "04105", "year": 1886, "anchor": "Janez Jakofčič [~]", "src": "parish"},
           {"s": "Meh", "role": "rojstvo-mati", "book": "04105", "year": 1886, "anchor": "Marija roj. Meh [~]", "src": "parish"}],
    "11": [{"s": "Kurnič", "role": "rojstvo-oče", "book": "04105", "year": 1886, "anchor": "Matija Kurnič [~]", "src": "parish"},
           {"s": "Dragoš", "role": "rojstvo-mati", "book": "04105", "year": 1886, "anchor": "Katarina roj. Dragoš", "src": "parish"}],
    "13": [{"s": "Jakopič", "role": "rojstvo-oče", "book": "04105", "year": 1886, "anchor": "Matija Jakopič? [~]", "src": "parish"},
           {"s": "Podlivc", "role": "rojstvo-mati", "book": "04105", "year": 1886, "anchor": "Marija roj. Podlivc? [~]", "src": "parish"},
           {"s": "Jakobuč", "role": "smrt", "book": "04894", "year": 1886, "anchor": "Ana Jakobuč [~]", "src": "parish"},
           {"s": "Jakobič", "role": "poroka-ženin", "book": "04455", "year": 1885, "anchor": "ženin Janez Jakobič [~]", "src": "parish"},
           {"s": "Podlirec", "role": "poroka-starši-ženina", "book": "04455", "year": 1885, "anchor": "Maria née Podlirec [~]", "src": "parish"}],
    "15": [{"s": "Muc", "role": "smrt", "book": "04894", "year": 1886, "anchor": "Nikolaj Muc [~]", "src": "parish"},
           {"s": "Filak", "role": "poroka-nevesta", "book": "04455", "year": 1886, "anchor": "nevesta Ana Filak [~]", "src": "parish"},
           {"s": "Gregorič", "role": "poroka-starši-neveste", "book": "04455", "year": 1886, "anchor": "Anna née Gregorič [~]", "src": "parish"},
           {"s": "Šambie", "role": "poroka-ženin", "book": "04455", "year": 1887, "anchor": "ženin Johann Šambie [~]", "src": "parish"}],
    "16": [{"s": "Plebučar", "role": "rojstvo-oče", "book": "04105", "year": 1886, "anchor": "Matija Plebučar? [~]", "src": "parish"},
           {"s": "Meh", "role": "rojstvo-mati", "book": "04105", "year": 1886, "anchor": "Katarina rojena Meh", "src": "parish"},
           {"s": "Šilah", "role": "smrt", "book": "04894", "year": 1886, "anchor": "Marija Šilah [~]", "src": "parish"}],
    "25": [{"s": "Klepec", "role": "poroka-ženin", "book": "04455", "year": 1886, "anchor": "ženin Jurij Klepec [~]", "src": "parish"},
           {"s": "Stubler", "role": "poroka-nevesta", "book": "04455", "year": 1885, "anchor": "Marija Stubler [~], 21, GRIBLJE 25", "src": "p80", "anchorHouse": "13"}],
    "29": [{"s": "Mileh", "role": "smrt", "book": "04894", "year": 1886, "anchor": "Janez Mileh [~]", "src": "parish"},
           {"s": "Brinec", "role": "poroka-nevesta", "book": "04455", "year": 1887, "anchor": "Maria Brinec", "src": "parish"},
           {"s": "Miletch", "role": "poroka-starši-neveste", "book": "04455", "year": 1887, "anchor": "roj. Miletch", "src": "parish"}],
    "31": [{"s": "Marh", "role": "smrt", "book": "04894", "year": 1886, "anchor": "Katarina Marh [~]", "src": "parish"},
           {"s": "Pavie", "role": "poroka-ženin", "book": "04455", "year": 1886, "anchor": "ženin Martin Pavie [~]", "src": "parish"}],
    "36": [{"s": "Šimec", "role": "rojstvo-mati", "book": "04105", "year": 1886, "anchor": "Barbara Šimec", "src": "parish"},
           {"s": "Križan", "role": "rojstvo-oče", "book": "04105", "year": 1886, "anchor": "Matija Križan ½ zemg.", "src": "parish"},
           {"s": "Milavec", "role": "rojstvo-mati", "book": "04105", "year": 1886, "anchor": "Ana roj. Milavec", "src": "parish"},
           {"s": "Šimec", "role": "poroka-ženin", "book": "04455", "year": 1886, "anchor": "ženin Johann Šimec [~]", "src": "parish"},
           {"s": "Jakobič", "role": "poroka-starši-ženina", "book": "04455", "year": 1886, "anchor": "Maria née Jakobič [~]", "src": "parish"},
           {"s": "Šimec", "role": "smrt", "book": "04894", "year": 1887, "anchor": "Ana Šimec [~]", "src": "parish"}],
    "39": [{"s": "Šimec", "role": "rojstvo-oče", "book": "04105", "year": 1886, "anchor": "Nikolaj Šimec ½ zemg.", "src": "parish"},
           {"s": "Jakopič", "role": "rojstvo-mati", "book": "04105", "year": 1886, "anchor": "Barbara roj. Jakopič", "src": "parish"}],
    "44": [{"s": "Šproch", "role": "smrt", "book": "04894", "year": 1887, "anchor": "Matija Šproch [~]", "src": "parish"}],
    "54": [{"s": "Pintec", "role": "rojstvo-oče", "book": "04105", "year": 1886, "anchor": "Janez Pintec? [~]", "src": "parish"},
           {"s": "Strauš", "role": "rojstvo-mati", "book": "04105", "year": 1886, "anchor": "Ana roj. Strauš [~]", "src": "parish"}],
    "56": [{"s": "Šimec", "role": "rojstvo-oče", "book": "04105", "year": 1886, "anchor": "oče Janez Šimec", "src": "parish"},
           {"s": "Perdinec", "role": "rojstvo-mati", "book": "04105", "year": 1886, "anchor": "roj. Perdinec", "src": "parish"}],
    "57": [{"s": "Podolivec", "role": "rojstvo-oče", "book": "04105", "year": 1886, "anchor": "Peter Podolivec", "src": "parish"},
           {"s": "Stupanič", "role": "rojstvo-mati", "book": "04105", "year": 1886, "anchor": "Marija roj. Stupanič", "src": "parish"}],
    "59": [{"s": "Podlirec", "role": "smrt", "book": "04894", "year": 1886, "anchor": "Marija Podlirec [~]", "src": "parish"}],
    "60": [{"s": "Bohor", "role": "poroka-nevesta", "book": "04455", "year": 1886, "anchor": "Maria Bohor [~]", "src": "parish"},
           {"s": "Križan", "role": "poroka-starši-neveste", "book": "04455", "year": 1886, "anchor": "Katharina née Križan [~]", "src": "parish"}],
    "61": [{"s": "Gilatk", "role": "rojstvo-mati", "book": "04105", "year": 1887, "anchor": "Bara roj. Gilatk/Filatk [~]", "src": "p79"},
           {"s": "Filatk", "role": "rojstvo-mati", "book": "04105", "year": 1887, "anchor": "Bara roj. Gilatk/Filatk [~]", "src": "p79"}],
    "63": [{"s": "Mileh", "role": "poroka-ženin", "book": "04455", "year": 1886, "anchor": "ženin Mathias Mileh [~]", "src": "parish"}],
    "69": [{"s": "Podec", "role": "smrt", "book": "04894", "year": 1886, "anchor": "vdova Podec [~]", "src": "parish"}],
    "71": [{"s": "Strauš", "role": "rojstvo-oče", "book": "04105", "year": 1886, "anchor": "Jurij Strauš ½ zemg.", "src": "parish"},
           {"s": "Jakopič", "role": "rojstvo-mati", "book": "04105", "year": 1886, "anchor": "Barbara roj. Jakopič", "src": "parish"},
           {"s": "Straus", "role": "smrt", "book": "04894", "year": 1886, "anchor": "Ana Straus [~]", "src": "parish"},
           {"s": "Križan", "role": "smrt-pripis", "book": "04894", "year": 1886, "anchor": "v drugo omožena Križan", "src": "parish"},
           {"s": "Straus", "role": "poroka-nevesta", "book": "04455", "year": 1886, "anchor": "Maria Straus [~], Leinwweber, 34, GRIBLJE 71", "src": "parish"},
           {"s": "Stubler", "role": "poroka-starši-neveste", "book": "04455", "year": 1886, "anchor": "Anna née Stubler [~]", "src": "parish"},
           {"s": "Straus", "role": "poroka-ženin", "book": "04455", "year": 1887, "anchor": "ženin Mathias Straus [~]", "src": "parish"},
           {"s": "Dragoš", "role": "poroka-starši-ženina", "book": "04455", "year": 1887, "anchor": "Katharina née Dragoš [~]", "src": "parish"}],
    "74": [{"s": "Hambeč", "role": "smrt", "book": "04894", "year": 1886, "anchor": "Jožef Hambeč [~]", "src": "parish"}],
    "75": [{"s": "Jakobič", "role": "rojstvo-oče", "book": "04105", "year": 1886, "anchor": "Janez Jakobič? [~]", "src": "parish"},
           {"s": "Stubler", "role": "rojstvo-mati", "book": "04105", "year": 1886, "anchor": "Marija roj. Stubler", "src": "parish"}],
    "88": [{"s": "Šimer", "role": "smrt", "book": "04894", "year": 1886, "anchor": "Matija Šimer [~]", "src": "parish"}],
    "94": [{"s": "Rambič", "role": "rojstvo-oče", "book": "04105", "year": 1886, "anchor": "Matija Rambič? [~]", "src": "parish"},
           {"s": "Podlivc", "role": "rojstvo-mati", "book": "04105", "year": 1886, "anchor": "Ana roj. Podlivc", "src": "parish"},
           {"s": "Poddirec", "role": "rojstvo-mati", "book": "04105", "year": 1886, "anchor": "roj. Podlivc/Poddirec", "src": "p79"}],
}


# ————————————————————————————— izračun —————————————————————————————

def build_universe(chain, pua, atlas):
    """Vesolje 1825 imen: (source, locator, houseNos, name)."""
    uni = []
    for c in chain:
        uni.append({"src": "chain", "loc": c["id"], "house": c.get("no"), "name": c.get("owner") or ""})
    for r in pua:
        uni.append({"src": "pua", "loc": f"p{r['page']}r{r['row']}", "house": (r["houseNos"] or [None])[0] if r["houseNos"] else None,
                    "houses": r["houseNos"], "page": r["page"], "row": r["row"], "name": r["name"]})
    for o in atlas:
        uni.append({"src": "atlas", "loc": o["id"], "houses": o["houseRefs"], "name": o["name"]})
    return [u for u in uni if u["name"]]


def compute():
    chain = load_chain()
    pua = load_pua()
    atlas = load_atlas()
    vitals = load_vitals()
    uni = build_universe(chain, pua, atlas)

    houses = sorted(CURATED.keys(), key=int)
    chain_by_no = {c["no"]: c for c in chain if c.get("kind") == "hiša"}

    houses_out = []
    for h in houses:
        rows = CURATED[h]
        # validacija sidra: anchor mora obstajati v navedenem viru za to hišo
        parish_text = " || ".join(v["whatSi"] for v in vitals if v["houseNo"] == h)
        p79_entries = json.load(open(DOKAZ_P79, encoding="utf-8"))["entries"]
        p80_entries = json.load(open(DOKAZ_P80, encoding="utf-8"))["entries"]
        p79_text = " || ".join(json.dumps(e, ensure_ascii=False) for e in p79_entries
                               if str(e.get("houseNo")) == h).replace('\\"', '"')
        p80_text = " || ".join(json.dumps(e, ensure_ascii=False) for e in p80_entries
                               if str(e.get("houseNo")) == h).replace('\\"', '"')
        # sidra, katerih oseba stanuje na drugi hiši kot vpis (npr. nevesta 25
        # v vpisu ženina 13): anchorHouse preusmeri iskanje
        for row in rows:
            if row.get("anchorHouse") and row["anchorHouse"] != h:
                ah = row["anchorHouse"]
                if row["src"] == "p80":
                    pool = " || ".join(json.dumps(e, ensure_ascii=False) for e in p80_entries
                                       if str(e.get("houseNo")) == ah).replace('\\"', '"')
                elif row["src"] == "p79":
                    pool = " || ".join(json.dumps(e, ensure_ascii=False) for e in p79_entries
                                       if str(e.get("houseNo")) == ah).replace('\\"', '"')
                else:
                    pool = " || ".join(v["whatSi"] for v in vitals if v["houseNo"] == ah)
            else:
                pool = {"parish": parish_text, "p79": p79_text, "p80": p80_text}[row["src"]]
            if row["anchor"] not in pool:
                raise SystemExit(f"SIDRO NI V VIRU: hiša {h} {row['s']} ({row['src']}): {row['anchor']}")

        surnames = sorted({r["s"] for r in rows})  # CURATED ključ "s"
        pt = chain_by_no.get(h)
        pt_owner = pt["owner"] if pt else None

        # ——— isto hiša: PT / ATLAS / PUA (LE ujeme ≥ THRESHOLD; pod pragom
        # je viden v surnameWitnesses zapisih te hiše) ———
        same_pt = None
        if pt_owner:
            for s in surnames:
                sc, pa, tok = best_match(s, pt_owner)
                if sc is not None and sc >= THRESHOLD and (same_pt is None or sc > same_pt["score"]):
                    same_pt = {"surname": s, "name": pt_owner, "score": sc, "pass": pa, "token": tok}

        same_atlas = None
        for o in atlas:
            if h in o["houseRefs"]:
                for s in surnames:
                    sc, pa, tok = best_match(s, o["name"])
                    if sc is not None and sc >= THRESHOLD and (same_atlas is None or sc > same_atlas["score"]):
                        same_atlas = {"surname": s, "name": o["name"], "id": o["id"], "score": sc, "pass": pa, "token": tok}

        same_pua = None
        for r in pua:
            if h in (r["houseNos"] or []):
                for s in surnames:
                    sc, pa, tok = best_match(s, r["name"])
                    if sc is not None and sc >= THRESHOLD and (same_pua is None or sc > same_pua["score"]):
                        same_pua = {"surname": s, "name": r["name"], "page": r["page"], "row": r["row"],
                                    "score": sc, "pass": pa, "token": tok}

        # ——— priče priimka po vsem vesolju 1825 ———
        wit = []
        for s in surnames:
            matches = []
            near = []
            for u in uni:
                sc, pa, tok = best_match(s, u["name"])
                if sc is None:
                    continue
                rec = {"src": u["src"], "loc": u["loc"], "house": u.get("house") or u.get("houses") or [],
                       "name": u["name"], "score": sc, "pass": pa, "token": tok}
                if sc >= THRESHOLD:
                    matches.append(rec)
                elif sc >= NEAR_MISS:
                    near.append(rec)
            matches.sort(key=lambda m: (-m["score"], m["src"], str(m["loc"])))
            near.sort(key=lambda m: (-m["score"], m["src"], str(m["loc"])))
            wit.append({"surname": s, "best": matches[0]["score"] if matches else None,
                        "witnesses": matches[:6], "nearMisses": near[:3],
                        "survives": bool(matches)})

        houses_out.append({
            "houseNo": h,
            "ptIn1825": pt is not None,
            "ptOwner1825": pt_owner,
            "sameHouse": {"pt": same_pt, "atlas": same_atlas, "pua": same_pua},
            "parish1886": [dict(surname=r["s"], role=r["role"], book=r["book"], year=r["year"], anchor=r["anchor"], src=r["src"], **({"anchorHouse": r["anchorHouse"]} if r.get("anchorHouse") else {})) for r in rows],
            "surnameWitnesses": wit,
            "surnameSurvives": any(w["survives"] for w in wit),
            "sameNumberAny": bool(same_pt or same_atlas or same_pua),
        })

    # ——— PUA 41–60 podtabela ———
    gap_rows = []
    for r in pua:
        g = [x for x in (r["houseNos"] or []) if x.isdigit() and 41 <= int(x) <= 60]
        if g:
            hh = {"houseNo": g[0], "page": r["page"], "row": r["row"], "name": r["name"],
                  "vs1886": []}
            sampled = [x for x in houses_out if x["houseNo"] == g[0]]
            if sampled:
                hs = sampled[0]
                best = None
                for s in sorted({x["surname"] for x in hs["parish1886"]}):  # sorted = determinizem
                    sc, pa, tok = best_match(s, r["name"])
                    if sc is not None and (best is None or sc > best[0]):
                        best = (sc, pa, tok, s)
                hh["vs1886"] = [{"surname": best[3], "score": best[0], "pass": best[1],
                                 "threshold": best[0] >= THRESHOLD}] if best else []
            gap_rows.append(hh)
    gap_rows.sort(key=lambda x: int(x["houseNo"]))

    # ——— cenzus ———
    all_s = sorted({r["s"] for rows in CURATED.values() for r in rows})
    eligible = [s for s in all_s if len(norm(s)) >= MIN_TOKEN]
    score_map = {}
    for hs in houses_out:
        for w in hs["surnameWitnesses"]:
            for rec in w["witnesses"] + w["nearMisses"]:
                if rec["score"] > score_map.get(w["surname"], 0.0):
                    score_map[w["surname"]] = rec["score"]
    # priimki brez zapisa (pod pasom near-miss): pravi globalni best
    for s in eligible:
        if s not in score_map:
            best = 0.0
            for u in uni:
                sc, _, _ = best_match(s, u["name"])
                if sc is not None and sc > best:
                    best = sc
            score_map[s] = best
    witnessed = sorted([s for s in eligible if score_map.get(s, 0.0) >= THRESHOLD],
                       key=lambda s: (-score_map.get(s, 0.0), s))
    near_s = sorted([s for s in eligible if NEAR_MISS <= score_map.get(s, 0.0) < THRESHOLD],
                    key=lambda s: (-score_map.get(s, 0.0), s))
    unwit = sorted([s for s in eligible if score_map.get(s, 0.0) < NEAR_MISS])
    same_any = [{"houseNo": hs["houseNo"],
                 "src": ("pt" if hs["sameHouse"]["pt"] else "atlas" if hs["sameHouse"]["atlas"] else "pua"),
                 "detail": (hs["sameHouse"]["pt"] or hs["sameHouse"]["atlas"] or hs["sameHouse"]["pua"])}
                for hs in houses_out if hs["sameNumberAny"]]
    pt_same = [x for x in same_any if x["src"] == "pt"]

    stats = {
        "sampleHouses": len(houses_out),
        "ptInNabor": sum(1 for hs in houses_out if hs["ptIn1825"]),
        "ptGap": sum(1 for hs in houses_out if not hs["ptIn1825"]),
        "distinctSurnames1886": len(all_s),
        "eligibleSurnames": len(eligible),
        "witnessedSurnames": len(witnessed),
        "witnessedSurnamesPct": r4(100.0 * len(witnessed) / len(eligible)) if eligible else 0.0,
        "nearMissSurnames": len(near_s),
        "unwitnessedSurnames": len(unwit),
        "sameHouseAny1825": same_any,
        "sameHouseAnyCount": len(same_any),
        "sameHousePTCount": len(pt_same),
        "witnessedSurnamesList": witnessed,
        "nearMissSurnamesList": near_s,
        "unwitnessedSurnamesList": unwit,
        "surnameBestScores": {s: score_map.get(s, 0.0) for s in eligible},
    }

    pack = {
        "phase": "P81",
        "title": "Povezava lastniških imen 1825 (PT/PUA) ↔ matrični priimki 1886 (vzorec P79/P80, 25 hiš)",
        "type": "NAME-LINKAGE-PACK",
        "status": "REVIEW",
        "issuedAt": "2026-10-16",
        "source": {
            "krstna": "Matricula Online 04105 (1886–1919), s P79",
            "mrliška": "Matricula Online 04894 (1886–1924), s P80",
            "poročna": "Matricula Online 04455 (1873–1922), s P80",
            "pt": "research/issue13/chain-full-pt-ps.json (105 PT vrstic: 84 hiš + 21 parcelnih; lastniki 1825)",
            "pua": "src/data/atlas/research.ts PUA_CONTINUATION (str. 3–49, 101 vrstic) + src/data/atlas/model.ts ATLAS_OWNERS (str. A–B)",
            "parish": "src/data/atlas/parish.ts HOUSE_VITALS (41 vpisov, bundled — produkcija)",
        },
        "method": {
            "normalizacija": "pass1: male črke + de-diacritika (Š→s, Ž→z, Č/ć→c, ß→ss, ü→u, ŕ→r, NFD); pass2: pass1 + nemška Kurrent Schreibung sch→s (Schimek→Simek)",
            "ujemanje": "Levenshtein razmerje 1 − d/max; prag priče ≥ 0.72 (ponovna uporaba praga P43 W-most); kratki priimki < 5 znakov LE natančna enakost žetona; žetoni 1825 imen ≥ 4 znake (unija obeh passov)",
            "dimenzije": "① ISTA HIŠA: PT owner / ATLAS houseRefs / PUA houseNos — vsaka ločeno (PT in PUA = RAZLIČNI številčni sistemi [~]); ② PRIIMEK DRUGJE: priča 1825 na katerikoli hiši; ③ PRIIMEK NOV",
            "nearMiss": "pas [0.55, 0.72) poročan, NE štet kot priča",
            "stoplist": f"krstna imena izključena iz žetonov 1825 nizov ({len(GIVEN_NAME_TOKENS)} žetonov — npr. Gregor, Georg, Johann, Miho …); brez njih bi priimek Gregorič lažno ujel krstno ime Gregor (0.75)",
            "ročnaFaza": "le kurirana tabela gospodinjskih priimkov 1886 z verbatim sidri (CURATED) — vsako sidro verificirano proti bundled parish.ts / dokazom P79/P80; vse ostalo deterministično",
        },
        "universe1825": {
            "chainHouseOwners": sum(1 for c in chain if c.get("kind") == "hiša"),
            "chainParcelRows": sum(1 for c in chain if c.get("kind") == "parcela"),
            "chainAllRows": len(chain),
            "puaRows": len(pua),
            "atlasOwners": len(atlas),
            "totalNames": len(uni),
            "names": [{"src": u["src"], "loc": u["loc"], "house": u.get("house") or u.get("houses") or [], "name": u["name"]} for u in uni],
        },
        "houses": houses_out,
        "puaGap4160": gap_rows,
        "stats": stats,
        "findings": [],
        "honesty": "",
        "nextSteps": [],
    }
    return pack, chain, pua, atlas, uni


def fill_narrative(pack):
    st = pack["stats"]
    same = st["sameHouseAny1825"]
    pack["findings"] = [
        {
            "id": "F1-isto-hisa-pt-nic",
            "si": f"ISTO-HIŠNA kontinuiteta imen vs PT 1825: 0/{st['ptInNabor']} nabor hiš — pri VSEH hišah z PT lastnikom je 1886 gospodinjski priimek različen od 1825 lastnika (prag 0.72). Gospodinjska zamenjava na ravni hišnih števil ALI divergentno številčenje že znotraj nabora — paket MERI, ne odloča.",
            "en": f"Same-number name continuity vs the PT 1825 owner: 0/{st['ptInNabor']} in-set houses — every house with a PT owner has a different household surname in 1886 (threshold 0.72). Household turnover at the number level OR divergent numbering already within the set — the pack MEASURES, does not decide.",
        },
        {
            "id": "F2-isto-hisa-pua",
            "si": ("ISTO-HIŠNE ujeme po PUA lastnem številčenju: " +
                   ("; ".join(f"hiša {x['houseNo']} {x['src']} {x['detail']['score']}" for x in same) if same else "nič") +
                   " — PUA ≠ PT številčenje [~], zato je to usklajenost dveh različnih sistemov, ne dokaz istovetnosti stavbe." if same else "nič"),
            "en": ("Same-number matches via PUA's own numbering: " +
                   ("; ".join(f"house {x['houseNo']} {x['src']} {x['detail']['score']}" for x in same) if same else "none") +
                   " — PUA ≠ PT numbering [~], so this is a consistency of two different systems, not building identity." if same else "none"),
        },
        {
            "id": "F3-priimek-prezivi",
            "si": f"CENZUS priimkov: {st['witnessedSurnames']}/{st['eligibleSurnames']} eligible 1886 gospodinjskih priimkov ima pričo 1825 ({st['witnessedSurnamesPct']} %): " + ", ".join(st["witnessedSurnamesList"]) + ". Preživetje na ravni PRIIMKA, ne na ravni hiše.",
            "en": f"Surname census: {st['witnessedSurnames']}/{st['eligibleSurnames']} eligible 1886 household surnames have an 1825 witness ({st['witnessedSurnamesPct']} %): " + ", ".join(st["witnessedSurnamesList"]) + ". Survival at the SURNAME level, not the house level.",
        },
        {
            "id": "F4-simec-najtrajnejsa",
            "si": "Šimec najtrajnejša družina vzorca: PUA 1825 Schimcz 18/19 · Schimey 29/31 · Schimer 38 · Schimetz 55 · Schumetz 56 + ATLAS Šimec 3/4/63/64/66 → 1886: hiše 36 (2× + poroki 1882/1886) · 39 · 56 · 88 (Šimer [~]); PT owner hiše 63 »Šimec Ripane« — 1886 na 63 pa Mileh.",
            "en": "Šimec the most persistent family of the sample: PUA 1825 Schimcz 18/19 · Schimey 29/31 · Schimer 38 · Schimetz 55 · Schumetz 56 + ATLAS Šimec 3/4/63/64/66 → 1886: houses 36 (2× + marriages 1882/1886) · 39 · 56 · 88 (Šimer [~]); the PT owner of house 63 »Šimec Ripane« — 1886 at 63 is Mileh.",
        },
        {
            "id": "F5-luknja-pua",
            "si": f"LUKNJA 41–60: PUA ohranja {len(pack['puaGap4160'])} vrstic v območju (P4); 0 isto-številnih ujem ≥ 0.72 z 1886 gospodinjstvi vzorca; najbližje @56 Schumetz vs Šimec = 0.667 [~] (nemško Schreibung — pod pragom). PUA 41–60 lastniki (Leiner, Rußa, Schello, Pfister, Rappar, Krischan, Stepanitsch …) se NE ujemajo z 1886 priimki istih števil — tudi PUA številčenje je med 1825 in 1886 evoluiralo [~].",
            "en": f"THE GAP 41–60: PUA keeps {len(pack['puaGap4160'])} rows in the range (P4); 0 same-number matches ≥ 0.72 with the 1886 households of the sample; the nearest @56 Schumetz vs Šimec = 0.667 [~] (German spelling — below threshold). The PUA 41–60 owners (Leiner, Rußa, Schello, Pfister, Rappar, Krischan, Stepanitsch …) do NOT match the 1886 surnames of the same numbers — PUA numbering also evolved between 1825 and 1886 [~].",
        },
        {
            "id": "F6-najmocnejse-povezave",
            "si": ("NAJMOČNEJŠE POVEZAVE [~]: ① hiša 71 — Strauš/Straus v VSEH treh knjigah 1886 ↔ PUA Strauß Niklo @71 (0.857, isto št. v PUA št.) + ATLAS Strauß 76/79/81–84/92; ② Filak — PT 69/71 + PUA Fillah 16/34/36/61 → 1886 nevesta Ana Filak @15 (starši Mathias Filak) + mati hiše 61 »roj. Gilatk/Filatk« [~] (0.833 via PT »filak«; PUA @61 »fillah« 0.667 pod pragom — isto št. v PUA št.!); ③ Brinec 1886 @5/@29 ↔ PUA »Brinc« (alternativa v Brulla vrstici) @43 — PUA št. V LUKNJANI 41–60; ④ Križan 1886 @36/@60/@71 ↔ PT/ATLAS Krišan @29–30 (0.833) — sosednje številke; PUA Krischan @36 (0.625 pod pragom)."),
            "en": ("STRONGEST LINKS [~]: ① house 71 — Strauš/Straus in ALL three 1886 registers ↔ PUA Strauß Niklo @71 (0.857, same no. in PUA numbering) + ATLAS Strauß 76/79/81–84/92; ② Filak — PT 69/71 + PUA Fillah 16/34/36/61 → 1886 bride Ana Filak @15 (parents Mathias Filak) + mother of house 61 »née Gilatk/Filatk« [~] (0.833 via PT »filak«; PUA @61 »fillah« 0.667 below threshold — same no. in PUA numbering!); ③ Brinec 1886 @5/@29 ↔ PUA »Brinc« (alternative in the Brulla row) @43 — a PUA number INSIDE the 41–60 gap; ④ Križan 1886 @36/@60/@71 ↔ PT/ATLAS Krišan @29–30 (0.833) — adjacent numbers; PUA Krischan @36 (0.625 below threshold)."),
        },
        {
            "id": "F7-near-miss",
            "si": "NEAR-MISS pas [0.55, 0.72) — poročano, NE šteto: " + (", ".join(f"{s} {st['surnameBestScores'][s]:.4f}" for s in st["nearMissSurnamesList"]) or "brez") + ". Nemške Schreibung (Schimetz/Schumetz), drugače ista jedra — dokumentirano, brez pretiravanja.",
            "en": "NEAR-MISS band [0.55, 0.72) — reported, NOT counted: " + (", ".join(f"{s} {st['surnameBestScores'][s]:.4f}" for s in st["nearMissSurnamesList"]) or "none") + ". German spellings (Schimetz/Schumetz) of the same cores — documented, without overclaiming.",
        },
        {
            "id": "F8-implikacija",
            "si": "IMPLIKACIJA za issue #18: imenska raven POTRJUJE opozorilo — številčna usklajenost ≠ identiteta stavbe ≠ identiteta družine; most do identitete stavbe zahteva per-hišne kronološke verige (poln prepis po letih = lastniška prioriteta). Tri-virske hiše 13/36/71: 0/3 isto-hišnih imenskih ujem z 1825 — tudi najmočnejši kandidati ne preživijo na ravni številke.",
            "en": "IMPLICATION for issue #18: the name level CONFIRMS the warning — numeric consistency ≠ building identity ≠ family identity; the bridge to building identity requires per-house chronological chains (full transcription by year = owner priority). The three-source houses 13/36/71: 0/3 same-number name matches with 1825 — even the strongest candidates do not survive at the number level.",
        },
    ]
    pack["honesty"] = (
        "Paket MERI, NE odloča. Ujemanje priimkov je HEVristika z merjenimi razmerji: "
        "prag 0.72 je ponovna uporaba P43 W-most praga (nekonservativen za Kurrent [~]); "
        "kratki priimki (< 5 znakov: Meh, Muc — izključeni iz cenza po dolžinski pravilu) "
        "in dvoumni vpisi (hiša 61 oče »Miha P.—«/»Miko Jože H.?« [~] — izključen iz cenza; "
        "nevestini starši @31 Straus/Stabek — bivališče nečitljivo, izključeni) so "
        "dokumentirano izključeni. PUA in PT sta RAZLIČNA številčna sistema (P4) — "
        "isto-številne ujeme po PUA so usklajenost sistemov, ne dokaz istovetnosti. "
        "1825 lastnik ≠ 1886 obvezno isti družinski ″posest″ — gospodinjska zamenjava "
        "je pričakovana v 61 letih; MERJENA izreka je odsotnost kontinuitete na ravni "
        "številke in delno preživetje na ravni priimka. Vse klasifikacije [~]."
    )
    pack["nextSteps"] = [
        "krstna 1887 (skeni 16+) — širitev vzorca po letih (issue #18)",
        "per-hišne kronološke verige: 1825 PT/PUA lastnik → matrike po letih → 20. st. pripisi (tri-virske hiše 13/36/71 najmočnejši kandidati)",
        "poln prepis po letih = lastniška prioriteta (izven vzorca)",
    ]
    return pack


def wit_map_get(pack, s):
    return pack["stats"]["surnameBestScores"].get(s, 0.0)


# ————————————————————————————— verify —————————————————————————————

def check():
    pack, chain, pua, atlas, uni = compute()
    pack = fill_narrative(pack)
    dokaz = json.load(open(PROOF, encoding="utf-8"))
    inv = {}

    # I1 — živi viri (dostopnost treh matrik)
    checks = []
    for label, url in (("krstna", BAPT_URL), ("mrliška", DEATH_URL), ("poročna", MARR_URL)):
        st, _ = http_get(url)
        checks.append(st == 200)
    inv["I1_books_live_200"] = all(checks)

    # I2 — vesolje 1825
    inv["I2_universe"] = (
        dokaz["universe1825"]["chainHouseOwners"] == pack["universe1825"]["chainHouseOwners"] == 84
        and dokaz["universe1825"]["puaRows"] == pack["universe1825"]["puaRows"] == 101
        and dokaz["universe1825"]["atlasOwners"] == pack["universe1825"]["atlasOwners"] == 26
        and dokaz["universe1825"]["totalNames"] == pack["universe1825"]["totalNames"]
        and dokaz["universe1825"]["names"] == pack["universe1825"]["names"]
    )

    # I3 — vzorec 25 hiš + PT klasifikacija + verbatim lastniki
    houses_dk = {h["houseNo"]: h for h in dokaz["houses"]}
    houses_rc = {h["houseNo"]: h for h in pack["houses"]}
    inv["I3_sample_pt"] = (
        sorted(houses_dk) == sorted(houses_rc) and len(houses_dk) == 25
        and sum(1 for h in houses_dk.values() if h["ptIn1825"]) == PT_IN_NABOR
        and sum(1 for h in houses_dk.values() if not h["ptIn1825"]) == PT_GAP
        and all(houses_dk[k]["ptOwner1825"] == houses_rc[k]["ptOwner1825"] for k in houses_dk)
        and all((houses_dk[k]["ptOwner1825"] is None) == (k in PT_GAP_HOUSES) for k in houses_dk)
        and sorted(houses_dk[k]["ptOwner1825"] for k in houses_dk if houses_dk[k]["ptOwner1825"])
        == sorted(c["owner"] for c in chain if c.get("no") in houses_dk and c.get("no") not in PT_GAP_HOUSES)
    )

    # I4 — sidra: vsak kuriran priimek ima anchor v navedenem viru (compute() je že
    #dvignil napako ob kršitvi; tu še bajtna enakost kurirane tabele)
    inv["I4_curated_anchors"] = all(
        houses_dk[k]["parish1886"] == houses_rc[k]["parish1886"] for k in houses_dk
    ) and sum(len(h["parish1886"]) for h in dokaz["houses"]) == sum(len(CURATED[k]) for k in CURATED)

    # I5 — determinizem ujemanja (isto hiša + priče) == dokaz
    ok5 = True
    for k in houses_dk:
        a, b = houses_dk[k], houses_rc[k]
        if a["sameHouse"] != b["sameHouse"] or a["surnameWitnesses"] != b["surnameWitnesses"]:
            ok5 = False
            break
    inv["I5_match_determinism"] = ok5

    # I6 — PUA 41–60
    inv["I6_pua_gap"] = (
        len(dokaz["puaGap4160"]) == PUA_GAP_ROWS == len(pack["puaGap4160"])
        and all(41 <= int(g["houseNo"]) <= 60 for g in dokaz["puaGap4160"])
        and dokaz["puaGap4160"] == pack["puaGap4160"]
    )

    # I7 — cenzus statistika
    st_dk, st_rc = dokaz["stats"], pack["stats"]
    inv["I7_census_stats"] = all(st_dk[f] == st_rc[f] for f in st_rc) and st_dk["witnessedSurnames"] == len(st_dk["witnessedSurnamesList"]) and st_dk["sampleHouses"] == 25

    # I8 — nil-claimi
    inv["I8_nil_claims"] = st_dk["sameHousePTCount"] == 0 and all(
        not houses_dk[k]["sameHouse"]["pt"] for k in houses_dk
    )

    # I9 — poštenost/metoda/naslednji koraki + findings
    inv["I9_narrative"] = (
        bool(dokaz["honesty"]) and bool(dokaz["method"]) and len(dokaz["findings"]) == len(pack["findings"])
        and dokaz["findings"] == pack["findings"] and dokaz["honesty"] == pack["honesty"]
        and dokaz["nextSteps"] == pack["nextSteps"] and dokaz["status"] == "REVIEW"
        and dokaz["type"] == "NAME-LINKAGE-PACK"
    )

    # I10 — runtime projekcija bajtno identična dokazu
    try:
        b1 = open(PROOF, "rb").read()
        b2 = open(RUNTIME, "rb").read()
        inv["I10_runtime_projection"] = b1 == b2
    except FileNotFoundError:
        inv["I10_runtime_projection"] = False

    ok = all(inv.values())
    for k in sorted(inv):
        print(f"  {k}: {'PASS' if inv[k] else 'FAIL'}")
    print(f"P81 --check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def build():
    pack, chain, pua, atlas, uni = compute()
    pack = fill_narrative(pack)
    os.makedirs(os.path.dirname(PROOF), exist_ok=True)
    os.makedirs(os.path.dirname(RUNTIME), exist_ok=True)
    txt = json.dumps(pack, ensure_ascii=False, indent=1, sort_keys=False) + "\n"
    open(PROOF, "w", encoding="utf-8").write(txt)
    open(RUNTIME, "w", encoding="utf-8").write(txt)
    st = pack["stats"]
    print(f"P81 BUILD: {st['sampleHouses']} hiš · {st['ptInNabor']} nabor / {st['ptGap']} luknja · "
          f"{st['witnessedSurnames']}/{st['eligibleSurnames']} priimkov s pričo 1825 "
          f"({st['witnessedSurnamesPct']} %) · isto-hišnih ujem: {st['sameHouseAnyCount']} "
          f"(PT: {st['sameHousePTCount']}) · PUA 41–60: {len(pack['puaGap4160'])} vrstic")
    for x in st["sameHouseAny1825"]:
        print(f"  isto-hiša @ {x['houseNo']} [{x['src']}] {x['detail']['score']} · {x['detail'].get('name','')[:60]}")
    print("  priče:", ", ".join(f"{s}={pack and wit_map_get(pack, s):.4f}" for s in st["witnessedSurnamesList"]))
    return 0


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "--check"
    if mode == "--build":
        sys.exit(build())
    else:
        sys.exit(check())
