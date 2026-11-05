# EXP-137 verdict: PARTIAL CONFIRMATION (Case 2 independently excluded; Case 1 identities verified, link partial, modular evidence)

Date: 2026-11-01. Hypothesis frozen at `d9197405`; Addendum A declared at `5eb67085` before its run.

## Result

Helali (Zenodo record 21479814, 2026-07-21) claims that both coefficient systems of GGHV Proposition 4.3
for the planar degree pair `(72,108)` are empty. Independent code (no external script executed or
imported; pickles read only through a restricted unpickler that admits builtin containers and `Fraction`)
establishes:

- **The systems are the right ones.** Helali's two Newton configurations equal our verbatim transcription
  of Proposition 4.3. Our derivation from the polygons, with `t = x y^2`, `z = y^-1` (`[t,z] = -1`,
  `x^2 = t^2 z^4`), reproduces his band equations J4 to J0 exactly for Case 2 and J4 to J2 for Case 1;
  in Case 1, J1 and J0 differ only by the cross terms of the negative bands, which his reduction carries
  into later steps. Case 1 has 302 coefficient equations, the row count of our own EXP-111 system.
- **The first elimination step.** J4 determines `D` and leaves six compatibility equations; their ideal is
  zero-dimensional of degree 35 and the eliminant `H(a7)` equals Helali's exactly. `H` is irreducible over
  `Q`, `H(a7) = G(a7^7)` with `G` an irreducible quintic, and `Q[a7^7]/(G)` is isomorphic to his field
  `Q[w]/(w^5 - w^4 + 3w^3 + 3w^2 + 26)`.
- **Case 2 is empty, independently.** Our own layered solve over `K = Q[a7]/(H)` leaves 25 residual
  equations in three parameters, and Singular `std` returns the standard basis `{1}`. Helali's four
  residual generators equal four of our 25 equations.
- **Case 1.** Our 13 compatibility equations span the same space as Helali's, layer by layer; the first is
  `kappa (s^2 - gamma)^2`, so the split `s = +c, -c` is exhaustive. All four of his serialized identities
  (Case 2 unit; Case 1 `h = 0` unit certificates on both branches; the hard identity `h = sum T_i E_i`) hold
  under our exact arithmetic over the degree-35 field. The chain from our 13 equations to his final branch
  systems (elimination of `r`, a shift in `h`, a rescaling and a descent to degree 5) was not reproduced,
  and our own Groebner run over `K` did not finish within budget.
- **Addendum A (modular evidence for Case 1).** At the five primes 1021, 1031, 1033, 1049 and 1061, where
  `H` has a simple root, our own 13 Case 1 equations specialized at both square roots of `gamma` reduce to
  the unit ideal over `F_p` (both branches, every prime); the control system of the upper layers alone
  stays non-unit (dimension 4). No external data enter this test. It is strong evidence that Case 1 has no
  solution, not a proof.

## Prediction table

| prediction | outcome |
|---|---|
| P1 band equations | PASS |
| P2 first elimination | PASS (H equal to Helali's, ratio 1) |
| P3 certificates and link | UNVERIFIED overall: identities PASS (4 of 4); Case 2 link PASS with an independent exclusion; Case 1 link partial |
| P4 controls | PASS (every corruption breaks its identity; the adverse polygon changes the system) |
| Addendum A | PASS (5 primes, both branches unit; control non-unit) |

## Consequence

Conditional on GGHV Proposition 4.3 being exhaustive, the exclusion of `(72,108)`, and hence the bound
`max deg >= 125` for a plane counterexample, now has: an independent proof of the Case 2 half; an
independent verification of every Case 1 identity with the Case 1 equations matched up to span; and
independent modular evidence for Case 1. Priority belongs to Helali. A complete independent proof of
Case 1 needs either the reproduction of his descent or a Groebner or certificate computation over `K`
that finishes; that is the next bounded item. Our planar atlas programme (EXP-052 to EXP-136) targeted
one part of the same system; it is parked.

Artifacts: `artifacts/results.json`, `artifacts/run-log.txt`, `artifacts/addendum-a.json`,
`artifacts/addendum-a-log.txt`, the Singular outputs; tests `tests/test_jacobian_exp137.py`.
