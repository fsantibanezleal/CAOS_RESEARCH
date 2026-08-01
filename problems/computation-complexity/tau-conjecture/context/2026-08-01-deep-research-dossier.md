# Shub-Smale tau conjecture (Smale problem 4): opening deep-research dossier

Dated 2026-08-01. First full primary-source pass for opening the problem
(portfolio slug `tau-conjecture`, area `computation-complexity`; scoped
2026-07-20 in the portfolio scoping dossier).

Claim tags: [V] = read directly in a primary source (named at the claim);
[MV] = stated in a reliable secondary source (typically the Buergisser 2024
survey) whose original we have not yet read; [D] = derived by us; [C] =
conjectured by us; [U]/[TO FETCH] = unverified, cannot support conclusions.

Sources read IN FULL for this dossier: Markstroem (arXiv:1306.3091v4, all 10
pages); Koiran 2004 (DOI 10.1007/s00037-004-0186-2, pages 131-136 read, rest
skimmed via statements); Buergisser 2024 survey section 4.4-4.6 (arXiv:
2406.06217, pages 24-28). Abstract-level reads: Rojas math/0304100; Hrubes
ToC 2013; KPTT arXiv:1308.2286; Buergisser TR06-113; Bhattacharjee-Blaeser-
Dutta-Mukherjee arXiv:2601.00387; Buergisser arXiv:2606.25121.

## 1. The statement

### 1.1 The model [V]

A constant-free arithmetic circuit (equivalently, a straight-line program)
over $\mathbb{Z}[x]$ uses gates $+,-,\times$ of fan-in 2; the only freely
available constants are $-1, 0, 1$; input gates carry $x$ or those constants.
The tau-complexity $\tau(f)$ of $f \in \mathbb{Z}[x]$ is the minimal number
of operation gates of such a circuit computing $f$.
[V: Buergisser 2024 survey, section 4.6, arXiv:2406.06217; consistent with
Koiran 2004, section 2.2, which calls these circuits constant-free.]

For an integer $n$, $\tau(n)$ is the minimum number of $+,-,\times$
operations building $n$: De Melo-Svaiter start from the constants 1 AND 2,
Blum-Cucker-Shub-Smale start from 1 alone; the two measures differ by at most
1. [V: Koiran 2004, section 2.1.] Dropping $-$ and $\times$ recovers classical
addition chains (Scholz 1937). [V: Koiran 2004, section 2.1.]

### 1.2 The conjecture [V]

Let $z(f)$ be the number of DISTINCT INTEGER roots of a nonzero
$f \in \mathbb{Z}[x]$. The Shub-Smale tau conjecture:

$$z(f) \le (1 + \tau(f))^c$$

for a universal constant $c > 0$.
[V: Buergisser 2024 survey, eq. (4.5); original: M. Shub and S. Smale, "On
the intractability of Hilbert's Nullstellensatz and an algebraic version of
'NP != P?'", Duke Math. J. 81(1):47-54, 1995 (Nash volume). TO FETCH: the
Duke original; we cite its statement through the survey. Compare also
Strassen 1990, Problem 9.2 [MV: survey].]

This is Smale's 4th problem on his 1998 list of mathematical problems for the
next century. [MV: universally so numbered, e.g. the FoCM 2014 Shub slides;
Smale's list itself TO FETCH.]

### 1.3 Trivial and general bounds

- $z(f) \le \deg f \le 2^{\tau(f)}$ (degree at most doubles per gate). [D:
  immediate induction; also stated in the literature.]
- For integers: $\log_2 \log_2 n + 1 \le \tau(n) \le 2 \log_2 n$ for all
  $n \ge 3$; the lower bound is attained by $n = 2^{2^k}$ (repeated
  squaring), the upper by binary expansion. [V: Markstroem eq. (1); Koiran
  2004, section 2.1.]
- Almost all integers are hard: for every $\epsilon > 0$, for almost all $n$,
  $\tau(n) \ge (\log n)/(\log\log n)^{1+\epsilon}$ (De Melo-Svaiter 1996,
  Proc. AMS 124(5):1377-1378), improved to
  $\tau(n) \ge (\log n)/\log\log n$ for almost all $n$ (Moreira 1997, Proc.
  AMS 125(2):347-353). [V: both stated with attribution in Koiran 2004,
  introduction; originals TO FETCH.]
- NO nontrivial lower bound on $\tau(n!)$ is known (state of the art as of
  Koiran 2004: "We are not aware of any nontrivial lower bound on
  $\tau(n!)$"). [V: Koiran 2004, section 2.1.]

## 2. Why the conjecture matters: the verified implication ladder

1. **Tau conjecture implies $P_{\mathbb{C}} \ne NP_{\mathbb{C}}$** in the
   Blum-Shub-Smale model over $\mathbb{C}$ (Shub-Smale 1995). The proof
   reduces to: it suffices that for every sequence of nonzero integers
   $m_n$, the sequence $(m_n \cdot n!)$ is hard to compute, where a sequence
   $(a(n))$ is HARD iff $\tau(a(n))$ is not polynomially bounded in
   $\log n$. This is the "factorials are ultimately hard" route. [V:
   Buergisser 2024 survey, section 4.6; Koiran 2004, introduction states the
   same implication citing Shub-Smale 1996 and BCSS 1998.]
2. **Tau conjecture implies $VP^0 \ne VNP^0$** (constant-free Valiant
   classes), and $VP^0 \ne VNP^0$ already follows if the single sequence
   $(n!)$ is hard to compute (Buergisser 2009, building on Koiran 2004; the
   key tool is the counting hierarchy of Wagner 1986). [V: survey, Theorem
   4.17. TR06-113 abstract [V]: poly-size arithmetic circuits for the
   permanent imply $\tau(n!)$ polynomially bounded in $\log n$; same for the
   Pochhammer-Wilkinson polynomials $\prod_{k=1}^{n}(X-k)$ and Taylor
   approximations of exp and log, allowing divisions.]
3. **Koiran 2004 theorems** (read directly): if $VP^0 = VNP^0$ then
   $\tau(\lfloor 2^{2^n} \ln 2 \rfloor)$ is polynomially bounded (Thm 3.5
   route via Prop 3.1: any sequence with #P/poly-definable "digits" in a
   base-$b$ expansion is cheap under $VP^0 = VNP^0$); $VP^0 = VNP^0$ iff the
   Hamilton-cycle family $HC_n \in VP^0$ (Thm 2.5; HC is used instead of the
   permanent because the permanent's completeness proof divides by 2); if
   $VP^0 = VNP^0$ AND $P = PSPACE$ then $n!$ is ultimately easy to compute
   (Thm 5.1). Contrapositives: proving $n!$ hard yields a permanent lower
   bound or $P \ne PSPACE$-type separations. [V: Koiran 2004.]
4. **Factoring connection.** If $n!$ (or suitable multiples) were easy to
   compute, integer factoring would be in (nonuniform) polynomial time
   (Strassen's observation; BCSS 1998, p. 126; Cheng 2003). With division
   (quotient and remainder) allowed, $n!$ IS easy (Shamir 1979); so the
   $+,-,\times$ restriction is essential. Lipton 1994: if factoring is hard
   on average, a weaker version of the tau conjecture follows; he also
   connects factoring to polynomials with many rational roots. [V: Koiran
   2004, section 2.1; survey section 4.6. Originals (Shamir 1979, Lipton
   1994, Cheng 2003) TO FETCH.]
5. **2026 state.** Buergisser (arXiv:2606.25121, June 2026): nonuniform
   $P_{\mathbb{C}} \ne NP_{\mathbb{C}}$ implies a constant-free uniform
   Valiant separation; strengthens the bridge the tau conjecture feeds. [V:
   abstract.] Bhattacharjee-Blaeser-Dutta-Mukherjee (arXiv:2601.00387, Jan
   2026, extending their ICALP 2024 work): the tau conjecture implies an
   EXPONENTIAL lower bound for an explicit exponential sum, "the first time
   the Shub-Smale tau-conjecture has been applied to prove explicit
   exponential lower bounds". [V: abstract.] No claimed proof or refutation
   of the conjecture found in the 2024-2026 sweep (searched arXiv, ECCC tag
   "tau-conjecture": only TR06-113 and TR19-142 carry the tag).

## 3. Partial results toward (and around) the conjecture

- **The real analogue is FALSE**: replacing "integer zeros" by "real zeros"
  kills the statement (polynomials computed by short circuits can have
  exponentially many real roots; the classical witnesses are Chebyshev-type
  polynomials). [V: survey, section 4.6 states the falsity; the Chebyshev
  witness attribution is [MV], to be pinned when the wiki page is written.]
- **Additive complexity and ultrametric bounds** (Rojas 2003,
  math/0304100): a nonzero univariate polynomial with ADDITIVE complexity
  $s$ has $e^{O(s \log s)}$ roots in $\mathbb{Q}_2$ (2-adic rationals),
  hence at most that many rational roots; two weak versions of the tau
  conjecture are proved, and the full conjecture is reduced to a stronger
  plausible hypothesis. [V: abstract only; the theorems and their exact
  constants TO FETCH before any use as a premise.]
- **Average-case**: the real tau conjecture holds on average for Gaussian
  coefficients (Briquel-Buergisser 2020, arXiv:1806.00417). [MV: survey +
  arXiv listing; original TO FETCH.]
- **Best known integer-root records vs tau**: we did NOT find, in this
  pass, any published family with $z(f)$ superpolynomial in $\tau(f)$ (that
  would refute the conjecture), nor a published exact census of the maximum
  $z$ achievable at each small $\tau$. Cheap linear-rate families exist,
  e.g. $\prod_{i=1}^{k}(x - 2^i)$ gives $z = k$ with $\tau = O(k)$ [D:
  explicit 3-ops-per-root construction]. Whether a superlinear record is
  known in print is OPEN IN OUR RECORD [U]; the small-tau census is the
  target of EXP-001.

## 4. The adjacent conjecture family (reformulation lens targets)

- **Real tau conjecture** (Koiran 2011, "Shallow circuits with high-powered
  inputs", arXiv:1004.4960): for $F = \sum_{i=1}^{m} \prod_{j=1}^{k} f_{ij}$
  with each $f_{ij}$ $t$-sparse, the number of REAL zeros of $F \ne 0$ is
  polynomially bounded in $m, k, t$. Implies $VP^0 \ne VNP^0$; in fact
  $VP \ne VNP$ (Tavenas 2014); a bound polynomial in $m, t, 2^k$ already
  suffices for the conclusion. Best known real-root bounds for such sums:
  Koiran-Portier-Tavenas 2015 and references. [V: survey, Conjecture 4.1 and
  following paragraph; KPT15 TO FETCH.]
- **Newton-polygon tau conjecture** (Koiran-Portier-Tavenas-Thomasse 2015,
  arXiv:1308.2286): for bivariate $P$ written as a sum of products of sparse
  polynomials, the number of EDGES of the Newton polygon of $P$ is
  polynomially bounded in the expression size; even a weak version implies
  the permanent has no poly-size arithmetic circuits. [V: abstract.]
- **SOS tau conjecture** (Dutta 2021, with Saxena-Thierauf): for
  $F = \sum_i c_i f_i^2$ with support-sum size $SoS_{\mathbb{R}}(F)$, the
  number of real zeros is $O(SoS_{\mathbb{R}}(F))$; implies $VP \ne VNP$
  over $\mathbb{C}$ AND explicit rigid matrices; a sum-of-cubes variant
  implies deterministic poly-time PIT. [V: survey, Conjecture 4.2 and
  discussion; original TO FETCH.]
- **Complex-root distribution equivalences** (Hrubes 2013, Theory of
  Computing v9 a10): statements about clustering of complex roots equivalent
  to (or implying) the real tau conjecture. [V: abstract; theorems TO
  FETCH.]
- **Proof complexity** (Alekseev-Grigoriev-Hirsch-Tzameret, ECCC TR19-142,
  2019): a tau-conjecture-flavored statement tied to Ideal Proof System
  lower bounds ("can a natural number be negative?"). [V: ECCC listing; TO
  FETCH.]
- **PosSLP adjacency**: deciding positivity of SLP-computed integers
  (Allender et al.; recent hardness work arXiv:2307.08008, arXiv:2403.00115)
  is the decision-side cousin of the tau measure. [U/TO FETCH; flagged as a
  lens-7 dictionary target, not a premise.]

## 5. Experimental prior art (the ground our program stands on)

**Markstroem 2014** (arXiv:1306.3091v4, published in INTEGERS 14 (2014);
read in full):

- Model: integer SLPs, $x_1 = 1$, each $x_k = x_i \circ x_j$ with
  $i \le j < k$, $\circ \in \{+,-,\times\}$; $\tau(y)$ = shortest length;
  ULTIMATE complexity $\tau'(x) = \min \{\tau(y) : x \mid y\}$.
- Method: two-stage exhaustive search. Stage 1: enumerate NORMALIZED
  programs (no repeated values, all values positive; both WLOG for optimal
  programs) up to length $k = 9$, deduplicated by RANGE-ISOMORPHISM (two
  programs equivalent if computed value-sequences are permutations of each
  other); 652,227 classes at $k = 9$; every integer with $\tau \le 9$
  thereby decided. Stage 2: per-target depth-first extension to length
  $K = 11$ complete (larger for big targets), with pruning: stop if
  current maximum value $x$ satisfies $x^{2^{(K-k)}} < N$ (cannot reach the
  target by repeated squaring in the remaining steps).
- Results: exact $\tau'(n!)$ for $n \le 28$ (e.g. $\tau'(20!) = \dots =
  \tau'(22!) = 12$, $\tau'(23!) = \dots = \tau'(28!) = 14$), bounds up to
  $n = 46$ ($f = 17$, lower bound 14); exact $\tau(n!)$ for $n \le 19$
  ($\tau(19!) = 13$; $n = 20$: $f = 14$, lower bound 13); primorials
  likewise. Optimal-program witnesses are printed in full (Figures 2-5).
- Statistics at $k = 9$: 652,227 reached values; all of $[1, 10266]$
  reached; all of $[1, 26686]$ covered (divisor-reached).
- Open problem 2.1: is $\tau(n!)$ monotone in $n$?
- Upper-bound landscape quoted there: Strassen 1976/77 gives
  $\tau(\text{multiple of } n!) = O(\sqrt{n} \log^2 n)$; Cheng 2004,
  conditional on a smooth-numbers conjecture, $O(\exp(c \sqrt{\log n \log\log n}))$
  for the ultimate complexity. [V: Markstroem pages 2-3; Strassen and Cheng
  originals TO FETCH.]
- Compute: HPC2N cluster resources, 2013-2014 era; search complete only to
  length 11.

**Gap we can occupy** [D]: (a) Markstroem's census is 12 years old and
CPU-bound; a modern exact re-derivation with better canonicalization,
checkpointing, and (for the DFS stage) GPU or massive-thread extension can
push the exhaustive frontier past length 11-12 and extend the $\tau'(n!)$
table; (b) nobody, as far as this pass found, has published the POLYNOMIAL
side census: the exact maximum number of distinct integer roots
$z_{\max}(\tau)$ achievable by a constant-free SLP of length $\tau$ over
inputs $\{1, x\}$, for small $\tau$. That census is the direct experimental
image of the conjecture's growth function, exactly analogous to what we did
for fiber degrees in the Jacobian program. It is decision-bearing for
structure (which mechanisms produce many integer roots cheaply) even though
no finite census can decide the conjecture itself.

## 6. Falsifiable subquestions for the program

1. Exact $z_{\max}(\tau)$ for $\tau \le T$ (T as far as canonicalized
   exhaustion reaches): growth data + the extremal witnesses. (EXP-001
   starts this.)
2. Exact extension of Markstroem's integer table: $\tau$ and $\tau'$ of
   $n!$, $p\#$ beyond length 11; monotonicity probe for his Problem 2.1.
3. The mechanism question (anatomy lens): what structural families realize
   the record $z$ at each $\tau$ (shifted-power products? nested composition?)
   and do they stall at linear rate in $\tau$?
4. The 2-adic ceiling (invariant lens, after reading Rojas in full): compute
   additive complexity alongside $\tau$ in the census; check his
   $e^{O(s \log s)}$ 2-adic bound against measured records.
5. Dictionary probes (reformulation lens): the real-tau sparse-products
   world has quantitative bounds (KPT15); measure the integer-root analogue
   of sum-of-products-of-sparse families empirically.

## 7. Honesty notes and non-claims

- No finite computation decides the tau conjecture in either direction; the
  program's products are exact censuses, extremal witnesses, mechanism
  understanding, reproductions, and (only if a construction emerged) a
  refutation certificate. A proof is not a deliverable we can promise.
- All claims marked TO FETCH above must be read in the primary source before
  they are used as premises of any experiment or manuscript claim
  (methodology 12, P1/P3).
- The conjecture is open; nothing in the 2024-2026 sweep suggests a claimed
  resolution. If one appears, the independence rule from the
  unsplittable-flow-cost program applies: record provenance, verify
  independently before adoption.
