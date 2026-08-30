# EXP-036 preflight - factor-two torsion localization and propagation

Date: 2026-08-30

## Decision surface

EXP-035 proves that the `(p,t)=(4,2)` incidence cokernel in offset `87` is

```text
Z^4 direct-sum Z/2Z.
```

It does not show whether the factor two persists for any larger parameter, whether it is tied to
the selected zero row, or whether it comes from a recognizable small integral subcomplex. HWB-061
therefore begins with two finite decisions before any all-parameter claim:

1. compute every declared family cell for `p=4,5,6` by exact sparse ranks, with integral Smith
   data whenever the matrix size permits;
2. reduce the known `p=4` boundary by unimodular unit cancellations and test whether the residual
   torsion support is the six-vertex projective-plane mechanism or a different incidence core.

The current work branch is `work/huneke-wiegand/open`. Its tree agrees with the promoted EXP-035
handoff. CAOS_MANAGE is current on `develop` and remains outside this round because it contains
unrelated QMine work.

## Premise reconciliation

The following records were reread before declaration:

- EXP-033 proves `0 -> K_p -> A_p -> D_p -> 0`, the regular reduction, and the minimal cubic cone.
- EXP-034 proves that the two-layer signed incidence maps compute both Betti strands of `K_p`.
- EXP-035 classifies all zero rows, supplies the family `b=10p+t`, and proves the exact
  characteristic-dependent `p=4` target and Smith factor.

The load-bearing premise hashes remain those frozen by EXP-035:

```text
EXP-032 proof    4dc37605c012b7f6a70ec5d383897c45a34e1dd5d5e4bb32a0582b7a6d651d1c
EXP-033 proof    e27cd386ad47da7ad5282e88a095d82f2b1156f76546e934b287e911da2c7b1c
EXP-034 proof    0d0a87b0a5fd4e3bbb5570e3e664eb59fcf8d07222abd62c48bdae9d20d61b4a
EXP-034 verdict  ebbf52a0b2d85b0bb5c71ca6fb48846d17b1d91644e48e69dbc3a5e8a5f81304
```

EXP-035's proof and verdict are additional premises, not extrapolations: their exact claim is only
the single `p=4` Smith factor and the all-parameter free zero-row family.

## Fresh primary-source sweep

The round rechecked the characteristic-dependence mechanism in the following primary sources:

1. Ripke and Yoon, *Characteristic Independence of Betti Numbers of Monomial Ideals in Five
   Variables*, arXiv:2607.10639v2, DOI `10.1016/j.jpaa.2026.108354`.
2. Dalili and Kummini, *Dependence of Betti Numbers on Characteristic*, arXiv:1009.4243.
3. Bolognini, Macchia, Strazzanti, and Welker, *Powers of monomial ideals with
   characteristic-dependent Betti numbers*, arXiv:2201.00571.
4. Katzman, *Characteristic-independence of Betti numbers of graph ideals*,
   arXiv:math/0408016v2.

The universal-coefficient and Hochster/lcm-lattice viewpoints identify integral torsion as the
source of characteristic dependence. Ripke--Yoon sharpen the small-support boundary: at most five
variables are torsion-free, while the six-vertex triangulation of the real projective plane gives
the sharp factor-two model. Dalili--Kummini and Katzman show how the same topology can survive in
monomial and bipartite/flag presentations. Bolognini--Macchia--Strazzanti--Welker show that torsion
mechanisms can propagate through structured monomial constructions.

None of these sources identifies the EXP-034 incidence module, its weight-collision component, or
the connecting map in the family `0 -> K_p -> A_p -> D_p -> 0`. The projective-plane comparison is
therefore a falsifiable recognition lens, not a premise or an attribution claim about this family.

## Invariant-first route

The cheapest propagation invariant is the rank defect

```text
rank_(GF(q))(delta_K) - rank_(GF(2))(delta_K)
```

for an odd prime `q`. A positive value detects even torsion without computing a full Smith form.
The connecting quotient is then decided by the block-rank identity already proved in EXP-035.
Only cells with an even-rank defect need integral localization.

For the known `p=4` matrix, unit entries permit exact row and column cancellation over `Z`.
The residual matrix, its row/column support, determinant divisors, and mod-prime ranks provide a
compact certificate. A six-essential-variable residual with the projective-plane incidence
profile would support the recognition hypothesis; any different residual refutes it.

## Tooling and budget gate

The literal `itertools.combinations` construction used for the first `p=4` target is not suitable
for `p=5`. EXP-036 must enumerate only fixed-cardinality subsets whose sums lie in the finite target
set, using exact branch bounds or dynamic programming. The mandatory smoke run is the already-known
`(4,2)` cell and must reproduce every EXP-035 basis hash and rank before a larger cell is accepted.

- implementation and `(4,2)` regression: 120 seconds;
- all family cells for `p=5`: 300 seconds;
- optional `p=6` cells after the `p=5` gate: 600 seconds;
- integral localization per positive even-rank defect: 300 seconds;
- checkpoint after every cell; stop the parameter ladder at the first budget breach.

A budget stop is `INCONCLUSIVE_BUDGET`. It is not evidence for or against propagation.

## Exploration moment

The new viewpoint is torsion recognition rather than another survival pivot. The experiment asks
whether the Smith factor is a small topological core padded by contractible/unit-matched cells.
If that recognition fails, the residual unimodular reduction still supplies a compact algebraic
torsion certificate and redirects the next round toward interval stabilization rather than
projective-plane topology.
