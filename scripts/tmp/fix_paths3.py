import io,re
def rd(p): return io.open(p,encoding="utf-8").read()
def wr(p,s): io.open(p,"w",encoding="utf-8",newline="\n").write(s)
for p in ["scripts/p19_data_correctness.py","scripts/p19_probe_firstmention.py"]:
    s=rd(p)
    assert 'BASE = "/home/z/my-project/muzej-analysis"' in s, p
    s=s.replace('BASE = "/home/z/my-project/muzej-analysis"',
                'BASE = os.environ.get("MUZEJ_ANALYSIS", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "muzej-analysis"))')
    if not re.search(r'^import os$',s,re.M):
        m=re.search(r'^import [^\n]*\n',s,re.M); assert m, p
        s=s[:m.end()]+"import os\n"+s[m.end():]
    wr(p,s)
print("p19 fixed")
