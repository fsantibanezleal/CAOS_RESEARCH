"""Exact explicit pressure ceiling after independent energy verification."""

from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path


def audit():
    here = Path(__file__).resolve().parent
    spec = importlib.util.spec_from_file_location('rh022_energy_auditor', here/'audit.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    verified = module.audit()
    assert verified['passed'] is True
    raw = (here/'artifacts/pressure-duality.json').read_bytes()
    record = json.loads(raw)
    i, j = verified['selected_witnesses']
    first, second = (record['exact_witnesses'][index] for index in [i, j])
    e1, e2 = (Fraction(w['energy_upper']) for w in [first, second])
    s1, s2 = (Fraction(w['span']) for w in [first, second])
    assert s1 > s2
    p = (e2-e1)/(s1-s2)
    assert p >= 0
    f = e1+p*s1
    assert f == e2+p*s2 and 2-f > 0
    h = Fraction(record['h_upper'])
    cap = (1+h-8*p)/(2-f)
    c = 2*cap-1-h
    assert c > 0 and cap*s1-8 > 0 > cap*s2-8
    assert cap*f-8*p == c
    decimal_cap = Fraction(8375, 10000)
    assert cap < decimal_cap
    problem = here.parents[1]
    files = [Path(__file__), here/'audit.py', here/'ceiling-declaration.md',
             here/'artifacts/pressure-duality.json']
    return {'schema': 'rh-exp022-explicit-pressure-cap-v1', 'passed': True,
            'exact_cap': str(cap), 'cap_decimal': float(cap),
            'conservative_rational_cap': str(decimal_cap),
            'pressure_intersection': str(p), 'witness_energy_at_intersection': str(f),
            'target_threshold': str(c), 'witness_indices': [i, j],
            'strict_finite_block_conclusion': 'every admissible fixed-packet transfer has q < exact_cap < 0.8375',
            'independent_energy_receipt': verified,
            'bindings': {path.relative_to(problem).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                         for path in files},
            'scope': 'fixed window and weights, all p>=0 and finite m; not a true-proportion ceiling, not sharp priority or RH'}


if __name__ == '__main__':
    result = audit()
    target = Path(__file__).resolve().parent/'artifacts/explicit-pressure-cap.json'
    target.write_bytes((json.dumps(result, indent=2)+'\n').encode())
    print(json.dumps(result, indent=2), flush=True)
