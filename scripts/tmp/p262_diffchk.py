import subprocess,re
d=subprocess.run(["git","diff","-U0","--","scripts"],capture_output=True).stdout.decode("utf-8","replace")
adds=[l for l in d.splitlines() if l.startswith("+") and not l.startswith("+++")]
bads=[l for l in adds if not (l.strip()=="+import os" or l.strip().startswith("+ROOT = os.path.dirname"))]
print("added lines:",len(adds),"unexpected:",len(bads))
print("\n".join(bads[:10]))
