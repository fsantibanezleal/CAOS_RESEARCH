# 04 - Our program: the attack ladder

Mirror of `program/central-configurations/plan.md` (the plan is authoritative; this page
tracks it for readers of the problem tree). Routes: `program/central-configurations/routes-2026-07-23.md`.

## Ladder

1. **CC-P0 Foundation (active)**: exact Albouy-Chenciner system builder over QQ;
   calibration on the fully classical $n = 3$ (Lagrange point, Euler-Moulton collinear
   count, the Euler eliminant, the equal-mass labeled census); assembly of the planar
   $n = 4$ Hampton-Moeckel system with a recorded structural profile and the exact
   equal-mass square solution. Experiment: EXP-001. Certificates: exact Groebner over
   QQ / QQ(m), machine asserts, nonzero exit on failure.
2. **CC-P1 The HM $n = 4$ reproduction**: direct read of HM06; exact equal-mass census
   against the 4-classes / 50-rotation-classes ground truth; the BKK data (Newton
   polytopes, exact mixed volume); the torus-direction exclusions. Target: our pipeline
   certifies "$n = 4$ finite for all positive masses" end to end in open, replayable
   tooling.
3. **CC-P2 The $n = 5$ landscape**: AK12 zw-diagram transcription; our certified-listing
   instrument reproducing the equal-mass count (5); the explicit codim-2 exceptional
   variety; HJ11 spatial prevariety reproduction (f-vector (1, 576, 1620, 1420, 450)).
4. **CC-P3 The $n = 6$ frontier**: equal masses first (9 classes, independent
   reproduction); then the 24 residual Chang-Chen diagram cases, attacked per diagram
   with exact elimination (Groebner + resultants + modfrac mod-p preprocessing) and
   GPU homotopy landscaping certified a posteriori. Any single diagram closed sharpens
   the world frontier.
5. **CC-P4 Spatial ladder and bounds**: Dziobek/Veronese structure (Moeckel 2001, Dias
   2026); bound improvements at $n = 4, 5$.
6. **CC-P5 Consolidate + publish**: wiki per unit as verdicts land; SVGs; web page
   (gates per methodology/06); manuscript when validated novel material exists
   (methodology/09).

## Discipline

- Calibration before frontier: no instrument touches an open case before reproducing a
  published answer exactly.
- Reproductions are labeled replications; novelty claims only after an adversarial
  novelty pass.
- Exact arithmetic carries verdicts; floats/GPU only explore; UNVERIFIED literature
  items ([U] in `../context/references.md`) carry nothing until upgraded.
