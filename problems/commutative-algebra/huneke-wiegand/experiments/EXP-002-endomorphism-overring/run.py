"""EXP-002: exact endomorphism-overring value semigroup by two routes."""

from __future__ import annotations

import heapq
import json
import math
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / "artifacts"
G = (
    56, 57, 58, 63, 64, 70, 71, 72, 73, 74, 75, 76, 77,
    78, 79, 80, 81, 82, 83, 87, 89, 90, 93, 95, 96, 97,
)
STEP = 14
EXPECTED_EXTRA = (101, 107, 181)


def log(message: str) -> None:
    line = f"[{time.strftime('%H:%M:%S')}] {message}"
    print(line, flush=True)
    with (ARTIFACTS / "run-log.txt").open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    log(f"PASS {message}")


def dp_membership(generators: tuple[int, ...], limit: int) -> tuple[bool, ...]:
    member = [False] * (limit + 1)
    member[0] = True
    for value in range(1, limit + 1):
        member[value] = any(value >= generator and member[value - generator] for generator in generators)
    return tuple(member)


def apery_dijkstra(generators: tuple[int, ...]) -> tuple[int, ...]:
    multiplicity = min(generators)
    infinity = 10**18
    distance = [infinity] * multiplicity
    distance[0] = 0
    queue = [(0, 0)]
    while queue:
        current, residue = heapq.heappop(queue)
        if current != distance[residue]:
            continue
        for generator in generators:
            candidate = current + generator
            target = candidate % multiplicity
            if candidate < distance[target]:
                distance[target] = candidate
                heapq.heappush(queue, (candidate, target))
    return tuple(distance)


def first_conductor(member, multiplicity: int, limit: int) -> int:
    for start in range(limit - multiplicity + 2):
        if all(member(value) for value in range(start, start + multiplicity)):
            return start
    raise RuntimeError("no conductor block within limit")


def analyze(member_gamma, limit: int) -> dict[str, object]:
    def member_v(value: int) -> bool:
        return value >= 0 and (member_gamma(value) or member_gamma(value - STEP))

    def member_lambda(value: int) -> bool:
        return value >= 0 and member_v(value) and member_v(value + STEP)

    conductor = first_conductor(member_lambda, min(G), limit)
    frobenius = conductor - 1
    gaps = tuple(value for value in range(conductor) if not member_lambda(value))
    extras = tuple(
        value for value in range(182) if member_lambda(value) and not member_gamma(value)
    )

    positive = [value for value in range(1, frobenius + min(G) + 1) if member_lambda(value)]
    minimal_generators = tuple(
        value
        for value in positive
        if not any(
            0 < other < value and member_lambda(other) and member_lambda(value - other)
            for other in positive
        )
    )
    pseudo_frobenius = tuple(
        gap
        for gap in gaps
        if all(member_lambda(gap + generator) for generator in minimal_generators)
    )
    closure_failures = tuple(
        (left, right)
        for left in range(conductor + min(G))
        for right in range(conductor + min(G))
        if member_lambda(left)
        and member_lambda(right)
        and not member_lambda(left + right)
    )
    failed_gamma_gaps = tuple(
        gap
        for gap in range(182)
        if not member_gamma(gap) and not member_lambda(gap)
    )
    return {
        "extras_over_gamma": extras,
        "frobenius": frobenius,
        "conductor": conductor,
        "genus": len(gaps),
        "symmetric": all(
            member_lambda(value) != member_lambda(frobenius - value)
            for value in range(frobenius + 1)
        ),
        "minimal_generators": minimal_generators,
        "pseudo_frobenius": pseudo_frobenius,
        "type": len(pseudo_frobenius),
        "closure_failures": closure_failures,
        "failed_gamma_gaps": failed_gamma_gaps,
        "stabilizer_101": member_lambda(101),
        "stabilizer_103": member_lambda(103),
    }


def main() -> int:
    ARTIFACTS.mkdir(exist_ok=True)
    (ARTIFACTS / "run-log.txt").write_text("", encoding="utf-8")
    log("EXP-002 start")
    require(math.gcd(*G) == 1, "input generators have gcd one")

    limit = 600
    dp = dp_membership(G, limit + max(G))

    def dp_gamma(value: int) -> bool:
        if value < 0:
            return False
        if value >= len(dp):
            raise ValueError("DP query outside bound")
        return dp[value]

    apery = apery_dijkstra(G)

    def apery_gamma(value: int) -> bool:
        return value >= 0 and value >= apery[value % min(G)]

    route_a = analyze(dp_gamma, limit)
    route_b = analyze(apery_gamma, limit)
    require(route_a == route_b, "P5 DP and Apery routes agree exactly")
    result = route_a

    require(result["extras_over_gamma"] == EXPECTED_EXTRA, "P1 exact three added values")
    require(result["frobenius"] == 125, "P2 Frobenius is 125")
    require(result["conductor"] == 126, "P2 conductor is 126")
    require(result["genus"] == 88, "P2 genus is 88")
    require(result["symmetric"] is False, "P3 Lambda is not symmetric")
    require(result["closure_failures"] == (), "P4 Lambda is additively closed")
    require(result["stabilizer_101"] is True, "P4 value 101 stabilizes V")
    require(result["stabilizer_103"] is False, "P6 false gap 103 is rejected")
    require(101 not in G and not dp_gamma(101), "P6 Gamma alone omits stabilizer 101")
    require(
        len(result["failed_gamma_gaps"]) == 88,
        "P4 every other Gamma gap below the old conductor fails stabilization",
    )

    output = {
        "verdict": "CONFIRMED",
        "predictions": {f"P{number}": "PASS" for number in range(1, 7)},
        "apery_gamma_mod_56": apery,
        "lambda": result,
    }
    (ARTIFACTS / "results.json").write_text(json.dumps(output, indent=2), encoding="utf-8")
    log(
        "DISCOVERY Lambda has type "
        f"{result['type']} with PF={result['pseudo_frobenius']}"
    )
    log("EXP-002 CONFIRMED: P1-P6 pass")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        ARTIFACTS.mkdir(exist_ok=True)
        log(f"FAIL {type(exc).__name__}: {exc}")
        raise
