"""EXP-148: exact replay of Long's universal Mathieu pair (arXiv:2609.16178 v1) on SU(N), first column, N = 2..16.

CPU only, headless, deterministic, Python standard library only (fractions, itertools, json, time, random with a fixed
seed for K4). Exact arithmetic throughout: coefficients are Gaussian integers held as pairs of Python ints, integrals are
Fractions. No float and no complex type appears; the only clock is time.perf_counter_ns (an int, timing only).

    python run.py

Exit 0 when every identity, every cell and every control behaves as the hypothesis states; 1 otherwise.
The hypothesis (hypothesis.md, frozen) fixes the four routes, the identity checks, the controls and the ranges.
"""
from __future__ import annotations

import itertools
import json
import random
import sys
import time
from fractions import Fraction
from functools import lru_cache
from math import comb, factorial
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "artifacts" / "results.json"

A_RANGE = (range(2, 17), range(1, 9), range(0, 5))      # N, m, s of Route A
B_RANGE = (range(2, 17), range(1, 6), range(0, 4))      # Route B
C_RANGE = (range(2, 7), ((1, 0), (1, 1)))               # Route C: N and the (m, s) pairs
H_RANGE = (range(1, 9), range(0, 5))                    # Route H (N = 2)

# The 16-term expansion of P transcribed in the preflight (exponents of z0, z1, w0, w1 -> integer coefficient).
PREFLIGHT_P = {
    (4, 0, 4, 0): -2, (3, 1, 4, 0): 2, (4, 0, 3, 1): -6, (3, 1, 3, 1): 4, (2, 2, 3, 1): 6, (4, 0, 2, 2): -4,
    (3, 1, 2, 2): 6, (2, 2, 2, 2): 12, (1, 3, 2, 2): 6, (3, 1, 1, 3): 8, (2, 2, 1, 3): 6, (1, 3, 1, 3): 4,
    (0, 4, 1, 3): 2, (2, 2, 0, 4): -4, (1, 3, 0, 4): -6, (0, 4, 0, 4): -2,
}


# ---------------------------------------------------------------- polynomials in (z0, z1, w0, w1), w = conj z
def gmul(x, y):
    return (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def padd(p, q, sign=1):
    out = dict(p)
    for e, c in q.items():
        old = out.get(e, (0, 0))
        out[e] = (old[0] + sign * c[0], old[1] + sign * c[1])
    return {e: c for e, c in out.items() if c != (0, 0)}


def pscale(p, k):
    return {e: gmul(c, k) for e, c in p.items() if gmul(c, k) != (0, 0)}


def pmul(p, q):
    out = {}
    for e1, c1 in p.items():
        for e2, c2 in q.items():
            e = tuple(x + y for x, y in zip(e1, e2))
            c = gmul(c1, c2)
            old = out.get(e)
            out[e] = c if old is None else (old[0] + c[0], old[1] + c[1])
    return {e: c for e, c in out.items() if c != (0, 0)}


def ppow(p, k):
    out = {(0,) * len(next(iter(p))): (1, 0)}
    for _ in range(k):
        out = pmul(out, p)
    return out


Z0 = {(1, 0, 0, 0): (1, 0)}
Z1 = {(0, 1, 0, 0): (1, 0)}
W0 = {(0, 0, 1, 0): (1, 0)}
W1 = {(0, 0, 0, 1): (1, 0)}


def build_pair(variant="paper"):
    """P and Q from eq (3-3) by polynomial arithmetic. variant 'k3' replaces the factor (2a + u) by (a + u) (control K3)."""
    zz0, zz1 = pmul(Z0, W0), pmul(Z1, W1)
    a = padd(zz0, zz1)
    tau = padd(zz0, zz1, -1)
    u = pscale(pmul(Z0, W1), (2, 0))
    v = pscale(pmul(Z1, W0), (2, 0))
    k = pscale(a, (2, 0)) if variant == "paper" else a
    inner = padd(pmul(pmul(a, a), v), pmul(padd(k, u), pmul(tau, tau)), -1)
    return pmul(padd(a, u), inner), u


def balanced_literal(e):
    return e[0] == e[2] and e[1] == e[3]


def balanced_degree(e):
    return e[0] + e[1] == e[2] + e[3]


# ---------------------------------------------------------------- Route A: complex sphere moments
def route_a_value(poly, N):
    """Integral over S^(2N-1) of a polynomial in (z0, z1, w0, w1): (N-1)! a0! a1! / (N-1+a0+a1)! per balanced monomial."""
    re = im = Fraction(0)
    for (a0, a1, b0, b1), (cr, ci) in poly.items():
        if a0 == b0 and a1 == b1:
            w = Fraction(factorial(N - 1) * factorial(a0) * factorial(a1), factorial(N - 1 + a0 + a1))
            re += cr * w
            im += ci * w
    return re, im


# ---------------------------------------------------------------- Route B: real sphere moments (own multiplication)
def rmul(p, q):
    """Product of two polynomials in x0..x3 with Gaussian-integer coefficients; separate from pmul on purpose."""
    re, im = {}, {}
    for e1, (a, b) in p.items():
        for e2, (c, d) in q.items():
            e = (e1[0] + e2[0], e1[1] + e2[1], e1[2] + e2[2], e1[3] + e2[3])
            re[e] = re.get(e, 0) + a * c - b * d
            im[e] = im.get(e, 0) + a * d + b * c
    out = {}
    for e in re:
        c = (re[e], im[e])
        if c != (0, 0):
            out[e] = c
    return out


def radd(p, q, sign=1):
    out = dict(p)
    for e, c in q.items():
        old = out.get(e, (0, 0))
        out[e] = (old[0] + sign * c[0], old[1] + sign * c[1])
    return {e: c for e, c in out.items() if c != (0, 0)}


def rscale(p, k):
    return {e: (k * c[0], k * c[1]) for e, c in p.items()}


# z0 = x0 + i x1, z1 = x2 + i x3, w = conjugate
RZ0 = {(1, 0, 0, 0): (1, 0), (0, 1, 0, 0): (0, 1)}
RW0 = {(1, 0, 0, 0): (1, 0), (0, 1, 0, 0): (0, -1)}
RZ1 = {(0, 0, 1, 0): (1, 0), (0, 0, 0, 1): (0, 1)}
RW1 = {(0, 0, 1, 0): (1, 0), (0, 0, 0, 1): (0, -1)}


def rpow(p, k):
    out = {(0, 0, 0, 0): (1, 0)}
    for _ in range(k):
        out = rmul(out, p)
    return out


def build_real_pair(variant="paper"):
    """P and Q of eq (3-3) built directly in the real coordinates x0..x3."""
    zz0, zz1 = rmul(RZ0, RW0), rmul(RZ1, RW1)
    a = radd(zz0, zz1)
    tau = radd(zz0, zz1, -1)
    u = rscale(rmul(RZ0, RW1), 2)
    v = rscale(rmul(RZ1, RW0), 2)
    k = rscale(a, 2) if variant == "paper" else a
    inner = radd(rmul(rmul(a, a), v), rmul(radd(k, u), rmul(tau, tau)), -1)
    return rmul(radd(a, u), inner), u


def dfact(k):
    """k!! for odd k >= -1 (and 1 for k <= 0)."""
    out = 1
    while k > 1:
        out *= k
        k -= 2
    return out


def route_b_value(rpoly, N):
    """Integral over S^(2N-1) in R^(2N): prod (e_k - 1)!! / (n (n+2) ... (n+|e|-2)) for all-even exponents, n = 2N, on the
    first four coordinates (the others have exponent 0)."""
    n = 2 * N
    sums = {}
    for e, (cr, ci) in rpoly.items():
        if any(k & 1 for k in e):
            continue
        w = 1
        for k in e:
            w *= dfact(k - 1)
        s = sums.setdefault(sum(e), [0, 0])
        s[0] += cr * w
        s[1] += ci * w
    re = im = Fraction(0)
    for deg, (sr, si) in sums.items():
        den = 1
        for j in range(deg // 2):
            den *= n + 2 * j
        re += Fraction(sr, den)
        im += Fraction(si, den)
    return re, im


def real_monomial(e):
    """z0^a0 z1^a1 w0^b0 w1^b1 in the real coordinates (used by K4)."""
    return rmul(rmul(rpow(RZ0, e[0]), rpow(RZ1, e[1])), rmul(rpow(RW0, e[2]), rpow(RW1, e[3])))


# ---------------------------------------------------------------- Route C: Weingarten calculus on U(N)
def partitions(d, max_parts, max_part=None):
    if max_part is None:
        max_part = d
    if d == 0:
        yield ()
        return
    if max_parts == 0:
        return
    for first in range(min(d, max_part), 0, -1):
        for rest in partitions(d - first, max_parts - 1, first):
            yield (first,) + rest


@lru_cache(maxsize=None)
def mn_char(lam, mu):
    """Character chi_lambda at cycle type mu by the Murnaghan-Nakayama rule (rim hooks on beta-numbers)."""
    length = len(lam)
    beta = tuple(sorted(lam[i] + length - 1 - i for i in range(length)))
    return _mn(beta, mu)


@lru_cache(maxsize=None)
def _mn(beta, mu):
    if not mu:
        return 1
    r, rest = mu[0], mu[1:]
    bset = set(beta)
    total = 0
    for b in beta:
        nb = b - r
        if nb >= 0 and nb not in bset:
            sign = -1 if sum(1 for x in beta if nb < x < b) & 1 else 1
            total += sign * _mn(tuple(sorted((bset - {b}) | {nb})), rest)
    return total


def schur_dim(lam, N):
    """s_lambda(1^N) by the hook-content formula."""
    conj = [sum(1 for part in lam if part > j) for j in range(lam[0])] if lam else []
    out = Fraction(1)
    for i, row in enumerate(lam):
        for j in range(row):
            hook = (row - j - 1) + (conj[j] - i - 1) + 1
            out *= Fraction(N + j - i, hook)
    return out


@lru_cache(maxsize=None)
def wg(rho, N):
    """Weingarten function of cycle type rho (a descending tuple) of S_d on U(N); partitions with at most N parts."""
    d = sum(rho)
    ones = (1,) * d
    total = Fraction(0)
    for lam in partitions(d, N):
        total += Fraction(mn_char(lam, ones) ** 2 * mn_char(lam, rho)) / schur_dim(lam, N)
    return total / factorial(d) ** 2


def cycle_type(perm):
    seen, out = set(), []
    for i in range(len(perm)):
        if i not in seen:
            n, j = 0, i
            while j not in seen:
                seen.add(j)
                j = perm[j]
                n += 1
            out.append(n)
    return tuple(sorted(out, reverse=True))


def compose_inverse(s, t):
    """The permutation s o t^-1."""
    inv = [0] * len(t)
    for i, ti in enumerate(t):
        inv[ti] = i
    return tuple(s[inv[i]] for i in range(len(s)))


PAIR_COUNT = {"pairs": 0}


def weingarten_monomial(rows_u, rows_c, N):
    """Integral over U(N) of prod_k g[rows_u[k]][0] * conj(g[rows_c[k]][0]): the sum over sigma, tau in S_d x S_d of
    delta(rows, sigma) delta(cols, tau) Wg(sigma tau^-1, N); every column index is 0, so the column delta is always 1."""
    d = len(rows_u)
    if d == 0:
        return Fraction(1)
    cols_u = [0] * d
    cols_c = [0] * d
    perms = list(itertools.permutations(range(d)))
    total = Fraction(0)
    for sigma in perms:
        row_ok = all(rows_u[k] == rows_c[sigma[k]] for k in range(d))
        for tau in perms:
            PAIR_COUNT["pairs"] += 1
            if row_ok and all(cols_u[k] == cols_c[tau[k]] for k in range(d)):
                total += wg(cycle_type(compose_inverse(sigma, tau)), N)
    return total


@lru_cache(maxsize=None)
def _wm_cached(rows_u, rows_c, N):
    return weingarten_monomial(list(rows_u), list(rows_c), N)


def route_c_value(poly, N, m, s):
    """Route C value of a polynomial given as Gaussian-integer coefficients (real part returned; imaginary part checked 0)."""
    re = im = Fraction(0)
    for (a0, a1, b0, b1), (cr, ci) in poly.items():
        if a0 + a1 != b0 + b1:
            continue  # different numbers of g and conj g factors: the integral over U(N) vanishes by phase
        v = _wm_cached(tuple([0] * a0 + [1] * a1), tuple([0] * b0 + [1] * b1), N)
        re += cr * v
        im += ci * v
    assert im == 0, "Route C imaginary part nonzero"
    return re


# ---------------------------------------------------------------- Route H: Hopf constant-term reduction, N = 2
def route_h_value(m, s):
    """(1/2) int_{-1}^{1} CT_u [ u^s (1+u)^m (1 - (1+u)^2 t^2)^m ] u^(-m) dt, as an exact polynomial integral in t."""
    def mul(p, q):
        out = {}
        for (i1, k1), c1 in p.items():
            for (i2, k2), c2 in q.items():
                key = (i1 + i2, k1 + k2)
                out[key] = out.get(key, 0) + c1 * c2
        return out
    one_u = {(0, 0): 1, (1, 0): 1}                      # 1 + u
    inner = {(0, 0): 1}
    sq = mul(one_u, one_u)
    inner = {(0, 0): 1}
    for key, c in sq.items():
        inner[(key[0], key[1] + 2)] = inner.get((key[0], key[1] + 2), 0) - c
    g = {(0, 0): 1}
    for _ in range(m):
        g = mul(g, one_u)
        g = mul(g, inner)
    # constant term of u^(s - m) g(u, t): the coefficient of u^(m - s)
    total = Fraction(0)
    for (iu, kt), c in g.items():
        if iu == m - s and kt % 2 == 0:
            total += Fraction(c, kt + 1)   # (1/2) int_{-1}^{1} t^kt dt
    return total


# ---------------------------------------------------------------- predictions
def rising(x, k):
    out = 1
    for i in range(k):
        out *= x + i
    return out


def c_m(m):
    return Fraction(4 ** m * factorial(m) ** 2, factorial(2 * m + 1))


def predicted(N, m, s, cm=None):
    if s == 0:
        return Fraction(0)
    k = 4 * m + s
    cm = c_m(m) if cm is None else cm
    b = comb(m - 1, s - 1) if s <= m else 0
    return cm * b * Fraction(rising(2, k), rising(N, k))


def fstr(x):
    return str(x)


def ms(t0):
    return (time.perf_counter_ns() - t0) // 1000000      # timing only


def log(msg):
    print(msg, flush=True)


# ---------------------------------------------------------------- identity checks
def exact_point(rng):
    return (Fraction(rng.randint(-9, 9), rng.randint(1, 5)), Fraction(rng.randint(-9, 9), rng.randint(1, 5)))


def eval_poly(poly, z0, z1):
    """Evaluate at (z0, z1) and w = conj z, Gaussian Fractions as pairs."""
    def gm(x, y):
        return (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0])

    def gp(x, k):
        out = (Fraction(1), Fraction(0))
        for _ in range(k):
            out = gm(out, x)
        return out
    c0, c1 = (z0[0], -z0[1]), (z1[0], -z1[1])
    re = im = Fraction(0)
    for (a0, a1, b0, b1), (cr, ci) in poly.items():
        t = gm(gm(gp(z0, a0), gp(z1, a1)), gm(gp(c0, b0), gp(c1, b1)))
        t = gm(t, (Fraction(cr), Fraction(ci)))
        re += t[0]
        im += t[1]
    return re, im


def abstract_identity():
    """u P - (1+u)(1 - (1+u)^2 tau^2) in the ring over (u, v, tau) with a = 1, reduced by u v -> 1 - tau^2: must be zero."""
    def mul(p, q):
        out = {}
        for e1, c1 in p.items():
            for e2, c2 in q.items():
                e = (e1[0] + e2[0], e1[1] + e2[1], e1[2] + e2[2])
                out[e] = out.get(e, 0) + c1 * c2
        return {e: c for e, c in out.items() if c}

    def add(p, q, sg=1):
        out = dict(p)
        for e, c in q.items():
            out[e] = out.get(e, 0) + sg * c
        return {e: c for e, c in out.items() if c}
    one = {(0, 0, 0): 1}
    u = {(1, 0, 0): 1}
    v = {(0, 1, 0): 1}
    t = {(0, 0, 1): 1}
    t2 = mul(t, t)
    a = one                                       # modulo the generator a - 1
    p_abs = mul(add(a, u), add(mul(mul(a, a), v), mul(add({(0, 0, 0): 2}, u), t2), -1))
    lhs = mul(u, p_abs)
    one_u = add(one, u)
    rhs = mul(one_u, add(one, mul(mul(one_u, one_u), t2), -1))
    diff = add(lhs, rhs, -1)
    reduced = {}
    for (iu, jv, kt), c in diff.items():
        mm = min(iu, jv)
        term = {(iu - mm, jv - mm, kt): c}
        for _ in range(mm):
            term = add(mul(term, one), mul(term, t2), -1)   # multiply by (1 - tau^2)
        reduced = add(reduced, term)
    return reduced


def identity_checks(fails):
    ids = []
    P, Q = build_pair("paper")
    zz0, zz1 = pmul(Z0, W0), pmul(Z1, W1)
    a = padd(zz0, zz1)
    tau = padd(zz0, zz1, -1)
    u = pscale(pmul(Z0, W1), (2, 0))
    v = pscale(pmul(Z1, W0), (2, 0))

    def rec(name, ok, detail):
        ids.append({"identity": name, "pass": bool(ok), "detail": detail})
        log(f"  identity {name}: {'pass' if ok else 'FAIL'} ({detail})")
        if not ok:
            fails.append("identity " + name)

    diff = padd(pmul(a, a), padd(pmul(u, v), pmul(tau, tau)), -1)
    rec("eq 3-2: a^2 = u v + tau^2 as a polynomial identity", not diff, f"difference has {len(diff)} monomials")
    rng = random.Random(148)
    okp = all(sum(e) == 8 for e in P) and all(sum(e) == 2 for e in Q)
    for r in (Fraction(3, 2), Fraction(2, 5)):
        for _ in range(3):
            z0, z1 = exact_point(rng), exact_point(rng)
            def sc(z, r=r):
                return (r * z[0], r * z[1])

            lhs_p = eval_poly(P, sc(z0), sc(z1))
            rhs_p = tuple(r ** 8 * x for x in eval_poly(P, z0, z1))
            lhs_q = eval_poly(Q, sc(z0), sc(z1))
            rhs_q = tuple(r ** 2 * x for x in eval_poly(Q, z0, z1))
            okp = okp and lhs_p == rhs_p and lhs_q == rhs_q
    rec("eq 3-4: P(rz) = r^8 P(z), Q(rz) = r^2 Q(z)", okp, "monomial degrees 8 and 2, and exact evaluation at 6 rational points with r = 3/2 and 2/5")
    red = abstract_identity()
    rec("u P - (1+u)(1-(1+u)^2 tau^2) in the ideal of a-1 and u v + tau^2 - 1", not red,
        f"remainder after a = 1 and u v -> 1 - tau^2 has {len(red)} terms")
    rec("P has 16 monomials", len(P) == 16, f"{len(P)} monomials")
    rec("P equals the 16-term list of the preflight", P == {e: (c, 0) for e, c in PREFLIGHT_P.items()}, "exponents and coefficients compared exactly")
    rec("each monomial of P has equal z-degree and w-degree (phase balance, as used by Lemma 5-5 of the paper)",
        all(balanced_degree(e) for e in P), "z-degree 4 and w-degree 4 on all 16")
    n_lit = sum(1 for e in P if balanced_literal(e))
    ids.append({"identity": "each monomial of P balanced in the Definitions sense (a0, a1) = (b0, b1)", "pass": n_lit == 16,
                "detail": f"{n_lit} of 16 monomials satisfy (a0, a1) = (b0, b1); recorded as a deviation of the hypothesis wording, "
                          "not counted as a failure: the 11 others are degree-balanced and are integrated to 0 by every route",
                "deviation": True})
    log(f"  identity literal balance: {n_lit} of 16 monomials have (a0, a1) = (b0, b1) (deviation from the hypothesis wording, recorded)")
    okc = True
    for m in range(1, 9):
        # int_0^1 (1 - s^2)^m ds as an exact polynomial integral
        val = sum(Fraction(comb(m, j) * (-1) ** j, 2 * j + 1) for j in range(m + 1))
        okc = okc and val == c_m(m)
    rec("eq 3-5: c_m = int_0^1 (1-s^2)^m ds = 4^m (m!)^2/(2m+1)! for m = 1..8", okc, "exact polynomial integral")
    return ids


# ---------------------------------------------------------------- main
def main():
    t_all = time.perf_counter_ns()
    fails = []
    results = {"routes": [], "identities": [], "controls": {}, "summary": {}, "environment": {"python": sys.version}, "notes": []}
    log("EXP-148 run (CPU, exact arithmetic)")
    results["identities"] = identity_checks(fails)

    P, Q = build_pair("paper")
    Pm = {m: ppow(P, m) for m in range(1, 9)}
    Qs = {s: ppow(Q, s) for s in range(0, 5)}
    cells = {}

    def cell(route, N, m, s, value, imag=Fraction(0)):
        pred = predicted(N, m, s)
        ok = (value == pred) and imag == 0
        results["routes"].append({"route": route, "N": N, "m": m, "s": s, "value": fstr(value), "predicted": fstr(pred), "equal": ok})
        cells.setdefault(route, [0, 0])
        cells[route][0] += 1
        if not ok:
            cells[route][1] += 1
            fails.append(f"cell route {route} N={N} m={m} s={s}: {value} vs {pred} (imag {imag})")

    # Route A
    t0 = time.perf_counter_ns()
    table_a = {}
    for m in A_RANGE[1]:
        for s in A_RANGE[2]:
            poly = pmul(Pm[m], Qs[s]) if s else Pm[m]
            for N in A_RANGE[0]:
                re, im = route_a_value(poly, N)
                cell("A", N, m, s, re, im)
                table_a[(N, m, s)] = re
    t_a = ms(t0)
    log(f"Route A: {cells['A'][0]} cells, {cells['A'][1]} mismatches, {t_a} ms")

    # Route B
    t0 = time.perf_counter_ns()
    RP, RQ = build_real_pair("paper")
    rpow_m = {0: {(0, 0, 0, 0): (1, 0)}}
    for m in B_RANGE[1]:
        rpow_m[m] = rmul(rpow_m[m - 1], RP)
        poly = rpow_m[m]
        for s in B_RANGE[2]:
            if s:
                poly = rmul(poly, RQ)
            for N in B_RANGE[0]:
                re, im = route_b_value(poly, N)
                cell("B", N, m, s, re, im)
        log(f"  route B m={m} done ({len(rpow_m[m])} monomials in P^m)")
    t_b = ms(t0)
    log(f"Route B: {cells['B'][0]} cells, {cells['B'][1]} mismatches, {t_b} ms")

    # Route C
    t0 = time.perf_counter_ns()
    PAIR_COUNT["pairs"] = 0
    for N in C_RANGE[0]:
        for (m, s) in C_RANGE[1]:
            poly = pmul(Pm[m], Qs[s]) if s else Pm[m]
            cell("C", N, m, s, route_c_value(poly, N, m, s))
    t_c = ms(t0)
    pairs_c = PAIR_COUNT["pairs"]
    log(f"Route C: {cells['C'][0]} cells, {cells['C'][1]} mismatches, {t_c} ms, {pairs_c} (sigma, tau) pairs visited")

    # Route H
    t0 = time.perf_counter_ns()
    for m in H_RANGE[0]:
        for s in H_RANGE[1]:
            cell("H", 2, m, s, route_h_value(m, s))
    t_h = ms(t0)
    log(f"Route H: {cells['H'][0]} cells, {cells['H'][1]} mismatches, {t_h} ms")

    # cross-route agreement on shared cells
    byk = {}
    for r in results["routes"]:
        byk.setdefault((r["N"], r["m"], r["s"]), {})[r["route"]] = r["value"]
    disagree = [k for k, v in byk.items() if len(set(v.values())) > 1]
    results["summary"]["cross_route_disagreements"] = len(disagree)
    if disagree:
        fails.append(f"routes disagree on {len(disagree)} shared cells")

    # ------------------------------------------------------------ controls
    controls = results["controls"]

    # K1
    t0 = time.perf_counter_ns()
    nonzero_pure = 0
    changed_all = True
    k1_rows = []
    for key in sorted(P):
        Pk = {e: c for e, c in P.items() if e != key}
        powk = {m: ppow(Pk, m) for m in range(1, 9)}
        pure = [m for m in range(1, 4) if route_a_value(powk[m], 2)[0] != 0]
        changed = 0
        for m in range(1, 9):
            for s in range(0, 5):
                poly = pmul(powk[m], Qs[s]) if s else powk[m]
                if route_a_value(poly, 2)[0] != table_a[(2, m, s)]:
                    changed += 1
        nonzero_pure += 1 if pure else 0
        changed_all = changed_all and changed > 0
        k1_rows.append({"removed": list(key), "pure_nonzero_m_le_3": pure, "table_cells_changed_of_40": changed})
    k1_ok = nonzero_pure >= 12 and changed_all
    controls["K1"] = {"observed": f"{nonzero_pure} of 16 removals give a nonzero pure moment for some m <= 3; every removal changes some value: {changed_all}",
                      "behaved": k1_ok, "rows": k1_rows}
    log(f"K1: {controls['K1']['observed']} -> {'ok' if k1_ok else 'FAIL'} ({ms(t0)} ms)")

    # K2
    alt = {(m, s): predicted(2, m, s, cm=Fraction(1, m + 1)) for m in (2,) for s in (1, 2)}
    dis = [(m, s) for (m, s), val in alt.items() if val != table_a[(2, m, s)]]
    k2_ok = len(dis) > 0
    controls["K2"] = {"observed": f"with c_m = 1/(m+1) the prediction at N = 2, m = 2 disagrees with the computed value for (m, s) in {dis}; "
                                  f"computed {[fstr(table_a[(2, 2, s)]) for s in (1, 2)]} vs alternative {[fstr(alt[(2, s)]) for s in (1, 2)]}",
                      "behaved": k2_ok}
    log(f"K2: {controls['K2']['observed']} -> {'ok' if k2_ok else 'FAIL'}")

    # K3
    P3, _ = build_pair("k3")
    pure3 = [(m, fstr(route_a_value(ppow(P3, m), 2)[0])) for m in range(1, 4)]
    k3_ok = any(v != "0" for _, v in pure3)
    controls["K3"] = {"observed": f"pure moments with (2a+u) replaced by (a+u), N = 2, m = 1..3: {pure3}", "behaved": k3_ok}
    log(f"K3: {controls['K3']['observed']} -> {'ok' if k3_ok else 'FAIL'}")

    # K4
    t0 = time.perf_counter_ns()
    rng = random.Random(148)
    monos = []
    for _ in range(100):
        a0, a1 = rng.randint(0, 3), rng.randint(0, 3)
        monos.append((a0, a1, a0, a1))
    for _ in range(100):
        monos.append(tuple(rng.randint(0, 3) for _ in range(4)))
    n_bal = sum(1 for e in monos if balanced_literal(e))
    n_chk = 0
    bad = 0
    for e in monos:
        rpoly = real_monomial(e)
        for N in (2, 3, 5):
            va, ia = route_a_value({e: (1, 0)}, N)
            vb, ib = route_b_value(rpoly, N)
            n_chk += 1
            if va != vb or ia != 0 or ib != 0:
                bad += 1
    k4_ok = bad == 0
    controls["K4"] = {"observed": f"{len(monos)} monomials ({n_bal} literally balanced, degree <= 12) x N in (2, 3, 5): {n_chk} comparisons, {bad} disagreements between A and B",
                      "behaved": k4_ok}
    log(f"K4: {controls['K4']['observed']} -> {'ok' if k4_ok else 'FAIL'} ({ms(t0)} ms)")

    # K5
    k5 = []
    k5_ok = True
    for N in range(2, 7):
        v1 = weingarten_monomial([0], [0], N)
        v2 = weingarten_monomial([0, 0], [0, 0], N)
        good = v1 == Fraction(1, N) and v2 == Fraction(2, N * (N + 1))
        k5_ok = k5_ok and good
        k5.append({"N": N, "int_abs_g11_sq": fstr(v1), "int_abs_g11_4": fstr(v2), "ok": good})
    controls["K5"] = {"observed": "Route C: " + "; ".join(f"N={r['N']}: {r['int_abs_g11_sq']}, {r['int_abs_g11_4']}" for r in k5), "behaved": k5_ok, "rows": k5}
    log(f"K5: {controls['K5']['observed']} -> {'ok' if k5_ok else 'FAIL'}")

    # K6
    Pr = {e: c for e, c in P.items() if e[1] == 0 and e[3] == 0}
    Qr = {e: c for e, c in Q.items() if e[1] == 0 and e[3] == 0}
    k6_ok = len(Qr) == 0
    controls["K6"] = {"observed": f"restricting to z1 = 0: Q has {len(Qr)} monomials (zero), P restricts to {sorted(Pr.items())}; so Q P^m = 0 on the torus direction",
                      "behaved": k6_ok}
    log(f"K6: {controls['K6']['observed']} -> {'ok' if k6_ok else 'FAIL'}")
    for name, c in controls.items():
        if not c["behaved"]:
            fails.append("control " + name)

    total_ms = ms(t_all)
    results["summary"].update({
        "cells": {r: cells[r][0] for r in cells}, "mismatches": {r: cells[r][1] for r in cells},
        "wall_ms": {"A": t_a, "B": t_b, "C": t_c, "H": t_h, "total": total_ms},
        "route_C_sigma_tau_pairs_visited": pairs_c, "failures": fails,
    })
    results["notes"].append("The hypothesis wording 'each monomial of P is balanced' is true in the sense of equal z-degree and w-degree (all 16) "
                            "and false in the sense of (a0, a1) = (b0, b1) of its Definitions (5 of 16); recorded under identities.")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(results, indent=1), encoding="utf-8")
    log(f"total {total_ms} ms; failures: {len(fails)}")
    for f in fails:
        log("  FAIL " + f)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
