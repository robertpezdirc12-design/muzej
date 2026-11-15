import subprocess,re
for p in ["p105_parish_baptism_1910.py","p159_parish_death_1893.py","p177_parish_death_1911.py","p190_parish_death_1924.py"]:
    r=subprocess.run(["python","scripts/"+p],capture_output=True)
    o=(r.stdout+r.stderr).decode("utf-8","replace")
    print("="*10,p)
    for l in o.splitlines():
        if re.match(r'^\s*[\[\(]?[✗xX*]?\s*(FAIL|✗)',l) or "FAIL" in l[:60]:
            print("   ",l[:130])
