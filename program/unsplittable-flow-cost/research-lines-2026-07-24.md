# Research lines: unsplittable-flow cost conjecture (opened 2026-07-24)

Genuinely new directions produced by the round-1 lens pass and exploration moment
(`lenses-2026-07-24.md`, methodology/11). Each line names its first step so it can become
an EXP-declared experiment without re-thinking. None of these is in the opening brief.

## RL1. The conflict graph and the stable-set reading (the organising line)

Given an SSUF instance, build the conflict graph $H$ whose nodes are the cheap path
choices and whose edges join two choices that cannot both be selected without breaking
some arc bound $y_a \le x_a + d_{\max}$. Then a congestion-good routing selects an
independent set of $H$, while the fractional flow selects a point $\rho$ with
$\rho_i = x(\text{choice } i)/d_i$. A counterexample requires $\rho$ to lie outside the
stable-set polytope of $H$ AND that violated inequality to be separable by NONNEGATIVE ARC
COSTS.

First step: implement the instrument (UFB-023), compute $H$ and $\rho$ for the 2026
instance, and check that $\rho$ violates exactly the triangle inequality
$\rho_1 + \rho_2 + \rho_3 \le 1$ with value $16/15$.

Why it matters: it converts a flow question into a polyhedral one with a mature theory,
and it gives the cheap pre-filter that makes an exhaustive search affordable.

## RL2. The frontier constant as a thinning threshold

At violation budget $\alpha d_{\max}$ the conflict graph THINS: pairs that conflicted at
budget 1 may be compatible at budget $\alpha$. Define $H_\alpha$ accordingly. Then

$$\alpha^\* = \inf\{\alpha : \text{for every instance, } \rho \text{ is dominated by a convex combination of independent sets of } H_\alpha\}.$$

This is a reformulation of the open $O(d_{\max})$ question as a question about when a
family of conflict graphs becomes LP-integral enough to cover the fractional point. As far
as the sources read on 2026-07-24 show, this reformulation is not stated in the
literature. It is a candidate contribution in its own right, and it is the natural frame
for both lower bounds (exhibit instances where $H_\alpha$ stays too dense) and upper
bounds (show conflict graphs are always sparse or perfect enough at $\alpha = $ some
constant).

First step: state it precisely with the domination relation pinned down, verify the
equivalence with the original definition on the 2026 instance and on the EXP-001 hand
instances, and only then treat it as a definition worth building on.

## RL3. Minimality of the obstruction

Nobody has published how small a counterexample can be. With the separation LP removing
the cost vector and a canonical form removing isomorphs, the search over
(digraph, demands, fractional flow) up to a size bound is finite and exactly decidable.

First step: UFB-025, the base rung, no counterexample with at most two terminals, proved
by the conflict-graph argument (a graph on two nodes has no odd cycle, so the stable-set
polytope is integral and $\rho \le 1$ componentwise cannot be violated in a way costs can
separate). Then the arc/vertex ladder.

Why it matters: a machine-verified minimality statement is a durable, citable result that
stands independently of who found the first counterexample, and it is the kind of result
this repo's discipline is built to produce.

## RL4. Planar sharpness

The claimed counterexample is planar. TVZ24 prove the cost statement for planar graphs at
violation $2 d_{\max}$. If the counterexample verifies, then for planar graphs the true
constant lies strictly between 1 and 2, and TVZ24's 2 cannot be improved to 1. Neither
endpoint is stated in the literature we read.

First step: verify planarity exactly (not by looking at the drawing), and compute the
exact $\alpha_{\mathrm{inst}}$; that pair of facts is the statement.

Follow-up question, harder and more interesting: what IS the planar constant? The instance
gives $\alpha^\*_{\text{planar}} \ge 16/15$ if the expectation holds; TVZ24 gives
$\le 2$; the gap is wide open and is a well-posed target for the family constructions of
RL1/RL2.

## RL5. Where the DGG augmentation argument becomes cost-blind

The DGG theorem is proved by flow augmentation along designated cycles (as MSW25 describe
when they note that the Morell-Skutella lower-bound result "can also be achieved by
augmenting flow in the reverse direction along the designated cycles of Dinitz, Garg, and
Goemans"). The conjecture asks whether the same augmentation can be steered to be
cost-nonincreasing. Now that a counterexample is claimed, the interesting question flips:
the augmentation must NECESSARILY increase cost on the counterexample, and locating the
exact step where it is forced to do so explains the obstruction in the original proof's
own language.

First step: UFB-002, obtain and read the Combinatorica paper. Nothing here is actionable
before that read, and no claim about the technique may be made until then.

## RL6. Transfer to the portfolio

The stable-set / LP-integrality-gap reading is not specific to flows. Any rounding
conjecture of the form "an integral solution exists that is simultaneously good in a
budgeted resource and no worse in a linear objective" has the same anatomy: a conflict
structure among cheap choices, a fractional point outside its independence polytope, and a
nonnegative separator. That template is worth carrying to the optimization-geometry
problems in the portfolio (sphere-log-energy has no such structure; linear-programming and
tau-conjecture may). Recorded as an analogy, not a claim; promotion requires a concrete
target problem.
