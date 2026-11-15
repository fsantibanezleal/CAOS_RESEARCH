# EXP-144: exact in-house check of Long's rank-two Poisson counterexample (arXiv:2608.23777v1).
# CPU only; exact rationals (sympy Rational, Fraction); one process; seed 20261114 for the random-point route.
# Run from the repo root:
#   .venv/Scripts/python.exe problems/algebraic-geometry/jacobian-conjecture/experiments/EXP-144-long-poisson-exact-check/run.py
# Predictions P1..P5 and controls C1, C2 as frozen in hypothesis.md. Writes artifacts/{results.json,run-log.txt,polynomials.txt}.
# Exits 1 if any prediction or control fails, 2 if the source PDF is missing or its hash differs.
import hashlib
import json
import random
import sys
import time
from fractions import Fraction
from pathlib import Path

from sympy import Matrix, Poly, Rational, expand, factor_list, groebner, solve, diff

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import exp144_long as L  # noqa: E402

PDF = Path("E:/_Datos/caos-research/jacobian-conjecture/sources/jcb102/2608.23777.pdf")
PDF_SHA = "5dd5861194bfea9130cddc10919510b060dab663f3a00222e57014125db5051a"
ART = HERE / "artifacts"
ART.mkdir(exist_ok=True)
LOG = []
failures = []
results = {}
T0 = time.time()


def log(s):
    print(s)
    LOG.append(s)


def check(name, ok, detail=""):
    log(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        failures.append(name)


def flush(code):
    results["elapsed_seconds"] = round(time.time() - T0, 2)
    results["failures"] = failures
    (ART / "results.json").write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
    (ART / "run-log.txt").write_text("\n".join(LOG) + "\n", encoding="utf-8")
    sys.exit(code)


# ---- source pin ---------------------------------------------------------------------------------
if not PDF.exists():
    log(f"MISSING source PDF {PDF}")
    flush(2)
sha = hashlib.sha256(PDF.read_bytes()).hexdigest()
results["pdf_sha256"] = sha
if sha != PDF_SHA:
    log(f"PDF hash differs: {sha} != {PDF_SHA}")
    flush(2)
log(f"source PDF hash matches {sha}")

x, q, p, z = L.GENS
F = (L.R, L.T, L.D, L.S)

# ---- polynomials.txt ----------------------------------------------------------------------------
body = "\n".join(f"{n} = {e}" for n, e in zip("RTDS", F)) + "\n"
(ART / "polynomials.txt").write_text(
    body + f"# sha256 of the lines above: {hashlib.sha256(body.encode()).hexdigest()}\n", encoding="utf-8")

# ---- P1 -----------------------------------------------------------------------------------------
log("P1 transcription")
sz = L.sizes()
results["P1_sizes_measured"] = {k: list(v) for k, v in sz.items()}
results["P1_sizes_printed"] = {k: list(v) for k, v in L.SIZE_TABLE.items()}
for k, v in L.SIZE_TABLE.items():
    check(f"P1 size {k}", sz[k] == v, f"measured terms,degree={sz[k]} printed={v}")
check("P1 R = x(2 - 3xq)", expand(L.R - x * (2 - 3 * x * q)) == 0)

# ---- P2 -----------------------------------------------------------------------------------------
log("P2 Poisson endomorphism (bracket convention: eq. (8), page 3: {f,g} = f_p g_x - f_x g_p + f_z g_q - f_q g_z)")
t = time.time()
ok, bad = L.poisson_symbolic(*F)
check("P2 symbolic bracket matrix of (R,T,D,S) equals that of (x,q,p,z)", ok, f"mismatches={bad}")
M = L.bracket_matrix(F)
results["P2_bracket_matrix_RTDS"] = [[str(e) for e in r] for r in M]
named = {"{D,R}": L.bracket(L.D, L.R), "{S,T}": L.bracket(L.S, L.T), "{R,S}": L.bracket(L.R, L.S),
         "{R,T}": L.bracket(L.R, L.T), "{D,S}": L.bracket(L.D, L.S), "{D,T}": L.bracket(L.D, L.T)}
results["P2_named_brackets"] = {k: str(v) for k, v in named.items()}
check("P2 {D,R}=1 and {S,T}=1", named["{D,R}"] == 1 and named["{S,T}"] == 1)
check("P2 the four mixed brackets vanish", all(named[k] == 0 for k in ("{R,S}", "{R,T}", "{D,S}", "{D,T}")))
results["P2_symbolic_seconds"] = round(time.time() - t, 2)


# second route: Fractions, no sympy simplification
def to_terms(e):
    return [(m, Fraction(int(c.p), int(c.q))) for m, c in Poly(e, *L.GENS).terms()]


def ev(terms, pt):
    s = Fraction(0)
    for m, c in terms:
        v = c
        for xi, k in zip(pt, m):
            v *= xi ** k
        s += v
    return s


def dterms(terms, i):
    out = []
    for m, c in terms:
        if m[i]:
            mm = list(m)
            mm[i] -= 1
            out.append((tuple(mm), c * m[i]))
    return out


def det4(A):
    A = [row[:] for row in A]
    n, d = 4, Fraction(1)
    for c in range(n):
        piv = next((r for r in range(c, n) if A[r][c] != 0), None)
        if piv is None:
            return Fraction(0)
        if piv != c:
            A[c], A[piv] = A[piv], A[c]
            d = -d
        d *= A[c][c]
        for r in range(c + 1, n):
            f = A[r][c] / A[c][c]
            for k in range(c, n):
                A[r][k] -= f * A[c][k]
    return d


# Omega_0^{-1} = -Omega_0 (page 3), order (x,q,p,z): the matrix of generator brackets
PI = [[Fraction(v) for v in r] for r in ([0, 0, -1, 0], [0, 0, 0, -1], [1, 0, 0, 0], [0, 1, 0, 0])]
for i in range(4):
    for j in range(4):
        assert L.bracket(L.GENS[i], L.GENS[j]) == int(PI[i][j]), "PI mismatch with bracket()"


def random_route(Fpolys, n=50, seed=20261114):
    terms = [to_terms(e) for e in Fpolys]
    d = [[dterms(tm, c) for c in range(4)] for tm in terms]
    rng = random.Random(seed)
    nonzero, dets = 0, set()
    for _ in range(n):
        pt = [Fraction(rng.randint(-9, 9), rng.randint(1, 9)) for _ in range(4)]
        J = [[ev(d[r][c], pt) for c in range(4)] for r in range(4)]
        JPJT = [[sum(J[i][k] * PI[k][m] * J[j][m] for k in range(4) for m in range(4)) for j in range(4)]
                for i in range(4)]
        nonzero += sum(1 for i in range(4) for j in range(4) if JPJT[i][j] - PI[i][j] != 0)
        dets.add(det4(J))
    return nonzero, dets


bad_entries, dets = random_route(F)
results["P2_random_route"] = {"points": 50, "seed": 20261114,
                              "nonzero_entries_of_JF_PI_JFT_minus_PI": bad_entries,
                              "distinct_detJF_values": [str(v) for v in dets]}
check("P2 random-point route: JF PI JF^T - PI = 0 at 50 rational points", bad_entries == 0,
      f"nonzero entries={bad_entries}")

# ---- P3 -----------------------------------------------------------------------------------------
log("P3 volume")
t = time.time()
JF = Matrix(4, 4, lambda i, j: diff(F[i], L.GENS[j]))
det = expand(JF.det(method="berkowitz"))
results["P3_detJF_symbolic"] = str(det)
results["P3_seconds"] = round(time.time() - t, 2)
check("P3 det JF = 1 identically (symbolic)", det == 1, f"det={det}")
check("P3 det JF = 1 at the 50 random points (Fractions)", dets == {Fraction(1)}, f"values={dets}")

# ---- P4 -----------------------------------------------------------------------------------------
log("P4 fiber over (0, 1/8, 0, 0)")
KILL = 45 * 60
t = time.time()
G = groebner([L.R, L.T - Rational(1, 8), L.D, L.S], x, q, p, z, order="lex")
gb_s = time.time() - t
results["P4_groebner_seconds"] = round(gb_s, 2)
results["P4_kill_criterion_triggered"] = gb_s > KILL
check("P4 Groebner basis finished inside the 45 minute kill window", gb_s <= KILL, f"{gb_s:.2f}s")
results["P4_lex_basis"] = [str(g) for g in G.exprs]
check("P4 ideal zero-dimensional", G.is_zero_dimensional)
lms = [Poly(g, x, q, p, z).monoms(order="lex")[0] for g in G.exprs]
results["P4_leading_monomials"] = [list(m) for m in lms]
rng6 = range(8)
std = [(a, b, c, d) for a in rng6 for b in rng6 for c in rng6 for d in rng6
       if not any(all((a, b, c, d)[i] >= lm[i] for i in range(4)) for lm in lms)]
results["P4_quotient_dimension"] = len(std)
sols = solve(list(G.exprs), [x, q, p, z], dict=True)
sol_pts = sorted(tuple(s[v] for v in (x, q, p, z)) for s in sols)
printed = sorted([(Rational(0), Rational(0), Rational(1, 24), -Rational(1, 8)),
                  (Rational(1), Rational(2, 3), Rational(247, 96), -Rational(89, 64)),
                  (Rational(-1), -Rational(2, 3), Rational(247, 96), -Rational(89, 64))])
results["P4_solutions"] = [[str(c) for c in s] for s in sol_pts]
results["P4_printed_points_eq7"] = [[str(c) for c in s] for s in printed]
check("P4 quotient dimension equals the number of distinct solutions (ideal is radical)",
      len(std) == len(sol_pts) == 3, f"dim={len(std)} solutions={len(sol_pts)}")
check("P4 solution set equals the three printed points of (7)", sol_pts == printed)
memb = []
for s in printed:
    pt = dict(zip((x, q, p, z), s))
    vals = [e.subs(pt) for e in (L.R, L.T - Rational(1, 8), L.D, L.S)]
    memb.append([str(v) for v in vals])
    check(f"P4 printed point {tuple(map(str, s))} satisfies R=0, T=1/8, D=0, S=0", all(v == 0 for v in vals))
results["P4_membership_values"] = memb
results["P4_fiber_points_count"] = len(sol_pts)

# ---- P5 -----------------------------------------------------------------------------------------
log("P5 not an automorphism")
fl = factor_list(L.R)
results["P5_factor_list_R"] = str(fl)
check("P5 R is reducible over Q (>= 2 non-constant irreducible factors)", len(fl[1]) >= 2, str(fl))
check("P5 fiber has 3 > 1 points, so the map is not injective (independent of the factorization)",
      len(sol_pts) == 3)

# ---- controls -----------------------------------------------------------------------------------
log("Controls")
c1_ok, c1_bad = L.poisson_symbolic(L.R, L.T, L.D0, L.S)
c1_DR = expand(L.bracket(L.D0, L.R))
c1_DS, c1_DT = expand(L.bracket(L.D0, L.S)), expand(L.bracket(L.D0, L.T))
results["C1"] = {"{D0,R}": str(c1_DR), "{D0,S}": str(c1_DS)[:300], "{D0,T}": str(c1_DT)[:300], "checker_ok": c1_ok,
                 "failing_entries": [[i, j] for i, j, v in c1_bad]}
check("C1 {D0,R} = 1 (the paper's (44))", c1_DR == 1)
check("C1 at least one of {D0,S}, {D0,T} is nonzero", c1_DS != 0 or c1_DT != 0,
      f"{{D0,S}}={str(c1_DS)[:60]}  {{D0,T}}={str(c1_DT)[:60]}")
check("C1 the P2 checker reports failure for D0", c1_ok is False)
rb, _ = random_route((L.R, L.T, L.D0, L.S), n=5)
results["C1"]["random_route_nonzero_entries_5_points"] = rb
check("C1 the random-point route also detects D0", rb > 0, f"nonzero entries={rb}")

c2_ok, c2_bad = L.poisson_symbolic(L.R, L.T, L.D_C2, L.S)
results["C2"] = {"checker_ok": c2_ok, "failing_entries": [[i, j] for i, j, v in c2_bad]}
check("C2 changing 125 to 126 in H makes P2 fail", c2_ok is False, f"failing entries={len(c2_bad)}")
rb2, _ = random_route((L.R, L.T, L.D_C2, L.S), n=5)
results["C2"]["random_route_nonzero_entries_5_points"] = rb2
check("C2 the random-point route also detects the changed H", rb2 > 0, f"nonzero entries={rb2}")

log(f"elapsed {time.time() - T0:.1f}s; failures: {failures or 'none'}")
log("RESULT: " + ("PASS" if not failures else "FAIL"))
flush(0 if not failures else 1)
