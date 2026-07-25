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

## 2026-07-24 (session 1 continued, round 2): EXP-002 decided; HM06 + JL25 read in full; multi-factorial rule

- Felipe's directives landed and persisted: ALL content and chat in English, always;
  and the MULTI-FACTORIAL standing rule (methodology/10 amendment): several lenses
  active concurrently, constant online research every round, recorded
  self-questioning of our own approaches.
- EXP-002 recorded run (2324 s, exit 0): P1 CONFIRMED (the enriched system F + G +
  e_IU is 0-dim DIRECTLY, 0.7 s per sample, no saturation; the G-equations kill the
  EXP-001 line symbolically): the caps pathology of EXP-001 dissolves. P2: decided
  samples (1,1,1), (1,1,2) perfectly classical (exactly 4 positive points; zero
  spurious); (1,2,3), (2,3,5) inconclusive-cap (engine limit MEASURED: sympy census
  2.4 h+ on integer-separated masses). P3 CONFIRMED (planar rhombus census = the
  square alone; tetrahedron excluded exactly by e_CM = 4). P4 CONFIRMED (U = M I
  exact; J baselines recorded). Census instrument v2 (Stickelberger charpoly
  eliminants + sqf dedup + certified-numeric pre-filter + exact acceptance); two
  more sympy traps caught and regression-gated (real_roots multiplicity duplicates;
  Matrix.charpoly's own-Dummy PurePoly).
- CCB-002 DONE: HM06 read IN FULL from the author PDF (archived on E: with SHA-256):
  the whole certificate transcribed (9-equation system; Minkowski polytope 12828
  vertices / 2980 facets; 53 nontrivial facets; 19 face classes; facet-22 eliminant
  m1 m4 - m2 m3 and facet-33 Q polynomial; second-order Puiseux kills; Mixvol 25380
  -> 8460 + 12 = 8472; lower bound 32 = 12 + 6 + 14). Cross-validation: HM06's "14
  distinct monomials" per AC equation matches our EXP-001 P6 profile exactly; the
  dimension-blindness our EXP-001 refutation found is stated in HM06 verbatim.
- AK12 skim (pp. 535-540; PDF archived): Smale's question verbatim; Chazy's false
  1918 postulate; Palmore's degenerate example (central mass (64 sqrt(3) + 81)/249);
  Wintner quotes; their delta-variable complex-continuation formulation.
- THE FRONTIER FIND (multi-lens online sweep + Felipe's pointer): Jensen-Leykin,
  arXiv:2301.02305v2 (Aug 2025), READ IN FULL: purely polyhedral generic-finiteness
  method (Puiseux-valued masses with chosen valuations; gfan tropical prevariety;
  pointed recession cones of all "comets" force dimension 0; Zariski-dense
  tropicalization fibers give generic masses); n = 5 done in 80 cpu-minutes with
  published one-liners and f-vectors; n = 6 INCONCLUSIVE at ~100 cpu-days for one
  valuation choice, with an explicit call for different valuations / equation
  variants. New frontier rows: CCB-029 (gfan reproduction), CCB-030 (valuation
  search), CCB-031 (equation-variant prevariety shrinking: our EXP-002 P1 phenomenon
  at prevariety level, aimed directly at their call).
- Engine decision recorded (self-questioning): sympy = specification + verification
  layer; msolve (RUR + certified boxes) = computation layer (CCB-025); OSCAR/
  polymake/gfan wrapped for tropical work (CCB-028), never hand-rolled first.
- Round closes WITHOUT version bump. Next round: CCB-029 (gfan n = 5 reproduction)
  and/or EXP-003 (msolve-engine P2 completion + n = 4 equal-mass planar census);
  reads queued: Sun degeneracy (arXiv:2510.25649), AK12 full anatomy (CCB-023).

## 2026-07-24 (session 1 continued, round 3): EXP-003 CONFIRMED: the JL25 certificate reproduced exactly

- gfan 0.7 built from the author tarball in WSL2 Ubuntu 24.04 (gcc-13 needed a
  two-line cstdint patch, recorded; tarball + binary SHA-256 in the artifacts);
  gfan ships dedicated _nbody / _smalessixth applications.
- EXP-003 (hypothesis committed BEFORE the run, db85647) DECIDED: all three
  predictions CONFIRMED: the n = 5 system inventory (35 polynomials: 20 asymmetric
  AC + 10 symmetric + 5 Cayley-Menger); the powers-of-3 prevariety f-vector
  (1506, 4744, 8586, 8787, 4652, 993) EXACT and its pointedness verified by our own
  exact parser (1591 rays, 85 unbounded directions, zero with a positive
  coordinate); the squares-valuation f-vector (3586, 12012, 18531, 15625, 7072,
  1357) EXACT. About 6 wall-minutes per valuation on 30 threads (~145 cpu-min each).
  OUR TOOLCHAIN NOW REPRODUCES THE STATE-OF-THE-ART GENERIC-MASS FINITENESS
  CERTIFICATE FOR n = 5 END TO END.
- Throughput calibration for the frontier: ~25 cpu-min per wall-min here, so a
  JL25-scale n = 6 attempt (~100 cpu-days) is ~2.8 wall-days on this machine;
  valuation/equation-variant SCREENING at n = 4/5 (minutes each) is the rational
  first move (CCB-030/031), before any multi-day n = 6 shot.
- Round-3 exploration moment: Sun-Xie-You (arXiv:2510.25649, revised Feb 2026)
  abstract read: four degeneracy formulations; treats our exact anchor cases (the
  equal-mass square; equilateral + central mass; rhombus nondegeneracy for
  arbitrary masses): the CCB-014 Hessian instrument now has a read-first gate
  satisfied at abstract level; full read queued before building.
- Round closes WITHOUT version bump. Next: CCB-030/031 experiment declarations
  (valuation screening; equation-variant prevariety shrinking) and CCB-025 (msolve)
  toward EXP-004.

## 2026-07-24 (round 4): EXP-004 DECIDED; the n = 6 lane opened and redirected by our own data

- MULTI-FRONT MODE (Felipe's directive): the program now advances several fronts
  concurrently, with heavy computations detached in background while reasoning
  continues elsewhere; persisted as program/central-configurations/
  research-lines-2026-07-24.md (fronts A tropical lane, B census engine, C
  manuscript + Zenodo, D web + release, E reads).
- EXP-004 (hypothesis committed first, 1a5fb84) DECIDED on a 16-cell grid:
  P2 and P3 CONFIRMED, P1 confirmed operationally with a bonus. TWO NEW WORKING
  VALUATION FAMILIES at n = 5 (powers of 2: 266/266 comets pointed; primes:
  250/250) beyond the two published by JL25; the squares control reproduced their
  published 257-COMPONENT COUNT EXACTLY, which validates our comet extraction and
  pointedness certificates independently of the f-vector; dropping the ten
  dependent symmetric AC equations (system S2) destroys the certificate at EVERY
  valuation and inflates the undecided comet from 71-95 to 241-2224 generators
  (the symmetric equations are tropically load-bearing: the prevariety-level form
  of EXP-002's enrichment law); n = 4 generic finiteness replicated purely
  polyhedrally in 2-4 seconds, with the equal-valuation case (0,0,0,0) resisting
  exactly as JL25 predict for the HM06-equivalent specialization.
- Honesty: our analyzer certifies pointedness (exact separating vector) and
  unpointedness (exact zero combination); on the failing controls it returns
  NEITHER, so negatives are recorded as "no certificate", never as "not pointed".
  CCB-032 (exact LP for a lineality vector) will close that gap.
- Instrument correction recorded: the first comet parser merged cones through
  shared UNBOUNDED rays and reported 245 fused components; the t = 1 slice only
  connects through BOUNDED rays. The fix reproduced the published 257.
- EXP-005 (n = 6) attempt 1 ABORTED after 6.5 min with
  gfan::MVMachineIntegerOverflow (powers of 3 reach t^243 at n = 6; the fast path
  raises rather than returning a wrong answer). REDIRECT WITHIN HOURS, driven by
  EXP-004's own finding: two variants relaunched in parallel (15 threads each),
  powers of 2 on the 64-bit path (max exponent 32) and powers of 3 with
  arbitrary-precision integers. This is the multi-front principle working: a
  screening result rescued a multi-day frontier run from a blind repeat.
- Front C: manuscript v0.01 -> v0.02 (real screening section + the n = 6 section;
  6 pages, compiles clean). Front D: the central-configurations problem page built
  on the shared shell (6 sections, EN/ES, verified citation spine) and routed.
- Note: a parallel session's commit swept some of our files into its own commit
  (ebc70df); content is intact and pushed, only the commit attribution differs.
- RELEASE v0.54.000 executed (this session owned the release step; no other session
  was mid-release: no open PRs, last merged v0.53.000). Version bumped in the three
  sources, CHANGELOG entry naming both problems' landed rounds, data bake refreshed
  (the five central-configurations experiments now bake, after their verdict headers
  were brought to the repo's "EXP-NNN - Verdict: ..." convention), content-standards
  guard OK, pytest green, frontend build green, tag v0.54.000 pushed, PR #66
  develop -> main MERGED via the API, Pages deploy triggered.
- MANUSCRIPT PUBLISHED on Zenodo (CC-BY): "Exact replication and screening of
  tropical finiteness certificates for central configurations", v0.02, version DOI
  10.5281/zenodo.21542484, concept DOI 10.5281/zenodo.21542483. Pre-publication
  reference audit (Felipe's no-fake-references rule) corrected two items: the
  Chang-Chen part-II volume/pages were search-only, so the bibliography now cites
  the verified part I (JSC 123 (2024) 102277, pinned via the Jensen-Leykin
  reference list) plus the programme preprint; and the "24 residual diagrams" count
  is now stated as OUR arithmetic from the three numbers in their abstract, not as
  a quoted claim. Both fixes propagated to the wiki, the references file and the
  frontend citation spine.
- EXP-005 UPDATE (second finding): the powers-of-2 variant ALSO aborted with
  gfan::MVMachineIntegerOverflow. So at n = 6 the machine-integer fast path is
  unusable REGARDLESS of valuation magnitude (max exponent 32 fails exactly like
  243): the n = 6 barrier has an arithmetic component, not only a combinatorial
  one. Both variants relaunched with arbitrary-precision integers (--bits 0), the
  path JL25 describe as about 10x slower, now running in parallel (15 and 14
  threads). This is data JL25 do not report for their own inconclusive attempt.
- Round closes; the next round monitors the n = 6 runs while front B (msolve
  census) advances.

## 2026-07-24 (round 5): three experiments decided in parallel with the n = 6 runs

- EXP-006 (msolve census) DECIDED: P1 and P2 CONFIRMED, P3 REFUTED AS POSED. The two
  censuses that saturated our sympy engine are CLOSED in under a second each by
  msolve, and for all four mass vectors the positive census is exactly classical,
  with every one of our exact algebraic points contained in a distinct rational box
  and no unexplained boxes: two implementations sharing no code agree everywhere.
  P3 refuted: the n = 4 affine enriched system has DIMENSION 1, so it has no
  isolated census; diagnostics exclude the vanishing-distance loci, so the census
  belongs in the torus (as HM06 do) and the published class count is recorded as
  UNTESTED rather than quoted.
- EXP-007 (exact pointedness) CONFIRMED on all three predictions: all 16 EXP-004
  cells decided in 33 seconds by a phase-I simplex over the rationals, zero
  certificate-verification failures, zero positive flips, and each failing control
  shown PROVABLY UNPOINTED with an explicit nonnegative zero combination. EXP-004's
  negative half is upgraded from "no certificate" to proof, and our data now
  independently CONFIRMS the failure of arithmetic valuations that JL25 report,
  localized to one comet out of 181.
- EXP-008 (equation enrichment) DECIDED: P1 and P2 REFUTED, P3 CONFIRMED. Dziobek's
  equations are tropically ACTIVE (comet counts fall 10 to 7 and 9 to 6) but do NOT
  rescue the hard equal-valuation case, which stays provably unpointed: the
  enrichment that saved HM06's ALGEBRAIC proof and the TROPICAL certificate come
  apart. My declared monotonicity prediction was wrong for a structural reason worth
  keeping: adding equations refines the polyhedral subdivision, so f-vector entries
  can grow while the set shrinks; the comet count is the invariant that behaves.
  The energy-inertia relation is tropically inert. Also recorded: a reproducible
  gfan --bits 0 parser bug on inputs mixing t^0 with positive powers, with a
  mathematically free valuation-shift workaround (mass-homogeneity means the shift
  multiplies each polynomial by a unit).
- MANUSCRIPT STANDARD (Felipe's review): an audit found two manuscripts shipping
  with no document-type marking. methodology/05 now carries a binding front-matter
  standard (running header naming the TYPE on every page, boxed type statement on
  page 1, ORCID author line, version in the date block, navy links, type matching
  the Zenodo publication_type). Our manuscript was brought to the standard and
  visually verified (page 1 and an interior page rendered), then published as
  Zenodo v0.03 (NEW VERSION 10.5281/zenodo.21554571, concept unchanged). The
  unsplittable-flow-cost manuscript of the parallel session is also unmarked; that
  is reported to Felipe rather than edited from here (isolation).
- EXP-005 (n = 6) heartbeat: both arbitrary-precision variants alive, about 2.8
  cpu-days consumed each in 9.5 wall hours, no output yet (gfan writes only at the
  end). Budget 7 days per variant.

## 2026-07-25 (round 6): the n = 6 barrier is characterized as INFRASTRUCTURAL

- EXP-005 fourth data point: the powers-of-2 arbitrary-precision variant ABORTED
  after 15 wall-hours (about 6 cpu-days) with a DIFFERENT gfan failure:
  `gfanlib_hypersurfaceintersection.cpp:505: Assertion !cone.isEmpty(mr)` in the
  CircuitTableInteger path. Combined with the two earlier 64-bit overflow aborts
  (which happen regardless of valuation magnitude, t^32 failing exactly like
  t^243), gfan 0.7 fails at n = 6 in BOTH arithmetic modes, in two distinct ways.
  The powers-of-3 arbitrary-precision variant is still running (about 7 cpu-days).
- Reading: our n = 6 barrier is a TOOLING barrier, not a compute-budget one. JL25
  report their n = 6 prevariety computation as completing (inconclusive because not
  all recession cones were pointed), so their run differed from ours in version,
  flags or valuation choice. This is data they do not publish.
- Action taken (tooling, no outreach): gfan 0.8beta (released 2026-05-07) fetched
  from the author page and built with the same two-line cstdint patch, to test
  whether the newer version clears either failure mode. Outreach to the author is
  NOT undertaken without Felipe's decision.
- RELEASES: v0.56.000 shipped the round-5 experiments after a version COLLISION
  with the parallel session (both bumped to 0.55.000; their tag was already
  published, so this round was renumbered to 0.56.000 and their tag left intact).
  The collision is a methodology/08 serialization miss on my side: no open PR was
  visible at the moment I checked, and one opened immediately after. v0.56.001
  followed, deriving the problem page's experiment counts from the baked records
  after a screenshot pass caught the state line reading "five experiments" when
  seven were decided.
