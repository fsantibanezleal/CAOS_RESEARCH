"""EXP-008: SMT decision of the final-pm residual at depth 8 (z_max(8)).

Evaluation encoding over Z (no coefficients), CEGAR against the zero
polynomial, every SAT witness replayed exactly through tclib.
Usage: python run.py [--phase known|bounded|unbounded] (default: all)
"""

import argparse
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "code"))

import z3  # noqa: E402

from tclib.enum import integer_roots, padd, pmul, psub  # noqa: E402

T0 = time.time()
ART = HERE / "artifacts"
INPUT_POLYS = [(-1,), (1,), (0, 1)]


def log(msg):
    print(f"[{time.time() - T0:8.1f}s] {msg}", flush=True)


def checkpoint(name, payload):
    ART.mkdir(exist_ok=True)
    p = ART / "sat8.json"
    data = json.loads(p.read_text("utf-8")) if p.exists() else {}
    data[name] = payload
    tmp = ART / "sat8.json.tmp"
    tmp.write_text(json.dumps(data, indent=1, sort_keys=True), "utf-8")
    tmp.replace(p)


def build_solver(ngates, nroots, final_pm, root_bound, timeout_ms,
                 value_bound=None):
    s = z3.SolverFor("QF_NIA")
    s.set("timeout", timeout_ms)
    ops = [z3.Int(f"op{j}") for j in range(ngates)]
    Ls = [z3.Int(f"L{j}") for j in range(ngates)]
    Rs = [z3.Int(f"R{j}") for j in range(ngates)]
    for j in range(ngates):
        s.add(ops[j] >= 0, ops[j] <= 2)
        s.add(Ls[j] >= 0, Ls[j] <= j + 2)
        s.add(Rs[j] >= 0, Rs[j] <= j + 2)
        # commutative symmetry-break
        s.add(z3.Implies(ops[j] != 1, Ls[j] <= Rs[j]))  # op 1 = '-'
    if final_pm:
        s.add(ops[ngates - 1] != 2)                       # +- only
        s.add(z3.Or(Ls[ngates - 1] == ngates + 1,
                    Rs[ngates - 1] == ngates + 1))        # involves prior gate
    r = [z3.Int(f"r{i}") for i in range(nroots)]
    for i in range(nroots - 1):
        s.add(r[i] < r[i + 1])
    if root_bound:
        for i in range(nroots):
            s.add(r[i] >= -root_bound, r[i] <= root_bound)
    # nroots root columns + ONE nonzero column (index nroots): f(y) != 0,
    # which excludes exactly the zero polynomial.
    y = z3.Int("y_nonroot")
    points = r + [y]
    for i, pt in enumerate(points):
        is_root = i < nroots
        E = [z3.IntVal(-1), z3.IntVal(1), pt]
        for j in range(ngates):
            e = z3.Int(f"E{i}_{j}")
            for a in range(j + 3):
                for b in range(j + 3):
                    s.add(z3.Implies(
                        z3.And(Ls[j] == a, Rs[j] == b, ops[j] == 0),
                        e == E[a] + E[b]))
                    s.add(z3.Implies(
                        z3.And(Ls[j] == a, Rs[j] == b, ops[j] == 1),
                        e == E[a] - E[b]))
                    s.add(z3.Implies(
                        z3.And(Ls[j] == a, Rs[j] == b, ops[j] == 2),
                        e == E[a] * E[b]))
            if value_bound and is_root:
                s.add(e >= -value_bound, e <= value_bound)
            E.append(e)
        if is_root:
            s.add(E[-1] == 0)
        else:
            s.add(E[-1] != 0)
    return s, ops, Ls, Rs, r


def replay(ngates, model, ops, Ls, Rs):
    vals = list(INPUT_POLYS)
    prog = []
    for j in range(ngates):
        o = model[ops[j]].as_long()
        a = model[Ls[j]].as_long()
        b = model[Rs[j]].as_long()
        fa, fb = vals[a], vals[b]
        v = (padd if o == 0 else psub if o == 1 else pmul)(fa, fb)
        vals.append(v)
        prog.append((list(fa), "+-*"[o], list(fb), list(v)))
    f = vals[-1]
    return f, prog


def solve_cegar(name, ngates, nroots, final_pm, root_bound, timeout_ms,
                value_bound=None):
    log(f"{name}: building (gates={ngates}, roots={nroots}, "
        f"final_pm={final_pm}, bound={root_bound})")
    s, ops, Ls, Rs, r = build_solver(ngates, nroots, final_pm, root_bound,
                                     timeout_ms, value_bound)
    blocked = 0
    phase_deadline = time.time() + timeout_ms / 1000.0
    while True:
        if blocked >= 50 or time.time() > phase_deadline:
            log(f"{name}: INCONCLUSIVE(budget) after {blocked} blocks")
            checkpoint(name, {"result": "inconclusive_budget",
                              "blocked": blocked,
                              "elapsed_s": round(time.time() - T0, 1)})
            return "inconclusive", None
        res = s.check()
        if res == z3.unsat:
            log(f"{name}: UNSAT (blocked {blocked} spurious)")
            checkpoint(name, {"result": "unsat", "blocked": blocked,
                              "elapsed_s": round(time.time() - T0, 1)})
            return "unsat", None
        if res == z3.unknown:
            log(f"{name}: UNKNOWN ({s.reason_unknown()})")
            checkpoint(name, {"result": "unknown",
                              "reason": str(s.reason_unknown()),
                              "blocked": blocked,
                              "elapsed_s": round(time.time() - T0, 1)})
            return "unknown", None
        m = s.model()
        f, prog = replay(ngates, m, ops, Ls, Rs)
        roots = sorted(integer_roots(f)) if f else []
        if f and len(roots) >= nroots:
            witness = {"program": prog, "poly": list(f), "roots": roots,
                       "model_roots": [m[x].as_long() for x in r]}
            log(f"{name}: SAT, VALID witness, roots {roots}")
            checkpoint(name, {"result": "sat", "witness": witness,
                              "blocked": blocked,
                              "elapsed_s": round(time.time() - T0, 1)})
            return "sat", witness
        blocked += 1
        log(f"{name}: spurious model (f zero or short); blocking "
            f"({blocked})")
        s.add(z3.Or([z3.Or(ops[j] != m[ops[j]].as_long(),
                           Ls[j] != m[Ls[j]].as_long(),
                           Rs[j] != m[Rs[j]].as_long())
                     for j in range(ngates)]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", default="all")
    args = ap.parse_args()

    if args.phase in ("all", "known"):
        res, wit = solve_cegar("known_answer_5roots_6gates", 6, 5, False,
                               8, 30 * 60 * 1000, value_bound=10**9)
        if res != "sat":
            log("KNOWN-ANSWER FAIL: encoding not trusted")
            return 1
    if args.phase in ("all", "bounded"):
        res, _ = solve_cegar("bounded_7roots_pm", 8, 7, True, 32,
                             120 * 60 * 1000)
        if res == "unknown":
            solve_cegar("doubly_bounded_7roots_pm", 8, 7, True, 32,
                        60 * 60 * 1000, value_bound=10**12)
    if args.phase in ("all", "unbounded"):
        solve_cegar("unbounded_7roots_pm", 8, 7, True, None,
                    120 * 60 * 1000)
    log("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
