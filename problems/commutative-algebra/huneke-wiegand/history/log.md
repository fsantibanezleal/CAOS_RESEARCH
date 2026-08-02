# Huneke-Wiegand extensions - history log

## 2026-08-01 - intake and declaration

- Audited the public candidate repository, manuscript, claim map and Professor Huneke's note.
- Read the primary theorem chain and positive regions; assigned discovery priority to Son Pham.
- Rejected a duplicate Python verifier as the main contribution.
- Selected an independent Singular/4ti2 colon route, endomorphism anatomy, certified SAT
  minimality and additive-family search.
- Created branch `work/huneke-wiegand/open` from current remote develop.
- Declared EXP-001 before writing or running experiment code.

## 2026-08-01 - EXP-001 confirmed

- Standard-library finite route reproduced F=181, conductor 182, genus 91, symmetry, both colon
  minima and the 49-generator intersection/product equality.
- Singular/4ti2 independently constructed a 322-generator toric standard basis of dimension one;
  both reduced ideal differences vanished.
- The hypersurface control `Gamma=<4,5>, I=(t^4,t^5)` rejected equality with explicit residues.
- Preserved two invalid instrumentation attempts: a missing helper PATH and DU's dimension-zero
  output; a third invocation had valid zero remainders but exposed Singular's zero-slot encoding.
- EXP-001 verdict CONFIRMED on P1-P6. Declared EXP-002 before its implementation or run.
- EXP-002 verdict CONFIRMED on P1-P6 by DP and Apéry routes. Computed overring Frobenius 125,
  genus 88, type 24 and new minimal generators 101 and 107. Audited Dey--Lyle Proposition
  4.1(2) and Theorems 4.2--4.4 to obtain the exact rigidity/reflexivity/Ext/Tor escape map.
- Declared EXP-003 before SAT dependency installation, implementation or execution. Kept
  calibration separate from any uniqueness, minimality or certified-UNSAT claim.
- EXP-003 verdict CONFIRMED on P1-P6. Z3 4.16.0 recovered the pinned `(181,14)` model; the
  standard-library checker verified the exact window and tail, rejected a corrupted vector, and
  produced explicit rigidity failures for every nonzero gap of the `<4,5>` control.

## 2026-08-02 - EXP-004 source-complete declaration

- Read García-Sánchez--Leamer through Example 23 and the complete future-work section. The
  published `F<69` statement cites a NumericalSgps computation but supplies no certificate suite.
- Added Blanco--Rosales Theorem 9 as an independent complete enumeration route for fixed odd
  Frobenius number, with the six-node `F=11` tree as a regression target.
- Selected proof-carrying SAT as the adversarial route: custom DIMACS, CaDiCaL DRAT output, and
  independent DRAT-trim validation.
- Fresh source/tool sweep found no published extension beyond 69 and no candidate minimality result.
- Declared EXP-004 before installing proof tools, implementation, or computation.

## 2026-08-02 - EXP-004 Route A complete and EXP-005 declared

- Directly implemented the Blanco--Rosales complete tree and independently checked every node.
- Exhausted all odd Frobenius values through 67: 48,954 symmetric semigroups and 1,503,391 gaps,
  with zero rigid ideals. The full run took 529.60 seconds.
- Started the independent 1,156-query CaDiCaL/DRAT-trim sweep; EXP-004 remains open until every
  proof passes.
- A fresh source search found no public frontier beyond 69 and no proof that the public `F=181`
  value is minimal.
- Declared EXP-005 before implementation or selector-formula computation. Its one-hot selector
  asks one existential SAT question per Frobenius value and retains proof-carrying lower bounds.
