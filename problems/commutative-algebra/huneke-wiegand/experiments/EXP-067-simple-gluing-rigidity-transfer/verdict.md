# EXP-067 verdict: CONFIRMED

Date: 2026-09-20.

## Result

The simple gluing `Delta=m*N+q*Gamma`, with `gcd(q,m)=1`, preserves symmetry
and transfers every finite consecutive-shift exponent set by

```text
C_r(Delta,q*s)=m*N+q*C_r(Gamma,s).
```

For `r=1,2`, this transfers the exact two-generated rigidity identity
`D=E+E`. Hence any symmetric numerical-semigroup counterexample with a
two-generated monomial ideal produces infinitely many simple-gluing
descendants.

Applied to EXP-009, this gives a two-parameter family for every `p>=4` and
every `q>=1` coprime to `24p`:

```text
multiplicity       = 24p,
embedding dimension = 11p,
Frobenius number   = q(102p-1)-24p,
ideal exponents    = 24pq and 30pq.
```

The case `q=1` recovers the previous family. The result strengthens the family
theorem without claiming another disproof of the original conjecture.

## Prediction table

| prediction | result | evidence |
|---|---|---|
| P1 Apery, Frobenius, and symmetry transfer | PASS | symbolic proof plus two exact constructions in all 72 cases |
| P2 complete `E` and `D` transfer and rigidity | PASS | simultaneous representation-alignment lemma; complete producer comparisons; independent sumset audit |
| P3 two-parameter CAOS corollary | PASS | substitution into EXP-009 and independent cases for `p=4,...,12` |
| P4 adverse controls | PASS | `<4,5>` remains nonrigid for four `q`; five noncoprime cases fail the gcd gate |

## Exact validation

- Producer: 72 of 72 cases accepted. Aggregate SHA-256:
  `4e08c7fb7799887f5c06655f8b30ef73e226eba812d96ffcf7d34ea3bb4b1742`.
- Independent auditor: 72 of 72 cases accepted and all core values agree with
  the producer. Audit aggregate SHA-256:
  `408c58763afa48fbb85027363e6a3613ca0e99d14d657ab746ea5745ef2b93b6`.
- Focused unit tests cover the direct/predicted Apery equality, the first
  nontrivial CAOS gluing, the negative control, and admissible-parameter order.
- Both implementations finish together in under 15 seconds on the recorded
  workstation, below the declared 120-second limits.

## Scope and novelty boundary

Simple gluing and Gorenstein inheritance are established constructions. The
new theorem-sized content is the simultaneous exponent-set formula and its
rigidity consequence. The primary-source search did not locate this exact
transfer result, but absence from that search does not prove worldwide novelty.
Specialist review remains required before strong priority language or journal
submission.

The theorem concerns two-generated monomial ideals over numerical semigroup
rings. It does not transfer arbitrary rigid modules, classify all gluings, or
determine the full tensor product in unrelated settings.

## How could this be wrong?

- The colon-to-rigidity dictionary is imported from the established
  two-generated Gorenstein criterion; the theorem does not reprove that ring-
  theoretic equivalence.
- A hidden sign issue cannot affect the set equality, but a mismatch between
  localization and exponent-set normalization would affect the algebraic
  interpretation. EXP-001 and EXP-009 independently validate that dictionary.
- The novelty search may have missed an equivalent transfer stated in gluing,
  ideal-class-monoid, or relative-ideal language.

## Consequence

The result meets the gate for a focused gluing-transfer manuscript. It does not
trigger a revision of the integral connecting-annihilator paper and does not by
itself authorize a Zenodo publication before claim, overlap, build, render, and
external-significance review.

## Pre-merge review (2026-09-24)

A review before promotion to `develop` checked this record against the code and
the frozen declaration. It changes no computed result, and the verdict remains
CONFIRMED.

- P2 was amended in the results commit `db5f4179`. `hypothesis.md` now keeps
  the declared text and discloses the amendment: the declared ideal is
  ill-posed for general `Gamma`, and for the CAOS family both statements
  coincide.
- Theorem item 4 in `proof.md` is now restricted to symmetric `Gamma`, which is
  what the colon-criterion argument proves. The CAOS consequence is unaffected
  because the EXP-009 base semigroups are symmetric.
- The auditor independently confirms Apery sets, Frobenius numbers, symmetry,
  the gap `q*s`, and the rigidity sumset. It does not recompute the `E` and `D`
  transfer sets or rerun the controls. The five noncoprime controls record
  `gcd(24p,q)>1` for pairs chosen with that property and exercise no rejection
  path, so the evidential weight of P4 rests on the `<4,5>` control.
- Novelty risk. Since `m in Gamma` and `gcd(q,m)=1`, `Delta` is the disjoint
  union of the translates `i*m+q*Gamma` for `0<=i<q`. Hence `k[Delta]` is free
  of rank `q` over `k[t^(q*Gamma)]`, which is isomorphic to `k[Gamma]`, with
  closed fiber `k[x]/(x^q)`. Faithfully flat base change would then transfer
  rigidity, nonprincipality, and the Gorenstein property. The novelty review
  did not consider this route. If the sketch is complete, the rigidity transfer
  is a standard consequence, and the remaining new content is the explicit
  exponent-set description and the two-parameter family.

Before the focused gluing-transfer manuscript is created, the flat-base-change
route needs a written assessment and a decision on whether the family belongs
in a focused paper or as a corollary in an existing one.
