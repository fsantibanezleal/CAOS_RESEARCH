"""Independent recomputation of EXP-146 plus-branch leaves at a third prime (reviewer script, own code).

Uses only python-flint primitives (fmpz_mpoly products, nmod_poly, nmod_mat determinant). It does not import
chaincert.py. Exact elements of Z[y]/(P) are lists of 5 fmpz_mpoly coordinates (basis 1, y, ..., y^4), multiplied
by convolution and reduced with the table y^k mod P. Resultants at the exact levels use the closed formula for a
linear pivot, Res_{m,1}(f, g) = (-1)^m sum_c f_c (-g0)^c g1^(m-c), or a Leibniz Sylvester determinant otherwise.
Image resultants are determinants of formal-size Sylvester matrices (no degree-drop formula needed: the formal
determinant IS phi of the formal resultant). Degree bounds are the plain Sylvester assignment bound with EXACT
coefficient supports as entries, maximized by brute force over all permutations.

Usage: python recompute_plus.py <slp-plus.json> <branch-plus eqs.json> <p> <r> <leaf id> [<leaf id> ...]
"""
import itertools
import json
import sys
import time

from flint import fmpz_mpoly_ctx, nmod_mat, nmod_poly, fmpz

PC = [26, 0, 3, 3, -1, 1]  # P = y^5 - y^4 + 3y^3 + 3y^2 + 26


def ypow_table(kmax):
    """y^k mod P as integer 5-vectors."""
    tab = []
    v = [1, 0, 0, 0, 0]
    for _ in range(kmax + 1):
        tab.append(list(v))
        # multiply by y: shift, then replace y^5 by y^4 - 3y^3 - 3y^2 - 26
        top = v[4]
        v = [0] + v[:4]
        v = [v[0] - 26 * top, v[1], v[2] - 3 * top, v[3] - 3 * top, v[4] + top]
    return tab


YP = ypow_table(8)


class R:
    """Exact polynomial ring over Z[y]/(P) in the given variables; elements are 5-lists of fmpz_mpoly."""

    def __init__(self, names):
        self.names = list(names)
        self.n = len(names)
        self.ctx = fmpz_mpoly_ctx.get(self.names, "lex")
        self.zero_p = self.ctx.from_dict({})

    def zero(self):
        return [self.zero_p] * 5

    def const(self, vec):
        z = (0,) * self.n
        return [self.ctx.from_dict({z: int(c)}) if c else self.zero_p for c in vec]

    def var(self, i):
        e = [0] * self.n
        e[i] = 1
        return [self.ctx.from_dict({tuple(e): 1})] + [self.zero_p] * 4

    def add(self, A, B):
        return [a + b for a, b in zip(A, B)]

    def neg(self, A):
        return [-a for a in A]

    def mul(self, A, B):
        c = [self.zero_p] * 9
        for i in range(5):
            if A[i] == 0:
                continue
            for j in range(5):
                if B[j] == 0:
                    continue
                c[i + j] = c[i + j] + A[i] * B[j]
        out = c[:5]
        for k in range(5, 9):
            if c[k] == 0:
                continue
            for j in range(5):
                if YP[k][j]:
                    out[j] = out[j] + YP[k][j] * c[k]
        return out

    def pow(self, A, k):
        out = self.const([1, 0, 0, 0, 0])
        for _ in range(k):
            out = self.mul(out, A)
        return out

    def is_zero(self, A):
        return all(a == 0 for a in A)

    def support(self, A):
        s = set()
        for a in A:
            for m in a.monoms():
                s.add(tuple(m))
        return s

    def coeffs(self, A, i):
        """{k: coefficient of x_i^k} (an element free of x_i)."""
        out = {}
        for j, a in enumerate(A):
            for mono, c in a.to_dict().items():
                k = mono[i]
                m2 = list(mono)
                m2[i] = 0
                d = out.setdefault(k, [dict() for _ in range(5)])
                d[j][tuple(m2)] = c
        return {k: [self.ctx.from_dict(dj) for dj in d] for k, d in out.items()}

    def from_coeffs(self, cf, i):
        tot = self.zero()
        for k, C in cf.items():
            tot = self.add(tot, self.mul(C, self.pow(self.var(i), k)))
        return tot

    def deg(self, A, i):
        s = self.support(A)
        return max((m[i] for m in s), default=-1)

    def phi_terms(self, A, p, r):
        """Image under y -> r mod p as {exponent tuple: int}."""
        rp = [pow(r, j, p) for j in range(5)]
        acc = {}
        for j, a in enumerate(A):
            for mono, c in a.to_dict().items():
                acc[mono] = (acc.get(mono, 0) + int(c) * rp[j]) % p
        return {k: v for k, v in acc.items() if v}


def remap(Rsrc, Rdst, A, mapping):
    """Move an element to another ring; mapping[i_src] = i_dst or None (exponent must then be 0)."""
    out = []
    for a in A:
        d = {}
        for mono, c in a.to_dict().items():
            e = [0] * Rdst.n
            for i, k in enumerate(mono):
                if mapping[i] is None:
                    assert k == 0, "dropping a variable that occurs"
                else:
                    e[mapping[i]] += k
            d[tuple(e)] = c
        out.append(Rdst.ctx.from_dict(d))
    return out


def res_linear(Rg, F, G, i):
    """Exact Res_{m,1}(F, G) in x_i, m = deg F, G = g1 x + g0 with exact degree 1."""
    cf, cg = Rg.coeffs(F, i), Rg.coeffs(G, i)
    m = max(cf)
    assert max(cg) == 1
    g1, g0 = cg[1], cg.get(0, Rg.zero())
    mg0 = Rg.neg(g0)
    tot = Rg.zero()
    for c in range(m + 1):
        if c not in cf:
            continue
        tot = Rg.add(tot, Rg.mul(cf[c], Rg.mul(Rg.pow(mg0, c), Rg.pow(g1, m - c))))
    if m % 2:
        tot = Rg.neg(tot)
    return tot, m


def perm_sign(pm):
    s, seen = 1, [False] * len(pm)
    for i in range(len(pm)):
        if seen[i]:
            continue
        j, L = i, 0
        while not seen[j]:
            seen[j] = True
            j = pm[j]
            L += 1
        if L % 2 == 0:
            s = -s
    return s


def sylvester_layout(m, n):
    """List of (row, col, which, c): entry = coefficient c of f (which 0) or g (which 1); size m + n."""
    N = m + n
    cells = {}
    for i in range(n):
        for t in range(m + 1):
            cells[(i, i + t)] = (0, m - t)
    for i in range(m):
        for t in range(n + 1):
            cells[(n + i, i + t)] = (1, n - t)
    return N, cells


def res_exact_general(Rg, F, G, i, m, n):
    """Exact formal Res_{m,n} by the Leibniz expansion of the Sylvester matrix (small sizes only)."""
    cf, cg = Rg.coeffs(F, i), Rg.coeffs(G, i)
    N, cells = sylvester_layout(m, n)
    tot = Rg.zero()
    for pm in itertools.permutations(range(N)):
        prod = None
        ok = True
        for row in range(N):
            cell = cells.get((row, pm[row]))
            if cell is None:
                ok = False
                break
            which, c = cell
            e = (cf if which == 0 else cg).get(c)
            if e is None:
                ok = False
                break
            prod = e if prod is None else Rg.mul(prod, e)
        if not ok:
            continue
        if perm_sign(pm) < 0:
            prod = Rg.neg(prod)
        tot = Rg.add(tot, prod)
    return tot


def assignment_bound(m, n, ef, eg, mode):
    """Plain Sylvester assignment bound by brute force over permutations.
    ef[c], eg[c]: entry values (None = structurally zero). mode 'max' (degree) or 'min' (order)."""
    N, cells = sylvester_layout(m, n)
    best = None
    for pm in itertools.permutations(range(N)):
        s = 0
        ok = True
        for row in range(N):
            cell = cells.get((row, pm[row]))
            if cell is None:
                ok = False
                break
            which, c = cell
            v = (ef if which == 0 else eg).get(c)
            if v is None:
                ok = False
                break
            s += v
        if not ok:
            continue
        if best is None or (s > best if mode == "max" else s < best):
            best = s
    return best


def det_poly_leibniz(M, p):
    """Determinant of a small square matrix of nmod_poly (Leibniz)."""
    N = len(M)
    tot = nmod_poly([0], p)
    for pm in itertools.permutations(range(N)):
        prod = nmod_poly([1], p)
        ok = True
        for row in range(N):
            e = M[row][pm[row]]
            if e == 0:
                ok = False
                break
            prod = prod * e
        if not ok:
            continue
        tot = tot + prod if perm_sign(pm) > 0 else tot - prod
    return tot


def sylvester_numeric(fc, gc, m, n, p):
    """Formal Sylvester matrix over F_p: fc[c], gc[c] ints for c = 0..m / 0..n."""
    N, cells = sylvester_layout(m, n)
    rows = []
    for row in range(N):
        line = []
        for col in range(N):
            cell = cells.get((row, col))
            if cell is None:
                line.append(0)
            else:
                which, c = cell
                line.append(int((fc if which == 0 else gc)[c]) % p)
        rows.append(line)
    return nmod_mat(rows, p)


def main():
    slp_path, eqs_path, p, r = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    leaves = sys.argv[5:]
    assert sum(c * pow(r, i, p) for i, c in enumerate(PC)) % p == 0, "P(r) != 0 mod p"
    assert fmpz(p).is_prime() and p < 2**29
    slp = json.load(open(slp_path))
    eqs = json.load(open(eqs_path))
    print(f"prime p = {p}, root r = {r}; P(r) mod p = 0; recorded primes {slp['prime_tree']} {slp['prime_replay']}")
    nodes = {nd["id"]: nd for nd in slp["nodes"]}

    # ---- root ring and inputs from the data-root branch file (not from the SLP) ----
    order0 = ["q5", "q3", "q4", "q2", "q0"]
    R0 = R(order0)
    ins0 = {}
    for frm, eq in zip(eqs["from"], eqs["eqs"]):
        d = [dict() for _ in range(5)]
        for mono, cs in eq:
            assert len(cs) == 5 and all(isinstance(c, int) for c in cs)
            e = tuple(mono[eqs["names"].index(v)] for v in order0)
            for j, c in enumerate(cs):
                if c:
                    d[j][e] = d[j].get(e, 0) + c
        ins0[f"E{frm}"] = [R0.ctx.from_dict(dj) for dj in d]
    # the SLP inputs equal the data-root inputs
    for mid, tl in slp["inputs"].items():
        d = [dict() for _ in range(5)]
        for t in tl:
            for j, c in enumerate(t["coords"]):
                if c:
                    d[j][tuple(t["exps"])] = c
        assert [R0.ctx.from_dict(dj) for dj in d] == ins0[mid], f"SLP input {mid} differs from eqs.json"
    print("inputs: 9 equations from eqs.json, identical to the SLP inputs:", list(ins0))

    def transform(Rsrc, ins, vname, a, b, wname, set_zero):
        """b^(deg_v f) f(v = (w - a)/b); new order = src order without v, then w (w := 0 if set_zero)."""
        vi = Rsrc.names.index(vname)
        names2 = [u for u in Rsrc.names if u != vname] + ([] if set_zero else [wname])
        R2 = R(names2)
        mapping = [None if i == vi else names2.index(u) for i, u in enumerate(Rsrc.names)]
        A = R2.const([-c for c in a]) if set_zero else R2.add(R2.var(R2.n - 1), R2.const([-c for c in a]))
        B = R2.const(b)
        out = {}
        for mid, F in ins.items():
            cf = Rsrc.coeffs(F, vi)
            d = max(cf)
            tot = R2.zero()
            for k, C in cf.items():
                C2 = remap(Rsrc, R2, C, mapping)
                tot = R2.add(tot, R2.mul(C2, R2.mul(R2.pow(A, k), R2.pow(B, d - k))))
            out[mid] = tot
        return R2, out

    def check_split(Rn, ins, sp):
        """The recorded split polynomial equals the leading coefficient of the named pivot, of the form a + b v."""
        xi = Rn.names.index(sp["x"])
        vi = Rn.names.index(sp["v"])
        cf = Rn.coeffs(ins[sp["pivot"]], xi)
        lc = cf[max(cf)]
        want = Rn.add(Rn.const(sp["a"]), Rn.mul(Rn.const(sp["b"]), Rn.var(vi)))
        return lc == want

    # build the node inputs along the path of each leaf
    cache = {"t": (R0, ins0)}

    def node_inputs(nid):
        if nid in cache:
            return cache[nid]
        nd = nodes[nid]
        par = nodes[nd["parent"]]
        Rp, insp = node_inputs(par["id"])
        sp = par["split"]
        ok = check_split(Rp, insp, sp)
        print(f"  split of {par['id']}: {sp['w']} = lc_{sp['x']}({sp['pivot']}) = a + b {sp['v']} exactly: {ok}")
        assert ok
        tr = nd["transform"]
        assert tr["a"] == sp["a"] and tr["b"] == sp["b"] and tr["v"] == sp["v"]
        Rn, insn = transform(Rp, insp, tr["v"], tr["a"], tr["b"], tr["w"], tr.get("set_w_zero", False))
        assert Rn.names == nd["order"], (Rn.names, nd["order"])
        cache[nid] = (Rn, insn)
        return Rn, insn

    def phi_uni(Rn, A, xi):
        """Image as nmod_poly in variable xi (A must be free of the other variables)."""
        t = Rn.phi_terms(A, p, r)
        d = {}
        for mono, c in t.items():
            assert all(k == 0 for j, k in enumerate(mono) if j != xi), "not univariate"
            d[mono[xi]] = c
        if not d:
            return nmod_poly([0], p)
        return nmod_poly([d.get(i, 0) for i in range(max(d) + 1)], p)

    summary = {}
    for leaf in leaves:
        t0 = time.time()
        nd = nodes[leaf]
        print(f"\n===== leaf {leaf} (kind {nd['kind']}, order {nd['order']}, split var {nd['split_var']})")
        Rn, ins = node_inputs(leaf)
        n = Rn.n
        assert sorted(nd["inputs"]) == sorted(ins), "input set differs"
        for mid in ins:
            assert not Rn.is_zero(ins[mid])
            assert Rn.phi_terms(ins[mid], p, r), f"input {mid} is zero at this prime"
        exact = dict(ins)  # exact members alive
        lvl = 0
        bounds = {}  # member id -> (deg_w, ord_w) proven for the last variable (non-exact members)
        img_only = {}  # member id -> image (non-exact, univariate coefficients in the last variable)
        for step in nd["steps"]:
            lvl += 1
            x = step["x"]
            xi = Rn.names.index(x)
            piv = step["pivot"]
            listed = {e["id"] for e in step["members"]}
            if lvl <= 2:
                # exact level: pivot exact degree and image degree
                Pe = exact[piv]
                dpiv = Rn.deg(Pe, xi)
                pimg = Rn.phi_terms(Pe, p, r)
                dimg = max(m[xi] for m in pimg)
                print(f" level {lvl} ({x}): pivot {piv} exact degree {dpiv}, recorded n {step['n']}, image degree at this prime {dimg}")
                assert dpiv == step["n"] == dimg
                new = {}
                for mid, F in exact.items():
                    if mid == piv:
                        continue
                    dF = Rn.deg(F, xi)
                    if mid not in listed:
                        assert dF == 0, f"{mid} not listed but depends on {x}"
                        new[mid] = F
                        continue
                for e in step["members"]:
                    F = exact[e["id"]]
                    dF = Rn.deg(F, xi)
                    assert dF == e["m"], f"recorded m {e['m']} != exact degree {dF} for {e['id']}"
                    assert e["kind"] == "res"
                    if step["n"] == 1:
                        Rx, _ = res_linear(Rn, F, Pe, xi)
                    else:
                        Rx = res_exact_general(Rn, F, Pe, xi, dF, step["n"])
                    if e["out"] is None:
                        print(f"   {e['id']} -> dropped in the record (image zero at p1); exact zero: {Rn.is_zero(Rx)}")
                        continue
                    assert not Rn.is_zero(Rx)
                    new[e["out"]] = Rx
                exact = new
                print(f"   exact members after level {lvl}: {sorted(exact)} ({time.time() - t0:.1f} s)")
            else:
                # image-only level (level 3 here): every alive member is exact level-2 (checked), the pivot too
                assert lvl == 3 and piv in exact, "this script handles one image level fed by exact level-2 members"
                last = n - 1
                assert xi == n - 2
                Pe = exact[piv]
                dpiv = Rn.deg(Pe, xi)
                cfP = Rn.coeffs(Pe, xi)
                print(f" level {lvl} ({x}): pivot {piv} exact degree {dpiv}, recorded n {step['n']}")
                assert dpiv == step["n"]
                gimg = {c: phi_uni(Rn, C, last) for c, C in cfP.items()}
                assert gimg[dpiv] != 0, "pivot leading coefficient vanishes at this prime"
                print(f"   pivot leading coefficient image nonzero at this prime (degree attained)")
                for mid, F in exact.items():
                    if mid != piv and mid not in listed:
                        assert Rn.deg(F, xi) == 0
                for e in step["members"]:
                    F = exact[e["id"]]
                    dF = Rn.deg(F, xi)
                    assert dF == e["m"], (e, dF)
                    if e["out"] is None:
                        continue
                    cfF = Rn.coeffs(F, xi)
                    # own plain Sylvester assignment bound on the last variable, entries = exact coefficient supports
                    def dg(C, sgn):
                        s = Rn.support(C)
                        if not s:
                            return None
                        return max(int(sgn * mono[last]) for mono in s)
                    ef = {c: dg(C, 1) for c, C in cfF.items() if not Rn.is_zero(C)}
                    eg = {c: dg(C, 1) for c, C in cfP.items() if not Rn.is_zero(C)}
                    D = assignment_bound(dF, dpiv, ef, eg, "max")
                    efo = {c: -dg(C, -1) for c, C in cfF.items() if not Rn.is_zero(C)}  # orders
                    ego = {c: -dg(C, -1) for c, C in cfP.items() if not Rn.is_zero(C)}
                    Lo = assignment_bound(dF, dpiv, efo, ego, "min")
                    bounds[e["out"]] = (D, Lo)
                    # image by the formal Sylvester determinant over F_p[last]
                    fimg = {c: phi_uni(Rn, C, last) for c, C in cfF.items()}
                    N, cells = sylvester_layout(dF, dpiv)
                    M = [[nmod_poly([0], p)] * N for _ in range(N)]
                    for (row, col), (which, c) in cells.items():
                        src = fimg if which == 0 else gimg
                        M[row][col] = src.get(c, nmod_poly([0], p))
                    img = det_poly_leibniz(M, p)
                    img_only[e["out"]] = img
                    print(f"   {e['out']} = Res_{x};{dF},{dpiv}({e['id']}, {piv}): own bound deg <= {D}, order >= {Lo}; "
                          f"image at this prime: degree {img.degree()}, order "
                          f"{min(i for i in range(img.degree() + 1) if int(img[i]) != 0) if img != 0 else None}")
                exact = {}
        # ---- last variable ----
        lastrec = nd["last"]
        last = n - 1
        print(f" last variable {lastrec['x']} (recorded pivot {lastrec['pivot']}, n {lastrec['n']})")
        V = {}
        dd = {}
        for u in lastrec["members"]:
            mid = u["id"]
            if mid in img_only:
                img = img_only[mid]
                D, Lo = bounds[mid]
                if nd["split_var"] == lastrec["x"]:
                    L = Lo
                else:
                    L = 0
                # recorded L must not exceed the own proven order bound; recorded d + L must not be below own D
                assert u["L"] <= L, f"recorded L {u['L']} above own proven order {L} for {mid}"
                assert u["d"] + u["L"] >= D, f"recorded formal degree below own bound for {mid}"
                Luse, duse = u["L"], u["d"]
                coeffs = [int(img[i]) for i in range(img.degree() + 1)] if img != 0 else []
                assert all(c == 0 for c in coeffs[:Luse]), "division by w^L not exact at this prime"
                Vp = nmod_poly(coeffs[Luse:] or [0], p)
                print(f"   {mid}: own D = {D}, own L = {L}; recorded L = {u['L']}, d = {u['d']}; "
                      f"V image degree {Vp.degree()} (<= d: {Vp.degree() <= duse})")
                assert Vp.degree() <= duse
            else:
                F = exact[mid]
                for j in range(n - 1):
                    assert Rn.deg(F, j) == 0
                Dx = Rn.deg(F, last)
                assert u["L"] == 0 and u["d"] == Dx, (u, Dx)
                Vp = phi_uni(Rn, F, last)
                duse = Dx
                print(f"   {mid}: exact degree {Dx} = recorded d {u['d']}; image degree {Vp.degree()}")
            V[mid] = Vp
            dd[mid] = duse
        # exact members not listed among the last members must be absent (free of the last variable => constants)
        pv = lastrec["pivot"]
        npv = lastrec["n"]
        assert V[pv].degree() == npv == dd[pv], f"final pivot does not attain its degree at this prime: {V[pv].degree()} vs {npv}"
        print(f"   final pivot {pv}: image degree {V[pv].degree()} = proven {npv} (attained at this prime)")
        consts = []
        gco = [int(V[pv][i]) for i in range(npv + 1)]
        for pr in lastrec["pairs"]:
            mid = pr["i"]
            m = pr["m"]
            assert m == dd[mid]
            fco = [int(V[mid][i]) if i <= V[mid].degree() else 0 for i in range(m + 1)]
            c = int(sylvester_numeric(fco, gco, m, npv, p).det())
            consts.append((mid, m, npv, c))
            print(f"   constant Res_{{{m},{npv}}}(V_{mid}, V_{pv}) mod p = {c}   (recorded at p1: {pr['c']})")
        nz = sum(1 for c in consts if c[3] != 0)
        print(f" leaf {leaf}: {nz} of {len(consts)} constants nonzero at p = {p} ({time.time() - t0:.1f} s)")
        summary[leaf] = {"nonzero": nz, "total": len(consts), "constants": consts}
    print("\nSUMMARY", json.dumps({k: {"nonzero": v["nonzero"], "total": v["total"],
                                       "constants": [[c[0], c[3]] for c in v["constants"]]}
                                   for k, v in summary.items()}))


if __name__ == "__main__":
    main()
