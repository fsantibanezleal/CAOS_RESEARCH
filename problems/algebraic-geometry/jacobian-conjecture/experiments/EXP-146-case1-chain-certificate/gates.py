"""EXP-146 gates G0 to G4 (hypothesis.md). G2 (real system) and G5 run inside chaincert.chain_node."""
import hashlib
import json
import random
import subprocess
import sys
from pathlib import Path

from flint import fmpz_mpoly_ctx

import chaincert as cc

HERE = Path(__file__).resolve().parent
DATA = Path("E:/_Datos/caos-research/jacobian-conjecture")
EXP141 = DATA / "exp141-main" / "eqs.json"
BRANCH = {"plus": DATA / "exp142-143-branch-plus" / "eqs.json", "minus": DATA / "exp142-143-branch-minus" / "eqs.json"}
SHA = {"plus": "bd227b531c813586f60b1792b90ef7595d19d226b7ab2d380b3125250849424a",
       "minus": "0a3a390581c4f44c06907a61022069f7d704283e3b1def8947bb44cafaae76e9"}
BRANCHES_PY = HERE.parent / "EXP-142-case1-branch-certificates" / "branches.py"
P1, R1 = 536870909, 505390653


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


def g1_ring_maps(prime2):
    res = {"p1": P1, "r1": R1, "p2": prime2.p, "r2": prime2.r}
    ok = True
    for p, r in ((P1, R1), (prime2.p, prime2.r)):
        ok = ok and sum(c * pow(r, i, p) for i, c in enumerate(cc.P_COEFFS)) % p == 0
    d = json.loads(BRANCH["plus"].read_text())
    ints = all(isinstance(c, int) for eq in d["eqs"] for _, cs in eq for c in cs)
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
             "split_cases": 0, "low_tight": 0, "formal_degree_above_actual": 0}
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
        def coeffs(poly, deg):
            out = [ctx.from_dict({}) for _ in range(deg + 1)]
            for m, c in poly.to_dict().items():
                if m[0] > deg:
                    raise cc.BoundViolation("polynomial degree above its formal degree")
                mm = (0,) + tuple(m[1:])
                out[m[0]] = out[m[0]] + ctx.from_dict({mm: int(c)})
            return out
        cf, cg = coeffs(f, mf), coeffs(g, ng)
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
        hs = sorted({tuple(m) for m in h.monoms()})
        import numpy as np
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
        stats["drops"][m - mp] = stats["drops"].get(m - mp, 0) + 1
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


def g4_controls(prime, branch_plus_path=None, node_seconds=300, removal_cases=(0,), log=print):
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
    if branch_plus_path is not None:
        d = json.loads(Path(branch_plus_path).read_text())
        ring5 = cc.NodeRing(["q5", "q3", "q4", "q2", "q0"])
        names = d["names"]
        sub = [3, 5, 6, 7, 10, 11]   # EXP-142 structure.md item 6: {E2,E3,E5,E6,E7,E10,E11}; E2 vanishes on a branch
        byfrom = dict(zip(d["from"], d["eqs"]))
        negs = []
        for k in removal_cases:
            keep = [e for j, e in enumerate(sub) if j != k]
            ins = []
            for e in keep:
                terms = [([m[names.index(v)] for v in ring5.order], cs) for m, cs in byfrom[e]]
                ins.append((f"E{e}", ring5.from_vectors(terms)))
            okc, stc = cc.solve_tree(ring5.order, ins, prime, max_depth=3, node_seconds=node_seconds,
                                     log=lambda *_: None, tag="neg")
            negs.append({"removed": f"E{sub[k]}", "certified": bool(okc), "nodes": [(r['id'], r['status']) for r in stc.records]})
            if okc:
                res["pass"] = False
        res["branch_minus_one_equation"] = negs
    return res
