import io,re
src=io.open("src/data/atlas/parish.ts",encoding="utf-8").read()
qa=io.open("src/lib/qa-parish.ts",encoding="utf-8").read()
vit=re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "([^"]+)",\s*year: (\d+),', src)
print("vitals",len(vit))
d04894=[v for v in vit if v[1]=="04894"]; print("04894",len(d04894))
houses={v[0] for v in vit}; dig={h for h in houses if h.isdigit()}
print("houses",len(houses),"digit",len(dig))
p80=io.open("scripts/p80_parish_baptism_1890.py",encoding="utf-8").read()
for pat in [r'len\(vitals\)[^\n]*', r'len\(houses\)[^\n]*', r'len\(gap\)[^\n]*']:
    print("p80:",re.findall(pat,p80)[:3])
for s in ["!== 1511","!== 446","!== 1032","!== 333",">= 1916",">= 1915","p80Houses.size !== 93","p80Houses.size !== 92"]:
    print("qa.count",repr(s),qa.count(s))
