import io,re
ROOT='ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))'
def rd(p): return io.open(p,encoding="utf-8").read()
def wr(p,s): io.open(p,"w",encoding="utf-8",newline="\n").write(s)
def first_code_idx(s):
    lines=s.splitlines()
    indoc=False
    for i,l in enumerate(lines):
        st=l.strip()
        if not indoc:
            if st.startswith('"""') and st.count('"""')==2 and len(st)>3: continue
            if st.startswith('"""'): indoc=True; continue
            if st.startswith('#') or st=='' : continue
            return i
        else:
            if st.endswith('"""'): indoc=False
            continue
    return 0
targets=["scripts/p248_restore_parish.py","scripts/p245_korekcija_modul.py","scripts/p245_worklog.py",
         "scripts/process-panoramas.py","scripts/p45-sheet-anchors.py","scripts/p45-verify.py"]
for p in targets:
    s=rd(p)
    i=first_code_idx(s)
    lines=s.splitlines()
    ins=[]
    if not re.search(r'^import os$',s,re.M): ins.append("import os")
    if not re.search(r'^ROOT = ',s,re.M): ins.append(ROOT)
    if ins:
        lines[i:i]=ins
        wr(p,"\n".join(lines)+"\n")

# p252_oldverifier_update
p="scripts/p252_oldverifier_update.py"; s=rd(p)
s=s.replace('P236 = "/home/z/my-project/scripts/p236_parish_synthesis_04104.py"', 'P236 = f"{ROOT}/scripts/p236_parish_synthesis_04104.py"')
s=s.replace('p2 = f"/home/z/my-project/scripts/{v}_04455.py"', 'p2 = f"{ROOT}/scripts/{v}_04455.py"')
if not re.search(r'^import os$',s,re.M) or not re.search(r'^ROOT = ',s,re.M):
    i=first_code_idx(s); lines=s.splitlines(); ins=[]
    if not re.search(r'^import os$',s,re.M): ins.append("import os")
    if not re.search(r'^ROOT = ',s,re.M): ins.append(ROOT)
    lines[i:i]=ins; s="\n".join(lines)+"\n"
wr(p,s)
print("done")
