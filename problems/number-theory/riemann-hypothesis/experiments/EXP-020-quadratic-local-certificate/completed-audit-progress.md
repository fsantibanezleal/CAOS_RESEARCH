# Actual completed-output validation progress

The full independent cover audit passes all 96 reports and completed
checkpoints, including exact source/table/domain/accounting bindings.
The completed interval execution has 107,752,902 nodes; its trust base
remains the frozen Python/FLINT/Arb verifier.

The separately declared 512-cell native input pilot passed both tables
in 0.977 seconds, projecting 116.46 seconds for 61,029 cells. It satisfies
the 600-second admission gate. One full-table audit is admitted. Twelve
actual-output corruption checks and the exact transfer will run alongside
it on separately declared one-CPU paths, preserving the original output.
All final checks subsequently passed. The actual-output controls rejected all
12 corruptions and revalidated unchanged originals. The exact transfer gives
3997934614153/4775507750000. The native kernel/Taylor recomputation enclosed
both tables on all 61,029 closed cells in 225.276 seconds, within 600 seconds.
The exact-byte archive passed CRC/member/hash checks and reproduced identical
cover and transfer results after extraction. Its SHA256 is
91be4798774837bc16007a8236a692078e825ffb1c8dfa476c05d3c733b17879.
See verdict.md for the completed mathematical result and its trust boundary.
