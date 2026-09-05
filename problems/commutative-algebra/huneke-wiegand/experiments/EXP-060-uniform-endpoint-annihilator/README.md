# EXP-060: a uniform original source for twice the endpoint residual

Status: **CONFIRMED: uniform 2-annihilation, not uniform nonvanishing.**

For every integer `p>=8`, the explicit integral source `V_p` in the frozen
[hypothesis](hypothesis.md) satisfies `M V_p=2eta_p` in the complete original
presentation. Thus the tracked class has order dividing two. Combining the
identity with EXP-057 also gives
`M(2s+2q-V_p)=2(b_A+b_B)`.

The result follows from the all-parameter [signed proof](proof.md), independently
reviewed and attacked by complete boundary checks at all 18 declared parameters.
It does not establish a nonzero class, exact order two, another independent
class, or a quotient upper bound. The connecting-parity problem remains open.

## Evidence and interfaces

- [hypothesis.md](hypothesis.md): pre-computation formula, predictions, and caps.
- [proof.md](proof.md): full D/K faces, reflection-symmetric interval potentials,
  two short K corrections, exact eta identity, and the original-class transfer.
- [run.py](run.py): `potential_source(p,potential)` and `candidate_source(p)`
  generate original signed sources without matrix elimination.
- [artifacts/results.json](artifacts/results.json): compact component identities,
  complete four-row boundaries, adversarial checks, and archive manifest.
- [artifacts/results-sources.json.gz](artifacts/results-sources.json.gz):
  deterministic, losslessly compressed full labelled `V_p` sources at all
  declared parameters. No source coefficient or exterior label is omitted.
- [audit.py](audit.py): independent source reconstruction and bitset differential.
- [artifacts/audit-results.json](artifacts/audit-results.json): 18-parameter
  independent audit, archive verification, and 25 literal-differential checks.
- [verdict.md](verdict.md): exact scope, certificate hashes, research consequences,
  and the complementary-manuscript decision.

The declared campaign is `p=8,...,20,25,32,50,64,100`. Every parameter passes
P1/P2/P3, `M V_p=2eta_p`, complete D cancellation, and both sign/coefficient
mutation controls. Both distinct rejected preflight formulas fail as predicted.
Observed source support ranges from 110 to 3054 and coefficient height is five
throughout this campaign; those observations are not asserted as uniform counts.

## Reproduction

From the repository root:

```powershell
.venv/Scripts/python.exe problems/commutative-algebra/huneke-wiegand/experiments/EXP-060-uniform-endpoint-annihilator/run.py
.venv/Scripts/python.exe problems/commutative-algebra/huneke-wiegand/experiments/EXP-060-uniform-endpoint-annihilator/audit.py
.venv/Scripts/python.exe -m pytest tests/test_hw_uniform_annihilator.py -q
```

The producer accepts `--smoke-only`, `--output`, and a `--budget` no greater
than 60 seconds. The auditor accepts `--results` and `--output`; its callable
interface is `audit(results_path=None,budget_seconds=60)`. Each process is
limited to one CPU, 60 seconds, and 1 GiB private memory. The producer checks
inside generation and multiplication and checkpoints after each parameter.
Tests use temporary outputs. All 20 new tests and the focused Ruff check pass.

No HNF, Smith form, ambient full basis, or old labelled HNF source is used.
The new formula is checked at `p=11`, but the original `p=11` HNF-source
holdout remains unread; this campaign makes no untouched-holdout claim.

## Consequence

Uniform annihilation is now proved for the tracked class, so further work must
prioritize a functional annihilating every original relation and pairing
nontrivially with eta. Such a functional would upgrade order dividing two to
exact order two. A second class and a separate full-quotient upper bound remain
independent obligations.

The all-parameter full-cokernel consequence opens a narrowly scoped
complementary-manuscript candidate together with EXP-059. It does not authorize
claiming the complete parity quotient or a solved conjecture. Publication still
requires the normal claim, build, render, metadata, and public-download gates;
no new Zenodo publication is claimed by this experiment record.
