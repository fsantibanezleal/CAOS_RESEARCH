# Code ownership

Exact experiment checkers remain with their frozen hypotheses and certificates:

- `../experiments/EXP-001-tree-strip/run.py`: original tree-strip controls, unchanged.
- `../experiments/EXP-002-next-shell/run.py`: full-shell constructions, independent finite checks, damaged-edge and complement-cycle controls, and the order-six census. It reuses the EXP-001 exact graph routines; the certificate records both source hashes.

Replay EXP-002 from the repository root with `python problems/combinatorics/bougard-joret/experiments/EXP-002-next-shell/run.py --output tmp/bougard-shell-replay.json`. The existing regression replay is `tests/test_bougard_joret_tree_strip.py`; consult the experiment verdict for current required checks. No reusable package is claimed here. Finite checker PASS is not a substitute for the all-parameter proof.

The full-shell regression is `tests/test_bougard_joret_next_shell.py`. Install the pinned `EXP-002-next-shell/requirements-audit.txt` for the separate `audit.py` replay; it uses NetworkX rather than the CAOS verifier functions and binds the proof and source hashes in `artifacts/independent-audit.json`.
