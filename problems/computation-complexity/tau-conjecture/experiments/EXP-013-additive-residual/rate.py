import pickle, sys, time
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "code"))
import scan9add as S

polys = pickle.load(open(S.POLYS, "rb"))["polys"]
N = 5000
arr = np.fromfile(S.FRONTIER / "uniq000.bin", dtype=np.int32).reshape(-1, 7)[:N]
AI, AJ, MI, MJ, SI, SJ = S.build_pairs(10)
c1, c2 = {}, {}
def vals(i, p, c):
    v = c.get(i)
    if v is None:
        v = S.polyvals_mod(polys[i], S.WINDOW, p); c[i] = v
    return v
t0 = time.time()
counts = {}
for thr in (5, 6, 7):
    counts[thr] = 0
full = 0
for row in arr:
    ids = (0, 1, 2) + tuple(int(x) for x in row)
    O1 = np.stack([vals(i, S.P1, c1) for i in ids])
    O2 = np.stack([vals(i, S.P2, c2) for i in ids])
    V1 = np.concatenate([(O1[AI]+O1[AJ]) % S.P1, (O1[MI]*O1[MJ]) % S.P1, (O1[SI]-O1[SJ]) % S.P1])
    V2 = np.concatenate([(O2[AI]+O2[AJ]) % S.P2, (O2[MI]*O2[MJ]) % S.P2, (O2[SI]-O2[SJ]) % S.P2])
    nO1, nO2 = (-O1) % S.P1, (-O2) % S.P2
    eqP = ((V1[:,None,:] == nO1[None,:,:]) & (V2[:,None,:] == nO2[None,:,:])).sum(axis=2)
    eqM = ((V1[:,None,:] == O1[None,:,:]) & (V2[:,None,:] == O2[None,:,:])).sum(axis=2)
    full += int((eqP == 65).sum() + (eqM == 65).sum())
    for thr in (5, 6, 7):
        counts[thr] += int(((eqP >= thr) & (eqP < 65)).sum() + ((eqM >= thr) & (eqM < 65)).sum())
el = time.time() - t0
print(f"states={N} elapsed={el:.1f}s  ({N/el:.0f} states/s, filter only)")
print("full-window (trivial zero) candidates:", full, f"({full/N:.1f}/state)")
for thr in (5, 6, 7):
    print(f"non-trivial candidates at threshold {thr}: {counts[thr]} ({counts[thr]/N:.3f}/state)")
