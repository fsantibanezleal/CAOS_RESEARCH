# Addendum: AK12 first-pass skim (2026-07-24)

Source: Annals of Mathematics 176 (2012) 535-588, publisher PDF (open on
annals.math.princeton.edu), pages 535-540 read this session; archived at
`E:\_Datos\caos-research\central-configurations\papers\albouy-kaloshin-2012-finiteness-cc-5bp.pdf`
(SHA-256 f2e57e185a0eb32f19b85667bd8d7829dcc4acca10fbb24758a779793b2507d9). Full
anatomy read (rules, zw-diagrams, the exceptional variety A) remains CCB-023.

Verified upgrades from the skim:

- **Smale's 6th question, verbatim as posed by AK12**: "Is the number of relative
  equilibria finite, in the n-body problem of celestial mechanics, for any choice of
  positive real numbers m_1, ..., m_n as the masses?" [V: Annals PDF p. 538; the
  Intelligencer original remains CCB-011 for the primary text.]
- **Theorem 2 (verbatim)**: finitely many positive normalized CCs of the planar
  5-body problem for masses in (R_0^+)^5 minus a CLOSED ALGEBRAIC subset A of
  codimension 2. The defining polynomials of A are computed via resultant
  factorizations with a standard CAS. An explicit Bezout-type upper bound exists but
  is "so bad that we avoid writing it explicitly".
- **Their working system (their (4))**: Cartesian coordinates plus inverse-distance
  variables delta_kl with delta_kl^2 (x_kl^2 + y_kl^2) = 1 and the rotation
  normalization y_12 = 0, lambda = 1; COMPLEX central configurations; the proof
  follows continua in the complex domain into their singularities. Note the contrast
  with HM06 (mutual distances + BKK) and with our cclib (mutual distances + enriched
  system): a second, genuinely different formulation worth implementing for
  cross-validation (candidate instrument for CC-P2).
- **Standing hypothesis**: no nonempty subset of bodies has total mass zero (their
  weak mass hypothesis; positivity is only needed for the final statements).
- **History (primary quotes)**: Chazy 1918 postulated nondegeneracy of all CCs (and
  hence mass-independent finite counts); the postulate is FALSE: Palmore 1975 gave a
  degenerate CC (equilateral triangle of unit masses + central mass
  (64 sqrt(3) + 81)/249); Simo 1978 showed the count varies with masses; Xia counts
  exactly on nonexplicit open mass sets. Wintner 1941 believed finiteness (sections
  360/365 quoted verbatim in the PDF); his stronger belief (q_n bounded as n -> infty)
  is self-contradicted by Moulton's n!/2. Palmore's topological lower bound: more than
  (n-1)!(n-2) SO(2)-classes when all CCs are nondegenerate (Poincare polynomial of
  the configuration space; Conley index for collinear saddles).
- **Related works pinned by AK12's intro**: Hampton (symmetric planar 5-body
  finiteness except a polynomial mass condition; exact citation to pin at CCB-023);
  Hampton-Jensen (spatial, improving Moeckel 2001); Lee-Santoprete (5 equal masses,
  new method).

New candidate instrument recorded (lens 7, reformulation): the AK12
delta-variable polynomial system as a THIRD exact formulation in cclib, for
cross-implementation agreement checks (methodology/03 route 3).
