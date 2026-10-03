"""Independent exact-inverse controls for the second-order pruning path."""

import importlib
from pathlib import Path
import sys

from flint import arb, ctx, fmpq
import pytest
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"problems/number-theory/riemann-hypothesis/code"))
quadratic = importlib.import_module("certified_quadratic")


@pytest.mark.parametrize("precision", [128, 256])
@pytest.mark.parametrize("n", [1, 2, 4, 8])
def test_ldl_completion_of_squares_matches_exact_inverse(precision, n):
    ctx.prec = precision
    # Rational SPD matrices with dense signed off-diagonal entries.
    factor = sp.Matrix(n, n, lambda i, j: sp.Rational((-1)**(i+j)*(i+1), j+2) if i >= j else 0)
    matrix = factor*factor.T+sp.eye(n)/7
    gradient = sp.Matrix([sp.Rational((-1)**j*(j+2), j+3) for j in range(n)])
    exact_loss = (gradient.T*matrix.inv()*gradient)[0]/2
    converted = [[arb(fmpq(int(matrix[i, j].p), int(matrix[i, j].q))) for j in range(n)] for i in range(n)]
    g = [arb(fmpq(int(x.p), int(x.q))) for x in gradient]
    decomposition = quadratic.positive_ldl(converted)
    assert decomposition is not None
    bound = quadratic.quadratic_lower(arb(7), g, decomposition)
    exact = 7-exact_loss
    exact_rational = fmpq(int(exact.p), int(exact.q))
    assert bound.lower().fmpq() <= exact_rational <= bound.upper().fmpq()
    # Independent completion-of-squares at the exact minimizing vector.
    center = -matrix.inv()*gradient
    assert 7+(gradient.T*center)[0]+(center.T*matrix*center)[0]/2 == exact
    for offset in [sp.ones(n, 1)/13, -sp.ones(n, 1)/11]:
        point = center+offset
        assert 7+(gradient.T*point)[0]+(point.T*matrix*point)[0]/2 >= exact


@pytest.mark.parametrize("matrix", [[[0]], [[-1]], [[1, 2], [2, 1]], [[1, 1], [1, 1]]])
def test_nonpositive_pivot_rejects(matrix):
    ctx.prec = 128
    assert quadratic.positive_ldl([[arb(x) for x in row] for row in matrix]) is None


def test_interval_uncertain_positive_pivot_rejects():
    assert quadratic.positive_ldl([[arb(1, 2)]]) is None


def test_gradient_interval_bound_contains_all_corner_minima():
    ctx.prec = 128
    decomposition = quadratic.positive_ldl([[arb(2), arb(1)], [arb(1), arb(3)]])
    bound = quadratic.quadratic_lower(arb(10), [arb(1, fmpq(1, 10)), arb(-2, fmpq(1, 10))], decomposition)
    inverse = sp.Matrix([[2, 1], [1, 3]]).inv()
    for a in [sp.Rational(9, 10), sp.Rational(11, 10)]:
        for b in [sp.Rational(-21, 10), sp.Rational(-19, 10)]:
            gradient = sp.Matrix([a, b])
            exact = 10-(gradient.T*inverse*gradient)[0]/2
            exact_rational = fmpq(int(exact.p), int(exact.q))
            assert bound.lower().fmpq() <= exact_rational <= bound.upper().fmpq()


def test_invalid_factorization_rejects():
    with pytest.raises(ValueError):
        quadratic.quadratic_lower(arb(1), [arb(1)], ([[arb(1)]], [arb(-1)]))
