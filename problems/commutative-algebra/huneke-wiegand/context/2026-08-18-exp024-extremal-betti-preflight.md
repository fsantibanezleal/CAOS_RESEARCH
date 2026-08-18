# EXP-024 preflight - extremal presentation-ring homology

Date: 2026-08-18.

## Reconciled starting point

For every `p>=4`, the committed EXP-021 and EXP-023 theorems give the conductor special fiber

```text
C_p=F(T_p)=P_p/J_p,
P_p=k[X_a : a in E_(p,1)],
N=|E_(p,1)|=10p,
```

as a one-dimensional Cohen--Macaulay standard graded algebra. Its Artinian reduction by the
regular degree-one parameter `X_0` has h-vector

```text
(1,10p-1,12p,2p-1,1)
```

and socle vector `(0,0,10p,0,1)`. EXP-023 gives
`beta_(1,2)=50p^2-17p`, `beta_(1,3)=1`, and no other minimal defining equations.

The v0.12 open-question wording incorrectly includes regularity over the full presentation ring.
The Cortadellas--Zarzuela definition and the standard Hilbert/local-cohomology calculation show
that this regularity is already forced to be four. Only the unresolved interior of the Betti
table remains open.

## Source and novelty boundary

- Cortadellas--Zarzuela, *On the structure of the fiber cone of ideals with analytic spread one*,
  arXiv:math/0603042, gives the Noether-normalization module structure and identifies the
  intrinsic regularity with the regularity over the one-variable normalization. It does not give
  this family's presentation-ring Betti table.
- Abdolmaleki--Kumashiro, *Defining ideals of the fiber cone with almost minimal multiplicity*,
  arXiv:2405.18041 and IJAC 34(7) (2024), gives a general defining-ideal construction and the
  degree-five completeness bound used by EXP-023. It does not give the homological formulas below.
- A fresh primary-source search found general work on Artinian/level resolutions and graded Betti
  numbers, but no explicit computation for the EXP-009 conductor special fibers and no occurrence
  of the proposed formulas.

The novelty claim must therefore remain family-specific: exact edge data for the minimal graded
`P_p`-resolution, not a full resolution and not a new general theorem about all fiber cones.

## Ranked paths

1. **Extremal Betti data (EXP-024).** Use Cohen--Macaulayness, the exact h-polynomial, the complete
   first Betti row, and the Artinian socle to determine projective dimension, regularity, the full
   last row, one penultimate extremal entry, and the linear first-syzygy count. This is exact,
   inexpensive, and independently auditable.
2. **Explicit quadratic/Gröbner basis.** Potentially stronger, but it needs term-order control
   across `10p` variables and is not necessary for the edge theorem. Declare separately only after
   EXP-024 closes.
3. **Full minimal resolution.** The Hilbert numerator alone leaves cancellations and interior
   Betti entries undetermined. A finite table campaign can scout patterns but cannot prove the
   family theorem.
4. **Minimal primes, nilradical, and generic fiber.** Structurally interesting but presently lacks
   a sharper invariant-first target than the Betti route.
5. **Formal certificate of the EXP-023 Presburger cover.** Valuable trust reduction, but it does
   not supersede the present theorem target and remains HWB-008.

## Declared target

Put `c=N-1=10p-1` and

```text
h_p(z)=1+(10p-1)z+12pz^2+(2p-1)z^3+z^4.
```

EXP-024 tests the following exact consequences:

1. `pd_(P_p)(C_p)=c` and `reg_(P_p)(C_p)=4`.
2. The alternating Betti polynomial is `(1-z)^c h_p(z)`.
3. `beta_(2,3)=2p(500p^2-330p+31)/3`.
4. The entire last row is
   `beta_(c,c+2)=10p`, `beta_(c,c+4)=1`, and `beta_(c,j)=0` otherwise.
5. `beta_(c-1,c+3)=8p`.
6. The canonical module has `10p` minimal generators in degree `-1` and one in degree `-3`.

The proofs must explicitly separate what follows from Hilbert coefficients, what uses the already
proved first Betti row, and what uses the Artinian socle. No computation may stand in for the
regular-sequence, Auslander--Buchsbaum, Koszul-socle, or coefficient arguments.

## Experiment and audit design

- Mandatory smoke gate: `p=4`, with the linear-syzygy formula computed both from the coefficient
  of `z^3` in `(1-z)^c h_p(z)` and from the independent dimension identity
  `N beta_(1,2)+beta_(1,3)-dim(J_p)_3`.
- Bounded exact campaign: all integers `p=4,...,300`; integer arithmetic only; hashed rows and a
  resumable checkpoint. Budget: one minute.
- Independent audit: rebuild `p=4,5,17,73,151,300`, verify every campaign row hash, and reject
  perturbed regularity, projective dimension, first linear syzygy, last row, and penultimate entry.
  Budget: one minute.
- Any nonintegral formula, disagreement of the two routes, corrupted premise hash, or failed
  adversarial control makes the affected claim `INCONCLUSIVE` or `REFUTED`; it cannot be repaired
  silently.

## Manuscript strategy

If confirmed, EXP-024 directly complements the v0.12 special-fiber presentation theorem and
corrects its stale open-question wording. It should become v0.13 of the same manuscript, with a
new Zenodo version after claim/build/render QA. It does **not** justify a split manuscript.

A separate complementary manuscript should be reconsidered only if a future experiment obtains
an explicit uniform Gröbner basis, a substantial portion of the full resolution, or a primary-
decomposition theorem that can stand independently of the counterexample narrative.

