# tau-conjecture: reference library

Status legend: READ = read directly (pages noted); ABS = abstract-level read;
TO FETCH = named, not yet read. Unread sources cannot support conclusions.

## Core problem sources

| Ref | Status | Notes |
|---|---|---|
| M. Shub, S. Smale. On the intractability of Hilbert's Nullstellensatz and an algebraic version of "NP != P?". Duke Math. J. 81(1):47-54, 1995 (Nash volume). DOI: 10.1215/S0012-7094-95-08105-8 | TO FETCH | The origin: tau conjecture, implication to P_C != NP_C via hard factorials. Statement transcribed via Buergisser 2024 survey eq. (4.5). |
| S. Smale. Mathematical problems for the next century. Math. Intelligencer 20(2):7-15, 1998. DOI: 10.1007/BF03025291 | TO FETCH | Problem 4 on the list. |
| L. Blum, F. Cucker, M. Shub, S. Smale. Complexity and Real Computation. Springer, 1998 | TO FETCH (p. 126 factoring remark cited via Koiran 2004) | The BSS book; tau over 1 only. |
| L. Blum, M. Shub, S. Smale. On a theory of computation and complexity over the real numbers. Bull. AMS 21(1):1-46, 1989. DOI: 10.1090/S0273-0979-1989-15750-9 | TO FETCH | The BSS model. |
| P. Buergisser. Completeness classes in algebraic complexity theory. arXiv:2406.06217 (2024-06-10); to appear, "FoCM: The Work of Leslie Valiant", ACM | READ (sections 4.4-4.6, pages 24-28) | The authoritative current survey; section 4.6 = Tau Conjectures: statement (4.5), SS95 implication, Thm 4.17 (Buer09), real tau (Conj 4.1), SoS tau (Conj 4.2), Lipton, Shamir, falsity of the real analogue. |
| P. Koiran. Valiant's model and the cost of computing integers. Comput. Complexity 13(3-4):131-146, 2004. DOI: 10.1007/s00037-004-0186-2 | READ (pages 131-136; theorem statements throughout) | tau(n) from {1,2}; easy / ultimately easy; DMS96 + Moreira97 almost-all bounds; no nontrivial lower bound on tau(n!); Shamir 1979 division trick; Thm 2.5 (VP0=VNP0 iff HC in VP0); Prop 3.1; Thm 5.1. |
| P. Buergisser. On defining integers and proving arithmetic circuit lower bounds. Comput. Complexity 18(1):81-103, 2009 (ECCC TR06-113; STACS 2007). DOI: 10.1007/s00037-009-0260-x | ABS (TR06-113 abstract) | Permanent in poly size => tau(n!) polylog; same for Pochhammer-Wilkinson prod (X-k) and Taylor(exp/log) with divisions; counting-hierarchy technique. |
| K. Markstroem. The straight line complexity of small factorials and primorials. INTEGERS 14 (2014), arXiv:1306.3091v4 | READ (full, 10 pages) | The experimental prior art: exhaustive census to length 9 + targeted DFS to 11; exact tau'(n!) n<=28, tau(n!) n<=19, primorials; normalization + range-isomorphism dedup + squaring-reach pruning; open problem: monotonicity of tau(n!). |

## Partial results and adjacent conjectures

| Ref | Status | Notes |
|---|---|---|
| J. M. Rojas. A direct ultrametric approach to additive complexity and the Shub-Smale tau conjecture. arXiv:math/0304100 (2003) | READ (full, 10 pages, 2026-08-01) | p-adic Digit Conjecture => full tau conjecture (Thm 1); valuation spectrum s <= N_p(s) <= s(s+1)/2, p-independent (Thm 2, Newton-polygon proof); <= 1 + s^3(s+1)(7.5)^s s! rational roots at additive complexity s (Thm 3); roots-near-1 bound (Thm 4); logistic real factory Example 1; open: p-adic factory analogue; Borodin-Cook 1976 / Grigoriev 1982 / Risler 1985 real-root ladder quoted. |
| P. Koiran. Shallow circuits with high-powered inputs. ICS 2011, arXiv:1004.4960 | ABS | The real tau conjecture; PIT connection. |
| S. Tavenas. Bornes inferieures et superieures dans les circuits arithmetiques (and the 2014 paper cited as [Tav14] in the survey) | TO FETCH | Real tau => VP != VNP; m,t,2^k version suffices. |
| P. Koiran, N. Portier, S. Tavenas. A Wronskian approach to the real tau-conjecture. J. Symbolic Comput. 68:195-214, 2015 (arXiv:1205.1015). DOI: 10.1016/j.jsc.2014.09.036 | ABS (identified precisely 2026-08-02; this is the survey's [KPT15]) | Wronskian-determinant upper bounds on real roots of sums of products of sparse polynomials; polynomial bounds in special cases (few distinct sparse factors, repeated); implies-permanent framing. Full bound formulas: read PDF at use time. |
| P. Koiran, N. Portier, S. Tavenas, S. Thomasse. A tau-conjecture for Newton polygons. Found. Comput. Math. / arXiv:1308.2286 | ABS | Newton-polygon variant; weak version already implies permanent lower bounds. |
| P. Hrubes. On the real tau-conjecture and the distribution of complex roots. Theory of Computing 9(10):403-411, 2013. DOI: 10.4086/toc.2013.v009a010 | ABS | Complex-root-clustering equivalences. |
| I. Briquel, P. Buergisser. The real tau-conjecture is true on average. Random Struct. Algorithms 57(2):279-303, 2020, arXiv:1806.00417. DOI: 10.1002/rsa.20926 | ABS | Average-case truth for Gaussian coefficients. |
| P. Dutta. Real tau-conjecture for sum-of-squares (with N. Saxena, T. Thierauf), CSR 2021. DOI: 10.1007/978-3-030-79416-3_5 | TO FETCH | SoS tau conjecture; rigid matrices; sum-of-cubes => PIT in P. |
| Y. Alekseev, D. Grigoriev, E. Hirsch, I. Tzameret. Semi-algebraic proofs, IPS lower bounds and the tau-conjecture. ECCC TR19-142 (STOC 2020) | TO FETCH | Proof-complexity bridge. |
| S. Bhattacharjee, M. Blaeser, P. Dutta, S. Mukherjee. Exponential lower bound via exponential sums. arXiv:2601.00387 (2026-01); ICALP 2024 predecessor: DOI 10.4230/LIPIcs.ICALP.2024.24 | ABS | Tau conjecture => explicit exponential lower bound for an exponential sum. |
| P. Buergisser. Intractability of Hilbert's Nullstellensatz implies algebraic hardness of permanent. arXiv:2606.25121 (2026-06-23) | ABS | Nonuniform P_C != NP_C => uniform constant-free Valiant separation. |
| Q. Cheng. On the ultimate complexity of factorials. Theoret. Comput. Sci. 326(1-3):419-429, 2004. DOI: 10.1016/j.tcs.2004.07.032 | TO FETCH | Conditional upper bound exp(c sqrt(log n loglog n)) on tau'(n!). |
| Q. Cheng. Straight-line programs and torsion points on elliptic curves. Comput. Complexity 12(3-4):150-161, 2003. DOI: 10.1007/s00037-003-0180-0 | TO FETCH | Nontrivial upper bound for multiples of n!. |
| V. Strassen. Einige Resultate ueber Berechnungskomplexitaet. Jber. Deutsch. Math.-Verein. 78(1):1-8, 1976/77 | TO FETCH | O(sqrt(n) log^2 n) for multiples of n! (as quoted by Markstroem). |
| C. G. Moreira. On asymptotic estimates for arithmetic cost functions. Proc. AMS 125(2):347-353, 1997. DOI: 10.1090/S0002-9939-97-03583-X | TO FETCH | tau(n) >= log n / loglog n almost all n. |
| W. de Melo, B. F. Svaiter. The cost of computing integers. Proc. AMS 124(5):1377-1378, 1996. DOI: 10.1090/S0002-9939-96-03173-5 | TO FETCH | Almost-all lower bound; the {1,2} base convention. |
| A. Shamir. Factoring numbers in O(log n) arithmetic steps. Inform. Process. Lett. 8(1):28-31, 1979. DOI: 10.1016/0020-0190(79)90087-5 | TO FETCH | With integer division, n! is easy; why {+,-,x} only is essential. |
| R. Lipton. Straight-line complexity and integer factorization. ANTS 1994, LNCS 877. DOI: 10.1007/3-540-58691-1_50 | TO FETCH | Average-case factoring => weak tau statements; many rational roots. |
| A. Lempel, G. Seroussi, J. Ziv. On the power of straight-line computations in finite fields. IEEE Trans. Inform. Theory 28(6):875-880, 1982. DOI: 10.1109/TIT.1982.1056579 | TO FETCH | Finite-field analogue bounds. |

## Adjacent computational surfaces

| Ref | Status | Notes |
|---|---|---|
| E. Allender, P. Buergisser, J. Kjeldgaard-Pedersen, P. B. Miltersen. On the complexity of numerical analysis. SIAM J. Comput. 38(5):1987-2006, 2009. DOI: 10.1137/070697926 | TO FETCH | PosSLP; the decision cousin of tau. |
| On the hardness of PosSLP. arXiv:2307.08008 | TO FETCH | Recent PosSLP hardness. |
| PosSLP and sum of squares. arXiv:2403.00115 | TO FETCH | Recent PosSLP work. |
| OEIS A005245 (integer complexity, +,x from 1s) | TO FETCH | The classical adjacent census; different model (no subtraction, counts 1s not ops). |
| G. Malajovich. Ultimate polynomial time. arXiv:math/9904130 (1999); Proc. LMS | ABS | The class UP over C; tau conjecture implies UP does not contain constant-free NP_C. Adjacent formulation. |
| K. Phillipson, J. M. Rojas. Fewnomial systems with many roots, and an adelic tau conjecture. arXiv:1011.4128 (2010, rev. 2012) | ABS | Adelic/local-field tau variant; explicit fewnomial systems near upper bounds via tropical intersections. Natural home for a p-adic census extension (RL-2). |
| C. Fuhs, P. Schneider-Kamp. Synthesizing shortest linear straight-line programs over GF(2) using SAT. SAT 2010, LNCS 6175. DOI: 10.1007/978-3-642-14186-7_8 | ABS | SAT reduction for optimal-length SLP decisions (linear case; MaxSNP-complete optimization). Template for the RL-7 integer encoding. |
| J. R. Doyle, B. Poonen. Gonality of dynatomic curves and strong uniform boundedness of preperiodic points. arXiv:1711.04233 | ABS READ 2026-08-20 (TCB-024) | Fix d >= 2, char k does not divide d, k contains the d-th roots of 1: the dynatomic curves for z^d + c are geometrically irreducible with gonality tending to infinity. Consequences: the FUNCTION-FIELD analogue of strong uniform boundedness for preperiodic points of z^d + c; over NUMBER FIELDS, strong uniform boundedness for preperiodic points of bounded eventual PERIOD, which reduces the full preperiodic conjecture to the periodic case. Import verdict for our V8 line: the number-field statement is conditional on bounded eventual period, so it does NOT yield an unconditional uniform constant for our parameterized-tower question over Z; our stall theorems stay self-contained (elementary escape + finite preimage core), and the dynamics literature is context, not a premise. |
| P. Morton, J. Silverman. Rational periodic points of rational functions. IMRN 1994 (uniform boundedness conjecture) | TO FETCH | The uniform-boundedness frame for RL-9. |
| M. Shub, S. Smale 1995 Duke original: access attempt 2026-08-01 FAILED (Project Euclid paywall; author page TLS misconfigured). Statement remains triply confirmed (Rojas Def 1 + survey 4.5 + Koiran); direct read still queued. | TO FETCH | |
