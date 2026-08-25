# 07: The three worlds ($\mathbb{F}_p$, $\mathbb{R}$, $\mathbb{Z}$)

Transcribed 2026-08-25 from the round 11b measurements. The three-worlds
reading (V10) had been an interpretive frame since round 8. This page states
it with numbers, all taken over the SAME enumerated set of $\tau$-gate
polynomials, so the columns are comparable term by term.

## The three ladders

| $\tau$ | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| $z_{\max}$ over $\mathbb{Z}$ | 1 | 2 | 3 | 3 | 4 | 5 |
| $z_{\max}$ over $\mathbb{R}$ | 1 | 2 | 3 | 4 | 6 | 8 |
| $z_{\max}$ over $\mathbb{F}_p$ | 1 | 2 | 4 | 8 | 16 | 32 |
| degree ceiling $2^{\tau-1}$ | 1 | 2 | 4 | 8 | 16 | 32 |

The integer row continues $5, 6$ through $\tau = 8$ (decision-complete,
[03 the census](03-census.md)). The $\mathbb{F}_p$ row continues $2^{\tau-1}$
for every $\tau$, as a theorem. The real row is exhaustive through $\tau = 6$;
$\tau = 6$ was reached without a depth-6 census, by applying the last-gate lemma
to the 778,087-state depth-5 frontier (134,497 new polynomials, 180 s), with a
known-answer gate requiring the INTEGER maximum over the same set to come out
at 5 before the real number was reported.

Each world leaves $\mathbb{Z}$ at a different point: $\mathbb{F}_p$ at
$\tau = 3$, $\mathbb{R}$ at $\tau = 4$.

## $\mathbb{F}_p$: exactly $2^{\tau-1}$, proved

**Proposition.** $z^p_{\max}(\tau) = 2^{\tau-1}$ for every $\tau \ge 1$.

*Upper bound.* For a value $v$ let $\mu(v)$ count the multiplicative gates in
its sub-DAG. Then $\deg v \le 2^{\mu(v)}$: the input has degree 1, constants
degree 0, $\deg(a \pm b) \le \max(\deg a, \deg b)$, and
$\deg(ab) = \deg a + \deg b \le 2^{\mu(a)} + 2^{\mu(b)} \le 2^{\mu(a)+\mu(b)+1}$.
A program with no additive gate computes only $\pm x^k$ or $0$, since the free
constants are $-1, 0, 1$ and products of those stay in $\{-1,0,1\}$; such a
polynomial has at most one distinct root in any field. So a non-monomial has
at most $\tau - 1$ multiplicative gates, hence degree at most $2^{\tau-1}$.

*Lower bound.* By Dirichlet there is a prime $p \equiv 1 \pmod{2^k}$ for every
$k$. Modulo such $p$, $x^{2^k} - 1$ has exactly $\gcd(2^k, p-1) = 2^k$ roots,
and it costs $k$ squarings plus one subtraction. The Fermat primes that the
small cases suggest ($5, 17, 257$) are not needed.

Both halves machine-checked: the degree bound holds on every non-monomial in
the depth-5 census and is attained exactly at each $\tau$; the construction
was verified for $k = 1..8$.

That the analogue fails over finite fields is folklore, and is why the
conjecture is always stated in characteristic zero. What is ours is the
like-for-like census and the exact value.

## $\mathbb{R}$: measured exactly, and it does not saturate

Distinct real roots counted with no floating point: square-free part
$f/\gcd(f,f')$, then Sturm over $\mathbb{Z}$. The instrument was gated on
seven known answers first, including $x^2+1$ (none), $x^2$ (a double root
counted once), $T_4$ (four) and $(x^2-1)(x^2-4)(x^2-16)$ (six).

Unlike $\mathbb{F}_p$, the real ladder does NOT reach the degree ceiling: 4
against 8 at $\tau = 4$, 6 against 16 at $\tau = 5$. Making roots real is
cheaper than making them integral but dearer than making them exist in a
finite field.

### The witness that says what $\mathbb{Z}$ loses

$$a = x\cdot x,\quad b = a-1,\quad c = b\cdot b,\quad d = c-a,\quad e = b\cdot d$$

$$e = (x-1)(x+1)(x^2-x-1)(x^2+x-1)$$

Five gates. **Six** distinct real roots $\pm 1, \pm\varphi, \pm\varphi^{-1}$
with $\varphi$ the golden ratio, and exactly **two** distinct integer roots.
The program is cheap, the roots are there, and four of them are irrational.

Two further points. It is built by the same difference-of-squares mechanism
that [04 mechanisms](04-mechanisms.md) identifies as the integer
record-maker. And it beats a Chebyshev tower at equal cost: $T_2 = 2x^2-1$
costs three gates and composition repeats it, so a tower would give only four
roots here. The real ladder is not simply the Chebyshev ladder.

### The real record mechanism, and where it stalls

The $\tau = 6$ real record is
$x^8 - 7x^6 + 14x^4 - 7x^2 + 1 = (x^4-3x^2+1)(x^4-4x^2+1)$, and its left factor
is exactly the $\tau = 4$ record $g_1 = (x^2-1)^2 - x^2$. So the step from four
gates to six is

$$g \;\longmapsto\; g\cdot(g - x^2)$$

which costs **two** gates ($x^2$ is already in the state) and **doubles** the
real root count. That beats a Chebyshev tower, which costs three gates per
doubling, and it matches the exhaustive census at both $\tau = 4$ and
$\tau = 6$, so in that range it is the record and not merely a good
construction.

Iterating it, distinct real roots against degree:

| gates | 4 | 6 | 8 | 10 | 12 |
|---|---|---|---|---|---|
| degree | 4 | 8 | 16 | 32 | 64 |
| distinct real roots | 4 | 8 | 16 | 28 | 48 |

Three clean doublings, reaching 16 distinct real roots at 8 gates, and then the
polynomial stops being totally real. Successive ratios fall from 2 to 1.75 to
1.71. This is the same shape as the integer-side results: a natural doubling
construction runs a few steps and stalls, exactly as the monic stall theorem
describes over $\mathbb{Z}$. The real side stalls later and from a far higher
base.

We claim no growth rate for the real ladder. Six points cannot separate
$\Theta(2^{\tau/2})$ from its neighbours, the family's own rate decays after
$\tau = 8$, and the paper needs only the known failure of the real analogue.

A caution on record sets, since it is easy to overstate: an interval is always
*among* the minimal-gate record root sets in the exhaustive range, but it is not
the only one. At $\tau = 5$ the four-root records include the interval
$\{-1,0,1,2\}$ and also $\{\pm 1, \pm 2\}$, computed by $x^2 - (x^2-2)^2$, which
is not an interval. An earlier draft of these notes claimed all minimal-gate
record sets are intervals; the census refutes that.

One observation worth keeping: the $\tau = 6$ real record has **zero** integer
roots, while the $\tau = 6$ integer record has five. At equal cost the two
worlds are optimized by completely disjoint polynomials. The real ladder is not
the integer ladder with extra roots attached; it is a different extremal problem
that happens to share the difference-of-squares mechanism at the bottom.

## Multiplicity is free; distinctness is the cost

A tempting reading is that $z_{\max}$ measures how much DEGREE a cheap program
can carry while splitting completely over $\mathbb{Z}$. Every census record is
indeed fully split. But that reading collapses on measurement: splitting is
cheap. Squaring a split polynomial keeps it split and doubles its degree, so

$$q = x^2 - x \ \text{(2 gates)}, \ \text{then three squarings} \ \to\ q^8$$

has degree 16, splits completely over $\mathbb{Z}$ as $x^8(x-1)^8$, costs five
gates, and has **two** distinct roots.

So the constraint is not splitting and not degree. Cheap programs reach
exponential degree, and over $\mathbb{F}_p$ they split completely at that
degree with all roots distinct. Over $\mathbb{Z}$ the degree and the splitting
are both available; the distinct roots are not.

## Why the mechanism differs

In $\mathbb{F}_p^{\times}$, cyclic of order $p-1$, the equation $x^d = 1$ has
$\gcd(d, p-1)$ solutions, up to $d$ of them. In
$\mathbb{Z}^{\times} = \{\pm 1\}$ it has at most two, for every $d$. The
exponential $\mathbb{F}_p$ ladder is precisely the $2^k$-torsion that the
cyclic group carries and the integers lack.

Read this way the conjecture asserts that no program shape recovers over
$\mathbb{Z}$ what the cyclotomic one achieves over $\mathbb{F}_p$. The census
is consistent with that: through $\tau = 8$, nothing over $\mathbb{Z}$ does
better than linear growth. The gap being conjectured is now between a PROVED
exponential and a MEASURED linear rate, rather than between two informal
impressions.

## Instrument note

Every one of these measurements returned a confident WRONG maximum on its
first run, always for the same reason: the degenerate object of the structure
being counted was included. Constants vanish identically mod $p$ when $p$
divides them; monomials are trivially "fully split"; the zero polynomial
vanishes everywhere. Together with the zero-polynomial floods in the CEGAR
loop and in EXP-013, that is four occurrences in this problem. The standing
rule: exclude the degenerate object of the ring or structure you are counting
in, BEFORE reading off any maximum, and gate the instrument on known answers
first.
