# EXP-094: Audit the source identities for C10, C11, C19, and C20

## Question

Do the exclusions in the closing remark of Guccione, Guccione, and Valqui
(arXiv:1605.09430) actually apply to configurations C10, C11, C19, and C20, or
were those configurations marked as candidates only because distinct source
objects were conflated?

## Motivation

EXP-084 and EXP-085 marked these four configurations as strong candidates for
exclusion. The primary sources distinguish:

- the main corner \(A_0\);
- the lower endpoint \(A'_0\);
- \(B_0=m^{-1}\operatorname{st}_{1,0}(P)\);
- \(B_1=m^{-1}\operatorname{en}_{1,0}(P)\).

The source theorem gives \(B_1=A_0\). The exclusions cited for \(A_0=(7,21)\)
also require \(A'_0=(2,1)\). The exclusions with \(B_0=(6,15)\) require
\(B_1=(6,18+6k)\), subject to a divisibility condition. The persisted family
table instead gives \(A'_0=(1,0)\) for C10 and C11, and \(B_1=A_0=(6,15)\) for
C19 and C20.

## Primary-source facts

1. GGHV17, arXiv:1708.07936, Theorem 2.20 proof: the first complete-chain
   corner satisfies
   \(A_0=m^{-1}\operatorname{en}_{1,0}(P)=B_1\).
2. GGHV17, section 5 family table:
   - C10 is family F9 with \(A_0=(7,21)\) and \(A'_0=(1,0)\);
   - C11 is family F11 with \(A_0=(7,21)\) and \(A'_0=(1,0)\);
   - C19 is family F7 with \(A_0=(6,15)\) and \(A'_0=(1,0)\);
   - C20 is family F8 with \(A_0=(6,15)\) and \(A'_0=(1,0)\).
3. GGV2, arXiv:1605.09430, Remark 2.32:
   - the two discarded Heitmann families corresponding to \(A_0=(7,21)\)
     come from \(A'_0=(2,1)\);
   - the separate \(B_0=(6,15)\) exclusions require
     \(B_1=(6,18+6k)\), where \(18+6k\) is not a multiple of 30.

## Premise dependencies

- The four family-table rows are verified transcriptions in
  `context/2026-07-22-beyond125-and-audit-dossier.md` and in the GGHV17 TeX
  source.
- The equality \(B_1=A_0\) is a source definition, not a computational
  hypothesis.
- The exclusion predicates are transcribed from GGV2 Remark 2.32.
- EXP-082 supplies a positive source-matching control:
  \(B_0=(8,28)\), \(B_1=(8,40)\) is excluded.

## Falsifiable prediction

All four configurations fail the exact source predicates:

- C10 and C11 have \(A'_0=(1,0)\), not \((2,1)\);
- C19 and C20 have \(B_1=A_0=(6,15)\), not
  \((6,18+6k)\).

Therefore the cited remark does not exclude any of the four. This would correct
their classification from strong candidate for exclusion to unresolved by that
remark.

## Invariant-first note

The endpoint identities \(A'_0\) and \(B_1\) are complete deciders for whether
the cited source predicates match. No polynomial-system computation, support
sweep, or numerical experiment is relevant.

## What a PASS proves and what a FAIL proves

- PASS: the four persisted rows fail the exact predicates in the cited remark.
  This proves only that this remark does not exclude C10, C11, C19, or C20.
  It does not prove that the configurations occur, survive other theorems, or
  yield counterexamples.
- FAIL: at least one persisted row matches a source predicate. That row becomes
  a genuine exclusion candidate and requires an independent chain-identity
  derivation before its status changes.

## Method and adversarial controls

Run an exact integer/tuple classifier over the four rows and the predicates
above. Require these controls:

1. \(A_0=(7,21)\), \(A'_0=(2,1)\) matches the discarded Heitmann condition.
2. \(B_0=(6,15)\), \(B_1=(6,18)\) matches the GGV condition.
3. \(B_0=(6,15)\), \(B_1=(6,30)\) does not match because 30 is excluded by
   the divisibility clause.
4. The EXP-082 pair \(B_0=(8,28)\), \(B_1=(8,40)\) matches its known
   exclusion.

## Compute budget and kill criterion

CPU only, exact integer arithmetic, expected runtime below one second. Budget:
10 seconds. There is no checkpoint because the full decision is atomic. If the
script does not finish within the budget, record an infrastructure failure and
draw no mathematical conclusion.

Declared 2026-07-25 before running `run.py`.
