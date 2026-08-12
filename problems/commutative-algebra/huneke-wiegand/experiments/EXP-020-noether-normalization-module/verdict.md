# EXP-020 - verdict

Status: **CONFIRMED** on 2026-08-12.

## Theorem

For every integer `p>=4`, let `G_p=gr_(T_p)(R_p)` and let
`F_p=k[x_p]`, where `x_p=(t^(4s))^*` is induced by the EXP-017 minimal reduction. Then

```text
G_p isomorphic to
  (F_p/(x_p))^p
  direct-sum F_p
  direct-sum F_p(-1)^(10p-1)
  direct-sum F_p(-2)^(12p)
  direct-sum F_p(-3)^(2p-1)
  direct-sum F_p(-4).
```

Its only nonzero graded Betti numbers over `F_p` are

```text
beta_(0,0)=p+1, beta_(0,1)=10p-1, beta_(0,2)=12p,
beta_(0,3)=2p-1, beta_(0,4)=1, beta_(1,1)=p.
```

Consequently

```text
pd_(F_p)(G_p)=1,
reg_(F_p)(G_p)=4,
a(G_p)=3,
length(G_p/x_pG_p)=25p=e0(T_p)+I(G_p).
```

Thus the complete failure of Cohen--Macaulayness is isolated in `p` exponent-one cyclic summands,
while the quotient is a rank-`24p` graded free module over the Noether normalization.

## Exact evidence

- Mandatory `p=4` smoke gate: PASS before campaign artifact creation.
- Complete two-route campaign: `p=4,...,300`, 297 rows, PASS in 12.234088 seconds.
- Campaign aggregate:
  `02cf6f62a71de1a897cd46149e8c89d1c55bf810d28dddc02fc6c5330b9c1aed`.
- Independent reconstructions: `p=4,5,17,73,151,300`, PASS.
- All 297 campaign rows independently rehashed.
- Independent audit aggregate:
  `c439f7e4fbd3cee983f32e5c6a27b347017c165cdf6d9fee54eb8d53ab634eac`.
- `results.json` SHA-256:
  `4c9dfbfe8f2cee53432e199476e69f89dd90a86d3160e81a76088723f53a3cd6`.
- `audit.json` SHA-256:
  `56b7bc8c690ddb40b83821798b43c7441b068982e968b7ff08e1b1ff4b7f74e9`.
- `ruff` and Python byte-compilation checks: PASS.

## Adversarial controls

The campaign and audit reject an exponent-two torsion summand, deletion of one degree-one free
summand, the false first Betti number `p-1`, regularity three, and parameter-section length
`25p-1`.

## How could this be wrong?

The theorem depends on the already confirmed EXP-017 minimal reduction and power profiles,
EXP-018 Hilbert series, and EXP-019 complete torsion calculation. An error in one of those symbolic
premises could propagate here despite finite agreement. The independent Apery-column route checks
their combined consequences but does not replace their infinite-family proofs. The notation
`a(G_p)=3` denotes the top-local-cohomology invariant `end H^1(G_p)`, not a claim that `G_p` is
Cohen--Macaulay.

## Scope and consequence

This is a complete graded-module theorem for the conductor tangent cones in the explicit EXP-009
family. It does not classify arbitrary tangent cones or arbitrary Buchsbaum filtrations. It is a
material structural extension beyond manuscript v0.09 and triggers the v0.10 manuscript gate.
