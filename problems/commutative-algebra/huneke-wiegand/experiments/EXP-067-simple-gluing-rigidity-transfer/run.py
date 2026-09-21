"""EXP-067 producer: exact simple-gluing transfer checks.

CPU only, deterministic, stdlib only. The symbolic proof in proof.md owns the
all-parameter theorem; this program checks exact finite consequences and emits
a reproducible certificate.
"""

from __future__ import annotations

import hashlib
import heapq
import importlib.util
import json
import math
import sys
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
ARTIFACT = HERE / "artifacts" / "results.json"
EXP009_RUN = (
    HERE.parent / "EXP-009-growing-interval-family" / "run.py"
)
CODE = HERE.parents[1] / "code"
sys.path.insert(0, str(CODE))

from hwcert.semigroup import analyze_rigidity  # noqa: E402


def load_module(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


EXP009 = load_module(EXP009_RUN, "exp009_gluing_dependency")


def apery_from_generators(multiplicity: int, generators: tuple[int, ...]) -> tuple[int, ...]:
    """Return the Apéry set by shortest paths in the residue graph."""
    infinity = 10**100
    distance = [infinity] * multiplicity
    distance[0] = 0
    queue = [(0, 0)]
    while queue:
        value, residue = heapq.heappop(queue)
        if value != distance[residue]:
            continue
        for generator in generators:
            candidate = value + generator
            target = candidate % multiplicity
            if candidate < distance[target]:
                distance[target] = candidate
                heapq.heappush(queue, (candidate, target))
    if any(value == infinity for value in distance):
        raise ValueError("generators do not define a numerical semigroup")
    return tuple(distance)


def member_from_apery(apery: tuple[int, ...], value: int) -> bool:
    return value >= 0 and value >= apery[value % len(apery)]


def mask_from_apery(apery: tuple[int, ...]) -> tuple[int, int]:
    multiplicity = len(apery)
    frobenius = max(apery) - multiplicity
    mask = sum(
        1 << value
        for value in range(frobenius + 1)
        if member_from_apery(apery, value)
    )
    return mask, frobenius


def predicted_glued_apery(
    base_apery: tuple[int, ...], q: int
) -> tuple[int, ...]:
    multiplicity = len(base_apery)
    if math.gcd(q, multiplicity) != 1:
        raise ValueError("q must be coprime to the multiplicity")
    result = [0] * multiplicity
    for residue, value in enumerate(base_apery):
        result[(q * residue) % multiplicity] = q * value
    return tuple(result)


def first_admissible_q(multiplicity: int, count: int = 8) -> tuple[int, ...]:
    values: list[int] = []
    q = 1
    while len(values) < count:
        if math.gcd(q, multiplicity) == 1:
            values.append(q)
        q += 1
    return tuple(values)


def exponent_set(
    apery: tuple[int, ...], shift: int, order: int, limit: int
) -> set[int]:
    return {
        value
        for value in range(limit + 1)
        if all(member_from_apery(apery, value + index * shift) for index in range(order + 1))
    }


def transferred_set(
    base_apery: tuple[int, ...], shift: int, order: int, q: int, limit: int
) -> set[int]:
    multiplicity = len(base_apery)
    result: set[int] = set()
    for value in exponent_set(base_apery, shift, order, limit // q):
        start = q * value
        result.update(range(start, limit + 1, multiplicity))
    return result


def genus_from_apery(apery: tuple[int, ...]) -> int:
    multiplicity = len(apery)
    numerator = sum(apery) - multiplicity * (multiplicity - 1) // 2
    if numerator % multiplicity:
        raise AssertionError("Apéry genus numerator is not divisible by m")
    return numerator // multiplicity


def case_record(p: int, q: int) -> dict[str, object]:
    base_mask, base_frobenius, base_generators = EXP009.formula_mask(p)
    del base_mask
    multiplicity = 24 * p
    shift = 6 * p
    base_apery = apery_from_generators(multiplicity, tuple(base_generators))
    if max(base_apery) - multiplicity != base_frobenius:
        raise AssertionError("EXP-009 Frobenius premise mismatch")

    glued_generators = (multiplicity,) + tuple(
        q * value for value in base_generators if value != multiplicity
    )
    generated_apery = apery_from_generators(multiplicity, glued_generators)
    predicted_apery = predicted_glued_apery(base_apery, q)
    apery_match = generated_apery == predicted_apery
    mask, frobenius = mask_from_apery(generated_apery)
    expected_frobenius = q * (base_frobenius + multiplicity) - multiplicity
    genus = genus_from_apery(generated_apery)
    symmetric = 2 * genus == frobenius + 1
    scaled_shift = q * shift
    shift_is_gap = not member_from_apery(generated_apery, scaled_shift)
    limit = 2 * frobenius + 1
    e_actual = exponent_set(generated_apery, scaled_shift, 1, limit)
    d_actual = exponent_set(generated_apery, scaled_shift, 2, limit)
    e_predicted = transferred_set(base_apery, shift, 1, q, limit)
    d_predicted = transferred_set(base_apery, shift, 2, q, limit)
    rigidity = analyze_rigidity(mask, frobenius, scaled_shift)

    failures: list[str] = []
    if not apery_match:
        failures.append("Apéry transfer mismatch")
    if frobenius != expected_frobenius:
        failures.append("Frobenius formula mismatch")
    if not symmetric:
        failures.append("symmetry mismatch")
    if not shift_is_gap:
        failures.append("scaled shift is not a gap")
    if e_actual != e_predicted:
        failures.append("E transfer mismatch")
    if d_actual != d_predicted:
        failures.append("D transfer mismatch")
    if not rigidity["rigid"]:
        failures.append("scaled ideal is not rigid")

    return {
        "p": p,
        "q": q,
        "multiplicity": multiplicity,
        "embedding_dimension": len(glued_generators),
        "frobenius": frobenius,
        "expected_frobenius": expected_frobenius,
        "scaled_shift": scaled_shift,
        "ideal_exponents": [q * multiplicity, q * (multiplicity + shift)],
        "apery_match": apery_match,
        "symmetric": symmetric,
        "shift_is_gap": shift_is_gap,
        "e_transfer": e_actual == e_predicted,
        "d_transfer": d_actual == d_predicted,
        "rigid": rigidity["rigid"],
        "first_missing_D": rigidity["first_missing_D"],
        "first_reverse_failure": rigidity["first_reverse_failure"],
        "accepted": not failures,
        "failures": failures,
    }


def negative_control(q: int) -> dict[str, object]:
    multiplicity = 4
    generators = (4, 5)
    glued = (multiplicity, q * 5)
    apery = apery_from_generators(multiplicity, glued)
    mask, frobenius = mask_from_apery(apery)
    rigidity = analyze_rigidity(mask, frobenius, q)
    return {
        "q": q,
        "frobenius": frobenius,
        "rigid": rigidity["rigid"],
        "first_missing_D": rigidity["first_missing_D"],
        "accepted": not rigidity["rigid"],
        "source_generators": list(generators),
    }


def main() -> int:
    cases: list[dict[str, object]] = []
    for p in range(4, 13):
        q_values = first_admissible_q(24 * p)
        for q in q_values:
            cases.append(case_record(p, q))
        print(f"producer p={p}: {len(q_values)} coprime q values checked", flush=True)

    controls = [negative_control(q) for q in (1, 3, 5, 7)]
    noncoprime = [
        {
            "p": p,
            "q": q,
            "generator_gcd": math.gcd(24 * p, q),
            "accepted": math.gcd(24 * p, q) > 1,
        }
        for p, q in ((4, 2), (5, 3), (6, 2), (7, 7), (8, 2))
    ]
    accepted = all(bool(case["accepted"]) for case in cases)
    accepted &= all(bool(control["accepted"]) for control in controls)
    accepted &= all(bool(control["accepted"]) for control in noncoprime)
    canonical = json.dumps(cases, sort_keys=True, separators=(",", ":"))
    artifact = {
        "experiment": "EXP-067",
        "method": "exact Apéry shortest paths, exponent-set transfer, and bitset rigidity",
        "scope": {"p": [4, 12], "q_per_p": 8, "case_count": len(cases)},
        "cases": cases,
        "negative_controls": controls,
        "noncoprime_controls": noncoprime,
        "case_aggregate_sha256": hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
        "accepted": accepted,
    }
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(
        json.dumps(artifact, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"producer wrote {ARTIFACT.relative_to(ROOT)}", flush=True)
    print(f"producer accepted={accepted}", flush=True)
    return 0 if accepted else 1


if __name__ == "__main__":
    raise SystemExit(main())
