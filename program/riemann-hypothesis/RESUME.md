# Riemann hypothesis handoff

## 1. State in one screen

Opened 2026-09-12 for a source-led zero-proportion investigation. The general RH remains outside
the established result. Imported baseline: $c_0=3/2-\cot(1/\sqrt2)/\sqrt2$ and
$c(\theta)=2-\theta/2-\cot(\theta/\sqrt2)/\sqrt2$ for short intervals.
No CAOS improvement is established yet. Hypotheses precede all experimental runs.

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
| EXP-001-source-and-constant-audit | Do independent exact/certified checks reproduce the imported constants and normalization? | declared |
| EXP-002-short-interval-stability | Does the finite stability defect give a strict improvement to Wang's bound? | declared |

## 4. In flight

The proposed route retains $\operatorname{tr}\Psi(G)$ for the Gram matrix of simple real
atoms instead of discarding it. A three-point kernel-energy bound, compactness, and interval
length counting may force a positive defect. The counting factor, bandwidth limit, and
analytic transfer must all survive independent review before a positive verdict.

## 5. Next actions

1. Finish context dossiers and source checks; keep unverified candidates quarantined.
2. Execute declared source and finite-kernel certificate runners once their code is reviewed.
3. Reconcile independent mathematical audits and write exact verdicts.
4. Transcribe validated results, run scoped tests and repository guards, then promote.

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
| Invariant | Simultaneous kernel zeros at two gaps and their sum appear algebraically impossible |
| External dialogue | Original proof, simplification, formal sources, and later candidates compared |
