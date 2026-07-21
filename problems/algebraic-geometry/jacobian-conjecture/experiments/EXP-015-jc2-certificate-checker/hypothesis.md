# EXP-015 - The JC(2) certificate checker and the m = 1 bridge extractor (tooling)

- **Question.** Ship the standing tooling of the 2D program: (a) an exact checker that decides,
  for any submitted pair (P, Q), whether it is a planar Keller map and whether two given points
  form a collision (the disproof certificate format for JC(2)); (b) the m = 1 bridge extractor
  that maps a hypothetical collision in the 3D weighted class o = (-1, -1, 1) to an explicit
  planar Keller counterexample (EXP-012's bridge, made executable).
- **Motivation.** JCB-023. The bridge theorem is only useful if the extraction is executable;
  and any future search (ours or anyone's) needs a neutral, exact verdict format.
- **Falsifiable predictions.**
  1. [MV] The checker accepts the library automorphisms (Keller: yes; submitted fake collisions:
     rejected with the exact reason) and rejects non-Keller maps.
  2. [MV] The extractor, fed a SYNTHETIC m = 1 collision datum (constructed by hand to satisfy
     the bridge equations formally, without claiming it exists as a polynomial map), outputs the
     corresponding planar pair and the checker then evaluates it, demonstrating the pipeline
     end to end; fed real m = 1 class data from EXP-012 (all injective), it must report "no
     collision to extract".
- **Method.** A tested module in the problem's code/ package (jclib2): sympy over QQ; pytest
  units; the checker protocol returns machine-readable verdicts.
- **Success criterion.** Both predictions hold under pytest.
- **Failure criterion.** Any checker misclassification (fix before shipping; the tool must be
  boringly correct).

Declared 2026-07-21 before the run.
