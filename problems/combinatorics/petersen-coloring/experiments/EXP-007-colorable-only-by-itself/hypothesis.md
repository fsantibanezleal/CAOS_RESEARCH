# EXP-007 - is the 52-vertex counterexample colorable only by itself? (and a quotient route to smaller counterexamples)

Declared 2026-09-18 before experiment code was run. Round 2. Backlog PCB-017.

## Question

For graphs `G`, `H`, an `H`-coloring of `G` is a map `f : E(G) -> E(H)` with adjacent edges
receiving distinct images and `f(d_G(v)) = d_H(u)` for some vertex `u` of `H`, for every vertex
`v` of `G` (Ma, Mattiolo, Steffen, Wolf, Combinatorica 45 (2025), Article 16, arXiv:2305.08619,
Section 1 `[V]`; graphs may have parallel edges but no loops `[V, their Section 2]`). `H_3` is
the unique inclusion-wise minimal set of connected bridgeless cubic graphs coloring every
connected bridgeless cubic graph, and by their Theorem 3.7 `[V]` the following are equivalent
for a connected bridgeless cubic `G`: `G` is in `H_3`; the only connected bridgeless cubic graph
coloring `G` is `G` itself; `G` cannot be colored by a bridgeless cubic graph of smaller order.

Goedgebeur, Jooken, Macajova, Mattiolo, Mazzuoccolo, Ulyanov (arXiv:2608.10028v3, 2026-09-11,
Section 5.4 `[V]`) ask whether their 52-vertex counterexamples are colorable only by
themselves, and note that the question is tied to whether they are smallest counterexamples.
Decide it for `G52`: for each even `k < 52`, is there a connected bridgeless cubic multigraph
`H` on `k` vertices with an `H`-coloring of `G52`?

## Why both outcomes matter

- If some `H` exists, then `H` has no Petersen coloring either (the relation "colors" is
  transitive, so `P` coloring `H` would give `P` coloring `G52`): `H` is a counterexample to the
  Petersen coloring conjecture on fewer than 52 vertices, improving the upper bound of the open
  window `[40, 52]` of v3 Problem 8. It would be certified independently by the EXP-001 route.
- If no `H` exists for any even `k < 52`, then `G52` belongs to `H_3`: it is colorable only by
  itself. This answers the v3 Section 5.4 question for this graph with checkable certificates.

## Method

One CNF per target order `k`, with the target multigraph unknown:

- target structure: each target vertex `i < k` has three slots; a perfect matching `p` on the
  `3k` slots with no pair inside one vertex (no loops; parallel edges allowed) is the edge set
  of a cubic multigraph `H`;
- the map: `x(v,i)` (vertex `v` of `G` is sent to `i`), and at every `v` a bijection `z` between
  its three incident edges and the three slots of its image, so the star of `v` maps onto the
  star of `i` with distinct images;
- consistency along each edge `uv` of `G`: the slot used at `u` and the slot used at `v` are the
  same slot or are matched by `p` (the same edge of `H` seen from either end);
- symmetry breaking: target vertices are numbered in order of first use (vertex 0 of `G` goes
  to 0; class `i+1` is first used only after class `i`), and the founder of each class fixes the
  slot order; unused target vertices are allowed (colorings need not be surjective) and sit at
  the end;
- connectedness and bridgelessness of `H` are enforced lazily: a model whose `H` is
  disconnected or has a bridge yields the sound clause "some further slot pair crosses the
  offending side", and the solve repeats.

A SAT answer is decoded and re-verified by an independent checker (`H` cubic, loopless,
connected, bridgeless; `f` an `H`-coloring from the definition), and `H` is then refuted for
Petersen colorability by the EXP-001 encoding with a checked proof (it must be a
counterexample). An UNSAT answer carries a DRAT proof checked by drat-trim; the lazily learned
clauses are logged with the cut that justifies each.

## Fixed objects

`G52` (`data/gjmmm-52.edgelist`). Controls: the Petersen graph with every even `k < 10` (must
be UNSAT: by Kardos, Macajova, Zerafa as cited in v3 Section 5.4 `[U, cited through v3]` the
Petersen graph is colored only by itself or by graphs with a bridge); the flower snark `J5`
with `k = 10` (must be SAT, since `J5` has a Petersen coloring, and the decoded `H` must pass the
checker); `K4` with `k = 2` (SAT: the three parallel edges; every 3-edge-colorable graph is
colored by it).

## Falsifiable predictions

- P1: controls behave as stated.
- P2 (the question): committed expectation, moderate confidence: every even `k` from 2 to 50 is
  UNSAT for `G52`, so `G52` is in `H_3`. A SAT instance REFUTES the expectation and produces a
  new smallest known counterexample.
- P3: for every SAT instance (controls included) the independent checker accepts the decoded
  pair `(H, f)`; for every UNSAT instance drat-trim verifies the proof.

## One-sidedness

UNSAT for all `k` with verified proofs is a theorem about `G52` (membership in `H_3`),
unconditional on any census. SAT is a positive certificate. TIMEOUT decides nothing for that
`k`; the verdict then reports exactly which orders are decided.

## Premise dependencies

- Theorem 3.7 of Ma-Mattiolo-Steffen-Wolf `[V]` (read in the arXiv version).
- EXP-001 CONFIRMED (`G52` has no Petersen coloring), used only to interpret a SAT outcome.
- The v3 lower bound 40 is NOT used: all even orders from 2 are tested here.

## Invariant-first note

A covering-type count already excludes foldings without identified adjacent vertices (they
would be coverings, forcing `k` to divide 52 with quotient at least 2, so `k <= 26`), but
identified adjacent vertices are allowed in `H`-colorings, so no single invariant decides the
question.

## Compute budget and kill criterion

CPU only, one process per `k` in parallel (at most 12 at a time). Wall cap 6 hours per `k`;
whole experiment 24 hours. Each instance logs flushed progress and writes its result JSON on
completion; undecided orders are listed.

## Verdict rules

- CONFIRMED (of P2) if P1 and P3 pass and every even `k` from 2 to 50 is UNSAT with a verified
  proof.
- REFUTED (of P2) if some `k` is SAT with a checker-accepted `(H, f)` and `H` is refuted for
  Petersen colorability with a verified proof: a new counterexample on `k` vertices.
- INCONCLUSIVE for the orders that hit the cap.

## Addendum declared 2026-09-18 09:25, before any target instance ran

Tooling measurement on the controls and one timing probe (`G52`, `k = 44`, stopped after 22
rounds, no decision used): each restart of the external solver costs about 8 seconds at this
size and the models found first have the unused target vertices in a separate component.
Method changes, fixed before the target runs:

- the lazy cut loop runs in-process with PySAT's CaDiCaL 1.9.5 (`run_inc.py`); when it reports
  UNSAT, the FINAL formula (base, static attach clauses, every learned cut) is written out and
  certified by WSL CaDiCaL with a DRAT proof checked by drat-trim, so the certificate does not
  depend on the in-process solver;
- a static, sound clause family is added: if class `i` is the first unused class, some slot
  pair joins a class below `i` to a class from `i` on (a connected target cannot have the used
  classes closed under the matching while unused vertices exist);
- the controls were re-run under the new runner with identical outcomes (Petersen `k = 6, 8`
  UNSAT with verified proofs after 82 and 139 rounds; `J5`, `k = 10` SAT with a checker-accepted
  target that is itself Petersen colorable).

## Addendum 2 declared 2026-09-18 09:59 (commit 755fe329), after attempt 1 was stopped without any decision

Attempt 1 (the runner above, all 25 orders, ten at a time) was stopped after about 35 minutes:
the ten orders that had started (`k` from 32 to 50) had each learned 1,800 to 2,400 lazy cuts, more
than 95 percent of them bridge cuts, at roughly one cut per second with no sign of convergence; no
order was decided and no outcome is used. Logs are kept under `artifacts/attempt-1/`. Diagnosis:
unused target vertices form a free part of `H` that the graph `G` does not constrain, and the
solver enumerates its bridged completions one by one.

Method change, fixed before any new target run, justified by two lemmas proved in
`context/2026-09-18-hcoloring-reduction-lemmas.md`:

- Lemma A (fiber parity): all fibers of the vertex map have the same parity. Encoded with one
  variable `q` and one XOR chain per target vertex.
- Lemma B (unused vertices): if some connected bridgeless cubic multigraph on fewer than `n`
  vertices colors `G`, then one with at most one unused vertex does (splitting lemma). Encoded as
  the unit clause "the last but one class is used".
- For `k - 1 > n/2` the even mode is impossible, so `q` is fixed to odd.

The reduced formula is therefore equisatisfiable with the question "is `G` colored by some
connected bridgeless cubic multigraph on at most `k` vertices in the modes O, E0, E1", and the
union over all even `k < 52` still decides the original question. One-sidedness is unchanged,
except that an UNSAT verdict now also depends on Lemmas A and B (proofs on file) and on the
splitting lemma as cited there.

New control, added to P1: the reduced and the unreduced runner must agree on every even
`k < n` for the small cubic graphs available in `pcclib.graphs`: `K4`, the prism, the Petersen
graph and the flower snark `J5` (wording of this sentence corrected right after the commit, before
any run); a disagreement refutes a lemma or exposes an encoding error and blocks the target runs.
Budget and verdict rules are unchanged (6 hours per order, 24 hours overall, counted from the
restart).

## Addendum 3 declared 2026-09-18, before any instance on the graphs named here ran

House of Graphs became reachable on 2026-09-18. Entries 57244 and 57237, 57279 are isomorphic to
our `G52`, `G112`, `H112` (checked); two graphs are new to this record and were added to `data/`:
`G52b` (entry 57278, the second 52-vertex counterexample of v3, digest `d30a423a...1477`) and `G68`
(entry 57280, the 68-vertex counterexample, digest `19c7c22a...5ab2`); both are cubic, girth 5,
edge connectivity 3, cyclically 4-edge-connected.

Scope extension, same reduced method, same certificates, 6 hours per order:

- `G52b`: every even `k < 52`. Committed expectation: all UNSAT (it is in `H_3`), moderate
  confidence, by analogy with `G52`.
- `G68`: every even `k < 68`. No committed direction: a SAT order would show that the 68-vertex
  graph is colored by a smaller counterexample (possibly one of the 52-vertex graphs at `k = 52`,
  possibly a new one below 52); all UNSAT puts it in `H_3`.
- `G112`, `H112`: every even `k < 112`, run after the smaller graphs, largest formulas about
  18 million clauses; same reading. For these, before the full sweep, the single order `k = 52` is
  run first as a probe of "colored by a 52-vertex counterexample".

Before the target runs on a new graph, EXP-001-style refutations of its Petersen colorability are
reproduced with our encoder (P0: `G52b` and `G68` have no Petersen coloring, UNSAT with verified
proofs), since only our own certificate makes the reading of a SAT outcome independent.

## Addendum 4 (2026-09-18 13:05): tooling only

Every instance decided so far was unsatisfiable without a single lazy cut, so the two-step route
(in-process solve, then an external solve of the same formula with a proof) spends a third of its
time on a solve that adds nothing. From this point a newly started instance first solves the
reduced formula once, externally, with a DRAT proof; UNSAT is certified by drat-trim as before; a
SAT answer falls through to the incremental loop unchanged. Instances already running are not
restarted. The formula, the certificates and the verdict rules are unchanged; the change was
tested on `J5` with `k = 14` (UNSAT, verified) and `k = 12` (SAT, checker-accepted target).

## Addendum 5 (2026-09-18 13:55): how the verdict will use the lower bound 40 of v3, stated before the mid-range orders end

State: for `G52` the orders 2 and 30 to 50 are refuted with verified proofs; 26 and 28 are
unsatisfiable in-process and in certification; the orders 4 to 24 have been solving for more than
three hours and may reach the 6-hour limit undecided. For `G52b` the orders 46 to 50 are refuted
and 40 to 44 are in progress.

The original premise list says that the lower bound 40 of v3 (Observation 9: a smallest
counterexample has at least 40 vertices, from their exhaustive check of the weak snarks on 38
vertices) is not used. That stays true for the unconditional statement. Since any graph that
colors a counterexample is a counterexample, and a counterexample with parallel edges reduces to a
smaller one (suppress the 2-edge cut around a digon; the two cut edges carry equal labels in any
Petersen coloring), Observation 9 excludes every target order below 40. The verdict will therefore
state two results and keep them apart:

- (U) unconditional, from our certificates alone: the list of target orders refuted with verified
  proofs, whatever it is when the limits expire;
- (C) conditional on Observation 9 of v3 `[V as a statement of v3; their computation is not
  reproduced here]`: membership in `H_3` as soon as every even order from 40 to `n - 2` is refuted.

For `G68`, `G112`, `H112` the runs are restricted accordingly to the orders from `n - 2` down to
40, largest first.

## Incident note (2026-09-18 14:10)

The shell driver of attempt 1 survived the stop command issued at 09:55: only its children had
been killed, and it kept starting instances with the code that was on disk when each one started.
Nine instances started at 09:57:09 ran the attempt-1 (unreduced) code for four hours, shared log
files with the reduced instances of the same orders (12 to 30), and took about a third of the
machine. They were found from the process list at 14:08 and killed together with the driver. No
result file came from them: every result file on disk carries `"reduced": true` and its own
verified certificate. The reduced instance of order 14 had died at start (its log stops after the
first line) and was restarted at 14:10 with a fresh 6-hour limit. The logs of orders 12 to 30 may
contain interleaved lines from the two writers and are not used as evidence; the result files are.
