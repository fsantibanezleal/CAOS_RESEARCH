"""CPU-only exact finite frequency and exponent controls, not an analytic proof."""
import argparse
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
import hashlib
import json
from math import gcd
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent


@lru_cache(None)
def max_divisors(limit):
    counts = [0] * (limit + 1)
    for d in range(1, limit + 1):
        for n in range(d, limit + 1, d):
            counts[n] += 1
    return max(counts)


def run(receipt):
    if receipt.exists():
        raise SystemExit("Preserve earlier receipt")
    start = time.process_time()
    blocks = triples = 0
    bad_spacing = bad_collision = None
    for coprime in (False, True):
        for p_size in (1, 2, 4, 8, 16, 32):
            for q_size in (1, 2, 4, 8, 16, 32):
                for n_size in (1, 2, 4, 8, 16, 32):
                    rational = Counter()
                    integer = Counter()
                    for p in range(p_size, 2 * p_size + 1):
                        for q in range(q_size, 2 * q_size + 1):
                            if coprime and gcd(p, q) != 1:
                                continue
                            for n in range(n_size, 2 * n_size + 1):
                                rational[F(p * q, n)] += 1
                                common = gcd(p * q, n)
                                integer[(p * q // common, n // common)] += 1
                                triples += 1
                    assert rational == Counter({F(r, s): count for (r, s), count in integer.items()})
                    frequencies = sorted(rational)
                    delta_inverse = 16 * p_size * q_size * n_size
                    for x, y in zip(frequencies, frequencies[1:]):
                        # log(y/x) >= (y-x)/y; exact arithmetic suffices.
                        assert delta_inverse * (y - x) >= y
                        if (p_size * q_size) * (y - x) < y and bad_spacing is None:
                            bad_spacing = {'P': p_size, 'Q': q_size, 'N': n_size,
                                           'left_ratio': str(x), 'right_ratio': str(y)}
                    divisor_bound = max_divisors(4 * p_size * q_size)
                    assert max(rational.values()) <= 2 * n_size * divisor_bound
                    if max(rational.values()) > divisor_bound and bad_collision is None:
                        ratio, count = max(rational.items(), key=lambda x: x[1])
                        bad_collision = {'P': p_size, 'Q': q_size, 'N': n_size,
                                         'ratio': str(ratio), 'actual_multiplicity': count,
                                         'wrong_no_N_bound': divisor_bound}
                    blocks += 1
                    if blocks % 36 == 0:
                        print(json.dumps({'blocks': blocks, 'triples': triples}), flush=True)
                    assert time.process_time() - start < 60, "Declared CPU budget exceeded"
    assert blocks == 432 and bad_spacing is not None and bad_collision is not None
    exponent_boxes = 0
    for theta in (F(501, 1000), F(527, 1000), F(3, 5), F(4, 5), F(99, 100)):
        for nu in (F(1, 100), F(499, 10000), F(1, 10), F(1, 4)):
            for p in (F(0), nu / 2, nu):
                for q in (F(0), nu / 3, nu):
                    a = 1 - 2 * theta
                    k = 1 - theta
                    n0 = a + p + q
                    direct1 = a / 2 + n0 / 2
                    direct2 = direct1 + (p + q + n0 - k) / 2
                    assert direct1 == a + (p + q) / 2
                    assert direct2 == F(3, 2) * a - k / 2 + F(3, 2) * (p + q)
                    assert direct1 <= 1 - 2 * theta + nu
                    assert direct2 <= 1 - F(5, 2) * theta + 3 * nu
                    exponent_boxes += 1
    theta, nu, eta = F(527, 1000), F(499, 10000), F(1, 100000)
    gaussian = theta - eta
    e1, e2 = 1 - 2 * gaussian + nu, 1 - F(5, 2) * gaussian + 3 * nu
    assert e1 < 0 and e2 < 0
    assert nu > min(F(1, 2), F(17, 33) * (2 * theta - 1))
    result = {'schema': 'exp029-finite-frequency-controls-v1', 'passed': True,
              'analytic_moment_theorem_proved': False,
              'hypothesis_sha256': hashlib.sha256((HERE / 'hypothesis.md').read_bytes()).hexdigest(),
              'runner_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'arithmetic': 'stdlib Fraction and independently reduced integer pairs; no floats',
              'dyadic_blocks': blocks, 'triples': triples, 'exponent_boxes': exponent_boxes,
              'negative_controls': {'drop_dual_N_spacing_cost': bad_spacing,
                                    'drop_collision_N_factor': bad_collision},
              'theta': str(theta), 'nu': str(nu), 'eta': str(eta),
              'charged_E1': str(e1), 'charged_E2': str(e2),
              'cpu_seconds': time.process_time() - start,
              'scope': 'Finite frequency/exponent controls only; no analytic theorem or new onset.'}
    assert result['cpu_seconds'] < 60
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--receipt', type=Path, required=True)
    run(parser.parse_args().receipt)
