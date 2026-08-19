"""Preflight for integrated.py: the four ball certificates only."""
import time
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("integrated", HERE / "integrated.py")
integ = importlib.util.module_from_spec(spec)
spec.loader.exec_module(integ)

for i, c in enumerate(integ.COPIES):
    print(i, [float(x) for x in c], flush=True)
for i, bl in enumerate(integ.BALLS):
    t = time.time()
    got = integ.certify_ball(bl)
    print(f"ball {i}: {got} [{time.time()-t:.1f}s]", flush=True)
