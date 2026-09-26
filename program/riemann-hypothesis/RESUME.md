# Riemann hypothesis handoff

## 1. State in one screen

Read [state.md](state.md), [backlog.md](backlog.md), and the EXP-009 verdict.
EXP-009 is confirmed, its seven-page preprint is public at
[10.5281/zenodo.22940291](https://doi.org/10.5281/zenodo.22940291), replay v8
is built, and release candidate 0.73.000 has passed local and rendered QA.
General RH remains open.

EXP-009 proves `R(alpha,beta) <= sqrt(2)` for nonnegative inputs, with equality
only at `(0,1)` and `(1,0)`. Under Wang's attributed global framework this
improves the lower proportion of simple critical zeros to
`0.6725007995946757558283550562963947865...`, a gain exceeding `9.5915e-8`
over the source baseline. The source framework is recent and unreviewed.

## 2. The objects table

| Object | Role | Current evidence |
|---|---|---|
| `R(alpha,beta)` | Three-point kernel ratio | Sharp theorem in EXP-009 |
| `sqrt(2)` | Optimal universal ratio constant | Equality only at `(0,1)` and `(1,0)` |
| `d_dagger` | Sharpened global optimization parameter | `0.283165430808537327...` |
| `C_simple` | Attributed global simple-critical lower proportion | `0.6725007995946757558283550562963947865...` |
| `C_distinct` | Attributed distinct-critical companion | `0.8362503997973378779141775281481973932...` |
| EXP-009 portable result | Exact theorem checks, source replay, global and local transfers | SHA-256 `0cea78e847d1bcec62eb8cd809b704ceaebd58f78f1c405f13ec40838fbb5a66` |
| Manuscript v0.01 | Seven-page published preprint | DOI `10.5281/zenodo.22940291` |

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

## 4. In flight

1. The scoped candidate branch includes the EXP-009 evidence, published
   manuscript receipt, replay v8, nine-record workbench, and release QA.
2. Python replay/bake passed 64 tests; the frontend passed 24 tests, TypeScript,
   and production build.
3. Eight exact-candidate desktop/phone, EN/ES, light/dark scenarios passed with
   48 tab visits and 1,586 screenshots.
4. Push, develop PR, main promotion, tag, CI/Pages, and live-byte verification
   remain to be completed.

## 5. Next actions

1. Run the final repository guards and freeze the candidate commit.
2. Promote the scoped public and private branches through their develop and
   main gates.
3. Tag `v0.73.000`, create the GitHub release, and verify exact-main CI, Pages,
   public bytes, routes, and the live browser matrix.

## 6. Where everything lives

Problem evidence is under `problems/number-theory/riemann-hypothesis/`.
EXP-009 proof, audit, verdict, runner, and immutable outputs are under
`experiments/EXP-009-wang-kernel-sharpening/`. Replay instructions are in
[docs/guides/riemann-replay.md](../../docs/guides/riemann-replay.md). The
manuscript and publication receipt are under
`manuscripts/riemann-hypothesis/sharp-three-point-kernel/`. Candidate release
evidence is under `program/riemann-hypothesis/release-0.73.000/`. Private
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
