import glob,io,subprocess,os,re
skip=re.compile(r'(cascade|sanacija|_fix|qa_|dokaz|s18_|korekcija|update|restore|append|insert|module|bump|docs|oldverifier|bak)')
files=[p for p in sorted(glob.glob("scripts/p2*.py")) if not skip.search(os.path.basename(p))]
fails=[]
for p in files:
    r=subprocess.run(["python",p],capture_output=True)
    o=(r.stdout+r.stderr).decode("utf-8","replace")
    if r.returncode!=0 or "FAIL" in o:
        fails.append(os.path.basename(p))
print("ran",len(files),"fails",len(fails)); print("\n".join(fails))
