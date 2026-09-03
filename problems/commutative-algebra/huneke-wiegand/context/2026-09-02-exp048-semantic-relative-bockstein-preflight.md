# EXP-048 preflight - semantic relative Bockstein coordinates

Date: 2026-09-02. Scope: HWB-074 finite-to-uniform proof gate.

## Source-complete and route check

The fresh source sweep found no theorem that turns the CAOS finite relative Smith forms into the
required parameter-compatible reduction:

- Peter Sin's survey on Smith normal forms of incidence matrices catalogs the main arithmetic and
  representation-theoretic techniques, but does not identify this interval-labelled relative
  presentation: <https://arxiv.org/abs/1401.8210>.
- Jollenbeck and Welker's algebraic discrete Morse construction requires an explicit acyclic unit
  matching; EXP-046 shows that leaf matching alone is absent here:
  <https://arxiv.org/abs/math/0501179>.
- Autry et al. establish the squarefree-divisor-complex dictionary for numerical-semigroup Betti
  numbers, but do not provide the CAOS relative filtration or connecting map:
  <https://arxiv.org/abs/1804.06632>.

The active spine remains justified: expose semantic factor-two representatives before attempting
a uniform matching. The new viewpoint is to regard the Bockstein image itself, rather than an HNF
kernel basis or a row atom, as the canonical finite object to transport in `p`.

## Cost and falsification decision

EXP-047 already fixes every relative matrix, so no HNF or Smith computation is needed. The only
potentially material cost is reconstruction of original row labels. The `p=8` smoke must emit
progress and a checkpoint before the full range is authorized. P2 and P3 are deliberately
refutable: unstable or growing normalized representatives redirect the work to dual parity
characters rather than another coefficient.

No cited source settles the experiment. No external publication action is open.
