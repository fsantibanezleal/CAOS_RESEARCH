"""The cases of EXP-011, fixed by hypothesis.md (frozen): families T, G and N.  A case is a plain dict; `case_record` evaluates one
(identities, Hilbert function, length, and the Betti table by `uhlib` when e <= 9) and returns the record stored in results.json."""
import time

import exp011_routine as R

# family T: A = x^e, B = y^e;  (id, e, p, l_1 = (x coefficient, y coefficient), l_2)
T_CASES = [
    ("T1", 3, 3, (0, 1), (1, 0)), ("T2", 3, 3, (1, 1), (1, -1)),
    ("T3", 5, 5, (0, 1), (1, 0)), ("T4", 5, 5, (0, 2), (3, 0)),
    ("T5", 7, 7, (0, 1), (1, 0)), ("T6", 7, 7, (0, 3), (5, 0)), ("T7", 7, 7, (1, 0), (0, 1)),
    ("T8", 9, 3, (0, 1), (1, 0)), ("T9", 9, 3, (1, 1), (0, 1)),
    ("T10", 11, 11, (0, 1), (1, 0)), ("T11", 13, 13, (0, 1), (1, 0)),
    ("T12", 15, 3, (0, 1), (1, 0)), ("T13", 15, 5, (0, 1), (1, 0)),
]
# family G: l_1 = y, l_2 = x;  A, B as polynomials {(i, j): c} in X = x^p, Y = y^p
G_CASES = [
    ("G1", 9, 3, {(3, 0): 1, (1, 2): 1}, {(0, 3): 1, (2, 1): 1, (3, 0): 1}),
    ("G2", 5, 5, {(1, 0): 1, (0, 1): 2}, {(1, 0): 3, (0, 1): 2}),
    ("G3", 15, 5, {(3, 0): 1, (2, 1): 1}, {(0, 3): 1, (1, 2): 2, (3, 0): 1}),
]
# family N (outside the hypotheses): (id, e, p, A, B, l_1, l_2, why outside), A and B as forms {(a, b): c} in x, y
N_CASES = [
    ("N1", 5, 5, {(5, 0): 1}, {(0, 5): 1}, (0, 0), (1, 0), "l_1 = 0"),
    ("N2", 5, 5, {(5, 0): 1}, {(0, 5): 1}, (0, 1), (0, 1), "l_1, l_2 dependent"),
    ("N3", 5, 7, {(5, 0): 1}, {(0, 5): 1}, (0, 1), (1, 0), "p does not divide e"),
    ("N4", 5, 3, {(5, 0): 1}, {(0, 5): 1}, (0, 1), (1, 0), "p does not divide e"),
    ("N5", 9, 3, {(9, 0): 1}, {(6, 3): 1}, (0, 1), (1, 0), "A-bar, B-bar not coprime (common factor x^6)"),
]
BETTI_UHLIB_MAX_E = 9


def specs():
    """Every case as a spec dict, in the order of the hypothesis tables."""
    out = []
    for cid, e, p, l1, l2 in T_CASES:
        out.append({"id": cid, "family": "T", "e": e, "p": p, "A_form": {(e, 0): 1}, "B_form": {(0, e): 1}, "A_XY": None,
                    "B_XY": None, "l1": l1, "l2": l2, "why_outside": None})
    for cid, e, p, a_xy, b_xy in G_CASES:
        out.append({"id": cid, "family": "G", "e": e, "p": p, "A_XY": a_xy, "B_XY": b_xy, "A_form": R.xy_from_XY(p, a_xy),
                    "B_form": R.xy_from_XY(p, b_xy), "l1": (0, 1), "l2": (1, 0), "why_outside": None})
    for cid, e, p, a, b, l1, l2, why in N_CASES:
        out.append({"id": cid, "family": "N", "e": e, "p": p, "A_form": a, "B_form": b, "A_XY": None, "B_XY": None, "l1": l1,
                    "l2": l2, "why_outside": why})
    return out


def spec_of(cid):
    for s in specs():
        if s["id"] == cid:
            return s
    raise KeyError(cid)


def order_key(spec):
    """Family order T, G, N; within a family the cases with e <= 9 first, each group in table order."""
    return ("TGN".index(spec["family"]), spec["e"] > BETTI_UHLIB_MAX_E, 0)


def sort_specs(lst):
    idx = {s["id"]: i for i, s in enumerate(specs())}
    return sorted(lst, key=lambda s: (order_key(s), idx[s["id"]]))


def _prepare(spec):
    """Applies the coprimality test of G1 and G3 (replacement of the X^3 coefficient of B when it fails) and returns the forms."""
    e, p = spec["e"], spec["p"]
    a_form, b_form = dict(spec["A_form"]), dict(spec["B_form"])
    res = R.resultant_mod(p, a_form, b_form, e) if spec["family"] in ("T", "G") else None
    replacement = None
    if spec["family"] == "G" and res == 0:
        c0 = spec["B_XY"][(3, 0)]
        for k in range(1, p):
            b_xy = dict(spec["B_XY"])
            b_xy[(3, 0)] = (c0 + k) % p
            b_try = R.xy_from_XY(p, {m: c for m, c in b_xy.items() if c})
            r2 = R.resultant_mod(p, a_form, b_try, e)
            if r2 != 0:
                replacement = {"old_coefficient_of_X3_in_B": c0, "new_coefficient_of_X3_in_B": (c0 + k) % p,
                               "resultant_before": res, "resultant_after": r2}
                b_form, res = b_try, r2
                break
    return a_form, b_form, res, replacement


def case_record(spec):
    """Everything computed in the worker for one case.  The Betti table by `uhlib` is done here only for e <= 9."""
    t0 = time.time()
    e, p = spec["e"], spec["p"]
    a_form, b_form, res, replacement = _prepare(spec)
    f, g = R.build_pair(e, p, a_form, b_form, spec["l1"], spec["l2"])
    a_poly = {(a, b, 0): c % p for (a, b), c in a_form.items()}
    b_poly = {(a, b, 0): c % p for (a, b), c in b_form.items()}
    ident = R.identities(e, p, f, g, a_poly, b_poly)
    t1 = time.time()
    top = 4 * e + 2 if spec["family"] != "N" else 5 * e
    dims = R.hilbert(p, e, f, g, top, stop_at_zero=spec["family"] == "N")
    t2 = time.time()
    he = [R.h_e(e, n) for n in range(4 * e + 3)]
    if spec["family"] == "N":
        n0 = next((n for n in range(e, len(dims)) if dims[n] == 0), None)
        finite = n0 is not None
    else:
        finite = dims[4 * e + 2] == 0
    rec = {
        "id": spec["id"], "family": spec["family"], "e": e, "p": p, "s": (e - 1) // 2,
        "A_in_xy": [[list(m), c] for m, c in sorted(a_form.items())], "B_in_xy": [[list(m), c] for m, c in sorted(b_form.items())],
        "A_XY": None if spec["A_XY"] is None else [[list(m), c] for m, c in sorted(spec["A_XY"].items())],
        "B_XY": None if spec["B_XY"] is None else [[list(m), c] for m, c in sorted(spec["B_XY"].items())],
        "l1": list(spec["l1"]), "l2": list(spec["l2"]), "l1_mod_p": [c % p for c in spec["l1"]],
        "l2_mod_p": [c % p for c in spec["l2"]], "why_outside": spec["why_outside"],
        "f": R.poly_list(f), "g": R.poly_list(g), "f_text": R.poly_text(f), "g_text": R.poly_text(g),
        "lambda_formula": R.lam_formula(spec["l1"], spec["l2"], p), "lambda": ident["lambda"],
        "identities": ident, "resultant_AB": res, "replacement": replacement,
        "hilbert": dims, "h_e": he, "hilbert_equals_h_e": dims[:4 * e + 3] == he,
        "finite_length": finite, "length": sum(dims) if finite else None,
        "dims_found": dims if not finite else None, "length_equals_e3": finite and sum(dims) == e ** 3,
        "betti_uhlib": {"status": "not attempted", "table": None, "pure": None, "seconds": None},
        "betti_singular": {"status": "not attempted", "table": None, "pure": None, "seconds": None, "error": None},
        "seconds_identities": round(t1 - t0, 2), "seconds_hilbert": round(t2 - t1, 2),
    }
    if e <= BETTI_UHLIB_MAX_E and finite:
        rec["betti_uhlib"] = betti_record(p, e, f, g)
    elif e <= BETTI_UHLIB_MAX_E:
        rec["betti_uhlib"] = {"status": "module not finite within degree 5e; no table", "table": None, "pure": False,
                              "seconds": 0.0}
    rec["seconds"] = round(time.time() - t0, 2)
    return rec


def betti_record(p, e, f, g):
    tab, length, secs = R.betti_uhlib(p, e, f, g)
    if tab is None:
        return {"status": "module not finite within degree %d" % (4 * e + 8), "table": None, "pure": False,
                "seconds": round(secs, 2)}
    return {"status": "computed", "table": R.table_rows(tab), "pure": tab == R.pure_table(e), "length": length,
            "seconds": round(secs, 2)}
