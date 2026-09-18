# Adversarial audit of the manuscript and the campaign results

Run 2026-08-25 on instruction to review adversarially at maximum detail and
validate the manuscript data and all results. The rule followed is the one
this campaign sets for itself: attack the claim, and record PASS only when
the attack fails. A claim that could not be attacked is recorded as NOT
TESTED, never as passed by silence.

Subject: the published record on tropical finiteness certificates for
central configurations, v0.08, Zenodo DOI 10.5281/zenodo.21760069,
published 2026-08-02; plus the campaign results from rounds 52 to 55.

## 1. Manuscript claims that SURVIVED attack

| claim | attack | result |
|---|---|---|
| the 6x4 mass matrix has generic rank 4 | 36 random shapes off the collision and equal-height loci | rank 4 at 36 of 36, smallest sigma_4/sigma_1 seen 2.5e-3 |
| the equal-mass regular hexagon is in the stratum with rank EXACTLY 3 | recompute both small singular values | sigma_3/sigma_1 = 5.66e-1, sigma_4/sigma_1 = 5.7e-52 |
| its kernel is the equal-mass ray | read the kernel off the SVD | (-1, -1, -1, -1) to 20 digits |
| the catalogue has 84 nonzero 2x2 minors | count identically-vanishing minors over 6 independent shapes | 6 identically zero, 84 nonzero, 90 total: EXACT match |

The 84 count is the strongest of these. A 6x4 matrix has 15 times 6 equals
90 two-by-two minors, and the manuscript figure of 84 is reproduced digit
for digit by an independent count.

## 2. A manuscript claim that is UNDER-SPECIFIED as printed

The abstract states that in the equal-mass rhombus stratum, after the
Cayley-Menger equation is adjoined, the square with side a satisfying
32a^6 - 32a^3 + 7 = 0 is the unique positive point of the stratum.

Two facts complicate reading that sentence on its own:

  * the sextic has TWO positive real roots, a = 0.68627928283838 and
    a = 0.87797428993016 (substituting x = a^3 gives 32x^2 - 32x + 7 = 0);
  * BOTH give an exact central configuration, and so does every other
    positive a, because a square of four equal masses is central at every
    size: scaling only rescales lambda. The two roots differ in lambda, at
    8.375345285 and exactly 4.

So the sextic is a statement about a NORMALISED distance system, not about
which square is central, and the word unique is meaningful only together
with the normalisation that produces it. Nothing here refutes the
manuscript: the claim is about the stratum of the distance system, where
the normalisation is fixed elsewhere in the text. What is recorded is that
the abstract sentence does not carry its own normalisation, so a reader
checking it the obvious way finds two roots and a whole scaling family.

A first pass of this audit verified the claim by checking that a square of
that side is a central configuration. That test CANNOT FAIL and established
nothing; it is withdrawn and replaced by the above.

## 3. External calibration: the Dias-Pan witness, reproduced

This is the strongest single validation obtained, and it is external.

Their Proposition 5.2 gives an explicit cross central configuration with
the four line masses equal and the off-line pair at m5 = m6 about 4.7648,
normalised by r14 = 2, in which the inner line pair and the off-line pair
form a SQUARE. The campaign direct-read dossier (2026-08-01, full read,
archived PDF with SHA-256) records that value and proposes re-deriving it
as a calibration anchor.

Feeding our own 3x4 cross system ONLY the condition that the two line
masses be equal, and solving for the shape:

| quantity | ours | theirs |
|---|---|---|
| off-line to line mass ratio | 4.764828362053881 | 4.7648 |
| inner line pair, distance from centre | 0.5597581471293 | (the square condition) |
| off-line pair, distance from centre | 0.5597581471293 | (the square condition) |

The ratio agrees to all five published digits. And the SQUARE was not
imposed: it emerged, the two distances coming out equal to 13 digits from a
condition that says nothing about them. The resulting configuration
satisfies the central-configuration equations with a lambda spread of
1.3e-51.

This validates the 3x4 cross system end to end, and with it the machinery
behind the degeneracy results of rounds 53 and 54.

## 4. Campaign results that SURVIVED attack

| claim | attack | result |
|---|---|---|
| the cross point has rank exactly 2 | rebuild the matrix from scratch and recompute | sigma_3/sigma_1 = 4.7e-51, sigma_4/sigma_1 = 8.9e-52 |
| it is an ISOLATED rank-2 point, not a curve | perturb along a generic direction at six scales | sigma_3/sigma_1 grows LINEARLY, 9.25e-3 down to 9.24e-8 |
| it does not contradict the stratum work | check it against the declared scope | v = q = 0 exactly, and the stratum explicitly excludes the equal-height sub-stratum, so it is a boundary point |
| no collinear collision-free (2,2) configuration exists | 2000 random shapes, all 20 triple areas plus a collision floor | none found |
| the new chart residue is covered by the bi-corner chart | map all 69996 residual boxes through the REAL coordinate map | 69996 of 69996 covered, largest d1A = 0.093875 against the limit 0.21875, none in the bi-corner own discard |

The last one was done through the coordinate map from the start,
deliberately, because the same claim checked the wrong way earlier produced
a false alarm about a hole in the atlas.

## 5. A false refutation, caught and withdrawn

The pair-equality lemma is the manuscript central result for this stratum.
An attack fixed mA different from mB, solved the central-configuration
equations for the shape, and returned 213 collision-free solutions with v
different from q, at residuals down to 1e-41. Reported as it stood, that
would have refuted a published lemma.

It refutes nothing. Re-reading the wording: the PAIR equations factor as
the mass difference times (q-v) times (cx^3 - cs^3), forcing PAIR-EQUAL
masses. The pair equations are L34 and L56, the ones BETWEEN the two bodies
of a single mirror pair, which the six-row reduction drops precisely
because this lemma consumes them; and pair-equal means the two bodies OF a
pair carry equal mass. The lemma justifies the equal-mass-within-a-pair
ansatz. It says nothing about mA against mB, so varying those tests a
proposition nobody made, and the 213 solutions are ordinary central
configurations of the stratum. Verified as such: one of them refined
against ALL TWELVE equations has max residual 6.9e-41.

Recorded because the failure mode is the interesting part: the attack was
technically clean, the solver was right, the residuals were real, and the
conclusion was still wrong, because the claim had been paraphrased before
it was attacked.

## 6. What remains NOT TESTED

The pair-equality lemma itself. The correct attack drops the ansatz: put
independent masses on all four pair bodies over a mirror symmetric geometry
and solve the full twelve-equation system. Run with the geometry HELD
FIXED, it returned no positive-mass solution at all, which is uninformative
rather than confirming: with asymmetric pair masses the centre of mass
leaves the symmetry axis, so the two x-equations at the axis bodies stop
being automatic, and the system becomes ten equations in six unknowns,
overdetermined. The informative version lets the geometry vary too, ten
equations in ten unknowns (u, v, p, q, four pair masses, one axis mass,
lambda). That has not been run.

Nothing in this audit validates that lemma.

## 7. A finding about the work of THIS session

The literature check recorded in CC-F58 was run by web search. The campaign
already held a direct-read dossier of exactly that paper, read in full on
2026-08-01, with the PDF archived and hashed, and the manuscript already
cites it as DP18. The conclusion reached by search was correct and matches
the dossier, but the framing in CC-F58 implied the identification was new
to the campaign. It was not.

Worse, the dossier contains something the search did not surface: it
records a DISCREPANCY inside the Dias-Pan paper itself. Their Theorems 1.1
and 7.11 as printed say there is a proper OPEN set of masses off which
finiteness holds, while the proof constructs a proper CLOSED subset. The
dossier instruction is explicit: never quote the open phrasing as if it
were the content. The wording used in CC-F58, for a generic choice of
positive masses, happens to be safe, but it was safe by luck, not by having
read the shelf.

The rule this violates is one the campaign sets for itself: read the
persisted research before acting. It is recorded here so the next session
opens context/ before reaching for a search engine.
