# Riemann hypothesis handoff

## 1. State in one screen

Read [state.md](state.md), [backlog.md](backlog.md), and [plan.md](plan.md), then
the latest experiment verdicts. Evidence outranks this handoff. Public release
v0.71.000 is released and live-verified from main commit `8302be35`. EXP-007 is
confirmed locally and awaits manuscript/release integration. It retains the
spectral defect through the EXP-006 parity product and strictly improves every
positive point of the EXP-006 curve. The onset remains
`0.545884<theta_HP<0.545885`. The general Riemann hypothesis remains open.

## 2. The objects table

| Object | Role | Current evidence |
|---|---|---|
| `N,S,O,Q` | Copies, simple real support, odd real support, pair sum | EXP-006 finite proof |
| `d=r+k` | First Hilbert-subspace dimension | Lamzouri interface and EXP-006 audit |
| `c(theta)` | Wang cosine baseline | Wang source and prior experiments |
| `k3(theta)` | Explicit local odd-support curve | Confirmed EXP-005 |
| `h3(theta)` | EXP-006 quadratic simple-zero term | Exact root and target certificate |
| EXP-006 canonical result | 18,479 profiles and exact interval gates | SHA-256 `82c4761b5c97011ff86cdd379d647ad0f94643a7eb8324a4a09aa37f58848bbf` |
| `D(G)` | Simple-real Gram spectral defect | Attributed rank-trace profile and EXP-003 pressure estimate |
| `H(theta)` | EXP-007 coupled quadratic root | Strictly above `h3` wherever `h3>0` |
| EXP-007 canonical result | 652,260 spectra, 18,479 profiles, correlated exact gain | SHA-256 `7b254608198f0025e490c2c169603ae68637f60d6a685a63370bc062323b0bf3` |

## 3. Experiment index

| Experiment | Scope | Outcome |
|---|---|---|
| EXP-001 | Source constants and normalization | confirmed |
| EXP-002 | First short-interval stability theorem | confirmed and released |
| EXP-003 | Odd-frame pressure improvement | confirmed and released |
| EXP-004 | Qualitative parity range extension | confirmed and released |
| EXP-005 | Local Selberg odd-support curve | confirmed; old threshold in `(0.5459,0.546)` |
| EXP-006 | Hilbert dimension and parity compression | confirmed; new threshold in `(0.545884,0.545885)` |
| EXP-007 | Spectral-defect parity coupling | confirmed; strict full-curve gain, onset unchanged |

## 3a. Confirmed EXP-006 result

For every nonempty finite conjugation-invariant multiset in Lamzouri's kernel
setting,

$$
(Q-S)(N-O)\ge2(N-S)^2.
$$

The coefficient two is sharp. For every fixed `1/2<theta<1`, this yields the
new term

$$
h_3(\theta)=\frac{3+k_3(\theta)-
\sqrt{(1-k_3(\theta))(9-k_3(\theta)-8c(\theta))}}4.
$$

At theta=0.5459, the exact lower bound is greater than
`0.0000168381638551244569880374399`; the old linear parity term is still
negative. The [proof](../../problems/number-theory/riemann-hypothesis/experiments/EXP-006-hilbert-parity-compression/mathematical-proof.md),
[audit](../../problems/number-theory/riemann-hypothesis/experiments/EXP-006-hilbert-parity-compression/adversarial-audit.md),
[verdict](../../problems/number-theory/riemann-hypothesis/experiments/EXP-006-hilbert-parity-compression/verdict.md),
and [proof review](../../problems/number-theory/riemann-hypothesis/experiments/EXP-006-hilbert-parity-compression/proof-review.json)
state the complete boundary.

## 3b. Confirmed EXP-007 result

For the same finite multiset and the simple-real Gram matrix `G`,

$$
(Q-S-D(G))(N-O)\ge2(N-S)^2.
$$

For every fixed exponent with `h3(theta)>0`, a pressure certificate chosen at
`R=4/h3(theta)` yields a coupled root `H(theta)>h3(theta)`. At theta=0.5459,
the exact relative gain exceeds
`1.3732525985593292701164661575215e-70`. This is a structural strict
improvement and does not support another headline decimal. The
[proof](../../problems/number-theory/riemann-hypothesis/experiments/EXP-007-spectral-defect-parity/mathematical-proof.md),
[audit](../../problems/number-theory/riemann-hypothesis/experiments/EXP-007-spectral-defect-parity/adversarial-audit.md),
[verdict](../../problems/number-theory/riemann-hypothesis/experiments/EXP-007-spectral-defect-parity/verdict.md),
and [proof review](../../problems/number-theory/riemann-hypothesis/experiments/EXP-007-spectral-defect-parity/proof-review.json)
state the boundary.

## 4. In flight

1. Integrate EXP-007 into manuscript v0.07 and publish only after the complete
   render and metadata review passes.
2. Bake replay v6, promote it through the scoped PR flow, and run live QA.
3. Seek independent mathematical review of the EXP-006/007 proofs and attribution.
4. Keep other alternative routes separate until they pass declaration and
   proof gates.

Completed in this round: replay v5 is baked and tested; manuscript v0.06 is
published at DOI 10.5281/zenodo.22852479 and its 26-page PDF matches a fresh
public download byte for byte. Research PR #316, release PR #317, and promotion
PR #318 are merged. Main CI, Pages, ten live byte comparisons, and eight live
browser scenarios passed.

## 5. Next actions

1. Build and visually review manuscript v0.07 with the EXP-007 theorem,
   sensitivity boundary, and verification appendix.
2. Publish v0.07 under the existing concept DOI if every publication gate
   passes; keep v0.06 immutable.
3. Export replay v6, run repository tests and rendered browser QA, then promote
   through develop and main.
4. Pursue the next onset-changing experiment only with a statistic that remains
   informative when `S=0`.

## 6. Where everything lives

Problem: `problems/number-theory/riemann-hypothesis/`. EXP-006 and EXP-007
proofs, audits, verdicts, runners, and immutable outputs are below their
`experiments/` directories.
Replay instructions: `docs/guides/riemann-replay.md`. Release receipts belong in
`program/riemann-hypothesis/release-0.71.000/`; prior release evidence remains
immutable. Manuscript v0.06 and its archived predecessors are under
`manuscripts/riemann-hypothesis/short-interval-stability/`. Private coordination
is mirrored under `plans/caos-research/riemann-hypothesis/` in CAOS_MANAGE.

## Reproduction

From the repository root:

```text
python problems/number-theory/riemann-hypothesis/experiments/EXP-006-hilbert-parity-compression/run.py --output-dir tmp/riemann-exp006-replay --budget-seconds 120
python problems/number-theory/riemann-hypothesis/experiments/EXP-007-spectral-defect-parity/run.py --output-dir tmp/riemann-exp007-replay --budget-seconds 180
pytest tests/test_riemann_hilbert_parity.py tests/test_riemann_local_selberg.py tests/test_riemann_parity.py
python -m pytest -q tests/test_riemann_spectral_defect_parity.py
```

The runner refuses overwrite, pins predecessor and source hashes, and separates
finite arithmetic from the universal proof. CPU arithmetic is sufficient; no
GPU workload is justified.

## 7. Gotchas

`N` counts copies; `S` and `O` count support points. The pair sum uses ordinary
complex squares before conjugation symmetry makes the total real. The current
hypothesis file includes a post-run strengthening, so the original declaration
must be inspected at commit `b1febcf8a6d5830218e1df386af1e8a92c3037be`.
Test functions and support stay fixed before height limits. The rank-six value
is sensitivity only because its full profile is unavailable. A DOI, finite
census, or passing build is not external mathematical acceptance.
