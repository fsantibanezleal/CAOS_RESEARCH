"""Independent reconstruction audit for EXP-012.

This module intentionally does not import EXP-011 or EXP-012 run code.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "artifacts/results.json"
AUDIT = ROOT / "artifacts/audit.json"


def closed(start: int, stop: int) -> set[int]:
    return set(range(start, stop + 1)) if start <= stop else set()


def canonical_hash(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def reconstruct(p: int) -> dict[str, object]:
    s = 6 * p
    a = closed(0, p) | closed(3 * p, 4 * p - 2)
    b = (
        (closed(p + 1, 3 * p - 1) - {2 * p - 1})
        | {4 * p}
        | closed(5 * p - 1, 6 * p - 1)
    )
    q = closed(p + 1, 2 * p - 2) | {2 * p, 4 * p}
    c = closed(0, 2 * p) | closed(3 * p, 5 * p - 2)
    generators = sorted(
        {4 * s + r for r in a}
        | closed(5 * s, 6 * s - 1)
        | {6 * s + r for r in b}
        | {7 * s + r for r in q}
    )
    conductor = 9 * s
    frobenius = conductor - 1

    def belongs(value: int) -> bool:
        if value == 0 or value >= conductor:
            return True
        level, residue = divmod(value, s)
        return (
            (level == 4 and residue in a)
            or level == 5
            or (level == 6 and residue in b)
            or (level == 7 and residue in q)
            or (level == 8 and residue in c)
        )

    gaps = [value for value in range(1, conductor) if not belongs(value)]
    pseudo_frobenius = tuple(
        value
        for value in gaps
        if all(belongs(value + generator) for generator in generators)
    )
    top_gaps = tuple(
        value for value in gaps if conductor - 4 * s <= value < conductor
    )
    if pseudo_frobenius != top_gaps:
        raise AssertionError(f"p={p}: independent lower PF witness")
    reflected = {
        frobenius - value
        for value in pseudo_frobenius
        if value != frobenius
    }
    return {
        "p": p,
        "type": len(pseudo_frobenius),
        "reduced_type": len(top_gaps),
        "maximal_reduced_type": pseudo_frobenius == top_gaps,
        "almost_symmetric": reflected <= set(pseudo_frobenius),
        "first_pf": pseudo_frobenius[0],
        "last_pf": pseudo_frobenius[-1],
        "pf_hash": canonical_hash(pseudo_frobenius),
    }


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def main() -> int:
    campaign = json.loads(RESULTS.read_text(encoding="utf-8"))
    rows = campaign["rows"]
    if campaign["range"] != {"first": 4, "last": 300, "count": 297}:
        raise AssertionError("campaign range is not the declared full range")
    rehashed = []
    row_by_p = {}
    for row in rows:
        supplied = row["row_hash"]
        body = {key: value for key, value in row.items() if key != "row_hash"}
        if canonical_hash(body) != supplied:
            raise AssertionError(f"p={row['p']}: row hash mismatch")
        rehashed.append(supplied)
        row_by_p[row["p"]] = row
    if canonical_hash(rehashed) != campaign["campaign_aggregate"]:
        raise AssertionError("campaign aggregate mismatch")

    samples = []
    for p in (4, 5, 17, 73, 151, 300):
        independent = reconstruct(p)
        recorded = row_by_p[p]
        for key in (
            "type",
            "reduced_type",
            "maximal_reduced_type",
            "almost_symmetric",
            "first_pf",
            "last_pf",
            "pf_hash",
        ):
            if independent[key] != recorded[key]:
                raise AssertionError(f"p={p}: independent {key} mismatch")
        samples.append(independent)

    control_p = 4
    control = reconstruct(control_p)
    if control["first_pf"] == 5 * (6 * control_p) - 1:
        raise AssertionError("injected lower-gap control was accepted")
    if control["type"] - 1 == control["reduced_type"]:
        raise AssertionError("deleted-PF control was accepted as maximal reduced type")

    audit = {
        "experiment": "EXP-012-endomorphism-type",
        "status": "AUDIT_PASS",
        "campaign_aggregate": campaign["campaign_aggregate"],
        "rehash_count": len(rows),
        "sample_parameters": [sample["p"] for sample in samples],
        "sample_hash": canonical_hash(samples),
        "controls": {
            "injected_lower_gap_rejected": True,
            "deleted_pf_rejected": True,
        },
    }
    audit["audit_aggregate"] = canonical_hash(audit)
    write_json_atomic(AUDIT, audit)
    print(f"EXP-012 audit PASS aggregate={audit['audit_aggregate']}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
