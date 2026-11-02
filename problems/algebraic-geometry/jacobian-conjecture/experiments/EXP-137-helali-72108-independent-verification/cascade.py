"""EXP-137: layer-by-layer exact cascade of [P,Q] = x^2 over the degree-35 field (own code).

Layer k (bracket band k, k <= 3) is linear in the new unknowns: Q band k-1 (partner A, the band-2 part of P)
and P band k-2 (partner D, the band-3 part of Q); every other product is already known. Rows are the
t-degrees; rref over K gives pivots, new free parameters and compatibility equations.
"""

from __future__ import annotations


import sympy as sp
from flint import fmpq, fmpq_poly

import exp137_lib as L

NVAR = 12  # maximum number of free parameters carried


def build_field(lex: dict, log=print):
    """From the lex basis text of P2: the field K=Q[u]/(H), a2..a7 in K, D in K. Returns (F, A, D)."""
    a = {i: sp.Symbol(f"a{i}") for i in range(2, 8)}
    u = a[7]

    def qp(expr):
        p = sp.Poly(expr, u, domain=sp.QQ)
        co = [fmpq(0)] * (p.degree() + 1)
        for (i,), c in p.terms():
            c = sp.Rational(c)
            co[i] = fmpq(int(c.p), int(c.q))
        return fmpq_poly(co)

    loc = {f"a{k}": a[k] for k in a}
    H = qp(sp.sympify(lex[1].replace("^", "**"), locals=loc))
    H = H / H[H.degree()]
    F = L.NF(H)  # raises unless irreducible over Q
    log(f"field: degree {F.deg}, minimal polynomial irreducible over Q (checked by flint factor)")
    val = {7: F.gen()}
    for i in sorted(lex):
        if i == 1:
            continue
        e = sp.sympify(lex[i].replace("^", "**"), locals=loc)
        (var,) = sorted(e.free_symbols - {u}, key=str)
        c = sp.Poly(e, var).coeff_monomial(var)
        rest = sp.expand(-(e - c * var) / c)
        k = int(str(var)[1:])
        val[k] = F.el(qp(rest))
    assert sorted(val) == [2, 3, 4, 5, 6, 7]
    A = [F.el(0) for _ in range(9)]
    A[1], A[8] = F.el(1), F.el(1)
    for i in range(2, 8):
        A[i] = val[i]
    return F, A, val


def solve_D(F, A):
    """D from J4 by the triangular solve in K, then exact check of every J4 coefficient. Returns D list (index = t-degree)."""
    D = [F.el(0) for _ in range(13)]
    for k in range(2, 13):
        # coefficient of t^k in 2AD' - 3A'D - t^2 : sum_{i+j-1=k} (2j-3i) A_i D_j, unknown D_k has A_1: (2k-3)
        s = F.el(0)
        for i in range(1, 9):
            j = k + 1 - i
            if 2 <= j <= 12 and j != k:
                s = s + A[i] * D[j] * (2 * j - 3 * i)
        if k == 2:
            s = s - 1
        D[k] = (-s) / (2 * k - 3)
    resid = []
    for k in range(0, 20):
        s = F.el(0)
        for i in range(1, 9):
            j = k + 1 - i
            if 2 <= j <= 12:
                s = s + A[i] * D[j] * (2 * j - 3 * i)
        if k == 2:
            s = s - 1
        resid.append(bool(s))
    return D, resid


class Cascade:
    def __init__(self, F, A, D, ppts, qpts):
        self.F = F
        self.ppts, self.qpts = ppts, qpts
        self.P = {}  # (band, a) -> MP
        self.Q = {}
        self.nparams = 0
        self.compat = []  # (layer, MP)
        self.layers = []
        one = MP_const(F, 1)
        for i in range(1, 9):
            self.P[(2, i)] = MP_const(F, A[i])
        for j in range(2, 13):
            self.Q[(3, j)] = MP_const(F, D[j])
        self.normalized = {(0, 8): one}  # vertex (8,16): P band 0, t^8, scaled to 1
        for key, v in self.normalized.items():
            self.P[key] = v

    def _pts(self, pts, band):
        return [(i, j) for (i, j) in pts if L.band_of((i, j)) == band and (i, j) != (0, 0)]

    def layer(self, k, log=print):
        F = self.F
        unknowns = []
        for (i, j) in self._pts(self.ppts, k - 2):
            if (k - 2, i) not in self.P:
                unknowns.append(("P", k - 2, i))
        for (i, j) in self._pts(self.qpts, k - 1):
            if (k - 1, i) not in self.Q:
                unknowns.append(("Q", k - 1, i))
        # all contributing pairs
        rows_by_m: dict = {}
        const_by_m: dict = {}
        ucol = {u: n for n, u in enumerate(unknowns)}
        # known coefficient lookup
        def getP(p, a):
            return self.P.get((p, a))

        def getQ(q, c):
            return self.Q.get((q, c))

        pb = {L.band_of(pt) for pt in self.ppts}
        qb = {L.band_of(pt) for pt in self.qpts}
        for p in pb:
            q = k + 1 - p
            if q not in qb:
                continue
            for (i, j) in self._pts(self.ppts, p):
                for (kk, ll) in self._pts(self.qpts, q):
                    a, c = i, kk
                    w = p * c - a * q
                    if w == 0:
                        continue
                    m = a + c - 1
                    pv, qv = getP(p, a), getQ(q, c)
                    up, uq = ("P", p, a) in ucol, ("Q", q, c) in ucol
                    if up and uq:
                        raise RuntimeError("unknown times unknown inside one layer")
                    if up or uq:
                        known = qv if up else pv
                        if known is None:
                            raise RuntimeError("partner of an unknown is unknown")
                        assert known.is_const()
                        coef = next(iter(known.d.values())) if known.d else F.el(0)
                        col = ucol[("P", p, a)] if up else ucol[("Q", q, c)]
                        row = rows_by_m.setdefault(m, {})
                        row[col] = row.get(col, F.el(0)) + coef * w
                    else:
                        if pv is None or qv is None:
                            raise RuntimeError(f"missing known coefficient in layer {k}: P{(p, a)} or Q{(q, c)}")
                        const_by_m[m] = const_by_m.get(m, MP_zero(F)) + (pv * qv).scale(w)
        ms = sorted(set(rows_by_m) | set(const_by_m))
        nU = len(unknowns)
        rows = [[rows_by_m.get(m, {}).get(c, F.el(0)) for c in range(nU)] for m in ms]
        rhs = [-(const_by_m.get(m, MP_zero(F))) for m in ms]
        info = {"layer": k, "unknowns": nU, "rows": len(ms)}
        if nU == 0:
            comp = [r for r in (-x for x in rhs) if r]
            for cpoly in rhs:
                if cpoly:
                    self.compat.append((k, cpoly))
            info.update(rank=0, new_params=0, compat=sum(1 for x in rhs if x))
            self.layers.append(info)
            return info
        R, Y, piv, free, compat = L.rref(F, rows, rhs) if rows and nU else ([], [], [], [], [])
        newp = {}
        for f in free:
            if self.nparams >= NVAR:
                raise RuntimeError("too many parameters")
            newp[f] = MP_var(F, self.nparams)
            self.nparams += 1
        for r_i, pc in enumerate(piv):
            val = Y[r_i]
            for f in free:
                if R[r_i][f]:
                    val = val - newp[f].scale(R[r_i][f])
            kind, band, a = unknowns[pc]
            (self.P if kind == "P" else self.Q)[(band, a)] = val
        for f in free:
            kind, band, a = unknowns[f]
            (self.P if kind == "P" else self.Q)[(band, a)] = newp[f]
        for cpoly in compat:
            self.compat.append((k, cpoly))
        info.update(rank=len(piv), new_params=len(free), compat=len(compat))
        self.layers.append(info)
        return info

    def bands_only_compat(self, k):
        """Layers with no unknowns left: compat = all coefficients of the band (no unknown column)."""
        return self.layer(k)


def MP_const(F, c):
    return L.MP.const(F, NVAR, c)


def MP_zero(F):
    return L.MP(F, NVAR)


def MP_var(F, i):
    return L.MP.var(F, NVAR, i)


def sing_field_decl(F, nparams, names=None):
    names = names or [f"p{i}" for i in range(nparams)]
    return names


def kel_to_sing(c, uname="u"):
    parts = []
    for i in range(len(c.p)):
        co = c.p[i]
        if co == 0:
            continue
        num, den = int(co.p), int(co.q)
        cs = f"({num}/{den})" if den != 1 else f"({num})"
        parts.append(cs if i == 0 else f"{cs}*{uname}^{i}")
    return "+".join(parts) if parts else "0"


def mp_to_sing(poly, names):
    terms = []
    for mon, c in sorted(poly.d.items(), key=lambda x: (sum(x[0]), x[0]), reverse=True):
        facs = [f"{names[i]}^{e}" if e > 1 else names[i] for i, e in enumerate(mon) if e]
        cs = kel_to_sing(c)
        terms.append(f"({cs})" + ("*" + "*".join(facs) if facs else ""))
    return "+".join(terms) if terms else "0"


def singular_unit_script(F, polys, nparams, tag, minpoly_note=""):
    names = [f"p{i}" for i in range(nparams)]
    mp = kel_to_sing(F.el(F.m)).replace("(", "(").replace("u", "u")
    # the minimal polynomial itself (not reduced mod itself)
    parts = []
    for i in range(F.m.degree() + 1):
        co = F.m[i]
        if co == 0:
            continue
        num, den = int(co.p), int(co.q)
        cs = f"({num}/{den})" if den != 1 else f"({num})"
        parts.append(cs if i == 0 else f"{cs}*u^{i}")
    minp = "+".join(parts)
    gens = ",\n".join(mp_to_sing(p, names) for p in polys)
    return f"""LIB "nfmodstd.lib";
short=0;
ring R=(0,u),({','.join(names)}),dp;
minpoly={minp};
option(redSB);
ideal I=
{gens};
"INPUT_SIZE="+string(size(I));
int t0=timer;
ideal J=std(I);
"STD_SIZE="+string(size(J));
"STD_TIME_SECONDS="+string(timer-t0);
if(size(J)==1 && deg(J[1])==0){{ "UNIT"; }} else {{ "NONUNIT"; "DIM="+string(dim(J)); }}
quit;
"""
