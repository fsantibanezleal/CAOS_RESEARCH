"""An exact rational simplex with Bland's rule, written for this programme.

Why ours. EXP-003's verdict flagged sympy's rational simplex as a single point of
failure for every optimum we report (UFB-033), and EXP-004's sweep then hit it for
real: sympy raised "Oscillating system led to invalid solution" on a degenerate
family member. Bland's rule makes cycling impossible, so this solver terminates on
degenerate problems by construction, at the cost of more pivots.

Solves, over exact Fractions:

    minimize  c^T z   subject to   A_ub z <= b_ub,  A_eq z = b_eq,  z >= 0.

Two phases, both with Bland's rule (entering variable = smallest index with negative
reduced cost; leaving variable = smallest basis index among ratio ties). Phase I
minimises the sum of artificials to find a basic feasible solution or prove
infeasibility; phase II optimises the real objective.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Optional, Sequence

Vector = list[Fraction]
Matrix = list[list[Fraction]]


class LPError(RuntimeError):
    """Raised when the problem is infeasible or unbounded."""


class Infeasible(LPError):
    pass


class Unbounded(LPError):
    pass


def _pivot(tableau: Matrix, obj: Vector, basis: list[int], row: int, col: int) -> None:
    """Standard pivot on (row, col), updating the objective row too."""
    piv = tableau[row][col]
    tableau[row] = [v / piv for v in tableau[row]]
    for i, r in enumerate(tableau):
        if i != row and r[col] != 0:
            factor = r[col]
            tableau[i] = [a - factor * b for a, b in zip(r, tableau[row])]
    if obj[col] != 0:
        factor = obj[col]
        for j in range(len(obj)):
            obj[j] -= factor * tableau[row][j]
    basis[row] = col


def _solve_tableau(tableau: Matrix, obj: Vector, basis: list[int], n_cols: int) -> None:
    """Run simplex to optimality with Bland's rule. Raises Unbounded if unbounded."""
    while True:
        entering = -1
        for j in range(n_cols):
            if obj[j] < 0:
                entering = j  # Bland: first (smallest index) negative reduced cost
                break
        if entering < 0:
            return
        leaving, best_ratio = -1, None
        for i, row in enumerate(tableau):
            if row[entering] > 0:
                ratio = row[-1] / row[entering]
                if (
                    best_ratio is None
                    or ratio < best_ratio
                    or (ratio == best_ratio and basis[i] < basis[leaving])
                ):
                    leaving, best_ratio = i, ratio
        if leaving < 0:
            raise Unbounded("the linear program is unbounded")
        _pivot(tableau, obj, basis, leaving, entering)


def solve_lp(
    c: Sequence[Fraction],
    A_ub: Optional[Sequence[Sequence[Fraction]]] = None,
    b_ub: Optional[Sequence[Fraction]] = None,
    A_eq: Optional[Sequence[Sequence[Fraction]]] = None,
    b_eq: Optional[Sequence[Fraction]] = None,
) -> tuple[Fraction, Vector]:
    """Minimise c^T z subject to the constraints, z >= 0. Returns (optimum, z)."""
    c = [Fraction(v) for v in c]
    n = len(c)
    rows: Matrix = []
    rhs: Vector = []
    n_slack = len(A_ub) if A_ub else 0

    for i, (row, rv) in enumerate(zip(A_ub or [], b_ub or [])):
        slack = [Fraction(0)] * n_slack
        slack[i] = Fraction(1)
        rows.append([Fraction(v) for v in row] + slack)
        rhs.append(Fraction(rv))
    for row, rv in zip(A_eq or [], b_eq or []):
        rows.append([Fraction(v) for v in row] + [Fraction(0)] * n_slack)
        rhs.append(Fraction(rv))

    if not rows:
        raise LPError("no constraints given")

    # make every right-hand side nonnegative
    for i in range(len(rows)):
        if rhs[i] < 0:
            rows[i] = [-v for v in rows[i]]
            rhs[i] = -rhs[i]

    width = n + n_slack
    m = len(rows)

    # phase I: artificial variables, minimise their sum
    tableau: Matrix = [
        rows[i] + [Fraction(1) if k == i else Fraction(0) for k in range(m)] + [rhs[i]]
        for i in range(m)
    ]
    basis = [width + i for i in range(m)]
    phase1_obj: Vector = [Fraction(0)] * width + [Fraction(1)] * m + [Fraction(0)]
    for i in range(m):
        for j in range(width + m + 1):
            phase1_obj[j] -= tableau[i][j]

    _solve_tableau(tableau, phase1_obj, basis, width + m)
    if -phase1_obj[-1] > 0:
        raise Infeasible("no feasible point")

    # drive any artificial still in the basis out, then drop the artificial columns
    for i in range(m):
        if basis[i] >= width:
            for j in range(width):
                if tableau[i][j] != 0:
                    _pivot(tableau, phase1_obj, basis, i, j)
                    break
    for i in range(m):
        del tableau[i][width : width + m]

    # phase II
    obj: Vector = list(c) + [Fraction(0)] * n_slack + [Fraction(0)]
    for i in range(m):
        if basis[i] < width and obj[basis[i]] != 0:
            factor = obj[basis[i]]
            for j in range(width + 1):
                obj[j] -= factor * tableau[i][j]
    _solve_tableau(tableau, obj, basis, width)

    z: Vector = [Fraction(0)] * width
    for i in range(m):
        if basis[i] < width:
            z[i_basis := basis[i]] = tableau[i][-1]
    return -obj[-1], z[:n]


def max_min_margin(
    loads: Sequence[Sequence[Fraction]], x: Sequence[Fraction]
) -> tuple[Fraction, tuple[Fraction, ...]]:
    """The separation LP: max delta s.t. c^T(y - x) >= delta for all y, sum c = 1, c >= 0.

    Cast for ``solve_lp`` by splitting the free variable delta into delta+ - delta-:
    variables are (delta+, delta-, c_0, ..., c_{m-1}), all nonnegative, and the
    objective minimises -(delta+ - delta-).
    """
    m = len(x)
    if not loads:
        # nothing to separate from: any price vector works
        return Fraction(1), tuple(Fraction(1, m) for _ in range(m))

    obj = [Fraction(-1), Fraction(1)] + [Fraction(0)] * m
    A_ub, b_ub = [], []
    for y in loads:
        # delta - c^T(y - x) <= 0
        A_ub.append([Fraction(1), Fraction(-1)] + [-(y[j] - x[j]) for j in range(m)])
        b_ub.append(Fraction(0))
    A_eq = [[Fraction(0), Fraction(0)] + [Fraction(1)] * m]
    b_eq = [Fraction(1)]

    optimum, z = solve_lp(obj, A_ub, b_ub, A_eq, b_eq)
    return -optimum, tuple(z[2:])
