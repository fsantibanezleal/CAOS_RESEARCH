# The scaling gap, measured exactly: T({0,+-2,+-4}) = 8 while T({0,+-1,+-2}) = 6

Derivation note, 2026-08-24. Closes the first case of TCB-031, the open
item minted by the RL-3 structure lemmas (2026-08-19), which proved
anti-monotonicity and +1 costs for UNION, TRANSLATION and REFLECTION but
showed that SCALING has no elementary substitution: over Z there is no
"x/2" to substitute, so nothing forces T(2S) close to T(S).

## Result

    T({0, +-1, +-2}) = 6      (census: minimal tau for 5 roots)
    T({0, +-2, +-4}) = 8      (this note)

so doubling this root set costs EXACTLY two extra gates. Scaling is
therefore provably NOT in the same +1 class as translation and
reflection, and the gap is not an artefact of a weak construction: both
bounds are exact.

## Upper bound (explicit, 8 gates) [D, machine-checked]

    1. u   = x * x            (x^2)
    2. two = 1 + 1            (2)
    3. four= two * two        (4)
    4. A   = u - four         (x^2 - 4)
    5. six = four * four      (16)
    6. B   = u - six          (x^2 - 16)
    7. C   = A * B
    8. f   = x * C            roots {0, +-2, +-4}

## Lower bound (from the census, exactly) [MV]

Suppose T({0,+-2,+-4}) <= 7. Then some f with tau(f) <= 7 vanishes on
that 5-element set. By EXP-004, z_max(7) = 5, so f has AT MOST 5 distinct
integer roots; containing a 5-element set, its root set is EXACTLY
{0,+-2,+-4}. But EXP-007 saved every five-rooter of tau <= 7 (67
polynomials: the 63 new at depth 7 plus the 4 records at depth 6) and
their root sets realise exactly seven patterns:

    {-4,-3,-2,-1,0}  {-4,-2,-1,0,1}  {-3,-2,-1,0,1}  {-2,-1,0,1,2}
    {-1,0,1,2,3}     {-1,0,1,2,4}    {0,1,2,3,4}

None is {0,+-2,+-4}. Hence T >= 8, and with the witness above, T = 8.

## Reading

Every five-rooter reachable in 7 gates has its roots inside a window of
five CONSECUTIVE integers (up to one puncture). The doubled set is spread
over nine integers, and reaching it forces building the constants 4 and
16 rather than reusing the free small ones: the same constant-building
friction the census plateaus expose, now visible as an exact price on a
structural operation. This is also a small independent confirmation that
the dual set-function T is not translation-invariant-plus-cheap in
general: its behaviour under dilation is where the cost lives.

## Open (next cases for TCB-031)

Is T(kS) - T(S) unbounded in k? The natural guess is yes, growing like
the cost of building k^2-scale constants (about 2 log k gates), but our
lower-bound technique needs a census at the corresponding depth, so it
is currently checkable only for small k. Recorded as open, not claimed.
