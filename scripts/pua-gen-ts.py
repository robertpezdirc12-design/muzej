# Generiraj TS vrstice za PUA_CONTINUATION iz parsed JSON + križanje s PT registrom
import json, re

parsed = json.load(open('research/p3/pua-12plus-parsed.json'))
entries = parsed['entries']

# PT hiše → lastnik (iz houses.ts)
src = open('src/data/atlas/houses.ts').read()
pt_rows = re.findall(r'\{\s*id:\s*"([^"]+)",\s*no:\s*"([^"]*)",\s*owner:\s*"([^"]*)"', src)
pt_map = {}
for hid, no, owner in pt_rows:
    if no and no not in ('—',):
        pt_map.setdefault(no, owner)

def esc(s):
    return s.replace('\\', '\\\\').replace('"', '\\"')

def compress_sections(sections_str):
    """'I: 841, 851, 856...' → 'I: 841–1743 (26)' če je seznam dolg"""
    out = []
    for part in sections_str.split('; '):
        if not part: continue
        m = re.match(r'^([IV]+):\s*(.*)$', part)
        if not m:
            out.append(part); continue
        sec, nums = m.groups()
        # poskusi stisniti sezname števil
        tokens = [t.strip() for t in re.split(r'[.,]\s*', nums) if t.strip()]
        pure = [t for t in tokens if re.fullmatch(r'\d+', t)]
        extras = [t for t in tokens if not re.fullmatch(r'\d+', t)]
        if len(pure) > 6:
            first, last = pure[0], pure[-1]
            s = f"{sec}: {first}–{last} ({len(pure)})"
            if extras:
                s += f" + {', '.join(extras[:3])}"
            out.append(s)
        else:
            out.append(part)
    return '; '.join(out)

lines = []
for e in entries:
    page, row = e['page'], e['row']
    name = e['nameAsWritten']
    # oznaka negotovosti [~] če je še ni
    if '[~]' not in name and '[?]' not in name:
        name = name + ' [~]'
    name = name.replace('\n', ' ')
    houses = e['house']
    hn = [h for h in houses if h]
    sections = compress_sections(e['sections']) or '—'
    if e.get('bP'):
        sections += f"; b.P. {e['bP']}"
    # križanje s PT
    conf = '~'
    notes = []
    for h in hn:
        try:
            hi = int(float(h))
        except:
            hi = None
        if h in pt_map:
            notes.append(f"PT hiša {h}: {pt_map[h]}")
        elif hi is not None and 41 <= hi <= 60:
            notes.append("PT: 42–60 brez hišnih št. (renumeracija P3)")
        elif h in ('0',):
            notes.append("institucija")
    if e.get('note'):
        n = e['note']
        if 'zap. št. VLM' in n:
            m = re.search(r'VLM prebral (\d+)', n)
            if m:
                notes.append(f"zap. št. prebrana {m.group(1)} [~], po zaporedju strani {row}")
    if notes:
        conf = '~ (' + '; '.join(notes[:2]) + ')'
    house_ts = '[' + ', '.join(f'"{esc(h)}"' for h in hn) + ']'
    lines.append(f'    {{ page: {page}, row: {row}, nameAsWritten: "{esc(name)}", houseNos: {house_ts}, sections: "{esc(sections)}", confidence: "{esc(conf)}" }},')

open('/tmp/pua-rows.ts', 'w').write('\n'.join(lines))
print(f'generiranih vrstic: {len(lines)}')
print('\n'.join(lines[:6]))
print('...')
print('\n'.join(lines[-3:]))
