# EXP-005 pow2: paused 2026-08-20 to free CPU for the stratum atlas

pow2-08b64r was holding 10 threads on a 32-thread machine while eight
interval coverings (the stratum theorem's primary line) shared the rest.
It is checkpoint-protected (checkpoint-pow2-08b64r.state, 1.2 GB, written
by --saveas), so pausing costs only the work since the last checkpoint.
RESUME with: bash ~/exp005b/run08-resume.sh pow2-08b64r 64 10
(or relaunch-both.sh, which also restarts pow3 - but pow3 stays PARKED
per the 2026-08-20f addendum: four launches, zero checkpoints).
