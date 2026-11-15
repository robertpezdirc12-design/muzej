import io,re
qa=io.open("src/lib/qa-parish.ts",encoding="utf-8").read()
for s in ["HOUSE_VITALS.length !== 2081","byBook01738 !== 69","HOUSE_VITALS.length","!== 2081","!== 1940","!== 92","p80Houses"]:
    print(repr(s), qa.count(s))
print([m for m in re.findall(r'HOUSE_VITALS\.length !== \d+', qa)][:5])
print([m for m in re.findall(r'byBook01738 !== \d+', qa)][:5])
