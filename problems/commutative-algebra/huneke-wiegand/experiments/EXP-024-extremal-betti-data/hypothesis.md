# EXP-024 - extremal presentation-ring Betti data

Status: DECLARED before implementation or execution on 2026-08-18.

## Question

How much of the minimal graded resolution of the conductor special fiber is already forced by
the exact h-vector, socle, and defining equations proved in EXP-021 and EXP-023?

## Setup

For `p>=4`, write

```text
C_p=P_p/J_p,
P_p=k[X_1,...,X_N],
N=10p,
c=N-1=10p-1,
h_p(z)=1+(10p-1)z+12pz^2+(2p-1)z^3+z^4.
```

Here `C_p` is one-dimensional Cohen--Macaulay, `X_0` is a regular linear parameter, the Artinian
reduction has socle dimensions `10p` in degree two and one in degree four, and the first Betti row
is `(50p^2-17p,1,0,...)` in degrees two, three, four and above.

## Falsifiable predictions

- P1: `pd_(P_p)(C_p)=c=10p-1` and `reg_(P_p)(C_p)=4`.
- P2: the alternating graded Betti polynomial is

  ```text
  sum_(i,j) (-1)^i beta_(i,j) z^j=(1-z)^c h_p(z).
  ```

- P3: the linear first-syzygy count is

  ```text
  beta_(2,3)=2p(500p^2-330p+31)/3.
  ```

- P4: the last homological row is exactly

  ```text
  beta_(c,c+2)=10p,
  beta_(c,c+4)=1,
  beta_(c,j)=0 otherwise.
  ```

- P5: the penultimate extremal entry is `beta_(c-1,c+3)=8p`.
- P6: the canonical module has `10p` minimal generators in degree `-1` and one in degree `-3`.

## Evidence required

1. Prove P1 from Cohen--Macaulayness, Auslander--Buchsbaum, and the exact h-polynomial.
2. Prove P2 from the Hilbert series of a minimal graded `P_p`-resolution.
3. Derive P3 independently from the degree-three Hilbert-numerator coefficient and from the
   dimension of `(J_p)_3` using EXP-023's complete minimal generators.
4. Reduce modulo the regular linear parameter and identify top Koszul homology with the Artinian
   socle to prove P4; translate the last free module into P6.
5. Combine P1/P2/P4 with the `z^(c+3)` coefficient to prove P5.
6. Pass the `p=4` smoke gate, the exact `p=4,...,300` campaign, independent selected rebuilds,
   row-hash verification, premise-hash verification, and all adversarial controls.

## Verdict rule

A campaign pass without the symbolic arguments remains `[MV]`. Any disagreement between the two
P3 derivations, the socle and last-row correspondence, or the Hilbert coefficient and P5 is a
refutation of the affected prediction. `CONFIRMED` requires the complete proof and independent
audit. Interior Betti numbers not forced by these arguments remain explicitly open.

## Adversarial controls

- change regularity from four to three;
- change projective dimension by one;
- perturb `beta_(2,3)` by one;
- delete either last-row socle contribution;
- change `beta_(c-1,c+3)` from `8p` to `8p-1`;
- corrupt one imported EXP-021/023 artifact hash;
- claim the Hilbert numerator determines the entire Betti table.

## Lenses

- Artinian reduction and top Koszul homology;
- Hilbert-numerator coefficient extraction;
- first/last resolution dual viewpoints;
- canonical-module generator degrees;
- adversarial non-identifiability of the interior Betti table.

