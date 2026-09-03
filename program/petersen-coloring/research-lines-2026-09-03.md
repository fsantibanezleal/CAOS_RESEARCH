# petersen-coloring: research lines and the exploration ledger (2026-09-03)

Per methodology 10 and 11: every round mints new viewpoints or records why none was found.
Lines are numbered PCR-n; each has a declared first step.

## Exploration moment of round 1 (EXP-001 to EXP-004)

What the machine showed that we did not predict:

1. The perfect matching index of all three counterexamples is 4, not 5 (EXP-002). The Petersen
   graph, the target of the coloring, is the one with index 5. So the counterexamples are not
   "Petersen-like" in the matching sense; they fail the coloring for a gadget reason (Jooken's
   distance constraints in the line graph), not for a covering reason.
2. Oddness separates the two constructions: 4 for Putman's 112-vertex graphs, 2 for the
   52-vertex graph (EXP-003), although both contain the same pole `F`. The 112-vertex graphs
   are therefore "worse" snarks than the 52 while being larger: minimality and oddness pull in
   different directions here.
3. All classical consequences survive on every retrievable counterexample (EXP-002, EXP-003).
   The disproof removed a sufficient condition, not a single instance of any lower conjecture.

## Lines

| id | line | lens | first step | status |
|---|---|---|---|---|
| PCR-1 | Is perfect matching index 4 forced for every cubic graph that contains `F` as a submultipole with the GJMMM gluing rules, or for every member of their infinite families `S_n`? | anatomy, invariant | build `S_1`, `S_2` (replace `F` by `F_1`, `F_2`) and the girth-5 members on 76 and 78 vertices; run the Berge-4 instance on each | todo |
| PCR-2 | Oddness along the families: does oddness stay 4 on `S_n` from `G112` and 2 on the family from `G52`? Is there a counterexample with oddness 6? | parameter ladder | same graphs as PCR-1, oddness ladder to bound 6 | todo |
| PCR-3 | The exact P-defect as an invariant of the gadget calculus: compute `P-Col` sets with defect allowance (which single vertex, when freed, restores colorability) and read the "critical vertices" of each counterexample | anatomy, two-sided | EXP-004 witnesses at the minimal defect: list the bad vertices; test whether they lie in the claw connectors | todo (needs EXP-004) |
| PCR-4 | Grammar minimality below 52: enumerate compositions of at most six copies of `F` with the two connector types (claw six-pole; trimmed `K4` 4-pole) and small joins; decide P-colorability of each by the cheap Petersen encoding (seconds each) | exclusion, bounded search | write the composition enumerator with canonical forms; budget 4 CPU-hours | todo |
| PCR-5 | Cyclic 5-edge-connectivity (GJMMM Problem 5): a counterexample needs a pole with the "distance rigidity" of `F` but no 4-cut; test whether 5-poles cut from small snarks have rigid `P-Col` sets | reformulation | compute `P-Col` sets of all 5-poles obtained from the Petersen graph and the Blanusa snarks by deleting a 5-cut | todo |
| PCR-6 | External dialogue: GJMMM's forthcoming version | external | re-check Zenodo concept 21933785 and arXiv weekly; re-derive any new claim in-repo before use | standing |

## Self-questioning

Is the consequence audit still the best route given what round 1 measured? Yes for the
manuscript (it is complete and unclaimed); after publication the highest-value line is PCR-4
(a certified minimality statement inside the grammar, cheap with the Petersen encoding) and
PCR-1/2 (structure along the infinite families), which reuse the round-1 tooling unchanged.

## Round 1 measurements that reshape PCR-4 (composition search)

- Classes without free vertices are trivial: a single universal coloring (all boundary labels
  equal) colors every composition (context note `2026-09-03-pure-f-compositions.md`).
- Counterexample-guided search with one blocking clause per coloring does not converge at 26
  semi-edges: the 26-vertex control `(3,2)` reached 1,059 iterations and 29,052 clauses in 15
  minutes without exhausting; `(5,2)` (also 26 semi-edges) is running under a 2-hour budget.
- Refinement for the next round (PCR-4b): break the outer symmetry with lex-leader constraints
  for the generators of the symmetry group of the join formula (the 8 semi-edge automorphisms of
  each copy of `F`, transpositions of copies, transpositions of free vertices, permutations of the
  three slots of a free vertex); a sound partial lex-leader encoding keeps at least one member of
  every orbit. Orbit estimates: `(5,2)` about 3e4, `(6,2)` about 5e5, `(5,4)` about 1.5e6; each
  candidate decision costs about 0.1 to 2 seconds with the Petersen encoding, so `(5,2)` and
  `(6,2)` become hours of CPU, and `(5,4)` a multi-core day.
- Alternative (PCR-4c): a 2QBF formulation (exists matching, for all labelings, some gadget
  constraint or equality fails) for a QBF solver; not attempted (no solver installed).
- The defect result reshapes PCR-3: the obstruction in `G52` needs two relaxed vertices and the
  pairs are plentiful; the critical-pair structure (which pairs, at what distance) is the next
  anatomical object.
