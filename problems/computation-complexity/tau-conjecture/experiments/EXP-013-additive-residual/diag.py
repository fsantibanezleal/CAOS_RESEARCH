import pickle, sys
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "code"))
from tclib.enum import integer_roots, padd, pmul, psub
import scan9add as S

polys = pickle.load(open(S.POLYS, "rb"))["polys"]
arr = np.fromfile(S.FRONTIER / "uniq000.bin", dtype=np.int32).reshape(-1, 7)[:3]
for row in arr[:1]:
    ids = (0, 1, 2) + tuple(int(x) for x in row)
    print("state polys:", [polys[i] for i in ids])
    O1 = np.stack([S.polyvals_mod(polys[i], S.WINDOW, S.P1) for i in ids])
    O2 = np.stack([S.polyvals_mod(polys[i], S.WINDOW, S.P2) for i in ids])
    AI, AJ, MI, MJ, SI, SJ = S.build_pairs(10)
    V1 = np.concatenate([(O1[AI]+O1[AJ]) % S.P1, (O1[MI]*O1[MJ]) % S.P1, (O1[SI]-O1[SJ]) % S.P1])
    V2 = np.concatenate([(O2[AI]+O2[AJ]) % S.P2, (O2[MI]*O2[MJ]) % S.P2, (O2[SI]-O2[SJ]) % S.P2])
    nO1, nO2 = (-O1) % S.P1, (-O2) % S.P2
    eqP = ((V1[:,None,:] == nO1[None,:,:]) & (V2[:,None,:] == nO2[None,:,:])).sum(axis=2)
    eqM = ((V1[:,None,:] == O1[None,:,:]) & (V2[:,None,:] == O2[None,:,:])).sum(axis=2)
    print("eqP max:", eqP.max(), " eqM max:", eqM.max())
    na, nm = len(AI), len(MI)
    opolys = [polys[i] for i in ids]
    def build(vi):
        if vi < na: return padd(opolys[AI[vi]], opolys[AJ[vi]])
        if vi < na+nm:
            k = vi-na; return pmul(opolys[MI[k]], opolys[MJ[k]])
        k = vi-na-nm; return psub(opolys[SI[k]], opolys[SJ[k]])
    shown = 0
    for vi, bi in np.argwhere(eqM >= 5):
        t = build(vi); b = opolys[bi]
        f = psub(t, b)
        print(f"  eqM={eqM[vi,bi]} t={t} b={b} f={f} exact_roots={sorted(integer_roots(f)) if f else 'ZERO'}")
        shown += 1
        if shown >= 6: break
    for vi, bi in np.argwhere(eqP >= 5)[:4]:
        t = build(vi); b = opolys[bi]
        f = padd(t, b)
        print(f"  eqP={eqP[vi,bi]} t={t} b={b} f={f} exact_roots={sorted(integer_roots(f)) if f else 'ZERO'}")
