# EXP-003: z_max(6) exactly, by the last-gate scan (no depth-6 frontier stored)

Declared 2026-08-01, before the run. Unblocks the depth-6 question that
EXP-002's verdict declared out of naive reach, via a method lemma instead
of raw compute.

## Question

The exact value of $z_{\max}(6)$, and hence whether the minimal $\tau$
with 5 distinct integer roots is 6 or larger (the Chebyshev-tower gives
$\le 7$ unconditionally: $G_2 = C(x)^2 - C^2(x)^2$ has root set
$\{0,\pm1,\pm2\}$ at 7 gates; derivation note 2026-08-01).

## The last-gate lemma (method contribution, [D], proved here)

Let $\mathcal{F}_d$ be the set of normalized reached-set states of depth
$d$ (our BFS frontier). CLAIM: every $f$ with $\tau(f) = d+1$ arises as a
single gate $a \circ b$ with $a, b$ operands (inputs or values) of some
state in $\mathcal{F}_d$.

Proof: take an optimal program for $f$ of length $d+1$. WLOG it is
normalized (no repeated values: deleting a duplicating gate and rewiring
shortens the program, contradicting optimality; no computed 0 and no
computed copy of an input: same deletion argument, using that a 0 or
input-duplicate operand can be replaced by the free input, EXP-001
hypothesis lemmas 1-2). Its first $d$ gates then form a normalized
reached-set state of depth $d$, i.e. an element of $\mathcal{F}_d$, and
the final gate is one op over that state's operands. QED.

Consequence: $z_{\max}(d+1) = \max(z_{\max}(d), \max\{z(f)\})$ over the
scan of one op over every state of $\mathcal{F}_d$, deduplicating results
and skipping polynomials already seen at depth $\le d$. Memory stays
$O(|\mathcal{F}_d| + \#\text{distinct polys})$; nothing of depth $d+1$ is
stored beyond the poly dictionary. This buys exactly one depth level past
any exhausted frontier.

## Method

`run.py`: recompute the depth-5 frontier with tclib (`return_frontier`),
verifying EXP-002's counts en route (states 9/98/1462/29506/778087: an
internal regression gate); then `last_gate_scan` over the 778,087 states;
exact root counts on the deduplicated new polynomials; record gallery +
2-adic spectra; witness reconstruction for the depth-6 records (bounded
DFS, depth 6).

## Falsifiable predictions (committed before the run)

1. The scan's deduplicated new-polynomial count at depth 6 is on the
   order of $10^5$ (extrapolating the observed ~9x growth of new polys:
   9, 34, 177, 1249, 11377).
2. $z_{\max}(6) = 4$: no 6-gate program attains 5 distinct integer roots
   (our cheapest known 5-rooter costs 7 gates; we predict the census
   confirms 6 is not enough, making the minimal $\tau$ for 5 roots
   exactly 7 when combined with the tower construction).

## One-sidedness

The scan is decision-complete for depth 6 (exact $z_{\max}(6)$ either
way, given the lemma). If prediction 2 fails (a 6-gate 5-rooter exists),
that is a mechanism DISCOVERY, recorded in full; the experiment itself is
then still CONFIRMED as a census (the prediction verdict is reported
separately, as in EXP-002). Nothing asymptotic follows either way.

## Premise dependencies (P3)

- The last-gate lemma above [D, self-contained].
- EXP-001/002 verdicts (anchored enumerator; depth-5 frontier counts).
- tclib test suite green, now including the Chebyshev-tower checks.

## Invariant-first note (P5)

Degree cap $2^6 = 64$ decides nothing. The tower lemma (context note)
excludes ONE mechanism class (single-inner-map DOS towers) from beating 5
roots at any depth, but does not bound 6-gate programs in general; no
cheaper decider found, so the scan is justified.

## Compute budget and kill criterion (P6)

- Smoke (P2): scan over the depth-4 frontier (29,506 states) must
  reproduce $z_{\max}(5) = 4$ and the 11,377 new-poly count from EXP-002
  within seconds, printing progress and writing the checkpoint.
- Budget: 60 minutes wall. Expected: frontier rebuild ~1 min; scan
  778k states x ~130 ops ~ 10-25 min single-core; root counting seconds
  (new-poly dedup keeps it ~1e5).
- Kill: deadline at 50 min inside the scan: checkpoint, report depth 6
  INCONCLUSIVE with states-scanned count; the standing bounds remain
  $4 \le z_{\max}(6) \le z_{\max}(7) \le \dots$ and min-$\tau$(5 roots)
  in $\{6, 7\}$.

## Success and failure criteria

- CONFIRMED: scan completes; $z_{\max}(6)$ exact; predictions scored.
- INCONCLUSIVE: kill hit.
- REFUTED (tooling): smoke scan fails to reproduce EXP-002's depth-5
  values (then nothing downstream is trusted).
