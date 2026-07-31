# EXP-127 attempt 001 - final JSON scalar serialization

Date: 2026-07-30.

The first full run completed the exact anchor, SCC, isolated determinant,
four rational controls, eight modular controls, quotient reduction, two norm
computations, factorization, and direct quotient-field classifications. It
then stopped before writing `results.json` because a multiplicity returned by
SymPy was a `sympy.Integer`, which Python's standard JSON encoder does not
serialize.

This is an artifact-layer failure, not a mathematical failure. No accepted
result was persisted and no conclusion was drawn from this run.

Correction: convert every factor multiplicity to a built-in `int` both in the
factorization record and in the factor-role ledger. The exact computation is
rerun in full; the accepted artifact must be deterministic across two runs.
