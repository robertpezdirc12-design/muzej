# P5-c: W-MOST med registroma — deterministično, brez AI
# Hipoteza [~]: sklic »W.<štev>« v PT (Protokoll stavbnih parcel) kaže na hišno
# številko v PUA (lastniškem registru Grundsteuerkatastra) — most med obema
# različnima številčenjema, ki ju je kvantificirala analiza P5-a (0/64 po imenih).
# Metoda: pridobi vse W. sklice iz houses.ts (hiše + parcele 41–60), pridobi vse
# PUA hišne št. iz research.ts (PUA_CONTINUATION, 69 vnosov), zjoinaj po številki,
# primerjaj priimke z Levenshtein podobnostjo ( prag 0.72/0.50 kot v P5-a ).
# Izhod: research/p5/pua-pt-wbridge.json + povzetek.
# Posebnost: W. številke BREZ PUA protistrani (64, 65, 68 …) so preverljive
# NAPOVEDI za strani 35–49 (priimki P–Ž) — validacijski instrument za P5-b.
import json, re, unicodedata, datetime

# ---------- 1. PT vrstice (houses.ts): id, no, owner, parcelRefs ----------
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

# ---------- 2. izlušči W. sklice ----------
# oblike: "W.10", "W.22/23", "W.20/22", "W.47 [~]", "… · W.64" (parcele)
w_rows = []  # {id, no, owner, W:[…], wRaw, uncertain}
for r in pt_rows:
    ws = []
    uncertain = False
    for m in re.finditer(r'W\.\s*([\d/½\s]+?)(?=\s*[·\]]|\s*$|\s[^/\d])', r['refs']):
        raw = m.group(1).strip()
        if '[~' in r['refs'][m.start():m.end() + 4] or re.search(r'W\.\s*\d+\s*\[~', r['refs']):
            uncertain = True
        nums = [int(x) for x in re.findall(r'\d+', raw)]
        for n in nums:
            ws.append(n)
    if ws:
        w_rows.append({'id': r['id'], 'no': r['no'], 'owner': r['owner'],
                       'isParcel': r['isParcel'], 'W': sorted(set(ws)), 'uncertain': uncertain})

# ---------- 3. PUA vnosi (research.ts) ----------
rsrc = open('src/data/atlas/research.ts', encoding='utf-8').read()
pua_rows = []
for m in re.finditer(
    r'\{\s*page:\s*(\d+),\s*row:\s*(-?\d+),\s*nameAsWritten:\s*"((?:[^"\\]|\\.)*)",\s*houseNos:\s*\[(.*?)\],\s*sections:\s*"((?:[^"\\]|\\.)*)"',
    rsrc):
    page, row = int(m.group(1)), int(m.group(2))
    name = m.group(3).replace('\\"', '"')
    houses = re.findall(r'"([^"]*)"', m.group(4))
    # "20 ali 23" → [20, 23] (VLM negotovost med branjema)
    nums, ambiguous = [], False
    for h in houses:
        if 'ali' in h:
            ambiguous = True
        for n in re.findall(r'\d+', h):
            nums.append(int(n))
    pua_rows.append({'page': page, 'row': row, 'name': name, 'nums': sorted(set(nums)),
                     'ambiguous': ambiguous})

# ---------- 4. normalizacija + Levenshtein (enako kot P5-a) ----------
def norm(s):
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    # posebne črke pred izrezo ne-a-z: ß→ss, æ→ae, œ→oe, ø→o, ł→l
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
        'bau', 'brun', 'baurn'}

def name_tokens(s):
    """vsi imenski žetoni brez opisnikov/krajev (križno-žetonjska primerjava)"""
    return [t for t in norm(s).split() if t not in STOP and len(t) >= 3]

def surname_pt(owner):
    toks = name_tokens(owner)
    return toks[0] if toks else ''

# ---------- 5. JOIN po W številki ----------
w_all = sorted({n for r in w_rows for n in r['W']})
pua_by_num = {}
for p in pua_rows:
    for n in p['nums']:
        pua_by_num.setdefault(n, []).append(p)

join = []
for w in w_all:
    pt_side = [r for r in w_rows if w in r['W']]
    pua_side = pua_by_num.get(w, [])
    entry = {'W': w,
             'pt': [{'id': r['id'], 'no': r['no'], 'owner': r['owner'],
                     'isParcel': r['isParcel']} for r in pt_side],
             'pua': [{'page': p['page'], 'row': p['row'], 'name': p['name'],
                      'ambiguous': p['ambiguous']} for p in pua_side]}
    if pua_side:
        # križno-žetonjska podobnost: VSI imenski žetoni PT vrstic ↔ PUA vnosov
        # (ulovi npr. Gregor↔Georg, Mufa↔Wufa — Kurrent zamenjave črk M/W/B/G)
        best, best_pair = 0.0, None
        for r in pt_side:
            for s_pt in name_tokens(r['owner']):
                for p in pua_side:
                    for s_pua in name_tokens(p['name']):
                        v = sim(s_pt, s_pua)
                        if v > best:
                            best, best_pair = v, (s_pt, s_pua)
        entry['bestTokenSim'] = round(best, 3)
        entry['bestPair'] = best_pair
        entry['verdict'] = ('MATCH' if best >= 0.72 else
                            'PARTIAL' if best >= 0.50 else 'MISMATCH')
        if any(p['ambiguous'] for p in pua_side) or any(r['uncertain'] for r in pt_side):
            entry['verdict'] += '?'
    else:
        # W brez PUA protistrani → NAPOVED za strani 35–49
        entry['verdict'] = 'NO_PUA (napoved za str. 35–49)'
        entry['expectedOwner'] = [r['owner'] for r in pt_side]
    join.append(entry)

# ---------- 6. PUA št. brez W sklica ----------
w_set = set(w_all)
pua_no_w = sorted({n for p in pua_rows for n in p['nums'] if n and n not in w_set})

# ---------- 7. statistika ----------
both = [e for e in join if e['pua']]
stats = {
    'ptRowsWithW': len(w_rows),
    'wRefsTotal': sum(len(r['W']) for r in w_rows),
    'wDistinct': len(w_all),
    'wWithPua': len(both),
    'wNoPua': len([e for e in join if not e['pua']]),
    'match': len([e for e in both if e['verdict'].startswith('MATCH')]),
    'partial': len([e for e in both if e['verdict'].startswith('PARTIAL')]),
    'mismatch': len([e for e in both if e['verdict'].startswith('MISMATCH')]),
    'puaNumsNoW': len(pua_no_w),
    'puaRows': len(pua_rows),
}

out = {
    'meta': {
        'title': 'P5-c: W-most PUA ↔ PT',
        'generated': datetime.date.today().isoformat(),
        'method': ('deterministično (brez AI): W.<n> sklici iz houses.ts (PT, str. 4–5, '
                   'hiše 21–40 + parcele 41–60 + hiša 76½) ⟷ PUA hišne št. iz PUA_CONTINUATION '
                   '(research.ts, 69 vnosov, str. 3–34); priimki po Levenshtein podobnosti, '
                   'prag 0.72 (MATCH) / 0.50 (PARTIAL) — enako kot P5-a'),
        'hypothesis': ('[~] Sklic W.<n> v PT kaže na hišno številko v PUA številčenju '
                       '(W = črka v viru; protistrani priimki se ujemajo nad naključjem '
                       'kljub Kurrent bralnim zmotam).'),
        'caveats': ('Vsa branja so strojna (VLM) s statusom REVIEW; »MISMATCH« je lahko '
                    'bralna zmota in ne dokaz protislovja; PUA vnosov s hišno št. ni nujno '
                    'enolično preslikati (VLM negotovost »20 ali 23«).'),
    },
    'stats': stats,
    'join': join,
    'puaNumsWithoutW': pua_no_w,
    'predictions': {
        'note': ('W številke brez PUA protistrani — pričakovani lastniki po PT; '
                 'preverljivo ob branju strani 35–49 (P5-b).'),
        'items': [{'W': e['W'], 'expectedOwners': e['expectedOwner']}
                  for e in join if not e['pua']],
    },
}
with open('research/p5/pua-pt-wbridge.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

# ---------- 8. povzetek ----------
print('=== P5-c: W-MOST PUA ↔ PT ===')
print(f"PT vrstice z W: {stats['ptRowsWithW']} (sklicev {stats['wRefsTotal']}, "
      f"različnih W {stats['wDistinct']})")
print(f"W z PUA protistrani: {stats['wWithPua']} — MATCH {stats['match']}, "
      f"PARTIAL {stats['partial']}, MISMATCH {stats['mismatch']}")
print(f"W BREZ PUA (napovedi za 35–49): {stats['wNoPua']}")
print(f"PUA št. brez W sklica: {stats['puaNumsNoW']} / {len(pua_no_w)}")
print()
print('--- JOIN (W | verdikt | sim | PT lastnik ↔ PUA priimek) ---')
for e in join:
    if e['pua']:
        pair = e.get('bestPair')
        pairS = f"{pair[0]} ↔ {pair[1]}" if pair else '(brez ujemanja)'
        print(f"W.{e['W']:<3} {e['verdict']:<10} {e.get('bestTokenSim', 0):<5} {pairS}")
    else:
        print(f"W.{e['W']:<3} {e['verdict']:<28} pričakovani: {'; '.join(e['expectedOwner'][:2])}")
print()
print('--- NAPOVEDI za str. 35–49 (preverljivo) ---')
for it in out['predictions']['items']:
    print(f"  PUA h{it['W']}: {' | '.join(it['expectedOwners'])}")
