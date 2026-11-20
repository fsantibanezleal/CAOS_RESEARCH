"""EXP-005 routine: the Hilbert function of a presentation over U(H), the classifier, the case generators.

First instrument of EXP-005.  It uses `uhlib` for the algebra (PBW monomials and the product), the fields and the
enumeration of subspaces, and carries its OWN rank computation (the module construction of `uhlib` is not used
here; gate G2 compares the two).  Exact arithmetic only: integers modulo a prime, tables of GF(2^k), Fractions.

A presentation is  M = U^a / (U F_1 + ... + U F_b),  generators in degree 0, F_j homogeneous of degree e in (U_e)^a,
given as dicts {(component, (i, j, k)): coefficient} (coefficient a field element of uhlib).
dim M_n = a dim U_n - rank of the span of { mu * F_j : mu a PBW monomial of degree n - e } in (U_n)^a  (LEFT multiples).
"""
import json
import random
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
CODE = HERE.parents[1] / "code"
if str(CODE) not in sys.path:
    sys.path.insert(0, str(CODE))

import numpy as np  # noqa: E402
from uhlib import algebra as A  # noqa: E402
from uhlib import structure as S  # noqa: E402
from uhlib.fields import QQ, CachedExtField, PrimeField  # noqa: E402

SEED_BASE = 20261120


class CaseTimeout(Exception):
    """The per-case time limit was reached; `partial` holds the dimensions computed so far."""

    def __init__(self, partial):
        super().__init__("time limit")
        self.partial = partial


# ------------------------------------------------------------------ fields with the stated moduli
class BinaryField(CachedExtField):
    """GF(2^k) with a stated modulus (low to high coefficients), checked irreducible; same API as uhlib's fields."""

    def __init__(self, k, modulus):
        super().__init__(2, k)
        modulus = list(modulus)
        assert len(modulus) == k + 1 and modulus[-1] == 1
        from uhlib.fields import _is_irreducible
        assert _is_irreducible(modulus, 2), "modulus is reducible"
        self.modulus = modulus
        self._mul, self._add, self._inv = {}, {}, {}


MODULI = {"GF(2^2)": (2, [1, 1, 1]), "GF(2^4)": (4, [1, 1, 0, 0, 1])}  # w^2+w+1, w^4+w+1


def make_field(name):
    """'QQ', 'GF(2)', 'GF(2^2)', 'GF(2^4)' (stated moduli) or 'GF(p)' for a prime p."""
    if name == "QQ":
        return QQ()
    if name in MODULI:
        k, mod = MODULI[name]
        return BinaryField(k, mod)
    assert name.startswith("GF(") and name.endswith(")") and "^" not in name, name
    return PrimeField(int(name[3:-1]))


def field_record(F):
    return {"name": F.name, "char": F.char, "degree": F.degree, "modulus": getattr(F, "modulus", None)}


# ------------------------------------------------------------------ the product and the dense rows
def left_multiple(F, mu, rel):
    """mu * rel for a PBW monomial mu = (i, j, k) and rel = {(comp, mono): c}: the LEFT multiple, as a dict."""
    out = {}
    for (k, m), c in rel.items():
        for mm, kk in A.mono_mul(mu, m):
            t = F.mul(c, F.from_int(kk))
            key = (k, mm)
            out[key] = F.add(out[key], t) if key in out else t
    return {key: c for key, c in out.items() if not F.is_zero(c)}


class _Codec:
    """Encoding of field elements as integers, and the row operations, for one field."""

    def __init__(self, F):
        self.F = F
        if isinstance(F, PrimeField):
            self.kind, self.p = ("bit" if F.p == 2 else "prime"), F.p
        elif isinstance(F, CachedExtField) and F.p == 2 and F.k <= 8:
            self.kind, self.q = "bin", 1 << F.k
            elts = [tuple((n >> i) & 1 for i in range(F.k)) for n in range(self.q)]
            self.MUL = np.array([[self._enc(F.mul(elts[a], elts[b])) for b in range(self.q)] for a in range(self.q)],
                                dtype=np.uint8)
            self.INV = np.array([0] + [self._enc(F.inv(elts[a])) for a in range(1, self.q)], dtype=np.uint8)
            assert all(self.MUL[a, self.INV[a]] == 1 for a in range(1, self.q))
        else:
            self.kind = "generic"

    def _enc(self, a):
        return sum(int(c) << i for i, c in enumerate(a))

    def enc(self, c):
        if self.kind in ("prime", "bit"):
            return int(c) % self.p
        if self.kind == "bin":
            return self._enc(c)
        return c


def _row_entries(codec, a, rels, n, e_list, pos, dn):
    """Yield, for every left multiple mu * F_j of degree n, its sparse row {column: encoded coefficient}."""
    F = codec.F
    kind = codec.kind
    for rel, e in zip(rels, e_list):
        if e > n:
            continue
        enc = [(k, m, codec.enc(c)) for (k, m), c in rel.items()]
        for u in A.monos(n - e):
            row = {}
            for k, m, c in enc:
                base = k * dn
                for mm, kk in A.mono_mul(u, m):
                    col = base + pos[mm]
                    if kind == "bit":
                        if kk & 1:
                            row[col] = row.get(col, 0) ^ 1
                    elif kind == "bin":
                        if kk & 1:
                            row[col] = row.get(col, 0) ^ c
                    elif kind == "prime":
                        row[col] = (row.get(col, 0) + c * kk) % codec.p
                    else:
                        t = F.mul(c, F.from_int(kk))
                        row[col] = F.add(row[col], t) if col in row else t
            yield row


def _rank_bitset(rows, ncols):
    basis = {}
    for row in rows:
        v = 0
        for col, c in row.items():
            if c:
                v |= 1 << col
        while v:
            low = v.bit_length() - 1
            b = basis.get(low)
            if b is None:
                basis[low] = v
                break
            v ^= b
    return len(basis)


def _rank_dense(codec, rows, ncols):
    """Rank of rows (list of sparse dicts) over a prime field p > 2 or GF(2^k): row echelon form with numpy."""
    if not rows:
        return 0
    A_ = np.zeros((len(rows), ncols), dtype=np.int64 if codec.kind == "prime" else np.uint8)
    for i, row in enumerate(rows):
        for col, c in row.items():
            A_[i, col] = c
    m, n = A_.shape
    r = 0
    for j in range(n):
        if r >= m:
            break
        nz = np.nonzero(A_[r:, j])[0]
        if nz.size == 0:
            continue
        piv = r + int(nz[0])
        if piv != r:
            A_[[r, piv]] = A_[[piv, r]]
        if codec.kind == "prime":
            inv = pow(int(A_[r, j]), -1, codec.p)
            A_[r, j:] = (A_[r, j:] * inv) % codec.p
        else:
            A_[r, j:] = codec.MUL[codec.INV[A_[r, j]], A_[r, j:]]
        below = r + 1 + np.nonzero(A_[r + 1:, j])[0]
        if below.size:
            f = A_[below, j]
            if codec.kind == "prime":
                A_[np.ix_(below, np.arange(j, n))] = (A_[below, j:] - f[:, None] * A_[r, j:][None, :]) % codec.p
            else:
                A_[below, j:] ^= codec.MUL[f[:, None], A_[r, j:][None, :]]
        r += 1
    return r


def _rank_generic(F, rows, ncols):
    """Exact elimination through the field API (QQ, or any field object)."""
    piv = {}
    for row in rows:
        v = {c: x for c, x in row.items() if not F.is_zero(x)}
        while v:
            col = min(v)
            if col in piv:
                pr = piv[col]
                f = v[col]
                for c2, x in pr.items():
                    t = F.sub(v.get(c2, F.zero), F.mul(f, x))
                    if F.is_zero(t):
                        v.pop(c2, None)
                    else:
                        v[c2] = t
            else:
                inv = F.inv(v[col])
                piv[col] = {c2: F.mul(inv, x) for c2, x in v.items()}
                break
    return len(piv)


def hilbert_function(F, a, relations, D, deadline=None):
    """[dim M_0, ..., dim M_D] of M = U^a / (U F_1 + ... + U F_b), generators in degree 0, exact over F.

    `deadline` is a time.time() value; reaching it raises CaseTimeout(partial list of the degrees done)."""
    codec = _Codec(F)
    rels, e_list = [], []
    for rel in relations:
        rel = {key: c for key, c in rel.items() if not F.is_zero(c)}
        if not rel:
            continue  # the zero relation spans nothing
        degs = {A.deg(m) for (_, m) in rel}
        assert len(degs) == 1, "relation is not homogeneous"
        rels.append(rel)
        e_list.append(degs.pop())
    out = []
    for n in range(D + 1):
        if deadline is not None and time.time() > deadline:
            raise CaseTimeout(out)
        dn = A.dim_U(n)
        pos = {m: i for i, m in enumerate(A.monos(n))}
        ncols = a * dn
        rows = list(_row_entries(codec, a, rels, n, e_list, pos, dn))
        if codec.kind == "bit":
            rk = _rank_bitset(rows, ncols)
        elif codec.kind in ("prime", "bin"):
            rk = _rank_dense(codec, rows, ncols)
        else:
            rk = _rank_generic(F, rows, ncols)
        out.append(ncols - rk)
    return out


# ------------------------------------------------------------------ the classifier
FINITE, CONSTANT, GROWING, UNCLASSIFIED = "finite length", "eventually constant", "growing", "unclassified"


def classify(h):
    """Classification of h(0..D) literally as the hypothesis words it.  Returns (class, value or None)."""
    D = len(h) - 1
    if any(v == 0 for v in h):
        return FINITE, None
    last = h[-6:]
    if len(last) == 6 and last[0] > 0 and all(v == last[0] for v in last):
        return CONSTANT, last[0]
    if D >= 6 and h[D] >= h[D - 6] > 0:
        return GROWING, None
    return UNCLASSIFIED, None


# ------------------------------------------------------------------ the cases
# family: (field names, shape (a, b, e), number of random cases per field, degree bound D)
RANDOM_FAMILIES = {
    "C2a": (("GF(2)", "GF(2^2)", "GF(2^4)"), (1, 2, 4), 120, 24),
    "C2b": (("GF(2)", "GF(2^2)", "GF(2^4)"), (1, 2, 5), 120, 28),
    "C2c": (("GF(2^4)",), (1, 2, 6), 10, 30),
    "C2d": (("GF(2^4)",), (1, 2, 7), 10, 32),
    "C2e": (("GF(2)", "GF(2^2)", "GF(2^4)"), (2, 3, 3), 20, 22),
    "C2f": (("GF(2^4)",), (2, 3, 2), 20, 20),
    "C2g": (("GF(2^4)",), (3, 4, 2), 5, 18),
}
C3_SHAPES = ((1, 3, 2), (1, 3, 3), (1, 3, 4), (2, 4, 2))
C3_D = 24
C1_FAMILIES = {"C1a": ((1, 2, 2), 2, 18), "C1b": ((1, 2, 3), 2, 18), "C1c": ((1, 1, 3), 1, 18)}  # shape, subspace dim, D


def rel_to_json(F, rel):
    return [[k, list(m), F.to_json(c)] for (k, m), c in sorted(rel.items())]


def rel_from_json(F, js):
    """Inverse of rel_to_json (the stored relations rebuild the case without the generator)."""
    out = {}
    for k, m, c in js:
        out[(k, tuple(m))] = _decode(F, c)
    return out


def _decode(F, c):
    if isinstance(F, QQ):
        from fractions import Fraction
        return Fraction(c)
    if isinstance(F, PrimeField):
        return int(c)
    return tuple(int(x) for x in c)


def random_relations(F, a, b, e, seed):
    """b relations in (U_e)^a with independent uniform coefficients on the monomial basis of U_e, from the seed.

    Draw order: relation j = 0..b-1, component k = 0..a-1, monomial m in A.monos(e) order, one F.random(rng) each."""
    rng = random.Random(seed)
    rels = []
    for _ in range(b):
        rel = {}
        for k in range(a):
            for m in A.monos(e):
                c = F.random(rng)
                if not F.is_zero(c):
                    rel[(k, m)] = c
        rels.append(rel)
    return rels


def case_id(family, field, index):
    return "%s|%s|%d" % (family, field, index)


def case_specs():
    """Every case of the hypothesis as a light spec (the relations are built when the case runs)."""
    specs = []
    for fam, (shape, sdim, D) in C1_FAMILIES.items():
        count = {("C1a"): 35, ("C1b"): 651, ("C1c"): 63}[fam]
        for i in range(count):
            specs.append({"id": case_id(fam, "GF(2)", i), "family": fam, "field": "GF(2)", "index": i,
                          "shape": list(shape), "D": D, "kind": "subspace"})
    for fam, (fields, shape, n, D) in RANDOM_FAMILIES.items():
        for f in fields:
            for i in range(n):
                specs.append({"id": case_id(fam, make_field(f).name, i), "family": fam, "field": make_field(f).name,
                              "index": i, "shape": list(shape), "D": D, "kind": "random"})
    i = 0
    for shape in C3_SHAPES:
        for _ in range(10):
            specs.append({"id": case_id("C3", "GF(2^4)", i), "family": "C3", "field": "GF(2^4)", "index": i,
                          "shape": list(shape), "D": C3_D, "kind": "random"})
            i += 1
    return specs


def subspace_all(F, family):
    """Every relation set of a C1 family, in the rref order of uhlib (one generator pass)."""
    a, b, e = C1_FAMILIES[family][0]
    mon = list(A.monos(e))
    for rws in S.rref_subspaces(F, len(mon), C1_FAMILIES[family][1]):
        yield [{(0, m): c for m, c in zip(mon, r) if not F.is_zero(c)} for r in rws]


def build_relations(F, spec, _cache={}):
    a, b, e = spec["shape"]
    if spec["kind"] == "random":
        return random_relations(F, a, b, e, SEED_BASE + spec["index"])
    key = (spec["family"], F.name)
    if key not in _cache:
        _cache[key] = list(subspace_all(F, spec["family"]))
    return _cache[key][spec["index"]]


def run_case(spec, limit_seconds=1200):
    """Compute one case with the first instrument; returns its record (status 'done' or 'unfinished')."""
    F = make_field(spec["field"])
    a, b, e = spec["shape"]
    rels = build_relations(F, spec)
    rec = {"id": spec["id"], "family": spec["family"], "field": spec["field"], "field_record": field_record(F),
           "a": a, "b": b, "e": e, "index": spec["index"], "D": spec["D"],
           "seed": SEED_BASE + spec["index"] if spec["kind"] == "random" else None,
           "relations": [rel_to_json(F, r) for r in rels]}
    t0 = time.time()
    try:
        h = hilbert_function(F, a, rels, spec["D"], deadline=t0 + limit_seconds)
    except CaseTimeout as exc:
        rec.update(status="unfinished", hilbert_partial=exc.partial, seconds=round(time.time() - t0, 1))
        return rec
    cls, val = classify(h)
    rec.update(status="done", hilbert=h, cls=cls, value=val, seconds=round(time.time() - t0, 1))
    return rec


def run_chunk(specs, limit_seconds=1200):
    return [run_case(s, limit_seconds) for s in specs]


# ------------------------------------------------------------------ predicted values and counts
def s2_value(a, e):
    """(a (a + 1) / 2) L.L with L.L = 2 m^2 (e = 2m) or 2 m (m + 1) (e = 2m + 1)."""
    m = e // 2
    ll = 2 * m * m if e % 2 == 0 else 2 * m * (m + 1)
    return a * (a + 1) // 2 * ll


def family_counts(records):
    """Counts of a list of case records: cases, finite, constant by value, growing, unclassified, unfinished."""
    c = {"cases": len(records), "finite_length": 0, "eventually_constant": 0, "constant_values": {}, "growing": 0,
         "unclassified": 0, "unfinished": 0}
    for r in records:
        if r["status"] != "done":
            c["unfinished"] += 1
        elif r["cls"] == FINITE:
            c["finite_length"] += 1
        elif r["cls"] == CONSTANT:
            c["eventually_constant"] += 1
            c["constant_values"][str(r["value"])] = c["constant_values"].get(str(r["value"]), 0) + 1
        elif r["cls"] == GROWING:
            c["growing"] += 1
        else:
            c["unclassified"] += 1
    return c


def dumps(obj):
    return json.dumps(obj, indent=1)
