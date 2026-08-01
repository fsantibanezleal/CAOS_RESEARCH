# 04: Mechanisms: how cheap polynomials acquire integer roots

Transcribed 2026-08-01 (round 4) from the EXP-001/002/003 verdicts and the
two derivation notes (`2026-08-01-chebyshev-tower-derivation.md`,
`2026-08-01-monic-stall-theorem.md`). All census facts are exact and
machine-verified; theorems are [D] with proofs in the notes.

## The move inventory (observed in census records, with gate costs)

| Move | Cost | Yield | First seen |
|---|---|---|---|
| Linear factor $x - a$, constant $a$ available | 2 (subtract, multiply) | +1 root ($a$) | depth 1-3 records |
| Multiply by the input $x$ | 1 | +1 root (0) | depth-6 records (EXP-003) |
| Block translation (roots $S \mapsto S + 1$) | +1 per unit shift | reuses a factor | depth-4 records |
| Difference-of-squares split $B^2 - A^2 = (B-A)(B+A)$ | 2 given $A, B$ | roots of both factors | depth-5 records (EXP-002) |
| Tower iterate $A \mapsto A^2 + c$ | 2 | bounded by the stall theorem | never a record beyond one split |
| Geometric-progression factor $(x - 2^{2^i})$, constants by squaring | ~3 per root | +1 root each | the literature's linear-rate record (Rojas) |

## The two theorems that bound mechanism classes

1. **Chebyshev-tower stall** ($h = x^2 - 2$): $h^{\circ k}(x) - x$ has
   exactly 2 integer roots for every $k$ (vs $2^k$ real roots at
   $\tau \le 2k + 2$); DOS towers over $h$ stall at $\{0, \pm1, \pm2\}$.
2. **Monic stall theorem** (any monic $h$, $\deg \ge 2$): a single-map
   tower's integer-root count is bounded by a constant $Z(h)$ INDEPENDENT
   of depth: the escape bound $|h(x)| \ge |x| + 1$ outside a finite ball
   forces a finite, stabilizing integer preimage core. Consequence: NO
   single-inner-map tower family can witness superpolynomial $z$ vs
   $\tau$; a refutation of the conjecture, if any, must build fresh
   constants or mix maps, paying gates for them.

## The emerging picture (two-sided reading)

Every record so far is a product of cheap low-degree factors whose roots
sit in a small ball around 0, assembled by the moves above; the only
known way to move roots OUT of the ball (translation, or geometric
constants) pays roughly a constant number of gates per root: linear
rate. The real-vs-integer divergence is now theorem-shaped: iteration
(free exponential real roots) is arithmetically sterile over $\mathbb{Z}$
(stall theorems), and what remains is constant-building, which the
census measures at $z = \tau - 1$ through depth 6. The bottom-law
question (does $z_{\max}(7) = 6$?) is exactly whether one more gate can
always be converted into one more root at this scale; EXP-004 decides
it.

## Census-calibrated dual values ($T(S)$ = min gates to vanish on $S$)

| $S$ | $T(S)$ | Witness |
|---|---|---|
| $\{0\}$, $\{1\}$, $\{-1\}$, $\{2\}$... | 1 | $x$; $x-1$; $x+1$; $2x - \dots$ (census depth 1) |
| $\{-1, 1\}$ | 2 | $x^2 - 1$ |
| $\{-1, 0, 1\}$ | 3 | $x^3 - x$ |
| $\{0, 1, 2\}$ (any consecutive triple) | 4 | $-x(x{+}1)(x{+}2)$-type |
| $\{\pm1, \pm2\}$, 4 consecutive | 5 | $x^2 - (x^2-2)^2$; $((x{-}1)^2 - x)^2 - 1$ |
| $\{0, \pm1, \pm2\}$ | 6 | $\mp x(x^2-1)(x^2-4)$ |

The moves calculus (round-4 addendum, view V7) will extend this table
with certified UPPER bounds past the census frontier.
