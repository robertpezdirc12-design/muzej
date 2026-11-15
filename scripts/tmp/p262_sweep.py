import glob,io,subprocess,os,re
skip=re.compile(r'(cascade|sanacija|_fix|qa_|dokaz|s18_|korekcija|update|restore|append|insert|module|jit|mutat|korek)')
files=[p for p in sorted(glob.glob("scripts/p2*.py")) if not skip.search(os.path.basename(p))]
fails=[]
for p in files:
    r=subprocess.run(["python",p],capture_output=True)
    o=(r.stdout+r.stderr).decode("utf-8","replace")
    if r.returncode!=0 or re.search(r'FAIL|Traceback', o):
        line=[l for l in o.splitlines() if 'FAIL' in l or 'Traceback' in l or 'Error' in l]
        fails.append(f"{os.path.basename(p)} -> {line[0] if line else 'rc='+str(r.returncode)}")
print("ran",len(files),"fails",len(fails))
print("\n".join(fails[:15]))
