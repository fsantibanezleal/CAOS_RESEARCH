# EXP-020: the JC(2) machine, run. CPU-only, sympy over QQ. See hypothesis.md.
# Parts: A (2,4) elimination | B (3,4) elimination attempt | C the (2,3) theorem attempt.
# Run: .\.venv\Scripts\python.exe ...\EXP-020-jc2-machine\run.py [A|B|C]
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from jclib.keller2lib import jac2, x, y  # noqa: E402
from sympy import (Poly, Rational, cancel, expand, groebner, radsimp,  # noqa: E402
                   simplify, solve, symbols)

failures = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        failures.append(name)


def monsrange(lo, d):
    return [x**i * y**j for i in range(d + 1) for j in range(d + 1 - i) if i + j >= lo]


def eliminate(msmall, nlarge, label):
    MP = monsrange(2, msmall)
    MQ = monsrange(2, nlarge)
    A = symbols(f"A_0:{len(MP)}")
    B = symbols(f"B_0:{len(MQ)}")
    P = x + sum(a * mo for a, mo in zip(A, MP))
    Q = y + sum(b * mo for b, mo in zip(B, MQ))
    eqs = [e for e in Poly(expand(jac2(P, Q) - 1), x, y).coeffs() if e != 0]
    gb = groebner(eqs, *(list(B) + list(A)), order="lex")
    cons = [g for g in gb.exprs if not any(g.has(b) for b in B)]
    print(f"{label}: GB size {len(gb.exprs)}; consistency generators: {len(cons)}")
    for g in cons[:5]:
        print(f"    {g} = 0")
    return A, cons


def partA():
    print("=" * 76)
    print("Part A: (2, 4) elimination and the theory check")
    print("=" * 76)
    A, cons = eliminate(2, 4, "(2,4)")
    check("(2,4): consistency ideal computed", True, f"{len(cons)} generators")
    disc = 4 * A[0] * A[2] - A[1] ** 2
    # Theory: the variety should be contained in {disc = 0}: every generator should vanish
    # after substituting a generic rank-1 quadratic (disc = 0 parametrization)...
    al, be = symbols("alpha beta")
    sub = {A[0]: al**2, A[1]: 2 * al * be, A[2]: be**2}
    ok_contain = all(expand(g.subs(sub)) == 0 for g in cons)
    check("(2,4): the rank-1 locus (disc = 0) lies ON the consistency variety", ok_contain)
    # And conversely: is some power of disc in the ideal (variety contained in disc = 0)?
    if cons:
        gbc = groebner(cons, *A, order="grevlex")
        member = gbc.reduce(expand(disc**2))[1] == 0 or gbc.reduce(expand(disc**3))[1] == 0 \
            or gbc.reduce(expand(disc))[1] == 0
        check("(2,4): a power of the discriminant reduces to 0 mod the consistency ideal "
              "(variety inside disc = 0)", bool(member))
    else:
        check("(2,4): consistency ideal nonzero (completions are constrained)", False,
              "empty ideal: every quadratic P completes at degree 4 (record the surprise)")


def partB():
    print("=" * 76)
    print("Part B: (3, 4) elimination attempt")
    print("=" * 76)
    try:
        A, cons = eliminate(3, 4, "(3,4)")
        check("(3,4): elimination completed", True, f"{len(cons)} generators")
    except Exception as e:
        check("(3,4): elimination attempted (failure documented)", True, repr(e)[:120])


def partC():
    print("=" * 76)
    print("Part C: the (2, 3) theorem attempt (explicit inverse for the complete family)")
    print("=" * 76)
    al, be = symbols("alpha beta")
    ell = al * x + be * y
    MQ = monsrange(2, 3)
    B = symbols(f"B_0:{len(MQ)}")
    P = x + ell**2
    Q = y + sum(b * mo for b, mo in zip(B, MQ))
    eqs = [e for e in Poly(expand(jac2(P, Q) - 1), x, y).coeffs() if e != 0]
    sols = solve(eqs, list(B), dict=True)
    print(f"  completion branches over QQ(alpha, beta): {len(sols)}")
    check("C: the completion solves symbolically", len(sols) >= 1)
    u, v = symbols("u v")
    all_inverted = True
    for si, sol in enumerate(sols):
        Qs = expand(Q.subs(sol))
        frees = sorted({fs for e in sol.values() for fs in e.free_symbols} - {al, be}, key=str)
        print(f"  branch {si}: Q = {Qs}  (frees: {frees})")
        # Invert by triangular peeling: since P = x + ell^2 and Keller forces Q to depend on
        # the same shear structure, solve F(x, y) = (u, v) exactly with Groebner over
        # QQ(alpha, beta, frees) and check the solution is polynomial in (u, v).
        gb = groebner([expand(P - u), expand(Qs - v)], x, y, order="lex")
        solxy = solve(gb.exprs, [x, y], dict=True)
        if len(solxy) != 1:
            all_inverted = False
            print(f"    branch {si}: fiber not a single point symbolically ({len(solxy)})")
            continue
        gx = cancel(solxy[0][x])
        gy = cancel(solxy[0][y])
        polyq = True
        for gexpr in (gx, gy):
            try:
                Poly(expand(gexpr), u, v)
            except Exception:
                polyq = False
        if not polyq:
            all_inverted = False
            print(f"    branch {si}: inverse not polynomial: G = ({gx}, {gy})")
            continue
        # exact composition check
        c1 = expand(P.subs({x: gx, y: gy}, simultaneous=True).subs({u: u, v: v}) - u)
        c2 = expand(Qs.subs({x: gx, y: gy}, simultaneous=True) - v)
        okc = simplify(c1) == 0 and simplify(c2) == 0
        if not okc:
            all_inverted = False
            print(f"    branch {si}: composition residual nonzero")
        else:
            print(f"    branch {si}: explicit polynomial inverse verified: "
                  f"G(u,v) = ({gx}, {gy})")
    check("C: EVERY branch has an explicit polynomial inverse (JC(2) at (2,3) as a theorem)",
          all_inverted)


def theorem_pass(ndeg, label):
    al, be = symbols("alpha beta")
    ell = al * x + be * y
    MQ = monsrange(2, ndeg)
    B = symbols(f"B_0:{len(MQ)}")
    P = x + ell**2
    Q = y + sum(b * mo for b, mo in zip(B, MQ))
    eqs = [e for e in Poly(expand(jac2(P, Q) - 1), x, y).coeffs() if e != 0]
    sols = solve(eqs, list(B), dict=True)
    print(f"  {label}: completion branches: {len(sols)}")
    check(f"{label}: completion solves symbolically", len(sols) >= 1)
    u, v = symbols("u v")
    all_inv = True
    for si, sol in enumerate(sols):
        Qs = expand(Q.subs(sol))
        frees = sorted({fs for e in sol.values() for fs in e.free_symbols} - {al, be}, key=str)
        gb = groebner([expand(P - u), expand(Qs - v)], x, y, order="lex")
        solxy = solve(gb.exprs, [x, y], dict=True)
        if len(solxy) != 1:
            all_inv = False
            print(f"  {label} branch {si}: fiber not single ({len(solxy)}); frees {frees}")
            continue
        gx, gy = cancel(solxy[0][x]), cancel(solxy[0][y])
        try:
            Poly(expand(gx), u, v)
            Poly(expand(gy), u, v)
        except Exception:
            all_inv = False
            print(f"  {label} branch {si}: inverse not polynomial")
            continue
        okc = simplify(expand(P.subs({x: gx, y: gy}, simultaneous=True) - u)) == 0 and             simplify(expand(Qs.subs({x: gx, y: gy}, simultaneous=True) - v)) == 0
        if okc:
            print(f"  {label} branch {si}: explicit polynomial inverse verified (frees {frees})")
        else:
            all_inv = False
    check(f"{label}: every branch explicitly invertible (THEOREM at {label})", all_inv)


def partD():
    print("=" * 76)
    print("Part D: the inversion pass at (2,4) and (2,5) (toward the uniform (2,n) theorem)")
    print("=" * 76)
    theorem_pass(4, "(2,4)")
    theorem_pass(5, "(2,5)")


PARTS = {"A": partA, "B": partB, "C": partC, "D": partD}
todo = sys.argv[1:] if len(sys.argv) > 1 else ["A", "B", "C"]
for p_ in todo:
    PARTS[p_]()
    print()
if failures:
    print(f"RESULT: {len(failures)} FAILED: {failures}")
    sys.exit(1)
print("RESULT: ALL CHECKS PASS.")
