# History log: central-configurations (append-only)

## 2026-07-23 (session 1): problem OPENED (scoped -> exploring)

- Session start ritual done (git pull both repos; methodology 01-08 re-read; jacobian
  RESUME skimmed as the working-style exemplar; isolation rules of methodology/08 in
  force: this session owns ONLY central-configurations folders, no version bumps).
- PRELIMINARY DEEP RESEARCH persisted (the opening gate):
  - `context/2026-07-23-deep-research-dossier.md`: the verified SOTA ladder. Key state:
    n = 3 classical (5 CCs); n = 4 planar closed by Hampton-Moeckel 2006 (count in
    [32, 8472], BKK, computer-assisted) and reproved by Albouy-Kaloshin 2012 without
    computer; n = 5 planar closed except an explicit codim-2 mass subvariety (AK12,
    Annals; equal masses ARE in the exceptional set, settled separately by
    Moczurad-Zgliczynski 2019); spatial 5-body: Moeckel 2001 generic + Hampton-Jensen
    2011 explicit exceptional list (tropical, Gfan); n = 6 planar OPEN, reduced by
    Chang-Chen (JSC 2024 + SIADS 2025) to 24 residual zw-diagram cases; n >= 7 fully
    open; Roberts 1999: continuum exists with one negative mass, so positivity is
    necessary; equal-mass rigorous counts n = 3..7: 2, 4, 5, 9, 14 (MZ19, PDF read,
    counts extracted from the appendix report files).
  - `context/2026-07-23-hampton-moeckel-method-dossier.md`: implementation-level
    transcription of the HM06 certificate logic (via HJ11, primary PDF read): the
    Albouy-Chenciner / Roberts / Dziobek / Cayley-Menger / IU equation set with exact
    polynomial forms; the BKK-tropical exclusion pipeline; calibration targets table;
    direct-read backlog CCB-002..006.
  - `context/references.md`: tagged bibliography ([V]/[Vs]/[U]).
- Portfolio flipped: `program/portfolio.yaml` central-configurations scoped -> exploring,
  opened 2026-07-23 (same commit as the first dossier, per Felipe's directive).
- Next in this session: program plan (program/central-configurations/), the CAOS_MANAGE
  mirror, then EXP-001 (calibration: exact AC-system builder validated on n = 3, the
  n = 4 HM system assembled; hypothesis BEFORE run).

## 2026-07-24 (session 1 continued): EXP-001 decided; lenses pass; methodology 11

- Program plan + backlog (CCB-001..012) + routes + RESUME written; portfolio row and
  program/README row flipped; CAOS_MANAGE mirror created (per-problem status/findings/
  history). Wiki 01-04 transcribed from the dossiers.
- Felipe's mid-session directive ("systematic programs persist, but take deliberate
  exploration moments; persist as a general constant tool") landed as
  methodology/11-exploration-cadence.md; the problem's first exploration moment
  produced program/central-configurations/lenses-2026-07-23.md (all 11 lenses of
  methodology/10 applied; analogies to the jacobian toolbox, vortices, homogeneous
  potentials, Smale 7; new paths CCB-013..020).
- EXP-001 recorded run (5490 s): CONFIRMED P2 (Lagrange identical in symbolic masses),
  P3 (Euler-Moulton: exactly one positive collinear solution per ordering, 4 exact
  mass samples; equal-mass chart value 90^(1/3)/6), P4 (symbolic Euler eliminant,
  degree 54, persisted), P6 (n = 4 planar HM system profile baseline), P1 at equal
  masses (saturated ideal 0-dimensional; GB size 37, 428 s). REFUTED P7-uniqueness:
  the equal-mass rhombus stratum contains TWO positive solutions of the bare AC
  system: the square (b^2 = 2a^2, CM = 0, a^3 = (4 + sqrt(2))/8, minpoly
  32x^6 - 32x^3 + 7) AND the regular tetrahedron (a = b = 1, CM = 4): the distance
  system is dimension-blind; planar statements require Cayley-Menger adjoined (then
  the square is unique in the stratum). INCONCLUSIVE at caps: P1 for the three
  unequal-mass samples (900 s each), P5 full equal-mass torus census (1800 s).
- Two real bugs caught and recorded (adversarial discipline): sympy solve_poly_system
  returns INCOMPLETE solution lists on these systems (missed the square; banned from
  verdict-bearing counts; replaced by the eliminant census with exact-residual
  acceptance) and is_positive returns None on nested RootOf (naive filters drop
  genuine solutions). A first monolithic runner was aborted at ~78 min inside the
  uncapped saturation; the staged capped runner replaced it.
- Dead ends recorded: naive resultant-chain eliminants vanish identically on the bare
  F-system (coordinate-hyperplane components; the line {r13 = r23 = 0} is in V(F) for
  all masses, machine-verified symbolically).
- Round closes WITHOUT version bump (methodology/08). Next: EXP-002 on the enriched
  system (corrected P7/P5 questions) + CCB-002 (HM06 direct read) + saturation
  instrument upgrade (CCB-007).
