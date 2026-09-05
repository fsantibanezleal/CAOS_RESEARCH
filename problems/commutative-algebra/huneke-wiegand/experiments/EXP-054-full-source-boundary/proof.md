# Full-map scope and the missing pivot coordinate

Let `M` denote the full EXP-037 combined integer map, `M_C` the frozen isolated matrix after
unit-leaf cancellation, `j` literal source-coordinate inclusion, and `P_C` row projection.
EXP-053 proves `P_C M j(z)=M_C z` and its relative mask-58 identity. It does not compute `M j(z)`.

## Exact finite finding [MV]

For `p=8,9,10`, direct original-label multiplication gives

$$M_pj(z_p)=2(b_p^A+b_p^B)+2(-1)^p e_p,$$

where

$$L_p=[1,p]\cup[3p,4p-2],\qquad
e_p=[K,L_p\setminus\{2,3p\};13p].$$

The residual supports are one in all three cases, with coefficients `2,-2,2`. The source
remains a mod-two cycle. The full-map identity without this extra term is false; the projected
identities and finite relative torsion classifications are unchanged.

## Why the distinction matters [D]

For a unit leaf pivot, after ordering the row and column first, write

$$M=\begin{pmatrix}\epsilon&a\\b&C\end{pmatrix},\qquad \epsilon=\pm1.$$

A row leaf has `a=0`; a column leaf has `b=0`. The Schur complement is `C` in either case.
Thus deleting the pivot preserves the remaining matrix and gives an integral equivalence
`M ~ [epsilon] direct-sum C`. Zero rows add free cokernel summands. This justifies the torsion
calculations on the peeled component.

But a reduced source `z` lifts as `(0,z)` only for a row leaf. For a column leaf it lifts as
`(-epsilon^{-1}a z,z)`. Direct multiplication gives `(0,Cz)`. Reverse composition of the
ordered pivot lifts recovers a full source identity; retained column labels alone omit these
coordinates. This is standard elimination, not a novel Morse-theory claim. The general
chain-map formulation appears in Skoldberg, Sections 2-3,
https://arxiv.org/html/1311.5803v1.

## Audit and limits

The independent checker uses explicit degree-two gap intervals and a reverse traversal of the
exterior signs. Its 213 checks compare the complete labelled boundary, all 15,405 retained
component rows, source gradings, residuals, common-source equality, and deliberate sign corruption.
The correction is constructed separately in EXP-055. No `p=11` source label was accessed, and
no generic formula for the HNF-derived source is asserted.
