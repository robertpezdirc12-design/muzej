import subprocess,os,re
p="scripts/p176_parish_death_1910.py"
r=subprocess.run(["python",p],capture_output=True)
o=(r.stdout+r.stderr).decode("utf-8","replace")
print("rc",r.returncode,"len",len(o))
print("FAIL-lines:",[l for l in o.splitlines() if re.match(r'^\[?FAIL',l)][:5])
print("tail:",o.splitlines()[-2:])
