"""Independent exact audit for EXP-021."""

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


def block(start: int, stop: int) -> set[int]:
    return set(range(start, stop + 1)) if start <= stop else set()


def digest(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def file_hash(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def profiles(p: int) -> list[tuple[set[int], int]]:
    """Closed EXP-017 value profiles, independently encoded."""
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
        (set(), 24 * s),
    ]


def contains(profile: tuple[set[int], int], value: int) -> bool:
    finite, conductor = profile
    return value >= conductor or value in finite


def ideal_sum(
    left: tuple[set[int], int], right: tuple[set[int], int]
) -> tuple[set[int], int]:
    left_values, left_conductor = left
    right_values, right_conductor = right
    left_minimum = min(left_values) if left_values else left_conductor
    right_minimum = min(right_values) if right_values else right_conductor
    stop = min(left_minimum + right_conductor, right_minimum + left_conductor)
    sums = {
        a + b
        for a in left_values
        for b in right_values
        if a + b < stop
    }
    floor = left_minimum + right_minimum
    missing = [v for v in range(floor, stop) if v not in sums]
    conductor = max(missing) + 1 if missing else floor
    return ({v for v in sums if v < conductor}, conductor)


def translated(profile: tuple[set[int], int], amount: int) -> tuple[set[int], int]:
    values, conductor = profile
    return ({value + amount for value in values}, conductor + amount)


def quotient_basis(
    numerator: tuple[set[int], int], denominators: list[tuple[set[int], int]]
) -> list[int]:
    minimum = min(numerator[0]) if numerator[0] else numerator[1]
    stop = max([numerator[1]] + [item[1] for item in denominators])
    return [
        v
        for v in range(minimum, stop)
        if contains(numerator, v) and not any(contains(item, v) for item in denominators)
    ]


def selected_reconstruction(p: int) -> dict[str, object]:
    data = profiles(p)
    ring_values, ring_conductor = data[0]
    maximal = (ring_values - {0}, ring_conductor)
    maximal_products = [ideal_sum(maximal, item) for item in data]
    q = 24 * p

    kernel_dimensions = [len(quotient_basis(maximal, [data[1]]))] + [
        len(quotient_basis(maximal_products[n], [data[n + 1]]))
        for n in range(1, 6)
    ]
    hilbert = [1] + [
        len(quotient_basis(data[n], [maximal_products[n]])) for n in range(1, 6)
    ]
    artinian: list[list[int]] = [[0]]
    for n in range(1, 6):
        artinian.append(
            quotient_basis(data[n], [maximal_products[n], translated(data[n - 1], q)])
        )

    generators = artinian[1]
    socle: list[list[int]] = []
    for n, basis in enumerate(artinian):
        if n + 1 == len(artinian):
            socle.append(list(basis))
            continue
        denominators = [maximal_products[n + 1], translated(data[n], q)]
        socle.append(
            [
                a
                for a in basis
                if all(any(contains(item, a + b) for item in denominators) for b in generators)
            ]
        )

    h_vector = [len(item) for item in artinian]
    socle_vector = [len(item) for item in socle]
    expected = {
        "kernel": [p, 0, 0, 0, 0, 0],
        "hilbert": [1, 10 * p, 22 * p, 24 * p - 1, 24 * p, 24 * p],
        "h_vector": [1, 10 * p - 1, 12 * p, 2 * p - 1, 1, 0],
        "socle": [0, 0, 10 * p, 0, 1, 0],
    }
    actual = {
        "kernel": kernel_dimensions,
        "hilbert": hilbert,
        "h_vector": h_vector,
        "socle": socle_vector,
    }
    if actual != expected:
        raise AssertionError(f"p={p}: independent invariant mismatch: {actual}")

    result: dict[str, object] = {
        "p": p,
        "kernel_dimensions_degrees_0_to_5": kernel_dimensions,
        "hilbert_function_through_degree_5": hilbert,
        "artinian_h_vector_through_degree_5": h_vector,
        "socle_vector_through_degree_5": socle_vector,
        "type": sum(socle_vector),
        "basis_aggregate": digest(
            [[value - n * q for value in basis] for n, basis in enumerate(artinian)]
        ),
        "socle_aggregate": digest(
            [[value - n * q for value in basis] for n, basis in enumerate(socle)]
        ),
    }
    result["audit_row_hash"] = digest(result)
    return result


def verify_rows(data: dict[str, object]) -> tuple[list[str], dict[int, dict[str, object]]]:
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
        actual = digest(row)
        if actual != recorded:
            raise AssertionError(f"campaign row hash mismatch at p={row.get('p')}")
        parameter = row.get("p")
        if not isinstance(parameter, int):
            raise AssertionError("campaign parameter missing")
        hashes.append(actual)
        by_p[parameter] = item
    if digest(hashes) != data.get("campaign_aggregate"):
        raise AssertionError("campaign aggregate mismatch")
    if sorted(by_p) != list(range(4, 301)):
        raise AssertionError("campaign range is not exactly p=4,...,300")
    return hashes, by_p


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--output", type=Path, default=DEFAULT_AUDIT)
    args = parser.parse_args()

    started = time.perf_counter()
    data = json.loads(args.results.read_text(encoding="utf-8"))
    campaign_hashes, by_p = verify_rows(data)
    selected: list[dict[str, object]] = []
    compared = (
        "kernel_dimensions_degrees_0_to_5",
        "hilbert_function_through_degree_5",
        "artinian_h_vector_through_degree_5",
        "socle_vector_through_degree_5",
        "type",
        "basis_aggregate",
        "socle_aggregate",
    )
    for p in SAMPLES:
        rebuilt = selected_reconstruction(p)
        for key in compared:
            if rebuilt[key] != by_p[p][key]:
                raise AssertionError(f"p={p}: audit mismatch in {key}")
        selected.append(rebuilt)
        print(f"p={p}: independent fiber-cone reconstruction PASS", flush=True)
        if time.perf_counter() - started > 60:
            raise TimeoutError("EXP-021 audit exceeded its one-minute budget")

    output = {
        "experiment": "EXP-021-conductor-fiber-cone",
        "status": "INDEPENDENT_AUDIT_PASS",
        "campaign_file_sha256": file_hash(args.results),
        "campaign_rows_rehashed": len(campaign_hashes),
        "selected_parameters": list(SAMPLES),
        "selected": selected,
        "audit_aggregate": digest(
            [row["audit_row_hash"] for row in selected] + campaign_hashes
        ),
    }
    write_json_atomic(args.output, output)
    elapsed = time.perf_counter() - started
    print(
        f"EXP-021 independent audit PASS aggregate={output['audit_aggregate']} "
        f"elapsed={elapsed:.6f}s",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
