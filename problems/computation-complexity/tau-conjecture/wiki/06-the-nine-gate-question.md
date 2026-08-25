# 06: The nine-gate question (the seven-root threshold)

Transcribed 2026-08-24 from the EXP-011/012 verdicts, the growth-rhythm
note and the scaling-gap note. The additive half is still running; this
page states exactly what is decided and what is not.

## The question

The census is decision-complete through depth 8:

    tau  : 1 2 3 4 5 6 7 8
    zmax : 1 2 3 3 4 5 5 6

and the cost thresholds are 3 roots at 3 gates, 4 at 5, 5 at 6, 6 at 8.
The next threshold is the first genuinely open one: how many gates does
7 distinct integer roots cost? An explicit 10-gate witness exists, and
z_max(8) = 6 excludes 8, so the answer is 9 or 10.

## Why the ninth gate is decidable at all

By the last-gate lemma, a 9-gate program is one gate over a depth-8
state, and any depth-8 state is one gate over a depth-7 state. Because
z_max(8) = 6, the final gate of a 9-gate 7-rooter MUST involve the 8th
value (otherwise the polynomial would be computable in 8 gates, and 8
gates cannot reach 7 roots). That splits the question in two:

- **Multiplicative last gate**: f = v8 * b, and then
  z(f) = |R_v8 union R_b|: a union of two ALREADY KNOWN root sets. No
  polynomial arithmetic is needed in the inner loop, only set unions.
- **Additive last gate**: f = v8 +- b. Root sets do not compose across
  addition, so this case needs a different instrument entirely.

## The multiplicative case: DECIDED, empty

EXP-012 scanned every one of the 1,048,460,912 depth-7 states, every
one-gate extension and every operand:

    max |R_v8 union R_b| = 6      unions reaching 7: ZERO

so **no 9-gate program whose last gate is a multiplication has 7
distinct integer roots**. The scan was gated first: the same machinery at
threshold 6 found 793 unions on a single partition, so it detects unions
when they exist.

## The additive case: in progress

Root sets are useless here, so the instrument works with VALUES: every
operand and every extension is evaluated on the window [-32, 32] modulo
a 31-bit prime, and f = v8 +- b vanishes at a point only if the residues
agree, so counting modular agreements never misses a witness. Only
candidates reaching 7 agreements are promoted to exact polynomial
construction and exact root counting. Two traps were fixed before
production (61-bit primes overflow int64 under modular multiplication;
identically-zero polynomials agree at every window point and were
excluded rigorously, since a nonzero polynomial of degree < 65 cannot
vanish at 65 points). Emptiness on this side is therefore WINDOWED: it
excludes only witnesses whose seven roots all lie in [-32, 32].

## What each outcome means

The census increments (+1, +1, 0 repeating) fit a closed form predicting
z_max(9) = 7, i.e. the rhythm predicts a nine-gate seven-rooter. That
prediction is already refuted on the multiplicative side. If the
additive side is also empty:

- the seven-root threshold is 10 (windowed on the additive side),
- z_max(9) = 6, a THIRD plateau, and the 2-roots-per-3-gates rhythm
  breaks for the first time at tau = 9.

The q-ladder arithmetic anticipates exactly this: the ladder's next
factor needs the constant 12, which costs two gates to build rather than
one, so the accounting that bought two roots per three gates stops
being purchasable there. The independently measured scaling gap
(T({0,+-1,+-2}) = 6 but T({0,+-2,+-4}) = 8) is the same phenomenon
priced on a different operation: past the free small constants, roots
get more expensive.

## The upper bound, now verified: two ten-gate witnesses

The 10-gate bound was stated in prose in round 8. It is now written out as
explicit programs and executed gate by gate
(`../scripts/seven_root_two_witnesses.py`). Two structurally different
programs reach seven roots in ten gates:

**A, folding.** With $q = x^2 - x$, the exhaustive 8-gate six-rooter is
$q(q-2)(q-6)$, and $q - 6 = (q-2) - 4$, so no constant 6 is needed;
appending $\times (x-4)$ costs two gates. Roots $\{-2,\dots,4\}$, the
INTERVAL, height 56.

**B, squaring.** $x^2(x^2-1)(x^2-4)(x^2-16)$, constants by repeated
squaring $2 \to 4 \to 16$. Roots $\{0,\pm 1,\pm 2,\pm 4\}$, a TOWER,
height 84.

Witness B generalizes: $p_m = x^2(x^2-1)\prod_{i=2}^{m+1}(x^2 - t_i)$ with
$t_{i+1} = t_i^2$ gives $z = 2m+3$ roots in $\tau = 3m+4$ gates, verified
for $m = 0..4$. It is optimal at $m=0$ (3 roots in 3 gates, matching the
census threshold) but NOT at $m=1$ (5 roots in 7 gates, where the census
does it in 6), so it supplies upper bounds only.

## V12: folding and squaring have opposite parity

The two witnesses use different mechanisms, and the difference is one of
parity:

- **Folding** ($q = x^2-x$) identifies $x$ with $1-x$, so every value with
  integer preimages contributes exactly TWO roots: folding natively gives
  EVEN counts, and an odd count costs an extra linear factor.
- **Squaring** ($y = x^2$) has one self-paired value, $0$, whose preimage
  is the single root $x=0$: squaring natively gives ODD counts, $2m+3$.

At seven, an odd target, the tower is native and the interval needs its
patch, and they come out EQUAL at ten gates. Through the whole exhaustive
range ($z \le 6$) the minimal-gate sets are intervals. The census range
therefore ends exactly where the two mechanisms tie, and never separates
them.

Height does separate them: 56 for A against 84 for B, and 15 against 84 at
six roots. This matches the TCB-030 height measurement (minimal height
$1,1,2,4,15$ for $z=2..6$, achieved by intervals): additively-structured
root sets are height-cheap, multiplicatively-structured ones buy their
constants at doubly exponential magnitude. A lower-bound argument tuned to
one mechanism will be blind to the other.
