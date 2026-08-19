"""Independent reconstruction audit for EXP-013; imports no experiment code."""

from __future__ import annotations

import hashlib
import json
from functools import cache
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "artifacts" / "results.json"
AUDIT = ROOT / "artifacts" / "audit.json"


def canonical_hash(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


@cache
def blocks(p: int) -> tuple[int, set[int], set[int], set[int], set[int]]:
    s = 6 * p
    a = set(range(p + 1)) | set(range(3 * p, 4 * p - 1))
    b = (
        (set(range(p + 1, 3 * p)) - {2 * p - 1})
        | {4 * p}
        | set(range(5 * p - 1, 6 * p))
    )
    c = set(range(2 * p + 1)) | set(range(3 * p, 5 * p - 1))
    q = set(range(p + 1, 2 * p - 1)) | {2 * p, 4 * p}
    return s, a, b, c, q


def gamma(n: int, p: int) -> bool:
    if n == 0:
        return True
    if n < 0:
        return False
    s, a, b, c, _ = blocks(p)
    k, r = divmod(n, s)
    table = {4: a, 5: set(range(s)), 6: b, 8: c}
    if k in table:
        return r in table[k]
    return 9 <= k <= 11 or (k == 12 and r < s - 1) or k >= 13


def lam(n: int, p: int) -> bool:
    s, _, _, _, q = blocks(p)
    return gamma(n, p) or (n // s == 7 and n % s in q) or n == 13 * s - 1


def reconstruct(p: int) -> dict[str, object]:
    s, a, b, c, q = blocks(p)
    limit = 15 * s
    new_e_values = {7 * s + residue for residue in q} | {13 * s - 1}
    conductor = {
        n
        for n in range(limit + 1)
        if gamma(n, p)
        and (n >= 6 * s or all(gamma(n + e, p) for e in new_e_values))
    }
    expected = {
        n
        for n in range(limit + 1)
        if (n // s == 4 and n % s in a)
        or (n // s == 5 and n % s in a | b)
        or (n // s == 6 and n % s in b)
        or (n // s == 8 and n % s in c)
        or (n // s >= 9 and gamma(n, p))
    }
    if conductor != expected:
        raise AssertionError(f"audit p={p}: conductor mismatch at {min(conductor ^ expected)}")
    w = {n for n in range(limit + 1) if gamma(n, p) and gamma(n + s, p)}
    trace_j = w | {n + s for n in w if n + s <= limit}
    if any(
        n + e <= limit and n + e not in conductor
        for n in conductor
        if n < 6 * s
        for e in new_e_values
    ):
        raise AssertionError(f"audit p={p}: conductor is not an E-ideal")
    trace_e = set(conductor)
    if trace_j != expected or trace_e != expected:
        raise AssertionError(f"audit p={p}: trace mismatch")
    missing = {n for n in range(9 * s) if gamma(n, p) and n not in expected}
    reflected = {s - 1 - residue for residue in q}
    if missing != {0} | {5 * s + residue for residue in reflected}:
        raise AssertionError(f"audit p={p}: defect formula mismatch")
    return {
        "p": p,
        "colength": len(missing),
        "trace_hash_through_15s": canonical_hash(sorted(expected)),
    }


def main() -> int:
    source = json.loads(RESULTS.read_text(encoding="utf-8"))
    rows = source["rows"]
    if canonical_hash([row["row_hash"] for row in rows]) != source["campaign_aggregate"]:
        raise AssertionError("campaign row hashes do not reproduce")
    samples = [4, 5, 17, 73, 151, 300]
    checks = []
    indexed = {row["p"]: row for row in rows}
    for p in samples:
        check = reconstruct(p)
        if check["colength"] != indexed[p]["colength"]:
            raise AssertionError(f"audit p={p}: committed colength mismatch")
        if check["trace_hash_through_15s"] != indexed[p]["trace_hash_through_15s"]:
            raise AssertionError(f"audit p={p}: committed trace hash mismatch")
        checks.append(check)
    aggregate = canonical_hash(checks)
    output = {
        "experiment": "EXP-013-trace-conductor",
        "status": "AUDIT_PASS",
        "all_rows_rehashed": True,
        "sample_parameters": samples,
        "checks": checks,
        "audit_aggregate": aggregate,
    }
    AUDIT.parent.mkdir(parents=True, exist_ok=True)
    temporary = AUDIT.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    temporary.replace(AUDIT)
    print(f"EXP-013 audit PASS aggregate={aggregate}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
