# EXP-010 - is there a sublinear bound on abnormal edges for cyclically 4-edge-connected cubic graphs?

Declared 2026-09-18 before any experiment code was run. Round 2. Backlog PCB-024.

## Question

Mattiolo, Mazzuoccolo, Mkrtchyan (Bull. Inst. Combin. Appl. 92 (2021) 78-90, arXiv:2104.09241,
read 2026-09-18 `[V]`) conjecture (their Conjecture 3) that five statements are equivalent: (a)
the Petersen coloring conjecture; (b), (c), (d), (e): there is a sublinear function bounding the
least number of abnormal edges of a proper 5-edge-coloring (`ab`) on, respectively, all
bridgeless, all 2-connected, all 3-connected, all cyclically 4-edge-connected cubic graphs. They
prove `(a) <=> (b)`, `(c) <=> ab <= 5` on 2-connected cubic graphs (Theorem 2), `(d) <=> ab <= 7`
on 3-connected cubic graphs (Theorem 3) and `(e) <=> ab <= 9` on cyclically 4-edge-connected cubic
graphs (Theorem 4).

After the disproof, (a) and (b) are false. `context/2026-09-18-defect-unbounded.md` (Theorems 2
and 3 there, `[D]`) gives 2-connected cubic graphs with `ab >= 6` (a ring of six counterexamples)
and 3-connected cubic graphs with `ab >= 8` (a 3-connected cubic frame on eight vertices), so (c)
and (d) are false as well. Statement (e) is the open one: is there a cyclically 4-edge-connected
cubic graph with `ab >= 10`? If so, all five statements are false and Conjecture 3 holds.

## Method

For a counterexample `G` and two independent edges `e1 = ab`, `e2 = cd`, let `M(G; e1, e2)` be the
4-pole obtained by deleting both edges and attaching a pendant edge at each of `a, b, c, d`. If
`M` has no Petersen coloring (no map to `E(P)` with all 52 vertex stars good, the four pendant
labels being free), then in the graph `H_t` obtained by joining `t` copies of `G - e1 - e2`
cyclically as in Figure 1 of Mattiolo et al. (edges `d_i a_{i+1}` and `c_i b_{i+1}`), every map to
`E(P)` has a bad vertex in every copy: a copy with only good vertices restricts to a Petersen
coloring of `M`. Hence `ab(H_t) >= pd(H_t) >= t` (Lemma 1 of the context note), and `H_10` would
settle (e) provided it is cyclically 4-edge-connected (their Proposition 2, stated without proof;
here it is checked by machine on the instance).

Step 1: decide the Petersen colorability of `M(G; e1, e2)` for one representative of every orbit
of unordered pairs of independent edges under the listed automorphisms, for `G52` first, then
`G52b`, `G68`, `G112`, `H112` if needed. UNSAT answers carry DRAT proofs checked by drat-trim; SAT
answers are validated by a checker and their pendant label patterns are tabulated (the cut-space
argument predicts only three patterns: `s(a) = s(b)` and `s(c) = s(d)` is impossible; crossed
equal pairs; or four distinct labels forming the 4-cut around an edge of `P`).

Step 2 (only if step 1 finds a non-colorable 4-pole): build `H_10`, verify that it is simple,
cubic and cyclically 4-edge-connected (3-edge-connected and every 3-edge cut isolates a vertex),
and record the statement. As a consistency check, `pd(H_2)` and `pd(H_3)` are computed by the
cardinality encoding (expected exactly 2 and 3 if attained, at least 2 and 3 in any case) and
twenty same-copy pair relaxations of `H_2` must be UNSAT.

## Falsifiable predictions

- P1 (control). For the Petersen-colorable snark `J5`, every 4-pole `M(J5; e1, e2)` is Petersen
  colorable, because a Petersen coloring of `J5` restricts to one of `M` (each pendant edge takes
  the label of the deleted edge): all orbit representatives SAT, with `s(a) = s(b)` and
  `s(c) = s(d)` available as a pattern.
- P2 (pattern check). No SAT witness of any `M(G; e1, e2)`, `G` a counterexample, has pendant
  labels with `s(a) = s(b)` and `s(c) = s(d)`; every witness shows one of the two other patterns.
  A violation refutes the cut-space argument or the encoder.
- P3 (the question). Committed expectation, low confidence (about one half): some pair of
  independent edges of `G52` gives a non-colorable 4-pole. The universal 2-criticality of `G52`
  (every vertex pair relaxation is satisfiable) points the other way, which is why the confidence
  is low. If `G52` has none, the other four graphs are examined with the same protocol.
- P4 (only if P3 holds). `H_10` is cyclically 4-edge-connected, so `ab(H_10) >= 10`, statement (e)
  is false and Conjecture 3 of Mattiolo et al. is true.

## One-sidedness

A non-colorable 4-pole is a DRAT-certified fact and the lower bound on `H_t` follows by a
two-line argument. If every 4-pole of every known counterexample is colorable, nothing is decided
about (e); the tabulated boundary patterns are then the reusable output.

## Premise dependencies

Theorems 2 to 4 of Mattiolo et al. `[V]`; Lemma 1 (`pd <= ab`) `[D]`; EXP-001 and EXP-007 P0
(the five graphs have no Petersen coloring).

## Invariant-first note

The cut-space argument restricts the boundary patterns but does not decide colorability of a
4-pole; it is used as a consistency check (P2).

## Compute budget and kill criterion

CPU only. 10 minutes per 4-pole; 6 hours overall; the cyclic connectivity check of `H_10` within
2 hours.

## Verdict rules

CONFIRMED if P1, P2 pass and P3 holds with P4; REFUTED (of P3) if every orbit representative of
all five graphs is colorable; INCONCLUSIVE if budget stops the sweep before either.

## Addendum 1 declared 2026-09-18, before any instance of the kind named here ran

State of step 1 when this was written: about 300 of the 482 orbit representatives of `G52` decided,
all SAT (no non-colorable 4-pole `M` so far).

Second family of 4-poles, same purpose. For an edge `uv` of a counterexample `G`, let
`N(G; uv) = G - {u, v}` with its four dangling edges `d1, d2` (at the other neighbours of `u`) and
`d3, d4` (at the other neighbours of `v`). The cut-space argument leaves, for a coloring of `N`
with all vertices good, only boundary patterns that cannot be completed to `G`:
`s(d1) = s(d2)` and `s(d3) = s(d4)`; crossed equal pairs with two non-adjacent labels; four
distinct labels around an edge of `P` split one and one at `u`. Whether any of them occurs is a
finite question per edge orbit.

If some `N(G; uv)` has no Petersen coloring, the necklace of `t` copies (the two dangling edges at
the `v` side of copy `i` joined to the two at the `u` side of copy `i + 1`, cyclically) has a bad
vertex in every copy under every map, so `ab >= pd >= t`; with `t = 10` and a machine check of
cyclic 4-edge-connectivity this settles statement (e).

- P5 (control): for `J5` every `N(J5; uv)` is colorable (restriction of a coloring of `J5`).
- P6: committed expectation, low confidence (one third): some edge of one of the five
  counterexamples gives a non-colorable `N`. One representative per edge orbit, all five graphs,
  10 minutes per instance. SAT witnesses are checked and their boundary pattern is tabulated; a
  witness whose pattern can be completed to `G` refutes the encoder (it would color `G`).
