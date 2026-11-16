"""Independent recomputation of EXP-146 branch q1 = -c, leaves t.z.nz (two splits, w2 != 0) and t.z.z (two splits,
w2 = 0), at a third prime p3 < 2^29 with a root of P, distinct from p1 and p2.

Reviewer script (jc-exp146-review-2026-11-15, lens recompute-minus). It does not import chaincert.py. It reads:
  - the exact branch inputs from the data root (exp142-143-branch-minus/eqs.json, SHA-256 checked);
  - the recorded tree (artifacts/slp-minus.json copied from the branch): coordinate changes (a, b), pivot ids,
    formal degrees, L_i, final pairs, p1 constants and the p1 digests of every member.
Everything else is recomputed here:
  - exact coordinate changes over Z[y]/(P) (own substitution code), the split polynomials re-derived from E3;
  - exact chain levels 1 and 2 over Z[y]/(P) (python-flint resultants, reduced mod P);
  - exact level 3 over Z[y]/(P) for t.z.nz when it finishes (gives the exact w2-order and degree outright);
  - own bound: plain Sylvester assignment bound (bitmask dynamic program, not a Hungarian) from the exact
    level-2 supports, at the weights +e_w2 and -e_w2 (Laurent) and over the whole grid W;
  - images at p1 (digest comparison with the record) and at p3 (formal Sylvester determinants built explicitly,
    the level-3 bivariate ones by evaluation and interpolation in w2, the constants by an nmod_mat determinant;
    cross-checked against flint's resultant with the degree-drop factor).
Usage: python recompute_minus.py <slp-minus.json> <eqs.json> [--p3 P]
"""
import hashlib
import itertools
import json
import sys
import time

from flint import fmpz_mpoly_ctx, nmod_mat, nmod_mpoly_ctx, nmod_poly

PC = (26, 0, 3, 3, -1, 1)  # P = y^5 - y^4 + 3y^3 + 3y^2 + 26, low to high
P1 = 536870909
P2 = 536870879
SHA_MINUS = "0a3a390581c4f44c06907a61022069f7d704283e3b1def8947bb44cafaae76e9"
NEGINF = None


def is_prime(n):
    if n < 2:
        return False
    for q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % q == 0:
            return n == q
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def roots_of_P(p):
    return sorted(int(r) for r, _ in nmod_poly(list(PC), p).roots())


def pick_p3(start):
    p = start
    while True:
        if is_prime(p) and p not in (P1, P2):
            rs = roots_of_P(p)
            if rs:
                return p, rs
        p -= 1


# ------------------------------------------------------------------------------------------------- exact ring
class Ring:
    def __init__(self, order):
        self.order = list(order)
        self.n = len(order)
        self.ctx = fmpz_mpoly_ctx.get(["y"] + self.order, "lex")
        y = self.ctx.gen(0)
        self.P = y**5 - y**4 + 3 * y**3 + 3 * y**2 + 26

    def red(self, f):
        _, r = divmod(f, self.P)
        if r != 0:
            assert max(m[0] for m in r.monoms()) < 5, "reduction left y^5"
        return r

    def yel(self, vec):
        """element of Z[y]/(P) from a coordinate vector, as a constant polynomial of this ring"""
        d = {}
        for i, c in enumerate(vec):
            if c:
                d[(i,) + (0,) * self.n] = int(c)
        return self.ctx.from_dict(d)

    def deg(self, f, v):
        return f.degrees()[1 + self.order.index(v)] if f != 0 else -1


def coeff_in(R, f, v, k):
    """coefficient of v^k in f (as a polynomial of R with v-exponent 0)"""
    j = 1 + R.order.index(v)
    d = {}
    for m, c in f.to_dict().items():
        if m[j] == k:
            mm = list(m)
            mm[j] = 0
            d[tuple(mm)] = c
    return R.ctx.from_dict(d)


def move(Rsrc, Rdst, f, rename=None):
    """re-embed f of Rsrc into Rdst (variables matched by name; rename maps src name -> dst name)."""
    rename = rename or {}
    idx = []
    for v in Rsrc.order:
        tv = rename.get(v, v)
        idx.append(None if tv is None else 1 + Rdst.order.index(tv))
    d = {}
    for m, c in f.to_dict().items():
        mm = [0] * (Rdst.n + 1)
        mm[0] = m[0]
        for t, e in enumerate(m[1:]):
            if e:
                assert idx[t] is not None, "variable dropped while present"
                mm[idx[t]] = e
        d[tuple(mm)] = c
    return Rdst.ctx.from_dict(d)


def substitute(Rsrc, Rdst, f, v, a_vec, b_vec, wname):
    """b^d f(v := (w - a)/b), d = deg_v f, exact over Z[y]/(P); wname None means w := 0."""
    d = Rsrc.deg(f, v)
    A = (Rdst.ctx.gen(1 + Rdst.order.index(wname)) if wname else 0) - Rdst.yel(a_vec)
    B = Rdst.yel(b_vec)
    total = Rdst.ctx.from_dict({})
    Ap = [Rdst.ctx.from_dict({(0,) * (Rdst.n + 1): 1})]
    Bp = [Ap[0]]
    for _ in range(d):
        Ap.append(Rdst.red(Ap[-1] * A))
        Bp.append(Rdst.red(Bp[-1] * B))
    for k in range(d + 1):
        fk = coeff_in(Rsrc, f, v, k)
        if fk == 0:
            continue
        fk2 = move(Rsrc, Rdst, fk, {v: None})
        total = total + Rdst.red(Rdst.red(fk2 * Ap[k]) * Bp[d - k])
    return Rdst.red(total)


def lin_coeffs(R, f, x, n, v):
    """leading coefficient of f in x (degree n) as a + b v; returns (a_vec, b_vec) or None."""
    lc = coeff_in(R, f, x, n)
    a, b = [0] * 5, [0] * 5
    jv = 1 + R.order.index(v)
    for m, c in lc.to_dict().items():
        rest = list(m[1:])
        if all(e == 0 for e in rest):
            a[m[0]] = int(c)
        elif rest[jv - 1] == 1 and sum(rest) == 1:
            b[m[0]] = int(c)
        else:
            return None
    return a, b


# ------------------------------------------------------------------------------------------------- images
def img(R, f, p, r):
    ctx = nmod_mpoly_ctx.get(R.order, modulus=p)
    acc = {}
    for m, c in f.to_dict().items():
        k = tuple(m[1:])
        acc[k] = (acc.get(k, 0) + int(c) * pow(r, m[0], p)) % p
    return ctx.from_dict({k: v for k, v in acc.items() if v})


def digest(F, n, p):
    pts = []
    for t in range(2):  # the record's digest points (key definition, chaincert.digest_points)
        pts.append(tuple((1000003 * (t + 2) * (i + 3) + 12345 * t + 7) % p or 1 for i in range(n)))
    return {"terms": len(F), "degrees": [int(e) for e in F.degrees()], "eval": [int(F(*pt)) for pt in pts]}


def sylv_det_scalar(fc, gc, m, n, p):
    """formal Sylvester determinant Res_{m,n} from coefficient lists fc[0..m], gc[0..n] (low to high) mod p."""
    N = m + n
    if N == 0:
        return 1
    M = [[0] * N for _ in range(N)]
    for i in range(n):
        for j in range(m + 1):
            M[i][i + j] = fc[m - j] % p
    for i in range(m):
        for j in range(n + 1):
            M[n + i][i + j] = gc[n - j] % p
    return int(nmod_mat(M, p).det())


def interp(xs, ys, p):
    """Newton interpolation mod p; returns coefficient list low to high."""
    n = len(xs)
    c = list(ys)
    for j in range(1, n):
        for i in range(n - 1, j - 1, -1):
            c[i] = (c[i] - c[i - 1]) * pow(xs[i] - xs[i - j], -1, p) % p
    poly = [0]
    for i in range(n - 1, -1, -1):
        # poly = poly * (x - xs[i]) + c[i]
        newp = [0] * (len(poly) + 1)
        for k, a in enumerate(poly):
            newp[k + 1] = (newp[k + 1] + a) % p
            newp[k] = (newp[k] - a * xs[i]) % p
        newp[0] = (newp[0] + c[i]) % p
        poly = newp
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def biv(F, ix, iw):
    """image F (only variables ix, iw present) -> dict {(cx, ew): coef}"""
    d = {}
    for m, c in F.to_dict().items():
        assert all(e == 0 for t, e in enumerate(m) if t not in (ix, iw)), "unexpected variable"
        d[(m[ix], m[iw])] = int(c)
    return d


def res_biv_formal(F, G, ix, iw, m, n, p):
    """phi Res_{x; m, n}(f, g) as a univariate in w (low to high), from the formal Sylvester determinant evaluated at
    enough points and interpolated. Degree bound used for the number of points: row sums (independent of any
    assignment bound)."""
    fd, gd = biv(F, ix, iw), biv(G, ix, iw)
    assert all(c <= m for c, _ in fd) and all(c <= n for c, _ in gd), "image above formal degree"
    fw = max([e for _, e in fd] + [0])
    gw = max([e for _, e in gd] + [0])
    D = n * fw + m * gw
    xs = list(range(1, D + 2))
    ys = []
    for t in xs:
        fc = [0] * (m + 1)
        gc = [0] * (n + 1)
        for (c, e), v in fd.items():
            fc[c] = (fc[c] + v * pow(t, e, p)) % p
        for (c, e), v in gd.items():
            gc[c] = (gc[c] + v * pow(t, e, p)) % p
        ys.append(sylv_det_scalar(fc, gc, m, n, p))
    return interp(xs, ys, p)


def res_image_flint(F, G, xname, ix, m, p):
    """cross-check: flint resultant of the images times the degree-drop factor (-1)^(n(m-m')) lc(G)^(m-m')."""
    n = G.degrees()[ix]
    mp = F.degrees()[ix]
    R = F.resultant(G, xname)
    if mp < m:
        dd = {}
        for mo, c in G.to_dict().items():
            if mo[ix] == n:
                mm = list(mo)
                mm[ix] = 0
                dd[tuple(mm)] = c
        R = R * (G.context().from_dict(dd) ** (m - mp))
        if (n * (m - mp)) % 2:
            R = -R
    return R


def univ_list(F, iw):
    d = {}
    for mo, c in F.to_dict().items():
        d[mo[iw]] = int(c)
    if not d:
        return [0]
    return [d.get(i, 0) for i in range(max(d) + 1)]


# ------------------------------------------------------------------------------------------------- own bound
def ent_deg(R, f, x, c, wt):
    """exact w-degree of the coefficient of x^c in f (None if that coefficient is zero); wt: dict var -> weight."""
    j = 1 + R.order.index(x)
    best = None
    for mo in f.monoms():
        if mo[j] == c:
            s = sum(wt.get(R.order[t], 0) * mo[1 + t] for t in range(R.n) if R.order[t] != x)
            best = s if best is None or s > best else best
    return best


def max_assign(M):
    """max over permutations of sum M[i][s(i)], None entries forbidden; bitmask DP over columns."""
    N = len(M)
    dp = {0: 0}
    for i in range(N):
        nd = {}
        for mask, val in dp.items():
            for j in range(N):
                if mask >> j & 1 or M[i][j] is None:
                    continue
                k = mask | (1 << j)
                v = val + M[i][j]
                if k not in nd or v > nd[k]:
                    nd[k] = v
        dp = nd
    return dp.get((1 << N) - 1)


def sylv_bound(R, f, g, x, m, n, wt):
    N = m + n
    M = [[None] * N for _ in range(N)]
    fe = [ent_deg(R, f, x, c, wt) for c in range(m + 1)]
    ge = [ent_deg(R, g, x, c, wt) for c in range(n + 1)]
    for i in range(n):
        for j in range(m + 1):
            M[i][i + j] = fe[m - j]
    for i in range(m):
        for j in range(n + 1):
            M[n + i][i + j] = ge[n - j]
    return max_assign(M)


# ------------------------------------------------------------------------------------------------- main
def main():
    slp_path, eqs_path = sys.argv[1], sys.argv[2]
    p3_start = int(sys.argv[sys.argv.index("--p3") + 1]) if "--p3" in sys.argv else 400_000_000
    out = {"problems": []}

    def problem(s):
        out["problems"].append(s)
        print("PROBLEM:", s)

    raw = open(eqs_path, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    print("eqs sha256", sha, "match" if sha == SHA_MINUS else "MISMATCH")
    if sha != SHA_MINUS:
        problem("input sha mismatch")
    E = json.loads(raw)
    slp = json.load(open(slp_path))
    nodes = {nd["id"]: nd for nd in slp["nodes"]}
    p1, r1 = slp["prime_tree"]["p"], slp["prime_tree"]["r"]
    assert p1 == P1 and slp["prime_replay"]["p"] == P2
    p3, roots3 = pick_p3(p3_start)
    r3 = roots3[0]
    assert p3 < 2**29 and sum(c * pow(r3, i, p3) for i, c in enumerate(PC)) % p3 == 0
    print(f"p3 = {p3}, roots of P mod p3 = {roots3}, r3 = {r3}")
    out.update({"p3": p3, "r3": r3, "roots3": roots3})

    # ---- root inputs (exact), compare to the slp's recorded inputs
    R0 = Ring(["q5", "q3", "q4", "q2", "q0"])
    names = E["names"]
    ins0 = {}
    for frm, eq in zip(E["from"], E["eqs"]):
        d = {}
        for ex, cs in eq:
            mono = [ex[names.index(v)] for v in R0.order]
            for i, c in enumerate(cs):
                if c:
                    d[(i,) + tuple(mono)] = int(c)
        ins0[f"E{frm}"] = R0.ctx.from_dict(d)
    # the slp stores exponents in the elimination order (q5, q3, q4, q2, q0); eqs.json in its own names order
    same = set(slp["inputs"]) == set(ins0) and all(
        sorted((tuple(t["exps"]), tuple(int(c) for c in t["coords"])) for t in slp["inputs"][k]) ==
        sorted((tuple(ex[names.index(v)] for v in slp["order"]), tuple(int(c) for c in cs))
               for ex, cs in E["eqs"][E["from"].index(int(k[1:]))])
        for k in slp["inputs"])
    print("slp inputs equal data-root eqs:", same)
    if not same:
        problem("slp inputs differ from eqs.json")
    for k, f in ins0.items():
        assert f == R0.red(f), "input not reduced"

    # ---- split 1: E3's q5 leading coefficient = a1 + b1 q0 at the root
    tz = nodes["t.z"]["transform"]
    lc1 = lin_coeffs(R0, ins0["E3"], "q5", R0.deg(ins0["E3"], "q5"), "q0")
    ok1 = lc1 is not None and lc1[0] == [int(c) for c in tz["a"]] and lc1[1] == [int(c) for c in tz["b"]]
    print("split1 (a1,b1) = E3 q5-leading coefficient, deg_q5 E3 =", R0.deg(ins0["E3"], "q5"), ":", ok1)
    if not ok1:
        problem("split 1 coefficients do not match E3")
    root1_p1 = (-sum(c * pow(r1, i, p1) for i, c in enumerate(lc1[0])) *
                pow(sum(c * pow(r1, i, p1) for i, c in enumerate(lc1[1])), -1, p1)) % p1
    print("split1 image root at p1:", root1_p1, "recorded", nodes["t"]["split"]["root"])

    # ---- node t.z inputs: w1 := 0
    Rz = Ring(["q5", "q3", "q4", "q2"])
    t0 = time.time()
    insz = {k: substitute(R0, Rz, f, "q0", lc1[0], lc1[1], None) for k, f in ins0.items()}
    print(f"t.z inputs exact in {time.time() - t0:.1f} s; zero inputs:", [k for k, f in insz.items() if f == 0])

    # ---- split 2: E3's q3 leading coefficient at t.z = a2 + b2 q2
    tzn = nodes["t.z.nz"]["transform"]
    dE3 = Rz.deg(insz["E3"], "q3")
    lc2 = lin_coeffs(Rz, insz["E3"], "q3", dE3, "q2")
    ok2 = lc2 is not None and lc2[0] == [int(c) for c in tzn["a"]] and lc2[1] == [int(c) for c in tzn["b"]]
    print("split2 (a2,b2) = E3 q3-leading coefficient at t.z, deg_q5 E3 =", Rz.deg(insz["E3"], "q5"),
          "deg_q3 =", dE3, ":", ok2)
    if not ok2:
        problem("split 2 coefficients do not match E3 at t.z")
    for name, pp, rr in (("p1", p1, r1), ("p3", p3, r3)):
        pa = sum(c * pow(rr, i, pp) for i, c in enumerate(lc2[0])) % pp
        pb = sum(c * pow(rr, i, pp) for i, c in enumerate(lc2[1])) % pp
        print(f"  split2 at {name}: phi(b2) = {pb}, root = {(-pa * pow(pb, -1, pp)) % pp if pb else None}")

    Rn = Ring(["q5", "q3", "q4", "w2"])
    t0 = time.time()
    insn = {k: substitute(Rz, Rn, f, "q2", lc2[0], lc2[1], "w2") for k, f in insz.items()}
    Rzz = Ring(["q5", "q3", "q4"])
    inszz = {k: substitute(Rz, Rzz, f, "q2", lc2[0], lc2[1], None) for k, f in insz.items()}
    print(f"t.z.nz and t.z.z inputs exact in {time.time() - t0:.1f} s")

    for leaf, R, ins in (("t.z.nz", Rn, insn), ("t.z.z", Rzz, inszz)):
        out[leaf] = run_leaf(leaf, nodes[leaf], R, ins, p1, r1, p3, r3, problem)
        if leaf == "t.z.nz":
            # the same leaf at p2 must reproduce the recorded replay constants (sanity of this script)
            out[leaf + "@p2"] = run_leaf(leaf, nodes[leaf], R, ins, P2, slp["prime_replay"]["r"], P2,
                                         slp["prime_replay"]["r"], problem, quiet=True)
            rec2 = [c["c"] for c in slp["replay"][leaf]["constants"]]
            mine2 = [abs(c) for c in out[leaf + "@p2"]["constants_p3_flint"]]
            print(f"[{leaf}] constants at p2 (this script, flint form):", out[leaf + "@p2"]["constants_p3_flint"],
                  "recorded replay:", rec2)
    for leaf, R, ins in (("t.z.nz", Rn, insn), ("t.z.z", Rzz, inszz)):
        o1 = run_leaf(leaf, nodes[leaf], R, ins, p1, r1, p1, r1, problem, quiet=True)
        rec1 = [pr["c"] for pr in nodes[leaf]["last"]["pairs"]]
        print(f"[{leaf}] constants at p1 (this script, flint form): {o1['constants_p3_flint']} recorded: {rec1}",
              "EQUAL" if o1["constants_p3_flint"] == rec1 else "DIFFERENT")
        if o1["constants_p3_flint"] != rec1:
            problem(f"{leaf}: p1 constants differ from the record")
    print("PROBLEMS:", len(out["problems"]))
    for k in ("t.z.nz", "t.z.z"):
        print(k, "constants at p3 (formal Sylvester det):", out[k]["constants_p3"],
              "nonzero", sum(1 for c in out[k]["constants_p3"] if c), "of", len(out[k]["constants_p3"]))
    json.dump(out, open(sys.argv[0].replace(".py", "-out.json"), "w"), indent=1, default=str)


def run_leaf(leaf, nd, R, ins, p1, r1, p3, r3, problem, quiet=False):
    say = (lambda *a: None) if quiet else print
    n = R.n
    order = R.order
    split = nd["split_var"]
    res = {}
    # digests of the inputs at p1
    ex = dict(ins)
    imgs1 = {k: img(R, f, p1, r1) for k, f in ins.items()}
    imgs3 = {k: img(R, f, p3, r3) for k, f in ins.items()}
    dig_bad = 0
    for k in nd["inputs"]:
        if p1 == P1 and digest(imgs1[k], n, p1) != nd["members"][k]["digest"]:
            dig_bad += 1
    say(f"[{leaf}] inputs {nd['inputs']}: p1 digest mismatches {dig_bad}")
    if dig_bad:
        problem(f"{leaf}: input digests differ at p1")
    exact_lvl = {}
    bstat = {"checked": 0, "tight": 0}
    cur = [k for k in nd["inputs"]]
    check_dig = (p1 == P1)
    # chain steps
    for lvl, st in enumerate(nd["steps"], start=1):
        x = st["x"]
        ix = order.index(x)
        pv = st["pivot"]
        exact_now = pv in ex
        n_rec = st["n"]
        # pivot degree: exact pivots (levels 1, 2 and exact members) have their exact degree as their bound
        if exact_now:
            n_ex = R.deg(ex[pv], x)
            att3 = imgs3[pv].degrees()[ix]
            say(f"[{leaf}] level {lvl} x={x} pivot {pv}: recorded n={n_rec}, exact degree {n_ex}, image degree at p3 "
                f"{att3}, at p1 {imgs1[pv].degrees()[ix]}")
            if n_ex != n_rec or att3 != n_ex or imgs1[pv].degrees()[ix] != n_ex:
                problem(f"{leaf}: pivot {pv} degree")
        else:
            problem(f"{leaf}: pivot {pv} not exact (not covered by this script)")
        # members with positive x-degree must all appear in the step
        listed = {e["id"] for e in st["members"]}
        pos = {k for k in cur if k != pv and k in ex and R.deg(ex[k], x) > 0}
        newcur = [k for k in cur if k != pv and k not in listed]
        for e in st["members"]:
            if e["kind"] == "pass":
                newcur.append(e["id"])
            elif e["out"] is not None:
                newcur.append(e["out"])
        nonexact_free = [k for k in cur if k != pv and k not in ex and k not in listed]
        assert not nonexact_free
        if not pos <= listed:
            problem(f"{leaf}: members with positive {x}-degree not in the step: {sorted(pos - listed)}")
        for e in st["members"]:
            g = e["id"]
            if e["kind"] == "pass":
                continue
            m_rec = e["m"]
            if g in ex:
                m_ex = R.deg(ex[g], x)
                if m_ex != m_rec:
                    problem(f"{leaf}: formal degree of {g} in {x}: recorded {m_rec}, exact {m_ex}")
            if e["out"] is None:
                continue
            oid = e["out"]
            if lvl <= 2:
                t0 = time.time()
                h = R.red(ex[g].resultant(ex[pv], x))
                ex[oid] = h
                exact_lvl[oid] = h
                if not quiet:
                    for v in order:
                        if v == x:
                            continue
                        jv = 1 + order.index(v)
                        hi = sylv_bound(R, ex[g], ex[pv], x, m_rec, n_rec, {v: 1})
                        lo = -sylv_bound(R, ex[g], ex[pv], x, m_rec, n_rec, {v: -1})
                        edeg = max(mo[jv] for mo in h.monoms()) if h != 0 else -1
                        eord = min(mo[jv] for mo in h.monoms()) if h != 0 else 0
                        bstat["checked"] += 1
                        bstat["tight"] += int(hi == edeg and lo == eord)
                        if hi < edeg or lo > eord:
                            problem(f"{leaf}: own Sylvester bound invalid at {oid} in {v}")
                imgs1[oid] = img(R, h, p1, r1)
                imgs3[oid] = img(R, h, p3, r3)
                # check against the image chain at p3 (degree-drop formula) as well
                chk = res_image_flint(img(R, ex[g], p3, r3), imgs3[pv], x, ix, m_rec, p3)
                if chk != imgs3[oid]:
                    problem(f"{leaf}: phi3(exact {oid}) != image chain")
            else:
                F3, G3 = imgs3[g], imgs3[pv]
                iw = n - 1
                U3 = res_biv_formal(F3, G3, ix, iw, m_rec, n_rec, p3)
                fl = res_image_flint(F3, G3, x, ix, m_rec, p3)
                if univ_list(fl, iw) != U3 and not (fl == 0 and U3 == [0]):
                    problem(f"{leaf}: formal Sylvester image differs from flint+drop at {oid}")
                ctx = F3.context()
                imgs3[oid] = ctx.from_dict({tuple(e2 if t == iw else 0 for t in range(n)): c
                                            for e2, c in enumerate(U3) if c})
                U1 = res_biv_formal(imgs1[g], imgs1[pv], ix, iw, m_rec, n_rec, p1)
                ctx1 = imgs1[g].context()
                imgs1[oid] = ctx1.from_dict({tuple(e2 if t == iw else 0 for t in range(n)): c
                                             for e2, c in enumerate(U1) if c})
            if check_dig and digest(imgs1[oid], n, p1) != nd["members"][oid]["digest"]:
                problem(f"{leaf}: p1 digest differs at {oid}")
        cur = newcur
    if set(cur) != {u["id"] for u in nd["last"]["members"]}:
        problem(f"{leaf}: members reaching the last variable {sorted(cur)} differ from the record")
    res["exact_levels"] = len(exact_lvl)
    res["own_bound_selfcheck"] = bstat
    say(f"[{leaf}] own Sylvester bound against the exact levels: {bstat['checked']} (member, variable) pairs, "
        f"0 invalid unless a PROBLEM is printed, {bstat['tight']} tight in both degree and order")
    say(f"[{leaf}] exact levels computed: {len(exact_lvl)}; p1 digests of every member compared")
    # ---- last variable
    last = nd["last"]
    xl = last["x"]
    iw = order.index(xl)
    rows = []
    level3 = [s for s in nd["steps"] if len(nd["steps"]) >= 3][-1:] if len(nd["steps"]) >= 3 else []
    src = {}
    for s in level3:
        for e in s["members"]:
            if e["out"]:
                src[e["out"]] = (e["id"], s["pivot"], s["x"], e["m"], s["n"])
    for u in last["members"]:
        uid = u["id"]
        if uid in ex:  # exact univariate (t.z.z): bound = exact
            B_hi = R.deg(ex[uid], xl)
            B_lo = min(mo[1 + iw] for mo in ex[uid].monoms())
            how = "exact"
        else:
            g, pv, x, m, nn = src[uid]
            wt_hi = {xl: 1}
            wt_lo = {xl: -1}
            B_hi = sylv_bound(R, ex[g], ex[pv], x, m, nn, wt_hi)
            B_lo = -sylv_bound(R, ex[g], ex[pv], x, m, nn, wt_lo)
            how = f"Sylvester bound of Res_{x}({g},{pv}; {m},{nn})"
        L_mine = B_lo if xl == split else 0
        d_mine = B_hi - L_mine
        I3 = imgs3[uid]
        ul = univ_list(I3, iw)
        ordr = next((i for i, c in enumerate(ul) if c), None)
        degr = len(ul) - 1 if ordr is not None else -1
        rows.append({"id": uid, "how": how, "bound_deg": B_hi, "bound_order": B_lo, "L_rec": u["L"], "d_rec": u["d"],
                     "img3_order": ordr, "img3_deg": degr})
        say(f"[{leaf}] {uid}: {how}: deg bound {B_hi}, order bound {B_lo}; recorded L={u['L']} d={u['d']}; "
            f"image at p3: order {ordr}, degree {degr}")
        if L_mine != u["L"] or d_mine != u["d"]:
            problem(f"{leaf}: {uid} recorded (L, d) = ({u['L']}, {u['d']}) vs own ({L_mine}, {d_mine})")
        if ordr is None or ordr < u["L"]:
            problem(f"{leaf}: {uid} image at p3 not divisible by w^L")
    res["last_rows"] = rows
    V3 = {}
    for u in last["members"]:
        ul = univ_list(imgs3[u["id"]], iw)
        V3[u["id"]] = ul[u["L"]:] if len(ul) > u["L"] else [0]
    pv = last["pivot"]
    nn = last["n"]
    vp = V3[pv]
    while len(vp) > 1 and vp[-1] == 0:
        vp.pop()
    say(f"[{leaf}] final pivot {pv}: recorded n={nn}, own formal degree {[r for r in rows if r['id'] == pv][0]['bound_deg'] - [r for r in rows if r['id'] == pv][0]['L_rec']}, image degree at p3 {len(vp) - 1}")
    if len(vp) - 1 != nn:
        problem(f"{leaf}: final pivot does not attain its degree at p3")
    consts, constsf = [], []
    for pr in last["pairs"]:
        vi = V3[pr["i"]]
        while len(vi) > 1 and vi[-1] == 0:
            vi.pop()
        m = pr["m"]
        if pr["constant"]:
            consts.append(vi[0])
            constsf.append(vi[0])
            continue
        assert len(vi) - 1 <= m
        fc = vi + [0] * (m + 1 - len(vi))
        c = sylv_det_scalar(fc, vp, m, nn, p3)
        consts.append(c)
        # cross-check: nmod_poly resultant with the degree-drop factor
        F = nmod_poly(vi, p3)
        G = nmod_poly(vp, p3)
        mp = F.degree()
        cf = int(F.resultant(G)) if F != 0 else 0
        if F != 0 and mp < m:
            cf = cf * pow(vp[-1], m - mp, p3) * (-1) ** (nn * (m - mp)) % p3
        constsf.append(cf)
        if cf % p3 != c % p3:
            problem(f"{leaf}: constant {pr['i']}: Sylvester det {c} vs flint+drop {cf}")
    res["constants_p3"] = consts
    res["constants_p3_flint"] = constsf
    res["constants_p1_recorded"] = [pr["c"] for pr in last["pairs"]]
    say(f"[{leaf}] constants at p3: {consts} (recorded at p1: {res['constants_p1_recorded']})")
    if not any(consts):
        problem(f"{leaf}: no nonzero constant at p3")
    return res


if __name__ == "__main__":
    main()
