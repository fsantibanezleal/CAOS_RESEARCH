"""EXP-004: rank certificates for the lift of the prime-field realizations to characteristic 0.

Library of the experiment (the frozen hypothesis is hypothesis.md in this folder). It holds:

- a parser for the Macaulay2 text of a saved EXP-001 hit (`hitD`, `hitM`, `hitGen`, `hitSeed`, `hitP`, `hitF`),
  with exact integer coefficients only;
- the symmetric lift of the coefficients mod p to integers (the lift of EXP-001's recheck.m2, 'qq' branch);
- the two constructions of the graded pieces as integer matrices, one per degree:
  form (a), the cokernel of a map of free S-modules (generator 'module'), dim M_d = rows - rank;
  form (b), the image of a map between free modules over T = S/(a^(r+1), b^(r+1), c^(r+1)) (generator 'socle'),
  dim N_d = rank;
- the rank of an integer matrix mod p and over QQ with python-flint (exact);
- the Hilbert function of a pure Betti table, from EXP-001's census.py (independent of every rank).

A matrix is sparse: `Mat(rows, cols, entries)` with entries `(i, j, v)`, zero-based, integers.
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP001 = HERE.parent / "EXP-001-pure-ray-census"

_VARS = "abc"
_TERM_FACTOR = re.compile(r"([abc])(?:\^(\d+))?")


# ------------------------------------------------------------------------------------------------ parsing

def parse_poly(text: str) -> dict[tuple[int, int, int], int]:
    """A polynomial in a, b, c with integer coefficients, as {exponent triple: coefficient} (no zero values).

    Accepts terms such as -3125*a^2*b, a^3, 15921*c^3, a, 7, 0, joined by + and -. Anything else raises ValueError.
    """
    s = re.sub(r"\s+", "", text)
    if not s:
        raise ValueError("empty polynomial")
    out: dict[tuple[int, int, int], int] = {}
    for term in re.split(r"(?=[+-])", s):
        if term == "":
            continue
        sign = 1
        body = term
        if body[0] in "+-":
            sign = -1 if body[0] == "-" else 1
            body = body[1:]
        if not body:
            raise ValueError(f"empty term in {text!r}")
        coef = 1
        exps = [0, 0, 0]
        for factor in body.split("*"):
            if re.fullmatch(r"\d+", factor):
                coef *= int(factor)
                continue
            m = _TERM_FACTOR.fullmatch(factor)
            if not m:
                raise ValueError(f"cannot parse factor {factor!r} in {text!r}")
            exps[_VARS.index(m.group(1))] += int(m.group(2)) if m.group(2) is not None else 1
        key = (exps[0], exps[1], exps[2])
        out[key] = out.get(key, 0) + sign * coef
    return {k: v for k, v in out.items() if v != 0}


@dataclass
class Hit:
    d: tuple[int, ...]
    m: int
    gen: str
    seed: int
    p: int
    F: list[list[dict[tuple[int, int, int], int]]]


_HEADER = re.compile(
    r'hitD\s*=\s*\{([\d,\s]+)\}\s*;\s*hitM\s*=\s*(\d+)\s*;\s*hitGen\s*=\s*"(\w+)"\s*;\s*'
    r'hitSeed\s*=\s*(\d+)\s*;\s*hitP\s*=\s*(\d+)\s*;')


def parse_matrix_text(text: str) -> list[list[dict[tuple[int, int, int], int]]]:
    """The M2 text '{{e11, e12}, {e21, e22}}' as a list of rows of polynomials."""
    t = text.strip()
    if t.endswith(";"):
        t = t[:-1].strip()
    if not (t.startswith("{{") and t.endswith("}}")):
        raise ValueError("matrix text must be {{...}, ...}")
    rows = re.split(r"\}\s*,\s*\{", t[2:-2])
    return [[parse_poly(e) for e in row.split(",")] for row in rows]


def parse_hit_text(text: str) -> Hit:
    """Parse a .hit.m2 file: line 2 the header, line 4 hitF (line 3, hitPres, is not used)."""
    lines = text.split("\n")
    if len(lines) < 4:
        raise ValueError("hit file has fewer than 4 lines (truncated)")
    m = _HEADER.search(lines[1])
    if not m:
        raise ValueError("header line not recognised")
    f_line = next((ln for ln in lines[2:] if ln.lstrip().startswith("hitF")), None)
    if f_line is None:
        raise ValueError("no hitF line")
    body = f_line.split("=", 1)[1]
    d = tuple(int(x) for x in m.group(1).replace(" ", "").split(","))
    F = parse_matrix_text(body)
    widths = {len(r) for r in F}
    if len(widths) != 1:
        raise ValueError("ragged hitF")
    return Hit(d=d, m=int(m.group(2)), gen=m.group(3), seed=int(m.group(4)), p=int(m.group(5)), F=F)


def symmetric(e: int, p: int) -> int:
    """The symmetric representative of e mod p (recheck.m2: e > p // 2 becomes e - p)."""
    e %= p
    return e - p if e > p // 2 else e


def lift_matrix(F, p: int):
    """Symmetric integer lift of every coefficient of F (zero coefficients are dropped)."""
    out = []
    for row in F:
        new_row = []
        for ent in row:
            lifted = {k: symmetric(v, p) for k, v in ent.items()}
            new_row.append({k: v for k, v in lifted.items() if v != 0})
        out.append(new_row)
    return out


# ------------------------------------------------------------------------------------------------ monomials

@lru_cache(maxsize=None)
def monomials(deg: int) -> tuple[tuple[int, int, int], ...]:
    """Monomials of degree deg in a, b, c, in a fixed order (empty for deg < 0)."""
    if deg < 0:
        return ()
    return tuple((i, j, deg - i - j) for i in range(deg, -1, -1) for j in range(deg - i, -1, -1))


@lru_cache(maxsize=None)
def monomials_t(deg: int, r: int) -> tuple[tuple[int, int, int], ...]:
    """Monomials of degree deg of T = S/(a^(r+1), b^(r+1), c^(r+1)): every exponent at most r."""
    return tuple(mu for mu in monomials(deg) if max(mu) <= r)


@lru_cache(maxsize=None)
def _index(deg: int, r: int | None) -> dict[tuple[int, int, int], int]:
    mons = monomials(deg) if r is None else monomials_t(deg, r)
    return {mu: k for k, mu in enumerate(mons)}


# ------------------------------------------------------------------------------------------------ matrices

@dataclass
class Mat:
    rows: int
    cols: int
    entries: list[tuple[int, int, int]]


def _check_degrees(F, col_degs) -> None:
    for row in F:
        for j, ent in enumerate(row):
            for mu in ent:
                if sum(mu) != col_degs[j]:
                    raise ValueError(f"entry of column {j} has a term of degree {sum(mu)}, expected {col_degs[j]}")


def build_form_a(F, col_degs, d: int) -> Mat:
    """A_d of form (a): coker of F as a map from sum S(-col_degs[j]) to S^len(F), in degree d.

    Rows: (target element i, monomial of degree d); columns: (source element j, monomial mu of degree
    d - col_degs[j]); the column of (j, mu) holds the coefficients of mu * F[i][j] for every i.
    dim M_d = rows - rank.
    """
    nrow_comp = len(F)
    ncol_comp = len(F[0])
    if len(col_degs) != ncol_comp:
        raise ValueError("col_degs must have one degree per column of F")
    _check_degrees(F, col_degs)
    n_d = len(monomials(d))
    idx = _index(d, None)
    entries: list[tuple[int, int, int]] = []
    col = 0
    for j in range(ncol_comp):
        for mu in monomials(d - col_degs[j]):
            for i in range(nrow_comp):
                for e, c in F[i][j].items():
                    nu = (mu[0] + e[0], mu[1] + e[1], mu[2] + e[2])
                    entries.append((i * n_d + idx[nu], col, c))
            col += 1
    return Mat(nrow_comp * n_d, col, entries)


def build_form_b(F, r: int, e: int, d: int) -> Mat:
    """A_d of form (b): the image of F between free T-modules, T = S/(a^(r+1), b^(r+1), c^(r+1)).

    F has len(F) target components and len(F[0]) generators, with entries that are forms of degree e (the
    package's s - r). Columns: (generator j, monomial nu of T of degree d); rows: (component i, monomial of T of
    degree d + e); the column of (j, nu) holds the coefficients of nu * F[i][j] reduced in T (a monomial with an
    exponent above r is zero). dim N_d = rank.
    """
    n_comp = len(F)
    n_gen = len(F[0])
    _check_degrees(F, [e] * n_gen)
    tgt = monomials_t(d + e, r)
    idx = _index(d + e, r)
    n_t = len(tgt)
    entries: list[tuple[int, int, int]] = []
    col = 0
    for j in range(n_gen):
        for nu in monomials_t(d, r):
            for i in range(n_comp):
                for ex, c in F[i][j].items():
                    mu = (nu[0] + ex[0], nu[1] + ex[1], nu[2] + ex[2])
                    if mu[0] > r or mu[1] > r or mu[2] > r:
                        continue
                    entries.append((i * n_t + idx[mu], col, c))
            col += 1
    return Mat(n_comp * n_t, col, entries)


# ------------------------------------------------------------------------------------------------ ranks

def _dense(mat: Mat) -> list[int]:
    flat = [0] * (mat.rows * mat.cols)
    cols = mat.cols
    for i, j, v in mat.entries:
        flat[i * cols + j] += v
    return flat


def rank_mod_p(mat: Mat, p: int) -> int:
    """Exact rank mod p (python-flint nmod_mat)."""
    from flint import nmod_mat
    if mat.rows == 0 or mat.cols == 0:
        return 0
    return nmod_mat(mat.rows, mat.cols, [v % p for v in _dense(mat)], p).rank()


def rank_qq(mat: Mat) -> int:
    """Exact rank over QQ of an integer matrix (python-flint fmpz_mat; no floating point)."""
    from flint import fmpz_mat
    if mat.rows == 0 or mat.cols == 0:
        return 0
    return fmpz_mat(mat.rows, mat.cols, _dense(mat)).rank()


def gp_text(mat: Mat, p: int) -> str:
    """A PARI/GP script that prints matrank of the integer matrix and of its reduction mod p."""
    ii = ",".join(str(i + 1) for i, _, _ in mat.entries)
    jj = ",".join(str(j + 1) for _, j, _ in mat.entries)
    vv = ",".join(str(v) for _, _, v in mat.entries)
    return (
        'default(parisizemax, "6G");\n'
        f"ri=[{ii}];\nrj=[{jj}];\nrv=[{vv}];\n"
        f"MM=matrix({mat.rows},{mat.cols});\n"
        "for(k=1,#rv, MM[ri[k],rj[k]]+=rv[k]);\n"
        'print("rankQQ ", matrank(MM));\n'
        f'print("rankP ", matrank(MM*Mod(1,{p})));\n'
    )


# ------------------------------------------------------------------------------------------------ pure table

def _census():
    sys.dont_write_bytecode = True
    p = str(EXP001)
    if p not in sys.path:
        sys.path.insert(0, p)
    import census
    return census


def hilbert_pure(d, m: int = 1) -> list[int]:
    """Hilbert function of m times the pure module of degree sequence d, degrees 0 .. d[-1] - 3, from the
    numerator of the pure Betti table divided by (1 - t)^3 (census.py of EXP-001), independent of any rank."""
    cen = _census()
    d = tuple(d)
    return [m * x for x in cen.hilbert_S(d, cen.primitive_point(d))]


def betti0_1(d) -> tuple[int, int, int, int]:
    """The primitive point of d (the pure Betti numbers up to scaling)."""
    return tuple(_census().primitive_point(tuple(d)))


def degree_plan(hit: Hit) -> dict:
    """Shapes and ranges used for a hit: the generator type, the matrix F dimensions it must have, the
    degree range 0..top+1 of the pure Hilbert function (top = d[-1] - 3), and for 'socle' r, s, e = s - r."""
    d = hit.d
    cc = len(d) - 1
    bt = betti0_1(d)
    top = d[-1] - d[0] - cc
    plan = {"top": top, "bt": bt}
    if hit.gen == "module":
        plan.update(F_rows=hit.m * bt[0], F_cols=hit.m * bt[1], col_degs=[d[1]] * (hit.m * bt[1]))
    elif hit.gen == "socle":
        r = d[-1] - d[0] - cc
        s = cc * r
        plan.update(F_rows=hit.m * bt[cc], F_cols=hit.m * bt[0], r=r, s=s, e=s - r)
    else:
        raise ValueError(f"unknown generator {hit.gen!r}")
    return plan
