# TCB-027 / V10: the F_p-versus-Z gap, measured as a census

Round 11b, 2026-08-25. The V10 three-worlds view says the conjecture should
be read as a statement about what the integers LACK relative to finite
fields. That has been an interpretive remark until now. This measures it on
exactly the same enumerated programs.

## The two censuses side by side

For each tau, over the SAME complete set of tau-gate polynomials:

    zmax(tau)  = max distinct roots over Z
    zpmax(tau) = max over primes p of distinct roots in F_p
                 (p ranges over all primes <= 257; a tau <= 5 polynomial has
                 degree <= 32, so the prime range is far past the degree bound)

    tau        1     2     3     4     5
    zmax(Z)    1     2     3     3     4
    zpmax(F_p) 1     2     4     8    16          = 2^(tau-1)
    ratio    1.00  1.00  1.33  2.67  4.00

The F_p ladder is EXACTLY 2^(tau-1) across the measured range: it doubles
with every gate. The integer ladder does not. The two agree at tau = 1, 2 and
separate from tau = 3 onward.

## The mechanism is Fermat's little theorem on Fermat primes

The maximizing witnesses are not exotic:

    tau = 3:  x^4  - 1     ->  4 roots mod 5
    tau = 4:  x^8  + 1     ->  8 roots mod 17
    tau = 5:  x^16 - 1     -> 16 roots mod 17

Repeated squaring builds x^(2^k) in k gates, and one more gate subtracts 1.
When p - 1 = 2^k (a Fermat prime: 5, 17, 257) every nonzero residue satisfies
x^(p-1) = 1, so x^(2^k) - 1 splits completely and has all p - 1 = 2^k roots.
The same polynomial has exactly TWO integer roots, x = +-1, for every k.

So one fixed cheap program shape yields exponentially many roots over F_p and
a constant number over Z. That is the whole content of the three-worlds view,
now with numbers attached.

## What is new here, and what is not

NOT new: that the tau conjecture's analogue fails over finite fields, and that
x^(p-1) - 1 is the standard reason. This is folklore in the area and is why
the conjecture is always stated in characteristic zero. We claim no priority
for it and cite it as known.

New: the like-for-like CENSUS. Both maxima are taken over the identical
enumerated set of tau-gate polynomials, so the ratio is a statement about the
same programs rather than a comparison of two separately chosen families. The
exhaustive value zpmax(tau) = 2^(tau-1) for tau <= 5 is, as far as we know,
not recorded anywhere, and it is what makes the gap quantitative.

## The reformulation this suggests

Over F_p the multiplicative group is cyclic of order p - 1, so x^d = 1 has
gcd(d, p-1) solutions, up to d of them. Over Z the unit group is {+-1}: the
equation x^d = 1 has at most two solutions for every d. The exponential F_p
ladder is precisely the 2^k-torsion that the cyclic group has and Z does not.

In that reading the conjecture is a quantitative statement that the integers'
lack of large torsion cannot be worked around by any program shape, not only
by the cyclotomic one. Our census is consistent with that: across all
tau <= 8 polynomials, nothing recovers more than linear growth over Z, while
the F_p side doubles every gate.

## CLOSED, same session: zpmax(tau) = 2^(tau-1) for every tau

This note first recorded the exact value as an open target, on the grounds
that the Fermat primes run out at 65537 and that degree alone gives only
2^tau. Both objections dissolve; the statement is a theorem.

UPPER BOUND. For a value v of a constant-free program let mu(v) count the
multiplicative gates in its sub-DAG. Then deg(v) <= 2^mu(v), by induction:
x has degree 1, constants degree 0, an additive gate satisfies
deg(a +- b) <= max(deg a, deg b), and a multiplicative gate satisfies
deg(a b) = deg a + deg b <= 2^mu(a) + 2^mu(b) <= 2^(mu(a)+mu(b)+1). A program
with NO additive gate computes only +-x^k or 0, since the free constants are
-1, 0, 1 and products of those stay in {-1,0,1}; such a polynomial has at most
ONE distinct root in any field. So a non-monomial f has at most tau-1
multiplicative gates, hence degree at most 2^(tau-1), hence at most 2^(tau-1)
roots in any F_p in which it does not vanish identically.

The bound is tight as a degree bound too: over the complete census to depth 5,
the maximum degree of a non-monomial is exactly 2^(tau-1) at every tau [MV].

LOWER BOUND. The Fermat primes are a red herring: what is needed is only a
prime p = 1 (mod 2^k), and Dirichlet supplies one for every k. Modulo such p
the polynomial x^(2^k) - 1 has exactly gcd(2^k, p-1) = 2^k roots, and it costs
k squarings plus one subtraction, so tau = k+1. Verified directly for
k = 1..8 (p = 3, 5, 17, 17, 97, 193, 257, 257), root counts exactly
2, 4, 8, 16, 32, 64, 128, 256 [MV].

So the finite-field question is completely settled, and the answer is
EXPONENTIAL:

    zpmax(tau) = 2^(tau-1)      (theorem, all tau)
    zmax(tau)  = 1,2,3,3,4,5,5,6 (exhaustive census, tau = 1..8)

The contrast is the point. The analogue of the conjecture over F_p is not
merely false, it is false at the maximum rate the degree permits, and the
extremal programs are the cheapest imaginable: repeated squaring, then
subtract one. Whatever makes the integer side hard is exactly what removes
that construction, and the census says the integers give back only linear
growth in its place.

## Instrument note: the same degeneracy, a third time

The first run of this measurement returned zpmax = 2, 3, 5, 17, 83 with
CONSTANT witnesses (2), (-3), (5), (17), (83). A nonzero constant c reduces to
the zero polynomial of F_p whenever p divides c, and then it vanishes at every
residue. That is the F_p analogue of f = 0, not a root count.

This is the third appearance of the same trap in this problem: the CEGAR loop
blocked on 179,649 zero-polynomial cases, EXP-013 had to exclude identically
zero polynomials from its window agreements, and now the mod-p instrument.
The rule to carry forward: any root-counting instrument must first exclude the
zero object OF THE RING IT COUNTS IN, and "the polynomial is nonzero over Z"
does not imply "its reduction is nonzero over F_p".
