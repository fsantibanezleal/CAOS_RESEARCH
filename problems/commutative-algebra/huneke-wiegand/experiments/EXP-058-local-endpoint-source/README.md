# EXP-058: local endpoint source search

Outcome: **P1 REFUTED at p=8; P2 NOT APPLICABLE**. The complete radius-two source span excludes
`2eta_8` over the rationals. This is a local obstruction, not a conclusion about the full
original source domain or the all-parameter problem.

The deterministic producer enumerates full original inverse incidence for two row-column-row
rounds. It uses exact rational elimination with source provenance and unit-first pivots. All
additional boundary equations are retained with right-hand side zero. Integer dual certificates
make the local rational refutations independently checkable.

From the repository root:

```powershell
.venv/Scripts/python.exe problems/commutative-algebra/huneke-wiegand/experiments/EXP-058-local-endpoint-source/run.py
.venv/Scripts/python.exe problems/commutative-algebra/huneke-wiegand/experiments/EXP-058-local-endpoint-source/audit.py
.venv/Scripts/python.exe -m pytest tests/test_hw_local_endpoint_source.py
```

The default producer run stops after the first completed radius-two refutation, which is `p=8`
in the canonical record. A separately authorized retained-claims continuation can use
`--continue-retained` with a distinct `--output` path. It must not erase the stopped canonical
outcome or be described as the original campaign. No such continuation was run for this result.

The maximum budget is 60 seconds, one CPU process, 1 GiB private memory, 1200 columns and 20000
nonzero incidences per parameter. CLI options may lower, but not raise, the caps. Completed
smaller neighborhoods are preserved if a later expansion stops; a cap is INCONCLUSIVE, not a
rational or integral refutation. A nonintegral particular solution is likewise inconclusive
about integer membership.

Artifacts:

- [results.json](artifacts/results.json): complete labels, incidence, frontiers, provenance,
  original-coordinate residuals, integer duals, premise hashes and resource bounds.
- [audit-results.json](artifacts/audit-results.json): independent complete-neighborhood,
  full-boundary, residual, dual and mutation verification.
- [proof.md](proof.md): exact local obstruction and the escaping-column necessary-condition lemma.
- [verdict.md](verdict.md): finite conclusions, validation metrics, hashes and remaining gates.

No HNF, global basis enumeration, old HNF source, or original `p=11` source labels are accessed.
Tests write only temporary files. Nothing here establishes nonzero full-cokernel class or an
all-parameter order-two witness, and no manuscript or Zenodo publication is performed.
