# EXP-136: cascade dimension audit. CPU only; exact arithmetic (sympy over QQ); deterministic, no seeds.
# Run from the repo root:
#   .venv/Scripts/python.exe problems/algebraic-geometry/jacobian-conjecture/experiments/EXP-136-cascade-dimension-audit/run.py
#
# Part A: closure of the located implications over JC(n), DC(n), PC(n), n = 1..NMAX, with the dimension
#         indices exactly as the primary sources state them (artifacts/sources.md).
# Part B: F (EXP-001) is not affinely equivalent to a map x - h with h homogeneous: the ideal of all
#         second partial derivatives of its components has no zero (Groebner basis [1]).
# Part C: the EXP-041 input (Thompson's H on Q^24, hash-matched) is x + H with H homogeneous cubic,
#         and its published collision holds exactly.
# Part D (amendment): Long's SU(2) Mathieu counterexample, exact Haar moments for n = 1..12.
# Part E (amendment): Long's GMC(3) counterexample, exact Gaussian moments for m = 1..10.
# Writes artifacts/result.json; exits 1 if any check fails.
import hashlib
import json
import sys
from math import factorial
from pathlib import Path

from sympy import Poly, Rational, diff, expand, groebner, symbols, sympify

HERE = Path(__file__).resolve().parent
EXP041 = HERE.parent / "EXP-041-gradient-witness"
NMAX = 8
failures = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        failures.append(name)


# ---------------------------------------------------------------------------------------------
# Part A: implication closure
# ---------------------------------------------------------------------------------------------
def closure(ground):
    """Propagate truth values through the located implications until a fixed point.

    ground: {(name, n): True/False}. Returns {(name, n): True/False/None} for JC, DC, PC and
    n = 1..NMAX (JC is tabulated to 2*NMAX so that JC(2n) exists for every tabulated n).
    """
    val = {("JC", n): None for n in range(1, 2 * NMAX + 1)}
    val.update({(s, n): None for s in ("DC", "PC") for n in range(1, NMAX + 1)})
    val.update(ground)
    imps = []  # (premise, conclusion, source)
    for n in range(1, NMAX + 1):
        imps.append((("DC", n), ("JC", n), "BKK introduction: DC_n implies JC_n (well known)"))
        imps.append((("JC", 2 * n), ("DC", n), "BKK Theorem 1: JC_2n implies DC_n"))
        imps.append((("JC", 2 * n), ("PC", n), "AvdE Theorem 7: JC(2n) => PC(n)"))
        imps.append((("PC", n), ("DC", n), "AvdE Theorem 7: PC(n) => DC(n)"))
        for m in range(1, n):
            imps.append((("DC", n), ("DC", m), "BKK introduction: DC_n implies DC_m for n > m"))
    for n in range(1, 2 * NMAX + 1):
        for m in range(1, n):
            imps.append((("JC", n), ("JC", m), "BKK introduction: JC_n implies JC_m if n > m"))
    changed, contradictions = True, []
    while changed:
        changed = False
        for a, b, src in imps:
            if val[a] is True and val[b] is not True:
                if val[b] is False:
                    contradictions.append((a, b, src))
                else:
                    val[b] = True
                    changed = True
            if val[b] is False and val[a] is not False:
                if val[a] is True:
                    contradictions.append((a, b, src))
                else:
                    val[a] = False
                    changed = True
    return val, contradictions


def part_a():
    print("=" * 78)
    print("Part A: closure of the located implications (JC, Dixmier DC, Poisson PC)")
    print("=" * 78)
    # Ground facts: JC(1) is true (BKK introduction: "obviously true in the case n = 1");
    # JC(n) is false for n >= 3 (EXP-001, and dummy coordinates); JC(2) is open.
    ground = {("JC", 1): True}
    ground.update({("JC", n): False for n in range(3, 2 * NMAX + 1)})
    val, contra = closure(ground)
    check("A1: the closure is consistent (no statement forced both ways)", not contra, f"{len(contra)}")
    status = {f"{s}({n})": ("true" if v is True else "false" if v is False else "undecided")
              for (s, n), v in sorted(val.items()) if n <= NMAX}
    for s in ("JC", "DC", "PC"):
        print("  " + "  ".join(f"{s}({n})={status[f'{s}({n})']}" for n in range(1, NMAX + 1)))
    # Conditional closures: what JC(2) would decide either way.
    cond = {}
    for jc2 in (True, False):
        g = dict(ground)
        g[("JC", 2)] = jc2
        v2, c2 = closure(g)
        check(f"A2: the closure with JC(2) = {jc2} is consistent", not c2)
        cond[f"JC(2)={str(jc2).lower()}"] = {
            k: ("true" if v2[(s, n)] is True else "false" if v2[(s, n)] is False else "undecided")
            for k, (s, n) in ((f"{s}({n})", (s, n)) for s in ("DC", "PC") for n in (1, 2))}
        print(f"  if JC(2) = {jc2}: " + ", ".join(f"{k}={x}" for k, x in cond[f'JC(2)={str(jc2).lower()}'].items()))
    return {"nmax": NMAX, "status": status, "conditional_on_jc2": cond,
            "ground_facts": {"JC(1)": "true (BKK introduction)",
                             "JC(n), n >= 3": "false (EXP-001 plus dummy coordinates)",
                             "JC(2)": "open"}}


# ---------------------------------------------------------------------------------------------
# Part B: F is not affinely of homogeneous type
# ---------------------------------------------------------------------------------------------
def part_b():
    print("=" * 78)
    print("Part B: F (EXP-001) is not affinely equivalent to x - h with h homogeneous")
    print("=" * 78)
    x, y, z = symbols("x y z")
    F = [(1 + x * y) ** 3 * z + y**2 * (1 + x * y) * (4 + 3 * x * y),
         y + 3 * x * (1 + x * y) ** 2 * z + 3 * x * y**2 * (4 + 3 * x * y),
         2 * x - 3 * x**2 * y - x**3 * z]
    degs = [Poly(expand(f), x, y, z).total_degree() for f in F]
    deg = max(degs)
    check("B1: total degrees of the components", degs == [7, 6, 4], f"{degs}; deg F = {deg}")
    second = []
    for f in F:
        for a, b in ((x, x), (x, y), (x, z), (y, y), (y, z), (z, z)):
            d2 = expand(diff(f, a, b))
            if d2 != 0:
                second.append(d2)
    gb = groebner(second, x, y, z, order="grevlex")
    empty = list(gb.exprs) == [1]
    check("B2: the second-derivative ideal is the unit ideal (no base point)", empty,
          f"{len(second)} nonzero generators, basis {list(gb.exprs)[:3]}")
    # Direct certificate, independent of the Groebner routine.
    f1, f3 = F[0], F[2]
    c1 = expand(diff(f3, x, y)) == -6 * x
    c2 = expand(diff(f3, x, x).subs(x, 0)) == -6 * y
    c3 = expand(diff(f1, y, y).subs({x: 0, y: 0})) == 8
    check("B3: direct certificate d2F3/dxdy = -6x, d2F3/dx2|x=0 = -6y, d2F1/dy2|x=y=0 = 8",
          c1 and c2 and c3)
    return {"component_total_degrees": degs, "total_degree": deg,
            "second_derivative_generators": len(second),
            "groebner_basis": [str(e) for e in gb.exprs],
            "affinely_homogeneous_type": not empty}


# ---------------------------------------------------------------------------------------------
# Part C: the 24-variable cubic-homogeneous form (EXP-041 input)
# ---------------------------------------------------------------------------------------------
SHA = {"cubic_map.txt": "10f416c2bf813771cddc392469d937fa06a5a9f4aeff1ed2a99af4214b64b632",
       "collision_points.txt": "0e02c18a6cf2ca9a7d95794e71f33c4b0aa79f4cb41e3615d3dacbcfc25a10f1"}


def part_c():
    print("=" * 78)
    print("Part C: Thompson's G = x + H on Q^24 (EXP-041 input) is of homogeneous type")
    print("=" * 78)
    for name, want in SHA.items():
        raw = (EXP041 / "data" / name).read_bytes().replace(b"\r\n", b"\n")
        got = hashlib.sha256(raw).hexdigest()
        check(f"C1: sha256({name}) matches the EXP-041 record", got == want, got[:16])
    U = symbols("u1:25")
    loc = {f"u{k}": U[k - 1] for k in range(1, 25)}
    H = [None] * 24
    for line in (EXP041 / "data" / "cubic_map.txt").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("H") and "=" in line:
            nm, expr = line.split("=", 1)
            H[int(nm.strip()[1:]) - 1] = sympify(expr.strip(), locals=loc)
    check("C2: all 24 components parsed", all(h is not None for h in H))
    nmon, hom = 0, True
    for h in H:
        if h == 0:
            continue
        p = Poly(h, *U)
        nmon += len(p.monoms())
        hom &= all(sum(m) == 3 for m in p.monoms())
    check("C3: H is homogeneous cubic, so G = x + H = x - h with h = -H homogeneous", hom,
          f"{nmon} monomials")
    pts = []
    for line in (EXP041 / "data" / "collision_points.txt").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith(("P =", "Q =")):
            pts.append([Rational(t.strip()) for t in line.split("=", 1)[1].strip().strip("()").split(",")])
    P, Q = pts
    sp, sq = dict(zip(U, P)), dict(zip(U, Q))
    GP = [expand(U[k] + H[k]).subs(sp) for k in range(24)]
    GQ = [expand(U[k] + H[k]).subs(sq) for k in range(24)]
    check("C4: G(P) = G(Q) exactly with P != Q", P != Q and GP == GQ)
    return {"dimension": 24, "cubic_monomials": nmon, "homogeneous_cubic": hom,
            "collision_exact": P != Q and GP == GQ,
            "keller": "det(I + JH) = 1 by the nilpotency of JH (EXP-041, index 18)"}


# ---------------------------------------------------------------------------------------------
# Part D (amendment): Long's SU(2) example, arXiv:2607.19012, n = 1..12
# ---------------------------------------------------------------------------------------------
def part_d(nmax=12):
    print("=" * 78)
    print("Part D: Long's Mathieu counterexample on SU(2), exact Haar moments for n = 1..%d" % nmax)
    print("=" * 78)
    al, alc, be, bec = symbols("alpha alphabar beta betabar")
    # g = [[a, c], [b, d]] = [[alpha, -conj(beta)], [beta, conj(alpha)]], |alpha|^2 + |beta|^2 = 1
    a, b, c, d = al, be, -bec, alc
    F = expand((1 + c) * (a * d + b))
    G = -c

    def haar(p):
        # int alpha^i conj(alpha)^j beta^k conj(beta)^l dg = [i = j][k = l] i! k! / (i + k + 1)!
        tot = Rational(0)
        for (i, j, k, l), coef in Poly(p, al, alc, be, bec).terms():
            if i == j and k == l:
                tot += coef * Rational(factorial(i) * factorial(k), factorial(i + k + 1))
        return tot

    ok, rows, Fn = True, [], Rational(1)
    for n in range(1, nmax + 1):
        Fn = expand(Fn * F)
        m0, m1 = haar(Fn), haar(expand(Fn * G))
        want = Rational((-1) ** (n - 1), n + 1)
        ok &= m0 == 0 and m1 == want
        rows.append({"n": n, "int_F^n": str(m0), "int_F^n_G": str(m1)})
    check(f"D1: int F^n dg = 0 and int F^n G dg = (-1)^(n-1)/(n+1) for n = 1..{nmax}", ok,
          f"n = {nmax}: {rows[-1]['int_F^n_G']}")
    return {"n_checked": nmax, "all_match": ok, "moments": rows}


# ---------------------------------------------------------------------------------------------
# Part E (amendment): Long's GMC(3) example, arXiv:2607.18186 eq. (10), m = 1..10
# ---------------------------------------------------------------------------------------------
def part_e(mmax=10):
    print("=" * 78)
    print("Part E: Long's explicit GMC(3) counterexample, exact Gaussian moments for m = 1..%d" % mmax)
    print("=" * 78)
    Z, W, T = symbols("Z W T")
    P3 = expand((1 + Z) * (W - Rational(1, 2) * (2 + Z) * T**2))
    printed = W + W * Z - T**2 - Rational(3, 2) * Z * T**2 - Rational(1, 2) * Z**2 * T**2
    p = Poly(P3, Z, W, T)
    check("E1: P3 expands to the printed five-term quartic", expand(P3 - printed) == 0
          and len(p.terms()) == 5 and p.total_degree() == 4)

    def dfact(k):  # (k)!! for odd k >= -1
        out = 1
        while k > 1:
            out *= k
            k -= 2
        return out

    def gauss(q):
        # E(Z^a W^b T^t) = [a = b] a! * [t even] (t - 1)!!, Z circular standard, T real standard
        tot = Rational(0)
        for (a, b, t), coef in Poly(q, Z, W, T).terms():
            if a == b and t % 2 == 0:
                tot += coef * factorial(a) * dfact(t - 1)
        return tot

    ok, rows, Pm = True, [], Rational(1)
    for m in range(1, mmax + 1):
        Pm = expand(Pm * P3)
        e0, e1 = gauss(Pm), gauss(expand(Z * Pm))
        ok &= e0 == 0 and e1 == factorial(m)
        rows.append({"m": m, "E_P3^m": str(e0), "E_Q3_P3^m": str(e1)})
    check(f"E2: E(P3^m) = 0 and E(Q3 P3^m) = m! for m = 1..{mmax}", ok, f"m = {mmax}: {rows[-1]['E_Q3_P3^m']}")
    return {"m_checked": mmax, "all_match": ok, "moments": rows}


def main():
    res = {"experiment": "EXP-136", "part_a": part_a(), "part_b": part_b(), "part_c": part_c(),
           "part_d": part_d(), "part_e": part_e()}
    a = res["part_a"]["status"]
    res["derived_rows"] = {
        "Dixmier": {"false": [n for n in range(1, NMAX + 1) if a[f"DC({n})"] == "false"],
                    "undecided": [n for n in range(1, NMAX + 1) if a[f"DC({n})"] == "undecided"]},
        "Poisson": {"false": [n for n in range(1, NMAX + 1) if a[f"PC({n})"] == "false"],
                    "undecided": [n for n in range(1, NMAX + 1) if a[f"PC({n})"] == "undecided"]},
        "Mathieu": {
            "F_reached_by_located_proof": res["part_b"]["affinely_homogeneous_type"],
            "false_for_SU(N)": "N >= 24" if res["part_c"]["homogeneous_cubic"] and res["part_c"]["collision_exact"]
            else "not established",
            "SU(2)": "false (Long, arXiv:2607.19012; finite check n <= %d: %s)"
                     % (res["part_d"]["n_checked"], "match" if res["part_d"]["all_match"] else "MISMATCH"),
            "not_established": "SU(N), 3 <= N <= 23"},
        "GaussianMoments": {"true": [1], "false": "n >= 3 (Long, Theorem 5.1 and dummy variables; finite check "
                            "m <= %d: %s)" % (res["part_e"]["m_checked"], "match" if res["part_e"]["all_match"]
                                              else "MISMATCH"),
                            "n=2": "proof claimed (Wilson, arXiv:2607.23887, preprint; not verified here)",
                            "note": "literature facts, transcribed in artifacts/sources.md"},
        "Dixmier_rank_1_claim": "proof claimed (Zheglov, arXiv:2410.06959v5, preprint; not verified here)",
    }
    print("=" * 78)
    for k, v in res["derived_rows"].items():
        print(f"RESULT {k}: {v}")
    res["failures"] = failures
    out = HERE / "artifacts" / "result.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(res, indent=1, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(f"written {out.relative_to(HERE).as_posix()}; {len(failures)} failed check(s)")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
