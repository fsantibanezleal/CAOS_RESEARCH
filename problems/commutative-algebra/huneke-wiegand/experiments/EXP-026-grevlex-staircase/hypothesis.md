# EXP-026 - explicit grevlex staircase

Declared: 2026-08-18, before implementation or committed artifact generation. Backlog: HWB-029.

Fix `p>=4`, put `q=24p`, and write

```text
P_p=k[X_a : a in G_p],
C_p=P_p/J_p,
X_a maps to x y^a in k[x,y]/(y^q).
```

Use graded reverse lexicographic order with `X_a>X_b` exactly when `a>b`; in particular, `X_0`
is the last variable. In a surviving bidegree `(n,s)`, write `N_(n,s)` for the unique
grevlex-smallest degree-`n` monomial of total offset `s`.

## Predictions

- P1: the standard monomials of `P_p/in(J_p)` are exactly the `N_(n,s)` with `s in E_n`; hence
  their counts are `(1,10p,22p,24p-1,24p,24p,...)`.
- P2: the minimal quadratic generators of `in(J_p)` are all noncanonical degree-two monomials.
  Their number is `50p^2-17p`; among them,

  ```text
  (77p^2-49p+2)/2
  ```

  lead binomial relations and `(23p^2+15p-2)/2` are monomial zero-relations.
- P3: the minimal cubic generators are exactly the six families in the preflight, numbering
  `5p-1`.
- P4: the minimal quartic generators are exactly

  ```text
  X_i X_p^2 X_(4p-2),  2<=i<=p-1,
  ```

  numbering `p-2`, with reduced tails `X_0^3 X_(6p+i-2)`.
- P5: there is no minimal initial generator in degree at least five. Thus the reduced Groebner
  basis has degree profile

  ```text
  (50p^2-17p, 5p-1, p-2)
  ```

  in degrees `(2,3,4)` and total size `50p^2-11p-3`.
- P6: no minimal initial generator is divisible by `X_0`; multiplication by `X_0` preserves the
  standard staircase. This gives a flat monomial degeneration with the known Hilbert series and
  an order-theoretic certificate of Cohen--Macaulayness.

## Exact campaign

- Mandatory post-implementation smoke at `p=4`.
- Main Route A: dynamic programming over `(degree,total offset)` computes canonical monomials,
  minimal boundary generators, tails, counts, and hashes at every `p=4,...,300`.
- Route A must check degrees through six even after the predicted degree-five stop.
- Independent Route B: enumerate nondecreasing offset factorizations directly for selected
  `p=4,5,6,17,73,151,300`, reconstruct the degree-two canonical pairs and the seven higher
  families without importing Route A's dynamic-programming state, then rehash every campaign row.
- The symbolic proof must derive the family list and show that its monomial complement has the
  frozen Hilbert function. Computation alone does not prove the statement for all `p`.

## Adversarial controls

The implementation must reject:

- reversing the variable order or moving `X_0` away from the last position;
- deleting one member from each of the five indexed cubic groups or the isolated cubic;
- shifting an endpoint in the quartic family;
- corrupting one tail while preserving total degree;
- accepting a tail with the wrong total offset;
- inserting an `X_0`-divisible leading generator;
- declaring a degree-five boundary element standard; and
- replacing the exact Hilbert function by only its eventual value `24p`.

## PASS, FAIL, and trust boundary

- A finite campaign PASS validates the implementation only.
- A premise-hash mismatch or budget exhaustion is `INCONCLUSIVE`, never a negative theorem.
- Any boundary, tail, count, order, or Hilbert mismatch refutes the affected prediction and stops
  the campaign.
- `CONFIRMED` requires a symbolic standard-staircase proof, mandatory smoke, full campaign,
  independent audit, frozen premise hashes, and all adversarial controls.

## Budget

CPU only, no randomness. Main campaign: 120 seconds. Independent audit: 120 seconds. Atomic
checkpoints are mandatory; a hard wrapper may stop either process at 240 seconds.

