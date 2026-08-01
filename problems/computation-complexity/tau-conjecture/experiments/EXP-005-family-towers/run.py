"""EXP-005: exact tower yields across the family h_c = x^2 - c, c <= 200.

Deterministic, exact, seconds-scale. See hypothesis.md (committed first).
Usage: python run.py [--smoke]
"""

import argparse
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "code"))

from tclib.enum import integer_roots, padd, peval, pmul, psub  # noqa: E402

T0 = time.time()
ART = HERE / "artifacts"
X = (0, 1)


def log(msg):
    print(f"[{time.time() - T0:8.1f}s] {msg}", flush=True)


def tau_integers(max_depth):
    """Exact tau(n) for all n reached within max_depth (Markstroem model)."""
    frontier = {()}
    tau = {1: 0}
    for depth in range(1, max_depth + 1):
        new_frontier = set()
        for state in frontier:
            operands = (1,) + state
            n = len(operands)
            cand = set()
            for i in range(n):
                a = operands[i]
                for j in range(i, n):
                    cand.add(a + operands[j])
                    cand.add(a * operands[j])
            for a in operands:
                for b in operands:
                    if a - b > 0:
                        cand.add(a - b)
            for v in cand:
                if v <= 0 or v in operands:
                    continue
                new_frontier.add(tuple(sorted(state + (v,))))
                if v not in tau:
                    tau[v] = depth
        frontier = new_frontier
    return tau


def roots_by_escape_bound(f, c):
    """Exact integer roots of the tower shapes for h_c: by the escape
    lemma (monic stall theorem, Lemma 1, proved independently), any
    integer root r of a shape built from iterates of h_c = x^2 - c
    satisfies |r| <= c + 1 (an orbit starting outside [-(c+1), c+1] has
    strictly increasing absolute values, so no iterate coincidence can
    occur). Divisor-based counting is infeasible here (constant terms up
    to ~c^{2^k}); direct evaluation over the proved window is exact."""
    if not f:
        return []
    return [r for r in range(-(c + 1), c + 2) if peval(f, r) == 0]


def yields_for_c(c, kmax=4):
    """Exact integer-root yields of tower shapes for h_c = x^2 - c."""
    cc = (-c,)
    iters = [X]
    for _ in range(kmax):
        iters.append(padd(pmul(iters[-1], iters[-1]), cc))
    rows = []
    for j in range(1, kmax + 1):
        # fixed-point shape h^j(x) - x
        f = psub(iters[j], X)
        rows.append(("fix", 0, j, roots_by_escape_bound(f, c)))
        # DOS shapes h^i squared minus h^j squared, i < j
        for i in range(0, j):
            g = psub(pmul(iters[i], iters[i]), pmul(iters[j], iters[j]))
            rows.append(("dos", i, j, roots_by_escape_bound(g, c)))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    cmax = 2 if args.smoke else 200

    if args.smoke:
        rows = yields_for_c(2)
        d = {(s, i, j): r for s, i, j, r in rows}
        assert d[("dos", 0, 1)] == [-2, -1, 1, 2]
        assert d[("dos", 1, 2)] == [-2, -1, 0, 1, 2]
        assert d[("fix", 0, 1)] == [-1, 2]
        log("smoke PASS (c=2 reproduces the Chebyshev note)")
        ART.mkdir(exist_ok=True)
        (ART / "family.json").write_text(json.dumps({"smoke": True}),
                                         encoding="utf-8")
        return 0

    # Adversarial cross-check of the escape-bound root finder against the
    # divisor method where the latter is feasible (small c, shapes j <= 2).
    for c in range(1, 11):
        cc = (-c,)
        iters = [X]
        for _ in range(2):
            iters.append(padd(pmul(iters[-1], iters[-1]), cc))
        for j in (1, 2):
            for i in range(0, j):
                g = psub(pmul(iters[i], iters[i]), pmul(iters[j], iters[j]))
                if g:
                    assert set(roots_by_escape_bound(g, c)) == \
                        integer_roots(g), (c, i, j)
    log("escape-bound root finder cross-checked vs divisor method (c<=10)")

    tau = tau_integers(7)
    log(f"tau table: {len(tau)} integers (depth 7)")

    per_c = {}
    zmax_family, argmax = 0, None
    violations = []
    for c in range(1, cmax + 1):
        rows = yields_for_c(c)
        zc = max((len(r) for _, _, _, r in rows), default=0)
        best = max(rows, key=lambda t: len(t[3]))
        m_form = None
        m = 0
        while m * (m + 1) < c:
            m += 1
        if m * (m + 1) == c:
            m_form = m
        per_c[c] = {
            "z_max_shapes": zc,
            "best_shape": {"shape": best[0], "i": best[1], "j": best[2],
                           "roots": best[3]},
            "m_form": m_form,
            "tau_c": tau.get(c),
        }
        if zc > zmax_family:
            zmax_family, argmax = zc, c
        # committed predictions
        if m_form is None and zc != 0:
            violations.append((c, "nonzero yield off m(m+1)", zc))
        if m_form is not None and m_form >= 2 and zc != 4:
            violations.append((c, f"m={m_form} yield != 4", zc))
        if c == 2 and zc != 5:
            violations.append((c, "c=2 yield != 5", zc))
    log(f"family z_max = {zmax_family} at c = {argmax}; "
        f"violations: {len(violations)}")

    payload = {
        "cmax": cmax,
        "kmax": 4,
        "family_zmax": zmax_family,
        "family_argmax": argmax,
        "violations": violations,
        "per_c_nonzero": {str(c): v for c, v in per_c.items()
                          if v["z_max_shapes"] > 0},
    }
    ART.mkdir(exist_ok=True)
    (ART / "family.json").write_text(
        json.dumps(payload, indent=1, sort_keys=True), encoding="utf-8")
    log("done; artifacts/family.json written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
