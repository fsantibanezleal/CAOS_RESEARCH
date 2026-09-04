# EXP-001 - independent certification of the public counterexamples

Declared 2026-09-03 before experiment code was run. Phase PC-P1. Backlog PCB-002.

## Question

Do CNF encodings written here, sharing no code with the public Putman encoders, certify with
checked DRAT proofs that Putman's two 112-vertex graphs and the Goedgebeur-Jooken-Macajova-
Mattiolo-Mazzuoccolo 52-vertex graph have neither a Petersen coloring nor a normal
5-edge-coloring, while the same encoders accept known Petersen-colorable graphs and reject
corrupted inputs?

## Motivation

Context dossier section "the disproof". Replication is the prerequisite of the consequence
audit (PC-P2..P4): every later verdict is conditioned on these three graphs being genuine
counterexamples under our own machinery, not under imported certificates.

## Fixed objects

- `G112`: `data/putman-112-main.edgelist`, digest `dc16cc18600cf77c8661b7baf89c7019f265299308541961ff884ea7187b4e8b`.
- `H112`: `data/putman-112-d3.edgelist`, digest `0f2d8858110c6f012de7ddffa92fdbc709d7da630f199b0e3c81bb56eb6b35c7`.
- `G52`: `data/gjmmm-52.edgelist`, transcribed from the appendix of Zenodo record 21933786
  (vertices renumbered 1..52 to 0..51); 78 edges.
- Controls (all cubic, bridgeless, Petersen-colorable by the sources): the Petersen graph
  (identity map), `K4` and the prism (3-edge-colorable, hence colorable), the flower snark `J5`
  (20-vertex snark, colorable by the order-36 census) and `J7`.
- Encodings: `pcclib.encoders.petersen_coloring` (edge-image variables, pairwise adjacency
  constraints, two symmetry-breaking units) and `pcclib.encoders.normal_coloring(k=5)`
  (edge-color, side-presence and rich indicator variables). Neither uses vertex-witness or
  missing-pair variables.

## Falsifiable predictions

- P1: the three graphs are simple, cubic, connected, with edge connectivity 3, girth 5, and
  their digests match the public values (`G52` has no published digest; its own is recorded).
- P2: for every control, both encodings are SAT and the decoded witness passes the independent
  checker (Petersen defect 0; normal defect 0).
- P3: for `G112`, `H112`, `G52`, both encodings are UNSAT and drat-trim prints `s VERIFIED`
  for every proof.
- P4: Putman's four archived DRAT proofs (record 21845291 v1.0.0 archive, SHA-256
  `8af3eec414b652f05c56979dc148321535cdc51ff9cbd59dff278ef3d53d9832`) are accepted by our
  drat-trim against his archived CNFs (third route: his encoding, our checker).
- P5: corrupted controls: (a) the identity map on the Petersen graph with two images swapped is
  rejected by the checker; (b) deleting the two symmetry-breaking units does not change any
  status; (c) a mutated expected digest makes the harness fail.
- P6: no cycle-separating edge cut of size at most 3 exists in any of the three graphs, and an
  explicit cycle-separating 4-cut is exhibited for each (cyclic edge connectivity exactly 4).

## One-sidedness (methodology 12, P4)

PASS on P3 with verified proofs is a positive certificate of non-colorability (a theorem about
these three graphs), not a statement about any other graph. FAIL on P3 (SAT) would refute the
public claim and produce an explicit coloring; FAIL by TIMEOUT proves nothing.

## Premise dependencies (P3)

- Petersen colorings are equivalent to normal 5-edge-colorings (Jaeger 1985, cited by both
  papers; not re-proved here). The experiment tests both directly, so no verdict depends on it.
- Triangle-freeness of the Petersen graph justifies the pairwise encoding: derived and unit-
  tested here.

## Invariant-first note (P5)

No single invariant decides P-colorability; cyclic edge connectivity and girth are recorded as
context only.

## Compute budget and kill criterion (P6)

CPU only, WSL CaDiCaL 1.7.3, drat-trim. Wall cap 30 minutes per SAT call, 60 minutes per
drat-trim check; the whole run under 4 hours. A capped instance is recorded INCONCLUSIVE and
the verdict is at best partial.

## Verdict rules

- CONFIRMED only if P1-P6 all pass.
- REFUTED if any target instance is SAT with a checker-validated coloring.
- INCONCLUSIVE if any target instance hits its cap or a proof is not verified.
- A control failure invalidates the verifier; it is never evidence about the targets.
