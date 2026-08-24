"""Census of degenerate points over the WHOLE (2,2) shape space.

The draft theorem statement was withdrawn because it named the centred
pentagon as THE sharp degenerate point of the stratum and the cross point
falsified that. Restating it needs the actual set, so this searches the
full four-dimensional shape space rather than any single face.

Gauge: bodies 1 and 2 at (0, +1) and (0, -1); pair A at (+-u, v); pair B
at (+-p, q). The reduced block is the six Laura-Andoyer equations
{L13, L15, L23, L25, L35, L36} over masses (m1, m2, mA, mB): a 6 x 4
matrix. A DEGENERATE point is where its rank drops to 2, because then the
kernel is two-dimensional and the configuration is central for a
one-parameter family of mass rays.

Method: many random starts, Nelder-Mead style descent on sigma_3 in double
precision to locate basins, then dedupe, then a kernel-positivity test on
each survivor. Hits are refined afterwards in high precision.
"""
import json
import math
import random
import sys
import numpy as np

ROWS = [(0, 2), (0, 4), (1, 2), (1, 4), (2, 4), (2, 5)]
COL = [0, 1, 2, 2, 3, 3]


def matrix(x):
    u, v, p, q = x
    P = np.array([[0.0, 1.0], [0.0, -1.0], [u, v], [-u, v], [p, q], [-p, q]])
    M = np.zeros((6, 4))
    for r, (i, j) in enumerate(ROWS):
        for k in range(6):
            if k == i or k == j:
                continue
            dik = P[i] - P[k]
            djk = P[j] - P[k]
            rik = math.hypot(dik[0], dik[1])
            rjk = math.hypot(djk[0], djk[1])
            if rik < 1e-9 or rjk < 1e-9:
                return None
            d = P[j] - P[i]
            e = P[k] - P[i]
            area = d[0] * e[1] - d[1] * e[0]
            M[r, COL[k]] += (rik ** -3 - rjk ** -3) * area
    return M


def sigmas(x):
    M = matrix(x)
    if M is None:
        return None
    n = np.abs(M).max(axis=1)
    if (n < 1e-300).any():
        return None
    return np.linalg.svd(M / n[:, None], compute_uv=False)


def bad(x):
    u, v, p, q = x
    if u < 0.02 or p < 0.02:
        return True
    if abs(u) > 12 or abs(p) > 12 or abs(v) > 12 or abs(q) > 12:
        return True
    # collisions between the two pairs, and with the axis bodies
    if (u - p) ** 2 + (v - q) ** 2 < 1e-4:
        return True
    if (u + p) ** 2 + (v - q) ** 2 < 1e-4:
        return True
    for (vv,) in ((v,), (q,)):
        pass
    if u ** 2 + (v - 1) ** 2 < 1e-4 or u ** 2 + (v + 1) ** 2 < 1e-4:
        return True
    if p ** 2 + (q - 1) ** 2 < 1e-4 or p ** 2 + (q + 1) ** 2 < 1e-4:
        return True
    return False


def obj(x):
    if bad(x):
        return 1e6
    s = sigmas(x)
    if s is None:
        return 1e6
    return s[2] / s[0]


def descend(x0, rnd, iters=1500, step0=0.25, shrink=0.5, every=150):
    """Coarse random-walk descent: finds the BASIN, not the bottom."""
    x = list(x0)
    best = obj(x)
    step = step0
    for it in range(iters):
        y = [x[i] + step * (rnd.random() - 0.5) for i in range(4)]
        v = obj(y)
        if v < best:
            best, x = v, y
        if it % every == every - 1:
            step *= shrink
    return x, best


def polish(x0, step0=1e-3, floor=1e-17):
    """Deterministic pattern search: drives the basin to its bottom.

    sigma_3 vanishes LINEARLY at a rank-2 point, so a coarse descent can
    only reach sigma_3 ~ (coordinate resolution). The bottom has to be
    approached with a shrinking axis-aligned pattern, which is what
    distinguishes a true zero from a positive plateau.
    """
    x = list(x0)
    cur = obj(x)
    step = step0
    while step > floor:
        moved = False
        for i in range(4):
            for sgn in (1.0, -1.0):
                y = list(x)
                y[i] += sgn * step
                v = obj(y)
                if v < cur:
                    cur, x, moved = v, y, True
        for sa in (1.0, -1.0):
            for sb in (1.0, -1.0):
                for (i, j) in ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)):
                    y = list(x)
                    y[i] += sa * step
                    y[j] += sb * step
                    v = obj(y)
                    if v < cur:
                        cur, x, moved = v, y, True
        if not moved:
            step *= 0.35
    return x, cur


def kernel_positive(x, tol=1e-9):
    """Does the 2-dim kernel meet the positive orthant?"""
    M = matrix(x)
    n = np.abs(M).max(axis=1)
    U, S, Vt = np.linalg.svd(M / n[:, None])
    k1, k2 = Vt[2], Vt[3]
    for i in range(4001):
        th = math.pi * i / 4000
        w = math.cos(th) * k1 + math.sin(th) * k2
        if (w > tol).all() or (w < -tol).all():
            return True, (w if w[0] > 0 else -w) / np.abs(w).max()
    return False, None


CONTROLS = {
    "centred pentagon": [1.9021130325903071, -0.3819660112501051,
                         1.1755705045849463, -2.6180339887498949],
    "cross point": [0.6309181371067368, 0.0,
                    1.4509074659080731, 0.0],
}


def report(tag, x, v):
    ok, w = kernel_positive(x)
    onface = abs(x[1] - x[3]) < 1e-6
    print(f"  {tag}")
    print(f"     u={x[0]:+.12f} v={x[1]:+.12f} p={x[2]:+.12f} q={x[3]:+.12f}")
    print(f"     sigma3/sigma1={v:.3e}  positive kernel={ok}  v==q={onface}")
    if ok:
        print("     masses (m1,m2,mA,mB) = "
              + ", ".join(f"{t:.8f}" for t in w))
    return {"x": [float(t) for t in x], "ratio": float(v),
            "positive": bool(ok),
            "masses": ([float(t) for t in w] if ok else None),
            "on_face_v_eq_q": bool(onface)}


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    starts = int(sys.argv[2]) if len(sys.argv) > 2 else 4000
    print("CONTROLS: the search must recover both known points")
    print("")
    for name, x0 in CONTROLS.items():
        x, v = polish(x0)
        report(name, x, v)
    print("")

    rnd = random.Random(seed)
    cands = []
    for t in range(starts):
        x0 = [rnd.uniform(0.05, 3.0), rnd.uniform(-3.5, 3.5),
              rnd.uniform(0.05, 3.0), rnd.uniform(-3.5, 3.5)]
        x, v = descend(x0, rnd)
        if v < 1e-2:
            cands.append((v, x))
        if (t + 1) % 500 == 0:
            print(f"  {t + 1}/{starts} starts, {len(cands)} basins",
                  flush=True)
    print("")
    print(f"basins below 1e-2: {len(cands)}")

    seen, hits = [], []
    for v, x in sorted(cands):
        xp, vp = polish(x)
        if vp > 1e-11:
            continue
        if any(sum((a - b) ** 2 for a, b in zip(xp, y)) < 1e-8 for y in seen):
            continue
        seen.append(xp)
        hits.append((vp, xp))
    print(f"distinct rank-2 points found: {len(hits)}")
    print("")

    out = []
    for v, x in sorted(hits):
        out.append(report("found", x, v))
    with open(f"artifacts/degenerate-census-{seed}.json", "w", encoding="utf-8") as f:
        json.dump({"seed": seed, "starts": starts, "points": out}, f, indent=1)
    print("")
    print(f"written to artifacts/degenerate-census-{seed}.json")


if __name__ == "__main__":
    main()
