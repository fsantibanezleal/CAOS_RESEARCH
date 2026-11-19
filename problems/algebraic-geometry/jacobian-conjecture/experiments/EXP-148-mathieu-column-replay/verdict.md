# EXP-148 verdict: CONFIRMED. Long's universal pair violates the Mathieu conjecture on SU(N) for every N from 2 to 16, exactly, on the range checked

Date: 2026-11-19. Hypothesis frozen in commit f6aa87e6 before any code ran. Exact rational arithmetic throughout
(`fractions.Fraction`; no float or complex value in the arithmetic). Run: `run.py`, exit 0, 4.4 s on one core; rerun by
the coordinating session with the same exit code and totals.

## What was computed

For P = (a + u)(a^2 v - (2a + u) tau^2), Q = u, A = a of C. D. Long (arXiv:2609.16178 v1, eqs. (3.1) to (3.3)), built by
polynomial arithmetic from (3.3), with z0 = g11, z1 = g21:

| Route | What it integrates with | Range | Cells | Mismatches |
|---|---|---|---|---|
| A | complex monomial moments of the uniform sphere S^(2N-1) | N = 2..16, m = 1..8, s = 0..4 | 600 | 0 |
| B | real-coordinate sphere moments after z = x + i y (separate formula and code) | N = 2..16, m = 1..5, s = 0..3 | 300 | 0 |
| C | Weingarten calculus on U(N), characters of S_d by Murnaghan-Nakayama, 1,198,080 pairs of permutations | N = 2..6, (m, s) = (1, 0), (1, 1) | 10 | 0 |
| H | the constant-term reduction on S^3 | N = 2, m = 1..8, s = 0..4 | 40 | 0 |

In all 950 cells: I(P^m) = 0, and I(Q^s P^m) = c_m binom(m-1, s-1) (2)_(4m+s) / (N)_(4m+s) with c_m = 4^m (m!)^2/(2m+1)!
(zero for s > m). No two routes disagree on a shared cell. Examples (Route A): N = 3: 4/21, 16/165, 32/525 for m = 1, 2,
3 with s = 1 (the table printed on pp. 8-9 of the paper); N = 14, m = 1: 1/2142; N = 14, m = 8:
32768/327432847566825. Every value of the s = 1 column is positive.

Identity checks: (3.2) and (3.4) hold as polynomial identities; u P = (1 + u)(1 - (1 + u)^2 tau^2) holds on a = 1 with
uv = 1 - tau^2; the expansion of P has the 16 monomials of the preflight transcription; c_m equals the integral of
(1 - s^2)^m over [0, 1] for m = 1..8.

## Controls (all behaved as the hypothesis states)

- K1: each of the 16 single-monomial removals from P gives a nonzero pure moment for some m <= 3 at N = 2 (16 of 16; the
  hypothesis asked for at least 12).
- K2: with c_m replaced by 1/(m+1) the prediction at m = 2 is 1/3 against the computed 8/15.
- K3: with (2a + u) replaced by (a + u) the pure moments at N = 2 are 1/3, -1/15, -1/5 for m = 1, 2, 3.
- K4: Routes A and B agree on 200 random monomials at N = 2, 3, 5 (600 comparisons).
- K5: Route C gives int |g11|^2 = 1/N and int |g11|^4 = 2/(N(N+1)) for N = 2..6.
- K6: on z1 = 0, Q vanishes identically.

## Deviation from the hypothesis (wording, no effect on a claim)

The hypothesis says that each of the 16 monomials of P is balanced, with "balanced" defined as (a0, a1) = (b0, b1). That
sentence is wrong as written: every monomial of P has equal total degree in z and in conj(z) (16 of 16), which is the
phase balance the paper's Lemma 5.5 uses, and only 5 of the 16 satisfy the stricter definition. The run records both
counts. The integration routes never used the sentence: they integrate every monomial and the unbalanced ones contribute
zero.

## Adversarial validation

The refutation routes were the three integration routes that do not use the paper's Hopf-coordinate proof (A, B, C),
the cross-route comparison, and the six controls, three of which perturb the object (K1, K3) or the prediction (K2) and
must fail. Route C integrates on the unitary group without passing through the sphere, which tests step 1 of the
derivation (the first column is uniform) on its range. A reviewer brief (does Route B share code with Route A; is P
built from (3.3); is any float present) was part of the delegation and its checks passed
(`grep` for float and complex literals finds none in the arithmetic).

## Verdict

CONFIRMED on the declared range: for every N from 2 to 16 and every m from 1 to 8, the finite-type functions P o Phi and
Q o Phi on SU(N) satisfy I(P^k) = 0 for k <= 8 and I(Q P^m) > 0, with the exact values of eq. (5.9) of the paper.

What this does and does not establish. The machine check is finite in m; the statement that the Mathieu conjecture fails
on SU(N) needs I(P^m) = 0 and I(Q P^m) != 0 for every m, which rests on the derivation written in the hypothesis (steps
1 to 3: the first column is uniform on the sphere; the constant-term identity on S^3; the radial transfer). That
derivation is short, uses nothing beyond the uniqueness of the invariant measure on a homogeneous space and a
one-variable integral, and is to be read by a reviewer other than its writer before the cascade paper states it. Nothing
here concerns groups other than SU(N), nor Sections 6 to 8 of the paper.

## Consequences

- The Mathieu row of the cascade paper (v0.10: false for N >= 15 and for SU(2), open for 3 <= N <= 14) is superseded:
  Long's direct construction gives a violation on SU(N) for every N >= 2, reproduced here exactly for N <= 16. The
  cascade is revised (v0.11): the row, the index map, the abstract, the discussion of the located proofs (which remain
  correct as statements about those proofs) and the next steps.
- The route through the Jacobian counterexample (a homogeneous map on C^15) stays in the paper as a second, independent
  reason for N >= 15, and the statement that the three-dimensional map alone does not reach SU(3) through the located
  proofs stays true and is no longer the status of SU(3).
- The claim for every nonabelian compact connected Lie group (Long's Theorem 1.2) is cited as his, not reproduced here.

## How could this be wrong?

- A transcription error in P shared by every route: the routes share the polynomial P by design. Guard: P is built from
  (3.3), its expansion equals the preflight's independent transcription, the paper's own table for SU(2), SU(3), SU(4)
  is reproduced, and K1 shows that every monomial matters.
- The first column is not uniform: Route C does not assume it and agrees for N = 2..6 at degree up to 5; beyond that
  range the statement is the uniqueness of the SU(N)-invariant probability measure on S^(2N-1).
- The functions are not of finite type: they are polynomials in g11, g21 and their conjugates.
- The definition of the conjecture differs from the one used: the cascade paper's Section 2 statement is the one
  compared; a variant that restricts g or f further would need a separate reading.

## Addendum 1 (2026-11-19): run times

The run was executed three times with identical cells and outcomes: 3.9 s (the implementer's run), 4.4 s (the first
rerun, quoted above) and 5.2 s (the rerun after a lint-only change of `run.py`, an inner lambda turned into a
function). The committed `artifacts/results.json` and `artifacts/run.log` are those of the last run (5,192 ms in all),
and that is the value the cascade paper quotes. The differences are machine load; no cell, control or identity
changed between runs.

