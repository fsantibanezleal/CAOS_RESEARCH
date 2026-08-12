"""Independent reconstruction audit for EXP-014; imports no experiment code."""

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


def segment(start: int, end: int) -> set[int]:
    return set(range(start, end + 1)) if start <= end else set()


def reconstruct(p: int) -> dict[str, object]:
    s = 6 * p
    a = segment(0, p) | segment(3 * p, 4 * p - 2)
    b = (
        (segment(p + 1, 3 * p - 1) - {2 * p - 1})
        | {4 * p}
        | segment(5 * p - 1, 6 * p - 1)
    )
    c = segment(0, 2 * p) | segment(3 * p, 5 * p - 2)
    layers = {
        4: a,
        5: a | b,
        6: b,
        8: c,
        9: segment(0, s - 1),
        10: segment(0, s - 1),
        11: segment(0, s - 1),
        12: segment(0, s - 2),
    }
    stop = 17 * s - 1
    t_values = {
        level * s + residue
        for level, residues in layers.items()
        for residue in residues
    }
    shifted = {4 * s + value for value in t_values if 4 * s + value <= stop}

    square: set[int] = set()
    layer_items = sorted(layers.items())
    for left_index, (left_level, left) in enumerate(layer_items):
        for right_level, right in layer_items[left_index:]:
            base = (left_level + right_level) * s
            if base > stop:
                continue
            for left_residue in left:
                square.update(
                    base + left_residue + right_residue
                    for right_residue in right
                    if base + left_residue + right_residue <= stop
                )
    defect = sorted(square - shifted)
    witness = 8 * s + p + 1
    if witness not in defect or not defect:
        raise AssertionError(f"audit p={p}: nonstability witness failed")
    counts: dict[str, int] = {}
    for value in defect:
        level = str(value // s)
        counts[level] = counts.get(level, 0) + 1
    return {
        "p": p,
        "defect_length": len(defect),
        "level_counts": counts,
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
        for field in ("defect_length", "level_counts", "defect_hash"):
            if check[field] != row[field]:
                raise AssertionError(f"audit p={p}: {field} mismatch")
        checks.append(check)
    output = {
        "experiment": "EXP-014-conductor-stability",
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
    print(f"EXP-014 audit PASS aggregate={output['audit_aggregate']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
