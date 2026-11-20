"""EXP-013 routine: the endomorphism phi of U(H) with phi(x) = f, phi(y) = g (phi(z) = f g - g f, computed), the substitution into
the stored generators of a left ideal, the scaling of a Betti table, and the first instrument (`uhlib`: module construction and
`tor.betti`).  The cases are fixed by hypothesis.md (frozen) and listed at the end.

Polynomials of U are dicts {(a, b, c): coefficient} for x^a y^b z^c (PBW basis, y x = x y - z), coefficients modulo p.
`uhlib` and the polynomial helpers of EXP-011 (`exp011_routine`) are imported, read-only.
"""
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPS = HERE.parent
CODE = HERE.parents[1] / "code"
for extra in (CODE, EXPS / "EXP-011-central-pair-machine-checks"):
    if str(extra) not in sys.path:
        sys.path.append(str(extra))  # appended: the EXP-011 folder also holds a make_summary.py that must not shadow ours

import exp011_routine as R11  # noqa: E402
from uhlib import algebra as A  # noqa: E402
from uhlib import fields as UF  # noqa: E402
from uhlib import tor  # noqa: E402
from uhlib.fastmod import quotient_module_np  # noqa: E402

mul, add, sub, red = R11.mul, R11.add, R11.sub, R11.red
poly_list, poly_from_list, poly_text = R11.poly_list, R11.poly_from_list, R11.poly_text
table_rows, rows_to_table, pure_table = R11.table_rows, R11.rows_to_table, R11.pure_table

ONE = {(0, 0, 0): 1}
X_, Y_, Z_ = {(1, 0, 0): 1}, {(0, 1, 0): 1}, {(0, 0, 1): 1}
LETTER = {"x": X_, "y": Y_, "z": Z_}


# ------------------------------------------------------------------ polynomials from words (products in U)
def from_words(terms, p):
    """terms: list of (coefficient, word) with word a string over x, y, z (the empty word is 1); the product is taken in U, so
    the result is in the PBW basis (y x = x y - z)."""
    out = {}
    for c, word in terms:
        w = dict(ONE)
        for ch in word:
            w = mul(w, LETTER[ch], p)
        out = add(out, {m: (c * v) % p for m, v in w.items()}, p)
    return out


def power(poly, n, p, cache=None):
    cache = cache if cache is not None else {}
    if n not in cache:
        cache[n] = dict(ONE) if n == 0 else mul(power(poly, n - 1, p, cache), poly, p)
    return cache[n]


# ------------------------------------------------------------------ the endomorphism
def make_phi(f, g, p):
    """phi as a dict with the images of x, y, z; phi(z) = phi(x) phi(y) - phi(y) phi(x), computed."""
    return {"p": p, "x": f, "y": g, "z": sub(mul(f, g, p), mul(g, f, p), p), "cache": {}, "pw": ({}, {}, {})}


def phi_mono(phi, m):
    """phi(x^a y^b z^c) = phi(x)^a phi(y)^b phi(z)^c, products in U."""
    key = tuple(m)
    c = phi["cache"]
    if key not in c:
        p = phi["p"]
        a, b, k = key
        pw = phi["pw"]
        c[key] = mul(mul(power(phi["x"], a, p, pw[0]), power(phi["y"], b, p, pw[1]), p), power(phi["z"], k, p, pw[2]), p)
    return c[key]


def phi_poly(phi, poly):
    """phi extended linearly."""
    p = phi["p"]
    out = {}
    for m, coef in poly.items():
        out = add(out, {mm: (coef * v) % p for mm, v in phi_mono(phi, m).items()}, p)
    return out


def phi_degree(phi):
    return max(A.deg(m) for m in phi["x"])


# ------------------------------------------------------------------ tables
def scale_table(table, d):
    """The table with every degree multiplied by d: b(i, j) -> b(i, d j)."""
    return {(i, d * j): r for (i, j), r in table.items()}


def compare(table_phi, length_phi, table_base, length_base, d):
    """The two comparisons of the hypothesis between COMPUTED data: the table of phi^* M' against the table of M' with degrees
    multiplied by d, and the length of phi^* M' against d^3 times the length of M'.  None when an input is missing."""
    t_eq = None if table_phi is None or table_base is None else table_phi == scale_table(table_base, d)
    l_eq = None if length_phi is None or length_base is None else length_phi == d ** 3 * length_base
    return {"table_is_scaled_table": t_eq, "length_is_d3_times": l_eq}


# ------------------------------------------------------------------ first instrument
def betti_uhlib(p, gens, maxdeg):
    """gens: list of polynomials (generators of a left ideal).  Returns a record with the table and the length when the module
    is finite within maxdeg (three zero degrees), else the dimensions found."""
    t0 = time.time()
    F = UF.make_field(p, 1)
    rels = [{(0, m): c for m, c in gpoly.items()} for gpoly in gens]
    M = quotient_module_np(F, [0], rels, maxdeg=maxdeg)
    dims = [M.dim(j) for j in range(M.lo, M.hi + 1)]
    if not M.finished:
        return {"status": "module not finite within degree %d" % maxdeg, "table": None, "length": None, "dims": dims,
                "top_degree": None, "seconds": round(time.time() - t0, 2)}
    tab = tor.betti(M)
    return {"status": "computed", "table": table_rows(tab), "length": M.total_dim(), "dims": dims, "top_degree": M.hi,
            "seconds": round(time.time() - t0, 2)}


def maxdeg_for(top_degree_base, d):
    """Degree bound for phi^* M': the top degree of phi^* M' is d t' + 4 (d - 1) (Hilbert series of the note), plus a margin of 6
    so that the three zero degrees required by `uhlib` fit."""
    return d * top_degree_base + 4 * (d - 1) + 6


# ------------------------------------------------------------------ cases (hypothesis.md)
ENDO = {  # name: (p, f terms, g terms) as lists of (coefficient, word)
    "A3": (3, [(1, "xxx"), (1, "yz")], [(1, "yyy"), (1, "xz")]),
    "A5": (5, [(1, "x" * 5), (1, "yzz")], [(1, "y" * 5), (1, "xzz")]),
    "B4": (3, [(1, "x" * 4), (1, "zz")], [(1, "y" * 4), (1, "zz")]),
    "B6": (5, [(1, "x" * 6), (1, "zzz")], [(1, "y" * 6), (1, "zzz")]),
    "B8": (7, [(1, "x" * 8), (1, "zzzz")], [(1, "y" * 8), (1, "zzzz")]),
    "FR5": (5, [(1, "x" * 5)], [(1, "y" * 5)]),
    "N2MAP": (7, [(1, "x" * 5), (1, "yyyz")], [(1, "y" * 5), (1, "xxxz")]),
}
MODS = {  # name: (p, generators as lists of (coefficient, word), text)
    "Q3": (3, [[(1, "xx"), (1, "yy"), (1, "yx")], [(1, "xx"), (1, "yx"), (-1, "z")]],
           "U/(U(x^2 + y^2 + yx) + U(x^2 + yx - z))"),
    "P2_5": (5, [[(1, "xx")], [(1, "yy")]], "U/(U x^2 + U y^2)"),
    "P2_7": (7, [[(1, "xx")], [(1, "yy")]], "U/(U x^2 + U y^2)"),
    "P3_7": (7, [[(1, "xxx")], [(1, "yyy")]], "U/(U x^3 + U y^3)"),
    "C3": (3, [[(1, "xxx"), (1, "yz")], [(1, "yyy"), (1, "xz")]], "U/(U(x^3 + y z) + U(y^3 + x z))"),
    "L": (3, [[(1, "x")], [(1, "yy")]], "U/(U x + U y^2)"),
    "L5": (5, [[(1, "x")], [(1, "yy")]], "U/(U x + U y^2)"),
    "T": (3, [[(1, "xx")], [(1, "xy")], [(1, "yy")], [(1, "z")]], "U/(U x^2 + U x y + U y^2 + U z)"),
}
# (id, family, endomorphism, module, what is compared)
CASES = [
    ("S1", "S", "A3", "Q3", "pair of degree 6"), ("S2", "S", "B4", "Q3", "pair of degree 8"),
    ("S3", "S", "B6", "P2_5", "pair of degree 12"), ("S4", "S", "A5", "P2_5", "pair of degree 10"),
    ("S5", "S", "B8", "P2_7", "pair of degree 16"), ("S6", "S", "A3", "C3", "pair of degree 9"),
    ("S7", "S", "B8", "P3_7", "pair of degree 24"),
    ("T1", "T", "A3", "L", "table not pure, degrees multiplied by 3"), ("T2", "T", "B6", "L5", "same, multiplied by 6"),
    ("T3", "T", "B4", "T", "same for T, multiplied by 4"),
    ("N1", "N", "FR5", "P2_5", "phi(z) = 0, outside the hypotheses"),
    ("N2", "N", "N2MAP", "P2_7", "commutator not central, outside the hypotheses"),
]
RUN_ORDER = ["S1", "S2", "S6", "T1", "T3", "S3", "S4", "T2", "S5", "N1", "N2", "S7"]
EXPECTED_LENGTH = {"S1": 216, "S2": 512, "S3": 1728, "S4": 1000, "S5": 4096, "S6": 729, "S7": 13824}
G1_PAIRS = ("A3", "A5", "B4", "B6", "B8")
G1_PURE_MODULES = ("Q3", "P2_5", "P2_7", "P3_7", "C3")
G1_LENGTH_3 = ("L", "T")


def case_ids():
    return [c[0] for c in CASES]


def case_spec(cid):
    for c in CASES:
        if c[0] == cid:
            return {"id": c[0], "family": c[1], "endo": c[2], "mod": c[3], "what": c[4]}
    raise KeyError(cid)


def endo_phi(name):
    p, fterms, gterms = ENDO[name]
    return make_phi(from_words(fterms, p), from_words(gterms, p), p)


def mod_gens(name):
    return [from_words(t, MODS[name][0]) for t in MODS[name][1]]


def case_setup(cid):
    """The data of a case built from the definitions only: the endomorphism, the generators of M' (PBW) and the images of exactly
    those generators."""
    s = case_spec(cid)
    phi = endo_phi(s["endo"])
    assert MODS[s["mod"]][0] == phi["p"], "field mismatch in " + cid
    gens = mod_gens(s["mod"])
    imgs = [phi_poly(phi, g) for g in gens]
    return s, phi, gens, imgs


def case_record(cid):
    """Everything the first instrument computes for one case (run in a worker)."""
    t0 = time.time()
    s, phi, gens, imgs = case_setup(cid)
    p, d = phi["p"], phi_degree(phi)
    rec = {"id": cid, "family": s["family"], "what": s["what"], "p": p, "d": d, "endomorphism": s["endo"],
           "module": s["mod"], "module_text": MODS[s["mod"]][2],
           "phi_x": poly_list(phi["x"]), "phi_y": poly_list(phi["y"]), "phi_z": poly_list(phi["z"]),
           "phi_x_text": poly_text(phi["x"]), "phi_y_text": poly_text(phi["y"]), "phi_z_text": poly_text(phi["z"]),
           "gens_base": [poly_list(g) for g in gens], "gens_base_text": [poly_text(g) for g in gens],
           "gens_phi": [poly_list(g) for g in imgs], "gens_phi_text": [poly_text(g) for g in imgs],
           "expected_length_phi": EXPECTED_LENGTH.get(cid)}
    rec["uhlib_base"] = betti_uhlib(p, gens, 60)
    top = rec["uhlib_base"]["top_degree"]
    rec["uhlib_phi"] = betti_uhlib(p, imgs, maxdeg_for(top if top is not None else 20, d))
    tb, tp = rows_to_table(rec["uhlib_base"]["table"]), rows_to_table(rec["uhlib_phi"]["table"])
    rec["scaled_table_base"] = None if tb is None else table_rows(scale_table(tb, d))
    rec["compare_uhlib"] = compare(tp, rec["uhlib_phi"]["length"], tb, rec["uhlib_base"]["length"], d)
    rec["singular_base"] = {"status": "not attempted"}
    rec["singular_phi"] = {"status": "not attempted"}
    rec["compare_singular"] = None
    rec["seconds"] = round(time.time() - t0, 2)
    return rec
