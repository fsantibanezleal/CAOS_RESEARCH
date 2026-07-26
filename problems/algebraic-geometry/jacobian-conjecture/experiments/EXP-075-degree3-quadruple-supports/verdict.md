# EXP-075 verdict: degree-three polynomial covectors excluded

Decided 2026-07-25 by targeted reproduction of the existing blocker-first hit.

## Result

The declared regression gate passed. The support at reordered index 2662,
$$
\{(0,3),(1,0),(3,4),(4,7)\},
$$
makes the degree-three necessary subsystem infeasible independently over both configured
primes. The original artifact reports the same support, and the targeted rerun reproduced it
in 12 seconds.

## Logical force

This is the conclusive direction of a support test. A global polynomial covector of parameter
degree at most three would restrict to a solution on every four-parameter coordinate slice.
The displayed slice has no solution. Therefore no global degree-three polynomial covector
exists in the declared certificate class.

This supersedes the stale “open through triples” summary. EXP-093's proposed full cubic solve
has an empty target and is cancelled.

## What this does not prove

- It does not prove the reduced Keller system is consistent.
- It does not produce a counterexample skeleton.
- It does not exclude covectors of degree at least four.
- It does not prove that a finite polynomial covector is necessary for uniform inconsistency.
- It does not decide $(72,108)$ or raise the planar degree floor.

## Preserved evidence

- `artifacts/output-run2-2026-07-24.txt`: original full blockers-first log and hit.
- `artifacts/output-targeted-rerun-2026-07-25.txt`: exact targeted reproduction from index 2662.
- `run2.py`: deterministic blocker-first ordering and two-prime decision path.

## Route decision

Stop the quadruple sweep after the first conclusive hit. Do not test the remaining 247,237
supports. The certificate tower now has exact exclusions at degrees one, two, and three, but
no valid finite ceiling. The next work is structural: source restrictions, applicability
through the GGHV reduction, and an all-degree certificate-module or chart-cover formulation.
