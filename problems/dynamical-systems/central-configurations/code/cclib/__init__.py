"""cclib: exact Albouy-Chenciner machinery for the central-configurations program.

Promoted from EXP-001/EXP-002 (methodology/04). Exact arithmetic only (sympy over QQ);
the census functions are verdict-grade and regression-gated by tests/ on the EXP-001
exact points. Forms per the method dossier (HJ11 eqs. (3)-(7), PDF read 2026-07-23):
S_ij = r_ij^{-3} + Lambda with Lambda = -1 (scale normalization), S_ii = 0.
"""

from itertools import combinations, permutations, product as iproduct

import sympy as sp

__all__ = [
    "dziobek4",
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


def dziobek4():
    """Cleared Dziobek equations for the PLANAR NONCOLLINEAR four-body problem.

    Hampton-Moeckel (2006), Section 2.2, equation (12): for a planar noncollinear
    relative equilibrium the four triangle areas are nonzero (perpendicular-bisector
    theorem) and

        S_12 S_34 = S_13 S_24 = S_14 S_23,     S_ij = r_ij^{-3} - 1.

    Returned symmetrized as the three differences, cleared of denominators, as HM06
    do to keep the S_4 action manifest. Valid only on the noncollinear stratum: a
    certificate obtained with these equations covers the noncollinear part, while
    the n!/2 collinear classes are classical (Moulton).
    """
    def S(i, j):
        return rvar(i, j) ** -3 - 1

    a = S(1, 2) * S(3, 4)
    b = S(1, 3) * S(2, 4)
    c = S(1, 4) * S(2, 3)
    return {"h_ab": _cleared(a - b), "h_bc": _cleared(b - c), "h_ac": _cleared(a - c)}


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


def quotient_staircase(G, gens, max_basis=4000):
    """Monomial staircase basis of QQ[gens]/I from a grevlex Groebner basis G.
    Returns the list of exponent tuples, or None when the ideal is not 0-dim
    (staircase infinite / exceeds max_basis)."""
    leads = [tuple(sp.Poly(g, *gens).LM(order="grevlex").exponents) for g in G.exprs]

    def divisible(m):
        return any(all(m[i] >= l[i] for i in range(len(gens))) for l in leads)

    basis = []
    seen = set()
    frontier = [tuple([0] * len(gens))]
    seen.add(frontier[0])
    while frontier:
        m = frontier.pop()
        if divisible(m):
            continue
        basis.append(m)
        if len(basis) > max_basis:
            return None
        for i in range(len(gens)):
            m2 = tuple(m[j] + (1 if j == i else 0) for j in range(len(gens)))
            if m2 not in seen:
                seen.add(m2)
                frontier.append(m2)
    return sorted(basis)


def coordinate_eliminant(G, gens, v, staircase):
    """Univariate eliminant for coordinate v via the multiplication-matrix
    characteristic polynomial (Stickelberger: the eigenvalues of M_v are exactly the
    values of v on V(I)); exact rational linear algebra, no lex Groebner needed."""
    idx = {m: k for k, m in enumerate(staircase)}
    N = len(staircase)
    cols = []
    for m in staircase:
        mono = sp.prod([g ** e for g, e in zip(gens, m)])
        _q, r = sp.reduced(v * mono, list(G.exprs), *gens, order="grevlex")
        pr = sp.Poly(r, *gens)
        col = [sp.Integer(0)] * N
        for mon, coef in zip(pr.monoms(), pr.coeffs()):
            col[idx[tuple(mon)]] = coef
        cols.append(col)
    M = sp.Matrix(N, N, lambda i, j: cols[j][i])
    # Exact fast path: DomainMatrix.charpoly over QQ (Matrix.charpoly's Berkowitz on
    # Expr entries is orders of magnitude slower at N ~ 100). Note the generator trap
    # caught in EXP-002 debugging: Matrix.charpoly returns a PurePoly over its OWN
    # Dummy; never wrap its expression with a fresh symbol (degree-0 Poly results).
    from sympy.polys.matrices import DomainMatrix
    dM = DomainMatrix.from_Matrix(M).convert_to(sp.QQ)
    coeffs = dM.charpoly()  # highest-degree-first domain coefficients
    x = sp.Dummy("x")
    expr = sum(sp.QQ.to_sympy(c) * x ** (len(coeffs) - 1 - k)
               for k, c in enumerate(coeffs))
    return sp.Poly(expr, x), x


def census_positive(eqs, gens, max_basis=4000):
    """Complete exact census of the real POSITIVE common zeros of a 0-dimensional
    system.

    Verdict-grade instrument (EXP-001, upgraded after EXP-002's first recorded run):
      1. ONE grevlex Groebner basis; finite staircase certifies 0-dim;
      2. per-coordinate univariate eliminants as multiplication-matrix characteristic
         polynomials (Stickelberger: eigenvalue set = coordinate value set:
         candidate completeness is structural);
      3. squarefree parts before root isolation (EXP-002 first-run lesson:
         Poly.real_roots returns roots WITH multiplicity; without sqf_part the
         census emits duplicate points);
      4. exact CRootOf isolation, positivity, and exact residual acceptance
         (`equals(0) is True` on EVERY equation).
    sympy's solve_poly_system stays BANNED for counts (EXP-001 adversarial record).
    Raises RuntimeError when the staircase is not finite (not 0-dimensional).
    """
    import time as _time
    t0 = _time.time()
    G = sp.groebner(eqs, *gens, order="grevlex")
    staircase = quotient_staircase(G, gens, max_basis=max_basis)
    if staircase is None:
        raise RuntimeError("ideal is not zero-dimensional (infinite staircase)")
    meta = {"eliminants": {}, "quotient_dim": len(staircase),
            "t_groebner_s": round(_time.time() - t0, 1)}
    per_var_roots = {}
    t0 = _time.time()
    for v in gens:
        P, _x = coordinate_eliminant(G, gens, v, staircase)
        Ps = P.sqf_part()
        meta["eliminants"][str(v)] = str(sp.factor(Ps.as_expr()))
        roots = [r for r in Ps.real_roots() if r > 0]
        per_var_roots[v] = sorted(set(roots), key=sp.default_sort_key)
    meta["t_eliminants_s"] = round(_time.time() - t0, 1)
    accepted = []
    n_cand = 1
    for v in gens:
        n_cand *= len(per_var_roots[v])
    meta["candidate_tuples"] = n_cand
    t0 = _time.time()
    for combo in iproduct(*[per_var_roots[v] for v in gens]):
        subs_map = dict(zip(gens, combo))
        ok = True
        for e in eqs:
            res = e.subs(subs_map)
            # certified-numeric pre-filter: sympy evalf tracks precision for
            # algebraic expressions; |value| demonstrably above the bound means
            # a nonzero residual, so rejection here is rigorous and cheap.
            v40 = res.evalf(40)
            if v40.is_comparable and abs(v40) > sp.Float(10) ** -20:
                ok = False
                break
            if res.equals(0) is not True:
                ok = False
                break
        if ok:
            accepted.append(combo)
    meta["t_accept_s"] = round(_time.time() - t0, 1)
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


def dziobek_products5():
    """Cleared Dziobek product differences for FIVE bodies, all quadruples.

    HJ11 eq. (5): on the Dziobek stratum (configuration dimension n - 2, i.e.
    SPATIAL for n = 5), S_ij S_kl = S_ik S_jl = S_il S_jk for every quadruple
    {i, j, k, l}, with S_ij = r_ij^-3 - 1. Five quadruples times three pairing
    differences = 15 cleared equations (five independent), kept in full for the
    manifest S_5 action. CAUTION (recorded in the EXP-011 hypothesis): the
    products characterize the rank-one factorization S_ij = z_i z_j only where
    enough entries are nonzero; the cut they define is an OVERVARIETY of the
    spatial Dziobek central configurations.
    """
    out = {}
    for i, j, k, l in combinations(range(1, 6), 4):
        a = _S(i, j) * _S(k, l)
        b = _S(i, k) * _S(j, l)
        c = _S(i, l) * _S(j, k)
        tag = f"{i}{j}{k}{l}"
        out[f"h{tag}_ab"] = _cleared(a - b)
        out[f"h{tag}_bc"] = _cleared(b - c)
        out[f"h{tag}_ac"] = _cleared(a - c)
    return out


def cayley_menger_spatial5():
    """Bordered 6x6 Cayley-Menger determinant of 5 points: zero iff the points
    embed in R^3 (HJ11 eq. (6))."""
    r = {}
    for i, j in combinations(range(1, 6), 2):
        r[(i, j)] = rvar(i, j) ** 2
    rows = [[0] + [1] * 5]
    for i in range(1, 6):
        row = [1]
        for j in range(1, 6):
            row.append(0 if i == j else r[(min(i, j), max(i, j))])
        rows.append(row)
    return sp.expand(sp.Matrix(rows).det(method="berkowitz"))
