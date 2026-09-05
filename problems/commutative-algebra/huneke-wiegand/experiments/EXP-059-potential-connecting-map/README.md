# EXP-059: potential basis and sparse connecting map

Status: **CONFIRMED in the declared fixed-high sector**, for every integer `p>=8`.
The full connecting-parity problem remains open.

For original S sources whose exterior high set is exactly `{6p,8p-4}`, the D
kernel has an explicit integral potential basis of rank `binom(p-1,2)`. Every
unit-potential source has coefficient height one and at most `3p-5` terms. Its
complete original boundary contains no D rows and at most seven K rows.

The uniform conclusion rests on signed reconstruction and complete face
classification, not on extrapolating the finite experiment.

## Evidence and interfaces

- [hypothesis.md](hypothesis.md): immutable declaration, scope, and resource caps.
- [proof.md](proof.md): exhaustive original-source classification, integral
  reconstruction from endpoint zero, and seven-row boundary theorem.
- [run.py](run.py): `unit_chain(p,u,r)` returns the source and its alpha/beta
  parts; `boundary_formula(p,source)` gives its complete retained K boundary.
- [artifacts/results.json](artifacts/results.json): 861 exact chain checks.
- [audit.py](audit.py): coefficient-first reconstruction and a separately
  encoded bitset differential.
- [artifacts/audit-results.json](artifacts/audit-results.json): independent
  861-chain audit, including 525 literal-differential crosschecks.
- [verdict.md](verdict.md): claim boundaries, adversarial evidence, and
  publication assessment.

The unit-potential indices are `0<=u<=p-3`, `u+2<=r<=p-1`. Every basis chain
is checked for `p=8,...,16`; four frozen endpoint pairs are checked at each
`p=17,...,100`. No old HNF source or original `p=11` source holdout is read.

## Reproduction

From the repository root, the canonical producer and independent auditor are:

```powershell
.venv/Scripts/python.exe problems/commutative-algebra/huneke-wiegand/experiments/EXP-059-potential-connecting-map/run.py
.venv/Scripts/python.exe problems/commutative-algebra/huneke-wiegand/experiments/EXP-059-potential-connecting-map/audit.py
.venv/Scripts/python.exe -m pytest tests/test_hw_potential_connecting.py -q
```

Each campaign has a 60-second, 1-GiB process cap. The producer checkpoints and
flushes after each parameter, with budget checks inside source generation. Tests
write only to temporary paths. The producer accepts `--maximum` in `8..100` and
`--output`; the auditor accepts `--results` and `--output` for temporary replays.

## Next mathematical use

Use this sparse connecting map as a structural input to a separately declared
comparison across high sectors or to an integral reduction of the K relations.
The theorem does not yet place `2eta` in the full image, establish nonvanishing,
provide the second class, or supply a quotient upper bound. The current scoped
basis is not a normal form of the full connecting quotient.
