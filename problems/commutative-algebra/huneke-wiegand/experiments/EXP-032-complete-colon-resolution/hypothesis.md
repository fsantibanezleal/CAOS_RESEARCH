# EXP-032 hypothesis - complete cubic-colon resolution

Status at declaration: **ACTIVE, NO RESULT CLAIMED**.

## Falsifiable prediction

For every integer `p>=4` and every field, put

```text
c=2p-2,
m=8p,
lambda_(c,a)=c*binom(c,a)-binom(c,a+1)-binom(c,a-1).
```

Let `E_p=V_p semidirect omega_(V_p)` be the low canonical idealization of EXP-030 and
`D_p=P_p/(Q_p:f_p)`. Their complete graded Betti polynomials are predicted to be

```text
B_(E_p)(x,z)
  =1+sum_(a=1)^(c-1) lambda_(c,a)x^a z^(a+1)+x^c z^(c+2),

B_(D_p)(x,z)
  =(1+xz)^m B_(E_p)(x,z).
```

Equivalently, over the `2p`-variable low polynomial ring,

```text
beta_(0,0)=1,
beta_(a,a+1)=lambda_(c,a) for 1<=a<=c-1,
beta_(c,c+2)=1,
```

and every other entry vanishes. Over `P_p`, tensor these entries with the binomial Koszul ranks
`binom(m,t)` in bidegree `(t,t)`.

Any negative coefficient, failed Hilbert reconstruction, failed Gorenstein symmetry, unexpected
shift, incorrect endpoint, or disagreement with an independently reconstructed coefficient row
refutes the relevant prediction.

## Deductive route

1. EXP-030 gives a two-dimensional graded Gorenstein algebra of codimension `c`, h-vector
   `(1,c,1)`, no linear equations, and regularity two.
2. Minimality excludes `beta_(i,i)` for `i>0`; regularity excludes rows above `j-i=2`.
3. Gorenstein self-duality with final shift `c+2` sends row two to row zero. Hence its only row-two
   entry is `beta_(c,c+2)=1`, and all remaining nonzero entries lie on `j=i+1`.
4. The coefficient of `z^(a+1)` in `(1+cz+z^2)(1-z)^c` determines
   `lambda_(c,a)` with the predicted sign.
5. The `m=8p` killed high variables are a regular linear Koszul factor, multiplying the Betti
   polynomial by `(1+xz)^m`.

## Compute and budget

- CPU only; repository Python 3.13 virtualenv; exact integers; no randomness and no solver.
- Canonical and independent routes: all `p=4,...,300`, 120-second budget each.
- Exact small tables for `p=4,5,6`; full coefficient arrays and canonical hashes are required.

## Success and claim gates

1. This declaration commit predates implementation and generated artifacts.
2. Frozen premise hashes match.
3. Both exact routes agree for every declared parameter and reject all adversarial controls.
4. The written all-parameter proof derives the complete shape and every coefficient.
5. Only after all gates pass may EXP-032 be marked CONFIRMED or a manuscript v0.19 gate open.

Finite formula agreement validates the implementations; it does not replace the Gorenstein
self-duality and Hilbert-numerator proof.
