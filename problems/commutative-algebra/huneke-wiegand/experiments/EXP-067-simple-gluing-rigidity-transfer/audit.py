"""Independent EXP-067 audit using relaxation and direct bitsets."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
RESULTS = HERE / "artifacts" / "results.json"
ARTIFACT = HERE / "artifacts" / "audit.json"
EXP009_AUDIT = HERE.parent / "EXP-009-growing-interval-family" / "audit.py"


def load_module(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


EXP009 = load_module(EXP009_AUDIT, "exp009_gluing_audit_dependency")


def residue_minima(multiplicity: int, generators: tuple[int, ...]) -> tuple[int, ...]:
    """Bellman-Ford relaxation, independent of the producer's heap route."""
    infinity = 10**100
    values = [infinity] * multiplicity
    values[0] = 0
    changed = True
    while changed:
        changed = False
        for residue, value in enumerate(tuple(values)):
            if value == infinity:
                continue
            for generator in reversed(generators):
                candidate = value + generator
                target = candidate % multiplicity
                if candidate < values[target]:
                    values[target] = candidate
                    changed = True
    if any(value == infinity for value in values):
        raise ValueError("non-numerical generator system")
    return tuple(values)


def member(apery: tuple[int, ...], value: int) -> bool:
    return value >= 0 and value >= apery[value % len(apery)]


def first_q_values(multiplicity: int, count: int = 8) -> tuple[int, ...]:
    return tuple(
        q
        for q in range(1, 10 * multiplicity)
        if math.gcd(q, multiplicity) == 1
    )[:count]


def rigidity_record(apery: tuple[int, ...], shift: int) -> tuple[bool, int | None]:
    frobenius = max(apery) - len(apery)
    end = 2 * frobenius + 1
    e_bits = 0
    d_bits = 0
    for value in range(end + 1):
        if member(apery, value) and member(apery, value + shift):
            e_bits |= 1 << value
            if member(apery, value + 2 * shift):
                d_bits |= 1 << value
    sums = 0
    remaining = e_bits
    while remaining:
        bit = remaining & -remaining
        left = bit.bit_length() - 1
        sums |= e_bits << left
        remaining ^= bit
    sums &= (1 << (end + 1)) - 1
    difference = sums ^ d_bits
    first = (difference & -difference).bit_length() - 1 if difference else None
    return difference == 0, first


def audit_case(p: int, q: int) -> dict[str, object]:
    _, base_frobenius, base_generators = EXP009.independent_mask(p)
    multiplicity = 24 * p
    glued = (multiplicity,) + tuple(
        q * value for value in base_generators if value != multiplicity
    )
    apery = residue_minima(multiplicity, glued)
    frobenius = max(apery) - multiplicity
    genus_numerator = sum(apery) - multiplicity * (multiplicity - 1) // 2
    genus = genus_numerator // multiplicity
    predicted = [0] * multiplicity
    base_apery = residue_minima(multiplicity, tuple(base_generators))
    for residue, value in enumerate(base_apery):
        predicted[(q * residue) % multiplicity] = q * value
    rigid, first_difference = rigidity_record(apery, 6 * p * q)
    accepted = all(
        (
            tuple(predicted) == apery,
            frobenius == q * (base_frobenius + multiplicity) - multiplicity,
            2 * genus == frobenius + 1,
            not member(apery, 6 * p * q),
            rigid,
        )
    )
    return {
        "p": p,
        "q": q,
        "frobenius": frobenius,
        "apery_match": tuple(predicted) == apery,
        "symmetric": 2 * genus == frobenius + 1,
        "scaled_shift_is_gap": not member(apery, 6 * p * q),
        "rigid": rigid,
        "first_rigidity_difference": first_difference,
        "accepted": accepted,
    }


def main() -> int:
    source = json.loads(RESULTS.read_text(encoding="utf-8"))
    cases: list[dict[str, object]] = []
    for p in range(4, 13):
        q_values = first_q_values(24 * p)
        for q in q_values:
            cases.append(audit_case(p, q))
        print(f"audit p={p}: {len(q_values)} coprime q values checked", flush=True)

    source_core = [
        (case["p"], case["q"], case["frobenius"], case["rigid"], case["accepted"])
        for case in source["cases"]
    ]
    audit_core = [
        (case["p"], case["q"], case["frobenius"], case["rigid"], case["accepted"])
        for case in cases
    ]
    producer_agreement = source_core == audit_core
    canonical = json.dumps(cases, sort_keys=True, separators=(",", ":"))
    accepted = producer_agreement and all(bool(case["accepted"]) for case in cases)
    artifact = {
        "experiment": "EXP-067",
        "method": "independent residue relaxation and direct bitset sumsets",
        "case_count": len(cases),
        "cases": cases,
        "producer_agreement": producer_agreement,
        "case_aggregate_sha256": hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
        "accepted": accepted,
    }
    ARTIFACT.write_text(
        json.dumps(artifact, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"audit wrote {ARTIFACT.relative_to(ROOT)}", flush=True)
    print(f"audit accepted={accepted}", flush=True)
    return 0 if accepted else 1


if __name__ == "__main__":
    raise SystemExit(main())
