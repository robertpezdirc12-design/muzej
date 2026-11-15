import glob,io,subprocess,os,re
skip=re.compile(r'(cascade|sanacija|_fix|qa_|dokaz|s18_|korekcija|update|restore|append|insert|module|bump|docs|oldverifier|bak|tmp)')
files=[p for p in sorted(glob.glob("scripts/p*.py")) if not skip.search(os.path.basename(p))]
fails=[]
for p in files:
    r=subprocess.run(["python",p],capture_output=True)
    o=(r.stdout+r.stderr).decode("utf-8","replace")
    fl=[l for l in o.splitlines() if re.match(r'^\[?FAIL',l) or "Traceback" in l]
    if r.returncode!=0 or fl:
        fails.append((os.path.basename(p), r.returncode, fl[0][:95] if fl else ""))
print("ran",len(files),"fails",len(fails))
for f in fails: print(f)
