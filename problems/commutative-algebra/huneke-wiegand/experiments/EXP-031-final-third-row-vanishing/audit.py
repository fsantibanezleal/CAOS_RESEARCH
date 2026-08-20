"""Independent EXP-031 unit-filler audit; imports no canonical experiment code."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from datetime import datetime, timezone
from math import comb
from pathlib import Path


HERE = Path(__file__).resolve().parent


def digest(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def save(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def generators(parameter: int) -> list[int]:
    blocks = [
        range(0, parameter + 1),
        range(3 * parameter, 4 * parameter - 1),
        range(6 * parameter, 8 * parameter - 1),
        range(8 * parameter, 10 * parameter - 1),
        [10 * parameter],
        range(11 * parameter - 1, 12 * parameter),
        range(13 * parameter + 1, 14 * parameter - 1),
        range(14 * parameter, 15 * parameter),
        [16 * parameter],
        range(17 * parameter - 1, 18 * parameter),
    ]
    return sorted({value for block in blocks for value in block})


def audit_parameter(parameter: int) -> dict[str, object]:
    vertices = [value for value in generators(parameter) if value]
    hole = 6 * parameter - 1
    alternative_pool = (4, 3, 2, 1)
    claimed_fillers: set[tuple[int, ...]] = set()
    signs = {"1": 0, "-1": 0}
    offsets: dict[int, int] = {}
    for face in itertools.combinations(vertices, 3):
        total = sum(face) + hole
        added = next(value for value in alternative_pool if value not in face)
        cell = tuple(sorted((*face, added)))
        residual = total - sum(cell)
        if not (0 <= residual <= 24 * parameter - 1 and residual != hole):
            raise AssertionError((parameter, face, added, residual))
        critical = []
        sign = None
        for deleted in range(len(cell)):
            boundary_face = cell[:deleted] + cell[deleted + 1 :]
            if total - sum(boundary_face) == hole:
                critical.append(boundary_face)
                sign = 1 if deleted % 2 == 0 else -1
        if critical != [face] or sign not in (-1, 1):
            raise AssertionError((parameter, face, critical, sign))
        if cell in claimed_fillers:
            raise AssertionError((parameter, "filler collision", cell))
        claimed_fillers.add(cell)
        signs[str(sign)] += 1
        offsets[total] = offsets.get(total, 0) + 1
    expected = comb(10 * parameter - 1, 3)
    controls = {
        "zero_filler_rejected": 0 not in alternative_pool and hole == hole,
        "wrong_hole_zero_rejected": all(-value < 0 for value in alternative_pool),
        "reused_single_filler_rejected": expected > 1,
        "three_candidate_pool_rejected": not any(
            value not in (1, 2, 3) for value in (1, 2, 3)
        ),
    }
    if len(claimed_fillers) != expected or not all(controls.values()):
        raise AssertionError((parameter, len(claimed_fillers), expected, controls))
    result: dict[str, object] = {
        "p": parameter,
        "generator_count": len(vertices) + 1,
        "critical_triangle_count": expected,
        "distinct_filler_count": len(claimed_fillers),
        "supported_offset_count": len(offsets),
        "offset_range": [min(offsets), max(offsets)],
        "unit_sign_counts": signs,
        "controls": controls,
    }
    result["row_hash"] = digest(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p-max", type=int, default=12)
    parser.add_argument("--budget-seconds", type=float, default=180.0)
    parser.add_argument("--output", type=Path, default=HERE / "artifacts" / "audit.json")
    args = parser.parse_args()
    started = time.perf_counter()
    rows = []
    for parameter in range(4, args.p_max + 1):
        rows.append(audit_parameter(parameter))
        print(f"audit p={parameter}: {rows[-1]['critical_triangle_count']}", flush=True)
        if time.perf_counter() - started > args.budget_seconds:
            payload = {
                "experiment": "EXP-031-final-third-row-vanishing",
                "route": "independent",
                "status": "INCONCLUSIVE_BUDGET",
                "completed": [row["p"] for row in rows],
                "elapsed_seconds": time.perf_counter() - started,
            }
            save(args.output, payload)
            return 2
    payload: dict[str, object] = {
        "experiment": "EXP-031-final-third-row-vanishing",
        "route": "independent",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "PASS",
        "range": [4, args.p_max],
        "rows": rows,
        "elapsed_seconds": time.perf_counter() - started,
    }
    payload["audit_aggregate"] = digest([row["row_hash"] for row in rows])
    save(args.output, payload)
    print(f"PASS aggregate={payload['audit_aggregate']}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
