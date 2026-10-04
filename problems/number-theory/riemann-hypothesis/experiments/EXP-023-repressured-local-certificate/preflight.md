# EXP-023 preflight and proof scope

2026-10-03. The hypothesis was pushed as f2e1e7ec and bounded RH-F13 admission
as 0de0e59d before implementation. RH-F4 remains the sole active focus.

Three meaningful controls pass: exact Fraction block conditions and the
declared gain gate; directed rounding over the new bounded domain; and a
real verifier/worker smoke instance that writes a partial checkpoint,
prints flushed progress, interrupts, resumes and agrees with a fresh
traversal. The synthetic smoke has seven nodes, two splits and depth two;
it does not certify the nine-point inequality. The existing quadratic
completion-of-squares and adversarial accounting tests are also required.

The pressure expression uses a sum of up to eight cell indices. Therefore
the new wrapper audits all 417849 possible integer sums 0 through 417848,
in addition to target and weight enclosures. This strengthens the originally
declared single-index audit. EXP-020's corresponding 488161 sums are checked
separately without modifying its frozen runtime source.

The source baseline contains 60853 cells in big-endian IEEE binary64 tables.
The new run copies exactly the first 52240 cells only after verifying both
complete baseline hashes and its frozen source binding. No new kernel
enclosures are generated. A preliminary prepare-only directory,
`exp023-repressured-local-20261003`, is retained outside Git: it binds the
earlier single-index audit and has no traversal or scientific result.
The strengthened runtime uses the separate
`exp023-repressured-local-v2-20261003` directory. It must not resume the
preliminary binding. Existing incompatible directories are rejected.

The first actual shard-0 pilot receives one CPU for at most twenty minutes
after preparation. Partial state at budget is preserved and audited before
any full-cover decision. Only all 96 reports, complete checkpoints,
independently reconstructed exclusions and domain partition, exact transfer
and the separately attributed analytic premises can license the proposed
distinct-strip bound. The independent auditor imports neither the verifier
nor the numerical kernel. Interval execution remains an explicit trust base.

This changed-pressure certificate cannot establish the original EXP-018
local inequality. Source-related inputs and published manuscripts remain
immutable. EXP-022 bounds what this fixed pressure family can achieve;
finite candidate search alone supports no stronger zero-proportion claim.
