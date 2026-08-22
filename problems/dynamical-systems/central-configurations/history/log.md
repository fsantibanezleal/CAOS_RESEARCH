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

## 2026-08-01 - EXP-009 direct torus census reaches both declared caps

- The exact-square smoke test passes on the enriched route-A system.
- Route A and the independent Hampton--Moeckel z-system route B each ran for
  the declared 3600-second cap under msolve 0.10.1 and produced zero output.
  The first route-B attempt ended in a documented WSL idle shutdown and is
  excluded from the evidence; its mechanically capped rerun supplies the verdict.
- Verdict: INCONCLUSIVE-CAP on both routes. No dimension or census is claimed;
  the published counts 50 and 4 remain untested by us.
- Direct solving is closed at current budgets. EXP-010 promotes the
  incidence-dimension lane; reproducing HM06's mixed volume 25380 is retained
  as the separate bounding rung.
- EXP-010 was declared after the EXP-009 verdict and before any run. Its first
  calibration targets the n=4 Dziobek variety with exact random linear sections
  and a deterministic dimension rung. Preflight reconciliation corrected the
  Rabinowitsch dimension bookkeeping: adding `t*prod(r_ij)-1` does not change
  Krull dimension. No EXP-010 computation has started.

## 2026-08-01 - EXP-010 decided: the cheap half of the dimension instrument survives

- EXP-010 VERDICT: EMPTINESS PROBES CONFIRMED IN SECONDS, CENSUS PROBES REFUTED
  BY CAP. Smoke gate passed in 1 s (square ON the Dziobek variety by exact
  polynomial reduction modulo 8A^3 = 4 + S2, S2^2 = 2; tetrahedron excluded by
  CM = 4; the 3-4-5 rectangle excluded by the Dziobek differences). Both
  codimension-4 random sections EMPTY in 1 s each (msolve `[-1]:`, raw outputs
  archived): probabilistic-exact support for dim D4 <= 3, the direction generic
  finiteness actually consumes. Both codimension-3 censuses and the sympy
  staircase capped (900 s / 1800 s): the declared kill criterion fired for the
  census half, so no degree data and no lower bound beyond the exact witness
  (dim >= 0 from the square). Stripped degrees measured: Dziobek differences
  drop to degree 9 with 6 terms each, Cayley-Menger degree 6 with 22 terms.
- Instrument consequences adopted: recorded-section emptiness probes VALIDATED
  as the cheap probabilistic upper-bound tool; CCB-037 (Dias-Pan partial-GB
  leading-term unions, deterministic upper bounds) pulled forward to replace
  full staircases; CCB-034 (witness sets) promoted for lower bounds and degrees.
  EXP-011 (n = 5 spatial Dziobek) is now shaped as the Dias-Pan proof pattern
  run on our exact instruments: emptiness probes + partial-GB + witness rank.
- Same morning: Dias-Pan arXiv:1811.08681 read IN FULL (CCB-036 stage 1 done;
  dossier persisted; PDF archived with SHA-256; the cross symmetric stratum of
  n = 6 is generically closed, their theorem statement misprints "open" for a
  closed exceptional set; journal search found no published version). CCB-037
  minted from their Lemma 7.5. Known-results ladder row added.

## 2026-08-01 - EXP-011 decided; the frontier read opens; the engine lesson lands

- EXP-011 VERDICT: SMOKE AND CAP-SIGNATURE CONFIRMED, EMPTINESS AND PARTIAL-GB
  RUNGS FAILED TO SCALE AT DECLARED BUDGETS. Smoke in 4 s (bipyramid exactly ON
  the products+CM cut; 4-simplex excluded by CM = -5; collinear control
  excluded by all 15 products). All four msolve section probes capped at 300 s
  (the declared kill criterion for the emptiness instrument at n = 5 fired);
  the partial-GB menu completed 1/15 subideals, union bound vacuous
  (d_pgb = 10). No algebraic refutation of the expected dimension 4; the
  6-to-10-variable wall is measured. Engine reading: Dias-Pan ran the same
  leading-term pattern in minutes under Singular; our worker used sympy
  Buchberger with the 130-term Cayley-Menger in every subideal. CCB-037 v2 =
  engine swap (msolve -g already installed) + product-pair menu; CCB-034
  witness sets promoted to next instrument spike; the n = 6 strata campaign
  (9-variable quotients) waits on those engines, exactly as Dias-Pan's own
  computations demonstrate is sufficient.
- CCB-004 stage 1 DONE: Chang-Chen programme preprint (117 pp) archived with
  SHA-256; pages 1-6 and 41-46 read. The residual 24 upgraded to a QUOTED
  statement (stated twice); one of the 62 mass-relation diagrams impossible
  for positive masses; the complete n = 4 mass-relation ladder transcribed
  (matches AK12 5.1-5.4); n = 5 sharpened (Algorithm I: 20 diagrams, II kills
  9/11/13/17, leaving AK12's 16). Cross-engine re-derivation of the n = 4
  relations with our exact stack is the declared calibration gate before any
  n = 6 residual-diagram spend.
- CCB-036 stage 2: the reflection-strata map of planar n = 6 persisted
  (collinear closed classically; CROSS closed by Dias-Pan; the 2+2-pair and
  3-pair types OPEN per two recorded searches; the flagged hit examined and
  cleared, a (1+4)-vortex paper). Both open types collapse to 9-variable
  quotients.
- Strategy answer persisted for Felipe's direct question: the ranked
  real-advance paths are (1) the symmetric-strata campaign, (2) the tropical
  n = 6 pointedness hunt (both gfan08 runs healthy, 34 and 55 cpu-hours), and
  (3) the Chang-Chen residual diagrams; census/dimension work is
  infrastructure, not advance, and today's caps SELECTED the surviving
  toolkit rather than killing the program.

## 2026-08-01 - Round 8: EXP-012 decided, the engine hypothesis confirmed

- EXP-012 VERDICT: ENGINE HYPOTHESIS CONFIRMED, UNION BOUND INFORMATIVE-WEAK
  AT DIM <= 7. Singular 4.3.2 (installed and hashed today) completes 12 of the
  IDENTICAL 15 subideal jobs sympy walled on, at 0.4-1 s each (sympy baseline
  1/15 at about 100 s): the EXP-011 wall was an engine artifact. The lighter
  16-subideal menu completed 16/16; the union of 466 grevlex-correct QQ
  leading monomials from 28 subideals gives the lane's first sound
  deterministic bound, dim <= 7 for the n = 5 spatial Dziobek cut (target 4
  not reached; the declared menu-growth follow-up applies). Cost pattern
  recorded: the three Singular-capping subideals are all _bc pairings sharing
  the body pair {1,2}.
- THE CONTROL DISCIPLINE FIRED ON ITS FIRST OUTING: EXP-012's
  exact-reproduction control caught a lex-vs-grevlex harvester bug in
  EXP-011's pgb worker (sympy gb.polys default to lex; monoms() must be told
  the order). Impact audit: EXP-011's harvested monomials were
  order-inconsistent but its bound was vacuous and nothing consumed them
  (correction note beside the retained artifact; verdict amended in place
  same day); EXP-010's P3 never completed, so nothing there depended on the
  bug. All three harvesters fixed; msolve's -g mode identified as MOD-P and
  pinned screen-only in the hypothesis BEFORE the run.
- Consequences: CCB-037 v2 VALIDATED (Singular workhorse, sympy verification
  layer); EXP-013 = menu growth (triples, mixed pairings, pairs with CM), 
  hypothesis first; the n = 6 symmetric-strata campaign is engine-unblocked.

## 2026-08-01 - EXP-013 decided: the products ideal has exact dimension 5; the n = 5 question localizes to the CM cut

- EXP-013 VERDICT: FULL SYSTEM CAPPED (600 s), MENU CONFIRMED AT DIM <= 5,
  PRODUCTS DIMENSION EXACT AT 5. The all-fifteen-products system (with
  saturation, without Cayley-Menger) completed a FULL reduced grevlex basis in
  nine seconds (2436 leading monomials): its staircase dimension is the true
  Krull dimension, 5, matching the rank-one parametrization count. The menu
  union (4615 leads from 11 completing subideals) confirms dim <= 5 for the
  cut. Cost law now sharp: everything without CM runs in seconds, everything
  mixing products WITH CM caps at 120 s. The whole n = 5 dimension question
  is now ONE algebraic event: does CM vanish identically on any top component
  of the products variety? EXP-014 (incremental std from the completed basis)
  is the declared next rung.

## 2026-08-01 - EXP-014 decided: the 5-to-4 question resists both Groebner routes; the lane hands it to witness sets

- EXP-014 VERDICT: SANITY AND NONZERO NORMAL FORM CONFIRMED, INCREMENTAL
  EXTENSION INCONCLUSIVE-CAP. The products basis reproduced in-session
  (2436), Cayley-Menger has a NONZERO normal form against it (so the cut is a
  proper subvariety, re-confirming the 4-simplex separation), and std(S, cm)
  ran its full new 1800 s budget without terminating, joining the
  from-scratch route as measured-out-of-reach. Deterministic state at n = 5:
  dim(products) = 5 exact, dim(cut) <= 5 proven, expected 4 undecided. Per
  the declared ladder the 5-vs-4 test moves to CCB-034 witness sets (list
  the top components, evaluate CM on witness points), and the k = 2, p = 2
  stratum campaign proceeds regardless with the twice-measured cost law
  (realizability equations out of the Groebner core, adjoined last).

## 2026-08-01 - Round 10: the stratum campaign opens and clears its first stage same day

- Novelty pass: no published closure of the k = 2, p = 2 stratum surfaced
  (recorded search; an unverifiable summary-level diagram count NOT imported).
- EXACT DERIVATION persisted (dossier + script): nine quotient distances;
  c_x^2 - c_s^2 = wA wB verified; THE PAIR-EQUALITY LEMMA in closed form
  (L34 and L56 factor through (m5 - m6) and (m3 - m4) times (q - v) times
  (c_x^3 - c_s^3)), forcing pair-equal masses on the open stratum with the
  honest q = v gap flagged; the reduced Laura-Andoyer block proved SIX
  independent mass-linear equations by a pure symmetry argument (reflection
  invariance + L_ji = L_ij), with the background computational cross-check
  still running.
- EXP-015 VERDICT: CONFIRMED ON ALL PREDICTIONS in about one second per run:
  shape variety dimension 5 ungauged, 4 gauged (two-way engine agreement),
  exactly the Dias-Pan dim(E) = 4 analogue; ghosts do not dominate; the cost
  law held. Stage (i) of the stratum pipeline is DONE. Next: EXP-016 (the
  6 x 4 mass-Jacobian rank analysis with determinantal loci) and EXP-017
  (the exact rank-4 witness); a completed chain is the stratum theorem, and
  its wording goes to Felipe first. A smoke evaluator bug (odd-term
  handling) was caught by the gate itself at zero solver cost and fixed in
  one commit.

## 2026-08-01 - Round 11: EXP-016 decided, the rank stage lands

- EXP-016 VERDICT: GENERIC RANK 4 CONFIRMED AT TWO EXACT WITNESSES (one
  second each, pure radical arithmetic, no truncation budgets), COMPONENT
  DECOMPOSITION CAPPED (minAssGTZ at 300 s; primary decomposition is far
  heavier than the one-second std of the same ideal). The smoke gate's
  pairing check doubled as the computational confirmation of the dossier's
  symmetry proof (all six partner identities exact at the witness), closing
  what the teardown-killed derivation script left open. The capped rung does
  not block the chain: EXP-017 is declared as dimension bounds on
  shape-intersect-Delta_k with the minors pushed to distance form,
  sidestepping irreducibility entirely; EXP-018 anchors the top case with a
  genuine CC witness. n = 6 note: the pow3 arbitrary-precision gfan08 run
  passed 7 cpu-days, outliving gfan 0.7's second failure mode; both runs
  healthy and checkpointed.

## 2026-08-01 - Round 12: EXP-018 decided; the chain re-weights onto the loci bounds

- EXP-018 VERDICT: HEXAGON VERIFIED AS STRATUM CC (all six reduced equations
  exactly zero at equal masses, in Q(sqrt(3)), one second), RANK DEGENERATES
  TO 3 at its symmetry (every 4x4 minor vanishes; a nonzero 3x3 minor is
  displayed in closed form). The declared second branch fired. Structural
  consequence: the theorem chain needs NO CC witness if EXP-017's dimension
  bounds land for all k (components with k-dim shape projection cannot sit
  inside Delta_k when dim(shape meet Delta_k) < k); the Dias-Pan witness
  route was their workaround for not computing the Delta_4 bound, and our
  route already chose the bounds. EXP-018b (a less symmetric witness) is
  demoted to redundancy.
- Session infrastructure: the shared checkout moved to a third problem's
  branch (work/huneke-wiegand/open, after tau-conjecture PRs 136-137);
  central-configurations work continues from an isolated git worktree on the
  same lineage branch, touching nothing of the parallel session's tree. A
  curation commit by the other session (52668e4, preserving the EXP-010
  tuple API correction) is acknowledged.

## 2026-08-02 - Round 13: EXP-017 decided (all caps, smokes green); the formulation lesson

- EXP-017 VERDICT: SMOKES CONFIRMED (the enlarged ghost-free ring gives shape
  dim 4 in a second; the mass matrix cross-validates entrywise against
  EXP-016 at W1), ALL FOUR LOCI BOUNDS INCONCLUSIVE-CAP (full std at 300 s
  and every per-minor subideal at 60 s walled: 13 + 80 + 84 + 20 subideals).
  One pipeline fix before any outcome: fractions serialized as fake rational
  exponents and Singular's exit-0-after-parse-error faked the OK sentinel;
  fixed, error markers now fatal. THE DIAGNOSIS: premature elimination.
  Row-LCM clearing inflates minors to degree near 100; Dias-Pan kept their
  S-quantities as ring variables exactly to avoid this (their minors stay
  degree <= 6 and completed in minutes). EXP-017b = the s-variable model
  (about 20 extra variables with sparse defining relations s a^3 b^3 =
  b^3 - a^3), declared next. The chain stands: stages (i) + (ii-rank)
  proven, case arithmetic unchanged, no theorem claimed.

## 2026-08-02 - Round 14: EXP-017b decided at the gate; the see-saw is measured

- EXP-017b VERDICT: THE BASE IDEAL ITSELF CAPS IN THE S-MODEL. The smoke gate
  (dim of shape + 22 degree-7 defining relations in 34 variables) walled at
  600 s and stopped everything before any minor time. Combined with EXP-017
  this measures the cost see-saw from both sides: eliminate the s-factors and
  the minors reach degree near 100; retain them and the base ideal explodes.
  Structural root: Dias-Pan's matrix entries were single-term, ours sum over
  mirror-pair members. EXP-017c declared: a mod-p feasibility SCREEN
  (screen-only, never verdict-carrying) over both formulations and all four
  rungs, then ONE long declared-budget QQ run on the most promising cell,
  with the Prop 7.2-style sign-analysis lemma prepared in parallel as the
  Groebner-free fallback for the low-rank cases.

## 2026-08-02 - Round 14 close: the screen is decisive; the theorem moves from compute to proof-writing

- EXP-017c VERDICT: all ten mod-p cells capped at both primes (P1 confirmed,
  P2 refuted): per the declared decision rule the Groebner route to the loci
  bounds is CLOSED at human budgets in both formulations. The obstruction is
  structural (the reduced block sums over mirror-pair members). The stratum
  theorem's remaining gap is now a PROOF task in the Dias-Pan Prop 7.2
  style: a rank-floor lemma on physical fibers by sign analysis over the
  shape inequalities (machine-verified, Groebner-free), plus for the top
  case either a rank-4 CC witness (EXP-018b, census machinery) or the
  image-dimension argument. Three exact anchor points exist (ranks 4, 4, 3
  at the two geometries and the hexagon). This is the normal shape of such
  results: Dias-Pan's own 7.2 was manual. Nothing is claimed.

## 2026-08-02 - Round 15 opens: the rank-floor lemma's first piece is PROVEN

- Lemma piece 1 (dossier 2026-08-02): on the open stratum, the {L35, L36} x
  {m1, m2} minor of the mass matrix factors EXACTLY as
  s(d1A,d1B) s(d2A,d2B) (-2 u p (v-q)(a1-a2)); the polynomial part never
  vanishes there, so rank J >= 2 everywhere off the explicit exceptional set
  {d1A = d1B} union {d2A = d2B}. Proof by radical factor-out plus one
  polynomial identity, machine-verified in milliseconds. This is the
  Dias-Pan Prop 7.2 pattern working for our stratum, and it vindicates the
  compute-to-proof transition: what three Groebner formulations could not
  reach in hours fell to one structured minor in closed form. The remaining
  case tree (equidistant exceptional sets, then the rank >= 3 floor) is
  enumerated in the dossier.

## 2026-08-02 - Round 21-22: the endgame's computational door closes; the proof door stays open

- EXP-019 decided (both single-minor cuts capped at 1800 s despite a
  32-term increment over a one-second base) and its mod-p screen addendum
  (all four cells capped): the Groebner route to the k = 3 and k = 4 loci
  bounds is now measured CLOSED at every granularity, formulation and
  characteristic tried. The CM/Krull reduction remains the frame: the shape
  ideal is a complete intersection, hence unmixed, so single-polynomial
  properness statements suffice, and properness can be established by
  EXACT WITNESSES instead of dimension computations, exactly as lemma
  pieces 4 and 5 did. The bordered-minor closed-form program for k = 3 is
  the sole active route, with the EXP-016 rank-4 geometries as the ready
  properness witnesses.

## 2026-08-19 (round 31): the covering-programme restructure

- EXP-005 n=6: both gfan runs found dead again (WSL restart); pow2 resumed
  from the fresh 1.2 GB checkpoint, pow3 relaunched fresh (still no
  checkpoint file ever written by its --saveas; loss recorded); resume
  tooling persisted (run08-resume.sh, relaunch-both.sh).
- Ladder correction: the chain needs dim(R_j) <= j for j = 0, 1, 2. R_0
  closed globally (exact two-line lemma: J = 0 forces v = q = 0, off the
  stratum; EXP-022/r0-lemma.py). Ball certificates extended with rank-2
  witnesses so R_1 meets no ball.
- Closure-hole correction: the slice-limit collar route abandoned BEFORE
  use (a 2-dim low-rank set can hide in a shrinking tube at every nearby
  slice value; the boundary-slice bound controls nothing off the slice).
- The simplification: collars BECOME coverings (band needs no rescaling;
  collision tube gets the polar blow-up with all 1/rho^3 cancelled
  algebraically; pair-collapse rescales the mA column by 4u^2). Dossier
  section: THE COVERING PROGRAMME RESTRUCTURE.
- EXP-021 integrated rerun launched (four pentagon balls, both
  certificates at radius 2^-8, all four certified in 0.1 s each; zero
  residual failures required; 12 h budget).
- EXP-022 opened: hypothesis (region atlas + trap certificates), band
  covering launched, tube blow-up algebra machine-verified (six exact
  polynomial identities; four face limits with linear convergence; NEW
  face finding: rank-2 degeneracy curve w^2 + v^2 = 1 on the rho = 0
  face, the coincident double-pair on the circle through the axis
  bodies), shared pipeline with the generalized trap certificate, tube
  covering launched on both angle charts after 5-point crosschecks.
- Mirrored CC-F32 (pentagon + piece 8) and CC-F33 (the restructure) to
  CAOS_MANAGE; wiki 05 rows added for EXP-019/020/021.

## 2026-08-20 (round 33): ulow certified; fa2 design error caught and fixed

- ulow (pair-collapse) DONE ok=true, zero failures: 880,947 boxes, 26,090
  traps. The trapped set is the near-collision CONDITIONING collar
  (v ~ +-1, u in [0.03, 0.25], d1A^-3 entry blow-up): sigma_3 is ORDER ONE
  at trapped midpoints (0.60), no rank-2 structure (probe + descent);
  contrast pentagon (exact rank 2) and cross (sigma_3 ~ 1.7e-3). A_plow
  free by the swap identity.
- fa2 FAILED BY DESIGN (272k structural failures, killed): the absolute
  far-tube criterion was wrong; CS vanishes identically on the whole
  double-infinity face, making boxes touching it uncertifiable. Root
  cause: the tube geometry is scale-RELATIVE (cs small vs R_A). Fix:
  fa2b ratio parametrization (r = epsA/epsB in [0,1]): CS^ = |dirA - r
  dirB| analytic, vanishing only on the true far-tube; discards {CS^ <
  1/16} (far-tube) and {CX^ < 1/16} (vertical far-corner) deferred to the
  blow-up chart. Crosschecked 5/5, launched.
- The sq() dependency bug resurfaced in fa2's discard (tau*tau on
  straddling intervals): fixed with .sq(); pipeline discard hardened
  (AssertionError -> not discarded).

## 2026-08-20 (round 34): the mini-chart cascade, derived end to end

- Certified today: tube extension BOTH charts (w in [1/8, 7/32], zero
  failures). Running: fa1-resume, fa2b, cb1, uplow, deep, both bi-corners
  (all checkpoint-fresh; slow under 7-way CPU sharing with two gfan runs).
- Derived, machine-verified (crosscheck gate 5/5 each), and queued:
  M1 (quadruple cluster; REUSED the fartube generated polynomials via the
  (c,s) <-> (a,b) identification, verified exactly; new Wronskian W1 and
  G5 extractions), M2 (collinear quadruple; the deepest singular point is
  UNPHYSICAL so the cascade terminates there), M3 (vertical far-corner;
  codim-3 center, rational 2-sphere blow-up, 9-quantity generator; the
  gate caught the signed-radius hemisphere error, fixed with the odd-hat
  convention), M1-vert (vertical collision corner at body 1; the M3
  pattern verbatim; seam bound rhoy <= sqrt3/8 < 1/4 exact).
- Remaining mathematics: M1v2 alone (the two cones inside M1-vert where
  the pairs ALSO merge; both centers are point-pairs on the blow-up
  sphere; same generator recipe). Then the atlas is complete and the
  chain assembles.
- The crosscheck gate's running tally: SEVEN real errors caught before
  any run (fa2 L36 sign, fa2 tau*tau dependency, cb1f misplaced eps^3
  twice, bicorner-opp L25 signs, m3 hemisphere composition, and the
  m2 grid-floor sampling artifact diagnosed as such).

## 2026-08-20 (round 35): the collision-collar gap closed; the atlas gate

- Diagnosed ALL residual covering failures to one cause: boxes CONTAINING
  an excluded face. Measured: every dyadic shell at positive distance
  certifies (6 halvings, both corner charts). Proven: LEMMA PIECE 10, the
  corner-face rank floor, uniform in the shell index, with a complete
  branch table; the two branches with no surviving minor are exactly the
  two collisions the open stratum excludes.
- Found and fixed a catastrophic cancellation in the naive s(r12, d) form
  (d -> 2 on the corner face); the exact identity d2B^2 - 4 =
  rhoc(4 ssig + rhoc) gives a cancellation-free evaluator, now used by
  cb1 and cb1f.
- deep's 13,354 failures traced to a WRONG-CHART sliver just outside the
  declared M2 discard; boundary shifted (M2 to Rc <= 3/32, deep's corner
  discard to {w < 1/32, rho < 1/16}), rerun certifying with ZERO failures.
- bicorner-same's 1020 failures traced to a dependency-inflated discard
  test at the 1/16 seam; threshold widened to 1/8 with the seam re-proven
  (rhoq <= 0.2795 < 3/8), both charts rerun fresh.
- ASSEMBLY record written (atlas table, the face principle, the dimension
  count term by term, the draft statement).
- ATLAS SEAM GATE: 40k samples (half adversarial, near every face), zero
  unclaimed points, with ELEVEN negative controls all firing. The controls
  caught a double-cover transcription bug (manual swap images alongside
  the Klein-orbit closure) and a sampler blind spot (the collinear
  quadruple region was never sampled).
- Fleet: eight coverings running, all at zero failures.

## 2026-08-20 (round 36): the face table completed; pieces 11 and 12

- LEMMA PIECE 11, the pair-collapse face: both pairs onto the axis. The
  mass-column rescales leave only the mA, mB columns, so the face is rank
  2; but the m1, m2 columns vanish to FIRST order, and dividing them by
  the collapse parameter makes the face matrix generically RANK 4, with
  the closed form C2 = 4ab[phi(1-v)phi(-1-q) - phi(-1-v)phi(1-q)],
  phi(x) = x(1/8 - 1/|x|^3), verified to 8 digits, plus a branch table on
  its zero curve (six points located, each with a surviving minor).
- THE FACE-RANK GATE: evaluate every chart's matrix ON its face and
  measure sigma_3. Eleven charts full rank (the reason they certify with
  no residual failures); two at exactly zero, NAMED by the gate rather
  than assumed: M1 and fartube.
- The entry-order probe diagnosed both: five rows scaled correctly, L35
  under-scaled by exactly one power, giving the piece-11 face structure.
- LEMMA PIECE 12 closes them by the piece-11 mechanism, verified at three
  scales and forty samples per face (sigma_3 = 1.0 throughout, with a
  structural reason).
- The atlas's face table is now COMPLETE: every face is either full rank
  or closed in closed form by pieces 10, 11, 12.
- Fleet: m1, bicorner-same, fartube, uplow, deep all at zero failures;
  m2's residue is exactly piece 11's face and is covered by it.

## 2026-08-20 (round 38): piece 11 made effective; the (0,3) stratum opened

- THE COLLAPSE CHART: lemma piece 11's column rescale implemented as an
  actual chart, so the collar is certified INCLUDING its face (19/19 face
  points certify rank >= 3 at eps = 0). No threshold left implicit.
- Its discard was corrected: |f| < 1/16 rejected precisely the region m2's
  residue occupies; the true criterion is cs < 1/32, since
  cs^2 = eps^2 (c-s)^2 + f^2 is bounded below whenever either term is.
  With the fix the chart certifies m2's residue DIRECTLY.
- final-gates.py runs all four gates in sequence. ALL 20 chart artifacts
  re-verify independently with negative controls firing (one blank result
  was the gate tripping over guarded entries, fixed).
- EXPLORATION (persisted): the machinery reaches ALL FOUR
  reflection-symmetric strata of n = 6, because every one of them has a
  4-dimensional shape space after gauge; only the mass count differs
  (6, 5, 4, 3). The no-axis case is the easiest unsolved one.
- EXP-023 OPENED, the (0, 3) stratum (three mirror pairs):
  * the mirror symmetry kills L12, L34, L56 identically and pairs off the
    rest, leaving SIX independent equations over THREE masses: a 6 x 3
    matrix. Verified to 40 digits at random shapes.
  * GENERIC RANK IS 3 = full rank, so the kernel is trivial and a generic
    shape admits NO masses: central configurations of this stratum are
    confined to the rank <= 2 locus, a codimension-2 subvariety.
  * INSTRUMENT VALIDATED on a known member: the regular hexagon has rank
    exactly 2 with kernel the equal-mass ray, reproducing the classical
    regular-hexagon central configuration.
  * the covering was built (matrix assembled generically from the six
    positions, crosschecked 5/5 against the independent mpmath
    derivation) and launched.

## 2026-08-20 (round 40): the (0,3) stratum's face structure is COMPLETE

- Merge chart built and verified: the merge is TWO simultaneous collisions
  (mirror-forced), row orders match tube.py's pattern exactly, both
  singular factors cleared algebraically, crosscheck 5/5, and the MERGE
  FACE certifies rank 3 at 40/40. The S3 symmetry makes this one chart
  cover both merge types (re-gauging to the third pair turns "A and B
  merge" into "the other two merge").
- NO REGION AT INFINITY: the outer region rescales onto the all-narrow
  (near-collinear) region, which is a collapse region. Measured full rank
  there, sigma_3 = 2.0 flat over four orders of magnitude.
- The (0,3) face inventory is now complete and EVERY entry is full rank:
  pair collapse 27/27, pair-pair merge 40/40, all-narrow flat at 2.0.
  This stratum needs NO face lemma and NO chart at infinity, against the
  (2,2) stratum's three lemmas plus inverted charts. The whole difference
  is the absence of axis-body mass columns.
- Fleet: twelve coverings running across both strata, all zero failures
  (the four pending (2,2) charts were rerun on request; cb1 and cb1f now
  use the tighter intersected evaluation).
