# EXP-014 duality and conductor-stability preflight

Date: 2026-08-12. Phase HW-P5. Proposed backlog items HWB-015 and HWB-016.

## Research redirect

EXP-013 proved an exact common trace/conductor ideal `T_p` and the equality

```text
length(R_p/T_p)=length(E_p/R_p)=p+1.
```

The present source audit shows that the equality of the two lengths is not a family-specific
phenomenon. It is the specialization of standard local duality for a finite birational extension
of a one-dimensional Gorenstein local ring. The exact block formula for `T_p` remains specific to
the CAOS family.

This redirects the next experiment from claiming a new balanced-defect mechanism to determining
the stability anatomy of the exact conductor.

## Primary sources and exact use

| source | load-bearing statement | local archive SHA-256 |
|---|---|---|
| J. Herzog and S. Kumashiro, *Upper bound on the colength of the trace of the canonical module in dimension one*, arXiv:2201.12508v1, Proposition 3.1 Claim 1 | For a finite birational extension `S subset R` with `S` one-dimensional Gorenstein, local duality gives `length_S(S/(S:R))=length_S(R/S)` | `4bc99c1d2054cb9eda10c25eafd94ebbac39bbbb3d27f282f0e05d45619663f9` |
| S. Dey, *Finite Birational extension with stable conductor*, arXiv:2212.09087v1, Corollary 3.7 | If `R` is one-dimensional Gorenstein and `R subset S` is finite birational, then `S` is Gorenstein if and only if `R:S` is stable | `0b02dc69d94d129e68235cdf4366775fc54f025d52fbf47dd918bd290c62a1c1` |

The PDFs were read through the relevant complete pages, including the proofs and stated hypotheses.
The source identities apply with Herzog-Kumashiro's `S=R_p`, their `R=E_p`, and Dey's
`R=R_p`, `S=E_p`.

## Premise audit

- EXP-009 proves `R_p` is a one-dimensional Gorenstein numerical semigroup domain.
- EXP-011 proves `R_p subset E_p` is a finite birational extension and computes its exact value
  semigroup.
- EXP-012 proves `type(E_p)=10p`, so `E_p` is not Gorenstein for every `p>=4`.
- EXP-013 proves `T_p=R_p:E_p` and its exact value-set blocks.

No premise depends on the new stability conclusion.

## Invariant-first derivation

Dey's Corollary 3.7 immediately predicts that `T_p` is not stable because `E_p` is not
Gorenstein. There is also a direct value-set witness. Since `0,1,p` lie in `A_p`,

```text
8s+(p+1) = (4s+1)+(4s+p) lies in T_p^2.
```

But `p+1` does not lie in `A_p`, so the same value is not in `t^(4s)T_p`. Thus
`T_p^2 != t^(4s)T_p` for every `p>=4`.

## Candidate paths ranked

1. **Conductor stability defect, selected.** It has a one-line invariant obstruction, a general
   recognition theorem, and an exact finite value-set surface for discovering a sharper formula.
2. **Natural Kunz-face maximality.** Potentially strong, but no canonical face or finite decision
   boundary has yet been fixed. It remains a classification path after the stability invariant.
3. **Global multiplicity or embedding-dimension minimum.** Important but presently unbounded at
   fixed multiplicity or embedding dimension. It needs a new finite reduction before compute.
4. **Formal proof packaging.** Valuable for trust, but it does not currently improve the
   mathematics and remains secondary to the theorem audit.

## Exploration moment

The new viewpoint is duality plus stability rather than another semigroup search. It separates
the literature-derived length balance from the family-specific conductor formula, and reads the
failure of Gorensteinness of `E_p` as a concrete failure of stability of its conductor.

## Cost gate

No SAT, Groebner basis, or long campaign is justified. EXP-014 uses exact integer value sets.
The initial campaign is capped at two minutes for `p=4,...,300`. Any exact formula suggested by
the campaign requires a separate symbolic proof before it can be confirmed for all `p`.
