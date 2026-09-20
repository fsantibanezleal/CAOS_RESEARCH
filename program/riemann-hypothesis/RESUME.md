# Riemann hypothesis handoff

## 1. State in one screen

Read [state.md](state.md), [backlog.md](backlog.md), and the latest EXP-007/008
verdicts. Public application release 0.71.000 remains live-verified. EXP-007 and
EXP-008 are confirmed, manuscript v0.07 is published, research PR #325 is
merged, and release 0.72.000 is the active candidate. General RH remains open.

EXP-007 proves the finite spectral-defect product

$$
(Q-S-D(G))(N-O)\ge2(N-S)^2.
$$

EXP-008 proves fixed finite-rank localization and applies Pearce-Crump's stated
rank-six constant. It certifies
`0.5458837<theta6<0.5458838`, strictly earlier than
`0.5458846<theta3<0.5458847`. At theta=0.5459, the rank-six lower bound exceeds
`0.0000177645181613023236390595079`. The public source does not print the
rank-six coefficient matrix, so $C_6$ remains an attributed theorem input.

## 2. The objects table

| Object | Role | Current evidence |
|---|---|---|
| `N,S,O,Q` | Copies, simple real support, odd real support, pair sum | EXP-006 finite proof |
| `D(G)` | Simple-real Gram spectral defect | EXP-007 finite proof |
| `Cq` | Fixed finite-rank Selberg detector constant | Pearce-Crump theorem input |
| `kq(theta)` | Local odd-support curve `(theta-1/2)/(4eCq)` | EXP-008 localization proof |
| `hq(theta)` | Hilbert-parity quadratic lower term | EXP-008 transfer |
| `theta6` | Unique rank-six positivity onset | `(0.5458837,0.5458838)` |
| EXP-007 portable result | 652,260 spectra and 18,479 profiles | SHA-256 `98094f267a78b88b8a976de6b6d816fbb25231869a6ad5dc8c941411bfa45947` |
| EXP-008 portable result | Rank-six onset, point comparison, spectral companion | SHA-256 `1ccfa56face643fb96148856c4608577b3afa75947383cf738423ce13eeb5781` |
| Manuscript v0.07 | 30-page published preprint | DOI `10.5281/zenodo.22860012` |

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

The EXP-007 portable result hash is
`98094f267a78b88b8a976de6b6d816fbb25231869a6ad5dc8c941411bfa45947`.
The EXP-008 portable result hash is
`1ccfa56face643fb96148856c4608577b3afa75947383cf738423ce13eeb5781`.

## 4. In flight

1. Replay v7 and the bilingual EXP-007/008 workbench are merged into `develop`
   through research PR #325, whose full Linux CI passed.
2. Release 0.72.000 is being validated on its scoped release branch.
3. The candidate must pass rendered browser QA, promote through `develop` and
   `main`, and record exact live verification.
4. The private CAOS_MANAGE mirror and Zenodo deposit ledger still need the
   final release receipts.

Manuscript v0.07 is already published at
[10.5281/zenodo.22860012](https://doi.org/10.5281/zenodo.22860012). Its 575,351
byte repository PDF and a fresh public download share SHA-256
`c7bda5f1acc0b34ac33b6a071e66586b4032ae6e385d93f7fdd2d197411dbf81`.

## 5. Next actions

1. Prepare the 0.72.000 version, changelog, replay data, and release evidence.
2. Run repository, frontend, and rendered browser gates.
3. Promote `develop` to `main`, tag the exact release commit, and verify Pages
   bytes plus live EN/ES light/dark desktop/phone scenarios.
4. Mirror the publication and release receipts into CAOS_MANAGE.
5. Pursue independent rank-six coefficient reconstruction as the next bounded
   mathematical target.

## 6. Where everything lives

Problem evidence: `problems/number-theory/riemann-hypothesis/`.
EXP-007 and EXP-008 proofs, audits, verdicts, runners, and immutable outputs are
under their `experiments/` directories. Replay instructions are in
[docs/guides/riemann-replay.md](../../docs/guides/riemann-replay.md).
The manuscript and publication receipts are under
`manuscripts/riemann-hypothesis/short-interval-stability/`. Release evidence
belongs under `program/riemann-hypothesis/release-0.72.000/`. Private
coordination is mirrored under `plans/caos-research/riemann-hypothesis/` in
CAOS_MANAGE.

Reproduce the two new certificates from the repository root:

```text
python problems/number-theory/riemann-hypothesis/experiments/EXP-007-spectral-defect-parity/run.py --output-dir tmp/riemann-exp007-replay --budget-seconds 180
python problems/number-theory/riemann-hypothesis/experiments/EXP-008-rank-six-local-transfer/run.py --output-dir tmp/riemann-exp008-replay --budget-seconds 120
python -m pytest -q tests/test_riemann_spectral_defect_parity.py tests/test_riemann_rank_six_local.py
```

## 7. Gotchas

`N` counts copies; `S` and `O` count support points. Fixed finite rank means
rank is chosen before the height limit. The public source prints the certified
$C_6$ interval but not its coefficient matrix, so do not describe EXP-008 as an
independent reconstruction. The runners require fresh output directories,
clean canonical source commits, and exact source hashes. Historical Windows
byte streams cited by v0.07 are preserved separately from the portable LF
canonical outputs. CPU arithmetic is sufficient; GPU acceleration is not
justified for these low-dimensional exact certificates. A DOI, finite census,
passing build, or successful deployment does not prove RH or establish external
peer acceptance.
