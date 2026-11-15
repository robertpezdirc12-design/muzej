import glob,io,re
pat=re.compile(r'^ROOT\s*=\s*["\']/home/z/my-project["\']\s*$', re.M)
new='ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))'
changed=[]; skip=[]
for p in glob.glob("scripts/*.py"):
    s=io.open(p,encoding="utf-8").read()
    if "/home/z/my-project" not in s: continue
    if not pat.search(s): skip.append(p); continue
    s2=pat.sub(new,s)
    if "import os" not in s2.split(new)[0]:
        s2 = re.sub(r'^(import [^\n]*\n)', lambda m: m.group(1)+"import os\n", s2, count=1, flags=re.M)
    io.open(p,"w",encoding="utf-8",newline="\n").write(s2)
    changed.append(p)
print("changed",len(changed),"skipped",len(skip)); print("skipped:",skip)
