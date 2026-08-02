# F=181 classification preflight - 2026-08-02

## Current evidence boundary

EXP-005 proves that 181 is the least Frobenius number in the symmetric numerical-semigroup-ring,
two-generated monomial-ideal class. Its SAT witness is the public candidate at shift 14. Neither
EXP-005 nor the public candidate-verification repository classifies all pairs at `F=181`.

A fresh review of the public repository on 2026-08-02 found v0.2 verification material and later
attribution notes, but no issue, pull request or commit announcing a complete `F=181`
classification. CAOS will not import or execute its verifier as independent evidence.

## Mathematical/computational route review

Blanco and Rosales enumerate numerical semigroups with fixed Frobenius number through Kunz-style
binary coordinates and also give a complete tree. CAOS used the tree independently through small
Frobenius values, but the observed growth already made an exhaustive `F=181` tree unsuitable.
The existing direct Boolean encoding imposes the same closure and symmetry conditions without
enumerating irrelevant semigroups.

The strongest next route is projected AllSAT:

- project first to the one-hot shift variables to certify support;
- project second to the semigroup membership variables for each supported shift;
- validate every positive model semantically;
- certify exhaustion by checking the final UNSAT proof.

Blocking auxiliaries would overcount the same mathematical object, so blockers contain only the
complete mathematical projection. Blocking only positive membership literals would be unsound;
both member and gap assignments must occur in the full blocking clause.

## Tool state

- CaDiCaL 1.7.3 is available under WSL and emits DRAT proofs.
- The pinned DRAT-trim build used by EXP-004/005 remains the external proof checker.
- Z3 4.16.0 is available in the repository virtual environment for calibration only; it is not
  needed in the completeness chain.
- No GPU route is justified.

## Primary sources

- V. Blanco and J. C. Rosales, *The set of numerical semigroups of a given Frobenius number*,
  Computational and Applied Mathematics 31 (2012), DOI `10.1016/j.camwa.2011.12.034`.
- V. Blanco and J. C. Rosales, *The tree of numerical semigroups with a fixed Frobenius number*,
  arXiv `1105.2147`.
- N. Kaplan and C. O'Neill, *Numerical semigroups, polyhedra, and posets I: the group cone*,
  Combinatorial Theory 1 (2021), DOI `10.5070/C61055385`.

These sources motivate coordinate/exhaustive enumeration. The correctness of EXP-007 rests on
the committed encoding proof, exact semantic checker and accepted terminal certificates, not on
an appeal to search software.
