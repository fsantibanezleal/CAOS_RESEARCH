# EXP-018 - Verdict: HEXAGON VERIFIED AS STRATUM CC, RANK DEGENERATES TO 3 AT ITS SYMMETRY (2026-08-01; the declared second branch; the theorem chain re-weights onto the loci bounds, which need no CC witness at all)

Hypothesis: `hypothesis.md` (declared before any run). Runner: `run.py` (pure
exact radical arithmetic in Q(sqrt(3)); three seconds total). Artifacts:
results.json, the full mass matrix in srepr form.

## Outcomes

| Prediction | Outcome | Facts |
|---|---|---|
| P1 (hexagon is a stratum CC through our block) | PASS | all six reduced Laura-Andoyer equations vanish EXACTLY at the equal-mass hexagon; the classical fact is now re-derived inside our framework, which also validates the block construction end to end |
| P2 (rank at the hexagon) | DECIDED: rank 3, the second declared branch | a nonzero 3 x 3 minor (value 147/128 - 735 sqrt(3)/512) exists and every 4 x 4 minor vanishes; the hexagon's dihedral symmetry beyond our reflection forces a linear dependency among the mass columns |

## Reading

The hexagon is a genuine stratum central configuration but NOT a rank-4
anchor: at maximal symmetry the mass map degenerates (recorded as a stratum
datum; consistent with the general phenomenon that symmetric points carry
degenerate Jacobians, and with the hexagon's known role as a bifurcation
locus in the literature, which we do not import as a claim).

STRUCTURAL CONSEQUENCE, the important one: the theorem chain does not need
any CC witness if EXP-017's dimension bounds land in full. If
dim(shape intersect Delta_k) < k for each k in {2, 3, 4}, then no component
of the incidence variety with k-dimensional shape projection can project
inside Delta_k, so every such component carries fiber points of rank >= k
and the Lemma 7.3 argument closes dim(Omega_stratum) <= 4 outright. The
Dias-Pan witness route (their Prop 5.2 + 7.8) was necessary for them
precisely because they did NOT compute the Delta_4 dimension bound; our
EXP-016 verdict already chose the bound route. EXP-018's outcome therefore
re-weights the campaign entirely onto EXP-017 and costs no progress. A
rank-4 CC witness remains a nice-to-have redundancy (EXP-018b, a less
symmetric witness via the census machinery) rather than a dependency.

## Soundness notes

- All arithmetic exact over Q(sqrt(3)); the nonzero 3 x 3 minor is displayed
  in closed form; the vanishing of all fifteen 4 x 4 minors was checked
  minor by minor.
- P1's pass also confirms, at a THIRD independent point (after the two
  EXP-016 geometries), that the block construction and pairing conventions
  are correct.
- Session note: this experiment ran from an isolated git worktree because
  the shared checkout moved to a third problem's branch; the lineage branch
  work/jacobian-conjecture/next-round receives the commits unchanged.
