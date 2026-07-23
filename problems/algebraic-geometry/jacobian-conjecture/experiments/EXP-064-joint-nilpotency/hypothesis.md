# EXP-064 - The gate: termination as joint nilpotency (hardening task 2)

- **Question.** Decide the simultaneous-symbolic interior certificate: does the
  corrector ladder terminate for ALL interior coefficients at once?
- **Motivation (the declared derivation).** With all-orders solvability proved (the
  kernel is the constants, EXP-058), fix a LINEAR pinned right-inverse sigma of
  Lambda -> Lambda M0 (one rref-with-transform of M0^T at t = 1; the gauge covers all
  t != 0). The ladder recursion Lambda_alpha M0 = -sum_i Lambda_{alpha - e_i} M_i
  becomes Lambda_alpha = (-1)^{|alpha|} (words in the FIXED operators A_i = sigma T_i)
  applied to Lambda_0. Hence: TERMINATION for all eps simultaneously <=> the A_i are
  JOINTLY NILPOTENT on the Krylov closure V_inf of Lambda_0 <=> the descending chain
  W_{k+1} = sum_i A_i W_k (W_0 = V_inf) reaches ZERO in at most dim V_inf steps. Both
  the Krylov closure and the chain are finite exact computations. If W_K = 0: the
  polynomial covector Lambda(eps) exists with degree < K: THE SIMULTANEOUS-SYMBOLIC
  CERTIFICATE EXISTS and the reduced systems close for ALL interior values (at t = 1,
  hence all t != 0 by the gauge), discharging the audit's central objection. If the
  chain stabilizes nonzero: THIS sigma's ladder does not terminate; re-pin or fall
  back to chart covers (recorded honestly).
- **Falsifiable predictions.**
  1. [MV] The rref-with-transform right-inverse reproduces two known correctors
     (spot checks against EXP-056's persisted Lambda_i).
  2. [MV] The Krylov closure V_inf is computed and SMALL (tens of dimensions,
     predicted from the localized corrector supports).
  3. [MV] The descending chain reaches ZERO in at most dim V_inf steps: JOINT
     NILPOTENCY: termination proved, with the explicit order bound K.
  4. [D] Assembly: with 3, the amended statement upgrades per the audit's own
     criterion (the simultaneous-symbolic certificate exists); the remaining
     hardening tasks 3-8 stay queued; outreach still last and gated.
- **Method.** sympy over QQ at t = 1; one rref of [M0^T | I]; sparse T_i
  applications; exact span computations. Background per the cap discipline.
- **Success criterion.** 1-3 verified either way (a nonzero stable chain is a valid,
  recorded outcome that redirects to re-pinning/chart covers).
- **Failure criterion.** The right-inverse failing the spot checks (implementation
  bug, fix before any claim).

Declared 2026-07-22 before the run.
