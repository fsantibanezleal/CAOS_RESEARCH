# EXP-038 - Pair-level corner theory: does the second component add obstruction power?

- **Question.** JCB-039. In the diagonal picture (EXP-035), a cornered Keller candidate has
  P_top = alpha B^p, and by top Jacobian-dependence its partner must have Q_top = beta B^q
  on the same base B. Does imposing the pair structure (Q's top cornered on B, the
  Abhyankar-similarity shape) produce obstructions the single-component window analysis
  (Q entirely free) does not already see, or does it only shrink the search space?
- **Motivation (derivation, declared).** Write P = alpha B^p + P_sub, Q = beta B^q + Q_sub
  (B = x^i y^j, i, j >= 1 primitive, D_P = p(i + j), D_Q = q(i + j)). The top class of
  J(P, Q) = 1 is J(B^p, B^q) = 0 automatically. The NEXT class is
  alpha J(B^p, Q_sub) - beta J(B^q, P_sub) = 0, and both operators are DIAGONAL
  (EXP-035): monomial (a, b) of Q_sub hits the same output as monomial (c, d) of P_sub
  iff (a, b) = (c, d) + (q - p)(i, j). So the second class is a MATCHED-PAIR LAW:
  alpha p (i b - j a) q_{a,b} = beta q (i d - j c) p_{c,d} on matched pairs, and
  (i b - j a) q_{a,b} = 0, (i d - j c) p_{c,d} = 0 on unmatched monomials. The pair
  structure therefore determines Q's subtop from P's subtop up to the corner kernel;
  everything it says about Q is already available to a free-Q window. The conjecture to
  test: the pair constraint does NOT lower the obstruction depth (the constant is
  manufactured on the staircase, EXP-035/037, which the free window already sees); its
  value is search-space reduction, not new obstructions.
- **Falsifiable predictions.**
  1. [MV] (Top dependence on the library) For every library Keller pair: the top-degree
     forms satisfy J(P_top, Q_top) = 0 and have proportional radicals (common base), and
     the top-2 class bookkeeping holds identically.
  2. [MV] (Matched-pair law) The derived second-class law is exact: for generic symbolic
     subtops and (i, j, p, q) on a grid, the class D_P + D_Q - 3 piece of J(P, Q) equals
     the matched-pair expression, term by term.
  3. [MV] (Depth comparison) For cornered swallowed samples, the minimal window N at which
     the completion system turns inconsistent is THE SAME with Q free and with Q's top
     constrained to the similarity shape (beta B^q at admissible degrees, 0 at
     inadmissible top degrees): the pair constraint adds no obstruction depth.
  4. [C] (Practical value) The constrained system is strictly smaller (fewer unknowns at
     equal window), quantified per sample: the pair theory's contribution is efficiency.
- **Method.** sympy over QQ; library from keller2lib; exact class decompositions; window
  solves with and without top constraints; minimal-N sweeps N = 3..8. Caps 570 s per part.
- **Success criterion.** 1-2 verified; 3 answered either way with the depth table (a NO
  answer, constrained depth < free depth, is a positive finding: the pair adds power);
  4 quantified.
- **Failure criterion.** A matched-pair mismatch (derivation wrong); a library pair
  violating top dependence (bookkeeping bug).

Declared 2026-07-22 before the run.
