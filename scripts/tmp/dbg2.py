import glob,io,subprocess,os,re
skip=re.compile(r'(cascade|sanacija|_fix|qa_|dokaz|s18_|korekcija|update|restore|append|insert|module|bump|docs|oldverifier|bak)')
files=[p for p in sorted(glob.glob("scripts/p2*.py")) if not skip.search(os.path.basename(p))]
print("p176 in files:", "scripts/p176_parish_death_1910.py" in files, "n=",len(files))
r=subprocess.run(["python","scripts/p176_parish_death_1910.py"],capture_output=True)
o=(r.stdout+r.stderr).decode("utf-8","replace")
print("match test:", [l for l in o.splitlines() if re.match(r'^\[?FAIL', l)][:1], "rc", r.returncode)
