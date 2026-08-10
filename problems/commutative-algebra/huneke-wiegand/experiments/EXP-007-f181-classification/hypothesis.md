# EXP-007 - complete classification at the minimal Frobenius value

Declared 2026-08-02 before implementation or classification computation. Phase HW-P3. Backlog
HWB-010. EXP-005 supplies the certified minimum `F=181`; this experiment asks what occupies that
minimum.

## Question and exact scope

Classify every pair `(Gamma,s)` such that:

- `Gamma` is a symmetric numerical semigroup with Frobenius number 181;
- `1 <= s <= 181` is a gap of `Gamma`;
- the normalized two-generated monomial ideal `(1,t^s)` is nonprincipal and rigid, equivalently
  the exact finite criterion `D_s = E_s + E_s` holds.

Translation and interchange of the two generators already reduce a two-generated monomial ideal
to one positive normalized shift `s`. The primary output is therefore the exact set of membership
vectors and shifts, not an unproved classification up to abstract ring isomorphism. Distinct
shifts in the same semigroup remain distinct normalized pairs unless a separate proof identifies
them.

## Certificate architecture

The computation is deliberately split into two exhaustive layers.

1. **Shift support.** Repeatedly solve the EXP-005 selector CNF. After a valid model with selected
   shift `s`, add the unit clause `not q_s`. A final UNSAT result, accompanied by a DRAT proof
   accepted by DRAT-trim, proves that the discovered list is the complete set of feasible shifts.
2. **Semigroups at each feasible shift.** Build the fixed `(181,s)` CNF. After each valid model,
   add one projected blocking clause containing the negation of its complete `h[0..181]`
   assignment. Auxiliary Tseitin assignments are not blocked. A final checked UNSAT proof proves
   that the retained membership vectors are the complete class for that shift.

Every SAT model is decoded by variable identity and independently checked with
`validate_symmetric_mask` and `analyze_rigidity`, including the proved tail. The final formulas,
proofs, solver logs, model list, hashes and checker logs are retained. CaDiCaL discovers models;
its UNSAT status is not trusted without an accepted proof.

## Independent and adversarial checks

- Regression at `F=11` must discover no feasible shift and end in checked UNSAT.
- Calibration at `F=181` must discover the public `(Gamma,14)` pair.
- Shift-support models are regenerated through the fixed-pair formula.
- A unit test proves that a projected blocker excludes exactly one membership vector while
  allowing a different vector, independent of auxiliary assignments.
- Every retained model is rechecked from the persisted membership string, without solver output.
- Deleting or flipping one literal in a calibration blocker must be detected by the blocker audit.
- Resume validates tool identities and hashes before accepting any prior checkpoint.

The Blanco--Rosales complete tree is not claimed as a second exhaustive route at `F=181`: its
measured growth makes that route disproportionate. Exact semantics plus proof-checked projected
enumeration are the declared trusted boundary.

## Committed predictions

- P1: the shift-support layer returns `s=14` and its final blocked formula is UNSAT with an
  accepted proof.
- P2: the public membership vector occurs in the fixed `s=14` class and passes the independent
  exact checker.
- P3: the public normalized pair is unique at `F=181`. This is a falsifiable scientific
  prediction, not an assumption: one additional validated vector or shift refutes it.
- P4: selector support and the union of nonempty fixed-shift classes agree exactly.
- P5: every reported completeness statement has an accepted DRAT proof and a reproducible
  manifest; a timeout, rejected proof, corrupt checkpoint or semantic mismatch yields only a
  partial lower bound.
- P6: deterministic model ordering, projected blockers and stable hashes make interruption and
  resume observationally equivalent to one uninterrupted run.

## Budgets and stop rules

1. Regression and blocker tests: five minutes total.
2. Shift-support classification at `F=181`: 1,800 seconds per solve, four hours total.
3. Fixed-shift enumeration: 1,800 seconds per solve, 10,000 models per shift and eight hours
   total. Checkpoint after every accepted model.
4. Proof checking: 1,800 seconds per terminal proof and four hours total.
5. Overall EXP-007 computation cap: sixteen hours and 16 GiB RAM. No GPU is justified.

Reaching a cap is `INCONCLUSIVE` for completeness. It is permissible to report the exact validated
models already found, but not uniqueness, a complete shift set, or a count. Heavy CNFs and proofs
live under
`E:/_Datos/caos-research/huneke-wiegand/EXP-007-f181-classification/`; Git retains deterministic
code, compact manifests, model data, audits and the verdict.

## Interpretation and publication gate

A completed enumeration can strengthen the minimum theorem to a classification theorem. If P3
passes, the public candidate is the unique normalized pair at the minimal Frobenius value in the
stated class. If P3 fails, the new pairs are retained and attributed as CAOS classification
outputs while Son Pham keeps discovery priority for the original counterexample.

Any complete result triggers a manuscript and Zenodo new-version assessment. It does not permit
silent replacement of v0.01, a general-module uniqueness claim, or a claim about all
one-dimensional Gorenstein local domains.
