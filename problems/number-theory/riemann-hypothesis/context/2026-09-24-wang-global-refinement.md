# Wang's September 2026 global refinement and EXP-009 preflight

Date: 2026-09-24. Source: Biao Wang, *Proportions of the non-trivial zeros of
the Riemann zeta function*, arXiv:2609.24167v1, submitted 2026-09-21.

## Archived source

- Abstract: <https://arxiv.org/abs/2609.24167v1>
- PDF: `source-cache/wang-global-refinement-2609.24167v1.pdf`, 372,759 bytes,
  SHA-256 `1c3803d1a825327186ed9a0888baf8ccdbaa8f07454291b357a3af682bfe0e6a`.
- TeX bundle: `source-cache/wang-global-refinement-2609.24167v1.tar.gz`,
  12,273 bytes, SHA-256
  `e28eb09c8bb1ec5e94a5460b1d384503cbd1a375ec518d931f753060a205b987`.
- License: arXiv perpetual non-exclusive distribution license. The archive is
  retained for research verification and is not relicensed.

## What the paper proves

Wang adds the Gram spectral defect `Delta_K=tr Psi(G_K)` to Lamzouri's finite
simple/distinct inequalities. A triple-packing argument and an explicit lower
bound for the Montgomery--Taylor kernel give the unconditional global bounds

`liminf N0s(T)/N(T) >= C0 + delta0`

and

`liminf Nd(T)/N(T) >= C1 + delta0/2`,

where `delta0=6.66624...e-8`. This is a real, although very small, improvement
on the global 2026 record. The paper also states that the refined inequality
can improve Wang's earlier short-interval proportions but does not calculate
that consequence.

## Relation to the CAOS record

EXP-007, declared on 2026-09-20, had already retained the same piecewise Gram
defect through a different parity product and proved a strict short-interval
correction. Wang's preprint was submitted on 2026-09-21. This date ordering is
recorded without an absolute priority claim. Wang supplies a new explicit
three-point kernel estimate which is much stronger near the short-interval
onset than EXP-007's generic analytic root-obstruction estimate.

The paper's auxiliary ratio is bounded by `2` using three elementary upper
bounds. That step is visibly non-sharp on much of the quadrant. EXP-009 freezes
the stronger target `R<=3/2` before numerical optimization and tests its global
and short-interval consequences.

## Other updates through 2026-09-24

An arXiv API query over math.NT submissions from September 20 through 24 found
no other new paper directly improving the critical-line zero proportions or
the short-interval theorem. The remaining returned zeta papers concern root
system zeta values, Epstein/Hurwitz zeta computation, multiple zeta values, or
zeta(3) irrationality and do not change this program's analytic inputs.

## Boundary

The source is an unrefereed v1 preprint. Its theorem must be audited and
replayed before adoption. Neither its global improvement nor any EXP-009
refinement proves RH.
