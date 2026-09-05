# EXP-057 verdict

Date: 2026-09-04. Status: **REFUTED overall** because declared P3 has the wrong sign.
P1 is proved for every `p>=8`; P2 passes all 93 exact stress parameters `p=8,...,100`.

## Retained uniform result

The complete original-column face argument in [proof.md](proof.md) proves

$$M_pq_p=\sum_{a=1}^{p-2}(-1)^{a-1}G_p(a,2;a),$$

and

$$\eta_p=\gamma_p+M_pq_p=(-1)^p\bigl(
2G_p(p-3,2;p-3)-G_p(p-2,2;p-2)
+2G_p(p-2,1;p-3)-2G_p(p-3,1;p-4)\bigr).$$

Here `G_p(a,j;c)` has original `K` target label
`[K,(L_p minus {a,3p,3p+j}) union {6p};10p+c]`.
The representative has exactly four distinct nonzero rows, only one with odd coefficient.
Its reduction modulo two is the single row `G_p(p-2,2;p-2)`.

In the full integral cokernel,

$$[b_p^A+b_p^B]=-[\gamma_p]=-[\eta_p].$$

This is a uniform reduction of a displayed class to a bounded endpoint representative, not a
normal form of the whole quotient.

## Exact P3 refutation and corrected identity

The declared equation used `s_p-q_p`. The first `p=8` smoke computation finds exactly six
nonzero discrepancy rows and agrees between independent implementations. Symbolically, at every
`p>=8`, the discrepancy is

$$M_p(s_p-q_p)-(b_p^A+b_p^B+\eta_p)=-2M_pq_p\ne0.$$

The correct equation is

$$M_p(s_p+q_p)=b_p^A+b_p^B+\eta_p.$$

The frozen hypothesis is unchanged. The initial smoke run recorded the refutation and stopped.
A separately invoked `--continue-retained` run then validated retained P1/P2 and the corrected
plus identity; it never relabelled P3 as a pass. The canonical artifact records the exact smoke
counterexample and this continuation explicitly.

## Adversarial validation

At every `p=8,...,100`, the canonical left-to-right original differential and the separate
right-to-left differential with independently encoded degree-two gap intervals agree. They verify
the one-column boundary, its cancellation against EXP-056's `gamma_p`, the four-row formula,
the one-odd-row count, and the corrected original-source identity against the frozen EXP-052
target formulas. Every parameter rejects a flipped source-column sign and a flipped odd-row
coefficient. All calculations use exact integers, without HNF or rank calculations.

The campaign completes inside the declared 60-second budget and writes deterministic checkpoints.
The original `p=11` HNF-source labels are not read. New parameters are stress tests of the written
identity, not a newly claimed untouched source holdout. The targeted pytest suite passes 13 tests,
including both source signs at several parameters, stopped-smoke behavior, deterministic retained
continuation, invalid input rejection, and canonical artifact integrity. Ruff passes for the
experiment runner and targeted test file. Test-generated files use temporary paths only.

The canonical [results.json](artifacts/results.json) has SHA-256
`30a730d44fe67104798115adcc82c95f7dc68df5d0ebe7f2d506eef5176e88aa` and internal hash
`2be9eda350eea4ddbf21b1a84efea3abbec45254289355a96a41aec5fbf18b0a`.
The exact `p=8` counterexample vector has hash
`a913703cbc2243db2d21a26fb1fdeeab6dcef451dd1c024433d35ee38f457191`.

## How could this be wrong?

- The original coefficient-module description is an imported premise. Agreement of two
  differential implementations does not independently reconstruct that algebraic model.
- The uniform claim rests on the complete face calculation, not the 93 finite parameters.
- One odd coordinate is not a proof of nonzero quotient class. It may be killed by other
  relations, and a parity functional must annihilate all original relations to establish otherwise.
- The four-row representative does not supply an all-parameter source with boundary twice that
  vector, a second independent class, an injective comparison from a projected relative quotient,
  or an upper bound.

## Consequence

The strongest next primal/dual target is now the explicit four-row vector `eta_p`, and especially
its single odd endpoint row. Seek a uniform annihilating dual and an integral source for
`2eta_p` separately. If `M_pz_p=2(b_p^A+b_p^B)` is known, the exact transfer is
`M_p(2(s_p+q_p)-z_p)=2eta_p`; finite witnesses do not make this premise uniform.

The connecting-parity problem is not solved. This result alone does not automatically meet the
stronger manuscript split gate and does not trigger a manuscript or Zenodo version.
