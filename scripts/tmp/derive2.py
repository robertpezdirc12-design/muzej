import io,re
p80=io.open("scripts/p80_parish_md_books.py",encoding="utf-8").read()
for pat in [r'len\(vitals\)[^\n]*', r'len\(houses\)[^\n]*', r'len\(gap\)[^\n]*', r'== \d+[^\n]*']:
    print(pat, re.findall(pat,p80)[:6])
qa=io.open("src/lib/qa-parish.ts",encoding="utf-8").read()
for s in ["!== 1511","!== 446","!== 1032","!== 333",">= 1916",">= 1915","p80Houses.size !== 93","p80Houses.size !== 92","p80Houses.size !== 100"]:
    print("qa",repr(s),qa.count(s))
