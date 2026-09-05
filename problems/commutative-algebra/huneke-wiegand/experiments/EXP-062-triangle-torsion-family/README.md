# EXP-062: a quadratic family of independent two-torsion classes

Status: **CONFIRMED: quadratically many independent integral order-two classes.**

For every increasing nonnegative triple `T=(i,j,k)` of sum `p-2`, the
declared construction supplies an original integral source `W_T` for `2x_ij`
and a relative parity functional detecting its class. The [proof](proof.md)
gives an embedded `(Z/2)^q` in the full integral cokernel, where
`q=floor(((p-2)^2+3)/12)`. Independent proof review and the complete
original-sector audit pass. A further existence argument shows this detected
subgroup is a direct summand; no explicit global retraction is claimed.

The producer passes all 70 declared signed source checks, all small pairing
matrices, 93 count checks, and five eta-to-`x_02` quotient-transfer source
identities. Functional supports have ten to twelve rows; adjacent endpoints
are handled explicitly. This is not a full-quotient or recurrence claim.

- [hypothesis.md](hypothesis.md): committed declaration and execution gate.
- [proof.md](proof.md): generic signed sources, complete relative-dual argument,
  diagonal detection, exact count, and a nonconstructive splitting corollary.
- [run.py](run.py): original signed source producer and generic functionals.
- [artifacts/results.json](artifacts/results.json): compact exact checks.
- [artifacts/results-sources.json.gz](artifacts/results-sources.json.gz): all
  70 complete labelled W sources and five transfer sources, preserved losslessly.
- [audit.py](audit.py) and [artifacts/audit-results.json](artifacts/audit-results.json):
  independent original-source and full-kernel certificates.
- [verdict.md](verdict.md): precise scope, audit counts, hashes, and remaining gates.

The independent audit certifies all 27 triangles at `p=8,...,12` on 364
complete triangle-sector matrices, representing 65 distinct high sectors. It
also independently checks all 70 signed W sources and all five eta transfers.
All 39 combined tests, focused Ruff checks, and byte-identical independent
audit replay pass. Each campaign finishes within its 120-second and 1-GiB
caps. No old HNF source is read.

## Reproduction

```powershell
.venv/Scripts/python.exe problems/commutative-algebra/huneke-wiegand/experiments/EXP-062-triangle-torsion-family/run.py
.venv/Scripts/python.exe problems/commutative-algebra/huneke-wiegand/experiments/EXP-062-triangle-torsion-family/audit.py
.venv/Scripts/python.exe -m pytest tests/test_hw_triangle_torsion_family.py tests/test_hw_triangle_torsion_audit.py -q
```

The producer accepts `--output`, `--smoke-only`, and `--budget` up to 120
seconds. The auditor accepts `--results`, `--output`, `--seconds`, and
`--memory-mib`, within the declared caps. Tests use temporary outputs.

The all-parameter theorem rests on the complete signed source/functional
proof, not extrapolation from sampled triangles. It strengthens the unpublished
complementary manuscript substantially, while leaving the full quotient,
isolated/relative-completion identifications, and recurrence open. No new
Zenodo publication is claimed by this experiment record.
