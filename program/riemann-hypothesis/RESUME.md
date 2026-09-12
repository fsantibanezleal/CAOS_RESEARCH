# Riemann hypothesis handoff

## 1. State in one screen

Opened 2026-09-12 for a source-led zero-proportion investigation. The general RH remains outside
the established result. Imported baseline: $c_0=3/2-\cot(1/\sqrt2)/\sqrt2$ and
$c(\theta)=2-\theta/2-\cot(\theta/\sqrt2)/\sqrt2$ for short intervals.
EXP-002 now derives a strict short-interval improvement; EXP-001 confirms the baseline.
The numerical example improves 0.4190750129754243337 to 0.4190768284253039967.
Lifecycle: consolidating. Hypotheses were committed in `266486f` before computation.

## 2. The objects table

| Object | Definition | Owner |
|---|---|---|
| $N(T,H)$ | Nontrivial zeros in $(T,T+H]$, counted with multiplicity | Wang source |
| $S(T,H)$ | Simple zeros on the critical line in that interval | Wang source |
| $Q$ | Squared Hilbert-Schmidt norm of the finite zero operator | Lamzouri source |
| $\Psi(t)$ | $(t-1)^2$ for $0\le t\le2$, $2t-3$ for $t\ge2$ | ainta stability source |
| $k_\lambda$ | Normalized Fourier transform of a compact cosine profile | EXP-002 |

## 3. Experiment index

| Experiment | Question | Status |
|---|---|---|
| EXP-001-source-and-constant-audit | Do independent exact/certified checks reproduce the imported constants and normalization? | confirmed |
| EXP-002-short-interval-stability | Does the finite stability defect give a strict improvement to Wang's bound? | confirmed |

## 4. In flight

The finite signed Hilbert operator retains the known Gram stability defect. An explicit
quantitative bound for the known three-point cosine-root obstruction, combined with
disjoint-triple counting, gives strict improvement of every positive point of Wang's curve.
Independent audits checked multiplicities, signed
off-line terms, the factor one third, the analytic interface, and the order of limits.
The numerical certificate uses theta=3/4, R=21/4 and d=1/7000, with zero unresolved boxes.
The manuscript and public replay are being completed from these persisted proofs.

## 5. Next actions

1. Complete wiki transcription and manuscript PDF review.
2. Publish the frozen validated preprint on Zenodo and verify public bytes and metadata.
3. Validate the bilingual public replay in both themes and all six sections.
4. Promote scoped PRs, serialize the release bake/version/tag, and verify live deployment.

## 6. Where everything lives

Operational files: `program/riemann-hypothesis/`. Primary record:
`problems/number-theory/riemann-hypothesis/{context,code,experiments,history,wiki}/`.
Manuscripts, when triggered: `manuscripts/riemann-hypothesis/`.
Management mirror: `plans/caos-research/riemann-hypothesis/` in the private management repo.

## 7. Gotchas

Do not confuse simple, critical-line, simple-critical, distinct, or simple-or-critical counts.
Keep asymptotic liminf theorems distinct from finite-height verification. AxiomMath's zeta
theorems take two explicit classical analytic assumptions. Its default CI library build is
not a comparator replay. Lamzouri's arXiv license is nonexclusive, not a CC redistribution
license; preserve local copies and public provenance without silently relicensing them.

## Lenses tried

| Lens | Outcome |
|---|---|
| Exclusion and anatomy | Pure kernel optimization and aggregate rank optimization reproduce known barriers |
| Reformulation | Short-interval transfer of the stability defect selected for an adversarial proof attempt |
| Invariant | Simultaneous kernel zeros at two gaps and their sum are algebraically impossible, with an explicit positive bound |
| External dialogue | Original proof, simplification, formal sources, and later candidates compared |
