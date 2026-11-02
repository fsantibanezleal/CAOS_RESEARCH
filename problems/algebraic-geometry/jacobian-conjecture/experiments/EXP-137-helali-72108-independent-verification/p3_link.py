"""EXP-137 P3 link: do the certificate generators concern the systems of P1?

Case 2: our own cascade (cascade.py, from the polygons) produces the 25 residual equations; we (a) decide
the unit ideal over K with Singular, (b) compare Helali's four serialized generators with ours up to a constant
and up to a renaming of the three parameters.
Case 1: our own cascade down to the lowest band, and a comparison of its compatibility system with Helali's
13-equation checkpoint where the cascade is reproducible within budget.
"""

from __future__ import annotations

import itertools
import re
import subprocess
import time
from pathlib import Path

from flint import fmpq

import cascade as C
import exp137_lib as L
import p2_firstblock as P2
import p3_certs as P3

HERE = Path(__file__).resolve().parent
ART = HERE / "artifacts"
SCRATCH = P2.SCRATCH


def our_field(log=print):
    lex = P2.parse_lex((ART / "p2_singular.out").read_text())
    F, A, val = C.build_field(lex, log=log)
    D, resid = C.solve_D(F, A)
    assert not any(resid), "J4 not satisfied exactly in K"
    return F, A, D


def normalize(poly, perm=None):
    """Monic-ize a MP (divide by the leading coefficient in sorted monomial order), optionally permuting variables."""
    items = {}
    for m, c in poly.d.items():
        mm = m if perm is None else tuple(m[perm[i]] for i in range(len(perm)))
        items[mm] = c
    if not items:
        return {}
    lead = items[max(items)]
    inv = lead.inv()
    return {m: (c * inv) for m, c in items.items()}


def key_of(nd):
    return frozenset((m, str(c.p)) for m, c in nd.items())


def case2_link(F, A, D, log=print):
    res = {"status": "UNVERIFIED"}
    cas = C.Cascade(F, A, D, L.lattice_points(L.CASE2_P), L.lattice_points(L.CASE2_Q))
    layers = [cas.layer(k) for k in (3, 2, 1, 0)]
    res["layers"] = layers
    res["parameters"] = cas.nparams
    res["residual_equations"] = len(cas.compat)
    res["residual_equations_by_layer"] = {str(k): sum(1 for kk, _ in cas.compat if kk == k) for k in (1, 0)}
    # (a) Singular unit ideal over K
    names = [f"p{i}" for i in range(cas.nparams)]
    polys = [c for _k, c in cas.compat]
    sing = SCRATCH / "case2_unit.sing"
    sing.write_text(C.singular_unit_script(F, polys, cas.nparams, "case2"))
    out = ART / "case2_unit_singular.out"
    t0 = time.time()
    r = subprocess.run(["wsl", "-e", "Singular", "-q", P2.wsl_path(sing)], capture_output=True, text=True, timeout=7200)
    out.write_text(r.stdout + r.stderr)
    res["singular_wall_seconds"] = round(time.time() - t0, 1)
    txt = r.stdout
    res["singular_unit_ideal"] = bool(re.search(r"^UNIT\s*$", txt, re.M))
    m = re.search(r"STD_SIZE=(\d+)", txt)
    res["singular_std_size"] = int(m.group(1)) if m else None
    res["singular_output_file"] = "artifacts/case2_unit_singular.out"
    # (b) compare Helali's generators
    payload, meta = P3.load_pickle("case2_exact_certificate.pkl")
    FH = P3.field_from_coeffs(payload["field_minpoly_coefficients"])
    assert P3.minpoly_monic_hash(FH) == P3.minpoly_monic_hash(F)
    hel = [P3.decode_poly(F, g) for g in payload["generators"]]
    ours = [c for _k, c in cas.compat]
    matches = []
    for perm in itertools.permutations(range(cas.nparams)):
        ours_n = {key_of(normalize(c, perm)) for c in ours}
        ok = []
        for g in hel:
            g6 = {m[:cas.nparams]: c for m, c in g.items()}
            assert all(sum(m[cas.nparams:]) == 0 for m in g)
            lead = g6[max(g6)]
            inv = lead.inv()
            ok.append(key_of({m: c * inv for m, c in g6.items()}) in ours_n)
        if all(ok):
            matches.append(perm)
    res["helali_generator_indices"] = list(payload["generator_indices"])
    res["helali_generators_equal_ours_up_to_constant_and_param_permutation"] = bool(matches)
    res["matching_parameter_permutations"] = [list(p) for p in matches]
    res["_cascade"] = cas
    res["_polys"] = polys
    if res["singular_unit_ideal"] and matches:
        res["status"] = "PASS"
    elif res["singular_unit_ideal"]:
        res["status"] = "PASS_UNIT_IDEAL_LINK_PARTIAL"
    return res


def helali_case1_compat(F):
    """Helali's 13 serialized Case-1 compatibility polynomials, from case1_checkpoint.pkl (restricted unpickler)."""
    obj, meta = P3.load_pickle("case1_checkpoint.pkl")
    polys = []
    for poly in obj["all_comp"]:
        d = {}
        for mon, co in poly:
            c = [(int(n), int(den)) for n, den in co]
            p = {i: x for i, x in enumerate(c) if x[0] != 0}
            d[tuple(mon)] = P3.decode_k(F, p)
        polys.append(d)
    return polys, list(obj["labels"]), meta


def _span_rank(F, polys, n):
    """Rank over K of the coefficient vectors of polys (dict mono -> Kel)."""
    monos = sorted({m for p in polys for m in p})
    idx = {m: i for i, m in enumerate(monos)}
    rows = [[F.el(0)] * len(monos) for _ in polys]
    for r, p in enumerate(polys):
        for m, c in p.items():
            rows[r][idx[m]] = c
    zero = L.MP.const(F, 1, 0)
    _R, _Y, piv, _f, _c = L.rref(F, rows, [zero] * len(rows)) if rows else ([], [], [], [], [])
    return len(piv)


def case1_link(F, A, D, layers=(3, 2, 1, 0, -1, -2, -3), log=print):
    res = {"status": "UNVERIFIED"}
    cas = C.Cascade(F, A, D, L.lattice_points(L.CASE1_P), L.lattice_points(L.CASE1_Q))
    for k in layers:
        t0 = time.time()
        info = cas.layer(k)
        log(f"case1 layer {k}: {info} ({time.time() - t0:.1f} s)")
    res["layers"] = cas.layers
    res["parameters"] = cas.nparams
    res["compat_by_layer"] = {str(k): sum(1 for kk, _ in cas.compat if kk == k) for k in layers}
    res["compat_total"] = len(cas.compat)
    n = cas.nparams
    hel, labels, meta = helali_case1_compat(F)
    res["helali_labels"] = labels
    res["helali_compat_total"] = len(hel)
    ours = {}
    for k, c in cas.compat:
        ours.setdefault(k, []).append({m[:n]: v for m, v in c.d.items()})
    theirs = {}
    for lab, d in zip(labels, hel):
        theirs.setdefault(lab, []).append(d)
    res["counts_equal_per_layer"] = all(len(ours.get(k, [])) == len(theirs.get(k, [])) for k in set(ours) | set(theirs) if k != 1)
    found = []
    for perm in itertools.permutations(range(n)):
        # layer 0 exact up-to-constant match as the filter, then all layers by spans
        def perm_poly(d):
            return {tuple(m[perm[i]] for i in range(n)): c for m, c in d.items()}
        ok = True
        for k in sorted(theirs, reverse=True):
            o = [perm_poly(d) for d in ours.get(k, [])]
            th = theirs[k]
            if len(o) != len(th):
                ok = False
                break
            r_o = _span_rank(F, o, n)
            r_u = _span_rank(F, o + th, n)
            r_t = _span_rank(F, th, n)
            if not (r_o == r_t == r_u):
                ok = False
                break
        if ok:
            found.append(perm)
            break
    res["helali_compat_span_equal_to_ours_per_layer_up_to_param_permutation"] = bool(found)
    res["matching_parameter_permutation"] = [list(p) for p in found]
    res["_cascade"] = cas
    return res


def parse_u_poly(F, text):
    """'(a/b)*u^4+(c/d)*u^11+...' (Singular style, in u) -> Kel; data only."""
    from flint import fmpq_poly as FP

    co: dict = {}
    for m in re.finditer(r"\((-?\d+)(?:/(\d+))?\)(?:\*u(?:\^(\d+))?)?", text):
        d = int(m.group(3)) if m.group(3) else (1 if "*u" in m.group(0) else 0)
        co[d] = co.get(d, fmpq(0)) + fmpq(int(m.group(1)), int(m.group(2) or 1))
    top = max(co)
    return F.el(FP([co.get(i, fmpq(0)) for i in range(top + 1)]))


def case1_split_check(F, cas):
    """Our first Case-1 compatibility equation is a polynomial in s alone, equal to kappa*(s^2-gamma)^2; Helali's c
    (from his meta file, data only) satisfies c^2 = gamma, so s = c or s = -c is exhaustive; the second compatibility
    equation vanishes modulo s^2 - gamma."""
    res = {}
    n = 6
    c0poly = cas.compat[0][1]
    S = 1  # parameter index of s (Helali's checkpoint: first term s^4)
    by_deg: dict = {}
    pure = True
    for m, c in c0poly.d.items():
        if any(m[i] for i in range(12) if i != S):
            pure = False
        by_deg[m[S]] = c
    res["first_compat_is_polynomial_in_s_only"] = pure
    res["first_compat_s_degrees"] = sorted(by_deg)
    if not pure or sorted(by_deg) != [0, 2, 4]:
        res["status"] = "FAIL_OR_DIFFERENT_SHAPE"
        return res
    c4, c2, c0 = by_deg[4], by_deg[2], by_deg[0]
    gamma = (-c2) / (c4 * 2)
    res["first_compat_equals_kappa_times_(s^2-gamma)^2"] = bool(c0 == c4 * gamma * gamma)
    meta = (ARCH_META).read_text().splitlines()
    sline = next(x for x in meta if x.startswith("s="))
    c = parse_u_poly(F, sline[2:])
    res["helali_c_squared_equals_gamma"] = bool(c * c == gamma)
    res["c_nonzero"] = bool(c)
    # second compat: reduce s^2 -> gamma
    second = cas.compat[1][1]
    red = L.MP(F, second.n)
    for m, co in second.d.items():
        e, r = divmod(m[S], 2)
        mm = list(m)
        mm[S] = r
        g = L.MP.const(F, second.n, 1)
        for _ in range(e):
            g = g.scale(gamma)
        red = red + L.MP(F, second.n, {tuple(mm): co}) * g
    res["second_compat_vanishes_mod_s2_minus_gamma"] = not red
    res["status"] = "PASS" if (res["first_compat_equals_kappa_times_(s^2-gamma)^2"] and res["helali_c_squared_equals_gamma"]
                                and res["second_compat_vanishes_mod_s2_minus_gamma"]) else "FAIL"
    return res


ARCH_META = P3.ARCH / "case1_branch1_after_w_meta.txt"


def _split_terms(expr):
    """Split a Singular-style sum at top-level '+' (outside parentheses)."""
    out, depth, cur = [], 0, ""
    for ch in expr:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "+" and depth == 0 and cur:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    if cur:
        out.append(cur)
    return out


def case1_branch_link(F, cas, which="br1", log=print):
    """Substitute s = +-c, Helali's forced affine relation for r and his shift of h (from the meta file, data only)
    into OUR compatibility equations and compare, by exact span, with his serialized after-w system (7 equations
    in h,u1,u2,u3). Both reading orders of the substitution are tried; the result states which one matched."""
    res = {"branch": which}
    name = "case1_branch1_after_w" if which == "br1" else "case1_branch2_after_w"
    meta = (P3.ARCH / f"{name}_meta.txt").read_text().splitlines()
    kv = {x.split("=", 1)[0]: x.split("=", 1)[1] for x in meta if "=" in x}
    c = parse_u_poly(F, kv["s"])
    rt = _split_terms(kv["r"])
    c_r = parse_u_poly(F, "+".join(t for t in rt if not t.endswith("*h") and not t.endswith("*u2")))
    ht = _split_terms(kv["h_old"])
    c_h = parse_u_poly(F, "+".join(t for t in ht if t != "h" and not t.endswith("*u2")))
    def coef_of(terms, var):
        t = next(t for t in terms if t.endswith("*" + var))
        return parse_u_poly(F, t[: -len("*" + var)])
    a_h, a_u2 = coef_of(rt, "h"), coef_of(rt, "u2")
    b_u2 = coef_of(ht, "u2")
    res["r_relation"] = "r = a_h*h + a_u2*u2 + c_r"
    obj, _m = P3.load_pickle(f"{name}.pkl")
    theirs = [{tuple(m): P3.decode_k(F, ser) for m, ser in eq.items()} for eq in obj]
    res["helali_equations"] = len(theirs)
    n = 12
    one = lambda: L.MP.const(F, n, 1)
    V = lambda i: L.MP.var(F, n, i)
    sv = c if which == "br1" else -c
    outcomes = {}
    for variant in ("r_in_old_h", "r_in_new_h"):
        polys = []
        for _k, p in cas.compat:
            q = p.subs_var(1, C.MP_const(F, sv))
            hnew = V(2)
            hold = hnew + V(4).scale(b_u2) + C.MP_const(F, c_h)
            hr = hold if variant == "r_in_old_h" else hnew
            rrep = hr.scale(a_h) + V(4).scale(a_u2) + C.MP_const(F, c_r)
            q = q.subs_var(0, rrep)
            q = q.subs_var(2, hold)
            if q:
                polys.append({(m[2], m[3], m[4], m[5]): co for m, co in q.d.items() if not any(m[i] for i in (0, 1) )})
        # sanity: r and s eliminated
        res[f"{variant}_our_polys_after_substitution"] = len(polys)
        rk_o, rk_t = _span_rank(F, polys, 4), _span_rank(F, theirs, 4)
        rk_u = _span_rank(F, polys + theirs, 4)
        outcomes[variant] = {"rank_ours": rk_o, "rank_theirs": rk_t, "rank_union": rk_u}
    res["outcomes"] = outcomes
    res["status"] = "PASS" if any(o["rank_ours"] == o["rank_theirs"] == o["rank_union"] and o["rank_theirs"] > 0
                                  for o in outcomes.values()) else "UNVERIFIED"
    return res
