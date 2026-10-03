# Literature update and dual-family preflight

Review date: 2026-10-03. This is an additive source review, not a revision of
the manifests or verdicts bound by earlier computations. Claim labels follow
methodology 05. The accompanying manifest records the locally archived PDF
and TeX bytes; third-party papers are not relicensed or committed.

## 1. Current external standing

[V, source statement] Kristian Muri Knausgard, arXiv:2609.33043v1, submitted
2026-09-27, gives an asymptotic distinct-zero bound
`16260119298029/19426831050000 = 0.83699288145242...`. These are distinct
nontrivial zeros anywhere in the strip, counted once in the numerator. This
is not a simple-critical or distinct-critical proportion. It exceeds the
global distinct-zero companion in EXP-009, for the same strip-wide count.
The published EXP-009 manuscript uses that count correctly; the current
handoff and status had mislabeled it as distinct-critical and are corrected
in this round. Earlier frozen evidence is retained.

The whole six-page paper, including the formalization exclusions and final
references, was reviewed. The mixed-multiplicity matrix inequality is an
explicit dual certificate: retain low-multiplicity real atoms, clip the
eigenvalues of their Gram matrix, and use a variational lower bound for a
convex trace function. The arithmetic and matrix lemmas have ancillary Lean
proofs. The analytic energy, operator construction, smoothing, pinching and
local interval certificate are not thereby formalized. The seven-point
certificate and its energy bound remain imported, recently unrefereed inputs.

[V, repository status] GitHub API inspection found no successor commit beyond
`1610b97b7895ff34982260f8dcaf04a0f7b82cf7` in trmdy/zeta-simple-zeros-673137
or `4c73b317232173a5e6d4253702c9870ee66c2c7b` in AxiomMath/ZetaZerosV2.
Their preserved certificates and formalization boundaries still apply.
The trmdy README lists additional candidate deductions, including the
nine-point candidate `0.673312742272...`; that is an attributed global
simple-critical claim, not a replacement for a short-window theorem.

Searches covered the supplied sources, arXiv number-theory results for
September/October 2026, simple/distinct-zero and short-interval terms,
hybrid/asymptotic large-sieve literature, and the cited upstream repositories.
No located primary source establishes a simple-critical onset below 0.534.
A negative search is not proof of worldwide novelty or completeness.

## 2. RH-038: the exact applicability gaps

[V] Conrey-Iwaniec-Soundararajan, arXiv:1808.02879v1, Theorem 1, allows
twists of length `Q^v`, `v<1`, and shifts of order `1/log Q`. Its final
proof balances `Q^(2+eps)/C + C Q^(1+v+eps)` at
`C=Q^((1-v)/2)`. At `v=1` this estimate supplies no power saving: no choice
of `C>=1` makes both terms smaller than `Q^2`. This is a limitation of the
displayed bound, not a lower bound for the actual remainder.

[V] CIS, arXiv:1105.1177v1, Theorems 1 and 2, does have a hybrid average,
but explicitly requires `(log Q)^6 <= U <= (log Q)^A` for fixed `A`.
Tang's dual range is `U=T/H=T^(1-theta)`, with moduli at most
`M=T^nu`. For fixed `theta<1` and `nu>0`, this is a positive power of the
modulus scale, larger than every fixed power of its logarithm. Thus saying
that no hybrid result exists would be too broad; the missing result is one
uniform over this polynomial-height range, at the twist endpoint, with the
appropriate shifts and arithmetic weights.

[V] Chandee-Li-Matomaki-Radziwill, arXiv:2409.01457v1, is a sixth-moment
central-value theorem. Its treatment of unbalanced sums uses automorphic
spectral theory and hyper-Kloosterman estimates. Its full introduction,
theorem and proof outline, and closing proof sections were inspected for
the needed uniformity. It does not state the shifted, twisted, polynomial-
height second-moment formula RH-038 requires. It supplies a toolkit to
investigate, not a ready theorem that can be substituted.

[V] Tang, arXiv:2608.14852v1, Theorem 1, is for distinct odd-prime twists,
without complex shifts; a formula for all composite mollifier indices is
an additional obligation. Its gamma-ratio, parity factor and `k^(-it)`
dependence cannot be discarded when the inner sum is assembled. The
schematic family in EXP-012 is a research target, not a proved reduction
for a full Mobius mollifier. In particular a bound for an unweighted,
positive square moment does not automatically evaluate this signed linear
character sum.

The direct application of the two pinned CIS theorems is therefore gated.
No conclusion that a longer mollifier is impossible follows. RH-038 remains
a research-level target requiring a proof of new uniformity and a treatment
of composite twists, rather than more numerical sampling of L-values.

## 3. Exploration through convex duality

The new paper connects Gram energy to a control-theoretic dual certificate.
For its fixed seven-point input, write
`delta=891/200000`, `p=1/2736`, `H0=3362285207/5000000000`, and for integer
`m>=7` set `a=delta(m-6)/m`, `beta=6p(m-6)/m`.
The paper selects `m=1298`, `tau=12/5`, `c=17/5`. The same assembly accepts
any parameters satisfying

```text
delta(m-6) <= tau^2,
c >= max(1+tau, 2+tau/2),
6c-7-c^2 >= a,
4c-2-c^2 >= 2a.
```

[D, declaration candidate] A rational parameter check at `m=1310`,
`tau=2411/1000`, `c=3411/1000` can retain the source's exact inputs and
increase `(1+H0-beta)/(2-a)`. An elimination of the off-line-pair residual
against the clipping requirement can bound every larger block size; this
is a finite-parameter improvement, not a new analytic zero-counting method.
EXP-013 will test and independently audit that statement before its result
is used. The local certificate is attributed; this session has not replayed
its 2,168,370 interval nodes or rebuilt the ancillary Lean development.

## 4. Exploration through phase resolution

Young's localized diagonal argument removes an off-diagonal term by making
`H |log(hm/kn)|` large. For coprime consecutive twists, the arithmetic
identity `hm-kn=1` can keep that phase bounded when the twist length times
`sqrt(T)` is comparable to, or greater than, the window length.
This is the same resolution threshold `nu=theta-1/2` seen from two sides:
Young's original variables and Tang's reciprocal family. EXP-014 will
test an exact integer collision family and prove its scale limit.

This cannot disprove a mollified moment asymptotic: individual resonant
terms can cancel after summation, and the generic collision family need
not have nonzero Mobius weights. Its value is to rule out repairing the
existing proof merely by increasing the number of integrations by parts.
The positive route must retain the signed off-diagonal sum and estimate
its cancellation with a theorem.

## 5. Strategy and publication gate

The two bounded questions use exact arithmetic, no GPU, and no large
search. The source constants and the count definitions remain explicit.
The constant tuning and a standard phase-resolution obstruction are
research records unless a substantive new theorem is proved. They do not
justify a separate manuscript or Zenodo version by themselves. Any
extension that actually lowers the short-window onset belongs in the next
short-interval-Levinson manuscript; a new hybrid moment theorem requires
its own coherent manuscript and a full analytic proof.

Sources: [Knausgard](https://arxiv.org/abs/2609.33043v1),
[CIS mean square](https://arxiv.org/abs/1808.02879v1),
[CIS critical zeros](https://arxiv.org/abs/1105.1177v1),
[Tang](https://arxiv.org/abs/2608.14852v1),
[CLMR sixth moment](https://arxiv.org/abs/2409.01457v1).

## 6. Completed round and strategic decision

EXP-013 confirms the exact gain and proves m=1310 is the largest admissible
integer block for these fixed inputs. EXP-014 proves the generic uniform
phase threshold; EXP-015 strengthens it to squarefree supported twists.
See their verdicts. The new source was not a global simple-critical record,
and no source located in this review improves the short-window onset.

After EXP-011, EXP-012 and these non-onset rounds, the methodology-13
review retains RH-F4 with a narrower positive task: derive a signed,
shifted, composite-twist reduction before attempting polynomial-height
asymptotic evaluation. The direct-CIS substitution and pointwise
integration-by-parts repairs are closed. No further parameter sweeps or
numerical L-value averages are justified without that analytic target.
The fixed-input secondary focus RH-F6 closes. No new manuscript is triggered.
