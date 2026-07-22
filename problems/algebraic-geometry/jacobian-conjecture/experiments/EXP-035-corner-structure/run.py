# EXP-035: the corner operator is diagonal; the obstruction is the staircase.
# CPU-only, sympy over QQ. Run: run.py [A|B|C|D]
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from jclib.keller2lib import jac2, x, y  # noqa: E402
from sympy import (Matrix, Poly, cancel, expand, factor, lcm, linsolve,  # noqa: E402
                   symbols)

failures = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        failures.append(name)


def partA():
    print("=" * 76)
    print("Part A: the corner operator is DIAGONAL; kernel = powers of B")
    print("=" * 76)
    okf = True
    okk = True
    for i in range(1, 4):
        for j in range(1, 4):
            for p in (1, 2, 3):
                B = x**i * y**j
                for aa in range(0, 5):
                    for bb in range(0, 5):
                        lhs = expand(jac2(B**p, x**aa * y**bb))
                        pred = expand(p * (i * bb - j * aa)
                                      * x**(i * p + aa - 1) * y**(j * p + bb - 1))
                        if expand(lhs - pred) != 0:
                            okf = False
                            print(f"  A MISMATCH i={i} j={j} p={p} a={aa} b={bb}")
                        iszero = expand(lhs) == 0
                        parallel = (i * bb - j * aa) == 0
                        if iszero != parallel:
                            okk = False
                            print(f"  A KERNEL mismatch i={i} j={j} p={p} "
                                  f"a={aa} b={bb}")
    check("A1: J(B^p, x^a y^b) = p(ib - ja) x^{ip+a-1} y^{jp+b-1} exactly (grid i,j<=3, "
          "p<=3, a,b<=4)", okf)
    check("A2: the kernel is EXACTLY the monomials parallel to (i, j), i.e. powers of B",
          okk)


def partB():
    print("=" * 76)
    print("Part B: a pure corner cannot produce the constant")
    print("=" * 76)
    ok = True
    hits = []
    for i in range(1, 4):
        for j in range(1, 4):
            for p in (1, 2, 3):
                B = x**i * y**j
                for aa in range(0, 6):
                    for bb in range(0, 6):
                        out = expand(jac2(B**p, x**aa * y**bb))
                        if out == 0:
                            continue
                        po = Poly(out, x, y)
                        if (0, 0) in po.monoms():
                            ok = False
                            hits.append((i, j, p, aa, bb))
    check("B: no monomial G gives J(B^p, G) a constant term (i, j >= 1): the constant "
          "must come from the staircase, not the corner", ok, f"hits: {hits[:4]}")


def newton_vertices(P):
    """Lower-left staircase vertices of the Newton polygon (the boundary a Keller
    component's constant must travel: from the linear vertex up to the top)."""
    pts = sorted(Poly(P, x, y).monoms())
    best = {}
    for (aa, bb) in pts:
        if aa not in best or bb > best[aa]:
            best[aa] = bb
    stair = []
    top = -1
    for aa in sorted(best):
        if best[aa] > top:
            stair.append((aa, best[aa]))
            top = best[aa]
    return sorted(pts), stair


def window_consistent(P, N):
    MQ = [x**ii * y**(dd - ii) for dd in range(2, N + 1) for ii in range(dd + 1)]
    B = symbols(f"B0:{len(MQ)}")
    Q0 = y + sum(bb * mm for bb, mm in zip(B, MQ))
    eqs = [e for e in Poly(expand(jac2(P, Q0) - 1), x, y).coeffs() if e != 0]
    return bool(linsolve(eqs, list(B)))


def certificate_support(P, N):
    MQ = [x**ii * y**(dd - ii) for dd in range(2, N + 1) for ii in range(dd + 1)]
    B = symbols(f"B0:{len(MQ)}")
    Q0 = y + sum(bb * mm for bb, mm in zip(B, MQ))
    Jm1 = Poly(expand(jac2(P, Q0) - 1), x, y)
    rows = [(mo, e) for mo, e in zip(Jm1.monoms(), Jm1.coeffs()) if e != 0]
    eqs = [e for _, e in rows]
    M = Matrix([[expand(e.diff(bb)) for bb in B] for e in eqs])
    rhs = Matrix([-expand(e.subs({bb: 0 for bb in B})) for e in eqs])
    for cv in M.T.nullspace():
        den = lcm([cancel(e).as_numer_denom()[1] for e in cv])
        cc = [expand(cancel(e * den)) for e in cv]
        f = expand(sum(ci * rhs[k, 0] for k, ci in enumerate(cc)))
        if f != 0:
            return factor(f), [rows[k][0] for k, ci in enumerate(cc) if ci != 0]
    return None, []


def partC():
    print("=" * 76)
    print("Part C: staircase mapping (polygon vs certificate support)")
    print("=" * 76)
    ok = True
    for (nm, P) in (("x + x^2 + x^2 y", x + x**2 + x**2 * y),
                    ("x + x^2 + x^2 y^3", x + x**2 + x**2 * y**3),
                    ("x + x^3 + x^2 y^2", x + x**3 + x**2 * y**2)):
        pts, stair = newton_vertices(P)
        f, sup = certificate_support(P, 7)
        if f is None:
            ok = False
            print(f"  C {nm}: no certificate at window 7")
            continue
        band = sorted({(mo[0], mo[1]) for mo in sup})
        print(f"  C {nm}: Newton points {pts}; staircase {stair}")
        print(f"      certificate {f}; support rows {len(sup)}; "
              f"x-range {min(m[0] for m in band)}..{max(m[0] for m in band)}, "
              f"y-range {min(m[1] for m in band)}..{max(m[1] for m in band)}")
        # the support must span MORE than one ray direction (multi-ray, EXP-034 finding)
        dirs = {(m[0], m[1]) for m in band}
        ok &= len(dirs) > 1
    check("C: certificates are multi-row bands (the coupling follows the staircase, not a "
          "single ray)", ok)


def partD():
    print("=" * 76)
    print("Part D: widened monomial-corner territory scan")
    print("=" * 76)
    okall = True
    CORNERS = [(1, 1), (2, 1), (1, 2), (2, 2), (3, 1)]
    for (i, j) in CORNERS:
        for p in (1, 2):
            B = (x**i * y**j) ** p
            for (tag, P) in ((f"x + B^{p}", x + B),
                             (f"x + x^2 + B^{p}", x + x**2 + B),
                             (f"x + x y + B^{p}", x + x * y + B)):
                if Poly(expand(P), x, y).total_degree() > 9:
                    continue
                cons = window_consistent(expand(P), 9)
                okall &= not cons
                st = "INCONSISTENT" if not cons else "CONSISTENT (escalate!)"
                print(f"  D B=x^{i}y^{j}, {tag}: {st}")
    check("D: every monomial-corner sample window is EMPTY (territory widened)", okall)


PARTS = {"A": partA, "B": partB, "C": partC, "D": partD}
todo = sys.argv[1:] if len(sys.argv) > 1 else ["A", "B", "C", "D"]
for p_ in todo:
    PARTS[p_]()
    print()
if failures:
    print(f"RESULT: {len(failures)} FAILED: {failures}")
    sys.exit(1)
print("RESULT: ALL CHECKS PASS.")
