"""Native-free outward rational parity and exact frequency-cost refutation."""
import argparse
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from math import isqrt
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
SCALE = 10**65
DETECTOR_SHA = '74ed14a925bdd10f27d09d6fb23a8e43f9474f8e0e5280fceafac33e06f49464'


def run(receipt):
    if receipt.exists():
        raise SystemExit('Preserve earlier receipt')
    started = time.process_time()
    toolkit = HERE.parent / 'EXP-026-multiplicity-defect-retention/independent_compact.py'
    spec = importlib.util.spec_from_file_location('rational_intervals029', toolkit)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    interval, trig = module.Interval, module.trig

    def sqrt_interval(value):
        assert value.lo >= 0
        low = isqrt(value.lo.numerator * SCALE * SCALE // value.lo.denominator)
        high = isqrt(value.hi.numerator * SCALE * SCALE // value.hi.denominator) + 1
        assert F(low, SCALE)**2 <= value.lo and F(high, SCALE)**2 >= value.hi
        return interval(F(low, SCALE), F(high, SCALE))

    source = HERE.parent / 'EXP-010-levinson-parity-transfer/artifacts/canonical/result.json'
    raw = source.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == DETECTOR_SHA
    detector = json.loads(raw)
    assert detector['accepted']
    theta, nu, eta = F(527, 1000), F(499, 10000), F(1, 100000)
    entry = next(x for x in detector['detector_constants'] if F(x['nu']) == nu)
    kappa = F(entry['kappa']['lower'])
    root2 = sqrt_interval(interval(2))
    sine, cosine = trig(interval(theta) / root2)
    pair = 2 - interval(theta) / 2 - cosine / (root2 * sine)
    k = interval(kappa)
    density = (3 + k - sqrt_interval((1 - k) * (9 - k - 8 * pair))) / 4
    assert density.lo > 0
    wrong_density = (3 - sqrt_interval(9 - 8 * pair)) / 4
    assert wrong_density.hi < 0
    gaussian = theta - eta
    # Independent power bookkeeping: coefficient norm, collision, multiplier.
    a, width, p, q = 1 - 2 * gaussian, 1 - gaussian, nu, nu
    n0 = a + p + q
    separation = a / 2
    collision = n0 / 2
    first = separation + collision
    second = separation + collision + (p + q + n0 - width) / 2
    assert first == F(-51, 12500) and second == F(-6711, 40000)
    # Exact permitted block P=Q=1, N=32: two actual ratios 1/64, 1/63.
    x, y = F(1, 64), F(1, 63)
    upper = (y - x) / x
    assert upper == F(1, 63) < F(1, 16)
    assert (y - x) / y >= F(1, 512)
    result = {'schema': 'exp029-independent-conditional-parity-v1',
              'passed_conditional_controls': True, 'analytic_moment_theorem_proved': False,
              'hypothesis_sha256': hashlib.sha256((HERE / 'hypothesis.md').read_bytes()).hexdigest(),
              'declaration_sha256': hashlib.sha256((HERE / 'independent-control-declaration.md').read_bytes()).hexdigest(),
              'runner_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'detector_receipt_sha256': DETECTOR_SHA,
              'interval_toolkit_sha256': hashlib.sha256(toolkit.read_bytes()).hexdigest(),
              'arithmetic': 'stdlib Fraction, Machin pi/trig outward intervals and integer square roots; no FLINT/Arb',
              'theta': str(theta), 'nu': str(nu), 'eta': str(eta),
              'charged_E1': str(first), 'charged_E2': str(second),
              'pair_term': pair.receipt(), 'conditional_density': density.receipt(),
              'zero_detector_rejected': True,
              'spacing_N_omission_witness': {'P': 1, 'Q': 1, 'N': 32,
                                            'ratios': [str(x), str(y)],
                                            'log_gap_upper': str(upper),
                                            'wrong_delta': '1/16', 'proper_delta': '1/512'},
              'cpu_seconds': time.process_time() - started,
              'scope': 'Conditional fixed arithmetic and one exact spacing refutation only; no new onset admitted.'}
    assert result['cpu_seconds'] < 60
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--receipt', type=Path, required=True)
    run(parser.parse_args().receipt)
