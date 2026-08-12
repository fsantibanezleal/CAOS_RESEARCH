# EXP-013 verdict - exact trace/conductor theorem CONFIRMED after one correction

Run date: 2026-08-12. Exact integer, set, and bitset arithmetic; CPU only.

## Result

For every integer `p>=4`, with `R_p`, `J_p`, and `E_p=End_(R_p)(J_p)` as declared,

```text
tr_(R_p)(J_p) = R_p:E_p = tr_(R_p)(E_p) = T_p,
```

where

```text
v(T_p) = (4s+A_p)
         union (5s+(A_p union B_p))
         union (6s+B_p)
         union (8s+C_p)
         union [9s,13s-2]
         union [13s,infinity).
```

Moreover,

```text
length(R_p/T_p)=length(E_p/R_p)=p+1.
```

The common trace is therefore exactly the conductor of the finite birational extension, and its
defect is unbounded but perfectly balanced with the extension defect.

## Preserved correction

The original hypothesis wrote the final two intervals as `[9s,infinity)`. The first `p=4` smoke
run refuted that shorthand at `13s-1`, the Frobenius gap of `Gamma_p`. Before any campaign artifact
was produced, the corrected prediction retained that gap. Thus the original tail clause is
**REFUTED**; the corrected common-ideal, equality, and colength theorem is **CONFIRMED**.

## Proof and validation

The proof in `proof.md` is load-bearing. It computes `R_p:J_p` by adjacent Gamma blocks and
`R_p:E_p` from the reflected level-seven overring block. The conductor identity then gives the
trace of `E_p`.

- Two exact routes agree for all 297 parameters `p=4,...,300`.
- Campaign aggregate:
  `77448398a26b958c66818b7ac4aaa4b542bad11cdba5ec7c8f7fe76db37526e2`.
- A separate implementation rehashes every row and reconstructs
  `p=4,5,17,73,151,300`.
- Audit aggregate:
  `d55ed876d7918cb4c46d8e5f3894a508d172693bde4b4c76cb67c42fcfbf0ac1`.
- `results.json` SHA-256:
  `d2c8c67f47b76e7349685368f9ec4d4dcb483b82e252c36a65b1000c51d2ee91`.
- `audit.json` SHA-256:
  `1a84e8deb66d7fc1bc6cb07ca2efa52d4af19869f94df9ba632304fe330631e8`.
- A full rerun reproduces `results.json` byte for byte.
- Deleted, injected, and altered-overring controls are rejected.

The first unoptimized full attempt exceeded its execution envelope without writing an artifact.
Restricting the colon intersection to `Lambda_p minus Gamma_p` is mathematically exact and brought
the completed campaign below ten seconds, within the declared two-minute budget.

## Interpretation and scope

Lindo-Maitra-Zhang Corollary 5.6 explains why trace equality itself is expected over the
one-dimensional Gorenstein base. The new content is the exact common conductor formula and its
balanced colength. This does not create a new counterexample or solve arbitrary surviving
Huneke-Wiegand variants.

The combination of EXP-012 and EXP-013 is substantial enough for a deliberate manuscript v0.05
candidate. Publication still requires the repository's claim, build, render, metadata, and public
download gates; it is not implied by this verdict alone.

## How could this be wrong?

The ring-theoretic step uses the standard value-set product for monomial fractional ideals and the
fact that the conductor is an `E_p`-ideal. The finite campaign is not the all-parameter proof. The
theorem has not been journal peer reviewed or formalized in a proof assistant.
