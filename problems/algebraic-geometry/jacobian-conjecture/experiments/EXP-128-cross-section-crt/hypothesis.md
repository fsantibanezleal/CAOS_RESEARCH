# EXP-128 - Cross-section CRT closure of the finite graph ledger

Declared 2026-07-31 before implementation or run.

## Question

Do the two already reconstructed exact maximal-minor sections cover each
other's retained finite divisors, thereby closing the complete rational graph
on the principal open \(AS\ne0\) without constructing another determinant?

## Premises

1. [MV] EXP-124 reduces the uncovered graph to \(F_3F_6F_7=0\).
2. [MV] EXP-125/126 use one exact section \(h_{36}\) and leave
   \(L_3=Q_9Q_{15}\) on \(F_3\) and \(L_6=Q_{18}Q_{30}\) on \(F_6\).
3. [MV] EXP-127 uses the distinct exact section \(h_7\), independent of
   \(Y\), and leaves \(L_7=E_3E_9E_{18}\) on \(F_7\).
4. [D] On a retained irreducible block, a section is nowhere zero exactly
   when its quotient class is a unit, equivalently when its norm is coprime
   to that block polynomial.
5. [H] The cross-restrictions are units on all retained blocks.

## Falsifiable predictions

1. The seven retained irreducible factors are pairwise coprime and their
   squarefree product has degree 102.
2. The norm of \(h_7\) on \(F_3\) is coprime to \(L_3\).
3. The norm of \(h_7\) on \(F_6\) is coprime to \(L_6\).
4. The norm of the graph-restricted \(h_{36}\) on \(F_7\) is coprime to
   \(L_7\).
5. Exact Bezout inverses and CRT idempotents reproduce unit identities in
   every covered quotient block.

## Method

1. Hash-verify the accepted EXP-125, EXP-126, and EXP-127 result artifacts.
2. Reconstruct \(F_3,F_6,F_7\), the retained ledger factors, \(h_{36}\), and
   \(h_7\) from the persisted artifacts.
3. Prove the combined ledger squarefree by exact pairwise gcds.
4. Compute the three cross-resultants in \(X\):
   \(\operatorname{Res}_X(F_3,h_7)\),
   \(\operatorname{Res}_X(F_6,h_7)\), and
   \(\operatorname{Res}_X(F_7,h_{36})\).
5. Compute their exact gcds with \(L_3,L_6,L_7\). For every unit gcd,
   persist a Bezout inverse modulo the ledger polynomial and verify the
   identity exactly.
6. Construct the seven CRT idempotents for the combined ledger and verify
   their sum, orthogonality, and block identities modulo the degree-102
   product.

## Interpretation

If predictions 1--5 pass, EXP-124 plus the two exact sections cover the
entire rational graph on \(AS\ne0\); the finite ledger is closed rather than
merely counted. The remaining four-parameter targets are then the finite
base locus \(V(R,S)\) and the separate boundary \(A=0\).

A nonconstant cross-gcd leaves only that exact finite block. It does not
refute the multi-minor strategy and does not justify root expansion.

No outcome closes the complete four-parameter restriction, 24-parameter
core, 51-parameter family, \((72,108)\), the planar degree floor, or JC(2).

## Controls and budget

- Characteristic zero only; no modular rank inference.
- Reconstruct all inputs from accepted artifacts and hard-coded hashes.
- Verify resultants through quotient multiplication determinants where the
  factor is quadratic in \(X\).
- Verify every inverse and CRT identity by exact remainder.
- CPU budget 120 seconds; hard stop at 180 seconds.
- Persist a deterministic artifact and reproduce its SHA-256 twice.
