# EXP-003 preflight: next matching level

Date: 2026-09-05. Status: frozen hypothesis before computation. CPU only.

## Falsifiable target and motivation [C]

Let T(d,m) be the maximum number of edges of any finite simple triangle-free graph with maximum degree at most d and matching number at most m. Predict

    T(d,d+1) = d*d+d+2, for every integer d>=7.

The stronger fixed-order ingredient predicts that the maximum for order 2d+3 and maximum degree at most d is also d*d+d+2. This resolves the m=d+1 slice of Ahanjideh-Ekim-Yildiz (AEY) Conjecture 6.1 if proved. Banak-Ekim-Taskin (BET) already supply the attaining construction and finite values through d=12; their Table 3 leaves d=13,m=14 between 184 and 185. The proposed contribution is the uniform upper bound, not the construction or the classical Andrasfai-Erdos-Sos obstruction.

## Frozen symbolic route and premise dependencies

For a triangle-free F on n=2d+3 vertices with maximum degree d, bipartite F has at most d(d+1) edges. Otherwise take a shortest odd cycle C of length l>=5. Every outside vertex has at most two neighbors in C (an odd gap among three or more neighbors would yield a shorter odd cycle). Therefore sum of C-degrees is at most 2n, and total deficit D=nd-2e is at least ld-2n>=d-6. The only edge count above the target not excluded is d*d+d+3. At equality, C has length five, every outside vertex has degree d and exactly two C-neighbors. Divide vertices into the five cycle-neighborhood types, of sizes n_i>=1. Then adjacent type sums are <=d and equal d whenever n_i>=2. Show these constraints are impossible when their sum is 2d+3 and d>6, using a singleton type and the adjacent-singleton cases. This is an all-parameter argument, not an inferred census result.

For arbitrary order, use AEY final published Lemma 2.4 / Corollary 3.5: an extremal maximizing d-star components has only d-stars and factor-critical nonstars with matching number at least d. There can be at most one nonstar at matching budget d+1. A nonstar of matching d has at most d*d+1 edges by their Theorem 3.4 (or Lemma 3.1), with at most one extra star. A nonstar of matching d+1 has order 2d+3 and invokes the new bound. These are primary-source-verified external theorems, not premises inferred from our EXP-001/002. The latter experiments are prior contextual results only, and are unchanged.

Attainment: take K_(d+1,d+1) minus its diagonal matching; delete A0B1 and A1B0; add a new vertex adjacent to A0,A1,B0,B1. Every old degree is d and the new degree is four. A shift-by-two perfect matching on the old vertices witnesses matching number d+1. This is the known BET t=1 construction, independently derived and credited.

## Bougard translation and rejected shortcut

The attaining graph's complement is NOT (d+2)-connected: A0,A1 have d common F-neighbors, producing a K_(2,d), and deleting the other d+1 vertices disconnects its complement. Do not claim this gives the exact Bougard value.

A valid secondary claim to prove is the one-edge bracket

    d*d+4*d+1 <= f(2d+3,2,d+2) <= d*d+4*d+2.

The lower bound follows from the fixed-order theorem. For the upper bound subdivide a single existing edge of the same crown graph, then complement it. Show triangle-freeness, exact independence two, and (d+2)-connectivity by excluding a complete bipartite subgraph on at least d+2 vertices in the subdivided crown. The lower bound exceeds ceil((2d+3)(d+2)/2) by floor(d/2)-2, an unbounded strict-interior discrepancy. The exact choice within this bracket is not part of the primary target.

## PASS / FAIL meanings and invariant-first decision

A finite PASS certifies only the listed graphs and integer constraint enumerations. The uniform target is confirmed only by a complete all-parameter proof surviving an independent adversarial review. A failed witness rejects that construction; a counterexample to the upper bound refutes the target. An implementation bug alone does not refute the mathematics. Unproved source premises or a proof gap mean inconclusive/revise, not confirmation.

The cheap degree-deficit invariant already reduces the entire fixed-order upper bound to a single forbidden equality case. No broad graph enumeration or speculative solver campaign is needed. At d=6 a balanced C5 blowup of type sizes (3,3,3,3,3) has 45 edges, exceeding the proposed formula 44; retain it as a boundary control.

## Exact validation protocol, budgets and stop conditions

Smoke d=7..9; full d=7..30. Build both the known maximizer and subdivided-crown construction, store deterministic edge lists, verify triangle-freeness, degrees, size and the explicit matching. Check the rejected complement cut directly. For d<=18, check complement connectivity via independent max-flow and exhaustive subset/recursive independence where practical; use NetworkX as a separate implementation audit with pinned version. Enumerate positive five-type sizes with a designated singleton, sum 2d+3 and the equality constraints for d=7..30; expect zero survivors. Include the all-size-three d=6 control.

Each stage has a five-minute cap, flushed per-degree progress and deterministic checkpoints. Hitting the cap yields partial finite evidence only. No GPU. Tests write temporary outputs and compare complete deterministic certificates. Source/receipt bytes use LF for cross-platform replay.

## Primary sources, accessed 2026-09-05

- AEY, final published 2024 paper, Sections 2-3 and 6, DOI 10.1007/s10878-024-01123-z: https://pure.uva.nl/ws/files/225491323/Maximum_size_of_a_triangle-free_graph.pdf
- BET, 2023 published work, DOI 10.1016/j.disopt.2023.100802; full author manuscript Proposition 4.1 and Table 3: https://arxiv.org/html/2304.01729 . Final publisher full PDF was not obtained; distinguish author-manuscript access.
- Das-Gupta final discussion: https://arxiv.org/html/2608.18828v1 . The current boundary correction does not prove or rule out this triangle-free matching slice. Bounded novelty search is not exhaustive priority certification.
