"""EXP-138: independent re-implementation of de Bondt's homogenization of Alpöge's map (arXiv:2610.24889,
anc/section2a.mac, read as text only) and exact verification of the resulting unipotent homogeneous
degree-7 map on C^15: Keller (det J = 1) and non-injective (an explicit rational collision).

Run from the repository root:
  .venv/Scripts/python.exe problems/algebraic-geometry/jacobian-conjecture/experiments/EXP-138-mathieu-su15/run.py
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
T = sp.Symbol("t", positive=True)
LOG: list[str] = []


def log(msg: str) -> None:
    line = f"{time.strftime('%H:%M:%S')} {msg}"
    LOG.append(line)
    print(line, flush=True)


def xs(n: int) -> list[sp.Symbol]:
    return list(sp.symbols(f"x1:{n + 1}"))


def scale(f, n: int, d) -> sp.Expr:
    """f(t^d * x1, ..., t^d * xn), expanded."""
    x = xs(n)
    return sp.expand(f.subs({x[i]: T ** d * x[i] for i in range(n)}, simultaneous=True))


def total_degree(f, n: int) -> int:
    return sp.Poly(scale(f, n, 1), T).degree()


def homogeneous_part(f, n: int, d: int) -> sp.Expr:
    """Part of f of total degree d in (x1..xn, t)."""
    x = xs(n)
    poly = sp.Poly(sp.expand(f), *x, T)
    return sp.Add(*[c * sp.Mul(*[v ** e for v, e in zip(x + [T], m)]) for m, c in poly.terms() if sum(m) == d])


def reduce_degree(f, n: int, d: int):
    degf = total_degree(f, n)
    if degf <= d:
        return f, 0
    lead = homogeneous_part(f, n, degf)
    h = sp.expand(sp.cancel(lead / T ** (degf - d))) + sp.Symbol(f"x{n + 1}")
    g = sp.expand(f - h * T ** (degf - d))
    return g, h


def reduce_map(F: list, d: int) -> list:
    n = len(F)
    m = n
    G = [sp.expand(sp.cancel(scale(sp.expand(fi / T ** (d - 2)), n, d - 2))) for fi in F]
    for i in range(n):
        g, h = reduce_degree(G[i], m, d)
        while h != 0:
            G[i] = g
            G.append(h)
            m += 1
            g, h = reduce_degree(G[i], m, d)
    return G


def make_unipotent_homogeneous(F: list, points: list[list[int]]):
    n = len(F)
    x = xs(n)
    linear = [sp.expand(sp.cancel(scale(fi / T, n, 1))).subs(T, 0) for fi in F]
    if linear != x:
        raise ValueError("linear part is not the identity")
    d = max(total_degree(fi, n) for fi in F)
    G = reduce_map(F, d)
    m = len(G)
    xm = xs(m)
    q_list = []
    for p in points:
        q = [sp.Rational(v) / T ** (d - 2) for v in p]
        for i in range(n, m):
            expr = xm[i] - G[i]
            q.append(sp.expand(expr.subs({xm[k]: q[k] for k in range(i)}, simultaneous=True)))
        q_list.append(q)
    x_last = sp.Symbol(f"x{m + 1}")
    G_h = [sp.expand(gi.subs(T, x_last)) for gi in G] + [x_last]
    return G_h, q_list, d, m + 1


def main() -> int:
    started = time.time()
    x1, x2, x3 = xs(3)
    v = 1 + 2 * x1 * x2
    F = [x1 - 3 * x1 ** 2 * x2 - x1 ** 3 * x3,
         3 * v ** 2 * x1 * x3 + (9 * v ** 2 - 6 * v - 2) * x2,
         v ** 3 * x3 + (6 * v ** 2 + 2 * v) * x2 ** 2]
    F = [sp.expand(f) for f in F]
    P = [[0, 1, -8], [-1, 1, 4]]
    detF = sp.factor(sp.Matrix(F).jacobian([x1, x2, x3]).det())
    images = [[sp.expand(f.subs({x1: p[0], x2: p[1], x3: p[2]})) for f in F] for p in P]
    p1 = detF.free_symbols == set() and detF != 0 and images[0] == images[1]
    log(f"P1: det J(F) = {detF}; F(P1) = {images[0]}; F(P2) = {images[1]}; pass={p1}")

    G_h, Q, d, N = make_unipotent_homogeneous(F, P)
    x = xs(N)
    H = [sp.expand(G_h[i] - x[i]) for i in range(N)]
    degrees = sorted({sp.Poly(h, *x).total_degree() for h in H if h != 0})
    homogeneous = all(h == 0 or sp.Poly(h, *x).is_homogeneous for h in H) and degrees == [d]
    log(f"P2: dimension {N}, degree {d}, H homogeneous of degree {degrees}: {homogeneous}")

    # Points of the homogeneous map at t = 1 (de Bondt's points satisfy x + t^-1 H collisions; at t = 1 the map is G_h).
    pts = []
    for q in Q:
        qq = [sp.nsimplify(sp.expand(c.subs(T, 1))) for c in q] + [sp.Integer(1)]
        pts.append(qq)
    imgs = [[sp.expand(g.subs(dict(zip(x, p)), simultaneous=True)) for g in G_h] for p in pts]
    collision = pts[0] != pts[1] and imgs[0] == imgs[1]
    log(f"P2: points {pts[0]} and {pts[1]}; equal images: {imgs[0] == imgs[1]}; distinct: {pts[0] != pts[1]}")

    JH = sp.Matrix(H).jacobian(x)
    t0 = time.time()
    # Nilpotency of JH: in characteristic zero, tr((JH)^k) = 0 for k = 1..N is equivalent to nilpotency.
    power = sp.eye(N)
    traces = []
    nilpotent = True
    for k in range(1, N + 1):
        power = (power * JH).applyfunc(sp.expand)
        tr = sp.expand(power.trace())
        traces.append(tr == 0)
        if tr != 0:
            nilpotent = False
            break
        if power.is_zero_matrix:
            log(f"P2: (JH)^{k} = 0 exactly")
            break
    log(f"P2: JH nilpotent (traces of powers vanish): {nilpotent} in {time.time() - t0:.0f}s")
    keller = nilpotent  # det(I + s JH) = 1 identically for nilpotent JH

    # Controls: perturb one coefficient of F.
    Fbad = [F[0], F[1] + x2 ** 2, F[2]]
    det_bad = sp.factor(sp.Matrix(Fbad).jacobian([x1, x2, x3]).det())
    imgs_bad = [[sp.expand(f.subs({x1: p[0], x2: p[1], x3: p[2]})) for f in Fbad] for p in P]
    control = not (det_bad.free_symbols == set() and imgs_bad[0] == imgs_bad[1])
    log(f"P4: perturbed F (+x2^2 in F2): det constant={det_bad.free_symbols == set()}, collision={imgs_bad[0] == imgs_bad[1]}; control fires={control}")

    ok = p1 and homogeneous and collision and keller and N == 15 and d == 7 and control
    out = {"P1": {"det_JF": str(detF), "collision_images": [str(i) for i in images[0]], "pass": p1},
           "P2": {"dimension": N, "degree": d, "homogeneous": homogeneous, "nilpotent_JH": nilpotent,
                  "points": [[str(c) for c in p] for p in pts], "image": [str(c) for c in imgs[0]],
                  "collision": collision, "components": [str(g) for g in G_h]},
           "P3": {"consequence": "Mathieu false for SU(N), N >= 15 (Zwart Theorems 4.23 and 4.16)", "pass": ok},
           "P4": {"det_bad": str(det_bad), "control_fires": control},
           "pass": ok, "seconds": round(time.time() - started, 1)}
    (HERE / "artifacts").mkdir(exist_ok=True)
    (HERE / "artifacts" / "results.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    (HERE / "artifacts" / "run-log.txt").write_text("\n".join(LOG) + "\n", encoding="utf-8")
    log(f"done: pass={ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
