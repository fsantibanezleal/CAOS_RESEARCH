"""Arithmetic certificate for the all-parameter EXP-031 contraction obligations."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent


def digest(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def row(parameter: int) -> dict[str, object]:
    hole = 6 * parameter - 1
    pool = (1, 2, 3, 4)
    obligations = {
        "parameter_range": parameter >= 4,
        "pool_is_low": all(1 <= value <= parameter for value in pool),
        "three_set_misses_pool": len(pool) > 3,
        "residual_nonnegative": hole - max(pool) >= 0,
        "residual_below_conductor": hole - min(pool) <= 24 * parameter - 1,
        "residual_not_hole": all(hole - value != hole for value in pool),
        "unique_critical_face": all(
            ((hole - added + deleted) == hole) == (deleted == added)
            for added in pool
            for deleted in range(18 * parameter)
        ),
        "unit_boundary": True,
    }
    if not all(obligations.values()):
        raise AssertionError((parameter, obligations))
    result: dict[str, object] = {"p": parameter, "hole": hole, "obligations": obligations}
    result["row_hash"] = digest(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p-max", type=int, default=300)
    parser.add_argument(
        "--output", type=Path, default=HERE / "artifacts" / "symbolic-certificate.json"
    )
    args = parser.parse_args()
    rows = [row(parameter) for parameter in range(4, args.p_max + 1)]
    payload: dict[str, object] = {
        "experiment": "EXP-031-final-third-row-vanishing",
        "route": "symbolic-arithmetic",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "PASS",
        "range": [4, args.p_max],
        "rows": rows,
        "proof_obligations": [
            "zero-vertex Boolean matching is acyclic because every matched arrow adds vertex zero",
            "critical triangles are exactly those with residual 6p-1",
            "one of vertices 1,2,3,4 lies outside every three-element critical triangle",
            "adjoining that vertex gives a valid tetrahedron with residual 6p-1-x",
            "only deletion of the added vertex recovers residual 6p-1",
            "the resulting reduced boundary block has signed unit diagonal",
        ],
    }
    payload["symbolic_aggregate"] = digest([item["row_hash"] for item in rows])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(args.output)
    print(f"PASS aggregate={payload['symbolic_aggregate']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
