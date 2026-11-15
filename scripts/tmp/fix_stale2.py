import io
def rd(p): return io.open(p,encoding="utf-8").read()
def wr(p,s): io.open(p,"w",encoding="utf-8",newline="\n").write(s)
for p in ["scripts/p193_parish_death_1884_04106.py","scripts/p194_parish_death_1883_04106.py","scripts/p195_parish_death_1882_04106.py",
          "scripts/p196_parish_death_1881_04106.py","scripts/p197_parish_death_1880_04106.py","scripts/p198_parish_death_1879_04106.py",
          "scripts/p199_parish_death_1878_04106.py"]:
    s=rd(p); o=s
    s=s.replace('st = qa.count("HOUSE_VITALS.length !== 2043")','st = qa.count("HOUSE_VITALS.length !== 2081")')
    s=s.replace("st >= 100","st >= 160")
    s=s.replace('f"1940-številcev={st}"','f"2081-številcev={st}"')
    s=s.replace('f"1256-številcev={st}"','f"2081-številcev={st}"')
    s=s.replace('pt["corpus"]["vitalsTotal"] == 1940','pt["corpus"]["vitalsTotal"] == 2081')
    s=s.replace('vitals==1375','vitals==2081')
    if s!=o: wr(p,s); print("ok",p)
    else: print("NOCHANGE",p)
