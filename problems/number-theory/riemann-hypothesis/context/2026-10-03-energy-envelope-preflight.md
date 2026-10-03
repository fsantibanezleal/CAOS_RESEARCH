# Full-energy clipping preflight and strategy review

Second source refresh on 2026-10-03. Knausgard arXiv:2609.33043 remains
v1 (September 27), Lamzouri 2609.02882 remains v2 (September 8), and
Wang 2609.07918 remains v1. Upstream HEADs independently fetched:
trmdy/zeta-simple-zeros-673137 1610b97b7895ff34982260f8dcaf04a0f7b82cf7;
AxiomMath/ZetaZerosV2 4c73b317232173a5e6d4253702c9870ee66c2c7b.
Existing source manifests and external payloads remain unchanged.

Primary sources: https://arxiv.org/html/2609.33043v1,
https://arxiv.org/abs/2609.02882, https://arxiv.org/abs/2609.07918,
https://github.com/trmdy/zeta-simple-zeros-673137,
https://github.com/AxiomMath/ZetaZerosV2. The complete six-page mixed-Gram
paper was read in the preceding round; its block, threshold and counting
arguments were re-read for this extension. No new accepted RH proof or
source with a stronger short-window onset was located. Negative searches
do not establish novelty. A search also surfaced Oukil's October 1 working
paper (10.33774/coe-2026-jmb68-v11); it is an unreviewed lead, not an input
or an adopted RH claim. No full-text evaluation of that lead is claimed.

## Question independent of the parameter search

For a real zero-sum vector of length m with energy E, determine the sharp
minimum of its one-sided quadratic clipping sum. The candidate envelope is
F(E)=E below tau^2*m/(m-1), and
F(E)=E/m+2*tau*sqrt((m-1)*E/m)-tau^2 above it. The equality spectrum
has one positive displacement and equal negative complementary entries.
For E<=m*(m-1) it is realizable by a PSD unit-diagonal matrix.

The proposed argument bounds the positive energy by (m-1)*E/m and the
largest displacement by its square root. This is a classical variance
mechanism, extending EXP-016's threshold evaluation to every energy.
The robust-optimization lens asks whether F is increasing and 1-Lipschitz:
if so, E+p*W>=D implies clipped_energy+p*W>=F(D). That would remove the
hard all-or-nothing block condition without adding analytic premises.

## Admission and value decision before computation

RH-F4 remains the sole active focus. A single bounded secondary RH-F8 is
admitted for the uniform envelope and pressure transfer, not for an
unbounded parameter sweep. The structural result is the value target;
a tiny numerical consequence alone does not meet the onset success gate.
Stop after the proof, adversarial controls and one feasible exact gain,
or immediately on a failed premise. No claim of global parameter optimality
is planned. No GPU is needed. If this is only elementary supporting
material, keep it as a research record. A genuinely distinct method with
novelty supported by the literature would require a focused manuscript;
the fixed-input consequence cannot be spliced into either short-interval
paper as though it improved their onset.

## Alternative directions retained

The spectral/convexity lens handles energy loss; it cannot supply the signed
short-window cancellation required by RH-038. Analytic continuation of the
existing project still requires the complete shifted composite-twist
reduction, with oscillatory and gamma factors retained. Further fixed-input
constant polishing is not admitted after this uniform envelope experiment.

## Post-computation prior-art reconciliation

The pinned upstream refined-deduction.md and the original tawanerguo
trace_energy_envelope.md were subsequently read in full. They contain the
same tau=1 formula and pressure transfer. Arbitrary tau follows by scaling,
so no novel formula is claimed. The independent proof here handles every
energy and multiple clipped entries uniformly. The exact numerical gain
is small; this closes the supporting route without a new manuscript.
The upstream nine-point packet, on the same window, offers a materially
larger local input and is a separate prospective transfer experiment.
