"""cclib: exact Albouy-Chenciner machinery for the central-configurations program.

Promoted from EXP-001/EXP-002 (methodology/04). Exact arithmetic only (sympy over QQ);
the census functions are verdict-grade and regression-gated by tests/ on the EXP-001
exact points. Forms per the method dossier (HJ11 eqs. (3)-(7), PDF read 2026-07-23):
S_ij = r_ij^{-3} + Lambda with Lambda = -1 (scale normalization), S_ii = 0.
"""

from itertools import combinations, permutations, product as iproduct

import sympy as sp

__all__ = [
    "rvar", "ac_symmetric", "ac_asymmetric", "e_iu", "cayley_menger_planar4",
    "strip_monomial_factors", "support_profile", "grevlex_pure_power_zero_dim",
    "census_positive", "u_i_j_invariants",
]


def rvar(i: int, j: int):
    i, j = min(i, j), max(i, j)
    return sp.Symbol(f"r{i}{j}", positive=True)


def _S(i, j):
    if i == j:
        return sp.Integer(0)
    return rvar(i, j) ** -3 - 1


def _r2(i, j):
    if i == j:
        return sp.Integer(0)
    return rvar(i, j) ** 2


def _cleared(expr):
    num, _den = sp.fraction(sp.together(expr))
    return sp.expand(num)


def ac_symmetric(n: int, masses):
    """Cleared symmetric Albouy-Chenciner polynomials f_ij (i < j). HJ11 eq. (3)."""
    out = {}
    for i, j in combinations(range(1, n + 1), 2):
        expr = sp.Integer(0)
        for k in range(1, n + 1):
            expr += masses[k - 1] * (
                _S(i, k) * (_r2(j, k) - _r2(i, k) - _r2(i, j))
                + _S(j, k) * (_r2(i, k) - _r2(j, k) - _r2(i, j))
            )
        out[(i, j)] = _cleared(expr)
    return out


def ac_asymmetric(n: int, masses):
    """Cleared asymmetric (Roberts) equations g_ij for ordered pairs i != j.
    HJ11 eq. (4); f_ij = g_ij + g_ji."""
    out = {}
    for i, j in permutations(range(1, n + 1), 2):
        expr = sp.Integer(0)
        for k in range(1, n + 1):
            expr += masses[k - 1] * _S(i, k) * (_r2(j, k) - _r2(i, k) - _r2(i, j))
        out[(i, j)] = _cleared(expr)
    return out


def e_iu(n: int, masses):
    """Cleared energy-inertia relation U - M I (HJ11 eq. (7); consequence of F).

    With I = (1/M) sum m_i m_j r_ij^2 this is U - sum m_i m_j r_ij^2.
    """
    U = sp.Integer(0)
    Isum = sp.Integer(0)
    for i, j in combinations(range(1, n + 1), 2):
        U += masses[i - 1] * masses[j - 1] / rvar(i, j)
        Isum += masses[i - 1] * masses[j - 1] * rvar(i, j) ** 2
    return _cleared(U - Isum)


def cayley_menger_planar4():
    """Bordered 5x5 Cayley-Menger determinant of 4 points: zero iff coplanar (R^2)."""
    r = {}
    for i, j in combinations(range(1, 5), 2):
        r[(i, j)] = rvar(i, j) ** 2
    M = sp.Matrix([
        [0, 1, 1, 1, 1],
        [1, 0, r[(1, 2)], r[(1, 3)], r[(1, 4)]],
        [1, r[(1, 2)], 0, r[(2, 3)], r[(2, 4)]],
        [1, r[(1, 3)], r[(2, 3)], 0, r[(3, 4)]],
        [1, r[(1, 4)], r[(2, 4)], r[(3, 4)], 0],
    ])
    return sp.expand(M.det(method="berkowitz"))


def strip_monomial_factors(expr, gens):
    """Product of the non-monomial irreducible factors (torus-equivalent form)."""
    coeff, factors = sp.factor_list(sp.expand(expr), *gens)
    out = sp.Integer(1)
    stripped = []
    for base, exp in factors:
        p = sp.Poly(base, *gens)
        if len(p.monoms()) == 1:
            stripped.append(f"{base}**{exp}")
        else:
            out *= base ** exp
    return sp.expand(out), stripped


def support_profile(expr, gens):
    p = sp.Poly(expr, *gens)
    monoms = p.monoms()
    vecs = [sp.Matrix(m) for m in monoms]
    if len(vecs) <= 1:
        adim = 0
    else:
        M = sp.Matrix.hstack(*[v - vecs[0] for v in vecs[1:]])
        adim = M.rank()
    return {"n_monomials": len(monoms),
            "total_degree": int(p.total_degree()),
            "support_affine_dim": int(adim)}


def grevlex_pure_power_zero_dim(polys, gens):
    """Standard 0-dim criterion on the grevlex Groebner basis (pure-power leads)."""
    G = sp.groebner(polys, *gens, order="grevlex")
    pure = set()
    lms = []
    for g in G.exprs:
        p = sp.Poly(g, *gens)
        mon = tuple(p.LM(order="grevlex").exponents)
        lms.append(mon)
        nz = [i for i, e in enumerate(mon) if e > 0]
        if len(nz) == 1:
            pure.add(nz[0])
    return pure == set(range(len(gens))), lms, G


def census_positive(eqs, gens):
    """Complete exact census of the real POSITIVE common zeros of a system that is
    0-dimensional in the positive orthant charts used.

    Verdict-grade instrument (EXP-001): per-variable univariate eliminants from lex
    Groebner bases (ideal members: completeness by construction), CRootOf real-root
    isolation, and exact residual acceptance (`equals(0) is True` on EVERY equation).
    sympy's solve_poly_system is BANNED for counts (returned incomplete lists,
    EXP-001 adversarial record). Raises RuntimeError when a variable has no univariate
    eliminant (not 0-dim in that elimination).
    """
    per_var_roots = {}
    meta = {"eliminants": {}}
    for v in gens:
        others = [g for g in gens if g != v]
        G = sp.groebner(eqs, *(others + [v]), order="lex")
        univ = [g for g in G.exprs if g.free_symbols <= {v}]
        if not univ:
            raise RuntimeError(f"no univariate eliminant for {v}")
        u = univ[0]
        for extra in univ[1:]:
            u = sp.gcd(u, extra)
        meta["eliminants"][str(v)] = str(sp.factor(u))
        per_var_roots[v] = [r for r in sp.Poly(u, v).real_roots() if r > 0]
    accepted = []
    n_cand = 1
    for v in gens:
        n_cand *= len(per_var_roots[v])
    meta["candidate_tuples"] = n_cand
    for combo in iproduct(*[per_var_roots[v] for v in gens]):
        subs_map = dict(zip(gens, combo))
        ok = True
        for e in eqs:
            if e.subs(subs_map).equals(0) is not True:
                ok = False
                break
        if ok:
            accepted.append(combo)
    return accepted, meta


def u_i_j_invariants(n: int, masses, point: dict):
    """Exact U, I, M and the scale-free J = U I^(1/2) / M^(5/2) at a distance point."""
    M = sum(masses)
    U = sp.Integer(0)
    I = sp.Integer(0)
    for i, j in combinations(range(1, n + 1), 2):
        rij = point[rvar(i, j)]
        U += masses[i - 1] * masses[j - 1] / rij
        I += masses[i - 1] * masses[j - 1] * rij ** 2
    I = I / M
    J = U * sp.sqrt(I) / M ** sp.Rational(5, 2)
    return U, I, M, J
