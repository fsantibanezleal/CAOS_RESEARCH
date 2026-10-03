# Riemann hypothesis handoff

## 1. State in one screen

Updated 2026-10-03. Read [state.md](state.md), [backlog.md](backlog.md), and
the [October dossier](../../problems/number-theory/riemann-hypothesis/context/2026-10-03-update-and-dual-family-preflight.md).
EXP-010 is confirmed on branch `work/riemann-hypothesis/levinson-parity-20260926`
(two referee passes, minor fixes applied):
the localized Levinson detector with degree-201 operator polynomials gives a
positive proportion of simple critical zeros in `(T,T+T^theta]` for every
fixed `theta` in `[0.534,1)` (previous onset `0.5458838`), and about 1000 times
the EXP-008 density at `theta=0.5459`. Its manuscript
`manuscripts/riemann-hypothesis/short-interval-levinson/` v0.01 is published at
[10.5281/zenodo.22984155](https://doi.org/10.5281/zenodo.22984155), byte-verified,
and EXP-010 is promoted to `develop` and `main`. Release 0.74.000 (replay v9: EXP-010 to EXP-012) is the latest
live release. General RH remains open.

## 2. The objects table

| Object | Role | Current evidence |
|---|---|---|
| `R(alpha,beta)` | Three-point kernel ratio | Sharp theorem in EXP-009 |
| `sqrt(2)` | Optimal universal ratio constant | Equality only at `(0,1)` and `(1,0)` |
| `d_dagger` | Sharpened global optimization parameter | `0.283165430808537327...` |
| `C_simple` | Attributed global simple-critical lower proportion | `0.6725007995946757558283550562963947865...` |
| `C_distinct` | Attributed distinct-strip companion | `0.8362503997973378779141775281481973932...` |
| EXP-017 `q` | Attributed seven-point distinct-strip lower bound | `0.83699292567522...`; full-energy assembly |
| EXP-018 conditional `q` | Larger distinct-strip target; nine-point local premise unclosed | `3997934614153/4775549550000 = 0.83716744477146...` |
| EXP-016 `q` | Attributed earlier distinct-strip bound | `69341429073721/82845897125000 = 0.83699291672944...`; trace-aware assembly |
| EXP-013 `q` | Attributed improved distinct-strip bound | `62359683640669/74504434380000 = 0.83699291404068...`; fixed-input optimum |
| EXP-009 portable result | Exact theorem checks, source replay, global and local transfers | SHA-256 `0cea78e847d1bcec62eb8cd809b704ceaebd58f78f1c405f13ec40838fbb5a66` |
| Manuscript v0.01 | Seven-page published preprint | DOI `10.5281/zenodo.22940291` |
| `kappa(P,Q,R,nu)` | Localized Levinson distinct sign-change density | `>0.7170 nu` at eight frozen `nu`; EXP-010 |
| `h(theta;kappa)` | Parity transfer of the Levinson density | positive for every `theta` in `[0.534,1)`; `>0.0177638` at `0.5459` |
| EXP-010 canonical result | Exact admissibility, Arb constants, anchors, onset | SHA-256 `74ed14a925bdd10f27d09d6fb23a8e43f9474f8e0e5280fceafac33e06f49464` |
| `short-interval-levinson` v0.01 | Ten-page manuscript of EXP-010 | DOI `10.5281/zenodo.22984155` (concept `10.5281/zenodo.22984154`), public bytes verified |

## 3. Experiment index

| Experiment | Outcome |
|---|---|
| EXP-001 | source constants and normalization confirmed |
| EXP-002 | first short-interval stability theorem confirmed |
| EXP-003 | odd-frame pressure improvement confirmed |
| EXP-004 | qualitative parity range extension confirmed |
| EXP-005 | rank-three local Selberg curve confirmed |
| EXP-006 | sharp Hilbert-parity product confirmed |
| EXP-007 | spectral-defect parity product and strict full-curve gain confirmed |
| EXP-008 | fixed-rank localization and attributed rank-six onset confirmed |
| EXP-009 | sharp three-point ratio, attributed global gain, and onset-neutral local companion confirmed |
| EXP-010 | short-window Levinson moment, distinct sign-change count, certified degree-201 detectors, onset `0.534` confirmed (Prediction A scope corrected to `Q(0)=1`) |
| EXP-011 | confirmed linear-refinement counterexamples |
| EXP-012 | inconclusive Tang route; standard bounds do not extend length |
| EXP-013 | confirmed source-based distinct-strip parameter gain and uniform cap |
| EXP-014 | confirmed generic pointwise phase obstruction |
| EXP-015 | confirmed obstruction on squarefree twists with nonzero basic mollifier coefficients |
| EXP-016 | confirmed trace-aware clipped-block refinement and revised integer cap |
| EXP-017 | confirmed full-energy envelope and pressure transfer; scaled prior art, small exact gain |
| EXP-018 | confirmed conditional nine-point transfer 0.83716744477146...; local replay obligation open |
| EXP-021 | confirmed classical shifted composite arithmetic layer; exact gcd, conductor and unequal-shift controls; analytic reciprocity and cancellation remain open |
| EXP-022 | confirmed fixed-packet pressure-family cap 0.837421287797... for all p>=0; changed-pressure candidate 0.837385561059... requires a new complete local certificate |
| EXP-024 | confirmed exact shifted Gaussian/Mellin representation and controlled smooth compact-window reduction; signed moment main sum remains open |

## 4. In flight

EXP-019 is admitted as bounded RH-F10. The complete rounding audit, source
binding and independent window audit passed. Its source-identical traversal
is suspended with validated snapshots (33 checkpoints, nine completed shards
at backup) to prioritize EXP-020; it has no complete-certificate verdict.
The backup receipt is under EXP-019/artifacts/baseline-snapshot-receipt.json.

EXP-020 is admitted as bounded RH-F11. Its independently declared stronger
target is 3051/500000 = 0.006102. Shard 0 passed with 648919 nodes; the full
96-shard cover is running with 24 workers on
`work/riemann-hypothesis/nine-replay-20261003`. Sixteen quadratic controls and
the 230-test Riemann suite passed. These controls and partial coverage are
not a universal local inequality or a new distinct-zero proportion. Issue
#358 tracks the stronger certificate. The independent stdlib cover auditor
supports both experiments and rejects incomplete coverage. Runtime-bound
source must remain frozen while workers run.

EXP-022 proves a uniform ceiling for this fixed window/weight schedule,
not for the true zero proportion: every finite admissible pressure/block
transfer is below 0.8374212877970697... . Two rational configurations,
192-bit enclosures and an independent native-sinc 256-bit audit close
the rising/falling-line proof. Issue #361 tracks this supporting result.
At p=1/1250, delta=52231/5000000, m=562, tau=1203/500, c=1703/500, a new
universal certificate would give 2340938143167/2795532013000 =
0.8373855610599298... . This passes the declared 0.0001 improvement
value gate; a separately declared certificate pilot is the next bounded
step. The six-second exploration does not prove that new lower bound.

EXP-023 is now admitted as bounded RH-F13, with issue #362. Its separately
bound wrapper, runner and independent auditor are committed in 62dd7923.
Thirty targeted controls pass. Directed pressure rounding is checked over
all 417849 possible sums of cell indices; the frozen EXP-020 source is
unchanged and its corresponding 488161 sums also pass. One actual shard-0
pilot began at 19:35:50 UTC on 2026-10-03, with a twenty-minute budget after
preparation, one additional CPU and external state in
`exp023-repressured-local-v2-20261003`. Read its live checkpoint before any
cost or completion claim. The preliminary prepare-only directory without
`v2` is retained but cannot be resumed by this strengthened binding.
EXP-023 at a different pressure does not imply EXP-018's local premise.

Update: that first pilot hit its budget incompletely and was stopped after
a validated backup at 19:57:22 UTC. It had one initial Cartesian box, so
only shard zero had actual work. The measured cost and 92-second budget
overrun are recorded in EXP-023/pilot-review.md. A separately bound exact
quarter partition gives 65536 initial boxes over 96 shards, with unchanged
pruning code and 41 targeted controls. Commit 748bcfb9 precedes its actual
shard-0 pilot, launched about 20:08:02 UTC with the same twenty-minute
budget. External state: `exp023-partitioned-local-20261003`; session 98159.
Keep both earlier pilot backups and all runtime-bound source frozen.

The revised pilot was stopped at 20:33:47 UTC after a validated backup:
1912832 nodes, depth 56, nine pending boxes, incomplete. Its 345-second
budget overrun and the subsequent six-hour full-cover cost review are
persisted. Commit 295ee71c includes an independent operational budget
supervisor, with three passing controls including a real owned process
tree and preservation of an unrelated sentinel. Both orchestration setup
failures are retained. The mathematical verifier source was not changed.
The full cover resumed at 20:48:12 UTC, four workers, same binding and
`exp023-partitioned-local-20261003`; supervisor session 37164, root PID 49576.
The actual six-hour deadline is 2026-10-04 02:48:12 UTC. Its external
full-cover-budget-receipt.json records ownership, command and source hashes.
At 20:50 UTC 94/96 shards were complete; coverage remains incomplete.
The complete mathematical auditor and exact transfer are still required.
The prior full Riemann suite passed; the three new orchestration controls
also pass. Scoped collection now finds 258 Riemann tests. A separate attempt
to collect all problem suites encountered 24 unrelated dependency errors;
it was abandoned in favor of the explicit Riemann file list, not reported
as a Riemann test failure or as full-repository validation.

External resumable state is under E:/_Datos/caos-research/riemann-hypothesis/
exp020-quadratic-local-20261003 (stronger run) and
exp019-local-replay-20261003 (suspended baseline). The stronger run's full-cover
planning budget is twelve hours from launch; a budget hit is incomplete and
does not fulfill the research objective. Resume the baseline if the stronger
target fails or its mathematical review raises a concern.
EXP-013--018 are closed research records. EXP-018 is conditional on its
unreplayed nine-point local input; issue #356 tracks that obligation.
The latest deployed replay remains v9 with twelve experiments. The tag
v0.74.000 is verified; no pending-tag action remains.

## 5. Next actions

The October strategic review retains RH-F4; bounded RH-F6--F9 are closed;
RH-F10 and RH-F11 are admitted for EXP-019 and EXP-020.
The onset remains 0.534. Direct CIS substitution and uniform pointwise
phase repairs are closed, including nonzero Mobius support. Signed
off-diagonal cancellation is not excluded.

1. RH-046: complete EXP-020's stronger 96-shard certificate and independent
   audit; issues #356 and #358. Check every binding, domain component and
   checkpoint. A complete stronger inequality implies EXP-018's weaker local
   premise; it does not retroactively complete EXP-019's suspended traversal.
   Re-evaluate a distinct-strip companion manuscript only after complete
   certification, exact transfer, analytic review and scientific value review.
2. RH-038: derive the complete shifted, composite-twist signed reduction,
   retaining gamma ratios, parity and oscillatory factors. EXP-021 closes
   its classical arithmetic layer: the local numerator is
   `S_b-p^(-alpha-beta)*S_(b-1)*chi(p)*p^(-s)` when `p` does not divide
   `q=h/d`; it is `S_b` otherwise. All gcd classes and primitive Euler
   factors are retained. The uniform shifted Mellin weight, residues and
   analytic errors remain to be proved before seeking signed cancellation
   or a spectral decomposition. Exact controls passed in 4.17 CPU seconds.
   EXP-024 subsequently closes the representation step for its stated
   Gaussian and fixed smooth compact windows, bounded polynomial-length
   composite twists and O(1/log T) shifts. Its exact residue and all-order
   phase/heat remainders are proved, with independent enclosed kernel and
   full-moment normalization controls. The signed main sum and its primitive
   conductor/gcd/polyweight estimates remain open. No onset upgrade follows.
3. RH-029: independently audit the rectangle-detour defect in EXP-005/008.
4. RH-021: recover an exact rank-six coefficient matrix or source artifact.
5. RH-042: later serialized replay/workbench release for the new records.

Latest source-based distinct-strip bound: EXP-017, 0.83699292567522... .
No new paper or Zenodo deposit yet. EXP-020's manuscript gate review removes
an unnecessary sharp energy-envelope step: at the proposed transfer parameters
D < tau^2, the attributed elementary block dichotomy suffices. A stronger local
certificate and its resulting distinct-strip transfer still require completion.

## 6. Where everything lives

Problem evidence is under `problems/number-theory/riemann-hypothesis/`.
EXP-010 proof, audit, controls, verdict, runners and immutable outputs are
under `experiments/EXP-010-levinson-parity-transfer/`; its manuscript source
is under `manuscripts/riemann-hypothesis/short-interval-levinson/`.
EXP-009 proof, audit, verdict, runner, and immutable outputs are under
`experiments/EXP-009-wang-kernel-sharpening/`. Replay instructions are in
[docs/guides/riemann-replay.md](../../docs/guides/riemann-replay.md). The
manuscript and publication receipt are under
`manuscripts/riemann-hypothesis/sharp-three-point-kernel/`. Latest release evidence is under `program/riemann-hypothesis/release-0.74.000/`. Private
coordination is mirrored under `plans/caos-research/riemann-hypothesis/` in
CAOS_MANAGE.

Reproduce the new certificate from the repository root:

```text
python problems/number-theory/riemann-hypothesis/experiments/EXP-009-wang-kernel-sharpening/run.py --output-dir tmp/riemann-exp009-replay --budget-seconds 600
python -m pytest -q tests/test_riemann_wang_kernel_sharpening.py tests/test_bake.py
```

## 7. Gotchas

EXP-023's complete-output corruption and exact-byte archive gates are
prepared in its `actual_cover_controls.py`, `reproducibility_archive.py`
and `reproducibility-review.md`. Both reject the actual incomplete
95-report output. Execute their completed-input paths after all 96
reports and the independent cover/transfer audits pass. CI 37155303536
passed for 098c0476 with repository-contract scope only. The unscoped
local structure checker cannot validate missing other-problem trees in
this sparse checkout; do not expand it beneath the frozen workers.

Both active covers were 95/96 at 22:31 UTC. EXP-023's additional native
kernel-first input audit passed every closed cell in both 52,240-cell tables;
see its source-bound native-kernel-taylor-full.json and mathematical
declaration. Earlier direct-interval and squared-kernel Taylor variants were
inconclusive and remain preserved. The archive builder now includes and
requires this successful native audit; its earlier partial-rejection receipt
binds the earlier builder version. Complete-cover gates remain mandatory.

The ratio theorem is an exact CAOS result. The global proportion transfers
through Wang's attributed arXiv:2609.24167v1 framework; it is not an independent
proof of that preprint. The short-interval companion still uses attributed pair
and rank-six inputs, and it does not change the onset. CPU arithmetic is
sufficient. A DOI, finite census, passing build, or successful deployment does
not prove RH or establish external peer acceptance.
