# EXP-124 interrupted launches

The accepted run is represented by `../results.json`.

- Foreground attempt: the command wrapper terminated the process during
  modular progress output because its launch timeout was too short. It did
  not reach a mathematical decision gate.
- `2026-07-30-run-01.stdout.txt`: a detached retry completed both modular
  samples and the exact SCC-size gate. Its process tree was terminated when
  the detached launcher exited, before the symbolic worker produced an
  artifact.
- `2026-07-30-run-01.stderr.txt`: empty.

The accepted resumable run used the same mathematical implementation. It
completed the exact worker and every declared validation inside the original
compute gate.
