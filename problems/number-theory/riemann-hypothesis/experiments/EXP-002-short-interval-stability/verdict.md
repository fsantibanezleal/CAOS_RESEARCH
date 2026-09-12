# EXP-002 verdict: confirmed short-interval stability refinement

Date: 2026-09-12. Verdict: **confirmed**, within the theorem scope below.
Declaration committed before computation: `266486f`.

## Result and scope

[D] For every fixed $\theta_0<\theta<1$, where $\theta_0$ is the unique root of
$c(\theta)=2-\theta/2-\cot(\theta/\sqrt2)/\sqrt2$, there is an explicit
$c_*(\theta)>c(\theta)$ such that the lower asymptotic simple-critical proportion in
$(T,T+T^\theta]$ is at least $c_*(\theta)$. The distinct-zero proportion is at least
$(1+c_*(\theta))/2$. The complete proof and explicit positive formula are in
`mathematical-proof.md`; the independent refutation attempt is `adversarial-audit.md`.

This is a refinement of Wang's short-interval cosine bounds using the known stability
inequality from ainta's manuscript, transferred directly to Lamzouri's finite Hilbert operator.
The stable rank-trace lemma, pair-correlation theorem, and cosine optimum are attributed prior
work. The transfer, explicit three-point obstruction bound, and entire positive-curve
refinement are the candidate contribution. Searches of the directly relevant primary papers
and successor repositories found no matching short-interval theorem; this is not a guarantee
of priority or independent acceptance.

## Certified example

[MV] With $\theta=3/4$, $R=21/4$, and $d=1/7000$, exhaustive interval arithmetic proves

$$2\{k_{3/4}(u)^2+k_{3/4}(v)^2+k_{3/4}(u+v)^2\}\ge1/7000$$

for every $u,v\ge0$ with $u+v\le21/4$. The resulting simple-critical bound is

$$c_* = \frac{3c(3/4)-2/(7000R)}{3-1/7000}
       =0.4190768284253039967366657875\ldots,$$

compared with $c(3/4)=0.4190750129754243337345536107\ldots$. The gain in proportion is
$0.0000018154498796630021121768\ldots$. The distinction between proportions and percentage
points is retained. This example does not establish a global record above the known or later
candidate global bounds.

## Arithmetic and validation

- `artifacts/triangle-certificate.json` encodes a complete binary subdivision of the square
  containing the triangle. It has 48,761 nodes, 24,252 accepted energy leaves, 129 leaves
  certified outside the triangle, and zero unresolved boxes.
- Discovery certificate: Arb through `python-flint==0.9.0`, 160-bit precision, exact rational
  boxes and threshold. The derivative bound $|k'|\le\pi\theta$ controls each entire cell.
- Arithmetic cross-check: every accepted leaf was replayed at 256 bits with an independently
  derived sinc Taylor formula and rigorous remainder. This shares the partition reconstruction,
  Lipschitz bound, and Arb arithmetic library with the first route; it is an independent
  evaluator, not an independently implemented full verifier or a Lean proof.
- The general theorem also has a conservative explicit analytic gap, requiring no numerical
  minimization. The finite spectral proof, complex conjugation, signed off-line contributions,
  multiplicities, three-offset counting factor, smoothing, and order of limits were checked
  independently. The full certified $d$ is justified by the final $\delta\uparrow d$ limit
  in Section 7 of the proof.
- A ten-node smoke run stopped deliberately with a resumable exact checkpoint. Its resumed
  $R=6,d=10^{-5}$ run completed with 8,365 nodes. The final stronger run completed inside its
  ten-minute and two-million-node budget. CPU only; GPU was unnecessary.

## Reproduction

Install the problem's pinned requirements into the repository virtual environment, then run

```text
python problems/number-theory/riemann-hypothesis/experiments/EXP-002-short-interval-stability/run.py --output-dir tmp/riemann-replay --radius 21/4 --threshold 1/7000
pytest tests/test_riemann_certificates.py
```

The runner writes to an explicit output directory. Test and replay outputs must not overwrite
the committed canonical artifacts. `explore.py` records a deterministic floating grid used
only to select the compact radius; its sampled values do not certify any lower bound.

## Exploration and rejected directions

Kernel-only optimization was already solved by Montgomery-Taylor and the inspected successor
sources. Aggregate multiplicity-defect inequalities were already implied by Anthropic's
arbitrary-parameter rank-trace lemma and appeared in a separate low-multiplicity repository.
Those routes were excluded from novelty claims. The selected new viewpoint retains the
simple-atom Gram defect in the exact finite operator, avoiding an unnecessary Gabor-tail
transfer when applying the method to short intervals.

## How could this be wrong?

The analytic conclusion depends on the cited classical inputs and Wang's inspected preprint
theorem. It is not an end-to-end formalization. The independent analytical reviews could share
an overlooked mathematical error; the numerical evaluators share Arb and geometric logic.
The current source search can miss earlier or concurrent work. No effective height threshold,
uniformity as $\theta\downarrow\theta_0$, improved positivity exponent, global-record claim,
or solution of RH follows. Publication must state these limits and preserve source attribution.
