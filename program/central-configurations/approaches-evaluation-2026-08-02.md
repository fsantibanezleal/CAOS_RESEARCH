# Approaches evaluation 2 (2026-08-02): measured effectiveness after eleven experiments and seven lemma pieces, plus three new views

Requested by Felipe (second edition; the first is
approaches-evaluation-2026-07-25.md). Everything below is ranked by
MEASURED outcomes in this program's record, not by promise.

## 1. Measured effectiveness ranking (what actually produced results)

1. CLOSED-FORM MINOR ANALYSIS ON PARAMETRIZED STRATA - the discovery of
   this campaign. Seven proven lemma pieces in one day; every identity
   machine-verified in milliseconds once the radical factors were pulled
   out of single-term columns. Cost: careful structuring, near-zero
   compute. This instrument closed k = 0, 1, 2, 4 of the theorem chain.
2. EXACT WITNESS CONSTRUCTION (3-4-5 and Q(sqrt(3)) geometries) - closed
   every independence gap it was aimed at, five for five. The
   witnesses construct themselves once the conditions are explicit.
3. THE SHAPE-PLUS REFRAMING (irreducible parametrized component + Krull)
   - dissolved the component-identification problem that killed two
   decomposition attempts; turned EXISTING exact computations (EXP-016's
   rank, EXP-018's hexagon minor) into chain cases at zero new cost.
4. SINGULAR ON SMALL COMPLETE SYSTEMS - seconds for shape dimensions and
   product-only bases (EXP-013's complete 9-second basis; EXP-015's
   one-second dimensions). NEVER succeeded on mixed product-plus-
   realizability ideals: five experiments, three formulations, all
   granularities, all capped. The boundary of its usefulness is now
   mapped precisely.
5. MOD-P SCREENS AS BUDGET GATES - twice decisive, zero wasted overnight
   runs. Screen-only soundness rule held throughout.
6. TROPICAL PREVARIETY RUNS (the n = 6 lottery) - 14+ cpu-days each,
   healthy, undecided. Correct as background load; never the plan.
7. msolve CENSUSES AND SECTIONS - retired at n >= 4 / n >= 5 by measured
   caps; their validated domain (n = 3 censuses, n = 4 emptiness probes)
   is on the record.

## 2. New views (beyond V1-V4 of the first edition)

V5. THE DEGENERACY-LOCUS VIEW. The stratum incidence variety is the
kernel locus {(x, m) : J(x) m = 0} of a 6 x 4 matrix over the
4-dimensional shape+: a degeneracy-locus problem. Expected codimensions
(Eagon-Northcott count (6-j)(4-j)) put the rank-2 locus at codimension 8
(EMPTY on a 4-fold) and the rank-3 locus at codimension 3 (dimension 1).
Our chain only needs dim <= 2 and <= 3 respectively: the slack between
expected and needed is enormous, which explains why every random exact
evaluation lands nonzero, and predicts the sign-chamber program would
find the rank-2 locus empty or near-empty on the physical region. Not a
proof by itself (genericity is unproven), but the right heuristic frame
for where the truth sits.

V6. THE COLUMN VIEW - ACTIONABLE NOW. Rank <= 2 means the mA and mB
columns lie in the plane spanned by the clean m1/m2 columns. Because
col(m1) vanishes on rows {L13, L15} and col(m2) on rows {L23, L25}, the
membership scalars are DETERMINED TWICE each (that is exactly piece 7b's
four conditions), BUT the pair rows L35, L36 give TWO MORE mixed
conditions per column that piece 7b never used, and their coefficients
are piece 1's clean single-term entries s(d1A, d1B) Delta_35k and
s(d2A, d2B) Delta_35k: a FIFTH and SIXTH bilinear condition whose
s-support ({s(d1A,d1B), s(d2A,d2B)}) is DISJOINT from C1's and C3's
r12-type support. Disjoint support is precisely what a second-cut
independence argument wants: identical vanishing of two conditions with
disjoint radical content on a common 3-fold is far easier to refute
(specialize the radicals appearing in only one of them). DECLARED: derive
and verify the L35-row conditions in closed form, evaluate at the three
anchors, and run the second cut against C1 with the disjoint-support
argument. This supersedes the heavy norm-elimination route if it lands.

V7. THE TEMPLATE VIEW (the program beyond one theorem). The campaign's
pipeline (pair-equality lemma by symmetry; nine-variable quotient; shape
dimension in seconds; clean-minor Boolean analysis; exact witnesses;
shape-plus Krull cuts) is a TEMPLATE that transfers with zero new theory
to: the k = 0, p = 3 stratum of n = 6 (three mirror pairs, projectivized
mass dimension 2, likely EASIER); the reflection strata of n = 7 (whose
general case is fully open, so ANY closed stratum there is new); and the
vortex analogues (Dias-Pan's own transfer shows the demand exists). A
paper series, "symmetry-stratified generic finiteness", with one
theorem per stratum and shared machinery, is a realistic program that
this record has already half-built.

## 3. Recommendation (one line per horizon)

Now: finish k = 3 via V6's disjoint-support conditions (Route A's
elimination continues in parallel as insurance). Next: the statement to
Felipe, the split manuscript, then the k = 0, p = 3 stratum by template.
Background: the n = 6 tropical lottery and the Chang-Chen diagram ladder
remain the paths to statements beyond symmetric strata.
