# The Chebyshev-tower obstruction: why the doubling factory stalls over Z

Derivation note, 2026-08-01 (RL-4 / TCB-016). All results here are [D]: our
own elementary proofs, machine-checked in `code/tclib/test_tclib.py`
(test_chebyshev_tower). Motivated by EXP-002's mechanism discovery: the
depth-5 records are difference-of-squares splittings on $C(x) := x^2 - 2$.

## 1. Setting

$C(x) = x^2 - 2$ is the integer model of angle doubling: under
$h(z) = z + 1/z$, $C(h(z)) = h(z^2)$. Over $\mathbb{R}$ (on $[-2,2]$,
$x = 2\cos\theta$: $C(2\cos\theta) = 2\cos 2\theta$) iteration doubles
oscillations: $C^k(x) - x$ has $2^k$ real roots, at SLP cost
$\tau(C^k(x) - x) \le 2k + 2$ (build $-2$: 1 gate; $x^2$: 1; $+c$: 1; then
each iterate square-and-add 2 gates; final $-x$: 1). This is the same
exponential real-root factory as Rojas' logistic Example 1 (the two maps
are affinely conjugate). The tau conjecture demands that its INTEGER root
count stay polynomial. It does far better: it stalls at a constant.

## 2. Lemma 1 (escape). If $|x| \ge 3$ then $|C(x)| \ge |x| + 1$.

Proof: $C(x) = x^2 - 2 \ge |x| + 1 \iff x^2 - |x| - 3 \ge 0$, true for
$|x| \ge 3$ ($9 - 3 - 3 = 3 > 0$, increasing in $|x|$). In particular
integer orbits starting at $|x| \ge 3$ have strictly increasing absolute
value, hence never revisit any value and never enter a cycle.

## 3. Lemma 2 (integer periodic points). For every $k \ge 1$, the integer
solutions of $C^k(x) = x$ are exactly $\{2, -1\}$.

Proof: an integer solution is a periodic point of $C$. By Lemma 1 a
periodic orbit lies in $S_0 := \{-2, -1, 0, 1, 2\}$. On $S_0$:
$0 \mapsto -2 \mapsto 2 \mapsto 2$, $1 \mapsto -1 \mapsto -1$. The only
cycles are the fixed points $\{2\}$ and $\{-1\}$; $0, \pm 2$ are
pre-periodic to $2$, and $1$ to $-1$. Fixed points solve
$x^2 - x - 2 = (x-2)(x+1) = 0$.

**Corollary (the constant-rate family).** For every $k$, the polynomial
$C^k(x) - x$ has EXACTLY 2 distinct integer roots and $2^k$ distinct real
roots, with $\tau \le 2k + 2$. The gap integer-vs-real is
$2$ vs $2^{(\tau-2)/2}$: the factory that kills the real analogue of the
conjecture contributes NOTHING over $\mathbb{Z}$ beyond its two rational
fixed points.

## 4. Lemma 3 (the DOS tower stalls at 5). Define
$G_k := C^{k-1}(x)^2 - C^k(x)^2$ for $k \ge 1$ (with $C^0 = x$). Then:

- $G_1$ has integer-root set $\{\pm 1, \pm 2\}$ (4 roots; this is the
  EXP-002 record shape at $\tau = 5$);
- for every $k \ge 2$, $G_k$ has integer-root set $\{0, \pm 1, \pm 2\}$
  (exactly 5 roots), at SLP cost $2k + 3$.

Proof: $G_k = (C^{k-1} - C^k)(C^{k-1} + C^k)$, so integer roots are the
integer solutions of $C^k = \pm C^{k-1}$, i.e. the $C^{k-1}$-preimages in
$\mathbb{Z}$ of $\{y : C(y) = y\} = \{2, -1\}$ and
$\{y : C(y) = -y\} = \{-2, 1\}$ (from $y^2 + y - 2 = (y+2)(y-1)$).
Integer preimages under $C$: $C^{-1}(2) = \{\pm 2\}$,
$C^{-1}(-1) = \{\pm 1\}$, $C^{-1}(-2) = \{0\}$, $C^{-1}(1) = \emptyset$
($x^2 = 3$), $C^{-1}(0) = \emptyset$ ($x^2 = 2$). Hence for $k = 1$:
roots $= \{2,-1\} \cup \{-2,1\}$. For $k = 2$: the preimage of
$\{\pm 1, \pm 2\}$ is $\{\pm 2\} \cup \{\pm 1\} \cup \{0\} = P :=
\{0, \pm 1, \pm 2\}$. For the induction: $C^{-1}(P) \cap \mathbb{Z} =
C^{-1}(\{2\}) \cup C^{-1}(\{-1\}) \cup C^{-1}(\{-2\}) \cup C^{-1}(\{1\})
\cup C^{-1}(\{0\}) = \{\pm 2, \pm 1, 0\} = P$: the integer preimage tree
STABILIZES at $P$, so every further tower level keeps root set $P$.
Cost: the chain $c = -2$, $x^2$, $A_1 = x^2 + c$, then per level the pair
(square, add $c$) reuses each square: $A_{k-1}^2$ sits at gate $2k$,
$A_k$ at $2k+1$, $A_k^2$ at $2k+2$, and $G_k = A_{k-1}^2 - A_k^2$ at
$2k+3$ (for $k \ge 2$; $G_1 = x^2 - A_1^2$ at 5, using the shared $x^2$).

## 5. What this proves, and does not

- PROVES (for this specific factory): composition of the doubling map
  cannot beat CONSTANT integer-root rate; the mechanism that generates
  the depth-5 census records is already saturated: one DOS split (4-5
  roots) is all it ever gives, at any depth. The reason is finiteness +
  stabilization of the integer preimage tree, forced by the escape bound
  (Lemma 1): a height obstruction invisible over $\mathbb{R}$.
- SUGGESTS (not proved): any fixed nonlinear integer polynomial map $h$
  with $|h(x)| > |x|$ outside a finite set has a finite stable preimage
  core, so single-inner-map towers $A \mapsto$ iterates of $h$ always
  stall at a constant root count. Candidate general lemma for the next
  round (needs care for $h$ with larger bounded regions, e.g.
  $h = x^2 - c$, where the core is $\{x : x^2 \le c + |x| \cdot 1\}$-ish
  and can be larger but still finite).
- DOES NOT touch multi-map factories (different inner polynomials per
  level, or products across shifted copies): those are exactly what the
  census ladder measures. The geometric-progression family stays the
  linear-rate record.

## 6. Machine verification

`test_chebyshev_tower` in `code/tclib/test_tclib.py` checks, exactly:
integer-root sets of $C^k(x) - x$ for $k \le 4$ (always $\{-1, 2\}$) and
of $G_k$ for $k \le 4$ ($G_1$: $\{\pm1, \pm2\}$; $G_2, G_3, G_4$:
$\{0, \pm1, \pm2\}$), building the polynomials by exact tuple arithmetic.
