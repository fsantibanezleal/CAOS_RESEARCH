# EXP-134 verdict - exact low-rank structure, graph identity inconclusive at gate

Status: **INCONCLUSIVE AT DECLARED EXACT GATES**.

## Exact result retained

The accepted EXP-124 section was rebuilt from the original 302-by-125
augmented matrix after adjoining direction `(2,8)`. Exact normalization at
the accepted rational anchor gives one joint cyclic block of size 33 and 86
singleton blocks.

On the 33-vertex core, the normalized transverse operator has exact rank
seven. Every singleton block has zero transverse diagonal. Consequently the
complete selected determinant has degree at most seven in `T`. This bound is
characteristic-zero and structural; it does not rely on the EXP-133 modular
controls.

## What did not complete

Five increasingly reduced routes were tested and checkpointed:

1. the ambient 33-by-33 determinant over `QQ[A,B,C,T]`;
2. graph substitution followed by a cleared determinant over `QQ[A,B,T]`;
3. the graph determinant over the exact coefficient ring `QQ(A,B)[T]`;
4. a redundant `T=0` root-certificate evaluation, stopped after recognizing
   that EXP-124 already persists the exact baseline;
5. the first new graph evaluation at `T=1` over `QQ(A,B)`.

The verdict-bearing 33-vertex computation reached the 240-second
single-block/value gate in every formulation. Attempt 005 records only the
accepted exact `T=0` baseline; it produced no `T=1` determinant. Therefore
the modular degree-zero observations of EXP-133 are not promoted to an exact
identity.

Accepted terminal checkpoint SHA-256:
`28253FE22638C15BE8F7736F0629B0A9697D55386FB46E5351DE9E58C388A351`.

## Strongest redirect

The rank-seven result changes the next exact object. Factor the transverse
core as `K_T=U V^T` over `QQ`, solve the seven right-hand sides
`H_0 W=U` on the graph quotient, and use the matrix determinant lemma

`det(H_0 + T U V^T) = det(H_0) det(I_7 + T V^T W)`.

This replaces a failed 33-by-33 determinant with a 7-by-7 transfer
determinant and makes every denominator fibre explicit. EXP-135 declares
that route.

## Strict scope

EXP-134 proves neither ambient nor graph `T`-inertness. It does not retain the
`F3*F6*F7` residual ledger as a transverse theorem, close any new graph
stratum, cover the finite base locus or transverse `d=0` quotient, or close
the five-coefficient restriction. It says nothing new about the
24-parameter core, full 51-parameter family, `(72,108)`, planar degree floor,
or JC(2).
