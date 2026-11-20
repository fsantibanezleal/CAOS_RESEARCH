"""Gate G3 of EXP-016 (boij-soderberg-realizability): the fast test of (b) against a reference with exact polynomial arithmetic (every form
of (6, 7) and (8, 5)), (C) against the description by roots (every form of (4, 13), roots in GF(13^2)), the rewriting of G in PBW monomials
against the powers of xy computed by uhlib, the arithmetic of GF(p^2) against python-flint, and the enumeration order."""
import importlib.util
import random
import sys
from pathlib import Path

import flint
import numpy as np

EXP16 = (Path(__file__).resolve().parents[1] / "problems" / "commutative-algebra" / "boij-soderberg-realizability" / "experiments"
         / "EXP-016-congruence-lists")
sys.path.insert(0, str(EXP16))
sys.path.insert(0, str(EXP16.parent / "EXP-010-weight-class-strata"))

import exp016_routine as R  # noqa: E402  (puts the code folder of uhlib on sys.path)
from uhlib import algebra as A  # noqa: E402
from uhlib.fields import ExtField  # noqa: E402


# ------------------------------------------------------------------ an independent exact reference (plain integers, lists low to high)
def pmul(a, b, p):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] = (out[i + j] + x * y) % p
    return out


def pshift(G, j, p):
    """G(h + j) for G given low to high."""
    out = [0]
    base = [1]
    for c in G:
        out = out + [0] * (len(base) - len(out))
        for i, b in enumerate(base):
            out[i] = (out[i] + c * b) % p
        base = pmul(base, [j % p, 1], p)
    return out


def pmod(a, G, p):
    a = list(a)
    m = len(G) - 1
    for i in range(len(a) - 1, m - 1, -1):
        q = a[i] % p
        if q:
            for t in range(m + 1):
                a[i - m + t] = (a[i - m + t] - q * G[t]) % p
    a = [x % p for x in a[:m]]
    return a + [0] * (m - len(a))


def ref_b(e, p, coeffs):
    """The exact test of (b) by plain integer lists: lambda, or None."""
    G = list(coeffs) + [1]
    A_e, B_e = [1], [1]
    for i in range(e):
        A_e = pmul(A_e, [i, 1], p)
        B_e = pmul(B_e, [(-(i + 1)) % p, 1], p)
    rm = pmod(pmul(pshift(G, -2 * e, p), B_e, p), G, p)
    rp = pmod(pmul(pshift(G, 2 * e, p), A_e, p), G, p)
    if not any(rm) or not any(rp):
        return None
    i = next(i for i, x in enumerate(rp) if x)
    lam = rm[i] * pow(rp[i], -1, p) % p
    return lam if all((lam * x - y) % p == 0 for x, y in zip(rp, rm)) else None


def digits(idx, p, m):
    out = []
    for _ in range(m):
        out.append(idx % p)
        idx //= p
    return out


# ------------------------------------------------------------------ (b)
def _check_b(e, p):
    F = R.Field(p)
    m = e // 2
    n = p ** m
    fast = set(R.fast_passing(e, F, 0, n).tolist())
    ref = {i for i in range(n) if ref_b(e, p, digits(i, p, m)) is not None}
    assert fast == ref, (sorted(fast - ref)[:5], sorted(ref - fast)[:5])
    for i in sorted(ref)[:40]:
        cs = R.form_from_index(e, F, i)
        assert R.exact_b(e, F, cs) == ref_b(e, p, cs)
    return fast


def test_fast_test_of_b_against_the_exact_reference_on_every_form_of_6_7():
    fast = _check_b(6, 7)
    assert len(fast) > 0


def test_fast_test_of_b_against_the_exact_reference_on_every_form_of_8_5():
    fast = _check_b(8, 5)
    assert len(fast) > 0


def test_fast_test_over_gf9_against_the_exact_test_with_python_flint():
    F = R.Field(3, 2)
    e, m = 4, 2
    n = F.q ** m
    fast = set(R.fast_passing(e, F, 0, n).tolist())
    exact = {i for i in range(n) if R.exact_b(e, F, R.form_from_index(e, F, i)) is not None}
    assert fast == exact
    assert exact


def test_fast_test_over_gf9_for_e6_against_the_exact_test():
    F = R.Field(3, 2)
    e, m = 6, 3
    n = F.q ** m
    fast = set(R.fast_passing(e, F, 0, n).tolist())
    exact = {i for i in range(n) if R.exact_b(e, F, R.form_from_index(e, F, i)) is not None}
    assert fast == exact


def test_blocks_by_index_agree_with_one_block():
    F = R.Field(5)
    whole = R.fast_passing(8, F, 0, 625).tolist()
    parts = []
    for a, b in ((0, 100), (100, 101), (101, 400), (400, 625)):
        parts += R.fast_passing(8, F, a, b).tolist()
    assert parts == whole


def test_the_lists_of_the_named_cases():
    def forms(e, p):
        F = R.Field(p)
        res = R.scan_range(e, F, 0, p ** (e // 2))
        return [tuple(r["coeffs"]) for r in res["list"]]
    assert forms(6, 7) == [(3, 0, 0), (3, 3, 4)]            # h^3 + 3 and h^3 + 4 h^2 + 3 h + 3
    assert forms(8, 5) == [(2, 0, 1, 3)]                    # h^4 + 3 h^3 + h^2 + 2
    assert len(forms(4, 7)) == 1 and len(forms(4, 11)) == 2 and len(forms(4, 13)) == 16 and len(forms(4, 17)) == 13


# ------------------------------------------------------------------ (C)
def test_condition_C_against_the_description_by_roots_on_every_form_of_4_13():
    e, p, m = 4, 13, 2
    F = R.Field(p, 1)
    ctx = flint.fq_default_ctx(13, 2)
    elems = [ctx(a) + ctx(b) * ctx.gen() for a in range(13) for b in range(13)]

    def roots_of(cs):
        out = []
        for z in elems:
            v = ctx(1)
            for c in reversed(cs):
                v = v * z + ctx(c)
            if v == 0:
                out.append(z)
        return out

    same = 0
    for idx in range(p ** m):
        cs = digits(idx, p, m)
        rts = roots_of(cs)
        bad = False
        for k in list(range(2, e + 1)) + list(range(-(e - 1), 0)):
            if any(z == ctx(k) for z in rts):
                bad = True
        if any(y - z == ctx(2 * e) for z in rts for y in rts):
            bad = True
        if any(z == 0 for z in rts) and any(z == 1 for z in rts):
            bad = True
        assert R.exact_C(e, F, cs) == (not bad), (cs, [str(z) for z in rts])
        same += 1
    assert same == 169


# ------------------------------------------------------------------ PBW rewriting
def _pbw_by_uhlib(e, p, k, comps):
    """sum_a c_a (xy)^a z^(m - a), with (xy)^a computed by uhlib's product, componentwise over GF(p)."""
    m = e // 2
    out = {}
    cur = {(0, 0, 0): 1}
    pw = [cur]
    for _ in range(m):
        pw.append(A.poly_mul_int(pw[-1], {(1, 1, 0): 1}))
    for a in range(m + 1):
        c = comps[a]
        for mono, v in pw[a].items():
            key = (mono[0], mono[1], mono[2] + m - a)
            cur = tuple((c[t] * v) % p for t in range(k))
            old = out.get(key, (0,) * k)
            out[key] = tuple((x + y) % p for x, y in zip(old, cur))
    return {mo: c for mo, c in out.items() if any(c)}


def test_pbw_rewriting_against_the_powers_of_xy_computed_by_uhlib():
    rng = random.Random(1)
    for e, p, k in ((6, 7, 1), (8, 5, 1), (10, 11, 1), (6, 13, 2), (8, 3, 2)):
        F = R.Field(p, k)
        m = e // 2
        for _ in range(12):
            cs = [F.elem(rng.randrange(F.q)) for _ in range(m)]
            g = R.pbw_g(e, F, cs)
            comps = [F.comps(c) for c in cs] + [(1,) + (0,) * (k - 1)]
            ref = _pbw_by_uhlib(e, p, k, comps)
            got = {mo: F.comps(c) for mo, c in g.items()}
            assert got == ref


# ------------------------------------------------------------------ GF(p^2)
def test_gf_p2_arithmetic_against_python_flint_and_uhlib():
    rng = random.Random(3)
    for p in (3, 7, 13):
        F = R.Field(p, 2)
        U = ExtField(p, 2)
        assert list(F.modulus) == list(U.modulus)
        ctx = flint.fq_default_ctx(modulus=flint.fmpz_mod_poly_ctx(p)(F.modulus))
        t = ctx.gen()

        def to_fl(a):
            return ctx(a[0]) + ctx(a[1]) * t
        for _ in range(200):
            a = (rng.randrange(p), rng.randrange(p))
            b = (rng.randrange(p), rng.randrange(p))
            prod = R.ext_mul(F, np.array([[a[0]], [a[1]]], dtype=np.int64), np.array([[b[0]], [b[1]]], dtype=np.int64))
            got = (int(prod[0][0]), int(prod[1][0]))
            assert to_fl(got) == to_fl(a) * to_fl(b)
            assert got == tuple(U.mul(a, b))
        # numbering a + b p
        assert F.elem(5 % (p * p)) == ((5 % (p * p)) % p, (5 % (p * p)) // p)


# ------------------------------------------------------------------ the enumeration order
def test_the_enumeration_order():
    F = R.Field(5)
    assert R.form_from_index(6, F, 0) == [0, 0, 0]
    assert R.form_from_index(6, F, 1) == [1, 0, 0]
    assert R.form_from_index(6, F, 5) == [0, 1, 0]
    assert R.form_from_index(6, F, 25) == [0, 0, 1]
    assert R.form_from_index(6, F, 124) == [4, 4, 4]
    seen = {tuple(R.form_from_index(6, F, i)) for i in range(125)}
    assert len(seen) == 125
    F2 = R.Field(3, 2)
    assert R.form_from_index(4, F2, 4) == [(1, 1), (0, 0)]      # a + b t numbered a + b p: 4 = 1 + 1 * 3
    assert R.form_from_index(4, F2, 9) == [(0, 0), (1, 0)]      # the second coefficient is the second digit in base 9
    assert len({tuple(R.form_from_index(4, F2, i)) for i in range(81)}) == 81


def test_the_module_of_a_form_of_a_list_has_length_e_cubed_and_the_pure_table():
    F = R.Field(7)
    cs = [3, 0, 0]                                           # h^3 + 3 at (6, 7)
    g = R.pbw_g(6, F, cs)
    out = R.first_instrument(6, F, g)
    assert out["length"] == 216 and out["pure"] is True
    assert out["betti"] == [[0, 0, 1], [1, 6, 2], [2, 18, 2], [3, 24, 1]]


def test_the_spec_is_importable_as_a_module_path():
    spec = importlib.util.spec_from_file_location("exp016_run_check", EXP16 / "run.py")
    assert spec is not None
