import subprocess,re
for p in ["p176_parish_death_1910.py","p192_parish_death_1885_04106.py","p193_parish_death_1884_04106.py","p194_parish_death_1883_04106.py","p195_parish_death_1882_04106.py","p196_parish_death_1881_04106.py","p197_parish_death_1880_04106.py","p198_parish_death_1879_04106.py","p199_parish_death_1878_04106.py"]:
    r=subprocess.run(["python","scripts/"+p],capture_output=True)
    o=(r.stdout+r.stderr).decode("utf-8","replace")
    fl=[l for l in o.splitlines() if re.match(r'^\[?FAIL',l)]
    print("="*8,p,"rc",r.returncode)
    for l in fl: print("   ",l[:120])
