# V10 completed: the three worlds, all measured on the same programs

Round 11b, 2026-08-25. The three-worlds view (F_p / R / Z) has been an
interpretive frame since round 8. All three columns are now filled with
proved or exhaustively measured values, over the IDENTICAL enumerated set of
tau-gate polynomials, so they are comparable term by term.

    tau                1    2    3    4    5
    zmax over Z        1    2    3    3    4        exhaustive census
    zRmax over R       1    2    3    4    6        exhaustive, exact (Sturm)
    zpmax over F_p     1    2    4    8   16        = 2^(tau-1), PROVED
    degree ceiling     1    2    4    8   16        2^(tau-1)

Three separations, each visible at a different tau:
- F_p leaves Z at tau = 3 and SATURATES the degree ceiling at every tau.
- R leaves Z at tau = 4 and does NOT saturate the ceiling (4 against 8, 6
  against 16).
- Z is below both from tau = 3 onward.

## How the real count was measured

Exactly, with no floating point: for each census polynomial take the
square-free part f / gcd(f, f'), then count real roots by Sturm's theorem in
exact rational arithmetic (sympy, domain ZZ). The instrument was gated on
seven known answers first, including x^2+1 (zero real roots), x^2 (a double
root counted once), Chebyshev T_4 (four), and (x^2-1)(x^2-4)(x^2-16) (six).
All seven passed before any production number was computed.
`scripts/real_census.py`, 20 s to depth 5.

Depth 6 is left for later: it needs the 25.8M-state frontier in RAM, and the
additive nine-gate scan is using the machine.

## The witness that says what the integers lose

The tau = 5 real record is not exotic, and it is built by the SAME
difference-of-squares mechanism the integer census identified as its own
record-maker:

    1  a = x * x          x^2
    2  b = a - 1          x^2 - 1
    3  c = b * b          (x^2 - 1)^2
    4  d = c - a          (x^2 - 1)^2 - x^2
    5  e = b * d

    e = (x-1)(x+1)(x^2 - x - 1)(x^2 + x - 1)

SIX distinct real roots: +-1, and +-phi, +-1/phi with phi the golden ratio.
TWO distinct integer roots: +-1. [MV]

Five gates, six real roots, and four of them are irrational. The program is
cheap, the roots are there, and the integers are simply not among them. This
is the conjecture's content in one line: the cost of a root set is not what
limits the real or finite-field worlds, and whatever limits Z is arithmetic,
not size.

It also sharpens the Chebyshev reading. A Chebyshev tower buys a doubling of
real roots for three gates (T_2(x) = 2x^2 - 1 costs three, and composition
repeats it), so it reaches about 2^(tau/3). The census beats that at tau = 5
with the DOS shape above (6 real roots, where a Chebyshev tower would give 4),
so the real ladder is not simply the Chebyshev ladder.

## Why F_p saturates and R does not

Over F_p the extremal program is x^(2^k) - 1: k squarings and one
subtraction, and modulo a prime p = 1 (mod 2^k) it splits COMPLETELY. One gate
per doubling. Over R the same polynomial has only two real roots, and making
real roots costs roughly three gates per doubling. The degree ceiling is
identical in both worlds; what differs is how cheaply a program can force the
roots to actually live in the field.

Stated as the open question this leaves: is zRmax(tau) = Theta(2^(tau/3)), and
does it ever approach the 2^(tau-1) ceiling? Our five points cannot tell, and
we do not claim a rate. The real analogue of the conjecture is known false,
which is all the paper needs; the ladder's exact growth is not something we
have measured far enough to assert.
