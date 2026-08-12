"""Independent reconstruction audit for EXP-016; imports no experiment code."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "artifacts" / "results.json"
AUDIT = ROOT / "artifacts" / "audit.json"


def digest(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def seq(start: int, stop: int) -> set[int]:
    return set(range(start, stop + 1)) if start <= stop else set()


def reconstruct(p: int) -> dict[str, object]:
    s = 6 * p
    a = seq(0, p) | seq(3 * p, 4 * p - 2)
    b = (
        (seq(p + 1, 3 * p - 1) - {2 * p - 1})
        | {4 * p}
        | seq(5 * p - 1, 6 * p - 1)
    )
    c = seq(0, 2 * p) | seq(3 * p, 5 * p - 2)
    layers = {
        4: a,
        5: a | b,
        6: b,
        8: c,
        9: seq(0, s - 1),
        10: seq(0, s - 1),
        11: seq(0, s - 1),
        12: seq(0, s - 2),
    }
    stop = 17 * s - 1
    square: set[int] = set()
    items = sorted(layers.items())
    for left_index, (left_level, left) in enumerate(items):
        for right_level, right in items[left_index:]:
            base = (left_level + right_level) * s
            if base <= stop:
                square.update(
                    base + x + y
                    for x in left
                    for y in right
                    if base + x + y <= stop
                )
    expected = (
        {8 * s + residue for residue in c}
        | seq(9 * s, 13 * s - 2)
        | seq(13 * s, stop)
    )
    if square != expected or 13 * s - 1 in square or 17 * s - 1 not in square:
        raise AssertionError(f"audit p={p}: corrected square formula mismatch")
    t_values = {
        level * s + residue
        for level, residues in layers.items()
        for residue in residues
    }
    shifted = {4 * s + value for value in t_values if 4 * s + value <= stop}
    defect = sorted(square - shifted)
    counts = {
        str(level): sum(value // s == level for value in defect)
        for level in (8, 9, 10, 11, 12, 16)
    }
    return {
        "p": p,
        "defect_length": len(defect),
        "level_counts": counts,
        "square_hash_through_17s_minus_1": digest(sorted(square)),
        "defect_hash": digest(defect),
    }


def main() -> int:
    source = json.loads(RESULTS.read_text(encoding="utf-8"))
    rows = source["rows"]
    if digest([row["row_hash"] for row in rows]) != source["campaign_aggregate"]:
        raise AssertionError("campaign row hashes do not reproduce")
    indexed = {row["p"]: row for row in rows}
    samples = [4, 5, 17, 73, 151, 300]
    checks = []
    for p in samples:
        check = reconstruct(p)
        row = indexed[p]
        for field in (
            "defect_length",
            "level_counts",
            "square_hash_through_17s_minus_1",
            "defect_hash",
        ):
            if check[field] != row[field]:
                raise AssertionError(f"audit p={p}: {field} mismatch")
        checks.append(check)
    output = {
        "experiment": "EXP-016-corrected-stability-defect",
        "status": "AUDIT_PASS",
        "all_rows_rehashed": True,
        "sample_parameters": samples,
        "checks": checks,
        "audit_aggregate": digest(checks),
    }
    AUDIT.parent.mkdir(parents=True, exist_ok=True)
    temporary = AUDIT.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    temporary.replace(AUDIT)
    print(f"EXP-016 audit PASS aggregate={output['audit_aggregate']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
