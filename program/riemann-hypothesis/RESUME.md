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
| EXP-016 `q` | Attributed latest distinct-strip bound | `69341429073721/82845897125000 = 0.83699291672944...`; trace-aware assembly |
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

## 4. In flight

No computation is in flight. EXP-013--017 are closed research records.
The latest deployed replay remains v9 with twelve experiments. The tag
v0.74.000 is verified; no pending-tag action remains.

## 5. Next actions

The October strategic review retains RH-F4; fixed-input RH-F6 and trace-aware RH-F7 are closed.
The onset remains 0.534. Direct CIS substitution and uniform pointwise
phase repairs are closed, including nonzero Mobius support. Signed
off-diagonal cancellation is not excluded.

1. RH-038: derive the complete shifted, composite-twist signed reduction,
   retaining gamma ratios, parity and oscillatory factors; only then seek
   polynomial-height asymptotic evaluation or a spectral decomposition.
2. RH-029: independently audit the rectangle-detour defect in EXP-005/008.
3. RH-021: recover an exact rank-six coefficient matrix or source artifact.
4. RH-042: later serialized replay/workbench release for the new records.

Latest source-based distinct-strip bound: EXP-017, 0.83699292567522... .
No new paper or Zenodo deposit: fixed-input tuning and an elementary
supporting obstruction do not meet the coherent manuscript gate.

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

The ratio theorem is an exact CAOS result. The global proportion transfers
through Wang's attributed arXiv:2609.24167v1 framework; it is not an independent
proof of that preprint. The short-interval companion still uses attributed pair
and rank-six inputs, and it does not change the onset. CPU arithmetic is
sufficient. A DOI, finite census, passing build, or successful deployment does
not prove RH or establish external peer acceptance.
