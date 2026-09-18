# EXP-013 verdict: CONFIRMED (windowed): no additive nine-gate seven-rooter with all roots in [-32, 32]

The production scan finished on 2026-08-25 (last partition written 20:21 local); this verdict and
its completeness audit are dated 2026-09-18. Artifacts: `artifacts/parts_final/part000..255.json`
(one record per frontier partition), `artifacts/audit.json` and
`artifacts/audit-output-2026-09-18.txt` (the audit below), `artifacts/gate.json` and
`artifacts/parts_gate/` (the pre-production gate), `artifacts/parts_regress/` (the engine
regression).

## Result

Over ALL 1,048,460,912 depth-7 states, every one-gate extension v8, every operand b of the
state and both signs, at threshold 7 on the window W = [-32, 32]:

    partitions scanned            : 256 of 256
    states scanned                : 1,048,460,912
    candidates promoted to exact  : 1,272,725
    exact seven-rooters (hits)    : 0

So no 9-gate constant-free program whose final gate is an addition or a subtraction computes a
polynomial with 7 distinct integer roots that all lie in [-32, 32].

## Completeness audit (`audit.py`, 7 checks, all PASS)

1. `parts_final` holds exactly part000.json to part255.json, one per frontier partition.
2. Every record is well formed (part, states, hit_count, hits, promoted) and names its own
   partition.
3. Each partition's scanned state count equals the state count of its frontier file uniqNNN.bin
   in EXP-011's SHA-256 manifest (`EXP-011-depth8-pipeline/artifacts/frontier7.manifest.md`,
   file size over 28-byte rows): no partition was scanned partially.
4. The scanned states total the manifest's 1,048,460,912.
5. No partition reports a hit (hit_count = 0 = len(hits) everywhere).
6. Partitions 0 and 1 equal the batched engine's exact regression records.
M. The manifest itself lists 256 partitions that sum to its stated total.

210 of the 256 records were committed during the run; the last 46 (written after the final
commit of 2026-08-25) were copied from the run's working tree on 2026-09-18, and the 210
committed ones were byte-identical to the working-tree copies.

## Scorecard

- Prediction 1 (production finds no additive 9-gate 7-rooter): CONFIRMED, windowed as declared in
  the soundness scope: the result excludes only witnesses whose seven roots all lie in
  [-32, 32].
- Prediction 2 (with EXP-012, the seven-root threshold is 10, windowed): CONFIRMED in the
  declared windowed form. With EXP-012 (the multiplicative last gate, unconditional) and EXP-011
  (z_max(8) = 6, so a 9-gate 7-rooter's last gate involves v8), a 9-gate program computing a
  polynomial with 7 distinct integer roots must have an additive last gate and at least one
  root outside [-32, 32]. By the confinement lemma (paper, Lemma confine) its trailing
  coefficient then satisfies |c| >= 396, and |c| >= 1188 when 0 is not a root. EXP-014 measured
  such window-limited candidates (degree >= 7 and |c| beyond the bound) at 0.0019% of the
  nonzero additive candidates, on a sample of 6.4 million from four partitions. The threshold is
  therefore 10 unless that residual class holds a seven-rooter; strictly, it stays in {9, 10}.
- The pre-registered growth rhythm (z_max(9) = 7) is refuted in the windowed sense on both
  halves of the ninth gate: z_max(9) = 6 for every program whose seven roots would lie in the
  window.

## Adversarial validation record

- **Known-answer gate before production** (hypothesis, "Gate"): threshold 5 on 20,000 states of
  partition 0 returned 41 hits, each promoted and verified exactly, so the pipeline finds
  witnesses when they exist; a zero at threshold 7 is not an instrument artefact of that kind.
- **Engine regression**: the batched engine reproduced the reference engine exactly on
  partitions 0 and 1 (states, hits and promoted counts) before it contributed any result; check
  6 of the audit re-confirms it against the final records.
- **Completeness against an independent record**: the per-partition state counts are checked
  against the frontier manifest generated from the frontier files themselves (EXP-011), not
  against the scan's own logs.
- **Soundness of the filter** (hypothesis, "Method"): f = v8 +- b vanishes at r only if the
  residues agree, so a seven-rooter inside the window cannot be missed by the modular filter;
  identically-zero candidates are discarded only when both degrees are below 65, so a nonzero
  high-degree candidate agreeing on the whole window is still promoted.

## How could this be wrong?

- The result is windowed. A seven-rooter with a root outside [-32, 32] is not excluded; the
  confinement lemma and EXP-014 bound where it could be (|c| >= 396, about 0.002% of the space
  in a four-partition sample), but that residual class has not been scanned exhaustively.
- The reduction rests on EXP-011 (z_max(8) = 6) and on the frontier being the complete depth-7
  reached set; both are earlier verdicts, not re-derived here.
- One implementation lineage: the two engines share the mathematics, and agree on the two
  regression partitions only.
- The run survived several operational incidents (processes killed mid-partition, relaunches).
  Records are written only when a partition completes, and check 3 shows every partition's state
  count equals its frontier file's, so no partial partition was recorded.

## Consequences

- The paper's statement "the additive case remains open" is replaced by this windowed theorem,
  its reduction to the confined residual class, and the unchanged strict window {9, 10}
  (census paper v0.05).
- Queued: an exhaustive pass over the window-limited residual (degree >= 7 and |c| above the
  confinement bound), with each survivor root-counted exactly over the divisors of its trailing
  coefficient, as EXP-014 proposed. It would decide the threshold outright.
- Operational: the scheduled task `tau_keepalive` (every 15 minutes) was still firing on
  2026-09-18, three weeks after the last partition, and logged "nothing to launch" each time;
  it was disabled on 2026-09-18 (not deleted).
