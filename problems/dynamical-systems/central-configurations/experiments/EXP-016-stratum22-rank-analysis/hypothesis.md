# EXP-016 - The k = 2, p = 2 stratum: mass-Jacobian rank, stage (ii) opens

Declared: 2026-08-01, BEFORE any run. Campaign: CCB-036 stage 3, after
EXP-015's confirmed shape dimensions (5 ungauged, 4 gauged).

## The objects

The reduced block {L13, L15, L23, L25, L35, L36} is linear in the four mass
unknowns (m1, m2, mA, mB). Its 6 x 4 mass-coefficient matrix J has entries
built from s-factors (inverse-cube differences of quotient distances) and
signed areas; on the stratum every signed area is a product of widths and
height differences (verified pattern: Delta_345 = wA (v - q) up to sign),
whose SQUARES are r-expressible by the dossier identities. The Dias-Pan
Section 7 chain needs: generic rank of J on the shape variety; the
determinantal loci Delta_k intersected with the shape variety per rank case;
and one genuine central-configuration witness with rank 4. THIS experiment
takes the first staged bites; the loci intersection chain and the CC witness
are EXP-017+ by design (no scale creep).

## Predictions

- P1 (rank at the exact geometry witness): at the rational geometry
  (a1, a2, u, v, p, q) = (3, -1, 2, 1, 1, -2), the matrix J, computed exactly
  in sympy (entries live in a real radical extension; rank decided by exact
  minor arithmetic), has rank 4.
- P2 (rank at an independent second geometry): same at
  (2, -2, 1, 2, 3, -1). Two independent full-rank points make rank 4 the
  generic rank on the shape variety (the rank-deficient locus is Zariski
  closed; two points is evidence recorded as such, one point already
  suffices for genericity ON ITS COMPONENT).
- P3 (component structure of the gauged shape ideal): Singular's minimal
  associated primes (minAssGTZ) of the EXP-015 gauged shape ideal complete
  within 300 s, and the witness geometry's distance vector lies on exactly
  one minimal component, which has dimension 4. This is the Dias-Pan
  "I(H) primary / E irreducible" analogue, adapted honestly to our
  ghost-carrying cut: we need the PHYSICAL component identified and its
  dimension pinned, not global irreducibility.
- Branches: rank < 4 at both witnesses = the stratum has a mass-degeneracy
  the cross case lacks (structural finding, stop and audit); minAss caps =
  the component analysis moves to the partial-GB/witness toolkit; the
  physical component NOT of dimension 4 = the EXP-015 reading was carried by
  a ghost, audit immediately (this is the uncomfortable branch and it is
  declared).

## Preflight (methodology/12)

- Source-complete: the block and its linearity are proved in the dossier
  (symmetry argument); the Delta factorization pattern is verified sympy
  output; Dias-Pan's chain is read in full. No [U] premise.
- Smoke: the J entries at the witness must satisfy the pairing identities
  (the discarded L14, L16, L24, L26, L46, L45 evaluate to the negatives of
  their partners at the same point): an internal consistency check computed
  BEFORE any rank is trusted.
- One-sidedness: every branch can refute (see above); P3's uncomfortable
  branch is explicit.
- Invariant-first: the recorded invariants are the two witness ranks, the
  number and dimensions of minimal components, and which component carries
  the witness.
- Budget and kill: sympy exact rank at two points (minutes; radical
  arithmetic in a 6 x 4 via 4 x 4 minors); one Singular minAssGTZ at 300 s.
  No extensions. If sympy's radical rank computation exceeds 1200 s per
  point, record inconclusive-cap and fall back to rank over a floating
  interval check ONLY as screen data (never verdict-carrying).

## Consequence ladder

- P1 + P3 land: stage (ii)'s foundation is set; EXP-017 = the distance-only
  pushforward of the Delta_k minor loci and the Lemma 7.3 case chain over
  the physical component; EXP-018 = the genuine CC witness (census machinery
  on the stratum equations at pair-equal masses). Chain closes = stratum
  theorem = wording to Felipe FIRST.
- Refutation branches: as declared above, each stops the campaign pending
  exact audit.
