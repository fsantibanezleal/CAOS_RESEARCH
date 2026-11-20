# EXP-006 preflight: the point (1,2,2,1) on (0, e, 3e, 4e) over U(H) in odd characteristic below 2e

Date: 2026-11-20. Status: frozen before any computation of this experiment. CPU only. Exact arithmetic (finite
fields; integers modulo a prime, and extension fields by exact tables).

## Question

Over U = U(H) the point (1,2,2,1) of the ray (0, e, 3e, 4e) is realized by U/U(x^e, y^e) exactly when the
characteristic is 0 or at least 2e (Theorem A of the manuscript), and it is realized by no module in characteristic 2
for every e >= 2 (Theorem C). For e = 2 this settles every characteristic: the pair f = x^2 + y^2 + yx,
g = x^2 + yx - z is pure in characteristic 3 (EXP-003). For e >= 3 the odd characteristics p < 2e are open: the module
of the family fails there, and nothing is known about other pairs of forms of degree e.

Question: for e = 3 (p = 3, 5) and e = 4 (p = 3, 5, 7), is there a pair of forms f, g of degree e over GF(p) such that
U/(Uf + Ug) has the pure Betti table (1,2,2,1) on (0, e, 3e, 4e)? A pair over GF(p) answers the question for every
field of characteristic p, because Betti tables do not change under an extension of the base field.

Only cyclic modules are searched: a module with that table has one generator and two relations of degree e, so it is
U/(Uf + Ug) for a two-dimensional space W = <f, g> of forms of degree e. The search space is the Grassmannian
G = Gr(2, U_e).

## Derivations made before the run

Notation: u(n) = dim U_n (1, 2, 4, 6, 9, 12, 16, 20, 25, 30, 36, 42, 49, 56, 64, 72, 81 for n = 0..16). For W in G
let mu_n(W): U_(n-e) tensor W to U_n be left multiplication, so that the Hilbert function of M_W = U/(U W) is
H_W(n) = u(n) - rank mu_n(W). The Hilbert function of the pure table is
h_e(n) = u(n) - 2 u(n-e) + 2 u(n-3e) - u(n-4e).

1. e = 3. h_3 = (1, 2, 4, 4, 5, 4, 4, 2, 1) in degrees 0 to 8 and 0 from degree 9 on (length 27). It equals the
   maximal-rank function max(0, u(n) - 2 u(n-3)) in every degree (u(9) - 2 u(6) = -2). So the pure Hilbert function is
   the generic one: the set of W with H_W = h_3 is open in G. EXP-003 (claim D1) found a random pair of cubics pure over
   GF(32003).

2. e = 4. h_4 = (1, 2, 4, 6, 7, 8, 8, 8, 7, 6, 4, 2, 1) in degrees 0 to 12 and 0 from degree 13 on (length 64). The
   maximal-rank function agrees up to degree 11 and is 0 in degree 12 (u(12) - 2 u(8) = 49 - 50 = -1), where
   h_4(12) = 1. So a pure pair is special: mu_12(W), a map from a space of dimension 50 to one of dimension 49, must
   have rank 48 and not 49. (EXP-003 observed this: the pair (x^4, y^4) has one more dimension than a general pair in
   degree 12, and 0 of 5 random pairs over GF(32003) were pure.)

3. The locus D = {W in G : rank mu_12(W) <= 48} is not empty, over every algebraically closed field. On G (dimension
   2 (9 - 2) = 14) mu_12 is a map of vector bundles from S tensor U_8 = S^(+25) (rank 50, S the tautological
   subbundle) to the trivial bundle of rank 49. By the formula of Thom and Porteous (Fulton, Intersection Theory,
   Theorem 14.4) the locus of rank at most 48 has expected codimension (50 - 48)(49 - 48) = 2 and, when it has that
   codimension or is empty, its class is c_1^2 - c_2 for c = c(O^49 - S^(+25)) = c(Q)^25, Q the tautological quotient.
   With c_1(Q) = sigma_1 and c_2(Q) = sigma_2: c_1 = 25 sigma_1, c_2 = 25 sigma_2 + 300 sigma_1^2, and
   c_1^2 - c_2 = 325 sigma_1^2 - 25 sigma_2 = 300 sigma_2 + 325 sigma_(1,1), which is not zero in the Chow ring of
   Gr(2, 9) (the same free abelian group in every characteristic). Hence D is not empty and each of its components has
   dimension at least 12. In characteristic 2, D is all of G (Theorem C: every M_W is infinite there).

4. What the derivation does not give. A point of D is pure only if, in addition, the rank is exactly 48, mu_n(W) is
   injective for n <= 11, M_W vanishes in degree 13, and the Betti table has no cancelling pair. These hold on a subset
   of D that is open in D and may be empty in a given characteristic. In characteristic 0 or at least 8 it contains the
   orbit of <x^4, y^4> under GL_2, which has dimension 2, far less than 12: if D is irreducible of dimension 12 there,
   the family of the manuscript is a small part of a larger family of pure modules.

5. Counting heuristic (Lang and Weil; an order of magnitude, not a theorem here): if the pure locus has a
   geometrically irreducible component of dimension 12 defined over GF(q), a uniformly random W over GF(q) is pure
   with probability about q^(-2): 11 percent at q = 3, 4 percent at q = 5, 2 percent at q = 7, 0.8 percent at
   q = 11, 0.6 percent at q = 13.

## Cases (fixed here; a random space is drawn with the seed 20261120 + its index in its family, as a uniformly random 2 by u(e) matrix of rank 2)

| Family | e | Field | Spaces W | What is computed |
|---|---|---|---|---|
| A1 | 3 | GF(3) | all 11,011 two-dimensional subspaces of U_3 | H_W to degree 10; Betti table when H_W = h_3 |
| A2 | 3 | GF(5), GF(9), GF(25), GF(27) | 2,000 random per field | the same |
| B1 | 4 | GF(3), GF(5), GF(7) | 20,000 random per field | rank mu_12; when it is 48, H_W to degree 14 and, when H_W = h_4, the Betti table |
| B2 (control) | 4 | GF(11), GF(13) | 20,000 random per field | the same; for each pure W, whether it lies in the orbit of <x^4, y^4> under GL_2 of the field and of its quadratic extension (W contains two fourth powers of linear forms) |
| B3 | 4 | GF(9) | 20,000 random | the same as B1 |
| C (exploration) | 5 | GF(3) | 50,000 random | H_W to degree 18; Betti table when H_W = h_5 |

For e = 5: h_5 = (1, 2, 4, 6, 9, 10, 12, 12, 13, 12, 12, 10, 9, 6, 4, 2, 1) in degrees 0 to 16 and 0 from degree 17
on (length 125). The maximal-rank function agrees up to degree 14 and is 0 in degrees 15 and 16, where h_5 is 2 and 1:
a pure pair needs rank 70 for mu_15 (a map between spaces of dimension 72), expected codimension 4 in Gr(2, 12). No
frequency is predicted for family C.

## Gates (a failed gate stops the run and no verdict is drawn until it is explained)

- G1 (known answers). Over GF(11) and GF(13) the pair (x^4, y^4) and, over GF(5) and GF(7), the pair (x^3, y^3) (p at
  least 2e in each case) have the pure Betti table; over GF(3), GF(5) and GF(7) the pair (x^4, y^4) does not, and over
  GF(3) and GF(5) the pair (x^3, y^3) does not; over GF(3) the pair f = x^2 + y^2 + yx, g = x^2 + yx - z has the pure
  table on (0, 2, 6, 8). All as in EXP-003 and Theorem A.
- G2 (the formula). The routine's h_e equals the Hilbert function of U/U(x^e, y^e) computed over GF(32003) for
  e = 3, 4, 5.
- G3 (second instrument). For every space reported pure in A1 (a fixed sample of 50, the first in the enumeration
  order), A2, B1, B2, B3 and C (the first 20 per field in each family), Singular 4.3.2 (Plural), with a script generated
  from the stored basis of W and sharing no arithmetic code with the first instrument, gives the same Betti table.
- G4 (unit tests) of the rank routine at degree 3e against the module construction of `uhlib`, of the random subspace
  generator (rank 2 always; the same seed gives the same space), and of the orbit test of B2 on spaces built in the
  orbit and on spaces built outside it.

## Predictions

- P1 (e = 3). Pure pairs of cubics exist over GF(3) and over GF(5). Over GF(25) and GF(27) at least half of the random
  pairs are pure. So the point (1,2,2,1) of (0, 3, 9, 12) is realized over U in every characteristic other than 2.
  Confidence 0.85 for existence in characteristic 5, 0.7 in characteristic 3.
- P2 (e = 4, the locus D). In each of the six fields of B1, B2 and B3 the share of random W with rank mu_12 at most 48
  is between 0.3 q^(-2) and 3 q^(-2). (Derivation 3 with heuristic 5. Confidence 0.7.)
- P3 (e = 4, pure pairs). Pure pairs of quartics exist over GF(3), GF(5) and GF(7). So the point (1,2,2,1) of
  (0, 4, 12, 16) is realized over U in every characteristic other than 2. Confidence 0.6 for each prime: derivation 4
  names what could fail.
- P4 (control). Over GF(11) and GF(13) pure pairs exist outside the orbit of <x^4, y^4>: the family of the manuscript
  is not the only pure cyclic module on this ray. Confidence 0.75.

What would falsify, and what each outcome means: no pure pair in a family where the rank condition is met on at least
50 spaces is evidence, not proof, that the point is not realized by a module over that prime field; it would make
that characteristic a candidate for a second characteristic-dependent point and calls for an exhaustive search or a
proof before any statement. A pure pair found is a proof of realizability in that characteristic once the second
instrument confirms its Betti table. A share far outside the interval of P2 says that heuristic 5 does not apply
(for instance D reducible or of larger dimension); the counts are then reported as they are.

## Method and budget

- First instrument: `code/uhlib` (algebra, fields, the Betti table through Tor against the resolution of the trivial
  module, as in EXP-003) with a rank routine for mu_n(W) over a finite field (exact; numpy integer arithmetic modulo
  p or exact tables for the extension fields; never floating point).
- Second instrument: Singular 4.3.2 with Plural in WSL, as in EXP-003.
- At most 8 worker processes, at most four hours of wall time. Every space reported with rank at most 48 (e = 4) or
  with the pure Hilbert function is stored with its field, seed and basis.

## Outputs

`run.py`, the routine and its tests; `artifacts/results.json` (per family and field: the counts by rank of mu_3e, by
Hilbert function, the pure spaces with their bases, the orbit test), `artifacts/run.log`, `artifacts/singular/`,
and `results-summary.md` generated from the results. The verdict is written by the coordinating session after its own
re-checks of the pure pairs.
