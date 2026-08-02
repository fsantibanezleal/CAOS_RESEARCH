# V10: the three-worlds view: the tau conjecture as quantitative absence of Frobenius over Z

Exploration note, 2026-08-02 (round 8, second sweep). All computations
here are one-line and [D]; folklore statuses marked; the adjacent
literature cited for the finite-field world.

## One program, three worlds

Take the SLP: repeated squaring to $x^{2^k}$ ($k$ gates), then one
subtraction: $f_k = x^{2^k} - x$, so $\tau(f_k) \le k + 1$. Read its
distinct-root count over three coefficient worlds:

| World | Roots of $x^{q} - x$-type programs | Growth vs $\tau$ |
|---|---|---|
| $\mathbb{F}_p$ (take $x^p - x$, $\tau \le \lceil \log_2 p \rceil + 1$) | ALL of $\mathbb{F}_p$: $p$ roots | $z \sim 2^{\tau}$: maximal violation |
| $\mathbb{R}$ | $\{-1, 0, 1\}$ for $f_k$; but Chebyshev/logistic programs give $2^k$ real roots at $\tau = O(k)$ | $z \sim 2^{c\tau}$: violation (Rojas Example 1 [V]) |
| $\mathbb{Z}$ | $f_k$: exactly $\{-1, 0, 1\}$ | conjecturally $z \le (1+\tau)^{\kappa}$ |

The $\mathbb{F}_p$ row is folklore ($x^q - x$ is the standard two-term
polynomial with $q$ roots; the finite-field SPARSE analogue is an active
literature: finite-field Descartes bounds of Bi-Cheng-Rojas 2013;
"Sparse univariate polynomials with many roots over finite fields",
arXiv:1411.6346; Kelley-Owen and Dwan-adjacent value-set work [MV: all
abstract-level]). The $\mathbb{R}$ row is Rojas' Example 1 [V]. The
$\mathbb{Z}$ row is the conjecture.

## The structural reading

Both failures are driven by a CHEAP COINCIDENCE-RICH ENDOMORPHISM of the
world's arithmetic:

- Over $\mathbb{F}_p$: Frobenius $x \mapsto x^p$ is a RING endomorphism
  fixing everything; $x^p - x$ is "identity minus Frobenius", and its
  kernel is the whole field: exponentially many roots for linearly many
  gates.
- Over $\mathbb{R}$ (on $[-2, 2]$): the doubling map $x^2 - 2$ is
  semiconjugate to angle doubling ($h(z) = z + 1/z$): a cheap map with
  $2^k$-point coincidence sets $C^{\circ k}(x) = x$: same shape,
  analytic rather than algebraic.
- Over $\mathbb{Z}$: the only ring endomorphism is the identity, and our
  stall theorems (2026-08-01 notes, [D]) are exactly the quantitative
  form of the missing middle: ANY single polynomial map's coincidence
  sets $h^{\circ k}(x) = \pm x$-type stay in a bounded core (escape +
  Northcott-flavored finiteness), and integer polynomial cycles have
  length $\le 2$ (classical). The tau conjecture is thus, in mechanism
  terms, the assertion that NOTHING repairs the absence of Frobenius
  over $\mathbb{Z}$: not iteration (stall theorems: closed), not
  parameterized families (EXP-005 for quadratics: closed), so any
  refutation must assemble its coincidences from CONSTANT-BUILDING,
  whose measured price (the census plateaus, the digit ladders) is the
  program's core data.

## Why this is useful, concretely

1. It unifies the paper's narrative (the three failure/openness rows
   make the conjecture's arithmetic nature vivid: candidate wiki-01 and
   next-paper-version content).
2. It gives the digit census (V9) its meaning: Rojas' digit classes
   $r \equiv 1 \pmod p$ are the shadow over $\mathbb{Z}$ of the
   $\mathbb{F}_p$ world where the conjecture dies; measuring
   $z^{(p,1)}_{\max}$ is measuring how much Frobenius-like coincidence
   survives reduction mod $p$ while staying integral. Smoke data:
   through $\tau = 6$ the odd-digit ladder reaches 3 vs the full
   ladder's 5.
3. It suggests a precise mod-p instrumentation (queued, cheap): for
   census records, compare $z(f)$ with the root counts of $f \bmod p$
   in $\mathbb{F}_p$: how far below the Frobenius ceiling do cheap
   integer polynomials sit mod small primes? (New backlog row.)

## Honesty

The three-worlds table is expository unification, not a theorem beyond
its one-line rows; the "quantitative absence of Frobenius" phrasing is a
READING of our proved stall results, not a new mathematical claim. The
finite-field sparse literature attacks a DIFFERENT parameter (term
count, not SLP length); no source found states the SLP-length
three-worlds contrast explicitly, so it is [C]-novel as exposition and
should be presented as such.
