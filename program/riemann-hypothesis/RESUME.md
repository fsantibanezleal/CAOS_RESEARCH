# Riemann hypothesis handoff

## 1. Current state

Read [state.md](state.md), [backlog.md](backlog.md), and the latest EXP-007/008
verdicts. Public application release 0.71.000 remains live-verified. EXP-007 and
EXP-008 are confirmed, manuscript v0.07 is published, and replay v7 integration
is being prepared for the next serialized release. General RH remains open.

## 2. Confirmed new results

EXP-007 retains the simple-real Gram defect:

$$
(Q-S-D(G))(N-O)\ge2(N-S)^2.
$$

It gives a strict full-curve improvement where the scalar EXP-006 term is
positive. The portable result hash is
`98094f267a78b88b8a976de6b6d816fbb25231869a6ad5dc8c941411bfa45947`.

EXP-008 proves fixed finite-rank localization and applies Pearce-Crump's stated
rank-six constant. It certifies
`0.5458837<theta6<0.5458838`, strictly earlier than
`0.5458846<theta3<0.5458847`. At theta=0.5459, the rank-six lower bound exceeds
`0.0000177645181613023236390595079`. Its portable result hash is
`1ccfa56face643fb96148856c4608577b3afa75947383cf738423ce13eeb5781`.

The public source does not print the rank-six coefficient matrix. Treat $C_6$
as an attributed theorem input until it is independently reconstructed.

## 3. Publication

Version 0.07 of *Simple critical zeros in short intervals: stability, parity,
localization, Hilbert compression, and spectral defect* is published at DOI
[10.5281/zenodo.22860012](https://doi.org/10.5281/zenodo.22860012). The 575,351
byte repository PDF and a fresh public download share SHA-256
`c7bda5f1acc0b34ac33b6a071e66586b4032ae6e385d93f7fdd2d197411dbf81`.

## 4. Evidence map

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

The complete proofs, audits, verdicts, runners, and immutable outputs are under
`problems/number-theory/riemann-hypothesis/experiments/`. Replay instructions
are in [docs/guides/riemann-replay.md](../../docs/guides/riemann-replay.md).

## 5. Remaining release work

1. Finish replay v7 and frontend integration for EXP-007/008.
2. Rebase the scoped branch on the latest `develop` without absorbing unrelated
   work.
3. Run the repository, frontend, and rendered browser gates.
4. Promote through the repository's develop and main PR flow, then verify Pages
   bytes and live EN/ES light/dark desktop/phone scenarios.
5. Mirror the publication and release receipts into CAOS_MANAGE.

## 6. Next mathematical target

Independently reconstruct the rank-six coefficient matrix or obtain a public
source artifact that permits exact $C_6$ replay. After that, test a broader
finite-rank profile family. Any growing-rank proposal needs uniform control in
the rank before the height limit. Alternative Nyman-Beurling, Weil-positivity,
spectral, and heat-flow routes remain separate until their missing infinite
limits or arithmetic inputs are proved.

## 7. Reproduction

```text
python problems/number-theory/riemann-hypothesis/experiments/EXP-007-spectral-defect-parity/run.py --output-dir tmp/riemann-exp007-replay --budget-seconds 180
python problems/number-theory/riemann-hypothesis/experiments/EXP-008-rank-six-local-transfer/run.py --output-dir tmp/riemann-exp008-replay --budget-seconds 120
python -m pytest -q tests/test_riemann_spectral_defect_parity.py tests/test_riemann_rank_six_local.py
```

The runners require fresh output directories, clean canonical source commits,
and exact source hashes. CPU arithmetic is sufficient; GPU acceleration is not
justified for these exact low-dimensional certificates.
