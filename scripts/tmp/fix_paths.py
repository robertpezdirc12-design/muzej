import io,re
def rd(p): return io.open(p,encoding="utf-8").read()
def wr(p,s): io.open(p,"w",encoding="utf-8",newline="\n").write(s)
ROOT='ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))'

def ensure_os(s):
    if re.search(r'^import os$',s,re.M): return s
    m=re.search(r'^import [^\n]*\n',s,re.M); assert m
    return s[:m.end()]+"import os\n"+s[m.end():]

# 1) preprosti primeri z ROOT
subs=[
 ("scripts/gen-pwa-icons.py", 'OUT = "/home/z/my-project/public/icons"', 'OUT = f"{ROOT}/public/icons"'),
 ("scripts/p248_restore_parish.py", 'F = "/home/z/my-project/src/data/atlas/parish.ts"', 'F = f"{ROOT}/src/data/atlas/parish.ts"'),
 ("scripts/p245_korekcija_json.py", "P = '/home/z/my-project/research/issue17/parish-marriage-1879-04455.json'", 'P = f"{ROOT}/research/issue17/parish-marriage-1879-04455.json"'),
 ("scripts/p245_korekcija_modul.py", "P = '/home/z/my-project/src/data/atlas/parish-marriage-early.ts'", 'P = f"{ROOT}/src/data/atlas/parish-marriage-early.ts"'),
 ("scripts/p245_worklog.py", "P = '/home/z/my-project/worklog.md'", 'P = f"{ROOT}/worklog.md"'),
 ("scripts/p45-sheet-anchors.py", "ROOT = '/home/z/my-project/muzej'", ROOT),
 ("scripts/p45-verify.py", "ROOT = '/home/z/my-project/muzej'", ROOT),
 ("scripts/process-panoramas.py", 'os.makedirs("/home/z/my-project/public/panoramas", exist_ok=True)', 'os.makedirs(f"{ROOT}/public/panoramas", exist_ok=True)'),
 ("scripts/process-panoramas.py", 'out = f"/home/z/my-project/public/panoramas/{name}.jpg"', 'out = f"{ROOT}/public/panoramas/{name}.jpg"'),
 ("scripts/process-panoramas.py", 'prev_out = f"/home/z/my-project/public/panoramas/{name}-preview.jpg"', 'prev_out = f"{ROOT}/public/panoramas/{name}-preview.jpg"'),
]
done=set()
for p,old,new in subs:
    s=rd(p); assert old in s,(p,old); s=s.replace(old,new); wr(p,s); done.add(p)

# ROOT vstavimo tja, kjer ni definiran (vse navedene + process-panoramas)
for p in sorted(done):
    s=rd(p)
    if re.search(r'^ROOT = ',s,re.M) is None:
        s=ensure_os(s)
        m=re.search(r'^(?:import [^\n]*\n)+',s,re.M)
        s=s[:m.end()]+ROOT+"\n"+s[m.end():]
        wr(p,s)

# 2) p252_oldverifier_update.py
p="scripts/p252_oldverifier_update.py"; s=rd(p)
s=s.replace('P236 = "/home/z/my-project/scripts/p236_parish_synthesis_04104.py"', 'P236 = f"{ROOT}/scripts/p236_parish_synthesis_04104.py"')
s=s.replace('p2 = f"/home/z/my-project/scripts/{v}_04455.py"', 'p2 = f"{ROOT}/scripts/{v}_04455.py"')
if re.search(r'^ROOT = ',s,re.M) is None:
    s=ensure_os(s); m=re.search(r'^(?:import [^\n]*\n)+',s,re.M); s=s[:m.end()]+ROOT+"\n"+s[m.end():]
wr(p,s)

# 3) p19_* -> MUZEJ_ANALYSIS env
for p in ["scripts/p19_data_correctness.py","scripts/p19_probe_firstmention.py"]:
    s=rd(p)
    s=s.replace('BASE = "/home/z/my-project/muzej-analysis"', 'BASE = os.environ.get("MUZEJ_ANALYSIS", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "muzej-analysis"))')
    s=ensure_os(s); wr(p,s)
print("done")
