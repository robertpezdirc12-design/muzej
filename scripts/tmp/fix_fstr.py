import io
def wr(p,s): io.open(p,"w",encoding="utf-8",newline="\n").write(s)
def rd(p): return io.open(p,encoding="utf-8").read()

p="scripts/p176_parish_death_1910.py"; s=rd(p)
old='''          f"{qa.count('=== \\"04894\\" && v.year === 1910')}")'''
new='''          f"{n1910}")'''
assert old in s, "p176 pattern"
# insert n1910 before the check call: find the check( ... line start
import re
m=re.search(r'( *)check\("I10[^\n]*\n(?:[^\n]*\n)? *f"\{qa\.count', s)
seg=s[:s.index(old)]
idx=seg.rfind("\ncheck(") if "\ncheck(" in seg else seg.rfind("check(")
# simplest: define n1910 right before the check line that contains qa.count(...1910)
lines=s.split("\n")
for i,l in enumerate(lines):
    if "qa.count('=== \"04894\" && v.year === 1910')" in l and l.strip().startswith("q"):
        pass
# find the check( line index containing '1910' guard
ci=[i for i,l in enumerate(lines) if 'qa.count(\'=== "04894" && v.year === 1910\')' in l]
first=ci[0]
indent=" "*(len(lines[first])-len(lines[first].lstrip()))
lines.insert(first, indent+'n1910 = qa.count(\'=== "04894" && v.year === 1910\')')
s="\n".join(lines).replace(old,new)
wr(p,s)

for p,var,key,cnt in [("scripts/p192_parish_death_1885_04106.py","n04106",'bookSignature: "04106"',433),
                      ("scripts/p199_parish_death_1878_04106.py","n04894",'bookSignature: "04894"',520),
                      ("scripts/p200_parish_death_1877_04106.py","n04894",'bookSignature: "04894"',520)]:
    s=rd(p)
    old=f'f"{{{"04106" if "04106" in key else "04894"}}={{src.count(\'{key.replace(chr(34),chr(92)+chr(34))}\')}}}}"'
    # built manually below instead
    broken=f'''f"{'04106' if '04106' in key else '04894'}={{src.count('bookSignature: \\"{key.split(chr(34))[1]}\\"')}}"'''
    idx=s.find('f"0'+("4106" if "04106" in key else "4894")+"={src.count(")
    assert idx!=-1, (p,"anchor")
    end=s.find('")',idx)
    start=s.rfind("\ncheck(",0,idx)
    line_start=start+1
    indent=" "*(len(s[line_start:].split("\n")[0])-len(s[line_start:].split("\n")[0].lstrip()))
    s=s[:line_start]+indent+f"{var} = src.count('{key}')\n"+s[line_start:end+2].replace(s[idx:end+2], f'f"{var}={{ {var} }}"')+s[end+2:]
    wr(p,s)
print("patched")
