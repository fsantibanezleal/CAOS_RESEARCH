"""One frozen-detector Arb control; the new analytic moment is unproved."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import time

from flint import arb, ctx, fmpq

HERE = Path(__file__).resolve().parent
DETECTOR_SHA = '74ed14a925bdd10f27d09d6fb23a8e43f9474f8e0e5280fceafac33e06f49464'


def ball(x):
    x = F(x)
    return arb(fmpq(x.numerator, x.denominator))


def run(receipt):
    if receipt.exists():
        raise SystemExit('Preserve earlier receipt')
    started = time.process_time()
    source = HERE.parent / 'EXP-010-levinson-parity-transfer/artifacts/canonical/result.json'
    raw = source.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == DETECTOR_SHA
    detector = json.loads(raw)
    assert detector['accepted']
    theta, nu, eta = F(527, 1000), F(499, 10000), F(1, 100000)
    entry = next(x for x in detector['detector_constants'] if F(x['nu']) == nu)
    assert entry['constraints'] == {'P(0)': '0', 'P(1)': '1', 'Q(0)': '1', 'Q(y)+Q(1-y)': '1'}
    kappa = F(entry['kappa']['lower'])
    gaussian = theta - eta
    e1, e2 = 1 - 2 * gaussian + nu, 1 - F(5, 2) * gaussian + 3 * nu
    assert e1 < 0 and e2 < 0
    assert nu > F(17, 33) * (2 * theta - 1)
    ctx.prec = 256
    t, k, root2 = ball(theta), ball(kappa), arb(2).sqrt()
    pair = 2 - t / 2 - (t / root2).cot() / root2
    density = (3 + k - ((1 - k) * (9 - k - 8 * pair)).sqrt()) / 4
    assert density > 0
    assert (3 - (9 - 8 * pair).sqrt()) / 4 < 0
    result = {'schema': 'exp029-conditional-native-parity-v1',
              'passed_conditional_controls': True, 'analytic_moment_theorem_proved': False,
              'hypothesis_sha256': hashlib.sha256((HERE / 'hypothesis.md').read_bytes()).hexdigest(),
              'declaration_sha256': hashlib.sha256((HERE / 'independent-control-declaration.md').read_bytes()).hexdigest(),
              'runner_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'detector_receipt_sha256': DETECTOR_SHA, 'theta': str(theta), 'nu': str(nu),
              'eta': str(eta), 'charged_E1': str(e1), 'charged_E2': str(e2),
              'certified_kappa_lower': str(kappa), 'pair_term': str(pair),
              'conditional_density': str(density), 'zero_detector_rejected': True,
              'cpu_seconds': time.process_time() - started,
              'scope': 'Conditional fixed arithmetic only; current admitted onset remains 0.5339.'}
    assert result['cpu_seconds'] < 60
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--receipt', type=Path, required=True)
    run(parser.parse_args().receipt)
