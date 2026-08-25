# A fourth column: the rational ladder equals the integer one

Round 11c, 2026-08-25. The conjecture counts INTEGER roots. Its natural
algebraic relaxation counts RATIONAL ones, and it is not obvious in advance
which of the two constraints carries the difficulty. Measured on the same
enumerated programs:

    tau            1    2    3    4    5    6
    zmax over Z    1    2    3    3    4    5
    zQmax over Q   1    2    3    3    4    5

exhaustive through tau = 6. Rational roots computed exactly by the rational
root theorem over ZZ (sympy ground_roots), never numerically. Depth 6 reached
by the last-gate lemma over the 778,087-state depth-5 frontier, gated by
requiring the INTEGER maximum on the same 134,497-polynomial set to reproduce
the established zmax(6) = 5 before the rational number was reported.

## The ladders coincide, the extremal objects do not

Allowing denominators buys nothing in the maximum. But the rational world is
not a copy of the integer one: the tau = 6 rational record is

    8x^6 - 10x^4 + 2x^2 = 2x^2 (x-1)(x+1)(2x-1)(2x+1)

with FIVE distinct rational roots {0, +-1/2, +-1} and only THREE integer ones,
while the tau = 6 integer record attains five integer roots outright. Half
integer roots are cheap here, because the constants 2 and 4 are cheap, and they
still do not raise the ceiling.

## What it says

Integrality is not where the difficulty lives, at least at the bottom of the
ladder. The same growth function appears over Q, so whatever separates Z from
R and from F_p in the three-worlds table separates Q from them too. A proof
strategy that leans on integrality specifically, as opposed to on the
arithmetic of a number field's units, would have to explain why the rational
ladder behaves identically.

This is a measurement over the census range and nothing asymptotic follows from
it. It is also a genuinely cheap column to have: the whole thing costs 261 s.

## Scope

Exhaustive for tau <= 6 only. Extending to tau = 7 needs the 25.8M-state
depth-6 frontier resident, which the additive nine-gate scan currently rules
out.
