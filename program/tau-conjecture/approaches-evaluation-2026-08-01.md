# tau-conjecture: approaches evaluation (2026-08-01)

Requested evaluation of the most effective known approaches to the problem,
plus deliberately minted alternative views. Sources: the opening dossier plus
Rojas math/0304100 now READ IN FULL (this round). Effectiveness is judged on
two axes: (a) leverage on the conjecture itself, (b) what OUR exact-compute
program can contribute along that route. Tags as in the dossier.

## A. The known routes, evaluated

### A1. Counting-hierarchy / Valiant route (Koiran 2004, Buergisser 2009)
What it is: transfer the question into constant-free Valiant classes; the
conjecture (or just hard factorials) separates VP0 from VNP0; conversely an
easy permanent makes tau(n!) polylog. [V]
Leverage: the strongest STRUCTURAL consequences; this is why the conjecture
matters. But as a route TO the conjecture it consumes hypotheses we cannot
supply (P = PSPACE, VP0 = VNP0); nobody expects to prove the conjecture
through it.
Our contribution: exposition only (wiki page 02). EFFECTIVENESS FOR US: low
as attack, high as motivation. Status: adopt for wiki, not for experiments.

### A2. The p-adic / ultrametric route (Rojas 2003, READ IN FULL this round)
What it is: (i) the p-adic Digit Conjecture (bound only roots with first
p-adic digit 1) IMPLIES the full tau-conjecture for any fixed prime p
(Rojas Thm 1): a genuine REDUCTION of the problem. (ii) The valuation
spectrum: over additive complexity s, the number N_p(s) of distinct p-adic
norms of C_p-roots satisfies s <= N_p(s) <= s(s+1)/2, INDEPENDENT of p
(Thm 2, via p-adic Newton polygons: lower-hull edge counts obey
L_{i+1} <= L_i + i + 1). (iii) Roots in Q_p at additive complexity s:
<= 1 + s^3(s+1)(7.5)^s s! (Thm 3), the best rational-root bound to date in
terms of additive complexity. [V all]
Leverage: the only route that has PROVED nontrivial weak versions. The
exponential factor s! concentrates in counting roots near 1 (Thm 4); Rojas
flags exactly where the (necessary?) exponentiality sits.
Our contribution: REAL and unexplored. Two measurable open gaps: the true
growth of N_p(s) (Rojas: lower bound s realized by (x-1)(x-p)...(x-p^{s-1});
he BELIEVES quadratic is possible; nobody has data), and the open question
whether a p-adic analogue of the logistic root factory exists (his words:
"still an open question"). Both are census-measurable. EFFECTIVENESS: HIGH.
Status: ADOPTED: valuation-spectrum measurement added to the census
instrumentation (EXP-002 onward); dedicated N_2(s) record hunt as a
research line (RL-2).

### A3. Real-tau / Wronskian route (Koiran 2011; Tavenas; KPT15; Hrubes;
Briquel-Buergisser; Dutta SoS)
What it is: bound REAL roots of structured expressions (sums of products of
sparse polynomials); implies VP != VNP; true on average; equivalent
complex-root-clustering forms. [V statements via survey]
Leverage: the most active modern line, but it deliberately REPLACES the
integer question (the literal real analogue is FALSE: the logistic family
g_{j+1} = 4 g_j (1 - g_j) makes g_j(x) - x have 2^j roots in (0,1) at
tau = O(j); Rojas Example 1, now [V]).
Our contribution: contrast data (real-root censuses of the same enumerated
programs) is cheap instrumentation; deciding the variant conjectures is not
in our reach. EFFECTIVENESS FOR US: medium (as contrast + exposition).
Status: instrument later (TC-P3), read KPT15 first.

### A4. Height / arithmetic-geometry route (Cheng 2003/2004; Lipton 1994)
What it is: upper bounds on tau'(n!) via torsion points on elliptic curves
(the L-conjecture link) and smooth numbers; factoring connections (easy
factorials => fast factoring; average-hard factoring => weak tau
statements). [V attributions; originals TO FETCH]
Leverage: it attacks the UPPER-bound side (constructions), where the
conjecture's refutation would live; Cheng's remark that improving even the
constant in trivial lower bounds is already hard (via the WL-conjecture
implying the Torsion Theorem) is a caution sign for lower-bound hopes.
Our contribution: the integer census (Markstroem extension) IS this route's
experimental side. EFFECTIVENESS: medium-high. Status: adopted via RL-6;
read Cheng before any claim.

### A5. Proof-complexity route (Alekseev-Grigoriev-Hirsch-Tzameret)
IPS lower bounds conditioned on tau-like statements. [V listing only]
Leverage on the conjecture: indirect. Our contribution: none beyond
exposition. EFFECTIVENESS FOR US: low. Status: read later (TCB-014).

### A6. Exhaustive census route (Markstroem 2014; ours)
What it is: decide the bottom of the ladder exactly; hunt mechanisms.
Rojas, verbatim, on why this matters: "there is still no more elegant
method known to compute tau for a fixed polynomial than brute force
enumeration". [V]
Leverage on the conjecture: cannot decide it; produces the only exact
unconditional facts available, the extremal mechanisms, and the data that
the analytic routes (A2 especially) lack.
Our contribution: this is our comparative advantage (EXP-001: z_max(1..4) =
1,2,3,3, enumerator anchored 14/14 to Markstroem). EFFECTIVENESS: HIGH for
knowledge-per-compute at small tau; degrades exponentially with depth;
must hand off to structure lemmas (TCB-005) past tau ~ 6-7.
Status: the active spine.

## B. Alternative views minted this round (methodology 10/11)

### B1. The DUAL view: cost of a root set (new formulation, [C]/[D])
Define, for a finite S subset Z, T(S) := min { tau(f) : f != 0, S subset
roots(f) }. The tau-conjecture IS the statement T(S) >= |S|^{1/c} - 1. This
reframes the problem as the growth theory of a set-function with structure:
monotone; subadditive under union (T(S1 union S2) <= T(S1) + T(S2) + 1 via
product); translation costs at most tau(a) + 1 extra gates (compose with
x - a); scaling by 2 costs O(1) via x -> 2x... (each needs a one-line
proof). Known values from the census: T of any 1-set is 1... 2-set >= 2,
consecutive triples cost 3, {-1,0,1,2} costs 5 (EXP-002 candidate). The
geometric-progression set {2,4,...,2^{2^j}}-type gives the literature's
linear-rate record (Rojas page 2). QUESTION MINTED: is T superlinear on
ARITHMETIC progressions [1..n] (the Pochhammer-Wilkinson question in dual
form), and what set structure makes T cheap? Cheap sets are exactly the
conjecture's enemies. This view organizes the anatomy lens into a theory.

### B2. The valuation-spectrum view (from A2, adopted)
Instead of counting roots, count 2-ADIC NORMS of roots: N_2(s) is provably
in [s, s(s+1)/2] and its true growth is OPEN (Rojas believes quadratic).
Any polynomial with many integer roots must either spread its roots over
many valuations (pressuring N_2) or pile roots into ONE valuation class
(pressuring the digit conjecture near 1). The census can measure BOTH
pressures separately: per record, the valuation multiset of its roots. A
superlinear N_2 lower-bound family would be a publishable theorem-grade
find (it would sharpen where Rojas' program must lose its s!).

### B3. The iteration/composition view (why R and Z differ, [C])
The real-side root factory is ITERATION (logistic conjugate of Chebyshev):
composition doubles real roots for 3 gates. Over Z the same iteration
fails: integer roots of g compose only through integer points of the
preimage fibers, which arithmetic (height growth) starves. CONJECTURED
mechanism statement to formalize: for f = g composed with h (h nonlinear),
z(f) <= (number of integer points among h^{-1}(integer roots of g)), and
height growth of h forces this to stay linear in cost. If a clean lemma
"composition cannot beat linear rate over Z" were proved, combined with a
census-backed claim that all cheap mechanisms are products-of-composites,
it would delimit exactly where a counterexample cannot come from. Realistic
deliverable: the lemma for special shapes (monic h, |h| coercive), plus
census evidence. The p-adic side of this view is Rojas' open question (does
a p-adic logistic analogue exist?): a cheap family with 2^j roots in Q_p
would REFUTE the natural p-adic strengthening and explain the s! barrier.

### B4. The addition-chain import (technique view)
tau restricted to +,x from 1 is the addition-chain world (Scholz 1937;
Thurber; the OEIS A005245 integer-complexity culture): a century of
canonicalization, pruning and search technique for EXACTLY our Stage-A
search shape. Import their normal forms for the TCB-005 lemmas and for
pushing past Markstroem's length-11 frontier (they routinely exhaust much
deeper chains because their branching is smaller). Effort: medium; payoff:
frontier depth.

## C. Effectiveness ranking (what we actually do next)

1. **A6 + B1 (census + dual set-function view)**: the spine, EXP-002 now
   (tau = 5, decides minimal tau for 4 roots), then TCB-005 lemmas.
2. **A2 + B2 (p-adic instrumentation)**: valuation-spectrum measurement in
   EXP-002 (observational), then an N_2(s) record hunt as its own
   experiment; read Rojas' [Roj02] and the Newton-polygon lemma deeply
   (done: Thm 2 proof transcribed).
3. **B3 (composition obstruction)**: formalize the lemma candidates after
   EXP-002's mechanism data; this is the most theorem-shaped line we own.
4. **A4/RL-6 (integer frontier)**: Markstroem extension with addition-chain
   technique (B4), GPU/multiprocess when the DFS pays.
5. **A3/A5**: read-and-transcribe lines (wiki), no experiments until the
   primary reads are done.

Non-claims: none of these routes promises a proof of the conjecture; routes
are ranked by verifiable-knowledge-per-effort, and the two-sided reading
(every exclusion is a construction probe) applies throughout.
