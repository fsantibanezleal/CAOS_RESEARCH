# Two ten-gate seven-rooters, and V12: folding vs squaring

Round 11b, 2026-08-25. The nine-gate scans can only prove a NEGATIVE (nine
gates do not reach seven roots). The threshold is pinned only if a
construction supplies the matching positive. This note makes that positive
explicit and machine-checked, and reports what comparing two of them shows.

## 0. What was already known, and what is new here

The 10-gate upper bound is NOT new: round 8 (EXP-007 verdict) already
stated it, in prose, as "append x (x - 4) to the 8-gate six-rooter, whose
state already contains the constant 4". That claim is correct, and it is
now verified rather than asserted.

New in this round:
1. both witnesses written out as explicit programs and executed gate by
   gate (the round-8 one had no artifact and no verification);
2. a second, structurally independent witness;
3. the square-tower FAMILY, which extends the ladder past the census;
4. V12, from comparing the two shapes.

## 1. Two ten-gate programs, seven roots each

**Witness A (folding).** q = x^2 - x; the exhaustive 8-gate six-rooter is
q(q-2)(q-6), and q - 6 = (q - 2) - 4, so no constant 6 is ever needed.

    1 g=x*x   2 q=g-x   3 c2=1+1   4 c4=c2*c2   5 a=q-c2
    6 b=a-c4  7 v=a*b   8 f=v*q    9 w=x-c4    10 p=f*w

f at gate 8 is the census record itself: roots {-2,-1,0,1,2,3}, height 15.
p has roots {-2,...,4}: the INTERVAL, seven roots, height 56.

**Witness B (squaring).** y = x^2, constants by repeated squaring.

    1 y=x*x   2 a=y+(-1)  3 t2=1+1   4 t4=t2*t2  5 b=y-t4
    6 t16=t4*t4  7 c=y-t16  8 d=y*a  9 e=b*c   10 p=d*e

p = x^2(x^2-1)(x^2-4)(x^2-16), roots {0,+-1,+-2,+-4}: a TOWER, seven
roots, height 84.

Both verified by `scripts/seven_root_two_witnesses.py`, which runs each
program as data through the census arithmetic and recomputes roots and
height from the expanded coefficients. Witness B is cross-checked against
an independent expansion in `scripts/seven_root_construction.py`.

**Consequence.** EXP-011 proved z_max(8) = 6, so seven roots need at least
nine gates. EXP-012 decided the multiplicative nine-gate case (empty). If
the additive case (EXP-013, running) is also empty, then

    minimal tau for 7 distinct integer roots = 10, exactly

lower bound exhaustive, upper bound constructive and now verified.

## 2. The square-tower family

    p_m(x) = x^2 (x^2 - 1) prod_{i=2}^{m+1} (x^2 - t_i),  t_1 = 2, t_{i+1} = t_i^2

gives z = 2m+3 roots in tau = 3m+4 gates: three gates per two roots. Each
constant is one squaring past the last, so it costs ONE gate, and each is a
perfect square, so it contributes a genuine PAIR of roots. Verified for
m = 0..4 by `scripts/square_tower_family.py` (roots out to {+-256}).

Checked against the exhaustive census in both directions, honestly:
- m = 0: 3 roots in 3 gates, and the census says minimal tau for 3 roots
  IS 3. Optimal here.
- m = 1: 5 roots in 7 gates, but the census says 6 suffice. **NOT optimal
  here.** The family only ever gives upper bounds; at seven roots it
  happens to meet the exhaustive lower bound, which is what would make ten
  exact.

Asymptotically z >= (2 tau + 1)/3: LINEAR. The conjecture permits
polynomial growth, so nothing here threatens it. No family we have found
or know of grows faster than linearly in the gate count, and the obvious
superlinear route (iterated quadratic towers) is precisely what our monic
stall theorem blocks.

## 3. V12: folding and squaring are two different cheap arithmetics

The two witnesses are not variants of each other. They exploit different
mechanisms, and the mechanisms have different PARITY:

- **Folding** (q = x^2 - x) sends x and 1-x to the same value, so every
  value with integer preimages contributes exactly TWO roots. Folding
  natively produces EVEN root counts, and reaching an odd count costs an
  extra linear factor (two gates: one subtraction, one multiplication).
- **Squaring** (y = x^2) has one self-paired value, 0, whose preimage is
  the single root x = 0. Squaring natively produces ODD root counts,
  2m+3.

At seven roots, an odd target, the tower is native and the interval needs
its patch, and they come out EQUAL at ten gates. Through the whole
exhaustive range (z <= 6) the minimal-gate root sets are intervals. So the
census range never separates the two mechanisms; it ends exactly where
they tie.

Height does separate them: witness A has height 56, witness B has 84, and
the six-root interval has height 15 against 84 for the six-root tower.
This lines up with the TCB-030 measurement (minimal height 1, 1, 2, 4, 15
for z = 2..6, achieved by intervals): the additively-structured sets are
the height-cheap ones, while the multiplicatively-structured ones buy
their constants with doubly exponential magnitude.

What V12 says for the conjecture: a lower-bound argument tuned to spread,
multiplicatively-built root sets will be blind to interval sets and vice
versa, and at the first odd count where both are available they cost the
same. Any proof has to cover both arithmetics at once.

Explicitly NOT claimed: that towers eventually beat intervals. Our earlier
draft of this note asserted a crossover at seven roots; that was wrong,
produced by pricing intervals only inside the x^2 family (where {-3..3}
costs 11) and overlooking the folding-based {-2..4} at 10. Corrected
before it left the working tree. Where the two rates actually separate, if
they do, is beyond what we have measured.

## Internal catch, recorded

The pricing helper that produced the first draft's table failed to charge a
gate for the `y - 1` factor and printed a NINE-gate seven-rooter, which
would have contradicted EXP-012's exhaustive scan. A summary table that
disagrees with an exhaustive scan is a bug in the table until proved
otherwise. The helper has been deleted; every count in this note now comes
from a program executed gate by gate, which is the only accounting that
cannot drift from the census convention.
