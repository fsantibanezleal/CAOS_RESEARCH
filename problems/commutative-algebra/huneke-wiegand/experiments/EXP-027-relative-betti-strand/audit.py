"""Independent reconstruction audit for EXP-027."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
DEFAULT_INPUT = HERE / "artifacts" / "results.json"
DEFAULT_SYMBOLIC = HERE / "artifacts" / "symbolic-certificate.json"
DEFAULT_OUTPUT = HERE / "artifacts" / "audit.json"
SAMPLES = (4, 5, 17, 73, 151, 300)


def digest(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def closed_range(start: int, stop: int) -> list[int]:
    return list(range(start, stop + 1)) if start <= stop else []


def generators_independent(p: int) -> list[int]:
    blocks = [
        [0],
        closed_range(1, p),
        closed_range(3 * p, 4 * p - 2),
        closed_range(6 * p, 8 * p - 2),
        closed_range(8 * p, 10 * p - 2),
        [10 * p],
        closed_range(11 * p - 1, 12 * p - 1),
        closed_range(13 * p + 1, 14 * p - 2),
        closed_range(14 * p, 15 * p - 1),
        [16 * p],
        closed_range(17 * p - 1, 18 * p - 1),
    ]
    return sorted({value for block in blocks for value in block})


def support_independent(p: int, generators: list[int]) -> list[int]:
    return sorted(3 * p + value for value in generators if value >= 6 * p)


def bases_independent(p: int, generators: list[int]) -> list[set[int]]:
    q = 24 * p
    return [
        {0},
        set(generators),
        set(closed_range(0, 2 * p))
        | set(closed_range(3 * p, 5 * p - 2))
        | set(closed_range(6 * p, q - 1)),
        set(closed_range(0, q - 1)) - {6 * p - 1},
        set(closed_range(0, q - 1)),
    ]


def xor_rank(columns: list[set[int]]) -> int:
    pivots: dict[int, set[int]] = {}
    for raw in columns:
        column = set(raw)
        while column:
            pivot = max(column)
            if pivot in pivots:
                column.symmetric_difference_update(pivots[pivot])
            else:
                pivots[pivot] = column
                break
    return len(pivots)


def independent_p4_profile() -> dict[str, object]:
    p = 4
    generators = generators_independent(p)
    bases = bases_independent(p, generators)
    combinations = {
        size: list(itertools.combinations(generators, size)) for size in (1, 2, 3)
    }
    maximum = max(
        max(generators) + max(bases[3]),
        2 * max(generators) + max(bases[2]),
        4 * max(generators),
    )
    profile = {}
    block_hashes = []
    for b in range(maximum + 1):
        cells = {
            size: [cell for cell in combinations[size] if b - sum(cell) in bases[4 - size]]
            for size in (1, 2, 3)
        }
        vertex_index = {cell: index for index, cell in enumerate(cells[1])}
        edge_index = {cell: index for index, cell in enumerate(cells[2])}
        d2 = []
        for edge in cells[2]:
            d2.append(
                {
                    vertex_index[face]
                    for face in ((edge[0],), (edge[1],))
                    if face in vertex_index
                }
            )
        d3 = []
        for triangle in cells[3]:
            faces = (
                (triangle[1], triangle[2]),
                (triangle[0], triangle[2]),
                (triangle[0], triangle[1]),
            )
            d3.append({edge_index[face] for face in faces if face in edge_index})
        h1 = len(cells[2]) - xor_rank(d2) - xor_rank(d3)
        if h1:
            profile[b] = h1
        block_hashes.append(
            digest({"b": b, "sizes": [len(cells[size]) for size in (1, 2, 3)], "h1": h1})
        )
    expected = {b: 1 for b in support_independent(p, generators)}
    if profile != expected:
        raise AssertionError(f"independent p=4 profile mismatch: {profile}")
    return {
        "p": p,
        "maximum_offset": maximum,
        "support_count": len(profile),
        "support_hash": digest(sorted(profile)),
        "block_aggregate": digest(block_hashes),
    }


def audit_sample(row: dict[str, object]) -> dict[str, object]:
    p = int(row["p"])
    generators = generators_independent(p)
    support = support_independent(p, generators)
    beta_24 = 8 * p
    numerator = p * (5 * p - 1) * (500 * p * p - 440 * p + 47)
    beta_34 = numerator // 2
    checks = {
        "generator_count": len(generators) == 10 * p == row["generator_count"],
        "support_count": len(support) == beta_24 == row["support_count"],
        "support_hash": digest(support) == row["support_hash"],
        "beta_2_4": row["beta_2_4"] == beta_24,
        "beta_3_4": numerator % 2 == 0 and row["beta_3_4"] == beta_34,
        "hilbert_difference": (
            row["hilbert_numerator_coefficient_4"] == beta_24 - beta_34
        ),
        "all_recorded_predictions": all(row["predictions"].values()),
        "all_recorded_controls": all(row["controls"].values()),
    }
    controls = {
        "deleted_first_support_rejected": digest(support[1:]) != row["support_hash"],
        "beta_24_minus_one_rejected": row["beta_2_4"] != beta_24 - 1,
        "beta_34_sign_rejected": row["beta_3_4"] != -beta_34,
    }
    if not all(checks.values()) or not all(controls.values()):
        raise AssertionError(f"p={p}: audit failure checks={checks} controls={controls}")
    audited = {"p": p, "checks": checks, "controls": controls}
    audited["audit_hash"] = digest(audited)
    return audited


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--symbolic", type=Path, default=DEFAULT_SYMBOLIC)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--budget-seconds", type=float, default=120.0)
    args = parser.parse_args()

    started = time.perf_counter()
    campaign = json.loads(args.input.read_text(encoding="utf-8"))
    symbolic = json.loads(args.symbolic.read_text(encoding="utf-8"))
    if campaign["status"] != "PASS" or campaign["completed_rows"] != 297:
        raise AssertionError("canonical campaign is incomplete")
    if symbolic["status"] != "PASS" or len(symbolic["queries"]) != 6:
        raise AssertionError("symbolic certificate is incomplete")
    if not all(row["passed"] and row["result"] == "unsat" for row in symbolic["queries"]):
        raise AssertionError("a symbolic query is not UNSAT")
    aggregate = digest([row["row_hash"] for row in campaign["rows"]])
    if aggregate != campaign["campaign_aggregate"]:
        raise AssertionError("campaign aggregate mismatch")

    by_p = {int(row["p"]): row for row in campaign["rows"]}
    rows = [audit_sample(by_p[p]) for p in SAMPLES]
    explicit = independent_p4_profile()
    elapsed = time.perf_counter() - started
    status = "PASS" if elapsed <= args.budget_seconds else "INCONCLUSIVE_BUDGET"
    result = {
        "experiment": "EXP-027-relative-betti-strand-audit",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "samples": list(SAMPLES),
        "campaign_aggregate": aggregate,
        "symbolic_aggregate": symbolic["aggregate"],
        "independent_p4_profile": explicit,
        "rows": rows,
        "audit_aggregate": digest([row["audit_hash"] for row in rows] + [explicit["block_aggregate"]]),
        "elapsed_seconds": elapsed,
    }
    write_json_atomic(args.output, result)
    print(
        f"EXP-027 audit {status}: samples={len(rows)} h1={explicit['support_count']} "
        f"aggregate={result['audit_aggregate']} elapsed={elapsed:.3f}s"
    )
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
