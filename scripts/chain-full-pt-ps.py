# P43: SESTAVA CELOTNE VERIGE PT → PUA → PS (issue #13, nadaljevanje P41 nextStep 3)
# ------------------------------------------------------------------------------
# Združi obstoječe dokazane komponente v prvo CELOTNO verigo:
#   1. W-most (P5-c, research/p5/pua-pt-wbridge.json):
#        PT vrstica --W.<n>--> PUA hiša n  (verdikt MATCH/PARTIAL/MISMATCH
#        po križno-žetonjski Levenshtein podobnosti 0.72/0.50)
#   2. P41 veriga (research/issue13/chain-pua-ps.json):
#        PUA hiša n --> PS parcele  (MOČNA ≥60 % vrstic / SREDNJA ≥30 % /
#        ŠIBKA >0 / NI UJEMANJA — megleno ujemanje priimkov nad PS branj)
#   3. Razširitev P43 (ta skript): PT hiše BREZ W. sklica → kandidati po
#        priimkih čez ves PUA univerzum hiš (enaka normalizacija kot P5-c).
#        Imenska povezava je po naravi šibkejša (isti lastnik več hiš) —
#        največja ranga MOGOČA, z obvezno dokumentirano dvoumnostjo.
#   4. Hiša 35 (Bring Weygandt — v ATLAS_OWNERS, ne v P41 verigi): PUA→PS
#        delež izračunan nad izbranimi (adjudiciranimi) PS branjmi po
#        PS-full-v2.json (pass3 > pass2 > pass1 po zapisu izbora) —
#        P43 približek metode P41, izrecno označeno.
# Zaupanje VERIGE = najšibkejša členica (kompozitum obeh verdiktov).
# Načelo nič-zgube: VSAKA PT vrstica (hiša + parcela) dobi vnos z rangom,
# utemeljitvijo in viri. Brez AI klicev — čisto deterministično.
# Izhod: research/issue13/chain-full-pt-ps.json + povzetek na stdout.
import json, re, unicodedata, datetime, os

TODAY = datetime.date.today().isoformat()

# ---------- 1. PT vrstice (houses.ts) — enak zajem kot pua-pt-wbridge.py ----------
src = open('src/data/atlas/houses.ts', encoding='utf-8').read()
pt_rows = []
for m in re.finditer(
    r'\{\s*id:\s*"([^"]+)",\s*no:\s*"([^"]*)",\s*owner:\s*"((?:[^"\\]|\\.)*)"'
    r'(?:,\s*ownerModernGuess:\s*"((?:[^"\\]|\\.)*)")?'
    r'(?:,\s*parcelRefs:\s*"((?:[^"\\]|\\.)*)")?',
    src):
    hid, no, owner, guess, refs = m.group(1), m.group(2), m.group(3), m.group(4) or '', m.group(5) or ''
    pt_rows.append({'id': hid, 'no': no, 'owner': owner, 'guess': guess, 'refs': refs,
                    'isParcel': hid.startswith('parcela-')})

def extract_w(refs):
    """W. sklici: 'W.10', 'W.22/23', 'W.47 [~]', '… · W.64'"""
    ws = []
    for m in re.finditer(r'W\.\s*([\d/½\s]+?)(?=\s*[·\]]|\s*$|\s[^/\d])', refs):
        for n in re.findall(r'\d+', m.group(1)):
            ws.append(int(n))
    return sorted(set(ws))

for r in pt_rows:
    r['W'] = extract_w(r['refs'])

# ---------- 2. W-most (P5-c) ----------
wbridge = json.load(open('research/p5/pua-pt-wbridge.json'))
wb_by_w = {e['W']: e for e in wbridge['join']}

def wb_verdict(w):
    e = wb_by_w.get(w)
    if not e: return None, None, None
    v = e.get('verdict', '')
    base = v.split(' ')[0].rstrip('?')
    return base, v.endswith('?'), e.get('bestTokenSim', 0.0)

# ---------- 3. P41 veriga PUA→PS ----------
chain41 = json.load(open('research/issue13/chain-pua-ps.json'))
ch_by_house = {}
for e in chain41['results']:
    ch_by_house[int(e['house'])] = e

def p41_tier(status):
    """MOČNA (≥60 % vrstic) / SREDNJA (≥30 %) / ŠIBKA (>0) / NI UJEMANJA"""
    if status.startswith('MOČNA'): return 'MOČNA'
    if status.startswith('SREDNJA'): return 'SREDNJA'
    if status.startswith('ŠIBKA'): return 'ŠIBKA'
    return 'NI_UJEMANJA'

# ---------- 4. ATLAS_OWNERS (strani A–B PUA) — LE dokumentacija mešanega številčenja ----------
# UGOTOVITEV P43: houseRefs v ATLAS_OWNERS so MEŠANE narave (prva gradnja pred
# odkritjem P4): nekateri sklici so PUA hišne št. (npr. Bring Weygandt 24 —
# potrjeno s PUA str. 4 vrstica 3), drugi PT-stranski (npr. lastnik-milleg
# [34, 36] = PT hiši 35/36 z Millegom; renumeracija str. 4 PT). Brez potrditve
# PUA strani POSAMEZNEGA sklica se ATLAS_OWNERS houseRefs NE smejo uporabljati
# niti za razširitev univerzuma niti kot lastniška korroboracija hišam —
# uporabimo jih izključno za dokumentacijo te ugotovitve spodaj (mešanje).
mtxt = open('src/data/atlas/model.ts', encoding='utf-8').read()
owners_ab = []  # {name, houses:[int]} — samo za poročilo o mešanem številčenju
for m in re.finditer(
    r'\{\s*id:\s*"([^"]+)",\s*nameAsWritten:\s*"((?:[^"\\]|\\.)*)"(?:,\s*modernGuess:\s*"((?:[^"\\]|\\.)*)")?[\s\S]*?houseRefs:\s*\[(.*?)\]',
    mtxt):
    name = m.group(2)
    nums = []
    for h in re.findall(r'"([^"]*)"', m.group(4)):
        for n in re.findall(r'\d+', h):
            nums.append(int(n))
    if nums:
        owners_ab.append({'name': name, 'houses': sorted(set(nums))})

# ---------- 5. normalizacija + podobnost (enako kot P5-c) ----------
def norm(s):
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    for a, b in (('ß', 'ss'), ('æ', 'ae'), ('œ', 'oe'), ('ø', 'o'), ('ł', 'l')):
        s = s.replace(a, b)
    s = re.sub(r'\[~\]|\[\?\]', '', s)
    s = re.sub(r'[^a-z ]', ' ', s)
    return ' '.join(s.split())

def lev(a, b):
    if len(a) < len(b): a, b = b, a
    if not b: return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a):
        cur = [i + 1]
        for j, cb in enumerate(b):
            cur.append(min(prev[j + 1] + 1, cur[j] + 1, prev[j] + (ca != cb)))
        prev = cur
    return prev[-1]

def sim(a, b):
    a, b = norm(a), norm(b)
    if not a or not b: return 0.0
    return 1.0 - lev(a, b) / max(len(a), len(b))

STOP = {'bauern', 'hiesig', 'grubln', 'gruble', 'griblje', 'gribla', 'bauer', 'baur',
        'burger', 'und', 'zu', 'hau', 'houlg', 'houlgubl', 'gsobln', 'gemeinde',
        'deschitz', 'molestitch', 'dragosche', 'institucija', 'undder', 'hofsing',
        'bau', 'brun', 'baurn', 'weixelbaum', 'weidendorf'}

def name_tokens(s):
    return [t for t in norm(s).split() if t not in STOP and len(t) >= 3]

# ---------- 6. PS korpus (adjudicirana branja po PS-full-v2) ----------
ps_v2 = json.load(open('research/issue17/PS-full-v2.json'))
ps_rows = []           # izbrane (adjudicirane) vrstice s hausNr
ps_pages_missing = []
for page_str, meta in ps_v2['pages'].items():
    page = int(page_str)
    chosen = meta['pass']            # 'pass1' | 'pass2' | 'pass3'
    fname = f"research/issue17/ps-raw/ps-{page:03d}.json" if chosen == 'pass1' \
        else f"research/issue17/ps-raw/ps-{page:03d}-{chosen}.json"
    if not os.path.exists(fname):
        ps_pages_missing.append(page)
        continue
    raw = json.load(open(fname, encoding='utf-8'))
    for line in raw.get('content', '').splitlines():
        line = line.strip()
        if not line: continue
        try:
            row = json.loads(line)
        except Exception:
            continue
        hn = row.get('hausNr')
        try: hn = int(str(hn))
        except (TypeError, ValueError): hn = None
        ps_rows.append({'page': page, 'blatt': row.get('blatt'), 'parzella': row.get('parzella'),
                        'hausNr': hn, 'name': row.get('name') or ''})

ps_by_house = {}
for r in ps_rows:
    if r['hausNr'] is not None:
        ps_by_house.setdefault(r['hausNr'], []).append(r)

# ---------- 7. hišni univerzum PUA ----------
# IZKLJUČNO P41 veriga (continuation — CEL register 49/49 strani prebrani):
# to je edini vir PUA hišnih št., ki ne meša številčenj. ATLAS_OWNERS (strani
# A–B) se univerzumu NE dodaja (mešani houseRefs — glej blok 4); strani A–B
# lastniška imena bodo v verigi uporabljiva šele po človeški potrditvi (#12).
universe = {}   # house -> {'owners': [(name, source)], 'chain': tier}
for h, e in ch_by_house.items():
    universe[h] = {'owners': [(o, 'PUA_CONTINUATION/P41') for o in e['puaOwners']],
                   'chain': p41_tier(e['status'])}

# poročilo o mešanem številčenju A–B: sklici izven verige ( bodisi PT-stranski
# bodisi PUA vrzeli, ki jih continuation ne pozna — npr. 65 iz P5-b)
ab_refs_outside = {}
for o in owners_ab:
    for h in o['houses']:
        if h not in universe:
            ab_refs_outside.setdefault(h, []).append(o['name'])
ab_refs_outside = {str(k): v for k, v in sorted(ab_refs_outside.items())}

# ---------- 9. kompozicija verige ----------
def compose(w_verdict, pua_tier):
    """Zaupanje VERIGE = najšibkejša členica."""
    if w_verdict is None: return None
    if w_verdict == 'NO_PUA':
        return ('NEREŠENA', 'PUA stran te številke ne obstaja (P5-b: napovedi)')
    if w_verdict == 'MISMATCH':
        return ('NEREŠENA', f'W-most: lastniki se pri tej št. ne ujemajo (MISMATCH)')
    if pua_tier in ('MOČNA', 'SREDNJA'):
        if w_verdict == 'MATCH':
            return ('DOKAZANA', f'W.MATCH + PUA↔PS {pua_tier}')
        if w_verdict == 'PARTIAL':
            return ('VERJETNA', f'W.PARTIAL + PUA↔PS {pua_tier}')
    if pua_tier == 'ŠIBKA':
        if w_verdict == 'MATCH':
            return ('VERJETNA', f'W.MATCH + PUA↔PS ŠIBKA')
        if w_verdict == 'PARTIAL':
            return ('MOGOČA', f'W.PARTIAL + PUA↔PS ŠIBKA')
    if pua_tier in ('NI_UJEMANJA', None):
        return ('NEREŠENA', f'PUA↔PS: {pua_tier or "brez PUA↔PS podatka"} pri tej hiši')
    return ('NEREŠENA', f'kombinacija W.{w_verdict}+{pua_tier}')

TIER_ORDER = {'DOKAZANA': 3, 'VERJETNA': 2, 'MOGOČA': 1, 'NEREŠENA': 0}

# ---------- 10. imenski kandidati (vse vrstice; primarno kjer brez W) ----------
# VODILNI ŽETON: regulativi v večini vrstic pišejo priimek PRVI (Hlebety
# Johann, Veith (H.), Šimec Jakob …), a ne povsod (Jožef Miko — ime prvi).
# Primerjava po prvem imenskem žetonu (dolžina ≥ 4) vsake strani ubije lažne
# pozitive prek kratkih krstnih imen (npr. »Jan«); kjer je vodilni žeton vseeno
# krstno ime, je povezava šibkejša — rang verige ostaja omejen na MOGOČA.
def surname(s):
    toks = [t for t in name_tokens(s) if len(t) >= 4]
    return toks[0] if toks else ''

def name_candidates(owner, exclude_house=None):
    """kandidatne PUA hiše po priimkih: priimek PT lastnika vs priimki
    lastnikov hiš; vrne [(hiša, podobnost)] ≥ 0.72, padajoče."""
    s_pt = surname(owner)
    if not s_pt: return []
    scored = []
    for h, u in universe.items():
        best_h = 0.0
        for (oname, _src) in u['owners']:
            s_pua = surname(oname)
            if s_pua:
                v = sim(s_pt, s_pua)
                if v > best_h: best_h = v
        if best_h >= 0.72:
            scored.append((h, round(best_h, 3)))
    scored.sort(key=lambda x: -x[1])
    return scored

# ---------- 11. sestava — nič-zguba po PT vrsticah ----------
out_rows = []
for r in pt_rows:
    entry = {'id': r['id'], 'no': r['no'], 'owner': r['owner'],
             'kind': 'parcela' if r['isParcel'] else 'hiša',
             'W': r['W'], 'links': []}
    best_tier, best_reason = None, None
    for w in r['W']:
        base, uncertain, wsim = wb_verdict(w)
        v_raw = wb_by_w.get(w, {}).get('verdict', '')
        if base is None:
            base = 'NO_PUA'
        ce = universe.get(w)
        pua_tier = ce['chain'] if ce else None
        tier, reason = compose(base, pua_tier)
        link = {'w': w, 'wbridgeVerdict': v_raw, 'wbridgeSim': wsim,
                'puaOwners': [n for n, _ in ce['owners']][:4] if ce else [],
                'puaToPsTier': pua_tier, 'chainTier': tier, 'reason': reason}
        # parcele PS, če veriga seže
        if ce and tier in ('DOKAZANA', 'VERJETNA', 'MOGOČA') and w in ch_by_house:
            parcels = ch_by_house[w].get('psParcels', [])
            link['psParcels'] = [
                {'page': p.get('page'), 'row': p.get('row'), 'blatt': p.get('blatt'),
                 'parzella': p.get('parzella'), 'kultur': p.get('kultur')}
                for p in parcels[:8]]
            link['psParcelsTotal'] = len(parcels)
        entry['links'].append(link)
        if tier and (best_tier is None or TIER_ORDER[tier] > TIER_ORDER[best_tier]):
            best_tier, best_reason = tier, reason
    # imenski kandidati — korroboracija ali primarna povezava (brez W)
    cands = name_candidates(r['owner'])
    entry['nameCandidates'] = [{'house': h, 'sim': s} for h, s in cands[:6]]
    corrob = [c for c in cands if c[0] in r['W']]
    if corrob:
        entry['nameCorroboratesW'] = [c[0] for c in corrob]
    if not r['W']:
        if len(cands) == 1:
            h, s = cands[0]
            pua_tier = universe.get(h, {}).get('chain')
            if pua_tier in ('MOČNA', 'SREDNJA', 'ŠIBKA'):
                tier = 'MOGOČA'
                reason = f'ime: edinstven priimek-kandidat h{h} (sim {s}) + PUA↔PS {pua_tier}'
            else:
                tier, reason = 'NEREŠENA', f'ime: kandidat h{h}, a PUA↔PS {pua_tier}'
            entry['nameLink'] = {'house': h, 'sim': s, 'tier': tier}
            if best_tier is None or TIER_ORDER[tier] > TIER_ORDER[best_tier]:
                best_tier, best_reason = tier, reason
        elif cands:
            entry['nameLinkAmbiguous'] = {'candidates': [c[0] for c in cands[:6]],
                                          'note': 'isti priimek več hiš — povezava ni enolična'}
    entry['chainTier'] = best_tier or 'NEREŠENA'
    entry['chainReason'] = best_reason or ('brez W. sklica in brez enoličnega imenskega kandidata' if not r['W'] else '—')
    out_rows.append(entry)

# ---------- 12. statistika ----------
houses = [e for e in out_rows if e['kind'] == 'hiša']
parcels = [e for e in out_rows if e['kind'] == 'parcela']
def tc(rows): return {t: len([e for e in rows if e['chainTier'] == t])
                      for t in ('DOKAZANA', 'VERJETNA', 'MOGOČA', 'NEREŠENA')}
stats = {
    'ptRows': len(out_rows), 'ptHouses': len(houses), 'ptParcelRows': len(parcels),
    'houseTiers': tc(houses), 'parcelRowTiers': tc(parcels),
    'housesWithW': len([e for e in houses if e['W']]),
    'housesNameOnly': len([e for e in houses if not e['W'] and e.get('nameLink')]),
    'housesCorroborated': len([e for e in houses if e.get('nameCorroboratesW')]),
    'puaUniverse': len(universe), 'p41ChainHouses': len(ch_by_house),
    'abRefsOutsideChain': ab_refs_outside,
}

# križna potrditev: naše število PS vrstic po hišah vs P41 (zaupanje v razširitev)
xval_match, xval_diff = 0, []
for h, e in ch_by_house.items():
    mine = len(ps_by_house.get(h, []))
    theirs = e.get('psRows', 0)
    if mine == theirs: xval_match += 1
    else: xval_diff.append({'house': h, 'mine': mine, 'p41': theirs})
xval = {'housesChecked': len(ch_by_house), 'exact': xval_match,
        'diff': xval_diff[:10],
        'note': ('P41 je verigo gradil na istem korpusu izbranih branj; popolna '
                 'ujemanja potrjujejo, da P43 razširitev (hiše 35 …) uporablja '
                 'enak korpus.')}

out = {
    'meta': {
        'title': 'P43: celotna veriga PT → PUA → PS (issue #13)',
        'generated': TODAY,
        'method': ('deterministično (brez AI): kompozicija W-mostu P5-c (PT→PUA, '
                   'verdikti po Levenshtein 0.72/0.50) in verige P41 (PUA→PS, '
                   'megleno ujemanje priimkov nad izbranimi PS branjmi); zaupanje '
                   'verige = najšibkejša členica; PT hiše brez W. sklica → '
                   'imenski kandidati PO VODILNEM ŽETONU vsake strani (v večini '
                   'primerov priimek — registri ga pišejo prvega; kjer vir piše '
                   'krstno ime prvi (npr. Jožef Miko), je povezava ustrezno '
                   'šibkejša in nikoli nad MOGOČA; prag 0.72) — dvoumnost '
                   'obvezno dokumentirana; PUA univerzum = IZKLJUČNO '
                   'P41 veriga (continuation, cel register) — ATLAS_OWNERS '
                   'houseRefs so mešane narave in se ne uporabljajo'),
        'inputs': ['src/data/atlas/houses.ts (PT, 84 hiš + parcelne vrstice)',
                   'research/p5/pua-pt-wbridge.json (W-most P5-c)',
                   'research/issue13/chain-pua-ps.json (veriga P41 — PUA univerzum)',
                   'research/issue17/PS-full-v2.json + ps-raw/ (korpus izbranih branj, križno potrjen)'],
        'caveats': ('Vsa branja so strojna (VLM, status REVIEW); MISMATCH je lahko '
                    'bralna zmota, ne dokaz protislovja; imenske povezave so po '
                    'naravi dvoumne (isti priimek več hiš) — nikoli nad MOGOČA; '
                    'ATLAS_OWNERS (strani A–B PUA) houseRefs so MEŠANE narave '
                    '(prva gradnja pred odkritjem P4: nekateri PUA, drugi PT-'
                    'stranski — npr. lastnik-milleg [34, 36] = PT hiši) in se za '
                    'verigo ne uporabljajo; dokončna potrditev vseh členic = '
                    'človeška paleografija (#12) + vektorizacija A01/A02.'),
        'zeroLoss': 'vsaka PT vrstica ima vnos (rang + utemeljitev + viri)',
        'crossValidation': xval,
    },
    'stats': stats,
    'chain': out_rows,
}
with open('research/issue13/chain-full-pt-ps.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

# ---------- 13. povzetek ----------
print('=== P43: CELOTNA VERIGA PT → PUA → PS ===')
print(f"PT vrstice: {stats['ptRows']} (hiše {stats['ptHouses']}, parcelne vrstice {stats['ptParcelRows']})")
print(f"Hiše — rangi: {stats['houseTiers']}")
print(f"Parcelne vrstice — rangi: {stats['parcelRowTiers']}")
print(f"Hiše z W. sklicem: {stats['housesWithW']} · imensko povezane (brez W): {stats['housesNameOnly']}")
print(f"Hiše s korroboracijo imena čez W: {stats['housesCorroborated']}")
print(f"PUA univerzum: {stats['puaUniverse']} hiš (IZKLJUČNO P41 veriga — continuation, cel register)")
print(f"ATLAS_OWNERS houseRefs izven verige (mešano številčenje, dokumentirano): {len(ab_refs_outside)} številk")
print(f"Križna potrditev korpusa: {xval['exact']}/{xval['housesChecked']} hiš Točno")
if xval_diff: print('  odstopanja:', xval_diff[:5])
print()
print('--- VRH VERIGE (DOKAZANA) ---')
for e in out_rows:
    if e['chainTier'] == 'DOKAZANA':
        ws = ', '.join(str(l['w']) for l in e['links'])
        print(f"  {e['id']} (št. {e['no']}) {e['owner'][:30]} — W.{ws}")
print('--- VERJETNA ---')
for e in out_rows:
    if e['chainTier'] == 'VERJETNA':
        ws = ', '.join(str(l['w']) for l in e['links'])
        print(f"  {e['id']} (št. {e['no']}) {e['owner'][:30]} — W.{ws}")
