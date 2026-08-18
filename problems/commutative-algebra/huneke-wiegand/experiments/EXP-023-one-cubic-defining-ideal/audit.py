"""Independent total-fiber graph audit for EXP-023."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
DEFAULT_RESULTS = HERE / "artifacts" / "results.json"
DEFAULT_OUTPUT = HERE / "artifacts" / "audit.json"
SAMPLES = (4, 13, 23)


def span(first: int, last: int) -> set[int]:
    return set(range(first, last + 1)) if first <= last else set()


def digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def file_hash(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def save(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def closed_blocks(p: int) -> tuple[set[int], ...]:
    one = (
        span(1, p)
        | span(3 * p, 4 * p - 2)
        | span(6 * p, 8 * p - 2)
        | span(8 * p, 10 * p - 2)
        | {10 * p}
        | span(11 * p - 1, 12 * p - 1)
        | span(13 * p + 1, 14 * p - 2)
        | span(14 * p, 15 * p - 1)
        | {16 * p}
        | span(17 * p - 1, 18 * p - 1)
    )
    two = (
        span(p + 1, 2 * p)
        | span(4 * p - 1, 5 * p - 2)
        | {8 * p - 1, 10 * p - 1}
        | span(10 * p + 1, 11 * p - 2)
        | span(12 * p, 13 * p)
        | {14 * p - 1}
        | span(15 * p, 16 * p - 1)
        | span(16 * p + 1, 17 * p - 2)
        | span(18 * p, 24 * p - 1)
    )
    three = span(2 * p + 1, 3 * p - 1) | span(5 * p - 1, 6 * p - 2)
    return ({0}, one, two, three, {6 * p - 1}, set())


def fiber_offsets(p: int, degree: int) -> set[int]:
    layers = closed_blocks(p)
    return set().union(*layers[: min(4, degree) + 1])


class LocalComponents:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))

    def find(self, item: int) -> int:
        while self.parent[item] != item:
            self.parent[item] = self.parent[self.parent[item]]
            item = self.parent[item]
        return item

    def join(self, left: int, right: int) -> None:
        root_left = self.find(left)
        root_right = self.find(right)
        if root_left != root_right:
            self.parent[root_right] = root_left


def total_graph_degree(p: int, degree: int) -> dict[str, object]:
    generators = sorted(fiber_offsets(p, 1))
    previous = fiber_offsets(p, degree - 1)
    remainder = fiber_offsets(p, degree - 2)
    current = fiber_offsets(p, degree)
    quotient_dimension = 0
    nonzero_component_counts: dict[int, int] = {}
    first_invalid: dict[str, object] | None = None

    for total in range(max(generators) + max(previous) + 1):
        vertices = [a for a in generators if total - a in previous]
        if not vertices:
            continue
        location = {a: index for index, a in enumerate(vertices)}
        zero = len(vertices)
        graph = LocalComponents(zero + 1)
        for a in vertices:
            source = location[a]
            for c in generators:
                r = total - a - c
                if r not in remainder:
                    continue
                target = location.get(c)
                if target is None:
                    graph.join(source, zero)
                else:
                    graph.join(source, target)

        zero_root = graph.find(zero)
        roots = {graph.find(index) for index in range(len(vertices))}
        roots.discard(zero_root)
        count = len(roots)
        quotient_dimension += count
        if total in current:
            nonzero_component_counts[total] = count
        elif count and first_invalid is None:
            first_invalid = {"total": total, "component_count": count}

    minimal_equations = quotient_dimension - len(current)
    exceptional = {
        str(total): count
        for total, count in sorted(nonzero_component_counts.items())
        if count != 1
    }
    return {
        "degree": degree,
        "quotient_dimension": quotient_dimension,
        "actual_dimension": len(current),
        "minimal_equations": minimal_equations,
        "exceptional_nonzero_totals": exceptional,
        "first_invalid_component": first_invalid,
        "component_hash": digest(nonzero_component_counts),
    }


def rebuild(p: int) -> dict[str, object]:
    started = time.perf_counter()
    degree_rows = [total_graph_degree(p, degree) for degree in (3, 4, 5)]
    betti = {
        "2": 50 * p * p - 17 * p,
        **{str(row["degree"]): row["minimal_equations"] for row in degree_rows},
    }
    expected = {"2": 50 * p * p - 17 * p, "3": 1, "4": 0, "5": 0}
    if betti != expected:
        raise AssertionError(f"p={p}: audit Betti mismatch: {betti}")
    if degree_rows[0]["exceptional_nonzero_totals"] != {str(3 * p): 2}:
        raise AssertionError(f"p={p}: cubic component is not uniquely at total 3p")
    if any(row["first_invalid_component"] is not None for row in degree_rows):
        raise AssertionError(f"p={p}: an invalid total survived lower relations")

    rebuilt: dict[str, object] = {
        "p": p,
        "first_betti_row_degrees_2_to_5": betti,
        "exceptional_cubic_total": 3 * p,
        "degree_rows": degree_rows,
        "elapsed_seconds": time.perf_counter() - started,
    }
    rebuilt["audit_row_hash"] = digest(rebuilt)
    return rebuilt


def verify_campaign(data: dict[str, object]) -> tuple[list[str], dict[int, dict[str, object]]]:
    rows = data.get("rows")
    if not isinstance(rows, list):
        raise AssertionError("campaign rows are missing")
    hashes: list[str] = []
    by_parameter: dict[int, dict[str, object]] = {}
    for stored in rows:
        if not isinstance(stored, dict):
            raise AssertionError("invalid campaign row")
        row = stored.copy()
        recorded = row.pop("row_hash", None)
        actual = digest(row)
        if recorded != actual:
            raise AssertionError(f"campaign row hash mismatch at p={row.get('p')}")
        parameter = row.get("p")
        if not isinstance(parameter, int):
            raise AssertionError("campaign row has no integer parameter")
        hashes.append(actual)
        by_parameter[parameter] = stored
    if digest(hashes) != data.get("campaign_aggregate"):
        raise AssertionError("campaign aggregate mismatch")
    if sorted(by_parameter) != list(range(4, 24)):
        raise AssertionError("campaign range is not exactly p=4,...,23")
    return hashes, by_parameter


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--budget-seconds", type=float, default=120.0)
    args = parser.parse_args()
    started = time.perf_counter()
    data = json.loads(args.results.read_text(encoding="utf-8"))
    campaign_hashes, by_parameter = verify_campaign(data)

    selected: list[dict[str, object]] = []
    for p in SAMPLES:
        row = rebuild(p)
        if row["first_betti_row_degrees_2_to_5"] != by_parameter[p][
            "first_betti_row_degrees_2_to_5"
        ]:
            raise AssertionError(f"p={p}: independent and campaign rows disagree")
        selected.append(row)
        elapsed = time.perf_counter() - started
        print(f"p={p}: independent total-graph reconstruction PASS elapsed={elapsed:.3f}s", flush=True)
        if elapsed > args.budget_seconds:
            raise TimeoutError(
                f"EXP-023 audit exceeded its declared {args.budget_seconds:g}-second budget"
            )

    output = {
        "experiment": "EXP-023-one-cubic-defining-ideal",
        "status": "INDEPENDENT_AUDIT_PASS",
        "campaign_file_sha256": file_hash(args.results),
        "campaign_rows_rehashed": len(campaign_hashes),
        "selected_parameters": list(SAMPLES),
        "selected": selected,
        "audit_aggregate": digest(
            [row["audit_row_hash"] for row in selected] + campaign_hashes
        ),
        "elapsed_seconds": time.perf_counter() - started,
    }
    save(args.output, output)
    print(
        f"EXP-023 independent audit PASS aggregate={output['audit_aggregate']} "
        f"elapsed={output['elapsed_seconds']:.3f}s",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
