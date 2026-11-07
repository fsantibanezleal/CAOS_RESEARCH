# TCB-004: the upper-bound ladder for tau'(n!), Cheng 2004 read (2026-11-07)

Marks: [V] read in the primary text; [V2] reported by a secondary source we read; [U] unverified.

Source read: Q. Cheng, "On the ultimate complexity of factorials", Theoret. Comput. Sci. 326 (2004) 419-429,
DOI 10.1016/j.tcs.2004.07.032; author copy https://qcheng2023.github.io/paper/factorial.pdf (preliminary version in
STACS 2003, LNCS 2607), archived in the data root under `caos-research/tau-conjecture/sources/tcb004/`
(SHA-256 07042ff35d3fad4ddb5c749295ae4020aa188ed698530ae3e0cde6b2209116a1). Formulas checked on the rendered pages.

## The ladder

1. **Unconditional, for n! itself [V via Cheng].** "So far the best algorithm we know computes n! in
   O(sqrt(n) log^2 n) ring operations over Z [14,4]" (Cheng, Section 1), with [14] = V. Strassen, Einige Resultate
   ueber Berechnungskomplexitaet, Jber. Deutsch. Math.-Verein. 78(1) (1976/77) 1-8, and [4] = Buergisser, Clausen,
   Shokrollahi, Algebraic Complexity Theory, 1997. Cheng adds that no better upper bound had been reported for the
   ultimate complexity of n!. Our dossier quoted this, via Markstroem, as a bound for a multiple of n!; Cheng states
   it for n! itself, which implies the multiple form. Strassen's original is not read [U].
2. **Conditional, for a nonzero multiple of n! [V].** Let L_x[c] = exp(c sqrt(log x log log x)) (natural logarithm).
   Conjecture 1 (smooth numbers in short intervals): for every constant a > 0,
   Psi(p + 1 + 2 sqrt(p), L_p[a]) - Psi(p + 1 - 2 sqrt(p), L_p[a]) = sqrt(p) L_p[-1/(2a) + o(1)].
   Theorem 1: if Conjecture 1 holds, there are absolute constants c1, c2 such that for every n a nonzero multiple
   of n! is computed by a straight-line program (additions, subtractions, multiplications, constant 1) of length at
   most L_n[c1], and the program is constructed in time L_n[c2] by a probabilistic Turing machine. The proof runs
   Lenstra's elliptic-curve method through division polynomials (P_s(x) of length O(log s) from 1, x, a, b).
3. **Why it matters [V].** Shub and Smale: if n! is ultimately hard (no nonzero multiple of n! has
   straight-line complexity (log n)^c), then the algebraic version of NP != P holds (Cheng, Section 1, citing [12]).
   Cheng's subexponential bound says the ultimate complexity is not above L_n[c1] under Conjecture 1; it does not
   decide polylogarithmic.

## Not obtained

- Q. Cheng, "Straight-line programs and torsion points on elliptic curves", Comput. Complexity 12 (2003) 150-161,
  DOI 10.1007/s00037-003-0180-0: no open copy (author site, Unpaywall). Its subject, from its bibliographic record
  and search listings [V2], is the link between Buergisser's L-conjecture and torsion bounds on elliptic curves, not
  an upper bound for multiples of n!; our references row describing it as "nontrivial upper bound for multiples of
  n!" is marked unverified until it is read.
- V. Strassen 1976/77 (above): no open copy found.
