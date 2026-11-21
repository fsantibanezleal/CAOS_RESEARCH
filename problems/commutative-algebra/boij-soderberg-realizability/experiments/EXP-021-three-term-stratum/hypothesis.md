# EXP-021 preflight: the stratum S(5; 0, 1) at (11, 3), the pairs x^11 + alpha(xy, z) x + gamma(xy, z) y^9, y^11 + beta(xy, z) y + delta(xy, z) x^9, enumerated completely over GF(3)

Date: 2026-11-20. Status: frozen before any computation of this experiment on the pair (11, 3). CPU only. Exact
arithmetic (integers modulo a prime).

## Question

After EXP-020 the pair (e, p) = (11, 3) is the only pair with e <= 16 and p an odd prime below 2e where the point
(1, 2, 2, 1) of (0, e, 3e, 4e) is not settled over U. Nothing known reaches it: 3 does not divide 11 * 10 (the
criterion for a central commutator), 11 is prime (no pull-back), 3 is neither 2e - 1 nor 2e - 3, and the pairs
x^e + alpha y^t, y^e + beta x^t have no allowed exponent (t = 1 is the only one with 2t <= p - 1, and 3 divides
e + t = 12). Of the admissible strata of e = 11, the proposition on the characteristic dividing the modulus and the
projection on the weight-zero summand leave S(2; 0, 1) and S(5; 0, 1) (backlog BSB-038).

The stratum S(5; 0, 1) (convention of EXP-010: the weight of x^a y^b z^c is b + c, f on the monomials of class 0
modulo 5 and g on those of class 1) is, for e = 11, the family

    f = a x^11 + alpha(xy, z) x + gamma(xy, z) y^9,      g = b y^11 + beta(xy, z) y + delta(xy, z) x^9,

alpha, beta of degree 5 and gamma, delta of degree 1 in xy and z: nine monomials each. For every odd e the same shape,
x^e + alpha x + gamma y^(e-2), y^e + beta y + delta x^(e-2) with alpha, beta of degree d = (e - 1)/2, is the stratum
S(d; 0, 1). A member with a = 0 or b = 0 has no quotient of finite length: z is central, so M/zM = k[x, y]/(f, g
modulo z) is a quotient of M = U/(Uf + Ug); modulo z every monomial of g is divisible by y and every monomial of f
other than x^e is divisible by y, so for a = 0 both lie in (y) and k[x] is a quotient of M; and every monomial of f is
divisible by x modulo z, and every monomial of g other than y^e too, so for b = 0 the quotient k[y] appears. So only
the members with a = b = 1 (up to scalars) matter: p^(e+5) of them, 3^16 = 43,046,721 at (11, 3).

For a pure pair of a stratum the resolution is homogeneous for the class (note
`context/2026-11-20-weight-class-strata.md`, proposition of the section 'The condition', reviewed), and for
S(d; 0, 1) with e = 5, 7, 9, 11, 13 exactly one triple of classes of the syzygies keeps the class-wise Hilbert
function nonnegative: (s1, s2, t) = (0, 1, 0) for e = 5 and (1, 2, 2) for e = 7, 9, 11, 13 (the test `admissible` of
EXP-010, listing every triple). So for a pure pair the block of mu_3e of class s1 and the block of class s2 each have
rank one less than their number of rows and every other block has full row rank. This pattern is a necessary
condition for a pure pair that costs one small rank for most members.

Evidence, all on settled pairs (probe of the coordinating session; scripts and logs under the data root,
`caos-research/boij-soderberg-realizability/EXP-021-probe/`):

| (e, p) | Members examined | Pure Hilbert function (plain staged test) | Share | Remark |
|---|---|---|---|---|
| (5, 3) | all 59,049 | 1,736 | 2.9 x 10^-2 = 0.26 x 3^-2 | 400 pure pairs (every member tabled); 1,664 of the 1,736 have the block pattern, and the 400 are among them |
| (5, 7) | 100,000 random | 1,997 | 2.0 x 10^-2 = 0.98 x 7^-2 | |
| (7, 5) | 400,000 random | 233 | 5.8 x 10^-4 = 0.36 x 5^-4 | |
| (9, 5) | 1,000,000 random | 20 | 2.0 x 10^-5 = 0.31 x 5^-6 | |

The share follows p^-(e-3) times a factor between 0.26 and 1. If that holds at (11, 3), about 0.26 x 3^8 = 1,700
members of the 43 million have the pure Hilbert function, and at (5, 3) a quarter of such members are pure pairs.
Against it: at (5, 3) none of the 486 members that the exchange of x and y carries to themselves is pure (28 have the
pure Hilbert function), where the same members hold many pure pairs at (5, 7), (7, 5), (9, 5), (9, 7) and (11, 7); so
characteristic 3 behaves differently in a part of the family, and (5, 3) is the only settled pair of this shape in
characteristic 3. At (5, 3) the members with gamma = delta = 0 hold no pure pair (22 with the pure Hilbert function
and the pattern), those with delta = 0 hold 58.

Question: does the complete list of the monic members of S(5; 0, 1) hold a pure pair over GF(3) at e = 11?

State when this file is frozen: no member of any stratum was computed at (11, 3) by this experiment or by its probe
(the probe scripts refuse the pair). EXP-006 to EXP-020 did not reach the pair.

## Definitions fixed here

- A member, for odd e and a prime p, d = (e - 1)/2: the pair of forms (PBW monomials x^a y^b z^c of `uhlib`)
  f = x^e + [gamma part] + [alpha part], g = y^e + [delta part] + [beta part] with coefficients in GF(p) on
  - delta part: g on x^(e-1) y, x^(e-2) z (2 coefficients);
  - gamma part: f on x y^(e-1), y^(e-2) z (2 coefficients);
  - alpha part: f on x^(d+1-c) y^(d-c) z^c for c = 0, ..., d (d + 1 coefficients);
  - beta part: g on x^(d-c) y^(d+1-c) z^c for c = 0, ..., d (d + 1 coefficients).
  Its digits are these e + 5 coefficients (residues 0, ..., p - 1) in the order delta, gamma, alpha, beta, each part in
  the order written; its index is the integer with these digits in base p, the first digit the most significant. The
  list is complete: p^(e+5) members. The members of index below p^(e+3) are those with delta = 0; below p^(e+1), those
  with gamma = delta = 0.
- The blocks: mu_3e (rows a f and a g for the monomials a of degree 2e, written on the monomials of degree 3e) is
  block diagonal by the class of the column modulo d (routine of EXP-010, imported, not edited). (s1, s2) is the pair
  of syzygy classes of the only admissible triple: (0, 1) for e = 5, (1, 2) for e = 7, 9, 11.
- The stage of a member: 0 when the block of class s1 does not have rank (rows - 1); 1 when that block has it and
  another block does not have its rank (rows - 1 for the class s2, rows for every other class; blocks tested in the
  order s1, s2, then the other classes increasing, stopping at the first failure); 2 when every block has its rank
  and the staged test of EXP-010 (the ranks of mu_n for n = 3e - 1 and 3e + 1, ..., 4e - 3) fails; 3 when it passes:
  the member has the pure Hilbert function and the block pattern.
- Pure means: the Betti table computed by `uhlib` is (1, 2, 2, 1) on (0, e, 3e, 4e) and the length is e^3.
- Betti tables: at (11, 3), on the members of stage 3 in the order of their index, until 5 pure members are found or
  40 tables are computed; the enumeration always continues to the end of the list (the counts are of the whole list).
  In the controls (5, 3) and (7, 5) every member of stage 3 is tabled.
- A random sample of a control: blocks of 20,000 members; the block that starts at position `start` has its digits
  drawn by numpy `default_rng([20261120 + 1000 e + p, start]).integers(0, p, size=(n, e + 5))`, one row per member.

## Cases (fixed here)

Family K, controls (the counts are those of the probe with the reference implementation `probe_canonical.py`):

| Case | Members | Stages 0, 1, 2, 3 | Tables on stage 3 | Pure |
|---|---|---|---|---|
| (5, 3), complete list by index | 59,049 | 44,175; 7,526; 5,684; 1,664 | 1,664 | 400 (58 with delta = 0, none with gamma = delta = 0); the first pure indices are 866 and 919 |
| (7, 5), random sample | 400,000 | 316,708; 64,914; 18,166; 212 | 212 | 64 |
| (11, 7), random sample | 200,000 | 196,061; 3,249; 690; 0 | none | none |

and, at (5, 3), the 73,447 normalized members of S(2; 0, 1) (enumeration of EXP-010) in which the coefficient of x^5
in f or of y^5 in g is zero: none reaches stage 3 (stages 60,933; 3,942; 8,572; 0).

Family X, the open pair: (11, 3), the complete list, 43,046,721 members, in the order of the index, in blocks of
20,000 members.

Order of the run: the gates; family K; family X.

## Gates (a failed gate stops the run and no verdict is drawn until it is explained)

- G1 (known answers, family K): every count of the table of the controls is reproduced exactly, the non-monic members
  at (5, 3) included; at (5, 3) the number of members with the pure Hilbert function by the plain staged test of
  EXP-010 (no pattern) is 1,736.
- G2 (second instrument): for every case with a pure member, Singular 4.3.2 (Plural), with a script generated from the
  stored polynomials, gives the pure Betti table on the first three pure members.
- G3 (unit tests): the admissible triples of S(d; 0, 1) for e = 5, 7, 9, 11, 13 are [(0, 1, 0)] and four times
  [(1, 2, 2)]; the rows of the blocks of mu_33 at e = 11 are 57, 59, 59, 57, 56; the digits, the index and the
  monomials of a member (the members of indices 0, 1, 3^14 and 3^16 - 1 at e = 11 written out; the index of a member is
  recovered from its coefficient vectors; every member lies in S(d; 0, 1)); the stages of the first 3,000 members at
  (5, 3) equal those of a direct computation that ranks every block; a member of stage 3 passes the plain staged test;
  the plan of the cases.

## Predictions

- P1 (a pure pair at (11, 3), confirmed by both instruments): 0.8.
- P2 (the number of members of stage 3 in the complete list at (11, 3) is between 200 and 4,000): 0.6.
- P3 (the members with delta = 0, the first 3^14 = 4,782,969 of the list, hold a pure pair): 0.6.
- P4 (no pure pair is found among the members with gamma = delta = 0, the first 3^12 = 531,441): 0.7.
- P5 (of the Betti tables computed at (11, 3), between one tenth and six tenths are pure): 0.6, given P1.

What would falsify, and what each outcome means. A pure member confirmed by the second instrument settles (11, 3): the
point (1, 2, 2, 1) of (0, 11, 33, 44) is realized over U in characteristic 3, and for 2 <= e <= 16 the point of
(0, e, 3e, 4e) fails only in characteristic 2. A complete list without a pure member says that S(5; 0, 1) holds no
pure pair over GF(3) at e = 11 (every pure pair of the stratum has the block pattern, by the proposition of the note,
and every member with the pattern and the pure Hilbert function is tabled unless 40 tables were computed without 5
pure ones, in which case the remaining members of stage 3 are tabled before the verdict); it says nothing about S(2; 0,
1) or about fields larger than GF(3). A pure pair without the block pattern cannot be seen by this experiment; the
control at (5, 3), where the 400 pure pairs of the complete list were found by a method without the pattern, is the
check of that.

## Method and budget

- First instrument: the routine of EXP-010 (the block ranks of mu_n with python-flint, the staged test, the Betti
  table by `uhlib`), imported, not edited; second instrument: Singular 4.3.2 with Plural through the script generator
  of EXP-009.
- At most 12 worker processes. Family K: 30 minutes of wall time. Family X: 4 hours of wall time, resumable, stored
  per block of 20,000 members; a list that does not finish is reported with the range of indices done, and no
  statement about the whole stratum is drawn from it.
- Stored per case: the counts by stage (per block for family X, so that the counts of the members with delta = 0 and
  with gamma = delta = 0 can be read), every member of stage 3 (index, digits, the two coefficient vectors, the
  readable polynomials, the Betti table when computed), the seconds.

## Outputs

`exp021_routine.py`, `run.py`, `make_summary.py`, the tests, `artifacts/results.json`, `artifacts/singular/` (scripts
only), `results-summary.md` generated from the results. The verdict is written by the coordinating session after its
own re-check of the decisive members with a separate parser and the module construction of `uhlib`.
