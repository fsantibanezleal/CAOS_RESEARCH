"""EXP-146 gates G0 to G4 (hypothesis.md). G2 (real system) and G5 run inside chaincert.chain_node."""
import hashlib
import json
import os
import random
import subprocess
import sys
from pathlib import Path

import numpy as np
from flint import fmpz_mpoly_ctx

import chaincert as cc
import singular_eval as se

HERE = Path(__file__).resolve().parent
DATA = Path("E:/_Datos/caos-research/jacobian-conjecture")
EXP141 = DATA / "exp141-main" / "eqs.json"
BRANCH = {"plus": DATA / "exp142-143-branch-plus" / "eqs.json", "minus": DATA / "exp142-143-branch-minus" / "eqs.json"}
SHA = {"plus": "bd227b531c813586f60b1792b90ef7595d19d226b7ab2d380b3125250849424a",
       "minus": "0a3a390581c4f44c06907a61022069f7d704283e3b1def8947bb44cafaae76e9"}
BRANCHES_PY = HERE.parent / "EXP-142-case1-branch-certificates" / "branches.py"
P1, R1 = 536870909, 505390653
ORDER = ["q5", "q3", "q4", "q2", "q0"]
TEMP_DEFAULT = "D:/_Temp/jc-exp146-2026-11-15"


def temp_root():
    """Scratch folder (the temp root's role): EXP146_TEMP overrides the default."""
    return Path(os.environ.get("EXP146_TEMP", TEMP_DEFAULT))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


# ------------------------------------------------------------------------------------------------ G0, G1

def g0_inputs(workdir):
    """Rerun EXP-142 branches.py on EXP-141's eqs.json; both outputs must equal the data-root branch files."""
    if not EXP141.exists() or not all(p.exists() for p in BRANCH.values()):
        return {"pass": False, "reason": "a data-root input is missing"}
    out = Path(workdir) / "g0"
    out.mkdir(parents=True, exist_ok=True)
    r = subprocess.run([sys.executable, str(BRANCHES_PY), "--src", str(EXP141), "--out", str(out)],
                       capture_output=True, text=True)
    res = {"pass": r.returncode == 0, "branches_py_stdout": r.stdout.strip().splitlines()[-3:]}
    for tag in ("plus", "minus"):
        f = out / f"branch_{tag}" / "eqs.json"
        res[f"sha_rerun_{tag}"] = sha(f) if f.exists() else None
        res[f"sha_dataroot_{tag}"] = sha(BRANCH[tag])
        res[f"sha_expected_{tag}"] = SHA[tag]
        res["pass"] = res["pass"] and res[f"sha_rerun_{tag}"] == SHA[tag] == res[f"sha_dataroot_{tag}"]
    return res


def check_branch_inputs(d, order):
    """Strict reading of one branch file (review F10): the variable set equals `order`, every coordinate vector has 5
    entries that are exact ints (a bool or float is refused), no monomial repeats within an equation."""
    problems = []
    names = d.get("names", [])
    if set(names) != set(order) or len(names) != len(set(names)):
        problems.append(f"variable names {names} differ from the elimination variables {order}")
    eqs, frm = d.get("eqs", []), d.get("from", [])
    if len(eqs) != len(frm):
        problems.append("from and eqs differ in length")
    coefficients = 0
    for f, eq in zip(frm, eqs):
        seen = set()
        for m, cs in eq:
            key = tuple(m)
            if len(key) != len(names):
                problems.append(f"E{f}: exponent vector {key} has {len(key)} entries")
            if key in seen:
                problems.append(f"E{f}: repeated monomial {key}")
            seen.add(key)
            if len(cs) != 5:
                problems.append(f"E{f}: coordinate vector has {len(cs)} entries")
            for c in cs:
                coefficients += 1
                if type(c) is not int:
                    problems.append(f"E{f}: coordinate {c!r} is not an exact int")
    return {"equations": len(eqs), "coefficients": coefficients, "problems": problems[:10],
            "pass": not problems and len(eqs) > 0}


def branch_inputs(d, ring):
    """(terms, inputs) of a branch file for NodeRing `ring`: terms {id: [(exponents over ring.order, vector)]} and
    inputs [(id, exact polynomial)]. Refuses a file that check_branch_inputs rejects (extra or missing variable)."""
    chk = check_branch_inputs(d, ring.order)
    if not chk["pass"]:
        raise ValueError(f"branch file refused: {chk['problems']}")
    terms, ins = {}, []
    for frm, eq in zip(d["from"], d["eqs"]):
        mid = f"E{frm}"
        tl = [([m[d["names"].index(v)] for v in ring.order], cs) for m, cs in eq]
        terms[mid] = tl
        ins.append((mid, ring.from_vectors(tl)))
    return terms, ins


def g1_ring_maps(prime2):
    res = {"p1": P1, "r1": R1, "p2": prime2.p, "r2": prime2.r}
    ok = True
    for p, r in ((P1, R1), (prime2.p, prime2.r)):
        ok = ok and sum(c * pow(r, i, p) for i, c in enumerate(cc.P_COEFFS)) % p == 0
    res["inputs"] = {tag: check_branch_inputs(json.loads(path.read_text()), ORDER) for tag, path in BRANCH.items()}
    ints = all(v["pass"] for v in res["inputs"].values())
    res["inputs_integer"] = ints
    res["pass"] = bool(ok and ints and P1 < 2**29 and prime2.p < 2**29)
    return res


def second_prime():
    """p2: the largest prime below p1 at which P has a root; r2: its smallest root."""
    from flint import nmod_poly
    import sympy
    p = P1
    while True:
        p = sympy.prevprime(p)
        rts = sorted(int(r) for r, _ in nmod_poly(list(cc.P_COEFFS), p).roots())
        if rts:
            return cc.Prime(p, rts[0])


# ------------------------------------------------------------------------------------------------ exact formal resultant

def formal_resultant_exact(mat_entries_f, mat_entries_g, ctx, reduce=None):
    """Determinant of the formal Sylvester matrix. mat_entries_f: coefficients f_0..f_m (exact polys or 0),
    mat_entries_g: g_0..g_n. Subset DP over columns; exact."""
    m, n = len(mat_entries_f) - 1, len(mat_entries_g) - 1
    N = m + n
    zero = ctx.from_dict({})
    rows = []
    for i in range(n):
        row = [zero] * N
        for c in range(m + 1):
            row[i + (m - c)] = mat_entries_f[c]
        rows.append(row)
    for i in range(m):
        row = [zero] * N
        for c in range(n + 1):
            row[i + (n - c)] = mat_entries_g[c]
        rows.append(row)
    dp = {0: ctx.from_dict({(0,) * ctx.nvars(): 1})}
    for i in range(N):
        nd = {}
        for mask, val in dp.items():
            if val == 0:
                continue
            for j in range(N):
                if mask >> j & 1 or rows[i][j] == 0:
                    continue
                sign = -1 if bin(mask >> (j + 1)).count("1") % 2 else 1
                t = val * rows[i][j]
                if reduce:
                    t = reduce(t)
                nd[mask | 1 << j] = nd.get(mask | 1 << j, zero) + (t if sign == 1 else -t)
        dp = nd
    return dp.get((1 << N) - 1, zero)


# ------------------------------------------------------------------------------------------------ G2 random

def coeffs_in(ctx, poly, deg, xi):
    """Exact coefficients of poly in the variable of index xi, as polynomials with that exponent set to 0."""
    out = [ctx.from_dict({}) for _ in range(deg + 1)]
    for m, c in poly.to_dict().items():
        if m[xi] > deg:
            raise cc.BoundViolation("polynomial degree above its formal degree")
        mm = list(m)
        mm[xi] = 0
        out[m[xi]] = out[m[xi]] + ctx.from_dict({tuple(mm): int(c)})
    return out


def _rand_poly(rng, ctx, nv, maxdeg, nterms, xdeg):
    d = {}
    for _ in range(nterms):
        e = [rng.randint(0, xdeg)] + [rng.randint(0, maxdeg) for _ in range(nv - 1)]
        while sum(e) > maxdeg + xdeg:
            e[rng.randint(1, nv - 1)] = 0
        c = rng.choice([-3, -2, -1, 1, 2, 3, 5])
        d[tuple(e)] = d.get(tuple(e), 0) + c
    return ctx.from_dict({k: v for k, v in d.items() if v})


def g2_random(ncases, seed=20261115, K=cc.KMAX):
    """Random sparse pairs over Z: bound >= exact formal resultant at every weight, proven-zero coefficients zero,
    the order lower bound is below the true order. Planted: top-coefficient cancellation (loose supports), zero
    top coefficients, monomial factors, a negative-weight variable."""
    rng = random.Random(seed)
    stats = {"cases": 0, "resultant_zero": 0, "dead_bound": 0, "weights_checked": 0, "violations": 0,
             "proven_zero_checked": 0, "proven_zero_violations": 0, "planted_cancel": 0, "planted_monomial": 0,
             "split_cases": 0, "low_tight": 0, "formal_degree_above_actual": 0, "weight_checked_pairs": 0}
    for case in range(ncases):
        nv = rng.randint(2, 4)
        names = ["x"] + ["a", "b", "c"][:nv - 1]
        ctx = fmpz_mpoly_ctx.get(names, "lex")
        split = rng.randint(1, nv - 1) if rng.random() < 0.6 else None
        xsplit = split is None and rng.random() < 0.4   # x itself as the split variable: proven-zero coefficients
        if xsplit:
            split = 0
        stats["split_cases"] += split is not None
        stats["x_split_cases"] = stats.get("x_split_cases", 0) + xsplit
        dx = rng.randint(1, 3)

        def make():
            f = _rand_poly(rng, ctx, nv, rng.randint(2, 6), rng.randint(2, 7), dx)
            loose = [f]
            mono = 0
            if rng.random() < 0.5:   # planted cancellation: loose support above the exact polynomial
                top = max((m[0] for m in f.monoms()), default=0)
                T = ctx.from_dict({m: int(c) for m, c in f.to_dict().items() if m[0] == top})
                extra = _rand_poly(rng, ctx, nv, 3, 3, max(top - 1, 0))
                f2 = f - T + extra
                loose = [f, T, extra]
                f = f2
                stats["planted_cancel"] += 1
            if split is not None and rng.random() < 0.5:
                k = rng.randint(1, 2)
                gens = ctx.gens()
                f = f * gens[split] ** k
                loose = [t * gens[split] ** k for t in loose]
                mono = k
                stats["planted_monomial"] += 1
            return f, loose, mono

        f, lf, _ = make()
        g, lg, _ = make()
        if f == 0 or g == 0:
            continue
        stats["cases"] += 1
        sup = lambda polys: sorted({tuple(m) for q in polys for m in q.monoms()})
        Bf = cc.exact_bound(sup(lf), nv, split, K)
        Bg = cc.exact_bound(sup(lg), nv, split, K)
        if Bf.deg(0) == 0 or Bg.deg(0) == 0:
            stats["cases"] -= 1
            continue
        mf, zf = cc.formal_degree(Bf, 0, split, K)
        ng, zg = cc.formal_degree(Bg, 0, split, K)
        if ng < 1 or mf < 1:
            stats["cases"] -= 1
            continue
        if mf > max(m[0] for m in f.monoms()):
            stats["formal_degree_above_actual"] += 1
        # exact coefficients in x
        cf, cg = coeffs_in(ctx, f, mf, 0), coeffs_in(ctx, g, ng, 0)
        for c in range(mf + 1):
            if zf[c]:
                stats["proven_zero_checked"] += 1
                if cf[c] != 0:
                    stats["proven_zero_violations"] += 1
        for c in range(ng + 1):
            if zg[c]:
                stats["proven_zero_checked"] += 1
                if cg[c] != 0:
                    stats["proven_zero_violations"] += 1
        h = formal_resultant_exact(cf, cg, ctx)
        Bh = cc.res_bound(Bf, mf, zf, Bg, ng, zg, 0, split, nv, K)
        if h == 0:
            stats["resultant_zero"] += 1
            continue
        if Bh is None:
            stats["dead_bound"] += 1
            stats["violations"] += 1   # the bound claims zero, the resultant is not
            continue
        stats["weight_checked_pairs"] += 1
        hs = sorted({tuple(m) for m in h.monoms()})
        A = np.array(hs, dtype=np.int64)
        for key in cc.weight_keys(Bh.vs, split, K):
            w = np.zeros(nv, dtype=np.int64)
            for i, c in zip(Bh.vs, key):
                w[i] = c
            exact_max = int((A @ w).max())
            stats["weights_checked"] += 1
            if Bh.tab[key] < exact_max:
                stats["violations"] += 1
        if split is not None and split in Bh.vs:
            true_order = min(m[split] for m in h.monoms())
            if Bh.low(split) > true_order:
                stats["violations"] += 1
            if Bh.low(split) == true_order:
                stats["low_tight"] += 1
    stats["pass"] = stats["violations"] == 0 and stats["proven_zero_violations"] == 0 and stats["cases"] > 0
    return stats


def g2_composition(ncases, seed=20261118, K=cc.KMAX, max_size=12):
    """Composed bounds (review F4): exact f, g in (x, a, b, [c]) and k in (a, b, [c]); B1 = res_bound of (f, g) in x is
    propagated (formal degree and zero proofs come from B1, never from the exact h1), B2 = res_bound(B1, Bk) in a, and
    B2 is checked against the exact two-level resultant Res_a(h1, k) (formal Sylvester over the formal degrees) at every
    weight. The split variable is drawn from {a, b, c, none}; the order lower bound of the split variable is checked
    against the true order; proven-zero coefficients of h1 are checked to be zero. A mutant (B2 lowered by 1) must fail."""
    rng = random.Random(seed)
    st = {"composition_cases": 0, "composition_zero_resultant": 0, "composition_skipped": 0, "composition_weights": 0,
          "composition_violations": 0, "composition_mutant_violations": 0, "composition_proven_zero_checked": 0,
          "composition_proven_zero_violations": 0, "composition_split_cases": 0, "composition_order_checked": 0}
    for _ in range(ncases):
        nv = rng.randint(3, 4)
        ctx = fmpz_mpoly_ctx.get(["x", "a", "b", "c"][:nv], "lex")
        split = rng.choice([None] + list(range(1, nv)))
        gens = ctx.gens()

        def make(xdeg):
            f = _rand_poly(rng, ctx, nv, rng.randint(2, 3), rng.randint(2, 4), xdeg)
            if split is not None and rng.random() < 0.4:
                f = f * gens[split] ** rng.randint(1, 2)
            return f
        f, g, k = make(2), make(2), make(0)
        if f == 0 or g == 0 or k == 0:
            st["composition_skipped"] += 1
            continue
        sup = lambda q: sorted({tuple(m) for m in q.monoms()})
        Bf, Bg, Bk = (cc.exact_bound(sup(q), nv, split, K) for q in (f, g, k))
        mf, zf = cc.formal_degree(Bf, 0, split, K)
        ng, zg = cc.formal_degree(Bg, 0, split, K)
        nk, zk = cc.formal_degree(Bk, 1, split, K)
        if mf < 1 or ng < 1 or nk < 1 or Bf.deg(0) == 0 or Bg.deg(0) == 0:
            st["composition_skipped"] += 1
            continue
        h1 = formal_resultant_exact(coeffs_in(ctx, f, mf, 0), coeffs_in(ctx, g, ng, 0), ctx)
        if h1 == 0:
            st["composition_zero_resultant"] += 1
            continue
        B1 = cc.res_bound(Bf, mf, zf, Bg, ng, zg, 0, split, nv, K)
        if B1 is None:
            st["composition_violations"] += 1   # B1 says h1 = 0, h1 is not
            continue
        m1, z1 = cc.formal_degree(B1, 1, split, K)
        if m1 < 1 or m1 + nk > max_size:
            st["composition_skipped"] += 1
            continue
        try:
            c1 = coeffs_in(ctx, h1, m1, 1)
        except cc.BoundViolation:
            st["composition_violations"] += 1   # h1 has a-degree above the formal degree read from B1
            continue
        for c in range(m1 + 1):
            if z1[c]:
                st["composition_proven_zero_checked"] += 1
                if c1[c] != 0:
                    st["composition_proven_zero_violations"] += 1
        h2 = formal_resultant_exact(c1, coeffs_in(ctx, k, nk, 1), ctx)
        B2 = cc.res_bound(B1, m1, z1, Bk, nk, zk, 1, split, nv, K)
        if h2 == 0:
            st["composition_zero_resultant"] += 1
            continue
        if B2 is None:
            st["composition_violations"] += 1
            continue
        st["composition_cases"] += 1
        st["composition_split_cases"] += split is not None
        A = np.array(sorted({tuple(m) for m in h2.monoms()}), dtype=np.int64)
        for key in cc.weight_keys(B2.vs, split, K):
            w = np.zeros(nv, dtype=np.int64)
            for i, c in zip(B2.vs, key):
                w[i] = c
            exact_max = int((A @ w).max())
            st["composition_weights"] += 1
            if B2.tab[key] < exact_max:
                st["composition_violations"] += 1
            if B2.tab[key] - 1 < exact_max:       # the mutant: every entry lowered by 1
                st["composition_mutant_violations"] += 1
        if split is not None and split in B2.vs:
            st["composition_order_checked"] += 1
            if B2.low(split) > min(m[split] for m in h2.monoms()):
                st["composition_violations"] += 1
    st["pass"] = (st["composition_violations"] == 0 and st["composition_proven_zero_violations"] == 0
                  and st["composition_cases"] > 0 and st["composition_mutant_violations"] > 0)
    return st


# ------------------------------------------------------------------------------------------------ G3 degree drop

def g3_degree_drop(ncases, prime, seed=20261116):
    """Random pairs over Z[y]/(P) in one variable x with an exact leading coefficient divisible by p at r (degree
    drop modulo p): phi of the exact formal resultant equals the M5 image formula."""
    rng = random.Random(seed)
    ring = cc.NodeRing(["x"])
    ctx = ring.ex
    y = ctx.gen(0)
    xg = ctx.gen(1)
    p, r = prime.p, prime.r
    stats = {"cases": 0, "mismatches": 0, "drops": {}}

    def rand_elt():
        return sum(rng.randint(-20, 20) * y**i for i in range(5))

    def vanishing_elt():
        return ring.reduce((y - r) * rand_elt() + p * rng.randint(1, 50))

    for _ in range(ncases):
        m, n = rng.randint(2, 4), rng.randint(1, 3)
        drop = rng.randint(1, min(2, m))
        cf = [rand_elt() for _ in range(m + 1)]
        for t in range(drop):
            cf[m - t] = vanishing_elt()
        cg = [rand_elt() for _ in range(n + 1)]
        cg[n] = rand_elt() + 1000003   # a unit image with overwhelming probability
        cf = [ring.reduce(c) for c in cf]
        cg = [ring.reduce(c) for c in cg]
        if cg[n] == 0 or cc.phi(ring, cg[n], prime) == 0:
            continue
        f = sum((cf[c] * xg**c for c in range(m + 1)), ctx.from_dict({}))
        g = sum((cg[c] * xg**c for c in range(n + 1)), ctx.from_dict({}))
        F, G = cc.phi(ring, f, prime), cc.phi(ring, g, prime)
        mp = F.degrees()[0]
        if F == 0 or mp == 0 and False:
            continue
        # exact formal Sylvester determinant over Z[y]/(P): entries are polynomials in y (variable x unused)
        yc = fmpz_mpoly_ctx.get(["y"], "lex")
        yy = yc.gen(0)
        Py = yy**5 - yy**4 + 3 * yy**3 + 3 * yy**2 + 26
        red = lambda t: divmod(t, Py)[1]
        to_y = lambda e: yc.from_dict({(k[0],): int(v) for k, v in e.to_dict().items()})
        det = formal_resultant_exact([to_y(c) for c in cf], [to_y(c) for c in cg], yc, reduce=red)
        det = red(det)
        # image of the exact value
        pimg = sum(int(c) * pow(r, k[0], p) for k, c in det.to_dict().items()) % p
        R = cc.res_image(F, G, 0, "x", m, p)
        val = R.to_dict().get((0,), 0) if R != 0 else 0
        stats["cases"] += 1
        key = int(m - mp)
        stats["drops"][key] = stats["drops"].get(key, 0) + 1
        if int(val) % p != pimg:
            stats["mismatches"] += 1
    stats["pass"] = stats["mismatches"] == 0 and stats["cases"] >= ncases * 0.9 and any(k > 0 for k in stats["drops"])
    return stats


# ------------------------------------------------------------------------------------------------ G4 controls

def planted_systems(prime, seed=20261117):
    """Exact systems over Z[y]/(P) in three variables (order x1, x2, x3): (unit, constant, common root)."""
    rng = random.Random(seed)
    ring = cc.NodeRing(["x1", "x2", "x3"])
    ctx = ring.ex
    y = ctx.gen(0)
    x1, x2, x3 = ctx.gens()[1:]

    def e():
        return sum(rng.randint(-9, 9) * y**i for i in range(5))

    def rpoly(vars_, deg, nt):
        out = ctx.from_dict({})
        for _ in range(nt):
            term = e()
            for v in vars_:
                term = term * v ** rng.randint(0, deg)
            out = out + term
        return ring.reduce(out)

    # unit ideal with a known constant: f3 = q f1 + c
    c = ring.reduce(e() + 3)
    f1 = ring.reduce(x1 + e() * x2 * x3 + e())
    f2 = rpoly([x1, x2, x3], 1, 4)
    q = rpoly([x1, x2, x3], 1, 3)
    f3 = ring.reduce(q * f1 + c)
    unit = [("f1", f1), ("f2", f2), ("f3", f3)]
    # common root (1, y, 2): every equation lies in the ideal of the point
    pt = [x1 - 1, x2 - y, x3 - 2]
    common = []
    for k in range(3):
        s = ctx.from_dict({})
        for lin in pt:
            s = s + ring.reduce(rpoly([x1, x2, x3], 1, 3) * lin)
        common.append((f"h{k}", ring.reduce(s)))
    # unit ideal whose chain ends in two coprime univariates: f1 = x1 - r1(x3), f2 = x2 - r2(x3), f3, f4 of degree 2
    # in x1 and x2 (so f1, f2 are the pivots); the expected final constant is Res_{x3}(f3(r1, r2, x3), f4(r1, r2, x3))
    r1 = rpoly([x3], 2, 2)
    r2 = rpoly([x3], 2, 2)
    g1 = ring.reduce(x1 - r1)
    g2 = ring.reduce(x2 - r2)
    g3 = ring.reduce(x1**2 * e() + x2**2 * e() + x3**3 * e() + x1 * x2 * e() + e())
    g4 = ring.reduce(x1**2 * e() + x2**2 * e() + x3**2 * e() + x1 * x3 * e() + e())

    def sub(f):
        return ring.reduce(f.compose(*[ctx.gen(0), r1, r2, x3]))

    unit2 = ([("f1", g1), ("f2", g2), ("f3", g3), ("f4", g4)], sub(g3), sub(g4))
    # the same shape with a planted common root (x3 = 2, x1 = r1(2), x2 = r2(2)): f3, f4 vanish there
    h = lambda: ring.reduce(x1 * e() + x2 * e() + x3 * e() + e())
    k3 = ring.reduce(h() * g1 + h() * g2 + h() * (x3 - 2) + x1**2 * (x3 - 2) * e())
    k4 = ring.reduce(h() * g1 + h() * g2 + h() * (x3 - 2) + x2**2 * (x3 - 2) * e())
    common2 = [("f1", g1), ("f2", g2), ("f3", k3), ("f4", k4)]
    return ring, unit, c, common + common2, unit2


def planted_split_common(seed=20261119, nextra=3):
    """A nonempty system that splits: f1 = w x - 1 with w = a + b v (a, b in Z[y]/(P), b a unit) and nextra generators
    (v - 2) (w^2 (e x^2 + e'') + w x e') that vanish at the point v = 2, x = 1/w(2) (w(2) != 0). Eliminating x against f1
    gives univariates (v - 2) w^2 (...), so the root splits on w; the root and the node w != 0 carry nextra - 1 >= 2
    final pairs on a nonempty ideal (their resultants share the factor v - 2, so every c is 0); the node w = 0 is empty
    (f1 becomes -1). nextra + 1 = n + 2 generators for n = 2 variables."""
    rng = random.Random(seed)
    ring = cc.NodeRing(["x", "v"])
    y, x, v = ring.ex.gens()

    def e():
        return sum(rng.randint(-9, 9) * y**i for i in range(5))
    w = (3 + y) + (2 - y**2) * v
    gens = [("f1", ring.reduce(w * x - 1))]
    for i in range(nextra):
        inner = w**2 * (e() * x**2 + e()) + w * x * e()
        gens.append((f"k{i}", ring.reduce((v - 2) * inner)))
    return ring, gens


def node_pair_stats(records):
    """Per node with a recorded last variable: the number of final pairs, how many are nonzero, the constant member."""
    out = {}
    for r in records:
        last = r.get("last")
        if last is None:
            continue
        out[r["id"]] = {"final_pairs": len(last["pairs"]), "nonzero_pairs": sum(1 for q in last["pairs"] if q["c"] != 0),
                        "constant_member": last["constant_member"], "certified": r.get("status") == "certified",
                        "status": r.get("status")}
    return out


def extended_control_violations(stats):
    """Nonempty nodes that carry a certificate (a certified status, a nonzero final constant or a constant member)."""
    return [nid for nid, s in stats.items()
            if s.get("nonempty") and (s["certified"] or s["nonzero_pairs"] or s["constant_member"] is not None)]


def extended_control_qualifying(stats):
    """Nonempty nodes that evaluated at least two final pairs, all zero, with no constant member and no certificate."""
    return [nid for nid, s in stats.items()
            if s.get("nonempty") and s["final_pairs"] >= 2 and s["nonzero_pairs"] == 0
            and s["constant_member"] is None and not s["certified"]]


def extended_control_ok(stats):
    return not extended_control_violations(stats) and bool(extended_control_qualifying(stats))


def _sing_poly(ring, f, prime):
    acc = {}
    for mono, c in f.to_dict().items():
        key = tuple(mono[1:])
        acc[key] = (acc.get(key, 0) + int(c) * pow(prime.r, mono[0], prime.p)) % prime.p
    terms = []
    for key, c in acc.items():
        if c:
            mono = "*".join(f"{v}^{e}" for v, e in zip(ring.order, key) if e)
            terms.append(str(c) + ("*" + mono if mono else ""))
    return "+".join(terms) or "0"


def singular_dims(systems, prime, workdir=None, name="dims", timeout=1800):
    """Dimension and vector-space dimension of std(I) in Singular 4.3.2 at (p, r), for each system
    {key: (ring, [exact polys], w or None)}; with w the ideal is I + (s w - 1) (s a new variable): dimension >= 0 means
    the zero set of I with w != 0 is nonempty. dim -1 is the unit ideal. Returns {key: {"dim", "vdim"}}."""
    lines = []
    for k, (key, (ring, polys, w)) in enumerate(systems.items()):
        vars_ = list(ring.order) + (["sinv_"] if w is not None else [])
        gens = [_sing_poly(ring, f, prime) for f in polys]
        if w is not None:
            gens.append(f"sinv_*({_sing_poly(ring, w, prime)})-1")
        lines.append(f"ring R{k} = {prime.p},({','.join(vars_)}),dp;")
        lines.append("option(redSB);")
        lines.append("ideal I = " + ",\n".join(gens) + ";")
        lines.append("ideal J = std(I);")
        lines.append(f"print(\"DIMS {key} \" + string(dim(J)) + \" \" + string(vdim(J)));")
        lines.append("kill I, J;")
    lines.append("quit;")
    wd = Path(workdir) if workdir else temp_root() / "dims"
    rc, out, err = se.run_singular("\n".join(lines) + "\n", wd, timeout=timeout, name=name)
    res = {}
    for ln in out.splitlines():
        t = ln.split()
        if len(t) == 4 and t[0] == "DIMS":
            res[t[1]] = {"dim": int(t[2]), "vdim": int(t[3])}
    if rc != 0 or set(res) != {str(k) for k in systems}:
        raise RuntimeError(f"Singular dimension check failed (rc {rc}): {err[-300:]}")
    return res


def tree_node_systems(st):
    """{node id: (ring, exact inputs, w)} for every node with a recorded last variable (w = the split variable of a
    w != 0 node, so the ideal is I + (s w - 1))."""
    out = {}
    for r in st.records:
        if r.get("last") is None:
            continue
        nd = st.nodes[r["id"]]
        ring = nd["ring"]
        w = ring.ex.gens()[-1] if r["kind"] == "w!=0" else None
        out[r["id"]] = (ring, list(nd["inputs"].values()), w)
    return out


def prove_nonempty(stats, st, prime, workdir=None, name="nodes"):
    """Fill stats[nid]["nonempty"], dim and vdim from Singular on each node's inputs (I, or I + (s w - 1))."""
    systems = tree_node_systems(st)
    if systems:
        for nid, d in singular_dims(systems, prime, workdir=workdir, name=name).items():
            ring, polys, w = systems[nid]
            # the generator and variable counts of the system Singular sees (a w != 0 node adds s and s w - 1), review F1 item 3
            stats[nid].update({"dim": d["dim"], "vdim": d["vdim"], "nonempty": d["dim"] >= 0,
                               "generators": len(polys) + (w is not None), "variables": ring.n + (w is not None)})
    return stats


def run_branch_control(k, node_seconds, hard_seconds, argv=None, extras=None):
    """One branch control in a child process with a hard wall limit (flint resultants are not interruptible).
    Entry: certified True/False only for a child that exited 0 and printed NEGRESULT ("finished"); a child that crashed
    or printed nothing is {certified: None, outcome: "crashed (returncode N)"} and blocks G4 (review F2); a child killed
    at the limit is {certified: None, outcome: "inconclusive (killed at the limit)"} and is counted apart."""
    removed = f"E{SUBSET[k]}"
    if argv is None:
        argv = [sys.executable, str(HERE / "gates.py"), "--neg", str(k), str(node_seconds)]
        if extras is not None:
            argv = [sys.executable, str(HERE / "gates.py"), "--neg-ext", str(k), str(node_seconds)] + list(extras)
    try:
        r = subprocess.run(argv, capture_output=True, text=True, timeout=hard_seconds, cwd=str(HERE))
    except subprocess.TimeoutExpired:
        entry = {"removed": removed, "certified": None, "outcome": f"inconclusive (killed at the {hard_seconds} s limit)"}
    else:
        lines = [ln for ln in r.stdout.splitlines() if ln.startswith("NEGRESULT ")]
        if r.returncode != 0 or not lines:
            entry = {"removed": removed, "certified": None, "outcome": f"crashed (returncode {r.returncode})",
                     "error": r.stderr[-300:]}
        else:
            entry = json.loads(lines[-1][len("NEGRESULT "):])
            entry["outcome"] = "finished"
    if extras is not None:
        entry["extras"] = list(extras)
    return entry


def control_blocks_g4(entry):
    """A control blocks G4 when it certified a nonempty system or crashed; a timeout is inconclusive, not a pass."""
    return entry.get("certified") is True or str(entry.get("outcome", "")).startswith("crashed")


def branch_subset_nonemptiness(primes, workdir=None):
    """Singular dim and vdim of the six drop-one ideals and the full subset at each prime (review F3). The drop-one
    ideals must be nonempty (dim >= 0) and the full subset must be the unit ideal (dim -1)."""
    d = json.loads(BRANCH["plus"].read_text())
    ring5 = cc.NodeRing(ORDER)
    _, ins = branch_inputs(d, ring5)
    exact = dict(ins)
    out = {"pass": True}
    for tag, pr in primes.items():
        systems = {"full": (ring5, [exact[f"E{e}"] for e in SUBSET], None)}
        for e in SUBSET:
            systems[f"drop{e}"] = (ring5, [exact[f"E{x}"] for x in SUBSET if x != e], None)
        dims = singular_dims(systems, pr, workdir=workdir, name=f"subset-{tag}")
        out[tag] = {"p": pr.p, "r": pr.r, **dims}
        out["pass"] = bool(out["pass"] and dims["full"]["dim"] == -1
                           and all(dims[f"drop{e}"]["dim"] >= 0 for e in SUBSET))
    return out


def g4_controls(prime, branch_plus_path=None, node_seconds=120, removal_cases=(0,), log=print, hard_seconds=300,
                neg_argv=None, extended_cases=None, nonempty=True, prime2=None, ext_hard_seconds=900,
                ext_node_seconds=400):
    res = {}
    ring, unit, c, commons, (unit2, A2, B2) = planted_systems(prime)
    common, common2 = commons[:3], commons[3:]
    ok, st = cc.solve_tree(ring.order, unit, prime, max_depth=2, node_seconds=60, log=lambda *_: None, tag="unit")
    res["planted_unit_certified"] = bool(ok)
    ok2, st2 = cc.solve_tree(ring.order, common, prime, max_depth=2, node_seconds=60, log=lambda *_: None, tag="common")
    res["planted_common_root_certified"] = bool(ok2)
    res["planted_common_root_statuses"] = [r["status"] for r in st2.records]
    ok3, st3 = cc.solve_tree(ring.order, unit2, prime, max_depth=2, node_seconds=60, log=lambda *_: None, tag="unit2")
    leaf = st3.records[0]
    pair = leaf["last"]["pairs"][0] if leaf["last"] and leaf["last"]["pairs"] else None
    expected = ring.reduce(A2.resultant(B2, "x3"))
    pexp = cc.phi(ring, expected, prime).to_dict()
    pexp = int(pexp.get((0, 0, 0), 0)) if pexp else 0
    res["planted_unit2_certified"] = bool(ok3)
    res["planted_unit2_constant_matches"] = bool(pair is not None and pair["c"] != 0 and pair["c"] in (pexp, prime.p - pexp))
    ok4, st4 = cc.solve_tree(ring.order, common2, prime, max_depth=3, node_seconds=60, log=lambda *_: None, tag="common2")
    res["planted_common_root_chain_certified"] = bool(ok4)
    res["planted_common_root_chain_statuses"] = [(r["id"], r["status"]) for r in st4.records]
    res["pass"] = bool(ok) and not ok2 and not ok4 and bool(ok3) and res["planted_unit2_constant_matches"]
    # the planted nonempty system with a split: final pairs on nonempty nodes (review F1)
    ring_s, gens_s = planted_split_common()
    ok5, st5 = cc.solve_tree(ring_s.order, gens_s, prime, max_depth=2, node_seconds=60, log=lambda *_: None, tag="psc")
    stats5 = node_pair_stats(st5.records)
    entry5 = {"generators": len(gens_s), "variables": ring_s.n, "certified": bool(ok5),
              "statuses": [(r["id"], r["status"]) for r in st5.records]}
    res["pass"] = bool(res["pass"] and not ok5 and len(gens_s) >= ring_s.n + 2)
    if nonempty:
        prove_nonempty(stats5, st5, prime, name="psc")
        entry5["extended_ok"] = extended_control_ok(stats5)
        res["pass"] = bool(res["pass"] and entry5["extended_ok"])
    entry5["nodes"] = stats5
    res["planted_split_common"] = entry5
    all_stats = {"planted_split_common": stats5}
    if branch_plus_path is not None:
        negs, exts = [], []
        for k in removal_cases:
            entry = run_branch_control(k, node_seconds, hard_seconds, argv=neg_argv)
            negs.append(entry)
            log(f"G4 control removing E{SUBSET[k]}: {entry}")
            if control_blocks_g4(entry):
                res["pass"] = False
        res["branch_minus_one_equation"] = negs
        res["branch_controls_finished"] = sum(1 for e in negs if e["outcome"] == "finished")
        res["branch_controls_inconclusive"] = sum(1 for e in negs if str(e["outcome"]).startswith("inconclusive"))
        res["branch_controls_crashed"] = sum(1 for e in negs if str(e["outcome"]).startswith("crashed"))
        for k, extras in (EXTENDED if extended_cases is None else extended_cases):
            entry = run_branch_control(k, ext_node_seconds, ext_hard_seconds, argv=neg_argv, extras=extras)
            exts.append(entry)
            log(f"G4 extended control {entry.get('removed')} + {list(extras)}: {entry}")
            if control_blocks_g4(entry):
                res["pass"] = False
            elif entry["outcome"] == "finished":
                all_stats[f"{entry['removed']}+{'+'.join(extras)}"] = entry["node_stats"]
        res["branch_extended_controls"] = exts
        if nonempty:
            ne = branch_subset_nonemptiness({"p1": prime, **({"p2": prime2} if prime2 is not None else {})})
            res["branch_subset_nonemptiness"] = ne
            res["pass"] = bool(res["pass"] and ne["pass"])
    summary = {"controls": list(all_stats), "violations": {}, "qualifying": {}}
    for tag, stt in all_stats.items():
        summary["violations"][tag] = extended_control_violations(stt)
        summary["qualifying"][tag] = extended_control_qualifying(stt)
    summary["nonempty_nodes_with_two_zero_pairs"] = sum(len(v) for v in summary["qualifying"].values())
    res["final_pair_summary"] = summary
    if nonempty:
        res["pass"] = bool(res["pass"] and not any(summary["violations"].values())
                           and summary["nonempty_nodes_with_two_zero_pairs"] >= 1)
    return res


SUBSET = [3, 5, 6, 7, 10, 11]   # EXP-142 structure.md item 6: {E2,E3,E5,E6,E7,E10,E11}; E2 vanishes on a branch
# branch controls with n + 2 = 7 generators: the drop-one subset plus two of its own ideal members E_a + c * var * E_b
# (spec "a:var:b:c", var "1" for none)
EXTENDED = [(4, ("5:q0:6:1", "7:q2:11:1")), (5, ("5:q0:6:1", "7:q2:10:1"))]


def _drop_one_inputs(k, extras=()):
    d = json.loads(BRANCH["plus"].read_text())
    ring5 = cc.NodeRing(ORDER)
    _, ins = branch_inputs(d, ring5)
    exact = dict(ins)
    sub = [(f"E{e}", exact[f"E{e}"]) for j, e in enumerate(SUBSET) if j != k]
    gens = dict(zip(ring5.order, ring5.ex.gens()[1:]))
    for i, spec in enumerate(extras):
        a, var, b, c = spec.split(":")
        mult = 1 if var == "1" else gens[var]
        sub.append((f"X{i}", ring5.reduce(exact[f"E{a}"] + int(c) * mult * exact[f"E{b}"])))
    return ring5, sub


def neg_worker(k, node_seconds, extras=None):
    """Child process of a branch control: the drop-one system (plus, when extras is given, members of its own ideal)."""
    prime = cc.Prime(P1, R1)
    ring5, ins = _drop_one_inputs(k, extras or ())
    ok, st = cc.solve_tree(ring5.order, ins, prime, max_depth=3, node_seconds=node_seconds, log=lambda *_: None,
                           tag="neg")
    out = {"removed": f"E{SUBSET[k]}", "certified": bool(ok),
           "nodes": [(r["id"], r["status"], r.get("reason")) for r in st.records]}
    if extras is not None:
        stats = node_pair_stats(st.records)
        out["generators"] = len(ins)
        out["variables"] = ring5.n
        prove_nonempty(stats, st, prime, name=f"ext{k}")
        out["node_stats"] = stats
    print("NEGRESULT " + json.dumps(out))


if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "--neg":
        neg_worker(int(sys.argv[2]), int(sys.argv[3]))
    elif len(sys.argv) >= 5 and sys.argv[1] == "--neg-ext":
        neg_worker(int(sys.argv[2]), int(sys.argv[3]), extras=sys.argv[4:])
