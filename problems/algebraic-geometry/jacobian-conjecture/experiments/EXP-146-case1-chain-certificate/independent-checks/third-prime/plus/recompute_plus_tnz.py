"""Independent recomputation of the EXP-146 plus-branch leaf t.nz (w1 != 0) at a given prime (reviewer script).

Builds on recompute_plus.py (own exact Z[y]/(P) arithmetic). Levels 1 and 2 exact (closed resultant formulas for
(m,1) and (2,2)); levels 3 and 4 only through phi, computed by evaluation at points of (q2, w1) and formal Sylvester
determinants over F_p, then interpolation in q2 and w1 (Vandermonde solves). Proven bounds: level 3 by the plain
Sylvester assignment bound with exact level-2 coefficient supports (brute force over permutations); level 4 by the
assignment bound with entry bounds e_c(t) = min_s B_l3(s, t) - s c (s = 0..S), maximized by an own Hungarian routine
checked against brute force on random matrices.

Usage: python recompute_plus_tnz.py <slp-plus.json> <branch-plus eqs.json> <p> <r>
"""
import itertools
import json
import os
import random
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import recompute_plus as rp  # noqa: E402  (own reviewer module, not chaincert)
from flint import nmod_mat, nmod_poly, fmpz  # noqa: E402

S_RANGE = range(0, 7)
T_RANGE = range(-6, 7)
NEGINF = None


def hungarian_max(W):
    """Maximum-weight perfect assignment of a square integer matrix (None = forbidden). Own O(n^3) routine
    (shortest augmenting path with potentials, minimizing -W). Returns None if no perfect assignment exists."""
    n = len(W)
    BIG = 10**12
    cost = [[(BIG if W[i][j] is None else -W[i][j]) for j in range(n)] for i in range(n)]
    INF = 10**18
    u = [0] * (n + 1)
    v = [0] * (n + 1)
    match = [0] * (n + 1)
    way = [0] * (n + 1)
    for i in range(1, n + 1):
        match[0] = i
        j0 = 0
        minv = [INF] * (n + 1)
        used = [False] * (n + 1)
        while True:
            used[j0] = True
            i0 = match[j0]
            delta = INF
            j1 = -1
            for j in range(1, n + 1):
                if not used[j]:
                    cur = cost[i0 - 1][j - 1] - u[i0] - v[j]
                    if cur < minv[j]:
                        minv[j] = cur
                        way[j] = j0
                    if minv[j] < delta:
                        delta = minv[j]
                        j1 = j
            for j in range(n + 1):
                if used[j]:
                    u[match[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if match[j0] == 0:
                break
        while True:
            j1 = way[j0]
            match[j0] = match[j1]
            j0 = j1
            if j0 == 0:
                break
    total = 0
    for j in range(1, n + 1):
        i = match[j]
        if W[i - 1][j - 1] is None:
            return None
        total += W[i - 1][j - 1]
    return total


def brute_max(W):
    n = len(W)
    best = None
    for pm in itertools.permutations(range(n)):
        if any(W[i][pm[i]] is None for i in range(n)):
            continue
        s = sum(W[i][pm[i]] for i in range(n))
        best = s if best is None or s > best else best
    return best


def self_test_hungarian(trials=3000):
    rnd = random.Random(146)
    for _ in range(trials):
        n = rnd.randint(1, 6)
        W = [[(None if rnd.random() < 0.3 else rnd.randint(-20, 40)) for _ in range(n)] for _ in range(n)]
        assert hungarian_max(W) == brute_max(W), W
    return trials


def sylvester_matrix_entries(ef, eg, m, n):
    N, cells = rp.sylvester_layout(m, n)
    W = [[None] * N for _ in range(N)]
    for (row, col), (which, c) in cells.items():
        W[row][col] = (ef if which == 0 else eg).get(c)
    return W


def vandermonde_interp(xs, ys, p):
    """Coefficients c_0..c_{N-1} of the unique poly of degree < N through (xs, ys) mod p."""
    N = len(xs)
    A = nmod_mat([[pow(x, k, p) for k in range(N)] for x in xs], p)
    b = nmod_mat([[y % p] for y in ys], p)
    sol = A.solve(b)
    return [int(sol[k, 0]) for k in range(N)]


def main():
    slp_path, eqs_path, p, r = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    assert sum(c * pow(r, i, p) for i, c in enumerate(rp.PC)) % p == 0 and fmpz(p).is_prime() and p < 2**29
    print(f"prime p = {p}, root r = {r}")
    print(f"own Hungarian vs brute force on {self_test_hungarian()} random matrices: agree")
    slp = json.load(open(slp_path))
    eqs = json.load(open(eqs_path))
    nodes = {nd["id"]: nd for nd in slp["nodes"]}
    nd = nodes["t.nz"]
    root = nodes["t"]
    sp = root["split"]
    order0 = ["q5", "q3", "q4", "q2", "q0"]
    R0 = rp.R(order0)
    ins0 = {}
    for frm, eq in zip(eqs["from"], eqs["eqs"]):
        d = [dict() for _ in range(5)]
        for mono, cs in eq:
            e = tuple(mono[eqs["names"].index(v)] for v in order0)
            for j, c in enumerate(cs):
                if c:
                    d[j][e] = d[j].get(e, 0) + c
        ins0[f"E{frm}"] = [R0.ctx.from_dict(dj) for dj in d]
    # split check: lc_q5(E3) = a + b q0
    cf = R0.coeffs(ins0["E3"], 0)
    lc = cf[max(cf)]
    assert lc == R0.add(R0.const(sp["a"]), R0.mul(R0.const(sp["b"]), R0.var(4)))
    print("split of t: w1 = lc_q5(E3) = a + b q0 exactly: True")
    tr = nd["transform"]
    assert tr["a"] == sp["a"] and tr["b"] == sp["b"] and not tr.get("set_w_zero")
    # transform q0 -> (w1 - a)/b, times b^deg_q0
    Rn = rp.R(["q5", "q3", "q4", "q2", "w1"])
    assert Rn.names == nd["order"]
    A = Rn.add(Rn.var(4), Rn.const([-c for c in sp["a"]]))
    B = Rn.const(sp["b"])
    mapping = [0, 1, 2, 3, None]
    ins = {}
    t0 = time.time()
    for mid, F in ins0.items():
        cf = R0.coeffs(F, 4)
        dq = max(cf)
        tot = Rn.zero()
        Ap = [Rn.const([1, 0, 0, 0, 0])]
        Bp = [Rn.const([1, 0, 0, 0, 0])]
        for _ in range(dq):
            Ap.append(Rn.mul(Ap[-1], A))
            Bp.append(Rn.mul(Bp[-1], B))
        for k, C in cf.items():
            tot = Rn.add(tot, Rn.mul(rp.remap(R0, Rn, C, mapping), Rn.mul(Ap[k], Bp[dq - k])))
        ins[mid] = tot
    print(f"inputs transformed to (q5, q3, q4, q2, w1) in {time.time() - t0:.1f} s")
    steps = nd["steps"]
    exact = dict(ins)

    def res22(F, G, i):
        cf_, cg_ = Rn.coeffs(F, i), Rn.coeffs(G, i)
        z = Rn.zero()
        f0, f1, f2 = cf_.get(0, z), cf_.get(1, z), cf_[2]
        g0, g1, g2 = cg_.get(0, z), cg_.get(1, z), cg_[2]
        mul, sub = Rn.mul, (lambda X, Y: Rn.add(X, Rn.neg(Y)))
        a = sub(mul(f2, g0), mul(f0, g2))
        b = sub(mul(f2, g1), mul(f1, g2))
        c = sub(mul(f1, g0), mul(f0, g1))
        return sub(mul(a, a), mul(b, c))

    # self-check of the (2,2) formula against the Leibniz Sylvester determinant on a small random example
    Rt = rp.R(["x", "z"])
    rnd = random.Random(7)

    def rnd_el():
        return [Rt.ctx.from_dict({(i, j): rnd.randint(-5, 5) for i in range(3) for j in range(2)}) for _ in range(5)]
    Ft, Gt = rnd_el(), rnd_el()
    cfF, cfG = Rt.coeffs(Ft, 0), Rt.coeffs(Gt, 0)
    assert max(cfF) == 2 and max(cfG) == 2
    Rn_save = Rn
    Rn = Rt
    chk = res22(Ft, Gt, 0) == rp.res_exact_general(Rt, Ft, Gt, 0, 2, 2)
    Rn = Rn_save
    print(f"(2,2) closed formula equals the Leibniz Sylvester determinant on a random example: {chk}")
    assert chk

    # ---- exact levels 1 and 2 ----
    for lvl in (1, 2):
        step = steps[lvl - 1]
        xi = Rn.names.index(step["x"])
        Pe = exact[step["pivot"]]
        dpiv = Rn.deg(Pe, xi)
        pim = Rn.phi_terms(Pe, p, r)
        dimg = max(mo[xi] for mo in pim)
        print(f" level {lvl} ({step['x']}): pivot {step['pivot']} exact degree {dpiv}, recorded {step['n']}, image degree {dimg}")
        assert dpiv == step["n"] == dimg
        listed = {e["id"] for e in step["members"]}
        new = {}
        for mid, F in exact.items():
            if mid != step["pivot"] and mid not in listed:
                assert Rn.deg(F, xi) == 0
                new[mid] = F
        for e in step["members"]:
            F = exact[e["id"]]
            assert Rn.deg(F, xi) == e["m"]
            if dpiv == 1:
                Rx, _ = rp.res_linear(Rn, F, Pe, xi)
            else:
                assert dpiv == 2 and e["m"] == 2
                Rx = res22(F, Pe, xi)
            assert e["out"] is not None and not Rn.is_zero(Rx)
            new[e["out"]] = Rx
        exact = new
        print(f"   exact members: {sorted(exact)} ({time.time() - t0:.1f} s)")

    # ---- level 3 (q4): bounds from exact level-2 supports ----
    s3 = steps[2]
    assert s3["x"] == "q4"
    i4, i2, iw = 2, 3, 4
    piv3 = s3["pivot"]
    P3 = exact[piv3]
    n3 = Rn.deg(P3, i4)
    assert n3 == s3["n"]
    cfP3 = Rn.coeffs(P3, i4)
    for mid, F in exact.items():
        if mid != piv3 and mid not in {e["id"] for e in s3["members"]}:
            assert Rn.deg(F, i4) == 0
    mem3 = [e for e in s3["members"] if e["out"] is not None]
    cf3 = {}
    for e in mem3:
        F = exact[e["id"]]
        assert Rn.deg(F, i4) == e["m"]
        cf3[e["out"]] = (Rn.coeffs(F, i4), e["m"])
        for j in (0, 1):
            assert Rn.deg(F, j) == 0
    for j in (0, 1):
        assert Rn.deg(P3, j) == 0

    _sup = {}

    def wdeg(C, s, t):
        if id(C) not in _sup:
            _sup[id(C)] = (C, Rn.support(C))
        sup = _sup[id(C)][1]
        return max(int(s * mo[i2] + t * mo[iw]) for mo in sup) if sup else None

    B3 = {}
    for out, (cfF, m) in cf3.items():
        tab = {}
        for s in S_RANGE:
            for t in T_RANGE:
                ef = {c: wdeg(C, s, t) for c, C in cfF.items() if not Rn.is_zero(C)}
                eg = {c: wdeg(C, s, t) for c, C in cfP3.items() if not Rn.is_zero(C)}
                tab[(s, t)] = rp.assignment_bound(m, n3, ef, eg, "max")
        B3[out] = tab
        print(f"   own bound {out} = Res_q4;{m},{n3}: deg_q2 <= {tab[(1, 0)]}, deg_w1 <= {tab[(0, 1)]}, "
              f"ord_w1 >= {-tab[(0, -1)]}")

    def formal_deg_q2(tab):
        Bx = tab[(1, 0)]
        zeros = {c: min(tab[(s, 0)] - s * c for s in S_RANGE) < 0 for c in range(Bx + 1)}
        mdeg = max(c for c in range(Bx + 1) if not zeros[c])
        return mdeg, zeros

    # ---- level 4 (q2) and the last variable: own bounds ----
    s4 = steps[3]
    assert s4["x"] == "q2"
    piv4 = s4["pivot"]
    n4 = s4["n"]
    m_piv, z_piv = formal_deg_q2(B3[piv4])
    print(f" level 4 (q2): pivot {piv4}, recorded n {n4}; own proven q2-degree bound {B3[piv4][(1, 0)]}, "
          f"own formal degree {m_piv}")
    assert m_piv == n4

    def entries(tab, mdeg, zeros, t):
        return {c: min(tab[(s, t)] - s * c for s in S_RANGE) for c in range(mdeg + 1) if not zeros[c]}

    mem4 = [e for e in s4["members"] if e["out"] is not None]
    own4 = {}
    for e in mem4:
        mdeg, zeros = formal_deg_q2(B3[e["id"]])
        print(f"   {e['id']}: own formal q2-degree {mdeg}, recorded m {e['m']} (recorded >= own: {e['m'] >= mdeg})")
        assert e["m"] >= mdeg
        # entries for the recorded formal degree (coefficients above the own formal degree are proven zero)
        mrec = e["m"]
        zf = {c: (c > mdeg or zeros.get(c, True)) for c in range(mrec + 1)}
        D = hungarian_max(sylvester_matrix_entries(entries(B3[e["id"]], mrec, zf, 1),
                                                   entries(B3[piv4], n4, z_piv, 1), mrec, n4))
        Bm = hungarian_max(sylvester_matrix_entries(entries(B3[e["id"]], mrec, zf, -1),
                                                    entries(B3[piv4], n4, z_piv, -1), mrec, n4))
        own4[e["out"]] = (D, -Bm)
        print(f"   own bound {e['out']} = Res_q2;{mrec},{n4}({e['id']}, {piv4}): deg_w1 <= {D}, ord_w1 >= {-Bm}")

    # ---- images by evaluation ----
    def img_bivar(C):
        """phi of an exact element free of q5, q3, q4 as {(e_q2, e_w1): int}."""
        out = {}
        for mono, c in Rn.phi_terms(C, p, r).items():
            assert mono[0] == mono[1] == mono[2] == 0
            out[(mono[i2], mono[iw])] = c
        return out

    def ev(dct, s, t):
        return sum(c * pow(s, a, p) * pow(t, b, p) for (a, b), c in dct.items()) % p

    def to_uni_at_t(dct, t):
        """poly in q2 (coefficient list) at w1 = t."""
        co = {}
        for (a, b), c in dct.items():
            co[a] = (co.get(a, 0) + c * pow(t, b, p)) % p
        return nmod_poly([co.get(k, 0) for k in range(max(co) + 1)] if co else [0], p)

    imgP3 = {c: img_bivar(C) for c, C in cfP3.items()}
    imgF3 = {out: {c: img_bivar(C) for c, C in cfF.items()} for out, (cfF, m) in cf3.items()}
    Dmax = max(D for D, _ in own4.values())
    Nt = Dmax + 8
    q2deg = {out: B3[out][(1, 0)] for out in cf3}
    Ns = max(q2deg.values()) + 4
    s_pts = list(range(1, Ns + 1))
    t_pts = list(range(1, Nt + 1))
    print(f" evaluating at {Nt} points of w1 x {Ns} points of q2")
    l4_vals = {e["out"]: [] for e in mem4}
    lc_piv4_nonzero = False
    t1 = time.time()
    for t in t_pts:
        P3u = {c: to_uni_at_t(dct, t) for c, dct in imgP3.items()}
        F3u = {out: {c: to_uni_at_t(dct, t) for c, dct in d.items()} for out, d in imgF3.items()}
        l3_at_t = {}
        for out, (cfF, m) in cf3.items():
            vals = []
            for s in s_pts:
                fc = [int(F3u[out][c](s)) if c in F3u[out] else 0 for c in range(m + 1)]
                gc = [int(P3u[c](s)) if c in P3u else 0 for c in range(n3 + 1)]
                vals.append(int(rp.sylvester_numeric(fc, gc, m, n3, p).det()))
            co = vandermonde_interp(s_pts, vals, p)
            assert all(x == 0 for x in co[q2deg[out] + 1:]), "q2-degree above the own bound"
            l3_at_t[out] = co
        if l3_at_t[piv4][n4] != 0:
            lc_piv4_nonzero = True
        gco = l3_at_t[piv4][:n4 + 1]
        assert all(x == 0 for x in l3_at_t[piv4][n4 + 1:])
        for e in mem4:
            fco = l3_at_t[e["id"]][:e["m"] + 1]
            assert all(x == 0 for x in l3_at_t[e["id"]][e["m"] + 1:])
            l4_vals[e["out"]].append(int(rp.sylvester_numeric(fco, gco, e["m"], n4, p).det()))
    print(f"   done in {time.time() - t1:.0f} s; pivot {piv4} q2^{n4} coefficient nonzero as a poly in w1: {lc_piv4_nonzero}")
    assert lc_piv4_nonzero
    # ---- last variable ----
    last = nd["last"]
    V, dd = {}, {}
    for u in last["members"]:
        co = vandermonde_interp(t_pts, l4_vals[u["id"]], p)
        D, Lo = own4[u["id"]]
        nzi = [k for k, x in enumerate(co) if x]
        deg_img, ord_img = (max(nzi), min(nzi)) if nzi else (None, None)
        assert deg_img is not None and deg_img <= D, "image degree above the own bound"
        assert u["L"] <= Lo, f"recorded L {u['L']} above own proven order {Lo}"
        assert u["d"] + u["L"] >= D
        assert all(x == 0 for x in co[:u["L"]]), "division by w1^L not exact at this prime"
        Vc = co[u["L"]:u["L"] + u["d"] + 1]
        assert all(x == 0 for x in co[u["L"] + u["d"] + 1:])
        V[u["id"]] = Vc
        dd[u["id"]] = u["d"]
        print(f"   {u['id']}: own D = {D}, own L = {Lo}; recorded L = {u['L']}, d = {u['d']}; image degree {deg_img}, "
              f"order {ord_img}; V degree {deg_img - u['L']}")
    pv, npv = last["pivot"], last["n"]
    assert V[pv][npv] != 0 and dd[pv] == npv and own4[pv][0] - own4[pv][1] == npv
    print(f"   final pivot {pv}: V image degree {npv} = own proven bound {own4[pv][0]} - {own4[pv][1]} (attained)")
    consts = []
    for pr in last["pairs"]:
        c = int(rp.sylvester_numeric(V[pr["i"]] + [0] * (pr["m"] + 1 - len(V[pr["i"]])), V[pv], pr["m"], npv, p).det())
        consts.append((pr["i"], c))
        print(f"   constant Res_{{{pr['m']},{npv}}}(V_{pr['i']}, V_{pv}) mod p = {c}   (recorded at p1: {pr['c']})")
    nz = sum(1 for _, c in consts if c)
    print(f" leaf t.nz: {nz} of {len(consts)} constants nonzero at p = {p} ({time.time() - t0:.0f} s)")
    print("SUMMARY", json.dumps({"t.nz": {"nonzero": nz, "total": len(consts), "constants": consts}}))


if __name__ == "__main__":
    main()
