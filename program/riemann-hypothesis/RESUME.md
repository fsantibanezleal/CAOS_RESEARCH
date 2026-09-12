# Riemann hypothesis handoff

## 1. State in one screen

Opened 2026-09-12 for a source-led zero-proportion investigation. The general RH remains outside
the established result. Imported baseline: $c_0=3/2-\cot(1/\sqrt2)/\sqrt2$ and
$c(\theta)=2-\theta/2-\cot(\theta/\sqrt2)/\sqrt2$ for short intervals.
EXP-002 now derives a strict short-interval improvement; EXP-001 confirms the baseline.
The numerical example improves 0.4190750129754243337 to 0.4190768284253039967.
Lifecycle: published research record; RH remains open. Hypotheses were committed in
`266486f` before computation. The 10-page preprint v0.01 is published and byte-verified:
version DOI 10.5281/zenodo.22727389, concept DOI 10.5281/zenodo.22727388.
Release v0.64.000 is deployed and live-verified at main `08660dc`; research PR #263
and release PR #264 are merged. EXP-003 is declared, with its run pending.

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
| EXP-003-odd-frame-pressure | Can pair-disjoint triples amplify the short-interval gain, followed by a bounded pressure-certificate search? | declared; run pending |

## 4. In flight

The finite signed Hilbert operator retains the known Gram stability defect. An explicit
quantitative bound for the known three-point cosine-root obstruction, combined with
disjoint-triple counting, gives strict improvement of every positive point of Wang's curve.
Independent audits checked multiplicities, signed
off-line terms, the factor one third, the analytic interface, and the order of limits.
The numerical certificate uses theta=3/4, R=21/4 and d=1/7000, with zero unresolved boxes.
The manuscript and complete wiki are finished. Predeployment replay QA passed all 20 scenarios,
five viewports and both languages/themes, with 960 screenshots and separate visual reviews.
The full suite has 251 passing Python tests plus two frontend tests. Research PR #263 merged
at `00eace9`; release PR #264 merged to main at `08660dc`, tagged v0.64.000. Pages run
34706614866 succeeded. The [live receipt](release-0.64.000/live-verification.json) records
13 public files matching the reviewed bytes and all eight desktop/phone EN/ES light/dark
scenarios passing, with 224 screenshots and no console, page or HTTP errors.

The next [declared experiment](../../problems/number-theory/riemann-hypothesis/experiments/EXP-003-odd-frame-pressure/hypothesis.md)
tests odd-frame pressure amplification and then a separately bounded two-variable search.
Its [source preflight](../../problems/number-theory/riemann-hypothesis/context/2026-09-12-pressure-frame-prior-art.md)
credits the existing global pressure and capacity framework. No new numerical bound is
claimed at this handoff; both experimental stages await their run and verdict.

## 5. Next actions

1. Confirm the EXP-003 declaration and complete source preflight are committed before running.
2. Complete and adversarially audit Stage A using the frozen EXP-002 certificate and exact
   pair-incidence, frame-span and denominator checks.
3. Run Stage B only under its declared candidate, time and node limits; record each stage's
   outcome separately, including null or inconclusive results.
4. Transcribe validated outcomes to the operational record, wiki and any later publication
   under the usual gates. Preserve the released manuscript and its existing receipt.

Reproduction commands and source restoration: `docs/guides/riemann-replay.md`.
Rendered evidence and exact build hashes: `program/riemann-hypothesis/release-0.64.000/`.

## 6. Where everything lives

Operational files: `program/riemann-hypothesis/`. Primary record:
`problems/number-theory/riemann-hypothesis/{context,code,experiments,history,wiki}/`.
Frozen manuscript and publication receipt: `manuscripts/riemann-hypothesis/short-interval-stability/`.
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
