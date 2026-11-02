"""EXP-137 P1: the Laurent reduction of [P,Q] = x^2, derived from the polygons alone (own code)."""

from __future__ import annotations

import random

import sympy as sp

import exp137_lib as L

t, z, x, y = sp.symbols("t z x y")


def sym_p(i, j):
    return sp.Symbol(f"p_{i}_{j}")


def sym_q(i, j):
    return sp.Symbol(f"q_{i}_{j}")


def band_equations(ppts, qpts, pairs=None):
    """{band k: {t-degree m: sympy coefficient of t^m z^k in [P,Q]_{x,y}}}, generic coefficients."""
    out: dict = {}
    for (m, k), lst in L.bracket_terms(ppts, qpts).items():
        terms = []
        for pp, qq, w in lst:
            if pairs is not None and not pairs(L.band_of(pp), L.band_of(qq)):
                continue
            terms.append(w * sym_p(*pp) * sym_q(*qq))
        if terms:
            out.setdefault(k, {})[m] = sp.Add(*terms)
    return out


def band_counts(ppts, qpts):
    """{band: number of nonzero coefficient equations}, structural (distinct monomials cannot cancel)."""
    out: dict = {}
    for (m, k) in L.bracket_terms(ppts, qpts):
        out[k] = out.get(k, 0) + 1
    return dict(sorted(out.items(), reverse=True))


def chain_rule_checks(seed=1370):
    """[t,z]=-1, x^2 = t^2 z^4, and [P,Q]_{x,y} = -[P,Q]_{t,z} on random polynomials of the Case-2 supports."""
    tx, zy = x * y**2, 1 / y
    jtz = sp.simplify(sp.diff(tx, x) * sp.diff(zy, y) - sp.diff(tx, y) * sp.diff(zy, x))
    res = {"[t,z]_{x,y}": int(jtz), "x2_minus_t2z4": int(sp.simplify(x**2 - tx**2 * zy**4))}
    rnd = random.Random(seed)
    Pp, Qq = L.lattice_points(L.CASE2_P), L.lattice_points(L.CASE2_Q)
    Pxy = sum(rnd.randint(-5, 5) * x**i * y**j for i, j in Pp)
    Qxy = sum(rnd.randint(-5, 5) * x**i * y**j for i, j in Qq)
    direct = sp.diff(Pxy, x) * sp.diff(Qxy, y) - sp.diff(Pxy, y) * sp.diff(Qxy, x)
    # same polynomials written in (t,z): x^i y^j = t^i z^(2i-j)
    rnd = random.Random(seed)
    Ptz = sum(rnd.randint(-5, 5) * t**i * z ** (2 * i - j) for i, j in Pp)
    Qtz = sum(rnd.randint(-5, 5) * t**i * z ** (2 * i - j) for i, j in Qq)
    btz = sp.diff(Ptz, t) * sp.diff(Qtz, z) - sp.diff(Ptz, z) * sp.diff(Qtz, t)
    via = -btz.subs({t: tx, z: zy}, simultaneous=True)
    res["bracket_xy_equals_minus_bracket_tz"] = bool(sp.simplify(sp.expand(direct - via)) == 0)
    return res


def _bands_as_polys(ppts, qpts, upper_only):
    """A..G as sympy polynomials in t from the lattice points: band k -> sum p_{ij} t^i."""
    def poly(pts, sym, k):
        return sum(sym(i, j) * t**i for i, j in pts if L.band_of((i, j)) == k)

    Pb = {k: poly(ppts, sym_p, k) for k in {L.band_of(p) for p in ppts}}
    Qb = {k: poly(qpts, sym_q, k) for k in {L.band_of(p) for p in qpts}}
    return Pb, Qb


def helali_J(Pb, Qb):
    """Helali section 4, J4..J0, from upper bands A,B,C (P bands 2,1,0) and D,E,F,G (Q bands 3..0)."""
    zero = sp.Integer(0)
    A, B, C = Pb.get(2, zero), Pb.get(1, zero), Pb.get(0, zero)
    D, E, F, G = Qb.get(3, zero), Qb.get(2, zero), Qb.get(1, zero), Qb.get(0, zero)
    d = lambda f: sp.diff(f, t)
    return {
        4: 2 * A * d(D) - 3 * d(A) * D,
        3: 2 * (A * d(E) - d(A) * E) + (B * d(D) - 3 * d(B) * D),
        2: (2 * A * d(F) - d(A) * F) + (B * d(E) - 2 * d(B) * E) - 3 * d(C) * D,
        1: 2 * A * d(G) + (B * d(F) - d(B) * F) - 2 * d(C) * E,
        0: B * d(G) - d(C) * F,
    }


def compare_with_helali(case):
    ppts = L.lattice_points(L.CASE2_P if case == "case2" else L.CASE1_P)
    qpts = L.lattice_points(L.CASE2_Q if case == "case2" else L.CASE1_Q)
    ours = band_equations(ppts, qpts)
    Pb, Qb = _bands_as_polys(ppts, qpts, upper_only=True)
    J = helali_J(Pb, Qb)
    res: dict = {}
    for k in range(4, -1, -1):
        poly_ours = sum(c * t**m for m, c in ours.get(k, {}).items())
        diff = sp.expand(poly_ours - J[k])
        if case == "case2":
            res[f"J{k}_equal"] = bool(diff == 0)
        else:
            # Case 1: the lower bands add cross terms to J1 and J0; the difference must be exactly
            # the bracket restricted to pairs with a negative band.
            neg = band_equations(ppts, qpts, pairs=lambda p, q: p < 0 or q < 0)
            cross = sum(c * t**m for m, c in neg.get(k, {}).items())
            res[f"J{k}_equal"] = bool(diff == 0)
            res[f"J{k}_equal_up_to_negative_band_cross_terms"] = bool(sp.expand(diff - cross) == 0)
            res[f"J{k}_cross_term_count"] = len(neg.get(k, {}))
    # the right-hand side: x^2 = t^2 z^4 only in band 4, t-degree 2
    j4 = sp.Poly(sum(c * t**m for m, c in ours[4].items()), t)
    res["J4_degrees"] = sorted(m for (m,) in j4.monoms())
    res["J4_residual_constant"] = 1  # equation J4 - t^2 = 0 has right-hand side coefficient 1 at t^2
    res["rhs_band"], res["rhs_t_degree"] = 4, 2
    return res


def adverse_polygon_control():
    """Case 2 with the extra vertex (0,8) added to N(P): the band system must change."""
    base_p, base_q = L.lattice_points(L.CASE2_P), L.lattice_points(L.CASE2_Q)
    adv_p = L.lattice_points(L.CASE2_P + [(0, 8)])
    base = L.bracket_terms(base_p, base_q)
    adv = L.bracket_terms(adv_p, base_q)
    extra = sorted({k for (_m, k) in adv} - {k for (_m, k) in base})
    ours_base = band_equations(base_p, base_q)
    ours_adv = band_equations(adv_p, base_q)
    changed_bands = sorted(k for k in ours_adv if k in ours_base and sp.expand(
        sum(c * t**m for m, c in ours_adv[k].items()) - sum(c * t**m for m, c in ours_base[k].items())) != 0)
    return {
        "p_points_base": len(base_p), "p_points_adverse": len(adv_p),
        "band_system_changed": bool(extra or changed_bands),
        "extra_bands": extra, "changed_existing_bands": changed_bands,
        "equation_count_base": len(base), "equation_count_adverse": len(adv),
    }


def main():
    out: dict = {"chain_rule": chain_rule_checks()}
    for case, pv, qv in (("case1", L.CASE1_P, L.CASE1_Q), ("case2", L.CASE2_P, L.CASE2_Q)):
        pp, qq = L.lattice_points(pv), L.lattice_points(qv)
        bands_p = sorted({L.band_of(p) for p in pp}, reverse=True)
        bands_q = sorted({L.band_of(p) for p in qq}, reverse=True)
        counts = band_counts(pp, qq)
        out[case] = {
            "P_points": len(pp), "Q_points": len(qq), "P_bands": bands_p, "Q_bands": bands_q,
            "equations_per_band": counts,
            "equations_total": sum(counts.values()),
            "equations_upper_J4_to_J0": sum(v for k, v in counts.items() if k >= 0),
            "equations_negative_bands": sum(v for k, v in counts.items() if k < 0),
            "negative_bands_with_equations": sorted(k for k in counts if k < 0),
            "compare_with_helali_J": compare_with_helali(case),
        }
    out["adverse_polygon_control"] = adverse_polygon_control()
    return out


if __name__ == "__main__":
    import json

    print(json.dumps(main(), indent=1, default=str))
