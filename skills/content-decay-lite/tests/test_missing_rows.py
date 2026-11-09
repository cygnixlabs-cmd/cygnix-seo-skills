import subprocess, sys, tempfile, os
d = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def run(prev, cur):
    with tempfile.TemporaryDirectory() as t:
        open(f"{t}/p.csv","w").write(prev); open(f"{t}/c.csv","w").write(cur)
        return subprocess.run([sys.executable, f"{d}/scripts/decay.py", f"{t}/p.csv", f"{t}/c.csv"], capture_output=True, text=True).stdout
o = run("Page,Clicks\nhttps://e.com/old,120\n", "Page,Clicks\nhttps://e.com/x,5\n")
assert "UNKNOWN" in o and "LOST" not in o and "lost on declining pages: 0" in o
o = run("Page,Clicks\nhttps://e.com/z,50\n", "Page,Clicks\nhttps://e.com/z,0\n")
assert "LOST" in o and "lost on declining pages: 50" in o
print("ok")
