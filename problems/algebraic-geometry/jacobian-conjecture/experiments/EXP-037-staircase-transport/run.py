# EXP-037: the staircase transport (classwise elimination of the Keller window).
# CPU-only, sympy over QQ. Run: run.py [A|B|C|D]
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from jclib.keller2lib import jac2, x, y  # noqa: E402
from sympy import (Matrix, Poly, Rational, expand, factor, linear_eq_to_matrix,  # noqa: E402
                   linsolve, symbols, zeros)

failures = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        failures.append(name)


def build_system(P, N):
    """Window system for J(P, y + sum B_i m_i) = 1, m_i of degree 2..N."""
    MQ = [(i, d - i) for d in range(2, N + 1) for i in range(d + 1)]
    B = symbols(f"B0:{len(MQ)}")
    Q0 = y + sum(b * x**i * y**j for b, (i, j) in zip(B, MQ))
    Jm1 = Poly(expand(jac2(P, Q0) - 1), x, y)
    rows = [(mo, e) for mo, e in zip(Jm1.monoms(), Jm1.coeffs()) if e != 0]
    M = Matrix([[expand(e.diff(b)) for b in B] for _, e in rows])
    rhs = Matrix([-expand(e.subs({b: 0 for b in B})) for _, e in rows])
    return MQ, list(B), rows, M, rhs


def window_consistent(P, N):
    _, B, _, M, rhs = build_system(P, N)
    eqs = [sum(M[r, c] * B[c] for c in range(M.cols)) - rhs[r, 0]
           for r in range(M.rows)]
    return bool(linsolve(eqs, B))


def transport(P, u, v, N, label="", verbose=True):
    """Classwise elimination under w = (v, 1-u). The diagonal block is the MINIMAL
    P-class s0 (for in-scope staircases s0 = v, the x-class; components with
    y-anchored tops have lower classes and s0 < v keeps the sweep triangular).
    Returns (consistent, report)."""
    w1, w2 = v, 1 - u
    sigma = w1 + w2
    MQ, B, rows, M, rhs = build_system(P, N)
    qcls = [w1 * i + w2 * j for (i, j) in MQ]
    rcls = [w1 * mo[0] + w2 * mo[1] for (mo, _) in rows]
    pcls = sorted({w1 * i + w2 * j for (i, j) in Poly(P, x, y).monoms()})
    s0 = pcls[0]
    doff = s0 - sigma
    Rvals = sorted(set(rcls) | {qc + doff for qc in qcls})
    sol = {}          # column index -> expression affine in kappas
    kappas = []
    trans = []        # (row-class, expression) transport equations
    kcount = [0]

    def fresh():
        kcount[0] += 1
        s = symbols(f"kap{kcount[0]}")
        kappas.append(s)
        return s

    for R in Rvals:
        t0 = R - doff
        cols = [c for c in range(len(MQ)) if qcls[c] == t0]
        rws = [r for r in range(len(rows)) if rcls[r] == R]
        if not rws:
            for c in cols:
                sol[c] = fresh()
            continue
        eqs = []
        U = symbols(f"u{R}_0:{len(cols)}") if cols else []
        U = list(U) if cols else []
        for r in rws:
            e = -rhs[r, 0]
            for c in range(len(MQ)):
                if M[r, c] == 0:
                    continue
                if qcls[c] == t0:
                    e += M[r, c] * U[cols.index(c)]
                else:
                    if c not in sol:
                        raise RuntimeError(
                            f"triangularity broken: row class {R} references "
                            f"unprocessed column class {qcls[c]}")
                    e += M[r, c] * sol[c]
            eqs.append(expand(e))
        if not cols:
            for e in eqs:
                if e != 0:
                    trans.append((R, e))
            continue
        A, bvec = linear_eq_to_matrix(eqs, U)
        for lam in A.T.nullspace():
            te = expand(sum(lam[k, 0] * bvec[k, 0] for k in range(A.rows)))
            if te != 0:
                trans.append((R, te))
        _, prow = A.T.rref()
        prow = list(prow)
        if prow:
            Asub = A[prow, :]
            bsub = bvec[prow, :]
            psol, taus = Asub.gauss_jordan_solve(bsub)
            rep = {tt: fresh() for tt in taus}
            psol = psol.subs(rep)
        else:
            psol = Matrix([fresh() for _ in cols])
        for k, c in enumerate(cols):
            sol[c] = expand(psol[k, 0])
    if not trans:
        return True, {"kappas": len(kappas), "trans": 0, "firstfail": None,
                      "eqs": []}
    tes = [e for _, e in trans]
    consistent = bool(linsolve(tes, kappas)) if kappas else all(
        e == 0 for e in tes)
    firstfail = None
    for k in range(1, len(tes) + 1):
        pre = tes[:k]
        ok = bool(linsolve(pre, kappas)) if kappas else all(e == 0 for e in pre)
        if not ok:
            firstfail = trans[k - 1][0]
            break
    if verbose:
        print(f"  transport[{label}]: {len(kappas)} kernel params, "
              f"{len(tes)} transport eqs, consistent={consistent}, "
              f"first-fail row-class={firstfail}")
    return consistent, {"kappas": len(kappas), "trans": len(tes),
                        "firstfail": firstfail, "eqs": trans}


def partA():
    print("=" * 76)
    print("Part A: block triangularity of the window system under w = (v, 1-u)")
    print("=" * 76)
    a, b = Rational(2), Rational(3)
    SAMPLES = [
        ("x + a x^2 y + b x^2 (u=2,v=1)", x + a * x**2 * y + b * x**2, 2, 1),
        ("x + a x^2 y^2 + b x^2 (u=2,v=2)", x + a * x**2 * y**2 + b * x**2, 2, 2),
        ("x + a x^3 y + b x^2 (u=3,v=1)", x + a * x**3 * y + b * x**2, 3, 1),
        ("x + a x^2 y + b x^3 (u=2,v=1)", x + a * x**2 * y + b * x**3, 2, 1),
    ]
    ok_off = True
    ok_tri = True
    for (nm, P, u, v) in SAMPLES:
        w1, w2 = v, 1 - u
        sigma = w1 + w2
        MQ, B, rows, M, rhs = build_system(P, 7)
        qcls = [w1 * i + w2 * j for (i, j) in MQ]
        rcls = [w1 * mo[0] + w2 * mo[1] for (mo, _) in rows]
        pcls = sorted({w1 * i + w2 * j for (i, j) in Poly(P, x, y).monoms()})
        allowed = {s - sigma for s in pcls}
        offs = set()
        for r in range(M.rows):
            for c in range(M.cols):
                if M[r, c] != 0:
                    offs.add(rcls[r] - qcls[c])
        bad = offs - allowed
        ok_off &= not bad
        ok_tri &= min(offs) == u - 1 and all(o >= u - 1 for o in offs)
        print(f"  A {nm}: P-classes {pcls}, offsets {sorted(offs)}, "
              f"allowed {sorted(allowed)}, diag offset {u - 1}"
              + (f"  BAD {bad}" if bad else ""))
    check("A1: every nonzero entry sits at a P-class offset s - sigma (block-banded exact)",
          ok_off)
    check("A2: the diagonal offset u - 1 is minimal (block TRIANGULAR, ascending classes)",
          ok_tri)


def partB():
    print("=" * 76)
    print("Part B: transport elimination == monolithic verdict (minimal family)")
    print("=" * 76)
    ok = True
    a, b = Rational(2), Rational(3)
    CASES = [
        ("x + 2 x^2 y + 3 x^2", x + a * x**2 * y + b * x**2, 2, 1),
        ("x + 2 x^2 y + 3 x^3", x + a * x**2 * y + b * x**3, 2, 1),
        ("x + 2 x^2 y^2 + 3 x^2", x + a * x**2 * y**2 + b * x**2, 2, 2),
        ("x + 2 x^3 y + 3 x^2", x + a * x**3 * y + b * x**2, 3, 1),
        ("x + x^2 + x^2 y (EXP-035 C)", x + x**2 + x**2 * y, 2, 1),
    ]
    for (nm, P, u, v) in CASES:
        mono = window_consistent(P, 7)
        cons, rep = transport(P, u, v, 7, label=nm)
        agree = (mono == cons)
        ok &= agree and not cons
        print(f"  B {nm}: monolithic={'CONS' if mono else 'EMPTY'}, "
              f"transport={'CONS' if cons else 'EMPTY'} "
              f"{'AGREE' if agree else 'DISAGREE'}")
    # positive control: a genuine component must come out CONSISTENT
    Pc = x + (x + y) ** 2
    mono = window_consistent(expand(Pc), 6)
    cons, rep = transport(expand(Pc), 2, 1, 6, label="control x+(x+y)^2 (u,v)=(2,1)")
    ok &= mono and cons
    print(f"  B control x+(x+y)^2: monolithic={'CONS' if mono else 'EMPTY'}, "
          f"transport={'CONS' if cons else 'EMPTY'}")
    check("B: classwise transport elimination reproduces the monolithic verdict on every "
          "sample, and the positive control stays consistent", ok)


def partC():
    print("=" * 76)
    print("Part C: the transport chain over the (u, v, d) grid + localization")
    print("=" * 76)
    ok_empty = True
    table = []
    for (u, v) in ((2, 1), (2, 2), (3, 1), (3, 2)):
        for d in (2, 3):
            if d == 1:
                continue
            P = x + Rational(2) * x**u * y**v + Rational(3) * x**d
            if Poly(P, x, y).total_degree() > 6:
                N = 7
            else:
                N = 8
            cons, rep = transport(P, u, v, N, verbose=False,
                                  label=f"(u,v,d)=({u},{v},{d})")
            ok_empty &= not cons
            diag = u - 1
            table.append((u, v, d, rep["kappas"], rep["trans"],
                          rep["firstfail"], diag))
            print(f"  C (u,v,d)=({u},{v},{d}) N={N}: kernels {rep['kappas']}, "
                  f"transport eqs {rep['trans']}, "
                  f"{'EMPTY' if not cons else 'CONSISTENT (escalate!)'}, "
                  f"first-fail row-class {rep['firstfail']} (diag offset {diag})")
    check("C1: every (u, v, d) staircase sample transport system is INCONSISTENT",
          ok_empty)
    # localization MEASUREMENT (prediction 3 adjudicated in the verdict): record the
    # row-class of the first inconsistent transport equation vs the constant's class 0
    # and the second-edge interference class.
    ok_loc = True
    at_zero = 0
    for (u, v, d, nk, nt, ff, diag) in table:
        sigma = v + 1 - u
        second = v * d - sigma
        ok_loc &= ff is not None
        at_zero += 1 if ff == 0 else 0
        print(f"    localization (u,v,d)=({u},{v},{d}): first-fail {ff}, "
              f"constant class 0, second-edge offset {second}")
    check("C2: inconsistency always LOCALIZES (a first failing transport equation "
          "exists); its class is recorded for the verdict", ok_loc,
          f"{at_zero}/{len(table)} at the constant's class")


def partD():
    print("=" * 76)
    print("Part D: territory: JCB-028 residue shapes + richer staircases all EMPTY")
    print("=" * 76)
    a, b, c = Rational(2), Rational(3), Rational(5)
    ZOO = [
        ("x + a(xy)^2 + b x^2", x + a * (x * y) ** 2 + b * x**2, 8),
        ("x + a(xy)^2 + b x^2 y", x + a * (x * y) ** 2 + b * x**2 * y, 8),
        ("x + a(xy)^2 + b x^2 + c x^2 y", x + a * (x * y) ** 2 + b * x**2
         + c * x**2 * y, 8),
        ("x + a(xy)^2 + b x^3", x + a * (x * y) ** 2 + b * x**3, 8),
        ("x + a x^2 y + b x^2 + c x^4 y^2", x + a * x**2 * y + b * x**2
         + c * x**4 * y**2, 8),
        ("x + a x^2 y + b x^3 + c x^3 y^2", x + a * x**2 * y + b * x**3
         + c * x**3 * y**2, 8),
        ("x + x^2 + a x^2 y + b x^4 y^3", x + x**2 + a * x**2 * y
         + b * x**4 * y**3, 8),
    ]
    ok = True
    for (nm, P, N) in ZOO:
        cons = window_consistent(expand(P), N)
        ok &= not cons
        print(f"  D {nm} (N={N}): {'EMPTY' if not cons else 'CONSISTENT (escalate!)'}")
    check("D: all above-weight residue shapes and 3-vertex staircases have EMPTY windows",
          ok)


def partE():
    print("=" * 76)
    print("Part E: symbolic transport equations (GENERIC in a, b: fraction-field "
          "steps; sound emptiness stays with the numeric runs of B/C)")
    print("=" * 76)
    a, b = symbols("a b")
    ok = True
    for (u, v, d) in ((2, 1, 2), (2, 2, 2), (2, 1, 3)):
        P = x + a * x**u * y**v + b * x**d
        try:
            cons, rep = transport(P, u, v, 7, verbose=False,
                                  label=f"sym ({u},{v},{d})")
        except Exception as ex:  # noqa: BLE001
            print(f"  E ({u},{v},{d}): symbolic run failed: {ex}")
            ok = False
            continue
        print(f"  E (u,v,d)=({u},{v},{d}): consistent={cons}; transport eqs:")
        for (Rc, e) in rep["eqs"]:
            print(f"      class {Rc}: {factor(e)} = 0")
        ok &= not cons
    check("E: symbolic (generic) transport is inconsistent with a readable closed "
          "pattern per equation", ok)


PARTS = {"A": partA, "B": partB, "C": partC, "D": partD, "E": partE}
todo = sys.argv[1:] if len(sys.argv) > 1 else ["A", "B", "C", "D"]
for p_ in todo:
    PARTS[p_]()
    print()
if failures:
    print(f"RESULT: {len(failures)} FAILED: {failures}")
    sys.exit(1)
print("RESULT: ALL CHECKS PASS.")
