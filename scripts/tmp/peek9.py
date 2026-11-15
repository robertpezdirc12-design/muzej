import glob,io
for p in [x for x in glob.glob("scripts/*.py") if "/home/z/my-project" in io.open(x,encoding="utf-8").read()]:
    s=io.open(p,encoding="utf-8").read()
    print("="*12,p)
    for l in s.splitlines():
        if "/home/z/my-project" in l: print("   ",l.strip()[:140])
