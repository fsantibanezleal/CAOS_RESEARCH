"""Bounded exploration followed by exact affine-witness pressure ceilings."""

from fractions import Fraction
import hashlib
from itertools import combinations
import json
import math
from pathlib import Path
import time
import platform

from flint import arb, ctx, fmpq
import numpy as np
from scipy.optimize import minimize
import scipy

from local_replay import PACKET, PACKET_SHA, spec_from_packet
from rh019_vendor.kernel import kernel_k0, squared_kernel_derivatives


def sinc_prime(z):
    result = np.empty_like(z)
    small = np.abs(z) < 1e-4
    a = z[small]
    result[small] = -a/3+a**3/30-a**5/840+a**7/45360
    a = z[~small]
    result[~small] = (a*np.cos(a)-np.sin(a))/(a*a)
    return result


def float_energy(spec):
    pairs = list(spec.weights)
    incidence = np.array([[float(i <= coordinate < j) for coordinate in range(8)]
                          for i, j in pairs])
    weights = np.array([float(spec.weights[p]) for p in pairs])
    coefficients = np.array([float(c) for c in spec.kernel.coeffs])
    frequencies = np.array([math.sqrt(2), *(math.pi*k for k in spec.kernel.omega_pi_multiples)])
    k0 = np.sum(coefficients*np.sinc(frequencies/(2*math.pi)))

    def evaluate(gaps, pressure):
        distances = incidence@np.asarray(gaps)
        minus = frequencies[:, None]/2-math.pi*distances
        plus = frequencies[:, None]/2+math.pi*distances
        kernel = np.sum(coefficients[:, None]*(np.sinc(minus/math.pi)+np.sinc(plus/math.pi))/2, axis=0)
        derivative = np.sum(coefficients[:, None]*math.pi*(-sinc_prime(minus)+sinc_prime(plus))/2, axis=0)
        energy = np.sum(weights*(kernel/k0)**2)
        gradient = incidence.T@(weights*2*kernel*derivative/(k0*k0))
        return float(energy+pressure*np.sum(gaps)), gradient+pressure

    return evaluate


def fraction_endpoint(value):
    mantissa, exponent = value.man_exp()
    return Fraction(int(mantissa))*Fraction(2)**int(exponent)


def exact_witness(spec, gaps):
    ctx.prec = 192
    rational = [Fraction(max(0, round(float(g)*10**6)), 10**6) for g in gaps]
    k0_squared = kernel_k0(spec.kernel)**2
    energy = arb(0)
    for (i, j), coefficient in spec.weights.items():
        x = sum(rational[i:j], Fraction(0))
        potential, _, _ = squared_kernel_derivatives(arb(fmpq(x.numerator, x.denominator)), spec.kernel, k0_squared)
        energy += arb(coefficient)*potential
    assert energy.is_finite()
    return {'gaps': [str(g) for g in rational], 'span': str(sum(rational, Fraction(0))),
            'energy_lower': str(fraction_endpoint(energy.lower())),
            'energy_upper': str(fraction_endpoint(energy.upper())),
            'energy_enclosure': str(energy)}


def envelope_peak(lines):
    """Exact all-vertex evaluation of min_i(intercept_i+slope_i*p)."""
    if not any(slope < 0 for _, slope in lines):
        return None
    vertices = {Fraction(0)}
    for (a, b), (c, d) in combinations(lines, 2):
        if b != d:
            p = (c-a)/(b-d)
            if p >= 0:
                vertices.add(p)
    values = [(min(a+b*p for a, b in lines), p) for p in vertices]
    return max(values)


def independent_pair_bound(lines):
    """A single decreasing line or one rising/falling pair bounds every p."""
    bounds = [(a, Fraction(0), (index,)) for index, (a, b) in enumerate(lines) if b <= 0]
    for i, (a, b) in enumerate(lines):
        for j, (c, d) in enumerate(lines):
            if b > 0 and d < 0:
                p = (c-a)/(b-d)
                if p >= 0:
                    bounds.append((a+b*p, p, (i, j)))
    return min(bounds) if bounds else None


def candidate_transfer(pressure, observed):
    # Exploratory lower proposal only: retain a 0.3 percent observed margin.
    delta = Fraction(math.floor(observed*0.997*10**7), 10**7)
    h = Fraction(3362285207, 5000000000)
    best = None
    for integer in range(3000, 3415):
        c = Fraction(integer, 1000)
        tau = c-1
        m = math.floor(8+tau*tau/delta)
        if m <= 8:
            continue
        t = Fraction(m-8, m)
        a = delta*t
        if (6*c-7-c*c < a or 4*c-2-c*c < 2*a
                or c < 2+tau/2 or delta*(m-8) > tau*tau or 2-a <= 0):
            continue
        q = (1+h-8*pressure*t)/(2-a)
        if best is None or q > best[0]:
            best = (q, m, tau, c, a)
    if best is None:
        return None
    q, m, tau, c, a = best
    return {'pressure': str(pressure), 'proposed_delta': str(delta), 'm': m,
            'tau': str(tau), 'c': str(c), 'a': str(a), 'conditional_q': str(q),
            'conditional_q_decimal': float(q),
            'status': 'exploratory proposed inequality; universal local bound NOT proved'}


def audit():
    started = time.monotonic()
    spec = spec_from_packet()
    raw = PACKET.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == PACKET_SHA
    packet = json.loads(raw)
    evaluate = float_energy(spec)
    source = np.array(packet['float_minimizing_gaps'])
    source_value, _ = evaluate(source, 1/2500)
    assert abs(source_value-packet['float_minimum_observed']) < 1e-13
    check = np.array([.91, 1.11, 1.43, .87, 1.9, 1.31, .98, 1.79])
    _, gradient = evaluate(check, .001)
    finite_difference = []
    for i in range(8):
        shift = np.eye(8)[i]*1e-6
        finite_difference.append((evaluate(check+shift, .001)[0]-evaluate(check-shift, .001)[0])/2e-6)
    gradient_error = float(np.max(np.abs(gradient-finite_difference)))
    assert gradient_error < 2e-8
    pressures = [Fraction(1, d) for d in [3000, 2500, 2000, 1600, 1250, 1000, 800, 600, 400]]
    rng = np.random.default_rng(222021)
    starts = [source, source[::-1], *(np.full(8, g) for g in [.9, 1.04, 1.2, 1.5, 1.98])]
    starts += [rng.choice([1.04, 1.98], 8)+rng.normal(0, .035, 8) for _ in range(17)]
    starts += [rng.uniform(.7, 2.15, 8) for _ in range(8)]
    outcomes, selected = [], []
    partial = False
    for pressure in pressures:
        results = []
        for index, initial in enumerate(starts):
            if time.monotonic()-started > 300:
                partial = True
                break
            result = minimize(lambda x: evaluate(x, float(pressure)), initial, jac=True,
                              method='L-BFGS-B', bounds=[(0, 20)]*8,
                              options={'maxiter': 600, 'ftol': 1e-14, 'gtol': 1e-10})
            results.append({'start': index, 'objective': float(result.fun),
                            'gaps': result.x.tolist(), 'success': bool(result.success),
                            'iterations': int(result.nit), 'message': str(result.message)})
        if not results:
            break
        results.sort(key=lambda r: r['objective'])
        best = results[0]
        selected += [r['gaps'] for r in results[:4]]
        outcomes.append({'pressure': str(pressure), 'local_results': results,
                         'candidate': candidate_transfer(pressure, best['objective'])})
        print(f"pressure={pressure} local_min={best['objective']:.14g} span={sum(best['gaps']):.10g} candidate={outcomes[-1]['candidate']}", flush=True)
        if partial:
            break
    witnesses, seen = [], set()
    for gaps in [source, *selected]:
        key = tuple(round(float(g)*10**6) for g in gaps)
        if key in seen:
            continue
        seen.add(key)
        witness = exact_witness(spec, gaps)
        rational_gaps = [float(Fraction(g)) for g in witness['gaps']]
        floated, _ = evaluate(rational_gaps, 0)
        assert abs(floated-float(Fraction(witness['energy_upper']))) < 1e-13
        witnesses.append(witness)
    target = Fraction(419, 500)
    # Independently enclosed window value is below this upward decimal rational.
    h_upper = Fraction(672457041415, 10**12)
    problem = Path(__file__).resolve().parents[1]
    window_receipt = problem/'experiments/EXP-019-nine-point-local-replay/artifacts/window-audit.json'
    window = json.loads(window_receipt.read_bytes())
    assert window['passed'] is True and window['packet_sha256'] == PACKET_SHA
    assert arb(window['H']) < arb(fmpq(h_upper.numerator, h_upper.denominator))
    needed = 2*target-1-h_upper
    assert needed > 0
    lines = [(target*Fraction(w['energy_upper']), target*Fraction(w['span'])-8) for w in witnesses]
    peak = envelope_peak(lines)
    independent = independent_pair_bound(lines)
    if peak is not None:
        assert independent is not None and peak[0] == independent[0]
    barrier = peak is not None and peak[0] < needed
    if barrier:
        # The converse inequality would not be a barrier; the audited direction matters.
        assert not peak[0] >= needed
    declaration = problem/'experiments/EXP-022-pressure-duality-audit/hypothesis.md'
    return {'schema': 'rh-pressure-duality-v1', 'target_q': str(target),
            'scope': 'fixed pinned window/weights; exact witness pressure-family upper audit',
            'source_packet_sha256': PACKET_SHA, 'source_float_anchor': source_value,
            'gradient_maximum_absolute_error': gradient_error, 'search_partial': partial,
            'search_outcomes': outcomes, 'exact_witnesses': witnesses,
            'h_upper': str(h_upper), 'required_threshold': str(needed),
            'envelope_peak': None if peak is None else {'value': str(peak[0]), 'pressure': str(peak[1])},
            'independent_pair_bound': None if independent is None else {
                'value': str(independent[0]), 'pressure': str(independent[1]), 'witness_indices': independent[2]},
            'uniform_0838_barrier': barrier,
            'elapsed_seconds': time.monotonic()-started,
            'runtime': {'python': platform.python_version(), 'numpy': np.__version__,
                        'scipy': scipy.__version__, 'precision': 192},
            'bindings': {p.relative_to(problem).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in [Path(__file__), declaration, window_receipt,
                                   problem/'code/local_replay.py', problem/'code/rh019_vendor/kernel.py']},
            'not_established': ['universal lower bound for any new pressure', 'new zero proportion',
                                'barrier for other windows or weights', 'novel priority', 'RH']}


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--receipt', type=Path, required=True)
    args = parser.parse_args()
    result = audit()
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_bytes((json.dumps(result, indent=2, sort_keys=True)+'\n').encode())
    print(json.dumps({k: result[k] for k in ['uniform_0838_barrier', 'envelope_peak', 'independent_pair_bound', 'elapsed_seconds']}, indent=2), flush=True)
