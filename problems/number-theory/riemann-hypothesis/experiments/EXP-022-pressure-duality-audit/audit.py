"""Independent witness-energy and two-line pressure obstruction audit."""

from fractions import Fraction
import hashlib
import json
from pathlib import Path

from flint import arb, ctx, fmpq


def ball(rational):
    r = Fraction(rational)
    return arb(fmpq(r.numerator, r.denominator))


def audit():
    root = Path(__file__).resolve().parents[2]
    here = Path(__file__).resolve().parent
    raw = (here/'artifacts/pressure-duality.json').read_bytes()
    record = json.loads(raw)
    packet_path = root/'experiments/EXP-018-nine-point-distinct-transfer/artifacts/input/nine-point-final.json'
    packet_raw = packet_path.read_bytes()
    assert hashlib.sha256(packet_raw).hexdigest() == record['source_packet_sha256']
    packet = json.loads(packet_raw)
    for path, digest in record['bindings'].items():
        assert hashlib.sha256((root/path).read_bytes()).hexdigest() == digest
    ctx.prec = 256
    coefficients = [ball(Fraction(n, packet['window_coefficient_denominator']))
                    for n in packet['window_coefficient_numerators']]
    frequencies = [arb(2).sqrt()]+[2*j*arb.pi() for j in range(1, 7)]
    k0 = sum((c*(w/2).sinc() for c, w in zip(coefficients, frequencies)), arb(0))
    assert k0 > 0
    weights = [Fraction(n, packet['pair_weight_denominator']) for n in packet['pair_weight_numerators']]
    pairs = [tuple(p) for p in packet['pair_order']]
    assert pairs == [(i, j) for i in range(9) for j in range(i+1, 9)]
    assert all(w >= 0 for w in weights)
    assert all(sum((w for (i, j), w in zip(pairs, weights) if j-i == r), Fraction(0)) == 2 for r in range(1, 9))
    indices = record['independent_pair_bound']['witness_indices']
    assert len(indices) == 2 and indices[0] != indices[1]
    target = Fraction(record['target_q'])
    lines = []
    for index in indices:
        witness = record['exact_witnesses'][index]
        gaps = [Fraction(g) for g in witness['gaps']]
        assert len(gaps) == 8 and min(gaps) >= 0
        span = sum(gaps, Fraction(0))
        assert span == Fraction(witness['span'])
        energy = arb(0)
        # Native sinc formula, independent of the verifier's derivative/series code.
        for (i, j), weight in zip(pairs, weights):
            x = 2*arb.pi()*ball(sum(gaps[i:j], Fraction(0)))
            kernel = sum((c*(((w-x)/2).sinc()+((w+x)/2).sinc())/2
                          for c, w in zip(coefficients, frequencies)), arb(0))
            energy += ball(weight)*(kernel/k0)**2
        assert energy.lower() >= ball(witness['energy_lower'])
        assert energy.upper() <= ball(witness['energy_upper'])
        lines.append((target*Fraction(witness['energy_upper']), target*span-8))
    (a, b), (c, d) = lines
    assert b > 0 and d < 0
    pressure = (c-a)/(b-d)
    assert pressure >= 0
    value = a+b*pressure
    assert value == c+d*pressure
    assert value == Fraction(record['independent_pair_bound']['value'])
    assert pressure == Fraction(record['independent_pair_bound']['pressure'])
    h_upper = Fraction(record['h_upper'])
    window_path = root/'experiments/EXP-019-nine-point-local-replay/artifacts/window-audit.json'
    window = json.loads(window_path.read_bytes())
    assert window['passed'] is True and window['packet_sha256'] == record['source_packet_sha256']
    assert arb(window['H']) < ball(h_upper)
    required = 2*target-1-h_upper
    assert required == Fraction(record['required_threshold']) and value < required
    assert record['uniform_0838_barrier'] is True
    return {'schema': 'rh-exp022-independent-audit-v1', 'passed': True,
            'target_q': str(target), 'selected_witnesses': indices,
            'pressure_intersection': str(pressure), 'universal_envelope_upper': str(value),
            'required_threshold': str(required), 'strict_margin': str(required-value),
            'precision': 256, 'energy_method': 'independent native Arb sinc; exact rational line intersection',
            'receipt_sha256': hashlib.sha256(raw).hexdigest(),
            'auditor_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'scope': 'fixed packet pressure-family obstruction; no new zero lower proportion or RH claim'}


if __name__ == '__main__':
    result = audit()
    path = Path(__file__).resolve().parent/'artifacts/independent-audit.json'
    path.write_bytes((json.dumps(result, indent=2)+'\n').encode())
    print(json.dumps(result, indent=2), flush=True)
