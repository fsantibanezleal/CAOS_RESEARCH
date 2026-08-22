# EXP-011: the full depth-8 census via an out-of-core pipeline (resolves $z_{\max}(8)$)

Declared 2026-08-20, before any run. Actions TCB-005 as re-ranked by
EXP-008/009: no unproved pruning (EXP-009 measured the symmetry quotient
unsound), pure engineering: hash-partitioned external dedup on the E:
scratch disk plus a multiprocess last-gate scan.

## Stages, each with its own gate and checkpoint

1. **validate**: run the identical out-of-core machinery one level down
   (depth-5 frontier in RAM, expand, shard, partition-dedup): MUST
   reproduce exactly 25,844,905 depth-6 states and 134,494 new depth-6
   polynomials (EXP-004 anchors). Nothing downstream runs until this
   gate passes.
2. **build7**: expand the depth-6 frontier (rebuilt in RAM, gate-checked)
   to the depth-7 frontier out-of-core: successor states as 28-byte
   binary rows, hash-partitioned into 256 files (identical rows always
   land in the same partition, so partitions dedup independently in
   memory), producing `frontier7/part*.bin` plus the exact
   $|\mathcal{F}_7|$ count and the depth-7 poly catalog additions.
3. **scan8**: stream every depth-7 state through the last-gate scan
   (Lemma of EXP-003, applied at depth 8) with a multiprocess pool:
   EXACT $z_{\max}(8)$, the full z histogram at depth 8, and record
   witnesses with provenance. This subsumes the final-$\pm$ residual
   (TCB-029): the scan covers all final gates.

## Falsifiable predictions (committed)

1. The validate gate passes exactly.
2. $|\mathcal{F}_7|$ lies in $[6 \times 10^8, 1.5 \times 10^9]$
   (extrapolating the ~30-33x per-level growth).
3. $z_{\max}(8) = 6$ (with EXP-006/007 this means the final-$\pm$ case
   adds nothing). Emptiness-flavored commitment number six; the record
   is 1-for-5, so confidence is stated MODERATE and the machine decides.
4. The minimal $\tau$ for 7 distinct integer roots is 9 or 10 (it is
   $> 8$ iff prediction 3 holds; the 10-gate witness stands).

## Premises (P3)

EXP-004's depth-6 anchors; EXP-003's last-gate lemma; EXP-009's verdict
(no symmetry pruning used); tclib arithmetic (sympy-cross-checked).

## Budgets and kill criteria (P6)

validate: 1.5 h cap. build7: 24 h detached, checkpoint per partition
flush; disk guard: abort if E: free space falls below 60 GB. scan8: 48 h
detached, 20 workers, per-partition result checkpoints; resumable by
partition. Any stage over budget: record INCONCLUSIVE(budget) with
coverage; partial scan coverage still yields a valid LOWER bound on
$z_{\max}(8)$ (reported as such, never as the census value).

## One-sidedness

A completed scan8 is decision-complete for depth 8 (exact
$z_{\max}(8)$, all-gate). Partial coverage gives lower bounds only.
Nothing asymptotic follows either way.

## Amendment (2026-08-20, before scan8 runs): histogram scope

scan8's z histogram is counted PER OP-APPLICATION (with multiplicity
across states and duplicate results); globally deduplicating the ~10^11
depth-8 op results is out of scope for this experiment. z_max(8), the
z >= 7 witness collection (with provenance), and the census DECISION are
exact and unaffected: z_max is a maximum, not a count. Distinct-poly
counts at depth 8 would require a further external-dedup pass and are
recorded as future work, not silently claimed.
