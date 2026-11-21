# EXP-029: the weighted Chebyshev sum of the 2026-11-20 formal proof: explicit formula, constant and size (a review control)

Declared 2026-11-21 before any computation. A bounded control inside focus RH-F16 (the review of the formal proof
of the Riemann hypothesis released on 2026-11-20). It is not a result on zeros, it cannot test the truth of the
hypothesis or of the formal proof, and no manuscript follows from it. CPU only.

## What is checked and why

The formal proof ends with a window form of Landau's theorem applied to

    S(x) = sum over n <= x of Lambda(n) (x/n - 1),        G(x) = S(x) - x log x + (1 + gamma) x

(`Formalism.Sz`, `Formalism.Gz`). The note `context/2026-11-21-windowed-landau-endgame.md` proves that step on
paper and derives, from the transform -zeta'(s)/zeta(s) * 1/(s (s - 1)) of S, the explicit formula

    G(x) = - sum over nontrivial zeros rho of x^rho/(rho (rho - 1)) + log 2 pi
           - sum over k >= 1 of x^(-2k)/(2k (2k + 1))                                   (note, formula (2))

and, when every zero used is on the critical line, the two-sided bound

    | G(x) - log 2 pi | <= (2 + gamma - log 4 pi) sqrt(x) + (1 - log 2)/x^2             (note, formula (3)).

This experiment checks the normalization (the transform, the constants x log x - (1 + gamma) x, the residue
log 2 pi at s = 0, the trivial zeros) by computing both sides independently, and records how large G is compared
with the bound the formal proof has to supply (G(x) <= x^(1/2 + epsilon) on windows).

## Definitions fixed here

- Primes by a segmented sieve up to X = 10^8. For an integer N, T(N) = sum over n <= N of Lambda(n)/n and
  psi(N) = sum over n <= N of Lambda(n), accumulated in double precision with compensated summation. For real x
  with N = floor(x): G(x) = x T(N) - psi(N) - x log x + (1 + gamma) x.
- On [N, N + 1) the function G is concave (G'' = -1/x), so its supremum there is at the critical point
  x* = exp(T(N) + gamma) when x* lies in the interval and at an end otherwise, and its infimum is at an end (the
  value at N or the left limit at N + 1). The extremes of (G(x) - log 2 pi)/sqrt(x) over [1, X] are taken over
  these points for every N.
- Zeros: the first 100,000 positive ordinates from A. Odlyzko's public table `zeros1`
  (https://www-users.cse.umn.edu/~odlyzko/zeta_tables/zeros1), downloaded to the data root with its SHA-256
  recorded; they are on the critical line (all zeros below height 3 x 10^12 are, Platt and Trudgian 2021). The
  truncated formula E(x) uses rho = 1/2 + i gamma_j and its conjugate for j <= 100,000 and k <= 20. Its truncation
  term is tail * sqrt(x) with tail = (2 + gamma - log 4 pi) - sum over j <= 100,000 of 2/(1/4 + gamma_j^2), which
  is exact for the sum of 1/|rho|^2 over the remaining zeros when they are on the line.
- Reference values: 50-digit arithmetic (mpmath) for T(N), psi(N) and G(N) at N = 10^3, 10^4, 10^5, 10^6, 10^7.

## Gates

- G1 (sieve): pi(10^6) = 78,498 and pi(10^8) = 5,761,455.
- G2 (precision): the double precision G(N) agrees with the 50-digit value within 10^-6 at the five reference N.
- G3 (zeros): the table has at least 100,000 ordinates, increasing, the first is 14.134725142 and the 100,000th is
  74920.827498994, each within 10^-8.
- G4 (unit tests): the concavity rule against a dense scan of G on [1, 2000]; formula (2) at x = 1, where it reads
  1 + gamma = log 2 pi + (2 + gamma - log 4 pi) - (1 - log 2).

## Predictions

- P1 (normalization). At 400 points spaced evenly in log x over [2, 10^8] and at the 60 points x = q and x = q
  minus 10^-9 for the first 30 prime powers q above 10^6: |G(x) - E(x)| <= tail * sqrt(x) + 10^-6. Confidence 0.97.
- P2 (the bound). For every x in [1, 10^8] (through the extreme points defined above):
  |G(x) - log 2 pi| <= (2 + gamma - log 4 pi) sqrt(x) + (1 - log 2)/x^2. Confidence 0.99. A failure would mean an
  error in the formula, the normalization or the computation, since the zeros that matter at this range are on the
  line.
- P3 (size and sign). Over [10^3, 10^8] the largest value of |G(x) - log 2 pi|/sqrt(x) is between 0.012 and
  0.0462, and both signs occur: the supremum of (G(x) - log 2 pi)/sqrt(x) is at least 0.008 and the infimum at most
  -0.008. Confidence 0.9.
- P4 (constant). The sum over the 100,000 zeros of 2/(1/4 + gamma_j^2), plus the tail computed from the
  Riemann-von Mangoldt main term (the integral over t > gamma_100000 of (2/t^2) (1/(2 pi)) log(t/(2 pi)) dt),
  agrees with 2 + gamma - log 4 pi = 0.0461914179... within 10^-6. Confidence 0.9.

PASS requires the four gates, P1 and P2. P3 and P4 are recorded with their outcome. Thirty minutes of CPU on at
most four processes; progress per decade of x; a budget hit keeps what was computed and is reported as incomplete.

## What this cannot show

Finite agreement does not prove the explicit formula (the note does) and says nothing about zeros that the
computation cannot see. The control does not touch the part of the formal proof that produces the one-sided
bound. It stays a research record of the review.
