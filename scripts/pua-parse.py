# Parser surovih VLM izpisov PUA str. 12-49 → strukturirani vnosi (format PuaOwnerRow)
import json, re, glob, sys

RAW = sorted(glob.glob('research/p3/pua-raw/pua-*.json'))

def extract_json_block(raw):
    m = re.search(r'```json\s*(.*?)\s*```', raw, re.S)
    if not m: return None, 'no json block'
    txt = m.group(1)
    # popravi surove control znake v nizih: novi znaki vrstic med narekovaji
    fixed = []
    in_str = False
    esc = False
    for ch in txt:
        if esc:
            fixed.append(ch); esc = False; continue
        if ch == '\\':
            fixed.append(ch); esc = True; continue
        if ch == '"':
            in_str = not in_str; fixed.append(ch); continue
        if in_str and ch == '\n':
            fixed.append(' '); continue
        fixed.append(ch)
    try:
        return json.loads(''.join(fixed)), None
    except Exception as e:
        return None, str(e)

def compact_sections(d):
    if isinstance(d, dict):
        parts = []
        for k in sorted(d.keys(), key=lambda x: ['I','II','III','IV','V'].index(x) if x in ['I','II','III','IV','V'] else 99):
            v = str(d[k]).strip()
            if v: parts.append(f"{k}: {v}")
        return '; '.join(parts)
    return str(d) if d else '—'

def normalize_row(page, vlm_row, seq):
    """Vrnemo (row, flag) — zaporedje ima prednost, VLM branje zabeležimo pri odstopanju."""
    try: vr = int(str(vlm_row).strip())
    except: vr = None
    if vr == seq: return seq, None
    if vr is None: return seq, f"zap. št. neberljiva, po zaporedju {seq}"
    return seq, f"VLM prebral {vr}, po zaporedju strani {seq}"

all_entries = []
errors = []
for f in RAW:
    d = json.load(open(f))
    page = d['page']
    data, err = extract_json_block(d['raw'])
    if err or not isinstance(data, list):
        errors.append((page, err)); continue
    for i, e in enumerate(data):
        # zaporedna št. od str. 12 dalje: vsaka stran 2 vnosa (str. 22 ima 3; str. 11 konča z 21)
        # izračunamo kumulativno iz dejanskih števil vnosov
        seq = None
        row, flag = normalize_row(page, e.get('row'), 0)
        name = str(e.get('name', '')).strip()
        house = e.get('house')
        houses = []
        if house is not None:
            hs = str(house).strip()
            if hs and hs not in ('null', '?'):
                houses = [hs]
        secs = compact_sections(e.get('sections'))
        bp = str(e.get('bP', '') or '').strip()
        note = str(e.get('note', '') or '').strip()
        pn = re.search(r'\*\*pageNote\*\*:\s*(.*)', d['raw'], re.S)
        all_entries.append({
            'page': page, 'vlmRow': e.get('row'), 'row': None,
            'nameAsWritten': name, 'house': houses,
            'sections': secs, 'bP': bp, 'note': note,
            'pageNote': (pn.group(1).strip()[:300] if pn else '')
        })

# dodeli zaporedne št.: str. 11 konča z row 21; nadaljujemo po vrstnem redu strani + indeksu vnosa
seq = 21
for e in all_entries:
    seq += 1
    e['row'] = seq
    vr = e.pop('vlmRow')
    try: vr = int(str(vr).strip())
    except: vr = None
    if vr != e['row']:
        e['note'] = (e['note'] + '; ' if e['note'] else '') + f"zap. št. VLM: {vr if vr is not None else 'neberljiva'} → po zaporedju {e['row']}"
    e.pop('pageNote', None)

print(f'skupaj vnosov: {len(all_entries)}, strani: {len(RAW)}, napake: {errors}')
json.dump({'entries': all_entries, 'errors': [str(e) for e in errors]}, open('research/p3/pua-12plus-parsed.json', 'w'), ensure_ascii=False, indent=1)
for e in all_entries:
    print(f"str.{e['page']:2d} #{e['row']:3d} {e['nameAsWritten'][:60]:60s} hiša {','.join(e['house']) or '—':6s} | {e['sections'][:80]}")
