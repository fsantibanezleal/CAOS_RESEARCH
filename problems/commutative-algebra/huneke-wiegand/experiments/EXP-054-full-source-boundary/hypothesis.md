# EXP-054 hypothesis: full source-boundary audit

Declared: 2026-09-04, before computation. CPU only, exact integers.

## Question and frozen predictions

EXP-053 identifies retained original column labels but multiplies only the peeled component.
Does its zero-extended labelled source actually have the claimed boundary in the original map?

- P1: at each training parameter `p=8,9,10`, direct signed multiplication of the saved original
  source chain equals twice the union of the frozen EXP-052 completion formulas on **all** rows.
- P2: the two completion source-label multisets agree and their projections onto every frozen
  component row recover the EXP-053 component identity. This is a regression, not a new theorem.
- P3: an independently encoded multiplication, with sign-corruption controls, reproduces the
  complete boundary and residual, including rows outside the component.

A P1 failure refutes only the naive source lift, not the integer cokernel calculations on the
peeled component. Record every residual coefficient and label. Do not silently replace the source.

## Premise dependencies and source-complete preflight

- EXP-036 defines the exact low-product table and degree-two offsets.
- EXP-037 defines the original combined signed differential.
- EXP-048 reconstructs retained row labels after row/column unit-leaf peeling.
- EXP-052 has confirmed finite candidate boundaries, not a generic theorem.
- EXP-053 has confirmed projected identities; its `full_boundary` variable refers only to the
  frozen EXP-042 matrix. No original-complex identity is a supported premise.

The implementations and the two latest verdicts have been read before this declaration. The
relevant external chain-lifting reference is Skoldberg, *Algebraic Morse theory and homological
perturbation theory*, https://arxiv.org/abs/1311.5803, Sections 2-3 including its final proof.
It supplies chain maps, not a CAOS-specific formula. The elementary unit-pivot lifting identity
will also be rederived directly, with no novelty claim for that standard linear algebra.

## Invariant first and one-sidedness

The distinguishing invariant is the complete residual `M z - 2(b_A+b_B)`. It can be evaluated
from a few hundred labelled source entries without enumerating the full basis or computing HNF.
PASS proves only the stated three finite identities. FAIL decisively invalidates the naive lift
and requires saved unit-pivot provenance or another explicit original chain before a uniform
source formula may be claimed. Neither outcome decides all parameters or the broad conjecture.

## Compute budget, controls, and stop condition

Budget: 60 seconds, one CPU process, 1 GiB private memory. Expected runtime is under ten seconds.
Write a checkpoint after each parameter with flushed progress. Stop on a premise hash mismatch,
independent-route disagreement, or budget exhaustion; an unfinished run is inconclusive.
No transformed HNF, full-basis enumeration, or `p=11` original-source access is authorized here.
Tests write to temporary paths. Canonical output is deterministic with no elapsed-time field.

## Exploration and publication gate

Lenses: adversarial scope audit, invariant-first residual, and chain-contraction reformulation.
If P1 fails, replace generic HNF telescoping by provenance-preserving lifting or a direct local
chain construction. Reassess manuscripts against their actual dependency lists; do not retract
unaffected published results or publish an unsupported uniform claim.
