# Riemann hypothesis handoff

## 1. State in one screen

Read [state.md](state.md), [backlog.md](backlog.md), and [plan.md](plan.md), then
the latest experiment verdicts. Evidence outranks this handoff. Public release
v0.71.000 is released and live-verified from main commit `8302be35`. EXP-006
improves the explicit simple-critical positivity threshold to
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

## 3. Experiment index

| Experiment | Scope | Outcome |
|---|---|---|
| EXP-001 | Source constants and normalization | confirmed |
| EXP-002 | First short-interval stability theorem | confirmed and released |
| EXP-003 | Odd-frame pressure improvement | confirmed and released |
| EXP-004 | Qualitative parity range extension | confirmed and released |
| EXP-005 | Local Selberg odd-support curve | confirmed; old threshold in `(0.5459,0.546)` |
| EXP-006 | Hilbert dimension and parity compression | confirmed; new threshold in `(0.545884,0.545885)` |

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

## 4. In flight

1. Mirror the final public state into the private coordination repository.
2. Seek independent mathematical review of the EXP-006 proof and attribution.
3. Keep alternative routes separate until they pass declaration and proof gates.

Completed in this round: replay v5 is baked and tested; manuscript v0.06 is
published at DOI 10.5281/zenodo.22852479 and its 26-page PDF matches a fresh
public download byte for byte. Research PR #316, release PR #317, and promotion
PR #318 are merged. Main CI, Pages, ten live byte comparisons, and eight live
browser scenarios passed.

## 5. Next actions

1. Mirror the final public release state into the private coordination repository.
2. Submit the manuscript for independent specialist review when a venue is chosen.
3. Start no successor experiment without a committed declaration and source audit.

## 6. Where everything lives

Problem: `problems/number-theory/riemann-hypothesis/`. EXP-006 proof, audit,
verdict, runner, and immutable outputs are below its `experiments/` directory.
Replay instructions: `docs/guides/riemann-replay.md`. Release receipts belong in
`program/riemann-hypothesis/release-0.71.000/`; prior release evidence remains
immutable. Manuscript v0.06 and its archived predecessors are under
`manuscripts/riemann-hypothesis/short-interval-stability/`. Private coordination
is mirrored under `plans/caos-research/riemann-hypothesis/` in CAOS_MANAGE.

## Reproduction

From the repository root:

```text
python problems/number-theory/riemann-hypothesis/experiments/EXP-006-hilbert-parity-compression/run.py --output-dir tmp/riemann-exp006-replay --budget-seconds 120
pytest tests/test_riemann_hilbert_parity.py tests/test_riemann_local_selberg.py tests/test_riemann_parity.py
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
