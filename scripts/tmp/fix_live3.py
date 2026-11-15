import glob,io,re
def rd(p): return io.open(p,encoding="utf-8").read()
def wr(p,s): io.open(p,"w",encoding="utf-8",newline="\n").write(s)
fixed=[]
for p in [x for x in glob.glob("scripts/*.py") if "BASE_URL" in io.open(x,encoding="utf-8").read()]:
    s=rd(p); o=s
    if re.search(r'^import os$', s, re.M) is None:
        m=re.search(r'^import [^\n]*\n', s, re.M)
        s=s[:m.end()]+"import os\n"+s[m.end():]
    if re.search(r'^live = "--live" in sys\.argv$', s, re.M) is None:
        i=s.find("if live")
        assert i!=-1, p
        ls=s[:i].split("\n"); idx=len(ls)-1
        indent=""
        ls.insert(idx, 'live = "--live" in sys.argv')
        s="\n".join(ls)+s[i:]
    if s!=o: wr(p,s); fixed.append(p)
print("fixed",len(fixed)); print("\n".join(fixed))
