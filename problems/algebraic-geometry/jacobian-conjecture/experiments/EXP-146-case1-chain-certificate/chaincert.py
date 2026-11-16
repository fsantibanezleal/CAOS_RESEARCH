"""EXP-146: single-prime resultant-chain certificates with proven degree bounds (hypothesis.md, frozen).

Everything is over Z[y]/(P), P = y^5 - y^4 + 3 y^3 + 3 y^2 + 26, and its image F_p under phi: y -> r (M1).
Exact objects are python-flint fmpz_mpoly in the variables (y, order...), every result reduced modulo P (M2, M3).
Images are python-flint nmod_mpoly. Bounds (M4) are integer weighted-degree tables propagated by an exact integer
assignment (Hungarian). No floats anywhere in a bound or a certificate.

Public surface used by run.py, singular_eval.py and the tests:
  Prime, NodeRing, Bd, exact_bound, formal_degree, res_bound, max_assignment      (bound engine, M4)
  res_image, shift_down                                                           (image formula, M5, M6)
  chain_node, solve_tree, replay_leaf, exact_transform                           (chain, tree, replay: M5 to M8)
"""
import itertools
import time

import numpy as np
from flint import fmpz_mpoly_ctx, nmod_mpoly_ctx, nmod_poly

P_COEFFS = (26, 0, 3, 3, -1, 1)
KMAX = 3
NEG = -10**9
DEAD_BELOW = -5 * 10**8
ENTRY_LIMIT = 10**7
INF64 = np.int64(4 * 10**15)


class Timeout(Exception):
    """A node exceeded its wall-time allowance."""


class BoundViolation(AssertionError):
    """The bound engine or an invariant of the chain failed (stops the experiment: it is a bug)."""


_DEADLINE = [None]


def set_deadline(t):
    _DEADLINE[0] = t


def tick():
    d = _DEADLINE[0]
    if d is not None and time.time() > d:
        raise Timeout()


# ---------------------------------------------------------------------------------------------------------
# Integer Hungarian (maximum weight perfect assignment), exact int64
# ---------------------------------------------------------------------------------------------------------

def max_assignment(M):
    """Maximum of sum M[i, s(i)] over permutations s. M: square int64 matrix; forbidden cells hold NEG."""
    M = np.asarray(M, dtype=np.int64)
    n = M.shape[0]
    if n == 0:
        return 0
    assert np.abs(M[M > NEG // 2]).max(initial=0) < ENTRY_LIMIT, "entry too large for the int64 Hungarian"
    a = -M
    u = np.zeros(n + 1, dtype=np.int64)
    v = np.zeros(n + 1, dtype=np.int64)
    p = np.zeros(n + 1, dtype=np.int64)
    way = np.zeros(n + 1, dtype=np.int64)
    for i in range(1, n + 1):
        p[0] = i
        j0 = 0
        minv = np.full(n + 1, INF64, dtype=np.int64)
        used = np.zeros(n + 1, dtype=bool)
        while True:
            used[j0] = True
            i0 = p[j0]
            cur = a[i0 - 1, :] - u[i0] - v[1:]
            free = ~used[1:]
            upd = free & (cur < minv[1:])
            minv[1:][upd] = cur[upd]
            way[1:][upd] = j0
            cand = np.where(free, minv[1:], INF64)
            j1 = int(np.argmin(cand)) + 1
            delta = cand[j1 - 1]
            uj = np.where(used)[0]
            u[p[uj]] += delta
            v[uj] -= delta
            minv[1:][free] -= delta
            j0 = j1
            if p[j0] == 0:
                break
        while True:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
            if j0 == 0:
                break
    total = 0
    for j in range(1, n + 1):
        total += int(M[p[j] - 1, j - 1])
    return total


# ---------------------------------------------------------------------------------------------------------
# Bound tables (M4)
# ---------------------------------------------------------------------------------------------------------

def x_range(xi, split, K=KMAX):
    return range(-K, K + 1) if xi == split else range(0, K + 1)


def weight_keys(vs, split, K=KMAX):
    return itertools.product(*[x_range(i, split, K) for i in vs])


class Bd:
    """B_h(w) for every weight w of W(vs): components 0..K, the split variable -K..K. Variables outside vs: weight 0."""
    __slots__ = ("vs", "tab")

    def __init__(self, vs, tab):
        self.vs = tuple(vs)
        self.tab = tab

    def at(self, w):
        return self.tab[tuple(w[i] for i in self.vs)]

    def axis(self, xi, s):
        """B at the weight s e_x."""
        if xi not in self.vs:
            return self.tab[tuple(0 for _ in self.vs)]
        return self.tab[tuple(s if i == xi else 0 for i in self.vs)]

    def deg(self, xi):
        """Proven upper bound of the x-degree: B(e_x)."""
        if xi not in self.vs:
            return 0
        return self.axis(xi, 1)

    def low(self, xi):
        """Proven lower bound of the x-order: -B(-e_x) (x must be the split variable)."""
        if xi not in self.vs:
            return 0
        return -self.axis(xi, -1)

    def line(self, w, xi, xr):
        """B(w + s e_x) for s in xr, as an int64 array (w has any x component, ignored)."""
        if xi not in self.vs:
            val = self.tab[tuple(w[i] for i in self.vs)]
            return np.full(len(xr), val, dtype=np.int64)
        key = [w[i] for i in self.vs]
        j = self.vs.index(xi)
        out = np.empty(len(xr), dtype=np.int64)
        for t, s in enumerate(xr):
            key[j] = s
            out[t] = self.tab[tuple(key)]
        return out


def exact_bound(support, n, split, K=KMAX):
    """B(w) = max over the exact support of w.a (inputs and exact levels). support: list of exponent tuples."""
    sup = np.array(list(support), dtype=np.int64).reshape(-1, n)
    vs = tuple(i for i in range(n) if sup.shape[0] and sup[:, i].any())
    if not vs:
        return Bd((), {(): 0})
    keys = list(weight_keys(vs, split, K))
    A = sup[:, list(vs)]
    tab = {}
    for c0 in range(0, len(keys), 256):
        chunk = np.array(keys[c0:c0 + 256], dtype=np.int64)
        vals = (chunk @ A.T).max(axis=1)
        for k, val in zip(keys[c0:c0 + 256], vals):
            tab[k] = int(val)
    return Bd(vs, tab)


def normalize(B, split, K=KMAX):
    """B(w) <- min(B(w), floor(B(k w) / k)) for k = 2, 3 when k w is in W (one pass over the old table)."""
    old = B.tab
    new = {}
    for key, val in old.items():
        best = val
        for k in (2, 3):
            kk = tuple(k * c for c in key)
            ok = all((-K <= c <= K) if i == split else (0 <= c <= K) for i, c in zip(B.vs, kk))
            if ok:
                cand = old[kk] // k
                if cand < best:
                    best = cand
        new[key] = best
    return Bd(B.vs, new)


def formal_degree(B, xi, split, K=KMAX):
    """(m, zeros): m = largest c <= B(e_x) whose coefficient is not proven zero; zeros[c] True if e_c(0) < 0."""
    Bx = B.deg(xi)
    xr = list(x_range(xi, split, K))
    ax = [B.axis(xi, s) for s in xr]
    zeros = []
    for c in range(Bx + 1):
        e0 = min(a - s * c for a, s in zip(ax, xr))
        zeros.append(e0 < 0)
    m = max((c for c in range(Bx + 1) if not zeros[c]), default=-1)
    return m, zeros


def entry_vector(B, xi, w, xr_arr, m, zeros):
    """e_c(w) for c = 0..m (NEG where the coefficient is proven zero)."""
    bs = B.line(w, xi, list(xr_arr))
    cs = np.arange(m + 1, dtype=np.int64)
    vals = bs[:, None] - xr_arr[:, None] * cs[None, :]
    e = vals.min(axis=0)
    for c in range(m + 1):
        if zeros[c]:
            e[c] = NEG
    return e


def sylvester_entries(ef, eg):
    """Banded Sylvester entry-bound matrix: n rows of f (degree m), m rows of g (degree n)."""
    m, n = len(ef) - 1, len(eg) - 1
    N = m + n
    M = np.full((N, N), NEG, dtype=np.int64)
    efr, egr = ef[::-1], eg[::-1]
    for i in range(n):
        M[i, i:i + m + 1] = efr
    for i in range(m):
        M[n + i, i:i + n + 1] = egr
    return M


def res_bound(Bf, mf, zf, Bg, ng, zg, xi, split, nvars, K=KMAX):
    """Bound table of Res_{x; mf, ng}(f, g) (M4). Returns None when the resultant is proven identically zero."""
    vs = tuple(sorted((set(Bf.vs) | set(Bg.vs)) - {xi}))
    xr_arr = np.array(list(x_range(xi, split, K)), dtype=np.int64)
    tab = {}
    memo = {}
    for key in weight_keys(vs, split, K):
        tick()
        w = [0] * nvars
        for i, c in zip(vs, key):
            w[i] = c
        ef = entry_vector(Bf, xi, w, xr_arr, mf, zf)
        eg = entry_vector(Bg, xi, w, xr_arr, ng, zg)
        mk = (ef.tobytes(), eg.tobytes())
        if mk in memo:
            val = memo[mk]
        else:
            val = max_assignment(sylvester_entries(ef, eg))
            memo[mk] = val
        if val < DEAD_BELOW:
            return None
        tab[key] = val
    zero = tuple(0 for _ in vs)
    if zero in tab:
        tab[zero] = 0  # a nonzero polynomial has w-degree 0 at w = 0
    return normalize(Bd(vs, tab), split, K)


def drop_var(B, xi, split, K=KMAX):
    """Bound table of a polynomial proven free of x: min over the x range."""
    if xi not in B.vs:
        return B
    vs = tuple(i for i in B.vs if i != xi)
    j = B.vs.index(xi)
    tab = {}
    for key in weight_keys(vs, split, K):
        best = None
        for s in x_range(xi, split, K):
            kk = list(key)
            kk.insert(j, s)
            val = B.tab[tuple(kk)]
            best = val if best is None or val < best else best
        tab[key] = best
    return Bd(vs, tab)


def bound_dominates(Bprop, Bex, split, K=KMAX):
    """True if Bprop(w) >= Bex(w) for every weight of W(Bprop.vs) (Bex lives on a subset of the variables)."""
    for key in weight_keys(Bprop.vs, split, K):
        w = {i: c for i, c in zip(Bprop.vs, key)}
        sub = tuple(w[i] for i in Bex.vs)
        if Bprop.tab[key] < Bex.tab[sub]:
            return False
    return True


# ---------------------------------------------------------------------------------------------------------
# Rings, exact objects, images
# ---------------------------------------------------------------------------------------------------------

class Prime:
    def __init__(self, p, r):
        self.p, self.r = p, r % p
        assert sum(c * pow(self.r, i, p) for i, c in enumerate(P_COEFFS)) % p == 0, "P(r) != 0 mod p"

    def __repr__(self):
        return f"Prime({self.p}, {self.r})"


class NodeRing:
    """Variables of a node, in elimination order; exact context (y first) and modular contexts."""

    def __init__(self, order):
        self.order = list(order)
        self.n = len(self.order)
        self.ex = fmpz_mpoly_ctx.get(["y"] + self.order, "lex")
        y = self.ex.gen(0)
        self.Pm = y**5 - y**4 + 3 * y**3 + 3 * y**2 + 26
        self._mod = {}

    def mod(self, p):
        if p not in self._mod:
            self._mod[p] = nmod_mpoly_ctx.get(self.order, modulus=p)
        return self._mod[p]

    def reduce(self, f):
        q, r = divmod(f, self.Pm)
        return r

    def from_vectors(self, terms):
        """terms: [(exponents over self.order, 5 integer coordinates)] -> exact polynomial (already reduced)."""
        d = {}
        for ex, cs in terms:
            for i, c in enumerate(cs):
                if c:
                    d[(i,) + tuple(ex)] = int(c)
        return self.ex.from_dict(d)


def support_of(f):
    return sorted({tuple(m[1:]) for m in f.monoms()})


def phi(ring, f, prime):
    """Image of an exact polynomial under y -> r mod p."""
    p, r = prime.p, prime.r
    acc = {}
    for mono, c in f.to_dict().items():
        key = tuple(mono[1:])
        acc[key] = (acc.get(key, 0) + int(c) * pow(r, mono[0], p)) % p
    return ring.mod(p).from_dict({k: v for k, v in acc.items() if v})


def lc_img(F, xi):
    d = F.degrees()[xi]
    dd = {}
    for mono, c in F.to_dict().items():
        if mono[xi] == d:
            m2 = list(mono)
            m2[xi] = 0
            dd[tuple(m2)] = c
    return F.context().from_dict(dd)


def res_image(F, G, xi, xname, m, p):
    """Image of Res_{x; m, n}(f, g) for phi f = F (x-degree m' <= m), phi g = G of x-degree n exactly (M5)."""
    n = G.degrees()[xi]
    mp = F.degrees()[xi]
    assert mp <= m, "image degree above the formal degree"
    R = F.resultant(G, xname)
    if mp < m:
        R = R * (lc_img(G, xi) ** (m - mp))
        if (n * (m - mp)) % 2:
            R = -R
    return R


def shift_down(F, xi, L):
    """Exact division of an image by x^L (every monomial must have x-exponent >= L)."""
    if L == 0:
        return F
    dd = {}
    for mono, c in F.to_dict().items():
        if mono[xi] < L:
            raise BoundViolation("division by x^L is not exact")
        m2 = list(mono)
        m2[xi] -= L
        dd[tuple(m2)] = c
    return F.context().from_dict(dd)


def univariate(F, xi):
    dd = {}
    for mono, c in F.to_dict().items():
        dd[mono[xi]] = c
    if not dd:
        return nmod_poly([0], F.context().modulus())
    return nmod_poly([dd.get(i, 0) for i in range(max(dd) + 1)], F.context().modulus())


def poly_digest(F, pts):
    """(terms, degrees, values at the given points): comparison key for the second implementation."""
    vals = [int(F(*pt)) for pt in pts]
    return {"terms": len(F), "degrees": [int(e) for e in F.degrees()], "eval": vals}


def digest_points(nvars, p):
    """Fixed evaluation points (deterministic) for digests."""
    pts = []
    for t in range(2):
        pts.append(tuple((1000003 * (t + 2) * (i + 3) + 12345 * t + 7) % p or 1 for i in range(nvars)))
    return pts


# ---------------------------------------------------------------------------------------------------------
# Members and the chain at a node (M5, M6)
# ---------------------------------------------------------------------------------------------------------

class Mem:
    __slots__ = ("id", "ex", "img", "B", "level")

    def __init__(self, id, ex, img, B, level):
        self.id, self.ex, self.img, self.B, self.level = id, ex, img, B, level


def is_constant_member(g, n):
    return all(g.B.deg(i) == 0 for i in range(n))


class ChainFail(Exception):
    def __init__(self, reason, level=0):
        super().__init__(reason)
        self.reason, self.level = reason, level


def chain_node(ring, inputs, split, prime, exact_levels=2, K=KMAX, log=None, pts=None):
    """Run the M5/M6 chain on exact inputs [(id, exact poly)]. Returns a dict:
    certified, record (JSON), exact (id -> exact poly of the exact levels), lcs, V (univariates), notes."""
    n = ring.n
    p = prime.p
    order = ring.order
    ctx = ring.mod(p)
    pts = pts or digest_points(n, p)
    rec = {"order": order, "inputs": [], "dropped_inputs": [],
           "steps": [], "last": None, "exact_levels": exact_levels, "members": {}}
    exact = {}
    lcs = []
    mem = []
    gate = {"g2_real_checked": 0, "g2_real_violations": 0, "g5_checked": 0, "g5_mismatches": 0}

    def note(mid, level, g, extra=None):
        d = {"level": level, "exact": g.ex is not None, "terms": len(g.img),
             "img_degrees": [int(e) for e in g.img.degrees()], "bound_deg": [g.B.deg(i) for i in range(n)],
             "digest": poly_digest(g.img, pts)}
        if extra:
            d.update(extra)
        rec["members"][mid] = d

    for mid, ex in inputs:
        img = phi(ring, ex, prime)
        if img == 0:
            rec["dropped_inputs"].append(mid)
            continue
        g = Mem(mid, ex, img, exact_bound(support_of(ex), n, split, K), 0)
        mem.append(g)
        rec["inputs"].append(mid)
        exact[mid] = ex
        note(mid, 0, g)

    level = 0
    for xi in range(n - 1):
        x = order[xi]
        act = [g for g in mem if g.B.deg(xi) > 0]
        if not act:
            continue
        cand = [g for g in act if g.img.degrees()[xi] == g.B.deg(xi)]
        if not cand:
            raise ChainFail(f"no pivot attains its bound at {x}", level + 1)
        order_pos = {id(g): i for i, g in enumerate(mem)}
        piv = min(cand, key=lambda g: (g.B.deg(xi), len(g.img), order_pos[id(g)]))
        ng, zg = formal_degree(piv.B, xi, split, K)
        if ng != piv.B.deg(xi) or zg[ng]:
            raise BoundViolation("pivot degree is not its attained bound")
        level += 1
        exact_level = level <= exact_levels
        if piv.ex is not None:
            lcs.append({"x": x, "xi": xi, "id": piv.id, "n": ng, "ex": piv.ex})
        step = {"x": x, "pivot": piv.id, "n": ng, "members": []}
        newmem = []
        k = 0
        for g in mem:
            tick()
            if g is piv:
                continue
            if g.B.deg(xi) == 0:
                newmem.append(g)
                continue
            mg, zf = formal_degree(g.B, xi, split, K)
            if mg == 0:
                B2 = drop_var(g.B, xi, split, K)
                newmem.append(Mem(g.id, g.ex, g.img, B2, g.level))
                step["members"].append({"id": g.id, "kind": "pass", "m": 0, "out": g.id})
                continue
            R_img = res_image(g.img, piv.img, xi, x, mg, p)
            oid = f"l{level}.{k}"
            k += 1
            Bp = res_bound(g.B, mg, zf, piv.B, ng, zg, xi, split, n, K)
            ex_res = None
            if exact_level and g.ex is not None and piv.ex is not None:
                ex_res = ring.reduce(g.ex.resultant(piv.ex, x))
                exact[oid] = ex_res
                gate["g5_checked"] += 1
                if phi(ring, ex_res, prime) != R_img:
                    gate["g5_mismatches"] += 1
                    raise BoundViolation(f"G5: phi(exact) != image at {oid}")
            if Bp is None:
                if ex_res is not None and ex_res != 0:
                    raise BoundViolation(f"bound says {oid} is zero, the exact resultant is not")
                if R_img != 0:
                    raise BoundViolation(f"bound says {oid} is zero, its image is not")
            if R_img == 0:
                step["members"].append({"id": g.id, "kind": "res", "m": mg, "out": None})
                rec["members"][oid] = {"level": level, "dropped": True, "reason": "image zero"}
                continue
            if ex_res is not None:
                Bx = exact_bound(support_of(ex_res), n, split, K)
                gate["g2_real_checked"] += 1
                if not bound_dominates(Bp, Bx, split, K):
                    gate["g2_real_violations"] += 1
                    raise BoundViolation(f"G2: propagated bound below the exact support at {oid}")
                newg = Mem(oid, ex_res, R_img, Bx, level)
            else:
                newg = Mem(oid, None, R_img, Bp, level)
            newmem.append(newg)
            step["members"].append({"id": g.id, "kind": "res", "m": mg, "out": oid})
            note(oid, level, newg, {"x": x, "m": mg, "n": ng})
        rec["steps"].append(step)
        mem = newmem

    # ---- last variable (M6) ----
    xi = n - 1
    x = order[xi]
    const = [g for g in mem if is_constant_member(g, n)]
    last = {"x": x, "members": [], "pivot": None, "pairs": [], "constant_member": None}
    out = {"certified": False, "record": rec, "exact": exact, "lcs": lcs, "V": [], "gate": gate}
    rec["last"] = last
    if const:
        last["constant_member"] = const[0].id
        rec["certified"] = True
        rec["witness"] = f"member {const[0].id} is a nonzero constant before the last variable"
        out["certified"] = True
        return out
    U = []
    for g in mem:
        if g.B.deg(xi) > 0:
            if any(g.B.deg(i) > 0 for i in range(xi)):
                raise BoundViolation(f"member {g.id} still depends on an eliminated variable")
            L = g.B.low(xi) if xi == split else 0
            if L < 0:
                raise BoundViolation("negative lower bound of the order")
            V = shift_down(g.img, xi, L)
            d = g.B.deg(xi) - L
            if V.degrees()[xi] > d:
                raise BoundViolation(f"image degree {V.degrees()[xi]} above the formal degree {d}")
            U.append({"id": g.id, "L": L, "d": d, "V": V, "mem": g,
                      "attained": V.degrees()[xi] == d})
            last["members"].append({"id": g.id, "L": L, "d": d, "img_deg": int(V.degrees()[xi]),
                                    "img_order": int(min(mo[xi] for mo in V.monoms()))})
    out["V"] = U
    cands = [u for u in U if u["attained"]]
    if not cands:
        rec["certified"] = False
        rec["reason"] = "no univariate attains its bound"
        raise ChainFail("no univariate attains its bound", level + 1)
    ub = min(cands, key=lambda u: (u["d"], len(u["V"]), U.index(u)))
    last["pivot"] = ub["id"]
    nn = ub["d"]
    last["n"] = nn
    nz = 0
    for u in U:
        if u is ub:
            continue
        if u["d"] == 0:
            # a nonzero constant of L (the image of a member that survived is nonzero)
            c = int(u["V"].to_dict()[tuple(0 for _ in range(n))])
            last["pairs"].append({"i": u["id"], "m": 0, "n": nn, "constant": True, "c": c})
            nz += 1
            continue
        Cimg = res_image(u["V"], ub["V"], xi, x, u["d"], p)
        c = 0
        if Cimg != 0:
            dct = Cimg.to_dict()
            assert set(dct) == {tuple(0 for _ in range(n))}, "final resultant is not a constant"
            c = int(dct[tuple(0 for _ in range(n))])
            nz += 1
        last["pairs"].append({"i": u["id"], "m": u["d"], "n": nn, "constant": False, "c": c})
    rec["certified"] = nz > 0
    out["certified"] = nz > 0
    rec["nonzero_constants"] = nz
    rec["pairs_total"] = len(U) - 1
    return out


# ---------------------------------------------------------------------------------------------------------
# Tree (M7)
# ---------------------------------------------------------------------------------------------------------

def exact_transform(ring, ring2, f, a_vec, b_vec, vi):
    """b^(deg_v f) f((w - a)/b) in ring2 (order without v, then w), exact over Z[y]/(P)."""
    ctx = ring2.ex
    y = ctx.gen(0)
    wgen = ctx.gen(ring2.n)

    def poly_y(vec):
        s = ctx.from_dict({})
        for i, c in enumerate(vec):
            if c:
                s = s + int(c) * y**i
        return s

    A = wgen - poly_y(a_vec)
    B = poly_y(b_vec)
    byk = {}
    for mono, c in f.to_dict().items():
        k = mono[1 + vi]
        nm = [mono[0]] + [mono[1 + j] for j in range(ring.n) if j != vi] + [0]
        byk.setdefault(k, {})[tuple(nm)] = c
    d = max(byk)
    Apow = [ctx.from_dict({(0,) * (ring2.n + 1): 1})]
    Bpow = [Apow[0]]
    for _ in range(d):
        Apow.append(ring2.reduce(Apow[-1] * A))
        Bpow.append(ring2.reduce(Bpow[-1] * B))
    total = ctx.from_dict({})
    for k, dct in byk.items():
        fk = ctx.from_dict(dct)
        total = total + ring2.reduce(ring2.reduce(fk * Apow[k]) * Bpow[d - k])
    return ring2.reduce(total)


def project_w0(ring2, ring3, f):
    """Set the last variable (w) of ring2 to 0 and drop it: ring3 has the order without w."""
    dd = {}
    for mono, c in f.to_dict().items():
        if mono[-1] == 0:
            dd[tuple(mono[:-1])] = c
    return ring3.ex.from_dict(dd)


def y_vector(dct, ey_len=5):
    v = [0] * ey_len
    for ey, c in dct.items():
        v[ey] = int(c)
    return v


def find_split(ring, lcs, V, prime):
    """M7: the first pivot (elimination order) whose exact leading coefficient is a + b v (v the last variable),
    b != 0, whose image root is a root of the gcd of the images of the V_i."""
    p = prime.p
    xi = ring.n - 1
    us = [univariate(u["V"], xi) for u in V]
    if not us:
        return None, "no univariate members", {}
    gg = us[0]
    for u in us[1:]:
        gg = gg.gcd(u)
    info = {"gcd_degree": int(gg.degree()),
            "gcd_factors": sorted((int(f.degree()), int(e)) for f, e in gg.factor()[1]) if gg.degree() > 0 else []}
    if gg.degree() <= 0:
        return None, "gcd of the univariates is trivial but no constant is nonzero", info
    roots = {int(rt) for rt, _ in gg.roots()}
    for item in lcs:
        n_ = item["n"]
        terms = {}
        for mono, c in item["ex"].to_dict().items():
            if mono[1 + item["xi"]] == n_:
                m2 = list(mono)
                m2[1 + item["xi"]] = 0
                terms[tuple(m2)] = c
        a, b, ok = {}, {}, True
        for key, c in terms.items():
            ey, rest = key[0], key[1:]
            if all(e == 0 for e in rest):
                a[ey] = c
            elif rest == tuple(1 if i == xi else 0 for i in range(ring.n)):
                b[ey] = c
            else:
                ok = False
                break
        if not ok or not b:
            continue
        av, bv = y_vector(a), y_vector(b)
        pa = sum(c * pow(prime.r, i, p) for i, c in enumerate(av)) % p
        pb = sum(c * pow(prime.r, i, p) for i, c in enumerate(bv)) % p
        if pb == 0:
            continue
        root = (-pa * pow(pb, -1, p)) % p
        if root not in roots:
            continue
        return {"x": item["x"], "pivot": item["id"], "a": av, "b": bv, "v": ring.order[xi], "root": root}, None, info
    return None, "no pivot leading coefficient a + b v matches a root of the gcd", info


class TreeState:
    def __init__(self):
        self.records = []
        self.nodes = {}   # node id -> {"ring", "inputs": {id: exact}, "exact": {id: exact}}
        self.counter = 0


def solve_tree(order, inputs, prime, max_depth=4, node_seconds=1800, K=KMAX, log=print, deadline=None,
               exact_levels=2, tag="t"):
    """Build the certificate tree for exact inputs [(id, poly in NodeRing(order).ex)]. Returns (certified, TreeState).
    certified is True only when every leaf is certified. UNKNOWN nodes make it False."""
    st = TreeState()
    ring0 = NodeRing(order)

    def solve(nid, parent, kind, ring, ins, split_name, depth, transform):
        split = None if split_name is None else ring.order.index(split_name)
        t0 = time.time()
        end = t0 + node_seconds
        if deadline is not None:
            end = min(end, deadline)
        set_deadline(end)
        res = None
        fallback = False
        rec = None
        err = None
        for el in (exact_levels, exact_levels + 1):
            try:
                res = chain_node(ring, ins, split, prime, exact_levels=el, K=K)
                err = None
                fallback = el != exact_levels
                break
            except ChainFail as e:
                err = ("fail", e.reason, e.level)
                if e.level >= 3 and el == exact_levels:
                    continue
                break
            except Timeout:
                err = ("timeout", "node time allowance exceeded", 0)
                break
        base = {"id": nid, "parent": parent, "kind": kind, "depth": depth, "order": ring.order,
                "split_var": split_name, "transform": transform}
        if res is None:
            base.update({"status": "unknown", "reason": err[1], "seconds": round(time.time() - t0, 2),
                         "inputs": [i for i, _ in ins]})
            st.records.append(base)
            st.nodes[nid] = {"ring": ring, "inputs": dict(ins), "exact": {}}
            log(f"[{nid}] UNKNOWN: {err[1]}")
            return False
        rec = res["record"]
        base.update(rec)
        base["fallback_exact_level3"] = fallback
        base["gate"] = res["gate"]
        base["seconds"] = round(time.time() - t0, 2)
        st.records.append(base)
        st.nodes[nid] = {"ring": ring, "inputs": dict(ins), "exact": res["exact"]}
        if res["certified"]:
            base["status"] = "certified"
            log(f"[{nid}] certified ({rec.get('nonzero_constants', 'const')} nonzero of "
                f"{rec.get('pairs_total', 0)}) in {base['seconds']} s")
            return True
        sp_, why, *info = find_split(ring, res["lcs"], res["V"], prime)
        if info:
            base["gcd"] = info[0]
        if sp_ is None:
            base["status"] = "unknown"
            base["reason"] = why
            log(f"[{nid}] UNKNOWN: {why}")
            return False
        if depth >= max_depth:
            base["status"] = "unknown"
            base["reason"] = "depth limit"
            log(f"[{nid}] UNKNOWN: depth limit")
            return False
        st.counter += 1
        wname = f"w{depth + 1}"
        base["status"] = "split"
        base["split"] = {"w": wname, **sp_}
        log(f"[{nid}] split on {sp_['x']}-pivot leading coefficient (a + b {sp_['v']}), gcd {info[0]}")
        vi = ring.order.index(sp_["v"])
        order2 = [u for u in ring.order if u != sp_["v"]] + [wname]
        ring2 = NodeRing(order2)
        ins2 = []
        for mid, ex in ins:
            ins2.append((mid, exact_transform(ring, ring2, ex, sp_["a"], sp_["b"], vi)))
        ring3 = NodeRing(order2[:-1])
        ins3, dropped3 = [], []
        for mid, ex in ins2:
            f3 = project_w0(ring2, ring3, ex)
            if f3 == 0:
                dropped3.append(mid)
            else:
                ins3.append((mid, f3))
        base["child_zero_dropped_inputs"] = dropped3
        okA = solve(nid + ".nz", nid, "w!=0", ring2, ins2, wname, depth + 1,
                    {"v": sp_["v"], "w": wname, "a": sp_["a"], "b": sp_["b"]})
        okB = solve(nid + ".z", nid, "w=0", ring3, ins3, None, depth + 1,
                    {"v": sp_["v"], "w": wname, "a": sp_["a"], "b": sp_["b"], "set_w_zero": True})
        return okA and okB

    ok = solve(tag, None, "root", ring0, inputs, None, 0, None)
    return ok, st


# ---------------------------------------------------------------------------------------------------------
# Replay of a recorded leaf at another prime (M8)
# ---------------------------------------------------------------------------------------------------------

def replay_leaf(state, rec, prime):
    """Evaluate the recorded SLP of a certified leaf at `prime`; returns {"certified", "constants", "problems"}."""
    node = state.nodes[rec["id"]]
    ring = node["ring"]
    n = ring.n
    p = prime.p
    problems = []
    img = {}
    for mid in rec["inputs"]:
        img[mid] = phi(ring, node["inputs"][mid], prime)
    # inputs dropped at the recording prime are not used by the certificate; an input that is zero here is absent
    for mid in list(img):
        if img[mid] == 0:
            del img[mid]
    exact_checked = 0
    for step in rec["steps"]:
        xi = ring.order.index(step["x"])
        piv = img.get(step["pivot"])
        if piv is None:
            problems.append(f"pivot {step['pivot']} is zero at the second prime")
            continue
        if piv.degrees()[xi] != step["n"]:
            problems.append(f"pivot {step['pivot']} loses its degree at the second prime")
            continue
        for e in step["members"]:
            if e["kind"] == "pass":
                continue
            f = img.get(e["id"])
            if e["out"] is None:
                continue
            if f is None:
                problems.append(f"{e['id']} is zero at the second prime (needed for {e['out']})")
                continue
            R = res_image(f, piv, xi, step["x"], e["m"], p)
            ex = node["exact"].get(e["out"])
            if ex is not None:
                exact_checked += 1
                if phi(ring, ex, prime) != R:
                    problems.append(f"phi(exact) differs from the chain at {e['out']}")
            if R == 0:
                problems.append(f"{e['out']} is zero at the second prime")
                continue
            img[e["out"]] = R
    last = rec["last"]
    consts = []
    if last["constant_member"] is not None:
        f = img.get(last["constant_member"])
        consts.append({"i": last["constant_member"], "constant": True, "nonzero": f is not None and f != 0})
    else:
        xi = n - 1
        Vimg = {}
        for u in last["members"]:
            f = img.get(u["id"])
            if f is None:
                continue
            Vimg[u["id"]] = shift_down(f, xi, u["L"])
        pv = Vimg.get(last["pivot"])
        if pv is None or pv.degrees()[xi] != last["n"]:
            problems.append("the final pivot loses its degree or vanishes at the second prime")
        else:
            for pr in last["pairs"]:
                f = Vimg.get(pr["i"])
                if f is None:
                    consts.append({"i": pr["i"], "nonzero": False, "missing": True})
                    continue
                if pr["constant"]:
                    consts.append({"i": pr["i"], "constant": True, "nonzero": f != 0})
                    continue
                if f.degrees()[xi] > pr["m"]:
                    problems.append("image degree above the formal degree at the second prime")
                    continue
                C = res_image(f, pv, xi, last["x"], pr["m"], p)
                cval = int(C.to_dict().get(tuple(0 for _ in range(n)), 0)) if C != 0 else 0
                consts.append({"i": pr["i"], "nonzero": C != 0, "c": cval})
    certified = any(c.get("nonzero") for c in consts)
    return {"certified": certified, "constants": consts, "problems": problems, "exact_checked": exact_checked}
