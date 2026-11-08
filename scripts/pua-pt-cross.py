# P5: navzkrižna analiza PUA (str. 3–34) ↔ PT register hiš — deterministično, brez AI
# Nadaljevanje ključnih ugotovitev P4 (različno številčenje PT/PUA, hišne št. 41–60).
# Izhod: research/p5/pua-pt-cross.json + povzetek za konzolo.
import json, re, unicodedata

# ---------- 1. PT register (houses.ts) ----------
src = open('src/data/atlas/houses.ts', encoding='utf-8').read()
pt_rows = []
for m in re.finditer(
    r'\{\s*id:\s*"([^"]+)",\s*no:\s*"([^"]*)",\s*owner:\s*"([^"]*)"(?:,\s*ownerModernGuess:\s*"([^"]*)")?',
    src):
    hid, no, owner, guess = m.group(1), m.group(2), m.group(3), m.group(4) or ''
    pt_rows.append({'id': hid, 'no': no, 'owner': owner, 'guess': guess,
                    'isParcel': hid.startswith('parcela-')})
house_rows = [r for r in pt_rows if not r['isParcel']]
parcel_rows = [r for r in pt_rows if r['isParcel']]
pt_no_map = {}
for r in house_rows:
    key = r['no'].split(' ')[0].replace('½', '.5')
    try:
        pt_no_map[float(key)] = r
    except ValueError:
        pass

# ---------- 2. PUA vnosi (research.ts PUA_CONTINUATION) ----------
rsrc = open('src/data/atlas/research.ts', encoding='utf-8').read()
pua_rows = []
for m in re.finditer(
    r'\{\s*page:\s*(\d+),\s*row:\s*(\d+),\s*nameAsWritten:\s*"((?:[^"\\]|\\.)*)",\s*houseNos:\s*\[(.*?)\],\s*sections:\s*"((?:[^"\\]|\\.)*)",\s*confidence:\s*"((?:[^"\\]|\\.)*)"\s*\}',
    rsrc):
    page, row = int(m.group(1)), int(m.group(2))
    name = m.group(3).replace('\\"', '"')
    houses = re.findall(r'"([^"]*)"', m.group(4))
    pua_rows.append({'page': page, 'row': row, 'name': name, 'houses': [h for h in houses if h]})

# ---------- 3. normalizacija priimkov ----------
def norm(s):
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
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
    d = lev(a, b)
    return 1.0 - d / max(len(a), len(b))

# priimki PUA: prvi večji token (nemško: zadnji token je ponavadi priimek — tukaj je zapis "Priimek Ime")
def surname_pua(name):
    toks = norm(name).split()
    return toks[0] if toks else ''

def surname_pt(owner):
    toks = norm(owner).split()
    if not toks: return ''
    # PT: "Priimek Ime" ali "Ime (Priimek)" — vzamemo prvi token
    return toks[0]

# ---------- 4. navzkrižna primerjava ----------
results = []
for e in pua_rows:
    if not e['houses']:
        results.append({**e, 'verdict': 'BREZ_HISNE_ST'})
        continue
    for h in e['houses']:
        try: hn = float(str(h).replace('½', '.5'))
        except ValueError:
            results.append({**e, 'house': h, 'verdict': 'NEBERLJIVA_ST'})
            continue
        if hn == 0:
            results.append({**e, 'house': h, 'verdict': 'INSTITUCIJA'})
            continue
        pt = pt_no_map.get(hn)
        if not pt:
            # PUA hrani hišne št. 41–60, ki jih PT nima (str. 5 = parcele)
            if 41 <= hn <= 60:
                results.append({**e, 'house': h, 'verdict': 'PT_PODATKA_NI_NI_St5_PARCELE'})
            else:
                results.append({**e, 'house': h, 'verdict': 'PT_BREZ_VPISA'})
            continue
        s = sim(surname_pua(e['name']), surname_pt(pt['owner']))
        if s >= 0.72:
            v = 'UJEMANJE'
        elif s >= 0.5:
            v = 'VERJETNO_UJEMANJE'
        else:
            v = 'DIVERGENCA'
        results.append({**e, 'house': h, 'ptOwner': pt['owner'], 'ptId': pt['id'],
                        'similarity': round(s, 2), 'verdict': v})

# ---------- 5b. priimki PUA, ki obstajajo KJERKOLI v PT (ne glede na hišno št.) ----------
pt_surnames = [surname_pt(r['owner']) for r in house_rows if surname_pt(r['owner'])]
pua_surname_found = {}
for e in pua_rows:
    sn = surname_pua(e['name'])
    if not sn or len(sn) < 4: continue  # preskoči kratke/glászne smeti
    best = max((sim(sn, ps), ps) for ps in set(pt_surnames)) if pt_surnames else (0, '')
    if best[0] >= 0.72:
        pua_surname_found.setdefault(sn, []).append(
            {'bestPtSurname': best[1], 'puaHouse': e['houses'], 'sim': round(best[0], 2)})
pua_surnames_also = {k: {'bestMatch': v[0]['bestPtSurname'], 'puaHouses': [h for x in v for h in x['puaHouse']]}
                     for k, v in pua_surname_found.items()}

print(f"\nPUA priimki, ki obstajajo KJERKOLI v PT (fuzzy ≥ 0.72): {len(pua_surname_found)}")
for k, v in sorted(pua_surname_found.items()):
    houses = [h for x in v for h in x['puaHouse']]
    print(f"  {k} ~ PT {v[0]['bestPtSurname']} — PUA hiše: {', '.join(houses)}")

# ---------- 6. povzetek ----------
counts = {}
for r in results:
    counts[r['verdict']] = counts.get(r['verdict'], 0) + 1

# pokritost: katere PT hišne št. ima PUA, katere ne
pua_house_nos = set()
for e in pua_rows:
    for h in e['houses']:
        try: pua_house_nos.add(float(str(h).replace('½', '.5')))
        except ValueError: pass
pt_house_nos = set(pt_no_map.keys())
covered = sorted(pua_house_nos & pt_house_nos)
missing_in_pua = sorted(pt_house_nos - pua_house_nos)
extra_in_pua = sorted(pua_house_nos - pt_house_nos)

out = {
    'generatedAt': '2026-10-08',
    'method': 'Deterministična navzkrižna analiza (Levenshtein podobnost priimkov, prag 0.72/0.50) — brez AI; PUA str. 3–34 (69 vnosov) ↔ PT register (84 hišnih vrstic)',
    'puaEntries': len(pua_rows),
    'ptHouseRows': len(house_rows),
    'ptParcelRows': len(parcel_rows),
    'verdictCounts': counts,
    'results': results,
    'ptCoveredByPua': covered,
    'ptMissingInPua': missing_in_pua,
    'puaExtraHouseNos': extra_in_pua,
    'puaSurnamesAlsoInPt': pua_surnames_also,
}
import os
os.makedirs('research/p5', exist_ok=True)
json.dump(out, open('research/p5/pua-pt-cross.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)

print(f"PUA vnosov: {len(pua_rows)} | PT hišnih vrstic: {len(house_rows)} (+ {len(parcel_rows)} parcelnih)")
print('OBSODBE:')
for k, v in sorted(counts.items(), key=lambda x: -x[1]):
    print(f'  {k}: {v}')
print(f"\nPT hišne št. pokrite v PUA: {len(covered)} → {covered}")
print(f"PT hišne št. BREZ PUA vnosa: {len(missing_in_pua)} → {missing_in_pua}")
print(f"PUA hišne št. brez PT vpisa: {len(extra_in_pua)} → {extra_in_pua}")
print('\nDIVERGENCE (podobnost < 0.5):')
for r in results:
    if r['verdict'] == 'DIVERGENCA':
        print(f"  str.{r['page']:2d} #{r['row']:3d} hiša {r.get('house')}: PUA «{r['name'][:40]}» vs PT «{r.get('ptOwner','')[:40]}» (sim {r['similarity']})")
print('\nVERJETNA UJEMANJA (0.5–0.72):')
for r in results:
    if r['verdict'] == 'VERJETNO_UJEMANJE':
        print(f"  str.{r['page']:2d} #{r['row']:3d} hiša {r.get('house')}: PUA «{r['name'][:40]}» vs PT «{r.get('ptOwner','')[:40]}» (sim {r['similarity']})")
