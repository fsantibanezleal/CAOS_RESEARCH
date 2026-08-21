"""Face-rank gate: does every chart's rescaled matrix keep rank >= 3 ON its face?

The atlas's design claim is that each singular collar was rescaled into a
chart whose matrix stays ANALYTIC and FULL RANK up to and including its
face, so boxes touching the face still certify. Two exceptions are known
and closed in closed form (lemma pieces 10 and 11). This gate tests the
claim for every chart: it sets the chart's face parameter to exactly zero,
samples the remaining parameters at random interior points, evaluates the
chart matrix, and reports the third singular value.

A chart whose face sigma_3 is bounded away from zero needs no lemma. A
chart whose face sigma_3 collapses is a rank-dropping face and MUST have
one; the gate names it so the claim cannot be made by assumption.
"""
import random
from fractions import Fraction as F
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parent

def load(name, fname):
    spec = importlib.util.spec_from_file_location(name, HERE / fname)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def sigma3(J):
    """third singular value of the 6x4 midpoint matrix, via Jacobi on Gram."""
    import math
    A = [[float((J[i][j].lo + J[i][j].hi) / 2) if J[i][j] is not None else 0.0
          for j in range(4)] for i in range(6)]
    G = [[sum(A[k][i] * A[k][j] for k in range(6)) for j in range(4)]
         for i in range(4)]
    for _ in range(60):
        off = sum(G[i][j] ** 2 for i in range(4) for j in range(i + 1, 4))
        if off < 1e-28:
            break
        for p in range(4):
            for q in range(p + 1, 4):
                if abs(G[p][q]) < 1e-300:
                    continue
                th = (G[q][q] - G[p][p]) / (2 * G[p][q])
                t = (1 if th >= 0 else -1) / (abs(th) + math.sqrt(th * th + 1))
                c = 1 / math.sqrt(t * t + 1)
                s = t * c
                for k in range(4):
                    a, b = G[k][p], G[k][q]
                    G[k][p], G[k][q] = c * a - s * b, s * a + c * b
                for k in range(4):
                    a, b = G[p][k], G[q][k]
                    G[p][k], G[q][k] = c * a - s * b, s * a + c * b
    ev = sorted((max(G[i][i], 0.0) ** 0.5 for i in range(4)), reverse=True)
    return ev[2]

# chart -> (module file, sgn or None, face index, sampler for the other three)
def r(rnd, lo, hi, den=64):
    return F(rnd.randint(int(lo * den) + 1, int(hi * den) - 1), den)

CHARTS = [
    ("tube-R",        "tube.py",           1,  3, lambda g: [g(0.25, 2.9), g(-2.9, 2.9), g(-0.95, 0.95)]),
    ("tube-L",        "tube.py",          -1,  3, lambda g: [g(0.25, 2.9), g(-2.9, 2.9), g(-0.95, 0.95)]),
    ("deep-R",        "deep.py",           1,  3, lambda g: [g(0.02, 0.12), g(-2.9, 2.9), g(-0.95, 0.95)]),
    ("ulow",          "ulow.py",        None,  0, lambda g: [g(-2.9, 2.9), g(0.3, 2.9), g(-2.9, 2.9)]),
    ("uplow(u=0)",    "uplow.py",       None,  0, lambda g: [g(-2.9, 2.9), g(0.02, 0.24), g(-2.9, 2.9)]),
    ("uplow(p=0)",    "uplow.py",       None,  2, lambda g: [g(0.02, 0.24), g(-2.9, 2.9), g(-2.9, 2.9)]),
    ("fa1(eps=0)",    "fa1.py",         None,  0, lambda g: [g(-0.95, 0.95), g(0.1, 1.4), g(-1.4, 1.4)]),
    ("fa2b(epsB=0)",  "fa2b.py",        None,  2, lambda g: [g(0.05, 0.95), g(-0.95, 0.95), g(-0.95, 0.95)]),
    ("fartube(rf=0)", "fartube.py",     None,  0, lambda g: [g(-0.95, 0.95), g(0.05, 0.6), g(-0.95, 0.95)]),
    ("cb1(rhoc=0)",   "cb1.py",         None,  0, lambda g: [g(-0.95, 0.95), g(0.3, 2.9), g(-2.9, 2.9)]),
    ("cb1f(rhoc=0)",  "cb1f.py",        None,  0, lambda g: [g(-0.95, 0.95), g(0.05, 0.3), g(-0.95, 0.95)]),
    ("bicorner-opp",  "bicorner-opp.py", None, 0, lambda g: [g(-0.95, 0.95), g(0.005, 0.09), g(-0.95, 0.95)]),
    ("bicorner-same", "bicorner-same.py", None, 0, lambda g: [g(-0.95, 0.95), g(0.05, 0.95), g(-0.95, 0.95)]),
    ("m1(rhoq=0)",    "m1chart.py",     None,  2, lambda g: [g(0.02, 0.2), g(-0.95, 0.95), g(-0.95, 0.95)]),
    ("m2-R(Rc=0)",    "m2chart.py",        1,  0, lambda g: [g(0.05, 0.95), g(-2.9, 2.9), g(-0.95, 0.95)]),
]

def main():
    rnd = random.Random(31337)
    print(f"{'chart':16s} {'face':>6s}  {'min sigma3':>12s}  {'median':>12s}   verdict")
    for name, fname, sgn, face_idx, sampler in CHARTS:
        try:
            mod = load(fname[:-3].replace("-", "_"), fname)
            ef = mod.entry_factory("iv") if sgn is None else mod.entry_factory(sgn, "iv")
        except Exception as e:
            print(f"{name:16s} load failed: {e}")
            continue
        vals = []
        for _ in range(60):
            others = sampler(lambda a, b: r(rnd, a, b))
            pt = others[:face_idx] + [F(0)] + others[face_idx:]
            try:
                J = ef([(x, x) for x in pt])
                vals.append(sigma3(J))
            except Exception:
                continue
        if not vals:
            print(f"{name:16s} no evaluable samples")
            continue
        vals.sort()
        mn, med = vals[0], vals[len(vals) // 2]
        drop = mn < 1e-9
        verdict = ("RANK DROPS on the face: needs a lemma" if drop
                   else "full rank on the face: no lemma needed")
        print(f"{name:16s} {face_idx:6d}  {mn:12.3e}  {med:12.3e}   {verdict}")

if __name__ == "__main__":
    main()
