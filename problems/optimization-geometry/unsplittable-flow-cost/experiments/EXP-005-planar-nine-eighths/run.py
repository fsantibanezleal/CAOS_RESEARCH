"""EXP-005: independent check of the planar 9/8 family (Muffatti) and its frontier values (hypothesis.md).

Deterministic, headless, CPU only, exact rational arithmetic; no floats, no randomness, no network.

    .venv/Scripts/python.exe problems/optimization-geometry/unsplittable-flow-cost/experiments/EXP-005-planar-nine-eighths/run.py [--jobs N]

Writes artifacts/run-log.txt and artifacts/grid-top.txt. Exits nonzero on a failed prediction (P1 to P3).
"""

from __future__ import annotations

import argparse
import sys
import time
from fractions import Fraction as F
from itertools import product
from multiprocessing import Pool
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROBLEM_ROOT = HERE.parent.parent
sys.path.insert(0, str(PROBLEM_ROOT / "code"))

from ufclib import Instance  # noqa: E402
from ufclib.decide import alpha_for_routing  # noqa: E402
from ufclib.enumerate_routings import all_routings, routing_load  # noqa: E402
from ufclib.frontier import frontier_value  # noqa: E402
from ufclib.graphs import has_k4_subdivision, is_acyclic, kuratowski_planarity_by_degrees  # noqa: E402

ARTIFACTS = HERE / "artifacts"
ARTIFACTS.mkdir(exist_ok=True)
_LOG: list[str] = []
BUDGET_S = 2 * 3600


def say(line: str = "") -> None:
    print(line, flush=True)
    _LOG.append(line)


def flush() -> None:
    ARTIFACTS.mkdir(exist_ok=True)
    (ARTIFACTS / "run-log.txt").write_text("\n".join(_LOG) + "\n", encoding="utf-8")


def check(name: str, ok: bool, detail: str = "") -> None:
    say(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))
    if not ok:
        flush()
        raise SystemExit(f"prediction failed: {name} {detail}")


def family(b, r1, q, r3, d3=F(1), costs=True, name="M"):
    """Rybin's topology; demands (1, b, d3); free-path fractions (r1, q, r3); Muffatti's unit paid-path costs."""
    d1, d2 = F(1), F(b)
    c1, c2, c3 = (1 / d1, 1 / d2, 1 / F(d3)) if costs else (0, 0, 0)
    free1, free2, free3 = d1 * r1, d2 * q, F(d3) * r3
    paid1, paid2, paid3 = d1 - free1, d2 - free2, F(d3) - free3
    arcs = [
        ("s", "t1", paid1, c1), ("s", "t2", paid2, c2), ("s", "u", free1 + free2 + F(d3), 0),
        ("u", "t3", paid3, c3), ("u", "v", free1 + free2 + free3, 0), ("v", "t1", free1, 0),
        ("v", "w", free2 + free3, 0), ("w", "t2", free2, 0), ("w", "t3", free3, 0),
    ]
    return Instance.build(source="s", demands={"t1": d1, "t2": d2, "t3": F(d3)}, arcs=arcs, name=name)


def fixed_cost_min_alpha(inst):
    frac = sum((a.cost * a.x for a in inst.arcs), F(0))
    best = None
    for routing in all_routings(inst):
        load = routing_load(inst, routing)
        cost = sum((a.cost * load[a.index] for a in inst.arcs), F(0))
        if cost <= frac:
            al = alpha_for_routing(inst, load)
            best = al if best is None or al < best else best
    return frac, best


def grid_point(p):
    b, d3, r1, q, r3 = p
    inst = family(b, r1, q, r3, d3, costs=False)
    fr = frontier_value(inst)
    return fr.alpha_max, p, fr.witness_cost


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=4)
    args = ap.parse_args()
    t0 = time.time()
    say("EXP-005: the planar 9/8 family (hypothesis frozen at 50e402e9)")

    say("\nP1 and P3: M(3/4, 1/4, 1/2 + eps, 1/4, 1)")
    for eps in (F(1, 10), F(1, 100), F(1, 1000)):
        inst = family(F(3, 4), F(1, 4), F(1, 2) + eps, F(1, 4))
        inst.check_feasible()
        frac, best = fixed_cost_min_alpha(inst)
        target = F(9, 8) - F(3, 4) * eps
        say(f" eps={eps}: fractional cost {frac}, least alpha over cost-good routings {best}, target {target}")
        check(f"P1 eps={eps}: fractional cost 2 - eps", frac == 2 - eps, str(frac))
        check(f"P1 eps={eps}: least alpha equals 9/8 - 3eps/4", best == target, f"{best} vs {target}")
        check(f"P2 eps={eps}: acyclic", is_acyclic(inst))
        k4 = has_k4_subdivision(inst)
        check(f"P2 eps={eps}: K4 subdivision", k4 is not None, str(k4))
        pl = kuratowski_planarity_by_degrees(inst)
        check(f"P2 eps={eps}: planar (degree-based Kuratowski check)", pl is True, str(pl))
        fr = frontier_value(family(F(3, 4), F(1, 4), F(1, 2) + eps, F(1, 4), costs=False))
        say(f"   frontier value alpha_max = {fr.alpha_max}, witness cost {tuple(str(c) for c in fr.witness_cost)}, "
            f"ceiling {fr.ceiling}")
        check(f"P3 eps={eps}: alpha_max >= 9/8 - 3eps/4", fr.alpha_max >= target, f"{fr.alpha_max}")

    say("\nP4: grid d1 = 1, b in k/8, d3 in k/4, r1, q, r3 in k/16")
    pts = [(F(i, 8), F(j, 4), F(a, 16), F(c, 16), F(e, 16))
           for i in range(1, 9) for j in range(1, 5) for a, c, e in product(range(1, 16), repeat=3)]
    say(f" {len(pts)} points, {args.jobs} processes, budget {BUDGET_S} s")
    top, done = [], 0
    with Pool(args.jobs) as pool:
        for res in pool.imap_unordered(grid_point, pts, chunksize=64):
            done += 1
            top.append(res)
            if len(top) > 2000:
                top.sort(key=lambda r: r[0], reverse=True)
                del top[50:]
            if time.time() - t0 > BUDGET_S:
                say(f" BUDGET reached after {done} of {len(pts)} points; the grid result covers only those")
                pool.terminate()
                break
    top.sort(key=lambda r: r[0], reverse=True)
    lines = [f"{a} {a.numerator / a.denominator:.6f} b={p[0]} d3={p[1]} r1={p[2]} q={p[3]} r3={p[4]} "
             f"cost={tuple(str(c) for c in w)}" for a, p, w in top[:50]]
    (ARTIFACTS / "grid-top.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    say(f" points evaluated: {done}; largest alpha_max: {lines[0] if lines else 'none'}")
    above = [r for r in top if r[0] > F(9, 8)]
    say(f" grid points with alpha_max > 9/8 among the top 50: {len(above)}")
    say(f"\nwall time {time.time() - t0:.1f} s")
    flush()


if __name__ == "__main__":
    main()
