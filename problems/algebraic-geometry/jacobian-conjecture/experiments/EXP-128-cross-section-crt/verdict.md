# EXP-128 verdict - the finite ledger is a five-block CRT scheme

## Verdict

**COMPLETE / REDIRECT.** The exact quotient-algebra computation refutes four
of the five pre-run predictions, but it compresses the remaining search much
more sharply than the predicted pairwise-disjoint ledger.

The seven retained factor appearances from EXP-125--127 contain only five
distinct squarefree projected factors. Their degrees are

\[
  9,\ 15,\ 18,\ 30,\ 3,
\]

so their union has projected degree 75, not 102. The degree-9 factor is shared
by the (F_3) and (F_7) ledgers; the degree-18 factor is shared by the
(F_6) and (F_7) ledgers. All five unique factors are pairwise coprime, and
the persisted CRT idempotents verify their exact direct-product decomposition.

## Cross-section result

The (h_7) section is not a unit on the complete (F_3) or (F_6) ledger,
but its failure is exactly concentrated on the two shared projected blocks:

- on (F_3), it covers degree 15 and leaves the shared degree-9 block;
- on (F_6), it covers degree 30 and leaves the shared degree-18 block.

The reciprocal (h_{36}) test is more degenerate: its remainder modulo the
whole (F_7) curve is zero, so it covers none of the retained degree-30
(F_7) divisor.

This changes the next computation. It is no longer rational to expand 102
algebraic values or select minors separately on all seven factor appearances.
The correct target is a simultaneous alternative maximal-minor section on the
three (F_7) CRT blocks of degrees (3,9,18). Before treating the repeated
projected factors as repeated geometric points, the next experiment must also
compare their exact (X)-classes.

## Reproducibility

Run:

```powershell
.venv\Scripts\python.exe problems\algebraic-geometry\jacobian-conjecture\experiments\EXP-128-cross-section-crt\run.py
```

Two consecutive runs produced the same canonical artifact. The accepted
artifact is `artifacts/results.json`; its SHA-256 is recorded by the run.

## Scope boundary

EXP-128 is an exact finite-scheme statement only on the (AS\ne0) rational
graph. It does not cover the surviving (F_7) divisor, (V(R,S)), (A=0),
or the full four-parameter restriction. It neither proves nor disproves the
((72,108)) case or JC(2).
