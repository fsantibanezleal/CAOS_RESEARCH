# Literature pass before EXP-001, 2026-11-19 (methodology 12, P1)

Four research lanes (the cyclic and level case; integral points and minimal multiples after Erman 2009; U(H) and
noncommutative Boij-Soderberg; follow-ups and tooling) read the literature beyond the 2026-09-02 dossier; twelve items
that change the experiment were re-read on their primary texts by independent skeptics. The full report, with every
quote, URL and search, is kept in the private management mirror (`wip/caos-research/bs-source-complete-2026-11-19.md`).
Marks: [V] read on the primary text, [V2] secondary, [D] derived, [U] not confirmed. Item identifiers (L1.1, L2.2, ...)
are those of the report. No negative search is a novelty proof.

Sources behind the items: J. Soderberg, Graded Betti numbers and h-vectors of level modules, arXiv:math/0612047v2
(Proposition 4.1) [L1.1]; the Macaulay2 BoijSoederberg documentation pages of pureCharFree, pureTwoInvariant, pureWeyman,
pureAll, randomModule and randomSocleModule (outputs over ZZ/101) [L2.1, L2.2]; A. Boocher, N. Huang, H. Wolf, Arithmetic
in the Boij-Soderberg cone, arXiv:2512.24320v1 (Theorems 3, 15, 21, Remark 14) [L2.4, L4.1]; S. V. Sam, Homology of
analogues of Heisenberg Lie algebras, arXiv:1307.1901v2 (Theorem 2.1, Kostant) with Erman-Sam 2016, Section 6 [L3.2, L3.3];
the Singular manual on Plural resolutions [L4.8].

Main changes to the picture of the dossier:

- Over S the census moves from 52 realized, 12 obstructed, 156 undecided to 68, 12, 140 (Table A), with fields stated.
- The least realizable multiple is 2 on the two d3 = 10 counterexample rays (Table B): the primitive point is the
  only missing point there.
- Over U(H), Kostant's theorem for sp_4 gives pure modules L(p,q) with beta = (q+1, p+2, p+2, q+1) on
  (0, p-q+1, p+q+3, 2p+4) in characteristic 0 (Table F): eleven primitive points with d3 <= 12, among them six of the ten
  S-obstructed parity-passing rays. The primitive points of (0,2,6,8), (0,3,9,12) and (0,2,10,12) were left open by the
  pass; EXP-002 addresses them.
- Boocher, Huang and Wolf (December 2025) describe the rays with B1 = 2 as a Pell family whose second member is the
  ray (0,6,20,21) of the Rethlas paper, and list (0,1,4,5,6) in codimension 4: the polynomial-ring half of both Rethlas
  examples has that antecedent, to be cited.

### Verdicts on the twelve experiment-changing items

| Item | Claim | Verdict | Main correction |
|---|---|---|---|
| L1.1 | Soderberg Prop 4.1 realizes a multiple on every (0,a,a+1,d3) | CONFIRMED | beta_0 = binom(d3-a,2); m = 1 on 25 of 55 rays; existence via Boij 2000 (unread); infinite field |
| L1.2 | BHW (lane-1 reading): (0,3,4,8) at L = 1; B1 = 2 and sum < 12 lists | NOT CONFIRMED | gcd = 1 restriction misses scaled census rays; no module given for L = 1; BE 1973, not Buchsbaum-Rim |
| L1.5 | General forms realize 31 cyclic points (Froberg match) | NOT CONFIRMED | settles no ray; purity unproved; breakdown of the 13 non-matching points corrected |
| L2.1 | c_d = 2 on (0,4,9,10) and (0,1,6,10) | CONFIRMED | shown over characteristic 101 and 5 (and 32003 for the first ray); dual ray by Ext^3 duality |
| L2.2 | Primitive point realized on 5 undecided rays (docs) | CONFIRMED | 6 newly closed ((0,6,7,9) added); characteristic 101; pureAll label i10 |
| L2.4 | BHW numeric lower bounds and classification | CONFIRMED | commutative only; Koszul rays exempt; counts are gcd = 1 |
| L2.10 | d1 Pieri complexes per ray give candidate multiples | NOT CONFIRMED | only the EFW member has finite length |
| L3.2 | Kostant gives pure U(H)-modules L(p,q) | CONFIRMED | duals in the quote; characteristic 0; exact CE check over Q |
| L3.3 | U(H) realizations with d3 <= 12 | CONFIRMED | (0,2,10,12) primitive also open; (0,3,7,10) newly answered |
| L4.1 | Rethlas ray is n = 2 of the BHW Pell family | CONFIRMED | preprint, not in print; typos; S half only |
| L4.7 | Macaulay2 has no noncommutative resolution; tools not installed | NOT CONFIRMED | NCAlgebra exports one; M2 1.22 and Singular 4.3.2 installed in WSL |
| L4.8 | Singular Plural resolves over G-algebras incl. U(H) | CONFIRMED | Heisenberg example is sing_458; betti() unreliable, read degrees |


### Table A: primitive point newly realized over S (dossier Appendix A status UNDECIDED)

Every multiple of a realized primitive point is realized (direct sums), so c_d = 1 on these rays, in the stated field.

| Ray | Primitive beta | Item | Exact statement | Field |
|---|---|---|---|---|
| (0,1,3,6) | (5,9,5,1) | L2.2 | pureWeyman: "i13 : betti res randomSocleModule({0,1,3,6},1) / o13 = total: 5 9 5 1" | char 101 (doc); QQ by skeptic run [D] |
| (0,2,3,6) | (2,9,8,1) | L2.2 | pureCharFree: "i13 : betti res randomSocleModule({0,2,3,6},1) / o13 = total: 2 9 8 1" | char 101; QQ [D] |
| (0,3,4,6) | (1,8,9,2) | L2.2 | pureCharFree: "i4 : L1 = {0,3,4,6}" ... "o10 = total: 1 8 9 2" | char 101; QQ [D] |
| (0,3,5,6) | (1,5,9,5) | L2.2 | pureWeyman: "i4 : L1 = {0,3,5,6}" ... "o10 = total: 1 5 9 5" | char 101; QQ [D]; ZZ/2 0/5 draws |
| (0,4,5,7) | (3,35,42,10) | L2.2, L1.1 | pureTwoInvariant: "i4 : L1 = {0,4,5,7}" ... "o10 = total: 3 35 42 10"; Prop 4.1 with s = binom(3,2) = 3, t = binom(5,2) = 10 | char 101; infinite field (L1.1); ZZ/2, ZZ/3 0/5 draws |
| (0,2,3,7) | (10,42,35,3) | L2.2, L1.1 | pureTwoInvariant: "i13 : betti res randomSocleModule({0,2,3,7},1) / o13 = total: 10 42 35 3"; Prop 4.1 with s = binom(5,2) = 10, t = binom(3,2) = 3 | char 101; infinite field; ZZ/2 0/5 draws |
| (0,2,3,9) | (7,27,21,1) | L2.2 | pureAll: "i8 : betti res randomSocleModule(L,1) / o8 = total: 7 27 21 1" with L = {0,2,3,9} | char 101; QQ [D] |
| (0,6,7,9) | (1,21,27,7) | L2.2 | pureAll: "i10 : betti res randomModule({0,6,7,9},1) / o10 = total: 1 21 27 7" | char 101; QQ [D] |
| (0,2,3,10) | (28,105,80,3) | L1.1 | Prop 4.1 with j = 1, c = 7: s = r_6 = binom(8,2) = 28, t = r_1 = binom(3,2) = 3 | infinite field |
| (0,7,8,10) | (3,80,105,28) | L1.1 | Prop 4.1 with j = 6, c = 7: s = binom(3,2) = 3, t = binom(8,2) = 28 | infinite field |
| (0,4,5,11) | (21,165,154,10) | L1.1 | Prop 4.1 with j = 3, c = 8: s = binom(7,2) = 21, t = binom(5,2) = 10 | infinite field |
| (0,6,7,11) | (10,154,165,21) | L1.1 | Prop 4.1 with j = 5, c = 8: s = binom(5,2) = 10, t = binom(7,2) = 21 | infinite field |
| (0,2,6,12) | (5,9,5,1) | L2.2 plus scaling | dossier 1.4 scaling lemma [D] applied to (0,1,3,6), e = 2 | as (0,1,3,6) |
| (0,4,6,12) | (2,9,8,1) | L2.2 plus scaling | scaling lemma [D] applied to (0,2,3,6), e = 2 | as (0,2,3,6) |
| (0,6,8,12) | (1,8,9,2) | L2.2 plus scaling | scaling lemma [D] applied to (0,3,4,6), e = 2 | as (0,3,4,6) |
| (0,6,10,12) | (1,5,9,5) | L2.2 plus scaling | scaling lemma [D] applied to (0,3,5,6), e = 2 | as (0,3,5,6) |

(0,2,3,7) and (0,2,3,9) were noted in the dossier's text (Section 4.2) but are UNDECIDED in its mechanical table. The
census over S becomes 68 realized, 12 obstructed, 140 undecided. The Soderberg m = 1 rays already realized in the dossier
((0,1,2,d3), (0,d3-2,d3-1,d3)) are a second construction for those rays.

### Table B: c_d settled on rays obstructed at m = 1

| Ray | Primitive beta | Item | Exact statement | c_d |
|---|---|---|---|---|
| (0,4,9,10) | (1,3,8,6) | L2.1 | "i4 : betti res randomModule(L,2)" "o4 = total: 2 6 16 12" (row 3 ". 6 . .", row 7 ". . 16 12"); same at `CoefficientRing=>ZZ/5`; m = 1 obstructed by the dossier's regular-sequence argument (4.3) | 2 over char 101 and 5 (and 32003, package Test 17); all m >= 2 over ZZ/101 (m = 2, 3 realized) |
| (0,1,6,10) | (6,8,3,1) | L2.1 plus duality | Ext^3 duality (dossier 1.4 [D]) of the L2.1 module; skeptic run: Ext^3 table 2*(6,8,3,1); m = 1 obstructed (Erman Prop 3.1(2) equality case) | 2 over the same fields |

Already in the dossier and unchanged: c_d = 2 on (0,1,3,4), (0,1,5,6), (0,1,7,8), (0,1,9,10), (0,1,11,12) (ES multiple 2,
primitive obstructed); the L3.3 skeptic notes c_d = 2 also on (0,2,6,8), (0,3,9,12), (0,2,10,12) over S by flat pullback
of the 2x tables [D]. L2.8 (EES Prop. 8.1, [D] reading) is consistent with c_d = 2 on (0,1,3,4).

### Table C: upper bounds c_d <= m from Soderberg Prop 4.1 on still-undecided rays (L1.1)

Exact statement for every row: Proposition 4.1 with p = 3, j = a-1, c = d3-3; the realizing module has s = binom(d3-a,2)
generators and socle type t = binom(a+1,2), so it realizes m = s/beta_0 times the primitive point (infinite field).

| Ray | Primitive beta | s, t | m (bound) | Dossier ES multiple |
|---|---|---|---|---|
| (0,2,3,8) | (5,20,16,1) | 15, 3 | 3 | 7 |
| (0,3,4,8) | (5,32,30,3) | 10, 6 | 2 | 7 |
| (0,4,5,8) | (3,30,32,5) | 6, 10 | 2 | 7 |
| (0,5,6,8) | (1,16,20,5) | 3, 15 | 3 | 7 |
| (0,3,4,9) | (5,30,27,2) | 15, 6 | 3 | 14 |
| (0,5,6,9) | (2,27,30,5) | 6, 15 | 3 | 14 |
| (0,3,4,10) | (7,40,35,2) | 21, 6 | 3 | 18 |
| (0,4,5,10) | (3,25,24,2) | 15, 10 | 5 | 42 |
| (0,5,6,10) | (2,24,25,3) | 10, 15 | 5 | 42 |
| (0,6,7,10) | (2,35,40,7) | 6, 21 | 3 | 18 |
| (0,2,3,11) | (12,44,33,1) | 36, 3 | 3 | 10 |
| (0,3,4,11) | (14,77,66,3) | 28, 6 | 2 | 15 |
| (0,7,8,11) | (3,66,77,14) | 6, 28 | 2 | 15 |
| (0,8,9,11) | (1,33,44,12) | 3, 36 | 3 | 10 |
| (0,2,3,12) | (15,54,40,1) | 45, 3 | 3 | 11 |
| (0,3,4,12) | (6,32,27,1) | 36, 6 | 6 | 55 |
| (0,4,5,12) | (14,105,96,5) | 28, 10 | 2 | 33 |
| (0,5,6,12) | (7,72,70,5) | 21, 15 | 3 | 66 |
| (0,6,7,12) | (5,70,72,7) | 15, 21 | 3 | 66 |
| (0,7,8,12) | (5,96,105,14) | 10, 28 | 2 | 33 |
| (0,8,9,12) | (1,27,32,6) | 6, 36 | 6 | 55 |
| (0,9,10,12) | (1,40,54,15) | 3, 45 | 3 | 11 |

The other eight m > 1 rays of the family are already realized at m = 1: (0,2,3,5), (0,3,4,7), (0,4,5,9), (0,5,6,11)
(Pfaffian, dossier) and (0,2,3,6), (0,3,4,6), (0,2,3,9), (0,6,7,9) (Table A).

Claimed but not reproduced: L1.2 / L2.4 source text, BHW Example 9: "in fact there actually is a module with L = 1 which
can be discovered by some experimentation with Macaulay2" for (0,3,4,8) (5,32,30,3). No module, field or seed is given;
the dual (0,4,5,8) follows by duality as an inference. Status: UNDECIDED with 1 <= c_d <= 2, primitive realization
UNVERIFIED (a target for EXP-001). The same paragraph's pureAll values (35, 175, 10) give the construction bound 2.

### Table D: lower bounds over S (L = 1 excluded), commutative rings, any field

| Ray | Primitive beta | Item | Exact statement |
|---|---|---|---|
| (0,1,3,4) | (1,2,2,1) | L2.4, L4.1 | proof of Thm 3: "the Krull altitude theorem rules out the first sequence"; Thm 3: "L must be at least 2" |
| (0,2,6,8), (0,3,9,12) | (1,2,2,1) | L2.4 (scaling inference) | same B as (0,1,3,4); the paper restricts to gcd = 1, the carry-over is the skeptic's inference |
| (0,1,5,6) | (2,3,3,2) | L2.4, L4.2 | "The third violates the general fact that beta1(M) >= beta0(M) + (c - 1) (see e.g. Theorem 2.1 in [5])" |
| (0,2,10,12) | (2,3,3,2) | L2.4 (scaling inference) | same B as (0,1,5,6) |
| (0,3,5,8) | (1,4,4,1) | L2.4, L4.2, L2.5 | "the sequence {1, 4, 4, 1} is not the betti sequence of a module because an almost complete intersection is never Gorenstein"; Kunte Remark 5.7: "The first case of Corollary 5.6 is (0, 3, 5, 8)" |

All six were already obstructed in the dossier; these items give a second printed route. No other census ray has B1 < 3,
B2 < 3 or primitive sum < 12 outside the exempt Koszul rays (script output above), so the BHW bounds obstruct nothing new
with d3 <= 12. Outside the window: (0,6,20,21) (1,2,9,8) and its dual (0,1,15,21) (8,9,2,1) get L >= 2 (n = 2 of
Theorem 15).

### Table E: Froberg comparison for cyclic points (L1.5, not confirmed; no ray settled)

Reproduced by this synthesis: of the 44 cyclic primitive points with d3 <= 12, 31 have the Hilbert function of beta_1
general forms of degree d1. Still UNDECIDED after Table A and matching: (0,4,6,7) (1,7,14,8), (0,5,6,8) (1,16,20,5),
(0,5,8,9) (1,6,15,10), (0,6,8,9) (1,12,27,16), (0,7,9,10) (1,15,35,21), (0,8,9,11) (1,33,44,12), (0,7,10,12) (1,8,14,7),
(0,8,11,12) (1,11,32,22), (0,9,10,12) (1,40,54,15), (0,9,11,12) (1,22,54,33). By Anick's theorem (cited in L1.5), general
forms of degree d1 cannot realize the 13 non-matching points; (0,6,8,12) and (0,8,9,12) are the non-matching ones that are
not obstructed, and (0,6,8,12) is realized anyway (Table A), so a mismatch is not an obstruction.

### Table F: rays realized over U(H) (L3.2, L3.3; characteristic 0; [D] with exact CE check)

Exact statement for every row: Kostant's theorem (Sam 2015, Thm 2.1) for g = sp_4, n = the Heisenberg nilradical,
lambda = (p,q): L(p,q) has pure resolution beta = (q+1,p+2,p+2,q+1) on (0,p-q+1,p+q+3,2p+4).

| Ray | (p,q) | Table | Multiple | Dossier S status | Consequence |
|---|---|---|---|---|---|
| (0,1,3,4) | (0,0) | (1,2,2,1) | 1 | obstructed | known (Erman-Sam) |
| (0,1,5,6) | (1,1) | (2,3,3,2) | 1 | obstructed | primitive realized over U(H): new, not a counterexample |
| (0,1,7,8) | (2,2) | (3,4,4,3) | 1 | obstructed | new, not a counterexample |
| (0,1,9,10) | (3,3) | (4,5,5,4) | 1 | obstructed | new, not a counterexample |
| (0,1,11,12) | (4,4) | (5,6,6,5) | 1 | obstructed | new, not a counterexample |
| (0,3,5,8) | (2,0) | (1,4,4,1) | 1 | obstructed | new, not a counterexample |
| (0,5,7,12) | (4,0) | (1,6,6,1) | 1 | obstructed | new, not a counterexample |
| (0,3,7,10) | (3,1) | (2,5,5,2) | 1 | UNDECIDED | Question 6.1 answered yes on the whole ray |
| (0,2,4,6) | (1,0) | (1,3,3,1) | 1 | realized | redundant |
| (0,2,8,10) | (3,2) | (3,5,5,3) | 1 | realized | redundant |
| (0,4,6,10) | (3,0) | (1,5,5,1) | 1 | realized | redundant |
| (0,2,6,8) | (2,1) | (2,4,4,2) | 2 | obstructed | 2x only; primitive open over U(H); 2x already realized over S |
| (0,3,9,12) | (4,2) | (3,6,6,3) | 3 | obstructed | 3x only; primitive open over U(H) |
| (0,2,10,12) | (4,3) | (4,6,6,4) | 2 | obstructed | 2x only; primitive open over U(H) |
| (0,4,8,12) | (4,1) | (2,6,6,2) | 2 | realized | redundant |

The family covers only the 15 symmetric parity-passing rays; the other 14 parity-passing rays ((0,2,4,8), (0,4,6,8),
(0,2,4,10), (0,2,6,10), (0,4,8,10), (0,6,8,10), (0,2,4,12), (0,2,6,12), (0,2,8,12), (0,4,6,12), (0,4,10,12), (0,6,8,12),
(0,6,10,12), (0,8,10,12)) are untouched over U(H). The 191 parity-failing rays, including (0,4,9,10) and (0,1,6,10), have no
U(H) point at all.

Consequence for the dossier's smallest-counterexample question (item B): of the parity-passing S-obstructed rays with d3
<= 9, only the primitive (1,2,2,1) on (0,2,6,8) remains open over U(H). The other route to a counterexample with d3 <= 9
is an S-obstruction on one of the 42 parity-failing rays with d3 <= 9 that remain UNDECIDED after Table A (script output;
none of them passes parity).
