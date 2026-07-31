# EXP-126 pre-run redirect: reuse the identical exact section

Recorded 2026-07-30 after the hypothesis commit and before implementation or
run.

The invariant-first identity check found that the EXP-125 `selected_rows.F6`
list is exactly equal, entry by entry, to `selected_rows.F3`. It is not equal
to the persisted \(F_7\) basis. Therefore the characteristic-zero maximal
minor requested by EXP-126 is not a new determinant: it is the same section
already reconstructed from all 87 SCC blocks, checked by four direct exact
determinants, and persisted in EXP-125.

Re-running the isolated symbolic worker would repeat about 40 seconds of
accepted exact arithmetic without adding an independent algorithm or a new
certificate. EXP-126 will instead:

1. verify the equality of the two row lists;
2. verify the SHA-256 hashes of the accepted EXP-125 result and worker
   artifacts against the verdict;
3. rebuild the exact anchor and SCC profile for the selected rows;
4. reload the accepted exact determinant section and reproduce its invariant
   and graph numerator;
5. rerun the four direct exact determinant controls;
6. perform the new \(F_6\) quotient, norm, independent multiplication-matrix
   check, and boundary diagnostics.

This redirect changes no success criterion. It removes redundant compute and
strengthens provenance by requiring exact artifact identity before reuse. If
any hash, row-basis, anchor, SCC, graph-numerator, or direct-control check
fails, the run stops rather than silently reusing the section.
