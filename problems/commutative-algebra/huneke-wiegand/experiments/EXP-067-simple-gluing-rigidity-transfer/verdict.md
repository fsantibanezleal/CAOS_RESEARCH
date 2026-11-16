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

## Novelty amendment (2026-10-30)

The flat-base-change assessment (HWB-094) located prior art. García-Sánchez and Leamer,
arXiv:1211.4554v1 (2012), Section 2, prove for every gluing `Gamma = a1*Gamma1 + a2*Gamma2`:
Lemma 8(8), `(a1*A + a2*C) - (a1*B + a2*D) = a1*(A - B) + a2*(C - D)`, which contains the exponent-set
transfer of P2 (take `Gamma1 = Gamma`, `Gamma2 = N`, `a1 = q`, `a2 = m`); Proposition 10,
`a1*A1 + a2*Gamma2` is Huneke-Wiegand iff `A1` is, which contains the rigidity transfer; and Theorem 13
for gluings of a symmetric semigroup with `N`. The symmetry and Apéry statements of P1 are standard
gluing facts. EXP-067 is therefore a corollary of that paper, and its results remain correct. What it
adds is the explicit two-parameter CAOS family (multiplicity `24p`, embedding dimension `11p`, every
`p >= 4` and `q` coprime to `24p`). The general statement and the case Proposition 9 leaves open are
EXP-068.

## Addendum 1

Date: 2026-11-15. Declared in `hypothesis.md` (Addendum 1) in commit `08fccb93`, before any code of the
addendum ran. The verdict stays CONFIRMED: no prediction of the experiment changed or failed.

Independent script `audit_v2.py`, artifact `artifacts/audit-v2.json` (aggregate SHA-256 of the 72 case
records `8f5df5c579a49f8311b54cb88ca5961d000fded05e6ad28d35b03f7ba197b747`, `accepted` true,
summary under key `summary`). Exit code 0 in about 42 s on CPU. The script does not import the producer as a
library: it reads only the 72 `(p, q)` pairs of `artifacts/results.json` (they equal the pairs the auditor builds
itself, key `summary.case_list_matches_producer`) and loads `run.py` to call its entry point on the
noncoprime pairs of H6(b).

| H | prediction | outcome | evidence (artifact keys) |
|---|---|---|---|
| H1 | `E^(q)` and `D^(q)` recomputed from the membership bitset of `Delta` equal `24p*N + q*E` and `24p*N + q*D` | 72 of 72 hold | `cases[].h1_e_equal`, `h1_d_equal`, `h1_tails_full`, `summary.H1 = 72`; no difference at any position (`h1_first_e_difference` and `h1_first_d_difference` are null) |
| H2 | `D^(q) = E^(q) + E^(q)` on the recomputed sets | 72 of 72 hold | `cases[].h2_rigid`, `summary.H2 = 72` |
| H3 | the rebuilt `Gamma_p` equals EXP-009's mask on every position | 9 of 9 hold (`p = 4, ..., 12`) | `base_semigroups[].mask_equal`, `positions_compared`, `summary.H3 = 9` |
| H4 | minimal generating set of `Delta` has `11p` elements | 72 of 72 hold | `cases[].h4_embedding_dimension` against `h4_expected`, `summary.H4 = 72` |
| H5 | `q*s` is a gap of `Delta` | 72 of 72 hold, recorded as a field | `cases[].h5_shift_is_gap`, `summary.H5 = 72` |
| H6(a) | `<4,5>`, `s = 1` nonrigid for `q = 1, 3, 5, 7` | 4 of 4 hold, first sumset differences at 14, 42, 70, 98 | `controls_h6a[]` |
| H6(b) | ten noncoprime pairs (the five original and `(9,2)`, `(10,5)`, `(11,11)`, `(12,3)`, `(4,6)`): generator gcd above 1, an integer above the proposed bound outside the set, producer refusal observed | 10 of 10 hold | `controls_h6b[]` (`generator_gcd`, `witness`, `witness_not_in_semigroup`, `elements_not_divisible_by_gcd`, `producer_refused`, `producer_error_type`), `producer_accepts_coprime_pair` true |
| H6(c) | the perturbed shift `q*s + 1`, data only | `q*s + 1` is a gap in 72 of 72 cases and the ideal is nonrigid in all 72 (`D` differs from `E + E`) | `cases[].h6c_perturbed`, `summary.H6c_perturbed_rigid = 0`, `summary.H6c_perturbed_gap = 72`; reported as data, no consequence drawn |

How the checks answer the two review concerns.

- Complete sets, not prefixes. The docstring of `audit_v2.py` proves that `E^(q)`, `D^(q)`, their predictions and
  `E^(q) + E^(q)` contain every integer from `2T` on, with `T = max(c, q*(cG + m))`, `c` the conductor of `Delta`
  and `cG` that of `Gamma_p`; each comparison covers every position of `[0, 2T + 2]` (at least 506 positions
  above the conductor in every case; the largest window holds 59,163 positions), and the artifact records that the
  tails inside the window are full (`h1_tails_full`). The bound is larger than the addendum's "conductor plus
  `2*q*s`" because the sumset `E + E` needs `2c`; the larger window contains the addendum's.
- A real refusal. For each noncoprime pair the producer's `case_record` was called and raised `ValueError`
  ("generators do not define a numerical semigroup"); the same entry point accepts the coprime pair
  `(4, 5)`. The set itself was tabulated: every element of `24p*N + q*Gamma_p` up to the witness is a multiple of
  the gcd (`elements_not_divisible_by_gcd = 0`) and the witness, above the bound `q*(F+m)`, is absent.

Evidential weight. P2: the auditor now recomputes the complete `E` and `D` transfer sets and the rigidity sumset
from the membership of `Delta` itself, against a prediction built from the base sets, for all 72 cases, which the
2026-09-24 review found missing; the weight of P2 rises from "Apery sets plus a rigidity sumset audit" to the
direct set equality, together with the symbolic proof. P4: the `<4,5>` control is rerun by the auditor, and the
noncoprime controls now exercise an observed rejection (the producer refuses) and a non-numerical set, so P4 no
longer rests on the `<4,5>` control alone.

How could this be wrong?

- The base semigroup is read from EXP-009's `independent_mask`; H3 rebuilds it from EXP-009's own generators, so a
  wrong generator list shared by both would pass. EXP-009 validated that family by its own audit and by the
  symmetric-semigroup checks of `hwcert`.
- The window argument depends on the tail proof in the docstring; the recorded `h1_tails_full` is an empirical
  check inside the window, not a second proof.
- H6(a) and H6(c) show nonrigidity of two small families and of `q*s + 1`; they probe sensitivity of the sumset
  test, not a theorem. The colon-to-rigidity dictionary remains imported, as the verdict states above.
- Both the producer and `audit_v2.py` share the bitset idiom and EXP-009's base; the independence is in the route
  (membership of `Delta` against a base-set prediction), not in the base data.
