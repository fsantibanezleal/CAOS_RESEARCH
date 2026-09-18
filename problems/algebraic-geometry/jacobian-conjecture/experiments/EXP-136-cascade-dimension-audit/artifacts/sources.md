# EXP-136 - Located statements (primary texts fetched 2026-09-18)

Each entry gives the source, the arXiv version read, the SHA-256 of the fetched PDF, and the
load-bearing statements transcribed verbatim (ASCII transliteration of the notation). Only these
statements enter `run.py` and the verdict.

## Dixmier: A. Belov-Kanel, M. Kontsevich, "The Jacobian Conjecture is stably equivalent to the Dixmier Conjecture"

arXiv:math/0512171v2 (16 Dec 2005); Mosc. Math. J. 7 (2007). PDF SHA-256
`399075cefd34b1081b996f2906ccd9b3aae647523985f0ae763f9b2acd86c642`.

- Introduction: "Obviously, JC_n implies JC_m if n > m. ... The conjecture JC_n is obviously true
  in the case n = 1, and it is open for n >= 2."
- Introduction: "The conjecture DC_n implies DC_m for n > m, and we can consider the stable
  Dixmier conjecture DC_infinity. The conjecture DC_n is open for any n >= 1."
- Introduction: "It is well-known that DC_n implies JC_n (in particular DC_infinity implies
  JC_infinity) (see [5], [3]). The argument is very easy. Let phi be a counterexample to JC_n.
  ... it induces a pullback homomorphism of the algebra of differential operators ... we obtain
  a counterexample to DC_n."
- "Our result is an opposite implication. Namely, we prove the following. Theorem 1. Conjecture
  JC_2n implies DC_n. In particular, we obtain that the stable conjectures JC_infinity and
  DC_infinity are equivalent."
- Abstract: "... the main result was already published by [Y. Tsuchimoto] in Osaka Journal of
  Mathematics Volume 42, Number 2 (June 2005). His proof is different."

## Poisson: K. Adjamagbo, A. van den Essen, "On the equivalence of the Jacobian, Dixmier and Poisson Conjectures in any characteristic"

arXiv:math/0608009v1 (1 Aug 2006); Acta Math. Vietnam. 32 (2007), 209-218. PDF SHA-256
`1f8c7b6c56c23530d9f1120a075fb4ee2f214c0c948eab0362d921bb5cd0bbda`.

- Abstract: the Poisson conjecture concerns "any endomorphism of the n-th canonical Poisson
  algebra over a field of characteristic p, i.e. the algebra of polynomial in 2n indeterminates
  over this field endowed with its classical Poisson bracket".
- Introduction: "It is well known since the publication of [10] in 1982 that Dixmier Conjecture
  of index n in characteristic zero implies the Jacobian one in dimension n."
- Theorem 7 (the United Conjectures Theorem): "1. For (n, d, p) ... with p = 0 or prime, we have
  the following chain of implications: CJC(2n, p, d) => CPC(n, p, d) => CDC(n, p, d) =>
  CJC(n, p, d). 2. It follows that ... CJC(2n, p) => CPC(n, p) => CDC(n, p) => CJC(n, p).
  3. Finally ... CJC(p) <=> CPC(p) <=> CDC(p)." (p = 0 is characteristic zero.)

## Gaussian moments: H. Derksen, A. van den Essen, W. Zhao, "The Gaussian Moments Conjecture and the Jacobian Conjecture"

arXiv:1506.05192v1 (17 Jun 2015); Israel J. Math. 219 (2017). PDF SHA-256
`1226da233f8055b7f5572ff456cd8878767add32ed52c3b87632b8853765eafc`.

- Theorem 1.6: "If GMC(n) is true for all n >= 1, then JC(n) is true for all n >= 1."
- Proposition 4.2 (end of statement): "In particular, GMC(n) is true for n = 1."
- Theorem 2.4 (Mathieu): "If MC(SL_n(C)/GL_{n-1}(C)) is true for all n >= 1, then JC(n) is true
  for all n >= 1."

## Gaussian moments: C. D. Long, "Small Counterexamples to the Gaussian Moments Conjecture"

arXiv:2607.18186v1 (20 Jul 2026). PDF SHA-256
`ca5d36529019375cede8dc6a7765430681751c4e587dc2122f37f21f05cdc42c`.

- Abstract: "We give explicit complex polynomials P, Q in three independent standard real
  Gaussian variables such that E(P^m) = 0, E(QP^m) = m! != 0 for every m >= 1. ... Hence the
  Gaussian Moments Conjecture is false in every dimension n >= 3."
- Abstract: "Although the main theorem of Derksen, van den Essen, and Zhao is stated globally in
  dimension, its proof has fixed-dimensional content: a noninvertible cubic-homogeneous Keller
  map in r variables forces the failure of GMC(2r)."
- After Theorem 5.1: "Proof. Theorem 5.1 disproves GMC(3). For n > 3, use the same polynomials
  in the first three variables and ignore the remaining independent Gaussian variables.
  Derksen, van den Essen, and Zhao proved GMC(1) [4, Proposition 4.2]. The only remaining
  dimension is therefore n = 2."

## Mathieu: K. Zwart, "Mathieu's approach to the Jacobian Conjecture" (expository)

arXiv:2511.16561v2 (21 Nov 2025). PDF SHA-256
`ccd62d8d63c97394cb1dc005e22ac49403886edc1bff912aebd89eadfa2225c7`.

- Theorem 2.2: "Let N in N and let K = SU(N). Assume the Mathieu Conjecture for SU(N). Then the
  Jacobian Conjecture on C^N is true."
- Conjecture 4.3 ([BCW82, Introduction]): "Let n in N, and f : C^n -> C^n be a polynomial map
  with Jacobian J(f) = 1. Assume that f_i = x_i - h_i where h_i : C^n -> C is a homogeneous
  polynomial of degree d, where d in N. Then f is invertible with polynomial inverse."
- Theorem 4.4 ([BCW82, Thm. II.2.1 and Cor. II.2.2]): "Conjecture 4.3 with d = 3 implies the
  Jacobian Conjecture." (Conjecture 4.3 quantifies over every n.)
- Theorem 4.16 ([Mat97, Thm. 5.3 + 5.4]): "Assume Conjecture 4.15. Then Conjecture 4.3 is true
  for all d in N. In particular, Conjecture 4.5 is true (which implies the Jacobian
  Conjecture)." Its proof begins: "Let f = (f_1, ..., f_n) : C^n -> C^n be a polynomial map
  with Jacobian J(f) = 1, and let f_j = x_j - h_j where h_j is a homogeneous polynomial of
  degree d", and works with Q := sum_i h_i (x) d_i in S^d C^n (x) (C^n)^*, an SL(n, C)-module.
- Theorem 4.23: "Let K = SU(N), G = SL(N, C) ... Assume the Mathieu Conjecture to be true for
  K. Then Conjecture 4.15 is true."
- Corollary 4.24: "Let N in N and consider K = SU(N). Assume the Mathieu Conjecture is true for
  SU(N). Then the Jacobian Conjecture for C^N is true. Proof. Combine Theorem 4.23 and
  Theorem 4.16."

Reading used here: Theorems 4.23 and 4.16 give, for each N, the Mathieu conjecture for SU(N)
implies Conjecture 4.3 on C^N (maps x - h, h homogeneous, every degree d). The passage to a
general Keller map runs through Theorem 4.4, which is a statement over all dimensions (the
Bass-Connell-Wright reduction adds variables). The fixed-dimensional form for general maps
stated in Theorem 2.2 and Corollary 4.24 therefore rests on a step the exposition does not
supply.

## Mathieu: the same implication as stated by other authors (all stable in dimension)

- A. van den Essen, "An introduction to Mathieu subspaces", arXiv:1907.06107v1 (PDF SHA-256
  `d9ad5dbfc1b9e7e41802aebe7beab5710205ae51846ae2ca4ef8b8de81da65d4`), Section 1: "He stated
  the following conjecture and showed that his conjecture implies the Jacobian Conjecture".
- A. van den Essen, D. Wright, W. Zhao, "On the Image Conjecture", arXiv:1008.3962v2 (PDF
  SHA-256 `8c295ebccdd0922620a05b7f7e1dde8d8bffa08b53b83733330abf23fa3a484d`), Introduction: "a
  conjecture of Olivier Mathieu ([3]), which was shown by Mathieu to imply the famed Jacobian
  Conjecture".
- T. Dings, E. Koelink, "On the Mathieu conjecture for SU(2)", arXiv:1404.4215v1 (PDF SHA-256
  `a95976f8480da4941a697129ae33f1f891a63532b851d36d17fef1116a278bd1`), Introduction: "it
  actually implies the Jacobian conjecture, see [6]".
- W. Zhao, "Generalizations of the Image Conjecture and the Mathieu Conjecture",
  arXiv:0902.0212v3 (PDF SHA-256
  `e5b3f759c060c03692d8f9daa342608f84e488b8a465b530bff9ff49867bc500`): "Mathieu also showed in
  [Ma] that his conjecture implies the Jacobian conjecture."
- M. Mueger, L. Tuset, "The Mathieu conjecture for SU(2) reduced to an abelian conjecture",
  arXiv:2210.06582v2 (PDF SHA-256
  `01c9cd57b22cf2fcd93bd5c94c895c1c28d335572f05643491ecb9ac0c4fadbc`), Introduction: "He then
  proved that this conjecture implies O.-H. Keller's notorious Jacobian conjecture."
- Derksen, van den Essen, Zhao, Theorem 2.4 above (stated for all n).

The fixed-dimensional form "Mathieu for SU(N) implies JC(N)" appears in Zwart's Theorem 2.2
and in Z. Zhang, "Direct Consequences of the Three-Dimensional Counterexample to the Jacobian
Conjecture" (web note, 2026-07-20, zzhang-iu.github.io/papers/direct-consequences-jacobian/,
Section 2), which cites Zwart's Theorem 2.2 for it.

Not located: O. Mathieu, "Some conjectures about invariant theory and their applications",
Algebre non commutative, groupes quantiques et invariants, Seminaires et Congres 2, SMF (1997),
263-279 (no open copy found on the SMF or EMIS sites or by search, 2026-09-18).

## Found by the bounded search pass (amendment; all preprints)

- C. D. Long, "Counterexamples to the xz-Conjecture and the Mathieu Conjecture for SU(2)",
  arXiv:2607.19012v1 (21 Jul 2026). PDF SHA-256
  `cb75f1acf144a2deb67e7c4ecd92f00d8c73ea5e92dd5e52ae303553941049e6`.
  - Theorem 4.2: "Let lambda, mu in C^x and define regular functions on SU(2) by
    F_{lambda,mu} = lambda (1 + mu c)(ad + mu^-1 b), G = -c. Then, for every integer n >= 1,
    int_SU(2) F_{lambda,mu}(g)^n dg = 0, int_SU(2) F_{lambda,mu}(g)^n G(g) dg =
    (-1)^(n-1) lambda^n mu^-1 / (n+1) != 0. In particular, the Mathieu conjecture for SU(2) is
    false." Part D checks lambda = mu = 1 for n = 1..12.
  - Introduction: "Mathieu proved that his conjecture for all compact connected Lie groups
    implies Keller's Jacobian Conjecture [6, 5]. ... It follows that Mathieu's conjecture cannot
    hold for all compact connected Lie groups. This argument does not determine whether the
    conjecture holds for SU(2)".
  - Remark 4.3: "Mathieu's implication from his compact-group conjecture to the Jacobian
    Conjecture is one-way. Consequently, Theorem 4.2 does not by itself imply that the
    two-dimensional Jacobian Conjecture is false."
- C. D. Long, arXiv:2607.18186v1, Section 5, eq. (10): "P3 = (1 + Z)(W - (1/2)(2 + Z)T^2) =
  W + WZ - T^2 - (3/2)ZT^2 - (1/2)Z^2T^2, Q3 = Z", with Z = (X1 + iX2)/sqrt 2,
  W = (X1 - iX2)/sqrt 2; Theorem 5.1: "E(P3^m) = 0, E(Q3 P3^m) = m! != 0 (m >= 1)". Part E
  checks m = 1..10.
- M. Wilson, "A face-isolation proof of the two-variable Gaussian Moments Conjecture",
  arXiv:2607.23887v1 (26 Jul 2026). PDF SHA-256
  `0f70a4a1a5cceca0ea2d9bba2aa6d1c120da4980cddf4c105a55db97f85f257a`. Abstract: "This proves
  the two-variable Gaussian Moments Conjecture with the explicit threshold m >= deg Q + 1. ...
  Combined with the known one-variable case and counterexamples in dimensions (n >= 3), this
  determines the dimensions in which the Gaussian Moments Conjecture holds." Not verified here.
- A. Zheglov, "The Conjecture of Dixmier for the first Weyl algebra is true",
  arXiv:2410.06959v5 (19 Jan 2026; first version 9 Oct 2024; 78 pages). PDF SHA-256
  `897913ef95e011332e86e348803c6c9da5dbd196db17a04f8f951110e9b095e3`. Abstract: "In this
  paper we prove that the Dixmier conjecture for the first Weyl algebra is true, i.e. each
  algebra endomorphism of the algebra A_1 is an automorphism." Not verified here.
- Consistency check (secondary): the Wikipedia article "Jacobian conjecture" (read 2026-09-18)
  states that DC_n and PC_n are false for every n > 2 "while both conjectures remain open for
  n = 1, 2", in agreement with Part A. T. Tao's post "A digestion of the Jacobian conjecture
  counterexample" (2026-07-21) does not discuss the cascade.
