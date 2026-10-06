# Supervisor smoke history

The first real eight-second Windows ownership smoke on 2026-10-03 failed
in orchestration: after stopping a descendant, its Python launcher exited
before Stop-Process executed on that launcher. The reported missing PID
was 73448, in the captured owned tree of test root 45352. No mathematical
worker or verifier was part of this smoke. Its unrelated sentinel was
explicitly cleaned by the test's finally block.

The correction treats a captured process that has actually exited as
already exited, while still rejecting PID reuse or any live stop error.
The successful repeated real-process smoke and malformed-state rejection
are required before launch. Raw snapshots are operational preservation,
not complete-cover audits. This history is retained instead of discarding
the failed setup attempt.

A subsequent fast-exit control caught PowerShell's implicit exit status 1
after a missing Get-Process lookup. An explicit successful lookup-script
exit now permits a runner that already exited to receive an operational
receipt, without interpreting exit status 0 as proof. The repeated owned
tree stop and unrelated-process preservation passed during that attempt.
