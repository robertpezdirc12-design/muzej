import io,re
src=io.open("src/data/atlas/parish.ts",encoding="utf-8").read()
print("04894-1916:",len(re.findall(r'bookSignature: "04894",\s*year: 1916',src)))
print("p80Houses:",io.open("src/lib/qa-parish.ts",encoding="utf-8").read().count("p80Houses"))
print("byBook01738 !== 69:",io.open("src/lib/qa-parish.ts",encoding="utf-8").read().count("byBook01738 !== 69"))
print("HOUSE_VITALS.length !== 2081:",io.open("src/lib/qa-parish.ts",encoding="utf-8").read().count("HOUSE_VITALS.length !== 2081"))
