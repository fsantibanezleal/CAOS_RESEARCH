# EXP-037 preflight - connecting-parity quasipolynomial and integral reduction

Date: 2026-08-30

## Decision surface

EXP-036 computes the complete `t=2` target through `p=9`.  Put

```text
e_p=dim_GF(2) A_(p,2)-dim_GF(3) A_(p,2).
```

The exact values are

```text
e_4,...,e_9=1,4,9,18,31,49.
```

The square and an interpolating quadratic were both refuted by later exact cells.  A sequence
lookup performed only after those refutations found the same six terms in OEIS A254874, whose
listed generating function suggests the new candidate

```text
Q(x)=(1+2x+x^2+x^3)/((1-x)^2(1-x^2)(1-x^3)),
e_p=[x^(p-4)]Q(x).                                             (1)
```

Equivalently, for `n=p-4`,

```text
e_p=floor((10n^3+63n^2+126n+89)/72).                          (2)
```

This match is a heuristic only.  It forces fresh predictions `e_10=73` and `e_11=104`, and its
denominators suggest a period-six lattice decomposition.  EXP-037 tests those predictions and
asks whether exact integral cancellation produces factor-two generators indexed by the lattice
points counted by (1).

## Premise reconciliation

The load-bearing local premises are frozen by SHA-256:

```text
EXP-036 proof       8e1dc8f69dbbd1e0587f33509fc80566bbb1e72e2a991e5db9c07ab2a7d2cc02
EXP-036 verdict     d6a86209cf36c8b78fca7bdefbf33ec23872b392c3cae26db7f7611646d69cbc
EXP-036 run.py      1c6923c7c6456673402b5bdd3dada137970f6d01985690f29c960af65a981d03
EXP-036 p<=6 file   b2452d307112b0d6010483cbafbdcde13fa83a46299f6c24b4a490f7e0cdd073
EXP-036 p=7,8 file  79da3d9f03ecf5dd7dfee27a8bd69382189214254e419ba7f2facd7e3fa06f31
EXP-036 p=9 file    24be490dd4e9a17562d9731f9ec033906824e76b258d1d37afd12d37de732a29
```

EXP-033 supplies `0 -> K_p -> A_p -> D_p -> 0`. EXP-034 supplies the integral two-layer
incidence differential. EXP-035 supplies the zero-row family. EXP-036 proves that the cubic
source is absent at every declared target and that the `t=2` kernel dimensions agree in the three
tested fields for `5<=p<=9`.  No premise states that this agreement or formula (1) persists.

## Fresh source and analogy sweep

The primary-source sweep rechecked:

1. Dalili and Kummini, *Dependence of Betti Numbers on Characteristic*, arXiv:1009.4243.
2. Bolognini, Macchia, Strazzanti, and Welker, *Powers of monomial ideals with
   characteristic-dependent Betti numbers*, arXiv:2201.00571.
3. Katzman, *Characteristic-independence of Betti numbers of graph ideals*,
   arXiv:math/0408016v2.
4. Ripke and Yoon, *Characteristic Independence of Betti Numbers of Monomial Ideals in Five
   Variables*, arXiv:2607.10639v2, DOI `10.1016/j.jpaa.2026.108354`.

These sources justify the topology, universal-coefficient, discrete-Morse, and integral-torsion
lenses. None identifies the family-specific connecting quotient or formula (1). OEIS A254874 is
used only to generate a falsifiable candidate; its unrelated entry is not mathematical evidence
for this problem.

## Invariant-first and structural route

The cheapest falsifier is the exact rank difference at `(10,2)`.  The canonical bases must be
generated with the EXP-036 exact-sum semantics, while a separately implemented `GF(2)` bitset
rank and reversed sparse odd-prime rank provide independent arithmetic.

The structural route treats the full block map

```text
M=[[d_D,0],[J,delta_K]]
```

integrally. Deterministic unit cancellations first remove contractible pairs. A genuine
all-parameter proof requires a signed matching whose unmatched factor-two rows are explicitly
indexed by

```text
(r,a,b,c),  r in {0,1,2,3},  2b+3c<=n-r,
```

with weights `1,2,1,1` and `a=0,...,n-r-2b-3c`.  Finite agreement of residual sizes is not a
proof of this bijection.

## Tooling and budget gate

- formula and stored-artifact regression: 30 seconds;
- `(4,2)` and `(5,2)` sparse-reduction smoke tests: 180 seconds each;
- exact `(10,2)` target: 1,800 seconds and 24 GB private memory;
- conditional `(11,2)` target only after `(10,2)` passes: 3,600 seconds and 40 GB private memory;
- progress must be flushed after basis construction and every field rank;
- the output JSON is checkpointed after each completed stage.

The run stops at the first time or memory boundary. A stop before a completed rank is
`INCONCLUSIVE_RESOURCE_BUDGET` and contributes no mathematical evidence.

## Exploration moment

The new viewpoint is Ehrhart-style lattice counting after integral discrete-Morse reduction. It
replaces polynomial interpolation by a rational generating function with a concrete proposed
index set.  The two-sided reading is explicit: failure at `p=10` kills the candidate cheaply;
success is useful only if the unmatched integral cells can be mapped to the lattice set.

