# 02: The implication ladder: why the tau conjecture matters

Transcribed 2026-08-01 from the opening dossier, the Koiran 2004 direct
read, the Rojas full read, and the approaches evaluation. Tags as in the
dossier; every claim carries its source.

## The chain downward from the conjecture

1. **Tau conjecture $\Rightarrow P_{\mathbb{C}} \ne NP_{\mathbb{C}}$**
   (Shub-Smale 1995). The proof route: it suffices that for EVERY sequence
   of nonzero integers $m_n$, the sequence $(m_n \cdot n!)$ is hard to
   compute, where $(a(n))$ is hard iff $\tau(a(n))$ is not polynomially
   bounded in $\log n$. Intuition: an easy Hilbert-Nullstellensatz decision
   procedure would let one build short programs for (multiples of)
   factorials; many integer roots of cheap polynomials are exactly what
   cheap factorials would provide, via
   $n! = \prod_{k=1}^{n}(x - k)\,\big|_{x=0}$-type specializations.
   [V: Buergisser 2024 survey 4.6; Koiran 2004 intro; Rojas SS95 citation.]
2. **Tau conjecture $\Rightarrow VP^0 \ne VNP^0$** (Buergisser 2009,
   building on Koiran 2004); already the single hypothesis "$(n!)$ is hard
   to compute" yields it. Tool: the counting hierarchy (Wagner 1986); the
   route shows an easy permanent forces $\tau(n!)$, and even
   $\tau(\prod_{k \le n}(X - k))$ with divisions, to be polylog. [V:
   survey Thm 4.17; TR06-113 abstract.]
3. **Koiran's concrete versions** (2004, read directly): $VP^0 = VNP^0$
   iff the Hamilton-cycle family is in $VP^0$; $VP^0 = VNP^0$ makes
   $\tau(\lfloor 2^{2^n} \ln 2 \rfloor)$ polynomial; adding $P = PSPACE$
   makes $n!$ ultimately easy. Contrapositive: prove $n!$ hard and you
   separate major classes. [V.]
4. **Factoring**: easy (multiples of) factorials give nonuniform
   polynomial-time integer factoring (Strassen's observation; BCSS p.126;
   Cheng 2003); with DIVISION $n!$ is genuinely easy (Shamir 1979), so the
   $+,-,\times$ restriction carries the entire difficulty. Average-case
   hard factoring implies weak tau statements (Lipton 1994). [V: Koiran
   2004 2.1; originals TO FETCH.]

## The reduction inward (Rojas 2003, read in full)

The **p-adic Digit Conjecture**: for a FIXED prime $p$, roots
$x \equiv 1 \pmod p$ number at most $(1 + \tau(f))^{c_p}$. Rojas Theorem
1: this ALREADY implies the full tau conjecture (and
$P_{\mathbb{C}} \ne NP_{\mathbb{C}}$), because the valuation spectrum is
subquadratic: the roots of an additive-complexity-$s$ polynomial occupy at
most $s(s+1)/2$ distinct $p$-adic norms (Theorem 2, via lower-hull edge
counts of $p$-adic Newton polygons), and each nonzero root is a unit times
a first-digit class. So the whole problem concentrates in ONE congruence
class near 1. Best unconditional bound from this route: at additive
complexity $s$, at most $1 + s^3(s+1)(7.5)^s s!$ rational roots (Theorem
3); the factorial factor concentrates in counting roots in small disks
about 1 (Theorem 4). [V: math/0304100.]

## What is NOT known

- No nontrivial lower bound on $\tau(n!)$ (Koiran 2004; still quoted as
  open in the 2024 survey). [V]
- No bound on integer roots polynomial in $\tau$; the trivial bound is
  $2^{\tau}$ (degree), the additive-complexity route gives
  $e^{O(s \log s)}$ in $s = \sigma(f) \le \tau(f)$. [V]
- The conjecture is open even with exponent $\kappa = 1$; it FAILS for
  $\kappa < 1$ (geometric-progression roots at linear rate). [V: Rojas.]
- The real analogue is FALSE (logistic/Chebyshev factory); whether a
  p-adic analogue of that factory exists is open. [V: Rojas.]

## 2024-2026 state

Survey consolidation (Buergisser 2024, section 4.6); the conjecture now
yields explicit EXPONENTIAL lower bounds for exponential sums
(Bhattacharjee-Blaeser-Dutta-Mukherjee, ICALP 2024 / arXiv:2601.00387);
nonuniform $P_{\mathbb{C}} \ne NP_{\mathbb{C}}$ implies uniform
constant-free Valiant separations (Buergisser, arXiv:2606.25121). No
claimed proof or refutation. [V: abstracts.]
