"""EXP-010: QF_BV decision of the final-pm residual. See hypothesis.md."""

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
W = 64
INPUT_POLYS = [(-1,), (1,), (0, 1)]


def log(msg):
    print(f"[{time.time() - T0:8.1f}s] {msg}", flush=True)


def checkpoint(name, payload):
    ART.mkdir(exist_ok=True)
    p = ART / "bv.json"
    data = json.loads(p.read_text("utf-8")) if p.exists() else {}
    data[name] = payload
    tmp = ART / "bv.json.tmp"
    tmp.write_text(json.dumps(data, indent=1, sort_keys=True), "utf-8")
    tmp.replace(p)


def bv(v):
    return z3.BitVecVal(v, W)


def guarded_op(s, o_is, a, b):
    """Return (result_expr_by_op, overflow_guards_by_op)."""
    add = a + b
    sub = a - b
    mul = a * b
    g_add = z3.And(z3.BVAddNoOverflow(a, b, True),
                   z3.BVAddNoUnderflow(a, b))
    g_sub = z3.And(z3.BVSubNoOverflow(a, b),
                   z3.BVSubNoUnderflow(a, b, True))
    g_mul = z3.And(z3.BVMulNoOverflow(a, b, True),
                   z3.BVMulNoUnderflow(a, b))
    return (add, sub, mul), (g_add, g_sub, g_mul)


def build_solver(ngates, nroots, final_pm, root_bound):
    s = z3.SolverFor("QF_BV")
    SW = 4
    ops = [z3.BitVec(f"op{j}", SW) for j in range(ngates)]
    Ls = [z3.BitVec(f"L{j}", SW) for j in range(ngates)]
    Rs = [z3.BitVec(f"R{j}", SW) for j in range(ngates)]
    def sv(v):
        return z3.BitVecVal(v, SW)
    for j in range(ngates):
        s.add(z3.ULE(ops[j], sv(2)))
        s.add(z3.ULE(Ls[j], sv(j + 2)))
        s.add(z3.ULE(Rs[j], sv(j + 2)))
        s.add(z3.Implies(ops[j] != sv(1), z3.ULE(Ls[j], Rs[j])))
    if final_pm:
        s.add(ops[ngates - 1] != sv(2))
        s.add(z3.Or(Ls[ngates - 1] == sv(ngates + 1),
                    Rs[ngates - 1] == sv(ngates + 1)))
    r = [z3.BitVec(f"r{i}", W) for i in range(nroots)]
    for i in range(nroots - 1):
        s.add(r[i] < r[i + 1])
    for i in range(nroots):
        s.add(r[i] >= bv(-root_bound), r[i] <= bv(root_bound))
    y = z3.BitVec("y_nonroot", W)
    s.add(y >= bv(0), y <= bv(256))
    points = r + [y]
    for i, pt in enumerate(points):
        is_root = i < nroots
        E = [bv(-1), bv(1), pt]
        for j in range(ngates):
            e = z3.BitVec(f"E{i}_{j}", W)
            for a in range(j + 3):
                for b in range(j + 3):
                    (radd, rsub, rmul), (ga, gs, gm) = \
                        guarded_op(s, None, E[a], E[b])
                    sel = z3.And(Ls[j] == z3.BitVecVal(a, 4),
                                 Rs[j] == z3.BitVecVal(b, 4))
                    s.add(z3.Implies(
                        z3.And(sel, ops[j] == z3.BitVecVal(0, 4)),
                        z3.And(ga, e == radd)))
                    s.add(z3.Implies(
                        z3.And(sel, ops[j] == z3.BitVecVal(1, 4)),
                        z3.And(gs, e == rsub)))
                    s.add(z3.Implies(
                        z3.And(sel, ops[j] == z3.BitVecVal(2, 4)),
                        z3.And(gm, e == rmul)))
            E.append(e)
        if is_root:
            s.add(E[-1] == bv(0))
        else:
            s.add(E[-1] != bv(0))
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
    return vals[-1], prog


def solve_cegar(name, ngates, nroots, final_pm, root_bound, cap_s):
    log(f"{name}: gates={ngates} roots={nroots} final_pm={final_pm} "
        f"bound={root_bound} width={W}")
    s, ops, Ls, Rs, r = build_solver(ngates, nroots, final_pm, root_bound)
    s.set("timeout", int(cap_s * 1000))
    blocked = 0
    deadline = time.time() + cap_s
    while True:
        if blocked >= 50 or time.time() > deadline:
            log(f"{name}: INCONCLUSIVE(budget) blocked={blocked}")
            checkpoint(name, {"result": "inconclusive_budget",
                              "blocked": blocked,
                              "elapsed_s": round(time.time() - T0, 1)})
            return "inconclusive", None
        res = s.check()
        if res == z3.unsat:
            log(f"{name}: UNSAT (blocked {blocked})")
            checkpoint(name, {"result": "unsat", "blocked": blocked,
                              "elapsed_s": round(time.time() - T0, 1)})
            return "unsat", None
        if res == z3.unknown:
            log(f"{name}: TIMEOUT/unknown ({s.reason_unknown()})")
            checkpoint(name, {"result": "timeout",
                              "reason": str(s.reason_unknown()),
                              "blocked": blocked,
                              "elapsed_s": round(time.time() - T0, 1)})
            return "timeout", None
        m = s.model()
        f, prog = replay(ngates, m, ops, Ls, Rs)
        roots = sorted(integer_roots(f)) if f else []
        if f and len(roots) >= nroots:
            witness = {"program": prog, "poly": list(f), "roots": roots}
            log(f"{name}: SAT, VALID witness, roots {roots}")
            checkpoint(name, {"result": "sat", "witness": witness,
                              "blocked": blocked,
                              "elapsed_s": round(time.time() - T0, 1)})
            return "sat", witness
        blocked += 1
        log(f"{name}: spurious ({blocked}); blocking")
        s.add(z3.Or([z3.Or(ops[j] != m[ops[j]].as_long(),
                           Ls[j] != m[Ls[j]].as_long(),
                           Rs[j] != m[Rs[j]].as_long())
                     for j in range(ngates)]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", default="all")
    args = ap.parse_args()
    if args.phase in ("all", "known"):
        res, _ = solve_cegar("known_answer_5roots_6gates", 6, 5, False, 8,
                             60 * 60)
        if res != "sat":
            log("KNOWN-ANSWER FAIL: encoding/engine not trusted")
            return 1
    if args.phase in ("all", "residual"):
        solve_cegar("residual_7roots_pm_8gates", 8, 7, True, 32,
                    12 * 60 * 60)
    log("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
