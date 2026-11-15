import io,re
def rd(p): return io.open(p,encoding="utf-8").read()
def wr(p,s): io.open(p,"w",encoding="utf-8",newline="\n").write(s)

# p176
p="scripts/p176_parish_death_1910.py"; s=rd(p)
s=s.replace("VITALS_TOTAL = 1511             # 1205 + 14! (P190 = KONEC-KNJIGE!)",
            "VITALS_TOTAL = 2081             # ZIVO (P262): 1511 -> 2081 (kaskada P238-P262!)")
s=s.replace("KORPUS_HOUSES = 93              # NESPREMENJENO",
            "KORPUS_HOUSES = 94              # ZIVO: 93 -> 94 (P178-h79; vseh-100-his, 94 s-tevkami!)")
s=s.replace('"len(vitals) == 1100" in p80 and "len(houses) == 94" in p80 and "len(gap) == 18" in p80',
            '"len(vitals) == 1940" in p80 and "len(houses) == 94" in p80 and "len(gap) == 18" in p80')
s=s.replace('''check("I10b qa-parish pini 1032 + 333 (P176-kaskada!)",
          qa.count("!== 1511") >= 91 and qa.count("!== 446") >= 25,
          f"1032×{qa.count('!== 1032')}/333×{qa.count('!== 333')}")''',
'''check("I10b qa-parish ZIVI-števec vitals-2081 (P176-kaskada!)",
          qa.count("HOUSE_VITALS.length !== 2081") >= 160,
          f"2081×{qa.count('HOUSE_VITALS.length !== 2081')}")''')
s=s.replace('''check("I10c qa-parish guardi ≥1916 (23× — P176-kaskada!)",
          qa.count(">= 1916") >= 28, f"{qa.count('>= 1915')}")''',
'''check("I10c qa-parish ZIVI byBook01738==69 (P176-kaskada!)",
          qa.count("byBook01738 !== 69") >= 1, f"{qa.count('byBook01738 !== 69')}")''')
s=s.replace('''check("I10d qa-parish p80 = 92 (24× — NESPREMENJENO!)",
          qa.count("p80Houses.size !== 93") >= 24, f"{qa.count('p80Houses.size !== 92')}")''',
'''check("I10d qa-parish ZIVI p80Houses-guardi (≥70×)",
          qa.count("p80Houses") >= 70, f"{qa.count('p80Houses')}")''')
s=s.replace('''check("I11d ni-04894-1916-blokov-še (P182-lead!; P181 = 1915 sedaj v korpusu!)",
          re.search(r'bookSignature: "04894",\\s*year: 1916', src) is None, "")''',
'''check("I11d 04894-1916-blokov = 9 (P184: +9!; P181 = 1915 NESPREMENJEN!)",
          len(re.findall(r'bookSignature: "04894",\\s*year: 1916', src)) == 9,
          str(len(re.findall(r'bookSignature: "04894",\\s*year: 1916', src))))''')
wr(p,s)

# p192
p="scripts/p192_parish_death_1885_04106.py"; s=rd(p)
s=s.replace('qa.count("HOUSE_VITALS.length !== 2043") >= 100','qa.count("HOUSE_VITALS.length !== 2081") >= 160')
s=s.replace('f"1940-številcev={qa.count(\'HOUSE_VITALS.length !== 1870\')}"','f"2081-številcev={qa.count(\'HOUSE_VITALS.length !== 2081\')}"')
wr(p,s)

# p193-p199
for p in ["p193_parish_death_1884_04106.py","p194_parish_death_1883_04106.py","p195_parish_death_1882_04106.py",
          "p196_parish_death_1881_04106.py","p197_parish_death_1880_04106.py","p198_parish_death_1879_04106.py",
          "p199_parish_death_1878_04106.py"]:
    s=rd(p)
    s=s.replace('st = qa.count("HOUSE_VITALS.length !== 2043")','st = qa.count("HOUSE_VITALS.length !== 2081")')
    s=s.replace("st >= 100","st >= 160")
    s=s.replace('f"1940-številcev={st}"','f"2081-številcev={st}"')
    s=s.replace('f"1256-številcev={st}"','f"2081-številcev={st}"')
    s=s.replace('pt["corpus"]["vitalsTotal"] == 1940','pt["corpus"]["vitalsTotal"] == 2081')
    s=s.replace('vitals==1375','vitals==2081')
    wr(p,s)
print("patched")
