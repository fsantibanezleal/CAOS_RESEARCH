# EXP-059 verdict

Date: 2026-09-05. Status: **CONFIRMED within the declared fixed-high sector**.
P1 is proved uniformly over the integers. P2 and P3 are proved by the signed
support and face arguments, with all 861 declared finite checks passed.

## Exact uniform result

Fix any integer `p>=8`. Let `d_D` be the D boundary of all original S sources
in the current multidegree with exterior high set exactly `{6p,8p-4}`. Then

$$\ker_{\mathbb Z}(d_D)\cong\mathbb Z^{\binom{p-1}{2}}.$$

An explicit integral basis is indexed by the unit potentials `(u,r)` with
`0<=u<=p-3` and `u+2<=r<=p-1`. The alpha and beta formulas in the frozen
[hypothesis](hypothesis.md) generate every element of this kernel, uniquely.
The inverse reads the distinguished alpha coordinate at first endpoint zero,
so the result is an integral reconstruction, not a rational-rank calculation.

Each basis source has coefficient height one and at most `3p-5` terms. Its
**complete original** boundary has zero D component and at most seven K rows:
at most one C0 row and six C2 rows. The surviving faces are exactly the negative
`8p-4` faces with alpha coefficient offset 3 or beta coefficient offset
`3p,3p+1,3p+2`. Every `6p` face vanishes. The complete argument, including
exhaustion of original sources and signs, is in [proof.md](proof.md).

This settles the sector-basis question. It does not settle the connecting-parity
problem or the original Huneke-Wiegand extension programme.

## Declared predictions and evidence

| Prediction | Verdict | Basis of the conclusion |
|---|---|---|
| P1: complete integral D-kernel basis | PROVED for every `p>=8` in this sector | Exhaustion, A equations through endpoint zero, B-star reconstruction, and an integral coordinate inverse |
| P2: height one, linear source support, at most seven K rows | PROVED for every `p>=8` | Unit-potential support classification and surviving-face count |
| P3: complete signed original boundary | PROVED for every `p>=8` | Exhaustive low/high product cases and exterior signs |
| Finite adversarial campaign | PASS for all 861 declared chains | Two literal full differentials plus an independently reconstructed bitset audit |
| Uniform nonzero order-two eta class | NOT ESTABLISHED | Requires a full-image source and a separate annihilating dual |

The finite campaign checks all 525 basis chains at `p=8,...,16`, then the four
frozen potential pairs at each `p=17,...,100`, giving 336 additional checks.
Every chain passes original grading, coefficient-height, support, potential
recovery, full-boundary, and wrong-sign/coefficient-mutation checks. Observed
source support ranges from 9 to 197 and complete K-boundary support from 3 to 7;
the predicted seven-row bound is attained. These ranges describe this campaign,
not an exhaustive survey of all parameters and potentials.

The producer uses the original left-to-right differential and the independently
encoded right-to-left differential from EXP-054. The separate auditor reconstructs
the source coefficient-first, uses bitsets for the full signed differential,
and verifies all 861 producer source and boundary hashes. It additionally
crosschecks the literal EXP-054 differential on all 525 small-parameter chains.
All arithmetic is exact over the integers. No HNF, Smith form, or full matrix
elimination is used.

Flipping the entire beta sign produces a nonzero D discrepancy; changing one
source coefficient likewise produces a nonzero D discrepancy. Both controls
are independently checked for every chain. The integral coordinate minor is
also permanently tested at `p=8`. All 20 new pytest tests and the focused Ruff
check pass. Tests use temporary paths and do not overwrite canonical artifacts.

The producer and independent auditor finish within their declared 60-second and
1-GiB caps. The producer preserves deterministic parameter checkpoints and a
first-failure record on a resource or assertion stop. The original `p=11` HNF
source holdout and all old labelled HNF sources remain unread.

## Certificate identity

| File | SHA-256 |
|---|---|
| `run.py` | `9eb0f3e5d455fc0ef985641c5e307167484c3332e5eadd01c711187a1e0f6c08` |
| `artifacts/results.json` | `4f48cdb9c7acc68da88a5fdaed99a961d989d43830bec7e2cab1f08feee7aa60` |
| `audit.py` | `abce39b985651b9097d5571be157702cd5a4737506dbe52cea0ee9118865c4ed` |
| `artifacts/audit-results.json` | `9120cf1d98e60802b84a4c2d8351dae373342accda9cb517d641b8f1f4fbc0a7` |

The producer internal hash is
`83394c7a99f7d3470df54582ec5038d8b20d13c91d3006b0173d74f4acffee3a`.
The independent certificate internal hash is
`14d661bd99ef25861a2127515c474ff784c06b0836bfe2d875bec395fed82e18`.

## Consequence for research priorities

The next source search can work with explicitly generated D cycles and their
bounded connecting images, instead of extracting another large HNF section.
This is a change of proof coordinates, not a claim that the full original map
has seven rows. Two comparisons remain essential: how these K images reduce
integrally against the complete K relations, and how other exterior-high
sectors interact with the selected sector. Any such calculation needs a new
declaration and must retain all original faces.

The single-sector result gives neither a uniform `2eta` source nor a functional
annihilating every original relation with value one on eta. A second independent
class and a separate quotient upper bound are also still open.

## Manuscript and Zenodo assessment

This is a genuine all-parameter theorem, not another finite table. Nevertheless,
the current result does not yet establish the stronger manuscript split gate in
`program/huneke-wiegand/research-lines-parity-normal-form.md`:

- It does not establish all-parameter torsion in the connecting quotient.
- Its complete basis concerns one D-kernel sector. It is not a full signed
  quotient normal form or an acyclic matching with a proved finite critical
  complex.
- It does not yet force a recurrence or rational series.
- The current audit proves the specific sector formulas, but does not establish
  a comparably strong independent transfer to another module, a full homological
  invariant, or the remaining connecting quotient. The classical potential and
  signed-complement methods themselves are not claimed as new.

Accordingly, this result is a substantial candidate component of the planned
complementary manuscript, but does not by itself trigger a new manuscript or
Zenodo version on the evidence presently established. This is not a requirement
to solve the whole conjecture before publishing: a proved finite critical
complex, a rigorous cross-sector homological consequence, or a comparably strong
transfer theorem could meet the existing gate independently. Such a result must
be checked on its actual scope and novelty, without relabelling the current
sector basis as a theorem about the whole quotient.

## How could this be wrong?

- The original coefficient module is an imported premise; agreement of several
  differential implementations does not reconstruct that module independently.
- Uniform completeness depends on the source exhaustion and integral signed
  reconstruction proof, not on the 861 numerical instances.
- The auditor is independent in source parametrization and differential encoding,
  but the implementations share the declared algebraic model and frozen formulas.
- A D cycle may map to zero after further K relations. A nonzero K vector is not
  thereby a nonzero class of the full cokernel.
- Nothing here supplies an integral retraction from the full presentation onto
  this sector, so extending its scope without new chain maps would be invalid.
