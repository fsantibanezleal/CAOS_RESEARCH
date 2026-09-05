# EXP-061: a twelve-row relative parity functional

Status: **CONFIRMED: one nonzero integral order-two class for every p>=8.**

The committed hypothesis defines a twelve-row `F_2` functional detecting
the tracked endpoint eta. The [proof](proof.md) classifies all original K
sources and every S high sector that can meet its support, reconstructs the
complete generalized-potential D kernels, and gives a relative-functional
contradiction to eta being a full original boundary.

Combined with EXP-060's integral twice-source identity, the argument proves
exact order two for eta and the EXP-057-equivalent class of `b_A+b_B`, for
every `p>=8`. Independent proof review and the full original-source audit
pass. No second class or complete quotient is asserted by this experiment.

- [hypothesis.md](hypothesis.md): frozen functional, complete sector list,
  campaign, caps, and rejection controls.
- [proof.md](proof.md): all-parameter argument, including the `10p-3` sector,
  `d=2` endpoint freedoms, and the original-class transfer.
- [verdict.md](verdict.md): current validation status and remaining gates.
- [run.py](run.py) and [artifacts/results.json](artifacts/results.json):
  2,123 potential chains at 14 declared parameters, including all small bases.
- [audit.py](audit.py) and [artifacts/audit-results.json](artifacts/audit-results.json):
  independent full-sector enumeration, exact D-row dual certificates, and controls.

The declaration was committed and pushed as `9169f23` before computation.
Producer and auditor each complete within their 120-second and 1-GiB caps.
The independent audit covers all 65 reachable high sectors at `p=8,...,12`:
23,695 original S columns, 108,261 complete D rows, and 231,986 incidences.
Its 1,070 labelled D-row dual terms certify annihilation of the full D kernels;
the audit does not import the producer's potential formulas. All 20 independent
adverse controls, all 21 new tests, and focused Ruff checks pass.

## Reproduction

```powershell
.venv/Scripts/python.exe problems/commutative-algebra/huneke-wiegand/experiments/EXP-061-uniform-parity-functional/run.py
.venv/Scripts/python.exe problems/commutative-algebra/huneke-wiegand/experiments/EXP-061-uniform-parity-functional/audit.py
.venv/Scripts/python.exe -m pytest tests/test_hw_uniform_parity_functional.py -q
```

The independent full audit also passes a byte-identical replay to temporary
outputs. No HNF or old `p=11` labelled source is read. Finite audit results
challenge the symbolic argument; they are not its proof of uniform completeness.

This upgrades the unpublished complementary-manuscript theorem from order
dividing two to exact order two for one tracked class. Publication still needs
the normal claim/build/render/Zenodo gates; no new public version is claimed here.
