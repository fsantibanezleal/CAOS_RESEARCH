# 01: Statement and history

Transcribed 2026-08-01 from `../context/2026-08-01-deep-research-dossier.md`
and the full read of Rojas math/0304100. Tags as in the dossier.

## The model

A constant-free straight-line program for $f \in \mathbb{Z}[x]$ is a
sequence $(1, x, f_2, \dots, f_N)$ with $f_N = f$, where each $f_i$
($i \ge 2$) is a sum, difference, or product of two earlier entries.
$\tau(f)$ is the least possible $N - 1$. [V: Rojas math/0304100, Def. 1;
equivalent to the constant-free circuit definition with free constants
$-1, 0, 1$ in Buergisser's 2024 survey, section 4.6.]

Two remarks fix intuition:

- $\deg f \le 2^{\tau(f)}$ (degree at most doubles per gate), so trivially
  $f$ has at most $2^{\tau(f)}$ integer roots. [V: Rojas, page 2.]
- With integer DIVISION allowed, $n!$ becomes easy to compute (Shamir
  1979), and the whole question collapses; the restriction to
  $+, -, \times$ is essential. [V: Koiran 2004, section 2.1.]

## The conjecture

**Shub-Smale tau conjecture (1995; Smale's problem 4).** There is an
absolute constant $\kappa \ge 1$ such that every nonzero
$f \in \mathbb{Z}[x]$ has at most $(1 + \tau(f))^\kappa$ distinct integer
roots. [V: Rojas, page 2; survey eq. (4.5). Original: Shub-Smale, Duke
Math. J. 81(1):47-54, 1995, TO FETCH.]

Sharpness of the exponent: the conjecture FAILS for $\kappa < 1$, by
$(x - 2^1)(x - 2^2)\cdots(x - 2^{2^j})$: geometric-progression roots are a
linear-rate root factory (each factor costs O(1) gates: square the previous
constant, subtract, multiply). As of the 2003 survey point, the conjecture
was open EVEN for $\kappa = 1$; our census data (EXP-001/002) measures
exactly this bottom regime. [V: Rojas, page 2.]

## Why the real analogue fails

Let $g_1 = 4x(1-x)$, $g_{j+1} = 4 g_j (1 - g_j)$ (the logistic/Chebyshev
iteration). Then $g_j(x) - x$ has exactly $2^j$ roots in $(0,1)$, yet
$\tau(g_j(x) - x) = O(j)$: over $\mathbb{R}$, composition doubles roots for
constant cost, so no real-root analogue of the conjecture can hold. The
conjecture is thus irreducibly ARITHMETIC: integer roots must be scarce for
cheap polynomials even though real roots need not be. Whether a p-adic
analogue of this root factory exists is an open question (Rojas). [V:
Rojas, Example 1 and following remark.]

## History ladder (abbreviated)

- 1976-1985: Borodin-Cook prove real roots are bounded in terms of ADDITIVE
  complexity; Grigoriev and Risler sharpen (bounds of shape
  $2^{O(s^2)}$). [V: Rojas, section 1.1 attributions.]
- 1989-1998: the BSS model; the conjecture (1995) as the number-theoretic
  route to $P_{\mathbb{C}} \ne NP_{\mathbb{C}}$; the book account
  (BCSS98). [V: survey; Koiran 2004.]
- 1996-1997: de Melo-Svaiter and Moreira: almost all integers $n$ have
  $\tau(n) \ge \log n / \log\log n$; still NO nontrivial lower bound for
  the specific sequence $\tau(n!)$. [V: Koiran 2004.]
- 2003: Rojas' ultrametric program: the p-adic Digit Conjecture (bounding
  only roots with first p-adic digit 1) already implies the full
  conjecture; subquadratic valuation-spectrum bound; best additive-
  complexity root bounds. [V: read in full.]
- 2004-2009: Koiran and Buergisser: the counting-hierarchy bridge to
  constant-free Valiant classes (see page 02). [V: Koiran 2004 read;
  TR06-113 abstract.]
- 2011-2021: the real-tau family (Koiran; Tavenas; KPTT Newton polygons;
  Hrubes; Briquel-Buergisser average case; Dutta SoS). [V: survey.]
- 2013-2014: Markstroem's exhaustive integer census (lengths <= 11), exact
  $\tau'(n!)$ for $n \le 28$. [V: read in full.]
- 2024-2026: survey consolidation (Buergisser); tau conjecture applied to
  explicit exponential lower bounds (BBDM); BSS-to-Valiant uniform bridge
  (Buergisser 2026). No claimed resolution. [V: abstracts.]

## Our census (this program)

$z_{\max}(\tau) = 1, 2, 3, 3$ for $\tau = 1..4$ (EXP-001, decision-
complete), with the enumerator anchored to Markstroem's published values;
$\tau = 5$ decided by EXP-002 (see page 03 when transcribed).
