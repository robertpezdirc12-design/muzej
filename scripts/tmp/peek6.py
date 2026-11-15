import io
for p in ["scripts/p254_house_stories.py","scripts/p258_meja_1831_32_33.py","scripts/p260_notranjost_1835_1836.py"]:
    s=io.open(p,encoding="utf-8").read()
    i=s.find("localhost:3000")
    print("="*12,p)
    print(s[max(0,i-220):i+120].replace("\n","\\n"))
