# Completed-cover validation declaration

The frozen twenty-four-worker cover has completed all 96 shards, exiting
successfully. The independently reconstructed input/domain/accounting audit
passes 107,752,902 nodes, 53,876,323 splits and 53,876,579 prunes over
256 initial boxes. This does not by itself complete the result's validation.

Before implementation, declare three final checks for this actual completed
output. They do not alter the target or frozen runtime, which is also protected
because the separate EXP-023 continues.

1. Run twelve actual-output corruption controls on isolated ordinary copies,
   using EXP-019's independent auditor with the explicit EXP-020 target.
   Recompute transport hashes for semantic corruptions. Budget: 180 seconds
   on one CPU; originals must be byte-identical after controls.
2. Apply the already successful native kernel-first whole-cell input audit
   to both full EXP-020 tables, now 61,029 cells. Its analytic identities
   and remainder proof are unchanged; the copied audit has a separately bound
   source and declaration. A 512-cell thirty-second pilot precedes one full
   run if its projection is <=600 seconds. Full run budget: 600 seconds on
   one CPU. All cells and both tables are required.
3. Independently reconstruct the exact mixed-Gram transfer at m=958,
   tau=2409/1000, c=3409/1000 with delta=3051/500000, pressure=1/2500 and
   the certified native window constant. Require the full cover before issuing
   a receipt. Then build a scoped exact-byte runtime archive, require the
   twelve corruption controls and native full-table receipt, extract it and
   rerun the standard-library full-cover and exact-transfer auditors. Archive
   budget: 120 seconds. Preserve physical source bytes and original evidence.

These checks strengthen accounting, input and transport validation; they do
not provide a separate kernel for the interval execution, an external referee
or a formal end-to-end proof. The universal stronger local inequality would
also imply the weaker EXP-018 premise, without retroactively describing
EXP-019's suspended replay as completed. Manuscript coherence and source
overlap must still be reviewed. The external vector-pressure EXP-025 remains
a separate attributed-input transfer, and EXP-023 remains incomplete.
