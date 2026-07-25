"""Exact rational decision of cone pointedness (CCB-032).

A cone C = cone(g_1, ..., g_k) is POINTED exactly when the only nonnegative
solution of sum_i lambda_i g_i = 0 is lambda = 0. So pointedness is decided by one
linear feasibility question:

    does there exist lambda >= 0, sum_i lambda_i = 1, with G lambda = 0 ?

FEASIBLE gives an explicit nonnegative zero combination: a CERTIFICATE OF
UNPOINTEDNESS (the cone contains a line, or at least a nontrivial subspace
direction). INFEASIBLE gives, by Farkas / the phase-I dual, a vector y with
y . g_i > 0 for every generator: a CERTIFICATE OF POINTEDNESS.

The decision is made by a phase-I simplex in exact `Fraction` arithmetic. The
system is small in the direction that matters: the number of ROWS is the ambient
dimension plus one (11 or 12 in our prevarieties), while the number of columns is
the generator count (tens to thousands). Bland's rule guarantees termination
without cycling; exact arithmetic means the answer is a proof, not an estimate.

This closes the gap left by `comet_analysis.py`, whose heuristics could return
UNDECIDED: here every comet is decided one way or the other.
"""

from fractions import Fraction

__all__ = ["decide_pointed", "PointedResult"]


class PointedResult:
    def __init__(self, pointed, certificate, kind, iterations):
        self.pointed = pointed          # True / False
        self.certificate = certificate  # separating vector y, or the lambda combination
        self.kind = kind                # "separating-vector" | "zero-combination"
        self.iterations = iterations

    def __repr__(self):
        return (f"PointedResult(pointed={self.pointed}, kind={self.kind}, "
                f"iterations={self.iterations})")


def _phase_one(A, b, n_struct):
    """Phase-I simplex in exact arithmetic.

    Solves min sum(artificials) s.t. A x = b, x >= 0, with b >= 0 assumed after a
    row sign flip. Returns (optimal_value, x, y) where y is the final dual vector
    (the simplex multipliers), both exact.
    """
    m = len(A)
    n = n_struct
    # tableau columns: n structural + m artificial
    T = [row[:] + [Fraction(1) if i == j else Fraction(0) for j in range(m)] + [b[i]]
         for i, row in enumerate(A)]
    basis = list(range(n, n + m))
    # cost row for phase I: minimize sum of artificials
    cost = [Fraction(0)] * (n + m + 1)
    for i in range(m):
        for j in range(n + m + 1):
            cost[j] -= T[i][j]
    for j in range(n, n + m):
        cost[j] += Fraction(1)  # artificials have cost 1; reduce them out of the basis

    it = 0
    while True:
        it += 1
        # Bland's rule: smallest index with negative reduced cost
        piv_col = -1
        for j in range(n + m):
            if cost[j] < 0:
                piv_col = j
                break
        if piv_col < 0:
            break
        # ratio test, Bland tie-break on the leaving variable index
        piv_row, best = -1, None
        for i in range(m):
            if T[i][piv_col] > 0:
                ratio = T[i][-1] / T[i][piv_col]
                if best is None or ratio < best or (ratio == best and basis[i] < basis[piv_row]):
                    best, piv_row = ratio, i
        if piv_row < 0:
            raise RuntimeError("phase-I unbounded, which cannot happen")
        # pivot
        pv = T[piv_row][piv_col]
        T[piv_row] = [v / pv for v in T[piv_row]]
        for i in range(m):
            if i != piv_row and T[i][piv_col] != 0:
                f = T[i][piv_col]
                T[i] = [a - f * bb for a, bb in zip(T[i], T[piv_row])]
        if cost[piv_col] != 0:
            f = cost[piv_col]
            cost = [a - f * bb for a, bb in zip(cost, T[piv_row])]
        basis[piv_row] = piv_col

    obj = -cost[-1]
    x = [Fraction(0)] * (n + m)
    for i, bi in enumerate(basis):
        x[bi] = T[i][-1]
    # dual multipliers: the phase-I reduced costs on the artificial block, shifted
    y = [Fraction(1) - cost[n + i] for i in range(m)]
    return obj, x[:n], y


def decide_pointed(generators):
    """Decide pointedness of cone(generators) exactly.

    generators: list of vectors (lists of Fraction/int) of equal length d.
    Returns a PointedResult. An empty generator list is pointed by convention.
    """
    gens = [[Fraction(c) for c in g] for g in generators]
    if not gens:
        return PointedResult(True, None, "separating-vector", 0)
    d = len(gens[0])
    k = len(gens)

    # rows: G lambda = 0 (d rows) and sum lambda = 1 (one row)
    A = [[gens[j][i] for j in range(k)] for i in range(d)]
    b = [Fraction(0)] * d
    A.append([Fraction(1)] * k)
    b.append(Fraction(1))
    # phase I needs b >= 0; the zero rows are already fine
    for i in range(len(A)):
        if b[i] < 0:
            A[i] = [-v for v in A[i]]
            b[i] = -b[i]

    obj, lam, y = _phase_one(A, b, k)

    if obj == 0:
        # feasible: an explicit nonnegative zero combination exists
        assert sum(lam) == 1
        for i in range(d):
            assert sum(lam[j] * gens[j][i] for j in range(k)) == 0
        return PointedResult(False, lam, "zero-combination", 0)

    # infeasible: build the separating vector from the phase-I duals.
    # y = (y_0..y_{d-1}, y_d) with y . (g_j, 1) <= 0 for all j and y_d > 0 at
    # optimum; then c = -(y_0..y_{d-1}) satisfies c . g_j < 0 for every j after a
    # strictness check, which we verify exactly below.
    c = [-y[i] for i in range(d)]
    if all(sum(c[i] * g[i] for i in range(d)) < 0 for g in gens):
        return PointedResult(True, c, "separating-vector", 0)
    # Fall back to the negated sum direction, then verify; if verification fails we
    # still know the cone is pointed (phase-I infeasibility is the proof), so the
    # certificate is reported as None rather than a wrong vector.
    s = [Fraction(0)] * d
    for g in gens:
        for i in range(d):
            s[i] -= g[i]
    if all(sum(s[i] * g[i] for i in range(d)) < 0 for g in gens):
        return PointedResult(True, s, "separating-vector", 0)
    return PointedResult(True, None, "farkas-infeasibility", 0)
