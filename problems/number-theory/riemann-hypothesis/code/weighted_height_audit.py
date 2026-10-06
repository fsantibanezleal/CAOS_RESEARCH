"""Exact finite obstruction to naive smoothed/unweighted moment substitution."""

from fractions import Fraction
import hashlib
import json
from pathlib import Path

import sympy as sp


def audit():
    g1, h1 = sp.Matrix([sp.sqrt(5)/2, 0]), sp.Matrix([0, sp.Rational(1, 2)])
    g2, h2 = sp.Matrix([0, sp.sqrt(2)]), sp.Matrix([1, 0])
    assert all(sp.simplify(g.dot(g)-h.dot(h)) == 1
               and g.dot(h) == 0 for g, h in [(g1, h1), (g2, h2)])
    pairs = [2*(g*g.T-h*h.T) for g, h in [(g1, h1), (g2, h2)]]
    operator = pairs[0]+pairs[1]/2
    assert operator == sp.Rational(3, 2)*sp.eye(2)
    trace, energy = sp.trace(operator), sp.trace(operator**2)
    assert trace == 3 and energy == sp.Rational(9, 2)
    assert 2*trace-energy == sp.Rational(3, 2)

    # Independently expand the signed diagonal coefficients as rational numbers.
    weights = [Fraction(1), Fraction(1, 2)]
    entries = [2*(weights[0]*Fraction(5, 4)-weights[1]),
               2*(-weights[0]*Fraction(1, 4)+2*weights[1])]
    assert entries == [Fraction(3, 2)]*2
    rational_energy = sum(x*x for x in entries)
    squared_mass = 2*sum(w*w for w in weights)
    assert rational_energy == Fraction(9, 2) and squared_mass == Fraction(5, 2)
    assert 2*squared_mass-rational_energy == Fraction(1, 2)

    # Symbolic general family, with positive b and w1>w2>0 understood.
    w1, w2, b = sp.symbols('w1 w2 b', positive=True)
    c = (w1*b+(w1-w2)/2)/w2
    a = sp.diag(2*(w1*(1+b)-w2*c), 2*(w2*(1+c)-w1*b))
    assert sp.simplify(a-(w1+w2)*sp.eye(2)) == sp.zeros(2)
    residual = sp.expand(4*(w1*w1+w2*w2)-sp.trace(a**2))
    assert sp.factor(residual) == 2*(w1-w2)**2
    assert residual.subs(w1, w2) == 0  # equal-weight negative control

    invalid_g1 = sp.Matrix([sp.sqrt(6)/2, 0])
    assert sp.simplify(invalid_g1.dot(invalid_g1)-h1.dot(h1)) != 1
    problem = Path(__file__).resolve().parents[1]
    declaration = problem/'context/2026-10-03-weighted-cycle-bridge-preflight.md'
    return {'schema': 'rh-weighted-height-preflight-v1', 'passed': True,
            'scope': 'finite signed-vector obstruction; no zeta-zero construction or proportion',
            'simple_vectors': 0, 'weights': ['1', '1/2'],
            'norm_difference_each': '1', 'pair_orthogonality': True,
            'operator_diagonal': ['3/2', '3/2'], 'weighted_trace': '3',
            'trace_square': '9/2', 'naive_first_weight_residual': '3/2',
            'squared_weight_mass': '5/2', 'naive_squared_weight_residual': '1/2',
            'general_squared_weight_residual': '2*(w1-w2)^2',
            'controls': {'equal_weights_residual': '0',
                         'incorrect_pair_normalization_rejected': True,
                         'independent_fraction_diagonal_expansion': True},
            'bindings': {str(path.relative_to(problem)).replace('\\', '/'):
                         hashlib.sha256(path.read_bytes()).hexdigest()
                         for path in [Path(__file__), declaration]},
            'not_established': ['novelty', 'zeta asymptotic gain', 'RH',
                                'weighted analytic transfer']}


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--receipt', type=Path, required=True)
    args = parser.parse_args()
    result = audit()
    args.receipt.write_bytes((json.dumps(result, indent=2, sort_keys=True)+'\n').encode())
    print('Exact weighted-height obstruction and discriminating controls passed.')
