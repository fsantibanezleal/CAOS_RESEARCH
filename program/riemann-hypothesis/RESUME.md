# Riemann hypothesis handoff

## 1. State in one screen

Read [state.md](state.md), [backlog.md](backlog.md), [plan.md](plan.md), then the
latest source verdicts. Evidence outranks this handoff. Public release v0.65.000
is released and live-verified; v0.02 is published at DOI 10.5281/zenodo.22728744
and the four-record replay is integrated. The release commit
`24a2cb250e44fa59c9f6a56c86eefdf009258e70` (tag `v0.65.000`), CI and Pages runs,
and the live receipt are recorded below; the general RH remains open.

## 2. The objects table

| Object | Role | Current evidence |
|---|---|---|
| $N,s,r,b,E$ | Multiplicity and support counts in a finite zero multiset | EXP-002/003/004 proofs |
| $Q,D,\sigma$ | Hilbert--Schmidt moment, simple Gram defect and residual slack | EXP-002/004 exact identities |
| $c(\theta)$ | Wang cosine baseline and its positive root $\theta_0$ | Wang source and EXP-004 comparison |
| EXP-002 certificate | Three-point compact energy certificate | Published v0.01 archive |
| EXP-003 pressure certificate | Odd-frame pressure improvement at $\theta=3/4$ | Confirmed 16,797-node replay |
| EXP-004 parity transfer | Qualitative fixed-exponent range extension | Confirmed exact run and proof review |
| EXP-005 local Selberg transfer | Candidate explicit odd-density curve and theta=0.546 simplicity consequence | Declared; canonical certificate and proof review pending |
| Alternative route dossiers | Spectral, Nyman--Beurling, Li/Weil, heat-flow and mollifier options | Source-reviewed proposals with open gates |

## 3. Experiment index

| Experiment | Scope | Outcome |
|---|---|---|
| EXP-001 | Source constants and normalization | confirmed |
| EXP-002 | First short-interval stability theorem and compact certificate | confirmed and released |
| EXP-003 A | Odd-frame amplification with the prior certificate | confirmed |
| EXP-003 B | New pressure inequality and more than 25% gain over A | confirmed |
| EXP-004 | Parity density transfer below the cosine positivity threshold | confirmed; proof review and exact arithmetic committed in fbc4f9f |
| EXP-005 | Localize Pearce-Crump's optimized sign detector and combine it with EXP-004 | declared 2026-09-19; unexecuted |

The [EXP-003 verdict](../../problems/number-theory/riemann-hypothesis/experiments/EXP-003-odd-frame-pressure/verdict.md), [proof](../../problems/number-theory/riemann-hypothesis/experiments/EXP-003-odd-frame-pressure/mathematical-proof.md),
[audit](../../problems/number-theory/riemann-hypothesis/experiments/EXP-003-odd-frame-pressure/adversarial-audit.md), and [results](../../problems/number-theory/riemann-hypothesis/experiments/EXP-003-odd-frame-pressure/artifacts/result.json) give the
current bound 0.419087888170111727959091183775 at theta=3/4. Its new 16,797-node
certificate passed both arithmetic evaluators. Full repository validation passed
288 Python tests. EXP-003 was declared in 8ed806d before all computation; proof
commit e21618c and result commit abfa001 preserve the sequence.

## 3a. Confirmed EXP-004 result

The parity theorem retains odd critical support and multiplicity excess in the
finite inequality, then packs one fixed classical odd-zero density seed into every
longer fixed-exponent interval. It proves a fixed $\theta_1<\theta_0$ with positive
simple-critical liminf on $[\theta_1,1)$ and a distinct proportion above one half
on a nearby range. The constants $\kappa$, $\theta_1$ and the effective onset remain
unquantified. See [the complete proof](../../problems/number-theory/riemann-hypothesis/wiki/07-parity-density-transfer.md)
and [confirmed verdict](../../problems/number-theory/riemann-hypothesis/experiments/EXP-004-parity-density-transfer/verdict.md).

## 4. In flight

The user's latest request explicitly asks for alternatives across mathematical areas
and a more relevant result. EXP-005 is now declared from a new post-cutoff source.
Pearce-Crump's coefficient-uniform arbitrary-subinterval estimate suggests an
explicit odd-critical density for every fixed interval exponent above one half.
The frozen target combines that density with EXP-004 and tests a positive
simple-critical proportion at theta=0.546. Source preflight is complete;
implementation, the canonical certificate, proof review, and verdict are pending.

Completed source dossiers also investigate:

1. Parity, multiplicity slack, and existing positive critical-zero mass as a possible
   route to a stronger positivity range. Exact seed theorem definitions, uniformity,
   interval packing and prior-art checks are essential.
2. Full-operator negative spectrum and spectral/optimization witnesses. Negative
   eigenvalue counts alone are known prior art; near-line conditioning can obstruct
   any uniform quantitative gain.
3. Nyman-Beurling approximation, Li/Weil positivity, spectral realizations and heat
   flow. A finite diagnostic must state what it proves and what remains an infinite
   limit. Proposed finite-prime compression requires an adversarial obstruction check.

EXP-004 is confirmed in fbc4f9f after complete exact checks, independent proof review
and verdict. The full-operator,
approximation/tail, heat-flow and generalized short-mollifier routes remain separate
source/paper proposals. Preserve every rejected route. The v0.02 manuscript is frozen
and published at DOI 10.5281/zenodo.22728744; all 21 rendered pages were reviewed,
the PDF is 498,500 bytes, and the local publication helper's 43 boundary tests pass.
The published v0.01 archive remains byte-identical.

## 5. Next actions

Implement and run EXP-005 exactly as declared, then adjudicate every localization
error term independently before writing a verdict. Preserve the released
v0.65.000 evidence. Publication and a new serialized release are considered only
if the explicit short-interval theorem survives both the certificate and proof
review; existing rendered QA and live verification receipts remain immutable.

## 6. Where everything lives

Problem: `problems/number-theory/riemann-hypothesis/`. The EXP-003 execution receipt
records exact commands and deterministic result hashes. Source restoration and replay
instructions: `docs/guides/riemann-replay.md`. The exporter reads committed Git HEAD
bytes and binds the hypothesis, code, runner, seeds, candidate list and certificates.
Dirty files cannot become replay evidence.

First release receipts: `program/riemann-hypothesis/release-0.64.000/`; current
release and live evidence: `program/riemann-hypothesis/release-0.65.000/`.
Frozen first preprint archive: `manuscripts/riemann-hypothesis/short-interval-stability/versions/v0.01/`.
Private coordination: `plans/caos-research/riemann-hypothesis/` in CAOS_MANAGE.

## 7. Gotchas

N counts all copies; simple-critical, odd-critical, distinct-critical and all distinct
counts differ. The Hilbert pair sum uses ordinary complex squares. Test functions and
support are fixed before height limits. A numerical energy certificate is a finite
premise, not a stand-alone zeta theorem. Imported pressure/stability frameworks retain
their authorship; dated source searches do not guarantee priority or peer acceptance.
