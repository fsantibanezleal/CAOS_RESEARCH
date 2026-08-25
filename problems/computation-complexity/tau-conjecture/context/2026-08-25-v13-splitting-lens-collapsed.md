# V13 proposed, and collapsed: splitting is cheap, DISTINCTNESS is the cost

Round 11b, 2026-08-25. Recorded because the framing failed, and the reason it
failed is the useful part.

## The proposal

Every census record is fully split over Z (verified for tau <= 5: at each tau
the record polynomial's integer roots account for its entire degree, counting
multiplicity) [MV]. That suggested reading zmax(tau) not as "how many roots fit"
but as "how much DEGREE a cheap program can carry while splitting completely
over Z". Since degree alone reaches 2^(tau-1), the whole exponential-to-linear
gap would then be the splitting condition.

## Why it collapsed

Splitting is cheap. Define S(tau) as the largest degree a NON-MONOMIAL tau-gate
polynomial can reach while splitting completely over Z. Measured:

    tau            1    2    3    4    5
    S(tau)         1    2    4    8   16       = 2^(tau-1), the degree ceiling
    zmax(tau)      1    2    3    3    4

S(tau) attains the ceiling exactly. The mechanism is one gate wide: squaring a
split polynomial keeps it split and doubles its degree. Five gates give

    q = x^2 - x   (2 gates), then three squarings  ->  q^8

degree 16, splitting completely over Z as x^8 (x-1)^8, and exactly TWO distinct
integer roots [MV].

So the constraint is not splitting. A cheap program can be fully split at
exponential degree. What it cannot do is be fully split at exponential degree
with DISTINCT roots.

Two earlier degeneracies in the same measurement, both the same species: the
monomial c*x^k is trivially "fully split" and reaches degree 2^tau, and had to
be excluded before S(tau) meant anything; and before that, the constant
polynomials had to be excluded from the mod-p census because they vanish
identically mod p. Recurring rule, now four times in this problem: exclude the
degenerate object of whatever structure you are counting in, BEFORE reading the
maximum.

## What survives

    Multiplicity is nearly free. Distinctness is the entire cost.

That is a sharper statement of what the census measures than "roots are
expensive", and it lines up with the three-worlds table. Over F_p the extremal
program x^(2^k) - 1 is split at degree 2^k with all roots DISTINCT, because the
cyclic group supplies 2^k distinct solutions of x^(2^k) = 1. Over Z the same
degree is reachable and splitting is reachable, but the distinct roots are not:
Z^* = {+-1} offers two. The conjecture asks that no program shape recover
distinctness at exponential scale over Z.

No new view is minted from this. V13 is withdrawn as a lens; the surviving
sentence is folded into the V10 three-worlds reading, where it belongs.
