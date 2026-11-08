# EXP-142 verdict: UNKNOWN (both branch certificates exceed the 6,000-prime budget)

Date: 2026-11-08. Hypothesis frozen at 77584b41.

## Result

- **Reduction [D], checked exactly:** E2 = a2 (q1^2 - c^2)^2 in L[q1] with a2 != 0 (`branches.py`), so Case 1 is
  empty iff both branch ideals q1 = +c and q1 = -c are the unit ideal. On each branch E1, E2, E4 and E8 vanish and
  nine equations remain in q0, q2, q3, q4, q5.
- **Gates PASS** (`artifacts/gates-output.txt`): both branch systems are unit at a root of P modulo each of the five
  gate primes; the pipeline gates of EXP-141 apply unchanged.
- **Certificates UNKNOWN:** each branch ran to its budget with every prime lucky (no prime discarded): 6,085 kept
  primes on q1 = +c and 6,069 on q1 = -c (the budget is checked after each batch, so the last batch overshot 6,000
  by 85 and 69 primes), 30,270 coordinates per branch (6,054 cofactor terms). At the last checkpoints (6,082 and
  6,066 primes, moduli of about 56,700 digits) no sampled coordinate reconstructs, also with the common-denominator
  pass: in every sampled coordinate the numerator or the denominator has more than about 28,000 digits.
- **Structure found on the way** (`structure.md`, scripts in `probes/`): E1 and E2 proportional over L; every
  branch equation linear in q5; E3, E7 and E13 with proportional q5 and q3 coefficients, giving a small quadric
  S(q0, q2, q4); rank 8 over L; near-minimal unit subsets mod p cut out 100 to 138 points; exact standard bases
  over Q(y) do not finish in an hour; a resultant chain ends in degree 568. None gives a shorter certificate.

## Run record

The runs were restarted twice without changing the method or any stored residue: once to checkpoint every 160
primes instead of 32, since each checkpoint re-ran the full reconstruction over all primes; and once because Git
Bash rewrote the crt_recon path given in the environment into a Windows path, so the checkpoints of that interval
failed (`run.log`). crt_recon gained a common-denominator pass and a sampled pre-pass (every 61st coordinate first;
the full pass only when all samples reconstruct), both checked on the planted gate with an identical certificate.

## Follow-up

The cost is linear in the height, so EXP-143 continues both branches from the stored residues with an extended
budget (up to 20,000 primes per branch, moduli of about 186,000 digits) on more processes.
