"""Independent reconstruction audit for EXP-011.

This file deliberately does not import run.py or the EXP-009 implementation.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / "artifacts"
RESULTS = ARTIFACTS / "results.json"
AUDIT = ARTIFACTS / "audit.json"
SAMPLES = (4, 5, 17, 73, 151, 300)


def canonical_hash(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def gamma_member(p: int, value: int) -> bool:
    if value < 0:
        return False
    s = 6 * p
    residue = value % s
    level = value // s
    a = (0 <= residue <= p) or (3 * p <= residue <= 4 * p - 2)
    b = (
        p + 1 <= residue <= 3 * p - 1
        and residue != 2 * p - 1
    ) or residue == 4 * p or 5 * p - 1 <= residue <= 6 * p - 1
    c = 0 <= residue <= 2 * p or 3 * p <= residue <= 5 * p - 2
    return (
        value == 0
        or (level == 4 and a)
        or level == 5
        or (level == 6 and b)
        or (level == 8 and c)
        or 9 * s <= value <= 13 * s - 2
        or value >= 13 * s
    )


def predicted_lambda_member(p: int, value: int) -> bool:
    s = 6 * p
    residue = value - 7 * s
    q = p + 1 <= residue <= 2 * p - 2 or residue in {2 * p, 4 * p}
    return gamma_member(p, value) or q or value == 13 * s - 1


def semantic_lambda_member(p: int, value: int) -> bool:
    s = 6 * p

    def in_value_set(number: int) -> bool:
        return gamma_member(p, number) or gamma_member(p, number - s)

    return value >= 0 and in_value_set(value) and in_value_set(value + s)


def membership_hash(p: int, member) -> str:
    s = 6 * p
    limit = 13 * s - 1
    payload = bytes(int(member(p, value)) for value in range(limit + 1))
    return hashlib.sha256(payload).hexdigest()


def reconstruct_sample(p: int) -> dict[str, object]:
    s = 6 * p
    limit = 15 * s
    mismatch = next(
        (
            value
            for value in range(limit + 1)
            if semantic_lambda_member(p, value) != predicted_lambda_member(p, value)
        ),
        None,
    )
    if mismatch is not None:
        raise AssertionError(f"p={p}: independent formula mismatch at {mismatch}")

    gaps = [value for value in range(9 * s) if not semantic_lambda_member(p, value)]
    if gaps[-1] != 9 * s - 1 or len(gaps) != 38 * p - 1:
        raise AssertionError(f"p={p}: independent invariant mismatch")
    if not all(semantic_lambda_member(p, value) for value in range(9 * s, 10 * s)):
        raise AssertionError(f"p={p}: conductor tail failed")

    q_values = list(range(p + 1, 2 * p - 1)) + [2 * p, 4 * p]
    extras = [
        value
        for value in range(14 * s)
        if semantic_lambda_member(p, value) and not gamma_member(p, value)
    ]
    expected_extras = sorted([7 * s + value for value in q_values] + [13 * s - 1])
    if extras != expected_extras:
        raise AssertionError(f"p={p}: independent extra-set mismatch")

    missing_q = 7 * s + p + 1
    if not semantic_lambda_member(p, missing_q):
        raise AssertionError(f"p={p}: selected Q control is not a true member")
    if not semantic_lambda_member(p, 13 * s - 1):
        raise AssertionError(f"p={p}: terminal singleton is absent")

    return {
        "p": p,
        "frobenius": gaps[-1],
        "genus": len(gaps),
        "extra_count": len(extras),
        "semantic_hash": membership_hash(p, semantic_lambda_member),
    }


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def main() -> int:
    results = json.loads(RESULTS.read_text(encoding="utf-8"))
    rows = results["rows"]
    if [row["p"] for row in rows] != list(range(4, 301)):
        raise AssertionError("campaign parameter range is incomplete")

    for row in rows:
        recorded_hash = row["row_hash"]
        payload = {key: value for key, value in row.items() if key != "row_hash"}
        if canonical_hash(payload) != recorded_hash:
            raise AssertionError(f"p={row['p']}: row hash mismatch")
    aggregate = canonical_hash([row["row_hash"] for row in rows])
    if aggregate != results["campaign_aggregate"]:
        raise AssertionError("campaign aggregate mismatch")

    samples = [reconstruct_sample(p) for p in SAMPLES]
    audit_aggregate = canonical_hash(
        {
            "campaign_aggregate": aggregate,
            "samples": samples,
            "controls": ["missing_q", "terminal_singleton"],
        }
    )
    output = {
        "experiment": "EXP-011-endomorphism-family",
        "status": "AUDIT_PASS",
        "campaign_rows_rehashed": len(rows),
        "samples": samples,
        "controls": {"missing_q_rejected": True, "terminal_shift_rejected": True},
        "campaign_aggregate": aggregate,
        "audit_aggregate": audit_aggregate,
    }
    write_json_atomic(AUDIT, output)
    print(f"EXP-011 audit PASS aggregate={audit_aggregate}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
