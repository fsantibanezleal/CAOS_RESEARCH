# EXP-011 verdict: CONFIRMED: $z_{\max}(8) = 6$: the census is decision-complete through depth 8

Runs 2026-08-20: validate 185 s; build7 2 h 50 m; scan8 smoke 463 s;
scan8 final 6 h 48 m (20 workers). Artifacts: `artifacts/pipeline.json`,
`artifacts/scan8_smoke.json`, `artifacts/scan8_final.json`,
`artifacts/polys.manifest.md`; the depth-7 frontier itself is retained as
a data asset (see below).

## The theorem this completes [MV]

$$z_{\max}(\tau) = 1, 2, 3, 3, 4, 5, 5, 6 \qquad (\tau = 1..8),$$
decision-complete at every depth, all final gates. Consequences:
- **No 8-gate program of ANY shape has 7 distinct integer roots** (zero
  $z \ge 7$ results across all $2 \times 10^{11}$ last-gate
  applications): the final-$\pm$ residual (TCB-029) is DECIDED, closing
  what EXP-006/007 left open and what two solver engines could not
  search (EXP-008/010).
- The minimal $\tau$ for 7 distinct integer roots is 9 or 10 (lower
  bound this census; upper bound the explicit 10-gate witness).
- The growth function through depth 8: two plateaus then a step:
  the six-rooters that appear at 8 (the EXP-006 witnesses) remain the
  records; no third plateau value is skipped.

## The construction behind it (method record)

- **build7**: the first complete construction of the depth-7 reached-set
  frontier: $|\mathcal{F}_7| = 1{,}048{,}460{,}912$ states (prediction
  window $[0.6, 1.5] \times 10^9$ confirmed), by out-of-core
  hash-partitioned expansion (2.43B raw 28-byte rows, 256 partitions,
  independent in-RAM dedups; identical rows land in the same partition
  by construction). INTERNAL CROSS-ANCHOR EXACT: the build's new
  depth-7 polynomial count, 2,013,706, equals EXP-004's independently
  computed value to the digit.
- **scan8**: multiprocess last-gate scan (Lemma of EXP-003 at depth 8)
  over every stored state; per-partition results, resumable; the
  histogram is per op-application (with multiplicity) per the
  pre-declared amendment; $z_{\max}$ and the (empty) $z \ge 7$ witness
  collection are exact.

## Validation ledger (everything gated before trust)

validate stage reproduced 25,844,905 / 134,494 exactly (185 s);
scan8 smoke reproduced $z_{\max}(7) = 5$ with zero six-rooters over the
full depth-6 frontier (463 s); build7's frontier6 gate and the
2,013,706 cross-anchor; the underlying tclib layer carries the
Markstroem 14/14 and sympy 284/284 anchors from rounds 1-3.

## Prediction scorecard

All four committed predictions CONFIRMED (validate gate; $|\mathcal{F}_7|$
window; $z_{\max}(8) = 6$: the emptiness-commitment record moves to
2-for-6; seven-root threshold in $\{9, 10\}$).

## Data assets

The depth-7 frontier (256 uniq files, ~29 GB) and the poly catalog
(polys.pkl, sha256 in the manifest) relocate to
`E:/_Datos/caos-research/tau-conjecture/` as reusable assets (the
depth-9 question and any future instrumentation replay from them);
the repo keeps manifests only (D6).

## How could this be wrong?

The chain rests on: the last-gate lemma (proved), the build's exactness
(anchored by the 2,013,706 cross-match: a frontier error would have to
conspire to preserve exactly the independently known new-poly count),
partition-dedup completeness (identical rows cannot land in different
partitions: the hash is a function of the row), and the scan's
arithmetic (sympy-cross-checked layer; smoke-gated end to end at the
known-answer level one depth down). Residual risk is a shared tclib
blind spot, hedged as before.

## Consequences

- TCB-005 DONE (the backend exists and is now the standard engine);
  TCB-029 RESOLVED; TCB-028 UNBLOCKED: paper v0.03 ships now with the
  full depth-8 resolution, per its declared gate.
- New standing question: $z_{\max}(9)$ / the 7-root threshold decision
  (build8 would be ~$4 \times 10^{10}$ states, ~1.1 TB of shards:
  out of scope on this disk; the {9,10} window may instead fall to a
  construction hunt with the corrected cost model).

## Addendum 2026-08-25 (adversarial validation pass)

The frontier had no hash manifest, only the catalog did, while the manuscript
claimed manifests for both assets. The missing one is now generated:
`artifacts/frontier7.manifest.md`, 256 per-file SHA-256 digests plus an
aggregate fingerprint 7a3b4484fa33498960885781a0662efcac8b7929f13c350c4063cdf96baaf174.
Its state count is DERIVED from the file sizes (29,356,905,536 bytes / 28) and
comes to 1,048,460,912, matching the figure this experiment reported, so the
asset now certifies its own headline number rather than being described by it.

The catalog manifest was also found to state 2,161,169 entries where the file
holds 2,161,049; its hash and size matched exactly, so the asset had not
drifted and only the prose was wrong. Corrected in place.
