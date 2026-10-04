"""Exact raw-cost, far-tail and range controls; no analytic theorem inference."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from math import gcd
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent


def audit():
    started = time.process_time()
    theta, nu, eta = F(527, 1000), F(499, 10000), F(1, 100000)
    width = theta - eta
    a, k = 1 - 2 * width, 1 - width
    targets = (1 - 2 * width + nu, 1 - F(5, 2) * width + 3 * nu)
    assert targets == (F(-51, 12500), F(-6711, 40000))
    boxes = 0
    worst = [None, None]
    for gi in range(9):
        g = nu * F(gi, 8)
        for pi in range(13):
            p = (nu - g) * F(pi, 12)
            for qi in range(13):
                q = (nu - g) * F(qi, 12)
                cutoff = a + p + q
                scales = {F(0), max(F(0), cutoff), F(1, 2), F(1), F(2)}
                if cutoff > 0:
                    scales.add(cutoff / 2)
                for r in scales:
                    sigma = F(1, 2) if r <= cutoff else F(9, 2)
                    gamma = -sigma + 2 * sigma * k
                    coefficients = (sigma - F(1, 2)) * (p + q) + (F(1, 2) - sigma) * r
                    collisions = r / 2
                    common = -g + gamma + coefficients + collisions
                    costs = (common, common + (p + q + r - k) / 2)
                    for i, total in enumerate(costs):
                        assert total <= targets[i], (g, p, q, r, sigma, i, total)
                        item = (total, g, p, q, r, sigma)
                        if worst[i] is None or total > worst[i][0]:
                            worst[i] = item
                    boxes += 1
        print(json.dumps({'gcd_scales_done': gi + 1, 'raw_cost_boxes': boxes}), flush=True)
        assert time.process_time() - started < 60
    low = (F(1, 2), F(1))
    high = tuple(x - 4 for x in low)
    assert all(x > 0 for x in low) and all(x < 0 for x in high)
    # These are actual retained coprime triples, with a single exact frequency.
    group = [(p, q, p * q) for p in range(4, 9) for q in range(4, 9)
             if gcd(p, q) == 1 and 16 <= p * q <= 32]
    assert len(group) == 6
    multiplicity = len(group)
    # On [-L,L], S=m is exact, so dividing by 2L leaves m^2, not m.
    assert multiplicity * multiplicity > multiplicity
    # For a single nonzero frequency, the integral over [-L,L] is 2L.
    # Its whole-line unweighted L2 norm diverges; these increasing exact masses
    # exhibit the failure without numerically imposing a fake truncation.
    unweighted_masses = [2 * length for length in (1, 2, 4, 8, 16, 32)]
    assert unweighted_masses == [2, 4, 8, 16, 32, 64]
    assert 1 - 2 * (theta - F(1, 100)) + nu > 0
    boundary_nu = 2 * width - 1
    assert not 1 - 2 * width + boundary_nu < 0
    uncontrolled_tail = a / 2 + F(2) / 2
    assert uncontrolled_tail > targets[0]
    # Both changes of which valid range is stronger are exact equalities.
    transition = F(4, 7)
    assert 2 * transition - 1 == (5 * transition - 2) / 6
    crossing = F(12, 13)
    assert F(17, 33) * (2 * crossing - 1) == (5 * crossing - 2) / 6
    assert nu > F(17, 33) * (2 * theta - 1)
    assert time.process_time() - started < 60
    return {'theta': str(theta), 'nu': str(nu), 'eta': str(eta),
            'charged_exponents': [str(x) for x in targets], 'raw_cost_boxes': boxes,
            'worst_grid_exponents_and_scales': [[str(x) for x in row] for row in worst],
            'principal_N_slopes': [str(x) for x in low],
            'tail_N_slopes_before_epsilon': [str(x) for x in high],
            'gcd_decay_powers': ['2', '4'],
            'negative_controls': {'omitted_collisions': {'triples': group,
                                                       'true_normalized_mass': multiplicity ** 2,
                                                       'wrong_diagonal_only_mass': multiplicity},
                                  'whole_line_unweighted_L2': {'interval_masses': unweighted_masses,
                                                              'analytic_divergence': True},
                                  'oversized_window_loss_rejected': True,
                                  'zero_strict_margin_rejected': True,
                                  'uncontrolled_tail_rejected': True},
            'range_transitions': ['4/7', '12/13'],
            'analytic_moment_theorem_proved': False,
            'scope': 'Finite raw-cost accounting; universal proof and admission are separate.',
            'cpu_seconds': time.process_time() - started}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--receipt', type=Path, required=True)
    destination = parser.parse_args().receipt
    if destination.exists():
        raise SystemExit('Preserve earlier receipt')
    result = {'schema': 'exp029-adversarial-raw-cost-v1', 'passed': False,
              'runner_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'declaration_sha256': hashlib.sha256((HERE / 'adversarial-declaration.md').read_bytes()).hexdigest()}
    try:
        result['audit'] = audit()
        result['passed'] = True
    except AssertionError as error:
        result['failure'] = str(error) or 'An accounting obligation failed'
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2), flush=True)
    raise SystemExit(0 if result['passed'] else 1)
