"""EXP-068 independent auditor: plain integer sets, no shared code with hwcert.gluing.

Re-derives (1) the Pham x Pham four-generated extension (minimal generators, symmetry, partition
criterion) and (2) the direct torsion length of the glued ideal on a subsample of the producer's
cases, by breadth-first search over the monomial relation graph. Reads artifacts/results.json and
writes artifacts/audit.json. Run from the repository root.
"""

from __future__ import annotations

import json
from collections import deque
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
PHAM = (56, 57, 58, 63, 64, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 87, 89, 90, 93, 95, 96, 97)


class Semigroup:
    def __init__(self, gens: tuple[int, ...], bound: int) -> None:
        self.gens = gens
        self.bound = bound
        table = [False] * (bound + 1)
        table[0] = True
        for v in range(1, bound + 1):
            table[v] = any(v >= g and table[v - g] for g in gens)
        self.table = table
        self.frobenius = max(v for v in range(bound + 1) if not table[v])
        if self.frobenius + max(gens) >= bound:
            raise ValueError("bound too small")

    def __contains__(self, v: int) -> bool:
        return v >= 0 and (v > self.bound or self.table[v])


def ideal_member(sg: Semigroup, gens, v: int) -> bool:
    return any((v - g) in sg for g in gens)


def minimal_gens(sg: Semigroup, gens) -> tuple[int, ...]:
    candidates = sorted(set(gens))
    return tuple(x for x in candidates if not any(ideal_member(sg, gens, x - s) for s in sg.gens))


def dual_member(sg: Semigroup, gens, z: int) -> bool:
    return all((z + g) in sg for g in gens)


def as_set(predicate, lo: int, hi: int) -> frozenset[int]:
    return frozenset(v for v in range(lo, hi) if predicate(v))


def huneke_wiegand(sg: Semigroup, gens, lo: int, hi: int) -> bool | None:
    gens = minimal_gens(sg, gens)
    if len(gens) == 1:
        return None
    star_gens_limit = hi
    star = as_set(lambda z: dual_member(sg, gens, z), lo, star_gens_limit)

    def plus(left_gens, right: frozenset[int]) -> frozenset[int]:
        return frozenset(v for v in range(lo, hi) if any((v - p) in right or v - p >= star_gens_limit for p in left_gens))

    for size in range(1, len(gens)):
        for p in combinations(gens, size):
            if gens[0] not in p:
                continue
            q = tuple(x for x in gens if x not in p)
            meet = as_set(lambda v: ideal_member(sg, p, v) and ideal_member(sg, q, v), lo, hi)
            meet_gens = tuple(x for x in sorted(meet) if not any((x - s) in meet for s in sg.gens))
            left = plus(p, star) & plus(q, star)
            right = plus(meet_gens, star)
            if left != right:
                return True
    return False


def direct_torsion(sg: Semigroup, gens) -> int:
    gens = minimal_gens(sg, gens)
    lo = -max(gens)
    star_min = next(z for z in range(lo, sg.bound) if dual_member(sg, gens, z))
    conductor = sg.frobenius + 1
    star_conductor = next(c for c in range(star_min, sg.bound) if all(dual_member(sg, gens, z) for z in range(c, c + max(sg.gens) + 1)))
    top = max(gens) + conductor + star_conductor
    total = 0
    for d in range(min(gens) + star_min, top + 1):
        nodes = [x for x in range(min(gens), d - star_min + 1)
                 if ideal_member(sg, gens, x) and dual_member(sg, gens, d - x)]
        node_set, seen, comps = set(nodes), set(), 0
        for start in nodes:
            if start in seen:
                continue
            comps += 1
            queue = deque([start])
            seen.add(start)
            while queue:
                x = queue.popleft()
                for g in sg.gens:
                    for y in (x - g, x + g):
                        if y in node_set and y not in seen:
                            low = min(x, y)
                            if ideal_member(sg, gens, low):
                                seen.add(y)
                                queue.append(y)
        total += max(0, comps - 1)
    return total


def main() -> int:
    results = json.loads((HERE / "artifacts" / "results.json").read_text(encoding="utf-8"))
    report: dict[str, object] = {}

    a1, a2 = 56, 57
    glued = tuple(sorted({a1 * g for g in PHAM} | {a2 * g for g in PHAM}))
    sg = Semigroup(glued, 30000)
    ext = sorted({a1 * x + a2 * z for x in (0, 14) for z in (0, 14)})
    mg = minimal_gens(sg, ext)
    symmetric = all((x in sg) != ((sg.frobenius - x) in sg) for x in range(sg.frobenius + 1))
    hw = huneke_wiegand(sg, ext, -max(ext) - 4, sg.frobenius + 3 * max(ext))
    report["pham_x_pham"] = {"frobenius": sg.frobenius, "symmetric": symmetric, "minimal_generators": mg,
                             "huneke_wiegand": hw}
    print("Pham x Pham:", report["pham_x_pham"], flush=True)

    sample = results["cases"][::8]
    rows = []
    for case in sample:
        bound = 4 * (case["a1"] * max(case["gens1"]) ** 2 + case["a2"] * max(case["gens2"]) ** 2 + case["a1"] * case["a2"])
        glued_small = tuple(sorted({case["a1"] * g for g in case["gens1"]} | {case["a2"] * g for g in case["gens2"]}))
        sgs = Semigroup(glued_small, bound)
        torsion = direct_torsion(sgs, tuple(case["ideal"]))
        rows.append({"index": case["index"], "audit_torsion": torsion, "producer_direct": case["torsion_direct"],
                     "producer_predicted": case["torsion_predicted"],
                     "agree": torsion == case["torsion_direct"] == case["torsion_predicted"]})
    report["torsion_subsample"] = rows
    report["torsion_subsample_all_agree"] = all(r["agree"] for r in rows)
    ok = (report["torsion_subsample_all_agree"] and hw is False and len(mg) == 4 and symmetric
          and sg.frobenius == 23645)
    report["audit_pass"] = ok
    (HERE / "artifacts" / "audit.json").write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")
    print("subsample agree:", report["torsion_subsample_all_agree"], "cases:", len(rows), "audit_pass:", ok)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
