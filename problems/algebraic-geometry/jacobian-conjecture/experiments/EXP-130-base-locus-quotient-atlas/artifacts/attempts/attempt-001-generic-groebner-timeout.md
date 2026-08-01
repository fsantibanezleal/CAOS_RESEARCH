# Attempt 001: generic rational Groebner timeout

Command:

```powershell
.venv\Scripts\python.exe problems\algebraic-geometry\jacobian-conjecture\experiments\EXP-130-base-locus-quotient-atlas\run.py
```

Observed result:

- EXP-123 and EXP-129 source hashes matched.
- Both exact projection resultants completed.
- Each resultant has degree 117 and factor-degree pattern
  \(1^{27},3,6,12,69\).
- The worker reached the declared 300-second gate during the generic rational
  Groebner stage.
- The orchestrator persisted `stopped_at_algebra_worker_timeout` and exited
  without a quotient-algebra conclusion.

Decision: retain the exact resultants and redirect to factorwise subresultants
and CRT. Do not increase the timeout for the same algorithm.

