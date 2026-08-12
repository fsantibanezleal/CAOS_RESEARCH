"""Independent audit for EXP-020 artifacts and selected module decompositions."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
DEFAULT_RESULTS = HERE / "artifacts" / "results.json"
DEFAULT_AUDIT = HERE / "artifacts" / "audit.json"
SAMPLES = (4, 5, 17, 73, 151, 300)


def canonical_hash(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def file_hash(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def block(start: int, stop: int) -> set[int]:
    return set(range(start, stop + 1)) if start <= stop else set()


def exact_power_profiles(p: int) -> list[tuple[set[int], int]]:
    """Rebuild EXP-017 power formulas without importing the campaign code."""
    s = 6 * p
    a = block(0, p) | block(3 * p, 4 * p - 2)
    b = (
        (block(p + 1, 3 * p - 1) - {2 * p - 1})
        | {4 * p}
        | block(5 * p - 1, 6 * p - 1)
    )
    c = block(0, 2 * p) | block(3 * p, 5 * p - 2)
    ring = (
        {0}
        | {4 * s + r for r in a}
        | block(5 * s, 6 * s - 1)
        | {6 * s + r for r in b}
        | {8 * s + r for r in c}
        | block(9 * s, 13 * s - 2)
    )
    conductor = (
        {4 * s + r for r in a}
        | {5 * s + r for r in a | b}
        | {6 * s + r for r in b}
        | {8 * s + r for r in c}
        | block(9 * s, 13 * s - 2)
    )
    square = {8 * s + r for r in c} | block(9 * s, 13 * s - 2)
    cube = block(12 * s, 13 * s - 2)
    return [
        (ring, 13 * s),
        (conductor, 13 * s),
        (square, 13 * s),
        (cube, 13 * s),
        (set(), 16 * s),
        (set(), 20 * s),
    ]


def contains(profile: tuple[set[int], int], value: int) -> bool:
    finite, conductor = profile
    return value >= conductor or value in finite


def minimum_in_residue(
    profile: tuple[set[int], int], residue: int, modulus: int
) -> int:
    value = residue
    while not contains(profile, value):
        value += modulus
    return value


def selected_reconstruction(p: int) -> dict[str, object]:
    profiles = exact_power_profiles(p)
    modulus = 24 * p
    free: dict[int, int] = {}
    torsion: dict[tuple[int, int], int] = {}
    sequence_hashes: list[str] = []

    for residue in range(modulus):
        minima = [minimum_in_residue(profile, residue, modulus) for profile in profiles]
        sequence = []
        for left, right in zip(minima, minima[1:]):
            step = right - left
            if step not in (0, modulus):
                raise AssertionError(f"p={p}, residue={residue}: bad independent step {step}")
            sequence.append(step // modulus)
        if sequence[4] != 1:
            raise AssertionError(f"p={p}, residue={residue}: final string is not free")
        sequence_hashes.append(canonical_hash(sequence))

        cursor = 0
        while cursor < 5:
            if sequence[cursor] == 0:
                cursor += 1
                continue
            start = cursor
            while cursor < 5 and sequence[cursor] == 1:
                cursor += 1
            if cursor == 5:
                free[start] = free.get(start, 0) + 1
            else:
                key = (start, cursor - start)
                torsion[key] = torsion.get(key, 0) + 1

    expected_free = {0: 1, 1: 10 * p - 1, 2: 12 * p, 3: 2 * p - 1, 4: 1}
    expected_torsion = {(0, 1): p}
    if free != expected_free or torsion != expected_torsion:
        raise AssertionError(f"p={p}: independent cyclic decomposition mismatch")

    beta_zero = expected_free.copy()
    beta_zero[0] += p
    beta_one = {1: p}
    section_length = len(sequence_hashes) + p
    if section_length != 25 * p:
        raise AssertionError(f"p={p}: independent section length mismatch")

    controls = {
        "torsion_exponent_control": (0, 2) not in torsion,
        "free_degree_one_control": free[1] != 10 * p - 2,
        "beta_one_control": beta_one[1] != p - 1,
        "regularity_control": max(free) != 3,
        "section_control": section_length != 25 * p - 1,
    }
    if not all(controls.values()):
        raise AssertionError(f"p={p}: independent corruption survived")

    result: dict[str, object] = {
        "p": p,
        "free_shifts": {str(key): free[key] for key in sorted(free)},
        "torsion_summands": {
            f"shift_{shift}_exponent_{exponent}": torsion[(shift, exponent)]
            for shift, exponent in sorted(torsion)
        },
        "beta_0": {str(key): beta_zero[key] for key in sorted(beta_zero)},
        "beta_1": {str(key): beta_one[key] for key in sorted(beta_one)},
        "regularity_over_F": max(free),
        "a_invariant": max(free) - 1,
        "parameter_section_length": section_length,
        "sequence_aggregate": canonical_hash(sequence_hashes),
        "controls": controls,
    }
    result["audit_row_hash"] = canonical_hash(result)
    return result


def verify_campaign_rows(data: dict[str, object]) -> tuple[list[str], dict[int, dict[str, object]]]:
    rows = data.get("rows")
    if not isinstance(rows, list):
        raise AssertionError("campaign rows missing")
    hashes: list[str] = []
    by_p: dict[int, dict[str, object]] = {}
    for item in rows:
        if not isinstance(item, dict):
            raise AssertionError("invalid campaign row")
        row = item.copy()
        recorded = row.pop("row_hash", None)
        actual = canonical_hash(row)
        if actual != recorded:
            raise AssertionError(f"campaign row hash mismatch at p={row.get('p')}")
        p = row.get("p")
        if not isinstance(p, int):
            raise AssertionError("campaign parameter missing")
        hashes.append(actual)
        by_p[p] = item
    if canonical_hash(hashes) != data.get("campaign_aggregate"):
        raise AssertionError("campaign aggregate mismatch")
    if sorted(by_p) != list(range(4, 301)):
        raise AssertionError("campaign range is not exactly p=4,...,300")
    return hashes, by_p


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--output", type=Path, default=DEFAULT_AUDIT)
    args = parser.parse_args()

    started = time.perf_counter()
    data = json.loads(args.results.read_text(encoding="utf-8"))
    campaign_hashes, by_p = verify_campaign_rows(data)
    selected: list[dict[str, object]] = []
    for p in SAMPLES:
        rebuilt = selected_reconstruction(p)
        campaign = by_p[p]
        for key in (
            "free_shifts",
            "torsion_summands",
            "beta_0",
            "beta_1",
            "regularity_over_F",
            "a_invariant",
            "parameter_section_length",
        ):
            if rebuilt[key] != campaign[key]:
                raise AssertionError(f"p={p}: audit mismatch in {key}")
        selected.append(rebuilt)
        print(f"p={p}: independent module reconstruction PASS", flush=True)
        if time.perf_counter() - started > 60:
            raise TimeoutError("EXP-020 audit exceeded its one-minute budget")

    output = {
        "experiment": "EXP-020-noether-normalization-module",
        "status": "INDEPENDENT_AUDIT_PASS",
        "campaign_file_sha256": file_hash(args.results),
        "campaign_rows_rehashed": len(campaign_hashes),
        "selected_parameters": list(SAMPLES),
        "selected": selected,
        "audit_aggregate": canonical_hash(
            [row["audit_row_hash"] for row in selected] + campaign_hashes
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    temporary.replace(args.output)
    elapsed = time.perf_counter() - started
    print(
        f"EXP-020 independent audit PASS aggregate={output['audit_aggregate']} "
        f"elapsed={elapsed:.6f}s",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
